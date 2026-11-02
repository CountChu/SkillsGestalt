r"""Merge one check-skill run's result for one skill into the Skills Dashboard.

The dashboard is the unstamped dashboard\skills.md under the wiki root: one section per skill group,
holding one row per checked skill and one cell per check. A run replaces the cells of the checks it
applied and leaves every other cell - and every other skill's row - as it was, so a cell it did not
touch keeps the date of the run that last applied it. Dates are yyyy-mm-dd: --run takes the run's
{yymmdd-hh} stamp and the dashboard records only its date, so every run on one day shares that date.
--mark-modified only flags the skill as edited since its cells were written; a later run that
re-applies every one of that skill's checks in full clears the flag, and a partial one does not.

--result takes one check per flag:
  <check>:<issues>:<recommendations>              e.g. 1:3:1
  <check>:<issues>:<recommendations>:<criteria>   a check narrowed to some criteria, e.g. 1:0:1:1.3+1.5
  <check>:na                                      the check does not apply, e.g. 4:na

Examples:
  python update_dashboard.py --dashboard "<wikiDir>\dashboard\skills.md" --run 260927-17
      --skill imp-app --group common --path "<skillGroups.common>\skills\imp-app\SKILL.md"
      --result 1:3:1 --result 2:0:1 --result 3:1:4 --result 4:0:2
  python update_dashboard.py --dashboard "<wikiDir>\dashboard\skills.md" --skill imp-app --mark-modified
"""

import argparse
import io
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

CHECKS = {
    1: "Template alignment",
    2: "Config conformance",
    3: "Description accuracy",
    4: "Terminology usage",
    5: "Cross-platform compatibility",
    6: "Dataflow",
}
COLUMNS = ["Skill", "Checked", *CHECKS.values(), "Verdict", "Needs check"]

CLEAN, RECS, ISSUES, NA = "\u2705", "\u26a0\ufe0f", "\u274c", "\u2796"
NEVER = "\u2014"
MARK = "\u2713"
DOT = "\u00b7"

TITLE = "# Skills"
NO_GROUP = "(no group)"
LEGEND = (
    "One section per skill group, one row per skill `check-skill` has checked in it, and one cell per "
    f"check holding that check's newest result as `<verdict> <issues> {DOT} <recommendations>`. A cell "
    "older than its row's **Checked** "
    "date carries its own date, and a check narrowed to some criteria names them. "
    f"{CLEAN} no finding {DOT} {RECS} recommendations only {DOT} {ISSUES} issues {DOT} "
    f"{NA} not applicable {DOT} {NEVER} never applied. **Needs check** {MARK} means the skill was "
    "edited after its cells were written, so they describe it as it was then; a run that re-applies "
    "every check in full clears it."
)
NOTE = (
    "Written by `update_dashboard.py` on every `/check-skill` run, and merged into rather than "
    "rewritten - change the skill, not this file."
)

STAMP = re.compile(r"^\d{6}-\d{2}$")
CRITERIA = re.compile(r"^\d+\.\d+(?:\+\d+\.\d+)*$")
COUNTS_CELL = re.compile(
    rf"^(?P<v>{CLEAN}|{RECS}|{ISSUES}) (?P<i>\d+) {DOT} (?P<r>\d+)(?: \((?P<ann>[^)]*)\))?$"
)
NA_CELL = re.compile(rf"^{NA} n/a(?: \((?P<ann>[^)]*)\))?$")
LINK = re.compile(r"^\[(?P<name>[^\]]+)\]\((?P<url>[^)]*)\)$")
CREATED = re.compile(r"^- \*\*Created\*\*: (.+)$", re.M)


def to_date(value):
    """The yyyy-mm-dd date the dashboard shows, from a date or from a yymmdd-hh run stamp."""
    for fmt in ("%Y-%m-%d", "%y%m%d-%H"):
        try:
            return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    raise ValueError(f"unreadable date {value!r}, neither yyyy-mm-dd nor a yymmdd-hh run stamp")


def verdict(issues, recs):
    return ISSUES if issues else RECS if recs else CLEAN


class Cell:
    """One check's newest result for one skill; `date` is the date of the run that applied it."""

    def __init__(self, kind, issues=0, recs=0, criteria=None, date=None):
        self.kind, self.issues, self.recs, self.criteria, self.date = kind, issues, recs, criteria, date

    def render(self, row_date):
        if self.kind == "never":
            return NEVER
        notes = [f"{self.criteria} only"] if self.criteria else []
        # A cell as new as its row needs no date; an older one must never pass for current.
        if self.date and self.date != row_date:
            notes.append(self.date)
        tail = f" ({', '.join(notes)})" if notes else ""
        if self.kind == "na":
            return f"{NA} n/a{tail}"
        return f"{verdict(self.issues, self.recs)} {self.issues} {DOT} {self.recs}{tail}"


