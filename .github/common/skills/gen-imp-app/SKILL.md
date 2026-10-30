---
name: gen-imp-app
description: >-
  Runs the three-step SOP that turns a vibe-coded app into a skill that owns it. Step 1 takes a
  natural-language brief and writes the first cut of the app into `artifacts\` - a Node server
  started with `node server.js`, its real work done by Python, both standard library only. Step 2
  repeats for as many prompts as it takes, changing the app and proving each change, until the app
  is right. Step 3 ends the vibe coding: it reads the app's own source and reverse-engineers it
  into an `imp-{app}` skill and the 繁體中文 reading copy that makes it reviewable, a bilingual
  RSDC design pair (English and 繁體中文), a bilingual wireframe pair scanned off the app's own
  running page, a `build_app.py` that assembles the app dir, and the skill's own `config.yaml`
  holding every value the app reads - then inverts ownership, so
  the source lives in the skill and the app dir becomes a build product. There is deliberately no
  Step 4: once the owner skill exists, every further change to that app goes through `imp-{app}`,
  never through another round of vibe coding. It builds one app per session and writes an MD report
  and a YAML checkpoint that a later step reopens.
---

# TERMINOLOGY

Terms that mean the same thing in every skill.

- **`run step N`** — a trailing prompt selector naming one step.
  It runs **only** that step, reading every earlier step's output back from the YAML checkpoint.
  This skill also accepts the bare form `step N`.
- **Checkpoint Dir** — the per-run directory holding a skill's YAML checkpoint.
  Every skill has its own; this skill's is given under **CONFIGURATION**.
- **YAML checkpoint** — the `process.yaml` inside the Checkpoint Dir.
  Every step writes its outputs there under a `step_{N}` group, so a later step reads them back instead of recomputing them.
- **MD report** — the Markdown report a skill writes into the wiki vault, in a folder named after that skill, carrying the standard header (Skill, Checkpoint, Created, Updated, Prompt) above its result sections.
- **no forward-reference** — the rule that a step must never depend on a step that comes after it.
  Naming a later step to route control flow does not break it; borrowing that step's output does.

# DEDICATED TERMINOLOGY

Terms specific to this skill's domain.
The glossary owns each definition — a step uses the term rather than restating what it means.

- **the SOP** — the three steps this skill runs for one app: **vibe coding** the first cut (Step 1), iterating it until it is right (Step 2), and **reverse engineering** it into the **owner skill** (Step 3).
  It runs once per app, one step per invocation, and ends at the **handoff**.
- **vibe coding** — building by prompt: the user describes behaviour in natural language and the agent writes the code.
  It is how Steps 1 and 2 work and the only thing Step 3 is there to end.
- **the app** — what the SOP produces: a self-contained directory started with `node server.js`, whose real work is done by Python, both standard library only.
  Node serves and spawns; Python decides.
  It must run with nothing installed.
- **app name** — the short kebab-case name that names everything else: the **app dir** under **the artifacts root**, the **owner skill** `imp-{app}`, and the **design pair**.
  Every prompt gives the app dir name on line 2; the app name is that name with a trailing `-app` stripped.
- **app dir** — the app's one directory, **the artifacts root** plus the app dir name given on line 2 of the prompt.
  It sits outside the wiki vault and outside version control.
  Before the **handoff** it is where the app is written; after it, it is a build product the **builder** overwrites.
- **the artifacts root** — `artifacts\`, relative to the workspace root.
  Every app this SOP builds lives under it.
- **app config** — the `app.config.json` beside the app dir's `server.js`, and the **only** file the app reads.
  Every value the server or the Python would otherwise ask a skill or a **skill config** for is carried here, which is what lets the folder be zipped and run somewhere else unchanged.
- **prompt log** — the ordered record of every **vibe coding** prompt, what it changed and how that change was proved.
  It accumulates across Steps 1 and 2 in the YAML checkpoint.
  Step 3 writes it out as `prompt-log.md` in the Checkpoint Dir, the record **gen-rsdc-app** compares the source against, and renders it into the **owner skill**'s `README.md` under a `# Prompts` heading — the history of *why* the app is shaped as it is, which the code cannot show.
- **owner skill** — `imp-{app}`, the skill Step 3 writes.
  It owns the app from the **handoff** onward: it holds the source, it holds the **design pair**, and it is the only way the app changes.
- **design pair** — `references\{App}-RSDC.md` and its 繁體中文 twin `references\{App}-RSDC-tw.md`, inside the **owner skill**.
  **gen-rsdc-app** writes them to the **RSDC standard**: they decide *what the app must be*; the owner skill decides *how to build and prove it*.
- **RSDC** — Requirements, Specification, Design, Coding: the four parts of a **design pair** document, in that order.
- **RSDC standard** — the chapter-responsibility rules a **design pair** is written to: which question each of the four parts answers, and what each may not reach forward into.
  A disagreement about where something belongs in a **design pair** is settled against it.
