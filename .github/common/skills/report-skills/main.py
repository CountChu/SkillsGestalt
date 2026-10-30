"""report-skills (compiled).

Description (from SKILL.md):
    The skill reads all SKILL.md files in the skills directory and generates
    a structured report of all available skills.

Workflow steps:
    Step 0 - Warmup
    Step 1 - Read All SKILL.md Files
    Step 2 - Summary Table
    Step 3 - Skills Description
    Step 4 - Category Breakdown
    Step 5 - Key Metrics
    Step 6 - Per-Skill Details

Classification: compilable (pure file-system; no MCP / SSH / ADO).

Output: <out-dir>/skills_report_{yyyyMMdd}.md (default out-dir: wiki/report-skills).

Usage:
    python .github/skills/report-skills/main.py
    python .github/skills/report-skills/main.py --out-dir wiki/report-skills
    python .github/skills/report-skills/main.py --date 2026-06-05 --prompt "Run all steps."
"""
from __future__ import annotations

import argparse
import datetime
import re
from collections import defaultdict
from pathlib import Path

# Workspace root = three levels up from this file (.github/skills/<name>/main.py).
ROOT = Path(__file__).resolve().parents[3]
SKILLS_DIR = ROOT / ".github" / "skills"
DEFAULT_OUT_DIR = ROOT / "wiki" / "report-skills"
DEFAULT_PROMPT = "Follow instructions in #prompt:SKILL.md"

CATEGORIES_ORDER = [
    "Build/Create",
    "Check/Validate",
    "Compare",
    "Report",
    "Triage",
    "Utility/Format",
]

OUTPUT_HINTS = [
    (r"\.md\b|markdown|MD report|wiki[\\/]", "Markdown"),
    (r"\.ya?ml\b|YAML checkpoint|YAML report", "YAML"),
    (r"\.html\b|HTML", "HTML"),
    (r"\.csv\b|CSV", "CSV"),
    (r"\.json\b|JSON", "JSON"),
    (r"console output|prints? to|display|stdout", "Console"),
]

FRONT_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
NAME_RE = re.compile(r"^name:\s*(.+?)\s*$", re.M)
DESC_RE = re.compile(r"^description:\s*(.+?)\s*$", re.M)
STEP_RE = re.compile(r"^## Step\b", re.M)
STEP_NUM_RE = re.compile(r"^## Step\s+(\d+)\b[^\n]*", re.M)
STEP_TITLE_RE = re.compile(r"^## Step\s+\d+\s*-\s*(.+?)\s*$", re.M)
SCRIPT_RE = re.compile(
    r"(?<![\w/\\.-])((?:scripts|\.github/skills/[^\s`)]+/scripts)[\\/][\w./-]+\.(?:py|ps1|sh))",
    re.I,
)
MCP_RE = re.compile(r"\bmcp_[a-z0-9_]+", re.I)


# ---------------------------------------------------------------------------
# Step 0 - Warmup
# ---------------------------------------------------------------------------

def step_0_warmup(out_dir: Path, prompt: str, date: datetime.date) -> dict:
    print("Step 0 - Warmup")
    if not SKILLS_DIR.is_dir():
        raise SystemExit(f"Skills directory not found: {SKILLS_DIR}")
    skill_dirs = sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir())
    have_md = [d for d in skill_dirs if (d / "SKILL.md").exists()]
    missing_md = [d.name for d in skill_dirs if not (d / "SKILL.md").exists()]
    out_dir.mkdir(parents=True, exist_ok=True)
    report = out_dir / f"skills_report_{date.strftime('%Y%m%d')}.md"
    print(f"  skills_dir: {SKILLS_DIR}")
    print(f"  total_dirs: {len(skill_dirs)}  with_skill_md: {len(have_md)}")
    if missing_md:
        print(f"  missing SKILL.md in: {', '.join(missing_md)}")
    print(f"  out_dir: {out_dir}")
    print(f"  report:  {report}")
    return {"skill_dirs": have_md, "report": report, "prompt": prompt, "date": date}


# ---------------------------------------------------------------------------
# Step 1 - Read All SKILL.md Files
# ---------------------------------------------------------------------------

