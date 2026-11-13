> Technical words: branch, clone, commit, day, document, entry, Forge, git, hash, line, message, publish, snapshot, tag.

## Settings of This Agency

A change in the `common` skill group can make work for a Forge, or a `FAIL` in a check of a Forge.
For such a change, add an entry to [CHANGES.md](skill-groups/common/CHANGES.md).
Each Forge does the chore [follow-gestalt](chores/follow-gestalt.md) for these entries.

## Branches

The local `main` contains only the snapshots that go to GitHub.
Do not commit on it.

The commits before 2026-10-30 are in the tag `archive/master`.
The commits before each subsequent release are in `archive/<branch>-<yymmdd>`, for example `archive/m1-261030`.
A day can have more than one release or pull.
Then more tags keep the commits of that day, for example `archive/devbox-261113-1` and `archive/devbox-261113-pull`.
To find a hash that a document refers to, look in all these tags.

To publish, follow the steps of [publish-gestalt](chores/publish-gestalt.md).
A snapshot of [publish-gestalt](chores/publish-gestalt.md) also has no `Co-Authored-By` line.
