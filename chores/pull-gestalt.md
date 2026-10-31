# pull-gestalt - 把 GitHub 上的新快照拿進工作分支

**Status**：使用中——先 `git fetch`，`incoming` 掃描新的快照與它的作者，使用者同意之後，本機 `main` 移到 `origin/main`，工作分支 rebase 上去。
**Started**：2026-10-31，另一台電腦的 SkillsGestalt 以 `countdell` 為工作分支，也發佈快照到同一個 GitHub repo；由 [[Task 89]] 建立。
**When**：發佈之前、git fetch 看到新快照時，或使用者要求時
**Private**：只有 SkillsGestalt 做——它把 SkillsGestalt 自己的 GitHub repo 的快照拿進本 repo 的工作分支，用的 `publish_snapshot.py` 寫死了 SkillsGestalt 的值。

## 1. 目的

SkillsGestalt 可能在不只一台電腦上，各有自己的工作分支，例如本機的 `m1` 與另一台的 `countdell`，都照 [[publish-gestalt]] 發佈到 GitHub 的 `main`。
一台發佈之後，另一台的 `main` 與工作分支就落後了；本 chore 把新的快照拿進來，讓工作分支接在它上面，下一次發佈才不會被拒絕或蓋掉別台的快照。

## 2. 何時要做

- 每次做 [[publish-gestalt]] 之前。
- 從根目錄跑 `git fetch origin`，再跑 `python {skillGroups.common}/scripts/publish_snapshot.py incoming`：印出 `nothing to pull` 就不必做。
- 使用者要求時。

## 3. 怎麼做

以下的 `<work>` 是本 clone 的工作分支，例如 `m1` 或 `countdell`；`<yymmdd>` 是當天。

1. 確認在 `<work>` 上，`git status` 沒有任何變動。
2. 跑 `git fetch origin`，再跑 `python {skillGroups.common}/scripts/publish_snapshot.py incoming`。
   它列出 `origin/main` 新的快照與改了哪些檔，掃描新快照的檔案，以及每個新 commit 的作者與 committer；它不寫入任何東西。
   印出 `diverged` 時，表示 GitHub 的 `main` 被改寫過，例如換掉了某個快照的作者；照下面的步驟做一樣處理得到。
3. 有 `[FIND]` 就停下來告訴使用者：檔案裡有公司內部的資訊，或作者、committer 是工作的身分。
   作者的問題要在發佈那台電腦改 git 的 `user.name` 與 `user.email`；GitHub 上已經公開的 commit 要不要改寫，由使用者決定。
4. 把新的快照與變動清單給使用者看，問要不要拿進來；使用者同意之前，不動 `main` 與 `<work>`。
5. 記下本機原本的 `main`：`git rev-parse main`。
   把舊的 `<work>` 存成 tag：`git tag -a -f archive/<work>-<yymmdd>-pull -m "The history of <work> before pull-gestalt" <work>`。
6. 本機的 `main` 移到 `origin/main`：`git branch -f main origin/main`。
7. 把 `<work>` rebase 到新的 `main`：`git rebase --onto main <第 5 步記下的 main> <work>`。
   衝突時停下來，把衝突的檔給使用者看，問怎麼解；`dashboard/` 的摘要表通常是兩邊都留。
8. 確認不公開的路徑還在：`git diff --name-status main <work>` 要有 `external/` 與 `.github/external/`。
9. 從根目錄跑 `python {skillGroups.common}/scripts/gen_claude_md.py`，再跑 CLAUDE.md 給出的 `check_tasks.py` 與 `check_chores.py`。
   新快照改了規則或格式時，只在 `<work>` 上的檔可能過不了，例如還沒發佈的 task；照新快照的 `CHANGES.md` 改它們。
10. 在摘要表 `## 執行紀錄` 的 `### pull-gestalt` 下記一筆：拿進來的快照、tag、衝突與改了什麼；摘要表的「上次執行」改成當天。
    commit 以 `chore pull-gestalt: ` 開頭。

## 4. 驗證

- `python {skillGroups.common}/scripts/publish_snapshot.py incoming` 印出 `nothing to pull`。
- `main` 是 `<work>` 的祖先，`git diff --name-status main <work>` 只有不公開的路徑與還沒發佈的改動。
- `gen_claude_md.py --check`、`check_tasks.py` 與 `check_chores.py` 都是 PASS。

## 5. 與其他 task、chore 的關係

- [[Task 89]]：建立本 chore 與 `publish_snapshot.py incoming`。
- [[publish-gestalt]]：發佈之前先做本 chore。
- [[follow-gestalt]]：給 Forge 做的 chore；本 chore 是 SkillsGestalt 自己的另一份 clone 跟上 GitHub。
