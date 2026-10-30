---
name: {SKILL_NAME}
description: {SKILL_DESCRIPTION}
---

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-19`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-30`  `8cc2e2061175`

> This file is in ASD-STE100 Simplified Technical English (STE), Issue 9.
> Technical words: API, argument, bearer token, call, canonical skill invocation, checkpoint, column, command, configuration, configuration file, credential, data file, definition, development, directory, field, file, folder, forward slash, glossary, header, inline code, key, line, link, link target, list, map, MD report, output directory, parse, parser, PAT, path, plain text, process, project, raw data, registry, root, save, scope, scratch file, script, section, selector, separator, session, shell, skill, table, term, terminal, user, vault, wiki, workflow, workspace, writer step.

# TERMINOLOGY

Each skill uses these terms with the same definition.
Remove each term that this skill does not use.
If the glossary gives a term that the skill does not use, the definition of the term can become incorrect when the skill changes.

- **`run step N`** — a selector at the end of a prompt, which identifies one step.
- **Checkpoint Dir** — the directory for one run, which holds the YAML checkpoint of a skill.
  Each skill has its own Checkpoint Dir.
  **CONFIGURATION** gives the Checkpoint Dir of this skill.
- **YAML checkpoint** — the `process.yaml` in the Checkpoint Dir.
  Each step writes its outputs there, in a `step_{N}` group.
  Thus, a subsequent step reads these outputs, and does not calculate them again.
- **MD report** — the Markdown report that a skill writes into the wiki vault, in a folder that has the name of that skill.
  It has the standard header (Skill, Checkpoint, Created, Updated, Prompt) above its sections of results.

# DEDICATED TERMINOLOGY

The terms that only this skill uses.

- **{TERM_1}** — {TERM_1_DEFINITION}
- **{TERM_2}** — {TERM_2_DEFINITION}

# CONFIGURATION

The values that this skill uses in a run.
Remove the line for each output that this skill does not make.

- **Checkpoint Dir** — `checkpoints\{SKILL_NAME}\{CHECKPOINT_DIR_NAME}\`.
- **MD report** — `{wikiDir}\{SKILL_NAME}\{REPORT_FILENAME}.md`.
  `wikiDir` comes from the [config.yaml](config.yaml) of the workspace, and Step 0 finds its value.
  Do not hard-code the root of the wiki.

# MUST FOLLOW

- Run the workflow one step at a time, and show the number of each step.
- **Honor a `run step N` selector**: run Step N, and then stop.
  Read the output of each previous step from the YAML checkpoint.
  Do not run a subsequent step.
- Obey [report-md-rules.md](.github/common/rules/report-md-rules.md) for the header and the shape of the MD report.
- Obey [report-yaml-rules.md](.github/common/rules/report-yaml-rules.md) for the shape of the YAML checkpoint and for its necessary fields.
- Obey [scratch-rules.md](.github/common/rules/scratch-rules.md) for the location of each scratch file of a run, and for how to remove it.
- **Each JSON file in the Checkpoint Dir has one writer step only.**
  The step that makes a data file writes the full file, and only that step changes it.
  A subsequent step that makes a decision writes it into its own `step_{N}.json`, adjacent to that file.
  It does not add, change or remove a key in a file that a different step wrote.
  This rule applies also when the decision of the subsequent step replaces the data in that file.
  The YAML checkpoint is the one exception: each step adds its `step_{N}` group at the end, and does not write the full file again.
- If more than one step writes into a data file, the first step erases the data of the other steps when it runs again.
  For example, a repair to the parser or a `run step 1` writes the full file again.
  This erases the results of all the subsequent steps, and no message tells you.
- **Before the skill stops, show the paths of the MD report and of the YAML checkpoint.**
  Show only the two paths, and do not show their contents.
  Write the two paths as Markdown links that open with a click.
  Do not write them as inline code or as plain text.
  - For the **MD report**, use a link with an `obsidian://open?vault={vaultName}&file=<vault-relative-path>` URI.
    The vault is not in this workspace, thus a link target that starts at the workspace cannot find it.
    For example: `[{REPORT_FILENAME}.md](obsidian://open?vault={vaultName}&file={SKILL_NAME}/{REPORT_FILENAME}.md)`.
  - For the **YAML checkpoint**, use a link target that starts at the workspace.
    Use the forward slash as the separator in it.
    For example: `[process.yaml](checkpoints/{SKILL_NAME}/{CHECKPOINT_DIR_NAME}/process.yaml)`.
  - Do this for each run, and also for a run of only one step, for example `run step 0`.

# Prompt Examples


## Prompt 1

```
/{SKILL_NAME}
```

## Prompt 2

```
/{SKILL_NAME}
run step 0
```

## Prompt 3

```
{NATURAL_LANGUAGE_PROMPT}
```


# Workflow

## Step 0 - Warmup

- Run `.venv` first.

