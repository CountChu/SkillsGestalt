# Chores

會重複做的例行工作。
每個 chore 是 `chores/<name>.md` 一個檔案，用名稱命名，例如 `keep-english.md`。
本檔只放下面的摘要表：先讀這張表，看哪一項該做了，再只開需要的那個 chore。
chore 檔的格式與摘要表的維護方式，見 [chore-rules.md](../skill-groups/common/rules/chore-rules.md)；檢查指令見根目錄的 [AGENTS.md](../AGENTS.md)。

| Chore | Started | Title | 何時要做 | 上次執行 | Status |
| --- | --- | --- | --- | --- | --- |
| [[clone-gestalt]] | 2026-11-13 | 在新電腦上裝 SkillsGestalt | 要在一台新電腦上裝 SkillsGestalt，也要在上面改、發佈時 | 2026-11-13 | 🔁 |
| [[clean-checkpoints]] | 2026-11-12 | 清理 checkpoints\ 的舊項目 | checkpoints\ 超過 config.yaml 的 cleanCheckpoints.maxSizeGB（沒寫時 10 GB） | — | 🔁 |
| [[follow-gestalt]] | 2026-10-31 | 跟上 Gestalt 的改動 | `{skillGroups.common}/CHANGES.md` 有比上次處理的那一筆新的條目 | — | 🔁 |
| [[pull-gestalt]] | 2026-10-31 | 把 GitHub 上的新快照拿進工作分支 | 發佈之前、git fetch 看到新快照時，或使用者要求時 | 2026-11-13 | 🔁 |
| [[publish-gestalt]] | 2026-10-30 | 發佈到 GitHub | 使用者要求發佈到 GitHub 時 | 2026-11-13 | 🔁 |
| [[keep-english]] | 2026-10-18 | keep-English 稽核 | tw-keep-english.md 換了版本，和上次稽核的版本不同 | 2026-11-10 | 🔁 |
| [[rerecord-ste-custom]] | 2026-10-18 | 集中重記 ste-custom.md | 當天改過 ste-custom.md，而且當天的修改都做完了 | 2026-10-30 | 🔁 |

Status：🔁 使用中　⏸️ 暫停　⏹️ 停用。

上次執行：下面「執行紀錄」一節裡這個 chore 最新的日期；— 表示還沒做過。

## 執行紀錄

### clone-gestalt

#### 2026-11-13

- 第一次，在 DevBox（Windows 11）做，work branch 是 `devbox`：repo 已經 clone 好，本機 `main` 追蹤 `origin/main`，是快照 `9b7b872`（SkillsGestalt 2026-11-13）。
  `git switch -c devbox main`，`branch.devbox.pushRemote` 設成 `no_push`，`git push` 以 128 失敗；`config.yaml` 只改 `wikiDir`；`.venv` 用 Python 3.12 建，`pip install` 以 0 結束。
- 這台的 Git 在全系統設了 `core.autocrlf=true`，checkout 出來的檔是 CRLF，`gen_agents_md.py` 以 2 結束；這個 clone 設 `core.autocrlf=false`，重新 checkout 之後 `--check` 是 PASS。
  這一步由 [[Task 105]] 加進本 chore 的第 3 步（`ea4ada9`）。
- `publish-keywords.local.txt` 從原本那台複製過來；`check` 的掃描是 `nothing found`，因為 `devbox` 已有 `ea4ada9`，印出的是 3 個檔的改動，不是 `no change since the last release`；`incoming` 印出 `nothing to pull`。
- `external/ASD-STE100_ISSUE9.pdf` 也從原本那台複製過來；之後 `check_tasks.py` 與 `check_chores.py` 都是 PASS。
- 這台沒有 `skill-groups/external/`。`git status` 只列出 `external/`，和 [[Task 104]] 試做的那份相同；不列出 `config.yaml`、`.venv/` 與 `publish-keywords.local.txt`。

### pull-gestalt

#### 2026-11-13

