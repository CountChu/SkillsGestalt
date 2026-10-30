# Task 44 - 把 rule 收進專案核准詞，STE 檔不再把它列為技術用字

**Status**：完成——2026-10-16 建立，同日在建立它的 session 做完：rule 成了專案核准詞，11 份 STE 檔與草稿都不再把它列為技術用字。
**Raised**：2026-10-16，[[Task 32]] 審 report-yaml-rules 的草稿（2.6）時，標題「YAML Checkpoint Rules」的 rule 不在字典裡；使用者提議把 rule 收進 ste-custom.md。
**Depends on**：—

## 1. 背景

rule 不在 STE Issue 9 的字典裡。
到 2026-10-16 為止，11 份 STE 檔與草稿中有 10 份把它列在 `Technical words:`，只有 report-yaml-rules 的草稿沒有列：它只在標題用到 rule，而 `check_ste.py` 只在內文找技術用字（見 [[Task 41]]）。
rule 是本專案每份文件都用的一般用語，不是某個主題的技術名詞（STE 規則 1.5），比較適合當專案核准詞：[ste-custom.md](../.github/common/skills/asd-ste/references/ste-custom.md) 核准的字是核准詞，不列為技術用字（House Rule 11）。

## 2. 現況

### 已決定（2026-10-16）

- rule 收進 ste-custom.md：詞性 n，意思是「a statement that tells what to do or what not to do, as each item of report-yaml-rules.md」，也就是一條規定。
  複數 rules 由 `check_ste.py` 自動接受，所以 Forms 寫「—」，和其他名詞一樣。
- 時機：另開本 task，現在就做；做完再回 [[Task 32]] 做 2.6 的對照頁。
- 提交：本 task 一個 commit，InvestForge 的重記另一個，前綴都是 `task 44`；2.6 另外一個 commit。
- skill-writing 的草稿：加上 `[[ste-custom]]` 之後，檢查報出它的 Technical words 還列著 Purpose，而 purpose 在 2026-10-14 已是專案核准詞。
  它在草稿裡是大寫的名稱（一個 step 的 Purpose），和 README-tmp 一樣；使用者決定照 README-tmp 的做法，從清單拿掉。

### 結果（2026-10-16）

- ste-custom.md 加上 rule 一列，中文版跟著改；新指紋 `5974f54b37e4`。
- 20 行 Technical words 拿掉 rule，項目數各少一個；RSDC-Standard 的 constraining rule 與 granting rule 是複合的技術用字，照舊。
- scratch-rules、skill-writing、tools 的草稿與中文版加上 `[[ste-custom]]`；skill-writing 兩份的清單另拿掉 Purpose。
- 7 份草稿重跑 Step 3 都 PASS：和上次比，只差在 rule 列進專案核准詞的 `[INFO]`，以及新宣告的三份多了檔頭與拼法的檢查；警告和之前相同。
- DFD、RSDC-Standard、md-style 的 `check_ste.py --ste` PASS，警告和之前相同。
- 重記：宣告 `[[ste-custom]]` 的 20 份；記錄 DFD.md 的 14 份、RSDC-Standard.md 的 8 份、md-style.md 的 6 份，讀過改動都仍成立。

## 3. 要做的

1. ste-custom.md 加上 rule 一列，中文版照 chinese skill 跟著改。
2. 10 份 STE 檔與草稿的 `Technical words:` 拿掉 rule，中文版的「技術用字」那一行同步：
   - STE 檔：DFD.md、RSDC-Standard.md、md-style.md。
   - 草稿：tw-keep-english、report-md-rules、scratch-rules、skill-writing、tools、README-tmp、SKILL-tmp。
3. scratch-rules、skill-writing、tools 的草稿內文用到 rule，卻沒有宣告 `[[ste-custom]]`：草稿與它的中文版都在檔頭加上這一行。
4. 重新檢查：7 份草稿重跑 Step 3，3 份 STE 檔跑 `check_ste.py --ste`。
5. 重記：
   - 宣告 `[[ste-custom]]` 的每一份，包括第 3 項新加的 6 份。
   - DFD.md、RSDC-Standard.md、md-style.md 的 `Technical words:` 那一行算在指紋裡：記錄它們的文件讀過改動之後重記，DFD 14 份、RSDC-Standard 8 份、md-style 6 份，其中 InvestForge 4 份。
6. 跑 asd-ste 的 README 為 ste-custom.md 列出的檢查。

## 4. 驗證

- ste-custom 與 10 份 STE 檔、草稿的中英對照：`check_parity.py` 0 failure，`diff_md.py --verify` PASS。
- 7 份草稿的 Step 3 與 3 份 STE 檔的 `check_ste.py --ste` 都 PASS，警告和之前相同。
- 重記的文件 `depends_on.py check` 都是 UNCHANGED；兩份 RSDC 範本的 `check_rsdc.py --standard` PASS。

## 5. 與其他 task 的關係

- [[Task 32]]：審 2.6 時提出；2.3、2.5 的對照頁是改之前建的，下次 `run step 6` 時更新。
- [[Task 41]]：標題裡用到的字不算進技術用字，所以 report-yaml-rules 的草稿沒有列 rule。
- [[Task 43]]：把 STE customization 改稱專案核准詞。

## 6. 日誌

### 2026-10-16

- 建立。
- 同日做完：ste-custom 加上 rule，20 行 Technical words 拿掉 rule，三份草稿宣告 `[[ste-custom]]`，skill-writing 拿掉 Purpose。
- 驗證：ste-custom 與 10 對中英對照的 `check_parity.py` 都是 0 failure，警告和改之前相同，`diff_md.py --verify` 都是 0 failure。
  7 份草稿的 Step 3 與 3 份 STE 檔的 `check_ste.py --ste` 都 PASS；重記的文件 `depends_on.py check` 都是 UNCHANGED，README-tmp 的兩份檔頭有 `{COMMON_PATH}`，直接核對那一行。
  兩份 RSDC 範本的 `check_rsdc.py --standard` 各 6 項 PASS；asd-ste 的 SKILL.md 與 README.md 的 `depends_on.py check` 都是 UNCHANGED，check-skill 的 `scan_skill.py` 只多了 ste-custom 兩份的行數。
