"""Verify the imp-{app} owner skill, its design and wireframe pairs and the app dir that gen-imp-app Step 3 produced.

Exits non-zero if any check fails: a failing check is a defect in what was just written.
"""
import argparse
import json
import os
import re
import sys

import yaml

CANONICAL_SECTIONS = [
    "TERMINOLOGY",
    "DEDICATED TERMINOLOGY",
    "CONFIGURATION",
    "MUST FOLLOW",
    "Prompt Examples",
    "Workflow",
]
PLACEHOLDER_RE = re.compile(r"_{3,}[A-Z0-9_]*_{3,}")
SECTION_NO_RE = re.compile(r"^#{1,4}\s+(\d+(?:\.\d+)*)\s")
# Node 'require' / ESM import of a bare specifier; anything not relative and not node: is a package.
BARE_IMPORT_RE = re.compile(r"""require\(\s*['"]([^'"]+)['"]\s*\)|from\s+['"]([^'"]+)['"]""")
NODE_BUILTINS = {
    "assert", "buffer", "child_process", "cluster", "console", "crypto", "dgram", "dns", "events",
    "fs", "http", "http2", "https", "net", "os", "path", "perf_hooks", "process", "punycode",
    "querystring", "readline", "stream", "string_decoder", "timers", "tls", "tty", "url", "util",
    "v8", "vm", "worker_threads", "zlib",
}
EXTERNAL_REF_RE = re.compile(
    r"""<script[^>]+src\s*=\s*['"](?:https?:)?//|<link[^>]+href\s*=\s*['"](?:https?:)?//|@import\s+url\(\s*['"]?(?:https?:)?//""",
    re.I,
)
# The app must publish its handler and keep the listen behind a direct-start check, so that
# requiring it starts nothing. Neither failure is visible in a reading of the code.
CREATE_APP_RE = re.compile(r"\bcreateApp\b")
DIRECT_START_RE = re.compile(r"require\.main\s*===\s*module")
# An address written from the origin root works at '/' and nowhere else. Only the leading slash is
# the fault: '//host/x' is a protocol-relative URL and EXTERNAL_REF_RE already owns that case.
ORIGIN_ROOT_RE = re.compile(
    r"""(?:src|href|action)\s*=\s*['"](/[^/'"][^'"]*)['"]"""
    r"""|(?:fetch|EventSource)\s*\(\s*[`'"](/[^/`'"][^`'"]*)[`'"]""",
)
# A design says what the app must be. Naming the procedure that builds it makes the two define each
# other, and neither is a single source any more. 'the skill it replaces' is a Requirement, so bare
# 'skill' is not forbidden here.
PROCEDURE_TERMS = ("SKILL.md", "owner skill", "builder")


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def check_frontmatter(skill_md, skill_dir, results):
    text = read(skill_md)
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        results.append(("frontmatter", False, "SKILL.md has no YAML frontmatter block"))
        return text, {}
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as exc:
        results.append(("frontmatter", False, f"frontmatter does not parse: {exc}"))
        return text, {}

    expected = os.path.basename(os.path.normpath(skill_dir))
    name_ok = fm.get("name") == expected
    results.append(("frontmatter name", name_ok,
                    f"name={fm.get('name')!r} parent dir={expected!r}"))
    desc = (fm.get("description") or "").strip()
    results.append(("frontmatter description", bool(desc), f"{len(desc)} chars"))

    leftovers = sorted(set(PLACEHOLDER_RE.findall(text)))
    results.append(("no template placeholders", not leftovers,
                    ", ".join(leftovers) if leftovers else "none"))
    return text, fm


def check_sections(text, results):
    found = re.findall(r"^# (.+)$", text, re.M)
    present = [s for s in CANONICAL_SECTIONS if s in found]
    order_ok = present == [s for s in found if s in CANONICAL_SECTIONS]
    missing = [s for s in CANONICAL_SECTIONS if s not in found]
    results.append(("canonical sections", order_ok and not missing,
                    f"found {found}; missing {missing or 'none'}"))

    steps = [int(n) for n in re.findall(r"^## Step (\d+) - ", text, re.M)]
    contiguous = steps == list(range(len(steps))) and len(steps) >= 2
    results.append(("step headings contiguous from 0", contiguous, f"steps {steps}"))


