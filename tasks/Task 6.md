# Task 6 - 評估是否建立 tasks skill 來處理 tasks.md

**Status**：完成——2026-10-10 決定採用選項 2：寫了 `.github/common/scripts/check_tasks.py`，檢查下表與各項的編號、順序、連結、標題、Raised 日期、狀態圖示與圖例，有不一致就以 `1` 結束；tasks.md 的導言與 memory 都寫明改完就跑它。
**Raised**：2026-10-09，連續幾次調整 tasks.md 的格式之後提出。
**Depends on**：—

## 1. 背景

問題：處理 `tasks.md` 的規則現在分散在兩處——檔案開頭的導言，以及 Claude 的 memory（`workspace-tasks-md`）。
值不值得把它們收成一個 skill（例如 `/tasks`），由 skill 來新增、更新、檢查 task？

**現在要守的規則**（也就是 skill 要承載的內容）：

- 檔案在 workspace 根目錄，用繁體中文（保留英文術語），沒有 `-tw` twin。
- 每個 task 是 `## Task N - 標題`，含 **Status** 與 **Raised** 兩行；新的編下一個號碼、放在最前面。
- 開頭有一張 `| Task | Raised | Title | Status |` 的摘要表，每個 task 一列、順序相同；Task 欄是連到該段的連結，Status 欄是圖標（⬜ 尚未開始、🔄 進行中、✅ 完成），圖例在表格下方。
- 狀態改變時，要同時改兩處：該 task 自己的 **Status** 行，和表格的圖標。

**可以機械檢查的**（適合寫成腳本）：表格列數與段落數相同、順序一致；連結錨點對得上標題（GitHub 的錨點規則：小寫、空白變 `-`、標點去掉，中文保留）；Raised 日期與表格一致；圖標與 **Status** 行的字面一致（完成／進行中／尚未開始）；編號沒有跳號或重複。

**需要判斷的**（留給 Claude）：task 的內容怎麼寫、背景與影響範圍查到多深、狀態該不該改成完成。

## 2. 現況

### 狀態細節

不建 skill：維護 tasks.md 的都是共用同一份 memory 的 Claude session，選項 3 的成本換不到對應的好處；日後若有 Claude 以外的人或其他 workspace 要維護，再考慮升為選項 3。
下文「可以機械檢查的」一段寫的 GitHub 錨點規則已經過時：表格現在用 Obsidian 的寫法（標題原文、空白寫成 `%20`），腳本照這個檢查。

**這次 session 暴露的問題**，說明規則不是只靠記憶就穩的：

- 加 Raised 欄時，我的第一版腳本因為表格有對齊用的空白，只改到一列，要重做；沒有檢查腳本，這種缺漏只能靠人發現。
- 表格連結的錨點是照規則推出來的，沒有在 Markdown 預覽裡實際點過。
- 檔案多次在我讀取之後被另一個 session 改動（Task 1、Task 2 被標為完成、內容被改寫）。
  多個 session 同時編輯同一個檔案，沒有任何機制確認表格與各段仍然一致。

## 3. 要做的

**選項**：

1. **維持現狀**：只靠導言與 memory。
   成本最低，現在也運作正常；缺點是上面那類不一致沒人檢查，而且 memory 只對這個專案的 Claude 有效。
2. **只寫一支檢查腳本**（例如 `tasks_check.py`），不建 skill：每次改完 tasks.md 跑一次，確認表格與各段一致。
   解決機械部分，成本小；但沒有 `/tasks` 入口，規則仍在 memory。
3. **建一個薄的 skill**：SKILL.md 寫明格式與新增、更新、檢查三個動作，檢查交給腳本。
   規則放進 repo，任何 session、任何人都讀得到，不依賴 memory。
   要付的成本：repo 的 skill 要有 `SKILL-tw.md` twin，用 gen-skill 建立、check-skill 檢查；放在 `.github/common/skills/`。
4. **完整的 skill 加互動**（例如列出未完成的 task、挑一個接手）：功能最多，但目前沒有這個需求，tasks.md 只有六項。

**決定前要回答**：

- 是否預期 tasks.md 會長到需要列出、篩選、歸檔？
  目前不需要。
- 是否有別的人或別的 agent 要照同一套格式維護它？
  有的話，規則放在 repo 比放在 memory 好。
- 是否容許 tasks.md 偶爾不一致？
  不容許的話，至少要有選項 2 的檢查腳本。

暫時的傾向（尚未決定）：先做選項 2；若確定要讓其他 session 或其他人維護，再升為選項 3。

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

- 決定採用選項 2：寫了 `check_tasks.py` 檢查腳本，不建 skill。
- tasks.md 的導言與 memory 都寫明改完就跑它。

### 2026-10-09

- 提出：連續幾次調整 tasks.md 的格式之後，評估是否建立 tasks skill。
