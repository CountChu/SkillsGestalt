# Chores

會重複做的例行工作。
每個 chore 是 `chores/<name>.md` 一個檔案，用名稱命名，例如 `keep-english.md`。
本檔只放下面的摘要表：先讀這張表，看哪一項該做了，再只開需要的那個 chore。
chore 檔的格式與摘要表的維護方式，見 [chore-rules.md](../.github/common/rules/chore-rules.md)；檢查指令見根目錄的 [CLAUDE.md](../CLAUDE.md)。

| Chore | Started | Title | 何時要做 | 上次執行 | Status |
| --- | --- | --- | --- | --- | --- |
| [[follow-gestalt]] | 2026-10-31 | 跟上 Gestalt 的改動 | `{skillGroups.common}/CHANGES.md` 有比上次處理的那一筆新的條目 | — | 🔁 |
| [[pull-gestalt]] | 2026-10-31 | 把 GitHub 上的新快照拿進工作分支 | 發佈之前、git fetch 看到新快照時，或使用者要求時 | 2026-10-31 | 🔁 |
| [[publish-gestalt]] | 2026-10-30 | 發佈到 GitHub | 使用者要求發佈到 GitHub 時 | 2026-10-31 | 🔁 |
| [[keep-english]] | 2026-10-18 | keep-English 稽核 | tw-keep-english.md 換了版本，和上次稽核的版本不同 | 2026-10-30 | 🔁 |
| [[rerecord-ste-custom]] | 2026-10-18 | 集中重記 ste-custom.md | 當天改過 ste-custom.md，而且當天的修改都做完了 | 2026-10-30 | 🔁 |

Status：🔁 使用中　⏸️ 暫停　⏹️ 停用。

上次執行：下面「執行紀錄」一節裡這個 chore 最新的日期；— 表示還沒做過。

## 執行紀錄

### pull-gestalt

#### 2026-10-31

- 第一次，在 [[Task 89]] 照手動步驟做：GitHub 的 `main` 有另一台電腦從 `countdell` 發佈的 `4765af0`，作者與 committer 是工作的身分。
  經使用者同意，在本機做出同樣檔案、訊息與時間、作者改成 CountChu 的 `4d2c5db`，以 `--force-with-lease` 換掉 GitHub 上的 `4765af0`。
- 本機 `main` 從 `93b4e1e` 移到 `4d2c5db`；舊的 `m1`（`e0365fc`）存成 tag `archive/m1-261031-pull`；`m1` 的 3 個 commit rebase 到 `4d2c5db` 上，沒有衝突；`external/` 與 `.github/external/` 仍在。
- 新快照把 task 改成七章：只在 `m1` 上的 [[Task 89]] 插入 `6. 知識`；CLAUDE.md 重新產生。

### publish-gestalt

#### 2026-10-31

- 以 `m1` 的 `b2e967f` 做出快照 `93b4e1e`，接在 `258940e` 之後，推到 `main`；變動 63 個檔，新增 23、改名 3、刪除 1、修改 36，來自 [[Task 26]]、[[Task 79]] 到 [[Task 88]]，以及 keep-english 與上次 publish-github 的執行紀錄。
  `check` 與 `publish` 的掃描都是 `nothing found`。
  `m1` 跟著從 `93b4e1e` 重新開始（`b9933dd`），舊的在 tag `archive/m1-261031`；GitHub 上確認：`main` 有 4 個 commit，最新的是 `93b4e1e`，tree 和本機做出的 `e5c202f` 相同，289 個檔裡沒有排除的路徑。

#### 2026-10-30

- 第一次在 `m1` 與 `main` 的新名稱下發佈：以 `m1` 的 `fb13518` 做出快照 `258940e`，接在 `cba1032` 之後，推到 `main`；變動 6 個檔，是 [[Task 79]] 的改名與重做 `m1`。
  `m1` 跟著從 `258940e` 重新開始（`54647f7`），舊的在 tag `archive/m1-258940e`，後來改名為 `archive/m1-261030`；GitHub 上確認：`main` 有 3 個 commit，267 個檔裡沒有排除的路徑。
- 第一次用程式發佈：以 master 的 `caadd77` 做出快照 `cba1032`，接在 `b2c697a` 之後，推到 `main`；變動 6 個檔，就是本 chore、程式與 [[Task 78]] 完成的那些。
  GitHub 上確認：`main` 有 2 個 commit，266 個檔裡沒有排除的路徑。
- 第一次發佈，在程式寫好之前照 [[Task 78]] 的步驟手動做：以 master 的 `9629f0a` 做出快照 `b2c697a`，建立公開的 repo，推到 `main`。
- 寫好程式之後試跑：`check` 對 master 的 `5c5094a` 是 `nothing found`；對清理之前的 `6cb068b` 找到 101 筆，以 `1` 結束。

### keep-english

#### 2026-10-30

