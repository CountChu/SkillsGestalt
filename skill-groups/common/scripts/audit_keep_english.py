#!/usr/bin/env python3
"""Audit every 繁體中文 twin under the roots for the renderings that the keep-English list flags.

The chinese skill checks a twin against the keep-English list - check_parity.py --keep - when it writes
or updates that twin. A twin it does not touch is never checked again, so a term that the list adds later
stays translated there. This script checks every pair at once - each X.md with an X-tw.md beside it - and
finds each flagged rendering as check_parity.py --keep does: in the twin's prose, outside fenced blocks,
headings, inline code and link targets.

  - A rendering that the matching English line writes too - the same line when the two files have the same
    number of lines, else anywhere in the English file - is listed apart, as "the English writes it too":
    that line is about the rendering itself, as a row of a translation table is.
  - The rest are the findings, for the user to decide about.

  audit  --keep LIST --root DIR [--root DIR ...] --out FOLDER
      Write the full list to FOLDER/<YYYY-MM-DD>-<version>.txt, <version> being the list's Version line,
      and compare its findings with the newest earlier report in FOLDER: each one that is new, and each one
      that is gone, by twin, term and rendering, its line numbers aside.
  due    --keep LIST --out FOLDER [--baseline VERSION]
      Say whether an audit is due: the list's version is not the one the newest report in FOLDER was made
      against, or, with no report yet, not the baseline version. Exit 0 due, 1 not due.

It skips .git, node_modules, checkpoints and the keep-English list's own two files.
Exit status: 0 done, or due; 1 not due; 2 a file that cannot be read, or a list with no Version line.
Standard library only; it imports scan_md.py of the chinese skill.
"""
from __future__ import annotations

import argparse
import datetime
import io
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

CHINESE = Path(__file__).resolve().parents[1] / 'skills' / 'chinese' / 'scripts'
sys.path.insert(0, str(CHINESE))
from scan_md import fence_spans, keep_english, prose_lines  # noqa: E402

SKIP_DIRS = {'.git', 'node_modules', '.venv', 'venv', '__pycache__', 'checkpoints', '.obsidian'}
VERSION_RE = re.compile(r'^>\s*Version:\s*(\d{6})\s*$')
REPORT_RE = re.compile(r'^(\d{4}-\d{2}-\d{2})-(\d{6})\.txt$')
FINDING, TOO = 'finding', 'english too'


def version_of(path: Path) -> str:
    for line in io.open(path, encoding='utf-8-sig'):
        if m := VERSION_RE.match(line):
            return m.group(1)
    print(f'error: {path} has no "> Version: yymmdd" line', file=sys.stderr)
    sys.exit(2)


def pairs(roots: list[Path], keep: Path) -> list[tuple[Path, Path]]:
    own = {keep.resolve(), keep.with_name(keep.name[:-len('.md')] + '-tw.md').resolve()}
    found, seen = [], set()
    for root in roots:
        for folder, dirs, files in os.walk(root):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
            for f in sorted(files):
                if not f.endswith('-tw.md'):
                    continue
                tw = Path(folder) / f
                en = tw.with_name(f[:-len('-tw.md')] + '.md')
                if en.is_file() and tw.resolve() not in own and tw.resolve() not in seen:
                    seen.add(tw.resolve())
                    found.append((en, tw))
    return found


def audit_pair(en: Path, tw: Path, terms: list[tuple[str, list[str]]]) -> dict[tuple[str, str, str], list[int]]:
    """{(kind, term, rendering): [line numbers]} of the flagged renderings in one twin."""
    en_lines = io.open(en, encoding='utf-8-sig').read().splitlines()
    tw_lines = io.open(tw, encoding='utf-8-sig').read().splitlines()
    en_text = '\n'.join(en_lines)
    same_shape = len(en_lines) == len(tw_lines)
    prose = list(prose_lines(tw_lines, fence_spans(tw_lines)[1]))
    hits: dict[tuple[str, str, str], list[int]] = defaultdict(list)
    for term, flagged in terms:
        for rendering in flagged:
            for i, line in prose:
                if rendering not in line:
                    continue
                too = rendering in en_lines[i - 1] if same_shape else rendering in en_text
                hits[(TOO if too else FINDING, term, rendering)].append(i)
    return hits


def shown(path: Path) -> str:
    return os.path.relpath(path)


def read_report(path: Path) -> set[tuple[str, str, str]]:
    """The (twin, term, rendering) of each finding in an earlier report."""
    keys, section = set(), None
    for line in io.open(path, encoding='utf-8'):
        if line.startswith('== '):
            section = FINDING if line.startswith('== findings') else TOO
            continue
        parts = line.rstrip('\n').split('\t')
        if section == FINDING and len(parts) == 4:
            keys.add((parts[0], parts[1], parts[2]))
    return keys


