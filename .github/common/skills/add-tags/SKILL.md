---
name: add-tags
description: The skill adds a Tags field to one or more wiki Markdown files before the Prompt field.
---

# MUST FOLLOW

- Must run workflow step by step, and display each step number.

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


## Step 1 - Add Tags

- For each target file:
  - Read the file header section (the first ~10 lines containing `- **...**:` metadata fields).
  - Check if a `- **Tags**:` line already exists:
    - If it exists and already contains the tag value, skip (no duplicate).
    - If it exists but does not contain the tag value, append the new tag (comma-separated).
    - If it does not exist, insert `- **Tags**: <tag_value>` immediately before the `- **Prompt**:` line.
  - Save the file.

- Display a summary of files modified and tags added.


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
