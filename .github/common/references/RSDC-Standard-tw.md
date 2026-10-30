# ArtifactFlowAgent: The Responsibilities of the Four RSDC Chapters

> Version: 261016
> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-14`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-30`  `8cc2e2061175`

> 本檔案以 ASD-STE100 Simplified Technical English（STE）第 9 版寫成。
> 技術用字：activity、address、answer、app、architecture、argument、authorization、boundary、branch、button、call、caller、chapter、checklist、code label、column、command、configuration、constraining rule、content、contract、cost、coverage、Dataflow、day、decimal、default、defect、derived value、description、development、diagram、directory、document、endpoint、environment、exception path、field、file、file-locking mechanism、flag、flowchart、git、goal、granting rule、guideline、heading、hint、history、import、kernel、key、label、layout、legend、library、line、link、list、logic、mapping、mermaid、metadata、module、network、node、notation、noun、operating system、orphan、parallelogram、parameter、parse、path、pathlib、platform、process、project、proof、query、question、record、refactor、request、researcher、response、retries、retrieval、rounding、schema、scope、screen、section、separator、server、skill、specification、spelling、stage、standard、status、style、subsection、syntax、table、task runner、template、term、terminology、text、title、topic、twin、user、verdict、verification、version、viewer、vocabularies、word、writer。

RSDC 是 **Requirements**、**Specification**、**Design** 與 **Coding** 的簡稱。
一份 RSDC 有四**章**，這四項各占一章。
各章的編號是 1 到 4。
章的數量與順序都不變。

**節**是章的一部分。
每一節都有編號 N.M，例如 2.2。
節以下的部分沒有編號。

RSDC-Standard.md 以 ArtifactFlowAgent 專案的 RSDC 為範例。
它提供的標準，適用於你從此以後寫的所有 RSDC。

本版取代 261010。
git 歷史保留先前的版本。
RSDC-Standard.md 文末的「Changes in This Version」一節，寫出各項改動及其原因。
同樣位於文末的「Versioning」一節，寫出新版本的規則。

# Core Writing Principle: One-way Dependency

撰寫所有文件時都要依照下列規則，並完全遵守這些規則。
這些規則讓 system 架構的各層保持清楚。
它們也讓每一層的邏輯與其他層隔開。

- **前章不得提及後章的內容**：
  - 在 Requirements 中，不要寫出 Specification 的內容（例如某個 Artifact type）。
  - 在 Specification 中，只用介面來指認 component。
    介面是外部 system 呼叫的 API 或 CLI，外部 system 例如 AI agent 或 skill。
    不要用 component 的內部來指認它（例如某個 Manager 模組）。
  - 在 Design 中，不要寫出 Coding 的語法（例如某個程式庫或 type hint）。
- **由抽象至具體**：每一章只能使用它前一章的內容。
- **每條規則都要寫出違反它會怎樣**：例如，一條規則可以是「查詢找不到結果時，畫面要告訴使用者。」
  這條規則接著說出 system 不遵守它時的後果：「畫面若沒有告訴使用者，使用者就無法知道是查詢找不到結果，還是查詢沒有正確運作。」
  規則的這個後果也給出了測法。
  讓查詢出錯，再檢查畫面。
  如果畫面告訴使用者查詢找不到結果，程式碼就是錯的。

  只測一般情況的測試，找不到只要清單是空的就顯示「沒有結果」的程式碼。
  那段程式碼只是碰巧才正確。

  畫面改變時，規則的這個後果也仍然成立。
  不論畫面怎麼改，使用者都必須仍然分得出這兩種情況。
- **No Forward Reference**：一節不得引用編號比它大的章或節。
  一段文字，例如「參閱下面那一節」，看似無害。
  但這樣一來，讀者不看另一節就讀不懂這一節。
  若甲節少了乙節的內容就不完整，就把那些內容放進甲節。
  或者，把甲節排在乙節之後。

# 1. Requirements — "What problem does this solve?"

本章寫出專案的目標，以及專案目前的問題。
**本章不得說明 system 如何完成工作，也不得寫出 system 的架構。**

- **Target Users**：使用本 system 的人或 system（例如研究人員或 AI agent）。
- **Core Vision**：system 必須提供、作為它所有工作目標的最高價值，以及使 system 有存在必要的原因。
- **Current Pain Points**：專案目前所用流程中的問題。
  這些問題讓工作變慢，或讓邏輯不清楚。
- **System Goals**：清楚列出 system 必須具備的性質。
  例如彼此隔開的邏輯，或一條能從頭到尾追蹤的完整流程。

**System Goals 的每一條目標，都必須在第 2 章有對應的規則。**
目標寫出 system 必須得到的結果。
規則寫出 system 因為這個目標而必須遵守的限制。
如果 Specification 沒有某個目標的規則，這個目標就沒有效力。
RSDC 中沒有任何部分能確保 system 得到那個目標的結果。

第 2 章 Invariants 結尾的目標表，列出保有每個目標的規則。

# 2. Specification — "What are the system rules?"

本章寫出 system 的標準與限制。
它們是所有 component 都必須遵守的「法律」。
本章可以規定 system 做「什麼」，但不得規定它「長什麼樣子」。

例如，本章可以規定 system 不得顯示某一項資料。
本章可以規定使用者必須能夠發起某個操作。
但本章不得規定使用者是用按鈕、連結還是指令來發起這個操作。

**判準**：設想一個改動，以及一個在改動之前會通過的驗證。
如果這個改動讓那個驗證不再通過，這個改動就是規則，放在本章。
如果這個改動只是換個說法或移動文字，它就不是規則。
這樣的改動放在 Design 或 Coding。

