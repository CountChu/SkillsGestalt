# Task 45 - 把文件的版本寫進 header quote，讓工具讀它

**Status**：完成——2026-10-16 建立，同日在建立它的 session 做完：版本寫在 header quote 的第一行，`depends_on.py`、`check_ste.py` 與 `check_rsdc.py` 都從那裡讀。
**Raised**：2026-10-16，[[Task 32]] 審 tw-keep-english 的草稿（2.3）時，使用者問「沒有工具讀這一行的版本」是什麼意思；聽完解釋之後決定把 Version 寫進 header 讓工具讀，RSDC-Standard 與所有寫著 `Version: yymmdd` 的 md 都照這樣做。
**Depends on**：—

## 1. 背景

版本號原本寫在正文：RSDC-Standard.md 的「**Version**: 261010.」、tw-keep-english.md 的「**Version**: 261013.」，中文版寫「**版本**：…」。
STE 草稿要改寫正文，所以 asd-ste 的 House Rule 7 讓草稿把版本行寫成長句，例如「**Version**: The version of tw-keep-english.md is 261013.」；只有工具要讀的版本行例外，例如 `check_rsdc.py --standard` 讀的 RSDC-Standard.md，版本號要緊接在「**Version**:」之後。
header quote 是標題下第一段 `>` 依賴行：草稿與中文版都照抄它，`depends_on.py` 算指紋時也不含它。
版本寫在那裡，就不必改寫、不必翻譯，工具也找得到。

## 2. 現況

### 已決定（2026-10-16）

- 寫法：header quote 的第一行寫 `> Version: yymmdd`，放在依賴行之前；沒有依賴的檔案，header quote 就只有這一行。
- 中文版照抄英文，也寫 `> Version: yymmdd`。
- 正文原本的 Version 行刪掉，其他說明照舊；tw-keep-english 原文第 7 行的 this line 指不到東西了，改成開頭的 Version 行。
- RSDC 範本也加上自己的 Version；第 12 行記的是範本依循的標準版本，照舊。
  範本本來沒有版本，從建立這一行的 261016 開始。
- 工具與 skill 一次改好，改 skill 之前先讀它的 README（沒有就讀 skill-writing.md），照它列的檢查跑。
- `depends_on.py` 把 Version 行當成 header quote 的一部分，但不是依賴；指紋照舊不含整個 header quote，所以只在 header 加上版本行的範本，指紋不變。
- tw-keep-english（[[Task 32]] 的 2.3）一起改：原文、草稿與兩份中文版；草稿不再需要 House Rule 7 的長句，對照頁重建。
- 提交：commit 前綴 `task 45`，兩個 repo 各自提交。

### 寫著版本號的檔案（2026-10-16 盤點）

- 自己的版本：RSDC-Standard.md 第 21 行、tw-keep-english.md 第 6 行、tw-keep-english-ste.md 第 16 行，以及三份的中文版。
- 範本記的標準版本：RSDC-App-tmp.md 與 RSDC-Skill-System-tmp.md 第 12 行，以及兩份的中文版，照舊。
- 規則的例子：ste-rules.md 的 House Rule 7。
- InvestForge 與 BookMaster 沒有。

### 結果（2026-10-16）

- `depends_on.py`：新增 `quote()`（整個 header quote，含 Version 行）、`version()`（讀出版本）；`header()` 只回傳依賴行，所以 check-md-deps、chinese、check-skill 透過它讀依賴的地方都不用改；指紋不含整個 header quote，Version 行也在內。
- `check_ste.py`：header quote 包含開頭的 Version 行，草稿要照抄；`draft.py` 用同一個函式，不必改。
- `check_rsdc.py --standard`：標準的版本從 header quote 讀；範本與中文版自己的版本也讀出來，各多一項檢查，兩份範本都是 8 項 PASS。
- 文件：RSDC-Standard 與中文版、tw-keep-english 與中文版、它的草稿與草稿的中文版，版本都移進 header quote；tw-keep-english 原文第 8 行改成「the Version line at the head of this file」，草稿拿掉長句；兩份範本與中文版加上 `> Version: 261016`。
- skill 文件：ste-rules.md 的 House Rule 5、7；asd-ste 與 check-md-deps 的 glossary（header quote、dependency）；gen-rsdc-app 的 Step 0 與 gen-rsdc-skill 的 Step 2 讀標準版本的那一句；四份 SKILL-tw.md 照 chinese skill 只改這幾行。
- 重記：記錄 RSDC-Standard 的 8 份（InvestForge 4 份）、記錄 `depends_on.py` 的 6 份 README、記錄 ste-rules.md 的 asd-ste SKILL.md 與中文版；範本只在 header quote 加了一行，指紋不變，記錄它們的 InvestForge RSDC 不必重記。
- [[Task 32]] 的 2.3：草稿重跑 Step 3 PASS；對照頁的行號自動對到新位置，版本那幾項改寫成第三輪的結果；header 多了一行，幾乎每一項的行號都移動，所以全部回到待審。

