# Task 33 - 從所有原檔拿掉指向中文版的那一句

**Status**：完成——2026-10-12：源頭、SkillsGestalt 與 InvestForge 的文件都拿掉了指向中文版的那一句（SkillsGestalt `0e55dde`、`e8828ea`，InvestForge `7d4f3fd`、`6bb7f33`）；第 4 步的檢查沒有找到本 task 留下的問題。
**Raised**：2026-10-12，[[Task 31]] 做 2.1 之前，使用者決定：中文版是給人審核用的，英文原檔不必寫「它的繁體中文 twin 是…」，所有原檔一次拿掉這一句。
**Depends on**：—

## 1. 背景

背景：有中文版、又沒有 frontmatter 的英文檔，開頭常有一句指向中文版，例如 DFD.md 第 6 行 `Its 繁體中文 twin is [DFD-tw.md](DFD-tw.md): the two are one document in two languages, and a change made to one is made to the other.`。
中文版在同一行連回英文，chinese skill 把這一行當作中文版的 pairing line。
照範本寫的 RSDC 則用 metadata 的「- **Twin**:」一行，`check_rsdc.py` 原本要求英文與中文版都要有，少了就是 FAIL。

## 2. 現況

**2026-10-12 做了什麼：第 1 步**（SkillsGestalt `0e55dde`、InvestForge `7d4f3fd`）

做之前問了 8 個問題，決定如下：`check_rsdc.py` 遇到指向中文版的連結就 FAIL；chinese 的提醒寫在 description，也加上觸發詞；chinese 對 pairing line 的處理留作相容，不改；指紋等依賴方改好的那一步再重記；CLAUDE.md 寫一句規則加一句做法；只跑涵蓋這次改動的檢查；改動與紀錄分開 commit。

- **範本**：README-tmp 第 17 行、`RSDC-App-tmp.md` 與 `RSDC-Skill-System-tmp.md` 第 21 行的 Twin 行拿掉，連同中文版。
  chinese 判定 INCREMENTAL，中文版只刪掉同一行。
- **`check_rsdc.py`**：英文 RSDC 連到自己的中文版、中文版連回英文，都判 FAIL，並列出行號——`no line links to the twin` 與 `neither file links to the other`。
  連結帶路徑或錨點也算，fenced block 裡的不算；比對兩份的連結時，兩者之間的連結仍放一邊。
  實測：InvCov 與 StopPriceChecker 現在各多 1 項英文、1 項一對的 FAIL；拿掉 Twin 行的副本全部 PASS——InvCov 英文 26 項、一對 13 項，StopPriceChecker 英文 28 項、一對 13 項。
  `--standard` PASS。
- **chinese**：description 加上 `Whenever an English file with a -tw.md twin beside it changes, run this skill on it in the same run, so the twin keeps up.` 與觸發詞 `update the twin`，中文版同步；pairing line 的處理不動。
- **asd-ste**：`references/ste-rules.md` 規則 7 的例子，換成 DFD 的 Version 行在 STE 草稿裡的寫法。
- **gen-skill**：Step 6 改成只有對 `SKILL.md` 的那一次執行會加 pairing line，中文版同步。
- **CLAUDE.md**：SkillsGestalt 在根目錄新增一份；InvestForge 在 `## Skills` 之後加 `## 繁體中文 twins` 一節。
- **重記**：6 份 README 對 chinese/SKILL.md 的記錄，asd-ste 的 SKILL.md 與中文版對 ste-rules.md 的記錄。
  README-tmp 的 6 筆與兩份 RSDC 範本的 4 筆現在是 CHANGED，分別留到第 2、3 步。
- **檢查**：9 對 `check_parity.py` 0 failure；5 對 `diff_md.py --verify` 通過；`depends_on.py check` 只剩上面那 10 筆 CHANGED。
  沒有跑 /gen-skill 的拋棄式 skill 與 /check-skill：這一步只拿掉幾行、改幾句，沒有動到標題、佔位符與步驟。

**2026-10-12 做了什麼：第 2 步**（SkillsGestalt `e8828ea`）

