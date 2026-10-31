# Task 62.1 - task 與 chore 的規則搬進 common

**Status**：完成——2026-10-18 兩份 STE 規則檔與中文版搬進 common，根目錄 CLAUDE.md 直接指向它們，資料夾裡的兩份 CLAUDE.md 刪掉，51 個連結改好；使用者看過規則檔。
**Raised**：2026-10-18，[[Task 62]] 拆出的第 1 步：兩個 workspace 要照同一份規則寫 task 與 chore。
**Depends on**：—

## 1. 背景

- `tasks/CLAUDE.md` 與 `chores/CLAUDE.md` 的規則幾乎都與 workspace 無關。
  只有連結的範例（`../.github/common/...`）與檢查指令（`python .github/common/scripts/check_tasks.py ...`）的路徑是這裡的。
- 有幾條做法只記在這裡的 Claude memory；memory 依專案的路徑分開，InvestForge 的 session 讀不到：
  - task 檔用繁體中文寫、保留英文術語、沒有中文版。
  - task 的 commit 前綴是小寫的 `task N: `；chore 的前綴寫在 `chores/CLAUDE.md`，task 的卻只在 memory。
  - 別的 session 會同時改這些檔，只 commit 自己的 hunk。
  - 摘要表與父 task 的檔，用 HEAD 加上自己的行組成 blob 再 stage，不 `git add` 整個檔。
  - 確認 HEAD 的那一步用 `&&` 串到 staging、`git add` 與 `git commit`，不單獨一行。

## 2. 現況

### 已決定（2026-10-18）

動手前問了 10 個問題：

- 兩份規則檔：`task-rules.md` 與 `chore-rules.md`，各自寫完整；兩份共用的約 10 條規則，兩份都寫。
- 直接用 STE 寫，以 `check_ste.py --ste` 檢查到沒有 FAIL，再請使用者看過；中文版照 chinese skill 寫。
- 只記在 memory 的提交做法，寫進兩份規則的 Commits 一節，再加一條：commit 之前確認 index 裡只有自己的路徑。
- 編號規則寫 [[Task 62.2]] 之後的版本：號碼不重複、可以有空號、用過不再用。
- task 與 chore 檔用繁體中文寫，寫成規定：章名與狀態字本來就是中文，`check_tasks.py` 也只認中文。
- 根目錄 CLAUDE.md 的 Tasks、Chores 兩節直接指向規則檔，並寫出本 workspace 的檢查指令。
- 刪掉 `tasks/CLAUDE.md` 與 `chores/CLAUDE.md`：根目錄直接指向規則檔之後，InvestForge 的 `tasks/`、`chores/` 也不用再維護各自的 CLAUDE.md。
  連到它們的 51 個檔跟著改：舊日誌的連結改成 inline code，字句不變，其他的改連規則檔。
- memory 的 workspace-tasks-md 與 task-commit-prefix 縮成指向規則檔，只留當初的事件。
- 中文版照原本 `tasks/CLAUDE.md` 的中文寫法，把 task、sub task、chore、wikilink、vault、session，以及 git 的 stage、index、blob、HEAD 留英文；這次不改 keep-English list，另開 [[Task 63]]。

### 結果（2026-10-18）

- [task-rules.md](../.github/common/rules/task-rules.md)（154 行）與 [chore-rules.md](../.github/common/rules/chore-rules.md)（134 行）：STE，`check_ste.py --ste` PASS，沒有 warning。
  檔頭的兩筆 STE 紀錄由 `depends_on.py record` 寫入，`depends_on.py check` 都是 UNCHANGED。
  兩份只寫「照 md-style.md」，不重述它的規則。
- 中文版 `task-rules-tw.md` 與 `chore-rules-tw.md`：照 chinese skill，FULL，line for line；`check_parity.py --keep` 都是 0 failure、沒有 warning。
  兩處「步驟」照 keep-English list 改留 step；3df3b36 加進清單的 alias 指的是 shell 的指令，連結的「別名」照舊翻譯。
- 根目錄 [CLAUDE.md](../CLAUDE.md)：Tasks、Chores 兩節照規則檔做，並寫出兩個檢查指令。
- 刪掉 `tasks/CLAUDE.md` 與 `chores/CLAUDE.md`。
- 51 個連結：43 個 task 的 2026-10-16 日誌改成 inline code，各記一行日誌；兩張摘要表的開頭改連規則檔與根目錄的 CLAUDE.md；[[Task 54]]、[[Task 55]]、[[Task 56]] 改連 chore-rules.md；[[Task 61]] 與本 task 改成 inline code；根目錄 CLAUDE.md 改連規則檔。
- memory 的兩條縮成指向規則檔。

## 3. 要做的

1. ✅ 在 `.github/common/rules/` 寫英文的規則檔：`tasks/CLAUDE.md` 與 `chores/CLAUDE.md` 中與 workspace 無關的部分，加上第 1 章只記在 memory 的做法。
   路徑一律從 workspace 的根目錄算起；common 的路徑寫成 `{skillGroups.common}`，不點名任何一個 workspace。
2. ✅ 中文版照 [chinese](../.github/common/skills/chinese/SKILL.md) skill 寫。
3. ✅ 根目錄 CLAUDE.md 直接指向規則檔，刪掉 `tasks/CLAUDE.md` 與 `chores/CLAUDE.md`，改連到它們的 51 個檔。
4. ✅ memory 的 workspace-tasks-md 與 task-commit-prefix 改成指向規則檔，不再重複規則的內容。
5. ✅ 使用者看過兩份規則檔與中文版。
6. ✅ commit：前綴 `task 62.1`；摘要表與父 task 的檔照規則用 blob stage。

## 4. 驗證

- 規則檔與中文版的 `check_parity.py` 都是 0 failure。
- 這裡沒有 `tasks/CLAUDE.md` 與 `chores/CLAUDE.md`，也沒有連到它們的連結。
- `check_tasks.py` 與 `check_chores.py` PASS。

## 5. 與其他 task 的關係

- [[Task 61]]：規則檔不重寫 md-style 已有的規則，改成 follow md-style；兩份規則共用的約 10 條規則是使用者選的寫法，[[Task 61]] 的日誌記了這一點。
- [[Task 62.2]]：規則檔已經照改過之後的腳本寫編號規則，腳本要跟上。
- [[Task 62.3]]：InvestForge 的根目錄 CLAUDE.md 照本 task 的寫法指向規則檔，不建資料夾裡的 CLAUDE.md。
- [[Task 63]]：中文版留英文的新詞要不要加進 keep-English list。
- [[rerecord-ste-custom]]：兩份規則檔也記錄 ste-custom.md，ste-custom.md 再改時一起重記。

## 6. 日誌

### 2026-10-30

- [[Task 86]] 把 chore 改用名稱：本檔的 `[[Chore N]]` 連結改成新名稱。

### 2026-10-18

- 從 [[Task 62]] 拆出。
- 開始：問了 10 個問題，見「已決定」。
- 寫好兩份 STE 規則檔與中文版，根目錄 CLAUDE.md 改成直接指向它們，刪掉資料夾裡的兩份 CLAUDE.md，改了 51 個檔的連結，縮短 memory 的兩條；另開 [[Task 63]]。
- 使用者看過規則檔，同意 commit；本 task 完成。
