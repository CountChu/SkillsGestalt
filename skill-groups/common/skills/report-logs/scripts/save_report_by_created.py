"""Read s4-created-*.yaml files and generate per-date Markdown reports in wiki/report-logs/by-created/."""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

import yaml


def wiki_dir() -> Path:
    """Vault root from the workspace config.yaml; the vault lives outside this repo."""
    for parent in Path(__file__).resolve().parents:
        cfg = parent / "config.yaml"
        if cfg.is_file():
            wiki = (yaml.safe_load(cfg.read_text(encoding="utf-8")) or {}).get("wikiDir")
            if wiki:
                return Path(wiki)
    raise SystemExit("config.yaml with a wikiDir entry was not found above this script")

SOURCE_LEGEND = """---

**Source**:
- **header**: Date read from `- **Created**:` field inside the MD file content.
- **file**: Date from the file system `CreationTime` timestamp (the MD file lacks `Created`/`Updated` header fields).
"""


def parse_existing_created(report_path: Path) -> str | None:
    """Extract the Created timestamp from an existing report file."""
    if not report_path.exists():
        return None
    pattern = re.compile(r"^- \*\*Created\*\*:\s*(.+)$")
    with open(report_path, encoding="utf-8") as f:
        for line in f:
            m = pattern.match(line.strip())
            if m:
                return m.group(1).strip()
    return None


def build_report(date_str: str, records: list, created_ts: str, updated_ts: str) -> str:
    """Build the Markdown report content for a single date."""
    lines: list[str] = []
    lines.append(f"# Build Log (Created): {date_str}")
    lines.append("")
    lines.append("- **Skill**: report-logs")
    lines.append(f"- **Created**: {created_ts}")
    lines.append(f"- **Updated**: {updated_ts}")
    lines.append("")

    # Period — based on created dates
    dates = sorted(r.get("created", "") for r in records)
    first_date = dates[0][:10] if dates else ""
    last_date = dates[-1][:10] if dates else ""
    lines.append(f"**Period**: {first_date} ~ {last_date}")
    lines.append("")

    # Table section
    lines.append("## Table")
    lines.append("")
    lines.append("| # | Hash | File | Skill | Created | Updated | Source |")
    lines.append("|---|------|------|-------|---------|---------|--------|")

    for i, rec in enumerate(records, 1):
        file_name = rec.get("file", "")
        skill_list = rec.get("skill", [])
        skill_name = skill_list[0].get("name", "") if skill_list else ""
        hash_short = rec.get("hash", "")[:6]
        created = rec.get("created", "")
        updated = rec.get("updated", "")
        source = rec.get("source", "")
        tags = rec.get("tags", "")
        # Build clickable markdown link for File column (display basename only)
        display_name = file_name.rsplit("/", 1)[-1] if file_name else file_name
        if not file_name:
            file_link = file_name
        elif " " in file_name:
            file_link = f"[{display_name}](<{file_name}.md>)"
        else:
            file_link = f"[{display_name}]({quote(file_name + '.md', safe='/')})"
        if tags:
            if isinstance(tags, str):
                tag_list = [t.strip() for t in tags.split(",") if t.strip()]
            else:
                tag_list = [
                    str(t.get("tagName", "")).strip()
                    for t in tags
                    if isinstance(t, dict) and t.get("tagName")
                ]
            if tag_list:
                file_link += "<br>" + " ".join(f"`{t}`" for t in tag_list)
        lines.append(
            f"| {i} | {hash_short} | {file_link} | {skill_name} | {created} | {updated} | {source} |"
        )

    lines.append("")

    # List section
    lines.append("## List")
    lines.append("")
    for i, rec in enumerate(records, 1):
        desc = rec.get("summary", "")
        lines.append(f"{i}. {desc}")

    lines.append("")
    lines.append(SOURCE_LEGEND)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate per-date Markdown reports from s4-created-*.yaml files."
    )
    parser.add_argument(
        "checkpoint_dir",
        help="Path to checkpoints/report-logs directory containing s4-created-*.yaml files",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default=None,
        help="Output directory for reports (default: wiki/report-logs/by-created)",
    )
    args = parser.parse_args()

    checkpoint_dir = Path(args.checkpoint_dir)
    if not checkpoint_dir.exists():
        print(f"Error: {checkpoint_dir} not found", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output_dir) if args.output_dir else wiki_dir() / "report-logs" / "by-created"
    output_dir.mkdir(parents=True, exist_ok=True)

    created_files = sorted(checkpoint_dir.glob("s4-created-*.yaml"))
    if not created_files:
        print("No s4-created-*.yaml files found", file=sys.stderr)
        sys.exit(1)

    now_ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    saved_count = 0
    summary_lines = []

    for yaml_file in created_files:
        # Extract date from filename: s4-created-2026-04-17.yaml -> 2026-04-17
        date_str = yaml_file.stem.replace("s4-created-", "")
        report_path = output_dir / f"{date_str}.md"

        with open(yaml_file, encoding="utf-8") as f:
            records = yaml.safe_load(f)

        if not isinstance(records, list):
            print(f"Warning: {yaml_file} is not a list, skipping", file=sys.stderr)
            continue

        # Exclude records generated by the report-logs skill itself
        records = [
            r
            for r in records
            if not (r.get("skill") and r["skill"][0].get("name") == "report-logs")
        ]

        if not records:
            continue

        # Preserve Created timestamp from existing file, or use current time
        existing_created = parse_existing_created(report_path)
        created_ts = existing_created if existing_created else now_ts

        content = build_report(date_str, records, created_ts, now_ts)

        with open(report_path, "w", encoding="utf-8") as f:
            f.write(content)

        saved_count += 1
        summary_lines.append(f"  {date_str}.md: {len(records)} records")

    print(f"Saved {saved_count} reports to {output_dir}")
    for line in summary_lines:
        print(line)


if __name__ == "__main__":
    main()
