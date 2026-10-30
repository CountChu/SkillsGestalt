# Create MD report file

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-18`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-30`  `8cc2e2061175`

> This file is in ASD-STE100 Simplified Technical English (STE), Issue 9.
> Technical words: argument, backtick, byte, cache, canonical skill invocation, checkpoint, clock, command, content, disk, double-quoted string, editor, escape character, escaping, fence, field, file, file-editing tool, filename, frontmatter, hard-code, header, here-string, interpolation, line, orchestration, parse, path, pipe, placeholder, root, section, shell, single-quoted here-string, skill, string, table, template, text, title, wiki, workflow, workspace, wrapper.

- Each skill gives the filename of its report (for example, `run-pr-{prId}-{yymmdd}`) in its MUST FOLLOW section.
- Create the MD report file at `{wikiDir}\{skill_name}\{REPORT_FILENAME}.md`.
  Read `wikiDir` from the [config.yaml](config.yaml) of the workspace, at the root of the workspace.
  Do not hard-code the root of the wiki.
  - If the file is there, use the rules that follow to update the fields of its header.
    Then remove all the content after the header.
- Write the MD report file with this template, and replace the placeholders with their values:

  ````markdown
  # {REPORT_TITLE}

  - **Skill**: {SKILL_NAME}
  - **Checkpoint**: `{CHECKPOINT_PATH}`
  - **Created**: {DATETIME}
  - **Updated**: {DATETIME}
  - **Prompt**:
  ```
  {USER_PROMPT}
  ```
  ````

  Placeholders:
  - `{REPORT_TITLE}` → the title of the report for this run of the skill.
  - `{SKILL_NAME}` → the name of the skill, from the YAML frontmatter.
  - `{CHECKPOINT_PATH}` → the path of the YAML checkpoint of this run, as the MUST FOLLOW section of the skill gives it (for example, `checkpoints\report-pipeline\{reportName}\process.yaml` or `checkpoints\report-known-issues\{reportName}.yaml`).
  - `{DATETIME}` → the current local date and time (`YYYY-MM-DD HH:MM`).
    Read it from the system clock when you write it.
    In PowerShell, use `Get-Date -Format "yyyy-MM-dd HH:mm"`.
    On macOS/Linux, use `date '+%Y-%m-%d %H:%M'`.
    Do not use an estimate or a time that you saw before.
    - **Created**: If the MD report file is there, keep its initial Created value.
    - **Updated**: Always set it to the current date and time.
  - `{USER_PROMPT}` → the **canonical skill invocation** that Step 0 keeps.
    It is the `/<skill-name>` command, and then the arguments that the skill parses (for example, `/report-week-note` and then `7/9 - 7/14`).
    Record this canonical skill invocation.
    Do **not** record the text around it, although that text started the run.
    Examples of that text are a wrapper, an orchestration and an instruction to an agent.


# Update MD report file

- Apply these rules at the end of each workflow step that adds content to the MD report file.
- Set the **Updated** field as `{DATETIME}` above tells.


# Write the MD report file safely

- A report contains many backticks, code fences and table pipes.
  Thus, **how** the text goes to the disk is as important as the content of the text.
- **If possible, write the file directly with the file-editing tool.**
  The cause of damage to report text is the shell command that the text goes through.
  Also, it is not necessary to use a shell to create a report.
- **Do not send report text through a PowerShell double-quoted string.**
  In `"..."`, the backtick is the escape character of PowerShell, and PowerShell changes it before it writes the text.
  `` `r `` becomes CR, `` `n `` becomes LF, `` `a `` becomes BEL, `` `t `` becomes TAB, and each other `` `x `` becomes only `x`.
  For example, the line ``verified `resolved` `` goes to the disk as `verified ` + CR + `esolved`.
  Also, a fence of three backticks becomes one backtick.
  You get **no error message**: the command shows that it operated correctly.
- If you must use the shell, put the text in a **single-quoted here-string**.
  A single-quoted here-string does no escaping and no interpolation.
  Then write the text as UTF-8 without BOM:

  ```powershell
  $md = @'
  ...report text, backticks and fences intact...
  '@
  $md = $md.Replace('{UPDATED}', $now)
  [System.IO.File]::WriteAllText($path, $md, [System.Text.UTF8Encoding]::new($false))
  ```

  Replace the values with `.Replace(...)` **after** the here-string.
  If you use interpolation in `"$var"`, the escaping occurs again.
  The single-quoted here-string is there to prevent this escaping.
- After you write with the shell, use `[System.IO.File]::ReadAllText($path)` to make sure that the bytes are correct.
  An editor can read the file from its cache, and show the previous content of the file.
  Then you can think that the shell did not write the file, although the shell wrote it correctly.
