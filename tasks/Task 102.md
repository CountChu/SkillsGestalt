# Task 102 - publish_snapshot.py 改成可以設定，讓 Forge 也能照 publish-gestalt、pull-gestalt 發佈快照

**Status**：完成——`publish_snapshot.py` 讀根目錄 `config.yaml` 的 `publish:`；沒有這一節時，SkillsGestalt 的輸出和改之前一樣。
**Raised**：2026-11-10，一個工作用的 Forge 要它的工作分支不推、遠端只放快照，做法和 SkillsGestalt 一樣（那個 Forge 的 Task 24）。
**Depends on**：—

## 1. 背景

- `publish_snapshot.py`（[skill-groups/common/scripts/publish_snapshot.py](../skill-groups/common/scripts/publish_snapshot.py)）由 [[publish-gestalt]] 與 [[pull-gestalt]] 使用，兩個 chore 都標成 Private：只有 SkillsGestalt 做。
- 那個 Forge 的 remote 是公司內部的 Azure DevOps repo，不是 GitHub；它也要：
  - 本機工作分支 `countdell` 不推；
  - 一個本機的快照分支（不是 `main`），推到遠端的一個使用者分支；
  - 遠端只有一串快照，工作分支的歷史只留在本機的 `archive/` tag；
  - 發佈前掃描 email 與 token；
  - 不只一台電腦推到同一個遠端分支（另一台的工作分支是 `devbox`），所以也要 pull。
- 本 task 會公開到 GitHub，所以不寫那個 Forge 的名稱與它的分支名稱：它們在 `publish-keywords.local.txt` 裡。

## 2. 結論

- `publish_snapshot.py` 從根目錄 `config.yaml` 的 `publish:` 讀分支、remote、排除的路徑、掃描與快照標題；沒寫的 key 用 SkillsGestalt 的值（`3.2`）。
- SkillsGestalt 沒有 `publish:`：改前改後的 `check` 與 `incoming` 輸出一字不差（`3.3`）。
- 用那個 Forge 的設定，在 scratch 的 clone 與 bare repo 上做完一整輪：`check --orphan`、`publish --orphan`（force push，換掉 215 個 commit）、DevBox 發佈、`incoming`、過期的 force push 被拒絕（`3.3`）。
- 順手修了兩個問題：push 失敗時快照分支留在沒推出去的快照上；`sk-` 在字中間也被當成 token（`3.2`）。
- chore 仍是 Private；Forge 照它們寫自己的 chore。`CHANGES.md` 記了一筆「Forge 要做的」（`3.4`）。
- 那個 Forge 的真實掃描結果（email 的誤報與真的 email）留給它的 Task 24 處理（`3.3`）。

## 3. 過程

### 3.1 寫死的值（2026-11-10 讀取）

**表 1：`publish_snapshot.py` 寫死的值與那個 Forge 要的值**

| 值 | 現在（SkillsGestalt） | 那個 Forge |
| --- | --- | --- |
| `BRANCH`：本機快照分支 | `main` | 不能是 `main`（遠端的 `main` 是產品程式碼） |
| `REMOTE, REMOTE_BRANCH` | `origin`、`main` | `origin`、一個使用者分支 |
| `EXCLUDED`：快照拿掉的路徑 | `external`、`skill-groups/external`、`skill-groups/archived` | 沒有 |
| `PRIVATE_PATH`：不該在 tree 裡的路徑 | `checkpoints/`、`config.yaml`、PDF 等 | `config.yaml` 與 PDF 在那個 Forge 是進 git 的 |
| 掃描 | email、私有 IP、ADO 組織、家目錄、token 與私鑰、關鍵字 | 只要 email 與 token；ADO 網址、SUT 的 IP 與家目錄在 Forge 的 skill 裡到處都是，是正常內容 |
| 關鍵字檔 | 沒有就以 `2` 結束 | 不掃關鍵字，不需要 |
| `IDENTITY`：快照的作者 | `CountChu` 與個人 email | 公司的身分 |
| 快照標題 | `SkillsGestalt yyyy-mm-dd` | Forge 自己的名稱 |
| restart commit | `chore publish-gestalt: ...` | 可以是 Forge 自己的 chore |
| 根目錄 | 從 script 自己的位置往上找 `config.yaml`，在 Forge 執行時找到 SkillsGestalt | 要是執行所在的 workspace |
| 第一次發佈 | 快照接在本機 `main` 後面 | 遠端分支已有完整的歷史，快照接上去的話遠端就不是「只有快照」 |
| GitHub 的確認步驟 | `gh api` 讀 GitHub | 遠端是 Azure DevOps，不能用 `gh` |

### 3.2 改了什麼

- `config_section()` 用手讀 `config.yaml` 的一節（script 不用 YAML 套件）：一層 key，值是一個字、`[a, b]`，或下面每行一個 `- item`；`identity:` 也改用它讀。
- `configure()` 照 `publish:` 改這些值：`name`、`chore`、`branch`、`remote`、`remoteBranch`、`excluded`、`privatePaths`、`scans`、`keywords`、`emailAllowed`。
  不認得的 key、值的形式不對（例如 `branch: [a, b]`、`excluded: one`）、不認得的掃描、同一個 key 寫兩次，都以 `2` 結束。
