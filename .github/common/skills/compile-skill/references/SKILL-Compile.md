# Skill Compiler - Compile SOP

The judgments that compile one Skill Source into a Compiled Script: classifying its steps, writing the script, correcting it, and judging what its runs produced.
Each step opens with its input, and starts once that input is given.

## Terms and Rules

- **Skill Source** — a skill's `SKILL.md`, directly inside the skill's own directory, whose parent directory is named `skills`: `skills/<name>/SKILL.md`.
- **Compiled Script** — `skill.py`, in the same directory as its Skill Source: a headless Python program that runs one Step Action at a time, or describes them all.
- **Step Action** — a step declared under the Skill Source's `Workflow` section by a heading such as `Step 0`, `Step 1` or `Step 2`.
- **Caller** — whoever runs the Compiled Script: a person at a terminal, a user interface with a person behind it, a scheduler, or an agent.
- **Person compiling** — whoever asks for a skill to be compiled, and decides what compiling leaves to a person.
- **Person revising the skill** — whoever writes and revises the Skill Source, by hand.
- **Input variable** — a value a Step Action takes from its caller for one run, declared with its name, whether it is required, its prompt text and its data type.
- **Handoff** — what a Cognitive step ends in instead of being run: control returns to the user or agent, who performs that step through the skill itself.
- **Introspection** — the Compiled Script describing its Step Actions, the Action type of each and the input variables each takes, while running none of them.
- **Core work** — work on the skill's own data, which must already be a program the skill runs.
- **Chore** — upkeep that shared rules or the step's own text fully specify, such as reading configuration, parsing the request or writing a checkpoint.
- **Stale** — said of a Compiled Script whose recorded fingerprint is missing, or differs from that of the Skill Source beside it.

Rules for every step:

- Compile only a skill whose workflow has stabilized; a skill still being revised is run as a skill.
- Never change the Skill Source.
- Write the Compiled Script whole, and no other file of the skill.
- Never edit a Compiled Script by hand: a change enters through the Skill Source, and reaches the script only by compiling again from Step 1.
- The fingerprint a Compiled Script records is the one given to Step 2; never write any other.
- When the script is stale, when Step 4 finds a gap in the source, or when the script's results deviate too far from what was expected, the person revising the skill revises it and runs it as a skill until it is stable; then compile it again from Step 1, and write the script whole.
- The Compiled Script never calls an LLM, and never waits for a person.
- A Compiled Script that has not passed every contract check and Step 4 is not finished, and nothing relies on it.
- A step that says stop ends the compile.

## Step 1 - Classify the Step Actions

**Input**: the Skill Source; its **step inventory** — each Step Action's identifier, title and line span, and every program file name in its inline code or fenced blocks, whether the step runs it or only mentions it, each marked as in the skill's directory or not; and, on a recompile, the existing Compiled Script's docstring.

- Read the whole Skill Source.
- Give each Step Action its identifier: the number of its `Step N` heading, without leading zeros.

Give each Step Action exactly one Action type, where the Cognitive dimension crosses the Execution dimension:

| Cognitive \ Execution | Automated | Interactive |
| :---- | :---- | :---- |
| **Deterministic** | `deterministic_automated`: local logic, no token cost, done in one action | `deterministic_interactive`: local logic, no token cost, done once a person has given its values |
| **Cognitive** | `cognitive_automated`: needs an LLM; the script hands it off | `cognitive_interactive`: needs an LLM working with a person; the script hands it off |

- Judge the Cognitive dimension by what the step's result needs, not by how its instructions read.
  Reading, parsing, computing, rendering, or calling a service that a program can call is Deterministic.
  A call made through an interface only an agent can use is Deterministic when the same call can be made without an LLM — through the service's own interface, an existing helper, or a library — and Cognitive only when no such route exists.
  A semantic judgment that needs an LLM is Cognitive.
- Judge the Execution dimension by the step's inputs.
  A step that takes a value from a person, given with the request or asked for, is Interactive; a step that needs nothing it cannot read for itself is Automated.
- Make each value a step takes from a person one of its input variables, with the kind of value it takes, and required when the Skill Source gives it no default.
  A Deterministic Automated step requires no input variable, and a Deterministic Interactive step declares at least one.
