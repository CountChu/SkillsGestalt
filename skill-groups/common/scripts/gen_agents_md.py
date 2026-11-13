#!/usr/bin/env python3
"""Make the AGENTS.md and the CLAUDE.md of an agency from the shared template and the agency's own part.

Every agency follows the same rules - Markdown, twins, tasks, chores - and each has a little of its own.
The shared rules are written once, as a template in the common skill group; each agency writes only its
own part, beside its AGENTS.md; this script puts the two together and fills in the paths:

  {skillGroups.common}/templates/AGENTS-tmp.md   the shared rules, its paths written {skillGroups.common}
  AGENTS.shared.md                               the agency's own part, at the root of its workspace, in git
  AGENTS.md                                      what this script writes - read by the agent, never edited
  CLAUDE.md                                      the one line @AGENTS.md, also written here

VS Code Copilot reads AGENTS.md and not CLAUDE.md; Claude Code reads CLAUDE.md, and its `@AGENTS.md` import
loads all of AGENTS.md. So the rules are written once, in AGENTS.md, and both agents read them.

An AGENTS.md cannot leave {skillGroups.common} for the agent to expand: an agent reads an `@path` import
and a link as written, and an agent that has to look the value up spends tokens on it. So the paths are
filled in here, from the config.yaml at the root, and AGENTS.md holds only real ones.

The template is read as written, but for:

  {agencyName}        the name of the root folder, such as SkillsGestalt
  {skillGroups.X}     the value of skillGroups.X in config.yaml, as written there
  {keepEnglishChore}  a link to the chore that keepEnglishChore in config.yaml names, such as keep-english:
                      [keep-english](chores/keep-english.md) when the agency has it, else the same file of
                      the one agency of config.yaml's agencies that has it, linked relative to the root.
                      Without that setting, each line that holds it goes
  {tasksDir}          tasksDir in config.yaml, or tasks when it is not set: the folder of the tasks
  {taskSummary}       taskSummary in config.yaml, or dashboard/task-summary.md when it is not set
  {tasksDir!q}        the same, in double quotes when the value holds a space - for a command;
  {taskSummary!q}     the two are set apart: the tasks and the summary can each be anywhere, such as in the vault
  {choreSummary}      choreSummary in config.yaml, or dashboard/chore-summary.md when it is not set
  {choreSummary!q}    the same, in double quotes when the value holds a space - for a command
  {skillGroupRoots}   a line of its own, replaced by a table of each skill group of skillGroups in config.yaml,
                      in its order, with its root as written there and the names of its skills - each
                      directory of <root>/skills with a SKILL.md - as a table: | `common` | `skill-groups/common` | `asd-ste`,
                      `chinese` |. So the agent finds a skill, or knows that there is none, with no read; and
                      a skill that is added or removed needs this script again
  {{name}}            {name}, as it is: for a sentence that has to show a placeholder
  {AGENTS-shared-top} a line of its own, replaced by the top part of AGENTS.shared.md
  {AGENTS-shared}     a line of its own, replaced by the rest of AGENTS.shared.md

AGENTS.shared.md is split at a line {AGENTS-shared} of its own: what is above it goes to the top slot, what
is below it to the other. Without that line, all of it goes to the other slot, and the top slot and its
blank line go.

A link to {skillGroups.X}/... is written relative to the root when the value is an absolute path or starts
with ~, as ../SkillsGestalt/skill-groups/common/...: a Markdown viewer does not expand ~, and a relative link
names no account. When no relative path exists - two drives on Windows - the link keeps the value as
written. A command and an inline-code span keep the value as written, ~ and all, which a shell expands.

AGENTS.shared.md may open with a "> Technical words: ..." line. That line does not go into AGENTS.md as it
is: its words join the template's own "> Technical words:" line, so that the STE check of AGENTS.md knows
them all, and its blank line goes with it.

The quotes under the title - the STE records and the Technical words - are for the STE check only, and an
agent reads AGENTS.md in each session: so AGENTS.md is written without them. --ste writes the full text,
with them, to a file of its own, for check_ste.py.

  (no flag)  write AGENTS.md and CLAUDE.md
  --check    write nothing; compare the two files with what it would write, and print the difference
  --ste FILE also write AGENTS.md with its STE header to FILE

A python without PyYAML runs the script again with the python of the .venv at the root, as
gen_config.py does. Its output is UTF-8 on each console.

Each file is read with its CRLF line ends made LF, as a Git for Windows clone with core.autocrlf=true
checks it out; the files are written with LF. A CRLF AGENTS.md or CLAUDE.md that is otherwise the same
is unchanged, and passes --check.

Run it from the root of the workspace after a change to the template, to AGENTS.shared.md or to
config.yaml. A workspace that has a config.shared.yaml runs gen_config.py instead: it makes config.yaml,
and then runs this script. Exit status: 0 the two files are written, or are already what it would write; 1 under --check,
one is not; 2 a file is missing or unreadable, the template names a value config.yaml does not have, or
the root has no config.shared.yaml, or config.yaml has no workBranch, the work branch of this clone, or no
list workBranches with it: each agency has the three, on each computer.
An agency that still has the AGENTS-local.md or the CLAUDE-local.md of an older version, and no
AGENTS.shared.md, stops with 2: rename the file to AGENTS.shared.md, and its {AGENTS-local} or
{CLAUDE-local} line to {AGENTS-shared}. An AGENTS.shared.md that still has such a line also stops with 2.
The name says where the file applies: -tmp is a template of the common skill group, .shared. is of this
agency and in git, and .local. is of one computer and not in git.
"""
from __future__ import annotations

