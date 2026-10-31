# Task 13 - 讓其他 skill 處理檔頭引用區的依賴格式

**Status**：完成——2026-10-10 新增了 check-md-deps，取代原本 check-skill 那一列，並讓它也檢查 twin 是否落後；chinese、check-wiki-doc 與 check-stop-price 三列也已完成，check-wiki-doc 後來加的兩列也都完成（見表）。
**Raised**：2026-10-10，整理「哪些 skill 會處理依賴格式」時提出，接續 [[Task 8]]。
**Depends on**：—

## 1. 背景

依賴格式（Task 8）：文件開頭的檔頭引用區，每一行一個連結，後面依序是 `cited`（只算引用到的節時才寫）、確認的日期與指紋，例如 `` > [[SkillCompiler-RSDC]]  `cited`  `2026-10-10`  `bd7932a83cd3` ``。
讀寫它的是共用的 [depends_on.py](../.github/common/scripts/depends_on.py)。

## 2. 現況

### 狀態細節

compile-skill 與 gen-skill 兩列要等觸發條件，移到 [[Task 16]]。

**已經會處理的**（不必再做）：

- **gen-rsdc-skill**：Step 2 由 RSDC Checker 讀範本檔頭的紀錄、與標準現在的內容比對，不符就停下；Step 8 在目標 skill 宣告 `> [[<system name>-RSDC]]`；Step 9 用 `record --cited` 記下；寫 RSDC 時保留範本檔頭那兩行。
- **gen-rsdc-app**（Task 14 從 imp-app 的 `reverse` 抽出）：Step 0 對它的 design template `RSDC-App-tmp.md` 執行 `check`，範本落後於標準就停下；寫 design pair 時保留範本檔頭那兩行（範本的刪除指示寫明只留上面連到標準的連結）。
  imp-app 的 `reverse` 改由它寫 design pair，自己不再讀寫依賴格式。
- **chinese**：連結目標與 inline code 都原樣抄進 twin，所以 twin 帶著同一份紀錄；但它不執行 `record`（見下表）。
- **check-md-deps**（2026-10-10 新增，[SKILL.md](../.github/common/skills/check-md-deps/SKILL.md)）：檢查任何 md 的依賴是否過時、格式是否正確。
  它的 `scan_md_deps.py` 給出每個依賴的判定與格式問題，判為 CHANGED 時再列出確認日之後的 commit、確認當時的版本（找不到就標為近似）與被引用之節的差異；skill 依 check-wiki-doc 的報告格式，就 Format、Recorded、Current、Twin 四項提出編號的修改意見，使用者以編號同意後才修改，`record` 也一樣。
  不產出 MD report 或 YAML checkpoint。
  **Twin**（2026-10-10 加入）：目標檔旁邊有 `<name>-tw.md` 時，scanner 以命令執行 chinese 的 `diff_md.py`（Twin Differ），依 git 判斷 twin 是否跟上——`UNCHANGED`、`INCREMENTAL`（附 change set）、`FULL`（附原因，例如 twin 從沒 commit 過，或 twin 自己有未 commit 的修改）或 `UNCHECKED`；Step 3 對使用者指名的 twin 建議執行 chinese skill。
  第一次掃 `.github/common`：20 份 twin 中 18 份 UNCHANGED；`compile-skill/references/Tasks.md` 的 twin 在 6580f9b 就沒有逐行對齊（FULL）。
  它的 Dataflow 有「Step 1、2 讀目標檔，Step 3 才改」（TW twins 也一樣），和 [[Task 7]] 是同一類問題。
  它取代了原本 check-skill 那一列：check-skill 不必改。

## 3. 要做的

**要做的**：

