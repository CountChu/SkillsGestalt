---
name: compile-skill
description: >-
  Compiles one skill's SKILL.md workflow into skill.py, a headless Python CLI beside it, so steps a
  program can do run without an LLM and stop costing tokens. It has no design of its own - the
  compile SOP in its references decides what a compiled script must be: how each step is
  classified (deterministic or cognitive, automated or interactive), the click CLI that runs one
  step by identifier via --step, the hidden --export-schema JSON a caller reads, and the
  exit code a cognitive step hands off with instead of calling an LLM. A source that is not
  skills/<name>/SKILL.md with Step N headings under its Workflow is refused with nothing written.
  The source is never edited; skill.py is the only output - no MD report, no YAML checkpoint. Every
  run ends by running it: a check of its source fingerprint, schema, handoffs and headless rule, then each
  deterministic step on a side-effect-free input. Triggers "compile this skill", "make skill.py",
  "run a skill without the agent".
---

# TERMINOLOGY

Terms that mean the same thing in every skill.

- **`run step N`** — a trailing prompt selector naming one step.
  It runs **only** that step, then stops.
- **MD report** — the Markdown report a skill writes into the wiki vault, in a folder named after that skill, carrying the standard header (Skill, Checkpoint, Created, Updated, Prompt) above its result sections.
- **YAML checkpoint** — the `process.yaml` in a skill's per-run checkpoint directory.
  Every step writes its outputs there under a `step_{N}` group, so a later step reads them back instead of recomputing them.
- **no forward-reference** — the rule that a step must never depend on a step that comes after it.
  Naming a later step to route control flow does not break it; borrowing that step's output does.

# DEDICATED TERMINOLOGY

Terms specific to this skill's domain.
The glossary owns each definition — a step uses the term rather than restating what it means.

- **compile SOP** — `SKILL-Compile.md`, in this skill's `references\`: the agent's judgments in a compile, Step 1 to Step 4 after its *Terms and Rules* — classifying the **Step Actions**, writing the **Compiled Script**, correcting it, and judging what its runs produced.
  It decides what a **Compiled Script** must be, and each of its steps opens with the input it works from.
  This skill runs every program, hands the **compile SOP** its inputs, and adds what a run needs around them: the **target skill**, the questions put to the user, and what is displayed.
  A step of it is cited here by number and heading, e.g. **compile SOP** Step 1 *Classify the Step Actions*, so that it is never mistaken for a step of this skill.
- **target skill** — the skill this run compiles, named on the prompt by its directory name or by the path of its `SKILL.md`.
- **Skill Source** — the **target skill**'s `SKILL.md`, in the sense of the **compile SOP**'s *Terms and Rules*.
- **Compiled Script** — the `skill.py` this run writes beside the **Skill Source**, in the same sense.
  It is this skill's only output.
- **source fingerprint** — the fingerprint of the **Skill Source** that a **Compiled Script** records, in the sense of **compile SOP** Step 2 *Write the Compiled Script*, which also says what a stale **Compiled Script** does.
  Step 1's script computes it.
- **Step Action** — one step of the **Skill Source**'s `# Workflow`, in the sense of the **compile SOP**'s *Terms and Rules*, run by its **step identifier**.
- **step identifier** — what a **Step Action** is addressed by, derived from its `## Step N` heading as **compile SOP** Step 1 *Classify the Step Actions* specifies.
- **Step Action type** — one of the four Action types of **compile SOP** Step 1 *Classify the Step Actions*.
  Its table owns what each one means; this file never restates it.
- **handoff step** — a **Step Action** of either cognitive type, which the **Compiled Script** ends with the handoff of **compile SOP** Step 2 *Write the Compiled Script*.
- **step inventory** — what the **Source Scanner** lists for a **Skill Source**, in the sense of the input of **compile SOP** Step 1 *Classify the Step Actions*.
- **Agentic Panel** — a user interface that would drive a **Compiled Script** as a caller, in the sense of the **compile SOP**'s *Terms and Rules*.
  The **compile SOP** does not name it; this skill never writes it.
