#!/usr/bin/env python3
"""The Dependency Scanner: every fact a program can find about the dependencies Markdown files
declare in their header quote, as one JSON for check-md-deps to judge.

For each target file - a file named on the command line, or every .md under a directory named
there - it reports:

  dependencies  each line of the header quote: its link, whether it is `cited`, the date and the
                fingerprint it records, the file the link resolves to, the fingerprint now, and a
                verdict - UNCHANGED, CHANGED, NO_RECORD, NOTHING_CITED, MISSING or UNRESOLVED. A
                `cited` dependency also names the sections its fingerprint covers.
  problems      every format problem: a line opening the head with a link that is not read as a
                dependency (malformed), a dependency line outside the header quote (misplaced), and
                one document declared twice (duplicate).
  changes       for a CHANGED dependency whose document is in git: the commits since the date it
                was confirmed; the baseline - the newest commit whose content has the recorded
                fingerprint, or failing that the last commit on or before that date, marked
                approximate; and the diff of the fingerprinted text from the baseline to now.
  twin          for a target file with a TW twin beside it - <name>-tw.md - whether the twin has
                kept up with it: UNCHANGED, INCREMENTAL - the file changed since the commit that last
                changed the twin, and the change set says what to translate again - FULL - no
                baseline the twin can be updated from, and why - or UNCHECKED when the comparison
                could not run; with the baseline and the change set. A target file that is itself a
                twin is not checked for one.

The header quote, the fingerprint and the verdicts are those of the shared depends_on.py, the
Dependency Checker, which this script loads; a twin's verdict is that of the chinese skill's
diff_md.py, the Twin Differ, which it runs as a command. It adds only what a report needs beside
them, and writes nothing.

Usage:
  python scan_md_deps.py <file-or-directory>... [--config config.yaml] [--root VAULT]

Exit status: 0 nothing found - every dependency and every twin UNCHANGED, and no problem;
1 something found; 2 the command is malformed, or a target cannot be read.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

SHARED = Path(__file__).resolve().parents[3] / 'scripts'
sys.path.insert(0, str(SHARED))
try:
    import depends_on as dep
except ImportError as e:
    print(f'cannot load the shared depends_on.py from {SHARED}: {e}', file=sys.stderr)
    sys.exit(2)


HEAD_LIMIT = 40   # how far under the frontmatter a dependency line is looked for
LOG_LIMIT = 100   # how many commits of a document are searched for the baseline
DIFF_LIMIT = 200  # how many lines of one dependency's diff are kept
CHANGE_LIMIT = 80  # how many lines of one twin's change set are kept
TWIN_DIFFER = Path(__file__).resolve().parents[2] / 'chinese' / 'scripts' / 'diff_md.py'
TWIN_VERDICTS = ('UNCHANGED', 'INCREMENTAL', 'FULL')
# A quote line that opens with a link - the shape of a dependency line.
LINK_START_RE = re.compile(r'^>\s*(\[\[|\[[^\]]*\]\()')


def targets(paths: list[Path]) -> list[Path]:
    out = []
    for p in paths:
        if p.is_dir():
            out += [f for f in sorted(p.rglob('*.md')) if not set(f.parts) & dep.SKIP_DIRS]
        elif p.is_file():
            out.append(p)
        else:
            raise dep.Fault(f'no such file or directory: {p}')
    return out


def head(lines: list[str]) -> range:
    """The lines a dependency line may be found on: under the frontmatter, before the first heading
    below the title, HEAD_LIMIT lines at most."""
    start = dep.body_start(lines)
    stop = min(len(lines), start + HEAD_LIMIT)
    stop = next((i for i in range(start, stop) if re.match(r'^#{2,}\s', lines[i])), stop)
    return range(start, stop)


def git(args: list[str], cwd: Path) -> str | None:
    try:
        r = subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True,
                           encoding='utf-8', errors='replace')
    except OSError:
        return None
    return r.stdout if r.returncode == 0 else None


def changes(path: Path, e: dep.Entry, cites: set | None) -> dict:
    """What changed in a CHANGED dependency's document since the date it was confirmed."""
    top = git(['rev-parse', '--show-toplevel'], path.resolve().parent)
    if top is None:
        return {'git': False}
    top = Path(top.strip())
    rel = path.resolve().relative_to(top.resolve()).as_posix()
    log = git(['log', '--follow', f'-n{LOG_LIMIT}', '--format=%x00%H%x09%ad%x09%s', '--date=short',
               '--name-only', '--', rel], top) or ''
    commits = []
    for chunk in log.split('\x00')[1:]:
        rows = [r for r in chunk.split('\n') if r.strip()]
        h, d, s = (rows[0].split('\t', 2) + ['', ''])[:3]
        commits.append({'commit': h, 'date': d, 'subject': s, 'path': rows[1] if len(rows) > 1 else rel})

    def text_at(c: dict) -> str | None:
        content = git(['show', f"{c['commit']}:{c['path']}"], top)
        return None if content is None else dep.scope_text(dep.split_text(content), cites)

    baseline, before = None, None
    for c in commits:
        text = text_at(c)
        if text is not None and dep.digest(text) == e.sha:
            baseline = (c, True, text)
            break
    if baseline is None:
        c = next((c for c in commits if c['date'] <= (e.date or '')), None)
        text = text_at(c) if c else None
        if text is not None:
            baseline = (c, False, text)
    out = {'git': True,
           'commitsSince': [{k: c[k][:8] if k == 'commit' else c[k] for k in ('commit', 'date', 'subject')}
                            for c in commits if c['date'] >= (e.date or '')]}
    if baseline is None:
        out['baseline'] = None
        return out
    c, exact, before = baseline
    now = dep.scope_text(dep.read_lines(path), cites) or ''
    diff = list(difflib.unified_diff(before.split('\n'), now.split('\n'), lineterm='', n=2,
                                     fromfile=f"{rel} @ {c['commit'][:8]}", tofile=f'{rel} (now)'))
    out['baseline'] = {'commit': c['commit'][:8], 'date': c['date'], 'exact': exact}
    out['diff'] = diff[:DIFF_LIMIT]
    if len(diff) > DIFF_LIMIT:
        out['diffTruncated'] = len(diff)
    if not diff:
        out['note'] = ('the fingerprinted text is the same as at the baseline: the sections the target '
                       'file cites have changed, or the baseline is not the content it was confirmed against')
    return out


