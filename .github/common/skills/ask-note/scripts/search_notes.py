"""Scan every note in one vault directory for a set of case-insensitive Search Terms.

Splits each note into Sections at its `## ` headings and prints, as JSON on stdout,
every Section carrying at least one term. Writes no file.
"""

import argparse
import json
import os
import re
import sys
from datetime import date, datetime

HEADING = re.compile(r"^##(?!#)\s+(.+?)\s*$")
DATE_HEADER = re.compile(r"^-\s*\*\*Date\*\*:\s*(\d{4})-(\d{2})-(\d{2})")
DIGITS8 = re.compile(r"(\d{8})")
DIGITS6 = re.compile(r"(\d{6})")


def note_date(path, lines):
    """The note's own Date header, else a yyyymmdd/yymmdd run in its name, else its mtime."""
    for ln in lines[:15]:
        m = DATE_HEADER.match(ln)
        if m:
            return "-".join(m.groups())

    name = os.path.basename(path)
    m = DIGITS8.search(name)
    if m:
        y, mo, d = m.group(1)[:4], m.group(1)[4:6], m.group(1)[6:]
    else:
        m = DIGITS6.search(name)
        if m:
            y, mo, d = "20" + m.group(1)[:2], m.group(1)[2:4], m.group(1)[4:]
        else:
            return datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d")
    try:
        return date(int(y), int(mo), int(d)).isoformat()
    except ValueError:
        return datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d")


def split_sections(lines):
    """[(number, heading, startLine, endLine)] - lines above the first `## ` are section 0."""
    starts = [(i, HEADING.match(ln).group(1)) for i, ln in enumerate(lines, 1) if HEADING.match(ln)]
    if not starts:
        return [(0, "(header)", 1, len(lines))]

    out = [(0, "(header)", 1, starts[0][0] - 1)]
    for n, (line_no, heading) in enumerate(starts, 1):
        end = starts[n][0] - 1 if n < len(starts) else len(lines)
        out.append((n, heading, line_no, end))
    return [s for s in out if s[3] >= s[2]]


def main():
    ap = argparse.ArgumentParser(description="Search a vault directory's notes by section.")
    ap.add_argument("--notes-dir", required=True)
    ap.add_argument("--terms", required=True, nargs="+")
    ap.add_argument("--max-body", type=int, default=6000, help="chars of each hit body to emit")
    ap.add_argument("--max-hits", type=int, default=200)
    args = ap.parse_args()

    if not os.path.isdir(args.notes_dir):
        print(json.dumps({"error": f"notes dir not found: {args.notes_dir}"}), file=sys.stderr)
        return 2

    terms = [t for t in args.terms if t.strip()]
    if not terms:
        print(json.dumps({"error": "no search terms given"}), file=sys.stderr)
        return 3
    lowered = [(t, t.lower()) for t in terms]

    notes = sorted(n for n in os.listdir(args.notes_dir) if n.lower().endswith(".md"))
    per_term = {t: 0 for t in terms}
    sections_read = 0
    hits = []

    for name in notes:
        path = os.path.join(args.notes_dir, name)
        with open(path, encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
        when = note_date(path, lines)

        for number, heading, start, end in split_sections(lines):
            sections_read += 1
            body = "\n".join(lines[start - 1 : end])
            hay = (heading + "\n" + body).lower()
            matched = [t for t, low in lowered if low in hay]
            if not matched:
                continue
            for t in matched:
                per_term[t] += 1
            hits.append(
                {
                    "note": name[:-3],
                    "date": when,
                    "section": number,
                    "heading": heading,
                    "startLine": start,
                    "endLine": end,
                    "matchedTerms": matched,
                    "body": body[: args.max_body],
                    "bodyTruncated": len(body) > args.max_body,
                }
            )

    hits.sort(key=lambda h: (h["date"], h["note"], -h["section"]), reverse=True)
    truncated = len(hits) > args.max_hits

    print(
        json.dumps(
            {
                "notesDir": args.notes_dir,
                "notesRead": len(notes),
                "sectionsRead": sections_read,
                "terms": terms,
                "perTermSectionCount": per_term,
                "termsMatchingNothing": [t for t, c in per_term.items() if c == 0],
                "hitCount": len(hits),
                "hitsTruncated": truncated,
                "hits": hits[: args.max_hits],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
