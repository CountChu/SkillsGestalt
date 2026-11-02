"""Step 3 - Rename hash-{hash}-new.yaml to hash-{hash}.yaml.

For each hash-*-new.yaml in the checkpoints directory:
  1. If an old hash-{hash}.yaml already exists, remove it.
  2. Rename hash-{hash}-new.yaml to hash-{hash}.yaml.

Usage:
    python rename_new_hashes.py <checkpoints_dir>
"""

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Rename hash-*-new.yaml to hash-*.yaml"
    )
    parser.add_argument(
        "checkpoints_dir", type=Path, help="Path to checkpoints/report-logs directory"
    )
    args = parser.parse_args()

    cp_dir = args.checkpoints_dir
    if not cp_dir.is_dir():
        print(f"Error: directory not found: {cp_dir}", file=sys.stderr)
        sys.exit(1)

    new_files = sorted(cp_dir.glob("hash-*-new.yaml"))
    removed = 0
    renamed = 0

    for new_file in new_files:
        # Extract hash from filename: hash-{hash}-new.yaml -> hash-{hash}.yaml
        name = new_file.name  # e.g. hash-abc123-new.yaml
        target_name = name.replace("-new.yaml", ".yaml")
        target_file = cp_dir / target_name

        if target_file.exists():
            target_file.unlink()
            removed += 1

        new_file.rename(target_file)
        renamed += 1

    print(f"Renamed {renamed} files (removed {removed} old files)")


if __name__ == "__main__":
    main()
