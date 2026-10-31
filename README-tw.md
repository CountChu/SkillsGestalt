# SkillsGestalt

共用的 agent skill、它們遵循的規則，以及檢查它們的 script。
英文版是 [README.md](README.md)。

## Gestalt and Forge

SkillsGestalt 是 Gestalt：以 skill 本身為主題的 agency。
以其他主題為主的 agency，例如 InvestForge，是 Forge，它使用本 repository 的 skill。
[glossary.md](.github/common/references/glossary.md) 說明這些 term。
要建立一個 Forge，照 [forge-setup.md](.github/common/references/forge-setup.md) 做。

## What Is Here

- [.github/common/skills/](.github/common/skills/)：skill，每個 skill 一個資料夾。
  skill 的 `SKILL.md` 寫出它的 step。
  它的 `README.md`（有的話）說明怎麼修改這個 skill。
- [.github/common/rules/](.github/common/rules/)：skill 與文件遵循的規則，例如 [md-style.md](.github/common/rules/md-style.md) 與 [skill-writing.md](.github/common/rules/skill-writing.md)。
- [.github/common/references/](.github/common/references/)、[.github/common/templates/](.github/common/templates/) 與 [.github/common/scripts/](.github/common/scripts/)：skill 用到的參考文件、template 與 script。
- [tasks/](tasks/) 與 [dashboard/task-summary.md](dashboard/task-summary.md)：跨 session 繼續進行的工作，每個 task 一個檔案。
- [chores/](chores/) 與 [dashboard/chore-summary.md](dashboard/chore-summary.md)：每當某個條件出現就要再做一次的工作。
- [CLAUDE.md](CLAUDE.md)：給在這個 workspace 工作的 agent 的指示。

## Getting Started

1. 把 [config.example.yaml](config.example.yaml) 複製成 workspace 根目錄的 `config.yaml`。
   再把 `wikiDir` 設成你的 Obsidian vault。
2. 讀某個 skill 的 `SKILL.md`，照它的 step 做。

## Not in This Repository

- ASD-STE100 Simplified Technical English 規格，第 9 版。
  asd-ste skill 從 `external/ASD-STE100_ISSUE9.pdf` 讀取它。
  請向 ASD 取得一份：<https://www.asd-ste100.org/>。
  [ste-dictionary.json](.github/common/skills/asd-ste/references/ste-dictionary.json) 是規格 Part 2 的字典，由規格做成。
- 從外面來的 skill，放在 `.github/external/`。

## License

MIT License，見 [LICENSE](LICENSE)。
