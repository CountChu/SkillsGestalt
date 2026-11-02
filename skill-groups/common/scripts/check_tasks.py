#!/usr/bin/env python3
"""Check that a workspace's task list agrees with itself: its summary table and its task files.

The workspace keeps work that outlives one session as one file per task, in the same folder as the
summary (an Obsidian vault folder; links between them are wikilinks):

  task-summary.md      the opening paragraph, the table, the legend of its icons (any name), and the 空號 line
  Task N.md            one task: its heading, its Status line, its Raised line, and what it says
  Task N.M.md          a sub task of Task N, numbered from 1 within it, in the same form as a task

A number is used once. A task or a sub task that moves to another workspace leaves its number behind as a
gap, and no later task takes it: the summary lists the gaps on one line below the table, each number once,
divided by 、 - a line it leaves out while there are none:

  空號：18.1、18.3、28。

A task file opens with its heading and its two lines:

  # Task N - <title>

  **Status**：<尚未開始|進行中|完成|取消>——<the detail>
  **Raised**：<YYYY-MM-DD>，<why it was raised>
  **Depends on**：<[[Task M]]、[[Task K]]，or —>

Then the numbered chapters, in this order: "## 1. 背景", "## 2. 現況", "## 3. 要做的", "## 4. 驗證",
"## 5. 與其他 task 的關係", "## 6. 知識", "## 7. 日誌" ("###" inside them is free; a chapter with nothing to say holds "—").
The log holds one "### YYYY-MM-DD" section per day, each recording what changed that day, newest first;
the oldest is the day the task was raised.

A task depends on another when it cannot be done before that one is done, or would be done for nothing.
The task file is where that is written; the table repeats it, each link followed by the icon its task has now:
  | [[Task N]] | ... | ... | ⬜ | [[Task M]] ✅、[[Task K]] 🔄 |

and the summary repeats each task in a row of its table, newest first, each task's sub tasks right below
it in ascending order (N.1, N.2, ...), with a legend for its icons beneath. A sub task's Task cell opens with
a tree line before its link: "└─ " for the last sub task of its task, "├─ " for the others.

  | Task | Raised | Title | Status | Depends on |
  |---|---|---|---|---|
  | [[Task N]] | <YYYY-MM-DD> | <title> | <⬜|🔄|✅|⊘> | <links, or —> |

The table is read instead of the files, so a row that disagrees with its file misleads exactly where
it is relied on; and several sessions edit these files at once, so nothing else notices when one of
them leaves them apart. What a program can compare, this script compares:

  1. files       the folder holds only Task N.md and Task N.M.md files (and the summary): each number from 1
                 to the largest, and each sub task's from 1 to the largest of its task, has a file or is on
                 the 空號 line, never both; the line lists well-formed numbers, each once; each sub task has its task
  2. rows        one row per file, newest first, each task's sub tasks right below it in ascending order,
                 each sub task's link after its tree line ("├─ ", or "└─ " for the last), a task's with none
  3. links       each row links to [[Task N]], its own file, and the file is there
  4. headings    each file opens with "# Task N - <title>", N the one in its name, and no "|" in the title
  5. titles      each row's Title is its file's title
  6. lines       each file has its Status line and its Raised line, a date on the latter
  7. dates       each row's Raised is its file's
  8. icons       each row's icon is its Status line's word: 尚未開始 ⬜, 進行中 🔄, 完成 ✅, 取消 ⊘
  9. legend      the legend of the icons follows the table
  10. references each wikilink and relative Markdown link in a task file lands on a file that exists - a
                 wikilink by file name anywhere in the vault (--vault, else the folder with .obsidian, else the folder holding both the summary and the tasks);
                 in a git repository, among the vault's files that git tracks or does not ignore, so a scan skips what
                 .gitignore keeps out (a virtual environment, a data cache), and a link into an ignored folder does not count
  11. depends     each file has a Depends on line of links to tasks, or —, and nothing else
  12. columns     each row's Depends on cell lists the tasks its file lists, in the same order
  13. targets     each task depended on exists, none depends on itself, and no chain of dependencies loops back
  14. icons       the icon after each link in a Depends on cell is the icon that task's own row has now
  15. day sections each file has "### YYYY-MM-DD" sections, one per day, a real date each, newest first,
                 and the oldest is the day on its Raised line
  16. chapters   each file has the numbered "##" chapters, in order, and its day sections are inside the last one (7. 日誌)

What it cannot judge - what a task says, how far its background was looked into, whether it is done -
stays with whoever edits the files.

Every check prints one line, [PASS] or [FAIL], each failure followed by what it found, and the run
ends with a verdict.

Exit status: 0 no check failed; 1 a check failed; 2 the command is malformed, a file cannot be read,
or the summary holds no task table.
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

HEADER = '| Task | Raised | Title | Status | Depends on |'
ID = r'\d+(?:\.\d+)?'
FILE_RE = re.compile(rf'^Task ({ID})\.md$')
HEADING_RE = re.compile(rf'^# Task ({ID}) - (.+?)\s*$')
LINK_RE = re.compile(rf'^((?:├─|└─) )?\[\[Task ({ID})\]\]$')
STATUS_RE = re.compile(r'^\*\*Status\*\*：(.+?)——')
RAISED_RE = re.compile(r'^\*\*Raised\*\*：(\d{4}-\d{2}-\d{2})')
DEPENDS_RE = re.compile(r'^\*\*Depends on\*\*：(.*?)\s*$')
FILE_DEP_RE = re.compile(rf'\[\[Task ({ID})\]\]')
ROW_DEP_RE = re.compile(rf'^\[\[Task ({ID})\]\] (⬜|🔄|✅|⊘)$')
WIKI_RE = re.compile(r'!?\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]')
DAY_RE = re.compile(r'^### (\d{4}-\d{2}-\d{2})\s*$')
NONE = '—'
MD_LINK_RE = re.compile(r'\]\(([^)\s]+)\)')
ICONS = {'尚未開始': '⬜', '進行中': '🔄', '完成': '✅', '取消': '⊘'}
LEGEND = 'Status：⬜ 尚未開始'
GAP_PREFIX = '空號：'
GAP_ITEM_RE = re.compile(r'^[1-9]\d*(?:\.[1-9]\d*)?$')


def parts(i: str) -> tuple[int, int]:
    """A task's number and, for a sub task, its number within the task (0 for a task itself)."""
    a, _, b = i.partition('.')
    return int(a), int(b or 0)


