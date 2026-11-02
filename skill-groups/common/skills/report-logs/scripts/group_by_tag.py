"""Group s1_metadata.yaml records by tag and save as s6-tag-{name}.yaml files."""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml


def slugify(name: str) -> str:
    """Convert a tag name to a safe filename slug."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def main():
    parser = argparse.ArgumentParser(
        description="Group metadata by tag into per-tag YAML files."
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
        tags = record.get("tags")
        if not tags:
            continue
        # tags is a list of {tagName, tagDescription} dicts (or legacy comma-separated string)
        if isinstance(tags, str):
            names = [t.strip() for t in tags.split(",") if t.strip()]
        else:
            names = []
            for item in tags:
                if isinstance(item, dict) and item.get("tagName"):
                    names.append(str(item["tagName"]).strip())
                elif isinstance(item, str) and item.strip():
                    names.append(item.strip())
        for tag in names:
            if tag:
                groups[tag].append(record)

    # Sort each group by updated time ascending
    for tag_name in groups:
        groups[tag_name].sort(key=lambda r: r.get("updated", ""))

    # Remove stale s6-tag-*.yaml files for tags no longer present
    current_slugs = {slugify(t) for t in groups}
    removed = 0
    for existing in output_dir.glob("s6-tag-*.yaml"):
        slug = existing.stem[len("s6-tag-"):]
        if slug not in current_slugs:
            existing.unlink()
            removed += 1

    for tag_name in sorted(groups):
        slug = slugify(tag_name)
        out_path = output_dir / f"s6-tag-{slug}.yaml"
        with open(out_path, "w", encoding="utf-8") as f:
            yaml.dump(
                groups[tag_name],
                f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )

    print(
        f"Grouped {sum(len(v) for v in groups.values())} records into {len(groups)} tag files in {output_dir} (removed {removed} stale)"
    )
    for tag_name in sorted(groups):
        slug = slugify(tag_name)
        print(f"  s6-tag-{slug}.yaml: {len(groups[tag_name])} records")


if __name__ == "__main__":
    main()
