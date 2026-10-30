# Task 12 - 對齊 RSDC-App-tmp 與 RSDC-Skill-System-tmp 兩份範本的格式與內容

**Status**：完成——2026-10-10 兩份範本逐節對齊完畢：甲類 17 項、乙類 5 項都照建議做完，「要決定的」4 點都已決定（見下方「進度」與「結果」）。
**Raised**：2026-10-10，逐節比較兩份範本（EN，各自的 tw 行數與 EN 相同）後提出。
**Depends on**：—

## 1. 背景

兩份範本是 [RSDC-App-tmp.md](../.github/common/skills/gen-rsdc-app/assets/RSDC-App-tmp.md)（335 行，imp-app 用）與 [RSDC-Skill-System-tmp.md](../.github/common/skills/gen-rsdc-skill/assets/RSDC-Skill-System-tmp.md)（365 行，gen-rsdc-skill 用）。
兩者都依 [RSDC 標準](../.github/common/references/RSDC-Standard.md)（261010）寫，章節的大架構相同；差異分三類。

**丙、為什麼值得對齊：app 的 RSDC 目前沒有任何機械檢查**

RSDC Checker（`.github/common/skills/gen-rsdc-skill/scripts/check_rsdc.py`）從範本讀取結構，有 `--template` 參數可以指定別份範本。
2026-10-10 試著指定 RSDC-App-tmp.md，結果 exit 2：範本缺少 Checker 比對的六個固定字串——`No stage reads what a later stage writes.`、`| Claim | Rule | Proven by | Performed by |`、`| Goal | Carried by |`，以及三個 Exception Paths 標籤。
imp-app 沒有任何 RSDC 檢查腳本。
甲類中的「Exception Paths 三個標籤」「目標表表頭」「Verification Obligations 表頭」「Order Imposed by the Data 的固定句」補齊之後，同一支 Checker 就能檢查 app 的 RSDC（還需要 App 範本加上 Optional 標記與 Twin 一行，見乙）。

## 2. 現況

**甲、標準有要求，但其中一份範本沒做到（優先）**

| 項目 | App | Skill-System | 建議 |
|---|---|---|---|
| 第 1 章的限制 | 範本區塊（寫成文件時會被刪掉）裡才說「不寫元件、函式庫、route……」；第 1 章本文只有「用使用者自己的話」 | 第 1 章開頭一句：只寫目標與痛點，不碰技術、架構、檔案、程式 | App 把這句放進第 1 章本文 |
| 1.3 痛點 | 「寫成使用者的問題，不寫成缺少某個功能」——這條規則很好 | 每個障礙一條，沒有這條規則 | Skill-System 採用 App 這句 |
| 1.4 目標的名稱 | 只有固定的那條目標有粗體名稱，`___A_GOAL___` 沒有 | 每條目標是粗體短名稱加冒號，並提醒「目標表用名稱引用」 | App 改成粗體短名稱，目標表才能逐條對上 |
| 2.1 資料的種類 | 一份平的清單，沒分種類，也沒有 Terms；2.2 卻說「圖用到的其他名稱都由 2.1 定義」 | 依種類分段（external inputs／records／one-run data），再加 Terms（每個名詞只定義一次） | App 依種類分段並加 Terms |
| 第三種資料的名稱 | 「one-call data」 | 「one-run data」（標準 261008 正式定名） | **已決定（2026-10-10）**：統一成標準的 one-run data。App 範本 2.1 寫明「對 app 來說，一次執行就是一次呼叫」；tw-keep-english.md 刪掉 one-call data 一列。標準不動 |
| 2.2 的 stage 清單 | 沒有。Task 3 刪掉 Stage Read/Write Table 之後，每個 stage 做什麼只剩圖上的名稱 | 圖之前先列出每個 stage 與它做什麼，依序 | App 補上 |
| 2.2 的 Exception Paths | 一段自由文字 | 三個固定標籤：Ending with nothing written、Stopping midway、Re-entering midway（標準的三種路徑） | App 改用同樣三個標籤；它那句「什麼都不回答，也是一種回答」保留 |
| 2.2 的 DFD 缺陷 | 兩種都寫：一份 record 多個寫入者；讀了卻沒有來源的資料 | 只有「多個寫入者」，而且是可省略的段落；**沒有「資料沒有來源」** | Skill-System 補上第二種（DFD.md 的 "What Counts as a Defect" 兩種都要） |
| 2.5／2.7 Derivation Rules | 表格四欄，沒有「沒有任何來源能回答時怎麼標示」 | 每個衍生值有「沒有來源時怎麼標示」 | App 加一欄 |
| Presentation Contract 的八個問題 | 照標準全文，一題一列 | 縮寫成斜體標籤（When there is nothing to report……），標準裡的細節（例如「略過的數量在哪裡報告」）不見了 | Skill-System 改回標準的問法，或在標準裡規定縮寫的寫法 |
| Invariants | 一個占位，沒有提醒每條規則要寫壞掉時會怎樣 | 每條規則後面接「壞掉時會怎樣」 | App 補上 |
| 目標表 | 表頭是 `Goal of 1.4` 與 `Carried by` 兩欄 | 表頭是 `Goal` 與 `Carried by` 兩欄（RSDC Checker 照這個比對） | 統一，建議用 Skill-System 的 |
| 3.1 元件如何互動 | 只有 App 專屬的「Node serves and spawns; Python decides」 | 有「How they interact」與指示 | App 補上通用的互動一段，專屬那段保留 |
| 4.4 Platform Traps | 必填，占位是「規則，與教會我們這條規則的失敗」 | 可省略：標準說只記錄真的發生過的 | App 改成可省略 |
| 4.5 Verification Obligations | 以元件為列：欄位是 Component、Acceptance、Rules of chapter 2 it proves、How it is proved | 以主張為列：欄位是 Claim、Rule、Proven by、Performed by，另規定每個元件至少出現一次 | 兩種都滿足標準的兩個覆蓋要求（每條規則、每個元件），但表頭不同；選一種，或各自說明理由 |
| 第 2 章各節順序 | HTTP API、Mountable Handler 排在 Config Schemas、Derivation、Presentation Contract 之前 | 依標準列出的主題順序，介面排在 Presentation Contract 之後 | 若要依標準，App 要把 2.4、2.5 移到 Presentation Contract 之後，節號又會動（2.4→2.7 等），連同範本內的節號引用 |
| Config Schemas 的 Default 欄 | 有，4.1 也寫「設定的預設值在 2.6」 | 沒有，依 261010 的 "No default for an input" | Task 2 留下的未決問題，要和這項一起決定 |

