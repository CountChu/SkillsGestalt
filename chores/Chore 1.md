# Chore 1 - 集中重記 ste-custom.md

**Status**：使用中——ste-custom.md 有改動的日子，當天最後一次修改之後跑一次 `draft.py recheck`。
**Started**：2026-10-18，ste-custom.md 一天改了好幾次，記錄它的 22 份不必每次都重檢、重記；做法由 [[Task 52]] 定下，chore 由 [[Task 53]] 建立。
**When**：當天改過 ste-custom.md，而且當天的修改都做完了

## 1. 目的

每份 STE 檔與草稿都在檔頭記錄 [ste-custom.md](../.github/common/skills/asd-ste/references/ste-custom.md) 的指紋，所以 ste-custom.md 一改，它們全部報 CHANGED。
一天只集中重檢、重記一次：指紋照樣可靠，同一件事也不會每改一次就重記一輪。

## 2. 何時要做

- 當天改過 ste-custom.md，而且當天不會再改。
- 看出該做了：從 workspace 的根目錄跑 `python .github/common/skills/asd-ste/scripts/draft.py recheck --root . --dry-run`，列出任何一份 `[STALE]`，就是還沒做。
- 正在處理的那份草稿不必等：照 ste-custom.md 的說明，立刻對它跑 Step 3。

## 3. 怎麼做

1. 從 workspace 的根目錄跑 `python .github/common/skills/asd-ste/scripts/draft.py recheck --root .`。
   其他用這個 skill group、而且有 STE 檔的 workspace，各加一個 `--root`。
2. 讀它的輸出：
   - `[FAILED]`：那一份保留舊的紀錄；照它列出的 `[FAIL]` 修正，草稿再跑 Step 3，STE 檔再跑 `check_ste.py --ste`。
   - `[NOT RECORDED]`：中文版，跟著它的英文檔一起處理。
   - `[NEW WARN]`：草稿多出的警告，它已經重記；讀過之後，改草稿或在下一次 Step 3 寫明理由。
3. 重記的結果單獨一個 commit，前綴 `chore 1: `。
4. 在 `6. 執行紀錄` 加一筆，摘要表的「上次執行」改成當天，再跑 `check_chores.py`。

## 4. 驗證

- `draft.py recheck --root . --dry-run` 一份都不列。
- `check_chores.py` PASS。

## 5. 與其他 task、chore 的關係

- [[Task 52]]：定下集中重記的做法，寫了 `draft.py recheck`。
- [[Task 53]]：建立 chore 制度與本 chore。
- [[Task 50]]：每份 STE 檔都宣告 `[[ste-custom]]`，所以 ste-custom.md 一改就是 22 份。

## 6. 執行紀錄

### 2026-10-30

- 第四次執行：[[Task 61]] 讓 ste-custom.md 第 8 行改成照 ste-rules 的 House Rule 5，之後 `draft.py recheck --root . --root ../InvestForge` 重檢 26 份，26 份都重記，以 0 結束；新指紋 `8cc2e2061175`。
  這次沒有草稿；13 份 STE 檔的 `check_ste.py --ste` 都 PASS，警告和之前相同：RSDC-Standard 4 則被動句，tw-keep-english 與 md-style 是 no-op 被拆成的 op；13 份中文版跟著英文檔重記。
  比上次多的 2 份是 README-tmp 與它的中文版；InvestForge 沒有記錄 ste-custom.md 的檔案。

### 2026-10-19

- 第三次執行：[[Task 32.8]] 到 [[Task 32.11]] 審核時，ste-custom.md 又改了幾次，加上 program、deterministic、search、need、exception、run、prompt 等字與保留名稱的規則。
  SKILL-tmp 取代原檔之後，`draft.py recheck --root .` 重檢 24 份，24 份都重記，以 0 結束；新指紋 `5978e1af2fcf`。
  SKILL-tmp 的草稿每次修改後都立刻跑了 Step 3，取代後的 SKILL-tmp.md 與它的中文版已記著新指紋，不在這 24 份裡；InvestForge 沒有記錄 ste-custom.md 的檔案。
  12 份 STE 檔的 `check_ste.py --ste` 都 PASS，警告和之前相同：RSDC-Standard 4 則被動句，tw-keep-english 與 md-style 是 no-op 被拆成的 op；12 份中文版跟著英文檔重記。
  所有草稿都已取代，這次沒有草稿；之後 `--dry-run` 一份都不列。

### 2026-10-18

- 第一次執行：當天 ste-custom.md 最後一次修改是 [[Task 52]]，之後 `draft.py recheck --root .` 重檢 22 份，22 份都重記，以 0 結束；新指紋 `3c5050b6a240`。
  6 份草稿的檢查都 PASS，沒有新的 WARN，`step_3` 都已存；5 份 STE 檔的 `check_ste.py --ste` 都 PASS，警告和之前相同：RSDC-Standard 4 則被動句，tw-keep-english 與 md-style 是 no-op 被拆成的 op。
  之後 `--dry-run` 一份都不列。
- 第二次執行：[[Task 32.7]] 審 scratch-rules 時，ste-custom.md 又改了兩次，加上 own、擴大 create 的意思；scratch-rules 取代原檔之後，`draft.py recheck --root .` 重檢 20 份，20 份都重記，以 0 結束；新指紋 `e12251a917f1`。
  scratch-rules 的草稿每次修改後都立刻跑了 Step 3，取代後的 scratch-rules.md 與它的中文版已記著新指紋，不在這 20 份裡。
  4 份草稿的檢查都 PASS，沒有新的 WARN，`step_3` 都已存；6 份 STE 檔的 `check_ste.py --ste` 都 PASS，警告和之前相同：RSDC-Standard 4 則被動句，tw-keep-english 與 md-style 是 no-op 被拆成的 op。
  skill-writing 的草稿由 [[Task 32.8]] 在審，重記只改了它與中文版檔頭的 `[[ste-custom]]` 那一行；之後 `--dry-run` 一份都不列。
