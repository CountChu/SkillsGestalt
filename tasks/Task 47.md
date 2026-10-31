# Task 47 - 把 phrase 收進專案核准詞，STE 檔不再把它列為技術用字

**Status**：完成——2026-10-16 建立，同日在建立它的 session 做完：phrase 成了專案核准詞，兩份 STE 檔不再把它列為技術用字。
**Raised**：2026-10-16，[[Task 32]] 審 tw-keep-english 的草稿（2.3）時，第 8 項第 2 個子項（term 的定義）標 `[?]`：草稿因為 phrase 不在 STE 字典裡，把原文的「a word or a phrase」寫成「a word or a group of words」；使用者提議把 phrase 收進 ste-custom.md。
**Depends on**：—

## 1. 背景

phrase 不在 STE Issue 9 的字典裡。
tw-keep-english 的草稿與 RSDC-Standard.md 把它列在 `Technical words:`，各在正文用了一次；但 tw-keep-english 草稿對 term 的定義卻避開它，寫成 a group of words。
phrase 是一般語言裡的詞，不是某個主題的技術名詞（STE 規則 1.5），和 [[Task 44]] 的 rule 一樣，比較適合當專案核准詞：[ste-custom.md](../.github/common/skills/asd-ste/references/ste-custom.md) 核准的字不列為技術用字（House Rule 11）。

## 2. 現況

### 已決定（2026-10-16）

- phrase 收進 ste-custom.md：詞性 n，意思是「a group of words that go together, as in "a word or a phrase"」；複數由 `check_ste.py` 自動接受，Forms 寫「—」。
- tw-keep-english 的草稿：`Technical words:` 拿掉 phrase；第 24 行的定義改成「A term is a word or a phrase that always identifies the same type of item in a document.」，中文版寫「詞或片語」，和原文中文版一致。
- RSDC-Standard.md：`Technical words:` 拿掉 phrase；只改文字，版本維持 261016；這一行算在指紋裡，記錄它的 8 份重記。
- 宣告 `[[ste-custom]]` 的 20 份這次一起重查、重記：7 份草稿重跑 Step 3，DFD、RSDC-Standard、md-style 跑 `check_ste.py --ste`。
- 對照頁：2.3 的這次重建，第 8 項的兩個相關子項註明第六輪已改；其他草稿的對照頁等下次 `run step 6` 更新。
- 提交：commit 前綴 `task 47`，兩個 repo 各一個；[[Task 32]] 2.3 的紀錄放進同一個 commit；InvestForge 只提交 RSDC-Standard 的檔頭紀錄那一行。

### 結果（2026-10-16）

- ste-custom.md 與中文版加上 phrase 一列；新指紋 `873052180f83`。
- tw-keep-english 的草稿與中文版：Technical words 拿掉 phrase，剩 125 個；第 24 行的定義改成「a word or a phrase」，中文版寫「詞或片語」。
- RSDC-Standard 與中文版：Technical words 拿掉 phrase，剩 124 個，版本維持 261016。
- 7 份草稿重跑 Step 3 都 PASS：和上次比，只差在 phrase 列進專案核准詞的 `[INFO]`，警告和之前相同；DFD、RSDC-Standard、md-style 的 `check_ste.py --ste` PASS。
- 重記：宣告 `[[ste-custom]]` 的 20 份，以及記錄 RSDC-Standard.md 的 8 份（InvestForge 4 份）；DFD 與 md-style 的正文沒變，記錄它們的文件不用重記。
- [[Task 32]] 的 2.3：第 8 項第 2 個子項更正 phrase 的說法，「定義的意思可能變了」那一項註明第六輪已改；對照頁重建，共 29 項、140 個行號，15 項維持通過。

## 3. 要做的

1. ste-custom.md 加上 phrase 一列，中文版照 chinese skill 跟著改。
2. tw-keep-english 的草稿與中文版、RSDC-Standard 與中文版：`Technical words:` 拿掉 phrase；草稿第 24 行的定義改用 phrase。
3. 7 份草稿重跑 Step 3，3 份 STE 檔跑 `check_ste.py --ste`；20 份重記 `[[ste-custom]]`。
4. 記錄 RSDC-Standard.md 的 8 份讀過改動後重記，其中 InvestForge 4 份。
5. 跑 asd-ste 的 README 為 ste-custom.md 列出的檢查；2.3 的對照頁重建。

## 4. 驗證

- ste-custom 與改到的每一對中英對照：`check_parity.py` 0 failure，`diff_md.py --verify` PASS。
- 7 份草稿的 Step 3 與 3 份 STE 檔的 `check_ste.py --ste` 都 PASS，警告和之前相同。
- 重記的文件 `depends_on.py check` 都是 UNCHANGED；兩份 RSDC 範本的 `check_rsdc.py --standard` PASS。

## 5. 與其他 task 的關係

- [[Task 32]]：審 2.3 時提出。
- [[Task 44]]：把 rule 收進專案核准詞，本 task 照同樣的做法處理 phrase。

## 6. 知識

—

## 7. 日誌

### 2026-10-16

- 建立：決定把 phrase 收進 ste-custom.md，兩份 STE 檔不再把它列為技術用字，草稿的定義改用 phrase。
- 做完：ste-custom、RSDC-Standard、tw-keep-english 草稿三對中英對照 `check_parity.py` 0 failure、警告和之前相同，`diff_md.py --verify` 都 PASS；宣告 `[[ste-custom]]` 的 10 對 `check_parity.py` 都是 0 failure。
  重記的 28 份 `depends_on.py check` 都是 UNCHANGED；兩份 RSDC 範本的 `check_rsdc.py --standard` 都是 8 項 PASS。
