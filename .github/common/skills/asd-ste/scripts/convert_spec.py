#!/usr/bin/env python3
"""Convert the dictionary of the ASD-STE100 specification PDF into the STE dictionary JSON.

The JSON is what check_ste.py reads: each approved word with its parts of speech, the forms of each
approved verb and adjective, and each unapproved word or phrase with the approved words that replace
it. It keeps no meaning and no example - only these word lists - and it is committed with the skill,
so that no run of the skill needs the PDF.

The JSON also records the PDF it was built from: its issue, its date, its file name and its
fingerprint - the first 12 hex digits of the SHA-256 of its bytes, as depends_on.py fingerprints a
file that is not text - so that check_ste.py can say when a header quote names another PDF.

The dictionary pages (Part 2, pages 2-1-*) are read in pypdf's layout mode, which keeps the four
columns of the table apart: the word and its part of speech, its approved meaning or the approved
words that replace it, an STE example, and a non-STE example. Only the first two columns are kept.

This is not a step of the workflow: it runs once for each issue of the specification.

Usage:
  python convert_spec.py --pdf <ASD-STE100_ISSUE9.pdf> --json <ste-dictionary.json>

Needs pypdf, and cryptography for the AES the PDF is encrypted with: pip install pypdf cryptography

Exit status: 0 written; 1 the PDF holds no dictionary page this script can read; 2 a file missing or
unreadable, or pypdf missing.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

POS = ('n', 'v', 'adj', 'adv', 'prep', 'conj', 'pron', 'art', 'prefix', 'suffix')
EN_DASH, ELLIPSIS = chr(0x2013), chr(0x2026)
WORD = r"[A-Za-z][A-Za-z'\-]*"
# A word of a headword, or the dots that stand for the words between: AS ... AS (conj).
HEAD_WORD = rf"(?:{WORD}|\.\.\.|{ELLIPSIS})"
# A headword: up to four words, any other spelling after a comma, a phrase or another spelling in
# parentheses, then its part of speech in parentheses: CONTAIN (v), MAKE SURE (v), MATT (or MATTE)
# (adj), long (as long as) (conj).
NOT_POS = rf'(?!(?:{"|".join(POS)})\))'
HEADWORD_RE = re.compile(rf'^(?P<word>{HEAD_WORD}(?: {HEAD_WORD}){{0,3}})(?P<variants>(?:, {WORD})*)'
                         rf'(?: \({NOT_POS}(?P<paren>[^()]*)\))? \((?P<pos>{"|".join(POS)})\)(?P<rest>.*)$')
# A phrase in lower case with no part of speech, which opens an entry of its own: such as
PHRASE_RE = re.compile(rf"^[a-z][a-z'\-]*(?: [a-z][a-z'\-]*){{1,2}}$")
# An approved word as the alternatives column prints it: MAKE SURE (v), ONE (TN).
ALT_RE = re.compile(rf"(?<![A-Za-z])([A-Z][A-Z'\-]*(?: [A-Z][A-Z'\-]*)*) \(({'|'.join(POS)}|TN|TV)\)")
PAGE_RE = re.compile(r'Page (\d)-(\d+)-([A-Z]?\d+)')
TITLE_RE = re.compile(r'ASD.?STE100 Simplified Technical English')
DATE_RE = re.compile(r'^\s*\d{4}-\d{2}-\d{2}\s*$')
PART_TITLE_RE = re.compile(rf'^\s*Part [12] [-{EN_DASH}] (Dictionary|Writing rules)\s*$')


def fail(message: str, status: int) -> None:
    print(f'error: {message}', file=sys.stderr)
    sys.exit(status)


def read_pages(pdf: Path) -> list:
    try:
        from pypdf import PdfReader
    except ImportError:
        fail('pypdf is not installed: pip install pypdf cryptography', 2)
    try:
        return list(PdfReader(str(pdf)).pages)
    except Exception as e:  # pypdf raises its own types, and DependencyError without cryptography
        fail(f'cannot read {pdf}: {e}', 2)
    return []


def page_code(text: str) -> tuple[str, str, str] | None:
    """The page's own number, such as ('2', '1', 'C19') for Page 2-1-C19, read from its footer."""
    found = PAGE_RE.findall(text)
    return found[-1] if found else None


def furniture(line: str) -> bool:
    """A line every page carries - the title, the footer, the date - or a blank page's mark."""
    s = line.strip()
    return (not s or bool(TITLE_RE.search(s)) or bool(PAGE_RE.search(s)) or bool(DATE_RE.match(s))
            or s == 'Blank Page' or bool(PART_TITLE_RE.match(s)))


