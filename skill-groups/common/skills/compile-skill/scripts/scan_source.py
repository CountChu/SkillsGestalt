"""Validate a Skill Source and print its step inventory.

This is the design document's Source Scanner, as this skill implements it: its command-line
contract is section 2.7 (CLI), and how it reaches its verdict section 3.2
(Execution Flow).

The compile-skill design document accepts a Skill Source only as a `SKILL.md` directly inside a
directory under a `skills` directory, with `Step N` headings under its `Workflow` section
(sections 2.3, Exception Paths, and 2.4, Naming and Data Structures), and gives every Step Action
a unique identifier (section 2.5, Step Identifier). This script decides that verdict and prints
the inventory a compiler works from. It writes no file.

It also prints the source fingerprint a compiled skill.py records as SOURCE_SHA256 (section 2.5,
Source Fingerprint). source_fingerprint() is the one implementation of it:
check_compiled.py imports it, so the value written at compile time and the value checked later
can never be computed two different ways.

For each step it also lists the programs the step runs - every file name with a program extension
inside the step's inline code or fenced blocks - and whether each is in the skill's directory. Which
of a Deterministic step's work is core work and which a chore is a person's decision, not this
script's (section 2.5, Core Work or Chore); this list only says where a
program exists to be called.

Exit codes: 0 valid, 2 INVALID (stop - no skill.py may be written), 64 no verdict - the command
was malformed, or the file is missing or cannot be read. A usage error exits 64 rather than
argparse's 2, which would read as an INVALID source.

Usage:
    python scan_source.py --file <skills-root>/skills/<name>/SKILL.md
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import NoReturn

import yaml

FENCE_RE = re.compile(r"^\s*(```|~~~)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
STEP_RE = re.compile(r"^Step\s+(\d+)(?=$|\s|[-–—:])\s*(?:[-–—:]\s*)?(.*)$", re.IGNORECASE)
NEAR_STEP_RE = re.compile(r"^Step\s*\d", re.IGNORECASE)
CODE_SPAN_RE = re.compile(r"(`+)(.+?)\1")
PROGRAM_RE = re.compile(r"([\w.-]+\.(?:py|js|mjs|cjs|ts|sh|ps1|cmd|bat))(?![\w.])")
SKIP_DIRS = {"__pycache__", "node_modules", ".git"}
INVALID_EXIT = 2
NO_VERDICT_EXIT = 64  # design document 2.7: no verdict, distinct from INVALID


class Parser(argparse.ArgumentParser):
    """An argument parser whose usage errors exit NO_VERDICT_EXIT, not argparse's 2."""

    def error(self, message: str) -> NoReturn:
        self.print_usage(sys.stderr)
        self.exit(NO_VERDICT_EXIT, f"{self.prog}: error: {message}\n")


@dataclass
class Step:
    id: str
    title: str
    line: int
    end: int
    programs: list[tuple[str, bool]] = field(default_factory=list)  # (file name, found in the skill's directory)


@dataclass
class Scan:
    path: Path
    fingerprint: str = ""
    shape_ok: bool = False
    frontmatter: dict | None = None
    frontmatter_error: str | None = None
    workflow_line: int | None = None
    steps: list[Step] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        return not self.errors

    @property
    def skill_name(self) -> str:
        name = (self.frontmatter or {}).get("name")
        return str(name) if name else self.path.parent.name


def split_frontmatter(text: str) -> tuple[dict | None, str | None]:
    if not text.startswith("---"):
        return None, None
    end = text.find("\n---", 3)
    if end == -1:
        return None, "frontmatter is never closed"
    try:
        data = yaml.safe_load(text[3:end])
    except yaml.YAMLError as exc:
        return None, str(exc).replace("\n", " ")
    return (data, None) if isinstance(data, dict) else (None, "frontmatter is not a mapping")


def source_fingerprint(path: str | Path) -> str:
    """SHA-256 of the text decoded as UTF-8, any BOM removed and line endings normalized to LF.

    Normalizing makes the fingerprint describe the text rather than the bytes, so a CRLF checkout
    of an unchanged SKILL.md is not mistaken for an edited one.
    """
    text = Path(path).read_bytes().decode("utf-8-sig")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def headings(lines: list[str]) -> list[tuple[int, int, str]]:
    """(line number, level, text) of every heading outside a fenced block."""
    out, fenced = [], False
    for i, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            fenced = not fenced
            continue
        m = None if fenced else HEADING_RE.match(line)
        if m:
            out.append((i, len(m.group(1)), m.group(2).strip().strip("*").strip()))
    return out


