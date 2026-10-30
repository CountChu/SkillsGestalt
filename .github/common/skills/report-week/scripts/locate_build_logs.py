"""Locate build-log MD files within a date range.

Lists `.md` files in `wiki\\report-logs\\by-updated\\` and `wiki\\report-logs\\by-created\\`
whose basename (yyyy-MM-dd) falls within [start, end] inclusive.

Usage:
    python .github/skills/report-week/scripts/locate_build_logs.py <start> <end> [--dirs DIR ...]

Example:
    python .github/skills/report-week/scripts/locate_build_logs.py 2026-05-06 2026-05-12

Output: JSON to stdout with shape:
    {
      "date_range": {"start": "...", "end": "..."},
      "directories": {
        "wiki\\report-logs\\by-updated\\": {"count": N, "names": [...]},
        "wiki\\report-logs\\by-created\\": {"count": N, "names": [...]}
      },
      "total": N
    }
"""

import argparse
import json
import os
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
DEFAULT_DIRS = [
    str(wiki_dir() / "report-logs" / "by-updated"),
    str(wiki_dir() / "report-logs" / "by-created"),
]


def list_md_in_range(directory: Path, start: str, end: str) -> list[str]:
    if not directory.is_dir():
        return []
    out = []
    for p in sorted(directory.glob("*.md")):
        name = p.stem
        if DATE_RE.match(name) and start <= name <= end:
            out.append(p.name)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("start", help="Start date yyyy-MM-dd (inclusive)")
    ap.add_argument("end", help="End date yyyy-MM-dd (inclusive)")
    ap.add_argument(
        "--dirs",
        nargs="*",
        default=DEFAULT_DIRS,
        help="Build-log directories to scan (default: by-updated, by-created)",
    )
    args = ap.parse_args()

    if not (DATE_RE.match(args.start) and DATE_RE.match(args.end)):
        print("ERROR: start/end must be yyyy-MM-dd", file=sys.stderr)
        return 2
    if args.start > args.end:
        print("ERROR: start must be <= end", file=sys.stderr)
        return 2

    result = {
        "date_range": {"start": args.start, "end": args.end},
        "directories": {},
        "total": 0,
    }

    for d in args.dirs:
        names = list_md_in_range(Path(d), args.start, args.end)
        # Normalize key with trailing separator for display.
        key = d.rstrip("\\/").replace("/", "\\") + "\\"
        result["directories"][key] = {"count": len(names), "names": names}
        result["total"] += len(names)

    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
