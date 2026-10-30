"""Print what changed in an English Markdown file since its TW twin was last committed, read from git diff.

The baseline is the commit that last changed the TW twin, with the source file as that commit holds
it: the version of the source the twin was last translated from. A source without a frontmatter is
compared line for line - each git diff hunk names the source lines to translate and the twin lines,
at the same numbers in the baseline, that they replace. A source with a frontmatter is compared
heading by heading - a section a hunk touches, or whose extent a hunk changes, is translated whole,
and the twin keeps every other section as it is.

The verdict is UNCHANGED (nothing to translate), INCREMENTAL (translate only the change set) or FULL
(no baseline the twin can be updated from, with the reason). With --verify, run once the twin has
been updated, it checks instead that every line or section outside the change set is still byte for
byte what the baseline twin holds, and exits 1 when one is not.

It needs git on the PATH, and it writes nothing.
"""

import argparse
import io
import os
import re
import subprocess
import sys

from check_parity import TW_SUFFIX, line_kind
from scan_md import HEADING_RE, fence_spans, split_frontmatter

HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


class NoBaseline(Exception):
    """Why the twin cannot be updated in place, so that the run translates the whole file."""


def git(cwd, *args):
    """The stdout bytes of one git command run in `cwd`, or None when git reports a failure."""
    try:
        done = subprocess.run(["git", "-C", cwd, *args], capture_output=True)
    except FileNotFoundError:
        raise NoBaseline("git was not found on the PATH") from None
    return done.stdout if done.returncode == 0 else None


def text_of(raw):
    return raw.decode("utf-8-sig", errors="replace")


def locate(path):
    """(top of the repository, the file's path relative to it, with forward slashes)."""
    folder = os.path.dirname(os.path.abspath(path))
    top, prefix = git(folder, "rev-parse", "--show-toplevel"), git(folder, "rev-parse", "--show-prefix")
    if top is None or prefix is None:
        raise NoBaseline(f"{folder} is not in a git repository")
    return text_of(top).strip(), text_of(prefix).strip() + os.path.basename(path)


def baseline(top, twin_rel):
    """(commit, date, subject) of the commit that last changed the twin."""
    raw = git(top, "log", "-1", "--format=%H%x09%ad%x09%s", "--date=short", "--", twin_rel)
    line = text_of(raw).strip() if raw else ""
    if not line:
        raise NoBaseline("the TW twin has never been committed")
    sha, date, subject = (line.split("\t", 2) + ["", ""])[:3]
    return sha, date, subject


def show(top, sha, rel):
    """A file's text as commit `sha` holds it, or None when the commit has no such file."""
    raw = git(top, "show", f"{sha}:{rel}")
    return None if raw is None else text_of(raw)


def hunks(top, sha, src_rel):
    """(old start, old length, new start, new length) of each hunk of `git diff -U0` from `sha` to the
    working tree. An old length of 0 inserts after old line `old start`; a new length of 0 deletes."""
    raw = git(top, "diff", "-U0", "--no-color", "--no-ext-diff", "--ignore-cr-at-eol", sha, "--", src_rel)
    if raw is None:
        raise NoBaseline("git diff failed on the source file")
    out = []
    for line in text_of(raw).splitlines():
        m = HUNK_RE.match(line)
        if m:
            a, b, c, d = m.groups()
            out.append((int(a), 1 if b is None else int(b), int(c), 1 if d is None else int(d)))
    return out


def dirty(top, rel):
    raw = git(top, "status", "--porcelain", "--", rel)
    return bool(raw and raw.strip())


def frontmatter_end(text):
    """The line number of a frontmatter's closing `---`, or 0 when the file has none."""
    fm, _body, offset = split_frontmatter(text)
    return offset if fm is not None else 0


def kinds(lines):
    _marks, inside = fence_spans(lines)
    return [line_kind(line, i in inside) for i, line in enumerate(lines, 1)]


