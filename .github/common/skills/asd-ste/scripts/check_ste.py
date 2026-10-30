#!/usr/bin/env python3
"""Inventory a Markdown file for the asd-ste skill, or check its STE file against it.

With --src alone (Step 1), print what of the source file must reach the STE file unchanged - its
frontmatter keys, headings, fenced blocks, inline code, links, placeholders, tables and header
quote - and where its prose breaks the measurable STE rules, then a verdict: `rewritable`, or
`NOT-ENGLISH` when the prose is mostly CJK. Nothing is written but what --report and --findings ask for.

With --src and --ste (Step 3), check the STE file: [FAIL] for a kept span the STE file lost or
changed and for each measurable rule it breaks, [WARN] for each word the STE dictionary does not
approve and the header note does not list as a technical word, for each sentence that looks
passive, for each double negative (a rule of the project, below), for each Latin abbreviation
(GR-6), and for each "make sure" with no "that" after it (GR-1). Nothing is written but what
--report and --findings ask for.

With --ste alone, check a file already in STE - a draft that has replaced its source (Step 7), or
such a file after a later edit - with no source to compare: its head, the rules a program measures,
its words and the spelling of its kept spans, as the check above does them. A kept span that holds a
British spelling is a [FAIL] that this file itself has to correct.

An inventory also lists each word of a heading that the dictionary lists as unapproved and approves
in no part of speech, as a [TODO] to decide: the STE file copies a heading unchanged, so a heading
that uses such a word in that part of speech must change in the source file, while one that uses it
as a technical noun or verb stays. A British spelling in a kept span makes the verdict SOURCE-FIRST:
the source file has to change before a rewrite.

Words are counted as STE counts them (rules 8.4 to 8.7): a number, an identifier, an inline-code
span, a link, quoted text and text in parentheses each count as one word, and a hyphenated word
counts as one. Counting is the only thing parentheses change: every other check reads the words
inside them as it reads the rest of the sentence; only quoted text is left out. A sentence that starts with an approved verb - or whose main clause does, after a
condition such as "If ..., " - is an instruction, with a limit of 20 words (rule 5.1); every other
sentence is descriptive, with a limit of 25 (rule 6.3).

Either mode can also keep what it found, for the skill's YAML checkpoint: --report writes the
printed report to a file as well, and --findings writes every finding to a JSON file in full - every
list the report shortens, such as the unapproved words with all their lines, is whole there.

--custom names the project-approved words and rules, ste-custom.md: a Markdown table of the words
this project approves beyond the dictionary, with the columns Word, Part of speech, Forms, Meaning and
Why, and a table of the writing rules it adds, which this script does not read. Each word, in each
form its row gives, counts as approved, and an [INFO] line names each one the prose uses. In a check,
every STE file must declare ste-custom.md in its header quote - [[ste-custom]] - or the check fails,
also one whose prose uses none of the words: every STE file follows the rules. Of the rules, the
one against two negatives that give a positive meaning is checked here, with or without --custom: a
[WARN] for each negative word - not, no, never, none, nothing, without, cannot - that a word of the
same clause, within four words, negates again, a word that a negative prefix makes from an approved
word, such as "incorrectly" from "correctly".

A placeholder in the retired form, ___UPPER_SNAKE___, which Markdown shows in bold italics instead of
as written, is no kept span: an inventory gives it a [WARN], and a check a [FAIL] when either file
holds one. Both name the script that converts it to {UPPER_SNAKE}, common/scripts/placeholders.py.

--spelling names the US spelling list, us-spelling.json: British spellings, each with its American
spelling (STE rule 1.14). A word of the list, or its -s, -ed, -ing, -er or -ers form, capitalized or
not, is found in the prose and in every kept span. In the prose of an STE file it is a [WARN] that
gives the American spelling; in a kept span it is a [FAIL], since the STE file copies the span from
the source file, which has to change first. An inventory lists both as [TODO]. A word the header
note lists as a technical word is never reported, and neither is a quotation or a web address:
md-style.md keeps a quotation, a proper name and a name that other documents or code use as written.

Usage:
  python check_ste.py --src <file.md> --dict <ste-dictionary.json> [--custom <ste-custom.md>] [--spelling <us-spelling.json>] [--report <txt>] [--findings <json>]
  python check_ste.py --src <file.md> --ste <file-ste.md> --dict <ste-dictionary.json> [--custom <ste-custom.md>] [--spelling <us-spelling.json>] [--report <txt>] [--findings <json>]
  python check_ste.py --ste <file.md> --dict <ste-dictionary.json> [--custom <ste-custom.md>] [--spelling <us-spelling.json>] [--report <txt>] [--findings <json>]

Exit status: 0 the inventory is printed, or the STE file passes; 1 the STE file fails a check;
2 a file is missing or unreadable, or, in an inventory, the source is not English; 3 in an
inventory, the source has to change first (SOURCE-FIRST).
Standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

LDQ, RDQ, RSQ = chr(0x201C), chr(0x201D), chr(0x2019)
CJK_RE = re.compile('[%s-%s%s-%s]' % (chr(0x4E00), chr(0x9FFF), chr(0x3400), chr(0x4DBF)))
FENCE_RE = re.compile(r'^\s*(```|~~~)')
HEADING_RE = re.compile(r'^#{1,6}\s')
TABLE_RE = re.compile(r'^\s*\|')
LIST_RE = re.compile(r'^(\s*)(?:[-*+]|\d+[.)])\s+')
# The line a header quote may open with, as depends_on.py reads it: the document's own version.
VERSION_RE = re.compile(r'^>\s*Version:\s*\d{6}\s*$')
# One line of a header quote, as depends_on.py reads it: a link, then its record in inline code.
ENTRY_RE = re.compile(r'^>\s*(?:\[\[(?P<name>[^\]|#]+)(?:\|[^\]]*)?\]\]'
                      r'|\[[^\]]*\]\((?:<(?P<apath>[^>]+)>|(?P<path>[^)\s]+))\))'
                      r'(?P<rec>(?:\s+`[^`]*`)*)\s*$')
CODE_RE = re.compile(r'(`+)(.+?)\1')
LINK_RE = re.compile(r'!?\[([^\]]*)\]\((?:<([^>]+)>|([^)\s]+))(?:\s+"[^"]*")?\)')
WIKI_RE = re.compile(r'!?\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]')
AUTOLINK_RE = re.compile(r'<(https?://[^>]+)>')
PLACEHOLDER_RE = re.compile(r'\{[^{}\s]+\}')
# A placeholder in the retired form, ___UPPER_SNAKE___: matched wherever it stands, fenced or not.
OLD_PLACEHOLDER_RE = re.compile(r'___[A-Z0-9_]+___')
# The script that converts each placeholder in the retired form to {UPPER_SNAKE}.
PLACEHOLDERS_PY = Path(__file__).resolve().parents[3] / 'scripts' / 'placeholders.py'
MATH_RE = re.compile(r'\$[^$\n]+\$')
LABEL_RE = re.compile(r'^\*\*[^*]+\*\*\s*(?::|\s[-%s%s]\s)\s*' % (chr(0x2014), chr(0x2013)))
TECH_RE = re.compile(r'^>\s*Technical words\b[^:]*:\s*(?P<words>.*?)\.?\s*$', re.I)
CONTRACTION_RE = re.compile(r"\b\w+n['%s]t\b|\b(?:it|that|there|what|who|here|he|she|they|we|you|i|let)['%s](?:s|re|ve|ll|d|m)\b"
                            % (RSQ, RSQ), re.I)
PASSIVE_RE = re.compile(r'\b(?:is|are|was|were|be|been|being)\s+(?:not\s+|also\s+|only\s+|then\s+)?'
                        r'(\w+ed|made|done|given|shown|written|read|kept|set|put|found|held|known|seen|sent|built'
                        r'|run|left|told|taken|drawn|chosen|broken|split|cut|meant|thrown|begun|spoken|hidden)\b', re.I)
# A rule of the project (ste-custom.md): two negatives that give a positive meaning, as in "do not write a
# command incorrectly" - a negative word, then in the same clause, within four words, a word that a
# negative prefix makes from an approved word.
NEGATIVE_RE = re.compile(r"\b(?:not|no|never|none|nothing|without|cannot)\b", re.I)
NEGATIVE_PREFIXES = ('non', 'dis', 'un', 'in', 'im', 'il', 'ir')
# Words that open as a negative prefix does, and are no negative of the word after it.
NOT_NEGATIVES = {'unless', 'until', 'inside', 'input', 'inputs', 'inline', 'inform', 'informs', 'information',
                 'install', 'installs', 'installed', 'insert', 'inserts', 'inserted', 'inset', 'index', 'indexes',
                 'increase', 'increases', 'increased', 'income', 'intend', 'interest', 'invoke', 'invokes', 'impact',
                 'import', 'imports', 'important', 'improve', 'display', 'displays', 'displayed', 'discharge'}
ABBREVIATIONS = ('e.g.', 'i.e.', 'vs.', 'etc.', 'cf.', 'fig.', 'no.', 'approx.', 'min.', 'max.')
# GR-6: a Latin abbreviation, and the English words STE writes in its place.
LATIN_RE = re.compile(r'(?<![\w.])(?:e\.g|i\.e|etc|viz|cf|et al|vs)\.(?!\w)', re.I)
LATIN_ENGLISH = {'e.g.': 'for example', 'i.e.': 'that is', 'etc.': 'and so on', 'viz.': 'that is',
                 'cf.': 'refer to', 'et al.': 'and others', 'vs.': 'compared with'}
# GR-1: "make sure" with no "that" after it.
MAKE_SURE_RE = re.compile(r'\b(?:make|makes|made)\s+sure\b(?!\s+that\b)', re.I)
NUMBER_WORDS = set('zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen '
                   'sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety '
                   'hundred thousand million first second third fourth fifth sixth seventh eighth ninth tenth'.split())
# Words that end in -ing without being a verb's -ing form, and prefixes a hyphen joins to a word.
ING_WORDS = {'nothing', 'something', 'anything', 'everything', 'thing', 'things', 'string', 'strings', 'during',
             'bring', 'spring', 'ring', 'king', 'wing', 'ceiling', 'morning', 'evening', 'sling', 'swing'}
PREFIXES = {'re', 'pre', 'non', 'co', 'un', 'sub', 'multi', 'self', 'semi', 'anti', 'de', 'post', 'inter', 'over'}
CONDITION_WORDS = {'if', 'when', 'before', 'after', 'unless', 'while', 'until', 'where', 'for', 'in', 'on',
                   'at', 'during', 'to', 'with', 'without', 'as'}
INSTRUCTION_LIMIT, DESCRIPTION_LIMIT, PARAGRAPH_LIMIT = 20, 25, 6
NOT_ENGLISH_SHARE = 0.3
# The header row of the table of project-approved words, which --custom looks for.
CUSTOM_HEADER = ['word', 'part of speech', 'forms', 'meaning', 'why']
NO_FORMS = ('', '-', '—')
# The endings --spelling adds to each word of the US spelling list, and to its American spelling.
SPELLING_ENDINGS = ('s', 'ed', 'ing', 'er', 'ers')
URL_RE = re.compile(r'\bhttps?://\S+')


class Fault(Exception):
    """A file missing or unreadable: exit status 2."""


# --------------------------------------------------------------------------- reading a document

@dataclass
class Doc:
    path: Path
    lines: list[str]
    bom: bool
    frontmatter: tuple[int, int] | None = None          # first and last line index, both '---'
    fenced: set[int] = field(default_factory=set)       # indexes inside a fence, fences included
    fences: list[tuple[int, int]] = field(default_factory=list)
    headings: list[int] = field(default_factory=list)
    tables: list[list[int]] = field(default_factory=list)
    header_quote: list[int] = field(default_factory=list)
    header_note: list[int] = field(default_factory=list)


def read_doc(path: Path) -> Doc:
    try:
        data = path.read_bytes()
    except OSError as e:
        raise Fault(f'cannot read {path}: {e}')
    bom = data.startswith(b'\xef\xbb\xbf')
    try:
        text = data.decode('utf-8-sig')
    except UnicodeDecodeError as e:
        raise Fault(f'{path} is not UTF-8: {e}')
    doc = Doc(path, text.replace('\r\n', '\n').replace('\r', '\n').split('\n'), bom)
    lines = doc.lines
    start = 0
    if lines and lines[0].strip() == '---':
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == '---'), None)
        if end is not None:
            doc.frontmatter, start = (0, end), end + 1
    open_at = None
    for i in range(start, len(lines)):
        if FENCE_RE.match(lines[i]):
            if open_at is None:
                open_at = i
            else:
                doc.fences.append((open_at, i))
                doc.fenced.update(range(open_at, i + 1))
                open_at = None
    if open_at is not None:  # an unclosed fence runs to the end, as a renderer reads it
        doc.fences.append((open_at, len(lines) - 1))
        doc.fenced.update(range(open_at, len(lines)))
    table: list[int] = []
    for i in range(start, len(lines)):
        if i in doc.fenced:
            continue
        if HEADING_RE.match(lines[i]):
            doc.headings.append(i)
        if TABLE_RE.match(lines[i]):
            table.append(i)
        elif table:
            doc.tables.append(table)
            table = []
    if table:
        doc.tables.append(table)
    doc.header_quote = header_quote(lines, start)
    if doc.header_quote:
        j = doc.header_quote[-1] + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        while j < len(lines) and lines[j].startswith('>') and not ENTRY_RE.match(lines[j]):
            doc.header_note.append(j)
            j += 1
    return doc


def header_quote(lines: list[str], start: int) -> list[int]:
    """The header quote at the head of a document - the Version line it may open with, and the run
    of dependency lines after it - under at most two other lines, a title or a twin's pairing line,
    as depends_on.py finds it."""
    lead, i = 0, start
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if VERSION_RE.match(line) or ENTRY_RE.match(line):
            block = [i] if VERSION_RE.match(line) else []
            i += len(block)
            while i < len(lines) and ENTRY_RE.match(lines[i]):
                block.append(i)
                i += 1
            return block
        if lead >= 2 or FENCE_RE.match(line) or re.match(r'^#{2,}\s', line):
            return []
        lead += 1
        i += 1
    return []


def body_lines(doc: Doc) -> list[int]:
    """Indexes of the lines outside the frontmatter and the fenced blocks."""
    start = doc.frontmatter[1] + 1 if doc.frontmatter else 0
    return [i for i in range(start, len(doc.lines)) if i not in doc.fenced]


def frontmatter_blocks(doc: Doc) -> dict[str, str]:
    """Each top-level key of the frontmatter, with the raw text of its value."""
    if not doc.frontmatter:
        return {}
    out: dict[str, list[str]] = {}
    key = None
    for line in doc.lines[doc.frontmatter[0] + 1:doc.frontmatter[1]]:
        m = re.match(r'^([A-Za-z_][\w-]*):(.*)$', line)
        if m:
            key = m.group(1)
            out[key] = [m.group(2)]
        elif key is not None:
            out[key].append(line)
    return {k: '\n'.join(v) for k, v in out.items()}


# --------------------------------------------------------------------------- spans kept unchanged

def spans(doc: Doc) -> dict[str, list]:
    """The kept spans of a document outside its fenced blocks, each with its line number."""
    code, links, placeholders = [], [], []
    for i in body_lines(doc):
        line = doc.lines[i]
        for m in CODE_RE.finditer(line):
            code.append((m.group(0), i + 1))
        bare = CODE_RE.sub(' ', line)
        for m in LINK_RE.finditer(bare):
            links.append((m.group(2) or m.group(3), i + 1))
        for m in WIKI_RE.finditer(bare):
            links.append((f'[[{m.group(1).strip()}]]', i + 1))
        for m in AUTOLINK_RE.finditer(bare):
            links.append((m.group(1), i + 1))
        for m in PLACEHOLDER_RE.finditer(line):
            placeholders.append((m.group(0), i + 1))
    return {'code': code, 'links': links, 'placeholders': placeholders}


def old_placeholders(doc: Doc) -> list[tuple[str, int]]:
    """Each placeholder in the retired form, with its line number - in the frontmatter, a fenced block or the prose."""
    return [(m.group(0), i + 1) for i, line in enumerate(doc.lines) for m in OLD_PLACEHOLDER_RE.finditer(line)]


def convert_command(*docs: Doc) -> str:
    return f'python {PLACEHOLDERS_PY.as_posix()} convert ' + ' '.join(str(d.path) for d in docs)


def table_columns(doc: Doc, table: list[int]) -> list[int]:
    return [len(re.split(r'(?<!\\)\|', doc.lines[i].strip().strip('|'))) for i in table]


def read_custom(path: Path) -> dict:
    """The project-approved words: the words of the table, each approved in the parts of speech and with
    the forms its row gives - {'name', 'file', 'approved': {word: [pos]}, 'forms': {form: word}}."""
    doc = read_doc(path)
    for table in doc.tables:
        rows = [[c.strip() for c in re.split(r'(?<!\\)\|', doc.lines[i].strip().strip('|'))] for i in table]
        if [c.lower() for c in rows[0]] != CUSTOM_HEADER:
            continue
        approved: dict[str, list[str]] = {}
        forms: dict[str, str] = {}
        for i, row in zip(table[2:], rows[2:]):
            if len(row) != len(CUSTOM_HEADER) or not row[0]:
                raise Fault(f'{path}, line {i + 1}: a row of the table needs {len(CUSTOM_HEADER)} cells and a word')
            word = row[0].strip('`*').lower()
            approved[word] = [p.strip() for p in row[1].split(',') if p.strip()]
            for form in row[2].split(','):
                form = form.strip().strip('`*').lower()
                if form not in NO_FORMS:
                    forms[form] = word
        return {'name': path.stem, 'file': path.name, 'approved': approved, 'forms': forms}
    raise Fault(f'{path} has no table with the columns ' + ', '.join(c.capitalize() for c in CUSTOM_HEADER))


def ending(word: str, end: str) -> str:
    """The word with an ending, as English adds it: -es after s, x, z, ch and sh, -ies for a y after a
    consonant, and a final e dropped before -ed, -ing and -er."""
    if end == 's':
        if word.endswith(('s', 'x', 'z', 'ch', 'sh')):
            return word + 'es'
        if word.endswith('y') and len(word) > 1 and word[-2] not in 'aeiou':
            return word[:-1] + 'ies'
        return word + 's'
    if end == 'ers':
        return ending(word, 'er') + 's'
    if word.endswith('e'):
        return word[:-1] + end
    if word.endswith('y') and len(word) > 1 and word[-2] not in 'aeiou' and end != 'ing':
        return word[:-1] + 'i' + end
    return word + end


def read_spelling(path: Path) -> dict:
    """The US spelling list: {'file', 'forms': {British form: (American form, British word)}} - each
    word of the list, and each of its endings that the list does not name as American as well."""
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as e:
        raise Fault(f'cannot read the US spelling list {path}: {e}')
    words = data.get('words') if isinstance(data, dict) else None
    if not isinstance(words, dict) or not words:
        raise Fault(f'{path} has no "words" object of British spellings')
    pairs = {b.lower(): a.lower() for b, a in words.items()}
    forms = {b: (a, b) for b, a in pairs.items()}           # a word of the list wins over an ending
    for b, a in pairs.items():
        for end in SPELLING_ENDINGS:
            forms.setdefault(ending(b, end), (ending(a, end), b))
    for word in data.get('not_british', []):
        forms.pop(word.lower(), None)
    return {'file': path.name, 'forms': forms}


def cased(found: str, american: str) -> str:
    """The American spelling, written in the case the British one was found in."""
    if found.isupper() and len(found) > 1:
        return american.upper()
    return american[0].upper() + american[1:] if found[:1].isupper() else american


# --------------------------------------------------------------------------- prose and sentences

@dataclass
class Sentence:
    line: int          # 1-based
    text: str          # as written
    words: int
    instruction: bool


def mask(text: str) -> str:
    """The line with each kept span, link, quote and parenthesis reduced to one placeholder word, and
    emphasis markers removed - what STE counts as one word counts as one here."""
    text = CODE_RE.sub(' CODE ', text)
    text = LINK_RE.sub(' LINK ', text)
    text = WIKI_RE.sub(' LINK ', text)
    text = AUTOLINK_RE.sub(' LINK ', text)
    text = MATH_RE.sub(' MATH ', text)
    text = re.sub(r'\*\*|__', '', text)
    text = re.sub(r'(?<![\w*])[*_](\S[^*_]*?)[*_](?![\w*])', r'\1', text)
    return text


def unquote(text: str) -> str:
    """The text with each quotation reduced to one placeholder word: what a text quotes is exempt."""
    text = re.sub(r'"[^"]*"', ' QUOTE ', text)
    return re.sub(f'{LDQ}[^{RDQ}]*{RDQ}', ' QUOTE ', text)


def quotes_and_parens(text: str) -> str:
    text = unquote(text)
    prev = None
    while prev != text:
        prev, text = text, re.sub(r'\([^()]*\)', ' PAREN ', text)
    return text


def split_sentences(text: str) -> list[str]:
    """A line's sentences: each ends at . ? or ! followed by a space and the start of the next one,
    never inside quotes, brackets or an abbreviation."""
    out, start, depth, quoted = [], 0, 0, False
    i = 0
    while i < len(text):
        c = text[i]
        if c in '([':
            depth += 1
        elif c in ')]':
            depth = max(0, depth - 1)
        elif c == '"':
            quoted = not quoted
        elif c == LDQ:
            quoted = True
        elif c == RDQ:
            quoted = False
        elif c in '.?!' and depth == 0 and not quoted:
            j = i + 1
            while j < len(text) and text[j] in '*_"' + RDQ + ')':
                j += 1
            nxt = text[j + 1:j + 2] if j < len(text) and text[j] == ' ' else ''
            word = text[start:i + 1].split()[-1].lower() if text[start:i + 1].split() else ''
            if nxt and (nxt.isupper() or nxt.isdigit() or nxt in '"`*[(_' + LDQ) and not word.endswith(ABBREVIATIONS) \
                    and not (c == '.' and text[i - 2:i + 1] == '...'):
                out.append(text[start:j].strip())
                start = j
                i = j
                continue
        i += 1
    rest = text[start:].strip()
    if rest:
        out.append(rest)
    return out


def word_count(text: str) -> int:
    counted = quotes_and_parens(mask(LABEL_RE.sub('', text.strip())))
    return len(re.findall(r"[A-Za-z0-9][\w'%s\-./#]*" % RSQ, counted))


class Vocabulary:
    def __init__(self, data: dict, technical: set[str], custom: dict | None = None, spelling: dict | None = None):
        # A project-approved word is approved as the dictionary's words are.
        self.custom = custom or {'approved': {}, 'forms': {}}
        self.spelling = (spelling or {}).get('forms', {})
        self.approved = {**data.get('approved', {}), **self.custom['approved']}
        self.forms = {**data.get('forms', {}), **self.custom['forms']}
        self.unapproved = data.get('unapproved', {})
        self.verbs = {w for w, pos in self.approved.items() if 'v' in pos and ' ' not in w}
        self.phrases = sorted({w for w in [*self.approved, *self.forms] if ' ' in w}, key=len, reverse=True)
        self.bad_phrases = sorted((w for w in self.unapproved if ' ' in w), key=len, reverse=True)
        self.technical = {t.lower() for t in technical}

    def is_instruction(self, sentence: str) -> bool:
        words = re.findall(r"[A-Za-z][A-Za-z'\-]*", quotes_and_parens(mask(LABEL_RE.sub('', sentence.strip()))))
        if not words:
            return False
        first = words[0].lower()
        if first in self.verbs or first == 'do':
            return True
        if first in CONDITION_WORDS and ',' in sentence:
            after = re.findall(r"[A-Za-z][A-Za-z'\-]*", mask(sentence).split(',', 1)[1])
            return bool(after) and (after[0].lower() in self.verbs or after[0].lower() == 'do')
        return False

    def known(self, word: str) -> bool:
        w = word.lower()
        if w in self.approved or w in self.forms or w in NUMBER_WORDS or w in self.technical:
            return True
        for stem in (w[:-1] if w.endswith('s') else None, w[:-2] if w.endswith('es') else None,
                     w[:-3] + 'y' if w.endswith('ies') else None):
            if stem and ((stem in self.approved and 'n' in self.approved[stem]) or stem in self.technical):
                return True
        # the forms of a technical verb: parse, parses, parsed
        return any(stem in self.technical for stem in (w[:-1], w[:-2]) if w.endswith(('d', 'ed')) and stem)

    def british(self, word: str) -> str | None:
        """The word in lowercase when the US spelling list names it and the header note does not keep it."""
        w = word.lower()
        hit = self.spelling.get(w)
        if not hit or w in self.technical or hit[1] in self.technical:
            return None
        return w

    def customized(self, word: str) -> str | None:
        """The project-approved word that this word is, or is a form or a plural of."""
        w = word.lower()
        approved, forms = self.custom['approved'], self.custom['forms']
        if w in approved:
            return w
        if w in forms:
            return forms[w]
        for stem in (w[:-1] if w.endswith('s') else None, w[:-2] if w.endswith('es') else None,
                     w[:-3] + 'y' if w.endswith('ies') else None):
            if stem and 'n' in approved.get(stem, []):
                return stem
        return None

    def words(self, text: str) -> list[str]:
        """The words of a stretch of prose that the dictionary is asked about: kept spans, quoted
        text, identifiers, acronyms, names, technical words and approved phrases set aside."""
        text = unquote(mask(text))                   # the words in parentheses are checked too
        text = LATIN_RE.sub(' ', text)               # GR-6 reports these, not the dictionary
        text = re.sub(r'\b(?:CODE|LINK|MATH|QUOTE)\b', ' ', text)
        for phrase in [t for t in self.technical if ' ' in t] + self.phrases:
            text = re.sub(rf'\b{re.escape(phrase)}\b', ' ', text, flags=re.I)
        out = []
        for k, raw in enumerate(text.split()):
            token = raw.strip('.,;:!?()[]{}"\'*_<>' + LDQ + RDQ + RSQ)
            if not token or re.search(r'[./_#\d@=+\\]', token) or CJK_RE.search(token):
                continue
            token = re.sub(r"['%s]s?$" % RSQ, '', token)
            if not token:
                continue
            if token.isupper() and len(token) > 1:
                continue                      # an acronym
            if token[0].isupper() and k > 0:
                continue                      # a name, or a technical noun written as one
            out.extend(p for p in token.split('-') if p and p.isalpha() and p.lower() not in PREFIXES)
        return out


@dataclass
class Prose:
    sentences: list[Sentence]
    multi: list[tuple[int, int]]                 # (line, sentences on it)
    long_paragraphs: list[tuple[int, int]]       # (first line, sentences)
    semicolons: list[int]
    contractions: list[tuple[int, str]]
    passives: list[tuple[int, str]]
    unapproved: dict[str, list[int]]
    unknown: dict[str, list[int]]
    bad_phrases: dict[str, list[int]]
    used_technical: set[str]
    cjk: int
    latin: int
    latin_abbreviations: list[tuple[int, str]] = field(default_factory=list)   # GR-6
    no_that: list[int] = field(default_factory=list)                         # GR-1
    used_custom: dict[str, list[int]] = field(default_factory=lambda: defaultdict(list))  # --custom
    british: dict[str, list[int]] = field(default_factory=lambda: defaultdict(list))      # --spelling, rule 1.14
    double_negatives: list[tuple[int, str]] = field(default_factory=list)                 # a rule of ste-custom.md


def prose(doc: Doc, vocab: Vocabulary) -> Prose:
    skip = set(doc.headings) | set(doc.header_quote) | set(doc.header_note)
    for table in doc.tables:
        skip.update(table)
    result = Prose([], [], [], [], [], [], defaultdict(list), defaultdict(list), defaultdict(list), set(), 0, 0)
    paragraph: list[int] = []

    def close() -> None:
        count = sum(len(split_sentences(LABEL_RE.sub('', strip_marker(doc.lines[i])))) for i in paragraph)
        if count > PARAGRAPH_LIMIT:
            result.long_paragraphs.append((paragraph[0] + 1, count))
        paragraph.clear()

    for i in body_lines(doc):
        line = doc.lines[i]
        if i in skip or not line.strip() or re.match(r'^\s*(<|\$\$|-{3,}\s*$|\*{3,}\s*$)', line):
            if paragraph:
                close()
            continue
        if LIST_RE.match(line) and paragraph:
            close()
        paragraph.append(i)
        text = strip_marker(line)
        check_text(text, i + 1, vocab, result)
    if paragraph:
        close()
    for table in doc.tables:                     # table cells: words only, after the header row
        for i in table[2:]:
            for cell in re.split(r'(?<!\\)\|', doc.lines[i].strip().strip('|')):
                vocabulary(cell, i + 1, vocab, result)
        for i in table[:1] + table[2:]:          # spelling: the header row too, as prose
            british_words(doc.lines[i], i + 1, vocab, result)
    for text, line in description_lines(doc):    # the description is prose, rewritten as the rest is
        british_words(text, line, vocab, result)
    return result


def strip_marker(line: str) -> str:
    text = re.sub(r'^\s*>\s?', '', line)
    return LIST_RE.sub('', text, count=1).strip()


def check_text(text: str, line: int, vocab: Vocabulary, result: Prose) -> None:
    body = LABEL_RE.sub('', text)
    parts = split_sentences(body)
    if len(parts) > 1:
        result.multi.append((line, len(parts)))
    masked = mask(text)
    if ';' in unquote(masked).replace('&lt;', '').replace('&gt;', ''):
        result.semicolons.append(line)
    for m in CONTRACTION_RE.finditer(masked):
        result.contractions.append((line, m.group(0)))
    for m in PASSIVE_RE.finditer(unquote(masked)):
        result.passives.append((line, m.group(0)))
    for hit in double_negatives(unquote(masked), vocab):
        result.double_negatives.append((line, hit))
    unquoted = unquote(masked)
    for m in LATIN_RE.finditer(unquoted):
        result.latin_abbreviations.append((line, m.group(0)))
    if MAKE_SURE_RE.search(unquoted):
        result.no_that.append(line)
    for part in parts:
        result.sentences.append(Sentence(line, part, word_count(part), vocab.is_instruction(part)))
        vocabulary(part, line, vocab, result)
    british_words(text, line, vocab, result)
    plain = CODE_RE.sub(' ', text)
    result.cjk += len(CJK_RE.findall(plain))
    result.latin += len(re.findall(r'[A-Za-z]', plain))


def double_negatives(text: str, vocab: Vocabulary) -> list[str]:
    """Each negative word that a word of the same clause, within four words, negates again: a word that a
    negative prefix makes from an approved word, such as "incorrectly" from "correctly"."""
    found = []
    for m in NEGATIVE_RE.finditer(text):
        clause = re.split(r'[.,;:!?()]', text[m.end():], maxsplit=1)[0]
        for word in re.findall(r"[A-Za-z][A-Za-z\-]*", clause)[:4]:
            w = word.lower()
            if w in NOT_NEGATIVES:
                continue
            prefix = next((x for x in NEGATIVE_PREFIXES if w.startswith(x) and len(w) - len(x) >= 4), None)
            root = w[len(prefix):].lstrip('-') if prefix else ''
            if root and (root in vocab.approved or root in vocab.forms):
                found.append(f'{m.group(0)} ... {word}')
                break
    return found


def vocabulary(text: str, line: int, vocab: Vocabulary, result: Prose) -> None:
    lowered = unquote(mask(text)).lower()
    for phrase in vocab.bad_phrases:
        if re.search(rf'\b{re.escape(phrase)}\b', lowered):
            result.bad_phrases[phrase].append(line)
    for t in vocab.technical:
        if re.search(rf'\b{re.escape(t)}(?:s|es)?\b', lowered):
            result.used_technical.add(t)
    for word in vocab.words(text):
        w = word.lower()
        if w in vocab.spelling:
            continue                                 # british_words reports it, with its American spelling
        if vocab.known(w):
            base = vocab.customized(w)
            if base:
                result.used_custom[base].append(line)
            continue
        if w in vocab.unapproved:
            result.unapproved[w].append(line)
        else:
            result.unknown[w].append(line)


# --------------------------------------------------------------------------- spelling (rule 1.14)

def prose_text(text: str) -> str:
    """A stretch of prose without its kept spans, its quotations, its math and its web addresses -
    the words a writer chose; the text of a link stays, since only its target is kept."""
    text = CODE_RE.sub(' ', text)
    text = LINK_RE.sub(lambda m: f' {m.group(1)} ', text)
    text = WIKI_RE.sub(' ', text)
    text = AUTOLINK_RE.sub(' ', text)
    text = URL_RE.sub(' ', text)
    text = PLACEHOLDER_RE.sub(' ', text)
    text = MATH_RE.sub(' ', text)
    return unquote(text)


def british_words(text: str, line: int, vocab: Vocabulary, result: Prose) -> None:
    """Each British spelling the prose of a line uses, capitalized or not."""
    for word in re.findall(r'[A-Za-z]+', prose_text(text)):
        w = vocab.british(word)
        if w:
            result.british[w].append(line)


def description_lines(doc: Doc) -> list[tuple[str, int]]:
    """The frontmatter's description, line by line: the one value of the frontmatter that is prose."""
    out: list[tuple[str, int]] = []
    if not doc.frontmatter:
        return out
    inside = False
    for i in range(doc.frontmatter[0] + 1, doc.frontmatter[1]):
        m = re.match(r'^([A-Za-z_][\w-]*):(.*)$', doc.lines[i])
        if m:
            inside = m.group(1) == 'description'
            if inside:
                out.append((m.group(2), i + 1))
        elif inside:
            out.append((doc.lines[i], i + 1))
    return out


