---
name: gen-skill
description: Creates a new skill from the SKILL and README templates, step by step - it parses the skill name and description from the prompt, asks which outputs the new skill produces and whether it gets 繁體中文 twins, copies the SKILL template into the chosen skillGroups root and generates the workflow by replacing every placeholder, and creates a placeholder for any script or reference file that workflow needs. It then writes the skill's README.md from the README template - the Dataflow, the Purpose of each step, the files each step uses, what changes together, and the files its header quote declares, whose fingerprints depends_on.py records. An existing skill of the same name is overwritten only once the user confirms. When the user asked for twins, it has the chinese skill write SKILL-tw.md and README-tw.md rather than translating anything itself.
---

# TERMINOLOGY

Terms that mean the same thing in every skill.

- **Checkpoint Dir** — the per-run directory holding a skill's YAML checkpoint.
  Every skill has its own.
- **YAML checkpoint** — the `process.yaml` inside the Checkpoint Dir.
  Every step writes its outputs there under a `step_{N}` group, so a later step reads them back instead of recomputing them.
- **MD report** — the Markdown report a skill writes into the wiki vault, in a folder named after that skill, carrying the standard header (Skill, Checkpoint, Created, Updated, Prompt) above its result sections.

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

- **SKILL template** — `{skillGroups.common}\templates\SKILL-tmp.md`.
- **README template** — `{skillGroups.common}\templates\README-tmp.md`.
- **new skill directory** — `{skillGroups[<group>]}\skills\<skill-name>\`, where `<group>` is the **Skill group** chosen in Step 0.
- **TW twins** — `SKILL-tw.md` and `README-tw.md`, in the **new skill directory**.
- **Dependency Checker** — `{skillGroups.common}\scripts\depends_on.py`.

# MUST FOLLOW

- Must run workflow step by step, and display each step number.
- **This skill has no `run step N` selector — every run is a whole run.**
  Every step feeds the next and none of them is expensive, so there is nothing worth resuming into.
  Never invent a step selector for it.
- **This skill produces neither an MD report nor a YAML checkpoint.**
  Its output is the **new skill directory**: the `SKILL.md` Step 2 copies and Step 3 fills in, any `scripts\` or `references\` placeholder file Step 4 creates, the `README.md` Step 5 writes, and the **TW twins** when the user asked for them in Step 1.
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
    Never hardcode `.github\...`.
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


## Step 1 - Ask which output files the skill produces

- Ask the user which of these the new skill produces, and accept `both`, `md`, `yaml`, or `none`:
  - an **MD report** under `{wikiDir}\<skill-name>\`.
  - a **YAML checkpoint** in a Checkpoint Dir under `checkpoints\<skill-name>\`.

- If an MD report is produced, ask for its filename pattern (e.g. `run-pr-{prId}-{yymmdd}`).
- If a YAML checkpoint is produced, ask for the Checkpoint Dir naming pattern.

- Ask whether the new skill also gets **TW twins**, and accept `yes` or `no`.
  Default to `no` — a twin doubles what every later edit has to touch, since a section changed on one side must be changed on the other in the same run.
  It is asked here, with the outputs, because the answer shapes the `README.md` as well: a skill with twins lists them among what changes together, and declares the `chinese` skill it depends on.


## Step 2 - Copy Template

- Copy the **SKILL template** to the **new skill directory**'s `SKILL.md`, and display the destination path.


## Step 3 - Build SKILL.md

- Write by [skill-writing.md](.github/common/rules/skill-writing.md): each step self-contained, a step a program can do deterministically running a script, and nothing in `SKILL.md` that a run does not need — no Dataflow and no Purpose, which go into the `README.md` in Step 5, and no link to that `README.md`.

- Replace every **placeholder** throughout the copied file:
  - `{SKILL_NAME}` → the skill name parsed in Step 0.
  - `{SKILL_DESCRIPTION}` → the skill description parsed in Step 0.
  - `{SKILL_GROUP}` → the **Skill group** chosen in Step 0.
  - `{NATURAL_LANGUAGE_PROMPT}` → a realistic natural-language example prompt.
  - `{REPORT_FILENAME}` → the MD report filename pattern from Step 1.
  - `{CHECKPOINT_DIR_NAME}` → the Checkpoint Dir naming pattern from Step 1.

- Edit the MUST FOLLOW section according to the Step 1 answer:
  - No MD report → remove the report-md-rules and MD report lines.
  - No YAML checkpoint → remove the report-yaml-rules and YAML checkpoint lines, and the one-writer-per-JSON item with the item after it, which gives its reason — without a Checkpoint Dir they govern nothing.
  - Neither → also remove the display-the-paths line.

- Edit Step 0 - Warmup:
  - Remove the `.venv` line if the skill does not need a virtual environment.
  - In the `config.yaml` bullet, keep only the keys the skill actually needs (drop `wikiDir` when Step 1 said no MD report).
  - Remove the `ADO_PAT` resolution and validation bullets if the skill does not call Azure DevOps.
  - Remove the scripts/files check section, or list the skill's scripts in place of `{SCRIPT_PATH_1}`.
  - Replace `{INPUT_1}` / `{INPUT_2}` with the inputs the skill parses from its prompt.
  - Remove the YAML checkpoint line if Step 1 said no YAML checkpoint.

- Replace the `{STEP_N_TITLE}` placeholder sections — and every placeholder inside them, including the ones not named `{STEP_N_*}` (e.g. `{SCRIPT_1_ACTION_1}`, `{ROW_1}`, `{COLUMN_1}`) — with the workflow steps inferred in Step 0.
  Add or remove step sections as needed, and drop each section's `Save YAML checkpoint` / `Save MD report file` line for any output the skill does not produce.

- Leave no **placeholder** behind — before finishing, scan the file for a capital letter right after `{`; only `{PLACEHOLDER}` may remain.

- Display the generated SKILL.md content.


## Step 4 - Create supporting files

- If any step written in Step 3 runs a script, create a placeholder script file for it under the **new skill directory**'s `scripts\`.
- If any step written in Step 3 needs a reference template, create a placeholder file for it under the **new skill directory**'s `references\`.
- Display the list of created files.


## Step 5 - Build README.md

- Copy the **README template** to the **new skill directory**'s `README.md`, and fill it from the `SKILL.md` Step 3 wrote, the files Step 4 created and the Step 1 answers, by [skill-writing.md](.github/common/rules/skill-writing.md).
  Every step it names is named exactly as its heading in `SKILL.md`, number included.

- Replace the placeholders of the head:
  - `{SKILL_NAME}` → the skill name parsed in Step 0.
  - `{SKILL_DIR}` → the **new skill directory**, workspace-relative, with forward slashes.
  - `{COMMON_DIR}` → `{skillGroups.common}`, workspace-relative, with forward slashes.
  - `{COMMON_PATH}` → the path from the **new skill directory** to `{skillGroups.common}`, relative, with forward slashes — `../..` for a skill in the `common` group.
  - `{MORE_PATH_ABBREVIATIONS}` → one line for each further short name the diagrams use, such as the file a run works on or the Checkpoint Dir, or nothing when there is none.

- Keep the header quote lines that apply to the new skill, and remove the rest:
  - Always: `DFD.md`, `md-style.md`, `skill-writing.md`, `SKILL-tmp.md` and `README-tmp.md`.
  - `report-md-rules.md` when it writes an MD report, `report-yaml-rules.md` when it writes a YAML checkpoint, and `scratch-rules.md` when its MUST FOLLOW kept that line.
  - `chinese/SKILL.md` when Step 1's answer asked for **TW twins**.
  - Add a line for every other file outside the **new skill directory** that a step reads or runs, such as a shared script — a path link relative to the `README.md`, as the template's lines are.

- **Dataflow**: redraw the template's diagram so that it draws this skill rather than the template's example, in the notation of [DFD.md](.github/common/references/DFD.md): every step a rounded box named exactly as its heading, and every input a step reads and every record it writes — the prompt, `config.yaml`, each document read, each data file in the Checkpoint Dir, and each step's own group of the YAML checkpoint and section of the MD report.
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


## Step 6 - Create the TW twins

- If Step 1's answer was `no`, say that no twin was written and end the run.

- If it was `yes`, run the `chinese` skill against the **new skill directory**'s `SKILL.md`, then against its `README.md`, handing it each path — e.g. `/chinese {skillGroups[<group>]}\skills\<skill-name>\SKILL.md`.
  Each run writes one of the **TW twins** beside its source, keeps every heading, inline-code span, link target and placeholder token in English — the `README.md`'s header quote among them — and ends with its own parity check; the run on `SKILL.md` also adds the pairing line under the twin's frontmatter.

- Do not translate either file here, and do not edit the generated `SKILL.md` or `README.md` while doing it — the `chinese` skill treats its source as read-only.

- Display the paths of the **TW twins** as clickable Markdown links.
