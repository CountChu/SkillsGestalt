"""Run one app's unit tests and report what ran, what failed, and what nothing covers.

The `test` command's checked half. Discovery and execution belong in a program because a test that
is silently skipped reads exactly like a test that passed - and the one thing a judgement call must
not decide is which tests it ran.

It runs the app's OWN tests with the app's own runners - `unittest` for the Python kernel and
`node --test` for the server - both standard library, because the app must be testable on a machine
with nothing installed.

Zero is zero, never green: a target with no tests exits non-zero.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

UNITTEST_LINE = re.compile(r"^(?P<name>\S+ \([^)]+\)(?: \S+)?) \.\.\. (?P<outcome>ok|FAIL|ERROR|skipped.*)$")
# A case carrying a docstring is printed over TWO lines - the name, then the docstring's first line
# followed by the outcome. Matching only the one-line form drops every documented test from the
# count while the run itself stays green, which reads as tests that went missing.
UNITTEST_NAME_ONLY = re.compile(r"^(?P<name>\S+ \([^)]+\)(?: \S+)?)$")
UNITTEST_OUTCOME_ONLY = re.compile(r"^(?P<detail>.*?) \.\.\. (?P<outcome>ok|FAIL|ERROR|skipped.*)$")
TAP_LINE = re.compile(r"^\s*(?P<not>not )?ok (?P<n>\d+) - (?P<name>.+?)\s*$")
TAP_SUMMARY = re.compile(r"^# (?P<key>pass|fail|skipped|todo|tests) (?P<n>\d+)$")
# The naming the two runners discover, and nothing else. A test file matching neither is reported
# rather than ignored: a file nobody runs is the failure this script exists to make visible.
PY_TEST = re.compile(r"^test_.+\.py$")
JS_TEST = re.compile(r"^.+\.test\.(js|mjs|cjs)$")


def run(cmd: list[str], cwd: str) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=900)
    except FileNotFoundError as exc:
        return 127, f"{exc}"
    except subprocess.TimeoutExpired:
        return 124, "timed out after 900s"
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def find_tests(tests_dir: str) -> tuple[list[str], list[str], list[str]]:
    py, js, other = [], [], []
    for base, _dirs, files in os.walk(tests_dir):
        if "__pycache__" in base:
            continue
        for f in sorted(files):
            rel = os.path.relpath(os.path.join(base, f), tests_dir)
            if PY_TEST.match(f):
                py.append(rel)
            elif JS_TEST.match(f):
                js.append(rel)
            elif f.endswith((".py", ".js", ".mjs", ".cjs")) and f != "__init__.py":
                other.append(rel)
    return py, js, other


def source_files(target: str) -> list[str]:
    """The app's own source: the root entry points and everything under scripts\\ and public\\."""
    out = []
    for f in sorted(os.listdir(target)):
        if f.endswith((".js", ".mjs", ".cjs")) and os.path.isfile(os.path.join(target, f)):
            out.append(f)
    for sub in ("scripts", "public"):
        d = os.path.join(target, sub)
        if not os.path.isdir(d):
            continue
        for base, _dirs, files in os.walk(d):
            if "__pycache__" in base:
                continue
            for f in sorted(files):
                if f.endswith((".py", ".js", ".mjs", ".cjs")):
                    out.append(os.path.relpath(os.path.join(base, f), target))
    return out


def unmentioned(target: str, tests_dir: str, sources: list[str]) -> list[str]:
    """Source files no test so much as names.

    A file nothing mentions cannot be covered by anything, which is a fact about the tests and
    checkable by reading them. Whether a file that IS mentioned is actually exercised is a
    judgement, and this deliberately does not claim to answer it.
    """
    blob = ""
    for base, _dirs, files in os.walk(tests_dir):
        for f in files:
            if f.endswith((".py", ".js", ".mjs", ".cjs")):
                try:
                    with open(os.path.join(base, f), encoding="utf-8", errors="replace") as fh:
                        blob += fh.read()
                except OSError:
                    pass
    stems: dict[str, int] = {}
    for src in sources:
        stems[os.path.basename(src)] = stems.get(os.path.basename(src), 0) + 1
    out = []
    for src in sources:
        name = os.path.basename(src)
        # Two source files sharing a basename cannot be told apart by it, so one of them being
        # mentioned would otherwise credit both. Those need the path itself.
        needles = [src, src.replace(os.sep, "/")] if stems[name] > 1 else [name, os.path.splitext(name)[0]]
        if not any(n in blob for n in needles):
            out.append(src)
    return out


