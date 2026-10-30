# Task 32.9 - tools

**Status**：完成——2026-10-18 第二輪審核 27 項全部通過，同日由 Step 7 取代原檔與它的中文版。
**Raised**：2026-10-12，[[Task 32]] 提出時列出的草稿之一，原本是它要做的 2.9。
**Depends on**：—

## 1. 背景

審核 [[Task 31]] 為 [tools.md](../.github/common/rules/tools.md) 產生的 STE 草稿與草稿中文版；通過就由 asd-ste 的 Step 7 取代原檔與它的中文版。
分工、取代的方式與「每取代一份要一併做的」，見 [[Task 32]]。

## 2. 現況

### 審核時決定的

- **送審前的準備**（2026-10-18）：重跑 Step 1，存下標題詞的判定：清冊問 Search（第 7 行）與 need（第 13、25 行），兩個都當動詞用，字典不核准。
  使用者決定把 search 收進 ste-custom.md，核准動詞與名詞，意思是「to look through files or text for a pattern, as `rg` does; as a noun, one time that you do this」。
  need 也收進 ste-custom.md，只核准動詞，意思是「to be in a condition where a thing is necessary for you」；兩個標題與表格標題列的「What you need」都維持原樣。
- **改回原文的字**（2026-10-18）：草稿第 17 行寫「Always search with `rg` (`ripgrep`).」，第 52 行寫「This command needs no line numbers.」，第 77 行引號裡的規則寫「read only the lines that you need」，第 95 行寫「the fields that the next step needs」。
  中文版第 52、95 行跟著改，第 17、77 行原本就是這個意思。
  Technical words 拿掉 search；已取代的 DFD.md 與中文版也拿掉，記錄 DFD.md 的 16 份讀過都仍成立、重記。
- **其他只列進審核重點**：第 24 行的「每個指令第一次就寫對」、第 56 行拿掉的 Exception、第 50 行的 cause、第 97–98 行的 agents，以及第 17、25、26 行加上的行內程式碼。
  標題裡的 Pick、narrowed、banned、Print 字典沒有收錄，清冊不問（[[Task 41]]），也列進審核重點。
- **提交**：本 workspace 與 InvestForge 各一個 commit，前綴 `task 32.9`；ste-custom.md 今天還可能再改，[[Chore 1]] 等當天最後一次修改之後再跑。
- **第二輪的 `[?]` 與 `[x]`**（2026-10-18）：使用者把英文第 4 點的第 56 行標 `[?]`、第 50 行標 `[x]`。
  第 56 行：原文以粗體的「Exception —」和上一項的「Default:」成對，exception 字典不核准、也沒有替代字，草稿原本寫「But if」。
  使用者看過說明之後，決定把 exception 收進 ste-custom.md，意思是「a case that a rule or a default does not include」。
  草稿改成「**Exception: if `rg` cannot isolate the one range that you want, use `sed -n 'A,Bp'`.**」，冒號和「Default:」一樣；中文版寫「**例外：如果 `rg` 無法只取出你要的那一段，就用 `sed -n 'A,Bp'`。**」。
  第 50 行照使用者同意的建議改成「That 97% is the purpose of this rule.」，中文版寫「那 97% 就是這條規則的目的。」，和原文中文版的「目的」一致。
  其他用到 exception 的只有 RSDC-Standard 的複合技術用字 exception path 與標籤 Exception Paths，照舊；一個 commit，前綴 `task 32.9`，[[Chore 1]] 照舊等當天最後一次修改。
- **alias 收進 keep-English list**（2026-10-18）：使用者把中文第 2 點的 alias 一項標 `[?]`：原文中文版第 11 行保留英文 alias，草稿中文版第 25 行寫「別名」，alias 不在清單上。
  使用者問能不能把 alias 放進技術用字；技術用字只管英文 STE 檔能用哪些字，中文正文怎麼寫由 keep-English list 決定，同一份草稿中文版的 binary、directory、filter 等技術用字也都翻成中文。
  使用者選擇在清單加上第三個條件：它是一個指令的名稱，替它取的中文詞會對不上執行指令時打的名稱。
  STE 只核准名詞的 type，所以英文寫成「the name that you write to operate the command」。
  清單加上 alias 一列：Replaces 寫「別名」，Flagged 寫「—」，因為「別名」也是「類別名稱」的一部分；Technical words 加上 alias，版本維持 261018，同一天的改動共用一個版號。
  草稿中文版第 25 行改回 alias；在本 task 裡做，一個 commit，前綴 `task 32.9`，[[Chore 2]] 照它的時機跑。

### 進度