- `m1` 這台：拿進 `countdell` 的 8 個快照，`04a90cc` 到 `49cf1fc`（[[Task 103]] 到 [[Task 113]]），變動 57 個檔，掃描 `nothing found`。
  舊的 `m1`（`470e461`）存成 tag `archive/m1-261113-pull`；本機 `main` 從 `593cb10` 移到 `49cf1fc`。
  rebase 停在第 7 個 commit：`m1` 開頭幾個 commit 用的 Task 104 到 107 和 `countdell` 的同號 task 撞在一起，到最後一個 commit 才改名為 114 到 117。
  經使用者同意改做 squash：`git rebase --abort`，再以 `git merge --squash 470e461` 把 18 個 commit 的淨改動做成一個 commit（`3db4156`），原本的 commit 留在那個 tag。
  衝突都兩邊留：`chore-summary.md` 2026-11-10 的兩筆發佈紀錄，`1cd81c2` 之後的 `593cb10` 在前；`CHANGES.md` 合成一節 2026-11-13 與一節 2026-11-12，`countdell` 的條目在前；`task-summary.md` 的 117 到 114 放在 113 之上。
  新快照改用 `gen_config.py`：建了本機的 `config.local.yaml`（`wikiDir` 照舊、`workBranch: m1`），重新產生的 `config.yaml` 只多了註解與 `workBranches`、`workBranch`。
  `gen_config.py --check`、`check_tasks.py` 與 `check_chores.py` 都是 PASS，`incoming` 印出 `nothing to pull`。
- 在 DevBox 的 `devbox` 做：拿進 `countdell` 發佈的快照 `2f07db8`（SkillsGestalt 2026-11-13），變動 1 個檔，是 `chore-summary.md` 的執行紀錄；作者與 committer 是 CountChu，`incoming` 的掃描是 `nothing found`。
  經使用者同意，舊的 `devbox`（`44a3890`）存成 tag `archive/devbox-261113-pull`；本機 `main` 從 `5e7a102` 移到 `2f07db8`；`devbox` 的 2 個 commit rebase 上去，沒有衝突，成為 `1b10a06` 與 `fd9a3e7`。
  `### publish-gestalt` 的 2026-11-13 自動合併：`devbox` 的 2 筆在上面，`countdell` 發佈 `9b7b872` 那 1 筆在下面。
  `git diff main devbox` 只有這次與第二次發佈的執行紀錄；這個 clone 的 `external/` 不在 git。`gen_agents_md.py` 印出 unchanged，`check_tasks.py` 與 `check_chores.py` 都是 PASS，`incoming` 印出 `nothing to pull`。
- 在 `countdell` 的 clone 做：拿進 DevBox 的 `devbox` 發佈的兩個快照 `7f62c8a`（[[Task 105]]）與 `5e7a102`（[[Task 106]]、[[Task 107]]：commit 訊息不寫 `Co-Authored-By`），變動 10 個檔，作者與 committer 是 CountChu，`incoming` 的掃描是 `nothing found`。
  經使用者同意，舊的 `countdell`（`1a26674`）存成 tag `archive/countdell-261113-pull`；本機 `main` 從 `9b7b872` 移到 `5e7a102`；`countdell` 的 2 個 commit rebase 上去，成為 `690e978` 與 `cd8adc8`。
- 衝突：`dashboard/chore-summary.md` 的 `### publish-gestalt` 兩邊都加了 2026-11-13 的紀錄；照使用者的決定兩邊都留，`devbox` 那 2 筆放上面，`countdell` 發佈 `9b7b872` 那 1 筆放下面。
- `gen_agents_md.py --check`、`check_tasks.py` 與 `check_chores.py` 都是 PASS；這個 clone 沒有設 `core.autocrlf`，`git ls-files --eol` 是 `i/lf w/lf`，所以 [[Task 105]] 的修正這裡不需要。
  從這次起，這個 clone 的 commit 也不寫 `Co-Authored-By`。

#### 2026-11-10

- 在公開 repo 的 clone 上做，work branch 是 `countdell`：拿進 `m1` 發佈的快照 `1cd81c2`（SkillsGestalt 2026-11-10），變動 133 個檔，作者與 committer 是 CountChu，`incoming` 的掃描是 `nothing found`。
  經使用者同意，舊的 `countdell`（`9c168fb`）存成 tag `archive/countdell-261110-pull`；本機 `main` 從 `8f47eda` 移到 `1cd81c2`；`countdell` 的 2 個 commit rebase 上去，沒有衝突，成為 `6e23485` 與 `5e8b1b9`，所以上面 2026-11-09 那筆的 `ba9039a` 現在只在這個 tag。
  這個 clone 沒有不公開的路徑在 git 裡，`git diff main countdell` 只有 2026-11-09 第二次發佈的紀錄；`gen_agents_md.py` 印出 unchanged，`check_tasks.py` 與 `check_chores.py` 都是 PASS。
  新快照把 tw-keep-english.md 換成 261110，所以 [[keep-english]] 該做了。