def table_order(ids) -> list[str]:
    """Tasks newest first, each followed by its own sub tasks in ascending order."""
    return sorted(ids, key=lambda i: (-parts(i)[0], parts(i)[1]))


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
    """The cells of a table row, the padding some rows carry removed."""
    return [c.strip() for c in row.strip().strip('|').split('|')]


def read_summary(path: Path) -> tuple[list[str], list[list[str]], int]:
    """The summary's lines, the table's rows, and the line after them."""
    lines = path.read_text(encoding='utf-8-sig').split('\n')
    try:
        top = next(i for i, l in enumerate(lines) if l.strip().replace(' ', '') == HEADER.replace(' ', ''))
    except StopIteration:
        print(f'{path}: no task table - a line "{HEADER}"', file=sys.stderr)
        sys.exit(2)
    rows, i = [], top + 2
    while i < len(lines) and lines[i].strip().startswith('|'):
        rows.append(cells(lines[i]))
        i += 1
    return lines, rows, i


def read_gaps(lines: list[str], after: int) -> tuple[list[str], list[str]]:
    """The numbers the 空號 line below the table lists, and what is wrong with the line."""
    found = [l.strip() for l in lines[after:] if l.strip().startswith(GAP_PREFIX)]
    if not found:
        return [], []
    problems = [] if len(found) == 1 else [f'{len(found)} 空號 lines, where one belongs']
    gaps: list[str] = []
    for x in (x.strip() for x in found[0][len(GAP_PREFIX):].rstrip('。').split('、')):
        if not GAP_ITEM_RE.match(x):
            problems.append(f'not a task number on the 空號 line: "{x}"')
        elif x in gaps:
            problems.append(f'on the 空號 line twice: {x}')
        else:
            gaps.append(x)
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
    """The folder wikilinks resolve in: --vault, else the nearest ancestor holding .obsidian, else the summary's folder."""
    if given:
        return given
    here = summary.resolve().parent
    found = next((d for d in (here, *here.parents) if (d / '.obsidian').is_dir()), None)
    return found or Path(os.path.commonpath([here, folder.resolve()]))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--summary', required=True, type=Path, help='the task-summary.md to check')
    ap.add_argument('--tasks-dir', type=Path, help='the folder of the Task N.md files (default: the summary own folder)')
    ap.add_argument('--vault', type=Path, help='the folder wikilinks resolve in (default: nearest ancestor with .obsidian)')
    a = ap.parse_args()
    folder = a.tasks_dir or a.summary.parent
    try:
        lines, rows, after = read_summary(a.summary)
        names = sorted(p.name for p in folder.iterdir() if p.name != a.summary.name and not p.name.startswith('.')) if folder.is_dir() else None
        if names is None:
            raise OSError(f'{folder} is not a folder')
        files: dict[str, list[str]] = {}
        for name in names:
            if m := FILE_RE.match(name):
                files[m.group(1)] = (folder / name).read_text(encoding='utf-8-sig').split('\n')
    except (OSError, UnicodeDecodeError) as e:
        print(f'{a.summary}: cannot be read - {e}', file=sys.stderr)
        sys.exit(2)

    rep = Report()
    order = table_order(files)
    print(f'{a.summary}: {len(files)} task files in {folder}, {len(rows)} table rows')

    # 1. files, and the gaps the 空號 line lists
    stray = [n for n in names if not FILE_RE.match(n)]
    gaps, numbering = read_gaps(lines, after)
    numbering += [f'Task {g} is on the 空號 line and has a file' for g in gaps if g in files]
    tops = {parts(i)[0] for i in files if parts(i)[1] == 0}
    top_gaps = {parts(g)[0] for g in gaps if parts(g)[1] == 0}
    lost = [t for t in range(1, max(tops | top_gaps, default=0) + 1) if t not in tops | top_gaps]
    if lost:
        numbering.append(f'tasks with no file, not on the 空號 line: {", ".join(map(str, lost))}')
    for t in sorted({parts(i)[0] for i in [*files, *gaps] if parts(i)[1]}):
        subs = {parts(i)[1] for i in files if parts(i)[0] == t and parts(i)[1]}
        sub_gaps = {parts(g)[1] for g in gaps if parts(g)[0] == t and parts(g)[1]}
        if subs and t not in tops:
            numbering.append(f'sub tasks of Task {t}, which has no file')
        elif sub_gaps and t not in tops | top_gaps:
            numbering.append(f'sub tasks of Task {t} on the 空號 line, a task with no file and not on the line')
        lost = [m for m in range(1, max(subs | sub_gaps) + 1) if m not in subs | sub_gaps]
        if lost:
            numbering.append(f'sub tasks of Task {t} with no file, not on the 空號 line: ' + ', '.join(f'{t}.{m}' for m in lost))
    rep.check(not stray and not numbering,
              'the folder holds only Task N.md and Task N.M.md files (and the summary); each number up to the largest has a file or is on the 空號 line, not both; each sub task has its task',
              [f'not a Task N.md file: {n}' for n in stray] + numbering)

    # 2. rows, matched to files by the number their link names
    linked = []
    for r in rows:
        m = LINK_RE.match(r[0]) if r else None
        linked.append((m.group(2), f'[[Task {m.group(2)}]]', m.group(1) or '') if m and len(r) == 5 else None)
    bad_rows = [f'row {k + 1}: {" | ".join(r)[:80]}' for k, (r, lk) in enumerate(zip(rows, linked)) if lk is None]
    rep.check(not bad_rows, 'every row has five cells and opens with a [[Task N]] link, a sub task\'s after its tree line', bad_rows)
    row_order = [lk[0] for lk in linked if lk]
    rep.check(row_order == order, "one row per file, newest first, each task's sub tasks right below it in ascending order",
              [f'rows:  {", ".join(map(str, row_order))}', f'files: {", ".join(map(str, order))}'])

    last_sub = {}
    for i in files:
        t, m = parts(i)
        if m:
            last_sub[t] = max(last_sub.get(t, 0), m)
    lines_off = []
    for lk in linked:
        if not lk:
            continue
        t, m = parts(lk[0])
        want = '' if not m else ('└─ ' if m == last_sub.get(t) else '├─ ')
        if lk[2] != want:
            lines_off.append(f'Task {lk[0]}: "{lk[2].strip() or "no line"}" where "{want.strip() or "no line"}" belongs')
    rep.check(not lines_off, 'each sub task row has its tree line, "└─" for the last of its task and "├─" before it; a task row has none', lines_off)

    by_number = {lk[0]: (r, lk[1]) for r, lk in zip(rows, linked) if lk}
    links, heads, titles, missing, dates, icons = [], [], [], [], [], []
    for n in order:
        body = files[n]
        first = next((l for l in body if l.strip()), '')
        hm = HEADING_RE.match(first)
        if not hm or hm.group(1) != n or '|' in hm.group(2):
            heads.append(f'Task {n}.md opens with: {first[:70]}')
        title = hm.group(2) if hm else None
        status = next((m.group(1) for l in body if (m := STATUS_RE.match(l))), None)
        raised = next((m.group(1) for l in body if (m := RAISED_RE.match(l))), None)
        if status is None or raised is None:
            missing.append(f'Task {n}: ' + ', '.join(w for w, v in (('no Status line', status), ('no Raised line with a date', raised)) if v is None))
        if n not in by_number:
            continue
        r, target = by_number[n]
        if target != f'[[Task {n}]]':
            links.append(f'Task {n}: links to {target[:60]}')
        if title is not None and r[2] != title:
            titles.append(f'Task {n}: row "{r[2][:40]}", heading "{title[:40]}"')
        if raised is not None and r[1] != raised:
            dates.append(f'Task {n}: row {r[1]}, file {raised}')
        if status is not None and ICONS.get(status) != r[3]:
            icons.append(f'Task {n}: row {r[3]}, Status "{status}"' + ('' if status in ICONS else ' - not one of ' + '/'.join(ICONS)))

    rep.check(not links, 'each row links to [[Task N]], its own file, and the file is there', links)
    rep.check(not heads, 'each file opens with "# Task N - <title>", N the one in its name, and no "|" in the title', heads)
    rep.check(not titles, "each row's Title is its file's title", titles)
    rep.check(not missing, 'each file has a Status line and a Raised line with a date', missing)
    rep.check(not dates, "each row's Raised is its file's", dates)
    rep.check(not icons, "each row's icon is its Status line's word: 尚未開始 ⬜, 進行中 🔄, 完成 ✅, 取消 ⊘", icons)

    # 9. legend
    tail = next((l for l in lines[after:] if l.strip()), '')
    rep.check(tail.startswith(LEGEND), 'the legend of the icons follows the table', [f'found: {tail[:60]}'])

    # 10. references
    broken = []
    root = vault_root(a.summary, folder, a.vault)
    known = known_names(root)
    for n in order:
        md_links, wikis = links_outside_code(files[n])
        for w in wikis:
            if w.split('/')[-1] not in known and w.split('/')[-1] + '.md' not in known:
                broken.append(f'Task {n}: [[{w[:70]}]]')
        for tg in md_links:
            if re.match(r'[A-Za-z][A-Za-z0-9+.-]*:|#|/', tg) or '<' in tg or '{' in tg:
                continue
            if not (folder / unquote(tg.split('#')[0])).exists():
                broken.append(f'Task {n}: {tg[:70]}')
    rep.check(not broken, 'each wikilink and relative link in a task file lands on a file that exists', broken)

    # 11-14. dependencies: what the files say, what the rows repeat, where they point, how current the icons are
    in_file: dict[str, list[str] | None] = {}
    malformed, cols, targets, stale = [], [], [], []
    for n in order:
        val = next((m.group(1) for l in files[n] if (m := DEPENDS_RE.match(l))), None)
        if val is None:
            malformed.append(f'Task {n}: no Depends on line')
            in_file[n] = None
        elif val == NONE:
            in_file[n] = []
        else:
            found = FILE_DEP_RE.findall(val)
            rest = FILE_DEP_RE.sub('', val).replace('、', '').strip()
            if not found or rest:
                malformed.append(f'Task {n}: {val[:70]}')
                in_file[n] = None
            else:
                in_file[n] = list(found)
    for n in order:
        if n not in by_number:
            continue
        cell = by_number[n][0][4]
        row_deps: list[str] = []
        shown: list[str] = []
        if cell != NONE:
            ms = [ROW_DEP_RE.match(x.strip()) for x in cell.split('、')]
            if not all(ms):
                cols.append(f'Task {n}: the cell reads "{cell[:70]}"')
                continue
            row_deps = [m.group(1) for m in ms]
            shown = [m.group(2) for m in ms]
        if in_file[n] is not None and in_file[n] != row_deps:
            cols.append(f'Task {n}: row {row_deps or NONE}, file {in_file[n] or NONE}')
        for d, icon in zip(row_deps, shown):
            now = by_number[d][0][3] if d in by_number else None
            if now is not None and icon != now:
                stale.append(f'Task {n}: shows Task {d} as {icon}, which is now {now}')
    for n, deps in in_file.items():
        for d in deps or []:
            if d == n:
                targets.append(f'Task {n}: depends on itself')
            elif d not in files:
                targets.append(f'Task {n}: Task {d} has no file')
    graph = {n: [d for d in deps or [] if d in files and d != n] for n, deps in in_file.items()}
    state: dict[str, int] = {}

    def visit(n: str, path: list[str]) -> None:
        state[n] = 1
        for d in graph.get(n, []):
            if state.get(d) == 1:
                targets.append('a loop: ' + ' -> '.join(f'Task {x}' for x in path[path.index(d):] + [d]))
            elif d not in state:
                visit(d, path + [d])
        state[n] = 2

    for n in order:
        if n not in state:
            visit(n, [n])

    rep.check(not malformed, 'each file has a Depends on line of links to tasks, or —, and nothing else', malformed)
    rep.check(not cols, "each row's Depends on cell lists the tasks its file lists, in the same order", cols)
    rep.check(not targets, 'each task depended on exists, none depends on itself, and no chain of dependencies loops back', targets)
    rep.check(not stale, "the icon after each link in a Depends on cell is that task's own icon now", stale)

    # 15. day sections
    days = []
    for n in order:
        found, fenced = [], False
        for l in files[n]:
            if l.lstrip().startswith(('```', '~~~')):
                fenced = not fenced
            elif not fenced and (m := DAY_RE.match(l)):
                found.append(m.group(1))
        raised = next((m.group(1) for l in files[n] if (m := RAISED_RE.match(l))), None)
        real = True
        for d in found:
            try:
                date.fromisoformat(d)
            except ValueError:
                real = False
                days.append(f'Task {n}: {d} is not a real date')
        if not found:
            days.append(f'Task {n}: no "### YYYY-MM-DD" section')
        elif real:
            if found != sorted(set(found), reverse=True):
                days.append(f'Task {n}: not one per day, newest first: {", ".join(found)}')
            elif raised is not None and found[-1] != raised:
                days.append(f'Task {n}: oldest section {found[-1]}, Raised {raised}')
    rep.check(not days, 'each file has one "### YYYY-MM-DD" section per day, newest first, the oldest being its Raised day', days)

    # 16. numbered chapters
    FIXED = ['1. 背景', '2. 現況', '3. 要做的', '4. 驗證', '5. 與其他 task 的關係', '6. 知識', '7. 日誌']
    secs = []
    for n in order:
        heads2, first_day, fenced = [], None, False
        for k, l in enumerate(files[n]):
            if l.lstrip().startswith(('```', '~~~')):
                fenced = not fenced
            elif not fenced and l.startswith('## '):
                heads2.append((k, l[3:].strip()))
            elif not fenced and first_day is None and DAY_RE.match(l):
                first_day = k
        names2 = [h for _, h in heads2]
        if names2 != FIXED:
            secs.append(f'Task {n}: "##" chapters {names2}, expected {FIXED}')
        elif first_day is not None and first_day < heads2[-1][0]:
            secs.append(f'Task {n}: a day section comes before "## {names2[-1]}"')
    rep.check(not secs, 'each file has the numbered "##" chapters in order: ' + ', '.join(FIXED) + '; day sections are inside the last', secs)

    print(f'\nverdict: {"PASS" if not rep.failed else "FAIL"} - {rep.passed} passed, {rep.failed} failed')
    sys.exit(1 if rep.failed else 0)


if __name__ == '__main__':
    main()
