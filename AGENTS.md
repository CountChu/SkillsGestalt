# SkillsGestalt

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-30`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-11-02`  `c612bdfa1ea7`

> This file is in ASD-STE100 Simplified Technical English (STE), Issue 9.
> Technical words: agency, argument, audit, branch, chore, clone, command, commit, computer, day, directory, document, English, entry, file, Forge, git, glob, hash, line, list, message, pattern, publish, repository, root, script, section, session, skill, snapshot, summary, table, tag, template, term, text, twin, user, version.

Instructions for an agent that works in this agency.
A script makes this file from the template `skill-groups/common/templates/AGENTS-tmp.md` and the `AGENTS-local.md` at the root.
The script also makes `CLAUDE.md`, which contains only the line `@AGENTS.md`: Claude Code reads `CLAUDE.md`, and this line gives it all of this file.

Do not change this file or `CLAUDE.md`.
To change a rule for each agency, change the template.
To change a rule for only this agency, change `AGENTS-local.md`.
Then, and after each change to the `config.yaml`, `config-tmp.yaml` or `config.local.yaml` at the root, run this command from the root:

```bash
python skill-groups/common/scripts/gen_config.py
```

If the root has a `config-tmp.yaml`, the command first makes the `config.yaml` from it and from `config.local.yaml`.
Then, do not change the `config.yaml`: change `config-tmp.yaml` for each computer, or `config.local.yaml` for only this computer.

## Skills

When a request starts with `/<name>`, `<name>` is the name of the skill to do, and the subsequent text is the argument of the skill.
For example, in `/check-skill asd-ste 5.6`, the skill is `check-skill`, and `asd-ste 5.6` is its argument.
When a request gives the name of a skill without `/`, do the same.

Each skill is in a skill group.
The `skillGroups` of the `config.yaml` at the root gives the root directory of each skill group:

- `common`: `skill-groups/common`
- `external`: `skill-groups/external`

A skill is in `<root of its skill group>/skills/<name of the skill>/SKILL.md`, for example `skill-groups/common/skills/chinese/SKILL.md`.
These skills are not in the skill list of the agent.
For each root in the list, in sequence, read `<root>/skills/<name of the skill>/SKILL.md` until you find the file.
Do not use a file search, a glob pattern or a text search to find a skill.
If no skill group has this file, tell the user, and stop.
When you find the file, read it, and then do its steps.

Before you change a skill, read its `README.md`, if it has one, and [skill-writing.md](skill-groups/common/rules/skill-writing.md).
Make each change that the section "When the Skill Is Changed" of the `README.md` gives, in the same run.
Then run the checks that the `README.md` gives.
The `SKILL.md` of a skill does not refer to its `README.md`, because a run of the skill must not read the `README.md`.

## Markdown

When you write or change a Markdown file in the repository, follow [md-style.md](skill-groups/common/rules/md-style.md).

## 繁體中文 twins

A Markdown file with a `-tw.md` adjacent to it has a 繁體中文 twin.
Put each change to the English file into the twin in the same run.
Use the [chinese](skill-groups/common/skills/chinese/SKILL.md) skill to change the twin.
It translates only the text that changed after the last commit of the twin, and then it compares the two files.

A twin keeps the terms of [tw-keep-english.md](skill-groups/common/references/tw-keep-english.md) in English.
When the version of the list changes, do the keep-English chore, [keep-english](chores/keep-english.md): it audits all the twins against the list.

## Tasks

The tasks that continue from one session to a different session are in `tasks/`.
Their summary table is `dashboard/task-summary.md`.
To add or change a task, follow [task-rules.md](skill-groups/common/rules/task-rules.md).
After a change, run this command from the root:

```bash
python skill-groups/common/scripts/check_tasks.py --summary dashboard/task-summary.md --tasks-dir tasks
```

## Chores

The work that you must do again each time that a condition occurs is in `chores/`.
Its summary table is `dashboard/chore-summary.md`.
When you must find or do a chore, read this table first.
A request that gives the name of a skill is not a chore.
To add, change or do a chore, follow [chore-rules.md](skill-groups/common/rules/chore-rules.md).
After a change, run this command from the root:

```bash
python skill-groups/common/scripts/check_chores.py --summary dashboard/chore-summary.md --chores-dir chores
```

## Settings of This Agency

The `config.yaml` and the `config.local.yaml` at the root are not in git.
`gen_config.py` makes the `config.yaml` from the template [config-tmp.yaml](config-tmp.yaml) and from `config.local.yaml`.
A change in the `common` skill group can make work for a Forge, or a `FAIL` in a check of a Forge.
For such a change, add an entry to [CHANGES.md](skill-groups/common/CHANGES.md).
Each Forge does the chore [follow-gestalt](chores/follow-gestalt.md) for these entries.

## Branches

Do your work on `m1`.
In a different clone, you can do your work on a different branch.
The local `main` contains only the snapshots that go to GitHub.
Do not commit on it.

The commits before 2026-10-30 are in the tag `archive/master`.
The commits before each subsequent release are in `archive/<branch>-<yymmdd>`, for example `archive/m1-261030`, with one tag for each day.
To find a hash that a document refers to, look in these tags.
To publish, follow the steps of [publish-gestalt](chores/publish-gestalt.md).

## Commits

Do not put a `Co-Authored-By` line in a commit message.
This rule is also true for the snapshots of [publish-gestalt](chores/publish-gestalt.md).
The `.claude/settings.json` at the root stops this line in the commits of Claude Code.
