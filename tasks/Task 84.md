# Task 84 - 由 CLAUDE-tmp.md 與 CLAUDE-local.md 產生 CLAUDE.md

**Status**：完成——2026-10-30 寫好 [CLAUDE-tmp.md](../.github/common/templates/CLAUDE-tmp.md)、本 repo 的 [CLAUDE-local.md](../CLAUDE-local.md) 與 [gen_claude_md.py](../.github/common/scripts/gen_claude_md.py)，CLAUDE.md 由它產生；重新打開之後，keep-English chore 改由 `config.yaml` 的 `keepEnglishChore` 填入。
**Raised**：2026-10-30，[[Task 83]] 做完之後，使用者提出：路徑由程式展開，比讓 agent 讀說明、或靠檢查比對路徑都直接，agent 也不必花 token 理解這些說明。
**Depends on**：[[Task 82]]、[[Task 83]]

## 1. 背景

- [[Task 82]] 把共用的規則抽成 `agency-rules.md`，本 repo 的 [CLAUDE.md](../CLAUDE.md) 以 Markdown 連結加 `@` import 引入它。
- [[Task 83]] 因為 `@` 與連結不懂 `{skillGroups.common}`，CLAUDE.md 只能寫實際路徑；於是加了一句說明路徑的來源，再寫 `check_claude_md.py` 比對四處路徑和 `config.yaml`。
- 這樣 agent 每次都要讀這些說明句，而一致性靠事後檢查。
- 由程式展開模板產生 CLAUDE.md，CLAUDE.md 就只有實際路徑：不用 `@`、不用說明句、不用逐處比對路徑；VS Code 的 agent 也讀得到完整的規則。

## 2. 現況

### 2026-10-30 做完之後

- [CLAUDE-tmp.md](../.github/common/templates/CLAUDE-tmp.md)：標題 `# {agencyName}`、STE 的 header quote、引言，以及 Markdown、繁體中文 twins、Tasks、Chores 四節；路徑都寫 `{skillGroups.common}`；最後一行 `{CLAUDE-local}`。
  引言說明 CLAUDE.md 由模板與 `CLAUDE-local.md` 產生、不要直接改；每個 agency 都適用的規則改模板，只有本 agency 的改 `CLAUDE-local.md`；改完或改了 `config.yaml` 之後執行 `gen_claude_md.py`。
- 本 repo 的 [CLAUDE-local.md](../CLAUDE-local.md)：第一行 `> Technical words:` 列出它自己的 technical words，然後是 Settings of This Agency（`config.example.yaml`、keep-English chore 是 [[keep-english]]）與 Branches。
- [gen_claude_md.py](../.github/common/scripts/gen_claude_md.py)：
  - 從 `config.yaml` 取 `skillGroups.common`，讀 `{skillGroups.common}/templates/CLAUDE-tmp.md` 與根目錄的 `CLAUDE-local.md`。
  - `{agencyName}` 換成根目錄的資料夾名稱，`{skillGroups.X}` 換成 `config.yaml` 裡寫的值，`{{name}}` 留成 `{name}`（給要顯示佔位符的句子），`{CLAUDE-local}` 那一行換成片段。
  - 片段第一行的 technical words 併進模板的 technical words，排序、去重，那一行不進 CLAUDE.md。
  - 不帶參數就寫出 CLAUDE.md；`--check` 只比對，不同就印出 unified diff 與「改模板或片段，不要改 CLAUDE.md」，以 `1` 結束；檔案缺、`skillGroups.common` 沒設或模板用到沒設的 group，以 `2` 結束；`--root` 指定根目錄。
- 本 repo 的 [CLAUDE.md](../CLAUDE.md) 由它產生，路徑都是 `.github/common`，只有 Tasks 一節那句說明規則裡的佔位符時保留 `{skillGroups.common}`。
- `agency-rules.md` 與中文版、`check_claude_md.py` 已刪；[[Task 82]] 與 [[Task 83]] 指向它們的連結改成純文字，各加一行日誌。

### 2026-10-30 重新打開之後

- 使用者問：CLAUDE.md 的「繁體中文 twins」為何提到 `CLAUDE-local.md`？
  因為模板不知道各 agency 的 keep-English chore 是哪一個，只能說「`CLAUDE-local.md` 可以指定一個」；但 agent 讀的是合併好的 CLAUDE.md，這句話會讓它以為要再開另一個檔。
