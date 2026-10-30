"""Deliver one app's code from its app dir to one or more named targets on other machines.

The `deploy` command's tool, and the only one of this skill's tools that writes outside the
workspace - which is why it is a program: copying a tree and writing a config is deterministic, and
the manifest is computed from what was actually written rather than from what was meant to be.

    python deploy_app.py --app-dir <dir> --target <name> [--target <name>] [--force] [--dry-run]
    python deploy_app.py --app-dir <dir> --all

`targets` is a list because there can be more than one machine serving this app, and two of them
drifting apart is what that list exists to prevent. **A target is named, never typed as a path**:
naming picks an entry the config already carries, so this tool cannot be pointed at a folder nobody
agreed to. With neither --target nor --all it REFUSES and prints the names - writing to somebody
else's machine is not a default.

It copies the CODE, and only the code: `server.js`, `app.js`, `start.cmd`, `README.txt`, `public\\`
and `scripts\\`. The app dir's `docs\\` and `tests\\` stay there - that is the app's history
and its source of record, and a fault found on a target is reproduced there. A target's own
`data\\`, `logs\\` and `temp\\` are ITS own - what it downloaded, what its own runs printed - and
overwriting them takes away work it did for itself. `__pycache__` is not code and is keyed to the
interpreter that wrote it.

A file is current at the target when its size AND its modification time both equal the app dir's, and
it is copied when either differs. The times are comparable only because the copy preserves the
source's, so both values come from THIS machine's clock and the two machines' clocks never enter
into it - which is what a plain "the target's copy is older" test gets wrong. Testing equality
rather than "newer" is also what still catches a source rewritten to the same length, and what still
replaces a hand edit made at the target rather than mistaking it for something newer than the app dir.

`app.config.json` is always written: that target's own `config` is applied over the app dir's. An
`assembledAt` the app dir carries is passed through rather than refreshed, because it labels the code
being sent; one the target does not carry is not invented here.

One unreachable target does not stop the others: each is reported on its own and the exit code says
whether any failed.

Standard library plus PyYAML, which the workspace has - it never runs on the target.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

import yaml

SKILL_DIR = Path(__file__).resolve().parent.parent
SKILL_CONFIG = SKILL_DIR / "assets" / "config.yaml"

# The app's code, and the whole of it. An app.config.json is transformed rather than copied.
CODE_FILES = ("server.js", "app.js", "start.cmd", "README.txt")
CODE_DIRS = ("public", "scripts")
APP_CONFIG = "app.config.json"
# In the app dir and never sent: the app's own history and source of record.
NOT_SENT = ("docs", "tests")
# On the target and never written: that machine's own work.
UNTOUCHED = ("data", "logs", "temp")

# For filesystems that store the time coarsely, not for clock skew - a copy carries the source's
# time, so skew cannot reach this comparison.
MTIME_TOLERANCE = 2.0


def load_targets() -> list[tuple[str, Path, dict]]:
    """The `targets` entries, as (name, appDir, config), in the order the config lists them."""
    if not SKILL_CONFIG.is_file():
        sys.exit(f"no skill config at {SKILL_CONFIG}; the targets list is what a destination is resolved through")
    cfg = yaml.safe_load(SKILL_CONFIG.read_text(encoding="utf-8")) or {}
    entries = cfg.get("targets")
    if entries is None:
        entries = []
    if not isinstance(entries, list):
        sys.exit(f"{SKILL_CONFIG}: `targets` must be a list of entries, each with a name and an appDir")
    out: list[tuple[str, Path, dict]] = []
    for entry in entries:
        entry = entry or {}
        name = str(entry.get("name") or "").strip()
        app_dir = str(entry.get("appDir") or "").strip()
        if not name or not app_dir:
            sys.exit(f"{SKILL_CONFIG}: every targets entry needs a name and an appDir; got {entry!r}")
        if name in [n for n, _, _ in out]:
            # A list cannot enforce this the way a mapping would, so it is enforced here: two
            # entries answering to one name means whichever comes first silently wins.
            sys.exit(f"{SKILL_CONFIG}: two targets are both named '{name}'")
        out.append((name, Path(app_dir), entry.get("config") or {}))
    return out


def pick(available: list, wanted: list[str], take_all: bool) -> list:
    """The targets this run may write to. Naming is required: an unnamed run writes nothing."""
    names = [n for n, _, _ in available]
    if not available:
        sys.exit(f"no targets in {SKILL_CONFIG} - nothing to deploy to")
    if take_all:
        return available
    if not wanted:
        sys.exit("name a target, or pass --all. Registered: " + ", ".join(names))
    unknown = [w for w in wanted if w not in names]
    if unknown:
        sys.exit(f"no such target: {', '.join(unknown)}. Registered: " + ", ".join(names))
    return [t for t in available if t[0] in wanted]


def code_set(app_dir: Path) -> list[tuple[str, Path]]:
    """Every code file to deploy, as (relative posix name, source path), in a stable order."""
    found: list[tuple[str, Path]] = []
    for name in CODE_FILES:
        source = app_dir / name
        if source.is_file():
            found.append((name, source))
    for folder in CODE_DIRS:
        base = app_dir / folder
        if not base.is_dir():
            continue
        for source in sorted(base.rglob("*")):
            if source.is_file() and "__pycache__" not in source.parts:
                found.append((source.relative_to(app_dir).as_posix(), source))
    return found


def is_current(source: Path, destination: Path) -> bool:
    """True when the target's file is this source: same size, and the time the copy carried over."""
    try:
        there = destination.stat()
    except OSError:
        return False
    here = source.stat()
    return here.st_size == there.st_size and abs(here.st_mtime - there.st_mtime) <= MTIME_TOLERANCE


