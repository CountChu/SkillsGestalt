---
name: add-tags-note
description: >-
  Scans each section of a daily note in wiki/write-note/ for referenced notes (markdown links
  to wiki .md files, e.g. on Note:/Notes:/Result: lines) and the section's Tags, then
  adds/merges each section's tags (validated against database/tags.yaml) into the Tags header
  of every note it references.
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
- **Daily note** — `{wikiDir}\write-note\<note-name>.md`, that the prompt gives.
  Step 0 finds it, and Step 1 reads its sections.

The last outputs, which a person, a different skill or a subsequent analysis reads:

- **Run record** — `database\skill-runs\add-tags-note\{yymmdd}.{N}.yaml`.
- **Referenced notes** — the wiki Markdown files that the sections of the daily note refer to, in `{wikiDir}\`.
  Step 2 merges the tags of the sections into their Tags field.

# MUST FOLLOW

- Must run workflow step by step, and display each step number.
- Obey [run-data-rules.md](skill-groups/common/rules/run-data-rules.md) for the Run Number and the run record of a run.
- If the skill stops before Step 2, write `result: stopped` and `stopped_at` (the step that did not complete, for example `step_1`) into the run record.
- **Before the skill stops, show the path of the run record.**
  Show only the path, and do not show the contents.
  Write the path as a Markdown link that opens with a click, with a link target that starts at the workspace and the forward slash as the separator.
  For example: `[{yymmdd}.{N}.yaml](database/skill-runs/add-tags-note/{yymmdd}.{N}.yaml)`.
  Do not write it as inline code or as plain text.
  Do this for each run that has a run record, also when the skill stops early.
- This skill only edits local Markdown files.
  It must not call any ADO write API.
- Every tag value MUST be validated against `database/tags.yaml` before being written.
- Do NOT modify the `Created` or `Updated` header fields of the referenced notes.

# Prompt Examples

## Prompt 1

```
/add-tags-note
note-260709-Th
```

## Prompt 2

```
/add-tags-note
note-260709
```

## Prompt 3

```
Propagate each section's tags into the notes referenced by note-260709-Th.
```


# Workflow

## Step 0 - Warmup

- Read the workspace config [config.yaml](config.yaml) at the workspace root and resolve:
  - **`wikiDir`**: the Obsidian vault root — every wiki file this skill reads or writes lives under `{wikiDir}\`.
  - Substitute the resolved value wherever `{wikiDir}` appears in the steps below (including in commands).
  - If `config.yaml` is missing or `wikiDir` is absent, stop and ask the user.

- Parse the user's prompt for:
  - **Note name**: e.g. `note-260709-Th` (the trailing `-<day>` — `Su`/`Mo`/`Tu`/`We`/`Th`/`Fr`/`Sa` — may be omitted, e.g. `note-260709`).
    Resolve to `{wikiDir}\write-note\<note-name>.md`; if that exact file does not exist, glob `{wikiDir}\write-note\<note-name>*.md` (notes are named `note-yyMMdd-<day>.md`) and use the single match.
  - If the note name is missing, ask the user.
  - If no note file resolves (neither exact nor glob match), abort and tell the user; if the glob matches multiple files, ask the user which one.

- Save the resolved note path for use in later steps.

- Save the canonical skill invocation, thus the run record can give it in its `prompt` field.

- Get the Run Number, as run-data-rules.md tells, and write the run record of the run.

- Add this step to the run record.


## Step 1 - Scan Sections

- Read the note Markdown file.

- For each `^## <N>. <Title>` section, capture the line range (from the heading to the next `## ` heading or EOF) and collect:
  - **Referenced notes**: every markdown link in the section that targets a wiki Markdown file — `[<name>](<relative-path>.md)` — typically on a `Note:` or `Result:` line.
    `Notes:` is the legacy form of `Note:`; treat it identically.
    Resolve each `<relative-path>` relative to the note's directory (`{wikiDir}\write-note\`, so `../<dir>/<file>.md`) to an existing file.
    Ignore links that do not resolve to an existing wiki `.md` file (e.g. ADO `Task:` / `PR:` URLs).
  - **Section tags**: the tag values on the section's `Tags:` line (comma/space separated).
    Empty if the section has no `Tags:` line.

- Build and display a table: `Section #` | `Referenced note(s)` | `Section tags`.

- Add this step to the run record.

- If no section has both a referenced note and at least one tag, report "Nothing to propagate" and exit the skill.
  Before you exit, write `result: stopped` and `stopped_at: step_2` into the run record.


## Step 2 - Propagate Tags to Referenced Notes

- Build the target map: for each referenced note, take the union of the tags from every section that references it (preserve first-seen order).

- Validate every tag against `database\tags.yaml`.
  If any tag is not listed there, warn the user and ask for confirmation before writing it.

- For each target referenced note, merge its tags into the note's file-level `- **Tags**:` header:
  - If a header field matching `^-\s+\*?\*?Tags\*?\*?:\s*` exists (supports `- **Tags**:` and `- Tags:` styles), append only tags not already listed (preserve original order).
    Skip writing if the merged list is identical.
  - If the field does not exist, insert a new `- **Tags**: <tag1>, <tag2>, ...` line after the header bullet block — after the last simple `- **<Field>**:` line, before the `- **Prompt**:` line if present, else before the first `## ` heading.
    Match the surrounding `- **<Field>**:` / `- <Field>:` punctuation style of that file.
  - Do NOT modify the referenced note's `Created` or `Updated` header fields.

- Skip sections that have no referenced notes or no tags.

- Display, per referenced note: the file path and the new value of its `Tags` header.

- Add this step to the run record, and write `result: completed`, because it is the last step.