- **Terminology**：後面各項會用到、卻沒有任何一項加以說明的名詞。
  例如 system 外部的 role（caller），或一個位置（一次執行寫入的目錄）。
  每個 term 只說明一次，而且在第一次使用之前說明。
  term 不是資料的名稱，因為 Artifact Types 在 Terminology 之後才寫出資料。
  Hierarchy 的單位、stage、代碼標籤、設定的 key、衍生值與 component，各有不同的項。
  不要把它們放在 Terminology。
- **Hierarchy**：system 的使用者用來組合出 system 的單位，分成哪些層級。
  以及哪一層包含哪一層（例如 Lambda、Flow 與 Agent 三層之間的關係）。
  只有當使用者用這類單位組合 system 時，才寫這一項。
  system 沒有這類單位時，不寫這一項。

  有些分層只存在於 system 的內部架構，例如把工作交給 kernel 的 server。
  這些分層不是 Hierarchy。
  你可以改變這些分層的順序，而改動之前通過的驗證都會繼續通過。
  所以依本章開頭的判準，這些分層屬於 Design 的 Core Component Responsibilities。
- **Artifact Types**：各種資料物件（例如 Sequence、Dataset、Archive）。
  對每一種，寫出它所承載的資訊、它的用途，以及內容上的限制。
  由誰寫入資料、由誰讀取資料，由 Dataflow 說明。
- **Dataflow**：資料如何在 system 的活動之間移動。
  寫出各個 **stage**，以及每個 stage 讀取與寫入的資料。
  說明每一份 **record** 由誰寫入、誰可以讀取。
  說明由資料而來的先後順序。

  把 Dataflow 畫成 DFD。
  [DFD.md](DFD.md) 寫出 DFD 的資料種類、形狀與線型。
  它也寫出每一張 DFD 都要檢查的缺陷。
  本項與相鄰各項的分界如下：
  - 「Hierarchy」說明有哪些單位，以及哪個單位包含哪個單位。
    單位只以 stage 讀取的資料出現在本項中（例如它的配置），而不是以 stage 的身分出現。
  - 「Artifact Types」說明資料的**種類**。
    本項說明資料**往哪裡走**。
  - 第 3 章的「Execution Flow」以 component 的名稱，說明 system 在執行時的運作。
    本項以活動的名稱，說明同樣的運作。
    第 3 章中兩套詞彙之間的對應，把這兩項接在一起。

  - **必備內容**：
    1. **DFD**：各 stage 的圖，system 外部的所有 role 都畫在圖上。
       只有 DFD 說出每個 stage 讀寫的資料。
       只有 DFD 說出每一項資料由誰寫入、由誰讀取，以及每一項資料屬於哪一種。
       不要再寫一張表重複這些資訊。
       第二份副本會變得和圖不一樣，而且沒有人會發現這個差異。
    2. **Data Read/Write Rules**：關於資料、而圖畫不出來的規則。
       說明每條規則適用於哪裡。
       說明 stage 是否把一項資料整份寫入。
       說明一項資料在 stage 寫入之後是否保持唯讀。
       說明由誰移除它。
    3. **Order Imposed by the Data**：每一條先後順序，都要寫出造成它的資料。
       這一節也必須明白寫出「沒有任何 stage 讀取後面 stage 寫入的東西」。
    4. **Exception Paths**：寫出下列三條路徑：
       - 在結束之前停止的路徑。
       - 結束時沒有寫入任何資料的路徑。
       - 從流程中段某個 stage 重新開始的路徑（例如只重做最後幾個 stage 的路徑）。
  - **stage 的內部**：不要在本項畫出 stage 的內部。
    stage 的內部是它的各個部分與它們的順序。
    也包括每個部分讀取、再交給下一個部分的資料。
    這是 component 完成這個 stage 工作的方式，屬於第 3 章的 Execution Flow。

    在某些情況下，stage 內部的某個順序就是規則。
    在 stage 各部分之間移動的資料，也可能是規則。
    某個驗證必須依靠這類規則。
    例如，stage 必須先完成某項檢查，才能寫入資料。

    在本章用文字寫出這樣的規則。
    只用整個 stage 邊界上的輸入與輸出，以及它們的先後順序，來說明這條規則。
    把它和相關的規則放在一起：某條 Derivation Rule、某條 Invariant，或某條 exception path。
    如果把這個 stage 畫成圖，圖上只會畫出遵守這條規則的一種做法。
    那張圖的其他部分都不是規則。
  - **命名**：每個 stage 都以它的活動命名，不以 component 命名。
    每一份 record 都用 system 所用的名稱。
    檔名也可以。
    不要用寫入它的模組名稱。
    用那個名稱，就等於 Specification 搶在 Design 之前替 Design 做了決定。

    圖也用到其他名稱。
    例如外部 role 的名稱、一項資料的名稱，以及圖中畫成一個節點的一組輸入的名稱。
    這些名稱都要在 Dataflow 之前，由 Terminology 或 Artifact Types 說明。
    如果 Dataflow 用了某個名稱，卻沒有任何一節說明它，讀者就無法知道這個名稱指的是什麼。
  - **位置**：本項提供後面各節所用的 stage 與 record 的名稱。
    依「No Forward Reference」，本項要排在所有使用這些名稱的節之前。
    不要給它一個固定不變的節號。
