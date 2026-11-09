# Task 100.3 - 範本與 gen-skill、check-skill 照 run-data-rules 改

**Status**：完成——SKILL-tmp、README-tmp、gen-skill 與 check-skill 照 run-data-rules 改好；check-skill 多了 5.7 與 5.8。
**Raised**：2026-11-06，[[Task 100]] 決定新的 checkpoint、process.yaml 與 handoff 做法，範本與照範本寫、照範本檢查的 skill 要跟著改。
**Depends on**：[[Task 100.2]]

## 1. 背景

- [SKILL-tmp.md](../skill-groups/common/templates/SKILL-tmp.md) 的 Glossary 定義 Checkpoint Dir 與 YAML checkpoint，CONFIGURATION 給 `checkpoints\{SKILL_NAME}\{CHECKPOINT_DIR_NAME}\`，MUST FOLLOW 要每一步從 YAML checkpoint 讀前一步的輸出，並連到兩個舊的規則檔。
- [README-tmp.md](../skill-groups/common/templates/README-tmp.md) 也連到舊的規則檔。
- gen-skill 照範本寫 skill；check-skill 照範本與 [checking-criteria.md](../skill-groups/common/skills/check-skill/references/checking-criteria.md) 檢查 skill。

## 2. 結論

—

## 3. 過程

### 2026-11-06 改好之後

- **SKILL-tmp.md 與中文版**：
  - TERMINOLOGY：加上 Run Number、Step file 與 Process record，拿掉 YAML checkpoint。
  - CONFIGURATION：Checkpoint Dir 是 `checkpoints\{SKILL_NAME}\{yymmdd}.{N}\`，加上 Process record 的路徑。
  - MUST FOLLOW：`run step N` 從 step 檔讀前一步的輸出；兩條舊規則換成一條 run-data-rules.md；「每份 JSON 只有一個寫入者」改成「Checkpoint Dir 中的每一份檔案」，拿掉 YAML checkpoint 的例外；停止前顯示 MD report 與 process record 的路徑。
  - Step 0 取得 Run Number、寫出 process record；每一步保存 `step_N.yaml`，再把自己加進 process record；Step 2 的 `step_2.json` 併進 `step_2.yaml`；最後一步寫 `result: completed`。
- **README-tmp.md 與中文版**：header quote 與兩處依賴樹，兩條舊規則換成 run-data-rules.md；Dataflow 的 `YAML checkpoint: step_N` 改成 `Step file: step_N.yaml`，拿掉 `step_2.json`，圖下說明 process record 不畫。
- **gen-skill**：Glossary 換成 Checkpoint Dir、Step file 與 Process record；Step 1 問 `both`、`md`、`steps` 或 `none`，不再問 Checkpoint Dir 的命名；Step 3 保留 run-data-rules 與顯示路徑那兩行；header quote 一律保留 run-data-rules.md；README 跟著改。
- **check-skill**：Glossary 與 description 同上；checking-criteria 的 1.2、1.4、3.2、4.1、6.4 改用新詞，加上 5.7 與 5.8；README 的 header quote 改記 run-data-rules.md。
- **重記指紋**：check-skill 與 gen-skill 的 README 與中文版，重記 SKILL-tmp.md、README-tmp.md 與 run-data-rules.md。
  asd-ste 與 compile-skill 的 README 仍顯示這兩個範本 CHANGED，留給 [[Task 100.4]] 改完再記。
- **還沒做的**：gen-skill 與 check-skill 自己寫 process record，屬於 [[Task 100.4]]。

### 已決定（2026-11-06）

使用者回答了 8 個問題：

1. 定義 term「Run Number」，路徑寫 `{yymmdd}.{N}`。
2. Step 2 的 `step_2.json` 併進 `step_2.yaml`。
3. 停止前顯示 MD report 與 process record 的路徑。
4. README-tmp 的 Dataflow 只畫 step 檔，process record 寫一句說明。
5. 每一步結束時把自己加進 process record。
6. 每個 skill 都寫 process record。
7. check-skill 的 README 改記 run-data-rules。
8. checking-criteria 改用新詞，並加上 5.7（系統的暫存目錄）與 5.8（路徑跟著目前目錄）。

## 4. 要做的

1. 改 SKILL-tmp.md 與中文版：
   - Glossary：Checkpoint Dir 是 `checkpoints\{SKILL_NAME}\{yymmdd}.{N}\`，每一步寫 step_N.yaml；加上 process.yaml（`database\skill-runs\`）與 handoff 的定義。
   - CONFIGURATION：Checkpoint Dir、process.yaml 與 handoff 的路徑。
   - MUST FOLLOW：每一步從前一步的 step_N.yaml 讀資料；連到 run-data-rules.md。
2. 改 README-tmp.md 與中文版裡連到舊規則檔的地方。
3. 改 [gen-skill](../skill-groups/common/skills/gen-skill/SKILL.md) 與 [check-skill](../skill-groups/common/skills/check-skill/SKILL.md) 的 SKILL.md、README.md 與 checking-criteria.md 裡引用舊規則檔或舊做法的地方，中文版也是。
4. 照每個 skill 的 README 的「When the Skill Is Changed」做，重記引用範本的檔的指紋。
5. 在 CHANGES.md 加一筆。

## 5. 驗證

- 範本與兩個 skill 的 STE 檢查與 parity check 通過。
- 用 check-skill 檢查一個已經照新做法改好的 skill，Template alignment 不報新的 issue；還沒有這樣的 skill，留給 [[Task 100.5]]。
- 2026-11-06：SKILL-tmp 與 README-tmp 的 STE 檢查 PASS；範本、gen-skill 與 check-skill 的 parity check 都是 0 failure；`scan_skill.py` 掃 gen-skill 正常。

## 6. 與其他 task 的關係

- [[Task 100]]：本 task 的上層。
- [[Task 100.2]]：寫 run-data-rules.md，本 task 照它改。
- [[Task 100.4]]：照本 task 的範本改各個 skill。
- [[Task 97]]：也會改 SKILL-tmp.md 與 skill 的 SKILL.md；兩個同時做的話，會改到同一個檔。

## 7. 知識

—

## 8. 日誌

### 2026-11-06

- 做完：範本、gen-skill 與 check-skill 照 run-data-rules 改，check-skill 加上 5.7 與 5.8。
- 提出。
