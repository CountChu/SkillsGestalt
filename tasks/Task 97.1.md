# Task 97.1 - 實測 agent 照 AGENTS.md 找到 skill-groups 的 skill

**Status**：完成——Claude Code 與 VS Code Local 照 AGENTS.md 找到 skill；Copilot harness 改了寫法仍先搜尋，記成已知限制。
**Raised**：2026-11-02，官方說明說 Copilot harness 只找 `.github/skills/` 與 `~/.copilot/skills/`，`chat.agentSkillsLocations` 是否還有效，前後兩段說法不同。
**Depends on**：[[Task 97.2]]、[[Task 97.7]]

## 1. 背景

- skill 原本放在 `.github/common/skills/<name>/` 與 `.github/external/skills/<name>/`，比 `.github/skills/` 多一層 skill group。
- InvestForge 靠 `InvestForge.code-workspace` 的 `chat.agentSkillsLocations` 找到它們；SkillsGestalt 自己沒有這個設定。
- 官方說明見 [[Task 97]] 的表 1。

## 2. 現況

### 已決定（2026-11-02）

- [[Task 97.7]] 把 `.github` 改名為 `skill-groups`。
- agent 不靠內建的位置找 skill，而是照 AGENTS.md 的指示，到 `skill-groups/<group>/skills/<name>/SKILL.md` 讀 skill，照它做；Claude Code 在這裡本來就這樣做。
- 不用 symlink，也不用 plugin；plugin 的做法已取消，見 [[Task 97.4]]。
- 代價：Copilot 與 Claude Code 的 `/` 選單不會列出這些 skill，使用者要用名稱請 agent 執行。

### 2026-11-02 Claude Code 的實測

開了兩個新的 session，背景只寫「這是 SkillsGestalt repo 的一次使用者請求」，不提 skill 在哪裡，也不提 AGENTS.md。
兩個都照 AGENTS.md 找到 `skill-groups/` 裡的 SKILL.md，並照它的 step 做；沒有去找 `.github` 或 `.claude/skills`。