def parse_unittest(text: str) -> list[dict]:
    def case(name: str, outcome: str, detail: str = "") -> dict:
        return {
            "runner": "unittest",
            "name": name,
            "result": "pass" if outcome == "ok" else ("skip" if outcome.startswith("skipped") else "fail"),
            "detail": detail if outcome == "ok" else (outcome + (f" - {detail}" if detail else "")),
        }

    cases = []
    pending = None          # a name whose outcome is on the next line, i.e. a documented test
    for raw in text.splitlines():
        line = raw.strip()
        m = UNITTEST_LINE.match(line)
        if m:
            pending = None
            cases.append(case(m.group("name"), m.group("outcome")))
            continue
        m = UNITTEST_NAME_ONLY.match(line)
        if m:
            pending = m.group("name")
            continue
        m = UNITTEST_OUTCOME_ONLY.match(line) if pending else None
        if m:
            cases.append(case(pending, m.group("outcome"), m.group("detail")))
        pending = None
    return cases


def parse_tap(text: str) -> list[dict]:
    cases = []
    for line in text.splitlines():
        m = TAP_LINE.match(line)
        if m and not m.group("name").startswith("Subtest:"):
            cases.append({
                "runner": "node:test",
                "name": m.group("name"),
                "result": "fail" if m.group("not") else "pass",
                "detail": "",
            })
    return cases


def main() -> None:
    ap = argparse.ArgumentParser(description="Run one imp-app target's unit tests.")
    ap.add_argument("--app-dir", required=True, help="the app directory, e.g. artifacts\\InvCov")
    ap.add_argument("--out", required=True, help="the run's Checkpoint Dir; unit-tests.json is written there")
    ap.add_argument("--python", default=sys.executable, help="the Python the kernel's tests run under")
    ap.add_argument("--node", default="node", help="the Node the server's tests run under")
    args = ap.parse_args()

    target = os.path.abspath(args.app_dir)
    if not os.path.isdir(target):
        sys.exit(f"no such app dir: {target}")
    tests_dir = os.path.join(target, "tests")

    result = {
        "appDir": args.app_dir,
        "testsDir": os.path.relpath(tests_dir, target) if os.path.isdir(tests_dir) else None,
        "runners": [],
        "cases": [],
        "counts": {"pass": 0, "fail": 0, "skip": 0, "total": 0},
        "sourceFilesNoTestMentions": [],
        "sourceFiles": [],
    }

    if not os.path.isdir(tests_dir):
        result["error"] = "the app dir has no tests\\ directory; a change is not finished until the test that would have caught its absence exists"
        write_out(args.out, result)
        sys.exit(1)

    py_tests, js_tests, undiscovered = find_tests(tests_dir)
    result["pythonTestFiles"], result["nodeTestFiles"] = py_tests, js_tests
    # Named so neither runner will pick them up: test_*.py and *.test.js are what is discovered.
    result["undiscoveredTestFiles"] = undiscovered

    if py_tests:
        # `-t .` lets a test import `tests.helpers`, which needs tests\ to be a package; without an
        # __init__.py the discovery itself refuses, so the top level is the tests directory instead.
        top = "." if os.path.isfile(os.path.join(tests_dir, "__init__.py")) else "tests"
        code, text = run([args.python, "-m", "unittest", "discover", "-s", "tests", "-t", top, "-v"], target)
        cases = parse_unittest(text)
        result["runners"].append({"runner": "unittest", "exit": code, "cases": len(cases), "output": text[-4000:]})
        result["cases"] += cases
    if js_tests:
        code, text = run([args.node, "--test", "tests"], target)
        cases = parse_tap(text)
        result["runners"].append({"runner": "node:test", "exit": code, "cases": len(cases), "output": text[-4000:]})
        result["cases"] += cases

    for c in result["cases"]:
        result["counts"][c["result"]] += 1
    result["counts"]["total"] = len(result["cases"])

    result["sourceFiles"] = source_files(target)
    result["sourceFilesNoTestMentions"] = unmentioned(target, tests_dir, result["sourceFiles"])

    write_out(args.out, result)

    if result["counts"]["total"] == 0:
        sys.exit("no unit test was found or run; zero tests is zero, never green")
    if result["counts"]["fail"]:
        sys.exit(f"{result['counts']['fail']} unit test(s) failed")


def write_out(out_dir: str, result: dict) -> None:
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "unit-tests.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, ensure_ascii=False)
    result_for_print = dict(result)
    result_for_print["runners"] = [{k: v for k, v in r.items() if k != "output"} for r in result.get("runners", [])]
    result_for_print["savedTo"] = path
    print(json.dumps(result_for_print, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
