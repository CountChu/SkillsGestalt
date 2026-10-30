---
name: imp-home
description: >-
  Carries a hub app through a five-command lifecycle in a target directory the prompt names. A hub
  is a Node server (`node server.js`) serving one page of buttons, one per entry of its link list,
  and an `app.config.json` that carries them. The prompt's second line is the `target` and its third
  is the `command`: `setup` creates the target frame and its `app.config.json` once, seeded from the
  hub named on the line after the command, so a target need not be called what its seed is; `gen`
  writes the app **from the design in the skill's references** - an RSDC document and a wireframe,
  each in
  English and 繁體中文 - and then copies those same documents into the target, so a hub is never code
  without the design it was generated from; `update` then changes that design first and the code
  second, so the documents never trail the thing they describe. Neither `gen` nor `update` serves
  what it wrote - writing and verifying are asked for separately, so an iteration is not charged the
  cost of a review nobody wanted yet, and a run never implies it checked something it did not.
  `test` serves it and reads it as a reader would, for a reader who wants to know it is right; `run`
  starts what is there and stops once it answers, for one who just wants to use the hub. Both
  change nothing. The order is one-way: the first `update` permanently closes `setup` and `gen` for
  that target, which is what stops a hub that has started diverging from being silently regenerated
  back to the seed. A target owns its code and its design from `setup` onward - the references are a
  seed, not a master - so two hubs may legitimately diverge. An entry may be MOUNTED, which makes
  the hub serve that app itself under a path of its own origin rather than link away to another
  port: it requires that app dir's `app.js`, calls its `createApp()` once at startup, strips the
  prefix and delegates. A mount is named by a REGISTRY ENTRY - the owning skill where that skill
  assembles one app, the app itself where it assembles many - and resolved through that registry,
  and one that cannot be prepared fails at its own prefix and nowhere else. Buttons are rendered by
  the SERVER on request, which is what lets the page carry no JavaScript and every label and URL be
  escaped before it becomes markup.
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

- **target** — the directory the prompt names on its second line, e.g. `artifacts/bios-home`, relative to the workspace root.
  It is where a hub lives, and from **setup** onward it is that hub's **source**, not a build product.
- **command** — the word on the prompt's third line: **setup**, **gen**, **update**, **test** or **run**.
  Exactly one per run, and it decides which steps execute.
- **lifecycle** — the one-way order `setup` → `gen` → `update`, with **test** and **run** available at any point after there is code.
  **update** is the door that only opens one way: once it has run, **setup** and **gen** are closed for that target forever.
- **lifecycle record** — `{target}\.imp-home.json`, carrying the **phase** and a `history` of every **command** run against this **target** with its timestamp.
  It lives in the **target** rather than in a checkpoint because the **lifecycle** spans sessions and a per-run file would forget it.
  The app never reads it.
- **phase** — the last state-changing **command** the **lifecycle record** carries: `setup`, `gen` or `update`.
  **run** changes nothing and so never changes it.
- **setup** — the **command** that creates the **target frame** once.
  It is the only **command** that may run against a directory with no **lifecycle record**.
- **gen** — the **command** that writes the **target code** from the **seed documents** and then copies those documents into the **target**.
  It runs as many times as it takes.
- **update** — the **command** that changes an already-generated **target**: **target documents** first, **target code** second, as many times as it takes.
- **test** — the **command** that serves the **target** and then reads it as a reader would, both halves.
  It is for a reader who wants to know the hub is **right**, and it is the only **command** that inspects what was served.
  It changes nothing in the **target**.
- **run** — the **command** that starts what is already in the **target**, confirms it answers, says where, and stops.
  It is for a reader who wants to **use** the hub, so unlike **test** it checks nothing beyond the server being up and judges nothing at all.
  It changes nothing either.
- **hub name** — which **seed entry** a **target** was seeded from.
  **setup** takes it from the prompt's fourth line and records it; every later **command** reads it back from the **lifecycle record**.
  It is deliberately **not** derived from the **target**'s name, so one seed entry can seed several targets and a target can be called something its seed is not.
  It also names every output of the run.
- **seed** — this skill's own `server\` and `references\`.
  It is a starting point, never a master: nothing in it is authoritative once a **target** exists.
- **seed documents** — the **seed**'s `references\Home-RSDC.md`, `Home-RSDC-tw.md`, `Wireframe.md` and `Wireframe-tw.md`.
  `Home-RSDC.md` decides what a hub must **do**; `Wireframe.md` decides what its page must **contain**.
  Together they are what **gen** generates from.
- **seed entry** — the `homes.{hub name}` block of the **skill config**: the port, the title and the starting **link list**.
  **setup** reads it; nothing after **setup** does, because by then the **app config** owns those values.
