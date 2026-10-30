# Task 25 - 舊檔中的 `___PLACEHOLDER___` 一律視為錯誤

**Status**：完成——2026-10-13 四項都做完（見下方「做了什麼」）；三個根目錄都沒有舊寫法，不必轉換。
**Raised**：2026-10-12，Task 15 把佔位符改成 `{UPPER_SNAKE}` 之後，使用者要求舊寫法一律視為錯誤，不再當成另一種合法的寫法。
**Depends on**：[[Task 15]]

## 1. 背景

背景：[[Task 15]] 把範本、規則與 skill 的佔位符都改成 `{UPPER_SNAKE}`，但決定檢查腳本繼續認舊寫法 `___X___`，說明句也寫成「`{PLACEHOLDER}`，或舊檔寫成的 `___PLACEHOLDER___`」。
所以一份還沒轉換的舊檔，在 chinese 與 asd-ste 中仍被當成正常的佔位符原樣保留，不會被指出來。
舊寫法在 Markdown 裡會顯示成粗斜體，這正是 Task 15 要改寫法的原因。

## 2. 現況

**已決定（2026-10-12）**

提出時問了 8 個問題，決定如下：

- **範圍**：四個工具都改——check-skill（`scan_skill.py` 與判準 1.8）、chinese（`scan_md.py` 與 `check_parity.py`）、asd-ste（`check_ste.py`）、gen-rsdc-skill（`check_rsdc.py`）。
- **嚴重度**：檢查失敗，但不中止。
  check-skill 報 issue，`check_parity.py`、`check_ste.py` 與 `check_rsdc.py` 報 FAIL；chinese 與 asd-ste 照常完成翻譯或改寫，由最後的檢查擋下。
- **修正**：在 `.github/common/scripts/` 新增一支獨立的轉換腳本，可以只掃描不改，也可以把 EN 與 tw 一起轉成 `{X}`；四個工具的錯誤訊息都指向它。
- **不豁免**：`___PLACEHOLDER___` 這個名稱本身也不再豁免，任何 `___X___` 都是錯誤；`{PLACEHOLDER}` 仍是說明新寫法時用的名稱。
- **說明句**：chinese、check-skill 與 asd-ste 的說明完全不再提舊寫法，只定義 `{PLACEHOLDER}`；舊寫法只由腳本的錯誤訊息說明。
- **`tasks/`**：歷史紀錄保持原樣，工具也不掃描它。
- **其他根目錄**：其他 skillGroups 根目錄與 vault 中的舊檔列入本 task——先用轉換腳本只掃描、列出清單，再決定轉換哪些。

**目前把舊寫法當成正常佔位符的地方（2026-10-12）**

- 腳本：
  - check-skill 的 `scan_skill.py`：`PLACEHOLDER` 兩種寫法都認，並豁免 `{PLACEHOLDER}` 與 `___PLACEHOLDER___`。
  - gen-rsdc-skill 的 `check_rsdc.py`：`PLACEHOLDER_RE` 同上。
  - chinese 的 `scan_md.py`：`TOKEN_RE` 把舊寫法當成要原樣保留的 token，`FILL_RE` 把它當成待填的佔位符；`check_parity.py` 匯入同一個 `TOKEN_RE`。
  - asd-ste 的 `check_ste.py`：`PLACEHOLDER_RE` 把舊寫法當成 kept span。
- 說明句，EN 與 tw 都有：
  - chinese 的 `SKILL.md`：kept-English span 的定義、Step 1 第 6 項、Step 3 第 9 項。
  - check-skill 的 `SKILL.md`：Step 2 第 5 項（leftovers）與第 8 項（readme-shape）；`checking-criteria.md` 的判準 1.8。
  - asd-ste 的 `SKILL.md`：kept span 的定義。
- `tasks/` 之外，repo 中已經沒有用舊寫法寫的佔位符。

**做了什麼（2026-10-13）**

動手前又問了 8 個問題，決定：腳本叫 `placeholders.py`，分 `scan` 與 `convert`；一定要給路徑；`task-summary.md` 視同 `tasks/`，不掃不改；舊寫法的範圍與原本相同（`___全大寫___`）；chinese 的 Step 1 列為警告；其他根目錄只掃 InvestForge 與它的 wikiDir；check-skill 只跑腳本檢查；全部做成一個 commit。

1. **轉換腳本** `.github/common/scripts/placeholders.py`：
   - `scan PATH...` 列出每一個 `___X___` 的檔案與行號，有就 exit 1；`convert PATH...` 改成 `{X}`，有 `-tw.md` twin 的一起改，BOM 照原樣保留。
   - PATH 一定要給：一個檔案，或遞迴找 `*.md` 的目錄；目錄裡跳過 `.git`、`.obsidian`、`.trash`、`node_modules`、`__pycache__`，以及 `task-summary.md` 與它旁邊的 `tasks/`。