| Skill | 現在 | 要做什麼 | 牽涉的檔案 |
|---|---|---|---|
| check-wiki-doc | **已完成（2026-10-10）**：步驟 1 對全部納管文件跑 check-md-deps 的 `scan_md_deps.py`（`--root` 給 `wikiRootDir`），步驟 4 在有邊不是 `UNCHANGED` 的上層打 ✓，只打勾、不清除；查了第 6 條時，步驟 4 對比對過的每個下層 `record`——比對出矛盾也照記，因為紀錄說的是「檢查結果是對著這一版的下層做的」，矛盾寫在 `檢查結果`；文件自己的改動與新納管的文件仍手動打勾（後來由下面「文件自己的改動」一列改為依賴掃描判出），步驟 5 改完要重跑掃描。第 1 條加上紀錄的格式（只比對連結、不寫 `cited`、`malformed` 算缺口），第 6 條加上掃描的判定與記錄。第一次唯讀掃 InvLlmWiki：17 份中 4 份在最底層、沒有依賴，其餘 13 份的 43 條邊全是 `NO_RECORD`，所以下一次執行會把這 13 份都打 ✓ | — | `check-wiki-doc/SKILL.md`（步驟 1、4、5）、`references/checking-criteria.md` 第 1、6 條 |
| check-wiki-doc：文件自己的改動 | **已完成（2026-10-10）**：採 (b)。架構文件的檔頭依〈名稱〉欄的順序逐一列出每份納管文件；步驟 4 檢查完，不論查了哪幾條，都以 `record --target` 在那一行記下待查文件當時的指紋，缺的行補上、已不納管的刪掉。步驟 1 的依賴掃描連架構文件一起掃，那一行不是 `UNCHANGED` 就打 ✓——文件在上次檢查之後改過（在 Obsidian、步驟 5 或別的對話改的都一樣），或新納管、還沒檢查過；步驟 4、5 的手動打勾因此拿掉。checking-criteria.md 的開頭註明架構文件的檔頭是檢查紀錄、不是依賴宣告；第 6 條仍比對全部下層。在 scratchpad 模擬：重記文件自己的下層（改到它的檔頭）仍是 `UNCHANGED`，改了內文才判 `CHANGED` 並附上差異；架構文件多了 17 行檔頭，產生的 HTML 依賴圖不變。git 顯示 17 份納管文件在各自的檢查日期當天或之後都還有 commit，所以下一次執行補上檔頭、把 17 份都打 ✓ 是對的 | — | `check-wiki-doc/SKILL.md`（步驟 1、4、5）、`references/checking-criteria.md`（開頭、第 6 條） |
| check-wiki-doc：架構文件的說明 | **已完成（2026-10-10）**：投資系統架構第 2、3、4 節的 6 處 `check-doc` 改為 `check-wiki-doc`；〈文件狀態〉的說明補上一句：本文件的檔頭逐一列出每份納管文件，記著它上次檢查的日期與指紋，由 `check-wiki-doc` 寫入。`待檢查` 的三種情況改寫成由依賴掃描判出——新納管＝檔頭裡它那一行還沒有紀錄；檢查後又改過＝那一行的指紋與現在不符；下層改過＝它自己檔頭的某條邊不符或沒有紀錄。帶子項目的引言後只留一句（第 2 條的寫法）。檔頭那 17 行沒有先加，下次執行 check-wiki-doc 時由步驟 4 補上 | — | InvLlmWiki 的 `config/投資系統架構.md` 第 2、3、4 節 |
| chinese | **已完成（2026-10-10）**：英文檔 `record` 之後，跑一次 chinese——它的 INCREMENTAL 更新依 git diff 只改那一行（line for line 的檔換那一行；SKILL.md 的檔頭引用區屬於 `(preamble)` 一段，整段重寫，pairing line 保留）——twin 的紀錄就和英文檔一致，「twin 只由 chinese 寫」也不變；check-md-deps 的 Twin 一項會提醒。為此把檔頭引用區的每一行（連結與其後的 inline code）寫進 kept-English span，`scan_md.py` 與 `check_parity.py` 也把 wiki link `[[name]]` 當成連結列出、比對；並修正 INCREMENTAL 那句還要「保留 twin 標題後綴」的舊規則 | — | `chinese/SKILL.md` 與 tw、`scripts/scan_md.py`、`scripts/check_parity.py` |
| check-stop-price（InvestForge） | **已完成（2026-10-10）**：依賴方定為 Rule Copies，由新檔 `rule-copies.md`（skill 根目錄，取代 `plan-docs-hash.json`）代表。不用 SKILL.md：它之後會由 gen-rsdc-skill 記 StopPriceChecker-RSDC 的 `cited` 紀錄，同一份文件對同一個目標只能有一行，兩種驗證會互相蓋掉對方的擔保。檔頭五行：四份 Plan Docs 寫成 `[名稱](<{wikiDir}/plan/...>)`，整份算；StopPriceChecker-RSDC 標 `cited`，本文引用 §2.4、§2.7，只算 Step 1 會讀的這兩節。Fingerprint Checker 改用共用的 `depends_on.py`（加 `--config config.yaml`），`plan_docs_hash.py` 與 `plan-docs-hash.json` 刪除；SKILL.md 的詞彙表、CONFIGURATION、目錄樹、Data Read/Write Rules、Step 0（確認紀錄檔存在）與 Step 1 跟著改，tw 依 chinese 的 INCREMENTAL 更新（parity 結果與改前相同，`--verify` 通過）。舊紀錄：四份 Plan Docs 自 10-07 起整份 SHA-256 沒變，以新算法換算、沿用 10-07 的日期；StopPriceChecker-RSDC 自當時的 `fb1a78f` 起 §2.4、§2.7 有實質修改，不換算、留 `NO_RECORD`，下次執行時 Step 1 照規定重讀並核對常數。Plan Docs 的指紋不含它們自己的檔頭，check-wiki-doc 在那裡 `record` 不再被判為改過 | — | InvestForge 的 `check-stop-price/SKILL.md` 與 tw、`rule-copies.md`（新）、`scripts/plan_docs_hash.py` 與 `plan-docs-hash.json`（刪）；SkillsGestalt 的 `depends_on.py` 說明 |

## 4. 驗證

—

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

- 提出：整理哪些 skill 會處理依賴格式，接續 Task 8。
- 新增 check-md-deps，取代原本 check-skill 那一列，並讓它也檢查 twin 是否落後。
- chinese、check-wiki-doc 與 check-stop-price 三列完成，check-wiki-doc 後來加的兩列也完成。
- compile-skill 與 gen-skill 兩列移到 Task 16。
