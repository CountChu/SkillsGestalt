# Task 32.3 - tw-keep-english

**Status**：完成——2026-10-18 第八輪通過，同日由 Step 7 取代原檔。
**Raised**：2026-10-12，[[Task 32]] 提出時列出的草稿之一，原本是它要做的 2.3。
**Depends on**：—

## 1. 背景

審核 [[Task 31]] 為 [tw-keep-english.md](../.github/common/references/tw-keep-english.md) 產生的 STE 草稿與草稿中文版；通過就由 asd-ste 的 Step 7 取代原檔與它的中文版。
分工、取代的方式與「每取代一份要一併做的」，見 [[Task 32]]。

## 2. 現況

### 審核時決定的

- **tw-keep-english 的分工**：The list 開頭的兩句改寫成 Replaces 與 Flagged 的分工，四份一起改。
  Replaces 列出譯者可能寫的每一種譯法，給譯者與審核的人看；Flagged 是其中由工具（chinese skill 的 `check_parity.py --keep` 與 gen-rsdc-skill 的 `check_rsdc.py`）在正文裡搜尋、找到就警告的譯法。
  本身也是一般用語的譯法會誤報，只留在 Replaces，Flagged 寫「—」；找到的是 WARN 不是 FAIL，由人判斷。
  照這條分工，system 那一列的 Flagged 改成「—」：「系統」會在「作業系統」誤報。

### 進度

- tw-keep-english：2026-10-18 對照頁 29 項全部通過，同日由 Step 7 取代。
  `draft.py replace` 把草稿與它的中文版寫回 tw-keep-english.md 與 tw-keep-english-tw.md，檔頭註記刪成兩行，再刪掉兩份草稿；header quote 的 Version 仍是 261016。
  `draft.py dependents` 以本 workspace、InvestForge 與 BookMaster 為 root，沒有文件記錄 tw-keep-english.md；`check_parity.py --keep` 與 `check_rsdc.py --keep` 是以路徑讀它的表格。
  檢查：`check_ste.py --ste` PASS，仍是 op 那一則警告；parity check 0 failure；檔頭的 `depends_on.py check` 都是 UNCHANGED；`check_rsdc.py` 讀得到表格的 94 個 Flagged 譯法，包括新加的「術語」。
  task-31 表格指向草稿的連結改成行內程式碼，並註明已取代；chinese skill 的 `scan_md.py` 讀不到 term 那一列，由 [[Task 48]] 修。

### 審核紀錄

