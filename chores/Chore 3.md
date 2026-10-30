# Chore 3 - 發佈到 GitHub

**Status**：使用中——每次發佈先跑 `check`，使用者看過變動、同意之後才 `publish`。
**Started**：2026-10-30，SkillsGestalt 公開到 GitHub 之後，發佈要重複做；做法由 [[Task 78]] 定下，也由它建立本 chore。
**When**：使用者要求發佈到 GitHub 時

## 1. 目的

把 master 目前的內容發佈到公開的 repo <https://github.com/CountChu/SkillsGestalt>，而不公開 master 的歷史、本機專用的檔案與公司內部資訊。
master 不推：每次發佈是本機 `public` 分支上的一個快照 commit，只把 `public` 推到 GitHub 的 `main`。
程式不切換分支、也不動工作區，所以其他 session 可以照常在 master 上工作。

## 2. 何時要做

使用者說要發佈、或要更新 GitHub 時。
不自己定期發佈：每次發佈都會公開新的內容，要由使用者確認。
要看有沒有東西可以發佈，執行 `python scripts/publish_snapshot.py check`：它最後列出和上次發佈相比的變動，印出 `no change since the last release` 就不必發佈。

## 3. 怎麼做

### 準備

- 根目錄要有本機的關鍵字檔 `publish-keywords.local.txt`：一行一個不能公開的組織、專案或產品名稱。
  [.gitignore](../.gitignore) 排除它，因為這些名稱本身就不能公開；沒有它，程式不掃描，以 `2` 結束。
  新發現不能公開的名稱，就加進這個檔。

### 步驟

1. 從根目錄執行 `python scripts/publish_snapshot.py check`。
   它做出要公開的 tree，也就是 master 的內容拿掉 `external/` 與 `.github/external/`，掃描每個檔，再列出和上次發佈相比的變動；它不寫入任何東西。
   掃描找的是：email、私有 IP、Azure DevOps 的組織、使用者的家目錄、token 與私鑰、關鍵字檔裡的名稱，以及不該在 tree 裡的路徑。
2. 有 `[FIND]` 就以 `1` 結束：在 master 上改掉那些內容並 commit，再回到第 1 步。
   是誤報的話，改 [publish_snapshot.py](../scripts/publish_snapshot.py) 的允許清單（`EMAIL_ALLOWED`、`ADO_ALLOWED`），不要為了通過掃描而改內容。
3. 把變動清單給使用者看，問要不要發佈；使用者同意之前不推。
4. 執行 `python scripts/publish_snapshot.py publish --source <check 印出的 source> --tree <check 印出的 tree> --co-author "<agent 的名稱與 email>"`。
   它重做一次 tree，和 `check` 那次不同就以 `2` 結束，表示 master 在這之間有了新的 commit，要回到第 1 步。
   相同的話，它再掃描一次，建一個快照 commit 接在 `public` 後面，推到 `origin` 的 `main`。
   作者與 committer 取自 git 的 `user.name` 與 `user.email`。
5. 到 GitHub 確認：`gh api "repos/CountChu/SkillsGestalt/commits?sha=main" --jq '.[0].sha'` 是新的快照，`gh api "repos/CountChu/SkillsGestalt/git/trees/main?recursive=1"` 裡沒有排除的路徑。
6. 在本 chore 的執行紀錄記下這次發佈，並更新摘要表的「上次執行」；commit 以 `chore 3: ` 開頭。

### 已決定的

這些決定來自 [[Task 78]]：

- 本機專用、不進 git：根目錄的 `config.yaml`（範本是 [config.example.yaml](../config.example.yaml)）、`*.mermaid.html` 預覽檔、`publish-keywords.local.txt`。
- 快照排除、master 照舊：`external/` 是 ASD-STE100 規格的 PDF，規格的版權頁寫明不得散布；`.github/external/` 是從外面來的 eli5，原作者與授權不明。
- `ste-dictionary.json` 公開，是使用者的決定。
- GitHub 的預設分支是 `main`；快照 commit 的訊息是 `SkillsGestalt yyyy-mm-dd`，內文寫它取自 master 的哪個 commit。

## 4. 驗證

- `check` 與 `publish` 的掃描都是 `nothing found`。
- GitHub 上 `main` 最新的 commit 是新的快照，只比上次多一個 commit，沒有 master 的歷史。
- GitHub 上的檔案裡沒有 `checkpoints/`、`external/`、`.github/external/`、`config.yaml`、預覽檔與 PDF。

## 5. 與其他 task、chore 的關係

- [[Task 78]]：建立本 chore，也記下公開時做的決定與第一次發佈。
- [[Task 26]]：ASD-STE100 的 PDF 是否留在 git；不論怎麼決定，它都不放進公開版。

## 6. 執行紀錄

### 2026-10-30

- 第一次發佈，在程式寫好之前照 [[Task 78]] 的步驟手動做：以 master 的 `9629f0a` 做出快照 `b2c697a`，建立公開的 repo，推到 `main`。
- 寫好程式之後試跑：`check` 對 master 的 `5c5094a` 是 `nothing found`；對清理之前的 `6cb068b` 找到 101 筆，以 `1` 結束。
