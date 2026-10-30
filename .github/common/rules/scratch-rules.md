# Scratch File Rules

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-18`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-30`  `8cc2e2061175`

> This file is in ASD-STE100 Simplified Technical English (STE), Issue 9.
> Technical words: app, checkpoint, command, commit, design document, directory, file, git, noise, path, root, scratch, script, skill, stage, untracked file, wildcard, workspace.

These rules tell where a run puts its scratch files, and how to remove these files.

- **Put each scratch file in `temp\` at the root of the workspace.**
  Do not put it directly in the root of the workspace.
  Do not put it adjacent to the source that it examines.
  If the directory is not there, create it.
  The directory is in `.gitignore`, thus no file in it goes into a commit.
- **Scratch is each item that a run writes and that is not one of the outputs that its skill identifies.**
  Examples are a temporary script that does a test or a check, and the output of a command that the run keeps.
  Other examples are a JSON file that the run uses before it writes its outputs, and a temporary copy of a directory for a test.
  The MD report, the YAML checkpoint, a `database\` file and the directory of an app are outputs, not scratch.
  Each of these outputs has its own path.
- **Start the name of a scratch file with the name of the skill that made it**, as in `temp\{skill-name}-{what-it-does}.py`.
  If you do not do this, two runs of different skills can use the same usual name.
  Then the second run replaces the file of the first run, and does not tell you.
- **Remove the scratch files that the run created, and give the full name of each file.**
  Do not use a wildcard.
  You can think that `Remove-Item temp\_s*.py` removes only your files, but it removes all the files that agree with the wildcard.
  These files can include files that a different run uses at that time.
  Also, `Remove-Item` does **not** use the Recycle Bin, thus it removes an untracked file permanently.
  Do not remove the `temp\` directory.
- **Scratch that stays after a run is not an error.**
  A run that stops before it completes its work can keep files in `temp\`, because they show how much of the work it did.
  Each item in `temp\` is safe to remove manually, when you want.
  This is the most important cause to keep all scratch in one location.

**The root of the workspace is not a correct location for scratch files.**
A file that a run writes there is an untracked file, *but git does not ignore it*.
Thus, it shows as noise in `git status`.
Also, if you use `git clean -fd` after a commit, it removes the file, and does not get your approval first.
At the same time, `git clean -fd` removes all the files of the other runs that are adjacent to it.

**The `temp\` directory of an app is a different directory.**
An app can have a `temp\` directory for the data that one of its stages gives to the next stage.
This directory is a part of the app.
The design document of the app tells about it.
These rules do not apply to it.
These rules apply only to the `temp\` directory at the root of the workspace.

**Also, `__pycache__` is not scratch.**
When you operate a script in its directory, Python makes `__pycache__` as a side effect.
Also, git ignores it.
The removal of `__pycache__` is optional, and it is not a part of the procedure that removes scratch.
