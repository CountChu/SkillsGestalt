#!/usr/bin/env python3
"""The RSDC Checker: what a program can check in an RSDC written for a skill's system, or for an app.

gen-rsdc-skill runs it four times, and gen-rsdc-app runs the --rsdc check on the English half of
an app's design pair; the arguments choose what one run checks:

  --standard RSDC-Standard.md
      The RSDC template against the standard, before anything is written to it: the version
      the template and its twin record where they name the standard is the standard's own
      version - the one its header quote opens with, > Version: 261010 - each of the two gives
      its own version the same way, and the fingerprint they record after each of their links to the standard -
      the standard, and DFD.md beside it - is that file's fingerprint now, as the shared
      .github/common/scripts/depends_on.py computes it: a version alone misses a change made
      under the same version. A template behind the standard passes every other check here,
      since they hold the template's shape and not the standard's.
  --rsdc X-RSDC.md [--skill-name NAME]
      The English RSDC alone: no placeholder or instruction of the template left, and no
      placeholder in the retired form ___UPPER_SNAKE___, which Markdown shows in bold italics
      instead of as written - its failure names .github/common/scripts/placeholders.py, which
      converts it to {UPPER_SNAKE}; its title,
      its links to the standard and to the template it was written from, no link to its twin, the four chapter headings, the numbering
      and order of the sections the template carries and the ones it never leaves out, no
      Directory Structure or Presentation Form unless the template carries them, the parts of the
      Dataflow, its diagram - the stages it lists drawn as rounded boxes, every node in a
      shape of the DFD notation - and no stage drawn open in it, the diagrams' line styles,
      the goals table, every component CLI names, where there is a CLI, broken down in Core
      Component Responsibilities, a component for every stage, a row of Verification Obligations
      for every component Core Component Responsibilities breaks down, and forward references -
      and, given the skill's name, that the RSDC never names it.
  --rsdc X-RSDC.md --tw X-RSDC-tw.md [--keep tw-keep-english.md]
      The pair: the twin line for line against the English file - the same line count and
      line kinds, the same headings, the title included, byte-identical fenced blocks, the same
      inline code and section citations in every section, the same link targets, neither
      file linking to the other, and neither holding a placeholder in the retired form. Every
      comparison reads a CRLF line ending as LF. It warns about two files that end their lines
      differently, about a shared sentence worded otherwise than in the template's twin, about the
      keep-English list's flagged renderings, about terms the twin uses less often than the
      English file, and about English run into Chinese without a space.
  --rsdc X-RSDC.md --skill SKILL.md
      The skill's side: every section citation lands on a section of the RSDC whose heading
      it names, and none lands in Design or Coding; the skill's Dataflow is a diagram that
      draws every Workflow step by its full name; its links to the pair resolve; and the RSDC
      never names the skill.

The shape is read from the template the RSDC's header quote names - > [[RSDC-Skill-System-tmp]], or
> [[RSDC-App-tmp]] for an app's - found in the RSDC's vault or else in {skillGroups.common}, and the
shared sentences' wording from the twin beside it. --template names another template, and
--tw-template another twin; an RSDC whose header quote names none, and --standard, read the template
beside this script's directory, assets/RSDC-Skill-System-tmp.md. The template owns the shape - the title, the heading level of a
chapter, a section and a subsection, which chapters and sections there are, in what order, and which a
system may leave out - and this script holds no second copy of it. The fixed tables and sentences it matches must appear in the template, or it stops
with exit status 2: a template and a checker that disagree would fail every RSDC written to
the template.

Every check prints one line: [PASS], [FAIL] or [WARN]. A warning never fails the run; it marks
something only a reader can settle.

Exit status: 0 no check failed; 1 a check failed; 2 the command is malformed, a file cannot
be read, or, with --standard, the standard gives no version in its header quote, or a template
records no version, does not link the standard, or records no fingerprint after a link to a
file of the standard.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / 'assets' / 'RSDC-Skill-System-tmp.md'
# {skillGroups.common}: where the shared depends_on.py is kept, and every RSDC template.
COMMON = Path(__file__).resolve().parents[3]
OPTIONAL_MARK = '> **Optional.**'
# A placeholder of the template, {UPPER_SNAKE}.
# The capitals keep it apart from a variable such as {skillGroups.common}, which a document keeps.
PLACEHOLDER_RE = re.compile(r'\{(?!PLACEHOLDER\})[A-Z][A-Z0-9_]+\}')
# A placeholder in the retired form, ___UPPER_SNAKE___: a failure wherever it stands, fenced or not.
OLD_PLACEHOLDER_RE = re.compile(r'___[A-Z0-9_]+___')
# The script that converts each placeholder in the retired form to {UPPER_SNAKE}, in a file and its twin.
PLACEHOLDERS_PY = COMMON / 'scripts' / 'placeholders.py'

# The shape, which load_shape() reads from the RSDC template: the chapter headings, each
# chapter's sections in order, the ones a system may never leave out, and the Dataflow's parts.
CHAPTERS: list[str] = []
SECTION_ORDER: dict[int, list[str]] = {}
REQUIRED: dict[int, list[str]] = {}
DATAFLOW_PARTS: list[str] = []
INSTRUCTIONS: set[str] = set()
KEPT: set[str] = set()
# A link to the standard, which a document keeps: > [[RSDC-Standard]], with or without the record
# depends_on.py writes after it.
WIKILINK_RE = re.compile(r'>\s*\[\[[^\]]+\]\](?:\s+`[^`]*`)*')
# The heading levels of a chapter, a section and a subsection, which load_shape() also reads from
# the template. The title is always the first heading, at level 1, whatever the chapters' level.
CHAPTER_LEVEL, SECTION_LEVEL, SUB_LEVEL = 1, 2, 3

# The title, which load_shape() also reads from the template: its first line, a placeholder
# standing for any name.
TITLE = ''
TITLE_RE = re.compile(r'^# ')
TW_SUFFIX = '（繁體中文）'
# A bullet in the form the template gave up for the App template's: marked *, or with a colon
# where the template ends a bold name with a dash, "- **Name** — what it is".
OLD_BULLET_RE = re.compile(r'^\s*(?:\*\s|-\s+\*\*[^*\n]+\*\*(?:, the (?:program|module|script) `[^`]+`'
                           r'|，(?:程式|模組) `[^`]+`)?\s*[:：])')

# The fixed tables and sentences this script matches; load_shape() confirms the template has them.
EXCEPTION_LABELS = ['Ending with nothing written', 'Stopping midway', 'Re-entering midway']
ORDER_SENTENCE = 'No stage reads what a later stage writes.'
LEGEND = 'How to read the diagram:'
VERIFY_HEADER = '| Claim | Rule | Proven by | Performed by |'
GOALS_HEADER = '| Goal | Carried by |'
BLUE = '#2563eb'

FENCE_RE = re.compile(r'^\s*(```|~~~)')
HEADING_RE = re.compile(r'^(#{1,6})\s+(.*?)\s*$')
CHAPTER_RE = re.compile(r'^(?:\*\*)?(\d)\.\s')
SECTION_RE = re.compile(r'^(?:\*\*)?(\d)\.(\d+)\s+(.+?)(?:\*\*)?$')
BOLD_TEXT_RE = re.compile(r'^\*\*(.+?)\*\*$')
CODE_RE = re.compile(r'`[^`]*`')
# A bare section citation such as 2.4, (2.6) or 2.10: not part of a longer number, a version, a
# path, a § citation of another document, or a value such as 2.5px. Only chapter 2 has a tenth
# section, so 3.10, a Python version, stays a value.
CITE_RE = re.compile(r'(?<![A-Za-z0-9_.§−\-+/#])([1-4])\.([1-9]|(?<=2\.)1[0-2])(?!\d|\.\d|[A-Za-z])')
# A chapter cited by number: chapter 2, Chapter 3, chapters 1 and 2.
CHAPTER_CITE_RE = re.compile(r'\b[Cc]hapters?\s+[1-4](?:\s*(?:,|and|or|to)\s*[1-4])*\b')
SKILL_CITE_RE = re.compile(r'§\s?([1-9])\.(\d+)(?:\s*\*([^*]+)\*)?')
EXTERNAL_BEFORE_RE = re.compile(r'(\.md`?|〉|》)\s*$')
LINK_RE = re.compile(r'\]\(([^)\s]+)\)')
EDGE_RE = re.compile(r'<-->|<==>|-\.->|-\.-|==>|-->|---|~~~|--[ox](?=\s)')  # ~~~ is invisible, yet counted
LINKSTYLE_RE = re.compile(r'^\s*linkStyle\s+([\d,\s]+?)\s+\S')
CJK = '㐀-䶿一-鿿'
GLUED_RE = re.compile(rf'[A-Za-z0-9][{CJK}]|[{CJK}][A-Za-z0-9]')


class Report:
    def __init__(self) -> None:
        self.passed = self.failed = self.warned = 0

    def ok(self, what: str) -> None:
        self.passed += 1
        print(f'[PASS] {what}')

    def fail(self, what: str, details: list[str] | None = None) -> None:
        self.failed += 1
        print(f'[FAIL] {what}')
        for d in (details or [])[:12]:
            print(f'         {d}')
        if details and len(details) > 12:
            print(f'         ... and {len(details) - 12} more')

    def warn(self, what: str, details: list[str] | None = None) -> None:
        self.warned += 1
        print(f'[WARN] {what}')
        for d in (details or [])[:12]:
            print(f'         {d}')
        if details and len(details) > 12:
            print(f'         ... and {len(details) - 12} more')

    def check(self, cond: bool, what: str, details: list[str] | None = None) -> None:
        if cond:
            self.ok(what)
        else:
            self.fail(what, details)


class Doc:
    """A Markdown file, split into lines, with its fenced blocks and headings located."""

    def __init__(self, path: Path) -> None:
        raw = path.read_bytes()
        self.path = path
        self.bom = raw.startswith(b'\xef\xbb\xbf')
        # a CRLF line ending reads as LF, so that every comparison sees the text alone
        self.crlf = b'\r\n' in raw
        self.lines = raw.decode('utf-8-sig').replace('\r\n', '\n').split('\n')
        self.fence = [False] * len(self.lines)
        self.blocks: list[tuple[int, int]] = []
        self.heads: list[tuple[int, int, str]] = []
        self.unclosed = None
        start = None
        for i, line in enumerate(self.lines):
            if FENCE_RE.match(line):
                self.fence[i] = True
                if start is None:
                    start = i
                else:
                    self.blocks.append((start, i))
                    start = None
                continue
            if start is not None:
                self.fence[i] = True
                continue
            m = HEADING_RE.match(line)
            if m:
                self.heads.append((i, len(m.group(1)), m.group(2)))
        self.unclosed = start
        self.head_at = {i: (lvl, txt) for i, lvl, txt in self.heads}

    def block_text(self, block: tuple[int, int]) -> str:
        return '\n'.join(self.lines[block[0]:block[1] + 1])

    def prose(self, i: int) -> str | None:
        """The line with inline code removed, or None for a fence or heading line."""
        if self.fence[i] or i in self.head_at:
            return None
        return CODE_RE.sub(' ', self.lines[i])

    def sections(self) -> dict[tuple[int, int], tuple[int, str]]:
        out = {}
        for i, lvl, txt in self.heads:
            m = SECTION_RE.match(txt) if lvl == SECTION_LEVEL else None
            if m:
                out[(int(m.group(1)), int(m.group(2)))] = (i, m.group(3))
        return out

    def span(self, start: int, stop_levels: tuple[int, ...]) -> range:
        """Lines after heading `start` up to the next heading of one of `stop_levels`."""
        end = len(self.lines)
        for i, lvl, _ in self.heads:
            if i > start and lvl in stop_levels:
                end = i
                break
        return range(start + 1, end)

    def section_keys(self) -> list[str]:
        """For every line, the text of the latest heading above it, down to the subsection level."""
        keys, cur = [], '(top)'
        for i in range(len(self.lines)):
            h = self.head_at.get(i)
            if h and h[0] <= SUB_LEVEL:
                cur = h[1][:-len(TW_SUFFIX)] if h[0] == 1 and h[1].endswith(TW_SUFFIX) else h[1]
            keys.append(cur)
        return keys


def upto(level: int) -> tuple[int, ...]:
    """The heading levels that end a part opened at `level`: that level, and every one above it."""
    return tuple(range(1, level + 1))


def bare_link(line: str) -> str:
    """A line with the record after its link left out: > [[DFD]]  `2026-10-10`  `1a2b3c4d5e6f` gives > [[DFD]]."""
    return re.sub(r'(?:\s+`[^`]*`)+\s*$', '', line.strip())


def strip_bold(s: str) -> str:
    m = BOLD_TEXT_RE.match(s.strip())
    return m.group(1) if m else s.strip()


def table_rows(doc: Doc, header_line: int) -> list[list[str]]:
    rows = []
    for i in range(header_line + 2, len(doc.lines)):
        s = doc.lines[i].strip()
        if not s.startswith('|'):
            break
        rows.append(split_cells(s))
    return rows


def split_cells(row: str) -> list[str]:
    cells = re.split(r'(?<!\\)\|', row.strip())
    return [c.strip() for c in cells[1:-1]]


def find_line(doc: Doc, lines: range, text: str, startswith: bool = True) -> int | None:
    for i in lines:
        s = doc.lines[i].strip()
        if (s.startswith(text) if startswith else text in s):
            return i
    return None


def links_to(doc: Doc, name: str) -> list[str]:
    """Every line outside a fence that links to the file `name`, whatever path or anchor the link adds."""
    return [f'line {i + 1}: {line.strip()[:90]}' for i, line in enumerate(doc.lines) if not doc.fence[i]
            and any(t.split('#')[0].rsplit('/', 1)[-1] == name for t in LINK_RE.findall(line))]


def mermaid_edges(text: str) -> int:
    n = 0
    for line in text.split('\n'):
        s = line.strip()
        if not s or s.startswith(('%%', 'linkStyle', 'classDef', 'class ', 'style ', 'subgraph',
                                  'end', 'flowchart', 'graph', 'direction')):
            continue
        n += len(EDGE_RE.findall(s))
    return n


def linkstyle_indices(text: str) -> list[tuple[list[int], str]]:
    out = []
    for line in text.split('\n'):
        m = LINKSTYLE_RE.match(line)
        if m:
            out.append(([int(x) for x in re.split(r'[,\s]+', m.group(1)) if x], line))
    return out


def node_labels(text: str) -> list[str]:
    labels = []
    for pat in (r'\[/"?(.*?)"?/\]', r'\[\("?(.*?)"?\)\]', r'\(\["?(.*?)"?\]\)', r'\{\{"?(.*?)"?\}\}',
                r'\[\["?(.*?)"?\]\]', r'\["(.*?)"\]'):
        labels += [m.group(1).strip() for m in re.finditer(pat, text)]
    # The flag shape of one-run data, ID>"label"]: the id must follow a line start or a space,
    # so the > of an arrow such as --> is never read as one.
    labels += [m.group(1).strip() for m in re.finditer(r'(?:^|\s)[A-Za-z_]\w*>"(.*?)"\]', text, re.M)]
    return labels


def rounded_boxes(text: str) -> list[str]:
    """The stages a DFD draws: the label of every rounded box, each once, in the order drawn."""
    boxes: list[str] = []
    for m in re.finditer(r'\(\[\s*"?(.*?)"?\s*\]\)', text):
        if m.group(1).strip() and m.group(1).strip() not in boxes:
            boxes.append(m.group(1).strip())
    return boxes


# A node opened in a shape DFD.md does not have: a rectangle, a round edge, a rhombus, a
# subroutine. The notation's own five open with ([ [/ [( {{ or, for a flag, >.
OTHER_SHAPE_RE = re.compile(r'(?<![\w>-])([A-Za-z_]\w*)(?:\[\[|\[(?![/(])|\((?!\[)|\{(?!\{))')


def odd_shapes(text: str) -> list[str]:
    """The ids of the nodes a mermaid DFD draws in a shape its notation does not have."""
    odd: list[str] = []
    for line in text.split('\n'):
        s = line.strip()
        if not s or s == 'end' or s.startswith(('%%', 'flowchart', 'graph', 'subgraph', 'linkStyle',
                                                 'classDef', 'class ', 'style ', 'direction')):
            continue
        # labels and edge texts may hold any bracket
        s = re.sub(r'\|[^|]*\|', '', re.sub(r'"[^"]*"', '""', s))
        odd += [m.group(1) for m in OTHER_SHAPE_RE.finditer(s) if m.group(1) not in odd]
    return odd


# --------------------------------------------------------------------------- the template

def load_shape(template: Doc) -> list[str]:
    """Read the shape from the RSDC template, and return what the template lacks of the fixed
    tables and sentences this script matches."""
    global CHAPTERS, SECTION_ORDER, REQUIRED, DATAFLOW_PARTS, INSTRUCTIONS, KEPT
    global CHAPTER_LEVEL, SECTION_LEVEL, SUB_LEVEL, TITLE, TITLE_RE
    TITLE = template.lines[0].strip() if template.lines else ''
    TITLE_RE = re.compile('^' + '.+'.join(re.escape(part) for part in PLACEHOLDER_RE.split(TITLE)) + '$')
    CHAPTERS, SECTION_ORDER, REQUIRED, DATAFLOW_PARTS = [], {}, {}, []
    CHAPTER_LEVEL = next((lvl for _, lvl, t in template.heads if CHAPTER_RE.match(t)), CHAPTER_LEVEL)
    SECTION_LEVEL = next((lvl for _, lvl, t in template.heads if SECTION_RE.match(t)), SECTION_LEVEL)
    SUB_LEVEL = SECTION_LEVEL + 1
    chapter, dataflow = 0, None
    for i, lvl, txt in template.heads[1:]:
        if lvl == CHAPTER_LEVEL and CHAPTER_RE.match(txt):
            chapter = int(CHAPTER_RE.match(txt).group(1))
            CHAPTERS.append('#' * CHAPTER_LEVEL + ' ' + txt)
            SECTION_ORDER[chapter], REQUIRED[chapter] = [], []
        elif lvl == SECTION_LEVEL:
            m = SECTION_RE.match(txt)
            if not m or chapter not in SECTION_ORDER:
                continue
            title = m.group(3)
            SECTION_ORDER[chapter].append(title)
            # a section the template marks Optional opens with that instruction
            first = next((l.strip() for l in template.lines[i + 1:] if l.strip()), '')
            if not first.startswith(OPTIONAL_MARK):
                REQUIRED[chapter].append(title)
            if title == 'Dataflow':
                dataflow = i
    if dataflow is not None:
        DATAFLOW_PARTS = [strip_bold(t) for j, lvl, t in template.heads
                          if lvl == SUB_LEVEL and j in template.span(dataflow, upto(SECTION_LEVEL))]
    # a > line is an instruction to delete, except a link to the standard, which the document keeps
    quotes = {l.strip() for l in template.lines if l.startswith('>') and l.strip() != '>'}
    KEPT = {q for q in quotes if WIKILINK_RE.fullmatch(q)}
    INSTRUCTIONS = quotes - KEPT
    text = '\n'.join(template.lines)
    wanted = [ORDER_SENTENCE, LEGEND, VERIFY_HEADER, GOALS_HEADER] + \
        [f'**{x}**' for x in EXCEPTION_LABELS]
    return [w for w in wanted if w not in text] + ([] if CHAPTERS else ['every chapter heading'])


# --------------------------------------------------------------------------- the English RSDC

def old_bullets(doc: Doc) -> list[str]:
    """The bullets after the metadata still in the form the template gave up."""
    first = next((i for i, lvl, _ in doc.heads[1:] if lvl == CHAPTER_LEVEL), len(doc.lines))
    return [f'line {i + 1}: {doc.lines[i].strip()[:70]}' for i in range(first, len(doc.lines))
            if not doc.fence[i] and OLD_BULLET_RE.match(doc.lines[i])]


def old_placeholders(doc: Doc) -> list[str]:
    """Each line holding a placeholder in the retired form, with the placeholders it holds."""
    return [f'{doc.path.name} line {i + 1}: ' + ', '.join(sorted(set(OLD_PLACEHOLDER_RE.findall(l))))
            for i, l in enumerate(doc.lines) if OLD_PLACEHOLDER_RE.search(l)]


def check_rsdc(doc: Doc, rep: Report, skill_name: str | None, template: Path) -> None:
    lines = doc.lines
    left = [f'line {i + 1}: ' + ', '.join(sorted(set(PLACEHOLDER_RE.findall(l))))
            for i, l in enumerate(lines) if PLACEHOLDER_RE.search(l)]
    rep.check(not left, 'no placeholder of the template is left', left)
    old = old_placeholders(doc)
    rep.check(not old, 'no placeholder in the retired form ___X___',
              [f'convert them: python {PLACEHOLDERS_PY.as_posix()} convert {doc.path}'] + old)
    told = [f'line {i + 1}: {l.strip()[:90]}' for i, l in enumerate(lines)
            if l.strip() in INSTRUCTIONS or l.strip().startswith(OPTIONAL_MARK)]
    rep.check(not told, 'no instruction line of the template is left', told)
    # a link is kept whatever record follows it: the document may have recorded the standard anew
    gone = sorted(q for q in KEPT if bare_link(q) not in {bare_link(l) for l in lines})
    rep.check(not gone, 'the links to the standard are kept', gone)
    # the twin words what the RSDC shares with its template from the template's twin, found by this link
    name = template.stem
    rep.check(name in header_notes(doc.path), f'the header quote links the template it was written from, [[{name}]]',
              [f'add > [[{name}]] under the links to the standard, then record it: '
               f'depends_on.py record <the RSDC> --target "[[{name}]]"'])
    rep.check(not doc.bom, 'UTF-8 without a byte-order mark')
    rep.check(doc.unclosed is None, 'every fenced block is closed',
              [f'line {doc.unclosed + 1}: a fence opens and never closes'] if doc.unclosed is not None else None)

    first = doc.heads[0] if doc.heads else None
    rep.check(first is not None and first[0] == 0 and first[1] == 1 and TITLE_RE.match(lines[0]) is not None,
              f'line 1 is the title: {TITLE}',
              [f'line {first[0] + 1}: {first[2]}'] if first else ['no heading'])
    # the twin is for a reviewer: the RSDC itself never points to it
    twin = doc.path.stem + '-tw.md'
    rep.check(not links_to(doc, twin), f'no line links to the twin, {twin}', links_to(doc, twin))

    got = ['#' * CHAPTER_LEVEL + ' ' + t for _, lvl, t in doc.heads[1:] if lvl == CHAPTER_LEVEL]
    rep.check(got == CHAPTERS, 'the four chapter headings, verbatim and in order',
              [f'found: {g}' for g in got if g not in CHAPTERS] + [f'missing: {c}' for c in CHAPTERS if c not in got])

    # sections: numbering, required ones, order, and the ones a skill's system has nothing to put in
    chapter, numbering, titles = 0, [], {c: [] for c in SECTION_ORDER}
    for i, lvl, txt in doc.heads[1:]:
        if lvl == CHAPTER_LEVEL:
            m = CHAPTER_RE.match(txt)
            chapter = int(m.group(1)) if m else 0
            expected = 1
        elif lvl == SECTION_LEVEL:
            m = SECTION_RE.match(txt)
            if not m:
                numbering.append(f'line {i + 1}: not "{"#" * SECTION_LEVEL} N.M Title": {txt}')
                continue
            c, s = int(m.group(1)), int(m.group(2))
            if c != chapter or s != expected:
                numbering.append(f'line {i + 1}: {c}.{s} where {chapter}.{expected} was due')
            expected = s + 1
            if c in titles:
                titles[c].append(m.group(3))
    rep.check(not numbering, 'sections are numbered N.M within their chapter, from 1, with no gap', numbering)

    missing = [f'{c}: {t}' for c, req in REQUIRED.items() for t in req
               if not any(x == t or x.startswith(t + ' ') for x in titles[c])]
    rep.check(not missing, 'every section the template does not mark Optional is present', missing)

    order_problems, unknown = [], []
    for c, have in titles.items():
        known = [t for t in have if t in SECTION_ORDER[c]]
        unknown += [f'{c}: {t}' for t in have if t not in SECTION_ORDER[c]]
        if known != [t for t in SECTION_ORDER[c] if t in known]:
            order_problems.append(f'chapter {c}: {", ".join(known)}')
    rep.check(not order_problems, "sections follow the template's order", order_problems)
    if unknown:
        rep.warn('sections the template does not carry - keep them only if the standard asks for them',
                 unknown)
    # the sections of the standard's Design that a skill's system has nothing to put in - unless the
    # template carries them, as an app's does
    for title, why in (('Directory Structure', "where the programs sit is the skill's to say"),
                       ('Presentation Form', "a person uses no control of the system's own")):
        if any(title in carried for carried in SECTION_ORDER.values()):
            continue
        found = [f'{c}: {t}' for c, have in titles.items() for t in have if t == title]
        rep.check(not found, f'no {title} section: {why}', found)

    blank_before = [f'line {i + 1}: {t}' for i, _, t in doc.heads if i > 0 and lines[i - 1].strip()]
    if blank_before:
        rep.warn('headings with no blank line before them', blank_before)
    old = old_bullets(doc)
    if old:
        rep.warn('bullets in the old form - the template writes "- **Name** — what it is", '
                 'never "* " or a colon after the name', old)

    sections = doc.sections()
    check_forward(doc, rep, sections)
    stages = check_dataflow(doc, rep, sections)
    check_goals(doc, rep, sections)
    check_tables(doc, rep, sections, stages)

    if skill_name:
        hits = [f'line {i + 1}: {l.strip()[:100]}' for i, l in enumerate(lines)
                if re.search(re.escape(skill_name), l, re.IGNORECASE)]
        rep.check(not hits, f'the RSDC never names the skill "{skill_name}"', hits)

    if stages:
        df_line = next((i for (c, s), (i, t) in sections.items() if t == 'Dataflow'), None)
        if df_line is not None:
            early = []
            for i in range(df_line):
                p = doc.prose(i)
                if p is None:
                    continue
                for st in stages:
                    if re.search(rf'(?<![\w-]){re.escape(st)}(?![\w-])', p):
                        early.append(f'line {i + 1}: {st}')
            if early:
                rep.warn('stage names used before the Dataflow names them - a forward reference unless the '
                         'word is used in another sense', early)


def check_forward(doc: Doc, rep: Report, sections: dict) -> None:
    cur, forward, own, unknown = (0, 0), [], [], []
    for i, line in enumerate(doc.lines):
        h = doc.head_at.get(i)
        if h:
            lvl, txt = h
            m2 = CHAPTER_RE.match(txt) if lvl == CHAPTER_LEVEL else None
            m3 = SECTION_RE.match(txt) if lvl == SECTION_LEVEL else None
            if m2:
                cur = (int(m2.group(1)), 0)
            elif m3:
                cur = (int(m3.group(1)), int(m3.group(2)))
            continue
        p = doc.prose(i)
        if p is None:
            continue
        for m in CITE_RE.finditer(p):
            ref = (int(m.group(1)), int(m.group(2)))
            where = f'line {i + 1}: in {cur[0]}.{cur[1]}, cites {ref[0]}.{ref[1]}: {line.strip()[:90]}'
            if ref not in sections:
                unknown.append(where)
            elif ref > cur:
                forward.append(where)
            elif ref == cur:
                own.append(where)
        for m in CHAPTER_CITE_RE.finditer(p):
            later = [n for n in map(int, re.findall(r'[1-4]', m.group(0))) if n > cur[0]]
            if later:
                forward.append(f'line {i + 1}: in {cur[0]}.{cur[1]}, cites chapter {later[0]}: {line.strip()[:90]}')
    rep.check(not forward, 'no forward reference: every citation is of a chapter or section numbered before it',
              forward)
    if own:
        rep.warn('sections that cite themselves', own)
    if unknown:
        rep.warn('numbers that read as citations of sections that do not exist', unknown)


def check_dataflow(doc: Doc, rep: Report, sections: dict) -> list[str]:
    df = next(((i, t) for (c, s), (i, t) in sections.items() if t == 'Dataflow'), None)
    if df is None:
        return []
    body = doc.span(df[0], upto(SECTION_LEVEL))
    h4 = [(i, t) for i, lvl, t in doc.heads if lvl == SUB_LEVEL and i in body]
    names = [strip_bold(t) for _, t in h4]
    rep.check(names[:len(DATAFLOW_PARTS)] == DATAFLOW_PARTS,
              f'the Dataflow opens with its {len(DATAFLOW_PARTS)} parts, in order: ' + ', '.join(DATAFLOW_PARTS),
              [f'found: {", ".join(names) or "no subsection"}'])
    rest = names[len(DATAFLOW_PARTS):]
    part_at = {strip_bold(t): i for i, t in h4}

    # the DFD: the one place that says what each stage reads and writes, so its rounded boxes are
    # the stages. It is found as the Dataflow's first mermaid diagram, not by its part's name - a
    # name looked up would let a renamed part skip every check below without a failure.
    stages: list[str] = []
    flow = next((b for b in doc.blocks if b[0] in body and 'mermaid' in doc.lines[b[0]]), None)
    rep.check(flow is not None, 'the Dataflow holds its DFD, a mermaid diagram')
    if flow is not None:
        # the legend sits under the diagram, in the part that holds it
        holder = max((i for i, _ in h4 if i < flow[0]), default=body.start)
        if find_line(doc, doc.span(holder, upto(SUB_LEVEL)), LEGEND) is None:
            rep.warn(f'no "{LEGEND}" legend under the DFD (an English RSDC needs one)')
        text = doc.block_text(flow)
        stages = rounded_boxes(text)
        rep.check(bool(stages), 'the DFD draws the stages as rounded boxes')
        rep.check('{{' in text, 'the DFD draws a role outside the system as a hexagon')
        odd = odd_shapes(text)
        rep.check(not odd, 'every node of the DFD has a shape of its notation - a piece of data '
                  'is a parallelogram, a flag or a cylinder', odd)
        if BLUE not in text:
            rep.warn('the DFD draws no blue line: nothing is written into a record?')
        # the stages the Dataflow lists as it opens, against the boxes it draws
        first_part = min((i for i, _ in h4), default=body.stop)
        listed = [strip_bold(m.group(1)) for j in range(body.start, first_part)
                  for m in [re.match(r'^[*-]\s+\*\*(.+?)\*\*', doc.lines[j])] if m]
        if listed:
            astray = [f'listed, not drawn: {s}' for s in listed if s not in stages] + \
                     [f'drawn, not listed: {s}' for s in stages if s not in listed]
            rep.check(not astray, 'the stages the Dataflow lists are the rounded boxes it draws', astray)

    # every mermaid diagram, the Execution Flow's included: linkStyle indices exist
    bad = []
    for b in doc.blocks:
        if 'mermaid' not in doc.lines[b[0]]:
            continue
        text = doc.block_text(b)
        n = mermaid_edges(text)
        for idx, line in linkstyle_indices(text):
            over = [x for x in idx if x >= n]
            if over:
                bad.append(f'diagram at line {b[0] + 1}: {n} edges, but linkStyle names {over}')
    rep.check(not bad, 'every linkStyle index names an edge that exists', bad)

    if 'Order Imposed by the Data' in part_at:
        obody = doc.span(part_at['Order Imposed by the Data'], upto(SUB_LEVEL))
        rep.check(find_line(doc, obody, ORDER_SENTENCE, startswith=False) is not None,
                  f'the order part states: {ORDER_SENTENCE}')
    if 'Exception Paths' in part_at:
        ebody = doc.span(part_at['Exception Paths'], upto(SUB_LEVEL))
        absent = [lab for lab in EXCEPTION_LABELS if find_line(doc, ebody, f'**{lab}**', startswith=False) is None]
        rep.check(not absent, 'the exception paths are ' + ', '.join(EXCEPTION_LABELS), absent)

    # the inside of a stage is the Design's: a rule about it is said in words, never drawn here
    inside = [n for n in rest if n.startswith('Inside ')]
    rep.check(not inside, 'no stage is drawn open in the Dataflow - its inside belongs to the Execution Flow, '
              'and a rule about it is said in words', inside)
    others = [n for n in rest if not n.startswith('Inside ')]
    if others:
        rep.warn('Dataflow subsections after its parts', others)
    return stages


def check_goals(doc: Doc, rep: Report, sections: dict) -> None:
    goals_sec = sections.get((1, 4))
    if goals_sec is None:
        return
    goals = []
    for i in doc.span(goals_sec[0], upto(SECTION_LEVEL)):
        m = re.match(r'^[*-]\s+\*\*(.+?)\*\*\s*(?:[:：]|—)', doc.lines[i])
        if m:
            goals.append(m.group(1).strip())
    inv = next(((i, t) for (c, s), (i, t) in sections.items() if t == 'Invariants'), None)
    if inv is None:
        return
    body = doc.span(inv[0], upto(SECTION_LEVEL))
    hdr = next((i for i in body if re.match(r'^\|\s*Goal\s*\|', doc.lines[i])), None)
    rep.check(hdr is not None, 'Invariants ends with the goals table | Goal | ... |')
    if hdr is None:
        return
    rows = [r[0] for r in table_rows(doc, hdr) if r]
    rep.check(sorted(rows) == sorted(goals) and len(rows) == len(goals),
              'the goals table has one row for each goal of 1.4, by its name',
              [f'goal with no row: {g}' for g in goals if g not in rows] +
              [f'row with no goal: {r}' for r in rows if r not in goals])


def check_tables(doc: Doc, rep: Report, sections: dict, stages: list[str]) -> None:
    vo = next(((i, t) for (c, s), (i, t) in sections.items() if t == 'Verification Obligations'), None)
    if vo is not None and find_line(doc, doc.span(vo[0], upto(SECTION_LEVEL)), VERIFY_HEADER) is None:
        rep.warn(f'Verification Obligations has no table {VERIFY_HEADER}')
    # an app is reached through its HTTP API and has no CLI: its components come from Core Component
    # Responsibilities alone
    cli = next(((i, t) for (c, s), (i, t) in sections.items() if t == 'CLI'), None)
    cli_body, progs = [], []
    if cli is not None:
        cli_body = doc.span(cli[0], upto(SECTION_LEVEL))
        # every program is a Python script a caller runs from the command line
        invocations = [(i, m.group(1)) for i in cli_body
                       for m in [re.match(r'^\s*[*-]\s+\*\*Invocation\*\*\s*(?:[:：]|—)\s*`([^`]+)`', doc.lines[i])] if m]
        not_python = [f'line {i + 1}: {cmd[:80]}' for i, cmd in invocations if not cmd.startswith('python ')]
        if not_python:
            rep.warn('invocations that do not run the program as python <program> <arguments>', not_python)
        progs = [m.group(1) for i in cli_body
                 for m in [re.match(r'^[*-]\s+\*\*(.+?)\*\*, the (?:program|module|script)\b', doc.lines[i])] if m]
        if not progs:
            rep.warn('CLI names no component as "- **Role Name**, the program `file`"')
    ccr = next(((i, t) for (c, s), (i, t) in sections.items() if t == 'Core Component Responsibilities'), None)
    if ccr is None:
        return
    ccr_body = doc.span(ccr[0], upto(SECTION_LEVEL))
    comps = [m.group(1) for i in ccr_body
             for m in [re.match(r'^[*-]\s+\*\*(.+?)\*\*', doc.lines[i])] if m]
    # the standard's Core Component Responsibilities breaks down every component chapter 2 names,
    # beside the components nothing outside the system calls, which CLI rightly leaves unnamed
    unbroken = [p for p in progs if p not in comps]
    if unbroken:
        rep.warn('components CLI names that Core Component Responsibilities does not break down', unbroken)
    if stages:
        # a stage finds the component that performs it in CLI, or in Core Component Responsibilities
        text = '\n'.join(doc.lines[i] for i in [*cli_body, *ccr_body])
        idle = [st for st in map(strip_bold, stages)
                if not re.search(rf'(?<![\w-]){re.escape(st)}(?![\w-])', text, re.IGNORECASE)]
        rep.check(not idle, 'every stage of the Dataflow has a component that performs it - one with none '
                  'is an activity nobody implemented', [f'no component performs: {st}' for st in idle])
    if vo is not None:
        # the standard asks Verification Obligations to name every component at least once
        table = '\n'.join(doc.lines[i] for i in doc.span(vo[0], upto(SECTION_LEVEL)) if doc.lines[i].lstrip().startswith('|'))
        unproven = [c for c in comps if c not in table]
        if unproven:
            rep.warn('components no row of Verification Obligations names - nothing shows they work', unproven)


# --------------------------------------------------------------------------- the pair

def line_kind(doc: Doc, i: int) -> str:
    if doc.fence[i]:
        return 'fence'
    line = doc.lines[i]
    if not line.strip():
        return 'blank'
    m = HEADING_RE.match(line)
    if m:
        return f'h{len(m.group(1))}'
    s = line.lstrip()
    ind = len(line) - len(s)
    if s.startswith('|'):
        return f'table/{ind}/{len(split_cells(s))}'
    if re.match(r'[*+-]\s', s):
        return f'bullet/{ind}'
    if re.match(r'\d+\.\s', s):
        return f'item/{ind}'
    if s.startswith('>'):
        return 'quote'
    return f'text/{ind}'


def per_section(doc: Doc, pattern: re.Pattern) -> dict[str, Counter]:
    keys, out = doc.section_keys(), {}
    for i, line in enumerate(doc.lines):
        if doc.fence[i] or i in doc.head_at:
            continue
        found = pattern.findall(line) if pattern is not CITE_RE else \
            [f'{m.group(1)}.{m.group(2)}' for m in CITE_RE.finditer(CODE_RE.sub(' ', line))]
        if found:
            out.setdefault(keys[i], Counter()).update(found)
    return out


def flagged_renderings(keep: Path) -> list[str]:
    words, in_list = [], False
    for line in keep.read_text(encoding='utf-8').split('\n'):
        if line.startswith('## '):
            in_list = line.strip() == '## The list'
            continue
        if in_list and line.startswith('|') and not re.match(r'^\|\s*(Term|-)', line):
            cells = split_cells(line)
            if len(cells) >= 3 and cells[2] not in ('—', '-', ''):
                words += [w.strip() for w in re.split(r'[,，]', cells[2]) if w.strip()]
    return words


def defined_terms(en: Doc) -> list[str]:
    """The names Terminology, Artifact Types and Naming and Data Structures define, and the stage names."""
    terms: list[str] = []
    for (c, s), (i, t) in en.sections().items():
        # an RSDC written before the section was renamed calls it Data Structures
        if c == 2 and (t == 'Terminology' or t.startswith('Artifact Types') or t.endswith('Data Structures')):
            for j in en.span(i, upto(SECTION_LEVEL)):
                m = re.match(r'^\s*[*-]\s+\*\*(.+?)\*\*', en.lines[j])
                if m:
                    name = re.sub(r'^(The|A|An)\s+', '', m.group(1).strip()).rstrip('.:：,')
                    if name and not re.search(f'[{CJK}`]', name) and len(name) < 40:
                        terms.append(name)
        if c == 2 and t == 'Dataflow':
            # the stages: the rounded boxes of the Dataflow's diagram
            flow = [b for b in en.blocks if b[0] in en.span(i, upto(SECTION_LEVEL)) and 'mermaid' in en.lines[b[0]]]
            if flow:
                terms += rounded_boxes(en.block_text(flow[0]))
    return sorted(set(terms))


def check_shared_wording(en: Doc, tw: Doc, rep: Report, tmpl_en: Doc, tmpl_tw: Doc) -> None:
    """A sentence the English RSDC copies from the template is worded in the twin as the
    template's twin words it, so that every RSDC twin says a shared thing the same way."""
    if len(tmpl_en.lines) != len(tmpl_tw.lines):
        rep.fail(f'the template and its twin have as many lines ({len(tmpl_en.lines)} / {len(tmpl_tw.lines)})')
        return
    shared: dict[str, str] = {}
    for j, line in enumerate(tmpl_en.lines):
        t = line.strip()
        if not t or tmpl_en.fence[j] or j in tmpl_en.head_at or t.startswith(('>', '|---')) \
                or PLACEHOLDER_RE.search(t):
            continue
        shared.setdefault(t, tmpl_tw.lines[j].strip())
    off = [f'line {i + 1}: "{tw.lines[i].strip()[:70]}" - the template\'s twin has "{shared[t][:70]}"'
           for i, line in enumerate(en.lines)
           if not en.fence[i] and (t := line.strip()) in shared and tw.lines[i].strip() != shared[t]]
    if off:
        rep.warn("shared sentences the twin words otherwise than the template's twin", off)
    else:
        rep.ok("every shared sentence of the twin is worded as the template's twin words it")