- 掃描照 `scans` 做；沒有 `keyword` 就不讀關鍵字檔。有 `publish:` 時，email 只放過快照自己的 `identity`。
- 根目錄：`--workspace`，或從目前的目錄往上、最近一個 `config.yaml` 有 `skillGroups` 的目錄；script 在那裡執行，命令列給的路徑先從目前的目錄解析。
- `--orphan`（`check` 與 `publish`）：快照沒有 parent；`check` 印出 push 會換掉遠端幾個 commit；push 用 `--force-with-lease=refs/heads/<remoteBranch>:<上次 fetch 看到的 commit>`。
- push 失敗時，快照分支移回原位、工作分支不動，以 `2` 結束，並說要先 fetch、必要時先 pull。
- `excluded: []` 時不跑 `git rm`（沒有路徑時 git 會失敗）；restart commit 說這次沒有排除的路徑。
- `SECRET` 的 `sk-` 前面不能是字母或數字。
- 改了 [config.example.yaml](../config.shared.yaml)（`publish:` 的範例，註解掉）、[[publish-gestalt]] 與 [[pull-gestalt]] 的 Private 說明、publish-gestalt 第 2 步的允許清單、`skill-groups/common/CHANGES.md`。

### 3.3 驗證

- SkillsGestalt（沒有 `publish:`）：改前存下 `check` 與 `incoming` 的輸出，改後在根目錄與 `skill-groups\` 下各跑一次，`Compare-Object` 沒有差異。
  改之前的 `check` 就對本 task 報了 16 個 keyword：初稿寫了那個 Forge 的名稱，所以改寫成現在的樣子。
- 那個 Forge 的設定（`scans: [email, token]`、`excluded: []`、公司身分），在 scratch 裡的 clone 與 bare repo 上，真的 repo 與遠端都沒動：
  - `check --orphan`：737 個檔，印出 push 會換掉遠端的 215 個 commit。
  - 掃描有 20 個 finding：Redfish 的欄位名（一個字後面接 `@odata.count` 一類）被當成 email、`sk-` 在字中間（已修），以及兩三個檔裡真的公司 email。測試時以 `emailAllowed` 放過，真的設定由那個 Forge 決定。
  - `publish --orphan`：遠端只剩 1 個快照，作者是公司身分；工作分支從快照重新開始，舊歷史在 `archive/countdell-261110`；之後的 `check` 印出 `no change`，`incoming` 印出 `nothing to pull`。
  - 從 bare repo clone 一份當 DevBox，工作分支 `devbox`：一般的 `publish` 接在快照後面；回到第一份 fetch 後，`incoming` 列出那個快照與它加的檔。
  - 第一份沒 fetch 就 `publish --orphan`：push 因 stale info 被拒絕，快照分支與工作分支都留在原位，以 `2` 結束。

### 3.4 chore 怎麼給 Forge 用

- publish-gestalt、pull-gestalt 仍是 Private：它們發佈到 SkillsGestalt 自己的 GitHub repo，第 5 步用 `gh` 確認，而 Forge 的 remote 不一定是 GitHub。
- Forge 照它們寫自己的 chore，在 `config.yaml` 寫 `publish:` 與 `identity:`；`CHANGES.md` 2026-11-10 那一筆寫了這件事。

## 4. 要做的

1. ✅ 讀完 `publish_snapshot.py`，列出所有寫死、和 SkillsGestalt 有關的值（表 1）。
2. ✅ 訂 `config.yaml` 的設定格式，寫進 [config.example.yaml](../config.shared.yaml)。
3. ✅ 改 `publish_snapshot.py`：讀設定、預設值等於現在的值；掃描可以選。
4. ✅ 在 SkillsGestalt 跑一次 `check` 與 `incoming`，結果和改之前一樣。
5. ✅ 決定 chore 怎麼給 Forge 用；在 `CHANGES.md` 寫一筆「Forge 要做」。

## 5. 驗證

- ✅ SkillsGestalt 沒有 `publish:` 設定時，`check` 的輸出和改之前一樣。
- ✅ 用那個 Forge 的設定跑 `check`，只掃 email 與 token，tree 裡沒有排除的路徑。

## 6. 與其他 task 的關係

- 那個 Forge 的 Task 24：要用本 task 改好的 script，在它的 `config.yaml` 寫 `publish:`，寫自己的 chore。
- [[Task 78]]、[[Task 89]]：建立 publish-gestalt、pull-gestalt 與 `publish_snapshot.py`。

## 7. 知識

- `git push --force-with-lease=<ref>:<commit>` 只在遠端的 ref 還在 `<commit>` 時才覆寫；`<commit>` 是空的表示遠端不能有這個 ref。
- PowerShell 的 `cd` 不改 .NET 的目前目錄：`[IO.File]::ReadAllText('config.yaml')` 讀的是 process 啟動時的目錄，要給絕對路徑。

## 8. 日誌

### 2026-11-10

- 建立 task：讀 `publish_snapshot.py` 寫死的值，對照那個 Forge 要的值，寫成表 1 與 `3.2`。
- 那個 Forge 的本機快照分支定了名稱，改表 1 與 `1. 背景`。
- 改名為 Task 102：m1 已經有 Task 101。
- 做完：改 `publish_snapshot.py`、`config.example.yaml`、兩個 chore 與 `CHANGES.md`；在 SkillsGestalt 比對改前改後的輸出，在 scratch 用那個 Forge 的設定做完一整輪（`3.3`）。
- 拿掉那個 Forge 的名稱與分支名稱：改之前的 `check` 對本 task 報了 keyword。表 1 加上找到的其他寫死的值，`3.2` 改成「改了什麼」，`2. 結論`、`3.3`、`3.4`、`7. 知識` 寫上結果。
