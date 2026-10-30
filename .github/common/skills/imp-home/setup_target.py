#!/usr/bin/env python3
"""Create one hub's target frame. This belongs to the `setup` command alone.

A frame is not an app: this writes the directory, the app config, the launcher, the README and the
lifecycle record, and deliberately writes NO server.js. Producing one is what `gen` is for.

Which hub and which target are both command-line arguments, not defaults. It refuses a target that
already carries a lifecycle record, because every command after setup edits the target in place and
rewriting the frame would discard what the target has become.

It is the only program that reads the skill config. The hub it seeds reads only its own
app.config.json, which is what lets the folder be moved as a whole.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_CONFIG = os.path.join(SKILL_DIR, "config.yaml")

# The whole of app.config.json, and the app has nothing else to fall back on.
CONFIG_KEYS = ("title", "port", "links", "assembledAt")

LIFECYCLE = ".imp-home.json"

START_CMD = '@echo off\r\nnode "%~dp0server.js" %*\r\n'

README = """{title} - standalone app

Run:  start.cmd        (or: node server.js)
Then: http://127.0.0.1:{port}/

One page of buttons, one per link in app.config.json. The server renders them on
request, so the page carries no JavaScript and every label and URL is escaped
before it becomes markup. Node only - no Python, nothing to pip or npm install.

This directory OWNS this hub. It was framed once by imp-home's `setup` command
and is not regenerated: the code here and the design in docs\\ are the source.
Change either through `/imp-home` with the command the lifecycle allows - see
.imp-home.json for which phase this target is in.

A file:// link cannot navigate from this page: a browser blocks a file:// target
from a page served over http, and says nothing when it does. Such a button still
renders exactly like every other one, because the hub cannot know how a reader
arrived and the same links may also be published as a page opened straight off a
share, where they work. So the fact is kept in /healthz and in this note rather
than on the page. {dead}

A link may also be MOUNTED: its path is served by this hub itself, out of the
app directory named beside it in app.config.json, so that app answers on this
port without its own server being up. A mount whose app.js is missing answers at
its own path saying so and changes nothing else about the hub. {mounts}

Everything this app reads is in app.config.json beside server.js. With no mounts
the folder can be moved as a whole; with them it moves only together with the
app directories it mounts.

Bound to loopback: pass --host 0.0.0.0 to let other machines reach it, but that
hands everyone who can reach this box the same links - and everything mounted on
them.

Framed {stamp}. There is no server.js yet - run the `gen` command to write one.
"""


def load_skill_config(path: str) -> dict:
    try:
        import yaml
    except ImportError:
        sys.exit("PyYAML is needed to read the skill config - run this from the workspace .venv")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    except OSError as exc:
        sys.exit(f"cannot read the skill config: {exc}")


def scheme_of(href: str) -> str:
    head = str(href or "").split(":", 1)
    return head[0].lower() if len(head) == 2 else ""


# The hub's own routes, which a mount prefix must not shadow.
RESERVED_PREFIXES = {"/", "/index.html", "/app.css", "/healthz"}


def mount_prefix(href: str) -> str:
    """A mounted entry's href is a path on this origin, and that path is the prefix."""
    raw = str(href or "").split("?")[0].split("#")[0]
    return raw.rstrip("/") if raw.startswith("/") else ""


