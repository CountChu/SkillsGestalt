"""Collect structural facts about a skill for the check-skill workflow.

SKILL.md gives the template, config, leftover and terminology facts; README.md gives the readme
facts - its headings against the README template's, its header quote as depends_on.py reads it,
its Step Purposes and Files Each Step Uses against the steps of SKILL.md - and the dataflow facts
of its Dataflow; every other text file in the skill directory - its scripts, its references, its
own config.yaml, its 繁體中文 twins - gives the hardcoded-path facts, since a path baked into a
script breaks exactly as one baked into SKILL.md does.

Facts only - no verdicts. Every fact carries its line number, the region or file it was
found in, whether it sits inside an inline-code span, and the whole line it came from, so
the agent can judge and quote it without reopening the file.
"""

import argparse
import importlib.util
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

STEP_HEAD = re.compile(r"^##\s+Step\s+(\d+)\s*-?\s*(.*)$")
PURPOSE = re.compile(r"^\s*-\s+\*\*Purpose\*\*")
TOP_HEAD = re.compile(r"^#\s+(.+)$")
STEP_REF = re.compile(r"\bSteps?\s+(\d+)\s*(?:-|to|and)\s*(\d+)|\bSteps?\s+(\d+)")
WIKI_PATH = re.compile(r"(?<![\w/\\{-])wiki[\\/][\w.*-]*")
# The lookbehind keeps a URL scheme out - `http://host` would otherwise read as drive `p`.
ABS_PATH = re.compile(r"(?<![\w:])[A-Za-z]:[\\/][\w.$%\\/-]+")
# 2-4 leading slashes, since a UNC written in Python source carries its own escaping.
UNC_PATH = re.compile(r"\\{2,4}[\w.$-]{2,}\\{1,2}[\w.$-]+")
GITHUB_PATH = re.compile(r"(?<![\w/])\.github[\\/][\w.\\/-]+")
CODE_SPAN = re.compile(r"``.+?``|`[^`]*`")  # double-backtick spans first, or a bare token inside one reads as outside
# A placeholder a template leaves to be filled: {UPPER_SNAKE}.
# The name PLACEHOLDER itself only talks about placeholders and is never one.
PLACEHOLDER = re.compile(r"\{(?!PLACEHOLDER\})[A-Z][A-Z0-9_]+\}")
# A placeholder in the retired form ___UPPER_SNAKE___, which Markdown shows in bold italics instead of as
# written: always a fact, shown or not, since common/scripts/placeholders.py converts it to {UPPER_SNAKE}.
OLD_PLACEHOLDER = re.compile(r"___[A-Z0-9_]+___")
MD_LINK = re.compile(r"\]\((\.github[^)]+)\)")
NAMED_SCRIPT = re.compile(r"([\w-]+\.py)")
ANY_HEAD = re.compile(r"^#{1,2}\s+(.+)$")
TERM_DEF = re.compile(r"^- \*\*(.+?)\*\*\s+[-\u2014]")
BACKTICKED = re.compile(r"`([^`]+)`")
FILE_LITERAL = re.compile(r"^[\w.-]+\.\w+$")
COMMENT_LEAD = re.compile(r"^\s*(#|//|/\*|\*|<!--|REM\b|::)")
NAME_CHARSET = re.compile(r"[a-z0-9-]+")

# README.md: its # and ## headings, the step items of its Step Purposes, the step lines of the tree in
# its Files Each Step Uses, and what in SKILL.md belongs in it instead.
README_HEAD = re.compile(r"^(#{1,2})\s+(.+?)\s*$")
SECTION_HEAD = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
STEP_ITEM = re.compile(r"^-\s+(Step\s+\d+\s+-\s+.+?)\s*$")
TREE_STEP = re.compile(r"^(Step\s+\d+\s+-\s+.+?)\s*$")
PURPOSE_INTRO = re.compile(r"opens with a \*\*Purpose\*\*")
README_LINK = re.compile(r"\]\(<?(?:\./)?README(?:-tw)?\.md")
SCRIPTED_RULE = re.compile(r"\*\*[^*]*\bscripts?\b[^*]*\*\*")
README_SECTIONS = ("Dataflow", "Steps at a Glance")

