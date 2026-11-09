# Task 100 - 決定 skill 執行中的資料該寫進 checkpoints 還是 temp

**Status**：完成——run 寫的資料分成 working data 與最後的輸出，規則是 run-data-rules.md；範本與 common 的 22 個 skill 都照它改好，CONFIGURATION 分成輸入與工具、working data、最後的輸出三組；working data 放在每個 skill 唯一的 Working Dir（Temp Dir 或 Checkpoint Dir）；6 個很少用的 skill 封存。
**Raised**：2026-11-05，使用者要探討 skill 執行時的資料該記在 `checkpoints\` 還是 `temp\`。
**Depends on**：—

## 1. 背景

- 兩條規則各管一個目錄，git 都不追蹤（`.gitignore` 第 25 行與第 31 行）：
  - `report-yaml-rules.md`：YAML checkpoint 在根目錄的 `checkpoints\`，每一步要把重要的輸出寫進它。
  - `scratch-rules.md`：scratch 放在根目錄的 `temp\`；run 結束時刪掉自己建的 scratch 檔；MD report、YAML checkpoint、`database\` 的檔與 app 的目錄是輸出，不是 scratch。
- [SKILL-tmp.md](../skill-groups/common/templates/SKILL-tmp.md) 要每一步從 YAML checkpoint 讀前一步的輸出。
- 兩條規則之間有一塊沒有說清楚：一步寫、下一步讀的中間資料，算輸出還是 scratch。
  例如 [check-skill](../skill-groups/common/skills/check-skill/SKILL.md) 沒有 YAML checkpoint，Step 2 把 facts file 寫到 `temp\check-skill-facts-{yymmdd-hh}.yaml`，Step 3 與 Step 4 讀它，Step 6 刪掉它。
- agent 自己也有暫存的地方：Claude Code 每個 session 有一個 scratchpad 目錄（在 `/private/tmp/` 下），Copilot 沒有。

## 2. 結論

—

## 3. 過程

### 已決定（2026-11-06）

使用者先決定了三件事：

1. **交接目錄叫 `handoff`**：第二類資料（跑完後留著，給另一個 skill 參考）放在這裡。
2. **skill 不能依賴 agent 的暫存目錄**：Claude Code 每個 session 有自己的暫存目錄，別的 session、Copilot 與 script 都找不到它。
3. **script 產生的暫存檔放在 `temp\`**，符合 scratch-rules；不用系統的暫存目錄，也不分語言。
   要改的是 compile-skill 的 `check_compiled.py`、asd-ste 的 `draft.py recheck` 與 imp-home 的 `test_hub.js`。

之後又用選項問了 11 個問題，決定如下：

4. **`handoff` 放在 workspace 根目錄**，和 `checkpoints\`、`temp\`、`database\` 並列；結構是 `handoff\{寫的 skill}\…`；git 不追蹤。
   寫的 skill 下次 run 時覆寫：2026-11-06 改成檔名帶 run 的編號、使用者手動清，見「新的規則檔」。
5. **`database\` 與 `handoff` 的分界**：好幾個 skill 一直共用、跨 run 累積的資料放 `database\`，例如 `tags.yaml`；一個 skill 每次 run 重新產生、給別的 skill 讀的資料放 `handoff`。
6. **process.yaml 改成效率紀錄**，移到 `database\skill-runs\{skill}\{yymmdd}.{N}.yaml`，N 是當天從 1 開始的序號。
   - 它記每一步花的時間與用的 model，供日後分析 skill 的效率，一直留著；2026-11-06 再加上 skill 名稱、prompt 與 run 的結果。
   - 它不引用 step_N.yaml。
7. **每一步產生的資料寫在 `step_N.yaml`**，放在 `checkpoints\` 的 Checkpoint Dir；skill 不自動刪，使用者手動清。
8. **MD report 的 Checkpoint 欄只連到 process.yaml**。
9. **很少用的 skill 搬到 `skill-groups\archived`**：先盤點再決定哪些；搬過去的 skill 不能執行，只是保存，不加進 `skillGroups`。

10. **執行時寫資料的目錄分成兩類**，取代 2026-11-05 的三類：判斷的方法是 run 跑完之後還有沒有人要讀它。
    原本的第 1 類（跑完可以刪）是過程產生的資料；第 2 類（交接）與第 3 類（一直留著）是最後的輸出。

**表 1：過程產生的資料**

| 目錄 | 放什麼 | 怎麼清 |
| --- | --- | --- |
| `temp\` | scratch、script 產生的暫存檔 | run 結束時刪掉自己的檔 |
| `checkpoints\{skill}\{run_dir}\` | 每一步的 `step_N.yaml` | 使用者手動清 |

**表 2：最後的輸出資料**

| 目錄 | 放什麼 | 給誰 | 怎麼清 |
| --- | --- | --- | --- |
| `handoff\{寫的 skill}\` | 每次 run 重新產生、交給別的 skill 的資料 | 別的 skill | 寫的 skill 下次 run 時覆寫 |
| `database\` | 好幾個 skill 共用、跨 run 累積的資料 | 別的 skill、以後的 run | 一直留著 |
| `database\skill-runs\` | process.yaml：每一步的時間與 model | 日後分析 skill 的效率 | 一直留著 |
| vault `{wikiDir}\{skill}\` | MD report | 人 | 一直留著 |

### 新的規則檔：run-data-rules.md（2026-11-06）

使用者又回答了 10 個問題，定下兩條規則的新分界：

1. **scratch-rules.md 與 report-yaml-rules.md 合併成 `run-data-rules.md`**，放在 `skill-groups/common/rules/`，有中文版；兩個舊檔刪掉，引用它們的檔改連到新檔。
2. **report-md-rules.md 不合併**：新檔在「最後的輸出」列出 vault 的 MD report，細節連到 report-md-rules.md；report-md-rules.md 的 Checkpoint 欄改成 process.yaml 的路徑。
3. **新檔分成兩章，就是表 1 與表 2 的兩類**：
   - **過程產生的資料**：`temp\` 的 scratch，沿用 scratch-rules 的規則；`checkpoints\` 的 step_N.yaml。
   - **最後的輸出**：`database\skill-runs\` 的 process.yaml、`handoff\`、`database\`，以及 vault 的 MD report。
4. **一次 run 的編號是 `{yymmdd}.{N}`**，N 是這個 skill 當天從 1 開始的序號；Checkpoint Dir、process.yaml 與 handoff 的檔都用同一個編號，所以不必互相引用就對得上。
5. **Checkpoint Dir 是 `checkpoints\{skill}\{yymmdd}.{N}\`**，每一步一個 `step_N.yaml`，run 的資料檔也放在這裡；拿掉「每次 run 一個檔」的結構。
6. **step_N.yaml 只寫這一步的輸出資料**，給後面的步驟讀；title 與 time 不寫在這裡。
7. **process.yaml 是 `database\skill-runs\{skill}\{yymmdd}.{N}.yaml`**，記 skill 名稱、prompt、run 的結果（完成，或中斷在第幾步），以及每一步的 title、begin、end、taken 與 model。
   report-yaml-rules 裡量時間的規則（讀系統時鐘、不估計、taken 只算整分鐘）搬到這一節。
8. **handoff 的檔是 `handoff\{寫的 skill}\{yymmdd}.{N}.md`**，一律 `.md`；寫的 skill 在 MUST FOLLOW 寫明它寫哪些 handoff 檔。
   舊的檔留著，使用者手動清；讀的 skill 讀最新的一個，或使用者指定的一個。
9. **`database\`** 放好幾個 skill 共用、跨 run 累積的資料；寫它的 skill 在 MUST FOLLOW 寫明檔名。
10. **不用的位置**：系統的暫存目錄、agent 的暫存目錄、workspace 的根目錄、原檔的旁邊。

### 2026-11-06 很少用的 skill

看了三種紀錄：`database\skill-tokens`（Claude Code 的 hook 從 2026-08-31 起記的 216 次執行，不完整：asd-ste 記 0 次，Copilot 的不記）、兩個 vault 的報告資料夾，以及別的 skill 有沒有讀它、呼叫它或用它的 script。

**表 3：封存的決定**

| Skill | 證據 | 決定 |
| --- | --- | --- |
| report-logs | 報告最後是 2026-09-16 | 封存 |
| report-week | 沒有報告資料夾；InvestForge 改用 report-inv-week | 封存 |
| report-skills | 報告最後是 2026-05-24 | 封存 |
| notify-week | 沒有紀錄；只能在 Windows 跑 | 封存 |
| synch-two-mds | 沒有紀錄 | 封存 |
| eli5 | 沒有紀錄；在 `external` | 封存 |
| report-my-chats | 只有 `scripts\`，沒有 SKILL.md，git 不追蹤 | 封存 |
| write-note、write-note-new-files、write-note-tags、add-tags、add-tags-note、del-tags、set-tag-status、ask-note | 沒有紀錄；`database\tags.yaml` 不存在 | 不封存 |
| write-topic | 報告最後是 2026-09-16，4 份 | 不封存 |
| check-wiki-doc | 沒有紀錄；check-md-deps 引用它 | 不封存 |

- 封存之後，add-tags 與 del-tags 的 Step 2 會找 `{wikiDir}\report-logs\` 的報告，report-logs 不再產生新的報告。
- compile-skill 的 SKILL.md 第 103、109、116 行用 report-skills 與 report-logs 當例子。

### 2026-11-06 盤點的結果

28 個 skill 分成 4 組，由 4 個只讀的 subagent 讀 SKILL.md 與每一支 script 寫檔的地方；下面是整理後的結果，行號以盤點當天的檔案為準。

- 只有 asd-ste 的 `checkpoints\` 有資料；`checkpoints\` 下的其他 skill 目錄都不存在，`temp\` 是空的。
- 步驟之間的資料，大部分 skill 只靠對話傳：對話不見了，這次 run 就接不下去。
- 沒有一支 script 寫進 `temp\` 或 `database\`；寫 scratch 的三支 script 都用系統的暫存目錄。

**表 4：交接資料的方式**

| 方式 | skill | 問題 |
| --- | --- | --- |
| 只靠對話 | ask-note、check-wiki-doc、check-md-deps、chinese、gen-skill、compile-skill、report-skills、gen-rsdc-app，以及 tag 與 note 類的 skill | check-md-deps 與 check-wiki-doc 的最後一步要靠對話裡 report 的編號 |
| `process.yaml` | asd-ste、imp-app、gen-imp-app、imp-home、notify-week | report-week 要存 checkpoint，卻沒寫路徑；gen-rsdc-skill 每一步各寫一個 `step-N.yaml`，不是 report-yaml-rules 允許的兩種結構 |
| Checkpoint Dir 裡的資料檔 | asd-ste 的 `step_*`、imp-app 的 `unit-tests.json` 與 `deploy-*.json`、gen-imp-app 的 `prompt-log.md` 與 `owner-skill-check.json`、report-logs 的 `s3`～`s7` yaml | 檔名固定，每次覆寫；asd-ste 的 findings JSON 在 process.yaml 又存一份 |
| `temp\` | check-skill 的 facts file；imp-app 與 gen-imp-app 測試用的複本與 probe | facts file 的 `--out` 跟著目前目錄，在 macOS 上建出一個名字裡有 `\` 的檔 |
| 系統的暫存目錄 | compile-skill 的 `check_compiled.py`、asd-ste 的 `draft.py recheck`、imp-home 的 `test_hub.js` | 用完自動刪掉，但 scratch-rules 要 scratch 放在 `temp\` |
| 原檔旁邊 | asd-ste 的 `-ste.md` 草稿、reformat-md 的 `#v1` 副本、chinese 的 twin | `#v1` 副本可能落在 git 追蹤的 `skill-groups\` 裡 |

