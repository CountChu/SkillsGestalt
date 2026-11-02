---
name: del-tags
description: The skill removes a tag value from the Tags field of one or more wiki Markdown files.
---

# MUST FOLLOW

- Must run workflow step by step, and display each step number.

# Prompt Examples

## Prompt 1

```
Remove tag note from
wiki\triage-test-case\tc3390145_verify_pcie_enumeration_20260508_193031_triage.md
```

## Prompt 2

```
wiki\build-pr\pr-fix_0508.md
del tag: todo
```

## Prompt 3

```
Remove tag 2605-white-list from these files:
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
  - **Tag value**: The tag string to remove (e.g., `note`).

- If the target file(s) or tag value is missing from the prompt, ask the user.

- Validate the tag value against `database/tags.yaml`.
  If the tag is not listed there, warn the user and ask for confirmation before proceeding.

- Verify each target file exists.
  If a file does not exist, warn and skip it.


## Step 1 - Remove Tag

- For each target file:
  - Read the file header section (the first ~10 lines containing `- **...**:` metadata fields).
  - Check if a `- **Tags**:` line exists:
    - If it does not exist, skip the file (nothing to remove).
    - If it exists but does not contain the tag value, skip the file.
    - If it exists and contains the tag value:
      - Remove the tag value from the comma-separated list.
      - Clean up any leading/trailing commas and extra spaces.
      - If no tags remain after removal, remove the entire `- **Tags**:` line.
  - Save the file.

- Display a summary of files modified and tags removed.


## Step 2 - Synch Tags in Build Logs

- Search `{wikiDir}\report-logs\` (recursively, including `by-updated\`, `by-created\`, `by-tag\`) for any MD report files whose tables reference the **target file(s)** modified in Step 1.
  - A reference is a row containing a link like `[<file-name>](.../<file-name>.md)`.
- Present the list of candidate build-log MD files to the user and ask which ones to synch.
  Default selection is **all** matched files.
- For each user-confirmed build-log MD file:
  - Locate the table row(s) for the target file.
  - Update the `File` cell to remove the deleted tag from the `<br>` followed by space-separated `` `tag` `` list.
  - If the row does not list the tag, skip it.
  - If removing the tag leaves no tags, also remove the trailing `<br>` so only the link remains.
  - Update the `- **Updated**:` header field of the build-log MD to the current local date-time (`Get-Date -Format "yyyy-MM-dd HH:mm"`); preserve `- **Created**:`.
  - Save the file.
- For tag-grouped reports (`{wikiDir}\report-logs\by-tag\<tag>.md`):
  - **Do not delete** the `<tag>.md` file or remove rows from it in this step (defer to the report-logs skill).
- Display a summary of build-log MD files modified.
