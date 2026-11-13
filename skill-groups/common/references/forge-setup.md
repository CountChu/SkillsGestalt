# Forge Setup

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-31`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-11-02`  `c612bdfa1ea7`

> This file is in ASD-STE100 Simplified Technical English (STE), Issue 9.
> Technical words: agency, branch, cell, chore, clone, command, commit, computer, day, directory, document, environment, file, Forge, Gestalt, git, introduction, InvestForge, line, link, package, path, placeholder, print, quote, repository, root, rule, script, section, sentence, setup, skill, skill group, status, summary, table, task, template, term, text, twin, vault, workspace.

This document tells how to make a Forge, an agency that uses the `common` skill group of SkillsGestalt.
[glossary.md](glossary.md) gives the terms agency, Gestalt and Forge.
InvestForge is a Forge that did these steps.
The examples use BookForge, a Forge that is only an example.

## Make a Forge

Do the steps in this sequence.
Each step gives the work to do and how to check it.

1. **Make the root of the workspace adjacent to the root of SkillsGestalt, and make it a git repository.**
   An example is `~/Library/CloudStorage/Dropbox/2-Areas-I/BookForge`.
   When the two roots are adjacent, the links that the script writes in step 5 are short.
   Check: `git status` in the root shows a repository.
2. **Copy [config-forge-tmp.yaml](../templates/config-forge-tmp.yaml) to `config.shared.yaml` at the root, and write `config.local.yaml` adjacent to it.**
   In `config.shared.yaml`, replace `{WORK_BRANCH}` with the work branch of this clone, for example `m1`.
   `config.local.yaml` gives the values of this computer, one on each line, for example `workBranch: m1`.
   It gives `gestaltRoot`, the root of SkillsGestalt, and `workBranch`.
   It also gives `wikiDir`, the vault of the Forge, and `wikiRootDir`, the directory that contains the vaults of all the agencies.
   Check: `config.shared.yaml` does not contain `{WORK_BRANCH}`, and `config.local.yaml` gives the four values.

   Add the lines `/config.yaml` and `/config.local.yaml` to `.gitignore`, because the values of each computer are different.
   Each clone has its own work branch, and it is not `main`.
   A clone of the Forge on a different computer writes its own `config.local.yaml`, and adds its work branch to `workBranches` in `config.shared.yaml`.
3. **Make the Python environment `.venv` at the root, and install the packages that the `common` skill group needs.**
   From the root, run `python3 -m venv .venv`, or `py -m venv .venv` on Windows, then `{python} -m pip install -r {skillGroups.common}/requirements.txt`.
   Here and in the steps that follow, `{python}` is the Python of `.venv`: `.venv/bin/python`, or `.venv\Scripts\python.exe` on Windows.
   The skills of the `common` skill group run their scripts with it, and they stop when the workspace has no `.venv`.
   Add the line `.venv/` to `.gitignore`, because git must not keep `.venv`.
   Check: `{python} -c "import yaml, pypdf"` gives no error.
4. **Write `AGENTS.shared.md` at the root.**
   It contains the rules that only this Forge has, for example how to set up its Python environment.
   A line `{AGENTS-shared}` divides it into two parts.
   The script puts the part above the line after the introduction of `AGENTS.md`, and the part below the line at the end.
   If the Forge does not have a rule of its own, write a section `## Settings of This Agency` with one sentence.
   Check: the file is at the root.

   Also write `.claude/settings.json` at the root, with the text below: then Claude Code puts no `Co-Authored-By` line in a commit message, as `AGENTS.md` tells.
   Check: the file is at the root.

   ```json
   {
     "attribution": {
       "commit": "",
       "pr": "",
       "sessionUrl": false
     }
   }
   ```
5. **Make `config.yaml`, `AGENTS.md` and `CLAUDE.md`: from the root, run `{python} {skillGroups.common}/scripts/gen_config.py`.**
   The script makes `config.yaml` from `config.shared.yaml` and `config.local.yaml`.
   Then it fills the template of the `common` skill group with the values of `config.yaml` and with `AGENTS.shared.md`, and writes `AGENTS.md`.
   It also writes `CLAUDE.md`, which contains only the line `@AGENTS.md`.

   Do not change `config.yaml`, `AGENTS.md` or `CLAUDE.md`.
   To change a rule, change `AGENTS.shared.md`, and then run the script again.
   Check: `{python} {skillGroups.common}/scripts/gen_config.py --check` prints `PASS` for the three files.
