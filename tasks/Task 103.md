# Task 103 - 加 skill 與 chore clean-checkpoints：checkpoints\ 太大時列出舊的項目，確認後清掉

**Status**：完成——skill 與 chore `clean-checkpoints`、`CHANGES.md` 的一筆與 `config.example.yaml` 的範例都寫好並試跑過（`3.4`–`3.6`）；使用者決定不做完整的 `/check-skill`。
**Raised**：2026-11-12，一個 Forge 的 `checkpoints\` 半年累積到約 18 GB，手動清過一次，要讓之後有固定的做法。
**Depends on**：—

## 1. 背景

- [run-data-rules.md](../skill-groups/common/rules/run-data-rules.md) 規定 Checkpoint Dir 是 `checkpoints\{skill}\{yymmdd}.{N}\`，也寫明 `temp\` 與 `checkpoints\` 的每個項目都可以在你想要的時候手動移除；但沒有 skill 或 chore 告訴你何時、怎麼移除。
- `common` 沒有清理用的 skill。SkillsGestalt 自己的 `checkpoints\` 只有 1 個資料夾，問題出在 Forge。
- 那個 Forge 的情形：
  - 清理前約 18 GB、62 個資料夾；九成以上是同一個 skill 的資料夾，每次執行會多一個大資料夾。
  - 手動清理後約 5.8 GB、10 個資料夾。
  - 有些資料夾別的 skill 還會讀，和「都可以移除」不一樣，所以要能指定不清的資料夾。
  - 有些執行資料夾的名稱出現在還沒完成的 task 裡，這些也要留。
- 本 task 會公開到 GitHub，所以不寫那個 Forge 的名稱、它的 skill 名稱與它的資料內容。

## 2. 結論

- 新的 skill [clean-checkpoints](../skill-groups/common/skills/clean-checkpoints/SKILL.md) 與 chore [[clean-checkpoints]]：`checkpoints\` 超過 `cleanCheckpoints.maxSizeGB`（預設 10 GB）時，列出最新的檔案超過 `keepDays`（預設 60 天）的項目，使用者確認後才送到資源回收筒（`3.4`）。
- 一定保留：`keep` 裡的 skill 資料夾、`checkpoints\chores\`，以及名稱或名稱裡 7 位以上的數字出現在 ⬜／🔄 task 裡的項目（`3.6`）。
- 每個 Forge 照 `CHANGES.md` 2026-11-12 那一筆，在自己的 `config.yaml` 加 `cleanCheckpoints`，要做這個 chore 就在摘要表加一列。
- 只用 `scan_skill.py` 檢查過，沒有做完整的 `/check-skill`（`3.5`）。

## 3. 過程

### 3.1 拆法（2026-11-12 與使用者決定）

- 通用的部分放在 SkillsGestalt：skill `clean-checkpoints` 與 chore `clean-checkpoints`。
- 每個 Forge 不同的部分放在 Forge 的根目錄 `config.yaml`：門檻、保留天數、不清的資料夾。
- Forge 自己在摘要表加 chore 的一列，用自己的設定試跑。

### 3.2 規則（2026-11-12 與使用者決定）

- 範圍：只有根目錄的 `checkpoints\`，不包括 `temp\`。
- 何時要做：`checkpoints\` 超過門檻時；那個 Forge 的門檻是 10 GB。
- 可以清：一個項目裡最新的檔案超過保留天數；那個 Forge 是 60 天。
- 一定要留：
  - 設定裡列出的資料夾（別的 skill 還會讀的）；
  - 名稱出現在 ⬜／🔄 task 檔裡的項目；
  - `checkpoints\chores\`（[chore-rules.md](../skill-groups/common/rules/chore-rules.md) 給 chore 放檔的地方）。
- 清的方式：先列出清單（項目、大小、最新檔案日期、理由），使用者確認後才送到資源回收筒；不直接刪除。

### 3.3 細節（2026-11-12 與使用者決定）

- 設定：Forge 根目錄 `config.yaml` 的 `cleanCheckpoints` 區段。沒有這個區段或少了 key 時，用預設值：`maxSizeGB: 10`、`keepDays: 60`、`keep: []`。

  ```yaml
  cleanCheckpoints:
    maxSizeGB: 10      # checkpoints\ 超過這個大小才做
    keepDays: 60       # 項目裡最新的檔案超過這麼多天，才列為可以清
    keep: [some-skill] # checkpoints\ 底下不清的 skill 資料夾
  ```

- 項目的單位：`checkpoints\{skill}\` 底下的每一個資料夾或檔案各算一項。資料夾的日期是它裡面最新的檔案的日期。
- 出現在 task 裡：讀 `config.yaml` 的 `taskSummary`，找 ⬜／🔄 的 task，開 `tasksDir` 裡的 task 檔；項目的名稱，或名稱裡任一段 6 位以上的數字（例如 `build_1234567_x` 的 `1234567`），出現在檔裡就保留。2026-11-12 改成 7 位以上，見 `3.6`。沒有 `tasksDir` 或 `taskSummary` 時，跳過這項檢查，並在清單上說明。
- 資源回收筒：Windows 用 PowerShell 的 `Microsoft.VisualBasic.FileIO.FileSystem` 送到資源回收筒；macOS／Linux 用 Python 的 `send2trash`，沒有安裝就停下來告訴使用者。絕不直接刪除。

### 3.4 寫好的檔（2026-11-12）

- skill：[SKILL.md](../skill-groups/common/skills/clean-checkpoints/SKILL.md)、[README.md](../skill-groups/common/skills/clean-checkpoints/README.md)、[clean_checkpoints.py](../skill-groups/common/skills/clean-checkpoints/scripts/clean_checkpoints.py)。
  - 照 gen-skill 的問題，使用者選：只有 step 檔、沒有 MD report；Working Dir 用 Temp Dir（清 `checkpoints\` 的 skill 不該自己又放東西在 `checkpoints\`）；沒有中文版。
  - 4 個 step：Step 0 Warmup、Step 1 List the items（script `list`，寫 `items.yaml`）、Step 2 Ask the user（不用 script，確認的清單寫進 `step_2.yaml`）、Step 3 Move to the recycle bin（script `recycle`，寫 `recycled.yaml`）。
  - `recycle` 會重新判斷每一項：Step 1 之後變新、或被 task 提到的項目會略過，不在清單上的路徑也略過。
  - script 只用 Python 標準函式庫、手讀 `config.yaml`，和 `check_chores.py` 一樣，所以沒有 `.venv` 也能跑；設定錯（不認得的 key、`keepDays` 不是整數、`maxSizeGB` 不大於 0、`keep` 的格式不對）以 `2` 結束。
- chore：[[clean-checkpoints]]，不是 Private；本 repo 的摘要表加了一列。
- `CHANGES.md` 加 2026-11-12 一筆「Forge 要做」；`config.example.yaml` 加註解掉的 `cleanCheckpoints` 範例。

### 3.5 試跑（2026-11-12）

- SkillsGestalt：`checkpoints\` 只有 `chores\keep-english`，0.00 GB，沒超過門檻；沒有 `tasksDir`，所以清單說沒比對 task。
- 一個 Forge（只跑 `list`，沒有移任何東西）：5.68 GB，沒超過 10 GB；777 項，可以清的 567 項只有 0.17 GB（多半是零散的小檔），42 項因為 ⬜／🔄 task 提到而保留。
- 假的 workspace（scratchpad，有舊的、新的、新舊混合、空資料夾、`keep`、`chores\`、task 與子 task 提到、已完成的 task 提到、根目錄的散檔）：每一項的判斷都對；`recycle` 送了 3 項到資源回收筒，略過 3 項（Step 1 之後變新、task 提到、不存在）。
- 發現：6 位以上的數字也會比對到日期。例如那個 Forge 的 `check-skill/check-260806-11`，名稱裡的 `260806` 出現在一個 🔄 task 的另一個項目名稱裡，就被保留。結果是多留，不會多清；使用者決定改成 7 位以上，見 `3.6`。
- check-skill：SkillsGestalt 沒有 `.venv`，所以借 Forge 的 `.venv` 只跑了 `scan_skill.py`。facts 裡的問題只有 Step 0 提到 Step 2（forward reference），已改掉；沒有照 checking-criteria 做完整的 `/check-skill`。

### 3.6 數字改成 7 位以上（2026-11-12 與使用者決定）

- build id 與 work item 都是 7 位，仍比對得到；日期 `yymmdd` 只有 6 位，不再比對。
- 使用者也問過改用建立目錄的日期：那是「舊不舊」的規則，不是「task 有沒有提到」的規則，解決不了這個問題。
  那個 Forge 的建立日期在搬家後還保留著，但會重複寫入的資料夾用建立日期會被當成舊的，所以「舊不舊」仍看最新的檔案。
- 那個 Forge 重跑 `list`：因 task 而保留的從 42 項變成 29 項，可以清的從 567 項變成 576 項；`check-skill/check-260806-11` 現在是可以清。
- 改了 script 的 `NUMBER_RE`、`SKILL.md` 的 description 與 **Clean item**、`CHANGES.md` 那一筆。

## 4. 要做的

1. ✅ 2026-11-12 和使用者定 `3.3`。
2. ✅ 2026-11-12 寫 skill `skill-groups/common/skills/clean-checkpoints/`（`3.4`）：
   - 先讀 [skill-writing.md](../skill-groups/common/rules/skill-writing.md) 與範本 [SKILL-tmp.md](../skill-groups/common/templates/SKILL-tmp.md)。
   - script 只列出可以清的項目，不刪；另一個步驟在使用者確認後送到資源回收筒。
   - 加 `README.md`，寫明改 skill 時要一起改的地方與檢查。
3. ✅ 2026-11-12 寫 chore `chores/clean-checkpoints.md`，照 [chore-rules.md](../skill-groups/common/rules/chore-rules.md)；不是 Private，Forge 也能做。在本 repo 的摘要表加一列。
4. ✅ 2026-11-12 在 `CHANGES.md` 記一筆「Forge 要做」：在 `config.yaml` 加設定、在摘要表加一列。
5. ✅ 2026-11-12 用 SkillsGestalt 自己的 `checkpoints\` 試跑；再用一份假的 `checkpoints\`（有舊的、新的、要留的與 task 提到的項目）確認清單正確。
6. ✅ 跑 `/check-skill clean-checkpoints`、`check_tasks.py` 與 `check_chores.py`： `check_tasks.py` 與 `check_chores.py` PASS；`/check-skill` 只跑了 `scan_skill.py`（`3.5`），使用者決定不做完整的檢查。
7. ✅ 2026-11-12 和使用者決定 6 位數字比對日期的問題：改成 7 位以上（`3.6`）。

## 5. 驗證

- 清單只列出超過保留天數、而且不在設定、不在 ⬜／🔄 task、不在 `checkpoints\chores\` 的項目。
- 沒有使用者確認，就不會移除任何東西；移除是送到資源回收筒。
- `checkpoints\` 沒超過門檻時，chore 說不必做。
- `check-skill`、`check_tasks.py` 與 `check_chores.py` 都 PASS。

## 6. 與其他 task 的關係

- [[Task 100]]：定了 Checkpoint Dir 與 Temp Dir 的規則，寫成 run-data-rules.md。
- [[clean-checkpoints]]：本 task 建立的 chore。

## 7. 知識

—

## 8. 日誌

### 2026-11-12

- 依使用者決定，不做完整的 `/check-skill`，直接完成：補 `2. 結論`，Status 改為完成。
- 依使用者決定，數字的比對從 6 位以上改成 7 位以上（`3.6`）；在那個 Forge 重跑 `list` 確認；第 7 項標完成。
- 照 gen-skill 寫 skill `clean-checkpoints`、chore `clean-checkpoints`、`CHANGES.md` 的一筆與 `config.example.yaml` 的範例；在 SkillsGestalt、一個 Forge 與假的 workspace 試跑（`3.4`、`3.5`）；第 2–5 項標完成，加第 7 項。
- 和使用者定 `3.3` 的 4 件事：設定的格式與預設值、項目的單位、怎麼比對 task、Windows 以外的資源回收筒；第 1 項標完成，Status 改為進行中。
- 建立 task：一個 Forge 的 `checkpoints\` 太大，要一個通用的清理做法。記下和使用者定好的拆法（`3.1`）與規則（`3.2`）。