def kept_texts(doc: Doc) -> list[tuple[str, int, str]]:
    """The text of each kept span - (text, line, kind) - but for the description and web addresses."""
    out: list[tuple[str, int, str]] = []
    described = {line for _, line in description_lines(doc)}
    if doc.frontmatter:
        for i in range(doc.frontmatter[0] + 1, doc.frontmatter[1]):
            text = doc.lines[i]
            if i + 1 in described:
                text = text.split(':', 1)[0] if re.match(r'^description:', text) else ''
            out.append((text, i + 1, 'frontmatter'))
    for a, b in doc.fences:
        out.extend((doc.lines[i], i + 1, 'fenced block') for i in range(a, b + 1))
    out.extend((doc.lines[i], i + 1, 'heading') for i in doc.headings)
    s = spans(doc)
    out.extend((t, ln, 'inline code') for t, ln in s['code'])
    out.extend((t, ln, 'link target') for t, ln in s['links'])
    out.extend((t, ln, 'placeholder') for t, ln in s['placeholders'])
    return out


def kept_british(doc: Doc, vocab: Vocabulary) -> list[dict]:
    """Each British spelling a kept span holds, once for each line and kind: the STE file copies the
    span from the source file, so only a change to the source file can correct it."""
    hits: dict[tuple, dict] = {}
    for text, line, kind in kept_texts(doc):
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', URL_RE.sub(' ', text))   # colourMap is colour Map
        for word in re.findall(r'[A-Za-z]+', text):
            w = vocab.british(word)
            if w:
                hits.setdefault((w, line, kind), {'text': word, 'american': cased(word, vocab.spelling[w][0]),
                                                  'line': line, 'kind': kind})
    return sorted(hits.values(), key=lambda h: (h['line'], h['text']))


