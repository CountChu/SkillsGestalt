"""Verify a reformat: that only formatting changed, and that a pair still lines up.

reformat-md's last step runs it on each original and its #v1 copy. In clean mode only
line breaks and the spaces around them may change, so every other character must read as
it did: any change is listed, with its line on each side, and fails. In raw mode it sets
aside what md-style.md's raw transforms may change - list, heading and quote markers, the
`*` of emphasis, the backticks of inline code, and the fence lines transform 6 adds - and
lists every stretch of text lost or added, which fails. A lost stretch that is nothing but
a citation marker is listed for review rather than failed: transform 9 removes those on
purpose; so is a change of escapes or math alone - `\\`, `$`, brackets, `~` and `-` - which
transforms 5 and 7 make, and a change of other punctuation. It then compares the
headings, which a clean file never changes, and the bold markers: a line break that leaves
an opening `**` at the end of a line, or a closing one at the start of a line, unmakes
the bold, and fails.

Given a twin, it also compares the two #v1 files block by block within each section.
After transform 10 a block holds one line per sentence, so a block whose line count
differs between the two halves is a paragraph or a list whose sentences the translation
did not keep one for one.

Usage:
    python3 check_reformat.py --mode raw|clean ORIGINAL REFORMATTED [--twin ORIGINAL_TW REFORMATTED_TW]

Exit status: 0 nothing to fix, 1 a finding, 2 a file that cannot be read.
"""
from __future__ import annotations

import argparse
import difflib
import re
import sys
import unicodedata
from pathlib import Path
from typing import List, Optional, Tuple

FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
FENCE_LINE_RE = re.compile(r"^\s*(`{3,}|~{3,})[\w+-]*\s*$")
HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)\s*$")
MARKER_RE = re.compile(r"^\s*(?:(?:[-*+]|\d{1,9}[.)])\s+|#{1,6}\s+|>\s?)")
CLEAN_TOKEN_RE = re.compile(r"[A-Za-z0-9]+|\S")
RAW_TOKEN_RE = re.compile(r"[A-Za-z0-9]+|[^\sA-Za-z0-9`*]")
ESCAPE_CHARS = set("\\$()~-")
CODE_SPAN_RE = re.compile(r"(`+).+?\1")
CITATION_RE = re.compile(r"^\d{1,2}(?:[-–]\d{1,2})?(?:,\d{1,2}(?:[-–]\d{1,2})?)*$")
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
SHOWN = 40                                  # findings listed per check before "... and N more"

Token = Tuple[str, int]                     # the token, and the line it stands on


def read(path: Path) -> List[str]:
    try:
        return path.read_bytes().decode("utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as e:
        print(f"cannot read {path}: {e}", file=sys.stderr)
        sys.exit(2)


def frontmatter_end(lines: List[str]) -> int:
    """The index of the frontmatter's closing ---, or -1 when there is none."""
    if lines and lines[0].strip() == "---":
        return next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), -1)
    return -1


def tokens(lines: List[str], raw: bool) -> List[Token]:
    """What a file says: in clean mode every character but whitespace; in raw mode, words
    and every other character but whitespace and the markup raw transforms may change."""
    out: List[Token] = []
    for no, line in enumerate(lines, 1):
        if raw:
            if FENCE_LINE_RE.match(line):
                continue                     # a fence line carries no text
            line = MARKER_RE.sub("", line, count=1)
        for m in (RAW_TOKEN_RE if raw else CLEAN_TOKEN_RE).finditer(line):
            out.append((m.group(0), no))
    return out


def textual(toks: List[str]) -> bool:
    """Does the stretch hold a letter or a digit, of any script?"""
    return any(unicodedata.category(c)[0] in "LN" for t in toks for c in t)


def shown(toks: List[str]) -> str:
    out = ""
    for t in toks:
        if out and out[-1].isascii() and out[-1].isalnum() and t[0].isascii() and t[0].isalnum():
            out += " "
        out += t
    return out


