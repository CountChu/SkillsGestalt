# Task 18.7 - Home-RSDC（imp-home 的 seed）

**Status**：完成——2026-10-18 照 App 範本手動對齊，英文版從 330 行變成 642 行；單獨、中英對照與 `--skill` 三種檢查都 PASS，imp-home 引用它節號的地方一起改。
**Raised**：2026-10-10，[[Task 18]] 提出時查的 8 份已寫好的 RSDC 之一。
**Depends on**：—

## 1. 背景

讓 imp-home 的 seed document [Home-RSDC.md](../.github/common/skills/imp-home/references/Home-RSDC.md) 跟上 App 範本。
共用的規則與決定，見 [[Task 18]]。

## 2. 現況

### 2026-10-18 查的結果

- `check_rsdc.py --rsdc` 單獨檢查有 6 項 FAIL：header quote 沒有連到標準與範本、標題不是 `# {SYSTEM} - RSDC`、四章的標題、小節不是 N.M 編號，以及範本的必要小節不齊。
- 330 行；小節是 1.1–1.4、2.1–2.9、3.1–3.3 與 4.1–4.2。
  範本第 2 章要有 Terminology、Artifact Types、Dataflow（含 DFD）、Naming and Data Structures、Config Schemas、Presentation Contract、HTTP API、Mountable Handler 與 Invariants，第 3、4 章也要有 Execution Flow、Implementation Guidelines and Tools、Safety and Robustness 與 Defects 等節。
- 範本只有 2.6 Derivation Rules 與 4.4 Platform Traps 標 Optional；2.9 Mountable Handler 是必要節，但 Home 自己就是 hub。
- imp-home 的 SKILL.md 有 12 處引用它的節號：§2.1–§2.8、§3.2、§3.3、§4.1 與 §4.2，中文版也一樣。
- [[Task 60]] 已把它改成 LF，8 處英式拼法改成美式；中英對照的 `check_rsdc.py` PASS。
- InvestForge 的那一份已經不同，歸 Task 18.6。

### 決定

- **2.9 Mountable Handler 從 hub 這一側寫**：hub 對它所掛載的 app 要求什麼，也就是原 2.8「What makes an app mountable」的內容；範本的第一句對 hub 也成立。
- **預設值照範本**：2.5 寫「缺少的欄位要回報，不能補值」；程式碼現在補預設值（port 8080、標題 `Home`、沒有連結），以及格式壞掉的 `app.config.json` 被當成空的，都列進 4.6 Defects，程式另外改。
- **假設「app 由 hub 掛載、有 Python kernel」的固定句照 hub 的實情改寫或拿掉**：1.4 的「Opens from the hub, runs alone」換成原本的第 7 個目標；2.1 的 Hub 定義成這個 app 本身；3.1 改成「Node does all of it; there is no kernel」；4.1 的 `require.main` 與 `app.js`、4.2 的 Python 版本、4.3 的「guards enforced again inside the Python kernel」拿掉或改寫。
- **4.5 Verification Obligations 全部標 not verified**：原本 15 列的證明方法，改寫成表格下的「可以怎麼改成機械化的檢查」。
- **自己做的小判斷**（列逐節對應時使用者看過，沒有異議）：保留兩個 Optional 節，2.6 寫 mount prefix 與 dead count 的推導，4.4 寫 `file://` 連結被瀏覽器擋下的陷阱；原 2.9 的 registry 規則併進 2.5；原本開頭四段併進 Authority、1.2、2.7 與 4.1；SKILL.md 引用 Design、Coding 兩章的四處改成不帶節號的說法。

### 進度

- 英文版：照 App 範本重寫成 642 行；header quote 連到 `[[RSDC-Standard]]`、`[[DFD]]` 與 `[[RSDC-App-tmp]]`，以 `depends_on.py record` 記錄指紋。
  stage 是 Prepare the mounts、Delegate to a mount、Render the page 與 Report health；role 是 reader、client、assembler 與 mounted app；hub 不寫任何 record，所以 DFD 沒有圓柱與藍線。
  原文的內容都保留，分到範本的各節；`server.js` 是新寫的 Artifact Types、Dataflow、HTTP API、Execution Flow 與 Defects 的依據。
  3.3 原本列了框架 skill 的生命週期紀錄檔，檔名帶著 skill 的名字，`--skill` 檢查判 FAIL，改成不寫檔名的一句。
  拼法另外掃過一次，把 `specialised` 改成 `specialized`。
