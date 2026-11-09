---
name: write-note-tags
description: Adds one or more tags to a specific section of a daily note file in wiki/write-note/, and merges them into the file-level Tags header.
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

- **Run record** — `database\skill-runs\write-note-tags\{yymmdd}.{N}.yaml`.
- **Note file** — `{wikiDir}\write-note\note-{yyMMdd}-{day}.md`, that the prompt gives.
  Steps 2 and 3 add the tags to one section and to the Tags field.

# MUST FOLLOW

- Must run workflow step by step, and display each step number.
- This skill only edits the local note Markdown file.
  It must not call any ADO write API.
- Tag values must be validated against `database/tags.yaml` before being written.
- Obey [run-data-rules.md](skill-groups/common/rules/run-data-rules.md) for the Run Number and the run record of a run.
- **Before the skill stops, show the paths of the note file and of the run record.**
  Show the path of the note file only if the run wrote it.
  Write the path of the run record as a Markdown link that starts at the workspace, with the forward slash as the separator: `[{yymmdd}.{N}.yaml](database/skill-runs/write-note-tags/{yymmdd}.{N}.yaml)`.
  Do this for each run, also for a run that stops before Step 3.
- A run that stops before Step 3 ends writes `result: stopped` and `stopped_at` in its run record.

# Prompt Examples

## Prompt 1

```
/write-note-tags
note-260608-Mo
section: 1
tags: new-skill
```

## Prompt 2

```
/write-note-tags
note-260603-We
section: 1
tags: new-skill, 2605-kane-pipe2
```

## Prompt 3

```
Tag section 2 of note-260608-Mo with new-skill.
```


# Workflow

## Step 0 - Warmup

- Read the workspace config [config.yaml](config.yaml) at the workspace root and resolve:
  - **`wikiDir`**: the Obsidian vault root — every wiki file this skill reads or writes lives under `{wikiDir}\`.
  - Substitute the resolved value wherever `{wikiDir}` appears in the steps below (including in commands).
  - If `config.yaml` is missing or `wikiDir` is absent, stop and ask the user.

- Parse the user's prompt for:
  - **Note name**: e.g. `note-260608-Mo` (the trailing `-<day>` — `Su`/`Mo`/`Tu`/`We`/`Th`/`Fr`/`Sa` — may be omitted, e.g. `note-260608`).
    Resolve to `{wikiDir}/write-note/<note-name>.md`; if that exact file does not exist, glob `{wikiDir}/write-note/<note-name>*.md` (notes are named `note-yyMMdd-<day>.md`) and use the single match.
  - **Section**: a 1-based section number (e.g. `2`).
    If missing, ask the user.
  - **Tags**: one or more tag values separated by comma or whitespace (e.g. `new-skill`, `new-skill, tune-skill`).
    If missing, ask the user.

- If no note file resolves (neither exact nor glob match), abort and tell the user; if the glob matches multiple files, ask the user which one.

- Validate every tag value against `database/tags.yaml`.
  If any tag is not listed there, warn the user and ask for confirmation before proceeding.

- Save the parsed inputs (note path, section, tag list) for use in later steps.

- Save the canonical skill invocation, thus the run record can store it as its prompt.

- Get the Run Number, as run-data-rules.md tells, and write the run record of the run.

- Add this step to the run record.


## Step 1 - Locate Section

- Read the note Markdown file.

- Find the heading line that matches `^## <section>\. <Title>` exactly.
  If not found, abort and report `Section <N> not found in <note-path>`.

- Capture the section title (without the `## N. ` prefix) and the line range from the heading to the next `## ` heading or EOF.

- Display a short table: section number | section title | tags to add.

- Add this step to the run record.


## Step 2 - Add Tags to Section

- Build the section tag line as `>Tags: <tag1>, <tag2>, ...` (blockquote-prefixed with `>`, comma + space separated, in the order requested).

- Placement: directly under the section title heading (`## <N>. <Title>`).
  - If the heading is immediately followed by a blockquote block (one or more `>`-prefixed lines, e.g. `>Task: ...`), add/merge the `>Tags:` line as the last line of that blockquote block.
  - Otherwise, insert the `>Tags:` line right after the heading line (skipping a single blank line if the heading is followed by one), so it sits at the top of the section body.

- Idempotency:
  - If a line matching `^>?\s*Tags:\s*` already exists anywhere in the section body, merge the new tags into the existing list (preserve original order, append only tags not already listed) and rewrite it in the `>Tags:` form.
    Skip writing if the merged list is identical and already in `>Tags:` form.
  - If no such line exists, insert a new `>Tags:` line per the Placement rule above.

- Display:
  - The note file path.
  - A diff-style preview of the inserted/updated `>Tags:` line.

- Add this step to the run record.


## Step 3 - Merge Tags into File Header

- Read the file's header field line that matches `^-\s+\*?\*?Tags\*?\*?:\s*` (supports both `- Tags:` and `- **Tags**:` styles).

- If the field exists:
  - Merge the new tags into the existing comma-separated list (preserve original order, append only tags not already listed).
  - Skip writing if the merged list is identical to the existing one.

- If the field does not exist:
  - Insert a new `- Tags: <tag1>, <tag2>, ...` line immediately after the existing header bullet block (after the last `- **<Field>**:` / `- <Field>:` line in the file's top section, before the first `## ` heading).
  - Match the punctuation style (`- **Tags**:` vs `- Tags:`) of the surrounding header bullets in the same file.

- Do not modify the `Updated` or `Created` header fields.

- Save the file.

- Display:
  - The new value of the file-level `Tags` header.

- Add this step to the run record, and write `result: completed`, because it is the last step.
