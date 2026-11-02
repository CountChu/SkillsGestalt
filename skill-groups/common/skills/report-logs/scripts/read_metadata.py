"""Step 1.1 - Collect Metadata for report-logs skill.

Incrementally collects metadata for .md files under a wiki directory.
If an existing v0 YAML exists, the script:
  1. Checks each existing record's fileUpdatedTime against the current
     file system LastWriteTime; re-processes only changed files.
  2. Adds records for any new .md files not present in the existing v0.
  3. Removes records whose .md files no longer exist.

Usage:
    python read_metadata.py <wiki_dir> [--skills-dir <skills_dir>] [-o <output_path>]

Output:
    YAML file at the specified output path (default: checkpoints/report-logs/s1_metadata.yaml).
"""

import argparse
import hashlib
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml


def read_lines(filepath: Path, encoding: str = "utf-8") -> list[str]:
    """Read all lines from a file, returning empty list on error."""
    try:
        return filepath.read_text(encoding=encoding, errors="replace").splitlines()
    except OSError:
        return []


def extract_header_field(lines: list[str], field: str) -> str | None:
    """Extract a header field value from the first 10 lines.

    Accepts any of these forms (whitespace-tolerant):
      - **Field**: value      (canonical bullet + bold)
      - **Field**: value      (bold only, no bullet)
      - Field: value          (bare, no bullet, no bold)
    """
    pattern = re.compile(
        rf"^(?:-\s+)?(?:\*\*)?{re.escape(field)}(?:\*\*)?:\s*(.+)$",
        re.IGNORECASE,
    )
    for line in lines[:10]:
        m = pattern.match(line.strip())
        if m:
            return m.group(1).strip()
    return None


def get_file_timestamps(filepath: Path) -> tuple[str, str]:
    """Return (created, updated) as 'yyyy-MM-dd HH:mm' from file system."""
    stat = filepath.stat()
    created = datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M")
    updated = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
    return created, updated


def extract_skill_description(skill_name: str, skills_dir: Path | None) -> str | None:
    """Extract the 'description' field from a skill's SKILL.md frontmatter."""
    if not skills_dir:
        return None
    skill_md = skills_dir / skill_name / "SKILL.md"
    if not skill_md.is_file():
        return None
    lines = read_lines(skill_md)
    in_frontmatter = False
    pattern = re.compile(r"^description:\s*(.+)$", re.IGNORECASE)
    for line in lines:
        stripped = line.strip()
        if stripped == "---":
            if in_frontmatter:
                break
            in_frontmatter = True
            continue
        if in_frontmatter:
            m = pattern.match(stripped)
            if m:
                return m.group(1).strip()
    return None