def check_pair(en: Doc, tw: Doc, rep: Report, keep: Path | None,
               templates: tuple[Doc, Doc] | None = None) -> None:
    rep.check(not en.bom and not tw.bom, 'both files are UTF-8 without a byte-order mark')
    if en.crlf != tw.crlf:
        crlf, lf = (en, tw) if en.crlf else (tw, en)
        rep.warn(f'the two files end their lines differently: {crlf.path.name} with CRLF, {lf.path.name} with LF - '
                 'every check here reads CRLF as LF, so make the two match')
    old = old_placeholders(en) + old_placeholders(tw)
    rep.check(not old, 'neither file holds a placeholder in the retired form ___X___',
              [f'convert them: python {PLACEHOLDERS_PY.as_posix()} convert {en.path}'] + old)
    rep.check(tw.unclosed is None, 'every fenced block of the twin is closed')
    same_count = len(en.lines) == len(tw.lines)
    rep.check(same_count, f'the twin has as many lines as the English file ({len(en.lines)} / {len(tw.lines)})')
    if same_count:
        diff = [f'line {i + 1}: {line_kind(en, i)} / {line_kind(tw, i)}'
                for i in range(len(en.lines)) if line_kind(en, i) != line_kind(tw, i)]
        rep.check(not diff, 'line for line: each line of the twin is the same kind as the English line', diff)
        if templates is not None:
            check_shared_wording(en, tw, rep, *templates)

    eh, th = [t for _, _, t in en.heads], [t for _, _, t in tw.heads]
    problems = []
    if len(eh) != len(th):
        problems.append(f'{len(eh)} headings / {len(th)}')
    # an older twin's title may still carry the suffix: it passes, with a warning
    old_title = bool(eh) and bool(th) and th[0] == eh[0] + TW_SUFFIX
    for k, (a, b) in enumerate(zip(eh, th)):
        if k == 0 and old_title:
            continue
        if a != b:
            problems.append(f'{a}  /  {b}')
    rep.check(not problems, 'headings are identical, the title included', problems)
    if old_title:
        rep.warn(f"the twin's title still ends in {TW_SUFFIX}: drop it, the title is the English file's", [th[0]])
    old = old_bullets(tw)
    if old:
        rep.warn('bullets of the twin in the old form - the template\'s twin writes "- **名稱** —— 說明", '
                 'never "* " or a colon after the name', old)

    ef, tf = [en.block_text(b) for b in en.blocks], [tw.block_text(b) for b in tw.blocks]
    fdiff = [f'block {k + 1} (English line {en.blocks[k][0] + 1})' for k, (a, b) in enumerate(zip(ef, tf)) if a != b]
    if len(ef) != len(tf):
        fdiff.insert(0, f'{len(ef)} blocks / {len(tf)}')
    rep.check(not fdiff, 'fenced blocks are byte-identical', fdiff)

    for label, pattern in (('inline-code spans', re.compile(r'`[^`]+`')), ('section citations', CITE_RE)):
        a, b = per_section(en, pattern), per_section(tw, pattern)
        bad = []
        for key in sorted(set(a) | set(b)):
            if a.get(key, Counter()) != b.get(key, Counter()):
                only_en = a.get(key, Counter()) - b.get(key, Counter())
                only_tw = b.get(key, Counter()) - a.get(key, Counter())
                bad.append(f'{key}: English only {dict(only_en)}; twin only {dict(only_tw)}')
        rep.check(not bad, f'every section has the same {label} in both files', bad)

    def targets(doc: Doc, other: str) -> list[str]:
        return [t for i, line in enumerate(doc.lines) if not doc.fence[i]
                for t in LINK_RE.findall(line) if t != other]
    rep.check(targets(en, tw.path.name) == targets(tw, en.path.name),
              'link targets match one for one, a link between the two aside')
    between = ([f'English {d}' for d in links_to(en, tw.path.name)] +
               [f'twin {d}' for d in links_to(tw, en.path.name)])
    rep.check(not between, 'neither file links to the other', between)

    if keep is not None:
        hits = []
        for w in flagged_renderings(keep):
            for i in range(len(tw.lines)):
                p = tw.prose(i)
                if p is not None and w in p:
                    hits.append(f'line {i + 1}: {w}')
        if hits:
            rep.warn('flagged renderings of the keep-English list in the twin\'s prose', hits)
        else:
            rep.ok('no flagged rendering of the keep-English list in the twin\'s prose')

    def pattern(form: str) -> re.Pattern:
        # a term written in lower case runs in prose and is capitalized only where a sentence or a
        # bullet opens, which the two languages do in different places: fold its first letter
        head = f'[{form[0].lower()}{form[0].upper()}]' if form[0].islower() else re.escape(form[0])
        return re.compile(rf'(?<![A-Za-z]){head}{re.escape(form[1:])}(?![A-Za-z])')

    def count(doc: Doc, form: str, i: int | None = None) -> int:
        pat, rng = pattern(form), (range(len(doc.lines)) if i is None else [i])
        return sum(len(pat.findall(p)) for j in rng if (p := doc.prose(j)) is not None)

    fewer = []
    for term in defined_terms(en):
        # compare the form the English prose uses most: "Caller" opens a bullet, "caller" runs in prose
        exact = re.compile(rf'(?<![A-Za-z]){re.escape(term)}(?![A-Za-z])')
        lower = term[0].lower() + term[1:]
        form = lower if sum(len(re.findall(rf'(?<![A-Za-z]){re.escape(lower)}(?![A-Za-z])', p))
                            for i in range(len(en.lines)) if (p := en.prose(i)) is not None) > \
            sum(len(exact.findall(p)) for i in range(len(en.lines)) if (p := en.prose(i)) is not None) else term
        if same_count:   # line for line, so compare each line with its own translation
            fewer += [f'line {i + 1}: {form} ({a} / {b})' for i in range(len(en.lines))
                      if (a := count(en, form, i)) > (b := count(tw, form, i))]
        elif (a := count(en, form)) > (b := count(tw, form)):
            fewer.append(f'{form}: {a} / {b}')
    if fewer:
        rep.warn('terms the twin uses less often than the English file (English / twin) - a term rendered in '
                 'Chinese, or the same word in another sense', fewer)
    else:
        rep.ok('every term of Terminology, Artifact Types, Naming and Data Structures and the stages is used in the twin '
               'wherever the English file uses it')

    glued, bold = [], []
    for i in range(len(tw.lines)):
        if tw.fence[i] or i in tw.head_at:
            continue
        line = CODE_RE.sub('X', tw.lines[i])
        line = LINK_RE.sub('](L)', line)
        if GLUED_RE.search(line):
            glued.append(f'line {i + 1}: ' + ', '.join(m.group(0) for m in GLUED_RE.finditer(line))[:80])
        for m in re.finditer(r'\*\*([^*\n]+?)\*\*', line):
            a, b, inner = m.start(), m.end(), m.group(1)
            if (b < len(line) and re.match(f'[{CJK}]', line[b]) and re.match(r'[A-Za-z0-9X)]', inner[-1])) or \
               (a > 0 and re.match(f'[{CJK}]', line[a - 1]) and re.match(r'[A-Za-z0-9X(]', inner[0])):
                bold.append(f'line {i + 1}: {line[max(0, a - 4):b + 3]}')
    if glued or bold:
        rep.warn('English run into Chinese with no space between them', glued + bold)
    else:
        rep.ok('a space separates English from Chinese throughout the twin')


