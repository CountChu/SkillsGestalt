---
name: imp-app
description: >-
  從一段散文建出一個本機的 web app 或 dashboard——一個 Node 伺服器（`node server.js`），
  真正的工作由一個 Python kernel 完成，兩邊都只用標準函式庫，並由單一一份 `app.config.json` 設定——
  再帶著它走完六個 command。prompt 的第二行指名 app dir，第三行是 command：
  `vibe` 直接從散文建造與修改這個 app；`reverse` 從原始碼與活著的頁面推導出它的文件——
  一份 RSDC design pair 與一份 wireframe pair，各有英文與繁體中文；`update` 先改那些文件、後改程式碼；
  `test` 先跑 unit tests，再在瀏覽器裡驅動頁面；`start` 啟動這個 app 並說出它在哪裡；
  `deploy` 把它複製到這個 skill 的 target list 裡的某個 target。順序是單向的：
  第一次 `reverse` 關上 `vibe`，第一次 `update` 關上 `reverse`。每個 app 寫一份 MD report 與
  一份 YAML checkpoint，由每一個 command 往後追加，另外還有 app dir 裡的 lifecycle record
  `.imp-app.json`，單向順序正是依它來強制執行。
---

本文件為 [SKILL.md](.github/common/skills/imp-app/SKILL.md) 的繁體中文版；真正會執行的是 SKILL.md，任一份改了某節，另一份必須在同一次執行中、以相同編號一起改。

# TERMINOLOGY

每個 skill 裡都是同一個意思的詞。

- **`run step N`** — 一個放在 prompt 結尾、指名某一個 step 的選擇器。
  它**只**執行那一個 step，並把每一個更早 step 的輸出從 YAML checkpoint 讀回來。
- **Checkpoint Dir** — 存放某個 skill 的 YAML checkpoint、每次執行各一份的目錄。
  每個 skill 都有自己的；這個 skill 的寫在 **CONFIGURATION** 底下。
- **YAML checkpoint** — Checkpoint Dir 裡的 `process.yaml`。
  每個 step 把它的輸出寫在那裡的 `step_{N}` 群組底下，於是後面的 step 把它們讀回來，而不是重算一次。
- **MD report** — 這個 skill 寫進 wiki vault 的那份 Markdown 報告，放在一個以這個 skill 命名的資料夾裡，在它的結果各節上方帶著標準的表頭（Skill、Checkpoint、Created、Updated、Prompt）。
- **no forward-reference** — 一個 step 絕不能依賴排在它後面的 step 這條規則。
  為了安排控制流而指名後面的 step 不算違反；借用那個 step 的輸出才算。

# DEDICATED TERMINOLOGY

這個 skill 領域專屬的詞。
詞彙表擁有每一則定義——step 使用這個詞，而不是把它的意思再講一遍。

- **app dir** — prompt 在它第二行指名的目錄，例如 `artifacts\InvCov`，相對於 workspace 根目錄，位於 wiki vault 之外。
  它是這個 app 住的地方，而且從第一次 **vibe** 起，它就是那個 app 的**原始碼**，不是建置產物。
- **app name** — **app dir** 路徑的最後一段，去掉結尾的 `-app`，拼法完全照那個目錄怎麼寫（`artifacts\InvCov` 得到 `InvCov`，`artifacts\redfish-test-app` 得到 `redfish-test`）。
  它為 Checkpoint Dir、**MD report** 與 **design pair** 命名。
- **command** — prompt 第三行的那個字：**vibe**、**reverse**、**update**、**test**、**start** 或 **deploy**。
  一次執行剛好一個，而它決定哪一個 step 會執行。
- **lifecycle** — `vibe` → `reverse` → `update` 這個單向順序，而 **test**、**start** 與 **deploy** 一旦有程式碼，在任何時點都可用。
  它有兩道只往一邊開的門：第一次 **reverse** 為那個 **app dir** 永久關上 **vibe**，而第一次 **update** 關上 **reverse**。
- **lifecycle record** — `{appDir}\.imp-app.json`，承載 **phase** 以及每一個對這個 **app dir** 執行過的 **command** 及其時間戳記的 `history`。
  它住在 **app dir** 裡而不是住在某個 checkpoint 裡，因為 **lifecycle** 跨越多個工作階段，而一份每次執行各一份的檔案會忘記它。
  這個 app 從不讀它。
- **phase** — **lifecycle record** 承載的最後一個會改變狀態的 **command**：`vibe`、`reverse` 或 `update`。
  **test**、**start** 與 **deploy** 什麼都不改，因此永遠不會改它。
- **adopted** — 第一個 **command** 對它執行時就已經有程式碼、卻沒有自己的 **lifecycle record** 的 **app dir**。
  它是被接管而不是被拒絕：記錄被寫出來、它的 `history` 以一筆指名現場發現了什麼的 `adopted` 開頭，而 **phase** 依磁碟上的東西設定——已經有 **app documents** 就是 `reverse`，沒有就是 `vibe`。
  關於 **fixed shape** 的任何事都不對它做假設。
- **vibe** — 直接從散文建造與修改這個 app、中間不擺任何文件的那個 **command**。
  它要多少個 prompt 就重複多少次，而且它是唯一被允許寫出沒有任何東西描述的程式碼的 **command**。
- **reverse** — 結束這場 **vibe** coding 的那個 **command**：它讀這個 app 自己的原始碼與它正在跑的頁面，並從它們寫出 **app documents**。
  它可以一直重複到第一次 **update**，此後絕不。
- **update** — 修改一個已經有文件的 app 的那個 **command**：先 **app documents**、後程式碼，要幾次就幾次。
- **test** — 追問這個 app 對不對的那個 **command**，分兩個半邊：先 **unit tests**，再 **UI test**。
  它不改 **app dir** 裡的任何東西。
- **start** — 啟動 **app dir** 裡已經有的東西、確認它有回應、說出它在哪裡，然後停下的那個 **command**。
  它是給想**用**這個 app 的讀者的，所以不像 **test**，除了伺服器有起來以外它什麼都不檢查，也完全不做任何判斷。
- **deploy** — 把這個 app 送到某個 **target** 的那個 **command**。
  它從 **app dir** 往外複製、絕不複製回它裡面，而且除了 **lifecycle record** 以外不改那裡的任何東西。
- **the app** — 這個 skill 建造出來的東西：一個以 `node server.js` 啟動、自我完備的目錄，它真正的工作由 **python kernel** 完成，兩邊都只用標準函式庫。
  Node 提供服務並衍生行程；Python 做決定。
  它必須在什麼都沒安裝的情況下跑得起來。
