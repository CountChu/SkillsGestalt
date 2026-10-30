# Markdown style

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-18`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-30`  `8cc2e2061175`

> This file is in ASD-STE100 Simplified Technical English (STE), Issue 9.
> Technical words: abbreviation, app, backslash, block, block quote, body, bold, bracket, bullet, cell, character, chat export, citation, clause, closing bracket, colon, column, command, comma, configuration, context, decode, definition, delimiter, description, design document, diagram, digit, directory, directory tree, document, dollar sign, dynamic token, ellipsis, escape, export, extractor, fence, fenced block, fenced code block, field, file, formula, frontmatter, git, guard, handler, hard break, heading, history, idempotent-only mode, identifier, indent, inline code, inline math, key, LaTeX, line, list, marker, math, module, no-op, non-breaking space, note, page, paragraph, paste, path, pattern, prefix, preformatted block, proper name, prose, punctuation, quotation, quote, raw mode, raw paste, reformat, renderer, repository, script, section, semicolon, sentence, skill, span, spelling, string, style, subscript, table, text, thousands separator, title, token, transform, twin, unescape, unordered list, version, whitespace, word, word character, writer, year.

When you make or change a Markdown file in this repository, obey these rules:

- Use `-` for the items of an unordered list, not `*`.
- Do not put `**` around the text of a heading.
  The `#` level of a heading gives it its style.
- In a heading, write a number prefix as `1. name`.
  Do not escape the `.`, as in `1\. name`.
- Put a directory tree, an ASCII diagram or a different preformatted block in a fenced code block.
  Then characters, for example `#` and `_`, show as they are, and it is not necessary to escape them with a backslash.
- Keep `\#` escaped where a renderer can read a bare `#` as a different item.
  The renderer can read it as a tag (`#1`, `#tag`) or, at the start of a line, as a heading.
- Remove the citation markers that a NotebookLM/Gemini export keeps in the text.
  These markers are a bare `1`, `1, 2` or `2-4` at the end of a clause.
  They refer to source documents that the note does not include now, thus they point to no document.
- Write math as Obsidian math: `$...$` for inline math, and `$$...$$` for display math.
  Put display math on a line that contains only that math.
  No renderer reads the escaped LaTeX of a chat export as math (`\\\\(x\\\\)`, `\\\\ ... \\\\`, and commands with two backslashes, as in `\\text`).
  Change it to Obsidian math.
- Write prose one sentence on each line, in all the Markdown files of the repository.
  This rule does not apply to the files in `.github/external/`.
  - The end of a sentence is `。`, `？` or `！`.
    The end can also be `.`, `?` or `!`, when a space and the start of the next sentence follow it.
    A colon or a semicolon does not stop a sentence.
  - An end mark does not stop a sentence in brackets, in quotes, in inline code or in math.
    It also does not stop a sentence in an abbreviation (`e.g.`, `vs.`) or in an ellipsis.
    Without a space after it, an end mark also does not stop a sentence in a number (`2.1`), a file name or a URL.
  - If a sentence is on more than one line, put it on one line.
  - Keep headings, table rows, fenced blocks, block quotes, HTML, display math and the frontmatter as they are.
  - In a list item, start each sentence after the first on a new line.
    Give each of these lines the indent of the text of the item.
  - A 繁體中文 twin keeps the sentences of its English file one for one.
    Thus, the two files stay line for line.

## Transforms applied by reformat_md.py

The script of the `reformat-md` skill ([reformat_md.py](.github/common/skills/reformat-md/scripts/reformat_md.py)) applies the rules before this section with these transforms, in this sequence:

1. Removes the Markdown hard breaks of two spaces from the end of each line.
2. Finds if the input is a raw paste from Word/Docs.
   To find a raw paste, it looks for headings in `**`, `\.` escapes, `\-` escapes in headings, or `*` bullets.
   If it finds none of them, the file is clean, and the script goes into idempotent-only mode.
   In this mode, it does not do transforms 3–6, 8 and 9.
   But it does transform 7, which changes the math, and transform 10, which puts each sentence on a line.
   This makes a second run on a clean file a no-op.

   With `--mode raw` or `--mode clean`, the script uses that mode, and does not find a mode from the input.
   `--twin` reformats the twin of a file in the mode that the file used.
   Thus, the script always applies the same mode to the two files of a pair.
   For a file that you wrote in this repository, and that you did not paste from an export, use `--mode clean`.
   One `*` bullet can make the script read it as a paste, and raw mode moves each heading down one level.
3. **Headers**: removes the `**…**` around a heading, and unescapes `\.` and `\-` in the heading text.
   Then it moves each heading down one level (`# 1. Requirements` in the source becomes `## 1. Requirements`), but the first `#` line stays as the title of the document.
