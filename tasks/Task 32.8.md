# Task 32.8 - skill-writing

**Status**：完成——2026-10-18 第三輪審核 27 項全部通過，同日由 Step 7 取代原檔與它的中文版。
**Raised**：2026-10-12，[[Task 32]] 提出時列出的草稿之一，原本是它要做的 2.8。
**Depends on**：—

## 1. 背景

審核 [[Task 31]] 為 [skill-writing.md](../.github/common/rules/skill-writing.md) 產生的 STE 草稿與草稿中文版；通過就由 asd-ste 的 Step 7 取代原檔與它的中文版。
分工、取代的方式與「每取代一份要一併做的」，見 [[Task 32]]。

## 2. 現況

### 審核時決定的

- **送審前的準備**（2026-10-18）：重跑 Step 1，存下標題詞的判定：清冊沒有問任何字；Skill 是技術用字，Writing 是文件名稱裡的字，Rules 是專案核准詞（[[Task 44]]）。
- **先改兩處 depend**（2026-10-18）：草稿寫在 depend 收進 ste-custom.md（2026-10-13）之前，繞開了 depend，意思跑掉；使用者決定送審前先改。
  第 24 行改成「It also tells which files change together, and which files the skill depends on.」，中文版寫「以及 skill 依賴哪些檔案」。
  第 34 行改成「A step does not depend on a step that comes after it.」，中文版寫「一個 step 不依賴排在它之後的 step。」。
- **補上 glossary 的定義**（2026-10-18）：使用者問 glossary 與 term 有沒有定義；term 在 chinese skill 與 tw-keep-english 都有，glossary 沒有，skill-writing 也沒指出是哪兩節。
  使用者決定不改用 terminology（意思是「一套術語」，而且 chinese 的 glossary term 會變得彆扭），改在 skill-writing 補一句定義，原文與草稿都改。
  原文第 16 行：「The glossary is the two sections `# TERMINOLOGY` and `# DEDICATED TERMINOLOGY`: the terms that mean the same thing in every skill, then the terms of the skill's own domain.」
  草稿第 29–30 行寫成兩句：meaning、second 不在字典，first 只核准副詞，所以直接點名兩節，「意義相同」寫成 identify the same item，和 tw-keep-english 對 term 的 STE 定義一致。
  這一條因此有 7 句，超過一段 6 句的上限，使用者決定在定義後面空一行，分成兩段。
  兩份中文版都寫 glossary；原文中文版另外三處「術語表」也一併改成 glossary。
- **其他只列進審核重點**：第 19、26 行的 so that 變成 thus、第 44–45 行的 lose 變成 problem、Technical words 裡字典不核准的 program（[[Task 41]]），以及中文版的 glossary 與 script 和原文中文版的譯法不同。
- **第二輪的兩項 `[?]`**（2026-10-18）：使用者在對照頁上把英文第 5 點的 Purpose 與 program 兩項標成 `[?]`，看過說明之後決定：
  - 第 48 行改成「That is, it tells how the skill becomes worse if you put the step and an adjacent step together.」，中文版寫「skill 會怎樣變差」。
    lose 字典不核准，「變差」同時包含出錯與少了某種能力，比 problem 接近原文的 lose；每個字都在字典裡，worse 是 bad 的比較級。
  - program 收進 ste-custom.md，只核准名詞，意思是「a set of instructions that a computer runs, as a script or `check_ste.py`」：字典的替代字 SEQUENCE 是 step 的順序，不是電腦執行的指令。
    RSDC-Standard 第 359 行的 programming 一起收進，意思是「the work of writing a program, as in "the programming style"」。
  - 在本 task 裡做，不另開 task：三份 STE 檔的 Technical words 拿掉 program，RSDC-Standard 再拿掉 programming，各自的中文版同步；RSDC-Standard 只改文字，版本維持 261016，和 [[Task 47]] 一樣。
  - 記錄 RSDC-Standard.md 的 8 份讀過都仍成立、重記；InvestForge 的 StopPriceChecker-RSDC 兩份有別的 session 還沒提交的改動，只提交檔頭紀錄那一行。
  - 其他 20 份的 ste-custom 紀錄等本草稿取代、當天不再改 ste-custom.md 之後，由 [[rerecord-ste-custom]] 集中重記。
  - 提交：本 workspace 與 InvestForge 各一個 commit，前綴 `task 32.8`。
