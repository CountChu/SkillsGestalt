---
name: check-skill
description: Checks named skills' SKILL.md and README.md against the SKILL and README templates, against the workspace `config.yaml` conventions in every text file of its directory, for whether the description matches what the workflow does, whether the prose uses its own defined terms, whether its commands and scripts run on Windows, macOS and Linux, and whether the Dataflow in its README.md draws what its steps read and write. The prompt selects the six numbered checks (`1` for a whole check, `1.3` for one criterion), or a picker asks. It reports in the chat, check by check - a verdict, then each problem numbered `<check>.<n>` with a direct fix, or the original lines and lettered options when the user must choose. It writes no MD report or YAML checkpoint; its one kept file is the Skills Dashboard (`dashboard\skills.md` in the vault), one row per skill with each check's newest verdict. It edits a checked skill only after the user names items, mirroring each change into its 繁體中文 twins and marking it for a re-check.
---

# TERMINOLOGY

Terms that mean the same thing in every skill.

- **Checkpoint Dir** — the per-run directory holding a skill's YAML checkpoint.
  Every skill that writes one has its own.
- **YAML checkpoint** — the `process.yaml` inside the Checkpoint Dir.
  Every step writes its outputs there under a `step_{N}` group, so a later step reads them back instead of recomputing them.
- **MD report** — the Markdown report a skill writes into the wiki vault, in a folder named after that skill, carrying the standard header (Skill, Checkpoint, Created, Updated, Prompt) above its result sections.

# DEDICATED TERMINOLOGY

Terms specific to this skill's domain.

- **`{yymmdd-hh}`** — the run stamp: the date and the hour the run started, read once in Step 0 (e.g. `260806-11`).
  It names the **facts file**, and its date — as `yyyy-mm-dd` — is what each checked skill's row on the **Skills Dashboard** records, so one run cannot land under two stamps.
- **checked skill** — a skill this run examines.
  Steps 0-5 only ever read it; Step 6 edits it, and only for the **items** the user named.
- **skill directory** — the checked skill's own folder: its `SKILL.md` and `README.md`, their 繁體中文 twins, its `scripts\`, its `references\` and its own `config.yaml`.
  The scan reads **every text file in it**, since a path baked into a script breaks exactly as one baked into a step does.
- **check** — one of the six selectable examinations, numbered in the **checking criteria**: `1` `Template alignment`, `2` `Config conformance`, `3` `Description accuracy`, `4` `Terminology usage`, `5` `Cross-platform compatibility`, `6` `Dataflow`.
  A run applies any combination of them, and narrows one to a single criterion by its `<check>.<n>` number.
- **checking criteria** — the rubric the six checks apply: the rules every check follows, and the numbered criteria of each one.
  **It owns the criteria**; this document owns the workflow that runs them, so a new or changed criterion is a change to that file and never to a step.
- **facts file** — the scratch YAML the scan writes: one YAML document per checked skill, holding facts only and never verdicts.
  It is the input every check reads, and it is deleted once the **Skills Dashboard** is updated.
- **fact group** — one top-level key of a checked skill's facts-file document: `template_shape`, `config_shape`, `dir_config_shape`, `leftovers`, `readme_shape`, `terminology`, `dataflow`.
- **region** — the part of a `SKILL.md` a fact was found in: `frontmatter`, `prompt_examples` or `body`.
  Only `body` is judged.
  A fact from anywhere else in the **skill directory** carries no region — it carries its file and that file's kind instead, and the `readme_shape` and `dataflow` facts are of the skill's `README.md`.
- **finding** — one defect pinned to a file and a line, with the offending text quoted.
  A defect that cannot be pinned to a line is not a finding and is not reportable.
- **issue** — a finding that breaks a contract: the checked skill does not do what its template, its `config.yaml`, its own description or its own glossary commits it to, or it exceeds a limit of the skill loader that has to accept it.
- **recommendation** — a finding that works as written but drifts from the reference.
  Never blocking; the author may decline it.
- **verdict** — one check's result for one checked skill: ✅ no finding, ⚠️ recommendations only, ❌ at least one issue, ➖ not applicable (check 4 on a skill with no glossary, check 6 on one with no Dataflow in a `README.md`).
- **item** — one numbered entry of the report, `<check>.<n>`, carrying one finding and the change that settles it; it is either a **direct fix** or a **decision item**.
  The user applies items by naming their numbers, and a number means something only in the report that printed it.
  It shares its shape with a criterion number but never its context: `1.3` on the prompt's check line is criterion 3 of check 1, while `1.3` in an answer to the report is item 3 of check 1.
