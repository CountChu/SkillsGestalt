# Skill Compiler - Compile SOP

這些判斷把一份 Skill Source 編譯成 Compiled Script：為它的 step 分類、寫出 script、修正它，以及判斷它的執行產出了什麼。
每個 step 都以它的輸入開頭，拿到那份輸入才開始。

## Terms and Rules

- **Skill Source** —— skill 的 `SKILL.md`，直接位於 skill 自己的目錄中，該目錄的上層目錄名為 `skills`：`skills/<name>/SKILL.md`。
- **Compiled Script** —— `skill.py`，與它的 Skill Source 在同一個目錄中：一支無頭的 Python 程式，一次執行一個 Step Action，或描述全部的 Step Action。
- **Step Action** —— Skill Source 的 `Workflow` 區段底下，以 `Step 0`、`Step 1` 或 `Step 2` 等標題宣告的 step。
- **Caller** —— 執行 Compiled Script 的一方：在終端機前的人、背後有人操作的使用者介面、scheduler，或 agent。
- **Person compiling** —— 要求編譯某個 skill、並決定編譯留給人決定之事的一方。
- **Person revising the skill** —— 以人手撰寫與修改 Skill Source 的一方。
- **Input variable** —— Step Action 在一次執行中向 caller 取得的值，宣告時帶有名稱、是否 required、提示說明與 data type。
- **Handoff** —— Cognitive step 不被執行、而以之結束的結局：控制權還給使用者或 agent，由他們透過 skill 本身執行該 step。
- **Introspection** —— Compiled Script 描述它的 Step Action、每一個的 Action type，以及每一個接受的 input variable，而不執行其中任何一個。
- **Core work** —— 處理 skill 自己資料的工作，必須早已是 skill 所執行的程式。
- **Chore** —— 由共用規則或該 step 自己的文字完整規定的雜務，例如讀取設定、解析 request 或寫入 checkpoint。
- **Stale** —— 指一份 Compiled Script 所記錄的指紋缺失，或與它旁邊 Skill Source 的指紋不同。

每一個 step 都遵守的規則：

- 只編譯 workflow 已經穩定的 skill；仍在修改中的 skill，以 skill 的方式執行。
- 絕不改變 Skill Source。
- 整份寫出 Compiled Script，不寫 skill 的任何其他檔案。
- 絕不手動修改 Compiled Script：變更經由 Skill Source 進入，只有從 Step 1 重新編譯，才會到達 script。
- Compiled Script 記錄的指紋，就是交給 Step 2 的那一個；絕不寫入其他指紋。
- script 為 stale、Step 4 發現來源有缺口，或 script 的結果與預期偏離太多時，由 person revising the skill 修改 skill，並以 skill 的方式執行直到穩定；之後從 Step 1 重新編譯，並整份寫出 script。
- Compiled Script 絕不呼叫 LLM，也絕不等待人。
- 沒有通過每一項 contract 檢查與 Step 4 的 Compiled Script 尚未完成，任何東西都不依賴它。
- 說要停止的 step，就結束這次編譯。

## Step 1 - Classify the Step Actions

**輸入**：Skill Source；它的 **step inventory**——每個 Step Action 的 identifier、標題與行範圍，以及它的 inline code 或 fenced block 中出現的每一個程式檔名，不論該 step 是執行它還是只提及它，每一個都標明是否在 skill 的目錄中；以及重新編譯時，既有 Compiled Script 的 docstring。

- 讀完整份 Skill Source。
- 給每個 Step Action 它的 identifier：其 `Step N` 標題去掉前導零的編號。

給每個 Step Action 恰好一種 Action type，由 Cognitive dimension 與 Execution dimension 交叉而成：

| Cognitive \ Execution | Automated | Interactive |
| :---- | :---- | :---- |
| **Deterministic** | `deterministic_automated`：本機邏輯，不花 token，一個動作就完成 | `deterministic_interactive`：本機邏輯，不花 token，人給出它的值之後完成 |
| **Cognitive** | `cognitive_automated`：需要 LLM；script 以 handoff 交出它 | `cognitive_interactive`：需要 LLM 與人一起工作；script 以 handoff 交出它 |

- 依 step 的結果需要什麼判斷 Cognitive dimension，不看它的指示讀起來如何。
  讀取、解析、計算、呈現，或呼叫程式能呼叫的服務，都是 Deterministic。
  透過只有 agent 能用的介面所做的呼叫，若同樣的呼叫不用 LLM 也做得到——透過服務自己的介面、既有的輔助程式或函式庫——就是 Deterministic；只有在沒有這種途徑時，才是 Cognitive。
  需要 LLM 的語意判斷是 Cognitive。
- 依 step 的輸入判斷 Execution dimension。
  向人取得值的 step——不論那個值是隨 request 給出，還是向人詢問——是 Interactive；所需要的一切都能自己讀到的 step，是 Automated。
- 把 step 向人取得的每一個值，都設為它的一個 input variable，帶有它所接受之值的種類，並在 Skill Source 沒有給它預設值時設為 required。
  Deterministic Automated step 不要求任何 input variable，Deterministic Interactive step 至少宣告一個。