DATAFLOW = "Dataflow"
DFD_KINDS =("external input", "record", "one-run data")
# The shapes of DFD.md as mermaid draws them: (shape, kind, opening, closing). The longer
# delimiters come first, so [[ is never read as [ nor ([ as (; and a flag's > must follow its id
# directly, so the > of an arrow such as --> is never read as one.
DFD_SHAPES = (
    ("double-edged box", "step", r"\[\[", r"\]\]"),
    ("cylinder", "record", r"\[\(", r"\)\]"),
    ("rounded box", "step", r"\(\[", r"\]\)"),
    ("hexagon", "role", r"\{\{", r"\}\}"),
    ("parallelogram", "external input", r"\[/", r"/\]"),
    ("flag", "one-run data", r">", r"\]"),
    ("rectangle", None, r"\[", r"\]"),
    ("round box", None, r"\(", r"\)"),
    ("diamond", None, r"\{", r"\}"),
)
MERMAID_NODE = re.compile(
    r"(?<![\w-])(?P<id>[A-Za-z_]\w*)(?:"
    + "|".join(
        f'{o}"(?P<q{i}>[^"]*)"{c}|{o}(?P<u{i}>[^"\\[\\](){{}}]*?){c}'
        for i, (_, _, o, c) in enumerate(DFD_SHAPES)
    )
    + ")"
)
MERMAID_ARROW = re.compile(r"\s*(?P<l><)?(?P<body>-{2,}|-\.+-|={2,})(?P<r>>)?\s*(?:\|[^|]*\|\s*)?")
MERMAID_SKIP = re.compile(r"^(?:flowchart|graph|subgraph|end|direction|classDef|class|style|click)\b")
LINK_STYLE = re.compile(r"^linkStyle\s+(?P<idx>default|[\d,\s]+?)\s+(?P<style>\S.*)$")
STEP_NUMBER = re.compile(r"^Step\s+(\d+)\b")
BLUE = "#2563eb"

PATH_FACTS = (
    ("literal_wiki_path", WIKI_PATH),
    ("absolute_path", ABS_PATH),
    ("unc_path", UNC_PATH),
    ("literal_github_path", GITHUB_PATH),
)
TEXT_SUFFIXES = {".py", ".md", ".yaml", ".yml", ".json", ".js", ".css", ".html", ".txt", ".ps1", ".cmd", ".robot"}
SKIP_DIRS = {"__pycache__", ".git", ".venv", "node_modules", "temp"}
MAX_SCAN_BYTES = 512 * 1024
DIR_KINDS = {"scripts": "script", "references": "reference", "templates": "template"}


def find_config(explicit=None) -> Path:
    """The config.yaml this run reads: --config if given, else the nearest one above this script or above the cwd."""
    if explicit:
        path = Path(explicit).resolve()
        path = path / "config.yaml" if path.is_dir() else path
        if not path.is_file():
            raise SystemExit(f"--config does not name a config.yaml: {path}")
        return path

    # The script and the workspace root can sit in different roots of a multi-root workspace.
    starts = [Path(__file__).resolve().parent, Path.cwd().resolve()]
    for start in starts:
        for parent in [start, *start.parents]:
            candidate = parent / "config.yaml"
            if candidate.is_file():
                return candidate
    raise SystemExit(
        "config.yaml was found neither above "
        + " nor above ".join(str(s) for s in starts)
        + " - pass --config <path to config.yaml>"
    )


def load_config(config: Path) -> dict:
    return yaml.safe_load(config.read_text(encoding="utf-8")) or {}


def find_skill(groups: dict, name: str, workspace: Path):
    """The skill's SKILL.md under the first skillGroups root that holds it.

    A root is absolute, or relative to the workspace root - and a leading ~ means
    the home directory, so it is expanded before use. A group declared with no
    value at all (`external:`) is skipped rather than resolved.
    """
    for group, group_root in groups.items():
        if not group_root:
            continue
        base = Path(str(group_root)).expanduser()
        if not base.is_absolute():
            base = workspace / base
        path = base / "skills" / name / "SKILL.md"
        if path.is_file():
            return group, path
    return None, None


def required_headings(template: Path) -> list:
    """The template's own top-level headings, in template order - the alignment reference."""
    out, fenced = [], False
    for ln in template.read_text(encoding="utf-8").splitlines():
        if ln.startswith("```"):
            fenced = not fenced
        elif not fenced and (m := TOP_HEAD.match(ln)):
            out.append(m.group(1).strip())
    return out


def regions(lines):
    """Map each 0-based line index to 'frontmatter', 'prompt_examples' or 'body'."""
    region = ["body"] * len(lines)
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                for j in range(0, i + 1):
                    region[j] = "frontmatter"
                break
    for i, ln in enumerate(lines):
        if re.match(r"^#\s+Prompt Examples", ln):
            end = len(lines)
            for j in range(i + 1, len(lines)):
                if TOP_HEAD.match(lines[j]):
                    end = j
                    break
            for j in range(i, end):
                region[j] = "prompt_examples"
            break
    return region


def fenced(lines):
    """Map each 0-based line index to whether it sits in a ``` block - a token shown there is displayed, not left behind."""
    out, inside = [False] * len(lines), False
    for i, ln in enumerate(lines):
        if ln.lstrip().startswith("```"):
            out[i], inside = True, not inside
        else:
            out[i] = inside
    return out


def sections(lines):
    """Map each 0-based line index to the nearest preceding `#` or `##` heading."""
    out, cur = [], "(frontmatter)"
    for ln in lines:
        m = ANY_HEAD.match(ln)
        if m:
            cur = m.group(1).strip()
        out.append(cur)
    return out