- **direct fix** — an item with one obvious change: its Problem, then its Fix.
- **decision item** — an item whose settlement is the user's choice: its Original lines, then its Problem, then its lettered options.
- **option** — one lettered way to settle a decision item, `(a)`, `(b)` and so on, named together with its item when applied (`1.3(a)`).
- **checker defect** — a false positive or blind spot in `scan_skill.py` or in a check's own instructions, rather than in the checked skill.
  Kept out of every count, and never an item.
- **Skills Dashboard** — the unstamped `skills.md` in the wiki vault's `dashboard\` folder: one section per skill group, one row per checked skill in it, one cell per check holding that check's newest verdict and counts, the date it was last checked, as `yyyy-mm-dd`, and whether it was edited since.
  It is a current view merged across runs — never a history, and never rewritten from a single run.
- **needs check** — the dashboard mark Step 6 sets on a skill it edited: that row's cells describe the skill as it was before the edit.
  Only a run that re-applies every check the row holds, in full, clears it.

# CONFIGURATION

Concrete values this skill runs with.

- **facts file** — `temp\check-skill-facts-{yymmdd-hh}.yaml`, under the workspace root.
- **checking criteria** — [checking-criteria.md](.github/common/skills/check-skill/references/checking-criteria.md), under `{skillGroups.common}\skills\check-skill\references\`.
- **Skills Dashboard** — `{wikiDir}\dashboard\skills.md`, where `wikiDir` comes from the workspace [config.yaml](config.yaml) (resolved in Step 0) — never hardcode the wiki root.

# MUST FOLLOW

- Must run workflow step by step, and display each step number.
- **This skill has no `run step N` selector — every run is a whole run.**
  Nothing it does is expensive or irreversible enough to be worth resuming, and the work a selector would narrow is already narrowed by the check numbers the prompt carries.
  Never invent a step selector for it.
  Step 6 is not one either: it runs only when the user answers the report by naming items.
- **Only check until the user names items.**
  Steps 0-5 never modify a checked skill — no edit, no rename, no reformat, no auto-fix, not even a whitespace change.
  Step 6 changes it for the **items** the user named by number and for nothing else, and only once they have named them.
  An obvious fix is still an item for the user to choose, never one to apply unasked.
- **This skill produces neither an MD report nor a YAML checkpoint**, and has no Checkpoint Dir.
  It reports in the chat, and the one file it keeps is the **Skills Dashboard**.
  The **facts file** is scratch, deleted at the end of Step 5.
  Every other file it opens — every text file in each checked **skill directory**, the SKILL and README templates, the files a `README.md` declares in its header quote, `DFD.md`, `config.yaml` — is read and never written, except the files Step 6 edits for the named items.
- **The Skills Dashboard is merged into, never rewritten from one run.**
  `update_dashboard.py` owns its shape: a skill this run did not check keeps its row as it was, and a check this run did not apply keeps its cell, marked with the date of the run that last applied it.
  Never edit the dashboard by hand — a row the script did not write is one the next run cannot read.
- Follow [scratch-rules.md](.github/common/rules/scratch-rules.md) for where the facts file goes and how it is cleaned up.
- **Before the skill ends, display the Skills Dashboard path** — the path only, never its contents, as a clickable Markdown link, never as inline code or plain text.
  The vault lives outside this workspace, so link it with an `obsidian://open?vault={vaultName}&file=dashboard/skills.md` URI (e.g. `[skills.md](obsidian://open?vault={vaultName}&file=dashboard/skills.md)`).
  Do this for every run, including one that stopped early because no skill resolved or no check was selected — and say then that the dashboard was not updated.
- **Every file and line the report cites must be a clickable link.**
  The report is read in the chat, and a checked skill usually lives outside this workspace, so only an absolute target can resolve to it.
  - Format: `[<file>:<n>](<absolute-path>:<n>)` — e.g. `[SKILL.md:44](C:/Users/.../.github/dedi-boot-times/skills/report-boot-times-html/SKILL.md:44)`.
  - `<absolute-path>` is the file the finding was found in — the checked skill's own `SKILL.md`, or the script, reference or config file a check-2 finding names — resolved through `skillGroups`, written with **forward slashes** throughout.
    A backslash silently breaks the link.
    Wrap the target in `<…>` when the path holds a space.
  - Applies to every Problem and Original line, and every line cited in prose.
    A range keeps `<file>:<n>-<m>` as its text and points the target at `<n>`, since the target addresses a single line.
  - Never render a line number as plain text or as inline code, and never emit one link covering two non-contiguous lines — cite each separately.