- **Naming and Data Structures**：名稱的標準規則（例如用 # 當分隔符），以及解析元數據的規則。
  - **代碼標籤是契約**：代碼標籤是一段不會改變的文字。
    程式寫出它，讀者精確地比對它。
    例如狀態、種類與 verdict。
    代碼標籤不是畫面上控制項的文字。
    每個存放代碼標籤的欄位，都要列出它可能存放的所有代碼標籤。
    代碼標籤的寫法一旦不同，就沒有讀者認得這個值，system 中也沒有任何部分會告知這個差異。
  - **每個數字都寫明精度**：說明數字在小數點後保留幾位，以及它的進位方式。
    如果兩個讀者對同一個值用了不同的進位方式，他們對這個值的看法就不一致。
    於是兩個讀者拿這個值和某個界限比較時，可能得到不同的結果。
- **Config Schemas**：system 讀取的每一份配置檔必須包含的欄位，以及這些欄位的邏輯限制。
  完整寫出這些欄位（例如 I/O 契約，以及向 AI 說明它的欄位）。
  system 有 Hierarchy 時，每個層級各有一份 schema（例如 Lambda、Flow 與 Agent 各自的 config.yaml）。
- **Derivation Rules**：system 如何取得那些**不是直接觀察到**的值。
  寫出 system 使用各來源的先後順序，以及造成這個順序的成本。
  也要說明 **system 不得拿來替代的項目**。
  一個值若有多個來源能提供，本項決定這些來源的順序。

  若沒有任何來源能提供，本項說明如何標示這個缺少的值。
  不要讓一個看似正確的近似值頂替它。
  在整份文件中，程式碼常常不遵守這類規則，而這些錯誤最難察覺。
  原因是錯誤的替代值看起來總是正確的。
- **Presentation Contract**：說明 **system 可以呈現哪些資料、呈現給哪些使用者**。
  說明**使用者必須能夠發起哪些操作**。
  說明**使用者看到的資料，是否與 system 所做的工作一致**。
  - **每個專案都必須回答下列八個問題。**
    這些問題來自 system 的實際使用。
    它們不是一張要套用的規則檢查清單。
    **不同的 system 給出不同的答案，但問題是一樣的。**
    1. 沒有結果時，畫面顯示哪些資料？
       哪個位置顯示 system 沒有納入的項目數量？
    2. 使用者不需協助就能啟動哪些流程？
       使用者不能啟動的每個流程，是什麼原因阻止它？
    3. 每一個取得動作，都有人或測試證明它在使用者的環境中正確運作嗎？
    4. 如果外部來源也有這份素材，system 能交出它的位址嗎？
    5. 檢視範圍縮小時，畫面上的數字與下一個操作的範圍一致嗎？
    6. 對許多項目進行的操作，數量上限是多少？
       數量太大時，system 如何擋下？
       操作會不會在結束之前停下，留下不完整的結果？
    7. system 擋下使用者的操作之後，使用者下一步該做什麼？
    8. 預設有哪些人或 system 可以存取這個 system？
       可以存取的變多時，誰會知道？

    這些問題不預設答案。
    一個 system 可以正當地回答「沒有外部來源」。
    但一個**沒有人檢視過**的問題，就是 Specification 缺少的一塊。
  - **所見即所為**：使用者依據所看到的資料選擇要做的操作。
    因此，**畫面顯示的範圍，必須和操作的範圍完全相同**。

    畫面上的數字若與選取不一致，使用者核可的是一組項目。
    但使用者收到的卻是另一組。
    system 依該範圍計算的每一道安全限制（例如容量上限）也會跟著失效。
    這不是顯示上的錯誤。
    這是授權上的錯誤。
  - 本項**不包含**版面配置、控制項的種類、標籤上的文字或樣式。
    原因是本章開頭的判準。
    本項的名稱用「contract」而不是「presentation」，就是為了把這些項目排除在外。
  - 專案的 Dataflow 可能有名為「presentation」的 stage 或活動。
    **本項和那個 stage 不是同一件事。**
    那個 stage 是一個會執行的活動。
    本項是 system 必須遵守的一組限制。
    替兩者取名時，不要用同一個詞。
- **Interfaces**：每一個由外部 system 呼叫的 component（例如 AI agent、skill 或其他程式）。
  每個 component 都要寫出它的名稱，以及它的 API 或 CLI：
  - 怎麼呼叫它：endpoint 與它的參數，或完整的指令與它的所有參數。
  - 一次呼叫執行 Dataflow 的哪些 stage。
  - 它讀寫的資料。
  - 它回傳的資料：回應，或輸出與 exit status。
  - 它不接受的呼叫。

  component 的名稱與它的介面，是和每一個 caller 之間的契約。
  重構若改了名稱或介面，每個 caller 都會無法正常運作，而且不會出現任何錯誤。
  所以由本章定下它們，而不是 Design。
  component 的內部（它的模組，以及它如何完成工作）屬於第 3 章。

  外部 system 只透過這個介面接觸 component。
  它呼叫 API，或執行 CLI。
  它不 import component 的模組，也不呼叫這些模組中的程式碼。
  第 3 章可以改動 component 的內部，同時保持介面不變。
  這時，用到這些內部的 caller 就會無法正常運作，而且不會出現任何錯誤。
  RSDC 可以依介面的類型替這一項命名，例如 CLI 或 HTTP API。
- **Invariants**：適用於所有 component、也適用於其中每一個的限制。
  Invariants 與前述各項的差別在於**適用範圍**。
  前述每一項各自規範一類對象。
  Invariants 規範全部。

  一條規則若必須在三處以上遵守，就把它放在這裡。
  不要在每一處各寫一份。
  一條規則的各份副本會各自改變，最後彼此不一致。
  - **目標表**：在 Invariants 的結尾放一張表。
    這張表依名稱，把第 1 章的每一個目標，連到守住它的各節與各條規則。
    每個目標寫一列。
    只有寫下來的表，才看得出哪個目標沒有任何規則守住。
    沒有這張表，要到使用時才會看出 system 沒有得到某個目標的結果。
    到那時，已經沒有人知道該由哪一條規則守住那個目標。

