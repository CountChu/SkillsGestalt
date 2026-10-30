# Task 49 - 把 false 與 false alarm 收進專案核准詞

**Status**：完成——2026-10-17 建立，同日在建立它的 session 做完：false 與 false alarm 成了專案核准詞，草稿寫 without false alarms，中文版寫「誤報」。
**Raised**：2026-10-17，[[Task 32]] 審 tw-keep-english 的草稿（2.3）時，中文第 148 行標 `[?]`：草稿因為 false 不核准、alarm 不在字典裡，把原文的「without false alarms」寫成「without incorrect warnings」，中文版跟著寫成繞口的「不正確的警告」；使用者決定中文改成「誤報」，並把 false alarm 收進 ste-custom.md，false 也核准。
**Depends on**：—

## 1. 背景

STE Issue 9 不核准 false（替代字是 INCORRECT），alarm 則不在字典裡。
tw-keep-english 的原文第 114 行寫「where one can be searched for without false alarms」；草稿改寫成 STE 時只能寫 incorrect warnings，第 59、148 行都是，中文版跟著寫「不正確的警告」。
`check_ste.py` 認得由幾個字組成的核准詞：整個詞組當成一個單位，不再逐字檢查。

## 2. 現況

### 已決定（2026-10-17）

- ste-custom.md 加兩列：
  - false：adj，意思是「not true or not correct, as a false alarm is a warning about a thing that is correct」；從此在任何 STE 檔都能單獨使用。
  - false alarm：n，Forms 寫「false alarms」，意思是「a warning about a thing that is correct, as when a tool finds a rendering in a correct sentence」。
- tw-keep-english 的草稿：第 59、148 行的 incorrect warnings 換成 false alarms，和原文第 114 行同一個說法；第 56 行的 warnings about correct text 照舊。
- 草稿的中文版：第 148 行照英文句式寫成「工具可以在 twin 中檢查其中一些譯法，而不會誤報。」，第 59 行寫成「…能讓工具檢查正文而不誤報。」。
- 宣告 `[[ste-custom]]` 的 20 份這次一起重查、重記；RSDC-Standard 的正文不變，InvestForge 不用重記。
- 對照頁：2.3 的這次重建，中文第 148 行那一項與英文第 5 項第 2 個子項註明第八輪已改。
- 提交：commit 前綴 `task 49`，一個 commit，[[Task 32]] 2.3 的紀錄放在一起。

### 結果（2026-10-17）

- ste-custom.md 與中文版在 phrase 之後加上 false 與 false alarm 兩列；新指紋 `8b3ca12391f5`。
- `check_ste.py` 會先查 ste-custom 再查字典的不核准詞，所以 false 單獨出現時算專案核准詞；false alarm 整個詞組當成一個單位，alarm 不再被報出。
- tw-keep-english 的草稿第 59、148 行改成 without false alarms，中文版改成「誤報」，第 148 行照英文句式寫，主詞改成工具。
- 7 份草稿重跑 Step 3 都 PASS，除了 `[INFO]` 之外和上次相同；DFD、RSDC-Standard、md-style 的 `check_ste.py --ste` PASS。
- 宣告 `[[ste-custom]]` 的 20 份重記；RSDC-Standard 的正文沒變，記錄它的文件不用重記。
- `check_ste.py` 列出「用到的專案核准詞」時不列詞組，所以 false alarm 不會出現在 `[INFO]` 裡；不影響檢查結果。

## 3. 要做的

1. ste-custom.md 加上 false 與 false alarm 兩列，中文版照 chinese skill 跟著改。
2. tw-keep-english 的草稿與中文版改第 59、148 行。
3. 7 份草稿重跑 Step 3，3 份 STE 檔跑 `check_ste.py --ste`；20 份重記 `[[ste-custom]]`。
4. 2.3 的對照頁重建。

## 4. 驗證

- ste-custom 與 tw-keep-english 草稿兩對中英對照：`check_parity.py` 0 failure，`diff_md.py --verify` PASS。
- 7 份草稿的 Step 3 與 3 份 STE 檔的 `check_ste.py --ste` 都 PASS，警告和之前相同。
- 重記的 20 份 `depends_on.py check` 都是 UNCHANGED。

## 5. 與其他 task 的關係

- [[Task 32]]：審 2.3 時提出。
- [[Task 47]]：前一天把 phrase 收進專案核准詞，本 task 照同樣的做法。

## 6. 日誌

### 2026-10-17

- 建立：決定把 false 與 false alarm 收進 ste-custom.md，草稿寫 without false alarms，中文版寫「誤報」。
- 做完：ste-custom 與 tw-keep-english 草稿兩對中英對照 `check_parity.py` 0 failure，`diff_md.py --verify` PASS；宣告 `[[ste-custom]]` 的 10 對 `check_parity.py` 都是 0 failure，重記的 20 份 `depends_on.py check` 都是 UNCHANGED。
