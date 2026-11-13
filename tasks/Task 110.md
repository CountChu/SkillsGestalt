# Task 110 - config-tmp.yaml 與 AGENTS-local.md 改成 .shared. 的名稱

**Status**：完成——`config-tmp.yaml` 改名為 `config.shared.yaml`，`AGENTS-local.md` 改名為 `AGENTS.shared.md`；`AGENTS-tmp.md` 加一節 File Names，寫下 `-tmp`、`.shared.`、`.local.` 的規則。
**Raised**：2026-11-13，使用者要 `gen_config.py` 讀的共用設定檔改名為 `config.shared.yaml`，和 `config.local.yaml` 成對；接著決定 `AGENTS-local.md` 也改名，並把命名規則寫下來。
**Depends on**：[[Task 108]]、[[Task 109]]

## 1. 背景

- [[Task 108]] 的 `gen_config.py` 用 `config-tmp.yaml` 與 `config.local.yaml` 產生 `config.yaml`；[[Task 109]] 把 SkillsGestalt 的 `config.example.yaml` 改名為 `config-tmp.yaml`。兩個 task 已經在快照 `8e9e9d1` 發佈。
- `AGENTS-local.md` 是每個 agency 自己的規則，進 git；但 `config.local.yaml`、`publish-keywords.local.txt` 的 `.local.` 是只屬於這台電腦、不進 git。兩種 local 意思衝突。

**表 1：使用者定的命名規則**

| 名稱 | 意思 | 進 git | 例子 |
| --- | --- | --- | --- |
| `-tmp` | `common/templates/` 裡給許多 agency 用的模板 | 是 | `AGENTS-tmp.md`、`config-forge-tmp.yaml` |
| `.shared.` | 只屬於這個 agency，各台電腦共用 | 是 | `AGENTS.shared.md`、`config.shared.yaml` |
| `.local.` | 只屬於這台電腦 | 否 | `config.local.yaml`、`publish-keywords.local.txt` |

## 2. 結論

- `config-tmp.yaml` 以 `git mv` 改名為 [config.shared.yaml](../config.shared.yaml)；[gen_config.py](../skill-groups/common/scripts/gen_config.py) 讀新名稱（`3.1`）。
- `AGENTS-local.md` 以 `git mv` 改名為 [AGENTS.shared.md](../AGENTS.shared.md)；[gen_agents_md.py](../skill-groups/common/scripts/gen_agents_md.py) 讀新名稱，slot 改成 `{AGENTS-shared}` 與 `{AGENTS-shared-top}`；遇到舊名稱以 `2` 結束，印出改法（`3.3`）。
- [AGENTS-tmp.md](../skill-groups/common/templates/AGENTS-tmp.md) 加一節 File Names，寫表 1 的規則（`3.4`）。
- [CHANGES.md](../skill-groups/common/CHANGES.md) 2026-11-13 加兩筆，Forge 要 `git mv` 兩個檔。
- 電腦自己的 `AGENTS.local.md` 現在不需要，沒有做。

**表 2：改的檔**

| 檔 | 改了什麼 |
| --- | --- |
| `config-tmp.yaml` → `config.shared.yaml` | 改名 |
| `AGENTS-local.md` → `AGENTS.shared.md` | 改名 |
| `skill-groups/common/scripts/gen_config.py` | `TEMPLATE`、docstring |
| `skill-groups/common/scripts/gen_agents_md.py` | `LOCAL`、slot、舊名稱的檢查、docstring |
| `skill-groups/common/templates/AGENTS-tmp.md`、`AGENTS.md` | 檔名、slot、File Names 一節、Technical words 加 git；`AGENTS.md` 重新產生 |
| `skill-groups/common/references/forge-setup.md`、`forge-setup-tw.md` | 第 4、5 步的檔名與 slot |
| `.gitignore`、`README.md`、`README-tw.md` | `config.shared.yaml` |
| `chores/clone-gestalt.md`、`pull-gestalt.md`、`publish-gestalt.md`、`clean-checkpoints.md` | `config.shared.yaml` |
| `skill-groups/common/skills/clean-checkpoints/README.md` | When the Skill Is Changed 的檔名 |
| `skill-groups/common/CHANGES.md` | 兩筆新的；Task 108 那一筆與兩筆舊條目的連結 |
| 17 個舊 task 檔 | 連結的目標改成新名稱，文字不改（`3.2`） |

## 3. 過程

### 3.1 config-tmp.yaml 改名（2026-11-13）

