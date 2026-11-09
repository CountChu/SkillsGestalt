# Run Data Rules

> [[ASD-STE100_ISSUE9.pdf]]  `2026-11-06`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-11-06`  `c612bdfa1ea7`

> This file is in ASD-STE100 Simplified Technical English (STE), Issue 9.
> Technical words: agent, analysis, app, canonical skill invocation, checkpoint, clock, command, commit, data file, definition, design document, directory, efficiency, epoch, field, file, folder, format, git, handoff, handoff file, handoff files, heading, language, list, metadata, minute, model, noise, path, root, rounding, run, scratchpad, script, second, section, session, skill, temp dir, timestamp, title, untracked file, user, vault, wiki, wildcard, working data, working dir, workspace.

These rules tell where a run of a skill writes its data, and when to remove this data.
A run writes two types of data:

- **The working data of a run** gives the outputs of each step to the subsequent steps.
  It also helps the run to complete its work, and to continue after it stops.
  After the run, no person and no skill must read it.
- **The last outputs** are the data that a person, a different skill or a subsequent analysis reads after the run.

## The Number of a Run

- **Each run has a number, `{yymmdd}.{N}`.**
  `{yymmdd}` is the date when the run starts.
  `{N}` is the sequence number of the run of this skill on that date, and it starts at 1.
- **Step 0 gets the number.**
  It finds the largest `{N}` of the date in `database\skill-runs\{skill}\`, and adds 1.
  Then, it writes the run record of the run immediately, thus a different run cannot get the same number.
  This first run record has `result: stopped` and `stopped_at: step_0`.
- **The Working Dir, the run record and the handoff file of a run use the same number.**
  Thus, you can find the data of one run in each directory, and the files do not refer to each other.

## The Working Data of a Run

### The Working Dir

- **The Working Dir of a run contains all the working data of the run.**
  It is one of these two directories, at the root of the workspace:
  - The **Temp Dir**, `temp\{skill}\{yymmdd}.{N}\`.
  - The **Checkpoint Dir**, `checkpoints\{skill}\{yymmdd}.{N}\`.
- **The two directories have the same structure.**
  Each directory is always the same.
  You cannot set it in `config.yaml`.
  The two directories are in `.gitignore`, thus no file in them goes into a commit.
- **The person who writes a skill selects one of the two directories.**
  The CONFIGURATION section of the skill gives it.
  A run of the skill does not use the other directory.
  After its CONFIGURATION section, the skill uses the name Working Dir.
- **If the Working Dir is not there, create it.**

### Step Files

- **Each step writes its outputs in its step file, `step_{N}.yaml`, in the Working Dir**, for example `step_0.yaml` and `step_1.yaml`.
  A subsequent step reads these outputs from the step file, and does not calculate them again.
  Also, `run step N` reads them when it starts a run again from step N.
- **A step file contains only the outputs of its step.**
  It does not contain the title of the step or the time.
  The run record contains them.
- **The data files of a run are also in its Working Dir.**
  Each skill gives the name of each data file in its MUST FOLLOW section.

### Temporary Files

- **Put each temporary file of a run in its Working Dir.**
  A temporary file is each item that a run writes, other than a step file, a data file or an output of its skill.
  Examples are a temporary script that does a test or a check, and the output of a command that the run keeps.
  Other examples are a JSON file that the run uses before it writes its outputs, and a temporary copy of a directory for a test.
- **The name of a file in the Working Dir tells the function of the file**, as in `facts.yaml`.
  The name does not start with the name of the skill, because the path of the Working Dir gives the skill and the run.
  Thus, two runs cannot use the same file.
- **A script that a step runs also puts its temporary files in the Working Dir of the run.**
  The step gives the Run Number to the script, and the script makes the path of the Working Dir.
  This rule applies to each language.
  Do not use the temporary directory of the system, for example `tempfile` in Python or `os.tmpdir()` in Node.
- **A script that a step runs uses the root of the workspace that the skill runs in.**
  If the command of the step gives the root, the script uses that root.
  If not, the root is the nearest directory, from the current directory up, that has a `config.yaml` with `skillGroups`.
  The script does not find the root from the location of its own file.
  A workspace can use a skill group of a different workspace, and then the `config.yaml` above the script is the `config.yaml` of the different workspace.
- **A script that does not operate in a run of a skill puts its temporary files in `temp\`.**
  The name of its directory starts with the name of the script, for example `temp\publish-gestalt-index-{pid}\`.
  The script removes this directory before it stops.

### The Removal of the Working Dir

- **The skill does not remove the Working Dir, or a file in it.**
  A run that stops before it completes its work keeps its files in the Working Dir.
  These files show how much of the work it did.
- **Each item in `temp\` and `checkpoints\` is safe to remove manually, when you want.**
  If you remove an item, give its full name.
  Do not use a wildcard, because a wildcard can also agree with the files of a different run.

## The Last Outputs

### The Run Record in `database\skill-runs\`

- **The run record of a run is `database\skill-runs\{skill}\{yymmdd}.{N}.yaml`.**
  It records the time that each step of the run used, and the model that operated the step.
  Thus, you can do an analysis of the efficiency of a skill after many runs.
  Do not remove it.
- **The run record does not refer to the step files.**
  It has the same number as the Working Dir.
- **The run record has these fields:**
  - `skill`: the name of the skill.
  - `run`: the number of the run, `{yymmdd}.{N}`.
  - `prompt`: the canonical skill invocation, which is `{USER_PROMPT}` in [report-md-rules.md](report-md-rules.md).
  - `result`: `completed` when the run completes its last step, or `stopped` before that.
  - `stopped_at`: only when `result` is `stopped`, the step that did not complete, for example `step_3`.
- **When a step adds its item to the run record, it also writes `stopped_at` again.**
  If the step completes and it is not the last step, `stopped_at` is the next step.
  If the run stops in the step, `stopped_at` is this step.
  The last step writes `result: completed` and removes `stopped_at`.
  Thus, if a run stops before its last step and does not write its result, its run record tells the step where it stopped.
  - `steps`: a list, with one item for each step that started.
- **Each item of `steps` has these fields:**
  - `step`: the number of the step.
  - `title`: the heading of the step in the skill definition, for example `Warmup`.
  - `model`: the AI model that operated the step.
  - `time`: `begin` and `end`, in the format `yyyy-MM-dd HH:mm:ss`, and `taken`, in the format `Xm Ys`.
- **Read the value of `time.begin` from the local system clock when each step starts.**
  Read the value of `time.end` from the same clock when the step stops.
  In PowerShell, use `Get-Date -Format "yyyy-MM-dd HH:mm:ss"`.
  On macOS/Linux, use `date '+%Y-%m-%d %H:%M:%S'`.
- **Do not use estimates or approximate timestamps for `time.begin` and `time.end`.**
  Also, do not get these timestamps from the metadata of a file after the step.
  A time that you get again from other data is false, because you did not measure it.
- **Calculate the value of `time.taken` as `end - begin`.**
  For example:
  - In PowerShell, use `$ts = (Get-Date $end) - (Get-Date $begin); "{0}m {1}s" -f [math]::Floor($ts.TotalMinutes), $ts.Seconds`.
  - On macOS/Linux, calculate the difference between the two times in epoch seconds.
    Then write the difference in the format of `taken`.
- **For `time.taken`, count only the full minutes.**
  Do not use rounding, because rounding can make the number of minutes too large.
  Do not hard-code the value of `time.taken`.
  Do not use an estimate of this value.
- **When `run step N` starts a run again, add the steps that it does to the list of `steps`.**
  Then, write the new `result`.

### Handoff Files in `handoff\`

- **A handoff file is data that a run makes for a different skill.**
  The run makes it again each time, and the different skill reads it.
- **The handoff file of a run is `handoff\{skill}\{yymmdd}.{N}.md`, at the root of the workspace.**
  `{skill}` is the skill that writes the file.
  Each handoff file is a Markdown file.
  The directory is in `.gitignore`.
- **The skill that writes a handoff file gives it in its MUST FOLLOW section.**
  The skill that reads the file gives the skill that writes it.
- **The skill that reads a handoff file reads the file that the user gives.**
  If the user does not give a file, it reads the file with the largest number.
  It tells which file it read.
- **The skill does not remove a handoff file.**
  Remove it manually, when you want.

### Shared Data in `database\`

- **`database\` at the root of the workspace contains data that many skills use, and that collects over many runs**, for example `database\tags.yaml`.
  A run adds to this data, or changes it.
  It does not make it again each time.
  Data that a run makes again each time for a different skill is a handoff file.
- **The skill that writes a file in `database\` gives the name of the file in its MUST FOLLOW section.**
- **Do not remove the data in `database\`.**
  The directory is in `.gitignore`.

### MD Reports in the Vault

- **The MD report of a run is in the wiki vault, in the folder of its skill.**
  A person reads it.
  [report-md-rules.md](report-md-rules.md) tells how to write it.
- **The `Run record` field of the MD report gives the path of the run record of the run.**

## Locations That You Must Not Use

- **Do not use the scratchpad of the agent.**
  For example, each session of Claude Code has its own scratchpad.
  A different session, a different agent and a script cannot find it.
- **Do not use the temporary directory of the system.**
  Use the Working Dir.
  There is one exception: a test that must not find the files of the workspace, for example its `config.yaml`.
  Such a test runs in the temporary directory of the system, because that directory is not in the workspace.
  The script removes the directory when the test stops, also after an error.
- **Do not put the data of a run in the root of the workspace.**
  A file that a run writes there is an untracked file, *but git does not ignore it*.
  Thus, it shows as noise in `git status`.
  Also, if you use `git clean -fd` after a commit, it removes the file, and does not get your approval first.
  At the same time, `git clean -fd` removes all the files of the other runs that are adjacent to it.
- **Do not put the data of a run adjacent to its source.**
  Use the Working Dir for all the working data of a run.

## Directories That These Rules Do Not Control

**The `temp\` directory of an app is a different directory.**
An app can have a `temp\` directory for the data that one of its stages gives to the next stage.
This directory is a part of the app.
The design document of the app tells about it.
These rules do not apply to it.

**Also, `__pycache__` is not a temporary file of a run.**
When you operate a script in its directory, Python makes `__pycache__` as a side effect.
Also, git ignores it.
The removal of `__pycache__` is optional.
