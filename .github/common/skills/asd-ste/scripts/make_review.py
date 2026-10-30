#!/usr/bin/env python3
"""Build the review page of the asd-ste skill: an STE file beside its source file, for its reviewer.

The page sets the source file and the STE file side by side, each whole in a column that scrolls on
its own, with a switch that makes either column follow the other section by section; the two TW twins
the same way; and the STE file with its TW twin line by line. Each column's caption names the chapter,
and the section under it, of the topmost line it shows. Above them it lists what the YAML
checkpoint and the STE file say about the rewrite - the STE check's verdict and the warnings left,
the technical words, the statements kept in source wording - and then the review notes Step 6 wrote.
On a window wider than 900 pixels the page is two regions that scroll apart - the lists and the notes
above, the files below - with a divider to drag between them, so a link in the notes leaves the notes
where they were; a narrower window scrolls as one page.

A line reference in the notes - {{en-o:N}}, {{en-d:N}}, {{tw-o:N}} or {{tw-d:N}} - is line N of the
source file, the STE file, the source file's TW twin or the STE file's TW twin; N-M is a range and
N,M a list. Each becomes a link that opens its tab, scrolls to the line and marks it, and opens a
fenced block that holds it; its number carries a pointer toward its column, before it on the left
and after it on the right, joined to it by a no-break space so that a line never ends between the
two, and its tooltip names the tab, the column and the file. Every link clicked within one item -
the innermost list item that holds it - keeps its lines, and itself, marked, the last one darker, so
the places one item names can be compared; a link in another item clears them and starts again.
A line reference that names no line fails the run, and no page is written: a page whose links lead
nowhere would look finished.

Each item of the review notes, and each item under it, opens with a review status the reviewer sets
by clicking it, in this order: [ ] pending, [v] approved, [?] to be explained - the reviewer does
not follow how the item is handled, and the agent explains it in the conversation - and [x]
rejected. An item is known by a key made of its own text, the heading above it and its parent's key,
so a page built again keeps the status of every item that did not change, and an item that changed
is pending again. The page starts with the statuses of --status, step_6-status.json, as they were
when it was built; served by the review server, review_server.js, it reads the latest ones and saves
each click, and opened as a file it says that a click is not saved.

Usage:
  python make_review.py --src <name>.md --ste <name>-ste.md --src-tw <name>-tw.md
                        --ste-tw <name>-ste-tw.md --checkpoint <process.yaml>
                        --notes <step_6-notes.html> --out <step_6-review.html>
                        [--status <step_6-status.json>] [--title "<title>"]

Needs PyYAML. Exit status: 0 the page written; 1 a line reference names no line, and no page is
written; 2 a bad argument, or a file that cannot be read or parsed.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

FILES = {
    'en-o': 'source file',
    'en-d': 'STE file',
    'tw-o': "source file's TW twin",
    'tw-d': "STE file's TW twin",
}
REF_RE = re.compile(r'\{\{(.*?)\}\}')
REF_BODY_RE = re.compile(r'^((?:en|tw)-[od]):(\d+(?:-\d+)?(?:,\d+(?:-\d+)?)*)$')
TECH_RE = re.compile(r'^>\s*Technical words:\s*(.*?)\s*$')
CODE_RE = re.compile(r'(`+)(.+?)\1')
INLINE = [
    (re.compile(r'\*\*(.+?)\*\*'), lambda m: f'<strong>{m.group(1)}</strong>'),
    (re.compile(r'\[\[([^\]]+)\]\]'), lambda m: f'<span class="wl">[[{m.group(1)}]]</span>'),
    (re.compile(r'\[([^\]]+)\]\(([^)]+)\)'), lambda m: f'<span class="lk">{m.group(1)}</span>'),
]


def fail(message: str) -> None:
    print(f'error: {message}', file=sys.stderr)
    sys.exit(2)


def read_lines(path: Path) -> list[str]:
    """The file's lines, numbered as an editor numbers them: a final newline ends a line, not opens one."""
    try:
        text = path.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError) as e:
        fail(f'{path}: {e}')
    lines = text.lstrip('\ufeff').split('\n')
    if lines and lines[-1] == '':
        lines.pop()
    return [line.rstrip('\r') for line in lines]


def is_fence(line: str) -> bool:
    return line.lstrip().startswith('```')


def inline(text: str) -> str:
    """One line of Markdown as HTML: code spans as they are, bold, wiki links and links outside them."""
    out, pos = [], 0
    for m in CODE_RE.finditer(text):
        out.append(prose(text[pos:m.start()]))
        out.append(f'<code>{html.escape(m.group(2), quote=False)}</code>')
        pos = m.end()
    out.append(prose(text[pos:]))
    return ''.join(out)


def prose(text: str) -> str:
    text = html.escape(text, quote=False)
    for rx, fn in INLINE:
        text = rx.sub(fn, text)
    return text


def sections(lines: list[str]) -> list[tuple[str | None, list[tuple[int, str]]]]:
    """The file split at each `# ` heading outside a fenced block; lines above the first heading are a section of their own."""
    out: list[tuple[str | None, list[tuple[int, str]]]] = []
    fence = False
    for n, line in enumerate(lines, 1):
        if is_fence(line):
            fence = not fence
        elif not fence and line.startswith('# '):
            out.append((line[2:].strip(), []))
        if not out:
            out.append((None, []))
        out[-1][1].append((n, line))
    return out


