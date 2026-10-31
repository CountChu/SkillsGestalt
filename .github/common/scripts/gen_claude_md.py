#!/usr/bin/env python3
"""Make the CLAUDE.md of an agency from the shared template and the agency's own part.

Every agency follows the same rules - Markdown, twins, tasks, chores - and each has a little of its own.
The shared rules are written once, as a template in the common skill group; each agency writes only its
own part, beside its CLAUDE.md; this script puts the two together and fills in the paths:

  {skillGroups.common}/templates/CLAUDE-tmp.md   the shared rules, its paths written {skillGroups.common}
  CLAUDE-local.md                                the agency's own part, at the root of its workspace
  CLAUDE.md                                      what this script writes - read by the agent, never edited

A CLAUDE.md cannot leave {skillGroups.common} for the agent to expand: Claude Code reads an `@path` import
and a link as written, and an agent that has to look the value up spends tokens on it. So the paths are
filled in here, from the config.yaml at the root, and CLAUDE.md holds only real ones.

The template is read as written, but for:

  {agencyName}        the name of the root folder, such as SkillsGestalt
  {skillGroups.X}     the value of skillGroups.X in config.yaml, as written there
  {keepEnglishChore}  a link to the chore that keepEnglishChore in config.yaml names, such as keep-english:
                      [keep-english](chores/keep-english.md) when the agency has it, else the same file of
                      the one agency of config.yaml's agencies that has it, linked relative to the root.
                      Without that setting, each line that holds it goes
  {{name}}            {name}, as it is: for a sentence that has to show a placeholder
  {CLAUDE-local-top}  a line of its own, replaced by the top part of CLAUDE-local.md
  {CLAUDE-local}      a line of its own, replaced by the rest of CLAUDE-local.md

CLAUDE-local.md is split at a line {CLAUDE-local} of its own: what is above it goes to the top slot, what
is below it to the other. Without that line, all of it goes to the other slot, and the top slot and its
blank line go.

A link to {skillGroups.X}/... is written relative to the root when the value is an absolute path or starts
with ~, as ../SkillsGestalt/.github/common/...: a Markdown viewer does not expand ~, and a relative link
names no account. When no relative path exists - two drives on Windows - the link keeps the value as
written. A command and an inline-code span keep the value as written, ~ and all, which a shell expands.

CLAUDE-local.md may open with a "> Technical words: ..." line. That line does not go into CLAUDE.md as it
is: its words join the template's own "> Technical words:" line, so that the STE check of CLAUDE.md knows
them all, and its blank line goes with it.

  (no flag)  write CLAUDE.md
  --check    write nothing; compare CLAUDE.md with what it would write, and print the difference

Run it from the root of the workspace after a change to the template, to CLAUDE-local.md or to
config.yaml. Exit status: 0 CLAUDE.md is written, or is already what it would write; 1 under --check, it
is not; 2 a file is missing or unreadable, or the template names a value config.yaml does not have.
"""
from __future__ import annotations

import argparse
import difflib
import os
import re
import sys
from pathlib import Path

import yaml

TEMPLATE = 'templates/CLAUDE-tmp.md'
LOCAL_SLOT = '{CLAUDE-local}'
TOP_SLOT = '{CLAUDE-local-top}'
CHORE = '{keepEnglishChore}'
WORDS = '> Technical words: '
LITERAL = re.compile(r'\{\{([^{}]+)\}\}')
GROUP = re.compile(r'\{skillGroups\.(\w+)\}')
LINK_GROUP = re.compile(r'\]\(\{skillGroups\.(\w+)\}')


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    sys.exit(2)


def read(path: Path) -> str:
    if not path.is_file():
        fail(f'{path}: no such file')
    return path.read_bytes().decode('utf-8')


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
    common = Path(os.path.expanduser(groups['common']))
    template = read((common if common.is_absolute() else root / common) / TEMPLATE)
    local = read(root / 'CLAUDE-local.md')

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
    missing = sorted({m.group(1) for m in GROUP.finditer(text)} - groups.keys())
    if missing:
        fail(f'the template uses skillGroups.{", skillGroups.".join(missing)}, which config.yaml does not set')
    text = LINK_GROUP.sub(lambda m: '](' + link_base(groups[m.group(1)], root), text)
    text = GROUP.sub(lambda m: groups[m.group(1)], text).replace('{agencyName}', root.name)
    return re.sub(r'\0(\d+)\0', lambda m: '{' + kept[int(m.group(1))] + '}', text)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--root', type=Path, default=Path('.'), help='the root of the workspace (default: .)')
    ap.add_argument('--check', action='store_true', help='compare CLAUDE.md with what would be written; write nothing')
    a = ap.parse_args()

    root = a.root.resolve()
    text = render(root)
    target = root / 'CLAUDE.md'
    now = target.read_bytes().decode('utf-8') if target.is_file() else ''
    if not a.check:
        if now != text:
            target.write_bytes(text.encode('utf-8'))
        print(f'CLAUDE.md: {"written" if now != text else "unchanged"}')
        return
    if now == text:
        print('CLAUDE.md: PASS - it is what the template, CLAUDE-local.md and config.yaml make')
        return
    sys.stdout.writelines(difflib.unified_diff(now.splitlines(True), text.splitlines(True),
                                               'CLAUDE.md', 'CLAUDE.md from the template'))
    print('\nCLAUDE.md: FAIL - it is not what the template, CLAUDE-local.md and config.yaml make.'
          '\nChange the template or CLAUDE-local.md, not CLAUDE.md, and then run gen_claude_md.py without --check.')
    sys.exit(1)


if __name__ == '__main__':
    main()