- 在 `countdell` 的第二次：拿進 `m1` 發佈的快照 `593cb10`（[[Task 101]]：Dropbox 不同步 `.git`，兩個 chore 最後加上 bundle 備份），變動 5 個檔，作者與 committer 是 CountChu，`incoming` 的掃描是 `nothing found`。
  經使用者同意，舊的 `countdell`（`2896027`）存成 tag `archive/countdell-261110-pull`；這個 tag 原本指的 `9c168fb` 沒有別的 ref，所以另存成 `archive/countdell-261110-pull-1`，和 `archive/countdell-261109-1` 的做法相同。
  本機 `main` 從 `94db4c4` 移到 `593cb10`；`countdell` 的 2 個 commit rebase 上去，沒有衝突，成為 `08fe78b` 與 `ad6b6d9`。
  `gen_agents_md.py --check`、`check_tasks.py` 與 `check_chores.py` 都是 PASS；repo 在 2026-11-10 從 OneDrive 搬到 `WorkArea\Innovation`，不在 Dropbox，bundle 仍照新步驟做在 `..\SkillsGestalt.bundle`。
- 拿進 `countdell` 發佈的兩個快照 `bb7eca1` 與 `8f47eda`（SkillsGestalt 2026-11-09）：變動 137 個檔，作者與 committer 是 CountChu，`incoming` 的掃描是 `nothing found`。
  經使用者同意，舊的 `m1`（`a04f0d1`）存成 tag `archive/m1-261110-pull`；本機 `main` 從 `1b41f68` 移到 `8f47eda`；`m1` 的 157 個 commit rebase 上去。
  開始之前，經使用者同意還原 `tasks/Task 97.md` 在 2026-11-06 只補空白的表格對齊，並移除 `.git/rebase-merge`，它是 2026-10-31 留下的空目錄。
- 衝突：`dashboard/chore-summary.md` 與 `CHANGES.md` 兩邊都留，照日期排；`tw-keep-english.md` 與中文版的 Technical words 取聯集，版本改成 261110，所以 [[keep-english]] 該做了。
  `task-rules.md` 與中文版的 Technical words 取聯集，`m1` 新加的 topic 規則照八章寫成 `7. 知識` 與 `8. 日誌`。
- 新快照把 task 改成八章：只在 `m1` 上的 13 份 Task 100 照 CHANGES.md 改好，`2. 結論` 寫 `—`（`72f88dc`）。
- `git diff main m1` 仍有 `external/` 與 `skill-groups/external/`；`gen_agents_md.py --check` 要用 `.venv` 的 python，它與 `check_tasks.py`、`check_chores.py` 都是 PASS。
- 第二次：`countdell` 又發佈了只有執行紀錄的 `b080dc7`；照使用者的決定只拿進來、不發佈，免得兩台互相發佈只有紀錄的快照。
  開始前發現 `.git/rebase-merge` 又出現：內容是早上那次 rebase 停在 128/157 時的狀態，那次 rebase 早已做完，應是 Dropbox 放回的舊副本；經使用者同意搬到 scratchpad，沒有執行 `git rebase --abort`，因為它會把 `m1` 拉回 `a04f0d1`。
  舊的 `m1`（`21c88b7`）存成 tag `archive/m1-261110-pull-2`；本機 `main` 從 `1cd81c2` 移到 `b080dc7`；`m1` 的 2 個 commit rebase 上去，沒有衝突。
  `git diff main m1` 仍有 `external/` 與 `skill-groups/external/`；`gen_agents_md.py --check`、`check_tasks.py` 與 `check_chores.py` 都是 PASS，`incoming` 印出 `nothing to pull`。
- 第三次：拿進 `countdell` 的 `94db4c4`（[[Task 102]]：`publish_snapshot.py` 可以由 `config.yaml` 的 `publish:` 設定），變動 9 個檔，掃描 `nothing found`。
  舊的 `m1`（`62e1082`）存成 tag `archive/m1-261110-pull-3`；本機 `main` 從 `b080dc7` 移到 `94db4c4`；`m1` 的 4 個 commit rebase 上去。
  衝突：`chore-summary.md` 的 `### publish-gestalt` 兩邊在同一天的段落各加一筆，兩筆都留，`b080dc7` 在前；`task-summary.md` 兩列都留，Task 102 在前。
  `publish-gestalt.md` 與 `pull-gestalt.md` 自動合併，和 `94db4c4` 相比只多了 [[Task 101]] 的 bundle 那一步。
  `gen_agents_md.py --check`、`check_tasks.py` 與 `check_chores.py` 都是 PASS，`incoming` 印出 `nothing to pull`。

#### 2026-11-02

- 在公開 repo 的 clone 上做，work branch 是 `countdell`：`incoming` 列出新快照 `1b41f68`（SkillsGestalt 2026-11-02），變動 295 個檔，作者與 committer 是 CountChu，掃描 `nothing found`。
  經使用者同意，舊的 `countdell`（`7d0dcd9`）存成 tag `archive/countdell-261102-pull`；本機 `main` 從 `65c25e5` 移到 `1b41f68`；`countdell` 的 2 個 commit rebase 上去，沒有衝突。
