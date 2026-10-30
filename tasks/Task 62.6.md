# Task 62.6 - SkillsGestalt 自己的 config.yaml

**Status**：完成——2026-10-20 根目錄有了 config.yaml，wikiDir 是新的 vault SkillsLlmWiki，使用者在 Obsidian 把它打開成 vault；使用者看過。
**Raised**：2026-10-18，[[Task 62]] 拆出的第 6 步：這裡沒有 `config.yaml`，要 `--config` 的工具一直借 InvestForge 的。
**Depends on**：—

## 1. 背景

- 要 `--config` 的工具：check-skill 的 `scan_skill.py`，以及 `depends_on.py record ... --config config.yaml`。
- 借用的紀錄：[[Task 7]]、[[Task 35]]、[[Task 39]] 與 [[Task 50]]。
  [[Task 7]] 也記了另一種做法：臨時寫一份只有 `skillGroups: {common: <workspace>/.github/common}` 的 config。
- check-skill 的 [update_dashboard.py](../.github/common/skills/check-skill/scripts/update_dashboard.py) 把結果寫進 `wikiDir` 底下的 `dashboard/skills.md`，每個 skill group 一節。
  現在那份在 InvestForge 的 `wikiDir`（InvLlmWiki）裡，表上只有 common 的 asd-ste 一列。
- memory 的 repo-skills-run-by-hand 寫著：這裡的根目錄沒有 config.yaml，`{skillGroups.common}` 就取 `.github/common`。

## 2. 現況

### 2026-10-20 查的結果

- 這裡有 30 個 common skill 在 Step 0 讀根目錄的 config.yaml。
  這裡會用到的 check-skill、gen-skill、gen-rsdc-skill、chinese、asd-ste 等，只要 `skillGroups` 與 `wikiDir`；`vaultName` 是 `wikiDir` 的最後一段。
- 其他 workspace 各有自己的 wiki vault：AccountQuick 用 AccLlmWiki、BookMaster 用 BookLlmWiki、InvestForge 用 InvLlmWiki；iCloud 的 Obsidian Documents 裡沒有給這裡用的。
- InvLlmWiki 裡已經有 common skill 的報告資料夾，以及 Skills Dashboard 的 common 一節。
- 讀 config 的 script 中，`depends_on.py` 與 `scan_skill.py` 會展開 `~`；其他的由 Step 0 代換好路徑再傳進去。
- 這裡有兩個 skill group：`.github/common`，以及 `.github/external`，裡面有 eli5。

### 已決定（2026-10-20）

動手前問了 8 個問題，都照建議：

- `wikiDir` 是新的 vault SkillsLlmWiki，放在 iCloud 的 Obsidian Documents，和其他 workspace 的 vault 並列；MD 報告與 Skills Dashboard 都寫在那裡，不在 git 裡。
- `skillGroups` 列 common 與 external，都是相對路徑；不加其他鍵，之後哪個 skill 在這裡要用再加。
- `wikiDir` 寫完整的絕對路徑，和 InvestForge 一樣，因為不是每支 script 都會展開 `~`。
- config.yaml 進 git；換機器時改 `wikiDir` 那一行。
- vault 的資料夾由本 task 建；使用者在 Obsidian 以「開啟資料夾為 vault」打開它，obsidian:// 連結才開得了。
- InvLlmWiki 的 Skills Dashboard 不手動改：check-skill 規定儀表板只由 `update_dashboard.py` 寫。
  那裡的 common 一節保留，在 Task 10 @ InvestForge 記下它不再更新，要不要拿掉由那邊決定。
- 這裡的 Skills Dashboard，在下一次 check-skill 時由 `update_dashboard.py` 建立。
- 根目錄 CLAUDE.md 寫明 `{skillGroups.common}` 照 config.yaml；memory 的 repo-skills-run-by-hand 跟著改。
- InvestForge 的修改是這裡的 session 做的，前綴用 `task 62.6`，和 [[Task 62.4]] 一樣。

### 結果（2026-10-20）

- 根目錄的 [config.yaml](../config.yaml)：`wikiDir` 與 `skillGroups` 的 common、external。
- 新建 `SkillsLlmWiki/` 與它的 `dashboard/`，都是空的。
- 根目錄 [CLAUDE.md](../CLAUDE.md) 的 Tasks 一節，寫明 `{skillGroups.common}` 照 config.yaml。
- [[Task 54]]：「已決定」加上 Skills Dashboard 的位置。
- Task 10 @ InvestForge：記下那裡的儀表板 common 一節不再更新，要不要拿掉列進它的「要決定的」。
- memory 的 repo-skills-run-by-hand 改成這裡有自己的 config.yaml。
- 使用者以「開啟資料夾為 vault」打開 SkillsLlmWiki：它有了 `.obsidian/`，Obsidian 的 vault 清單也有它。

## 3. 要做的

1. ✅ 在根目錄寫 `config.yaml`：`skillGroups.common` 是 `.github/common`，再加上這裡的工具要的其他鍵。
2. ✅ 決定 Skills Dashboard 放哪裡，[[Task 54]] 照它寫。
3. ✅ 改 memory 的 repo-skills-run-by-hand。
4. ✅ 使用者在 Obsidian 打開 SkillsLlmWiki。
5. ✅ 使用者看過之後 commit：這裡一個，InvestForge 一個，前綴都是 `task 62.6`。

## 4. 驗證

- 在這裡跑 `scan_skill.py` 與 `depends_on.py check`，`--config` 給這裡的 `config.yaml`，不用到 InvestForge 的任何檔。
- `{wikiDir}/dashboard/` 存在，`update_dashboard.py` 可以寫到 `{wikiDir}/dashboard/skills.md`。

### 結果（2026-10-20）

- `scan_skill.py --config config.yaml`：asd-ste 找到在 common，eli5 找到在 external。
- `depends_on.py check --config config.yaml` 對 imp-home 的 Home-RSDC.md：經由 skillGroups 找到 `[[RSDC-App-tmp]]` 等 3 筆紀錄，都是 UNCHANGED。
- config.yaml 以 `yaml.safe_load` 讀得出來；`wikiDir` 與它的 `dashboard/` 都存在，vaultName 是 SkillsLlmWiki。

## 5. 與其他 task 的關係

- [[Task 54]]：Chore 3 的 Skills Dashboard 照本 task 決定的位置。
- [[Task 7]]：臨時 config 的做法。
- Task 10 @ InvestForge：那裡的儀表板 common 一節，本 task 之後不再更新。

## 6. 日誌

### 2026-10-20

- 開始：問了 8 個問題，見「已決定」。
- 寫好 config.yaml，建好 SkillsLlmWiki 的資料夾，改了 CLAUDE.md、[[Task 54]]、Task 10 @ InvestForge 與 memory；驗證的結果記在第 4 章。
- 驗證的第 2 項原本是 `update_dashboard.py` 寫到決定的位置；它只寫真的檢查結果，所以改成確認路徑，第一列等下一次 check-skill。
- 使用者第一次是在 Documents 這個 vault 裡把 SkillsLlmWiki 當資料夾打開，它沒有成為 vault；改用「開啟資料夾為 vault」之後，`.obsidian/` 與 Obsidian 的 vault 清單都有它了。
- 使用者看過，同意 commit；本 task 完成。

### 2026-10-18

- 從 [[Task 62]] 拆出。
