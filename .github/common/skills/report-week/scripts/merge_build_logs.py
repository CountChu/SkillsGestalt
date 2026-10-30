"""Merge build-log entries from MD files within a date range.

Scans both `wiki\\report-logs\\by-updated\\` and `wiki\\report-logs\\by-created\\` (or
custom dirs), parses table rows, deduplicates by `Hash`, and emits the merged set
sorted by `Updated` ascending.

Usage:
    python .github/skills/report-week/scripts/merge_build_logs.py <start> <end> [--dirs DIR ...] [--format {markdown,json}]

Example:
    python .github/skills/report-week/scripts/merge_build_logs.py 2026-05-06 2026-05-12

Default `--format markdown` prints a table to stdout. `--format json` prints a JSON
array of entries with keys: hash, file, link, skill, created, updated.
"""

import argparse
import json
import re
import sys
from pathlib import Path

import yaml


def wiki_dir() -> Path:
    """Vault root from the workspace config.yaml; the vault lives outside this repo."""
    for parent in Path(__file__).resolve().parents:
        cfg = parent / "config.yaml"
        if cfg.is_file():
            wiki = (yaml.safe_load(cfg.read_text(encoding="utf-8")) or {}).get("wikiDir")
            if wiki:
                return Path(wiki)
    raise SystemExit("config.yaml with a wikiDir entry was not found above this script")


DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ROW_RE = re.compile(
    r"^\|\s*\d+\s*\|\s*([0-9a-f]{6})\s*\|\s*\[([^\]]+)\]\(([^)]+)\)(?:[^|]*)\|"
    r"\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|"
)
DEFAULT_DIRS = [
    str(wiki_dir() / "report-logs" / "by-updated"),
    str(wiki_dir() / "report-logs" / "by-created"),
]


def parse_file(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        rows.append({
            "hash": m.group(1),
            "file": m.group(2),
            "link": m.group(3),
            "skill": m.group(4).strip(),
            "created": m.group(5).strip(),
            "updated": m.group(6).strip(),
        })
    return rows


def merge(dirs: list[str], start: str, end: str) -> list[dict]:
    by_hash: dict[str, dict] = {}
    for d in dirs:
        directory = Path(d)
        if not directory.is_dir():
            continue
        for p in sorted(directory.glob("*.md")):
            if not (DATE_RE.match(p.stem) and start <= p.stem <= end):
                continue
            for row in parse_file(p):
                by_hash.setdefault(row["hash"], row)
    return sorted(by_hash.values(), key=lambda r: r["updated"])


def render_markdown(entries: list[dict]) -> str:
    lines = [
        "| # | Hash | File | Skill | Created | Updated |",
        "|---|------|------|-------|---------|---------|",
    ]
    for i, r in enumerate(entries, 1):
        lines.append(
            f"| {i} | {r['hash']} | {r['file']} | {r['skill']} | {r['created']} | {r['updated']} |"
        )
    lines.append("")
    lines.append(f"Total unique entries: {len(entries)}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("start")
    ap.add_argument("end")
    ap.add_argument("--dirs", nargs="*", default=DEFAULT_DIRS)
    ap.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = ap.parse_args()

    if not (DATE_RE.match(args.start) and DATE_RE.match(args.end)):
        print("ERROR: start/end must be yyyy-MM-dd", file=sys.stderr)
        return 2
    if args.start > args.end:
        print("ERROR: start must be <= end", file=sys.stderr)
        return 2

    entries = merge(args.dirs, args.start, args.end)
    if args.format == "json":
        json.dump(entries, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(render_markdown(entries))
    return 0


if __name__ == "__main__":
    sys.exit(main())