- `config.yaml` 加一個設定 `keepEnglishChore`，值寫 chore 的名稱，例如 `Chore 2`；[config.example.yaml](../config.example.yaml) 與本機的 `config.yaml` 都加上 `keepEnglishChore: Chore 2`。
- 模板那三句改成一行：「When the version of the list changes, do the keep-English chore, `{keepEnglishChore}`: it audits all the twins against the list.」
- `gen_claude_md.py` 把 `{keepEnglishChore}` 換成 `[Chore 2](chores/Chore%202.md)` 這樣的連結；沒設定時，含它的那一行整行拿掉。
- 本 repo 的 `CLAUDE-local.md` 拿掉「The keep-English chore is Chore 2」。
- 模板的 Tasks 一節拿掉「In the rules, `{skillGroups.common}` is …」：task-rules.md 與 chore-rules.md 只在檢查指令用到這個佔位符，而 CLAUDE.md 已經給出展開好的指令；skill 在 Step 0 自己讀 `config.yaml`。
  `gen_claude_md.py` 的 `{{name}}` 功能留著，現在沒有句子用到。

## 3. 要做的

### 已決定（2026-10-30）

- 結構是共用模板加各 agency 的片段，共用規則只有一份：

  ```
  {skillGroups.common}/templates/CLAUDE-tmp.md   共用的規則，路徑寫 {skillGroups.common}
  <agency 根目錄>/CLAUDE-local.md                只有這個 agency 的內容
  {skillGroups.common}/scripts/gen_claude_md.py  讀 config.yaml，合併、展開，寫出 CLAUDE.md；--check 只比對不寫
  <agency 根目錄>/CLAUDE.md                      產生出來的檔
  ```

- 檔名照現有模板的寫法用 `-tmp.md`：`CLAUDE-tmp.md`；片段是 `CLAUDE-local.md`。
- 模板與片段以 STE 寫，過 `check_ste.py`；CLAUDE.md 沒有中文版。
- 產生的 CLAUDE.md 開頭有一句引言：它由哪兩份產生、要改規則改哪一份、改完跑哪個指令；不要直接改 CLAUDE.md。
- CLAUDE.md 仍然 commit：Claude Code 讀的是磁碟上的檔，公開版也要有它。
- 新做法完成後，刪掉 agency-rules.md 與中文版、`check_claude_md.py`：共用規則搬進 `CLAUDE-tmp.md`，`gen_claude_md.py --check` 取代 `check_claude_md.py`。

### 開始做時決定的（2026-10-30）

- 模板裡以一行 `{CLAUDE-local}` 標出片段的位置。
- 標題寫 `# {agencyName}`，取自根目錄的資料夾名稱；引言只說 this agency，不用名稱。
- 「改了模板、片段或 `config.yaml` 要重新產生」只寫在模板，每份 CLAUDE.md 都會有。
- task-rules.md 與 chore-rules.md 不改：產生的 CLAUDE.md 仍然給出實際路徑的指令。
- `--check` 失敗時印 unified diff 加一句提醒。
- 模板有 header quote，片段沒有；CLAUDE.md 照抄模板的 header quote，片段的 technical words 由程式併進去。

### 重新打開時決定的（2026-10-30）

- 做法 B：用佔位符由 `config.yaml` 填入，不用間接的說明。
- 設定名稱 `keepEnglishChore`，值寫 `Chore 2`，由程式做出連結。
- 沒設定的 agency：含佔位符的那一行拿掉，所以模板把依賴它的內容寫成一行。
- 記在本 task：使用者說記在最後一個 task；做完之後通知做 InvestForge Task 13 的 session。

### 要決定的

- Forge 的 `skillGroups.common` 是 `~/…` 時：已由 [[Task 83]] 決定，Markdown 連結改成從根目錄起算的相對路徑，指令照 `config.yaml` 寫的值。

### 步驟

1. 寫 `CLAUDE-tmp.md`：由 agency-rules.md 的四節與本 repo CLAUDE.md 的檢查指令改寫，路徑一律寫 `{skillGroups.common}`。
2. 寫本 repo的 `CLAUDE-local.md`：本 repo 自己的設定（`config.example.yaml`、keep-English chore 是 [[keep-english]]）與 Branches。
3. 寫 `gen_claude_md.py`：讀 `config.yaml`、合併、展開、寫出；`--check` 只比對，不同就以 `1` 結束。
4. 產生本 repo 的 CLAUDE.md，和現在的對照：每一條規則都還在，路徑都是實際值。
5. 刪掉 agency-rules.md 與中文版、`check_claude_md.py`，並改掉提到它們的地方。

