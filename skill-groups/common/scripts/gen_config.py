#!/usr/bin/env python3
"""Make the config.yaml of a workspace from its shared template and the values of this computer, then AGENTS.md.

A workspace that is cloned on more than one computer cannot keep config.yaml in git: its paths name the home
folder of one computer, and a pull on a different computer writes over that computer's own paths. So the
shared part goes into git as a template, the part of each computer stays out of git, and this script puts
the two together:

  config.shared.yaml  the shared settings, in git; a value of this computer is written {name}
  config.local.yaml   the values of this computer, not in git: a mapping of names to values,
                      such as  home: D:/Work
  config.yaml         what this script writes - read by the skills and the scripts, never edited, not in git

config.shared.yaml is read as text, not as YAML, so that its comments and its order go into config.yaml as they
are; each {name} is replaced by the value of name in config.local.yaml, as written there, and {{name}} by
{name}, as it is. A line that starts with # is a comment, and stays as it is, so that a comment can name a
placeholder; a comment at the end of a line is replaced as the line is. The result must be valid YAML. A {name} that config.local.yaml does not have is an error;
a name of config.local.yaml that config.shared.yaml does not use is only told. A value is put into the text as
it is: write paths with / or in single quotes, as the line of config.shared.yaml needs.

config.yaml starts with a comment line that names the two files. Then, in the same run, the script runs
gen_agents_md.py with the same --root and --check, because AGENTS.md takes its paths from config.yaml.
A workspace without config.shared.yaml keeps its config.yaml as it is, and the script only runs
gen_agents_md.py; so each workspace can run this one command.

  (no flag)  write config.yaml, then AGENTS.md and CLAUDE.md
  --check    write nothing; compare config.yaml, AGENTS.md and CLAUDE.md with what would be written

Run it from the root of the workspace after a change to config.shared.yaml, to config.local.yaml, to the
template of AGENTS.md or to AGENTS.shared.md. Each file is read with its CRLF line ends made LF; config.yaml
is written with LF. Exit status: 0 the files are written, or are already what it would write; 1 under
--check, one is not; 2 a file is missing or unreadable, config.local.yaml is not a mapping of names to
values, config.shared.yaml uses a name that config.local.yaml does not have, or the result is not valid YAML.
"""
from __future__ import annotations

import argparse
import difflib
import re
import subprocess
import sys
from pathlib import Path

import yaml

TEMPLATE = 'config.shared.yaml'
LOCAL = 'config.local.yaml'
TARGET = 'config.yaml'
HEADER = f'# Made by gen_config.py from {TEMPLATE} and {LOCAL}. Do not change this file: change those two, and run gen_config.py.\n'
PLACEHOLDER = re.compile(r'\{\{(\w+)\}\}|\{(\w+)\}')
NAME = re.compile(r'^\w+$')


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    sys.exit(2)


def read(path: Path) -> str:
    if not path.is_file():
        fail(f'{path}: no such file')
    try:
        return path.read_bytes().decode('utf-8').replace('\r\n', '\n')
    except (OSError, UnicodeDecodeError) as e:
        fail(f'{path}: cannot read it: {e}')


def load_values(path: Path) -> dict[str, str]:
    try:
        data = yaml.safe_load(read(path))
    except yaml.YAMLError as e:
        fail(f'{path}: not valid YAML: {e}')
    if data is None:
        return {}
    if not isinstance(data, dict):
        fail(f'{path}: it must be a mapping of names to values, such as  home: D:/Work')
    values = {}
    for k, v in data.items():
        if not isinstance(k, str) or not NAME.match(k):
            fail(f'{path}: {k!r} is not a name: use only letters, digits and _')
        if isinstance(v, (dict, list)) or v is None:
            fail(f'{path}: {k} must have one value, not {"nothing" if v is None else type(v).__name__}')
        values[k] = str(v)
    return values


def render(root: Path) -> str:
    template = read(root / TEMPLATE)
    values = load_values(root / LOCAL)
    used: set[str] = set()
    missing: list[str] = []

    def replace(m: re.Match) -> str:
        if m.group(1):
            return '{' + m.group(1) + '}'
        name = m.group(2)
        if name not in values:
            missing.append(name)
            return m.group(0)
        used.add(name)
        return values[name]

    text = '\n'.join(line if line.lstrip().startswith('#') else PLACEHOLDER.sub(replace, line)
                     for line in template.split('\n'))
    if missing:
        fail(f'{root / TEMPLATE} uses {", ".join(sorted(set(missing)))}, which {LOCAL} does not have')
    for name in sorted(values.keys() - used):
        print(f'{LOCAL}: {name} is not used in {TEMPLATE}')
    try:
        yaml.safe_load(text)
    except yaml.YAMLError as e:
        fail(f'{TARGET} that {TEMPLATE} and {LOCAL} make is not valid YAML: {e}')
    return HEADER + text


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--root', type=Path, default=Path('.'), help='the root of the workspace (default: .)')
    ap.add_argument('--check', action='store_true', help='compare config.yaml, AGENTS.md and CLAUDE.md with what would be written; write nothing')
    a = ap.parse_args()

    root = a.root.resolve()
    failed = False
    if not (root / TEMPLATE).is_file():
        print(f'{TARGET}: kept as it is - there is no {TEMPLATE}')
    else:
        text = render(root)
        target = root / TARGET
        now = target.read_bytes().decode('utf-8').replace('\r\n', '\n') if target.is_file() else ''
        if not a.check:
            if now != text:
                target.write_bytes(text.encode('utf-8'))
            print(f'{TARGET}: {"written" if now != text else "unchanged"}')
        elif now == text:
            print(f'{TARGET}: PASS - it is what {TEMPLATE} and {LOCAL} make')
        else:
            sys.stdout.writelines(difflib.unified_diff(now.splitlines(True), text.splitlines(True),
                                                       TARGET, f'{TARGET} from {TEMPLATE}'))
            print(f'\n{TARGET}: FAIL - it is not what {TEMPLATE} and {LOCAL} make.')
            print(f'Change {TEMPLATE} or {LOCAL}, not {TARGET}, and then run gen_config.py without --check.')
            failed = True
    sys.stdout.flush()

    command = [sys.executable, str(Path(__file__).with_name('gen_agents_md.py')), '--root', str(root)]
    code = subprocess.run(command + (['--check'] if a.check else [])).returncode
    if code == 2:
        sys.exit(2)
    if failed or code:
        sys.exit(1)


if __name__ == '__main__':
    main()