def kept_list(hits: list[dict], limit: int = 20) -> str:
    return ', '.join(f'{h["text"]} -> {h["american"]} (line {h["line"]}, {h["kind"]})' for h in hits[:limit]) \
        + (', ...' if len(hits) > limit else '')


def heading_words(doc: Doc, vocab: Vocabulary) -> list[dict]:
    """Each word of a heading that the dictionary lists as unapproved and approves in no part of speech,
    once for each line, with the parts of speech it is unapproved in. The STE file copies a heading
    unchanged, so a heading that uses such a word in that part of speech can only change in the source
    file; a word used as a technical noun or verb, such as file as a noun, is no fault, and only a reader
    can tell the two apart. Quoted text, inline code and link targets are left out."""
    hits: dict[tuple, dict] = {}
    for i in doc.headings:
        text = re.sub(r'\b(?:CODE|LINK|MATH|QUOTE)\b', ' ', prose_text(re.sub(r'^#{1,6}\s+', '', doc.lines[i])))
        for word in re.findall(r'[A-Za-z]+', text):
            w = word.lower()
            base = next((s for s in (w, w[:-1] if w.endswith('s') else None, w[:-2] if w.endswith('es') else None,
                                     w[:-3] + 'y' if w.endswith('ies') else None) if s and s in vocab.unapproved), None)
            if base and not vocab.known(w) and not vocab.british(word):
                entry = vocab.unapproved[base]
                hits.setdefault((base, i + 1), {
                    'text': word, 'word': base, 'line': i + 1, 'kind': 'heading', 'pos': list(entry),
                    'replacements': list(dict.fromkeys(a for pos in entry.values() for a in pos))})
    return sorted(hits.values(), key=lambda h: (h['line'], h['text']))


