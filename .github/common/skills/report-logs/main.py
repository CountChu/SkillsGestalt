"""Compiled runner for the `report-logs` skill.

Description (from SKILL.md):
    The skill reads all MD files in the wiki directory, extracts
    Created/Updated timestamps, and displays a build log grouped by date.

Step classification:
    Step 0  Warmup ............................... compiled
    Step 1  Collect Metadata via report-metadata . compiled (freshness check only)
    Step 2  Group by Updated Date ................ compiled
    Step 3  Group by Created Date ................ compiled
    Step 4  Group by Skill ....................... compiled
    Step 5  Group by Tag ......................... compiled
    Step 6  Group by Status ...................... compiled
    Step 7  Save Report by Updated ............... compiled
    Step 8  Save Report by Created ............... compiled
    Step 9  Save Report by Tag ................... compiled
    Step 10 Save Report by Status ................ compiled
    Step 11 Save Report by Skill ................. compiled
    Step 12 Summarize Run Time ................... compiled

Overall: FULLY COMPILED.

Usage:
    python .github\\skills\\report-logs\\main.py
    python .github\\skills\\report-logs\\main.py --only-step 7

Step 1 only verifies that ``database/metadata.yaml`` is fresh (exists, and no
wiki MD file has been modified since it was last written). If it is stale, the
runner prints instructions to run the ``report-metadata`` skill via the agent
and exits non-zero -- it never invokes ``read_metadata.py`` itself, because the
report-metadata skill's LLM summarization phase has no deterministic equivalent.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
SKILL_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
WIKI_DIR = WORKSPACE_ROOT / "wiki"
METADATA_YAML = WORKSPACE_ROOT / "database" / "metadata.yaml"
CHECKPOINT_DIR = WORKSPACE_ROOT / "checkpoints" / "report-logs"

MANUAL_STEPS: list[str] = []
TIMINGS: list[dict] = []

STEP_NAMES = {
    0: "Warmup",
    1: "Collect Metadata via report-metadata Skill",
    2: "Group by Updated Date",
    3: "Group by Created Date",
    4: "Group by Skill",
    5: "Group by Tag",
    6: "Group by Status",
    7: "Save Report by Updated",
    8: "Save Report by Created",
    9: "Save Report by Tag",
    10: "Save Report by Status",
    11: "Save Report by Skill",
    12: "Summarize Run Time",
}


def _manual(step: int, why: str, action: str) -> None:
    msg = f"[manual] Step {step} ({STEP_NAMES.get(step, '?')}): {why} -> {action}"
    print(msg)
    MANUAL_STEPS.append(msg)


def _fmt_ts(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def _fmt_taken(seconds: float) -> str:
    total = int(round(seconds))
    return f"{total // 60}m {total % 60}s"


def _run(step: int, fn, *args, **kwargs):
    name = STEP_NAMES.get(step, f"Step {step}")
    print(f"\n## Step {step} - {name}")
    begin_dt = datetime.now()
    begin_s = time.monotonic()
    try:
        result = fn(*args, **kwargs)
    finally:
        end_dt = datetime.now()
        end_s = time.monotonic()
        TIMINGS.append({
            "step": step,
            "name": name,
            "begin": _fmt_ts(begin_dt),
            "end": _fmt_ts(end_dt),
            "taken": _fmt_taken(end_s - begin_s),
        })
    return result


def _exec(cmd: list[str]) -> int:
    print("> " + " ".join(cmd))
    proc = subprocess.run(cmd, cwd=str(WORKSPACE_ROOT))
    return proc.returncode


def _py(script: Path, *script_args: str) -> int:
    return _exec([sys.executable, str(script), *script_args])


# ---------------------------------------------------------------------------
# Step implementations
# ---------------------------------------------------------------------------

def step_0_warmup() -> int:
    if not WIKI_DIR.is_dir():
        print(f"ERROR: wiki directory not found: {WIKI_DIR}")
        return 1
    subdirs = sorted(p for p in WIKI_DIR.iterdir() if p.is_dir())
    md_files = [
        p for p in WIKI_DIR.rglob("*.md")
        if ".obsidian" not in p.parts and "images" not in p.parts
    ]
    print(f"wiki subdirectories: {len(subdirs)}")
    print(f"total .md files (excluding .obsidian/, images/): {len(md_files)}")
    return 0


def step_1_collect_metadata() -> int:
    rel_meta = METADATA_YAML.relative_to(WORKSPACE_ROOT)
    if not METADATA_YAML.is_file():
        print(f"ERROR: {rel_meta} does not exist.")
        print("Please run the `report-metadata` skill via the agent to generate it,")
        print("then re-run this script.")
        return 1
    meta_mtime = METADATA_YAML.stat().st_mtime
    newer: list[Path] = []
    for p in WIKI_DIR.rglob("*.md"):
        if ".obsidian" in p.parts or "images" in p.parts or "report-logs" in p.parts:
            continue
        if p.stat().st_mtime > meta_mtime:
            newer.append(p)
    if newer:
        meta_ts = _fmt_ts(datetime.fromtimestamp(meta_mtime))
        print(f"ERROR: {rel_meta} is stale (last written {meta_ts}).")
        print(f"  {len(newer)} wiki MD file(s) have been modified since; first few:")
        for p in newer[:5]:
            p_ts = _fmt_ts(datetime.fromtimestamp(p.stat().st_mtime))
            print(f"    - {p.relative_to(WORKSPACE_ROOT)}  ({p_ts})")
        print("Please run the `report-metadata` skill via the agent to refresh it,")
        print("then re-run this script.")
        return 1
    meta_ts = _fmt_ts(datetime.fromtimestamp(meta_mtime))
    print(f"{rel_meta} is up to date (last written {meta_ts}).")
    return 0


def _group_step(script_name: str) -> int:
    return _py(
        SCRIPTS_DIR / script_name,
        str(METADATA_YAML.relative_to(WORKSPACE_ROOT)),
        "--output-dir",
        str(CHECKPOINT_DIR.relative_to(WORKSPACE_ROOT)),
    )


def step_2_group_by_date() -> int:
    return _group_step("group_by_date.py")


def step_3_group_by_created() -> int:
    return _group_step("group_by_created.py")


def step_4_group_by_skill() -> int:
    return _group_step("group_by_skill.py")


def step_5_group_by_tag() -> int:
    return _group_step("group_by_tag.py")


def step_6_group_by_status() -> int:
    return _group_step("group_by_status.py")


def _save_step(script_name: str) -> int:
    return _py(
        SCRIPTS_DIR / script_name,
        str(CHECKPOINT_DIR.relative_to(WORKSPACE_ROOT)),
    )


def step_7_save_by_updated() -> int:
    return _save_step("save_report.py")


def step_8_save_by_created() -> int:
    return _save_step("save_report_by_created.py")


def step_9_save_by_tag() -> int:
    return _save_step("save_report_by_tag.py")


def step_10_save_by_status() -> int:
    return _save_step("save_report_by_status.py")


def step_11_save_by_skill() -> int:
    return _save_step("save_report_by_skill.py")


def step_12_summarize_timing(overall_begin: datetime, overall_end: datetime) -> int:
    out_path = CHECKPOINT_DIR / "s12-timing.yaml"
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    total_seconds = (overall_end - overall_begin).total_seconds()
    lines = [
        "skill: report-logs",
        f"begin: {_fmt_ts(overall_begin)}",
        f"end: {_fmt_ts(overall_end)}",
        f"total: {_fmt_taken(total_seconds)}",
        "steps:",
    ]
    for entry in TIMINGS:
        if entry["step"] == 12:
            continue
        lines.append(f"  - step: {entry['step']}")
        lines.append(f"    name: {entry['name']}")
        lines.append(f"    begin: {entry['begin']}")
        lines.append(f"    end: {entry['end']}")
        lines.append(f"    taken: {entry['taken']}")
    content = "\n".join(lines) + "\n"
    out_path.write_text(content, encoding="utf-8")
    print(f"Wrote {out_path}")
    print("---")
    print(content, end="")
    print("---")
    return 0


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

STEP_REGISTRY = {
    0: ("step_0_warmup", lambda args: step_0_warmup()),
    1: ("step_1_collect_metadata", lambda args: step_1_collect_metadata()),
    2: ("step_2_group_by_date", lambda args: step_2_group_by_date()),
    3: ("step_3_group_by_created", lambda args: step_3_group_by_created()),
    4: ("step_4_group_by_skill", lambda args: step_4_group_by_skill()),
    5: ("step_5_group_by_tag", lambda args: step_5_group_by_tag()),
    6: ("step_6_group_by_status", lambda args: step_6_group_by_status()),
    7: ("step_7_save_by_updated", lambda args: step_7_save_by_updated()),
    8: ("step_8_save_by_created", lambda args: step_8_save_by_created()),
    9: ("step_9_save_by_tag", lambda args: step_9_save_by_tag()),
    10: ("step_10_save_by_status", lambda args: step_10_save_by_status()),
    11: ("step_11_save_by_skill", lambda args: step_11_save_by_skill()),
}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compiled runner for the report-logs skill (Steps 0-12).",
    )
    parser.add_argument(
        "--only-step",
        type=int,
        choices=sorted(STEP_REGISTRY.keys()) + [12],
        help="Run only the given step (0-12). Useful for re-running save_* steps.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

    overall_begin = datetime.now()

    if args.only_step is not None:
        target = args.only_step
        if target == 12:
            overall_end = datetime.now()
            _run(12, step_12_summarize_timing, overall_begin, overall_end)
            return 0
        _, fn = STEP_REGISTRY[target]
        rc = _run(target, fn, args)
        if rc:
            print(f"\nStep {target} failed with exit code {rc}.")
            return rc
    else:
        for step in sorted(STEP_REGISTRY.keys()):
            _, fn = STEP_REGISTRY[step]
            rc = _run(step, fn, args)
            if rc:
                print(f"\nStep {step} failed with exit code {rc}. Aborting.")
                return rc
        overall_end = datetime.now()
        _run(12, step_12_summarize_timing, overall_begin, overall_end)

    if MANUAL_STEPS:
        print("\nManual steps remaining:")
        for m in MANUAL_STEPS:
            print(f"  - {m}")
        return 2

    print("\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
