#!/usr/bin/env python3
"""Make a release of this workspace for its public repository: a snapshot of the work branch, scanned before it leaves.

It serves the chores publish-gestalt and pull-gestalt of SkillsGestalt. Its values are SkillsGestalt's
(NAME, CHORE, BRANCH, REMOTE, REMOTE_BRANCH, EXCLUDED, PRIVATE_PATH, SCANS, KEYWORDS), unless the
config.yaml at the root has a section "publish:", which a Forge writes to publish itself the same way:

  publish:
    name: MyForge                  # the first word of the subject of a snapshot
    chore: publish-gestalt         # the chore that the commit that starts WORK again names
    branch: release                # the local branch of the releases; not the work branch
    remote: origin
    remoteBranch: users/me/release # the branch of the remote that gets the releases
    excluded: []                   # the paths that a snapshot leaves out
    privatePaths: ['^checkpoints/', '\\.pdf$']   # regular expressions: a path that must not be in the tree
    scans: [email, token]          # some of email, privateIP, ado, home, token, keyword
    keywords: publish-keywords.local.txt        # the keyword file, for the scan keyword
    emailAllowed: [example.org]    # more domains whose email addresses are not a finding

A key that is not there keeps the value of SkillsGestalt. The root is --workspace, or the nearest
directory at or above the current directory whose config.yaml has skillGroups; the script runs there.

The work branch is the branch that --work names, by default the branch that is checked out: m1 in the
workspace, or a different branch in a different clone. It cannot be BRANCH. Below, WORK stands for it.

The remote branch carries no history of the work branch. Each release is one commit on the
local branch BRANCH, whose tree is the tree of WORK with the paths of EXCLUDED taken out; only BRANCH is
pushed, to REMOTE_BRANCH of REMOTE. After a release WORK starts again from it: the old history of WORK is kept
in the tag archive/WORK-<yymmdd> of the day of the release, and WORK becomes one commit on the release that
puts back the excluded paths, so `git diff BRANCH WORK` shows only them and what is not published yet. Nothing here switches a
branch or touches the working tree, so other sessions can go on working on WORK while a release is made.

When the remote branch already has a history of its own, which is not a line of releases, give --orphan to
the first `check` and `publish`: the snapshot then has no parent, and the push replaces that history with a
force push, with a lease on the commit that the last fetch saw.

  check     build the tree of the release, scan it, and list what changed since the last release.
            It writes nothing. Exit 0 when the scan finds nothing, 1 when it finds something.
  publish   after a person has read what `check` printed: build the same tree again, scan it again,
            make the snapshot commit on BRANCH, push it (unless --no-push), and start WORK again from it.
            Give it the work, the source and the tree that `check` printed, and a summary of the changes.
  incoming  after `git fetch`: list what REMOTE/REMOTE_BRANCH has that the local BRANCH has not, scan its tree and
            the author and committer of each new commit. It writes nothing; the chore pull-gestalt then
            moves main and rebases WORK by hand. Exit 0 when the scan finds nothing, 1 when it finds something.

The message of a snapshot commit is `NAME yyyy-mm-dd`, then the summary that --summary or --summary-file gives,
then the work branch and the commit that the snapshot comes from. `check` lists the commits of WORK since
the last release, to write the summary from.

The scan looks at the text of every file of the tree for each kind of SCANS, by default all of them:

  - email: an email address, except the made-up and no-reply ones (EMAIL_ALLOWED) and the one of the
    snapshot's identity, which every snapshot carries anyway (without "publish:", also the one of IDENTITY)
  - privateIP: a private IP address (10.x.x.x, 172.16-31.x.x, 192.168.x.x)
  - ado: an Azure DevOps organization: a host under visualstudio.com, or a path under dev.azure.com,
    except the public documentation and the made-up contoso examples (ADO_ALLOWED)
  - home: the home directory of a user (/Users/<name>/, /home/<name>/, C:\\Users\\<name>)
  - token: a token or a private key
  - keyword: each word of the keyword file, which is not in git: the names of the organization, projects and
    products that must not be published are themselves private, so they are kept only on this machine.
    Without the file the scan does not run.

It also checks that no private path is in the tree (PRIVATE_PATH): for SkillsGestalt checkpoints/, the
paths of EXCLUDED, the root config.yaml, a *.mermaid.html preview, a PDF.

The author and the committer go out with each commit, and the scan of the files does not see them. So
a snapshot does not take them from the git settings of the computer that makes it, which can be a work
identity: its author and committer are IDENTITY, the one every snapshot on GitHub has, unless the config.yaml at the
root gives an identity of its own, with both of its keys:

  identity:
    name: CountChu
    email: <the email>

 Only the snapshot does;
the commit that starts WORK again stays local and keeps the git settings. `check` prints IDENTITY, and
`check` and `publish` look for each word of the keyword file in it, should it ever be changed to a work
identity; `incoming` does the same for the author and the committer of each new commit. A finding names
only the field, never its value.

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
import shutil
from pathlib import Path

# The values of SkillsGestalt. The "publish:" section of the config.yaml at the root changes them (configure()).
NAME = 'SkillsGestalt'   # the first word of the subject of a snapshot
CHORE = 'publish-gestalt'   # the chore that the commit that starts WORK again names
EXCLUDED = ['external', 'skill-groups/external', 'skill-groups/archived']
PRIVATE_PATH = re.compile(r'^(checkpoints/|handoff/|external/|skill-groups/external/|skill-groups/archived/|config\.yaml$)|\.mermaid\.html$|\.pdf$', re.I)
BRANCH = 'main'
REMOTE, REMOTE_BRANCH = 'origin', 'main'
KEYWORDS = 'publish-keywords.local.txt'
SCANS = ['email', 'privateIP', 'ado', 'home', 'token', 'keyword']   # all the kinds of scan; "scans:" chooses some
IDENTITY = ('CountChu', 'visualge@gmail.com')   # the author and committer of every snapshot
CONFIG = 'config.yaml'
ACTIVE, ACTIVE_FROM = IDENTITY, 'publish_snapshot.py'   # IDENTITY, or the identity of config.yaml
# The commit that starts the work branch again after a release: it is not a change, so it is not in the list of commits.
# publish-github is the old name of the chore, and a work branch can still hold a restart commit with it.
RESTART = re.compile(r'^chore (?:publish-gestalt|publish-github): \S+ starts again from ')
# Each key of "publish:", and the global that it sets. A list key takes [a, b] or one "- item" on each line below it.
PUBLISH_KEYS = {'name': 'NAME', 'chore': 'CHORE', 'branch': 'BRANCH', 'remote': 'REMOTE', 'remoteBranch': 'REMOTE_BRANCH',
                'excluded': 'EXCLUDED', 'privatePaths': 'PRIVATE_PATH', 'scans': 'SCANS', 'keywords': 'KEYWORDS',
                'emailAllowed': 'EMAIL_ALLOWED'}
LIST_KEYS = {'excluded', 'privatePaths', 'scans', 'emailAllowed'}

# The last label of the domain is letters, so a package version such as mermaid@11.4.1 is not taken for one.
EMAIL = re.compile(r'[A-Za-z0-9._%+-]+@((?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,})(?![A-Za-z0-9.-])')
EMAIL_ALLOWED = re.compile(r'^(example\.(com|org|net)|users\.noreply\.github\.com|github\.com)$', re.I)
PRIVATE_IP = re.compile(r'(?<![\d.])(10\.\d{1,3}\.\d{1,3}\.\d{1,3}|172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3})(?![\d.])')
ADO = re.compile(r'([A-Za-z0-9-]+\.visualstudio\.com|dev\.azure\.com/[A-Za-z0-9_.-]+)', re.I)
ADO_ALLOWED = re.compile(r'^(code\.visualstudio\.com|dev\.azure\.com/contoso)$', re.I)
HOME = re.compile(r'(/Users/|/home/|[A-Za-z]:\\Users\\)([A-Za-z0-9._-]+)')
# sk- only at the start of a word: "task-note-description" has sk- in it, and is not a key.
SECRET = re.compile(r'gh[pousr]_[A-Za-z0-9]{20,}|(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|xox[baprs]-[A-Za-z0-9-]{10,}')


def git(*args: str, env: dict | None = None, data: bytes | None = None) -> str:
    r = subprocess.run(['git', *args], capture_output=True, input=data, env=env)
    if r.returncode != 0:
        print(f'git {" ".join(args)}: {r.stderr.decode(errors="replace").strip()}', file=sys.stderr)
        sys.exit(2)
    return r.stdout.decode('utf-8', errors='replace')


ROOT: Path | None = None   # set by main() from --workspace or the current directory
CONFIGURED = False   # True when config.yaml has a "publish:" section


def workspace_root() -> Path:
    """The root of the workspace that runs the script: ROOT, which main() sets."""
    assert ROOT is not None
    return ROOT


def find_root(given: Path | None) -> Path:
    """--workspace, or the nearest directory at or above the current directory whose config.yaml has
    skillGroups (run-data-rules.md). Not the location of this script: a Forge runs it from SkillsGestalt."""
    if given is not None:
        if not (given / CONFIG).is_file():
            print(f'{given}: no {CONFIG}', file=sys.stderr)
            sys.exit(2)
        return given.resolve()
    for d in [Path.cwd(), *Path.cwd().parents]:
        f = d / CONFIG
        if f.is_file() and re.search(r'^skillGroups:', f.read_text(encoding='utf-8-sig'), re.M):
            return d
    print(f'no {CONFIG} with skillGroups at or above {Path.cwd()}: run from the root of the workspace, '
          f'or give --workspace', file=sys.stderr)
    sys.exit(2)


def config_section(config: Path, section: str) -> dict[str, str | list[str]] | None:
    """The keys under "<section>:" of config.yaml, or None when it has no such section. Read by hand, as
    the rest of this script needs no YAML: one level of keys, each a scalar, an inline list [a, b], or
    a list with one "- item" on each line below it; a # comment allowed after a space. A value can be in
    quotes, which keep a # or a , in it."""
    if not config.is_file():
        return None
    found: dict[str, str | list[str]] = {}
    inside = seen = False
    key = None
    for line in config.read_text(encoding='utf-8-sig').split('\n'):
        bare = re.sub(r'''\s+#(?=(?:[^'"]|'[^']*'|"[^"]*")*$).*$''', '', line).rstrip()
        if not bare or bare.lstrip().startswith('#'):
            continue
        if not bare.startswith((' ', '\t')):
            inside = bare == f'{section}:'
            seen = seen or inside
            continue
        if not inside:
            continue
        item = bare.strip()
        if item.startswith('- ') and key is not None:
            value = found.get(key)
            found[key] = (value if isinstance(value, list) else []) + [unquote(item[2:])]
        elif ':' in item:
            key, value = (x.strip() for x in item.split(':', 1))
            if key in found:
                print(f'{config}: {section}.{key} is there two times', file=sys.stderr)
                sys.exit(2)
            if value.startswith('[') and value.endswith(']'):
                found[key] = [unquote(v) for v in re.findall(r'''"[^"]*"|'[^']*'|[^,\s][^,]*''', value[1:-1])]
            else:
                found[key] = unquote(value) if value else []
    return found if seen else None


