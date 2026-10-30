---
name: imp-app
description: >-
  Builds one local web app or dashboard from plain prose - a Node server (`node server.js`) whose real
  work is done by a Python kernel, both standard library only, configured by one `app.config.json` -
  and carries it through six commands. The prompt's second line names the app dir, its third the
  command: `vibe` builds and changes the app from prose; `reverse` derives its documents from the source
  and the live page, an RSDC design pair and a wireframe pair in English and 繁體中文; `update` changes
  those documents first, the code second; `test` runs the unit tests, then drives the page in a
  browser; `start` brings the app up and says where; `deploy` copies it to a target in this skill's target
  list. The order is one-way: the first `reverse` closes `vibe`, the first `update` closes `reverse`.
  Per app it writes one MD report and one YAML checkpoint, appended to by every command, and a
  lifecycle record, `.imp-app.json` in the app dir, that the order is enforced from.
---

# TERMINOLOGY

Terms that mean the same thing in every skill.

- **`run step N`** — a trailing prompt selector naming one step.
  It runs **only** that step, reading every earlier step's output back from the YAML checkpoint.
- **Checkpoint Dir** — the per-run directory holding a skill's YAML checkpoint.
  Every skill has its own; this skill's is given under **CONFIGURATION**.
- **YAML checkpoint** — the `process.yaml` inside the Checkpoint Dir.
  Every step writes its outputs there under a `step_{N}` group, so a later step reads them back instead of recomputing them.
- **MD report** — the Markdown report this skill writes into the wiki vault, in a folder named after the skill, carrying the standard header (Skill, Checkpoint, Created, Updated, Prompt) above its result sections.
- **no forward-reference** — the rule that a step must never depend on a step that comes after it.
  Naming a later step to route control flow does not break it; borrowing that step's output does.

# DEDICATED TERMINOLOGY

Terms specific to this skill's domain.
The glossary owns each definition — a step uses the term rather than restating what it means.

- **app dir** — the directory the prompt names on its second line, e.g. `artifacts\InvCov`, relative to the workspace root and outside the wiki vault.
  It is where the app lives, and from the first **vibe** onward it is that app's **source**, not a build product.
- **app name** — the **app dir**'s last path segment with a trailing `-app` stripped, spelled exactly as the directory is (`artifacts\InvCov` gives `InvCov`, `artifacts\redfish-test-app` gives `redfish-test`).
  It names the Checkpoint Dir, the **MD report** and the **design pair**.
- **command** — the word on the prompt's third line: **vibe**, **reverse**, **update**, **test**, **start** or **deploy**.
  Exactly one per run, and it decides which step executes.
- **lifecycle** — the one-way order `vibe` → `reverse` → `update`, with **test**, **start** and **deploy** available at any point once there is code.
  It has two doors that open one way only: the first **reverse** closes **vibe** for that **app dir** forever, and the first **update** closes **reverse**.
- **lifecycle record** — `{appDir}\.imp-app.json`, carrying the **phase** and a `history` of every **command** run against this **app dir** with its timestamp.
  It lives in the **app dir** rather than in a checkpoint because the **lifecycle** spans sessions and a per-run file would forget it.
  The app never reads it.
- **phase** — the last state-changing **command** the **lifecycle record** carries: `vibe`, `reverse` or `update`.
  **test**, **start** and **deploy** change nothing and so never change it.
- **adopted** — an **app dir** that already held code when the first **command** ran against it, with no **lifecycle record** of its own.
  It is taken over rather than refused: the record is written, its `history` opens with an `adopted` entry naming what was found, and the **phase** is set from what is on disk — `reverse` if **app documents** are already there, `vibe` if not.
  Nothing about the **fixed shape** is assumed of it.
- **vibe** — the **command** that builds and changes the app straight from prose, with no document in the way.
  It repeats for as many prompts as it takes, and it is the only **command** allowed to write code that nothing describes.
- **reverse** — the **command** that ends the **vibe** coding: it reads the app's own source and its running page and writes the **app documents** out of them.
  It may repeat until the first **update**, and never after it.
- **update** — the **command** that changes an already-documented app: **app documents** first, code second, as many times as it takes.
- **test** — the **command** that asks whether the app is right, in two halves: the **unit tests**, then the **UI test**.
  It changes nothing in the **app dir**.
- **start** — the **command** that starts what is already in the **app dir**, confirms it answers, says where, and stops.
  It is for a reader who wants to **use** the app, so unlike **test** it checks nothing beyond the server being up and judges nothing at all.
- **deploy** — the **command** that delivers the app to a **target**.
  It copies out of the **app dir** and never back into it, and changes nothing there but the **lifecycle record**.
- **the app** — what this skill builds: a self-contained directory started with `node server.js`, whose real work is done by the **python kernel**, both standard library only.
  Node serves and spawns; Python decides.
  It must run with nothing installed.