# 3. Design — "How is the system structured?"

本章寫出 system 的結構與 component。
它也說明 system 用哪些方法來遵守它之前的 Specification。

- **Core Component Responsibilities**：第 2 章指認的 component，各自拆成它的模組。
  另外也列出外部 system 不會呼叫的 component（例如 ArtifactManager、File Table、Runtime），以及所有 component 如何協同運作。
  每個 component 只負責**一種工作**，並且有一條 **boundary**。
  boundary 說明一次跨越它的修改，可能讓哪些項目出錯。

  跨越 boundary 的一次修改，就是對兩個 component 的修改。
  一個 component 若做兩種工作，這兩種工作之間的 boundary 就在這個 component 裡面。
  在那裡，沒有人看得出改了其中一種工作，可能讓另一種出錯。
- **Execution Flow**：每個 component 在執行時如何完成它的工作。
  例如 system 如何讀取它的配置，以及如何在執行時產生它的任務網絡（例如 dodo.py 給出的任務）。
  以及 system 在執行時的其餘邏輯。
  需要畫圖時，用 [DFD.md](DFD.md) 記法的 DFD。
  這張 DFD 和 Dataflow 有兩點不同：
  - 它的 process 是 component 的 step。
    step 用程式碼裡的名稱。
  - 它可以畫出 Dataflow 不畫的東西。
    這些東西是 stage 的內部、分支、重試與平行處理。
    也包括由程式碼選擇、而不是由資料造成的順序。

  每一條規則都引用第 2 章。
  不要把規則再寫一次。
  關於 stage 內部的規則也一樣。
- **Directory Structure**：專案檔案的存放位置，以及它們的分層邏輯（例如 lambdas/、flows/、agents/、warehouse/）。
- **Presentation Form**：對 Specification 中的每一件「使用者必須能夠……」，本項說明由**哪個 component** 提供。
  它也說明人用來做這件事的**控制項種類**，以及有幾個控制項。
  API 或 CLI 在本章之前，已由第 2 章的 Interfaces 寫出。
  Specification 說「必須能發起」。
  Design 說「由誰發起、經由幾個入口」。
  - **必須列出對照表**：這張表有三欄：
    1. Specification 所要求的 capability。
    2. 執行它的 component。
    3. 使用者所認得的名稱。

    這張表是 **coverage proof**。
    它不是介面規格。
    它由第 2 章的規則長出來。
    所以它的列數不會比規則多。
  - **orphan 即缺陷**：orphan 是找不到對應規則的一列。
    那一列的 capability，從來沒有人同意過。
    當場補上規則，或移除這個 capability。
    反向檢查**只適用於 granting rule**。
    granting rule 寫出使用者必須能夠進行的操作。

    granting rule 若找不到對應的列，這條規則就沒有入口。
    **constraining rule** 規定 system 不得呈現的資料，或不得取得存取權的使用者。
    constraining rule 因為它的種類而沒有入口。
    所以表中不列出它是正確的，這不是缺陷。
    若把這兩種規則當成同一種，這張表在啟用的第一天，就會列出錯誤的 orphan。
  - **並非每個控制項都是 capability**：有些控制項只改變畫面顯示多少，或怎麼顯示（例如「全部展開」與「全部收合」）。
    如果拿掉這樣的控制項，所有驗證仍然通過，它就不是 Specification 所給的 capability。
    **表中不列出它是正確的。**
    這就是第 2 章開頭的判準。
    只有能讓通過的驗證不再通過的改動，才是規則。
    若不寫明這一點，後來的讀者會把這類控制項當成 orphan 去「修正」。
  - **僅止於名稱**：使用者所見的名稱，只能出現在表中對應的那一欄。
    不要用它來說明 system 如何運作，也不要用它寫出版面配置、位置或樣式。
    這些項目仍屬於 Coding。
- **Specification 詞彙與 component 詞彙必須接得起來**：Specification 使用活動與資料的名稱。
  在 Interfaces 中，它也使用外部 system 呼叫的 component 的名稱。
  Design 寫出所有 component 的名稱。
  兩套詞彙說的是同一個 system。
  Design 必須明白寫出兩者之間的對應（哪個 component 執行哪個活動）。

  若沒有寫出，讀者就無從得知這個對應。
  兩章看起來就會像在說兩個不同的 system。
  Dataflow 的每一個 stage，都必須有執行它的 component。
  外部 system 呼叫的 component 寫在第 2 章的 Interfaces，其餘的寫在本章。
  沒有 component 的 stage，表示沒有人為那個活動寫出程式碼。

# 4. Coding — "How should the code be written?"

本章提供程式碼的開發準則與最佳做法。
它們讓程式碼保持高品質，並能在不同平台上運作。

- **Key Development Guidelines**：
  - **Config-driven**：在執行時由配置檔產生邏輯。
  - **Path injection**：不要把路徑寫進程式碼中。
    每一個路徑都在執行時注入程式碼。
  - **AI-First**：每個描述欄位都要為 AI 而寫。
    AI 必須能從欄位取得所需的資訊，並據以分派工作。
  - **輸入值沒有預設值**：從輸入讀取每一個值時，都不帶預設值。
    輸入若沒有某個值，規則拿到的就是一個缺少的值，而不是一個數字。
    預設值是寫在程式碼裡、看似正確的近似值。
    Derivation Rules 不允許使用這樣的值。
    而且預設值被用上時，不會告訴你。
