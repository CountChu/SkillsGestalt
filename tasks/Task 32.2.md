# Task 32.2 - RSDC-Standard

**Status**：完成——2026-10-14 第四輪通過，同日由 Step 7 取代原檔。
**Raised**：2026-10-12，[[Task 32]] 提出時列出的草稿之一，原本是它要做的 2.2。
**Depends on**：—

## 1. 背景

審核 [[Task 31]] 為 [RSDC-Standard.md](../.github/common/references/RSDC-Standard.md) 產生的 STE 草稿與草稿中文版；通過就由 asd-ste 的 Step 7 取代原檔與它的中文版。
分工、取代的方式與「每取代一份要一併做的」，見 [[Task 32]]。

## 2. 現況

### 審核時決定的

- **RSDC-Standard 的版本規則自成一節**：換版本的規則從開頭移到文末新的一節 `# Versioning`，放在「Changes in This Version」之前，不編號；原文、草稿與兩份中文版一起改。
  開頭只留 Version 行與兩句指引，新加的一句指到 Versioning。
  原文只搬原本那一句，不加規則；「the version on the line above」搬走之後指不到 Version 行，改成「the Version line at the head of this document」，草稿的第 1 步改成「the Version line at the top of RSDC-Standard.md」。
  只是搬移與改措辭，所以版本不變，「Changes in This Version」也不記；對照頁的行號自動對到新位置，另加一項說明。

### 進度

RSDC-Standard 的草稿當時以為正由別的 session 審核，沒有動；其實是 「O - Task 38」 那個 session 在 14:38 產生對照頁之後就停了。
同日在本 session 接手：RSDC-Standard 重跑 Step 3 PASS，只留原本的 4 個被動句警告，`[[ste-custom]]` 重記，草稿中文版的檔頭跟上。
版本規則移到 Versioning 之後，RSDC-Standard 重跑 Step 3 PASS，仍是那 4 個被動句警告；原文與草稿兩對中英對照的 `check_parity.py` 0 failure。
記錄 RSDC-Standard.md 的 8 份讀過改動都仍成立，全部重記，`depends_on.py check` 都是 UNCHANGED；InvestForge 的 4 份在 `ac63dfd`，只提交檔頭那一行；兩份 RSDC 範本的 `check_rsdc.py --standard` PASS。
對照頁重建：說明裡的行號自動對到新位置，版本規則那幾處手改，再加上 Versioning 一項，共 15 項、84 個行號。
原本還沒決定的「是否在 RSDC-Standard.md 的「Changes in This Version」補一句說明 DFD.md 的修改」，2026-10-13 審 RSDC-Standard 時決定記，見下一項。
- RSDC-Standard 第二輪（2026-10-13）：使用者在對照頁上把第 12、16 項標成 `[x]`，再改標 `[?]` 要求解釋；解釋之後決定「12 記、16 改」。
  草稿第 408–410 行改成 RSDC-Standard 那句不寫日期、說清楚沒改的是給 RSDC 的規則，只改了本標準自己的版本規則；另起一段（第 412–414 行）記 DFD 在 2026-10-13 經三次審核後由 STE 版取代、不再提 RSDC、README 與版本、標題與範例名稱的改動。
  第 157 行改成「只用 stage 邊界上的輸入與輸出，以及它們的先後順序來說明規則」。
  為了通過 STE 檢查調整了措辭：three rounds of review 寫成 we examined it three times，under the heading 寫成 in the section。
  Step 3 重跑 PASS，仍只有那 4 個被動句警告；草稿中文版照 chinese skill 只改 change set，`check_parity.py` 0 failure，`diff_md.py --verify` PASS。
  註記只在改到的第 9–12、16、34、41 項註明第二輪已改；這幾項的文字變了，回到待審，其餘項目的狀態保留。
- RSDC-Standard 第三輪（2026-10-13）：使用者在對照頁上把第 17、18、24、25、28、29 項標成 `[?]` 要求解釋；解釋之後決定都改。
  第 214–215 行改問預設有哪些人或 system 可以存取它，第 207、368 行的「a person saw」改成由人或測試證明（a person or a test shows）。
  第 64 行改成「as the goal of all its work」，第 281 行改成兩種工作之間的 boundary 就在那個 component 裡。
  Presentation Form 內文的 function 一律改成 capability，並列進 Technical words；第 327 行改用 unsatisfactory，和第 90 行一致。
  為了通過 STE 檢查調整了措辭：final purpose 寫成 the goal of all its work，inside 寫成 in。
  Step 3 重跑 PASS，仍只有那 4 個被動句警告；草稿中文版照 chinese skill 只改 change set，capability 保留英文，`check_parity.py` 0 failure，`diff_md.py --verify` PASS。
  註記只在改到的第 17、18、24、25、28、29 項與中文的第 35、36、38 項註明第三輪已改；這幾項回到待審，其餘項目的狀態保留。
  第二輪在第 408–414 行多出 4 行之後，中文第 31、38 項有幾個行號連結沒跟著移，這次一併更正。
