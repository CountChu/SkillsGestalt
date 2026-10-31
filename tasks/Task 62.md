# Task 62 - 讓每個 workspace 有自己的 task 與 chore

**Status**：進行中——[[Task 62.1]] 到 [[Task 62.6]] 完成；剩 [[Task 62.7]]，它要等 Task 11 @ InvestForge 的依賴巡檢 chore 建好、跑過一次。
**Raised**：2026-10-18，使用者要每個 workspace 有自己的 task 與 chore，SkillsGestalt 的 task 與 chore 不再放 InvestForge 的工作。
**Depends on**：—

## 1. 背景

- 只有 SkillsGestalt 有 `tasks/`、`chores/` 與兩張摘要表；InvestForge 沒有，它的工作也記在這裡。
- 2026-10-18 查的結果：51 個 task 檔與 [[keep-english]] 提到 InvestForge。
  - 主題就是 InvestForge 的東西：9 個，其中 3 個已完成，見 [[Task 62.4]]。
  - 一半是 InvestForge：[[Task 18]] 的 5 個 sub task 隨 [[Task 62.4]] 搬走；[[Task 32]]、[[Task 38]]、[[Task 54]]、[[Task 55]] 與 [[keep-english]] 見 [[Task 62.5]]。
  - 只在紀錄裡提到：其餘 37 個，都已完成，記的是當時順手改了 InvestForge 的哪些檔、commit 是哪一個。
- 這些提及一直冒出來，有兩個原因。
  - 上游的 task 直接改下游的檔：這裡改了共用的標準、範本或清單，就順手去 InvestForge 重記指紋或改中文版，commit 也用這裡的編號。
    InvestForge 的 git log 有 40 個 `task N:` commit，用的都是這裡的編號：14、18、19、28、32、32.8、33、44–48。
    asd-ste 的 Step 7 明文要問還有哪些 workspace 用這個 skill group，把它們加成 `--root`；[[rerecord-ste-custom]] 的第 1 步也一樣。
  - 借 InvestForge 的設定：這裡沒有 `config.yaml`，check-skill 一直借 InvestForge 的（[[Task 7]]、[[Task 35]]、[[Task 39]]、[[Task 50]]）；Skills Dashboard 也在 InvestForge 的 `wikiDir` 裡。
- task 記在這裡，就在 SkillsGestalt 的 session 裡接手。
  那種 session 載入的是這裡的 CLAUDE.md 與 memory，看不到 InvestForge 的 CLAUDE.md，也看不到它自己的 19 條 memory。
- [[Task 6]] 決定不建 tasks skill 時留下的條件「其他 workspace 要維護時再考慮」，現在成立了。

## 2. 現況

### 已決定（2026-10-18）

使用者回答了 8 個問題，都照建議：

- 方向：下游可以提到上游，上游不提任何一個下游。
  SkillsGestalt 是上游，提供 common 的 skill、規則、範本與腳本；InvestForge 是下游，以 `skillGroups.common` 用它們。
- 每個 workspace 有自己的 `tasks/`、`chores/`、`dashboard/task-summary.md` 與 `dashboard/chore-summary.md`，編號各自從 1 起。
  InvestForge 的兩張摘要表也放在 `dashboard/`；它的 `config.yaml` 另有一個 `dashboardDir`，指向 repo 外產生的頁面，和 repo 裡的 `dashboard/` 不衝突。
- 規則放在 common：[task-rules.md](../.github/common/rules/task-rules.md) 與 [chore-rules.md](../.github/common/rules/chore-rules.md)，英文加中文版；每個 workspace 的根目錄 CLAUDE.md 直接指向它們，並寫出自己的檢查指令，`tasks/`、`chores/` 裡不放 CLAUDE.md（[[Task 62.1]]）。
  不建 skill：Claude Code 看不到 repo 裡的 skill，它會自動載入的是 CLAUDE.md。
- 主題是 InvestForge 的 9 個 task 全搬，包括已完成的 3 個；InvestForge 的歷史留在 InvestForge（[[Task 62.4]]）。
- 號碼用過不再用：搬走的 task 在這裡留下空號，留下的 task 不重新編號，免得 commit 前綴指到別的 task（[[Task 62.2]]）。
  空號逐號寫在摘要表圖例下面的 `空號：` 那一行，check 1 確認每個號碼不是有檔案，就是在那一行。
- 提到別的 workspace 的 task 時，寫成純文字 `Task N @ <workspace>`，不加連結（[[Task 62.3]]）。
- 其餘 37 個已完成的 task 裡提到 InvestForge 的句子保留：那是當時發生的事與 commit 的位置；只改會斷的 wikilink。
  要拆的 task 照同一個原則：已記下的紀錄保留，只改還要做的部分。
