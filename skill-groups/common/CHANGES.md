# CHANGES

SkillsGestalt 的 `common` skill group 裡，會影響 Forge 的改動。
「會影響」是指：Forge 必須做點什麼，或它的檢查會從 PASS 變成 FAIL；只改措辭、不改做法的改動不記。
每一筆寫明改了什麼、commit，以及 Forge 要做什麼；新的日期在前。
Forge 以 chore [follow-gestalt](../../chores/follow-gestalt.md) 處理這裡的條目：它的執行紀錄記下處理到哪一筆，比那一筆新的就該做了。

### 2026-11-09

- **asd-ste 的 review server 與 imp-home 的 `test_hub.js` 也從目前的目錄找 workspace 的根目錄**（接續 `8eae02d`）：兩支都多了 `--workspace`；除了只在 SkillsGestalt 執行的 `publish_snapshot.py`，`common` 裡已經沒有從 script 自己的位置找根目錄的 script。
  review server 的設計不變：port 8790 上只跑一個，服務啟動它的 workspace 的 `checkpoints\asd-ste\`；探測不分辨 workspace，所以另一個 workspace 啟動的 review server 占著 8790 時，探測照樣以 0 結束，連結連到的是那個 workspace 的執行（[ReviewPage-RSDC.md](skills/asd-ste/references/ReviewPage-RSDC.md) 4.6）。
  ReviewPage-RSDC.md 多了 Workspace root 一詞，asd-ste 的 README 重記 run-data-rules.md。
  Forge 要做的：要在 Forge 審核 asd-ste 的 draft 時，先看 8790 上的 review server 服務哪個 workspace：`--probe` 會印出它的 review root；是 SkillsGestalt 的，就用 `/healthz` 給的 pid 停掉它，Step 6 會為 Forge 啟動一個。

### 2026-11-08

- **task 改成八章：`1. 背景` 後面多了 `2. 結論`，`2. 現況` 改名為 `3. 過程`**：[task-rules.md](rules/task-rules.md) 的章依序是 `1. 背景`、`2. 結論`、`3. 過程`、`4. 要做的`、`5. 驗證`、`6. 與其他 task 的關係`、`7. 知識`、`8. 日誌`。
  `2. 結論` 用簡短的項目寫 task 做了什麼、每一部分的結果、改了什麼、還留下哪些問題，並指出細節在 `3. 過程` 的哪一節；還沒有結果時寫 `—`；能用表格呈現的部分（例如每一次執行、改動與問題）都用表格。
  `check_tasks.py` 對七章的 task 報 FAIL；[forge-setup.md](references/forge-setup.md) 的 Task 1 範本也改成八章。
  Forge 要做：每個 task 檔在 `## 2. 現況` 前插入 `## 2. 結論`（內容 `—`），`## 2. 現況` 改成 `## 3. 過程`，後面各章的編號加 1；`3. 過程` 裡的 `### 2.N` 改成 `### 3.N`，其他章裡帶章號的 `###` 也一樣加 1。
  日誌以外，指向這些節或章的引用（例如 `2.8`、`3. 要做的`）跟著改；日誌是當天的紀錄，不改；講 chore 的章（例如 chore 的 `4. 驗證`）與講舊格式歷史的句子也不改。
  自己的 skill、chore 若寫了 task 的章名或章號（例如 `## 7. 日誌`），也要改。
  SkillsGestalt 自己的 127 個 task 已改好。

### 2026-11-07