- **fixed shape** — 這個 skill 寫出來的每一個 app 都有的那個版面，無論它的需求要求什麼。
  一個 **command** 改的是這個 app 做什麼，絕不是這個：
  - `server.js` 在根目錄，只用 Node 標準函式庫，它的 `listen` 擺在 `require.main === module` 後面，於是 require 這個檔案不會啟動任何東西。
  - `app.js` 在它旁邊——就是 **mountable handler**。
  - **python kernel** 在 `scripts\` 底下。
  - `public\`，存放伺服器按名稱提供的那個頁面：標記、樣式與行為分成各自的本地檔案，而且這個頁面送出的每一個位址都寫成**相對於它自己**——`./api/x` 與 `./app.css`，絕不是 `/api/x` 與 `/app.css`。
  - **app config** 在 `server.js` 旁邊。
  - 一條 `/healthz` 路由，回答這個 app 在啟動時解析出了什麼——它讀到的值、它找到的 **python kernel**、組裝的時間——而且不含任何機密。
  - **unit tests** 在 `tests\` 底下。
  - 一份 `start.cmd` 與一份 `README.txt`，於是這個資料夾對一個沒參與過這場對話的人也是跑得起來的。
- **python kernel** — `{appDir}\scripts\` 底下的 Python，只用標準函式庫，由伺服器衍生並轉送到頁面。
  它擁有這個 app 的領域所需的每一個決定；**伺服器完全不解析其中任何一部分**，這正是讓換掉這個 kernel 等於改動這個 app 的原因。
- **app config** — **app dir** 的 `server.js` 旁邊那份 `app.config.json`，也是這個 app **唯一**會讀的檔案。
  伺服器或 **python kernel** 否則就得向這個 skill 索取的每一個值都承載在這裡，這正是讓這個資料夾可以被複製到某個 **target** 並在那裡原封不動跑起來的原因。
- **mountable handler** — `server.js` 旁邊的 `app.js`，匯出 `createApp(options)` 並回傳伺服器原本會用來監聽的那個 `(req, res)` 函式。
  它是這個 app 被自己以外的東西提供服務的方式：一個 hub require 它、呼叫它一次，然後在自己的某條路徑底下替這個 app 回應。
  擁有一個通訊埠與回應請求是可以分開的，而只有前者才是關於擁有一個位址。
- **unit tests** — `{appDir}\tests\` 底下的測試，只用標準函式庫：**python kernel** 用 `unittest`，伺服器用 `node:test`。
  它們是這個 app 的一部分，不是這個 skill 的一部分，於是它們在什麼都沒安裝的機器上也跑得起來。
  只有兩種命名會被發現、其他都不會——`tests\test_*.py` 與 `tests\*.test.js`——因為一個沒有任何東西會去跑的測試檔案，讀起來跟一個通過了的測試檔案一模一樣。
- **UI test** — **test** 被判斷的那半邊：在一個真正的瀏覽器裡驅動這個頁面，並對照 **wireframe pair** 一個元素一個元素地讀它。
  抓取標記不算是一次。
- **app documents** — **design pair** 與 **wireframe pair** 合起來，放在 `{appDir}\docs\` 底下。
  **reverse** 寫出它們、**update** 修改它們，而且從第一次 **reverse** 起，是它們、而不是 prompt 的歷史，說出這個 app 必須是什麼。
- **design pair** — `{appDir}\docs\{app name}-RSDC.md` 與它的繁體中文 twin `{app name}-RSDC-tw.md`。
  依 **RSDC** 標準寫成，它們決定*這個 app 必須是什麼*。
- **RSDC** — Requirements、Specification、Design、Coding：一份 **design pair** 文件的四個部分，依這個順序。
- **wireframe pair** — `{appDir}\docs\Wireframe.md` 與它的繁體中文 twin `Wireframe-tw.md`。
  它們是這個頁面的元素清冊——每一個面板、控制項、表格欄位與可見狀態——是從**正在跑的**頁面讀下來的，而不是從標記寫出來的。
  這一對擁有那份清冊：其他任何地方都不再重述它。
- **document templates** — 這個 skill 裡的 `assets\Wireframe-tmp.md`，以及 **gen-rsdc-app** 寫 **design pair** 所依的 design template `RSDC-App-tmp.md`。
  它們擁有一份 **app document** 的**形狀**——它帶著哪些編號的章節、每一節放什麼——於是相隔一年寫出文件的兩個 app 可以用同一種方式讀。
  step 指向它們，絕不重述那份章節清單。
- **RSDC standard** — **design pair** 所依循的章節職責規範：四個部分各自回答哪一個問題，以及各自不得向後取用什麼。
  **document templates** 帶的是它的形狀，它帶的是理由；當某段內容該放哪一章有爭議時，以它為準。
- **gen-rsdc-app** — **reverse** 用來寫 **design pair** 的 skill：它讀這個 app 的原始碼、畫出 **components**，先拿它的 design template 對照 **RSDC standard**，再依那份 template 寫出英文半邊，然後讓 `chinese` skill 寫出 twin。
  它不改任何程式碼，並交回它寫了什麼。
- **component** — 這個 app 裡一個可實作、且只有一項工作的部件：伺服器、**mountable handler**、某一個頁面、**python kernel** 的某一個進入點。
  **design pair** 的 Design 部分畫出這些邊界，而每一個 component 都至少出現在一項 **verification obligation** 裡。
- **verification obligation** — **design pair** 的 Coding 部分中，Verification Obligations 的一列：一個主張、它證明的規則、證明它的觀察與由誰來做——或標 *not verified*，並寫明目前讀過了什麼。
  每一個 **component** 都至少出現在一列；這些列是這個 skill 對「已證明」唯一的定義。
- **prompt log** — 每一次 **vibe** 與 **update** 的要求、它改了什麼、以及那次改動是怎麼被證明的，依序留下的記錄。
  它在 YAML checkpoint 裡累積，並被渲染進 `{appDir}\docs\Prompts.md`——那是*為什麼*這個 app 長成這樣的歷史，而那是程式碼無法顯示的。
- **target** — 這個 app 被送達的某個目的地，在 prompt 第四行指名，並透過 **target list** 解析。
  它是這個 app 在別處的一份副本，絕不是第二份原始碼。
- **target list** — **skill config** 的 `targets` **清單**：一筆項目對一個目的地，每一筆承載一個 `name`、程式碼**在那台機器上**要去的 `appDir`，以及那些在那裡為真、而在 **app dir** 裡為假的 **app config** 值。
  一個 **target** 就是這同一個 app 在別處，所以一筆項目只說出關於那個別處有什麼不同。
  它是一次 **deploy** 用來解析一個名稱的那份已審閱清單，這正是為什麼目的地絕不是一個打進 prompt 的路徑。
- **skill config** — 這個 skill 裡的 `assets\config.yaml`，承載 **target list**。
  只有這個 skill 自己的工具會讀它；沒有任何 app 會讀，而且它不隨一次 **deploy** 出發。
- **session resolver** — 這個 skill 的 `scripts\` 裡的 `resolve_session.py`。
  它在第一個 **command** 時為這個 app 的 Checkpoint Dir 打上戳記，並在之後每一次呼叫時重新開啟現存最新的那一個，於是同一個 app 的兩次呼叫不可能落在不同的目錄裡。
- **test runner** — 這個 skill 的 `scripts\` 裡的 `run_tests.py`。
  它發現並執行 **unit tests**，並印出一份 JSON 結果。
  它是這個 skill 的工具，不是這個 app 的一部分。
- **deploy tool** — 這個 skill 的 `scripts\` 裡的 `deploy_app.py`。
  它透過 **target list** 解析一個 **target**，並把這個 app 送到它那裡。
- **server origin** — `http://127.0.0.1:{port}`，其中的通訊埠是 **app config** 的 `port`。
- **target origin** — 對一個 **target** 的同一件事：那個目的地自己的 **app config** 所承載的主機與通訊埠。

# CONFIGURATION

這個 skill 執行時所用的具體值。
底下每一條路徑都是這個 skill 的常數；關於正在處理的那個 app 的一切，都從 prompt 指名的 **app dir** 讀進來。

