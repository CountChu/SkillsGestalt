# Task 34 - 為 .github/common 中沒有中文版的 4 份原檔執行 /chinese

**Status**：完成——2026-10-12：4 份原檔都有了中文版（`3bdb57a`、`3549a16`、`9653e26`、`bc18013`），[[Task 31]] 表格的中文版欄已補上；keep-English 清單共加了 26 個詞。
**Raised**：2026-10-12，[[Task 31]] 做 2.1 之前，使用者決定：Task 31 的 11 份原檔裡，沒有中文版的 4 份先執行 /chinese 寫出中文版，Task 31 依賴本 task。
**Depends on**：[[Task 33]]

## 1. 背景

背景：[[Task 31]] 為 `.github/common` 的 references、rules、templates 共 11 份原檔產生 STE 草稿與草稿的中文版。
其中 4 份原檔本身沒有中文版，本 task 先為它們寫出中文版，Task 31 再為它們產生草稿。

## 2. 現況

**2026-10-12 做了什麼：第 1 份**（commit `3bdb57a`）

做之前問了 4 個問題，決定如下：`{skillGroups.common}` 用 `.github/common`，因為 SkillsGestalt 沒有 config.yaml；Python 用系統的 python3。
4 個不在清單上的詞都保留英文，並加入 keep-English 清單。
4 份依序做完，每份在 Step 4 問一次 commit；每份各一個中文版 commit 與一個記錄 commit。

- **中文版**：chinese 判定 FULL，17 行逐行翻譯；`check_parity.py` 0 failure、0 warning。
- **keep-English 清單**：加了 canonical skill invocation、epoch、metadata、section partial 4 個詞，Version 改成 261012。
- **新 Flagged 譯法的副作用**：現有中文版有 12 行用了被 flag 的譯法，下次跑 /chinese 時會出現警告；不在本 task 的範圍內修正。
  - canonical skill invocation 的舊譯法，10 行：SKILL-tmp-tw.md:112、asd-ste（192、196）、gen-rsdc-skill（334、644）、chinese:223、imp-app:406，以及 InvestForge 的 imp-inv-tech-rank:168、select-stocks:136、imp-inv-ctl:173。
    SKILL-tmp-tw.md:112 是 shared line，會抄進每個從範本產生的 SKILL 中文版，要修的話先修它。
  - 元數據，2 行：RSDC-Standard-tw.md:72、RSDC-Standard-ste-tw.md:185。

**2026-10-12 做了什麼：第 2 份**（commit `3549a16`）

- **中文版**：chinese 判定 FULL，61 行逐行翻譯，兩個 fenced block 逐位元組照抄；`check_parity.py` 0 failure、0 warning。
- **keep-English 清單**：照清單的規則加了 fence、here-string、interpolation、pipe、shell、wiki 6 個詞，在 Step 4 經使用者確認。
  它們的 Flagged 譯法在現有中文版中都沒有出現，不會引起新的警告。
- **照前例翻譯**：escape 譯「跳脫」、header 譯「檔頭」、arguments 譯「引數」。

**2026-10-12 做了什麼：第 3 份**（commit `9653e26`）

翻譯前另外問了 4 個關於詞的問題：md-style 有十幾個技術詞不在清單上，其中幾個加進清單會讓現有中文版出現警告。
決定如下：

- **保留英文並加入清單，共 13 個**：
  - 只在本檔出現：hard break、delimiter、non-breaking space、word character、no-op。
  - 其他中文版也用到：identifier、handler、pattern、context。
  - script：保留英文，並 flag「腳本」與「指令碼」，和 step、template 的先例一樣。
  - reformat-md 的模式名稱：raw mode、clean mode、idempotent-only mode。
- **照中文譯**：display math 譯「獨立成行的數學式」，inline math 譯「行內數學式」，math span 譯「數學式區段」，math 譯「數學式」；header 在本檔指 Markdown 的標題，譯「標題」。
- **中文版**：chinese 判定 FULL，76 行逐行翻譯，153 個 inline code 照抄；`check_parity.py` 0 failure、0 warning。
- **新 Flagged 譯法的副作用**：現有中文版有 293 行用了被 flag 的譯法，下次跑 /chinese 時會出現警告；不在本 task 的範圍內修正。
  - 腳本與指令碼 276 行（40 個檔案）。
  - 識別碼 10 行（7 個檔案）、識別字 3 行（3 個檔案）。
  - 處理器 4 行（3 個檔案）。

  行數是做第 4 份時照 `check_parity.py` 讀正文的方式重算的；原先記的「腳本 333 行」是出現次數，不是行數。

