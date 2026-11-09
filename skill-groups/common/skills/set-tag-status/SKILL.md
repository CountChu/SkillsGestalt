---
name: set-tag-status
description: The skill sets the status field of a tag in tags.yaml to one of the allowed values (active, done, archived, blocked, on-hold), or removes it.
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
- **Run record** — the file that records the time and the model of each step of one run.
- **MD report** — the Markdown report that the skill writes into the wiki vault, in the folder `set-tag-status`.

# CONFIGURATION

The inputs and tools, which the run reads or runs:

- **Workspace configuration** — the [config.yaml](config.yaml) at the root of the workspace.

The working data of a run, which no person and no skill reads after the run:

- **Working Dir** — the Checkpoint Dir, `checkpoints\set-tag-status\{yymmdd}.{N}\`.

The last outputs, which a person, a different skill or a subsequent analysis reads:

- **Tags file** — `database\tags.yaml`.
- **Run record** — `database\skill-runs\set-tag-status\{yymmdd}.{N}.yaml`.
- **MD report** — `{wikiDir}\set-tag-status\set-tag-status-{yymmdd}.md`.
  `wikiDir` comes from the [config.yaml](config.yaml) of the workspace, and Step 0 finds its value.
  Do not hard-code the root of the wiki.

# MUST FOLLOW

- Must run workflow step by step, and display each step number.
- The report filename is `set-tag-status-{yymmdd}`.
- Follow [report-md-rules.md](skill-groups/common/rules/report-md-rules.md) to create or update the MD report file.
- Obey [run-data-rules.md](skill-groups/common/rules/run-data-rules.md) for the Run Number, the step files, the run record and the Working Dir of a run.
- The skill writes `database\tags.yaml`, at the root of the workspace.
  It is shared data: the skill changes the `status` field of one tag, and does not make the file again.
- **Before the skill stops, show the paths of the MD report and of the run record.**
  Show only the two paths, and do not show their contents.
  Write the two paths as Markdown links that open with a click.
  - For the **MD report**, use an `obsidian://open?vault={vaultName}&file=<vault-relative-path>` URI.
    For example: `[set-tag-status-{yymmdd}.md](obsidian://open?vault={vaultName}&file=set-tag-status/set-tag-status-{yymmdd}.md)`.
  - For the **run record**, use a link target that starts at the workspace, with the forward slash as the separator.
    For example: `[{yymmdd}.{N}.yaml](database/skill-runs/set-tag-status/{yymmdd}.{N}.yaml)`.
  - If the run stops before Step 3, it has no MD report: show only the path of the run record.

# Prompt Examples

## Prompt 1

```
/set-tag-status
```

## Prompt 2

```
/set-tag-status 2605-run-pr active
```

## Prompt 3

```
Set the tag 2605-clear-cmos status to done
```


# Workflow

## Step 0 - Warmup

- Read [config.yaml](config.yaml), the configuration file at the root of the workspace, and find these values:
  - **`wikiDir`**: the root of the MD reports.
    The reports of this skill go into `{wikiDir}\set-tag-status\`.
  - **`vaultName`**: the last part of the path of `wikiDir`, for example `MyVault`.
    It is the name of the Obsidian vault, and the `obsidian://` links use it.
  - Replace each `{wikiDir}` and `{vaultName}` in the steps that follow with the value that you found.
  - If `config.yaml` is missing, or if `wikiDir` is not in it, stop, and tell the user to supply it.

- Parse the user's prompt for:
  - **Tag** (optional): The tag name to update (e.g., `2605-run-pr`).
  - **Status** (optional): One of the allowed values below.

- Save the canonical skill invocation, thus the subsequent steps and the MD report can refer to it.

- Get the Run Number, as run-data-rules.md tells, and write the run record of the run.

- Verify the tag exists in `database/tags.yaml`.
  If provided but not found, warn the user, write `result: stopped` and `stopped_at: step_0` in the run record, and stop.

- Save `step_0.yaml`, with: the parsed tag and status (empty when the prompt does not give them).
  Add this step to the run record.


## Step 1 - Select Tag and Status

- If the tag name is missing, read `database/tags.yaml` and display all tags with their current status in a table, then ask the user to pick one:

  | # | Tag | Status |
  |---|-----|--------|
  | 1 | ... | ...    |

- If the status is missing, ask the user to select one:

  | # | Status | Description |
  |---|--------|-------------|
  | 1 | active | Currently in progress |
  | 2 | done | Work completed |
  | 3 | archived | No longer relevant, kept for history |
  | 4 | blocked | Waiting on something external |
  | 5 | on-hold | Paused intentionally |
  | 6 | (none) | Remove the status field entirely |

- Save `step_1.yaml`, with: the selected tag and the selected status.
  Add this step to the run record.


## Step 2 - Update Tag Status

- Read the tag and the status from `step_1.yaml`.

- Read `database/tags.yaml`.

- Find the entry matching the specified tag name.

- If the user selected `(none)`, remove the `status` line from the tag entry entirely.

- If a `status` field already exists on that entry, replace its value with the new status.

- If no `status` field exists, add `status: <value>` as a new line after the `description` field of that tag entry.

- Write the updated content back to `database/tags.yaml`.

- Display the updated tag entry:

  ```yaml
  - tag: <tag_name>
    description: <description>
    status: <new_status>
  ```

- Save `step_2.yaml`, with: the tag, its old status and its new status (empty when there is none).
  Add this step to the run record.


## Step 3 - List Tag Table

- Read `database/tags.yaml`.

- Display all tags in a table:

  | # | Tag | Status | Description |
  |---|-----|--------|-------------|
  | 1 | ... | ...    | ...         |

- Tags without a `status` field should show an empty cell.

- Save MD report file following this format.
  The **Run record** field is the path of the run record of this run.
  When the report file already exists for today, set it to the run record of this run.

  ````markdown
  # set-tag-status-{yymmdd}

  - **Skill**: set-tag-status
  - **Run record**: `database\skill-runs\set-tag-status\{yymmdd}.{N}.yaml`
  - **Created**: {YYYY-MM-DD HH:MM}
  - **Updated**: {YYYY-MM-DD HH:MM}
  - **Prompt**:
  ```
  {user prompt}
  ```

  ## Updated Tags

  ```yaml
  - tag: <tag_name>
    description: <description>
    status: <new_status>
  ```

  (Append each new update below the previous ones when the report file already exists for today.)

  ## All Tags

  | # | Tag | Status | Description |
  |---|-----|--------|-------------|
  | 1 | ... | ...    | ...         |
  ````

- Save `step_3.yaml`, with: the path of the MD report and the number of tags in the table.
  Add this step to the run record, and write `result: completed`, because it is the last step.
