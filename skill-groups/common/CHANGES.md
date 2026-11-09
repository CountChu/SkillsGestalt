# CHANGES

SkillsGestalt 的 `common` skill group 裡，會影響 Forge 的改動。
「會影響」是指：Forge 必須做點什麼，或它的檢查會從 PASS 變成 FAIL；只改措辭、不改做法的改動不記。
每一筆寫明改了什麼、commit，以及 Forge 要做什麼；新的日期在前。
Forge 以 chore [follow-gestalt](../../chores/follow-gestalt.md) 處理這裡的條目：它的執行紀錄記下處理到哪一筆，比那一筆新的就該做了。

### 2026-11-08

- **task 改成八章：`1. 背景` 後面多了 `2. 結論`，`2. 現況` 改名為 `3. 過程`**：[task-rules.md](rules/task-rules.md) 的章依序是 `1. 背景`、`2. 結論`、`3. 過程`、`4. 要做的`、`5. 驗證`、`6. 與其他 task 的關係`、`7. 知識`、`8. 日誌`。
  `2. 結論` 用簡短的項目寫 task 做了什麼、每一部分的結果、改了什麼、還留下哪些問題，並指出細節在 `3. 過程` 的哪一節；還沒有結果時寫 `—`；能用表格呈現的部分（例如每一次執行、改動與問題）都用表格。
  `check_tasks.py` 對七章的 task 報 FAIL；[forge-setup.md](references/forge-setup.md) 的 Task 1 範本也改成八章。
  Forge 要做：每個 task 檔在 `## 2. 現況` 前插入 `## 2. 結論`（內容 `—`），`## 2. 現況` 改成 `## 3. 過程`，後面各章的編號加 1；`3. 過程` 裡的 `### 2.N` 改成 `### 3.N`，其他章裡帶章號的 `###` 也一樣加 1。
  日誌以外，指向這些節或章的引用（例如 `2.8`、`3. 要做的`）跟著改；日誌是當天的紀錄，不改；講 chore 的章（例如 chore 的 `4. 驗證`）與講舊格式歷史的句子也不改。
  自己的 skill、chore 若寫了 task 的章名或章號（例如 `## 7. 日誌`），也要改。
  SkillsGestalt 自己的 127 個 task 已改好。

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
