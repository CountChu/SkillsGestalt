---
name: reformat-md
description: "Reformat a user-specified Markdown file, and its 繁體中文 twin with it, to the MD style rules in md-style.md - one sentence per line among them - then verify that no text was lost or added and that the twin still lines up with its English file sentence for sentence"
---

# MUST FOLLOW

- Must run workflow step by step, and display each step number.
- Touch only the user-specified MD file and its twin — `<name>-tw.md` beside it, or the English file when the given one is the twin.
  Do NOT modify any other files.
- **Reformat the two halves of a pair together, in the English file's mode.**
  Reformatted apart, they can take different modes, and a sentence split on one side only leaves them no longer line for line.
- Preserve the user's additions verbatim (new sub-sections, new numbered steps, new table rows).
  Reformat them; never drop or merge.
- **Never edit a `#v1` file to make the verification pass.**
  Text the script lost is a defect of the script, reported as one; a sentence the translation merged or split is the user's to settle in the translation.

# Prompt Examples

## Prompt 1

```
What skills do you have?
```

## Prompt 2

```
Reformat the MD
checkpoints\1 reformat rsdc\GeminiChatOrganizer-RSDC-tw.md
```

## Prompt 3

```
Reformat the MD
checkpoints\1 reformat rsdc\GeminiChatOrganizer-RSDC-tw.md
run step 0
```

## Prompt 4

```
Reformat the MD
.github\common\skills\check-skill\SKILL.md
```


# Workflow

## Step 0 - Warmup

- Read the workspace config [config.yaml](config.yaml) at the workspace root and resolve **`skillGroups`**: this skill's own directory is `{skillGroups.common}\skills\reformat-md\`, and the MD style rules are `{skillGroups.common}\rules\md-style.md`.
  Substitute the resolved value wherever `{skillGroups.common}` appears below, commands included.
  If `config.yaml` is missing or has no `skillGroups`, stop and ask the user.

- The user provides the **MD file path** in their prompt.
  Parse it from the prompt text.

- Confirm the MD file exists.
  Bail out immediately if it doesn't — there is nothing for the workflow to operate on.

- Find its twin.
  A file named `<name>-tw.md` is the twin of `<name>.md`, its English file; a file without `-tw` has `<name>-tw.md` beside it as its twin, when one exists.
  Whichever of the two the prompt names, the pair is reformatted together, and the English file decides the mode.

- Decide the mode: `clean` for a file this repo already holds, and the detection's own choice only for a paste just brought in from Word, Docs or a chat export.
  A repo file is given `--mode clean` in Step 1, since one `*` bullet would make the detection read it as a paste ([md-style.md](.github/common/rules/md-style.md), transform 2).

- Check if the below scripts exist before running workflow.
  They must exist.
  - `{skillGroups.common}\skills\reformat-md\scripts\reformat_md.py`
  - `{skillGroups.common}\skills\reformat-md\scripts\check_reformat.py`

- Read [md-style.md](.github/common/rules/md-style.md) to anchor the rules in scope.

- Audit [reformat_md.py](./scripts/reformat_md.py) against the rules just anchored.
  Confirm each rule in [md-style.md](.github/common/rules/md-style.md) has a corresponding transform in the script — every rule but those under its "Rules checked elsewhere".
  Those rules change words, which this skill never does, and each one names what checks it instead.
  If a rule has no matching transform — or the script enforces a rule not in `md-style.md` — stop and surface the gap before running Step 1.
  Do not edit the script in this skill; flag it for a separate change.


## Step 1 - Reformat MD

- The updated MD file is `<original-name>#v1.md` in the same directory as the original.
  For example, `GeminiChatOrganizer-RSDC-tw.md` → `GeminiChatOrganizer-RSDC-tw#v1.md`.
  A pair gets one for each half: `SKILL.md` → `SKILL#v1.md`, `SKILL-tw.md` → `SKILL-tw#v1.md`.

- Copy each original MD file to its `#v1` path first, then run the script on the copies.

- Read the user-specified MD file end-to-end first, so you can describe what changed after the script runs.

- Run the script [reformat_md.py](./scripts/reformat_md.py) to apply every Markdown-style transformation in one pass:
  ```bash
  python3 {skillGroups.common}/skills/reformat-md/scripts/reformat_md.py <v1-file-path> --twin <tw-v1-file-path> --mode clean
  ```
  - The first argument is the English file's `#v1` copy, and `--twin` the twin's.
    The script edits both in place, the twin in the mode the English file takes, and keeps each file's line endings.
  - Leave out `--twin` for a file with no twin, and `--mode` only for a paste whose mode the detection should decide.
    Never pass `--mode raw` for a `#v1` file: raw mode would shift every heading down once more.
  - The script outputs one block of metrics per file to stdout:
    ```
    reformatted <path>
    mode: raw|clean
    headers_normalized: <n>
    bullets_converted: <n>
    code_fences_added: <n>
    inline_code_added: <n>
    math_blocks_converted: <n>
    citations_removed: <n>
    lines_joined: <n>
    sentences_split: <n>
    ```
  - Exit codes: `0` success, `1` file missing, `2` bad arguments.

