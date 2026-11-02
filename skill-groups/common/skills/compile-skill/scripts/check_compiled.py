"""Check a compiled skill.py against the interface contracts of the compile-skill design document.

This is the design document's Contract Checker, as this skill implements it: its command-line
contract is section 2.7 (CLI), and the order of its checks section 3.2
(Execution Flow).

Every run of the script happens in a fresh, empty temporary directory outside the workspace - so
no workspace config.yaml can be found from it - with nothing on stdin, and no deterministic step
is asked to do its real work: only --help, --export-schema, an unknown step identifier, each
cognitive step's handoff, and each deterministic interactive step with its required arguments
left out. The script's own directory must be unchanged afterwards.

Before anything runs, the source fingerprint the script records (SOURCE_SHA256) is compared with
the Skill Source as it is now, read by parsing the file rather than importing it (section 2.4,
Naming and Data Structures). A missing or different fingerprint means the script is
stale, and nothing else is checked: a stale script is recompiled, never fixed (section 2.7, CLI).

Exit codes: 0 every check passed, 1 at least one failed, 2 the Skill Source is INVALID, 4 the
Compiled Script is stale - 4 rather than 3, which is the Compiled Script's own handoff code - and
64 no verdict: the command was malformed, or a file it names is missing or cannot be read.

Usage:
    python check_compiled.py --source <skills-root>/skills/<name>/SKILL.md --script <skills-root>/skills/<name>/skill.py
"""
from __future__ import annotations

import ast
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

from scan_source import INVALID_EXIT, NO_VERDICT_EXIT, Parser, scan

REFUSAL_EXIT = 2  # design document section 2.7, CLI: a refusal before any work
HANDOFF_EXIT = 3  # design document section 2.7, CLI: the dedicated handoff status code
STALE_EXIT = 4  # the stale code: this checker's verdict, and what a stale skill.py itself exits with (design document 2.7)
HANDOFF_TEXT = "This step is a cognitive task and cannot be processed by this system."
TYPES = ("deterministic_automated", "cognitive_automated", "deterministic_interactive", "cognitive_interactive")
COGNITIVE = {"cognitive_automated", "cognitive_interactive"}
STEP_KEYS = ("id", "name", "type", "description", "arguments")
ARG_KEYS = ("name", "required", "type", "description")
ARG_TYPES = ("string", "integer", "number", "boolean", "path")  # design document section 2.4: an argument's data type
BLOCKING_CLICK = {"prompt", "confirm", "pause", "getchar", "edit", "password_option", "confirmation_option"}
UNKNOWN_STEP = "no-such-step"


class Checker:
    def __init__(self) -> None:
        self.failures: list[str] = []

    def check(self, name: str, ok: bool, detail: str = "") -> bool:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}{(' - ' + detail) if detail else ''}")
        if not ok:
            self.failures.append(name)
        return ok


