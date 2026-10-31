# SkillsGestalt

Shared agent skills, the rules that they follow, and the scripts that check them.
The Traditional Chinese version is [README-tw.md](README-tw.md).

## Gestalt and Forge

SkillsGestalt is the Gestalt: the agency that has the skills as its subject.
An agency that has a different subject, for example InvestForge, is a Forge, and it uses the skills of this repository.
[glossary.md](.github/common/references/glossary.md) gives these terms.
To make a Forge, follow [forge-setup.md](.github/common/references/forge-setup.md).

## What Is Here

- [.github/common/skills/](.github/common/skills/): the skills, one directory for each skill.
  The `SKILL.md` of a skill gives its steps.
  Its `README.md`, when it has one, tells how to change the skill.
- [.github/common/rules/](.github/common/rules/): the rules that the skills and the documents follow, for example [md-style.md](.github/common/rules/md-style.md) and [skill-writing.md](.github/common/rules/skill-writing.md).
- [.github/common/references/](.github/common/references/), [.github/common/templates/](.github/common/templates/) and [.github/common/scripts/](.github/common/scripts/): the references, the templates and the scripts that the skills use.
- [tasks/](tasks/) and [dashboard/task-summary.md](dashboard/task-summary.md): the work that continues after one session, one file for each task.
- [chores/](chores/) and [dashboard/chore-summary.md](dashboard/chore-summary.md): the work that is done again each time that a condition occurs.
- [CLAUDE.md](CLAUDE.md): the instructions for an agent that works in this workspace.

## Getting Started

1. Copy [config.example.yaml](config.example.yaml) to `config.yaml` at the root of the workspace.
   Then set `wikiDir` to your Obsidian vault.
2. Read the `SKILL.md` of a skill, and do its steps.

## Not in This Repository

- The ASD-STE100 Simplified Technical English specification, Issue 9.
  The asd-ste skill reads it at `external/ASD-STE100_ISSUE9.pdf`.
  Get your copy from ASD at <https://www.asd-ste100.org/>.
  [ste-dictionary.json](.github/common/skills/asd-ste/references/ste-dictionary.json) is the dictionary of Part 2 of the specification, built from it.
- The skills that come from outside, in `.github/external/`.

## License

The MIT License, in [LICENSE](LICENSE).
