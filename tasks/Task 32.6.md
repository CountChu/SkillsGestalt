# Task 32.6 - report-yaml-rules

**Status**：完成——2026-10-18 第二輪審核 14 項全部通過，同日由 Step 7 取代原檔與它的中文版。
**Raised**：2026-10-12，[[Task 32]] 提出時列出的草稿之一，原本是它要做的 2.6。
**Depends on**：—

## 1. 背景

審核 [[Task 31]] 為 [report-yaml-rules.md](../.github/common/rules/report-yaml-rules.md) 產生的 STE 草稿與草稿中文版；通過就由 asd-ste 的 Step 7 取代原檔與它的中文版。
分工、取代的方式與「每取代一份要一併做的」，見 [[Task 32]]。

## 2. 現況

### 審核時決定的

- **report-yaml-rules 的標題**（2026-10-16）：清冊沒有問任何字，但 Rules 的 rule 字典沒有收錄，和 report-md-rules 的 Update 是同一個落差。
  使用者決定把 rule 收進 ste-custom.md，只核准「一條規定」這個意思；另開 [[Task 44]] 一次改完，另外 10 份 STE 檔與草稿都不再把 rule 列為技術用字。
  Checkpoint 是技術名詞，本來就在 Technical words；YAML 是名稱。
- **report-yaml-rules 送審前不先改**：第 35 行的 You made it.、第 20 行的 agrees with、第 45 行的 change 與第 12 行的 cannot set 可能改了句意，照使用者的決定只列進審核重點。
- **第二輪的兩項 `[x]`**（2026-10-18）：使用者在對照頁上把英文第 3 點的第 1、3 項標成 `[x]`。
  第 35–36 行併成一句「A time that you get again from other data is false, because you did not measure it.」：STE 沒有 fabricated，改用專案核准詞 false；中文版寫「從其他資料再次取得的時間是捏造的，因為你並沒有量到它。」，「捏造」沿用原文中文版的說法。
  第 46 行改成「If the YAML file is there, merge or update only the related `step_{number}` group.」，中文版寫「只合併或更新」。
  merge 照使用者的提議收進 ste-custom.md，只核准「把新的值併進既有的檔案或群組，沒有改的值照舊」這個意思；在本 task 裡做，不另開 task。

### 進度

- report-yaml-rules：2026-10-16 以 Step 6 產生對照頁送審，連結是 `http://127.0.0.1:8790/rules-report-yaml-rules/`。
  送審前重跑 Step 1，存下標題詞的判定；Step 3 原本停在 2026-10-12，重跑 PASS，沒有任何警告，也沒有用到專案核准詞，所以不宣告 `[[ste-custom]]`。
  `[[ASD-STE100_ISSUE9.pdf]]` 重記，指紋不變，日期改成 2026-10-16；原文與草稿兩對中英對照的 `check_parity.py` 都是 0 failure。
  審核重點英文 4 項、中文 2 項，共 14 個審核狀態、41 個行號：檔頭、標題用字、四處句意與結構。
  2026-10-18 起每份 STE 檔都宣告 `[[ste-custom]]`（[[Task 50]]）：草稿與中文版第 4 行補上並記錄，Step 3 重跑 PASS，註記的草稿行號跟著加 1、兩項「檔頭」改寫，對照頁重建，仍是 14 項、41 個行號。
  第二輪（2026-10-18）：兩項 `[x]` 改好，草稿與中文版各少一行；草稿中文版照 chinese skill 只改 change set，`check_parity.py` 0 failure，`diff_md.py --verify` PASS。
  merge 收進 ste-custom.md 之後，記錄它的 22 份都重新檢查：6 份草稿重跑 Step 3 都 PASS，除了本草稿多了 false、merge、update 的 `[INFO]`，報告和之前相同；5 份 STE 檔的 `check_ste.py --ste` PASS，警告和之前相同。
  22 份都重記 `[[ste-custom]]`（新指紋 `87b027217859`），`depends_on.py check` 都是 UNCHANGED；ste-custom 中英兩份 `check_parity.py` 0 failure。
  註記改寫兩項 `[x]` 與中文對應的兩項，註明第二輪已改，行號跟著減 1；對照頁重建，仍是 14 項、41 個行號，已通過的 3 項維持通過，其餘 11 項待審。
  [[Task 52]] 改了 ste-custom.md 之後，[[rerecord-ste-custom]] 當天集中重記（2026-10-18）：草稿與中文版重記 `[[ste-custom]]`（新指紋 `3c5050b6a240`），Step 3 PASS、沒有警告，`step_3` 已存；對照頁也已重建，仍是 14 項，3 項通過、11 項待審。