- 「用 reformat-md 整理 tasks/Task 97.1.md，只報告會改什麼」（[session](#local_8dbce98b-9237-4882-af7a-27c9d6208fc8)）：讀的第一個 repo 檔就是 `skill-groups/common/skills/reformat-md/SKILL.md`，照 Step 0 到 2 做，在 scratchpad 的副本上跑；結果是本檔不用改。
- 「/check-skill asd-ste 5.6」（[session](#local_aa9e7e0c-f027-410d-ac5d-9932aa4fd30b)）：先查 `config.yaml` 的 `skillGroups`，再讀 `check-skill/SKILL.md`，照 Step 0 到 5 做，範圍只有 5.6；結果是 asd-ste 沒有 finding。
  它沒有更新 Skills Dashboard，是因為提示叫它不要改檔，不是 skill 漏了 Step 5。
- 兩個 session 都沒有讀 AGENTS.md 這個檔：Claude Code 開始時已由 CLAUDE.md 的 `@AGENTS.md` 載入它。

### 2026-11-02 VS Code 的實測

使用者在 VS Code 打開 SkillsGestalt 資料夾，使用者設定沒有 `chat.agentSkillsLocations`；兩個 harness 的模型都是 GPT-6 Luna，提示和 Claude Code 的相同。
四次都找到 SKILL.md，照它的 step 做，結論和 Claude Code 相同；但都是搜尋 repository 找到的，沒有用 skill group 的根目錄組出路徑。

- Copilot harness，reformat-md：讀 `config.yaml`、`dashboard/chore-summary.md`，再以 `reformat-md|format.*Markdown|Markdown.*format` 搜尋，才讀 SKILL.md；只在記憶體推演，沒有執行 script。
- Copilot harness，`/check-skill asd-ste 5.6`：讀 `dashboard/chore-summary.md`，找 `**/*asd-ste*` 與 `**/SKILL.md`，以 `check-skill|skill check|Check skill` 搜尋，才讀 SKILL.md；沒有讀 `config.yaml`。
- Local harness，reformat-md：讀 memory，找 `**/reformat-md/**`（4 個檔），讀 SKILL.md 之後才讀 `config.yaml`；以 Python 載入 `reformat_md.py` 在記憶體執行。
- Local harness，`/check-skill asd-ste 5.6`：先把 asd-ste 當成要執行的 skill，讀它的 SKILL.md；再以 `check-skill|5\.6` 搜尋 `**/skill-groups/**/skills/**/SKILL.md`，才找到 check-skill。
  提示叫它不要改檔，所以它沒有執行會寫 facts 檔的 `scan_skill.py`。
- `/check-skill` 在兩個 harness 都顯示成藍色的指令標籤，但 `/` 選單沒有列出它：VS Code 本身不認得這個 skill。
- Copilot harness 兩次都先讀 chore-summary.md：Chores 一節的「Read this table first to find the chore that you must do」被當成每個請求都要先讀。

在 SkillsGestalt 搜尋會成功，因為 skill 在 repository 裡；InvestForge 的 common 在 SkillsGestalt，搜尋 InvestForge 找不到它。

### AGENTS.md 的找法（已決定，2026-11-02）

使用者選了改寫 AGENTS.md 的做法，不在 AGENTS.md 列出每個 skill，又回答了 8 個問題，都照建議：

1. **Skills 一節的位置不動**，找法寫在最前面，改 skill 的規則留在後面。
2. **`/<name>` 的 `<name>` 是 skill，後面是參數**，舉 `/check-skill asd-ste 5.6` 為例；請求只說出 skill 名稱時也一樣。
3. **不搜尋 repository**：每個 skill group 的根目錄都沒有這個 SKILL.md 時，告訴使用者，停下。
4. **AGENTS.md 列出每個 skill group 的根目錄**：`gen_agents_md.py` 把範本的 `{skillGroupRoots}` 換成 `config.yaml` 的 `skillGroups` 清單。
5. **Chores 一節改成只在找或做 chore 時先讀摘要表**。
6. **CHANGES.md 請 Forge 重新產生 AGENTS.md**。
7. **重測**：Copilot 與 Local harness 都重測，Claude Code 也再開新的 session；提示改成可以寫 `temp/` 與 scratchpad，讓 `scan_skill.py` 與副本照 SKILL.md 執行。
8. **一個 commit**，重測通過才標完成。

### 2026-11-02 改好之後

- [AGENTS-tmp.md](../skill-groups/common/templates/AGENTS-tmp.md) 照上面改寫；`Technical words:` 加上 argument 與 user；範本與 AGENTS.md 通過 STE 檢查。
- [gen_agents_md.py](../skill-groups/common/scripts/gen_agents_md.py) 支援 `{skillGroupRoots}`；在副本以 Forge 的 `config.yaml` 試過：common 列出絕對路徑，沒有值的 external 不列。
- [CHANGES.md](../skill-groups/common/CHANGES.md) 加一筆。

### 2026-11-02 Claude Code 的重測

改好之後，再開兩個新的 session；提示改成可以寫 `temp/` 與 scratchpad，不要改 repo 裡的其他檔，也不要 commit。
兩個都照新的 AGENTS.md，用 skill group 的根目錄組出路徑，沒有搜尋 repository。

- 「用 reformat-md 整理 tasks/Task 97.1.md，只報告會改什麼」（[session](#local_99d09fa0-9979-4af5-a852-c3c2d2c426bf)）：`ls` 兩個根目錄的 `skills/reformat-md/`，common 有、external 沒有；讀 SKILL.md 與 `config.yaml`。
  在 scratchpad 的副本上執行 `reformat_md.py` 與 `check_reformat.py`：PASS，本檔不用改。
- 「/check-skill asd-ste 5.6」（[session](#local_660b6461-e122-4b7c-9e0d-cb33b8f96826)）：把 `check-skill` 當成 skill、`asd-ste 5.6` 當成參數；`ls` 根目錄，確認 check-skill 與 asd-ste 都在。
  依序讀 check-skill 的 SKILL.md、`config.yaml`、`scratch-rules.md` 與 `checking-criteria.md`；執行 `scan_skill.py`，用完刪掉 facts 檔；結果是 5.6 沒有 issue。
  提示叫它不要更新 Skills Dashboard，所以 Step 5 沒有做。
- 兩個 session 都沒有讀 `dashboard/chore-summary.md`：Chores 一節的新寫法有效。

### 2026-11-02 VS Code 的重測

提示和 Claude Code 重測的相同，模型都是 GPT-6 Luna；四次的結論都和 Claude Code 相同，也都照 SKILL.md 執行了 script。

- Local harness，reformat-md：第一個動作就是讀 `reformat-md/SKILL.md`，再讀 `config.yaml`、`md-style.md` 與兩支 script；唯一的搜尋是 SKILL.md 要的「預覽檔名沒被占用」。
  在 `temp/` 的副本上執行 `reformat_md.py` 與 `check_reformat.py`：PASS，本檔不用改；預覽檔留在 `temp/`。
- Local harness，`/check-skill asd-ste 5.6`：說「先按工作區規則載入 check-skill」，第一個動作就是讀 check-skill 的 SKILL.md；asd-ste 的 SKILL.md 是掃描時才讀。
  執行 `scan_skill.py`，facts 檔放在 `temp/`，用完刪掉；照提示沒有更新 Skills Dashboard；結果是 5.6 沒有 issue。
- Copilot harness，reformat-md：想法裡說 skill「not currently listed among the available skills」；先找 `**/*reformat-md*`、`chores/*summary*`，讀了 `chore-summary.md`，再找 `**/skills/reformat-md/**` 才讀 SKILL.md；`config.yaml` 在 SKILL.md 之後才讀。
  它有讀 AGENTS.md 連到的 `md-style.md` 與 `task-rules.md`，所以讀到了 AGENTS.md，但沒有照 Skills 一節的找法。
- Copilot harness，`/check-skill asd-ste 5.6`：送出的提示只有這一行；先說「I'll locate the asd-ste skill」並讀 asd-ste 的 SKILL.md，再以 `check-skill|check_skill|Check Skill|check skill` 搜尋，才改做 check-skill。
  提示沒有叫它不要改 Dashboard，所以它照 Step 5 更新了 vault 的 `dashboard/skills.md`，5.6 仍是 ✅。
- 結論：Local 照 AGENTS.md 找到 skill，通過；Copilot 先查 VS Code 自己的 skill 清單，查不到就搜尋，沒有通過；照這個找法，Copilot 在 InvestForge 找不到 common 的 skill。

### Copilot 的處理（已決定，2026-11-02）

使用者決定先試一個成本低的改法，只在 Copilot 重測；還是不行，就把「Copilot harness 靠搜尋找 skill」記成已知限制，本 task 以 Claude Code 與 Local 通過結案。
又回答了 6 個問題，都照建議：

1. **「不要搜尋」點名檔案搜尋、glob 與文字搜尋**，Copilot 兩次用的就是這些。
2. **寫明這些 skill 不在 agent 自己的 skill 清單裡**。
3. **找法改成依序讀**：對清單的每個根目錄，讀 `<root>/skills/<name>/SKILL.md`，直到讀到。
4. **Chores 一節加一句：說出 skill 名稱的請求不是 chore**。
5. **CHANGES.md 併進今天 97.1 那一筆**：Forge 還沒做，不另加一筆。
6. **先 commit，只在 Copilot 重測兩個提示**；Local 與 Claude Code 已通過，不重測。

改好之後：[AGENTS-tmp.md](../skill-groups/common/templates/AGENTS-tmp.md) 照上面改寫，`Technical words:` 加上 glob 與 pattern；範本與 AGENTS.md 通過 STE 檢查。

### 2026-11-02 Copilot 的第二次重測

只跑了 `/check-skill asd-ste 5.6`，整段提示都有送出；結論是 0 個 issue，沒有更新 Dashboard，也沒有 commit，但比上次更不照指示：

- 第一個想法是「Searching for chore summaries」，讀的第一個檔是 `chore-summary.md`；又搜尋了幾次，才讀 check-skill 的 SKILL.md。
  AGENTS.md 新加的「不是 chore」與「不用檔案搜尋、glob 或文字搜尋」都沒有照做。
- 把 `5.6` 當成 check 5 與 check 6，兩個都整個做了；`5.6` 是 criterion 5.6。
- facts 檔沒有放在 `temp/`，而是在根目錄新建 `scratchpad/`，用完也沒有刪；這兩個已經清掉。

reformat-md 沒有再跑：這一次已經足以判斷。

### 結案（已決定，2026-11-02）

使用者決定照「Copilot 的處理」的第二步結案，又回答了 6 個問題，都照建議：

1. **Copilot harness 不照 AGENTS.md 找 skill，記成已知限制**：細節寫在本 task，[[Task 97]] 的「知識」補一句。
2. **[[Task 97]] 的驗證改成 Claude Code 與 VS Code Local**，並標完成。
3. **CHANGES.md 今天 97.1 那一筆補一句**：在 Forge 請用 VS Code Local 或 Claude Code。
4. **Copilot 的其他問題只記在本 task**，不開新的 task。
5. **本 task 的「驗證」改成 Claude Code 與 Local**，「要做的」不動。
6. **兩個 commit**：先本 task，再 [[Task 97]]。

## 3. 要做的

1. 在 Copilot harness、Local harness 與 Claude Code 各開一個新的 session，請它執行一個 skill，例如 reformat-md：看它是否照 AGENTS.md 找到並讀了 SKILL.md。
2. 只給 skill 的名稱（例如「/check-skill asd-ste」）時，也試一次。
3. 找不到時，調整 AGENTS.md 的寫法，再試。
4. 把結果寫進本 task；InvestForge 的 `chat.agentSkillsLocations` 怎麼處理，交給 CHANGES.md 那一筆。

## 4. 驗證

- Claude Code 與 VS Code Local harness 的 session 都照 AGENTS.md 找到 `skill-groups/` 裡的 skill，並照 SKILL.md 做。
- VS Code Copilot harness 不照 AGENTS.md 找 skill，是已知限制，不在驗證的範圍。

## 5. 與其他 task 的關係

- [[Task 97]]：本 task 的上層，決定與官方說明寫在那裡。
- [[Task 97.2]]：建 AGENTS.md。
- [[Task 97.7]]：把 `.github` 改名為 `skill-groups`，並在範本寫明 skill 的位置。
- [[Task 93]]：description 超過 1024 字元的 skill 不會載入；實測前先確認都已縮短。

## 6. 知識

—

## 7. 日誌

### 2026-11-02

- 完成：Copilot 第二次重測仍先讀 chore 表、先搜尋，記成已知限制；驗證改成 Claude Code 與 Local；CHANGES.md 補一句。
- VS Code 的重測寫進「現況」：Local 通過，Copilot 仍靠搜尋；AGENTS.md 再改寫找法與 Chores 一節，等 Copilot 重測。
- Claude Code 的重測通過，寫進「現況」：兩個 session 都用 skill group 的根目錄找到 skill，沒有搜尋；剩 VS Code 的兩個 harness。
- VS Code 兩個 harness 的實測寫進「現況」：都靠搜尋找到 skill；AGENTS.md 改寫找法，列出 skill group 的根目錄，等重測。
- Claude Code 的實測通過，寫進「現況」；剩 VS Code 的兩個 harness。
- 改成新的做法：`.github` 改名為 `skill-groups`，AGENTS.md 寫明 skill 的位置，不用 symlink；標題與 Depends on 跟著改。
- 取消「做成 plugin」，見 [[Task 97.4]]。
- 候選做法加上「做成 plugin」（優先實測）與「根目錄 `skills/` 加 symlink」，見 [[Task 97]] 的決定。
- 提出。
