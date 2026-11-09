---
name: reformat-md
description: "Reformat a user-specified Markdown file, and its 繁體中文 twin with it, to the MD style rules in md-style.md - one sentence per line among them - then verify that no text was lost or added and that the twin still lines up with its English file sentence for sentence"
---

# TERMINOLOGY

Terms that mean the same thing in every skill.

- **`run step N`** — a selector at the end of a prompt, which identifies one step.
- **Run Number** — the number of one run, `{yymmdd}.{N}`.
  `{N}` is the sequence number of the run of this skill on that date, and it starts at 1.
- **Working Dir** — the directory for one run, which holds all the working data of the run: its step files, its data files and its temporary files.
  In this skill, it is the Checkpoint Dir, and **CONFIGURATION** gives it.
  The skill does not remove it.
- **Checkpoint Dir** — a Working Dir in `checkpoints\` at the root of the workspace.
- **Step file** — the `step_{N}.yaml` in the Working Dir.
  Each step writes its outputs there.
  Thus, a subsequent step reads these outputs, and does not calculate them again.
- **Run record** — the file that records the time and the model of each step of one run.
  The analysis of the efficiency of a skill uses it.

# DEDICATED TERMINOLOGY

Terms specific to this skill.

- **`#v1` copy** — the reformatted copy of one half of the pair, `<name>#v1.md` for the English file and `<name>-tw#v1.md` for the twin, in the Working Dir.
  The original stays as it was; the run reformats only the copies.

# CONFIGURATION

Concrete values this skill runs with.

The inputs and tools, which the run reads or runs:

- **Workspace configuration** — the [config.yaml](config.yaml) at the root of the workspace.
- **Scripts** — `{skillGroups.common}\skills\reformat-md\scripts\reformat_md.py` and `{skillGroups.common}\skills\reformat-md\scripts\check_reformat.py`.
- **MD style rules** — `{skillGroups.common}\rules\md-style.md`.

The working data of a run, which no person and no skill reads after the run:

- **Working Dir** — the Checkpoint Dir, `checkpoints\reformat-md\{yymmdd}.{N}\`.
- **`#v1` copies** — `checkpoints\reformat-md\{yymmdd}.{N}\<name>#v1.md` and `checkpoints\reformat-md\{yymmdd}.{N}\<name>-tw#v1.md`, the data files of the run.

The last outputs, which a person, a different skill or a subsequent analysis reads:

- **Run record** — `database\skill-runs\reformat-md\{yymmdd}.{N}.yaml`.

# MUST FOLLOW

- Must run workflow step by step, and display each step number.
- **Honor a `run step N` selector**: run Step N, and then stop.
  Read the output of each previous step from its step file.
  Do not run a subsequent step.
- Never modify the user-specified MD file or its twin — `<name>-tw.md` beside it, or the English file when the given one is the twin.
  The run writes only its `#v1` copies, its step files and its run record.
  Do NOT modify any other files.
- Obey [run-data-rules.md](skill-groups/common/rules/run-data-rules.md) for the Run Number, the step files, the run record and the Working Dir of a run.
- **Before the skill stops, show the paths of the `#v1` copies and of the run record.**
  Show only the paths, as Markdown links whose target starts at the workspace and uses the forward slash — not as inline code or plain text.
  Write the `#` of a `#v1` copy as `%23` in the link target, or the link opens `<name>` at a heading `v1.md`: `[SKILL#v1.md](checkpoints/reformat-md/{yymmdd}.{N}/SKILL%23v1.md)` and `[{yymmdd}.{N}.yaml](database/skill-runs/reformat-md/{yymmdd}.{N}.yaml)`.
  Do this for each run, and also for a run of only one step, for example `run step 0`.
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
mods\mermaid-view\MermaidView-RSDC-tw.md
```

## Prompt 3

```
Reformat the MD
mods\mermaid-view\MermaidView-RSDC-tw.md
run step 0
```

## Prompt 4

```
Reformat the MD
skill-groups\common\skills\check-skill\SKILL.md
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
  A repo file is given `--mode clean` in Step 1, since one `*` bullet would make the detection read it as a paste ([md-style.md](skill-groups/common/rules/md-style.md), transform 2).

- Check if the below scripts exist before running workflow.
  They must exist.
  - `{skillGroups.common}\skills\reformat-md\scripts\reformat_md.py`
  - `{skillGroups.common}\skills\reformat-md\scripts\check_reformat.py`

- Read [md-style.md](skill-groups/common/rules/md-style.md) to anchor the rules in scope.

- Audit [reformat_md.py](./scripts/reformat_md.py) against the rules just anchored.
  Confirm each rule in [md-style.md](skill-groups/common/rules/md-style.md) has a corresponding transform in the script — every rule but those under its "Rules checked elsewhere".
  Those rules change words, which this skill never does, and each one names what checks it instead.
  If a rule has no matching transform — or the script enforces a rule not in `md-style.md` — stop and surface the gap before running Step 1.
  Do not edit the script in this skill; flag it for a separate change.