- rebase 過來的 4765af0 發佈紀錄自成一個 `#### 2026-10-31`，併進 `### publish-gestalt` 同一天的段落，放在 `65c25e5` 與 `93b4e1e` 兩筆之間，並註明它後來換成 `4d2c5db`。
- 新快照把 `.github/` 改名為 `skill-groups/`：本機的 `config.yaml` 的 `skillGroups` 跟著改；`gen_agents_md.py` 重新產生 AGENTS.md 與 CLAUDE.md，沒有變動。
  這個 clone 的 `external/` 不在 git，所以 `git diff main countdell` 沒有不公開的路徑。
- `incoming` 印出 `nothing to pull`；`gen_agents_md.py --check`、`check_tasks.py` 與 `check_chores.py` 都是 PASS。

#### 2026-10-31

- 第一次，在 [[Task 89]] 照手動步驟做：GitHub 的 `main` 有另一台電腦從 `countdell` 發佈的 `4765af0`，作者與 committer 是工作的身分。
  經使用者同意，在本機做出同樣檔案、訊息與時間、作者改成 CountChu 的 `4d2c5db`，以 `--force-with-lease` 換掉 GitHub 上的 `4765af0`。
- 本機 `main` 從 `93b4e1e` 移到 `4d2c5db`；舊的 `m1`（`e0365fc`）存成 tag `archive/m1-261031-pull`；`m1` 的 3 個 commit rebase 到 `4d2c5db` 上，沒有衝突；`external/` 與 `skill-groups/external/` 仍在。
- 新快照把 task 改成七章：只在 `m1` 上的 [[Task 89]] 插入 `6. 知識`；CLAUDE.md 重新產生。

### publish-gestalt

#### 2026-11-13

- 第四次發佈：以 `devbox` 的 `828652e` 做出快照 `b16b300`，接在 `8e9e9d1` 之後，推到 `main`；變動 39 個檔，是 [[Task 110]]、[[Task 111]]、[[Task 112]] 與第三次發佈的執行紀錄。
  先做 [[pull-gestalt]]：`incoming` 印出 `nothing to pull`；`check` 與 `publish` 的掃描都是 `nothing found`。
  發佈前把 `c39a780` 存成 tag `archive/devbox-261113-3`，因為下面一筆引用它；發佈後 `archive/devbox-261113` 從 `c39a780` 移到 `828652e`，`devbox` 從 `b16b300` 重新開始（`5381a4e`）。
  用 git 確認：`git ls-remote` 的 `main` 是 `b16b300`；`origin/main` 的 tree 沒有排除的路徑，有 `AGENTS.shared.md` 與 `config.shared.yaml`；快照訊息沒有 `Co-Authored-By` trailer，只有摘要裡說這條規則的一句。
  別台下次 [[pull-gestalt]] 時，`config.local.yaml` 要有 `wikiDir` 與自己的 `workBranch`，不然 `gen_config.py` 以 `2` 結束（[[Task 111]]、[[Task 112]]）。
- 第三次發佈：以 `devbox` 的 `c39a780` 做出快照 `8e9e9d1`，接在 `countdell` 發佈的 `2f07db8` 之後，推到 `main`；變動 28 個檔，是 [[Task 108]]、[[Task 109]] 與這台第二次發佈、pull 的執行紀錄。
  先做 [[pull-gestalt]]：`incoming` 印出 `nothing to pull`。第一次 `check` 的掃描找到 [[Task 109]] 裡描述掃描結果的那一行有使用者目錄的路徑，改掉並 commit（`c39a780`）之後，`check` 與 `publish` 都是 `nothing found`。
  `devbox` 跟著從 `8e9e9d1` 重新開始（`029ccba`）；tag `archive/devbox-261113` 從 `31e193e` 移到 `c39a780`。發佈後把 `31e193e` 存成 tag `archive/devbox-261113-2`，因為下面一筆與 `fd9a3e7` 的訊息引用它。
  用 git 確認：`git ls-remote` 的 `main` 是 `8e9e9d1`；`origin/main` 的 tree 沒有排除的路徑，有 `config-tmp.yaml`；快照沒有 `Co-Authored-By`。
  別台下次 [[pull-gestalt]] 第 9 步要先照 [[clone-gestalt]] 第 5 步寫自己的 `config.local.yaml`（[[Task 109]]）。