# Prompt Examples


## Prompt 1

```
/check-skill
report-boot-times-html
```

## Prompt 2

```
/check-skill
report-pipeline, triage-test-case
1, 2, 3, 4
```

## Prompt 3

```
/check-skill
report-pipeline
1.3, 4
```


# Workflow

## Step 0 - Warmup

- Run `.venv` first — the scan script imports `PyYAML`.

- Read the workspace config [config.yaml](config.yaml) at the workspace root and resolve:
  - **`skillGroups`**: the group name -> skills-root map — every checkable skill lives at `{skillGroups[<group>]}\skills\<skill-name>\SKILL.md`, and this skill's own directory is `{skillGroups.common}\skills\check-skill\`.
  - **`wikiDir`**: the wiki root — the **Skills Dashboard** lives under `{wikiDir}\dashboard\`.
    It is also the value the config-conformance check compares against, so it can tell a skill that correctly resolves `wikiDir` from one that hardcodes a wiki path.
  - **`vaultName`**: the last path segment of `wikiDir` (e.g. `MyVault`) — the Obsidian vault name used to build the dashboard's `obsidian://` link.
  - Substitute the resolved values wherever `{skillGroups.common}`, `{wikiDir}` or `{vaultName}` appears in the steps below (including in commands).
  - If `config.yaml` is missing or a needed key is absent, stop and ask the user.

- This skill calls no Azure DevOps API and needs no `ADO_PAT` — it reads local files only.
  Never prompt for a credential.

- Check if the below scripts/files exist before running workflow.
  - `{skillGroups.common}\skills\check-skill\scripts\scan_skill.py`
  - `{skillGroups.common}\skills\check-skill\scripts\update_dashboard.py`
  - `{skillGroups.common}\skills\check-skill\references\checking-criteria.md`
  - `{skillGroups.common}\references\DFD.md`
  - `{skillGroups.common}\scripts\depends_on.py`

- Confirm the SKILL template and the README template exist at `{skillGroups.common}\templates\SKILL-tmp.md` and `{skillGroups.common}\templates\README-tmp.md`.
  They are the references the alignment check compares a skill's `SKILL.md` and `README.md` against, so stop and tell the user if one is missing rather than checking against a remembered shape.

- The prompt takes one of the forms shown in **Prompt Examples** above.
  Parse it for:
  - **Skill names** (required): one or more skill names, comma- or space-separated (e.g. `report-pipeline, triage-test-case`).
    Resolve each against the `skillGroups` roots; report any name that matches no skill and drop it.
    This skill never offers a list of skills to choose from — a list carrying every skill in the workspace is slower to answer than typing the name — so when the prompt names none, ask the user to type the skill name and wait for the answer.
  - **Check numbers** (optional): the line after the skill names, comma- or space-separated (e.g. `1, 2, 3, 4`).
    `1` selects a whole check; `1.3` selects only that check's third criterion, leaving its other criteria out of the run.
    Report and drop a number outside 1-6, and a criterion number the **checking criteria** does not define.
    When the line is absent, leave the selection unresolved — Step 1 asks for it.

- If a required input is missing, ask the user for it.

- Read the clock **once** here and keep the `{yymmdd-hh}` stamp for the whole run, so the **facts file** and the dashboard rows of one run cannot land under two stamps across an hour or midnight rollover.
  Re-running within the same hour reuses the stamp and overwrites that hour's facts file; the dashboard keeps only the date, so every run on the same day records the same one.

- Display the resolved `wikiDir`, the parsed skill names and check numbers, and the `{yymmdd-hh}` stamp.


## Step 1 - Resolve Skills and Select Checks

- Take the skill names Step 0 parsed and confirm each resolves to `<root>\skills\<skill-name>\SKILL.md` under a `skillGroups` root, recording its group and its **absolute** `SKILL.md` path — every line link in the report, and the skill's row on the **Skills Dashboard**, are built from it.
  Drop and report any name that does not resolve.
  If no name resolves, stop and ask the user to name a skill — never fall back to checking every skill.

