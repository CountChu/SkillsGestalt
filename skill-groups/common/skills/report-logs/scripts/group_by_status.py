"""Group s1_metadata.yaml records by tag status and save as s7-status-{name}.yaml files."""

import argparse
import sys
from collections import defaultdict
from pathlib import Path

import yaml

TAGS_YAML_PATH = Path("database/tags.yaml")


def load_tag_statuses(tags_path: Path) -> dict[str, str]:
    """Load tags.yaml and return a mapping of tag name -> status."""
    if not tags_path.exists():
        print(f"Warning: {tags_path} not found, all records will be no-status", file=sys.stderr)
        return {}
    with open(tags_path, encoding="utf-8") as f:
        tags = yaml.safe_load(f)
    if not isinstance(tags, list):
        return {}
    result = {}
    for entry in tags:
        tag_name = entry.get("tag", "")
        status = entry.get("status", "")
        if tag_name and status:
            result[tag_name] = status
    return result


def extract_tag_names(record: dict) -> list[str]:
    """Return list of tag name strings from a record's tags field."""
    tags = record.get("tags")
    if not tags:
        return []
    if isinstance(tags, str):  # legacy comma-separated
        return [t.strip() for t in tags.split(",") if t.strip()]
    if isinstance(tags, list):
        names = []
        for item in tags:
            if isinstance(item, dict):
                name = item.get("tagName")
                if name:
                    names.append(str(name).strip())
            elif isinstance(item, str) and item.strip():
                names.append(item.strip())
        return names
    return []


def get_record_status(record: dict, tag_statuses: dict[str, str]) -> str:
    """Determine the status for a record based on its first tag that has a status."""
    names = extract_tag_names(record)
    if not names:
        return "no-status"
    for tag in names:
        if tag in tag_statuses:
            return tag_statuses[tag]
    return "no-status"


def main():
    parser = argparse.ArgumentParser(
        description="Group metadata by tag status into per-status YAML files."
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

    tag_statuses = load_tag_statuses(TAGS_YAML_PATH)

    groups: dict[str, list] = defaultdict(list)
    for record in records:
        status = get_record_status(record, tag_statuses)
        groups[status].append(record)

    # Sort each group by updated time ascending
    for status_name in groups:
        groups[status_name].sort(key=lambda r: r.get("updated", ""))

    for status_name in sorted(groups):
        out_path = output_dir / f"s7-status-{status_name}.yaml"
        with open(out_path, "w", encoding="utf-8") as f:
            yaml.dump(
                groups[status_name],
                f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )

    print(
        f"Grouped {sum(len(v) for v in groups.values())} records into {len(groups)} status files in {output_dir}"
    )
    for status_name in sorted(groups):
        print(f"  s7-status-{status_name}.yaml: {len(groups[status_name])} records")


if __name__ == "__main__":
    main()
