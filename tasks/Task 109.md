# Task 109 - SkillsGestalt 的 config.example.yaml 改為 config-tmp.yaml

**Status**：完成——`config.example.yaml` 改名為 `config-tmp.yaml`，`wikiDir` 寫成 `{wikiDir}`；這台的 `config.yaml` 由 `gen_config.py` 產生，clone-gestalt 與 pull-gestalt 跟著改。
**Raised**：2026-11-13，[[Task 108]] 做完 `gen_config.py` 之後，使用者要 SkillsGestalt 自己也用 `config-tmp.yaml`。
**Depends on**：[[Task 108]]

## 1. 背景

- [[Task 108]] 加了 [gen_config.py](../skill-groups/common/scripts/gen_config.py)，用 `config-tmp.yaml` 與 `config.local.yaml` 產生 `config.yaml`；它的 `3.5` 原本決定 SkillsGestalt 自己不改。
- SkillsGestalt 的 `config.yaml` 本來就不在 git，各台從 `config.example.yaml` 手動複製，再改 `wikiDir`。
- 手動複製的問題：範本加了新的 key（例如 `cleanCheckpoints`）時，各台的 `config.yaml` 不會跟著變，也沒有檢查會發現。
- 這台的 `config.yaml` 和 `config.example.yaml` 去掉註解後，只差 `wikiDir` 一行。

## 2. 結論

- `config.example.yaml` 以 `git mv` 改名為 [config-tmp.yaml](../config-tmp.yaml)；`wikiDir` 寫成 `"{wikiDir}"`，開頭的註解改成說明 `gen_config.py` 與 `config.local.yaml`（`3.1`）。
- 這台寫了 `config.local.yaml`，只有 `wikiDir` 一行；產生的 `config.yaml` 和原本的只差開頭的註解（`3.1`）。
- `.gitignore` 加上 `/config.local.yaml`。
- 每個說 `config.example.yaml` 的檔都改了；`tasks/` 與 `dashboard/` 是過去的紀錄，不改（`3.2`）。
- clone-gestalt 第 5 步改成寫 `config.local.yaml`，第 8 步改跑 `gen_config.py`；pull-gestalt 第 9 步改跑 `gen_config.py`（`3.3`）。
- 別台電腦（例如 `countdell`）pull 之後，要照 clone-gestalt 第 5 步寫自己的 `config.local.yaml`；pull-gestalt 第 9 步寫了這件事。

**表 1：改的檔**

| 檔 | 改了什麼 |
| --- | --- |
| `config.example.yaml` → `config-tmp.yaml` | 改名；`wikiDir` 是 `{wikiDir}`；開頭三行註解 |
| `.gitignore` | 加 `/config.local.yaml`，註解改成說 `gen_config.py` |
| `AGENTS-local.md`、`AGENTS.md` | Settings of This Agency 說 `config.yaml` 由 `config-tmp.yaml` 與 `config.local.yaml` 產生 |
| `README.md`、`README-tw.md` | Getting Started 第 1 步改成寫 `config.local.yaml`、跑 `gen_config.py` |
| `chores/clone-gestalt.md` | 第 5、8 步，`4. 驗證`，`5.` 加本 task |
| `chores/pull-gestalt.md` | 第 9 步，`4. 驗證`，`5.` 加本 task |
| `chores/publish-gestalt.md` | 不進 git 的檔加上 `config.local.yaml` |
| `chores/clean-checkpoints.md` | 範例的連結 |
| `skill-groups/common/CHANGES.md` | 兩筆舊條目的範例連結，不然會斷 |
| `skill-groups/common/skills/clean-checkpoints/README.md` | When the Skill Is Changed 的檔名 |
| 10 個舊 task 檔 | 連到 `config.example.yaml` 的連結，目標改成 `config-tmp.yaml`，文字不改 |

## 3. 過程

### 3.1 改名與這台的 config.local.yaml（2026-11-13）

