# Task 97 - 讓 SkillsGestalt 同時適用於 VS Code Copilot 與 Claude Code

**Status**：完成——七個 sub task：97.1、97.2、97.3 與 97.7 完成，97.4 到 97.6 的 plugin 做法已取消；Claude Code 與 VS Code Local 照 AGENTS.md 找到 skill，Copilot harness 不照，是已知限制。
**Raised**：2026-11-02，使用者問目前的架構是否適用於 VS Code Copilot；查了官方說明，Copilot harness 找不到 `.github/common/skills` 的 skill，也不讀 CLAUDE.md。
**Depends on**：—

## 1. 背景

- skill 一開始照 VS Code Copilot 的方式寫：[gen-skill/SKILL.md](../skill-groups/common/skills/gen-skill/SKILL.md) 第 119 行說每個 `skillGroups` 的根目錄都列在 workspace 檔的 `chat.agentSkillsLocations`；[check-skill/SKILL.md](../skill-groups/common/skills/check-skill/SKILL.md) 第 176 行用 Copilot 的 `vscode_askQuestions`。
- 這個設定只在 `InvestForge.code-workspace` 裡；SkillsGestalt 沒有 `.code-workspace`，也沒有 `.vscode/settings.json`。
- 規則寫在根目錄的 CLAUDE.md，由 [gen_claude_md.py](../skill-groups/common/scripts/gen_agents_md.py) 從 [CLAUDE-tmp.md](../skill-groups/common/templates/AGENTS-tmp.md) 與 `CLAUDE-local.md` 產生；Claude Code 讀它，Copilot harness 不讀。
- Claude Code 看不到 `.github/common/skills`，所以在這裡都照 SKILL.md 手動做；兩邊都只支援一半。

## 2. 現況

### 2026-11-02 查的官方說明

讀的是 VS Code 的 [Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills) 與 [Custom instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions) 兩頁，頁尾日期 2026-10-28。
兩個 harness 找 skill 與規則的位置，整理在「知識」的表 1。

### 已決定（2026-11-02）

使用者回答了 8 個問題，除了第 3 題，都照建議：

1. **範圍**：Copilot 與 Claude Code 都要能找到 skill、讀到規則；包括只有一邊有的工具。
2. **skill 的位置**：先在 VS Code 實測 `chat.agentSkillsLocations` 是否還有效，再決定做法。
3. **規則檔**：改成 AGENTS.md，CLAUDE.md 只引用它。
4. **只有一邊有的工具**：寫成動作，不寫工具名稱，並在 skill-writing.md 加一條規則。
5. **拆成三個 sub task**，可以分開做。
6. **InvestForge**：每個 sub task 做完，在 [CHANGES.md](../skill-groups/common/CHANGES.md) 加一筆，由 InvestForge 的 follow-gestalt 接手。
7. **標題**：讓 SkillsGestalt 同時適用於 VS Code Copilot 與 Claude Code。
8. **先只開 task**，等使用者指定再做。

### 加上 plugin 的三個 sub task（2026-11-02）

使用者問了 plugin 的做法，又回答了 8 個問題，除了第 6 題，都照建議：

1. **再加三個 sub task**：[[Task 97.4]] marketplace 與兩個 skill group 的 plugin、[[Task 97.5]] chore 的步驟改成 skill、[[Task 97.6]] mermaid-view 成為 plugin。
2. **依賴**：97.4 依賴 97.1；97.5 與 97.6 依賴 97.4。
3. **SessionStart hook** 提醒該做的 chore，放在 97.5。
4. **mermaid-view 只搬 mod 本身**：Finder Quick Action 與頁面檔維持現在的位置。
5. **改成 skill 的 chore**：follow-gestalt、keep-english、rerecord-ste-custom。
6. **plugin 的名稱**：gestalt、gestalt-ext、mermaid-view；skill 在 Claude Code 裡是 `/gestalt:<skill>`。
7. **97.1 跟著改**：plugin 加進候選，並優先實測。
8. **先只加 sub task**。