- **Take the checks from the check numbers Step 0 parsed.**
  `1` puts the whole check in scope; `1.3` puts only that criterion in scope and leaves every other criterion of check 1 out of this run, which the steps below judge by and the report says explicitly.

- **Present the check picker only when Step 0 parsed no check numbers**, via `vscode_askQuestions` so the user chooses which checks to apply.
  Never carry a selection over from an earlier run:
  - One question, `header: checks`, `question: Select the checks to apply`, `multiSelect: true`.
  - Six options, all marked recommended:
    - `1 Template alignment` — do the skill's `SKILL.md` and `README.md` follow `SKILL-tmp.md` and `README-tmp.md`?
    - `2 Config conformance` — does the skill follow the workspace `config.yaml`?
    - `3 Description accuracy` — does the skill's `description` match what its workflow actually does and produces?
    - `4 Terminology usage` — does every section use the skill's own defined terms, instead of restating or paraphrasing them?
    - `5 Cross-platform compatibility` — do the commands the skill runs, and its scripts, work on Windows, macOS and Linux, or say which platform they assume?
    - `6 Dataflow` — does the Dataflow in the skill's `README.md` draw, in DFD notation, what its steps actually read and write?
  - If the user selects nothing, stop and say that no check was selected.

- Display the resolved selection:
  - **Summary line**: how many skills resolved, and which checks were selected.
  - **Skills table** with columns **Skill**, **Group**, **Path**.
  - **Notes**: every name that was dropped; every check that was **not** selected, named explicitly, since an unrun check is not a clean bill of health; and every criterion left out of a narrowed check, for the same reason.


## Step 2 - Scan the Selected Skills

- Run the script `scan_skill.py` once for the whole selection, passing every selected skill.
  - `--skill`: a selected skill name; repeat the flag once per skill.
  - `--out`: the **facts file** path given under **CONFIGURATION**.
  - `--template`: the SKILL template path Step 0 confirmed.
    The script reads the required headings out of it, so the reference is never a shape remembered in code.
  - `--readme-template`: the README template path Step 0 confirmed, read the same way for the headings of `README.md`.
  - `--depends-on`: `{skillGroups.common}\scripts\depends_on.py`, which the script loads to read each `README.md`'s header quote as `depends_on.py check` reads it.
  - Example: `python {skillGroups.common}\skills\check-skill\scripts\scan_skill.py --skill report-pipeline --skill triage-test-case --out "temp\check-skill-facts-{yymmdd-hh}.yaml" --template "{skillGroups.common}\templates\SKILL-tmp.md" --readme-template "{skillGroups.common}\templates\README-tmp.md" --depends-on "{skillGroups.common}\scripts\depends_on.py"`