def _extract(skill_dir: Path) -> dict:
    md = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    front = FRONT_RE.search(md)
    name = skill_dir.name
    desc = ""
    if front:
        body = front.group(1)
        m = NAME_RE.search(body)
        if m:
            name = m.group(1).strip()
        m = DESC_RE.search(body)
        if m:
            desc = m.group(1).strip()
    step_nums = [int(x) for x in STEP_NUM_RE.findall(md)]
    if step_nums:
        steps_count = len(step_nums)
        steps_range = f"Step {min(step_nums)}-{max(step_nums)}"
    else:
        steps_count = len(STEP_RE.findall(md))
        steps_range = f"{steps_count} steps" if steps_count else "n/a"
    scripts = sorted({s.replace("/", "\\") for s in SCRIPT_RE.findall(md)})
    mcp = sorted({t for t in MCP_RE.findall(md)})
    outputs: list[str] = []
    for pat, label in OUTPUT_HINTS:
        if re.search(pat, md, re.I) and label not in outputs:
            outputs.append(label)
    return {
        "dir_name": skill_dir.name,
        "name": name,
        "desc": desc,
        "steps_count": steps_count,
        "steps_range": steps_range,
        "step_titles": STEP_TITLE_RE.findall(md),
        "scripts": scripts,
        "mcp": mcp,
        "outputs": outputs,
    }


def _categorize(s: dict) -> str:
    n = s["dir_name"]
    if n.startswith("build-") or n in {"download-smbios", "render-md", "run-pr", "sw-lifecycle"}:
        return "Build/Create"
    if n.startswith("check-"):
        return "Check/Validate"
    if n.startswith("compare-"):
        return "Compare"
    if n.startswith("report-") or n == "trace-test-case":
        return "Report"
    if n.startswith("triage-") or n.startswith("review-"):
        return "Triage"
    return "Utility/Format"


def step_1_read_all_skill_md_files(skill_dirs: list[Path]) -> list[dict]:
    print("Step 1 - Read All SKILL.md Files")
    skills = []
    for d in skill_dirs:
        s = _extract(d)
        s["category"] = _categorize(s)
        skills.append(s)
    print(f"  parsed {len(skills)} skills")
    return skills


# ---------------------------------------------------------------------------
# Step 2 - Summary Table
# ---------------------------------------------------------------------------

def step_2_summary_table(skills: list[dict]) -> list[str]:
    print("Step 2 - Summary Table")
    md = ["## Summary Table", "",
          "| # | Skill | Steps | Scripts | MCP | Primary Output |",
          "|---|-------|-------|---------|-----|----------------|"]
    for i, s in enumerate(skills, 1):
        out = ", ".join(s["outputs"]) if s["outputs"] else "-"
        md.append(
            f"| {i} | **{s['dir_name']}** | {s['steps_count']} | "
            f"{len(s['scripts'])} | {'Yes' if s['mcp'] else 'No'} | {out} |"
        )
    md.append("")
    return md


# ---------------------------------------------------------------------------
# Step 3 - Skills Description
# ---------------------------------------------------------------------------

def step_3_skills_description(skills: list[dict]) -> list[str]:
    print("Step 3 - Skills Description")
    md = ["## Skills Description", "",
          "| Skill | Description |",
          "|-------|-------------|"]
    for s in sorted(skills, key=lambda x: x["dir_name"]):
        desc = (s["desc"] or "(no description)").replace("|", "\\|")
        md.append(f"| **{s['dir_name']}** | {desc} |")
    md.append("")
    return md


# ---------------------------------------------------------------------------
# Step 4 - Category Breakdown
# ---------------------------------------------------------------------------

def step_4_category_breakdown(skills: list[dict]) -> list[str]:
    print("Step 4 - Category Breakdown")
    md = ["## Category Breakdown", ""]
    groups: dict[str, list[dict]] = defaultdict(list)
    for s in skills:
        groups[s["category"]].append(s)
    for cat in CATEGORIES_ORDER:
        items = sorted(groups.get(cat, []), key=lambda x: x["dir_name"])
        if not items:
            continue
        total_steps = sum(x["steps_count"] for x in items)
        total_scripts = sum(len(x["scripts"]) for x in items)
        md.append(f"### {cat}")
        md.append("")
        md.append(
            f"- **Skills**: {len(items)}  **Steps**: {total_steps}  "
            f"**Scripts**: {total_scripts}"
        )
        md.append("")
        md.append("| Skill | Description |")
        md.append("|-------|-------------|")
        for s in items:
            desc = (s["desc"] or "(no description)").replace("|", "\\|")
            md.append(f"| **{s['dir_name']}** | {desc} |")
        md.append("")
    return md


# ---------------------------------------------------------------------------
# Step 5 - Key Metrics
# ---------------------------------------------------------------------------