- **gen-rsdc-app** — the skill Step 3 runs to write the **design pair**.
  It reads the app's source, draws the **components**, derives the design from the source rather than from the **prompt log**, writes the English half to its design template after checking that template against the **RSDC standard**, and has the `chinese` skill write the twin.
  It changes no code, and hands back the components, findings, defects and **verification obligations** it wrote.
- **skill pair** — the **owner skill**'s `SKILL.md` and its 繁體中文 twin `SKILL-tw.md`, both at the **owner skill root**.
  Unlike the **design pair** and the **wireframe pair**, its two halves are not equals: `SKILL.md` is the only one that runs, and `SKILL-tw.md` exists so a reader can review the procedure in their own language.
  That is what it is for — a procedure nobody can read is a procedure nobody audits.
- **wireframe pair** — `references\Wireframe.md` and its 繁體中文 twin `references\Wireframe-tw.md`, inside the **owner skill**.
  They are the page's element inventory — every panel, control, table column and visibility state — read off the **running** page rather than written from the markup.
  The pair owns that inventory: the **owner skill** points at it and never restates it.
- **component** — one implementable piece of the app that exactly one of the **owner skill**'s steps owns.
  **gen-rsdc-app** draws the component boundaries out of the source, and Step 3 writes one step per component.
- **contract** — the **design pair** sections, plus the **wireframe pair** for a page, that decide what one **component** must do.
  Each of the **owner skill**'s steps names its component's contract and builds against it, and never restates what it says.
- **verification obligation** — a row of the **design pair**'s Verification Obligations, in its Coding part: a claim, the rule it proves, the observation that proves it and who makes it — or *not verified*, with what has been read so far.
  Every **component** is named in at least one; the rows are the only definition of "proved" the **owner skill** has.
- **step purpose** — the one sentence at the head of each of the **owner skill**'s steps saying why that step exists as a step: what the procedure would lose by folding it into its neighbour.
  It is not what the component does — that is the component's one job, and it already has a home in the **design pair**.
- **builder** — `build_app.py` in the **owner skill**.
  It reads the **skill config**, copies the source components over the **app dir** and writes the **app config**.
  It is the owner skill's own tool, not part of the app — the app never builds itself.
- **mountable handler** — `app.js` beside `server.js`, exporting `createApp(options)` and returning the `(req, res)` function the server would have listened with.
  It is how an app is served by something other than itself: a hub requires it, calls it once, and answers for the app under a path of its own.
  Owning a port and answering requests are separable, and only the first is about owning an address.
- **skill config** — `config.yaml` at the **owner skill root**, beside its `SKILL.md`.
  It is the one place a value the app reads is written down, and it lives with the skill rather than in the group's shared file because the **owner skill** is its only reader: keys sitting beside another app's made *who else depends on this* a question nobody could answer by looking, and now the answer is the directory.
  It carries one required top-level key, **`app`** — an `appDir` naming where the **builder** assembles, and a `config` holding the **app config keys** — plus any further top-level key the skill itself reads and the app never does.
  A skill that also delivers the app to another machine gives each destination that same `appDir` + `config` shape under `targets`, because a destination is this same app somewhere else and two things differing only in where they sit should not need two vocabularies.
- **app config keys** — the keys of the **skill config**'s `app.config` block.
  Each becomes an **app config** key **of the same name**: the **builder** copies them across, it does not rename them, so a reader holding an `app.config.json` key can take that exact string back to the file where its value was chosen.
  **The indentation is what says which keys reach the app** — inside a `config` block they do, outside one they never do — and that is checkable by looking, which a naming prefix carrying the same meaning is not.
- **handoff** — the end of Step 3, when the **owner skill** exists and proves out.
  From that moment this skill is finished with that app.

# CONFIGURATION

Concrete values this skill runs with.