4. **Bullets**: changes each `*` at the start of a line to `-`.
   It keeps `**bold**`, and `*` in YAML strings.
5. **De-escapes body text**: `\-` → `-`, `\_` → `_`, `\[` → `[`, `\]` → `]`, `\>` → `>`, `\*` → `*`, `\=` → `=`, `\+` → `+`, `\~` → `~`, `\\n` → `\n`, `\\$` → `\$`.
   A dollar sign that is only a character stays escaped, thus Obsidian does not start a math span.
    - **A `\#` changes only in some conditions.**
      It becomes `#` only where a bare `#` has no effect.
      That is, the `#` is not at the start of a line, and is not before a word character, `-` or `/`.
      In the other conditions, it keeps the backslash, as the rule above tells.
      Examples are `機會 \#1`, `\#tag` and a `\#` at the start of a line.
      With the backslash or without it, the renderer shows only `#`, thus the escape causes no problem.
6. **Wraps preformatted blocks in fenced code blocks**:
    - A `**Syntax**` body → a ` ``` ` fence.
    - An `**Example**` body → a ` ```json ` fence.
    - A YAML configuration block below `#### Config - <name>.yaml` (adjacent `key: value` lines after the paragraph of the description) → a ` ```yaml ` fence.
    - A directory tree that starts with a `data/` line, and then `├──`/`└──` lines → a ` ``` ` fence.
    - Each handler does not put a block in a fence if the block is in a fence (the next line that is not empty is ` ``` `).
      Thus, an input that is not fully clean does not get two fences.
7. **Changes the LaTeX of a chat export to Obsidian math.**
   Gemini/NotebookLM pastes have two backslashes for each LaTeX backslash (`\text` comes as `\\text`, and `\%` as `\\%`), and they escape Markdown punctuation with one backslash (`\=`, `\+`, `\-`, `\)`, `\_`, `\~`).
   Delimiters come as runs of four backslashes: `\\\\(`…`\\\\)` for inline math, and a bare `\\\\` on each side for display math.
   Thus, a run of backslashes decodes as follows: 4 = one delimiter, 2 = one LaTeX command, and a longer run = a sum of those (6 = 4+2, 8 = 4+4, 10 = 4+4+2).

   Inline math becomes `$…$`, and display math becomes `$$…$$` on a line that contains only that math.
   The transform puts the prose before and after the display math on lines that do not contain the math.
   These decisions are important:
    - In math, `\~` becomes `-`.
      The source uses `~` for a range of numbers (`10~12%`), but LaTeX reads `~` as a non-breaking space.
      Thus, `\text{10~12\%}` shows as "10 12%", and no message tells you.
    - `\%`, `\$` and `\_` keep their backslash.
      LaTeX must have `\%` and `\$` escaped, and `PV\_1` is a LaTeX subscript.
    - The transform operates in **each** mode: raw mode and clean mode.
      It does not change a line that has no run of four backslashes.
      Thus, a second run makes no change, and the transform can also repair a file at a version after `#v1`.
    - The transform does not change a line that contains inline code, because inline code shows its text as it is.
      Escaped LaTeX that a file shows as an example, as in md-style.md, is not math, and the transform does not change it.
8. **Puts identifiers in inline code**, only in raw mode, and only in body text.
   It does not do this in fences, in heading lines, or on a line that contains inline code.
   The script contains a list of identifiers: modules (`parser.py`, `topic_mgr.py`, `render_md.py`, `exporter.py`), configurations (`sync_config.yaml`, `export_template.yaml`), tools (`pathlib`, `jinja2`, `child_process.spawn`) and paths (`data/0-raw/`, `data/1-sessions/`, `data/2-turns_md/`, `data/3-topics/`, `data/4-exports/`, `0-raw/`).
   The transform also puts in inline code each identifier that the document shows in a `{a, b, …}` set.
   Examples are the field names (`visibilityFlag`, `timestamp`, `timestampUtc`, `sessionId`, `topicId`, `turnId`, `beginTime`, `endTime`, `sessionIds`) and the configuration keys (`rawDir`, `sessionsDir`, `turnsMdDir`, `topicsDir`, `exportsDir`, `sessionGapSeconds`) of a data structure.

   A file that you wrote in this repository can show a name in a set, for example the `N` of `step_{N}`.
   If the transform also operates in clean mode, it puts that name in inline code at each location where the name is a word.
   Thus, the transform operates only in raw mode.
   It does not change a line that has a `$`/`$$` math span.
   `\text{ROIC}` gives `ROIC` to the dynamic token extractor.
   Without this rule, the transform can change the formula to `$$\text{`ROIC`}$$` in a subsequent run.