# --------------------------------------------------------------------------- the skill

def check_skill(rsdc: Doc, skill: Doc, rep: Report) -> None:
    name = None
    if skill.lines and skill.lines[0].strip() == '---':
        for line in skill.lines[1:]:
            if line.strip() == '---':
                break
            m = re.match(r'^name:\s*(\S+)', line)
            if m:
                name = m.group(1).strip('\'"')
    rep.check(name is not None, 'the skill\'s frontmatter has a name')
    if name:
        hits = [f'line {i + 1}: {l.strip()[:100]}' for i, l in enumerate(rsdc.lines)
                if re.search(re.escape(name), l, re.IGNORECASE)]
        rep.check(not hits, f'the RSDC never names the skill "{name}"', hits)

    sections = rsdc.sections()
    subs: dict[tuple[int, int], set[str]] = {}
    for key, (i, title) in sections.items():
        subs[key] = {title} | {strip_bold(t) for j, lvl, t in rsdc.heads
                               if lvl == SUB_LEVEL and j in rsdc.span(i, upto(SECTION_LEVEL))}
    design, absent, misnamed, total = [], [], [], 0
    for i, line in enumerate(skill.lines):
        if skill.fence[i]:
            continue
        for m in SKILL_CITE_RE.finditer(line):
            if EXTERNAL_BEFORE_RE.search(line[:m.start()]):
                continue
            total += 1
            ref = (int(m.group(1)), int(m.group(2)))
            where = f'line {i + 1}: §{ref[0]}.{ref[1]}' + (f' *{m.group(3)}*' if m.group(3) else '')
            if ref[0] >= 3:
                design.append(where)
            if ref not in sections:
                absent.append(where)
            elif m.group(3) and not any(h.startswith(m.group(3).strip()) for h in subs[ref]):
                misnamed.append(f'{where} - the section is "{sections[ref][1]}"')
    rep.check(not design, 'the skill cites no section of the RSDC\'s Design or Coding (chapters 3 and 4)', design)
    rep.check(not absent, f'every § citation ({total}) lands on a section of the RSDC', absent)
    rep.check(not misnamed, 'every heading a § citation names opens that section\'s heading or a subsection\'s',
              misnamed)

    h1 = [(i, t) for i, lvl, t in skill.heads if lvl == 1]
    def h1_span(title: str) -> range | None:
        start = next((i for i, t in h1 if t.strip() == title), None)
        return skill.span(start, (1,)) if start is not None else None
    wf, df = h1_span('Workflow'), h1_span('Dataflow')
    steps = []
    if wf is not None:
        for i, lvl, t in skill.heads:
            if lvl == 2 and i in wf:
                m = re.match(r'^Step\s+(\d+)\s*[-–—:]\s*(.+?)\s*$', t)
                if m:
                    steps.append(f'Step {m.group(1)} - {m.group(2)}')
    if df is None:
        rep.warn('the skill has no "# Dataflow" section, which a skill citing its RSDC carries')
    else:
        # The skill's Dataflow is one diagram, as the SKILL template draws it: the steps already say
        # what each reads and writes, so it carries no table to compare them with.
        blocks = [b for b in skill.blocks if b[0] in df and 'mermaid' in skill.lines[b[0]]]
        rep.check(bool(blocks), 'the skill\'s Dataflow is drawn as a mermaid diagram')
        if blocks:
            text = skill.block_text(blocks[0])
            undrawn = [s for s in steps if s not in node_labels(text)]
            rep.check(not undrawn, 'every step is a node of the skill\'s DFD, by its full name', undrawn)
            n = mermaid_edges(text)
            over = [x for idx, _ in linkstyle_indices(text) for x in idx if x >= n]
            rep.check(not over, 'every linkStyle index of the skill\'s DFD names an edge that exists',
                      [f'{n} edges, but linkStyle names {over}'] if over else None)

    links = [(i, t) for i, line in enumerate(skill.lines) if not skill.fence[i]
             for t in LINK_RE.findall(line) if re.search(r'-RSDC(-tw)?\.md$', t)]
    rep.check(any(Path(t).name == rsdc.path.name for _, t in links), f'the skill links to {rsdc.path.name}')
    # a link may be relative to the skill's directory or to the workspace root above it
    bases = [skill.path.resolve().parent, *skill.path.resolve().parent.parents]
    broken = [f'line {i + 1}: {t}' for i, t in links
              if '{' not in t and not any((b / t).exists() for b in bases)]
    rep.check(not broken, 'every link to an RSDC file resolves, from the skill\'s directory or a directory above it',
              broken)


