# Task 87 - chore 不放自己的程式，只呼叫 skill group 裡的

**Status**：完成——2026-10-30 chore-rules.md 與中文版規定 chore 沒有自己的程式、只用 skill 或 skill group 裡的程式，並加上 private chore；`check_chores.py` 檢查每個執行檔案的指令都寫成 `{skillGroups.X}/…`；`publish_snapshot.py` 搬進 common，[[publish-gestalt]] 標為 private。
**Raised**：2026-10-30，[[Task 86]] 讓 chore 和 skill 一樣用名稱之後，使用者問：chore 能不能有自己的程式（那樣就和 skill 一樣），以及要不要限制 chore 至少用一個 skill。
**Depends on**：[[Task 86]]

## 1. 背景

- skill 回答「怎麼做一件事」：步驟、程式與 references，沒有狀態，需要時才呼叫。
- chore 回答「什麼時候要做、做了沒有」：觸發條件、要呼叫什麼、結果怎麼記，有上次執行與執行紀錄。
- chore 若有自己的程式，「怎麼做」就分散在 skill 與 chore 兩處，同一種邏輯可能寫兩份；別的 agency 也拿不到 chore 的程式，因為它只透過 skill group 使用共用的東西。
- 「至少用一個 skill」太嚴：現在三個 chore 只有 [[rerecord-ste-custom]] 呼叫 skill 的程式（asd-ste 的 `draft.py`）；[[keep-english]] 呼叫 common 的 `audit_keep_english.py`，[[publish-gestalt]] 呼叫本 repo 根目錄的 `scripts/publish_snapshot.py`。
  為了合規而把小程式包成 skill，只換來形式上的一致。

## 2. 現況

| chore | 呼叫的程式 | 在 skill group 裡 |
| --- | --- | --- |
| [[rerecord-ste-custom]] | `.github/common/skills/asd-ste/scripts/draft.py` | 是，但路徑寫死 `.github/common` |
| [[keep-english]] | `{skillGroups.common}/scripts/audit_keep_english.py` | 是 |
| [[publish-gestalt]] | `scripts/publish_snapshot.py` | 否，在本 repo 根目錄 |

- [chore-rules.md](../.github/common/rules/chore-rules.md) 沒有規定 chore 能呼叫哪裡的程式。
- `check_chores.py` 的 files 檢查已經只接受 `chores/<name>.md`，`chores/` 裡放程式或子目錄會 FAIL；規則沒有寫出原因。

### 2026-10-30 做完之後

- [chore-rules.md](../.github/common/rules/chore-rules.md) 與中文版：
  - Files：`chores/` 裡不放程式或目錄，因為 chore 沒有自己的程式。
  - A Chore of a Different Agency：不做別的 agency 的 private chore。
  - The Chore File：格式多一行選用的 `**Private**`；新增「chore 沒有自己的程式」：step 使用 skill 或 skill group 裡的程式，路徑寫 `{skillGroups.X}`，並說明 skill 與 chore 的分工；新增 private chore：只有擁有它的 agency 做，程式可以寫那個 agency 的值，但仍放在 skill group。
- [check_chores.py](../.github/common/scripts/check_chores.py) 加上兩項檢查（共 18 項）：
  - programs：本 workspace 的 chore 檔裡，每個 inline code 與 fenced block 中執行檔案的指令（`python`、`node`、`bash`、`sh` 等加上 `.py`、`.js`、`.sh` 之類的路徑，或直接執行 `./…`、`{skillGroups.X}/…`），路徑要寫成 `{skillGroups.X}/…`，X 是 `config.yaml` 有的 skill group；寫實際路徑（例如 `.github/common/…`）也 FAIL；沒有路徑的指令（`git`、`gh`）不看。
  - private：摘要表裡文字的一列，不能是別的 agency 的 private chore。
  - `config.yaml` 的 `skillGroups` 與 `agencies` 都由同一個小函式讀，仍只用標準函式庫。
- `publish_snapshot.py` 用 `git mv` 搬到 [.github/common/scripts/](../.github/common/scripts/publish_snapshot.py)，開頭註明它只服務 SkillsGestalt 的 private chore [[publish-gestalt]]，值照舊寫死；`.gitignore` 的註解、[[Task 78]] 與 [[Task 79]] 的連結跟著改，兩個 task 各加一行日誌。
- [[publish-gestalt]] 加上 `**Private**` 行，三條指令改寫 `{skillGroups.common}/scripts/publish_snapshot.py`；[[rerecord-ste-custom]] 的兩條指令改寫 `{skillGroups.common}/skills/asd-ste/scripts/draft.py`。

## 3. 要做的

### 已決定（2026-10-30）

- 規則：chore 不放自己的程式；它的步驟只呼叫 skill，或 skill group 裡的程式。
  chore 檔只寫觸發條件、要呼叫什麼、怎麼判斷結果、怎麼記錄與 commit。