def reports(folder: Path) -> list[Path]:
    return sorted((p for p in folder.glob('*.txt') if REPORT_RE.match(p.name)), key=lambda p: p.name) if folder.is_dir() else []


def audit(keep: Path, roots: list[Path], out: Path) -> None:
    version, terms = version_of(keep), keep_english(keep)
    now = datetime.datetime.now()
    rows: dict[str, list[tuple[str, str, str, list[int]]]] = {FINDING: [], TOO: []}
    found = pairs(roots, keep)
    for en, tw in found:
        try:
            hits = audit_pair(en, tw, terms)
        except (OSError, UnicodeDecodeError) as e:
            print(f'error: {tw}: {e}', file=sys.stderr)
            sys.exit(2)
        for (kind, term, rendering), lines in sorted(hits.items()):
            rows[kind].append((shown(tw), term, rendering, lines))
    earlier = reports(out)
    out.mkdir(parents=True, exist_ok=True)
    report = out / f'{now:%Y-%m-%d}-{version}.txt'
    with io.open(report, 'w', encoding='utf-8') as f:
        f.write(f'keep-English audit of {now:%Y-%m-%d %H:%M}, against the list of version {version}\n')
        f.write(f'roots: {", ".join(shown(r) for r in roots)}; pairs: {len(found)}\n')
        for kind, title in ((FINDING, 'findings'), (TOO, 'the English writes it too')):
            f.write(f'== {title}: {sum(len(r[3]) for r in rows[kind])} line(s) in {len({r[0] for r in rows[kind]})} twin(s)\n')
            for tw, term, rendering, lines in rows[kind]:
                f.write(f'{tw}\t{term}\t{rendering}\t{",".join(map(str, lines))}\n')
    findings = rows[FINDING]
    print(f'keep-English list {version}: {len(found)} pairs; findings: '
          f'{sum(len(r[3]) for r in findings)} line(s) in {len({r[0] for r in findings})} twin(s); '
          f'the English writes it too: {sum(len(r[3]) for r in rows[TOO])} line(s)')
    by_rendering: dict[tuple[str, str], list] = defaultdict(list)
    for tw, term, rendering, lines in findings:
        by_rendering[(term, rendering)].append((tw, lines))
    for (term, rendering), where in sorted(by_rendering.items(), key=lambda kv: -sum(len(l) for _, l in kv[1]))[:10]:
        print(f'  {rendering} for {term}: {sum(len(l) for _, l in where)} line(s) in {len(where)} twin(s)')
    previous = [p for p in earlier if p != report]
    if previous:
        before, now_keys = read_report(previous[-1]), {(r[0], r[1], r[2]) for r in findings}
        new, gone = sorted(now_keys - before), sorted(before - now_keys)
        print(f'compared with {shown(previous[-1])}: {len(new)} new, {len(gone)} gone')
        for tw, term, rendering in new:
            print(f'  [NEW] {tw}: {rendering} for {term}')
        for tw, term, rendering in gone:
            print(f'  [GONE] {tw}: {rendering} for {term}')
    else:
        print('no earlier report to compare with')
    print(f'report: {shown(report)}')


def due(keep: Path, out: Path, baseline: str | None) -> bool:
    version = version_of(keep)
    earlier = reports(out)
    last = REPORT_RE.match(earlier[-1].name).group(2) if earlier else baseline
    where = f'the last audit, {shown(earlier[-1])}' if earlier else f'the baseline {baseline}' if baseline else 'no audit yet'
    is_due = last != version
    print(f'{"due" if is_due else "not due"} - the list is {version}; {where}' + (f' is {last}' if earlier else ''))
    return is_due


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='command', required=True)
    a1 = sub.add_parser('audit', help='audit every twin under the roots')
    a1.add_argument('--keep', type=Path, required=True, help='the keep-English list, tw-keep-english.md')
    a1.add_argument('--root', type=Path, action='append', required=True, help='a folder to search')
    a1.add_argument('--out', type=Path, required=True, help='the folder of the reports')
    a2 = sub.add_parser('due', help='say whether an audit is due')
    a2.add_argument('--keep', type=Path, required=True, help='the keep-English list, tw-keep-english.md')
    a2.add_argument('--out', type=Path, required=True, help='the folder of the reports')
    a2.add_argument('--baseline', help='the version to compare with while there is no report yet')
    a = ap.parse_args()
    if a.command == 'audit':
        audit(a.keep, a.root, a.out)
    else:
        sys.exit(0 if due(a.keep, a.out, a.baseline) else 1)


if __name__ == '__main__':
    main()
