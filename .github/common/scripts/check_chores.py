#!/usr/bin/env python3
"""Check that a workspace's chore list agrees with itself: its summary table, its chore files and its run records.

A chore is work that comes back: it is done whenever its condition holds, again and again, so it is never
finished, only stopped. A chore is named, as a skill is - keep-english - and no two chores in all the agencies
share a name. The workspace keeps one file per chore of its own, and a summary (an Obsidian vault; links between
them are wikilinks):

  chores/<name>.md     one chore: its heading, its three lines, its five chapters - what it is, never its runs
  chore-summary.md     the opening paragraph, the table, the legend of its icons, and "## 執行紀錄", the runs

A workspace may also do a chore of another agency, one whose skill group it uses. That chore has no file here:
its row names it as text - a wikilink would find nothing in this vault - and the agencies of config.yaml say
where to look for its file:

  agencies:
    SkillsGestalt: ~/Library/CloudStorage/Dropbox/2-Areas-I/SkillsGestalt

A workspace that does only such chores may have no chores/ folder at all - git keeps no empty folder -
and a missing one is taken as empty.

A chore file opens with its heading and its three lines:

  # <name> - <title>

  **Status**：<使用中|暫停|停用>——<the detail>
  **Started**：<YYYY-MM-DD>，<why it was started>
  **When**：<when it is due, on one line>
  **Private**：<the agency that alone does it, and why - only for a private chore>

Then the numbered chapters, in this order: "## 1. 目的", "## 2. 何時要做", "## 3. 怎麼做", "## 4. 驗證",
"## 5. 與其他 task、chore 的關係" ("###" inside them is free; a chapter with nothing to say holds "—").

The summary repeats each chore in a row of its table, newest Started first, a tie by name, with a legend for
its icons beneath:

  | Chore | Started | Title | 何時要做 | 上次執行 | Status |
  |---|---|---|---|---|---|
  | [[<name>]] or <name> | <YYYY-MM-DD> | <title> | <its When line> | <its newest run, or —> | <🔁|⏸️|⏹️> |

Below the legend, "## 執行紀錄" holds a "### <name>" for each chore that was done, in the order of the table,
and in it a "#### YYYY-MM-DD" for each day it was done, newest first.

The table is read instead of the files, to see which chore is due; a row that disagrees with its file
misleads exactly there, and several sessions edit these files at once. What a program can compare, this
script compares:

  1. files       the folder holds only <name>.md files, each name lowercase letters, digits and hyphens,
                 starting with a letter
  2. rows        each row has six cells: [[<name>]] for a chore of this workspace, <name> as text for one of
                 another agency
  3. own         one [[<name>]] row per file, and no row of text names a file of this folder
  4. others      each row of text names a chore file that one of the agencies of config.yaml has
  5. order       the rows are newest Started first, a tie by name
  6. headings    each chore file opens with "# <name> - <title>", <name> its file name, and no "|" in the title
  7. titles      each row's Title is its chore file's title
  8. lines       each chore file of this workspace has its Status, Started and When lines, a date on Started
  9. started     each row of this workspace's chores has its file's Started; every row has a date there
  10. when       each row's 何時要做 is its chore file's When line
  11. icons      each row's icon is one of 🔁 ⏸️ ⏹️ - and, for this workspace's chores, its Status line's word
  12. legend     the legend of the icons follows the table
  13. references each wikilink and relative Markdown link in a chore file of this workspace lands on a file
                 that exists - a wikilink by file name anywhere in the vault (--vault, else the folder with
                 .obsidian, else the folder holding both the summary and the chores); in a git repository,
                 among the vault's files that git tracks or does not ignore
  14. chapters   each chore file of this workspace has the five numbered "##" chapters, in order
  15. runs       "## 執行紀錄" has a "### <name>" only for a row of the table, in its order, each once; its days
                 are real dates, one per day, newest first, none before the row's Started
  16. last run   each row's 上次執行 is its newest run day, or — when it has none
  17. programs   a chore has no program of its own: each command of a chore file of this workspace that runs a
                 file - python, node, bash, sh and the like followed by a path, or a path run as it is - names
                 it as {skillGroups.X}/..., X a skill group of config.yaml; a real path such as
                 .github/common/... fails too, as it would not run in another agency. A command with no path,
                 such as git or gh, is not looked at
  18. private    no row of text names a private chore - one whose file has a **Private** line

What it cannot judge - whether a chore is due, whether a run did what it says - stays with whoever edits
the files.

Every check prints one line, [PASS] or [FAIL], each failure followed by what it found, and the run ends with
a verdict.

Exit status: 0 no check failed; 1 a check failed; 2 the command is malformed, a file cannot be read, or the
summary holds no chore table.
Standard library only.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from urllib.parse import unquote

HEADER = '| Chore | Started | Title | 何時要做 | 上次執行 | Status |'
NAME = r'[a-z][a-z0-9-]*'
FILE_RE = re.compile(rf'^({NAME})\.md$')
HEADING_RE = re.compile(rf'^# ({NAME}) - (.+?)\s*$')
OWN_RE = re.compile(rf'^\[\[({NAME})\]\]$')
TEXT_RE = re.compile(rf'^({NAME})$')
STATUS_RE = re.compile(r'^\*\*Status\*\*：(.+?)——')
STARTED_RE = re.compile(r'^\*\*Started\*\*：(\d{4}-\d{2}-\d{2})')
WHEN_RE = re.compile(r'^\*\*When\*\*：(.+?)\s*$')
PRIVATE_RE = re.compile(r'^\*\*Private\*\*：')
RUNNER = r'(?:python3?|py|node|deno|bash|sh|zsh|pwsh|powershell|ruby|perl)'
RUN_FILE_RE = re.compile(rf'(?:^|[\s;&|(]){RUNNER}\s+(?:-\S+\s+)*([^\s`;&|)]+\.(?:py|js|mjs|cjs|ts|sh|ps1|rb|pl))')
RUN_PATH_RE = re.compile(r'(?:^|[;&|(]\s*)(\.{1,2}/[^\s`;&|)]+|\{skillGroups\.\w+\}/[^\s`;&|)]+)')
GROUP_PATH_RE = re.compile(r'^\{skillGroups\.(\w+)\}/')
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
WIKI_RE = re.compile(r'!?\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]')
MD_LINK_RE = re.compile(r'\]\(([^)\s]+)\)')
RUNS = '## 執行紀錄'
RUN_CHORE_RE = re.compile(r'^### (.+?)\s*$')
RUN_DAY_RE = re.compile(r'^#### (.+?)\s*$')
NONE = '—'
ICONS = {'使用中': '🔁', '暫停': '⏸️', '停用': '⏹️'}
LEGEND = 'Status：🔁 使用中'
CHAPTERS = ['1. 目的', '2. 何時要做', '3. 怎麼做', '4. 驗證', '5. 與其他 task、chore 的關係']


class Report:
    def __init__(self) -> None:
        self.failed = 0
        self.passed = 0

    def check(self, ok: bool, what: str, details: list[str] | None = None) -> None:
        if ok:
            self.passed += 1
            print(f'[PASS] {what}')
            return
        self.failed += 1
        print(f'[FAIL] {what}')
        for d in details or []:
            print(f'         {d}')


def cells(row: str) -> list[str]:
    return [c.strip() for c in row.strip().strip('|').split('|')]


def read_summary(path: Path) -> tuple[list[str], list[list[str]], int]:
    """The summary's lines, the table's rows, and the line after them."""
    lines = path.read_text(encoding='utf-8-sig').split('\n')
    try:
        top = next(i for i, l in enumerate(lines) if l.strip().replace(' ', '') == HEADER.replace(' ', ''))
    except StopIteration:
        print(f'{path}: no chore table - a line "{HEADER}"', file=sys.stderr)
        sys.exit(2)
    rows, i = [], top + 2
    while i < len(lines) and lines[i].strip().startswith('|'):
        rows.append(cells(lines[i]))
        i += 1
    return lines, rows, i


def read_block(config: Path, block: str) -> dict[str, str]:
    """The entries of a block of config.yaml, such as agencies or skillGroups: each "name: value" under
    "<block>:". Read by hand, as the rest of this script needs no YAML: one level, a # comment allowed."""
    if not config.is_file():
        return {}
    found: dict[str, str] = {}
    inside = False
    for line in config.read_text(encoding='utf-8-sig').split('\n'):
        bare = re.sub(r'\s+#.*$', '', line).rstrip()
        if not bare or bare.lstrip().startswith('#'):
            continue
        if not bare.startswith((' ', '\t')):
            inside = bare == f'{block}:'
            continue
        if inside and ':' in bare:
            key, value = (x.strip().strip('"\'') for x in bare.split(':', 1))
            if key and value:
                found[key] = value
    return found


