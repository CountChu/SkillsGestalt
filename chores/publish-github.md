# publish-github - 發佈到 GitHub

**Status**：使用中——每次發佈先跑 `check`，使用者看過變動、同意之後才 `publish`。
**Started**：2026-10-30，SkillsGestalt 公開到 GitHub 之後，發佈要重複做；做法由 [[Task 78]] 定下，也由它建立本 chore。
**When**：使用者要求發佈到 GitHub 時
**Private**：只有 SkillsGestalt 做——它發佈的是本 repo 的工作分支到它自己的 GitHub repo，`publish_snapshot.py` 寫死了 `main`、`origin` 與這個 GitHub repo。

## 1. 目的

把本機 work branch 目前的內容發佈到公開的 repo <https://github.com/CountChu/SkillsGestalt>，而不公開 work branch 的歷史、本機專用的檔案與公司內部資訊。
本機有兩種分支：work branch 是平常工作的分支，`main` 只放發佈的快照。
work branch 不寫死：程式用 `--work` 指定的分支，沒指定就用目前 checkout 的分支。
SkillsGestalt 工作區的 work branch 是 `m1`；別的 clone 可以是別的名稱，例如 `countdell`。
work branch 不能是 `main`，HEAD 也不能是 detached。
work branch 不推，要設 `branch.<work branch>.pushRemote no_push`，在它上面 `git push` 會失敗；每次發佈是 `main` 上的一個快照 commit，只把 `main` 推到 GitHub 的 `main`。
不要在本機的 `main` 上 commit。
每次發佈之後，work branch 從新的快照重新開始：舊的歷史存成 tag `archive/<work branch>-<yymmdd>`，日期是發佈當天；同一天再發佈，那天的 tag 改指新的歷史，當天較早的那段之後會被 `git gc` 清掉，程式會印出來，work branch 變成快照上的一個 commit，放回不公開的路徑，所以 `git diff main <work branch>` 只有那些路徑和還沒發佈的變動。
程式不切換分支、也不動工作區，所以其他 session 可以照常在 work branch 上工作。

## 2. 何時要做

使用者說要發佈、或要更新 GitHub 時。
不自己定期發佈：每次發佈都會公開新的內容，要由使用者確認。
要看有沒有東西可以發佈，執行 `python {skillGroups.common}/scripts/publish_snapshot.py check`：它最後列出和上次發佈相比的變動，印出 `no change since the last release` 就不必發佈。

## 3. 怎麼做

### 準備

- 根目錄要有本機的關鍵字檔 `publish-keywords.local.txt`：一行一個不能公開的組織、專案或產品名稱。
  [.gitignore](../.gitignore) 排除它，因為這些名稱本身就不能公開；沒有它，程式不掃描，以 `2` 結束。
  新發現不能公開的名稱，就加進這個檔。

### 步驟

1. 在 work branch 上，從根目錄執行 `python {skillGroups.common}/scripts/publish_snapshot.py check`；不在 work branch 上就加 `--work <work branch>`。
   它先印出用的 `work`，再做出要公開的 tree，也就是 work branch 的內容拿掉 `external/` 與 `.github/external/`，掃描每個檔，再列出和上次發佈相比的變動；它不寫入任何東西。
   掃描找的是：email、私有 IP、Azure DevOps 的組織、使用者的家目錄、token 與私鑰、關鍵字檔裡的名稱，以及不該在 tree 裡的路徑。
2. 有 `[FIND]` 就以 `1` 結束：在 work branch 上改掉那些內容並 commit，再回到第 1 步。
   是誤報的話，改 [publish_snapshot.py](../.github/common/scripts/publish_snapshot.py) 的允許清單（`EMAIL_ALLOWED`、`ADO_ALLOWED`），不要為了通過掃描而改內容。
3. 依 `check` 列出的 commit 寫這次改動的摘要，摘要用英文，一段或幾段，段落之間空一行。
   把摘要寫進 repo 外的一個 UTF-8 檔，例如 scratchpad；只有一行時也可以用 `--summary "<摘要>"`。
   多行的摘要不要用 `--summary`：Windows 上 python 的 `.bat` shim 會在換行處切斷參數。
   把變動清單與摘要給使用者看，問要不要發佈；使用者同意之前不推。
4. 執行 `python {skillGroups.common}/scripts/publish_snapshot.py publish --work <check 印出的 work> --source <check 印出的 source> --tree <check 印出的 tree> --summary-file <摘要檔> --co-author "<agent 的名稱與 email>"`。
   它重做一次 tree，和 `check` 那次不同就以 `2` 結束，表示 work branch 在這之間有了新的 commit，要回到第 1 步。
   相同的話，它再掃描一次，建一個快照 commit 接在本機的 `main` 後面，推到 `origin` 的 `main`。
   最後它讓 work branch 從新的快照重新開始，commit 以 `chore publish-github: ` 開頭；work branch 在這之間有了新的 commit 時，它不動 work branch，只印出來，work branch 留著原本的歷史，到下次發佈再重新開始。
   作者與 committer 取自 git 的 `user.name` 與 `user.email`。
5. 到 GitHub 確認：`gh api "repos/CountChu/SkillsGestalt/commits?sha=main" --jq '.[0].sha'` 是新的快照，`gh api "repos/CountChu/SkillsGestalt/git/trees/main?recursive=1"` 裡沒有排除的路徑。
6. 在摘要表 `## 執行紀錄` 的 `### publish-github` 下記下這次發佈，並更新摘要表的「上次執行」；commit 以 `chore publish-github: ` 開頭。

### 已決定的

這些決定來自 [[Task 78]]：

- 本機專用、不進 git：根目錄的 `config.yaml`（範本是 [config.example.yaml](../config.example.yaml)）、`*.mermaid.html` 預覽檔、`publish-keywords.local.txt`。
- 快照排除、work branch 照舊：`external/` 是 ASD-STE100 規格的 PDF，規格的版權頁寫明不得散布；`.github/external/` 是從外面來的 eli5，原作者與授權不明。
- `ste-dictionary.json` 公開，是使用者的決定。
- 每次發佈之後都重做 work branch，讓它的歷史一直很短；舊的歷史留在本機的 tag，不推。
- GitHub 的預設分支是 `main`；快照 commit 的訊息是 `SkillsGestalt yyyy-mm-dd`，內文先寫這次改動的摘要，再寫它取自哪個 work branch 的哪個 commit。

## 4. 驗證

- `check` 與 `publish` 的掃描都是 `nothing found`。
- GitHub 上 `main` 最新的 commit 是新的快照，只比上次多一個 commit，沒有 work branch 的歷史。
- GitHub 上的檔案裡沒有 `checkpoints/`、`external/`、`.github/external/`、`config.yaml`、預覽檔與 PDF。

## 5. 與其他 task、chore 的關係

- [[Task 78]]：建立本 chore，也記下公開時做的決定與第一次發佈。
- [[Task 79]]：把本機分支 `master` 改名為 `m1`、`public` 改名為 `main`，並讓 `m1` 從 `main` 重新開始。
- [[Task 26]]：ASD-STE100 的 PDF 留在 `m1` 的 git，不放進公開版（2026-10-30 決定）。
