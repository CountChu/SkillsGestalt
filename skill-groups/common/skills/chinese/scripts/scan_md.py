"""Print the kept-English inventory of an English Markdown file: headings, fences, code spans, links, tokens, tables,
and the lines it shares with the template its header quote names."""

import argparse
import io
import re
import sys
from pathlib import Path

import yaml

FENCE_RE = re.compile(r"^\s*(```|~~~)")
HEADING_RE = re.compile(r"^(#{1,6}) +(.*\S)\s*$")
CODE_SPAN_RE = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)")
BOLD_TERM_RE = re.compile(r"^\s*[-*] +\*\*(.+?)\*\* +(?:—|--|-) ")
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
# A wiki link, [[name]], [[name#heading]] or [[name|text]]: its target is the [[name]] it opens with.
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]*))?\]\]")
TOKEN_RE = re.compile(r"\{[A-Za-z][A-Za-z0-9_.\[\]<>-]*\}")
# A placeholder in the retired form ___UPPER_SNAKE___, which Markdown shows in bold italics instead of as written:
# not a token, but a warning that names the script converting it to {UPPER_SNAKE}.
OLD_RE = re.compile(r"___[A-Z0-9_]+___")
CJK_RE = re.compile(r"[\u3000-\u303f\u3400-\u4dbf\u4e00-\u9fff\uff00-\uffef]")
LEVEL1_RE = re.compile(r"^#\s+\S")
GLOSSARY_HEADING_RE = re.compile(r"^#\s+(?:DEDICATED\s+)?TERMINOLOGY\s*$", re.IGNORECASE)
# A section of definitions at any level, numbered or not - an RSDC's 2.1 Terminology.
TERMINOLOGY_HEADING_RE = re.compile(r"^#{1,6}\s+(?:\d+(?:\.\d+)*\.?\s+)?Terminology\s*$")
# A placeholder a template leaves to be filled - {UPPER_SNAKE}.
# A variable such as {skillGroups.common} is kept by a filled file, so a line holding one may still be shared.
FILL_RE = re.compile(r"\{[A-Z][A-Z0-9_]+\}")
RULE_ROW_RE = re.compile(r"^\|[\s:|-]+\|$")
# {skillGroups.common}: where depends_on.py is kept, and every template a file may be filled from.
COMMON = Path(__file__).resolve().parents[3]
# The script that converts each placeholder in the retired form to {UPPER_SNAKE}, in a file and its twin.
PLACEHOLDERS_PY = COMMON / "scripts" / "placeholders.py"


def split_frontmatter(text):
    if not text.startswith("---"):
        return None, text, 0
    end = text.find("\n---", 3)
    if end == -1:
        return None, text, 0
    raw = text[3:end]
    offset = text[: end + 4].count("\n") + 1
    try:
        return yaml.safe_load(raw), text[end + 4 :], offset
    except yaml.YAMLError as exc:
        return {"__error__": str(exc)}, text[end + 4 :], offset


def fence_spans(lines):
    """Return (line numbers of fence lines, set of 1-based line numbers inside a fence)."""
    marks, inside, open_at = [], set(), None
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            marks.append(i)
            if open_at is None:
                open_at = i
            else:
                inside.update(range(open_at, i + 1))
                open_at = None
    if open_at is not None:
        inside.update(range(open_at, len(lines) + 1))
    return marks, inside


def glossary_terms(lines, inside):
    """(line number, term) for each `- **term** — ` bullet under a `# TERMINOLOGY` or `# DEDICATED TERMINOLOGY` heading,
    or under a heading named Terminology at any level - an RSDC's 2.1 Terminology - up to the next heading as high as it.

    A bold-led bullet anywhere else - a rule under MUST FOLLOW - is not a term, so it is not read.
    """
    out, on, terms_level = [], False, None
    for i, line in enumerate(lines, 1):
        if i in inside:
            continue
        h = HEADING_RE.match(line)
        if h:
            level = len(h.group(1))
            if terms_level is not None and level <= terms_level:
                terms_level = None
            if TERMINOLOGY_HEADING_RE.match(line):
                terms_level = level
            if LEVEL1_RE.match(line):
                on = bool(GLOSSARY_HEADING_RE.match(line))
            continue
        m = BOLD_TERM_RE.match(line) if on or terms_level is not None else None
        if m:
            out.append((i, m.group(1)))
    return out