def terminology(lines, secs):
    """Glossary terms, where each is used, and where a variant or raw literal is used instead."""
    glossary = {s for s in set(secs) if "TERMINOLOGY" in s.upper()}
    # A term defined under CONFIGURATION is a definition the glossary does not own.
    in_config = [
        {"term": m.group(1).replace("`", ""), "line": i + 1, "section": secs[i]}
        for i, ln in enumerate(lines)
        if "CONFIGURATION" in secs[i].upper() and (m := TERM_DEF.match(ln))
    ]
    if not glossary:
        return {"has_glossary": False, "terms_defined_in_configuration": in_config}

    terms = []
    for i, ln in enumerate(lines):
        if secs[i] not in glossary:
            continue
        m = TERM_DEF.match(ln)
        if not m:
            continue
        tail = ln.split("**", 2)[-1]
        terms.append({
            "term": m.group(1).replace("`", ""),
            "defined_at": i + 1,
            "defined_in": secs[i],
            # A filename in the definition is the raw artefact the term stands for.
            "literals": [x for x in BACKTICKED.findall(tail) if FILE_LITERAL.match(x)],
        })

    for t in terms:
        used, variants, literal_uses = [], [], []
        rx = re.compile(r"(?<![\w-])" + re.escape(t["term"]) + r"(?![\w-])", re.I)
        for i, ln in enumerate(lines):
            if secs[i] in glossary:
                continue
            for m in rx.finditer(ln):
                rec = {"line": i + 1, "section": secs[i], "text": m.group(0)}
                (used if m.group(0) == t["term"] else variants).append(rec)
            for lit in t["literals"]:
                if lit in ln:
                    literal_uses.append({"line": i + 1, "section": secs[i], "literal": lit})
        t["used"] = used
        t["variants"] = variants
        t["literal_uses"] = literal_uses

    return {
        "has_glossary": True,
        "glossary_sections": sorted(glossary),
        "terms": terms,
        "unused_terms": [t["term"] for t in terms if not t["used"] and not t["variants"]],
        "terms_defined_in_configuration": in_config,
    }


def mermaid_edges(text):
    """Every link on one diagram line whose node definitions are already reduced to ids: (from, to, arrow)."""
    ends, arrows, last = [], [], 0
    for m in MERMAID_ARROW.finditer(text):
        ends.append(text[last:m.start()])
        arrows.append(m)
        last = m.end()
    ends.append(text[last:])
    ids = [[x.strip() for x in e.split("&")] for e in ends]
    return [
        (a, b, m)
        for k, m in enumerate(arrows)
        for a in ids[k]
        for b in ids[k + 1]
        if re.fullmatch(r"\w+", a) and re.fullmatch(r"\w+", b)
    ]


def section(lines, in_fence, title, level):
    """(start, end) of the section headed `title` at `level`: from its heading up to the next heading of
    that level or above, outside fenced blocks - or None when there is no such heading."""
    start = next(
        (i for i, ln in enumerate(lines)
         if not in_fence[i] and (m := SECTION_HEAD.match(ln)) and len(m.group(1)) == level and m.group(2) == title),
        None,
    )
    if start is None:
        return None
    end = next(
        (i for i in range(start + 1, len(lines))
         if not in_fence[i] and (m := SECTION_HEAD.match(lines[i])) and len(m.group(1)) <= level),
        len(lines),
    )
    return start, end