def run(script: Path, args: list[str], cwd: Path, timeout: float) -> subprocess.CompletedProcess[str] | None:
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    try:
        return subprocess.run(
            [sys.executable, str(script), *args],
            cwd=cwd, env=env, stdin=subprocess.DEVNULL, capture_output=True,
            encoding="utf-8", errors="replace", timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return None


def said(proc: subprocess.CompletedProcess[str] | None) -> str:
    if proc is None:
        return "timed out - did it wait for input?"
    text = (proc.stdout + proc.stderr).strip().splitlines()
    return f"exit {proc.returncode}" + (f", said {text[-1][:120]!r}" if text else ", said nothing")


def snapshot(root: Path) -> dict[str, tuple[int, int]]:
    return {
        str(p.relative_to(root)): (p.stat().st_size, p.stat().st_mtime_ns)
        for p in root.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
    }


def call_name(node: ast.Call) -> tuple[str | None, str]:
    """(module the callee was reached through, callee name) for `mod.f(...)` and `f(...)`."""
    f = node.func
    if isinstance(f, ast.Attribute):
        return (f.value.id if isinstance(f.value, ast.Name) else None), f.attr
    return None, f.id if isinstance(f, ast.Name) else ""


def blocking_calls(tree: ast.AST) -> list[str]:
    imported: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module in ("click", "getpass", "sys"):
            for alias in node.names:
                imported[alias.asname or alias.name] = f"{node.module}.{alias.name}"
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            mod, name = call_name(node)
            origin = f"{mod}.{name}" if mod else imported.get(name, name)
            if origin in ("input", "raw_input", "getpass.getpass") or (
                origin.startswith("click.") and origin.split(".", 1)[1] in BLOCKING_CLICK
            ):
                found.append(f"L{node.lineno} {origin}()")
            if origin in ("click.option", "click.argument"):
                for kw in node.keywords:
                    quiet = isinstance(kw.value, ast.Constant) and kw.value.value in (False, None, "")
                    if kw.arg in ("prompt", "confirmation_prompt") and not quiet:
                        found.append(f"L{node.lineno} {origin}({kw.arg}=...)")
        elif isinstance(node, ast.Attribute) and node.attr == "stdin" and isinstance(node.value, ast.Name) and node.value.id == "sys":
            found.append(f"L{node.lineno} sys.stdin")
        elif isinstance(node, ast.Name) and imported.get(node.id) == "sys.stdin":
            found.append(f"L{node.lineno} sys.stdin")
    return sorted(set(found), key=lambda s: int(s.split()[0][1:]))


def unannotated(tree: ast.AST) -> list[str]:
    out = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            a = node.args
            params = [*a.posonlyargs, *a.args, *a.kwonlyargs, *(p for p in (a.vararg, a.kwarg) if p)]
            missing = [p.arg for p in params if p.annotation is None and p.arg not in ("self", "cls")]
            if node.returns is None:
                missing.append("return")
            if missing:
                out.append(f"L{node.lineno} {node.name}({', '.join(missing)})")
    return out


def recorded(tree: ast.Module, name: str) -> str | None:
    """The string literal a module-level `NAME = "..."` assigns, read without running the script."""
    for node in tree.body:
        targets = node.targets if isinstance(node, ast.Assign) else [node.target] if isinstance(node, ast.AnnAssign) else []
        if any(isinstance(t, ast.Name) and t.id == name for t in targets):
            value = node.value
            return value.value if isinstance(value, ast.Constant) and isinstance(value.value, str) else None
    return None


def iso_with_offset(value: str | None) -> bool:
    if not value:
        return False
    try:
        stamp = datetime.fromisoformat(value[:-1] + "+00:00" if value.endswith("Z") else value)
    except ValueError:
        return False
    return stamp.tzinfo is not None


def imports_click(tree: ast.AST) -> bool:
    return any(
        (isinstance(n, ast.Import) and any(a.name == "click" for a in n.names))
        or (isinstance(n, ast.ImportFrom) and n.module == "click")
        for n in ast.walk(tree)
    )


def schema_problems(schema: object) -> list[str]:
    if not isinstance(schema, dict):
        return ["the top level is not an object"]
    problems = []
    if not isinstance(schema.get("skill_name"), str) or not schema["skill_name"].strip():
        problems.append("skill_name is missing or empty")
    steps = schema.get("steps")
    if not isinstance(steps, list) or not steps:
        return problems + ["steps is missing or empty"]
    seen: set[str] = set()
    for i, s in enumerate(steps):
        where = f"steps[{i}]"
        if not isinstance(s, dict):
            problems.append(f"{where} is not an object")
            continue
        missing = [k for k in STEP_KEYS if k not in s]
        if missing:
            problems.append(f"{where} lacks {', '.join(missing)}")
        sid = s.get("id")
        if not isinstance(sid, str) or not sid.strip():
            problems.append(f"{where} id {sid!r} is not a non-empty string")
        elif sid in seen:
            problems.append(f"{where} id {sid!r} is not unique")
        else:
            seen.add(sid)
        if s.get("type") not in TYPES:
            problems.append(f"{where} type {s.get('type')!r} is not one of {', '.join(TYPES)}")
        for key in ("name", "description"):
            if key in s and (not isinstance(s[key], str) or not s[key].strip()):
                problems.append(f"{where} {key} is not a non-empty string")
        args = s.get("arguments")
        if not isinstance(args, list):
            problems.append(f"{where} arguments is not a list")
            continue
        for j, arg in enumerate(args):
            if not isinstance(arg, dict) or any(k not in arg for k in ARG_KEYS):
                problems.append(f"{where}.arguments[{j}] lacks one of {', '.join(ARG_KEYS)}")
            elif not isinstance(arg["name"], str) or not arg["name"] or not isinstance(arg["required"], bool):
                problems.append(f"{where}.arguments[{j}] needs a string name and a boolean required")
            elif arg["type"] not in ARG_TYPES:
                problems.append(f"{where}.arguments[{j}] type {arg['type']!r} is not one of {', '.join(ARG_TYPES)}")
    return problems


def required_args(step: dict) -> list[str]:
    return [a["name"] for a in step.get("arguments", []) if isinstance(a, dict) and a.get("required") is True]


def main() -> int:
    ap = Parser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--source", required=True, help="path to the Skill Source (SKILL.md)")
    ap.add_argument("--script", required=True, help="path to the Compiled Script (skill.py)")
    ap.add_argument("--timeout", type=float, default=60, help="seconds each run may take (default 60)")
    args = ap.parse_args()

    try:
        source = scan(args.source)
    except (OSError, UnicodeDecodeError) as exc:
        print(f"STOP: cannot read {args.source}: {exc}")
        return NO_VERDICT_EXIT
    if not source.valid:
        print("STOP: the Skill Source is INVALID - run scan_source.py for the reason.")
        return INVALID_EXIT
    script = Path(args.script).resolve()
    if not script.is_file():
        print(f"STOP: no Compiled Script at {script}")
        return NO_VERDICT_EXIT

    c = Checker()
    c.check("interpreter is Python 3.10+", sys.version_info >= (3, 10), sys.version.split()[0])

    try:
        tree = ast.parse(script.read_text(encoding="utf-8-sig"), filename=str(script))
    except SyntaxError as exc:
        c.check("script parses", False, f"L{exc.lineno}: {exc.msg}")
        print(f"\n{len(c.failures)} failure(s)")
        return 1

    recorded_sha = recorded(tree, "SOURCE_SHA256")
    compiled_at = recorded(tree, "COMPILED_AT")
    fresh = recorded_sha is not None and recorded_sha == source.fingerprint
    if recorded_sha is None:
        why = "it records no SOURCE_SHA256 string literal"
    else:
        why = (f"the Skill Source changed after {compiled_at or 'an unrecorded time'} "
               f"(recorded {recorded_sha[:12]}..., now {source.fingerprint[:12]}...)")
    c.check("source fingerprint matches the Skill Source", fresh, source.fingerprint[:12] + "..." if fresh else why)
    if not fresh:
        print(f"\nSTOP: the Compiled Script is stale - {why}. Recompile it; never rewrite its fingerprint by hand.")
        return STALE_EXIT
    c.check("COMPILED_AT is an ISO 8601 date-time with a UTC offset", iso_with_offset(compiled_at), repr(compiled_at))

    c.check("CLI is built with click", imports_click(tree))
    blocking = blocking_calls(tree)
    c.check("nothing waits for a person", not blocking, "; ".join(blocking))
    bare = unannotated(tree)
    c.check("every function is type-hinted", not bare, "; ".join(bare))

    before = snapshot(script.parent)
    with tempfile.TemporaryDirectory(prefix="compile-skill-check-") as tmp:
        cwd = Path(tmp)

        helped = run(script, ["--help"], cwd, args.timeout)
        ok = helped is not None and helped.returncode == 0
        c.check("--help exits 0", ok, "" if ok else said(helped))
        if ok:
            c.check("--help lists --step", "--step" in helped.stdout)
            c.check("--export-schema is hidden from --help", "--export-schema" not in helped.stdout)

        exported = run(script, ["--export-schema"], cwd, args.timeout)
        ok = exported is not None and exported.returncode == 0
        c.check("--export-schema exits 0", ok, "" if ok else said(exported))
        schema = None
        if ok:
            try:
                schema = json.loads(exported.stdout)
                c.check("--export-schema stdout is one JSON document and nothing else", True)
            except json.JSONDecodeError as exc:
                first = exported.stdout.strip().splitlines()[:1]
                c.check("--export-schema stdout is one JSON document and nothing else", False, f"{exc.msg}; first line {first}")
        if schema is not None:
            problems = schema_problems(schema)
            c.check("schema has the design document's shape", not problems, "; ".join(problems))
            if not problems:
                steps = schema["steps"]
                c.check("skill_name matches the Skill Source", schema["skill_name"] == source.skill_name,
                        f"{schema['skill_name']!r} vs {source.skill_name!r}")

                print("\n-- Step Actions --")
                for s in steps:
                    marks = ", ".join(a["name"] + ("*" if a["required"] else "") for a in s["arguments"]) or "-"
                    print(f"  {s['id']:<6} {s['type']:<26} {s['name']}  [args: {marks}]")
                print()

                inventory = [s.id for s in source.steps]
                owners: dict[str, list[str]] = {}
                stray = []
                for s in steps:
                    head = s["id"].split(".", 1)[0]
                    (owners.setdefault(head, []) if head in inventory else stray).append(s["id"])
                uncovered = [n for n in inventory if n not in owners]
                doubled = [n for n, ids in owners.items() if n in ids and len(ids) > 1]
                c.check("every source step has a Step Action", not uncovered, ", ".join(f"Step {n}" for n in uncovered))
                c.check("every identifier names a source step", not stray, ", ".join(stray))
                c.check("no source step is both whole and split", not doubled, ", ".join(f"Step {n}" for n in doubled))
                heads = [int(s["id"].split(".", 1)[0]) for s in steps if s["id"].split(".", 1)[0].isdigit()]
                c.check("Step Actions are in source order", heads == sorted(heads))

                # design document 2.5: a program a Deterministic step runs is called, never rewritten
                det_heads = {s["id"].split(".", 1)[0] for s in steps if str(s.get("type", "")).startswith("deterministic_")}
                text = script.read_text(encoding="utf-8-sig")
                uncalled = [f"Step {st.id}: {name}" for st in source.steps if st.id in det_heads
                            for name, found in st.programs if found and name not in text]
                c.check("every program a Deterministic step runs is named in the script", not uncalled, "; ".join(uncalled))

                bad = [s["id"] for s in steps if s["type"] == "deterministic_automated" and required_args(s)]
                c.check("no deterministic_automated step requires an argument", not bad, ", ".join(bad))
                bad = [s["id"] for s in steps if s["type"] == "deterministic_interactive" and not s["arguments"]]
                c.check("every deterministic_interactive step declares an argument", not bad, ", ".join(bad))

                for s in steps:
                    if s["type"] in COGNITIVE:
                        proc = run(script, ["--step", s["id"]], cwd, args.timeout)
                        ok = proc is not None and proc.returncode == HANDOFF_EXIT and HANDOFF_TEXT in proc.stdout + proc.stderr
                        c.check(f"step {s['id']} hands off with exit {HANDOFF_EXIT}", ok, "" if ok else said(proc))
                    elif s["type"] == "deterministic_interactive" and required_args(s):
                        name = required_args(s)[0]
                        proc = run(script, ["--step", s["id"]], cwd, args.timeout)
                        text = "" if proc is None else (proc.stdout + proc.stderr).lower()
                        named = any(form in text for form in {name.lower(), name.lower().replace("_", "-")})
                        ok = proc is not None and proc.returncode == REFUSAL_EXIT and named
                        c.check(f"step {s['id']} refuses a missing {name!r} with exit {REFUSAL_EXIT}", ok, "" if ok else said(proc))

        proc = run(script, ["--step", UNKNOWN_STEP], cwd, args.timeout)
        ok = proc is not None and proc.returncode == REFUSAL_EXIT
        c.check(f"an unknown step identifier is refused with exit {REFUSAL_EXIT}", ok, "" if ok else said(proc))

        left = sorted(str(p.relative_to(cwd)) for p in cwd.rglob("*"))
        c.check("no run wrote into its working directory", not left, ", ".join(left[:5]))

        # design document 2.7: a stale script refuses every invocation itself, with the stale code
        steps_ = schema.get("steps") if isinstance(schema, dict) else None
        first_id = steps_[0].get("id", "0") if isinstance(steps_, list) and steps_ and isinstance(steps_[0], dict) else "0"
        with tempfile.TemporaryDirectory(prefix="compile-skill-stale-") as stale_tmp:
            copy = Path(stale_tmp) / script.parent.name
            shutil.copytree(script.parent, copy, ignore=shutil.ignore_patterns("__pycache__"))
            src_copy = copy / "SKILL.md"
            src_copy.write_text(src_copy.read_text(encoding="utf-8-sig") + "\n<!-- changed after compiling -->\n", encoding="utf-8")
            for argv in (["--export-schema"], ["--step", str(first_id)]):
                proc = run(copy / script.name, argv, cwd, args.timeout)
                ok = proc is not None and proc.returncode == STALE_EXIT and not proc.stdout.strip()
                c.check(f"a stale script refuses {' '.join(argv)} with exit {STALE_EXIT} and empty stdout", ok,
                        "" if ok else said(proc))

    after = snapshot(script.parent)
    changed = sorted(k for k in before.keys() | after.keys() if before.get(k) != after.get(k))
    c.check("the skill directory is unchanged", not changed, ", ".join(changed[:5]))

    print(f"\n{len(c.failures)} failure(s)" + (": " + ", ".join(c.failures) if c.failures else ""))
    return 1 if c.failures else 0


if __name__ == "__main__":
    sys.exit(main())
