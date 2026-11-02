# Task 98 - 修正 imp-home seed 的三個缺陷

**Status**：完成——2026-11-02 seed 的 `server.js` 遇到不齊或壞掉的設定，會在 listen 之前以 2 結束並指名每一個問題，頁面每次都重讀設定；26 項觀察都通過，驗證 script 放在 imp-home 的 `scripts/`，Home-RSDC 的 4.6 改成沒有已知缺陷。
**Raised**：2026-11-02，[[Task 18.7]] 對齊 Home-RSDC 時記下 seed 的 `server.js` 有三個缺陷，使用者決定另開 task 修正。
**Depends on**：—

## 1. 背景

[[Task 18.7]] 把 imp-home 的 seed document [Home-RSDC.md](../skill-groups/common/skills/imp-home/references/Home-RSDC.md) 對齊 App 範本時，在 4.6 Defects 記下三個讀 [server.js](../skill-groups/common/skills/imp-home/server/server.js) 時發現的缺陷：

- 設定缺欄位時補上預設值：port 8080、標題 `Home`、沒有連結。
- 不是 JSON 的 `app.config.json` 被當成空的。
- 設定只在啟動時讀一次，所以對連結的修改要重新啟動才會反映到頁面，而 2.7 說下一個 request 就會反映。

2026-11-02 再查，三處都還在，也沒有 task 在處理。

## 2. 現況

### 決定

- **四個欄位都必要，也檢查種類**：`title`、`port`、`links` 與 `assembledAt` 缺一個就停下；`port` 不是整數、`links` 不是清單，或 `title`、`assembledAt` 不是文字，也停下。
  搭建 hub 的 `setup_target.py` 本來就寫齊這四個欄位，所以搭建出來的 hub 不受影響。
- **命令列參數不代替檔案缺少的欄位**：`--port` 與 `--title` 只覆寫那一次執行的值，檔案缺少 `port` 或 `title` 照樣停下。
- **設定不齊或壞掉時，在 listen 之前以 2 結束**：主控台列出每一個問題；2 與 port 被佔用的 3、意料之外的 1 分得開。
- **頁面每次都重讀設定**：Render the page 在每個 request 重讀標題與 link list；那時檔案壞了或缺欄位，就以 500 回答並指名問題，hub 照常執行。
  mount 與 Health answer 仍然是啟動時的結果，與 Home-RSDC 2.3 的寫法一致。
- **實際跑 hub 驗證，結果寫進 4.5**。
- **不加 CHANGES.md**：Forge 已經建好的 hub 用的是自己的程式，搭建又一定寫齊四個欄位，所以 Forge 不必做什麼，它的檢查也不會從 PASS 變成 FAIL。
- **[[Task 18.7]] 連到這個 task**。
- **驗證 script 放進 repo**（2026-11-02，修好之後）：放在 imp-home 的 [test_hub.js](../skill-groups/common/skills/imp-home/scripts/test_hub.js)，寫法照 reformat-md 的 `test_reformat.py`：一支 script，每項印 `[PASS]` 或 `[FAIL]`。
  它在系統的暫存目錄放一份 hub，結束時刪掉；預設測 seed，也可以指定一個 hub 目錄。
  Home-RSDC 4.5 的 Performed by 改成它；imp-home 的 SKILL.md 不提它，因為它不是 skill 執行時的一步；它也不另外拿修正前的程式來比。

### 進度

- `server.js`：新增 `readAppConfig`，檢查 Home-RSDC 2.5 的每一個欄位，回傳設定或逐項的問題，絕不補值；`describeProblems` 把問題寫成一段訊息。
  `resolveOptions` 遇到問題就印出、把 exit code 設為 2 並回傳 null，`main` 因此什麼都不啟動；頁面的路由每次都呼叫 `readAppConfig`，有問題就以 500 回答。
  換行仍是 CRLF，`node --check` 通過。
- Home-RSDC.md：2.3 寫明執行中壞掉的檔案只讓那一次頁面的 request 被拒絕，Exception Paths 多一項；2.5 寫明四個欄位、種類、exit code 2，以及覆寫不代替缺少的欄位，欄位表的 `port`、`links` 與 `assembledAt` 補上種類；2.8 的頁面路由補上 500；3.2 的第 2 步與第 7 步照新的程式改寫。
  4.5 新增兩列記下這次的修正，原本的 15 列中有 14 列寫上 2026-11-02 觀察到的結果；只有「mounted app 不發出任何絕對位址」仍是 not verified，因為那是被掛載的 app 的事，hub 無法強制。
  4.6 改成 None known，英文版從 642 行變成 627 行。
- 中文版：照 chinese skill 更新，判定 INCREMENTAL，change set 是 12 個 hunk、33 行；其餘 594 行逐字保留，4.6 照範本中文版寫成「目前沒有已知缺陷。」。

### 驗證的方法

