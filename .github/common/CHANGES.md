# CHANGES

SkillsGestalt 的 `common` skill group 裡，會影響 Forge 的改動。
「會影響」是指：Forge 必須做點什麼，或它的檢查會從 PASS 變成 FAIL；只改措辭、不改做法的改動不記。
每一筆寫明改了什麼、commit，以及 Forge 要做什麼；新的日期在前。
Forge 以 chore [follow-gestalt](../../chores/follow-gestalt.md) 處理這裡的條目：它的執行紀錄記下處理到哪一筆，比那一筆新的就該做了。

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
- **CLAUDE.md 由模板產生**（`2815afe`、`e9ed765`）：CLAUDE.md 由 [CLAUDE-tmp.md](templates/CLAUDE-tmp.md) 與 agency 根目錄的 `CLAUDE-local.md` 經 `gen_claude_md.py` 產生；`CLAUDE-local.md` 裡一行 `{CLAUDE-local}` 把它分成放在開頭與結尾的兩段；連到 common 的連結是相對路徑。
  取代同一天的 `agency-rules.md` 與 `check_claude_md.py`（`e50a302`、`188afa9`），兩者已刪。
  Forge 要做：把只有自己的規則搬到 `CLAUDE-local.md`，執行 `gen_claude_md.py`，不再手改 CLAUDE.md。
