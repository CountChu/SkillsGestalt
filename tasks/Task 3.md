# Task 3 - 決定 RSDC-Skill-System-tmp 的 Dataflow 是否只留 DFD

**Status**：完成——2026-10-09 決定刪掉兩張表（Stage Read/Write Table，以及 Data Read/Write Rules 的表格），其餘三個部分保留；標準的修改併入 261010。
**Raised**：2026-10-09，檢視 RSDC-Skill-System-tmp 的 2.3 Dataflow 時提出。
**Depends on**：—

## 1. 背景

### 決定之前要知道的

問題：[RSDC-Skill-System-tmp.md](../.github/common/skills/gen-rsdc-skill/assets/RSDC-Skill-System-tmp.md) 的 2.2 Dataflow（Task 2 之前是 2.3）除了 Flowchart（DFD）與它的圖例，還有 Stage Read/Write Table、Data Read/Write Rules、Order Imposed by the Data、Exception Paths 四個部分。
DFD 已經畫出每個 stage 讀寫哪些資料，這四個部分還有存在的必要嗎？

決定之前要知道的：

- **它們是標準要求的。**
  [RSDC 標準](../.github/common/references/RSDC-Standard.md) Dataflow 的 **Required content** 第 2～5 項就是這四個部分（第 1 項是 Flowchart，第 6 項是 Draw a stage open）。
  只從範本刪掉，就是偏離標準；要刪，應該先改標準（EN 與 tw，並發一個新版本）。
  [RSDC-App-tmp.md](../.github/common/skills/gen-rsdc-app/assets/RSDC-App-tmp.md) 的 2.2 Dataflow 也有同樣這四部分，要一起決定。
- **已有前例。**
  SKILL template（[SKILL-tmp.md](../.github/common/templates/SKILL-tmp.md)）的 `# Dataflow` 已改成只有一張圖與圖例、不附表格或分段，gen-rsdc-skill 的 Step 8 與 RSDC Checker 的 `check_skill` 也跟著改了；理由是 skill 的每個 step 已經寫明它讀寫什麼。
  system 的 RSDC 沒有對應的 step 敘述，這個理由能不能套用，要另外判斷。
- **各部分有哪些內容是 DFD 畫不出來的**——刪掉之前，這些要先找到別的位置，否則就遺失：
  - **Stage Read/Write Table**：每個 stage 讀什麼、寫什麼、誰接著讀，大致都能從圖上讀出，是最可能真正多餘的一項。
  - **Data Read/Write Rules**：資料種類由形狀表示、讀寫者由線表示，可以從圖上讀出；但「是否整份寫入、寫入後是否唯讀、由誰刪除」，以及違反 one-writer 規則時的缺陷說明，圖上沒有。
  - **Order Imposed by the Data**：順序可以從資料依賴推出，但「每個順序由哪份資料造成」與 "No stage reads what a later stage writes."
    這句明確的宣告，圖上只能讓讀者自己推。
  - **Exception Paths**：什麼都沒寫就結束、中途停止、從中間某個 stage 重新進入——DFD 通常只畫正常路徑。

### 評估

評估（2026-10-09）：四個部分混著兩種內容——DFD 已經畫出的事實，與 DFD 畫不出來的規則。

| 部分 | DFD 已經畫出的 | 只有它有的 | check-stop-price 引用 |
| --- | --- | --- | --- |
| Stage Read/Write Table | 每個 stage 讀寫什麼、誰接著讀 | 沒有 | 0 |
| Data Read/Write Rules 的表格 | 種類（形狀）、寫入者與讀者（線） | 沒有 | 0 |
| Data Read/Write Rules 的性質 | — | 是否整份寫入、寫入後是否唯讀、誰刪除、one-writer 缺陷 | 2 |
| Order Imposed by the Data | 從線推得出順序 | 每個順序由哪份資料造成，與 "No stage reads what a later stage writes." 的宣告 | 1 |
| Exception Paths | 通常只畫正常路徑 | 中途停止、什麼都沒寫、從中間重新進入 | 4 |

skill 引用的全是規則（例如「Holding Judge 整份重寫 Check Table，會抹掉 back-solve 的欄位，所以每次 Step 2 之後都要重跑 Step 3」），兩張表一次也沒被引用。
重複的是兩張表，不是四個部分；這也和 SKILL template 的前例一致：誰讀寫什麼由圖說，圖說不出來的用文字寫。