**乙、機制與格式的不同（一旦決定方向，要一次改完）**

- **可省略的段落與指示行**：Skill-System 用 `> **Optional.**` 標出可省略的節，並用 `>` 開頭的指示行說明（寫成文件時刪掉）；App 範本沒有任何可省略的節，條件性的說明直接寫在本文。
  對照 imp-app 的 `reverse` 規則「範本有的節都寫，沒有的都不寫」，App 的每一節（包括 Mountable Handler、Config Schemas）都是必寫。
  若某些 app 沒有設定檔或衍生值，現在只能寫「沒有」。
- **圖例**：App 是固定文字；Skill-System 每個形狀一條，要換成這張圖自己的例子，不用的刪掉。
- **metadata 清單**：Skill-System 有 `Twin` 一行，連到 `X-RSDC-tw.md`；App 沒有（但 imp-app 的 SKILL.md 規定每份 app 設計文件都有 twin，兩份同時寫）。
- **版面**：App 的段落在約 100 欄折行；Skill-System 一個段落一行。
  清單符號 App 用 `-`、Skill-System 用 `*`；App 的條目用「`**名稱** —— 說明`」，Skill-System 用「`**名稱**：說明`」；表格分隔線 App 補空白對齊，Skill-System 是 `|---|`；粗體小標 App 結尾有句號（`**Guards.**`），Skill-System 沒有。
- **路徑的寫法**：App 範本區塊寫 `{skillGroups.common}` 加反斜線，Skill-System 是正斜線。

**丁、該保留的差異**

HTTP API 與 Mountable Handler（對 CLI 與 Rule Constants）；Directory Structure 與 Presentation Form（App 有，Skill-System 刻意沒有，並在第 3 章開頭說明原因）；「No LLM, anywhere」與「No tokens」只屬 Skill-System；「Opens from the hub, runs alone」（原名 Reachable from the hub as well as on its own）只屬 App；Node／Python 的限制；`Started with` 與 `Run as`。

**進度（2026-10-10）**：逐節比較、逐項由使用者決定，EN 與 tw 一起改，第 1 章到第 4 章都做完了：

- **格式**：Skill-System 的條列改成 App 的 `- **名稱** — 說明`（tw 是 `——`）；RSDC Checker 新舊兩種格式都認得，對舊格式發警告（commit 05d60f0）。
  第 1 章與第 2 章的開頭一句一行。