import argparse
import difflib
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:  # this python has no PyYAML: run again with the python of the .venv at the root
    import os
    import subprocess
    for venv in (Path('.venv/Scripts/python.exe'), Path('.venv/bin/python')):
        if venv.is_file() and not os.environ.get('GESTALT_VENV_RERUN'):
            sys.exit(subprocess.run([str(venv), *sys.argv], env={**os.environ, 'GESTALT_VENV_RERUN': '1'}).returncode)
    print(f'{sys.executable} has no PyYAML, and the root has no .venv with it: pip install pyyaml', file=sys.stderr)
    sys.exit(2)

for _stream in (sys.stdout, sys.stderr):  # a Windows console or pipe can be cp1252: print Chinese text and icons
    if hasattr(_stream, 'reconfigure'):
        _stream.reconfigure(encoding='utf-8')

TEMPLATE = 'templates/AGENTS-tmp.md'
LOCAL = 'AGENTS.shared.md'
OLD_LOCALS = ('AGENTS-local.md', 'CLAUDE-local.md')
LOCAL_SLOT = '{AGENTS-shared}'
TOP_SLOT = '{AGENTS-shared-top}'
OLD_SLOTS = ('{AGENTS-local}', '{CLAUDE-local}')
CLAUDE_TEXT = '@AGENTS.md\n'
CHORE = '{keepEnglishChore}'
ROOTS_SLOT = '{skillGroupRoots}'
WORDS = '> Technical words: '
LITERAL = re.compile(r'\{\{([^{}]+)\}\}')
TASK_PATHS = {'tasksDir': 'tasks', 'taskSummary': 'dashboard/task-summary.md', 'choreSummary': 'dashboard/chore-summary.md'}
TASK_PATH = re.compile(r'\{(tasksDir|taskSummary|choreSummary)(!q)?\}')
GROUP = re.compile(r'\{skillGroups\.(\w+)\}')
LINK_GROUP = re.compile(r'\]\(\{skillGroups\.(\w+)\}')
SHARED_CONFIG = 'config.shared.yaml'