做之前問了 6 個問題，決定如下：版本的註明放在 261010 一節最前面；gen-imp-app 要 owner skill 指向 SKILL-tw.md 的那一句也拿掉；Task 31 記錄的草稿行號，在 Task 31.md 與 checkpoint 一起更新；指向中文版的句子後面接著的「兩份一起改」一起拿掉；只跑涵蓋這次改動的檢查；改動與紀錄分開 commit。

- **references 與 rules**：DFD.md、RSDC-Standard.md、skill-writing.md 的這一句，scratch-rules.md、tools.md 的引用區連同後面一個空行，與它們的中文版。
- **版本的註明**：RSDC-Standard.md 的 261010 一節最前面加上 `On 2026-10-12 the line that pointed to the 繁體中文 twin was taken out of this document and DFD.md; no rule changed, so the version did not.`。
  STE 草稿把它寫成兩句，放在草稿原有的三句之後；中文版都同步，版本仍是 261010。
- **STE 草稿**：DFD-ste 與 RSDC-Standard-ste 各拿掉第 21–24 行——asd-ste 把原檔那一句寫成的三句，與一個空行。
  DFD-ste 不再用到 twin，Technical words 拿掉它；`check_ste.py` 兩份都 PASS，RSDC-Standard-ste 仍是原本那 4 個被動句警告。
- **README**：asd-ste、check-skill、gen-skill 的那一行，與它們的中文版。
- **skill 與 mermaid-view 的文件**：
  - checking-criteria.md、compile-skill 的 Tasks.md、imp-home 的 Home-RSDC 與 Wireframe（連同「兩份一起改」那一句）、MermaidView-RSDC 第 3 行與第 527 行。
  - SKILL.md 字彙表的那一條（gen-rsdc-app、imp-app、imp-home），與內文的「this file's **繁體中文 twin**」。
  - check-skill 與 compile-skill 指向別份文件中文版的地方；gen-imp-app 的「Point at it from `SKILL.md`'s CONFIGURATION…」，它沒有中文版。
- **重記**：6 份 README 對 README-tmp、DFD.md、skill-writing.md 的記錄，check-skill 的 README 兩份對 scratch-rules.md 的記錄，兩份 RSDC 範本與中文版對 DFD.md、RSDC-Standard.md 的記錄。
  `check_rsdc.py --standard` PASS；這 12 份檔的 56 筆記錄都是 UNCHANGED。
- **Task 31 的行號**：Task 31.md 與兩份 checkpoint 的 `intentional_differences` 改成新行號——DFD-ste 26→22，RSDC-Standard-ste 31→27、40→36、408→404。
- **檢查**：20 對 `check_parity.py` 0 failure，`diff_md.py --verify` 都通過；剩下的警告在改動之前就有。
  再掃一次 SkillsGestalt，英文檔裡提到中文版的，只剩「保留的」所列。
- **InvestForge**：StopPriceChecker、InvCov 兩對對 DFD.md、RSDC-Standard.md 與兩份範本的記錄現在是 CHANGED，留到第 3 步。

**2026-10-12 做了什麼：第 3 步**（InvestForge `6bb7f33`）

做之前問了 6 個問題，決定如下：沒對齊的中文版手動拿掉對應的句子，確認 FAIL 沒有變多；折行的段落不重排；InvCov 的檔案清單寫成 `this design document` 與 `the Page's wireframe`；InvCov 與 InvHome 的生命週期紀錄不記；只跑涵蓋這次改動的檢查；改動與紀錄分開 commit。

- **RSDC**：StopPriceChecker、InvCov 的 Twin 行；InvCtl、InvDatabase、InvFinSight、InvTechRank、InvHome 開頭指向中文版的那一段或那一句；InvFinSight 第 10–11 行對 Wireframe 中文版的指向；InvCov 的檔案清單只列英文檔。
- **Wireframe**：imp-inv-* 的四份與 InvHome 的那一句。
- **SKILL.md**：check-stop-price 與四個 owner skill 字彙表指向自己中文版的那一條；design document、wireframe 條目裡的中文版連結，`they decide` 跟著改成 `it decides`；check-stop-price 的目錄樹拿掉兩列中文版。
- **README**：四個 owner skill 的 README 只連英文檔；它們沒有中文版。
- **中文版**：17 份。
  逐行對齊的 StopPriceChecker、InvCov 與 InvHome 的 Wireframe，以及 5 份 SKILL-tw.md，照 chinese 的 INCREMENTAL 改；其餘沒對齊的，手動拿掉對應的句子。