def folder_summary(path: Path) -> dict | None:
    """{files, bytes} of a folder this command does not write, or None when it is not there."""
    if not path.is_dir():
        return None
    files = total = 0
    for item in path.rglob("*"):
        try:
            if item.is_file():
                files += 1
                total += item.stat().st_size
        except OSError:          # a file that vanished mid-walk is the far side's business
            continue
    return {"files": files, "bytes": total}


def target_state(app_dir: Path) -> str:
    if app_dir.is_dir():
        return "reachable, already carrying a copy"
    if app_dir.parent.is_dir():
        return "reachable, empty"
    return "unreachable"


def deploy_one(name: str, app_dir: Path, overrides: dict, base: dict,
               files: list[tuple[str, Path]], args) -> dict:
    state = target_state(app_dir)
    report = {
        "target": name,
        "appDir": str(app_dir),
        "state": state,
        "dryRun": bool(args.dry_run),
        "written": [],
        "current": [],
        "failed": [],
        "notSent": {f: folder_summary(Path(args.app_dir) / f) for f in NOT_SENT},
        "leftAlone": {},
        "appConfigWritten": None,
        "appConfigOverrides": sorted(overrides),
        "targetOrigin": None,
        "deployedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    if state == "unreachable":
        # One unreachable machine is not grounds to abandon the others.
        report["error"] = f"{app_dir.parent} is not reachable - nothing was written here"
        return report

    for relative, source in files:
        destination = app_dir / relative
        if not args.force and is_current(source, destination):
            report["current"].append(relative)
            continue
        size = source.stat().st_size
        if args.dry_run:
            report["written"].append({"path": relative, "size": size})
            continue
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        except OSError as error:
            report["failed"].append({"path": relative, "error": str(error)})
            continue
        report["written"].append({"path": relative, "size": size})

    # The one file that is transformed rather than copied: this target's config over the app dir's.
    written_config = dict(base)
    written_config.update(overrides)
    report["appConfigWritten"] = written_config
    destination = app_dir / APP_CONFIG
    try:
        theirs = json.loads(destination.read_text(encoding="utf-8"))
    except (OSError, ValueError):   # unreadable is not grounds to claim their values as ours
        theirs = {}
    report["appConfigReplaced"] = {k: theirs.get(k) for k in sorted(set(overrides) | {"assembledAt"})}
    if not args.dry_run:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(written_config, indent=2, ensure_ascii=False) + "\n",
                               encoding="utf-8")

    port, host = written_config.get("port"), written_config.get("host") or "127.0.0.1"
    if port:
        report["targetOrigin"] = f"http://{host}:{port}"
    report["leftAlone"] = {f: folder_summary(app_dir / f) for f in UNTOUCHED}
    return report


def main() -> int:
    ap = argparse.ArgumentParser(description="Deliver one imp-app app dir's code to registered targets.")
    ap.add_argument("--app-dir", required=True, help="the app directory, e.g. artifacts\\InvCov")
    ap.add_argument("--target", action="append", default=[],
                    help="the NAME of a targets entry, repeatable; never a path")
    ap.add_argument("--all", action="store_true", dest="take_all",
                    help="deploy to every registered target")
    ap.add_argument("--force", action="store_true",
                    help="copy every code file regardless of the comparison")
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would be written without writing it")
    ap.add_argument("--out", required=True,
                    help="the run's Checkpoint Dir; deploy-{target}.json is written there")
    args = ap.parse_args()
    began = time.time()

    app_dir = Path(args.app_dir).resolve()
    if not app_dir.is_dir():
        sys.exit(f"no such app dir: {app_dir}")
    args.app_dir = str(app_dir)

    base_path = app_dir / APP_CONFIG
    if not base_path.is_file():
        sys.exit(f"no {APP_CONFIG} in {app_dir} - a target's config is applied over the app dir's")
    base = json.loads(base_path.read_text(encoding="utf-8"))

    chosen = pick(load_targets(), args.target, args.take_all)
    files = code_set(app_dir)
    if not files:
        sys.exit(f"no code files found under {app_dir} - nothing to deploy")

    reports = [deploy_one(name, dest, overrides, base, files, args)
               for name, dest, overrides in chosen]

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    for report in reports:
        (out_dir / f"deploy-{report['target']}.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    manifest = {
        "appDir": os.path.relpath(app_dir, Path.cwd()) if str(app_dir).startswith(str(Path.cwd())) else str(app_dir),
        "codeFiles": len(files),
        "targets": reports,
        "savedTo": str(out_dir),
        "elapsed": f"{time.time() - began:.1f}s",
        "restartNeeded": any(r["written"] and not args.dry_run for r in reports),
    }
    print(json.dumps(manifest, indent=2, ensure_ascii=False))

    bad = [r["target"] for r in reports if r["failed"] or r["state"] == "unreachable"]
    if bad:
        print(f"\nfailed or unreachable: {', '.join(bad)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