- Read [config.yaml](config.yaml), the configuration file at the root of the workspace, and find these values:
  - **`wikiDir`**: the root of the MD reports.
    The reports of this skill go into `{wikiDir}\{SKILL_NAME}\`.
  - **`vaultName`**: the last part of the path of `wikiDir`, for example `MyVault`.
    It is the name of the Obsidian vault, and the `obsidian://` links use it.
  - **`skillGroups`**: the map from the name of a group to the root of its skills.
    The directory of this skill is `{skillGroups.{SKILL_GROUP}}\skills\{SKILL_NAME}\`.
  - Replace each `{wikiDir}`, `{vaultName}` and `{skillGroups.{SKILL_GROUP}}` in the steps that follow with the value that you found.
    Do this also in the commands.
  - If `config.yaml` is missing, or if a necessary key is not in it, stop, and tell the user to supply it.

- Get the PAT with `[Environment]::GetEnvironmentVariable('ADO_PAT','User')`.
  This gives the **User-scope** value, and not the `$env:ADO_PAT` of the session.
  If the user sets `$env:ADO_PAT` in a terminal of the user, the value is local to that process.
  The terminal in which this skill runs does **not** see that value.
  But each shell reads the current value of the User scope directly from the registry.
  Put the value into the session, thus the scripts of the steps get it, because they read `os.getenv("ADO_PAT")`:

  ```powershell
  $env:ADO_PAT = [Environment]::GetEnvironmentVariable('ADO_PAT','User')
  ```

- Make sure that the `ADO_PAT` is not empty, and that it **operates correctly**.
  To do this, call an ADO API, for example the API that gives the list of the projects.
  If the PAT is empty, or if the call gives an error (for example, `401 Unauthorized`), **STOP the skill immediately**.
  Tell the user that you cannot use `ADO_PAT`.
  Then tell the user to save a new PAT in the User scope (`[Environment]::SetEnvironmentVariable('ADO_PAT','<new-pat>','User')`) before the skill runs again.
  Do not use a different credential as an alternative, for example an Azure CLI or `ADO_BEARER` bearer token.

- Before you run the workflow, make sure that the scripts and files that follow are there.
  Write only the files that the development of the skill added to the directory of the skill.
  These files are in the directory of the skill, adjacent to this `SKILL.md`.
  - `{skillGroups.{SKILL_GROUP}}\skills\{SKILL_NAME}\scripts\{SCRIPT_PATH_1}`

- The prompt agrees with one of the examples in **Prompt Examples**.
  Parse it, and find these items:
  - {INPUT_1}
  - {INPUT_2}

- If a necessary input is missing, tell the user to supply it.

- Save the canonical skill invocation, thus the subsequent steps can refer to it.

- Save `step_0` of the YAML checkpoint, with the parsed inputs.
  In this step, it is not necessary to create the MD report file, because the run possibly has no important results at this time.


## Step 1 - {STEP_1_TITLE}

- Run the script `{SCRIPT_PATH_1}` with the `{STEP_1_ARG_1}` and `{STEP_1_ARG_2}` arguments.
  - `{STEP_1_ARG_3}`: the checkpoint directory of this run.
  - Example: `python {skillGroups.{SKILL_GROUP}}\skills\{SKILL_NAME}\scripts\{SCRIPT_PATH_1} {STEP_1_ARG_1} {STEP_1_ARG_1_VALUE} {STEP_1_ARG_3} "checkpoints\{SKILL_NAME}\{CHECKPOINT_DIR_NAME}"`

- The script:
  1. {SCRIPT_1_ACTION_1}
  2. {SCRIPT_1_ACTION_2}
  3. Saves the results as `{STEP_1_OUTPUT}` in the output directory.
     All the steps of the run use this file of raw data, and it is not the same file as `process.yaml`.

- Save `step_1` of the YAML checkpoint, with: {STEP_1_CHECKPOINT_FIELDS}.

- Save the MD report file.
  Add a **{STEP_1_SECTION}** section at the end of the file, and show it:
  - **{STEP_1_TABLE} table** with rows:
    - **{ROW_1}**
    - **{ROW_2}**: {ROW_2_RENDER_RULE}


## Step 2 - {STEP_2_TITLE}

- Read the `{STEP_1_OUTPUT}` data file that Step 1 saved at `checkpoints\{SKILL_NAME}\{CHECKPOINT_DIR_NAME}\{STEP_1_OUTPUT}`.
  Use {STEP_2_INPUT_KEY} as the input.

- These rules apply to each instruction that follows:
  - {STEP_2_RULE_1}
  - {STEP_2_RULE_2}
  - Make each decision only from the data that you read.
    Do not supply a value that is not in the data.
    If you cannot make a decision about {STEP_2_AMBIGUOUS_CASE} from the data, record it as `unknown`.
    Then give the cause, and do not use an estimate.

- For each {STEP_2_ITEM}:
  1. {STEP_2_INSTRUCTION_1}
  2. {STEP_2_INSTRUCTION_2}
  3. {STEP_2_INSTRUCTION_3}

- Write the results into `step_2.json` in the Checkpoint Dir, as `{STEP_2_OUTPUT_KEY}`.
  Do not write them into `{STEP_1_OUTPUT}`, because that file is the file of Step 1.

- Save `step_2` of the YAML checkpoint, with: {STEP_2_CHECKPOINT_FIELDS}.

- Save the MD report file.
  Add a **{STEP_2_SECTION}** section at the end of the file, and show it:
  - **Summary line**: {STEP_2_SUMMARY}.
  - **{STEP_2_TABLE} table** with columns:
    - **{COLUMN_1}**
    - **{COLUMN_2}**: {COLUMN_2_RENDER_RULE}
  - **Notes**: {STEP_2_NOTES}
