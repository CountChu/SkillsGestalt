# Task 94 - 為 asd-ste 的對照頁寫 RSDC

**Status**：完成——ReviewPage-RSDC.md 與中文版已寫好，RSDC Checker 與 parity check 都通過；讀程式找到的 5 個缺陷記在 RSDC 的 4.6，程式沒有改。
**Raised**：2026-11-01，使用者問對照頁有沒有 RSDC；查過之後沒有，使用者要求開 task 寫一份。
**Depends on**：—

## 1. 背景

asd-ste 的 Step 6 以 `make_review.py` 產生對照頁 `step_6-review.html`，`review_server.js` 提供頁面並儲存審核狀態。
[[Task 39]] 建立了對照頁，[[Task 40]] 又做了 9 項修改。
這些設計沒有一份 RSDC，現在分散在三個地方：

- asd-ste 的 [SKILL.md](../skill-groups/common/skills/asd-ste/SKILL.md)：review page、review status、review server 的定義，以及 Step 6 的做法。
- asd-ste 的 [README.md](../skill-groups/common/skills/asd-ste/README.md)：Dataflow 裡的 Review statuses 與 `step_6-status.json`。
- [[Task 39]] 與 [[Task 40]] 的現況：每一項當時的決定，例如兩欄捲動、◄ ► 行號、反白規則、狀態的順序與 key 的算法。
  其中有幾項被後來的項目取代，例如第 2 項被第 4 項取代、第 6 項的順序被第 8 項取代，要讀完全部才知道對照頁現在的樣子。

## 2. 現況

### 2026-11-01 結果

- 寫好 [ReviewPage-RSDC.md](../skill-groups/common/skills/asd-ste/references/ReviewPage-RSDC.md) 與 [ReviewPage-RSDC-tw.md](../skill-groups/common/skills/asd-ste/references/ReviewPage-RSDC-tw.md)，各 564 行。
  gen-rsdc-app 的 Step 0 要 app 目錄有 `server.js`，對照頁沒有，所以照它的 SKILL.md 手動做；requirements record 是 [[Task 39]] 與 [[Task 40]]。
- 和範本不合的地方，使用者的決定：
  - 1.4 留著 hub 的目標，2.9 照範本寫出應有的契約 `createApp({ mountedAt, root })`；沒有 `app.js` 記成 4.6 的缺陷。
  - 2.5 寫「沒有設定檔」，命令列參數放進 2.8 的兩個命令列入口。
  - 3.1 的「Node serves and spawns; Python decides.」改成「Python builds; Node serves and keeps the marks.」，因為兩者都不啟動對方。
- 3 個 component：Review Builder（`make_review.py`）、Page Script（建頁寫進頁面的 script）、Review Server（`review_server.js`）；4 個 stage：Build the page、Show the page、Read the statuses、Save the statuses。
- 4.6 記下 5 個缺陷，程式都沒有改：
  - 沒有 hub 能掛載的 `app.js`。
  - 頁面的 `/healthz` 與索引的連結是絕對位址，在 hub 的前綴底下會失效。
  - 同一份頁面開兩份時，後儲存的一份會抹掉另一份的標記：每次儲存都取代整組。
  - 超過 1 MiB 的 body 得不到 400，伺服器直接關閉連線。
  - `--host` 能把監聽位址擴大到 loopback 以外，沒有任何提示，雖然程式的說明寫著只用 loopback。
- asd-ste 的 README 與中文版：When the Skill Is Changed 加上 ReviewPage-RSDC 那一段，改完要跑的檢查加上 `check_rsdc.py`。

### 2026-11-01 已決定

- **檔名與位置**：`.github/common/skills/asd-ste/references/ReviewPage-RSDC.md`，加上中文版 `ReviewPage-RSDC-tw.md`，和 SkillCompiler-RSDC、Home-RSDC 一樣放在 skill 的 references。
- **範本**：RSDC-App-tmp，用 [gen-rsdc-app](../skill-groups/common/skills/gen-rsdc-app/SKILL.md) 寫。
- **範圍**：`make_review.py` 與 `review_server.js`，也就是建頁、頁面的互動、審核狀態與伺服器；Step 6 怎麼呼叫它們，只寫介面。
- **以後的修改**：asd-ste README 的 When the Skill Is Changed 加一條：改 `make_review.py` 或 `review_server.js` 時，ReviewPage-RSDC 與它的中文版跟著改。
- **Task 40**：本 task 完成時一併結束 [[Task 40]]；之後對照頁的修改直接改 RSDC，不再記成 Task 40 的新項目。