class Row:
    def __init__(self, name, url, group, checked, cells, needs):
        self.name, self.url, self.group, self.checked, self.cells, self.needs = (
            name, url, group, checked, cells, needs,
        )

    def verdict(self):
        counted = [c for c in self.cells.values() if c.kind == "counts"]
        if not counted:
            return NA if any(c.kind == "na" for c in self.cells.values()) else NEVER
        issues = sum(c.issues for c in counted)
        recs = sum(c.recs for c in counted)
        return f"{verdict(issues, recs)} {issues} {DOT} {recs}"

    def view(self):
        """The row's group and every column but Skill as it renders, so a change reads as old -> new."""
        out = {"Group": self.group or "", "Checked": self.checked or ""}
        out.update({CHECKS[n]: self.cells[n].render(self.checked) for n in CHECKS})
        out["Verdict"] = self.verdict()
        out["Needs check"] = MARK if self.needs else ""
        return out

    def render(self):
        skill = f"[{self.name}]({self.url})" if self.url else self.name
        cells = self.view()
        return "| " + " | ".join([skill, *(cells[c] for c in COLUMNS[1:])]) + " |"


def split_row(line):
    s = line.strip()
    s = s[1:] if s.startswith("|") else s
    s = s[:-1] if s.endswith("|") else s
    return [c.strip() for c in s.split("|")]


def parse_cell(text, row_date):
    if not text or text == NEVER:
        return Cell("never")
    m = COUNTS_CELL.match(text)
    na = None if m else NA_CELL.match(text)
    if not (m or na):
        raise ValueError(f"unreadable cell {text!r}")
    criteria, date = None, row_date
    for note in filter(None, (s.strip() for s in ((m or na).group("ann") or "").split(","))):
        if note.endswith(" only") and CRITERIA.match(note[: -len(" only")]):
            criteria = note[: -len(" only")]
            continue
        try:
            date = to_date(note)
        except ValueError:
            raise ValueError(f"unreadable note {note!r} in cell {text!r}") from None
    if na:
        return Cell("na", date=date)
    return Cell("counts", int(m.group("i")), int(m.group("r")), criteria, date)


def parse_row(path, rec, heading):
    link = LINK.match(rec.get("Skill", ""))
    name, url = (link.group("name"), link.group("url")) if link else (rec.get("Skill", ""), None)
    # An older dashboard kept one table with a Group column; this one files each group under a heading.
    group = rec.get("Group") or (heading if heading and heading != NO_GROUP else None)
    try:
        # An older dashboard wrote the run stamp here; reading it as its date migrates the row.
        checked = to_date(rec["Checked"]) if rec.get("Checked") else None
        cells = {n: parse_cell(rec.get(title, ""), checked) for n, title in CHECKS.items()}
    except ValueError as exc:
        sys.exit(f"{path}: row {name!r} has an {exc} - fix the row or remove it, then re-run")
    return Row(name, url, group, checked, cells, rec.get("Needs check") == MARK)


def load(path):
    """The dashboard's Created value, its rows by skill, and whatever follows the last table."""
    if not path.exists():
        return None, {}, []
    text = io.open(path, encoding="utf-8").read()
    lines = text.splitlines()
    rows, heading, end, k = {}, None, None, 0
    while k < len(lines):
        line = lines[k].strip()
        if line.startswith("## "):
            heading = line[3:].strip()
        elif line.startswith("| Skill |"):
            # The latest heading above a table names the group of every row in it.
            header = split_row(line)
            k += 2
            while k < len(lines) and lines[k].strip().startswith("|"):
                row = parse_row(path, dict(zip(header, split_row(lines[k]))), heading)
                rows[row.name] = row
                k += 1
            end = k
            continue
        k += 1
    if end is None:
        sys.exit(f"{path} exists but carries no dashboard table - refusing to overwrite it")
    suffix = lines[end:]
    while suffix and not suffix[0].strip():
        suffix.pop(0)
    created = CREATED.search(text)
    return (created.group(1).strip() if created else None), rows, suffix


