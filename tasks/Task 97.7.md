# Task 97.7 - 把 .github 改名為 skill-groups

**Status**：完成——`.github` 改名為 `skill-groups`，路徑都已改，CLAUDE.md 多了 Skills 一節；InvestForge 要照 CHANGES.md 跟上。
**Raised**：2026-11-02，使用者取消 plugin 的做法，決定把放 skill group 的 `.github` 改名為 `skill-groups`，由 AGENTS.md 寫明 skill 的位置。
**Depends on**：—

## 1. 背景

- `.github/` 底下只有兩個 skill group：`common` 與 `external`；沒有 GitHub 自己用的檔，例如 workflows。
- skill 引用其他檔時多半寫 `{skillGroups.common}`，由 `config.yaml` 的 `skillGroups` 代入；但也有直接寫 `.github/` 的地方。

## 2. 結論

—

## 3. 過程

### 2026-11-02 查的結果

- 不算 `tasks/` 與 `dashboard-hist/`，git 追蹤的檔裡有 72 個寫了 `.github/`。
- 最多的是 `chores/`（5 個），以及 gen-skill、compile-skill、check-skill、asd-ste 與 `rules/`（各 4 個）。
- `config.example.yaml` 有 2 處，`config-forge-tmp.yaml` 有 1 處。
- [publish_snapshot.py](../skill-groups/common/scripts/publish_snapshot.py) 發佈時排除 `.github/external/`。

### 已決定（2026-11-02）

使用者回答了 12 個問題，除了第 7 題的範圍後來擴大，都照建議：

1. **InvestForge 只靠 CHANGES.md**，由使用者在 InvestForge 做 follow-gestalt。
2. **少了 group 的舊路徑**（`.github\skills\<name>\...`）改成 `{skillGroups.common}/skills/<name>/...`。
3. **從根目錄寫的連結**只把 `.github` 換成 `skill-groups`。
4. **依賴的指紋這次一起重記**。
5. **範本新增 `## Skills` 一節**。
6. **兩個 commit**：先只做 `git mv`，再改內容。
7. **`tasks/` 與 `dashboard-hist/` 的舊紀錄不改**；但 `check_tasks.py` 對斷掉的連結報 FAIL，所以 task 檔的連結目標改成 `../skill-groups/`，字句不改，每個檔的日誌加一行；`dashboard-hist/` 仍不改。
8. **memory 跟著更新**。

### 2026-11-02 改好之後

- `a344e60` 只有 `git mv .github skill-groups`，165 個檔。
- 第二個 commit 改了 75 個檔、265 處路徑：一般的 `.github/` 換成 `skill-groups/`；notify-week、report-logs、report-skills 與 report-week 少了 group 的舊路徑改成 `{skillGroups.common}/skills/...`。
- 個別處理的地方：
  - [scan_skill.py](../skill-groups/common/skills/check-skill/scripts/scan_skill.py) 的 `GITHUB_PATH` 與 `MD_LINK` 認得 `skill-groups` 與 `.github` 兩種開頭；check-skill 的 SKILL.md 與中文版跟著改。
  - publish_snapshot.py 排除 `skill-groups/external/`。
  - asd-ste 的 Step 0：`--hidden` 的理由改成 skill group 可能在隱藏目錄裡，例如 `.claude`。
- [CLAUDE-tmp.md](../skill-groups/common/templates/AGENTS-tmp.md) 多了 `## Skills`，CLAUDE.md 重新產生；[CHANGES.md](../skill-groups/common/CHANGES.md) 加一筆。
- `config.yaml` 的 `skillGroups` 改成 `skill-groups/...`。
- 104 個 task 檔的 373 個連結改了目標，日誌各加一行。
- 26 個依賴的指紋重記。

### 後續

- report-skills 的 `main.py`（`SKILLS_DIR`、找 script 的 regex）與 report-logs 的 `read_metadata.py` 仍找 `.github/skills`：改名之前就是錯的路徑，程式沒動，要另外修。
- asd-ste 的 README 與中文版第 449 行記的是當時的驗證「在副本放一份 `.github`」，是紀錄，沒改。
- InvestForge 的 `config.yaml` 與 `InvestForge.code-workspace` 仍指向 `.github/common`，照 CHANGES.md 改之前，它找不到 common。

## 4. 要做的

1. 用 `git mv` 把 `.github` 改名為 `skill-groups`。
2. 改 `config.yaml`、[config.example.yaml](../config-tmp.yaml) 與 `config-forge-tmp.yaml` 的 `skillGroups`；key 仍是 `skillGroups`。
3. 改 72 個檔裡的 `.github/`，中文版也是；STE 檔與依賴的指紋照規定重記。
4. 改 publish_snapshot.py 排除的路徑，以及 [publish-gestalt](../chores/publish-gestalt.md) 與其他 chore 的路徑。
5. 在範本 [CLAUDE-tmp.md](../skill-groups/common/templates/AGENTS-tmp.md) 寫明 skill 在 `skill-groups/<group>/skills/<name>/SKILL.md`，要執行 skill 時讀它；[[Task 97.2]] 把它變成 AGENTS.md。
6. 重新產生 CLAUDE.md；在 CHANGES.md 加一筆，讓 InvestForge 改 `skillGroups.common` 的路徑與 `chat.agentSkillsLocations`。

## 5. 驗證

- `git grep -F '.github/'` 只剩 `tasks/` 與 `dashboard-hist/` 的舊紀錄，以及上面「後續」列的兩支程式。
- `check_tasks.py`、`check_chores.py` 與 `gen_claude_md.py --check` 通過。
- 改過的 STE 檔通過 `check_ste.py`，twin 通過 parity check。
- `publish_snapshot.py` 的預覽不含 `skill-groups/external/`。

## 6. 與其他 task 的關係

- [[Task 97.1]]：改名之後，實測 agent 是否照 AGENTS.md 找到 skill；它依賴本 task。
- [[Task 97.2]]：範本變成 AGENTS.md；本 task 寫的 skill 位置跟著進去。
- [[Task 97.4]]：plugin 的做法取消之後，改用本 task。

## 7. 知識

—

## 8. 日誌

### 2026-11-02

- 連結的目標從 `CLAUDE-local.md`、`CLAUDE-tmp.md`、`gen_claude_md.py` 改成改名後的 `AGENTS-local.md`、`AGENTS-tmp.md`、`gen_agents_md.py`，字句沒有改（[[Task 97.2]]）。
- 完成：改名、改路徑、加 Skills 一節、重記指紋，task 檔的連結目標跟著改。
- 提出。
