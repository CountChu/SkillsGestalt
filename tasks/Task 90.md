# Task 90 - 快照的作者與 committer 由 publish_snapshot.py 指定

**Status**：完成——2026-10-31 `publish_snapshot.py` 以 `IDENTITY` 做快照 commit，`check` 印出它並檢查它；檔案的掃描只放過 `IDENTITY` 的 email；[[publish-gestalt]] 跟著改。
**Raised**：2026-10-31，[[Task 89]] 之後，使用者問發佈到 GitHub 時能不能指定 CountChu 的個人身分，不靠每台電腦的 git 設定。
**Depends on**：[[Task 89]]

## 1. 背景

- 快照 commit 的作者與 committer 現在取自發佈那台電腦的 git `user.name` 與 `user.email`。
- 另一台電腦的 git 設定是工作的身分，所以它發佈的 `4765af0` 把工作 email 公開在 GitHub 上；[[Task 89]] 改寫了它，並讓 `publish_snapshot.py` 在發佈前用關鍵字檔檢查作者與 committer。
- 但每台電腦都要記得設對 git，設錯就要靠檢查擋下來。
- `publish_snapshot.py` 只服務 private chore [[publish-gestalt]]，SkillsGestalt 的值本來就寫在裡面；這個身分也已經公開在 GitHub 上的每個快照。

## 2. 現況

- `publish` 以 `git commit-tree` 做出快照 commit，身分取自 git 的設定。
- 作者檢查掃描 `git var GIT_AUTHOR_IDENT` 與 `GIT_COMMITTER_IDENT`，也就是那台電腦的 git 設定。
- [[publish-gestalt]] 的步驟寫「作者與 committer 取自 git 的 `user.name` 與 `user.email`」。

### 2026-10-31 做完之後

- [publish_snapshot.py](../.github/common/scripts/publish_snapshot.py)：
  - 常數 `IDENTITY = ('CountChu', '<個人 email>')`，和 `BRANCH`、`REMOTE` 放在一起；`publish` 做快照 commit 時，以它設定 `GIT_AUTHOR_NAME`、`GIT_AUTHOR_EMAIL`、`GIT_COMMITTER_NAME`、`GIT_COMMITTER_EMAIL`。
  - 讓工作分支重新開始的 commit 照舊用 git 的設定。
  - `check` 與 `publish` 印出 `identity:`，並以關鍵字檔檢查 `IDENTITY`；`[FIND]` 的提示是「改 `publish_snapshot.py` 的 `IDENTITY`」；`incoming` 的提示仍是發佈那台電腦要設 git。
  - 檔案的掃描放過 `IDENTITY` 的那一個 email：它就寫在這支程式裡，而且每個快照都帶著它；其他 gmail 的 email 照舊會被找出來。
- [[publish-gestalt]]：第 4 步改成快照的作者與 committer 是 `IDENTITY`，不受 git 設定影響，重新開始的 commit 仍用 git 的設定。

### 2026-10-31 config.yaml 的 identity

- 使用者要求：`config.yaml` 有 `identity` 時，覆寫程式裡的 `IDENTITY`。
- `config.yaml` 的寫法是 `identity:` 底下 `name:` 與 `email:` 兩個鍵；只寫一個時以 `2` 結束，不和程式的值混用。
- 程式自己讀這一段，不需要 PyYAML；`check` 印出 `identity: … from config.yaml` 或 `from publish_snapshot.py`。
- `config.yaml` 的身分一樣以關鍵字檔檢查，提示改成「改 config.yaml 的 identity」；檔案的掃描放過程式的 `IDENTITY` 與實際使用的那一個 email。
- [config.example.yaml](../config.example.yaml) 加上註解掉的範例，用 `you@example.com`；[[publish-gestalt]] 第 4 步跟著改。
- 暫用 clone 試過四種情況：有 `identity` 時快照用它、重新開始的 commit 仍用 git 設定；只有 `name` 時以 `2` 結束；工作網域的 email 報兩個 `[FIND]`；沒有 `identity` 時用程式的值。