def main() -> int:
    cfg = load_skill_config(SKILL_CONFIG)
    homes = cfg.get("homes") or {}

    ap = argparse.ArgumentParser(description="Create one hub's target frame.")
    ap.add_argument("--hub", help="which homes entry to seed from")
    ap.add_argument("--target", help="the directory to frame, relative to --root")
    ap.add_argument("--root", default=os.getcwd(),
                    help="workspace root a relative target resolves against (default: cwd)")
    ap.add_argument("--port", type=int, help="override the seed entry's port")
    ap.add_argument("--title", help="override the seed entry's title")
    args = ap.parse_args()

    # Never frame "the only one" or "the first one": which hub is the caller's to say.
    if not args.hub:
        sys.exit("no --hub given. This tool frames one named hub and never picks.\n"
                 "  configured hubs: " + (", ".join(sorted(homes)) or "(none)"))
    if args.hub not in homes:
        sys.exit(f"{args.hub!r} is not a key of `homes` in {SKILL_CONFIG}.\n"
                 "  configured hubs: " + (", ".join(sorted(homes)) or "(none)"))
    if not args.target:
        sys.exit("no --target given. The target directory is named on the prompt, not guessed here.")

    entry = homes[args.hub] or {}
    root = os.path.abspath(args.root)
    port = args.port if args.port is not None else entry.get("port")
    title = args.title or entry.get("title") or args.hub

    if port is None:
        sys.exit(f"homes.{args.hub} has no port, and no --port was given")

    links_raw = entry.get("links")
    if not links_raw:
        sys.exit(f"homes.{args.hub}.links is missing or empty - the hub would have no buttons, "
                 "which is never what was wanted")

    links: list[dict] = []
    mounts: list[dict] = []
    for i, e in enumerate(links_raw):
        where = f"homes.{args.hub}.links[{i}]"
        if not isinstance(e, dict) or not e.get("label") or not e.get("href"):
            sys.exit(f"{where} needs both a label and an href: {e!r}")
        link = {"label": str(e["label"]), "href": str(e["href"])}
        if e.get("note"):
            link["note"] = str(e["note"])

        spec = e.get("mount")
        if spec:
            if not isinstance(spec, dict) or not spec.get("appDir"):
                sys.exit(f"{where}.mount needs an appDir: {spec!r}")
            prefix = mount_prefix(link["href"])
            if not prefix:
                sys.exit(f"{where} is mounted, so its href must be a path on this origin such as "
                         f"/some-app/, not {link['href']!r}")
            if prefix in RESERVED_PREFIXES:
                sys.exit(f"{where} would mount on {prefix}, which is one of the hub's own routes "
                         "and would shadow it")
            clash = next((m for m in mounts if m["prefix"] == prefix), None)
            if clash:
                sys.exit(f"{where} would mount on {prefix}, already taken by {clash['label']!r}")

            raw_dir = str(spec["appDir"])
            app_dir = raw_dir if os.path.isabs(raw_dir) else os.path.join(root, raw_dir)
            app_dir = os.path.abspath(app_dir)
            # Absolute, because the hub resolves its own paths against its own directory and a
            # mount is the one thing that lives outside it.
            link["mount"] = {"appDir": app_dir}
            if spec.get("skill"):
                link["mount"]["skill"] = str(spec["skill"])
            mounts.append({
                "prefix": prefix,
                "label": link["label"],
                "appDir": app_dir,
                "skill": spec.get("skill"),
                # Reported, not rejected: that app has simply not had its own skill run yet.
                "ready": os.path.isfile(os.path.join(app_dir, "app.js")),
            })

        links.append(link)

    dest = args.target if os.path.isabs(args.target) else os.path.join(root, args.target)
    dest = os.path.abspath(dest)
    if dest.lower().startswith(SKILL_DIR.lower()):
        sys.exit(f"refusing to frame the skill's own directory: {dest}")

    # `setup` runs once. A target with a lifecycle record is one a later command has been editing.
    record_path = os.path.join(dest, LIFECYCLE)
    if os.path.isfile(record_path):
        try:
            with open(record_path, "r", encoding="utf-8") as fh:
                phase = (json.load(fh) or {}).get("phase", "unknown")
        except (OSError, ValueError):
            phase = "unreadable"
        nxt = {"setup": "gen", "gen": "update", "update": "update"}.get(phase, "gen")
        sys.exit(f"{dest} is already set up - it is in phase {phase!r}.\n"
                 f"  setup runs once per target. The command that follows is `{nxt}`.")

    os.makedirs(os.path.join(dest, "public"), exist_ok=True)
    written: list[tuple[str, int]] = []

    def text(rel: str, body: str) -> None:
        with open(os.path.join(dest, rel), "w", encoding="utf-8", newline="") as fh:
            fh.write(body)
        written.append((rel, len(body.encode("utf-8"))))

    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    app_cfg = {"title": str(title), "port": int(port), "links": links, "assembledAt": stamp}
    missing = [k for k in CONFIG_KEYS if k not in app_cfg]
    if missing:
        sys.exit(f"app.config.json would be incomplete, missing: {', '.join(missing)}")

    dead = [l for l in links if scheme_of(l["href"]) == "file"]
    dead_note = (
        f"\nThis frame has {len(dead)} such link: " + ", ".join(l["label"] for l in dead) + "."
    ) if dead else ""

    pending = [m for m in mounts if not m["ready"]]
    mounts_note = (
        f"\nThis frame mounts {len(mounts)} app(s): "
        + ", ".join(f"{m['label']} at {m['prefix']}/" for m in mounts) + "."
        + (f"\n{len(pending)} of them has no app.js yet: "
           + ", ".join(m["label"] for m in pending) + "." if pending else "")
    ) if mounts else "\nThis frame mounts nothing - every button leaves this hub."

    text("app.config.json", json.dumps(app_cfg, indent=2) + "\n")
    text("start.cmd", START_CMD)
    text("README.txt", README.format(title=app_cfg["title"], port=app_cfg["port"], stamp=stamp,
                                     dead=dead_note, mounts=mounts_note))
    text(LIFECYCLE, json.dumps({
        "hub": args.hub,
        "phase": "setup",
        "history": [{"command": "setup", "at": stamp}],
    }, indent=2) + "\n")

    total = sum(size for _, size in written)
    print(f"hub           {args.hub}")
    print(f"title         {app_cfg['title']}")
    print(f"target        {dest}")
    for rel, size in written:
        print(f"  {rel.replace(os.sep, '/'):24} {size / 1024:8.1f} KB")
    print(f"  {'total':24} {total / 1024:8.1f} KB")
    print(f"port          {app_cfg['port']}")
    print(f"links         {len(links)}")
    for l in links:
        mark = ""
        if scheme_of(l["href"]) == "file":
            mark = "  [cannot navigate from an http page]"
        if "mount" in l:
            mark = "  [served by this hub]"
        print(f"  {l['label']:22} -> {l['href']}{mark}")
    if mounts:
        print(f"mounts        {sum(1 for m in mounts if m['ready'])}/{len(mounts)} ready")
        for m in mounts:
            state = "ready" if m["ready"] else f"NO app.js yet - run {m['skill'] or 'its own skill'}"
            print(f"  {m['prefix'] + '/':22} {m['appDir']}  [{state}]")
    if dead:
        print(f"dead links    {len(dead)} - " + ", ".join(l["label"] for l in dead)
              + "  (counted in /healthz, never marked on the page)")
    print("phase         setup")
    print("no server.js  a frame is not an app - run the `gen` command next")
    return 0


if __name__ == "__main__":
    sys.exit(main())
