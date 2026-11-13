# Task 111 - work branch 寫在 config.shared.yaml 與 config.local.yaml

**Status**：完成——`config.shared.yaml` 列出 `workBranches`，`config.local.yaml` 寫這台的 `workBranch`；`AGENTS.shared.md` 不再寫死 `m1`，`publish_snapshot.py` 檢查這個值。
**Raised**：2026-11-13，`AGENTS.shared.md` 寫著 `Do your work on m1.`，但這台的 work branch 是 `devbox`；使用者要分支清單放在 `config.shared.yaml`，各台的分支放在 `config.local.yaml`。
**Depends on**：[[Task 110]]

## 1. 背景

- SkillsGestalt 有三個 clone，各有自己的 work branch：`m1`、`countdell`、`devbox`。
- `AGENTS.shared.md` 的 Branches 一節寫 `Do your work on m1.`；照 [[Task 110]] 的命名規則，「這台用哪個分支」是 `.local.` 的資訊，不該寫在 `.shared.` 的檔裡。
- `AGENTS.md` 留在 git（使用者決定），所以每台產生的 `AGENTS.md` 必須一樣：分支名稱不能代換進 `AGENTS.md`。

## 2. 結論

- [config.shared.yaml](../config.shared.yaml) 加 `workBranches`（`m1`、`countdell`、`devbox`）與 `workBranch: "{workBranch}"`；這台的 `config.local.yaml` 加 `workBranch: devbox`（`3.1`）。
- [AGENTS.shared.md](../AGENTS.shared.md) 說 work branch 是 `config.yaml` 的 `workBranch`，清單在 `config.shared.yaml`；`AGENTS.md` 每台都一樣（`3.1`）。
- [publish_snapshot.py](../skill-groups/common/scripts/publish_snapshot.py) 沒有 `--work` 時用 `workBranch`，並檢查它和 `--work`、`workBranches`、`pushRemote no_push` 一致（`3.2`）。
- [[clone-gestalt]]、[[publish-gestalt]]、[[pull-gestalt]] 改用 `workBranch`；`CHANGES.md` 記一筆，Forge 不必做（`3.3`）。

**表 1：改的檔**

| 檔 | 改了什麼 |
| --- | --- |
| `config.shared.yaml` | `workBranches` 與 `workBranch` |
| `config.local.yaml`（不在 git） | `workBranch: devbox`；註解改成 `config.shared.yaml` |
| `AGENTS.shared.md`、`AGENTS.md` | Branches 一節的前兩行 |
| `skill-groups/common/scripts/publish_snapshot.py` | `top_level()`；`work_branch()` 的預設值與三個檢查；docstring |
| `chores/clone-gestalt.md` | `<work>` 的名稱不能和清單重複；第 5 步寫 `workBranch`、加進清單 |
| `chores/publish-gestalt.md`、`chores/pull-gestalt.md` | work branch 的說明 |
| `skill-groups/common/CHANGES.md` | 2026-11-13 一筆 |

## 3. 過程

### 3.1 兩個設定與 AGENTS.shared.md（2026-11-13）

- 清單只寫分支名稱，不寫電腦名稱：主機名稱含有帳號的一部分，不能發佈；所以用 list，不用電腦對分支的 mapping。
- `AGENTS.shared.md` 叫 agent 讀 `config.yaml` 的 `workBranch`，不用 `{workBranch}` 代換，所以 `AGENTS.md` 每台都一樣。
- `check_ste.py` 對 `AGENTS.md` 是 PASS；它對 Commits 一節既有的 true 有一個 WARN，不是本 task 改的。

### 3.2 publish_snapshot.py（2026-11-13）

- 這支 script 不用 YAML 套件，自己讀 `config.yaml`；新的 `top_level()` 讀頂層的 key：scalar、`[a, b]`，或下面每行一個 `- item`。
- `work_branch()`：沒有 `--work` 時用 `workBranch`，沒有 `workBranch` 時照舊用目前 checkout 的分支；不切換分支。

**表 2：在 scratchpad 的 git repo 試跑 `check`**

| 情形 | 結果 |
| --- | --- |
| `workBranch: devbox`，沒有 `pushRemote no_push` | `devbox can be pushed`，`2` |
| 設了 `no_push`，沒有 `--work` | `work: devbox` |
| `--work other` | `the work branch of this clone is devbox`，`2` |
| `workBranches` 沒有 `devbox` | `devbox is not in workBranches`，`2` |
| `workBranches: [m1, devbox]`，`workBranch` 有引號與註解 | `work: devbox` |
| `workBranch: [a, b]` | `workBranch must be one branch name`，`2` |
| 沒有 `workBranch`，checkout `other` | `work: other`，和以前一樣 |

- 這台的 `check`：`work: devbox`，掃描是 `nothing found`。

### 3.3 chore 與 CHANGES.md（2026-11-13）

- clone-gestalt：新的 `<work>` 不能是清單裡已有的名稱；第 5 步的 `config.local.yaml` 寫 `wikiDir` 與 `workBranch`，並把 `<work>` 加進 `workBranches`，和第 11 步的紀錄一起 commit。
- publish-gestalt：說明 `workBranch`、`workBranches` 與三個檢查。pull-gestalt：`<work>` 就是 `workBranch`。
- `CHANGES.md`：沒有 `workBranch` 的 Forge 照舊，所以只說可以用。

## 4. 要做的

1. ✅ 兩個設定與 `AGENTS.shared.md`（`3.1`）。
2. ✅ `publish_snapshot.py` 的檢查（`3.2`）。
3. ✅ chore 與 `CHANGES.md`（`3.3`）。
4. 下次在 `countdell` 做 [[pull-gestalt]] 時，那台的 `config.local.yaml` 要寫 `wikiDir` 與 `workBranch: countdell`；`m1` 那台也一樣。
5. 使用者同意之後，和 [[Task 110]] 一起照 [[publish-gestalt]] 發佈。

## 5. 驗證

- 表 2 的每一種情形都和預期一樣。
- `gen_config.py --check`、`check_tasks.py` 與 `check_chores.py` 都是 PASS。
- `publish_snapshot.py check` 的 `work` 是 `devbox`，掃描是 `nothing found`。

## 6. 與其他 task 的關係

- [[Task 110]]：命名規則；本 task 把 `.local.` 的分支名稱移出 `AGENTS.shared.md`。
- [[Task 109]]：`config.shared.yaml` 與 `config.local.yaml` 的做法。

## 7. 知識

—

## 8. 日誌

### 2026-11-13

- 建立並做完：`workBranches` 與 `workBranch`（`3.1`），`publish_snapshot.py` 的檢查（`3.2`），chore 與 `CHANGES.md`（`3.3`）。Status 是完成；`4.` 第 4、5 項等別台 pull 與使用者同意發佈。
