---
name: imp-home
description: >-
  在 prompt 指名的 target 目錄裡，帶著一個 hub app 走完五個 command 的 lifecycle。一個 hub 是一個 Node
  伺服器（`node server.js`），提供單一一頁按鈕，它的 link list 每有一筆就是一顆，以及一份承載它們的
  `app.config.json`。prompt 的第二行是 `target`、第三行是 `command`：`setup` 一次性地建立 target frame
  與它的 `app.config.json`，並以 command 下一行所指名的 hub 為它播種，因此一個 target 不必叫得跟它的
  seed 一樣；`gen` **依據這個 skill 的 references 裡的設計**寫出這個 app——一份 RSDC
  文件與一份 wireframe，各有英文與繁體中文——然後把那同一批文件複製進 target，於是一個 hub 永遠不會只有
  程式碼、卻沒有它被產生時所依據的設計；`update` 接著先改那份設計、後改程式碼，於是文件永遠不會落後於
  它所描述的那個東西。`gen` 與 `update` 都不會提供它們寫出來的東西——寫與驗證是分開被要求的，
  因此一次疊代不必被收取一道沒有人現在想要的審閱的代價，而一次執行也絕不會暗示它檢查了它實際沒有
  檢查的東西。`run` 啟動已經在那裡的東西，並在它有回應時停下，給想要**使用**這個 hub 的人；
  `test` 提供它並像讀者那樣讀它，給想知道它**是不是對的**人。兩者都不改變任何事物。這個順序是
  單向的：第一次 `update` 會為那個 target 永久關閉 `setup` 與 `gen`，而那正是讓一個已經開始分岔的 hub，
  不會被悄悄重新產生回 seed 的原因。從 `setup` 開始，target 就擁有它的程式碼與它的設計——references
  是 seed，不是母版——因此兩個 hub 可以正當地分岔。一筆項目可以被 MOUNTED，這會讓 hub 在自己來源的
  某個路徑下親自提供那個 app，而不是連出去到另一個 port：它會 require 那個 app dir 的 `app.js`、
  在啟動時呼叫它的 `createApp()` 一次、剝掉 prefix 然後委派。一個 mount 由一筆 REGISTRY 條目指名——該 skill 只組裝一個 app 時是那個 skill，組裝許多時則是 app 自己、
  並透過一份登錄表解析，而一個準備不起來的 mount 只在它自己的 prefix 上失效，別處都不受影響。按鈕是由
  **伺服器**在請求當下渲染的，這正是讓頁面能夠不帶 JavaScript、且每一個 label 與 URL 在成為 markup
  之前都被跳脫的原因。
---

本文件為 [SKILL.md](.github/common/skills/imp-home/SKILL.md) 的繁體中文版；真正會執行的是 SKILL.md，任一份改了某節，另一份必須在同一次執行中、以相同編號一起改。

# TERMINOLOGY

每一個 skill 裡都指同一件事的 term。

- **`run step N`** — 一個放在 prompt 結尾、指名某一個步驟的選擇子。
  它**只**執行那一個步驟，並從 YAML checkpoint 把先前每一個步驟的輸出讀回來。
- **Checkpoint Dir** — 存放某個 skill 的 YAML checkpoint 的每次執行專屬目錄。
  每個 skill 都有自己的；這個 skill 的寫在 **CONFIGURATION** 底下。
- **YAML checkpoint** — Checkpoint Dir 裡的 `process.yaml`。
  每個步驟都把自己的輸出寫在 `step_{N}` 群組底下，於是後面的步驟是把它們讀回來，而不是重算一次。
- **MD report** — 這個 skill 寫進 wiki vault 的 Markdown 報告，放在一個以該 skill 命名的資料夾裡，在結果各節之上帶著標準表頭（Skill、Checkpoint、Created、Updated、Prompt）。
- **no forward-reference** — 一個步驟絕不得依賴排在它後面的步驟的規則。
  指名某個較後面的步驟來安排流程走向並不違反它；借用那個步驟的輸出才違反。

# DEDICATED TERMINOLOGY

這個 skill 領域專屬的 term。
定義由詞彙表擁有——步驟使用 term，而不是把它的意思重述一遍。

- **target** — prompt 在第二行指名的目錄，例如 `artifacts/bios-home`，相對於工作區根目錄。
  它是一個 hub 所在的地方，而從 **setup** 開始，它就是那個 hub 的**源頭**，不是一個 build product。
- **command** — prompt 第三行的那個字：**setup**、**gen**、**update**、**test** 或 **run**。
  每次執行恰好一個，並由它決定哪些步驟會執行。
- **lifecycle** — 單向的順序 `setup` → `gen` → `update`，而 **test** 與 **run** 在有程式碼之後的任何時點都可用。
  **update** 是那道只朝一個方向開的門：它一旦跑過，**setup** 與 **gen** 就對那個 target 永遠關閉。
- **lifecycle record** — `{target}\.imp-home.json`，承載 **phase**，以及一份針對這個 **target** 執行過的每一個 **command** 及其時間戳的 `history`。
  它住在 **target** 裡而不是某個 checkpoint 裡，因為 **lifecycle** 橫跨多次工作階段，而一個每次執行專屬的檔案會把它忘掉。
  app 從不讀它。
- **phase** — **lifecycle record** 所承載的、最後一個改變狀態的 **command**：`setup`、`gen` 或 `update`。
  **run** 什麼都不改，所以從不改變它。
- **setup** — 一次性建立 **target frame** 的 **command**。
  它是唯一一個可以對「沒有 **lifecycle record** 的目錄」執行的 **command**。
- **gen** — 依據 **seed documents** 寫出 **target code**、然後把那些文件複製進 **target** 的 **command**。
  它要跑幾次就跑幾次。
- **update** — 修改一個已經產生出來的 **target** 的 **command**：先 **target documents**，後 **target code**，要跑幾次就跑幾次。
- **test** — 提供 **target**、接著像讀者那樣讀它的 **command**，兩半都做。
  它是給想知道這個 hub **是不是對的**的人的，也是唯一一個會去檢視所提供出來的東西的 **command**。
  它不改變 **target** 裡任何東西。
- **run** — 啟動 **target** 裡已經有的東西、確認它有回應、說出它在哪裡，然後停下的 **command**。
  它是給想**使用**這個 hub 的人的，所以與 **test** 不同，除了伺服器有起來之外什麼都不檢查，也完全不做判斷。
  它同樣什麼都不改變。
