# Task 108 - 用 config-tmp.yaml 與 config.local.yaml 產生 config.yaml

**Status**：完成——新的 `gen_config.py` 用 `config-tmp.yaml` 與 `config.local.yaml` 產生 `config.yaml`，再跑 `gen_agents_md.py`；`gen_agents_md.py` 不再受 CRLF 影響。
**Raised**：2026-11-13，一個 Forge 在兩台電腦上同步時，`config.yaml` 與 `AGENTS.md` 都在 git，各台的路徑不同就會互相蓋掉；那個 Forge 決定這兩個檔都由 script 產生、不進 git，產生的 script 由 SkillsGestalt 提供。
**Depends on**：—

## 1. 背景

- 一個 Forge 根目錄的 `config.yaml` 進 git，裡面的路徑都寫死這台的 home 目錄：`wikiDir`、`skillGroups`、`wikiRootDir`、`agencies`、`tasksDir`、`taskSummary`、`choreSummary`。
- [gen_agents_md.py](../skill-groups/common/scripts/gen_agents_md.py) 用模板 `AGENTS-tmp.md`、`AGENTS-local.md` 與 `config.yaml` 產生 `AGENTS.md`，路徑原樣寫進去；那個 Forge 的 `AGENTS.md` 也進 git。
- 帳號或目錄不同的兩台電腦，`config.yaml` 與 `AGENTS.md` 本來就該不同；但兩個檔都在 git，一台發佈之後，另一台 pull 就被蓋掉。
- 起因：在 Windows 上 clone 那個 Forge 時，`gen_agents_md.py` 產生的 `AGENTS.md` 和 commit 裡的不同。Git for Windows 預設 `core.autocrlf=true`，`AGENTS-local.md` checkout 成 CRLF；`gen_agents_md.py` 用 `read_bytes().decode()` 讀、用 `'\n'` 切行，分隔行讀成 `{AGENTS-local}\r`，找不到。[[Task 105]] 讓 SkillsGestalt 的 clone 設 `core.autocrlf=false` 繞過，script 本身還沒改。
- 那個 Forge 查過：沒有 script 或 skill 步驟寫入根目錄的 `config.yaml`，只有讀；所以改成產生出來的檔，不會掉資料。

**表 1：那個 Forge 決定的檔案分工**

| 檔案 | 內容 | 進 git |
| --- | --- | --- |
| `config-tmp.yaml` | 共用的設定，例如 `publish:`、`identity:`、`cleanCheckpoints:`、`keepEnglishChore`；路徑寫成佔位符，例如 `{home}/Obsidian/MyVault` | 是 |
| `config.local.yaml` | 這台的值，例如 `home`、`workArea` | 否 |
| `config.yaml` | 本 task 的 script 用前兩個檔產生，內容和現在一樣 | 否 |
| `AGENTS.md` | `gen_agents_md.py` 用 `config.yaml` 產生，因機器而不同 | 否 |
| `CLAUDE.md` | 只有 `@AGENTS.md`，各台一樣 | 是 |

- 選這個做法，是因為每個讀 `config.yaml` 的 script 都不用改。

## 2. 結論

- 新的 [gen_config.py](../skill-groups/common/scripts/gen_config.py) 產生 `config.yaml`，再跑 `gen_agents_md.py`；`--check` 三個檔都比對（`3.2`）。
- `config.local.yaml` 只放 `name: value`，`config-tmp.yaml` 當文字代換 `{name}`，註解與順序原樣留下（`3.1`）。
- `gen_agents_md.py` 讀檔時把 CRLF 換成 LF（`3.3`）。
- [AGENTS-tmp.md](../skill-groups/common/templates/AGENTS-tmp.md) 的指令改成 `gen_config.py`；[CHANGES.md](../skill-groups/common/CHANGES.md) 記了 2026-11-13 一筆（`3.4`）。
- SkillsGestalt 自己原本不改成 `config-tmp.yaml`（`3.5`）；之後 [[Task 109]] 改了。

**表 2：改的檔**

| 檔 | 改了什麼 |
| --- | --- |
| `skill-groups/common/scripts/gen_config.py` | 新的 script |
| `skill-groups/common/scripts/gen_agents_md.py` | 讀檔時 CRLF 換成 LF；docstring 提到 `gen_config.py` |
| `skill-groups/common/templates/AGENTS-tmp.md` | 指令改成 `gen_config.py`，加兩行說明；Technical words 加 computer |
| `AGENTS.md` | 重新產生 |
| `skill-groups/common/CHANGES.md` | 2026-11-13 一筆 |

- 還留下的：那個 Forge 自己的 `config-tmp.yaml`、移出 git 與 chore 的改動，由它自己的 task 做。

## 3. 過程

### 3.1 config.local.yaml 的格式（2026-11-13）

**表 3：比較過的格式**

| 格式 | 結果 |
| --- | --- |
| 只放變數，`config-tmp.yaml` 當文字代換 `{name}` | 採用：註解與順序留在 `config.yaml`，產生的檔能和原本的一樣 |
| `config.local.yaml` 以 YAML 合併蓋過 `config-tmp.yaml` | 不用：寫回 YAML 會掉註解、改順序 |

- `{{name}}` 寫成 `{name}`，和 `gen_agents_md.py` 一樣。
- 名稱只能用字母、數字與 `_`；值是一個 scalar，不能是 mapping 或 list。
- [config-forge-tmp.yaml](../skill-groups/common/templates/config-forge-tmp.yaml) 的註解行有 `{PLACEHOLDER}`，所以 `#` 開頭的行不代換；行尾的註解照樣代換。

### 3.2 gen_config.py（2026-11-13）