def dataflow(lines, in_fence, steps, path):
    """The skill's own Dataflow, the `## Dataflow` of its README.md: its diagram's nodes and arrows, and
    what they say against the Workflow of SKILL.md. Every line number is a line of README.md."""
    span = section(lines, in_fence, DATAFLOW, 2) if lines else None
    if span is None:
        return {"has_dataflow": False, "file": str(path) if lines else None}
    start, end = span

    blocks, i = [], start + 1
    while i < end:
        if lines[i].strip().startswith("```mermaid"):
            j = next((k for k in range(i + 1, end) if lines[k].strip().startswith("```")), end)
            blocks.append((i, j))
            i = j + 1
        else:
            i += 1

    # The facts are read from the first diagram alone; the legend is what follows it, up to a heading or a fence.
    nodes, links, blue, legend = {}, [], set(), 0
    if blocks:
        b0, b1 = blocks[0]
        for i in range(b0 + 1, b1):
            raw = lines[i].strip()
            if m := LINK_STYLE.match(raw):
                if BLUE in m.group("style").lower():
                    idx = m.group("idx")
                    blue |= {"default"} if idx == "default" else {int(x) for x in re.findall(r"\d+", idx)}
                continue
            if not raw or raw.startswith("%%") or MERMAID_SKIP.match(raw):
                continue
            for m in MERMAID_NODE.finditer(raw):
                k = next(k for k in range(len(DFD_SHAPES)) if m.group(f"q{k}") is not None or m.group(f"u{k}") is not None)
                label = m.group(f"q{k}") if m.group(f"q{k}") is not None else m.group(f"u{k}")
                nodes.setdefault(m.group("id"), {
                    "label": label.strip(), "shape": DFD_SHAPES[k][0], "kind": DFD_SHAPES[k][1], "line": i + 1,
                })
            for a, b, arrow in mermaid_edges(MERMAID_NODE.sub(lambda m: m.group("id"), raw)):
                l, r = arrow.group("l"), arrow.group("r")
                links.append((a, b, {
                    "line": i + 1,
                    "index": len(links),
                    "direction": "both" if l and r else "forward" if r else "backward" if l else "none",
                    "dotted": "." in arrow.group("body"),
                }))
        for _, _, e in links:
            e["blue"] = "default" in blue or e["index"] in blue
        k = b1 + 1
        while k < end and not ANY_HEAD.match(lines[k]) and not lines[k].strip().startswith("```"):
            legend += bool(lines[k].strip())
            k += 1

    kind = {n: v["kind"] for n, v in nodes.items()}
    name = {n: v["label"] for n, v in nodes.items()}
    data = set(DFD_KINDS)
    writers, readers, sources = defaultdict(set), defaultdict(set), defaultdict(set)
    for a, b, e in links:
        # A dotted line carries no data, and an undirected one says nothing of which way it moves.
        if e["dotted"] or e["direction"] == "none":
            continue
        pairs = [(a, b)] if e["direction"] in ("forward", "both") else []
        pairs += [(b, a)] if e["direction"] in ("backward", "both") else []
        for src, dst in pairs:
            if kind.get(dst) in data and kind.get(src) in ("step", "role"):
                sources[dst].add(src)
                if kind.get(src) == "step":
                    writers[dst].add(src)
            if kind.get(src) in data and kind.get(dst) == "step":
                readers[src].add(dst)

    def number(n):
        m = STEP_NUMBER.match(name.get(n, ""))
        return int(m.group(1)) if m else None

    headings = [s["heading"] for s in steps]
    drawn = [v["label"] for v in nodes.values() if v["kind"] == "step"]

    # A record several steps write is not one that a later step overwrites when every writer after the
    # first also reads it - the two-headed arrow - for each builds on what the one before left. Such a
    # record is edited in turn, and its first writer, when it reads the record too, starts from a state
    # that was there before the run: a step before it reads the record as found, not a later write.
    def order(d):
        ws = sorted(writers.get(d, ()), key=lambda w: (number(w) is None, number(w) or 0))
        return ws if all(number(w) is not None for w in ws) else None

    edited_in_turn, overwritten, as_found = {}, {}, {}
    for d, ws in writers.items():
        if kind.get(d) != "record":
            continue
        ordered = order(d)
        if len(ws) > 1:
            later = [w for w in ordered[1:] if w not in readers.get(d, ())] if ordered else sorted(ws)
            if later:
                overwritten[d] = later
            else:
                edited_in_turn[d] = ordered
        if ordered and ordered[0] in readers.get(d, ()):
            before = [r for r in sorted(readers[d], key=lambda r: number(r) or 0)
                      if number(r) is not None and number(r) < number(ordered[0])]
            if before:
                as_found[d] = (ordered[0], before)

    def exempt(d, r):
        """Whether step r reads record d without reading a later write: d is edited in turn and r comes
        after its first writer, or its first writer reads it too (so r reads it as found)."""
        if d in edited_in_turn:
            first = order(d)[0]
            return number(r) >= number(first) or first in readers.get(d, ())
        return d in as_found and r in as_found[d][1]

    return {
        "has_dataflow": True,
        "file": str(path),
        "line": start + 1,
        "mermaid_blocks": len(blocks),
        "nodes": [{"id": n, **v} for n, v in nodes.items()],
        "edges": [{"from": name.get(a, a), "to": name.get(b, b), **e} for a, b, e in links],
        "legend_lines": legend,
        "steps_not_drawn": [h for h in headings if h not in drawn],
        "processes_not_steps": [d for d in drawn if d not in headings],
        "multi_writer_records": [
            {"record": name[d], "line": nodes[d]["line"], "writers": sorted(name[w] for w in ws),
             "overwritten_by": [name[w] for w in overwritten[d]]}
            for d, ws in writers.items()
            if d in overwritten
        ],
        "records_edited_in_turn": [
            {"record": name[d], "line": nodes[d]["line"], "writers": [name[w] for w in ws]}
            for d, ws in edited_in_turn.items()
        ],
        "records_read_as_found": [
            {"record": name[d], "line": nodes[d]["line"], "first_writer": name[w], "readers": [name[r] for r in rs]}
            for d, (w, rs) in as_found.items()
        ],
        "unsourced_data": [
            {"data": v["label"], "kind": v["kind"], "line": v["line"]}
            for n, v in nodes.items()
            if v["kind"] in ("record", "one-run data") and not sources.get(n)
        ],
        "reads_of_later_writes": [
            {"data": name[d], "reader": name[r], "writer": name[w]}
            for d, rs in readers.items()
            for r in sorted(rs)
            for w in sorted(writers.get(d, ()))
            if number(r) is not None and number(w) is not None and number(w) > number(r)
            and not exempt(d, r)
        ],
        "edges_between_data": [
            {"from": name.get(a, a), "to": name.get(b, b), "line": e["line"]}
            for a, b, e in links
            if not e["dotted"] and kind.get(a) in data and kind.get(b) in data
        ],
    }