- 第二次發佈：以 `devbox` 的 `31e193e` 做出快照 `5e7a102`，接在 `7f62c8a` 之後，推到 `main`；變動 8 個檔，是 [[Task 106]]、[[Task 107]] 與第一次發佈的執行紀錄。
  先做 [[pull-gestalt]]：`git fetch` 之後 `incoming` 印出 `nothing to pull`；`check` 與 `publish` 的掃描都是 `nothing found`。照 [[Task 106]] 改過的第 4 步，不加 `--co-author`。
  `devbox` 跟著從 `5e7a102` 重新開始（`dd61196`）；同一天第二次發佈，tag `archive/devbox-261113` 從 `a098a95` 移到 `31e193e`。發佈前先把 `a098a95` 存成 tag `archive/devbox-261113-1`，因為 [[clone-gestalt]] 的執行紀錄引用 `ea4ada9`。
  用 git 確認：`git ls-remote` 的 `main` 是 `5e7a102`，只比 `7f62c8a` 多 1 個 commit，作者是 `CountChu`；`origin/main` 的 tree 沒有排除的路徑；`7f62c8a` 之後的 commit 都沒有 `Co-Authored-By`。
- 第一次從 DevBox 的 clone 發佈，work branch 是 `devbox`：以 `devbox` 的 `a098a95` 做出快照 `7f62c8a`（SkillsGestalt 2026-11-13），接在 `9b7b872` 之後，推到 `main`；變動 4 個檔，是 [[Task 105]] 與 [[clone-gestalt]] 第一次的執行紀錄。
  先做 [[pull-gestalt]]：`git fetch` 之後 `incoming` 印出 `nothing to pull`；`check` 與 `publish` 的掃描都是 `nothing found`，發佈前自己查 diff，也沒有主機名稱、帳號名稱或公司的雲端資料夾名稱。
  這台第一次 push，Git Credential Manager 要求登入 GitHub，使用者登入之後程式自己推上去了。
  `devbox` 跟著從 `7f62c8a` 重新開始（`ba712f7`），舊的在 tag `archive/devbox-261113`。
  這台的 `gh` 沒有登入，改用 git 確認：`git ls-remote` 的 `main` 是 `7f62c8a`，只比 `9b7b872` 多 1 個 commit，作者是 `CountChu`；`origin/main` 的 tree 沒有排除的路徑。
- 第一次推上去的快照是 `4235a83`，訊息有 `Co-Authored-By`，因為照第 4 步加了 `--co-author`；使用者要求拿掉。
  經使用者同意，做出同樣 tree、parent、作者與時間、只拿掉這一行的 `7f62c8a`，以 `--force-with-lease` 換掉 GitHub 上的 `4235a83`；`devbox` 重新開始的 commit 也照樣重做（`a35eff1` 換成 `ba712f7`）。
  別台若在這之間拿進了 `4235a83`，下次 [[pull-gestalt]] 的 `incoming` 會印出 `diverged`。以後發佈不加 `--co-author`。
- 以 `countdell` 的 `7c80e47` 做出快照 `9b7b872`（SkillsGestalt 2026-11-13），接在 `04a90cc` 之後，推到 `main`；變動 5 個檔，是 [[Task 104]]（新的 chore [[clone-gestalt]]，pull-gestalt 指向它）與上次發佈的執行紀錄。
  先做 [[pull-gestalt]]：本機的 `main` 和 `origin/main` 都是 `04a90cc`，`nothing to pull`；`check` 與 `publish` 的掃描都是 `nothing found`。
  沒有給 `--co-author`：使用者不要 commit 訊息有 `Co-Authored-By`。
  `countdell` 跟著從 `9b7b872` 重新開始（`94e838b`），舊的在 tag `archive/countdell-261113`。
  這台沒有 `gh`，改用 git 確認：`git ls-remote` 的 `main` 是 `9b7b872`，作者是 `CountChu`；`origin/main` 的 tree 沒有排除的路徑。

#### 2026-11-12

- 以 `countdell` 的 `00dd814` 做出快照 `04a90cc`（SkillsGestalt 2026-11-12），接在 `593cb10` 之後，推到 `main`；變動 9 個檔，是 [[Task 103]]（skill 與 chore `clean-checkpoints`）。
  本機的 `main` 和 `origin/main` 都是 `593cb10`，不必先做 [[pull-gestalt]]；`check` 與 `publish` 的掃描都是 `nothing found`。
  發佈前自己查 diff，發現 2026-11-10 [[pull-gestalt]] 的執行紀錄寫了公司的雲端資料夾名稱，掃描沒抓到；改掉之後才發佈（`00dd814`）。
  `countdell` 跟著從 `04a90cc` 重新開始（`492602c`），舊的在 tag `archive/countdell-261112`。
  這台沒有 `gh`，改用 git 確認：`git ls-remote` 的 `main` 是 `04a90cc`，只比 `593cb10` 多 1 個 commit；`origin/main` 的 tree 沒有排除的路徑。