- 本 task 與它的 sub task 可以點名 InvestForge：它就是搬家本身，做完就成為紀錄；之後新寫的 task 與 chore 不再提。
- 上游停在自己的邊界：這裡改了共用檔，這裡的 task 只重記這裡的依賴方；InvestForge 的依賴方，由 InvestForge 自己的依賴巡檢 chore 讀過改動之後重記（[[Task 62.7]]）。
- SkillsGestalt 有自己的 `config.yaml`，不再借 InvestForge 的（[[Task 62.6]]）。

### 不在本 task

- imp-home 的 `config.yaml` 有 InvestForge launcher 那一段，`scripts/skill_tokens.py` 列了 InvestForge 的路徑。
  它們不是 task 或 chore，要不要改另外決定。

## 3. 要做的

依編號順序做。
這裡的 commit 前綴是 `task 62.N`；InvestForge 裡的 commit 用什麼前綴，在 [[Task 62.3]] 決定。

- [[Task 62.1]] ✅ task 與 chore 的規則搬進 common
- [[Task 62.2]] ✅ 檢查腳本允許空號，只掃 git 追蹤的檔
- [[Task 62.3]] ✅ 建立 InvestForge 的 task 與 chore
- [[Task 62.4]] ✅ 搬走 InvestForge 的 9 個 task，Task 18 只留這裡的 3 份
- [[Task 62.5]] ✅ 拆開 Task 32、38、54、55 與 Chore 2
- [[Task 62.6]] ✅ SkillsGestalt 自己的 config.yaml
- [[Task 62.7]] ⬜ asd-ste 的 Step 7 只重記本 workspace 的依賴方

## 4. 驗證

- 這裡沒有一項還要做的工作會改 InvestForge 的檔：未完成的 task 的「要做的」與使用中的 chore 的「怎麼做」只動本 workspace；本 task 家族除外。
- 已記下的紀錄照「已決定」保留，所以 grep 仍找得到 InvestForge；之後新寫的段落不再提。
- 兩個 workspace 的 `check_tasks.py` 與 `check_chores.py` 都 PASS，在 InvestForge 幾秒內跑完。
- cwd 在 InvestForge 的 session 只讀 InvestForge 的 CLAUDE.md，就找得到 task 與 chore 的規則與檢查指令。

## 5. 與其他 task 的關係

- [[Task 6]]：當初不建 tasks skill；本 task 改把規則放進 common，仍然不建 skill。
- [[Task 53]]：建立 chore 制度；本 task 讓它也能用在別的 workspace。
- [[Task 61]]：規則只寫一次；[[Task 62.1]] 新寫的規則檔不重寫 md-style 已有的規則。
- [[Task 55]]：這裡的依賴巡檢 chore；InvestForge 的那一個是 [[Task 62.7]] 的前提。
- [[Task 63]]：[[Task 62.1]] 另開，決定中文版留英文的新詞要不要加進 keep-English list。

## 6. 日誌

### 2026-10-30

- [[Task 86]] 把 chore 改用名稱：本檔的 `[[Chore N]]` 連結改成新名稱。

### 2026-10-20

- [[Task 62.6]] 完成：根目錄有了 config.yaml，wikiDir 是新的 vault SkillsLlmWiki。

### 2026-10-19

- [[Task 62.4]] 完成：9 個 task 搬到 InvestForge，成為那裡的 Task 2–6。
- [[Task 62.5]] 完成：Task 32、38、54、55 與 Chore 2 只留本 workspace 的部分；InvestForge 開了 Task 7–11 與 Chore 1。

### 2026-10-18

- 建立：評估每個 workspace 怎麼有自己的 task 與 chore，結果寫在第 1、2 章。
- 使用者回答 8 個問題，都照建議；拆成 7 個 sub task。
- [[Task 62.1]] 開始；它的 10 個問題改了兩件事：規則檔分成兩份，根目錄的 CLAUDE.md 直接指向規則檔、資料夾裡不放 CLAUDE.md；「已決定」跟著改。
- [[Task 62.1]] 完成。
- [[Task 62.2]] 開始；空號記在摘要表的 `空號：` 那一行，「已決定」跟著改。
- [[Task 62.2]] 完成。
- [[Task 62.3]] 開始；InvestForge 的 Task 1 是建立它自己的 task，提到別的 workspace 的 task 寫成 `Task N @ <workspace>`，「已決定」跟著改。
- [[Task 62.3]] 完成。
