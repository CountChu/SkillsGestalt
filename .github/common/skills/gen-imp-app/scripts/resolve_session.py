"""Resolve the gen-imp-app SOP session directory for one app.

Step 1 stamps a new Checkpoint Dir; Steps 2 and 3 reopen the newest existing one, because the SOP
is a single session spread over several invocations.
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime

import yaml

SKILL = "gen-imp-app"
STAMP_RE = re.compile(r"^(?P<app>.+)-(?P<stamp>\d{6}-\d{4})$")


def repo_root(explicit):
    if explicit:
        return os.path.abspath(explicit)
    # <root>\.github\common\skills\gen-imp-app\scripts\resolve_session.py -> the workspace holding config.yaml
    here = os.path.dirname(os.path.abspath(__file__))
    for _ in range(8):
        if os.path.isfile(os.path.join(here, "config.yaml")):
            return here
        parent = os.path.dirname(here)
        if parent == here:
            break
        here = parent
    return os.getcwd()


def load_wiki_dir(root, explicit):
    if explicit:
        return explicit
    cfg = os.path.join(root, "config.yaml")
    if not os.path.isfile(cfg):
        return None
    with open(cfg, encoding="utf-8") as fh:
        return (yaml.safe_load(fh) or {}).get("wikiDir")


def list_sessions(skill_ckpt, app):
    out = []
    if not os.path.isdir(skill_ckpt):
        return out
    for name in os.listdir(skill_ckpt):
        m = STAMP_RE.match(name)
        if m and m.group("app") == app and os.path.isdir(os.path.join(skill_ckpt, name)):
            out.append((m.group("stamp"), name))
    out.sort()
    return out


def main():
    ap = argparse.ArgumentParser(description="Resolve the gen-imp-app session directory for one app.")
    ap.add_argument("--app", required=True, help="app name, e.g. redfish-test")
    ap.add_argument("--step", required=True, type=int, help="step being run: 1 creates, 2 and 3 reopen")
    ap.add_argument("--stamp", help="pin an explicit yymmdd-hhmm session instead of the newest")
    ap.add_argument("--workspace", help="workspace root holding config.yaml")
    ap.add_argument("--wiki-dir", help="override wikiDir instead of reading config.yaml")
    args = ap.parse_args()

    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", args.app):
        sys.exit(f"app name '{args.app}' is not kebab-case; it names a directory and a skill")

    root = repo_root(args.workspace)
    skill_ckpt = os.path.join(root, "checkpoints", SKILL)
    sessions = list_sessions(skill_ckpt, args.app)

    if args.stamp:
        stamp = args.stamp
        if stamp not in [s for s, _ in sessions] and args.step != 1:
            sys.exit(f"no session '{args.app}-{stamp}' under {skill_ckpt}")
    elif args.step <= 1:
        stamp = datetime.now().strftime("%y%m%d-%H%M")
    elif sessions:
        stamp = sessions[-1][0]
    else:
        known = ", ".join(n for _, n in list_sessions(skill_ckpt, args.app)) or "(none)"
        sys.exit(
            f"step {args.step} needs a session from step 1, but none exists for '{args.app}' "
            f"under {skill_ckpt}; sessions seen: {known}"
        )

    ckpt_dir = os.path.join(skill_ckpt, f"{args.app}-{stamp}")
    created = not os.path.isdir(ckpt_dir)
    os.makedirs(ckpt_dir, exist_ok=True)

    wiki_dir = load_wiki_dir(root, args.wiki_dir)
    md_report = None
    if wiki_dir:
        md_report = os.path.join(wiki_dir, SKILL, f"{SKILL}-{args.app}-{stamp}.md")

    print(json.dumps({
        "app": args.app,
        "step": args.step,
        "stamp": stamp,
        "checkpointDir": ckpt_dir,
        "processYaml": os.path.join(ckpt_dir, "process.yaml"),
        "mdReport": md_report,
        "created": created,
        "sessions": [n for _, n in sessions],
    }, indent=2))


if __name__ == "__main__":
    main()