- **Implementation Guidelines and Tools**：必須使用的程式庫（例如 pathlib、arrow），以及程式風格（例如 type hint）。
- **Safety and Robustness**：同時執行的任務所用的檔案鎖定機制，以及檢查 I/O 契約的邏輯。
- **Platform Traps**：曾經**實際造成**看似正確卻是錯的結果、又沒有出現錯誤的情況。
  只記錄真的發生過的情況。
  不要記錄可能發生的情況。
  可能發生的情況沒有止境，真正發生過的情況會在其中變得難以找到。
- **Verification Obligations**：一份逐項的清單。
  每一項都寫出「宣稱其可運作」與「如何證明它可運作」。
  component 只有在人或測試**證明**它如何運作之後，才算合格。
  只是認為它能正確運作，並不算合格。
  - 清單包含第 2 章的每一條規則。
    如果你無法驗證某條規則，那條規則的效力就和一條沒有人寫下的規則一樣。
  - 清單裡，第 3 章的每一個 component 至少出現一次。
    沒有任何一列為它提供證明的 component，就無法證明它能正確運作。
  - 目前還沒有證明的項目，也要留在清單中。
    把它標為 **「not verified」**，並寫出到目前為止為它找到的資訊。
  - 在本項的最後，說明每一個「not verified」的項目可以如何改成自動化的證明。

  不在清單上的項目，之後的每個讀者都會以為它已有證明。
  標著「not verified」的項目，每個讀者都看得出它還沒有證明，也能補上證明。
- **Defects**：程式碼不遵守第 2 章某條規則的每一處。
  每個缺陷都寫出你在哪裡看到它，以及它的代價。
  規則仍然留在第 2 章。
  本項只記錄程式碼在哪裡沒有遵守它們。

  這樣可以避免為了把缺陷寫成規則而改動 Specification。
  本項記下的缺陷，後來的讀者能夠結案。
  本項沒記下的缺陷，後來的讀者只能重新找出來。

# Versioning

RSDC-Standard.md 的檔名不含日期。
只有規則的改動才會產生新版本。
改動 RSDC-Standard.md 的規則時，只做下列事項：

1. 更新 RSDC-Standard.md 開頭 Version 行的版本。
2. 在文末「Changes in This Version」的最上方，為新版本加一個小節。
3. 不要改檔名。

這樣，引用 RSDC-Standard.md 的文件就不必跟著改。

只改動 RSDC-Standard.md 的文字或版面時，不要更改版本。
在該版本的小節中說明這次改動。

# Changes in This Version

## 261016

第 2 章的 Terms 改名為 Terminology。
SKILL.md 在 TERMINOLOGY 一節寫出 skill 的名詞，所以兩種文件現在用同一個名稱稱呼它們的名詞。
以名稱找這一項的工具也一起改了：`gen-rsdc-skill` 的 `check_rsdc.py`，以及 `chinese` skill。
這一項的規則沒有改變。

## 261010

我們以 STE 重新寫了 RSDC-Standard.md 的文字。
給 RSDC 的規則都沒有改變，所以版本也沒有改變。
我們只改了本標準自己的版本規則：現在只有給 RSDC 的規則改了，才會產生新版本。

2026-10-13，我們審核了三次之後，DFD.md 的 STE 文字取代了它原本的文字。
DFD.md 現在不再提 RSDC、README 或版本。
它的資料種類現在在 Types of Data 這一節，範例也改用 Catalog 這個名稱。

2026-10-12，我們從 RSDC-Standard.md 與 DFD.md 拿掉了關於繁體中文 twin 的那一行。
規則沒有改變，所以版本也沒有改變。

我們為 skill 的 system 寫了一份 template。
這份 template 顯示出一些每一份 RSDC 都必須有、標準卻沒有寫出的規則。
app 的 template 與 skill system 的 template，各自獨立寫下了其中一些規則。
我們就是這樣找到這些規則的。

接著，我們讓 skill system 的 template 與標準一致。
在這項工作中，我們發現標準有兩條規則必須改。
一條讓 Design 混進了 Specification。
另一條讓 Dataflow 把它的圖已經畫出的資訊再說一次。
我們也把標準的檔名，改成引用它的文件所用的名稱。
本版中，Dataflow 的圖改用它所屬的圖種名稱。

- **目標表。**
  「System Goals 的每一條目標，都必須在第 2 章找到對應的規則」這條規則，沒有說這個對應要寫在哪裡。
  沒有人寫下來的對應，無從檢查。
  兩份 template 都在 Invariants 的結尾放了一張表，每個目標一列。
  每一列寫出守住該目標的規則。
  本版中，這張表是 Invariants 的一部分，第 1 章也指向它。
- **代碼標籤與精度。**
  Naming and Data Structures 這一項規範了名稱。
  它沒有規範程式寫出、讀者比對的值。
  代碼標籤可能有兩種寫法，數字也可能有兩種進位方式。
  這時寫入者與讀者的認知就不一致，而且不會出現任何錯誤。

  本版中，每個存放代碼標籤的欄位都列出它的代碼標籤。
  每個數字都寫明精度。
  名稱是「代碼標籤」，不是「標籤」。
  原因是 Presentation Contract 中的「標籤文字」指的是控制項上的文字，那是另一回事。
- **Dataflow 的名稱，由它之前的項說明。**
  Dataflow 提供了 stage 與 record 的名稱。
  但沒有任何規則說明它的其他名稱從哪裡來。
  skill system 的 Dataflow，在任何一節說明「request」之前就用了它。
  本版中，圖所用的每一個名稱，都由 Terms 或 Artifact Types 在 Dataflow 之前說明。