- **skill config** — `config.yaml` at this skill's root, carrying `homes` and the **app registry**.
  Only the **setup tool** reads it.
- **app registry** — the `apps` key of the **skill config**: a **registry name** mapped to that app's `appDir`, the `skill` that owns it, and its default `label`, `href` and `note`.
  It is what lets a prompt name a **mount source** by a reviewed name instead of by a path.
- **mount source** — a **registry name** on the prompt's `mounts:` line.
  Resolving it through the **app registry** is the only way this skill learns where another app was assembled.
- **registry name** — the key of an **app registry** entry, and the only thing a `mounts:` line may say.
  A skill that assembles exactly one app is named by **itself**; a skill that assembles many — one per directory it is pointed at — has no single app dir to be named by, so each of its apps is named by **itself** instead.
  Which of the two a name is does not change how it resolves: both arrive at one reviewed entry.
- **owner skill** — the `skill` of a registry entry: who to run when that app needs building or repairing.
  It is written on every entry rather than inferred from the key, because a key that is an app name would otherwise name a skill that does not exist.
- **target frame** — what **setup** writes: the **target** directory, its `public\`, the **app config**, `start.cmd`, `README.txt` and the **lifecycle record**.
  It carries no `server.js` — a frame is not yet an app.
- **target code** — the **target**'s `server.js` and `public\app.css`, written by **gen** and thereafter edited by **update**.
- **target documents** — the **target**'s `docs\Home-RSDC.md`, `docs\Home-RSDC-tw.md`, `docs\Wireframe.md` and `docs\Wireframe-tw.md`: the copy **gen** leaves behind.
  From then on they, not the **seed documents**, decide what **this** hub must be.
- **RSDC standard** — the chapter-responsibility rules `Home-RSDC.md` is written to: which question each of the four parts answers, and what each may not reach forward into.
  Where a change belongs in the **target documents** is settled against it.
- **app config** — the `app.config.json` beside the **target**'s `server.js`.
  The **only** file the app reads, which is what lets the folder be moved as a whole.
- **link entry** — one item of the **link list**: a `label`, an `href`, and an optional `note`.
  Its order in the list is its order on the page.
- **link list** — the **app config**'s `links`.
  Nothing else decides what buttons exist.
- **dead link** — a **link entry** whose scheme the page cannot navigate to, which today means `file://`.
  It is rendered **exactly like every other button**; the fact is reported by `/healthz`, never on the page.
- **mount** — a **link entry** carrying a `mount` field, which makes the hub serve that app itself instead of linking away to it.
  Its `href` is then a path on the hub's own origin, and that path is the **mount prefix**.
- **mount prefix** — the path a **mount** answers under, taken from its `href` with any trailing slash removed.
  The hub strips it from the request before delegating, so the **mounted app** sees only the path it was written to answer.
- **mounted app** — the app a **mount** points at, reached by requiring `app.js` from its directory and calling the `createApp(options)` it exports.
  It belongs to **another skill**: this one loads it, never builds it, starts it or repairs it.
- **setup tool** — `setup_target.py`, this skill's own tool and **setup**'s alone.
  Every later **command** edits the **target** in place, so no other may invoke it.

# CONFIGURATION

Concrete values this skill runs with.
Every path below is a constant of the skill; everything about the hub being worked on is read from the **target** the prompt names.

- **Checkpoint Dir** — `checkpoints\imp-home\{hub}-{command}-{yymmdd-hhmm}\`.
- **YAML checkpoint** — `process.yaml` inside the Checkpoint Dir.
- **MD report** — `{wikiDir}\imp-home\imp-home-{hub}-{command}-{yymmdd-hhmm}.md`, carrying the same `{hub}`, `{command}` and stamp as the Checkpoint Dir, where `wikiDir` comes from the workspace [config.yaml](config.yaml) (resolved in Step 0) — never hardcode the wiki root.
- **seed** — `{skillGroups.common}\skills\imp-home\server\` and `{skillGroups.common}\skills\imp-home\references\`.
- **seed documents** — [Home-RSDC.md](.github/common/skills/imp-home/references/Home-RSDC.md), `Home-RSDC-tw.md`, [Wireframe.md](.github/common/skills/imp-home/references/Wireframe.md) and `Wireframe-tw.md`.
- **setup tool** — `{skillGroups.common}\skills\imp-home\setup_target.py`.
- **skill config** — `{skillGroups.common}\skills\imp-home\config.yaml`.
- **target** — from the prompt's second line, relative to the workspace root.
  It sits outside the wiki vault.
- **lifecycle record** — `{target}\.imp-home.json`.
- **target documents** — `{target}\docs\`.
- **RSDC standard** — `{skillGroups.common}\references\RSDC-Standard.md`, with its diagram notation in `{skillGroups.common}\references\DFD.md`.
- **server origin** — `http://127.0.0.1:{port}`, where the port is the **app config**'s `port`.

