# Task 112 - AGENTS.shared.md 裡通用的規則搬到 AGENTS-tmp.md

**Status**：完成——work branch 與不加 `Co-Authored-By` 的規則搬進 `AGENTS-tmp.md` 的 Work Branch and Commits 一節，每個 agency 都要有 `workBranch`；`AGENTS.shared.md` 只留 SkillsGestalt 自己的部分；forge-setup 多寫 `.claude/settings.json` 與 `{WORK_BRANCH}`。
**Raised**：2026-11-13，[[Task 111]] 之後，使用者問 `AGENTS.shared.md` 的內容能不能都搬到 `AGENTS-tmp.md`；使用者決定不加 `Co-Authored-By` 是每個 agency 的規則。
**Depends on**：[[Task 111]]

## 1. 背景

- `AGENTS-tmp.md` 是每個 agency 的 `AGENTS.md` 的模板；`AGENTS.shared.md` 是只屬於這個 agency 的規則。
- 模板不能只對某些 agency 出現一段文字（只有 `{keepEnglishChore}` 那一行可以拿掉），所以搬過去的規則要對每個 agency 都對，或寫成「If …」。

**表 1：AGENTS.shared.md 每一段能不能搬**

| 內容 | 結果 | 原因 |
| --- | --- | --- |
| `config.yaml` 由 `config.shared.yaml` 與 `config.local.yaml` 產生 | 拿掉 | 模板的引言已經寫了 |
| `common` 的改動寫 `CHANGES.md` | 留下 | 只有擁有 `common` 的 SkillsGestalt 寫 |
| work branch 是 `workBranch` | 搬；先寫成「If `config.yaml` has `workBranch`」，`3.3` 改成一定要有 | 使用者決定每個 Forge 都要有 `workBranch` |
| `workBranches` 的清單 | 搬（`3.3`） | 使用者決定每個 Forge 在每台電腦都要定義 work branch |
| 本機 `main` 只放快照 | 留下 | 只有用 `publish_snapshot.py` 發佈的 agency 才有，Forge 的快照分支名稱也可能不同；模板沒辦法判斷 |
| `archive/*` tag | 留下 | `archive/master` 是 SkillsGestalt 自己的歷史；`archive/<branch>-<yymmdd>` 和上一列一樣，只有發佈的 agency 才有 |
| 照 publish-gestalt 發佈 | 留下 | Private 的 chore |
| commit 訊息不加 `Co-Authored-By`，`.claude/settings.json` | 搬 | 使用者決定每個 agency 都一樣 |
| 快照也不加 `Co-Authored-By` | 留下 | 講的是 publish-gestalt |

## 2. 結論

- [AGENTS-tmp.md](../skill-groups/common/templates/AGENTS-tmp.md) 在 File Names 之後加 `## Work Branch and Commits`，Technical words 加 branch 與 message（`3.1`）。
- [AGENTS.shared.md](../AGENTS.shared.md) 拿掉重複的兩行與搬走的規則；`## Commits` 一節併進 `## Branches` 的最後一行（`3.1`）。
- [forge-setup.md](../skill-groups/common/references/forge-setup.md) 與中文版第 4 步寫 `.claude/settings.json`，第 8 步一起 commit（`3.2`）。
- 每個 agency 都要有 `workBranch`：[gen_agents_md.py](../skill-groups/common/scripts/gen_agents_md.py) 沒有它就以 `2` 結束；[config-forge-tmp.yaml](../skill-groups/common/templates/config-forge-tmp.yaml) 多了 `workBranches` 與 `{WORK_BRANCH}`（`3.3`）。
- [CHANGES.md](../skill-groups/common/CHANGES.md) 記一筆：每個 Forge 要定義 `workBranch`，並寫 `.claude/settings.json`。

## 3. 過程

### 3.1 模板與 AGENTS.shared.md（2026-11-13）

- 新的一節用 STE 寫四句：有 `workBranch` 時在那個分支上工作，`config.local.yaml` 設它；不加 `Co-Authored-By`，`.claude/settings.json` 擋掉它。
- 模板若也叫 `## Commits`，會和 `AGENTS.shared.md` 的 `## Commits` 重複，所以 `AGENTS.shared.md` 只留一行，放在 `## Branches` 最後，連到 publish-gestalt。
- `check_ste.py` 對模板與 `AGENTS.md` 都是 PASS。

### 3.2 forge-setup.md（2026-11-13）

- 第 4 步加一段寫 `.claude/settings.json`，附上內容；放進原本那一段會有 7 句，超過 6 句，所以另成一段。
- `check_ste.py` 對 `forge-setup.md` 是 PASS；中文版同樣改。

