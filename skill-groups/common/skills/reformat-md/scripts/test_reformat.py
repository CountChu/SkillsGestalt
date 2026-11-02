#!/usr/bin/env python3
"""Test transform 10 of reformat_md.py: where it breaks a line into sentences, and where it does not.

Each case is a paragraph and the lines that reformatting it in clean mode must give. A case
for a break shows the next sentence on a new line; a case for no break shows the paragraph
unchanged. Each one is also run a second time, which must change nothing.

Run it after a change to reformat_md.py:

  python3 test_reformat.py

Every case prints one line, [PASS] or [FAIL], each failure followed by the lines it gave.

Exit status: 0 every case passed; 1 a case failed.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reformat_md import reformat  # noqa: E402

CASES = [
    # an end mark in quotes ends no sentence
    ('a straight quote keeps its sentences',
     'It prints **"Warning: you are outside this system. Please stop."** and exits.',
     ['It prints **"Warning: you are outside this system. Please stop."** and exits.']),
    ('a curly quote keeps its sentences',
     'It prints “Stop here. Then go.” and exits.',
     ['It prints “Stop here. Then go.” and exits.']),
    ('a sentence that ends in a quote stays with the next, as one in brackets does',
     'He said "Stop." Then it ran.',
     ['He said "Stop." Then it ran.']),
    ('a straight quote with no closing mark is a character',
     'The panel is 5" wide. Then it stops.',
     ['The panel is 5" wide.', 'Then it stops.']),
    ('a single quote is not a quote',
     "It's done. Then the users' files go.",
     ["It's done.", "Then the users' files go."]),
    ('a quote that opens a sentence starts it',
     'It ended. "Next" was printed.',
     ['It ended.', '"Next" was printed.']),
    # how the next sentence starts
    ('a symbol opens a sentence',
     'Press the key. ⌘ opens the menu.',
     ['Press the key.', '⌘ opens the menu.']),
    ('an arrow opens a sentence',
     'It is done. → The next step follows.',
     ['It is done.', '→ The next step follows.']),
    ('a lowercase name with a hyphen opens a sentence',
     'Use the tool. mermaid-view draws the graph.',
     ['Use the tool.', 'mermaid-view draws the graph.']),
    ('a lowercase word without a hyphen does not',
     'Use the tool. pathlib reads the path.',
     ['Use the tool. pathlib reads the path.']),
    ('an abbreviation ends no sentence',
     'Some files, e.g. well-known ones, stay.',
     ['Some files, e.g. well-known ones, stay.']),
    ('a capital opens a sentence',
     'It is done. The next one waits.',
     ['It is done.', 'The next one waits.']),
    ('a number with a dot ends no sentence',
     'See section 2.1 for the rule. It applies.',
     ['See section 2.1 for the rule.', 'It applies.']),
    # $$ in inline code is no math
    ('$$ in inline code leaves the line prose',
     'Write `$$...$$` for display math. Put it on its own line.',
     ['Write `$$...$$` for display math.', 'Put it on its own line.']),
    ('$$ outside inline code leaves the line as it is',
     'The sum is $$a + b$$ here. It holds.',
     ['The sum is $$a + b$$ here. It holds.']),
]


def body(lines: list[str]) -> list[str]:
    """The paragraph lines of a reformatted case, the title left out."""
    return [l for l in lines[1:] if l.strip()]


def main() -> int:
    failed = 0
    for name, paragraph, want in CASES:
        once = reformat(f'# Case\n\n{paragraph}\n', raw=False)
        twice = reformat(once, raw=False)
        got = body(once.split('\n'))
        ok = got == want and twice == once
        failed += not ok
        print(f'[{"PASS" if ok else "FAIL"}] {name}')
        if not ok:
            for l in got:
                print(f'         {l}')
            if twice != once:
                print('         a second run changed it')
    print(f'\nverdict: {"PASS" if not failed else "FAIL"} - {len(CASES) - failed} passed, {failed} failed')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