- **fixed shape** — the layout every app this skill writes has, whatever its requirements ask.
  A **command** changes what the app does, never this:
  - `server.js` at the root, Node standard library only, its `listen` behind `require.main === module`, so requiring the file starts nothing.
  - `app.js` beside it — the **mountable handler**.
  - the **python kernel** under `scripts\`.
  - `public\`, holding the page the server serves by name: markup, styling and behaviour in separate local files, and every address the page emits written **relative to itself** — `./api/x` and `./app.css`, never `/api/x` and `/app.css`.
  - the **app config** beside `server.js`.
  - a `/healthz` route answering what the app resolved at startup — the values it read, the **python kernel** it found, the assembly time — and nothing secret.
  - the **unit tests** under `tests\`.
  - a `start.cmd` and a `README.txt`, so the folder is runnable by someone who was not in the conversation.
- **python kernel** — the Python under `{appDir}\scripts\`, standard library only, spawned by the server and relayed to the page.
  It owns every decision the app's domain needs; **the server parses none of it**, which is what makes swapping the kernel a change to the app.
- **app config** — the `app.config.json` beside the **app dir**'s `server.js`, and the **only** file the app reads.
  Every value the server or the **python kernel** would otherwise ask this skill for is carried here, which is what lets the folder be copied to a **target** and run there unchanged.
- **mountable handler** — `app.js` beside `server.js`, exporting `createApp(options)` and returning the `(req, res)` function the server would have listened with.
  It is how an app is served by something other than itself: a hub requires it, calls it once, and answers for the app under a path of its own.
  Owning a port and answering requests are separable, and only the first is about owning an address.
- **unit tests** — the tests under `{appDir}\tests\`, standard library only: `unittest` for the **python kernel**, `node:test` for the server.
  They are part of the app, not of this skill, so they run on a machine with nothing installed.
  Two names are discovered and no others — `tests\test_*.py` and `tests\*.test.js` — because a test file nothing runs reads exactly like one that passed.
- **UI test** — the judged half of **test**: the page driven in a real browser and read element by element against the **wireframe pair**.
  Fetching markup is not one.
- **app documents** — the **design pair** and the **wireframe pair** together, under `{appDir}\docs\`.
  **reverse** writes them, **update** changes them, and from the first **reverse** onward they, not the prompt history, say what this app must be.
- **design pair** — `{appDir}\docs\{app name}-RSDC.md` and its 繁體中文 twin `{app name}-RSDC-tw.md`.
  Written to the **RSDC** standard, they decide *what the app must be*.
- **RSDC** — Requirements, Specification, Design, Coding: the four parts of a **design pair** document, in that order.
- **wireframe pair** — `{appDir}\docs\Wireframe.md` and its 繁體中文 twin `Wireframe-tw.md`.
  They are the page's element inventory — every panel, control, table column and visibility state — read off the **running** page rather than written from the markup.
  The pair owns that inventory: nothing else restates it.
- **document templates** — `assets\Wireframe-tmp.md` in this skill, and `RSDC-App-tmp.md`, the design template **gen-rsdc-app** writes the **design pair** to.
  They own the **shape** of a **app document** — which numbered sections it carries and what each one holds — so that two apps documented a year apart can be read the same way.
  A step points at them and never restates the section list.
- **RSDC standard** — the chapter-responsibility rules the **design pair** is written to: which question each of the four parts answers, and what each may not reach forward into.
  The **document templates** carry its shape; it carries the reasoning, and is the reference a disagreement about where something belongs is settled against.
- **gen-rsdc-app** — the skill **reverse** runs to write the **design pair**: it reads the app's source, draws the **components** and writes the English half to its design template, after checking that template against the **RSDC standard**, then has the `chinese` skill write the twin.
  It changes no code, and hands back what it wrote.
- **component** — one implementable piece of the app that has one job: the server, the **mountable handler**, one page, one **python kernel** entry point.
  The **design pair**'s Design part draws the boundaries, and every component is named in at least one **verification obligation**.
- **verification obligation** — a row of the **design pair**'s Verification Obligations, in its Coding part: a claim, the rule it proves, the observation that proves it and who makes it — or *not verified*, with what has been read so far.
  Every **component** is named in at least one; the rows are the only definition of "proved" this skill has.
- **prompt log** — the ordered record of every **vibe** and **update** request, what it changed and how that change was proved.
  It accumulates in the YAML checkpoint and is rendered into `{appDir}\docs\Prompts.md` — the history of *why* the app is shaped as it is, which the code cannot show.
- **target** — a destination the app is delivered to, named on the prompt's fourth line and resolved through the **target list**.
  It is a copy of this app somewhere else, never a second source.
- **target list** — the `targets` **list** of the **skill config**: one entry per destination, each carrying a `name`, the `appDir` the code goes to **on that machine**, and the **app config** values that are true there and false in the **app dir**.
  A **target** is this same app somewhere else, so an entry says only what differs about that somewhere.
  It is the reviewed list a **deploy** resolves a name against, which is why a destination is never a path typed into a prompt.
- **skill config** — `assets\config.yaml` in this skill, carrying the **target list**.
  Only this skill's own tools read it; no app ever does, and it does not travel with a **deploy**.
- **session resolver** — `resolve_session.py` in this skill's `scripts\`.
  It stamps the app's Checkpoint Dir on the first **command** and reopens the newest existing one on every later invocation, so two invocations of one app cannot land in different directories.
- **test runner** — `run_tests.py` in this skill's `scripts\`.
  It discovers and runs the **unit tests** and prints one JSON result.
  It is this skill's tool, not part of the app.
- **deploy tool** — `deploy_app.py` in this skill's `scripts\`.
  It resolves a **target** through the **target list** and delivers the app to it.
- **server origin** — `http://127.0.0.1:{port}`, where the port is the **app config**'s `port`.
- **target origin** — the same for a **target**: the host and port that destination's own **app config** carries.

# CONFIGURATION

Concrete values this skill runs with.
Every path below is a constant of the skill; everything about the app being worked on is read from the **app dir** the prompt names.