def sections(lines, fm_end):
    """[(heading, first line, last line)] below the frontmatter, the preamble first - even when empty."""
    _marks, inside = fence_spans(lines)
    starts = [i for i, line in enumerate(lines, 1) if i > fm_end and i not in inside and HEADING_RE.match(line)]
    out = [("(preamble)", fm_end + 1, starts[0] - 1 if starts else len(lines))]
    for k, s in enumerate(starts):
        out.append((lines[s - 1], s, starts[k + 1] - 1 if k + 1 < len(starts) else len(lines)))
    return out


def body(lines, sec):
    return lines[sec[1] - 1 : sec[2]]


def same_headings(src_secs, twin_secs):
    """True when the twin's headings are the source's, in order - an older twin's title may still carry the suffix."""
    a, b = [h for h, _, _ in src_secs[1:]], [h for h, _, _ in twin_secs[1:]]
    return len(a) == len(b) and all(x == y or (k == 0 and y == x + TW_SUFFIX) for k, (x, y) in enumerate(zip(a, b)))


def mapper(hs):
    """Map a baseline line number to its number in the working tree, or None for a line a hunk changed."""
    def new_of(i):
        shift = 0
        for a, b, _c, d in hs:
            if b and a <= i < a + b:
                return None
            if (b and a + b - 1 < i) or (not b and a < i):
                shift += d - b
        return i + shift
    return new_of


def matched(old_lines, old_secs, new_lines, new_secs, hs):
    """Pairs (old index, new index) of the sections no hunk touches and whose extent no hunk changes,
    in order. The preamble is matched by its text, since it may be empty."""
    new_of = mapper(hs)
    at = {(s, e): k for k, (_, s, e) in enumerate(new_secs)}
    pairs = [(0, 0)] if body(old_lines, old_secs[0]) == body(new_lines, new_secs[0]) else []
    for k, (_h, s, e) in enumerate(old_secs[1:], 1):
        if any(b and a <= e and s <= a + b - 1 for a, b, _c, _d in hs):
            continue
        if any(not b and s <= a < e for a, b, _c, _d in hs):
            continue
        j = at.get((new_of(s), new_of(e)))
        if j is not None and body(old_lines, old_secs[k]) == body(new_lines, new_secs[j]):
            pairs.append((k, j))
    if any(p2[0] <= p1[0] or p2[1] <= p1[1] for p1, p2 in zip(pairs, pairs[1:])):
        raise NoBaseline("the sections that git diff leaves unchanged do not line up in order")
    return pairs


def groups(n_old, n_new, pairs):
    """[(old indices, new indices)] of the unmatched sections between two matched pairs, in order."""
    out, po, pn = [], -1, -1
    for ko, kn in pairs + [(n_old, n_new)]:
        olds, news = list(range(po + 1, ko)), list(range(pn + 1, kn))
        if olds or news:
            out.append((olds, news, po))
        po, pn = ko, kn
    return out


def span(secs, ks):
    """'L<first>-<last>' over the sections `ks`, or '' when they hold no line."""
    lines = [n for k in ks for n in range(secs[k][1], secs[k][2] + 1)]
    return f"L{lines[0]}-{lines[-1]}" if lines else ""


def heads(secs, ks):
    return "; ".join(secs[k][0] for k in ks)


def load(path):
    return io.open(path, encoding="utf-8-sig").read()


