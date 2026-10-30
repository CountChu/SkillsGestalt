---
name: asd-ste
description: Rewrites one English Markdown file in ASD-STE100 Simplified Technical English (STE, Issue 9) as a draft beside it, for the user to review, and puts the draft in the file's place once the user approves it. Headings, fenced blocks, inline code, link targets, placeholders and the source's own header quote stay unchanged, and every statement is kept; the prose is rewritten by the STE writing rules and the STE dictionary, one sentence per line. A script checks the kept spans, the sentence and paragraph limits and each word against the dictionary and the project-approved words; depends_on.py records the fingerprints; the run offers to commit the draft and to have the chinese skill write its 繁體中文 twin, and builds an HTML review page that sets it beside the source. On the user's approval it replaces the source file and its twin with the draft and the draft's twin, records the source file again in each document that declares it, and checks the result. Each step saves what it did in a YAML checkpoint that run step N reads back. It refuses a -tw.md twin, a file already in STE or a source that is not English, and changes the source only to replace it with the approved draft. Triggers "rewrite in STE", "Simplified Technical English", "ASD-STE100".
---

> [ste-rules.md](references/ste-rules.md)  `2026-10-30`  `8014dc37df5f`

# TERMINOLOGY

Terms that mean the same thing in every skill.

- **`run step N`** — a trailing prompt selector naming one step.
  It runs **only** that step, reading every earlier step's output back from the YAML checkpoint.
- **Checkpoint Dir** — the directory holding a skill's YAML checkpoint and the data files its steps write.
  Every skill has its own; this skill's is given under **CONFIGURATION**.
- **YAML checkpoint** — the `process.yaml` inside the Checkpoint Dir.
  Every step writes its outputs there under a `step_{N}` group, so a later step reads them back instead of recomputing them.

# DEDICATED TERMINOLOGY

Terms specific to this skill's domain.

- **source file** — the English Markdown file this run rewrites: a reference, a rule file, a template, a skill's `SKILL.md` — any `.md`.
- **draft** — the file this run writes beside the source file, for the user to review, at the path the **draft tool** gives.
  It is the source file said again in STE: the same headings, fenced blocks, links and placeholders, and the same statements, with the prose rewritten.
  Once the user approves it, Step 7 puts it in the source file's place.
- **STE file** — a file already in STE: its header quote declares the **STE specification**.
  A draft is one, and so is a source file that a draft has replaced.
- **STE specification** — `ASD-STE100_ISSUE9.pdf`, ASD-STE100 Simplified Technical English, Issue 9.
  No step reads it: Step 3 only fingerprints it, for the **header quote**.
- **STE rules digest** — this skill's own summary of the writing rules and the general recommendations of Part 1, with the number of each, followed by the replacements documents like these need most and the House Rules that say how STE is applied to a Markdown file.
  Step 2 writes by it.
- **STE dictionary** — the words of Part 2 as one JSON file: each approved word with its parts of speech and the forms it may take, and each unapproved word with the approved words that replace it.
  It also records the issue, the date and the fingerprint of the PDF it was built from.
- **project-approved words** — the words this project approves beyond Issue 9, as a table: each word with its parts of speech, its forms, its meaning and why the user approved it.
  `check_ste.py` accepts each one as an approved word, and prints an `[INFO]` line that names each one a file uses.
- **project rules** — the writing rules this project adds beyond Issue 9 and the House Rules of the **STE rules digest**, as a second table beside the **project-approved words**: each rule with an example, how it is checked and why the user added it.
  `check_ste.py` gives a `[WARN]` line where the prose may break a rule that the table marks as checked, as it does for two negatives that give a positive meaning.
- **US spelling list** — the shared list of British spellings, each with its American spelling, behind the rule "Write English in American spelling" of [md-style.md](.github/common/rules/md-style.md) (STE rule 1.14).
  `check_ste.py` finds each one, and its -s, -ed, -ing and -er forms, in the prose and in every kept span.
- **technical word** — a word the draft uses that the STE dictionary does not approve in that use: a word it does not approve at all, or an approved word in a technical meaning the dictionary does not give it (STE rule 1.3), such as *record* for data a system keeps.
  It is a technical noun of the source file's subject (STE rule 1.5), such as *stage* or *Dataflow*, or a technical verb (STE rule 1.12), such as *parse*.
  The **header note** lists every one the draft uses, and `check_ste.py` reports none of them.
  A name that md-style.md lets keep its British spelling is listed there too, so that the spelling check passes it.
- **kept span** — a stretch of the source file that reaches the draft byte for byte: every `#` heading line, every fenced block, every inline-code span, every link target and wiki link (`[[name]]`), every `{PLACEHOLDER}` token and every `{placeholder}` token, the frontmatter's keys and every value but `description`, and every line of the source file's own header quote.
- **header quote** — the run of `>` lines at the head of a Markdown file, under its frontmatter or its title: the file's own version first, when it gives one, such as `> Version: 261013`, then one dependency on each line, a link followed by the date and the fingerprint the **Dependency Checker** records, each in inline code.
  The draft's header quote is the source file's own, when it has one, followed by one line that declares the STE specification, such as `` > [[ASD-STE100_ISSUE9.pdf]]  `2026-10-11`  `d1f4ea9e7cd6` ``.
  One more line declares ste-custom.md, `> [[ste-custom]]`, recorded the same way: the draft follows the **project rules**, also when its prose uses none of the **project-approved words**.
- **header note** — the block quote under the header quote of the draft, three lines: a link to the source file, the statement that the source file is correct where the two do not agree, and `Technical words:` followed by every **technical word** the draft uses.
  Once the draft replaces the source file, the first line loses its link and the second line goes.