- RSDC-Standard 第四輪（2026-10-14）：使用者把中文第 38 項（「功能」指兩件事）標成 `[x]`。
  查了 Issue 9：purpose 已從字表移除，只列為第 21 類（法律與規範）的技術名詞；capability 是不核准的字，替代字是 FUNCTION 與 CAN。
  使用者決定把兩個字都收進 ste-custom.md：purpose 取一般的意思，capability 只限規格要求 system 要能做到的事，例如對照表的每一列。
  草稿第 110、677 行的 function 改成 purpose，中文版的「功能」改成原文中文版的「用途」；capability 從 Technical words 拿掉，用字不變，第 323 行的粗體標題照舊。
  ste-custom.md 改了之後，宣告它的 7 份 STE 檔都重新檢查：6 份草稿重跑 Step 3 都 PASS，警告和之前相同，DFD.md 的 `check_ste.py --ste` PASS；連同中文版共 14 份重記。
  README-tmp 的草稿照使用者的決定，從 Technical words 拿掉 Purpose；它是大寫的欄位名稱，`check_ste.py` 本來就當名稱略過，檢查結果不變。
  asd-ste 的 README 列出的檢查：ste-custom 中英兩份 `check_parity.py` 0 failure，SKILL.md 與 README.md 的 `depends_on.py check` 都是 UNCHANGED，check-skill 的結果和之前相同，description 超過 1024 字元等兩項仍待決定。
  註記只在第 20、28、38 項註明第四輪已改，這三項回到待審，其餘 40 項維持通過。
  `check_ste.py` 對字典不核准的技術用字不提醒，記成 [[Task 41]]。
- RSDC-Standard：2026-10-14 對照頁 43 項全部通過，同日由 Step 7 取代。
  `draft.py replace` 把草稿與它的中文版寫回 RSDC-Standard.md 與 RSDC-Standard-tw.md，檔頭註記刪成兩行，再刪掉兩份草稿；兩份都是 724 行，Version 行是「**Version**: 261010.」。
  `draft.py dependents` 以本 workspace、InvestForge 與 BookMaster 為 root，找到記錄 RSDC-Standard.md 的 8 份：兩份 RSDC 範本與它們的中文版，InvestForge 的 StopPriceChecker-RSDC、InvCov-RSDC 與它們的中文版；BookMaster 也用這個 skill group，但沒有文件記錄它。
  8 份都只在檔頭引用它，範本另記版本 261010；範本照抄的規格問題（例如第 8 題）和 STE 版的意思一致，讀過都仍成立，全部重記；InvestForge 的 4 份在 `7b40f92`，只提交檔頭那一行，StopPriceChecker-RSDC 其餘的修改是別的 session 的。
  檢查：`check_ste.py --ste` PASS，仍是那 4 個被動句警告；parity check 0 failure，只有原本的「元數據」警告；8 份的 `depends_on.py check` 都是 UNCHANGED；兩份 RSDC 範本的 `check_rsdc.py --standard` 各 6 項 PASS。
  task-31 表格與 task-23 指向草稿的連結改成行內程式碼，並註明已取代；審核伺服器照使用者的決定繼續開著。

### 審核紀錄

- 2.2 ✅ RSDC-Standard——2026-10-14 第四輪通過；對照頁 2026-10-13 送審；標題的 way（One-way）與 Design 判定保留，不列進 Technical words；同日版本規則移到新的一節 Versioning，對照頁重建後再送審。
  同日起以審核狀態審：第 12 項決定記 DFD 的取代、第 16 項決定改第 157 行，第 10、11 項一起說清楚；第二輪改好、Step 3 PASS，對照頁重建，這四項回到待審。
  第三輪（同日）：第 17、18、24、25、28、29 項決定都改；改好、Step 3 PASS，對照頁重建，這六項與中文對應的三項回到待審。
  第四輪（2026-10-14）：中文第 38 項標 `[x]`；purpose 與 capability 收進 ste-custom，Step 3 PASS，對照頁重建，第 20、28、38 項回到待審。
  同日再審，43 項全部通過，由 Step 7 取代原檔。

## 3. 要做的

—

## 4. 驗證

—

## 5. 與其他 task 的關係

—

## 6. 日誌

### 2026-10-18

- 從 [[Task 32]] 拆出：原本是它要做的 2.2；屬於這份檔案的內容搬到這裡，內容沒有改。

### 2026-10-14

- 第四輪審核通過（43 項），由 Step 7 取代原檔與它的中文版。

### 2026-10-13

- 第二、三輪的意見改好，Step 3 PASS，對照頁重建，改到的項目回到待審。

### 2026-10-12

- 列為 [[Task 32]] 要審核的草稿之一。