- 指示混合了多種 Action type 的 step，依來源順序拆成 `N.1`、`N.2`、…，每一個恰好一種 type，之後就不再以整體指定它；其他每個 step 都保留 `N`。
- 對每個 Deterministic step，從 step inventory 取出它所執行的程式，略去它只是提及的檔名；把該 step 編譯成呼叫同樣這些程式，絕不重寫其中任何一支。
- 絕不以 deterministic 邏輯近似 Cognitive step。
- 對每個有一部分工作沒有執行任何程式的 Deterministic step，逐一 step 詢問 person compiling，那部分工作是 core work 還是 chore。
  重新編譯時，把 docstring 所記錄的決定作為預設選項提出。
  絕不自行決定，問題沒有得到回答時就停止。
- 有工作被判定為沒有程式支撐的 core work 時，停止，什麼都不寫，並列出那些 step 及各自需要程式做什麼，交給 person revising the skill 寫成 skill 所執行的程式。
- 在寫任何程式碼之前，先呈現分類：每個 Step Action 的 identifier、標題、Action type、input variable、它呼叫的程式或人的決定，以及決定其 type 的依據。

## Step 2 - Write the Compiled Script

**輸入**：Step 1 的分類與人的決定，以及被分類之 Skill Source 內容的指紋。

在 Skill Source 旁邊整份寫出 `skill.py`。

**它記錄什麼**

- `SOURCE_SHA256` —— 一個 module 層級的常數，以單純的字串常值賦值：作為輸入交給它的指紋，64 個小寫十六進位數字。
- `COMPILED_AT` —— 一個 module 層級的常數，以單純的字串常值賦值：這次編譯的 ISO 8601 日期時間，含 UTC 位移。
- module docstring —— Skill Source 的 `description`，接著是每個 Step Action 及其 identifier 與 type、執行其中一個的指令，並對每個工作沒有執行程式的 Deterministic step，記錄人判定它為 chore。

**它如何被執行**

- `python skill.py --step <id> [--<name> <value> ...]` 執行 identifier 為 `<id>` 的那一個 Step Action，它的每個 input variable 都以一個以該 variable 命名的選項傳入。
- `python skill.py --export-schema` 印出 introspection metadata，不執行任何 step。

**每一次呼叫依序做的事**

1. 在每一次呼叫中（包括 `--export-schema`），計算 script 自己目錄中 `SKILL.md` 的指紋——它的文字以 UTF-8 解碼、移除任何 byte-order mark、把每個換行統一為 LF，再以 UTF-8 編碼後的 SHA-256 小寫十六進位摘要——並與 `SOURCE_SHA256` 比對。
   兩者不一致、或 `SKILL.md` 不存在時，在標準錯誤輸出寫明 script 已 stale、必須重新編譯，標準輸出什麼都不印，並以 `4` 退出。
2. 以 `click` 讀取命令列：缺少 required 選項，或值被它的 parameter type 拒絕，都在做任何工作之前以 `2` 退出。
3. 有 `--export-schema` 時，在標準輸出印出 introspection metadata，只有一份 JSON 文件，此外什麼都沒有，再以 `0` 退出。
4. 有 `--step <id>` 時，執行該 step 的 Action Logic Builder；不對應任何 step 的 identifier 以 `2` 退出。
   Cognitive step 的 builder 印出 handoff 訊息，並以 `3` 退出；Deterministic step 的 builder 做該 step 的工作，並以 `0` 退出。

**它如何結束**

- Exit status：`0` 成功；`2` refusal，在做任何工作之前，並指名哪裡不對——缺少 required 輸入、值的種類錯誤，或 identifier 不對應任何 step；`3` handoff，在 handoff 訊息之後；`4` stale，標準輸出什麼都沒有。
- handoff 訊息：`This step is a cognitive task and cannot be processed by this system. Please have the user or Agent invoke the corresponding Skill separately.`

**introspection metadata**

一份 JSON 文件，採用以下形式：

```json
{
  "skill_name": "example_skill",
  "steps": [
    {
      "id": "1.1",
      "name": "Fetch raw data",
      "type": "deterministic_automated",
      "description": "Run a local Python web crawler to fetch data",
      "arguments": []
    },
    {
      "id": "1.2",
      "name": "Analyze article sentiment",
      "type": "cognitive_automated",
      "description": "Call an LLM to classify text sentiment; this system only provides a handoff prompt",
      "arguments": []
    },
    {
      "id": "1.3",
      "name": "Set export path",
      "type": "deterministic_interactive",
      "description": "Requires the user to specify a local backup directory",
      "arguments": [
        {
          "name": "output_path",
          "required": true,
          "type": "path",
          "description": "Target path for export"
        }
      ]
    },
    {
      "id": "2.0",
      "name": "Human creative review",
      "type": "cognitive_interactive",
      "description": "A human and AI jointly review revision suggestions; this system only provides a handoff prompt",
      "arguments": []
    }
  ]
}
```

它的欄位：