- 沒有 `config-tmp.yaml` 時，`config.yaml` 不動，只跑 `gen_agents_md.py`；所以每個 workspace 都能跑同一個指令。
- `config.yaml` 第一行是一行註解，說它是產生的、要改哪兩個檔。
- `config.local.yaml` 沒有的名稱、結果不是正確的 YAML，都以 `2` 結束；沒用到的名稱只印出來。
- `--check` 什麼都不寫；`config.yaml` 不同時印出 diff，以 `1` 結束；接著用同一個 `--root` 跑 `gen_agents_md.py --check`。

**表 4：在 scratchpad 的 workspace 試跑**

| 情形 | 結果 |
| --- | --- |
| 第一次產生 | 三個檔 written，`{{this}}` 寫成 `{this}`，結束碼 `0` |
| 再跑 `--check` | 三個 PASS，`0` |
| 手改 `config.yaml` 後 `--check` | `config.yaml` FAIL，`1` |
| 五個檔都改成 CRLF 後 `--check` | 三個 PASS，`0` |
| `config-tmp.yaml` 用了沒有的名稱 | 印出名稱，`2` |
| 結果不是正確的 YAML | 印出 YAML 的錯，`2`；沒用到的名稱也印出 |
| 沒有 `config-tmp.yaml` | `config.yaml` kept，另兩個 PASS，`0` |
| `config-forge-tmp.yaml` 原樣當 `config-tmp.yaml` | 三個 written，`--check` 三個 PASS |

### 3.3 gen_agents_md.py 的 CRLF（2026-11-13）

- `read()` 與比對用的 `now` 都把 `\r\n` 換成 `\n`；寫出的檔照舊是 LF。
- 只有換行不同的 `AGENTS.md`、`CLAUDE.md` 算 unchanged，`--check` 是 PASS（表 4 的 CRLF 那一列）。

### 3.4 AGENTS-tmp.md 與 CHANGES.md（2026-11-13）

- 模板的指令改成 `gen_config.py`，觸發條件加上 `config-tmp.yaml` 與 `config.local.yaml`，並說有 `config-tmp.yaml` 時不改 `config.yaml`。
- `check_ste.py` 對模板是 PASS；computer 不在字典裡，加進 Technical words。
- `CHANGES.md` 的 Forge 要做：跑 `gen_config.py`、commit 改了的 `AGENTS.md`；多台電腦、路徑不同的 Forge 才改成 `config-tmp.yaml`。
- chore 與 [forge-setup.md](../skill-groups/common/references/forge-setup.md) 裡的 `gen_agents_md.py` 不改：沒有 `config-tmp.yaml` 時，它和 `gen_config.py` 做的一樣。

### 3.5 SkillsGestalt 自己（2026-11-13）

- SkillsGestalt 的 `config.yaml` 本來就不在 git，範本是 `config.example.yaml`，[[Task 109]] 改名為 [config-tmp.yaml](../config-tmp.yaml)。
- 它的 `AGENTS.md` 只有相對路徑，例如 `skill-groups/common`，每台都一樣，可以留在 git。所以不改。
- 之後使用者要它也用 `config-tmp.yaml`，好讓範本新的 key 跟到各台；由 [[Task 109]] 做。

## 4. 要做的

1. ✅ 決定 `config.local.yaml` 的格式（`3.1`）。
2. ✅ 加 `gen_config.py`，有 `--check`，接著跑 `gen_agents_md.py`（`3.2`）。
3. ✅ `gen_agents_md.py` 不受 CRLF 影響（`3.3`）。
4. ✅ 改 `AGENTS-tmp.md` 的指令（`3.4`）。
5. ✅ 在 `CHANGES.md` 記一筆（`3.4`）。
6. ✅ SkillsGestalt 自己不改成 `config-tmp.yaml`（`3.5`）。

## 5. 驗證

- 表 4 的每一種情形都和預期一樣。
- SkillsGestalt 的 `gen_config.py --check`、`check_tasks.py` 與 `check_chores.py` 都是 PASS。
- 模板的 `check_ste.py` 是 PASS。

## 6. 與其他 task 的關係

- [[Task 109]]：SkillsGestalt 自己的 `config.example.yaml` 改為 `config-tmp.yaml`。
- [[Task 105]]：clone-gestalt 設 `core.autocrlf=false`，繞過同一個 CRLF 問題；本 task 讓 `gen_agents_md.py` 本身不受影響。

## 7. 知識

### 適合寫成新 topic

—

### 適合併進現有 topic

—

### 不算知識

- Git for Windows 預設 `core.autocrlf=true`，會把 LF 的檔 checkout 成 CRLF；用 `'\n'` 切行、比對整行的 script 會出錯。
- 要讓產生的 YAML 留住註解，就把模板當文字代換；用 YAML 讀進來再寫出去會掉註解。

## 8. 日誌

### 2026-11-13

- 建立。一個 Forge 決定 `config.yaml` 與 `AGENTS.md` 由 script 產生、不進 git，需要 SkillsGestalt 提供產生 `config.yaml` 的 script 與 `gen_agents_md.py` 的 CRLF 修正。Status 是尚未開始。
- 開始做：定了 `config.local.yaml` 的格式（`3.1`），寫了 `gen_config.py` 並試跑（`3.2`），修了 `gen_agents_md.py` 的 CRLF（`3.3`），改了模板與 `CHANGES.md`（`3.4`）；SkillsGestalt 自己不改（`3.5`）。Status 改成完成。
- 使用者要 SkillsGestalt 自己也用 `config-tmp.yaml`，開 [[Task 109]]；`3.5` 加一行。
