# Task 5 - 將兩份 RSDC 範本第 2 章的 Flowchart 改稱 DFD

**Status**：完成——2026-10-09 照評估實作：Dataflow 的第一部分改稱 DFD（標準併入 261010），RSDC Checker 改成依圖、而不是依名稱找。
**Raised**：2026-10-09，檢視兩份範本的 Dataflow 時提出。
**Depends on**：—

## 1. 背景

提議：RSDC-Skill-System-tmp 與 RSDC-App-tmp（EN 與 tw 都改）第 2 章的 Dataflow 裡，把名為 **Flowchart** 的部分改稱 **DFD**。
那張圖本來就是 DFD（標準與 [DFD.md](../.github/common/references/DFD.md) 都這麼說），"Flowchart" 這個名稱容易讓人以為是一般流程圖。

### 評估

評估（2026-10-09）：**值得改**，但 RSDC Checker 要一起改成不依賴名稱。

- **名稱說錯了圖的種類。**
  這張圖是 DFD：標準說 Dataflow "is drawn as a DFD"，[DFD.md](../.github/common/references/DFD.md) 開頭就是 "A DFD — data flow diagram — is how every flow in these documents is drawn"，圖例講的也是 DFD 的形狀與線。
  flowchart 一般指控制流程圖——接下來做什麼、在哪裡分岔——而不是資料往哪裡流。
  這個名稱多半是從 mermaid 的語法 `flowchart TB` 帶過來的。
- **在 MermaidView-RSDC 已經造成混淆。**
  那份設計的主題就是 mermaid 的 flowchart（它追蹤 flowchart 的節點），文件裡三十幾處 "flowchart" 都指它處理的圖；第 125 行它自己的 Dataflow 部分也叫 Flowchart，讀者分不出哪一個是設計本身的圖。
- **成本低。**
  標準與兩份範本各一兩處；同一天的修改併入 261010（Task 4 定下的做法），範本記的版本不必改。
- **要一起處理的風險。**
  RSDC Checker 寫死 `'Flowchart' in part_at`（現在是第 499 行）：只改名稱，圖的每一項檢查——圓角框、hexagon、節點形狀、藍線、圖例，以及 Task 3 之後從圖取得 stage 名稱的「每個 stage 都有元件執行」與 stage 清單比對——都會悄悄跳過，不報錯。
  不要只把字串換成 `'DFD'`：改成找 Dataflow 裡的第一張 mermaid 圖、找不到就 FAIL，日後再改名，檢查也不會靜默失效。

## 2. 現況

### 做了什麼

做了什麼（2026-10-09，照上面的建議；EN 與 tw 一起改、逐行對齊）：

- **標準**（併入 261010）：Required content 第 1 項改為 **DFD**，寫成 "the diagram of the stages"，避免「DFD：一張 DFD」；261010 開頭補半句，並新增條目 **The diagram is called a DFD.**
- **RSDC-Skill-System-tmp**：`### Flowchart` → `### DFD`；Execution Flow 指示行的 "a flowchart in the notation of the DFD" → "a DFD"（tw「一張 DFD 記法的 flowchart」→「一張 DFD」）。
- **RSDC-App-tmp**：`**Flowchart.**`／`**Flowchart。**` → `**DFD.**`／`**DFD。**`。
- **RSDC Checker**：圖改成「Dataflow 裡的第一張 mermaid 圖」，找不到就 FAIL（新的檢查 "the Dataflow holds its DFD"）；圖例在圖所在的那一部分裡找；訊息裡的 flowchart 改成 DFD，`check_skill` 的兩則也一樣。
  跳過 mermaid 關鍵字的兩處（那裡的 `flowchart` 是語法）不改。

## 3. 要做的

### 要改的地方

要改的地方（2026-10-09 搜尋的結果）：

- **[RSDC-Skill-System-tmp.md](../.github/common/skills/gen-rsdc-skill/assets/RSDC-Skill-System-tmp.md)**：第 93 行的 `### Flowchart` 小節標題；tw 檔同一行，標題兩邊要逐字相同。
- **[RSDC-App-tmp.md](../.github/common/skills/gen-rsdc-app/assets/RSDC-App-tmp.md)**：第 67 行的粗體小標 `**Flowchart.**`；tw 檔是 `**Flowchart。**`。
- **標準**：[RSDC-Standard.md](../.github/common/references/RSDC-Standard.md) 第 40 行 Dataflow 的 Required content 第 1 項就叫 **Flowchart**（"a DFD of the stages"），tw 同一行。
  範本只改不動標準，兩邊的名稱就不一致；建議標準一起改，並發一個新版本、在 "Changes in This Version" 記下。
