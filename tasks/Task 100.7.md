# Task 100.7 - 各 skill 的 CONFIGURATION 分成兩類，MD report 的 Checkpoint 欄改名為 Run record

**Status**：完成——22 個 skill 的 CONFIGURATION 都分成兩類，MD report 的表頭欄改名為 Run record；所有依賴紀錄都是 UNCHANGED。
**Raised**：2026-11-06，使用者發現 SKILL-tmp 的 CONFIGURATION 只列 Checkpoint Dir，但 run-data-rules 的過程資料有 `temp\` 與 `checkpoints\` 兩個位置。
**Depends on**：—

## 1. 背景

- [run-data-rules.md](../skill-groups/common/rules/run-data-rules.md) 把一次執行寫的資料分成過程產生的資料（`temp\` 的暫存檔、`checkpoints\` 的 step 檔）與最後的輸出（process record、handoff 檔、`database\`、MD report）。
- SKILL-tmp 的 CONFIGURATION 原本只列 Checkpoint Dir、process record 與 MD report，沒有 `temp\` 與 handoff 檔，也沒有分類。
- MD report 表頭的 Checkpoint 欄，在 [[Task 100.2]] 之後指向 process record，名稱和它指的東西不一致。

## 2. 結論

—

## 3. 過程

### 2026-11-06 範本與規則改好之後

- [SKILL-tmp.md](../skill-groups/common/templates/SKILL-tmp.md) 與中文版：
  - TERMINOLOGY 加上 Scratch file 與 Handoff file；MD report 的標準表頭改成 Skill、Process record、Created、Updated、Prompt。
  - CONFIGURATION 分成兩組：過程產生的資料（Scratch files `temp\{SKILL_NAME}-{what-it-does}.{ext}`、Checkpoint Dir），以及最後的輸出（Process record、Handoff file、MD report）；用不到的那一行刪掉。
- [report-md-rules.md](../skill-groups/common/rules/report-md-rules.md) 與中文版：表頭的 `- **Checkpoint**: {CHECKPOINT_PATH}` 改成 `- **Process record**: {PROCESS_RECORD_PATH}`。
- run-data-rules.md 與中文版：MD report 那一節改稱 `Process record` 欄。
- gen-skill 與 check-skill：Glossary 的 MD report 表頭跟著改；gen-skill 的 Step 3 加上「不寫暫存檔就刪 Scratch files 那一行，沒有別的 skill 讀它的輸出就刪 Handoff file 那一行」。
- gen-skill 與 check-skill 的 README 重記 SKILL-tmp.md 與 run-data-rules.md；asd-ste 與 compile-skill 的 README 這兩項仍是 CHANGED，等本 task 改完再記。

### 已決定（2026-11-06）

使用者回答了 4 個問題，都照建議：

1. CONFIGURATION 照兩類分成兩組，列出全部位置。
2. TERMINOLOGY 加上 Scratch file 與 Handoff file。
3. MD report 表頭的 Checkpoint 欄改名為 Process record。
4. 先改範本、規則、gen-skill 與 check-skill；各 skill 在本 task 改。

之後使用者又提出改名，回答了 4 個問題，都照建議：

5. **Process record 改名為 Run record**：它記的是一次 run，和 Run Number、`database\skill-runs\` 一致；「Skill Record」容易讀成 skill 本身的紀錄。
6. **「The Data of the Process」改名為「The Working Data of a Run」**，並寫明它把每個 step 的輸出交給之後的 step；中文版稱「執行時的工作資料」。
7. 「The Last Outputs」不改。
8. 改名併進本 task。

### 2026-11-06 改名之後

- `skill-groups/common` 中 55 個檔（CHANGES.md 的舊紀錄不改）：Process record、process record、`process_record`、`processRecord`、`PROCESS_RECORD` 都換成 Run record、run record、`run_record`、`runRecord`、`RUN_RECORD`；「data of the process」換成「working data of a run」。
- MD report 表頭的欄位因此是 `Run record`，placeholder 是 `{RUN_RECORD_PATH}`。
- run-data-rules、report-md-rules、SKILL-tmp 與 README-tmp 的 STE 檢查都 PASS；改過的中文版 parity 都是 0 failure；script 都編譯得過，`save_step.py --new-run` 印出 `run_record`。
- 引用這些檔的 README 指紋都會顯示 CHANGED，等各 skill 改完一起重記。

### 2026-11-06 各 skill 改好之後

- 22 個 skill 分給 4 個 subagent 改，一個 skill 一個 commit（`542cba9` 到 `058e586`）。
- CONFIGURATION：寫暫存檔或 step 檔的 skill 有「The working data of a run」那一組，其餘只有「The last outputs」；輸入與工具（範本、script、設定檔、resolver 等）放在兩組之前。
- MD report 的表頭欄：set-tag-status、imp-app 等改成 `Run record`；Glossary 的標準表頭也改了；`git grep` 找不到 `Skill, Checkpoint` 與 `**Checkpoint**`。
- asd-ste、check-skill、compile-skill、gen-skill 的 README 與中文版重記 run-data-rules、SKILL-tmp、README-tmp 與 chinese/SKILL.md；check-md-deps 重記 check-wiki-doc，checking-criteria 重記 README-tmp；`skill-groups/common` 的每一份依賴紀錄都是 UNCHANGED。

### 留給使用者決定的

- 輸入與工具放在兩組之前，沒有自己的一組；要的話可以加第三組「The inputs」。
- write-note 一系列的 MUST FOLLOW 寫著遵守 run-data-rules 的「scratch files」，它們其實不寫暫存檔。
- set-tag-status 加了 Tags file 一行，check-wiki-doc 加了 HTML 依賴圖與架構文件兩行，都是它們的輸出。

## 4. 要做的

1. 每個有 CONFIGURATION 的 skill，照 SKILL-tmp 改成兩組，列出它寫的暫存檔、Checkpoint Dir、run record、handoff 檔與 MD report。
2. Glossary 寫著 MD report 標準表頭（Skill, Checkpoint, …）的 skill，改成 Run record：compile-skill、gen-imp-app、gen-rsdc-app、gen-rsdc-skill、imp-app、imp-home。
3. MD report 的表頭寫 Checkpoint 欄的 skill，改成 Run record 欄：imp-app、imp-home、gen-imp-app、gen-rsdc-skill、set-tag-status；write-topic 說明它沒有 Checkpoint 欄的那一句跟著改。
4. 有中文版的同時改；asd-ste 與 compile-skill 的 README 重記 SKILL-tmp.md 與 run-data-rules.md。
5. 一個 skill 一個 commit；在 CHANGES.md 加一筆。

## 5. 驗證

- `git grep -n -e 'Skill, Checkpoint' -e '\*\*Checkpoint\*\*' -- skill-groups/common` 沒有輸出。
- 每個有 CONFIGURATION 的 SKILL.md 都有兩組。
- 有中文版的 parity check 是 0 failure；四份 README 的 `depends_on.py check` 都是 UNCHANGED。

## 6. 與其他 task 的關係

- [[Task 100]]：本 task 的上層。
- [[Task 100.3]]：範本第一次照 run-data-rules 改。
- [[Task 100.4]]、[[Task 100.6]]：各 skill 第一次照 run-data-rules 改。

## 7. 知識

—

## 8. 日誌

### 2026-11-06

- 做完：22 個 skill 照新的 CONFIGURATION 改，所有依賴紀錄重記。
- 改名：Process record 改成 Run record，「The Data of the Process」改成「The Working Data of a Run」。
- 提出：範本、report-md-rules、run-data-rules、gen-skill 與 check-skill 先改好。
