#!/usr/bin/env python3
"""Save one step's group into the YAML checkpoint of the asd-ste skill.

The YAML checkpoint is `process.yaml` in the skill's Checkpoint Dir: one `step_{N}` group for each
step, as report-yaml-rules.md requires - the step's `title`, its `time` (begin, end, taken) and its
outputs. This script writes one group and leaves every other group as it is, so that each step owns
its own group, and a list too long to copy by hand - a findings file of check_ste.py - goes in whole.

  --begin    when the step began, read from the system clock as it began:
             date '+%Y-%m-%d %H:%M:%S'. The end is read from the clock when this script runs, as
             the step ends, and the time taken is worked out from the two, never estimated.
  --data     a JSON file whose keys go into the group, such as a findings file of check_ste.py.
  --set      key=value, the value as text.
  --json     key=value, the value as JSON: true, 3, ["a", "b"], {"hash": "1a2b3c4"}.
  --stopped  why the run stopped in this step: a refused source, a NOT-ENGLISH verdict, a no.
  --new      start the YAML checkpoint afresh, without the groups an earlier run left: Step 0 of a
             run, so that a Checkpoint Dir that every run reuses never mixes two runs.

Usage:
  python save_step.py --checkpoint <process.yaml> --step N --title "<title>" --begin "<time>"
                      [--new] [--data <json>] [--set key=value]... [--json key=value]... [--stopped "<why>"]

Needs PyYAML. Exit status: 0 saved; 2 a bad argument, or a file that cannot be read or parsed.
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

import yaml

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class Dumper(yaml.SafeDumper):
    """YAML that writes a text of several lines as a block, the way it reads: the prompt, a sentence."""


def text_block(dumper: yaml.SafeDumper, value: str) -> yaml.ScalarNode:
    return dumper.represent_scalar('tag:yaml.org,2002:str', value, style='|' if '\n' in value else None)


Dumper.add_representer(str, text_block)


def fail(message: str) -> None:
    print(f'error: {message}', file=sys.stderr)
    sys.exit(2)


def pairs(items: list[str], parse) -> dict:
    """key=value arguments as a mapping, each value read by `parse`."""
    out = {}
    for item in items:
        key, sep, value = item.partition('=')
        if not sep or not key.strip():
            fail(f'not key=value: {item}')
        try:
            out[key.strip()] = parse(value)
        except ValueError as e:
            fail(f'{key.strip()} is not JSON: {e}')
    return out


def step_number(key: str) -> int:
    m = re.fullmatch(r'step_(\d+)', key)
    return int(m.group(1)) if m else 10 ** 6


def main() -> None:
    ap = argparse.ArgumentParser(description="Save one step's group into the YAML checkpoint.")
    ap.add_argument('--checkpoint', type=Path, required=True, help='the process.yaml in the Checkpoint Dir')
    ap.add_argument('--step', type=int, required=True)
    ap.add_argument('--title', required=True, help="the step's heading, without its number")
    ap.add_argument('--begin', required=True, help=f'when the step began, as {TIME_FORMAT}')
    ap.add_argument('--new', action='store_true', help='start the YAML checkpoint afresh')
    ap.add_argument('--data', type=Path, help='a JSON file whose keys go into the group')
    ap.add_argument('--set', action='append', default=[], metavar='KEY=VALUE', help='a value as text')
    ap.add_argument('--json', action='append', default=[], metavar='KEY=VALUE', help='a value as JSON')
    ap.add_argument('--stopped', help='why the run stopped in this step')
    a = ap.parse_args()
    try:
        begin = datetime.datetime.strptime(a.begin, TIME_FORMAT)
    except ValueError:
        fail(f'--begin is {TIME_FORMAT}, not {a.begin!r}')
    end = datetime.datetime.now().replace(microsecond=0)
    seconds = max(0, int((end - begin).total_seconds()))
    group: dict = {'title': a.title,
                   'time': {'begin': a.begin, 'end': end.strftime(TIME_FORMAT),
                            'taken': f'{seconds // 60}m {seconds % 60}s'}}
    if a.data:
        try:
            data = json.loads(a.data.read_text(encoding='utf-8'))
        except (OSError, ValueError) as e:
            fail(f'cannot read {a.data}: {e}')
        if not isinstance(data, dict):
            fail(f'{a.data} does not hold a JSON object')
        group.update({k: v for k, v in data.items() if k not in ('title', 'time')})
    given = {**pairs(a.set, str), **pairs(a.json, json.loads)}
    clash = sorted(set(given) & set(group))
    if clash:   # a value given by hand would silently replace one the data file holds
        fail(f'{", ".join(clash)} given twice: in --data, and in --set or --json')
    group.update(given)
    if a.stopped:
        group['stopped'] = a.stopped
    process: dict = {}
    if a.checkpoint.exists() and not a.new:
        try:
            process = yaml.safe_load(a.checkpoint.read_text(encoding='utf-8')) or {}
        except (OSError, yaml.YAMLError) as e:
            fail(f'cannot read {a.checkpoint}: {e}')
        if not isinstance(process, dict):
            fail(f'{a.checkpoint} does not hold a mapping of step groups')
    process[f'step_{a.step}'] = group
    ordered = dict(sorted(process.items(), key=lambda kv: step_number(kv[0])))
    a.checkpoint.parent.mkdir(parents=True, exist_ok=True)
    a.checkpoint.write_text(yaml.dump(ordered, Dumper=Dumper, sort_keys=False, allow_unicode=True, width=1000),
                            encoding='utf-8')
    t = group['time']
    print(f"saved step_{a.step} ({a.title}) in {a.checkpoint}: {t['begin']} to {t['end']}, {t['taken']}")


if __name__ == '__main__':
    main()
