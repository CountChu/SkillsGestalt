#!/usr/bin/env python3
"""Find, or convert, placeholders written in the retired form ___X___.

The repo writes a placeholder a template leaves to be filled as {UPPER_SNAKE}. The form before it,
the name between three underscores on each side - ___UPPER_SNAKE___ - is retired: Markdown shows it
in bold italics instead of as written. The skills that read placeholders - check-skill, chinese,
asd-ste and gen-rsdc-skill - report it as an error and name this script.

  scan PATH...     list each ___X___ with its file and line; exit 1 when there is one, 0 when none
  convert PATH...  write each ___X___ as {X}; a file with a 繁體中文 twin beside it, X.md and
                   X-tw.md, is converted with its twin, so the two stay alike

A PATH is a Markdown file, or a directory searched for *.md. The search skips .git, .obsidian,
.trash, node_modules and __pycache__, and the task records - task-summary.md, and the directory
tasks beside it, or beside the dashboard directory that holds it - whose history stays as it was
written. A file named on the command line is read
even where a search would skip it.

Every ___X___ is matched, in prose, inline code and fenced blocks alike: a placeholder written to be
shown is written {X} too.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# The retired form, as every skill that reads placeholders matches it: capitals, digits and
# underscores between three underscores on each side.
OLD_RE = re.compile(r"___[A-Z0-9_]+___")
# The same, for converting: the shortest name, so that two placeholders side by side stay two.
CONVERT_RE = re.compile(r"___([A-Z0-9_]+?)___")
SKIP_DIRS = {".git", ".obsidian", ".trash", "node_modules", "__pycache__"}
TASK_SUMMARY = "task-summary.md"


def markdown_files(paths: list[Path]) -> list[Path]:
    """Each Markdown file a PATH names or holds, once, in order."""
    out: list[Path] = []
    for path in paths:
        if path.is_file():
            out.append(path)
            continue
        if not path.is_dir():
            raise SystemExit(f"{path}: no such file or directory")
        for found in sorted(path.rglob("*.md")):
            rel = found.relative_to(path).parts
            if any(part in SKIP_DIRS for part in rel[:-1]):
                continue
            if found.name == TASK_SUMMARY:
                continue
            if any(part == "tasks" and ((path.joinpath(*rel[:k]) / TASK_SUMMARY).is_file()
                                        or (path.joinpath(*rel[:k]) / "dashboard" / TASK_SUMMARY).is_file())
                   for k, part in enumerate(rel[:-1])):
                continue
            out.append(found)
    seen: set[Path] = set()
    unique = []
    for f in out:
        key = f.resolve()
        if key not in seen:
            seen.add(key)
            unique.append(f)
    return unique


def read(path: Path) -> tuple[str, bool] | None:
    """The file's text, and whether it opens with a byte-order mark - or None when it is not UTF-8."""
    raw = path.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    try:
        return raw.decode("utf-8-sig"), bom
    except UnicodeDecodeError:
        return None


def hits(text: str) -> list[tuple[int, str]]:
    return [(n, m.group(0)) for n, line in enumerate(text.splitlines(), 1) for m in OLD_RE.finditer(line)]


def twin_of(path: Path) -> Path | None:
    """The other half of a pair: X-tw.md for X.md, and X.md for X-tw.md - when it is there."""
    other = path.with_name(path.name[:-6] + ".md") if path.name.endswith("-tw.md") else path.with_name(path.stem + "-tw.md")
    return other if other.is_file() else None


def scan(paths: list[Path]) -> int:
    total, files = 0, 0
    for path in markdown_files(paths):
        got = read(path)
        if got is None:
            print(f"{path}: skipped, not UTF-8")
            continue
        found = hits(got[0])
        if found:
            files += 1
            total += len(found)
            for n, token in found:
                print(f"{path}:{n}: {token}")
    if total:
        print(f"{total} placeholder(s) in the retired form ___X___, in {files} file(s); "
              f"convert them with: python {Path(__file__).as_posix()} convert <file>")
        return 1
    print("no placeholder in the retired form ___X___")
    return 0


def convert(paths: list[Path]) -> int:
    targets = markdown_files(paths)
    pending = list(targets)
    for path in targets:
        other = twin_of(path)
        if other is not None and other.resolve() not in {p.resolve() for p in pending}:
            pending.append(other)
    total, files = 0, 0
    for path in pending:
        got = read(path)
        if got is None:
            print(f"{path}: skipped, not UTF-8")
            continue
        text, bom = got
        new, count = CONVERT_RE.subn(lambda m: "{" + m.group(1) + "}", text)
        if not count:
            continue
        path.write_bytes(("\ufeff" if bom else "").encode("utf-8") + new.encode("utf-8"))
        files += 1
        total += count
        print(f"{path}: {count} converted")
    print(f"{total} placeholder(s) converted to {{X}}, in {files} file(s)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command", required=True)
    for name, text in (("scan", "list each ___X___ with its file and line"),
                       ("convert", "write each ___X___ as {X}, with the twin beside a file")):
        cmd = sub.add_parser(name, help=text)
        cmd.add_argument("paths", nargs="+", type=Path, help="a Markdown file, or a directory searched for *.md")
    args = ap.parse_args()
    return scan(args.paths) if args.command == "scan" else convert(args.paths)


if __name__ == "__main__":
    sys.exit(main())
