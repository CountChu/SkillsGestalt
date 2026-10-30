# Task 48 - 把中文版裡指 term 的「術語」改成 term

**Status**：完成——2026-10-16 建立，同日在建立它的 session 做完：22 份中文版、88 處「術語」改成 term；`scan_md.py` 讀清單時跳過 term 那一列的問題，2026-10-18 修好。
**Raised**：2026-10-16，[[Task 32]] 審 tw-keep-english 的草稿（2.3）時，使用者決定把 term 加進 keep-English list；清單加上一列之後，其他中文版裡指 term 的「術語」要改成 term，使用者決定這次一起改。
**Depends on**：—

## 1. 背景

[[Task 43]] 把 technical term 改稱 term，中文本來寫「術語」；之後 chinese skill 依它的 glossary、tw-keep-english 的中文版也寫 term，其他中文版仍寫「術語」。
[[Task 32]] 2.3 第七輪把 term 加進 keep-English list（Replaces 與 Flagged 都是「術語, 技術詞」），清單換成 261016：從此每一份中文版都保留英文的 term，`check_parity.py --keep` 會在「術語」的地方警告。

## 2. 現況

### 已決定（2026-10-16）

- 這次一起改，不留給之後。
- 規則和先前 role、system 的轉換相同：只改英文對應行（逐節對應的中文版則是那一節）寫 term 或 terms 的地方；英文寫 terms 時也寫原形 term；中英文之間留半形空格，全形標點前後不留。
- 不改：「術語表」（glossary 的譯法，另外處理）；英文本身寫著「術語」的行（清單表格裡列的譯法）。
- 提交：commit 前綴 `task 48`，SkillsGestalt 與 InvestForge 各一個；InvestForge 只提交改到的行，別的 session 的修改不動。

### 盤點（2026-10-16）

- 26 份中文版有「術語」，共 102 處：13 處是「術語表」，另 89 處的英文寫 term 或 terms；英文本身寫「術語」的 6 處都在「術語表」裡。
- 要改的 23 份：SkillsGestalt 18 份（RSDC-Standard、兩份 RSDC 範本、SKILL 範本與它的草稿、skill-writing 與它的草稿、tools 的草稿、check-skill 的 SKILL 與 checking-criteria、asd-ste、check-md-deps、chinese、compile-skill、gen-rsdc-skill、gen-skill、imp-home 的 SKILL，以及 MermaidView-RSDC），InvestForge 5 份（check-stop-price 的 SKILL 與 StopPriceChecker-RSDC、extract-filled-orders、imp-inv-tech-rank、select-stocks 的 SKILL）。
- 先不改：MermaidView-RSDC-tw.md 第 100 行的粗體標籤「**術語**」——英文是舊格式的標籤「**Terms**」，寫成「**term**」不像標籤；[[Task 46]] 已決定這份設計文件的標籤先不動，等決定英文標籤時一起處理。

### 結果（2026-10-16）

- 22 份中文版、88 處改成 term，共 77 行；這些檔案剩下的「術語」都在「術語表」裡。
- 只有一處要手補空格：checking-criteria-tw.md 的「該 term **意義相同**」，term 後面接粗體記號，轉換時沒補到；`check_parity.py` 報出來之後補上。
- 每一對 `check_parity.py` 的 failure 與警告都和改之前相同；check-stop-price 那一對原本就有 1 個 failure（glossary term 的粗體次數），不是本 task 造成的。
- StopPriceChecker-RSDC 與 InvCov-RSDC 的 `check_rsdc.py` 中英對照都 PASS，警告和之前相同。
- 一句一行：SkillsGestalt 的 17 份都沒有變動；InvestForge 的 5 份改之前就不是一句一行，不在本 task 範圍。

### 發現的問題（2026-10-16）

- chinese skill 的 `scan_md.py` 的 `keep_english()` 把第一格是 term 的列當成表頭（`cells[0].lower() == "term"`），所以清單新加的 term 那一列沒有被讀到：`check_parity.py --keep` 不會在「術語」的地方警告，chinese skill 的 Step 1 也不會把 term 列進要保留英文的詞。
- `check_rsdc.py` 的 `flagged_renderings()` 用大小寫區分的 `Term` 判斷表頭，讀得到這一列。
- 2026-10-18 修好：使用者決定認表頭時，第一格要是 Term、第二格要是 Replaces，兩格都符合才算表頭，term 那一列就照常讀進來，清單共 75 列。
  兩個 repo 的 69 對中英對照，修好前後只有 6 對的 `check_parity.py --keep` 多了警告：清單自己的中文版（表格的 term 與 glossary 兩列）、skill-writing、tools、compile-skill、gen-rsdc-skill 的「術語表」，以及先不改的 MermaidView 標籤，都在預期之內；failure 都沒有變。

## 3. 要做的

1. 照上面的規則改 22 份、88 處。
2. 每一對中英對照跑 `check_parity.py --keep`，和改之前比；RSDC 與範本的中文版另跑 `check_rsdc.py` 的中英對照，看共用句子的寫法。
3. 提交兩個 repo。

## 4. 驗證

- 每一對 `check_parity.py` 都是 0 failure；「術語」的警告消失，沒有新的警告。
- 中文版都是一句一行。

## 5. 與其他 task 的關係

- [[Task 32]]：2.3 第七輪把 term 加進清單，本 task 改其他中文版。
- [[Task 43]]：把 technical term 改稱 term。
- [[Task 46]]：MermaidView-RSDC 的「**Terms**」標籤先不動，本 task 的那一處也跟著它。

## 6. 日誌

### 2026-10-18

- 修好 `scan_md.py` 讀清單表頭的方式：第一格 Term、第二格 Replaces 才算表頭，term 那一列讀得到了；69 對中英對照比過，多出來的警告都在「術語表」與清單自己的表格。

### 2026-10-16

- 建立：決定這次一起改，規則同 role、system 的轉換，「術語表」與 MermaidView 的標籤先不動。
- 做完：22 份、88 處；`check_parity.py` 與 `check_rsdc.py` 的結果都和改之前相同。
  發現 `scan_md.py` 讀清單時跳過 term 那一列，記在「現況」一章，待決定。