- `git mv config.example.yaml config-tmp.yaml`；`wikiDir` 加引號，因為 `{` 開頭的值不加引號，YAML 會讀成 mapping。
- 註解說：路徑用 `/`，因為值放進雙引號裡，`\` 會被當成跳脫字元。
- `config.local.yaml` 的 `wikiDir` 從原本的 `config.yaml` 抄過來；先確認 `git check-ignore` 忽略它，才寫它。
- 跑 `gen_config.py`：產生的 `config.yaml` 第 2 行以後，和原本的只差開頭的註解，其他每一行都一樣。

### 3.2 說 config.example.yaml 的檔（2026-11-13）

- `git grep config.example`：`tasks/` 與 `dashboard/` 以外有 9 個檔，另有 `AGENTS.md`，由 `AGENTS-local.md` 產生。
- `README-tw.md` 是 `README.md` 的 twin，同一行一起改。
- `CHANGES.md` 2026-11-12 與 2026-11-10 兩筆舊條目連到 `config.example.yaml`，改成 `config-tmp.yaml`，不留斷掉的連結。
- `check_tasks.py` 的連結檢查找出 10 個 task 檔連到 `../config.example.yaml`：Task 78、84、88.1、90、91、97.7、100.1、102、104、108。
  它們是過去的紀錄，所以只把連結的目標改成 `../config-tmp.yaml`，連結文字照舊寫 `config.example.yaml`；Task 108 的 `3.5` 另寫明改了名。
- `publish_snapshot.py check` 的 home 掃描把 [[Task 108]] 例子裡 Windows 使用者目錄下的路徑當成 home 目錄：`CHANGES.md` 一處、`gen_config.py` 兩處。例子改成 `D:/Work`，`config-tmp.yaml` 的例子也改成 `D:/Notes/MyVault`；commit 之後掃描是 `nothing found`。

### 3.3 chore 的步驟（2026-11-13）

- clone-gestalt：第 5 步寫 `config.local.yaml`，不改 `config-tmp.yaml`；第 8 步的 `gen_config.py` 產生 `config.yaml`，再跑 `gen_agents_md.py`。第 7 步建 `.venv` 只用到 `skillGroups.common` 的預設值，所以 `config.yaml` 在第 8 步才產生也可以。
- pull-gestalt：第 9 步改跑 `gen_config.py`；沒有 `config.local.yaml`，或用了它沒有的名稱時，以 `2` 結束，照 clone-gestalt 第 5 步寫這台的值。
- 兩個 chore 的 `4. 驗證` 改成 `gen_config.py --check`；clone-gestalt 的 `git status` 也不能列出 `config.local.yaml`。

## 4. 要做的

1. ✅ 改名、寫 `config.local.yaml`、產生 `config.yaml`（`3.1`）。
2. ✅ 改說 `config.example.yaml` 的檔（`3.2`）。
3. ✅ 改 clone-gestalt 與 pull-gestalt（`3.3`）。
4. 下次在 `countdell` 做 pull-gestalt 時，寫那台的 `config.local.yaml`，`gen_config.py --check` 要 PASS。

## 5. 驗證

- `gen_config.py --check`、`check_tasks.py` 與 `check_chores.py` 都是 PASS。
- `git grep config.example` 在 `tasks/` 與 `dashboard/` 以外沒有結果；task 檔裡沒有連到 `config.example.yaml` 的連結。
- `git status` 不列出 `config.yaml` 與 `config.local.yaml`。

## 6. 與其他 task 的關係

- [[Task 108]]：做了 `gen_config.py`；本 task 讓 SkillsGestalt 自己也用它，改掉 108 的 `3.5`。
- [[Task 105]]：clone-gestalt 的上一次改動。

## 7. 知識

### 適合寫成新 topic

—

### 適合併進現有 topic

—

### 不算知識

- YAML 裡以 `{` 開頭的值要加引號，不然讀成 mapping。

## 8. 日誌

### 2026-11-13

- 建立並做完：`config.example.yaml` 改名為 `config-tmp.yaml`（`3.1`），改了說它的檔（`3.2`）與 clone-gestalt、pull-gestalt（`3.3`）。Status 是完成；`4.` 第 4 項等 `countdell` 下次 pull。
