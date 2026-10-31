# Task 86 - chore 改用名稱，不用編號，和 skill 一樣

**Status**：完成——2026-10-30 chore 改用名稱（`rerecord-ste-custom`、`keep-english`、`publish-github`），名稱在所有 agency 裡只有一個；chore 檔只放定義，執行紀錄搬到各 agency 的摘要表；別的 agency 的 chore 在摘要表寫成文字的名稱，由 `agencies` 找到定義，不再用使用檔。
**Raised**：2026-10-30，[[Task 85]] 讓別的 agency 使用本 agency 的 chore 之後，使用者提出：chore 不應該用編號命名，要和 skill 一樣用名稱。
**Depends on**：[[Task 85]]

## 1. 背景

- chore 和 skill 一樣，是會重複做、也會被別的 agency 引用的單位。
- 編號只在一個 agency 裡有意義：同一件 keep-English 稽核，在本 agency 是 Chore 2，在 InvestForge 是 Chore 1 @ InvestForge；名稱則到哪裡都一樣，也比編號好認。
- [[Task 85]] 之後，chore 的編號出現在跨 agency 的引用 `Chore N @ <agency>`、checkpoints 的路徑 `checkpoints/chores/<agency>/chore-<N>`、`config.yaml` 的 `keepEnglishChore` 與 `gen_claude_md.py` 產生的連結裡。

## 2. 現況

### 2026-10-30 用到 chore 編號的地方

- 本 agency 的三個 chore：`chores/Chore 1.md`（集中重記 ste-custom.md）、`Chore 2.md`（keep-English 稽核）、`Chore 3.md`（發佈到 GitHub）。
- [chore-rules.md](../.github/common/rules/chore-rules.md) 與中文版：檔名 `Chore N.md`、標題 `# Chore N - 標題`、Numbers 一節（從 1 開始、不重用、`空號：` 那一行）、摘要表照編號由新到舊、commit 前綴 `chore N: `、跨 agency 的 `Chore N @ <agency>`、使用檔、checkpoints 的 `chore-<N>`。
- `check_chores.py`：約 40 處和編號有關，例如檔名格式、連續編號、空號、排序與 `[[Chore N]]` 的連結。
- [dashboard/chore-summary.md](../dashboard/chore-summary.md)：每一列 `[[Chore N]]`。
- task 檔裡有 112 個 `[[Chore N]]` 的連結；CLAUDE-local.md、CLAUDE.md、`config.example.yaml`、`gen_claude_md.py`、`dashboard/task-summary.md` 也有。
- `checkpoints/chores/SkillsGestalt/chore-2/` 放 keep-English 稽核的報告。

### 2026-10-30 做完之後

- [chore-rules.md](../.github/common/rules/chore-rules.md) 與中文版：
  - Files：檔名是名稱加 `.md`；摘要表除了表格與圖例，還有執行紀錄；workspace 可以做它所用的 skill group 所屬 agency 的 chore。
  - 新的 Names 一節取代 Numbers：小寫字母、數字與連字號，以字母開頭；所有 agency 裡沒有兩個 chore 同名；可以改名，由那個 task 改連結與執行紀錄；停用的檔案留著，名稱不再用；拿掉 `空號：` 那一行。
  - Links：本 workspace 的 chore 用 `[[<name>]]`，別的 agency 的 chore 寫成文字的名稱；task 仍是 `Task N @ <workspace>`。
  - A Chore of a Different Agency 取代 Task 85 的使用檔：在自己的摘要表加一列，Chore 欄寫文字的名稱，Title 與何時要做和定義一樣，Started 與 Status 是自己的；`agencies` 給出那些 agency 的根目錄。
  - The Chore File：五章，拿掉 `6. 執行紀錄`；checkpoints 放在 `checkpoints/chores/<name>`。
  - The Summary Table：照 Started 排、新的在前、同日照名稱；圖例下面 `## 執行紀錄`，每個 chore 一個 `### <name>`，裡面每天一個 `#### yyyy-mm-dd`。
  - Commits：`chore <name>: `。