- The script applies the ten transforms documented in [md-style.md](.github/common/rules/md-style.md) ("Transforms applied by reformat_md.py").
  Skim them so you know what to expect in the diff, especially transform 2's idempotent-only mode for already-clean inputs and its modes, transform 7's math conversion, transforms 8 and 9 — inline-coding and citation stripping, both raw mode only — and transform 10's sentence lines.

- Use the script's output metrics to build the summary table, one column per file:

  | Metric | Value |
  |--------|-------|
  | Mode | from `mode:` output |
  | Headers normalized | from `headers_normalized:` output |
  | Bullets converted | from `bullets_converted:` output |
  | Code fences added | from `code_fences_added:` output |
  | Inline-code added | from `inline_code_added:` output |
  | Math blocks converted | from `math_blocks_converted:` output |
  | Citations removed | from `citations_removed:` output |
  | Lines joined | from `lines_joined:` output |
  | Sentences split | from `sentences_split:` output |

- Show the summary table in the chat reply.
  This skill writes no report file.


## Step 2 - Verify & Report

- Run the script [check_reformat.py](./scripts/check_reformat.py) on each original and its `#v1` copy, in the mode Step 1 reported:
  ```bash
  python3 {skillGroups.common}/skills/reformat-md/scripts/check_reformat.py --mode <mode> <original-path> <v1-file-path> --twin <original-tw-path> <tw-v1-file-path>
  ```
  - In clean mode every character but whitespace must read as it did; in raw mode it sets aside what the raw transforms may change.
    It lists every change with its line on each side, then compares the headings and the bold markers, and for a pair, the two `#v1` files block by block: after transform 10 a block holds one line per sentence, so a block whose line counts differ is a paragraph whose sentences the translation did not keep one for one.
  - Exit codes: `0` nothing to fix, `1` a finding, `2` a file it cannot read.

- Act on each finding:
  - **Characters other than whitespace changed** (`[FAIL]`, clean mode): a defect of `reformat_md.py` — clean mode changes only line breaks and the spaces around them.
    Report the lines listed and stop; never patch the `#v1` file to hide it.
  - **Text lost or added** (`[FAIL]`, raw mode): a defect of `reformat_md.py`.
    Report the lines listed and stop; never patch the `#v1` file to hide it.
  - **A `**` that cannot open or close** (`[FAIL]`): a defect of `reformat_md.py` — a line break left an opening `**` at the end of a line, or a closing one at the start of one, and the bold no longer renders.
    Report the lines listed and stop.
  - **Citation markers removed** (`[WARN]`, raw mode only): read each listed line of the original.
    A real number that only looks like a citation (`本益比是 15。`) is restored by hand in the `#v1` file.
  - **Escapes or math changed** (`[WARN]`, raw mode): read each.
    Transforms 5 and 7 drop escapes and rewrite chat-export math on purpose, a delimiter's `(` and `)` among them; anything else is reported.
  - **Punctuation changed** (`[WARN]`, raw mode): read each, and report any change the transforms do not explain.
  - **Headings changed** (`[FAIL]`): in clean mode any change is a defect; in raw mode only a change of a title's text is.
    Report it.
  - **The pair does not line up** (`[FAIL]`): show each block it names, the English sentences beside the twin's.
    The twin keeps its English file's sentences one for one, so the user settles each block in the translation; never merge or split sentences by hand to force the counts.

- Eyeball the diff for anything the script couldn't infer (a brand-new sub-section type, a Syntax block that uses an unfamiliar marker word, a custom code-ish identifier that isn't in the inline-code list).
  Hand-touch only those.

- Run these greps as well.
  The first four should return zero matches.
  `\#` is deliberately absent from the fourth — transform 5 keeps that escape where a bare `#` would become a tag or a heading:
  ```bash
  grep -nE '[0-9]\\\.' <v1-file-path>
  grep -nE '^\s*\*\s' <v1-file-path>
  grep -nE '^#+ \*\*' <v1-file-path>
  grep -nE '\\[-_\[\]>+]' <v1-file-path>
  grep -nE '[^0-9\\$][0-9]{1,2}(, ?[0-9]{1,2})*[。，：！]' <v1-file-path>
  ```

- The last grep is the citation check, and applies to raw mode only — transform 9 runs in no other.
  It can return a legitimate hit — a sentence that really does end in a small number (`本益比是 15。`) — so read each match rather than assuming zero.
  Transform 9 cannot tell those apart; if the script removed one, restore it by hand.

- Report in the chat reply:
  - **File**: the `#v1` output file path — both, for a pair.
  - **Mode**: `raw` or `clean`.
  - **Headers normalized**: count of `##`/`###`/`####` after rewrite.
  - **Bullets converted**: count of `-`-bullets after.
  - **Code fences added**: count of new ` ``` ` blocks.
  - **Citations removed**: count of NotebookLM/Gemini source markers dropped.
  - **Lines joined** and **Sentences split**: from the metrics.
  - **Content check**: the verdict of `check_reformat.py`, with every finding it listed.
  - **Style greps**: each of the five verification greps with its match count (expected: 0 for the first four).
