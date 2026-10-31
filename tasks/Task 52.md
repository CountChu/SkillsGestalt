# Task 52 - ste-custom 一天改好幾次時，集中一次重記

**Status**：完成——2026-10-18 建立，同日做完：`draft.py recheck` 一個指令做完集中重記，ste-custom.md、SKILL.md 的 Step 6、7 與 README 都寫明做法。
**Raised**：2026-10-18，ste-custom.md 一天改了 3 次，每改一次，記錄它的 22 份就要重檢、重記一次；使用者問能不能只記日期，討論之後決定保留指紋、改成集中一次重記。
**Depends on**：—

## 1. 背景

每份 STE 檔與草稿都在檔頭記錄 [ste-custom.md](../.github/common/skills/asd-ste/references/ste-custom.md) 的日期與指紋（[[Task 50]]），所以 ste-custom.md 一改，22 份都報 CHANGED。
2026-10-18 它改了 3 次（[[Task 50]]、[[Task 51]]、[[Task 32.6]] 的 merge），10-12 以來共 15 次；每次都把 22 份重檢、重記一輪。
只記日期分不出同一天的先後：00:30 核對過、記成 2026-10-18 的檔，看不出 11:21 與 11:46 那兩次修改，所以指紋留著，改的是重記的時機。

## 2. 現況

### 已決定（2026-10-18）

- 範圍：只有 ste-custom.md；DFD、RSDC-Standard 等的依賴檔要人讀過改動才能重記，照舊。
- 時機：一天內 ste-custom.md 改幾次都先不重記；當天最後一次修改之後，重檢、重記一次，單獨一個 commit。
- 中間的狀態：別的檔記的指紋可以暫時是舊的；正在改、正在審的那份草稿照常跑自己的 Step 3，送審（Step 6）與取代（Step 7）之前也要先是新的。
- 工具：draft.py 加子指令 `recheck`，一個指令做完：
  - 找出記錄 ste-custom.md、指紋不是現在這個的檔。
  - 草稿照 Step 3 的檢查重跑，報告與 findings 寫進它的 Checkpoint Dir，存 `step_3` 群組；草稿取代過的 STE 檔跑 `check_ste.py --ste`；中文版跟著它的英文檔。
  - 通過的才重記；沒通過的不重記，列出檔名與 FAIL，以 1 結束；新的 WARN 也列出來，但照樣重記。
- 文件：ste-custom.md 第 9 行、asd-ste 的 README（When the Skill Is Changed 與要跑的檢查）、SKILL.md 的 Step 6 與 Step 7，各自的中文版照 chinese skill 跟著改。
- 提交：本 task 一個 commit，前綴 `task 52`。

### 結果（2026-10-18）

- draft.py 加上 `recheck`：找出記錄 ste-custom.md、指紋不是現在這個的檔，依種類重檢；草稿的檢查先寫到暫存目錄，通過才搬進 Checkpoint Dir，所以沒通過的草稿，原本的報告不會被蓋掉。
  新的 WARN 以拿掉行號之後的文字和上次的報告比對，所以前面多一行不會被當成新的；草稿的 `step_3` 群組沿用上次 `warnings_left` 的理由，新的寫明尚未讀過。
  草稿取代過的 STE 檔沒有上次的報告可比，所以列出它全部的 WARN。
- SKILL.md 的 Step 6 與 Step 7 開頭比對 `custom_fingerprint` 與 `depends_on.py hash` 的結果，不同就先重跑 Step 3（Step 7 再加上 Step 6）；用 `step_3` 的紀錄比，不用 `depends_on.py check`，因為 README-tmp 的草稿檔頭有 `{COMMON_PATH}`，沒有 `--config` 就檢查不了。
- ste-custom.md 第 9 行改成四句：改了不必立刻重檢、當天最後一次修改之後跑一次 `recheck` 並單獨 commit、它怎麼檢查與重記、正在處理的草稿是例外。
- README 的 When the Skill Is Changed：draft.py 與 ste-custom.md 兩處，以及改完要跑的檢查多一項 `recheck` 的測試。

## 3. 要做的

1. draft.py 加上 `recheck`，docstring 一起改。
2. SKILL.md 的 Step 6 與 Step 7：開始之前比對 `step_3` 群組的 `custom_fingerprint` 與 ste-custom.md 現在的指紋，不同就先重跑 Step 3（Step 7 再加上 Step 6）。
3. ste-custom.md 第 9 行改成集中重記的做法，指向 `recheck`。
4. README 的 When the Skill Is Changed：draft.py 與 ste-custom.md 兩處、已寫出的產出，以及改完要跑的檢查。
5. 三份中文版照 chinese skill 跟著改。
6. 照 README 跑它列出的檢查。
   ste-custom.md 這次也改了，22 份照新的做法，等當天最後一次修改之後由 `recheck` 一次重記，另一個 commit；這件例行工作由 [[rerecord-ste-custom]] 接手。

## 4. 驗證

- 在 workspace 以外的副本上：ste-custom.md 加一列之後，`recheck --dry-run` 列出 22 份與各自的檢查；`recheck` 全部重記，6 份草稿存了 `step_3`；之後 `--dry-run` 一份都不列。
- 副本上讓一份草稿出現 FAIL：那一份與它的中文版不重記，`recheck` 以 1 結束；出現新的 WARN 的那一份照樣重記，並列出那則 WARN。
- README 列出的檢查都通過。

## 5. 與其他 task 的關係

- [[Task 50]]：每份 STE 檔都宣告 `[[ste-custom]]`，所以 ste-custom.md 一改就是 22 份。
- [[Task 51]]、[[Task 32.6]]：2026-10-18 另外兩次修改 ste-custom.md。
- [[rerecord-ste-custom]]：執行本 task 定下的集中重記，每次的結果記在那裡；由 [[Task 53]] 建立。

## 6. 知識

—

## 7. 日誌

### 2026-10-30

- [[Task 86]] 把 chore 改用名稱：本檔的 `[[Chore N]]` 連結改成新名稱。

### 2026-10-18

- 建立。
- 同日做完：draft.py 的 `recheck`、SKILL.md 的 Step 6 與 Step 7、ste-custom.md 與 README，三份中文版照 chinese skill 只改 change set。
- 驗證：在 workspace 以外的副本上，ste-custom.md 多加一列之後，`--dry-run` 列出 22 份；`recheck` 重記 20 份，加了分號的 scratch-rules 草稿與它的中文版保留舊紀錄、以 1 結束，它原本的報告沒被蓋掉；tools 草稿多出的字列為新的 WARN 並照樣重記，`step_3` 記下它；拿掉分號之後再跑，2 份重記、以 0 結束，`--dry-run` 一份都不列。
  README 的其他檢查：`draft.py paths`、`replace`（第二次以 1 結束）與 `dependents` 照舊；三對中英對照 `check_parity.py` 0 failure、警告和改之前相同，`diff_md.py --verify` 都是 0 failure；SKILL.md 與 README.md 的 `depends_on.py check` 都是 UNCHANGED；check-skill 的 `scan_skill.py` 只多了行號、Step 6 用到的兩個詞，以及 draft.py 照 Step 7 的規定把 `config.yaml` 傳給 `depends_on.py`。