- 開始做的時候，工作目錄已經有一半的改動：`git mv` 已經 staged，`.gitignore`、兩個 README、`clean-checkpoints`、`pull-gestalt`、clean-checkpoints 的 README 與 10 個舊 task 的連結已改；這些照原樣留下。
- 接著改其餘的檔：`gen_config.py`、`gen_agents_md.py`、`AGENTS-tmp.md`、`AGENTS-local.md`、`clone-gestalt`、`publish-gestalt`、`CHANGES.md`，以及 [[Task 108]]、[[Task 109]] 的連結。
- 產生的 `config.yaml` 只有第一行的註解改成新名稱。commit `46e1952`。

### 3.2 歷史紀錄（2026-11-13）

- `tasks/` 的文字、`dashboard/` 的紀錄與 `CHANGES.md` 的舊條目是過去的事，照舊寫舊名稱；只有連結的目標改成新名稱，讓 `check_tasks.py` 的連結檢查通過。
- 連到 `config-tmp.yaml` 的：Task 78、84、88.1、90、91、97.7、100.1、102、104、108、109。連到 `AGENTS-local.md` 的：Task 84、88.3、91、92、97.2、99。
- [[Task 108]]、[[Task 109]] 的標題照舊，摘要表也照舊。

### 3.3 AGENTS-local.md 改名（2026-11-13）

- slot 也改名，`{AGENTS-local}` 改成 `{AGENTS-shared}`、`{AGENTS-local-top}` 改成 `{AGENTS-shared-top}`，名稱才和檔名一致；SkillsGestalt 的 `AGENTS.shared.md` 沒有分隔行，不用改內容。
- 照以前 `CLAUDE-local.md` 的做法：沒有 `AGENTS.shared.md`、有 `AGENTS-local.md` 或 `CLAUDE-local.md` 時，以 `2` 結束，印出 `git mv` 的指令；`AGENTS.shared.md` 裡還有舊的分隔行，也以 `2` 結束。

**表 3：在 scratchpad 的 workspace 試跑**

| 情形 | 結果 |
| --- | --- |
| 只有 `AGENTS-local.md`，裡面有 `{AGENTS-local}` | 印出 `git mv AGENTS-local.md AGENTS.shared.md` 與改分隔行，`2` |
| 改名了，分隔行還是 `{AGENTS-local}` | 印出改分隔行，`2` |
| 分隔行改成 `{AGENTS-shared}` | 寫出 `AGENTS.md`，上段在引言之後、下段在最後，`0` |

- `clone-gestalt` 第 3 步與 `CHANGES.md` 2026-11-13 Task 108 那一筆引用的舊錯誤訊息 `{AGENTS-local}` 是過去的輸出，照舊。

### 3.4 File Names 一節（2026-11-13）

- 放在 `AGENTS-tmp.md` 的 Markdown 一節之後，用 STE 寫表 1 的三種名稱，最後一句說新的檔要照這個規則取名。
- `check_ste.py` 對模板、`AGENTS.md` 與 `forge-setup.md` 都是 PASS；git 加進模板的 Technical words。

## 4. 要做的

1. ✅ `config-tmp.yaml` 改名（`3.1`）。
2. ✅ `AGENTS-local.md` 改名，改 `gen_agents_md.py`（`3.3`）。
3. ✅ File Names 一節（`3.4`）。
4. ✅ `CHANGES.md` 記兩筆（`2.`）。
5. 使用者同意之後，照 [[publish-gestalt]] 發佈。

## 5. 驗證

- `gen_config.py --check`、`check_tasks.py` 與 `check_chores.py` 都是 PASS。
- 表 3 的每一種情形都和預期一樣。
- `git grep` 在 `tasks/` 與 `dashboard/` 以外，舊名稱只剩 `CHANGES.md` 說改名的條目、舊條目、舊的錯誤訊息，以及 `gen_agents_md.py` 檢查舊名稱的地方。

## 6. 與其他 task 的關係

- [[Task 108]]：做了 `gen_config.py`。
- [[Task 109]]：SkillsGestalt 自己改用 `config-tmp.yaml`；本 task 再改名。
- [[Task 97.2]]：把 `CLAUDE-local.md` 改名為 `AGENTS-local.md`；本 task 照它檢查舊名稱的做法。

## 7. 知識

—

## 8. 日誌

### 2026-11-13

- 建立並做完 `config-tmp.yaml` 的改名：接著工作目錄裡已有的一半改動（`3.1`），歷史紀錄只改連結（`3.2`）。
- 使用者決定 `AGENTS-local.md` 也改名，並寫下命名規則：改了 `AGENTS-local.md` 與 slot（`3.3`），`AGENTS-tmp.md` 加 File Names（`3.4`）；標題改成兩個改名。Status 是完成；`4.` 第 5 項等使用者同意發佈。