- Split a step whose instructions mix Action types into `N.1`, `N.2`, … in source order, each of exactly one type, and never address it as a whole after that; every other step keeps `N`.
- For each Deterministic step, take the programs it runs from the step inventory, leaving out a name the step only mentions; compile the step into a call to those same programs, and never rewrite one.
- Never approximate a Cognitive step by deterministic logic.
- For each Deterministic step part of whose work runs no program, ask the person compiling whether that work is core work or a chore, one step at a time.
  On a recompile, offer the decision the docstring records as the default.
  Never decide it alone, and stop when a question is left unanswered.
- When work is judged core work with no program, stop, write nothing, and list those steps, each with what it needs a program for, for the person revising the skill to write as programs the skill runs.
- Show the classification before any code is written: each Step Action's identifier, title, Action type, input variables, the program it calls or the person's decision, and what decided the type.

## Step 2 - Write the Compiled Script

**Input**: the classification of Step 1, with the person's decisions, and the fingerprint of the Skill Source content that was classified.

Write `skill.py` beside the Skill Source, whole.

**What it records**

- `SOURCE_SHA256` — a module-level constant, assigned a plain string literal: the fingerprint given as input, 64 lowercase hexadecimal digits.
- `COMPILED_AT` — a module-level constant, assigned a plain string literal: the ISO 8601 date-time of the compile, with its UTC offset.
- The module docstring — the Skill Source's `description`, then every Step Action with its identifier and type, the command that runs one, and, for each Deterministic step whose work runs no program, that a person judged it a chore.

**How it is run**

- `python skill.py --step <id> [--<name> <value> ...]` runs the one Step Action whose identifier is `<id>`, each of its input variables given as an option named after it.
- `python skill.py --export-schema` prints the introspection metadata and runs no step.

**What every invocation does, in order**

1. In every invocation, `--export-schema` included, take the fingerprint of the `SKILL.md` in the script's own directory — the lowercase SHA-256 hex digest of its text, decoded as UTF-8 with any byte-order mark removed and every line ending normalized to LF, then re-encoded as UTF-8 — and compare it with `SOURCE_SHA256`.
   When the two differ, or the `SKILL.md` is missing, write to standard error that the script is stale and must be recompiled, print nothing on standard output, and exit `4`.
2. Read the command line with `click`: a missing required option, or a value its parameter type rejects, exits `2` before any work is done.
3. With `--export-schema`, print the introspection metadata on standard output as one JSON document and nothing else, then exit `0`.
4. With `--step <id>`, run the Action Logic Builder of that step; an identifier that names no step exits `2`.
   A Cognitive step's builder prints the handoff message and exits `3`; a Deterministic step's builder does the step's work and exits `0`.

**How it ends**

- Exit status: `0` success; `2` refusal, before any work is done, naming what was wrong — a required input missing, a value of the wrong kind, or an identifier that names no step; `3` handoff, after the handoff message; `4` stale, with nothing on standard output.
- The handoff message: `This step is a cognitive task and cannot be processed by this system. Please have the user or Agent invoke the corresponding Skill separately.`

**The introspection metadata**

One JSON document, in this form:

```json
{
  "skill_name": "example_skill",
  "steps": [
    {
      "id": "1.1",
      "name": "Fetch raw data",
      "type": "deterministic_automated",
      "description": "Run a local Python web crawler to fetch data",
      "arguments": []
    },
    {
      "id": "1.2",
      "name": "Analyze article sentiment",
      "type": "cognitive_automated",
      "description": "Call an LLM to classify text sentiment; this system only provides a handoff prompt",
      "arguments": []
    },
    {
      "id": "1.3",
      "name": "Set export path",
      "type": "deterministic_interactive",
      "description": "Requires the user to specify a local backup directory",
      "arguments": [
        {
          "name": "output_path",
          "required": true,
          "type": "path",
          "description": "Target path for export"
        }
      ]
    },
    {
      "id": "2.0",
      "name": "Human creative review",
      "type": "cognitive_interactive",
      "description": "A human and AI jointly review revision suggestions; this system only provides a handoff prompt",
      "arguments": []
    }
  ]
}
```

