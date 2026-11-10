# Task 101 - 讓 Dropbox 不同步 SkillsGestalt 的 .git

**Status**：完成——`.git` 設了 File Provider 的忽略屬性 `com.apple.fileprovider.ignore#P`，repo 仍在原路徑；整個 repo 備份成根目錄旁的 `SkillsGestalt.bundle`，[[publish-gestalt]] 與 [[pull-gestalt]] 最後一步重做它。
**Raised**：2026-11-10，Dropbox 兩次放回舊的 `.git/rebase-merge`，讓 git 以為 rebase 還在進行。
**Depends on**：—

## 1. 背景

- repo 在 `~/Library/CloudStorage/Dropbox/2-Areas-I/SkillsGestalt`，`.git` 跟著 Dropbox 同步，沒有忽略屬性；`.git` 約 28 MB、1654 個檔，其中 1604 個 loose object。
- 2026-10-31 的 [[pull-gestalt]] 之後留下一個空的 `.git/rebase-merge`。
- 2026-11-10 第二次 pull-gestalt 之前，`.git/rebase-merge` 又出現，內容是早上那次 rebase 停在 128/157 時的狀態；那次 rebase 早已做完。
  `git rebase --abort` 會把 `m1` 拉回 `a04f0d1`，所以只把目錄搬走，見 `chore-summary.md` 的執行紀錄。
- `m1` 的歷史與 `archive/*` tag 只在本機的 `.git`；GitHub 只有 `main` 的快照。

## 2. 結論

- 選了「只讓 Dropbox 忽略 `.git`」，不把 clone 搬出 Dropbox：路徑不變，InvestForge 與 BookMaster 都不用改。
- 備份是 `git bundle --all`，放在 `~/Library/CloudStorage/Dropbox/2-Areas-I/SkillsGestalt.bundle`，只留最新一份，舊版靠 Dropbox 的版本紀錄。
- 第一份 bundle 驗證過，也從它還原到 scratchpad 比對過，見「3. 過程」。
- 兩份 chore 各加一步與一條驗證，見表 1。

**表 1：改的檔**

| 檔 | 改了什麼 |
| --- | --- |
| [publish-gestalt.md](../chores/publish-gestalt.md) | 第 7 步做 bundle；第 4 章加一條驗證；第 5 章加本 task |
| [pull-gestalt.md](../chores/pull-gestalt.md) | 第 11 步做 bundle；第 4 章加一條驗證；第 5 章加本 task |

## 3. 過程

### 調查（2026-11-10）

- 本機的 Dropbox 是 macOS File Provider 版（路徑在 `~/Library/CloudStorage/`）。
  這一版的忽略屬性是 `com.apple.fileprovider.ignore#P`；`com.dropbox.ignored` 只用在舊的 `~/Dropbox` 位置。
- CountDell：`chore-summary.md` 2026-11-02 的執行紀錄寫它在公開 repo 的 clone 上做 `countdell`，本 `.git` 也沒有 `countdell` 分支。
  使用者確認 CountDell 有裝 Dropbox，但不用這個資料夾；它 Dropbox 裡的 `.git` 副本會跟著消失，不影響它自己的 clone。
- 若把 clone 搬出 Dropbox，要改的地方見表 2；這個方案沒有選。

**表 2：寫了這個 Dropbox 路徑的地方**

| 檔 | 行 |
| --- | --- |
| `InvestForge/config.yaml` | 5（`skillGroups.common`）、10（`agencies.SkillsGestalt`） |
| `InvestForge/AGENTS.md` | 10、19、39、42、76、89，由 `gen_agents_md.py` 產生 |
| `InvestForge/InvestForge.code-workspace` | 24、25 |
| `BookMaster/config.yaml`、`BookMaster.code-workspace` | 3、36，已經是舊的 `.github/common` 路徑 |
| [check_chores.py](../skill-groups/common/scripts/check_chores.py) | 17，說明文字裡的例子 |
| [chore-rules.md](../skill-groups/common/rules/chore-rules.md) 與中文版 | 71，例子 |
| [skill_tokens.py](../scripts/skill_tokens.py) | 54 |
| Claude Code 的記憶目錄 | 以路徑命名：`~/.claude/projects/-Users-visualge-Library-CloudStorage-Dropbox-2-Areas-I-SkillsGestalt` |

### 使用者的決定（2026-11-10）

用選項問了 8 個問題；CountDell 那一題見「調查」，其他的決定如下：

1. 只讓 Dropbox 忽略 `.git`。
2. 備份用 `git bundle --all`。
3. 每次 [[publish-gestalt]] 與 [[pull-gestalt]] 之後做一次。
4. bundle 放在 `Dropbox/2-Areas-I/SkillsGestalt.bundle`，只留最新一份。
5. 只處理 SkillsGestalt；InvestForge 與 BookMaster 的 `.git` 也在 Dropbox、沒有忽略，留給以後。
6. 做 bundle 的指令寫在兩份 chore 的步驟裡，不改 common 的 script，所以不加 `CHANGES.md`。
7. 建 task 並馬上執行。

### 執行（2026-11-10）

1. 從根目錄跑 `git bundle create ../SkillsGestalt.bundle.tmp --all && git bundle verify -q ../SkillsGestalt.bundle.tmp && mv -f ../SkillsGestalt.bundle.tmp ../SkillsGestalt.bundle`：11.6 MB，26 個 head，等於 25 個 ref 加 HEAD。
2. `git clone --mirror` 到 scratchpad：`m1` 是 `3de7748`、`archive/master` 是 `c501a98`，都和本機相同；`git fsck` 沒有錯。
3. 跑 `xattr -w 'com.apple.fileprovider.ignore#P' 1 .git`；`xattr -l .git` 有 `com.apple.fileprovider.ignore#P: 1`；`git status` 照常。

## 4. 要做的

- 在 Dropbox 的 app 或 dropbox.com 確認 `SkillsGestalt/.git` 不再同步，dropbox.com 上的 `.git` 進了刪除的檔案。
- 要復原時：`git clone --mirror <bundle> <dir>/.git`，再 `git -C <dir> config --bool core.bare false` 與 `git -C <dir> reset --hard m1`；或在現有的 repo 跑 `git fetch <bundle> 'refs/*:refs/*'`。

## 5. 驗證

- `xattr -p 'com.apple.fileprovider.ignore#P' .git` 印出 `1`。
- `git bundle verify -q ../SkillsGestalt.bundle` 印出 `is okay`。
- `check_tasks.py` 與 `check_chores.py` 都是 PASS。

## 6. 與其他 task 的關係

- [[Task 89]]：建立 [[pull-gestalt]]，本 task 在它最後加一步。
- [[Task 78]]：建立 [[publish-gestalt]]，本 task 在它最後加一步。

## 7. 知識

### 適合寫成新 topic

- **Dropbox 的 File Provider 版怎麼忽略一個資料夾**：在 `~/Library/CloudStorage/Dropbox` 下用 `xattr -w 'com.apple.fileprovider.ignore#P' 1 <path>`；舊的 `~/Dropbox` 才用 `com.dropbox.ignored`。
  忽略之後本機的檔留著，雲端與別台電腦的副本會被刪。
  來源：本 task 的調查。

### 適合併進現有 topic

—

### 不算知識

- bundle 的路徑 `Dropbox/2-Areas-I/SkillsGestalt.bundle`，以及表 2 的各行號。

## 8. 日誌

### 2026-11-10

- 建立本 task：調查、問使用者、做第一份 bundle、設忽略屬性，兩份 chore 加上做 bundle 的一步。