- **Checkpoint Dir** — `checkpoints\gen-imp-app\{app}-{yymmdd-hhmm}\`, where `{app}` is the **app name** and `{yymmdd-hhmm}` is stamped when Step 1 runs.
  Steps 2 and 3 **reopen the newest existing directory** for that app rather than stamping a new one — the SOP is one session spread over several invocations.
- **YAML checkpoint** — `process.yaml` inside the Checkpoint Dir.
- **MD report** — `{wikiDir}\gen-imp-app\gen-imp-app-{app}-{yymmdd-hhmm}.md`, carrying the same stamp as the Checkpoint Dir, where `wikiDir` comes from the workspace [config.yaml](config.yaml) (resolved in Step 0) — never hardcode the wiki root.
- **the artifacts root** — `artifacts\`, relative to the workspace root.
- **SKILL template** — `{skillGroups.common}\templates\SKILL-tmp.md`, the file Step 3 writes the **owner skill** from.
- **owner skill root** — `{skillGroups.<group>}\skills\imp-{app}\`, where `<group>` is the `skillGroups` key chosen in Step 3.
  It defaults to `dedi-apps`, the group that owns the apps this SOP builds.
- **skill config** — `{owner skill root}\config.yaml`, written by Step 3.
- **session resolver** — `{skillGroups.common}\skills\gen-imp-app\scripts\resolve_session.py`.
- **owner-skill checker** — `{skillGroups.common}\skills\gen-imp-app\scripts\check_owner_skill.py`.
- **RSDC standard** — `{skillGroups.common}\references\RSDC-Standard.md`, with its diagram notation in `{skillGroups.common}\references\DFD.md`.
- **gen-rsdc-app** — `{skillGroups.common}\skills\gen-rsdc-app\SKILL.md`.
- **prompt log** — `step_1` and `step_2` of the YAML checkpoint, written out by Step 3 as `prompt-log.md` in the Checkpoint Dir.

# MUST FOLLOW

- Must run workflow step by step, and display each step number.
- Each step must be self-contained.
  **No forward-reference.**
- A step that a program can do deterministically must be run as a script.
  A step that needs reading, judgement, or summarization **must not** be scripted — write it as natural-language instructions for the agent to perform directly.
- **Honour a `run step N` selector**: run Step N, then stop; never a later step.
- **One step per invocation, and the SOP is not run end to end.**
  Step 1 is one conversation, Step 2 is as many as it takes, Step 3 is another.
  An invocation with no step selector is asking which step to run, not asking for all of them.
- **There is no Step 4.**
  Once Step 3 has produced the **owner skill**, this skill is finished with that app: a later change is `/imp-{app}`, never another `/gen-imp-app step 2`.
  That is not bookkeeping — after the **handoff** the **app dir** is a build product, so a second round of **vibe coding** would edit files the **builder** silently overwrites on its next run, with no diff left to show what was lost.
- **Prove every change before recording it.**
  A **vibe coding** round is finished when the app was started, the changed path was exercised, and what came back was read — not when the code looks right.
  The **prompt log** records the proof next to the change, and a round with no proof is recorded as unproven rather than as done.
- **The app is production code, however it was written.**
  No secret on a command line — a Windows process list is readable by every other process, so a password reaches Python on **stdin** or not at all.
  No host, path or URL taken from a browser and used unchecked: an allow-list decided by the app, enforced again inside the Python, is what keeps the server from being a relay into the network behind it.
  Escape every value that reaches the page — the data comes from somewhere else.
  **Never weaken one of these to make a step pass.**
- **Step 3 has gen-rsdc-app derive the design from the source, not from the prompt log.**
  The code is what the app *is*; the **prompt log** is why.
  Where the two disagree, the code wins and the disagreement is itself a finding worth writing down — a rule that was asked for and never landed is exactly what a reverse-engineered design is for catching.
- **A design pair is one design in two languages.**
  A section written or changed in `{App}-RSDC.md` is written or changed in `{App}-RSDC-tw.md` in the same run, under the same number.
  Two files that drift no longer say what the app is; they argue about it.
  The **wireframe pair** carries the same rule, and so does the **skill pair** — with one difference: only `SKILL.md` runs, so a change is written there first and mirrored into `SKILL-tw.md` in the same run, never the other way round.
- **The page is documented by scanning it, not by describing it.**
  The **wireframe pair** is read off the app running in a browser, element by element from the live DOM — because an inventory written from the markup lists what the author believes the page has, and the point of the scan is to find out.
  Panels that only appear after something happens are reached before they are written down.
- **The page's element inventory lives in the wireframe pair, and the owner skill never restates it.**
  A panel, control or column named in one of the owner skill's steps is a pointer to the **wireframe pair**, not a second list.
  Two inventories of one page drift, and a reader cannot tell which is current.
- **The owner skill carries no architecture and no UI detail at all — the same rule, widened.**
  What the app must be lives in the **design pair**; what a page contains lives in the **wireframe pair**.
  A step names its **contract** and its **verification obligations** and stops there.
  This is what keeps the owner skill a procedure rather than a third description of the app, and it is why a **step purpose** may say why the step exists but never what its component does.
- **The dependency runs one way: the owner skill reads the design, and the design never mentions the owner skill.**
  A **design pair** or **wireframe pair** that names `SKILL.md`, the **owner skill** or the **builder** has stopped being a design and become half of a circular definition — each document explaining itself by pointing at the other, and no single source left.
  A design says what the app must be; the app does not know what procedure built it.
  A design states its own authority without naming what it outranks: *any implementation disagreeing with this document is what changes*.
  Naming the thing the app **replaces** is a different matter and belongs in Requirements.
- **Step 3 inverts ownership, and that inversion is the point of the SOP.**
  Before it, the app dir holds the source.
  After it, the **owner skill** holds the source and the **builder** produces the app dir from it.
  Move the files; do not copy them and leave two editable originals behind.
- **The built app must not need any skill to keep working.**
  Everything a user does routinely is reachable from its page, with Node and Python standard library only — no `npm install`, no package, no CDN, no font fetched at load.
  The skills exist to build and change the app, not to operate it.
  - The **skill config** does not travel with the app, so a component that finds no `config.yaml` beside it treats that as **normal, not fatal**: inside the **app dir** there is none, and every value it would have read is already on its command line or in the **app config**.
- **Every app is mountable, and both halves of that are written from the first cut.**
  It publishes a **mountable handler**, and its `server.js` keeps the `listen` behind `require.main === module` so that loading the app does not start a server.
  Its page addresses the server **relative to itself** — `./api/x`, never `/api/x` — and a page the server *generates* several segments deep computes its way back rather than assuming it is at the root.
  - This is in the fixed shape rather than added when a hub appears, because **neither failure is visible in a reading**.
    An unguarded `listen` only shows when the file is required; an absolute address only shows when the app is served under a path — both at the moment somebody else depends on it.
    Retrofitting one app is an afternoon of design-document changes in two languages; writing it correctly costs a dozen lines.
  - The **mountable handler** prepares once and refuses there rather than on someone's first request.
    What it must **not** refuse is an absent artifact the app is designed to answer without — a design that serves an empty view and says so is not a design that fails to start.
  - What a **hub** requires of something it mounts, and which half of it a hub can verify, is that hub's own business and belongs in its design.
    This rule is about what every app publishes, not about who consumes it.
- **Every output carries the one `{yymmdd-hhmm}` stamp** — one MD report and one Checkpoint Dir per SOP session, appended to by each step.
  The **app dir** is **unstamped**: it is meant to be replaced, and stamping it would leave a trail of stale copies where a reader expects one current folder.
- Follow [report-md-rules.md](.github/common/rules/report-md-rules.md) for the MD report's header and shape.
- Follow [report-yaml-rules.md](.github/common/rules/report-yaml-rules.md) for the YAML checkpoint's shape and required fields.
- Follow [scratch-rules.md](.github/common/rules/scratch-rules.md) for where a run's throwaway files go and how they are cleaned up.
  This SOP writes more of them than most — every proof in Steps 1 and 2 is a probe — and a probe left in the workspace root is indistinguishable from the app it was testing.
- **Before the skill ends, display the MD report and YAML checkpoint paths** — show only the two paths, never their contents, and render both as clickable Markdown links, never as inline code or plain text.
  - Link the **MD report** with an `obsidian://open?vault={vaultName}&file=<vault-relative-path>` URI — the vault lives outside this workspace, so a workspace-relative target cannot resolve to it (e.g. `[gen-imp-app-redfish-test-260829-1530.md](obsidian://open?vault={vaultName}&file=gen-imp-app/gen-imp-app-redfish-test-260829-1530.md)`).
  - Link the **YAML checkpoint** with a workspace-relative, forward-slash target (e.g. `[process.yaml](checkpoints/gen-imp-app/redfish-test-260829-1530/process.yaml)`).
  - Do this for every run, including a partial one such as `run step 0`.

