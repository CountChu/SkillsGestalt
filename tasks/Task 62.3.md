# Task 62.3 - 建立 InvestForge 的 task 與 chore

**Status**：完成——2026-10-18 InvestForge 的 `tasks/`、摘要表與 Task 1、根目錄 CLAUDE.md 的 Tasks 一節都建好，兩份規則檔寫進 `Task N @ <workspace>`；使用者看過。
**Raised**：2026-10-18，[[Task 62]] 拆出的第 3 步：搬過去的 task 與 chore 要有地方放。
**Depends on**：[[Task 62.1]]

## 1. 背景

- InvestForge 的根目錄有 `.obsidian`，是自己的 vault；裡面沒有任何 `Task N.md`、`Chore N.md` 或摘要表。
- InvestForge 的 CLAUDE.md 是英文；它的 `config.yaml` 有一個 `dashboardDir`，指向 repo 外產生的頁面，和 repo 裡的 `dashboard/` 是兩回事。
- InvestForge 的 `.gitignore` 不忽略 `tasks/`、`chores/` 與 `dashboard/`；`checkpoints/` 被忽略，和這裡一樣。
- InvestForge 的 git log 有 40 個 `task N:` commit，用的是這裡的編號：14、18、19、28、32、32.8、33、44–48。
- InvestForge 有自己的 Claude memory，共 19 條，沒有這裡關於 task 的那幾條。
- 2026-10-18 試過：`check_tasks.py` 與 `check_chores.py` 遇到沒有任何列的摘要表都 PASS，所以表可以先是空的。
- 在 [[Task 62.7]] 做完之前，這裡的 session 還會在 InvestForge commit，前綴用這裡的編號，例如 2026-10-18 的 d3828bf `task 32.10:`。

## 2. 現況

### 已決定（2026-10-18）

動手前問了 10 個問題：

- InvestForge 的 Task 1 就是「建立本 workspace 的 task 與 chore」：建立制度也記成 task，和這裡的 [[Task 53]] 一樣。
  InvestForge 的 commit 從第一個起就用自己的編號；[[Task 62.4]] 搬去的 9 個從 Task 2 起。
- InvestForge 的 CLAUDE.md 寫 common 的路徑時，寫成 `{skillGroups.common}`，照它的 Workspace configuration 一節代換，不寫死路徑。
- InvestForge 摘要表的開頭寫一句：commit 前綴的 task N 指那裡的 Task N；Task 1 之前的 commit，以及這裡的 session 在那裡做的 commit，指這裡的編號。
- `chores/` 等第一個 chore 再建：InvestForge 的 `chores/`、`dashboard/chore-summary.md` 與根目錄 CLAUDE.md 的 Chores 一節，由 [[Task 62.5]] 建第一個 chore 時一起建。
- Tasks 一節放在 InvestForge 的 CLAUDE.md 的「繁體中文 twins」之後、「Python environment」之前。
- 提到別的 workspace 的 task 時，寫成純文字 `Task N @ <workspace>`，例如 `Task 62 @ SkillsGestalt`，不加連結；這個寫法也寫進 task-rules.md 與 chore-rules.md 的 Links 一節，chore 是 `Chore N @ <workspace>`。
- InvestForge 的 Task 1 在 `tasks/`、摘要表與 Tasks 一節建好時就完成。
- 驗證只檢查內容：讀 InvestForge 的 CLAUDE.md，代換 `{skillGroups.common}` 之後規則檔存在，指令在 InvestForge 的根目錄跑得通。

### 結果（2026-10-18）

- InvestForge：`tasks/Task 1.md`、`dashboard/task-summary.md`，根目錄 CLAUDE.md 加上 `## Tasks` 一節（10 行）。
  從 InvestForge 的根目錄跑 `check_tasks.py`：18 項 PASS。
  照 CLAUDE.md 的 Workspace configuration 代換 `{skillGroups.common}`，`rules/task-rules.md` 存在，指令跑得通。
- 這裡：task-rules.md、chore-rules.md 與中文版的 Links 一節改成 `Task N @ <workspace>` 的寫法；`check_ste.py --ste` PASS，`check_parity.py` 0 failure。
- [[Task 62.4]] 第 1 步引用這裡的 task 時改用這個寫法；[[Task 62.5]] 加上建 InvestForge 的 `chores/` 這件事。

## 3. 要做的

1. ✅ 建 InvestForge 的 `tasks/` 與 `dashboard/task-summary.md`：開頭說明、表頭與圖例，照 [[Task 62.1]] 的規則檔；`tasks/` 裡是 Task 1。
2. ✅ InvestForge 根目錄的 CLAUDE.md 加上 `## Tasks` 一節，用英文：照 task-rules.md 做，並寫出檢查指令。
   `tasks/` 裡不放 CLAUDE.md，和這裡一樣。
3. ✅ `dashboard/task-summary.md` 的開頭註明 commit 前綴的編號屬於哪一個 workspace。
4. ✅ 在 InvestForge 的根目錄跑 `check_tasks.py`。
5. ✅ 使用者看過之後 commit：InvestForge 一個，前綴 `task 1`；這裡一個，前綴 `task 62.3`。

## 4. 驗證

- 在 InvestForge 的根目錄跑 `check_tasks.py`，PASS；`check_chores.py` 等 [[Task 62.5]] 建了 `chores/` 再跑。
- 只讀 InvestForge 的 CLAUDE.md，就找得到 task 的規則與檢查指令。

## 5. 與其他 task 的關係

- [[Task 62.4]]、[[Task 62.5]]：把 task 與 chore 搬進本 task 建好的地方；[[Task 62.5]] 也建 InvestForge 的 `chores/`。
- [[Task 62.7]]：做完之後，這裡的 session 不再在 InvestForge commit。

## 6. 日誌

### 2026-10-18

- 從 [[Task 62]] 拆出。
- 在 scratchpad 試過：兩支檢查遇到空的摘要表都 PASS。
- [[Task 62.1]] 決定根目錄的 CLAUDE.md 直接指向規則檔，所以 InvestForge 不建資料夾裡的 CLAUDE.md；第 3 章跟著改。
- 開始：問了 10 個問題，見「已決定」。
- 建好 InvestForge 的 `tasks/`、摘要表、Task 1 與 CLAUDE.md 的 Tasks 一節；兩份規則檔的 Links 一節寫進 `Task N @ <workspace>`。
- 使用者看過，同意 commit；本 task 完成。
