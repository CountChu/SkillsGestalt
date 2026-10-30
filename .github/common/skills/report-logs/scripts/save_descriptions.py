"""Step 5 - Save descriptions from hash-{hash}.yaml files to descriptions.yaml.

For each hash-{hash}.yaml in the checkpoints directory:
  1. Read the hash and description fields.
  2. Append a record with only those two fields to the list.
Write the list to descriptions.yaml.

Usage:
    python save_descriptions.py <checkpoints_dir>
"""

import argparse
import sys
from pathlib import Path

import yaml


def main():
    parser = argparse.ArgumentParser(
        description="Save descriptions from hash-*.yaml to descriptions.yaml"
    )
    parser.add_argument(
        "checkpoints_dir", type=Path, help="Path to checkpoints/report-logs directory"
    )
    args = parser.parse_args()

    cp_dir = args.checkpoints_dir
    if not cp_dir.is_dir():
        print(f"Error: directory not found: {cp_dir}", file=sys.stderr)
        sys.exit(1)

    hash_files = sorted(cp_dir.glob("hash-*.yaml"))
    # Exclude any leftover -new.yaml files
    hash_files = [f for f in hash_files if not f.name.endswith("-new.yaml")]

    descriptions = []
    for hf in hash_files:
        with open(hf, "r", encoding="utf-8") as fh:
            record = yaml.safe_load(fh)
        if record and "hash" in record and "description" in record:
            descriptions.append(
                {
                    "hash": record["hash"],
                    "description": record["description"],
                }
            )

    out_path = cp_dir / "descriptions.yaml"
    with open(out_path, "w", encoding="utf-8") as fh:
        yaml.dump(
            descriptions,
            fh,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )

    print(f"Saved {len(descriptions)} descriptions to {out_path}")


if __name__ == "__main__":
    main()