- **hub name** — 一個 **target** 是從哪一筆 **seed entry** 播種而來。
  **setup** 從 prompt 的第四行取得它並記下來；之後每一個 **command** 都從 **lifecycle record** 把它讀回來。
  它刻意**不**從 **target** 的名字推導，因此一筆 seed entry 可以為好幾個 target 播種，而一個 target 也可以叫得跟它的 seed 不一樣。
  它同時為這次執行的每一個輸出命名。
- **seed** — 這個 skill 自己的 `server\` 與 `references\`。
  它是一個起點，絕不是母版：一旦某個 **target** 存在，它裡面沒有任何東西還具有權威性。
- **seed documents** — **seed** 的 `references\Home-RSDC.md`、`Home-RSDC-tw.md`、`Wireframe.md` 與 `Wireframe-tw.md`。
  `Home-RSDC.md` 決定一個 hub 必須**做**什麼；`Wireframe.md` 決定它的頁面必須**包含**什麼。
  兩者合起來就是 **gen** 據以產生的東西。
- **seed entry** — **skill config** 的 `homes.{hub name}` 區塊：port、標題，以及起始的 **link list**。
  **setup** 讀它；**setup** 之後就沒有任何東西讀它，因為到那時候 **app config** 已經擁有那些值。
- **skill config** — 這個 skill 根目錄下的 `config.yaml`，承載 `homes` 與 **app registry**。
  只有 **setup tool** 讀它。
- **app registry** — **skill config** 的 `apps` 鍵：一個 **registry name** 對應到該 app 的 `appDir`、擁有它的 `skill`，以及它預設的 `label`、`href` 與 `note`。
  它就是讓 prompt 能以擁有者 skill 而不是以路徑來指名一個 **mount source** 的東西。
- **mount source** — prompt 的 `mounts:` 那一行上的一個 **registry name**。
  透過 **app registry** 解析它，是這個 skill 得知另一個 app 被組裝在哪裡的唯一途徑。
- **registry name** — **app registry** 條目的鍵，也是 `mounts:` 那一行唯一能寫的東西。
  一個只組裝**一個** app 的 skill，以**它自己**為名；一個組裝**許多** app 的 skill——每指向一個目錄就造出一個不同的 app——沒有單一的 app dir 可以拿來命名，因此它的每一個 app 改以 **app 自己**為名。
  名稱屬於哪一種，不影響它如何被解析：兩者都抵達同一筆經過審閱的條目。
- **owner skill** — 一筆 registry 條目的 `skill`：當那個 app 需要被建置或修復時，該去跑的是誰。
  它寫在每一筆條目上，而不是從鍵推斷出來——因為一個「是 app 名稱」的鍵若被拿來推斷，會指名一個根本不存在的 skill。
- **target frame** — **setup** 所寫出來的東西：**target** 目錄、它的 `public\`、**app config**、`start.cmd`、`README.txt` 與 **lifecycle record**。
  它不帶 `server.js`——一個框架還不是一個 app。
- **target code** — **target** 的 `server.js` 與 `public\app.css`，由 **gen** 寫出，之後由 **update** 修改。
- **target documents** — **target** 的 `docs\Home-RSDC.md`、`docs\Home-RSDC-tw.md`、`docs\Wireframe.md` 與 `docs\Wireframe-tw.md`：**gen** 留下的那份副本。
  從那時起，決定**這個** hub 必須是什麼的是它們，不是 **seed documents**。
- **RSDC standard** — `Home-RSDC.md` 所依循的章節職責規則：四個部分各自回答哪個問題、各自不得向前觸及什麼。
  一項變更該落在 **target documents** 的哪裡，以它為準。
- **app config** — **target** 的 `server.js` 旁邊那份 `app.config.json`。
  這個 app **唯一**會讀的檔案，也正是讓那個資料夾能被整份搬走的原因。
- **link entry** — **link list** 的一筆項目：一個 `label`、一個 `href`，以及選填的 `note`。
  它在清單裡的順序就是它在頁面上的順序。
- **link list** — **app config** 的 `links`。
  沒有別的東西決定有哪些按鈕存在。
- **dead link** — 一筆 **link entry**，其 scheme 是頁面無法 navigate 過去的，今天指的就是 `file://`。
  它被渲染得**跟其他每一顆按鈕一模一樣**；那個事實由 `/healthz` 回報，絕不出現在頁面上。
- **mount** — 一筆帶有 `mount` 欄位的 **link entry**，這會讓 hub 親自提供那個 app，而不是連出去到它。
  它的 `href` 於是是一個位於 hub 自己 origin 上的路徑，而那個路徑就是 **mount prefix**。
- **mount prefix** — 一個 **mount** 所回應的路徑，取自它的 `href` 並去掉結尾斜線。
  hub 在委派之前會把它從請求裡剝掉，因此 **mounted app** 只看到它被寫來回答的那個路徑。
- **mounted app** — 一個 **mount** 所指向的 app，透過 require 它目錄裡的 `app.js` 並呼叫它匯出的 `createApp(options)` 來抵達。
  它屬於**另一個 skill**：這一個只載入它，從不建置它、啟動它或修好它。
- **setup tool** — `setup_target.py`，這個 skill 自己的工具，而且只屬於 **setup**。
  **setup** 之後的每一個 **command** 都是就地修改 **target**，所以其他任何一個都不得呼叫它。

# CONFIGURATION

這個 skill 執行時所用的具體值。
底下每一條路徑都是這個 skill 的常數；關於正在處理的那個 hub 的一切，都是從 prompt 指名的那個 **target** 讀出來的。

- **Checkpoint Dir** — `checkpoints\imp-home\{hub}-{command}-{yymmdd-hhmm}\`。
- **YAML checkpoint** — Checkpoint Dir 裡的 `process.yaml`。
- **MD report** — `{wikiDir}\imp-home\imp-home-{hub}-{command}-{yymmdd-hhmm}.md`，帶著與 Checkpoint Dir 相同的 `{hub}`、`{command}` 與時間戳，其中 `wikiDir` 來自工作區的 [config.yaml](config.yaml)（在 Step 0 解析）——絕不把 wiki 根目錄寫死。
- **seed** — `{skillGroups.common}\skills\imp-home\server\` 與 `{skillGroups.common}\skills\imp-home\references\`。
- **seed documents** — [Home-RSDC.md](.github/common/skills/imp-home/references/Home-RSDC.md)、`Home-RSDC-tw.md`、[Wireframe.md](.github/common/skills/imp-home/references/Wireframe.md) 與 `Wireframe-tw.md`。
- **setup tool** — `{skillGroups.common}\skills\imp-home\setup_target.py`。
- **skill config** — `{skillGroups.common}\skills\imp-home\config.yaml`。
- **target** — 來自 prompt 第二行，相對於工作區根目錄。
  它位於 wiki vault 之外。
- **lifecycle record** — `{target}\.imp-home.json`。
- **target documents** — `{target}\docs\`。
- **RSDC standard** — `{skillGroups.common}\references\RSDC-Standard.md`，其圖的記法在 `{skillGroups.common}\references\DFD.md`。
- **server origin** — `http://127.0.0.1:{port}`，其中 port 是 **app config** 的 `port`。