9. **Removes NotebookLM/Gemini citation markers.**
   The export identifies the source document of each part of the text with a bare `1`, a list `1, 2` / `3, 4`, or a range `2-4`.
   The markers occur in four positions, and the sequence of the patterns is important.
   The script must find a line that contains only a marker before it uses the pattern for whitespace.
   If it does not, the whitespace pattern removes only the ` 2` of `1, 2`, and `1,` stays in the text:
    - A line that contains only a marker.
      Transform 7 can make this line: when it divides `…\\\\ 6`, it gives the display block and a line that contains only the `6`.
      The transform removes this line, and does not make it an empty line.
    - `效果）1。`, `機會成本」1。`: directly after a closing bracket (`）」』】》〉`).
    - ` 1。`, ` 3, 4。`, `\$60 2,\$60`: whitespace before the marker, and the end of a clause after it.
    - `**：2 這樣…`, `（EBIT / EV）3 更高的…`: the marker is at the start of the clause, not at its end.

    Numbers that are not markers stay safe, because each pattern must have a context at the end of a clause (`。，、：；！？`, `**`, a `|` of a table cell, an ASCII `,`, or the end of a line).
    `40%`, `\$5`, `第 141 頁` and a `1.` list marker do not occur in that context.
    There are two more guards.
    A marker has a maximum of **two digits**.
    Thus, the script reads a bare `2024。` or `141。` as a year or a page, and not as a citation.
    Also, the context of an ASCII comma does not accept a thousands separator (`,(?!\d{3}(?!\d))`), thus `1,000` keeps its `1`.

    The transform operates only in raw mode, and not in inline code or in a table row.
    In a file that you wrote in this repository, a step number or a row number is in the same position as a citation (`Step 3。`, `| 1 |`).
    It only removes text, thus a second run is a no-op.

    The transform has three known limits:
    - A number of one or two digits at the end of a sentence (`本益比是 15。`) looks the same as a citation.
      Thus, the transform removes it, although it is not a marker.
    - The transform does not change a marker that has `（` after it (`**已動用有形資本**, 2（…`).
      If it removes the marker, the comma before the marker stays in the text.
    - With the `）N 中文` shape, the transform cannot find the difference between a citation and a number that is a part of the text (`（含）3 個月`).

10. **Puts one sentence of prose on each line**, in raw mode and in clean mode.
    It uses the definition of a sentence that the rule before this section gives.
    Some lines are 60 columns wide or more (a CJK character counts as two), and their end is not the end of a sentence.
    In these lines, the sentence continues on the next line, and the transform puts the two lines together.
    A shorter line, for example `**Raised**: 2026-10-11`, is a break that the writer wanted, and it stays.

    Then it breaks the line after each sentence that has its end in the line.
    In a list item, it gives each subsequent sentence the indent of the text of the item.
    A `**` directly after an end mark goes with the sentence before it only when it closes an open bold.
    A `**` that opens a bold, as in `…x。**Name**`, starts the next line, because at the end of a line it cannot open a bold.

    It changes only line breaks and the spaces around them.
    When it puts two lines together, it puts no space between two CJK characters.
    Thus, a second run is a no-op.

## Rules checked elsewhere

These rules also apply to all Markdown files of the repository.
But `reformat_md.py` does not apply them, because each one changes words.
`check_reformat.py` lets a reformat change only line breaks and the spaces around them.
Each rule tells which tool checks it.

- Write English in American spelling: "color", "behavior", "catalog" and "judgment", not "colour", "behaviour", "catalogue" and "judgement".
  [us-spelling.json](.github/common/references/us-spelling.json) gives each British spelling with its American spelling.
  The `check_ste.py` script of the `asd-ste` skill uses this list to check an STE file.
  Do not change the spelling of a quotation or of a proper name.
  A name that other documents or code use keeps its spelling too, for example the name of a component, a file or an identifier.
  In an STE file, put such a name in the `Technical words:` list, and the check then accepts it.
- Do not tell the history of a text in that text.
  This history includes the previous version of the text, the method that it replaces, and the procedure before it.
  Git and the files in `tasks/` keep this history.
  The procedure that an app replaces is not the history of its design document, and that document can tell it.
  No tool checks this rule: the person who examines the file checks it.
  - This rule does not apply to a text that records work or changes.
    These texts are the files in `tasks/`, `chores/` and `dashboard/`, the `Changes in This Version` section of an RSDC document, and the `Why` column of `ste-custom.md`.
    Also, this rule does not apply to the files in `.github/external/`.