def check_markdown(text, label, results):
    fences = len(re.findall(r"^```", text, re.M))
    results.append((f"{label}: code fences balanced", fences % 2 == 0, f"{fences} fence lines"))

    bad = []
    for block in re.split(r"\n\s*\n", text):
        rows = [ln for ln in block.splitlines() if ln.strip().startswith("|")]
        if len(rows) < 2:
            continue
        counts = {r.replace(r"\|", "").count("|") for r in rows}
        if len(counts) > 1:
            bad.append(rows[0].strip()[:60])
    results.append((f"{label}: table columns consistent", not bad,
                    "; ".join(bad) if bad else "every table block uniform"))


def check_design_pair(skill_dir, skill_text, results):
    refs = os.path.join(skill_dir, "references")
    if not os.path.isdir(refs):
        results.append(("design pair present", False, f"no references dir at {refs}"))
        return
    en = sorted(f for f in os.listdir(refs) if f.endswith("-RSDC.md"))
    tw = sorted(f for f in os.listdir(refs) if f.endswith("-RSDC-tw.md"))
    if not en or not tw:
        results.append(("design pair present", False, f"english={en} chinese={tw}"))
        return
    results.append(("design pair present", True, f"{en[0]} + {tw[0]}"))

    en_text, tw_text = read(os.path.join(refs, en[0])), read(os.path.join(refs, tw[0]))
    en_nums = [m.group(1) for m in (SECTION_NO_RE.match(ln) for ln in en_text.splitlines()) if m]
    tw_nums = [m.group(1) for m in (SECTION_NO_RE.match(ln) for ln in tw_text.splitlines()) if m]
    results.append(("design pair sections match", en_nums == tw_nums,
                    f"en={len(en_nums)} tw={len(tw_nums)}"
                    + ("" if en_nums == tw_nums
                       else f"; only-en={sorted(set(en_nums) - set(tw_nums))} "
                            f"only-tw={sorted(set(tw_nums) - set(en_nums))}")))
    for label, txt in (("RSDC en", en_text), ("RSDC tw", tw_text)):
        check_markdown(txt, label, results)

    # The dependency runs one way, and both ends are checked.
    for label, txt in (("en", en_text), ("tw", tw_text)):
        named = [t for t in PROCEDURE_TERMS if t in txt]
        results.append((f"RSDC {label}: names no procedure", not named,
                        ", ".join(named) if named else "no SKILL.md / owner skill / builder"))
    refers = en[0] in skill_text
    results.append(("SKILL.md refers to design pair", refers,
                    f"names {en[0]}" if refers else f"no reference to {en[0]}"))


def check_wireframe_pair(skill_dir, skill_text, results):
    refs = os.path.join(skill_dir, "references")
    en_path = os.path.join(refs, "Wireframe.md")
    tw_path = os.path.join(refs, "Wireframe-tw.md")
    missing = [os.path.basename(p) for p in (en_path, tw_path) if not os.path.isfile(p)]
    results.append(("wireframe pair present", not missing,
                    f"missing {missing}" if missing else "Wireframe.md + Wireframe-tw.md"))
    if missing:
        return

    shapes = []
    for path in (en_path, tw_path):
        text = read(path)
        lines = text.splitlines()
        shapes.append((
            len([ln for ln in lines if ln.startswith("## ")]),
            len([ln for ln in lines if ln.lstrip().startswith("- ")]),
            len([ln for ln in lines if ln.strip().startswith("|")]),
        ))
        check_markdown(text, f"wireframe {'en' if path is en_path else 'tw'}", results)
    results.append(("wireframe pair shapes match", shapes[0] == shapes[1],
                    f"en={shapes[0]} tw={shapes[1]} (headings, bullets, table rows)"))

    # The skill must point at the wireframe, not carry a second inventory of the same page.
    refers = "Wireframe.md" in skill_text
    results.append(("SKILL.md refers to wireframe", refers,
                    "names Wireframe.md" if refers else "no reference to Wireframe.md"))