- 2.3 ✅ tw-keep-english——2026-10-18 第八輪通過；對照頁 2026-10-14 送審；標題的 list（The list）判定保留，照常列在 Technical words。
  同日由 [[Task 43]] 把 technical term 改稱 term：原文與草稿一起改，草稿重跑 Step 3 PASS，對照頁加第 8 項說明後重建，已通過的檔頭那一項維持通過。
  同日再由 Task 43 在 The rule 的第一句補上 term 的定義，兩份中文版指 term 的地方都寫 term；草稿重跑 Step 3 PASS，第 8 項改寫並分成四個子項，對照頁重建，檔頭那一項維持通過。
  2026-10-16 再檢查一次：說明的 108 個行號都指到對的行，`check_ste.py` PASS，兩對 `check_parity.py` 0 failure，草稿檔頭的紀錄都是 UNCHANGED。
  第 8 項加了兩個待審的子項：term 保留英文、清單卻沒有 term 這一列（列出三種做法與影響），以及草稿的 term 定義可能改了意思（建議改成 the same type of item）；第 3 個子項的「術語」更正為「技術詞」，最後一個子項註明版本要和第 3 點一起決定；對照頁重建，共 29 項、115 個行號，檔頭那一項維持通過。
  第二輪（同日）：第 2 項（標題的 list）與第 3 項的三個子項標 `[?]`，解釋之後決定：list 保留、Version 行照 House Rule 7 的寫法，兩項不改；換版本比照 RSDC-Standard，只有改規則或清單才換，Task 43 不算改規則，版本維持 261013。
  草稿第 18 行改成「Only a change to a rule or to the list makes a new version, and the Version line shows the new version.」，第 20 行新增「When a change does not change a rule or the list, the version stays the same.」，this line 也因此改成直接寫 the Version line；原文照舊，由 Step 7 取代時換掉。
  草稿中文版照 chinese skill 只改這兩行，`check_parity.py` 0 failure，`diff_md.py --verify` PASS；Step 3 重跑 PASS，仍只有 op 那一則警告。
  對照頁的行號自動對到新位置，第 3 項的兩個子項、中文的版本行與第 8 項最後一個子項註明第二輪的結果，回到待審；共 29 項、120 個行號，檔頭那一項維持通過。
  第三輪（同日）：第 3 項第 1 個子項與第 8 項第 2 個子項標 `[?]`；解釋時使用者決定把版本寫進 header quote，另開 [[Task 45]] 做。
  原文、草稿與兩份中文版的版本都移到 header quote 的第一行 `> Version: 261013`，草稿不再需要 House Rule 7 的長句，原文第 8 行的 this line 改成 the Version line at the head of this file；草稿重跑 Step 3 PASS。
  對照頁重建：版本那幾項與檔頭改寫成第三輪的結果；header 多了一行，幾乎每一項的行號都移動，所以 29 項全部回到待審，之前通過的 8 項要重新看過。
  第 8 項第 2 個子項（term 的定義）已經解釋，還沒決定要不要改成 the same type of item。
  第四輪（同日）：上面兩項仍是 `[?]`；版本那一項第三輪已解決，term 的定義決定照建議改。
  草稿第 24、26 行改成 the same type of item，中文版寫「一律指同一類項目」；原文第 11 行不動，和 chinese skill 的 glossary 維持同一句。
  草稿中文版照 chinese skill 只改這兩行，`check_parity.py` 0 failure，`diff_md.py --verify` PASS；Step 3 重跑 PASS，仍只有 op 那一則警告。
  對照頁重建：第 8 項第 2 個子項補上哪幾個字不在字典裡、各換成什麼，「定義的意思可能變了」那一項註明第四輪已改；共 29 項、127 個行號，都在待審。
  第五輪（同日）：第 5 項的三個子項標 `[?]`，解釋之後決定都照建議改；討論第一個子項時開出 [[Task 46]]，把 RSDC 的 Terms 改名為 Terminology。
  草稿第 38 行改成「the rules of that document keep the term in English」，第 62 行改成「A rendering that usually identifies the term can also identify a different item, in a sentence about that item.」，第 147 行拿掉 many；中文版的三行跟著改。
  草稿中文版照 chinese skill 只改這三行，`check_parity.py` 0 failure，`diff_md.py --verify` PASS；Step 3 重跑 PASS，仍只有 op 那一則警告。
  對照頁重建：這三項與中文第 2 項對應的三個子項註明第五輪已改，回到待審；共 29 項、135 個行號，10 項維持通過。
  第六輪（同日）：第 8 項第 2 個子項（term 的定義）標 `[?]`；使用者提議把 phrase 收進 ste-custom，另開 [[Task 47]] 做。
  phrase 成了專案核准詞，草稿與 RSDC-Standard 的 Technical words 都拿掉它；草稿第 24 行改回「a word or a phrase」，中文版寫「詞或片語」；7 份草稿重跑 Step 3 PASS。
  對照頁重建：第 8 項第 2 個子項更正 phrase 的說法（它本來就列在 Technical words），「定義的意思可能變了」那一項註明第六輪已改；共 29 項、140 個行號，15 項維持通過。
  第七輪（同日）：第 8 項的「term 不在清單上」與「版本維持 261013」標 `[?]`；解釋之後使用者照建議選做法（1），把 term 加進清單。
  原文、草稿與兩份中文版的表格在 template 之後加上 term 一列：Replaces 與 Flagged 都是「術語, 技術詞」，Why 欄照 script、template 的寫法；清單改了，所以版本換成 261016，ste-rules.md 拿 261013 當例子的地方不改。
  草稿重跑 Step 3 PASS，仍只有 op 那一則警告；兩對中英對照 `check_parity.py` 0 failure，`diff_md.py --verify` PASS。
  對照頁重建：兩項 `[?]` 與提到版本號的兩項註明第七輪的結果；表格多了一列，幾項的行號跟著移動，共 29 項、146 個行號，12 項維持通過。
  其他 23 份中文版裡指 term 的「術語」，由 [[Task 48]] 改成 term。
  第八輪（2026-10-17）：中文第 148 行那一項標 `[?]`；解釋之後使用者決定中文的「不正確的警告」改成「誤報」，並由 [[Task 49]] 把 false 與 false alarm 收進 ste-custom。
  草稿第 59、148 行的 incorrect warnings 換成 false alarms，和原文第 114 行同一個說法；中文版第 148 行照英文句式寫成「工具可以在 twin 中檢查其中一些譯法，而不會誤報」，第 59 行寫成「能讓工具檢查正文而不誤報」。
  7 份草稿重跑 Step 3 PASS，兩對中英對照 `check_parity.py` 0 failure，`diff_md.py --verify` PASS。
  對照頁重建：這一項與英文第 5 項第 2 個子項註明第八輪已改；共 29 項、151 個行號，26 項維持通過。
  解釋第八輪時，使用者問 STE 有沒有禁止雙重否定；Issue 9 沒有這一條，由 [[Task 50]] 在 ste-custom.md 加上 Rules 一章，第一條就是不用雙重否定。
  2026-10-18 使用者說審完了：29 項都算通過（中文第 148 行那一項第八輪改過之後沒有再點 `[v]`，使用者說算通過），同日由 Step 7 取代原檔。
  這份草稿沒有雙重否定的警告，Step 3 PASS；對照頁因檔頭的紀錄重建，項目與狀態和第八輪相同。