- **Source Scanner** — the program that judges whether a **Skill Source** can be compiled at all, and prints its **step inventory** and **source fingerprint**; Step 1 runs it.
- **Contract Checker** — the program that checks a **Compiled Script** against its contracts, running it only as a caller does and reading its text; Step 3 runs it.
- **side-effect-free input** — an input of the kind **compile SOP** Step 4 *Prove the Steps* chooses for a step, to reach the step's branches: an empty date range, an ID with no children, a host not in inventory.
- **core work** — in the sense of the **compile SOP**'s *Terms and Rules*.
  Whether a step's work that runs no program is core work, the user decides from Step 2's menu.
- **chore** — in the same sense: the kind of that work that is not core work.

# CONFIGURATION

Concrete values this skill runs with.

- **compile SOP** — [SKILL-Compile.md](.github/common/skills/compile-skill/references/SKILL-Compile.md), in `{skillGroups.common}\skills\compile-skill\references\`.
- **Skill Source** — `{skillGroups[<group>]}\skills\<skill-name>\SKILL.md`, resolved in Step 0 from the name or path the prompt gives.
- **Compiled Script** — `skill.py`, in the **Skill Source**'s own directory (the **compile SOP**'s *Terms and Rules*).
- **Source Scanner** — `{skillGroups.common}\skills\compile-skill\scripts\scan_source.py`.
- **Contract Checker** — `{skillGroups.common}\skills\compile-skill\scripts\check_compiled.py`.

# MUST FOLLOW

- Must run workflow step by step, and display each step number.
- Each step must be self-contained.
  **No forward-reference.**
- A step that a program can do deterministically must be run as a script.
  A step that needs reading, judgement, or summarization **must not** be scripted — write it as natural-language instructions for the agent to perform directly.
- **Honour a `run step N` selector**: run Step N, then stop; never a later step.
  This skill writes no YAML checkpoint, so each step re-derives its inputs from the prompt and from the files on disk — which it can, because the **Skill Source** and the **Compiled Script** are the only state any step needs.
- **This skill produces neither an MD report nor a YAML checkpoint.**
  The **Compiled Script** is its only output.
- Follow [scratch-rules.md](.github/common/rules/scratch-rules.md) for where a run's throwaway files go and how they are cleaned up.
- **This file runs every program; the compile SOP runs none, and names neither a program nor this skill.**
  A step below runs the **Source Scanner**, the **Contract Checker** or the **Compiled Script**, and hands what they print and write to the **compile SOP** step it names, as that step's input.
  It is the lower document and this file the upper one: the **compile SOP** holds only the judgments a compile needs, and a **compile SOP** that named a program or this skill would know the system it is kept apart from.
- **Each step does the compile SOP steps it names, as the compile SOP writes them.**
  A step below adds only what a run needs around them — the programs, the **target skill**, the questions put to the user, and what is displayed — and never restates what they say: a rule copied into this file is a second copy, and the two will drift.
  Where this file and the **compile SOP** disagree, the **compile SOP** wins; report the disagreement rather than resolving it in the run.
- **The compile SOP's steps map onto this skill's**: its Step 1 and Step 2 are done in Step 2, its Step 3 in Step 3 when a check fails and in Step 4 when a difference lies in the script, and its Step 4 in Step 4.
  Where it says stop, the run ends there, with what it reports, and nothing more is written.
- **Never edit the compile SOP while compiling.**
  A change to what a **Compiled Script** must be is a change of its own, made deliberately and outside any run — never a side effect of compiling one skill.
- **Write only the Compiled Script.**
  Never the **Agentic Panel**, and never another file of the **target skill**.
- **Before the skill ends, display the Compiled Script path** — the path only, never its contents, rendered as a clickable Markdown link and never as inline code or plain text.
  Do this for every run, including a partial one such as `run step 0`.

# Prompt Examples


## Prompt 1

```
/compile-skill
report-skills
```

## Prompt 2

```
/compile-skill report-logs --force
```

## Prompt 3

```
/compile-skill
report-skills
run step 3
```

## Prompt 4

```
Compile the report-suts-usage skill into skill.py so I can run it directly.
```


# Workflow

## Step 0 - Warmup

- Run `.venv` first.
  The Step 1 and Step 3 scripts import `PyYAML`, and the **Compiled Script** needs the interpreter version and packages **compile SOP** Step 2 *Write the Compiled Script* names.
  Check every one of them, e.g. with `python --version` and `python -c "import click, yaml"`; if any is missing, stop and name it — never compile for a toolchain the script cannot run on.

- Read the workspace config [config.yaml](config.yaml) at the workspace root and resolve:
  - **`skillGroups`**: the group name -> skills-root map — a bare skill name resolves to `{skillGroups[<group>]}\skills\<skill-name>\SKILL.md`, and this skill's own directory is `{skillGroups.common}\skills\compile-skill\`.
  - Substitute the resolved values wherever `{skillGroups.common}` or `{skillGroups[<group>]}` appears in the steps below, including in commands.
  - If `config.yaml` is missing or `skillGroups` is absent, stop and ask the user.

- This skill calls no API of its own and needs no credential.
  Never prompt for one.

- Check if the below scripts/files exist before running workflow.
  - `{skillGroups.common}\skills\compile-skill\scripts\scan_source.py`
  - `{skillGroups.common}\skills\compile-skill\scripts\check_compiled.py`
  - `{skillGroups.common}\skills\compile-skill\references\SKILL-Compile.md`

- The prompt takes one of the forms shown in **Prompt Examples** above.
  Parse it for:
  - **target skill** (required): the first word after `/compile-skill`, on its line or the next, or the skill a plain-language prompt names.
    Either a bare skill name, resolved by looking for `<root>\skills\<name>\SKILL.md` under every `skillGroups` root, or a path ending in `SKILL.md`.
    A name that matches under more than one root is ambiguous: list the matches and ask which one, never pick the first.
  - **`--force`** (optional): overwrite an existing **Compiled Script** without asking.
  - **`run step N`** (optional): a trailing step selector.

- If the **target skill** is missing, ask the user for it.

- Confirm the **Skill Source** exists.
  Whether it is one this skill accepts is Step 1's verdict, not this step's.

- Confirm the **target skill** has stabilized, as the **compile SOP**'s *Terms and Rules* requires.
  Judge it from what is known — the user's word, or how recently the **Skill Source** was revised — and if it is still being revised, say so and ask whether to compile anyway.

- Derive the **Compiled Script** path: `skill.py` in the **Skill Source**'s directory.
  - If it exists, say so — but ask nothing yet: whether to overwrite it is a question for the moment it is about to be written, not for before the source has even been judged.
  - If it does not exist, a `run step 3` or `run step 4` has nothing to check — say so and stop.

- If a `main.py` sits beside the **Skill Source**, say so and leave it — this skill writes only `skill.py`, and removing another runner is the user's call.

- Display the resolved **Skill Source** path and **Compiled Script** path.


## Step 1 - Validate the Skill Source

- Run the **Source Scanner**, `scan_source.py`, on the **Skill Source** resolved in Step 0.
  - Example: `python {skillGroups.common}/skills/compile-skill/scripts/scan_source.py --file "{skillGroups.common}/skills/report-skills/SKILL.md"`

- Act on the exit code:
  - `0`, valid: continue, keeping the **step inventory** and the **source fingerprint** it printed.
  - `2`, `INVALID`: **stop the skill here** — report the reasons it printed, and write no **Compiled Script**.
  - `64`, no verdict — the command was malformed, or the file is missing or cannot be read: correct the command or the path, and run it again.

- Display the **step inventory** — number and title per step — and any warnings.


## Step 2 - Classify and Compile the Step Actions

- Work from the **step inventory** and the **source fingerprint** Step 1 printed.
  On a `run step 2`, re-derive them by running the Step 1 script again, and stop on an `INVALID` verdict exactly as Step 1 would.

- Read the whole **Skill Source**, then the whole **compile SOP**.
  Read it on every run — the **compile SOP**, not the memory of an earlier compile, decides the types and the shape of the script.

- Do **compile SOP** Step 1 *Classify the Step Actions*, giving it the **Skill Source**, the **step inventory** and, on a recompile, the existing **Compiled Script**'s docstring, with these for the user:
  - Show its classification as a **Classification table**, with columns **Step identifier**, **Title**, **Step Action type**, **Arguments**, **Program** — the program it calls, or the user's decision when it calls none — and **Why** — one line saying what decided the type.
    Its cognitive rows are the **handoff steps**: the steps this run will not compile.
  - Put each of its core work or chore questions to the user with a menu: one question per step, quoting what the step does, with these three options, one recommended and the reason given — on a recompile, the decision the existing **Compiled Script**'s docstring records:
    1. **Chore** — this skill writes it into the **Compiled Script**.
    2. **Core work** — the run stops.
    3. **Cognitive** — the classification was wrong, and the step becomes a **handoff step**.

- If the **Compiled Script** already exists and `--force` was not given, say so and ask whether to overwrite it before writing anything — with the **Classification table** in view, so the answer is given knowing what would replace it.
  A refusal ends the run with nothing written.

- Do **compile SOP** Step 2 *Write the Compiled Script*, giving it the classification, the user's decisions and the **source fingerprint** Step 1 printed, and writing to the path Step 0 derived.

- Display the **Compiled Script** path and its size.


## Step 3 - Check the Script Contracts

- Run the **Contract Checker**, `check_compiled.py`, on the **Skill Source** and the **Compiled Script**.
  - Example: `python {skillGroups.common}/skills/compile-skill/scripts/check_compiled.py --source "{skillGroups.common}/skills/report-skills/SKILL.md" --script "{skillGroups.common}/skills/report-skills/skill.py"`
  - It runs the script only in temporary places outside the workspace, and runs no deterministic **Step Action**'s real work: Step 4 proves that.

- Act on the exit code:
  - `0`, every check passed: continue.
  - `1`, at least one check failed: report each failing check with what it said, do **compile SOP** Step 3 *Correct the Script* with those checks as its input, and run this step again until it passes.
    Correct the script — never the **Skill Source**, and never the **compile SOP**.
  - `2`, the **Skill Source** is `INVALID`: stop, exactly as Step 1 would.
  - `4`, the script is stale: never fix it by writing a fingerprint into the script; in a whole run, go back to Step 1, and on a `run step 3`, stop and say that a whole run must recompile it.
  - `64`, no verdict — the command was malformed, or a file it names is missing or cannot be read: correct the command or the paths, and run it again.

- Report as not checked, never as passed, the rules **compile SOP** Step 2 *Write the Compiled Script* reviews the script against, and that the script was never edited by hand: no check here or anywhere else proves them.

- If a failure turns out to be a contradiction inside the **compile SOP** itself, say so plainly and leave it for the user to settle in a separate run.

- Display the result: how many checks passed, and the **Step Action** list the script printed.


## Step 4 - Prove the Deterministic Steps

- Run the **Compiled Script** on disk with `--export-schema`, and give the **Step Action** list it prints, with the **Skill Source**, to **compile SOP** Step 4 *Prove the Steps*: it chooses a **side-effect-free input** for each deterministic **Step Action**, or says why the step is not run.
  - Example: `python {skillGroups.common}/skills/report-skills/skill.py --export-schema`

- Run each step it chose, as it says, with the input it chose: `python <Compiled Script> --step <id>`, plus those arguments.
  Give each run's exit code, what it printed and what it wrote back to **compile SOP** Step 4 *Prove the Steps*, which judges it.

- Where it judges a difference to lie in the script, do **compile SOP** Step 3 *Correct the Script* with that difference as its input, do Step 3 again, then repeat this step.

- Display:
  - The command that runs one **Step Action**: `python <Compiled Script> --step <id>`, plus the arguments that step declares.
  - A **Result table** with columns **Step identifier**, **Step Action type** and **Result** — `passed` with what it produced, `not run` with why, or `handoff` for a **handoff step**, naming the source step the user or an agent must perform there.

- Close with the **Compiled Script** path as a clickable Markdown link.