### 2026-11-01 和範本不合的地方

gen-rsdc-app 假設 app 以 `node server.js` 啟動，實際的工作由 Python kernel 做。
對照頁不一樣：

- Python 的 `make_review.py` 一次建好靜態頁，不常駐。
- Node.js 的 `review_server.js` 只提供頁面、讀寫 `step_6-status.json`，不呼叫 Python。
- 一個伺服器服務 `checkpoints/asd-ste/` 底下所有的對照頁。
- 不經過伺服器、直接開檔案時，頁面也能用，只是不儲存狀態。

做的時候，逐項決定範本的哪些章節照寫、哪些寫 —，並和使用者確認。

## 3. 要做的

1. 讀 gen-rsdc-app 的 SKILL.md（它沒有 README.md），照它從 `make_review.py`、`review_server.js` 寫 ReviewPage-RSDC.md。
   以 [[Task 39]]、[[Task 40]] 的紀錄核對每一項設計，被取代的項目只寫最後的結果。
2. 照 chinese skill 寫 ReviewPage-RSDC-tw.md。
3. 以 check_rsdc.py 檢查 RSDC。
4. asd-ste 的 README.md 的 When the Skill Is Changed 加上 ReviewPage-RSDC 那一條；README-tw.md 照 chinese skill 跟著改；跑 README 列出的檢查。
5. 把 [[Task 40]] 改為完成。

**牽涉的檔案**

- 新增 `asd-ste/references/ReviewPage-RSDC.md` 與 `ReviewPage-RSDC-tw.md`
- asd-ste 的 `README.md` 與 `README-tw.md`
- `tasks/Task 40.md` 與摘要表

## 4. 驗證

- 在 scratchpad 以四個 15 行的測試檔與三個 item 實際跑兩支程式，結果寫進 RSDC 4.5 的 10 列；頁面的點擊沿用 [[Task 40]] 當時在瀏覽器裡的觀察，4 列；hub 那一列是 *not verified*。
  測試用的伺服器在 port 8797、8798 上啟動，測完都已關掉。
- `check_rsdc.py --rsdc ReviewPage-RSDC.md --tw ReviewPage-RSDC-tw.md`：PASS，13 項通過；1 個 warning 是一般字義的 item、草稿等字，不是 term 被譯掉。
  只檢查英文版時是 27 項通過，留下 1 個 warning：「Python 3.9」被讀成第 3.9 節，那是版本號。
- `check_parity.py` 對 ReviewPage-RSDC 一對：0 failure，1 個 warning 是範本中文版自己的「識別碼」，照範本照抄。
- `check_parity.py` 對 README 一對：0 failure，2 個 warning 和改之前相同；`diff_md.py --verify`：0 failure。
- `depends_on.py check`：README.md、ReviewPage-RSDC.md 與中文版都是 UNCHANGED。

## 5. 與其他 task 的關係

- [[Task 39]]：建立對照頁；它的現況是 RSDC 的來源之一。
- [[Task 40]]：對照頁的 9 項修改；本 task 完成時一併結束它。
- [[Task 93]]：也改 asd-ste 的 SKILL.md 與 README.md，兩個 task 不要同時做。
- [[Task 24]]：把其餘 skill 改成新格式時可能也改到 asd-ste 的 README.md，兩個 task 不要同時做。

## 6. 知識

—

## 7. 日誌

### 2026-11-02

- 連結的目標路徑從 `../.github/` 改成 `../skill-groups/`，字句沒有改（[[Task 97.7]]）。

### 2026-11-01

- 完成：寫好 ReviewPage-RSDC 與中文版，改 asd-ste 的 README 與中文版，並結束 [[Task 40]]。
- 提出：對照頁沒有 RSDC；決定檔名、範本、範圍，以及完成時一併結束 [[Task 40]]。
