# Task 113 - AGENTS-tmp.md 的指令能直接跑，找 skill 與載入的 token 變少

**Status**：完成——沒有 PyYAML 的 python 會改用 `.venv` 重跑，script 以 UTF-8 輸出，`AGENTS.md` 用一張表列出 skill、不寫 STE 標頭；每個 agency 都要有 `config.shared.yaml` 與 `workBranches`。
**Raised**：2026-11-13，一個 Forge 檢查它產生的 `AGENTS.md`：內容有沒有錯、指令夠不夠直接、會不會花太多 token；它只屬於自己的錯在它的 `AGENTS.shared.md` 改好了，下面這些在模板與 script，要在 SkillsGestalt 改。
**Depends on**：—

## 1. 背景

- 每個 session 都載入 `AGENTS.md`；那個 Forge 的約 1,600 字，約 3–3.5k token，其中約 740 字來自它的 `AGENTS.shared.md`。
- [AGENTS-tmp.md](../skill-groups/common/templates/AGENTS-tmp.md) 是所有 agency 共用的模板，它的問題每個 agency 都有。

**表 1：檢查找到、要在 SkillsGestalt 改的問題**

| # | 問題 | 在哪裡 | 種類 |
| --- | --- | --- | --- |
| 1 | `python {skillGroups.common}/scripts/gen_config.py` 用系統 python 跑，那台電腦的系統 python 沒有 PyYAML，以 `ModuleNotFoundError: No module named 'yaml'` 結束；用 agency 的 `.venv/Scripts/python` 跑才過 | `AGENTS-tmp.md` 第 19 行 | 錯誤 |
| 2 | `check_chores.py` 印中文與圖示時，Windows 主控台的 cp1252 讓它以 `UnicodeEncodeError` 結束；要先設 `PYTHONIOENCODING=utf-8`。task-rules 有寫這個做法，但 `AGENTS.md` 的指令沒有 | `check_chores.py`，可能還有 `check_tasks.py` 與其他印中文的 script | 錯誤 |
| 3 | 找 skill 的規則要依序讀每個 skill group 的 `<root>/skills/<name>/SKILL.md`，不能搜尋；那個 Forge 有 7 個 group，名稱其實是 chore 時，要讀 7 次都失敗才知道 | `AGENTS-tmp.md` 的 Skills 一節 | token |
| 4 | 開頭的 STE 紀錄與 Technical words 約 80 字，是給 STE 的檢查用，agent 用不到 | `AGENTS-tmp.md` 第 3–7 行 | token |
| 5 | 「沒有 `config.shared.yaml` 時……」與「有 `workBranches` 時……」兩段，對某個 agency 不是一定成立就是一定不成立 | `AGENTS-tmp.md` 的開頭與 Work Branch 一節 | token |

## 2. 結論

- #1：選第一個做法，指令不變。[gen_config.py](../skill-groups/common/scripts/gen_config.py)、[gen_agents_md.py](../skill-groups/common/scripts/gen_agents_md.py) 與 [depends_on.py](../skill-groups/common/scripts/depends_on.py) 在 `import yaml` 失敗時，用根目錄的 `.venv/Scripts/python.exe` 或 `.venv/bin/python` 重跑自己；環境變數 `GESTALT_VENV_RERUN` 防止重跑第二次；沒有 `.venv` 就以 `2` 結束（`3.1`）。
- #2：`skill-groups/common/scripts/` 的 8 個 script 都在 import 之後把 stdout 與 stderr 設成 UTF-8；task-rules 與 chore-rules（含中文版）不再要求設 `PYTHONIOENCODING`（`3.1`）。
- #3：`{skillGroupRoots}` 換成一張「skill group、根目錄、skill 名稱」的表；Skills 一節改成查表，表裡沒有就看 `chores/<name>.md`；開頭說新增或刪除 skill 後要跑 `gen_config.py`（`3.2`）。
- #4：`AGENTS.md` 不寫標題下面的引言；`--ste FILE` 寫出含引言的全文給 `check_ste.py`（`3.2`）。
- #5：使用者決定每個 agency 都要有 `config.shared.yaml` 與 `workBranches`，所以這兩個條件一定成立；模板直接寫成立的句子，script 在缺少時以 `2` 結束。先做的條件行 `{?…}` 拿掉（`3.3`）。
- [config-forge-tmp.yaml](../skill-groups/common/templates/config-forge-tmp.yaml) 改成 `config.shared.yaml` 的範本，[forge-setup.md](../skill-groups/common/references/forge-setup.md) 與中文版、[follow-gestalt](../chores/follow-gestalt.md) 跟著改（`3.3`）。
- [CHANGES.md](../skill-groups/common/CHANGES.md) 記一筆。

## 3. 過程

### 3.1 python 與編碼（2026-11-13）

- 這台的系統 python 3.12 也沒有 PyYAML；`python skill-groups/common/scripts/gen_config.py` 原樣跑，經 `.venv` 重跑後是 `0`。
- 在沒有 `.venv` 的目錄跑，印出 `... has no PyYAML, and the root has no .venv with it: pip install pyyaml`，以 `2` 結束。
- 設 `PYTHONIOENCODING=cp1252` 再跑 `check_tasks.py` 與 `check_chores.py`，中文與圖示照常印出，都是 PASS。

