# Checking Criteria

> [[README-tmp]]  `2026-10-30`  `43ace64a88a6`
> [[skill-writing]]  `2026-10-30`  `c7696bf6351a`

The rubric the `check-skill` skill applies.
**This file owns the criteria** — what each check looks for, and where the line between an issue and a recommendation falls.
`SKILL.md` owns the workflow that runs them: which check runs, what it reads, and what it writes.
A new or changed criterion is a change to this file, never to a step.

Read only the sections for the checks the run selected.
Each check carries a number, and each of its criteria is addressed as `<check>.<n>` — `1` is the whole `Template alignment` check, `1.3` is its third criterion alone.

## Rules that apply to every check

- **Classify every finding as an issue or a recommendation.**
  An **issue** breaks a contract the checked skill committed to — its template, its `config.yaml`, its own description, its own glossary, or the limits of the skill loader that has to accept it.
  A **recommendation** works as written but drifts from the reference; it never blocks, and the author may decline it.
- **Cite the file and the line, and quote the offending text.**
  A finding that cannot be pinned to a line is not reportable — never infer a violation from a skill's name, age or reputation.
- **Never invent a value.**
  Base every conclusion on the input the step names.
  When something cannot be judged from the available text, record it as `unknown` and say why instead of guessing.
- **A fact's `region` decides whether it is judged.**
  Judge the `body` region only: a literal path or a plain-prose phrase in `frontmatter` or `prompt_examples` is written without the config or the glossary in view and is intentional.
  The one exception is a check whose subject *is* the frontmatter — `Description accuracy` reads the `description` field itself.
- **A fact from outside `SKILL.md` carries no region.**
  It carries its `file`, its `kind` (`script`, `reference`, `twin`, `skill config`, `doc`, `other`) and the `backticked` / `fenced` / `commented` flags instead, and those are what say whether the path is being *used* or merely *shown*.
  The `readme_shape` and `dataflow` facts are of the skill's `README.md`: their line numbers are lines of that file, and a finding against one cites `README.md`.

## 1. Template alignment

**Why it exists** — it isolates the one question the template can answer, shape, so a structural defect is still reported in a skill whose prose reads faultlessly.

The two templates are the reference — `SKILL-tmp.md` for `SKILL.md`, `README-tmp.md` for `README.md` — **not a straitjacket**.
A skill may legitimately omit a template section it does not need — an `ADO_PAT` bullet in a skill that calls no API, a `.venv` line in a skill that runs no script.
Report a missing section only when the skill plainly needs it.

1. **Frontmatter** — does it parse as YAML, does `name` match the directory name, is a non-empty `description` present, and does each stay within the limits the skill loader documents ([VS Code: Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)) — `name` at most 64 characters of lowercase letters, digits and hyphens, `description` at most 1024 characters?
   Read `name_chars`, `name_charset_ok` and `description_chars`.
   **A value over a limit is an issue however well the rest of the skill reads**: the loader skips the skill with no error and no diagnostic, so it never appears among the available skills and cannot be selected at all — and a file that is otherwise well formed leaves no other criterion anything to catch.
   Beyond those limits, check presence and structure only — **never judge what the description says**.
2. **Required headings** — is every heading listed in `required_headings` present in `SKILL.md`, in the template's order, and every heading listed in `readme_shape.required_headings` present in `README.md`, in the README template's order, under a title that is the skill's name?
   Those are the templates' own headings, so judge against them and never against a remembered list.
   Read `missing_headings`, and `readme_shape.missing_headings`, `heading_order_ok` and `title_is_skill_name`.
   A missing `# TERMINOLOGY` or `# DEDICATED TERMINOLOGY` is an issue whenever the steps lean on nouns the skill never defines — which is nearly always; only a skill with no domain vocabulary of its own may omit the dedicated one.
   A missing `# CONFIGURATION` is an issue for any skill that writes an MD report or a YAML checkpoint, since their paths have nowhere else to live.
   **A skill with no `README.md` (`readme_shape.has_readme: false`) has one issue here, not one for each section it lacks**: its Dataflow, its Step Purposes and what changes with it have nowhere else to live, and check 6 has nothing to judge.
   A missing `## Dataflow` in a `README.md` is an issue for every skill, for the reason check 6 gives.
3. **Glossary placement** — does `terms_defined_in_configuration` name a term that `# CONFIGURATION` defines rather than merely gives a path for?
   `# CONFIGURATION` carries concrete values; the glossary owns definitions.
   A `- **X** — <path>` line is correct there; a `- **X** — <what X means>` line belongs in `# TERMINOLOGY` or `# DEDICATED TERMINOLOGY`.