def heading_list(hits: list[dict], limit: int = 20) -> str:
    return ', '.join(f'{h["text"]} ({", ".join(h["pos"])}) -> {", ".join(h["replacements"]) or "no alternative"} '
                     f'(line {h["line"]})' for h in hits[:limit]) + (', ...' if len(hits) > limit else '')


# --------------------------------------------------------------------------- reporting

def lines_of(numbers: list[int], limit: int = 6) -> str:
    uniq = sorted(set(numbers))
    shown = ', '.join(map(str, uniq[:limit]))
    return f'line{"s" if len(uniq) > 1 else ""} {shown}{", ..." if len(uniq) > limit else ""}'


def alternatives(vocab: Vocabulary, word: str) -> str:
    entry = vocab.unapproved.get(word, {})
    alts = [a for pos in entry.values() for a in pos]
    use = ', '.join(dict.fromkeys(alts)) or 'no alternative in the dictionary'
    return f'{word} ({", ".join(entry)}) -> {use}'


def ste_findings(p: Prose, vocab: Vocabulary, mark_fail: str, mark_warn: str) -> int:
    """Print what the prose breaks; return how many [FAIL] lines were printed."""
    fails = 0

    def out(mark: str, text: str) -> None:
        nonlocal fails
        fails += mark == '[FAIL]'
        print(f'{mark} {text}')

    over = [s for s in p.sentences if s.words > (INSTRUCTION_LIMIT if s.instruction else DESCRIPTION_LIMIT)]
    if over:
        out(mark_fail, f'sentence length: {len(over)} sentence(s) over the limit '
                       f'({INSTRUCTION_LIMIT} words in an instruction, {DESCRIPTION_LIMIT} in a description)')
        for s in sorted(over, key=lambda s: -s.words)[:40]:
            kind = 'instruction' if s.instruction else 'description'
            print(f'    line {s.line}: {s.words} words ({kind}): {s.text[:110]}')
    else:
        print(f'[PASS] sentence length: all {len(p.sentences)} sentences within the limit')
    if p.multi:
        out(mark_fail, f'one sentence per line: {len(p.multi)} line(s) hold more than one - '
                       + ', '.join(f'{ln} ({n})' for ln, n in p.multi[:20]) + (' ...' if len(p.multi) > 20 else ''))
    else:
        print('[PASS] one sentence per line')
    if p.long_paragraphs:
        out(mark_fail, f'paragraph length: {len(p.long_paragraphs)} paragraph(s) over {PARAGRAPH_LIMIT} sentences - '
                       + ', '.join(f'line {ln} ({n})' for ln, n in p.long_paragraphs))
    else:
        print(f'[PASS] paragraph length: no paragraph over {PARAGRAPH_LIMIT} sentences')
    if p.semicolons:
        out(mark_fail, f'semicolons (rule 8.1): {lines_of(p.semicolons, 20)}')
    else:
        print('[PASS] no semicolon')
    if p.contractions:
        out(mark_fail, 'contractions (rule 4.2): ' + ', '.join(f'{c} (line {ln})' for ln, c in p.contractions[:20]))
    else:
        print('[PASS] no contraction')
    for phrase, where in sorted(p.bad_phrases.items()):
        out(mark_warn, f'unapproved phrase: {alternatives(vocab, phrase)} - {lines_of(where)}')
    for word, where in sorted(p.unapproved.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        out(mark_warn, f'unapproved word x{len(where)}: {alternatives(vocab, word)} - {lines_of(where)}')
    for word, where in sorted(p.unknown.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        why = ' (-ing form, rule 3.5)' if word.endswith('ing') and len(word) > 5 and word not in ING_WORDS else ''
        out(mark_warn, f'not in the dictionary x{len(where)}: {word}{why} - {lines_of(where)}')
    for word, where in sorted(p.british.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        out(mark_warn, f'British spelling (rule 1.14) x{len(where)}: {word} -> {vocab.spelling[word][0]} - {lines_of(where)}')
    if p.passives:
        out(mark_warn, f'passive voice? (rule 3.6) {len(p.passives)} - '
                       + ', '.join(f'"{t}" (line {ln})' for ln, t in p.passives[:25]))
    if p.double_negatives:
        out(mark_warn, f'double negative? (a rule of ste-custom.md) {len(p.double_negatives)} - '
                       + ', '.join(f'"{t}" (line {ln})' for ln, t in p.double_negatives[:25]))
    if p.latin_abbreviations:
        out(mark_warn, f'Latin abbreviations (GR-6) {len(p.latin_abbreviations)} - ' + ', '.join(
            f'{a} (line {ln}) -> {LATIN_ENGLISH.get(re.sub(r"[ ]+", " ", a.lower()), "English words")}'
            for ln, a in p.latin_abbreviations[:25]))
    if p.no_that:
        out(mark_warn, f'"make sure" without "that" (GR-1): {lines_of(p.no_that, 20)}')
    return fails


def cjk_share(p: Prose) -> float:
    return p.cjk / (p.cjk + p.latin) if p.cjk + p.latin else 0.0


def limit(s: Sentence) -> int:
    return INSTRUCTION_LIMIT if s.instruction else DESCRIPTION_LIMIT


def word_entry(vocab: Vocabulary, word: str, where: list[int]) -> dict:
    entry = vocab.unapproved.get(word, {})
    return {'word': word, 'count': len(where), 'pos': list(entry),
            'replacements': list(dict.fromkeys(a for pos in entry.values() for a in pos)),
            'lines': sorted(set(where))}


def findings_data(p: Prose, vocab: Vocabulary) -> dict:
    """Every finding of the prose, in full: what the printed report shortens, this keeps whole."""
    return {
        'sentences': len(p.sentences),
        'instructions': sum(1 for s in p.sentences if s.instruction),
        'sentences_over_limit': [
            {'line': s.line, 'words': s.words, 'kind': 'instruction' if s.instruction else 'description',
             'limit': limit(s), 'text': s.text} for s in p.sentences if s.words > limit(s)],
        'lines_with_more_than_one_sentence': [{'line': ln, 'sentences': n} for ln, n in p.multi],
        'paragraphs_over_six_sentences': [{'line': ln, 'sentences': n} for ln, n in p.long_paragraphs],
        'semicolons': sorted(set(p.semicolons)),
        'contractions': [{'line': ln, 'text': c} for ln, c in p.contractions],
        'unapproved_phrases': [word_entry(vocab, w, where) for w, where in sorted(p.bad_phrases.items())],
        'unapproved_words': [word_entry(vocab, w, where) for w, where in
                             sorted(p.unapproved.items(), key=lambda kv: (-len(kv[1]), kv[0]))],
        'words_not_in_dictionary': [
            {'word': w, 'count': len(where), 'lines': sorted(set(where)),
             'ing_form': w.endswith('ing') and len(w) > 5 and w not in ING_WORDS}
            for w, where in sorted(p.unknown.items(), key=lambda kv: (-len(kv[1]), kv[0]))],
        'passive_voice': [{'line': ln, 'text': t} for ln, t in p.passives],
        'double_negatives': [{'line': ln, 'text': t} for ln, t in p.double_negatives],
        'latin_abbreviations': [
            {'line': ln, 'text': a, 'english': LATIN_ENGLISH.get(re.sub(r'[ ]+', ' ', a.lower()), '')}
            for ln, a in p.latin_abbreviations],
        'make_sure_without_that': sorted(set(p.no_that)),
        'custom_words_used': [{'word': w, 'count': len(where), 'lines': sorted(set(where))}
                              for w, where in sorted(p.used_custom.items())],
        'british_spelling': [{'word': w, 'american': vocab.spelling[w][0], 'count': len(where),
                              'lines': sorted(set(where))}
                             for w, where in sorted(p.british.items(), key=lambda kv: (-len(kv[1]), kv[0]))],
        'cjk_share': round(cjk_share(p), 4),
    }


def custom_note(p: Prose, vocab: Vocabulary) -> str:
    """The [INFO] text naming each project-approved word the prose uses, or ''."""
    if not p.used_custom:
        return ''
    return (f'words approved by {vocab.custom.get("file", "the project-approved words")}, not by the dictionary: '
            + ', '.join(f'{w} ({lines_of(where)})' for w, where in sorted(p.used_custom.items())))


def measurable(p: Prose) -> list[dict]:
    """The pass or fail of each STE rule a program measures, as the report prints it."""
    over = [s for s in p.sentences if s.words > limit(s)]
    return [{'check': label, 'result': 'FAIL' if bad else 'PASS', 'detail': detail if bad else ''}
            for label, bad, detail in (
                ('sentence length', over, f'{len(over)} sentence(s) over the limit'),
                ('one sentence per line', p.multi, f'{len(p.multi)} line(s) hold more than one'),
                ('paragraph length', p.long_paragraphs, f'{len(p.long_paragraphs)} paragraph(s) over {PARAGRAPH_LIMIT} sentences'),
                ('no semicolon', p.semicolons, f'{len(set(p.semicolons))} line(s) with a semicolon'),
                ('no contraction', p.contractions, f'{len(p.contractions)} contraction(s)'))]


def inventory(src: Doc, vocab: Vocabulary, data: dict) -> int:
    print(f'== inventory: {src.path}')
    fm = frontmatter_blocks(src)
    print(f'frontmatter: {", ".join(fm) if fm else "none"}')
    print(f'headings ({len(src.headings)}):')
    for i in src.headings:
        print(f'    {i + 1}: {src.lines[i]}')
    print(f'fenced blocks ({len(src.fences)}): ' + ', '.join(f'lines {a + 1}-{b + 1}' for a, b in src.fences))
    s = spans(src)
    code = list(dict.fromkeys(c for c, _ in s['code']))
    print(f'inline code ({len(code)} distinct): ' + ' '.join(code))
    links = list(dict.fromkeys(t for t, _ in s['links']))
    print(f'link targets ({len(links)} distinct): ' + ', '.join(links))
    ph = list(dict.fromkeys(t for t, _ in s['placeholders']))
    print(f'placeholders ({len(ph)} distinct): ' + ' '.join(ph))
    old = old_placeholders(src)
    if old:
        print(f'[WARN] placeholders in the retired form ___X___ ({len(old)}): '
              + ', '.join(f'{t} (line {ln})' for t, ln in old[:20])
              + f' - convert them: {convert_command(src)}')
    print(f'tables ({len(src.tables)}): ' + ', '.join(
        f'line {t[0] + 1}, {max(table_columns(src, t))} columns' for t in src.tables))
    print(f'header quote ({len(src.header_quote)} lines):')
    for i in src.header_quote:
        print(f'    {i + 1}: {src.lines[i]}')
    p = prose(src, vocab)
    print(f'prose: {len(p.sentences)} sentences, '
          f'{sum(1 for x in p.sentences if x.instruction)} of them instructions')
    print('== STE findings in the source - what the rewrite must change')
    ste_findings(p, vocab, '[TODO]', '[TODO]')
    kept = kept_british(src, vocab) if vocab.spelling else []
    if kept:
        print(f'[TODO] change the source file first - {len(kept)} British spelling(s) in a kept span (rule 1.14), '
              f'which the STE file copies unchanged: {kept_list(kept)}')
    headed = heading_words(src, vocab)
    if headed:
        print(f'[TODO] decide - {len(headed)} word(s) in a heading that the dictionary does not approve in the part '
              f'of speech shown (rule 1.1): a heading that uses one so must change in the source file first, since '
              f'the STE file copies it unchanged; one used as a technical noun or verb stays: {heading_list(headed)}')
    if custom_note(p, vocab):
        print(f'[INFO] {custom_note(p, vocab)}')
    share = cjk_share(p)
    verdict = 'NOT-ENGLISH' if share > NOT_ENGLISH_SHARE else 'SOURCE-FIRST' if kept else 'rewritable'
    print(f'CJK share of the prose: {share:.1%} - verdict: {verdict}')
    data.update({
        'mode': 'inventory',
        'source': str(src.path),
        'frontmatter_keys': list(fm),
        'headings': [{'line': i + 1, 'text': src.lines[i]} for i in src.headings],
        'fenced_blocks': [{'from': a + 1, 'to': b + 1} for a, b in src.fences],
        'inline_code': code,
        'link_targets': links,
        'placeholders': ph,
        'old_placeholders': [{'text': t, 'line': ln} for t, ln in old],
        'tables': [{'line': t[0] + 1, 'columns': max(table_columns(src, t))} for t in src.tables],
        'header_quote': [{'line': i + 1, 'text': src.lines[i]} for i in src.header_quote],
        'findings': findings_data(p, vocab),
        'british_spelling_in_kept_spans': kept,
        'heading_words_to_decide': headed,
        'verdict': verdict,
    })
    return {'NOT-ENGLISH': 2, 'SOURCE-FIRST': 3}.get(verdict, 0)


def check(src: Doc | None, ste: Doc, vocab: Vocabulary, spec: dict, data: dict) -> int:
    """Check an STE file against its source; with no source, check a file already in STE - a draft
    that replaced its source - by its head and the rules a program measures, and compare nothing."""
    print(f'== check: {ste.path} against {src.path}' if src else f'== check: {ste.path}, a file already in STE')
    fails = 0
    checks: list[dict] = []
    notes: list[dict] = []

    def result(ok: bool, label: str, detail: str = '') -> None:
        nonlocal fails
        fails += not ok
        checks.append({'check': label, 'result': 'PASS' if ok else 'FAIL', 'detail': detail})
        print(f'{"[PASS]" if ok else "[FAIL]"} {label}{" - " + detail if detail else ""}')

    def note(level: str, text: str) -> None:
        notes.append({'level': level, 'text': text})
        print(f'[{level}] {text}')

    result(not ste.bom, 'encoding: UTF-8 without a byte-order mark')
    if src is not None:
        compare(src, ste, vocab, spec, result, note)
    else:
        old = old_placeholders(ste)
        result(not old, 'placeholders: none in the retired form ___X___',
               ', '.join(f'{t} (line {ln})' for t, ln in old[:20]) + f' - convert them: {convert_command(ste)}'
               if old else '')
    quote = [ste.lines[i] for i in ste.header_quote]
    spec_lines = [q for q in quote if (m := ENTRY_RE.match(q)) and (m['name'] or '').strip() == spec.get('file')]
    result(bool(spec_lines), f'header quote: declares [[{spec.get("file")}]]')
    for q in spec_lines:
        rec = re.findall(r'`([^`]*)`', ENTRY_RE.match(q)['rec'])
        if not rec:
            note('INFO', 'header quote: the STE specification line has no record yet - '
                         'depends_on.py record writes it once the check passes')
        elif rec[-1] != spec.get('fingerprint'):
            note('WARN', f'header quote: recorded fingerprint {rec[-1]} is not the one the dictionary was '
                         f'built from ({spec.get("fingerprint")}) - the STE file was checked against another PDF')
    # The line of ste-custom.md: in every STE file, which follows its rules though it may use none of its words.
    custom = vocab.custom.get('name')
    p = prose(ste, vocab)
    if custom:
        custom_lines = [q for q in quote if (m := ENTRY_RE.match(q)) and (m['name'] or '').strip() == custom]
        result(bool(custom_lines), f'header quote: declares [[{custom}]], the project-approved words and rules',
               '' if custom_lines else 'every STE file declares it, also one whose prose uses none of its words')
        if custom_lines and not re.findall(r'`([^`]*)`', ENTRY_RE.match(custom_lines[0])['rec']):
            note('INFO', f'header quote: the [[{custom}]] line has no record yet - '
                         'depends_on.py record writes it once the check passes')
    if src is not None:
        note_text = '\n'.join(ste.lines[i] for i in ste.header_note)
        result(src.path.name in note_text,
               f'header note: a block quote under the header quote that links to {src.path.name}')
    tech_line = next((ste.lines[i] for i in ste.header_note if TECH_RE.match(ste.lines[i])), None)
    if tech_line is None:
        note('WARN', 'header note: no "Technical words:" line - every word outside the dictionary is reported')
    fails += ste_findings(p, vocab, '[FAIL]', '[WARN]')
    checks.extend(measurable(p))
    kept = kept_british(ste, vocab) if vocab.spelling else []
    if vocab.spelling:
        fix = 'change the source file first, then the STE file and both TW twins' if src is not None \
            else 'change the kept span here, and in the TW twin'
        result(not kept, 'spelling: no kept span holds a British spelling (rule 1.14)',
               f'{kept_list(kept)} - {fix}' if kept else '')
    unused = sorted(vocab.technical - p.used_technical)
    if unused:
        note('WARN', f'technical words listed but never used: {", ".join(unused)}')
    approved = sorted(t for t in vocab.technical if t in vocab.approved or t in vocab.forms)
    if approved:
        note('INFO', f'technical words the dictionary approves anyway: {", ".join(approved)}')
    if custom_note(p, vocab):
        note('INFO', custom_note(p, vocab))
    share = cjk_share(p)
    if share > NOT_ENGLISH_SHARE:
        result(False, 'language', f'CJK share of the prose is {share:.1%}')
    verdict = 'FAIL' if fails else 'PASS'
    print(f'verdict: {verdict + " - " + str(fails) + " check(s) failed" if fails else verdict}')
    data.update({
        'mode': 'check' if src is not None else 'check alone',
        'source': str(src.path) if src is not None else None,
        'ste_file': str(ste.path),
        'checks': checks,
        'notes': notes,
        'technical_words': sorted(vocab.technical),
        'technical_words_unused': unused,
        'technical_words_approved_anyway': approved,
        'findings': findings_data(p, vocab),
        'british_spelling_in_kept_spans': kept,
        'failed': fails,
        'verdict': verdict,
    })
    return 1 if fails else 0


def compare(src: Doc, ste: Doc, vocab: Vocabulary, spec: dict, result, note) -> None:
    """The checks that set an STE file beside its source: what it must keep of the source, byte for byte.
    Each one goes through result(), which counts the failures."""
    fs, ft = frontmatter_blocks(src), frontmatter_blocks(ste)
    changed = [k for k in fs if k != 'description' and fs.get(k) != ft.get(k)]
    result(list(fs) == list(ft) and not changed, 'frontmatter: the same keys, and every value but the description',
           f'source {list(fs)}, STE file {list(ft)}, changed {changed}' if (list(fs) != list(ft) or changed) else '')
    hs, ht = [src.lines[i] for i in src.headings], [ste.lines[i] for i in ste.headings]
    first = next((k for k in range(max(len(hs), len(ht)))
                  if k >= len(hs) or k >= len(ht) or hs[k] != ht[k]), None)
    result(first is None, f'headings: {len(hs)} identical, in order',
           '' if first is None else f'first difference: source "{hs[first] if first < len(hs) else "-"}", '
                                    f'STE file "{ht[first] if first < len(ht) else "-"}"')
    bs = ['\n'.join(src.lines[a:b + 1]) for a, b in src.fences]
    bt = ['\n'.join(ste.lines[a:b + 1]) for a, b in ste.fences]
    bad = next((k for k in range(max(len(bs), len(bt))) if k >= len(bs) or k >= len(bt) or bs[k] != bt[k]), None)
    result(bad is None, f'fenced blocks: {len(bs)} identical, in order',
           '' if bad is None else f'block {bad + 1} differs (source line '
                                  f'{src.fences[bad][0] + 1 if bad < len(src.fences) else "-"}, STE line '
                                  f'{ste.fences[bad][0] + 1 if bad < len(ste.fences) else "-"})')
    ss, st = spans(src), spans(ste)
    for kind, label in (('code', 'inline code'), ('placeholders', 'placeholders')):
        have = {t for t, _ in st[kind]}
        lost = [(t, ln) for t, ln in dict((t, ln) for t, ln in reversed(ss[kind])).items() if t not in have]
        result(not lost, f'{label}: every one of the source\'s {len({t for t, _ in ss[kind]})} kept',
               ', '.join(f'{t} (source line {ln})' for t, ln in lost[:20]))
    old = [('source', t, ln) for t, ln in old_placeholders(src)] + [('STE file', t, ln) for t, ln in old_placeholders(ste)]
    result(not old, 'placeholders: none in the retired form ___X___',
           ', '.join(f'{t} ({side} line {ln})' for side, t, ln in old[:20]) + f' - convert them: {convert_command(src, ste)}'
           if old else '')
    have = {t for t, _ in st['links']}
    lost = [(t, ln) for t, ln in dict((t, ln) for t, ln in reversed(ss['links'])).items() if t not in have]
    result(not lost, f'link targets: every one of the source\'s {len({t for t, _ in ss["links"]})} kept',
           ', '.join(f'{t} (source line {ln})' for t, ln in lost[:20]))
    custom = vocab.custom.get('name')
    allowed = {src.path.name, f'[[{spec.get("file")}]]', f'[[{src.path.stem}]]'} | ({f'[[{custom}]]'} if custom else set())
    extra = sorted({t for t, _ in st['links']} - {t for t, _ in ss['links']} - allowed)
    if extra:
        note('WARN', f'link targets the source does not have: {", ".join(extra)}')
    cs = [max(table_columns(src, t)) for t in src.tables]
    ct = [max(table_columns(ste, t)) for t in ste.tables]
    result(cs == ct, f'tables: {len(cs)}, with the same column counts', '' if cs == ct else f'source {cs}, STE file {ct}')
    # The header quote: the source's own lines - its Version line among them - unchanged; the STE
    # specification's line follows them.
    own = [src.lines[i] for i in src.header_quote]
    quote = [ste.lines[i] for i in ste.header_quote]
    result(quote[:len(own)] == own, f'header quote: the source\'s {len(own)} line(s) kept unchanged')


class Tee:
    """Standard output written to the report file as well."""

    def __init__(self, *streams):
        self.streams = streams

    def write(self, text: str) -> None:
        for stream in self.streams:
            stream.write(text)

    def flush(self) -> None:
        for stream in self.streams:
            stream.flush()


def main() -> None:
    ap = argparse.ArgumentParser(description='Inventory a Markdown file for an STE rewrite, or check the rewrite.')
    ap.add_argument('--src', type=Path, help='the source file')
    ap.add_argument('--ste', type=Path, help='the STE file to check against the source, or alone')
    ap.add_argument('--dict', type=Path, required=True, help='the STE dictionary JSON')
    ap.add_argument('--custom', type=Path, help='the project-approved words: a Markdown table of the words '
                                                'this project approves beyond the dictionary')
    ap.add_argument('--spelling', type=Path, help='the US spelling list, us-spelling.json: British spellings, '
                                                  'each with its American spelling (rule 1.14)')
    ap.add_argument('--report', type=Path, help='also write the printed report to this file')
    ap.add_argument('--findings', type=Path, help='write every finding, in full, to this JSON file')
    a = ap.parse_args()
    if a.src is None and a.ste is None:
        ap.error('give --src, --ste, or both')
    report = None
    status = 2
    data: dict = {}
    try:
        if a.report:
            a.report.parent.mkdir(parents=True, exist_ok=True)
            report = a.report.open('w', encoding='utf-8')
            sys.stdout = Tee(sys.__stdout__, report)
        try:
            dictionary = json.loads(a.dict.read_text(encoding='utf-8'))
        except (OSError, ValueError) as e:
            raise Fault(f'cannot read the dictionary {a.dict}: {e}')
        custom = read_custom(a.custom) if a.custom else None
        spelling = read_spelling(a.spelling) if a.spelling else None
        src = read_doc(a.src) if a.src else None
        if a.ste is None:
            status = inventory(src, Vocabulary(dictionary, set(), custom, spelling), data)
        else:
            ste = read_doc(a.ste)
            tech_line = next((ste.lines[i] for i in ste.header_note if TECH_RE.match(ste.lines[i])), '')
            words = TECH_RE.match(tech_line)['words'] if tech_line else ''
            technical = {w.strip().strip('`*') for w in words.split(',') if w.strip()}
            status = check(src, ste, Vocabulary(dictionary, technical, custom, spelling),
                           dictionary.get('spec', {}), data)
        if a.findings:
            data['dictionary'] = dictionary.get('spec', {})
            data['customization'] = ({'file': str(a.custom), 'words': sorted(custom['approved'])}
                                     if custom else None)
            data['spelling_list'] = str(a.spelling) if spelling else None
            data['exit_status'] = status
            a.findings.parent.mkdir(parents=True, exist_ok=True)
            a.findings.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    except Fault as e:
        print(f'error: {e}', file=sys.stderr)
        status = 2
    finally:
        sys.stdout = sys.__stdout__
        if report is not None:
            report.close()
    sys.exit(status)


if __name__ == '__main__':
    main()