- tools：2026-10-18 以 Step 6 產生對照頁送審，連結是 `http://127.0.0.1:8790/rules-tools/`。
  ste-custom.md 與中文版加上 search、need 兩列（新指紋 `fe617c163e46`）；中文版照 chinese skill 只改 change set，`check_parity.py` 0 failure、0 warning，`diff_md.py --verify` PASS。
  草稿與中文版照 chinese skill 只改 change set 的 5 行，`check_parity.py` 0 failure，`diff_md.py --verify` PASS。
  Step 3 重跑 PASS，沒有警告，多了 need 與 search 的 `[INFO]`；`[[ASD-STE100_ISSUE9.pdf]]`（指紋不變）與 `[[ste-custom]]` 重記。
  DFD.md 與中文版的 Technical words 由 31 個減為 30 個，`check_parity.py` 和之前相同、`diff_md.py --verify` PASS，`check_ste.py --ste` PASS，只多了 search 的 `[INFO]`；新指紋 `0bb513b15b3a`。
  記錄 DFD.md 的 16 份重記：兩份 RSDC 範本、imp-home 的 Home-RSDC 與 asd-ste、check-skill、gen-skill 的 README，各含中文版，以及 InvestForge 的 StopPriceChecker-RSDC 與 InvCov-RSDC 與中文版。
  16 份的 `depends_on.py check` 都是 UNCHANGED，兩份範本的 `check_rsdc.py --standard` 都是 8 項 PASS。
  asd-ste 的 SKILL.md、README.md 與中文版 `depends_on.py check` 都是 UNCHANGED，check-skill 的 `scan_skill.py` 只多了 ste-custom 兩份的行數與重記的紀錄。
  審核重點英文 5 項、中文 4 項，共 27 個審核狀態、89 個行號：檔頭、標題用字、送審前已改的地方、五處句意、結構與中文版的譯法。
  第二輪（同日）：ste-custom.md 與中文版加上 exception 一列（新指紋 `76067d3d0559`）；中文版照 chinese skill 只改 change set，`check_parity.py` 0 failure、0 warning，`diff_md.py --verify` PASS。
  草稿第 50、56 行改寫，中文版照 chinese skill 只改 change set 的 2 行，`check_parity.py` 0 failure，`diff_md.py --verify` PASS。
  Step 3 重跑 PASS，沒有警告，多了 exception 與 purpose 的 `[INFO]`；`[[ste-custom]]` 重記。
  asd-ste 的 SKILL.md、README.md 與中文版 `depends_on.py check` 都是 UNCHANGED，check-skill 的 `scan_skill.py` 只多了 ste-custom 兩份的行數。
  註記改寫英文第 4 點與中文第 3 點裡第 56、50 行的各兩項，註明第二輪已改；對照頁重建，仍是 27 項、89 個行號，11 項通過、16 項待審。
  alias（同日）：tw-keep-english.md 的 The rule 加上第三個條件、清單加上 alias 一列，Technical words 由 123 個增為 124 個。
  它的中文版照 chinese skill 只改 change set 的 6 行，`check_parity.py` 和之前相同，`diff_md.py --verify` PASS；`check_ste.py --ste` PASS，句子由 46 句增為 49 句，警告仍只有原本的 op。
  草稿中文版第 25 行的「別名」改成 alias；英文沒有改，`diff_md.py --verify` 照預期只報這一行在改動範圍之外，`check_parity.py` 0 failure。
  Step 3 重跑 PASS，報告和之前相同；註記改寫中文第 2 點的 alias 一項，對照頁重建，27 項中 25 項通過、2 項待審。
- 取代（2026-10-18）：使用者審核完畢，26 項通過，英文第 4 點的標題項沒有標，它底下的子項都已通過；Step 3 記下的 ste-custom 指紋仍是現在的 `76067d3d0559`，所以 Step 7 不必先重跑 Step 3 與 Step 6。
  `draft.py replace` 把草稿與它的中文版寫回 tools.md 與 tools-tw.md，檔頭註記刪成兩行，再刪掉兩份草稿；兩份都是 97 行。
  `draft.py dependents` 以本 workspace、InvestForge 與 BookMaster 為 root，沒有文件記錄 tools.md。
  檢查：`check_ste.py --ste` PASS，沒有警告；parity check 0 failure、0 warning，原文中文版第 40 行的三則 keep-English 警告也沒有了；兩份的 `depends_on.py check` 都是 UNCHANGED。
  [[Task 31]] 表格裡指向兩份草稿的連結改成行內程式碼，並註明已取代。
  另外 20 份的 ste-custom 紀錄仍是舊的：使用者說今天可能還會改 ste-custom.md，[[Chore 1]] 等當天最後一次修改之後再跑。

## 3. 要做的

—

## 4. 驗證

—

## 5. 與其他 task 的關係

- [[Task 50]]：審核前把第 24 行的雙重否定改成肯定句。
- [[Task 41]]：標題裡字典沒有收錄的字，清冊不問。
- [[Task 32.1]]：DFD 已取代原檔；search 收進 ste-custom.md 之後，它的 Technical words 拿掉 search。
- [[Chore 1]]：ste-custom.md 有改動的日子集中重記一次，本草稿與它的中文版也在其中。
- [[Task 59]]：同一天把 app 收進 keep-English list，版本改成 261018；alias 這次照樣用這個版號。
- [[Chore 2]]：keep-English list 換版本之後稽核所有中文版；261018 這一版還沒稽核過，下次會一併涵蓋 app 與 alias。

## 6. 日誌

### 2026-10-18

- 從 [[Task 32]] 拆出：原本是它要做的 2.9；屬於這份檔案的內容搬到這裡，內容沒有改。
- 送審：重跑 Step 1；search 與 need 收進 ste-custom.md，草稿改回原文的字，DFD 拿掉 search 並重記 16 份；Step 3 PASS，對照頁 27 項送審。
- 第二輪：exception 收進 ste-custom.md，第 56 行照原文以「Exception:」開頭，第 50 行改用 purpose；Step 3 PASS，對照頁重建，16 項待審。
- alias：keep-English list 加上「指令的名稱」這個條件並收進 alias，草稿中文版第 25 行改回 alias；Step 3 PASS，對照頁重建，2 項待審。
- 審核通過，由 Step 7 取代原檔與它的中文版；沒有文件記錄 tools.md，[[Task 31]] 表格的草稿連結改成行內程式碼。

### 2026-10-17

- [[Task 50]] 在審核前把第 24 行的雙重否定改成肯定句，中文版跟著改。

### 2026-10-12

- 列為 [[Task 32]] 要審核的草稿之一。
