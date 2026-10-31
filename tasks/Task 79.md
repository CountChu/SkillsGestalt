# Task 79 - 本機分支改名：master 改為 m1，public 改為 main

**Status**：完成——2026-10-30 改好分支名稱，`m1` 從 `main` 重新開始，舊的歷史在 tag `archive/master`；之後每次發佈，[publish_snapshot.py](../.github/common/scripts/publish_snapshot.py) 都讓 `m1` 從新的快照重新開始。
**Raised**：2026-10-30，第二次發佈之後，使用者要把本機的 `public` 改名為 `main`、`master` 改名為 `m1`。
**Depends on**：—

## 1. 背景

[[Task 78]] 把 SkillsGestalt 公開到 GitHub：本機的 `public` 分支放發佈的快照，推到 GitHub 的 `main`；平常工作的 `master` 不推。
使用者要讓本機的名稱對上 GitHub：放快照的分支叫 `main`，工作的分支叫 `m1`。
改名之後，使用者覺得 `m1` 與 `main` 離太遠：兩邊的內容只差幾個檔，但沒有共同的祖先，`m1` 有 527 個 commit，`main` 只有 2 個。
使用者要 `m1` 只留短短的新歷史，並保留只在 `m1` 的檔案。

## 2. 現況

- 本機的 `main`（原本的 `public`）追蹤 `origin/main`，最新的是快照 `cba1032`。
- 工作的分支是 `m1`（原本的 `master`），設了 `branch.m1.pushRemote no_push`，在 `m1` 上 `git push` 會失敗。
- 只有一個 worktree，改名之後工作區直接在 `m1` 上。
- `m1` 的 527 個 commit 存成本機的 annotated tag `archive/master`（`c501a98`），不推。
- 新的 `m1` 接在 `main` 的 `cba1032` 後面，有兩個 commit：`5608f7f` 放回 `external/` 與 `.github/external/`，`4d44a82` 是還沒發佈的變動；內容和 `archive/master` 完全相同，`main` 是它的祖先。

## 3. 要做的

### 已決定（2026-10-30）

- 改名記在本 task；[[Task 78]] 保持完成。
- [[publish-github]] 說明現況的地方改成新名稱，並寫明兩個分支的用途與舊名稱；日誌與執行紀錄是當時的事，照舊。
- 快照 commit 的內文改成 `From m1 <sha>.`。
- [publish_snapshot.py](../.github/common/scripts/publish_snapshot.py) 的 `check` 預設以 `m1` 為來源，快照放在本機的 `main`。
- 不用 rebase：527 個 commit 的內容 `main` 都已經有了，一個一個疊上去只會是衝突與空的 commit。
- 舊的歷史存成 tag `archive/master`，不是分支，免得被 checkout 之後又有人 commit。
- 新的 `m1` 有兩個 commit：先放回不公開的路徑，再放還沒發佈的變動。
- 每次發佈之後都重做 `m1`：`publish` 把舊的歷史存成 `archive/m1-<yymmdd>`，日期是發佈當天，同一天再發佈就蓋掉那天的 tag 並印出原本指的 commit；`m1` 變成快照上的一個 commit；`m1` 在發佈之間有了新的 commit，就不動它。
- 文件裡引用的舊 hash 照舊，在 [[publish-github]] 與根目錄的 [CLAUDE.md](../CLAUDE.md) 寫明到 tag 裡查。

## 4. 驗證

- `git branch -vv`：`m1` 與 `main`，`main` 追蹤 `origin/main`，沒有 `master` 與 `public`。
- `python scripts/publish_snapshot.py check` 以 `m1` 為來源，掃描是 `nothing found`，列出和 `cba1032` 相比的變動。
- `git diff archive/master m1` 在重做之後是空的；`git merge-base --is-ancestor main m1` 成立。
- 在暫用的 clone 試跑 `publish --no-push`：建了快照，`m1` 變成快照上的一個 commit，`git diff main m1` 只有兩個不公開的路徑，內容和舊的 `m1` 相同，工作區沒有變動。

## 5. 與其他 task 的關係

- [[Task 78]]：建立 `public` 分支與發佈的做法；它的紀錄照舊名稱。
- [[publish-github]]：發佈的步驟，改用新名稱。

## 6. 知識

—

## 7. 日誌

### 2026-10-30

- 建立 task：`master` 改名為 `m1`，`public` 改名為 `main`，`m1` 設 `pushRemote no_push`。
- 改 [publish_snapshot.py](../.github/common/scripts/publish_snapshot.py)、[[publish-github]]，在 [[Task 78]] 加上關係與日誌；本 task 完成。
- 使用者覺得 `m1` 與 `main` 離太遠，要 `m1` 只留短短的新歷史：舊的歷史存成 tag `archive/master`，`m1` 從 `cba1032` 重新開始；`publish` 加上每次發佈之後重做 `m1`。
- 使用者要 tag 以發佈當天命名：`archive/m1-258940e` 改名為 `archive/m1-261030`，`publish` 之後建 `archive/m1-<yymmdd>`，同一天再發佈就蓋掉那天的 tag；`archive/master` 照舊。
- [[Task 86]] 把 chore 改用名稱：本檔的 `[[Chore N]]` 連結改成新名稱。
- [[Task 87]] 把 `publish_snapshot.py` 搬進 `.github/common/scripts/`：本檔連到它的連結改成新的路徑。