def unquote(value: str) -> str:
    value = value.strip()
    return value[1:-1] if len(value) > 1 and value[0] == value[-1] and value[0] in '"\'' else value


def configure(config: Path) -> None:
    """Take the values of the "publish:" section of config.yaml. Without the section, the values of
    SkillsGestalt stay. Exit 2 for a key that is not known, or a value of the wrong form."""
    section = config_section(config, 'publish')
    if section is None:
        return
    g = globals()
    g['CONFIGURED'] = True
    for key, value in section.items():
        if key not in PUBLISH_KEYS:
            print(f'{config}: publish.{key} is not a known key; the keys are {", ".join(PUBLISH_KEYS)}', file=sys.stderr)
            sys.exit(2)
        if (key in LIST_KEYS) != isinstance(value, list) or value in ('', []) and key not in LIST_KEYS:
            print(f'{config}: publish.{key} must be {"a list" if key in LIST_KEYS else "one value"}', file=sys.stderr)
            sys.exit(2)
        if key == 'privatePaths':
            value = re.compile('|'.join(f'(?:{p})' for p in value), re.I) if value else re.compile(r'(?!)')
        elif key == 'emailAllowed':
            value = re.compile(EMAIL_ALLOWED.pattern[:-2] + ''.join(f'|{re.escape(d)}' for d in value) + ')$', re.I)
        elif key == 'scans' and set(value) - set(SCANS):
            print(f'{config}: publish.scans: {", ".join(sorted(set(value) - set(SCANS)))} is not a scan; '
                  f'the scans are {", ".join(SCANS)}', file=sys.stderr)
            sys.exit(2)
        g[PUBLISH_KEYS[key]] = value
    if 'chore' in section:
        g['RESTART'] = re.compile(rf'^chore (?:{re.escape(CHORE)}|publish-gestalt|publish-github): \S+ starts again from ')