# --------------------------------------------------------------------------- main

def load(path: str, rep_name: str) -> Doc:
    p = Path(path)
    try:
        return Doc(p)
    except (OSError, UnicodeDecodeError) as e:
        print(f'cannot read the {rep_name} {p}: {e}', file=sys.stderr)
        sys.exit(2)


# --------------------------------------------------------------------------- the version

# The standard's version a template records where it names the standard: at **Version** 261010 -
# in a twin, **版本**. A document's own version is the Version line its header quote opens with,
# > Version: 261010, which the shared depends_on.py reads.
VERSION_RE = re.compile(r'\*\*(?:Version|版本)\*\*[:：]?\s*(\d{6})')


def recorded_version(doc: Doc, rep_name: str) -> str:
    m = next((m for m in map(VERSION_RE.search, doc.lines) if m), None)
    if m is None:
        print(f'the {rep_name} {doc.path} records no **Version**', file=sys.stderr)
        sys.exit(2)
    return m.group(1)


def own_version(doc: Doc) -> str | None:
    """The version a document gives itself: the Version line its header quote opens with."""
    return depends_on_module().version(doc.lines)


def check_version(standard: Doc, templates: list[tuple[str, Doc]], rep: Report) -> None:
    at = own_version(standard)
    if at is None:
        print(f'the RSDC standard {standard.path} gives no version: its header quote opens with no > Version: line',
              file=sys.stderr)
        sys.exit(2)
    for name, doc in templates:
        v = recorded_version(doc, name)
        rep.check(v == at, f"the {name} records the standard's version, {at}", [f'it records {v}'])
        own = own_version(doc)
        rep.check(own is not None, f'the {name} gives its own version in its header quote' + (f', {own}' if own else ''),
                  ['its header quote opens with no > Version: line'])