#### 2026-11-10

- 第二次（`m1`）：先做 [[pull-gestalt]]，拿進 `countdell` 的 `94db4c4`；之後以 `m1` 的 `0def18d` 做出快照 `593cb10`，接在 `94db4c4` 之後，推到 `main`；變動 5 個檔、4 個 commit，主要是 [[Task 101]]。
  `check` 與 `publish` 的掃描都是 `nothing found`；訊息有兩段英文摘要，照使用者的決定不加 Co-Authored-By。
  `m1` 跟著從 `593cb10` 重新開始（`483b85e`），`archive/m1-261110` 從 `dda8233` 改指 `0def18d`；經使用者同意，早上的歷史另存成 tag `archive/m1-261110-1`（指向 `dda8233`）。
  GitHub 上確認：`main` 有 13 個 commit，最新的是 `593cb10`，tree 和本機做出的 `619f93f` 相同，299 個檔裡沒有排除的路徑。
- 第二次發佈：以 `countdell` 的 `015b0f6` 做出快照 `94db4c4`，接在 `b080dc7` 之後，推到 `main`；變動 9 個檔，是 [[Task 102]]（`publish_snapshot.py` 可以由 `publish:` 設定、`--orphan`）與 [[keep-english]] 261110 稽核。
  先做 [[pull-gestalt]]：本機的 `main` 和 `origin/main` 都是 `b080dc7`，`nothing to pull`；`check` 與 `publish` 的掃描都是 `nothing found`。
  `countdell` 跟著從 `94db4c4` 重新開始（`de150e1`）；同一天第二次發佈，tag `archive/countdell-261110` 從 `65a42e4` 移到 `015b0f6`。
  這台沒有 `gh`，改用 git 確認：`git ls-remote` 的 `main` 是 `94db4c4`，只比 `b080dc7` 多 1 個 commit，作者是 `CountChu`；`origin/main` 的 tree 沒有排除的路徑。
  m1 的 Task 101 還沒發佈，所以快照有 Task 102、沒有 Task 101，`check_tasks.py` 在快照上會報 101 號沒有檔案，直到 m1 發佈。
- 以 `countdell` 的 `65a42e4` 做出快照 `b080dc7`，接在 `1cd81c2` 之後，推到 `main`；變動 1 個檔，是 2026-11-09 第二次發佈與本日 [[pull-gestalt]] 的執行紀錄。
  先做 [[pull-gestalt]]，拿進 `m1` 發佈的 `1cd81c2`；`check` 與 `publish` 的掃描都是 `nothing found`，程式自己推上去了。
  `countdell` 跟著從 `b080dc7` 重新開始（`0a7cf29`），舊的在 tag `archive/countdell-261110`。
  GitHub 上確認：`main` 是 `b080dc7`，只比 `1cd81c2` 多 1 個 commit，沒有排除的路徑，也沒有 `skill-groups/archived/`。
  [[keep-english]] 261110 還沒做，使用者決定先發佈。
- 先做 [[pull-gestalt]]：GitHub 上有 `countdell` 的 `bb7eca1` 與 `8f47eda`，拿進來之後 `m1` 是 `dda8233`。
- 以 `m1` 的 `dda8233` 做出快照 `1cd81c2`，接在 `8f47eda` 之後，推到 `main`；變動 133 個檔，修改 87、新增 15、刪除 31，共 158 個 commit。
  主要是 [[Task 100]] 的 run data：run-data-rules.md 取代 scratch-rules 與 report-yaml-rules，6 個很少用的 skill 搬到 `skill-groups/archived`；其餘是 script 從執行所在的 workspace 找根目錄、task-rules 的 Obsidian URI，以及 keep-English list 261110。
  `check` 與 `publish` 的掃描都是 `nothing found`，快照的作者與 committer 是 `publish_snapshot.py` 的 `IDENTITY`；訊息有五段英文摘要，照使用者的決定不加 Co-Authored-By。
  `m1` 跟著從 `1cd81c2` 重新開始（`871ac1c`），舊的在 tag `archive/m1-261110`；GitHub 上確認：`main` 有 10 個 commit，最新的是 `1cd81c2`，tree 和本機做出的 `6415266` 相同，297 個檔裡沒有排除的路徑。

#### 2026-11-09

