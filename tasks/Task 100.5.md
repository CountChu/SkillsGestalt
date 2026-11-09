# Task 100.5 - 檢查 Task 100 是否完成

**Status**：完成——9 項的主要部分都合；asd-ste Step 4 的 no、Step 7 與讀 handoff 檔的那一步，留到下次真的跑這兩個 skill 時確認。
**Raised**：2026-11-06，使用者要一個 sub task 檢查 [[Task 100]] 是否做完，例如 scratch-rules 與 report-yaml-rules 是否移除了。
**Depends on**：[[Task 100.2]]、[[Task 100.3]]、[[Task 100.4]]、[[Task 100.6]]

## 1. 背景

- [[Task 100]] 把 run 寫的資料分成兩類，[[Task 100.2]] 寫了 [run-data-rules.md](../skill-groups/common/rules/run-data-rules.md)，[[Task 100.3]] 改範本，[[Task 100.4]] 改各個 skill。
- 兩個舊檔由 [[Task 100.4]] 在改完引用之後刪掉；本 task 只檢查，不改檔。
- 檢查項目寫成下面的清單，每一項有要跑的指令與預期的結果，不另寫 script。

## 2. 結論

—

## 3. 過程

### 2026-11-06 第 1 到第 7 項的結果

**表 1：清單的結果**