def build_tree(source: str) -> str:
    """The tree of `source` without the EXCLUDED paths, written through an index of its own.

    The index is a temporary file of a script that is not in a run of a skill, so it goes in
    temp/publish-gestalt-index-{pid}/ at the root of the workspace (run-data-rules.md), and the
    directory is removed when the tree is written, also after an error."""
    d = workspace_root() / 'temp' / f'publish-gestalt-index-{os.getpid()}'
    d.mkdir(parents=True, exist_ok=False)
    try:
        env = {**os.environ, 'GIT_INDEX_FILE': str(d / 'index')}
        git('read-tree', source, env=env)
        if EXCLUDED:
            git('rm', '-r', '--cached', '--quiet', '--ignore-unmatch', '--', *EXCLUDED, env=env)
        return git('write-tree', env=env).strip()
    finally:
        shutil.rmtree(d, ignore_errors=True)


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


def own_emails() -> tuple[str, ...]:
    """The emails that the scan lets through because every snapshot carries them anyway: ACTIVE, and IDENTITY
    too when no "publish:" section is there. A workspace with its own section has its own identity, so the
    email of SkillsGestalt is a finding there."""
    return (ACTIVE[1],) if CONFIGURED else (IDENTITY[1], ACTIVE[1])


def scan(tree: str, keywords: list[str]) -> list[str]:
    """Each finding, as 'path:line: kind: text'."""
    findings = []
    paths = [l for l in git('ls-tree', '-r', '--name-only', '-z', tree).split('\0') if l]
    findings += [f'{p}: a private path in the tree' for p in paths if PRIVATE_PATH.search(p)]
    kw = re.compile('|'.join(re.escape(k) for k in keywords), re.I) if keywords and 'keyword' in SCANS else None
    on = set(SCANS)
    for path, text in blobs(tree):
        for n, line in enumerate(text.split('\n'), 1):
            hits = []
            if 'email' in on:
                hits += [('email', m.group(0)) for m in EMAIL.finditer(line)
                         if not EMAIL_ALLOWED.match(m.group(1)) and m.group(0) not in own_emails()]
            if 'privateIP' in on:
                hits += [('private IP', m.group(0)) for m in PRIVATE_IP.finditer(line)]
            if 'ado' in on:
                hits += [('Azure DevOps', m.group(0)) for m in ADO.finditer(line) if not ADO_ALLOWED.match(m.group(0))]
            if 'home' in on:
                hits += [('home directory', m.group(0)) for m in HOME.finditer(line) if set(m.group(2)) != {'.'}]
            if 'token' in on:
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
    left_out = (f'{", ".join(e + "/" for e in EXCLUDED)}, which the snapshots leave out. ' if EXCLUDED
                else 'The snapshots leave out no path, so this commit changes no file. ')
    message = (f'chore {CHORE}: {work} starts again from {BRANCH} {release[:7]} - the files that are never published\n\n'
               f'{left_out}The history before it is in the tag {tag}.\n')
    if co_author:
        message += f'\nCo-Authored-By: {co_author}\n'
    commit = git('commit-tree', f'{source}^{{tree}}', '-p', release, '-F', '-', data=message.encode()).strip()
    git('update-ref', f'refs/heads/{work}', commit, source)
    print(f'{work}: {commit[:7]} on {release[:7]}; the old history is in {tag}')