### 3.3 workBranch 一定要有（2026-11-13）

- 使用者再看一次之後，決定第 11 行的 `workBranches` 也搬，而且每個 Forge 在每台電腦都要定義 work branch。
- 模板的句子不再寫「If `config.yaml` has `workBranch`」：一律在 `workBranch` 上工作，`workBranches` 列出每個 clone 的分支；有 `config.shared.yaml` 時，由每台的 `config.local.yaml` 設 `workBranch`。
- `gen_agents_md.py` 是每個 agency 都會跑的 script，所以在這裡檢查；`publish_snapshot.py` 的檢查照 [[Task 111]] 不變。
- forge-setup.md 的 Technical words 加 branch 與 clone；`check_ste.py` 對模板、`AGENTS.md` 與 forge-setup.md 都是 PASS。

**表 2：在 scratchpad 試跑 gen_agents_md.py**

| config.yaml | 結果 |
| --- | --- |
| 沒有 `workBranch` | `workBranch is not set`，`2` |
| `workBranches: [a, b]`、`workBranch: c` | `workBranches does not list workBranch c`，`2` |
| `workBranches: [a, c]`、`workBranch: c` | 寫出 `AGENTS.md`，`0` |
| 只有 `workBranch: c` | `0`；`workBranches` 不是一定要有 |

### 3.4 再讀一次 AGENTS.md（2026-11-13）

- 使用者要再檢查 `AGENTS.md`；從頭讀過，找到 5 個說法不精確的地方，使用者決定都改，`workBranches` 維持可有可無。

**表 3：AGENTS.md 的 5 個問題**

| 問題 | 改法 | 改的檔 |
| --- | --- | --- |
| 「每天一個 tag」，但同一天有 `-1`、`-2`、`-pull` 的 tag | 說同一天可以有更多 tag，舉 `archive/devbox-261113-1` 與 `-pull`；找 hash 要看所有這些 tag | `AGENTS.shared.md` |
| 引言說改 `config.yaml` 就跑指令，又說有 `config.shared.yaml` 時不改 `config.yaml` | 先只列 `config.shared.yaml` 與 `config.local.yaml`；沒有 `config.shared.yaml` 的，改 `config.yaml` 後也跑 | 模板 |
| 「for each computer」可以讀成每台各一份 | 改成「for all the computers」，引言與 File Names 兩處 | 模板 |
| 讀起來像每個 agency 都有 `workBranches` | 改成「If the `config.yaml` has `workBranches`」 | 模板 |
| 引言沒說路徑來自 `config.yaml` | 加上 `config.yaml` | 模板 |

- 改 tag 那段時，STE 檢查先報句子太長、三個不在字典的字，再報一段 7 句；改寫成兩句，發佈的兩行另成一段之後，`check_ste.py` 對模板與 `AGENTS.md` 都是 PASS。
- 只改說法、不改做法，所以 `CHANGES.md` 不另記；Forge 照 Task 112 那一筆跑 `gen_config.py` 就會拿到。

## 4. 要做的

1. ✅ 模板與 `AGENTS.shared.md`（`3.1`）。
2. ✅ forge-setup 與中文版（`3.2`）。
3. ✅ `CHANGES.md` 記一筆。
4. ✅ `workBranch` 一定要有（`3.3`）。
5. ✅ `AGENTS.md` 的 5 個說法（`3.4`）。
6. 使用者同意之後，和 [[Task 110]]、[[Task 111]] 一起照 [[publish-gestalt]] 發佈。

## 5. 驗證

- `gen_config.py --check`、`check_tasks.py` 與 `check_chores.py` 都是 PASS。
- `AGENTS.md` 有 Work Branch and Commits 一節，最後的 SkillsGestalt 部分沒有重複的規則。

## 6. 與其他 task 的關係

- [[Task 107]]：原本把不加 `Co-Authored-By` 寫在 `AGENTS-local.md`，並建 `.claude/settings.json`。
- [[Task 111]]：`workBranch`。

## 7. 知識

—

## 8. 日誌

### 2026-11-13

- 建立並做完：使用者決定不加 `Co-Authored-By` 是每個 agency 的規則；兩條規則搬進模板（`3.1`），forge-setup 多寫 `.claude/settings.json`（`3.2`）。Status 是完成。
- 使用者決定 `workBranches` 也搬，每個 Forge 都要定義 work branch：`gen_agents_md.py` 沒有 `workBranch` 就停，Forge 的範本與 forge-setup 跟著改（`3.3`）。
- 再讀一次 `AGENTS.md`，改了 5 個說法（`3.4`）。`4.` 第 6 項等使用者同意發佈。