- 取代（2026-10-18）：第二輪 14 項全部通過；Step 3 記下的 ste-custom 指紋仍是現在的 `3c5050b6a240`，所以 Step 7 不必先重跑 Step 3 與 Step 6。
  `draft.py replace` 把草稿與它的中文版寫回 report-yaml-rules.md 與 report-yaml-rules-tw.md，檔頭註記刪成兩行，再刪掉兩份草稿；兩份都是 44 行。
  `draft.py dependents` 以本 workspace、InvestForge 與 BookMaster 為 root，只找到 asd-ste 的 README.md 與 README-tw.md；它們引用的是 YAML checkpoint 的格式與必要欄位，STE 版的規則相同，讀過都仍成立，重記（新指紋 `5bca1fce746c`）。
  檢查：`check_ste.py --ste` PASS，沒有警告；parity check 0 failure、0 warning；兩份 README 的 `depends_on.py check` 都是 UNCHANGED；`draft.py recheck --dry-run` 一份都不列。
  [[Task 31]] 表格裡指向兩份草稿的連結改成行內程式碼，並註明已取代。

### 審核紀錄

- 2.6 report-yaml-rules——對照頁 2026-10-16 送審，共 14 項；標題的 Rules 由 [[Task 44]] 收進 ste-custom，Checkpoint 保留。
  第二輪（2026-10-18）：英文第 3 點的第 1 項（You made it.）與第 3 項（change）標 `[x]`，照使用者的決定改寫；檔頭、標題用字與第 20–21 行（agrees with）通過。
  同日再審，14 項全部通過，由 Step 7 取代原檔。

## 3. 要做的

—

## 4. 驗證

—

## 5. 與其他 task 的關係

- [[Task 44]]：2026-10-16 審 report-yaml-rules（2.6）時開出——rule 收進專案核准詞，同日做完；2.3、2.5 的草稿也因此改了 Technical words 那一行。
- [[Task 52]]：Step 6、7 一開始比對 `step_3` 的 `custom_fingerprint`，ste-custom.md 改過就先重跑 Step 3；取代本草稿時會用到。
- [[Task 53]]：建立 chore 制度，例行的重記寫成 chore。
- [[rerecord-ste-custom]]：ste-custom.md 有改動的日子集中重記一次，本草稿與它的中文版也在其中。

## 6. 知識

—

## 7. 日誌

### 2026-10-30

- [[Task 86]] 把 chore 改用名稱：本檔的 `[[Chore N]]` 連結改成新名稱。

### 2026-10-18

- 從 [[Task 32]] 拆出：原本是它要做的 2.6；屬於這份檔案的內容搬到這裡，內容沒有改。
- report-yaml-rules（2.6）：[[Task 50]] 決定每份 STE 檔都宣告 `[[ste-custom]]`，草稿與中文版補上並記錄，Step 3 PASS，對照頁重建（註記的草稿行號加 1，兩項「檔頭」改寫）。
- 第二輪：兩項 `[x]` 改好——第 35–36 行用 false 併成一句，第 46 行寫 merge or update；merge 收進 ste-custom.md，22 份重檢、重記，對照頁重建。
- [[rerecord-ste-custom]] 集中重記 ste-custom：草稿 Step 3 PASS，對照頁重建；這個檔的 Status、要做的與關係跟著更新。
- 第二輪審核 14 項全部通過，由 Step 7 取代原檔與它的中文版；asd-ste 的 README 兩份重記，[[Task 31]] 表格的草稿連結改成行內程式碼。

### 2026-10-16

- report-yaml-rules（2.6）：重跑 Step 1 與 Step 3，對照頁送審；標題的 rule 由 [[Task 44]] 收進專案核准詞。

### 2026-10-12

- 列為 [[Task 32]] 要審核的草稿之一。
