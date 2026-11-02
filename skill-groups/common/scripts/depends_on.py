#!/usr/bin/env python3
"""Check and record what a document depends on: the fingerprint of every document it was last
brought in line with.

A document A that depends on a document B - a skill on the RSDC it cites, a note on the notes it
borrows from - declares B in its header quote, and keeps there B's fingerprint as it stood when
someone last read B and confirmed that A still holds. `check` computes each fingerprint again and
says which have changed since; `record` writes the current ones, and is run only after that
reading: a fingerprint recorded without it vouches for an A nobody checked against the B it now
has.

The header quote is the run of `>` lines at the head of A - under its frontmatter, its title or a
twin's pairing line, before anything else. It may open with A's own version, the date of that
version as yymmdd, which a tool such as check_rsdc.py reads there and a twin copies as it is:

  > Version: 261010

Every other line of it is one dependency: a link to B, then `cited` when only the sections of B
that A cites count, then the record - the date it was confirmed, and B's fingerprint then - each
in inline code of its own:

  > [[RSDC-Standard]]  `2026-10-10`  `a6b1c2712472`
  > [[SkillCompiler-RSDC]]  `cited`  `2026-10-10`  `bd7932a83cd3`
  > [股票停損價](<{wikiDir}/plan/股票停損價.md>)  `2026-10-07`  `7e1d491bf28e`

An RSDC and a wiki note already declare what they depend on there - `> [[RSDC-Standard]]` - so one
form serves every kind of document. The link and `cited` are written by whoever declares the
dependency; the date and the fingerprint are this script's, and `record` fills them in. A line
with no date and fingerprint declares a dependency not recorded yet.

  [[Name]]      a note in A's vault: the one Name.md under the nearest directory above A that holds
                .obsidian, or failing that .git. When the vault has none, it is looked for under each
                skillGroups root of config.yaml in turn, where a document written in one workspace
                finds the RSDC standard kept in another. Name must be unique where it is found, as
                Obsidian needs it. A Name that carries an extension of its own and names no note,
                such as [[ASD-STE100_ISSUE9.pdf]], is the one file of exactly that name, found the
                same way, as Obsidian links an attachment.
  [text](path)  a file by its path, relative to A's directory. It may name a value of config.yaml
                in braces, such as {wikiDir}; a path with spaces is written in <...>.
  cited         narrows the fingerprint to the sections of B that A cites as §N.M *Heading*: each
                section whose heading opens with the heading cited, matched by its words rather
                than its number, so that renumbering B moves no citation off its section. A citation
                without a heading is matched by number; one right after another file's name -
                `plan.md` §2 - is of that file.

A fingerprint is the first 12 hex digits of the SHA-256 of B's text decoded as UTF-8, with any
byte-order mark removed and every line ending made LF - as compile-skill's source_fingerprint()
computes its own, so a sync that rewrites line endings is not a change - and with B's own header
quote left out, its Version line with it, so that confirming B's dependencies does not make
everything that depends on B look changed. A B that is not UTF-8 text, such as a PDF, has no lines to normalise, no header quote
and no sections to cite: its fingerprint is the first 12 hex digits of the SHA-256 of its bytes.

A record follows no dependency further: A keeps only what it depends on directly.

Usage:
  python depends_on.py check  <A.md>... [--config config.yaml] [--root DIR]
  python depends_on.py record <A.md> [--target T [--cited]] [--date YYYY-MM-DD] [--config ...] [--root DIR]
  python depends_on.py hash   <B.md> [--cited-by A.md]

check   prints one line per dependency - [UNCHANGED], [CHANGED], [NO_RECORD], [NOTHING_CITED] or
        [MISSING] - and writes nothing.
record  writes the date and the current fingerprint after each link of A's header quote:
        every dependency A declares, or only --target - "[[Name]]", Name or a link's path - which
        must be declared first. A twin beside A (A-tw.md) keeps a header quote of its own; record
        says so, and leaves it as it is.
hash    prints B's fingerprint, narrowed to the sections A.md cites when --cited-by names it.

Exit status: 0 nothing changed, or the record is written; 1 a dependency changed, has no record, or
has nothing cited; 2 the command is malformed, or a file is missing, cannot be read, or holds a
header quote that does not parse.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

import yaml

DIGITS = 12
# The line a header quote may open with: the document's own version, the date of it as yymmdd.
VERSION_RE = re.compile(r'^>\s*Version:\s*(?P<version>\d{6})\s*$')
# One line of a header quote: a link - [[Name]], [[Name|alias]] or [text](path) - and its record.
ENTRY_RE = re.compile(r'^>\s*(?P<link>\[\[(?P<name>[^\]|#]+)(?:\|[^\]]*)?\]\]'
                      r'|\[[^\]]*\]\((?:<(?P<apath>[^>]+)>|(?P<path>[^)\s]+))\))'
                      r'(?P<rec>(?:\s+`[^`]*`)*)\s*$')
CODE_RE = re.compile(r'`([^`]*)`')
DATE_RE = re.compile(r'\d{4}-\d{2}-\d{2}')
SHA_RE = re.compile(r'[0-9a-f]{12}')
# A citation of a section, §2.4 or §2.4 *CLI*, as the RSDC Checker reads one; a citation right
# after another file's name - `plan.md` §2 - is of that file.
CITE_RE = re.compile(r'§\s?(\d)\.(\d+)(?:\s*\*([^*]+)\*)?')
EXTERNAL_BEFORE_RE = re.compile(r'(\.md`?|〉|》)\s*$')
HEADING_RE = re.compile(r'^(#{1,6})\s+(.*?)\s*$')
FENCE_RE = re.compile(r'^\s*(```|~~~)')
PLACEHOLDER_RE = re.compile(r'\{([^{}]+)\}')
# The lines a header quote may sit under: a title, a twin's pairing line.
LEAD = 2
SKIP_DIRS = {'.git', '.obsidian', '.trash', '.venv', 'node_modules', '__pycache__'}


class Fault(Exception):
    """A file missing, unreadable or malformed: exit status 2."""


@dataclass
class Entry:
    line: int
    link: str
    kind: str  # 'note' for [[Name]], 'path' for [text](path)
    target: str
    cited: bool
    sha: str | None
    date: str | None

    def text(self) -> str:
        spans = (['cited'] if self.cited else []) + ([self.date, self.sha] if self.sha else [])
        return f'> {self.link}' + ''.join(f'  `{s}`' for s in spans)


# --------------------------------------------------------------------------- reading a file

def read_lines(path: Path) -> list[str]:
    try:
        return split_text(Path(path).read_bytes().decode('utf-8'))
    except (OSError, UnicodeDecodeError) as e:
        raise Fault(f'cannot read {path}: {e}')


def split_text(text: str) -> list[str]:
    """A file's text as its lines, any byte-order mark removed and every line ending made LF."""
    if text.startswith('\ufeff'):
        text = text[1:]
    return text.replace('\r\n', '\n').replace('\r', '\n').split('\n')