- **刪掉兩處重複**（2026-10-18）：使用者問草稿中文版第 19、26 行是否重複，再要找出其他重複的規則。
  找到三處，都是原文本來就重複：「SKILL.md 不連到 README，所以執行不會讀它」（原文第 9、13 行）、「README 說明哪些檔案要一起改」（原文第 9、12 行）、「Purpose 寫在 README、不寫在 SKILL.md，因為執行用不到」（原文第 12、29 行）。
  使用者決定刪掉第一與第三處，原文與草稿都改：原文第 9 行刪掉分號後半句，第 29 行只留「Each Purpose is given in the Step Purposes section of the `README.md`.」，草稿與中文版刪掉對應的兩句。
  第二處保留：它是第一條要先讀 README 的理由，第二條的清單也要完整。
  6 份 README 讀過改動之後重記；本 workspace 一個 commit，前綴 `task 32.8`。
- **deterministic 收進 ste-custom**（2026-10-18，第三輪）：使用者問 deterministic 是不是 STE 允許的字，再問中文版能不能保留它。
  字典沒有收錄這個詞，形容詞與副詞也不能當技術用字；中文版跟著英文檔，英文沒有的字，中文版不能自己加。
  使用者決定把 deterministic（adj）與 deterministically（adv）收進 ste-custom.md，意思是「that always gives the same output for the same input, as a step that a script can do」。
  草稿第 39 行照原文的句型改成「If a program can do a step deterministically, the step operates a script.」，中文版寫「如果程式能以 deterministic 方式做某個 step」，和原文中文版一致。
  tw-keep-english 的 Technical words 拿掉 deterministic，中文版同步，版本維持 261018；其他 20 份的 ste-custom 紀錄照舊等取代之後由 [[rerecord-ste-custom]] 重記；一個 commit，前綴 `task 32.8`。

### 進度

