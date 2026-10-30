# Task 32.5 - report-md-rules

**Status**：完成——2026-10-18 對照頁 21 項全部通過，同日由 Step 7 取代原檔。
**Raised**：2026-10-12，[[Task 32]] 提出時列出的草稿之一，原本是它要做的 2.5。
**Depends on**：—

## 1. 背景

審核 [[Task 31]] 為 [report-md-rules.md](../.github/common/rules/report-md-rules.md) 產生的 STE 草稿與草稿中文版；通過就由 asd-ste 的 Step 7 取代原檔與它的中文版。
分工、取代的方式與「每取代一份要一併做的」，見 [[Task 32]]。

## 2. 現況

### 審核時決定的

- **report-md-rules 的標題**（2026-10-14）：三個標題照舊，原文不改。
  Create 是字典不核准的動詞，使用者決定收進 ste-custom.md，只核准「建立新的檔案或資料」這個意思；草稿內文第 11、64 行原本寫 make，改回 create，中文版本來就寫「建立」。
  Update 字典裡沒有，清冊也沒問；判定為電腦作業的技術動詞，列進兩份草稿的 Technical words，但 `check_ste.py` 只在內文找技術用字，Step 3 因此留下一則「listed but never used」的 WARN。
  三個標題的 file 是名詞，當技術名詞保留，本來就在 Technical words。
  清冊不問字典沒收錄的字、技術用字不算標題，以及 SKILL.md Step 1 拿「create 當動詞」當例子，這三項記進 [[Task 41]]，之後再改。
- **report-md-rules 送審前不先改**：比對時發現第 39 行的 a previous value 與第 83 行的 Replace the values 可能改了句意，照使用者的決定只列進審核重點，由審核決定。
- **update 收進專案核准詞**（2026-10-18）：對照頁的 Update 一項標 `[?]`，解釋之後使用者提議把 update 收進 ste-custom.md，因為它的受詞通常是 file。
  另開 [[Task 51]] 做：只核准動詞，意思以 file 為主、也涵蓋檔案裡的資料；草稿不再把它列為技術用字，第 52 行的 Set the **Updated** field 改回 Update，和原文、標題一致。

### 進度

- report-md-rules：2026-10-14 以 Step 6 產生對照頁送審，連結是 `http://127.0.0.1:8790/rules-report-md-rules/`。
  送審前重跑 Step 1，存下標題詞的判定；create 收進 ste-custom 之後，草稿重跑 Step 3 PASS，只留 update 那一則 WARN；草稿與它的中文版 `check_parity.py` 0 failure，`diff_md.py --verify` PASS。
  ste-custom 改了，宣告它的 14 份都重新檢查：另外 4 份草稿重跑 Step 3，報告和改之前相同；DFD.md 與 RSDC-Standard.md 的 `check_ste.py --ste` PASS，警告和之前相同。
  14 份都重記 `[[ste-custom]]`，`depends_on.py check` 都是 UNCHANGED；README-tmp 的兩份檔頭有 `{COMMON_PATH}`，要給 `--config` 才能檢查，所以直接核對那一行。
  ste-custom 中英兩份 `check_parity.py` 0 failure；asd-ste 的 SKILL.md 與 README.md 的 `depends_on.py check` 都是 UNCHANGED；check-skill 的 `scan_skill.py` 只多了 ste-custom 兩份的行數，description 仍是 1259 字元。
  審核重點英文 5 項、中文 3 項，共 21 個審核狀態、55 個行號：檔頭、標題用字、四處句意、名稱與結構。
  tw-keep-english 與 md-style 的對照頁是重記之前建的，草稿檔頭顯示的仍是舊的 `[[ste-custom]]` 指紋，下次 `run step 6` 時就會更新。
  第二輪（2026-10-16）：第 39 行改成「Do not use an estimate or a time that you saw before.」，第 14 行改成「If the file is there, use the rules that follow to update the fields of its header.」，第 44 行改成「Record this canonical skill invocation.」。
  Step 3 PASS，沒有任何警告：第 14 行用了 update，「listed but never used: update」那則 WARN 消失，[[Task 41]] 第 2 項補記了這件事；`[[ASD-STE100_ISSUE9.pdf]]` 與 `[[ste-custom]]` 重記，指紋不變，日期改成 2026-10-16。
  草稿中文版照 chinese skill 只改 change set 的 5 行（檔頭兩行與第 14、39、44 行），`check_parity.py` 0 failure，`diff_md.py --verify` PASS。
  2026-10-18 對照頁以原本的註記重建：[[Task 44]] 與 [[Task 50]] 改了草稿的檔頭（`[[ste-custom]]` 的指紋，Technical words 拿掉 rule），內文沒動。
  同日 [[Task 51]] 把 update 收進專案核准詞：Technical words 剩 45 項，第 52 行改回 Update；Step 3 PASS，沒有警告；結果見 Task 51。
  對照頁再重建一次：Update 一項與中英兩個「檔頭」項改寫成現況。
  取代（同日）：對照頁 21 項全部通過，由 Step 7 取代；`draft.py replace` 把草稿與它的中文版寫回 report-md-rules.md 與 report-md-rules-tw.md，檔頭註記刪成兩行，再刪掉兩份草稿，兩份都是 87 行。
  `draft.py dependents` 以本 workspace、InvestForge 與 BookMaster 為 root，沒有文件在檔頭記錄 report-md-rules.md，所以不必重記。
  正文引用它的 61 份都是整份檔案、標題或 `{USER_PROMPT}` 定義的引用，取代後都仍成立，照使用者的決定不動。
  [[Task 31]] 表格指向兩份草稿的連結改成行內程式碼，並註明已取代；審核伺服器照使用者的決定繼續開著。

