# Task 104 - 整理在新電腦上安裝 SkillsGestalt 的步驟

**Status**：完成——安裝步驟在新的 chore [[clone-gestalt]]，在 scratchpad 照著做過一次（`3.3`、`3.4`）；那個 Forge 也建了自己的 clone chore；這台的 `countdell` 補設了 `no_push`（`3.5`）。
**Raised**：2026-11-13，使用者要在一台 DevBox 上裝一個 Forge，問 SkillsGestalt 是不是要先裝、步驟寫在哪裡。
**Depends on**：—

## 1. 背景

- Forge 的 `config.yaml` 以 `skillGroups.common` 與 `agencies` 指到 SkillsGestalt，所以 common 的 skill 與 `check_tasks.py`、`check_chores.py`、`gen_agents_md.py`、`publish_snapshot.py` 都從那裡讀。在新電腦上裝 Forge 之前，要先裝 SkillsGestalt。
- 另一台電腦（CountDell，工作分支 `countdell`）已經有一份 clone，但它是怎麼 clone、怎麼設定的，沒有記下來。
- 這次的新電腦是一台 DevBox，要放一個 Forge，工作分支叫 `devbox`。

## 2. 結論

- 使用者決定：DevBox 上的 SkillsGestalt 也要在上面改、發佈。步驟先寫在 [[pull-gestalt]] 的「新的 clone」（`3.3`），之後搬到新的 chore [[clone-gestalt]]，共 11 步；pull-gestalt 只留一句「新電腦先做 clone-gestalt」（`3.4`）。
- 在 scratchpad 從 GitHub clone 一次，照步驟做完：檢查都是 PASS，`check` 與 `incoming` 沒有要做的，`git push` 失敗（`3.3`）。
- README 不改：只拿來用的情況，這次沒有要寫。
- 那個 Forge 也建了自己的 clone chore，第一步是先做 clone-gestalt（`3.4`）。
- 這台的 `countdell` 補設了 `branch.countdell.pushRemote no_push`，`git push` 以 128 失敗（`3.5`）。
- DevBox 上真的做一次 clone-gestalt，會記在它的執行紀錄。

## 3. 過程

### 3.1 安裝要做的事，現在寫在哪裡（2026-11-13）

**表 1：在新電腦上裝 SkillsGestalt 要做的事**

| 要做的事 | 寫在哪裡 |
| --- | --- |
| `git clone https://github.com/CountChu/SkillsGestalt` | 都沒寫 |
| 從 [config.example.yaml](../config.shared.yaml) 做出 `config.yaml`，設 `wikiDir` | [README.md](../README.md) 的 Getting Started（`README-tw.md` 也有） |
| 建 `.venv`，裝 `requirements.txt` | [[Task 95]]；Forge 的部分在 `forge-setup.md` 的 Make a Forge 第 3 步（[[Task 96]]） |
| 本機的 `main` 只放快照，追蹤 `origin/main` | [[publish-gestalt]] 的 `1. 目的` |
| 工作分支，設 `branch.<work>.pushRemote no_push` | [[publish-gestalt]] 的 `1. 目的` |
| `publish-keywords.local.txt`（不進 git，要從原本那台複製） | [[publish-gestalt]] 的「準備」 |
| `config.yaml` 的 `identity`，不用那台電腦的工作身分 | [[Task 90]]、[[publish-gestalt]] 第 4 步 |
| 之後怎麼跟上別台發佈的快照 | [[pull-gestalt]]（[[Task 89]]） |

- [[pull-gestalt]] 寫的是已經有 clone 的電腦怎麼跟上，沒有寫第一次 clone。
- `forge-setup.md` 寫的是怎麼把一個 workspace 做成 Forge，不是怎麼裝 SkillsGestalt 本身。
- 這台 clone 的 `countdell` 沒有設 `branch.countdell.pushRemote no_push`，和 publish-gestalt 寫的不同（2026-11-10 看到）。

### 3.2 要決定的事

新電腦上的 SkillsGestalt 有兩種用法，要寫的步驟不同：

**表 2：兩種用法**

| 用法 | 要裝的 | 寫在哪裡 |
| --- | --- | --- |
| 只拿來用：Forge 讀它，這台不改 | clone、`config.yaml`、`.venv`；之後在 `main` 上 `git pull` | README 的 Getting Started 補 clone 與 `.venv`（`README-tw.md` 一起改） |
| 也要在上面改、發佈 | 上面的，加上 `main` 追蹤 `origin/main`、工作分支與 `no_push`、`publish-keywords.local.txt`、`identity` | [[pull-gestalt]] 加一節「新的 clone」 |

- 第一種用法的 `main` 不只放快照時，`git pull` 就是跟上的方法，不需要 pull-gestalt；要改的時候再照第二種補設定。
- 兩種都寫的話，README 給一般的讀者，pull-gestalt 給自己的另一台電腦。

### 3.3 寫進 pull-gestalt，並試做一次（2026-11-13）