def identity_findings(idents: list[tuple[str, str]], keywords: list[str], fix: str) -> list[str]:
    """Each (label, "Name <email>") that holds a word of the keyword file - named by its label only."""
    kw = re.compile('|'.join(re.escape(k) for k in keywords), re.I) if keywords else None
    return [f'{label}: holds a word of {KEYWORDS} - {fix}' for label, ident in idents if kw and kw.search(ident)]


def config_identity(config: Path) -> tuple[str, str] | None:
    """The name and the email under "identity:" of config.yaml, or None when it has no identity.
    Exit 2 when only one of the two keys is there: half of an identity would be someone else's."""
    found = config_section(config, 'identity')
    if found is None:
        return None
    if not isinstance(found.get('name'), str) or not found.get('name') or \
            not isinstance(found.get('email'), str) or not found.get('email'):
        print(f'{config}: identity needs both name and email', file=sys.stderr)
        sys.exit(2)
    return found['name'], found['email']


def snapshot_identity() -> list[tuple[str, str]]:
    """The author and the committer of a snapshot: ACTIVE, whatever the git settings are."""
    return [(label, f'{ACTIVE[0]} <{ACTIVE[1]}>') for label in ('author', 'committer')]


def snapshot_env() -> dict:
    """The environment that makes git write ACTIVE as the author and the committer."""
    name, email = ACTIVE
    return {**os.environ, 'GIT_AUTHOR_NAME': name, 'GIT_AUTHOR_EMAIL': email,
            'GIT_COMMITTER_NAME': name, 'GIT_COMMITTER_EMAIL': email}


