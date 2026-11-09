---
name: add-tags
description: The skill adds a Tags field to one or more wiki Markdown files before the Prompt field.
---

# TERMINOLOGY

Each skill uses these terms with the same definition.

- **Run Number** — the number of one run, `{yymmdd}.{N}`.
  `{N}` is the sequence number of the run of this skill on that date, and it starts at 1.
- **Run record** — the file that records the time and the model of each step of one run.
  The analysis of the efficiency of a skill uses it.

# CONFIGURATION

The values that this skill uses in a run.

The inputs and tools, which the run reads or runs:

- **Workspace configuration** — the [config.yaml](config.yaml) at the root of the workspace.
- **Tag database** — `database\tags.yaml` at the root of the workspace, which gives the approved tags.

The last outputs, which a person, a different skill or a subsequent analysis reads:

- **Run record** — `database\skill-runs\add-tags\{yymmdd}.{N}.yaml`.
- **Tagged files** — the wiki Markdown files that the prompt gives, in `{wikiDir}\`.
  Step 1 adds the tag to their Tags field.
- **Build-log MD reports** — the MD reports in `{wikiDir}\report-logs\` that refer to a tagged file.
  Step 2 adds the tag to their rows and changes their Updated field.

# MUST FOLLOW

- Must run workflow step by step, and display each step number.
- Obey [run-data-rules.md](skill-groups/common/rules/run-data-rules.md) for the Run Number and the run record of a run.
- If the skill stops before Step 2, write `result: stopped` and `stopped_at` (the step that did not complete, for example `step_1`) into the run record.
- **Before the skill stops, show the path of the run record.**
  Show only the path, and do not show the contents.
  Write the path as a Markdown link that opens with a click, with a link target that starts at the workspace and the forward slash as the separator.
  For example: `[{yymmdd}.{N}.yaml](database/skill-runs/add-tags/{yymmdd}.{N}.yaml)`.
  Do not write it as inline code or as plain text.
  Do this for each run that has a run record, also when the skill stops early.

# Prompt Examples

## Prompt 1

```
Add Tags: 2605-white-list before Prompt
wiki\triage-test-case\tc2362070_check_device_info_20260505_222211_triage.md
```

## Prompt 2

```
wiki\triage-test-case\tc2362070_check_device_info_20260505_222211_triage.md
add Tags: 2605-white-list before Prompt
```

## Prompt 3

```
Add tag 2605-white-list to these files:
wiki\triage-test-case\tc2362070_check_device_info_20260505_222211_triage.md
wiki\triage-test-case\tc2362070_check_device_info_20260506_001222_triage.md
```


# Workflow

## Step 0 - Warmup

- Read the workspace config [config.yaml](config.yaml) at the workspace root and resolve:
  - **`wikiDir`**: the Obsidian vault root — every wiki file this skill reads or writes lives under `{wikiDir}\`.
  - Substitute the resolved value wherever `{wikiDir}` appears in the steps below (including in commands).
  - If `config.yaml` is missing or `wikiDir` is absent, stop and ask the user.

- Parse the user's prompt for:
  - **Target file(s)**: One or more wiki MD file paths (absolute or relative).
  - **Tag value**: The tag string to add (e.g., `2605-white-list`).

- If the target file(s) or tag value is missing from the prompt, ask the user.

- Validate the tag value against `database/tags.yaml`.
  If the tag is not listed there, warn the user and ask for confirmation before proceeding.

- Verify each target file exists.
  If a file does not exist, warn and skip it.

- Save the canonical skill invocation, thus the run record can give it in its `prompt` field.

- Get the Run Number, as run-data-rules.md tells, and write the run record of the run.

- Add this step to the run record.


## Step 1 - Add Tags

- For each target file:
  - Read the file header section (the first ~10 lines containing `- **...**:` metadata fields).
  - Check if a `- **Tags**:` line already exists:
    - If it exists and already contains the tag value, skip (no duplicate).
    - If it exists but does not contain the tag value, append the new tag (comma-separated).
    - If it does not exist, insert `- **Tags**: <tag_value>` immediately before the `- **Prompt**:` line.
  - Save the file.

- Display a summary of files modified and tags added.

- Add this step to the run record.


## Step 2 - Synch Tags in Build Logs

- Search `{wikiDir}\report-logs\` (recursively, including `by-updated\`, `by-created\`, `by-tag\`) for any MD report files whose tables reference the **target file(s)** modified in Step 1.
  - A reference is a row containing a link like `[<file-name>](.../<file-name>.md)`.
- Present the list of candidate build-log MD files to the user and ask which ones to synch.
  Default selection is **all** matched files.
- For each user-confirmed build-log MD file:
  - Locate the table row(s) for the target file.
  - Update the `File` cell to include the new tag(s) in the format `<br>` followed by space-separated `` `tag` `` entries (e.g., `[note-260512](write-note/note-260512.md)<br>` `` `2605-run-pr` `` `` `todo` ``).
  - If the row already lists the tag, skip it (no duplicate).
  - If the row already has a `<br>` tag list, append the new tag(s) to the existing list.
  - Update the `- **Updated**:` header field of the build-log MD to the current local date-time (`Get-Date -Format "yyyy-MM-dd HH:mm"`); preserve `- **Created**:`.
  - Save the file.
- For tag-grouped reports (`{wikiDir}\report-logs\by-tag\<tag>.md`):
  - If the new tag has no corresponding `<tag>.md` yet, **do not create** it in this step (defer to the report-logs skill).
  - If the `<tag>.md` exists but does not include the target file, skip silently — only the report-logs skill should add new rows.
- Display a summary of build-log MD files modified.

- Add this step to the run record, and write `result: completed`, because it is the last step.