**表 5：照兩類分開的資料**

| 類 | 資料 |
| --- | --- |
| 過程產生的資料 | check-skill 的 facts file；測試用的複本與 probe；asd-ste 的 findings JSON、`step_1-inventory.txt`、`step_6-notes.html` 與 `test-DFD` 孤兒目錄；report-logs 的 `s3`～`s7` 與 `s12-timing.yaml` |
| 最後的輸出：交接 | report-logs 的 MD report（report-week 讀）；gen-imp-app 的 `prompt-log.md` 與 imp-app 的 `docs/Prompts.md`（gen-rsdc-app 讀）；asd-ste 的 review 頁面、`step_6-status.json` 與 `-ste.md` 草稿；`database\tags.yaml`（8 個 skill 讀，檔案不存在）；gen-rsdc-app 交回給呼叫者的結果（只在對話裡） |
| 最後的輸出：一直留著 | MD report、RSDC、twin、Skills Dashboard、`.imp-app.json` 與 `.imp-home.json`、notify-week 的 `%LOCALAPPDATA%` 檔；process.yaml（移到 `database\skill-runs\`） |

**表 6：asd-ste 的 `checkpoints\asd-ste\`（3.2M，12 個 run 目錄）**

| 檔 | 大小 | 類 |
| --- | --- | --- |
| `step_6-review.html` | 1.95 MB | 輸出；可以從四份文件與 YAML 重建 |
| `process.yaml` | 413 KB | 輸出，移到 `database\skill-runs\`；RSDC-Standard 那一份的 `step_1` 是 findings JSON 的複本 |
| `step_1-findings.json` | 360 KB | 過程；和 process.yaml 重複 |
| `step_1-inventory.txt` | 166 KB | 過程 |
| `step_6-notes.html` | 83 KB | 過程 |
| `step_6-status.json` | 64 KB | 輸出；使用者的審核狀態 |
| `step_3-findings.json` | 60 KB | 過程；和 process.yaml 重複 |
| `step_3-check.txt` | 16 KB | 輸出；`draft.py recheck` 讀它 |

**表 7：每個 skill 的盤點**

| Skill | 交接方式 | 寫到規定位置以外 |
| --- | --- | --- |
| add-tags | 對話 | 改 report-logs 的 MD report |
| add-tags-note | 對話 | — |
| ask-note | 對話 | — |
| asd-ste | process.yaml 與資料檔 | 草稿在原檔旁邊；`recheck` 用系統暫存目錄；Checkpoint Dir 跟著目前目錄 |
| check-md-deps | 對話 | — |
| check-skill | 對話與 `temp\` 的 facts file | facts file 跟著目前目錄 |
| check-wiki-doc | 對話 | HTML 依賴圖在 vault 裡架構文件的旁邊 |
| chinese | 對話 | twin 在原檔旁邊，照設計 |
| compile-skill | 對話 | 系統暫存目錄；Step 4 跑目標 skill 時寫的檔沒有說放哪裡 |
| del-tags | 對話 | 改 report-logs 的 MD report |
| eli5 | 沒有步驟 | HTML 放哪裡沒有寫 |
| gen-imp-app | process.yaml 與資料檔 | `artifacts\`；新的 skill 目錄 |
| gen-rsdc-app | 對話 | 交回的結果只在對話裡 |
| gen-rsdc-skill | 每一步一個 `step-N.yaml` | — |
| gen-skill | 對話 | — |
| imp-app | process.yaml 與資料檔 | app 目錄；部署目標；`temp\` 的複本沒有檔名 |
| imp-home | process.yaml | 目標目錄；`test_hub.js` 用系統暫存目錄 |
| notify-week | process.yaml | `%LOCALAPPDATA%`，只在 Windows |
| reformat-md | 對話 | `#v1` 副本在原檔旁邊 |
| report-logs | Checkpoint Dir 的 `s*` yaml | `main.py` 寫到 `skill-groups\checkpoints\` |
| report-skills | 對話 | 把報告的資料夾叫做 checkpoints directory |
| report-week | MD report 的段落；checkpoint 沒有路徑 | — |
| set-tag-status | 對話 | 寫 `database\tags.yaml` |
| synch-two-mds | 對話 | 一個空的「checkpoints directory」，可能建在任何地方 |
| write-note | 對話 | — |
| write-note-new-files | 對話 | — |
| write-note-tags | 對話 | — |
| write-topic | 對話 | — |

### 盤點時順便發現的缺陷

這些不在本 task 的範圍，還沒開 task。

- **路徑跟著目前目錄**：check-skill 的 `--out`、imp-app 的 `resolve_session.py`、asd-ste 的 Checkpoint Dir、imp-home 的 `setup_target.py`，以及 imp-app 與 gen-imp-app 的 `--out`；從根目錄以外的地方跑，就寫錯地方。
- **`main.py` 的根目錄錯了**：report-logs 與 report-skills 的 `main.py` 用 `parents[3]`，算出來是 `skill-groups\`；兩支都不在 SKILL.md 裡。
- **report-logs 刪 vault 的檔**：Step 9 與 Step 11 刪掉沒有對應 yaml 的 MD 檔，SKILL.md 沒寫；Step 2、4、6 不清過期的 yaml。
- **gen-rsdc-skill 的 `run step N`** 覆寫整個 run 的 MD report。
- **check-wiki-doc** 讀 `wikiRootDir`，config.yaml 只有 `wikiDir`。
- **write-topic、set-tag-status、synch-two-mds** 照 report-md-rules 寫報告，卻沒有 Checkpoint 欄。
- **asd-ste 的 Step 0 `--new`** 重設 process.yaml，卻留下舊的 `step_*` 檔；舊的 `step_6-status.json` 會影響新的 review 頁面。

### 2026-11-05 初步看到的

- 根目錄的 `checkpoints\` 現在有 `asd-ste`（3.2M）與 `chores`（12K）；`temp\` 是空的。
- 用到 `temp\` 的 SKILL.md 只有兩份：check-skill 的 facts file，以及 [imp-app](../skill-groups/common/skills/imp-app/SKILL.md) 第 566 行測試用的 app 目錄複本。
- 其餘 skill 只提到 checkpoint，還沒逐一確認每一步寫了什麼、寫到哪裡。

### 已決定（2026-11-05）

使用者回答了 6 個問題：

1. **核心問題**：步驟之間傳的中間資料放在哪裡。
2. **agent 的暫存目錄**：納入比較，和 `checkpoints\`、`temp\` 一起看。
3. **資料分成三類**，這是使用者自己加的；2026-11-06 改成兩類，見第 10 項：
   - 跑完可以立刻刪的；
   - 跑完後要留著，給另一個 skill 參考的；
   - 跑完後要一直留下來的。
4. **判斷的標準**：run 結束後還要不要留著、MD report 會不會引用它、下一步或下一次 run 會不會讀它、檔案大小。
5. **第三個位置**：第二類（給另一個 skill 參考）除了 `checkpoints\` 與 `temp\`，也比較 `database\` 或一個指定的交接目錄。
6. **範圍**：本 task 只盤點與決定；改規則、範本與各 skill，另開 sub task。

## 4. 要做的

1. ✅ 盤點每個 skill 的每一步寫了哪些檔、寫到哪裡、後面誰讀它、run 結束後留不留；做成一張表（2026-11-06）。
2. 把盤點到的資料照類別分開，每一類用四個判斷標準檢查；2026-11-06 改成兩類，表 5 是照兩類的分法。
3. 每一類比較可以放的位置：`checkpoints\`、`temp\`、`database\` 或一個交接目錄，以及 agent 的暫存目錄；寫出各自的好處與問題，問使用者。
   2026-11-06 都定了，見「已決定（2026-11-06）」。
4. ✅ 寫下決定：每一類放在哪裡、scratch-rules.md 與 report-yaml-rules.md 的分界怎麼改；兩個檔合併成 run-data-rules.md，見「新的規則檔」（2026-11-06）。
5. 照決定開 sub task，分成三個（2026-11-06 開了 [[Task 100.2]]、[[Task 100.3]]、[[Task 100.4]]）：
   - 寫 run-data-rules.md 與中文版，刪掉兩個舊檔，改 report-md-rules.md，`.gitignore` 加上 `handoff/`。
   - 改 SKILL-tmp.md、README-tmp.md，以及 gen-skill 與 check-skill 照範本寫與檢查的地方。
   - 改各個 skill：checkpoint 的寫法、`temp\` 的暫存檔，以及引用兩個舊檔的地方。

**Sub task**

- [[Task 100.1]] ✅ 把很少用的 skill 搬到 skill-groups/archived
- [[Task 100.2]] ✅ 寫 run-data-rules.md，取代 scratch-rules 與 report-yaml-rules
- [[Task 100.3]] ✅ 範本與 gen-skill、check-skill 照 run-data-rules 改
- [[Task 100.4]] ✅ 各個 skill 照 run-data-rules 改
- [[Task 100.5]] ✅ 檢查 Task 100 是否完成
- [[Task 100.6]] ✅ 其餘 9 個 skill 補上 process record
- [[Task 100.7]] ✅ 各 skill 的 CONFIGURATION 分成兩類，MD report 的 Checkpoint 欄改名為 Run record
- [[Task 100.8]] ✅ CONFIGURATION 的輸入與工具要不要有自己的一組
- [[Task 100.9]] ✅ write-note 系列不寫暫存檔，MUST FOLLOW 卻提到 scratch files
- [[Task 100.10]] ✅ set-tag-status 與 check-wiki-doc 在 CONFIGURATION 多列的輸出
- [[Task 100.11]] ✅ Scratch files 改成 Temp Dir，working data 在中文版保留英文
- [[Task 100.12]] ✅ Temp Dir 與 Checkpoint Dir 合稱 Working Dir，一個 skill 選一個

## 5. 驗證

- 盤點表列出每一個有 SKILL.md 的 skill。
- 每一類資料都有一個位置，而且沒有一筆資料同時符合兩類。
- check-skill 的 facts file 與 imp-app 的 app 目錄複本，都能照新的分界判定放在哪裡。

## 6. 與其他 task 的關係

- [[Task 32.6]]：把 report-yaml-rules 改寫成 STE。
- [[Task 32.7]]：把 scratch-rules 改寫成 STE。
- [[Task 97]]：Copilot 與 Claude Code 都要能用；agent 的暫存目錄只有 Claude Code 有，決定時要考慮。

## 7. 知識

—

## 8. 日誌

### 2026-11-06

- [[Task 100.12]] 完成：Temp Dir 與 Checkpoint Dir 合稱 Working Dir，每個 skill 只用一個；Task 100 完成。
- 開 [[Task 100.12]]：Temp Dir 與 Checkpoint Dir 合稱 Working Dir；Task 100 回到進行中。
- [[Task 100.11]] 完成：暫存檔放進 Temp Dir，working data 在中文版保留英文；Task 100 完成。
- 開 [[Task 100.11]]：Scratch files 改成 Temp Dir，working data 在中文版保留英文；Task 100 回到進行中。
- [[Task 100.8]] 完成：CONFIGURATION 加上「The inputs and tools」一組；Task 100 完成。
- [[Task 100.10]] 完成：保留 set-tag-status 與 check-wiki-doc 多列的輸出。
- [[Task 100.9]] 完成：write-note 系列拿掉多餘的「scratch files」。
- 開 [[Task 100.8]]、[[Task 100.9]]、[[Task 100.10]]：Task 100.7 留下、等使用者決定的三件事。
- [[Task 100.7]] 完成：22 個 skill 的 CONFIGURATION 分成兩類，Run record 改名完成；Task 100 完成。
- 開 [[Task 100.7]]：使用者發現 SKILL-tmp 的 CONFIGURATION 只列 Checkpoint Dir；範本與規則先改好。
- [[Task 100.5]] 完成：清單的主要部分都合；Task 100 完成。
- [[Task 100.6]] 完成：其餘 9 個 skill 補上 process record。
- [[Task 100.4]] 完成：13 個 skill 照新規則改，兩個舊規則檔刪掉。
- 開 [[Task 100.6]]：其餘 9 個 skill 補上 process record。
- [[Task 100.3]] 完成：範本、gen-skill 與 check-skill 照新規則改。
- 開 [[Task 100.5]]：檢查 Task 100 是否完成。
- [[Task 100.2]] 完成：run-data-rules.md 寫好。
- 開 [[Task 100.2]]、[[Task 100.3]]、[[Task 100.4]]。
- 寫下新的規則檔 run-data-rules.md 的分界：合併兩條規則、run 的編號 `{yymmdd}.{N}`、step_N.yaml、process.yaml 與 handoff 的檔名。
- 執行時寫資料的目錄分成兩類：過程產生的資料與最後的輸出，取代三類；表格重新編號。
- 盤點很少用的 skill，決定封存 7 個，見表 3；由 [[Task 100.1]] 搬完。
- 再問 11 個問題，定下 `handoff` 的細節、`database\` 與 `handoff` 的分界、process.yaml 與 step_N.yaml 的新做法、`skill-groups\archived`。
- 記下三個決定：交接目錄叫 `handoff`；skill 不依賴 agent 的暫存目錄；Python 的暫存檔放 `temp\`。
- 盤點 28 個 skill，結果寫進「現況」一章的表 4 到表 7；順便發現的缺陷另列一節。

### 2026-11-05

- 提出。