- **Checkpoint Dir** — `checkpoints\imp-app\{app}-{yymmdd-hhmm}\`，其中 `{app}` 是 **app name**，而 `{yymmdd-hhmm}` 由對那個 **app dir** 執行的**第一個** **command** 打上戳記。
- **YAML checkpoint** — Checkpoint Dir 裡的 `process.yaml`。
- **MD report** — `{wikiDir}\imp-app\imp-app-{app}-{yymmdd-hhmm}.md`，帶著與 Checkpoint Dir 相同的 `{app}` 與戳記，其中 `wikiDir` 來自 workspace 的 [config.yaml](config.yaml)（在 Step 0 解析）——絕不把 wiki 根目錄寫死。
- **lifecycle record** — `{appDir}\.imp-app.json`。
- **app documents** — `{appDir}\docs\`。
- **prompt log** — `{appDir}\docs\Prompts.md`。
- **document templates** — `{skillGroups.common}\skills\gen-rsdc-app\assets\RSDC-App-tmp.md` 與 `{skillGroups.common}\skills\imp-app\assets\Wireframe-tmp.md`。
- **gen-rsdc-app** — `{skillGroups.common}\skills\gen-rsdc-app\SKILL.md`。
- **RSDC standard** — `{skillGroups.common}\references\RSDC-Standard.md`，其圖的記法在 `{skillGroups.common}\references\DFD.md`。
- **skill config** — `{skillGroups.common}\skills\imp-app\assets\config.yaml`。
- **session resolver** — `{skillGroups.common}\skills\imp-app\scripts\resolve_session.py`。
- **test runner** — `{skillGroups.common}\skills\imp-app\scripts\run_tests.py`。
- **deploy tool** — `{skillGroups.common}\skills\imp-app\scripts\deploy_app.py`。
- **shared report rules** — `{skillGroups.common}\rules\report-md-rules.md`、`{skillGroups.common}\rules\report-yaml-rules.md` 與 `{skillGroups.common}\rules\scratch-rules.md`。

# MUST FOLLOW

- **文件決定程式碼是什麼——從 `reverse` 起，而那個例外正是重點。**
  **vibe** 是唯一被允許寫出沒有任何東西描述的程式碼的 **command**，因為在一開始還沒有東西可以描述，而那時寫出來的設計會是一份對猜測的描述。
  **reverse** 結束那件事，而在它之後 **update** 先改 **app documents**、再改程式碼。
  在 **reverse** 之後，沒有任何時點是先寫程式碼、事後再描述它——那樣產出的設計是一份逐字稿，對下一位讀者一文不值。
- **lifecycle 只往一個方向走，而每一道門都在身後關上。**
  一旦 **lifecycle record** 承載了一筆 `reverse`，**vibe** 就對那個 **app dir** 永遠被拒絕；一旦它承載了一筆 `update`，**reverse** 也一併被拒絕。
  - **那件事的代價值得指名。**
    在第一次 **update** 之後，就沒有重新推導文件這條路了：每一次文件改動都是對著 **app dir** 自己的檔案手工做的。
    那是刻意的——一份從原始碼重新推導出來的設計，會刪掉的恰恰是原始碼無法顯示的東西：一項被接受的代價、一個被否決的替代方案、一筆被記下的缺陷。
    **reverse** 可用的期間，剛好就是文件還沒有任何屬於自己的東西可以失去的那段期間。
- **如果程式碼在文件寫出之後動過了，在改動任何一邊之前先說出來。**
  把 **app dir** 的程式碼修改時間拿來跟 **app documents** 比對；在這個 skill 之外做的手工編輯是常見的原因。
  去更新一份程式碼已經走過頭的設計，是把改動寫進一份本來就已經錯了的文件裡。
- **每一份文件都是一對，而兩個半邊一起移動。**
  在 `{app name}-RSDC.md` 裡寫下或改過的一節，要在同一次執行中、以相同編號在 `{app name}-RSDC-tw.md` 裡寫下或改過；**wireframe pair** 帶著同一條規則。
  兩份漂移開的檔案不再說出這個 app 是什麼；它們是在為它爭論。
- **繁體中文 twin 的每一個標題都保留英文**——一個字元一個字元照它的來源怎麼寫——於是兩份可以並排閱讀，而審閱者一眼就能看出沒有東西漏掉。
  檔名、路徑、config 鍵、checkpoint 欄位名稱與詞彙表用詞同樣保持原樣；被翻譯的是圍繞它們的散文。
- **design pair 的各章是單向的。**
  Requirements 不陳述任何技術選擇，Specification 只透過 caller 使用的介面提到 component，Design 不涉及任何程式庫或語法，而且沒有任何一節指向編號在它之後的節。
  向後借來的詞彙，等於在那一章就把後面那一章存在的理由先答掉了，讀者再也分不出哪些是需要、哪些是做出來的東西。
  某段內容該放哪一章有爭議時，以 **RSDC standard** 為準。
- **app documents 絕不指名這個 skill、某個 command，或它的任何工具。**
  一份指向產生它的那套程序的設計，是循環定義的一半，而且不留下單一來源。
  一份文件在不指名它勝過誰的情況下陳述它自己的權威：*任何與本文件不一致的實作，該改的是實作*。
- **Node 提供服務並衍生行程；python kernel 做決定。**
  伺服器完全不解析領域。
  一個長出了領域規則的伺服器，是邊界擺錯了位置——去移動那條邊界，而不是把那個值穿過去。
- **這個 app 在沒有任何 skill 在場時必須照樣運作。**
  使用者例行做的每一件事都能從它的頁面到達，只用 Node 與 Python 標準函式庫——不 `npm install`、不 `pip install`、沒有套件、沒有 CDN、載入時不抓字型。
  skill 存在是為了建造與修改這個 app，不是為了操作它。
  - **skill config** 不隨這個 app 出發，所以一個在自己旁邊找不到 `config.yaml` 的 component 把那當成**正常，不是致命**：在 **app dir** 裡與在某個 **target** 上都沒有這份檔案，而它原本會讀到的每一個值，早就在 **app config** 裡或在它的命令列上了。
- **這個 app 是生產程式碼，無論它是怎麼被寫出來的。**
  命令列上不放機密——一份行程清單是每一個其他行程都讀得到的，所以密碼要嘛經由 **stdin** 到 Python，要嘛就不到。
  不拿瀏覽器給的主機、路徑或 URL 未經檢查就用：由這個 app 決定、並在 **python kernel** 裡再強制一次的白名單，才是讓伺服器不變成通往它背後網路的中繼的東西。
  把每一個到達頁面的值都轉義。
  **絕不為了讓某個 command 過關而放寬其中任何一條**——如果某道防護擋住了某個改動，那個改動就是錯的；把這件事說出來，並提出不是那樣的版本。
- **新的值屬於 app config；新的行為屬於 python kernel。**
  如果一項改動可以用加一個鍵而不是加一個分支來完成，就加那個鍵——那正是讓下一次改動根本不需要這個 skill 的東西。
- **每一個 app 都是可被 mount 的，而那件事的兩個半邊從第一版就寫進去。**
  它發佈一個 **mountable handler**，而它的 `server.js` 把 `listen` 擺在 `require.main === module` 後面。
  它的頁面以相對於自己的方式定址伺服器，而一個由伺服器*產生*、深在好幾層路徑底下的頁面，會自己算回去，而不是假設自己在根目錄。
  - 這件事是擺在 **fixed shape** 裡、而不是等某個 hub 出現時才加上，因為**兩種失敗在閱讀中都看不見**。
    一個沒有防護的 `listen` 只有在這個檔案被 require 時才顯現；一個絕對位址只有在這個 app 被掛在某條路徑底下提供服務時才顯現——兩者都發生在別人開始依賴它的那一刻。
    事後改造一個 app 是一個下午、兩種語言的文件改動；一開始就寫對只要十幾行。
- **target 就是原始碼，裡面沒有任何東西是建置產物。**
  沒有任何 **command** 會從別的東西重新產生 **app dir**，而一次 **deploy** 是從它往外複製、絕不複製回它裡面。
  坐在某個 **target** 上的是副本；坐在 **app dir** 裡的才是這個 app。
- **在那個能抓到某項改動缺席的 unit test 存在之前，那項改動都還沒完成。**
  **vibe** 與 **update** 各自在與改動同一輪裡寫出它。
  一輪有改動而沒有測試的，記錄為**未證明**，不是完成。
- **`test` 有兩個半邊，而被檢查的那半邊不等於這個 step。**
  每一個 **unit test** 在一個沒有人用得下去的頁面上都會通過，那正是 **UI test** 存在的全部理由。
  一次只報告 unit 結果就停下的 **test** 並沒有做完。
  一次找到**零**個測試的執行就報告零——絕不報綠燈——而且每一個沒有任何測試提到過的原始檔都會被指名，每一個命名成兩個 runner 都不會發現的測試檔案也一樣。
- **UI test 是被驅動出來的，不是被讀出來的。**
  是在真正的瀏覽器裡的即時 DOM，不是標記檔案，而且 **wireframe pair** 記下的每一個**可見狀態**都在被判斷之前先到達過。
  一個沒有人打開過的狀態是猜測，而一個狀態碼不是一種外觀。
- **`test`、`start` 與 `deploy` 不改 app dir 裡的任何東西。**
  前兩者之中任何一個發現缺陷時**指名它並停下**；修它是一次 **update**，或在 **vibe** 還開著時是一次 **vibe**。
  **deploy** 唯一寫進 **app dir** 的，是它自己那筆 **lifecycle record**。
- **`vibe`、`reverse` 與 `update` 不留下一個正在跑的伺服器。**
  寫與驗證是分開被要求的，因此一次疊代不必被收取一道沒有人現在想要的審閱的代價。
  所以這三者各自在結尾說出它**沒有**觀察到什麼，並指名 **test** 或 **start**。
- **一個 target 由 registry 指名，絕不由 prompt 裡的某條路徑指名。**
  prompt 裡的路徑是未經審閱、卻會抵達某個檔案系統的輸入——而那可能是別人的。
  **target list** 才是那份已審閱清單，而一個不在裡面的 target 是一次停下、說出要加什麼，不是一次猜測。
  **指名一個也不是選擇性的**：一次沒有指名任何 target 的 **deploy** 會被拒絕並列出那些名稱，而 `all` 才是要求每一個的方式。
  寫到別人的機器上不是預設。
- **一次執行一個 app dir。**
  這個 **command** 剛好套用在一個 **app dir** 上。
  一次執行絕不處理兩個，而且當 prompt 沒有指名任何一個時，絕不退而取「唯一的那個」——它會問。
- **絕不把某個 app 寫死。**
  任何 **app name**、**app dir** 路徑、通訊埠、標題、端點或 **target** 都不得出現在這個檔案裡、**document templates** 裡，或這個 skill 的工具裡。
  prompt 指名 **app dir**；**skill config** 指名 **targets**。
- **每一個 command 都往 lifecycle record 追加。**
  一個改了 **app dir** 卻沒有把自己記下的 **command**，會把 **phase** 留給下一次執行去猜，而上面那道閘門的可靠程度，就等於它讀到的東西的可靠程度。
- **一個 app 的每一份輸出都帶著同一個 `{yymmdd-hhmm}` 戳記**——每個 app 一份 Checkpoint Dir 與一份 **MD report**，由第一個 **command** 打上戳記，並由之後每一個往後追加。
  **app dir** 本身**不帶戳記**：它是當前的那個 app，而為它打上戳記會在讀者預期只有一個資料夾的地方留下一長串 stale 副本。
- **MD report 每個 app 建立一次，此後都是往後追加。**
  **shared report rules** 裡的建立規則，在檔案已存在時會清掉表頭以下的一切；那條適用於一次*新的*執行，而這裡後來的一個 **command** 屬於*同一個*工作階段。
  所以在之後的呼叫裡，刷新表頭的 **Updated** 欄位並**追加**新的一節——絕不清掉本文，因為那是更早的那些 **command** 做了什麼的唯一記錄。
- 必須一步一步執行 workflow，並顯示每一個 step 編號。
- 每個 step 必須自我完備。
  **No forward-reference.**
- 一個程式能以 deterministic 方式完成的 step 必須以腳本執行。
  一個需要閱讀、判斷或摘要的 step **絕不可**腳本化——把它寫成自然語言指示，讓 agent 自己直接執行。
- **遵守 `run step N` 選擇器**：執行 Step N，然後停下；絕不執行更後面的 step。
- MD report 的表頭與形狀依 `{skillGroups.common}\rules\report-md-rules.md`。
- YAML checkpoint 的形狀與必要欄位依 `{skillGroups.common}\rules\report-yaml-rules.md`。
- 一次執行的拋棄式檔案放在哪裡、以及怎麼清掉，依 `{skillGroups.common}\rules\scratch-rules.md`——每一次探測、每一份 **app dir** 的拋棄式副本與每一份被擷取下來的輸出，正是那種東西。
- **Checkpoint Dir 裡的每一份 JSON 都恰好只有一個寫入它的 step。**
  產生某份資料檔的那個 step 一次把它整份寫完，並擁有它；之後得出結論的 step 在它旁邊寫自己的 `step_{N}.json`，絕不在另一個 step 寫的檔案裡新增、修改或刪除任何一個鍵——即使是為了取代它也不行。
  YAML checkpoint 是唯一的例外：它是往後追加的，每個 step 一個 `step_{N}` 群組，而不是整份重寫。
  一份被好幾個 step 回寫的資料檔，在它的第一個 step 重跑的那一刻就毀了——一次 parser 修正或一次 `run step 1`，就會把它整份重寫，無聲無息地抹掉之後每一個 step 的結果。
- **在這個 skill 結束之前，顯示 server origin、app dir、MD report 與 YAML checkpoint**——只顯示那四樣，並把每一樣都渲染成可點擊的 Markdown 連結。
  **server origin** 是一個 `http://` URL，就以它自己作為連結，而且只由啟動過伺服器的那些 **command** 顯示——**test**、**start**，以及一次能在它的 **target** 上把這個 app 啟動起來的 **deploy**，那一次會在旁邊顯示 **target origin**；**vibe**、**reverse** 與 **update** 省略它，因為它們沒有留下任何正在跑的東西。
  MD report 住在 vault 裡、在這個 workspace 之外，所以用 `obsidian://open?vault={vaultName}&file=<vault-relative-path>` URI 連結它（例如 `[imp-app-InvCov-260924-1130.md](obsidian://open?vault={vaultName}&file=imp-app/imp-app-InvCov-260924-1130.md)`）；**app dir** 與 YAML checkpoint 保持相對於 workspace、使用正斜線的目標（例如 `[process.yaml](checkpoints/imp-app/InvCov-260924-1130/process.yaml)`）。
  - 每一次執行都這樣做，包含像 `run step 0` 這種只跑一部分的執行。

