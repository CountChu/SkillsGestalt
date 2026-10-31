# Glossary

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-30`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-30`  `8cc2e2061175`

> 本檔案以 ASD-STE100 Simplified Technical English（STE）第 9 版寫成。
> 技術用字：agency、AI assistant、chore、directory、document、domain、file、Forge、Gestalt、glossary、investment、note、Obsidian、path、report、repository、root、rule、script、session、setting、skill、skill group、SkillsGestalt、subject、summary、table、target、template、term、vault、wiki、wikilink、workspace。

本 glossary 列出說明 skill、agent 與 wiki 如何一起運作的 term。
每個 term 在每個 agency 的每份文件裡都是同一個意思。

## Agencies

- **agency**——一群一起工作的 skill 與 agent，加上這些工作的檔案與 wiki。
  一個 agency 有一個 workspace 和一個 wiki。
  每個 agency 是 Gestalt 或 Forge。
  SkillsGestalt 與 InvestForge 都是 agency。
- **Gestalt**——以 skill 本身為主題的 agency。
  它有 `common` skill group：每個 agency 使用的 skill、規則、template 與 script。
  這些項目決定每個 skill 的形態。
  Gestalt 只有一個，就是 SkillsGestalt。
  在德文裡，Gestalt（完形）是大於各部分總和的整體形態。
- **Forge**——以一個領域為主題的 agency，例如投資。
  Forge 使用 Gestalt 的 `common` skill group，也有自己的 `dedi` skill group。
  Forge 可以有很多個，InvestForge 是其中之一。
  [forge-setup.md](forge-setup.md) 說明怎麼建立一個 Forge。
  agency 的名稱是它的主題，再接它的類型：Skills 加 Gestalt，或 Invest 加 Forge。

## Parts of an Agency

- **workspace**——agency 的 repository 的根目錄。
  文件說一個路徑「從 workspace 的根目錄」起算時，路徑從這個目錄開始。
  這個根目錄的 `config.yaml` 給出 agency 的設定。
  VS Code 的 workspace，也就是 `.code-workspace` 檔，是另一個東西。
- **wiki**——agency 的 Obsidian vault，它的 skill 在這裡寫筆記與報告。
  `config.yaml` 的 `wikiDir` 設定給出它的路徑。
  每個 agency 有自己的 wiki，例如 SkillsLlmWiki 與 InvLlmWiki。
- **knowledge-base root**——裝著所有 agency 的 wiki 的目錄。
  `config.yaml` 的 `wikiRootDir` 設定給出它的路徑。
  一個 wikilink 可以連到這個根目錄裡任何一個 wiki 的筆記。
  因此，要找 wikilink 的目標，檢查必須掃過整個根目錄。
- **skill group**——有同一個根目錄的一組 skill。
  `config.yaml` 的 `skillGroups` 設定給出每個 skill group 的根目錄。
  group `g` 的 skill 在 `{skillGroups.g}/skills/<name>/`。
  - `common`——Gestalt 的 skill group，每個 agency 都使用它。
    在 SkillsGestalt，它的根目錄是 `.github/common`。
    在 Forge，它的根目錄是 SkillsGestalt 裡那個目錄的路徑。
  - `dedi`——一個 Forge 的 skill group：只有那個 Forge 使用的 skill。
    在 InvestForge，它的根目錄是 `.claude`。
  - `external`——來源不是 agency 的 skill，例如 eli5。
- **agent**——在 workspace 裡工作的 AI 助理，例如 Claude Code。
  它讀 workspace 的 `CLAUDE.md` 裡的指示，並執行 skill 的 step。
- **task**——跨過一個 session 繼續、最後會完成的工作。
  agency 的 task 在 `tasks/`，摘要表是 `dashboard/task-summary.md`。
  [task-rules.md](../rules/task-rules.md) 說明怎麼寫 task。
- **chore**——每次某個條件發生時，agent 都必須再做一次的工作。
  agency 的 chore 在 `chores/`，摘要表是 `dashboard/chore-summary.md`。
  [chore-rules.md](../rules/chore-rules.md) 說明怎麼寫 chore。