Its fields:

| Field | Meaning |
|---|---|
| `skill_name` | the `name` in the `SKILL.md` frontmatter, or the skill's directory name when the frontmatter has none |
| `steps` | every Step Action of the Skill Source, in source order, and no other: the identifiers `--step` accepts |
| `steps[].id` | the step identifier |
| `steps[].name` | a human-readable name for the step |
| `steps[].type` | the Action type: `deterministic_automated`, `cognitive_automated`, `deterministic_interactive` or `cognitive_interactive` |
| `steps[].description` | a human-readable description of the step |
| `steps[].arguments` | each input variable the step takes |
| `arguments[].name` | the input variable's name |
| `arguments[].required` | whether it is required |
| `arguments[].type` | its data type: `string`, `integer`, `number`, `boolean` or `path` |
| `arguments[].description` | its prompt text |

Spell every field name and code label exactly as above.

**How it is written**

- Python 3.10 or later, from the workspace's `.venv`, with type hints on every function, and its command-line interface built with `click`.
- Read every file as UTF-8, with any byte-order mark removed.
- Give each input variable's option the `click` parameter type that matches its `type`: `click.Path` for `path`, and `str`, `int`, `float` and `bool` for `string`, `integer`, `number` and `boolean`.
- Declare `--export-schema` with `hidden=True`; when it is given, print the metadata with Python's built-in `json.dumps()`, then call `sys.exit(0)`.
- Raise an identifier that names no step as `click.BadParameter`; every refusal exits with `click`'s usage-error status, `2`, before any work is done.
- Never call `input()`, `click.prompt()` or anything else that waits for a person.
- Take every input variable as an option; read a credential only from the environment variable or key store the Skill Source reads it from, never from the command line, and never ask for it.
- Resolve the workspace from the current working directory, where the workspace configuration file sits, never from the script's own location.
- Write one Action Logic Builder for each Step Action: it calls the program the skill's step runs, does the work a person judged a chore, or hands a Cognitive step off.
  A builder never calls another step's builder, and keeps nothing in memory for a later invocation.
- Each Deterministic step writes exactly what the skill's step writes — the same files, names, places and structure — and finds what earlier steps produced only in what they persisted or in the files they read.
- A Cognitive step contains no LLM call: it ends in the handoff.

**Review it**

When the script is written, review it against these rules: each step has the Action type Step 1 gave it; a Cognitive step contains no LLM call; no credential is taken from the command line; the workspace is resolved from the working directory; each option's `click` type matches its declared `type`; the docstring opens with the description and lists every Step Action.

## Step 3 - Correct the Script

**Input**: the contract checks the Compiled Script failed, each with what it found; or a difference Step 4 judged to lie in the script.

- Write the script again, whole, as Step 2 writes it, correcting what the input names.
- Never change the Skill Source to make a check pass or a step agree.
- Review the corrected script as Step 2 does.
- The corrected script is checked again from the first contract check, and Step 4 proves its steps again from the start.

## Step 4 - Prove the Steps

**Input**: the Step Actions the Compiled Script's introspection metadata lists, with the Skill Source; then, for each run, its exit status, what it printed and what it wrote.

- For each Deterministic step, in source order, choose an input that changes nothing shared — such as an empty date range, an ID with no children, or a host not in inventory — with the input variables its metadata declares.
- Never choose a step's defaults when the source takes required inputs or drives a live integration.
- Choose no input for a step that would change shared state — writing to a service, sending mail, pushing or deleting — and report it as not run, with the reason.
- Each chosen step runs once, from the workspace, as a separate invocation, the way a caller does.
- Compare what each run produced with what its source step says it produces — the files, their names and places, and the sections and fields in them — and quote what came back.
- Give each step one result: passed, with what it produced; not run, with the reason; or a difference, with where it lies; a Cognitive step's result is the handoff.
- A difference in the script — it breaks a contract, or a step produces something its source step does not say: give it to Step 3.
- A difference in the source — a step that does not say what it produces, or says it ambiguously: stop, and give the finding to the person revising the skill; never patch the script to cover it.