### 3.2 gen_agents_md.py 與模板（2026-11-13）

- skill 名稱先寫成清單的一行，STE 檢查說那一行 26 字太長；改成表格，表格不在 STE 檢查的範圍。
- Skills 一節一段 8 句，超過 6 句，分成兩段；`exists` 不在字典，改成「If the root has `chores/<name>.md`」。
- `--ste` 寫出的全文與模板，`check_ste.py` 都是 PASS。
- 在 scratchpad 用沒有 `config.shared.yaml`、沒有 `workBranches` 的 `config.yaml` 試跑：開頭只剩「after each change to the `config.yaml`」，Work Branch 一節只剩兩句。

**表 2：SkillsGestalt 的 AGENTS.md 前後**

| | 行 | 字 |
| --- | --- | --- |
| 之前 | 130 | 976 |
| 之後 | 128 | 971 |

- 少的字不多，因為多了 23 個 skill 名稱的表；但找 skill 不必再讀檔，名稱是 chore 時也只讀一次。

### 3.3 config.shared.yaml 與 workBranches 一定要有（2026-11-13）

- `3.2` 先做了條件行：一行開頭寫 `{?configShared}`、`{?!configShared}` 或 `{?workBranches}`，條件成立才留下。
- 使用者看了之後決定兩個都一定要有，條件行就沒有用了：`gen_agents_md.py` 拿掉這個機制，模板直接寫成立的句子，SkillsGestalt 的 `AGENTS.md` 不變。
- `gen_config.py` 沒有 `config.shared.yaml` 時不再只跑 `gen_agents_md.py`，改成以 `2` 結束；`gen_agents_md.py` 也檢查 `config.shared.yaml`，並要求 `workBranches` 列出 `workBranch`。
- Forge 原本把 `config.yaml` 放進 git，現在照 forge-setup 第 2 步寫 `config.shared.yaml` 與 `config.local.yaml`。範本裡大寫的 `{WORK_BRANCH}` 手動換；camelCase 的 `{wikiDir}` 這類留著，由 `gen_config.py` 從 `config.local.yaml` 填。
- forge-setup 的 STE 檢查先報兩句太長、兩段 7 句；拆句、分段，Technical words 加 computer 與 path 之後是 PASS。

**表 3：在 scratchpad 試跑**

| 情形 | 結果 |
| --- | --- |
| 沒有 `config.shared.yaml`，跑 `gen_config.py` | `no such file`，`2` |
| 有 `config.shared.yaml`，沒有 `workBranches` | `workBranches does not list workBranch x`，`2` |
| 兩個都有 | `0` |
| 沒有 `config.shared.yaml`，直接跑 `gen_agents_md.py` | `no such file`，`2` |

## 4. 要做的

1. ✅ 表 1 的 #1：`gen_config.py` 等改用 `.venv` 重跑（`3.1`）。
2. ✅ 表 1 的 #2：script 以 UTF-8 輸出（`3.1`）。
3. ✅ 表 1 的 #3：skill 的表（`3.2`）。
4. ✅ 表 1 的 #4：`AGENTS.md` 不寫 STE 引言，`--ste` 給檢查用（`3.2`）。
5. ✅ 表 1 的 #5：`config.shared.yaml` 與 `workBranches` 一定要有（`3.3`）。
6. ✅ 重新產生 SkillsGestalt 的 `AGENTS.md`，在 `CHANGES.md` 記一筆。
7. ✅ Forge 的範本、forge-setup 與 follow-gestalt 改用 `config.shared.yaml` 與 `gen_config.py`（`3.3`）。

## 5. 驗證

- 系統 python 沒有 PyYAML，`AGENTS.md` 給的 `gen_config.py` 指令原樣跑是 `0`；`--check` 是 PASS。
- 設 `PYTHONIOENCODING=cp1252`，`check_tasks.py` 與 `check_chores.py` 都是 PASS，沒有 `UnicodeEncodeError`。
- 不存在的 skill 名稱：表裡沒有，agent 不必讀檔就知道。
- 產生的 `AGENTS.md` 比原本短（表 2）。

## 6. 與其他 task 的關係

- [[Task 108]]：建 `gen_config.py` 與目前的指令。
- [[Task 112]]：把通用的規則搬進 `AGENTS-tmp.md`，本 task 改的就是那些規則。

## 7. 知識

- STE 檢查不看表格與 inline code，一長串名稱放進表格就不會算成一個太長的句子。

## 8. 日誌

### 2026-11-13

- 建立本 task：一個 Forge 檢查 `AGENTS.md` 找到表 1 的問題。
- 做完 5 項（`3.1`、`3.2`），`CHANGES.md` 記一筆。Status 是完成。
- 使用者決定每個 agency 都要有 `config.shared.yaml` 與 `workBranches`：拿掉條件行，script 缺少時停下，Forge 的範本與 forge-setup 跟著改（`3.3`）。
