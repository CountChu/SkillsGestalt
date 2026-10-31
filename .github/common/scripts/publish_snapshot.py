#!/usr/bin/env python3
"""Make a release of this workspace for its public repository: a snapshot of the work branch, scanned before it leaves.

It serves the private chore publish-github of SkillsGestalt and no other agency: the branch main,
the remote origin, the keyword file, the paths it leaves out and the subject of a snapshot are
SkillsGestalt's, written here as they are. It lives in the common skill group only because a chore has no
program of its own. Run it from the root of SkillsGestalt.

The work branch is the branch that --work names, by default the branch that is checked out: m1 in the
workspace, or a different branch in a different clone. It cannot be `main`. Below, WORK stands for it.

The public repository carries no history of the work branch. Each release is one commit on the
local branch `main`, whose tree is the tree of WORK with the private paths taken out; only `main` is pushed,
to `main` of the remote `origin`. After a release WORK starts again from it: the old history of WORK is kept
in the tag archive/WORK-<yymmdd> of the day of the release, and WORK becomes one commit on the release that
puts back the private paths, so `git diff main WORK` shows only them and what is not published yet. Nothing here switches a
branch or touches the working tree, so other sessions can go on working on WORK while a release is made.

  check     build the tree of the release, scan it, and list what changed since the last release.
            It writes nothing. Exit 0 when the scan finds nothing, 1 when it finds something.
  publish   after a person has read what `check` printed: build the same tree again, scan it again,
            make the snapshot commit on `main`, push it (unless --no-push), and start WORK again from it.
            Give it the work, the source and the tree that `check` printed, and a summary of the changes.

The message of a snapshot commit is `SkillsGestalt yyyy-mm-dd`, then the summary that --summary or --summary-file gives,
then the work branch and the commit that the snapshot comes from. `check` lists the commits of WORK since
the last release, to write the summary from.

The scan looks at the text of every file of the tree for:

  - an email address, except the made-up and no-reply ones (EMAIL_ALLOWED)
  - a private IP address (10.x.x.x, 172.16-31.x.x, 192.168.x.x)
  - an Azure DevOps organization: a host under visualstudio.com, or a path under dev.azure.com,
    except the public documentation and the made-up contoso examples (ADO_ALLOWED)
  - the home directory of a user (/Users/<name>/, /home/<name>/, C:\\Users\\<name>)
  - a token or a private key
  - each word of the keyword file, which is not in git: the names of the organization, projects and
    products that must not be published are themselves private, so they are kept only on this machine.
    Without the file the scan does not run.

It also checks that no private path is in the tree: checkpoints/, the paths of EXCLUDED, the root
config.yaml, a *.mermaid.html preview, a PDF.

Exit status: 0 no finding; 1 a finding; 2 the command is malformed, git fails, the keyword file is
missing, or the tree changed between `check` and `publish`.
"""
from __future__ import annotations

import argparse
import datetime
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

EXCLUDED = ['external', '.github/external']
PRIVATE_PATH = re.compile(r'^(checkpoints/|external/|\.github/external/|config\.yaml$)|\.mermaid\.html$|\.pdf$', re.I)
BRANCH = 'main'
REMOTE, REMOTE_BRANCH = 'origin', 'main'
KEYWORDS = 'publish-keywords.local.txt'
# The commit that starts the work branch again after a release: it is not a change, so it is not in the list of commits.
RESTART = re.compile(r'^chore publish-github: \S+ starts again from ')

# The last label of the domain is letters, so a package version such as mermaid@11.4.1 is not taken for one.
EMAIL = re.compile(r'[A-Za-z0-9._%+-]+@((?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,})(?![A-Za-z0-9.-])')
EMAIL_ALLOWED = re.compile(r'^(example\.(com|org|net)|users\.noreply\.github\.com|github\.com)$', re.I)
PRIVATE_IP = re.compile(r'(?<![\d.])(10\.\d{1,3}\.\d{1,3}\.\d{1,3}|172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3})(?![\d.])')
ADO = re.compile(r'([A-Za-z0-9-]+\.visualstudio\.com|dev\.azure\.com/[A-Za-z0-9_.-]+)', re.I)
ADO_ALLOWED = re.compile(r'^(code\.visualstudio\.com|dev\.azure\.com/contoso)$', re.I)
HOME = re.compile(r'(/Users/|/home/|[A-Za-z]:\\Users\\)([A-Za-z0-9._-]+)')
SECRET = re.compile(r'gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|xox[baprs]-[A-Za-z0-9-]{10,}')


def git(*args: str, env: dict | None = None, data: bytes | None = None) -> str:
    r = subprocess.run(['git', *args], capture_output=True, input=data, env=env)
    if r.returncode != 0:
        print(f'git {" ".join(args)}: {r.stderr.decode(errors="replace").strip()}', file=sys.stderr)
        sys.exit(2)
    return r.stdout.decode('utf-8', errors='replace')


