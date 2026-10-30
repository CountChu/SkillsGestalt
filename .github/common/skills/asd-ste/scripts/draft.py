#!/usr/bin/env python3
"""The draft tool of the asd-ste skill: where a source file's draft goes, the replacement of the source
file by its approved draft, the documents that record the source file, and the check, once a day, of
every STE file that records ste-custom.md.

  paths SOURCE
      Print, as JSON, the paths a run uses for SOURCE - its TW twin, its draft, the draft's TW twin and
      the Checkpoint Dir - whether each file exists, whether SOURCE is a TW twin, and whether it is
      already in STE: its header quote declares [[ASD-STE100_ISSUE9.pdf]].
  replace SOURCE
      Write the draft over SOURCE, and the draft's TW twin over SOURCE's TW twin, then delete the draft
      and its TW twin. The header note keeps two of its three lines: the line that names STE, without
      the link to the source file, and the Technical words line; the header quote stays as it is. A TW
      twin under a frontmatter has its pairing line pointed back at SOURCE: the chinese skill adds that
      line to link to the draft, and its link then names SOURCE, in its text and in its target. Nothing
      is written unless both files are in the form House Rule 5 gives, and such a TW twin has a pairing
      line that links to the draft.
  dependents SOURCE --root DIR [--root DIR ...]
      Print each Markdown file under the roots whose header quote records SOURCE - a wiki link to its
      name, or a link whose path leads to it - with the link, one on each line; --json prints a list.
  recheck --root DIR [--root DIR ...] [--dry-run]
      Check again each file under the roots whose header quote records ste-custom.md with a fingerprint
      other than its current one, and record ste-custom.md again in each one that passes: a draft by
      the check of Step 3 against its source file, its report and findings file written into its
      Checkpoint Dir and its step_3 group saved; a file that a draft replaced by check_ste.py --ste; and
      a TW twin with the file it is the twin of. A file that fails keeps its old record, and is listed
      with its [FAIL] lines; a warning that the last check of a draft did not give is listed, and the
      draft is recorded all the same. --dry-run lists the files and the check each one would get, and
      changes nothing. ste-custom.md says when to run it: once, after its last change of the day.

The draft of DFD.md is DFD-ste.md beside it, and the draft's TW twin DFD-ste-tw.md: this script is the
one part of the skill that knows the names. The Checkpoint Dir is checkpoints/asd-ste/{parent}-{name}
under the workspace root, the directory the script runs in.

Exit status: 0 done; 1 replace refused - a draft or a TW twin that is missing, a header note not in the
form House Rule 5 gives, or a TW twin under a frontmatter with no pairing line to the draft - and
nothing written, or a file that recheck found failing; 2 a file missing or unreadable.
Standard library only, but recheck needs PyYAML to read a YAML checkpoint, as save_step.py does.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_ste import ENTRY_RE, Doc, Fault, header_quote, read_doc  # noqa: E402

HERE = Path(__file__).resolve().parent
CUSTOM = HERE.parent / 'references' / 'ste-custom.md'
DICTIONARY = HERE.parent / 'references' / 'ste-dictionary.json'
SPELLING = HERE.parents[2] / 'references' / 'us-spelling.json'
DEPENDS_ON = HERE.parents[2] / 'scripts' / 'depends_on.py'
CHECK_STE = HERE / 'check_ste.py'
SAVE_STEP = HERE / 'save_step.py'
CUSTOM_LINK = 'ste-custom'
SPEC = 'ASD-STE100_ISSUE9.pdf'
SKIP_DIRS = {'.git', 'node_modules', '.venv', 'venv', '__pycache__'}
# The header note of a draft and of its TW twin (House Rule 5): the line that names STE, which links to
# the source file, and the line that says the source file is correct where the two do not agree.
EN_NAMES = re.compile(r'^> This file is \[[^\]]+\]\([^)]+\) in (ASD-STE100 .+)$')
EN_CORRECT = re.compile(r'^> If the two files do not agree, \[[^\]]+\]\([^)]+\) is correct\.$')
TW_NAMES = re.compile(r'^> 本檔案是以 (ASD-STE100 .+?)寫成的 \[[^\]]+\]\([^)]+\)。$')
TW_CORRECT = re.compile(r'^> 兩份檔案不一致時，以 \[[^\]]+\]\([^)]+\) 為準。$')
# A link as the chinese skill's check_parity.py reads one, to find the pairing line of a TW twin.
PAIR_LINK = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')


class Refused(Exception):
    """A replacement that cannot be made: exit status 1, and nothing written."""


def names(source: Path) -> dict:
    stem = source.name[:-len('.md')] if source.name.endswith('.md') else source.stem
    return {
        'source_twin': source.with_name(f'{stem}-tw.md'),
        'draft': source.with_name(f'{stem}-ste.md'),
        'draft_twin': source.with_name(f'{stem}-ste-tw.md'),
        'checkpoint_dir': Path('checkpoints') / 'asd-ste' / f'{source.resolve().parent.name}-{stem}',
    }


def declares_spec(path: Path) -> bool:
    doc = read_doc(path)
    start = doc.frontmatter[1] + 1 if doc.frontmatter else 0
    for i in header_quote(doc.lines, start):
        m = ENTRY_RE.match(doc.lines[i])
        if m and (m['name'] or '').strip() == SPEC:
            return True
    return False


def paths(source: Path) -> dict:
    if not source.is_file():
        raise Fault(f'no file {source}')
    n = names(source)
    return {
        'source': str(source),
        'twin': source.name.endswith('-tw.md'),
        'ste': declares_spec(source),
        'source_twin': str(n['source_twin']), 'source_twin_exists': n['source_twin'].is_file(),
        'draft': str(n['draft']), 'draft_exists': n['draft'].is_file(),
        'draft_twin': str(n['draft_twin']), 'draft_twin_exists': n['draft_twin'].is_file(),
        'checkpoint_dir': n['checkpoint_dir'].as_posix(),
    }


def file_name(target: str) -> str:
    """The name of the file a link target leads to, as check_parity.py reads it."""
    return target.replace('\\', '/').split('#')[0].rstrip('/').rsplit('/', 1)[-1]


def pairing_line(doc: Doc, english: str) -> int | None:
    """The index of the pairing line of a TW twin under a frontmatter, found as check_parity.py finds it:
    the first line above the first heading with a link whose target names english, the file that the
    twin links back to. None when no line links to it."""
    end = doc.headings[0] if doc.headings else len(doc.lines)
    return next((i for i in range(end) if i not in doc.fenced and
                 any(file_name(m.group(2)) == english for m in PAIR_LINK.finditer(doc.lines[i]))), None)


def point_back(line: str, draft: str, source: str) -> str:
    """A pairing line with each link to the draft naming the source file in its place, in its text and
    in its target."""
    def swap(m: re.Match) -> str:
        text, target = m.groups()
        if file_name(target) != draft:
            return m.group(0)
        path, mark, anchor = target.partition('#')
        end = len(path.replace('\\', '/').rstrip('/'))
        return f'[{text.replace(draft, source)}]({path[:end - len(draft)]}{source}{path[end:]}{mark}{anchor})'
    return PAIR_LINK.sub(swap, line)


def tidy(path: Path, names_re: re.Pattern, correct_re: re.Pattern, plain: str,
         pair: tuple[str, str] | None = None) -> tuple[str, int | None]:
    """The text of a draft, or of its TW twin, with its header note cut to two lines. Given pair - the
    names of the draft and of the source file - a TW twin under a frontmatter also has its pairing line
    pointed back at the source file, and the number of that line in the text comes back with it."""
    doc = read_doc(path)
    if not doc.header_note:
        raise Refused(f'{path}: no header note under the header quote')
    lines = list(doc.lines)
    named = [i for i in doc.header_note if names_re.match(lines[i])]
    correct = [i for i in doc.header_note if correct_re.match(lines[i])]
    if len(named) != 1 or len(correct) != 1:
        raise Refused(f'{path}: the header note is not in the form House Rule 5 gives - '
                      f'{len(named)} line(s) that name STE, {len(correct)} that name the file that is correct')
    paired = None
    if pair and doc.frontmatter:
        paired = pairing_line(doc, pair[0])
        if paired is None:
            raise Refused(f'{path}: no pairing line above the first heading that links to {pair[0]}')
        lines[paired] = point_back(lines[paired], *pair)
    lines[named[0]] = plain.format(names_re.match(lines[named[0]]).group(1))
    del lines[correct[0]]
    # the pairing line's number in the text written: one less when the line cut from the header note is above it
    return '\n'.join(lines), None if paired is None else paired + 1 - (paired > correct[0])


def replace(source: Path) -> list[str]:
    n = names(source)
    if not source.is_file():
        raise Fault(f'no file {source}')
    if not n['draft'].is_file():
        raise Refused(f'no draft {n["draft"]} to replace {source} with')
    if n['source_twin'].is_file() and not n['draft_twin'].is_file():
        raise Refused(f'{source} has a TW twin, but its draft has none: {n["draft_twin"]} is missing')
    text, _ = tidy(n['draft'], EN_NAMES, EN_CORRECT, '> This file is in {}')
    twin, paired = tidy(n['draft_twin'], TW_NAMES, TW_CORRECT, '> 本檔案以 {}寫成。',
                        (n['draft'].name, source.name)) if n['draft_twin'].is_file() else (None, None)
    source.write_text(text, encoding='utf-8')
    done = [f'replaced {source} with its draft']
    if twin is not None:
        n['source_twin'].write_text(twin, encoding='utf-8')
        done.append(f'replaced {n["source_twin"]} with the draft\'s TW twin')
        if paired is not None:
            done.append(f'pointed the pairing line of {n["source_twin"]} (line {paired}) back at {source.name}')
        n['draft_twin'].unlink()
        done.append(f'deleted {n["draft_twin"]}')
    n['draft'].unlink()
    done.append(f'deleted {n["draft"]}')
    return done


def dependents(source: Path, roots: list[Path]) -> list[dict]:
    target = source.resolve()
    stem = source.name[:-len('.md')]
    found, seen = [], set()
    for root in roots:
        for folder, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for f in files:
                path = Path(folder) / f
                if not f.endswith('.md') or path.resolve() == target or path.resolve() in seen:
                    continue
                seen.add(path.resolve())
                try:
                    doc = read_doc(path)
                except Fault:
                    continue
                start = doc.frontmatter[1] + 1 if doc.frontmatter else 0
                for i in header_quote(doc.lines, start):
                    m = ENTRY_RE.match(doc.lines[i])
                    if not m:
                        continue
                    name, link = (m['name'] or '').strip(), m['apath'] or m['path']
                    if name:
                        hit = name in (stem, source.name)
                    else:
                        hit = '{' not in link and (path.parent / link).resolve() == target
                    if hit:
                        found.append({'file': str(path), 'line': i + 1,
                                      'link': f'[[{name}]]' if name else link})
    return found


def record_of(path: Path, name: str) -> tuple[str, str] | None:
    """The date and the fingerprint that the header quote of path records for [[name]]: ('', '') for a
    line with no record yet, None when the header quote does not declare it."""
    doc = read_doc(path)
    start = doc.frontmatter[1] + 1 if doc.frontmatter else 0
    for i in header_quote(doc.lines, start):
        m = ENTRY_RE.match(doc.lines[i])
        if m and (m['name'] or '').strip() == name:
            spans = [s for s in re.findall(r'`([^`]*)`', m['rec'] or '') if s != 'cited']
            return (spans[0], spans[1]) if len(spans) >= 2 else ('', '')
    return None


def workspace(path: Path) -> Path:
    """The workspace that holds path: the nearest directory above it with a .git."""
    for folder in path.resolve().parents:
        if (folder / '.git').exists():
            return folder
    return Path.cwd()


def run(cmd: list[str], cwd: Path | None = None) -> tuple[int, list[str]]:
    r = subprocess.run([sys.executable, *cmd], cwd=cwd, capture_output=True, text=True, encoding='utf-8')
    return r.returncode, (r.stdout + r.stderr).splitlines()


def fingerprint(path: Path) -> str:
    code, out = run([str(DEPENDS_ON), 'hash', str(path)])
    if code != 0 or not out:
        raise Fault(f'depends_on.py hash {path}: {" ".join(out)}')
    return out[-1].split()[-1]


def record_custom(path: Path) -> tuple[bool, str]:
    """Record ste-custom.md in the header quote of path, from the root of its workspace."""
    root = workspace(path)
    cmd = [str(DEPENDS_ON), 'record', str(path.resolve().relative_to(root)), '--target', f'[[{CUSTOM_LINK}]]']
    if (root / 'config.yaml').is_file():
        cmd += ['--config', 'config.yaml']
    code, out = run(cmd, cwd=root)
    return code == 0, ' '.join(line for line in out if line.startswith(('recorded', 'error')))


def check_ste(ste: Path, src: Path | None = None, report: Path | None = None,
              findings: Path | None = None) -> tuple[int, list[str]]:
    cmd = [str(CHECK_STE)] + (['--src', str(src)] if src else []) + [
        '--ste', str(ste), '--dict', str(DICTIONARY), '--custom', str(CUSTOM), '--spelling', str(SPELLING)]
    cmd += (['--report', str(report)] if report else []) + (['--findings', str(findings)] if findings else [])
    return run(cmd)


def warnings_in(lines: list[str]) -> list[str]:
    return [line[len('[WARN] '):] for line in lines if line.startswith('[WARN] ')]


def bare(warning: str) -> str:
    """A warning without its line numbers, so that a line added above it does not make it a new one."""
    return ' '.join(re.sub(r'\(lines? [^)]*\)|\blines? \d+(?:, \d+)*(?:, \.\.\.)?', '', warning).split())


def kind_of(path: Path) -> tuple[str, Path | None]:
    """What recheck does with a file that records ste-custom.md: ('twin', its English file),
    ('draft', its source file), ('ste', None) for a file a draft replaced, or ('hand', None)."""
    if path.name.endswith('-tw.md'):
        return 'twin', path.with_name(path.name[:-len('-tw.md')] + '.md')
    if path.name.endswith('-ste.md'):
        source = path.with_name(path.name[:-len('-ste.md')] + '.md')
        if source.is_file():
            return 'draft', source
    if declares_spec(path):
        return 'ste', None
    return 'hand', None


def recheck_draft(draft: Path, source: Path, current: str, today: str) -> tuple[bool, list[str]]:
    """Check a draft again as Step 3 does, and on a pass record ste-custom.md and save its step_3 group."""
    folder = workspace(draft) / names(source)['checkpoint_dir']
    report = folder / 'step_3-check.txt'
    before = warnings_in(report.read_text(encoding='utf-8').splitlines()) if report.is_file() else []
    begin = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with tempfile.TemporaryDirectory() as tmp:
        new_report, new_findings = Path(tmp) / 'step_3-check.txt', Path(tmp) / 'step_3-findings.json'
        code, out = check_ste(draft, source, new_report, new_findings)
        if code != 0:
            return False, [line for line in out if line.startswith('[FAIL]')] or out[-3:]
        recorded, said = record_custom(draft)
        if not recorded:
            return False, [said]
        notes = []
        now = warnings_in(out)
        new = [w for w in now if bare(w) not in {bare(b) for b in before}]
        notes += [f'[NEW WARN] {w}' for w in new]
        if not (folder / 'process.yaml').is_file():
            return True, notes + ['no YAML checkpoint: the step_3 group is not saved']
        shutil.move(str(new_report), report)
        shutil.move(str(new_findings), folder / 'step_3-findings.json')
    import yaml
    group = (yaml.safe_load((folder / 'process.yaml').read_text(encoding='utf-8')) or {}).get('step_3') or {}
    why = {bare(w.get('warning', '')): w.get('why', '') for w in group.get('warnings_left') or []}
    left = [{'warning': w, 'why': why.get(bare(w)) or
             (f'new at draft.py recheck on {today}: not read yet' if w in new else
              'given by the check before as well, with no reason saved')} for w in now]
    spec = record_of(draft, SPEC)
    cmd = [str(SAVE_STEP), '--checkpoint', str(folder / 'process.yaml'), '--step', '3', '--title', 'STE Check',
           '--begin', begin, '--data', str(folder / 'step_3-findings.json'),
           '--set', 'report_file=step_3-check.txt', '--set', 'findings_file=step_3-findings.json',
           '--json', 'check_runs=1', '--json', 'warnings_left=' + json.dumps(left, ensure_ascii=False),
           '--json', 'custom_fingerprint=' + json.dumps({'date': today, 'fingerprint': current})]
    if spec and spec[1]:
        cmd += ['--json', 'fingerprint=' + json.dumps({'date': spec[0], 'fingerprint': spec[1]})]
    else:
        cmd += ['--set', 'fingerprint_not_recorded=the header quote holds no record of the STE specification']
    code, out = run(cmd)
    return True, notes + ([] if code == 0 else [f'step_3 not saved: {" ".join(out)}'])


def recheck(roots: list[Path], dry_run: bool) -> tuple[list[str], bool]:
    current, today = fingerprint(CUSTOM), datetime.date.today().isoformat()
    files = [Path(d['file']) for d in dependents(CUSTOM, roots)]
    stale = [f for f in files if (record_of(f, CUSTOM_LINK) or ('', ''))[1] != current]
    lines = [f'ste-custom.md is {current}: {len(files)} file(s) record it, {len(stale)} of them with another fingerprint']
    recording = {f.resolve() for f in files}
    waiting = {f.resolve() for f in stale}
    passed, recorded_count, failed = set(), 0, False
    for f in sorted(stale, key=lambda p: (kind_of(p)[0] == 'twin', str(p))):
        kind, other = kind_of(f)
        if kind == 'hand':
            lines.append(f'[BY HAND] {f} - neither a draft nor an STE file: read the change, then record it')
        elif dry_run:
            lines.append({'twin': f'[STALE] {f} - recorded with {other}',
                          'draft': f'[STALE] {f} - the check of Step 3 against {other}',
                          'ste': f'[STALE] {f} - check_ste.py --ste'}[kind])
        elif kind == 'twin':
            english = other.resolve()
            if english in passed or (english in recording and english not in waiting):
                recorded, said = record_custom(f)
                lines.append(f'[RECORDED] {f} - with {other}' if recorded else f'[FAILED] {f} - {said}')
                recorded_count += recorded
                failed |= not recorded
            else:
                lines.append(f'[NOT RECORDED] {f} - {other} did not pass, or records no ste-custom.md')
                failed = True
        else:
            if kind == 'draft':
                ok, notes = recheck_draft(f, other, current, today)
            else:
                code, out = check_ste(f)
                ok = code == 0
                notes = [f'[WARN] {w}' for w in warnings_in(out)] if ok else \
                    [line for line in out if line.startswith('[FAIL]')] or out[-3:]
                if ok:
                    recorded, said = record_custom(f)
                    ok, notes = recorded, notes if recorded else [said]
            if ok:
                passed.add(f.resolve())
                recorded_count += 1
                lines.append(f'[RECORDED] {f} - ' + ('the check of Step 3 PASS, step_3 saved' if kind == 'draft'
                                                     else 'check_ste.py --ste PASS'))
            else:
                lines.append(f'[FAILED] {f} - the old record stays')
                failed = True
            lines.extend(f'    {n}' for n in notes)
    if not dry_run:
        lines.append(f'verdict: {"FAIL" if failed else "PASS"} - {recorded_count} of {len(stale)} recorded again'
                     + ('; a file failed: correct it, then run step 3 on a draft, or check_ste.py --ste on an STE file'
                        if failed else ''))
    return lines, failed


def main() -> None:
    ap = argparse.ArgumentParser(description='The draft tool of the asd-ste skill.')
    sub = ap.add_subparsers(dest='command', required=True)
    sub.add_parser('paths', help='the paths a run uses for a source file').add_argument('source', type=Path)
    sub.add_parser('replace', help='replace a source file by its draft').add_argument('source', type=Path)
    dep = sub.add_parser('dependents', help='the Markdown files whose header quote records a source file')
    dep.add_argument('source', type=Path)
    dep.add_argument('--root', type=Path, action='append', required=True, help='a directory to search')
    dep.add_argument('--json', action='store_true', help='print a JSON list')
    rec = sub.add_parser('recheck', help='check again each STE file that records an older ste-custom.md')
    rec.add_argument('--root', type=Path, action='append', required=True, help='a directory to search')
    rec.add_argument('--dry-run', action='store_true', help='list the files and their checks only')
    a = ap.parse_args()
    try:
        if a.command == 'paths':
            print(json.dumps(paths(a.source), ensure_ascii=False, indent=1))
        elif a.command == 'replace':
            for line in replace(a.source):
                print(line)
        elif a.command == 'recheck':
            lines, failed = recheck(a.root, a.dry_run)
            print('\n'.join(lines))
            if failed:
                sys.exit(1)
        else:
            if not a.source.is_file():
                raise Fault(f'no file {a.source}')
            found = dependents(a.source, a.root)
            if a.json:
                print(json.dumps(found, ensure_ascii=False, indent=1))
            else:
                for d in found:
                    print(f'{d["file"]}\t{d["link"]}')
                print(f'{len(found)} file(s) record {a.source.name}')
    except Refused as e:
        print(f'refused: {e}', file=sys.stderr)
        sys.exit(1)
    except Fault as e:
        print(f'error: {e}', file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
