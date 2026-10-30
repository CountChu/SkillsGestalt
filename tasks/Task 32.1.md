# Task 32.1 - DFD

**Status**：完成——2026-10-13 第三輪通過，同日由 Step 7 取代原檔。
**Raised**：2026-10-12，[[Task 32]] 提出時列出的草稿之一，原本是它要做的 2.1。
**Depends on**：—

## 1. 背景

審核 [[Task 31]] 為 [DFD.md](../.github/common/references/DFD.md) 產生的 STE 草稿與草稿中文版；通過就由 asd-ste 的 Step 7 取代原檔與它的中文版。
分工、取代的方式與「每取代一份要一併做的」，見 [[Task 32]]。

## 2. 現況

### 審核時決定的

- **DFD 的拼法**：範例圖把一份資料叫做 `Catalogue`，是英式拼法，而 STE 規則 1.14 要用美式拼法。
  草稿沒有改掉它，因為圖在 fenced block 裡，是照抄原文的 kept span；`check_ste.py` 又略過句中以大寫開頭的字，所以也沒有報出來。
  決定只改範例的名稱：DFD.md 與 DFD-tw.md 的第 46、66、70 行，DFD-ste.md 與 DFD-ste-tw.md 的第 85、105、111 行，都改成 `Catalog`；DFD.md 第 38 行散文裡的 catalogue 不改。
  DFD-tw.md 第 38 行原本也寫 `Catalogue`，只在中文版改成 `Catalog`。
- **DFD 的標題**：`# Kinds of Data` 在四份都改成 `# Types of Data`，原文是第 10 行，草稿是第 26 行。
  STE 字典不核准 kind，要用 type；標題也是 kept span，草稿沒辦法自己改。
- **重記**：上面兩項改了 DFD.md，依賴它的 14 份（見「每取代一份要一併做的」）讀過改動、確認仍然成立之後，以 `depends_on.py record --target` 只重記 DFD 那一行。
- **DFD 第一輪的四點意見**：只改草稿與它的中文版，原文照舊，取代時由草稿換掉。
  1. DFD 不是只給 RSDC 用：仍是 RSDC 標準的一部分，版本也跟標準走，但寫明 skill 的 README.md 也用它——DFD-ste.md 第 14 行改成 the Dataflow in the README.md of a skill，第 20 行句尾加上 and the README.md of a skill also uses it。
     第二輪改成完全不提 RSDC 與 README，見下一項。
  2. 第 33 行的 this 指涉不明，改成 the lines do not show which data the system keeps。
  3. 第 46 行保留 interact：A role interacts with the system；interact 加進 ste-custom.md（v；interacts、interacted、interacting），它的中文版跟著改。
  4. input 與 system 是技術用字：兩份草稿第 8 行的清單都加上；中文版第 47、50 行的「輸入」改回 input，和 DFD-tw.md 一致。
     英文的那兩行沒有改，所以 `diff_md.py --verify` 會把它們列在變動範圍之外。
     清單裡的兩個字之後拿掉，見「技術用字清單」。
- **DFD 第二輪的兩點意見**：
  1. 不提 RSDC 與 README：拿掉開頭的文件清單、「是 RSDC 標準的一部分」、Version 一段，以及 Shapes 的 stage 與 step 兩行；開頭改成一句話說明 DFD，範例前的說明改成 every DFD。
     原文 DFD.md 也得一起改，因為它連到 RSDC-Standard.md 的連結是 kept span，原文不拿掉，草稿就過不了 STE 檢查；改寫的那一句順便把 colour 改成 color。
     DFD.md 不再寫版本；RSDC-Standard.md 這一輪不改，它仍說 DFD.md 是標準的一部分、跟著標準的版本走。
  2. role 與 system 是技術用字，中文版維持原文：草稿中文版的「角色」「系統」都改回 role、system，「作業系統」照舊；兩份草稿的技術用字加上 role，之後拿掉，見「技術用字清單」。
     兩個詞也加進 tw-keep-english.md（版本 261013），它的中文版、STE 草稿與草稿的中文版跟著改；原文中文版 DFD-tw.md 照舊，之後由草稿的中文版取代。