def build_tree(source: str) -> str:
    """The tree of `source` without the EXCLUDED paths, written through an index of its own."""
    with tempfile.TemporaryDirectory() as d:
        env = {**os.environ, 'GIT_INDEX_FILE': str(Path(d) / 'index')}
        git('read-tree', source, env=env)
        git('rm', '-r', '--cached', '--quiet', '--ignore-unmatch', '--', *EXCLUDED, env=env)
        return git('write-tree', env=env).strip()


def read_keywords(path: Path) -> list[str]:
    if not path.is_file():
        print(f'{path}: no keyword file - write the private names to scan for, one on each line, '
              f'and keep the file out of git', file=sys.stderr)
        sys.exit(2)
    words = [l.strip() for l in path.read_text(encoding='utf-8').splitlines()]
    return [w for w in words if w and not w.startswith('#')]


def blobs(tree: str) -> list[tuple[str, str]]:
    """Each file of the tree: its path and its text, binary files left out."""
    out = []
    entries = [l.split('\t', 1) for l in git('ls-tree', '-r', '-z', tree).split('\0') if l]
    shas = [(e[0].split()[2], e[1]) for e in entries if e[0].split()[1] == 'blob']
    if not shas:
        return out
    raw = subprocess.run(['git', 'cat-file', '--batch'], input=''.join(s + '\n' for s, _ in shas).encode(),
                         capture_output=True).stdout
    pos = 0
    for sha, path in shas:
        header_end = raw.index(b'\n', pos)
        size = int(raw[pos:header_end].split()[2])
        body = raw[header_end + 1:header_end + 1 + size]
        pos = header_end + 1 + size + 1
        if b'\0' not in body:
            out.append((path, body.decode('utf-8', errors='replace')))
    return out


def scan(tree: str, keywords: list[str]) -> list[str]:
    """Each finding, as 'path:line: kind: text'."""
    findings = []
    paths = [l for l in git('ls-tree', '-r', '--name-only', '-z', tree).split('\0') if l]
    findings += [f'{p}: a private path in the tree' for p in paths if PRIVATE_PATH.search(p)]
    kw = re.compile('|'.join(re.escape(k) for k in keywords), re.I) if keywords else None
    for path, text in blobs(tree):
        for n, line in enumerate(text.split('\n'), 1):
            hits = []
            hits += [('email', m.group(0)) for m in EMAIL.finditer(line) if not EMAIL_ALLOWED.match(m.group(1))]
            hits += [('private IP', m.group(0)) for m in PRIVATE_IP.finditer(line)]
            hits += [('Azure DevOps', m.group(0)) for m in ADO.finditer(line) if not ADO_ALLOWED.match(m.group(0))]
            hits += [('home directory', m.group(0)) for m in HOME.finditer(line) if set(m.group(2)) != {'.'}]
            hits += [('token or key', m.group(0)[:12] + '...') for m in SECRET.finditer(line)]
            if kw:
                hits += [('keyword', m.group(0)) for m in kw.finditer(line)]
            findings += [f'{path}:{n}: {kind}: {what}' for kind, what in hits]
    return findings


def last_release() -> str | None:
    r = subprocess.run(['git', 'rev-parse', '--verify', '-q', f'refs/heads/{BRANCH}'], capture_output=True, text=True)
    return r.stdout.strip() or None


def work_branch(name: str | None) -> str:
    """The work branch: `name`, or the branch that is checked out. Never BRANCH, never a detached HEAD."""
    if name is None:
        r = subprocess.run(['git', 'symbolic-ref', '-q', '--short', 'HEAD'], capture_output=True, text=True)
        name = r.stdout.strip()
        if not name:
            print('HEAD is detached: check out the work branch, or give --work', file=sys.stderr)
            sys.exit(2)
    if name == BRANCH:
        print(f'{BRANCH} has only the releases and cannot be the work branch: '
              f'check out the work branch, or give --work', file=sys.stderr)
        sys.exit(2)
    if subprocess.run(['git', 'rev-parse', '--verify', '-q', f'refs/heads/{name}'], capture_output=True).returncode:
        print(f'{name}: no such local branch', file=sys.stderr)
        sys.exit(2)
    return name


def restart_work(work: str, source: str, release: str, day: datetime.date, co_author: str | None) -> None:
    """Start the work branch again from the release, when it is still at the source of it.

    The new commit has the tree of the source, so the working tree and the index stay as they are.
    One tag is kept for each day: a second release on the same day moves the tag of that day.
    """
    tip = git('rev-parse', f'refs/heads/{work}').strip()
    if tip != source:
        print(f'{work} is at {tip[:7]}, not at the source {source[:7]}: it keeps its history')
        return
    tag = f'archive/{work}-{day:%y%m%d}'
    r = subprocess.run(['git', 'rev-parse', '--verify', '-q', f'refs/tags/{tag}^{{commit}}'], capture_output=True, text=True)
    if r.stdout.strip():
        print(f'{tag} moves: it was at {r.stdout.strip()[:7]}, whose history git gc may now remove')
    git('tag', '-a', '-f', tag, '-m', f'The history of {work} up to the release {release[:7]}', source)
    message = (f'chore publish-github: {work} starts again from {BRANCH} {release[:7]} - the files that are never published\n\n'
               f'{", ".join(e + "/" for e in EXCLUDED)}, which the snapshots leave out. '
               f'The history before it is in the tag {tag}.\n')
    if co_author:
        message += f'\nCo-Authored-By: {co_author}\n'
    commit = git('commit-tree', f'{source}^{{tree}}', '-p', release, '-F', '-', data=message.encode()).strip()
    git('update-ref', f'refs/heads/{work}', commit, source)
    print(f'{work}: {commit[:7]} on {release[:7]}; the old history is in {tag}')