- **重記**：StopPriceChecker、InvCov 兩對對 DFD.md、RSDC-Standard.md 與範本的 12 筆記錄，都是 UNCHANGED。
- **檢查**：
  - `check_parity.py`：FAIL 沒有變多，反而少了 7 項——InvCtl、InvDatabase 的 RSDC 與 imp-inv-tech-rank 的 Wireframe 各少 2 項（pairing line 與連結），check-stop-price 的 SKILL 少 1 項（連結數）；「孿生檔」的譯法警告也沒了。
    沒對齊的幾對，「每一行同一種」那一項的不符行數有增有減，例如 imp-inv-database 的 Wireframe 從 65 變成 100：中文版少了一行，錯位更多；Task 30、[[Task 18]] 對齊時會整份重寫。
  - `diff_md.py --verify`：逐行對齊的 3 對與 5 份 SKILL 都通過。
  - RSDC Checker：StopPriceChecker 與 InvCov 的英文、一對都恢復 PASS，InvCov 英文仍有原本那 1 個警告；check-stop-price 的 `--skill` PASS。
  - gen-imp-app 的 owner-skill checker：imp-inv-database、fin-sight、tech-rank 通過；imp-inv-ctl 的 2 項 FAIL——app dir 有 `node_modules`、`app.js` 用了 express——HEAD 也一樣，與本次無關。
  - 再掃一次 InvestForge：英文檔裡提到中文版的，只剩「保留的」所列。
- **沒有動**：InvestForge 裡別人還沒 commit 的 8 個修改，例如 check-stop-price 的 `rule-copies.md`。

**2026-10-12 做了什麼：第 4 步**

先跑完檢查，再問了 6 個問題，決定如下：標為完成；不是本 task 造成的 3 筆 CHANGED 不動，寫進紀錄；Task 31、18、30 裡「等 Task 33」的說明一起更新；「驗證」照實際結果改寫；收尾放在一個 commit；做完先停，不接著做 [[Task 34]]。

- **記錄的指紋**：兩個 workspace 共 28 份檔、84 筆記錄，81 筆 UNCHANGED。
  另外 3 筆 CHANGED 不是本 task 造成的，沒有動：
  - check-md-deps 的 SKILL.md 與中文版對 check-wiki-doc 的記錄，來自 [[Task 19]] 把 check-wiki-doc 改成一句一行（`105ae8d`）。
  - InvestForge 的 check-stop-price 的 `rule-copies.md` 對 StopPriceChecker-RSDC（cited）的記錄，[[Task 18]] 對齊時就已 CHANGED，留給 check-stop-price 下次執行時重記；用第 3 步之前的 RSDC 算，指紋相同。
    這個檔還有別人沒 commit 的修改。
- **`check_parity.py`**：SkillsGestalt 本 task 碰過的 26 對都是 0 failure。
  InvestForge 的 17 對和第 3 步做完時相同：5 對 0 failure，其餘 12 對的 FAIL 都是中文版原本就沒對齊，或 SKILL 原本就有的。
- **RSDC Checker**：兩個 workspace 的 12 份 RSDC，「不連到中文版」的英文與一對兩項檢查都 PASS。
  StopPriceChecker 與 InvCov 整份 PASS；其餘 10 份是舊形狀，FAIL 都在標題、章節、範本連結這類對齊項目，歸 Task 18、30。
- **再掃一次**：兩個 workspace 都找不到指向中文版的寫法——`Its 繁體中文 twin`、`- **Twin**:`、`([繁體中文](…))`、`Chinese reading copy` 與中文版裡連回英文的那一行都沒有了。
- **依賴方**：Task 31、18、30 裡「等 Task 33」的說明改成已完成；摘要表裡 Task 34、31、30、18 的 Depends on 圖示改成 ✅。