def commands(body: list[str]) -> list[str]:
    """The code a chore file shows - each inline-code span, and each line of a fenced block."""
    out, fenced = [], False
    for l in body:
        if l.lstrip().startswith(('```', '~~~')):
            fenced = not fenced
            continue
        out += [l] if fenced else re.findall(r'`([^`]+)`', l)
    return out


def run_paths(code: str) -> list[str]:
    """The files a line of code runs: the path after an interpreter, or a path run as it is."""
    return RUN_FILE_RE.findall(code) + [p for p in RUN_PATH_RE.findall(code.strip()) if p not in RUN_FILE_RE.findall(code)]


def read_runs(lines: list[str]) -> tuple[list[tuple[str, list[str]]], list[str]]:
    """Each "### <name>" under "## 執行紀錄", in order, with its "#### <day>" headings; and what is malformed."""
    try:
        start = lines.index(RUNS)
    except ValueError:
        return [], []
    runs: list[tuple[str, list[str]]] = []
    problems: list[str] = []
    for l in lines[start + 1:]:
        if l.startswith('## '):
            problems.append(f'a "##" heading after "{RUNS}": {l[:50]}')
            break
        if m := RUN_DAY_RE.match(l):
            if runs:
                runs[-1][1].append(m.group(1))
            else:
                problems.append(f'a day before any "### <name>": {m.group(1)}')
        elif m := RUN_CHORE_RE.match(l):
            runs.append((m.group(1), []))
    return runs, problems