- **第 1 章到 1.2**：開頭三句與 1.1 對齊（commit 05d60f0）。
- **1.3**：兩份同一結構——先寫現在怎麼做、接管什麼、哪些刻意不沿用，再逐條列障礙；加一行指示：障礙寫成使用者遇到的問題，不寫成缺少某某功能。
- **1.4**：App 加上「名稱要短」的指示與粗體目標名稱，固定目標改名為 Opens from the hub, runs alone（tw：可從 hub 開啟，也能獨自執行）。
- **第 2 章開頭**：兩份都是三句——本章定義什麼、每一句都可能被推翻、指名哪些名稱（名稱是契約）。
- **2.1**：兩份都先說本節寫什麼，再定義三種資料；App 依種類分成三組（三種資料的定義從 2.2 移來），External input 加上指示與群組（位置寫成 app 的設定所指定的位置）；兩份的 External input 佔位符統一。
- **2.1 的其餘項目**：App 加上 Terms（Caller、Hub；2.5 開頭不再重述 hub 的定義）；one-run data 的第二條改名 outcome，App 的 Dataflow 開頭、DFD 節點（`{THE_OUTCOME}`）與圖例一起改；Skill-System 的 Record 佔位符改成和 App 一樣，Request 刪掉和定義重複的一句；兩份 2.1 都一句一行。
- **寫法**：兩份範本的佔位符改成 `{UPPER_SNAKE}`（見 Task 15），tw 裡佔位符和中文字之間留一個空白；Skill-System 的名稱佔位符合併成 `{SYSTEM}`，和 App 的 `{APP}` 一致；tw 裡條列名稱與說明之間寫成 ` —— `，前後各一個空白。
- **Terms 獨立成 2.1**：標準（EN、tw）第 2 章最前面加上 Terms——下面各項都依賴、卻沒有一項定義的名詞，不用任何資料的名稱，也不定義其他各項各自定義的名稱；Naming 那條改成「圖上的其他名稱在 Terms 或 Artifact Types 中定義」，changelog 併入 261010。
  兩份範本把術語從 Artifact Types 移到新的 2.1 Terms（Caller、Run directory／Hub 改寫成不用資料名稱），Artifact Types 變成 2.2，之後各節順延，Invariants 是 2.10；範本重新記錄標準的指紋（e55132878955）。
  RSDC Checker 的術語檢查多讀 Terms，節號引用認得 2.10（只有第 2 章）；gen-rsdc-skill 的 SKILL.md 裡範本節號的範例跟著改。
- **2.2–2.10**：Dataflow 列出每個 stage 與它做什麼，DFD 的指示分行、圖例每個形狀一條，App 的節點改用 caller、request、outcome；Data Read/Write Rules 的兩種缺陷（唯一寫入者、資料都有來源）兩份都有；Order 有固定句；Exception Paths 用三個標籤，各寫出 caller 收到的 outcome。
  Naming and Data Structures 的命名、欄位表（Part 欄）、代碼標籤與精度對齊。
  Config Schemas 不設 Default 欄，App 4.1 的對應例外拿掉。
  Derivation Rules 在 App 改成 Optional，每個衍生值三條（來源、絕不能代替它的、沒有來源時怎麼標示）。
  Presentation Contract 兩份都有「講清楚的事」與八個完整的問題。
  App 的 HTTP API 逐條路由寫 Takes／Answers／Refuses，加上 `/healthz` 與 Guards；Mountable Handler 一句一行。
  Invariants 每條規則寫壞掉時會怎樣，目標表是 `| Goal | Carried by |`。
- **第 2 章的順序**：App 依標準重排，HTTP API、Mountable Handler 成為 2.8、2.9，兩份共用 2.1–2.10 的節號。
- **第 3 章**：一句一行。
  標準改成 Execution Flow 排在 Directory Structure 之前（併入 261010 的 changelog），兩份共用 3.1、3.2，App 的 Directory Structure 與 Presentation Form 成為 3.3、3.4。
  3.1：App 的表格改成條列（檔案、執行的 stage、唯一的工作、邊界），加上「它們如何互動」，「Node serves and spawns; Python decides」的寫作指示移進 `>`；Skill-System tw 的「組件」改成 component。
  3.2：每個 component 一個小節，列齊分支、重試、平行處理與順序。
  3.4：加上 orphan、granting 與 constraining、只改變顯示的控制項、名稱只寫在名稱欄、Component 欄用 3.1 的名稱等指示，表頭縮短。
