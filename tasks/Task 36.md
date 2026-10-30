# Task 36 - 讓 reformat_md.py 在直引號內不斷句，並認得以 ⌘ 或小寫名稱開頭的句子

**Status**：完成——2026-10-30 修好兩處斷句並加上測試；兩個 workspace 重排之後，沒有檔案因為這兩處而改變。
**Raised**：2026-10-13，[[Task 19]] 轉換最後 8 組中英對照時發現。
**Depends on**：—

## 1. 背景

[reformat_md.py](../.github/common/skills/reformat-md/scripts/reformat_md.py) 的第 10 個轉換（每個句子一行）有兩處不符合 [md-style.md](../.github/common/rules/md-style.md) 對句子的定義。
Task 19 轉換時繞過了它們，沒有修工具。

## 2. 現況

**兩處問題**

- **直引號內會斷句**：md-style.md 規定引號內的句號不結束句子，但工具只認得「」『』（）這類分開頭與結尾的符號，不認得直引號 `"`。
  例如 `**"Warning: … this system. Please …"**` 會在引號裡斷成兩行。
  Task 19 把 compile-skill 的 Tasks 與 SkillCompiler-RSDC 裡的兩段訊息改成 inline code 來繞過（5edb298）。
- **認不出以 ⌘ 或小寫名稱開頭的句子**：句號後面接 `⌘`，或接小寫開頭的名稱（例如 mermaid-view），工具不會斷句。
  中文版在「。」斷開了，英文版卻留在同一行，兩邊就對不上。
  Task 19 在 MermaidView-RSDC.md 手動加了 4 個換行來繞過（5edb298）；重跑工具也不會把它們接回去。

### 做了什麼（2026-10-30）

- 直引號 `"` 與彎引號 `“` `”` 成對時當成引號：引號內的句號不結束句子，和括號一樣。
  同一段找不到結尾的 `"` 時當成一般字元（例如 `5"` 的英吋）；單引號不處理，避開 it's、users' 這類。
- 句號、空格之後若是 ASCII 以外的符號（Unicode 的 So、Sm 類，例如 ⌘、→），或含連字號的小寫名稱（例如 mermaid-view、gen-skill），就是新句子的開頭。
- 仍認不出的：沒有連字號的小寫名稱（例如 pathlib）。
  引號裡的句號即使是整句的結尾也不斷句：`He said "Stop." Then it ran.` 留在同一行，照 md-style.md 的字面規則。
- 新增 [test_reformat.py](../.github/common/skills/reformat-md/scripts/test_reformat.py)，15 個例子：該斷的、不該斷的，以及 [[Task 42]] 的 `$$`；每個例子再跑一次，確認沒有變化。
- [[Task 19]] 的兩處繞法不必還原：改成 inline code 的訊息不受影響；MermaidView-RSDC.md 手動加的 4 個換行，和工具現在的斷法一致。

## 3. 要做的

**要做的**

2026-10-30 三項都已做完，見「2. 現況」的「做了什麼」。

- 修好這兩處斷句，並把這兩種例子加進 check_reformat.py 或測試。
- 直引號不分開頭與結尾，要決定怎麼配對，並避開所有格與縮寫裡的單引號。
- 修好之後，對所有已轉換的 md 重跑一次：沒有改變最好；有改變的，逐一確認是修正而不是新問題。

## 4. 驗證

- `test_reformat.py` 15 項 PASS。
  同樣的例子用修改前的版本跑，正好 7 項 FAIL（這兩處斷句與 [[Task 42]] 的 `$$`），其餘 8 項本來就 PASS。
- 在 SkillsGestalt 與 InvestForge 的全部 md 上比較修改前後的輸出（排除 `.git`、`node_modules`、`checkpoints`、`.github/external` 等）：346 份中只有 1 份因為修改而改變，是 [[Task 42]] 那一份。
  這兩處斷句沒有讓任何檔案改變。

## 5. 與其他 task 的關係

- [[Task 42]]：同一次修改一起做（2026-10-30），只重排一次、跑一次檢查。
- [[Task 56]]：md-style 巡檢不再漏掉這兩種一行多句。

## 6. 日誌

### 2026-10-30

- 修好直引號與 ⌘、小寫名稱的斷句，新增 `test_reformat.py`；和 [[Task 42]] 一起比較兩個 workspace 的 md，這兩處沒有讓任何檔案改變。

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-13

- 提出：Task 19 轉換最後 8 組中英對照時，發現兩處斷句問題。