def twin(owner: Path) -> dict | None:
    """Whether the TW twin beside a target file has kept up with it, as the Twin Differ reads it
    from git: its verdict, its baseline, and the change set it prints."""
    if owner.stem.endswith('-tw'):
        return None
    tw = owner.with_name(owner.stem + '-tw' + owner.suffix)
    if not tw.is_file():
        return None
    out: dict = {'file': str(tw)}
    if not TWIN_DIFFER.is_file():
        out.update(verdict='UNCHECKED', why=f'the Twin Differ is not at {TWIN_DIFFER}')
        return out
    try:
        r = subprocess.run([sys.executable, str(TWIN_DIFFER), '--en', str(owner), '--tw', str(tw)],
                           capture_output=True, text=True, encoding='utf-8', errors='replace')
    except OSError as e:
        out.update(verdict='UNCHECKED', why=str(e))
        return out
    lines = r.stdout.splitlines()
    verdict = next((l.split(':', 1)[1].strip() for l in reversed(lines) if l.startswith('verdict:')), None)
    if r.returncode != 0 or verdict not in TWIN_VERDICTS:
        out.update(verdict='UNCHECKED', why=(r.stderr.strip() or r.stdout.strip() or 'no verdict')[-400:])
        return out
    out['verdict'] = verdict
    base = next((l.split(':', 1)[1].strip() for l in lines if l.startswith('baseline:')), '')
    if base.startswith('none - '):
        out['baseline'], out['why'] = None, base[len('none - '):]
    else:
        out['baseline'] = base
    if '-- change set --' in lines:
        k = lines.index('-- change set --')
        change = [l for l in lines[k + 1:] if l.strip() and not l.startswith('verdict:')]
        out['changeSet'] = change[:CHANGE_LIMIT]
        if len(change) > CHANGE_LIMIT:
            out['changeSetTruncated'] = len(change)
    return out