def step_programs(lines: list[str], start: int, end: int, skill_dir: Path) -> list[tuple[str, bool]]:
    """Program file names in a step's inline code and fenced blocks, each with whether the skill has it."""
    names: list[str] = []
    fenced = False
    for line in lines[start - 1:end]:
        if FENCE_RE.match(line):
            fenced = not fenced
            continue
        texts = [line] if fenced else [m.group(2) for m in CODE_SPAN_RE.finditer(line)]
        for text in texts:
            for m in PROGRAM_RE.finditer(text):
                if m.group(1) not in names:
                    names.append(m.group(1))
    present = {f.name for f in skill_dir.rglob("*") if f.is_file() and not SKIP_DIRS & set(f.parts)}
    return [(n, n in present) for n in names]


def scan(path: str | Path) -> Scan:
    p = Path(path)
    result = Scan(path=p)
    resolved = p.resolve()
    result.shape_ok = resolved.name == "SKILL.md" and resolved.parent.parent.name == "skills"
    if not result.shape_ok:
        result.errors.append(f"not a Skill Source path: expected .../skills/<name>/SKILL.md, got {p}")

    text = p.read_text(encoding="utf-8-sig")
    result.fingerprint = source_fingerprint(p)
    lines = text.splitlines()
    result.frontmatter, result.frontmatter_error = split_frontmatter(text)
    if result.frontmatter is None and result.frontmatter_error is None:
        result.warnings.append("no frontmatter - skill_name falls back to the directory name")

    heads = headings(lines)
    wf = next(((i, lvl) for i, lvl, t in heads if t.lower() == "workflow"), None)
    if wf is None:
        result.errors.append("no Workflow section")
        return result
    result.workflow_line, wf_level = wf

    section = []
    for i, lvl, t in heads:
        if i <= result.workflow_line:
            continue
        if lvl <= wf_level:
            break
        section.append((i, lvl, t))
    section_end = next((i - 1 for i, lvl, _ in heads if i > result.workflow_line and lvl <= wf_level), len(lines))

    for n, (i, lvl, t) in enumerate(section):
        m = STEP_RE.match(t)
        if not m:
            if NEAR_STEP_RE.match(t):
                result.warnings.append(f"L{i} '{t}' looks like a step but is not 'Step N' - it is not a Step Action")
            continue
        end = next((j - 1 for j, l2, _ in section[n + 1:] if l2 <= lvl), section_end)
        result.steps.append(Step(id=m.group(1).lstrip("0") or "0", title=m.group(2).strip().strip("*").strip(), line=i, end=end,
                                 programs=step_programs(lines, i, end, resolved.parent)))

    if not result.steps:
        result.errors.append(f"no 'Step N' headings under the Workflow section (L{result.workflow_line})")
        return result

    seen: dict[str, int] = {}
    for s in result.steps:
        if s.id in seen:
            result.errors.append(f"Step {s.id} appears twice (L{seen[s.id]}, L{s.line}) - a Step Action needs a unique identifier")
        seen.setdefault(s.id, s.line)
    numbers = [int(s.id) for s in result.steps]
    if numbers != sorted(numbers):
        result.warnings.append(f"steps are not in ascending order: {numbers}")
    for a, b in zip(sorted(set(numbers)), sorted(set(numbers))[1:]):
        if b != a + 1:
            result.warnings.append(f"step numbers skip from {a} to {b}")
    return result


def main() -> int:
    ap = Parser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--file", required=True, help="path to the Skill Source (SKILL.md)")
    args = ap.parse_args()
    try:
        result = scan(args.file)
    except (OSError, UnicodeDecodeError) as exc:
        print(f"cannot read {args.file}: {exc}")
        return NO_VERDICT_EXIT

    print(f"file: {result.path}")
    print(f"path shape: {'ok' if result.shape_ok else 'INVALID'}")
    if result.frontmatter is not None:
        desc = str(result.frontmatter.get("description") or "")
        print(f"frontmatter: name={result.frontmatter.get('name')!r}, description {len(desc)} chars")
    else:
        print(f"frontmatter: {'UNPARSEABLE - ' + result.frontmatter_error if result.frontmatter_error else 'missing'}")
    print(f"skill_name: {result.skill_name}")
    print(f"fingerprint: {result.fingerprint}")
    print(f"workflow: {'L' + str(result.workflow_line) if result.workflow_line else 'MISSING'}")

    print(f"\n-- step inventory ({len(result.steps)}) --")
    for s in result.steps:
        progs = ", ".join(f"{n} ({'here' if found else 'not in this skill'})" for n, found in s.programs) or "none"
        print(f"  Step {s.id:<3} L{s.line}-{s.end}  {s.title}  [programs: {progs}]")

    if result.warnings:
        print(f"\n-- warnings ({len(result.warnings)}) --")
        for w in result.warnings:
            print(f"  - {w}")

    print(f"\nverdict: {'valid' if result.valid else 'INVALID'}")
    if not result.valid:
        for e in result.errors:
            print(f"  - {e}")
        print("\nSTOP: the Skill Source does not conform - write no skill.py.")
        return INVALID_EXIT
    return 0


if __name__ == "__main__":
    sys.exit(main())