- **Checkpoint Dir** — `checkpoints\imp-app\{app}-{yymmdd-hhmm}\`, where `{app}` is the **app name** and `{yymmdd-hhmm}` is stamped by the **first** **command** run against that **app dir**.
- **YAML checkpoint** — `process.yaml` inside the Checkpoint Dir.
- **MD report** — `{wikiDir}\imp-app\imp-app-{app}-{yymmdd-hhmm}.md`, carrying the same `{app}` and stamp as the Checkpoint Dir, where `wikiDir` comes from the workspace [config.yaml](config.yaml) (resolved in Step 0) — never hardcode the wiki root.
- **lifecycle record** — `{appDir}\.imp-app.json`.
- **app documents** — `{appDir}\docs\`.
- **prompt log** — `{appDir}\docs\Prompts.md`.
- **document templates** — `{skillGroups.common}\skills\gen-rsdc-app\assets\RSDC-App-tmp.md` and `{skillGroups.common}\skills\imp-app\assets\Wireframe-tmp.md`.
- **gen-rsdc-app** — `{skillGroups.common}\skills\gen-rsdc-app\SKILL.md`.
- **RSDC standard** — `{skillGroups.common}\references\RSDC-Standard.md`, with its diagram notation in `{skillGroups.common}\references\DFD.md`.
- **skill config** — `{skillGroups.common}\skills\imp-app\assets\config.yaml`.
- **session resolver** — `{skillGroups.common}\skills\imp-app\scripts\resolve_session.py`.
- **test runner** — `{skillGroups.common}\skills\imp-app\scripts\run_tests.py`.
- **deploy tool** — `{skillGroups.common}\skills\imp-app\scripts\deploy_app.py`.
- **shared report rules** — `{skillGroups.common}\rules\report-md-rules.md`, `{skillGroups.common}\rules\report-yaml-rules.md` and `{skillGroups.common}\rules\scratch-rules.md`.

# MUST FOLLOW

- **The documents decide what the code is — from `reverse` onward, and the exception is the point.**
  **vibe** is the one **command** allowed to write code that nothing describes, because at the start there is nothing yet to describe and a design written then would be a description of a guess.
  **reverse** ends that, and after it **update** changes the **app documents** before the code.
  At no point after **reverse** is code written first and described afterwards — a design produced that way is a transcript, and worth nothing to the next reader.
- **The lifecycle runs one way, and each door closes behind it.**
  Once the **lifecycle record** carries a `reverse`, **vibe** is refused for that **app dir** for good; once it carries an `update`, **reverse** is refused too.
  - **What that costs is worth naming.**
    After the first **update** there is no re-derive-the-documents path: every document change is made by hand against the **app dir**'s own files.
    That is deliberate — a design re-derived from source would delete exactly what the source cannot show: a cost that was accepted, an alternative that was rejected, a defect that was recorded.
    **reverse** was available for as long as the documents had nothing of their own to lose.
- **If the code has moved since the documents were written, say so before changing either.**
  Compare the **app dir**'s code mtimes against the **app documents**; a hand edit made outside this skill is the usual cause.
  Updating a design the code has already passed writes the change into a document that was already wrong.
- **Every document is a pair, and both halves move together.**
  A section written or changed in `{app name}-RSDC.md` is written or changed in `{app name}-RSDC-tw.md` in the same run, under the same number; the **wireframe pair** carries the same rule.
  Two files that drift no longer say what the app is; they argue about it.
- **Keep every heading of a 繁體中文 twin in English** — character for character as its source has them — so the two can be read side by side and a reviewer can see at a glance that nothing is missing.
  File names, paths, config keys, checkpoint field names and glossary terms keep their original form too; the prose around them is what is translated.
- **The chapters of a design pair run one way.**
  Requirements states no technical choice, Specification names a component only by the interface its callers use, Design names no library or syntax, and no section points at one numbered after it.
  A term borrowed from a later chapter settles there a question that chapter exists to answer, and the reader can no longer tell what was needed from what was built.
  The **RSDC standard** is what a disagreement about where something belongs is settled against.
- **The app documents never name this skill, a command, or any of its tools.**
  A design that points at the procedure that produced it is half of a circular definition, and leaves no single source.
  A document states its own authority without naming what it outranks: *any implementation disagreeing with this document is what changes*.
- **Node serves and spawns; the python kernel decides.**
  The server parses none of the domain.
  A server that has grown a domain rule is a boundary in the wrong place — move the boundary rather than threading the value through.
- **The app must keep working with no skill present.**
  Everything a user does routinely is reachable from its page, with Node and Python standard library only — no `npm install`, no `pip install`, no package, no CDN, no font fetched at load.
  The skills exist to build and change the app, not to operate it.
  - The **skill config** does not travel with the app, so a component that finds no `config.yaml` beside it treats that as **normal, not fatal**: in the **app dir** and on a **target** there is none, and every value it would have read is already in the **app config** or on its command line.
- **The app is production code, however it was written.**
  No secret on a command line — a process list is readable by every other process, so a password reaches Python on **stdin** or not at all.
  No host, path or URL taken from a browser and used unchecked: an allow-list decided by the app, enforced again inside the **python kernel**, is what keeps the server from being a relay into the network behind it.
  Escape every value that reaches the page.
  **Never weaken one of these to make a command pass** — if a guard blocks a change, the change is wrong; say so and propose the version that is not.
- **A new value belongs in the app config; a new behaviour belongs in the python kernel.**
  If a change can be made by adding a key rather than a branch, add the key — that is what keeps the next change from needing this skill at all.
- **Every app is mountable, and both halves of that are written from the first cut.**
  It publishes a **mountable handler**, and its `server.js` keeps the `listen` behind `require.main === module`.
  Its page addresses the server relative to itself, and a page the server *generates* several segments deep computes its way back rather than assuming it is at the root.
  - This is in the **fixed shape** rather than added when a hub appears, because **neither failure is visible in a reading**.
    An unguarded `listen` only shows when the file is required; an absolute address only shows when the app is served under a path — both at the moment somebody else depends on it.
    Retrofitting one app is an afternoon of document changes in two languages; writing it correctly costs a dozen lines.
- **The target is the source, and nothing in it is a build product.**
  No **command** regenerates the **app dir** from anything else, and a **deploy** copies out of it and never back into it.
  What sits on a **target** is a copy; what sits in the **app dir** is the app.
- **A change is not finished until the unit test that would have caught its absence exists.**
  **vibe** and **update** each write it in the same round as the change.
  A round with a change and no test is recorded as **unproven**, not as done.
- **`test` has two halves, and the checked one is not the step.**
  Every **unit test** passes on a page nobody can use, which is the whole reason the **UI test** exists.
  A **test** that reports the unit results and stops has not finished.
  A run that found **zero** tests reports zero — never green — and every source file no test so much as mentions is named, as is every test file named so that neither runner would discover it.
- **The UI test is driven, not read.**
  The live DOM in a real browser, not the markup file, and every **visibility state** the **wireframe pair** records is reached before it is judged.
  A state nobody opened is a guess, and a status code is not an appearance.
- **`test`, `start` and `deploy` change nothing in the app dir.**
  Either of the first two that finds a defect **names it and stops**; fixing it is an **update**, or a **vibe** while that is still open.
  **deploy**'s only write into the **app dir** is its own **lifecycle record** entry.
- **`vibe`, `reverse` and `update` do not leave a server running.**
  Writing and verifying are asked for separately, so an iteration is not charged the cost of a review nobody wanted yet.
  Each of the three therefore ends by saying what it has **not** observed, and naming **test** or **start**.
- **A target is named by the registry, never by a path in the prompt.**
  A path in a prompt is unreviewed input that reaches a filesystem — possibly someone else's.
  The **target list** is the reviewed list, and a target that is not in it is a stop saying what to add, not a guess.
  **Naming one is not optional either**: a **deploy** that named none is refused and lists the names, and `all` is how every one of them is asked for.
  Writing to somebody else's machine is not a default.
- **One app dir per run.**
  The **command** applies to exactly one **app dir**.
  A run never works on two, and never falls back to "the only one" when the prompt named none — it asks.
- **Never hardcode an app.**
  No **app name**, **app dir** path, port, title, endpoint or **target** may appear in this file, in the **document templates**, or in this skill's tools.
  The prompt names the **app dir**; the **skill config** names the **targets**.
- **Every command appends to the lifecycle record.**
  A **command** that changed the **app dir** and did not record itself leaves the next run to guess the **phase**, and the gate is only as good as what it reads.
- **Every output of one app carries the one `{yymmdd-hhmm}` stamp** — one Checkpoint Dir and one **MD report** per app, stamped by the first **command** and appended to by every later one.
  The **app dir** itself is **unstamped**: it is the current app, and stamping it would leave a trail of stale copies where a reader expects one folder.
- **The MD report is created once per app and appended to thereafter.**
  The create rule in the **shared report rules** clears everything after the header when the file already exists; that applies to a *new* run, and a later **command** here is the *same* session.
  So on a later invocation, refresh the header's **Updated** field and **append** the new section — never clear the body, which is the only record of what the earlier **commands** did.
- Must run workflow step by step, and display each step number.
- Each step must be self-contained.
  **No forward-reference.**
- A step that a program can do deterministically must be run as a script.
  A step that needs reading, judgement, or summarization **must not** be scripted — write it as natural-language instructions for the agent to perform directly.
- **Honour a `run step N` selector**: run Step N, then stop; never a later step.
- Follow `{skillGroups.common}\rules\report-md-rules.md` for the MD report's header and shape.
- Follow `{skillGroups.common}\rules\report-yaml-rules.md` for the YAML checkpoint's shape and required fields.
- Follow `{skillGroups.common}\rules\scratch-rules.md` for where a run's throwaway files go and how they are cleaned up — every probe, every throwaway copy of the **app dir** and every captured output is exactly that.
- **Every JSON in the Checkpoint Dir has exactly one writer step.**
  The step that produces a data file writes it whole and owns it; a later step that concludes something writes its own `step_{N}.json` beside it, and never adds to, edits or deletes a key in a file another step wrote — not even to supersede it.
  The YAML checkpoint is the one exception: it is appended to, one `step_{N}` group per step, rather than rewritten.
  A data file several steps write back into is lost the moment its first step is re-run — a parser fix or a `run step 1` rewrites it whole and erases every later step's result without a word.
- **Before the skill ends, display the server origin, app dir, MD report and YAML checkpoint** — show only those four, and render each as a clickable Markdown link.
  The **server origin** is an `http://` URL and links as itself, and is shown only by the **commands** that started a server — **test**, **start**, and a **deploy** that could start the app on its **target**, which shows the **target origin** beside it; **vibe**, **reverse** and **update** omit it, having left nothing running.
  The MD report lives in the vault, outside this workspace, so link it with an `obsidian://open?vault={vaultName}&file=<vault-relative-path>` URI (e.g. `[imp-app-InvCov-260924-1130.md](obsidian://open?vault={vaultName}&file=imp-app/imp-app-InvCov-260924-1130.md)`); the **app dir** and the YAML checkpoint keep a workspace-relative, forward-slash target (e.g. `[process.yaml](checkpoints/imp-app/InvCov-260924-1130/process.yaml)`).
  - Do this for every run, including a partial one such as `run step 0`.