**2026-10-12 做了什麼：第 4 份**（commit `bc18013`）

翻譯前另外問了 1 個問題：清單的說明文字裡有 3 個詞不在清單上，決定 wireframe、schema、glossary 都保留英文並加入清單。

- **中文版**：chinese 判定 FULL，108 行逐行翻譯。
  表頭與 Term、Replaces、Flagged 三欄由一支小程式從英文版逐字元照抄，只譯 Why 欄與說明文字；inline-code span 算在清單上 inline code 那一列的範圍。
  `**Version**` 照 RSDC-Standard-tw 的前例寫成 `**版本**`。
- **parity**：`check_parity.py` 0 failure；91 個 warning 都在表格列，是清單自己列出的譯法，每一處都在英文版的同一行，照 chinese 的規則留著。
- **新 Flagged 譯法的副作用**：glossary 的「詞彙表」「術語表」，現有中文版有 15 行（11 個檔案）會出現警告；schema、wireframe 的譯法都沒有出現。
- **合計**：本 task 為 keep-English 清單加了 26 個詞，原檔從 82 行變成 108 行。
  新的 Flagged 譯法會讓現有中文版出現 320 行警告：canonical skill invocation 10、metadata 2、script 276、identifier 13、handler 4、glossary 15，都不在本 task 的範圍內修正。

## 3. 要做的

**已決定（2026-10-12）**

提出時問了 8 個問題，決定如下：

- **範圍**：4 份原檔，都沒有 frontmatter。
  - [report-yaml-rules.md](../.github/common/rules/report-yaml-rules.md)（17 行）
  - [report-md-rules.md](../.github/common/rules/report-md-rules.md)（61 行）
  - [md-style.md](../.github/common/rules/md-style.md)（76 行）
  - [tw-keep-english.md](../.github/common/references/tw-keep-english.md)（82 行）
- **做法**：照 chinese skill 的流程為每一份寫出 `-tw.md`，放在原檔旁邊。
- **原檔不動**：不在原檔加「它的繁體中文 twin 是…」那一句，和 [[Task 33]] 的決定一致。
- **順序**：照 Task 31 用到它們的順序——report-yaml-rules（2.1）、report-md-rules（2.5）、md-style（2.6）、tw-keep-english（第 3 步）。
- **commit**：每份一個，照 chinese 的 Step 4，前綴 `task 34`。
- **進度**：每譯完一份，在那一份打 ✅ 並附 commit。
- **依賴**：本 task 依賴 Task 33，等它改完 chinese skill 再執行；Task 31 依賴本 task。

**要做的**

1. ✅ report-yaml-rules.md → `report-yaml-rules-tw.md`（2026-10-12 完成，`3bdb57a`，見下）
2. ✅ report-md-rules.md → `report-md-rules-tw.md`（2026-10-12 完成，`3549a16`，見下）
3. ✅ md-style.md → `md-style-tw.md`（2026-10-12 完成，`9653e26`，見下）
4. ✅ tw-keep-english.md → `tw-keep-english-tw.md`（2026-10-12 完成，`bc18013`，見下）

每一份都照 chinese 的 Step 0 到 Step 4 做：Step 1 的 `diff_md.py` 會判定 FULL，因為還沒有中文版。
4 份都完成之後，把 Task 31 表格中這 4 份的中文版欄補上。

**注意**

- tw-keep-english.md 本身就是 keep-English 清單：照 chinese 的規則，表頭與 Term 欄保留英文，Replaces、Flagged 兩欄本來就是中文，譯的是 Why 欄與說明文字。
  chinese 的工具讀的是英文版（`--keep` 指向它），中文版不影響工具。
- md-style.md 由 reformat-md 讀取，讀的也是英文版。

## 4. 驗證

**驗證**

- 每一對的 `check_parity.py` 0 failure，中文版逐行對齊英文。

## 5. 與其他 task 的關係

**與其他 task 的關係**

- [[Task 31]]：依賴本 task——它的 2.1、2.5、2.6 與第 3 步，要等這裡寫出原檔的中文版再產生草稿；2026-10-12 已寫出，它表格的中文版欄也已補上。
- [[Task 33]]：本 task 依賴它。
- [[Task 32]]：審核通過、以草稿取代原檔時，草稿的中文版寫回本 task 寫出的 `-tw.md`。

## 6. 知識

—

## 7. 日誌

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-12

- 提出：Task 31 做 2.1 之前，決定先為沒有中文版的 4 份原檔執行 /chinese。
- 決定範圍、做法、順序與 commit 方式。
- 4 份中文版都寫出並 commit，keep-English 清單共加了 26 個詞，Task 31 表格的中文版欄已補上。
