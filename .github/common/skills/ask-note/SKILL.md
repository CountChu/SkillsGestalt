---
name: ask-note
description: >-
  Answers a natural-language question from the notes in one directory of the Obsidian vault -
  deriving the Search Terms the question implies (including the words the notes actually use, not the
  question's), scanning every note section for them, reading the sections that
  hit, and answering from those sections alone - then closing with an Evidence Table naming the note,
  section, line range and date behind every claim, plus the sections it looked at and rejected. The
  notes directory is an optional first line and defaults to write-note. It reads the vault and
  nothing else: it calls no API, writes no MD report, no YAML checkpoint and no file of any kind, and
  it never edits a note. Triggers "ask my notes", "what do my notes say about", "/ask-note".
---

# TERMINOLOGY

Terms that mean the same thing in every skill.

- **no forward-reference** - the rule that a step must never depend on a step that comes after it.
  Naming a later step to route control flow does not break it; borrowing that step's output does.

# DEDICATED TERMINOLOGY

Terms specific to this skill's domain.

- **Notes Dir** - the one directory of the vault this run reads, `{wikiDir}\{notesDir}\`.
  Parsed from the prompt; `write-note` when the prompt names none.
  Nothing outside it is read.
- **Question** - the natural-language question the run answers.
  It is answered from the **Notes Dir** alone.
- **Section** - a `## ` heading in a note plus the lines beneath it up to the next `## `.
  This is the unit the skill matches, reads and cites.
  The lines above a note's first `## ` are its header **Section**, numbered 0.
- **Search Term** - one string the scan looks for, compared case-insensitively.
  Step 1 derives them from the **Question**.
  Because the comparison ignores case, two terms differing only in casing are one term - never spend a term on that.
- **Hit** - one **Section** carrying at least one **Search Term**, together with its note, heading, line range, date and body.
- **Surviving Hit** - a **Hit** that Step 3 judged to actually bear on the **Question**, as opposed to one that merely shares a word with it.
  Only these may support the answer.
- **Evidence Table** - the table the last step displays: one row per **Surviving Hit**, naming where that part of the answer came from.

# CONFIGURATION

Concrete values this skill runs with.

- **Notes Dir** - `{wikiDir}\{notesDir}\`, where `wikiDir` comes from the workspace [config.yaml](config.yaml) (resolved in Step 0) and `notesDir` is the prompt's optional first line, defaulting to `write-note`.
  Never hardcode the vault root.

# MUST FOLLOW

- Must run workflow step by step, and display each step number.
- Each step must be self-contained.
  **No forward-reference.**
- A step that a program can do deterministically must be run as a script.
  A step that needs reading, judgement, or summarization **must not** be scripted - write it as natural-language instructions for the agent to perform directly.
- **This skill has no `run step N` selector - every run is a whole run.**
  Every step feeds the next, and with nothing persisted between runs there is no earlier output to resume from.
  Never invent a step selector for it.
- **This skill produces no MD report, no YAML checkpoint, and no file of any kind.**
  Everything it produces is displayed in the conversation.
  It never writes into the vault and never edits a note.
- **Answer from the Notes Dir and nothing else.**
  Never call an API, read a share, or fill a gap from earlier conversation or from memory.
  If the **Surviving Hits** do not answer the **Question**, say which part they leave open rather than completing it from elsewhere.
- **Every claim in the answer must be traceable to a row of the Evidence Table.**
  A statement no row supports must be cut or rewritten until a row supports it.
- **The Evidence Table is the last thing the run displays.**
  Nothing follows it.

# Prompt Examples


## Prompt 1

```
/ask-note
write-note
The most recent successful L5A5 pipeline
```

## Prompt 2

```
/ask-note
The most recent successful L5A5 pipeline
```

## Prompt 3

```
Look through my daily notes and tell me which BMC version I last flashed on X750, and where I wrote it down.
```


# Workflow

Each step opens with a **Purpose**: one sentence saying why that step exists as a step - what this skill would lose by folding it into its neighbour.

**Step 2 runs a script; Steps 0, 1, 3 and 4 do not**, because choosing what words to look for, judging which **Hits** bear on the **Question**, and writing the answer are all readings of meaning, while scanning a directory of notes for a fixed set of strings is not.

## Step 0 - Warmup

- **Purpose**: settle what the run reads and what it is being asked, so no later step has to guess either.

- Run `.venv` first.

- Read the workspace config [config.yaml](config.yaml) at the workspace root and resolve:
  - **`wikiDir`**: the vault root - the **Notes Dir** is a directory directly under it.
  - **`vaultName`**: the last path segment of `wikiDir` (e.g. `MyVault`) - the Obsidian vault name used to build the `obsidian://` links in Step 4.
  - **`skillGroups`**: the group name -> skills-root map - this skill's own directory is `{skillGroups.common}\skills\ask-note\`.
  - Substitute the resolved values wherever `{wikiDir}`, `{vaultName}` or `{skillGroups.common}` appears in the steps below (including in commands).
  - If `config.yaml` is missing or a needed key is absent, stop and ask the user.

- Check the below script exists before running the workflow.
  - `{skillGroups.common}\skills\ask-note\scripts\search_notes.py`

- The prompt takes one of the forms shown in **Prompt Examples** above.
  Parse it for:
  - **Notes Dir**: the line after the command, *only when* it names an existing directory under `{wikiDir}`.
    Otherwise there is no such line - the notes directory is `write-note` and that line is part of the **Question**.
    Resolve this by testing the path, never by guessing from the wording.
  - **Question**: everything after the command that is not the **Notes Dir** line, joined into one question.

- Verify the resolved **Notes Dir** exists and report how many `.md` files it holds.
  If it does not exist, stop and list the directories that are directly under `{wikiDir}` so the user can pick one.

- If the **Question** is empty, ask the user for it.

- Display the resolved **Notes Dir**, its `.md` count, and the **Question**.


## Step 1 - Derive the Search Terms

- **Purpose**: notes are written in their author's vocabulary, not the question's, so the gap between the two has to be closed deliberately before anything is scanned - a term never tried cannot be distinguished from a term that matched nothing.

- From the **Question**, write the list of **Search Terms**.
  Include:
  - **Every proper noun as the notes would spell it**, with each spelling variant worth trying.
    A **Question** naming `X75` must also search `X750`; one naming a person or a board must include the abbreviations and the full forms.
    Casing is not a variant - the scan ignores it, so `X750` and `x750` are the same term and listing both wastes one.
  - **The vocabulary the notes use for the concept**, not the **Question**'s.
    A **Question** about a *successful pipeline* must also search the words a note would actually carry - `passed`, `succeeded`, `Run:`, `buildId` - because a note recording a pass rarely uses the word the question used.
  - **Any identifier the Question names** in the shape a note would carry it: a work-item number, a PR number, a build id, a version string, a file name.

- Prefer over-generating.
  A term that matches nothing costs one scan; a term never tried can hide the answer entirely.
  Stop short only of terms so common they would mark nearly every **Section** as a **Hit** (`the`, `run`, `test` on their own).

- Display the **Search Terms**, grouped by what each is standing in for, so the user can add one before the scan.


## Step 2 - Scan the notes for the Search Terms

- **Purpose**: turning a term list into the exact set of sections that carry them is mechanical and total, and it is precisely the part that eyes skip - a section missed here is invisible to every step after it.

- Run the script `search_notes.py` with the **Notes Dir** and the **Search Terms**.
  - Example: `python {skillGroups.common}\skills\ask-note\scripts\search_notes.py --notes-dir "{wikiDir}\write-note" --terms X750 passed succeeded buildId`

- The script:
  1. Reads every `*.md` directly in the **Notes Dir** (non-recursive).
  2. Splits each note into **Sections** at every `^## ` heading, numbering the lines above the first heading as **Section** 0.
  3. Reads each note's date from its `- **Date**:` header line when present, else from the digits in its filename, else from its file mtime.
  4. Marks a **Section** as a **Hit** when any **Search Term** appears in its heading or body, compared case-insensitively.
  5. Prints JSON to stdout: the totals (notes read, sections read, hits, per-term match counts), then one object per **Hit** with `note`, `date`, `section`, `heading`, `startLine`, `endLine`, `matchedTerms` and `body` - newest note first.

- The script writes no file.
  Its stdout is the whole result, and it is the only input Step 3 has.

- Display the totals and the **Hit** headings only - never the bodies, which Step 3 reads.

- Display the per-term match counts, and call out any **Search Term** that matched nothing: that is the signal that the notes name the thing differently.

- If there are no **Hits** at all, return to Step 1 once with broader **Search Terms** and scan again before concluding the notes do not answer the **Question**.


## Step 3 - Read the Hits and answer the Question

- **Purpose**: a **Hit** is only a section that contains a word, and the difference between that and a section that answers the question is the whole reading this skill exists to do.

- Read each **Hit**'s `body` from Step 2's output.

- Judge every **Hit** against the **Question**: does it bear on it, or does it merely share a word with it?
  Keep the ones that bear on it as the **Surviving Hits**; set the rest aside for Step 4 and record how many were set aside.

- Answer the **Question** from the **Surviving Hits** alone, under these rules:
  - **Carry the note's own values over exactly.**
    Where a note states a number, a build, a date, a version or a command, reproduce it rather than paraphrasing it.
  - **Where two notes disagree, report both** and say which note is later.
  - **Where the Surviving Hits answer only part of the Question, answer that part and name the part they leave open.**
    A partial answer said plainly is correct; a whole answer completed from outside the notes is not.
  - **Never fill a gap from an API, a share, earlier conversation, or memory.**
    If the notes are silent, that silence is the finding, and it is worth reporting - a topic the notes never recorded is exactly what the user needs to know.

- Add a **Coverage** line stating: how many **Sections** across how many notes the answer rests on, how many **Hits** were set aside, and the date range the **Surviving Hits** span.

- Display the answer and the **Coverage** line.


## Step 4 - Display the Evidence Table

- **Purpose**: an answer assembled out of a vault is only checkable if each part names the note it came from, and showing what was rejected is what stops a confident answer from hiding how thin its evidence was.

- Display a final section holding the **Evidence Table**, one row per **Surviving Hit**, newest note first, with columns:
  - **Note** - the note's basename without `.md`, rendered as a clickable `obsidian://open?vault={vaultName}&file={notesDir}/<basename>.md` link.
    The vault is outside the workspace, so a workspace-relative target cannot resolve to it.
  - **Section** - `<number>. <heading>`, or `(header)` for **Section** 0.
  - **Lines** - the **Hit**'s `startLine`-`endLine` from Step 2.
  - **Date** - the note's date from Step 2.
  - **Supports** - one short phrase naming what this **Section** contributed to the answer.
    Never a restatement of its heading, and never a phrase that would fit every row equally.

- Below the table, under **Mentioned but not used**, list every **Hit** set aside in Step 3 as `note - section heading` only, with no body.
  A reader can then see what was looked at and rejected, and challenge a rejection.

- If any **Search Term** matched nothing in Step 2, restate that here in one line - it bounds what this answer could have found.

- This table is the last thing the run displays.
  Nothing follows it.