# Prompt Examples

## Prompt 1

```
/imp-app
artifacts/InvCov
vibe
Read InvDatabase/data and show each stock's coverage as one row.
Start it with node server.js. Do the real work in Python.
```

## Prompt 2

```
/imp-app
artifacts/InvCov
reverse
```

## Prompt 3

```
/imp-app
artifacts/InvCov
update
Add a 缺漏天數 column, and sort the table by it descending.
```

## Prompt 4

```
/imp-app
artifacts/InvCov
test
```

## Prompt 5

```
/imp-app
artifacts/InvCov
start
```

## Prompt 6

```
/imp-app
artifacts/InvCov
deploy
nuc-win
```

## Prompt 7

```
/imp-app
artifacts/InvCov
start
run step 0
```

# Workflow

每個 step 以一句 **Purpose** 開頭：說出這個 step 為什麼要作為一個 step 存在——把它折進隔壁那個 step，這個 skill 會失去什麼。

**command 安排這次執行的路由。**
Step 0 永遠執行，也是那道閘門被強制的地方。
Step 1 只為 **vibe** 執行、Step 2 為 **reverse**、Step 3 為 **update**、Step 4 為 **test**、Step 5 為 **start**、Step 6 為 **deploy**。
在這裡指名那些 step 是路由，不是 forward-reference：沒有任何 step 借用後面 step 的輸出。

**沒有任何 command 同時改動這個 app 又判斷它。**
**vibe**、**reverse** 與 **update** 以磁碟上的檔案結束，並且不留下任何正在跑的東西；**test**、**start** 與 **deploy** 除了那筆 **lifecycle record** 以外，什麼都不寫進 **app dir**。
那道切分正是讓一次疊代只付它所改動的代價的東西，也正是讓一次執行不會暗示它檢查了它從未看過的東西的東西。
代價是一次 **vibe** 或一次 **update** 可以在這個 app 事後從未被提供服務的情況下結束——這件事被說出來，而不是被藏起來。

**Step 0、4 與 6 執行腳本，Step 1、2、3 與 5 不執行**，因為為一個工作階段打上戳記、發現並執行測試、以及把一棵目錄樹複製到一個已審閱的目的地都是 deterministic 的，而從散文寫出一個 app、從原始碼推導出設計、把一項改動穿過設計帶進程式碼、以及像一個使用者那樣讀一個頁面，都是判斷。
Step 4 承載那道切分的兩個半邊，並把它們指名為半邊，於是被判斷的那半邊不會被遺落在被檢查的那半邊後面。

## Step 0 - Warmup

- **Purpose**：定下正在處理哪一個 **app dir**、哪一個 **command** 適用、以及 **lifecycle** 是否允許它——那道閘門必須在任何東西被寫出之前被強制，因為事後就沒有東西可以拒絕了。

- 先執行 `.venv`——這個 skill 的工具需要 `PyYAML` 來讀一份 config。
  **Node** 必須在 `PATH` 上，**Python** 也必須；檢查 `node --version` 與 `python --version` 兩者都有回應，並把它們記下來。
  沒有任何東西要 `npm install`。