def fenced_blocks(lines: list[str]) -> set[str]:
    out, buf = set(), None
    for line in lines:
        if buf is not None:
            buf.append(line)
            if is_fence(line):
                out.add('\n'.join(buf))
                buf = None
        elif is_fence(line):
            buf = [line]
    return out


def fence_html(buf: list[str], start: int, end: int, key: str, other: set[str], found: set[int]) -> str:
    text = '\n'.join(buf)
    same = '（與另一邊逐字相同）' if text in other else ''
    found.update(range(start, end + 1))
    return (f'<details class="fence" data-k="{key}" data-from="{start}" data-to="{end}">'
            f'<summary><span class="ln">{start}–{end}</span> 程式碼區塊 {same}</summary>'
            f'<pre>{html.escape(text)}</pre></details>')


def heading_attrs(text: str) -> str:
    """A heading's level and words as attributes: the page shows, at the top of each column, the
    chapter and the section under it that the column has reached."""
    level = len(text) - len(text.lstrip('#'))
    return f' data-level="{level}" data-title="{html.escape(text.lstrip("#").strip(), quote=True)}"'


def render(rows: list[tuple[int, str]], key: str, other: set[str], found: set[int]) -> str:
    """A section's lines, each with its number; a fenced block folded, opened by a line reference into it."""
    out, buf, start = [], None, 0
    for n, line in rows:
        if buf is not None:
            buf.append(line)
            if is_fence(line):
                out.append(fence_html(buf, start, n, key, other, found))
                buf = None
            continue
        if is_fence(line):
            buf, start = [line], n
            continue
        found.add(n)
        if not line.strip():
            out.append(f'<div class="blank" id="{key}-L{n}"></div>')
            continue
        indent = len(line) - len(line.lstrip(' '))
        text = line.strip()
        kind = 'tx'
        if line.startswith('#'):
            kind = 'h'
        elif text.startswith('>'):
            kind = 'q'
        elif re.match(r'[-*] ', text):
            kind = 'li'
        elif re.match(r'\d+\. ', text):
            kind = 'ol'
        elif text.startswith('|'):
            kind = 'tb'
        out.append(f'<div class="row {kind}" id="{key}-L{n}"{heading_attrs(text) if kind == "h" else ""} '
                   f'style="padding-left:{0.6 * indent:.1f}em">'
                   f'<span class="ln">{n}</span><span class="t">{inline(text)}</span></div>')
    if buf is not None:
        out.append(fence_html(buf, start, rows[-1][0], key, other, found))
    return '\n'.join(out)


def pane(left: list[str], right: list[str], lang: str, captions: tuple[str, str], found: dict) -> str:
    """Two files side by side, each whole in a column that scrolls on its own.
    Each section carries its number, the same on both sides since the STE check keeps the headings the
    same and in order, so that the page can scroll either column to the section the other shows."""
    def label(heading: str | None) -> str:
        return '（第一個標題之前）' if heading is None else heading

    def column(secs: list, key: str, other: set[str], caption: str) -> str:
        body = ''.join(f'<div class="sec" data-sec="{i}">{render(rows, key, other, found[key])}</div>'
                       for i, (_, rows) in enumerate(secs))
        return (f'<div class="col scroll" data-col="{key}"><div class="cap">{html.escape(caption)}'
                f'<span class="where"></span></div>{body}</div>')

    sa, sb = sections(left), sections(right)
    fa, fb = fenced_blocks(left), fenced_blocks(right)
    odd = [f'{label(sa[i][0] if i < len(sa) else "（缺這一節）")} ／ {label(sb[i][0] if i < len(sb) else "（缺這一節）")}'
           for i in range(max(len(sa), len(sb)))
           if i >= len(sa) or i >= len(sb) or sa[i][0] != sb[i][0]]
    warn = ('<p class="warn">兩邊的標題沒有逐節相同，同步捲動依順序對應各節：'
            + '、'.join(map(html.escape, odd)) + '</p>') if odd else ''
    return (f'{warn}<div class="cols">{column(sa, lang + "-o", fb, captions[0])}'
            f'{column(sb, lang + "-d", fa, captions[1])}</div>')


def pairing_block(en: list[str], tw: list[str], en_name: str) -> set[int]:
    """The twin's pairing lines, by index: under a frontmatter, the chinese skill adds a paragraph that
    links back to the English file, and a blank line after it, which the English file does not have."""
    if not (en and tw and en[0] == '---' and tw[0] == '---') or '---' not in tw[1:]:
        return set()
    i = tw.index('---', 1) + 1
    while i < len(tw) and not tw[i].strip():
        i += 1
    if i >= len(tw) or not re.search(r'\]\((?:[^)]*/)?' + re.escape(en_name) + r'\)', tw[i]):
        return set()
    block = set()
    while i < len(tw) and tw[i].strip():
        block.add(i)
        i += 1
    if i < len(tw):
        block.add(i)
    return block