class Run:
    """Everything one comparison reads: the baseline, both versions of the source, the twin, the hunks."""

    def __init__(self, en, tw, allow_dirty):
        if not os.path.exists(tw):
            raise NoBaseline("there is no TW twin yet")
        top, self.src_rel = locate(en)
        _top, self.twin_rel = locate(tw)
        self.sha, self.date, self.subject = baseline(top, self.twin_rel)
        base_src = show(top, self.sha, self.src_rel)
        base_twin = show(top, self.sha, self.twin_rel)
        if base_src is None:
            raise NoBaseline(f"{self.src_rel} is not in {self.sha[:7]}, the commit that last changed the TW twin")
        if base_twin is None:
            raise NoBaseline(f"{self.sha[:7]}, the commit that last changed the TW twin, deleted it")
        self.base_src, self.new_src, self.twin = base_src, load(en), load(tw)
        self.base_fm, self.new_fm = frontmatter_end(base_src), frontmatter_end(self.new_src)
        self.twin_fm, self.base_twin_fm = frontmatter_end(self.twin), frontmatter_end(base_twin)
        if bool(self.base_fm) != bool(self.new_fm):
            raise NoBaseline("the source gained or lost its frontmatter since the baseline")
        self.line_for_line = not self.new_fm
        self.base_src_l, self.new_src_l = base_src.splitlines(), self.new_src.splitlines()
        self.base_twin_l, self.twin_l = base_twin.splitlines(), self.twin.splitlines()
        if self.line_for_line:
            if kinds(self.base_src_l) != kinds(self.base_twin_l):
                raise NoBaseline(f"at {self.sha[:7]} the TW twin does not line up with the source line for line")
        else:
            self.base_secs = sections(self.base_src_l, self.base_fm)
            self.base_twin_secs = sections(self.base_twin_l, self.base_twin_fm)
            if not self.base_twin_fm or not same_headings(self.base_secs, self.base_twin_secs):
                raise NoBaseline(f"at {self.sha[:7]} the TW twin's headings are not the source's")
            self.new_secs = sections(self.new_src_l, self.new_fm)
        self.hs = hunks(top, self.sha, self.src_rel)
        self.twin_dirty = dirty(top, self.twin_rel)
        if self.hs and self.twin_dirty and not allow_dirty:
            raise NoBaseline("the TW twin has uncommitted changes of its own - commit them to keep them, "
                             "and the next run translates only what changed")

    def fm_changed(self):
        return self.base_src_l[: self.base_fm] != self.new_src_l[: self.new_fm]

    def fm_keys_changed(self):
        """The frontmatter keys whose values differ between the baseline and the working tree."""
        old, _, _ = split_frontmatter(self.base_src)
        new, _, _ = split_frontmatter(self.new_src)
        old, new = old if isinstance(old, dict) else {}, new if isinstance(new, dict) else {}
        return sorted(k for k in set(old) | set(new) if old.get(k) != new.get(k))


def plan(run):
    """Print the change set and return the verdict."""
    print("\n-- change set --")
    if not run.hs:
        print("  (none: the source is what the baseline holds)")
        if run.twin_dirty:
            print("  the TW twin has uncommitted changes of its own; this run leaves them alone")
        return "UNCHANGED"
    if run.line_for_line:
        total = 0
        for n, (a, b, c, d) in enumerate(run.hs, 1):
            twin = f"replaces twin L{a}-{a + b - 1}" if b else f"inserts after twin L{a}"
            src = f"translate source L{c}-{c + d - 1}" if d else "translate nothing"
            print(f"  hunk {n}: {src}; {twin}" + ("" if d else f" (deletes {b} line(s))"))
            for i in range(c, c + d):
                print(f"    + L{i}: {run.new_src_l[i - 1]}")
            for i in range(a, a + b):
                print(f"    - L{i}: {run.twin_l[i - 1]}")
            total += d
        print(f"\nlines to translate: {total} of {len(run.new_src_l)}")
        return "INCREMENTAL"
    if run.fm_changed():
        keys = run.fm_keys_changed()
        what = ", ".join(keys) if keys else "layout only"
        print(f"  frontmatter: {what} - a changed description is translated again; every other key is copied")
    pairs = matched(run.base_src_l, run.base_secs, run.new_src_l, run.new_secs, run.hs)
    gs = groups(len(run.base_secs), len(run.new_secs), pairs)
    twin_secs = sections(run.twin_l, run.twin_fm)
    for n, (olds, news, before) in enumerate(gs, 1):
        src = f"translate source {span(run.new_secs, news)} [{heads(run.new_secs, news)}]" if news else "translate nothing"
        if olds:
            twin = f"replaces twin {span(twin_secs, olds) or 'its empty preamble'} [{heads(twin_secs, olds)}]"
        else:
            twin = f"inserts after twin L{twin_secs[before][2]}"
        print(f"  group {n}: {src}; {twin}")
    translated = sum(1 for _, news, _ in gs for k in news if k)
    preamble = any(0 in news for _, news, _ in gs)
    print(f"\nsections to translate: {translated} of {len(run.new_secs) - 1}" + (", and the preamble" if preamble else ""))
    return "INCREMENTAL"


