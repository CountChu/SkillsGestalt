# Task 107 - commit 訊息不加 Co-Authored-By

**Status**：完成——`AGENTS-local.md` 加一節 `## Commits`，規定 commit 訊息不加 `Co-Authored-By`；根目錄的 `.claude/settings.json` 關掉 Claude Code 的 attribution。
**Raised**：2026-11-13，使用者要求以後的 commit 都不要有 `Co-Authored-By`，不只靠一台電腦的 Claude Code 記憶。
**Depends on**：—

## 1. 背景

- 2026-11-13 的快照 `4235a83` 有 `Co-Authored-By`，換成了 `7f62c8a`；[[Task 106]] 拿掉 [[publish-gestalt]] 第 4 步的 `--co-author`。
- Claude Code 預設會在 commit 訊息加這一行。這台的 Claude Code 記憶記下了「不加」，但記憶只在這台的 `~/.claude/`，別台電腦與別的 agent 讀不到。

## 2. 結論

**表 1：兩處改動**

| 改的地方 | 作用 | 誰會讀到 |
| --- | --- | --- |
| `AGENTS-local.md` 的 `## Commits`，再由 `gen_agents_md.py` 寫進 `AGENTS.md` | 規定 commit 訊息不加 `Co-Authored-By`，快照也一樣 | 每台電腦、每個讀 AGENTS.md 的 agent |
| 根目錄的 `.claude/settings.json`：`attribution` 的 `commit`、`pr` 是空字串，`sessionUrl` 是 `false` | Claude Code 本身不加這一行，也不加 PR 的 attribution | 每台電腦的 Claude Code，跟著 repo 走 |

- 改完之後，這個 session 的 Claude Code 就不再要求加 attribution（`3.2`）。
- `.claude/settings.json` 會進下一次發佈的快照；它只有這個設定，沒有不公開的內容。
- `AGENTS-local.md` 是 local 的部分，`common` 不變，所以 `CHANGES.md` 不記。

## 3. 過程

### 3.1 AGENTS-local.md（2026-11-13）

- 在 `## Branches` 之後加 `## Commits`，三行 STE：不加 `Co-Authored-By`，快照也一樣，`.claude/settings.json` 讓 Claude Code 不加。
- Technical words 加上 commit、line、message。
- `gen_agents_md.py` 寫出 `AGENTS.md`，`CLAUDE.md` 不變；`--check` 兩個都是 PASS。

### 3.2 .claude/settings.json（2026-11-13）

- repo 原本沒有 `.claude/`，這台也沒有 `~/.claude/settings.json`。
- 新建 `.claude/settings.json`，只有 `attribution`：`{"commit": "", "pr": "", "sessionUrl": false}`。用物件的寫法，不寫 `"attribution": false`，因為舊版的 Claude Code 會因此略過整個設定檔。
- 存檔之後，這個 session 收到的系統提示就改成「不加 attribution」。

## 4. 要做的

1. ✅ 改 `AGENTS-local.md`，重新產生 `AGENTS.md`（`3.1`）。
2. ✅ 建 `.claude/settings.json`（`3.2`）。
3. ✅ 要不要在 `CHANGES.md` 記一筆：只改本 agency 的 local 部分，不記。

## 5. 驗證

- `gen_agents_md.py --check`、`check_tasks.py` 與 `check_chores.py` 都是 PASS。
- `.claude/settings.json` 是正確的 JSON。
- 下一個 commit 沒有 `Co-Authored-By`。

## 6. 與其他 task 的關係

- [[Task 106]]：拿掉 [[publish-gestalt]] 第 4 步的 `--co-author`；本 task 讓其他 commit 也不加。

## 7. 知識

—

## 8. 日誌

### 2026-11-13

- 建立 task：使用者要求兩個做法都做：`AGENTS-local.md` 加 `## Commits`，重新產生 `AGENTS.md`，寫成 `3.1`；建 `.claude/settings.json`，寫成 `3.2`。Status 是完成。
