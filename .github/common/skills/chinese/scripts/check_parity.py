"""Compare an English Markdown file against its -tw.md twin and exit non-zero on any structural mismatch.

A source with a frontmatter - every SKILL.md - is compared section by section: its twin writes the
translated description as a folded block and adds a pairing line under the frontmatter, so its lines
cannot keep their numbers. A source without one is compared line for line as well: the same line
count, and the same kind of line at every number.

Glossary terms are compared twice. A term used bold fewer times in the twin than in the source is a
failure: bold marks the term, so a drop in that count is a term that was translated. A term used
unbolded fewer times is only a warning, because the same English word may also be an ordinary word
that is rightly translated - which of the two each use was is a reading, not a count.

With --keep, every rendering the shared keep-English list flags is searched for in the twin's prose,
and each one found is a warning too: the list keeps that term in English, but a flagged word can
still be right in a sentence about something else.

A `**` the twin sets against a punctuation mark where CommonMark will not read it as bold is a warning
as well: the page shows the asterisks, and no structural comparison notices.

So is English set against a Chinese character with no space between them, and a space between two
Chinese characters. An inline-code span and a placeholder token count as English; a full-width
punctuation mark needs no space on either side.

Every section holds the same inline-code spans and the same section citations as the source's - a
translation copies both unchanged, so one missing, or one the twin alone has, was lost or translated.
They are read paragraph by paragraph, so a span the source wraps over two lines is still one span, and
compared as sets: Chinese often repeats a name where English says "which", and a repeat loses nothing.
A citation is §2.3; in a file filled from a template, whose sections are numbered, a bare 2.3 is one
too. The pairing line is left out, and a span naming the twin in the source matches one naming the
source in the twin, since each file names the other.

A source compared line for line whose header quote names the template it was filled from - a
`[[name]]` ending in -tmp - has its shared lines checked too: each line it takes unchanged from the
template is worded in the twin as the template's twin words it, and each one worded otherwise is a
warning. A template that cannot be used - not found, without a twin, or not line for line with its
twin - is a warning as well, since then no line was checked.

A placeholder in the retired form, ___UPPER_SNAKE___, is a failure in either file, wherever it stands:
Markdown shows it in bold italics instead of as written. The failure names the script that converts
it to {UPPER_SNAKE} in the file and its twin, common/scripts/placeholders.py.
"""

import argparse
import io
import re
import sys
import unicodedata

from scan_md import (CODE_SPAN_RE, HEADING_RE, LINK_RE, OLD_RE, PLACEHOLDERS_PY, TOKEN_RE, WIKILINK_RE, fence_spans, first_link,
                     glossary_terms, keep_english, prose_lines, shared_lines, source_pairing_link, split_frontmatter, table_blocks,
                     template_pair, top_end)

TW_SUFFIX = "（繁體中文）"
LIST_RE = re.compile(r"(\s*)([-*+]|\d+[.)]) ")
QUOTE_RE = re.compile(r"^\s*(?:>\s?)+")
BOLD_RE = re.compile(r"(?<!\*)\*\*(?!\*)")
# A Chinese character, which a space keeps apart from English; full-width punctuation is not one.
HAN = r"㐀-䶿一-鿿"
# \x01 stands for what the page does not show between two letters: a backtick, a bold marker, a link's
# brackets and target.
GLUED_RE = re.compile(rf"[A-Za-z0-9]\x01*[{HAN}]|[{HAN}]\x01*[A-Za-z0-9]")
SPACED_RE = re.compile(rf"[{HAN}]\x01* +\x01*[{HAN}]")
# A section citation, §2.3; and a bare section number, 2.3, as a file filled from a template cites its own
# sections - the RSDC Checker's pattern, which leaves out a decimal, a version and a number in a path.
SECTION_CITE_RE = re.compile(r"§\s?([1-9])\.(\d+)")
BARE_CITE_RE = re.compile(r"(?<![A-Za-z0-9_.§−\-+/#])([1-4])\.([1-9]|(?<=2\.)1[0-2])(?!\d|\.\d|[A-Za-z])")


def read(path):
    raw = io.open(path, "rb").read()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig"), has_bom


def file_name(target):
    return target.replace("\\", "/").split("#")[0].rstrip("/").rsplit("/", 1)[-1]