### 取消 plugin，改名為 skill-groups（2026-11-02）

使用者決定捨棄 plugin 的做法，又回答了 8 個問題：

1. **97.4、97.5、97.6 改成取消**，檔案與摘要表的列保留。
2. **原因**：plugin 的架構不適合，因為有 chores。
3. **`.github` 改名為 `skill-groups`**，另開 [[Task 97.7]]。
4. **SessionStart hook 的提醒跟著捨棄**。
5. **skill 的位置寫在 AGENTS.md**，不用 symlink；[[Task 97.1]] 改成實測這個做法。
6. **名稱**：`skill-groups`；`config.yaml` 的 key 仍是 `skillGroups`。
7. **先只改 task**。

### 2026-11-02 兩個 harness 的差別對本 task 的影響

兩個 harness 的差別寫在「知識」一章；對本 task 的影響是：

- AGENTS.md 在 SkillsGestalt 的根目錄，兩個 harness 都讀得到：Copilot 讀 repo 根目錄到工作目錄的 AGENTS.md，Local 只讀 workspace 根目錄的。
- [[Task 97.1]] 在 VS Code 實測時，要在送出第一個提示之前，用 Chat 面板 New Chat（+）旁的 Session Target 選 harness。
- Session Target 裡沒有 Local 時，要打開實驗設定 `chat.editor.localAgent.enabled`。
- 使用者設定裡沒有 `chat.agentSkillsLocations`，所以實測不受它影響。

## 3. 要做的

- [[Task 97.1]] ✅ 實測 agent 照 AGENTS.md 找到 skill-groups 的 skill
- [[Task 97.2]] ✅ 規則改寫在 AGENTS.md，CLAUDE.md 只引用它
- [[Task 97.3]] ✅ skill 只寫動作，不寫某個 agent 才有的工具名稱
- [[Task 97.4]] ⊘ 建 plugin marketplace：gestalt 與 gestalt-ext 兩個 plugin
- [[Task 97.5]] ⊘ 三個 chore 的步驟改成 gestalt 的 skill，並以 hook 提醒
- [[Task 97.6]] ⊘ mermaid-view 的 mod 搬進 repo，成為 marketplace 的 plugin
- [[Task 97.7]] ✅ 把 .github 改名為 skill-groups

## 4. 驗證

- 沒有取消的 sub task，驗證都通過。
- 只開 SkillsGestalt 資料夾時，VS Code 的 Local harness 照 AGENTS.md 找到 `skill-groups/` 的 skill。
- VS Code 的 Copilot harness 不照 AGENTS.md 找 skill，是已知限制，見 [[Task 97.1]]；原本要它照 AGENTS.md 找到 skill 的這一條，改成上一條。
- 在 Claude Code 裡，規則照舊載入。

## 5. 與其他 task 的關係

- [[Task 93]]：把超過 1024 字元的 description 縮短，Copilot 才載入得了這些 skill。
- [[Task 88]]：寫了 forge-setup.md；skill 位置或規則檔改了，它要跟著改。
- [[Task 62]]：common 是上游；InvestForge 的改動只經 CHANGES.md，不在本 task 改。

## 6. 知識

### 適合寫成新 topic

