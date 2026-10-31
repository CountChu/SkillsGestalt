# Task 43 - 把 technical term 改稱 term（術語），STE customization 改稱 project-approved word（專案核准詞）

**Status**：完成——2026-10-14 建立，同日在建立它的 session 做完。
**Raised**：2026-10-14，[[Task 32]] 審 tw-keep-english 的草稿（2.3）時，使用者問 tw-keep-english 的「技術詞」和 STE 的「技術用字」有什麼不同：兩個名稱太像，容易混淆。
**Depends on**：—

## 1. 背景

背景：這幾個名稱分屬兩個面向。
英文 STE 檔能用哪些字：**technical word**（技術用字，STE 規則 1.5、1.12 的技術名詞與技術動詞，見 asd-ste 的 House Rule 6），以及 **STE customization**（[ste-custom.md](../.github/common/skills/asd-ste/references/ste-custom.md)，本專案在 Issue 9 之外核准的字，見 House Rule 11）。
中文版要不要保留英文：[tw-keep-english.md](../.github/common/references/tw-keep-english.md) 規則裡的 **technical term**（它的中文版寫「技術詞」，chinese skill 的中文版寫「技術術語」），以及判定要保留英文、列進表格的 **keep-English list**。
technical term 和 technical word 只差一個字，中文的「技術詞」和「技術用字」也是；customization 則看不出它其實就是核准字，只是由本專案核准，所以不算技術用字。

## 2. 現況

**已決定（2026-10-14）**

- **改兩個名稱**：
  - technical term 改稱 **term**，中文「術語」：清單的標題 Terms Kept in English 與表格的 Term 欄本來就這樣叫，文件在自己 glossary 定義的詞也叫 term；「術語」也是本 workspace 中文版裡 term 的慣用譯法。
  - STE customization 改稱 **project-approved word**，中文「專案核准詞」：和字典的 approved word（中文版譯作「核准詞」）並列；ste-custom.md 的標題改成 Project-Approved Words。
    建立時寫的是「專案核准字」，同日更正：中文版把 approved word 譯成「核准詞」，「核准字」只是 task 檔的寫法。
- **不改的**：technical word／技術用字，它對應 STE 規則 1.5、1.12，`Technical words:` 那一行有 `check_ste.py` 與 `make_review.py` 在讀；keep-English list，chinese skill 的 glossary 已經這樣定義。
  ste-custom 只改標題與正文裡的稱呼：檔名 ste-custom.md、`[[ste-custom]]` 連結，以及腳本的選項與 JSON 鍵都照舊。
- **範圍**：現行文件都不再寫 technical term，包括 write-topic 與 write-note 的 SKILL.md；task 檔、checkpoints 這些紀錄保留當時的寫法，不改。
- **時機**：現在就做，不等 Task 32；tw-keep-english 的原文與草稿一起改，2.3 的對照頁重建。
- **動手前再決定的（同日）**：
  - asd-ste 裡，整份清單叫 project-approved words，其中一個字叫 a project-approved word；要指檔案時直接寫 ste-custom.md。
  - tw-keep-english 只改措辭、清單沒變，版本維持 261013。
  - 不能只刪 technical 的地方：chinese SKILL.md 的「where it is used as the technical term」改成「where it is used in the meaning the list gives it」；write-note 與 write-topic 改成「Keep terms in English when they are already English in the source」。
  - 2.3 的對照頁加一項說明這次改名；report-md-rules 的草稿（2.5）和其他 13 份一起重查、重記；全部一個 commit。

**進度**

