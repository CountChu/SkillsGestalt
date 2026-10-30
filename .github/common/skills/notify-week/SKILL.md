---
name: notify-week
description: Set up a recurring weekly Windows reminder popup (message box) via a Scheduled Task from a given message, then verify the task is registered and report its next run time.
---

# MUST FOLLOW

- Must run workflow step by step, and display each step number.
- Each step must be self-contained and **must not forward-reference a later step** — a step may reference earlier steps, but never a step (or a later step's output section) that comes after it.
- The report filename is `notify-week-{yymmdd-hhmmss}` (e.g., `notify-week-260727-141530`).
- The YAML checkpoint file is `checkpoints\notify-week\{yymmdd}\notify-week-{yymmdd-hhmmss}.yaml` (one date subfolder per day, e.g. `checkpoints\notify-week\260727\notify-week-260727-141530.yaml`).
- Follow [report-md-rules.md](.github/common/rules/report-md-rules.md) to create or update the MD report file.
- Follow [report-yaml-rules.md](.github/common/rules/report-yaml-rules.md) to save step outputs to the YAML checkpoint file.
- The default notifications live in `.github\skills\notify-week\config.yaml` under a **`tasks:` list**; each entry has its own `taskName`, `title`, `dayOfWeek`, `timeOfDay`, and `message`.
  When the skill is invoked without an inline message (e.g. just `/notify-week`), read the list (as UTF-8, so each non-ASCII `message` is preserved) and set up **every** task in it.
  The user may instead name one or more `taskName`s in the prompt to set up only those, or pass an inline message to create a one-off reminder (which overrides the config defaults for that single run and does not modify the file).
  Register each task **independently** — its own `<task-slug>` stable folder, files, and Scheduled Task.
- The reminder files (`reminder.txt`, `title.txt`, `Show-Reminder.ps1`) must live in a **stable per-user location** — `%LOCALAPPDATA%\notify-week\<task-slug>\` — NOT in `checkpoints\` (which may be cleaned) and NOT inside the repo (so the scheduled task's script path survives repo moves/renames).
- Write `reminder.txt` / `title.txt` as **UTF-8 without BOM**.
  The popup script reads them via `[System.IO.File]::ReadAllText($path, [System.Text.UTF8Encoding]::new($false))` so non-ASCII content (e.g. Chinese) renders correctly regardless of the PowerShell host code page.
  Keep the `Show-Reminder.ps1` body ASCII-only.
- Register the task with `Register-ScheduledTask` using a **`New-ScheduledTaskPrincipal -LogonType Interactive -RunLevel Limited`** principal for the current user, so the popup appears on the interactive desktop and no admin elevation is required.
  Use `-Force` to overwrite an existing task of the same name (warn the user first).
- The reminder popup only fires **while the user is logged on** (it needs the interactive desktop).
  This is a per-user, per-machine reminder — it does not notify other people.
- When test-firing the task with `Start-ScheduledTask`, a `LastTaskResult` of `267009` (`0x00041301` = `SCHED_S_TASK_RUNNING`) is **expected** while the message box is still open — it means the popup launched, not that it failed.
- Run verification commands (`Get-ScheduledTask`, `Get-ScheduledTaskInfo`) as **single-line** commands; multi-line pasted blocks can be mangled by the shell integration.

# Prompt Examples

## Prompt 1

Set up **all** weekly reminders defined in the `tasks:` list of `.github\skills\notify-week\config.yaml` — no message needed in the prompt:

```
/notify-week
```

## Prompt 2

Set up only one configured task by naming it:

```
/notify-week notify-week-hife-sg
```


# Workflow

## Step 0 - Warmup

- Read the workspace config [config.yaml](config.yaml) at the workspace root and resolve:
  - **`wikiDir`**: the Obsidian vault root — every wiki file this skill reads or writes lives under `{wikiDir}\`.
  - Substitute the resolved value wherever `{wikiDir}` appears in the steps below (including in commands).
  - If `config.yaml` is missing or `wikiDir` is absent, stop and ask the user.

- Load `.github\skills\notify-week\config.yaml` (read as UTF-8) and read its `tasks:` list.
  Each task has `taskName`, `title`, `dayOfWeek`, `timeOfDay`, and `message`.
  Treat a missing/empty file or empty list as "no configured tasks".

- Determine the **task set** to set up this run:
  - If the prompt supplies an inline message (and/or an explicit title/day/time), build a **single ad-hoc task** from it.
    It is not written back to `config.yaml` unless the user asks.
  - Else if the prompt names one or more existing `taskName`s (or titles) from `config.yaml`, select just those.
  - Else (bare `/notify-week`), select **all** tasks in the config `tasks:` list.
  - If there is no inline message and `config.yaml` has no tasks, ask the user for the reminder text.

- For each task in the selected set, resolve its fields (prompt override → the task's `config.yaml` value → built-in default):
  - **Reminder message** (required): the popup text.
    May be multi-line and multi-language (e.g., English + 中文).
    If none can be resolved, ask the user.
  - **Title** (optional): the message-box title and basis for the task name.
    Default to the task's `title`, else `Weekly Reminder` or a short phrase derived from the message.
  - **Task name** (optional): the Scheduled Task name.
    Default to the task's `taskName`, else `notify-week-<task-slug>`, where `<task-slug>` is a lowercase, hyphenated slug of the title.
    If a task with this name already exists, warn the user and confirm overwrite before using `-Force`.
  - **Day of week** (optional): the weekly trigger day.
    Default to the task's `dayOfWeek`, else `Monday`.
  - **Time of day** (optional): the trigger time, 24h `HH:mm`.
    Default to the task's `timeOfDay`, else `09:00`.

- Save the entire user prompt text for reference in later steps.

- Capture the run's start timestamp `{yymmdd-hhmmss}` once.
  Compute the checkpoint path `checkpoints\notify-week\{yymmdd}\notify-week-{yymmdd-hhmmss}.yaml` (create the `{yymmdd}` date subfolder if it does not exist) and the report path `{wikiDir}\notify-week\notify-week-{yymmdd-hhmmss}.md`.

- For each selected task, compute its own stable reminder folder `%LOCALAPPDATA%\notify-week\<task-slug>\` and its `reminder.txt`, `title.txt`, and `Show-Reminder.ps1` paths, and record them in the checkpoint below.

- Save YAML checkpoint under `step_0` with the run timestamp, the resolved checkpoint / report paths, and the selected **task set** as a list — each item recording its `task_name`, `title`, `day_of_week`, `time_of_day`, `message`, and reminder-folder path.


## Step 1 - Create Reminder Files

- Perform Steps 1–3 for **each** task in the selected set from Step 0.
  The instructions below describe a single task (its `<task-slug>` / `<task-name>`); repeat them for every selected task.

- Create the stable reminder folder `%LOCALAPPDATA%\notify-week\<task-slug>\` if it does not exist.

- Write the message to `reminder.txt` and the title to `title.txt` in that folder, as **UTF-8 without BOM**.

- Copy the popup script `.github\skills\notify-week\scripts\Show-Reminder.ps1` into that folder (overwrite if present).
  The script reads `reminder.txt` and `title.txt` as explicit UTF-8 and shows a `System.Windows.Forms.MessageBox`, so the popup renders non-ASCII text correctly.

- Validate all three files exist and `reminder.txt` is non-empty.
  If any is missing, report and abort.

- Append to the checkpoint under `step_1` (keyed by `<task-slug>`): the reminder folder path and the three written/copied file paths with their sizes.


## Step 2 - Register Weekly Scheduled Task

- Register (or overwrite with `-Force`, after the Step 0 confirmation) a weekly Windows Scheduled Task named `<task-name>` that runs the popup script on the chosen day/time.
  Substitute `<task-slug>`, `<task-name>`, `<DayOfWeek>`, and `<HH:mm>` from Step 0:
  ```powershell
  $script    = Join-Path $env:LOCALAPPDATA 'notify-week\<task-slug>\Show-Reminder.ps1'
  $psExe     = (Get-Command powershell.exe).Source
  $action    = New-ScheduledTaskAction -Execute $psExe -Argument ('-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File "{0}"' -f $script)
  $trigger   = New-ScheduledTaskTrigger -Weekly -DaysOfWeek <DayOfWeek> -At '<HH:mm>'
  $principal = New-ScheduledTaskPrincipal -UserId ("{0}\{1}" -f $env:USERDOMAIN, $env:USERNAME) -LogonType Interactive -RunLevel Limited
  $settings  = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
  Register-ScheduledTask -TaskName '<task-name>' -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description '<one-line description of the reminder>' -Force | Out-Null
  ```

- If registration raises an error (e.g., `Access is denied`), report it and abort; do not silently fall back to another mechanism.

- Append to the checkpoint under `step_2` (keyed by `<task-slug>`): the task name, the execute path + arguments, the weekly day/time, and the registration status.


## Step 3 - Verify and Report

- Confirm the task exists and read its schedule (run each as a single-line command):
  ```powershell
  Get-ScheduledTask -TaskName '<task-name>' | Select-Object TaskName, State
  (Get-ScheduledTaskInfo -TaskName '<task-name>').NextRunTime
  ```

- Optionally test-fire the popup once so the user can confirm it renders (including any non-ASCII text).
  Do this only when the user asks for it, or offer it:
  ```powershell
  Start-ScheduledTask -TaskName '<task-name>'
  (Get-ScheduledTaskInfo -TaskName '<task-name>').LastTaskResult
  ```
  A `LastTaskResult` of `267009` (`SCHED_S_TASK_RUNNING`) means the message box is open — that is success, not an error.

- Include the removal command in the report so the user can undo the reminder:
  ```powershell
  Unregister-ScheduledTask -TaskName '<task-name>' -Confirm:$false
  ```

- Append to the checkpoint under `step_3` (keyed by `<task-slug>`): the task `State`, `NextRunTime`, whether a test-fire was run and its `LastTaskResult`, and the removal command.

- Save the MD report file summarizing **all** tasks set up this run — one section (or table row) per task with: task name, schedule (day + time), next run time, the reminder message, the stable reminder-folder path and files, how to change the schedule (re-run with a different `-DaysOfWeek` / `-At`), and the removal command.
