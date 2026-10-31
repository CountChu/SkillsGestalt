# Task 32.7 - scratch-rules

**Status**：完成——2026-10-18 第三輪之後對照頁 15 項全部通過，同日由 Step 7 取代原檔與它的中文版。
**Raised**：2026-10-12，[[Task 32]] 提出時列出的草稿之一，原本是它要做的 2.7。
**Depends on**：—

## 1. 背景

審核 [[Task 31]] 為 [scratch-rules.md](../.github/common/rules/scratch-rules.md) 產生的 STE 草稿與草稿中文版；通過就由 asd-ste 的 Step 7 取代原檔與它的中文版。
分工、取代的方式與「每取代一份要一併做的」，見 [[Task 32]]。

## 2. 現況

### 審核時決定的

- **標題的 File**（2026-10-18）：「# Scratch File Rules」的 File 字典不核准當動詞；這裡是名詞 scratch file，使用者判定當技術名詞保留（rule 1.5），本來就在 Technical words，原文不改。
- **送審前不先改**：比對時找到四處可能改了句意或用字——第 40 行的 git clean -fd、第 21 行的 a different path、第 19 行的 between two steps、第 15 與 25 行的 make 與 create——照使用者的決定只列進審核重點，附上建議寫法，由審核決定。
  第 32 行少了 deliberately、第 44 行少了 built，合成一項小改動列進去。
- **第二輪的三項**（2026-10-18）：第 40、19 行標 `[x]`，第 21 行標 `[?]`；解釋之後，第 40、19 行照建議改，第 21 行改用 own。
  第 40 行改成「Also, if you use `git clean -fd` after a commit, it removes the file, and does not get your approval first.」，第 19 行的 JSON 檔改成「a JSON file that the run uses before it writes its outputs」。
- **own 收進專案核准詞**（2026-10-18）：使用者決定把 own 收進 ste-custom.md，詞性 adj 與 pron，兩種用法各寫一句意思；記在本 task，不另開 task。
  第 21 行改成「Each of these outputs has its own path.」，和原文一樣；中文版寫「各有自己的路徑」。
  宣告 ste-custom 的其他 STE 檔，照 [[rerecord-ste-custom]] 在當天 ste-custom.md 的修改都做完之後一次重記。
- **make 與 create**（2026-10-18）：這一項標 `[?]`；解釋之後，使用者決定擴大 ste-custom 裡 create 的核准意思，加上新的目錄，Why 欄補記這次的決定。
  草稿第 15 行改成「create it」、第 25 行改成「created」，和原文一樣；中文版第 15 行本來就寫「建立」，第 25 行的「產生」改成「建立」。
  其他還沒審完的草稿，原文寫 create、草稿寫 make 的地方，審到那一份時再看。

### 進度

- 2026-10-18 重跑 Step 1：清冊 rewritable，只問標題的 File，判定存進 checkpoint 的 `heading_words`。
  Step 3 是同日重跑的：PASS，沒有警告；noise 是字典核准、用在技術意思的字，rule 是專案核准詞。
  以 Step 6 產生對照頁送審，連結是 `http://127.0.0.1:8790/rules-scratch-rules/`。
  審核重點英文 5 項、中文 3 項，共 15 個審核狀態、48 個行號：檔頭、標題用字、三處句意與一項小改動、make 與 create、結構；中文另說明 workspace、script、step 照 tw-keep-english 保留英文。
  第二輪（同日）：ste-custom.md 加上 own 一列，中文版照 chinese skill 跟著改，先單獨提交；新指紋 `4f28cc39ac22`。
  草稿改第 19、21、40 行，Step 3 PASS，沒有警告，own 列進專案核准詞的 `[INFO]`；草稿中文版照 chinese skill 只改 change set 的 4 行（檔頭一行與第 19、21、40 行），`check_parity.py` 0 failure，`diff_md.py --verify` PASS。
  對照頁重建：改到的 3 項與中文對應的 3 項註明第二輪已改，回到待審，檔頭與標題用字維持通過。
  第三輪（同日）：ste-custom.md 裡 create 的意思加上新的目錄，中文版跟著改；草稿改第 15、25 行，Step 3 PASS，沒有警告，create 列進專案核准詞的 `[INFO]`。
  草稿中文版照 chinese skill 只改 change set：檔頭一行與第 25 行，第 15 行的譯文照舊；`check_parity.py` 0 failure，`diff_md.py --verify` PASS；對照頁重建，這一項回到待審。
