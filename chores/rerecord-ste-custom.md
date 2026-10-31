# rerecord-ste-custom - 集中重記 ste-custom.md

**Status**：使用中——ste-custom.md 有改動的日子，當天最後一次修改之後跑一次 `draft.py recheck`。
**Started**：2026-10-18，ste-custom.md 一天改了好幾次，記錄它的 22 份不必每次都重檢、重記；做法由 [[Task 52]] 定下，chore 由 [[Task 53]] 建立。
**When**：當天改過 ste-custom.md，而且當天的修改都做完了

## 1. 目的

每份 STE 檔與草稿都在檔頭記錄 [ste-custom.md](../.github/common/skills/asd-ste/references/ste-custom.md) 的指紋，所以 ste-custom.md 一改，它們全部報 CHANGED。
一天只集中重檢、重記一次：指紋照樣可靠，同一件事也不會每改一次就重記一輪。

## 2. 何時要做

- 當天改過 ste-custom.md，而且當天不會再改。
- 看出該做了：從 workspace 的根目錄跑 `python {skillGroups.common}/skills/asd-ste/scripts/draft.py recheck --root . --dry-run`，列出任何一份 `[STALE]`，就是還沒做。
- 正在處理的那份草稿不必等：照 ste-custom.md 的說明，立刻對它跑 Step 3。

## 3. 怎麼做

1. 從 workspace 的根目錄跑 `python {skillGroups.common}/skills/asd-ste/scripts/draft.py recheck --root .`。
   其他用這個 skill group、而且有 STE 檔的 workspace，各加一個 `--root`。
2. 讀它的輸出：
   - `[FAILED]`：那一份保留舊的紀錄；照它列出的 `[FAIL]` 修正，草稿再跑 Step 3，STE 檔再跑 `check_ste.py --ste`。
   - `[NOT RECORDED]`：中文版，跟著它的英文檔一起處理。
   - `[NEW WARN]`：草稿多出的警告，它已經重記；讀過之後，改草稿或在下一次 Step 3 寫明理由。
3. 重記的結果單獨一個 commit，前綴 `chore rerecord-ste-custom: `。
4. 在摘要表 `## 執行紀錄` 的 `### rerecord-ste-custom` 下加一筆，摘要表的「上次執行」改成當天，再跑 `check_chores.py`。

## 4. 驗證

- `draft.py recheck --root . --dry-run` 一份都不列。
- `check_chores.py` PASS。

## 5. 與其他 task、chore 的關係

- [[Task 52]]：定下集中重記的做法，寫了 `draft.py recheck`。
- [[Task 53]]：建立 chore 制度與本 chore。
- [[Task 50]]：每份 STE 檔都宣告 `[[ste-custom]]`，所以 ste-custom.md 一改就是 22 份。
