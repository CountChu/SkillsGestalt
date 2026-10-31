# Task 88 - 讓別的 agency 能自己接上 SkillsGestalt

**Status**：完成——2026-10-31 三個 sub task 都完成：Forge 用的設定範本、接上的指南 forge-setup.md，以及 CHANGES.md 與 chore follow-gestalt。
**Raised**：2026-10-31，使用者問 SkillsGestalt 現在的架構是否已經能被別的 agency 引用；InvestForge 已經在用，但新的 Forge 要靠人帶才接得上。
**Depends on**：—

## 1. 背景

- InvestForge 已經實際使用 SkillsGestalt：`skillGroups.common` 指向本 repo 的 `.github/common`，CLAUDE.md 由 `CLAUDE-local.md` 與模板產生，keep-English 稽核透過 `agencies` 做 [[keep-english]]；`gen_claude_md.py --check` 與 `check_chores.py` 都是 PASS。
- 但怎麼接上，散在 [[Task 82]] 到 [[Task 87]]、[chore-rules.md](../.github/common/rules/chore-rules.md) 與 [CLAUDE-tmp.md](../.github/common/templates/CLAUDE-tmp.md) 裡，README 的 Getting Started 只講本 repo 自己。
- `config.example.yaml` 是本 repo 自己的例子，沒有 Forge 會用到的 `agencies`，也沒說明每個鍵。
- Forge 直接讀本 repo 的工作目錄，本 repo 一改，Forge 立刻跟著變；[[Task 86]] 改了 `check_chores.py`，InvestForge 就有一陣子 FAIL，靠手動通知 Task 13 @ InvestForge 的 session 才修好。

## 2. 現況

### 各 agency 的情況（2026-10-31）

- InvestForge：照新的機制，CLAUDE.md 與 chore 的檢查都 PASS，沒有 `chores/`。
- BookMaster：`config.yaml` 指向本 repo，但 CLAUDE.md 仍是手寫的舊版，沒有 `CLAUDE-local.md`，也沒有 `chores/`。

## 3. 要做的

依編號順序做；[[Task 88.2]] 依賴 [[Task 88.1]]，[[Task 88.3]] 可以單獨做。

- [[Task 88.1]] ✅ Forge 用的 config.yaml 範本
- [[Task 88.2]] ✅ 接上 SkillsGestalt 的指南 forge-setup.md
- [[Task 88.3]] ✅ 改了會影響 Forge 的東西時怎麼通知

## 4. 驗證

- 三個 sub task 都完成。
- 照指南，在一個新的暫用資料夾從零接上本 repo：`gen_claude_md.py --check`、`check_tasks.py` 與 `check_chores.py` 都是 PASS。

## 5. 與其他 task 的關係

- [[Task 81]]：術語表的 agency、Gestalt 與 Forge。
- [[Task 84]]、[[Task 85]]、[[Task 86]]、[[Task 87]]：Forge 接上時要用的機制。
- BookMaster 改成新的機制，在 BookMaster 自己的 tasks 做；它可以當指南的第一個試用者。
- GitHub 上的公開版還停在 `258940e`，之後的機制都還沒發佈；發佈照 [[publish-github]]，由使用者決定時機。

## 6. 知識

—

## 7. 日誌

### 2026-10-31

- 建立 task 與三個 sub task：Forge 的設定範本、接上的指南、改動的通知方式。
- [[Task 88.1]] 完成，本 task 改成進行中。
- [[Task 88.2]] 完成：`forge-setup.md` 與中文版。
- [[Task 88.3]] 完成：`CHANGES.md` 與 [[follow-gestalt]]；本 task 完成。
