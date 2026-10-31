# Task 62.4 - 搬走 InvestForge 的 9 個 task，Task 18 只留這裡的 3 份

**Status**：完成——9 個 task 搬到 InvestForge，成為那裡的 Task 2–6；這裡留下空號，指向它們的連結改成純文字；使用者看過。
**Raised**：2026-10-18，[[Task 62]] 拆出的第 4 步：主題是 InvestForge 的 task 搬到 InvestForge。
**Depends on**：[[Task 62.2]]、[[Task 62.3]]

## 1. 背景

主題就是 InvestForge 的東西，共 9 個，其中 18.1、18.3 與 28 已完成。
搬走之後，它們在這裡是空號，在 InvestForge 的編號是：

- Task 18.1（StopPriceChecker-RSDC）→ Task 2.1 @ InvestForge
- Task 18.3（InvCov-RSDC）→ Task 2.2 @ InvestForge
- Task 18.4（InvDataflow-RSDC）→ Task 2.3 @ InvestForge
- Task 18.5（InvIndexAnalyzer-RSDC）→ Task 2.4 @ InvestForge
- Task 18.6（Home-RSDC，InvHome）→ Task 2.5 @ InvestForge
- Task 28（修正 InvCov-RSDC 4.6 記下的缺陷）→ Task 3 @ InvestForge
- Task 29（在 Windows 上實測 InvCov Kernel 輸出的編碼）→ Task 4 @ InvestForge
- Task 30（讓 4 個 owner skill 的 design pair 跟上 App 範本）→ Task 5 @ InvestForge
- Task 37（讓 InvCov 的 Wireframe 中英兩份逐行對齊）→ Task 6 @ InvestForge

## 2. 現況

### 2026-10-18 查的結果

- 留在這裡的 task 中，指向它們的 wikilink：[[Task 18]] 連到 18.1、18.3–18.6 與 30；[[Task 18.7]] 連到 18.6；[[Task 14]]、[[Task 32]]、[[Task 33]] 與 [[Task 55]] 連到 30；本 task 也連到全部 9 個。
- 9 個之間也互相連：18.3、28、29 與 37 彼此連，搬過去時改成 InvestForge 的新編號。
- 摘要表沒有一列依賴它們。
- 9 個中只有 Task 30 有 Depends on：[[Task 12]]、[[Task 10]] 與 [[Task 33]]，都已完成；[[Task 18]] 的 Depends on 也是這 3 個。
- 9 個裡的「這裡」指的都是那個 task 自己，搬過去意思不變。

### 已決定（2026-10-18）

動手前問了 7 個問題，都照建議：

- InvestForge 的新父 task 沿用 [[Task 18]] 的 Raised（2026-10-10），所以照 Raised 排序是 Task 2，sub task 2.1–2.5；28、29、30、37 依序是 Task 3–6。
- 搬家這次在 InvestForge 的 commit，前綴用 `task 62.4`：這是這裡的 session 在那裡做的 commit，照 InvestForge 摘要表的說明，用這裡的編號。
- 搬過去的 task 裡，指向這裡的 wikilink 改成文字 `Task N @ SkillsGestalt`；Task 37 連到 md-style.md 的連結改成 inline code `{skillGroups.common}/rules/md-style.md`。
- [[Task 18]] 的「要決定的」第 2 點（App 的 design pair）只關於 InvDataflow 與 InvIndexAnalyzer，整點搬到 InvestForge 的 Task 2。
- InvestForge 的 Task 2 只引用 [[Task 18]] 的共用規則，不抄一份。
- 這裡留下的 task 裡，指向它們的 wikilink 改成純文字的舊編號，例如 `Task 30`；這裡不提 InvestForge，空號那一行說明號碼已移出。
- 搬過去的 9 個 task 正文不改：只改編號、連結與 Depends on，再加一行日誌記下原本的編號。

### 結果（2026-10-18）

- InvestForge：新建 Task 2（父 task，裝 2.1–2.5 與「要決定的」），以及 2.1–2.5 與 3–6；摘要表加上 10 列。
  每個搬來的檔：標題改成新編號；指向這裡的 wikilink 改成 `Task N @ SkillsGestalt`，彼此之間改成新編號；日誌加一行「從 Task N @ SkillsGestalt 搬來」。
  Task 5（原本的 30）的 Depends on 改成 —，三個前提寫在第 5 章。
  從 InvestForge 的根目錄跑 `check_tasks.py`：11 個 task 檔，18 項 PASS。
- 這裡：刪掉 9 個檔與摘要表的 9 列；摘要表加上 `空號：18.1、18.3、18.4、18.5、18.6、28、29、30、37。` 與一句說明。
  [[Task 18]] 的 Status 行、sub task 清單與「要決定的」只留這裡的 3 份。
  [[Task 14]]、[[Task 18]]、[[Task 18.7]]、[[Task 32]]、[[Task 33]] 與 [[Task 55]] 指向它們的 wikilink 改成純文字，各記一行日誌。

## 3. 要做的

1. ✅ 在 InvestForge 匯入 9 個 task，照 [[Task 62.1]] 的規則檔：
   - 編號接在 InvestForge 現有的號碼之後，依原本的 Raised 排序。
   - 18.1、18.3–18.6 成為一個新父 task 的 sub task；父 task 寫明它們共用的規則與決定，並以文字 `Task 18 @ SkillsGestalt` 引用這裡的 [[Task 18]]。
   - 每個檔的 Raised 與日誌照舊，日誌加上搬來那天的一節，寫明原本是 SkillsGestalt 的哪一個 task。
   - Depends on 只留 InvestForge 自己的 task；指向這裡的連結改成文字 `Task N @ SkillsGestalt`，寫在第 5 章。
2. ✅ 在這裡刪掉 9 個檔與摘要表的 9 列；把 9 個號碼寫進摘要表的空號那一行，並在圖例的說明加一句（見 [[Task 62.2]]）。
3. ✅ 改 [[Task 18]]：Status 行、sub task 清單與「要決定的」只留 18.2、18.7 與 18.8；日誌加一節。
4. ✅ 留在這裡的 task 中，指向 9 個的 wikilink 改成純文字；句子本身照 [[Task 62]] 的「已決定」保留。
5. ✅ 兩邊都跑 `check_tasks.py`。
6. ✅ 使用者看過之後 commit：InvestForge 一個、這裡一個，前綴都是 `task 62.4`。

## 4. 驗證

- 兩邊的 `check_tasks.py` 都 PASS。
- 這裡的 `tasks/` 沒有 18.1、18.3–18.6、28、29、30 與 37 的檔，也沒有指向它們的 wikilink。
- InvestForge 每個搬來的 task 都寫著原本的編號，兩個 repo 的 `git log --grep` 用原本的編號找得到當時的 commit。

## 5. 與其他 task 的關係

- [[Task 18]]：只留 18.2、18.7 與 18.8。
- [[Task 62.5]]：其他一半是 InvestForge 的 task 在那裡拆。

## 6. 知識

—

## 7. 日誌

### 2026-10-19

- 使用者看過，同意 commit；本 task 完成。

### 2026-10-18

- 從 [[Task 62]] 拆出，列出要搬的 9 個，以及指向它們的 wikilink。
- [[Task 62.2]] 定下空號那一行，第 2 步跟著改。
- [[Task 62.3]] 定下 `Task N @ <workspace>` 的寫法，第 1 步跟著改。
- 開始：問了 7 個問題，見「已決定」。
- 9 個 task 搬到 InvestForge，成為 Task 2–6；這裡留下空號，指向它們的 wikilink 改成純文字。
