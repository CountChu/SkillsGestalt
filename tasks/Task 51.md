# Task 51 - 把 update 收進專案核准詞，STE 檔不再把它列為技術用字

**Status**：完成——2026-10-18 建立，同日在建立它的 session 做完：update 成了專案核准詞，report-md-rules 的草稿不再把它列為技術用字。
**Raised**：2026-10-18，[[Task 32.5]] 審 report-md-rules 的草稿時，標題「Update MD report file」的 Update 不在字典裡，原本列為技術動詞；使用者提議把它收進 ste-custom.md，因為它的受詞通常是 file。
**Depends on**：—

## 1. 背景

update 不在 STE Issue 9 的字典裡，既不核准，也不列為不核准。
report-md-rules.md 第二節的標題是「Update MD report file」，標題要照抄，所以草稿把 update 當成電腦作業的技術動詞（STE 規則 1.12），列在 `Technical words:`。
`check_ste.py` 只在內文找技術用字（見 [[Task 41]]），所以只在標題用到時會報「listed but never used」；2026-10-16 第二輪把第 14 行改成用 update 之後，這則 WARN 才消失。
使用者決定照 create 的做法，把 update 收進 [ste-custom.md](../.github/common/skills/asd-ste/references/ste-custom.md)：專案核准詞不列為技術用字（House Rule 11）。

## 2. 現況

### 已決定（2026-10-18）

- update 收進 ste-custom.md：詞性 v，形式 updates、updated、updating；只核准動詞，名詞的 an update 不核准。
- 意思以 file 為主，也涵蓋檔案裡的資料：「to change a file, or the data in it, so that it is current, as a skill updates its MD report file」，所以第 14 行的 update the fields of its header 也在這個意思內。
- 草稿第 52 行原本寫 Set the **Updated** field，照 create 的先例改回 Update，和原文第 36 行、標題一致；中文版跟著改成「更新為」。
- 另開本 task，現在就做；做完再回 [[Task 32.5]]。
- 驗證照 [[Task 44]] 的做法；本 task 一個 commit，Task 32.5 的紀錄另一個。

### 結果（2026-10-18）

- ste-custom.md 加上 update 一列，中文版照 chinese skill 跟著改；新指紋 `d5627f9e2abf`。
- report-md-rules 的草稿與中文版：Technical words 拿掉 update，剩 45 項；第 52 行改回 Update。
  Step 3 PASS，沒有警告，update 列進專案核准詞的 `[INFO]`。
- 其餘 6 份草稿重跑 Step 3 都 PASS，沒有警告，和上次相同；DFD、RSDC-Standard、tw-keep-english、md-style 的 `check_ste.py --ste` PASS，警告和之前相同。
- 宣告 `[[ste-custom]]` 的 22 份都重記；只有檔頭引用區那一行變了，而指紋不算檔頭引用區，所以記錄這些檔案的文件不必重記。
- 對照頁：[[Task 32.5]] 的 Update 一項與中英兩個「檔頭」項改寫成現況，回到待審；[[Task 32.6]] 以原本的註記重建，狀態保留。

## 3. 要做的

1. ste-custom.md 加上 update 一列，中文版照 chinese skill 跟著改。
2. report-md-rules 的草稿與中文版：Technical words 拿掉 update，第 52 行改回 Update。
3. 重新檢查：7 份草稿重跑 Step 3，4 份已取代的 STE 檔跑 `check_ste.py --ste`。
4. 重記宣告 `[[ste-custom]]` 的 22 份。
5. 重建 Task 32.5 與 Task 32.6 的對照頁。
6. 跑 asd-ste 的 README 為 ste-custom.md 列出的檢查。

## 4. 驗證

- ste-custom 與 report-md-rules 草稿兩對中英對照：`check_parity.py` 0 failure，`diff_md.py --verify` PASS。
- 7 份草稿的 Step 3 與 4 份 STE 檔的 `check_ste.py --ste` 都 PASS，警告和之前相同；11 對中英對照的 `check_parity.py` 都是 0 failure，警告和改之前相同。
- 22 份重記之後，`depends_on.py check` 都是 UNCHANGED；README-tmp 的兩份檔頭有 `{COMMON_PATH}`，要給 `--config` 才能檢查，所以直接核對那一行。
- asd-ste 的 SKILL.md 與 README.md 的 `depends_on.py check` 都是 UNCHANGED；check-skill 的 `scan_skill.py` 沒有新的問題，改到的只有 ste-custom 兩份的行數。

## 5. 與其他 task 的關係

- [[Task 32.5]]：審 report-md-rules 時提出。
- [[Task 41]]：標題裡用到的字不算進技術用字；它的第 2 項拿 update 當例子，補記了這次的改動。
- [[Task 44]]、[[Task 47]]、[[Task 49]]：同樣把字收進專案核准詞的先例。

## 6. 知識

—

## 7. 日誌

### 2026-10-18

- 建立，同日做完：ste-custom 加上 update，report-md-rules 的草稿不再列它，第 52 行改回 Update；22 份重記，兩份對照頁重建。