def skill_names(value: str, root: Path) -> list[str]:
    """The names of the skills of a skill group: each directory of <root of the group>/skills with a SKILL.md."""
    base = Path(os.path.expanduser(value))
    skills = (base if base.is_absolute() else root / base) / 'skills'
    return sorted(p.name for p in skills.iterdir() if (p / 'SKILL.md').is_file()) if skills.is_dir() else []


def drop_ste_header(text: str) -> str:
    """The text without the quotes under its title - the STE records and the Technical words - which only
    the STE check reads."""
    lines = text.split('\n')
    i = 1
    while i < len(lines) and (not lines[i] or lines[i].startswith('>')):
        i += 1
    return '\n'.join(lines[:1] + [''] + lines[i:])


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    sys.exit(2)


def read(path: Path) -> str:
    if not path.is_file():
        fail(f'{path}: no such file')
    return path.read_bytes().decode('utf-8').replace('\r\n', '\n')


def link_base(value: str, root: Path) -> str:
    """The value for a link target: relative to the root when it is absolute, as written otherwise."""
    path = Path(os.path.expanduser(value))
    if not path.is_absolute():
        return value
    try:
        return os.path.relpath(os.path.realpath(path), os.path.realpath(root)).replace(os.sep, '/')
    except ValueError:
        return value