def load_depends_on(path: Path):
    """The shared depends_on.py, loaded as a module: the header quote is read and fingerprinted as its
    check command does, so a status here is never one that command would not give."""
    spec = importlib.util.spec_from_file_location("depends_on", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["depends_on"] = module
    spec.loader.exec_module(module)
    return module


def readme_required_headings(template: Path) -> list:
    """The README template's # and ## headings, in template order, each with its # marks - all but its
    title, which names the skill and so is a placeholder in the template."""
    out, inside = [], False
    for ln in template.read_text(encoding="utf-8").splitlines():
        if ln.lstrip().startswith("```"):
            inside = not inside
        elif not inside and (m := README_HEAD.match(ln)) and not PLACEHOLDER.search(m.group(2)):
            out.append(f"{m.group(1)} {m.group(2)}")
    return out


def header_quote(path: Path, dep, dep_config) -> dict:
    """Each dependency the header quote of README.md declares, with the status depends_on.py check gives it."""
    try:
        lines = dep.read_lines(path)
        deps = dep.entries(path, lines)
    except dep.Fault as e:
        return {"error": str(e), "entries": []}
    cites = dep.citations(lines)
    out = []
    for e in deps:
        try:
            target = dep.resolve(e, path, dep_config, None)
            now = None if target is None else dep.fingerprint(target, cites if e.cited else None)
        except dep.Fault as ex:
            target, now = None, str(ex)
        if target is None:
            status = "MISSING"
        elif now is None:
            status = "NOTHING_CITED"
        elif e.sha is None:
            status = "NO_RECORD"
        else:
            status = "UNCHANGED" if e.sha == now else "CHANGED"
        out.append({
            "line": e.line + 1,
            "link": e.link,
            "status": status,
            "recorded": e.sha,
            "date": e.date,
            "now": now if target is not None else None,
            "line_text": lines[e.line].strip(),
        })
    return {"entries": out}


def step_purposes(lines, in_fence, headings) -> dict:
    """The items of README.md's Step Purposes: each step it names, and whether a Purpose is indented beneath it."""
    span = section(lines, in_fence, "Step Purposes", 2)
    if span is None:
        return {"present": False}
    start, end = span
    items, cur = [], None
    for i in range(start + 1, end):
        ln = lines[i]
        if in_fence[i]:
            continue
        if m := STEP_ITEM.match(ln):
            cur = {"step": m.group(1), "line": i + 1, "purpose_lines": 0}
            items.append(cur)
        elif cur is not None and ln.startswith("  ") and ln.strip():
            cur["purpose_lines"] += 1
        elif ln.strip():
            cur = None
    listed = [it["step"] for it in items]
    return {
        "present": True,
        "line": start + 1,
        "items": [{"step": it["step"], "line": it["line"], "has_purpose": it["purpose_lines"] > 0} for it in items],
        "steps_missing": [h for h in headings if h not in listed],
        "items_not_steps": [s for s in listed if s not in headings],
        "items_without_purpose": [it["step"] for it in items if not it["purpose_lines"]],
        "order_ok": [s for s in listed if s in headings] == [h for h in headings if h in listed],
    }


def files_each_step_uses(lines, in_fence, headings) -> dict:
    """The steps the tree of README.md's Files Each Step Uses names, and whether its prose answers the
    scripted-versus-not rule in a bold sentence."""
    span = section(lines, in_fence, "Files Each Step Uses", 2)
    if span is None:
        return {"present": False}
    start, end = span
    steps = [
        {"step": m.group(1), "line": i + 1}
        for i in range(start + 1, end)
        if in_fence[i] and not lines[i].lstrip().startswith("```") and (m := TREE_STEP.match(lines[i]))
    ]
    listed = [s["step"] for s in steps]
    return {
        "present": True,
        "line": start + 1,
        "answers_scripted_rule": any(SCRIPTED_RULE.search(lines[i]) for i in range(start + 1, end) if not in_fence[i]),
        "steps": steps,
        "steps_missing": [h for h in headings if h not in listed],
        "items_not_steps": [s for s in listed if s not in headings],
    }


def readme_content_in_skill_md(lines, in_fence) -> dict:
    """What SKILL.md still holds that belongs in README.md - a Dataflow or Steps at a Glance heading, a
    Purpose line, the paragraph that introduces the Purposes - and every link it makes to README.md."""
    found, links = [], []
    for i, ln in enumerate(lines):
        if in_fence[i]:
            continue
        kind = None
        if (m := TOP_HEAD.match(ln)) and m.group(1).strip() in README_SECTIONS:
            kind = "heading"
        elif PURPOSE.match(ln):
            kind = "purpose"
        elif PURPOSE_INTRO.search(ln):
            kind = "purpose intro"
        if kind:
            found.append({"line": i + 1, "kind": kind, "line_text": ln.strip()[:400]})
        if README_LINK.search(ln):
            links.append({"line": i + 1, "line_text": ln.strip()[:400]})
    return {"found": found, "links_to_readme": links}


def readme(skill_dir: Path, name: str, steps, required: list, dep, dep_config):
    """The readme facts of the skill's README.md, with its lines and fence map for the dataflow facts."""
    path = skill_dir / "README.md"
    twins = {
        "has_twin": (skill_dir / "README-tw.md").is_file(),
        "skill_has_twin": (skill_dir / "SKILL-tw.md").is_file(),
    }
    if not path.is_file():
        return {"has_readme": False, "path": str(path), **twins}, [], []
    lines = path.read_text(encoding="utf-8").split("\n")
    in_fence = fenced(lines)
    title, heads = None, {}
    for i, ln in enumerate(lines):
        if in_fence[i] or not (m := README_HEAD.match(ln)):
            continue
        if title is None and m.group(1) == "#":
            title = {"line": i + 1, "text": m.group(2)}
            continue
        heads.setdefault(f"{m.group(1)} {m.group(2)}", i + 1)
    headings = [s["heading"] for s in steps]

    def tokens(pattern):
        out = []
        for i, ln in enumerate(lines, 1):
            spans = [(c.start(), c.end()) for c in CODE_SPAN.finditer(ln)]
            for m in pattern.finditer(ln):
                out.append({
                    "line": i,
                    "text": m.group(0),
                    "backticked": any(s <= m.start() and m.end() <= e for s, e in spans),
                    "fenced": in_fence[i - 1],
                    "line_text": ln.strip()[:400],
                })
        return out

    present = [h for h in heads if h in required]
    facts = {
        "has_readme": True,
        "path": str(path),
        **twins,
        "title": title,
        "title_is_skill_name": bool(title) and title["text"] == name,
        "required_headings": required,
        "headings": heads,
        "missing_headings": [h for h in required if h not in heads],
        "heading_order_ok": present == [h for h in required if h in heads],
        "header_quote": header_quote(path, dep, dep_config),
        "step_purposes": step_purposes(lines, in_fence, headings),
        "files_each_step_uses": files_each_step_uses(lines, in_fence, headings),
        "placeholder_tokens": tokens(PLACEHOLDER),
        "old_placeholder_tokens": tokens(OLD_PLACEHOLDER),
    }
    return facts, lines, in_fence


def commented(lines, suffix):
    """Which lines sit in a comment or a Python docstring - a path shown there is an example, not a value."""
    out, quote = [False] * len(lines), None
    for i, ln in enumerate(lines):
        if quote:
            out[i] = True
            if ln.count(quote) % 2:
                quote = None
            continue
        if suffix == ".py":
            for q in ('"""', "'''"):
                if ln.count(q) % 2:
                    quote, out[i] = q, True
                    break
        if not out[i]:
            out[i] = bool(COMMENT_LEAD.match(ln))
    return out


def file_kind(rel: Path) -> str:
    """What the file is to the skill - a path in its own config.yaml is placed, one in a script is baked."""
    if len(rel.parts) == 1:
        if rel.name in ("config.yaml", "config.yml"):
            return "skill config"
        if rel.suffix.lower() == ".md":
            return "twin" if rel.stem.endswith("-tw") else "doc"
    return DIR_KINDS.get(rel.parts[0], "other")


def scan_dir(skill_dir: Path) -> dict:
    """Hardcoded-path facts for every text file in the skill directory except its own SKILL.md."""
    files, hardcoded, skipped = [], [], []
    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(skill_dir)
        if any(part in SKIP_DIRS for part in rel.parts) or rel.as_posix() == "SKILL.md":
            continue
        suffix = path.suffix.lower()
        if suffix not in TEXT_SUFFIXES:
            skipped.append({"file": rel.as_posix(), "reason": f"not a text file ({suffix or 'no suffix'})"})
            continue
        size = path.stat().st_size
        if size > MAX_SCAN_BYTES:
            skipped.append({"file": rel.as_posix(), "reason": f"{size} bytes, over the {MAX_SCAN_BYTES} byte scan limit"})
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            skipped.append({"file": rel.as_posix(), "reason": f"unreadable: {e}"})
            continue

        lines = text.split("\n")
        markdown = suffix == ".md"
        in_fence = fenced(lines) if markdown else [False] * len(lines)
        in_comment = [False] * len(lines) if markdown else commented(lines, suffix)
        found = 0
        for i, ln in enumerate(lines, 1):
            spans = [(c.start(), c.end()) for c in CODE_SPAN.finditer(ln)] if markdown else []
            for fact, pattern in PATH_FACTS:
                for m in pattern.finditer(ln):
                    found += 1
                    hardcoded.append({
                        "file": rel.as_posix(),
                        "kind": file_kind(rel),
                        "fact": fact,
                        "line": i,
                        "text": m.group(0),
                        "backticked": any(s <= m.start() and m.end() <= e for s, e in spans),
                        "fenced": in_fence[i - 1],
                        "commented": in_comment[i - 1],
                        "line_text": ln.strip()[:400],
                    })
        files.append({
            "file": rel.as_posix(),
            "kind": file_kind(rel),
            "lines": len(lines),
            "reads_config_yaml": [i for i, ln in enumerate(lines, 1) if "config.yaml" in ln],
            "hardcoded_paths": found,
        })
    return {
        "has_own_config": (skill_dir / "config.yaml").is_file(),
        "files_scanned": files,
        "skipped": skipped,
        "hardcoded_paths": hardcoded,
    }


def frontmatter(text: str, lines, skill_name: str) -> dict:
    if not lines or lines[0].strip() != "---":
        return {"parses": False, "reason": "no leading --- fence"}
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return {"parses": False, "reason": "unterminated --- fence"}
    try:
        data = yaml.safe_load("\n".join(lines[1:end])) or {}
    except yaml.YAMLError as e:
        return {"parses": False, "reason": f"YAML error: {e}"}
    name = data.get("name")
    desc = data.get("description")
    name_text = "" if name is None else str(name)
    desc_text = str(desc) if desc else ""
    return {
        "parses": True,
        "name": name,
        "name_matches_dir": name == skill_name,
        "name_chars": len(name_text),
        "name_charset_ok": bool(NAME_CHARSET.fullmatch(name_text)),
        "has_description": bool(desc),
        "description_words": len(desc_text.split()),
        # UTF-16 code units, as a JavaScript string counts its length: never fewer than the
        # characters, so text carrying an emoji is measured as the stricter count would.
        "description_chars": len(desc_text.encode("utf-16-le")) // 2,
    }


def scan(path: Path, group: str, name: str, required: list, readme_required: list, root: Path,
         dep, dep_config) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    region = regions(lines)
    in_fence = fenced(lines)
    secs = sections(lines)

    headings = {}
    for i, ln in enumerate(lines, 1):
        m = TOP_HEAD.match(ln)
        if m:
            headings.setdefault(m.group(1).strip(), i)

    steps, forward_refs, cur = [], [], None
    for i, ln in enumerate(lines, 1):
        m = STEP_HEAD.match(ln)
        if m:
            cur = int(m.group(1))
            steps.append({"number": cur, "title": m.group(2).strip(), "heading": ln[2:].strip(), "line": i})
            continue
        if cur is None:
            continue
        for r in STEP_REF.finditer(ln):
            nums = [int(x) for x in r.groups() if x]
            if any(n > cur for n in nums):
                forward_refs.append({"line": i, "in_step": cur, "ref": r.group(0)})

    readme_facts, readme_lines, readme_fence = readme(path.parent, name, steps, readme_required, dep, dep_config)
    readme_facts["readme_content_in_skill_md"] = readme_content_in_skill_md(lines, in_fence)

    def collect(pattern):
        out = []
        for i, ln in enumerate(lines, 1):
            spans = [(c.start(), c.end()) for c in CODE_SPAN.finditer(ln)]
            for m in pattern.finditer(ln):
                out.append({
                    "line": i,
                    "text": m.group(0),
                    "backticked": any(s <= m.start() and m.end() <= e for s, e in spans),
                    "fenced": in_fence[i - 1],
                    "line_text": ln.strip(),
                    "region": region[i - 1],
                })
        return out

    numbers = [s["number"] for s in steps]
    scripts_dir = path.parent / "scripts"
    on_disk = sorted(p.name for p in scripts_dir.glob("*.py")) if scripts_dir.is_dir() else []
    named = {m for m in NAMED_SCRIPT.findall(text)}

    broken_links = []
    for i, ln in enumerate(lines, 1):
        for m in MD_LINK.finditer(ln):
            target = m.group(1).split("#")[0].replace("\\", "/")
            if not (root / target).exists():
                broken_links.append({"line": i, "target": m.group(1)})

    return {
        "skill": name,
        "group": group,
        "path": str(path),
        "lines": len(lines),
        "template_shape": {
            "frontmatter": frontmatter(text, lines, name),
            "required_headings": required,
            "headings": headings,
            "missing_headings": [h for h in required if h not in headings],
            # Order is judged over the required headings that are present; extra sections may sit between or before them.
            "heading_order_ok": [h for h in headings if h in required]
            == [h for h in required if h in headings],
            "extra_headings": [h for h in headings if h not in required],
            "steps": steps,
            "step_numbers_contiguous_from_0": numbers == list(range(len(numbers))),
            "step_0_is_warmup": bool(steps) and steps[0]["number"] == 0 and "Warmup" in steps[0]["title"],
            "forward_references": forward_refs,
        },
        "config_shape": {
            "reads_config_yaml": [i for i, ln in enumerate(lines, 1) if "config.yaml" in ln],
            "literal_wiki_paths": collect(WIKI_PATH),
            "absolute_paths": collect(ABS_PATH),
            "unc_paths": collect(UNC_PATH),
            "literal_github_paths": collect(GITHUB_PATH),
            "placeholders": {
                key: [i for i, ln in enumerate(lines, 1) if key in ln]
                for key in ("{wikiDir}", "{vaultName}", "{skillGroups")
            },
            "resolves_wikidir": "wikiDir`**:" in text,
            "resolves_vaultname": "vaultName`**:" in text,
        },
        "dir_config_shape": scan_dir(path.parent),
        "leftovers": {
            "placeholder_tokens": collect(PLACEHOLDER),
            "old_placeholder_tokens": collect(OLD_PLACEHOLDER),
            "broken_github_links": broken_links,
            "scripts_named_but_missing": sorted(n for n in named if n not in on_disk and n in text),
            "scripts_on_disk_not_named": sorted(n for n in on_disk if n not in named),
        },
        "readme_shape": readme_facts,
        "terminology": terminology(lines, secs),
        "dataflow": dataflow(readme_lines, readme_fence, steps, path.parent / "README.md"),
    }


def summarize(doc: dict) -> dict:
    """One row per skill for the Scan table - counts only; the facts file holds the detail."""
    shape = doc["template_shape"]
    term = doc["terminology"]
    readme_facts = doc["readme_shape"]
    return {
        "skill": doc["skill"],
        "group": doc["group"],
        "lines": doc["lines"],
        "description_chars": shape["frontmatter"].get("description_chars"),
        "steps": len(shape["steps"]),
        "missing_headings": shape["missing_headings"],
        "heading_order_ok": shape["heading_order_ok"],
        "forward_references": len(shape["forward_references"]),
        "config_facts": sum(len(v) for v in doc["config_shape"].values() if isinstance(v, list)),
        "dir_files": len(doc["dir_config_shape"]["files_scanned"]),
        "dir_hardcoded_paths": len(doc["dir_config_shape"]["hardcoded_paths"]),
        "leftovers": sum(len(v) for v in doc["leftovers"].values()),
        "has_glossary": term["has_glossary"],
        "terms": len(term.get("terms", [])),
        "terms_defined_in_configuration": len(term.get("terms_defined_in_configuration", [])),
        "has_readme": readme_facts["has_readme"],
        "readme_missing_headings": readme_facts.get("missing_headings", []),
        "header_quote_not_unchanged": sum(
            e["status"] != "UNCHANGED" for e in readme_facts.get("header_quote", {}).get("entries", [])
        ),
        "readme_content_in_skill_md": len(readme_facts["readme_content_in_skill_md"]["found"]),
        "has_dataflow": doc["dataflow"]["has_dataflow"],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--skill", action="append", required=True, help="skill name; repeat per skill")
    ap.add_argument("--out", required=True, help="the facts file to write - a scratch file under the workspace temp folder")
    ap.add_argument("--template", required=True, help="path to SKILL-tmp.md; its headings are the reference")
    ap.add_argument("--readme-template", required=True,
                    help="path to README-tmp.md; its # and ## headings are the reference for README.md")
    ap.add_argument("--depends-on", required=True,
                    help="path to the shared depends_on.py, which reads README.md's header quote")
    ap.add_argument("--config", help="path to the workspace config.yaml; defaults to the nearest one above this script or the cwd")
    args = ap.parse_args()

    config = find_config(args.config)
    root = config.parent
    groups = load_config(config).get("skillGroups") or {}
    if not groups:
        raise SystemExit(f"{config} has no skillGroups")

    template = Path(args.template)
    if not template.is_file():
        raise SystemExit(f"SKILL template was not found: {template}")
    required = required_headings(template)
    if not required:
        raise SystemExit(f"SKILL template defines no top-level heading: {template}")

    readme_template = Path(args.readme_template)
    if not readme_template.is_file():
        raise SystemExit(f"README template was not found: {readme_template}")
    readme_required = readme_required_headings(readme_template)
    if not readme_required:
        raise SystemExit(f"README template defines no heading but its title: {readme_template}")

    depends_on = Path(args.depends_on)
    if not depends_on.is_file():
        raise SystemExit(f"depends_on.py was not found: {depends_on}")
    dep = load_depends_on(depends_on)
    dep_config = dep.load_config(config)

    docs, missing = [], []
    for name in args.skill:
        group, path = find_skill(groups, name, root)
        if path is None:
            missing.append(name)
            continue
        docs.append(scan(path, group, name, required, readme_required, root, dep, dep_config))

    for name in missing:
        print(f"# not found under any skillGroups root: {name}", file=sys.stderr)
    if not docs:
        return 1

    facts_path = Path(args.out)
    facts_path.parent.mkdir(parents=True, exist_ok=True)
    facts_path.write_text(
        yaml.safe_dump_all(docs, sort_keys=False, allow_unicode=True, width=4096),
        encoding="utf-8",
    )

    print(yaml.safe_dump(
        {
            "facts_file": str(facts_path),
            "config": str(config),
            "template": str(template),
            "required_headings": required,
            "readme_template": str(readme_template),
            "readme_required_headings": readme_required,
            "scanned": [summarize(d) for d in docs],
        },
        sort_keys=False, allow_unicode=True, width=4096,
    ), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
