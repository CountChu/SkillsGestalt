# Task 32.10 - README-tmp

**Status**：完成——2026-10-19 第四輪審核 30 項全部通過，先做完 [[Task 64]] 的 gen-skill 規則，同日由 Step 7 取代原檔與它的中文版。
**Raised**：2026-10-12，[[Task 32]] 提出時列出的草稿之一，原本是它要做的 2.10。
**Depends on**：[[Task 64]]

## 1. 背景

審核 [[Task 31]] 為 [README-tmp.md](../.github/common/templates/README-tmp.md) 產生的 STE 草稿與草稿中文版；通過就由 asd-ste 的 Step 7 取代原檔與它的中文版。
分工、取代的方式與「每取代一份要一併做的」，見 [[Task 32]]。

## 2. 現況

### 審核時決定的

- **送審前的準備**（2026-10-18）：重跑 Step 1，存下標題詞的判定：清冊問 Runs（第 21 行「# When the Skill Runs」，動詞）與 Files（第 84 行「## Files Each Step Uses」）。
  使用者決定把 run 收進 ste-custom.md，核准動詞與名詞，意思是「to make a program, a script, a skill or a step do its work; as a noun, one time that it does this」；標題是每份 README 都要維持原樣的必要標題。
  Files 是名詞，當技術名詞；清冊把它當動詞問，是因為字典只列了 file 的動詞。
- **連帶拿掉 run**（2026-10-18）：run 原本列在 10 份 STE 檔與 2 份草稿的 Technical words，專案核准詞不列為技術用字（House Rule 11），所以都拿掉，各自的中文版同步。
  這 12 份是 DFD、RSDC-Standard、tw-keep-english、report-yaml-rules、scratch-rules、md-style、report-md-rules、skill-writing、chore-rules、task-rules，以及 README-tmp 與 SKILL-tmp 的草稿；只改 header note，RSDC-Standard 與 tw-keep-english 的版本照舊。
  記錄這些檔的 42 行紀錄讀過都仍成立，重記：DFD 16 行、RSDC-Standard 10 行、md-style 6 行、skill-writing 6 行、report-yaml-rules 2 行、scratch-rules 2 行，其中 InvestForge 8 行。
- **改回原文的字**（2026-10-18）：草稿第 20 行寫「Each time a skill runs」，第 21 行寫「the parts that a run does not need」，第 43 行寫「when it runs」，第 108 行寫「run a script」；中文版這四行原本就寫「執行」「不需要」，不必改。
  已取代的 skill-writing、tools 寫的 operate 這次不動。
- **gen-skill 會抄進範本的 STE 檔頭**（2026-10-18）：gen-skill 的 Step 5 整份抄 README 範本，header note 兩行會留在新的 README，把它標成 STE 檔。
  使用者決定另開 [[Task 64]] 改 gen-skill，在本草稿取代原檔之前做完；SKILL-tmp（[[Task 32.11]]）也一樣。
- **其他只列進審核重點**：第 22 行把並列寫成因果、第 42 行與第 179–180 行的 so that 變成 thus、第 107 行會抄進每份 README 的句子、第 170 行多了 `[FAIL]`，以及標題裡清冊不問的 Tracked、Dependencies（[[Task 41]]）。
- **提交**：本 workspace 與 InvestForge 各一個 commit，前綴 `task 32.10`；ste-custom.md 今天還可能再改，[[Chore 1]] 等當天最後一次修改之後再跑。
- **第二輪的三項 `[?]`**（2026-10-18）：使用者把英文第 4 點的第 22、107、179–180 行標 `[?]`。
  使用者問第 22 行的 this file 指什麼：指照範本寫出的那份 README，範本正文是用它的口吻寫的。
  使用者決定把正文的 this file 都改成 this README.md，第 22 行寫「SKILL.md does not have a link to this README.md, thus no run reads it.」。
  改到的是第 19、21、22、24、131、171、179 行與最後一行；第 162 行在 fenced block 裡，必須和原文一字不差，照舊；檔頭註記的 This file 指範本自己，也不改。
  中文版的「本檔」一律寫「這份 README.md」，第 131 行不再把 README.md 與本檔對調，改照英文的順序。
  第 179–180 行併成一句「…, to keep SKILL.md short.」，用不定詞保留原文 so that 的目的，中文版寫「讓 SKILL.md 保持精簡」。
  第 107 行照建議不改，由使用者在對照頁上標 `[v]`；一個 commit，前綴 `task 32.10`。