def render(root: Path) -> str:
    config = yaml.safe_load(read(root / 'config.yaml')) or {}
    groups = {k: str(v) for k, v in (config.get('skillGroups') or {}).items() if v}
    if 'common' not in groups:
        fail(f'{root / "config.yaml"}: skillGroups.common is not set')
    work = config.get('workBranch')
    if not isinstance(work, str) or not work.strip():
        fail(f'{root / "config.yaml"}: workBranch is not set: each clone names its work branch, '
             f'in config.local.yaml when the root has config.shared.yaml')
    listed = config.get('workBranches')
    if not isinstance(listed, list) or work not in [str(b) for b in listed]:
        fail(f'{root / "config.yaml"}: workBranches does not list workBranch {work}: '
             f'it is the list of the work branch of each clone, in config.shared.yaml')
    if not (root / SHARED_CONFIG).is_file():
        fail(f'{root / SHARED_CONFIG}: no such file: each agency keeps its settings in it, and the values '
             f'of each computer in config.local.yaml; gen_config.py makes config.yaml from the two')
    common = Path(os.path.expanduser(groups['common']))
    template = read((common if common.is_absolute() else root / common) / TEMPLATE)
    if not (root / LOCAL).is_file():
        for old in OLD_LOCALS:
            if (root / old).is_file():
                fail(f'{root / old}: rename it to {LOCAL} (git mv {old} {LOCAL}), '
                     f'and a line {" or ".join(OLD_SLOTS)} in it to {LOCAL_SLOT}')
    local = read(root / LOCAL)
    for old in OLD_SLOTS:
        if old in local.split('\n'):
            fail(f'{root / LOCAL}: change its line {old} to {LOCAL_SLOT}')

    words: list[str] = []
    if local.startswith(WORDS):
        first, _, local = local.partition('\n')
        words = [w.strip() for w in first[len(WORDS):].rstrip('.').split(',') if w.strip()]
        local = local.lstrip('\n')
    parts = local.split('\n')
    top, bottom = ('', local) if LOCAL_SLOT not in parts else (
        '\n'.join(parts[:parts.index(LOCAL_SLOT)]), '\n'.join(parts[parts.index(LOCAL_SLOT) + 1:]))
    lines = template.split('\n')
    for slot in (LOCAL_SLOT, TOP_SLOT):
        if lines.count(slot) != 1:
            fail(f'the template has {lines.count(slot)} line(s) {slot}, not 1')
    lines[lines.index(LOCAL_SLOT)] = bottom.strip('\n')
    roots = '\n'.join(['| Skill group | Root | Skills |', '| --- | --- | --- |'] + [
        f'| `{k}` | `{v}` | {", ".join(f"`{s}`" for s in skill_names(v, root)) or "—"} |' for k, v in groups.items()])
    lines = [roots if l == ROOTS_SLOT else l for l in lines]
    i = lines.index(TOP_SLOT)
    if top.strip():
        lines[i] = top.strip('\n')
    else:
        del lines[i:i + 2 if i + 1 < len(lines) and not lines[i + 1] else i + 1]
    for i, line in enumerate(lines):
        if line.startswith(WORDS) and words:
            have = [w.strip() for w in line[len(WORDS):].rstrip('.').split(',')]
            lines[i] = WORDS + ', '.join(sorted(set(have) | set(words), key=str.lower)) + '.'
            break
    chore = str(config.get('keepEnglishChore') or '').strip()
    if chore:
        target = f'chores/{chore}.md'
        if not (root / target).is_file():
            homes = [str(v) for v in (config.get('agencies') or {}).values()
                     if Path(os.path.expanduser(str(v)), target).is_file()]
            if len(homes) != 1:
                fail(f'keepEnglishChore is {chore}, and {len(homes)} agencies of config.yaml have {target}, not 1')
            target = f'{link_base(homes[0], root)}/{target}'
        lines = [l.replace(CHORE, f'[{chore}]({target})') for l in lines]
    else:
        lines = [l for l in lines if CHORE not in l]
    text = '\n'.join(lines)

    kept: list[str] = []
    text = LITERAL.sub(lambda m: (kept.append(m.group(1)), f'\0{len(kept) - 1}\0')[1], text)
    paths = {k: str(config.get(k) or v) for k, v in TASK_PATHS.items()}
    text = TASK_PATH.sub(lambda m: f'"{paths[m.group(1)]}"' if m.group(2) and any(c.isspace() for c in paths[m.group(1)])
                         else paths[m.group(1)], text)
    missing = sorted({m.group(1) for m in GROUP.finditer(text)} - groups.keys())
    if missing:
        fail(f'the template uses skillGroups.{", skillGroups.".join(missing)}, which config.yaml does not set')
    text = LINK_GROUP.sub(lambda m: '](' + link_base(groups[m.group(1)], root), text)
    text = GROUP.sub(lambda m: groups[m.group(1)], text).replace('{agencyName}', root.name)
    return re.sub(r'\0(\d+)\0', lambda m: '{' + kept[int(m.group(1))] + '}', text)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--root', type=Path, default=Path('.'), help='the root of the workspace (default: .)')
    ap.add_argument('--check', action='store_true', help='compare AGENTS.md and CLAUDE.md with what would be written; write nothing')
    ap.add_argument('--ste', type=Path, help='also write AGENTS.md with its STE header to this file, for check_ste.py')
    a = ap.parse_args()

    root = a.root.resolve()
    full = render(root)
    if a.ste:
        a.ste.write_bytes(full.encode('utf-8'))
        print(f'{a.ste}: written, with the STE header')
    wanted = {'AGENTS.md': drop_ste_header(full), 'CLAUDE.md': CLAUDE_TEXT}
    failed = False
    for name, text in wanted.items():
        target = root / name
        now = target.read_bytes().decode('utf-8').replace('\r\n', '\n') if target.is_file() else ''
        if not a.check:
            if now != text:
                target.write_bytes(text.encode('utf-8'))
            print(f'{name}: {"written" if now != text else "unchanged"}')
        elif now == text:
            print(f'{name}: PASS - it is what the template, {LOCAL} and config.yaml make')
        else:
            sys.stdout.writelines(difflib.unified_diff(now.splitlines(True), text.splitlines(True),
                                                       name, f'{name} from the template'))
            print(f'\n{name}: FAIL - it is not what the template, {LOCAL} and config.yaml make.')
            failed = True
    if failed:
        print(f'Change the template or {LOCAL}, not AGENTS.md or CLAUDE.md, and then run gen_agents_md.py without --check.')
        sys.exit(1)


if __name__ == '__main__':
    main()