# Prompt Examples


## Prompt 1

```
/gen-imp-app
redfish-test-app
step 1
Read note-260824-Mo to build an app.
Start it with node server.js.
Do the real work in Python.
```

## Prompt 2

```
/gen-imp-app
redfish-test-app
step 2
Can you add this one to SINGLE CALL?
/9/redfish/v1/Managers/System/LogServices/Log/Actions/LogService.ClearLog
```

## Prompt 3

```
/gen-imp-app
redfish-test-app
step 3
```


# Workflow

## Step 0 - Warmup

- Run `.venv` first.

- Read the workspace config [config.yaml](config.yaml) at the workspace root and resolve:
  - **`wikiDir`**: the MD report root — this skill's reports go under `{wikiDir}\gen-imp-app\`.
  - **`vaultName`**: the last path segment of `wikiDir` (e.g. `MyVault`) — the Obsidian vault name used to build `obsidian://` links.
  - **`skillGroups`**: the group name -> skills-root map — this skill's own directory is `{skillGroups.common}\skills\gen-imp-app\`, and the group Step 3 writes into is `{skillGroups.<group>}`.
  - Substitute the resolved values wherever `{wikiDir}`, `{vaultName}`, `{skillGroups.common}` or `{skillGroups.<group>}` appears in the steps below (including in commands).
  - If `config.yaml` is missing or a needed key is absent, stop and ask the user.