def table_blocks(lines, inside):
    """Column count per contiguous run of pipe rows, ignoring escaped pipes."""
    blocks, run = [], []
    for i, line in enumerate(lines, 1):
        is_row = i not in inside and line.strip().startswith("|") and line.strip().endswith("|")
        if is_row:
            run.append(line.replace(r"\|", "").count("|") - 1)
        elif run:
            blocks.append((i - len(run), run))
            run = []
    if run:
        blocks.append((len(lines) - len(run) + 1, run))
    return blocks


def cjk_stats(lines, inside):
    """CJK share of prose, and how many heading lines carry CJK. Code spans and fences excluded."""
    prose_cjk = prose_total = heads = heads_cjk = 0
    for i, line in enumerate(lines, 1):
        if i in inside:
            continue
        if HEADING_RE.match(line):
            heads += 1
            heads_cjk += bool(CJK_RE.search(line))
        bare = "".join(ch for ch in CODE_SPAN_RE.sub("", line) if not ch.isspace())
        prose_cjk += len(CJK_RE.findall(bare))
        prose_total += len(bare)
    return prose_cjk, prose_total, heads_cjk, heads


def keep_english(path):
    """(term, [flagged renderings]) for every row of the shared keep-English list's table."""
    rows, in_table = [], False
    for line in io.open(path, encoding="utf-8-sig"):
        if not line.strip().startswith("|"):
            in_table = False
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        # the header row is Term, then Replaces: a row of the list may itself be the term "term"
        if cells[0].lower() == "term" and len(cells) > 1 and cells[1].lower() == "replaces":
            in_table = True
            continue
        if not in_table or set(cells[0]) <= set("-: "):
            continue
        flagged = re.split(r"[,、]", cells[2]) if len(cells) > 2 else []
        rows.append((cells[0], [r.strip() for r in flagged if r.strip() not in ("", "—", "-")]))
    return rows


def prose_lines(lines, inside):
    """(line number, text) of every non-heading line outside a fence, inline code and link targets removed."""
    for i, line in enumerate(lines, 1):
        if i in inside or HEADING_RE.match(line):
            continue
        yield i, LINK_RE.sub(lambda m: m.group(1), CODE_SPAN_RE.sub("", line))


def top_end(lines, inside):
    """The line number the top of a file runs to: its first heading, or its second when the file opens
    with its title. A pairing line sits above it."""
    heads = [i for i, line in enumerate(lines, 1) if i not in inside and HEADING_RE.match(line)]
    first = next((i for i, line in enumerate(lines, 1) if line.strip()), None)
    if heads and heads[0] == first:
        heads = heads[1:]
    return heads[0] if heads else len(lines) + 1


def first_link(lines, inside, end, wanted):
    """(line number, target) of the first link above line `end` whose target `wanted` accepts, or None."""
    for i, line in enumerate(lines[: end - 1], 1):
        if i in inside:
            continue
        for m in LINK_RE.finditer(line):
            if wanted(m.group(2)):
                return i, m.group(2)
    return None


def source_pairing_link(lines, inside):
    """A file's own pairing link: the first link above its first section to a -tw.md file, or None."""
    return first_link(lines, inside, top_end(lines, inside), lambda target: target.endswith("-tw.md"))


