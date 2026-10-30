# Task 50 - 讓 ste-custom.md 分成 Words 與 Rules，加上第一條專案規則：不用雙重否定

**Status**：完成——2026-10-17 做完 Words 與 Rules 與雙重否定的 `[WARN]`；2026-10-18 重新打開並做完：每份 STE 檔都宣告 `[[ste-custom]]`，沒宣告是 `[FAIL]`，改了 Rules 時 `depends_on.py check` 會報出每一份。
**Raised**：2026-10-17，[[Task 32]] 審 tw-keep-english 的草稿（2.3）時，使用者問 STE 有沒有禁止雙重否定；查過 Issue 9 的寫作規則沒有這一條，使用者決定在 ste-custom.md 加上 Rules 一章，放本專案自己加的規則。
**Depends on**：—

## 1. 背景

ste-custom.md 原本只有專案核准詞的表格，標題是 Project-Approved Words（[[Task 43]] 取的名稱）。
ASD-STE100 Issue 9 的 Part 1 共 9 節寫作規則，沒有一條提到雙重否定；唯一提到否定的是第 7 節的說明，要求安全指示寫出 DO NOT。
asd-ste 的 [ste-rules.md](../.github/common/skills/asd-ste/references/ste-rules.md) 有 11 條 House Rules，是 skill 自己的寫法約定；使用者為本專案決定的規則，從此放在 ste-custom.md。

## 2. 現況

### 已決定（2026-10-17）

- ste-custom.md 分成兩章：`## Words`（原本的表格與說明）與 `## Rules`；標題改成 Project-Approved Words and Rules。
- Rules 也是表格，一列一條：Rule、Example、Checked（`check_ste.py` 會不會檢查）、Why（哪天、使用者為什麼決定）。
- 分工：House Rules 仍是 skill 自己的寫法約定；使用者為本專案加的規則放 ste-custom 的 Rules；House Rule 11 改寫成同時涵蓋字與規則。
- 第一條規則：「Do not use two negatives to give a positive meaning: write the positive statement.」，例子是「do not write a command incorrectly」改成肯定句；`check_ste.py` 找 not、no、without 等否定詞後面接 un-、in-、dis- 等字首的字，報 `[WARN]`，由人判斷，和被動語態的警告一樣。
- tools 的草稿第 24 行「do not write a command incorrectly」一起改成肯定句，中文版跟著改。
- 中文版不加對應的規則：ste-custom 只管 STE 英文，中文版的翻譯規則屬於 chinese skill。
- asd-ste 的 glossary 加上 project rules 的定義；SKILL.md、README.md 與兩者的中文版提到 ste-custom 的地方跟著改。
- 提交：commit 前綴 `task 50`；ste-custom.md 的指紋會變，宣告它的 20 份一起重查、重記；InvestForge 沒有文件記錄它，不受影響。

### 結果（2026-10-17）

- ste-custom.md 與中文版：`## Words` 放原本的說明與 19 個詞，`## Rules` 放說明與第一條規則；新指紋 `8025b634914c`，`check_ste.py` 讀到的詞仍是 19 個。
- `check_ste.py`：在 not、no、never、none、nothing、without、cannot 之後，同一個子句四個字以內，找由 non-、dis-、un-、in-、im-、il-、ir- 加上核准詞構成的詞，報 `[WARN] double negative?`；unless、input、display 這類開頭像字首、其實不是否定的詞不算。
  不加 `--custom` 也會檢查；Step 1 的 inventory 把它列成 `[TODO]`，findings 多了 `double_negatives`。
  兩個否定詞連用（例如 not … nothing）不在檢查範圍，由審核的人看。
- 8 份草稿與 3 份 STE 檔中，只有 tools 草稿第 24 行「do not write a command incorrectly」被報出；改成「you write each command correctly the first time」之後，8 份草稿的 Step 3 都 PASS，報告和改之前相同。
  DFD、RSDC-Standard、md-style 的 `check_ste.py --ste` PASS，結果和改之前相同。
- ste-rules.md 的開頭與 House Rule 11 改成涵蓋詞與規則；asd-ste 的 SKILL.md 加上 project rules 的 glossary 與 CONFIGURATION，Step 1、2、3 提到雙重否定；README.md 的 Dataflow 節點、圖說與兩張依賴圖跟著改；兩份中文版照 chinese skill 跟著改。
- 重記：宣告 `[[ste-custom]]` 的 20 份，以及 asd-ste 的 SKILL.md 與中文版記錄的 ste-rules.md（`1e0287c3fc4b`）；report-yaml-rules 的草稿沒有宣告 ste-custom，也重跑了 Step 3，沒有新的警告。
- asd-ste 的 README 列出的檢查：`1710643` 的 DFD 兩項都 PASS；`ed0076e` 的 DFD 檢查仍因 Catalogue 失敗，inventory 仍以 `3` 結束（SOURCE-FIRST，問 Kinds）；check-skill 的 `scan_skill.py` 沒有沒用到的 glossary term。
  `draft.py`、`make_review.py`、`review_server.js` 沒有改，沒有跑它們的檢查。