- **STE check** — the comparison Step 3's `check_ste.py` makes: every kept span of the source file is in the draft, and the draft keeps every STE rule a program can measure.
  A `[FAIL]` is a rule broken; a `[WARN]` is a word or a sentence that a reader has to decide about.
  With `--ste` alone, `check_ste.py` checks an STE file by the rules a program can measure, with no source file to compare.
- **Dependency Checker** — the shared `depends_on.py`: it reads a header quote, fingerprints the files it names, and records each date and fingerprint.
- **dependent** — a document whose header quote records the source file, in any workspace that uses this one's skill group.
  Step 7 records the source file again in each one that still holds after the replacement.
- **draft tool** — this skill's `draft.py`: it gives the paths a run uses for a source file and says whether the source file is a TW twin or an STE file, puts the approved draft and its TW twin in the place of the source file and its TW twin, and lists the dependents.
- **findings file** — the JSON file `check_ste.py` writes with `--findings`: every finding it reports, in full, where the printed report shortens a list.
  Step 1 writes `step_1-findings.json` and Step 3 writes `step_3-findings.json`, in the Checkpoint Dir.
- **step saver** — this skill's `save_step.py`: it writes one step's group into the YAML checkpoint — the title, the time, the values the step gives and a findings file whole — and leaves every other group as it is.
- **TW twin** — a file's 繁體中文 version, which the `chinese` skill writes beside it.
- **pairing line** — the line of a TW twin, above its first heading, that links back to its English file; the `chinese` skill adds one under a frontmatter.
- **review page** — the HTML page Step 6 builds for the user who reviews the draft: the source file and the draft side by side, each in a column that scrolls on its own; the two **TW twins** side by side the same way; and the draft and its TW twin line by line.
  Above them it lists the STE check's result, the warnings left, the technical words and the statements kept in source wording, and then the **review notes**; its labels are in 繁體中文.
  Each item of the review notes, and each item under it, opens with its **review status**.
- **review notes** — the part of the review page that Step 6 writes itself: each place a reviewer should compare, and why.
- **line reference** — how the review notes give a line: `{{en-o:N}}` is line N of the source file, `{{en-d:N}}` of the draft, `{{tw-o:N}}` of the source file's TW twin and `{{tw-d:N}}` of the draft's TW twin; `N-M` is a range, and `N,M` a list.
  The **review builder** turns each one into a link that opens its line.
- **review builder** — this skill's `make_review.py`: it builds the review page from the four files, the YAML checkpoint and the review notes, and writes no page while a line reference names no line.
- **review status** — the mark a reviewer sets on an item of the review notes: `[ ]` pending, `[v]` approved, `[?]` to be explained or `[x]` rejected, each click moving it on to the next.
  `[?]` says that the reviewer does not follow how the item is handled: the agent explains each such item in the conversation, and leaves the review notes as they are.
  `[v]` says that the draft passes at that place as it stands, so a reviewer who agrees with a suggestion in an item marks it `[x]`, not `[v]`.
  On `[x]`, the agent changes the draft as the reviewer decides, then runs Steps 3 and 6 again.
  An item is known by its own text, so an item that changes between two builds of the review page is pending again.
- **review server** — this skill's `review_server.js`, which runs on Node.js: it serves every review page under `checkpoints\asd-ste\`, lists them with how far each review is, and writes the review statuses that a page it serves sends into `step_6-status.json` in that page's Checkpoint Dir.
  It runs until the user stops it; a review page opened as a file shows the review statuses of its build, and saves none.

# CONFIGURATION

Concrete values this skill runs with.

- **source file** — the `.md` path the prompt gives, or the one file of the name it gives, found in Step 0.
- **draft** — the path the draft tool gives, in the source file's own directory.
- **TW twin** — the source file's, beside it, and the draft's, beside the draft, at the paths the draft tool gives.
- **Checkpoint Dir** — `checkpoints\asd-ste\{parent}-{name}\`, where `{parent}` is the name of the source file's directory and `{name}` is the source file's name without `.md`: `.github\common\references\DFD.md` gives `checkpoints\asd-ste\references-DFD\`.
  The draft tool gives it as well.
  There is one for each source file, and every run reuses it.
  It holds the YAML checkpoint, `process.yaml`, and the files Steps 1, 3 and 6 write: `step_1-inventory.txt`, `step_1-findings.json`, `step_3-check.txt`, `step_3-findings.json`, `step_6-notes.html`, `step_6-review.html` and `step_6-status.json`.
- **STE rules digest** — `{skillGroups.common}\skills\asd-ste\references\ste-rules.md`.
- **STE dictionary** — `{skillGroups.common}\skills\asd-ste\references\ste-dictionary.json`.
- **project-approved words** — `{skillGroups.common}\skills\asd-ste\references\ste-custom.md`, its Words table.
- **project rules** — `{skillGroups.common}\skills\asd-ste\references\ste-custom.md`, its Rules table.
- **US spelling list** — `{skillGroups.common}\references\us-spelling.json`.
- **STE specification** — `ASD-STE100_ISSUE9.pdf`, found as the Dependency Checker finds `[[ASD-STE100_ISSUE9.pdf]]`: under the draft's vault, then under each `skillGroups` root.
  In the SkillsGestalt workspace it is `external\ASD-STE100_ISSUE9.pdf`.
- **Dependency Checker** — `{skillGroups.common}\scripts\depends_on.py`.
- **draft tool** — `{skillGroups.common}\skills\asd-ste\scripts\draft.py`.
- **step saver** — `{skillGroups.common}\skills\asd-ste\scripts\save_step.py`.
- **review builder** — `{skillGroups.common}\skills\asd-ste\scripts\make_review.py`.
- **review server** — `{skillGroups.common}\skills\asd-ste\scripts\review_server.js`, at `http://127.0.0.1:8790/`, where the Checkpoint Dir `{parent}-{name}` has its review page at `http://127.0.0.1:8790/{parent}-{name}/`.
- **parity check** — the `chinese` skill's `{skillGroups.common}\skills\chinese\scripts\check_parity.py`, with the keep-English list `{skillGroups.common}\references\tw-keep-english.md`.