- [check_chores.py](../.github/common/scripts/check_chores.py) 改寫：以名稱取代編號；別的 agency 的列由 `config.yaml` 的 `agencies` 找到定義檔，比對 Title 與何時要做；檢查摘要表的執行紀錄與上次執行；不再檢查連續編號與空號；仍只用標準函式庫，`agencies` 由程式自己讀；新加 `--config`，預設是摘要表所在資料夾的上一層的 `config.yaml`。
- 三個 chore 用 `git mv` 改名，標題改成 `# <name> - <標題>`，`6. 執行紀錄` 搬到 [dashboard/chore-summary.md](../dashboard/chore-summary.md) 的 `## 執行紀錄`（日期從 `###` 變成 `####`）；步驟裡的執行紀錄、commit 前綴與 checkpoints 路徑跟著改；keep-english 的報告搬到 `checkpoints/chores/keep-english/`。
- `config.example.yaml` 與本機的 `config.yaml` 的 `keepEnglishChore` 改成 `keep-english`；[gen_claude_md.py](../.github/common/scripts/gen_claude_md.py) 把它連到 `chores/<name>.md`，本 agency 沒有這個檔時，從 `agencies` 找到唯一有它的 agency，連結寫成從根目錄起算的相對路徑。
- CLAUDE-local.md 的發佈連結改成 [[publish-gestalt]]，重新產生 CLAUDE.md；`publish_snapshot.py` 的 commit 前綴改成 `chore publish-github: `。
- 29 個 task 檔的 `[[Chore N]]` 改成新名稱，各加一行日誌；本檔說明對照關係的地方改成純文字；Task 26 的 Markdown 連結改成 `../chores/publish-github.md`。
  task 檔裡寫在 inline code 的 `chores/Chore N.md` 與 commit 前綴是當時的紀錄，照舊。

### 2026-10-30 沒有 chores/ 的 workspace

- InvestForge 照新寫法改好之後（Task 15 @ InvestForge），只做別的 agency 的 chore，`chores/` 變成空的；git 不追蹤空資料夾，重新 clone 就沒有 `chores/`，而 `check_chores.py` 遇到不是資料夾的 `--chores-dir` 就以 `2` 結束。
- `check_chores.py` 把不存在的 `chores/` 當成沒有檔案，開頭那行印出它不存在；`--chores-dir` 指到一個檔案時照舊以 `2` 結束；有 `[[<name>]]` 的列卻沒有檔時照舊 FAIL。
- [chore-rules.md](../.github/common/rules/chore-rules.md) 與中文版的 Files 加一句：只做別的 agency 的 chore 的 workspace，可以沒有 `chores/`。

## 3. 要做的

### 已決定（2026-10-30）

- 檔案是 `chores/<name>.md` 一個檔；名稱是 kebab-case，和 skill 一樣，在一個 agency 裡不重名。
- 標題行是 `# <name> - <標題>`，例如 `# keep-english - keep-English 稽核`。
- 現有三個 chore 的名稱：Chore 1 改為 `rerecord-ste-custom`，Chore 2 改為 `keep-english`，Chore 3 改為 `publish-github`。
- 摘要表照 Started 排，新的在前；同一天再照名稱。
- commit 前綴是 `chore <name>: `，例如 `chore keep-english: `。
- task 檔裡的 `[[Chore N]]` 全部依對照表改成新名稱，連結不斷；每個被改的 task 加一行日誌。
- 只改 chore；task 會完成，照舊用流水號。

### 開始做時決定的（2026-10-30）

- 名稱：小寫字母、數字與連字號，以字母開頭；不規定動詞開頭。
- 可以改名，由做這件事的 task 把連結一起改；停用的 chore 檔留著，名稱不再用；搬到別的 workspace 的不另外記，拿掉 `空號：` 那一行。
- 名稱和 skill 一樣在所有 agency 裡只有一個，所以沒有 `<name> @ <agency>` 的寫法，也沒有同名的使用檔；`keepEnglishChore` 直接寫名稱。
- 不要使用檔：別的 agency 的 chore 在自己的摘要表寫成文字的名稱，`check_chores.py` 依 `agencies` 去各 agency 的 `chores/` 找。
- 每個 agency 的執行紀錄都寫在自己的 `chore-summary.md`，包括自己的 chore：chore 檔只有定義，拿掉 `6. 執行紀錄`。
- 執行紀錄放在圖例下面的 `## 執行紀錄`，每個 chore 一個 `### <name>`，裡面是 `#### yyyy-mm-dd`。
- checkpoints 的路徑是 `checkpoints/chores/<name>`，不再分 agency。
- `check_chores.py` 的檔名就是 chore 的名稱。

