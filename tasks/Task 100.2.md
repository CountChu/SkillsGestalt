# Task 100.2 - 寫 run-data-rules.md，取代 scratch-rules 與 report-yaml-rules

**Status**：完成——run-data-rules.md 與中文版寫好，report-md-rules.md 的 Checkpoint 欄改成 process record；兩個舊檔只剩一句指向新檔，等 [[Task 100.4]] 改完引用再刪。
**Raised**：2026-11-06，[[Task 100]] 決定把 scratch-rules.md 與 report-yaml-rules.md 合併成 run-data-rules.md。
**Depends on**：—

## 1. 背景

- `scratch-rules.md` 只管 `temp\`；`report-yaml-rules.md` 一個檔管每一步的資料與時間紀錄。
- [[Task 100]] 把 run 寫的資料分成兩類：過程產生的資料與最後的輸出，並定下每一類的目錄與檔名。

## 2. 結論

—

## 3. 過程

### 2026-11-06 改好之後

- **[run-data-rules.md](../skill-groups/common/rules/run-data-rules.md) 與中文版**，174 行，直接用 STE 寫：
  - 開頭說明兩類資料；「The Number of a Run」一節定 `{yymmdd}.{N}`：Step 0 查 `database\skill-runs\{skill}\` 當天最大的 N 加 1，立刻寫出 process record。
  - 「The Data of the Process」：`temp\` 的規則沿用 scratch-rules，加上 script 的暫存檔也放 `temp\`、script 從 `config.yaml` 取得根目錄；`checkpoints\{skill}\{yymmdd}.{N}\` 的 `step_{N}.yaml` 只放這一步的輸出，資料檔也放這裡，skill 不刪。
  - 「The Last Outputs」：process record 的欄位是 `skill`、`run`、`prompt`、`result`（`completed` 或 `stopped`）、`stopped_at` 與 `steps`，每一步有 `step`、`title`、`model`、`time`；量時間的規則搬自 report-yaml-rules；`run step N` 把做的 step 加進 `steps`。
  - handoff 檔是 `handoff\{skill}\{yymmdd}.{N}.md`；讀的 skill 讀使用者指定的，否則讀編號最大的，並說明讀了哪一個。
  - `database\` 與 vault 的 MD report 各一節；「Locations That You Must Not Use」列出 agent 的 scratchpad、系統的暫存目錄、根目錄與原檔旁邊。
- **舊規則不再用的**：每次 run 一個檔的結構；`step_0` 的 `skill`、`model`、`prompt` 移到 process record；「YAML 檔已存在時只更新該 step 的群組」換成 `run step N` 的規則。
- **[report-md-rules.md](../skill-groups/common/rules/report-md-rules.md) 與中文版**：`{CHECKPOINT_PATH}` 是 process record 的路徑，例子是 `database\skill-runs\report-pipeline\261106.1.yaml`；技術用字拿掉 checkpoint。
- **兩個舊檔與中文版**只剩一句「本檔案的規則現在在 run-data-rules.md」，連結不會斷。
- **`.gitignore`** 加上 `handoff/`；[publish_snapshot.py](../skill-groups/common/scripts/publish_snapshot.py) 的 `PRIVATE_PATH` 也擋下 `handoff/`。
- **CHANGES.md** 加一筆。

### 已決定（2026-11-06）

使用者回答了 8 個問題：

1. 直接用 STE 寫，用 check_ste.py 檢查到 PASS，不跑 asd-ste 的完整流程。
2. 兩個舊檔先留一個指向新檔的短檔，等 [[Task 100.4]] 改完引用再刪。
3. `result` 是 `completed`，或 `stopped` 加上 `stopped_at`。
4. N 查 `database\skill-runs\{skill}\` 當天最大的 N 加 1。
5. process record 的頂層欄位是 `skill`、`run`、`prompt`、`result`、`stopped_at`、`steps`。
6. 每一步都記 model。
7. 讀 handoff 的 skill：使用者指定就讀指定的，否則讀編號最大的。
8. 寫好、檢查過就 commit。

## 4. 要做的

1. 寫 `skill-groups/common/rules/run-data-rules.md`，照 [[Task 100]]「新的規則檔」的 10 項：
   - 第一章「過程產生的資料」：`temp\` 的 scratch，沿用 scratch-rules 的規則；`checkpoints\{skill}\{yymmdd}.{N}\` 的 step_N.yaml。
   - 第二章「最後的輸出」：`database\skill-runs\{skill}\{yymmdd}.{N}.yaml` 的 process.yaml，搬入 report-yaml-rules 量時間的規則；`handoff\{寫的 skill}\{yymmdd}.{N}.md`；`database\`；vault 的 MD report，細節連到 report-md-rules.md。
   - run 的編號 `{yymmdd}.{N}`，以及不用的位置。
2. 用 asd-ste 寫成 STE，用 chinese 寫中文版。
3. 改 [report-md-rules.md](../skill-groups/common/rules/report-md-rules.md) 與中文版：Checkpoint 欄是 process.yaml 的路徑，例子跟著改。
4. 兩個舊檔與中文版改成一句指向 run-data-rules.md 的短檔；[[Task 100.4]] 改完引用後再刪。
5. `.gitignore` 加上 `handoff/`；確認 publish_snapshot.py 不發佈 `handoff/`。
6. 在 CHANGES.md 加一筆。

## 5. 驗證

- `check_ste.py` 與 `check_parity.py`：run-data-rules.md 與 report-md-rules.md 都通過。
  2026-11-06：run-data-rules、report-md-rules 與兩個舊檔的短檔都 PASS，parity 都是 0 failure；`depends_on.py check` 兩項 UNCHANGED。
- 新檔涵蓋舊的兩個檔的每一條規則，或寫明哪一條不再用。

## 6. 與其他 task 的關係

- [[Task 100]]：本 task 的上層，內容在它的「新的規則檔」。
- [[Task 100.3]]：照本 task 的新檔改範本。
- [[Task 100.4]]：照本 task 的新檔改各個 skill；引用兩個舊檔的地方，在 100.3 與 100.4 改，所以本 task 刪掉舊檔時，連結會暫時斷掉。
- [[Task 32.6]]、[[Task 32.7]]：把兩個舊檔改寫成 STE。

## 7. 知識

—

## 8. 日誌

### 2026-11-06

- 做完：寫 run-data-rules.md 與中文版、改 report-md-rules.md、兩個舊檔改成短檔、`.gitignore` 加上 `handoff/`。
- 提出。