def headings(lines, inside):
    return [(i, l) for i, l in enumerate(lines, 1) if i not in inside and re.match(r"^#{1,6} +\S", l)]


def links(lines, inside, drop=None):
    """Every link target outside a fence - a wiki link's [[name]] included - in order, less the one pairing link
    `drop` names as (line, target)."""
    out = []
    for i, line in enumerate(lines, 1):
        if i in inside:
            continue
        found = [(m.start(), m.group(2)) for m in LINK_RE.finditer(line)]
        found += [(m.start(), f"[[{m.group(1).strip()}]]") for m in WIKILINK_RE.finditer(line)]
        for _, target in sorted(found):
            if drop and (i, target) == drop:
                drop = None
                continue
            out.append(target)
    return out


def fenced_blocks(lines, marks):
    """The text of each fenced block, its fence lines included, in order."""
    return ["\n".join(lines[a - 1 : b]) for a, b in zip(marks[::2], marks[1::2])]


def tokens(lines, inside):
    out = []
    for i, line in enumerate(lines, 1):
        if i in inside:
            continue
        out.extend(m.group(0) for m in TOKEN_RE.finditer(line))
    return out


def bold_uses(lines, inside, term):
    needle = f"**{term}**"
    return sum(line.count(needle) for i, line in enumerate(lines, 1) if i not in inside)


def plain_uses(lines, inside, term):
    """Uses outside fences and inline code that are not exactly **term** - including a term inside a
    longer bold phrase. The boundary is ASCII only, so a term set against a Chinese character still counts."""
    pat = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(term) + r"(?![A-Za-z0-9_])")
    every = sum(len(pat.findall(CODE_SPAN_RE.sub(" ", line))) for i, line in enumerate(lines, 1) if i not in inside)
    return every - bold_uses(lines, inside, term)


def items_per_section(lines, inside):
    """Bullet and numbered-item counts per section, in order: (heading, count), the preamble first.

    Sections are matched by position, not by heading text, so a title the twin marks with a suffix
    still lines up with the source's; whether the headings match is a check of its own."""
    counts = [["(preamble)", 0]]
    for i, line in enumerate(lines, 1):
        if i in inside:
            continue
        if re.match(r"^#{1,6} +\S", line):
            counts.append([line, 0])
        elif re.match(r"^\s*(?:[-*] |\d+\. )", line):
            counts[-1][1] += 1
    return counts


def inline_texts(lines, inside):
    """(first line number, text) of each run of lines CommonMark reads as one inline text - a paragraph, a list
    item's text, a table row - its lines joined by a space, quote and list markers taken out; headings and
    fenced lines are not read."""
    block, start = [], None
    for i, line in enumerate(lines, 1):
        body = QUOTE_RE.sub("", line)
        if i in inside or not body.strip() or HEADING_RE.match(line) or body.strip().startswith("|"):
            if block:
                yield start, " ".join(block)
                block = []
            if i not in inside and body.strip().startswith("|"):
                yield i, body
            continue
        if LIST_RE.match(body):
            if block:
                yield start, " ".join(block)
                block = []
            body = LIST_RE.sub("", body, count=1)
        if not block:
            start = i
        block.append(body)
    if block:
        yield start, " ".join(block)


def per_section(lines, inside, collect, skip=frozenset()):
    """For each section by position - the preamble first - the set of what `collect` finds in its inline texts;
    a text opening on a line `skip` names is left out."""
    section, k = {}, 0
    for i, line in enumerate(lines, 1):
        if i not in inside and re.match(r"^#{1,6} +\S", line):
            k += 1
        section[i] = k
    out = [set() for _ in range(k + 1)]
    for start, text in inline_texts(lines, inside):
        if start not in skip:
            out[section[start]].update(collect(text))
    return out


