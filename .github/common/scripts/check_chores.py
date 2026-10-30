#!/usr/bin/env python3
"""Check that a workspace's chore list agrees with itself: its summary table and its chore files.

A chore is work that comes back: it is done whenever its condition holds, again and again, so it is never
finished, only stopped. The workspace keeps one file per chore, and a summary of them (an Obsidian vault;
links between them are wikilinks):

  chore-summary.md     the opening paragraph, the table, the legend of its icons (any name), and the 空號 line
  Chore N.md           one chore: its heading, its three lines, its six chapters

A number is used once. A chore that moves to another workspace leaves its number behind as a gap, and no later
chore takes it: the summary lists the gaps on one line below the table, each number once, divided by 、 - a line
it leaves out while there are none:

  空號：3、5。

A chore file opens with its heading and its three lines:

  # Chore N - <title>

  **Status**：<使用中|暫停|停用>——<the detail>
  **Started**：<YYYY-MM-DD>，<why it was started>
  **When**：<when it is due, on one line>

Then the numbered chapters, in this order: "## 1. 目的", "## 2. 何時要做", "## 3. 怎麼做", "## 4. 驗證",
"## 5. 與其他 task、chore 的關係", "## 6. 執行紀錄" ("###" inside them is free; a chapter with nothing to
say holds "—"). The last one, the run log, holds one "### YYYY-MM-DD" section for each day the chore was
done, newest first, none before the day it was started - or "—" when it was never done.

The summary repeats each chore in a row of its table, newest first, with a legend for its icons beneath:

  | Chore | Started | Title | 何時要做 | 上次執行 | Status |
  |---|---|---|---|---|---|
  | [[Chore N]] | <YYYY-MM-DD> | <title> | <its When line> | <its newest run, or —> | <🔁|⏸️|⏹️> |

The table is read instead of the files, to see which chore is due; a row that disagrees with its file
misleads exactly there, and several sessions edit these files at once. What a program can compare, this
script compares:

  1. files       the folder holds only Chore N.md files (and the summary): each number from 1 to the largest has a
                 file or is on the 空號 line, never both; the line lists well-formed numbers, each once
  2. rows        one row per file, newest first, each with six cells and a [[Chore N]] link to its own file
  3. headings    each file opens with "# Chore N - <title>", N the one in its name, and no "|" in the title
  4. titles      each row's Title is its file's title
  5. lines       each file has its Status, Started and When lines, a date on Started
  6. started     each row's Started is its file's
  7. when        each row's 何時要做 is its file's When line
  8. icons       each row's icon is its Status line's word: 使用中 🔁, 暫停 ⏸️, 停用 ⏹️
  9. legend      the legend of the icons follows the table
  10. references each wikilink and relative Markdown link in a chore file lands on a file that exists - a
                 wikilink by file name anywhere in the vault (--vault, else the folder with .obsidian, else
                 the folder holding both the summary and the chores); in a git repository, among the vault's
                 files that git tracks or does not ignore, so a scan skips what .gitignore keeps out (a virtual
                 environment, a data cache), and a link into an ignored folder does not count
  11. chapters   each file has the numbered "##" chapters, in order, and its run sections are inside the last
  12. runs       the run sections are real dates, one per day, newest first, none before Started
  13. last run   each row's 上次執行 is its file's newest run section, or — when the file has none

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
FILE_RE = re.compile(r'^Chore (\d+)\.md$')
HEADING_RE = re.compile(r'^# Chore (\d+) - (.+?)\s*$')
LINK_RE = re.compile(r'^\[\[Chore (\d+)\]\]$')
STATUS_RE = re.compile(r'^\*\*Status\*\*：(.+?)——')
STARTED_RE = re.compile(r'^\*\*Started\*\*：(\d{4}-\d{2}-\d{2})')
WHEN_RE = re.compile(r'^\*\*When\*\*：(.+?)\s*$')
WIKI_RE = re.compile(r'!?\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]')
MD_LINK_RE = re.compile(r'\]\(([^)\s]+)\)')
DAY_RE = re.compile(r'^### (\d{4}-\d{2}-\d{2})\s*$')
NONE = '—'
ICONS = {'使用中': '🔁', '暫停': '⏸️', '停用': '⏹️'}
LEGEND = 'Status：🔁 使用中'
GAP_PREFIX = '空號：'
GAP_ITEM_RE = re.compile(r'^[1-9]\d*$')
CHAPTERS = ['1. 目的', '2. 何時要做', '3. 怎麼做', '4. 驗證', '5. 與其他 task、chore 的關係', '6. 執行紀錄']


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


def read_gaps(lines: list[str], after: int) -> tuple[list[int], list[str]]:
    """The numbers the 空號 line below the table lists, and what is wrong with the line."""
    found = [l.strip() for l in lines[after:] if l.strip().startswith(GAP_PREFIX)]
    if not found:
        return [], []
    problems = [] if len(found) == 1 else [f'{len(found)} 空號 lines, where one belongs']
    gaps: list[int] = []
    for x in (x.strip() for x in found[0][len(GAP_PREFIX):].rstrip('。').split('、')):
        if not GAP_ITEM_RE.match(x):
            problems.append(f'not a chore number on the 空號 line: "{x}"')
        elif int(x) in gaps:
            problems.append(f'on the 空號 line twice: {x}')
        else:
            gaps.append(int(x))
    return gaps, problems


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


def chapters(body: list[str]) -> tuple[list[tuple[int, str]], list[tuple[int, str]]]:
    """The "##" chapters and the "### YYYY-MM-DD" sections of a file, each with its line, outside fenced blocks."""
    heads, days, fenced = [], [], False
    for k, l in enumerate(body):
        if l.lstrip().startswith(('```', '~~~')):
            fenced = not fenced
        elif not fenced and l.startswith('## '):
            heads.append((k, l[3:].strip()))
        elif not fenced and (m := DAY_RE.match(l)):
            days.append((k, m.group(1)))
    return heads, days


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--summary', required=True, type=Path, help='the chore-summary.md to check')
    ap.add_argument('--chores-dir', type=Path, help='the folder of the Chore N.md files (default: the summary own folder)')
    ap.add_argument('--vault', type=Path, help='the folder wikilinks resolve in (default: nearest ancestor with .obsidian)')
    a = ap.parse_args()
    folder = a.chores_dir or a.summary.parent
    try:
        lines, rows, after = read_summary(a.summary)
        if not folder.is_dir():
            raise OSError(f'{folder} is not a folder')
        names = sorted(p.name for p in folder.iterdir()
                       if p.name != a.summary.name and not p.name.startswith('.'))
        files = {int(m.group(1)): (folder / n).read_text(encoding='utf-8-sig').split('\n')
                 for n in names if (m := FILE_RE.match(n))}
    except (OSError, UnicodeDecodeError) as e:
        print(f'{a.summary}: cannot be read - {e}', file=sys.stderr)
        sys.exit(2)

    rep = Report()
    order = sorted(files, reverse=True)
    print(f'{a.summary}: {len(files)} chore files in {folder}, {len(rows)} table rows')

    # 1. files, and the gaps the 空號 line lists
    stray = [n for n in names if not FILE_RE.match(n)]
    gaps, numbering = read_gaps(lines, after)
    numbering += [f'Chore {g} is on the 空號 line and has a file' for g in gaps if g in files]
    lost = [c for c in range(1, max(set(files) | set(gaps), default=0) + 1) if c not in files and c not in gaps]
    if lost:
        numbering.append(f'chores with no file, not on the 空號 line: {", ".join(map(str, lost))}')
    rep.check(not stray and not numbering,
              'the folder holds only Chore N.md files (and the summary); each number up to the largest has a file or is on the 空號 line, not both',
              [f'not a Chore N.md file: {n}' for n in stray] + numbering)

    # 2. rows
    linked = []
    for r in rows:
        m = LINK_RE.match(r[0]) if r else None
        linked.append(int(m.group(1)) if m and len(r) == 6 else None)
    bad = [f'row {k + 1}: {" | ".join(r)[:80]}' for k, (r, n) in enumerate(zip(rows, linked)) if n is None]
    rep.check(not bad, 'every row has six cells and opens with a [[Chore N]] link', bad)
    row_order = [n for n in linked if n is not None]
    rep.check(row_order == order, 'one row per file, newest first, each linking to its own file',
              [f'rows:  {", ".join(map(str, row_order))}', f'files: {", ".join(map(str, order))}'])

    by_number = {n: r for r, n in zip(rows, linked) if n is not None}
    heads, titles, missing, started, whens, icons, refs, secs, runs, lasts = ([] for _ in range(10))
    root = vault_root(a.summary, folder, a.vault)
    known = known_names(root)
    for n in order:
        body = files[n]
        first = next((l for l in body if l.strip()), '')
        hm = HEADING_RE.match(first)
        if not hm or int(hm.group(1)) != n or '|' in hm.group(2):
            heads.append(f'Chore {n}.md opens with: {first[:70]}')
        title = hm.group(2) if hm else None
        status = next((m.group(1) for l in body if (m := STATUS_RE.match(l))), None)
        start = next((m.group(1) for l in body if (m := STARTED_RE.match(l))), None)
        when = next((m.group(1) for l in body if (m := WHEN_RE.match(l))), None)
        gone = [w for w, v in (('no Status line', status), ('no Started line with a date', start), ('no When line', when)) if v is None]
        if gone:
            missing.append(f'Chore {n}: ' + ', '.join(gone))

        # 11-12. chapters and run sections
        h2, days = chapters(body)
        names2 = [h for _, h in h2]
        if names2 != CHAPTERS:
            secs.append(f'Chore {n}: "##" chapters {names2}, expected {CHAPTERS}')
        elif days and days[0][0] < h2[-1][0]:
            secs.append(f'Chore {n}: a run section comes before "## {CHAPTERS[-1]}"')
        found = [d for _, d in days]
        real = True
        for d in found:
            try:
                date.fromisoformat(d)
            except ValueError:
                real = False
                runs.append(f'Chore {n}: {d} is not a real date')
        if real and found:
            if found != sorted(set(found), reverse=True):
                runs.append(f'Chore {n}: not one per day, newest first: {", ".join(found)}')
            elif start is not None and found[-1] < start:
                runs.append(f'Chore {n}: run {found[-1]} comes before Started {start}')
        newest = found[0] if found and real else NONE

        # 10. references
        md_links, wikis = links_outside_code(body)
        for w in wikis:
            if w.split('/')[-1] not in known and w.split('/')[-1] + '.md' not in known:
                refs.append(f'Chore {n}: [[{w[:70]}]]')
        for tg in md_links:
            if re.match(r'[A-Za-z][A-Za-z0-9+.-]*:|#|/', tg) or '<' in tg or '{' in tg:
                continue
            if not (folder / unquote(tg.split('#')[0])).exists():
                refs.append(f'Chore {n}: {tg[:70]}')

        if n not in by_number:
            continue
        r = by_number[n]
        if title is not None and r[2] != title:
            titles.append(f'Chore {n}: row "{r[2][:40]}", heading "{title[:40]}"')
        if start is not None and r[1] != start:
            started.append(f'Chore {n}: row {r[1]}, file {start}')
        if when is not None and r[3] != when:
            whens.append(f'Chore {n}: row "{r[3][:40]}", When "{when[:40]}"')
        if status is not None and ICONS.get(status) != r[5]:
            icons.append(f'Chore {n}: row {r[5]}, Status "{status}"' + ('' if status in ICONS else ' - not one of ' + '/'.join(ICONS)))
        if r[4] != newest:
            lasts.append(f'Chore {n}: row {r[4]}, newest run section {newest}')

    rep.check(not heads, 'each file opens with "# Chore N - <title>", N the one in its name, and no "|" in the title', heads)
    rep.check(not titles, "each row's Title is its file's title", titles)
    rep.check(not missing, 'each file has a Status line, a Started line with a date, and a When line', missing)
    rep.check(not started, "each row's Started is its file's", started)
    rep.check(not whens, "each row's 何時要做 is its file's When line", whens)
    rep.check(not icons, "each row's icon is its Status line's word: 使用中 🔁, 暫停 ⏸️, 停用 ⏹️", icons)

    # 9. legend
    tail = next((l for l in lines[after:] if l.strip()), '')
    rep.check(tail.startswith(LEGEND), 'the legend of the icons follows the table', [f'found: {tail[:60]}'])

    rep.check(not refs, 'each wikilink and relative link in a chore file lands on a file that exists', refs)
    rep.check(not secs, 'each file has the numbered "##" chapters in order: ' + ', '.join(CHAPTERS) + '; run sections are inside the last', secs)
    rep.check(not runs, 'the run sections are real dates, one per day, newest first, none before Started', runs)
    rep.check(not lasts, "each row's 上次執行 is its file's newest run section, or — when it has none", lasts)

    print(f'\nverdict: {"PASS" if not rep.failed else "FAIL"} - {rep.passed} passed, {rep.failed} failed')
    sys.exit(1 if rep.failed else 0)


if __name__ == '__main__':
    main()