- **第三輪的兩項 `[?]`**（2026-10-18）：第 107 行是 scripted-versus-not 規則的引導句，草稿照抄 skill-writing 第 41 行寫成「This skill tells one time …」，但說明的其實是這份 README。
  使用者標 `[x]`，主詞改成「This README.md tells one time how the skill obeys the rule of skill-writing.md about scripts:」。
  第 179 行第二輪放在句尾的「, to keep SKILL.md short」會被讀成 SKILL.md 為了精簡而依賴那些檔案；使用者決定把目的移到句首：「To keep SKILL.md short, this README.md gives the files external to the skill that SKILL.md depends on.」。
  中文版照英文改；第 42 行維持通過，不改；asd-ste、check-skill、gen-skill 的 README 裡第 107 行那一句，取代原檔時照「範本的後續」一併決定；一個 commit，前綴 `task 32.10`。

- **第四輪：保留規則的名稱**（2026-10-18）：使用者認為 STE 改寫規則的名稱時，例如「The scripted-versus-not rule …」，應該保留 scripted-versus-not。
  它是規則的名稱，check-skill、gen-skill、gen-imp-app 與三份 README 都用它；STE 規定一樣東西只用一個名稱（規則 1.11），skill-writing 的 STE 版也把「no forward-reference」寫在引號裡。
  第 107 行保留第三輪的主詞，加上名稱：「This README.md tells one time how the skill obeys the "scripted-versus-not" rule of skill-writing.md:」，中文版用中文引號寫「「scripted-versus-not」規則」。
  ste-custom.md 的 Rules 表加上一條：原文替一樣東西取的名稱，例如一條規則的名稱，照原樣寫在引號裡；Checked 寫「—」，由審核的人看。
  skill-writing 那條規則的標題帶上這個名稱，交給 [[Task 61]]；已取代的 STE 檔有沒有被改寫掉的名稱，使用者決定現在就回頭找；一個 commit，前綴 `task 32.10`。

### 進度

- README-tmp：2026-10-18 以 Step 6 產生對照頁送審，連結是 `http://127.0.0.1:8790/templates-README-tmp/`。
  ste-custom.md 與中文版加上 run 一列（新指紋 `f64a5e15b755`）；中文版照 chinese skill 只改 change set，`check_parity.py` 0 failure、0 warning，`diff_md.py --verify` PASS。
  12 份檔與中文版的 Technical words 拿掉 run：`diff_md.py --verify` 都 PASS，`check_parity.py` 和之前相同；10 份 STE 檔的 `check_ste.py --ste` 都 PASS，只多了 run 的 `[INFO]`。
  草稿第 20、21、43、108 行改回原文的字；Step 3 重跑 PASS，沒有警告，多了 need 與 run 的 `[INFO]`，`[[ASD-STE100_ISSUE9.pdf]]`（指紋不變）與 `[[ste-custom]]` 重記。
  SKILL-tmp 的草稿也重跑 Step 3，PASS，沒有警告，`[[ste-custom]]` 重記。
  42 行紀錄重記之後，本 workspace 的 12 份 `depends_on.py check` 共 62 項都是 UNCHANGED，InvestForge 4 份共 12 項也是；兩份 RSDC 範本的 `check_rsdc.py --standard` 都是 8 項 PASS。
  asd-ste 的 SKILL.md 與中文版 `depends_on.py check` 都是 UNCHANGED，check-skill 的 `scan_skill.py` 只多了 ste-custom 兩份的行數與 README 重記的紀錄。
  審核重點英文 5 項、中文 4 項，共 26 個審核狀態、79 個行號：檔頭與 gen-skill、標題用字、送審前已改的地方、六處句意、結構、中文版的譯法。
  第二輪（同日）：草稿與中文版各改 8 行、併掉 1 行，剩 195 行；中文版照 chinese skill 只改 change set，`check_parity.py` 0 failure，`diff_md.py --verify` PASS。
  Step 3 重跑 PASS，沒有警告，句子由 54 句減為 53 句；`[[ste-custom]]` 照舊是 `f64a5e15b755`。
  註記改寫第 22 行與第 179 行的兩項與中文對應的兩項，「送審前已改的地方」英文與中文各加一項 this README.md，結構那一項跟著改；對照頁重建，共 9 項、29 個審核狀態、98 個行號，14 項通過、1 項待解釋、14 項待審。
  第三輪（同日）：草稿與中文版各改 2 行；中文版照 chinese skill 只改 change set，`check_parity.py` 0 failure，`diff_md.py --verify` PASS；Step 3 重跑 PASS，報告和之前相同。
  註記改寫英文與中文的第 107、179 行各兩項，註明第三輪已改；對照頁重建，共 9 項、30 個審核狀態、100 個行號，15 項通過、15 項待審。
  第四輪（同日）：ste-custom.md 與中文版的 Rules 表加上一列（新指紋 `d318d3b982e5`）；中文版照 chinese skill 只改 change set，`check_parity.py` 0 failure、0 warning，`diff_md.py --verify` PASS；`check_ste.py` 照樣讀得到這張表。
  草稿與中文版第 107 行改寫，`check_parity.py` 0 failure，`diff_md.py --verify` PASS；Step 3 重跑 PASS，報告和之前相同：引號裡的名稱照 House Rule 10 算一個字。
  註記改寫英文與中文的第 107 行各一項，註明第四輪已改；對照頁重建，共 9 項、30 個審核狀態、100 個行號，15 項通過、15 項待審。