- `chores/` 只放 `<name>.md`：規則補一句原因，`check_chores.py` 已經這樣檢查。
- `check_chores.py` 檢查 `3. 怎麼做` 裡每個執行本機檔案的指令，例如 `python`、`node`、`bash` 加上一個 `.py`、`.js`、`.sh` 之類的路徑：那個路徑要在某個 skill group 裡，寫成 `{skillGroups.X}/…`，或展開之後落在 `config.yaml` 的 `skillGroups` 的某個目錄。
- 不規定「至少用一個 skill」。
- [[publish-gestalt]] 的 `publish_snapshot.py` 搬進 `{skillGroups.common}/scripts/`。

### 開始做時決定的（2026-10-30）

- `publish_snapshot.py` 的值照舊寫死，[[publish-gestalt]] 標為 private chore：加一個頭行 `**Private**`，規則說明 private chore 只有擁有它的 agency 做，它的程式可以寫那個 agency 的值；程式開頭也註明只給 SkillsGestalt 用。
- [[rerecord-ste-custom]] 的路徑改成 `{skillGroups.common}`。
- 沒有路徑的指令（`git`、`gh`）不檢查。
- 指令裡寫實際路徑而不是 `{skillGroups.X}` 時 FAIL：別的 agency 的 common 在別的位置，實際路徑在那裡跑不動。
- 檢查的範圍是整份 chore 檔的 inline code 與 fenced block，不只「3. 怎麼做」：「2. 何時要做」也有 `due` 這類指令，同樣要在別的 agency 跑得動。

### 步驟

1. [chore-rules.md](../.github/common/rules/chore-rules.md) 與中文版：加上 chore 不放自己的程式、只呼叫 skill group 裡的程式，以及 `chores/` 只放 `<name>.md` 的原因。
2. `check_chores.py`：加上 `3. 怎麼做` 的指令檢查。
3. `publish_snapshot.py` 搬進 `{skillGroups.common}/scripts/`，[[publish-gestalt]] 與 `.gitignore` 等提到它的地方跟著改。
4. [[rerecord-ste-custom]] 的路徑改成 `{skillGroups.common}`。
5. 跑 `check_chores.py`、`check_tasks.py`，以及 `publish_snapshot.py check`。

## 4. 驗證

- `check_chores.py` 在本 agency 是 PASS；在副本把某個 chore 的指令改成 `python scripts/x.py`，它就 FAIL。
- `publish_snapshot.py check` 從新的位置執行，結果和搬之前一樣。
- chore-rules.md `check_ste.py` 是 PASS，與中文版 `check_parity.py` 是 0 failure。

2026-10-30 的結果：

- 本 agency：加上檢查之後、改 chore 之前，`check_chores.py` 正好在 [[publish-gestalt]]（三處 `scripts/publish_snapshot.py`）與 [[rerecord-ste-custom]]（`.github/common/…`）FAIL；改完之後 18 passed。
- 暫用副本：`python scripts/x.py`、`{skillGroups.nope}/…`、`./run.sh`、fenced block 裡的 `bash .github/common/…` 都 FAIL；`git status && gh api` 不看；`node {skillGroups.dedi}/…` 通過；摘要表一列文字的 `publish-github` 因為是 private 而 FAIL。
- `publish_snapshot.py check` 從新的位置執行：scan 是 `nothing found`，列出和上次發佈相比的變動。
- chore-rules.md `check_ste.py` 是 PASS，與中文版 `check_parity.py` 是 0 failure，`diff_md.py --verify` 是 0 failure；`check_tasks.py` 是 PASS。

## 5. 與其他 task 的關係

- [[Task 86]]：chore 改用名稱，並把執行紀錄搬到摘要表；本 task 再定下 chore 與 skill 的分工。
- [[Task 78]]：建立 `publish_snapshot.py` 與 [[publish-gestalt]]。
- [[Task 85]]：別的 agency 做本 agency 的 chore；程式在 skill group 裡，別的 agency 才拿得到。

## 6. 知識

—

## 7. 日誌

### 2026-10-31

- [[Task 91]] 把 chore `publish-github` 改名為 `publish-gestalt`：本檔的連結跟著改，意思不變。

### 2026-10-30

- 建立 task：chore 不放自己的程式，只呼叫 skill 或 skill group 裡的程式，不規定至少用一個 skill；`check_chores.py` 檢查「3. 怎麼做」裡的指令；`publish_snapshot.py` 搬進 common。
- 開始做並完成：規則加上「chore 沒有自己的程式」與 private chore，`check_chores.py` 加上 programs 與 private 兩項，`publish_snapshot.py` 搬進 common，[[publish-gestalt]] 標為 private。
