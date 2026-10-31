# Forge Setup

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-31`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-31`  `8cc2e2061175`

> This file is in ASD-STE100 Simplified Technical English (STE), Issue 9.
> Technical words: agency, cell, chore, command, commit, day, directory, document, environment, file, Forge, Gestalt, git, introduction, InvestForge, line, link, placeholder, print, quote, repository, root, rule, script, section, sentence, setup, skill group, status, summary, table, task, template, term, text, twin, vault, workspace.

This document tells how to make a Forge, an agency that uses the `common` skill group of SkillsGestalt.
[glossary.md](glossary.md) gives the terms agency, Gestalt and Forge.
InvestForge is a Forge that did these steps.
The examples use BookForge, a Forge that is only an example.

## Make a Forge

Do the steps in this sequence.
Each step gives the work to do and how to check it.

1. **Make the root of the workspace adjacent to the root of SkillsGestalt, and make it a git repository.**
   An example is `~/Library/CloudStorage/Dropbox/2-Areas-I/BookForge`.
   When the two roots are adjacent, the links that the script writes in step 4 are short.
   Check: `git status` in the root shows a repository.
2. **Copy [config-forge-tmp.yaml](../templates/config-forge-tmp.yaml) to `config.yaml` at the root, and replace each placeholder.**
   `{GESTALT_ROOT}` is the root of SkillsGestalt.
   `{WIKI_DIR}` is the vault of the Forge, and `{WIKI_ROOT_DIR}` is the directory that contains the vaults of all the agencies.
   Keep the quotes around each value.
   Check: no value in `config.yaml` contains `{GESTALT_ROOT}`, `{WIKI_DIR}` or `{WIKI_ROOT_DIR}`.
3. **Write `CLAUDE-local.md` at the root.**
   It contains the rules that only this Forge has, for example how to set up its Python environment.
   A line `{CLAUDE-local}` divides it into two parts.
   The script puts the part above the line after the introduction of `CLAUDE.md`, and the part below the line at the end.
   If the Forge does not have a rule of its own, write a section `## Settings of This Agency` with one sentence.
   Check: the file is at the root.
4. **Make `CLAUDE.md`: from the root, run `python {skillGroups.common}/scripts/gen_claude_md.py`.**
   The script fills the template of the `common` skill group with the values of `config.yaml` and with `CLAUDE-local.md`.
   Do not change `CLAUDE.md`.
   To change a rule, change `CLAUDE-local.md`, and then run the script again.
   Check: `python {skillGroups.common}/scripts/gen_claude_md.py --check` prints `PASS`.
5. **Record the setup as the first task: write `tasks/Task 1.md` and `dashboard/task-summary.md`.**
   Git does not keep an empty directory, and the check of the tasks stops if `tasks/` is not there.
   Use the two texts below.
   Change the date to the day of the setup, in the task file and in its row.
   Check: the `check_tasks.py` command that `CLAUDE.md` gives prints `PASS`.
6. **Write `dashboard/chore-summary.md` from the text below.**
   Its row is for the chore `keep-english` of SkillsGestalt, which `keepEnglishChore` in `config.yaml` names.
   The Title and 何時要做 cells are the same as in the chore file of SkillsGestalt, and the Started cell is the day of the setup.
   If the Forge does not do the chore, remove the row and the `keepEnglishChore` line.
   The Forge has no directory `chores/` before it has a chore of its own.
   Check: the `check_chores.py` command that `CLAUDE.md` gives prints `PASS`.
7. **Commit `config.yaml`, `CLAUDE-local.md`, `CLAUDE.md`, `tasks/` and `dashboard/`.**
   Then, in `tasks/Task 1.md`, write that the setup is complete, change its status, and commit again.
   Check: `git status` shows no change.

The file `tasks/Task 1.md` of step 5:

```
# Task 1 - 接上 SkillsGestalt

**Status**：進行中——照 forge-setup.md 接上 SkillsGestalt。
**Raised**：2026-10-31，建立本 agency，使用 SkillsGestalt 的 common skill group。
**Depends on**：—

## 1. 背景

—

## 2. 現況

—

## 3. 要做的

—

## 4. 驗證

—

## 5. 與其他 task 的關係

—

## 6. 日誌

### 2026-10-31

- 建立 task。
```

The file `dashboard/task-summary.md` of step 5:

```
# Tasks

跨 session 的待辦工作。
每個 task 是 `tasks/Task N.md` 一個檔案。

| Task | Raised | Title | Status | Depends on |
| --- | --- | --- | --- | --- |
| [[Task 1]] | 2026-10-31 | 接上 SkillsGestalt | 🔄 | — |

Status：⬜ 尚未開始　🔄 進行中　✅ 完成。
```

The file `dashboard/chore-summary.md` of step 6:

```
# Chores

會重複做的例行工作。

| Chore | Started | Title | 何時要做 | 上次執行 | Status |
| --- | --- | --- | --- | --- | --- |
| keep-english | 2026-10-31 | keep-English 稽核 | tw-keep-english.md 換了版本，和上次稽核的版本不同 | — | 🔁 |

Status：🔁 使用中　⏸️ 暫停　⏹️ 停用。
```

## Change an Older Workspace

Some workspaces use the `common` skill group, but they have a `CLAUDE.md` that a person wrote.
To change such a workspace into a Forge, do these steps.
Then do steps 4 to 7 of the section "Make a Forge".

- **Move the rules that only this workspace has from `CLAUDE.md` into `CLAUDE-local.md`.**
  Do not move a rule that the template of the `common` skill group has.
  The template has the rules for the twins, the Markdown files, the tasks and the chores.
- **Add the values that [config-forge-tmp.yaml](../templates/config-forge-tmp.yaml) has and that `config.yaml` does not have, as `agencies` and `keepEnglishChore`.**
- **If a chore of the workspace does the same work as a chore of SkillsGestalt, remove its file.**
  Write its row with the name of the chore of SkillsGestalt as text.
  Move its run records to the section `## 執行紀錄` of the summary table, and its reports to `checkpoints/chores/<name>`.
- **Give a name to each chore of its own, as [chore-rules.md](../rules/chore-rules.md) tells.**

## After a Change in SkillsGestalt

A Forge reads SkillsGestalt where it is.
Thus, a change in SkillsGestalt changes the Forge immediately.
After such a change, run the `gen_claude_md.py`, `check_tasks.py` and `check_chores.py` commands of `CLAUDE.md` again.