- 第二次發佈：以 `countdell` 的 `822e561` 做出快照 `8f47eda`，接在 `bb7eca1` 之後，推到 `main`；變動 2 個檔，是第一次發佈與 [[keep-english]] 261108 稽核的執行紀錄。
  先做 [[pull-gestalt]]：本機的 `main` 和 `origin/main` 都是 `bb7eca1`；`check` 與 `publish` 的掃描都是 `nothing found`。
  這次程式自己推上去了，不必由使用者推。
  `countdell` 跟著從 `8f47eda` 重新開始（`ba9039a`），`archive/countdell-261109` 從 `e7e9684` 改指 `822e561`；經使用者同意，早上的歷史另存成 tag `archive/countdell-261109-1`（指向 `e7e9684`），因為下面那筆紀錄引用它。
  GitHub 上確認：`main` 是 `8f47eda`，只比 `bb7eca1` 多 1 個 commit，沒有排除的路徑。
- 以 `countdell` 的 `e7e9684` 做出快照 `bb7eca1`，接在 `1b41f68` 之後；變動 136 個檔，其中 127 個是 task 改成八章，來自 5 個 commit：task 的八章與 2. 結論、結論用表格、伺服器上的項目連到它的 URL，以及 tw-keep-english.md 261108。
  先做 [[pull-gestalt]]：本機的 `main` 和 `origin/main` 都是 `1b41f68`，沒有東西要拿進來；`check` 與 `publish` 的掃描都是 `nothing found`，快照的作者與 committer 是 `publish_snapshot.py` 的 `IDENTITY`。
  程式推送失敗：這個 clone 仍沒有 GitHub 的帳號資料，由使用者自己執行 `git push origin main:main`；之後用程式的 `restart_work` 讓 `countdell` 從 `bb7eca1` 重新開始（`4feaeaf`），舊的在 tag `archive/countdell-261109`。
  GitHub 上確認：`main` 是 `bb7eca1`，只比 `1b41f68` 多 1 個 commit，沒有排除的路徑。

#### 2026-11-02

- 以 `m1` 的 `2a2ff3d` 做出快照 `1b41f68`，接在 `65c25e5` 之後，推到 `main`；變動 295 個檔，改名 159、修改 110、新增 23、刪除 3，共 45 個 commit。
  主要是 [[Task 97]] 把 `.github` 搬到 `skill-groups`、把規則搬進 `AGENTS.md`；其餘來自 [[Task 18.8]]、[[Task 27]]、[[Task 41]]、[[Task 41.1]]、[[Task 92]] 到 [[Task 99]]、兩個 task-rules 的修改，以及上次發佈的執行紀錄。
  先做 [[pull-gestalt]]：`incoming` 印出 `nothing to pull`；`check` 與 `publish` 的掃描都是 `nothing found`，快照的作者與 committer 是 `publish_snapshot.py` 的 `IDENTITY`。
  快照的訊息有六段英文摘要；照使用者的決定，這次不加 Co-Authored-By。
  `m1` 跟著從 `1b41f68` 重新開始（`3507e58`），舊的在 tag `archive/m1-261102`；GitHub 上確認：`main` 有 7 個 commit，最新的是 `1b41f68`，tree 和本機做出的 `7f8582e` 相同，313 個檔裡沒有排除的路徑，也沒有舊的 `.github/`。

#### 2026-10-31

- 第二次發佈：以 `m1` 的 `3933273` 做出快照 `65c25e5`，接在 `4d2c5db` 之後，推到 `main`；變動 18 個檔，新增 4、改名 1、修改 13，來自 [[Task 89]]、[[Task 90]]、[[Task 91]]，以及早上那次發佈的執行紀錄。
  先做 [[pull-gestalt]]：`incoming` 印出 `nothing to pull`；`check` 與 `publish` 的掃描都是 `nothing found`，快照的作者與 committer 是 `publish_snapshot.py` 的 `IDENTITY`。
  發佈之前，經使用者同意，把早上的歷史另存成 tag `archive/m1-261031-1`（指向 `b2e967f`）：`archive/m1-261031` 一改指，就有 34 個 commit 沒有任何 ref，其中 14 個 hash 被文件引用，11 個在 CHANGES.md；以後的做法由 [[Task 92]] 決定。
  `m1` 跟著從 `65c25e5` 重新開始（`e1db93c`），`archive/m1-261031` 改指 `3933273`；GitHub 上確認：`main` 有 6 個 commit，最新的是 `65c25e5`，tree 和本機做出的 `450e498` 相同，293 個檔裡沒有排除的路徑。
- 第一次從公開 repo 的 clone 發佈，work branch 是 `countdell`，不是 `m1`：以 `countdell` 的 `96b7534` 做出快照 `4765af0`，接在 `93b4e1e` 之後；變動 124 個檔，其中 108 個是 task 加上「6. 知識」這一章。
  快照 commit 第一次帶有改動的摘要（`--summary-file`），摘要寫的是 10 個 commit 做的事。
  程式推送失敗：這個 clone 沒有 GitHub 的帳號資料，由使用者自己執行 `git push origin main:main`；之後用程式的 `restart_work` 讓 `countdell` 從 `4765af0` 重新開始（`93357d9`），舊的在 tag `archive/countdell-261031`。
  GitHub 上確認：`main` 是 `4765af0`，只比 `93b4e1e` 多 1 個 commit，沒有排除的路徑。
  它的作者是工作的身分，之後由 [[pull-gestalt]] 換成 `4d2c5db`。
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

