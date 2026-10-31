# SkillsGestalt

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-30`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-30`  `8cc2e2061175`

> This file is in ASD-STE100 Simplified Technical English (STE), Issue 9.
> Technical words: agency, audit, chore, command, commit, day, document, English, entry, file, Forge, git, hash, list, publish, repository, root, script, session, skill, snapshot, summary, table, tag, template, term, text, twin, version.

Instructions for an agent that works in this agency.
A script makes this file from the template `.github/common/templates/CLAUDE-tmp.md` and the `CLAUDE-local.md` at the root.
Do not change this file.
To change a rule for each agency, change the template.
To change a rule for only this agency, change `CLAUDE-local.md`.
Then, and after each change to the `config.yaml` at the root, run this command from the root:

```bash
python .github/common/scripts/gen_claude_md.py
```

## Markdown

When you write or change a Markdown file in the repository, follow [md-style.md](.github/common/rules/md-style.md).

## 繁體中文 twins

A Markdown file with a `-tw.md` adjacent to it has a 繁體中文 twin.
Put each change to the English file into the twin in the same run.
Use the [chinese](.github/common/skills/chinese/SKILL.md) skill to change the twin.
It translates only the text that changed after the last commit of the twin, and then it compares the two files.

A twin keeps the terms of [tw-keep-english.md](.github/common/references/tw-keep-english.md) in English.
When the version of the list changes, do the keep-English chore, [keep-english](chores/keep-english.md): it audits all the twins against the list.

## Tasks

The tasks that continue from one session to a different session are in `tasks/`.
Their summary table is `dashboard/task-summary.md`.
To add or change a task, follow [task-rules.md](.github/common/rules/task-rules.md).
After a change, run this command from the root:

```bash
python .github/common/scripts/check_tasks.py --summary dashboard/task-summary.md --tasks-dir tasks
```

## Chores

The work that you must do again each time that a condition occurs is in `chores/`.
Its summary table is `dashboard/chore-summary.md`.
Read this table first to find the chore that you must do.
To add, change or do a chore, follow [chore-rules.md](.github/common/rules/chore-rules.md).
After a change, run this command from the root:

```bash
python .github/common/scripts/check_chores.py --summary dashboard/chore-summary.md --chores-dir chores
```

## Settings of This Agency

The `config.yaml` at the root is not in git, and [config.example.yaml](config.example.yaml) is its template.
A change in the `common` skill group can make work for a Forge, or a `FAIL` in a check of a Forge.
For such a change, add an entry to [CHANGES.md](.github/common/CHANGES.md).
Each Forge does the chore [follow-gestalt](chores/follow-gestalt.md) for these entries.

## Branches

Do your work on `m1`.
The local `main` contains only the snapshots that go to GitHub.
Do not commit on it.

The commits before 2026-10-30 are in the tag `archive/master`.
The commits before each subsequent release are in `archive/m1-<yymmdd>`, with one tag for each day.
To find a hash that a document refers to, look in these tags.
To publish, follow the steps of [publish-github](chores/publish-github.md).