def report(work: str, source: str, tree: str, keywords: list[str]) -> bool:
    print(f'work:   {work}')
    print(f'source: {source[:12]} ({git("log", "-1", "--format=%s", source).strip()[:70]})')
    print(f'tree:   {tree}')
    print(f'keywords: {len(keywords)} from {KEYWORDS}')
    findings = scan(tree, keywords)
    for f in findings:
        print(f'[FIND] {f}')
    print(f'scan: {"nothing found" if not findings else f"{len(findings)} finding(s)"}')
    prev = last_release()
    if prev is None:
        print(f'first release: {len(git("ls-tree", "-r", "--name-only", tree).splitlines())} files')
    elif git('rev-parse', f'{prev}^{{tree}}').strip() == tree:
        print(f'no change since the last release {prev[:7]}')
    else:
        changes = git('diff', '--name-status', f'{prev}^{{tree}}', tree).splitlines()
        print(f'changes since the last release {prev[:7]}: {len(changes)} file(s)')
        for c in changes:
            print(f'  {c}')
        commits = [l for l in git('log', '--reverse', '--format=%h %s', f'{prev}..{source}').splitlines()
                   if not RESTART.match(l.split(' ', 1)[1])]
        print(f'commits of {work} since the last release: {len(commits)}')
        for l in commits:
            print(f'  {l}')
    return not findings


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('check', help='build and scan the tree of the release; write nothing')
    c.add_argument('--work', help='the work branch (default: the branch that is checked out)')
    c.add_argument('--source', help='the commit to release (default: the tip of the work branch)')
    p = sub.add_parser('publish', help='make the snapshot commit on main and push it')
    p.add_argument('--work', required=True, help='the work branch that check printed')
    p.add_argument('--source', required=True, help='the commit that check printed')
    p.add_argument('--tree', required=True, help='the tree that check printed')
    m = p.add_mutually_exclusive_group(required=True)
    m.add_argument('--summary', help='the summary of the changes for the body of the commit message')
    m.add_argument('--summary-file', type=Path,
                   help='a UTF-8 file with the summary; use it for more than one line, because a .bat shim of python '
                        'breaks an argument at its line ends. A blank line divides paragraphs')
    p.add_argument('--co-author', help='a Co-Authored-By trailer for the commit message, "Name <email>"')
    p.add_argument('--no-push', action='store_true', help='make the commit, but do not push')
    for s in (c, p):
        s.add_argument('--keywords', type=Path, default=Path(KEYWORDS), help=f'the keyword file (default: {KEYWORDS})')
    a = ap.parse_args()

    summary = getattr(a, 'summary', None)
    if getattr(a, 'summary_file', None):
        summary = a.summary_file.read_text(encoding='utf-8')
    if a.cmd == 'publish' and not summary.strip():
        print('--summary is empty: write what changed since the last release', file=sys.stderr)
        sys.exit(2)
    keywords = read_keywords(a.keywords)
    work = work_branch(a.work)
    source = git('rev-parse', '--verify', f'{a.source or work}^{{commit}}').strip()
    tree = build_tree(source)
    if a.cmd == 'check':
        sys.exit(0 if report(work, source, tree, keywords) else 1)

    if tree != a.tree:
        print(f'the tree of {source[:12]} is {tree}, not {a.tree}: run check again', file=sys.stderr)
        sys.exit(2)
    if not report(work, source, tree, keywords):
        sys.exit(1)
    prev = last_release()
    day = datetime.date.today()
    message = f'SkillsGestalt {day.isoformat()}\n\n{summary.strip()}\n\nFrom {work} {source[:12]}.\n'
    if a.co_author:
        message += f'\nCo-Authored-By: {a.co_author}\n'
    commit = git('commit-tree', tree, *(['-p', prev] if prev else []), '-F', '-', data=message.encode()).strip()
    git('update-ref', f'refs/heads/{BRANCH}', commit, prev or '')
    print(f'release: {commit[:7]} on {BRANCH}' + (f', after {prev[:7]}' if prev else ''))
    if a.no_push:
        print(f'not pushed: git push {REMOTE} {BRANCH}:{REMOTE_BRANCH}')
    else:
        git('push', REMOTE, f'{BRANCH}:{REMOTE_BRANCH}')
        print(f'pushed: {BRANCH} -> {REMOTE}/{REMOTE_BRANCH}')
    restart_work(work, source, commit, day, a.co_author)


if __name__ == '__main__':
    main()