- **Terms 排在最前面。**
  RSDC 所用的名詞中，有些不是資料的名稱（例如 caller，或一次執行寫入的目錄）。
  這些名詞原本沒有自己的一項。
  兩份 template 都把它們放在 Artifact Types 的最後，和資料的種類放在一起。

  本版中，它們有了自己的一項，就是第 2 章的第一項。
  於是之後的每一項（包括 Artifact Types），都在這一項說明它們之後才使用它們。
  term 不是資料的名稱，因為本章在 term 之後才寫出資料。
- **Execution Flow 排在 component 之後。**
  Directory Structure 原本夾在 Core Component Responsibilities 與 Execution Flow 之間。
  但 Execution Flow 逐一處理的，正是同一批 component。
  skill system 沒有 Directory Structure。
  所以它的 Execution Flow 編號比 app 的少一號。

  本版中，Execution Flow 緊接在 component 之後，Directory Structure 排在 Execution Flow 之後。
  於是兩種 system 都有的節，在兩種 system 中編號相同。
- **我們拿掉了 Task Generation Logic。**
  在這一項中，RSDC 寫出工具（例如 dodo.py）如何從邏輯產生可執行的任務。
  只有由任務工具控制的 system，才有這樣的工具。
  而且 Execution Flow 也要求寫出 system 產生的任務網絡。

  沒有任何一份 RSDC 有這一項。
  skill system 的 template 還得說明自己沒有這一項的原因。
  本版中，有任務工具的 system，在 Execution Flow 寫出它的任務。
  工具本身則寫在 Implementation Guidelines and Tools。
- **一條線是執行時的移動。**
  我們畫了一個 skill 的 Dataflow。
  這時我們不知道，一份文件引用另一份文件時，要不要畫成一條線。
  本版中，DFD.md 寫明圖上不畫它。
  一條線是流程執行時移動的資料。
- **沒有證明的項目留在表中。**
  Verification Obligations 要求寫下有人看到的運作。
  它沒有說到當時還沒有人看到的項目。
  表中若沒有列出這些項目，讀者就會以為它們已有證明。
  本版中，這些項目留在表中，並標為「not verified」。
  表中也為每一項說明如何把它的證明自動化。
- **輸入值沒有預設值。**
  Derivation Rules 不允許使用看似正確的近似值。
  寫在程式碼裡的預設值就是這樣的值，而且被用上時不會告訴你。
  本版中，Key Development Guidelines 不允許使用預設值。
- **介面是唯一入口。**
  Interfaces 定下了 caller 呼叫的 API 或 CLI。
  它沒有說 caller 不得呼叫其他部分。
  AI agent 或 skill 若 import 某個 component 的模組，這個 component 內部的改動就可能讓它出錯。
  本版中，外部 system 只透過 API 或 CLI 接觸 component。
- **stage 的內部在 Design 中畫出。**
  261008 版在 stage 的內部是規則時，把它留在 Dataflow 中。
  原因是 skill 只能引用第 1、2 章。
  但圖會畫出 stage 的所有部分。
  這些部分大多是 component 完成工作的方式，不是規則。
  而且 stage 內部的順序，常常只是遵守某條規則的一種做法，而不是規則本身。

  例如「verdict 在重建 trailing stop 之前就已定案」。
  這個順序遵守「沒有任何 verdict 讀取 trailing stop」這條規則，但圖並沒有畫出這條規則。
  本版中，第 2 章以文字寫出這條規則，skill 可以在那裡引用它。
  畫出 stage 內部的圖，放在 Execution Flow 中。
- **誰讀寫資料，只由圖說一次。**
  Stage Read/Write Table 與 Data Read/Write Rules 的表格，把 DFD 已經畫出的資訊再列一次。
  它們列出每個 stage 讀寫的資料。
  也列出每一項資料由誰寫入與讀取，以及它屬於哪一種。
  第二份副本會變得和圖不一樣，而且沒有人會發現這個差異。

  沒有任何 skill 引用這兩張表。
  skill 引用的，是圖畫不出來的資訊。
  我們刪除了這兩張表，本版中只有 DFD 寫出這些資訊。
  Data Read/Write Rules 只保留圖畫不出來的資訊。
  Order Imposed by the Data 與 Exception Paths 這兩項沒有改變。
- **檔名改了。**
  `RSDC-Responsibilities.md` 的新名稱是 `RSDC-Standard.md`。
  它的 twin `RSDC-Responsibilities-tw.md` 的新名稱是 `RSDC-Standard-tw.md`。
  在這次改動之前，引用 RSDC-Standard.md 的文件就已經稱它為 RSDC standard。
  舊名稱只說出內容的一部分（四章各自必須做的工作）。
  而且每一份引用它的文件，都得再寫一次那個長名稱。

  沒有任何規則改變。
  這次改動是唯一不遵守上面「檔名不變」那條規則的改動。
  所有仍在使用、引用這個檔案的文件，都隨檔案一起改了。
  舊名稱只留在先前版本的文字中，例如下面的 261008。
- **這張圖的名稱是 DFD。**
  Dataflow 第一部分的名稱原本是 Flowchart，名稱來自畫它的 mermaid 語法。
  但 flowchart 畫的是 system 下一步做什麼。
  這張圖畫的則是資料往哪裡去。

  有些 RSDC 談的就是 flowchart，例如 mermaid 檢視器的 RSDC。
  在這樣的 RSDC 中，讀者分不出這個名稱指的是哪一張圖。
  本版中，這一部分的名稱是 DFD，與 DFD.md 所用的名稱相同。