- **第 4 章**：開頭對齊。
  4.1 的指示改成清單（Config-driven、AI-First、輸入值沒有預設值、執行時不發出 prompt），App 的固定規則改成粗體標題句。
  4.2 的版本、函式庫、程式風格、編碼一一對應。
  4.3 加上併行寫入與輸入契約的指示。
  4.4 兩份逐字相同（Optional）。
  4.5 兩份都用 Claim、Rule、Proven by、Performed by 四欄。
  4.6 對齊。
  標準拿掉 Task Generation Logic（另一個 session 做的）。
- **範本開頭**：兩份都有 Twin 一行、Optional 的說明與正斜線的路徑；記錄的標準指紋是 `e64967b01b85`。
- **StopPriceChecker（InvestForge）**：還是舊結構，連同其他已寫好的 RSDC 移到 [[Task 18]]。

**結果（2026-10-10）**：

- 甲類 17 項、乙類 5 項都照建議做完。
- 「要決定的」4 點：
  1. 方向：App 往 Skill-System 靠；兩份共用的規則寫進標準（Terms 排最前、Execution Flow 排在 Directory Structure 之前）。
  2. RSDC Checker 讀得了 App 範本：以 App 範本為形狀檢查它自己，12 項通過，2 項失敗只是 Twin 連結的佔位符（Skill-System 範本的自我檢查也一樣）。
     讓 gen-rsdc-app 執行它，移到 Task 17。
  3. 表頭與名稱：4.5 用主張表，目標表是 `| Goal | Carried by |`，第三種資料是 one-run data。
  4. 第 2 章依標準重排，兩份共用節號。
- Task 2 留下的 Default 欄：兩份都不設，設定檔缺少的欄位回報為缺少。
- Task 14 實測留下的三個範本問題：第 3 點（4.5 每個 component 只有一列）已解，4.5 改成每個主張一列；第 1 點（Presentation Contract 沒有放「使用者必須能夠……」的地方）由 3.4 的指示把每一列接到 2.7 第 2 題的答案，2.7 沒有另加 placeholder；第 2 點（Directory Structure 列不列 `.imp-app.json`）沒有處理，留在 Task 14。

## 3. 要做的

**要決定的**

1. 往哪個方向對齊：App 往 Skill-System 靠（多數項目 Skill-System 較完整），還是兩份都往標準靠，把共同的部分寫進標準，兩份範本只留各自專屬的節。
2. 是否讓 App 範本也可被 RSDC Checker 讀取（丙）；若是，甲類的固定字串與乙類的 Optional 標記都要做。
3. 甲類的表頭與名稱（4.5、目標表、第三種資料）要選哪一種。
4. 第 2 章各節要不要依標準重排（會讓節號再動一次）。

**牽涉的檔案**

- 範本：兩份 EN 與各自的 tw（逐行對齊，行數要維持相同）。
- imp-app：`SKILL.md` 與 tw（Step 0 的版本檢查、Step 2 的「寫範本有的節」）；gen-imp-app 的 `SKILL.md`。
- RSDC Checker：`check_rsdc.py` 若要支援 App。
- 標準：只有在第三種資料的名稱走「讓標準允許」那條路時才動，要更新 changelog。
- 已寫好的 app 設計文件（例如 imp-home 的 `Home-RSDC.md` 與 tw）：範本改動後，下次對齊時要跟著改。
- 與 Task 2、Task 3 有關：兩者留下的「Default 欄」與 stage 清單問題在這裡一併處理。

暫時的傾向（尚未決定）：先做甲類（這些是標準的要求），方向是 App 往 Skill-System 靠，再看要不要做乙類與 Checker 的支援。

## 4. 驗證

- 驗證：兩份範本 EN 與 tw 的 `check_parity.py` 都是 0 failure，`check_rsdc.py --standard` PASS，`depends_on.py check` 全部 UNCHANGED。

## 5. 與其他 task 的關係

後續工作另開 [[Task 17]]（gen-rsdc-app 與 imp-app 跟上範本、執行 RSDC Checker）與 [[Task 18]]（已寫好的 RSDC 跟上範本）。

## 6. 日誌

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-10

- 提出：逐節比較兩份範本後，列出甲、乙、丙、丁四類差異。
- 逐節對齊兩份範本，EN 與 tw 一起改，第 1 章到第 4 章都做完。
- 甲類 17 項、乙類 5 項都做完，「要決定的」4 點都已決定。
