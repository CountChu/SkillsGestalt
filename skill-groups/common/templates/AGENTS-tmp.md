# {agencyName}

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-30`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-11-02`  `c612bdfa1ea7`

> This file is in ASD-STE100 Simplified Technical English (STE), Issue 9.
> Technical words: agency, argument, audit, branch, chore, clone, command, commit, computer, directory, English, file, git, glob, line, list, message, pattern, repository, root, script, section, session, skill, summary, table, template, term, text, twin, user, version.

Instructions for an agent that works in this agency.
A script makes this file from the template `{skillGroups.common}/templates/AGENTS-tmp.md`, and from the `AGENTS.shared.md` and the `config.yaml` at the root.
The script also makes `CLAUDE.md`, which contains only the line `@AGENTS.md`: Claude Code reads `CLAUDE.md`, and this line gives it all of this file.

Do not change this file or `CLAUDE.md`.
To change a rule for each agency, change the template.
To change a rule for only this agency, change `AGENTS.shared.md`.
Then, and after each change to the `config.shared.yaml` or the `config.local.yaml` at the root, run this command from the root:

```bash
python {skillGroups.common}/scripts/gen_config.py
```

Also run it after you add or remove a skill, because it makes the table of skills in the section "Skills".
The command first makes the `config.yaml` from the `config.shared.yaml` and the `config.local.yaml`.
Do not change the `config.yaml`: change `config.shared.yaml` for all the computers, or `config.local.yaml` for only this computer.

{AGENTS-shared-top}

## Skills

When a request starts with `/<name>`, `<name>` is the name of the skill to do, and the subsequent text is the argument of the skill.
For example, in `/check-skill asd-ste 5.6`, the skill is `check-skill`, and `asd-ste 5.6` is its argument.
When a request gives the name of a skill without `/`, do the same.

Each skill is in a skill group.
This table gives each skill group of the `skillGroups` of the `config.yaml` at the root, its root directory, and the names of its skills:

{skillGroupRoots}

A skill is in `<root of its skill group>/skills/<name of the skill>/SKILL.md`, for example `{skillGroups.common}/skills/chinese/SKILL.md`.
These skills are not in the skill list of the agent.
Find the name in the table, and read the `SKILL.md` of the first skill group that has the name.
Then do its steps.

Do not use a file search, a glob pattern or a text search to find a skill.
If the table does not have the name, it is not a skill.
If the root has `chores/<name>.md`, it is a chore: see the section "Chores".
If not, tell the user, and stop.

Before you change a skill, read its `README.md`, if it has one, and [skill-writing.md]({skillGroups.common}/rules/skill-writing.md).
Make each change that the section "When the Skill Is Changed" of the `README.md` gives, in the same run.
Then run the checks that the `README.md` gives.
The `SKILL.md` of a skill does not refer to its `README.md`, because a run of the skill must not read the `README.md`.

## Markdown

When you write or change a Markdown file in the repository, follow [md-style.md]({skillGroups.common}/rules/md-style.md).

## File Names

The name of a file tells which computers and agencies use it, and if it is in git:

- `-tmp`, for example `AGENTS-tmp.md`: a template in `{skillGroups.common}/templates/`, for many agencies.
  It is in git.
- `.shared.`, for example `AGENTS.shared.md`: a file of only this agency, for all the computers.
  It is in git.
- `.local.`, for example `config.local.yaml`: a file of only this computer.
  It is not in git.

When you add such a file, give it a name that follows this list.

## Work Branch and Commits

Do your work on the branch that `workBranch` in the `config.yaml` at the root gives.
Each clone of this agency has its own work branch.
The `workBranches` of the `config.yaml` gives the list of them.
The `config.local.yaml` of each computer sets `workBranch`.

Do not put a `Co-Authored-By` line in a commit message.
The `.claude/settings.json` at the root stops this line in the commits of Claude Code.

## 繁體中文 twins

A Markdown file with a `-tw.md` adjacent to it has a 繁體中文 twin.
Put each change to the English file into the twin in the same run.
Use the [chinese]({skillGroups.common}/skills/chinese/SKILL.md) skill to change the twin.
It translates only the text that changed after the last commit of the twin, and then it compares the two files.

A twin keeps the terms of [tw-keep-english.md]({skillGroups.common}/references/tw-keep-english.md) in English.
When the version of the list changes, do the keep-English chore, {keepEnglishChore}: it audits all the twins against the list.

## Tasks

The tasks that continue from one session to a different session are in `{tasksDir}/`.
Their summary table is `{taskSummary}`.
To add or change a task, follow [task-rules.md]({skillGroups.common}/rules/task-rules.md).
After a change, run this command from the root:

```bash
python {skillGroups.common}/scripts/check_tasks.py --summary {taskSummary!q} --tasks-dir {tasksDir!q}
```

## Chores

The work that you must do again each time that a condition occurs is in `chores/`.
Its summary table is `{choreSummary}`.
When you must find or do a chore, read this table first.
A request that gives the name of a skill is not a chore.
To add, change or do a chore, follow [chore-rules.md]({skillGroups.common}/rules/chore-rules.md).
After a change, run this command from the root:

```bash
python {skillGroups.common}/scripts/check_chores.py --summary {choreSummary!q} --chores-dir chores
```

{AGENTS-shared}
