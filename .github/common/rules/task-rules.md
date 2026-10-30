# Task Rules

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-18`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-30`  `8cc2e2061175`

> This file is in ASD-STE100 Simplified Technical English (STE), Issue 9.
> Technical words: blob, chapter, chore, column, command, commit, content, day, directory, document, file, format, heading, hunk, icon, index, legend, line, link, list, lowercase, note, paragraph, path, prefix, repository, root, section, sentence, session, shell, skill, stage, status, subject, summary, table, term, text, title, tree line, twin, vault, wikilink, word, workspace.

These rules tell how to write the tasks of a workspace, and how to keep their summary table.
A task is work that continues after one session, and that becomes complete.
Work that you must do again each time that a condition occurs is a chore, not a task.
[chore-rules.md](chore-rules.md) tells how to write a chore.

## Files

- **Each workspace keeps its tasks in the directory `tasks/` at its root, in one file for each task.**
  The name of the file is `Task N.md`: the word `Task`, a space, and the number of the task.
  In the file, write the current state of the task and the files that the task changes.
  Then a session that did not start the task can continue it.
- **The summary table is in `dashboard/task-summary.md` at the root of the workspace, not in `tasks/`.**
  It has an opening paragraph, the table and the legend of the status icons.
  Read the table first.
  Then open only the task that you need.
- **A workspace keeps only its own tasks.**
  A task records the work on the files of its own workspace.
  A workspace can refer to the tasks of a workspace if it uses the skill group of that workspace.
  A workspace does not refer to the tasks of a workspace that uses its skill group.
- **Write each task file in Traditional Chinese (繁體中文).**
  Keep in English each term that [tw-keep-english.md](../references/tw-keep-english.md) gives, as a TW twin does.
  A task file has no TW twin.
  The names of the chapters and the words of the Status line are in Chinese, and `check_tasks.py` reads them as they are.

## Links

- **Use a wikilink for a link to a task or to a different note, for example `[[Task 2]]`.**
- **Use a Markdown link for a link to a program, a skill, a rule or a document in the repository.**
  Give the path from the directory of the task file.
  These files frequently have the same name, as `SKILL.md` and `README.md` do, and a wikilink can go to an incorrect file.
- **To refer to a task of a different workspace, write `Task N @ <workspace>` as text, for example `Task 62 @ SkillsGestalt`.**
  Do not write a link to it.
  A wikilink finds a file only in the vault of its workspace.
  A Markdown link to a different repository breaks if the two repositories are not adjacent.
- **In the summary table, do not write a link with a different text, as `[[Task N|text]]`.**
  The table uses `|` to divide its columns.

## The Task File

A task file has this format:

```
# Task N - 標題

**Status**：<尚未開始|進行中|完成>——<一行結論>
**Raised**：yyyy-mm-dd，<為什麼提出>
**Depends on**：[[Task M]]、[[Task K]]，沒有就寫 —

## 1. 背景
## 2. 現況
## 3. 要做的
## 4. 驗證
## 5. 與其他 task 的關係
## 6. 日誌
### yyyy-mm-dd
```

- **The six `##` chapters have the numbers 1 to 6 and these names, in this sequence.**
  If a chapter has no content, write `—` in it.
  Do not remove the chapter.
- **In `2. 現況`, divide the information into sections with `###` headings.**
  The Status line gives only a short result, in one line.
  Put the other information in `2. 現況` and in `3. 要做的`.
- **In `6. 日誌`, write one section `### yyyy-mm-dd` for each day, with the changes of that day.**
  Put the newest date first.
  If you change the task again on the same day, add to the section of that day.
  The last day section in the file always has the date of the Raised line.
- **In the Depends on line, write only the tasks that must be complete before this task.**
  Before they are complete, you cannot do this task, or you must do its work again.
  Write a task that has only a relation to this task in `5. 與其他 task 的關係`.
  The Depends on line gives only the tasks of the same workspace.
  Write a task of a different workspace that must be complete first in `5. 與其他 task 的關係`.
