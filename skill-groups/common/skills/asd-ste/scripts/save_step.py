#!/usr/bin/env python3
"""The step saver of the asd-ste skill: the Run Number, the step files and the run record of a run.

run-data-rules.md gives the shape. A run has a Run Number, {yymmdd}.{N}; its Checkpoint Dir is
checkpoints/asd-ste/{yymmdd}.{N}/ under the workspace root, and each step writes its outputs there in a
step file of its own, step_{N}.yaml; its run record is database/skill-runs/asd-ste/{yymmdd}.{N}.yaml,
with the fields skill, run, prompt, result, stopped_at and steps, and one item in steps - step, title,
model and time (begin, end, taken) - for each step that ran.

  --new-run  Step 0 gets the Run Number: the largest {N} of today in database/skill-runs/asd-ste/, plus
             1. The run record is written at once - created only if no file has that name, so two
             runs cannot get the same number - and the Checkpoint Dir is made. Prints, as JSON, the run,
             the Checkpoint Dir and the run record. Takes --prompt, the canonical skill invocation.
  --run      the Run Number of the run whose step is saved: writes step_{N}.yaml in its Checkpoint Dir,
             replacing the one an earlier save of the same step wrote, and adds the step to the steps of
             the run record - a step run again is added again, as run step N adds it.
  --begin    when the step began, read from the system clock as it began:
             date '+%Y-%m-%d %H:%M:%S'. The end is read from the clock when this script runs, as
             the step ends, and the time taken is worked out from the two, never estimated.
  --summary  a findings file of check_ste.py: the step file gets its path, as findings_file, and its
             verdict, failed and exit_status - never the findings themselves, which stay in that file.
  --set      key=value, the value as text.
  --json     key=value, the value as JSON: true, 3, ["a", "b"], {"hash": "1a2b3c4"}.
  --stopped  why the run stopped in this step: a refused source, a NOT-ENGLISH verdict, a no. The step
             file gets it as stopped, and the run record gets result: stopped and stopped_at.
  --last     the last step of the run: the run record gets result: completed.

The workspace root is the root of the workspace the skill runs in: the directory --root names, or else
the nearest directory, from the current directory up, whose config.yaml has skillGroups - the workspace
configuration, which names the skill groups the workspace reads. It is never found from this file: a
workspace can read a skill group in place from a different workspace, and then the config.yaml above
this file is that other workspace's, so the Run Number, the step files and the run record would land
there. The walk goes up, so a run from a directory below the root still finds the root, and the
skillGroups key passes over a config.yaml below the root that is not the workspace configuration.
draft.py finds the root with workspace_root from here; its recheck saves a step of a run in the
workspace of a draft, and gives save() the root of that workspace itself.

Usage:
  python save_step.py --new-run --prompt "<canonical skill invocation>"
  python save_step.py --run <yymmdd.N> --step N --title "<title>" --model "<model>" --begin "<time>"
                      [--summary <findings json>] [--set key=value]... [--json key=value]...
                      [--stopped "<why>"] [--last]

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

SKILL = 'asd-ste'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
RUN_RE = re.compile(r'^(\d{6})\.(\d+)$')
SUMMARY_KEYS = ('verdict', 'failed', 'exit_status')
WORKSPACE_HELP = ('the root of the workspace the skill runs in (default: the nearest directory, '
                  'from the current directory up, whose config.yaml has skillGroups)')


class Dumper(yaml.SafeDumper):
    """YAML that writes a text of several lines as a block, the way it reads: the prompt, a sentence."""


def text_block(dumper: yaml.SafeDumper, value: str) -> yaml.ScalarNode:
    return dumper.represent_scalar('tag:yaml.org,2002:str', value, style='|' if '\n' in value else None)


Dumper.add_representer(str, text_block)


class SaveError(Exception):
    """A save that cannot be made: exit status 2."""


def fail(message: str) -> None:
    print(f'error: {message}', file=sys.stderr)
    sys.exit(2)


def workspace_config(d: Path) -> dict | None:
    """The workspace configuration in d: its config.yaml when that has a skillGroups mapping, else None."""
    cfg = d / 'config.yaml'
    if not cfg.is_file():
        return None
    try:
        doc = yaml.safe_load(cfg.read_text(encoding='utf-8'))
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return None
    return doc if isinstance(doc, dict) and isinstance(doc.get('skillGroups'), dict) else None


def workspace_root(explicit: str | Path | None = None) -> Path:
    """The root of the workspace the skill runs in: --root, or else the nearest directory, from the
    current directory up, whose config.yaml has skillGroups - never found from this file."""
    if explicit:
        root = Path(explicit).expanduser().resolve()
        if workspace_config(root) is None:
            raise SaveError(f'{explicit} is not the root of a workspace: {root} holds no config.yaml '
                            'with skillGroups - name the root of the workspace the skill runs in')
        return root
    here = Path.cwd().resolve()
    root = next((d for d in [here, *here.parents] if workspace_config(d) is not None), None)
    if root is None:
        raise SaveError(f'no config.yaml with skillGroups in {here} or in a directory above it - '
                        'run from the workspace the skill runs in, or name its root')
    return root


def checkpoint_dir(root: Path, run: str) -> Path:
    return root / 'checkpoints' / SKILL / run


def run_record(root: Path, run: str) -> Path:
    return root / 'database' / 'skill-runs' / SKILL / f'{run}.yaml'


def dump(value) -> str:
    return yaml.dump(value, Dumper=Dumper, sort_keys=False, allow_unicode=True, width=1000)


def new_run(root: Path, prompt: str) -> dict:
    """Get the Run Number of a new run, write its run record at once, and make its Checkpoint Dir."""
    today = datetime.date.today().strftime('%y%m%d')
    records = root / 'database' / 'skill-runs' / SKILL
    records.mkdir(parents=True, exist_ok=True)
    used = [int(m.group(2)) for p in [*records.glob(f'{today}.*.yaml'),
                                      *(root / 'checkpoints' / SKILL).glob(f'{today}.*')]
            if (m := RUN_RE.match(p.name[:-len('.yaml')] if p.suffix == '.yaml' else p.name)) and m.group(1) == today]
    n = max(used, default=0) + 1
    while True:
        run = f'{today}.{n}'
        try:
            with run_record(root, run).open('x', encoding='utf-8') as f:
                f.write(dump({'skill': SKILL, 'run': run, 'prompt': prompt, 'result': 'stopped', 'stopped_at': 'step_0', 'steps': []}))
            break
        except FileExistsError:   # another run took the number between the look and the write
            n += 1
    checkpoint_dir(root, run).mkdir(parents=True, exist_ok=True)
    return {'run': run,
            'checkpoint_dir': checkpoint_dir(root, run).relative_to(root).as_posix(),
            'run_record': run_record(root, run).relative_to(root).as_posix()}


def summary_of(path: Path, folder: Path, root: Path) -> dict:
    """The path of a findings file and its verdict, as a step file holds them."""
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as e:
        raise SaveError(f'cannot read {path}: {e}')
    if not isinstance(data, dict):
        raise SaveError(f'{path} does not hold a JSON object')
    resolved = path.resolve()
    try:
        shown = resolved.relative_to(folder.resolve()).as_posix()
    except ValueError:
        try:
            shown = resolved.relative_to(root).as_posix()
        except ValueError:
            shown = str(path)
    return {'findings_file': shown, **{k: data[k] for k in SUMMARY_KEYS if k in data}}


def save(root: Path, run: str, step: int, title: str, model: str, begin: str, outputs: dict,
         stopped: str | None = None, last: bool = False) -> dict:
    """Write step_{step}.yaml with the outputs, and add the step to the run record."""
    if not RUN_RE.match(run):
        raise SaveError(f'--run is {{yymmdd}}.{{N}}, not {run!r}')
    try:
        start = datetime.datetime.strptime(begin, TIME_FORMAT)
    except ValueError:
        raise SaveError(f'--begin is {TIME_FORMAT}, not {begin!r}')
    record_path = run_record(root, run)
    if not record_path.is_file():
        raise SaveError(f'no run record {record_path}: Step 0 gets the Run Number with --new-run')
    try:
        record = yaml.safe_load(record_path.read_text(encoding='utf-8')) or {}
    except (OSError, yaml.YAMLError) as e:
        raise SaveError(f'cannot read {record_path}: {e}')
    if not isinstance(record, dict):
        raise SaveError(f'{record_path} does not hold a mapping')
    end = datetime.datetime.now().replace(microsecond=0)
    seconds = max(0, int((end - start).total_seconds()))
    item = {'step': step, 'title': title, 'model': model,
            'time': {'begin': begin, 'end': end.strftime(TIME_FORMAT), 'taken': f'{seconds // 60}m {seconds % 60}s'}}
    data = dict(outputs)
    if stopped:
        data['stopped'] = stopped
    folder = checkpoint_dir(root, run)
    folder.mkdir(parents=True, exist_ok=True)
    step_file = folder / f'step_{step}.yaml'
    step_file.write_text(dump(data) if data else '{}\n', encoding='utf-8')
    steps = record.get('steps') or []
    steps.append(item)
    out = {'skill': record.get('skill', SKILL), 'run': record.get('run', run), 'prompt': record.get('prompt', '')}
    if stopped:   # the run stops in this step: this step did not complete
        out.update({'result': 'stopped', 'stopped_at': f'step_{step}'})
    elif last:
        out['result'] = 'completed'
    else:   # until the last step, the record says where an interrupted run stops: at the next step
        out.update({'result': 'stopped', 'stopped_at': f'step_{step + 1}'})
    out['steps'] = steps
    record_path.write_text(dump(out), encoding='utf-8')
    return {'step_file': step_file, 'run_record': record_path, 'time': item['time']}


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


def main() -> None:
    ap = argparse.ArgumentParser(description='The Run Number, the step files and the run record of a run.')
    ap.add_argument('--new-run', action='store_true', help='get the Run Number, and write the run record')
    ap.add_argument('--prompt', help='with --new-run: the canonical skill invocation')
    ap.add_argument('--run', help='the Run Number, {yymmdd}.{N}')
    ap.add_argument('--step', type=int)
    ap.add_argument('--title', help="the step's heading, without its number")
    ap.add_argument('--model', help='the AI model that operated the step')
    ap.add_argument('--begin', help='when the step began, as ' + TIME_FORMAT.replace('%', '%%'))
    ap.add_argument('--summary', type=Path, help='a findings file: its path and verdict go into the step file')
    ap.add_argument('--set', action='append', default=[], metavar='KEY=VALUE', help='a value as text')
    ap.add_argument('--json', action='append', default=[], metavar='KEY=VALUE', help='a value as JSON')
    ap.add_argument('--stopped', help='why the run stopped in this step')
    ap.add_argument('--last', action='store_true', help='the last step: result completed')
    ap.add_argument('--root', type=Path, help=WORKSPACE_HELP)
    a = ap.parse_args()
    try:
        root = workspace_root(a.root)
        if a.new_run:
            if a.prompt is None:
                fail('--new-run needs --prompt, the canonical skill invocation')
            print(json.dumps(new_run(root, a.prompt), ensure_ascii=False, indent=1))
            return
        missing = [n for n in ('run', 'step', 'title', 'model', 'begin') if getattr(a, n) is None]
        if missing:
            fail('a save needs ' + ', '.join(f'--{n}' for n in missing))
        outputs = summary_of(a.summary, checkpoint_dir(root, a.run), root) if a.summary else {}
        given = {**pairs(a.set, str), **pairs(a.json, json.loads)}
        clash = sorted(set(given) & set(outputs))
        if clash:   # a value given by hand would silently replace one the summary holds
            fail(f'{", ".join(clash)} given twice: in --summary, and in --set or --json')
        outputs.update(given)
        done = save(root, a.run, a.step, a.title, a.model, a.begin, outputs, a.stopped, a.last)
    except SaveError as e:
        fail(str(e))
    t = done['time']
    print(f"saved step_{a.step} ({a.title}) of run {a.run}: {done['step_file'].relative_to(root).as_posix()}, "
          f"added to {done['run_record'].relative_to(root).as_posix()}: {t['begin']} to {t['end']}, {t['taken']}")


if __name__ == '__main__':
    main()