- 取代（2026-10-19）：第四輪 30 項全部通過；Step 3 記下的 ste-custom 指紋是現在的 `d318d3b982e5`，所以 Step 7 不必先重跑 Step 3 與 Step 6。
  使用者決定先做 [[Task 64]]：gen-skill 的 MUST FOLLOW 加上不帶範本 STE 標記的規則，另一個 commit。
  `draft.py replace` 把草稿與它的中文版寫回 README-tmp.md 與 README-tmp-tw.md，檔頭註記刪成兩行，再刪掉兩份草稿；兩份都是 194 行。
  `draft.py dependents` 以本 workspace、InvestForge 與 BookMaster 為 root，找到 asd-ste、check-skill、gen-skill 的 README 與中文版 6 份。
  它們依賴的是範本的結構：`scan_skill.py` 對三個 skill 都報 `readme_missing_headings: []`，結構仍符合，照使用者的決定重記（新指紋 `22c905a3669e`），`depends_on.py check` 都是 UNCHANGED。
  檢查：`check_ste.py --ste` PASS，沒有警告；parity check 0 failure、0 warning，原文中文版「腳本」的那則警告也沒有了。
  三份 README 還有 60 行照舊範本抄的共用句子，照「範本的後續」列出來，使用者決定另開 [[Task 66]] 一次改完。
  [[Task 31]] 表格裡指向兩份草稿的連結改成行內程式碼，並註明已取代。

## 3. 要做的

—

## 4. 驗證

—

## 5. 與其他 task 的關係

- [[Task 64]]：gen-skill 抄範本時不帶 STE 檔頭，本草稿取代原檔之前要先做完。
- [[Task 32.11]]：SKILL-tmp 的草稿，有同樣的 gen-skill 問題；這次 Technical words 也拿掉 run。
- [[Task 41]]：標題裡字典沒有收錄的字，清冊不問。
- [[Task 61]]：第 22 行「SKILL.md 不連到 README」也是 skill-writing 第二條說的事，屬於規則重複的檢查。
- [[Task 65]]：本草稿取代原檔之後，對照 DFD.md 檢查範本的 Dataflow 一節。
- [[Task 66]]：取代之後，三份 README 照舊範本抄的共用句子換成新範本的寫法。
- [[Chore 1]]：ste-custom.md 有改動的日子集中重記一次，本草稿與它的中文版也在其中。

## 6. 日誌

### 2026-10-19

- 第四輪審核 30 項全部通過；[[Task 64]] 先改好 gen-skill，再由 Step 7 取代原檔與它的中文版；6 份 README 重記，[[Task 31]] 表格的草稿連結改成行內程式碼；另開 [[Task 66]]。

### 2026-10-18

- 從 [[Task 32]] 拆出：原本是它要做的 2.10；屬於這份檔案的內容搬到這裡，內容沒有改。
- 送審：重跑 Step 1；run 收進 ste-custom.md，12 份檔的 Technical words 拿掉 run 並重記 42 行紀錄，草稿改回原文的字；Step 3 PASS，對照頁 26 項送審；另開 [[Task 64]]。
- 第二輪：正文的 this file 改成 this README.md，第 179–180 行併成一句、用不定詞保留目的；Step 3 PASS，對照頁重建，14 項待審。
- 第三輪：第 107 行的主詞改成這份 README，第 179 行的目的移到句首；Step 3 PASS，對照頁重建，15 項待審。
- 第四輪：第 107 行的規則名稱照原文寫在引號裡，ste-custom.md 的 Rules 表加上保留名稱的規則；skill-writing 補名稱交給 [[Task 61]]；Step 3 PASS，對照頁重建，15 項待審。

### 2026-10-12

- 列為 [[Task 32]] 要審核的草稿之一。
