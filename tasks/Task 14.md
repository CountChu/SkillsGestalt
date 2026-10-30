# Task 14 - 將 imp-app 的 reverse 抽成 gen-rsdc-code skill，由 imp-app reverse 呼叫

**Status**：完成——2026-10-12 第 1、2、3 期與 twin 交給 `chinese` 都已完成；4 個 owner skill 的 design pair 的對齊移到 Task 30，另兩件要等時機的事記在下方「結案時沒做的」。
**Raised**：2026-10-10，使用者提出。
**Depends on**：[[Task 10]]、[[Task 12]]、[[Task 17]]

## 1. 背景

提議：把 imp-app `reverse` 裡「從程式碼寫出 RSDC」的部分抽成一個新的 skill `gen-rsdc-code`；imp-app 的 `reverse` 改成呼叫它，自己只留 app 生命週期的部分。

**reverse 現在做什麼**（[imp-app 的 SKILL.md](../.github/common/skills/imp-app/SKILL.md)，2026-10-10 讀取）：

- **Step 0（只有 reverse）**：用 dependency checker 確認 `RSDC-App-tmp.md` 跟上 RSDC standard（版本與指紋），不符就停。
- **Step 2「Reverse-engineer the Documents」**（沒有腳本，全是判斷）：
  1. 從 YAML checkpoint 讀回 app dir、app name 與 prompt log（vibe 回合的紀錄；adopted 的 app dir 沒有）。
  2. 由上而下讀整份原始碼（`server.js`、`app.js`、`public\`、`scripts\`、app config、`tests\`），劃出 components：各有一件事、說出邊界。
  3. 以程式碼為準，不以 prompt log 為準；兩者不一致記成 finding。
  4. 寫 design pair——`{appDir}\docs\{app name}-RSDC.md` 與 tw，同一次執行、逐節對應：照 `RSDC-App-tmp.md` 的節；每個 component 一列 acceptance；回答 Presentation Contract 的八個問題；capability coverage 表與兩種檢查；存檔前對照標準；寫下 vibe 回合學到的規則與教訓；文件不提 skill、command 或工具。
  5. 啟動 app、開瀏覽器讀 live DOM，依 `Wireframe-tmp.md` 寫 wireframe pair（`Wireframe.md` 與 tw）；掃描到的缺陷同時寫進 design pair 的 Defects。
  6. 在 lifecycle record 追加 `reverse`（第一次 reverse 關閉 vibe）。
  7. YAML checkpoint `step_2`；MD report 的 Documents 一節（components 表、findings 表）。

**還有第二份 reverse**：[gen-imp-app](../.github/common/skills/gen-imp-app/SKILL.md) 的 Step 3「Reverse-engineer the app into imp-{app}」做的是同一件事——讀整份原始碼、劃 components、寫 design pair 與 wireframe pair，只是寫進 owner skill 的 `references\`。
兩份已經分岔：gen-imp-app 不用 `RSDC-App-tmp.md`，四章的內容寫在 step 裡；掃描到的缺陷寫進 Specification，而 imp-app 與標準都放在第 4 章的 Defects。
抽成一個 skill，兩邊都可以呼叫它，分岔就不會再擴大。

**評估**（2026-10-10）：值得做——兩份 reverse 不只重複，而且已經分岔，分岔得比上面寫的還嚴重。
上面的事實都核對過，另外補三點：

- **分岔比寫的嚴重**：InvestForge 有 4 個由 gen-imp-app 產生的 owner skill（imp-inv-ctl、imp-inv-database、imp-inv-fin-sight、imp-inv-tech-rank），design pair 共約 3,000 行（另有 tw），用的都是 gen-imp-app 的舊形狀。
  例如 InvFinSight-RSDC 有「1.1 The problem」「1.5 Out of scope」「2.10 Known defects」，還有 2.2.1 這種節以下的編號，而標準規定節以下不再編號。
  gen-imp-app 若改呼叫新 skill，之後的 owner skill 會是標準形狀，現有 4 個則留在舊形狀；owner skill 沒有 reverse 可以重推，要對齊只能手動改。
- **範本是 imp-app 其他 step 的契約**：update（Step 3）依 design pair 的節修改內容、維護 acceptance 列；test（Step 4）依 wireframe pair 逐項比對頁面。
  範本移到新 skill 之後，imp-app 是依賴它的上層；Task 12 若改了 4.5 的表頭之類，imp-app 的 update 與 test 也要跟著改。
- **呼叫的介面有現成前例**：`chinese` 就是被其他 skill 呼叫的 skill——不寫 MD report 也不寫 YAML checkpoint，產出就是它寫的檔案，最後跑自己的檢查。
  新 skill 照這個模式：只寫 design pair，最後檢查，印出摘要（components、findings、defects、acceptance 列），由 imp-app 記進自己的 `step_2` 與 MD report；imp-app 的 checkpoint 與報告格式都不必改。

對「要決定的」六點的建議：

1. **wireframe**：留在呼叫者。
   它是 imp-app test 與 update 的另一份契約，又要啟動 app、開瀏覽器；gen-imp-app 那份重複先接受，需要時再另抽。
2. **通用或 app 專用**：先做 app 專用。
   名稱建議改成 `gen-rsdc-app`——和 `RSDC-App-tmp` 對得上，也不會和同樣「從程式碼寫 RSDC」的 gen-rsdc-skill 混淆。
   名稱由使用者決定。
3. **gen-rsdc-skill**：先分開。
   它面對的是 skill 執行的 CLI 程式，有自己的劃界步驟與 RSDC Checker，和 app 的 Node + Python 架構不同；等 Task 12 之後再看哪些規則可以共用。
4. **介面**：照 `chinese` 的模式。
   輸入用 prompt 的幾行：原始碼目錄、文件寫到哪、文件名稱，以及可選的「要求紀錄」（imp-app 傳 prompt log）。
   新 skill 不提 imp-app，也不提 lifecycle。
5. **範本**：`RSDC-App-tmp.md`（與 tw）連同它對標準的檢查一起移到新 skill；`chinese`、check-md-deps 範例裡的路徑，以及 imp-app 的引用跟著改。
6. **twin**：最終交給 `chinese`，和 gen-rsdc-skill 一致；但要先做 Task 10，否則 RSDC twin 逐行對齊之類的專用規則沒有人負責。
   在那之前，暫時維持同一次執行寫兩份。

## 2. 現況

### 做了什麼

**第 1 期做了什麼**（2026-10-10，名稱用 `gen-rsdc-app`）：

- **新 skill** [gen-rsdc-app](../.github/common/skills/gen-rsdc-app/SKILL.md)（與 tw），照 SKILL template 的節：
  - Step 0 - Warmup：依位置解析 prompt 的四行——app dir、app name、output dir、requirements record（或 `none`）；檢查 design template 跟上 RSDC standard（版本號與 `depends_on.py check`，原本 imp-app Step 0 那一段）。
  - Step 1 - Derive the Design Pair from the Source：imp-app Step 2 裡 design pair 的部分原樣搬過來——讀整份原始碼、劃 components、以程式碼為準、寫 design pair 的七條規則；最後交回 Components 表、Findings 表與缺陷，欄位就是 imp-app MD report 用的那幾欄。
  - 介面照 `chinese` 的模式：不寫 MD report、不寫 YAML checkpoint；沒有 `run step N`；不提呼叫它的 skill。
    只改了用詞：prompt log 改稱 requirements record，"test 與 update 將會擁有" 改成 "這個 app 將會擁有"，"vibe 輪次學到的規則" 改成 "requirements record 顯示是辛苦學到的規則"。
  - 新增一條：output dir 裡已經有的 design pair 會被整份取代，能不能取代由執行它的一方決定（imp-app 由 lifecycle 的閘門決定）。
- **範本**：`RSDC-App-tmp.md` 與 tw 用 `git mv` 移到 `gen-rsdc-app/assets/`；範本區塊裡的 "`reverse` fills every placeholder" 改成 "Every placeholder is filled"，範本不再提 imp-app 的 command。
- **imp-app**（EN 與 tw）：Step 2 改成以 `/gen-rsdc-app` 寫 design pair（傳入 app dir、app name、`{appDir}\docs`、prompt log 或 `none`），範本落後時跟著停；wireframe 掃描、lifecycle record、checkpoint 與 MD report 不變。
  Step 0 拿掉 reverse 的範本檢查與 `step_0` 裡對應的欄位；字彙表與 CONFIGURATION 加上 **gen-rsdc-app**、改 document templates 的路徑、拿掉不再用到的 dependency checker。
- **引用範本路徑的地方**：`chinese` 與 check-md-deps 的 Prompt Examples（各兩份），以及 tasks.md 裡 4 個連結。
- **驗證**：
  - check-skill 的掃描：gen-rsdc-app 的 frontmatter（description 934 字元）、八個必要標題、Dataflow 都沒有問題（沒有多寫入者、沒有來源不明的資料、沒有往回讀）；imp-app 照常。
  - `check_parity.py`：gen-rsdc-app、imp-app、chinese、check-md-deps 都是 0 failure；`scan_source.py` 兩個 SKILL 都 valid。
  - 範本在新位置：`depends_on.py check` 全部 UNCHANGED，`check_rsdc.py --standard --template` PASS。
  - 在 InvestForge（imp-app 實際執行的 workspace）照 gen-rsdc-app 的 Step 0 實際走過一次：config 解析、五個檔案、InvCov 的四行輸入（output dir 指向 scratch）、範本檢查都通過。

**沒有做的實測**（第 1 期當時；2026-10-10 已依下方「實測」補做）：計畫中的「在現有的 app dir 上跑一次 reverse，比對產出與原本的 design pair」沒有做。
InvestForge 的三個 app（InvCov、InvDataflow、InvIndexAnalyzer）都已經 `update` 過，imp-app 的 reverse 會被閘門擋下；它們的 design pair 也都帶著 update 加進去的決定，重新推導出來的版本本來就會不同，比對看不出搬移有沒有出錯。
Step 1 的內容是原樣搬移，風險主要在介面，而介面已在 Step 0 實測。
要完整驗證，可以讓 gen-rsdc-app 對 InvCov（約 1,900 行）寫一份 design pair 到 scratch，與現有的那份並列給使用者看——要使用者決定要不要花這個成本。

**實測：對 InvCov 跑一次 gen-rsdc-app**（2026-10-10，使用者要求）：上一段提出的做法已經做了。
InvCov 已經 `update` 過，所以不經 imp-app，直接照 gen-rsdc-app 的 Step 0 與 Step 1 執行；output dir 是那個 session 的 scratchpad（暫存，session 結束後可能就不在了），沒有寫進 `InvCov/docs`，也沒有啟動 app 或跑它的測試。

- **產出**：`InvCov-RSDC.md` 與 tw，各 534 行。
  32 個標題（文件標題、4 章、23 節、2.2 的 4 個子節）與範本一致；`check_parity.py --keep` 0 failure、0 warning；檔頭引用區 `depends_on.py check` 全部 UNCHANGED；沒有往後引用，各章也沒有越界的字（第 1 章沒有識別碼與技術名詞、第 2 章沒有 component 名稱、第 3 章沒有函式庫名稱）。
- **劃出的 components**：Server（`server.js`）、Handler（`app.js`）、Kernel（`scripts/kernel.py`）、Page（`public/` 的三個檔案），和現有的那份相同。
  4.5 裡 Server 與 Page 是 not verified（沒有測試載入它們）；Handler 由 12 個 node:test 涵蓋，Kernel 由 35 個 unittest 涵蓋。
- **和現有 design pair 相同的結果**：只讀原始碼就找到 D1/D2（兩個計數共用「配對點」）、D5（開在自己停用的配對方式上）、D6（`bLeads` 的軸標反了）、D7（`/healthz` 回報配置的 port）。
  D5 當初是靠掃描真實頁面才找到的。
- **新找到的**：
  - `bLeads` 畫出的迴歸線是錯的那一條：kernel 把點轉置到畫面的軸上，卻沒有轉置 `fit`，斜率差了兩個 instrument 變異數的比值；自我比較時幾乎看不出來。
  - D7 不只 port：以 `--host 0.0.0.0` 啟動時，`/healthz` 回報 `127.0.0.1`。
  - request 缺 `begin`、`end` 或 `rollingWindow` 時，kernel 以今天、`defaultDays`、60 代替而不拒絕，違反範本 4.1 在 261010 新加的「輸入值沒有預設值」；清空窗口欄位會送出 0，結果拿到 60。
  - body 為 JSON `null` 時 handler 拋出例外，回 500 而不是 400。
  - 三處會通過、卻沒有證明它聲稱之事的測試：bar 日期的測試用 UTC 01:00（台北同一天 09:00），拿掉時差也會通過；證明「交進來的價格會被丟掉」的測試，不論價格有沒有被丟掉都會通過；64 KiB 上限沒有測試，而程式在回答之前就 destroy 了 request，400 可能送不到真正的 caller。
- **新版沒有的**：真實頁面上觀察到的數字——gen-rsdc-app 不開頁面，那是 imp-app 的 wireframe 掃描。
  D3（拒絕訊息是英文）與 D4（`start.cmd` 只能在 Windows 用）記成事實（2.8 第 7 題、3.4），不是缺陷，因為沒有第 2 章的規則說它們錯；D8（標籤都寫「指數」）放在 3.2，因為標準說標籤措辭不屬於第 2 章。
- **現有的 design pair**：還是舊版範本的形狀（26 個標題、Defects 在 2.9、沒有 DFD、沒有檔頭引用區，`depends_on.py` 回報 NO_RECORD），4.2 的測試數量也過時了（寫 11 與 33，現在是 12 與 35）。

**實測發現的範本與 skill 問題**（留給第 2 期與 Task 12）：

1. **範本的 2.8 沒有放「使用者必須能夠……」的地方**：3.2 的 capability coverage 要對照 2.8 的每一條授予規則，但範本的 2.8 只有八個問題的表。
   這次把規則放在 2.8 的開頭句與八個問題之間；範本應該補一個 placeholder。
   **2026-10-12**：Task 12 對齊後的範本已解決——3.4 的每一列，對應 2.7 第 2 題裡使用者自己能啟動的一個流程。
2. **3.4 要列出每一個檔案，其中有 `.imp-app.json`**：檔名本身就點出 caller，和「文件不提呼叫它的 skill」有衝突。
   這次以中性的描述保留；要決定列或不列。
   **2026-10-12**：還沒決定；重跑 InvCov 時照樣以中性的描述保留。
3. **4.5 每個 component 只有一列**：not verified 的子項只能塞進同一格，格子很長。
   要不要讓一個 component 可以有多列，跟 Task 12 一起看。
   **2026-10-12**：Task 12 已解決——4.5 改成每列一個主張。

**2026-10-12 做了什麼**（使用者要求三項都做；每項做完各 commit 一次）：

- **twin 交給 `chinese`**（`eaebd95`）：
  - gen-rsdc-app 的 Step 1 只寫英文半邊、記下範本、以 RSDC Checker 檢查英文半邊；新增 Step 2 - Have chinese Write the Twin，執行 `/chinese`：twin 逐行寫出，共用句子照範本 twin 抄，由 chinese 的 parity check 證明——Task 10 已把成對檢查搬進 `check_parity.py`——並照常問要不要 commit。
  - 拿掉不再用到的 keep-English list 設定，加上 **chinese skill**；Dataflow、Steps at a Glance 與 MUST FOLLOW 跟著改，description 精簡到 988 字元。
  - imp-app 只改描述：字彙表、Step 2 讀回的內容，以及把 chinese 的 commit 問題轉給使用者；`check_rsdc.py` 的 docstring 跟著改。
  - 兩份 SKILL-tw.md 照 chinese 的 INCREMENTAL 更新：`check_parity.py` 0 failure，`diff_md.py --verify` 通過，警告與改動前相同。
- **用新流程重跑 InvCov**（輸出在那個 session 的 scratchpad，沒有 commit）：
  - Step 0 通過：標準與範本都是 261010，範本指紋 UNCHANGED；InvCov 的原始碼自 09-25 起沒改過。
  - 英文半邊照現行範本寫成，703 行、47 個標題；RSDC Checker PASS（26 項），3 則警告留著並有理由——2.10 的目標表引用同一節的規則、範本那一行的「Python 3.7」被讀成章節引用、這個 app 不寫 record，所以 DFD 沒有藍線。
  - twin 由 chinese 的流程寫出（FULL，93 行照範本 twin 抄）：parity 0 failure、0 warning；RSDC Checker 的成對檢查也 PASS（14 項）。
  - 依現行範本多了一項缺陷：App config 缺少的欄位被程式碼補上，而不是回報（2.5 規定要回報）；其餘結果與 10-10 的實測相同。
  - 寫到 scratch 時，`depends_on.py record` 要多給 `--root`，因為 scratch 不在任何 vault 裡；寫進 InvestForge 時不需要。
- **第 3 期**（SkillsGestalt 與這段紀錄同一個 commit；InvestForge `34a7d4b`）：
  - gen-imp-app 的 Step 3 先把 prompt log 寫成 Checkpoint Dir 裡的 `prompt-log.md`，再以 `/gen-rsdc-app` 寫 design pair，output dir 是 owner skill 的 `references\`；components 取自它交回的結果；wireframe 掃描到的缺陷改寫進 design pair 的 Defects，不再寫進 Specification。
    字彙表、CONFIGURATION、Step 0、MUST FOLLOW、checkpoint 的欄位（多了 `promptLogFile` 與 `findings`）與 MD report 的 Notes 跟著改；check-skill 的掃描結果與改動前相同（description 1148 字元超過上限、`build_app.py` 等 leftovers，原本就有）。
  - 4 個 owner skill 的 design pair 決定先不動，仍是 gen-imp-app 的舊形狀；結案時移到 Task 30。
  - 兩份 twin 的已知缺陷已修正：InvDatabase 的 4 個 placeholder；InvFinSight 的 inline code、`date`、`holdings.suffixes` 與 41 處 §。
    兩份仍未通過的是逐行版面（兩份都不是與英文逐行對應），以及 InvFinSight 3 個被翻成中文的 fenced block，等這兩份 design pair 對齊時處理。

## 3. 要做的

**可能的分工**（待決定）：

- **gen-rsdc-code**：讀原始碼、劃 components、寫 design pair、對照標準，交回 components、findings、defects 與 acceptance rows；擁有範本，以及範本對標準的檢查（現在 imp-app Step 0 那一段）。
- **imp-app reverse**：lifecycle 的門（reverse 只能在第一次 update 之前）、交給 gen-rsdc-code 的輸入（app dir、app name、prompt log、是不是 adopted、文件寫到哪裡）、lifecycle record、YAML checkpoint 與 MD report、說明下一步（test 或 update）。
- **單向依賴**：imp-app 與 gen-imp-app 是上層，gen-rsdc-code 是下層；gen-rsdc-code 與它寫出的文件都不提呼叫它的 skill、command 或 lifecycle（imp-app 現在的 MUST FOLLOW 已經這樣要求文件）。

**要決定的**：

1. **wireframe 跟不跟過去**：名稱是 rsdc，但 reverse 也寫 wireframe pair，而且那要啟動 app、開瀏覽器讀 live DOM，是網頁專屬的工作。
   選項：(a) 只抽 design pair，wireframe 留在 imp-app；(b) 一起抽，名稱可能要改；(c) wireframe 另成一個 skill。
2. **通用或 app 專用**：`gen-rsdc-code` 聽起來適用任何程式碼，但現在的做法與範本都是 app 專屬的（Node server 加 Python kernel、HTTP API、Mountable Handler、`server.js`／`app.js`／`public\` 的讀法）。
   選項：(a) app 專用；(b) 通用，由呼叫者指定範本與要讀哪些檔——要先分出哪些規則是通用的。
3. **和 gen-rsdc-skill 的分界**：gen-rsdc-skill 也是從程式碼與資料寫 RSDC（delimitation、每個事實取自程式碼與資料、Verification Obligations 以觀察為準、RSDC Checker）。
   若 gen-rsdc-code 是通用的，gen-rsdc-skill 寫 RSDC 的那幾步可能也改呼叫它，或兩者共用規則；若不是，要寫清楚兩者的分界。
   這也連到 Task 12（兩份範本對齊）。
4. **呼叫的介面**：照 repo 的慣例，在 step 裡執行 `/gen-rsdc-code …`（gen-skill、gen-rsdc-skill 呼叫 `chinese` 都是這樣）。
   要定的是輸入有哪些，以及 gen-rsdc-code 交回什麼、用什麼形式，讓 imp-app 的 checkpoint 與 MD report 讀得到——它自己的 YAML checkpoint，還是固定格式的輸出。
5. **範本與檢查放哪裡**：`RSDC-App-tmp.md`（與 tw）、可能還有 `Wireframe-tmp.md`，是否移到 gen-rsdc-code 的 `assets\`；範本對標準的指紋檢查跟著移。
   Task 12 丙的「RSDC Checker 支援 app 的 RSDC」若要做，gen-rsdc-code 是自然的位置，也可以在這裡補上 app 的 RSDC 現在沒有的機械檢查。
   （2026-10-11 已由 [[Task 17]] 做完：RSDC Checker 也能檢查 app 的 RSDC，gen-rsdc-app 寫完 design pair 後執行它。）
6. **twin 由誰寫**：reverse 現在同一次執行寫 EN 與 tw；gen-rsdc-skill 則交給 `chinese` skill。
   gen-rsdc-code 要採哪一種（與 Task 10「讓 chinese skill 承接 RSDC twin 的專用規則」有關）。

**牽涉的檔案**：

- **新 skill**：`.github/common/skills/gen-rsdc-code/`——`SKILL.md` 與 tw（用 gen-skill 建立、check-skill 檢查），可能還有 `assets\` 與 `scripts\`。
- **imp-app**：`SKILL.md` 與 tw 的字彙表（reverse、app documents、design pair、document templates、dependency checker）、CONFIGURATION、MUST FOLLOW 中關於 reverse 與文件的規則、Step 0 的範本檢查、Step 2 整段、Prompt Examples；`assets\` 的範本可能移走。
- **gen-imp-app**：`SKILL.md` 的 Step 3（若也改呼叫 gen-rsdc-code）。
- **引用範本路徑的地方**：`chinese` skill 的 `SKILL.md` 與 tw（以 `RSDC-App-tmp.md` 為例）、[check-md-deps](../.github/common/skills/check-md-deps/SKILL.md) 的 Prompt Examples（用 `.github/common/skills/imp-app/assets/RSDC-App-tmp.md`）、這份 tasks.md 的 Task 12。
- **已寫好的 app 文件**：格式不變，不必改；之後的 reverse 改由新 skill 寫。

**暫時的傾向**（尚未決定，2026-10-10 依評估修正）：先只抽 design pair，app 專用，第 1 期只有 imp-app 改呼叫它；gen-imp-app 等第 3 期，先決定現有 owner skill 的 design pair 怎麼處理；wireframe 留在呼叫者；範本與它對標準的檢查跟著新 skill 走。
是否推廣成通用、是否讓 gen-rsdc-skill 也呼叫它，等 Task 12 的範本對齊之後再決定。

建議分期：

- **第 1 期**：建立新 skill，把 imp-app Step 2 的 design pair 部分與範本原樣搬過去，內容不改；imp-app 改成呼叫它。
  驗證：在一個現有的 app dir 上跑一次 reverse，比對產出與原本的 design pair。
- **第 2 期**：在新位置做 Task 12 的範本對齊，只要改一處。
  **2026-10-11**：已由 [[Task 12]] 做完。
- **第 3 期**：gen-imp-app 改成呼叫新 skill，並決定現有 4 個 owner skill 的 design pair 要不要手動對齊。
  **2026-10-12**：gen-imp-app 已改成呼叫 gen-rsdc-app；4 個 owner skill 的 design pair 決定先不動，結案時移到 Task 30。
  - **owner skill 的 RSDC twin 已知的缺陷**（[[Task 10]] 第 4 點，2026-10-11）：`check_parity.py` 新的檢查在 InvDatabase-RSDC-tw（2.14 的 `{holding name}`、`{anything}` 被譯成中文）與 InvFinSight-RSDC-tw（多處 inline code 被譯成中文、少了 `date`、多了 `holdings.suffixes`，章節引用加了 §）找到缺陷；處理這兩份 design pair 時一併修正。
    **2026-10-12**：已修正（InvestForge `34a7d4b`）。
- **twin 交給 `chinese`**：等 Task 10。
  **2026-10-11**：Task 10 已完成——chinese 會照範本 twin 抄共用句子，`check_parity.py` 也涵蓋了成對檢查，twin 可以交給 chinese 了。
  **2026-10-12**：已完成（`eaebd95`）。

工作量：主要是搬移說明文字，沒有程式；但驗證只能實際跑一次 reverse（讀整份原始碼、啟動 app），而 design pair 目前沒有機械檢查（Task 12 丙），只能靠人讀。

**待使用者決定**：要不要用這份取代 `InvCov/docs` 現有的 design pair。
gen-rsdc-app 本身不擋，由呼叫的一方決定；取代之後，imp-app 的 update 改的就是新範本形狀的文件。
scratch 裡的檔案是暫存，要保留得先複製出來。
**2026-10-11**：scratch 那份是 [[Task 12]] 對齊範本之前的形狀；要取代，請在 [[Task 17]] 之後重新產生。
**2026-10-12**：已依現行範本重新產生一份，寫在那個 session 的 scratchpad（見下方「2026-10-12 做了什麼」），還沒寫進 `InvCov/docs`。
**2026-10-12**：已由 [[Task 18]] 處理：InvestForge `1357e12` 以 gen-rsdc-app 重跑的稿為底，對齊了 `InvCov/docs` 的 design pair。

**結案時沒做的**（2026-10-12）：

- **imp-app 的 Step 2 與 gen-imp-app 新的 Step 3 都還沒實際走過。**
  兩者都要等時機：imp-app 要一個還在 vibe 階段的 app dir，gen-imp-app 要下一個以它建立的 app。
  走過時，對照 gen-rsdc-app 交回的內容，以及兩者寫進 checkpoint 與 MD report 的欄位。
- **3.3 要不要列出 `.imp-app.json` 還沒決定。**
  檔名本身點出了 caller，和「文件不提呼叫它的 skill」有衝突；兩次重跑都以中性的描述保留，Task 18 對齊後的 InvCov 也照樣保留。
- **4 個 owner skill 的 design pair**：移到 Task 30。

## 4. 驗證

**還沒有驗證的**：imp-app 的 Step 2 實際呼叫 gen-rsdc-app 走完一次——InvestForge 的三個 app 都過了 `update`，reverse 會被閘門擋下，要等一個還在 vibe 階段的 app dir。
**2026-10-11**：imp-app 的實際呼叫等 [[Task 17]] 之後再驗。
**2026-10-12**：Task 17 已完成；gen-imp-app 新的 Step 3 同樣還沒實際走過，要等下一個以 gen-imp-app 建立的 app。

## 5. 與其他 task 的關係

—

## 6. 日誌

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。
- 指向 Task 30 的 wikilink 改成純文字：它已移出本 workspace（[[Task 62.4]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-12

- 第 2、3 期完成：Task 12 對齊範本、gen-imp-app 改呼叫 gen-rsdc-app。
- twin 交給 chinese，並用新流程重跑 InvCov。
- 結案：第 1、2、3 期與 twin 交給 chinese 都完成，4 個 owner skill 的 design pair 移到 Task 30。

### 2026-10-11

- Task 12 與 Task 17 完成，第 2 期的範本對齊與 RSDC Checker 支援 app 的 RSDC 都已做完。
- Task 10 完成，twin 可以交給 chinese。

### 2026-10-10

- 提出：把 imp-app reverse 裡寫 RSDC 的部分抽成新 skill。
- 評估後決定名稱用 gen-rsdc-app，先只抽 design pair、app 專用。
- 第 1 期完成：建立 gen-rsdc-app，imp-app 改呼叫它，並對 InvCov 實測一次。