### 讀 header quote 或版本號的工具

- `depends_on.py`：找 header quote、記錄與檢查指紋；check-md-deps 的 `scan_md_deps.py`、chinese 的 `scan_md.py`、check-skill 的 `scan_skill.py` 都透過它讀 header quote。
- `check_ste.py` 與 `draft.py`：各自找 header quote，檢查草稿照抄原文的 header quote。
- `check_rsdc.py --standard`：讀 RSDC-Standard 的版本，和範本第 12 行記的版本比對。

## 3. 要做的

1. 工具：
   - `depends_on.py`：header quote 可以用 `> Version: yymmdd` 開頭；依賴只讀它後面的行；指紋不含整個 header quote；提供讀出版本的函式；docstring 跟著改。
   - `check_ste.py`：header quote 包含 Version 行，草稿要照抄；`draft.py` 用它的函式。
   - `check_rsdc.py`：標準的版本從 header quote 讀；範本自己的版本也讀出來並列出。
2. 文件：
   - RSDC-Standard.md 與中文版：版本行搬進 header quote。
   - tw-keep-english.md、它的草稿，以及兩份中文版：版本行搬進 header quote；原文第 7 行改成開頭的 Version 行，草稿拿掉長句。
   - 兩份 RSDC 範本與中文版：header quote 的第一行加上 `> Version: 261016`。
3. skill 的文件：asd-ste 的 ste-rules.md（House Rule 5、7）、SKILL.md、README.md 與中文版；gen-rsdc-app 與 gen-rsdc-skill 讀標準版本的那一步與中文版；check-md-deps 說明 header quote 的地方與中文版。
4. 重記：RSDC-Standard 的正文變了，記錄它的 8 份讀過改動後重記；改了的 skill 文件與腳本，記錄它們的文件也一樣。
5. [[Task 32]] 的 2.3：對照頁的說明跟著改，重建。

## 4. 驗證

- asd-ste 的 README 在 When the Skill Is Changed 列出的檢查。
- 兩份 RSDC 範本的 `check_rsdc.py --standard` PASS。
- RSDC-Standard 的 `check_ste.py --ste` PASS，tw-keep-english 的草稿重跑 Step 3 PASS。
- 改到的每一對中英對照：`check_parity.py` 0 failure，`diff_md.py --verify` PASS。
- check-md-deps 的 `scan_md_deps.py` 對改到的檔案沒有 malformed 或 misplaced。
- 重記的文件 `depends_on.py check` 都是 UNCHANGED。

## 5. 與其他 task 的關係

- [[Task 32]]：審 2.3 時提出；tw-keep-english 的草稿一起改，2.3 的對照頁跟著重建。

## 6. 日誌

### 2026-10-16

- 建立：決定版本寫在 header quote 的第一行，中文版照抄，範本也加上自己的版本，工具與 skill 一次改好。
- 做完：三支工具、五對文件、四個 skill 的文件都改好，重記 16 份。
  檢查：RSDC-Standard 的 `check_ste.py --ste` PASS，警告和之前相同；tw-keep-english 的 Step 3 PASS；兩份範本的 `check_rsdc.py --standard` PASS，InvCov 與 StopPriceChecker 的 `--rsdc` 也 PASS。
  asd-ste 的 README 列出的檢查：`1710643` 與 `ed0076e` 兩組 DFD 的 `check_ste.py` 結果都和 README 說的一樣，DFD.md 的 `--ste` PASS，`draft.py` 的 paths、replace（另外在有 Version 行的 tw-keep-english 副本上也跑過，Version 行留在 header quote）、dependents 都正常；完整跑一次 Step 0 到 6、`make_review.py` 與 `review_server.js` 的測試沒有跑，因為這次沒改它們。
  九對中英對照 `check_parity.py` 0 failure，警告和改之前相同，`diff_md.py --verify` 都 PASS；`depends_on.py check` 都是 UNCHANGED；`scan_md_deps.py` 沒有 malformed 或 misplaced；check-skill 掃 asd-ste，header quote 都是 UNCHANGED。
