"""Merge s1_metadata.yaml and descriptions.yaml into metadata_output_v1.yaml.

For each record in v0, look up the description by hash from descriptions.yaml
and add the description field.
"""

import argparse
import sys
from pathlib import Path

import yaml


def main():
    parser = argparse.ArgumentParser(
        description="Merge v0 metadata with descriptions into v1."
    )
    parser.add_argument("v0", help="Path to s1_metadata.yaml")
    parser.add_argument("descriptions", help="Path to descriptions.yaml")
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output path (default: metadata_output_v1.yaml in same directory as v0)",
    )
    args = parser.parse_args()

    v0_path = Path(args.v0)
    desc_path = Path(args.descriptions)

    if not v0_path.exists():
        print(f"Error: {v0_path} not found", file=sys.stderr)
        sys.exit(1)
    if not desc_path.exists():
        print(f"Error: {desc_path} not found", file=sys.stderr)
        sys.exit(1)

    output_path = (
        Path(args.output) if args.output else v0_path.parent / "metadata_output_v1.yaml"
    )

    with open(v0_path, encoding="utf-8") as f:
        records = yaml.safe_load(f)
    with open(desc_path, encoding="utf-8") as f:
        descriptions = yaml.safe_load(f)

    if not isinstance(records, list):
        print("Error: v0 file must contain a YAML list", file=sys.stderr)
        sys.exit(1)
    if not isinstance(descriptions, list):
        print("Error: descriptions file must contain a YAML list", file=sys.stderr)
        sys.exit(1)

    desc_map = {d["hash"]: d["description"] for d in descriptions if "hash" in d}

    merged = []
    matched = 0
    for record in records:
        h = record.get("hash")
        out = dict(record)
        if h in desc_map:
            out["description"] = desc_map[h]
            matched += 1
        merged.append(out)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(
            merged, f, default_flow_style=False, allow_unicode=True, sort_keys=False
        )

    print(
        f"Merged {len(records)} records ({matched} with descriptions) into {output_path}"
    )


if __name__ == "__main__":
    main()