def step_5_key_metrics(skills: list[dict]) -> list[str]:
    print("Step 5 - Key Metrics")
    total_steps = sum(s["steps_count"] for s in skills)
    total_scripts = sum(len(s["scripts"]) for s in skills)
    mcp_skills = [s["dir_name"] for s in skills if s["mcp"]]
    md = ["## Key Metrics", "",
          f"- **Total skills**: {len(skills)}",
          f"- **Total steps**: {total_steps}",
          f"- **Total scripts**: {total_scripts}",
          f"- **Skills using MCP**: {len(mcp_skills)}"]
    if mcp_skills:
        md.append(f"- **MCP skills**: {', '.join(f'`{n}`' for n in sorted(mcp_skills))}")
    md.append("")
    fmt_count: dict[str, list[str]] = defaultdict(list)
    for s in skills:
        for o in s["outputs"]:
            fmt_count[o].append(s["dir_name"])
    md.append("### Output format breakdown")
    md.append("")
    md.append("| Format | Count | Skills |")
    md.append("|--------|-------|--------|")
    for fmt in sorted(fmt_count, key=lambda k: -len(fmt_count[k])):
        names = sorted(fmt_count[fmt])
        sample = ", ".join(names[:8])
        if len(names) > 8:
            sample += f", … (+{len(names) - 8})"
        md.append(f"| {fmt} | {len(names)} | {sample} |")
    md.append("")
    return md


# ---------------------------------------------------------------------------
# Step 6 - Per-Skill Details
# ---------------------------------------------------------------------------

def step_6_per_skill_details(skills: list[dict]) -> list[str]:
    print("Step 6 - Per-Skill Details")
    md = ["## Per-Skill Details", ""]
    for s in sorted(skills, key=lambda x: x["dir_name"]):
        md.append(f"### {s['dir_name']}")
        md.append("")
        md.append(f"- **Description**: {s['desc'] or '(no description)'}")
        if s["step_titles"]:
            md.append(f"- **Steps** ({s['steps_range']}):")
            for i, t in enumerate(s["step_titles"]):
                md.append(f"  - Step {i}: {t}")
        else:
            md.append(f"- **Steps**: {s['steps_range']}")
        md.append(
            "- **Scripts**: "
            + (", ".join(f"`{p}`" for p in s["scripts"]) if s["scripts"] else "None")
        )
        md.append(
            "- **MCP tools**: "
            + (", ".join(f"`{m}`" for m in s["mcp"]) if s["mcp"] else "None")
        )
        md.append(f"- **Output**: {', '.join(s['outputs']) if s['outputs'] else '-'}")
        md.append("")
    return md


# ---------------------------------------------------------------------------
# Header + main
# ---------------------------------------------------------------------------

def _header(skills_count: int, prompt: str, date: datetime.date) -> list[str]:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    return [
        f"# Skills Report - {date.strftime('%Y-%m-%d')}",
        "",
        "- **Skill**: report-skills",
        f"- **Created**: {now}",
        f"- **Updated**: {now}",
        "- **Prompt**:",
        "",
        "```text",
        prompt,
        "```",
        "",
        f"Found **{skills_count}** skills under `.github\\skills\\`. "
        "All directories contain a `SKILL.md`.",
        "",
    ]


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate a Skills Report from .github/skills/*/SKILL.md")
    ap.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR), help="Output directory (default: wiki/report-skills)")
    ap.add_argument("--date", default=None, help="Override report date (yyyy-MM-dd; default: today)")
    ap.add_argument("--prompt", default=DEFAULT_PROMPT, help="Prompt text recorded in the report header")
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    date = (
        datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
        if args.date
        else datetime.date.today()
    )

    ctx = step_0_warmup(out_dir, args.prompt, date)
    skills = step_1_read_all_skill_md_files(ctx["skill_dirs"])

    body: list[str] = []
    body += _header(len(skills), ctx["prompt"], ctx["date"])
    body += step_2_summary_table(skills)
    body += step_3_skills_description(skills)
    body += step_4_category_breakdown(skills)
    body += step_5_key_metrics(skills)
    body += step_6_per_skill_details(skills)

    report_path: Path = ctx["report"]
    report_path.write_text("\n".join(body), encoding="utf-8")

    total_steps = sum(s["steps_count"] for s in skills)
    total_scripts = sum(len(s["scripts"]) for s in skills)
    mcp_count = sum(1 for s in skills if s["mcp"])
    print(f"Wrote {report_path} ({report_path.stat().st_size} bytes)")
    print(f"skills={len(skills)} steps={total_steps} scripts={total_scripts} mcp={mcp_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