- 清單 261030 版（[[Task 81]] 加上 agency、Forge、Gestalt）：37 對中英對照，18 份中文版有 186 行警告。
- 和 2026-10-20 的 261018 版相比：0 筆新出現，5 筆消失，都是 compile-skill 的 `SKILL-tw.md` 與 `SkillCompiler-RSDC-tw.md`；新加的三個 term 沒有找到任何一筆。
- 最多的 3 種譯法：script 的「腳本」133 行（15 份）、step 的「步驟」24 行（1 份）、identifier 的「識別碼」7 行（5 份）。
- 「英文也寫中文」1 行，不算進警告：MermaidView-RSDC-tw.md 的「角色」，和上次相同。
- 只列出，沒有改中文版；要改的仍記在 [[Task 73]]。
- 報告：`checkpoints/chores/keep-english/2026-10-30-261030.txt`，2026-10-30 從 `checkpoints/chores/chore-2/` 搬過來。

#### 2026-10-20

- 清單 261018 版：33 對中英對照，19 份中文版有 264 行警告；這是第一份報告，沒有上一份可比。
- 最多的 3 種譯法：script 的「腳本」206 行（16 份）、step 的「步驟」24 行（1 份）、identifier 的「識別碼」9 行（6 份）。
- 「英文也寫中文」1 行，不算進警告：MermaidView-RSDC-tw.md 的「角色」。
- 只列出，沒有改中文版；要改的記在 [[Task 73]]。
- 報告：`checkpoints/chores/keep-english/2026-10-20-261018.txt`，2026-10-30 從 `checkpoints/chores/chore-2/` 搬過來。

### rerecord-ste-custom

#### 2026-10-30

- 第四次執行：[[Task 61]] 讓 ste-custom.md 第 8 行改成照 ste-rules 的 House Rule 5，之後 `draft.py recheck --root . --root ../InvestForge` 重檢 26 份，26 份都重記，以 0 結束；新指紋 `8cc2e2061175`。
  這次沒有草稿；13 份 STE 檔的 `check_ste.py --ste` 都 PASS，警告和之前相同：RSDC-Standard 4 則被動句，tw-keep-english 與 md-style 是 no-op 被拆成的 op；13 份中文版跟著英文檔重記。
  比上次多的 2 份是 README-tmp 與它的中文版；InvestForge 沒有記錄 ste-custom.md 的檔案。

#### 2026-10-19

- 第三次執行：[[Task 32.8]] 到 [[Task 32.11]] 審核時，ste-custom.md 又改了幾次，加上 program、deterministic、search、need、exception、run、prompt 等字與保留名稱的規則。
  SKILL-tmp 取代原檔之後，`draft.py recheck --root .` 重檢 24 份，24 份都重記，以 0 結束；新指紋 `5978e1af2fcf`。
  SKILL-tmp 的草稿每次修改後都立刻跑了 Step 3，取代後的 SKILL-tmp.md 與它的中文版已記著新指紋，不在這 24 份裡；InvestForge 沒有記錄 ste-custom.md 的檔案。
  12 份 STE 檔的 `check_ste.py --ste` 都 PASS，警告和之前相同：RSDC-Standard 4 則被動句，tw-keep-english 與 md-style 是 no-op 被拆成的 op；12 份中文版跟著英文檔重記。
  所有草稿都已取代，這次沒有草稿；之後 `--dry-run` 一份都不列。

#### 2026-10-18

- 第一次執行：當天 ste-custom.md 最後一次修改是 [[Task 52]]，之後 `draft.py recheck --root .` 重檢 22 份，22 份都重記，以 0 結束；新指紋 `3c5050b6a240`。
  6 份草稿的檢查都 PASS，沒有新的 WARN，`step_3` 都已存；5 份 STE 檔的 `check_ste.py --ste` 都 PASS，警告和之前相同：RSDC-Standard 4 則被動句，tw-keep-english 與 md-style 是 no-op 被拆成的 op。
  之後 `--dry-run` 一份都不列。
- 第二次執行：[[Task 32.7]] 審 scratch-rules 時，ste-custom.md 又改了兩次，加上 own、擴大 create 的意思；scratch-rules 取代原檔之後，`draft.py recheck --root .` 重檢 20 份，20 份都重記，以 0 結束；新指紋 `e12251a917f1`。
  scratch-rules 的草稿每次修改後都立刻跑了 Step 3，取代後的 scratch-rules.md 與它的中文版已記著新指紋，不在這 20 份裡。
  4 份草稿的檢查都 PASS，沒有新的 WARN，`step_3` 都已存；6 份 STE 檔的 `check_ste.py --ste` 都 PASS，警告和之前相同：RSDC-Standard 4 則被動句，tw-keep-english 與 md-style 是 no-op 被拆成的 op。
  skill-writing 的草稿由 [[Task 32.8]] 在審，重記只改了它與中文版檔頭的 `[[ste-custom]]` 那一行；之後 `--dry-run` 一份都不列。