# MUST FOLLOW

- **設計決定程式碼是什麼，而不是反過來。**
  **gen** 依據 **seed documents** 產生 **target code**，而 **update** 先改 **target documents**、後改 **target code**。
  任何時候都不會先寫程式碼、事後再描述它——那樣產出的設計是逐字稿，對下一位讀者毫無價值。
- **`gen` 要在同一次執行裡，把它據以產生的那些文件複製進 target。**
  沒有設計相伴的程式碼，是沒有人能核對的程式碼；而只留在 seed 裡的設計，會變成之後每一個 hub 都靜默共用的東西。
  如果那次複製沒有發生，那次 **gen** 就沒有完成。
- **lifecycle 是單向的，而第一次 `update` 會把門在身後關上。**
  一旦 **lifecycle record** 帶著一筆 `update`，**setup** 與 **gen** 這兩個 **command** 就對那個 **target** 永遠被拒絕。
  一個已經開始分岔的 hub，不得被一個不知道自己正在覆寫什麼的 command 重新產生回 seed。
  - **這個代價值得說出來。**
    第一次 **update** 之後就沒有「整個重新產生」這條路了：每一項改動，不論多小，都是針對 **target** 自己的檔案做的。
    這是刻意的——重新產生正是 **gen** 的用途，而它可用的期間，恰恰就是這個 hub 還沒有任何屬於自己、會被弄丟的東西的那段時間。
- **`update` 會拒絕比程式碼還舊的文件。**
  如果在 **target documents** 最後一次被改動之後又跑過一次 **gen**，那麼在改任何東西之前先重讀它們：對一份程式碼早已越過的設計做 update，等於把改動寫進一份本來就已經是錯的文件裡。
- **每一份文件都是一對，兩半一起動。**
  `Home-RSDC.md` 裡改了某一節，`Home-RSDC-tw.md` 就在同一次執行中、以同一個編號一起改；wireframe 那一對適用同一條規則。
- **`setup` 每個 target 只跑一次。**
  一個已經帶有 **lifecycle record** 的 **target** 會被拒絕，並指名它正處在哪一個 **phase**、以及接在後面的是哪一個 **command**。
- **`test` 與 `run` 都不改變任何東西。**
  **test** 啟動已經在那裡的東西，接著檢查它、讀它；**run** 啟動它，並在它有回應時停下。
  兩者中任一個發現缺陷時，都是指名那個缺陷然後停下；修它是一次 **gen** 或一次 **update**，看 **phase** 允許哪一個。
- **`gen` 與 `update` 不提供它們寫出來的東西。**
  寫與驗證是分開被要求的，因此一次疊代不必被收取一道沒有人現在想要的審閱的代價。
  因此這兩個 **command** 都要在結尾說出這個 hub **尚未**被執行過，並指名 **test**。
  - **它的代價值得說出來，而且兩者並不相同。**
    一次 **update** 仍然帶著 Step 3 自己的重新證明，在一份拋棄式副本上、用一個備用 port。
    一次 **gen** 什麼都沒帶：它結束時寫出了一個從來沒被啟動過的 `server.js`。
    要明白地說出來，而不是讓一份看起來干淨的報告暗示了相反的事。
- **setup tool 只屬於 `setup`。**
  其他任何 **command** 都不得呼叫它。
  它是從 seed 寫出一個 **target frame**，所以之後再呼叫它，會把這個 **target** 已經長成的樣子整個抹掉。
- **target 擁有它的程式碼與它的設計；seed 只是一個起點。**
  **setup** 之後沒有任何 **command** 會修改 **seed**，而兩個 hub 被允許分岔——那正是讓它們成為兩個 hub、而不是同一個被渲染兩次的原因。
  代價是被接受的：日後對 **seed documents** 的修正不會抵達任何已經產生出來的 target。
- **絕不把某個 hub 寫死。**
  任何 **hub name**、target 路徑、port、標題、標籤或網址，都不得出現在本檔案、**seed** 或 **setup tool** 裡。
  prompt 指名 target，**skill config** 為它提供種子。
- **每次執行一個 target。**
  **command** 恰好套用在一個 **target** 上。
  一次執行絕不處理兩個，而且在 prompt 沒有指名時，也絕不退回去用「唯一的那一個」——它會問。
- **hub name 說的是這個 target 從什麼播種而來，不是它叫什麼。**
  **setup** 從 prompt 取得它並寫進 **lifecycle record**；**target** 目錄可以叫任何名字。
  因此兩個 target 可以從同一筆 **seed entry** 播種——而如果真的這樣做了，兩者都會帶著那一筆的 port，而兩個 hub 不可能同時綁同一個。
  發生時就說出來，而不是留給第二個啟動的那一個去講。
- **每一個 command 都要往 lifecycle record 追加一筆。**
  一個改動了 **target** 卻沒有把自己記下來的 **command**，會讓下一次執行去猜 **phase**，而上面那道閘門，好壞完全取決於它讀到什麼。
- **就照 link list、就照它的順序渲染。**
  絕不新增、刪除、重排或改寫任何一筆 **link entry**，除非那正是 prompt 所要求的改動。
- **在每一個 label、href 與 note 成為 markup 的地方把它跳脫**，兩種引號都算在內。
  一筆 **link entry** 是設定文字，而未經跳脫的設定文字會從它所在的那個屬性裡逃出來。
  這一點是用惡意的值證明出來的，不是假設出來的。
- **一個 dead link 被渲染得跟其他每一顆按鈕一樣，並記在別的地方。**
  hub 無從得知讀者會怎麼打開一個目的地，而一個對某位讀者正確的標記，對下一位就是錯的。