- Check if the below scripts/files exist before running workflow.
  - `{skillGroups.common}\skills\gen-imp-app\scripts\resolve_session.py`
  - `{skillGroups.common}\skills\gen-imp-app\scripts\check_owner_skill.py`
  - `{skillGroups.common}\skills\gen-rsdc-app\SKILL.md`

- The prompt takes one of the forms shown in **Prompt Examples** above.
  Parse it **positionally**, so a brief line is never mistaken for one of the two arguments:
  - **Line 2 — the app dir name**, e.g. `redfish-test-app`.
    It names the directory under **the artifacts root** directly; the **app name** is that name with a trailing `-app` stripped, so `redfish-test-app` yields `redfish-test`, an **app dir** of `artifacts\redfish-test-app` and an **owner skill** named `imp-redfish-test`.
    Display the derived name and the paths it implies before using it, and let the user override it.
    On Steps 2 and 3 it also selects which session to reopen: check it against the `app` recorded in the YAML checkpoint and stop on a mismatch, rather than opening a second session for the same app.
  - **Line 3 — the step selector**, `step N` or `run step N`.
    It selects which of Steps 1, 2 and 3 runs.
    If the prompt names no step, do not guess: say which steps exist, say which one the app's current state suggests, and ask.
  - **The brief** — every line after the step selector, verbatim.
    **It may be empty**, as Prompt 3 shows: Step 3 needs no brief, because everything it works from is the app's own source and the YAML checkpoint.
    For Step 1 the brief describes the app to build; for Step 2 it describes one change; for Step 3, when present, it names the group or a preference for the **owner skill**.
    Keep it in the user's own words — it becomes a **prompt log** entry, and a paraphrase loses the request.
  - **Referenced notes** — a brief may name a wiki note (e.g. `note-260824-Mo`).
    Resolve it under `{wikiDir}\write-note\` and read it before doing anything else; it usually carries the requirements the brief only gestures at.
  - A prompt written as free-form prose carries none of these positional arguments.
    Ask for the app dir name and the step rather than inferring either from the prose.

- If a required input is missing, ask the user for it.

- Resolve the SOP session by running the **session resolver**, which owns this deterministically so two invocations of the same session cannot land in different directories.
  - Example: `python {skillGroups.common}\skills\gen-imp-app\scripts\resolve_session.py --app redfish-test --step 1`
  - On `--step 1` it stamps and creates a new Checkpoint Dir.
    On `--step 2` or `--step 3` it reopens the **newest existing** `{app}-*` directory, and exits non-zero naming the sessions it can see if there is none — a Step 2 with no Step 1 behind it is a mistake, not a fresh start.
  - It prints one JSON object carrying `app`, `stamp`, `checkpointDir`, `processYaml`, `mdReport` and `sessions`.
    Use those paths verbatim for the rest of the run.

- Save the canonical skill invocation for reference in later steps.

- Save YAML checkpoint `step_0` with: `step`, `app`, `stamp`, `checkpointDir`, `mdReport`, `brief`, `referencedNotes`.
  Creating the MD report file is optional in this step since there may not be meaningful results yet.


## Step 1 - Vibe-code the first cut

- **No script for this step** — writing an app from a natural-language brief is the whole of **vibe coding** and needs judgement, so follow the instructions below yourself.

- Read the brief and every note it references, then say back in one paragraph what the app is for, what it replaces, and what the user will click.
  Get that agreed before writing code: everything after this is built on it.

- Write the first cut into the **app dir**.
  Whatever the brief asks for, the shape is fixed:
  - `server.js` at the root, started with `node server.js`.
    Node standard library only — no framework, no package, no `npm install`.
    Its `listen` sits behind `require.main === module`, so requiring the file starts nothing.
  - `app.js` at the root, the **mountable handler**: it prepares the app once and returns the `(req, res)` function `server.js` would have listened with.
    Two entry points, one app — never a second copy of the routing.
  - The real work in Python under `scripts\`, standard library only.
    The server spawns it and relays what it prints; **the server parses none of the domain**, so swapping the Python changes the app.
  - `public\` holding the page the server serves by name — markup, styling and behaviour in separate files, all local.
  - An **app config** beside `server.js`, holding every value the app reads.
    Nothing that could be configured is written into the code instead.
  - A `start.cmd` and a `README.txt`, so the folder is runnable by someone who was not in this conversation.

- Honour the production-code rules in **MUST FOLLOW** from the first cut, not as a later cleanup: stdin for secrets, an allow-list for anything a browser supplies, escaping on the way to the page, and **every address the page emits written relative to the page** — `./api/x` and `./app.css`, never `/api/x` and `/app.css`.

- Prove it before recording it: start the server, open the page, exercise one path end to end, and read what came back.
  Say what was run and what it returned.
  **Prove the second entry point too** — require `app.js`, call `createApp()`, and answer one request through the handler it returns with no port bound.
  An app.js that has never been called is a claim.

- Open the **prompt log** with this round: the brief verbatim, the files written, what was proved and what is still missing.

- Save YAML checkpoint under `step_1` with: `app`, `appDir`, `entry`, `serverPort`, `pythonScripts`, `pageFiles`, `appConfigKeys`, `promptLog`, `proof`, `openIssues`.

- Save MD report file.
  Append and display a **First Cut** section:
  - **Summary line**: what the app is for, what it replaces, and the one command that starts it.
  - **Files table** with columns:
    - **File**: the path relative to the **app dir**.
    - **Role**: which part of the fixed shape above it fills.
  - **Proof table** with columns:
    - **Check**: what was run.
    - **Result**: what came back, quoted rather than characterized.
  - **Open**: what the brief asked for that this cut does not yet do.


## Step 2 - Iterate until the app is right

- **No script for this step** — deciding whether a change belongs in the code, in the **app config** or nowhere is judgement, so follow the instructions below yourself.

- This step **repeats**.
  Each invocation carries one change brief, and there are as many invocations as the app needs.
  Read `step_1` and any existing `step_2` from the YAML checkpoint first, so this round starts from what the app already is.

- Rules that apply to every round:
  - **Change the source, then re-run, then read the result.**
    A round ends at the proof, not at the edit.
  - **A new value belongs in the app config, a new behaviour belongs in the Python.**
    If a change can be made by adding a key rather than a branch, add the key — that is what keeps the next change from needing this skill.
  - **Never widen a guard to make a round work.**
    If the allow-list, the stdin rule or an escaping rule blocks the change, the change is wrong.
    Say so and propose the version that is not.
  - **A destructive or irreversible action gets a fence before it gets a button** — confirmation in the page, an explicit flag in the Python, and exclusion from anything that runs unattended.
  - Base every conclusion on what the app returned — do not report a change as working because the code says it should.

- For each change brief, in order:
  1. **Locate.**
     Name the files the change touches and say why those and not others.
     A change that touches the server *and* the Python usually means the boundary between them is in the wrong place — fix the boundary rather than threading the value through.
  2. **Change.**
     Make the edit, keeping the fixed shape from Step 1 intact.
  3. **Prove.**
     Start the app, exercise the changed path, read what came back, and quote it.
  4. **Record.**
     Append one **prompt log** entry: the brief verbatim, the files touched, the proof, and anything the change revealed that was not asked about.

- **Append to the round list; never overwrite it.**
  `step_2` in the YAML checkpoint holds a `rounds` list that grows by one entry per invocation.
  Read it, append, write it back — a round that replaces the list erases the history Step 3 renders into the **owner skill**'s README, and nothing else holds a copy.

- Stop when the user says the app is right.
  That is the only stop condition; a round that reveals more work is not the end of Step 2.

- Save YAML checkpoint under `step_2` with: `rounds` (append one entry carrying `n`, `brief`, `filesTouched`, `proof`, `notes`), `roundCount`, `appConfigKeys`, `openIssues`.

- Save MD report file.
  Append to (or create) an **Iterations** section:
  - **Rounds table**, one row per round, with columns:
    - **#**: the round number.
    - **Asked**: the brief, condensed to one line — escape any `\|` so a quoted path does not split the row.
    - **Changed**: the files touched.
    - **Proof**: what was run and what came back.
  - **Still open**: what remains before Step 3 is worth running.


## Step 3 - Reverse-engineer the app into imp-{app}

- **No script for this step's reading and writing** — deriving a design from source code, drawing **component** boundaries and writing a skill are judgement: **gen-rsdc-app** derives the design, and the rest is done by following the instructions below yourself.
  Only the final conformance check is scripted.

- Read `step_1` and `step_2` from the YAML checkpoint for the **app name**, the **app dir** and the **prompt log**.
  Then **read the app's whole source**, top down: `server.js`, `public\`, `scripts\`, the **app config**.
  **gen-rsdc-app** derives the design from it, and the owner skill, the wireframe scan and the builder are written from it here.

- Resolve the group for the **owner skill**: the `skillGroups` key named in the brief, or `dedi-apps` when there is none — which is the usual case, since Step 3 normally runs with no brief at all.
  If the named key is absent from the workspace `config.yaml`, stop and ask rather than inventing a path — a skill written under an unregistered root is invisible to VS Code.

- For each of the following, in order:
  1. **Write the prompt log out.**
     Render every **prompt log** entry of `step_1` and `step_2`, in order — the brief verbatim, the files touched, the proof and the notes — into `prompt-log.md` in the Checkpoint Dir.
     It is the record of what was asked that **gen-rsdc-app** compares the source against; without it, a rule that was asked for and never landed goes unnoticed.
  2. **Write the design pair with gen-rsdc-app.**
     Run it on the **app dir**, naming `{App}` as the app name, the **owner skill root**'s `references\` as where the pair goes, and the prompt log written out above:

     ```
     /gen-rsdc-app
     artifacts\{app}-app
     {App}
     {skillGroups.<group>}\skills\imp-{app}\references
     checkpoints\gen-imp-app\{app}-{yymmdd-hhmm}\prompt-log.md
     ```

     - It checks its design template against the **RSDC standard** first, and stops before writing anything if the template has fallen behind.
       A stop there stops this step too: say so, and that the template is **gen-rsdc-app**'s to bring up to the standard.
     - It derives the design from the source rather than from the **prompt log**, and records each disagreement between them as a finding.
       Its documents name no skill and no tool, so they keep the one-way rule of **MUST FOLLOW**.
     - Each **component** it hands back becomes one step of the **owner skill**: the smallest set of pieces that each have one job and one owner, so a piece too large to build in one step is still two components.
     - It has the `chinese` skill write the twin, which asks whether to commit the **design pair**; pass the question to the user.
     - Read back what it hands back — the **components**, the findings, the defects, the **verification obligations**, its check of the English half and what the `chinese` skill reported of the twin — for the checkpoint and the report below.
  3. **Scan the running UI into the wireframe pair.**
     Start the app, open its page in a browser, and read the **live DOM** — not the markup file — into `references\Wireframe.md` and `references\Wireframe-tw.md` under the **owner skill root**, both in the same run:
     - Walk the page top to bottom, one bullet per element, each tagged with its kind — `[Panel]`, `[Button]`, `[Select]`, `[Input]`, `[Text]` and so on — and carrying the label a user actually sees, not the element's id.
     - Render every table as a table of its own columns, in the order the page shows them.
     - Record the **visibility states**: which parts are hidden until something happens, and what makes each appear.
       A wireframe of only the opening screen documents a fraction of the app.
     - Exercise the page far enough to reach those states before writing them down.
       A state nobody opened is a guess, and a guess is what the scan exists to replace.
     - Where the scan reveals a defect, write it in the wireframe as a defect and in the **design pair**'s Defects, in its Coding part, as one — in both halves, under the same number.
       An element that shows a wrong value is still an element; the wireframe records both facts.
  4. **Write the owner skill** from the **SKILL template** into `{skillGroups.<group>}\skills\imp-{app}\SKILL.md`: one step per component, a DEDICATED TERMINOLOGY entry naming every component, every file, the **design pair** and the **wireframe pair**, and a MUST FOLLOW carrying the seven rules that make the skill hold — the **design pair** is the source of record; a design change is a design-pair change first and in both languages; the skill carries no architecture and no UI detail, because what the app must be already lives in the **design pair** and what a page contains already lives in the **wireframe pair**; a **step purpose** says why the step exists, never what its component does; edit the components and never the **app dir**; the app must keep working with no skill present; and no guard is widened to make a change work.
     Draw its `# Dataflow` from those steps, as the template lays it out: each step named exactly as its heading, and the data each one reads and writes.
     Leave none of the template's placeholder tokens behind.
     - **Give every step the same four-part head**: a **step purpose**, the **component** it owns, the **contract** it builds against — the design-pair sections, plus `Wireframe.md` for a page step — and the **verification obligations** it is proved by, which are the rows of the design pair's Verification Obligations that name its component.
       Say the shared shape once above the steps rather than eleven times inside them.
     - **A step names its contract and stops.**
       It does not repeat what the contract says: a rule, an endpoint, a field, a file layout, a panel or a column written into the skill is a second copy of something that already has a home, and the two will drift.
       The step that owns a page says how the page is **built and proved** and refers to `Wireframe.md` for what it **contains**.
     - **Say once, above the steps, which of them are not scripted and why** — never under each heading.
       A line repeated beneath nine of eleven steps carries no information, and once a step has a **step purpose** the two end up saying the same thing: the reason a step needs judgement is usually the reason it exists.
       The scripted-versus-not rule in **MUST FOLLOW** still has to be answered — answer it once, for the whole workflow.
     - **A step purpose says why the step is a step** — what the SOP would lose by folding it into its neighbour.
       It must not slide into describing the component, which is the *one job* column of the design pair's component table; that is architecture, and the rule above forbids it.
       One sentence.
     - **Then write the 繁體中文 half of the skill pair**, `SKILL-tw.md`, beside it in the same run — every section, every rule, every step, in the same order and with nothing dropped.
       It is what lets the procedure be reviewed by hand rather than taken on trust, so a summary is not one; a step missing from it is a step nobody reviews.
     - **Keep every heading in English** — the six section headings and each `## Step N - ` title, character for character as `SKILL.md` has them — so the two can be read side by side and a reviewer can see at a glance that nothing is missing.
       Keep file names, paths, config keys, checkpoint field names and glossary terms in their original form for the same reason; translate the prose around them.
     - **Say at the top of `SKILL-tw.md` that it does not run**: it is a translation for reading, `SKILL.md` is the one that executes, and a change is made there first.
  5. **Invert ownership.**
     Move the source out of the **app dir** and under the **owner skill root** — the server, the **mountable handler** and the page under `server\`, the Python under `scripts\` — so exactly one editable copy of each file exists.
     Moving, not copying: two originals is the failure this step exists to prevent.
  6. **Write the builder.**
     `build_app.py` under the **owner skill root**, reading the **skill config** and assembling the **app dir**: copying the components over it — the **mountable handler** among them, at the app dir's root and not under `public\` — and writing the **app config** from the `app.config` block.
     Assert it carries every key of that block into the **app config** under the same name and invents none, then run it and diff the rebuilt app dir against what was moved — a byte difference here means the builder is not reproducing the app that was proved.
  7. **Write the skill config.**
     `config.yaml` at the **owner skill root**, carrying `app` with its `appDir` and its `config` block, each key commented with what it is for and what changing it costs.
     Head the file with what the two levels mean, so the next reader does not have to infer the rule from the indentation they are looking at.
     Then re-parse it and confirm the **builder** resolves every key out of it.
     - **Do not add these keys to the group's `config.yaml`.**
       The group file is shared, and a key in it invites the question of who else reads it — which for an app exactly one skill owns has no answer worth the search.
     - **A path key is relative to the workspace root unless its own comment says otherwise**, so the file can be read without knowing where a run started.
  8. **Render the prompt log.**
     Write `README.md` under the **owner skill root** with a `# Prompts` section carrying every **prompt log** brief in order, followed by whatever a reader needs to run the app's pieces by hand.