- The script collects **facts only, never verdicts** — it records what each file contains and leaves every judgement to the checks:
  1. Resolves each skill under the `skillGroups` roots and reads its `SKILL.md`.
  2. Records the **template-shape** facts: whether the YAML frontmatter parses and carries `name` / `description`, whether `name` equals the directory name, the lengths of `name` and `description` in characters (`name_chars`, `description_chars`) and whether `name` holds only lowercase letters, digits and hyphens (`name_charset_ok`), the top-level headings the SKILL template itself defines (`required_headings`, read from the `--template` file so a change to the template changes the reference), which of them the skill has, which are absent (`missing_headings`), whether the present ones keep the template's relative order, the `## Step N` headings found, whether they run contiguously from 0, whether Step 0 is titled `Warmup`, and every step reference that points forward.
  3. Records the **config-shape** facts of that `SKILL.md`: every literal `wiki\` / `wiki/` path, every `{wikiDir}` / `{vaultName}` / `{skillGroups...}` placeholder and whether Step 0 resolves it, every machine-specific absolute path, every UNC share path, and every `.github\...` path written literally instead of through `skillGroups`.
  4. Records the **dir-config-shape** facts: the same hardcoded-path facts for **every other text file in the skill directory** — its scripts, its references, its 繁體中文 twin, its own `config.yaml` — each carrying the file, that file's `kind` (`script`, `reference`, `twin`, `skill config`, `doc`, `other`), the line, whether the line is a comment or a Python docstring (`commented`), and whether the skill has a `config.yaml` of its own (`has_own_config`).
     It also lists the files it skipped with the reason — a binary, or one over the scan's size limit — so a file nobody checked is never mistaken for a clean one.
  5. Records the **leftovers**: any `{PLACEHOLDER}` token, any placeholder in a retired form on a list of its own (`old_placeholder_tokens`), any `.github` rules link that does not resolve on disk, any `scripts\*.py` the SKILL.md names but that is missing, and any script on disk the SKILL.md never names.
  6. Tags every fact with the region it was found in, whether it sits inside an inline-code span (`backticked`) or a fenced block (`fenced`), and the whole line it came from (`line_text`) — a literal path is expected in `frontmatter` and `prompt_examples` and suspect only in `body`, a token that is quoted or fenced is being *shown* rather than left behind, and the line is what a finding quotes.
     A fact from outside `SKILL.md` carries its file and `commented` flag in place of a region.
     The same token on two lines of one file, and what the fields settle:

     ```
     - `{SKILL_NAME}` -> the skill name parsed in Step 0.
       backticked: true  -> the step is describing the token. Not a leftover.

     - Replace {SKILL_NAME} with the parsed name.
       backticked: false -> the token really was left behind. A finding, which
                            quotes this whole line from line_text.
     ```
  7. Records the **terminology** facts: whether the skill has a glossary section (any `#` heading whose name contains `TERMINOLOGY`), each term it defines, every line outside the glossary where that term is used exactly, every line where a case- or form-variant of it appears instead, every line where a filename the definition introduces is used raw, and every term defined under a `CONFIGURATION` heading rather than in the glossary (`terms_defined_in_configuration`).
     A skill with no glossary yields `has_glossary: false`, and its `CONFIGURATION` definitions are still recorded.
  8. Records the **readme-shape** facts of the skill's `README.md`: whether it has one (`has_readme`), and whether it and `SKILL.md` have 繁體中文 twins; its title, and the `#` and `##` headings the README template defines (`required_headings`, read from the `--readme-template` file), which are absent (`missing_headings`) and whether the present ones keep the template's order; every dependency its header quote declares, with the status `depends_on.py check` gives it — `UNCHANGED`, `CHANGED`, `NO_RECORD`, `NOTHING_CITED` or `MISSING`; against the Workflow, every step its Step Purposes leaves out, misnames or gives no Purpose, and every step the tree of its Files Each Step Uses leaves out or misnames, and whether that section answers the scripted-versus-not rule in a bold sentence; every `{PLACEHOLDER}` token in it, and every placeholder in a retired form on a list of its own (`old_placeholder_tokens`); and every line of `SKILL.md` that holds what belongs in `README.md` — a `# Dataflow` or `# Steps at a Glance` heading, a `- **Purpose**:` line, the paragraph that introduces the Purposes — or links to it.
  9. Records the **dataflow** facts of the `## Dataflow` in the skill's `README.md`, every line number a line of that file: whether it has one (`has_dataflow`) and how many mermaid diagrams it holds; every node of its first diagram with the shape it is drawn in, every arrow with whether it is dotted, two-headed or blue, and how many lines of legend follow the diagram; against the Workflow, every step the diagram leaves out or misnames; and every record a later step overwrites, every record several steps edit in turn, every piece of data nothing supplies, every solid arrow between two pieces of data, every read of something a later step writes, and every record that steps before its first writer read as it was found.
  10. Writes the facts file to the `--out` path — one YAML document per skill — and prints to **stdout** its path plus one summary row per skill.

- Read the facts file at `temp\check-skill-facts-{yymmdd-hh}.yaml`.
  Every fact carries a line number, so quote that line when reporting a finding against it.

- Display one line per skill: its group, its line and step count, its missing headings, whether it has a `README.md` and the headings missing from it, and how many files in its **skill directory** the scan read and skipped — naming every skipped file with its reason, since an unread file is not a conformant one.


## Step 3 - Apply the Selected Checks

- **No script for this step** — deciding whether a deviation is a genuine defect or a deliberate, well-founded exception is reading and judgement a program cannot do, so follow the instructions below yourself.

- Work through the checks Step 1 put in scope in ascending number order.
  For each one: read its input, judge, record, then move to the next.
  Say which checks were not selected and judge nothing for them.