# MUST FOLLOW

- **The design decides what the code is, not the other way round.**
  **gen** generates the **target code** from the **seed documents**, and **update** changes the **target documents** before the **target code**.
  At no point is code written first and described afterwards — a design produced that way is a transcript, and worth nothing to the next reader.
- **`gen` copies the documents it generated from into the target, in the same run.**
  Code without the design it came from is code nobody can check, and a design left only in the seed is one every later hub would silently share.
  If the copy did not happen, the **gen** did not finish.
- **The lifecycle runs one way, and the first `update` closes the door behind it.**
  Once the **lifecycle record** carries an `update`, the **commands** **setup** and **gen** are refused for that **target** for good.
  A hub that has begun to diverge must not be regenerated back to the seed by a command that does not know what it is overwriting.
  - **What that costs is worth naming.**
    After the first **update** there is no regenerate-from-scratch path: every change, however small, is made against the **target**'s own files.
    That is deliberate — regeneration is what **gen** was for, and it was available for exactly as long as the hub had nothing of its own to lose.
- **`update` refuses documents older than the code.**
  If a **gen** ran after the last change to the **target documents**, re-read them before changing anything: updating a design the code has already moved past writes the change into a document that was already wrong.
- **Every document is a pair, and both halves move together.**
  A section changed in `Home-RSDC.md` is changed in `Home-RSDC-tw.md` in the same run, under the same number; the wireframe pair carries the same rule.
- **`setup` runs once per target.**
  A **target** that already carries a **lifecycle record** is refused, naming the **phase** it is in and the **command** that follows it.
- **`test` and `run` change nothing.**
  **test** starts what is there and then checks and reads it; **run** starts it and stops once it answers.
  Either one that finds a defect names it and stops; fixing it is a **gen** or an **update**, whichever the **phase** allows.
- **`gen` and `update` do not serve what they wrote.**
  Writing and verifying are asked for separately, so an iteration is not charged the cost of a review nobody wanted yet.
  Both **commands** therefore end by saying the hub has **not** been run and naming **test**.
  - **What that costs is worth naming, and it is not the same for both.**
    An **update** still carries Step 3's own re-proving, on a throwaway copy at a spare port.
    A **gen** carries nothing: it ends having written a `server.js` that has never been started.
    Say so plainly rather than letting a clean-looking report imply otherwise.
- **The setup tool belongs to `setup` alone.**
  No other **command** may invoke it.
  It writes a **target frame** from the seed, so calling it later would revert whatever the **target** has become.
- **The target owns its code and its design; the seed is only a starting point.**
  No **command** after **setup** edits the **seed**, and two hubs are allowed to diverge — that is what makes them two hubs rather than one rendered twice.
  The cost is accepted: a later fix to the **seed documents** reaches no target already generated.
- **Never hardcode a hub.**
  No **hub name**, target path, port, title, label or URL may appear in this file, in the **seed**, or in the **setup tool**.
  The prompt names the target and the **skill config** seeds it.
- **One target per run.**
  The **command** applies to exactly one **target**.
  A run never works on two, and never falls back to "the only one" when the prompt named none — it asks.
- **The hub name says what a target was seeded from, not what it is called.**
  **setup** takes it from the prompt and writes it into the **lifecycle record**; the **target** directory may be named anything.
  Two targets may therefore be seeded from one **seed entry** — and if they are, both carry that entry's port, which two hubs cannot both bind.
  Say so when it happens, rather than leaving it to whichever one starts second.
- **Every command appends to the lifecycle record.**
  A **command** that changed the **target** and did not record itself leaves the next run to guess the **phase**, and the gate above is only as good as what it reads.
- **Render exactly the link list, in its order.**
  Never add, drop, reorder or rewrite a **link entry** except as a change the prompt asked for.
- **Escape every label, href and note where it becomes markup**, both quote forms included.
  A **link entry** is config text, and unescaped config text breaks out of the attribute it sits in.
  This is proven with a hostile value, not assumed.
- **A dead link is rendered like every other button, and counted elsewhere.**
  The hub cannot know how a reader will open a destination, and a marking that is right for one reader is wrong for the next.
- **The page carries no JavaScript.**
  Rendering happens in the hub server.
  Do not move it into the browser to "simplify" the server — that adds a client-side surface to audit and lets the page disagree with the config.
- **The app stays dependency-free.**
  Node stdlib only, one same-origin stylesheet, no CDN, no web font, no image.
  A **mount** does not change this: an app is reached by requiring a file, which is a language feature and not a framework.
