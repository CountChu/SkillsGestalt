# YAML Checkpoint Rules

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-18`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-30`  `8cc2e2061175`

> This file is in ASD-STE100 Simplified Technical English (STE), Issue 9.
> Technical words: canonical skill invocation, checkpoint, clock, definition, directory, epoch, field, file, flat file, format, hard-code, heading, layout, metadata, minute, model, partial, path, root, rounding, second, section, skill, subfield, timestamp, workspace.

- Each skill gives the path of its YAML checkpoint in its MUST FOLLOW section.
  The YAML checkpoint is in the `checkpoints\` directory at the root of the workspace.
  This directory is always the same.
  You set the root directory of the MD reports in `config.yaml`, but you cannot set the `checkpoints\` directory there.
  In this directory, the skills use two layouts:
  - `checkpoints\{skill_name}\{run_dir}\process.yaml` puts each run in a different directory.
    A skill uses this layout when the run also writes data files or section partials in the same directory as the checkpoint.
  - `checkpoints\{skill_name}\{report_filename}.yaml` is one flat file for each run.
- Each step must write its important output fields in this YAML checkpoint file.
- Each step puts its outputs in a group with the name `step_{number}` (for example, `step_0` and `step_1`).
- Each step must include a `title` field.
  The value of this field agrees with the heading of the step in the skill definition (for example, `Warmup` and `Fetch PR Info`).
- `step_0` must include these fields:
  - `skill`: the name of the skill.
  - `model`: the AI model that operates the skill.
  - `prompt`: the canonical skill invocation, which is `{USER_PROMPT}` in [report-md-rules.md](.github/common/rules/report-md-rules.md).
- Each step must include a `time` field with these subfields:
  - `begin` and `end`, in the format `yyyy-MM-dd HH:mm:ss`.
  - `taken`, in the format `Xm Ys`.
- Read the value of `time.begin` from the local system clock when each step starts.
  Read the value of `time.end` from the same clock when the step stops.
  In PowerShell, use `Get-Date -Format "yyyy-MM-dd HH:mm:ss"`.
  On macOS/Linux, use `date '+%Y-%m-%d %H:%M:%S'`.
- Do not use estimates or approximate timestamps for `time.begin` and `time.end`.
  Also, do not get these timestamps from the metadata of a file after the step.
  A time that you get again from other data is false, because you did not measure it.
- Calculate the value of `time.taken` as `end - begin`.
  For example:
  - In PowerShell, use `$ts = (Get-Date $end) - (Get-Date $begin); "{0}m {1}s" -f [math]::Floor($ts.TotalMinutes), $ts.Seconds`.
  - On macOS/Linux, calculate the difference between the two times in epoch seconds.
    Then write the difference in the format of `taken`.
- For `time.taken`, count only the full minutes.
  Do not use rounding, because rounding can make the number of minutes too large.
  Do not hard-code the value of `time.taken`.
  Do not use an estimate of this value.
- If the YAML file is there, merge or update only the related `step_{number}` group.