- **Inputs**, per check.
  Every fact group named here comes from the facts file Step 2 wrote at `temp\check-skill-facts-{yymmdd-hh}.yaml`:

  | # | Check | Input |
  |---|-------|-------|
  | 1 | Template alignment | the templates at `{skillGroups.common}\templates\SKILL-tmp.md` and `{skillGroups.common}\templates\README-tmp.md`, plus the `template_shape`, `readme_shape` and `terminology` fact groups |
  | 2 | Config conformance | the workspace [config.yaml](config.yaml), plus the `config_shape` and `dir_config_shape` fact groups, and the checked skill's own `config.yaml` when it has one |
  | 3 | Description accuracy | each selected skill's **whole** `SKILL.md` — its `description` field, its `# MUST FOLLOW` contract and every step section. This check reads no fact group |
  | 4 | Terminology usage | the `terminology` fact group. A skill whose facts say `has_glossary: false` is out of scope — its verdict is ➖ `no glossary — not applicable` and it finds nothing, rather than inventing terms it never claimed; its missing glossary is already an issue check 1 raises |
  | 5 | Cross-platform compatibility | each selected skill's **whole** `SKILL.md` and every script under its `scripts\` — the commands a step tells the agent to run, and each script's subprocess and platform-specific calls. This check reads no fact group |
  | 6 | Dataflow | the `dataflow` fact group, [DFD.md](.github/common/references/DFD.md), and each selected skill's **whole** `SKILL.md` and `README.md` — every step's section, to compare what it reads and writes with what the Dataflow in `README.md` draws. A skill whose facts say `has_dataflow: false` is out of scope — its verdict is ➖ `no Dataflow — not applicable`; its missing `README.md` or Dataflow is already an issue check 1 raises |

- Judge each selected skill against the **checking criteria** — its `Rules that apply to every check` section, then the section of the check being applied, restricted to the criteria Step 1 put in scope.
  Read both before judging; never work from a remembered rubric.

- **Record every finding for the report**, per check and per skill: its severity — **issue** or **recommendation** — the criterion it breaks (`<check>.<criterion>`), its file and line, the offending line whole from `line_text`, why it breaks the contract or drifts, and how it is settled.
  - A finding with one obvious change becomes a **direct fix**; record that change, with the replacement text when it is a wording change.
  - A finding with more than one reasonable settlement — typically two places that contradict each other, where the user must say which one wins — becomes a **decision item**; record every line it touches and each **option**, with the lines and files that option would change and what it costs.
  - A check-3 finding records both the description's claim and the step that contradicts or omits it, since the workflow is authoritative and the claim is what changes.

- **Record what each check found clean, too**, for the report's notes — each one on the record rather than silently passed:
  - Check 1 — the criteria that passed, and every template section a skill omits that the check judged legitimate.
  - Check 2 — the criteria that passed; every literal path judged intentional, named with its region, or with its file and kind when it came from outside `SKILL.md`, so a deliberate literal is not mistaken for an unreviewed one; and every file the scan skipped, since an unread file is not a conformant one.
  - Check 3 — the criteria that passed, and every claim recorded as `unknown`, since a claim the workflow can neither confirm nor refute is not a passing one.
  - Check 4 — how many terms were looked at and how many are used, and every skill skipped for having no glossary, named explicitly, since a skipped skill is not a consistent one.
  - Check 5 — the criteria that passed, every command judged shown rather than invoked, and every platform the skill declares, since a declared platform is not a defect.
  - Check 6 — the criteria that passed, how many steps, pieces of data and arrows were compared, and every skill skipped for having no Dataflow, named explicitly, since a skipped skill is not a conforming one.

- Record, apart from every finding, each **checker defect** the judging exposed — a fact `scan_skill.py` got wrong, or a criterion that misled — with the line that misled it.


## Step 4 - Report the Findings

- **No script for this step** — laying out an argument so a reader can act on it is writing, not computation, so follow the instructions below yourself.

- **Report in the chat.**
  Nothing in this step is written to a file.

- **Render Step 3's findings and judge nothing anew.**
  A gap noticed while writing is a gap in the check that should have caught it — record it as a **checker defect**, never as a new **item**.

- **One section per checked skill**, in the order Step 1 resolved them, opening with one line: the skill, its group, and its overall **verdict** with its totals.

- **Within it, one sub-section per check that ran**, in number order, each laid out as **verdict → notes → items**:
  - **Verdict** — the check's **verdict** for this skill.
    A check narrowed to some criteria names them beside it, so a narrowed pass never reads as a whole one.
  - **Notes** — one or two unnumbered sentences on what was checked and found clean: the criteria that passed, the facts looked at, and the notes Step 3 recorded for this check.
    They take no number.
  - **Direct fixes**, then **Needs your decision** — both labels always appear.
    An empty one reads **None**: the empty place is what says the check is clean rather than skipped.