def section_drift(en_sets, tw_sets, en_heads, en_name, tw_name):
    """'heading: en only [...]; tw only [...]' for each section whose sets differ, matched by position. A span
    naming the twin in the source and the same span naming the source in the twin are one: each names the other."""
    names = ["(preamble)"] + [line.strip() for _, line in en_heads]
    out = []
    for k in range(max(len(en_sets), len(tw_sets))):
        a = en_sets[k] if k < len(en_sets) else set()
        b = tw_sets[k] if k < len(tw_sets) else set()
        only_en, only_tw = a - b, b - a
        for s in list(only_en):
            swapped = s.replace(tw_name, en_name)
            if tw_name in s and swapped in only_tw:
                only_en.discard(s)
                only_tw.discard(swapped)
        if only_en or only_tw:
            name = names[k] if k < len(names) else f"section {k}"
            out.append(f"{name[:50]}: en only {sorted(only_en)}; tw only {sorted(only_tw)}")
    return out


def line_kind(line, fenced):
    """What a line is, for the line-for-line comparison: the twin must have the same kind at the same number."""
    if fenced:
        return "fenced"
    if not line.strip():
        return "blank"
    if HEADING_RE.match(line):
        return "heading"
    s = line.strip()
    if s.startswith("|") and s.endswith("|"):
        return "table row"
    if s.startswith(">"):
        return "quote"
    m = LIST_RE.match(line)
    if m:
        return f"{'bullet' if m.group(2) in '-*+' else 'numbered item'} at indent {len(m.group(1))}"
    return f"text at indent {len(line) - len(line.lstrip())}"


def is_punct(ch):
    return unicodedata.category(ch)[0] in "PS"


def inline_blocks(lines, inside):
    """Each run of lines CommonMark reads as one inline text - a paragraph, a list item's text, a table
    row, a heading - as [(line number, text)], with quote and list markers and inline code taken out."""
    block = []
    for i, line in enumerate(lines, 1):
        body = QUOTE_RE.sub("", line)
        if i in inside or not body.strip() or HEADING_RE.match(line) or body.strip().startswith("|"):
            if block:
                yield block
                block = []
            if i not in inside and body.strip():
                yield [(i, CODE_SPAN_RE.sub("x", body))]
            continue
        if LIST_RE.match(body):
            if block:
                yield block
                block = []
            body = LIST_RE.sub("", body, count=1)
        block.append((i, CODE_SPAN_RE.sub("x", body)))
    if block:
        yield block


def unrendered_bold(lines, inside):
    """(line number, excerpt) for each line holding a `**` CommonMark leaves as literal asterisks.

    A run opens bold only when it is left-flanking and closes it only when it is right-flanking, so a
    run set against a punctuation mark needs whitespace or punctuation on its other side: `。**後`
    never closes. Within each inline block a run that can close takes the nearest open one, as
    CommonMark does, so nested bold is read the way the page renders it.
    """
    out = []
    for block in inline_blocks(lines, inside):
        text = "\n".join(t for _, t in block)
        starts, at = [], 0
        for _, t in block:
            starts.append(at)
            at += len(t) + 1
        stack, literal = [], []
        for m in BOLD_RE.finditer(text):
            at = m.start()
            before = text[at - 1] if at else "\n"
            after = text[at + 2] if at + 2 < len(text) else "\n"
            opens = not after.isspace() and (not is_punct(after) or before.isspace() or is_punct(before))
            closes = not before.isspace() and (not is_punct(before) or after.isspace() or is_punct(after))
            if closes and stack:
                stack.pop()
            elif opens:
                stack.append(at)
            else:
                literal.append(at)
        for at in sorted(literal + stack):
            k = max(n for n, s in enumerate(starts) if s <= at)
            line_no, t = block[k]
            col = at - starts[k]
            if not out or out[-1][0] != line_no:
                out.append((line_no, t[max(0, col - 8) : col + 12]))
    return out


def as_shown(line):
    """The line as the page shows its words, character for character: the text of an inline-code span
    and of a placeholder token becomes x - English, whatever it holds - and what the page does not
    show between two words, a backtick, a bold marker or a link's brackets and target, becomes \\x01."""
    def hide(n):
        return "\x01" * n

    def wiki(m):
        shown = m.group(2) or m.group(1)
        return hide(2) + shown + hide(len(m.group(0)) - 2 - len(shown))

    s = CODE_SPAN_RE.sub(lambda m: hide(len(m.group(1))) + "x" * len(m.group(2)) + hide(len(m.group(1))), line)
    s = TOKEN_RE.sub(lambda m: "x" * len(m.group(0)), s)
    s = WIKILINK_RE.sub(wiki, s)
    s = LINK_RE.sub(lambda m: hide(1) + m.group(1) + hide(len(m.group(0)) - 1 - len(m.group(1))), s)
    return s.replace("**", hide(2))


