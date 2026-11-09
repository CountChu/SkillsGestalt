# Task 100.4 - 各個 skill 照 run-data-rules 改

**Status**：完成——13 個 skill 照 run-data-rules 改好，scratch-rules 與 report-yaml-rules 刪掉；其餘 9 個 skill 的 process record 在 [[Task 100.6]]。
**Raised**：2026-11-06，[[Task 100]] 盤點出各個 skill 寫資料的地方，要照新的規則與範本改。
**Depends on**：[[Task 100.2]]、[[Task 100.3]]

## 1. 背景

- [[Task 100]] 的表 4 到表 7 是盤點的結果；表 7 列出每個 skill 交接資料的方式與寫到規定位置以外的地方。
- 封存到 `skill-groups/archived/` 的 skill 不改（[[Task 100.1]]）。

## 2. 結論

—

## 3. 過程

### 2026-11-06 改好之後

每個 skill 由一個 subagent 照同一份說明改，只改自己的目錄；檢查與 commit 在本 session 做，一個 skill 一個 commit。

**表 1：改好的 skill**

| Skill | 改了什麼 | Commit |
| --- | --- | --- |
| set-tag-status | Run Number、step 檔、process record；Step 0 從 config.yaml 讀 `wikiDir`；報告的表頭加上 Checkpoint 欄 | `041a6d0` |
| write-topic | Run Number、step 檔、process record；修好先顯示後存檔的順序；topic 檔不是 MD report，不再引用 report-md-rules | `597b737` |
| check-md-deps | Run Number 與 process record，沒有 step 檔 | `cfbe14f` |
| reformat-md | `#v1` 副本改放 Checkpoint Dir；Run Number、step 檔、process record | `3d7e398` |
| gen-skill | 自己的 process record | `4ab500b` |
| gen-rsdc-app | 交回的結果寫進 `handoff\gen-rsdc-app\{yymmdd}.{N}.md`；Run Number、step 檔、process record | `015bcbf` |
| compile-skill | Run Number 與 process record；驗證的試跑留在系統的暫存目錄，是隔離測試的例外 | `b0b6399` |
| check-skill | 自己的 process record；兩支 script 的相對路徑從根目錄算，接受兩種分隔符號；5.7 寫明隔離測試的例外 | `aa81524` |
| gen-imp-app | `resolve_session.py` 算 Run Number；prompt log 改成 handoff 檔；讀 gen-rsdc-app 的 handoff 檔 | `c3900e2` |
| imp-home | Run Number、step 檔、process record；`test_hub.js` 改在 `temp\` 跑；`setup_target.py` 從 config.yaml 取得根目錄 | `b7ea40c` |
| gen-rsdc-skill | `step_N.yaml` 與新的目錄名稱；`run step N` 只更新它跑過的步驟在 MD report 中的段落 | `8fd9e83`、`20bce11` |
| imp-app | `resolve_session.py` 從 config.yaml 取得根目錄並算 Run Number；測試與部署的輸出檔帶序號；讀 gen-rsdc-app 的 handoff 檔 | `2b39ca4` |
| asd-ste | 每次 run 一個 Checkpoint Dir；`save_step.py` 寫 step 檔與 process record；findings JSON 不再複製進 YAML；`recheck` 在 `temp\` 跑，寫進它重檢的那次 run；review 的狀態從同一份原檔較早的那次 run 讀 | `02e6e68` |

- **run-data-rules.md 加了一條例外**（`f9d338a`）：不可以找到 workspace 檔案的測試，可以用系統的暫存目錄，停下時移除。
- **兩個舊規則檔刪掉**：剩下提到它們的只有 ste-custom 的 Meaning 與 Why 欄，以及 ReviewPage-RSDC 第 548 行的驗證紀錄；這些是說明與歷史，不是連結，改了會改到 ste-custom 的指紋。
- **Home-RSDC 驗證表**寫著「在暫存目錄裡的 hub 複本」，那是 2026-11-02 驗證時的紀錄，不改。

### 留給使用者決定的

- set-tag-status 當天的報告一直往後加，和 report-md-rules「檔案已存在時清掉表頭之後的內容」不同；同一天的報告，Checkpoint 欄只指向最後一次 run。
- write-topic 加了 step 檔；只要 process record 的話可以拿掉。
- gen-rsdc-app 照停止規則只顯示兩個路徑，不再在對話裡印出結果的表格。
- reformat-md、gen-rsdc-skill、imp-app、imp-home、gen-imp-app、gen-rsdc-app 都沒有 README.md，skill-writing.md 規定每個 skill 都要有。
- reformat-md 的指令仍寫 `python3`，沒有改成 `{python}`。
- check-skill 的 `scan_skill.py` 找不到 config.yaml 時仍從目前目錄往上找；facts file 仍以 `{yymmdd-hh}` 命名。
- imp-app 在 Node v22 上，`node --test tests` 把 `tests` 當成模組，測試會失敗；這是原本就有的問題。
- asd-ste 的 process record 要到 `--stopped` 或 Step 7 的 `--last` 才寫 `result`；只跑 `run step N`（N 小於 7）的那次 run 沒有 `result`。

### 2026-11-06 要改的 skill

- **asd-ste**：Checkpoint Dir 從 `{parent}-{name}` 改成 `{yymmdd}.{N}`；process.yaml 分成 step_N.yaml 與 `database\skill-runs\`；改 `save_step.py`；`draft.py recheck` 的暫存檔改放 `temp\`；Checkpoint Dir 不再跟著目前目錄；另有 README.md、ReviewPage-RSDC.md 與 ste-custom.md 引用舊規則檔。
- **gen-rsdc-skill**：已經每一步一個 `step-N.yaml`，改成 `step_N.yaml` 與新的目錄名稱；process.yaml 移到 `database\skill-runs\`。
- **imp-app**：process.yaml 分開；`unit-tests.json` 與 `deploy-*.json` 放在 Checkpoint Dir；`resolve_session.py` 與 `--out` 不再跟著目前目錄。
- **gen-imp-app**：process.yaml 分開；交給 gen-rsdc-app 的 `prompt-log.md` 改放 `handoff\gen-imp-app\`。
- **imp-home**：process.yaml 分開；`test_hub.js` 的暫存檔改放 `temp\`。
- **compile-skill**：`check_compiled.py` 的暫存檔改放 `temp\`；SKILL.md 與 README.md 引用舊規則檔。
- **check-md-deps**：SKILL.md 引用舊規則檔。
- **set-tag-status**、**write-topic**：照 report-md-rules 寫報告，卻沒有 Checkpoint 欄，也沒有 process.yaml。
- **還沒決定的**：gen-rsdc-app 交回給呼叫者的結果只在對話裡，是否改寫進 `handoff\`；reformat-md 的 `#v1` 副本寫在原檔旁邊。