- **A mount is loaded, not started, and never repaired here.**
  The hub requires the **mounted app**'s `app.js` and calls its factory; it never spawns a process.
  Making an app mountable is its own skill's work — if an `app.js` is missing, name the **owner skill** the registry records for it and stop.
- **A mount that cannot be prepared must not cost anything else.**
  The hub starts, every other button works, and the failure is answered at that prefix alone.
- **A failure the hub was never handed must not be fatal either.**
  A **mounted app** that throws on a later tick, or starts a promise and never returns it, hands the hub nothing to catch.
  It is logged and survived, never attributed to a prefix — the request that caused it is already gone.
- **A mount is named by a registry entry, never by a path typed into the prompt.**
  A path in a prompt is unreviewed input that reaches the filesystem; the **app registry** is the reviewed list, and a **mount source** that is not in it is a stop that says what to add, not a guess.
- **Least exposure by default.**
  The hub binds loopback unless `--host` is passed, and any wider binding is stated plainly to whoever asked for it — including that it widens every **mount** along with the hub.
- **This skill starts nothing else and repairs nothing else.**
  A button whose target is down belongs to the skill that owns that target.
  Name it and stop.
- Must run workflow step by step, and display each step number.
- Each step must be self-contained.
  **No forward-reference.**
- **Honour a `run step N` selector**: run Step N, then stop; never a later step.
  It is distinct from the **run** command — `run` alone on the third line is the command, while `run step` followed by a number is the selector, and a prompt may carry both.
- Follow [report-md-rules.md](.github/common/rules/report-md-rules.md) for the MD report's header and shape.
- Follow [report-yaml-rules.md](.github/common/rules/report-yaml-rules.md) for the YAML checkpoint's shape and required fields.
- Follow [scratch-rules.md](.github/common/rules/scratch-rules.md) for where a run's throwaway files go and how they are cleaned up — the escaping and mounting probes are exactly that.
- **Before the skill ends, display the server origin, target, MD report and YAML checkpoint** — show only those four, and render each as a clickable Markdown link.
  The **server origin** is an `http://` URL and links as itself, and is shown only by **test** and **run**, the two **commands** that start a server; **setup**, **gen** and **update** omit it, having left nothing running.
  The MD report lives in the vault, outside this workspace, so link it with an `obsidian://open?vault={vaultName}&file=<vault-relative-path>` URI (e.g. `[imp-home-{hub}-{command}-{yymmdd-hhmm}.md](obsidian://open?vault={vaultName}&file=imp-home/imp-home-{hub}-{command}-{yymmdd-hhmm}.md)`); the **target** and the YAML checkpoint keep a workspace-relative, forward-slash target (e.g. `[process.yaml](checkpoints/imp-home/{hub}-{command}-{yymmdd-hhmm}/process.yaml)`).
  - Do this for every run, including a partial one such as `run step 0`.

# Prompt Examples

## Prompt 1

```
/imp-home
artifacts/bios-home
setup
bios-home
mounts: imp-bios-logs, imp-bios-logs-search, imp-boot-times
```

## Prompt 2

```
/imp-home
artifacts/bios-home
gen
use black buttons.
```

## Prompt 3

```
/imp-home
artifacts/bios-home
update
use blue buttons, each button display only title.
```

## Prompt 4

```
/imp-home
InvHome
update
mounts: InvDataflow
```

`InvDataflow` is a **registry name** of the second kind: the app is assembled by `imp-app`, which builds a different app for every directory it is pointed at and so has no single app dir to be named by.
The entry carries `skill: imp-app`, which is what the hub reports if that app has no `app.js` yet.

## Prompt 5

```
/imp-home
artifacts/bios-home
test
```

## Prompt 6

```
/imp-home
artifacts/bios-home
run
```

# Workflow

Each step opens with a **Purpose**: one sentence saying why that step exists as a step — what this skill would lose by folding it into its neighbour.

**The command routes the run.**
Step 0 runs always and is where the gate is enforced.
Step 1 runs for **setup** only, Step 2 for **gen**, Step 3 for **update**; Step 4 runs for **test** and **run** only.
Naming those steps here is routing, not a forward-reference: no step borrows a later step's output.

**No command both writes and serves.**
**setup**, **gen** and **update** end with files on disk and start nothing; **test** and **run** start a server and write nothing.
That split is what lets an iteration cost only what it changed, and it is also what stops a run from implying it checked something it never looked at.
The price is that a **gen** can finish without its `server.js` ever having been started — stated, not hidden.

**Step 1 runs a script and Steps 0, 2 and 3 do not; Step 4 is half of each**, because writing a frame and starting a server are deterministic, whereas judging what a prompt asked for, generating an app from a design, changing a design and the code it governs, and reading a page as a reader would are judgement.
Step 4 carries both halves because they are two questions about one running page, and it names them as halves so the judged one cannot be lost behind the checked one.

