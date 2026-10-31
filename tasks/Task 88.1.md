# Task 88.1 - Forge 用的 config.yaml 範本

**Status**：完成——2026-10-31 寫好 [config-forge-tmp.yaml](../.github/common/templates/config-forge-tmp.yaml)：五個鍵加上 `wikiRootDir`，說明寫在註解，要填的值用 `{GESTALT_ROOT}`、`{WIKI_DIR}`、`{WIKI_ROOT_DIR}`。
**Raised**：2026-10-31，[[Task 88]] 拆出的第 1 步：Forge 要設哪些鍵，現在沒有一個地方寫出來。
**Depends on**：—

## 1. 背景

- [config.example.yaml](../config.example.yaml) 是本 repo 自己的設定範例：`wikiDir`、`skillGroups.common` 是相對路徑 `.github/common`、`keepEnglishChore`。
- Forge 要的設定不一樣：`skillGroups.common` 是本 repo 的絕對路徑（可用 `~`）、`agencies` 給出本 repo 的根目錄、`keepEnglishChore` 的 chore 在本 repo；InvestForge 還有 `wikiRootDir`、`dashboardDir`、`dedi`。
- [[Task 85]] 當時決定 `config.example.yaml` 不加 `agencies` 的範例；這裡改成另寫一份範本，不動本 repo 自己的。

## 2. 現況

- [config-forge-tmp.yaml](../.github/common/templates/config-forge-tmp.yaml)：開頭的註解說明它給誰用、怎麼用（複製成根目錄的 `config.yaml`、換掉每個佔位符）、相對路徑與 `~`、以 `{` 開頭的值要保留引號，以及術語在 glossary.md。
- 鍵：`wikiDir`、`wikiRootDir`、`skillGroups`（`common` 是 `{GESTALT_ROOT}/.github/common`、`dedi` 預設 `.claude`、`external` 空著）、`agencies.SkillsGestalt` 是 `{GESTALT_ROOT}`、`keepEnglishChore` 預設 `keep-english`；每個鍵的說明寫在行尾的英文註解。

## 3. 要做的

### 已決定（2026-10-31）

- 另寫一份 Forge 用的範本，例如 `{skillGroups.common}/templates/config-forge-tmp.yaml`；本 repo 的 `config.example.yaml` 不動。

### 開始做時決定的（2026-10-31）

- 檔名是 `config-forge-tmp.yaml`，放在 `{skillGroups.common}/templates/`，和其他範本一樣用 `-tmp`。
- 收的鍵：`wikiDir`、`skillGroups`（`common`、`dedi`、`external`）、`agencies`、`keepEnglishChore`，再加 `wikiRootDir`；`dashboardDir` 是 InvestForge 自己的，不收。
- 每個鍵的說明寫在範本的註解，複製之後跟著走；註解用英文，沒有中文版。
- 要填的值用 `{UPPER_SNAKE}` 佔位符：`{GESTALT_ROOT}`、`{WIKI_DIR}`、`{WIKI_ROOT_DIR}`；`dedi` 與 `keepEnglishChore` 給預設值 `.claude` 與 `keep-english`。
- 以 `{` 開頭的值加上引號：沒有引號時，YAML 會把它讀成 mapping。

## 4. 驗證

- 以範本做出的 `config.yaml`，讓 `gen_claude_md.py` 產生 CLAUDE.md，`check_chores.py` 找得到 [[keep-english]] 的定義。

2026-10-31 的結果：

- 範本以 `yaml.safe_load` 讀得進來，`external` 是空值。
- 暫用資料夾直接複製範本、不填佔位符：`gen_claude_md.py` 找不到 `{GESTALT_ROOT}/.github/common/templates/CLAUDE-tmp.md`，以 `2` 結束；`check_chores.py` 找不到 [[keep-english]] 的定義而 FAIL。
- 填好佔位符之後：`gen_claude_md.py` 寫出 CLAUDE.md，標題是資料夾的名稱，指令用 `~/…/SkillsGestalt/.github/common/scripts/…`，keep-English chore 連到 SkillsGestalt 的 `chores/keep-english.md`；摘要表一列文字的 `keep-english`，`check_chores.py` 是 18 passed。
- 拿掉 `keepEnglishChore` 那一行，產生的 CLAUDE.md 就沒有 keep-English chore 那一句。

## 5. 與其他 task 的關係

- [[Task 88]]：本 task 是它的第 1 步。
- [[Task 88.2]]：指南引用這份範本。
- [[Task 85]]：當時決定 `config.example.yaml` 不加 `agencies`。

## 6. 知識

—

## 7. 日誌

### 2026-10-31

- 建立：另寫一份 Forge 用的 config.yaml 範本。
- 開始做並完成：寫好 `config-forge-tmp.yaml`，在暫用資料夾試過不填、填好與拿掉 `keepEnglishChore` 三種情況。