- **由各 step 依序修改的 record，沒有第二個寫入者。**
  DFD.md 原本把每一份有不止一個寫入者的 record 都算成缺陷。
  所以它也把「檢查並修正」的循環標成缺陷。
  例如一個 skill 的各 step 寫出一份文件、審查它，再檢查並修正它。
  這些 step 都寫入同一份文件。

  這個缺陷是一種風險：一個 process 重跑時，抹掉了另一個 process 的結果。
  但只要後面的每個寫入者都先讀取它要改的資料，這件事就不會發生。
  本版中，DFD.md 寫明這種情況不是缺陷。
  這種情況的名稱是「依序編輯的 record」。
  圖以雙向箭頭畫出它。

  這種情況有一個代價。
  第一個寫入者重跑時，後面所有的 step 都必須重跑。
  流程必須說明如何控制這件事。

  排在第一個寫入者之前的 step，可以讀取這種 record。
  那個 step 讀到的，是 record 當時的原樣。
  所以那個 step 並沒有讀取後面的 step 所寫的資料。

## 261009

AI agent 或 skill 透過 API 與 CLI 呼叫 system 的 component。
所以 component 的名稱與它的介面都是契約。
標準原本不允許 Specification 寫出 component 的名稱。
所以這些契約在標準中無處可放。
但有兩份文件把它們放進了第 2 章：skill system 的 RSDC 規則，以及 app 的 template。

- **第 2 章寫出外部 system 呼叫的 component 的名稱。**
  它的新主題 Interfaces，定下每個這類 component 的 API 或 CLI。
  這些若留在 Design，重構時就可能改掉某個名稱或參數。
  這時每個 caller 都會無法正常運作，而且不會出現任何錯誤。
  本版中，One-way Dependency 那條規則改為說明 Specification 不得寫出的項目：component 的內部。
- **第 3 章把 component 拆成各個部分。**
  Core Component Responsibilities 這一項把第 2 章的 component 拆成它們的模組。
  它也列出外部 system 不會呼叫的 component。
  Presentation Form 這一項只保留給人用的控制項，因為 API 或 CLI 由第 2 章寫出。
  要找某個 stage 的 component 時，若它由外部 system 呼叫，就到 Interfaces 中找。
- **Defects 有了位置，驗證涵蓋所有 component。**
  第 4 章新增了一項：Defects。
  它寫出程式碼沒有遵守第 2 章的每一處，以及你在哪裡看到它、它的代價。
  這樣就沒有人會把缺陷當成規則，寫進 Specification。
  在本版之前，skill system 的 RSDC 規則與 app 的 template 就已經有這樣的清單。

  本版中，Verification Obligations 要求列入第 3 章的每一個 component，至少一次。
  它也要求列入第 2 章的每一條規則。
  清單若只列規則，可能會留下一個沒有證明的 component。
- **每個 component 只負責一種工作，並有一條 boundary。**
  Core Component Responsibilities 這一項原本只要求寫出每個 component 的範圍，以及各 component 如何協同運作。
  於是一個 component 可能做兩種工作，卻沒有人看見。

  本版中，它要求每個 component 只負責一種工作。
  它也要求為每個 component 寫出它的 boundary，以及一次跨越它的修改可能讓哪些項目出錯。
  在本版之前，app 的 template 就已經這樣做。
  這樣你就看得出，同時改到兩種工作的修改，就是對兩個 component 的修改。

## 261008

我們用英文把標準重寫一次，再逐行讀過。
我們發現有些措辭會讓讀者把一條規則當成另一條。
也發現有一條規則，它的字面所涵蓋的比它的理由少。

- **同一份標準，以英文與繁體中文寫成。**
  本版中，標準以英文撰寫，它的繁體中文 twin 是 `RSDC-Responsibilities-tw.md`。
  twin 的標題、主題名稱與 Dataflow 的 term 保留英文。
  這樣兩份檔案就與每一份 RSDC 及其 twin 用同一套詞。
  原本的中文版把這些詞寫成了中文。
  所以讀者在每次檢查之前，都得先把「階段」對回 stage。
- **標準寫明哪個部分是章、哪個部分是節。**
  「章節」這個詞同時指這兩種部分。
  所以讀者可能把關於其中一個的規則，讀成關於另一個的規則。
  本版中，章是四個固定不變的部分（Requirements、Specification、Design、Coding）之一，編號 1 到 4。
  節是章的一部分，編號為 N.M。
- **我們把兩條 One-way 規則區分開來。**
  章的那條規則，標題用了「引用」一詞。
  所以它讀起來像是章層級的 No Forward Reference。
  但它的子規則說的是：一章不得寫出後面某一章的內容。

  本版中，標題是「前章不得提及後章的內容」。
  Specification 寫出一個 component 的名稱，就不遵守這條規則，但它並沒有引用其他部分。
  2.3 中的「見 2.5」不遵守 No Forward Reference，但它沒有離開自己的章。
- **No Forward Reference 涵蓋章。**
  這條規則原本只寫了「節」。
  所以「見第 3 章」這段文字，照字面並沒有違反這條規則。
  但讀者不看另一節，就讀不懂那一節。
- **Specification 的界線寫在第 2 章。**
  「可以規定『什麼』，不得規定『長什麼樣子』」這條規則，原本和適用於所有章的規則放在一起。
  但它只適用於第 2 章。

  本版中，它放在第 2 章的開頭，就像第 1 章的界線放在第 1 章的開頭。
  Presentation Contract 與第 3 章引用的是那裡的這條規則。
  它們不再重寫一次。
- **「每條規則都要寫出違反它會怎樣」的措辭變清楚了。**
  「符合的例子」與「具名的失敗」這兩個說法並不清楚。
  讀者得先取得更多說明，才用得上它們。
  本版中，用一個例子從規則一路講到它所給出的測試。