- 讀 workspace 根目錄的 workspace config [config.yaml](config.yaml) 並解析：
  - **`wikiDir`**：MD report 的根目錄——這個 skill 的報告放在 `{wikiDir}\imp-app\` 底下。
  - **`vaultName`**：`wikiDir` 路徑的最後一段（例如 `InvLlmWiki`）——用來組出 `obsidian://` 連結的 Obsidian vault 名稱。
  - **`skillGroups`**：群組名稱 -> skills 根目錄的對映——這個 skill 自己的目錄是 `{skillGroups.common}\skills\imp-app\`，而 **shared report rules** 在 `{skillGroups.common}\rules\` 底下。
  - 把解析出來的值代入底下 step 裡每一處出現 `{wikiDir}`、`{vaultName}` 或 `{skillGroups.common}` 的地方，包含指令裡。
  - 如果 `config.yaml` 不存在、或缺少某個需要的鍵，停下並問使用者。

- 這個 skill 不呼叫任何 API，也不需要自己的任何憑證。
  某個 **target** 可能需要一個才到得了；那屬於已經把它掛起來的那個東西與 **target list**，絕不屬於命令列。

- 在執行 workflow 之前檢查底下這些腳本／檔案存在。
  - `{skillGroups.common}\skills\imp-app\scripts\resolve_session.py`
  - `{skillGroups.common}\skills\imp-app\scripts\run_tests.py`
  - `{skillGroups.common}\skills\imp-app\scripts\deploy_app.py`
  - `{skillGroups.common}\skills\gen-rsdc-app\SKILL.md`
  - `{skillGroups.common}\skills\gen-rsdc-app\assets\RSDC-App-tmp.md`
  - `{skillGroups.common}\skills\imp-app\assets\Wireframe-tmp.md`
  - `{skillGroups.common}\skills\imp-app\assets\config.yaml`
  - `{skillGroups.common}\references\RSDC-Standard.md`
  - `{skillGroups.common}\references\DFD.md`

- prompt 會是上面 **Prompt Examples** 所示形式之一。
  **按位置**解析它，於是一行需求絕不會被誤當成一個參數：
  - **app dir** — 第二行，一條目錄路徑。
    沒有給就問；絕不自己挑一個。
  - **command** — 第三行：`vibe`、`reverse`、`update`、`test`、`start` 或 `deploy`。
    任何其他字、或沒有字，都是一次停下，並依 **lifecycle** 順序列出這六個。
  - **target** — 只對 **deploy**，第四行：某一筆 **target list** 項目的 `name`，或用 `all` 表示每一筆。
    如果這一行缺了，就問並列出現有的名稱——指名不是選擇性的，所以絕不自己挑一個。
  - **requirements** — 對 **vibe** 與 **update**，其餘每一行散文，以使用者自己的話**逐字**保留：每一行都是被要求的一件事，而每一行都會成為一筆 **prompt log**，改寫過就會失去那個要求。
    對 **test**，其餘的散文行改為一個 **review focus**：要先看的東西。
    **reverse**、**start** 與 **deploy** 不接受任何一行，而它們其中之一上面出現散文，是一次停下、問的是原本想用哪一個 **command**。
  - **referenced notes** — 一行需求可能指名一份 wiki note（例如 `note-260824-Mo`）。
    在 `{wikiDir}\write-note\` 底下解析它，並在做任何其他事之前先讀它；它通常承載著散文只是點到為止的那些需求。
  - 結尾一個可選的 **`run step N`** 選擇器。

- 從 **app dir** 推導出 **app name**，並在使用它們之中任何一個之前，把它與它所隱含的路徑一起顯示出來——Checkpoint Dir、**MD report** 與 **design pair** 的檔名。
  讓使用者可以覆寫它。

- **讀 lifecycle record 並強制那道閘門。**
  這是整個 **lifecycle** 所倚賴的那道檢查：
  - 如果 `{appDir}\.imp-app.json` 在那裡就讀它，並從它取出 **phase** 與 `history`。
  - 一個有程式碼卻**沒有**記錄的 **app dir** 是 **adopted**：寫出記錄、以一筆指名現場發現了什麼的 `adopted` 為它的 `history` 開頭，並依磁碟上的東西設定 **phase**。
    明白地說出這個 skill 並沒有寫出那裡的東西，所以關於 **fixed shape** 的任何事都不對它做假設。
  - 一個不存在、或是空的 **app dir**，只能是一次 **vibe**，別無其他。
    對它使用任何其他 **command** 都是一次停下，說出還沒有 app。
  - **vibe**：如果 `history` 裡任何地方出現 `reverse` 就被拒絕——說出這個 app 現在有文件了，而 **update** 才是它現在改動的方式。
  - **reverse**：需要程式碼。
    如果 `history` 裡任何地方出現 `update` 就被拒絕——說出那些文件承載著原始碼無法顯示的決定，而重新推導它們會刪掉的恰恰是那些。
  - **update**：需要程式碼**與** **app documents**；如果文件不存在，說出要先執行 **reverse**。
  - **test**、**start**、**deploy**：需要程式碼。
    任何有程式碼的 **phase** 都可以。
    這三者從不因為 **lifecycle** 做過什麼而被拒絕——它們什麼都不改，所以沒有東西要那道閘門去保護。

- **只對第一次 `vibe`**，檢查 **app dir** 的歸屬：在 `skillGroups` 的各個 skills 根目錄裡搜尋另一個 config 聲稱擁有同一個目錄的 skill。
  如果有，停下、報出兩位聲稱者，並問哪一個擁有它——兩個 skill 寫同一個目錄，正是一項改動在沒有任何 diff 的情況下消失的方式。

- 如果 **app dir** 有 **app config** 就讀它，取得通訊埠以及這個 app 從它解析出來的其他東西。
  檢查那個通訊埠是不是已經被占用：有回應通常表示更早一次執行的伺服器還活著，那沒問題——把這件事說出來，並且要嘛重用它、要嘛把它停掉，而不是再啟動一個綁不上去的第二個。

- **只對 `deploy`**，透過 **skill config** 的 **target list** 把 **target** 解析成它的目的地 `appDir` 與它自己的 **app config** 值；`all` 解析成每一筆項目，依這個檔案列出它們的順序。
  一個 registry 沒有承載的名稱，是一次停下並列出它有承載的那些名稱。

- 執行 **session resolver** 來解析這個 app 的工作階段，它以 deterministic 的方式擁有這件事，於是同一個 app 的兩次呼叫不可能落在不同的目錄裡。
  - 例：`python {skillGroups.common}/skills/imp-app/scripts/resolve_session.py --app InvCov --command vibe`
  - 它重新開啟**現存最新的** `{app}-*` Checkpoint Dir，並且只在完全沒有時才打上一個新戳記——對一個 **app dir** 的第一個 **command** 開啟這個工作階段，之後每一個都加入它，無論那是哪一個 **command**。
  - 它印出一個 JSON 物件，承載 `app`、`stamp`、`checkpointDir`、`processYaml`、`mdReport`、`opened`（`created` 或 `reopened`）與 `sessions`。
    這次執行接下來逐字使用那些路徑。

- 把這次標準的 skill 呼叫存起來，供後面的 step 參考。

- 儲存 YAML checkpoint `step_0`，內含解析出來的 `wikiDir`、**app dir**（存成 `appDir`，也就是 **session resolver** 用來判斷一個被重新開啟的工作階段的那個欄位）、**app name**、**command**、**target** 與它解析成什麼、從 **lifecycle record** 讀到的 **phase** 與 `history`、這個 app dir 是否為 **adopted**、閘門判定、通訊埠與它是否被占用、逐字的 **requirements**、**referenced notes**、Node 與 Python 版本、戳記與這個工作階段是被建立還是被重新開啟、輸出路徑、step 選擇器，以及計時。
  - **`step_0` 只承載這一次呼叫**，並會被下一次覆寫。
    逐次執行的歷史屬於 **lifecycle record** 與 **prompt log**，這正是為什麼兩者都住在 **app dir** 裡而不是住在這裡。

- 顯示 **app dir**、**command**、**phase** 與那道閘門決定了什麼。
  在這個 step 裡建立 MD report 檔案是選擇性的。

## Step 1 - Vibe-code the App

- **Purpose**：讓這個 app 透過被建造而被找到——這是唯一一個散文直接變成程式碼的 phase，因為在一開始還沒有東西可以描述，而那時寫出來的文件會描述一個猜測。

- **只為 `vibe` 這個 command 執行。**
  對任何其他 **command**，跳到那個 command 路由到的 step。

- 從 YAML checkpoint 的 `step_0` 群組讀回 **app dir**、**requirements**、**phase** 與這個 app dir 是否為 **adopted**。

- **這個 step 沒有腳本**——從散文寫出一個 app 就是 vibe coding 的全部，需要判斷。

- **在對一個空 app dir 的第一輪**，用一段話說回這個 app 是為了什麼、它取代什麼、以及使用者會點什麼。
  在寫程式碼**之前**把那件事談定：之後的一切都建在它上面。
  在後面的一輪，先從 checkpoint 讀回 **prompt log**，於是這一輪從這個 app 已經是什麼開始。

- **把這個 app 寫成 fixed shape**，並從第一版就遵守 **MUST FOLLOW** 裡的生產程式碼規則，而不是當成事後的清理。
  一個 **adopted** app dir 是隨著需求觸及每個部分而一輪一輪被帶到 **fixed shape** 的，而還不在那個形狀裡的東西要被指名，而不是被假設。

- 對每一行需求，依序：
  1. **Locate.**
     指名這項改動觸及哪些檔案，並說出為什麼是那些而不是其他。
     一項同時觸及伺服器*與* **python kernel** 的改動，通常表示它們之間那條邊界擺錯了位置。
  2. **Change.**
     做那次編輯，讓 **fixed shape** 保持完整。
  3. **Test.**
     在同一輪裡，寫出或擴充那個能抓到這項改動缺席的 **unit test**。
  4. **Prove.**
     啟動這個 app、走一遍被改動的路徑、讀回來的東西，並引用它。
     **也證明第二個進入點**——require `app.js`、呼叫 `createApp()`，並在沒有綁任何通訊埠的情況下，透過它回傳的那個 handler 回應一個請求。
     一個從未被呼叫過的 **mountable handler** 是一種聲稱。
  5. **Record.**
     追加一筆 **prompt log**：逐字的需求、被觸及的檔案、寫出的測試、那份證明，以及這項改動揭露出來、卻沒有人問過的任何東西。

- **往這份輪次清單追加；絕不覆寫它。**
  `step_1` 承載一份 `rounds` 清單，每次呼叫增長一筆。
  讀它、追加、寫回去——一輪如果替換掉這份清單，就抹掉了 **reverse** 會讀的那段歷史，而沒有其他地方留有副本。

- **也把 prompt log 寫出到 `{appDir}\docs\Prompts.md`**，依輪次順序。
  它是 `docs\` 裡唯一在 **reverse** 之前就存在的部分，而它就是這個 app 為什麼長成這樣。

- **往 lifecycle record 追加**：一筆帶時間戳記的 `vibe`，以及 **phase** `vibe`。

- **說出接下來是什麼，以及什麼還沒發生。**
  還沒有 **app documents**，而那是刻意的。
  更多 **vibe** 輪次，或在這個 app 對了的時候用 **reverse**；要看它就用 **test** 或 **start**，而這個 **command** 並沒有留下任何正在跑的東西。

- 在 `step_1` 底下儲存 YAML checkpoint，內含：`appDir`、`entry`、`serverPort`、`fixedShapeFiles`、`pythonKernel`、`pageFiles`、`appConfigKeys`、`unitTests`、`rounds`（追加一筆，承載 `n`、`requirement`、`filesTouched`、`test`、`proof`、`notes`）、`roundCount`、`openIssues`，以及計時。

- 儲存 MD report 檔案。
  往一節 **Vibe** 追加（或建立它）：
  - **Summary line**：這個 app 是為了什麼、啟動它的那一道指令，以及它經過了幾輪。
  - **Rounds table**，每輪一列，欄位為：
    - **#**：輪次編號。
    - **Asked**：那行需求，壓成一行——把任何 `\|` 轉義，於是一條被引用的路徑不會把這一列切開。
    - **Changed**：被觸及的檔案。
    - **Test**：寫出或擴充的那個 unit test，或 `none` 加上為什麼。
    - **Proof**：跑了什麼、回來了什麼，引用而不是形容。
  - **Open**：需求要求了、而這個 app 還做不到的東西。

## Step 2 - Reverse-engineer the Documents

- **Purpose**：把這個 app **是**什麼用文字定下來，是從這個 app 本身推導、而不是從當初被要求的東西推導——那是一個 app 不再是一場對話、而成為後來的讀者能拿來對照檢查的東西的那個時點。

- **只為 `reverse` 這個 command 執行。**
  對任何其他 **command**，跳到那個 command 路由到的 step。

- 從 YAML checkpoint 的 `step_0` 與 `step_1` 群組讀回 **app dir**、**app name** 與 **prompt log**。
  一個 **adopted** app dir 沒有 **prompt log**；把這件事說出來——設計就只從原始碼推導。

- **這個 step 沒有腳本**——**design pair** 由 **gen-rsdc-app** 推導，而讀一個正在跑的頁面是判斷；一個被要求做這兩件事的程式，只會是在聲稱它做了。

- **用 gen-rsdc-app 寫出 design pair。**
  對 **app dir** 執行它，指名 **app name**、以 `{appDir}\docs` 作為這一對寫到哪裡，以及 **prompt log**——對一個 **adopted** app dir 則是 `none`：

  ```
  /gen-rsdc-app
  {appDir}
  {app name}
  {appDir}\docs
  {appDir}\docs\Prompts.md
  ```

  - 它先拿它的 design template 對照 **RSDC standard**，template 落後時，在寫出任何東西之前停下。
    在那裡停下，這個 **command** 也跟著停下：把這件事說出來，並說明 template 由 **gen-rsdc-app** 負責跟上標準。
  - 它會整份取代 `{appDir}\docs\` 裡已經有的 **design pair**——閘門只在第一次 **update** 之前允許這麼做。
  - 它從原始碼推導設計，而不是從 **prompt log**，並把兩者之間每一項不一致記成一項發現。
    讀回它交回的東西——**components**、發現、缺陷、**verification obligations**、它檢查英文半邊的結果，以及 `chinese` skill 對 twin 的回報——供下面的 checkpoint 與報告使用。
  - 它所執行的 `chinese` skill 會問要不要 commit **design pair**：把這個問題轉給使用者。
    那個 commit 只含這一對，而不論回答是什麼，這個 **command** 都繼續往下做。

- **把正在跑的頁面掃描進 wireframe pair**——`{appDir}\docs\Wireframe.md` 與 `Wireframe-tw.md`，兩份在同一次執行裡，依 `Wireframe-tmp.md` 承載的形狀：
  - 啟動這個 app、在瀏覽器裡打開它的頁面，並讀那份**即時 DOM**——不是標記檔案。
    一份從標記寫出來的清冊，列的是作者相信這個頁面有什麼，而搞清楚實情正是這次掃描的重點。
  - 從上到下走過這個頁面，一個元素一個項目符號，每一個都標上它的種類——`[Panel]`、`[Button]`、`[Select]`、`[Input]`、`[Text]` 等等——並帶著使用者實際看到的那個標籤，不是元素的 id。
  - 把每一張表格都畫成一張有它自己欄位的表格，依這個頁面顯示它們的順序。
  - 記下那些**可見狀態**：哪些部分在某件事發生之前是隱藏的，以及什麼讓每一個出現。
    在把它寫下來之前，把這個頁面操作到足以到達每一個狀態——一份只有開場畫面的 wireframe，記錄的是這個 app 的一小部分。
  - 掃描揭露出缺陷的地方，在 wireframe 裡把它寫成一筆缺陷，**並且**在 design pair 的 Defects 裡也寫成一筆。
    一個顯示了錯誤值的元素仍然是一個元素；wireframe 把兩件事實都記下來。

- **往 lifecycle record 追加**：一筆帶時間戳記的 `reverse`，以及 **phase** `reverse`。
  如果這是第一次，明白地說出 **vibe** 現在對這個 **app dir** 關上了，而從這裡起 **update** 才是它改動的方式。

- **說出接下來是什麼，以及什麼還沒發生。**
  這個 **command** 寫了文件、沒有改任何程式碼，而且沒有留下任何正在跑的東西。
  下一個 **command** 是 **test**，或是用 **update** 做對著文件的第一次改動。

- 在 `step_2` 底下儲存 YAML checkpoint，內含：`components`、`designPair`、`wireframePair`、`sectionsWritten`、`wireframeScan`（這個頁面是怎麼被到達的、以及哪些可見狀態被打開過）、`findings`（原始碼與 **prompt log** 之間每一項不一致）、`defects`、`verificationObligations`、被追加的 **lifecycle record**，以及計時。

- 儲存 MD report 檔案。
  追加並顯示一節 **Documents**：
  - **Summary line**：寫出的那四份文件、它們指名了幾個 **components**、這次掃描產出了幾項發現與幾項缺陷，以及沒有任何程式碼改動。
  - **Documents line**：**design pair** 與 **wireframe pair** 作為四個連結，附上每一對的兩個半邊是以哪些章節計數比對過的。
  - **Components table**，欄位為：
    - **Component**：它在 design pair 裡的名字。
    - **File**：它的原始碼在 **app dir** 裡住在哪裡。
    - **Obligations**：提到它的那些 **verification obligations** 的主張，尚未證明的每一項標 *not verified*。
  - **Findings table**，欄位為：
    - **Asked for**：那筆 **prompt log**，對一個 **adopted** app dir 則是 `—`。
    - **What the code does**
    - **Recorded as**：現在承載它的那一節。

## Step 3 - Update the Documents then the Code

- **Purpose**：依那個順序把一項改動穿過設計帶進程式碼，而那是唯一一個事後還讓文件值得一讀的順序。

- **只為 `update` 這個 command 執行。**
  對任何其他 **command**，跳到那個 command 路由到的 step。

- 從 YAML checkpoint 的 `step_0` 群組讀回 **app dir** 與 **requirements**，並在改動任何東西之前先讀 **app documents** 本身。

- **這個 step 沒有腳本**——決定一行需求是什麼意思、它在設計裡屬於哪裡、以及它隱含什麼程式碼，都是判斷。

- **對每一行需求，先決定它落在 app documents 的哪裡**，然後把它寫在那裡：
  - **依重繪測試安排它，而不是依主題。**
    一個在頁面換顏色時仍然為真的陳述，是一次 **design pair** 改動——某個編號的章節，被修改或新增。
    一個那時會不再為真的陳述，屬於 **wireframe pair**，跟它所描述的那些元素放在一起。
  - 所以：這個 app 做什麼、一個值對讀者*意味*什麼、以及一項改動的代價是什麼，都是 **design pair**。
    顏色、hover、字體與這個頁面的元素清冊是 **wireframe pair**。
    「這個頁面顯示什麼」橫跨兩者，這正是為什麼那道測試是那個陳述的措辭、而不是它的主題。
  - 一項在文件裡哪裡都放不進去的改動，也是一項不屬於程式碼的改動。
    把這件事說出來並詢問，而不是只把它寫進程式碼。
  - **在這次執行裡寫下每一對的兩個半邊**，用相同的編號。
  - **在文件裡陳述一項移除了某樣東西的改動的代價**：這個 app 從此做不到什麼，以及為什麼那是值得的。
  - **兩份文件都不得指名另一份。**
    各自陳述自己的範圍；一條需要另一份的理由的規則，會在自己這邊、用自己的話把那個理由完整給出。
    另一份檔案裡的一個章節編號，是一條會在沒有人注意到的情況下腐爛的連結。

- **然後把程式碼改成相符**，編輯 **app dir** 自己的檔案，並讓 **fixed shape** 保持完整。
  一個新的**值**進 **app config**；一個新的**行為**進 **python kernel**。

- **在同一輪裡寫出或擴充那個能抓到這項改動缺席的 unit test**，並新增或修改提到所改 **component** 的那些 **verification obligations**，涵蓋這項改動讓那個 component 新增、要被證明的東西。

- **重新證明這項改動可能弄壞的東西**，用一個備用通訊埠、對著 workspace `temp\` 底下一份 **app dir** 的拋棄式副本——絕不用真正的通訊埠，也絕不對著 **app dir** 本身。
  重跑提到這項改動觸及之 **component** 的那些 **verification obligations**，以及它改過的那些檔案的 **unit tests**。

- **往 lifecycle record 追加**：一筆帶時間戳記的 `update`，以及 **phase** `update`。
  如果這是第一次，明白地說出 **reverse** 現在對這個 **app dir** 關上了。

- **把這一輪追加進 prompt log**，在 checkpoint 裡與在 `{appDir}\docs\Prompts.md` 裡。

- **說出接下來是什麼，並且精確說出上面那些探測證明了什麼、沒證明什麼。**
  它們是對著一份拋棄式副本跑的，所以它們證明的是這項改動沒有弄壞它們所涵蓋的東西——不是 **app dir** 提供得了服務。
  下一個 **command** 是 **test**，或用 **start** 單純把它帶起來。

- 在 `step_3` 底下儲存 YAML checkpoint，內含：`updates`（追加一筆，承載 `n`、`requirement`、`documentSections`、`filesChanged`、`test`、`probes`、`results`、`costsRecorded`）、`updateCount`、`verificationObligations`、被追加的 **lifecycle record**，以及計時。

- 儲存 MD report 檔案。
  往一節 **Update** 追加（或建立它）：
  - **Summary line**：這一輪承載了幾行需求、這次執行是否就是關上 **reverse** 的那一次，以及 **app dir** 本身並沒有被提供服務過。
  - **Changes table**，欄位為：
    - **Asked**：使用者自己的話。
    - **Document**：它被寫進那一對的哪一節。
    - **Code**：它接著改了哪些 app dir 檔案。
    - **Test**：寫出或擴充的那個 unit test。
    - **Proved by**：為它重跑的那次探測，或為什麼不需要。

## Step 4 - Test the App

- **Purpose**：這是唯一一個追問這個 app 對不對的地方，用的是回答不同問題的那兩種方式——一台機器能檢查它的什麼，以及只有一位看著頁面的讀者才看得見的什麼。

- **只為 `test` 這個 command 執行。**
  沒有其他 **command** 會判斷這個 app。

- 從 YAML checkpoint 的 `step_0` 群組讀回 **app dir**、通訊埠與任何 **review focus**。

- **這個 step 有兩個半邊，而它們依那個順序執行：先被檢查的，再被判斷的。**
  前者是腳本化且 deterministic 的；後者兩者都不是，而且做不到。
  **被檢查的那半邊通過不等於這個 step 通過**——每一個 **unit test** 在一個沒有人會想用的頁面上都會通過，那正是第二個半邊存在的全部理由。

### The checked half

- **執行 test runner**，它擁有發現與執行，於是一個測試不可能被無聲地跳過。
  - 例：`python {skillGroups.common}/skills/imp-app/scripts/run_tests.py --app-dir artifacts/InvCov --out "checkpoints/imp-app/InvCov-260924-1130"`
  - 它發現 `{appDir}\tests\` 底下的 **unit tests**，用 `unittest` 那些對著 **python kernel** 跑、用 `node:test` 那些對著伺服器跑，並印出一份 JSON 結果，承載每個測試的結果、各項計數、每一個沒有任何測試提到過的原始檔，以及每一個命名成兩個 runner 都不會發現的測試檔案。
  - 它把那份結果存成輸出目錄裡的 `unit-tests.json`。
  - **當有測試失敗、或什麼都沒跑到時，它以非零離開。**
    那是這個 app 的判定，不是這個工具的故障：讀那份結果並繼續這個 step，而不是重跑它。
  - **一個沒有任何測試提到的檔案，是關於這些測試的事實，不是一項覆蓋率聲稱。**
    一個*確實*被提到的檔案是否真的被操作過是判斷，而這個 runner 刻意不斷言它——請自己把每一項結果對映到某個 **component**：找出 Proven by 或 Performed by 提到該測試的那一項 **verification obligation**，取那一列提到的 component。
- **零個測試就是零，絕不是綠燈。**
  一個 runner 找不到任何測試提到的原始檔，會在報告裡被指名為未被測試，而一次完全沒找到任何測試的執行是一次停下、說出要寫哪些測試——不是通過。
- **讀每一個失敗，並引用它說了什麼。**
  一個失敗是關於這個 app 的發現，不是關於這個 runner 的，而它在這裡被指名而不是被修掉：修它是一次 **update**，或在 **vibe** 還開著時是一次 **vibe**。

### The judged half

- **以背景行程啟動伺服器**並讓它繼續跑——它是一個伺服器，不是一支跑一次就結束的腳本，而這半邊是在它有回應時開始，不是在那道指令回傳時。
  - 例：`node {appDir}/server.js`
  - 使用絕對路徑。
    這個 app 把每一條路徑都對著它自己的目錄解析，所以 **app dir** 是它唯一跑得起來的地方。
  - 如果那個通訊埠已經被占用，先把那個伺服器停掉，而不是啟動一個綁不上去的第二個。
- **在繼續之前確認伺服器有回應。**
  詢問 `{server origin}/healthz`，並記下它說它解析出了什麼。
- **在一個真正的瀏覽器裡、像一個使用者那樣驅動這個頁面**——`playwright-cli` skill 就是做法。
  一次只抓了 HTML 的 **UI test** 記錄為**沒有被執行過**：一個狀態碼不是一種外觀，而一份被抓下來的樣式表不等於一份讀起來順的樣式表。
  - 先看 **review focus** 要求要看的東西，再看整個頁面。
  - 操作 **wireframe pair** 為之記下了**可見狀態**的每一個互動，並在判斷它之前到達每一個狀態。
  - 用看的來確認，而不是靠相信某個計數：顯示出來的值就是 **python kernel** 回傳的那些、這個頁面載入的每一個位址都在 **server origin** 上、而且沒有任何東西是從它之外抓來的。
- **在相信一次探測報告了什麼之前，先追問它能證明什麼。**
  一次不可能失敗的檢查、或一次被瀏覽器替這個 app 悄悄滿足掉的檢查，讀起來跟一次通過了的檢查一模一樣——一次被自動跟隨的轉址、一個用錯大小寫讀到的標頭、一張渲染起來跟被篩選過的一模一樣的空表格。
- **對照 wireframe pair 核對這個頁面**，一個元素一個元素——它是一份規範性的清冊，所以它標記為必要的每一列都必須在這個頁面上：
  - 一個缺了 wireframe 要求的東西的頁面是一項缺陷。
    指名它；不要在這裡修它。
  - 一個帶著 wireframe 沒有列出的東西的頁面也是一項缺陷：要嘛那個元素該走，要嘛 wireframe 本來就該把它寫上。
    指名該改的是哪一端，然後放著。
  - **報告它並停下——這個 command 無法記錄它。**
    wireframe 是一份 **app document**，而只有 **update** 寫那些。
    所以在這裡發現的一項缺陷，會晚一個 **command** 才被寫下來，而這份報告必須承載足夠的東西，讓那次 **update** 不必再觀察一次就寫得出來。
- 不要修這個 app、不要重啟另一個伺服器，也不要編輯 **app dir** 裡的任何東西。

- 在 `step_4` 底下儲存 YAML checkpoint，內含：`tests`（每次呼叫追加一筆，承載 **server origin**、綁定的通訊埠與主機、行程 id、Node 與 Python 版本、`/healthz` 回應、unit test 各項計數與每一個失敗、這個頁面是在哪個瀏覽器裡被驅動的、到達過的每一個**可見狀態**、wireframe 核對、發現的那些缺陷、整體判定與建議的下一個 **command**）、`testCount`，以及計時。

- 儲存 MD report 檔案。
  往一節 **Test** 追加（或建立它）：
  - **Summary line**：幾個 **unit tests** 通過與失敗、幾個 **components** 一個都沒有、**UI test** 是在什麼裡被驅動的、產出了幾項缺陷，以及下一個是哪一個 **command**。
  - **Unit tests table**，欄位為：
    - **Test**：這個測試在 runner 報告裡的名字。
    - **Component**：它涵蓋哪一個 **component**，從 Proven by 或 Performed by 提到該測試的那一項 **verification obligation** 讀出來——這件事不是 runner 決定的。
    - **Result**：pass、fail 加上它說了什麼、`skip` 加上為什麼，或對一個沒有任何東西指名過的原始檔給 `no test mentions this file`。
  - **UI test table**，欄位為：
    - **Interaction**：對這個頁面做了什麼。
    - **Expected**：**wireframe pair** 或 **design pair** 說接下來應該怎樣。
    - **Observed**：這個頁面實際顯示了什麼，引用而不是形容。
    - **Verdict**
  - **Defects**：每一項、它是在哪裡被看到的，以及為它一次 **update** 必須改哪一份文件。
  - **Notes**：任何是看到而不是推斷出來的東西，以及任何 **app documents** 已經接受為代價而不是缺陷的東西，並如此指名，於是後來的讀者不會再把它翻出來。

## Step 5 - Start the App

- **Purpose**：為只想用這個 app 的人把它帶起來，並且不向他們多收任何東西——一次以對這個頁面的判定收尾的 **start**，已經悄悄變成一次 **test**，而那比兩者都更糟，因為呼叫的人要的既不是這個也不是那個。

- **只為 `start` 這個 command 執行。**

- 從 YAML checkpoint 的 `step_0` 群組讀回 **app dir** 與通訊埠。

- **這個 step 沒有腳本**——它是一道指令與一個請求，而把那兩者包進一個程式裡，只會藏住是哪一個失敗了。

- **以背景行程啟動伺服器**並讓它繼續跑。
  - 例：`node {appDir}/server.js`
  - 使用絕對路徑，理由就是這個 app 用那種方式解析它自己的路徑。
  - 如果那個通訊埠已經被占用，把這件事說出來，並且要嘛重用那個伺服器、要嘛把它停掉——絕不啟動一個綁不上去的第二個。

- **詢問 `{server origin}/healthz`、報出 server origin，然後停下。**
  這個 **command** 不打開頁面、不拿它跟任何東西比對，也不做出任何判定。
  如果 `/healthz` 沒有回應，說出它說了什麼、或說它什麼都沒說，然後就停在那裡——診斷它是一次 **test**。

- 在 `step_5` 底下儲存 YAML checkpoint，內含：`starts`（追加一筆，承載 **server origin**、綁定的通訊埠與主機、行程 id、Node 與 Python 版本與 `/healthz` 回應）、`startCount`，以及計時。

- 儲存 MD report 檔案。
  往一節 **Start** 追加（或建立它）：**一行摘要，別無其他**——**server origin** 與 `/healthz` 報告了什麼。
  沒有表格、沒有判定，因為這個 **command** 什麼都沒看。

## Step 6 - Deploy the App to a Target

- **Purpose**：把這個 app 放到它實際會被使用的地方，用那個目的地需要的值、而不是 **app dir** 開發時對著的那些值，並證明這次送達，而不是假設它。

- **只為 `deploy` 這個 command 執行。**

- 從 YAML checkpoint 的 `step_0` 群組讀回 **app dir**、**target** 與它解析成什麼。

- **如果 phase 是 `vibe`，在送出之前把這件事說出來**：要出去的東西沒有 **app documents**，所以另一端沒有人能拿它去對照任何東西檢查。
  那是一個警告而不是一次拒絕——要不要出貨是使用者的決定，不是這個 skill 的。

- **先證明這個 app 在這裡跑得起來，再把它送到那裡。**
  啟動它、詢問 `{server origin}/healthz`，然後把它停掉。
  把一個在本地啟動不了的 app 送出去，是把同一個失敗送到一個更難除錯的地方。

- **執行 deploy tool**，它擁有那些複製，於是同一批檔案以同一種方式抵達每一個 **target**。
  - 例：`python {skillGroups.common}/skills/imp-app/scripts/deploy_app.py --app-dir artifacts/InvCov --target ftp-server --out "checkpoints/imp-app/InvCov-260924-1130"`——`--target` 可以重複，而 `--all` 是每一個登記過的。
  - 它透過 **target list** 解析每一個 **target**、把程式碼複製到那筆項目的 `appDir`、用這個 target 的值蓋過 **app dir** 的值寫出那個目的地自己的 **app config**，並印出一份 JSON 清單，列出它寫了什麼、什麼本來就已經是最新的、以及它放著沒動什麼。
    它為每一個 target 在輸出目錄裡存一份 `deploy-{target}.json`。
  - **它送的是程式碼，而且只有程式碼**：`server.js`、`app.js`、`start.cmd`、`README.txt`、`public\` 與 `scripts\`，加上它寫出的那份 **app config**。
    **app dir** 的 `docs\`、`tests\` 與 **lifecycle record** 留在 **app dir** 裡——那是這個 app 的歷史與它的存證來源，所以一個在某個 **target** 上發現的故障是改在 **app dir** 裡重現、而不是在那裡重現，而那也是它該去的地方，因為修正無論如何都是在那裡寫的。
    一個 **target** 自己的 `data\`、`logs\` 與 `temp\` 是**那台機器的**——它下載的東西、它自己的執行印出來的東西——覆蓋它們會拿掉它為自己做過的工作。
  - **一個檔案在 target 上是最新的，條件是它的大小與它的修改時間都等於 app dir 的**，而只要有一項不同就複製它。
    兩者可以比較，只因為複製會把來源的時間帶過去，所以兩個值都來自**這台**機器的時鐘，而兩台機器的時鐘從不進入這個比較——那正是單純用「target 上那份比較舊」去測會搞錯的地方。
    測相等而不是測「較新」，也正是還能抓到一份被改寫成相同長度的來源、以及還能取代一次在 **target** 上做的手工編輯、而不是把它誤認為比 **app dir** 更新的東西的原因。
    `--force` 不管那個比較，把每一個檔案都複製。
  - **一個到不了的 target 不會擋住其他的。**
    每一個各自被報告，而離開碼說出是否有任何一個失敗了——一個今天沒有掛上的 share，不構成放棄那些掛上了的機器的理由。
  - **它絕不寫進 app dir**，也絕不從 prompt 取用目的地路徑。
  - **命令列上不放機密。**
    一個需要憑證的目的地，是由某個已經持有它的東西抵達的——一個掛載好的 share、一把 **target list** 指名的金鑰——絕不是由一個放在引數裡的密碼，因為這台機器上每一個其他行程都讀得到它。
  - **`--dry-run` 規劃並清列這次送達而不寫出任何東西**，那就是一筆新的 **target** 項目在被信任之前被檢查的方式。

- **然後確認抵達了什麼。**
  如果這個 app 可以從這裡在那個 **target** 上被啟動，就啟動它、詢問 `{target origin}/healthz`，並報出兩個 origin。
  如果不行，明白地說出這次送達是**只以那份清單與那次檔案比較**驗證的，而且在那裡**沒有任何東西被觀察到正在跑**——一個被複製過去的檔案不是一個正在跑的 app。
  只要有任何東西被寫出，就說出那個 **target** 上的伺服器必須重啟，因為 Node 不會重新載入 `server.js`。

- **往 lifecycle record 追加**：一筆帶時間戳記、並帶著它去到的那個 **target** 的 `deploy`。
  **phase** 不改變：一次 **deploy** 不改變關於這個 app 是什麼的任何事。

- 在 `step_6` 底下儲存 YAML checkpoint，內含：`deploys`（每一個 **target** 追加一筆，承載它的 `name` 與目的地 `appDir`、它是否到得了、**target origin**、寫出的那些檔案與大小、本來就已經最新的那些檔案、在那裡被放著沒動的東西、為那個目的地寫出的那些 **app config** 值與它們取代了 **app dir** 的哪些值、本地那份證明，以及抵達是怎麼被確認的）、`deployCount`、`phaseAtDeploy`、被追加的 **lifecycle record**，以及計時。

- 儲存 MD report 檔案。
  往一節 **Deploy** 追加（或建立它）：
  - **Summary line**：每一個 **target**、這個 app 現在坐在它上面的哪裡、寫出了幾個檔案與幾個本來就已經是最新的、在那裡是否被觀察到正在跑，以及它是從哪一個 **phase** 被部署出去的——包含那個警告，當那個 phase 是 `vibe` 時。
  - **Files table**，欄位為：
    - **File**：相對於目的地 `appDir` 的路徑。
    - **Size**
    - **State**：written、already current，或 failed 加上它說了什麼。
  - **Verification table**，欄位為：
    - **Check**：被詢問了什麼——本地那次啟動、那份清單、大小與時間的比較、遠端的 `/healthz`。
    - **Result**：回來了什麼，引用而不是形容，或 `not run` 加上為什麼。
  - **Notes**：**app dir** 的 **app config** 與為每一個 **target** 寫出的那一份之間有什麼不同、在那台機器上有什麼被放著沒動，以及那個目的地需要、而這個 **command** 沒有放進去的任何東西。