#### 2026-11-10

- 清單 261110 版（261108 與 261106 合併，有 working data）：38 對中英對照，19 份中文版有 189 行警告；working data 的「工作資料」沒有找到任何一筆。
- 在 `countdell` 的 clone 稽核，和 2026-11-09 的 261108 版報告比：2 筆新出現，2 筆消失。
  - 新出現：checking-criteria-tw.md 與 gen-skill `SKILL-tw.md` 的 template「範本」各 1 行。
  - 消失：gen-rsdc-skill `SKILL-tw.md` 的「標準化的 skill 叫用方式」，imp-app `SKILL-tw.md` 的「標準的 skill 呼叫」。
  - 行數改變：imp-home `SKILL-tw.md` 的「步驟」24 → 31 行，check-skill `SKILL-tw.md` 的「腳本」22 → 25 行，imp-app `SKILL-tw.md` 的「腳本」10 → 9 行，asd-ste `SKILL-tw.md` 的「標準形式的 skill 呼叫」2 → 1 行；這些和 `m1` 2026-11-06 那筆列出的相同，是 `1cd81c2` 帶進來的。
- 最多的 3 種譯法：script 的「腳本」131 行（14 份）、step 的「步驟」31 行（1 份）、identifier 的「識別碼」9 行（7 份）。
- 「英文也寫中文」1 行，不算進警告：MermaidView-RSDC-tw.md 的「角色」，和上次相同。
- 只列出，沒有改中文版；要改的仍記在 [[Task 73]]。
- 報告：`checkpoints/chores/keep-english/2026-11-10-261110.txt`，只在 `countdell` 的 clone。

#### 2026-11-09

- 清單 261108 版（加上 bug、build、feature、pipeline、pull request、server、test case、work item）：39 對中英對照，19 份中文版有 182 行警告。
- 在 `countdell` 的 clone 稽核：這裡沒有 `checkpoints/`，程式印出 no earlier report to compare with，所以和 2026-10-30 那筆執行紀錄的數字比：多 1 份中文版，少 4 行警告；新加的 term 沒有找到任何一筆。
- 最多的 3 種譯法：script 的「腳本」129 行（14 份），上次 133 行（15 份）；step 的「步驟」24 行（1 份），和上次相同；identifier 的「識別碼」9 行（7 份），上次 7 行（5 份）。
- 「英文也寫中文」1 行，不算進警告：MermaidView-RSDC-tw.md 的「角色」，和上次相同。
- 只列出，沒有改中文版；要改的仍記在 [[Task 73]]。
- 報告：`checkpoints/chores/keep-english/2026-11-09-261108.txt`，只在 `countdell` 的 clone。

#### 2026-11-06

- 清單 261106 版（[[Task 100.11]] 加上 working data）：38 對中英對照，19 份中文版有 191 行警告；working data 的「工作資料」沒有找到任何一筆。
- 和 2026-10-30 的 261030 版相比，報告列出 37 筆新出現、37 筆消失，大多是 `.github/common/` 搬到 `skill-groups/common/` 的路徑；照新路徑對照，實際的差異是：
  - 增加：imp-home `SKILL-tw.md` 的「步驟」24 → 31 行，check-skill `SKILL-tw.md` 的「腳本」22 → 25 行，checking-criteria-tw.md 的「腳本」13 → 14 行與「範本」1 行，gen-skill `SKILL-tw.md` 的「範本」1 行，ReviewPage-RSDC-tw.md 與 MermaidView-RSDC-tw.md 的「識別碼」各 1 行。
  - 減少：MermaidView-RSDC-tw.md 的「腳本」「範本」「術語」，gen-rsdc-skill `SKILL-tw.md` 的「標準化的 skill 叫用方式」，asd-ste `SKILL-tw.md` 的「標準形式的 skill 呼叫」2 → 1 行。
- 最多的 3 種譯法：script 的「腳本」132 行（14 份）、step 的「步驟」31 行（1 份）、identifier 的「識別碼」9 行（7 份）。
- 「英文也寫中文」1 行，不算進警告，和上次相同。
- 只列出，沒有改中文版；要改的仍記在 [[Task 73]]。
- 報告：`checkpoints/chores/keep-english/2026-11-06-261106.txt`。

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