4. **MUST FOLLOW contract** — does it declare the step-by-step rule, its `run step N` rule — how the selector behaves, or an explicit statement that the skill has none — and its output contract (MD report / YAML checkpoint, or an explicit statement that it produces neither)?
   The no-forward-reference rule and the script-versus-judgement rule are not declared here: [skill-writing.md](.github/common/rules/skill-writing.md) holds them for every skill, criterion 7 judges the first in the steps themselves, and criterion 12 the answer to the second.
5. **Step 0 - Warmup** — does it exist, is it titled `Warmup`, and does it resolve everything the later steps actually use?
6. **Step numbering** — do the `## Step N` headings run contiguously from 0, with no duplicated or skipped number?
7. **Forward references** — does any step **depend** on a step that comes after it?
   Judge each entry in `forward_references` against what the reference does: naming a later step to route control flow (`skip ahead when Step N found nothing`) is allowed, borrowing a later step's output is an issue.
8. **Leftover placeholders** — is any `{PLACEHOLDER}` token still present, in `SKILL.md` or, read from `readme_shape.placeholder_tokens`, in `README.md`, or any placeholder in a retired form, read from `old_placeholder_tokens` in `leftovers` and in `readme_shape`?
   A token left behind from a template is always an issue; a token the step is *showing* rather than using is not — read `backticked` and `fenced`, which say whether it sits in an inline-code span or a fenced block.
   A placeholder in a retired form is always an issue, shown or not: the fix is `python {skillGroups.common}\scripts\placeholders.py convert <file>`, which converts it in the file and its twin.
9. **Prompt Examples** — is there at least one `/`-invocation example, does one show `run step N` where the skill honours it, and does the workflow actually parse what the examples show?
10. **Step Purposes** — does `README.md`'s `## Step Purposes` list every `## Step N` of `SKILL.md`, named exactly as its heading and in its order, each with its Purpose indented beneath?
    Read `readme_shape.step_purposes`: `steps_missing`, `items_not_steps`, `items_without_purpose` and `order_ok`.
    A step left out or misnamed, or one with no Purpose, is an issue: the Purpose is the one record of why the step exists, and [skill-writing.md](.github/common/rules/skill-writing.md) puts it there and nowhere else.
    Judge what it says too: a Purpose that restates the step's instructions instead of saying why the step exists *as a step* is a recommendation, since skill-writing.md calls that a second copy that will drift.
11. **What a run does not need stays out of `SKILL.md`** — does `SKILL.md` still hold a `# Dataflow` or `# Steps at a Glance` section, a `- **Purpose**:` line, or the paragraph that introduces the Purposes, and does it link to `README.md`?
    Read `readme_shape.readme_content_in_skill_md`: `found` and `links_to_readme`.
    Each is an issue: every run loads the whole `SKILL.md`, a second copy beside the one in `README.md` drifts from it, and a link leads a run into a file that holds nothing a run needs.
    The fix moves the content into `README.md`, or deletes it when `README.md` already holds it.
12. **Files Each Step Uses** — does `README.md`'s `## Files Each Step Uses` answer the scripted-versus-not rule once, in a bold sentence, and name every step exactly as its heading in its tree?
    Read `readme_shape.files_each_step_uses`: `answers_scripted_rule`, `steps_missing` and `items_not_steps`.
    A step left out or misnamed is an issue: a reader matching the tree to the Workflow either cannot find the step or finds a different one.
    A missing answer is a recommendation, since the steps still say what each one runs.
13. **Tracked dependencies** — is every file that `README.md`'s header quote declares still as it was when it was recorded?
    Read `readme_shape.header_quote`: each entry carries the status `depends_on.py check` gives it.
    A `MISSING` entry is an issue: the link names no file, so the dependency it declares is not tracked at all.
    A `CHANGED`, `NO_RECORD` or `NOTHING_CITED` entry is a recommendation: a file the skill depends on changed, or was never confirmed, since anyone checked that the skill still holds — the fix is to read what changed, bring `SKILL.md` and `README.md` in line, and record it again with `depends_on.py record`.
    A `README.md` with no header quote, or one whose header quote `depends_on.py` cannot read (`error`), is an issue: every skill depends at least on its two templates and skill-writing.md.
    Never judge a fingerprint by eye; the status is the script's.