| Field | Meaning |
|---|---|
| `skill_name` | `SKILL.md` frontmatter 中的 `name`，frontmatter 沒有時則為 skill 的目錄名稱 |
| `steps` | Skill Source 的每一個 Step Action，依來源順序，不多也不少：也就是 `--step` 所接受的 identifier |
| `steps[].id` | step identifier |
| `steps[].name` | step 的人類可讀名稱 |
| `steps[].type` | Action type：`deterministic_automated`、`cognitive_automated`、`deterministic_interactive` 或 `cognitive_interactive` |
| `steps[].description` | step 的人類可讀說明 |
| `steps[].arguments` | step 接受的每一個 input variable |
| `arguments[].name` | input variable 的名稱 |
| `arguments[].required` | 它是否為 required |
| `arguments[].type` | 它的 data type：`string`、`integer`、`number`、`boolean` 或 `path` |
| `arguments[].description` | 它的提示說明 |

每一個欄位名稱與代碼標籤，都照上面的拼法逐字寫出。

**它怎麼寫**

- Python 3.10 以上，使用 workspace 的 `.venv`，每個函式都加上 type hint，命令列介面以 `click` 建構。
- 每個檔案都以 UTF-8 讀取，並移除任何 byte-order mark。
- 為每個 input variable 的選項，指定與它的 `type` 相符的 `click` parameter type：`path` 用 `click.Path`，`string`、`integer`、`number` 與 `boolean` 分別用 `str`、`int`、`float` 與 `bool`。
- 以 `hidden=True` 宣告 `--export-schema`；收到它時，以 Python 內建的 `json.dumps()` 印出 metadata，再呼叫 `sys.exit(0)`。
- 不對應任何 step 的 identifier 以 `click.BadParameter` 拋出；每一個 refusal 都在做任何工作之前，以 `click` 的 usage-error 狀態 `2` 退出。
- 絕不呼叫 `input()`、`click.prompt()` 或任何其他會等待人的東西。
- 每個 input variable 都以選項取得；credential 只從 Skill Source 讀取它的環境變數或金鑰儲存區讀取，絕不從命令列取得，也絕不向人詢問。
- 從目前的工作目錄——也就是 workspace configuration 檔所在之處——解析 workspace，絕不從 script 自己的位置推導。
- 為每個 Step Action 寫一個 Action Logic Builder：它呼叫 skill 的該 step 所執行的程式、做人判定為 chore 的工作，或把 Cognitive step 以 handoff 交出。
  builder 絕不呼叫另一個 step 的 builder，也不為之後的呼叫在記憶體中保留任何東西。
- 每個 Deterministic step 寫出的，恰好就是 skill 的該 step 所寫出的——同樣的檔案、名稱、位置與結構——而且只在先前的 step 保存下來的東西或它們讀取的檔案中找它們的產出。
- Cognitive step 不含任何 LLM 呼叫：它以 handoff 結束。

**審視它**

寫好 script 之後，依下列規則審視它：每個 step 的 Action type 都是 Step 1 給它的那一種；Cognitive step 不含任何 LLM 呼叫；credential 絕不從命令列取得；workspace 從工作目錄解析；每個選項的 `click` type 與它宣告的 `type` 相符；docstring 以 description 開頭，並列出每一個 Step Action。

## Step 3 - Correct the Script

**輸入**：Compiled Script 沒有通過的 contract 檢查，各附上它的發現；或 Step 4 判定出在 script 的差異。

- 照 Step 2 的寫法再整份寫出 script，修正輸入所指出的問題。
- 絕不為了讓檢查通過或讓 step 相符而修改 Skill Source。
- 照 Step 2 的方式審視修正後的 script。
- 修正後的 script 從第一項 contract 檢查起重新檢查，Step 4 也從頭重新證明它的 step。

## Step 4 - Prove the Steps

**輸入**：Compiled Script 的 introspection metadata 所列的 Step Action，以及 Skill Source；之後是每一次執行的 exit status、它印出的內容與它寫出的東西。

- 依來源順序，為每個 Deterministic step 選一個不改變任何共享事物的輸入——例如空的日期區間、沒有子項的 ID，或不在清冊中的主機——並帶上它的 metadata 所宣告的 input variable。
- 來源需要 required 輸入、或驅動實際運作中的整合時，絕不選該 step 的預設值。
- 會改變共享狀態的 step——寫入某個服務、寄送郵件、push 或刪除——不為它選輸入，並回報為沒有執行，附上理由。
- 每個選定的 step 都從 workspace 中，像 caller 那樣以各自獨立的呼叫執行一次。
- 把每次執行的產出，與它的來源 step 所說的產出比對——檔案、它們的名稱與位置，以及其中的段落與欄位——並引用回傳的內容。
- 每個 step 給一個結果：通過，附上它的產出；沒有執行，附上理由；或有差異，指出差異在哪裡；Cognitive step 的結果是 handoff。
- 差異出在 script——它違反某項 contract，或某個 step 產出了它的來源 step 沒有說的東西：交給 Step 3。
- 差異出在來源——某個 step 沒有說它產出什麼，或說得含糊：停止，把這項發現交給 person revising the skill；絕不修補 script 來掩蓋它。