- 2026-10-14 做完：
  - term：tw-keep-english 原文、草稿與兩份中文版各 3 行；草稿的 Technical words 拿掉 technical term，term 本來就在清單上。
    chinese 的 SKILL.md 改了 6 行，比盤點多出第 31 行 kept-English span 的定義，它和第 365 行是同一句話；SKILL-tw.md 的「技術術語」跟著改成「術語」。
    write-note 與 write-topic 各 1 行；現行文件不再有 technical term、技術詞或技術術語，只剩 task 檔的紀錄。
  - project-approved words：ste-custom.md 與中文版的標題、ste-rules.md 6 行（第 210 行也有一處，盤點時漏了）、asd-ste 的 SKILL.md 與中文版各 13 處、README.md 與中文版各 7 處，以及 `check_ste.py` 的 10 處說明文字。
    `check_ste.py` 的方法名 `customized` 與 findings 的 `customization` 鍵是識別字，照舊。
  - 檢查：6 對中英對照的 `check_parity.py` 都是 0 failure，警告和改之前相同；`diff_md.py --verify` 都是 0 failure。
    4 份草稿重跑 Step 3 都 PASS，檢查結果和上次逐行相同；DFD、RSDC-Standard、md-style 的 `check_ste.py --ste` PASS。
    14 份重記 `[[ste-custom]]`（新指紋 `170f44db79c8`）；asd-ste 的 SKILL.md 與中文版重記 ste-rules.md，6 份 README 重記 chinese SKILL.md，`depends_on.py check` 都是 UNCHANGED。
    check-skill 的 `scan_skill.py`：asd-ste 與 chinese 都沒有沒用到的術語；和改之前比，差別只在改名本身。
  - 2.3 的對照頁加了第 8 項說明這次改名，共 12 項、95 個行號，已通過的檔頭那一項維持通過；2.5 的對照頁以原本的註記重建，草稿文字沒動。
- 2026-10-14 補做：中文版的名稱統一成 keep-English list。
  asd-ste 的 SKILL-tw.md 第 99 行、README-tw.md 第 154 行與 ste-custom-tw.md 第 27 行原本寫「keep-English 清單」；chinese 的 SKILL-tw.md 本來就寫 keep-English list。
  順帶照 keep-English list 改了兩處：chinese 的 SKILL-tw.md 第 94 行的「結果」改成 outcome，asd-ste 的 SKILL-tw.md 第 43 行的「系統」改成 system。
  四對的 `check_parity.py` 都是 0 failure，警告和改之前相同；英文沒有改，所以 `diff_md.py --verify` 把中文版的這幾行報成變動範圍之外的修改。
  另外對兩個 workspace 的 70 對中英對照跑了一次 `check_parity.py --keep`，只列出來，沒有改：tw-keep-english 自己的兩份表格之外，48 份中文版有譯法警告，共 364 行。
  最多的是 script 寫成「腳本」（190 行、40 份）、step 寫成「步驟」（70 行、13 份）與 stale 寫成「過期」（21 行、9 份）；要不要改，另外決定。
- 2026-10-14 再補：chinese skill 的 glossary 補上 **term** 的定義，放在 DEDICATED TERMINOLOGY 的 glossary term 前面。
  定義是「a word or a phrase with one fixed meaning in the source file's subject, such as *checkpoint*, *commit*, *placeholder* or *verdict*, as opposed to an ordinary word in its everyday sense」，例子取自 keep-English list。
  SKILL.md 的規則與步驟有多處用到 term，glossary term 與 keep-English list 的定義也靠它，卻沒有定義；skill-writing.md 要求步驟依賴的名詞都定義在 glossary。
  term 成了 glossary term，依 chinese skill 自己的規則在中文版保留英文：SKILL-tw.md 的 35 處「術語」改成 term，只有第 12、21 行是範本共用的行，照範本保留「術語」。
  tw-keep-english 不動；它不在 chinese skill 裡，中文版照前面的決定寫「術語」。
  檢查：`check_parity.py` 0 failure，警告和改之前相同；`diff_md.py --verify` 報 2 個 failure，因為中文版改到了英文變動範圍以外的段落與 description，這是照 glossary 的規則刻意改的。
  check-skill 的 `scan_skill.py` 把 term 認成 glossary term，沒有沒用到的；記錄 chinese SKILL.md 的 6 份 README 重記，`depends_on.py check` 都是 UNCHANGED。
