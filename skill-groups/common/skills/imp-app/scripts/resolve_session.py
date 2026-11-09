"""Resolve the imp-app session of one app: its Run Number, Checkpoint Dir and run record.

One app is one session spread over many invocations: the FIRST command run against an app gets a
Run Number, and every later command - whichever it is - reopens a run of that app: the run the user
names, or else the newest one. That is why this is a script and not a paragraph: two invocations
of one app must not be able to land in different directories.

The layout is the one run-data-rules.md gives:

- Checkpoint Dir  checkpoints\\imp-app\\{yymmdd}.{N}\\
- run record  database\\skill-runs\\imp-app\\{yymmdd}.{N}.yaml

A run belongs to an app when the `step_0.yaml` of its Checkpoint Dir carries `app: <name>`.
A Checkpoint Dir in the older `{app}-{yymmdd-hhmm}` form is not a run and is not reopened.

A new Run Number is the largest `{N}` of today in `database\\skill-runs\\imp-app\\`, plus 1. The
run record is written at once, with `skill` and `run`, so that a different run cannot take the
same number. Step 0 adds the prompt and its own step to it.

The workspace root is the root of the workspace the skill runs in: the directory `--workspace`
names, or else the nearest directory, from the current directory up, whose `config.yaml` has
`skillGroups` - the workspace configuration, which names the skill groups the workspace reads.

It is never found from this file. A workspace can read a skill group in place from a different
workspace, and then the `config.yaml` above this file is that other workspace's, with its own
`wikiDir`: the Run Number, the Checkpoint Dir, the run record and the MD report would all land in
the wrong workspace. The walk goes up, so a run from a directory below the root still finds the
root and makes no `checkpoints` there; the `skillGroups` key passes over the `config.yaml` of an
app dir or of a skill, which a workspace can hold below its root.

The test runner and the deploy tool find the root with `workspace_root` from here, so a relative
`--out` naming the Checkpoint Dir this script printed lands where it points.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml

SKILL = "imp-app"
COMMANDS = ("vibe", "reverse", "update", "test", "start", "deploy")
RUN_RE = re.compile(r"^(?P<date>\d{6})\.(?P<n>[1-9]\d*)$")
# The app name is the app dir's last path segment with a trailing -app stripped, spelled as the
# directory is. It names a document, so nothing but word characters and dashes.
APP_RE = re.compile(r"^[A-Za-z0-9]+([-_][A-Za-z0-9]+)*$")
WORKSPACE_HELP = ("the root of the workspace the skill runs in (default: the nearest directory, "
                  "from the current directory up, whose config.yaml has skillGroups)")


def workspace_config(d: Path) -> dict | None:
    """The workspace configuration in d: its config.yaml when that has a skillGroups mapping, else None."""
    cfg = d / "config.yaml"
    if not cfg.is_file():
        return None
    try:
        with open(cfg, encoding="utf-8") as fh:
            doc = yaml.safe_load(fh)
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return None
    return doc if isinstance(doc, dict) and isinstance(doc.get("skillGroups"), dict) else None


def workspace_root(explicit: str | None = None) -> Path:
    """The root of the workspace the skill runs in: --workspace, or else the nearest directory, from
    the current directory up, whose config.yaml has skillGroups - never found from this file."""
    if explicit:
        root = Path(explicit).expanduser().resolve()
        if workspace_config(root) is None:
            sys.exit(f"--workspace {explicit}: {root} holds no config.yaml with skillGroups; "
                     "name the root of the workspace the skill runs in")
        return root
    here = Path.cwd().resolve()
    for d in (here, *here.parents):
        if workspace_config(d) is not None:
            return d
    sys.exit(f"no config.yaml with skillGroups in {here} or in a directory above it; "
             "run from the workspace the skill runs in, or pass --workspace")


def run_key(run: str) -> tuple[str, int]:
    m = RUN_RE.match(run)
    return (m.group("date"), int(m.group("n")))


def app_runs(skill_ckpt: Path, app: str) -> list[str]:
    """The Run Numbers whose step_0.yaml names this app, oldest first."""
    runs: list[str] = []
    if not skill_ckpt.is_dir():
        return runs
    for d in skill_ckpt.iterdir():
        if not (d.is_dir() and RUN_RE.match(d.name)):
            continue
        step0 = d / "step_0.yaml"
        if not step0.is_file():
            continue
        try:
            with open(step0, encoding="utf-8") as fh:
                doc = yaml.safe_load(fh) or {}
        except yaml.YAMLError:
            continue
        if isinstance(doc, dict) and doc.get("app") == app:
            runs.append(d.name)
    runs.sort(key=run_key)
    return runs


def next_run(records_dir: Path, skill_ckpt: Path, today: str) -> str:
    """Today's largest N in the run records, plus 1 - also past a Checkpoint Dir already there."""
    largest = 0
    for base, suffix in ((records_dir, ".yaml"), (skill_ckpt, "")):
        if not base.is_dir():
            continue
        for p in base.iterdir():
            name = p.name[: -len(suffix)] if suffix and p.name.endswith(suffix) else p.name
            m = RUN_RE.match(name)
            if m and m.group("date") == today:
                largest = max(largest, int(m.group("n")))
    return f"{today}.{largest + 1}"