- 取代（2026-10-18）：第三輪之後 15 項全部通過；Step 3 記下的 ste-custom 指紋仍是現在的 `e12251a917f1`，所以 Step 7 不必先重跑 Step 3 與 Step 6。
  `draft.py replace` 把草稿與它的中文版寫回 scratch-rules.md 與 scratch-rules-tw.md，檔頭註記刪成兩行，再刪掉兩份草稿；兩份都是 52 行。
  `draft.py dependents` 以本 workspace、InvestForge 與 BookMaster 為 root，只找到 check-skill 的 README.md 與 README-tw.md；它們引用的是 facts 檔放在哪裡、怎麼清掉，STE 版的規則相同，讀過都仍成立，重記（新指紋 `040a0e811927`）。
  正文引用它的兩份範本、本 workspace 9 個 skill 與 InvestForge 4 個 skill 的 SKILL.md，都是整份檔案的引用，說的是一次執行的暫存檔放在哪裡、怎麼清掉，取代後都仍成立，照使用者的決定不動。
  [[Task 31]] 表格裡指向兩份草稿的連結改成行內程式碼，並註明已取代；審核伺服器照使用者的決定繼續開著。

## 3. 要做的

✅ 2026-10-18 審核通過，由 Step 7 取代原檔，[[Task 32]] 的「每取代一份要一併做的」也做完。
今天 ste-custom.md 加上 own、擴大 create 之後，其他宣告它的 STE 檔照使用者的決定交給 [[rerecord-ste-custom]]，在取代之後集中重記。

## 4. 驗證

- 取代後 `check_ste.py --ste` PASS，沒有警告；scratch-rules.md 與它的中文版 `check_parity.py` 0 failure、0 warning。
- 取代後 check-skill 兩份 README 的 `depends_on.py check` 都是 UNCHANGED；兩份 README 的 `check_parity.py` 0 failure，唯一一則「腳本」的 WARN 在取代前就有；check-skill 的 `scan_skill.py` 沒有缺少的 README 標題，檔頭每一項都是 UNCHANGED。

## 5. 與其他 task 的關係

- [[Task 40]]：審本草稿時，使用者問同意某一項的建議該標 `[v]` 還是 `[x]`；它的第 9 項把答案寫進對照頁與 asd-ste 的 SKILL.md。
- [[rerecord-ste-custom]]：ste-custom.md 有改動的日子集中重記一次；本 task 加上 own、擴大 create 的那兩次也由它重記。

## 6. 知識

—

## 7. 日誌

### 2026-10-30

- [[Task 86]] 把 chore 改用名稱：本檔的 `[[Chore N]]` 連結改成新名稱。

### 2026-10-18

- 從 [[Task 32]] 拆出：原本是它要做的 2.7；屬於這份檔案的內容搬到這裡，內容沒有改。
- 重跑 Step 1，標題的 File 判定為名詞、保留；以 Step 6 產生對照頁送審，共 15 項。
- 第二輪：第 40、19 行照建議改，own 收進專案核准詞、第 21 行改用 own；Step 3 PASS，對照頁重建。
- 第三輪：create 的核准意思加上目錄，第 15、25 行改回 create；Step 3 PASS，對照頁重建。
- 對照頁 15 項全部通過，由 Step 7 取代原檔與它的中文版；check-skill 的 README 兩份重記，[[Task 31]] 表格的草稿連結改成行內程式碼。

### 2026-10-12

- 列為 [[Task 32]] 要審核的草稿之一。