## 3. 要做的

—

## 4. 驗證

—

## 5. 與其他 task 的關係

- [[Task 43]]：2026-10-14 審 tw-keep-english（2.3）時開出——technical term 改稱 term，STE customization 改稱 project-approved word。
  它改到 tw-keep-english 的草稿；ste-custom.md 一改，宣告它的草稿都要重跑 Step 3，包括正在審的 report-md-rules（2.5）；同日都已做完。
- [[Task 45]]：2026-10-16 審 tw-keep-english（2.3）時開出——版本寫進 header quote 的第一行，同日做完；2.3 的原文、草稿與兩份中文版一起改，RSDC-Standard 也改了。
- [[Task 46]]：2026-10-16 解釋 2.3 第 5 項第 1 個子項（glossary 那一句）時開出——RSDC 第 2 章的 Terms 改名為 Terminology，RSDC-Standard 換成 261016，同日做完；那一項的措辭另外處理。
- [[Task 47]]：2026-10-16 審 2.3 第 8 項第 2 個子項時開出——phrase 收進專案核准詞，同日做完；宣告 `[[ste-custom]]` 的草稿都重跑了 Step 3，2.5 等其他草稿的對照頁下次 `run step 6` 時更新。
- [[Task 48]]：2026-10-16 2.3 第七輪把 term 加進清單之後開出——其他中文版裡指 term 的「術語」改成 term，同日做完。
- [[Task 49]]：2026-10-17 審 2.3 中文第 148 行時開出——false 與 false alarm 收進專案核准詞，同日做完。
- [[Task 50]]：2026-10-17 解釋 2.3 第八輪時開出——ste-custom.md 分成 Words 與 Rules，第一條規則是不用雙重否定，同日做完；tools 的草稿（2.9）第 24 行因此改成肯定句，2.5 的對照頁下次 `run step 6` 時更新。

## 6. 知識

—

## 7. 日誌

### 2026-10-18

- 從 [[Task 32]] 拆出：原本是它要做的 2.3；屬於這份檔案的內容搬到這裡，內容沒有改。
- tw-keep-english（2.3）✅：使用者說審完了，29 項都算通過；Step 7 取代原檔與中文版，沒有文件記錄它，`check_ste.py --ste` PASS，parity 0 failure；Task 31 指向草稿的連結改成行內程式碼。

### 2026-10-17

- tw-keep-english（2.3）第八輪：草稿寫 without false alarms，中文版寫「誤報」；false 與 false alarm 由 [[Task 49]] 收進專案核准詞；Step 3 PASS，對照頁重建。

### 2026-10-16

- tw-keep-english（2.3）再檢查一次：機械檢查都通過；對照頁第 8 項加上兩個子項（term 不在清單上、term 定義的用字），更正兩處說明，對照頁重建。
- tw-keep-english（2.3）第二輪：四項 `[?]` 解釋之後，草稿與中文版的版本規則改成只有改規則或清單才換版本，並直接寫 Version 行；Step 3 PASS，對照頁重建。
- tw-keep-english（2.3）第三輪：版本由 [[Task 45]] 移進 header quote，原文、草稿與兩份中文版一起改；Step 3 PASS，對照頁重建，29 項回到待審。
- tw-keep-english（2.3）第四輪：草稿的 term 定義改成 the same type of item，中文版寫「一律指同一類項目」；Step 3 PASS，對照頁重建。
- tw-keep-english（2.3）：第 5 項的三個子項標 `[?]`，已解釋；討論第一個子項時開出 [[Task 46]]，三項的措辭都還沒改。
- tw-keep-english（2.3）第五輪：第 5 項的三個子項照建議改（glossary 的 term 保留英文、Flagged 不能誤報、譯法也可能指別的東西）；Step 3 PASS，對照頁重建。
- tw-keep-english（2.3）第六輪：phrase 由 [[Task 47]] 收進專案核准詞，草稿的定義改回「a word or a phrase」；Step 3 PASS，對照頁重建。
- tw-keep-english（2.3）第七輪：清單加上 term 一列，版本換成 261016；Step 3 PASS，對照頁重建。

### 2026-10-14

- 對照頁送審。

### 2026-10-12

- 列為 [[Task 32]] 要審核的草稿之一。