def known_names(root: Path) -> set[str]:
    """The names of the files a wikilink can land on: in a git repository, the vault's files that git tracks or does
    not ignore, and that are there; elsewhere, every file under the vault."""
    try:
        out = subprocess.run(['git', '-C', str(root), 'ls-files', '--cached', '--others', '--exclude-standard', '-z'],
                             capture_output=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return {p.name for p in root.rglob('*') if p.is_file()}
    return {Path(p).name for p in out.decode('utf-8', 'replace').split('\0') if p and (root / p).is_file()}


def links_outside_code(lines: list[str]) -> tuple[list[str], list[str]]:
    """The Markdown link targets and the wikilink names of a file, leaving out fenced blocks and inline code."""
    found, wikis, fenced = [], [], False
    for l in lines:
        if l.lstrip().startswith(('```', '~~~')):
            fenced = not fenced
            continue
        if fenced:
            continue
        for part in re.split(r'(`[^`]*`)', l)[::2]:
            found += MD_LINK_RE.findall(part)
            wikis += [w.strip() for w in WIKI_RE.findall(part)]
    return found, wikis


def vault_root(summary: Path, folder: Path, given: Path | None) -> Path:
    if given:
        return given
    here = summary.resolve().parent
    found = next((d for d in (here, *here.parents) if (d / '.obsidian').is_dir()), None)
    return found or Path(os.path.commonpath([here, folder.resolve()]))


def chapters(body: list[str]) -> list[str]:
    """The "##" chapters of a file, outside fenced blocks."""
    heads, fenced = [], False
    for l in body:
        if l.lstrip().startswith(('```', '~~~')):
            fenced = not fenced
        elif not fenced and l.startswith('## '):
            heads.append(l[3:].strip())
    return heads


def fields(body: list[str]) -> tuple[re.Match | None, str | None, str | None, str | None]:
    first = next((l for l in body if l.strip()), '')
    return (HEADING_RE.match(first),
            next((m.group(1) for l in body if (m := STATUS_RE.match(l))), None),
            next((m.group(1) for l in body if (m := STARTED_RE.match(l))), None),
            next((m.group(1) for l in body if (m := WHEN_RE.match(l))), None))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--summary', required=True, type=Path, help='the chore-summary.md to check')
    ap.add_argument('--chores-dir', type=Path, help='the folder of the <name>.md files (default: the summary own folder)')
    ap.add_argument('--config', type=Path, help='the config.yaml whose agencies to look in (default: the one beside the folder of the summary, else the one in the current folder)')
    ap.add_argument('--vault', type=Path, help='the folder wikilinks resolve in (default: nearest ancestor with .obsidian)')
    a = ap.parse_args()
    folder = a.chores_dir or a.summary.parent
    config = a.config or a.summary.resolve().parent.parent / 'config.yaml'
    if not a.config and not config.is_file() and Path('config.yaml').is_file():
        config = Path('config.yaml')  # a summary outside the workspace, such as in the vault: run from the root
    try:
        lines, rows, after = read_summary(a.summary)
        if folder.exists() and not folder.is_dir():
            raise OSError(f'{folder} is not a folder')
        names = [] if not folder.exists() else sorted(p.name for p in folder.iterdir()
                       if p.name != a.summary.name and not p.name.startswith('.'))
        files = {m.group(1): (folder / n).read_text(encoding='utf-8-sig').split('\n')
                 for n in names if (m := FILE_RE.match(n))}
        agencies = {k: Path(os.path.expanduser(v)) for k, v in read_block(config, 'agencies').items()}
        groups = read_block(config, 'skillGroups')
    except (OSError, UnicodeDecodeError) as e:
        print(f'{a.summary}: cannot be read - {e}', file=sys.stderr)
        sys.exit(2)

    rep = Report()
    where = f'in {folder}' if folder.exists() else f'- {folder} does not exist, so it holds none'
    print(f'{a.summary}: {len(files)} chore files {where}, {len(rows)} table rows, {len(agencies)} agencies in {config}')

    # 1. files
    stray = [n for n in names if not FILE_RE.match(n)]
    rep.check(not stray, 'the folder holds only <name>.md files (and the summary), each name lowercase letters, digits and hyphens, starting with a letter',
              [f'not a <name>.md file: {n}' for n in stray])

    # 2. rows: (name, own?) for each well-formed row
    parsed: list[tuple[str, bool] | None] = []
    for r in rows:
        own, text = (OWN_RE.match(r[0]), TEXT_RE.match(r[0])) if r else (None, None)
        parsed.append((own.group(1), True) if own and len(r) == 6 else (text.group(1), False) if text and len(r) == 6 else None)
    bad = [f'row {k + 1}: {" | ".join(r)[:80]}' for k, (r, p) in enumerate(zip(rows, parsed)) if p is None]
    rep.check(not bad, 'every row has six cells and opens with [[<name>]], or with <name> as text for a chore of another agency', bad)
    good = [(r, p[0], p[1]) for r, p in zip(rows, parsed) if p is not None]

    # 3. own rows against the files
    own_rows = [n for _, n, own in good if own]
    problems = [f'no row for the file {n}.md' for n in files if n not in own_rows]
    problems += [f'[[{n}]] has no file in {folder}' for n in own_rows if n not in files]
    problems += [f'{n} is named as text, but it is a file of this workspace: write [[{n}]]' for _, n, own in good if not own and n in files]
    problems += [f'{n} has more than one row' for n in sorted({n for _, n, _ in good if [x for _, x, _ in good].count(n) > 1})]
    rep.check(not problems, "one [[<name>]] row per chore file, and no row of text names one", problems)

    # 4. chores of other agencies
    other_files: dict[str, list[str]] = {}
    problems, private = [], []
    for _, n, own in good:
        if own or n in files:
            continue
        hits = [root / 'chores' / f'{n}.md' for root in agencies.values() if (root / 'chores' / f'{n}.md').is_file()]
        if not hits:
            problems.append(f'{n}: no agency of {config} has chores/{n}.md' + ('' if agencies else ' - it sets no agencies'))
        elif len(hits) > 1:
            problems.append(f'{n}: more than one agency has it: {", ".join(map(str, hits))}')
        else:
            other_files[n] = hits[0].read_text(encoding='utf-8-sig').split('\n')
            if any(PRIVATE_RE.match(l) for l in other_files[n]):
                private.append(f'{n}: {hits[0]} is private - only its own agency does it')
    rep.check(not problems, "each row of text names a chore file that one agency of config.yaml has", problems)

    # 5. order
    keyed = [(r[1], n) for r, n, _ in good]
    want = sorted(keyed, key=lambda x: (x[0], [-ord(c) for c in x[1]]), reverse=True)
    rep.check(keyed == want, 'the rows are newest Started first, a tie by name',
              [f'rows:     {", ".join(n for _, n in keyed)}', f'expected: {", ".join(n for _, n in want)}'])

    heads, titles, missing, started, whens, icons, refs, secs, programs = ([] for _ in range(9))
    root = vault_root(a.summary, folder, a.vault)
    known = known_names(root)
    for r, n, own in good:
        body = files.get(n) if own or n in files else other_files.get(n)
        if not DATE_RE.match(r[1]):
            started.append(f'{n}: Started "{r[1]}" is not a date')
        if r[5] not in ICONS.values():
            icons.append(f'{n}: row {r[5]} - not one of {" ".join(ICONS.values())}')
        if body is None:
            continue
        hm, status, start, when = fields(body)
        if not hm or hm.group(1) != n or '|' in hm.group(2):
            heads.append(f'{n}.md opens with: {next((l for l in body if l.strip()), "")[:70]}')
        if hm and r[2] != hm.group(2):
            titles.append(f'{n}: row "{r[2][:40]}", heading "{hm.group(2)[:40]}"')
        if when is not None and r[3] != when:
            whens.append(f'{n}: row "{r[3][:40]}", When "{when[:40]}"')
        if n not in files:
            continue
        gone = [w for w, v in (('no Status line', status), ('no Started line with a date', start), ('no When line', when)) if v is None]
        if gone:
            missing.append(f'{n}: ' + ', '.join(gone))
        if start is not None and r[1] != start:
            started.append(f'{n}: row {r[1]}, file {start}')
        if status is not None and ICONS.get(status) != r[5]:
            icons.append(f'{n}: row {r[5]}, Status "{status}"' + ('' if status in ICONS else ' - not one of ' + '/'.join(ICONS)))
        if chapters(body) != CHAPTERS:
            secs.append(f'{n}: "##" chapters {chapters(body)}, expected {CHAPTERS}')
        for code in commands(body):
            for path in run_paths(code):
                g = GROUP_PATH_RE.match(path)
                if not g:
                    programs.append(f'{n}: {path} - write it as {{skillGroups.X}}/..., in a skill group')
                elif g.group(1) not in groups:
                    programs.append(f'{n}: {path} - config.yaml sets no skillGroups.{g.group(1)}')
        md_links, wikis = links_outside_code(body)
        for w in wikis:
            if w.split('/')[-1] not in known and w.split('/')[-1] + '.md' not in known:
                refs.append(f'{n}: [[{w[:70]}]]')
        for tg in md_links:
            if re.match(r'[A-Za-z][A-Za-z0-9+.-]*:|#|/', tg) or '<' in tg or '{' in tg:
                continue
            if not (folder / unquote(tg.split('#')[0])).exists():
                refs.append(f'{n}: {tg[:70]}')

    rep.check(not heads, 'each chore file opens with "# <name> - <title>", <name> its file name, and no "|" in the title', heads)
    rep.check(not titles, "each row's Title is its chore file's title", titles)
    rep.check(not missing, 'each chore file of this workspace has a Status line, a Started line with a date, and a When line', missing)
    rep.check(not started, "each row's Started is a date, and its file's for a chore of this workspace", started)
    rep.check(not whens, "each row's 何時要做 is its chore file's When line", whens)
    rep.check(not icons, "each row's icon is 🔁, ⏸️ or ⏹️, and its Status line's word for a chore of this workspace", icons)

    # 12. legend
    tail = next((l for l in lines[after:] if l.strip()), '')
    rep.check(tail.startswith(LEGEND), 'the legend of the icons follows the table', [f'found: {tail[:60]}'])

    rep.check(not refs, 'each wikilink and relative link in a chore file of this workspace lands on a file that exists', refs)
    rep.check(not secs, 'each chore file of this workspace has the numbered "##" chapters in order: ' + ', '.join(CHAPTERS), secs)

    # 15-16. run records
    runs, problems = read_runs(lines)
    row_names = [n for _, n, _ in good]
    started_of = {n: r[1] for r, n, _ in good}
    run_names = [n for n, _ in runs]
    problems += [f'### {n} names no row of the table' for n in run_names if n not in row_names]
    problems += [f'### {n} is there more than once' for n in sorted({n for n in run_names if run_names.count(n) > 1})]
    in_table = [n for n in run_names if n in row_names]
    if in_table != sorted(in_table, key=row_names.index):
        problems.append(f'not in the order of the table: {", ".join(in_table)}')
    newest: dict[str, str] = {}
    for n, days in runs:
        bad_days = [d for d in days if not DATE_RE.match(d)]
        for d in days:
            if DATE_RE.match(d):
                try:
                    date.fromisoformat(d)
                except ValueError:
                    bad_days.append(d)
        if bad_days:
            problems.append(f'{n}: not a real date: {", ".join(bad_days)}')
            continue
        if days != sorted(set(days), reverse=True):
            problems.append(f'{n}: not one per day, newest first: {", ".join(days)}')
        elif days and n in started_of and DATE_RE.match(started_of[n]) and days[-1] < started_of[n]:
            problems.append(f'{n}: run {days[-1]} comes before Started {started_of[n]}')
        if days:
            newest[n] = days[0]
    rep.check(not problems, f'"{RUNS}" has one "### <name>" per chore that was done, in the order of the table; its days are real, one per day, newest first, none before Started', problems)
    lasts = [f'{n}: row {r[4]}, newest run {newest.get(n, NONE)}' for r, n, _ in good if r[4] != newest.get(n, NONE)]
    rep.check(not lasts, "each row's 上次執行 is its newest run day, or — when it has none", lasts)

    rep.check(not programs, 'each command of a chore file of this workspace that runs a file names it as {skillGroups.X}/..., X a skill group of config.yaml', programs)
    rep.check(not private, 'no row of text names a private chore of another agency', private)

    print(f'\nverdict: {"PASS" if not rep.failed else "FAIL"} - {rep.passed} passed, {rep.failed} failed')
    sys.exit(1 if rep.failed else 0)


if __name__ == '__main__':
    main()