- skill-writing：2026-10-18 以 Step 6 產生對照頁送審，連結是 `http://127.0.0.1:8790/rules-skill-writing/`。
  Step 3 原本已是最新：[[rerecord-ste-custom]] 當天重記過，ste-custom 指紋 `3c5050b6a240`；兩處改好之後重跑 PASS，沒有警告，多了 depend 的 `[INFO]`；`[[ASD-STE100_ISSUE9.pdf]]` 與 `[[ste-custom]]` 重記，指紋不變。
  草稿中文版照 chinese skill 只改 change set 的 2 行，`check_parity.py` 0 failure，`diff_md.py --verify` PASS。
  審核重點英文 5 項、中文 4 項，共 16 個審核狀態、61 個行號：檔頭、標題用字、送審前已改的兩處、三處句意、結構與中文版的譯法。
  補上 glossary 的定義之後（同日）：Step 3 先因一段 7 句 FAIL，空一行之後 PASS，沒有警告；兩對中英對照 `check_parity.py` 0 failure，草稿那一對 `diff_md.py --verify` PASS，原文那一對報原文中文版第 17、18 行在英文改動範圍之外，是刻意把「術語表」改成 glossary。
  原文改了，記錄 skill-writing.md 的 6 份（asd-ste、check-skill、gen-skill 的 README 與中文版）讀過改動都仍成立，重記（新指紋 `5f631cd75849`），`depends_on.py check` 都是 UNCHANGED。
  註記的行號自動對到新位置，加上英文與中文各一項說明新增的定義，中文「譯法」一項只剩 script；對照頁重建，共 11 項、21 個審核狀態、64 個行號。
  第二輪（2026-10-18）：ste-custom.md 與中文版加上 program、programming 兩列（新指紋 `b2a3ef3766e0`）；中文版照 chinese skill 只改 change set，「步驟」照 keep-English list 改成 step 之後，`check_parity.py` 0 failure、0 warning，`diff_md.py --verify` PASS。
  Technical words：RSDC-Standard 由 124 個減為 122 個，tw-keep-english 由 125 個減為 124 個，草稿由 18 個減為 17 個，三份中文版同步；三對中英對照 `check_parity.py` 0 failure、警告和之前相同，`diff_md.py --verify` 都 PASS。
  RSDC-Standard 與 tw-keep-english 的 `check_ste.py --ste` PASS，只多了 program（RSDC-Standard 另有 programming）的 `[INFO]`。
  草稿第 48 行改寫，中文版照 chinese skill 只改 change set 的 2 行；Step 3 重跑 PASS，沒有警告，多了 program 的 `[INFO]`；草稿與中文版重記 `[[ASD-STE100_ISSUE9.pdf]]`（指紋不變）與 `[[ste-custom]]`。
  記錄 RSDC-Standard.md 的 8 份重記（新指紋 `150b54d00af5`）：本 workspace 的兩份 RSDC 範本與中文版、InvestForge 的 StopPriceChecker-RSDC 與 InvCov-RSDC 與中文版；`depends_on.py check` 都是 UNCHANGED，兩份範本的 `check_rsdc.py --standard` 都是 8 項 PASS。
  asd-ste 的 SKILL.md、README.md 與中文版 `depends_on.py check` 都是 UNCHANGED，check-skill 的 `scan_skill.py` 只多了 ste-custom 兩份的行數。
  註記改寫英文的檔頭、第 47–48 行與第 8 行三項，以及中文第 48 行一項，各自註明第二輪已改；對照頁重建，共 11 項、21 個審核狀態、66 個行號，12 項通過、9 項待審。
  刪掉兩處重複之後（同日）：原文與中文版照 chinese skill 只改 change set 的 2 行，`check_parity.py` 0 failure、警告和之前相同，`diff_md.py --verify` PASS；草稿與中文版各刪 2 行，剩 50 行，`check_parity.py` 0 failure，`diff_md.py --verify` PASS。
  Step 3 重跑 PASS，沒有警告，句子由 39 句減為 37 句；`[[ASD-STE100_ISSUE9.pdf]]` 與 `[[ste-custom]]` 重記，指紋不變。
  原文改了，記錄 skill-writing.md 的 6 份 README 讀過都仍成立，重記（新指紋 `38f780d5dd4d`），`depends_on.py check` 都是 UNCHANGED。
  註記英文與中文各加一點說明刪掉的重複，thus 那一項只剩第 25 行，結構那一項拿掉原文第 9、29 行，其他行號往前移；對照頁重建，共 13 項、25 個審核狀態、68 個行號。
  審核狀態依項目文字認，所以行號移動的已通過項目也變回待審：重建前 15 項通過（使用者已通過第二輪改的三項），重建後 4 項通過、21 項待審。
  使用者再審之後，24 項通過；中文第 5 點（script 的譯法）標 `[?]`，已在對話中說明草稿中文版照 keep-English list 寫 script，審核重點不改。
  第三輪（同日）：ste-custom.md 與中文版加上 deterministic、deterministically 兩列（新指紋 `798347d46d28`）；中文版照 chinese skill 只改 change set，`check_parity.py` 0 failure、0 warning，`diff_md.py --verify` PASS。
  tw-keep-english 的 Technical words 由 124 個減為 123 個，中文版同步；`check_parity.py` 警告和之前相同，`diff_md.py --verify` PASS，`check_ste.py --ste` PASS，只多了 deterministic 的 `[INFO]`。
  草稿第 39 行改寫，中文版照 chinese skill 只改 change set 的 1 行；Step 3 重跑 PASS，沒有警告，多了 deterministically 的 `[INFO]`；草稿與中文版重記 `[[ste-custom]]`。
  asd-ste 的 SKILL.md、README.md 與中文版 `depends_on.py check` 都是 UNCHANGED，check-skill 的 `scan_skill.py` 只多了 ste-custom 兩份的行數。
  審核重點的英文第 6 點與中文第 4 點各加一個子項說明第 39 行；對照頁重建，共 13 項、27 個審核狀態、72 個行號，24 項通過、1 項待解釋、2 項待審。