- **標題**：VS Code 的 Copilot 與 Local harness
- **內容**：表 1 與表 2，加上下面幾條；表 1 也列出 Claude Code，作為比較。
  - 兩個 harness 都用 VS Code 設定的模型，「Local」不是指模型在本機跑。
  - 兩個都要在送出第一個提示之前選；chat 標題前面會顯示 harness；Ask、Agent、Plan 的選單與換模型都不改 harness。
  - skill 是否出現在 `/` 選單由 `user-invocable` 決定，文件沒寫兩個 harness 有沒有差別。
  - SKILL.md 的 frontmatter：`name` 只能有小寫字母、數字與連字號，要和資料夾名稱相同，最多 64 字元，不合的話 skill 不會載入，也不報錯；`description` 最多 1024 字元。
  - `chat.agentSkillsLocations`：一段說它「仍然支援，沒有 deprecated」，另一段（Local 那一節）說它「已 deprecated，Copilot harness 不讀」；兩段互相矛盾。
  - 文件沒有提到使用者設定裡打開的 `chat.useAgentSkills`。
  - Claude Code 的 Project instructions 設定可以改讀 AGENTS.md 的預設，例如兩個都讀；文件說某些 session 讀不到 AGENTS.md，那裡要由 CLAUDE.md import。
  - 文件沒寫：兩個 harness 在 subagent、問使用者的工具與 MCP 上的差別，以及 Local 能不能用 worktree。
