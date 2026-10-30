# Task 32.4 - md-style

**Status**：完成——2026-10-14 第三輪通過，同日由 Step 7 取代原檔。
**Raised**：2026-10-12，[[Task 32]] 提出時列出的草稿之一，原本是它要做的 2.4。
**Depends on**：—

## 1. 背景

審核 [[Task 31]] 為 [md-style.md](../.github/common/rules/md-style.md) 產生的 STE 草稿與草稿中文版；通過就由 asd-ste 的 Step 7 取代原檔與它的中文版。
分工、取代的方式與「每取代一份要一併做的」，見 [[Task 32]]。

## 2. 現況

### 進度

- md-style：2026-10-14 以 Step 6 產生對照頁送審，連結是 `http://127.0.0.1:8790/rules-md-style/`。
  送審前重跑檢查：`check_ste.py` PASS，只有 no-op 被拆成 op 的 3 個警告；原文與草稿兩對中英對照的 `check_parity.py` 0 failure；草稿兩份的 `depends_on.py check` 都是 UNCHANGED。
  審核重點英文 7 項、中文 6 項，共 27 個審核狀態、89 個行號：a different line 讀不出獨佔一行（附上字典核准的寫法）、「two decisions」底下有四項（原文也一樣，審核時決定）、轉換 3–6 的粗體標籤照 House Rule 9 照抄、四處句意、美式拼法的例字從斜體改成引號，以及結構。
  原文第 12、44 行一行有好幾句，是 `reformat_md.py` 遇到含 `$$` 的行就不斷句，連 inline code 裡的也算，記成 [[Task 42]]。
  第二輪（同日）：第 38 行改成「start each sentence after the first on a new line」，第 85 行改成「on lines that do not contain the math」，第 116 行改成「a line that contains only the `6`」；第 103–105 行重排成先說 repo 檔案的集合名稱、再以 if 句說執行會怎樣、最後以 Thus 說所以只在 raw mode 執行。
  Step 3 重跑 PASS，仍只有那 3 個 op 警告；草稿中文版照 chinese skill 只改 change set，`check_parity.py` 0 failure，`diff_md.py --verify` PASS。
  當時另一個 session 重記 `[[ste-custom]]` 還沒 commit，中文版有自己的修改，`diff_md.py` 判成 FULL；所以在 scratchpad 以目前的 commit 建一個共用 clone，只放進英文的改動來算 change set，結果是 INCREMENTAL 的 5 行。
  第三輪（同日）：第 86 行拿掉數目，寫「These decisions are important:」；第 104 行寫明是假設「If the transform also operates in clean mode」；第 107 行寫「the dynamic token extractor」，第 108 行改公式的改成 the transform；第 113 行改成「find a line that contains only a marker」。
  為了通過 STE 檢查調整了措辭：第 104 行原本的 27 字超過描述句的 25 字，拿掉 in that file、改說 that name；第 107 行的 dynamic tokens 會被報成字典沒有的 dynamic，因為技術用字只列單數的 dynamic token，所以改用單數。
  Step 3 第二次 PASS，仍只有那 3 個 op 警告；草稿中文版照 chinese skill 只改 change set，第 107 行的譯文本來就是「dynamic token 的擷取器」，照舊；`check_parity.py` 0 failure，`diff_md.py --verify` PASS。
  取代（同日）：對照頁 27 項全部通過，由 Step 7 取代；`draft.py replace` 把草稿與它的中文版寫回 md-style.md 與 md-style-tw.md，檔頭註記刪成兩行，再刪掉兩份草稿，兩份都是 166 行。
  `draft.py dependents` 以本 workspace、InvestForge 與 BookMaster 為 root，找到記錄 md-style.md 的 6 份：asd-ste、check-skill、gen-skill 的 README 與它們的中文版；它們引用的一句一行與「Write English in American spelling」兩條規則取代後都還在，讀過都仍成立，全部重記。
  檢查：`check_ste.py --ste` PASS，仍是那 3 個 op 警告；parity check 0 failure；6 份的 `depends_on.py check` 都是 UNCHANGED。
  「每取代一份要一併做的」裡 reformat-md 的 Step 0 稽核，這次照使用者的決定略過。
  task-31 表格指向兩份草稿的連結改成行內程式碼，並註明已取代；[[Task 42]] 補記原文那兩行已在取代時拆開；審核伺服器照使用者的決定繼續開著。

### 審核紀錄

- 2.4 ✅ md-style——2026-10-14 第三輪通過；對照頁同日產生並送審，共 27 項。
  同日以審核狀態審：英文第 2 點的三個子項（第 38、85、116 行的 a different line）與中文第 2 點的第一項（第 103–105 行）標 `[?]`，解釋之後決定都照建議改。
  第二輪改好、Step 3 PASS，對照頁重建；這四項，連同同一件事的英文第 5 點第一項與中文第 1 點，註明第二輪已改，回到待審，檔頭維持通過。
  第三輪（同日）：英文第 3 點（two decisions）與第 5 點的前三項（第 103–105、107、113 行）標 `[?]`，解釋之後決定都改；第 3 點只改草稿與它的中文版，原文由 Step 7 取代時換掉。
  第三輪改好、Step 3 PASS，對照頁重建；這四項與中文對應的三項註明第三輪已改，回到待審，其餘 7 項維持通過。
  同日再審，27 項全部通過，由 Step 7 取代原檔。

## 3. 要做的

—

## 4. 驗證

—

## 5. 與其他 task 的關係

—

## 6. 日誌

### 2026-10-18

- 從 [[Task 32]] 拆出：原本是它要做的 2.4；屬於這份檔案的內容搬到這裡，內容沒有改。

### 2026-10-14

- 對照頁送審；第三輪之後 27 項全部通過，由 Step 7 取代原檔與它的中文版。

### 2026-10-12

- 列為 [[Task 32]] 要審核的草稿之一。