def dump(path, created, updated, rows, suffix):
    out = [
        TITLE, "",
        "- **Skill**: check-skill",
        f"- **Created**: {created}",
        f"- **Updated**: {updated}",
        "", LEGEND, "", NOTE,
    ]
    for group in sorted({r.group or NO_GROUP for r in rows.values()}, key=str.lower):
        members = [r for r in rows.values() if (r.group or NO_GROUP) == group]
        out += [
            "", f"## {group}", "",
            "| " + " | ".join(COLUMNS) + " |",
            "| " + " | ".join("---" for _ in COLUMNS) + " |",
        ]
        out += [r.render() for r in sorted(members, key=lambda r: r.name.lower())]
    if suffix:
        out += ["", *suffix]
    path.parent.mkdir(parents=True, exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out) + "\n")


def parse_results(specs, ap):
    out = {}
    shape = "<check>:<issues>:<recommendations>[:<criteria>] or <check>:na"
    for spec in specs:
        parts = spec.split(":")
        if not parts[0].isdigit() or int(parts[0]) not in CHECKS:
            ap.error(f"--result {spec!r}: the check must be one of {', '.join(map(str, CHECKS))}")
        n = int(parts[0])
        if n in out:
            ap.error(f"--result names check {n} twice")
        if len(parts) == 2 and parts[1] == "na":
            out[n] = Cell("na")
        elif len(parts) in (3, 4) and parts[1].isdigit() and parts[2].isdigit():
            criteria = parts[3] if len(parts) == 4 else None
            if criteria is not None and (
                not CRITERIA.match(criteria) or any(c.split(".")[0] != str(n) for c in criteria.split("+"))
            ):
                ap.error(f"--result {spec!r}: criteria must be check {n}'s own, e.g. {n}.3+{n}.5")
            out[n] = Cell("counts", int(parts[1]), int(parts[2]), criteria)
        else:
            ap.error(f"--result {spec!r}: expected {shape}")
    return out


def vscode_url(skill_md):
    target = Path(skill_md)
    if not target.is_file():
        sys.exit(f"--path is not a file: {skill_md}")
    return "vscode://file/" + quote(str(target.resolve()).replace("\\", "/"), safe="/:")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dashboard", required=True, help="the Skills Dashboard, dashboard/skills.md under the wiki root")
    ap.add_argument("--skill", required=True, help="the checked skill's name")
    ap.add_argument("--group", help="its skillGroups group, which names the section its row is filed under")
    ap.add_argument("--path", help="its SKILL.md, which the row links to")
    ap.add_argument("--run", help="this run's {yymmdd-hh} stamp; the dashboard records its date")
    ap.add_argument("--result", action="append", default=[], help="one check's result; repeat once per check that ran")
    ap.add_argument(
        "--mark-modified", action="store_true", help="flag the skill as edited since its last check, and change nothing else"
    )
    args = ap.parse_args()

    path = Path(args.dashboard)
    created, rows, suffix = load(path)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    row = rows.get(args.skill)

    if args.mark_modified:
        if args.run or args.result:
            ap.error("--mark-modified takes no --run or --result")
        if row is None:
            sys.exit(f"{args.skill} has no row on {path} - a skill is checked before it can be marked modified")
        before = row.view()
        row.needs = True
        action = "marked modified"
    else:
        if not (args.group and args.run and args.result):
            ap.error("a result run needs --group, --run and at least one --result")
        try:
            run_date = to_date(args.run) if STAMP.match(args.run) else None
        except ValueError:
            run_date = None
        if run_date is None:
            ap.error("--run must be a {yymmdd-hh} stamp, e.g. 260927-17")
        results = parse_results(args.result, ap)
        url = vscode_url(args.path) if args.path else None
        if row is None:
            row = Row(args.skill, None, None, None, {n: Cell("never") for n in CHECKS}, False)
            rows[args.skill] = row
            action = "row added"
        else:
            action = "row updated"
        before = row.view()
        # The flag clears only when this run re-applied, in full, every check the row holds - a
        # partial run leaves older cells still describing the skill as it was before the edit.
        held = [n for n, c in row.cells.items() if c.kind != "never"]
        if all(n in results and results[n].criteria is None for n in held):
            row.needs = False
        for n, cell in results.items():
            cell.date = run_date
            row.cells[n] = cell
        row.group = args.group
        row.url = url or row.url
        row.checked = max(c.date for c in row.cells.values() if c.kind != "never")

    after = row.view()
    existed = path.exists()
    dump(path, created or now, now, rows, suffix)

    print(f"dashboard: {path} ({'updated' if existed else 'created'})")
    print(f"{args.skill}: {action}")
    changed = [(col, before[col], after[col]) for col in after if before[col] != after[col]]
    for col, old, new in changed:
        print(f"  {col}: {old or '(empty)'} -> {new or '(empty)'}")
    if not changed:
        print("  no cell changed")
    print(f"rows: {len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