def spacing(lines, inside):
    """(line number, excerpt, what is wrong) for each prose line where English touches a Chinese
    character, or a space stands between two Chinese characters: at most one of each a line."""
    out = []
    for i, line in enumerate(lines, 1):
        if i in inside or HEADING_RE.match(line):
            continue
        shown = as_shown(line)
        for pattern, wrong in ((GLUED_RE, "English set against a Chinese character: put a space between them"),
                               (SPACED_RE, "a space between two Chinese characters: take it out")):
            m = pattern.search(shown)
            if m:
                out.append((i, line[max(0, m.start() - 8) : m.end() + 8], wrong))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--en", required=True, help="path to the English source file")
    ap.add_argument("--tw", required=True, help="path to its -tw.md twin")
    ap.add_argument("--keep", help="path to the shared keep-English list; warns about each flagged rendering")
    args = ap.parse_args()

    en_text, en_bom = read(args.en)
    tw_text, tw_bom = read(args.tw)
    en_lines, tw_lines = en_text.splitlines(), tw_text.splitlines()
    en_marks, en_inside = fence_spans(en_lines)
    tw_marks, tw_inside = fence_spans(tw_lines)
    source_name = file_name(args.en)

    failures = []

    def check(name, ok, detail=""):
        print(f"[{'PASS' if ok else 'FAIL'}] {name}{(' - ' + detail) if detail else ''}")
        if not ok:
            failures.append(name)

    en_fm, _, _ = split_frontmatter(en_text)
    tw_fm, _, _ = split_frontmatter(tw_text)
    line_for_line = en_fm is None
    if line_for_line:
        check("no frontmatter, as in the source", tw_fm is None)
    else:
        parsed = isinstance(en_fm, dict) and isinstance(tw_fm, dict)
        parsed = parsed and "__error__" not in en_fm and "__error__" not in tw_fm
        check("frontmatter parses", parsed, "" if parsed else f"en={en_fm} tw={tw_fm}")
        if parsed:
            check("frontmatter keys match", sorted(en_fm) == sorted(tw_fm), f"{sorted(en_fm)} vs {sorted(tw_fm)}")
            check("name unchanged", en_fm.get("name") == tw_fm.get("name"), f"{en_fm.get('name')} vs {tw_fm.get('name')}")
            if "description" in en_fm:
                check("description non-empty", bool(str(tw_fm.get("description", "")).strip()))

    en_heads, tw_heads = headings(en_lines, en_inside), headings(tw_lines, tw_inside)
    en_h, tw_h = [l for _, l in en_heads], [l for _, l in tw_heads]
    first = next((i for i, line in enumerate(en_lines, 1) if line.strip()), None)
    titled = line_for_line and bool(en_heads) and en_heads[0][0] == first and en_h[0].startswith("# ")
    same = len(en_h) == len(tw_h) and all(
        a == b or (k == 0 and titled and b == a + TW_SUFFIX) for k, (a, b) in enumerate(zip(en_h, tw_h))
    )
    check("headings identical and in order", same, f"{len(en_h)} vs {len(tw_h)}")
    if not same:
        for k, (a, b) in enumerate(zip(en_h, tw_h)):
            if a != b and not (k == 0 and titled and b == a + TW_SUFFIX):
                print(f"       en: {a}\n       tw: {b}")
        for extra in en_h[len(tw_h):]:
            print(f"       missing in tw: {extra}")
        for extra in tw_h[len(en_h):]:
            print(f"       extra in tw:   {extra}")

    check("fence counts equal", len(en_marks) == len(tw_marks), f"{len(en_marks)} vs {len(tw_marks)}")
    check("fences balanced in tw", len(tw_marks) % 2 == 0, f"{len(tw_marks)} fence markers")
    en_b, tw_b = fenced_blocks(en_lines, en_marks), fenced_blocks(tw_lines, tw_marks)
    changed = [k for k, (a, b) in enumerate(zip(en_b, tw_b), 1) if a != b]
    check("fenced blocks copied byte for byte", not changed, ", ".join(f"block {k}" for k in changed))

    en_t = table_blocks(en_lines, en_inside)
    tw_t = table_blocks(tw_lines, tw_inside)
    check("table count equal", len(en_t) == len(tw_t), f"{len(en_t)} vs {len(tw_t)}")
    for idx, (a, b) in enumerate(zip(en_t, tw_t)):
        check(
            f"table {idx + 1} column count",
            set(a[1]) == set(b[1]) and len(set(b[1])) == 1,
            f"en L{a[0]} cols {sorted(set(a[1]))} vs tw L{b[0]} cols {sorted(set(b[1]))}",
        )

    en_pair = tw_pair = None
    if line_for_line:
        en_pair = source_pairing_link(en_lines, en_inside)
        if en_pair:
            back = en_pair[1][: -len("-tw.md")] + ".md"
            row = tw_lines[en_pair[0] - 1] if en_pair[0] <= len(tw_lines) else ""
            if any(m.group(2) == back for m in LINK_RE.finditer(row)):
                tw_pair = (en_pair[0], back)
            check("pairing line links back to the source", tw_pair is not None, f"L{en_pair[0]} should link to {back}")
    else:
        tw_pair = first_link(tw_lines, tw_inside, top_end(tw_lines, tw_inside), lambda t: file_name(t) == source_name)
        check("pairing line present", tw_pair is not None,
              f"L{tw_pair[0]}" if tw_pair else f"no link back to {source_name} above the first heading")

    en_l = links(en_lines, en_inside, en_pair)
    tw_l = links(tw_lines, tw_inside, tw_pair)
    check("link targets match one for one", en_l == tw_l, f"{len(en_l)} vs {len(tw_l)}")
    if en_l != tw_l:
        for a, b in zip(en_l, tw_l):
            if a != b:
                print(f"       en: {a}\n       tw: {b}")

    # what a translation copies unchanged, section by section; the pairing line names the other file
    en_skip = {en_pair[0]} if en_pair else set()
    tw_skip = {tw_pair[0]} if tw_pair else set()
    template = template_pair(args.en)
    templated = template[0] is not None

    def spans(text):
        return [re.sub(r"\s+", " ", m.group(0)) for m in CODE_SPAN_RE.finditer(text)]

    def citations(line):
        prose = CODE_SPAN_RE.sub(" ", line)
        found = [f"§{a}.{b}" for a, b in SECTION_CITE_RE.findall(prose)]
        return found + ([f"{a}.{b}" for a, b in BARE_CITE_RE.findall(prose)] if templated else [])

    for label, collect in (("inline-code spans", spans), ("section citations", citations)):
        drift = section_drift(per_section(en_lines, en_inside, collect, en_skip),
                              per_section(tw_lines, tw_inside, collect, tw_skip), en_heads,
                              file_name(args.en), file_name(args.tw))
        check(f"every section has the same {label}", not drift, f"{len(drift)} section(s) differ" if drift else "")
        for d in drift[:12]:
            print(f"       {d}")
        if len(drift) > 12:
            print(f"       ... and {len(drift) - 12} more")

    en_tok, tw_tok = tokens(en_lines, en_inside), tokens(tw_lines, tw_inside)
    missing = sorted(set(en_tok) - set(tw_tok))
    check("every placeholder token carried over", not missing, ", ".join(missing))

    retired = [f"{side} L{i}: {m.group(0)}" for side, side_lines in (("en", en_lines), ("tw", tw_lines))
               for i, line in enumerate(side_lines, 1) for m in OLD_RE.finditer(line)]
    check("no placeholder in the retired form ___X___", not retired,
          f"{len(retired)} - convert them: python {PLACEHOLDERS_PY.as_posix()} convert {args.en}" if retired else "")
    for d in retired[:12]:
        print(f"       {d}")
    if len(retired) > 12:
        print(f"       ... and {len(retired) - 12} more")

    en_items, tw_items = items_per_section(en_lines, en_inside), items_per_section(tw_lines, tw_inside)
    drift = [(head, a, tw_items[k][1] if k < len(tw_items) else None)
             for k, (head, a) in enumerate(en_items) if k >= len(tw_items) or tw_items[k][1] != a]
    check("bullet/numbered counts match per section", not drift)
    for head, a, b in drift:
        print(f"       {head.strip()}: en={a} tw={b}")

    terms = list(dict.fromkeys(term for _, term in glossary_terms(en_lines, en_inside)))
    lost = [(term, bold_uses(en_lines, en_inside, term), bold_uses(tw_lines, tw_inside, term)) for term in terms]
    lost = [x for x in lost if x[2] < x[1]]
    check("every glossary term kept bold as often as in the source", not lost, f"{len(terms)} terms")
    for term, a, b in lost:
        print(f"       **{term}**: en={a} tw={b}")

    if line_for_line:
        check("line for line: the same line count", len(en_lines) == len(tw_lines), f"{len(en_lines)} vs {len(tw_lines)}")
        kinds = [(i, line_kind(a, i in en_inside), line_kind(b, i in tw_inside))
                 for i, (a, b) in enumerate(zip(en_lines, tw_lines), 1)]
        kinds = [x for x in kinds if x[1] != x[2]]
        check("line for line: the same kind of line at every number", not kinds, f"{len(kinds)} line(s) differ" if kinds else "")
        for i, a, b in kinds[:12]:
            print(f"       L{i}: en {a}, tw {b}")
        if len(kinds) > 12:
            print(f"       ... and {len(kinds) - 12} more")

    warnings = []
    for term in terms:
        if "`" in term:
            continue
        a, b = plain_uses(en_lines, en_inside, term), plain_uses(tw_lines, tw_inside, term)
        if b < a:
            warnings.append(f"{term}: unbolded en={a} tw={b}")
    for w in warnings:
        print(f"[WARN] {w} - read each source use: an ordinary word translated is right, a term translated is not")

    # a title is copied as it is; a suffix an older twin still carries passes, with a warning
    if titled and en_h and tw_h and tw_h[0] == en_h[0] + TW_SUFFIX:
        warnings.append("title suffix")
        print(f"[WARN] the title still ends in {TW_SUFFIX} - drop it: the twin's title is the source's, byte for byte")

    if args.keep:
        prose = list(prose_lines(tw_lines, tw_inside))
        for term, flagged in keep_english(args.keep):
            for rendering in flagged:
                at = [i for i, line in prose if rendering in line]
                if at:
                    warnings.append(f"{rendering} for {term}")
                    shown = ", ".join(f"L{i}" for i in at[:8]) + (" ..." if len(at) > 8 else "")
                    print(f"[WARN] '{rendering}' at {shown} - the keep-English list keeps '{term}' in English")

    for i, excerpt in unrendered_bold(tw_lines, tw_inside):
        warnings.append(f"bold at L{i}")
        print(f"[WARN] L{i}: '{excerpt}' - this ** will not render as bold: against a punctuation mark, it needs "
              "whitespace or punctuation on its other side")

    for i, excerpt, wrong in spacing(tw_lines, tw_inside):
        warnings.append(f"spacing at L{i}")
        print(f"[WARN] L{i}: '{excerpt}' - {wrong}")

    # a line the source takes unchanged from its template is worded as the template's twin words it
    if line_for_line:
        name, _, twin, shared, problem = template
        if problem:
            warnings.append("template")
            print(f"[WARN] the template [[{name or '?'}]] gives no shared lines: {problem} - none was checked")
        elif name:
            taken = shared_lines(en_lines, en_inside, shared)
            off = [(i, wording) for i, wording in taken if i > len(tw_lines) or tw_lines[i - 1].strip() != wording]
            for i, wording in off:
                warnings.append(f"shared line L{i}")
                print(f"[WARN] L{i}: a line the source shares with [[{name}]] is worded otherwise than {twin.name} "
                      f"- copy it: '{wording[:80]}'")
            if not off:
                check(f"every line the source shares with [[{name}]] worded as {twin.name} words it", True,
                      f"{len(taken)} lines")

    check("tw has no BOM", not tw_bom)
    check("tw decodes as UTF-8", True)

    print(f"\n{len(failures)} failure(s)" + (": " + ", ".join(failures) if failures else "")
          + (f"; {len(warnings)} warning(s) to read" if warnings else ""))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