def load_tag_descriptions(tags_path: Path | None) -> dict[str, str | None]:
    """Load tags.yaml and return a mapping of tag name -> description (or None)."""
    if not tags_path or not tags_path.is_file():
        return {}
    try:
        data = yaml.safe_load(tags_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return {}
    if not isinstance(data, list):
        return {}
    result: dict[str, str | None] = {}
    for entry in data:
        if not isinstance(entry, dict):
            continue
        name = entry.get("tag")
        if name:
            desc = entry.get("description")
            result[str(name).strip()] = desc if desc else None
    return result


def build_tags(raw: str | None, tag_descriptions: dict[str, str | None]) -> list[dict]:
    """Parse a comma-separated tag string into list of {tagName, tagDescription} dicts."""
    if not raw:
        return []
    out: list[dict] = []
    for name in (t.strip() for t in str(raw).split(",") if t.strip()):
        out.append(
            {
                "tagName": name,
                "tagDescription": tag_descriptions.get(name),
            }
        )
    return out


def normalize_tags(
    value, tag_descriptions: dict[str, str | None]
) -> list[dict]:
    """Normalize a tags value (legacy string or list of dicts) into list of dicts."""
    if not value:
        return []
    if isinstance(value, str):
        return build_tags(value, tag_descriptions)
    if isinstance(value, list):
        out: list[dict] = []
        for item in value:
            if isinstance(item, dict) and item.get("tagName"):
                name = str(item["tagName"]).strip()
                desc = item.get("tagDescription")
                if desc is None:
                    desc = tag_descriptions.get(name)
                out.append({"tagName": name, "tagDescription": desc})
            elif isinstance(item, str) and item.strip():
                name = item.strip()
                out.append({"tagName": name, "tagDescription": tag_descriptions.get(name)})
        return out
    return []


def process_file(
    filepath: Path,
    parent_dir_name: str,
    skills_dir: Path | None,
    wiki_dir: Path,
    tag_descriptions: dict[str, str | None],
) -> dict:
    """Process a single .md file and return its metadata record."""
    lines = read_lines(filepath)

    # Try header source
    created = extract_header_field(lines, "Created")
    updated = extract_header_field(lines, "Updated")
    skill = extract_header_field(lines, "Skill")
    tags = extract_header_field(lines, "Tags")

    if created and updated:
        source = "header"
        if not skill:
            skill = parent_dir_name
    else:
        source = "file"
        created, updated = get_file_timestamps(filepath)
        skill = skill or parent_dir_name

    # Windows may set a newer CreationTime when files are copied;
    # clamp created to updated so created never exceeds updated.
    if created > updated:
        created = updated

    rel_path = filepath.relative_to(wiki_dir).as_posix()
    file_hash = hashlib.sha256(rel_path.encode()).hexdigest()

    # Relative path under wiki_dir, without the .md extension (e.g. "build-pr/pr_fix_0515")
    filename = rel_path[:-3] if rel_path.endswith(".md") else rel_path

    skill_description = extract_skill_description(skill, skills_dir)

    # Always include file system LastWriteTime
    _, file_updated_time = get_file_timestamps(filepath)

    record = {
        "hash": file_hash,
        "file": filename,
        "skill": [
            {"name": skill},
            {"description": skill_description},
        ],
        "created": created,
        "updated": updated,
        "fileUpdatedTime": file_updated_time,
        "source": source,
    }
    if tags:
        record["tags"] = build_tags(tags, tag_descriptions)
    return record


def get_current_file_updated_time(filepath: Path) -> str:
    """Return file system LastWriteTime as 'yyyy-MM-dd HH:mm'."""
    stat = filepath.stat()
    return datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")


def discover_md_files(wiki_dir: Path) -> dict[str, Path]:
    """Discover all .md files under wiki subdirectories.

    Returns a dict mapping hash -> filepath.
    """
    if not wiki_dir.is_dir():
        print(f"Error: wiki directory not found: {wiki_dir}", file=sys.stderr)
        sys.exit(1)

    result = {}
    for subdir in sorted(wiki_dir.iterdir()):
        if not subdir.is_dir() or subdir.name.startswith("."):
            continue
        for md_file in sorted(subdir.glob("*.md")):
            rel_path = md_file.relative_to(wiki_dir).as_posix()
            file_hash = hashlib.sha256(rel_path.encode()).hexdigest()
            result[file_hash] = md_file
    return result


def load_existing_v0(
    output_path: Path, tag_descriptions: dict[str, str | None]
) -> dict[str, dict]:
    """Load existing v0 YAML and return a dict mapping hash -> record."""
    if not output_path.is_file():
        return {}
    try:
        data = yaml.safe_load(output_path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            return {}
        result = {}
        for r in data:
            if isinstance(r, dict) and "hash" in r:
                r.pop("file_context", None)
                # Migrate legacy `file` (basename only) to relative posix path: "{skill}/{file}"
                f = r.get("file")
                if isinstance(f, str) and "/" not in f:
                    skill_list = r.get("skill") or []
                    skill_name = (
                        skill_list[0].get("name", "")
                        if skill_list and isinstance(skill_list[0], dict)
                        else ""
                    )
                    if skill_name:
                        r["file"] = f"{skill_name}/{f}"
                if "tags" in r:
                    normalized = normalize_tags(r["tags"], tag_descriptions)
                    if normalized:
                        r["tags"] = normalized
                    else:
                        r.pop("tags", None)
                result[r["hash"]] = r
        return result
    except (OSError, yaml.YAMLError):
        return {}


def scan_wiki(
    wiki_dir: Path,
    skills_dir: Path | None,
    existing_records: dict[str, dict],
    tag_descriptions: dict[str, str | None],
) -> tuple[list[dict], dict[str, int]]:
    """Incrementally scan .md files under wiki subdirectories.

    - Re-processes files whose fileUpdatedTime has changed.
    - Adds new files not in existing_records.
    - Drops records for files that no longer exist.

    Returns (records, stats) where stats has keys: unchanged, updated, new, removed.
    """
    current_files = discover_md_files(wiki_dir)
    records = []
    stats = {"unchanged": 0, "updated": 0, "new": 0, "removed": 0}

    for file_hash, md_file in current_files.items():
        parent_dir_name = md_file.parent.name

        if file_hash in existing_records:
            old_record = existing_records[file_hash]
            current_mtime = get_current_file_updated_time(md_file)
            old_mtime = old_record.get("fileUpdatedTime", "")

            if current_mtime == old_mtime:
                # File unchanged on disk. If the existing record was parsed
                # under the older "file" source (no header recognized), try
                # the header parser again — handles cases where the header
                # form is now supported by an improved parser, even though
                # the file's mtime hasn't changed.
                if old_record.get("source") == "file":
                    lines = read_lines(md_file)
                    if (
                        extract_header_field(lines, "Created")
                        and extract_header_field(lines, "Updated")
                    ):
                        record = process_file(
                            md_file, parent_dir_name, skills_dir, wiki_dir, tag_descriptions
                        )
                        record["isNew"] = True
                        records.append(record)
                        stats["updated"] += 1
                        continue
                old_record["isNew"] = False
                records.append(old_record)
                stats["unchanged"] += 1
            else:
                # File updated — re-process
                record = process_file(
                    md_file, parent_dir_name, skills_dir, wiki_dir, tag_descriptions
                )
                record["isNew"] = True
                records.append(record)
                stats["updated"] += 1
        else:
            # New file
            record = process_file(
                md_file, parent_dir_name, skills_dir, wiki_dir, tag_descriptions
            )
            record["isNew"] = True
            records.append(record)
            stats["new"] += 1

    # Count removed (in existing but no longer on disk)
    removed_hashes = set(existing_records.keys()) - set(current_files.keys())
    stats["removed"] = len(removed_hashes)

    return records, stats


def main():
    parser = argparse.ArgumentParser(
        description="Step 1 - Read Metadata for report-logs skill"
    )
    parser.add_argument("wiki_dir", type=Path, help="Path to wiki directory")
    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=None,
        help="Path to .github/skills directory (for reading skill SKILL.md files)",
    )
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Filter by Created date (yyyy-MM-dd). Only include files matching this date.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output YAML file path (default: checkpoints/report-logs/s1_metadata.yaml)",
    )
    args = parser.parse_args()

    # Auto-detect skills dir if not provided
    skills_dir = args.skills_dir
    if skills_dir is None:
        candidate = args.wiki_dir.parent / ".github" / "skills"
        if candidate.is_dir():
            skills_dir = candidate

    # Auto-detect tags.yaml and load descriptions
    tags_yaml = args.wiki_dir.parent / "database" / "tags.yaml"
    tag_descriptions = load_tag_descriptions(tags_yaml)

    # Determine output path
    output_path = args.output
    if output_path is None:
        output_path = (
            args.wiki_dir.parent
            / "checkpoints"
            / "report-logs"
            / "s1_metadata.yaml"
        )

    # Load existing v0 for incremental update
    existing_records = load_existing_v0(output_path, tag_descriptions)

    records, stats = scan_wiki(
        args.wiki_dir, skills_dir, existing_records, tag_descriptions
    )

    # Filter by date if specified
    if args.date:
        records = [r for r in records if r["created"].startswith(args.date)]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        yaml.dump(
            records, default_flow_style=False, allow_unicode=True, sort_keys=False
        ),
        encoding="utf-8",
    )
    print(
        f"Wrote {len(records)} records to {output_path}  "
        f"(unchanged={stats['unchanged']}, updated={stats['updated']}, "
        f"new={stats['new']}, removed={stats['removed']})"
    )


if __name__ == "__main__":
    main()