6. **Record the setup as the first task: write `tasks/Task 1.md` and `dashboard/task-summary.md`.**
   Git does not keep an empty directory, and the check of the tasks stops if `tasks/` is not there.
   Use the two texts below.
   Change the date to the day of the setup, in the task file and in its row.
   Check: the `check_tasks.py` command that `AGENTS.md` gives prints `PASS`.
7. **Write `dashboard/chore-summary.md` from the text below.**
   Its row is for the chore `keep-english` of SkillsGestalt, which `keepEnglishChore` in `config.yaml` names.
   The Title and 何時要做 cells are the same as in the chore file of SkillsGestalt, and the Started cell is the day of the setup.
   If the Forge does not do the chore, remove the row and the `keepEnglishChore` line.
   The Forge has no directory `chores/` before it has a chore of its own.
   Check: the `check_chores.py` command that `AGENTS.md` gives prints `PASS`.
8. **Commit `.gitignore`, `config.shared.yaml`, `AGENTS.shared.md`, `.claude/settings.json`, `AGENTS.md`, `CLAUDE.md`, `tasks/` and `dashboard/`.**
   Then, in `tasks/Task 1.md`, write that the setup is complete, change its status, and commit again.
   Check: `git status` shows no change.

The file `tasks/Task 1.md` of step 6:

```
# Task 1 - 接上 SkillsGestalt

**Status**：進行中——照 forge-setup.md 接上 SkillsGestalt。
**Raised**：2026-10-31，建立本 agency，使用 SkillsGestalt 的 common skill group。
**Depends on**：—

## 1. 背景

—

## 2. 結論

—

## 3. 過程

—

## 4. 要做的

—

## 5. 驗證

—

## 6. 與其他 task 的關係

—

## 7. 知識

—

## 8. 日誌

### 2026-10-31

- 建立 task。
```

The file `dashboard/task-summary.md` of step 6:

```
# Tasks

跨 session 的待辦工作。
每個 task 是 `tasks/Task N.md` 一個檔案。

| Task | Raised | Title | Status | Depends on |
| --- | --- | --- | --- | --- |
| [[Task 1]] | 2026-10-31 | 接上 SkillsGestalt | 🔄 | — |

Status：⬜ 尚未開始　🔄 進行中　✅ 完成　⊘ 取消。
```

The file `dashboard/chore-summary.md` of step 7:

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
Then do step 3, and steps 5 to 8, of the section "Make a Forge".

- **Move the rules that only this workspace has from `CLAUDE.md` into `AGENTS.shared.md`.**
  Do not move a rule that the template of the `common` skill group has.
  The template has the rules for the twins, the Markdown files, the tasks and the chores.
- **Move `config.yaml` to `config.shared.yaml` with `git mv`, and do step 2 for it.**
  Add the values that [config-forge-tmp.yaml](../templates/config-forge-tmp.yaml) has and that the file does not have, as `agencies`, `workBranches` and `keepEnglishChore`.
  Write each path of this computer as a placeholder, for example `{wikiDir}`.
  Give its value in `config.local.yaml`.
- **If a chore of the workspace does the same work as a chore of SkillsGestalt, remove its file.**
  Write its row with the name of the chore of SkillsGestalt as text.
  Move its run records to the section `## 執行紀錄` of the summary table, and its reports to `checkpoints/chores/<name>`.
- **Give a name to each chore of its own, as [chore-rules.md](../rules/chore-rules.md) tells.**

## After a Change in SkillsGestalt

A Forge reads SkillsGestalt where it is.
Thus, a change in SkillsGestalt changes the Forge immediately.
After such a change, run the `gen_config.py`, `check_tasks.py` and `check_chores.py` commands of `AGENTS.md` again.