- 取代（2026-10-18）：第三輪 27 項全部通過；Step 3 記下的 ste-custom 指紋仍是現在的 `798347d46d28`，所以 Step 7 不必先重跑 Step 3 與 Step 6。
  `draft.py replace` 把草稿與它的中文版寫回 skill-writing.md 與 skill-writing-tw.md，檔頭註記刪成兩行，再刪掉兩份草稿；兩份都是 49 行。
  `draft.py dependents` 以本 workspace、InvestForge 與 BookMaster 為 root，找到 asd-ste、check-skill、gen-skill 的 README 與中文版 6 份。
  它們引用的是 step 怎麼寫、scripted-versus-not 那條規則與 check-skill 的準則 1.4、1.7、1.10–1.14，STE 版的規則相同，讀過都仍成立，重記（新指紋 `dc4fdbb634cb`）。
  檢查：`check_ste.py --ste` PASS，沒有警告；parity check 0 failure、0 warning，原文中文版「腳本」的那則警告也沒有了；6 份 README 的 `depends_on.py check` 都是 UNCHANGED。
  [[Task 31]] 表格裡指向兩份草稿的連結改成行內程式碼，並註明已取代。
  另外 20 份的 ste-custom 紀錄仍是舊的：使用者說今天可能還會改 ste-custom.md，[[rerecord-ste-custom]] 等當天最後一次修改之後再跑。

## 3. 要做的

—

## 4. 驗證

—

## 5. 與其他 task 的關係

- [[Task 44]]：標題的 Rules 收進專案核准詞。
- [[Task 41]]：Technical words 裡的 program 字典不核准，`check_ste.py` 不提醒；第二輪改由 ste-custom.md 核准，Task 41 的清單拿掉它。
- [[Task 47]]：把 phrase 收進專案核准詞的做法，program 與 programming 照著做。
- [[Task 61]]：審本草稿時刪掉兩處重複之後提出，檢查所有定規則的 md 之間重複的規則；skill-writing 取代原檔之後，也在它的範圍內。
- [[rerecord-ste-custom]]：ste-custom.md 有改動的日子集中重記一次，本草稿與它的中文版也在其中。

## 6. 知識

—

## 7. 日誌

### 2026-10-30

- [[Task 86]] 把 chore 改用名稱：本檔的 `[[Chore N]]` 連結改成新名稱。

### 2026-10-18

- 從 [[Task 32]] 拆出：原本是它要做的 2.8；屬於這份檔案的內容搬到這裡，內容沒有改。
- 送審：重跑 Step 1，先改兩處 depend，Step 3 PASS，對照頁 16 項送審。
- 補上 glossary 的定義：原文與草稿各加一句（草稿兩句、另起一段），兩份中文版都寫 glossary；6 份 README 重記，對照頁重建為 21 項。
- 第二輪：兩項 `[?]` 照使用者的決定處理——第 48 行改寫，program 與 programming 收進 ste-custom.md，三份 STE 檔的 Technical words 拿掉它們，記錄 RSDC-Standard 的 8 份重記；Step 3 PASS，對照頁重建，9 項待審。
- 刪掉兩處重複：原文第 9、29 行各刪半句，草稿與中文版各刪 2 行；6 份 README 重記，Step 3 PASS，對照頁重建，21 項待審。
- 第三輪：deterministic 與 deterministically 收進 ste-custom.md，草稿第 39 行照原文的句型改寫，tw-keep-english 拿掉這個技術用字；Step 3 PASS，對照頁重建，2 項待審。
- 第三輪審核 27 項全部通過，由 Step 7 取代原檔與它的中文版；6 份 README 重記，[[Task 31]] 表格的草稿連結改成行內程式碼。

### 2026-10-12

- 列為 [[Task 32]] 要審核的草稿之一。