def body_start(lines: list[str]) -> int:
    """The first line after the frontmatter, or 0 when there is none."""
    if lines and lines[0].strip() == '---':
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == '---'), None)
        if end is not None:
            return end + 1
    return 0


def quote(lines: list[str]) -> list[int]:
    """Every line of the header quote: the Version line it may open with, and the run of dependency
    lines after it, at the head of a document - under at most LEAD other lines, a title or a twin's
    pairing line, and before any deeper heading."""
    lead, i = 0, body_start(lines)
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if VERSION_RE.match(line) or ENTRY_RE.match(line):
            block = [i] if VERSION_RE.match(line) else []
            i += len(block)
            while i < len(lines) and ENTRY_RE.match(lines[i]):
                block.append(i)
                i += 1
            return block
        if lead >= LEAD or FENCE_RE.match(line) or re.match(r'^#{2,}\s', line):
            return []
        lead += 1
        i += 1
    return []


def header(lines: list[str]) -> list[int]:
    """The dependency lines of the header quote: every line of it but the Version line."""
    return [i for i in quote(lines) if not VERSION_RE.match(lines[i])]


def version(lines: list[str]) -> str | None:
    """The version a document gives itself on the Version line its header quote opens with, or None."""
    q = quote(lines)
    m = VERSION_RE.match(lines[q[0]]) if q else None
    return m['version'] if m else None