- Run the **owner-skill checker** to verify what was written, rather than trusting that it was.
  - Example: `python {skillGroups.common}\skills\gen-imp-app\scripts\check_owner_skill.py --skill-dir "{skillGroups.<group>}\skills\imp-{app}" --app-dir "artifacts\{app}-app" --out "checkpoints\gen-imp-app\{app}-{yymmdd-hhmm}"`
  - The script:
    1. Parses the SKILL.md frontmatter, and checks `name` equals the parent directory name, that a description is present, and that no placeholder token from the template survives.
    2. Checks the top-level sections appear in the canonical order and that the `## Step N` headings run contiguously from 0.
    3. Checks the Markdown is well formed — balanced code fences, and every table row carrying the same column count as its separator once escaped pipes are removed.
    4. Checks the **design pair**: both files present, their numbered section headings matching one for one so a translation that lost or gained a section is caught, that neither file names `SKILL.md`, the **owner skill** or the **builder**, and that the SKILL.md does name the design document — the dependency runs one way and both of its ends are checked.
    5. Checks the **wireframe pair**: both files present, the two carrying the same shape — heading, bullet and table-row counts — and the SKILL.md naming `Wireframe.md`.
       A skill that lists its own panels instead of pointing at the wireframe is the drift this pair exists to prevent.
    6. Checks the **app dir** is self-contained — no `node_modules`, no non-builtin `require`, no external `script`, `link` or CDN reference in the page.
    7. Saves the results as `owner-skill-check.json` in the output directory, and exits non-zero if any check failed.