def incoming(upstream: str, keywords: list[str]) -> bool:
    """What upstream has that the local main has not: its commits, the scan of their identities and of the
    tree of upstream, and the files that change. True when nothing is found."""
    up = git('rev-parse', '--verify', f'{upstream}^{{commit}}').strip()
    here = git('rev-parse', '--verify', f'refs/heads/{BRANCH}^{{commit}}').strip()
    print(f'{BRANCH}: {here[:7]}, {upstream}: {up[:7]}')
    if up == here:
        print(f'nothing to pull: {BRANCH} is at {upstream}')
        return True
    base = git('merge-base', here, up).strip()
    if base == up:
        print(f'nothing to pull: {BRANCH} is ahead of {upstream}, and {CHORE} pushes it')
        return True
    if base != here:
        print(f'{BRANCH} and {upstream} diverged at {base[:7]}: the history of {upstream} was rewritten. '
              f'Reset {BRANCH} to it, and rebase the work branch onto it')
    log = git('log', '--reverse', '--format=%H%x00%s%x00%an <%ae>%x00%cn <%ce>', f'{base}..{up}').splitlines()
    print(f'new commits of {upstream}: {len(log)}')
    findings = []
    for line in log:
        sha, subject, author, committer = line.split('\0')
        print(f'  {sha[:7]} {subject[:70]}')
        findings += [f'{sha[:7]} {f}' for f in identity_findings([('author', author), ('committer', committer)], keywords,
                                                                 'the computer that published it must set git user.name and user.email')]
    tree = git('rev-parse', f'{up}^{{tree}}').strip()
    findings += scan(tree, keywords)
    changes = git('diff', '--name-status', f'{base}^{{tree}}', tree).splitlines()
    print(f'changes since {base[:7]}: {len(changes)} file(s)')
    for c in changes:
        print(f'  {c}')
    for f in findings:
        print(f'[FIND] {f}')
    print(f'scan: {"nothing found" if not findings else f"{len(findings)} finding(s)"}')
    return not findings