def scan(owner: Path, config: dict | None, root: Path | None) -> dict:
    lines = dep.read_lines(owner)
    quote = dep.header(lines)
    report = {'file': str(owner), 'headerQuote': [i + 1 for i in quote], 'dependencies': [], 'problems': []}
    found = []
    for i in quote:
        try:
            found.append(dep.parse_entry(owner, lines, i))
        except dep.Fault as f:
            report['problems'].append({'line': i + 1, 'text': lines[i].strip(), 'kind': 'malformed',
                                       'why': str(f).split(': ', 1)[-1]})
    for i in head(lines):
        if i in quote or not LINK_START_RE.match(lines[i]):
            continue
        if dep.ENTRY_RE.match(lines[i]):
            why = ('a dependency line counts only in the header quote: the first run of them under the '
                   'frontmatter, the title or a twin\'s pairing line, with no blank line inside the run')
            report['problems'].append({'line': i + 1, 'text': lines[i].strip(), 'kind': 'misplaced', 'why': why})
        else:
            report['problems'].append({'line': i + 1, 'text': lines[i].strip(), 'kind': 'malformed',
                                       'why': 'a quote line opening with a link is a dependency only when '
                                              'nothing but its record follows the link'})
    seen: dict[tuple[str, str], int] = {}
    for e in found:
        key = (e.kind, e.target)
        if key in seen:
            report['problems'].append({'line': e.line + 1, 'text': lines[e.line].strip(), 'kind': 'duplicate',
                                       'why': f'the same document is declared on line {seen[key]} too'})
        seen.setdefault(key, e.line + 1)
    cites = dep.citations(lines)
    for e in found:
        d = {'line': e.line + 1, 'text': lines[e.line].strip(), 'link': e.link, 'cited': e.cited,
             'date': e.date, 'fingerprint': e.sha}
        report['dependencies'].append(d)
        try:
            path = dep.resolve(e, owner, config, root)
        except dep.Fault as f:
            d.update(verdict='UNRESOLVED', why=str(f))
            continue
        if path is None:
            d.update(verdict='MISSING', why='the link names no file')
            continue
        scope = cites if e.cited else None
        now = dep.fingerprint(path, scope)
        d.update(resolved=str(path), now=now)
        if e.cited:
            d['sections'] = [w for w, _ in dep.cited_sections(dep.read_lines(path), cites)]
        if now is None:
            d['verdict'] = 'NOTHING_CITED'
        elif e.sha is None:
            d['verdict'] = 'NO_RECORD'
        elif e.sha == now:
            d['verdict'] = 'UNCHANGED'
        else:
            d['verdict'] = 'CHANGED'
            d['changes'] = changes(path, e, scope)
    report['twin'] = twin(owner)
    return report


def main() -> None:
    ap = argparse.ArgumentParser(description='Scan the dependencies Markdown files declare in their header quote.')
    ap.add_argument('paths', nargs='+', type=Path, help='a Markdown file, or a directory whose .md files are scanned')
    ap.add_argument('--config', type=Path, help='config.yaml, for a link whose path names one of its values')
    ap.add_argument('--root', type=Path, help='the vault a [[Name]] link is found under')
    a = ap.parse_args()
    try:
        config = dep.load_config(a.config) if a.config else None
        files = [scan(f, config, a.root) for f in targets(a.paths)]
    except dep.Fault as e:
        print(f'error: {e}', file=sys.stderr)
        sys.exit(2)
    named = {p.resolve() for p in a.paths if p.is_file()}
    shown = [f for f in files if f['headerQuote'] or f['problems'] or f['twin'] or Path(f['file']).resolve() in named]
    verdicts: dict[str, int] = {}
    twins: dict[str, int] = {}
    for f in files:
        for d in f['dependencies']:
            verdicts[d['verdict']] = verdicts.get(d['verdict'], 0) + 1
        if f['twin']:
            twins[f['twin']['verdict']] = twins.get(f['twin']['verdict'], 0) + 1
    problems = sum(len(f['problems']) for f in files)
    summary = {'files': len(files), 'filesWithoutDependencies': len(files) - len(shown) +
               sum(1 for f in shown if not f['dependencies']), 'verdicts': verdicts, 'problems': problems,
               'twins': twins}
    print(json.dumps({'summary': summary, 'files': shown}, ensure_ascii=False, indent=1))
    clean = problems == 0 and set(verdicts) <= {'UNCHANGED'} and set(twins) <= {'UNCHANGED'}
    sys.exit(0 if clean else 1)


if __name__ == '__main__':
    main()