## Step 0 - Warmup

- **Purpose**: settle which **target** is being worked on, which **command** applies, and whether the **lifecycle** permits it — the gate has to be enforced before anything is written, because afterwards there is nothing to refuse.

- Run `.venv` first — the **setup tool** needs `PyYAML`.
  The app itself needs no Python at all.
  **Node** must be on `PATH`; check `node --version` answers.
  There is nothing to `npm install`.

- Read the workspace config [config.yaml](config.yaml) at the workspace root and resolve:
  - **`wikiDir`**: the MD report root — this skill's report goes under `{wikiDir}\imp-home\`.
  - **`vaultName`**: the last path segment of `wikiDir` (e.g. `MyVault`) — the Obsidian vault name used to build the `obsidian://` link.
  - **`skillGroups`**: the group name -> skills-root map — this skill's own directory is `{skillGroups.common}\skills\imp-home\`.
  - Substitute the resolved values wherever `{wikiDir}`, `{vaultName}` or `{skillGroups.common}` appears in the steps below, including in commands.
  - If `config.yaml` is missing or a needed key is absent, stop and ask the user.

- This skill calls no API and needs no credential of any kind.

- The prompt takes one of the forms shown in **Prompt Examples** above.
  Parse it for:
  - **target** — the second line, a directory path.
    If none is given, ask; never pick one.
  - **command** — the third line: `setup`, `gen`, `update`, `test` or `run`.
    Any other word, or none, is a stop that lists the five in **lifecycle** order.
  - **hub name** — for **setup** only, the fourth line: which **seed entry** to seed this **target** from.
  - **mount sources** — the comma-separated **registry names** on an optional `mounts:` line.
    A name is a key of `apps`, which for some apps is their owner skill and for others the app itself; it is never a path.
  - **change requests** — for **gen** and **update**, every remaining prose line, each one a change the user is asking for.
    For **test**, any remaining prose line is instead a **review focus**: something to look at first.
    **run** takes none, and prose on a **run** is a stop that asks whether **test** was meant.
  - an optional trailing **`run step N`** selector.
    `run` on the third line is the **command**; only `run step` followed by a number is the selector.

- **Read the lifecycle record and enforce the gate.**
  This is the check the whole **lifecycle** rests on:
  - Read `{target}\.imp-home.json` if it is there, and take the **phase** and the `history` from it.
    A **target** with no record has never been set up.
  - **setup**: refused if a record exists.
    Name the **phase** and the **command** that follows it.
  - **gen**: refused if `update` appears anywhere in `history` — say that this target is past the point of no return and that **update** is how it changes now.
    It also needs a record, so a **target** never set up is refused too.
  - **update**: needs **target code** and **target documents**; if either is absent, say to run **gen** first.
  - **test** and **run**: need **target code**.
    Any **phase** that has it is fine.
    Neither is ever refused for what the **lifecycle** has done — they change nothing, so there is nothing for the gate to protect.

- **Settle the hub name**, which comes from a different place depending on the **command**:
  - **setup**: the prompt's fourth line.
    If it is missing, ask — never fall back to the **target**'s last path segment, because that seeds from an entry nobody chose and the mistake surfaces only later, as a wrong port or a wrong title.
  - **gen**, **update**, **test**, **run**: the `hub` field of the **lifecycle record**, where **setup** wrote it.
    A record without one predates that field; say so and ask which **seed entry** the **target** came from rather than guessing.

- **For `setup` only**, resolve the **seed entry** `homes.{hub name}` of the **skill config** for the port, the title and the starting **link list**.
  A **hub name** that is not a key of `homes` is a stop listing the keys that are.
  Then resolve each **mount source** through the **app registry** into a complete **link entry**, in the order the prompt gave; a name that is not a key of `apps` is a stop naming what to add.

- **For every other command**, read the **app config** in the **target** for the port and the current **link list**.
  A `mounts:` line is then a change request, resolved through the **app registry** the same way.

- For each **mount** in the resolved **link list**, check whether its `appDir` holds an `app.js`.
  Record which do and which do not — one that does not is a pending run of that app's own skill, not a fault here.

- **For `setup` only**, check the ownership of the **target**: search the skills roots of `skillGroups` for another skill whose config claims the same directory.
  If one does, stop and report both claimants and ask which owns it.

- Check whether the port is already taken.
  A live answer usually means an earlier run's server is still up, which is fine — say so, and either reuse it or stop it rather than starting a second one that cannot bind.

- Read the clock **once** and derive the run's `{yymmdd-hhmm}` stamp, and with the **hub name** and **command** the two output paths.