def template_pair(path):
    """The template the file at `path` was filled from, as its header quote names it - a `[[name]]` whose name
    ends in -tmp, looked for in the file's vault and then in {skillGroups.common} - and that template's twin.

    Returns (name, template, twin, shared, problem). All five are None when the header quote names no template.
    `problem` says why a template named cannot be used: it is not found, it has no twin, or the twin is not line
    for line with it. Otherwise `shared` maps each line of the template a filled file may hold unchanged - not
    blank, fenced, a heading, a quote or a table's rule, and holding no placeholder - stripped, to the twin's line
    at the same number, stripped; of two equal lines, the first decides.
    """
    sys.path.insert(0, str(COMMON / "scripts"))
    import depends_on

    owner = Path(path)
    try:
        named = [e for e in depends_on.entries(owner, depends_on.read_lines(owner))
                 if e.kind == "note" and e.target.endswith("-tmp")]
    except depends_on.Fault as exc:
        return None, None, None, None, str(exc)
    if not named:
        return None, None, None, None, None
    name = named[0].target
    if len(named) > 1:
        return name, None, None, None, "the header quote names several templates: " + ", ".join(f"[[{e.target}]]" for e in named)
    try:
        template = depends_on.resolve(named[0], owner, None, None)
    except depends_on.Fault:
        template = None
    try:
        template = template or depends_on.find_note(name, COMMON)
    except depends_on.Fault as exc:
        return name, None, None, None, str(exc)
    if template is None:
        return name, None, None, None, f"it is in neither the file's vault nor {COMMON}"
    twin = template.with_name(template.stem + "-tw.md")
    if not twin.is_file():
        return name, template, None, None, f"{template.name} has no twin {twin.name} beside it"
    en = io.open(template, encoding="utf-8-sig").read().splitlines()
    tw = io.open(twin, encoding="utf-8-sig").read().splitlines()
    if len(en) != len(tw):
        return name, template, twin, None, f"{template.name} and {twin.name} are not line for line ({len(en)} / {len(tw)} lines)"
    _, inside = fence_spans(en)
    shared = {}
    for i, (a, b) in enumerate(zip(en, tw), 1):
        s = a.strip()
        if not s or i in inside or HEADING_RE.match(a) or s.startswith(">") or RULE_ROW_RE.match(s) or FILL_RE.search(s):
            continue
        shared.setdefault(s, b.strip())
    return name, template, twin, shared, None