# MUST FOLLOW

- Must run workflow step by step, and display each step number.
- **Honour a `run step N` selector**: run Step N, then stop; never a later step.
  Find the Checkpoint Dir by the source file the prompt names: a path gives `{parent}-{name}` at once, and a bare name matches `checkpoints\asd-ste\*-{name}\`, where more than one match is listed for the user to choose from.
  Read the paths Step 0 resolved, and every earlier step's output, from the YAML checkpoint.
  When a group that Step N needs is missing, name the step to run first, and stop.
- **This skill produces no MD report; it writes a YAML checkpoint.**
  The draft is its output, and the Checkpoint Dir records how each run made it and holds the review page Step 6 builds for the user.
  Its other writes are the commit Step 4 makes and the TW twin Step 5 has the `chinese` skill write, each only on the user's yes, and the replacement and the records Step 7 makes, only on the user's approval.
- Follow [report-yaml-rules.md](.github/common/rules/report-yaml-rules.md) for the YAML checkpoint's shape and required fields.
- **Save each step's group with the step saver, never by hand.**
  Read each step's begin time from the system clock as the step begins, with `date '+%Y-%m-%d %H:%M:%S'` on macOS/Linux or `Get-Date -Format "yyyy-MM-dd HH:mm:ss"` in PowerShell, and give it to the step saver as the step ends: the step saver reads the end time and works out the time taken, so no time is estimated.
  A list copied into the YAML by hand loses entries without a word.
- **Every data file in the Checkpoint Dir has exactly one writer step.**
  Step 1 writes `step_1-inventory.txt` and `step_1-findings.json`, Step 3 writes `step_3-check.txt` and `step_3-findings.json`, and Step 6 writes `step_6-notes.html` and, through the review builder, `step_6-review.html`; the review server that Step 6 starts writes `step_6-status.json`; no other step changes them.
  The YAML checkpoint is the one exception: each step replaces its own group in it, and Step 0 starts it afresh, so that a run never mixes its groups with an earlier run's.
  Only the files the YAML checkpoint names belong to its run: a file an earlier run left is replaced when its step runs again.
- **A run that stops early still saves the group of the step it stops in**, with `--stopped` and the reason: a refused source, a `NOT-ENGLISH` or `SOURCE-FIRST` verdict, a no to the overwrite, a check that cannot pass, a TW twin that is missing, a replacement the draft tool refuses.
  The YAML checkpoint then says why a run left no draft, no review page, or the source file as it was.
- **The source file is read-only until the user approves the draft.**
  Never edit, reformat or "fix" it — not even when the rewrite exposes a real defect in it.
  Report the defect and leave it for the user.
  Only Step 7 writes it, and only by putting the approved draft in its place.
- **Refuse a source that is a TW twin, an STE file, or not English.**
  A twin's English file is the one to rewrite, an STE file is STE already, and STE is written in English.
  Step 0 turns away a TW twin and an STE file by what the draft tool says; for the language, Step 1's `check_ste.py` decides, and its verdict is binding.
- **Never change a kept span.**
  A heading, an identifier, a path, a link target or a placeholder that changes stops matching what it names or what names it, and the STE check rejects it.
- **Keep every statement.**
  STE changes how a thing is said, never what is said.
  A rewrite that drops a condition reads better and is wrong, and no script finds it.
  A statement that cannot be said in STE without changing its claim keeps its technical word or its source wording, and Step 2 names it.
- **Never write the date or the fingerprint in the header quote by hand.**
  `depends_on.py record` writes them once the STE check passes; a fingerprint typed in vouches for a check that nobody ran.
- **Write the draft as UTF-8 without a BOM**, using the file-creation tool — or, to correct it, the file-editing tool.
  Never echo it through a shell string: a backtick or a `$` in the text would be rewritten without a word.
- **Commit only on the user's yes, and only the draft.**
  A commit made without asking puts the user's unfinished edits into history, and a file staged by someone else does not belong in it.
  Step 7 commits nothing: the replacement and the records span files that the user commits, in each workspace.
- **Before the skill ends, display the draft path, the review page's link on the review server — or its path, when no review server runs — once Step 6 has built it, and the YAML checkpoint path** — after Step 7, the source file path in place of the draft's — the paths only, never their contents, rendered as clickable Markdown links and never as inline code or plain text.
  Link the YAML checkpoint with a workspace-relative, forward-slash target, such as `[process.yaml](checkpoints/asd-ste/references-DFD/process.yaml)`.
  Do this for every run, including a partial one such as `run step 0`.

# Prompt Examples


## Prompt 1

```
/asd-ste
.github/common/references/DFD.md
```

## Prompt 2

```
/asd-ste
DFD.md
```

## Prompt 3

```
/asd-ste
DFD
```

## Prompt 4

```
/asd-ste
DFD
run step 3
```

## Prompt 5

```
把 .github/common/references/DFD.md 用 ASD-STE100 的風格重寫成草稿，給我審核
```

## Prompt 6

```
/asd-ste
DFD
run step 6
```

## Prompt 7

```
/asd-ste
DFD
run step 7
```


# Workflow

## Step 0 - Warmup

- Run `.venv` first when the workspace has one — the Dependency Checker and the step saver import `PyYAML`; `check_ste.py` and the draft tool need only the Python standard library.

- Read the workspace config [config.yaml](config.yaml) at the workspace root, when there is one, and resolve:
  - **`skillGroups`**: the group name -> skills-root map — this skill's own directory is `{skillGroups.common}\skills\asd-ste\`.
  - Without a `config.yaml`, or without `skillGroups` in it, take `{skillGroups.common}` to be the directory two levels above this skill's own — the one that holds `skills\` — and look for the source file in the workspace folders only.
  - Substitute the resolved value wherever `{skillGroups.common}` appears in the steps below, including in commands.

- Check if the below scripts/files exist before running workflow.
  - `{skillGroups.common}\skills\asd-ste\scripts\check_ste.py`
  - `{skillGroups.common}\skills\asd-ste\scripts\draft.py`
  - `{skillGroups.common}\skills\asd-ste\scripts\save_step.py`
  - `{skillGroups.common}\skills\asd-ste\scripts\make_review.py`
  - `{skillGroups.common}\skills\asd-ste\scripts\review_server.js`
  - `{skillGroups.common}\skills\asd-ste\references\ste-rules.md`
  - `{skillGroups.common}\skills\asd-ste\references\ste-dictionary.json` — when it is missing, stop, and say that `convert_spec.py` builds it again from the STE specification (`python {skillGroups.common}/skills/asd-ste/scripts/convert_spec.py --pdf <ASD-STE100_ISSUE9.pdf> --json <ste-dictionary.json>`, with `pypdf` and `cryptography` installed).
    Do not build it in this run.
  - `{skillGroups.common}\skills\asd-ste\references\ste-custom.md`
  - `{skillGroups.common}\references\us-spelling.json`
  - `{skillGroups.common}\scripts\depends_on.py`

- The prompt takes one of the forms shown in **Prompt Examples** above.
  Parse it for:
  - **source file** (required): a path to a `.md` file, workspace-relative or absolute, as in Prompt 1; a file name, as in Prompt 2; or a name without `.md`, as in Prompt 3, which stands for that name with `.md` added.
  - **`run step N`** (optional): a trailing step selector.

- Resolve the source file:
  - A path that exists — absolute, or relative to a workspace folder — is the source file.
  - Otherwise, look for files of exactly that name under every workspace folder and every `skillGroups` root: `rg --files --hidden -g '<name>' -g '!.git' <folder>`.
    `--hidden` is needed because `.github` is a hidden directory, and `rg` still skips what `.gitignore` excludes.
  - One match is the source file.
    With none, ask the user to type the path and wait for the answer.
    With several, list them and ask which one — never pick the first.

- Run the draft tool on the source file, from the workspace root: `python {skillGroups.common}/skills/asd-ste/scripts/draft.py paths "<source file>"`.
  It prints, as JSON, the source file's TW twin, its draft, the draft's TW twin and the Checkpoint Dir, whether each file exists, and whether the source file is a TW twin (`twin`) or an STE file (`ste`).
  It exits `2` when the source file cannot be read.

- Take the Checkpoint Dir from the draft tool, and create it when it is missing.
  A source file that cannot be found names no Checkpoint Dir, and its run leaves no YAML checkpoint.

- Stop, and say which check failed, rather than rewrite the file, when the source file:
  - does not end in `.md` — this skill rewrites Markdown only;
  - is a TW twin — `twin` is true, and its English file is the one to rewrite;
  - is an STE file — `ste` is true: a draft, or a source file that a draft has replaced;
  - opens with a frontmatter that does not parse — the draft's frontmatter could not be checked against it.

  Before the skill stops, save the group of Step 0, as the last bullet of this step says, with `--stopped` and the check that failed.

- Say whether the draft already exists; whether to overwrite it is Step 2's to ask.

- Save the canonical skill invocation for reference in later steps.

- Display the resolved source file path and the draft path.

- Save the YAML checkpoint under `step_0` with the step saver, and `--new`, which starts it afresh: `skill`, `model`, `prompt` (the canonical skill invocation), `source_file`, `source_twin`, `draft`, `draft_exists`, `draft_twin` and `checkpoint_dir`, each as the draft tool printed it.
  - Example: `python {skillGroups.common}/skills/asd-ste/scripts/save_step.py --checkpoint "checkpoints/asd-ste/references-DFD/process.yaml" --step 0 --title "Warmup" --begin "<begin>" --new --set skill=asd-ste --set model="<model>" --set prompt="<canonical invocation>" --set source_file=".github/common/references/DFD.md" --set source_twin=".github/common/references/DFD-tw.md" --set draft="<draft>" --json draft_exists=true --set draft_twin="<draft's TW twin>" --set checkpoint_dir="checkpoints/asd-ste/references-DFD"`


## Step 1 - Inventory the Source

- Run the script `check_ste.py` with the `--src`, `--dict`, `--custom`, `--spelling`, `--report` and `--findings` arguments.
  - `--src`: the source file resolved in Step 0.
  - `--dict`: the **STE dictionary**.
  - `--custom`: the **project-approved words**.
  - `--spelling`: the **US spelling list**.
  - `--report`: `step_1-inventory.txt` in the Checkpoint Dir.
  - `--findings`: `step_1-findings.json` in the Checkpoint Dir, this step's **findings file**.
  - Example: `python {skillGroups.common}/skills/asd-ste/scripts/check_ste.py --src ".github/common/references/DFD.md" --dict "{skillGroups.common}/skills/asd-ste/references/ste-dictionary.json" --custom "{skillGroups.common}/skills/asd-ste/references/ste-custom.md" --spelling "{skillGroups.common}/references/us-spelling.json" --report "checkpoints/asd-ste/references-DFD/step_1-inventory.txt" --findings "checkpoints/asd-ste/references-DFD/step_1-findings.json"`

- The script prints its inventory to **stdout**, and writes it to the two files as well:
  1. The frontmatter's keys, or that there is none.
  2. Every heading line, in order, with its line number.
  3. The fenced blocks, with their lines.
  4. Every inline-code span, link target and placeholder, each once.
     A placeholder in a retired form is not a kept span: a `[WARN]` lists it, with the command that converts it.
  5. Each table's column count.
  6. The source file's own header quote, line by line.
  7. The STE findings, each marked `[TODO]`: the sentences over the limit, the lines that hold more than one sentence, the paragraphs over six sentences, the semicolons and the contractions, every unapproved word with its replacements, every word the dictionary does not list, the sentences that look passive, every double negative, every Latin abbreviation, every *make sure* with no *that* after it, and every British spelling with its American spelling.
     A project-approved word is not a finding: an `[INFO]` line names each one the prose uses.
     A British spelling in a kept span is a `[TODO]` of its own, to change the source file first: the draft copies the span unchanged.
     So is each word of a heading that the dictionary lists as unapproved and approves in no part of speech, a `[TODO]` to decide.
  8. The CJK share of the prose, and a **verdict**: `rewritable`, `SOURCE-FIRST` when a kept span holds a British spelling, or `NOT-ENGLISH`.

- **If the script exits `2` with the verdict `NOT-ENGLISH`, stop the skill here.**
  Report the share it printed, say that STE is written in English, and do not write a draft.
  Save the group of Step 1 first, as the last bullet of this step says, with `--stopped` and the share.

- **If the script exits `3` with the verdict `SOURCE-FIRST`, stop the skill here.**
  The draft copies each kept span unchanged, so the source file has to change first: report each British spelling in a kept span, with its American spelling and its line, and say that the run starts again once the source file has changed.
  Save the group of Step 1 first, as the last bullet of this step says, with `--stopped` and the spellings.

- Decide each heading word the inventory asks about, from the heading it stands in:
  - Used in the part of speech, or the meaning, that the dictionary does not approve — such as *kind* for type, or *create* as a verb — the heading breaks STE, and only the source file can change it.
    Stop the skill as for `SOURCE-FIRST`, naming each heading and the word it has to replace.
  - Used as a technical noun or a technical verb of the source file's subject (STE rules 1.5 and 1.12), such as *file* as a noun, the word stays, and Step 2 lists it as a technical word.

- Exit `0` means `rewritable`, and once every heading word is decided to stay, the run continues.

- Display a short summary of the inventory: the heading, fence, link and table counts, how many sentences are over the limit, how many unapproved words, words outside the dictionary and British spellings the prose uses, each British spelling in a kept span, and each heading word with what was decided.

- Save the YAML checkpoint under `step_1` with the step saver: the findings file whole, with `--data`; `report_file` and `findings_file`, the names of the two files; and `heading_words`, each heading word decided, with its line and whether it stays, as a JSON list.
  - Example: `python {skillGroups.common}/skills/asd-ste/scripts/save_step.py --checkpoint "checkpoints/asd-ste/references-DFD/process.yaml" --step 1 --title "Inventory the Source" --begin "<begin>" --data "checkpoints/asd-ste/references-DFD/step_1-findings.json" --set report_file=step_1-inventory.txt --set findings_file=step_1-findings.json --json heading_words='[]'`


## Step 2 - Rewrite in STE

- **No script for this step** — saying the same thing in fewer and simpler words without losing any of it is reading and writing that no program can do, so follow the instructions below yourself.

- If the draft exists, say so, and ask the user whether to overwrite it with a full rewrite.
  A no ends the run with no draft written, and the group of Step 2 saved, as the last bullet of this step says, with `--stopped`.

- Read the **STE rules digest** whole, the source file whole, and the Step 1 inventory — under `run step 2`, the `step_1` group of the YAML checkpoint, with `step_1-inventory.txt` beside it.

- Rules that apply to every instruction below:
  - **Copy every kept span byte for byte**, as the inventory lists them.
  - **Keep every statement.**
    No rule, condition, number, example or reason is dropped, merged away or added.
    A long sentence becomes several sentences or a vertical list, never a shorter claim.
  - **Write by the STE rules digest and the project rules**: approved words — those of the STE dictionary and the project-approved words — in their approved part of speech, meaning and form; a technical word only where rule 1.5 or 1.12 allows one; at most 20 words in an instruction and 25 in a description; the active voice; one topic in each sentence and in each paragraph; at most six sentences in a paragraph; no semicolon and no contraction.
  - **Settle every `[TODO]` the inventory printed**: replace each unapproved word with its replacement, or build the sentence again; replace each word outside the dictionary, or keep it as a technical word when it is one; write each British spelling in its American spelling, or keep a name that md-style.md lets keep it, as a technical word.
  - **Put one sentence on each line**, as [md-style.md](.github/common/rules/md-style.md) requires.
  - **Keep one name for one thing.**
    A term the source file uses for one item is the same term in every sentence of the draft.
  - If a statement cannot be said in STE without changing what it claims, keep its technical word or its source wording rather than paraphrase the claim away, and name it in the display at the end of this step.

- Build the draft:
  1. **Frontmatter** — only where the source file has one: every key and every value unchanged, but the `description`, which is rewritten in STE in the same scalar style.
  2. **Title** — the source file's title line, unchanged, when its first line under the frontmatter is one.
  3. **Header quote** — the source file's own header quote lines, unchanged, then `> [[ASD-STE100_ISSUE9.pdf]]` with nothing after it, and `> [[ste-custom]]` with nothing after it, also when the prose uses no project-approved word: the dates and the fingerprints are the Dependency Checker's to write.
  4. **Header note** — a blank line, then the three-line block quote the digest's House Rules give: the link to the source file by its file name, the statement that the source file is correct where the two do not agree, and `Technical words:` followed by every technical word the draft uses, in alphabetical order.
  5. **Body** — the source file's headings and fenced blocks where they stand, and between them the prose rewritten, with the digest's House Rules for tables, emphasis, quoted text and the source file's references to itself.

- Write the draft to the path the draft tool gave in Step 0, as UTF-8 without a BOM, using the file-creation tool.

- Display the draft path, the number of technical words, and every statement kept in its source wording, with why.

- Save the YAML checkpoint under `step_2` with the step saver: `overwrite`, whether a draft that existed was overwritten; `technical_words`, the list the header note gives; and `kept_wording`, each statement kept in its source wording, with its line in the draft, its text and why — the lists given with `--json`.
  - Example: `python {skillGroups.common}/skills/asd-ste/scripts/save_step.py --checkpoint "checkpoints/asd-ste/references-DFD/process.yaml" --step 2 --title "Rewrite in STE" --begin "<begin>" --json overwrite=true --json technical_words='["caller", "stage"]' --json kept_wording='[]'`


## Step 3 - STE Check

- Run the script `check_ste.py` with the `--src`, `--ste`, `--dict`, `--custom`, `--spelling`, `--report` and `--findings` arguments.
  - `--src`: the source file resolved in Step 0.
  - `--ste`: the draft.
  - `--dict`: the **STE dictionary**.
  - `--custom`: the **project-approved words**.
  - `--spelling`: the **US spelling list**.
  - `--report`: `step_3-check.txt` in the Checkpoint Dir.
  - `--findings`: `step_3-findings.json` in the Checkpoint Dir, this step's **findings file**.
  - Example: `python {skillGroups.common}/skills/asd-ste/scripts/check_ste.py --src ".github/common/references/DFD.md" --ste "<draft>" --dict "{skillGroups.common}/skills/asd-ste/references/ste-dictionary.json" --custom "{skillGroups.common}/skills/asd-ste/references/ste-custom.md" --spelling "{skillGroups.common}/references/us-spelling.json" --report "checkpoints/asd-ste/references-DFD/step_3-check.txt" --findings "checkpoints/asd-ste/references-DFD/step_3-findings.json"`

- The script prints one line per check to **stdout**, writes it to the two files as well, and exits `1` if any of them fails:
  1. The draft is UTF-8 without a BOM.
  2. The frontmatter has the same keys, and every value but the `description` is unchanged — or neither file has one.
  3. The heading lines are identical, in order.
  4. The fenced blocks are identical byte for byte, in order.
  5. Every inline-code span, placeholder and link target of the source file is still there.
     A link target the source file does not have, other than the header note's and the header quote's, is a `[WARN]`.
     Neither file holds a placeholder in a retired form.
  6. The tables have the same column counts.
  7. The header quote keeps the source file's own lines and declares `[[ASD-STE100_ISSUE9.pdf]]`.
     A recorded fingerprint other than the one the STE dictionary was built from is a `[WARN]`.
     It declares `[[ste-custom]]` as well, also when the prose uses no project-approved word, because the draft follows the **project rules**.
  8. The header note links to the source file.
     A header note without a `Technical words:` line is a `[WARN]`.
  9. Every sentence is within its limit, each line holds one sentence, each paragraph holds at most six, and the prose has no semicolon and no contraction.
  10. No kept span holds a British spelling of the US spelling list that the header note does not list as a technical word.
      The draft copies a kept span from the source file, so the source file has to change first.

- It also prints a `[WARN]` line for each unapproved word, with its replacements; for each word the STE dictionary does not list; for each British spelling in the prose, with its American spelling; for each sentence that looks passive; for each double negative, which a **project rule** forbids; for each Latin abbreviation (GR-6), with the English words to write; for each *make sure* with no *that* after it (GR-1); and for each technical word listed but never used.
  A word the header note lists as a technical word is not reported, and neither are its plural and its verb forms.
  A project-approved word is not reported either: an `[INFO]` line names each one the prose uses.

- If the script exits `1`, correct the draft for each `[FAIL]`, and run this step's command again until it exits `0`.
  **Fix the draft, never the source file.**

- Read each `[WARN]`, correct the draft where it is right, and run the command again:
  - an unapproved word is replaced with its replacement, or the sentence is built again;
  - a word outside the dictionary stays only when it is a technical word, and is then added to the `Technical words:` line;
  - a British spelling becomes its American spelling, or, when it is a name that md-style.md lets keep it, goes on the `Technical words:` line;
  - a Latin abbreviation becomes the English words the warning gives, and *make sure* takes *that*;
  - a double negative is written as the positive statement, unless the two negatives do not give a positive meaning;
  - a passive sentence is made active, unless nobody knows who or what does the action.

- If a `[FAIL]` is the source file's own defect — an unclosed fence, a table row with the wrong column count, a placeholder in a retired form, a British spelling in a kept span — say so plainly, leave the source file alone, and report it as something for the user to fix.
  The check cannot pass, so save the group of Step 3, as the last bullet of this step says, with `--stopped` and the defect.

- Once the script exits `0`, record the STE specification in the header quote:
  - Run `python {skillGroups.common}/scripts/depends_on.py record "<draft>" --target "[[ASD-STE100_ISSUE9.pdf]]"`, with `--config config.yaml` when the workspace has one.
  - Run the same command again with `--target "[[ste-custom]]"`.
  - `--target` leaves the source file's own dependency lines as the source file recorded them: the draft vouches only for the specification, and the project-approved words and rules, it was just checked against.
  - If it exits `2` because no file named `ASD-STE100_ISSUE9.pdf` is found under the draft's vault or a `skillGroups` root, say so, and leave the line without a record.

- Display the check result: each check's pass or fail, and every warning left, with why it stays.

- Save the YAML checkpoint under `step_3` with the step saver: the findings file of the last check whole, with `--data`; `report_file` and `findings_file`, the names of the two files; `check_runs`, how many times the check ran; `warnings_left`, each warning left with why it stays; and `fingerprint`, the date and the fingerprint the Dependency Checker recorded, or `fingerprint_not_recorded` with why; and `custom_fingerprint`, the same for ste-custom.md.
  - Example: `python {skillGroups.common}/skills/asd-ste/scripts/save_step.py --checkpoint "checkpoints/asd-ste/references-DFD/process.yaml" --step 3 --title "STE Check" --begin "<begin>" --data "checkpoints/asd-ste/references-DFD/step_3-findings.json" --set report_file=step_3-check.txt --set findings_file=step_3-findings.json --json check_runs=2 --json warnings_left='[]' --json fingerprint='{"date": "2026-10-11", "fingerprint": "d1f4ea9e7cd6"}' --json custom_fingerprint='{"date": "2026-10-11", "fingerprint": "<fingerprint>"}'`


## Step 4 - Offer to Commit

- Offer a commit only when there is something to commit and the draft is sound.
  Skip the step, saying why, when:
  - the draft is not in a git repository;
  - git shows no change to it;
  - it fails the STE check — the `verdict` of the `step_3` group in the YAML checkpoint.

- Ask the user whether to commit the draft, showing its branch, the commit subject, and anything else already staged, which the commit leaves out.
  - The subject follows the repository's recent subjects, read with `git log -5 --format=%s`: where they name the document changed, it names the draft's file name.

- On a yes:
  - `git add` the draft when it is new to git, then commit it alone with `git commit -m "<subject>" -- <draft>`, so that whatever else is staged stays staged and out of the commit.
  - Never `git commit -a`, never push, amend, create or switch a branch, and never skip the repository's hooks.
    A hook that rejects the commit is reported with its output, and the step stops there.

- On a no, commit nothing.

- Display the commit's hash and subject, or that nothing was committed.

- Save the YAML checkpoint under `step_4` with the step saver: `skipped` with why, when the step was skipped; otherwise `answer`, yes or no, and `commit`, the commit's hash and subject, when there is one.
  - Example: `python {skillGroups.common}/skills/asd-ste/scripts/save_step.py --checkpoint "checkpoints/asd-ste/references-DFD/process.yaml" --step 4 --title "Offer to Commit" --begin "<begin>" --set answer=yes --json commit='{"hash": "5c98468", "subject": "<subject>"}'`


## Step 5 - Offer the TW Twin

- Skip the step, saying why, when the draft fails the STE check — the `verdict` of the `step_3` group in the YAML checkpoint.

- Ask the user whether the `chinese` skill should write the draft's TW twin, at the path the draft tool gave in Step 0.

- On a yes, run the `chinese` skill against the draft, handing it the draft's path — e.g. `/chinese <draft>`.
  It translates the draft, keeps its header quote and every kept-English span, ends with its own parity check, and offers its own commit of the twin.
  - Do not translate the file here, and do not edit the draft while the `chinese` skill runs — it treats its source as read-only.

- On a no, say that no twin was written.

- Save the YAML checkpoint under `step_5` with the step saver: `skipped` with why, when the step was skipped; otherwise `answer`, yes or no, and `twin_file`, the TW twin's path, when one was written.
  - Example: `python {skillGroups.common}/skills/asd-ste/scripts/save_step.py --checkpoint "checkpoints/asd-ste/references-DFD/process.yaml" --step 5 --title "Offer the TW Twin" --begin "<begin>" --set answer=no`


## Step 6 - Build the Review Page

- Skip the step, saying why, when the draft fails the STE check — the `verdict` of the `step_3` group in the YAML checkpoint.

- Compare the `custom_fingerprint` of the `step_3` group with the fingerprint that ste-custom.md has now: `python {skillGroups.common}/scripts/depends_on.py hash "{skillGroups.common}/skills/asd-ste/references/ste-custom.md"`.
  When they differ, or the group has none, the **project-approved words** or the **project rules** changed after the last STE check: run Step 3 again first, then go on with this step.

- Find the two **TW twins** that CONFIGURATION names.
  When one is missing, stop, and say which one and what writes it: Step 5 writes the draft's, also under `run step 5`, and the `chinese` skill writes the source file's.
  Save the group of Step 6 first, as the last bullet of this step says, with `--stopped` and the TW twin that is missing.

- Read the source file, the draft and the two TW twins whole, and the `step_2` and `step_3` groups of the YAML checkpoint.
  `step_2` is missing when Step 2 did not run after the last Step 0; the review page then lists no statement kept in source wording, and says why.

- Write the **review notes** to `step_6-notes.html` in the Checkpoint Dir, in 繁體中文, using the file-creation tool:
  - An HTML fragment of two parts, each an `<h3>` heading followed by an `<ol>` list: what to look at in the draft, then what to look at in its TW twin.
  - Each item names one place to compare and why a reviewer should look at it.
    Such a place is a sentence whose claim may have moved in the rewrite, set beside the source sentence; one thing with two names, or two things with one name; a term that the draft's TW twin renders other than the source file's TW twin does; a list or a paragraph whose shape changed; or the header quote and the header note.
  - Give every line as a **line reference**, never as a bare number, so that the review builder can link it; `{{` and `}}` mean nothing else in the review notes.
  - Do not list again what the review builder lists by itself — the STE check's result, the warnings left, the technical words and the statements kept in source wording — but name one of them where it raises a question for the reviewer.

- Run the review builder with the `--src`, `--ste`, `--src-tw`, `--ste-tw`, `--checkpoint`, `--notes`, `--out` and `--status` arguments.
  - `--src` and `--ste`: the source file and the draft.
  - `--src-tw` and `--ste-tw`: their TW twins.
  - `--checkpoint`: the YAML checkpoint.
  - `--notes`: `step_6-notes.html` in the Checkpoint Dir, the review notes.
  - `--out`: `step_6-review.html` in the Checkpoint Dir, the **review page**.
  - `--status`: `step_6-status.json` in the Checkpoint Dir, the review statuses the review page starts with; it is missing until the reviewer sets the first one.
  - Example: `python {skillGroups.common}/skills/asd-ste/scripts/make_review.py --src ".github/common/references/DFD.md" --ste "<draft>" --src-tw ".github/common/references/DFD-tw.md" --ste-tw "<draft's TW twin>" --checkpoint "checkpoints/asd-ste/references-DFD/process.yaml" --notes "checkpoints/asd-ste/references-DFD/step_6-notes.html" --out "checkpoints/asd-ste/references-DFD/step_6-review.html" --status "checkpoints/asd-ste/references-DFD/step_6-status.json"`

- The review builder prints to **stdout** the review page path, the section and line counts, how many line references the review notes hold, and how many items each review status has, and exits `0` once it has written the page.
  It exits `1`, and writes no page, when a line reference names no line of its file, with a `[FAIL]` line for each one: correct the review notes, never the four files, and run the command again until it exits `0`.
  It exits `2` when a file cannot be read, or when the YAML checkpoint has no `step_3` group.

- Make sure that the **review server** runs, from the workspace root.
  It needs Node.js: when `node --version` fails, say so, and give the review page's path in place of its link.
  - Ask whether one answers: `node {skillGroups.common}/skills/asd-ste/scripts/review_server.js --probe`.
  - Exit `0`: a review server answers, and serves the review page already.
  - Exit `1`: nothing answers, so start one in the background, where it keeps serving after the run ends, then ask again.
    On macOS and Linux, run `nohup node {skillGroups.common}/skills/asd-ste/scripts/review_server.js --root checkpoints/asd-ste > /dev/null 2>&1 &`; in PowerShell, run `Start-Process node -ArgumentList '{skillGroups.common}/skills/asd-ste/scripts/review_server.js','--root','checkpoints/asd-ste' -WindowStyle Hidden`.
  - Exit `2`: another program holds port 8790; say so, and give the review page's path in place of its link.

- Display the review page's link, `http://127.0.0.1:8790/{parent}-{name}/`, as a clickable Markdown link — or its path, when no review server runs — and the number of items in the review notes.
  When the agent has a browser panel, open the link there as well.