- **來源**：VS Code 官方文件 [Agent harnesses](https://code.visualstudio.com/docs/agents/run/agent-harnesses)、[Agent harness 概念](https://code.visualstudio.com/docs/agents/concepts/agent-harnesses)、[Tools](https://code.visualstudio.com/docs/agents/run/tools)、[Approvals](https://code.visualstudio.com/docs/agents/run/approvals)、[Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills) 與 [Custom instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)，頁尾日期 2026-10-28；表 1 的兩個 harness 來自後兩頁。
  表 1 的 Claude Code 一欄來自 Claude Code 官方文件 [Skills](https://code.claude.com/docs/en/skills) 與 [Memory](https://code.claude.com/docs/en/memory) 兩頁，2026-11-02 讀原文核對過。
  內容由代理讀頁面後整理，還沒有逐頁核對；寫成 topic 之前要核對。

**表 1：VS Code 兩個 harness 與 Claude Code 找 skill 與規則的位置**

| 項目 | Copilot harness | Local harness | Claude Code |
| --- | --- | --- | --- |
| 專案的 skill | `.github/skills/` | `.github/skills/`、`.claude/skills/`、`.agents/skills/` | `.claude/skills/`：啟動目錄與上層，到 repo 根目錄；子目錄的 `<subdir>/.claude/skills/` 在處理那裡的檔案時才載入；`--add-dir` 的目錄底下的 `.claude/skills/` 也載入 |
| 個人的 skill | `~/.copilot/skills/` | `~/.copilot/skills/`、`~/.claude/skills/`、`~/.agents/skills/` | `~/.claude/skills/` |
| CLAUDE.md | 不讀 | `chat.useClaudeMdFile` 打開時讀根目錄、`.claude/`、`~/.claude/` 的 CLAUDE.md，以及 `CLAUDE.local.md` | 讀工作目錄與上層的 CLAUDE.md、`.claude/CLAUDE.md`、`CLAUDE.local.md`，以及 `~/.claude/CLAUDE.md`；子目錄的用到時才讀 |
| AGENTS.md | 不用設定就讀：repo 根目錄、工作目錄，以及兩者之間的目錄 | `chat.useAgentsMdFile`，預設打開；子目錄的要再打開 `chat.useNestedAgentsMdFiles` | v2.1.277 起，工作目錄與上層都沒有 CLAUDE.md、`.claude/CLAUDE.md`、`CLAUDE.local.md` 時直接讀；有的話只讀 CLAUDE.md，除非 CLAUDE.md 以 `@AGENTS.md` import；`.agents/` 下的都不讀 |
| `.github/copilot-instructions.md` | 讀 | `github.copilot.chat.codeGeneration.useInstructionFiles` 打開時讀 | 不讀；只有 `/init` 會把它的內容併進產生的 CLAUDE.md |

**表 2：兩個 harness 的差別**

| 項目 | Copilot harness | Local harness |
| --- | --- | --- |
| 是什麼 | 預設的 harness，用 Copilot SDK，在 Agent Host 執行 | VS Code 內建的 harness，在 extension host 執行 |
| 關掉視窗之後 | 仍可在背景繼續 | 停下 |
| 模型 | VS Code 設定的模型 | VS Code 設定的模型 |
| 在哪裡選 | Chat 面板 New Chat（+）旁的 Session Target，或 Agents 視窗 | 只有 Chat 面板 New Chat（+）旁的 Session Target |
| session 轉給另一個 harness | 不能轉給 Local | 可以轉給 Copilot |
| 工具 | 預設打開所有它能用的工具，但不是每個工具都能用 | 每次請求可以用 Configure Tools 選工具 |
| 權限 | Manual、Assisted、Allow all；Autopilot 是另一個模式 | 沒有 Assisted；Autopilot 是一個權限等級 |
| 沙箱與 policy | 可以把終端機放進沙箱 | 不強制執行期的沙箱與權限規則，也不載入 SDK Policy Hooks |
| Computer Use | 有 | 沒有 |
| 規則檔與 skill 的位置 | 見表 1 | 見表 1；AGENTS.md 只讀 workspace 根目錄的，子目錄的是實驗功能 |
| `/skills` 與 `/create-skill` | 沒有 | 有 |
| 照 AGENTS.md 找 skill（實測，[[Task 97.1]]） | 先查自己的 skill 清單、讀 chore 表，再以 glob 或文字搜尋；AGENTS.md 寫明「不要搜尋」也一樣 | 照 Skills 一節直接讀 SKILL.md |
| 官方的定位 | 建議平常用 | 像是轉換期保留的選項；要留在選單裡，打開實驗設定 `chat.editor.localAgent.enabled` |

### 適合併進現有 topic

—

### 不算知識

- InvestForge 的 `chat.agentSkillsLocations` 寫在 `InvestForge.code-workspace`。

## 7. 日誌

### 2026-11-02

- 表 1 加上 Claude Code 一欄：Claude Code 不讀 `.agents/` 下的任何檔；沒有 CLAUDE.md 時直接讀 AGENTS.md。
- 表 1 從「現況」搬到「知識」，兩個 topic 候選合併成「VS Code 的 Copilot 與 Local harness」；「現況」只留一句指向它。
- 「知識」裡兩個 harness 的差別改寫成表 2，表放不下的留成條列。
- 完成：[[Task 97.1]] 完成，Copilot harness 不照 AGENTS.md 找 skill，記成已知限制；驗證改成 Claude Code 與 Local，「知識」補上實測的結果。
- 查了兩個 harness 的差別：細節寫進「知識」，對本 task 的影響寫進「現況」。
- [[Task 97.3]] 完成：skill 只寫動作；skill-writing.md 多一條規則，check-skill 多了 criterion 5.6。
- [[Task 97.2]] 完成：規則寫在 AGENTS.md，CLAUDE.md 只有 `@AGENTS.md`。
- 連結的目標從 `CLAUDE-local.md`、`CLAUDE-tmp.md`、`gen_claude_md.py` 改成改名後的 `AGENTS-local.md`、`AGENTS-tmp.md`、`gen_agents_md.py`，字句沒有改（[[Task 97.2]]）。
- [[Task 97.7]] 完成：`.github` 改名為 `skill-groups`。
- 連結的目標路徑從 `../.github/` 改成 `../skill-groups/`，字句沒有改（[[Task 97.7]]）。
- 取消 plugin 的做法（[[Task 97.4]]、[[Task 97.5]]、[[Task 97.6]]），加上 [[Task 97.7]]，[[Task 97.1]] 改成實測 AGENTS.md 的做法。
- 加上 [[Task 97.4]]、[[Task 97.5]]、[[Task 97.6]]：把 skill group、chore 與 mod 做成 plugin。
- 提出：查了官方說明，決定分成 [[Task 97.1]]、[[Task 97.2]]、[[Task 97.3]]。