- **DFD 通過**：第三輪審核通過；取代照原計畫，等決定待決定的五項、改好 asd-ste 之後，由它取代。
- **技術用字清單**：DFD 通過之後，role、input、system 從 DFD 兩份草稿的清單拿掉。
  role 由 ste-custom.md 核准，而 House Rule 11 規定 ste-custom 的字不列為技術用字；input 與 system 是字典本來就核准、意思也相符的字。
  其他草稿列的核准字——record、standard、agent、step、paste、noise、hit——是核准字用在字典沒給的技術意思（規則 1.3），留著。
  中文版的 role、system 照 tw-keep-english.md 維持英文。

### 進度

- DFD：2026-10-13 第三輪審核通過，同日由 Step 7 取代。
  `draft.py replace` 把草稿與它的中文版寫回 DFD.md 與 DFD-tw.md，檔頭註記刪成兩行，再刪掉兩份草稿；`check_ste.py --ste` PASS，parity check 0 failure，兩份 RSDC 範本的 `check_rsdc.py --standard` PASS。
  `draft.py dependents` 在本 workspace 與 InvestForge 找到記錄 DFD.md 的 14 份，讀過改動都仍成立，全部重記；InvestForge 的 4 份在 `1c3f9c3`，只提交檔頭那一行。
  task-31 表格與 task-23 指向草稿的連結改成行內程式碼，並註明已取代。
  取代時發現：README 那項測試把 DFD.md 的副本寫進 workspace，`[[DFD]]` 就指到兩份檔案，`depends_on.py` 拒絕記錄；測試改成寫到 workspace 以外。
  通過之後，兩份清單拿掉 role、input、system：DFD 重跑 Step 3 PASS，草稿與中文版的 `check_parity.py` 0 failure，對照頁重建。
  第一輪的對照頁是手做的；之後的由 asd-ste 的 Step 6 產生，在 `checkpoints/asd-ste/references-DFD/step_6-review.html`，註記列出該輪改的地方。
  拼法與標題改好之後，`check_ste.py` PASS，DFD 與草稿兩對中英對照的 `check_parity.py` 都是 0 failure，兩份 RSDC 範本的 `check_rsdc.py --standard` PASS。
  14 份依賴方重記之後，`depends_on.py check` 對 DFD 都是 UNCHANGED；InvestForge 的 4 份在 `7eee794`，只提交檔頭那一行，StopPriceChecker-RSDC 其餘的修改是別的 session 的。
  第一輪的四點改好之後，DFD 重跑 Step 3：`check_ste.py` PASS，草稿與它的中文版 `check_parity.py` 0 failure。
  ste-custom.md 加上 interact 之後，宣告 `[[ste-custom]]` 的另外 5 份草稿（tw-keep-english、md-style、report-md-rules、README-tmp、SKILL-tmp）重跑 Step 3 都 PASS，連同中文版重記。
  第二輪的兩點改好之後，DFD 與 tw-keep-english 重跑 Step 3 都 PASS，四對中英對照的 `check_parity.py` 都是 0 failure；14 份依賴方再重記一次，InvestForge 的 4 份在 `bbb9b36`，兩份 RSDC 範本的 `check_rsdc.py --standard` PASS。

### 審核紀錄

- 2.1 ✅ DFD——2026-10-13 第三輪通過。

## 3. 要做的

—

## 4. 驗證

—

## 5. 與其他 task 的關係

—

## 6. 日誌

### 2026-10-18

- 從 [[Task 32]] 拆出：原本是它要做的 2.1；屬於這份檔案的內容搬到這裡，內容沒有改。

### 2026-10-13

- DFD 第三輪審核通過，由 Step 7 取代原檔。

### 2026-10-12

- 列為 [[Task 32]] 要審核的草稿之一。