# A template's links to the standard - its header quote, `> [[RSDC-Standard]]` and `> [[DFD]]` -
# record after each, in the form the shared depends_on.py writes, the fingerprint of the file's
# content as the template was last brought in line with it: > [[RSDC-Standard]]  `2026-10-10`  `1a2b3c4d5e6f`.

def depends_on_module():
    """The shared depends_on.py, which reads a header quote and finds what its links name."""
    shared = COMMON / 'scripts'
    sys.path.insert(0, str(shared))
    try:
        import depends_on
    except ImportError as e:
        print(f'cannot load the shared depends_on.py from {shared}: {e}', file=sys.stderr)
        sys.exit(2)
    return depends_on


def header_notes(path: Path) -> set[str]:
    """The names the [[...]] links of a document's header quote give; none when it cannot be read as one."""
    depends_on = depends_on_module()
    try:
        return {e.target for e in depends_on.entries(path, depends_on.read_lines(path)) if e.kind == 'note'}
    except depends_on.Fault:
        return set()


def named_template(path: Path) -> Path | None:
    """The template an RSDC's header quote names - a [[name]] ending in -tmp - found in the RSDC's vault or
    else in {skillGroups.common}; None when it names none. One it names and nothing holds stops the run."""
    depends_on = depends_on_module()
    names = sorted(n for n in header_notes(path) if n.endswith('-tmp'))
    if not names:
        return None
    if len(names) > 1:
        print(f'{path}: its header quote names several templates: ' + ', '.join(f'[[{n}]]' for n in names), file=sys.stderr)
        sys.exit(2)
    entry = depends_on.Entry(0, f'[[{names[0]}]]', 'note', names[0], False, None, None)
    try:
        found = depends_on.resolve(entry, path, None, None)
    except depends_on.Fault:
        found = None
    try:
        found = found or depends_on.find_note(names[0], COMMON)
    except depends_on.Fault as e:
        print(e, file=sys.stderr)
        sys.exit(2)
    if found is None:
        print(f'{path}: its header quote names [[{names[0]}]], which is in neither its vault nor {COMMON}', file=sys.stderr)
        sys.exit(2)
    return found


