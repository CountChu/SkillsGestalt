"""Split s1_metadata.yaml into individual hash-{hash}.yaml files."""

import argparse
import sys
from pathlib import Path

import yaml


def main():
    parser = argparse.ArgumentParser(
        description="Split v0 metadata into per-record YAML files."
    )
    parser.add_argument("input", help="Path to s1_metadata.yaml")
    parser.add_argument(
        "-o",
        "--output-dir",
        default=None,
        help="Output directory (default: same directory as input)",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: {input_path} not found", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output_dir) if args.output_dir else input_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(input_path, encoding="utf-8") as f:
        records = yaml.safe_load(f)

    if not isinstance(records, list):
        print("Error: expected a YAML list of records", file=sys.stderr)
        sys.exit(1)

    count = 0
    for record in records:
        hash_value = record.get("hash")
        if not hash_value:
            print(
                f"Warning: skipping record without hash: {record.get('file')}",
                file=sys.stderr,
            )
            continue
        is_new = record.get("isNew", False)
        if not is_new:
            continue
        out_path = output_dir / f"hash-{hash_value}-new.yaml"
        with open(out_path, "w", encoding="utf-8") as f:
            yaml.dump(
                record, f, default_flow_style=False, allow_unicode=True, sort_keys=False
            )
        count += 1

    print(f"Split {count} new records (of {len(records)} total) into {output_dir}")


if __name__ == "__main__":
    main()