- Save the canonical skill invocation, thus the subsequent steps can refer to it.

- Get the Run Number, as run-data-rules.md tells, and write the run record of the run, with the canonical skill invocation as its `prompt`.

- Save `step_0.yaml`, with: the English file's path, the twin's path (or none), and the mode decided above.
  Add this step to the run record.


## Step 1 - Reformat MD

- Read the English file's path, the twin's path and the mode from `step_0.yaml`.

- Each original gets its `#v1` copy in the Working Dir, never beside the original.
  For example, `mods\mermaid-view\MermaidView-RSDC-tw.md` → `{Working Dir}\MermaidView-RSDC-tw#v1.md`.
  A pair gets one for each half: `SKILL.md` → `{Working Dir}\SKILL#v1.md`, `SKILL-tw.md` → `{Working Dir}\SKILL-tw#v1.md`.

- Copy each original MD file to its `#v1` path first, then run the script on the copies.
  Create the Working Dir when it is not there.

- Read the user-specified MD file end-to-end first, so you can describe what changed after the script runs.

- Run the script [reformat_md.py](./scripts/reformat_md.py) to apply every Markdown-style transformation in one pass:
  ```bash
  python3 {skillGroups.common}/skills/reformat-md/scripts/reformat_md.py "checkpoints/reformat-md/{yymmdd}.{N}/<name>#v1.md" --twin "checkpoints/reformat-md/{yymmdd}.{N}/<name>-tw#v1.md" --mode clean
  ```
  - The first argument is the English file's `#v1` copy, and `--twin` the twin's.
    Quote each path: a name can hold a space, and in a shell a `#` at the start of a word starts a comment.
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

- The script applies the ten transforms documented in [md-style.md](skill-groups/common/rules/md-style.md) ("Transforms applied by reformat_md.py").
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

- Save `step_1.yaml`, with: the path of each `#v1` copy, the mode the script reported, and the metrics of each file.
  Add this step to the run record.


## Step 2 - Verify & Report

- Read the original paths from `step_0.yaml`, and the `#v1` paths and the mode from `step_1.yaml`.

- Run the script [check_reformat.py](./scripts/check_reformat.py) on each original and its `#v1` copy, in the mode Step 1 reported:
  ```bash
  python3 {skillGroups.common}/skills/reformat-md/scripts/check_reformat.py --mode <mode> <original-path> "checkpoints/reformat-md/{yymmdd}.{N}/<name>#v1.md" --twin <original-tw-path> "checkpoints/reformat-md/{yymmdd}.{N}/<name>-tw#v1.md"
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
  Run each on each `#v1` copy, `"checkpoints/reformat-md/{yymmdd}.{N}/<name>#v1.md"` here, quoted for its `#`:
  ```bash
  grep -nE '[0-9]\\\.' "checkpoints/reformat-md/{yymmdd}.{N}/<name>#v1.md"
  grep -nE '^\s*\*\s' "checkpoints/reformat-md/{yymmdd}.{N}/<name>#v1.md"
  grep -nE '^#+ \*\*' "checkpoints/reformat-md/{yymmdd}.{N}/<name>#v1.md"
  grep -nE '\\[-_\[\]>+]' "checkpoints/reformat-md/{yymmdd}.{N}/<name>#v1.md"
  grep -nE '[^0-9\\$][0-9]{1,2}(, ?[0-9]{1,2})*[。，：！]' "checkpoints/reformat-md/{yymmdd}.{N}/<name>#v1.md"
  ```

- The last grep is the citation check, and applies to raw mode only — transform 9 runs in no other.
  It can return a legitimate hit — a sentence that really does end in a small number (`本益比是 15。`) — so read each match rather than assuming zero.
  Transform 9 cannot tell those apart; if the script removed one, restore it by hand.

- Report in the chat reply:
  - **File**: the path of the `#v1` copy in the Working Dir — both, for a pair.
  - **Mode**: `raw` or `clean`.
  - **Headers normalized**: count of `##`/`###`/`####` after rewrite.
  - **Bullets converted**: count of `-`-bullets after.
  - **Code fences added**: count of new ` ``` ` blocks.
  - **Citations removed**: count of NotebookLM/Gemini source markers dropped.
  - **Lines joined** and **Sentences split**: from the metrics.
  - **Content check**: the verdict of `check_reformat.py`, with every finding it listed.
  - **Style greps**: each of the five verification greps with its match count (expected: 0 for the first four).

- Save `step_2.yaml`, with: the verdict of `check_reformat.py`, each finding it listed, and the match count of each grep.
  Add this step to the run record, and write `result: completed`, because it is the last step.

- Show the links to the `#v1` copies and to the run record, as **MUST FOLLOW** tells.