- **RSDC Checker**（`.github/common/skills/gen-rsdc-skill/scripts/check_rsdc.py`）：第 494 行寫死 `'Flowchart' in part_at`，Dataflow 的部分名稱雖然從範本讀取（`DATAFLOW_PARTS`），這一處沒有。
  只改範本不改這裡，圖的檢查（hexagon、圓角框、節點形狀、藍線、圖例）會悄悄全部跳過，卻不報錯；而且 Task 3 之後 stage 名稱也從這張圖取得，「每個 stage 都有元件執行」與 stage 清單的比對也會跟著跳過。
  同檔第 490～509 行的註解與訊息文字也提到 flowchart，可一起改（2026-10-09 Task 3 完成後的行號）。
- **已寫好的 RSDC**：InvestForge 的 `StopPriceChecker-RSDC.md` 與 tw 各有 1 處 Flowchart，下次對齊時一起改；在那之前，Checker 會報 Dataflow 沒有這一部分。
- **不用改**：mermaid 程式碼裡的 `flowchart TB` 是 mermaid 的語法，不是名稱；`check-wiki-doc`、`check-skill` 的腳本只是跳過 mermaid 的關鍵字。
  範本 3.2 Execution Flow 指示行的 "a flowchart in the notation of the DFD" 是一般用語，可順手改成 "a DFD"。

### 更新後的範圍

更新後的範圍（2026-10-09 重新搜尋；上面列的行號有幾處已因 Task 3、4 與第 3、4 章對齊而移動）：

- **標準**：RSDC-Standard.md 與 tw 第 40 行 Required content 第 1 項。
  改名時要改寫 "a DFD of the stages"，免得寫成「DFD：一張 DFD」。
- **RSDC-Skill-System-tmp** 與 tw：第 93 行 `### Flowchart`；第 303 行 Execution Flow 指示行的 "a flowchart in the notation of the DFD" → "a DFD"。
- **RSDC-App-tmp** 與 tw：第 67 行 `**Flowchart.**`／`**Flowchart。**`。
- **RSDC Checker**：第 495～514 行（找圖的方式、註解與訊息）；第 889、892 行 `check_skill` 訊息裡的 "the skill's flowchart" 可一起改成 DFD。
  第 246、291 行是跳過 mermaid 關鍵字，不改。
- **已寫好的文件**（下次對齊時改）：StopPriceChecker-RSDC 與 tw 第 161 行、MermaidView-RSDC 與 tw 第 125 行的 `#### **Flowchart**`。
  MermaidView-RSDC 第 312 行的 "The Graph of a Flowchart" 與其他提到 flowchart 之處，說的是它處理的 mermaid 圖，不改。
  其他寫好的 RSDC（Home、SkillCompiler、EvernoteCli、InvestForge 的十幾份）都沒有這個部分名稱。
- **可順手改**：check-skill 的 `checking-criteria.md` 第 108 行 "drawn as a mermaid flowchart" 指的是 mermaid 的圖種，不算錯，可改成 "drawn in mermaid as a DFD"。
- **不屬於本項**：check-stop-price 的 `SKILL.md` 與 tw 的 `## Flowchart`，是 skill 自己舊格式、分成幾部分的 Dataflow；SKILL template 現在只要一張圖，gen-rsdc-skill 的 Step 9 重新產生它時就會消失。

### 建議的做法

建議的做法：名稱用 **DFD**（DFD.md 的標題，也是全 repo 的用語）；標準併入 261010，在 changelog 加一條；Checker 改成依圖而不是依名稱找；EN 與 tw 一起改。

### 留下的

留下的：

- **已寫好的文件**：StopPriceChecker-RSDC 與 tw 第 161 行、MermaidView-RSDC 與 tw 第 125 行的 `#### **Flowchart**`，下次對齊時改成 DFD；在那之前，Checker 會把 StopPriceChecker-RSDC 報成 Dataflow 的部分不符，但圖本身照樣被檢查。
- **沒做的順手改**：check-skill 的 `checking-criteria.md` 第 108 行 "drawn as a mermaid flowchart"——屬於另一個 skill，說的也是 mermaid 的圖種，不算錯；留給 check-skill 自己的修改。

## 4. 驗證

驗證：

- 標準 148 行、Skill-System 範本 366 行、App 範本 329 行，EN／tw 每行類型一致、標題相同；chinese 的 parity 結果與 HEAD 相同。
- 用範本填的樣本：single PASS（29 項）、pair PASS（13 項），唯一的警告與之前相同。
- 反向測試：只有文件改掉部分名稱 → 部分順序 FAIL，圖的檢查照跑；拿掉圖 → FAIL；範本與文件都改成別的名稱、Checker 不動 → 圖的檢查仍全部執行，原本的靜默跳過不會再發生。

## 5. 與其他 task 的關係

—

## 6. 日誌

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-09

- 提出：檢視兩份範本的 Dataflow 時，發現 Flowchart 這個名稱說錯了圖的種類。
- 評估後決定把名稱改為 DFD，RSDC Checker 改成依圖、而不是依名稱找圖。
- 實作完成：標準、兩份範本與 RSDC Checker 都已改。
