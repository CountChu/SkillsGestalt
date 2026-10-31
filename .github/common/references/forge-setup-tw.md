# Forge Setup

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-31`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-31`  `8cc2e2061175`

> 本檔案以 ASD-STE100 Simplified Technical English（STE）第 9 版寫成。
> 技術用字：agency、cell、chore、command、commit、day、directory、document、environment、file、Forge、Gestalt、git、introduction、InvestForge、line、link、placeholder、print、quote、repository、root、rule、script、section、sentence、setup、skill group、status、summary、table、task、template、term、text、twin、vault、workspace。

本文件說明怎麼建立一個 Forge，也就是使用 SkillsGestalt 的 `common` skill group 的 agency。
[glossary.md](glossary.md) 說明 agency、Gestalt 與 Forge 這些 term。
InvestForge 就是照這些 step 建立的 Forge。
例子用 BookForge，它只是一個例子。

## Make a Forge

依這個順序做。
每個 step 寫出要做的事，以及怎麼檢查。

1. **在 SkillsGestalt 的根目錄旁邊建立 workspace 的根目錄，並把它做成 git repository。**
   例如 `~/Library/CloudStorage/Dropbox/2-Areas-I/BookForge`。
   兩個根目錄並排時，script 在第 4 步寫出的連結比較短。
   檢查：在根目錄執行 `git status`，看得到它是一個 repository。
2. **把 [config-forge-tmp.yaml](../templates/config-forge-tmp.yaml) 複製成根目錄的 `config.yaml`，再換掉每個 placeholder。**
   `{GESTALT_ROOT}` 是 SkillsGestalt 的根目錄。
   `{WIKI_DIR}` 是這個 Forge 的 vault，`{WIKI_ROOT_DIR}` 是裝著所有 agency 的 vault 的目錄。
   每個值外面的引號要留著。
   檢查：`config.yaml` 的值裡沒有 `{GESTALT_ROOT}`、`{WIKI_DIR}` 或 `{WIKI_ROOT_DIR}`。
3. **在根目錄寫 `CLAUDE-local.md`。**
   它放只有這個 Forge 才有的規則，例如怎麼設定它的 Python environment。
   一行 `{CLAUDE-local}` 把它分成兩段。
   script 把這一行以上的部分放在 `CLAUDE.md` 的引言之後，以下的部分放在最後。
   這個 Forge 還沒有自己的規則時，寫一節 `## Settings of This Agency`，裡面一句話。
   檢查：這個檔在根目錄。
4. **產生 `CLAUDE.md`：從根目錄執行 `python {skillGroups.common}/scripts/gen_claude_md.py`。**
   script 用 `config.yaml` 的值與 `CLAUDE-local.md` 填入 `common` skill group 的 template。
   不要改 `CLAUDE.md`。
   要改規則，就改 `CLAUDE-local.md`，再執行一次 script。
   檢查：`python {skillGroups.common}/scripts/gen_claude_md.py --check` 印出 `PASS`。
5. **把這次的設定記成第一個 task：寫 `tasks/Task 1.md` 與 `dashboard/task-summary.md`。**
   git 不保留空的目錄，而沒有 `tasks/` 時，task 的檢查就會停下來。
   用下面兩段文字。
   task 檔與它那一列裡的日期，改成設定的那一天。
   檢查：`CLAUDE.md` 給出的 `check_tasks.py` 指令印出 `PASS`。
6. **照下面的文字寫 `dashboard/chore-summary.md`。**
   它的一列是 SkillsGestalt 的 chore `keep-english`，也就是 `config.yaml` 的 `keepEnglishChore` 指定的那一個。
   Title 與何時要做和 SkillsGestalt 的 chore 檔一樣，Started 是設定的那一天。
   這個 Forge 不做這個 chore 時，拿掉這一列與 `keepEnglishChore` 那一行。
   這個 Forge 有自己的 chore 之前，沒有 `chores/` 目錄。
   檢查：`CLAUDE.md` 給出的 `check_chores.py` 指令印出 `PASS`。
7. **commit `config.yaml`、`CLAUDE-local.md`、`CLAUDE.md`、`tasks/` 與 `dashboard/`。**
   然後在 `tasks/Task 1.md` 寫下設定完成，改它的狀態，再 commit 一次。
   檢查：`git status` 沒有任何變動。

第 5 步的 `tasks/Task 1.md`：

```
# Task 1 - 接上 SkillsGestalt

**Status**：進行中——照 forge-setup.md 接上 SkillsGestalt。
**Raised**：2026-10-31，建立本 agency，使用 SkillsGestalt 的 common skill group。
**Depends on**：—

## 1. 背景

—

## 2. 現況

—

## 3. 要做的

—

## 4. 驗證

—

## 5. 與其他 task 的關係

—

## 6. 知識

—

## 7. 日誌

### 2026-10-31

- 建立 task。
```

第 5 步的 `dashboard/task-summary.md`：

```
# Tasks

跨 session 的待辦工作。
每個 task 是 `tasks/Task N.md` 一個檔案。

| Task | Raised | Title | Status | Depends on |
| --- | --- | --- | --- | --- |
| [[Task 1]] | 2026-10-31 | 接上 SkillsGestalt | 🔄 | — |

Status：⬜ 尚未開始　🔄 進行中　✅ 完成　⊘ 取消。
```

第 6 步的 `dashboard/chore-summary.md`：

```
# Chores

會重複做的例行工作。

| Chore | Started | Title | 何時要做 | 上次執行 | Status |
| --- | --- | --- | --- | --- | --- |
| keep-english | 2026-10-31 | keep-English 稽核 | tw-keep-english.md 換了版本，和上次稽核的版本不同 | — | 🔁 |

Status：🔁 使用中　⏸️ 暫停　⏹️ 停用。
```

## Change an Older Workspace

有些 workspace 使用 `common` skill group，但它的 `CLAUDE.md` 是人寫的。
要把這樣的 workspace 改成 Forge，照下面的 step 做。
然後做「Make a Forge」一節的第 4 到 7 步。

- **把只有這個 workspace 才有的規則，從 `CLAUDE.md` 搬到 `CLAUDE-local.md`。**
  `common` skill group 的 template 已經有的規則不要搬。
  template 有 twin、Markdown 檔、task 與 chore 的規則。
- **把 [config-forge-tmp.yaml](../templates/config-forge-tmp.yaml) 有、而 `config.yaml` 沒有的值加上去，例如 `agencies` 與 `keepEnglishChore`。**
- **workspace 的某個 chore 和 SkillsGestalt 的 chore 做同樣的工作時，刪掉它的檔。**
  它那一列的 Chore 欄，寫成 SkillsGestalt 那個 chore 的文字名稱。
  它的執行紀錄搬到摘要表的 `## 執行紀錄` 一節，報告搬到 `checkpoints/chores/<name>`。
- **照 [chore-rules.md](../rules/chore-rules.md) 給自己的每個 chore 取名稱。**

## After a Change in SkillsGestalt

Forge 直接讀 SkillsGestalt 原本的位置。
所以 SkillsGestalt 一改，Forge 立刻跟著變。
這樣的改動之後，再執行一次 `CLAUDE.md` 的 `gen_claude_md.py`、`check_tasks.py` 與 `check_chores.py` 指令。