def main() -> None:
    ap = argparse.ArgumentParser(description="Resolve the imp-app session of one app.")
    ap.add_argument("--app", required=True, help="app name, e.g. InvCov")
    ap.add_argument("--command", required=True, choices=COMMANDS, help="the command being run")
    ap.add_argument("--run", help="reopen this run, {yymmdd}.{N}, instead of the newest run of the app")
    ap.add_argument("--new", action="store_true", help="get a new Run Number even though the app has a run")
    ap.add_argument("--workspace", help=WORKSPACE_HELP)
    ap.add_argument("--wiki-dir", help="override wikiDir instead of reading config.yaml")
    ap.add_argument("--dry-run", action="store_true",
                    help="print what would be resolved; create no directory and write no run record")
    args = ap.parse_args()

    if not APP_RE.match(args.app):
        sys.exit(f"app name '{args.app}' names a document; use letters, digits, - or _")
    if args.run and args.new:
        sys.exit("--run reopens a run and --new makes one; pass one of them")
    if args.run and not RUN_RE.match(args.run):
        sys.exit(f"'{args.run}' is not a Run Number; the form is {{yymmdd}}.{{N}}, e.g. 261106.1")

    root = workspace_root(args.workspace)
    skill_ckpt = root / "checkpoints" / SKILL
    records_dir = root / "database" / "skill-runs" / SKILL
    runs = app_runs(skill_ckpt, args.app)

    if args.run:
        if args.run not in runs:
            sys.exit(f"run {args.run} is not a run of {args.app}; its runs are: {', '.join(runs) or 'none'}")
        run, opened = args.run, "reopened"
    elif runs and not args.new:
        run, opened = runs[-1], "reopened"
    else:
        run, opened = next_run(records_dir, skill_ckpt, datetime.now().strftime("%y%m%d")), "created"

    ckpt_dir = skill_ckpt / run
    record = records_dir / f"{run}.yaml"

    if opened == "created" and not args.dry_run:
        ckpt_dir.mkdir(parents=True)
        records_dir.mkdir(parents=True, exist_ok=True)
        # Written at once, so that a different run cannot take the same number.
        with open(record, "x", encoding="utf-8") as fh:
            yaml.safe_dump({"skill": SKILL, "run": run, "result": "stopped", "stopped_at": "step_0", "steps": []}, fh, sort_keys=False, allow_unicode=True)

    wiki_dir = args.wiki_dir or (workspace_config(root) or {}).get("wikiDir")
    md_report = os.path.join(wiki_dir, SKILL, f"{SKILL}-{args.app}-{run}.md") if wiki_dir else None

    print(json.dumps({
        "workspace": root.as_posix(),
        "app": args.app,
        "command": args.command,
        "run": run,
        "checkpointDir": ckpt_dir.relative_to(root).as_posix(),
        "runRecord": record.relative_to(root).as_posix(),
        "mdReport": md_report,
        "opened": opened,
        "runs": runs,
        "dryRun": args.dry_run,
    }, indent=2))


if __name__ == "__main__":
    main()