- **Number every item `<check>.<n>`:**
  - `<n>` starts at 1 in each check and never continues across checks — check 3's first item is `3.1`.
  - Direct fixes and decision items share one sequence: the direct fixes first, the decision items continuing after them, so no check carries two `3.1`s.
  - **None** takes no number.
  - A number holds only within this report; a re-run renumbers, so an old number never names an item in a new report.
  - When the run checked more than one skill, a number is unique only within its skill's section, and the user names both (`imp-app 1.1`).

- **Head every item** `**<check>.<n> <the problem in one line>**`, followed by its severity and the criterion it breaks.

- **A direct fix is Problem → Fix:**
  - **Problem** — its file and line as a link, the offending text quoted, and why it breaks the contract or drifts.
  - **Fix** — what changes and in which files, with the replacement text itself whenever the change is a wording change.

- **A decision item is Original → Problem → Options** — the original comes first because the user has to see how the skill actually reads before choosing a side, and the paraphrase inside a problem statement is not enough for that:
  - **Original** — every line the decision touches, each with its file and line as a link and quoted **whole** as a block quote beneath it: from line start to line end, verbatim, dropping only the leading indent and the list marker.
    Never excerpt a line and never shorten it with `…` — a cut line loses the conditions and the scope the choice turns on.
    A table row is quoted as the whole row.
  - **Problem** — why those lines conflict, or what the choice is between.
  - **Options** — `(a)`, `(b)` and so on, each saying what it changes, which lines and files it touches, and what it costs.
    Then **Recommended**: the **option** you would pick and, in one sentence, why the others are worse.

- **Expand in proportion to the decision.**
  A direct fix stays two or three lines; a decision item earns the full treatment.
  Padding a simple item to the shape of a complex one buries the complex one.

- **A change to a skill's `SKILL.md` or `README.md` names that file's 繁體中文 twin too**, when the skill has one — the twin moves in the same edit, so the fix touches both files.