- 中文版：照 chinese skill 更新，判定 INCREMENTAL，change set 是 642 行中的 547 行。
  change set 以外的 95 行逐字保留，與範本共用的 69 行照抄範本中文版，其餘翻譯；Terminology 定義的詞、資料與 stage 的名稱都保留英文，和 InvCov 的中文版一樣。
  第一次 `diff_md.py --verify` 判 1 項 FAIL：第 26 行的英文與舊版相同，卻被重新翻譯；改回舊譯文後通過。
- imp-home 的 SKILL.md 與中文版：第 2 章的 8 處引用改成新的節號並寫上節名；§3.2、§3.3、§4.1 與 §4.2 在 Design、Coding 兩章，改成不帶節號的說法。
  SKILL.md 中英兩份照 chinese skill 更新，只改這兩行。
- seed 的 `server.js`：16 處「design X.Y」註解改成新的節號，換行仍是 CRLF，`node --check` 通過；`app.config.json` 讀不到時補預設值的那一行註解，改成指向 4.6 的缺陷。

### 順帶發現

- 4.6 記下 3 個缺陷，都是讀 `server.js` 時發現的，還沒在執行中看到：缺少的欄位被補上預設值；不是 JSON 的 `app.config.json` 被當成空的；`app.config.json` 只在啟動時讀一次，所以對連結的修改要重新啟動才會反映到頁面，而 2.7 說下一個 request 就會反映。
  程式另外改，還沒開 task。
- `--skill` 檢查的 WARN：imp-home 的 SKILL.md 沒有「# Dataflow」一節，HEAD 就有，屬於 [[Task 24]] 要改的 skill 格式。
- 中文版的 5 則用詞 WARN 都在必須照抄的行上：範本共用句裡的「識別碼」與「讀者」，以及 change set 以外逐字保留的「被掛載的 app」「使用者」與「請求」。

## 3. 要做的

✅ 2026-10-18 照 App 範本對齊，中文版與 imp-home 的引用一起改。

## 4. 驗證

- 英文版單獨檢查 `check_rsdc.py --rsdc` PASS，27 項通過，1 個警告：DFD 沒有藍線，因為 hub 不寫任何 record。
- 中英對照 `check_rsdc.py --rsdc --tw` PASS，13 項通過，2 個警告，見「順帶發現」。
- `check_rsdc.py --rsdc --skill` PASS：6 處 § 引用都落在寫出節名的那一節，也沒有引用 Design 與 Coding；1 個警告，見「順帶發現」。
- Home-RSDC 中英兩份 `check_parity.py` 0 failure，`diff_md.py --verify` PASS；imp-home 的 SKILL.md 中英兩份也一樣，警告和 HEAD 相同。
- 英文版沒有英式拼法，也沒有引用編號在後面的節。

## 5. 與其他 task 的關係

- [[Task 60]]：記下單獨檢查的 6 項 FAIL，也先把換行與拼法整理好。
- Task 18.6：InvestForge 的那一份，各自對齊。
- [[Task 58]]：寫新的內容時照它的規則，不寫文件自己的來歷。
- [[Task 24]]：imp-home 的 SKILL.md 沒有 Dataflow 一節，屬於它要改的 skill 格式。

## 6. 日誌

### 2026-10-18

- 從 [[Task 18]] 拆出。
- 使用者決定先對齊這一份：照 App 範本手動改，引用處同一次一起改；先列逐節的對應給使用者確認。
- 使用者確認逐節的對應，並決定 2.9、預設值、範本固定句與 4.5 的寫法。
- 英文版照範本重寫，中文版照 chinese skill 更新，imp-home 的 SKILL.md 與 `server.js` 的節號一起改；三種 `check_rsdc.py` 檢查都 PASS。
- 指向 Task 18.6 的 wikilink 改成純文字：它已移出本 workspace（[[Task 62.4]]）。

### 2026-10-10

- 列為 [[Task 18]] 要對齊的 RSDC 之一。