def parse_entry(path: Path, lines: list[str], i: int) -> Entry:
    """Line i read as one dependency, or a Fault saying why it is not one."""
    m = ENTRY_RE.match(lines[i])
    if m is None:
        raise Fault(f'{path}:{i + 1}: not a link followed only by its record: {lines[i].strip()}')
    spans = [s.strip() for s in CODE_RE.findall(m['rec'])]
    cited = spans[:1] == ['cited']
    rest = spans[1:] if cited else spans
    if rest and not (len(rest) == 2 and DATE_RE.fullmatch(rest[0]) and SHA_RE.fullmatch(rest[1])):
        raise Fault(f'{path}:{i + 1}: after the link come `cited` if only the sections cited count, '
                    f'then `<date>` `<fingerprint>`: {lines[i].strip()}')
    date, sha = rest if rest else (None, None)
    kind, target = ('note', m['name'].strip()) if m['name'] else ('path', m['apath'] or m['path'])
    return Entry(i, m['link'], kind, target, cited, sha, date)


def entries(path: Path, lines: list[str]) -> list[Entry]:
    return [parse_entry(path, lines, i) for i in header(lines)]


# --------------------------------------------------------------------------- fingerprints

def headings(lines: list[str]) -> list[tuple[int, int, str]]:
    """(line, level, text) of every heading outside the frontmatter and fenced code."""
    out, fenced = [], False
    for i in range(body_start(lines), len(lines)):
        if FENCE_RE.match(lines[i]):
            fenced = not fenced
        elif not fenced:
            m = HEADING_RE.match(lines[i])
            if m:
                out.append((i, len(m.group(1)), m.group(2)))
    return out


def heading_words(text: str) -> tuple[str | None, str]:
    """A heading's section number, such as 2.1, and its words: **2.1 Artifact Types** gives
    ('2.1', 'Artifact Types')."""
    t = text.strip()
    if t.startswith('**') and t.endswith('**') and len(t) > 4:
        t = t[2:-2].strip()
    m = re.match(r'^(\d+\.\d+)\s+(.+)$', t)
    if m:
        return m.group(1), m.group(2).strip()
    m = re.match(r'^\d+\.\s+(.+)$', t)
    return (None, m.group(1).strip()) if m else (None, t)


def citations(lines: list[str]) -> set[tuple[str, str | None]]:
    """Every § citation outside the frontmatter and fenced code: (number, heading or None)."""
    out, fenced = set(), False
    for i in range(body_start(lines), len(lines)):
        line = lines[i]
        if FENCE_RE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        for m in CITE_RE.finditer(line):
            if not EXTERNAL_BEFORE_RE.search(line[:m.start()]):
                out.add((f'{m.group(1)}.{m.group(2)}', (m.group(3) or '').strip() or None))
    return out


def opens_with(words: str, cited: str) -> bool:
    return words == cited or words.startswith(cited + ' ') or words.startswith(cited + ':')


def cited_sections(lines: list[str], cites: set[tuple[str, str | None]]) -> list[tuple[str, str]]:
    """The sections of a document that the citations land on, in the document's order: (heading,
    text from the heading to the next heading at its level or above)."""
    heads = headings(lines)
    out = []
    for k, (i, level, text) in enumerate(heads):
        if level == 1:
            continue
        number, words = heading_words(text)
        if any(opens_with(words, h) if h else number == n for n, h in cites):
            stop = next((j for j, lv, _ in heads[k + 1:] if lv <= level), len(lines))
            out.append((words, '\n'.join(lines[i:stop])))
    return out


def digest(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:DIGITS]


def scope_text(lines: list[str], cites: set[tuple[str, str | None]] | None = None) -> str | None:
    """The text a fingerprint is taken of: the file, its own header quote and its Version line left
    out, narrowed to the sections `cites` land on when it is given - or None when they land on none."""
    own = set(quote(lines))
    if own:
        # with the blank lines after it, so a file with a header quote reads as it did before one
        j = max(own) + 1
        while j < len(lines) and not lines[j].strip():
            own.add(j)
            j += 1
    lines = [line for k, line in enumerate(lines) if k not in own]
    if cites is None:
        return '\n'.join(lines)
    parts = cited_sections(lines, cites)
    return '\n'.join(text for _, text in parts) if parts else None


def fingerprint(path: Path, cites: set[tuple[str, str | None]] | None = None) -> str | None:
    """The fingerprint of a file's scope_text, or None when `cites` land on no section of it. A file
    that is not UTF-8 text, such as a PDF, is fingerprinted by its bytes, and has no section to cite."""
    try:
        data = Path(path).read_bytes()
    except OSError as e:
        raise Fault(f'cannot read {path}: {e}')
    try:
        decoded = data.decode('utf-8')
    except UnicodeDecodeError:
        return None if cites is not None else hashlib.sha256(data).hexdigest()[:DIGITS]
    text = scope_text(split_text(decoded), cites)
    return None if text is None else digest(text)


