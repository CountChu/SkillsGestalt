---
name: synch-two-mds
description: "Synchronize two parallel Markdown files (e.g., English and Chinese) by merging unique content from each into the other"
---

# MUST FOLLOW

- Must run workflow step by step, and display each step number.
- Do NOT delete or rewrite existing content.
  Only add missing sections/bullets translated from the other file.
- Preserve each file's language — translate added content into the target file's language.
- Preserve heading structure, numbering, and formatting of both files.

# Prompt Examples

## Prompt 1

```
synch the two MD files. The first is English. The second is Chinese
checkpoints\2 synch rsdc\GeminiChatOrganizer-RSDC.md
checkpoints\2 synch rsdc\GeminiChatOrganizer-RSDC-tw.md
```

## Prompt 2

```
Synchronize these two docs (EN and TW):
docs\spec-en.md
docs\spec-tw.md
```

## Prompt 3

```
Merge both ways:
wiki\design-en.md (English)
wiki\design-zh.md (Chinese)
```


# Workflow

## Step 0 - Warmup

- Read the workspace config [config.yaml](config.yaml) at the workspace root and resolve:
  - **`wikiDir`**: the Obsidian vault root — every wiki file this skill reads or writes lives under `{wikiDir}\`.
  - Substitute the resolved value wherever `{wikiDir}` appears in the steps below (including in commands).
  - If `config.yaml` is missing or `wikiDir` is absent, stop and ask the user.

- Parse the user's prompt for:
  - **File A path** and its **language label** (e.g., English).
  - **File B path** and its **language label** (e.g., Chinese).

- Confirm both files exist.
  Bail out if either is missing.

- The **checkpoints directory** is the shared parent directory of the two files.
  - If files are in different directories, default to `{wikiDir}\synch-two-mds`.

- Check if the checkpoints directory exists.
  Create it if not.

- Save the entire user prompt text for reference in later steps.

- The report MD file name is `yyyy-mm-dd#hh-mm#<file-A-basename>--<file-B-basename>.md`.

- Follow [report-md-rules.md](.github/common/rules/report-md-rules.md) to create or update the report file, using the filename pattern above as `{REPORT_FILENAME}`.


## Step 1 - Diff & Merge

- Read both files end-to-end.
  Build a mental map of each file's section structure (headings, sub-headings, bullet lists).

- Identify content unique to File A (not present in File B) and content unique to File B (not present in File A).
  Compare at the section/bullet granularity, not line-by-line.

- For each unique section or bullet:
  - Translate it into the target file's language.
  - Insert it at the structurally equivalent position in the target file.

- After merging, confirm both files now have the same logical structure and coverage.

- Summarize changes in a table:

  | Metric | Value |
  |--------|-------|
  | Sections added to File A | count |
  | Bullets added to File A | count |
  | Sections added to File B | count |
  | Bullets added to File B | count |

- Follow [report-md-rules.md](.github/common/rules/report-md-rules.md) "Update report" with the summary table above.