- Save the YAML checkpoint under `step_6` with the step saver: `notes_file` and `review_file`, the names of the two files; `notes`, the number of items in the review notes; `line_references`, the number the review builder printed; and `review_url`, the review page's link, or `review_server` with why no review server runs.
  - Example: `python {skillGroups.common}/skills/asd-ste/scripts/save_step.py --checkpoint "checkpoints/asd-ste/references-DFD/process.yaml" --step 6 --title "Build the Review Page" --begin "<begin>" --set notes_file=step_6-notes.html --set review_file=step_6-review.html --json notes=12 --json line_references=42 --set review_url=http://127.0.0.1:8790/references-DFD/`

- Close with the draft path, the TW twin paths that exist, the review page's link — or its path — when the step built one, and the YAML checkpoint path, as clickable Markdown links.


## Step 7 - Replace the Source

- Skip the step, saying why, when the draft fails the STE check — the `verdict` of the `step_3` group in the YAML checkpoint — or when no review page was built — no `review_file` in the `step_6` group.

- Compare the two fingerprints as Step 6 does: when they differ, run Steps 3 and 6 again first, and then ask.

- Ask the user whether the draft has passed their review, naming the draft, its TW twin and the review page.
  - Only a clear pass replaces the source file.
  - A change the user asks for is made to the draft, or to its TW twin through the `chinese` skill; Steps 3 and 6 then run again, and this step asks again.
  - Any other answer leaves every file as it is.