def line_pane(en: list[str], tw: list[str], names: tuple[str, str]) -> str:
    """The STE file and its TW twin line by line, as the chinese skill writes the twin: one line for one line,
    but for the pairing lines it adds under a frontmatter, which are set aside."""
    skip = pairing_block(en, tw, names[0])
    tw_rows = [(j + 1, line) for j, line in enumerate(tw) if j not in skip]
    rows = []
    if skip:
        rows.append(f'<tr><td class="ln">{min(skip) + 1}–{max(skip) + 1}</td><td colspan="2" class="mut">'
                    f'中文版在 frontmatter 下多一段指回英文檔的說明，英文檔沒有，略過；下面的行號，斜線後是中文版的</td></tr>')
    if len(en) != len(tw_rows):
        rows.append(f'<tr><td class="ln"></td><td colspan="2" class="warn">兩份的行數不同：{len(en)} 行對 {len(tw_rows)} 行，'
                    f'下面的列不一定對得上</td></tr>')

    def number(i: int, m: int | None) -> str:
        return str(i) if m in (None, i) else f'{i}／{m}'

    fence, start = False, 0
    for k in range(max(len(en), len(tw_rows))):
        i = k + 1
        x = en[k] if k < len(en) else ''
        m, y = tw_rows[k] if k < len(tw_rows) else (None, '')
        if is_fence(x):
            if not fence:
                fence, start = True, i
                continue
            fence = False
            same = en[start - 1:i] == [line for _, line in tw_rows[start - 1:i]]
            first = tw_rows[start - 1][0] if start - 1 < len(tw_rows) else None
            span = f'{number(start, first)}–{number(i, m)}'
            if same:
                rows.append(f'<tr><td class="ln">{span}</td><td colspan="2" class="mut">程式碼區塊（兩邊逐字相同，略）</td></tr>')
            else:
                rows.append(f'<tr><td class="ln">{span}</td><td colspan="2" class="warn">程式碼區塊兩邊不同</td></tr>')
            continue
        if fence or (not x.strip() and not y.strip()):
            continue
        mark = heading_attrs(x.strip()) if x.startswith('#') else ''
        rows.append(f'<tr{mark}><td class="ln">{number(i, m)}</td><td>{inline(x.strip())}</td><td>{inline(y.strip())}</td></tr>')
    head = f'<tr><th></th><th>{html.escape(names[0])}</th><th>{html.escape(names[1])}</th></tr>'
    return (f'<div class="cap lp-cap">{html.escape(names[0])} ／ {html.escape(names[1])}<span class="where"></span></div>'
            f'<table class="lines">{head}{"".join(rows)}</table>')


def technical_words(ste: list[str]) -> list[str] | None:
    """The header note's `Technical words:` list, the one Step 3 left: Step 2's record of it may be older."""
    for line in ste:
        m = TECH_RE.match(line)
        if m:
            return [w.strip() for w in m.group(1).rstrip('.').split(',') if w.strip()]
    return None


def facts(step2: dict | None, step3: dict, ste: list[str]) -> str:
    """What the YAML checkpoint and the STE file say about the rewrite, as the review page lists it."""
    items = []
    runs = step3.get('check_runs')
    left = step3.get('warnings_left') or []
    verdict = html.escape(str(step3.get('verdict', '（沒有記錄）')))
    ran = f'，Step 3 跑了 {runs} 次' if runs else ''
    warn = ''.join(f'<li>{inline(str(w.get("warning", "")))} — {inline(str(w.get("why", "")))}</li>'
                   if isinstance(w, dict) else f'<li>{inline(str(w))}</li>' for w in left)
    items.append(f'<li><b>STE check</b>：{verdict}{ran}；留下的 warning {len(left)} 個'
                 + (f'<ul>{warn}</ul>' if warn else '') + '</li>')
    words = technical_words(ste)
    if words is None:
        items.append('<li><b>Technical words</b>：header note 沒有 <code>Technical words:</code> 這一行</li>')
    else:
        items.append(f'<li><b>Technical words</b>（{len(words)} 個）：' + '、'.join(html.escape(w) for w in words) + '</li>')
    if step2 is None:
        items.append('<li><b>保留原文措辭的陳述</b>：YAML checkpoint 沒有 <code>step_2</code> 群組，'
                     '這次執行沒有跑 Step 2，所以沒有列出</li>')
    else:
        kept = step2.get('kept_wording') or []
        rows = []
        for k in kept:
            if not isinstance(k, dict):
                rows.append(f'<li>{inline(str(k))}</li>')
                continue
            n = k.get('line')
            where = f'{{{{en-d:{n}}}}}：' if isinstance(n, int) and 1 <= n <= len(ste) else ''
            rows.append(f'<li>{where}{inline(str(k.get("text", "")))} — {inline(str(k.get("why", "")))}</li>')
        items.append(f'<li><b>保留原文措辭的陳述</b>（{len(kept)} 項）' + (f'<ul>{"".join(rows)}</ul>' if rows else '') + '</li>')
    return '<h3>腳本列出的項目</h3><ul>' + ''.join(items) + '</ul>'


def check_refs(text: str, found: dict, counts: dict) -> list[str]:
    """Every line reference in the text, unless it names a line the page shows."""
    problems = []
    for m in REF_RE.finditer(text):
        ref = '{{' + m.group(1) + '}}'
        body = REF_BODY_RE.match(m.group(1).strip())
        if not body:
            problems.append(f'{ref}: not a line reference - write {{{{en-o:N}}}}, {{{{en-d:N}}}}, {{{{tw-o:N}}}} '
                            f'or {{{{tw-d:N}}}}, with N-M for a range and N,M for a list')
            continue
        key = body.group(1)
        for item in body.group(2).split(','):
            a, _, b = item.partition('-')
            first, last = int(a), int(b or a)
            if last < first:
                problems.append(f'{ref}: the range {item} runs backwards')
                continue
            missing = [n for n in range(first, last + 1) if n not in found[key]]
            if missing:
                problems.append(f'{ref}: line {missing[0]} is not a line of the {FILES[key]}, '
                                f'which has {counts[key]} lines')
    return problems