- The shape, for one skill and one check:

  ```
  ❌ imp-app (common) — 4 issues, 8 recommendations across checks 1-4

  ### 1 Template alignment — ❌

  Criteria 1.1, 1.2, 1.5-1.8 and 1.10 pass: <what was looked at>.

  **Direct fixes**

  **1.1 No Prompt Example shows `run step N`** — issue, criterion 1.9
  - **Problem**: [SKILL.md:138](<absolute-path>:138) — <quoted text>; <why>.
  - **Fix**: <what changes, in SKILL.md and SKILL-tw.md>.

  **Needs your decision**

  **1.2 `# CONFIGURATION` defines `app dir` instead of giving its value** — issue, criterion 1.3
  - **Original**:
    - [SKILL.md:39](<absolute-path>:39)
      > <the whole line>
    - [SKILL.md:93](<absolute-path>:93)
      > <the whole line>
  - **Problem**: <why the two lines conflict>.
  - **Options**:
    - (a) <change> — touches SKILL.md:93 and SKILL-tw.md:91; <cost>.
    - (b) <change> — touches SKILL.md:39 and SKILL-tw.md:37; <cost>.
  - **Recommended**: (a) — <why (b) is worse>.
  ```

- **Close the report with these, in this order, and nothing else:**
  1. **Root cause** — only when findings in several checks come from one cause: name the cause and the item numbers it drives.
     The items stay under their checks; never move them here.
  2. **Checker defects** — each one Step 3 recorded, citing the line that misled the scan or the check, stated plainly as a defect in `scan_skill.py` or in a check's own instructions rather than in the checked skill.
     Unnumbered and uncounted — a checker bug is not the author's debt.
  3. **Not selected** — the checks this run did not apply, named in one line, since an unrun check is not a clean one.
  4. **How to apply** — the user applies items by naming their numbers (e.g. `fix 1.1 3.2`, `fix 1.2(a)`, `fix all of check 1`), and nothing changes until they do.


## Step 5 - Update the Skills Dashboard

- **Run this step on every run**, including one where every checked skill came back clean.
  A clean row is the evidence that an earlier run's findings are gone, so skipping it is what leaves a fixed skill looking broken.

- Run the script `update_dashboard.py` once per checked skill.
  - `--dashboard`: the **Skills Dashboard** path given under **CONFIGURATION**.
  - `--run`: this run's `{yymmdd-hh}` stamp.
    The script records only its date, as `yyyy-mm-dd`.
  - `--skill`, `--group`, `--path`: the skill, its group and its absolute `SKILL.md` path, as Step 1 resolved them.
    The group names the section the row is filed under.
  - `--result`: once per check that ran, as `<check>:<issues>:<recommendations>` from Step 3's counts; as `<check>:<issues>:<recommendations>:<criteria>` for a check narrowed to some criteria, joined by `+` (e.g. `1:0:1:1.3+1.5`); and as `4:na` for a skill with no glossary, or `6:na` for one with no Dataflow.
  - Example: `python {skillGroups.common}\skills\check-skill\scripts\update_dashboard.py --dashboard "{wikiDir}\dashboard\skills.md" --run {yymmdd-hh} --skill report-pipeline --group dedi-triage-pipeline --path "<absolute SKILL.md path>" --result 1:1:5 --result 2:0:0 --result 3:0:2 --result 4:na`

- The script:
  1. Creates the dashboard with its header when it does not exist yet, and otherwise reads its table back.
  2. Replaces the skill's cells for the checks this run applied, and **records nothing for a check the run did not select** — that cell keeps its earlier result, marked with the date of the run that produced it, since an unrun check is not evidence that its findings are gone.
  3. Sets the row's **Checked** to this run's date, links the skill to its `SKILL.md`, and recomputes the row's overall verdict from its cells.
  4. Clears the row's **needs check** mark only when this run re-applied every check the row holds, in full.
  5. Leaves every other skill's row untouched, files each row under its group's section — sections sorted by group, rows by skill — and refreshes the header's **Updated** field.
  6. Prints each cell it changed as `old -> new`.

- Display, per skill, the cells its call changed as `old -> new`, so the user sees that the dashboard moved and how.
  Say a finding is gone only where its cell fell from what an earlier run left there — that fall is the evidence, and this run alone is not.

- Delete the **facts file** by its exact name — `temp\check-skill-facts-{yymmdd-hh}.yaml`, never a wildcard.
  Nothing after this step reads it.


## Step 6 - Apply the Named Items

- **Runs only when the user answers the report by naming items.**
  A run whose report the user does not answer is complete at Step 5.

- **No script for this step** — settling a finding means rewriting prose so that it keeps its meaning, which is judgement.

- **Read the selection by the report's numbers** — `fix 1.1 3.2`, a range such as `1.1-1.3`, `all of check 3`, or `all`:
  - A **decision item** needs its **option** (`1.2(a)`); named without one, ask which, and never pick one for the user.
  - When the run checked more than one skill, a number needs its skill (`imp-app 1.1`).
  - A number the report does not carry, or one that could mean two items, is a question to the user, never a guess.

- **Apply the items one by one, in the order named**, and report each as it lands: what changed, in which files, and at which lines, as links.

- Rules that apply to every item:
  - **Change what the item names and nothing more.**
    A problem noticed while editing is reported, not fixed — it has not been judged, and the next run is what judges it.
  - **Mirror every change into the 繁體中文 twin of the file it changes in the same step** — `SKILL-tw.md` for `SKILL.md`, `README-tw.md` for `README.md` — under the same heading, keeping every heading, glossary term, inline-code span, fenced block and link target in English.
    A changed reference file with a `-tw` twin moves with its twin the same way.
  - **Propagate a rename** — of a term, a file, a heading or a script flag — to everywhere the **skill directory** names it: the glossary, every step, the twins, each script's help text, and the Dataflow, Step Purposes and Files Each Step Uses of `README.md`, which name each step exactly as its heading.
  - **When a change alters a value or a definition, find every other sentence in the skill that restates it** — prose often repeats a table's numbers or a glossary entry — and change those too, so the fix does not open a new drift of its own.
  - **When a change introduces or rewrites a term, update its glossary entry** in the same edit, and use the term — bolded, as the glossary spells it — wherever the prose names it.
  - **Never edit outside the checked skill's directory.**
    A **checker defect** is fixed in this skill only when the user asks for it separately.

- **After the last item, mark the skill on the dashboard as needing a re-check**, so its row is not mistaken for a check of the edited skill:
  - Example: `python {skillGroups.common}\skills\check-skill\scripts\update_dashboard.py --dashboard "{wikiDir}\dashboard\skills.md" --skill imp-app --mark-modified`
  - The cells stay as the last check left them — they describe the skill before these edits — and the next run that re-applies every check clears the **needs check** mark.

- Close by listing the items applied, any skipped and why, and that re-running `/check-skill` on the skill is what confirms them.