def check_pins(standard: Doc, templates: list[tuple[str, Doc]], rep: Report) -> None:
    """Each file of the standard a template links is recorded at its content now: the version
    alone misses a change made under the same version, as every change of one day is."""
    depends_on = depends_on_module()
    here = standard.path.resolve().parent
    for name, doc in templates:
        try:
            links = depends_on.entries(doc.path, depends_on.read_lines(doc.path))
        except depends_on.Fault as e:
            print(e, file=sys.stderr)
            sys.exit(2)
        files = [e for e in links if e.kind == 'note' and (here / f'{e.target}.md').is_file()]
        if standard.path.stem not in {e.target for e in files}:
            print(f'the {name} {doc.path} does not link {standard.path.name} in its header quote', file=sys.stderr)
            sys.exit(2)
        for e in files:
            f = f'{e.target}.md'
            if e.sha is None:
                print(f'the {name} {doc.path} links {f} but records no fingerprint after it', file=sys.stderr)
                sys.exit(2)
            now = depends_on.fingerprint(here / f)
            rep.check(e.sha == now, f'the {name} records {f} at its content now, {now}',
                      [f'it records {e.sha}, of {e.date}: bring it in line with what changed in {f}, then record '
                       f'it anew - depends_on.py record - in both the template and its twin'])