### 步驟

1. [chore-rules.md](../.github/common/rules/chore-rules.md) 與中文版：檔名、標題、命名規則取代 Numbers 一節、摘要表的排序、commit 前綴、跨 agency 的寫法、使用檔、checkpoints 的路徑。
2. `check_chores.py`：以名稱取代編號的檢查，例如檔名、標題、排序、連結。
3. 三個 chore 檔改名、改標題與內文；報告搬到新的 checkpoints 路徑。
4. 摘要表、task 檔、CLAUDE-local.md、`config.example.yaml`、本機的 `config.yaml`、`gen_claude_md.py` 改成新名稱，重新產生 CLAUDE.md。
5. 跑 `check_chores.py`、`check_tasks.py`、`gen_claude_md.py --check`。

## 4. 驗證

- `check_chores.py` 與 `check_tasks.py` 都是 PASS；`gen_claude_md.py --check` 是 PASS。
- repo 裡找不到 `[[Chore N]]`、`chores/Chore N.md` 或 `chore-<N>` 的路徑，只剩 commit 訊息等歷史。
- `keep-english` 的 `due` 照新的報告路徑是 not due。
- chore-rules.md `check_ste.py` 是 PASS，與中文版 `check_parity.py` 是 0 failure。

2026-10-30 的結果：

- 本 agency：`check_chores.py` 16 passed，`check_tasks.py` 18 passed，`gen_claude_md.py --check` 是 PASS；keep-english 照新的路徑跑 `due` 是 not due。
- 以本 agency 的副本試 `check_chores.py`：兩列對調、執行紀錄的順序不對、`### no-such-chore`、上次執行和執行紀錄不一致、`Keep English.md` 這種檔名、標題的名稱和檔名不同，都各報 FAIL。
- 模擬的 Forge：摘要表一列文字的 `keep-english` 加上它的執行紀錄，`config.yaml` 設 `agencies.SkillsGestalt`：`check_chores.py` 16 passed；拿掉 `agencies` 就 FAIL，`gen_claude_md.py` 以 `2` 結束；以 InvestForge 的真實位置計算，連結是 `../SkillsGestalt/chores/keep-english.md`。
- chore-rules.md `check_ste.py` 是 PASS，與中文版 `check_parity.py` 是 0 failure；`reformat_md.py --mode clean` 不改動 chore 檔、摘要表與任何 task 檔。
- repo 裡沒有 `[[Chore N]]` 的連結；`chores/Chore N.md` 只出現在 task 檔的 inline code 裡，是當時的紀錄。

## 5. 與其他 task 的關係

- [[Task 85]]：讓別的 agency 以使用檔使用本 agency 的 chore，並定下 checkpoints 的路徑；本 task 把其中的編號都換成名稱。
- [[Task 84]]：`keepEnglishChore` 與 `gen_claude_md.py` 的連結。
- InvestForge 的 chore 改成用名稱，在它自己的 tasks 做：`check_chores.py` 已經改了，InvestForge 的 `Chore 1.md` 與 `[[Chore 1]]` 那一列在它改之前會 FAIL。

## 6. 知識

—

## 7. 日誌

### 2026-10-31

- [[Task 91]] 把 chore `publish-github` 改名為 `publish-gestalt`：本檔的連結跟著改，意思不變。

### 2026-10-30

- 建立 task：chore 改用 kebab-case 的名稱，檔案 `chores/<name>.md`，標題 `# <name> - <標題>`，摘要表照 Started 排，commit 前綴 `chore <name>: `；task 檔裡的舊連結全部改成新名稱。
- 開始做並完成：chore-rules.md 與中文版、`check_chores.py`、`gen_claude_md.py` 改用名稱；三個 chore 改名，執行紀錄搬到摘要表；29 個 task 檔的連結改成新名稱。
- InvestForge 回報沒有 `chores/` 時檢查會失敗：`check_chores.py` 把不存在的 `chores/` 當成空的，chore-rules.md 與中文版加上一句。