2. **四個工具**：`___X___` 不再是佔位符或 kept span，`___PLACEHOLDER___` 也不再豁免；錯誤訊息都附上 `placeholders.py` 的完整路徑與 `convert` 指令。
   - check-skill：`scan_skill.py` 把舊寫法另列為 `leftovers.old_placeholder_tokens` 與 `readme_shape.old_placeholder_tokens`；判準 1.8 規定它一律是 issue，修正方式是 `placeholders.py convert`。
   - chinese：`scan_md.py` 在盤點中多印一節 WARNING，照常 exit 0；`check_parity.py` 在任一份檔案有舊寫法時 FAIL。
   - asd-ste：`check_ste.py` 盤點時給 `[WARN]`，檢查時 source file 或 STE file 有舊寫法就給 `[FAIL]`。
   - gen-rsdc-skill：`check_rsdc.py` 的 `--rsdc` 與 pair 兩種檢查都給 FAIL。
3. **說明句**：刪掉 chinese、check-skill、checking-criteria 與 asd-ste 共 7 處英文對舊寫法的描述，不再寫出舊語法。
   新的警告與檢查以「已停用寫法的 placeholder」帶過，加在原有的項目裡，沒有重新編號；4 份 tw 照 chinese 的 INCREMENTAL 只改這些行。
   chinese 的 `SKILL.md` 改了，所以 check-skill、asd-ste 與 gen-skill 的 README 與 tw 重新記錄 header quote 中的 `chinese/SKILL.md`。
   chinese 與 gen-rsdc-skill 沒有 README；`placeholders.py` 沒有加進任何 README 的依賴樹，改由它的 docstring 寫明哪四個 skill 會指向它。
4. **掃描**：三個根目錄都沒有舊寫法，所以不必決定轉換哪些。
   - SkillsGestalt：掃了 111 份 `.md`；24 處舊寫法都在 `tasks/` 與 `task-summary.md`，照決定不掃不改。
   - InvestForge：掃了 135 份 `.md`，包括 `.claude/skills`。
   - InvLlmWiki（wikiDir）：掃了 313 份 `.md`。

## 3. 要做的

**要做的**

1. 轉換腳本：新增於 `.github/common/scripts/`，名稱待定。
   只掃描時列出每一個 `___X___` 的檔案與行號；轉換時改成 `{X}`，有 `-tw` twin 的一起改，做法與 Task 15 的轉換相同。
2. 四個工具：不再把 `___X___` 當成佔位符或 kept span，改報為錯誤，並在訊息中指向轉換腳本。
   拿掉 `___PLACEHOLDER___` 的豁免。
3. 說明句：刪除上列各處對舊寫法的描述，EN 與 tw 一起改；有 README.md 的 skill，照它的 When the Skill Is Changed 一併處理。
4. 其他根目錄與 vault：用轉換腳本只掃描，列出清單，交給使用者決定轉換哪些。

## 4. 驗證

**驗證結果（2026-10-13）**

- 測試檔（scratch 中的一個 skill、一對 md 與一對 RSDC）：四個工具都報錯，chinese 的 `scan_md.py` 與 asd-ste 的盤點仍 exit 0；`convert` 之後，舊寫法的檢查全部 PASS。
- 42 對 twin 重跑 `check_parity.py`：全部 0 failure，與動手前的結果完全相同。
- check-skill 與 asd-ste 的 README 列出的腳本檢查：`scan_skill.py`（asd-ste、gen-skill、check-skill）沒有缺少的標題、Step Purposes 與 Files Each Step Uses，header quote 全部 UNCHANGED；各對的 `check_parity.py` 都是 0 failure；`depends_on.py check` 全部 UNCHANGED；`check_ste.py` 對 DFD.md 的盤點 exit 0，檢查 PASS。
- `/check-skill` 與實際跑一次 asd-ste，照決定沒有做。

**驗證**

- 拿一份含 `___X___` 的測試檔：四個工具都報錯，而且 chinese 與 asd-ste 仍跑完；用轉換腳本轉換之後，四個工具都通過。
- 現有的 twin 跑 `check_parity.py`，沒有新的失敗。

## 5. 與其他 task 的關係

**與其他 task 的關係**

- [[Task 15]]：本 task 推翻它「檢查腳本繼續認舊寫法」的決定。
- [[Task 24]]：把其餘 skill 改成新格式時，可以順便用轉換腳本掃描。

## 6. 日誌

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-13

- 四項都做完：新增轉換腳本 `placeholders.py`，四個工具改報錯，說明句已刪除舊寫法。
- 掃描三個根目錄，都沒有舊寫法。

### 2026-10-12

- 提出：Task 15 之後，使用者要求舊寫法一律視為錯誤。
- 問過 8 個問題後決定範圍、嚴重度與修正方式。
