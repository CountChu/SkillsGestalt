# Task 89 - 設計 chore pull-gestalt：把 GitHub 上的新快照拿進 m1

**Status**：完成——2026-10-31 寫好 chore [[pull-gestalt]] 與 `publish_snapshot.py incoming`，發佈前也檢查作者與 committer；GitHub 上的 `4765af0` 經使用者同意改寫成 `4d2c5db`，本機 `main` 與 `m1` 照 pull-gestalt 的步驟拿進來；另一台電腦要照它重設 `main`。
**Raised**：2026-10-31，另一台電腦的 SkillsGestalt 以 `countdell` 為工作分支，已經發佈了一個快照到 GitHub；使用者要本機的 `m1` 從 GitHub 拿到這些更新。
**Depends on**：—

## 1. 背景

- 本機的工作分支是 `m1`，本機的 `main` 只放發佈的快照；[[publish-gestalt]] 把 `m1` 做成快照，推到 GitHub 的 `main`，再讓 `m1` 從新的快照重新開始。
- 另一台電腦也有一份 SkillsGestalt，工作分支是 `countdell`，也照 [[publish-gestalt]] 發佈到同一個 GitHub repo 的 `main`。
- 兩台都發佈時，GitHub 的 `main` 會有另一台的快照，本機的 `main` 與 `m1` 都還沒有它；目前沒有 chore 說明怎麼把它拿進來。

## 2. 現況

### GitHub 上的新快照（2026-10-31）

- 本機最後一次發佈是 `93b4e1e`，取自 `m1` 的 `b2e967f`；之後 `m1` 從 `93b4e1e` 重新開始，現在在 `20d9b22`。
- GitHub 的 `main` 在 `93b4e1e` 之後多了 `4765af0`，訊息寫明取自 `countdell` 的 `96b7534`，改了 124 個檔，主要是：
  - task 多了狀態「取消」與一章「6. 知識」，日誌改成第 7 章；task 規則允許摘要表和 task 放在不同的地方。
  - `config.yaml` 可以設定 tasks 與 chore 摘要的位置，`gen_claude_md.py` 與 `check_chores.py` 會用這些值。
  - `publish_snapshot.py` 的工作分支取自 `--work` 或目前 checkout 的分支，不再寫死 `m1`；快照訊息可以帶摘要；[[publish-gestalt]] 跟著改。
- `m1` 與 `origin/main` 的共同祖先是 `93b4e1e`；本機的 `main` 還在 `93b4e1e`。
- `4765af0` 的作者 email 是工作 email，已經公開在 GitHub 上；[[Task 78]] 當時決定快照的作者用個人 email，就是為了不公開它。
  `publish_snapshot.py` 的掃描只看檔案內容，不看 commit 的作者與 committer。
  本 task 檔也會公開，所以這裡不寫出那個 email。

### 2026-10-31 做完之後

- GitHub：經使用者同意，做出和 `4765af0` 同樣檔案、parent、訊息與時間，作者與 committer 改成 CountChu 個人 email 的 `4d2c5db`，以 `git push --force-with-lease=main:4765af0` 換掉；GitHub 上五個快照的作者現在都是個人 email。
  舊的 `4765af0` 不在 `main` 上了，但 GitHub 可能還保留一段時間，知道 hash 的人仍查得到。
- 本機：`main` 從 `93b4e1e` 移到 `4d2c5db`；舊的 `m1`（`e0365fc`）存成 tag `archive/m1-261031-pull`；`m1` 的 3 個 commit rebase 上去，沒有衝突；`external/` 與 `.github/external/` 仍在。
  新快照把 task 改成七章，本 task 插入 `6. 知識`；`CLAUDE-local.md` 改了，CLAUDE.md 重新產生。
- [publish_snapshot.py](../.github/common/scripts/publish_snapshot.py)：
  - `check` 與 `publish` 也用關鍵字檔掃描 git 會寫的作者與 committer（`git var GIT_AUTHOR_IDENT`、`GIT_COMMITTER_IDENT`），抓到就不發佈；`[FIND]` 只寫出是哪一欄，不印出值。
  - 新的子指令 `incoming`：在 `git fetch` 之後，列出 `origin/main` 有、本機 `main` 沒有的快照與改了哪些檔，掃描新快照的檔案與每個新 commit 的作者與 committer；`main` 與 `origin/main` 分岔時說明 GitHub 的歷史被改寫過；它不寫入任何東西。
- [[pull-gestalt]]：private chore，步驟是 `git fetch`、`incoming`、有 `[FIND]` 就停、給使用者看、記下原本的 `main`、存 tag `archive/<work>-<yymmdd>-pull`、`git branch -f main origin/main`、`git rebase --onto main <原本的 main> <work>`、確認不公開的路徑、重新產生 CLAUDE.md 並跑檢查、記執行紀錄；步驟用 `<work>`，不寫死 `m1`，另一台的 `countdell` 也照它做，包括 `main` 分岔的情況。
- [[publish-gestalt]] 的「準備」加上「先做 pull-gestalt」。
- 摘要表加上 pull-gestalt，執行紀錄記下這一次。