- **頁面不帶 JavaScript。**
  渲染發生在 hub 伺服器裡。
  不要為了「簡化伺服器」而把它搬進瀏覽器——那會多出一個客戶端面要稽核，並讓頁面有可能與設定不一致。
- **app 維持零相依。**
  僅 Node 標準函式庫、一份同源樣式表、無 CDN、無網路字型、無圖片。
  一個 **mount** 不改變這一點：抵達一個 app 靠的是 require 一個檔案，那是語言特性，不是框架。
- **一個 mount 是被載入，不是被啟動，而且絕不在這裡被修好。**
  hub 會 require **mounted app** 的 `app.js` 並呼叫它的工廠；它從不生出行程。
  讓一個 app 變得可掛載，是它自己的 skill 的工作——如果缺了 `app.js`，就指名 registry 為它記載的 **owner skill** 並停下來。
- **一個準備不起來的 mount 不得付出任何其他代價。**
  hub 要啟動、其他每一顆按鈕都要能用，而失敗只在那一個 prefix 上被回應。
- **一個從未被交到 hub 手上的失敗，同樣不得是致命的。**
  一個在後續 tick 才 throw、或是啟動了一個 promise 卻從未回傳它的 **mounted app**，並沒有交給 hub 任何可以接住的東西。
  它會被記錄下來並被撐過去，而且絕不被歸屬到某個 prefix——造成它的那個請求已經不在了。
- **一個 mount 由一筆 registry 條目指名，絕不由打進 prompt 裡的一條路徑指名。**
  prompt 裡的路徑是一段會抵達檔案系統的、未經審閱的輸入；**app registry** 才是那份經過審閱的清單，而一個不在其中的 **mount source** 是一次停下、並說出該補什麼，不是一次猜測。
- **預設最小暴露。**
  除非傳入 `--host`，否則 hub 綁定 loopback；任何更寬的綁定都要對提出要求的人說明白——包含那會連同 hub 一起放寬每一個 **mount**。
- **這個 skill 不啟動別的東西，也不修好別的東西。**
  一顆目標掛掉的按鈕，屬於擁有那個目標的 skill。
  指名它，然後停下來。
- 必須逐步執行工作流程，並顯示每一個步驟編號。
- 每個步驟都必須自足。
  **No forward-reference.**
- **遵守 `run step N` 選擇子**：執行 Step N，然後停下；絕不執行更後面的步驟。
  它與 **run** 這個 command 不同——第三行上單獨的 `run` 是 command，而只有 `run step` 後面接一個數字才是選擇子，一個 prompt 可以同時帶有兩者。
- MD report 的表頭與形狀，遵循 [report-md-rules.md](.github/common/rules/report-md-rules.md)。
- YAML checkpoint 的形狀與必填欄位，遵循 [report-yaml-rules.md](.github/common/rules/report-yaml-rules.md)。
- 一次執行的拋棄式檔案該放哪裡、以及如何清掉，遵循 [scratch-rules.md](.github/common/rules/scratch-rules.md)——那些跳脫探測與掛載探測正是這一類。
- **在這個 skill 結束之前，顯示 server origin、target、MD report 與 YAML checkpoint**——只顯示這四個，並各自渲染成可點擊的 Markdown 連結。
  **server origin** 是一個 `http://` 網址，就以它自己連結，而且只由 **test** 與 **run** 這兩個會啟動伺服器的 **command** 顯示；**setup**、**gen** 與 **update** 則省略它，因為它們沒有留下任何正在執行的東西。
  MD report 位於 vault 裡、在這個工作區之外，所以用 `obsidian://open?vault={vaultName}&file=<vault-relative-path>` URI 連結它（例如 `[imp-home-{hub}-{command}-{yymmdd-hhmm}.md](obsidian://open?vault={vaultName}&file=imp-home/imp-home-{hub}-{command}-{yymmdd-hhmm}.md)`）；**target** 與 YAML checkpoint 則維持工作區相對、使用正斜線的目標（例如 `[process.yaml](checkpoints/imp-home/{hub}-{command}-{yymmdd-hhmm}/process.yaml)`）。
  - 每一次執行都要這樣做，包含像 `run step 0` 這種只跑一部分的執行。

# Prompt Examples

## Prompt 1

```
/imp-home
artifacts/bios-home
setup
bios-home
mounts: imp-bios-logs, imp-bios-logs-search, imp-boot-times
```

## Prompt 2

```
/imp-home
artifacts/bios-home
gen
use black buttons.
```

## Prompt 3

```
/imp-home
artifacts/bios-home
update
use blue buttons, each button display only title.
```

## Prompt 4

```
/imp-home
InvHome
update
mounts: InvDataflow
```

`InvDataflow` 是第二種 **registry name**：這個 app 是由 `imp-app` 組裝的，而 `imp-app` 每被指向一個目錄就造出一個不同的 app，因此沒有單一的 app dir 可以拿來命名。
該條目帶有 `skill: imp-app`，而那正是當那個 app 還沒有 `app.js` 時，hub 會回報的內容。

## Prompt 5

```
/imp-home
artifacts/bios-home
test
```

## Prompt 6

```
/imp-home
artifacts/bios-home
run
```

# Workflow

每個步驟都以一段 **Purpose** 開頭：一句話說明那個步驟為什麼要作為一個步驟存在——把它併進隔壁那一步，這個 skill 會失去什麼。

**command 決定這次執行怎麼走。**
Step 0 永遠執行，也是那道閘門被執行的地方。
Step 1 只在 **setup** 時執行，Step 2 在 **gen**，Step 3 在 **update**；Step 4 只在 **test** 與 **run** 時執行。
在這裡指名那些步驟是流程安排，不是 forward-reference：沒有任何步驟借用較後面步驟的輸出。

**沒有任何一個 command 同時既寫入又提供服務。**
**setup**、**gen** 與 **update** 結束時留下的是磁碟上的檔案，什麼都不啟動；**test** 與 **run** 啟動一個伺服器，什麼都不寫。
那個切分正是讓一次疊代只付出它所改動的成本的原因，也正是讓一次執行不會暗示它檢查了某個它從未看過的東西的原因。
代價是一次 **gen** 可以在它的 `server.js` 從未被啟動過的情況下就結束——這是被說出來的，不是被藏起來的。

