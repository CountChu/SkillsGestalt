# Glossary

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-30`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-30`  `8cc2e2061175`

> This file is in ASD-STE100 Simplified Technical English (STE), Issue 9.
> Technical words: agency, AI assistant, chore, directory, document, domain, file, Forge, Gestalt, glossary, investment, note, Obsidian, path, report, repository, root, rule, script, session, setting, skill, skill group, SkillsGestalt, subject, summary, table, target, template, term, vault, wiki, wikilink, workspace.

This glossary gives the terms that tell how the skills, the agents and the wikis operate together.
Each term has the same sense in each document of each agency.

## Agencies

- **agency** — a group of skills and agents that do work together, with the files and the wiki of that work.
  An agency has a workspace and a wiki.
  Each agency is a Gestalt or a Forge.
  SkillsGestalt and InvestForge are agencies.
- **Gestalt** — the agency that has the skills as its subject.
  It has the `common` skill group: the skills, the rules, the templates and the scripts that each agency uses.
  These items set the shape of each skill.
  There is only one Gestalt, and it is SkillsGestalt.
  In German, a Gestalt is a shape that is more than the sum of its parts.
- **Forge** — an agency that has one domain as its subject, for example investment.
  A Forge uses the `common` skill group of the Gestalt, and it has its own `dedi` skill group.
  There can be many Forges, and InvestForge is one of them.
  [forge-setup.md](forge-setup.md) tells how to make a Forge.
  The name of an agency is its subject, and then its type: Skills and Gestalt, or Invest and Forge.

## Parts of an Agency

- **workspace** — the root directory of the repository of an agency.
  When a document gives a path "from the root of the workspace", the path starts at this directory.
  The `config.yaml` at this root gives the settings of the agency.
  A VS Code workspace, which is a `.code-workspace` file, is a different item.
- **wiki** — the Obsidian vault of an agency, where its skills write notes and reports.
  The `wikiDir` setting of `config.yaml` gives its path.
  Each agency has its own wiki, for example SkillsLlmWiki and InvLlmWiki.
- **knowledge-base root** — the directory that contains the wikis of all the agencies.
  The `wikiRootDir` setting of `config.yaml` gives its path.
  A wikilink can go to a note in each wiki in this root.
  Thus, to find the target of a wikilink, a check must examine all of the root.
- **skill group** — a set of skills that has one root directory.
  The `skillGroups` setting of `config.yaml` gives the root of each skill group.
  A skill of the group `g` is in `{skillGroups.g}/skills/<name>/`.
  - `common` — the skill group of the Gestalt, which each agency uses.
    In SkillsGestalt, its root is `.github/common`.
    In a Forge, its root is the path of that directory in SkillsGestalt.
  - `dedi` — the skill group of one Forge: the skills that only that Forge uses.
    In InvestForge, its root is `.claude`.
  - `external` — the skills that come from a source that is not an agency, for example eli5.
- **agent** — an AI assistant, for example Claude Code, that does work in a workspace.
  It reads the instructions in the `CLAUDE.md` of the workspace, and it does the steps of the skills.
- **task** — work that continues after one session, and that becomes complete.
  The tasks of an agency are in `tasks/`, and their summary table is `dashboard/task-summary.md`.
  [task-rules.md](../rules/task-rules.md) tells how to write a task.
- **chore** — work that an agent must do again each time that a condition occurs.
  The chores of an agency are in `chores/`, and their summary table is `dashboard/chore-summary.md`.
  [chore-rules.md](../rules/chore-rules.md) tells how to write a chore.