## 4. 驗證

- `gen_claude_md.py --check` 在本 repo 是 PASS；直接改 CLAUDE.md 一個字，它就 FAIL。
- 暫用副本把 `skillGroups.common` 改成別的值，重新產生的 CLAUDE.md 每個路徑都跟著變。
- 模板與片段 `check_ste.py` 是 PASS；產生的 CLAUDE.md 裡沒有 `{skillGroups.common}`。
- 產生的 CLAUDE.md 載入後，原本的每一條規則都還在，`check_tasks.py` 與 `check_chores.py` 照它的指令能跑。
- repo 裡沒有任何地方還連到 agency-rules.md 或 `check_claude_md.py`（task 的紀錄除外）。

2026-10-30 的結果：

- 本 repo：`gen_claude_md.py --check` 是 PASS；把 CLAUDE.md 的一個句點改成驚嘆號，`--check` 印出那一行的 diff 與提醒，以 `1` 結束；改回之後 PASS。
- 暫用副本照 Forge 的寫法，`skillGroups.common` 是 `~/…/SkillsGestalt/.github/common`：產生的 CLAUDE.md 標題是副本資料夾的名稱，每個路徑都換成那個值，`{skillGroups` 只剩說明佔位符的那一句。
- 暫用副本的 `config.yaml` 沒有 `skillGroups.common`：以 `2` 結束，說明沒有設定。
- CLAUDE.md 與模板 `check_ste.py` 都是 PASS，`depends_on.py check CLAUDE.md` 是 UNCHANGED；`reformat_md.py --mode clean` 不改動模板、片段與 CLAUDE.md。
- 對照改之前的 CLAUDE.md 與 agency-rules.md：每一條規則都在新的 CLAUDE.md 裡，不同的只有路徑寫成實際值、`@` 與 `check_claude_md.py` 的說明拿掉，以及「規則改哪一份」的說明。
- `check_tasks.py` 與 `check_chores.py` 照新的 CLAUDE.md 的指令都是 PASS；`git grep` 在 task 的紀錄之外找不到 agency-rules 或 `check_claude_md`。

重新打開之後的結果（2026-10-30）：

- 本 repo：重新產生的 CLAUDE.md 只差兩處，twins 一節的三句變成連到 Chore 2 的一行，Settings 一節少了 Chore 2 那一句；`--check` 是 PASS。
- 模擬的 InvestForge：`config.yaml` 沒有 `keepEnglishChore` 時那一行不出現，前後沒有多出空行；加上 `keepEnglishChore: Chore 1` 之後連到 Chore 1。
- CLAUDE.md 與模板 `check_ste.py` 是 PASS，`depends_on.py check CLAUDE.md` 是 UNCHANGED，`reformat_md.py --mode clean` 不改動。

## 5. 與其他 task 的關係

- [[Task 82]]：建立 agency-rules.md 與 `@` import；本 task 完成後它們退場。
- [[Task 83]]：建立 `check_claude_md.py`；本 task 以 `gen_claude_md.py --check` 取代它。
- [[Task 81]]：術語表定義了 agency、Gestalt 與 Forge；模板用這些名稱。
- InvestForge 與 BookMaster 改成以模板產生 CLAUDE.md，在它們自己的 tasks 做。

## 6. 知識

—

## 7. 日誌

### 2026-10-30

- 建立 task：共用模板 `CLAUDE-tmp.md` 加各 agency 的 `CLAUDE-local.md`，由 `gen_claude_md.py` 讀 `config.yaml` 產生 CLAUDE.md；完成後刪掉 agency-rules.md 與 `check_claude_md.py`。
- 開始做並完成：寫好模板、片段與 `gen_claude_md.py`，產生本 repo 的 CLAUDE.md，試跑四種情況；刪掉 `agency-rules.md`、中文版與 `check_claude_md.py`，[[Task 82]] 與 [[Task 83]] 的連結改成純文字。
- [[Task 83]] 重新打開，決定了「要決定的」裡 `~` 連結那一項，並為模板加上開頭的插入點 `{CLAUDE-local-top}`。
- 重新打開：keep-English chore 改由 `config.yaml` 的 `keepEnglishChore` 填入，模板的三句併成一行，沒設定就拿掉；完成。
- 模板拿掉 Tasks 一節說明 `{skillGroups.common}` 值的那一句：CLAUDE.md 已經給出展開好的指令，這句多餘。
- [[Task 86]] 把 chore 改用名稱：本檔的 `[[Chore N]]` 連結改成新名稱。