def content(before: List[str], after: List[str], raw: bool):
    """Every stretch lost or added: (kind, before line, after line, lost, added)."""
    a, b = tokens(before, raw), tokens(after, raw)
    ta, tb = [t for t, _ in a], [t for t, _ in b]
    if ta == tb:
        return []
    found = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ta, tb, autojunk=False).get_opcodes():
        if op == "equal":
            continue
        lost, added = ta[i1:i2], tb[j1:j2]
        la = a[i1][1] if i1 < i2 else (a[i1 - 1][1] if i1 else 1)
        lb = b[j1][1] if j1 < j2 else (b[j1 - 1][1] if j1 else 1)
        if not raw:
            kind = "changed"
        elif not added and CITATION_RE.match("".join(lost)):
            kind = "citation"
        elif set("".join(lost + added)) <= ESCAPE_CHARS:
            kind = "escape"
        elif textual(lost) or textual(added):
            kind = "text"
        else:
            kind = "punctuation"
        found.append((kind, la, lb, shown(lost), shown(added)))
    return found


def headings(lines: List[str]) -> List[Tuple[int, str, int]]:
    """(level, title, line) of each heading outside the frontmatter and fenced blocks."""
    out, fence, fm = [], "", frontmatter_end(lines)
    for no, line in enumerate(lines, 1):
        if no - 1 <= fm:
            continue
        f = FENCE_RE.match(line)
        if fence:
            if f and f.group(1)[0] == fence[0]:
                fence = ""
            continue
        if f:
            fence = f.group(1)
            continue
        m = HEADING_RE.match(line)
        if m:
            title = re.sub(r"^\*\*(.*)\*\*$", r"\1", m.group(2))
            out.append((len(m.group(1)), title.replace("\\.", ".").replace("\\-", "-"), no))
    return out


def dangling_bold(lines: List[str]) -> List[int]:
    """Lines where a ** cannot work: an opening one at the end of a line, or a closing one
    at its start - paragraph by paragraph, outside fenced blocks and inline code."""
    out, fence, bold = [], "", False
    for no, line in enumerate(lines, 1):
        s = line.strip()
        f = FENCE_RE.match(line)
        if fence:
            if f and f.group(1)[0] == fence[0]:
                fence = ""
            continue
        if f:
            fence, bold = f.group(1), False
            continue
        if not s:
            bold = False                     # a blank line ends the paragraph
            continue
        body = CODE_SPAN_RE.sub(lambda m: "x" * len(m.group(0)), s)
        body = re.sub(r"^(?:[-*+]|\d+[.)])\s+", "", body)
        for m in re.finditer(r"\*\*", body):
            if (not bold and m.end() == len(body)) or (bold and m.start() == 0):
                out.append(no)
            bold = not bold
    return out


def sections(lines: List[str]) -> List[Tuple[Optional[str], List[Tuple[int, int]]]]:
    """Each section - the preamble first - with its blocks as (first line, last line).

    A block is a run of non-blank lines; a fenced block belongs to the run it stands in,
    blank lines and all.
    """
    secs: List[Tuple[Optional[str], List[Tuple[int, int]]]] = [(None, [])]
    fence, start, fm = "", 0, frontmatter_end(lines)
    for no, line in enumerate(lines, 1):
        if no - 1 <= fm:
            continue
        f = FENCE_RE.match(line)
        if fence:
            if f and f.group(1)[0] == fence[0]:
                fence = ""
            continue
        if f:
            fence = f.group(1)
            start = start or no
            continue
        m = HEADING_RE.match(line)
        if m or not line.strip():
            if start:
                secs[-1][1].append((start, no - 1))
                start = 0
            if m:
                secs.append((line.strip(), []))
            continue
        start = start or no
    if start:
        secs[-1][1].append((start, len(lines)))
    return secs


def alignment(en: List[str], tw: List[str], en_name: str) -> List[str]:
    """Blocks whose line counts differ between the two halves of a pair."""
    se, st = sections(en), sections(tw)
    # The twin's pairing line - a block before its first heading that links back to the
    # English file - has nothing to line up with, when the English file has no such block.
    extra = len(st[0][1]) - len(se[0][1])
    pre = []
    for first, last in st[0][1]:
        if extra > 0 and any(Path(t).name == en_name for no in range(first, last + 1)
                             for t in LINK_RE.findall(tw[no - 1])):
            extra -= 1
            continue
        pre.append((first, last))
    st[0] = (None, pre)
    if len(se) != len(st):
        return [f"the two halves have {len(se) - 1} and {len(st) - 1} headings - "
                f"line them up first (the chinese skill's parity check)"]
    found = []
    for (head, be), (_, bt) in zip(se, st):
        where = head or "(before the first heading)"
        if len(be) != len(bt):
            found.append(f"{where}: {len(be)} blocks in the English file, {len(bt)} in the twin")
            continue
        for (e1, e2), (t1, t2) in zip(be, bt):
            if e2 - e1 != t2 - t1:
                found.append(f"{where}: English lines {e1}-{e2} ({e2 - e1 + 1}), "
                             f"twin lines {t1}-{t2} ({t2 - t1 + 1})")
    return found


