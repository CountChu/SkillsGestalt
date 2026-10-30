# Tool Rules

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-18`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-30`  `8cc2e2061175`

> This file is in ASD-STE100 Simplified Technical English (STE), Issue 9.
> Technical words: alias, binary, block, byte, call, command, content, default, definition, directory, false negative, field, file, filter, flag, glossary, harness, hit, line, macOS, path, pattern, prefix, preview, project, query, scope, separator, skill, string, term, token, verification.

These rules tell which command-line tools to use in all skills.
These rules are for **a smaller number of tokens**, not for one binary that is better than a different binary.

We measured all the numbers of bytes that follow on one `SKILL.md` of 363 lines and 37,948 bytes.

# 1. Search with `rg`

- Always search with `rg` (`ripgrep`).
  Do not use `grep`.
- **The cause is not the number of bytes in the output.**
  For the same query, `rg` and `grep` give the same output, byte for byte (we measured 3,728 bytes for each).
  You get the **defaults** of `rg`.
  `rg` automatically ignores the paths in `.gitignore`, and binary files.
  Thus, you do not add filters, for example `| grep -v __pycache__`.
  The result is that you write each command correctly the first time, and you operate it only one time.
- On macOS, `grep` can be an alias for **`ugrep`** (`grep --version` shows `ugrep`).
  The flags of `ugrep` do not always give the same result as the flags of GNU `grep`.
  If you use the two tools together, you get differences that are not easy to see.
  If you always use `rg`, this problem does not occur.

## Pick the flag by what you need to know

| What you need | Use | Measured output |
| :--- | :--- | ---: |
| Is it there? How many hits are there? | `rg -c pattern file` | **2 bytes** |
| Which files contain it? | `rg -l pattern dir/` | **153 bytes** |
| Which lines are around it? | `rg -n pattern -A3 file` | **298 bytes** |
| All the hits, in full | `rg -n pattern file` | **2,830 bytes** |

- To make sure that a string has **no** hits, use `rg -c` or `rg -l`, and **not** `rg -n`.
  The outputs of the two commands are different by more than 1,400×.
- **A verification search must include each directory that can contain the string.**
  Most frequently, a false negative has this cause: you examine only `scripts/`, and then you tell that the full project is clean.
  If the scope of the search is incorrect, no search tool can help you.

# 2. Read only the range you need

- It is important to compare **a range with the full file**, not one tool with the other tool.
  When you read a block of 9 lines from that `SKILL.md`, the full file is **37,948** bytes.
  The 9 lines are **~1,200** bytes.
  That 97% is the purpose of this rule.
- **Default: `rg -n pattern -B<n> -A<n>`.**
  This command needs no line numbers.
  Thus, the command is one call, and not a search and then a second call that reads the lines.
  For the same content, it uses some more bytes than `sed` (the prefixes of the line numbers, and the `--` separators).
  This difference is too small to be important.
- **Exception: if `rg` cannot isolate the one range that you want, use `sed -n 'A,Bp'`.**
  `rg` has no flag for a range of lines.
  Thus, in two conditions, `rg` does not give the range that you want.
  The two conditions look different, but they are the same problem:
  - The pattern hits **many** locations, and `-A`/`-B` shows all the blocks.
  - There is **no** pattern that identifies the range (for example, only a range of lines in the middle of the file).

  This difference is not small.
  `Checkpoint Dir` is in that `SKILL.md` 17 times.
  You want to read only the one on lines 37–38:

  | | Output |
  | :--- | ---: |
  | `rg -n 'Checkpoint Dir' -A1`: all the 17 blocks | **4,693 bytes** |
  | `sed -n '37,38p'`: only the one that you want | **119 bytes** |

  For example, a glossary gives the definition of a term, and then each step uses the term.
  This condition occurs frequently.
  First, use `rg -c` to count the hits.
  If there is more than one hit, use `sed`.
  (Use `head` or `tail` for the start or the end of the file.)
- The rule is "**read only the lines that you need**", not "use `rg`" or "use `sed`".
  If you use `sed -n '1,$p'` to read a full file that this rule does not let you read, you use the same number of tokens.
  Also, the command does not show clearly that it reads the full file.
  When you do this, you do not obey the rule.

# 3. `cat` is narrowed, not banned

- Use `cat` only in one of these conditions:
  - You know that the file is small (approximately less than 100 lines, for example a `config.yaml`).
  - A rule tells you to read the file **in full** (for example, a skill that tells you "read every `.md` in this directory, do not sample").
- For all other files, obey rule 2.
- **Do not use `cat` for more than one large file at the same time.**
  If the output is too large, the harness keeps it in a file and gives only a preview of 2KB.
  Then you must read the files again, one at a time.
  This uses more tokens than when you read the files one at a time at the start.

# 4. Print only the fields you are about to use

- When `python -c` or an equivalent command examines JSON or YAML, show **only the fields that the next step needs**.
  Do not show the full structure.
- If you show all of a large file between two steps (`market-data.json` and files of that type), you usually use more tokens than with the largest `cat`.
  In the work of agents, this is the cause of a high number of tokens that they most frequently do not see.