14. **The README's twin** — when `SKILL.md` has a 繁體中文 twin (`readme_shape.skill_has_twin`), does `README.md` have one too (`readme_shape.has_twin`)?
    A missing `README-tw.md` is a recommendation: [skill-writing.md](.github/common/rules/skill-writing.md) asks for it, but the skill runs the same without it.

## 2. Config conformance

**Why it exists** — it makes the workspace's single source of truth enforceable: a path that should have come from `config.yaml` reads perfectly well in prose and only shows itself when something goes looking for it.

`config.yaml` is the single source of truth for `wikiDir` and `skillGroups`.
A skill that needs either must resolve it in Step 0 rather than hardcode it.
**Not every literal path is a defect** — `checkpoints\`, `database\` and `packages\` live inside the workspace and are correctly written literally, and a Markdown link target such as `](.github/common/rules/report-md-rules.md)` is the project's own link convention: the link has to resolve on disk, so it is written literally on purpose and is never a finding.

Its subject is the **whole skill directory**, not just `SKILL.md`.
Criteria 1-6 judge the `config_shape` facts of `SKILL.md`; criteria 7-8 judge the `dir_config_shape` facts of every other text file in that directory — the scripts, the references, the 繁體中文 twin and the skill's own `config.yaml`.
A path baked into a script breaks exactly as one baked into a step does, and nothing else in a run opens those files.

1. **`wikiDir` resolution** — if the skill reads or writes anything in the wiki vault, does Step 0 resolve `wikiDir` from `config.yaml`?
2. **Hardcoded wiki paths** — does any body step use a literal `wiki\<skill>\` path instead of `{wikiDir}\<skill>\`?
   This is an issue: the vault root is configurable and lives outside the workspace, so a literal path writes to the wrong place.
3. **Unresolved placeholders** — does the skill use `{wikiDir}`, `{vaultName}` or `{skillGroups.<group>}` anywhere without Step 0 resolving it?
   A placeholder that is never resolved is an issue.
4. **`skillGroups` resolution** — does the skill reach its own directory, or another skill's, through `{skillGroups.<group>}` rather than a literal `.github\...`?
   A hardcoded `.github\` path breaks as soon as the skill moves between groups.
5. **Absolute paths** — is a machine-specific absolute path (e.g. `C:\Users\...`) baked into the SKILL.md where a config key or a workspace-relative path belongs?
6. **Group placement** — does the skill sit under the `skillGroups` root its content implies: project-agnostic in `common`, project-specific in `dedi`, imported third-party in `external`?
7. **Hardcoded paths outside `SKILL.md`** — does any script, reference, twin or other file under the skill directory bake in a literal wiki path, a machine-specific absolute path (`C:\Users\...`, `D:\...`), a UNC share (`\\host\share\...`) or a literal `.github\` path?
   Read `dir_config_shape.hardcoded_paths`; each fact carries its `file`, `kind` and `line`.
   A path the file **uses** — a default, a constant, a fallback — is an issue: it is invisible from `SKILL.md`, so no other criterion can reach it.
   A path the file merely **shows** is not a finding, which `commented`, `fenced` and `backticked` settle — a usage example in a module docstring, a `--help` string or a fenced block is documentation, and a placeholder host (`\\host\share`) is documentation even where those flags are false.
8. **Site-specific values belong in the skill's own `config.yaml`** — when `dir_config_shape.has_own_config` is true, a share root, a host, a vault path or a lab-specific directory is correct *there* and a defect anywhere else.
   A script that names such a path itself instead of reading it from that config or taking it as a CLI argument is an issue even while the value is right: the next machine needs a code edit rather than a config edit.
   When the skill has no `config.yaml` of its own, the value belongs in the workspace `config.yaml` or in an argument; read each file's `reads_config_yaml` lines to tell one that resolves its paths from another that bakes them in.

## 3. Description accuracy

**Why it exists** — it checks the only text read before the skill is chosen, which no structural check can reach; a perfectly shaped skill with a wrong description is one that never gets selected at all.

**The description is the claim; the workflow is the ground truth.**

- **The workflow is authoritative.**
  When the description and the steps disagree, it is the description that is wrong — never report the workflow as needing to change to match the description.
- Judge **accuracy and coverage, never style**.
  Wording, tone and sentence structure are the author's call, and so is length below the 1024-character limit criterion 1.1 enforces.
  Report a finding only where the description claims something the workflow does not do, or omits something the workflow always does.
- The `description` is the only part of a `SKILL.md` read during skill *selection* — the body is read only after the skill is chosen.
  An omission here costs the user a skill that never gets picked, so weigh findings by that cost.
- Quote **both** the description's claim and the step that contradicts or omits it.
- **A fix must never push the description over that limit.**
  Naming an unstated output or action lengthens it, and a description over the limit costs what criterion 1.1 says — a worse defect than the omission it fixes.
  When there is no room, the fix names what to cut to make room.

1. **Overstated** — does the description claim an input, action or output that no step performs?
   This is an issue: it gets the skill selected for work it cannot do.
2. **Unstated output** — does the skill always write something the description never names?
   Compare against every output the MUST FOLLOW contract declares — MD report, YAML checkpoint, data store, HTML page.
3. **Unstated action** — does a step do something material the description omits, such as writing to ADO, connecting to a host, triggering a pipeline, sending mail, or mutating a shared file?
4. **Stale** — does the description still describe behaviour a step has since changed, such as a renamed output directory or a dropped argument?
5. **Trigger coverage** — would a user asking in plain language for what this skill does actually match this description?
   Name the phrasing that would fail to match.

## 4. Terminology usage

**Why it exists** — it holds the glossary to account: a term is only worth defining if the prose actually uses it, and nothing else in a run compares a definition against its use.

- Judge prose only.
  A term's lowercase form inside a **data key** (`store_file`, `stored`), a **CLI flag** (`--share-root`), a **user-facing string**, or a **code identifier** is correct as written — never report it.
- A variant is only a defect when it means the **same thing** as the term.
  Confirm the referent first — the same words can name a different object, and capitalising them would then invert the meaning.

1. **Literal instead of term** — does a section name the raw artefact where a term is defined for it (e.g. `process.yaml` where **YAML checkpoint** is defined)?
   The glossary entry that introduces the literal keeps it; every other prose use should be the term.
2. **Wrong term** — does a section use one term where another is meant (e.g. naming the directory when the thing referred to lives *inside* the file)?
   This is an issue, not style: it misstates the referent.
3. **Variant spelling** — is a defined term written in a different case or form (`store file` for **Store file**, `launched run` for **Launched run**)?
4. **Restated definition** — does a section re-explain what a term means instead of using it?
   The glossary owns the definition; a step that repeats it will drift from it.
5. **Unused term** — is a term defined but never used outside the glossary?
   Either the prose should use it, or the term should go.
6. **Heading consistency** — do table column headers and section names use the terms they refer to?

## 5. Cross-platform compatibility

**Why it exists** — a command that works on the author's machine reads identically to one that works everywhere, and nothing else in a run ever executes the commands, so this is the only pass that asks whether they would survive a different shell.

A skill and the tools or commands it and its Python scripts invoke must run on Windows, macOS and Linux — or say which platform they assume.

- Judge commands the skill **invokes**, not commands it merely **shows**.
  A command in a fenced block or an inline-code span that a step tells the agent to run is in scope; a command quoted as an example of what not to do is not — read `backticked` and `fenced` together with the surrounding prose.
- **A declared platform is not a defect.**
  A skill that states it runs on one platform only — one built on Outlook COM automation or a Windows Scheduled Task says so plainly — keeps its `powershell` and `cmd` commands without a finding.
  Judge the undeclared assumption, never the declared one.
- Severity: an **issue** when the skill would fail outright on one of the three platforms without saying so; a **recommendation** when a portable alternative exists and the current form merely narrows where the skill can run.

1. **Shell commands in steps** — does a command a step runs use a platform-specific builtin (`copy`, `dir`, `type`, `del`, `move` on Windows; `open`, `pbcopy`, `osascript` on macOS) without naming the equivalent on the other platforms, or stating the platform it assumes?
2. **Path separators in executable commands** — does a command the agent must execute carry `\` separators?
   A backslash path is correct in Windows shells, batch files and config values, but breaks in bash/zsh.
   Paths in prose are `Config conformance`'s subject — this criterion judges paths inside executable commands only.
3. **Script subprocess use** — does a Python script the skill names shell out through `os.system`, `subprocess.run(..., shell=True)` or a platform-specific binary, where `pathlib` plus a `subprocess` argument list would do?
   `shell=True` is an issue: it ties the script to one shell's quoting rules and builtin set.
4. **Platform-specific Python APIs** — does a script call `os.startfile`, `win32com`, `ctypes.windll`, AppleScript or similar without a per-platform branch or a stated platform requirement?
5. **External tools assumed present** — does the skill or one of its scripts require a tool that is not standard on all three platforms (`powershell`, `pbcopy`, `xdg-open`, a GNU-only `sed`/`date` flag) without naming the requirement and, where one exists, the portable alternative?

## 6. Dataflow

**Why it exists** — a skill's Dataflow is the one place that shows at a glance what every step reads and writes, so it is read instead of the steps; nothing else in a run compares the drawing with the steps, and a Dataflow that has drifted from them misleads exactly where it is relied on.

The Dataflow is the `## Dataflow` of the skill's `README.md`, and every line a finding cites is a line of that file (`dataflow.file`).
It is judged against [DFD.md](.github/common/references/DFD.md) — its kinds of data, its shapes, its lines and the two defects any DFD is read for — and against the steps of `SKILL.md`; the README template's `## Dataflow` shows how it is laid out.
A Dataflow left in `SKILL.md` is criterion 1.11's to report, never this check's.

