"""List the old items of checkpoints\\, and move the items that the user confirms to the recycle bin.

An item is each folder or file directly in checkpoints\\{skill}\\, and each file directly in checkpoints\\.
The date of an item is the date of its newest file.

    python clean_checkpoints.py list    --run 261112.1 [--root DIR]
    python clean_checkpoints.py recycle --run 261112.1 [--root DIR]

list     writes items.yaml in the Working Dir temp\\clean-checkpoints\\{run}\\: the size of checkpoints\\,
         the settings, and each item with its verdict, clean or keep, and the reason.
recycle  reads the confirmed list of step_2.yaml in the same Working Dir, classifies each item again,
         and moves only the items that are still clean to the recycle bin; it writes recycled.yaml.
         It never removes an item permanently.

The settings are the cleanCheckpoints block of config.yaml at the root, and the top-level keys
tasksDir and taskSummary. Without a key, the default applies: maxSizeGB 10, keepDays 60, keep [].
Only the Python standard library is used, so the script runs without a .venv.

Exit codes: 0 done; 2 a usage, root or config problem; 3 no recycle bin on this system; 4 a move failed.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

SKILL = 'clean-checkpoints'
DEFAULTS = {'maxSizeGB': 10.0, 'keepDays': 60, 'keep': []}
OPEN_ICONS = ('⬜', '🔄')
TASK_LINK_RE = re.compile(r'\[\[(Task [0-9.]+)\]\]')
NUMBER_RE = re.compile(r'\d{7,}')  # 7 or more: a 6-digit number is frequently a date, yymmdd
RUN_RE = re.compile(r'^\d{6}\.\d+$')


def fail(message: str, code: int = 2) -> None:
    print(message, file=sys.stderr)
    sys.exit(code)


def find_root(given: str | None) -> Path:
    """The root of the workspace: --root, or the nearest directory up with a config.yaml that has skillGroups."""
    if given:
        root = Path(given).resolve()
        if not (root / 'config.yaml').is_file():
            fail(f'{root}: no config.yaml')
        return root
    here = Path.cwd().resolve()
    for d in (here, *here.parents):
        c = d / 'config.yaml'
        if c.is_file() and re.search(r'^skillGroups:', c.read_text(encoding='utf-8-sig'), re.M):
            return d
    fail(f'{here}: no config.yaml with skillGroups in this directory or above it')
    raise AssertionError


def scalar(value: str) -> str:
    return value.strip().strip('"\'')


def read_config(root: Path) -> dict:
    """The settings of this skill. Read by hand: the cleanCheckpoints block, tasksDir and taskSummary."""
    text = (root / 'config.yaml').read_text(encoding='utf-8-sig')
    found: dict = {}
    top: dict[str, str] = {}
    inside = False
    in_keep = False
    for line in text.split('\n'):
        bare = re.sub(r'\s+#.*$', '', line).rstrip()
        if not bare or bare.lstrip().startswith('#'):
            continue
        if not bare.startswith((' ', '\t')):
            inside = bare == 'cleanCheckpoints:'
            in_keep = False
            if ':' in bare and not inside:
                k, v = bare.split(':', 1)
                top[k.strip()] = scalar(v)
            continue
        if not inside:
            continue
        item = bare.strip()
        if item.startswith('- '):
            if not in_keep:
                fail(f'config.yaml: cleanCheckpoints: a list item outside keep: "{item}"')
            found['keep'].append(scalar(item[2:]))
            continue
        if ':' not in item:
            fail(f'config.yaml: cleanCheckpoints: cannot read "{item}"')
        k, v = (x.strip() for x in item.split(':', 1))
        in_keep = False
        if k in found:
            fail(f'config.yaml: cleanCheckpoints: {k} is set two times')
        if k == 'keep':
            if v.startswith('['):
                if not v.endswith(']'):
                    fail('config.yaml: cleanCheckpoints: keep must be [a, b] or a list of "- a" lines')
                found['keep'] = [scalar(x) for x in v[1:-1].split(',') if scalar(x)]
            elif v:
                fail('config.yaml: cleanCheckpoints: keep must be [a, b] or a list of "- a" lines')
            else:
                found['keep'] = []
                in_keep = True
        elif k == 'maxSizeGB':
            try:
                found[k] = float(scalar(v))
            except ValueError:
                fail(f'config.yaml: cleanCheckpoints: maxSizeGB is not a number: {v}')
            if found[k] <= 0:
                fail('config.yaml: cleanCheckpoints: maxSizeGB must be more than 0')
        elif k == 'keepDays':
            if not scalar(v).isdigit():
                fail(f'config.yaml: cleanCheckpoints: keepDays is not a whole number: {v}')
            found[k] = int(scalar(v))
        else:
            fail(f'config.yaml: cleanCheckpoints: unknown key {k}; the keys are maxSizeGB, keepDays and keep')
    settings = {**DEFAULTS, **found}
    settings['defaults'] = sorted(k for k in DEFAULTS if k not in found)

    def path_of(key: str) -> Path | None:
        if not top.get(key):
            return None
        p = Path(os.path.expanduser(top[key]))
        return p if p.is_absolute() else root / p

    settings['tasksDir'] = path_of('tasksDir')
    settings['taskSummary'] = path_of('taskSummary')
    return settings


def open_task_texts(settings: dict) -> tuple[dict[str, str] | None, str]:
    """The text of each task with ⬜ or 🔄 in the summary table, or None and the cause."""
    tasks_dir, summary = settings['tasksDir'], settings['taskSummary']
    if tasks_dir is None or summary is None:
        return None, 'config.yaml has no tasksDir or no taskSummary'
    if not summary.is_file() or not tasks_dir.is_dir():
        return None, f'{summary if not summary.is_file() else tasks_dir} is not there'
    texts: dict[str, str] = {}
    for line in summary.read_text(encoding='utf-8-sig').split('\n'):
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 4 or not any(i in cells[3] for i in OPEN_ICONS):
            continue
        m = TASK_LINK_RE.search(cells[0])
        if m:
            f = tasks_dir / f'{m.group(1)}.md'
            if f.is_file():
                texts[m.group(1)] = f.read_text(encoding='utf-8-sig')
    return texts, ''


def measure(path: Path) -> tuple[int, float]:
    """The size in bytes, and the time of the newest file (the item itself for an empty folder)."""
    if path.is_file():
        st = path.stat()
        return st.st_size, st.st_mtime
    total, newest = 0, path.stat().st_mtime
    first = True
    for d, _, files in os.walk(path):
        for f in files:
            try:
                st = os.stat(os.path.join(d, f))
            except OSError:
                continue
            total += st.st_size
            newest = st.st_mtime if first else max(newest, st.st_mtime)
            first = False
    return total, newest


def items_of(checkpoints: Path) -> list[tuple[str, Path]]:
    """Each item, with its path relative to checkpoints\\ in forward slashes."""
    out: list[tuple[str, Path]] = []
    for top in sorted(checkpoints.iterdir(), key=lambda p: p.name.lower()):
        if top.is_dir():
            for child in sorted(top.iterdir(), key=lambda p: p.name.lower()):
                out.append((f'{top.name}/{child.name}', child))
        else:
            out.append((top.name, top))
    return out


def classify(root: Path, settings: dict) -> dict:
    checkpoints = root / 'checkpoints'
    if not checkpoints.is_dir():
        return {'checkpoints': checkpoints, 'total': 0, 'items': [], 'tasks': None, 'tasksNote': 'no checkpoints\\'}
    texts, note = open_task_texts(settings)
    today = date.today()
    items, total = [], 0
    keep = set(settings['keep'])
    for rel, path in items_of(checkpoints):
        size, newest = measure(path)
        total += size
        age = (today - date.fromtimestamp(newest)).days
        name = path.name
        stem = path.stem if path.is_file() else name
        skill = rel.split('/')[0] if '/' in rel else ''
        reason, verdict = '', 'keep'
        hits: list[str] = []
        if texts:
            numbers = NUMBER_RE.findall(name)
            for task, text in texts.items():
                if name in text or (stem and stem != name and stem in text) or any(n in text for n in numbers):
                    hits.append(task)
        if skill == 'chores':
            reason = 'checkpoints\\chores\\ is for the chores'
        elif skill in keep:
            reason = f'{skill} is in keep'
        elif hits:
            reason = 'in an open task: ' + ', '.join(hits)
        elif age <= settings['keepDays']:
            reason = f'newest file is {age} days old'
        else:
            verdict, reason = 'clean', f'newest file is {age} days old, more than {settings["keepDays"]}'
        items.append({'path': rel, 'bytes': size, 'newest': date.fromtimestamp(newest).isoformat(),
                      'ageDays': age, 'verdict': verdict, 'reason': reason})
    return {'checkpoints': checkpoints, 'total': total, 'items': items,
            'tasks': None if texts is None else len(texts), 'tasksNote': note}


def q(value) -> str:
    """A YAML scalar: JSON is a subset of YAML, so json.dumps quotes a string safely."""
    if isinstance(value, bool) or value is None:
        return json.dumps(value)
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)


def working_dir(root: Path, run: str) -> Path:
    if not RUN_RE.match(run):
        fail(f'--run must be the Run Number {{yymmdd}}.{{N}}, for example 261112.1: {run}')
    d = root / 'temp' / SKILL / run
    d.mkdir(parents=True, exist_ok=True)
    return d


def gb(n: int) -> str:
    return f'{n / 1024 ** 3:.2f}'


def cmd_list(args) -> None:
    root = find_root(args.root)
    settings = read_config(root)
    wd = working_dir(root, args.run)
    r = classify(root, settings)
    limit = int(settings['maxSizeGB'] * 1024 ** 3)
    over = r['total'] > limit
    clean = [i for i in r['items'] if i['verdict'] == 'clean']
    lines = [
        f'checkpoints: {q(r["checkpoints"].as_posix())}',
        f'measured: {q(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}',
        f'totalBytes: {r["total"]}',
        f'totalGB: {gb(r["total"])}',
        f'maxSizeGB: {q(settings["maxSizeGB"])}',
        f'overThreshold: {q(over)}',
        f'keepDays: {settings["keepDays"]}',
        'keep: [' + ', '.join(q(k) for k in settings['keep']) + ']',
        'defaults: [' + ', '.join(settings['defaults']) + ']',
        f'openTasks: {q(r["tasks"])}',
        f'openTasksNote: {q(r["tasksNote"])}',
        f'cleanCount: {len(clean)}',
        f'cleanBytes: {sum(i["bytes"] for i in clean)}',
        f'cleanGB: {gb(sum(i["bytes"] for i in clean))}',
        'items:' + ('' if r['items'] else ' []'),
    ]
    for i in r['items']:
        lines.append(f'  - path: {q(i["path"])}')
        for k in ('bytes', 'newest', 'ageDays', 'verdict', 'reason'):
            lines.append(f'    {k}: {q(i[k])}')
    out = wd / 'items.yaml'
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'checkpoints\\ is {gb(r["total"])} GB; the threshold is {settings["maxSizeGB"]} GB: '
          f'{"over" if over else "not over"}')
    print(f'{len(r["items"])} items, {len(clean)} to clean ({gb(sum(i["bytes"] for i in clean))} GB)')
    if r['tasks'] is None:
        print(f'open tasks not checked: {r["tasksNote"]}')
    if settings['defaults']:
        print('defaults used for: ' + ', '.join(settings['defaults']))
    print(out)


def read_confirmed(step2: Path) -> list[str]:
    """The paths of the confirmed list of step_2.yaml: each "- path" line under "confirmed:"."""
    if not step2.is_file():
        fail(f'{step2}: not there; Step 2 writes it')
    paths, inside = [], False
    for line in step2.read_text(encoding='utf-8-sig').split('\n'):
        bare = re.sub(r'\s+#.*$', '', line).rstrip()
        if not bare:
            continue
        if not bare.startswith((' ', '\t', '-')):
            inside = bare.startswith('confirmed:')
            if inside and bare.split(':', 1)[1].strip() == '[]':
                inside = False
            continue
        if inside and bare.strip().startswith('- '):
            value = bare.strip()[2:].strip()
            if value.startswith('"'):
                value = json.loads(value)
            paths.append(value.strip("'"))
    return paths


def to_recycle_bin(path: Path) -> str | None:
    """Move one item to the recycle bin. None when done, else the cause."""
    system = platform.system()
    if system == 'Windows':
        kind = 'DeleteDirectory' if path.is_dir() else 'DeleteFile'
        script = ('Add-Type -AssemblyName Microsoft.VisualBasic; '
                  f'[Microsoft.VisualBasic.FileIO.FileSystem]::{kind}($env:CLEAN_CHECKPOINTS_ITEM, '
                  "'OnlyErrorDialogs', 'SendToRecycleBin')")
        env = {**os.environ, 'CLEAN_CHECKPOINTS_ITEM': str(path)}
        p = subprocess.run(['powershell', '-NoProfile', '-NonInteractive', '-Command', script],
                           env=env, capture_output=True, text=True)
        if p.returncode != 0 or path.exists():
            return (p.stderr or p.stdout).strip() or 'the item is still there'
        return None
    from send2trash import send2trash  # checked in main before any move
    try:
        send2trash(str(path))
    except Exception as e:  # noqa: BLE001 - report each cause, and continue with the next item
        return str(e)
    return None


def cmd_recycle(args) -> None:
    root = find_root(args.root)
    settings = read_config(root)
    wd = working_dir(root, args.run)
    if platform.system() != 'Windows':
        try:
            import send2trash  # noqa: F401
        except ImportError:
            fail('no recycle bin: on this system the script needs the Python package send2trash. '
                 'Nothing was removed.', 3)
    confirmed = read_confirmed(wd / 'step_2.yaml')
    now = {i['path']: i for i in classify(root, settings)['items']}
    moved, skipped, failed = [], [], []
    for rel in confirmed:
        item = now.get(rel)
        if item is None:
            skipped.append((rel, 'not an item of checkpoints\\ now'))
        elif item['verdict'] != 'clean':
            skipped.append((rel, 'not clean now: ' + item['reason']))
        else:
            cause = to_recycle_bin(root / 'checkpoints' / Path(rel))
            if cause:
                failed.append((rel, cause))
            else:
                moved.append(item)
    lines = [f'confirmed: {len(confirmed)}',
             f'movedCount: {len(moved)}',
             f'movedBytes: {sum(i["bytes"] for i in moved)}',
             f'movedGB: {gb(sum(i["bytes"] for i in moved))}',
             'moved:' + ('' if moved else ' []')]
    lines += [f'  - path: {q(i["path"])}\n    bytes: {i["bytes"]}\n    newest: {q(i["newest"])}' for i in moved]
    for name, rows in (('skipped', skipped), ('failed', failed)):
        lines.append(f'{name}:' + ('' if rows else ' []'))
        lines += [f'  - path: {q(p)}\n    cause: {q(c)}' for p, c in rows]
    out = wd / 'recycled.yaml'
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'moved {len(moved)} of {len(confirmed)} items to the recycle bin '
          f'({gb(sum(i["bytes"] for i in moved))} GB); skipped {len(skipped)}, failed {len(failed)}')
    for p, c in skipped + failed:
        print(f'  {p}: {c}')
    print(out)
    if failed:
        sys.exit(4)


def main() -> None:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='command', required=True)
    for name, fn in (('list', cmd_list), ('recycle', cmd_recycle)):
        p = sub.add_parser(name)
        p.add_argument('--run', required=True, help='the Run Number, {yymmdd}.{N}')
        p.add_argument('--root', help='the root of the workspace; without it, found from the current directory')
        p.set_defaults(fn=fn)
    args = ap.parse_args()
    args.fn(args)


if __name__ == '__main__':
    main()