## 2. 現況

做了什麼（EN 與 tw 一起改、逐行對齊）：

- **標準**（併入 261010）：Dataflow 的 Required content 從 5 項變成 4 項——Flowchart 寫明它是唯一說出誰讀寫什麼的地方，不以表格重複；Data Read/Write Rules 只留圖畫不出來的性質（整份寫入、寫入後唯讀、誰刪除）。
  Naming 一項與 261010 changelog 中的 "the diagram and its tables" 改為 "the diagram"。
  261010 開頭補一句，並新增條目 **The drawing says who reads and writes what, once.**
- **RSDC-Skill-System-tmp**（各 366 行）：刪掉 `### Stage Read/Write Table` 與 Data Read/Write Rules 的表格；Flowchart 的指示行補上「這張圖是唯一說出每個 stage 讀寫什麼的地方：每個 stage 畫成圓角框，每份資料畫成它那一種的形狀」。
- **RSDC-App-tmp**（各 329 行）：刪掉兩張表；Data Read/Write Rules 改成一段說明加三種資料的條列；"the diagram and its tables" 改為 "the diagram"。
- **RSDC Checker**（`check_rsdc.py`）：
  - stage 名稱改從 DFD 的圓角框取得（原本從 Stage Read/Write Table），`defined_terms()` 也一樣。
  - 新增兩項檢查：2.2 開頭列出的 stage 就是圖上的圓角框；圖上每個節點都是 DFD.md 五種形狀之一（取代原本的 Kind 欄檢查）。
  - 刪掉 `STAGE_HEADER`、`DATA_HEADER`、`KINDS`；範本不再需要這兩個表頭。

## 3. 要做的

### 牽涉的檔案

- **牽涉的檔案**：
  - 標準：`RSDC-Standard.md` 與 tw 的 Dataflow 一項；可能還有 [DFD.md](../.github/common/references/DFD.md)。
  - 範本：RSDC-Skill-System-tmp 與 tw 的 2.2；RSDC-App-tmp 與 tw 的 2.2。
  - RSDC Checker（`.github/common/skills/gen-rsdc-skill/scripts/check_rsdc.py`）：從範本讀取 Dataflow 的各部分標題，並比對 `STAGE_HEADER`、`DATA_HEADER`、`ORDER_SENTENCE`、`EXCEPTION_LABELS` 這些固定字串。
    「每個 stage 都有元件執行」的檢查，stage 名稱也是從 Stage Read/Write Table 取得——刪掉這張表，就要改從圖上的圓角框取得。
  - 已寫好的 RSDC 只有 InvestForge 的 `.claude/skills/check-stop-price/references/StopPriceChecker-RSDC.md`（與 tw）有這四部分；SkillCompiler-RSDC 與 Home-RSDC 都沒有。

### 留下的

留下的：

- **已寫好的文件還沒對齊**：InvestForge 的 StopPriceChecker-RSDC 與 `mods/mermaid-view/MermaidView-RSDC.md`（各與 tw）仍有兩張表，下次對齊時刪掉；在那之前，Checker 會把它們報成 Dataflow 的部分不符。
  check-stop-price 引用的三個部分都還在，只是 Dataflow 隨 Task 2 改成 2.2，它的 §2.3 引用到時要改成 §2.2。

## 4. 驗證

驗證：

- 標準與兩份範本的 EN／tw 行數相同，每行的類型與占位一致；chinese 的 parity 結果與 HEAD 相同。
- 用範本填的樣本：single PASS（29 項；唯一的警告是 Verification Obligations 沒列出樣本的元件），pair PASS（唯一的警告是樣本用英文填中文占位造成的英中相連）。
- 反向測試：圖上多一個方框節點 → FAIL；2.2 開頭列的 stage 與圖不一致 → FAIL。

## 5. 與其他 task 的關係

—

## 6. 日誌

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-09

- 提出：檢視 RSDC-Skill-System-tmp 的 Dataflow 時，問是否只留 DFD。
- 評估後決定刪掉兩張表，其餘三個部分保留；標準的修改併入 261010。
- 標準、兩份範本與 RSDC Checker 都已改。
