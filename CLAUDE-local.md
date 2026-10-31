> Technical words: branch, clone, day, document, entry, Forge, git, hash, publish, snapshot, tag.

## Settings of This Agency

The `config.yaml` at the root is not in git, and [config.example.yaml](config.example.yaml) is its template.
A change in the `common` skill group can make work for a Forge, or a `FAIL` in a check of a Forge.
For such a change, add an entry to [CHANGES.md](.github/common/CHANGES.md).
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