- Save YAML checkpoint `step_0` with the resolved `wikiDir`, the **target**, the **hub name** and where it came from, the **command**, the **phase** and `history` read from the **lifecycle record**, the gate verdict, the port and whether it was in use, the **link list** and its count, every **mount source** and what it resolved to, which mounts carry an `app.js`, any **change requests**, the Node version, the stamp, the output paths, the step selector, and timing.

- Display the **target**, the **command**, the **phase** and what the gate decided.
  Creating the MD report file is optional in this step.

## Step 1 - Setup the Target

- **Purpose**: give a hub a frame and an identity before any code exists, so that generation already knows its port, its title and its buttons instead of inventing them.

- **Runs for the `setup` command only.**
  For any other **command**, skip to the step that command routes to.

- Read the **target**, the **hub name**, the **seed entry** and the resolved **link list** back from the `step_0` group of the YAML checkpoint.

- **Run the setup tool** to write the **target frame**:
  - Example: `python {skillGroups.common}\skills\imp-home\setup_target.py --hub {hub name} --target {target}`
  - It creates the **target** and its `public\`, and writes the **app config**, `start.cmd`, `README.txt` and the **lifecycle record** with **phase** `setup`.
  - **It writes no `server.js`.**
    A frame is not an app; producing one is what **gen** is for.
  - It rejects a **link list** that is missing, empty, or carries an entry without a `label` or an `href` — a blank button looks like something that ought to work.
    It rejects a **mount** with no `appDir`, one whose `href` is not a path on this origin, one that would shadow one of the hub's own routes, or two claiming the same **mount prefix**.
  - A **mount** whose `appDir` has no `app.js` is **reported, not rejected**: that app has not had its own skill run yet.

- **Say what comes next**: the **target** now has a frame and nothing to run.
  The next **command** is **gen**.

- Save YAML checkpoint `step_1` with the files written and their sizes, the **link list** carried across, each **mount**'s readiness, the **lifecycle record** written, and timing.

- Save MD report file.
  Append and display a **Setup** section: the frame written with sizes, the buttons carried across, any mount reported as not yet ready, and the **phase** now recorded.

## Step 2 - Generate the App

- **Purpose**: turn a design into a working app in one act, and leave that design beside the code it produced, so a hub never exists without the thing it can be checked against.

- **Runs for the `gen` command only.**
  For any other **command**, skip to the step that command routes to.

- Read the **target**, the **change requests** and the **link list** back from the `step_0` group of the YAML checkpoint.

- **No script for this step.**
  Generating an implementation from a written design is judgement; a program asked to do it would only be asserting it had.

- **Read the seed documents first, and generate from them.**
  They are the specification, not background reading:
  - `Home-RSDC.md` — §2.7 *Presentation Contract* for what the page carries and where its buttons come from, §2.5 *Config Schemas* for the **app config** it reads, §2.6 *Derivation Rules* for the **dead link** count and the **mount prefix**, §2.8 *HTTP API* for the routes, §2.9 *Mountable Handler* for what a **mount** requires, §2.10 *Invariants* for the invariants, and its Design and Coding chapters for the components, the layout, escaping and how the code is written.
  - `Wireframe.md` — §1 for the page's structure, §2 for the elements every button must carry, §3 for the pages that are not the hub page, §5 for what the page must not contain.
  - Where a **change request** contradicts a **seed document**, the request wins for **this target** — but say so plainly, and write the difference into the **target documents** when they are copied below.
    A hub whose code and design disagree on the day it is generated is one nobody can check afterwards.

- **Write the target code** — `{target}\server.js` and `{target}\public\app.css` — to satisfy the documents above and every **change request**.
  On a later **gen**, regenerate against the same documents rather than patching around the last result.

- **Then copy the seed documents into the target**, as `{target}\docs\`:
  - All four, both languages, in the same run — this is what makes the **target** self-describing.
  - Where this **gen** departed from a **seed document**, amend the copy so it describes **this** hub, under the same section number, and say what the departure costs.
  - From here those copies are the **target documents**, and the **seed documents** are no longer authoritative for this hub.

- **Append to the lifecycle record**: a `gen` entry with its timestamp, and **phase** `gen`.

- **Say what comes next, and what has not happened.**
  This **command** wrote a `server.js` and did not start it, so nothing here has been observed running.
  The next **command** is **test**, or **run** to simply bring it up.

- Save YAML checkpoint `step_2` with each **change request**, the seed document sections generated against, the code files written, the documents copied, every departure recorded, the **lifecycle record** appended, and timing.

- Save MD report file.
  Append and display a **Gen** section:
  - **Summary line**: the code written, the documents copied, how many departures from the seed were recorded, and that the hub has not been run.
  - **Departures table** with columns:
    - **Change request**: the user's own words.
    - **What the seed design says**
    - **Recorded as**: the section of the **target documents** that now carries it.

## Step 3 - Update the Target

- **Purpose**: carry a change through the design and into the code in that order, which is the only order that leaves the documents worth reading afterwards.

- **Runs for the `update` command only.**
  For any other **command**, skip to the step that command routes to.

- Read the **target**, the **change requests** and the **link list** back from the `step_0` group of the YAML checkpoint.

- **No script for this step.**
  Deciding what a change request means, where in the design it belongs, and what code it implies is judgement.

- **For each change request, decide first where it lands in the target documents**, then write it there:
  - **Route it by the repaint test, not by topic.**
    A statement that stays true when the buttons change colour is a **Specification** change — a numbered section of `docs\Home-RSDC.md`, amended or added.
    A statement that would stop being true belongs in `docs\Wireframe.md`, with the elements it describes.
  - So: what the hub does, what a button *tells* a reader, and what a change costs are **Specification**.
    Colour, hover, border, typeface and the page's element inventory are **Wireframe**.
    "What the page shows" splits across both, which is why the test is the wording of the statement rather than its subject.
  - A change that fits nowhere in the documents is a change that does not belong in the code either.
    Say so and ask, rather than writing it into the code alone.
  - **Write both halves of every pair in this run**, under the same numbering.
  - Check every amended chapter against the **RSDC standard**: nothing technical in Requirements, no component in Specification beyond the interface its callers use, no library in Design, and no section reaching forward.
  - **State the cost of a change that removes something**, in the document: what this hub can no longer do, and why that was worth it.
  - **Neither design document may name the other.**
    Each states its own scope; a rule needing a reason from the other is given that reason in full, in its own words.
    A section number in the other file is a link that rots without anyone noticing.

- **Then change the target code to match**, editing the **target**'s own files:
  - `server.js` and `public\app.css` for behaviour and appearance, `app.config.json` for the **link list**, the port or the title.
  - **Never invoke the setup tool**, and never edit the **seed**.
  - A `mounts:` change request is applied to the **app config**'s `links`, resolved through the **app registry**, each resolved `appDir` written as an absolute path and the entry's **owner skill** written beside it — the hub shows that owner on the page a failed mount serves, and without it a mount that cannot be prepared cannot say who to run.

- **Re-prove what the change could have broken**, on a spare port against a throwaway copy of the **target** — never the real port and never the **target** itself.
  The **target documents**' Verification Obligations list the obligations; re-run the ones this change could have touched:
  - Escaping, if anything touched how a label, href or note reaches the markup.
  - Mounting, if anything touched routing — including a **nested** path, a bare prefix, a throw, a rejection, a **floating** async failure, and a mount with no `app.js`.

- **Append to the lifecycle record**: an `update` entry with its timestamp, and **phase** `update`.
  If this is the first one, say plainly that **setup** and **gen** are now closed for this **target**.

- **Say what comes next, and be exact about what the probes above did and did not prove.**
  They ran against a throwaway copy, so they prove the change did not break what they cover — not that the **target** serves.
  The next **command** is **test**, or **run** to simply bring it up.

- Save YAML checkpoint `step_3` with each **change request**, the document sections it changed, the code files it changed, the probes re-run and their results, the **lifecycle record** appended, and timing.

- Save MD report file.
  Append and display an **Update** section:
  - **Summary line**: how many change requests, whether this run was the one that closed the earlier commands, and that the **target** itself has not been served.
  - **Changes table** with columns:
    - **Change request**: the user's own words.
    - **Document**: the section of the pair it was written into.
    - **Code**: the target files it then changed.
    - **Proved by**: the probe re-run for it, or why none was needed.

## Step 4 - Serve and Review the Target

- **Purpose**: the one place the target becomes a running server and is then read as a reader would read it — what a machine can check about a page and what only a person can are two questions about the **same** live instance, and asking either one anywhere else would be asking about something that is not running.

- **Runs for the `test` and `run` commands only.**
  No other **command** starts a server.

- **`test` runs the whole step; `run` stops as soon as the server answers.**
  A **run** starts it, asks `/healthz`, reports the **server origin**, and ends — it does not compare the page to the **app config**, and it does not look at the page at all.
  That is the whole distinction between the two **commands**: **test** is for knowing the hub is right, **run** is for using it.
  A **run** that ends with a verdict on the page has quietly become a **test**, which is worse than either, because the caller asked for neither.

- **For `test`, this step has two halves and they run in that order: first what is checked, then what is judged.**
  The first is scripted and deterministic; the second is neither, and cannot be made so.
  **The checked half passing is not this step passing** — every check in it passes on a page nobody would want to use, which is the whole reason the judged half exists.
  A **test** that reports the first half and stops has not finished this step.

- Read the **target** and the port back from the `step_0` group of the YAML checkpoint.

### The checked half

- **Start the server as a background process** and leave it running — it is a server, not a one-shot script, and this half ends when it answers, not when the command returns.
  - Example: `node {target}\server.js`
  - Use an absolute path.
    The hub resolves every path against its own directory, so the **target** is the only place it runs.
  - If the port was already in use, stop that server first rather than starting a second one that cannot bind.

- **Confirm the server answers before going on.**
  Ask `{server origin}/healthz`, which returns the title, the link count, how many are **dead links**, every **mount** with its state, and the assembly time.
  **A `run` ends here**, reporting the **server origin** and what `/healthz` said.

- **Check the served page against the app config, not against the source.**
  Fetch `/` and compare its anchors to the **app config**'s labels and hrefs, in order; confirm zero external references other than the stylesheet; confirm no button is styled differently from any other.
  For each **mount**, ask its prefix as well and record what answered.

- **Ask a probe what it would prove before trusting what it reported.**
  A check that cannot fail, or that a library quietly satisfied on the hub's behalf, reads exactly like a check that passed — a redirect followed automatically, a mount asked only at its root, a header read with the wrong case.
  Where the design names what a proof requires, meet it: a **nested** path for prefix stripping, and the redirect itself rather than what it led to.

### The judged half

- No script for this half.
  Open the page and look at it, as a reader would.
  This half is judgement.

- Confirm by looking, not by trusting the counts just gathered: the buttons are the **link list** in order; each URL reads correctly, character for character; every button is styled identically; the page loads nothing from outside the **server origin**.

- **Look at whatever the prompt asked to be looked at, and then at the page as a whole.**
  Appearance is answered by the page, never by a status code — a stylesheet that was fetched is not a stylesheet that reads well.
  Say plainly when something was reasoned rather than seen.

- **Reconcile the page against the target documents' wireframe**, element by element — it is a prescriptive inventory, so every row it marks required must be on the page:
  - A page missing something the wireframe requires is a defect.
    Name it; do not fix it here.
  - A page carrying something the wireframe does not list is also a defect: either the element should go, or the wireframe should have said so.
    Name which, and leave it.
  - **Report it and stop — this **command** cannot record it.**
    The wireframe's own defects section is a **target document**, and only **update** writes those.
    So a defect found here is written down one **command** later, by whoever runs **update** next.
    That is the price of **test** changing nothing, and the report must carry enough for that **update** to be written without re-observing anything.

- **Say what a reader will experience per button** — including that this skill probes nothing, so a button pointing at a stopped app looks identical to one pointing at a running app, and that a **dead link** looks identical to a working one **by design**.
  Name the skill that owns each target so a dead button has an owner rather than a shrug.

- **A mount is the one destination this skill can speak for.**
  Its state was read at startup, so say for each whether it came up, and for one that did not, name the app dir and the skill that assembles it — then stop, because making it mountable is that skill's work.

- Do not repair a target, restart another server, or edit another skill's output.

- Save YAML checkpoint `step_4`.
  **A `test` records** the **server origin**, the port and host bound, the process id, the Node version, the `/healthz` response, the anchor comparison, each **mount**'s state, the buttons reviewed, the **dead link** count, what was looked at and what it showed, the wireframe reconciliation, the overall state, the recommended next **command**, and timing.
  **A `run` records only the first six of those** — origin, port and host, process id, Node version, `/healthz`, timing — because it saw nothing else.

- Save MD report file.
  Append and display a **Serve and Review** section for a **test**, or a **Serve** section for a **run**.
  - **A `test`'s section carries the tables and the verdict below.**
  - **A `run`'s section is one summary line and nothing else**: the **server origin**, how many buttons, how many are **dead links**, and how many **mounts** came up — every one of those read from `/healthz` rather than from the page.
    It carries no tables and no verdict, because it looked at nothing.
  - **Summary line**: the **server origin**, how many buttons, how many are **dead links**, how many **mounts** came up, whether the hub is usable as it stands, and which **command** the **phase** says comes next.
  - **Buttons table** with columns:
    - **Label**
    - **Href**: verbatim, exactly as the **app config** carries it.
    - **Note**
    - **State**: rendered, **dead link**, or **mount** with what its prefix answered.
  - **Mounts table** with columns:
    - **Prefix**
    - **App dir**
    - **Skill**: the one that assembles it.
    - **Answered**: what came back from that prefix.
  - **Per-button notes**: what a reader meets at each destination, and which skill owns it.
  - **Notes**: the wireframe reconciliation, anything seen rather than inferred about what this run changed, and anything the **target documents** accept as a cost rather than a defect, named as such so a later reader does not reopen it.
