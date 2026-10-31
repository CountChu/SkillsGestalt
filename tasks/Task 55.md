# Task 55 - 建立依賴巡檢的 chore：定期找出檔頭紀錄過期的文件

**Status**：尚未開始——2026-10-18 記下；試掃時已找到兩筆過期的紀錄，留作第一次巡檢的對象。
**Raised**：2026-10-18，檢視哪些 task 適合做成 chore 時提出：只有 asd-ste 取代原檔時與 [[rerecord-ste-custom]] 會重記依賴，其他人改了被依賴的檔，依賴它的文件就悄悄過期。
**Depends on**：—

## 1. 背景

- 文件在 header quote 記下它依賴的每份檔案的日期與指紋（[[Task 8]]）；被依賴的檔一改，`depends_on.py check` 就報 CHANGED，要有人讀過改動、確認依賴方仍然成立，再重記。
- 目前只有兩處會主動這樣做：asd-ste 的 Step 7 取代原檔時找出依賴方並重記，[[rerecord-ste-custom]] 重記 ste-custom.md；其他的修改之後，依賴方沒有人檢查。
- check-md-deps 的 [scan_md_deps.py](../.github/common/skills/check-md-deps/scripts/scan_md_deps.py) 可以一次掃一整個資料夾：每份文件 header quote 的每一筆紀錄，以及中文版是否跟上英文。
- 2026-10-18 試掃 SkillsGestalt 的 `.github` 與 `mods`：102 份文件中 45 份有依賴，紀錄 109 筆 UNCHANGED、2 筆 CHANGED、36 筆 UNRESOLVED，中文版 38 份都跟上了。
  - CHANGED 的兩筆：check-md-deps 的 SKILL.md 與 SKILL-tw.md 記的 check-wiki-doc 的 SKILL.md，一直沒有人發現。
  - UNRESOLVED 的 36 筆是 README-tmp 草稿檔頭的 `{COMMON_PATH}` 連結，範本本來就解析不了。
- [[Task 18]]、Task 30 那類「RSDC 沒跟上範本」，也會以 CHANGED 出現在巡檢裡；對齊本身要判斷，照舊開 task。

## 2. 現況

### 已決定（2026-10-18）

- 範圍：本 workspace 的全部 md；wiki 的筆記有自己的 check-wiki-doc，不列進來；2026-10-19 起不含其他 workspace（[[Task 62.5]]）。
- 試掃找到的兩筆，留作第一次巡檢的對象：讀過 check-wiki-doc 的改動、確認 check-md-deps 仍然成立，再重記。
- 提交：本 task 的修改前綴 `task 55`。

### 要決定的

- 何時要做：例如每週一次，或當天 commit 很多的時候。
- 怎麼處理 CHANGED：讀過改動仍然成立就重記；不成立的，修正或另開 task。
- 怎麼分 UNRESOLVED：範本的佔位符是正常的，其他的要查原因。
- 要不要寫一支包裝腳本：掃本 workspace 一次，只列出 CHANGED 與 UNRESOLVED，並和上次比。
- 和 [[rerecord-ste-custom]] 的分工：ste-custom.md 的紀錄由 Chore 1 自動重記，巡檢要不要略過它。

## 3. 要做的

1. 決定「要決定的」五項，照 [chore-rules.md](../.github/common/rules/chore-rules.md) 建立 chore 與摘要表的一列。
2. 需要的話，寫包裝腳本。
3. 跑第一次：處理試掃找到的兩筆。

## 4. 驗證

- `check_chores.py` 與 `check_tasks.py` 都 PASS。
- 第一次巡檢之後，`scan_md_deps.py` 對本 workspace 沒有 CHANGED，UNRESOLVED 都有交代。

## 5. 與其他 task 的關係

- [[Task 8]]：決定文件以指紋記錄依賴。
- [[Task 53]]：建立 chore 制度。
- [[rerecord-ste-custom]]：只管 ste-custom.md 的紀錄，可以自動重記。
- [[Task 18]]、Task 30：RSDC 跟上範本；巡檢會找出它們還沒跟上的部分。

## 6. 知識

—

## 7. 日誌

### 2026-10-30

- [[Task 86]] 把 chore 改用名稱：本檔的 `[[Chore N]]` 連結改成新名稱。

### 2026-10-19

- 範圍改成本 workspace 的全部 md，「要決定的」的包裝腳本與驗證跟著改（[[Task 62.5]]）。

### 2026-10-18

- 建立：記下試掃的結果與兩筆過期的紀錄。
- 第 3 章連到的 `chores/CLAUDE.md` 已刪除，改連 [chore-rules.md](../.github/common/rules/chore-rules.md)（[[Task 62.1]]）。
- 指向 Task 30 的 wikilink 改成純文字：它已移出本 workspace（[[Task 62.4]]）。
