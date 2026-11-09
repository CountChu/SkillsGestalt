# Task 100.12 - Temp Dir 與 Checkpoint Dir 合稱 Working Dir，一個 skill 選一個

**Status**：完成——Temp Dir 與 Checkpoint Dir 是兩種 Working Dir，每個 skill 只用一個；兩個都有的 4 個 skill 併入 Checkpoint Dir，CONFIGURATION 之後都寫 Working Dir。
**Raised**：2026-11-06，使用者要把 Temp Dir 與 Checkpoint Dir 合稱為 Working Dir，working data 存在 Working Dir，兩者二選一，CONFIGURATION 之後提到的 Checkpoint Dir 改為 Working Dir。
**Depends on**：[[Task 100.11]]

## 1. 背景

- [[Task 100.11]] 之後，一次執行可以同時有 Temp Dir `temp\{skill}\{yymmdd}.{N}\`（暫存檔）與 Checkpoint Dir `checkpoints\{skill}\{yymmdd}.{N}\`（step 檔與資料檔）。
- asd-ste、imp-app、imp-home、gen-imp-app 兩個都有；check-skill 只有 Temp Dir；其他 skill 只有 Checkpoint Dir 或都沒有。
- SKILL-tmp 的 MUST FOLLOW 與 steps 寫的是 Checkpoint Dir。

## 2. 結論

—

## 3. 過程

### 已決定（2026-11-06）

- **Working Dir** 是一次執行存放 working data 的目錄，是 Temp Dir 或 Checkpoint Dir 其中之一；三個詞都留在 Glossary。
- 用哪一個由 skill 作者自選。
- 一個 run 只有一個 Working Dir：用 Checkpoint Dir 的 skill，暫存檔也放 Checkpoint Dir；用 Temp Dir 的 skill，step_N.yaml 也寫在 Temp Dir。
- SKILL-tmp 的 CONFIGURATION 兩行並列，說明只留一行。
- 現有 skill：兩個都有的 4 個併入 Checkpoint Dir；只有一個的維持現狀。
- CONFIGURATION 之後提到的 Checkpoint Dir 改為 Working Dir：範本、規則與所有 skill。

## 4. 要做的

1. ✅ 改 run-data-rules.md 與中文版：Working Dir 一節，Temp Dir 與 Checkpoint Dir 二選一。
2. ✅ 改 SKILL-tmp.md、README-tmp.md 與中文版。
3. ✅ 改 gen-skill（問作者選哪一個）與 check-skill（檢查只有一個 Working Dir）。
4. ✅ asd-ste、imp-app、imp-home、gen-imp-app 把暫存檔併入 Checkpoint Dir，script 一起改。
5. ✅ 其他 skill 的 MUST FOLLOW 與 steps 把 Checkpoint Dir 改成 Working Dir。
6. ✅ 重記依賴紀錄、寫 CHANGES.md。

## 5. 驗證

- 每個 skill 的 CONFIGURATION 最多有一個 Working Dir。
- SKILL.md 在 CONFIGURATION 之後不再寫 Checkpoint Dir 或 Temp Dir 的通稱。
- 有中文版的檔 parity 0 failure；STE 檔 check_ste PASS；改過的 script 跑過測試。

## 6. 與其他 task 的關係

- [[Task 100]]：本 task 的上層。
- [[Task 100.11]]：Temp Dir 是在這個 task 加的。

## 7. 知識

- **各 skill 的 Working Dir**：
  - Checkpoint Dir：asd-ste、gen-imp-app、imp-app、imp-home（原本兩個都有，暫存檔併進來），以及 gen-rsdc-app、gen-rsdc-skill、reformat-md、set-tag-status、write-topic。
  - Temp Dir：check-skill（`facts.yaml`）。
  - ask-note、check-md-deps、chinese、compile-skill 沒有 Working Dir 那一行，只有 MUST FOLLOW 改成 Working Dir。
- **script 的路徑**：asd-ste `draft.py recheck` 改寫到該次執行 Checkpoint Dir 的 `recheck\`；imp-home `test_hub.js --run` 改寫到 Checkpoint Dir 的 `test-hub\`；其他 script 不必搬。
- **Glossary 的寫法**：只用一種的 skill，Working Dir 的第二行寫「In this skill, it is the Checkpoint Dir, and **CONFIGURATION** gives it.」，不照抄範本的「the Temp Dir or the Checkpoint Dir」，因為那個 skill 沒有定義另一種；gen-skill 的 Step 3 也照這樣改。
- **刻意保留的**：指令範例中的具體路徑（`--out "checkpoints\..."`）、imp-app session resolver 的 JSON 欄位 `checkpointDir`、asd-ste README 說明舊格式目錄的「Checkpoint Dirs from before run-data-rules.md」、gen-skill 與 check-skill 中以兩種目錄為主題的句子。
- **留給使用者決定**：check-skill 新的準則 5.7 把「working data 寫到另一種目錄」定為 issue，要不要改成 recommendation。

## 8. 日誌

### 2026-11-06

- 做完：規則與範本（`049ab29`），gen-rsdc-app 等 5 個 skill（`8b7d743`），imp-app、imp-home（`8d740e5`），asd-ste、gen-imp-app（`1c13261`），gen-skill（`cb94d19`），check-skill（`0be4df7`），ask-note 等 4 個 skill（`9317962`），依賴紀錄（`d121553`、`91ac493`）；CHANGES.md 加一筆。
- 提出。
