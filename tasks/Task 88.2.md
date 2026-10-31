# Task 88.2 - 接上 SkillsGestalt 的指南 forge-setup.md

**Status**：完成——2026-10-31 寫好 [forge-setup.md](../.github/common/references/forge-setup.md) 與中文版：七個編號步驟從零建立一個 Forge，加上舊 workspace 怎麼改、SkillsGestalt 改了之後怎麼辦；照它在暫用資料夾從零接上，三個檢查都 PASS。
**Raised**：2026-10-31，[[Task 88]] 拆出的第 2 步：新的 Forge 要做哪些事，寫成一份照著做就能接上的指南。
**Depends on**：[[Task 88.1]]

## 1. 背景

- 接上 SkillsGestalt 要做的事散在 [[Task 82]] 到 [[Task 87]]、[chore-rules.md](../.github/common/rules/chore-rules.md)、[CLAUDE-tmp.md](../.github/common/templates/CLAUDE-tmp.md) 與 `gen_claude_md.py` 的說明裡。
- InvestForge 是靠 Task 13 @ InvestForge 的 session 收到一則則訊息才接上的。

## 2. 現況

- [forge-setup.md](../.github/common/references/forge-setup.md) 與 [中文版](../.github/common/references/forge-setup-tw.md)，以 STE 寫，例子用虛構的 BookForge：
  - Make a Forge：七個編號步驟，每步一個動作、一個檢查——建立根目錄與 git repository、複製 [config-forge-tmp.yaml](../.github/common/templates/config-forge-tmp.yaml) 並換掉佔位符、寫 `CLAUDE-local.md`、以 `gen_claude_md.py` 產生 CLAUDE.md、把設定記成 Task 1 並寫 task 摘要表、寫 chore 摘要表（一列文字的 [[keep-english]]）、commit。
    後面附三段照抄就能過檢查的內容：`tasks/Task 1.md`、`dashboard/task-summary.md`、`dashboard/chore-summary.md`。
  - Change an Older Workspace：把自己的規則搬到 `CLAUDE-local.md`、補上 `agencies` 與 `keepEnglishChore`、和 SkillsGestalt 做同樣工作的 chore 改成文字的一列、自己的 chore 取名稱，再做第 4 到 7 步。
  - After a Change in SkillsGestalt：Forge 直接讀 SkillsGestalt，改了之後再跑三個檢查。
- [README.md](../README.md) 與中文版的 Gestalt and Forge 一節、[glossary.md](../.github/common/references/glossary.md) 與中文版的 Forge、`config-forge-tmp.yaml` 開頭的註解，都加一句連到指南。

## 3. 要做的

### 已決定（2026-10-31）

- 指南放在 `.github/common/references/forge-setup.md`，和 glossary.md 一起；以 STE 寫，另有 `-tw.md` 中文版。

### 開始做時決定的（2026-10-31）

- 範圍：從零建立一個 Forge 是主流程，另加一節短的「舊的 workspace 怎麼改」，BookMaster 用得上。
- 摘要表在指南裡給最小的內容，照抄就能過檢查；chore 摘要表先放 [[keep-english]] 那一列，並說明 Title 與何時要做要和定義一樣。
- 連到指南的地方：README 與中文版、glossary.md 與中文版、`config-forge-tmp.yaml` 的開頭註解。
- 不寫 VS Code 的 `.code-workspace` 設定。
- 例子用虛構的 BookForge。
- 步驟寫成編號，每步一個動作、一個檢查。
- 第一個 task：沒有 `tasks/` 時 `check_tasks.py` 會停下來，而 git 不保留空目錄；所以照 InvestForge 當初的做法，把這次的設定記成 Task 1，指南附上它的內容。

## 4. 驗證

- 照指南在一個新的暫用資料夾從零接上本 repo：`gen_claude_md.py --check`、`check_tasks.py` 與 `check_chores.py` 都是 PASS。
- 指南 `check_ste.py` 是 PASS，與中文版 `check_parity.py` 是 0 failure。

2026-10-31 的結果：

- 照指南在全新的暫用資料夾從零做：`config.yaml` 由範本換掉佔位符；`CLAUDE-local.md` 一節；`gen_claude_md.py` 寫出 CLAUDE.md，`--check` 是 PASS；三個檔的內容直接從指南的 fenced block 取出；照 CLAUDE.md 給的指令，`check_tasks.py` 與 `check_chores.py` 都是 18 passed；沒有 `chores/`；commit 之後 `git status` 沒有變動。
- 走這一遍時發現第 2 步原本的檢查「`config.yaml` 裡沒有 `{`」不成立，因為範本的註解本身有 `{`；改成「`config.yaml` 的值裡沒有三個佔位符」。
- 指南與 glossary.md 的 `check_ste.py` 是 PASS；指南、README、glossary 三組中英對照 `check_parity.py` 都是 0 failure，`diff_md.py --verify` 確認 README 與 glossary 的中文版只改了新加的一行；`reformat_md.py --mode clean` 不改動。

## 5. 與其他 task 的關係

- [[Task 88]]：本 task 是它的第 2 步。
- [[Task 88.1]]：指南引用它的範本。
- BookMaster 改成新的機制時，可以當這份指南的第一個試用者，在 BookMaster 自己的 tasks 做。

## 6. 知識

—

## 7. 日誌

### 2026-10-31

- 建立：寫 `forge-setup.md` 與中文版，等 [[Task 88.1]] 的範本。
- 開始做並完成：寫好指南與中文版，README、glossary 與設定範本連到它；照指南從零接上一次，三個檢查都 PASS。