## 3. 要做的

**已決定（2026-10-12）**

提出時問了 7 個問題；使用者回答五項待判斷之後，又問了 7 個。
決定如下：

- **範圍**：所有原檔一次拿掉這一句；中文版逐行對齊，同一行一起拿掉。
- **源頭一起改**：範本、產生它的 skill、檢查它的工具都改，免得下一份新文件又寫回去。
- **「兩份要一起改」的提醒**：寫在 chinese skill，也寫進兩個 workspace 根目錄的 CLAUDE.md。
  chinese 只在執行時才讀得到；CLAUDE.md 由 Claude Code 自動載入，改英文檔的人看得到。
  InvestForge 的 CLAUDE.md 加一句；SkillsGestalt 在根目錄新增一份 CLAUDE.md。
- **frontmatter 檔的中文版回連保留**：SKILL-tw.md 這類中文版在 frontmatter 下方連回英文的那一行，在中文版裡、不在原檔裡，保留。
- **現有的 STE 草稿**：DFD-ste 與 RSDC-Standard-ste（含中文版）裡的這一句也由本 task 拿掉，送到 [[Task 32]] 審核的草稿就沒有它。
- **版本**：維持 261010，照 [[Task 31]] 決定的版本規則——只有規則改變才升版。
  RSDC-Standard.md 與 RSDC-Standard-ste.md 的 261010 一節各加一句：拿掉了指向中文版的那一句，規則沒有變；DFD 的改動也記在這裡；中文版同步。
- **SKILL.md 字彙表裡指向自己中文版的一條**：拿掉，共 8 份；內文用到這個術語的地方跟著改。
  提出時說有 frontmatter 的英文檔沒有這一句，這一點不對，是掃描時才發現的。
- **兩份 RSDC 範本第 9 行保留**：說明引用區裡「`RSDC-App-tmp-tw.md` is this file's twin…」說的是範本中文版的用途——chinese 從它複製共用句——不只是指向它。
- **指向別份文件中文版的**：連結和只寫檔名的單純指向都拿掉；skill 真的要寫出中文版的定義與規則保留，例如 design pair、wireframe pair。
- **列出檔案的清單**：只拿掉描述檔案的清單。
  README 的 Files Each Step Uses、When the Skill Is Changed、Tracked Dependencies 列到中文版的行，以及執行前要確認存在的檔，都保留：`skills/CLAUDE.md` 要求改 skill 的人照 README 做，拿掉了就沒有東西提醒他改中文版、跑 `check_parity.py`。
- **分步**：先源頭、再文件，分 4 步；每一步在動到的 repo 各一個 commit，前綴 `task 33`，做完打 ✅。
- **指紋重記**（第 1 步之前決定）：等依賴方改好的那一步再重記——重記的意思是讀過、確認依賴方仍然成立。
  所以各步自己重記它改好的文件；第 4 步只做最後的檢查。
- **依賴**：Task 31、Task 18、Task 30 依賴本 task。

**要做的**

行號是 2026-10-12 的；每一份的中文版跟著改，沒有 frontmatter 的在同一行，SKILL-tw.md 在同一個標題下。

1. ✅ **源頭**：範本、`check_rsdc.py`、chinese、asd-ste、gen-skill 與兩份 CLAUDE.md（2026-10-12 完成，見下）。
2. ✅ **SkillsGestalt 的文件**：references 與 rules、兩份 STE 草稿、README、skill 與 mermaid-view 的文件，以及 gen-imp-app（2026-10-12 完成，見下）。
3. ✅ **InvestForge 的文件**：7 份 RSDC、5 份 Wireframe、5 份 SKILL.md 與 4 份 README（2026-10-12 完成，見下）。
4. ✅ **最後的檢查**：記錄的指紋、每一對的 `check_parity.py`、每一份 RSDC 的 RSDC Checker，再掃一次兩個 workspace（2026-10-12 完成，見下）。

