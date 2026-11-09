# Task 97.4 - 建 plugin marketplace：gestalt 與 gestalt-ext 兩個 plugin

**Status**：取消——plugin 的架構不適合，因為有 chores：chore 的條件與紀錄是各 agency 自己的，放不進 plugin；改由 [[Task 97.7]] 把 `.github` 改名為 `skill-groups`。
**Raised**：2026-11-02，使用者問 plugin 的做法；skill group 的資料夾本來就有 `skills/<name>/SKILL.md`，加上 manifest 就是 plugin，不用搬檔。
**Depends on**：[[Task 97.1]]

## 1. 背景

- Claude Code 的 plugin 是一個資料夾：`.claude-plugin/plugin.json` 只要 `name`，skill 放在 `skills/<name>/SKILL.md`。
- marketplace 是 `.claude-plugin/marketplace.json`，列出每個 plugin 的 `name` 與 `source`；`source` 可以是相對路徑（以 `./` 開頭，不用 `..`）或 GitHub repo。
- VS Code 也接受 `.claude-plugin/plugin.json`，要打開 `chat.plugins.enabled`；專案的 `.claude/settings.json` 寫 `extraKnownMarketplaces` 與 `enabledPlugins`，兩邊都讀。
- 從本機路徑加入的 marketplace，相對路徑的 plugin 不複製，直接讀原檔；從 GitHub 安裝的會複製到 `~/.claude/plugins/cache/`，版本改了才更新。
- 讀的官方說明：Claude Code 的 [plugins](https://code.claude.com/docs/en/plugins)、[plugins-reference](https://code.claude.com/docs/en/plugins-reference)、[plugin-marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)，以及 VS Code 的 [Agent plugins](https://code.visualstudio.com/docs/copilot/customization/agent-plugins)。

## 2. 結論

—

## 3. 過程

### 2026-11-02 的規劃

**表 1：marketplace 的三個 plugin**

| Plugin | source | 內容 | 由哪個 sub task 做 |
| --- | --- | --- | --- |
| gestalt | `./.github/common` | common 的 skill、規則、範本與 script | 本 task |
| gestalt-ext | `./.github/external` | eli5 | 本 task |
| mermaid-view | `./mods/mermaid-view` | mermaid-view 這個 mod，只能在 Claude Code 用 | [[Task 97.6]] |

- Claude Code 裡的 skill 名稱會加上 plugin 的前綴，例如 `/gestalt:asd-ste`；VS Code 怎麼稱呼 plugin 的 skill，文件沒有寫。
- plugin 不載入它根目錄的 CLAUDE.md，所以 `.github/common/skills/CLAUDE.md` 的提醒不隨 plugin 生效。

## 4. 要做的

1. 在 root 加 `.claude-plugin/marketplace.json`，列 gestalt 與 gestalt-ext；在 `.github/common/` 與 `.github/external/` 各加 `.claude-plugin/plugin.json`。
2. 處理 skill 裡寫成 `{skillGroups.common}/...` 的路徑：從 GitHub 安裝時，它指向 config.yaml 設的路徑，不指向 plugin 的副本；決定是否改用 `${CLAUDE_PLUGIN_ROOT}`。
   Bash 工具執行的指令裡沒有這個變數，SKILL.md 要另外寫怎麼找到 plugin 的根目錄。
3. 決定 `version` 的規則：從 GitHub 安裝的人，版本改了才會更新。
4. SkillsGestalt 與 Forge 的 `.claude/settings.json` 啟用這兩個 plugin；InvestForge 的 `chat.agentSkillsLocations` 由 CHANGES.md 告訴它移除。
5. 改 [forge-setup.md](../skill-groups/common/references/forge-setup.md) 與 [gen-skill/SKILL.md](../skill-groups/common/skills/gen-skill/SKILL.md) 第 119 行，中文版也是。
6. 確認 publish-gestalt 發佈時帶上 marketplace.json 與兩個 plugin.json。
7. 在 CHANGES.md 加一筆。

## 5. 驗證

- `claude plugin validate .` 通過。
- 新的 Claude Code session 列出 `/gestalt:` 與 `/gestalt-ext:` 的每一個 skill。
- 只開 SkillsGestalt 時，VS Code Chat 列出這些 skill。
- 從 GitHub 的 `CountChu/SkillsGestalt` 加入 marketplace，也裝得起來。

## 6. 與其他 task 的關係

- [[Task 97.1]]：先實測 plugin 在兩邊能不能用，本 task 才做。
- [[Task 97.5]]、[[Task 97.6]]：把 chore 的 skill 與 mermaid-view 加進本 task 建的 marketplace。
- [[Task 97.2]]：plugin 不載入 CLAUDE.md，規則仍靠各 agency 的 AGENTS.md 或 CLAUDE.md。

## 7. 知識

—

## 8. 日誌

### 2026-11-02

- 連到的 `skills/CLAUDE.md` 已刪除，內容搬進 `AGENTS-tmp.md` 的 Skills 一節；連結改成 inline code，字句沒有改（[[Task 97.2]]）。
- 連結的目標路徑從 `../.github/` 改成 `../skill-groups/`，字句沒有改（[[Task 97.7]]）。
- 取消：plugin 的架構不適合，因為有 chores；改由 [[Task 97.7]] 處理。
- 提出。
