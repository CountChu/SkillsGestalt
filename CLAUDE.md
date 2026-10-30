# SkillsGestalt

Instructions for an agent that works in this workspace.

- **A Markdown file with a `-tw.md` beside it has a 繁體中文 twin, and a change to the English file goes into the twin in the same run.**
  Update the twin with the [chinese](.github/common/skills/chinese/SKILL.md) skill: it translates only what changed since the twin's last commit, then checks the two against each other.
- **When you create or edit a Markdown file in the repo, follow [md-style.md](.github/common/rules/md-style.md).**

## Branches

平常在 `m1` 上工作；本機的 `main` 只放發佈到 GitHub 的快照，不要在上面 commit。
2026-10-30 之前的 commit 在 tag `archive/master`，之後每次發佈前的在 `archive/m1-<快照>`：文件裡引用的舊 hash 到那裡查。
發佈照 [Chore 3](chores/Chore%203.md) 的步驟。

## Tasks

跨 session 的待辦在 `tasks/`，摘要表在 `dashboard/task-summary.md`。
要新增或修改 task，照 [task-rules.md](.github/common/rules/task-rules.md) 做。
規則裡的 `{skillGroups.common}` 照根目錄的 `config.yaml`（不進 git，範本是 [config.example.yaml](config.example.yaml)），在這個 workspace 是 `.github/common`，所以改完後從根目錄執行：

```bash
python .github/common/scripts/check_tasks.py --summary dashboard/task-summary.md --tasks-dir tasks
```

## Chores

會重複做的例行工作在 `chores/`，摘要表在 `dashboard/chore-summary.md`：先讀這張表，看哪一項該做了。
要新增、修改或執行 chore，照 [chore-rules.md](.github/common/rules/chore-rules.md) 做。
改完後從根目錄執行：

```bash
python .github/common/scripts/check_chores.py --summary dashboard/chore-summary.md --chores-dir chores
```
