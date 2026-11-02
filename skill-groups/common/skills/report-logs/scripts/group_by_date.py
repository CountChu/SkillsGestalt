"""Group s1_metadata.yaml records by updated date and save as s3-updated-{yyyy-MM-dd}.yaml files."""

import argparse
import sys
from collections import defaultdict
from pathlib import Path

import yaml


def main():
    parser = argparse.ArgumentParser(
        description="Group metadata by date into per-date YAML files."
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

    groups: dict[str, list] = defaultdict(list)
    for record in records:
        updated = record.get("updated", "")
        date_part = updated[:10] if len(updated) >= 10 else "unknown"
        groups[date_part].append(record)

    # Sort each group by updated time ascending
    for date_key in groups:
        groups[date_key].sort(key=lambda r: r.get("updated", ""))

    for date_key in sorted(groups):
        out_path = output_dir / f"s3-updated-{date_key}.yaml"
        with open(out_path, "w", encoding="utf-8") as f:
            yaml.dump(
                groups[date_key],
                f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )

    print(
        f"Grouped {len(records)} records into {len(groups)} date files in {output_dir}"
    )
    for date_key in sorted(groups):
        print(f"  s3-updated-{date_key}.yaml: {len(groups[date_key])} records")


if __name__ == "__main__":
    main()
