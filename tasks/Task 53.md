# Task 53 - 建立 chore：會重複做的例行工作

**Status**：完成——2026-10-18 建立，同日做完：chore 有了自己的資料夾、規則、摘要表與 `check_chores.py`，並建立 [[rerecord-ste-custom]] 與 [[keep-english]]。
**Raised**：2026-10-18，[[Task 52]] 定下的集中重記，是每次 ste-custom.md 有改動的日子都要再做的例行工作，放在 task 裡會變成「完成了卻還要一直做」；使用者決定另立 chore，有自己的編號與摘要表。
**Depends on**：—

## 1. 背景

task 是做完就結束的工作，狀態是尚未開始、進行中、完成。
有些工作條件成立就要做、做完還會再來，例如 [[Task 52]] 的集中重記、兩個 workspace 中英對照的 keep-English 稽核，以及以 check-skill 掃描全部 skill 之後更新 Skills Dashboard。
這類工作放在 task 裡，task 標了完成卻還要一直做，每次做了什麼也沒有固定的地方記。

## 2. 現況

### 已決定（2026-10-18）

- 名稱：chore，中文是例行雜務；從十個候選中選定。
  routine 和 Claude Code 排程執行的雲端 agent 同名，upkeep 與 housekeeping 不可數，sweep 只適合「掃一遍」的工作。
- 位置：`chores/Chore N.md`，規則寫在 `chores/CLAUDE.md`，摘要表放在 `dashboard/chore-summary.md`；編號和 task 分開，從 1 起。
- 狀態：使用中 🔁、暫停 ⏸️、停用 ⏹️；chore 不會完成，只會停用。
- 格式：標題下三行——Status、Started、When（何時要做）；六章是 `1. 目的`、`2. 何時要做`、`3. 怎麼做`、`4. 驗證`、`5. 與其他 task、chore 的關係`、`6. 執行紀錄`，執行紀錄每天一個日期小節，新的在前。
- 摘要表的欄：Chore、Started、Title、何時要做、上次執行、Status。
- 檢查：另寫 `check_chores.py`，和 `check_tasks.py` 分開。
- commit 前綴：chore 的執行是 `chore N: `，小寫；建立 chore 制度的修改記在本 task，前綴 `task 53: `。
- 第一個 chore：[[rerecord-ste-custom]] 集中重記 ste-custom.md，建好之後馬上跑第一次。
- 第二個 chore：[[keep-english]] keep-English 稽核，同日由使用者提出，記在本 task。
  - 何時要做：tw-keep-english.md 換了版本，和上次稽核的版本不同；261016 這一版不稽核，第一次等下一版。
  - 範圍：SkillsGestalt 與 InvestForge 的全部中英對照，不含 tw-keep-english 自己的兩份與 checkpoints。
  - 工具：共用的 `.github/common/scripts/audit_keep_english.py`，不動 chinese skill；完整清單存在 `checkpoints/chores/chore-2/`，執行紀錄只寫總數與和上一份的差異。
  - 找到的只列出，要改的另開 task；英文那一行本身就寫著那個中文詞的，標成「英文也寫中文」分開列。

### 結果（2026-10-18）

- `chores/CLAUDE.md`：chore 和 task 怎麼分、檔案、格式、摘要表與檢查，寫法照 tasks/CLAUDE.md。
- `dashboard/chore-summary.md`：開頭說明、摘要表、圖示與「上次執行」的說明。
- `chores/Chore 1.md`：何時要做寫明以 `draft.py recheck --dry-run` 看出該做了；怎麼做照 ste-custom.md 的說明，列出 `[FAILED]`、`[NOT RECORDED]` 與 `[NEW WARN]` 怎麼處理。
- `check_chores.py`：14 項檢查，和 `check_tasks.py` 一樣只用標準函式庫；「上次執行」比對的是 chore 檔執行紀錄最新的日期。
- 根目錄的 CLAUDE.md 加上 Chores 一節，tasks/CLAUDE.md 開頭註明例行工作寫成 chore。
- `audit_keep_english.py`：`audit` 找出每一對 X.md 與 X-tw.md，照 `check_parity.py --keep` 的做法在中文版正文裡找 Flagged 的譯法；`due` 比對清單的版本與上一份報告的版本。
  它從 chinese skill 的 `scan_md.py` 匯入讀清單與正文的函式，所以和 `check_parity.py` 找的是同樣的東西。
- `chores/Chore 2.md` 與摘要表的一列。

## 3. 要做的

1. 寫 `chores/CLAUDE.md`、`dashboard/chore-summary.md` 與 `chores/Chore 1.md`。
2. 寫 `.github/common/scripts/check_chores.py`。
3. 根目錄的 CLAUDE.md 加上 Chores 一節；tasks/CLAUDE.md 註明例行工作寫成 chore。
4. [[Task 52]] 的關係一章加上 [[rerecord-ste-custom]]。
5. 跑 [[rerecord-ste-custom]] 的第一次，結果單獨一個 commit，前綴 `chore 1: `。

## 4. 驗證

- `check_chores.py` 與 `check_tasks.py` 都 PASS。
- 把 chore 檔與摘要表故意改得不一致（標題、圖示、上次執行），`check_chores.py` 以 1 結束並指出那一項。

## 5. 與其他 task 的關係

- [[Task 52]]：定下集中重記的做法，由 [[rerecord-ste-custom]] 接手執行。
- [[rerecord-ste-custom]]：本 task 建立的第一個 chore。

## 6. 知識

—

## 7. 日誌

### 2026-10-30

- [[Task 86]] 把 chore 改用名稱：本檔的 `[[Chore N]]` 連結改成新名稱。

### 2026-10-18

- 建立。
- 同日做完：chore 的資料夾、規則、摘要表、`check_chores.py` 與 [[rerecord-ste-custom]]；[[Task 52]] 的關係一章加上 [[rerecord-ste-custom]]。
- 驗證：`check_chores.py` 14 項 PASS，`check_tasks.py` 18 項 PASS。
  在副本上把摘要表的標題、圖示、上次執行改錯，執行紀錄排成舊的在前，再放一個多的檔案：`check_chores.py` 以 1 結束，逐項指出這五處。
- [[keep-english]]：使用者決定再收一件例行工作，記在本 task；寫了 `audit_keep_english.py` 與 Chore 2。
  驗證：`due --baseline 261016` 印出 not due、以 1 結束；沒給 baseline 時印出 due。
  把報告寫到 scratchpad 試跑一次：67 對中英對照，47 份中文版有 605 行警告，「英文也寫中文」4 行（MermaidView-RSDC 的「角色」與 InvestForge 兩份 SKILL 的「過期」等）；最多的是 script 的「腳本」294 行、step 的「步驟」202 行。
  再放一份較早、少一筆又多一筆的報告：比對印出 1 筆 `[NEW]` 與 1 筆 `[GONE]`。
  正式的第一次照決定等清單換版本，所以 `checkpoints/chores/chore-2/` 還沒有報告。