- 2.3 的對照頁重建：共 29 項、151 個行號，26 項維持通過，3 項是第八輪改過說明、待審的。

### 發現的問題（2026-10-17）

- Rules 適用於每一份 STE 檔，但只有用到專案核准詞的檔案才宣告 `[[ste-custom]]`：report-yaml-rules 的草稿沒有宣告，之後改了 Rules，`depends_on.py check` 不會把它報為 CHANGED。
- 要不要讓每一份 STE 檔都宣告 `[[ste-custom]]`（House Rule 5、11 與 `check_ste.py`「宣告了卻沒用到」的警告要跟著改），等使用者決定。
- 2026-10-18 使用者決定每一份都宣告，不另開 task，由本 task 重新打開處理，見「已決定（2026-10-18）」。

### 已決定（2026-10-18）

- 每份草稿，以及每份由草稿取代的 STE 檔，都在 header quote 宣告 `[[ste-custom]]`，不論內文有沒有用到專案核准詞：Rules 每一份都要遵守，Words 用到才用。
- `check_ste.py` 給了 `--custom` 時，header quote 沒宣告 `[[ste-custom]]` 一律 `[FAIL]`，和沒宣告 STE 規格一樣；「宣告了卻沒用到任何詞」的 `[WARN]` 拿掉。
- ste-custom.md 與中文版：宣告的那一條從 Words 移到開頭的說明，改成每份 STE 檔都宣告本檔；Rules 的「改表格會改指紋」那一條併進去。
  指紋會變，所以 8 份草稿重跑 Step 3、3 份 STE 檔跑 `check_ste.py --ste`，連同中文版重記。
- ste-rules.md 的 House Rule 5 與 11、asd-ste 的 SKILL.md 與 README.md（含中文版）提到宣告的地方跟著改。
- `draft.py` 不改：它不讀也不寫 `[[ste-custom]]`，而 Step 3 與 Step 7 的 `check_ste.py` 會擋下沒宣告的檔。
  Step 3 一律跑兩次 `depends_on.py record`（STE 規格與 `[[ste-custom]]`），`step_3` 一律存 `custom_fingerprint`。
- report-yaml-rules 的草稿與中文版加上 `> [[ste-custom]]`；草稿第 4 行以後的行號都加 1，所以它的對照頁在本 task 重建：註記的草稿行號跟著移，兩項「檔頭」改寫，再跑 Step 6。
- [[Task 32]] 的 report-yaml-rules 進度補一句，並記日誌；只提交本 task 改的 hunk。

### 結果（2026-10-18）

- ste-rules.md：House Rule 5 一律寫 `> [[ste-custom]]`；House Rule 11 改成每份 STE 檔都宣告，沒用到詞的也一樣，改了任一張表格就會報出每一份。
  asd-ste 的 SKILL.md 與中文版重記 ste-rules.md，新指紋 `126a02a67fdc`。
- ste-custom.md 與中文版：開頭多兩句，說每份 STE 檔都宣告本檔，本檔一改就要重查；Words 的宣告那一條與 Rules 的指紋那一條拿掉。
  新指紋 `182b88428cdd`，`check_ste.py` 讀到的詞仍是 19 個。
- `check_ste.py`：給了 `--custom` 時一律檢查宣告，那一行的說明改成「declares [[ste-custom]], the project-approved words and rules」，沒宣告就 `[FAIL]`，並寫明連沒用到詞的檔也要宣告；「宣告了卻沒用到」的 `[WARN]` 拿掉，docstring 跟著改。
  改好、還沒補宣告之前，report-yaml-rules 的草稿就報出這個 `[FAIL]`。
- SKILL.md 與中文版：header quote 的定義、Step 2 的 Header quote、Step 3 的第 7 項檢查與 record 指令都改成一律宣告、一律記錄；`step_3` 一律存 `custom_fingerprint`，範例也加上它。
- README.md 與中文版：Dataflow 的圖說、Files Each Step Uses 的 Step 3、When the Skill Is Changed 的 ste-custom.md 一節與 Tracked Dependencies 跟著改；fenced block 中英兩份逐位元組相同。
- report-yaml-rules 的草稿與中文版第 4 行加上 `> [[ste-custom]]`。
  8 份草稿重跑 Step 3 都 PASS，報告和改之前比只差那一行的說明，report-yaml-rules 多了那一行的 PASS，留下的警告仍只有 tw-keep-english 的 op；8 份的 `step_3` 都存了 `custom_fingerprint`。
  DFD、RSDC-Standard、md-style 的 `check_ste.py --ste` PASS，和 HEAD 的腳本比只差那一行的說明。
- 重記：22 份 `[[ste-custom]]`；20 份連同 SKILL.md、README.md 與兩者的中文版，`depends_on.py check` 的 60 項都是 UNCHANGED；README-tmp 的兩份檔頭有 `{COMMON_PATH}`，`depends_on.py hash` 算出的指紋和記錄的相同。
- 中英對照：ste-custom、SKILL、README、report-yaml-rules 草稿四對 `check_parity.py` 0 failure，`diff_md.py --verify` PASS；SKILL 的 3 則、README 的 2 則 WARN 在 HEAD 就有。
  11 對 STE 檔都是 0 failure。