- **Follow [md-style.md](md-style.md).**

## Numbers

- **Give a new task the number after the largest number that the workspace used.**
  This number can be on the `空號：` line of the summary table.
- **Do not use a number again.**
  If a task moved to a different workspace, no file in this workspace has its number, and that is not an error.
  If you use the number again, the commits that start with its prefix refer to two tasks.
- **When a task or a sub task moves to a different workspace, add its number to the `空號：` line.**
  The line is below the legend of the summary table, for example `空號：18.1、18.3、28。`.
  Write each number one time, and put `、` between the numbers.
  Also write one sentence that tells that a task on the line moved to a different workspace, and that no task uses its number again.
  If all numbers have a file, do not write the line.
- **`check_tasks.py` makes sure that each number from 1 to the largest number has a file or is on the line.**
  A number that has a file is not on the line.

## Sub Tasks

- **A task can have sub tasks, each in a file `Task N.M.md`.**
  The heading of a sub task is `# Task N.M - 標題`, and its wikilink is `[[Task N.M]]`.
  In each task, M starts at 1, and the rules of the numbers apply to it too.
- **Only the number shows that a sub task is a part of its task.**
  Do not add a line for it.
  The Depends on line of a task does not give its sub tasks.
- **A sub task has the same format as a task**: the Status, Raised and Depends on lines, and the six chapters.
- **Write the content of a sub task only in the sub task.**
  Also write its subsequent records only there.
  The task keeps only the list of its sub tasks, and the rules and decisions for all of them.
  Each item of the list is one line: the link, the status icon and the title, for example `- [[Task 32.1]] ✅ DFD`.
- **When the status of a sub task changes, change its Status line and its icon in the summary table.**
  Also change its icon in the list of its task.

## The Summary Table

- **When you add a task, add its row at the top of the table, because the newest task is first.**
- **Put the rows of the sub tasks directly below the row of their task, in the sequence of their numbers.**
  Before the link of a sub task, put a tree line.
  For the last sub task, write `└─ [[Task N.M]]`.
  For each other sub task, write `├─ [[Task N.M]]`.
  When you add a sub task, change the `└─` of the row that was the last one to `├─`.
  In the Depends on column, do not put a tree line before a link.
- **The Depends on column gives the links of the Depends on line, each with the current icon of its task**, for example `[[Task 1]] ✅`.
- **When the status of a task changes, change its Status line and its icon in the table.**
  Also change its icon in the Depends on column of each row that has a link to it.
- **The status icons are ⬜ for 尚未開始, 🔄 for 進行中, and ✅ for 完成.**
  The legend below the table gives them.

## Commits

- **Start the subject of a commit for the work of a task with `task N: ` in lowercase, and then a summary.**
  For a sub task, start it with `task N.M: `.
  If the commit is for more than one task, give the primary task.
- **Commit only the hunks that you changed.**
  Other sessions can change the same files at the same time.
  Before you commit, look at `git status` and at HEAD.
  If a different session also changes a file that you changed, wait for its commit.
  Or, stage a blob that is the file at HEAD with only your lines added: `git hash-object -w`, then `git update-index --cacheinfo`.
- **For `dashboard/task-summary.md` and for the file of a task that has sub tasks, always stage such a blob.**
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
python {skillGroups.common}/scripts/check_tasks.py --summary dashboard/task-summary.md --tasks-dir tasks
```

- `{skillGroups.common}` is the root of the skill group `common` of the workspace.
  The `CLAUDE.md` at the root of the workspace gives the command with this path.
- The command compares the table with each task file.
  It compares the numbers, the sequence, the links, the titles and the Raised dates.
  It also compares the status icons, the Depends on lines, the day sections and the chapter numbers.
  If they do not agree, it stops with the exit code `1`.
- If Windows cannot show the Chinese text and the icons, set `PYTHONIOENCODING=utf-8` first.