def check_app_dir(app_dir, results):
    if not os.path.isdir(app_dir):
        results.append(("app dir present", False, f"not a directory: {app_dir}"))
        return
    results.append(("app dir present", True, app_dir))

    has_modules, packages, external = [], [], []
    origin_root = []
    for base, dirs, files in os.walk(app_dir):
        if "node_modules" in dirs:
            has_modules.append(os.path.join(base, "node_modules"))
            dirs.remove("node_modules")
        for name in files:
            path = os.path.join(base, name)
            rel = os.path.relpath(path, app_dir)
            if name.endswith((".js", ".mjs")):
                for a, b in BARE_IMPORT_RE.findall(read(path)):
                    spec = a or b
                    if spec.startswith((".", "/", "node:")) or spec.split("/")[0] in NODE_BUILTINS:
                        continue
                    packages.append(f"{rel}: {spec}")
            if name.endswith((".html", ".css")) and EXTERNAL_REF_RE.search(read(path)):
                external.append(rel)
            # Every address a browser is handed, wherever it was written. `public\` covers a page
            # served as a file; the root .js files cover one the server renders or generates.
            if name.endswith((".html", ".js")) and (
                os.path.basename(base) == "public" or os.path.samefile(base, app_dir)
            ):
                for a, b in ORIGIN_ROOT_RE.findall(read(path)):
                    origin_root.append(f"{rel}: {a or b}")

    results.append(("no node_modules", not has_modules, "; ".join(has_modules) or "none"))
    results.append(("node stdlib only", not packages, "; ".join(packages) or "no bare imports"))
    results.append(("page has no external refs", not external,
                    "; ".join(external) or "no cdn/script/link off-origin"))

    # The two halves of being mountable, both invisible in a reading of the code.
    entry = os.path.join(app_dir, "app.js")
    server = os.path.join(app_dir, "server.js")
    has_entry = os.path.isfile(entry) and bool(CREATE_APP_RE.search(read(entry)))
    results.append(("app.js publishes createApp", has_entry,
                    entry if has_entry else f"missing or exports no createApp: {entry}"))
    guarded = os.path.isfile(server) and bool(DIRECT_START_RE.search(read(server)))
    results.append(("server.js guards its listen", guarded,
                    "require.main === module" if guarded
                    else f"no direct-start guard in {server} - requiring it would bind a port"))
    results.append(("page emits no origin-root address", not origin_root,
                    "; ".join(origin_root) or "every address is relative to the page"))


def main():
    ap = argparse.ArgumentParser(description="Verify an imp-{app} owner skill and its app dir.")
    ap.add_argument("--skill-dir", required=True, help="the imp-{app} skill directory")
    ap.add_argument("--app-dir", required=True, help="the app dir under artifacts")
    ap.add_argument("--out", required=True, help="checkpoint directory for owner-skill-check.json")
    args = ap.parse_args()

    skill_md = os.path.join(args.skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        sys.exit(f"no SKILL.md at {skill_md}")

    results = []
    text, _ = check_frontmatter(skill_md, args.skill_dir, results)
    check_sections(text, results)
    check_markdown(text, "SKILL.md", results)
    check_design_pair(args.skill_dir, text, results)
    check_wireframe_pair(args.skill_dir, text, results)
    check_app_dir(args.app_dir, results)

    width = max(len(name) for name, _, _ in results)
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}  {name.ljust(width)}  {detail}")
    failed = [name for name, ok, _ in results if not ok]
    print(f"\n{len(results) - len(failed)}/{len(results)} passed")

    os.makedirs(args.out, exist_ok=True)
    out_file = os.path.join(args.out, "owner-skill-check.json")
    with open(out_file, "w", encoding="utf-8") as fh:
        json.dump({
            "skillDir": args.skill_dir,
            "appDir": args.app_dir,
            "checks": [{"check": n, "pass": ok, "detail": d} for n, ok, d in results],
            "failed": failed,
        }, fh, indent=2)
    print(f"wrote {out_file}")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
