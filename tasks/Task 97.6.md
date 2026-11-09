# Task 97.6 - mermaid-view 的 mod 搬進 repo，成為 marketplace 的 plugin

**Status**：取消——跟著 [[Task 97.4]] 取消；mermaid-view 的程式碼仍在 dev-mods。
**Raised**：2026-11-02，mermaid-view 本來就是 Claude Code 的 plugin，但程式碼只在一個 session 的 dev-mods 資料夾，只有那個 session 載入它。
**Depends on**：[[Task 97.4]]

## 1. 背景

- repo 的 `mods/mermaid-view/` 只有 [MermaidView-RSDC.md](../mods/mermaid-view/MermaidView-RSDC.md) 與中文版。
- 程式碼在 `~/.claude/dev-mods/438db5fa-5da6-456a-90db-c9e6ad1178b3/mermaid-view/`：`.claude-plugin/plugin.json`（name `mermaid-view`，version `0.1.0`）、`hooks/hooks.json`、`hooks/register.tsx`、`types/`、`tests/`。
- 其他 session 要用 `--plugin-dir` 或 `CLAUDE_CODE_PLUGIN_DIRS` 才載入。

## 2. 結論

—

## 3. 過程

### 2026-11-02 的規劃

- 只搬 mod 本身；下面兩部分維持現在的位置，plugin 的說明寫清楚還要裝哪些：
  - Finder Quick Action：`~/Library/Services/顯示 Mermaid 圖.workflow`，它的 Python 只在 `.workflow` 裡，只能在 macOS 用；
  - 共用的頁面檔：`~/Library/Application Support/mermaid-view/`。
- 頁面檔不放 `${CLAUDE_PLUGIN_ROOT}`：它每個版本都換路徑，已寫好的頁面會找不到它們。
- 它的面板用 Claude 桌面版的介面，VS Code 不執行；marketplace 的說明要寫它只能在 Claude Code 用。

## 4. 要做的

1. 把 dev-mods 裡的程式碼與測試搬進 `mods/mermaid-view/`，和 RSDC 放在一起。
2. 在 marketplace.json 加 mermaid-view，`source` 是 `./mods/mermaid-view`。
3. 照 RSDC 的規定，`tests/regen_fixtures.py` 與 `claude plugin test` 通過。
4. RSDC 與中文版寫明程式碼的新位置，以及 Quick Action 與頁面檔要另外裝。
5. 決定 publish-gestalt 是否發佈 mermaid-view。

## 5. 驗證

- `claude plugin validate` 與 `claude plugin test` 通過。
- 從 marketplace 啟用後，任何新的 Claude Code session 都有 `/mermaid`，面板列出含 mermaid 圖的 Markdown 檔。

## 6. 與其他 task 的關係

- [[Task 97.4]]：建 marketplace；本 task 加進第三個 plugin。
- [[Task 18.8]]：讓 MermaidView-RSDC 對齊範本。

## 7. 知識

—

## 8. 日誌

### 2026-11-02

- 取消：跟著 [[Task 97.4]] 取消。
- 提出。