# Prompt Examples

## Prompt 1

```
/imp-app
artifacts/InvCov
vibe
Read InvDatabase/data and show each stock's coverage as one row.
Start it with node server.js. Do the real work in Python.
```

## Prompt 2

```
/imp-app
artifacts/InvCov
reverse
```

## Prompt 3

```
/imp-app
artifacts/InvCov
update
Add a 缺漏天數 column, and sort the table by it descending.
```

## Prompt 4

```
/imp-app
artifacts/InvCov
test
```

## Prompt 5

```
/imp-app
artifacts/InvCov
start
```

## Prompt 6

```
/imp-app
artifacts/InvCov
deploy
nuc-win
```

## Prompt 7

```
/imp-app
artifacts/InvCov
start
run step 0
```

# Workflow

Each step opens with a **Purpose**: one sentence saying why that step exists as a step — what this skill would lose by folding it into its neighbour.

**The command routes the run.**
Step 0 runs always and is where the gate is enforced.
Step 1 runs for **vibe** only, Step 2 for **reverse**, Step 3 for **update**, Step 4 for **test**, Step 5 for **start**, Step 6 for **deploy**.
Naming those steps here is routing, not a forward-reference: no step borrows a later step's output.

**No command both changes the app and judges it.**
**vibe**, **reverse** and **update** end with files on disk and leave nothing running; **test**, **start** and **deploy** write nothing into the **app dir** but its **lifecycle record** entry.
That split is what lets an iteration cost only what it changed, and it is also what stops a run from implying it checked something it never looked at.
The price is that a **vibe** or an **update** can finish with the app never having been served afterwards — stated, not hidden.

**Steps 0, 4 and 6 run a script and Steps 1, 2, 3 and 5 do not**, because stamping a session, discovering and running tests, and copying a tree to a reviewed destination are deterministic, whereas writing an app from prose, deriving a design from source, carrying a change through a design into code, and reading a page as a user would are judgement.
Step 4 carries both halves of that split and names them as halves, so the judged one cannot be lost behind the checked one.

## Step 0 - Warmup

- **Purpose**: settle which **app dir** is being worked on, which **command** applies, and whether the **lifecycle** permits it — the gate has to be enforced before anything is written, because afterwards there is nothing to refuse.

- Run `.venv` first — this skill's tools need `PyYAML` to read a config.
  **Node** must be on `PATH` and so must **Python**; check `node --version` and `python --version` both answer, and record them.
  There is nothing to `npm install`.

- Read the workspace config [config.yaml](config.yaml) at the workspace root and resolve:
  - **`wikiDir`**: the MD report root — this skill's report goes under `{wikiDir}\imp-app\`.
  - **`vaultName`**: the last path segment of `wikiDir` (e.g. `InvLlmWiki`) — the Obsidian vault name used to build the `obsidian://` link.
  - **`skillGroups`**: the group name -> skills-root map — this skill's own directory is `{skillGroups.common}\skills\imp-app\`, and the **shared report rules** are under `{skillGroups.common}\rules\`.
  - Substitute the resolved values wherever `{wikiDir}`, `{vaultName}` or `{skillGroups.common}` appears in the steps below, including in commands.
  - If `config.yaml` is missing or a needed key is absent, stop and ask the user.

- This skill calls no API and needs no credential of its own.
  A **target** may need one to be reachable at all; that belongs to whatever already mounts it and to the **target list**, and never to a command line.

- Check the below scripts/files exist before running the workflow.
  - `{skillGroups.common}\skills\imp-app\scripts\resolve_session.py`
  - `{skillGroups.common}\skills\imp-app\scripts\run_tests.py`
  - `{skillGroups.common}\skills\imp-app\scripts\deploy_app.py`
  - `{skillGroups.common}\skills\gen-rsdc-app\SKILL.md`
  - `{skillGroups.common}\skills\gen-rsdc-app\assets\RSDC-App-tmp.md`
  - `{skillGroups.common}\skills\imp-app\assets\Wireframe-tmp.md`
  - `{skillGroups.common}\skills\imp-app\assets\config.yaml`
  - `{skillGroups.common}\references\RSDC-Standard.md`
  - `{skillGroups.common}\references\DFD.md`