def table_rows(text: str) -> list[list[str] | None]:
    """A layout-mode dictionary page as its table rows: four cells each, split at the columns the
    page's header row places; None where a blank line or the page's end separates rows."""
    lines = text.split('\n')
    head = next((k for k, line in enumerate(lines) if 'STE EXAMPLE' in line and 'Non-STE' in line), None)
    if head is None:
        return []
    h = lines[head]
    starts = [0, h.find('ALTERNATIVES'), h.find('STE EXAMPLE'), h.find('Non-STE')]
    if min(starts[1:]) < 0:
        return []
    rows: list[list[str] | None] = []
    for line in lines[head + 1:]:
        if furniture(line):
            rows.append(None)
            continue
        cells = ['', '', '', '']
        for m in re.finditer(r'\S+(?: \S+)*', line):
            col = max(k for k in range(4) if m.start() >= starts[k] - 2)
            cells[col] = f'{cells[col]} {m.group(0)}'.strip()
        rows.append(cells)
    rows.append(None)
    return rows


def entries_of(rows: list[list[str] | None]) -> list[dict]:
    """The dictionary entries the rows hold, in order. A headword opens an entry in the first column
    - on one row, or on two or three when it runs onto the lines below - and every row after it
    belongs to that entry until the next headword, across pages."""
    entries: list[dict] = []
    cur: dict | None = None
    k = 0
    while k < len(rows):
        row = rows[k]
        k += 1
        if row is None:
            if cur is not None:
                cur['rows'].append(None)
            continue
        c1 = row[0]
        # A long headword broken with a hyphen at the end of its line: ELECTROMAG- / NETIC (adj)
        while (c1 and re.fullmatch(r'[A-Za-z]+-', c1) and k < len(rows) and rows[k] is not None
               and rows[k][0][:1].isalpha()):
            c1 = c1[:-1] + rows[k][0]
            row = [c1] + [f'{a} {b}'.strip() for a, b in zip(row[1:], rows[k][1:])]
            k += 1
        # A headword that runs onto the lines below: a parenthesis left open (process (in the /
        # process of ) (prep)), or a part of speech, with a phrase before it, on the next line
        # (CONTAMINATION / (n), chance / (by chance) (n)).
        joins = 0
        while (c1 and not HEADWORD_RE.match(c1) and joins < 2 and k < len(rows) and rows[k] is not None
               and rows[k][0] and (c1.count('(') > c1.count(')') or rows[k][0].startswith('('))):
            joined = f'{c1} {rows[k][0]}'
            if c1.count('(') <= c1.count(')') and not HEADWORD_RE.match(joined):
                break
            c1 = joined
            row = [c1] + [f'{a} {b}'.strip() for a, b in zip(row[1:], rows[k][1:])]
            k += 1
            joins += 1
        m = HEADWORD_RE.match(c1) if c1 else None
        if (m is None and c1 and PHRASE_RE.match(c1) and re.match(r'[A-Z]{2}', row[1]) and cur is not None
                and c1 != cur['word']):
            cur = {'word': c1, 'pos': '', 'approved': False, 'variants': [], 'phrase': '',
                   'col1': [''], 'rows': [['', *row[1:]]]}
            entries.append(cur)
            continue
        if m and (m['word'] == m['word'].upper() or m['word'] == m['word'].lower()):
            variants = [v.strip() for v in m['variants'].split(',') if v.strip()]
            phrase = (m['paren'] or '').strip()
            if phrase.startswith('or '):                  # MATT (or MATTE): another spelling
                variants.append(phrase[3:].strip())
                phrase = ''
            cur = {'word': m['word'], 'pos': m['pos'], 'approved': m['word'] == m['word'].upper(),
                   'variants': variants, 'phrase': phrase, 'col1': [m['rest'].strip()], 'rows': []}
            entries.append(cur)
            cur['rows'].append(['', *row[1:]])
        elif cur is not None:
            if c1:
                cur['col1'].append(c1)
            cur['rows'].append(['', *row[1:]])
    return entries


def runs(rows: list, col: int) -> list[tuple[int, list[str]]]:
    """The items of one column of an entry: each run of consecutive rows that hold text in that
    column, as its lines, with the row it starts on."""
    out: list[tuple[int, list[str]]] = []
    start, parts = None, []
    for k, row in enumerate(rows + [None]):
        cell = row[col] if row is not None else ''
        if cell:
            if start is None:
                start = k
            parts.append(cell)
        elif start is not None:
            out.append((start, parts))
            start, parts = None, []
    return out


def join_parts(parts: list[str], known: set[str]) -> str:
    """The lines of one cell as one text. A word the layout broke with a hyphen at the end of a line
    is joined again: without the hyphen when that makes a word of the dictionary, such as
    ELECTROMAGNETICALLY, and with it otherwise, such as DE-ENERGIZED."""
    text = ''
    for part in parts:
        head = re.search(r'[A-Za-z]+-$', text)
        tail = re.match(r'[A-Za-z]+', part)
        if head and tail:
            whole = (head.group(0)[:-1] + tail.group(0)).lower()
            text = text[:-1] + part if whole in known else text + part
        else:
            text = f'{text} {part}'.strip()
    return re.sub(r'\s+', ' ', text).strip()