- On a pass, run the draft tool from the workspace root: `python {skillGroups.common}/skills/asd-ste/scripts/draft.py replace "<source file>"`.
  It writes the draft over the source file, and the draft's TW twin over the source file's TW twin, with the header note cut to two lines as the digest's House Rule 5 gives, and the TW twin's pairing line pointed back at the source file; the header quote stays as it is.
  It then deletes the draft and its TW twin, and prints what it did.
  It exits `1`, and writes nothing, when the draft's TW twin is missing while the source file has one, when a header note is not in the form House Rule 5 gives, or when the draft's TW twin has a frontmatter but no pairing line that links to the draft: say which, and stop.

- Find the dependents: run `python {skillGroups.common}/skills/asd-ste/scripts/draft.py dependents "<source file>" --root <folder>`, with one `--root` for each workspace folder and each `skillGroups` root.
  Ask the user which other workspaces use this one's skill group — as one whose `config.yaml` names it in `skillGroups` does — and add each one's folder as one more `--root`.

- For each dependent, read what changed in the source file — `git diff` of it — and every place where the dependent cites it.
  - When the dependent still holds, record the source file again: `python {skillGroups.common}/scripts/depends_on.py record "<dependent>" --target "<link>"`, with `--config config.yaml` when the dependent's workspace has one.
  - When it no longer holds, do not record it: name it, and what in it the change breaks, for the user to correct.

- Check the result, and run each check again after a correction until it passes:
  - `check_ste.py` with `--ste` set to the source file, and `--dict`, `--custom` and `--spelling` as in Step 3: no `[FAIL]`.
  - the **parity check** on the source file and its TW twin: no failure.
  - `depends_on.py check` on each dependent recorded again: the source file is `UNCHANGED`.

- Display the source file and its TW twin as replaced, the files deleted, each dependent with whether it was recorded again or why not, and each check's result.
  Say that nothing was committed: the user commits the changes in each workspace.

- Save the YAML checkpoint under `step_7` with the step saver: `skipped` with why, when the step was skipped; otherwise `answer`, what the user answered; and, after a replacement, `replaced`, the lines the draft tool printed; `dependents`, each one with its link and whether it was recorded again; and `checks`, each check with its result.
  - Example: `python {skillGroups.common}/skills/asd-ste/scripts/save_step.py --checkpoint "checkpoints/asd-ste/references-DFD/process.yaml" --step 7 --title "Replace the Source" --begin "<begin>" --set answer=pass --json replaced='[]' --json dependents='[]' --json checks='[]'`

- Close with the source file path, its TW twin's path, and the YAML checkpoint path, as clickable Markdown links.