def link_refs(text: str, names: dict) -> str:
    """Each line reference as a link: its number with an arrow toward its column, and a tooltip that
    names the tab, the column and the file, which the arrow cannot."""
    def one(key: str, item: str) -> str:
        a, _, b = item.partition('-')
        b = b or a
        label = a if a == b else f'{a}–{b}'
        left = key.endswith('-o')
        shown = f'◄\u00a0{label}' if left else f'{label}\u00a0►'
        tip = (f'{"English 頁籤" if key.startswith("en") else "中文頁籤"}・{"左欄" if left else "右欄"}・'
               f'{names[key]} 第 {label} 行')
        return (f'<a href="#{key}-L{a}" class="go" data-k="{key}" data-a="{a}" data-b="{b}" '
                f'title="{html.escape(tip)}">{shown}</a>')

    def sub(m: re.Match) -> str:
        body = REF_BODY_RE.match(m.group(1).strip())
        if not body:
            return m.group(0)
        key = body.group(1)
        return '第 ' + '、'.join(one(key, x) for x in body.group(2).split(',')) + ' 行'
    return REF_RE.sub(sub, text)


class _Items(HTMLParser):
    """The <li> items of the review notes in order: each one's own text, without its sub-items',
    the index of its parent item, and the <h3> heading above it."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.items: list[dict] = []
        self.stack: list[int] = []
        self.h3 = ''
        self.in_h3 = False

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag == 'li':
            self.items.append({'parent': self.stack[-1] if self.stack else None, 'h3': self.h3, 'text': []})
            self.stack.append(len(self.items) - 1)
        elif tag == 'h3':
            self.in_h3, self.h3 = True, ''

    def handle_endtag(self, tag: str) -> None:
        if tag == 'li' and self.stack:
            self.stack.pop()
        elif tag == 'h3':
            self.in_h3 = False

    def handle_data(self, data: str) -> None:
        if self.in_h3:
            self.h3 += data
        elif self.stack:
            self.items[self.stack[-1]]['text'].append(data)


LI_RE = re.compile(r'<li\b[^>]*>', re.IGNORECASE)


def item_keys(notes: str) -> list[str]:
    """One key for each <li> of the review notes, in order: its heading, its parent's key and its own
    text, so that a key stays while the item stays the same, and changes with it."""
    parser = _Items()
    parser.feed(notes)
    parser.close()
    keys: list[str] = []
    seen: dict[str, int] = {}
    for item in parser.items:
        parent = keys[item['parent']] if item['parent'] is not None else ''
        base = f"{' '.join(item['h3'].split())}|{parent}|{' '.join(''.join(item['text']).split())}"
        n = seen.get(base, 0)
        seen[base] = n + 1
        keys.append(hashlib.sha1(f'{base}|{n}'.encode('utf-8')).hexdigest()[:12])
    return keys


def add_status_boxes(notes: str, keys: list[str]) -> str:
    """A status box at the start of each <li>, the box the reviewer clicks."""
    it = iter(keys)

    def sub(m: re.Match) -> str:
        key = next(it, None)
        return m.group(0) if key is None else f'{m.group(0)}<button type="button" class="st" data-key="{key}">[ ]</button>'
    return LI_RE.sub(sub, notes)


def read_statuses(path: Path | None, keys: list[str]) -> dict:
    """The statuses --status holds for the items of this page; an item it does not know is pending."""
    if path is None or not path.is_file():
        return {}
    try:
        items = json.loads(path.read_text(encoding='utf-8')).get('items') or {}
    except (OSError, UnicodeDecodeError, ValueError, AttributeError) as e:
        print(f'[WARN] {path} cannot be read, so every item starts pending: {e}')
        return {}
    wanted = set(keys)
    return {k: v.get('s') for k, v in items.items()
            if k in wanted and isinstance(v, dict) and v.get('s') in ('v', 'x', '?')}


STYLE = '''
:root{--bg:#fbfbfa;--fg:#1f2328;--mut:#6b7280;--line:#e5e7eb;--card:#ffffff;--code:#f3f4f6;--acc:#2563eb;--warn:#b45309;--note:#fff7e6;--ok:#15803d;--no:#b91c1c}
@media (prefers-color-scheme: dark){:root{--bg:#16181d;--fg:#e6e8eb;--mut:#9aa1ab;--line:#2b2f36;--card:#1d2026;--code:#262a31;--acc:#6ea8ff;--warn:#f0b35a;--note:#2a2418;--ok:#4ade80;--no:#f87171}}
#review-notes ol{padding-left:4.6em} #review-notes ul{padding-left:3.6em} #review-notes li{position:relative}
#review-notes li>button.st{position:absolute;top:.2em;font:12px/1.4 ui-monospace,Menlo,monospace;padding:0 3px;border:1px solid var(--line);border-radius:4px;background:var(--card);color:var(--mut);cursor:pointer}
#review-notes ol>li>button.st{left:-4.4em} #review-notes ul>li>button.st{left:-3.4em}
#review-notes button.st[data-s="v"]{color:var(--ok);border-color:var(--ok)} #review-notes button.st[data-s="x"]{color:var(--no);border-color:var(--no)}
#review-notes button.st[data-s="?"]{color:var(--warn);border-color:var(--warn)}
.st-bar{display:flex;flex-wrap:wrap;gap:12px;align-items:baseline;font-size:13px;margin:0 0 6px} .st-bar b{font-weight:600}
*{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 -apple-system,"PingFang TC","Noto Sans TC",system-ui,sans-serif}
header{padding:20px 24px 8px} h1{margin:0 0 4px;font-size:22px} .sub{color:var(--mut)}
.notes{margin:12px 24px;padding:12px 16px;background:var(--note);border:1px solid var(--line);border-radius:10px}
.notes h3{margin:4px 0 8px;font-size:16px} .notes li{margin:4px 0}
.tabs{position:sticky;top:0;z-index:2;background:var(--bg);padding:8px 24px;border-bottom:1px solid var(--line)}
.tabs button{font:inherit;padding:6px 14px;margin-right:6px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--fg);cursor:pointer}
.tabs button.on{border-color:var(--acc);color:var(--acc)}
main{padding:8px 24px 40px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:14px} @media (max-width:900px){.cols{grid-template-columns:1fr}}
.col{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:0 12px 10px;min-width:0;position:relative}
.cap{position:sticky;top:0;z-index:1;background:var(--card);font-size:12px;color:var(--mut);padding:8px 0 6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.cap .where{color:var(--fg)} .lp-cap{background:var(--bg);padding:6px 0}
.sec+.sec{margin-top:10px}
.row{display:flex;gap:8px;align-items:baseline} .ln{color:var(--mut);font:12px/1.6 ui-monospace,Menlo,monospace;min-width:2.6em;text-align:right;flex:none}
.t{overflow-wrap:anywhere} .h .t{font-weight:700} .q .t{color:var(--mut);border-left:3px solid var(--line);padding-left:8px}
.blank{height:8px}
code{background:var(--code);padding:0 4px;border-radius:4px;font:13px ui-monospace,Menlo,monospace}
.wl,.lk{color:var(--acc)} .fence summary{cursor:pointer;color:var(--mut);font-size:13px} pre{background:var(--code);padding:8px;border-radius:8px;overflow:auto;font-size:12px}
.warn{color:var(--warn)} .hide{display:none !important}
a.go{color:var(--acc);text-decoration:underline;cursor:pointer} .hl{background:rgba(250,204,21,.38);border-radius:4px}
.hl-old{background:rgba(250,204,21,.15);border-radius:4px}
a.go.on{background:rgba(250,204,21,.38);border-radius:3px} a.go.was{background:rgba(250,204,21,.15);border-radius:3px}
.tabs{display:flex;align-items:center} .tabs .sync{margin-left:auto;margin-right:0}
.tabs .sync[aria-pressed="true"]{border-color:var(--acc);color:var(--acc)} .tabs button:disabled{opacity:.45;cursor:default}
@media (max-width:900px){.tabs .sync{display:none}}
.hint{color:var(--mut);font-size:13px;margin:0 0 6px} .mut{color:var(--mut)}
table.lines{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:10px;table-layout:fixed}
table.lines th,table.lines td{border-top:1px solid var(--line);padding:4px 8px;vertical-align:top;overflow-wrap:anywhere}
table.lines th{text-align:left;font-size:12px;color:var(--mut)} table.lines td.ln,table.lines th:first-child{width:4.2em}
#split{display:none}
@media (min-width:901px){
 html,body{height:100%}
 body{display:flex;flex-direction:column;overflow:hidden}
 #upper{flex:none;height:var(--upper,35vh);min-height:48px;overflow:auto}
 #split{display:block;flex:none;height:10px;cursor:row-resize;background:var(--line);position:relative;touch-action:none}
 #split::after{content:"";position:absolute;left:50%;top:3px;width:44px;height:4px;margin-left:-22px;border-radius:2px;background:var(--mut)}
 #split:focus-visible{outline:2px solid var(--acc);outline-offset:-2px}
 #lower{flex:1 1 auto;min-height:0;display:flex;flex-direction:column;overflow:hidden}
 #lower .tabs{flex:none}
 #lower main{flex:1 1 auto;min-height:0;overflow:hidden;padding:8px 24px 12px}
 #en,#tw{height:100%;display:flex;flex-direction:column}
 #lp{height:100%;overflow:auto}
 .cols{flex:1 1 auto;min-height:0;grid-template-rows:minmax(0,1fr)}
 .col.scroll{overflow:auto;min-height:0}
}
'''

SCRIPT = '''
function show(t){
 document.querySelectorAll('.tabs button[data-t]').forEach(x=>x.classList.toggle('on',x.dataset.t===t));
 ['en','tw','lp'].forEach(k=>document.getElementById(k).classList.toggle('hide',k!==t));
 document.querySelector('.tabs .sync').disabled=t==='lp';
}
// With the sync switch on, scrolling one column scrolls the other to the same place in the same section.
let syncOn=false, syncQuietUntil=0;
function follow(a,b){
 const secs=[...a.querySelectorAll(':scope > .sec')], top=a.scrollTop;
 let s=secs[0];
 for(const x of secs){ if(x.offsetTop<=top+1) s=x; else break; }
 if(!s) return;
 const f=Math.min(1,Math.max(0,(top-s.offsetTop)/Math.max(1,s.offsetHeight)));
 const t=b.querySelector(':scope > .sec[data-sec="'+s.dataset.sec+'"]');
 if(!t) return;
 const y=Math.round(t.offsetTop+f*t.offsetHeight);
 if(Math.abs(b.scrollTop-y)>=1){ b.dataset.follow='1'; b.scrollTop=y; }
}
document.querySelectorAll('.col.scroll').forEach(c=>c.addEventListener('scroll',()=>{
 if(c.dataset.follow){ delete c.dataset.follow; return; }
 if(!syncOn||Date.now()<syncQuietUntil) return;
 const other=[...c.parentElement.querySelectorAll(':scope > .col.scroll')].find(x=>x!==c);
 if(other) follow(c,other);
}));
document.querySelector('.tabs .sync').onclick=e=>{
 syncOn=!syncOn; e.currentTarget.setAttribute('aria-pressed',String(syncOn));
 const p=[...document.querySelectorAll('#en,#tw')].find(x=>!x.classList.contains('hide'));
 const cols=p?[...p.querySelectorAll('.col.scroll')]:[];
 if(syncOn&&cols.length===2) follow(cols[0],cols[1]);
};
document.querySelectorAll('.tabs button[data-t]').forEach(b=>b.onclick=()=>show(b.dataset.t));
// Every link clicked within one item keeps its lines marked, the last one dark and the rest light;
// a link in another item clears them. An item is the innermost list item that holds the link.
let item=null, clicked=[];
function itemOf(a){ return a.closest('li')||a.parentElement; }
function targets(a,open){
 const k=a.dataset.k, from=+a.dataset.a, to=+a.dataset.b, out=[];
 for(let n=from;n<=to;n++){
  let el=document.getElementById(k+'-L'+n);
  if(!el){
   el=[...document.querySelectorAll('details[data-k="'+k+'"]')].find(d=>+d.dataset.from<=n&&n<=+d.dataset.to);
   if(el&&open) el.open=true;
  }
  if(el&&!out.includes(el)) out.push(el);
 }
 return out;
}
function mark(){
 document.querySelectorAll('.hl,.hl-old').forEach(x=>x.classList.remove('hl','hl-old'));
 document.querySelectorAll('a.go.on,a.go.was').forEach(x=>x.classList.remove('on','was'));
 const last=clicked[clicked.length-1];
 clicked.forEach(a=>{ if(a===last) return; targets(a,false).forEach(el=>el.classList.add('hl-old')); a.classList.add('was'); });
 if(last){ targets(last,false).forEach(el=>{ el.classList.remove('hl-old'); el.classList.add('hl'); }); last.classList.add('on'); }
}
document.addEventListener('click',e=>{
 const a=e.target.closest('a.go'); if(!a) return; e.preventDefault();
 const it=itemOf(a);
 if(it!==item){ item=it; clicked=[]; }
 clicked=clicked.filter(x=>x!==a); clicked.push(a);
 show(a.dataset.k.slice(0,2));
 const first=targets(a,true)[0];
 mark();
 syncQuietUntil=Date.now()+1200;
 if(first) first.scrollIntoView({behavior:'smooth',block:'center'});
});
mark();
(function(){
 const split=document.getElementById('split'), upper=document.getElementById('upper');
 function setHeight(h){
  h=Math.max(48,Math.min(h,window.innerHeight-120));
  document.body.style.setProperty('--upper',h+'px');
 }
 split.addEventListener('pointerdown',e=>{
  e.preventDefault(); split.setPointerCapture(e.pointerId);
  const grab=e.clientY-upper.getBoundingClientRect().bottom;
  const move=ev=>setHeight(ev.clientY-grab-upper.getBoundingClientRect().top);
  const up=()=>{['pointermove','pointerup','pointercancel'].forEach((n,i)=>split.removeEventListener(n,i?up:move));};
  split.addEventListener('pointermove',move); split.addEventListener('pointerup',up); split.addEventListener('pointercancel',up);
 });
 split.addEventListener('keydown',e=>{
  if(e.key!=='ArrowUp'&&e.key!=='ArrowDown') return;
  e.preventDefault(); setHeight(upper.getBoundingClientRect().height+(e.key==='ArrowUp'?-24:24));
 });
})();
// Where each column is: the chapter, and the section under it, of the topmost line the column shows.
(function(){
 const views=[...document.querySelectorAll('.col.scroll'), document.getElementById('lp')];
 function where(view){
  const cap=view.querySelector('.cap'), out=cap&&cap.querySelector('.where'); if(!out) return;
  const edge=cap.getBoundingClientRect().bottom+2;
  let h1='', h2='';
  for(const h of view.querySelectorAll('[data-level]')){
   if(h.getBoundingClientRect().top>edge) break;
   const lv=+h.dataset.level;
   if(lv===1){ h1=h.dataset.title; h2=''; } else if(lv===2&&h1){ h2=h.dataset.title; }
  }
  out.textContent=h1?' › '+h1+(h2?' › '+h2:''):'';
  cap.title=cap.textContent;
 }
 let queued=false;
 function all(){ if(queued) return; queued=true; requestAnimationFrame(()=>{ queued=false; views.forEach(v=>{ if(v&&v.offsetParent!==null) where(v); }); }); }
 views.forEach(v=>v&&v.addEventListener('scroll',all,{passive:true}));
 window.addEventListener('scroll',all,{passive:true}); window.addEventListener('resize',all);
 document.querySelectorAll('.tabs button[data-t]').forEach(b=>b.addEventListener('click',all));
 document.addEventListener('click',e=>{ if(e.target.closest('a.go')) setTimeout(all,700); });
 all();
})();
// Review statuses, in the order a click moves through them: [ ] pending, [v] approved, [?] to be explained, [x] rejected. Served by the review server, the page saves each click.
(function(){
 const LABEL={'':'[ ]',v:'[v]',x:'[x]','?':'[?]'}, NAME={'':'待審',v:'審核通過',x:'不通過','?':'待解釋'}, NEXT={'':'v',v:'?','?':'x',x:''};
 const boxes=[...document.querySelectorAll('#review-notes button.st')];
 const count=document.getElementById('st-count'), flag=document.getElementById('st-flag'), note=document.getElementById('st-note');
 let state={}, served=false;
 try{ state=JSON.parse(document.getElementById('status-data').textContent)||{}; }catch(e){ state={}; }
 function own(b){ const li=b.closest('li'); if(!li) return ''; const c=li.cloneNode(true); c.querySelectorAll('ul,ol,button.st').forEach(x=>x.remove()); return c.textContent.replace(/\s+/g,' ').trim().slice(0,120); }
 function paint(){
  const n={'':0,v:0,x:0,'?':0};
  boxes.forEach(b=>{ const s=state[b.dataset.key]||''; b.textContent=LABEL[s]; b.dataset.s=s; b.title=NAME[s]+'（點一下切換）'; n[s]++; });
  count.innerHTML='審核狀態：<b>通過 '+n.v+'</b>、<b>待解釋 '+n['?']+'</b>、<b>不通過 '+n.x+'</b>、待審 '+n['']+'（共 '+boxes.length+' 項）';
 }
 async function save(){
  if(!served) return;
  const items={};
  boxes.forEach(b=>{ const s=state[b.dataset.key]||''; if(s) items[b.dataset.key]={s, text:own(b)}; });
  try{
   const r=await fetch('status',{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({items})});
   const j=await r.json().catch(()=>({}));
   flag.textContent=r.ok?'已儲存 '+(j.updated||''):'儲存失敗：'+(j.error||r.status);
  }catch(e){ flag.textContent='儲存失敗：審核伺服器沒有回應'; }
 }
 boxes.forEach(b=>b.addEventListener('click',()=>{ const k=b.dataset.key; state[k]=NEXT[state[k]||'']; if(!state[k]) delete state[k]; paint(); save(); }));
 async function load(){
  if(!/^https?:$/.test(location.protocol)) throw new Error('file');
  const r=await fetch('status',{cache:'no-store'}); if(!r.ok) throw new Error('status');
  const j=await r.json(); state={};
  Object.entries(j.items||{}).forEach(([k,v])=>{ if(v&&(v.s==='v'||v.s==='x'||v.s==='?')) state[k]=v.s; });
  served=true; paint();
  const h=await fetch('/healthz',{cache:'no-store'}).then(x=>x.json()).catch(()=>null);
  note.textContent='點方框切換：[ ] 待審 → [v] 審核通過 → [?] 待解釋 → [x] 不通過，每一次都會存進這份草稿 Checkpoint Dir 的 step_6-status.json；標 [?] 的項目，請在對話裡要我解釋；同意某一項的建議、要照它改，請標 [x]；[v] 表示草稿這一處照現狀通過。'
   +(h&&h.pid?'審核伺服器的 PID 是 '+h.pid+'：要關掉它，macOS／Linux 執行 kill '+h.pid+'，PowerShell 執行 Stop-Process -Id '+h.pid+'。':'');
 }
 paint();
 load().catch(()=>{ note.textContent='這份頁面不是從審核伺服器開啟的：方框可以切換，但不會儲存，顯示的是建頁時的狀態；要儲存，請用 Step 6 給的 http://127.0.0.1 連結開啟。同意某一項的建議、要照它改，請標 [x]；[v] 表示草稿這一處照現狀通過。'; });
})();
'''


def main() -> int:
    ap = argparse.ArgumentParser(description='Build the review page of an STE file.')
    ap.add_argument('--src', type=Path, required=True, help='the source file')
    ap.add_argument('--ste', type=Path, required=True, help='the STE file')
    ap.add_argument('--src-tw', type=Path, required=True, help="the source file's TW twin")
    ap.add_argument('--ste-tw', type=Path, required=True, help="the STE file's TW twin")
    ap.add_argument('--checkpoint', type=Path, required=True, help='the YAML checkpoint, process.yaml')
    ap.add_argument('--notes', type=Path, required=True, help='the review notes, step_6-notes.html')
    ap.add_argument('--out', type=Path, required=True, help='the review page to write, step_6-review.html')
    ap.add_argument('--status', type=Path, help='the review statuses, step_6-status.json: the page starts with them')
    ap.add_argument('--title', help='the page title (default: the source file name without .md, then 審核)')
    a = ap.parse_args()

    paths = {'en-o': a.src, 'en-d': a.ste, 'tw-o': a.src_tw, 'tw-d': a.ste_tw}
    for key, path in paths.items():
        if not path.is_file():
            fail(f'no {FILES[key]}: {path}')
    lines = {key: read_lines(path) for key, path in paths.items()}
    counts = {key: len(v) for key, v in lines.items()}

    try:
        import yaml
    except ImportError:
        fail('needs PyYAML: run the workspace .venv first')
    try:
        checkpoint = yaml.safe_load(a.checkpoint.read_text(encoding='utf-8')) or {}
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as e:
        fail(f'{a.checkpoint}: {e}')
    if not isinstance(checkpoint, dict) or not isinstance(checkpoint.get('step_3'), dict):
        fail(f'{a.checkpoint} has no step_3 group: run step 3 first')
    step2 = checkpoint.get('step_2') if isinstance(checkpoint.get('step_2'), dict) else None
    try:
        notes = a.notes.read_text(encoding='utf-8').lstrip('\ufeff')
    except (OSError, UnicodeDecodeError) as e:
        fail(f'{a.notes}: {e}')

    found = {key: set() for key in paths}
    names = {key: path.name for key, path in paths.items()}
    en = pane(lines['en-o'], lines['en-d'], 'en', (f'原文 · {names["en-o"]}', f'STE 草稿 · {names["en-d"]}'), found)
    tw = pane(lines['tw-o'], lines['tw-d'], 'tw', (f'原文中文版 · {names["tw-o"]}', f'STE 草稿中文版 · {names["tw-d"]}'), found)
    lp = line_pane(lines['en-d'], lines['tw-d'], (names['en-d'], names['tw-d']))
    listed = facts(step2, checkpoint['step_3'], lines['en-d'])

    problems = check_refs(listed + notes, found, counts)
    refs = len(REF_RE.findall(notes))
    if problems:
        for p in problems:
            print(f'[FAIL] {p}')
        print(f'verdict: NOT WRITTEN - {len(problems)} line reference(s) name no line; correct the review notes')
        return 1
    if not notes.strip():
        print('[WARN] the review notes are empty')
    keys = item_keys(notes)
    if len(keys) != len(LI_RE.findall(notes)):
        print('[WARN] the review notes hold an <li> the parser does not see, so no item has a status box')
        keys = []
    statuses = read_statuses(a.status, keys)
    status_data = json.dumps(statuses, ensure_ascii=False).replace('</', '<\\/')

    title = a.title or f'{a.src.name[:-3] if a.src.name.endswith(".md") else a.src.name} 審核'
    hint = ('<p class="hint">點任何一個「第 N 行」，就會切到對應的分頁、捲到那一行並標亮；'
            '「◄&nbsp;9」是左欄的第 9 行，「10&nbsp;►」是右欄的第 10 行，滑鼠移到行號上會顯示它在哪個頁籤、哪個檔案；'
            '同一項裡點過的行號都保留反白，剛點的較深、其餘較淡；點到另一項的行號，才清掉前一項的反白。'
            '落在程式碼區塊裡的行，會自動展開區塊。'
            '視窗夠寬時，上下兩區各自捲動，拖曳中間的分隔線可以調整兩區的大小；'
            'English 與中文頁籤的左右兩欄也各自捲動，打開頁籤列的「同步捲動」，捲一欄時另一欄會跟到同一節；'
            '每一欄頂端的檔名旁，寫著它目前所在的 chapter 與小節。</p>')
    reply = ('<p class="hint">回覆時，請用「英文第 N 行」或「中文第 N 行」指出要改的地方，'
             'N 是 STE 草稿或它的中文版的行號。</p>')
    page = (f'<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(title)}</title>\n'
            f'<style>{STYLE}</style></head><body>\n'
            f'<div id="upper"><header><h1>{html.escape(title)}</h1><div class="sub">英文 {counts["en-o"]} → {counts["en-d"]} 行；'
            f'中文 {counts["tw-o"]} → {counts["tw-d"]} 行。左欄原文、右欄 STE 草稿，兩欄各自捲動；'
            f'數字是各自檔案的行號。</div></header>\n'
            f'<div class="notes">{hint}{link_refs(listed, names)}</div>\n'
            f'<div class="notes" id="review-notes"><div class="st-bar"><span id="st-count"></span><span id="st-flag" class="mut"></span></div>'
            f'<p class="hint" id="st-note"></p>{link_refs(add_status_boxes(notes, keys), names)}{reply}</div></div>\n'
            f'<div id="split" role="separator" aria-orientation="horizontal" tabindex="0" '
            f'aria-label="拖曳調整上下兩區的大小" title="拖曳調整上下兩區的大小"></div>\n'
            f'<div id="lower"><div class="tabs"><button class="on" data-t="en">English</button><button data-t="tw">中文</button>'
            f'<button data-t="lp">草稿英中逐行</button>'
            f'<button class="sync" type="button" aria-pressed="false" title="打開時，捲動一欄，另一欄跟到同一節的同一處">同步捲動</button></div>\n'
            f'<main><div id="en">{en}</div><div id="tw" class="hide">{tw}</div><div id="lp" class="hide">{lp}</div></main></div>\n'
            f'<script id="status-data" type="application/json">{status_data}</script>\n'
            f'<script>{SCRIPT}</script></body></html>\n')
    try:
        a.out.write_text(page, encoding='utf-8')
    except OSError as e:
        fail(f'{a.out}: {e}')

    print(f'review page: {a.out}')
    print(f'sections: {len(sections(lines["en-o"]))} in the source file, {len(sections(lines["en-d"]))} in the STE file')
    print(f'lines: source file {counts["en-o"]}, STE file {counts["en-d"]}, '
          f'source TW twin {counts["tw-o"]}, STE TW twin {counts["tw-d"]}')
    print(f'line references: {refs} in the review notes, every one names a line')
    v = sum(1 for s in statuses.values() if s == 'v')
    x = sum(1 for s in statuses.values() if s == 'x')
    q = sum(1 for s in statuses.values() if s == '?')
    print(f'review statuses: {len(keys)} items - {v} approved, {q} to be explained, {x} rejected, '
          f'{len(keys) - v - x - q} pending')
    print('verdict: WRITTEN')
    return 0


if __name__ == '__main__':
    sys.exit(main())