- **script 的根目錄是 skill 執行所在的 workspace，不從 script 自己的位置找**：Forge 就地讀取 `common`，所以從 script 自己的檔案往上找 `config.yaml` 的 script，在 Forge 執行時找到的是 SkillsGestalt 的根目錄、`skillGroups`、`wikiDir` 與 `checkpoints\`。
  現在根目錄是指令選項指定的目錄，否則是從目前的目錄往上、最近一個 `config.yaml` 有 `skillGroups` 的目錄；skill 自己的 config 仍在 skill 的檔案旁邊找。
  照這個找法改的有：imp-app 的 `resolve_session.py`、`run_tests.py`、`deploy_app.py`（`--workspace`，`1acb108`），gen-imp-app 的 `resolve_session.py`、`check_owner_skill.py`（`--workspace`，resolver 的 JSON 多了 `workspace`），asd-ste 的 `save_step.py`（`--root`）與 `draft.py`（`runs --workspace`），check-skill 的 `scan_skill.py`（`--config`）與 `update_dashboard.py`（`--workspace`），imp-home 的 `setup_target.py`（`--root`）。
  [run-data-rules.md](rules/run-data-rules.md) 把這條寫成一條規則；check-skill 的準則 5.8 改名為 Paths that follow the current directory or the script's location，從 `__file__` 或 `__dirname` 往上找 `config.yaml` 的 script 也報 issue。
  asd-ste 的 `review_server.js` 與 imp-home 的 `test_hub.js` 還是從自己的位置找根目錄，還沒改；asd-ste 的 README 因此還沒重記 run-data-rules.md。
  Forge 要做的：從 Forge 的根目錄或其下的目錄執行 skill；自己的 script 若從 `__file__` 或 `__dirname` 找 workspace 的 `config.yaml`（例如 `Path(__file__).parents[4]`），改成上面的找法，check-skill 的 5.8 會對它報 issue；引用 run-data-rules.md 的 README 報 CHANGED，讀過新規則後以 `depends_on.py record --target` 重記。
- **連到別的 vault 的 topic 用 Obsidian URI，`check_tasks.py` 也檢查這種連結**（`4b6946b`）：[task-rules.md](rules/task-rules.md) 說，`6. 知識` 的項目寫進 topic 之後，topic 在 task 檔所在的 vault 時用 wikilink，在別的 vault 時用 `[<Title>](obsidian://open?vault=<vault>&file=<path>)`，空格寫成 `%20`；vault 是從檔案往上最近一個含有 `.obsidian` 目錄的目錄，`write-topic` 的 topic 在 `wikiDir` 這個 vault。
  新 topic 的標題不用 `#`、`^`、`[`、`]`、`|`，因為 Obsidian 的連結找不到檔名含有這些字元的檔案。
  [check_tasks.py](scripts/check_tasks.py) 的檢查 10 從 Obsidian 的 vault 清單（Obsidian 設定目錄裡的 `obsidian.json`，或 `--obsidian-config` 指定的檔）依名稱或 id 找 vault；`file=` 的路徑不在那個 vault、vault 不在清單裡、清單讀不到，或連結裡留著空格，都判 FAIL；`obsidian://search` 這類別的動作不檢查。
  Forge 要做的：task 檔裡連到別的 vault 的 topic 的 wikilink（檢查 10 本來就判 FAIL）改成上面的 URI；`obsidian://open` 連結的 vault 不在這台機器的 Obsidian vault 清單裡，或 topic 改了名，檢查 10 會從 PASS 變成 FAIL，照它列出的連結修正。
  InvestForge 現有的 task 檔用的就是這種 URI，檢查 10 通過。

### 2026-11-06

- **Working Dir**（Task 100.12）：[run-data-rules.md](rules/run-data-rules.md) 把 Temp Dir 與 Checkpoint Dir 定為兩種 Working Dir；一次執行所有的 working data（step 檔、資料檔、暫存檔）都放在它唯一的 Working Dir，由寫 skill 的人二選一。[SKILL-tmp.md](templates/SKILL-tmp.md) 的 CONFIGURATION 列兩行 Working Dir、只留一行，CONFIGURATION 之後都寫 Working Dir，新增 `{WORKING_DIR}` placeholder；gen-skill 問要用哪一種；check-skill 的準則 1.15 要求只有一個 Working Dir，準則 5.7 檢查 working data 都在 Working Dir 裡。imp-home 的 `test_hub.js --run` 改寫到 `checkpoints\imp-home\{yymmdd}.{N}\test-hub\`。
  Forge 要做的：自己的 skill 若同時有 Temp Dir 與 Checkpoint Dir，併成一個；CONFIGURATION 那行改成 `- **Working Dir** — the Checkpoint Dir, ...`（或 the Temp Dir），之後的 Checkpoint Dir／Temp Dir 改成 Working Dir；check-skill 會對兩個 Working Dir 報 issue，對其餘舊寫法報 recommendation。
- **Scratch files 改成 Temp Dir**（Task 100.11）：[run-data-rules.md](rules/run-data-rules.md) 把一次執行的暫存檔放進 Temp Dir `temp\{skill}\{yymmdd}.{N}\`，結構和 Checkpoint Dir 一樣，檔名不必以 skill 名開頭，skill 不移除它；step 執行的 script 由 step 傳入 Run Number。[SKILL-tmp.md](templates/SKILL-tmp.md) 的 Glossary 與 CONFIGURATION 把 Scratch file(s) 換成 Temp Dir。check-skill 的 `scan_skill.py` 改用 `--run-number`，不再有 `--out`，facts file 是 Temp Dir 裡的 `facts.yaml`；準則 5.7 檢查 Temp Dir 的規則。imp-home 的 `test_hub.js` 加上 `--run`。
  [tw-keep-english.md](references/tw-keep-english.md) 換成 261106 版，加上 working data，中文版不再寫「執行時的工作資料」。
  Forge 要做的：自己的 skill 把 `temp\{skill}-*` 的暫存檔改放進 Temp Dir，拿掉以完整名稱移除暫存檔的步驟；中文版的「工作資料」改成 working data；做 keep-english chore；check-skill 可能對還在舊位置的暫存檔報 recommendation。
- **CONFIGURATION 先列輸入與工具**（Task 100.8）：[SKILL-tmp.md](templates/SKILL-tmp.md) 的 CONFIGURATION 依序是「The inputs and tools」、「The working data of a run」、「The last outputs」；gen-skill 照它寫，check-skill 的準則 1.3 檢查組的順序。
  Forge 要做的：自己的 skill 把讀取的檔、執行的 script 與用到的程式列在第一組；check-skill 可能對放錯組的行報 recommendation。
- **Process record 改名為 Run record，22 個 skill 的 CONFIGURATION 分成兩類**（Task 100.7）：run-data-rules 的「The Data of the Process」改成「The Working Data of a Run」；`database\skill-runs\` 的檔改稱 run record，script 輸出的欄位改成 `run_record`、`runRecord`；MD report 的表頭欄是 `Run record`。
  Forge 要做的：自己的 skill 與文件照新名稱改；讀 `resolve_session.py` 或 `save_step.py` 輸出的地方，欄位名改成 `runRecord` 或 `run_record`。
- **CONFIGURATION 照兩類分組，MD report 的 Checkpoint 欄改名為 Process record**（Task 100.7）：[SKILL-tmp.md](templates/SKILL-tmp.md) 的 CONFIGURATION 分成過程產生的資料（Scratch files、Checkpoint Dir）與最後的輸出（Process record、Handoff file、MD report），TERMINOLOGY 加上 Scratch file 與 Handoff file；[report-md-rules.md](rules/report-md-rules.md) 的表頭欄 `Checkpoint` 改成 `Process record`，placeholder 改成 `{PROCESS_RECORD_PATH}`。
  Forge 要做的：自己的 skill 寫 MD report 時，表頭用 `Process record` 欄；引用 SKILL-tmp.md 的 README 會顯示 CHANGED。
- **其餘 9 個 skill 也寫 process record**（Task 100.6）：add-tags、add-tags-note、ask-note、check-wiki-doc、chinese、del-tags、write-note、write-note-new-files、write-note-tags；現在 `common` 的每個 skill 都寫 process record。
  check-wiki-doc 讀的設定名稱從 `wikiRootDir` 改成 config.yaml 實際有的 `wikiDir`。
  Forge 要做的：沒有；第一次 run 時建立 `database\skill-runs\`。
- **13 個 skill 照 run-data-rules 改，兩個舊規則檔刪掉**（Task 100.4）：asd-ste、check-md-deps、check-skill、compile-skill、gen-imp-app、gen-rsdc-app、gen-rsdc-skill、gen-skill、imp-app、imp-home、reformat-md、set-tag-status、write-topic。
  - 每個 skill 都寫 process record；有 checkpoint 的改成 `checkpoints\{skill}\{yymmdd}.{N}\` 的 step 檔；script 的根目錄從 `config.yaml` 找，不跟著目前目錄。
  - gen-rsdc-app 交回的結果寫進 `handoff\gen-rsdc-app\`，gen-imp-app 的 prompt log 寫進 `handoff\gen-imp-app\`；imp-app 與 gen-imp-app 從 handoff 檔讀。
  - run-data-rules.md 加一條例外：不可以找到 workspace 檔案的測試，可以用系統的暫存目錄（compile-skill 的驗證試跑）。
  - scratch-rules.md、report-yaml-rules.md 與中文版刪掉。
  Forge 要做的：引用這兩個舊檔的檔改連 [run-data-rules.md](rules/run-data-rules.md)；舊格式的 Checkpoint Dir（例如 `checkpoints\asd-ste\{parent}-{name}\`）不會再被讀到，要留的資料自己搬；`database\skill-runs\` 與 `handoff\` 第一次 run 時建立。
- **範本、gen-skill 與 check-skill 照 run-data-rules 改**（Task 100.3）：
  - [SKILL-tmp.md](templates/SKILL-tmp.md)：Glossary 加上 Run Number、Step file 與 Process record，拿掉 YAML checkpoint；Checkpoint Dir 是 `checkpoints\{SKILL_NAME}\{yymmdd}.{N}\`；Step 0 取得 Run Number 並寫出 process record；每一步保存 `step_N.yaml`，再把自己加進 process record；`{CHECKPOINT_DIR_NAME}` 拿掉。
  - [README-tmp.md](templates/README-tmp.md)：header quote 與依賴樹改連 run-data-rules.md；Dataflow 畫 step 檔，不畫 process record。
  - gen-skill 的 Step 1 改問 MD report 與 step 檔；每個 skill 都寫 process record。
  - check-skill 加上 5.7（用系統的暫存目錄）與 5.8（路徑跟著目前目錄）兩項。
  Forge 要做的：用 gen-skill 寫新的 skill 時照新範本；已有的 skill 照 Task 100.4 的做法改，check-skill 的 5.7 與 5.8 可能報出新的 issue；引用 SKILL-tmp.md 或 README-tmp.md 的 README 會顯示 CHANGED。
- **run-data-rules.md 取代 scratch-rules.md 與 report-yaml-rules.md**（Task 100.2）：[run-data-rules.md](rules/run-data-rules.md) 把 run 寫的資料分成兩類。
  - 過程產生的資料：`temp\` 的暫存檔，script 的暫存檔也放這裡，不用系統的暫存目錄；`checkpoints\{skill}\{yymmdd}.{N}\` 的 `step_{N}.yaml`。
  - 最後的輸出：`database\skill-runs\{skill}\{yymmdd}.{N}.yaml` 的 process record（每一步的時間與 model）、`handoff\{skill}\{yymmdd}.{N}.md`、`database\`，以及 vault 的 MD report。
  [report-md-rules.md](rules/report-md-rules.md) 的 Checkpoint 欄改成 process record 的路徑；兩個舊檔只剩一句指向新檔；`.gitignore` 加上 `handoff/`。
  Forge 要做的：`.gitignore` 加上 `handoff/`；範本與 skill 照新規則改的部分在 Task 100.3 與 100.4，做完會再加一筆。
- **6 個很少用的 skill 搬到 `skill-groups/archived/skills/`**（Task 100.1）：report-logs、report-week、report-skills、notify-week、synch-two-mds 從 `common` 搬走，eli5 從 `external` 搬走；`skill-groups/archived/` 不在 `skillGroups` 裡，裡面的 skill 不能執行。
  [publish_snapshot.py](scripts/publish_snapshot.py) 發佈時也排除 `skill-groups/archived/`。
  Forge 要做的：用到這幾個 skill 的 Forge，把它們從自己的 skill 清單、workspace 檔或文件裡拿掉；InvestForge 的 `InvestForge.code-workspace` 仍列著 `skill-groups/external/skills`，這個目錄現在沒有 skill。
  add-tags 與 del-tags 仍會改 `{wikiDir}\report-logs\` 裡舊的報告，report-logs 不再產生新的報告。

### 2026-11-02

- **AGENTS.md 寫明怎麼找 skill，並列出 skill group 的根目錄**（Task 97.1）：[AGENTS-tmp.md](templates/AGENTS-tmp.md) 的 Skills 一節說明 `/<name>` 的 `<name>` 是 skill、後面是參數；只在每個 skill group 的根目錄找 `skills/<name>/SKILL.md`，不搜尋 repository，找不到就告訴使用者。
  [gen_agents_md.py](scripts/gen_agents_md.py) 把範本的 `{skillGroupRoots}` 換成 `config.yaml` 的 `skillGroups` 清單；Chores 一節改成只在找或做 chore 時先讀摘要表，說出 skill 名稱的請求不是 chore。
  VS Code 的 Copilot harness 仍會先查自己的 skill 清單再搜尋，所以 Skills 一節再寫明：這些 skill 不在 agent 的清單裡，依序讀每個根目錄的 `skills/<name>/SKILL.md`，不用檔案搜尋、glob 或文字搜尋。
  Copilot harness 改了寫法仍先搜尋，找不到 workspace 外的 skill；在 Forge 請用 VS Code 的 Local harness 或 Claude Code，`chat.agentSkillsLocations` 照舊。
  Forge 要做：執行 `{python} {skillGroups.common}/scripts/gen_agents_md.py`，commit AGENTS.md。
- **skill 只寫動作，不寫只有某個 agent 才有的工具名稱**（Task 97.3）：[skill-writing.md](rules/skill-writing.md) 多一條規則；check-skill 的 check 5 多了 criterion 5.6 Agent-specific tool names，找到時是 issue；check-skill 自己的 check picker 不再寫 `vscode_askQuestions`。
  Forge 要做：對自己的每個 skill 執行 `/check-skill <name> 5.6`，把 step 裡的工具名稱（例如 `vscode_askQuestions`、`AskUserQuestion`）改成動作，例如「問使用者一題多選題」；依賴 skill-writing.md 的檔報 CHANGED，讀過新規則後以 `depends_on.py record --target` 重記。
- **規則改寫在 AGENTS.md；CLAUDE.md 只有 `@AGENTS.md`**（Task 97.2）：`CLAUDE-tmp.md` 改名為 [AGENTS-tmp.md](templates/AGENTS-tmp.md)，`gen_claude_md.py` 改名為 [gen_agents_md.py](scripts/gen_agents_md.py)；script 寫出 AGENTS.md，另寫一行 `@AGENTS.md` 的 CLAUDE.md，`--check` 比對兩個檔。
  agency 自己的部分改名為 `AGENTS-local.md`，裡面的 `{CLAUDE-local}` 改成 `{AGENTS-local}`；只有 `CLAUDE-local.md` 時，script 停下並說明。
  `skills/CLAUDE.md`（改 skill 前先讀 README）刪掉，內容搬進範本的 `## Skills`。
  Forge 要做：`git mv CLAUDE-local.md AGENTS-local.md`，把裡面的 `{CLAUDE-local}` 改成 `{AGENTS-local}`；執行 `{python} {skillGroups.common}/scripts/gen_agents_md.py`，commit AGENTS-local.md、AGENTS.md 與 CLAUDE.md；自己的檔與 chore 裡的 `gen_claude_md.py` 改成 `gen_agents_md.py`。
- **`.github` 改名為 `skill-groups`；CLAUDE.md 多了 Skills 一節**（Task 97.7）：SkillsGestalt 的 skill group 在 `skill-groups/common` 與 `skill-groups/external`，舊的 `.github/` 路徑都已改掉。
  CLAUDE-tmp.md 多了 `## Skills`：skill 在 `<skill group 的根目錄>/skills/<name>/SKILL.md`，要執行 skill 時讀它，照它的步驟做。
  check-skill 的 `scan_skill.py` 把 `skill-groups/` 與 `.github/` 開頭的路徑都當成寫死的路徑。
  Forge 要做：`config.yaml` 的 `skillGroups.common` 改成 `<SkillsGestalt>/skill-groups/common`，執行一次 `gen_claude_md.py`；VS Code workspace 檔的 `chat.agentSkillsLocations` 也改成新的路徑；自己的檔裡指向 SkillsGestalt `.github/` 的路徑跟著改。
  改之前，Forge 找不到 common 的 skill、規則與 script。
- **Forge 必須有 `.venv`**（Task 96）：forge-setup.md 的「Make a Forge」多了第 3 步，原本的第 3 到 7 步變成第 4 到 8 步；套件清單是新的 [requirements.txt](requirements.txt)。
  SKILL-tmp.md 的 Step 0 要求 `.venv`，以 `{python}`（`.venv/bin/python`，Windows 上是 `.venv\Scripts\python.exe`）執行每個 script，沒有 `.venv` 就停下；asd-ste 已照著改。
  Forge 要做：照 forge-setup.md 第 3 步在根目錄建 `.venv`，或在已有的 `.venv` 加裝 `{skillGroups.common}/requirements.txt`；`.gitignore` 要有 `.venv/`。
- **STE 不查標題的字；ste-custom.md 多 8 個字**（Task 41.1）：`check_ste.py` 不再問標題的字，清冊的標題字 `[TODO]`、檢查的「標題裡字典沒收的字」`[WARN]`，以及 findings key `heading_words_to_decide`、`heading_words_not_in_dictionary` 都拿掉，asd-ste 的 Step 1 也不再存 `heading_words`。
  ste-custom.md 把 activity、event、partial、process、request、route、stage 與 variable 當名詞核准；DFD.md、RSDC-Standard.md、tw-keep-english.md、report-yaml-rules.md 與 scratch-rules.md 的 `Technical words:` 拿掉這些字，內文沒變。
  Forge 要做：照 ste-custom.md 跑一次 `draft.py recheck`，commit 它記下的紀錄；自己的 STE 檔，`Technical words:` 裡和 ste-custom.md 意思相同的這 8 個字拿掉；引用 DFD.md、RSDC-Standard.md、report-yaml-rules.md 或 scratch-rules.md 的文件報 CHANGED，以 `depends_on.py record --target` 重記。

### 2026-10-31

- **task 多了「取消」狀態與 `6. 知識` 章**（`00e333e`）：Status 可以是 `取消`，圖示 ⊘；task 檔固定七章，`5. 與其他 task 的關係` 之後是 `6. 知識`，日誌改為 `7. 日誌`。`check_tasks.py` 對只有六章的 task 報 FAIL。
  Forge 要做：每個 task 檔在 `## 6. 日誌` 前插入 `## 6. 知識`（內容 `—`），並把 `## 6. 日誌` 改成 `## 7. 日誌`；摘要表的圖例加上 `⊘ 取消`。SkillsGestalt 自己的 108 個 task 已改好。
- **新的 chore follow-gestalt**（Task 88.3）：Forge 以它處理本檔的條目。
  Forge 要做：在 `dashboard/chore-summary.md` 加一列文字的 `follow-gestalt`，Title 與何時要做照 SkillsGestalt 的 `chores/follow-gestalt.md`；`config.yaml` 要有 `agencies.SkillsGestalt`。

### 2026-10-30

- **chore 不放自己的程式；private chore**（`1f0b0a8`）：chore 檔裡每個執行檔案的指令，路徑都要寫成 `{skillGroups.X}/…`；別的 agency 的 private chore 不能做。
  Forge 要做：自己的 chore 若有指令寫實際路徑或本 repo 的程式，改成 `{skillGroups.X}/…`，程式搬進 skill group；摘要表不能有 `publish-github`。
- **沒有 `chores/` 也可以**（`78c4dc1`）：只做別的 agency 的 chore 時，`check_chores.py` 把不存在的 `chores/` 當成空的。
  Forge 要做：不必放空的 `chores/`。
- **chore 改用名稱，執行紀錄搬到摘要表**（`3a1fd0c`）：chore 檔是 `chores/<name>.md`，名稱在所有 agency 裡只有一個；chore 檔只放定義；執行紀錄寫在自己的 `dashboard/chore-summary.md` 的 `## 執行紀錄`；別的 agency 的 chore 寫成文字的名稱，由 `config.yaml` 的 `agencies` 找到定義；checkpoints 放在 `checkpoints/chores/<name>`；commit 前綴 `chore <name>: `。
  取代同一天的使用檔做法（`3d23308`、`6af3dbd`）。
  Forge 要做：照 [forge-setup.md](references/forge-setup.md) 的 Change an Older Workspace 改；`config.yaml` 加 `agencies`；和 SkillsGestalt 做同樣工作的 chore 刪掉自己的檔，改成文字的一列。
  InvestForge 已在 Task 15 @ InvestForge 做完。
- **`keepEnglishChore`**（`19b96b6`、`d29a546`）：CLAUDE.md 的 keep-English chore 由 `config.yaml` 的 `keepEnglishChore` 填入，值是 chore 的名稱。
  Forge 要做：`config.yaml` 加 `keepEnglishChore`，再執行一次 `gen_claude_md.py`。
- **CLAUDE.md 由模板產生**（`2815afe`、`e9ed765`）：CLAUDE.md 由 [CLAUDE-tmp.md](templates/AGENTS-tmp.md) 與 agency 根目錄的 `CLAUDE-local.md` 經 `gen_claude_md.py` 產生；`CLAUDE-local.md` 裡一行 `{CLAUDE-local}` 把它分成放在開頭與結尾的兩段；連到 common 的連結是相對路徑。
  取代同一天的 `agency-rules.md` 與 `check_claude_md.py`（`e50a302`、`188afa9`），兩者已刪。
  Forge 要做：把只有自己的規則搬到 `CLAUDE-local.md`，執行 `gen_claude_md.py`，不再手改 CLAUDE.md。