def shared_lines(lines, inside, shared):
    """(line number, the template twin's wording) of every line of a file that it shares with its template."""
    return [(i, shared[line.strip()]) for i, line in enumerate(lines, 1)
            if i not in inside and not HEADING_RE.match(line) and line.strip() in shared]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--file", required=True, help="path to the source Markdown file")
    ap.add_argument("--keep", help="path to the shared keep-English list; lists the listed terms the prose uses")
    args = ap.parse_args()

    text = io.open(args.file, encoding="utf-8-sig").read()
    fm, _body, _offset = split_frontmatter(text)
    lines = text.splitlines()
    marks, inside = fence_spans(lines)

    print(f"file: {args.file}")
    print(f"lines: {len(lines)}")
    if fm is None:
        print("frontmatter: none")
    elif "__error__" in fm:
        print(f"frontmatter: UNPARSEABLE - {fm['__error__']}")
    else:
        print(f"frontmatter keys: {sorted(fm)}  name={fm.get('name')!r}")

    headings, spans, terms, links, tokens = [], {}, [], [], []
    for i, line in enumerate(lines, 1):
        if i in inside:
            continue
        m = HEADING_RE.match(line)
        if m:
            headings.append((i, line))
        for s in CODE_SPAN_RE.finditer(line):
            spans.setdefault(s.group(2).strip(), i)
        for lk in LINK_RE.finditer(line):
            links.append((i, lk.group(1), lk.group(2)))
        for wl in WIKILINK_RE.finditer(line):
            links.append((i, wl.group(2) or wl.group(1).strip(), f"[[{wl.group(1).strip()}]]"))
        for tk in TOKEN_RE.finditer(line):
            tokens.append((i, tk.group(0)))

    terms = glossary_terms(lines, inside)
    tables = table_blocks(lines, inside)

    print(f"\n-- headings ({len(headings)}) --")
    for i, line in headings:
        print(f"  L{i}: {line}")

    print(f"\n-- fences ({len(marks)}, {'balanced' if len(marks) % 2 == 0 else 'ODD - UNCLOSED'}) --")
    print(f"  at lines: {marks}")

    print(f"\n-- glossary terms ({len(terms)}) --")
    for i, term in terms:
        print(f"  L{i}: {term}")

    print(f"\n-- inline-code spans ({len(spans)}) --")
    for span, i in sorted(spans.items(), key=lambda kv: kv[1]):
        print(f"  L{i}: `{span}`")

    print(f"\n-- links ({len(links)}) --")
    for i, disp, target in links:
        print(f"  L{i}: [{disp}] -> {target}")

    print(f"\n-- placeholder tokens ({len(tokens)}) --")
    for i, tok in tokens:
        print(f"  L{i}: {tok}")

    old = [(i, m.group(0)) for i, line in enumerate(lines, 1) for m in OLD_RE.finditer(line)]
    if old:
        print(f"\n-- WARNING: placeholders in the retired form ___X___ ({len(old)}) --")
        for i, tok in old:
            print(f"  L{i}: {tok}")
        print(f"  convert them, in the file and its twin: python {PLACEHOLDERS_PY.as_posix()} convert {args.file}")

    print(f"\n-- tables ({len(tables)}) --")
    for start, cols in tables:
        flag = "" if len(set(cols)) == 1 else "  <- RAGGED"
        print(f"  L{start}: {len(cols)} rows, columns {sorted(set(cols))}{flag}")

    kept = []
    if args.keep:
        prose = [line for _, line in prose_lines(lines, inside)]
        for term, _flagged in keep_english(args.keep):
            uses = sum(len(re.findall(rf"\b{re.escape(term)}\b", line, re.IGNORECASE)) for line in prose)
            if uses:
                kept.append((term, uses))
        print(f"\n-- keep-English terms the prose uses ({len(kept)}) --")
        for term, uses in kept:
            print(f"  {term}: {uses}")

    print("\n-- shape --")
    if fm is None:
        print("  line for line: no frontmatter, so the twin keeps every line at its number and adds none")
        pair = source_pairing_link(lines, inside)
        if pair:
            back = pair[1][: -len("-tw.md")] + ".md"
            print(f"  pairing line: L{pair[0]} links to {pair[1]}; the twin's L{pair[0]} links back to {back}")
        else:
            print("  pairing line: none above the first section, so the twin has none either")
    else:
        print("  frontmatter: the twin adds its pairing line under the frontmatter and is matched heading by heading")

    name, template, twin, shared, problem = template_pair(args.file)
    taken = shared_lines(lines, inside, shared) if shared else []
    print("\n-- template --")
    if name is None and problem is None:
        print("  none: the header quote names no [[...-tmp]], so every line is translated")
    elif problem:
        print(f"  [[{name or '?'}]]: {problem} - so no line is copied, and every line is translated")
    else:
        print(f"  [[{name}]] -> {template}")
        print(f"  its twin -> {twin}, line for line: {len(shared)} lines a filled file may take unchanged")
        print(f"  shared lines the source holds ({len(taken)}), each copied from the twin as it stands here, not translated:")
        for i, wording in taken:
            print(f"  L{i}: {wording}")

    print(
        f"\nsummary: headings={len(headings)} fences={len(marks)} terms={len(terms)} "
        f"spans={len(spans)} links={len(links)} tokens={len(tokens)} tables={len(tables)} shared={len(taken)}"
    )

    p_cjk, p_total, h_cjk, h_total = cjk_stats(lines, inside)
    prose_ratio = p_cjk / p_total if p_total else 0.0
    head_ratio = h_cjk / h_total if h_total else 0.0
    desc = str(fm.get("description", "")) if isinstance(fm, dict) else ""
    already = head_ratio > 0.5 or prose_ratio > 0.3

    print("\n-- language --")
    print(f"  prose CJK: {p_cjk}/{p_total} = {prose_ratio:.0%}")
    print(f"  headings carrying CJK: {h_cjk}/{h_total} = {head_ratio:.0%}")
    print(f"  description carries CJK: {bool(CJK_RE.search(desc))}")
    print(f"  verdict: {'ALREADY-CHINESE' if already else 'translatable'}")
    if already:
        print("\nSTOP: the source is already Traditional Chinese - a twin would be a copy, not a translation.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
