---
name: write-note-new-files
description: >-
  Reads the newFiles list from the Obsidian recently-added-files plugin's data.json
  and writes a fixed "New Notes" section in today's daily note
  ({wikiDir}/write-note/note-yyMMdd-<day>.md, where wikiDir comes from the workspace
  config.yaml) — merging into the existing "New Notes" section when present, otherwise
  appending it — with a `Note:` Obsidian wikilink (`[[<basename>]]`, falling back to a
  `[<name>](<relative-path>)` Markdown link when the basename is ambiguous) to each
  newly added wiki Markdown file.
---

# MUST FOLLOW

- Must run workflow step by step, and display each step number.
- Each step must be self-contained.
  **No forward-reference.**
- A step that a program can do deterministically must be run as a script.
  A step that needs reading, judgement, or summarization **must not** be scripted — write it as natural-language instructions for the agent to perform directly.
- This skill only **reads** the Obsidian recently-added-files `data.json` and **edits the target daily note**.
  It must not modify `data.json` and must not call any ADO write API.
- Follow the [write-note](.github/common/skills/write-note/SKILL.md) conventions for the daily-note header and section numbering (`## <N>. <Title>`).
  For the `Note:` line, **prefer an Obsidian wikilink** `Note: [[<basename>]]`, and **fall back** to the `Note: [<name>](<relative-path>)` Markdown link only when that wikilink is not workable (see Step 2).
- `Note:` is the current label; `Notes:` is its legacy form.
  Write only `Note:`, but recognize an existing `Notes:` line as the same kind of entry when merging and de-duplicating.

# Prompt Examples

## Prompt 1

```
/write-note-new-files
```

## Prompt 2

```
/write-note-new-files
tags: 2606-pipeline-report
```

## Prompt 3

```
Add today's Obsidian recently-added files as a new Notes section in today's daily note.
```


# Workflow

## Step 0 - Warmup

- Read the workspace config [config.yaml](config.yaml) at the workspace root and resolve:
  - **`wikiDir`**: the Obsidian vault root — every wiki file this skill reads or writes lives under `{wikiDir}\`.
  - Substitute the resolved value wherever `{wikiDir}` appears in the steps below (including in commands).
  - If `config.yaml` is missing or `wikiDir` is absent, stop and ask the user.

- Parse the user's prompt for:
  - **Data.json path** (optional): the Obsidian recently-added-files plugin data file.
    Defaults to `{wikiDir}\.obsidian\plugins\recently-added-files\data.json`.
    Use the user-supplied path if provided.
    It MUST exist — if it does not, abort and tell the user.
  - **Date** (optional): the target daily-note date in `yyyy-MM-dd`.
    Defaults to today (`Get-Date -Format "yyyy-MM-dd"`).
  - **Tags** (optional): a comma/space-separated list given as `tags: <tag1>, <tag2>`.
    Every tag MUST be defined in `database\tags.yaml` — resolved relative to the **workspace root**, not `{wikiDir}` (the tag database stays in the repo even when the vault lives outside it).
    If any is not listed there, warn the user and ask for confirmation before writing it.
    Omit if not provided.

- Derive the target note slug `note-<yyMMdd>-<day>` where `<day>` is the two-letter weekday abbreviation (`Su`/`Mo`/`Tu`/`We`/`Th`/`Fr`/`Sa`) of the target date (PowerShell: `$d = Get-Date '<date>'; "note-$($d.ToString('yyMMdd'))-$($d.DayOfWeek.ToString().Substring(0,2))"`).

- Get the current local date-time using `Get-Date -Format "yyyy-MM-dd HH:mm"` for the header timestamps.


## Step 1 - Read newFiles

- Read the `data.json` and parse `recentFiles.newFiles` — an ordered array of `{ "path": ..., "basename": ... }` entries.
  The `path` is relative to the wiki vault root (`{wikiDir}\`), e.g. `triage-pipeline-run/build_2797162_triage.md`.

- If `newFiles` is missing or empty, tell the user there are no new files and **stop** (do not create or edit the note).

- For each entry, resolve `{wikiDir}\<path>` to an existing file and keep only entries that resolve to an existing wiki `.md` file.
  Warn and skip any entry that does not resolve (do not invent paths).
  Preserve the `newFiles` order.

- **Exclude the target daily note itself.**
  The plugin records the daily note as a newly added file as soon as this skill creates it, so `newFiles` often contains `write-note/note-<yyMMdd>-<day>.md`.
  Drop that entry — linking a note to itself is never useful.
  Say so when skipping it.

- Display the resolved list as a short table: `#`, basename, path.


## Step 2 - Write the "New Notes" Section

- Target file: `{wikiDir}\write-note\note-<yyMMdd>-<day>.md`.
  - If it does **not** exist, create it with the write-note header (`# note-<yyMMdd>-<day>`, then `- **Skill**: write-note`, `- **Date**: <yyyy-MM-dd>`, `- **Created**: <now>`, `- **Updated**: <now>`).
  - If it **exists**, preserve the original `Created` value and set `Updated` to the current date-time.

- The section title is **fixed** to `New Notes`.
  Check whether a `New Notes` section (heading matching `^## \d+\. New Notes\b`) already exists in the file:
  - **If it exists — merge**: append the new `Note:` lines into that existing `New Notes` section (after its current `Note:` / legacy `Notes:` lines, before the next `## ` heading or EOF).
    Keep the section's existing number, heading, and body — do not duplicate them.
  - **If it does not exist — append**: count the existing `^## ` headings and add a new section `## <N>. New Notes` (where `<N>` is `count + 1`) at the end of the file, with an optional one-line body description.

- `Note:` lines: add one `Note:` line per resolved new file.
  **Prefer an Obsidian wikilink** `Note: [[<basename>]]` (the `<basename>` **without** the `.md` extension).
  - **Check the wikilink is workable first**: `<basename>` must resolve **unambiguously** to exactly one Markdown file in the wiki vault — glob `{wikiDir}\**\<basename>.md` (case-insensitive) and count the matches.
    - **Exactly one match** → the wikilink is workable → write `Note: [[<basename>]]`.
    - **Zero or two-or-more matches** (Obsidian cannot disambiguate a duplicated basename) → **not workable** → fall back to the **vault-root-relative Markdown link** `Note: [<basename>](<relative-path>)`, where `<relative-path>` is the entry's vault-relative `path` prefixed with `/` (e.g. `/triage-pipeline-run/build_2797162_triage.md`).
      Use forward slashes `/` and URL-encode spaces (` ` → `%20`).
  - **Do not duplicate** a `Note:` line already present in the `New Notes` section — treat the wikilink `[[<basename>]]` and the Markdown link `[<basename>](<relative-path>)` for the same file as the **same** entry (do not add one form when the other is already present), and treat a legacy `Notes:` line as the same entry as a `Note:` line.

- If **Tags** were parsed in Step 0, add/merge a `Tags: <tag1>, <tag2>` line after the `Note:` lines in the `New Notes` section, and merge those tags into the file-level `- **Tags**:` header (create it after the header bullet block if absent), per write-note.
  Only tags validated against `database\tags.yaml` may be written.

- Save the file.

- Display the saved file path and a short preview of the `New Notes` section (indicate whether it was created or merged).