- **The steps are what runs.**
  Where the diagram and a step disagree about what the step reads or writes, the diagram is what changes — unless the step itself breaks a rule the diagram is read for, such as a record with a second writer, and then the finding is against the step.
- **Only what a step reads or writes at run time is an edge.**
  A document a step only cites — a rules file it follows, a section it names — is not data the step reads, and leaving it off the diagram is not a finding.
- Severity: an **issue** when the diagram states something false or leaves out something that runs — a step, a read, a write, a writer; a **recommendation** when only the notation is off and nothing it states is false — a colour, a line of the legend.

1. **Every step, named exactly** — is every `## Step N` of the Workflow a step in the diagram, named exactly as its heading, number included, and is nothing drawn as a step that is not one?
   Read `steps_not_drawn` and `processes_not_steps`.
   A step left out or misnamed is an issue: a reader matching the drawing to the Workflow either cannot find the step or finds a different one.
2. **Shapes and lines** — is the Dataflow drawn as a mermaid flowchart, with a legend beneath it that says what each shape and each kind of line means?
   Is every node drawn in the shape of its kind, as DFD.md gives them — an external input a parallelogram, one-run data a flag, a record a cylinder, a step a rounded box, or a double-edged box for a step that runs a program of an RSDC system, and a role outside the skill a hexagon?
   Is an arrow blue exactly when its data is written into a record or turned into a record's content, and does no solid arrow join two pieces of data directly?
   Read `mermaid_blocks`, `nodes`, `edges`, `edges_between_data` and `legend_lines`.
   A Dataflow with no diagram is an issue, since there is nothing to read; so is a shape that misstates its node's kind, since the shape is what tells a reader whether the data outlives the run; and so is a solid arrow between two pieces of data, since it draws data moving with no step to move it.
   A colour or a legend that is off is a recommendation.
