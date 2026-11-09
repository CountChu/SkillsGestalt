---
name: gen-skill
description: Creates a new skill from the SKILL and README templates, step by step - it parses the skill name and description from the prompt, asks which outputs the new skill produces, which Working Dir it uses and whether it gets 繁體中文 twins, copies the SKILL template into the chosen skillGroups root and generates the workflow by replacing every placeholder, and creates a placeholder for any script or reference file that workflow needs. It then writes the skill's README.md from the README template - the Dataflow, the Purpose of each step, the files each step uses, what changes together, and the files its header quote declares, whose fingerprints depends_on.py records. An existing skill of the same name is overwritten only once the user confirms. When the user asked for twins, it has the chinese skill write SKILL-tw.md and README-tw.md rather than translating anything itself.
---

# TERMINOLOGY

Terms that mean the same thing in every skill.

- **Run Number** — the number of one run, `{yymmdd}.{N}`.
  `{N}` is the sequence number of the run of this skill on that date, and it starts at 1.
- **Working Dir** — the per-run directory that holds all the working data of a run: its step files, its data files and its temporary files.
  It is the Temp Dir or the Checkpoint Dir, and the CONFIGURATION of a skill gives which one.
- **Temp Dir** — a Working Dir at `temp\<skill-name>\{yymmdd}.{N}\`, under the workspace root.
- **Checkpoint Dir** — a Working Dir at `checkpoints\<skill-name>\{yymmdd}.{N}\`, under the workspace root.
- **Step file** — the `step_{N}.yaml` inside the Working Dir.
  Every step writes its outputs to its own step file, so a later step reads them back instead of recomputing them.
- **Run record** — `database\skill-runs\<skill-name>\{yymmdd}.{N}.yaml`, the time and the model of each step of one run; every skill writes one.
- **MD report** — the Markdown report a skill writes into the wiki vault, in a folder named after that skill, carrying the standard header (Skill, Run record, Created, Updated, Prompt) above its result sections.

# DEDICATED TERMINOLOGY

Terms specific to this skill's domain.

- **SKILL template** — the template file Step 2 copies into the new skill's `SKILL.md`.
  Its placeholders are what Step 3 replaces, so its shape is the shape every generated `SKILL.md` starts from.
- **README template** — the template file Step 5 copies into the new skill's `README.md`: the part of a skill that a run does not need, and a change does.
  Its placeholders are what Step 5 replaces.
- **placeholder** — a `{PLACEHOLDER}` token in either template standing where a real value goes: capital letters, digits and underscores between braces.
  A run is not finished while one survives, inside backticks or not; the name `{PLACEHOLDER}` itself only ever talks about placeholders and is never one, and lowercase braces such as `{skillGroups.common}` are values resolved at run time.
- **Skill group** — the `skillGroups` key whose root the new skill is written under.
- **new skill directory** — the directory this skill creates and fills: the new skill's `SKILL.md`, its `README.md`, and any supporting file beside them.
  It is this skill's only output.
- **TW twins** — the `SKILL-tw.md` and `README-tw.md` that Step 6 has the `chinese` skill write beside the generated `SKILL.md` and `README.md`.
  They are optional: Step 1 asks for them, and most skills do without.
- **Dependency Checker** — the shared `depends_on.py`: it reads the header quote of a file, fingerprints the files it declares, and records each date and fingerprint.

# CONFIGURATION

Concrete values this skill runs with.

The inputs and tools, which the run reads or runs:

- **Workspace configuration** — the [config.yaml](config.yaml) at the root of the workspace.
- **SKILL template** — `{skillGroups.common}\templates\SKILL-tmp.md`.
- **README template** — `{skillGroups.common}\templates\README-tmp.md`.
- **Dependency Checker** — `{skillGroups.common}\scripts\depends_on.py`.
- **DFD notation** — `{skillGroups.common}\references\DFD.md`.
- **skill-writing rules** — `{skillGroups.common}\rules\skill-writing.md`.
- **run data rules** — `{skillGroups.common}\rules\run-data-rules.md`.
- **chinese skill** — `{skillGroups.common}\skills\chinese\SKILL.md`.

The last outputs, which a person, a different skill or a subsequent analysis reads:

- **Run record** — `database\skill-runs\gen-skill\{yymmdd}.{N}.yaml`.
- **new skill directory** — `{skillGroups[<group>]}\skills\<skill-name>\`, where `<group>` is the **Skill group** chosen in Step 0.
- **TW twins** — `SKILL-tw.md` and `README-tw.md`, in the **new skill directory**.

# MUST FOLLOW

- Must run workflow step by step, and display each step number.
- **This skill has no `run step N` selector — every run is a whole run.**
  Every step feeds the next and none of them is expensive, so there is nothing worth resuming into.
  Never invent a step selector for it.
- **This skill produces neither an MD report nor step files.**
  Its output is the **new skill directory**: the `SKILL.md` Step 2 copies and Step 3 fills in, any `scripts\` or `references\` placeholder file Step 4 creates, the `README.md` Step 5 writes, and the **TW twins** when the user asked for them in Step 1.
  Beside it, every run writes its own **Run record**.
- Obey [run-data-rules.md](skill-groups/common/rules/run-data-rules.md) for the Run Number, the run record and the Working Dir of a run.
  A run that stops before its last step writes `result: stopped` and `stopped_at` in the run record, as it tells.
- **Before the skill ends, display the path of the run record** — the path only, never its contents, rendered as a clickable Markdown link and never as inline code or plain text.
  Use a link target that starts at the workspace, with the forward slash as the separator: `[{yymmdd}.{N}.yaml](database/skill-runs/gen-skill/{yymmdd}.{N}.yaml)`.
- **The generated `SKILL.md` never links to its `README.md`.**
  A skill loads its whole `SKILL.md` each time it runs, and a link would lead a run into a file that holds nothing a run needs.
- **The new skill's `SKILL.md` and `README.md` carry none of a template's STE marks.**
  A template in ASD-STE100 Simplified Technical English declares `[[ASD-STE100_ISSUE9.pdf]]` and `[[ste-custom]]` in its header quote, and has a header note that says it is in STE and lists its Technical words.
  Step 2 and Step 5 drop those two header-quote lines and the whole header note from the copy: what this skill writes into the new files is never checked as STE, so the marks would claim a check that nobody made.
- **Never write the date or the fingerprint in a header quote by hand.**
  The **Dependency Checker** writes them in Step 5, once the `README.md` it vouches for is written; a fingerprint typed in vouches for a reading nobody made.
- **Never write the TW twins by hand.**
  Step 6 delegates to the `chinese` skill, and that skill's parity check is what proves each twin kept its source's headings, fences, tables, links and placeholders.
  A twin written here would skip that check.

# Prompt Examples


## Prompt 1

```
/gen-skill
compare-builds
Compare two pipeline builds and report differences.
```

## Prompt 2

```
/gen-skill
Compare two pipeline builds and report differences.
example:
/compare-builds
https://dev.azure.com/contoso/Firmware/_build/results?buildId=1234567&view=results
https://dev.azure.com/contoso/Firmware/_build/results?buildId=1234500&view=results
```


# Workflow

## Step 0 - Warmup

- Read the workspace config [config.yaml](config.yaml) at the workspace root and resolve:
  - **`skillGroups`**: the group name -> skills-root path map (e.g. `common` / `dedi` / `external`).
    Every skills root used below is `{skillGroups[<group>]}\skills\`, and both templates are under `{skillGroups.common}\templates\`.
    Never hardcode `skill-groups\...`.
  - **`wikiDir`**: the wiki root used for the new skill's MD report directory (Step 1).
- If `config.yaml` is missing or a needed key is absent, stop and ask the user.

- Check if the below files exist before running workflow, and stop, naming the missing one, if one does not.
  - the **SKILL template** and the **README template**.
  - `{skillGroups.common}\references\DFD.md` — the notation Step 5 draws the Dataflow in.
  - `{skillGroups.common}\rules\skill-writing.md` — the rules Steps 3 and 5 write by.
  - the **Dependency Checker**.

- The prompt takes one of the forms shown in **Prompt Examples** above.
  Parse it as:
  - **Prompt 1**:
    - **Skill name** = line 2 (e.g. `compare-builds`).
    - **Skill description** = line 3.
  - **Prompt 2**:
    - **Skill description** = line 2.
    - **Skill name** = the slash-command name on the first line after `example:` (e.g. `/compare-builds` becomes `compare-builds`).
    - Treat the remaining example lines as conversation context for inferring the workflow steps, not as gen-skill inputs.

- If the skill name or description cannot be parsed from these forms, ask the user for it.
  Ignore any other prompt shape.

- These are not parsed from the prompt:
  - **Skill group**: one of the `skillGroups` keys, chosen by what the skill is.
    A skill that is generic and project-agnostic goes to `common`; a skill that only makes sense inside one project goes to that project's group.
    Never choose `external` — that root is reserved for imported third-party skills.
    - No registration step is needed: every `skillGroups` root is already listed under `chat.agentSkillsLocations` in the workspace file.
      VS Code scans each root only one level deep (`<root>/<dir>/SKILL.md`), so a newly introduced group folder must be added there as its own entry (relative path, forward slashes, no globs) — and to `skillGroups` in `config.yaml` — before any of its skills are discovered.
  - **Workflow steps**: infer them from the conversation context above the prompt.

- Check if a skill with the same name already exists under any `skillGroups` root (`{skillGroups[<group>]}\skills\<skill-name>\`).
  If it does, warn the user and ask whether to overwrite.

- Keep the canonical skill invocation, for the `prompt` of the run record.

- Get the Run Number, as run-data-rules.md tells, and write the run record of the run.
  Add this step to the run record.


## Step 1 - Ask which output files the skill produces

- Ask the user which of these the new skill produces, and accept `both`, `md`, `steps`, or `none`:
  - an **MD report** under `{wikiDir}\<skill-name>\`.
  - **step files** in its **Working Dir**.
  Every skill writes a **run record**, so it is not asked.

- If an MD report is produced, ask for its filename pattern (e.g. `run-pr-{prId}-{yymmdd}`).

- Ask which **Working Dir** the new skill uses, and accept `temp`, `checkpoints`, or `none`:
  - `temp` → the **Temp Dir**, `temp\<skill-name>\{yymmdd}.{N}\`.
  - `checkpoints` → the **Checkpoint Dir**, `checkpoints\<skill-name>\{yymmdd}.{N}\`.
  - `none` → the skill writes no working data: no step file, no data file and no temporary file.
  A run never uses both, so its step files, its data files and its temporary files all go into the one chosen here.
  Accept `none` only when the skill produces no step files and writes no data file and no temporary file; otherwise ask again.

- Ask whether the new skill also gets **TW twins**, and accept `yes` or `no`.
  Default to `no` — a twin doubles what every later edit has to touch, since a section changed on one side must be changed on the other in the same run.
  It is asked here, with the outputs, because the answer shapes the `README.md` as well: a skill with twins lists them among what changes together, and declares the `chinese` skill it depends on.

- Add this step to the run record.


## Step 2 - Copy Template

- Copy the **SKILL template** to the **new skill directory**'s `SKILL.md`, and display the destination path.

- Add this step to the run record.


## Step 3 - Build SKILL.md

- Write by [skill-writing.md](skill-groups/common/rules/skill-writing.md): each step self-contained, a step a program can do deterministically running a script, and nothing in `SKILL.md` that a run does not need — no Dataflow and no Purpose, which go into the `README.md` in Step 5, and no link to that `README.md`.

- Replace every **placeholder** throughout the copied file:
  - `{SKILL_NAME}` → the skill name parsed in Step 0.
  - `{SKILL_DESCRIPTION}` → the skill description parsed in Step 0.
  - `{SKILL_GROUP}` → the **Skill group** chosen in Step 0.
  - `{NATURAL_LANGUAGE_PROMPT}` → a realistic natural-language example prompt.
  - `{REPORT_FILENAME}` → the MD report filename pattern from Step 1.
  - `{WORKING_DIR}` → the Working Dir Step 1 chose, with the new skill's name and without the last backslash: `temp\<skill-name>\{yymmdd}.{N}` or `checkpoints\<skill-name>\{yymmdd}.{N}`.
    With `none`, the step that uses it is written without it.

- Edit the MUST FOLLOW section according to the Step 1 answer:
  - No MD report → remove the report-md-rules and MD report lines.
  - In CONFIGURATION, list under "The inputs and tools" each file the skill reads, each script it runs and each other program it uses, such as a template, a reference or another skill; nothing the skill writes goes there.
  - In CONFIGURATION, remove the Handoff file line if no other skill reads its output.
  - In CONFIGURATION, keep only the Working Dir line of the Step 1 answer, the Temp Dir line or the Checkpoint Dir line, and remove the other; with `none`, remove both.
    Add after the kept path what the skill puts in it; a step that runs a script which writes temporary files gives the script the Run Number.
  - In TERMINOLOGY, keep the Working Dir term and the term of the one kind Step 1 chose, and remove the other kind.
    In the Working Dir term, change "It is the Temp Dir or the Checkpoint Dir, and **CONFIGURATION** gives which one." to name the chosen kind, for example "In this skill, it is the Checkpoint Dir, and **CONFIGURATION** gives it."
    With `none`, remove all three and the Step file term.
  - After CONFIGURATION, call the directory the Working Dir, never the Temp Dir or the Checkpoint Dir, and name a file in it as `step_3.yaml` in the Working Dir rather than by its full path.
  - No Working Dir → remove the one-writer-per-file item with the item after it, which gives its reason — without a Working Dir they govern nothing.
  - Keep the run-data-rules line and the display-the-paths line in every skill, because every skill writes a run record; without an MD report, the paths line shows only the run record.

- Edit Step 0 - Warmup:
  - Remove the `.venv` line if the skill does not need a virtual environment.
  - In the `config.yaml` bullet, keep only the keys the skill actually needs (drop `wikiDir` when Step 1 said no MD report).
  - Remove the `ADO_PAT` resolution and validation bullets if the skill does not call Azure DevOps.
  - Remove the scripts/files check section, or list the skill's scripts in place of `{SCRIPT_PATH_1}`.
  - Replace `{INPUT_1}` / `{INPUT_2}` with the inputs the skill parses from its prompt.
  - Remove the `step_0.yaml` line if Step 1 said no step files; keep the Run Number and run record lines.

- Replace the `{STEP_N_TITLE}` placeholder sections — and every placeholder inside them, including the ones not named `{STEP_N_*}` (e.g. `{SCRIPT_1_ACTION_1}`, `{ROW_1}`, `{COLUMN_1}`) — with the workflow steps inferred in Step 0.
  Add or remove step sections as needed, and drop each section's `Save step_N.yaml` / `Save MD report file` line for any output the skill does not produce; keep each `Add this step to the run record` line.

- Leave no **placeholder** behind — before finishing, scan the file for a capital letter right after `{`; only `{PLACEHOLDER}` may remain.

- Display the generated SKILL.md content.

- Add this step to the run record.


## Step 4 - Create supporting files

- If any step written in Step 3 runs a script, create a placeholder script file for it under the **new skill directory**'s `scripts\`.
- If any step written in Step 3 needs a reference template, create a placeholder file for it under the **new skill directory**'s `references\`.
- Display the list of created files.

- Add this step to the run record.


## Step 5 - Build README.md

- Copy the **README template** to the **new skill directory**'s `README.md`, and fill it from the `SKILL.md` Step 3 wrote, the files Step 4 created and the Step 1 answers, by [skill-writing.md](skill-groups/common/rules/skill-writing.md).
  Every step it names is named exactly as its heading in `SKILL.md`, number included.

- Replace the placeholders of the head:
  - `{SKILL_NAME}` → the skill name parsed in Step 0.
  - `{SKILL_DIR}` → the **new skill directory**, workspace-relative, with forward slashes.
  - `{COMMON_DIR}` → `{skillGroups.common}`, workspace-relative, with forward slashes.
  - `{COMMON_PATH}` → the path from the **new skill directory** to `{skillGroups.common}`, relative, with forward slashes — `../..` for a skill in the `common` group.
  - `{MORE_PATH_ABBREVIATIONS}` → one line for each further short name the diagrams use, such as the file a run works on or the Working Dir, or nothing when there is none.

- Keep the header quote lines that apply to the new skill, and remove the rest:
  - Always: `DFD.md`, `md-style.md`, `skill-writing.md`, `run-data-rules.md`, `SKILL-tmp.md` and `README-tmp.md`.
  - `report-md-rules.md` when it writes an MD report.
  - `chinese/SKILL.md` when Step 1's answer asked for **TW twins**.
  - Add a line for every other file outside the **new skill directory** that a step reads or runs, such as a shared script — a path link relative to the `README.md`, as the template's lines are.

- **Dataflow**: redraw the template's diagram so that it draws this skill rather than the template's example, in the notation of [DFD.md](skill-groups/common/references/DFD.md): every step a rounded box named exactly as its heading, and every input a step reads and every record it writes — the prompt, `config.yaml`, each document read, each data file in the Working Dir, and each step's own step file and section of the MD report.
  Drop what Step 1 said the skill does not produce, number the blue arrows in `linkStyle` anew, and bring the legend beneath it in line with what the diagram now draws.

- **Step Purposes**: one item for each step, its heading on the first line and its Purpose indented beneath — one sentence saying why the step exists as a step, what the skill would lose by folding it into its neighbour, and never a summary of what the step does.

- **Files Each Step Uses**: answer the scripted-versus-not rule once, in the bold sentence, saying which steps run a script, which do not, and why.
  Then, in the fenced tree, list under each step what it reads, checks, runs — with what that script reads and writes beneath it — and writes.

- **When the Skill Is Changed**: list in the fenced tree the files that change together with `SKILL.md` (`⇄`) and the rules it follows (`─▶`): its scripts and references, with what each step says of them; the twin lines only when Step 1's answer asked for **TW twins**; the rule lines that match the header quote kept above.
  Under `outputs already written`, name what earlier runs leave behind that a change to the skill can leave in an old shape, or remove that branch when there is none.
  Replace `{SKILL_REGRESSION_CHECK}` with a run that proves the skill still works after a change, or remove that line.

- **Tracked Dependencies**: list in the fenced tree every file the header quote declares, in the same order.

- Leave no **placeholder** behind — before finishing, scan the file for a capital letter right after `{`; only `{PLACEHOLDER}` may remain.

- Record the header quote with the **Dependency Checker**, which writes the date and the fingerprint after each line:
  - Example: `python {skillGroups.common}\scripts\depends_on.py record "{skillGroups[<group>]}\skills\<skill-name>\README.md"`
  - It exits `2` when a line names no file: correct that link, and record again.

- Display the `README.md` path as a clickable Markdown link.

- Add this step to the run record.


## Step 6 - Create the TW twins

- If Step 1's answer was `no`, say that no twin was written, and go on to the last two items of this step.

- If it was `yes`, run the `chinese` skill against the **new skill directory**'s `SKILL.md`, then against its `README.md`, handing it each path — e.g. `/chinese {skillGroups[<group>]}\skills\<skill-name>\SKILL.md`.
  Each run writes one of the **TW twins** beside its source, keeps every heading, inline-code span, link target and placeholder token in English — the `README.md`'s header quote among them — and ends with its own parity check; the run on `SKILL.md` also adds the pairing line under the twin's frontmatter.

- Do not translate either file here, and do not edit the generated `SKILL.md` or `README.md` while doing it — the `chinese` skill treats its source as read-only.

- Display the paths of the **TW twins** as clickable Markdown links.

- Add this step to the run record, and write `result: completed`, because it is the last step.

- Close with the path of the run record, as a clickable Markdown link.