- 2026-10-14 三補：tw-keep-english 也補上 term 的定義，中文版也寫 term。
  原文在 The rule 的第一句加上和 chinese skill 的 glossary 同一句的定義；草稿以 STE 寫成三句，因為 subject 與 meaning 不在字典裡，寫成「always identifies the same item in a document」。
  兩份中文版指 term 的地方都寫 term，和 chinese skill 的中文版一致：Task 43 改的「術語」，以及原本的「詞」「這個詞」「英文詞」——原檔中文版 10 行、草稿中文版 15 行，另加定義那幾行；指 ordinary word 的「一般的詞」照舊。
  只是改名與補上定義，規則與清單都沒變，版本維持 261013。
  草稿重跑 Step 3 PASS，仍只有 op 那一則警告；兩對的 `check_parity.py` 0 failure，警告和改之前相同；`diff_md.py --verify` 各報 1 個 failure，因為中文版改到了英文變動範圍以外的行，這是刻意的。
  2.3 的對照頁：第 8 項改寫成四個子項，其他項目的行號自動對到新位置，共 108 個行號；檔頭那一項維持通過。
  現在中文版寫 term 的，是 chinese skill 與 tw-keep-english；其他中文版仍寫「術語」。

## 3. 要做的

**要改的（2026-10-14 盤點）**

- technical term：
  - tw-keep-english.md 第 11、18、110 行，與中文版的「技術詞」。
  - 草稿 tw-keep-english-ste.md 第 23、33、140 行與 Technical words 行裡的 technical term，草稿的中文版跟著改。
  - chinese 的 SKILL.md 第 32、88、90、365、366 行，與 SKILL-tw.md 的「技術術語」；記錄 chinese SKILL.md 的 6 份 README（asd-ste、check-skill、gen-skill 與它們的中文版）讀過改動後重記。
  - write-note 的 SKILL.md 第 158 行、write-topic 的 SKILL.md 第 126 行；這兩個 skill 沒有中文版，也沒有 README。
- STE customization：
  - asd-ste 的 SKILL.md、README.md 與兩者的中文版：glossary、CONFIGURATION、Step 1 到 Step 3，以及 Dataflow 的節點。
  - [ste-rules.md](../.github/common/skills/asd-ste/references/ste-rules.md) 第 8、16、225、239、243 行，其中第 239 行是 House Rule 11 的標題；記錄它的 asd-ste SKILL.md 與中文版重記。
  - ste-custom.md 與中文版的標題。
  - `check_ste.py` 的 docstring、註解與 `--custom` 的說明文字。
- 連帶要做的：
  - ste-custom.md 一改，指紋就變：記錄它的 14 份要重查再重記——DFD、RSDC-Standard、md-style 這 3 份 STE 檔跑 `check_ste.py --ste`，tw-keep-english、report-md-rules、SKILL-tmp、README-tmp 這 4 份草稿重跑 Step 3，各連同中文版。
  - tw-keep-english 改完，草稿重跑 Step 3，2.3 的對照頁重建；文字變了的項目回到待審。

**改 skill 時**

asd-ste 有 README.md：先讀它的 When the Skill Is Changed，照它一起改、跑它列的檢查。
chinese、write-note 與 write-topic 沒有 README.md：先讀 [skill-writing.md](../.github/common/rules/skill-writing.md)。
中文版照 chinese skill 只翻改動的部分，再以 `check_parity.py` 對照。

## 4. 驗證

—

## 5. 與其他 task 的關係

**與其他 task 的關係**

- [[Task 32]]：本 task 改到它正在審的 tw-keep-english 草稿（2.3），也讓宣告 `[[ste-custom]]` 的草稿要重跑 Step 3，包括正在審的 report-md-rules（2.5）。
- [[Task 35]]：建立 ste-custom.md，當時取名 STE customization。

## 6. 知識

—

## 7. 日誌

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-14

- 提出：Task 32 審 tw-keep-english 的草稿時，發現 technical term 與 technical word 的名稱太像。
- 決定 technical term 改稱 term，STE customization 改稱 project-approved word，並在同日完成改名。
- 同日補做：統一中文版的名稱，並在 chinese skill 與 tw-keep-english 補上 term 的定義。
