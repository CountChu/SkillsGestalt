"""Group s1_metadata.yaml records by skill and save as s5-skill-{name}.yaml files."""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml


def slugify(name: str) -> str:
    """Convert a skill name to a safe filename slug."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def main():
    parser = argparse.ArgumentParser(
        description="Group metadata by skill into per-skill YAML files."
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
        skill_list = record.get("skill", [])
        skill_name = skill_list[0].get("name", "unknown") if skill_list else "unknown"
        groups[skill_name].append(record)

    # Sort each group by updated time ascending
    for skill_name in groups:
        groups[skill_name].sort(key=lambda r: r.get("updated", ""))

    for skill_name in sorted(groups):
        slug = slugify(skill_name)
        out_path = output_dir / f"s5-skill-{slug}.yaml"
        with open(out_path, "w", encoding="utf-8") as f:
            yaml.dump(
                groups[skill_name],
                f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )

    print(
        f"Grouped {len(records)} records into {len(groups)} skill files in {output_dir}"
    )
    for skill_name in sorted(groups):
        slug = slugify(skill_name)
        print(f"  s5-skill-{slug}.yaml: {len(groups[skill_name])} records")


if __name__ == "__main__":
    main()
