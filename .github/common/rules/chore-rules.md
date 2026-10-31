# Chore Rules

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-18`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-30`  `8cc2e2061175`

> This file is in ASD-STE100 Simplified Technical English (STE), Issue 9.
> Technical words: agency, blob, cell, chapter, chore, column, command, commit, content, day, digit, directory, document, file, format, hunk, hyphen, icon, index, legend, letter, line, link, lowercase, paragraph, path, prefix, private, repository, root, section, session, shell, skill, stage, status, subject, summary, table, term, text, title, twin, vault, wikilink, word, workspace.

These rules tell how to write the chores of a workspace, how to do a chore, and how to keep their summary table.
A chore is work that you must do each time that its condition occurs.
Thus, a chore does not become complete, but you can stop it.
Work that becomes complete is a task, and [task-rules.md](task-rules.md) tells how to write it.
When you make, change or stop a chore, record this work as a task.

## Files

- **Each workspace keeps its chores in the directory `chores/` at its root, in one file for each chore.**
  The name of the file is the name of the chore and `.md`, for example `keep-english.md`.
  In the file, write when and how to do the chore.
  Then each session can do the chore.
  A workspace that does only chores of different agencies can have no `chores/`.
  Do not put a program or a directory in `chores/`, because a chore has no program of its own.
- **The summary table is in `dashboard/chore-summary.md` at the root of the workspace, not in `chores/`.**
  It has an opening paragraph, the table, the legend of the icons, and the run records.
  Read the table first, to find the chore that you must do.
  Then open only that chore.
- **A chore does work on the files of the workspace that does it.**
  A workspace can do a chore of an agency if it uses the skill group of that agency.
  A workspace does not do the chores of a workspace that uses its skill group.
- **Write each chore file in Traditional Chinese (繁體中文).**
  Keep in English each term that [tw-keep-english.md](../references/tw-keep-english.md) gives, as a TW twin does.
  A chore file has no TW twin.
  The names of the chapters and the words of the Status line are in Chinese, and `check_chores.py` reads them as they are.

## Names

- **The name of a chore has lowercase letters, digits and hyphens, and starts with a letter.**
  An example is `keep-english`.
- **No two chores in all the agencies have the same name, as no two skills do.**
  Thus, a name identifies one chore, also in a different agency.
- **You can change the name of a chore.**
  The task that changes it also changes each link to the chore and its run records.
- **When you stop a chore, keep its file in `chores/`, and do not use its name again.**
  If you use the name again, the commits that start with its prefix refer to two chores.

## Links

- **Use a wikilink for a link to a chore of your workspace or to a task, as `[[keep-english]]` or `[[Task 52]]`.**
- **Use a Markdown link for a link to a program, a skill, a rule or a document in the repository.**
  Give the path from the directory of the chore file.
  These files frequently have the same name, as `SKILL.md` and `README.md` do, and a wikilink can go to an incorrect file.
- **To refer to a chore of a different agency, write its name as text, for example `keep-english`.**
  For a task of a different workspace, write `Task N @ <workspace>` as text.
  Do not write a link to them.
  A wikilink finds a file only in the vault of its workspace.
  A Markdown link to a different repository breaks if the two repositories are not adjacent.
- **In the summary table, do not write a link with a different text, as `[[name|text]]`.**
  The table uses `|` to divide its columns.

## A Chore of a Different Agency

- **To do a chore of a different agency, add a row for it to your summary table.**
  In the Chore cell, write the name of the chore as text, not as a link.
  The Title and 何時要做 cells are the same as in the chore file of that agency.
  The Started cell is the day that your workspace started the chore.
  The Status cell is the status of the chore in your workspace.
- **The `agencies` value of `config.yaml` gives the root of each agency that has a chore that the workspace does.**
  An example is the line `SkillsGestalt: ~/Library/CloudStorage/Dropbox/2-Areas-I/SkillsGestalt` in `agencies:`.
  `check_chores.py` finds the chore file at `{agencies.<agency>}/chores/<name>.md`.
- **Do not do a private chore of a different agency.**
  Its file has a `**Private**` line, as the section "The Chore File" tells.
- **If more than one workspace does a chore, its file does not contain a value of one workspace.**
  Write a path in the skill group as `{skillGroups.common}`.
  Each workspace does the chore at its root, on its own files, and keeps its reports, its run records and its commits.

## The Chore File

A chore file has this format:

