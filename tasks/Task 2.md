# Task 2 - 兩份 RSDC 範本的 Naming and Data Structures 對齊標準

**Status**：完成——2026-10-09 實作，連同下面「相關」的第 2 點（Optional 的 Config Schemas）；第 1、3、4 點仍未決定。
**Raised**：2026-10-09，比較 RSDC-Skill-System-tmp 與 RSDC-App-tmp 的第 2 章時提出。
**Depends on**：—

## 1. 背景

[RSDC 標準](../.github/common/references/RSDC-Standard.md)（Version 261010）把 **Naming and Data Structures** 列為第 2 章的主題之一：命名規範、metadata 的解析規則，以及 261010 加入的兩條——代碼標籤（code label）是契約、每個數字都寫明精度。
標準沒有給它省略的條件（只有 Hierarchy 有）。
另外，Dataflow 的 **Placement** 規則要求 Dataflow 排在每一個引用 stage 名稱的節之前。
兩份範本原本都沒有完全做到：

- **[RSDC-Skill-System-tmp.md](../.github/common/skills/gen-rsdc-skill/assets/RSDC-Skill-System-tmp.md)** 有 `## 2.2 Data Structures`，是從 StopPriceChecker-RSDC 的章節順序繼承來的。
  名稱少了 "Naming"；而且它排在 `## 2.3 Dataflow` 之前，Part 欄卻要寫 stage 名稱，違反 Placement 規則。
- **[RSDC-App-tmp.md](../.github/common/skills/gen-rsdc-app/assets/RSDC-App-tmp.md)** 從第一版（2026-09-24）起就沒有這一節。
  app 的資料契約分散在 2.1 Artifact Types、2.3 HTTP API 的 Takes／Answers 欄與 2.5 Config Schemas；代碼標籤與精度只是 2.1 裡的一段，命名規範與解析規則沒有位置。

## 2. 現況

### 做了什麼

做了什麼（EN 與 tw 一起改、逐行對齊）：

- **RSDC-Skill-System-tmp**（各 384 行）：
  - 第 2 章改為 2.1 Artifact Types → 2.2 Dataflow → 2.3 Naming and Data Structures → 2.4 Config Schemas（新增，Optional）→ 2.5 Derivation Rules → 2.6 Presentation Contract → 2.7 CLI → 2.8 Rule Constants → 2.9 Invariants；第 2 章開頭那句的順序跟著改。
  - **Run directory** 的定義移到 2.1 的 Terms；2.3 只留它裡面放什麼、哪些執行共用它。
  - 2.3 新增一行可省略的命名與解析規則（分隔符、日期格式、從名稱或標頭讀出的值），附上它被打破時會壞掉什麼。
  - 2.4 Config Schemas：設定檔的每個欄位、允許值與欄位之間的限制，以及檔案不符 schema 時程式怎麼做。
    **沒有 Default 欄**，依 261010 的 "No default for an input"。
  - 範本內 14 處節號引用跟著改（preamble、Rule Constants、goals 表、第 3 章開頭、3.1 的開頭、四條與指示行、第 4 章開頭）。
    3.1 指示行的 "a record of 2.2" 不改：2.2 現在是寫明每份 record 由誰寫、誰讀的 Dataflow，引用更貼切。
- **gen-rsdc-skill**：`SKILL.md` 與 `SKILL-tw.md` 各 6 行的節號——Step 2 的 "2.6 names it" → 2.7、Step 3 的 "2.1 and 2.3" → 2.2、"every term 2.1 and 2.2 define" → 2.3、Step 8 的 §2.5／§2.4／§2.3 → §2.6／§2.5／§2.2。
- **RSDC Checker**（`check_rsdc.py`）：`defined_terms()` 原本寫死 `t == 'Data Structures'`，改成同時接受 Naming and Data Structures 與舊名稱。
- **RSDC-App-tmp**（各 337 行）：在 Dataflow 之後新增 `## 2.3 Naming and Data Structures`——資料如何命名與配置、命名與解析規則，以及從 2.1 移過來的代碼標籤與精度那段，附一行列出每個欄位的代碼標籤或精度的占位。
  原 2.3～2.8 順延為 2.4～2.9，7 處節號引用跟著改。

和原提議不同的兩點：

1. 原提議說 RSDC Checker「不必改」——不對。
   不改 `defined_terms()`，改名之後它會悄悄不再讀這一節定義的術語，pair 檢查跟著變弱，卻不會報錯。
2. 原提議只要「確認」run directory 在 2.1 定義——它原本只在 Data Structures 定義，而 261010 要求 Dataflow 用到的名稱都在 Artifact Types 定義，所以要移過去。

## 3. 要做的

留下的：

- **已寫好的 RSDC 還沒對齊**：InvestForge 的 StopPriceChecker-RSDC 仍是 Data Structures 排在 Dataflow 之前（整份也還是舊格式的粗體標題），下次對齊時一起改；在那之前，Checker 會把這一節報成缺少 Naming and Data Structures。
- **兩份範本對設定預設值的處理不同**：App 範本的 Config Schemas 有 Default 欄，4.1 也寫 "Configuration defaults are 2.6's"；Skill-System 範本依 261010 不設 Default 欄。
  2026-10-10 在 [[Task 12]] 決定統一：兩份都不設 Default 欄。

**相關、尚未決定**：先前對 RSDC-Skill-System-tmp 第 2 章提過的另外 4 點對齊提議。
第 2 點已併入這次完成；其餘 3 點若要做，會再動到第 2 章，但不會再重新編號：

1. 第 2 章開頭加上標準對本章的限制：只規範「什麼」，不規範「長什麼樣子」，以及那個判準。
2. ~~新增一節 Optional 的 Config Schemas。
   ~~ 已完成（2.4）。
3. Artifact Types 的占位要涵蓋意義、目的與內容限制。
4. CLI 的每支程式加上 **Reads and writes**（指向 Dataflow）與 **Refuses**。

## 4. 驗證

驗證：

- 兩份範本 EN／tw 行數相同，標題、占位、inline code、節號引用逐行一致（App 範本有兩處引用因換行落在相鄰行，原本就如此）。
- 用新範本填了兩份樣本——保留與省略 Config Schemas——`check_rsdc.py` single 全部 PASS（30 項、0 警告），pair PASS（唯一的警告是樣本用英文填中文占位造成的英中相連）。
- gen-rsdc-skill：`check_parity.py` 0 failure，`scan_source.py` valid。

## 5. 與其他 task 的關係

—

## 6. 知識

—

## 7. 日誌

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-10

- 在 Task 12 決定兩份範本統一不設 Default 欄。

### 2026-10-09

- 提出：比較兩份範本的第 2 章時，發現 Naming and Data Structures 沒有對齊標準。
- 實作完成，連同 Optional 的 Config Schemas；其餘 3 點仍未決定。
