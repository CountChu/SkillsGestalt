"""Group s1_metadata.yaml records by created date and save as s4-created-{yyyy-MM-dd}.yaml files."""

import argparse
import sys
from collections import defaultdict
from pathlib import Path

import yaml


def main():
    parser = argparse.ArgumentParser(
        description="Group metadata by created date into per-date YAML files."
    )
    parser.add_argument("input", help="Path to metadata_output_v1.yaml")
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
        created = record.get("created", "")
        date_part = created[:10] if len(created) >= 10 else "unknown"
        groups[date_part].append(record)

    # Sort each group by created time ascending
    for date_key in groups:
        groups[date_key].sort(key=lambda r: r.get("created", ""))

    # Remove stale s4-created-*.yaml files for dates no longer present
    current_dates = set(groups.keys())
    removed = 0
    for existing in output_dir.glob("s4-created-*.yaml"):
        date_part = existing.stem[len("s4-created-"):]
        if date_part not in current_dates:
            existing.unlink()
            removed += 1

    for date_key in sorted(groups):
        out_path = output_dir / f"s4-created-{date_key}.yaml"
        with open(out_path, "w", encoding="utf-8") as f:
            yaml.dump(
                groups[date_key],
                f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )

    print(
        f"Grouped {len(records)} records into {len(groups)} date files in {output_dir} (removed {removed} stale)"
    )
    for date_key in sorted(groups):
        print(f"  s4-created-{date_key}.yaml: {len(groups[date_key])} records")


if __name__ == "__main__":
    main()
