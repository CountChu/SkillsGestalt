# Task 4 - 為 RSDC-Responsibilities 改一個較短的名稱

**Status**：完成——2026-10-09 改名為 `RSDC-Standard.md` 與 `RSDC-Standard-tw.md`，併入版本 261010。
**Raised**：2026-10-09，認為 `RSDC-Responsibilities` 這個檔名太長時提出。
**Depends on**：—

## 1. 背景

候選名稱（英文檔與 twin 一起改，例如 `RSDC-Standard.md` 與 `RSDC-Standard-tw.md`）：

1. **RSDC-Standard**（推薦）：每個 skill 的字彙表本來就稱它為 **RSDC standard**，檔名與術語一致；也和兩份範本 `RSDC-App-tmp`、`RSDC-Skill-System-tmp` 的「RSDC-<種類>」命名一致。
2. **RSDC-Chapters**：直接說出內容——四個 chapter 各自的職責；但它也規範寫作原則與 Dataflow，名稱涵蓋不到。
3. **RSDC-Rules**：很短，但第 2 章的問題就是 "What are the system rules?"，每份 RSDC 都在談 rules，容易混淆。
4. **RSDC**：最短，但每份 RSDC 文件都命名為 `<system name>-RSDC.md`，`RSDC.md` 看起來像又一份 RSDC，而不是它們的標準。

標題 `# ArtifactFlowAgent: The Responsibilities of the Four RSDC Chapters` 不必跟著改，可以一起決定。

改名前要知道的：

- **標準承諾過檔名不變。**
  它寫明 "the file name stays as it is, so nothing that cites this document has to change with it"。
  改名就是破例一次：要在 "Changes in This Version" 記下新舊檔名並發一個新版本，舊名稱的引用要一次全部改完。
- **要改的引用**（2026-10-09 搜尋的結果）：
  - 標準本身與 twin：第 3 行互相連結。
    261008 的 changelog 提到 twin 的舊檔名，那是歷史紀錄，可以保留。
  - [DFD.md](../.github/common/references/DFD.md) 與 tw：各 2 處連結。
  - 兩份範本與 tw：每份寫成的文件都會保留的 wiki link `> [[RSDC-Responsibilities]]`，以及範本區塊中的路徑。
    RSDC Checker 從範本讀取要保留的 wiki link，範本一改，Checker 就會要求新名稱。
  - skill：gen-rsdc-skill（`SKILL.md` 的 description、字彙表、CONFIGURATION、Step 0，與 tw）、imp-app（CONFIGURATION、Step 0，與 tw）、gen-imp-app（CONFIGURATION）、imp-home（CONFIGURATION，與 tw）。
  - 已寫好的文件：`mods/mermaid-view/MermaidView-RSDC.md` 與 tw 第 631 行（敘述當初依哪份標準寫成，屬歷史敘述）；EvernoteCli workspace 的 `docs/EvernoteCli-RSDC.md` 與 tw 第 3 行（「遵循 RSDC-Responsibilities.md」，要改）。
  - InvestForge 的 memory：`upper-lower-documents.md`。
  - 這份 tasks.md 的 Task 2、Task 3 也提到它。

## 2. 現況

做了什麼（2026-10-09，採用推薦的 **RSDC-Standard**；標題 `# ArtifactFlowAgent: The Responsibilities of the Four RSDC Chapters` 不變）：

- **檔案**：`git mv` 成 `RSDC-Standard.md` 與 `RSDC-Standard-tw.md`；兩份第 3 行的互相連結改為新檔名。
- **版本**：沒有另發 261011，而是併入 261010——同一天的修改都併入同一個版本（Task 3 也是這樣做的），版本號才不會比日期跑得更前面；兩份範本記的版本因此不必改。
  261010 的開頭補一句，並新增條目 **The file is renamed.**：寫明新舊檔名、規則沒有改變，以及這是「檔名不變」那條規則唯一的一次例外。
- **repo 內的引用**（13 個檔案）：DFD.md 與 tw 各 2 處連結；兩份範本與 tw 的 wiki link（`> [[RSDC-Standard]]`）與範本區塊中的路徑；gen-rsdc-skill 的 `SKILL.md` 與 tw 各 4 處、imp-app 各 2 處、gen-imp-app 1 處、imp-home 各 1 處。
- **repo 外的引用**：EvernoteCli 的 `docs/EvernoteCli-RSDC.md` 與 tw 第 3 行（那個 repo 原本就有其他未 commit 的修改，這次只動這一行，沒有 commit）；InvestForge 的 memory `upper-lower-documents.md`，標準的路徑改為新名稱，歷史敘述處註明改名。
- **tasks.md**：Task 2、3、5、7 指向標準的連結與路徑改為新檔名；這一項保留舊名稱，因為它記錄的就是改名本身。

沒有改的——舊名稱只留在記錄過去的地方：

- 標準 261008 的 changelog（twin 當時的檔名）。
- `mods/mermaid-view/MermaidView-RSDC.md` 與 tw 第 631 行（當初依哪份標準寫成）。
- Obsidian vault 裡的副本與記錄：`CountChuObs/2.2 Areas - 創造 - Import/` 的 EvernoteCli-RSDC 與 tw（匯入的副本），`GeminiOrganizedChats` 的幾份對話記錄；以及 Claude 的 session 記錄。

搜尋範圍：repo 全部；repo 外以檔名找出的 46 份 `*RSDC*.md`、`CLAUDE.md`／`AGENTS.md`，以及所有 Claude memory。
對整個 Dropbox 的內容搜尋沒有跑完——為了不觸發雲端檔案下載而中止——所以 Dropbox 裡不屬於上述檔名的檔案若提到舊名稱，可能還沒找到。

## 3. 要做的

—

## 4. 驗證

驗證：

- 標準、DFD、兩份範本的 EN／tw 行數相同；標準相對 HEAD 只改了第 3 行、261010 的開頭與新條目。
- 用 Skill-System 範本填的樣本（保留與省略 Config Schemas）：single PASS（28 項、0 警告），pair PASS；樣本保留的 wiki link 是 `> [[RSDC-Standard]]`。
- `check_parity.py`：gen-rsdc-skill、imp-app、imp-home 都 0 failure（imp-app 10 個、imp-home 7 個警告，與 HEAD 相同，原本就有）。
  `scan_source.py`：gen-rsdc-skill、imp-app、gen-imp-app、imp-home 都 valid。

## 5. 與其他 task 的關係

—

## 6. 日誌

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-09

- 提出：認為 `RSDC-Responsibilities` 這個檔名太長。
- 採用 `RSDC-Standard` 為新名稱，檔案與 twin 一起改名，引用一併改完。
- 改名併入標準版本 261010，沒有另發新版本。
