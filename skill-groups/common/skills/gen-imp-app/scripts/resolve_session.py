"""Resolve the gen-imp-app run of one app: its Run Number, Checkpoint Dir and run record.

The SOP is one run spread over several invocations. Step 1 gets a new Run Number, as
run-data-rules.md tells: the largest {N} of today in database/skill-runs/gen-imp-app/, plus 1. It
writes the run record at once, so a different run cannot get the same number. Steps 2 and 3
reopen the run that --run names, or else the newest run of the app. A run belongs to the app that
its step_0.yaml records.

The workspace root is the root of the workspace the skill runs in: the directory --workspace
names, or else the nearest directory, from the current directory up, whose config.yaml has
skillGroups - the workspace configuration, which names the skill groups the workspace reads.

It is never found from this file. A workspace can read a skill group in place from a different
workspace, and then the config.yaml above this file is that other workspace's, with its own
wikiDir: the Run Number, the Checkpoint Dir, the run record, the handoff file and the MD report
would all land in the wrong workspace. The walk goes up, so a run from a directory below the root
still finds the root and makes no checkpoints there; the skillGroups key passes over the
config.yaml of an app dir or of a skill, which a workspace can hold below its root.

The owner-skill checker finds the root with workspace_root from here, so a relative --out naming
the Checkpoint Dir lands in the one this script printed.
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime

import yaml

SKILL = "gen-imp-app"
RUN_RE = re.compile(r"^(?P<date>\d{6})\.(?P<n>[1-9]\d*)$")
RECORD_RE = re.compile(r"^(?P<date>\d{6})\.(?P<n>[1-9]\d*)\.yaml$")
WORKSPACE_HELP = ("the root of the workspace the skill runs in (default: the nearest directory, "
                  "from the current directory up, whose config.yaml has skillGroups)")


def workspace_config(d):
    """The workspace configuration in d: its config.yaml when that has a skillGroups mapping, else None."""
    cfg = os.path.join(d, "config.yaml")
    if not os.path.isfile(cfg):
        return None
    try:
        with open(cfg, encoding="utf-8") as fh:
            doc = yaml.safe_load(fh)
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return None
    return doc if isinstance(doc, dict) and isinstance(doc.get("skillGroups"), dict) else None


def workspace_root(explicit=None):
    """The root of the workspace the skill runs in: --workspace, or else the nearest directory, from
    the current directory up, whose config.yaml has skillGroups - never found from this file."""
    if explicit:
        root = os.path.realpath(os.path.expanduser(explicit))
        if workspace_config(root) is None:
            sys.exit(f"--workspace {explicit}: {root} holds no config.yaml with skillGroups; "
                     "name the root of the workspace the skill runs in")
        return root
    here = os.path.realpath(os.getcwd())
    d = here
    while True:
        if workspace_config(d) is not None:
            return d
        parent = os.path.dirname(d)
        if parent == d:
            sys.exit(f"no config.yaml with skillGroups in {here} or in a directory above it; "
                     "run from the workspace the skill runs in, or pass --workspace")
        d = parent


def run_key(run):
    m = RUN_RE.match(run)
    return (m.group("date"), int(m.group("n")))


def recorded_app(ckpt_dir):
    step0 = os.path.join(ckpt_dir, "step_0.yaml")
    if not os.path.isfile(step0):
        return None
    with open(step0, encoding="utf-8") as fh:
        return (yaml.safe_load(fh) or {}).get("app")


def list_runs(skill_ckpt, app):
    """The runs of this app, oldest first: each Checkpoint Dir whose step_0.yaml records the app."""
    out = []
    if not os.path.isdir(skill_ckpt):
        return out
    for name in os.listdir(skill_ckpt):
        path = os.path.join(skill_ckpt, name)
        if RUN_RE.match(name) and os.path.isdir(path) and recorded_app(path) == app:
            out.append(name)
    out.sort(key=run_key)
    return out


def new_run_number(records_dir):
    today = datetime.now().strftime("%y%m%d")
    largest = 0
    if os.path.isdir(records_dir):
        for name in os.listdir(records_dir):
            m = RECORD_RE.match(name)
            if m and m.group("date") == today:
                largest = max(largest, int(m.group("n")))
    return f"{today}.{largest + 1}"


def main():
    ap = argparse.ArgumentParser(description="Resolve the gen-imp-app run of one app.")
    ap.add_argument("--app", required=True, help="app name, e.g. redfish-test")
    ap.add_argument("--step", required=True, type=int, choices=(1, 2, 3),
                    help="step being run: 1 gets a new Run Number, 2 and 3 reopen a run")
    ap.add_argument("--run", help="reopen this Run Number, yymmdd.N, instead of the newest run of the app")
    ap.add_argument("--workspace", help=WORKSPACE_HELP)
    ap.add_argument("--wiki-dir", help="override wikiDir instead of reading config.yaml")
    args = ap.parse_args()

    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", args.app):
        sys.exit(f"app name '{args.app}' is not kebab-case; it names a directory and a skill")
    if args.run and not RUN_RE.match(args.run):
        sys.exit(f"run '{args.run}' is not a Run Number of the form yymmdd.N")

    root = workspace_root(args.workspace)
    skill_ckpt = os.path.join(root, "checkpoints", SKILL)
    records_dir = os.path.join(root, "database", "skill-runs", SKILL)
    runs = list_runs(skill_ckpt, args.app)

    if args.run:
        run_dir = os.path.join(skill_ckpt, args.run)
        if not os.path.isdir(run_dir):
            sys.exit(f"no run '{args.run}' under {skill_ckpt}")
        owner = recorded_app(run_dir)
        if owner is not None and owner != args.app:
            sys.exit(f"run '{args.run}' belongs to app '{owner}', not '{args.app}'")
        run = args.run
    elif args.step == 1:
        run = new_run_number(records_dir)
    elif runs:
        run = runs[-1]
    else:
        sys.exit(
            f"step {args.step} needs a run from step 1, but none exists for '{args.app}' "
            f"under {skill_ckpt}"
        )

    ckpt_dir = os.path.join(skill_ckpt, run)
    record = os.path.join(records_dir, f"{run}.yaml")
    created = not os.path.isfile(record)
    os.makedirs(ckpt_dir, exist_ok=True)
    if created:
        # Write the run record at once, so a different run cannot get the same number.
        os.makedirs(records_dir, exist_ok=True)
        with open(record, "x", encoding="utf-8") as fh:
            yaml.safe_dump({"skill": SKILL, "run": run, "result": "stopped", "stopped_at": "step_0", "steps": []}, fh, sort_keys=False)

    wiki_dir = args.wiki_dir or (workspace_config(root) or {}).get("wikiDir")
    md_report = None
    if wiki_dir:
        md_report = os.path.join(wiki_dir, SKILL, f"{SKILL}-{args.app}-{run}.md")

    print(json.dumps({
        "workspace": root,
        "app": args.app,
        "step": args.step,
        "run": run,
        "checkpointDir": ckpt_dir,
        "runRecord": record,
        "handoffFile": os.path.join(root, "handoff", SKILL, f"{run}.md"),
        "mdReport": md_report,
        "created": created,
        "runs": runs,
    }, indent=2))


if __name__ == "__main__":
    main()