### 審核紀錄

- 2.5 report-md-rules——對照頁 2026-10-14 送審，共 21 項；標題的 Create 收進 ste-custom，Update 列為技術動詞，file 保留。
  同日 [[Task 43]] 改了 ste-custom.md 的標題：草稿重跑 Step 3 PASS，結果和上次相同，重記 `[[ste-custom]]`，對照頁以原本的註記重建；草稿文字沒動。
  2026-10-16 以審核狀態審：英文第 3 點的第 1、3、4 項（第 39、14、44 行）與第 4 點的兩項（第 44 行的名稱）標 `[?]`，解釋之後決定都照建議改。
  第二輪改好、Step 3 PASS，連 update 那則 WARN 也消失；對照頁重建，這五項、中文對應的三項與英文第 2 點的 Update 子項註明第二輪，回到待審，其餘 6 項維持通過。
  2026-10-18 再審到 20 項通過，只有 Update 一項標 `[?]`；解釋之後由 [[Task 51]] 把 update 收進專案核准詞。
  改寫的 3 項回到待審，其餘 18 項維持通過。
  同日再審，21 項全部通過，由 Step 7 取代原檔。

## 3. 要做的

✅ 2026-10-18 審核通過，由 Step 7 取代原檔，[[Task 32]] 的「每取代一份要一併做的」也做完。

## 4. 驗證

- 取代後 `check_ste.py --ste` PASS，沒有警告；report-md-rules.md 與它的中文版 `check_parity.py` 0 failure。
- 取代後兩份檔案自己的 `depends_on.py check` 都是 UNCHANGED；沒有依賴方要重記。

## 5. 與其他 task 的關係

- [[Task 51]]：審 Update 一項時開出，把 update 收進專案核准詞。

## 6. 日誌

### 2026-10-18

- 從 [[Task 32]] 拆出：原本是它要做的 2.5；屬於這份檔案的內容搬到這裡，內容沒有改。
- 對照頁以原本的註記重建，檔頭跟上 [[Task 44]] 與 [[Task 50]] 的修改。
- Update 一項標 `[?]`，解釋之後由 [[Task 51]] 把 update 收進專案核准詞；對照頁再重建，改寫的 3 項回到待審。
- 對照頁 21 項全部通過，由 Step 7 取代原檔。

### 2026-10-16

- report-md-rules 第二輪：五項 `[?]` 解釋之後照建議改，草稿與中文版改好、Step 3 PASS，對照頁重建。

### 2026-10-14

- 對照頁送審，共 21 項。

### 2026-10-12

- 列為 [[Task 32]] 要審核的草稿之一。