def report(status: str, title: str, items: List[str]) -> None:
    print(f"[{status}] {title}")
    for item in items[:SHOWN]:
        print(f"       {item}")
    if len(items) > SHOWN:
        print(f"       ... and {len(items) - SHOWN} more")


def check_file(original: Path, reformatted: Path, raw: bool) -> int:
    before, after = read(original), read(reformatted)
    name = f"{original.name} -> {reformatted.name}"
    found = content(before, after, raw)
    failures = 0
    def listed(kind):
        return [f"line {la} -> {lb}: lost {lost!r} added {added!r}" for k, la, lb, lost, added in found if k == kind]
    changed, text = listed("changed"), listed("text")
    cites = [f"line {la} -> {lb}: lost {lost!r}" for k, la, lb, lost, _ in found if k == "citation"]
    escapes, punct = listed("escape"), listed("punctuation")
    if changed:
        report("FAIL", f"{name}: characters other than whitespace changed in {len(changed)} places - "
               "clean mode changes only line breaks and the spaces around them", changed)
        failures += 1
    elif text:
        report("FAIL", f"{name}: text lost or added in {len(text)} places", text)
        failures += 1
    else:
        report("PASS", f"{name}: " + ("only whitespace changed" if not raw else "no text lost or added"), [])
    if escapes:
        report("WARN", f"{name}: escapes or math changed in {len(escapes)} places - transforms 5 and 7; read each", escapes)
    if cites:
        report("WARN", f"{name}: {len(cites)} citation markers removed - read each; restore a real number by hand", cites)
    if punct:
        report("WARN", f"{name}: punctuation changed in {len(punct)} places", punct)

    hb, ha = headings(before), headings(after)
    if raw:
        changed = [f"line {nb} -> {na}: {tb!r} became {ta!r}" for (_, tb, nb), (_, ta, na) in zip(hb, ha) if tb != ta]
        if len(hb) != len(ha):
            changed.insert(0, f"{len(hb)} headings became {len(ha)}")
    else:
        changed = [f"line {nb} -> {na}: {'#' * lb} {tb} became {'#' * la} {ta}"
                   for (lb, tb, nb), (la, ta, na) in zip(hb, ha) if (lb, tb) != (la, ta)]
        if len(hb) != len(ha):
            changed.insert(0, f"{len(hb)} headings became {len(ha)}")
    if changed:
        report("FAIL", f"{name}: headings changed", changed)
        failures += 1
    else:
        report("PASS", f"{name}: headings kept ({len(ha)})", [])

    broken = dangling_bold(after)
    if len(broken) > len(dangling_bold(before)):
        report("FAIL", f"{name}: a line break left a ** where it cannot open or close - the bold no longer renders",
               [f"line {no}" for no in broken])
        failures += 1
    else:
        report("PASS", f"{name}: bold markers intact", [])
    return failures


def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser(description="Verify a reformat by reformat_md.py.")
    ap.add_argument("--mode", required=True, choices=("raw", "clean"), help="the mode reformat_md.py took")
    ap.add_argument("original")
    ap.add_argument("reformatted")
    ap.add_argument("--twin", nargs=2, metavar=("ORIGINAL_TW", "REFORMATTED_TW"),
                    help="the twin, before and after: check it too, and that the pair lines up")
    args = ap.parse_args(argv[1:])
    raw = args.mode == "raw"
    failures = check_file(Path(args.original), Path(args.reformatted), raw)
    if args.twin:
        failures += check_file(Path(args.twin[0]), Path(args.twin[1]), raw)
        misaligned = alignment(read(Path(args.reformatted)), read(Path(args.twin[1])), Path(args.original).name)
        if misaligned:
            report("FAIL", f"the pair does not line up: {len(misaligned)} blocks differ in their sentence lines", misaligned)
            failures += 1
        else:
            report("PASS", "the pair lines up block for block", [])
    print(f"verdict: {'FAIL' if failures else 'PASS'} - {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
