# Task 15 - 把其餘範本與 skill 的佔位符改成大括號寫法

**Status**：完成——2026-10-11 其餘範本、規則與 skill 都改成 `{UPPER_SNAKE}`，兩件待決定的事也已決定並做完。
**Raised**：2026-10-10，使用者在 Obsidian 看範本時，發現 `___PLACEHOLDER___` 被顯示成粗斜體。
**Depends on**：—

## 1. 背景

背景：`___UPPER_SNAKE___` 在 Markdown 裡就是粗斜體的標記。
2026-10-10 決定改用 `{UPPER_SNAKE}`：
- Obsidian 照字面顯示，不會變成斜體。
- 反引號維持原本的兩種意思：佔位符的值本身是程式碼（例如 `` `{FILE_1}` ``），或只是「提到」一個佔位符而不是留下沒填的。
- repo 原本就用大括號表示要代換的值；大寫底線（寫文件時填）與小寫駝峰（例如 `{skillGroups.common}`，執行時解析）以大小寫區分。

沒有採用「加反引號」：會和上面兩種反引號的用法混在一起，連結目標與 mermaid 圖裡也加不了，tw 裡黏著中文的佔位符還得逐一補空格。

## 2. 現況

**已完成（2026-10-10）**：
- 兩份 RSDC 範本，EN 與 tw：Skill-System 每份 182 個（tw 183 個——第 32 行把 EN 的 it 寫成 `{THE_SYSTEM}`），App 每份 96 個。
  範本區塊的說明改成「一份填好的文件若還留著任何一個，就有一部分沒有人寫」。
- `check_rsdc.py` 的 `PLACEHOLDER_RE` 同時認 `{UPPER_SNAKE}` 與舊的 `___UPPER_SNAKE___`，不認小寫的 `{skillGroups.common}`。
- gen-rsdc-skill 的 `SKILL.md` 與 tw 提到佔位符的那一句。

**做了什麼（2026-10-11）**

使用者先選定的做法：
- 沒填的佔位符：任何大寫的 `{…}` 都算沒寫完，不論在不在反引號裡。
- 說明佔位符時一律寫 `{PLACEHOLDER}`，這個名稱本身永遠豁免。
- 舊寫法：檢查腳本繼續認 `___X___`，當作沒填。
- README 範本一併納入（它在 Task 22 才建立，原本不在清單上）。
- mermaid 圖：實際渲染確認。

轉換：一支腳本把 332 個 `___X___` 換成 `{X}`，EN 與 tw 同時。
- SKILL 範本與 tw 各 72 個，README 範本與 tw 各 52 個，`Wireframe-tmp.md` 27 個，`report-md-rules.md` 13 個，`report-yaml-rules.md` 1 個。
- gen-skill 的 `SKILL.md` 與 tw 各 19 個，check-skill 的 `SKILL.md` 與 tw 各 2 個，synch-two-mds 1 個。

人工改寫的說明句（EN 與 tw 同步）：
- gen-skill：glossary 的 placeholder 定義、兩處「收尾前掃描」，以及 `{STEP_N_*}`。
- check-skill：`SKILL.md` 的 leftovers 與 readme-shape 兩處，`checking-criteria.md` 第 8 項。
- chinese：kept-English span 的定義，以及 Step 的第 6、9 項。
- asd-ste：kept span 的定義。
- chinese、asd-ste、check-skill 的工具都還認舊寫法，所以這些句子寫成「`{PLACEHOLDER}`，或舊檔寫成的 `___PLACEHOLDER___`」。

腳本：
- check-skill 的 `scan_skill.py`：`PLACEHOLDER` 認兩種寫法，並豁免 `{PLACEHOLDER}` 與 `___PLACEHOLDER___`。
- `check_rsdc.py`：`PLACEHOLDER_RE` 同樣豁免。