## 3. 要做的

### 已決定（2026-10-31）

- `publish_snapshot.py` 加一個常數 `IDENTITY`，值是 GitHub 上的快照一直用的 CountChu 與個人 email；`publish` 做快照 commit 時，以它設定作者與 committer。
- 只有推到 GitHub 的快照用 `IDENTITY`；發佈之後讓工作分支重新開始的那個 commit 不推出去，照舊用各台電腦的 git 設定。
- 作者檢查改成檢查快照實際用的身分，也就是 `IDENTITY`；各台電腦的 git 設定不再擋發佈。
  `IDENTITY` 被改成工作的身分時，檢查仍會擋下。
- `check` 印出快照會用的身分，給使用者看變動時一起確認。
- [[publish-gestalt]] 的那句改成「快照的作者與 committer 是 `publish_snapshot.py` 的 `IDENTITY`」，並說明重新開始的 commit 仍用 git 的設定。

### 開始做時決定的（2026-10-31）

- `IDENTITY` 寫成名字與 email 分開的 tuple。
- 不留參數改用別的身分：要改就改常數，經過 commit。
- 在暫用的 clone 設定別的 git 身分，跑 `publish --no-push` 測試。
- 不記進 `CHANGES.md`：`publish_snapshot.py` 只服務 private chore，Forge 不必做任何事。
- 做完先不發佈。

### 步驟

1. `publish_snapshot.py`：加 `IDENTITY`，`publish` 以它做快照 commit；作者檢查與 `check` 的輸出跟著改。
2. [[publish-gestalt]] 的步驟跟著改。
3. 在暫用的 clone 以 `publish --no-push` 試：git 設定是別的身分時，快照的作者與 committer 仍是 `IDENTITY`；重新開始的 commit 用 git 的設定。

## 4. 驗證

- `check` 印出 `IDENTITY`，掃描是 nothing found。
- 暫用的 clone 裡，`publish --no-push` 做出的快照，`git log --format='%an <%ae> / %cn <%ce>'` 是 `IDENTITY`，不受 git 設定影響。
- 把 `IDENTITY` 暫時改成含關鍵字的身分，`check` 報 `[FIND]`。
- `check_tasks.py` 與 `check_chores.py` 是 PASS。

2026-10-31 的結果：

- 第一次在暫用 clone 試時，檔案的掃描把程式裡新寫的個人 email 當成要擋的 email，`publish` 在做快照之前就停了；改成只放過 `IDENTITY` 的 email 之後再試。
- 暫用 clone 的 git 設定是另一個身分：`check` 印出 `IDENTITY`，nothing found；`publish --no-push` 做出的快照，作者與 committer 都是 `IDENTITY`，parent 是 `4d2c5db`；讓 `m1` 重新開始的 commit 是 git 設定的身分。
- 把 `IDENTITY` 改成工作網域的 email：`check` 報作者與 committer 兩個 `[FIND]`，提示改 `IDENTITY`。
- 本機：`check` 印出 `IDENTITY`，nothing found。

## 5. 與其他 task 的關係

- [[Task 89]]：改寫 `4765af0`，加上作者檢查與 [[pull-gestalt]]。
- [[Task 78]]：決定快照的作者用個人 email。
- 另一台電腦拿到本 task 的改動之後，發佈就不再受它的 git 設定影響。

## 6. 知識

—

## 7. 日誌

### 2026-10-31

- 建立 task：快照的身分由 `publish_snapshot.py` 的 `IDENTITY` 指定，只用在推到 GitHub 的快照；作者檢查改成檢查它；`check` 印出它。
- 開始做並完成：`IDENTITY` 做快照、`check` 印出並檢查它，檔案的掃描只放過它的 email；在暫用 clone 試過。
- `config.yaml` 的 `identity` 覆寫 `IDENTITY`：`name` 與 `email` 兩個都要寫，一樣以關鍵字檔檢查，`check` 印出它的來源。
- [[Task 91]] 把 chore `publish-github` 改名為 `publish-gestalt`：本檔的連結跟著改，意思不變。
