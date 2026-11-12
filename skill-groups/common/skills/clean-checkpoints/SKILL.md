---
name: clean-checkpoints
description: Finds the old items of checkpoints\ when checkpoints\ is larger than a threshold, shows them to the user, and moves only the items that the user confirms to the recycle bin. An item is each folder or file directly in checkpoints\{skill}\; it is old when its newest file is older than the keep period. An item always stays when its skill folder is in the keep list of config.yaml, when its name or a number of 7 or more digits in its name is in an open task, or when it is in checkpoints\chores\. It never removes an item permanently.
---

# TERMINOLOGY

Each skill uses these terms with the same definition.

- **`run step N`** — a selector at the end of a prompt, which identifies one step.
- **Run Number** — the number of one run, `{yymmdd}.{N}`.
  `{N}` is the sequence number of the run of this skill on that date, and it starts at 1.
- **Working Dir** — the directory for one run, which holds all the working data of the run: its step files, its data files and its temporary files.
  In this skill, it is the Temp Dir, and **CONFIGURATION** gives it.
  The skill does not remove it.
- **Temp Dir** — a Working Dir in `temp\` at the root of the workspace.
- **Step file** — the `step_{N}.yaml` in the Working Dir.
  Each step writes its outputs there.
  Thus, a subsequent step reads these outputs, and does not calculate them again.
- **Run record** — the file that records the time and the model of each step of one run.
  The analysis of the efficiency of a skill uses it.

# DEDICATED TERMINOLOGY

The terms that only this skill uses.

- **Item** — one folder or one file directly in `checkpoints\{skill}\`, or one file directly in `checkpoints\`.
  The date of an item is the date of its newest file.
  The date of an empty folder is the date of the folder.
- **Threshold** — the size of `checkpoints\` above which the skill finds old items: `cleanCheckpoints.maxSizeGB` in `config.yaml`, 10 GB if it is not there.
- **Keep period** — the number of days, `cleanCheckpoints.keepDays` in `config.yaml`, 60 if it is not there.
  An item is old when its date is more than this number of days before today.
- **Keep list** — the names of the skill folders in `checkpoints\` that the skill never cleans, `cleanCheckpoints.keep` in `config.yaml`, empty if it is not there.
  A different skill reads the data in these folders after the run that wrote it.
- **Open task** — a task with ⬜ or 🔄 in the task summary table, `taskSummary` in `config.yaml`, whose file is in `tasksDir`.
- **Clean item** — an item that the script lists for removal: it is old, its skill folder is not in the keep list, it is not in `checkpoints\chores\`, and no open task contains its name or a number of 7 or more digits in its name.
  The skill does not use a number of 6 digits, because such a number is frequently a date, `yymmdd`, that the names of many items contain.
  Each other item is a kept item, and the script gives the reason.
- **Confirmed list** — the clean items that the user agrees to move to the recycle bin in Step 2.

# CONFIGURATION

The values that this skill uses in a run.

The inputs and tools, which the run reads or runs:

- **Workspace configuration** — the [config.yaml](config.yaml) at the root of the workspace: `skillGroups`, the `cleanCheckpoints` block, `tasksDir` and `taskSummary`.
- **Checkpoints** — `checkpoints\` at the root of the workspace.
- **Script** — `{skillGroups.common}\skills\clean-checkpoints\scripts\clean_checkpoints.py`.
  It uses only the Python standard library.
  On macOS and Linux, the `recycle` command also needs the Python package `send2trash`.

The working data of a run, which no person and no skill reads after the run:

- **Working Dir** — the Temp Dir, `temp\clean-checkpoints\{yymmdd}.{N}\`.
  It holds the step files, `items.yaml` from Step 1 and `recycled.yaml` from Step 3.

The last outputs, which a person, a different skill or a subsequent analysis reads:

- **Run record** — `database\skill-runs\clean-checkpoints\{yymmdd}.{N}.yaml`.

# MUST FOLLOW

- Run the workflow one step at a time, and show the number of each step.
- **Honor a `run step N` selector**: run Step N, and then stop.
  Read the output of each previous step from its step file.
  Do not run a subsequent step.
- Obey [run-data-rules.md](skill-groups/common/rules/run-data-rules.md) for the Run Number, the step files, the run record and the Working Dir of a run.
- **Each file in the Working Dir has one writer step only.**
  The step that makes a data file writes the full file, and only that step changes it.
  A subsequent step that makes a decision writes it into its own step file.
  It does not add, change or remove a key in a file that a different step wrote.
  This rule applies also when the decision of the subsequent step replaces the data in that file.
- If more than one step writes into a data file, the first step erases the data of the other steps when it runs again.
  For example, a `run step 1` writes the full file again.
  This erases the results of all the subsequent steps, and no message tells you.
- **Do not remove an item permanently, and do not remove an item that the user did not confirm.**
  Only the script of Step 3 moves items, and it moves them to the recycle bin.
  Do not remove an item with a different command, also when the script cannot move it.
- **Do not change `checkpoints\` in Step 0, Step 1 or Step 2.**
- **Before the skill stops, show the path of the run record.**
  Show only the path, and do not show its contents.
  Write the path as a Markdown link that opens with a click.
  Do not write it as inline code or as plain text.
  Use a link target that starts at the workspace.
  Use the forward slash as the separator in it.
  For example: `[{yymmdd}.{N}.yaml](database/skill-runs/clean-checkpoints/{yymmdd}.{N}.yaml)`.
  Do this for each run, and also for a run of only one step, for example `run step 0`.

# Prompt Examples


## Prompt 1

```
/clean-checkpoints
```

## Prompt 2

```
/clean-checkpoints
run step 1
```

## Prompt 3

```
checkpoints\ is too large. Find the old items and clean them.
```


# Workflow

## Step 0 - Warmup

- Find `{python}`, the Python of the workspace.
  If the workspace has a `.venv` at its root, use `.venv/bin/python` on macOS and Linux, and `.venv\Scripts\python.exe` on Windows.
  If not, use `python`.
  The script uses only the Python standard library.

- Read [config.yaml](config.yaml), the configuration file at the root of the workspace, and find these values:
  - **`skillGroups`**: the map from the name of a group to the root of its skills.
    The directory of this skill is `{skillGroups.common}\skills\clean-checkpoints\`.
  - **`cleanCheckpoints`**: the threshold, the keep period and the keep list.
    If the block or one of its keys is not there, the script uses the default.
  - **`tasksDir`** and **`taskSummary`**: the open tasks.
    If one of them is not there, the script does not look for items in open tasks, and it writes the cause in its output.
  - Replace each `{skillGroups.common}` in the steps that follow with the value that you found.
    Do this also in the commands.
  - If `config.yaml` is missing, or if `skillGroups` is not in it, stop, and tell the user to supply it.

- Before you run the workflow, make sure that this script is there:
  - `{skillGroups.common}\skills\clean-checkpoints\scripts\clean_checkpoints.py`

- The prompt agrees with one of the examples in **Prompt Examples**.
  It has no input, other than a `run step N` selector.

- Save the canonical skill invocation, thus the subsequent steps can refer to it.

- Get the Run Number, as run-data-rules.md tells, and write the run record of the run.

- Save `step_0.yaml`, with the Run Number and the values of `cleanCheckpoints`, `tasksDir` and `taskSummary` that you found.
  Add this step to the run record.


## Step 1 - List the items

- Run the `list` command of the script from the root of the workspace, with the Run Number.
  - Example: `{python} {skillGroups.common}\skills\clean-checkpoints\scripts\clean_checkpoints.py list --run {yymmdd}.{N}`

- The script:
  1. Reads the settings from `config.yaml`, and the open tasks.
  2. Measures the size of `checkpoints\`, and the size and the date of each item.
  3. Gives each item the verdict `clean` or `keep`, with the reason.
  4. Saves the results as `items.yaml` in the Working Dir.
     The subsequent steps of the run use this data file, and it is not a step file.
- If the script stops with the exit code `2`, show its message to the user, and stop.

- Save `step_1.yaml`, with: `totalGB`, `maxSizeGB`, `overThreshold`, `cleanCount`, `cleanGB`, `openTasks`, and `defaults`, from `items.yaml`.
  Add this step to the run record.

- If `overThreshold` is `false`, tell the user the size of `checkpoints\` and the threshold, and that it is not necessary to clean it.
  Write `result: completed` in the run record, and stop.


## Step 2 - Ask the user

- Read `items.yaml`, the data file that Step 1 saved in the Working Dir.

- Show the user:
  - The size of `checkpoints\`, the threshold, the keep period and the keep list.
    Tell which values are defaults, from `defaults`.
  - If `openTasks` is `null`, the cause from `openTasksNote`: the items in open tasks are not kept, thus the user must examine each clean item.
  - A table of the clean items, with the columns **Item**, **Size**, **Newest file** and **Reason**.
    Put the largest item first.
    If there are more than 30 clean items, show the 30 largest, and one line for the other items with their number and their total size.
  - The number and the total size of the kept items, for each reason.

- If there is no clean item, tell the user that the skill moves nothing.
  Save `step_2.yaml` with `confirmed: []`, write `result: completed` in the run record, and stop.

- Ask the user one multiple-choice question: move all the clean items to the recycle bin, move only some of them, or move nothing.
  - If the user selects some, ask which items, and use only the items that the user gives.
  - Do not add an item that is not a clean item in `items.yaml`.

- Save `step_2.yaml`, with `confirmed`: the list of the paths of the confirmed list, as `items.yaml` writes them, one `- "<path>"` line for each path.
  If the user selects nothing, write `confirmed: []`.
  Add this step to the run record.

- If the confirmed list is empty, tell the user that the skill moves nothing.
  Write `result: completed` in the run record, and stop.


## Step 3 - Move to the recycle bin

- Run the `recycle` command of the script from the root of the workspace, with the Run Number.
  - Example: `{python} {skillGroups.common}\skills\clean-checkpoints\scripts\clean_checkpoints.py recycle --run {yymmdd}.{N}`

- The script:
  1. Reads the confirmed list from `step_2.yaml`.
  2. Gives each item its verdict again, because an item can change after Step 1.
     It skips each item that is not a clean item now, and gives the reason.
  3. Moves each other item to the recycle bin.
     On Windows, it uses PowerShell.
     On macOS and Linux, it uses the Python package `send2trash`.
  4. Saves the results as `recycled.yaml` in the Working Dir: the moved items, the skipped items and the failed items.
- If the script stops with the exit code `3`, there is no recycle bin that it can use, and it moved nothing.
  Tell the user to install `send2trash` in the Python of the workspace, and stop.
- If the script stops with the exit code `4`, one or more moves failed.
  Show each failed item and its cause.
  Do not remove these items in a different way.

- Save `step_3.yaml`, with: `movedCount`, `movedGB`, and the number of skipped items and of failed items, from `recycled.yaml`.
  Add this step to the run record, and write `result: completed`, because it is the last step.

- Tell the user the number and the total size of the moved items, and that they are in the recycle bin.
  Show the skipped items and the failed items, with their causes.