## 3. 要做的

### 已決定（2026-10-31）

- chore 叫 `pull-gestalt`，定義在本 repo 的 `chores/pull-gestalt.md`。
- 做法：`git fetch origin`；本機 `main` 快轉到 `origin/main`；`m1` rebase 到新的快照上。
- merge 之前先列出變動給使用者看，也掃描一次有沒有公司內部的資訊；使用者同意之後才動 `main` 與 `m1`。
- 和 [[follow-gestalt]] 分開：pull 完接著做 follow-gestalt，處理 `CHANGES.md` 的新條目。
- [[publish-gestalt]] 的第一步先做 pull-gestalt：本機 `main` 落後 `origin/main` 時，push 會被拒絕，或蓋掉另一台的快照。
- `4765af0` 作者 email 的問題記在本 task，處理方式另外決定。

### 開始做時決定的（2026-10-31）

- 何時要做：發佈之前、`git fetch` 看到新的快照時，或使用者要求時。
- 先照手動步驟把 `4765af0` 拿進來，再寫 chore：新快照改了 `publish_snapshot.py`、task 規則與 [[publish-gestalt]]，chore 與程式才寫在新版上。
- 拿進來的步驟寫成 chore 裡的 git 指令；只有需要讀關鍵字檔的掃描用程式，所以 `publish_snapshot.py` 多了唯讀的 `incoming`。
- rebase 之前把舊的工作分支存成 `archive/<work>-<yymmdd>-pull`，和發佈的 tag 分開；同一天再做就蓋掉。
- 衝突時兩邊都留；這次沒有衝突。
- 作者 email：發佈前檢查作者與 committer、`incoming` 也檢查新 commit 的作者，並改寫 GitHub 上的 `4765af0`，作者與之前的快照一樣是 CountChu 的個人 email。
- 另一台電腦的 `main` 與 `countdell` 建在舊的 `4765af0` 上：pull-gestalt 的步驟在 `main` 分岔時一樣處理得到。

### 步驟

1. 決定「要決定的」各項。
2. 寫 `chores/pull-gestalt.md`，摘要表加一列；需要程式就放進 `{skillGroups.common}/scripts/`。
3. [[publish-gestalt]] 的步驟加上「先做 pull-gestalt」。
4. 照 pull-gestalt 把 `4765af0` 拿進本機的 `main` 與 `m1`，再做 [[follow-gestalt]]。

## 4. 驗證

- 本機的 `main` 等於 `origin/main`，`m1` 以它為祖先；`m1` 仍有不公開的路徑，自己的 commit 都在。
- `check_tasks.py`、`check_chores.py` 與 `gen_claude_md.py --check` 都是 PASS。
- `publish_snapshot.py check` 列出的變動，只有 `m1` 在新快照之後的 commit。

2026-10-31 的結果：

- 改寫前用 `publish_snapshot.py` 的掃描看 `4765af0` 的檔案：nothing found，問題只在作者與 committer；`4d2c5db` 的 tree 與訊息和它逐位元組相同。
- `gh api` 確認 GitHub 的 `main` 是 `4d2c5db`，五個快照的作者都是個人 email。
- `incoming`：本機已拿進來時印出 `nothing to pull`；以舊的 `93b4e1e` 與 `4765af0` 試，列出 124 個變動的檔，並對 `4765af0` 的作者與 committer 各報一個 `[FIND]`。
- `check`：作者或 committer 的 email 用工作網域時各報一個 `[FIND]`；平常是 nothing found。
- `check_tasks.py`、`check_chores.py` 與 `gen_claude_md.py --check` 都是 PASS；`git diff --name-status main m1` 只有不公開的兩個路徑與 `m1` 自己的改動。

## 5. 與其他 task 的關係

- [[Task 78]]：公開到 GitHub，決定快照的作者用個人 email。
- [[Task 79]]：`m1` 與 `main` 的分工，以及發佈之後 `m1` 從新的快照重新開始。
- [[Task 87]]：chore 沒有自己的程式。
- [[Task 88.3]]：`CHANGES.md` 與 [[follow-gestalt]]。
- [[pull-gestalt]]：本 task 建立的 chore。
- 另一台電腦的 SkillsGestalt 要照 [[pull-gestalt]] 重設 `main`，並把 `countdell` rebase 到 `4d2c5db`；它的 git `user.email` 也要改成個人 email，在那台電腦做。

## 6. 知識

—

## 7. 日誌

### 2026-10-31

- 建立 task：fetch 之後發現 GitHub 的 `main` 有另一台電腦從 `countdell` 發佈的 `4765af0`；決定 chore 叫 pull-gestalt，`m1` rebase 到新的快照上，merge 前給使用者確認，publish-github 先做它；`4765af0` 的作者是工作 email，記在本 task。
- 開始做並完成：經使用者同意改寫並 force push GitHub 上的 `4765af0`；照手動步驟拿進本機；寫好 [[pull-gestalt]] 與 `publish_snapshot.py` 的作者檢查與 `incoming`。
- [[Task 91]] 把 chore `publish-github` 改名為 `publish-gestalt`：本檔的連結跟著改，意思不變。