def main() -> None:
    ap = argparse.ArgumentParser(description='Check an RSDC written for a skill\'s system, or for an app.')
    ap.add_argument('--standard', help='the RSDC standard, RSDC-Standard.md: check that the RSDC '
                    'template and its twin record its version, and pin its content')
    ap.add_argument('--rsdc', help='the English RSDC, <SystemName>-RSDC.md (required without --standard)')
    ap.add_argument('--skill-name', help='the skill the RSDC must never name')
    ap.add_argument('--tw', help='the 繁體中文 twin, <SystemName>-RSDC-tw.md: check the pair')
    ap.add_argument('--keep', help='the keep-English list, tw-keep-english.md (with --tw)')
    ap.add_argument('--skill', help='the SKILL.md that cites the RSDC: check its citations')
    ap.add_argument('--template',
                    help='the RSDC template, whose shape the RSDC must have (default: the one its header quote '
                    f'names, else {TEMPLATE})')
    ap.add_argument('--tw-template',
                    help="the template's twin, whose wording the RSDC twin keeps (default: the -tw.md beside the template)")
    a = ap.parse_args()
    if a.standard and (a.rsdc or a.skill_name or a.tw or a.keep or a.skill):
        ap.error('--standard goes alone, or with --template and --tw-template')
    if not a.standard and not a.rsdc:
        ap.error('--rsdc is required, unless --standard is given')
    if a.keep and not a.tw:
        ap.error('--keep goes with --tw')

    if a.standard:
        # before the shape is loaded: a template behind the standard is what this run looks for
        rep = Report()
        std = load(a.standard, 'RSDC standard')
        print(f'== the RSDC template against {std.path.name}')
        template = Path(a.template) if a.template else TEMPLATE
        tw_template = Path(a.tw_template) if a.tw_template else template.with_name(template.stem + '-tw.md')
        templates = [('RSDC template', load(str(template), 'RSDC template')),
                     ("template's twin", load(str(tw_template), "template's twin"))]
        check_version(std, templates, rep)
        check_pins(std, templates, rep)
        verdict = 'FAIL' if rep.failed else 'PASS'
        print(f'verdict: {verdict} - {rep.passed} passed, {rep.failed} failed, {rep.warned} warnings')
        sys.exit(1 if rep.failed else 0)

    named = None if a.template else named_template(Path(a.rsdc))
    template = Path(a.template) if a.template else (named or TEMPLATE)
    tw_template = Path(a.tw_template) if a.tw_template else template.with_name(template.stem + '-tw.md')
    print(f'== the template: {template.name}' + (', as the header quote names it' if named else
                                                ', as --template names it' if a.template else
                                                ', since the header quote names none'))
    tmpl = load(str(template), 'RSDC template')
    lacking = load_shape(tmpl)
    if lacking:
        print('the RSDC template and this script disagree - the template lacks: ' + '; '.join(lacking),
              file=sys.stderr)
        sys.exit(2)

    rep = Report()
    rsdc = load(a.rsdc, 'English RSDC')
    if a.tw:
        tw = load(a.tw, 'twin')
        keep = Path(a.keep) if a.keep else None
        if keep is not None and not keep.is_file():
            print(f'cannot read the keep-English list {keep}', file=sys.stderr)
            sys.exit(2)
        print(f'== the pair: {rsdc.path.name} / {tw.path.name}')
        check_pair(rsdc, tw, rep, keep, (tmpl, load(str(tw_template), "template's twin")))
    if a.skill:
        skill = load(a.skill, 'skill')
        print(f'== the skill: {skill.path} citing {rsdc.path.name}')
        check_skill(rsdc, skill, rep)
    if not a.tw and not a.skill:
        print(f'== the English RSDC: {rsdc.path.name}')
        check_rsdc(rsdc, rep, a.skill_name, template)

    verdict = 'FAIL' if rep.failed else 'PASS'
    print(f'verdict: {verdict} - {rep.passed} passed, {rep.failed} failed, {rep.warned} warnings')
    sys.exit(1 if rep.failed else 0)


if __name__ == '__main__':
    main()