**保留的**

- 講中文版的規則或做法的句子：例如 `md-style.md` 第 19 行、`skill-writing.md` 第 15 行、`tw-keep-english.md` 第 3 行，以及 chinese、check-skill、check-md-deps、gen-skill、asd-ste、reformat-md 這類寫出或檢查中文版的 skill。
- 歷史紀錄：RSDC-Standard.md 的 Changes 一節（第 220、256 行）與 STE 草稿裡對應的句子、MermaidView-RSDC 第 685 行、InvDataflow 的 `Prompts.md`。
- 範本的說明引用區：兩份 RSDC 範本第 9 行；imp-app 的 `assets/Wireframe-tmp.md` 第 4 行——它說 reverse 寫出哪兩份檔，範本本身沒有這一句。
- skill 真的要寫出或讀取中文版的定義與規則：
  - gen-rsdc-app、gen-imp-app、imp-app、imp-home 的 design pair、wireframe pair、skill pair、seed documents 這類定義。
  - gen-rsdc-app 的 design template、gen-rsdc-skill 的 RSDC template 連同範本的中文版：chinese 從範本中文版複製共用句，和範本第 9 行同一個理由。
  - owner skill 的「A design change … in both languages」這類規則。
- README 列到中文版的行，以及 imp-inv-fin-sight 的 SKILL.md 第 149–150 行執行前的確認。
- chinese 對沒有 frontmatter 時 pairing line 的處理：留作相容，還留著那一行的檔照樣通過。
- 沒有這一句的：InvDataflow、InvIndexAnalyzer、SkillCompiler，以及其他 workspace 的 5 份 RSDC（ArtifactPipe、GeminiChatOrganizer、CompileSkill、EvernoteCli、LlmWikiGenerator）。

**改的方式**

- 中文版照 chinese 的 INCREMENTAL 流程跟著改；每一對都跑 `check_parity.py`。
- 改 skill 之前，先讀它 README 的 When the Skill Is Changed，照它改並跑它列出的檢查。
- RSDC：`check_rsdc.py` 與兩份範本已在第 1 步改好；拿掉已寫好的 RSDC 的這一句之後，每一份跑 RSDC Checker。

## 4. 驗證

**驗證**

- 有 `-tw.md` 的英文檔裡，找不到「要做的」所列的那幾類句子；還提到中文版的，只剩「保留的」所列。
- 本 task 碰過的檔：SkillsGestalt 的 `check_parity.py` 都是 0 failure；InvestForge 沒有新增 FAIL。
- RSDC Checker 對每一份 RSDC 的「不連到中文版」兩項檢查都 PASS；`check_tasks.py` PASS。
- `depends_on.py check` 找不到本 task 造成的 CHANGED。
- 2026-10-12 的結果與例外，見「第 4 步」。

## 5. 與其他 task 的關係

**與其他 task 的關係**

- [[Task 31]]：依賴本 task——其餘的草稿在這一句拿掉之後再產生；原本沒有中文版的檔，草稿也不必寫這一句。
- [[Task 34]]：依賴本 task——chinese skill 先改好，再為沒有中文版的 4 份原檔寫中文版。
- [[Task 18]]、Task 30：依賴本 task——RSDC 範本先拿掉 Twin 行，對齊才不必做兩次。
- [[Task 32]]：審核的草稿已經沒有這一句。
  本 task 先照新的版本規則做；原檔裡寫的版本規則，要等 Task 32 以草稿取代原檔才改過來。
- [[Task 24]]：要照 README-tmp.md 寫 27 份 README，本 task 改了範本之後，它寫出的 README 就沒有這一句。

## 6. 日誌

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。
- 指向 Task 30 的 wikilink 改成純文字：它已移出本 workspace（[[Task 62.4]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-12

- 提出：使用者決定所有原檔拿掉指向中文版的那一句。
- 分 4 步完成：源頭、SkillsGestalt 的文件、InvestForge 的文件、最後的檢查。
- 標為完成，檢查沒有找到本 task 留下的問題。