# --------------------------------------------------------------------------- resolving a link

def load_config(path: Path) -> dict:
    """config.yaml, with its own directory under '_dir': a relative path in it, such as
    skillGroups.dedi: .claude, is relative to the workspace the file sits at the root of."""
    try:
        config = yaml.safe_load('\n'.join(read_lines(path))) or {}
    except yaml.YAMLError as e:
        raise Fault(f'{path} does not parse: {e}')
    if not isinstance(config, dict):
        raise Fault(f'{path} is not a mapping')
    config['_dir'] = str(Path(path).resolve().parent)
    return config


def config_path(config: dict, value: object) -> Path:
    p = Path(str(value)).expanduser()
    return p if p.is_absolute() else Path(config.get('_dir', '.')) / p


def lookup(config: dict, key: str) -> str:
    value: object = config
    for part in re.sub(r'\[([^\]]+)\]', r'.\1', key).split('.'):
        if not isinstance(value, dict) or part not in value:
            raise Fault(f'config.yaml has no {key}')
        value = value[part]
    return str(config_path(config, value))


def vault_root(owner: Path) -> Path:
    base = owner.resolve().parent
    for marker in ('.obsidian', '.git'):
        for d in [base, *base.parents]:
            if (d / marker).exists():
                return d
    raise Fault(f'{owner} is in no vault - no directory above it holds .obsidian or .git; give --root')


def find_note(name: str, root: Path) -> Path | None:
    """The one Name.md under root - or, when there is none and Name carries an extension of its own,
    such as spec.pdf, the one file of exactly that name, as Obsidian links an attachment."""
    notes, named = [], []
    attachment = Path(name).suffix.lower() not in ('', '.md')
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        if f'{name}.md' in files:
            notes.append(Path(d) / f'{name}.md')
        if attachment and name in files:
            named.append(Path(d) / name)
    hits = notes or named
    if len(hits) > 1:
        kind = 'notes' if notes else 'files'
        raise Fault(f'[[{name}]] names several {kind} under {root}: ' + ', '.join(map(str, hits))
                    + ' - link it by its path instead')
    return hits[0] if hits else None


def resolve(e: Entry, owner: Path, config: dict | None, root: Path | None) -> Path | None:
    if e.kind == 'note':
        found = find_note(e.target, root or vault_root(owner))
        groups = (config or {}).get('skillGroups') or {}
        for value in (groups.values() if found is None and root is None and isinstance(groups, dict) else []):
            base = config_path(config, value) if value else None
            if base is not None and base.is_dir():
                found = find_note(e.target, base)
                if found is not None:
                    break
        return found
    target = unquote(e.target)
    if PLACEHOLDER_RE.search(target):
        if config is None:
            raise Fault(f'{owner}: {e.target} names a value of config.yaml: give --config')
        target = PLACEHOLDER_RE.sub(lambda m: lookup(config, m.group(1)), target)
    p = Path(target).expanduser()
    p = p if p.is_absolute() else owner.parent / p
    return p if p.is_file() else None


# --------------------------------------------------------------------------- the commands

def scope(e: Entry) -> str:
    return ' (the sections it cites)' if e.cited else ''


def check(paths: list[Path], config: dict | None, root: Path | None) -> int:
    counts = dict.fromkeys(('UNCHANGED', 'CHANGED', 'NO_RECORD', 'NOTHING_CITED', 'MISSING'), 0)
    for owner in paths:
        print(f'== {owner}')
        lines = read_lines(owner)
        deps = entries(owner, lines)
        if not deps:
            print(f'[NO_RECORD] {owner.name} declares no dependency in its header quote')
            counts['NO_RECORD'] += 1
            continue
        cites = citations(lines)
        for e in deps:
            target = resolve(e, owner, config, root)
            now = None if target is None else fingerprint(target, cites if e.cited else None)
            if target is None:
                verdict, why = 'MISSING', 'no such file'
            elif now is None:
                verdict, why = 'NOTHING_CITED', f'{owner.name} cites no section of it'
            elif e.sha is None:
                verdict, why = 'NO_RECORD', f'never recorded: read it, then record ({now})'
            elif e.sha == now:
                verdict, why = 'UNCHANGED', f'{now}, as confirmed on {e.date}'
            else:
                verdict, why = 'CHANGED', (f'recorded {e.sha} on {e.date}, now {now}: '
                                           f'read what changed, then record once {owner.name} still holds')
            counts[verdict] += 1
            print(f'[{verdict}] {e.link}{scope(e)} - {why}')
    print('verdict: ' + ('MISSING' if counts['MISSING'] else 'UNCHANGED' if counts['UNCHANGED'] == sum(counts.values())
                         else 'CHANGED') + ' - ' + ', '.join(f'{n} {k.lower().replace("_", " ")}' for k, n in counts.items()))
    return 2 if counts['MISSING'] else 0 if counts['UNCHANGED'] == sum(counts.values()) else 1


