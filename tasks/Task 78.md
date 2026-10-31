# Task 78 - 把 SkillsGestalt 公開到 GitHub，排除 checkpoints 與公司內部資訊

**Status**：完成——2026-10-30 公開到 GitHub；之後的發佈由 [[publish-github]] 做，每次發佈前掃描、使用者確認之後才推。
**Raised**：2026-10-30，使用者要把 SkillsGestalt 公開到自己的 GitHub，名稱 SkillsGestalt，排除 `checkpoints/`。
**Depends on**：—

## 1. 背景

使用者決定把 SkillsGestalt 放上 GitHub 帳號 CountChu，設為公開，repo 名稱是 SkillsGestalt，並排除 `checkpoints/`。
推上去之前掃描了 repo，發現有些檔案含有公司內部的資訊，公開會洩漏同事的資料與公司內部的位置。
本 task 檔也會被公開，所以這裡只記類別與檔案路徑，不寫出實際的 email、IP、主機或專案名稱。

## 2. 現況

### 已確認沒有問題的

- 本機 repo 沒有設定遠端，GitHub 帳號下也沒有 SkillsGestalt。
- `checkpoints/` 已經在 [.gitignore](../.gitignore) 裡，也從來沒有被 commit 過，歷史裡沒有它。
- 所有歷史裡都找不到密碼、token、API key 或私鑰。

### 已處理的

- 2026-10-30 刪除 mail-inline skill：`.github/common/skills/mail-inline/` 的 `SKILL.md`、`config.yaml` 與 `scripts/make_outlook_safe.py`。
  它的 `config.yaml` 有使用者自己與十幾位同事的工作 email，`SKILL.md` 也有工作 email 與用公司網域寫的範例地址。
  使用者的 Windows 工作環境也有一份 SkillsGestalt；那裡若還要用這個 skill，由使用者另外處理，例如放到工作 workspace 自己的 skill。
  刪除之前的版本仍在 git 歷史裡，所以「歷史裡的問題」一節仍然適用。
- 2026-10-30 刪除 report-my-chats 與 write-note-chat：`.github/common/skills/report-my-chats/` 的 `SKILL.md`、`config.yaml` 與 `scripts/` 的三支程式，以及 `.github/common/skills/write-note-chat/SKILL.md`。
  report-my-chats 的 `SKILL.md` 有公司內部的 IP、內部共享資料夾的路徑與工作 workspace 的名稱；write-note-chat 讀的就是 report-my-chats 產生的報告，沒有它就沒有輸入，所以一起刪。
  工作環境若還要用這兩個 skill，和 mail-inline 一樣由使用者另外處理。
- 2026-10-30 換成範例值，不刪檔：
  - [gen-skill/SKILL.md](../.github/common/skills/gen-skill/SKILL.md) 與中文版 Prompt 2 的兩個 build 連結，換成虛構組織 contoso 的 Azure DevOps 網址。
  - [write-note/SKILL.md](../.github/common/skills/write-note/SKILL.md) 的 Git 連結（專案、repo 與分支名稱）、pipeline 名稱與產品代號，換成 contoso 的網址與虛構的名稱。
  - [imp-app/assets/config.yaml](../.github/common/skills/imp-app/assets/config.yaml) 註解裡公司內部 IP 的共享路徑，換成 `\\fileserver\apps\InvCov`。
  - [ask-note/SKILL.md](../.github/common/skills/ask-note/SKILL.md) 的產品代號，換成虛構的 `X750`（縮寫 `X75`）。
  - 工作 vault 的名稱：ask-note、check-skill 與中文版、gen-imp-app、imp-home 與中文版，以及 [SKILL-tmp.md](../.github/common/templates/SKILL-tmp.md) 與中文版，說明 `vaultName` 時用的例子換成 `MyVault`。
    範本換了一個字，記錄它指紋的 8 份 README（asd-ste、check-skill、compile-skill、gen-skill，各含中文版）讀過改動仍然成立，重記之後 `depends_on.py check` 都是 UNCHANGED；範本的 `check_ste.py --ste` PASS，三組中文版與四組 README 的 `check_parity.py` 都是 0 failure。
  - gen-skill 照它 README 的「When the Skill Is Changed」跑了檢查：中英對照 `check_parity.py` 0 failure，`depends_on.py check` 都是 UNCHANGED，check-skill 的掃描正常；只改了範例的網址，所以略過「用 gen-skill 產生一個暫用的 skill」那一項。

### 第一次發佈（2026-10-30）

- 公開的 repo：<https://github.com/CountChu/SkillsGestalt>，預設分支 `main`。
- 快照 commit `b2c697a`，沒有 parent，作者 CountChu，取自 master 的 `9629f0a`，共 264 個檔。
- 本機加了遠端 `origin`，`public` 分支追蹤 `origin/main`；master 沒有推。

### 不宜公開的內容（2026-10-30 掃描 HEAD）

目前的檔案裡已經沒有：上面「已處理的」都處理掉了。

### 不必改的

- 產品名稱（Outlook、Teams 的開發商名稱），出現在 check-wiki-doc 的一份 HTML，屬於公開的產品資訊。
- [checking-criteria.md](../.github/common/skills/check-skill/references/checking-criteria.md) 與中文版裡的 Azure DevOps 網域，是 VS Code 官方文件的公開網址；`C:\Users\...` 是通用的範例路徑。

### 歷史裡的問題

- 上面這些內容從 2026-09-24 起就在 git 歷史裡。
  只改現在的檔案，推上整份歷史時，舊版本仍然看得到。
- 541 個 commit 的作者是使用者的個人 email，但有 1 個 commit 的作者是工作 email。