## 4. 要做的

1. 每個 skill 先讀它的 README.md 與 skill-writing.md，照「When the Skill Is Changed」改，中文版也是。
2. 照上面的清單，一個 skill 一個 commit；太大的再拆成 sub task。
3. 改完的 skill 用 check-skill 檢查。
4. ✅ 引用都改完之後，刪掉 scratch-rules.md、report-yaml-rules.md 與它們的中文版；[[Task 100.5]] 檢查。
5. 在 CHANGES.md 加一筆。

## 5. 驗證

- `git grep` 在 `skill-groups/common` 找不到 scratch-rules 與 report-yaml-rules。
- 每個改過的 skill，check-skill 的 Template alignment 與 Dataflow 不報新的 issue。
- 跑一次 asd-ste：`checkpoints\asd-ste\{yymmdd}.{N}\` 有 step_N.yaml，`database\skill-runs\asd-ste\{yymmdd}.{N}.yaml` 有每一步的時間與 model。

## 6. 與其他 task 的關係

- [[Task 100]]：本 task 的上層；盤點在它的表 4 到表 7。
- [[Task 100.2]]、[[Task 100.3]]：新的規則與範本。
- [[Task 100.5]]：檢查本 task 的結果，包括舊檔已刪。
- [[Task 97]]：也會改各個 skill 的 SKILL.md；兩個同時做的話，會改到同一個檔。

## 7. 知識

—

## 8. 日誌

### 2026-11-06

- 做完：13 個 skill 照 run-data-rules 改，兩個舊規則檔刪掉；其餘 9 個開 [[Task 100.6]]。
- [[Task 100.5]] 提出：刪兩個舊檔的工作加進「要做的」第 4 項。
- 提出。