- report-yaml-rules 的對照頁：註記 22 個草稿行號中，20 個移過之後指到的內容和改之前相同，另外 2 個是兩項「檔頭」，範圍包進新的宣告行；Step 6 重建，仍是 14 項、41 個行號，都待審，`step_6` 已存。
- asd-ste 的 README 列出的檢查：`1710643` 的 DFD 兩項都 PASS；`ed0076e` 的 DFD 檢查仍因 Catalogue 失敗，inventory 仍以 `3` 結束（SOURCE-FIRST，問 Kinds）；check-skill 的 `scan_skill.py`（借 InvestForge 的 `config.yaml`）沒有沒用到的 glossary term，Dataflow 沒有漏畫的 step 或多個寫入者的 record。
  `draft.py`、`save_step.py`、`make_review.py`、`review_server.js` 沒有改，沒有跑它們的檢查與 `test` 目錄的那次執行。

## 3. 要做的

1. ste-custom.md 與中文版分成 Words 與 Rules，加上第一條規則。
2. `check_ste.py` 加上雙重否定的 `[WARN]`，docstring、報告與 findings 跟著改。
3. ste-rules.md 的開頭與 House Rule 11、asd-ste 的 SKILL.md 與 README.md（含中文版）提到 ste-custom 的地方。
4. tools 草稿第 24 行與中文版改成肯定句。
5. 7 份草稿重跑 Step 3，3 份 STE 檔跑 `check_ste.py --ste`，新的警告逐一判斷；20 份重記 `[[ste-custom]]`，asd-ste 的 SKILL.md 與中文版重記 ste-rules.md。
6. 跑 asd-ste 的 README 列出的檢查；2.3 的對照頁重建。

2026-10-18 重新打開之後：

7. ste-rules.md 的 House Rule 5 與 11、ste-custom.md 與中文版的開頭、asd-ste 的 SKILL.md 與 README.md（含中文版）提到宣告的地方，改成每份 STE 檔都宣告 `[[ste-custom]]`。
8. `check_ste.py`：給了 `--custom` 而沒宣告就 `[FAIL]`，拿掉「宣告了卻沒用到」的 `[WARN]`，docstring 跟著改。
9. report-yaml-rules 的草稿與中文版加上 `> [[ste-custom]]`。
10. 8 份草稿重跑 Step 3，3 份 STE 檔跑 `check_ste.py --ste`；22 份重記 `[[ste-custom]]`，asd-ste 的 SKILL.md 與中文版重記 ste-rules.md。
11. report-yaml-rules 的對照頁：註記的草稿行號跟著移，兩項「檔頭」改寫，重跑 Step 6。
12. [[Task 32]] 的 report-yaml-rules 進度補一句；跑 asd-ste 的 README 列出的檢查。

## 4. 驗證

- ste-custom、SKILL、README、tools 草稿的中英對照：`check_parity.py` 0 failure，`diff_md.py --verify` PASS。
- `check_ste.py` 在 tools 草稿原本的第 24 行報出雙重否定，改好之後不再報；其他檔案新出現的警告都讀過、處理或說明。
- 重記的文件 `depends_on.py check` 都是 UNCHANGED。
- 2026-10-18：`check_ste.py` 對沒宣告 `[[ste-custom]]` 的檔報 `[FAIL]`，對宣告了而沒用到任何詞的檔不再報 `[WARN]`；report-yaml-rules 的草稿 Step 3 PASS，對照頁的每個行號都對到原本的那一行。

## 5. 與其他 task 的關係

- [[Task 32]]：審 2.3 時提出；2026-10-18 重新打開時，report-yaml-rules（2.6）的草稿加上宣告，對照頁重建。
- [[Task 43]]：把 STE customization 改稱 project-approved words，本 task 再加上 rules。
- [[Task 49]]：把 false 與 false alarm 收進專案核准詞，草稿第 148 行因此改回 without false alarms，不再是雙重否定。

## 6. 日誌

### 2026-10-18

- 重新打開：使用者決定每份 STE 檔都宣告 `[[ste-custom]]`，沒宣告是 `[FAIL]`，「宣告了卻沒用到」的 `[WARN]` 拿掉；不另開 task。
- 做完：report-yaml-rules 的草稿與中文版補上宣告，8 份草稿 Step 3 都 PASS，22 份重記，對照頁重建；四對中英對照 `check_parity.py` 0 failure，`diff_md.py --verify` 都 PASS。

### 2026-10-17

- 建立：決定 ste-custom.md 分成 Words 與 Rules，第一條規則是不用雙重否定，由 `check_ste.py` 報警告。
- 做完：ste-custom、SKILL、README、tools 草稿四對中英對照 `check_parity.py` 0 failure、警告和改之前相同，`diff_md.py --verify` 都 PASS；重記的 22 份 `depends_on.py check` 都是 UNCHANGED。
  記下一個待決定的問題：沒有宣告 `[[ste-custom]]` 的 STE 檔，改 Rules 時不會被報出。