- 使用者決定 DevBox 也要在上面改、發佈。[[pull-gestalt]] 在 `3. 怎麼做` 的最後加 `### 新的 clone`，11 步：git 與帳號、目錄、clone、工作分支與 `no_push`、`config.yaml`、從原本那台複製不進 git 的檔、`.venv`、檢查、`check` 與 `incoming`、`git push` 要失敗、記執行紀錄。
- 在 scratchpad 照著做（工作分支 `devbox`）：
  - clone 出來的 `main` 已經追蹤 `origin/main`（`04a90cc`）；`git switch -c devbox main` 的 `devbox` 沒有 upstream。
  - `config.yaml` 只改 `wikiDir`；`publish-keywords.local.txt` 與 ASD-STE100 的 PDF 從這台複製。
  - `.venv` 用 Python 3.13 建，`pip install -r skill-groups/common/requirements.txt` 以 0 結束。
  - `gen_agents_md.py`：`AGENTS.md`、`CLAUDE.md` 不變；`check_tasks.py` 與 `check_chores.py` 都是 PASS。
  - `check`：`scan: nothing found`、`no change since the last release 04a90cc`；`incoming`：`nothing to pull`。
  - `git push` 以 128 失敗。`git status` 只有 `external/`，和這台一樣；`.venv/` 與 `config.yaml` 不出現。
- `identity` 不必寫：快照的作者沒寫時是 `IDENTITY`，不看這台的 git 設定。

### 3.4 搬到新的 chore clone-gestalt（2026-11-13）

- 使用者提議把「新的 clone」搬到一個新的 chore：何時要做和 pull-gestalt 不同（新電腦，不是新快照），在 chore 摘要表上找得到，每裝一台記一筆。
- 新的 chore [[clone-gestalt]]，Private，When 是「要在一台新電腦上裝 SkillsGestalt，也要在上面改、發佈時」；`3. 怎麼做` 是原本的 11 步，第 11 步改成記在 `### clone-gestalt`，在新電腦的工作分支上以 `chore clone-gestalt: ` commit。
- [[pull-gestalt]] 的 `### 新的 clone` 換成一句「先做 clone-gestalt」，第 5 章加 clone-gestalt。摘要表加一列，上次執行是 —。
- 那個 Forge 也照這個做法，把它 pull chore 的「新的 clone」搬到自己的 clone chore；第一步是先做 clone-gestalt，clone 改成只抓它的快照分支。

### 3.5 這台的 countdell 補設 no_push（2026-11-13）

- 使用者同意：`git config branch.countdell.pushRemote no_push`。
- `countdell` 本來就沒有 upstream；設了之後 `git push` 以 128 失敗。`pushRemote` 只管沒寫 remote 的 `git push`：明寫 remote 的 `git push origin countdell` 仍會推上去，所以不要這樣打。

## 4. 要做的

1. ✅ 問使用者：DevBox 上的 SkillsGestalt 是只拿來用，還是也要在上面改、發佈（`3.2`）：也要改、發佈。
2. ✅ 照決定寫步驟：先寫在 [[pull-gestalt]] 的「新的 clone」（`3.3`），再搬到 [[clone-gestalt]]（`3.4`）。
3. ✅ 要不要替這台的 `countdell` 補設 `pushRemote no_push`，問使用者：要（`3.5`）。
4. ✅ 寫完後告訴那個 Forge：它建了自己的 clone chore，第一步是先做 [[clone-gestalt]]（`3.4`）。
5. ✅ 改了 README 或 chore 而 Forge 要跟著做的話，在 `CHANGES.md` 記一筆：pull-gestalt 是 Private，Forge 不必做，不記。

## 5. 驗證

- 照寫好的步驟，在 scratchpad 的一個新目錄 clone 一次，做完每一步：`check_tasks.py` 與 `check_chores.py` 是 PASS；第二種用法另外確認在工作分支上 `git push` 會失敗，`publish_snapshot.py check` 能跑。
- README 與 `README-tw.md` 有改的話，兩份對得上。

## 6. 與其他 task 的關係

- [[Task 89]]、[[Task 90]]：另一台電腦的 pull 與快照的身分，本 task 要用到它們的結論。
- [[Task 95]]、[[Task 96]]：`.venv` 的建法。
- [[Task 102]]：讓 Forge 也能照 publish-gestalt、pull-gestalt 發佈；那個 Forge 在 DevBox 上要先裝好 SkillsGestalt，才能用它。
- [[clone-gestalt]]：本 task 建立的 chore。

## 7. 知識

—

## 8. 日誌

### 2026-11-13

- 建立 task：在 tasks、README、publish-gestalt、pull-gestalt 與 `forge-setup.md` 找安裝要做的事，寫成表 1；兩種用法寫成表 2。
- 使用者決定 DevBox 也要在上面改、發佈：[[pull-gestalt]] 加「新的 clone」，在 scratchpad 照著做一次，寫成 `3.3` 與 `2. 結論`；`4. 要做的` 第 1、2、5 項完成。
- 使用者同意把「新的 clone」搬到新的 chore：建 [[clone-gestalt]]，pull-gestalt 只留一句，摘要表加一列；那個 Forge 也建了自己的 clone chore。寫成 `3.4`，第 4 項完成，`2. 結論` 與 Status 跟著改。
- 使用者同意補設 `countdell` 的 `no_push`，寫成 `3.5`；第 3 項完成，Status 改成完成。
