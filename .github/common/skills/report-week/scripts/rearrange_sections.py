"""Rearrange sections in a weekly report file to match the order defined in SKILL.md Step 24.

Usage:
    python .github/skills/report-week/scripts/rearrange_sections.py <report_file>

Example:
    python .github/skills/report-week/scripts/rearrange_sections.py wiki/report-week/week-2026-04-22.md
"""

import os
import re
import sys
from datetime import datetime

SKILL_MD = os.path.join(os.path.dirname(__file__), "..", "SKILL.md")


def load_section_order() -> list[str]:
    """Parse section order from Step 24's numbered list in SKILL.md."""
    with open(SKILL_MD, "r", encoding="utf-8") as f:
        content = f.read()

    # Find Step 24 block
    match = re.search(r"## Step 24.*?\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
    if not match:
        raise RuntimeError("Cannot find Step 24 in SKILL.md")

    # Extract numbered items (e.g. "  2. Build Log Entries" or "  5. **Key Takeaways**")
    items = re.findall(r"^\s+\d+\.\s+(.+)$", match.group(1), re.MULTILINE)
    order = []
    for item in items:
        # Skip "Header" entry — it's not a ## section
        if item.lower().startswith("header"):
            continue
        # Strip bold markers
        name = item.replace("**", "").strip()
        order.append(f"## {name}")
    return order


def rearrange(filepath: str) -> None:
    section_order = load_section_order()
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Update timestamp
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    content = re.sub(
        r"(?<=\*\*Updated\*\*: )\d{4}-\d{2}-\d{2} \d{2}:\d{2}", now, content
    )

    # Split into header (before first ##) and sections
    parts = re.split(r"(?=^## )", content, flags=re.MULTILINE)
    header = parts[0]
    sections = parts[1:]

    # Map section title -> content
    sec_map = {}
    for s in sections:
        title = s.split("\n")[0].strip()
        # Ensure section ends with exactly one trailing newline
        sec_map[title] = s.rstrip("\n") + "\n\n"

    # Rebuild in desired order
    result = header.rstrip("\n") + "\n\n"
    found = 0
    for title in section_order:
        if title in sec_map:
            result += sec_map[title]
            found += 1

    # Append any sections not in the defined order (preserve unknown sections)
    for s in sections:
        title = s.split("\n")[0].strip()
        if title not in section_order:
            result += s.rstrip("\n") + "\n\n"
            found += 1

    # Remove trailing whitespace
    result = result.rstrip() + "\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"Rearranged {found} sections in {filepath}")
    print(f"Updated timestamp to {now}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <report_file>")
        sys.exit(1)
    rearrange(sys.argv[1])
