# Task 99 - 評估 Claude Code 直接讀 AGENTS.md 之後是否還需要 CLAUDE.md

**Status**：完成——保留根目錄只有 `@AGENTS.md` 的 CLAUDE.md：import 不會讓 AGENTS.md 被讀兩次，又能涵蓋讀不到 AGENTS.md 的 session 與 `CLAUDE.local.md` 擋掉 AGENTS.md 的情況；`gen_agents_md.py`、範本與 CLAUDE.md 都不改。
**Raised**：2026-11-02，核對 Claude Code 的 Memory 文件時發現，v2.1.277 起沒有 CLAUDE.md 時會直接讀 AGENTS.md，[[Task 97.2]] 留下的 CLAUDE.md 可能已經多餘。
**Depends on**：—

## 1. 背景

- [[Task 97.2]] 把規則改寫在 AGENTS.md，由 [gen_agents_md.py](../skill-groups/common/scripts/gen_agents_md.py) 從 [AGENTS-tmp.md](../skill-groups/common/templates/AGENTS-tmp.md) 與 [AGENTS-local.md](../AGENTS.shared.md) 產生。
- 同一支 script 也寫出只有一行 `@AGENTS.md` 的 CLAUDE.md，因為當時認定 Claude Code 只讀 CLAUDE.md；VS Code 的 Copilot harness 不讀 CLAUDE.md，但不用設定就讀 AGENTS.md。
- 2026-11-02 核對 Claude Code 的 [Memory](https://code.claude.com/docs/en/memory) 文件，寫進 [[Task 97]] 「知識」表 1 的 Claude Code 欄：v2.1.277 起，工作目錄與上層都沒有 CLAUDE.md 時直接讀 AGENTS.md。
- 這個 task 只評估、寫下建議，不改 script、範本與 CLAUDE.md。

## 2. 結論

—

## 3. 過程

### 官方文件（2026-11-02 讀）

來源是 Claude Code 官方文件 [Memory](https://code.claude.com/docs/en/memory) 的 AGENTS.md 一節與相關的幾節，由代理讀頁面後回報；頁面後段約四分之一只拿到摘要。

- **直接讀 AGENTS.md 要 v2.1.277 以上**。
- **預設只在沒有 CLAUDE.md 時讀 AGENTS.md**：工作目錄或任何上層有 `CLAUDE.md`、`.claude/CLAUDE.md` 或 `CLAUDE.local.md`，就只讀 CLAUDE.md；CLAUDE.md 以 `@AGENTS.md` import 時，AGENTS.md 經由 import 讀進來。
- **不擋 AGENTS.md 的檔**：`~/.claude/CLAUDE.md`、組織的 managed CLAUDE.md，以及 `.claude/rules/` 的檔。
- **沒有被擋時讀的檔**：工作目錄與上層的每一個 `AGENTS.md` 與 `.claude/AGENTS.md`；子目錄的 AGENTS.md 在以 Read 讀那裡的檔、而那裡沒有自己的三種 CLAUDE.md 時才讀。
  `AGENTS.local.md`、`AGENTS.override.md` 與 `.agents/` 下的檔都不讀。
- **`CLAUDE.local.md` 也會擋**：文件特別說，在靠 AGENTS.md 的專案加一個 `CLAUDE.local.md`，Claude 就不再讀 AGENTS.md。
- **import 不會讀兩次**：文件說，不管 Project instructions 設成什麼，留著 import 都不會讓 AGENTS.md 被讀兩次。
  文件在「Share one file with other coding tools」一節建議：專案也有 CLAUDE.md、Project instructions 設成 `claude-md`，或 session 讀不到 AGENTS.md 時，在 CLAUDE.md 寫 `@AGENTS.md`。
  另一個做法是 `ln -s AGENTS.md CLAUDE.md`，但 Edit 與 Write 不能寫穿 symlink，Windows 的 clone 沒設 `core.symlinks` 也會壞。
- **Project instructions 設定**：見表 1。
  它在 `/config` 的面板裡；寫在設定檔時是 `pluginConfigs` 的 `"cc-plugin-agents-md@builtin"` 的 `options.instructionFiles`（v2.1.285 以前的 ID 是 `agents-md@builtin`）。
  只從 `~/.claude/settings.json`、`--settings` 的檔或 managed settings 讀，專案與 local 的設定檔裡的會被忽略，所以不能隨 repo 帶給 Forge。

**表 1：Project instructions 的值**

| 值 | 讀哪些檔 |
| --- | --- |
| `claude-md-or-agents-md` | 預設：有 CLAUDE.md 就只讀 CLAUDE.md，沒有才讀 AGENTS.md |
| `claude-md-and-agents-md` | 兩種都讀，每一層先 CLAUDE.md 再 AGENTS.md |
| `claude-md` | 只讀 CLAUDE.md |
| `managed-only` | 啟動時只讀組織的 managed CLAUDE.md 與 auto memory |

### 哪些 session 讀不到 AGENTS.md

文件列出只讀 CLAUDE.md、`/config` 也沒有 Project instructions 的情況：

- Claude Code 比 v2.1.277 舊。
- 讀 AGENTS.md 的內建 plugin 被 `/plugin` 關掉。
- 有時是從 v2.1.276 以前升級之後的第一個 session。
- v2.1.281 以前，有些 session 只讀 CLAUDE.md，例如 Amazon Bedrock 上的，或關掉 telemetry 的。

文件沒有點名 Cowork、cloud、SDK、IDE、desktop app 或 subagent 讀不到 AGENTS.md，也沒說原因。
關於 subagent，文件只說沒有專案指示就啟動的 subagent，也不帶這些檔。

### 本機與 Forge

- **本機版本**：`claude --version` 是 2.1.289，比 2.1.277 新。
- **這個 session**（desktop app 的 Code 分頁）：規則以「CLAUDE.md 的內容，接著 AGENTS.md 的內容」載入，和文件說的 import 一致。
- **上層目錄**：SkillsGestalt 到 `/` 之間沒有 CLAUDE.md、`.claude/CLAUDE.md` 或 `CLAUDE.local.md`；只有 `~/.claude/CLAUDE.md`，文件說它不擋。
- **InvestForge**：沒有 `CLAUDE.local.md`，也沒有 `.claude/CLAUDE.md`。
  它還沒跟上 [[Task 97.2]]：仍是舊的 CLAUDE.md 全文與 `CLAUDE-local.md`，沒有 AGENTS.md。
- **使用者設定**：`~/.claude/settings.json` 與 `settings.local.json` 都沒有設 Project instructions，所以是預設值。
- **實測沒有做成**：在 scratchpad 建了三個目錄（只有 AGENTS.md、CLAUDE.md import AGENTS.md、AGENTS.md 加 `CLAUDE.local.md`），以 `claude -p` 問指示裡的暗號；三次都在 sandbox 裡 `OAuth session expired` 失敗。
  所以「只有 AGENTS.md 時會讀」只有文件為證，見「5. 驗證」。

### [[Task 97.2]] 當初為什麼保留 CLAUDE.md

- 它的決定 3 是「CLAUDE.md 只有 `@AGENTS.md` 一行」，理由寫在 gen_agents_md.py 的 docstring：Copilot 讀 AGENTS.md 不讀 CLAUDE.md，Claude Code 讀 CLAUDE.md，以 import 讀進 AGENTS.md 的全部。
- 那時還不知道 Claude Code 會直接讀 AGENTS.md，所以保留的理由是「Claude Code 只讀 CLAUDE.md」，不是這個 task 找到的理由。

### 已決定（2026-11-02）

使用者回答了 6 個問題，都照建議：

1. **保留 CLAUDE.md**，理由見下一節。
2. **實測記為未驗證**，列進「5. 驗證」，由使用者在自己的終端機跑。
3. **task 完成**：這次只評估。
4. **拿掉時要改的檔寫在「3. 過程」，標明不做**；「4. 要做的」寫 —。
5. **AGENTS-tmp.md 第 11 行只記在這裡，不改範本**。
6. **知識寫成「適合併進現有 topic」**，併進 [[Task 97]] 的 topic 候選。

### 建議：保留

- **留著沒有壞處**：import 不會讓 AGENTS.md 被讀兩次，CLAUDE.md 只有一行，由 script 產生，`--check` 也比對它。
- **拿掉有風險**：
  - 舊版、內建 plugin 被關掉、升級後的第一個 session，以及 v2.1.281 以前的 Bedrock 或關掉 telemetry 的 session，都只讀 CLAUDE.md；沒有 CLAUDE.md，這些 session 什麼規則都讀不到。
  - 使用者或 Forge 加一個 `CLAUDE.local.md`，就擋掉 AGENTS.md；有 CLAUDE.md import，規則照樣讀到。
  - 工作目錄的上層有一個別人寫的 CLAUDE.md 時也一樣。
  - 改用 `claude-md-and-agents-md` 只能設在每個使用者的 `~/.claude/settings.json`，不能隨 repo 走，Forge 的每個使用者都要自己設。
- **AGENTS-tmp.md 第 11 行仍然正確**：它說 Claude Code 讀 CLAUDE.md，而這一行讓它讀到全部；有 CLAUDE.md 時，Claude Code 確實只讀 CLAUDE.md。
  只是理由不完整：新版沒有 CLAUDE.md 也會讀 AGENTS.md，保留是為了讀不到 AGENTS.md 的 session 與擋住 AGENTS.md 的檔。
  gen_agents_md.py docstring 第 13 到 14 行的說法也一樣。

### 如果拿掉（不做）

日後改變主意時要改的檔：

- [gen_agents_md.py](../skill-groups/common/scripts/gen_agents_md.py)：拿掉 `CLAUDE_TEXT` 與 `wanted` 裡的 `'CLAUDE.md'`；docstring 第 2、11、13 到 14 行、`--check` 的說明（第 53 行附近）與第 197 行的訊息不再提 CLAUDE.md。
  要決定 script 遇到已有的 CLAUDE.md 時怎麼辦：只有 `@AGENTS.md` 一行的就刪掉，別的內容就停下說明。
- [AGENTS-tmp.md](../skill-groups/common/templates/AGENTS-tmp.md)：第 11 行改成說明 Claude Code v2.1.277 起直接讀 AGENTS.md；第 13 行的「or `CLAUDE.md`」拿掉；再重新產生 AGENTS.md。
- [forge-setup.md](../skill-groups/common/references/forge-setup.md) 與中文版：第 5 步的標題與第 42、43 行、第 8 步要 commit 的檔；第 132 行起的「已有人寫的 CLAUDE.md」一節要加上：搬完之後刪掉 CLAUDE.md。
- [README.md](../README.md) 與中文版：第 23 行。
- [follow-gestalt.md](../chores/follow-gestalt.md)：第 22 行的「AGENTS.md 與 CLAUDE.md」。
- 根目錄的 CLAUDE.md：`git rm`。
- 已有的 CHANGES.md 條目與 `tasks/` 的舊紀錄不改。

[CHANGES.md](../skill-groups/common/CHANGES.md) 的草稿：

```
- **CLAUDE.md 拿掉，Claude Code 直接讀 AGENTS.md**（Task N）：Claude Code v2.1.277 起，沒有 CLAUDE.md、`.claude/CLAUDE.md` 與 `CLAUDE.local.md` 時直接讀 AGENTS.md，所以 gen_agents_md.py 不再寫 CLAUDE.md，`--check` 只比對 AGENTS.md；只有 `@AGENTS.md` 一行的 CLAUDE.md 由 script 刪掉。
  Forge 要做：確定每個使用者的 Claude Code 是 v2.1.277 以上；執行 `{python} {skillGroups.common}/scripts/gen_agents_md.py`，commit 刪掉的 CLAUDE.md；有 `CLAUDE.local.md` 的使用者，要把 Project instructions 設成 `claude-md-and-agents-md`，否則讀不到 AGENTS.md。
```

## 4. 要做的

—

## 5. 驗證

- 已做：官方文件 Memory 頁的 AGENTS.md 一節、「Share one file with other coding tools」與讀不到 AGENTS.md 的情況，2026-11-02 由代理讀過。
- 已做：`claude --version` 是 2.1.289；InvestForge 與 SkillsGestalt 的上層沒有會擋 AGENTS.md 的檔。
- 未驗證：只有 AGENTS.md、CLAUDE.md import AGENTS.md、AGENTS.md 加 `CLAUDE.local.md` 三種目錄，Claude Code 各讀到什麼。
  在 sandbox 裡 `claude -p` 無法登入；使用者可以在自己的終端機，於只放一個 AGENTS.md 的空目錄執行 `claude -p "What code word appears in your project instructions?"` 來驗證。

## 6. 與其他 task 的關係

- [[Task 97]]：它「知識」的表 1 記下 Claude Code 讀 AGENTS.md 的方式，這個 task 由此提出。
- [[Task 97.2]]：決定 CLAUDE.md 只有 `@AGENTS.md` 一行；這個 task 確認保留，理由換成讀不到 AGENTS.md 的 session 與 `CLAUDE.local.md`。
- [[Task 62]]：common 是上游；這個 task 不改 common，不加 CHANGES.md，InvestForge 不必做什麼。

## 7. 知識

### 適合寫成新 topic

—

### 適合併進現有 topic

- **topic**：[[Task 97]] 的候選「VS Code 的 Copilot 與 Local harness」，表 1 的 Claude Code 欄。
- **要加的**：
  - Project instructions 的四個值（本檔表 1），以及它只能設在 `~/.claude/settings.json`、`--settings` 的檔或 managed settings，專案的設定檔裡的會被忽略。
  - 讀不到 AGENTS.md 的情況：比 v2.1.277 舊、內建 plugin 被 `/plugin` 關掉、有時是升級後的第一個 session、v2.1.281 以前的 Bedrock 或關掉 telemetry 的 session。
  - `CLAUDE.local.md` 也擋 AGENTS.md；`~/.claude/CLAUDE.md` 不擋。
  - CLAUDE.md 以 `@AGENTS.md` import 時，AGENTS.md 不會被讀兩次。
- **來源**：Claude Code 官方文件 [Memory](https://code.claude.com/docs/en/memory)，2026-11-02 由代理讀頁面，頁面後段只拿到摘要；寫成 topic 之前要核對。

### 不算知識

- 本機 Claude Code 是 2.1.289；InvestForge 還沒跟上 [[Task 97.2]]，沒有 `CLAUDE.local.md`。
- sandbox 裡的 `claude -p` 因 OAuth 過期無法登入，不能用來實測。

## 8. 日誌

### 2026-11-02

- 提出並完成：評估後建議保留 CLAUDE.md，不改 script、範本與 CLAUDE.md。