def remote_commits() -> int | None:
    """The number of commits of REMOTE/REMOTE_BRANCH as the last fetch saw it, or None when there is no such ref."""
    r = subprocess.run(['git', 'rev-list', '--count', f'refs/remotes/{REMOTE}/{REMOTE_BRANCH}'], capture_output=True, text=True)
    return int(r.stdout) if r.returncode == 0 else None


def report(work: str, source: str, tree: str, keywords: list[str], orphan: bool = False) -> bool:
    print(f'work:   {work}')
    print(f'source: {source[:12]} ({git("log", "-1", "--format=%s", source).strip()[:70]})')
    print(f'tree:   {tree}')
    if CONFIGURED:
        print(f'config: publish: of {CONFIG} - {NAME}, {BRANCH} -> {REMOTE}/{REMOTE_BRANCH}')
        print(f'scans: {", ".join(SCANS)}')
    if 'keyword' in SCANS:
        print(f'keywords: {len(keywords)} from {KEYWORDS}')
    print(f'identity: {ACTIVE[0]} <{ACTIVE[1]}> from {ACTIVE_FROM}, the author and committer of the snapshot')
    fix = 'change identity in config.yaml' if ACTIVE_FROM == CONFIG else 'change IDENTITY in publish_snapshot.py'
    findings = identity_findings(snapshot_identity(), keywords, fix) + scan(tree, keywords)
    for f in findings:
        print(f'[FIND] {f}')
    print(f'scan: {"nothing found" if not findings else f"{len(findings)} finding(s)"}')
    prev = None if orphan else last_release()
    if prev is None:
        print(f'first release: {len(git("ls-tree", "-r", "--name-only", tree).splitlines())} files')
        n = remote_commits()
        if orphan:
            print(f'--orphan: the snapshot has no parent, and the push replaces '
                  f'{"no commit" if n is None else f"the {n} commit(s)"} of {REMOTE}/{REMOTE_BRANCH} with it')
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
    p = sub.add_parser('publish', help='make the snapshot commit on the release branch and push it')
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
    i = sub.add_parser('incoming', help='after git fetch: list and scan what the remote branch has that the release branch has not; write nothing')
    i.add_argument('--upstream', help='the branch to compare with (default: REMOTE/REMOTE_BRANCH, origin/main without a "publish:" section)')
    for s in (c, p):
        s.add_argument('--orphan', action='store_true',
                       help='the first release of a remote branch that has a history of its own: the snapshot has no parent, '
                            'and publish replaces that history with a force push. Give it to check and to publish')
    for s in (c, p, i):
        s.add_argument('--keywords', type=Path, help=f'the keyword file (default: publish.keywords, or {KEYWORDS})')
        s.add_argument('--workspace', type=Path,
                       help=f'the root of the workspace (default: the nearest directory at or above the current one whose {CONFIG} has skillGroups)')
    a = ap.parse_args()
    global ROOT, ACTIVE, ACTIVE_FROM
    # The paths of the command line are from the current directory; the rest is from the root.
    a.keywords = a.keywords and a.keywords.resolve()
    if getattr(a, 'summary_file', None):
        a.summary_file = a.summary_file.resolve()
    ROOT = find_root(a.workspace)
    os.chdir(ROOT)
    configure(Path(CONFIG))
    keywords = read_keywords(a.keywords or Path(KEYWORDS)) if 'keyword' in SCANS else []
    if a.cmd == 'incoming':
        sys.exit(0 if incoming(a.upstream or f'{REMOTE}/{REMOTE_BRANCH}', keywords) else 1)

    summary = getattr(a, 'summary', None)
    if getattr(a, 'summary_file', None):
        summary = a.summary_file.read_text(encoding='utf-8')
    if a.cmd == 'publish' and not summary.strip():
        print('--summary is empty: write what changed since the last release', file=sys.stderr)
        sys.exit(2)
    own = config_identity(Path(CONFIG))
    if own:
        ACTIVE, ACTIVE_FROM = own, CONFIG
    work = work_branch(a.work)
    source = git('rev-parse', '--verify', f'{a.source or work}^{{commit}}').strip()
    tree = build_tree(source)
    if a.cmd == 'check':
        sys.exit(0 if report(work, source, tree, keywords, a.orphan) else 1)

    if tree != a.tree:
        print(f'the tree of {source[:12]} is {tree}, not {a.tree}: run check again', file=sys.stderr)
        sys.exit(2)
    if not report(work, source, tree, keywords, a.orphan):
        sys.exit(1)
    old = last_release()
    prev = None if a.orphan else old
    day = datetime.date.today()
    message = f'{NAME} {day.isoformat()}\n\n{summary.strip()}\n\nFrom {work} {source[:12]}.\n'
    if a.co_author:
        message += f'\nCo-Authored-By: {a.co_author}\n'
    commit = git('commit-tree', tree, *(['-p', prev] if prev else []), '-F', '-', data=message.encode(),
                 env=snapshot_env()).strip()
    git('update-ref', f'refs/heads/{BRANCH}', commit, old or '')
    print(f'release: {commit[:7]} on {BRANCH}' + (f', after {prev[:7]}' if prev else '')
          + (f', in place of {old[:7]}, which stays only in the reflog of {BRANCH}' if a.orphan and old else ''))
    # The lease: the push replaces the remote branch only when it is still where the last fetch saw it
    # (or, with no remote-tracking branch, only when the remote branch is not there).
    seen = subprocess.run(['git', 'rev-parse', '--verify', '-q', f'refs/remotes/{REMOTE}/{REMOTE_BRANCH}'],
                          capture_output=True, text=True).stdout.strip()
    force = [f'--force-with-lease=refs/heads/{REMOTE_BRANCH}:{seen}'] if a.orphan else []
    if a.no_push:
        print(f'not pushed: git push {" ".join(force + [""])}{REMOTE} {BRANCH}:{REMOTE_BRANCH}')
    else:
        r = subprocess.run(['git', 'push', *force, REMOTE, f'{BRANCH}:{REMOTE_BRANCH}'], capture_output=True, text=True)
        if r.returncode != 0:
            # Put BRANCH back, so that it is again what the remote has, and WORK keeps its history.
            git('update-ref', *([f'refs/heads/{BRANCH}', old, commit] if old else ['-d', f'refs/heads/{BRANCH}', commit]))
            print(f'git push: {r.stderr.strip()}', file=sys.stderr)
            print(f'not pushed: {BRANCH} is back at {old[:7] if old else "nothing"}, and {work} is as it was. '
                  f'git fetch {REMOTE}, run pull first if {REMOTE}/{REMOTE_BRANCH} has new releases, then check again',
                  file=sys.stderr)
            sys.exit(2)
        print(f'pushed: {BRANCH} -> {REMOTE}/{REMOTE_BRANCH}' + (' (force, with lease)' if a.orphan else ''))
    restart_work(work, source, commit, day, a.co_author)


if __name__ == '__main__':
    main()