def record_cmd(owner: Path, target: str | None, cited: bool, date: str,
               config: dict | None, root: Path | None) -> int:
    lines = read_lines(owner)
    deps = entries(owner, lines)
    if not deps:
        raise Fault(f'{owner} declares no dependency: write its link in the header quote first, such as > [[Name]]')
    if target is not None:
        want = target.strip()
        want = want[2:-2] if want.startswith('[[') and want.endswith(']]') else want
        chosen = [e for e in deps if e.target == want]
        if not chosen:
            raise Fault(f'{owner} does not declare {target}: write its link in the header quote first')
        for e in chosen:
            e.cited = e.cited or cited
    else:
        chosen = deps
    cites = citations(lines)
    done = []
    for e in chosen:
        path = resolve(e, owner, config, root)
        if path is None:
            raise Fault(f'{owner}: {e.link} names no file')
        now = fingerprint(path, cites if e.cited else None)
        if now is None:
            raise Fault(f'{owner.name} cites no section of {e.link}, so it has nothing to record as cited')
        was = f' (was {e.sha}, {e.date})' if e.sha else ''
        e.sha, e.date = now, date
        lines[e.line] = e.text()
        done.append(f'recorded {e.link}{scope(e)}: {now}, {date}{was}')
    owner.write_text('\n'.join(lines), encoding='utf-8')
    print(f'== {owner}')
    print('\n'.join(done))
    twin = owner.with_name(owner.stem + '-tw' + owner.suffix)
    if twin.is_file():
        print(f'note: {twin.name} keeps a header quote of its own - regenerate the twin, or record it as well')
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description='Check and record the fingerprints of the documents a document depends on.')
    sub = ap.add_subparsers(dest='command', required=True)
    c = sub.add_parser('check', help='say which dependencies changed since they were recorded')
    c.add_argument('files', nargs='+', type=Path)
    r = sub.add_parser('record', help='write the current fingerprints, after reading what changed')
    r.add_argument('file', type=Path)
    r.add_argument('--target', help='record only this dependency: "[[Name]]", Name, or the path of a link')
    r.add_argument('--cited', action='store_true', help='with --target: narrow it to the sections the file cites')
    r.add_argument('--date', default=datetime.date.today().isoformat(), help='the date of the confirmation')
    for p in (c, r):
        p.add_argument('--config', type=Path, help='config.yaml, for a path that names one of its values')
        p.add_argument('--root', type=Path, help='the vault a [[Name]] link is found under')
    h = sub.add_parser('hash', help="print a file's fingerprint")
    h.add_argument('file', type=Path)
    h.add_argument('--cited-by', type=Path, help='narrow it to the sections this file cites')
    a = ap.parse_args()
    if a.command == 'record' and a.cited and not a.target:
        ap.error('--cited goes with --target')
    if a.command == 'record' and not re.fullmatch(r'\d{4}-\d{2}-\d{2}', a.date):
        ap.error('--date is YYYY-MM-DD')
    try:
        config = load_config(a.config) if getattr(a, 'config', None) else None
        if a.command == 'check':
            sys.exit(check(a.files, config, a.root))
        if a.command == 'record':
            sys.exit(record_cmd(a.file, a.target, a.cited, a.date, config, a.root))
        fp = fingerprint(a.file, citations(read_lines(a.cited_by)) if a.cited_by else None)
        if fp is None:
            raise Fault(f'{a.cited_by} cites no section of {a.file}')
        print(fp)
    except Fault as e:
        print(f'error: {e}', file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
