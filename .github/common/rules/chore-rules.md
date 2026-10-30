# Chore Rules

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-18`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-30`  `8cc2e2061175`

> This file is in ASD-STE100 Simplified Technical English (STE), Issue 9.
> Technical words: blob, cell, chapter, chore, column, command, commit, content, day, directory, document, file, format, hunk, icon, index, legend, line, link, lowercase, paragraph, path, prefix, repository, root, section, sentence, session, shell, skill, stage, status, subject, summary, table, term, text, title, twin, vault, wikilink, word, workspace.

These rules tell how to write the chores of a workspace, how to do a chore, and how to keep their summary table.
A chore is work that you must do each time that its condition occurs.
Thus, a chore does not become complete, but you can stop it.
Work that becomes complete is a task, and [task-rules.md](task-rules.md) tells how to write it.
When you make, change or stop a chore, record this work as a task.

## Files

- **Each workspace keeps its chores in the directory `chores/` at its root, in one file for each chore.**
  The name of the file is `Chore N.md`: the word `Chore`, a space, and the number of the chore.
  In the file, write when and how to do the chore.
  Also write a record of each time that you did it.
  Then each session can do the chore.
- **The summary table is in `dashboard/chore-summary.md` at the root of the workspace, not in `chores/`.**
  It has an opening paragraph, the table, and the legend of the icons and the columns.
  Read the table first, to find the chore that you must do.
  Then open only that chore.
- **A workspace keeps only its own chores.**
  A chore does work on the files of its own workspace.
  A workspace can refer to the chores of a workspace if it uses the skill group of that workspace.
  A workspace does not refer to the chores of a workspace that uses its skill group.
- **Write each chore file in Traditional Chinese (繁體中文).**
  Keep in English each term that [tw-keep-english.md](../references/tw-keep-english.md) gives, as a TW twin does.
  A chore file has no TW twin.
  The names of the chapters and the words of the Status line are in Chinese, and `check_chores.py` reads them as they are.

## Links

- **Use a wikilink for a link to a chore or to a task, for example `[[Chore 1]]` or `[[Task 52]]`.**
- **Use a Markdown link for a link to a program, a skill, a rule or a document in the repository.**
  Give the path from the directory of the chore file.
  These files frequently have the same name, as `SKILL.md` and `README.md` do, and a wikilink can go to an incorrect file.
- **To refer to a chore of a different workspace, write `Chore N @ <workspace>` as text, for example `Chore 2 @ SkillsGestalt`.**
  For a task of a different workspace, write `Task N @ <workspace>`.
  Do not write a link to them.
  A wikilink finds a file only in the vault of its workspace.
  A Markdown link to a different repository breaks if the two repositories are not adjacent.
- **In the summary table, do not write a link with a different text, as `[[Chore N|text]]`.**
  The table uses `|` to divide its columns.

## The Chore File

A chore file has this format:

```
# Chore N - 標題

**Status**：<使用中|暫停|停用>——<一行結論>
**Started**：yyyy-mm-dd，<為什麼建立>
**When**：<何時要做，一行>

## 1. 目的
## 2. 何時要做
## 3. 怎麼做
## 4. 驗證
## 5. 與其他 task、chore 的關係
## 6. 執行紀錄
### yyyy-mm-dd
```

- **The six `##` chapters have the numbers 1 to 6 and these names, in this sequence.**
  If a chapter has no content, write `—` in it.
  Do not remove the chapter.
- **In `2. 何時要做`, write the condition that starts the chore.**
  Also write how you see that the condition occurs, for example the output of a command.
- **In `3. 怎麼做`, write the commands and the steps to do, and how to commit the result.**
- **In `6. 執行紀錄`, write one section `### yyyy-mm-dd` for each day.**
  The section tells the work that you did on that day, its result and its commit.
  Put the newest date first.
  If you do the chore again on the same day, add to the section of that day.
  If you did not do the chore before, write `—`.
  A date is not before the date of the Started line.
- **Follow [md-style.md](md-style.md).**

## Numbers

- **The chores have their own numbers, which start at 1.**
  A chore and a task can have the same number.
- **Give a new chore the number after the largest number that the workspace used for a chore.**
  This number can be on the `空號：` line of the summary table.
- **Do not use a number again.**
  If a chore moved to a different workspace, no file in this workspace has its number, and that is not an error.
  If you use the number again, the commits that start with its prefix refer to two chores.
- **When a chore moves to a different workspace, add its number to the `空號：` line.**
  The line is below the legend of the summary table, for example `空號：3、5。`.
  Write each number one time, and put `、` between the numbers.
  Also write one sentence that tells that a chore on the line moved to a different workspace, and that no chore uses its number again.
  If all numbers have a file, do not write the line.
- **`check_chores.py` makes sure that each number from 1 to the largest number has a file or is on the line.**
  A number that has a file is not on the line.

## The Summary Table

- **When you add a chore, add its row at the top of the table, because the newest chore is first.**
- **The columns are Chore, Started, Title, 何時要做, 上次執行 and Status.**
  - 何時要做: the When line of the chore file, as it is.
  - 上次執行: the newest date in `6. 執行紀錄` of the chore file, or `—` if you did not do the chore before.
- **Each time that you do a chore, change its `6. 執行紀錄` and its 上次執行 cell in the table.**
- **When the status of a chore changes, change its Status line and its icon in the table.**
  The status icons are 🔁 for 使用中, ⏸️ for 暫停, and ⏹️ for 停用.
  The legend below the table gives them.

## Commits

- **Start the subject of a commit for a run of a chore with `chore N: ` in lowercase, and then a summary.**
  An example is `chore 1: ste-custom.md is recorded again in the 22 STE files`.
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
  It compares the numbers, the sequence, the links, the titles, the Started dates and the 何時要做 cells.
  It also compares the 上次執行 cells, the status icons, the run records and the chapter numbers.
  If they do not agree, it stops with the exit code `1`.
- If Windows cannot show the Chinese text and the icons, set `PYTHONIOENCODING=utf-8` first.
