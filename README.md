# SkillsGestalt

Shared agent skills, the rules that they follow, and the scripts that check them.
The Traditional Chinese version is [README-tw.md](README-tw.md).

## Gestalt and Forge

SkillsGestalt is the Gestalt: the agency that has the skills as its subject.
An agency that has a different subject, for example InvestForge, is a Forge, and it uses the skills of this repository.
[glossary.md](skill-groups/common/references/glossary.md) gives these terms.
To make a Forge, follow [forge-setup.md](skill-groups/common/references/forge-setup.md).

## What Is Here

- [skill-groups/common/skills/](skill-groups/common/skills/): the skills, one directory for each skill.
  The `SKILL.md` of a skill gives its steps.
  Its `README.md`, when it has one, tells how to change the skill.
- [skill-groups/common/rules/](skill-groups/common/rules/): the rules that the skills and the documents follow, for example [md-style.md](skill-groups/common/rules/md-style.md) and [skill-writing.md](skill-groups/common/rules/skill-writing.md).
- [skill-groups/common/references/](skill-groups/common/references/), [skill-groups/common/templates/](skill-groups/common/templates/) and [skill-groups/common/scripts/](skill-groups/common/scripts/): the references, the templates and the scripts that the skills use.
- [tasks/](tasks/) and [dashboard/task-summary.md](dashboard/task-summary.md): the work that continues after one session, one file for each task.
- [chores/](chores/) and [dashboard/chore-summary.md](dashboard/chore-summary.md): the work that is done again each time that a condition occurs.
- [AGENTS.md](AGENTS.md): the instructions for an agent that works in this workspace.
  [CLAUDE.md](CLAUDE.md) contains only the line `@AGENTS.md`, for Claude Code.

## Getting Started

1. Write `config.local.yaml` at the root of the workspace, with the line `wikiDir: <your Obsidian vault>`.
   Then run `python skill-groups/common/scripts/gen_config.py`: it makes `config.yaml` from [config.shared.yaml](config.shared.yaml) and `config.local.yaml`.
2. Read the `SKILL.md` of a skill, and do its steps.

## Not in This Repository

- The ASD-STE100 Simplified Technical English specification, Issue 9.
  The asd-ste skill reads it at `external/ASD-STE100_ISSUE9.pdf`.
  Get your copy from ASD at <https://www.asd-ste100.org/>.
  [ste-dictionary.json](skill-groups/common/skills/asd-ste/references/ste-dictionary.json) is the dictionary of Part 2 of the specification, built from it.
- The skills that come from outside, in `skill-groups/external/`.

## License

The MIT License, in [LICENSE](LICENSE).