- **由另一份文件說明這種圖。**
  第 2 章的 Dataflow、第 3 章的 Execution Flow，以及 skill 的 Dataflow，都用同一種圖。
  所以本版中，[DFD.md](DFD.md) 寫出每一張這類圖的資料種類、形狀與線型。
  它也寫出要檢查的兩種缺陷。
  DFD.md 是本標準的一部分，版本與本標準相同。

  Dataflow 的必備內容仍寫在第 2 章。
  Execution Flow 可以多畫哪些項目，由第 3 章說明。
  我們沒有用其中一個使用者的名稱來替這份文件命名。
  若用了這樣的名稱，另一個使用者就得引用一份它並不是的 Dataflow。

  本版中，有一條規則變寬了。
  由 system 外部 role 提供的資料，也有來源。
  所以本版中，caller 送來的 request，不算是沒有任何 process 產生的資料。
  這份文件附有一個 mermaid 例子。
  例子的圖例逐一點名例子裡的各個部分。
- **Hierarchy 這一項寫明何時適用、到哪裡為止。**
  有讀者把 Hierarchy 和 Dataflow 一起讀。
  於是 Hierarchy 看起來就像是 Dataflow 所包含的一部分。
  但其實不是。
  Hierarchy 說明使用者用哪些單位組合出 system，以及哪個單位包含哪個單位。
  Dataflow 說明資料如何在 system 的活動之間移動。

  Lambda 不是 stage。
  它是執行這個 Lambda 的 stage 所讀取的資料。
  一條規則，例如「Flow 只包含 Lambda」，在 Dataflow 的各個部分中無處可放。
  但這次檢查看出，這一項來自單一範例。
  skill 的 RSDC 與 app 的 template 都沒有它。

  所以本版中，這一項寫明：只有當使用者以分層的單位組合 system 時，才寫它。
  它也寫明架構中的分層屬於 Design。
  Hierarchy 與 Dataflow 之間的分界，寫在 Dataflow 中。

  Config Schemas 這一項原本寫的是「各層級的 config.yaml」。
  本版中，Config Schemas 不再預設 system 有層級。
  它涵蓋 system 讀取的每一份配置檔。
  只有在有 Hierarchy 時，才每個層級各一份 schema。
- **Artifact Types and Flow 的新名稱是 Artifact Types。**
  這一項與 Dataflow 的界線，把資料的種類分給了這一項。
  把「資料往哪裡走」分給了 Dataflow。
  但這一項的名稱卻包含了 Flow。
  每一種資料由誰寫入、誰讀取，由 Dataflow 的 Data Read/Write Rules 說明。

  所以這一項保留每一種資料的資訊、用途與內容上的限制。
  它也改用 skill 的 RSDC 所用的名稱。
  我們在本版之前寫的一些 RSDC，有一節名為 Artifact Types and Flow。
  下次讓這些 RSDC 與標準對齊時，把那一節改名。
- **只有內部本身是規則時，Dataflow 才畫出 stage 的內部。**
  「必要時」這幾個字讓讀者自行選擇。
  於是 component 的做法可能混進 Specification。
  本版中，第 2 章只在一種情況下畫出 stage 的內部。
  stage 內部的順序，或在它各部分之間移動的資料，必須是某個驗證所依賴的。

  其餘的內部都歸 Execution Flow。
  這些情況仍留在第 2 章，因為 skill 只能引用 RSDC 的第 1、2 章。
  而且 skill 目前也引用了畫出內部的 stage。
- **第三種資料有了名稱：one-run data。**
  「data of one run」這幾個字把 term 拆開了。
  繁體中文版更把它拆成英文與中文兩種詞。
  本版中，它和 record、external input 一樣是一個名詞。
  Kind 欄位以同樣的字填入它。
- **三種資料不再重疊，「input from outside」的新名稱是 external input。**
  caller 送來的 request 來自 system 外部的來源，也沒有任何 process 寫入它。
  所以它既是「input from outside」，也是 one-run data。
  本版中，每一種資料各有自己的界線：
  - record 由 process 寫入，並由 system 保留。
  - external input 來自 system 外部的來源，在每次執行結束後仍然存在。
  - one-run data 只存在於一次執行之中，不論來源為何。

  新名稱和另外兩個名稱一樣是一個名詞。
- **one-run data 有了不同的形狀。**
  one-run data 與 external input 原本形狀相同，都是平行四邊形。
  所以圖上畫不出兩種資料的差別。
  一種保存在 system 之外，另一種只存在於一次執行之中。
  本版中，每一種資料都有不同的形狀。
  在 mermaid 中，one-run data 的形狀是旗形。
- **DFD 裡的工作單位叫 process。**
  「step」這個詞是 skill 的 Workflow 中 step 的名稱。
  skill 的 Dataflow 畫的正是這些 step。
  所以一般用語改用 DFD 自己的詞「process」。
  DFD 中的 process 不是作業系統的行程。

  每一種流程都用自己的名稱稱呼它的 process。
  在 RSDC 的 Dataflow 中，它們叫 stage。
  在 Execution Flow 與 skill 的 Dataflow 中，它們叫 step。

我們把較寬的 No Forward Reference 規則，套用到先前寫好的 RSDC 上。
結果找到一處錯誤。
某個 template 在它的 1.4 節引用了第 2 章。
每一份由那個 template 寫出的 RSDC，也都在它的 1.4 節引用了第 2 章。
不是由那個 template 寫出的 RSDC 都沒有。
本版中，該 template 改為在 2.9 往回引用 1.4。