### 重新掃描的方法

在根目錄搜尋 `git log --all -p` 新增的行，找：email 地址、私有 IP（`10.`、`172.16.`–`172.31.`、`192.168.` 開頭）、Azure DevOps 的網域（`visualstudio.com`、`dev.azure.com`），以及工作代號與 vault 名稱；換掉的值可以從本 task 的 commit 看到差異，只在本機的歷史裡。
也要用 `git log --all --format='%ae'` 看每個 commit 的作者 email。

## 3. 要做的

### 已決定（2026-10-30）

- **只推一份清理過的新歷史**：本機保留 `public` 分支，每次發佈把 master 的內容做成 `public` 上的一個快照 commit，只把 `public` 推到 GitHub 的 `main`。
  master 不推，所以它的歷史、包括那個以工作 email 為作者的 commit，都不會公開；其他 session 照舊在 master 上工作。
- **快照 commit 的作者**：使用者的個人 email，名稱 CountChu。
- **本機專用的檔案不進 git**：根目錄的 `config.yaml` 有本機 vault 的絕對路徑，改成只在本機，另加 [config.example.yaml](../config.example.yaml)；`SKILL.mermaid.html` 是 mermaid-view 在本機產生的預覽，[.gitignore](../.gitignore) 加上 `*.mermaid.html`。
  [skill_tokens.py](../scripts/skill_tokens.py) 的 workspace 對照表用 `~/`，看不到帳號名稱，照舊。
- **根目錄加上** [README.md](../README.md) 與中文版，以及 MIT 授權的 [LICENSE](../LICENSE)，著作權人 CountChu。
- **公開** `tasks/`、`chores/` 與 `dashboard/`：公司資訊已經清掉。
- **快照時排除，master 照舊**：
  - `external/`：ASD-STE100 規格的 PDF；規格的版權頁寫明未經 STEMG 許可不得散布，見 [[Task 26]]。
  - `.github/external/`：從外面來的 eli5 skill，原作者與授權不明。
- **ste-dictionary.json 放進公開版**：使用者的決定。
  它是從規格 Part 2 做成的字典，而規格的版權頁寫明未經 ASD 書面授權不得複製全部或部分內容；README 寫明它由規格做成，規格本身要向 ASD 取得。

### 之後的發佈

- 「之後怎麼防止公司資訊再寫進 repo」由 [[publish-github]] 處理：每次發佈前，[publish_snapshot.py](../.github/common/scripts/publish_snapshot.py) 掃描要公開的 tree，使用者看過變動、同意之後才推。
- 原本記在這裡的發佈步驟搬到 [[publish-github]]，改由程式做。
- 掃描用的工作代號放在不進 git 的 `publish-keywords.local.txt`，因為這些名稱本身就不能公開。

## 4. 驗證

2026-10-30 第一次發佈的結果：

- 推之前掃描快照的 tree：公司內部資訊、私有 IP、個人路徑、token 都是 0 筆；找得到的網址只有 VS Code 官方文件、contoso 的範例與本 task 的搜尋條件。
- GitHub 上：只有 1 個 commit；264 個檔裡沒有 `checkpoints/`、`external/`、`.github/external/`、`config.yaml`、預覽檔或 PDF。

每次發佈都要再確認：

- 推上去之後，GitHub 上的檔案與歷史搜尋不到上面任何一類內部資訊。
- GitHub 上沒有 `checkpoints/`。
- 本機原本的歷史與其他 session 的工作沒有受到影響（選只推新歷史時）。

## 5. 與其他 task 的關係

- [[publish-github]]：本 task 建立的發佈 chore。
- [[Task 79]]：之後把本機分支 `master` 改名為 `m1`、`public` 改名為 `main`；本 task 的紀錄照當時的名稱。
- [[Task 26]]：ASD-STE100 的 PDF 不放進公開版，記在它的日誌。

## 6. 日誌

### 2026-10-30

- 建立 task：使用者決定公開、名稱與排除 `checkpoints/`；掃描後找到公司內部資訊，列出四個處理方式，尚未決定。
- 刪除 mail-inline skill，Status 改成進行中；[[Task 70]] 的清單跟著拿掉它。
- 刪除 report-my-chats 與讀它報告的 write-note-chat；[[Task 70]] 與 [[Task 24]] 的清單跟著拿掉它們。
- gen-skill、write-note、imp-app、ask-note 的公司內部資訊換成範例值；checking-criteria 確認是公開網址，移到「不必改的」。
- 工作 vault 的名稱換成 `MyVault`，8 份 README 重記範本的指紋；「要判斷是否算內部資訊的」一節處理完，拿掉。
- 決定只推 `public` 分支上的快照，以及作者、本機專用的檔案、README 與 LICENSE、要排除的路徑；`config.yaml` 與預覽檔不再進 git，加上 README、LICENSE 與 `config.example.yaml`。
- 第一次發佈：以 master 的 `9629f0a` 做出快照 `b2c697a`，建立公開的 repo，推到 `main`；GitHub 上確認只有 1 個 commit，也沒有排除的路徑。
- 建立 [[publish-github]] 與 [publish_snapshot.py](../.github/common/scripts/publish_snapshot.py)，發佈的步驟搬過去；本 task 完成。
- [[Task 79]] 把本機分支改名：`master` 改為 `m1`，`public` 改為 `main`；本檔的紀錄照當時的名稱，只在「與其他 task 的關係」加上它。
- [[Task 86]] 把 chore 改用名稱：本檔的 `[[Chore N]]` 連結改成新名稱。
- [[Task 87]] 把 `publish_snapshot.py` 搬進 `.github/common/scripts/`：本檔連到它的連結改成新的路徑。