依賴：gen-skill、check-skill、asd-ste 的 `README.md` 與 tw 追蹤了 SKILL 範本、README 範本與 chinese 的 `SKILL.md`（asd-ste 另有 `report-yaml-rules.md`）。
這些改動不影響 README 的內容，所以用 `depends_on.py record --target` 只重新記錄這幾項。

## 3. 要做的

**尚未改**（照同一方式）：
- SKILL 範本：`.github/common/templates/SKILL-tmp.md` 與 tw，各 90 個，其中 36 個在反引號裡。
- `imp-app/assets/Wireframe-tmp.md`，27 個。
- `rules/report-md-rules.md`，13 個；`rules/report-yaml-rules.md` 提到 `___USER_PROMPT___`。
- 說明或引用佔位符的 skill：gen-skill（glossary 的 placeholder 定義、逐一列出的佔位符、「掃描 `___`」那一句）、check-skill（`SKILL.md` 與 `checking-criteria.md` 第 8 項，各有 tw）、synch-two-mds（`___REPORT_FILENAME___`）、chinese（列出要原樣保留的 token，`{placeholder}` 已涵蓋新寫法，可能只需改例子）。
- 腳本：check-skill 的 `scan_skill.py`（`PLACEHOLDER`）。
  chinese 的 `scan_md.py` 的 `TOKEN_RE` 已經兩種都認，不必改。

**要決定的**：
1. gen-skill 的規則是「佔位符留在反引號外面才算沒寫完」，可是 SKILL 範本有 36 個佔位符本來就在反引號裡（例如 `` `___SCRIPT_PATH_1___` ``），沒填也不會被抓到。
   改寫法時，要不要一併改成「任何大寫的 `{…}` 都算沒寫完，說明佔位符的句子除外」。
2. 兩份 RSDC 範本的 mermaid 圖裡也有佔位符（放在引號裡，例如 `CALLER{{"{THE_CALLER}"}}`）。
   RSDC Checker 的形狀檢查通過，但還沒有在 Obsidian 實際看過圖是否正常。

**留下的**：
- SKILL 範本的 frontmatter `name: {SKILL_NAME}` 在 YAML 裡會被讀成物件，不是字串。
  目前沒有工具把範本的 frontmatter 當字串讀，parity 檢查也通過；gen-skill 填完之後就是字串。
- SKILL 範本有 4 處 `{skillGroups.{SKILL_GROUP}}`，是大括號套大括號；填完之後就是 `{skillGroups.common}` 這類執行時的值。
- 沒有跑 gen-skill README 列的最後一項：用 gen-skill 寫一個拋棄式的 skill，再用 check-skill 檢查。
  也沒有跑完整的 `/check-skill`；只跑了它們的腳本。
- `tasks/` 裡的舊 task 仍寫著 `___X___`，那是歷史紀錄，不改。

## 4. 驗證

驗證：
- `check_parity.py`：10 組 twin（兩份範本、gen-skill 與 check-skill 的 `SKILL.md` 與 README、`checking-criteria.md`、chinese 與 asd-ste 的 `SKILL.md`、asd-ste 的 README）與改動前相同，沒有新的失敗；gen-skill 原本的一個警告消失了。
- `scan_skill.py`：新寫法被抓到，`{PLACEHOLDER}` 不再被當成沒填。
- `depends_on.py check`：六份 README 全部 UNCHANGED。
- mermaid：README 範本與 tw、兩份 RSDC 範本的 4 張圖，用 mermaid 10.9.1 在瀏覽器實際渲染，都沒有錯誤，每個佔位符都照字面顯示在節點裡。

## 5. 與其他 task 的關係

—

## 6. 知識

—

## 7. 日誌

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-11

- 其餘範本、規則與 skill 都改成 `{UPPER_SNAKE}`。
- 兩件待決定的事也已決定並做完。

### 2026-10-10

- 提出：在 Obsidian 看範本時，發現 `___PLACEHOLDER___` 被顯示成粗斜體。
- 決定改用 `{UPPER_SNAKE}`；兩份 RSDC 範本、`check_rsdc.py` 與 gen-rsdc-skill 先改。
