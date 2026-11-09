---
name: write-topic
description: The skill creates or appends a topic Markdown file in wiki/write-topic, using English by default or Traditional Chinese when the prompt includes a standalone `Chinese` language selector.
---

# TERMINOLOGY

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

- **Topic file** — the wiki page `<Title>.md` that this skill creates or appends.
- **Forbidden title character** — the character `#`, `^`, `[`, `]` or `|`.
  The title is the name of the topic file, and an Obsidian link cannot find a file that has one of these characters in its name.

# CONFIGURATION

The inputs and tools, which the run reads or runs:

- **Workspace configuration** — the [config.yaml](config.yaml) at the root of the workspace.
- **Images directory** — `{wikiDir}\images\`, where Step 1 looks for each image that the source refers to.

The working data of a run, which no person and no skill reads after the run:

- **Working Dir**: the Checkpoint Dir, `checkpoints\write-topic\{yymmdd}.{N}\`.

The last outputs, which a person, a different skill or a subsequent analysis reads:

- **Run record**: `database\skill-runs\write-topic\{yymmdd}.{N}.yaml`.
- **Topic file**: `{wikiDir}\write-topic\<Title>.md`.
  `wikiDir` comes from the [config.yaml](config.yaml) of the workspace, and Step 0 resolves it.

# MUST FOLLOW

- Must run workflow step by step, and display each step number.
- The topic filename is `<Title>.md` (verbatim title with spaces, e.g., `TSG.md`, `Agent Feature in Teams.md`).
  The full path is `{wikiDir}\write-topic\<Title>.md`.
- Never write a topic file whose title contains a forbidden title character.
  Do not change the title yourself: Step 0 asks the user for a different title.
- The topic file is a wiki page, not an MD report of one run.
  It collects sections over many runs, so its header has no `Run record` and no `Prompt` field, and a run never removes its existing content.
- Follow [run-data-rules.md](skill-groups/common/rules/run-data-rules.md) for the Run Number, the step files, the run record and the Working Dir of a run.
- **Before the skill stops, show the paths of the topic file and of the run record.**
  Show only the two paths as clickable Markdown links, not as inline code or plain text.
  - For the **topic file**, use `[<Title>.md](obsidian://open?vault={vaultName}&file=write-topic/<Title>.md)`, where `{vaultName}` is the last path segment of `wikiDir`.
    URL-encode spaces in the `file=` value (` ` -> `%20`).
  - For the **run record**, use `[{yymmdd}.{N}.yaml](database/skill-runs/write-topic/{yymmdd}.{N}.yaml)`.
  - Do this for each run, also for a run that stops early.
- The output language defaults to English.
  A standalone `Chinese` line immediately after `/write-topic` selects Traditional Chinese for the new content instead.
- Translate prose into the selected output language.
  Preserve URLs, code, command names, identifiers, and proper nouns verbatim.
- Preserve the meaning faithfully.
  Do not paraphrase away technical detail.

# Prompt Examples

## Prompt 1

```
/write-topic
title: TSG
content: TSG stands for Troubleshooting Guide.
```

## Prompt 2

```
/write-topic
Chinese
title: 疑難排解指南
content: 這是一份供維運團隊使用的結構化操作手冊。
```


# Workflow

## Step 0 - Warmup

- Read the workspace config [config.yaml](config.yaml) at the workspace root and resolve:
  - **`wikiDir`**: the Obsidian vault root — every wiki file this skill reads or writes lives under `{wikiDir}\`.
  - Substitute the resolved value wherever `{wikiDir}` appears in the steps below (including in commands).
  - If `config.yaml` is missing or `wikiDir` is absent, stop and ask the user.

- Run `.venv` first.

- Parse the user's prompt for required inputs:
  - **Output language**: Inspect the first non-empty line after `/write-topic`.
    If it is the standalone word `Chinese` (case-insensitive), use Traditional Chinese.
    If it is `English` or no language selector is present, use English.
    Treat the selector as control metadata and do not include it in the topic content.
  - **Title**: Topic title (free-form, e.g., `TSG`, `Agent Feature in Teams`).
    Used as both the H1 and the file name.
  - **Source**: Original source URL or document reference (e.g., ADO wiki link).
    Optional.
  - **Author**: Original author of the source content.
    Optional.
  - **Body**: The raw topic content (may contain non-English characters, URLs, lists, code blocks).
    Accept either `content:` or `body:` as the field label.
  - **Topics directory**: Defaults to `{wikiDir}\write-topic`.
    Use the user-supplied path if provided.

- If the title or body is missing, ask the user.

- If the title contains a forbidden title character, do not continue with this title.
  Name each forbidden title character that the title contains, and ask the user for a title without one.
  Offer the title with these characters removed, with single spaces between words and no space at its ends.
  Check the title of the answer in the same way, and use it as the Title in the rest of the run.
  If the user gives no title without a forbidden title character, stop the run: it writes no file, thus it has no path to show.

- Ensure the topics directory exists.
  Create it if not.

- Get the current local date-time for header timestamps.
  In PowerShell, use `Get-Date -Format "yyyy-MM-dd HH:mm"`.
  On macOS/Linux, use `date '+%Y-%m-%d %H:%M'`.

- Save the canonical skill invocation (the `/write-topic` line and the fields that this step parses, without any wrapper text around them).

- Get the Run Number, as run-data-rules.md tells, and write the run record of the run.
  Put the canonical skill invocation into its `prompt` field.

- Save `step_0.yaml`, with: the output language, title, source, author, body, topics directory and the header date-time.
  Add this step to the run record.


## Step 1 - Create or Append Topic File

- Read the inputs from `step_0.yaml`.

- Target file: `<topics-dir>\<Title>.md` (e.g., `{wikiDir}\write-topic\TSG.md`).

- If the file does not exist, create it with the following header:
  - **Title**: `# <Title>` (e.g., `# TSG`).
  - **Header fields** (bullet list immediately after the title):
    - **Skill**: write-topic
    - **Source**: Markdown link to the source URL (or omit if no source).
    - **Author**: Source author name (or omit if no author).
    - **Created**: current date-time
    - **Updated**: current date-time
  - A horizontal rule (`---`) separating the header from the body.

- If the file already exists:
  - Preserve the original `Created` value.
  - Update `Updated` to the current date-time.
  - Append the new section at the end (under a new numbered `##` heading derived from the user prompt — see **Section numbering** below — or merge into an existing matching section if the user explicitly says so).

- Body conventions:
  - Translate prose into the selected output language: clear, concise English by default, or Traditional Chinese when `Chinese` was selected.
  - Apply the selected language only to the newly created or appended content.
    Do not translate or otherwise rewrite existing topic content.
  - URLs: keep as bare links wrapped in angle brackets `<https://...>` on their own line, unless the user already supplied a Markdown link.
  - Code, identifiers, file paths, command names: wrap in backticks.
  - Preserve list structure, numbered steps, code blocks, and inline emphasis from the source.
  - For images referenced in the source, use Obsidian-style embeds (`![[image-name.png]]`) only if the image is already in `{wikiDir}\images\`; otherwise note the image with a placeholder and ask the user to attach.

- Section numbering:
  - Number every top-level `##` body section sequentially with an `N. ` prefix, in document order: `## 1. <Heading>`, `## 2. <Heading>`, ….
  - Do **not** number `###` (or deeper) subsections, the `# <Title>` H1, or the header / `Reference` block.
  - When appending, give the new `##` section the next number in sequence.
    If sections are inserted, removed, or reordered, renumber all top-level `##` sections so they stay contiguous starting at `1`.

- Auto-add references:
  - If the topic content was moved or copied from another wiki MD file, add a `> Reference: [<title>](<relative-path>)` blockquote line immediately after the section heading.
  - The path must be relative to the topic file's location.
  - URL-encode spaces in the link target (` ` -> `%20`); keep the display text human-readable.
  - If multiple sources apply, list each on its own `> Reference:` line.

- Save the topic file.

- Save `step_1.yaml`, with: the topic file path, whether the file was created or appended, and the heading of the new section.
  Add this step to the run record, and write `result: completed`, because it is the last step.

- Display a short preview (the new or appended section), and then the paths of the topic file and of the run record, as MUST FOLLOW tells.


# Output Language Rules

- **English (default)**: Translate non-English prose, including Chinese, Japanese, and Korean, into clear, concise English.
- **Chinese**: Write prose in Traditional Chinese.
  Preserve Traditional Chinese prose and translate other explanatory prose into Traditional Chinese.
- Keep terms in English when they are already English in the source (e.g., `pipeline`, `PR`, `BIOS`, `TSG`).
- Keep structural metadata labels such as `Skill`, `Source`, `Author`, `Created`, `Updated`, and `Reference` in English in both output languages.
- Do not invent details.
  If something is ambiguous, render it literally.
- Preserve list structure, line breaks between paragraphs, and inline emphasis.