- **The checker does not read `SKILL-tw.md`, so verify the skill pair by hand before the handoff**: list the headings of both files and confirm they match one for one, and that every `## Step N - ` title is present in both under the same number.
  A heading only the English half has is a section the reviewer will never see.
  Report the two heading counts alongside the checker's results.
- Do not report the **handoff** until every check passes.
  A failing check is a defect in what was just written, not a note for later.

- Save YAML checkpoint under `step_3` with: `ownerSkill`, `group`, `ownerSkillDir`, `promptLogFile`, `components`, `findings`, `skillPair`, `designPair`, `wireframePair`, `wireframeScan`, `builder`, `skillConfig`, `readme`, `checks`, `handoff`.

- Save MD report file.
  Append and display a **Handoff** section:
  - **Summary line**: the **owner skill** that now owns the app, where its source lives, and the one sentence that matters — every further change to this app goes through `/imp-{app}`, and this skill will not run on it again.
  - **Documents line**: the **skill pair**, the **design pair** and the **wireframe pair** as six links, with the counts the checker compared, the heading counts the skill pair was matched on, and how the page was reached for the scan.
  - **Components table** with columns:
    - **Component**: its name in the owner skill's glossary.
    - **File**: where its source now lives.
    - **Owning step**: which step of the owner skill builds it.
  - **Verification table** with columns:
    - **Check**: each check the **owner-skill checker** ran.
    - **Result**: what it returned, including the counts it compared.
  - **Notes**: the findings **gen-rsdc-app** handed back — a rule that was asked for and never landed, or a behaviour nobody asked for that the code has — and the defects it and the wireframe scan found.