**Step 1 執行腳本、Step 0、2 與 3 不執行；Step 4 兩者各半**，因為寫出一個框架與啟動一個伺服器是決定性的，而判斷一個 prompt 要求了什麼、依據一份設計產生一個 app、修改一份設計以及它所管轄的程式碼、還有像讀者那樣讀一個頁面，都是判斷。
Step 4 同時承載兩半，是因為它們是關於同一個執行中頁面的兩個問題；而它把兩者明確稱為「半」，是為了讓被判斷的那一半不會消失在被檢查的那一半後面。

## Step 0 - Warmup

- **Purpose**：定案正在處理的是哪一個 **target**、套用的是哪一個 **command**，以及 **lifecycle** 是否允許它——這道閘門必須在寫出任何東西之前執行，因為在那之後就沒有東西可以拒絕了。

- 先執行 `.venv`——**setup tool** 需要 `PyYAML`。
  app 本身完全不需要 Python。
  **Node** 必須在 `PATH` 上；確認 `node --version` 有回應。
  沒有任何東西需要 `npm install`。

- 讀取工作區根目錄的工作區設定 [config.yaml](config.yaml) 並解析：
  - **`wikiDir`**：MD report 的根目錄——這個 skill 的報告放在 `{wikiDir}\imp-home\` 底下。
  - **`vaultName`**：`wikiDir` 的最後一段路徑（例如 `MyVault`）——用來組出 `obsidian://` 連結的 Obsidian vault 名稱。
  - **`skillGroups`**：群組名稱 -> skills 根目錄的對應表——這個 skill 自己的目錄是 `{skillGroups.common}\skills\imp-home\`。
  - 在底下的步驟裡，凡是出現 `{wikiDir}`、`{vaultName}` 或 `{skillGroups.common}` 的地方都代入解析出來的值，包含出現在指令裡的。
  - 如果 `config.yaml` 不存在、或缺了某個需要的鍵，就停下來問使用者。

- 這個 skill 不呼叫任何 API，也不需要任何一種憑證。

- prompt 會是上面 **Prompt Examples** 所示形式的其中一種。
  從中解析出：
  - **target** — 第二行，一條目錄路徑。
    如果一個都沒給就問；絕不自己挑一個。
  - **command** — 第三行：`setup`、`gen`、`update`、`test` 或 `run`。
    任何其他字、或什麼都沒有，都是一次停下並依 **lifecycle** 順序列出這五個。
  - **hub name** — 只在 **setup** 時，第四行：要用哪一筆 **seed entry** 為這個 **target** 播種。
  - **mount sources** — 選填的 `mounts:` 那一行上、以逗號分隔的 **registry names**。
    一個名稱是 `apps` 的鍵，對某些 app 而言那是它的 owner skill，對另一些而言則是 app 自己；它永遠不會是一條路徑。
  - **change requests** — 對 **gen** 與 **update** 而言，其餘每一行散文，每一行都是使用者所要求的一項改動。
    對 **test** 而言，其餘的散文行則是一項 **review focus**：要先去看的東西。
    **run** 不接受任何散文，而一次 **run** 帶著散文是一次停下，詢問是不是本來要 **test**。
  - 選填、放在結尾的 **`run step N`** 選擇子。
    第三行上的 `run` 是 **command**；只有 `run step` 後面接一個數字才是選擇子。

- **讀取 lifecycle record 並執行閘門。**
  整個 **lifecycle** 就靠這道檢查撐住：
  - 如果 `{target}\.imp-home.json` 在那裡就讀它，並從中取出 **phase** 與 `history`。
    一個沒有紀錄的 **target** 從來沒有被 setup 過。
  - **setup**：若紀錄存在則拒絕。
    指名 **phase** 以及接在它後面的 **command**。
  - **gen**：若 `history` 裡任何地方出現 `update` 則拒絕——說明這個 target 已經過了不可回頭的那一點，而 **update** 才是它現在改變的方式。
    它同樣需要一份紀錄，所以一個從未被 setup 過的 **target** 也會被拒絕。
  - **update**：需要 **target code** 與 **target documents**；若兩者之一不在，就說先跑 **gen**。
  - **test** 與 **run**：需要 **target code**。
    任何有程式碼的 **phase** 都可以。
    兩者都不會因為 **lifecycle** 做過什麼而被拒絕——它們不改變任何東西，所以那道闘門沒有任何東西需要保護。

- **定案 hub name**，它的來源依 **command** 而不同：
  - **setup**：prompt 的第四行。
    如果它不在，就問——絕不退回去用 **target** 的最後一段路徑，因為那會從一筆沒有人選過的項目播種，而這個錯誤只會在後來以錯的 port 或錯的標題現形。
  - **gen**、**update**、**test**、**run**：**lifecycle record** 的 `hub` 欄位，也就是 **setup** 寫下它的地方。
    一份沒有這個欄位的紀錄早於它存在；說出來並詢問這個 **target** 是從哪一筆 **seed entry** 來的，而不是用猜的。

- **只在 `setup` 時**，解析 **skill config** 的 **seed entry** `homes.{hub name}`，取得 port、標題與起始的 **link list**。
  一個不是 `homes` 之鍵的 **hub name** 是一次停下，並列出哪些是。
  接著把每一個 **mount source** 透過 **app registry** 解析成一筆完整的 **link entry**，依 prompt 給出的順序；一個不是 `apps` 之鍵的 skill 是一次停下，並指名該補什麼。

- **對其他每一個 command**，讀取 **target** 裡的 **app config**，取得 port 與目前的 **link list**。
  此時一行 `mounts:` 就是一項改動要求，以同樣的方式透過 **app registry** 解析。

- 對已解析的 **link list** 裡的每一個 **mount**，檢查它的 `appDir` 裡是否有 `app.js`。
  記下哪些有、哪些沒有——沒有的那一個，是那個 app 自己的 skill 還沒被執行，不是這裡的錯。

- **只在 `setup` 時**，檢查 **target** 的擁有權：在 `skillGroups` 的各個 skills 根目錄裡，搜尋是否有另一個 skill 的設定也宣稱擁有同一個目錄。
  如果有，就停下來、回報這兩個宣稱者，並問哪一個才是擁有者。

- 檢查 port 是否已經被佔用。
  有回應通常表示先前某次執行的伺服器還活著，這沒問題——說出來，然後要嘛沿用它、要嘛把它停掉，而不是再啟動一個根本綁不上去的。

- 讀時鐘**一次**，並推導出這次執行的 `{yymmdd-hhmm}` 時間戳，再連同 **hub name** 與 **command** 推導出那兩條輸出路徑。

- 儲存 YAML checkpoint `step_0`，內容包含解析出來的 `wikiDir`、**target**、**hub name** 及它從哪裡來、**command**、從 **lifecycle record** 讀到的 **phase** 與 `history`、閘門的判定、port 以及它是否被佔用、**link list** 與它的數量、每一個 **mount source** 與它解析成了什麼、哪些 mount 帶有 `app.js`、任何 **change requests**、Node 版本、時間戳、輸出路徑、步驟選擇子，以及時間。

- 顯示 **target**、**command**、**phase**，以及閘門判定了什麼。
  這個步驟裡建立 MD report 檔案是選擇性的。

## Step 1 - Setup the Target

- **Purpose**：在任何程式碼存在之前，先給一個 hub 一個框架與一個身分，好讓產生這件事一開始就知道它的 port、它的標題與它的按鈕，而不是自己發明。

- **只在 `setup` 這個 command 時執行。**
  對其他任何 **command**，直接跳到那個 command 所導向的步驟。

- 從 YAML checkpoint 的 `step_0` 群組，把 **target**、**hub name**、**seed entry** 與已解析的 **link list** 讀回來。

- **執行 setup tool** 來寫出 **target frame**：
  - 例如：`python {skillGroups.common}\skills\imp-home\setup_target.py --hub {hub name} --target {target}`
  - 它會建立 **target** 與它的 `public\`，並寫出 **app config**、`start.cmd`、`README.txt`，以及 **phase** 為 `setup` 的 **lifecycle record**。
  - **它不寫 `server.js`。**
    一個框架不是一個 app；把 app 做出來是 **gen** 的事。
  - 它會拒絕一個缺漏的、空的、或帶著沒有 `label` 或沒有 `href` 之項目的 **link list**——一顆空白按鈕看起來像是應該要能用的東西。
    它會拒絕一個沒有 `appDir` 的 **mount**、一個 `href` 不是這個 origin 上之路徑的、一個會遮蔽 hub 自己某條路由的，或是兩個宣稱同一個 **mount prefix** 的。
  - 一個 `appDir` 裡沒有 `app.js` 的 **mount** 是**被回報，不是被拒絕**：那個 app 還沒有被它自己的 skill 跑過。

- **說出接下來是什麼**：**target** 現在有了一個框架，而且沒有任何東西可以執行。
  下一個 **command** 是 **gen**。

- 儲存 YAML checkpoint `step_1`，內容包含寫出的檔案與它們的大小、帶過去的 **link list**、每一個 **mount** 的就緒狀態、寫出的 **lifecycle record**，以及時間。

- 儲存 MD report 檔案。
  附加並顯示一個 **Setup** 區段：寫出的框架與大小、帶過去的按鈕、任何被回報為尚未就緒的 mount，以及現在被記錄下來的 **phase**。

## Step 2 - Generate the App

- **Purpose**：在同一個動作裡把一份設計變成一個能動的 app，並把那份設計留在它所產生的程式碼旁邊，好讓一個 hub 永遠不會在缺少「可供核對之物」的情況下存在。

- **只在 `gen` 這個 command 時執行。**
  對其他任何 **command**，直接跳到那個 command 所導向的步驟。

- 從 YAML checkpoint 的 `step_0` 群組，把 **target**、**change requests** 與 **link list** 讀回來。

- **這個步驟沒有腳本。**
  從一份寫好的設計產生出一份實作是判斷；一個被要求去做這件事的程式，只不過是在宣稱它做完了。

- **先讀 seed documents，並依據它們產生。**
  它們是規格，不是背景讀物：
  - `Home-RSDC.md` — §2.7 *Presentation Contract* 是頁面承載什麼、按鈕從哪裡來，§2.5 *Config Schemas* 是它讀的 **app config**，§2.6 *Derivation Rules* 是 **dead link** 的數量與 **mount prefix**，§2.8 *HTTP API* 是路由，§2.9 *Mountable Handler* 是一個 **mount** 需要什麼，§2.10 *Invariants* 是那些不變量；它的 Design 與 Coding 兩章，則是 component、配置、跳脫，以及程式碼怎麼寫。
  - `Wireframe.md` — §1 是頁面的結構、§2 是每顆按鈕必須承載的元素、§3 是那些不是 hub 頁面的頁面、§5 是頁面不得包含什麼。
  - 當一項 **change request** 與某份 **seed document** 衝突時，**對這個 target** 而言以那項要求為準——但要明白說出來，並在下面複製文件時把這個差異寫進 **target documents**。
    一個在它被產生的當天，程式碼與設計就彼此矛盾的 hub，事後沒有人核對得了。

- **寫出 target code** — `{target}\server.js` 與 `{target}\public\app.css` — 使其滿足上述文件與每一項 **change request**。
  之後的 **gen** 是針對同一批文件重新產生，而不是繞著上一次的結果打補丁。

- **接著把 seed documents 複製進 target**，成為 `{target}\docs\`：
  - 四份全部、兩種語言、在同一次執行裡——這正是讓 **target** 自我描述的東西。
  - 凡是這次 **gen** 偏離了某份 **seed document** 的地方，就修改那份副本，讓它描述的是**這個** hub，編號相同，並寫出那個偏離的代價。
  - 從這裡開始，那些副本就是 **target documents**，而 **seed documents** 對這個 hub 不再具有權威性。

- **往 lifecycle record 追加一筆**：一筆帶時間戳的 `gen`，並把 **phase** 設為 `gen`。

- **說出接下來是什麼，以及什麼沒有發生。**
  這個 **command** 寫出了一個 `server.js`，並沒有啟動它，所以這裡沒有任何東西是在執行狀態下被觀察過的。
  下一個 **command** 是 **test**，或者用 **run** 單純把它開起來。

- 儲存 YAML checkpoint `step_2`，內容包含每一項 **change request**、據以產生的那些 seed 文件章節、寫出的程式碼檔案、複製過去的文件、記錄下來的每一項偏離、追加的 **lifecycle record**，以及時間。

- 儲存 MD report 檔案。
  附加並顯示一個 **Gen** 區段：
  - **Summary line**：寫出的程式碼、複製過去的文件、記錄了幾項對 seed 的偏離，以及這個 hub 尚未被執行過。
  - **Departures table**，欄位為：
    - **Change request**：使用者自己的原話。
    - **What the seed design says**
    - **Recorded as**：現在承載它的那一節 **target documents**。

## Step 3 - Update the Target

- **Purpose**：讓一次改動依序穿過設計、再進入程式碼，而那是唯一一種讓文件事後仍然值得一讀的順序。

- **只在 `update` 這個 command 時執行。**
  對其他任何 **command**，直接跳到那個 command 所導向的步驟。

- 從 YAML checkpoint 的 `step_0` 群組，把 **target**、**change requests** 與 **link list** 讀回來。

- **這個步驟沒有腳本。**
  判斷一項改動要求是什麼意思、它該落在設計的哪裡、以及它蘊含什麼程式碼，這是判斷。

- **對每一項改動要求，先決定它落在 target documents 的哪裡**，然後把它寫在那裡：
  - **用「重新上色」來分，不是用主題來分。**
    一句在按鈕換了顏色之後仍然成立的話，是一次 **Specification** 的改動——`docs\Home-RSDC.md` 的某個編號章節，修改或新增。
    一句會因此不再成立的話，則屬於 `docs\Wireframe.md`，與它所描述的元素在一起。
  - 所以：hub 做什麼、一顆按鈕 *告訴* 讀者什麼、一項改動的代價是什麼，都是 **Specification**。
    顏色、hover、框線、字體與頁面的元素清單，都是 **Wireframe**。
    「頁面顯示什麼」橫跨兩者，而那正是為什麼判準是那句話的寫法，而不是它的主題。
  - 一項在文件裡完全放不進去的改動，就是一項在程式碼裡同樣放不進去的改動。
    說出來並詢問，而不是只把它寫進程式碼。
  - **在這一次執行裡把每一對的兩半都寫好**，編號相同。
  - 依 **RSDC standard** 檢查每一個改過的章節：Requirements 裡沒有技術選擇、Specification 裡除了 caller 使用的介面之外沒有組件、Design 裡沒有程式庫，也沒有任何一節向前引用。
  - **對一項移除了什麼的改動，在文件裡寫出它的代價**：這個 hub 從此不能再做什麼，以及那為什麼值得。
  - **兩份設計文件不得提到對方。**
    各自聲明自己的範圍；一條規則若需要另一份的理由，就用自己的話完整寫出那個理由。
    另一份檔案裡的章節編號，是一條會腐掉而沒人發現的連結。

- **接著把 target code 改成與之相符**，修改 **target** 自己的檔案：
  - 行為與外觀改 `server.js` 與 `public\app.css`，**link list**、port 或標題改 `app.config.json`。
  - **絕不呼叫 setup tool**，也絕不修改 **seed**。
  - 一項 `mounts:` 改動要求會被套用到 **app config** 的 `links` 上，透過 **app registry** 解析，每一個解析出來的 `appDir` 以絕對路徑寫入，並在它旁邊寫上該條目的 **owner skill**——hub 會在一個 mount 準備失敗時所提供的頁面上顯示那個擁有者，而少了它，一個備不起來的 mount 就說不出該去跑誰。

- **把這次改動可能弄壞的東西重新證明一次**，在一個備用 port 上、針對一份拋棄式的 **target** 複本——絕不用真正的 port、也絕不用 **target** 本身。
  **target documents** 的 Verification Obligations 列出了那些義務；重跑這次改動可能碰到的那幾項：
  - 如果有任何東西碰到了 label、href 或 note 抵達 markup 的方式，就重測跳脫。
  - 如果有任何東西碰到了路由，就重測掛載——包含一條**巢狀**路徑、一個裸前綴、一次 throw、一次 rejection、一個**漏網的**非同步失敗，以及一個沒有 `app.js` 的 mount。

- **往 lifecycle record 追加一筆**：一筆帶時間戳的 `update`，並把 **phase** 設為 `update`。
  如果這是第一筆，就明白說出 **setup** 與 **gen** 現在對這個 **target** 已經關閉。

- **說出接下來是什麼，並且精確地說出上面那些探測證明了什麼、沒證明什麼。**
  它們是對著一份拋棄式副本跑的，所以它們證明的是這項改動沒有弄壞它們所涵蓋的那些東西——不是證明了 **target** 能提供服務。
  下一個 **command** 是 **test**，或者用 **run** 單純把它開起來。

- 儲存 YAML checkpoint `step_3`，內容包含每一項 **change request**、它改動的文件章節、它改動的程式碼檔案、重跑的探測與它們的結果、追加的 **lifecycle record**，以及時間。

- 儲存 MD report 檔案。
  附加並顯示一個 **Update** 區段：
  - **Summary line**：有幾項改動要求、這次執行是不是那一次關閉了先前那些 command 的執行，以及 **target** 本身尚未被提供過。
  - **Changes table**，欄位為：
    - **Change request**：使用者自己的原話。
    - **Document**：它被寫進那一對文件的哪一節。
    - **Code**：它接著改動了哪些 target 檔案。
    - **Proved by**：為它重跑的那個探測，或是為什麼不需要。

## Step 4 - Serve and Review the Target

- **Purpose**：這是 target 變成一個執行中伺服器、並且接著像讀者那樣被讀過一遍的唯一地方——機器能檢查一個頁面的什麼、以及只有人能看出什麼，是關於**同一個**執行中實例的兩個問題，而在別的地方問其中任何一個，問的都是某個並沒有在跑的東西。

- **只在 `test` 與 `run` 這兩個 command 時執行。**
  沒有別的 **command** 會啟動伺服器。

- **`test` 跑完整個步驟；`run` 在伺服器一有回應時就停下。**
  一次 **run** 啟動它、詢問 `/healthz`、報出 **server origin**，然後結束——它不拿頁面去跟 **app config** 比對，也完全不去看那個頁面。
  這就是這兩個 **command** 的全部差別：**test** 是為了知道這個 hub 是不是對的，**run** 是為了使用它。
  一次以「對頁面下判斷」作結的 **run**，已經悄悄變成了一次 **test**，而那比兩者中任何一個都更糟，因為 caller 要的既不是前者也不是後者。

- **對 `test` 而言，這個步驟有兩半，而且依這個順序執行：先是被檢查的，後是被判斷的。**
  前者是腳本化且決定性的；後者兩者皆非，也無法被弄成那樣。
  **被檢查的那一半通過，不等於這個步驟通過**——在一個沒有人會想用的頁面上，那一半裡的每一項檢查都會通過，而這正是被判斷的那一半存在的全部理由。
  一次只回報前半就停下的 **test**，並沒有完成這個步驟。

- 從 YAML checkpoint 的 `step_0` 群組，把 **target** 與 port 讀回來。

### The checked half

- **把伺服器當成背景行程啟動**，並讓它繼續跑——它是一個伺服器，不是一支一次性腳本，而這一半是在它有回應時結束，不是在指令返回時結束。
  - 例如：`node {target}\server.js`
  - 使用絕對路徑。
    hub 會把每一條路徑都相對於它自己的目錄解析，因此 **target** 是它唯一能執行的地方。
  - 如果 port 先前已被佔用，先把那個伺服器停掉，而不是再啟動一個根本綁不上去的。

- **繼續之前先確認伺服器有回應。**
  詢問 `{server origin}/healthz`，它會回傳標題、連結數量、其中有多少是 **dead links**、每一個 **mount** 與它的狀態，以及組裝時間。
  **一次 `run` 到這裡就結束**，報出 **server origin** 與 `/healthz` 說了什麼。

- **拿 app config 去核對所提供的頁面，而不是拿原始碼去核對。**
  抓取 `/` 並把它的 anchor 與 **app config** 的 label 與 href 逐一依序比對；確認除了那份樣式表之外沒有任何外部參照；確認沒有任何一顆按鈕的樣式與其他不同。
  對每一個 **mount**，也詢問它的前綴，並記下回應了什麼。

- **在相信一個探測回報了什麼之前，先問它究竟能證明什麼。**
  一個根本不可能失敗的檢查，或是一個被函式庫悄悄替 hub 滿足掉的檢查，讀起來跟一個通過了的檢查一模一樣——被自動跟隨的轉址、只在根路徑上被詢問過的 mount、用錯大小寫讀到的標頭。
  凡是設計指明了一項證明需要什麼，就照做：前綴剝除要用一條 **nested** 路徑，轉址本身要看它自己，而不是看它導向了什麼。

### The judged half

- 這一半不用腳本。
  打開頁面，像讀者那樣看它。
  這一半是判斷。

- 用看的去確認，而不是信任剛剛蒐集到的那些數字：按鈕就是依序排列的 **link list**；每一個網址逐字讀起來都正確；每一顆按鈕的樣式都一模一樣；頁面不從 **server origin** 以外的任何地方載入東西。

- **看 prompt 要求看的東西，然後再看整個頁面。**
  外觀是由頁面來回答的，絕不是由一個狀態碼來回答——一份被抓取到的樣式表，不等於一份讀起來好看的樣式表。
  在某件事是推論出來、而不是親眼看到時，明白說出來。

- **拿頁面逐一元素去核對 target documents 的 wireframe**——它是一份規定性的清單，所以它標為必要的每一列都必須出現在頁面上：
  - 頁面缺少 wireframe 所要求的東西，是一個缺陷。
    指名它；不要在這裡修它。
  - 頁面帶著 wireframe 沒有列出的東西，同樣是一個缺陷：要嘆那個元素該拿掉，要嘆 wireframe 早該把它寫進去。
    指明是哪一種，然後放著。
  - **回報它然後停下——這個 **command** 記不了它。**
    wireframe 自己的缺陷區段是一份 **target document**，而只有 **update** 會寫那些。
    所以在這裡發現的缺陷，會晚一個 **command** 才被寫下來，由下一個跑 **update** 的人寫。
    那是 **test** 什麼都不改變的代價，而報告必須帶足夠的東西，讓那一次 **update** 不必重新觀察任何事情就能寫出來。

- **說出讀者在每一顆按鈕上會遇到什麼**——包含這個 skill 不探測任何東西，所以一顆指向已停止 app 的按鈕，看起來跟一顆指向執行中 app 的按鈕一模一樣；以及一個 **dead link** 看起來跟一個能用的連結一模一樣，**這是設計如此**。
  指名擁有每一個目標的那個 skill，好讓一顆掛掉的按鈕有一個擁有者，而不是只換來一個聳肩。

- **一個 mount 是這個 skill 唯一能為之發言的目的地。**
  它的狀態是在啟動時讀到的，所以逐一說出它有沒有起來；對於沒起來的那一個，指名它的 app dir 與組裝它的那個 skill——然後停下來，因為讓它變得可掛載是那個 skill 的工作。

- 不要修好一個目標、不要重啟另一個伺服器，也不要修改另一個 skill 的產出。

- 儲存 YAML checkpoint `step_4`。
  **一次 `test` 記下** **server origin**、綁定的 port 與 host、行程 id、Node 版本、`/healthz` 的回應、anchor 比對結果、每一個 **mount** 的狀態、被審視過的按鈕、**dead link** 的數量、看了什麼以及它顯示了什麼、wireframe 對帳結果、整體狀態、建議的下一個 **command**，以及時間。
  **一次 `run` 只記下其中前六項**——origin、port 與 host、行程 id、Node 版本、`/healthz`、時間——因為它別的什麼都沒看到。

- 儲存 MD report 檔案。
  對一次 **test** 附加並顯示一個 **Serve and Review** 區段，對一次 **run** 則是 **Serve** 區段。
  - **一次 `test` 的區段承載下面那些表格與判定。**
  - **一次 `run` 的區段只有一行 summary，沒有別的**：**server origin**、有幾顆按鈕、有幾個是 **dead links**，以及有幾個 **mounts** 起來了——這些全都是從 `/healthz` 讀來的，而不是從頁面。
    它不帶表格、也不帶判定，因為它什麼都沒看。
  - **Summary line**：**server origin**、有幾顆按鈕、有幾個是 **dead links**、有幾個 **mounts** 起來了、這個 hub 就目前這樣是否可用，以及 **phase** 說接下來是哪一個 **command**。
  - **Buttons table**，欄位為：
    - **Label**
    - **Href**：逐字照登，就跟 **app config** 所承載的一模一樣。
    - **Note**
    - **State**：已渲染、**dead link**，或是 **mount** 加上它的前綴回應了什麼。
  - **Mounts table**，欄位為：
    - **Prefix**
    - **App dir**
    - **Skill**：組裝它的那一個。
    - **Answered**：從那個前綴回來的東西。
  - **Per-button notes**：讀者在每一個目的地會遇到什麼，以及哪一個 skill 擁有它。
  - **Notes**：wireframe 對帳結果、關於這次執行改了什麼是親眼看到而非推論出來的部分，以及任何 **target documents** 視之為代價而非缺陷的東西，都以「代價」指名，好讓後來的讀者不會又把它重新翻出來。