| 項 | 結果 | 說明 |
| --- | --- | --- |
| 1 | 合 | `rules/` 沒有兩個舊檔 |
| 2 | 合 | 只列出 asd-ste 的 ste-custom 與 ReviewPage-RSDC（和中文版），都是說明與歷史紀錄 |
| 3 | 合 | 只剩 ste-custom（和中文版）第 45 行 merge 的 Meaning 欄；和第 2 項同類，使用者決定保留，預期結果改成允許它 |
| 4 | 合 | `publish_snapshot.py` 原本用 `tempfile` 放一份 git index，改放 `temp\publish-gestalt-index-{pid}\`、在 finally 刪掉；剩下的是 compile-skill 的隔離測試例外、建在 `temp\` 裡的 `test_hub.js`，以及規則與準則的說明文字 |
| 5 | 合 | `handoff/`、`temp/`、`checkpoints/`、`database/` 都被 git 忽略 |
| 6 | 合 | SKILL-tmp、README-tmp、run-data-rules、report-md-rules 的 STE 檢查都 PASS，parity 都是 0 failure |
| 7 | 合 | `scan_skill.py` 掃 22 個 skill：沒有缺少的標題；4 份 README 的 chinese/SKILL.md 在 [[Task 100.6]] 改過而顯示 CHANGED，讀過之後重記（`0d53e40`） |


### 2026-11-06 第 8、9 項的結果

由一個 subagent 試跑：asd-ste 用 `skill-groups/external/README.md` 在 `temp\` 的副本，gen-imp-app 只跑 `resolve_session.py`；試跑的檔都已刪掉。

- **第 8 項，asd-ste**：Run Number 是 `261106.1`。
  - Step 0 到 3 照 SKILL.md 跑完，之後停下；`run step 4` 用 `draft.py runs` 找到同一次 run，`steps` 依序有 0 到 3，再加上 4。
  - 每個 step 檔只放這一步的輸出，Step 1 與 Step 3 的資料檔也在 Checkpoint Dir 裡；`temp\` 沒有留下這次 run 的檔。
  - process record 沒有 `result`：被中斷、再用 `run step N` 接著跑的 run，原本的規則沒有給值；使用者決定一開始就寫 `result: stopped`，每一步重寫 `stopped_at`（`b377873`）。
  - Step 4 沒有走「回答 no」那一支：草稿在被 git 忽略的 `temp\`，照 SKILL.md 跳過；`result: completed` 要到 Step 7，這次也沒有跑到，改由 `save_step.py` 的小測試確認 `--last` 寫出 `completed`。
  - `save_step.py --help` 會出錯：help 裡的 `%Y` 被 argparse 當成格式字元，已修好（`fd0d937`）。
- **第 9 項，gen-imp-app**：`resolve_session.py --step 1` 給出 Run Number、Checkpoint Dir、process record 與 `handoff/gen-imp-app/{yymmdd}.{N}.md`；補上 `step_0.yaml` 之後，`--step 2` 重開同一次 run。
  讀 handoff 檔的 skill 說明它讀了哪一個，這次沒有跑到。

## 4. 要做的

從 workspace 的根目錄逐項跑，每一項記下結果；有一項不合，就在對應的 sub task 補做，再從頭跑一次。

### 舊檔與引用

1. 舊檔已刪：`ls skill-groups/common/rules/ | grep -e scratch-rules -e report-yaml-rules` 沒有輸出。
2. 沒有引用：`git grep -l -e scratch-rules -e report-yaml-rules -- . ':!tasks' ':!dashboard' ':!skill-groups/common/CHANGES.md' ':!skill-groups/archived'` 只列出 asd-ste 的 ste-custom 與 ReviewPage-RSDC（和中文版）；它們的那幾行是說明與歷史紀錄，不是連結（[[Task 100.4]]）。

### 舊做法不在了

3. `git grep -n -e 'process\.yaml' -e 'YAML checkpoint' -e 'CHECKPOINT_DIR_NAME' -- skill-groups/common ':!skill-groups/common/CHANGES.md'` 只列出 ste-custom（和中文版）merge 那一列的說明文字。
4. `git grep -n -e 'tempfile' -e 'os.tmpdir' -e 'mkdtemp' -- skill-groups/common` 沒有輸出。
5. `git check-ignore handoff/x temp/x checkpoints/x database/x` 印出四行。

### 範本與 skill 都通過檢查

6. SKILL-tmp.md、README-tmp.md、run-data-rules.md 與 report-md-rules.md：`check_ste.py` 都 PASS，`check_parity.py` 都是 0 failure。
7. [[Task 100.4]] 改過的每個 skill：check-skill 的 Template alignment 與 Dataflow 不報新的 issue。

### 實際跑一次 skill

8. 跑一次 asd-ste，確認：
   - `checkpoints\asd-ste\{yymmdd}.{N}\` 有每一步的 `step_{N}.yaml`；
   - `database\skill-runs\asd-ste\{yymmdd}.{N}.yaml` 有 `skill`、`run`、`prompt`、`result` 與每一步的 `title`、`model`、`time`，`result` 是 `completed`；
   - `temp\` 沒有這次 run 留下的檔；
   - 中斷一次再用 `run step N` 接著跑，`steps` 加上重做的步驟。
9. 跑一次寫 handoff 檔的 skill（gen-imp-app），確認 `handoff\gen-imp-app\{yymmdd}.{N}.md` 存在，讀它的 skill 說明讀了哪一個。

## 5. 驗證

- 清單的 9 項都合，結果寫在「現況」一章。
- 9 項都合之後，把 [[Task 100]] 的 Status 改成完成。

## 6. 與其他 task 的關係

- [[Task 100]]：本 task 的上層。
- [[Task 100.2]]、[[Task 100.3]]、[[Task 100.4]]：本 task 檢查它們的結果；舊檔由 [[Task 100.4]] 刪。

## 7. 知識

—

## 8. 日誌

### 2026-11-06

- 使用者決定現在結束：沒跑到的三個部分，下次真的跑 asd-ste 或 gen-imp-app 時確認；[[Task 100]] 改成完成。
- 跑第 8、9 項：修好 `save_step.py --help`；process record 一開始就寫 `result: stopped`，每一步重寫 `stopped_at`。
- 第 3 項保留 ste-custom 的說明，第 4 項 `publish_snapshot.py` 改放 `temp\`；兩項都改成合。
- 跑第 1 到第 7 項：第 3、4 項不合，見表 1；4 份 README 重記 chinese/SKILL.md。
- 第 2 項的預期結果改成允許 ste-custom 與 ReviewPage-RSDC 的說明與歷史紀錄。
- Depends on 加上 [[Task 100.6]]：每個 skill 都寫 process record 之後才算完成。
- 提出。
