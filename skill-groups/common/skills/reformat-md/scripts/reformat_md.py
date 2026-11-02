"""Reformat a Markdown file to the MD style rules of md-style.md.

The rules live in {skillGroups.common}/rules/md-style.md, whose "Transforms applied by
reformat_md.py" lists what this script does, in order and by the same numbers:

  1. Strip Markdown hard-break trailing two-space sequences.
  2. Detect a raw Word/Docs/chat-export paste; a clean file skips 3-6, 8 and 9.
  3. Headers: strip surrounding `**...**`, unescape `\.` and `\-` in titles, shift
     heading levels down by 1 except the very first `#` line.
  4. Bullets: line-leading `*` -> `-`.
  5. Body: de-escape `\-`, `\_`, `\[`, `\]`, `\>`, `\*`, `\=`, `\+`, `\~`, and `\#`
     where a bare `#` is inert.
  6. Wrap preformatted blocks in fenced code blocks (Syntax, Example, YAML config,
     directory tree).
  7. Convert chat-export escaped LaTeX to Obsidian math. Runs in both modes, and
     skips a line that holds inline code.
  8. Inline-code a fixed list of identifiers, and those the document lists in a
     `{a, b}` set. Raw mode only.
  9. Strip NotebookLM/Gemini citation markers. Raw mode only, and never inside
     inline code or a table row.
 10. Put each sentence of prose on a line of its own. Runs in both modes.

Mechanical and idempotent: re-running on its own output is a no-op.

Usage:
    python3 reformat_md.py FILE [--twin TWIN] [--mode raw|clean]

--twin reformats the file's twin (or, given the twin, its English file) in the mode
FILE takes, so the two halves of a pair are never treated differently. --mode
overrides the raw-paste detection: a file written in the repo, not pasted, takes clean.
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path
from typing import List, Optional, Tuple

INLINE_TOKENS = [
    "child_process.spawn",
    "data/0-raw/", "data/1-sessions/", "data/2-turns_md/",
    "data/3-topics/", "data/4-exports/",
    "sync_config.yaml", "export_template.yaml",
    "parser.py", "topic_mgr.py", "render_md.py", "exporter.py",
    "pathlib", "jinja2",
    "0-raw/",
]


def _is_code_like(token: str) -> bool:
    """True if token looks like a programming identifier (camelCase, snake_case, etc.)."""
    if "_" in token:
        return True
    # camelCase: lowercase followed by uppercase
    if re.search(r"[a-z][A-Z]", token):
        return True
    # Contains digits mixed with letters (e.g. prompt2)
    if re.search(r"[a-zA-Z]\d", token):
        return True
    return False


def extract_dynamic_tokens(text: str) -> List[str]:
    """Extract field names from `x = {field1, field2, ...}` syntax patterns.

    All tokens from explicit data-structure definitions are code identifiers.
    Sorted longest-first so longer matches take priority.
    """
    tokens: set = set()
    for m in re.finditer(r"\{([^}]+)\}", text):
        fields = [f.strip() for f in m.group(1).split(",")]
        for f in fields:
            # Single identifier token (no spaces, alphabetic start)
            if f and " " not in f and re.match(r"[a-zA-Z]", f):
                tokens.add(f)
    return sorted(tokens, key=len, reverse=True)

BODY_ESCAPES = [
    (r"\\-", "-"),
    (r"\\_", "_"),
    (r"\\\[", "["),
    (r"\\\]", "]"),
    (r"\\>", ">"),
    (r"\\\*", "*"),
    (r"\\=", "="),
    (r"\\\+", "+"),
    (r"\\\\n", "\\n"),
    (r"\\\\\$", r"\\$"),
    (r"\\~", "~"),
]


def strip_hard_break(line: str) -> str:
    return re.sub(r"  +$", "", line)


HASH_ESCAPE_RE = re.compile(r"\\#")
TAG_CHAR_RE = re.compile(r"[\w\-/]", re.UNICODE)


def deescape_hash(line: str) -> str:
    """`\\#` -> `#`, but only where a bare `#` is inert.

    The export escapes these deliberately. Obsidian reads `#word` as a tag and a
    line-leading `#` as a heading, so `\u6a5f\u6703 \\#1` must keep its backslash - it
    renders the same either way, and unescaping it invents a tag.
    """
    def sub(m: re.Match) -> str:
        if not line[:m.start()].strip():
            return m.group(0)                      # would open the line: heading
        after = line[m.end():m.end() + 1]
        if after and TAG_CHAR_RE.match(after):
            return m.group(0)                      # `#1`, `#tag`: tag-shaped
        return "#"
    return HASH_ESCAPE_RE.sub(sub, line)


def deescape_body(line: str) -> str:
    for pat, lit in BODY_ESCAPES:
        line = re.sub(pat, lit, line)
    return deescape_hash(line)


def convert_bullet(line: str) -> str:
    return re.sub(r"^(\s*)\*(\s)", r"\1-\2", line)


def shift_header(line: str, *, is_title: bool) -> str:
    m = re.match(r"^(#+)\s+(.*)$", line)
    if not m:
        return line
    hashes, text = m.group(1), m.group(2).strip()
    text = re.sub(r"^\*\*(.*)\*\*$", r"\1", text).strip()
    text = re.sub(r"(\d)\\\.", r"\1.", text)
    text = text.replace(r"\-", "-").replace(r"\_", "_")
    new_level = len(hashes) if is_title else min(len(hashes) + 1, 6)
    return ("#" * new_level) + " " + text


def looks_like_yaml(line: str) -> bool:
    # `key: value` where key is identifier-like.
    return bool(re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*:\s*\S", line))


def looks_like_tree_start(line: str) -> bool:
    return bool(re.match(r"^[A-Za-z0-9_-]+/\s*$", line.strip()))


def looks_like_tree_continuation(line: str) -> bool:
    return bool(re.match(r"^[├└│]", line)) or bool(re.match(r"^[ \t]+[├└│]", line))


def is_already_fenced(out: List[str]) -> bool:
    """True if the most recent fence is open (odd count)."""
    n = sum(1 for l in out if l.startswith("```"))
    return n % 2 == 1


MATH_SPAN_RE = re.compile(r"\$\$|(?<!\\)\$[^$]+(?<!\\)\$")


def inline_code_tokens(line: str, extra_tokens: List[str] | None = None) -> str:
    if "`" in line:
        # Heuristic: leave lines with existing backticks alone (already partly coded).
        return line
    if MATH_SPAN_RE.search(line):
        # A `$`/`$$` span is LaTeX, not prose. Backticks inside it would break
        # the formula - and `\text{ROIC}` hands a token straight to
        # extract_dynamic_tokens, so this fires on the second pass without it.
        return line
    all_tokens = INLINE_TOKENS + (extra_tokens or [])
    for tok in all_tokens:
        # Word-boundary-ish: not preceded/followed by alphanum/underscore/dot/slash.
        pat = re.compile(
            r"(?<![A-Za-z0-9_./])" + re.escape(tok) + r"(?![A-Za-z0-9_./])"
        )
        line = pat.sub("`" + tok + "`", line)
    return line


# A NotebookLM/Gemini export tags each claim with the source document it came
# from: a bare `1`, a list `1, 2` / `3, 4`, or a range `2-4`. Once the note is
# detached from its sources those numbers point at nothing, so they are noise.
#
# What keeps real numbers safe is CITE_END: every pattern demands a clause
# ending right after the marker. `40%`, `\$5`, `第 141 頁` and a `1.` list
# marker never sit in that position. Two further guards:
#   - Two digits max. A bare `2024。` or `141。` is a year or a page number far
#     more often than a citation, and deleting one of those is the expensive
#     mistake.
#   - The ASCII-comma context refuses a thousands separator. It exists to catch
#     a marker stranded mid-line by a CSV-ish paste (`\$60 2,\$60`), but
#     `,(?!\d{3}(?!\d))` means `1,000` keeps its `1`.
#
# Pattern order matters: the paren-anchored one must run first, or the space
# before `2` in `費用）1, 2**。` lets the second pattern eat only ` 2` and
# strand `1,`.
CITE_LIST = r"\d{1,2}(?:\s*[-\u2013]\s*\d{1,2})?(?:,\s*\d{1,2}(?:\s*[-\u2013]\s*\d{1,2})?)*"
CITE_END = r"(?=[。，、：；！？]|,(?!\d{3}(?!\d))|\*\*|\s*\||$)"
CITE_CLOSER = "[）」』】》〉]"
CITE_PATTERNS = [
    # A line that is nothing but a citation - transform 7 strands one of these
    # when it splits `…\\ 6` into a display block plus its trailing prose.
    # First, or the whitespace pattern nibbles ` 2` off `1, 2` and leaves `1,`.
    re.compile(r"^\s*" + CITE_LIST + r"\s*$"),
    # `效果）1。` / `機會成本」1。` - butted straight against a closing bracket
    re.compile(r"(?<=" + CITE_CLOSER + r")" + CITE_LIST + CITE_END),
    # ` 1。` / ` 3, 4。` / ` 1 |` - whitespace before, clause end after
    re.compile(r"\s+" + CITE_LIST + CITE_END),
    # `**：2 這樣…` / `（EBIT / EV）3 更高的…` - opens the clause, does not close it
    re.compile(r"(?<=[：）」])" + CITE_LIST + r"\s+(?=[一-鿿])"),
]

_citations_removed = 0


CODE_SPAN_RE = re.compile(r"(`+).+?\1")


def strip_citations(line: str) -> str:
    """Drop citation markers, leaving amounts, percentages and page numbers.

    An inline-code span is copied through as it is: a number inside one is part
    of the code. Only ever deletes, and every pattern needs a marker to delete,
    so running this twice is a no-op.
    """
    out, last = [], 0
    for m in CODE_SPAN_RE.finditer(line):
        out.append(strip_citations_text(line[last:m.start()]))
        out.append(m.group(0))
        last = m.end()
    out.append(strip_citations_text(line[last:]))
    return "".join(out)


def strip_citations_text(text: str) -> str:
    global _citations_removed
    for pat in CITE_PATTERNS:
        text, n = pat.subn("", text)
        _citations_removed += n
    return text


def strip_citations_line(line: str) -> List[str]:
    """strip_citations, but a line that held nothing else drops out entirely.

    A table row is left whole: its numbers are cells - a row number, a count -
    and stand exactly where a citation would (` 1 |`).
    """
    if line.lstrip().startswith("|"):
        return [line]
    stripped = strip_citations(line)
    if line.strip() and not stripped.strip():
        return []
    return [stripped]


MATH_RUN_RE = re.compile(r"\\{4}")

_math_spans = 0


def convert_gemini_math(line: str) -> List[str]:
    """Convert Gemini/NotebookLM escaped LaTeX into Obsidian `$`/`$$` math.

    The export doubles every real LaTeX backslash (`\text` ships as `\\text`,
    `\%` as `\\%`) and single-escapes markdown punctuation (`\=`, `\+`, `\-`,
    `\)`, `\_`, `\~`). Math delimiters arrive as four-backslash runs: `\\\\(`
    and `\\\\)` around inline math, a bare `\\\\` on each side of display math.
    Backslash runs therefore decode as 4 = one delimiter, 2 = one LaTeX
    command, and longer runs as a sum of those (6 = 4+2, 8 = 4+4, 10 = 4+4+2).

    Returns the rewritten line, split so each `$$` block sits on its own line.
    A line with no four-backslash run is returned unchanged, which makes
    re-running a no-op; so is a line that holds inline code, which shows its
    text as it is - escaped LaTeX quoted as an example is not math to convert.
    """
    if not MATH_RUN_RE.search(line) or "`" in line:
        return [line]

    global _math_spans
    out: List[str] = []
    i, n = 0, len(line)
    in_math = False

    while i < n:
        if line[i] != "\\":
            out.append(line[i])
            i += 1
            continue

        j = i
        while j < n and line[j] == "\\":
            j += 1
        run = j - i
        i = j

        if run == 1:
            # Markdown punctuation escape: drop the backslash. Inside math a
            # `~` is a range dash in the source prose, not LaTeX's nbsp.
            if i < n:
                out.append("-" if (in_math and line[i] == "~") else line[i])
                i += 1
            continue

        delims, rem = divmod(run, 4)
        if rem not in (0, 2):
            out.append("\\" * run)
            continue

        for _ in range(delims):
            if i < n and line[i] in "()":
                out.append("$")
                i += 1
            else:
                out.append("$$")
            if in_math:          # closing delimiter completes one span
                _math_spans += 1
            in_math = not in_math
        if rem == 2:
            out.append("\\")

    text = "".join(out)
    if text.count("$$") % 2:
        # Unbalanced display delimiters: leave the line whole rather than
        # split it at a fence we cannot trust.
        return [text]
    return split_display_math(text)


def split_display_math(text: str) -> List[str]:
    """Put every `$$...$$` block on a line of its own."""
    if "$$" not in text:
        return [text]
    parts = text.split("$$")
    lines: List[str] = []
    for idx, part in enumerate(parts):
        if idx % 2:
            lines.append("$$" + part + "$$")
        elif part.strip():
            lines.append(part.strip() if lines else part.rstrip())
    return lines or [text]


def consume_block_until_blank(lines: List[str], i: int) -> Tuple[List[str], int]:
    block: List[str] = []
    while i < len(lines) and lines[i].strip():
        block.append(strip_hard_break(deescape_body(lines[i])))
        i += 1
    return block, i


def is_raw_paste(text: str) -> bool:
    """Heuristic: did this text come straight from a Word/Docs export?

    True if any of the unmistakable raw-paste artifacts are present:
        - bolded headers          `# **...**`
        - escaped numbered prefix `# 1\. Foo`
        - line-leading `*` bullets
        - escaped dashes in headers `### **Data \- topic**`
    """
    if re.search(r"^#+\s+\*\*", text, re.M):
        return True
    if re.search(r"^#+.*\\\.", text, re.M):
        return True
    if re.search(r"^\s*\*\s", text, re.M):
        return True
    if re.search(r"^#+.*\\-", text, re.M):
        return True
    return False


def next_nonblank(lines: List[str], start: int) -> int:
    j = start
    while j < len(lines) and not lines[j].strip():
        j += 1
    return j


# ---------------------------------------------------------------------------
# Transform 10: one sentence per line.
#
# md-style.md's rule: prose is written one sentence per line. A sentence ends at
# 。？！, or at . ? ! followed by a space and the start of the next sentence. A
# colon or a semicolon ends nothing, and neither does an end mark inside
# brackets or quotes, inside inline code or math, in an abbreviation or in an
# ellipsis. A straight quote " counts as a quote only when the text has the next
# one to close it, and so does a curly “ with its ”; a single quote is left alone,
# as it is also the mark of it's and users'. The next sentence starts with a
# capital, a CJK character, an opening mark, a symbol such as ⌘ or →, or a
# lowercase name with a hyphen in it, such as mermaid-view. A line that ends no sentence and is wide enough to have been wrapped
# runs on into the next, and is joined to it. Headings, table
# rows, fenced blocks, block quotes, HTML, display math, link definitions and the
# frontmatter are left as they are. Only line breaks and the spaces around them
# change, so re-running is a no-op.

CJK_END = "。？！"
ASCII_END = ".?!"
OPENERS = "(（[「『【《〈"
CLOSERS = ")）]」』】》〉"
# What may follow an end mark and still belong to its sentence: a closing quote
# or bracket - and a run of asterisks, but only one that closes an open bold or
# italic. In `…x。**Name**` the ** opens the next sentence's bold, and a break
# after it would leave it at the end of a line, where it cannot open.
TRAILERS = "」』）】》〉\"”’'"
SENTENCE_OPENERS = "`*_[{\"“‘'§(（「『"
ABBREVIATIONS = {
    "e.g", "i.e", "vs", "etc", "cf", "al", "approx", "incl", "resp", "viz",
    "fig", "figs", "no", "nos", "vol", "pp", "ca", "mr", "mrs", "ms", "dr",
    "st", "jr", "sr", "inc", "ltd", "co", "corp", "dept", "u.s", "a.m", "p.m",
}
# A line this wide (a CJK character counts two) that ends no sentence was
# wrapped, and runs on; a shorter one, such as `**Raised**: 2026-10-11`, is a
# break the writer meant.
RUN_ON_WIDTH = 60
# Quotes whose closing mark is found later in the same run of prose.
QUOTE_PAIRS = {'"': '"', "“": "”"}
# A lowercase name that can open a sentence: words of a name joined by hyphens.
LOWER_NAME_RE = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)+\b")

LIST_ITEM_RE = re.compile(r"^(\s*)([-*+]|\d{1,9}[.)])(\s+)(?=\S)")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}(\s|$)")
SETEXT_RE = re.compile(r"^\s{0,3}(=+|-+)\s*$")
RULE_RE = re.compile(r"^\s{0,3}([-*_])(\s*\1){2,}\s*$")
REFDEF_RE = re.compile(r"^\s{0,3}\[[^\]]+\]:\s")
WORD_BEFORE_RE = re.compile(r"([A-Za-z][A-Za-z.]*)$")

_lines_joined = 0
_sentences_split = 0


def is_wide(ch: str) -> bool:
    return unicodedata.east_asian_width(ch) in ("W", "F")


def display_width(text: str) -> int:
    return sum(2 if is_wide(c) else 1 for c in text)


def outside_code(text: str) -> str:
    """The text with its inline-code spans taken out."""
    out, i = [], 0
    while i < len(text):
        k = skip_span(text, i) if text[i] == "`" else i
        if k != i:
            i = k
            continue
        out.append(text[i])
        i += 1
    return "".join(out)


def is_prose(line: str) -> bool:
    """A line of a paragraph or a list item - the only lines transform 10 touches. A line
    with display math is not, but `$$` written in inline code is no math."""
    s = line.strip()
    if not s or "$$" in outside_code(s) or s.startswith(("|", ">", "<")):
        return False
    return not (HEADING_RE.match(line) or SETEXT_RE.match(line) or RULE_RE.match(line)
                or REFDEF_RE.match(line))


def is_setext_title(lines: List[str], i: int) -> bool:
    """A line underlined by `===` or `---` is a heading, not prose."""
    return i + 1 < len(lines) and bool(SETEXT_RE.match(lines[i + 1])) and bool(lines[i].strip())


def closes_fence(line: str, fence: str) -> bool:
    m = FENCE_RE.match(line)
    return (bool(m) and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence)
            and not line.strip()[len(m.group(1)):].strip())


def skip_span(text: str, i: int) -> int:
    """Past the inline-code or inline-math span that opens at i, or i itself."""
    n = len(text)
    if text[i] == "`":
        j = i
        while j < n and text[j] == "`":
            j += 1
        run, k = j - i, j
        while k < n:
            if text[k] != "`":
                k += 1
                continue
            m = k
            while m < n and text[m] == "`":
                m += 1
            if m - k == run:
                return m
            k = m
        return j                                  # never closed: literal backticks
    if text[i] == "$" and (i == 0 or text[i - 1] != "\\") and not text.startswith("$$", i):
        k = i + 1
        while True:
            k = text.find("$", k)
            if k == -1:
                return i + 1
            if text[k - 1] != "\\":
                return k + 1
            k += 1
    return i


def closing_quote(text: str, i: int, mark: str) -> Optional[int]:
    """Where the quote mark that closes a quote opened before i stands, or None."""
    n = len(text)
    while i < n:
        k = skip_span(text, i)
        if k != i:
            i = k
            continue
        if text[i] == mark:
            return i
        i += 1
    return None


def is_symbol(ch: str) -> bool:
    """A symbol outside ASCII, such as ⌘ or →, that can open a sentence."""
    return ord(ch) > 127 and unicodedata.category(ch) in ("So", "Sm")


def emphasis_after(run: int, bold: bool, italic: bool) -> Tuple[bool, bool]:
    """The bold and italic state after a run of asterisks: ** toggles bold, * italic, *** both."""
    if run >= 2:
        bold = not bold
    if run % 2:
        italic = not italic
    return bold, italic


def sentence_end(text: str, i: int, bold: bool, italic: bool) -> Optional[Tuple[int, bool, bool]]:
    """Where the sentence whose end mark stands at i ends - past its trailers - with
    the bold and italic state there, or None when the mark ends no sentence."""
    c, n = text[i], len(text)
    if c == ".":
        if text[i + 1:i + 2] == "." or text[i - 1:i] == ".":
            return None                                   # an ellipsis
        m = WORD_BEFORE_RE.search(text[:i])
        if m and m.group(1).lower() in ABBREVIATIONS:
            return None                                   # e.g. / vs. / etc.
    j = i + 1
    while j < n:
        if text[j] in TRAILERS:
            j += 1
            continue
        if text[j] == "*":
            k = j
            while k < n and text[k] == "*":
                k += 1
            run = k - j
            if not ((run >= 2 and bold) or (run == 1 and italic) or (run == 3 and bold and italic)):
                break                                     # it opens: the next sentence's
            bold, italic = emphasis_after(run, bold, italic)
            j = k
            continue
        break
    if c in CJK_END:
        return (j, bold, italic) if text[j:].strip() else None
    if j >= n or text[j] not in " \t":
        return None                                       # `2.1`, `SKILL.md`, `x.y`
    k = j
    while k < n and text[k] in " \t":
        k += 1
    if k < n and (text[k].isupper() or is_wide(text[k]) or text[k] in SENTENCE_OPENERS
                  or is_symbol(text[k]) or LOWER_NAME_RE.match(text, k)):
        return j, bold, italic
    return None


def split_sentences(text: str, bold: bool = False, italic: bool = False) -> Tuple[List[str], bool, bool]:
    """One run of prose, broken after each sentence that ends inside it, with the bold
    and italic state at its end. A bold may run over several lines of a paragraph, so
    the state a line starts in is the one the line before it ended in."""
    out, start, depth, i, n = [], 0, 0, 0, len(text)
    quote_end = -1                        # where the closing mark of an open quote stands
    while i < n:
        k = skip_span(text, i)
        if k != i:
            i = k
            continue
        c = text[i]
        if c == "*":
            k = i
            while k < n and text[k] == "*":
                k += 1
            bold, italic = emphasis_after(k - i, bold, italic)
            i = k
            continue
        if i <= quote_end:                # inside a quote, or its closing mark
            i += 1
            continue
        if c in QUOTE_PAIRS:
            close = closing_quote(text, i + 1, QUOTE_PAIRS[c])
            if close is not None:
                quote_end = close
                i += 1
                continue
        if c in OPENERS:
            depth += 1
        elif c in CLOSERS:
            depth = max(0, depth - 1)
        elif depth == 0 and (c in CJK_END or c in ASCII_END):
            found = sentence_end(text, i, bold, italic)
            if found is not None:
                end, bold, italic = found
                out.append(text[start:end].strip())
                while end < n and text[end] in " \t":
                    end += 1
                start = i = end
                continue
        i += 1
    if text[start:].strip():
        out.append(text[start:].strip())
    return out, bold, italic


def ends_sentence(text: str) -> bool:
    """Does the line end a sentence - or on a colon, a break the writer made?"""
    s = text.rstrip()
    while s and (s[-1] in TRAILERS or s[-1] in "*_)"):
        s = s[:-1]
    return bool(s) and s[-1] in CJK_END + ASCII_END + ":："


def runs_on(line: str) -> bool:
    """A line that ends no sentence and was wrapped, so it continues on the next."""
    s = line.rstrip()
    if s.endswith(("\\", "<br>", "<br/>", "<br />")):
        return False
    return not ends_sentence(s) and display_width(s) >= RUN_ON_WIDTH


def join_text(a: str, b: str) -> str:
    """Join two pieces of one sentence: no space between two CJK characters."""
    a, b = a.rstrip(), b.lstrip()
    return a + b if a and b and is_wide(a[-1]) and is_wide(b[0]) else a + " " + b


def sentence_lines(lines: List[str]) -> List[str]:
    """Transform 10: every sentence of prose on a line of its own."""
    global _lines_joined, _sentences_split
    out: List[str] = []
    n, i = len(lines), 0
    if n and lines[0].strip() == "---":
        end = next((k for k in range(1, n) if lines[k].strip() == "---"), None)
        if end is not None:
            out.extend(lines[:end + 1])
            i = end + 1
    fence, in_comment, in_math = "", False, False
    while i < n:
        line = lines[i]
        s = line.strip()
        if fence:
            out.append(line)
            if closes_fence(line, fence):
                fence = ""
            i += 1
            continue
        if in_comment or in_math:
            out.append(line)
            if in_comment and "-->" in s:
                in_comment = False
            elif in_math and s == "$$":
                in_math = False
            i += 1
            continue
        fm = FENCE_RE.match(line)
        if fm:
            fence = fm.group(1)
        elif s.startswith("<!--") and "-->" not in s:
            in_comment = True
        elif s == "$$":
            in_math = True
        if fm or in_comment or in_math or not is_prose(line) or is_setext_title(lines, i):
            out.append(line)
            i += 1
            continue
        item = LIST_ITEM_RE.match(line)
        head = line[:item.end()] if item else line[:len(line) - len(line.lstrip(" "))]
        indent = len(head)
        block, j = [line], i + 1
        while j < n:
            nxt = lines[j]
            if (not is_prose(nxt) or FENCE_RE.match(nxt) or LIST_ITEM_RE.match(nxt)
                    or is_setext_title(lines, j)):
                break
            ind = len(nxt) - len(nxt.lstrip(" "))
            if (item and not indent <= ind < indent + 4) or (not item and ind != indent):
                break
            block.append(nxt)
            j += 1
        logical: List[list] = []          # [text, the line it came from - None once joined]
        for k, phys in enumerate(block):
            text = phys[indent:].rstrip() if k == 0 else phys.strip()
            if logical and runs_on(block[k - 1]):
                logical[-1] = [join_text(logical[-1][0], text), None]
                _lines_joined += 1
            else:
                logical.append([text, phys])
        bold = italic = False
        for k, (text, phys) in enumerate(logical):
            sentences, bold, italic = split_sentences(text, bold, italic)
            if phys is not None and len(sentences) <= 1:
                out.append(phys)
                continue
            _sentences_split += max(0, len(sentences) - 1)
            out.append((head if k == 0 else " " * indent) + sentences[0])
            out.extend(" " * indent + s for s in sentences[1:])
        i = j
    return out


def finish(out: List[str]) -> str:
    """Transform 10 over the result, then a single trailing newline."""
    return "\n".join(sentence_lines(out)).rstrip() + "\n"


def reformat(text: str, raw: Optional[bool] = None) -> str:
    global _math_spans, _citations_removed, _lines_joined, _sentences_split
    _math_spans = _citations_removed = _lines_joined = _sentences_split = 0
    if raw is None:
        raw = is_raw_paste(text)
    raw_lines = text.splitlines()
    lines = [strip_hard_break(l) for l in raw_lines]
    dynamic_tokens = extract_dynamic_tokens(text)

    # Idempotent-only mode: a clean file keeps its structure, headers and fenced
    # code; only transform 7's math and transform 10's sentence lines apply.
    if not raw:
        out: List[str] = []
        fence = ""
        for line in lines:
            if fence:
                out.append(line)
                if closes_fence(line, fence):
                    fence = ""
                continue
            fm = FENCE_RE.match(line)
            if fm:
                fence = fm.group(1)
                out.append(line)
                continue
            if line.startswith("#"):
                out.append(line)
                continue
            out.extend(convert_gemini_math(line))
        return finish(out)

    out: List[str] = []
    i = 0
    title_emitted = False
    last_header_was_yaml_config = False

    while i < len(lines):
        line = lines[i]

        # Headers
        if line.startswith("#"):
            new_line = shift_header(line, is_title=not title_emitted)
            title_emitted = True
            last_header_was_yaml_config = bool(
                re.match(r"^#+ Config - .+\.yaml\b", new_line)
            )
            out.append(new_line)
            i += 1
            continue

        # Already-fenced lines, indented or not: pass through unchanged
        fm = FENCE_RE.match(line)
        if fm:
            out.append(line)
            i += 1
            while i < len(lines):
                out.append(lines[i])
                i += 1
                if closes_fence(lines[i - 1], fm.group(1)):
                    break
            continue

        # **Syntax** marker → fence the next non-blank block as plain code
        if line.strip() == "**Syntax**":
            out.append(line)
            i += 1
            j = next_nonblank(lines, i)
            if j < len(lines) and lines[j].startswith("```"):
                # Already fenced — let the main loop pass through.
                continue
            while i < len(lines) and not lines[i].strip():
                out.append(lines[i])
                i += 1
            block, i = consume_block_until_blank(lines, i)
            if block:
                out.append("```")
                out.extend(block)
                out.append("```")
            continue

        # **Example** marker → fence as ```json
        if line.strip() == "**Example**":
            out.append(line)
            i += 1
            j = next_nonblank(lines, i)
            if j < len(lines) and lines[j].startswith("```"):
                continue
            while i < len(lines) and not lines[i].strip():
                out.append(lines[i])
                i += 1
            block, i = consume_block_until_blank(lines, i)
            if block:
                out.append("```json")
                out.extend(block)
                out.append("```")
            continue

        # Directory tree: line is `data/` (or similar dir/) followed by `├──`/`└──`
        if (
            looks_like_tree_start(line)
            and i + 1 < len(lines)
            and looks_like_tree_continuation(lines[i + 1])
        ):
            block = [strip_hard_break(deescape_body(line))]
            i += 1
            while i < len(lines) and lines[i].strip() and looks_like_tree_continuation(lines[i]):
                block.append(strip_hard_break(deescape_body(lines[i])))
                i += 1
            out.append("```")
            out.extend(block)
            out.append("```")
            continue

        # YAML config block: contiguous `key: value` lines, only after a Config heading
        if last_header_was_yaml_config and looks_like_yaml(line):
            block = []
            while i < len(lines) and looks_like_yaml(lines[i]):
                block.append(strip_hard_break(deescape_body(lines[i])))
                i += 1
            out.append("```yaml")
            out.extend(block)
            out.append("```")
            last_header_was_yaml_config = False
            continue

        # Normal body line
        line = convert_bullet(line)
        math = convert_gemini_math(line)
        if math != [line]:
            # The math scanner already de-escaped the whole line.
            for m in math:
                out.extend(strip_citations_line(m))
            i += 1
            continue
        line = deescape_body(line)
        line = inline_code_tokens(line, dynamic_tokens)
        out.extend(strip_citations_line(line))
        i += 1

    return finish(out)


def process(path: Path, raw: Optional[bool]) -> bool:
    """Reformat one file in place, keeping its line endings, and print its metrics.
    Returns the mode it took: True for raw."""
    data = path.read_bytes()
    src = data.decode("utf-8")
    raw = is_raw_paste(src) if raw is None else raw
    new = reformat(src, raw)
    path.write_bytes((new.replace("\n", "\r\n") if b"\r\n" in data else new).encode("utf-8"))

    new_lines = new.splitlines()
    headers = sum(1 for l in new_lines if re.match(r"^##", l))
    bullets = sum(1 for l in new_lines if re.match(r"^\s*-\s", l))
    fences = sum(1 for l in new_lines if l.startswith("```")) // 2
    inline_orig = sum(len(re.findall(r"`[^`]+`", l)) for l in src.splitlines())
    inline_new = sum(len(re.findall(r"`[^`]+`", l)) for l in new_lines)

    print(f"reformatted {path}")
    print(f"mode: {'raw' if raw else 'clean'}")
    print(f"headers_normalized: {headers}")
    print(f"bullets_converted: {bullets}")
    print(f"code_fences_added: {fences}")
    print(f"inline_code_added: {inline_new - inline_orig}")
    # Count what transform 7 actually built. Scanning the output instead would
    # count pre-existing `$$` blocks and bare-dollar currency as conversions.
    print(f"math_blocks_converted: {_math_spans}")
    print(f"citations_removed: {_citations_removed}")
    print(f"lines_joined: {_lines_joined}")
    print(f"sentences_split: {_sentences_split}")
    return raw


def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser(description="Reformat a Markdown file, in place, to md-style.md.")
    ap.add_argument("file", help="the Markdown file to reformat")
    ap.add_argument("--twin", help="its twin, or the English file of a twin: reformatted in the same mode")
    ap.add_argument("--mode", choices=("raw", "clean"), help="take this mode instead of detecting one")
    args = ap.parse_args(argv[1:])
    paths = [Path(args.file)] + ([Path(args.twin)] if args.twin else [])
    for p in paths:
        if not p.exists():
            print(f"error: {p} not found", file=sys.stderr)
            return 1
    raw = process(paths[0], None if args.mode is None else args.mode == "raw")
    if args.twin:
        process(paths[1], raw)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