- The prompt takes one of the forms shown in **Prompt Examples** above.
  Parse it **positionally**, so a requirement line is never mistaken for an argument:
  - **app dir** — the second line, a directory path.
    If none is given, ask; never pick one.
  - **command** — the third line: `vibe`, `reverse`, `update`, `test`, `start` or `deploy`.
    Any other word, or none, is a stop that lists the six in **lifecycle** order.
  - **target** — for **deploy** only, the fourth line: the `name` of a **target list** entry, or `all` for every one of them.
    If the line is missing, ask and list the names that exist — naming is not optional, so never pick one.
  - **requirements** — for **vibe** and **update**, every remaining prose line, kept **verbatim** in the user's own words: each is one thing being asked for, and each becomes a **prompt log** entry that a paraphrase would lose.
    For **test**, a remaining prose line is instead a **review focus**: something to look at first.
    **reverse**, **start** and **deploy** take none, and prose on one of them is a stop asking which **command** was meant.
  - **referenced notes** — a requirement may name a wiki note (e.g. `note-260824-Mo`).
    Resolve it under `{wikiDir}\write-note\` and read it before doing anything else; it usually carries the requirements the prose only gestures at.
  - an optional trailing **`run step N`** selector.

- Derive the **app name** from the **app dir** and display it with the paths it implies — the Checkpoint Dir, the **MD report** and the **design pair** filenames — before using any of them.
  Let the user override it.

- **Read the lifecycle record and enforce the gate.**
  This is the check the whole **lifecycle** rests on:
  - Read `{appDir}\.imp-app.json` if it is there, and take the **phase** and the `history` from it.
  - A **app dir** that holds code but carries **no** record is **adopted**: write the record, open its `history` with an `adopted` entry naming what was found, and set the **phase** from what is on disk.
    Say plainly that this skill did not write what is there, so nothing about the **fixed shape** is assumed of it.
  - A **app dir** that does not exist, or is empty, is a **vibe** and nothing else.
    Any other **command** against it is a stop saying there is no app yet.
  - **vibe**: refused if `reverse` appears anywhere in `history` — say that this app is documented now and that **update** is how it changes.
  - **reverse**: needs code.
    Refused if `update` appears anywhere in `history` — say that the documents carry decisions the source cannot show and that re-deriving them would delete exactly those.
  - **update**: needs code **and** **app documents**; if the documents are absent, say to run **reverse** first.
  - **test**, **start**, **deploy**: need code.
    Any **phase** that has it is fine.
    None of the three is ever refused for what the **lifecycle** has done — they change nothing, so there is nothing for the gate to protect.

- **For a first `vibe` only**, check the ownership of the **app dir**: search the skills roots of `skillGroups` for another skill whose config claims the same directory.
  If one does, stop, report both claimants, and ask which owns it — two skills writing one directory is how a change disappears without a diff.

- Read the **app config** if the **app dir** has one, for the port and whatever else the app resolves from it.
  Check whether that port is already taken: a live answer usually means an earlier run's server is still up, which is fine — say so, and either reuse it or stop it rather than starting a second one that cannot bind.

- **For `deploy` only**, resolve the **target** through the **target list** of the **skill config** into its destination `appDir` and its own **app config** values; `all` resolves to every entry, in the order the file lists them.
  A name the registry does not carry is a stop listing the names it does.

- Resolve the app's session by running the **session resolver**, which owns this deterministically so two invocations of one app cannot land in different directories.
  - Example: `python {skillGroups.common}/skills/imp-app/scripts/resolve_session.py --app InvCov --command vibe`
  - It reopens the **newest existing** `{app}-*` Checkpoint Dir, and stamps a new one only when there is none — the first **command** against a **app dir** opens the session and every later one joins it, whichever **command** that was.
  - It prints one JSON object carrying `app`, `stamp`, `checkpointDir`, `processYaml`, `mdReport`, `opened` (`created` or `reopened`) and `sessions`.
    Use those paths verbatim for the rest of the run.

- Save the canonical skill invocation for reference in later steps.

- Save YAML checkpoint `step_0` with the resolved `wikiDir`, the **app dir** (as `appDir`, the field the **session resolver** checks a reopened session by), the **app name**, the **command**, the **target** and what it resolved to, the **phase** and `history` read from the **lifecycle record**, whether the app dir was **adopted**, the gate verdict, the port and whether it was in use, the **requirements** verbatim, the **referenced notes**, the Node and Python versions, the stamp and whether the session was created or reopened, the output paths, the step selector, and timing.
  - **`step_0` holds this invocation only** and is overwritten by the next one.
    The run-by-run history is the **lifecycle record**'s and the **prompt log**'s, which is why both live in the **app dir** and not here.

- Display the **app dir**, the **command**, the **phase** and what the gate decided.
  Creating the MD report file is optional in this step.

## Step 1 - Vibe-code the App

- **Purpose**: let the app be found by building it — this is the one phase where prose goes straight to code, because at the start there is nothing yet to describe and a document written then would describe a guess.

- **Runs for the `vibe` command only.**
  For any other **command**, skip to the step that command routes to.

- Read the **app dir**, the **requirements**, the **phase** and whether the app dir was **adopted** back from the `step_0` group of the YAML checkpoint.

- **No script for this step** — writing an app from prose is the whole of vibe coding and needs judgement.

- **On the first round against an empty app dir**, say back in one paragraph what the app is for, what it replaces, and what the user will click.
  Get that agreed **before** writing code: everything after it is built on it.
  On a later round, read the **prompt log** back from the checkpoint first, so this round starts from what the app already is.

- **Write the app to the fixed shape**, and honour the production-code rules in **MUST FOLLOW** from the first cut rather than as a later cleanup.
  An **adopted** app dir is brought to the **fixed shape** one round at a time as the requirements touch each part, and what is not yet in that shape is named rather than assumed.

- For each requirement, in order:
  1. **Locate.**
     Name the files the change touches and say why those and not others.
     A change that touches the server *and* the **python kernel** usually means the boundary between them is in the wrong place.
  2. **Change.**
     Make the edit, keeping the **fixed shape** intact.
  3. **Test.**
     Write or extend the **unit test** that would have caught this change's absence, in this same round.
  4. **Prove.**
     Start the app, exercise the changed path, read what came back, and quote it.
     **Prove the second entry point too** — require `app.js`, call `createApp()`, and answer one request through the handler it returns with no port bound.
     A **mountable handler** that has never been called is a claim.
  5. **Record.**
     Append one **prompt log** entry: the requirement verbatim, the files touched, the test written, the proof, and anything the change revealed that was not asked about.

- **Append to the round list; never overwrite it.**
  `step_1` holds a `rounds` list that grows by one entry per invocation.
  Read it, append, write it back — a round that replaces the list erases the history **reverse** reads, and nothing else holds a copy.

- **Write the prompt log out to `{appDir}\docs\Prompts.md`** as well, in round order.
  It is the only part of `docs\` that exists before **reverse**, and it is why the app is shaped as it is.

- **Append to the lifecycle record**: a `vibe` entry with its timestamp, and **phase** `vibe`.

- **Say what comes next, and what has not happened.**
  There are no **app documents** yet and that is deliberate.
  More **vibe** rounds, or **reverse** when the app is right; **test** or **start** to look at it, which this **command** did not leave running.

- Save YAML checkpoint under `step_1` with: `appDir`, `entry`, `serverPort`, `fixedShapeFiles`, `pythonKernel`, `pageFiles`, `appConfigKeys`, `unitTests`, `rounds` (append one entry carrying `n`, `requirement`, `filesTouched`, `test`, `proof`, `notes`), `roundCount`, `openIssues`, and timing.

- Save MD report file.
  Append to (or create) a **Vibe** section:
  - **Summary line**: what the app is for, the one command that starts it, and how many rounds it has had.
  - **Rounds table**, one row per round, with columns:
    - **#**: the round number.
    - **Asked**: the requirement, condensed to one line — escape any `\|` so a quoted path does not split the row.
    - **Changed**: the files touched.
    - **Test**: the unit test written or extended, or `none` with why.
    - **Proof**: what was run and what came back, quoted rather than characterized.
  - **Open**: what the requirements asked for that the app does not yet do.

## Step 2 - Reverse-engineer the Documents

- **Purpose**: fix in writing what the app **is**, derived from the app rather than from what was asked — the point at which an app stops being a conversation and becomes something a later reader can check it against.

- **Runs for the `reverse` command only.**
  For any other **command**, skip to the step that command routes to.

- Read the **app dir**, the **app name** and the **prompt log** back from the `step_0` and `step_1` groups of the YAML checkpoint.
  An **adopted** app dir has no **prompt log**; say so — the design is then derived from the source alone.

- **No script for this step** — the **design pair** is derived by **gen-rsdc-app**, and reading a running page is judgement; a program asked to do either would only be asserting it had.

- **Write the design pair with gen-rsdc-app.**
  Run it on the **app dir**, naming the **app name**, `{appDir}\docs` as where the pair goes, and the **prompt log** — or `none` for an **adopted** app dir:

  ```
  /gen-rsdc-app
  {appDir}
  {app name}
  {appDir}\docs
  {appDir}\docs\Prompts.md
  ```

  - It checks its design template against the **RSDC standard** first, and stops before writing anything if the template has fallen behind.
    A stop there stops this **command** too: say so, and that the template is **gen-rsdc-app**'s to bring up to the standard.
  - It replaces a **design pair** already in `{appDir}\docs\` whole — which the gate allows only until the first **update**.
  - It derives the design from the source rather than from the **prompt log**, and records each disagreement between them as a finding.
    Read back what it hands back — the **components**, the findings, the defects, the **verification obligations**, what its check of the English half found and what the `chinese` skill reported of the twin — for the checkpoint and the report below.
  - The `chinese` skill it runs asks whether to commit the **design pair**: pass the question to the user.
    The commit holds the pair alone, and this **command** goes on whatever the answer.

- **Scan the running page into the wireframe pair** — `{appDir}\docs\Wireframe.md` and `Wireframe-tw.md`, both in the same run, to the shape `Wireframe-tmp.md` carries:
  - Start the app and open its page in a browser, and read the **live DOM** — not the markup file.
    An inventory written from the markup lists what the author believes the page has, and finding out is the point of the scan.
  - Walk the page top to bottom, one bullet per element, each tagged with its kind — `[Panel]`, `[Button]`, `[Select]`, `[Input]`, `[Text]` and so on — and carrying the label a user actually sees, not the element's id.
  - Render every table as a table of its own columns, in the order the page shows them.
  - Record the **visibility states**: which parts are hidden until something happens, and what makes each appear.
    Exercise the page far enough to reach each one before writing it down — a wireframe of only the opening screen documents a fraction of the app.
  - Where the scan reveals a defect, write it in the wireframe as a defect **and** in the design pair's Defects as one.
    An element that shows a wrong value is still an element; the wireframe records both facts.

- **Append to the lifecycle record**: a `reverse` entry with its timestamp, and **phase** `reverse`.
  If this is the first one, say plainly that **vibe** is now closed for this **app dir** and **update** is how it changes from here.

- **Say what comes next, and what has not happened.**
  This **command** wrote documents and changed no code, and it left nothing running.
  The next **command** is **test**, or **update** for the first change against the documents.

- Save YAML checkpoint under `step_2` with: `components`, `designPair`, `wireframePair`, `sectionsWritten`, `wireframeScan` (how the page was reached and which visibility states were opened), `findings` (each disagreement between source and **prompt log**), `defects`, `verificationObligations`, the **lifecycle record** appended, and timing.

- Save MD report file.
  Append and display a **Documents** section:
  - **Summary line**: the four documents written, how many **components** they name, how many findings and defects came out of the scan, and that no code changed.
  - **Documents line**: the **design pair** and the **wireframe pair** as four links, with the section counts the two halves of each pair were matched on.
  - **Components table** with columns:
    - **Component**: its name in the design pair.
    - **File**: where its source lives in the **app dir**.
    - **Obligations**: the claims of the **verification obligations** that name it, each one not yet proven marked *not verified*.
  - **Findings table** with columns:
    - **Asked for**: the **prompt log** entry, or `—` for an **adopted** app dir.
    - **What the code does**
    - **Recorded as**: the section that now carries it.

## Step 3 - Update the Documents then the Code

- **Purpose**: carry a change through the design and into the code in that order, which is the only order that leaves the documents worth reading afterwards.

- **Runs for the `update` command only.**
  For any other **command**, skip to the step that command routes to.

- Read the **app dir** and the **requirements** back from the `step_0` group of the YAML checkpoint, and read the **app documents** themselves before changing anything.

- **No script for this step** — deciding what a requirement means, where in the design it belongs, and what code it implies is judgement.

- **For each requirement, decide first where it lands in the app documents**, then write it there:
  - **Route it by the repaint test, not by topic.**
    A statement that stays true when the page changes colour is a **design pair** change — a numbered section, amended or added.
    A statement that would stop being true belongs in the **wireframe pair**, with the elements it describes.
  - So: what the app does, what a value *means* to a reader, and what a change costs are **design pair**.
    Colour, hover, typeface, and the page's element inventory are **wireframe pair**.
    "What the page shows" splits across both, which is why the test is the wording of the statement rather than its subject.
  - A change that fits nowhere in the documents is a change that does not belong in the code either.
    Say so and ask, rather than writing it into the code alone.
  - **Write both halves of every pair in this run**, under the same numbering.
  - **State the cost of a change that removes something**, in the document: what this app can no longer do, and why that was worth it.
  - **Neither document may name the other.**
    Each states its own scope; a rule needing a reason from the other is given that reason in full, in its own words.
    A section number in the other file is a link that rots without anyone noticing.

- **Then change the code to match**, editing the **app dir**'s own files and keeping the **fixed shape** intact.
  A new **value** goes into the **app config**; a new **behaviour** goes into the **python kernel**.

- **Write or extend the unit test that would have caught the change's absence**, in this same round, and add or amend the **verification obligations** that name a **component** it changed, for anything new the change gives that component to be proved by.

- **Re-prove what the change could have broken**, on a spare port against a throwaway copy of the **app dir** under the workspace `temp\` — never the real port and never the **app dir** itself.
  Re-run the **verification obligations** that name a **component** this change touched, and the **unit tests** for the files it changed.

- **Append to the lifecycle record**: an `update` entry with its timestamp, and **phase** `update`.
  If this is the first one, say plainly that **reverse** is now closed for this **app dir**.

- **Append the round to the prompt log**, in the checkpoint and in `{appDir}\docs\Prompts.md`.

- **Say what comes next, and be exact about what the probes above did and did not prove.**
  They ran against a throwaway copy, so they prove the change did not break what they cover — not that the **app dir** serves.
  The next **command** is **test**, or **start** to simply bring it up.

- Save YAML checkpoint under `step_3` with: `updates` (append one entry carrying `n`, `requirement`, `documentSections`, `filesChanged`, `test`, `probes`, `results`, `costsRecorded`), `updateCount`, `verificationObligations`, the **lifecycle record** appended, and timing.

- Save MD report file.
  Append to (or create) an **Update** section:
  - **Summary line**: how many requirements this round carried, whether this run was the one that closed **reverse**, and that the **app dir** itself has not been served.
  - **Changes table** with columns:
    - **Asked**: the user's own words.
    - **Document**: the section of the pair it was written into.
    - **Code**: the app dir files it then changed.
    - **Test**: the unit test written or extended.
    - **Proved by**: the probe re-run for it, or why none was needed.

## Step 4 - Test the App

- **Purpose**: the one place the app is asked whether it is **right**, in the two ways that answer different questions — what a machine can check about it and what only a reader looking at the page can see.

- **Runs for the `test` command only.**
  No other **command** judges the app.

- Read the **app dir**, the port and any **review focus** back from the `step_0` group of the YAML checkpoint.

- **This step has two halves and they run in that order: first what is checked, then what is judged.**
  The first is scripted and deterministic; the second is neither, and cannot be made so.
  **The checked half passing is not this step passing** — every **unit test** passes on a page nobody would want to use, which is the whole reason the second half exists.

### The checked half

- **Run the test runner**, which owns discovery and execution so that a test cannot be silently skipped.
  - Example: `python {skillGroups.common}/skills/imp-app/scripts/run_tests.py --app-dir artifacts/InvCov --out "checkpoints/imp-app/InvCov-260924-1130"`
  - It discovers the **unit tests** under `{appDir}\tests\`, runs the `unittest` ones against the **python kernel** and the `node:test` ones against the server, and prints one JSON result carrying each test's outcome, the counts, every source file no test so much as mentions, and every test file named so that neither runner would have discovered it.
  - It saves that result as `unit-tests.json` in the output directory.
  - **It exits non-zero when a test failed or when nothing ran.**
    That is the app's verdict, not a fault in the tool: read the result and carry on with this step rather than re-running it.
  - **A file no test mentions is a fact about the tests, not a coverage claim.**
    Whether a file that *is* mentioned is actually exercised is judgement, and the runner deliberately does not assert it — map each result onto a **component** yourself: find the **verification obligation** whose Proven by or Performed by names the test, and take the component that row names.
- **Zero tests is zero, never green.**
  A source file the runner found no test mentioning is named in the report as untested, and a run that found no test at all is a stop saying which tests to write — not a pass.
- **Read every failure, and quote what it said.**
  A failure is a finding about the app, not about the runner, and it is named here rather than fixed: fixing it is an **update**, or a **vibe** while that is still open.

### The judged half

- **Start the server as a background process** and leave it running — it is a server, not a one-shot script, and this half begins when it answers, not when the command returns.
  - Example: `node {appDir}/server.js`
  - Use an absolute path.
    The app resolves every path against its own directory, so the **app dir** is the only place it runs.
  - If the port was already in use, stop that server first rather than starting a second one that cannot bind.
- **Confirm the server answers before going on.**
  Ask `{server origin}/healthz` and record what it said it resolved.
- **Drive the page in a real browser, as a user would** — the `playwright-cli` skill is how.
  A **UI test** that only fetched HTML is recorded as **not having been run**: a status code is not an appearance, and a stylesheet that was fetched is not a stylesheet that reads well.
  - Look first at whatever the **review focus** asked to be looked at, then at the page as a whole.
  - Exercise every interaction the **wireframe pair** records a **visibility state** for, and reach each state before judging it.
  - Confirm by looking, not by trusting a count: the values shown are the ones the **python kernel** returned, every address the page loads is on the **server origin**, and nothing is fetched from outside it.
- **Ask a probe what it would prove before trusting what it reported.**
  A check that cannot fail, or that a browser quietly satisfied on the app's behalf, reads exactly like a check that passed — a redirect followed automatically, a header read in the wrong case, an empty table that renders identically to a filtered one.
- **Reconcile the page against the wireframe pair**, element by element — it is a prescriptive inventory, so every row it marks required must be on the page:
  - A page missing something the wireframe requires is a defect.
    Name it; do not fix it here.
  - A page carrying something the wireframe does not list is also a defect: either the element should go, or the wireframe should have said so.
    Name which end should change, and leave it.
  - **Report it and stop — this command cannot record it.**
    The wireframe is an **app document**, and only **update** writes those.
    So a defect found here is written down one **command** later, and the report must carry enough for that **update** to be written without re-observing anything.
- Do not repair the app, restart another server, or edit anything in the **app dir**.

- Save YAML checkpoint under `step_4` with: `tests` (append one entry per invocation carrying the **server origin**, the port and host bound, the process id, the Node and Python versions, the `/healthz` response, the unit-test counts and each failure, the browser the page was driven in, every **visibility state** reached, the wireframe reconciliation, the defects found, the overall verdict and the recommended next **command**), `testCount`, and timing.

- Save MD report file.
  Append to (or create) a **Test** section:
  - **Summary line**: how many **unit tests** passed and failed, how many **components** have none, what the **UI test** was driven in, how many defects came out, and which **command** comes next.
  - **Unit tests table** with columns:
    - **Test**: the test's name as the runner reported it.
    - **Component**: which **component** it covers, read from the **verification obligation** whose Proven by or Performed by names the test — the runner does not decide this.
    - **Result**: pass, fail with what it said, `skip` with why, or `no test mentions this file` for a source file nothing named.
  - **UI test table** with columns:
    - **Interaction**: what was done to the page.
    - **Expected**: what the **wireframe pair** or the **design pair** says should follow.
    - **Observed**: what the page actually showed, quoted rather than characterized.
    - **Verdict**
  - **Defects**: each one, where it was seen, and which document an **update** must change for it.
  - **Notes**: anything seen rather than inferred, and anything the **app documents** already accept as a cost rather than a defect, named as such so a later reader does not reopen it.

## Step 5 - Start the App

- **Purpose**: bring the app up for someone who only wants to use it, and charge them nothing else — a **start** that ends in a verdict on the page has quietly become a **test**, which is worse than either, because the caller asked for neither.

- **Runs for the `start` command only.**

- Read the **app dir** and the port back from the `step_0` group of the YAML checkpoint.

- **No script for this step** — it is one command and one request, and wrapping those in a program would only hide which of them failed.

- **Start the server as a background process** and leave it running.
  - Example: `node {appDir}/server.js`
  - Use an absolute path, for the reason the app resolves its own paths that way.
  - If the port was already in use, say so and either reuse that server or stop it — never start a second one that cannot bind.

- **Ask `{server origin}/healthz`, report the server origin, and stop.**
  This **command** does not open the page, does not compare it to anything, and reaches no verdict.
  If `/healthz` does not answer, say what it said or that it said nothing, and stop there — diagnosing it is a **test**.

- Save YAML checkpoint under `step_5` with: `starts` (append one entry carrying the **server origin**, the port and host bound, the process id, the Node and Python versions and the `/healthz` response), `startCount`, and timing.

- Save MD report file.
  Append to (or create) a **Start** section: **one summary line and nothing else** — the **server origin** and what `/healthz` reported.
  No tables and no verdict, because this **command** looked at nothing.

## Step 6 - Deploy the App to a Target

- **Purpose**: put the app where it will actually be used, with the values that destination needs rather than the ones the **app dir** develops against, and prove the delivery instead of assuming it.

- **Runs for the `deploy` command only.**

- Read the **app dir**, the **target** and what it resolved to back from the `step_0` group of the YAML checkpoint.

- **If the phase is `vibe`, say so before delivering**: what is going out has no **app documents**, so nobody on the other end can check it against anything.
  That is a warning and not a refusal — whether to ship it is the user's call, not this skill's.

- **Prove the app runs here before sending it there.**
  Start it, ask `{server origin}/healthz`, and stop it.
  Shipping an app that does not start locally sends the same failure somewhere with less to debug it.

- **Run the deploy tool**, which owns the copying so that the same files reach every **target** the same way.
  - Example: `python {skillGroups.common}/skills/imp-app/scripts/deploy_app.py --app-dir artifacts/InvCov --target ftp-server --out "checkpoints/imp-app/InvCov-260924-1130"` — `--target` repeats, and `--all` is every registered one.
  - It resolves each **target** through the **target list**, copies the code to that entry's `appDir`, writes that destination's own **app config** from that target's values over the **app dir**'s, and prints one JSON manifest of what it wrote, what was already current and what it left alone.
    It saves one `deploy-{target}.json` per target in the output directory.
  - **It sends the code, and only the code**: `server.js`, `app.js`, `start.cmd`, `README.txt`, `public\` and `scripts\`, plus the **app config** it writes.
    The **app dir**'s `docs\`, `tests\` and **lifecycle record** stay in the **app dir** — that is the app's history and its source of record, so a fault found on a **target** is reproduced in the **app dir** rather than there, which is the right place for it since that is where a fix would be written anyway.
    A **target**'s own `data\`, `logs\` and `temp\` are **that machine's** — what it downloaded, what its own runs printed — and overwriting them would take away work it did for itself.
  - **A file is current at the target when its size and its modification time both equal the app dir's**, and it is copied when either differs.
    The two are comparable only because the copy carries the source's time over, so both values come from **this** machine's clock and the two machines' clocks never enter into it — which is what a plain "the target's copy is older" test gets wrong.
    Testing equality rather than "newer" is also what still catches a source rewritten to the same length, and what still replaces a hand edit made at the **target** rather than mistaking it for something newer than the **app dir**.
    `--force` copies every file regardless of the comparison.
  - **One unreachable target does not stop the others.**
    Each is reported on its own, and the exit code says whether any failed — a share that is not mounted today is not grounds to abandon the machines that are.
  - **It never writes into the app dir** and never takes a destination path from the prompt.
  - **No secret on a command line.**
    A destination that needs a credential is reached by something that already holds it — a mounted share, a key the **target list** names — never by a password in an argument, which every other process on this machine can read.
  - **`--dry-run` plans and manifests the delivery without writing anything**, which is how a new **target** entry is checked before it is trusted.

- **Then confirm what arrived.**
  If the app can be started on the **target** from here, start it, ask `{target origin}/healthz`, and report both origins.
  If it cannot, say plainly that the delivery was verified by **the manifest and the file comparison only** and that **nothing was observed running** there — a copied file is not a running app.
  Where anything was written, say that the server at that **target** has to be restarted, since Node does not reload `server.js`.

- **Append to the lifecycle record**: a `deploy` entry with its timestamp and the **target** it went to.
  The **phase** does not change: a **deploy** changes nothing about what the app is.

- Save YAML checkpoint under `step_6` with: `deploys` (append one entry per **target** carrying its `name` and destination `appDir`, whether it was reachable, the **target origin**, the files written with sizes, the files already current, what was left alone there, the **app config** values written for that destination and which of the **app dir**'s they replaced, the local proof, and how the arrival was confirmed), `deployCount`, `phaseAtDeploy`, the **lifecycle record** appended, and timing.

- Save MD report file.
  Append to (or create) a **Deploy** section:
  - **Summary line**: each **target**, where the app now sits on it, how many files were written and how many were already current, whether it was observed running there, and the **phase** it was deployed from — including the warning, when that phase was `vibe`.
  - **Files table** with columns:
    - **File**: the path relative to the destination `appDir`.
    - **Size**
    - **State**: written, already current, or failed with what it said.
  - **Verification table** with columns:
    - **Check**: what was asked — the local start, the manifest, the size-and-time comparison, the remote `/healthz`.
    - **Result**: what came back, quoted rather than characterized, or `not run` with why.
  - **Notes**: what differs between the **app dir**'s **app config** and the one written for each **target**, what was left alone on that machine, and anything the destination needs that this **command** did not put there.
