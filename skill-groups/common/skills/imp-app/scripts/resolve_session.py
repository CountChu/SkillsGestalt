"""Resolve the imp-app session directory for one app.

One app is one session spread over many invocations: the FIRST command run against a target stamps
the Checkpoint Dir, and every later command - whichever it is - reopens the newest existing one.
That is why this is a script and not a paragraph: two invocations of one app must not be able to
land in different directories.

`checkpoints\\imp-app\\` also holds sessions written by an earlier skill that was called `imp-app`
and is now `gen-imp-app`. Those are not this skill's sessions: their `step_0` carries no `appDir`.
Reopening one would append this app's steps into another skill's record, so this refuses and says
so instead.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime

import yaml

SKILL = "imp-app"
COMMANDS = ("vibe", "reverse", "update", "test", "start", "deploy")
STAMP_RE = re.compile(r"^(?P<app>.+)-(?P<stamp>\d{6}-\d{4})$")
# The app name is the target's last path segment with a trailing -app stripped, spelled as the
# directory is. It names a directory and a document, so nothing but word characters and dashes.
APP_RE = re.compile(r"^[A-Za-z0-9]+([-_][A-Za-z0-9]+)*$")


def workspace_root(explicit: str | None) -> str:
    """The workspace holding config.yaml - the root every relative path in the skill resolves against."""
    if explicit:
        return os.path.abspath(explicit)
    here = os.getcwd()
    for _ in range(8):
        if os.path.isfile(os.path.join(here, "config.yaml")):
            return here
        parent = os.path.dirname(here)
        if parent == here:
            break
        here = parent
    return os.getcwd()


def load_wiki_dir(root: str, explicit: str | None) -> str | None:
    if explicit:
        return explicit
    cfg = os.path.join(root, "config.yaml")
    if not os.path.isfile(cfg):
        return None
    with open(cfg, encoding="utf-8") as fh:
        return (yaml.safe_load(fh) or {}).get("wikiDir")


def list_sessions(skill_ckpt: str, app: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    if not os.path.isdir(skill_ckpt):
        return out
    for name in sorted(os.listdir(skill_ckpt)):
        m = STAMP_RE.match(name)
        if m and m.group("app") == app and os.path.isdir(os.path.join(skill_ckpt, name)):
            out.append((m.group("stamp"), name))
    out.sort()
    return out


def is_foreign(ckpt_dir: str) -> bool:
    """True when this directory's process.yaml was written by something other than this skill.

    This skill's step_0 always carries `appDir`. A session that has a process.yaml without one
    belongs to the earlier skill of the same name, and appending to it would mix two records.
    """
    path = os.path.join(ckpt_dir, "process.yaml")
    if not os.path.isfile(path):
        return False
    try:
        with open(path, encoding="utf-8") as fh:
            doc = yaml.safe_load(fh) or {}
    except yaml.YAMLError:
        return False
    step0 = doc.get("step_0")
    if not isinstance(step0, dict):
        return False
    return "appDir" not in step0


def main() -> None:
    ap = argparse.ArgumentParser(description="Resolve the imp-app session directory for one app.")
    ap.add_argument("--app", required=True, help="app name, e.g. InvCov")
    ap.add_argument("--command", required=True, choices=COMMANDS, help="the command being run")
    ap.add_argument("--stamp", help="pin an explicit yymmdd-hhmm session instead of the newest")
    ap.add_argument("--new", action="store_true", help="stamp a new session even though one exists")
    ap.add_argument("--workspace", help="workspace root holding config.yaml")
    ap.add_argument("--wiki-dir", help="override wikiDir instead of reading config.yaml")
    args = ap.parse_args()

    if not APP_RE.match(args.app):
        sys.exit(f"app name '{args.app}' names a directory and a document; use letters, digits, - or _")

    root = workspace_root(args.workspace)
    skill_ckpt = os.path.join(root, "checkpoints", SKILL)
    sessions = list_sessions(skill_ckpt, args.app)

    if args.stamp:
        stamp, opened = args.stamp, "reopened" if args.stamp in [s for s, _ in sessions] else "created"
    elif sessions and not args.new:
        stamp, opened = sessions[-1][0], "reopened"
    else:
        stamp, opened = datetime.now().strftime("%y%m%d-%H%M"), "created"

    ckpt_dir = os.path.join(skill_ckpt, f"{args.app}-{stamp}")

    if args.new and not args.stamp and os.path.isdir(ckpt_dir):
        # Two sessions of one app cannot share a stamp, and inventing a minute the clock did not
        # read would be a fabricated time. Whoever wants a second session this minute names it.
        sys.exit(f"{ckpt_dir} already exists; pass --stamp to name the new session explicitly")

    if opened == "reopened" and is_foreign(ckpt_dir):
        sys.exit(
            f"{ckpt_dir} was written by the earlier skill also called imp-app (now gen-imp-app): "
            f"its step_0 carries no appDir. Re-run with --new to stamp this app's own session."
        )

    os.makedirs(ckpt_dir, exist_ok=True)

    wiki_dir = load_wiki_dir(root, args.wiki_dir)
    md_report = os.path.join(wiki_dir, SKILL, f"{SKILL}-{args.app}-{stamp}.md") if wiki_dir else None

    print(json.dumps({
        "app": args.app,
        "command": args.command,
        "stamp": stamp,
        "checkpointDir": os.path.relpath(ckpt_dir, root),
        "processYaml": os.path.relpath(os.path.join(ckpt_dir, "process.yaml"), root),
        "mdReport": md_report,
        "opened": opened,
        "sessions": [n for _, n in sessions],
    }, indent=2))


if __name__ == "__main__":
    main()