- 以 [test_hub.js](../skill-groups/common/skills/imp-home/scripts/test_hub.js) 觀察：它在系統的暫存目錄放一份 hub，用它自己的 `app.config.json` 與六個小 app 啟動 hub，逐項觀察，共 26 項，結束時刪掉暫存目錄。
  六個小 app 分別是：正常回答、throw、回傳被 reject 的 promise、回答後在之後的 tick 上 throw、回答後留下被遺忘的 rejection，以及沒有 `app.js` 的目錄。
- 同一支 script 也在 HEAD 的舊程式上跑：與三個缺陷有關的 10 項失敗，其餘 16 項在新舊程式上都通過，見表 1。
- 預設測 seed 的 `server/`；給一個 hub 目錄，就測那個 hub 的 `server.js` 與 `public/`，它原本的 `app.config.json` 不讀也不寫。
  全部通過以 0 結束，有一項失敗以 1 結束，目錄裡沒有 `server.js` 以 2 結束。
- 這支 script 先在 scratchpad 寫成、跑過，使用者決定之後才放進 repo；表 1 的結果，放進 repo 之後再跑一次也一樣。

**表 1：驗證 script 的 26 項觀察**

| 項目 | 項數 | 新程式 | HEAD 的舊程式 |
|---|---|---|---|
| 設定不齊或壞掉時拒絕啟動 | 7 | 7 項通過 | 7 項失敗：照常啟動 |
| 執行中修改或弄壞設定 | 4 | 4 項通過 | 3 項失敗：頁面仍是啟動時的內容 |
| 頁面、`/healthz` 與 404 | 6 | 6 項通過 | 6 項通過 |
| mount | 8 | 8 項通過 | 8 項通過 |
| 同一份原始碼提供第二份設定 | 1 | 1 項通過 | 1 項通過 |

## 3. 要做的

✅ 2026-11-02 三個缺陷都修好，Home-RSDC 與它的中文版跟著改。

## 4. 驗證

- 驗證 script 的 26 項在新程式上都通過；在 HEAD 的舊程式上，與三個缺陷有關的 10 項失敗，見表 1。
- Home-RSDC 的單獨檢查 `check_rsdc.py --rsdc` PASS，27 項通過，1 個警告和修正前相同；`--skill` 檢查也 PASS。
- 中英對照 `check_rsdc.py --rsdc --tw` PASS，2 個警告和修正前相同；`check_parity.py` 0 failure，`diff_md.py --verify` PASS。
- `server.js` 的 `node --check` 通過，換行仍是 CRLF。
- repo 裡的 `test_hub.js`：seed 26 項全部通過；以參數指定修正前的 `server.js`，與缺陷有關的 10 項失敗；沒有 `server.js` 的目錄以 2 結束；跑完沒有留下暫存目錄，也沒有留下 process。
- Home-RSDC 4.5 改了 Performed by 之後，中英兩份的 `check_parity.py` 0 failure，`diff_md.py --verify` PASS，三種 `check_rsdc.py` 檢查都 PASS，警告和之前相同。

## 5. 與其他 task 的關係

- [[Task 18.7]]：對齊 Home-RSDC 時記下這三個缺陷。
- Task 2.5 @ InvestForge：InvHome 的程式有同樣的寫法，但它自己的設計文件還是舊版；要不要算缺陷，在它對齊時決定。

## 6. 知識

### 適合寫成新 topic

- **用修正前的程式確認檢查抓得到缺陷**：修好缺陷之後，把同一支檢查拿到修正前的程式上再跑一次；與缺陷有關的項目必須失敗，否則這支檢查證明不了修正。
  來源：本 task 的驗證，在 HEAD 的舊 `server.js` 上 10 項失敗、16 項通過。

### 適合併進現有 topic

—

### 不算知識

- 驗證 script 等待一個應該結束的 process；舊程式不會結束，script 因此卡住，加上 2 秒逾時之後才跑完。
- macOS 沒有 `timeout` 指令。
- 同一天 `.github/` 改名為 `skill-groups/`（[[Task 97.7]]）；在改名之後寫到舊路徑的檔，會建出一個未追蹤的 `.github/`，所以寫新檔之前先確認目錄還在。

## 7. 日誌

### 2026-11-02

- 連結的目標路徑從 `../.github/` 改成 `../skill-groups/`，字句沒有改（[[Task 97.7]]）。
- 建立：使用者決定另開 task 修正 [[Task 18.7]] 記下的三個缺陷。
- `server.js` 修好，Home-RSDC 與它的中文版跟著改；驗證 script 的 26 項都通過，在舊程式上與缺陷有關的 10 項失敗。
- 使用者決定把驗證 script 放進 repo：寫成 [test_hub.js](../skill-groups/common/skills/imp-home/scripts/test_hub.js)，Home-RSDC 4.5 的 Performed by 改成它，中文版跟著改。