```
# <name> - 標題

**Status**：<使用中|暫停|停用>——<一行結論>
**Started**：yyyy-mm-dd，<為什麼建立>
**When**：<何時要做，一行>
**Private**：<只有哪個 agency 做，為什麼；不是 private 就不寫這一行>

## 1. 目的
## 2. 何時要做
## 3. 怎麼做
## 4. 驗證
## 5. 與其他 task、chore 的關係
```

- **The five `##` chapters have the numbers 1 to 5 and these names, in this sequence.**
  If a chapter has no content, write `—` in it.
  Do not remove the chapter.
- **In `2. 何時要做`, write the condition that starts the chore.**
  Also write how you see that the condition occurs, for example the output of a command.
- **In `3. 怎麼做`, write the commands and the steps to do, and how to commit the result.**
- **A chore has no program of its own.**
  Its steps use a skill, or a program in a skill group.
  Write the path of the program with `{skillGroups.X}`, for example `{skillGroups.common}/scripts/audit_keep_english.py`.
  A skill tells how to do the work, and a chore tells when to do it and records each run.
  Thus, each program is in one location, where each agency can find it.
- **A private chore has the line `**Private**` after the When line.**
  Only the agency that has the chore does it.
  Its programs can contain values of that agency, but they are in a skill group, as all programs are.
- **If a chore keeps files in `checkpoints/`, put them in `checkpoints/chores/<name>`.**
  `<name>` is the name of the chore.
  Thus, each workspace that does the chore uses the same path.
- **A chore file does not contain run records.**
  Each workspace writes the runs of the chore in its own summary table, as the section "The Summary Table" tells.
- **Follow [md-style.md](md-style.md).**

## The Summary Table

- **Put the rows in the sequence of their Started dates, the newest first.**
  If two rows have the same date, put them in the sequence of their names.
- **The columns are Chore, Started, Title, 何時要做, 上次執行 and Status.**
  - 何時要做: the When line of the chore file, as it is.
  - 上次執行: the newest date in the run records of the chore, or `—` if you did not do the chore before.
- **Below the legend, the section `## 執行紀錄` contains the run records.**
  It has one section `### <name>` for each chore that you did, in the sequence of the table.
  In it, write one section `#### yyyy-mm-dd` for each day that you did the chore.
  This section tells the work that you did on that day, its result and its commit.
  Put the newest date first, and do not put a date before the Started cell of the row.
  If you do the chore again on the same day, add to the section of that day.
- **Each time that you do a chore, change its run records and its 上次執行 cell.**
- **When the status of a chore changes, change its Status line and its icon in the table.**
  The status icons are 🔁 for 使用中, ⏸️ for 暫停, and ⏹️ for 停用.
  The legend below the table gives them.

## Commits

- **Start the subject of a commit for a run of a chore with `chore <name>: `, and then a summary.**
  An example is `chore rerecord-ste-custom: ste-custom.md is recorded again in the 22 STE files`.
- **A commit that makes, changes or stops a chore is for a task, and its subject starts with `task N: `.**
- **Commit only the hunks that you changed.**
  Other sessions can change the same files at the same time.
  Before you commit, look at `git status` and at HEAD.
  If a different session also changes a file that you changed, wait for its commit.
  Or, stage a blob that is the file at HEAD with only your lines added: `git hash-object -w`, then `git update-index --cacheinfo`.
- **For `dashboard/chore-summary.md`, always stage such a blob.**
  Do not `git add` the full file.
  A different session can add a row to the file between your check and your `git add`.
  Then your commit contains a row that a different session added.
- **Put the check of HEAD and the steps after it in one shell command, with `&&` between the steps.**
  These steps are the commands that stage a blob, `git add` and `git commit`.
  A check on a line of its own does not stop the commands on the subsequent lines.
- **Before you do `git commit`, make sure that the index contains only your paths.**
  A different session can stage its files, and then your commit contains them.

## Check

After each change, run this command from the root of the workspace:

```bash
python {skillGroups.common}/scripts/check_chores.py --summary dashboard/chore-summary.md --chores-dir chores
```

- `{skillGroups.common}` is the root of the skill group `common` of the workspace.
  The `CLAUDE.md` at the root of the workspace gives the command with this path.
- The command compares the table with each chore file.
  It compares the names, the sequence, the links, the titles, the Started dates and the 何時要做 cells.
  It also compares the 上次執行 cells, the status icons, the run records and the chapter numbers.
  If they do not agree, it stops with the exit code `1`.
- If Windows cannot show the Chinese text and the icons, set `PYTHONIOENCODING=utf-8` first.
