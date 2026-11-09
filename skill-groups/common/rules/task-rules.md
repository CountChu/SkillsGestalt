# Task Rules

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-18`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-11-02`  `c612bdfa1ea7`

> This file is in ASD-STE100 Simplified Technical English (STE), Issue 9.
> Technical words: blob, bold, bug, build, chapter, character, chore, column, command, commit, content, day, directory, document, feature, file, format, hash, heading, hunk, icon, indent, index, legend, line, link, list, lowercase, note, paragraph, path, prefix, pull request, repository, root, section, sentence, server, session, shell, skill, stage, status, subject, summary, table, term, test case, text, title, topic, tree line, twin, URI, URL, vault, wikilink, word, work item, workspace.

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
- **A workspace can keep its tasks in a different directory, for example in its vault.**
  Then set `tasksDir` in `config.yaml`.
- **A workspace can also keep the summary table in a different file.**
  Then set `taskSummary` in `config.yaml`.
  The summary table can be in a directory that is not the directory of the tasks.
  You can set one of the two values, or the two values.
  `AGENTS.md` gives the paths and the command of the check with these values.
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
- **Use a Markdown link with the full URL for a commit, a pull request, a build or a work item.**
  These items are on a server, for example Azure DevOps.
  A test case, a bug and a feature are also work items.
  Thus, each number of an item on the server has a link.
- **The text of the link is the short hash or the number.**
  An example is `[a798480e68](https://<server>/<repository>/commit/<full hash>)`.
  The URL contains the full hash of the commit.
  A commit can be only in a local repository.
  Then write its short hash without a link, and write that it is not on the server.
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

**Status**：<尚未開始|進行中|完成|取消>——<一行結論>
**Raised**：yyyy-mm-dd，<為什麼提出>
**Depends on**：[[Task M]]、[[Task K]]，沒有就寫 —

## 1. 背景
## 2. 結論
## 3. 過程
## 4. 要做的
## 5. 驗證
## 6. 與其他 task 的關係
## 7. 知識
### 適合寫成新 topic
### 適合併進現有 topic
### 不算知識
## 8. 日誌
### yyyy-mm-dd
```

- **The eight `##` chapters have the numbers 1 to 8 and these names, in this sequence.**
  If a chapter has no content, write `—` in it.
  Do not remove the chapter.
- **In `2. 結論`, give the result of the task in short items.**
  Tell which work the task did, and the result of each part.
  Tell the changes that the task made, and the problems that stay.
  For more information, give the section of `3. 過程` that has it.
  When `3. 過程` changes, make `2. 結論` agree with it.
  If the task has no result at this time, write `—`.
- **In `2. 結論`, use a table for each part that a table can show.**
  For example, give the runs, the changes and the problems in tables.
- **In `3. 過程`, divide the information into sections with `###` headings.**
  Write the work and the facts that you find, in the sequence that you find them.
  The Status line gives only a short result, in one line.
  Put the other information in `2. 結論`, in `3. 過程` and in `4. 要做的`.
- **In `7. 知識`, write the information from this task that you can write into a topic of `write-topic`.**
  Use the three `###` sections of the format.
  In `適合寫成新 topic`, give the title, the content and the source of a new topic.
  In `適合併進現有 topic`, give the topic and the information to add to it.
  In `不算知識`, give the facts that are only for this work, for example the path of one file.
  Also give there a problem of a tool, which a different task must repair.
- **Do not put `#`, `^`, `[`, `]` or `|` in the title of a new topic.**
  The title is the name of the topic file.
  In Obsidian, a link cannot find a file that has one of these characters in its name.
- **When you write an item of `7. 知識` into a topic, put ✅ before it and a link to the topic.**
  If the topic is in the vault of the task file, use a wikilink, for example `[[<Title>]]`.
  If the topic is in a different vault, use a Markdown link to an Obsidian URI, for example `[<Title>](obsidian://open?vault=<vault>&file=<path>)`.
  `<vault>` is the name of the vault directory, and `<path>` is the path of the topic file from that directory.
  Write each space in the URI as `%20`.
  If you did not examine the task for this information, write only `—` in the chapter.
- **The vault of a file is the nearest directory above the file that contains a `.obsidian` directory.**
  For a topic of `write-topic`, the vault is the directory that `wikiDir` in `config.yaml` gives.
  In Obsidian and in `check_tasks.py`, a wikilink finds a file only in the vault of the task file.
  If Obsidian cannot find the file, a click on the wikilink makes an empty note in that vault.
- **In `8. 日誌`, write one section `### yyyy-mm-dd` for each day, with the changes of that day.**
  Put the newest date first.
  If you change the task again on the same day, add to the section of that day.
  The last day section in the file always has the date of the Raised line.
- **In the Depends on line, write only the tasks that must be complete before this task.**
  Before they are complete, you cannot do this task, or you must do its work again.
  Write a task that has only a relation to this task in `6. 與其他 task 的關係`.
  The Depends on line gives only the tasks of the same workspace.
  Write a task of a different workspace that must be complete first in `6. 與其他 task 的關係`.
- **Use a table when the content compares items, puts items into groups, or gives quantities.**
  Put the table after the list that it is part of, and do not indent it.
  Do not write the information of the table in the list again.
  Give each table a number, from 1 in the file.
  Write its number and its name in a bold line before the table, for example `**表 1：字的分類**`.
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
- **A sub task has the same format as a task**: the Status, Raised and Depends on lines, and the eight chapters.
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
- **The status icons are ⬜ for 尚未開始, 🔄 for 進行中, ✅ for 完成, and ⊘ for 取消.**
  The legend below the table gives them.
- **Use 取消 when you stop a task and do not complete it.**
  In the Status line, give the cause, for example `取消——改由 [[Task 7]] 處理`.
  Keep the file of the task and its row in the table.
  Examine each task that has a link to it in its Depends on line.
  If you cannot do that task now, change its Depends on line.

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
  The `AGENTS.md` at the root of the workspace gives the command with this path.
- The command compares the table with each task file.
  It compares the numbers, the sequence, the links, the titles and the Raised dates.
  It also compares the status icons, the Depends on lines, the day sections and the chapter numbers.
  If they do not agree, it stops with the exit code `1`.
- If Windows cannot show the Chinese text and the icons, set `PYTHONIOENCODING=utf-8` first.