def forms_of(entry: dict) -> list[str]:
    """An entry's other spellings and the forms its first column lists, each form whole, so that
    GOES OFF stays one form. A note such as "No other verb forms." is set aside first."""
    col1 = ' '.join(t for t in entry['col1'] if t)
    bare = col1
    for note in re.findall(r'[A-Z][a-z][^.]*(?:\.|$)', col1):
        bare = bare.replace(note, ' ')
    bare = re.sub(r'\(also\b|[()]', ' ', bare)
    size = len(entry['word'].split())             # GOES OFF is one form of GO OFF
    forms: list[str] = []
    for part in bare.split(',') if entry['approved'] else []:
        words = part.split()
        if not words or not all(re.fullmatch(r"[A-Z][A-Z'\-]*", w) for w in words):
            continue
        if len(words) % size or (size == 1 and len(words) > 1 and words[0] == entry['word']):
            # not a whole number of forms, or a phrase made with the headword (FOR EXAMPLE)
            forms.append(' '.join(words))
            continue
        # the PDF sometimes leaves out the comma between two forms: OCCURS OCCURRED
        forms += [' '.join(words[i:i + size]) for i in range(0, len(words), size)]
    return entry.get('variants', []) + forms


def known_words(entries: list[dict]) -> set[str]:
    """Every headword, spelling and form of the dictionary, in lower case."""
    known = {e['word'].lower() for e in entries}
    for e in entries:
        known.update(f.lower() for f in forms_of(e))
    return known


def dictionary_json(entries: list[dict], spec: dict) -> dict:
    known = known_words(entries)
    approved: dict[str, set[str]] = {}
    forms: dict[str, str] = {}
    unapproved: dict[str, dict[str, list[str]]] = {}
    for e in entries:
        # A phrase in parentheses is what the entry is about: long (as long as) is "as long as", and
        # so (that) is "so that".
        phrase = e.get('phrase', '').lower()
        word = e['word'].lower()
        if phrase:
            # long (no longer) holds its headword as LONGER; so (that) does not hold it at all
            word = phrase if any(w.startswith(word) for w in phrase.split()) else f'{word} {phrase}'
        if e['approved']:
            approved.setdefault(word, set()).add(e['pos'])
            for f in forms_of(e):
                forms.setdefault(f.lower(), word)
            continue
        alts = unapproved.setdefault(word, {}).setdefault(e['pos'] or 'phrase', [])
        for variant in e.get('variants', []):
            unapproved.setdefault(variant.lower(), {})[e['pos'] or 'phrase'] = alts
        # The second column of an unapproved word: each run of its rows is one replacement.
        for _, parts in runs(e['rows'], 1):
            text = join_parts(parts, known)
            found = [f'{a} ({p})' for a, p in ALT_RE.findall(text)]
            if not found and text and text == text.upper() and len(text) <= 40:
                found = [text]                     # a replacement with no part of speech: AT THIS TIME
            alts += [a for a in found if a not in alts]
    return {
        'spec': spec,
        'approved': {w: sorted(p) for w, p in sorted(approved.items())},
        'forms': dict(sorted(forms.items())),
        'unapproved': {w: e for w, e in sorted(unapproved.items())},
    }


def main() -> None:
    ap = argparse.ArgumentParser(description='Convert the ASD-STE100 dictionary into the STE dictionary JSON.')
    ap.add_argument('--pdf', type=Path, required=True)
    ap.add_argument('--json', type=Path, required=True, help='the STE dictionary JSON to write')
    a = ap.parse_args()
    if not a.pdf.is_file():
        fail(f'no such file: {a.pdf}', 2)
    rows: list[list[str] | None] = []
    issue = date = None
    for page in read_pages(a.pdf):
        text = page.extract_text() or ''
        code = page_code(text)
        if code is None:
            continue
        issue = issue or (re.search(r'Issue (\d+)', text) or [None, None])[1]
        date = date or (re.search(r'\d{4}-\d{2}-\d{2}', text) or [None])[0]
        if code[0] == '2' and code[1] == '1':     # a dictionary page: Page 2-1-*
            rows += table_rows(page.extract_text(extraction_mode='layout') or '')
    entries = entries_of(rows)
    if not entries:
        fail(f'{a.pdf} holds no dictionary page this script can read', 1)
    spec = {
        'title': 'ASD-STE100 Simplified Technical English',
        'issue': issue,
        'date': date,
        'file': a.pdf.name,
        'fingerprint': hashlib.sha256(a.pdf.read_bytes()).hexdigest()[:12],
        'built': datetime.date.today().isoformat(),
    }
    data = dictionary_json(entries, spec)
    a.json.parent.mkdir(parents=True, exist_ok=True)
    a.json.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    pairs = sum(len(p) for p in data['approved'].values())
    print(f'wrote {a.json}')
    print(f'spec: issue {issue}, {date}, {a.pdf.name}, fingerprint {spec["fingerprint"]}')
    print(f'entries: {len(entries)}; approved words: {len(data["approved"])} ({pairs} with their parts of speech), '
          f'forms: {len(data["forms"])}, unapproved words: {len(data["unapproved"])}')


if __name__ == '__main__':
    main()