def verify(run):
    """Check that the twin outside the change set is what the baseline twin holds; return the failure count."""
    failures = 0

    def check(name, ok, detail=""):
        nonlocal failures
        print(f"[{'PASS' if ok else 'FAIL'}] {name}{(' - ' + detail) if detail else ''}")
        failures += not ok

    if run.line_for_line:
        check("the twin has the source's line count", len(run.twin_l) == len(run.new_src_l),
              f"{len(run.twin_l)} vs {len(run.new_src_l)}")
        new_of = mapper(run.hs)
        moved = []
        for i, line in enumerate(run.base_twin_l, 1):
            j = new_of(i)
            if j is not None and (j > len(run.twin_l) or run.twin_l[j - 1] != line):
                moved.append((i, j))
        kept = sum(1 for i in range(1, len(run.base_twin_l) + 1) if new_of(i) is not None)
        check("every line outside the change set kept byte for byte", not moved,
              f"{kept - len(moved)} of {kept}" if moved else f"{kept} lines")
        for i, j in moved[:12]:
            print(f"       baseline L{i} -> twin L{j}")
        return failures
    twin_secs = sections(run.twin_l, run.twin_fm)
    aligned = same_headings(run.new_secs, twin_secs)
    check("the twin has the source's headings, in order", aligned)
    if not aligned:
        return failures
    if not run.fm_changed():
        check("frontmatter kept", run.base_twin_l[: run.base_twin_fm] == run.twin_l[: run.twin_fm])
    pairs = matched(run.base_src_l, run.base_secs, run.new_src_l, run.new_secs, run.hs)
    changed = [run.base_twin_secs[ko][0] for ko, kn in pairs
               if body(run.base_twin_l, run.base_twin_secs[ko]) != body(run.twin_l, twin_secs[kn])]
    check("every section outside the change set kept byte for byte", not changed,
          f"{len(pairs) - len(changed)} of {len(pairs)}" if changed else f"{len(pairs)} sections")
    for head in changed[:12]:
        print(f"       {head}")
    return failures


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--en", required=True, help="path to the English source file")
    ap.add_argument("--tw", required=True, help="path to its -tw.md twin")
    ap.add_argument("--verify", action="store_true",
                    help="after the twin was updated: check that nothing outside the change set changed")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    print(f"source: {args.en}")
    print(f"twin: {args.tw}")
    try:
        run = Run(args.en, args.tw, allow_dirty=args.verify)
    except NoBaseline as why:
        if args.verify:
            print(f"[SKIP] nothing to verify - {why}")
            return 0
        print(f"baseline: none - {why}")
        print("\nverdict: FULL")
        return 0
    shape = "line for line (no frontmatter)" if run.line_for_line else "heading by heading (frontmatter)"
    print(f"shape: {shape}")
    print(f"baseline: {run.sha[:7]} {run.date} \"{run.subject}\" - the commit that last changed the TW twin")
    if args.verify:
        failures = verify(run)
        print(f"\n{failures} failure(s)")
        return 1 if failures else 0
    try:
        verdict = plan(run)
    except NoBaseline as why:
        print(f"  {why}")
        verdict = "FULL"
    print(f"\nverdict: {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
