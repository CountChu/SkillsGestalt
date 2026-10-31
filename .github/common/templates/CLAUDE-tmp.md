# {agencyName}

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-30`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-30`  `8cc2e2061175`

> This file is in ASD-STE100 Simplified Technical English (STE), Issue 9.
> Technical words: agency, audit, chore, command, commit, English, file, list, repository, root, script, session, skill, summary, table, template, term, text, twin, version.

Instructions for an agent that works in this agency.
A script makes this file from the template `{skillGroups.common}/templates/CLAUDE-tmp.md` and the `CLAUDE-local.md` at the root.
Do not change this file.
To change a rule for each agency, change the template.
To change a rule for only this agency, change `CLAUDE-local.md`.
Then, and after each change to the `config.yaml` at the root, run this command from the root:

```bash
python {skillGroups.common}/scripts/gen_claude_md.py
```

{CLAUDE-local-top}

## Markdown

When you write or change a Markdown file in the repository, follow [md-style.md]({skillGroups.common}/rules/md-style.md).

## 繁體中文 twins

A Markdown file with a `-tw.md` adjacent to it has a 繁體中文 twin.
Put each change to the English file into the twin in the same run.
Use the [chinese]({skillGroups.common}/skills/chinese/SKILL.md) skill to change the twin.
It translates only the text that changed after the last commit of the twin, and then it compares the two files.

A twin keeps the terms of [tw-keep-english.md]({skillGroups.common}/references/tw-keep-english.md) in English.
When the version of the list changes, do the keep-English chore, {keepEnglishChore}: it audits all the twins against the list.

## Tasks

The tasks that continue from one session to a different session are in `tasks/`.
Their summary table is `dashboard/task-summary.md`.
To add or change a task, follow [task-rules.md]({skillGroups.common}/rules/task-rules.md).
After a change, run this command from the root:

```bash
python {skillGroups.common}/scripts/check_tasks.py --summary dashboard/task-summary.md --tasks-dir tasks
```

## Chores

The work that you must do again each time that a condition occurs is in `chores/`.
Its summary table is `dashboard/chore-summary.md`.
Read this table first to find the chore that you must do.
To add, change or do a chore, follow [chore-rules.md]({skillGroups.common}/rules/chore-rules.md).
After a change, run this command from the root:

```bash
python {skillGroups.common}/scripts/check_chores.py --summary dashboard/chore-summary.md --chores-dir chores
```

{CLAUDE-local}