3. **Agreement with the steps** — does what the diagram says each step reads and writes match what the step's own section reads and writes at run time?
   Compare each step's section with its arrows.
   A gap either way is an issue: a read the diagram leaves out is data whose source nobody drew, and a write it leaves out is a record whose writer nobody sees.
4. **One writer per record** — does every record have exactly one writer: each data file in the Checkpoint Dir, each `step_{N}` group of the YAML checkpoint, each section of the MD report?
   Read `multi_writer_records`, and `records_edited_in_turn`.
   A record that a later step writes without reading it is an issue, whether the diagram draws it or the steps do it: re-running one of them silently erases the other's result.
   A record every later writer also reads — the two-headed arrow — is edited in turn, and is no defect (DFD.md); judge only what re-running its first writer does to the edits after it, and make it a recommendation when the steps do not say, such as a first writer that overwrites without asking while the later steps are not run again.
5. **No data without a source** — is every piece of data a step reads an external input, supplied by a role outside the skill, or written by some step?
   Read `unsourced_data`.
   Data nothing supplies is an issue: nobody is responsible for producing it, and it is found only the first time it is missing.
6. **No read of a later write** — does any step read what a later step writes?
   Read `reads_of_later_writes`.
   Every entry is an issue: it is a forward reference made in data, the same defect criterion 1.7 judges in the prose of the steps.
   Read `records_read_as_found` too: each is a record whose first writer reads it, so the steps before that writer read it as it was found, and the scanner leaves them out of `reads_of_later_writes`.
   Confirm that the record exists before the run begins, as a file the run edits does, such as the skill it works on; where the run creates it, those steps read a record nothing has written yet, and each is an issue after all.
