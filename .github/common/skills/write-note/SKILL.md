---
name: write-note
description: The skill creates a daily note Markdown file in wiki/write-note, translating any non-English content (e.g., Chinese) to English.
---

# MUST FOLLOW

- Must run workflow step by step, and display each step number.
- Each step must be self-contained.
  **No forward-reference.**
- A step that a program can do deterministically must be run as a script.
  A step that needs reading, judgement, or summarization **must not** be scripted — write it as natural-language instructions for the agent to perform directly.
- Translate any non-English content (e.g., Traditional Chinese, Simplified Chinese, Japanese) to English.
  Preserve URLs, code, command names, identifiers, and proper nouns verbatim.
- Preserve the meaning faithfully.
  Do not paraphrase away technical detail.
- If the prompt specifies `tags:`, every tag MUST be defined in `database/tags.yaml`.
  If it specifies `notes:`, the referenced note MD MUST exist (resolve it under `{wikiDir}\`).
  Validate both in Step 0 before writing anything.

# Prompt Examples

## Prompt 1

```
/write-note
notes:  pr-fix_0709
tags: 2607-acpi-tpm2
```

## Prompt 2

```
Write a note for today from Kane:

你這邊 能不能幫們做個skill 就是 submit pr 前 會自動把要做的test case 加到 debug.custom.args
```

## Prompt 3

```
Append today's note from Kane:
Pipeline 觸發後 結果會 mail 給我
```


# Workflow

## Step 0 - Warmup

- Read the workspace config [config.yaml](config.yaml) at the workspace root and resolve:
  - **`wikiDir`**: the Obsidian vault root — every wiki file this skill reads or writes lives under `{wikiDir}\`.
  - Substitute the resolved value wherever `{wikiDir}` appears in the steps below (including in commands).
  - If `config.yaml` is missing or `wikiDir` is absent, stop and ask the user.

- Parse the user's prompt for:
  - **Date**: Target note date in `yyyy-MM-dd`.
    If not provided, default to today (`Get-Date -Format "yyyy-MM-dd"`).
  - **Source / Author**: The person the note is from (e.g., `Kane`).
    If not provided, omit the source heading.
  - **Body**: The raw note text (may contain non-English characters and URLs).
  - **Tags** (optional): a comma/space-separated tag list given as `tags: <tag1>, <tag2>`.
    Every tag MUST be defined in `database\tags.yaml`; if any tag is not listed there, warn the user and ask for confirmation before writing it.
    Omit if not provided.
  - **Note reference** (optional): a reference to an existing note/report MD given as `notes: <name>` (e.g. `notes: pr-fix_0709`).
    Resolve `<name>` to a wiki MD file — try `{wikiDir}\write-note\<name>.md`, else glob `{wikiDir}\**\<name>.md` — and it MUST exist.
    If it does not resolve to exactly one existing file, abort and tell the user (do not invent a path).
    Capture its wiki-relative path for the `Note:` line.
    Omit if not provided.
  - **Notes directory**: Defaults to `{wikiDir}\write-note`.
    Use the user-supplied path if provided.

- Derive the **file slug** as `note-yyMMdd-<day>` where:
  - `yyMMdd` is two-digit year, two-digit month, two-digit day, no separators.
  - `<day>` is the two-letter abbreviation of the target date's weekday: `Su`, `Mo`, `Tu`, `We`, `Th`, `Fr`, `Sa`.
  - Example: `2026-05-12` (a Tuesday) -> `note-260512-Tu`.
  - PowerShell (today): `"note-$(Get-Date -Format 'yyMMdd')-$((Get-Date).DayOfWeek.ToString().Substring(0,2))"`.
  - PowerShell (specific date): `$d = Get-Date '2026-05-12'; "note-$($d.ToString('yyMMdd'))-$($d.DayOfWeek.ToString().Substring(0,2))"`.

- If the body is missing, ask the user.

- Ensure the notes directory exists.
  Create it if not.

- Get the current local date-time using `Get-Date -Format "yyyy-MM-dd HH:mm"` for header timestamps.


## Step 1 - Create or Append Note File

- Target file: `<notes-dir>\note-<yyMMdd>-<day>.md` (e.g., `{wikiDir}\write-note\note-260512-Tu.md`).

- If the file does not exist, create it with the following header:
  - **Title**: `# note-<yyMMdd>-<day>` (e.g., `# note-260512-Tu`).
  - **Header fields** (bullet list immediately after the title):
    - **Skill**: write-note
    - **Date**: `<yyyy-MM-dd>` (the full date, for readability).
    - **Created**: current date-time
    - **Updated**: current date-time

- If the file already exists:
  - Preserve the original `Created` value.
  - Update `Updated` to the current date-time.
  - Append the new section at the end.

- Append the note section:
  - Heading: auto-generate a concise topic heading from the body content (3-7 words, Title Case, no trailing punctuation).
    It should summarize the main subject of the note (e.g., `Created run-pr Skill`, `Update X750 Pipeline White List`, `Pipeline Trigger Email Notification`).
    - **Prefix with a sequence number**: every `##` section in the file must start with `<N>. ` where `<N>` is the 1-based index of that section within the file.
      When appending, count the existing `^## ` headings in the file and use `<count+1>` as the prefix.
      Final form: `## <N>. <Topic>` (e.g., `## 1. Created run-pr Skill`, `## 2. Update X750 Pipeline White List`).
    - If a source was provided, append ` (from <Source>)` to the heading (e.g., `## 1. Created run-pr Skill (from Kane)`).
    - If the body is too short or ambiguous to summarize, fall back to `## <N>. Note` (or `## <N>. From <Source>` when a source is provided).
  - Body: the translated English text.
  - URLs: render as `[<link-text>](<url>) (<title>)` where only the link text is clickable and the title is plain text after the link.
    Rules for `<link-text>`:
    - If the URL contains an id (e.g., `sharedParameterId=<id>`, `_workitems/edit/<id>`, `buildId=<id>`, `pullRequestId=<id>`), use the bare id as the link text.
      Examples:
      - ADO work item: `[3574782](https://.../_workitems/edit/3574782) (SMBIOS0018 ...)`.
      - ADO shared parameter: `[3367502](https://.../sharedParameters?sharedParameterId=3367502&_a=values) (C419E_SMBIOS_Type_45)`.
      - ADO build results: `[1234567](https://.../_build/results?buildId=1234567) (FW_DEV #1234567)`.
      - ADO PR: `[12345](https://.../pullrequest/12345) (Fix X750 whitelist)`.
    - If the URL has no id, fall back to a short friendly name derived from the URL context (e.g., file path, page title, last meaningful segment).
      Examples:
      - ADO Git file preview: `[run-pr/SKILL.md @ my_branch](https://dev.azure.com/contoso/Firmware/_git/tools?version=GBuser/me/my_branch&path=/.github/skills/run-pr/SKILL.md&_a=preview) (run-pr SKILL)`.
    - The `(<title>)` suffix is the human-readable title fetched from ADO (e.g., `System.Title` for work items / shared parameters) or derived from the page context.
      Omit the suffix only when no meaningful title can be obtained.
    - If the user already supplied a Markdown link, preserve it as-is.
    - Only fall back to a bare angle-bracket link `<https://...>` when no meaningful link text can be derived.
  - Code, identifiers, file paths, and command names: wrap in backticks.

- Auto-add references:
  - If the note's content was moved or copied from another wiki MD file, or the user explicitly cites a source MD, add a `> Note: [<title>](<relative-path>)` blockquote line immediately after the section heading.
  - The path must be relative to the note's location (e.g., from `{wikiDir}\write-note\` use `../topics/<file>.md`).
  - URL-encode spaces in the link target (` ` -> `%20`); keep the display text human-readable.
  - If multiple sources apply, list each on its own `> Note:` line.
  - Skip this step if no source MD is known.

- Add the `notes:` line (only if a **Note reference** was parsed in Step 0):
  - Append a plain (non-blockquote) `Note: [<name>](<relative-path>)` line at the end of the section body (before the next `## ` heading or EOF), using the resolved MD path as a **vault-root-relative** link (from the `{wikiDir}\` vault root use `/<dir>/<name>.md`, e.g. `/triage-test-case/<name>.md`; URL-encode spaces `%20`).
  - Idempotency: if a plain `Note:` line — or a legacy `Notes:` line — for the same `<name>` already exists in the section, do not duplicate it.
    The `> Note:` blockquote added by **Auto-add references** is a separate form and does not count.
    When both are present, place the `Note:` line above the `Tags:` line.

- Add the `tags:` line (only if **Tags** were parsed in Step 0):
  - Append a `Tags: <tag1>, <tag2>, ...` line (comma + space separated, in the order given) at the end of the section body (before the next `## ` heading or EOF).
    If a `Tags:` line already exists in the section, merge — append only tags not already listed, preserving order.
  - Merge the same tags into the file-level `- **Tags**:` header: create it right after the header bullet block if absent (matching the surrounding `- **<Field>**:` style), else append only new tags to the existing comma-separated list.
  - Only tags validated against `database\tags.yaml` in Step 0 may be written.

- Save the file.

- Display the saved file path and a short preview (the appended section).


# Translation Rules

- Translate Chinese / Japanese / Korean prose into clear, concise English.
- Keep terms in English when they are already English in the source (e.g., `pipeline`, `PR`, `pipeline branch`).
- Do not invent details.
  If something is ambiguous, render it literally.
- Preserve list structure, line breaks between paragraphs, and inline emphasis.
