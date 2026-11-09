# Task 100.11 - Scratch files 改成 Temp Dir，working data 在中文版保留英文

**Status**：完成——暫存檔都放進 Temp Dir `temp\{skill}\{yymmdd}.{N}\`，skill 不移除它，script 由 step 傳入 Run Number；中文版把 working data 保留為英文，tw-keep-english 換成 261106 版。
**Raised**：2026-11-06，使用者要把 SKILL-tmp 的 Scratch files 改成和 Checkpoint Dir 同結構的 Temp Dir `temp\{SKILL_NAME}\{yymmdd}.{N}\`，並在中文版把 working data 保留為英文。
**Depends on**：—

## 1. 背景

- [[Task 100.2]] 的 run-data-rules.md 把暫存檔放在 `temp\`，檔名以 skill 名開頭，例如 `temp\{skill-name}-{what-it-does}.py`，執行結束時以完整檔名移除。
- [SKILL-tmp.md](../skill-groups/common/templates/SKILL-tmp.md) 的 CONFIGURATION 有一行 **Scratch files** `temp\{SKILL_NAME}-{what-it-does}.{ext}`。
- 中文版把 working data 譯成「執行時的工作資料」。

## 2. 結論

—

## 3. 過程

### 已決定（2026-11-06）

- 名稱用 **Temp Dir**，並移除 scratch file 這個詞。
- Temp Dir 的結構和 Checkpoint Dir 一樣：`temp\{skill}\{yymmdd}.{N}\`，裡面的檔名不必以 skill 名開頭。
- skill 不移除 Temp Dir，使用者手動清，和 Checkpoint Dir 一樣。
- 範圍是全部：SKILL-tmp、run-data-rules、gen-skill、check-skill，以及有 Scratch files 行的 asd-ste、gen-imp-app、imp-app、imp-home 與它們的 script。
- skill 的 step 呼叫 script 時傳入 Run Number；不屬於 skill 的 run 的 script（publish_snapshot.py）維持現狀。
- working data 在每份中文版都保留英文，並加進 tw-keep-english.md；清單換版本，要做 keep-english chore。

## 4. 要做的

1. ✅ 改 run-data-rules.md 與中文版：Temp Dir 取代暫存檔的規則。
2. ✅ 改 SKILL-tmp.md、README-tmp.md 與中文版。
3. ✅ tw-keep-english.md 加上 working data，換版本。
4. ✅ 改 gen-skill 與 check-skill。
5. ✅ 改 asd-ste、gen-imp-app、imp-app、imp-home 與它們的 script，以及其他提到 scratch 的 skill。
6. ✅ 中文版的「執行時的工作資料」改成 working data。
7. ✅ 重記依賴紀錄、寫 CHANGES.md，做 keep-english chore。

## 5. 驗證

- `git grep -i scratch -- skill-groups/common` 只剩說明歷史或不屬於 run 的行。
- `git grep 工作資料 -- skill-groups/common` 沒有結果。
- 有中文版的檔 parity 0 failure；STE 檔 check_ste PASS；改過的 script 跑過測試。

## 6. 與其他 task 的關係

- [[Task 100]]：本 task 的上層。
- [[Task 100.2]]：run-data-rules.md 是在這個 task 寫的。

## 7. 知識

- **script 介面的改變**：
  - check-skill 的 `scan_skill.py` 拿掉 `--out`，改成 `--run-number {yymmdd}.{N}`，寫到 `temp\check-skill\{yymmdd}.{N}\facts.yaml`；不用 `--run`，因為 Step 5 的 `update_dashboard.py --run` 已經用了另一種值。
  - imp-home 的 `test_hub.js` 加上 `--run {yymmdd}.{N}`，工作目錄是 Temp Dir 的 `test-hub\`，跑完保留；不帶 `--run` 時用 `temp\test-hub-*` 並在結束時移除，照「不在 skill 的執行中的 script」那條規則。
    Step 3 新增一行指令傳入 `--run`。
  - asd-ste 的 `draft.py recheck` 不是 step 執行的，是 chore `rerecord-ste-custom` 執行；它沒有加參數，而是把檢查的兩份檔寫在每份 draft 的 source 最新那次執行的 Temp Dir `recheck\`，再搬進那次執行的 Checkpoint Dir；沒有執行時不寫檔。
- **留給使用者決定**：
  - imp-app 同一次執行的多次 update 用同一份 `{app}-copy\`，每次重新從 app dir 做、取代舊的；要不要每次 update 用不同的副本名稱。
  - `draft.py recheck` 在 source 沒有任何執行時，輸出仍寫「[RECORDED] … step_3 saved」，下一行卻說「no step_3 is saved」；這是之前就有的不一致。
- **保留的 scratch**：run-data-rules 的 scratchpad（agent 的暫存目錄）、ReviewPage-RSDC 第 548 行的歷史列、ste-custom 的 Why 欄、ste-dictionary.json 的 SCRATCH、imp-home 的英文慣用語 regenerate-from-scratch。
- RSDC-Standard-tw.md 第 652 行原本誤譯成「沒有任何 執行時的工作資料」，改成「沒有任何 process 產生的資料」。

## 8. 日誌

### 2026-11-06

- 做完：run-data-rules、範本、keep 清單（`8122699`），中文版的 working data（`c97977b`），9 個 skill 的 MUST FOLLOW（`3192791`），publish_snapshot.py（`df2b895`），asd-ste（`8277a40`），imp-app、imp-home、gen-imp-app（`34dfaab`），gen-skill（`58e6a4f`），check-skill（`1f64a6c`），依賴紀錄（`0401a5d`）；keep-english chore（`81a4457`）；CHANGES.md 加一筆。
- 提出。
