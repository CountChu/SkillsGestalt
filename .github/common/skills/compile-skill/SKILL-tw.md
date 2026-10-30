---
name: compile-skill
description: >-
  把一個 skill 的 SKILL.md workflow 編譯成 skill.py——一個放在它旁邊的無頭 Python CLI——讓程式做得到的 step 不必經過 LLM 就能執行，不再消耗 token。它沒有自己的設計：編譯出的 script 必須是什麼樣子，由它 references 中的 compile SOP 決定——每個 step 如何分類（deterministic 或 cognitive、automated 或 interactive）、透過 --step 依 identifier 執行單一 step 的 click CLI、供 caller 讀取的隱藏 --export-schema JSON，以及 cognitive step 不呼叫 LLM、改以 handoff 結束時所用的 exit code。不是 skills/<name>/SKILL.md、或其 Workflow 底下沒有 Step N 標題的來源會被拒絕，且什麼都不寫。來源絕不被編輯；skill.py 是唯一的輸出——沒有 MD report，也沒有 YAML checkpoint。每次執行都以實際執行該 script 作結：先檢查其 source fingerprint、schema、handoff 與無頭規則，再以 side-effect-free input 逐一執行每個 deterministic step。觸發語：「compile this skill」、「make skill.py」、「run a skill without the agent」。
---

本文件為 [SKILL.md](.github/common/skills/compile-skill/SKILL.md) 的繁體中文版。
任一份改了某節，另一份必須在同一次執行中一起改。

# TERMINOLOGY

在每個 skill 中意義都相同的 term。

- **`run step N`** — 一個放在 prompt 結尾、指名某一個 step 的選擇子。
  它**只**執行那一個 step，然後停止。
- **MD report** — skill 寫進 wiki vault 的 Markdown 報告，放在以該 skill 命名的資料夾中，於結果各節之上帶有標準表頭（Skill、Checkpoint、Created、Updated、Prompt）。
- **YAML checkpoint** — skill 每次執行之 checkpoint 目錄中的 `process.yaml`。
  每個 step 都把輸出寫在其中的 `step_{N}` 群組下，讓後續 step 讀回而不必重算。
- **no forward-reference** — 一個 step 絕不可依賴排在它之後的 step 的規則。
  為了控制流程而指名後面的 step 並不違反它；借用那個 step 的輸出才違反。

# DEDICATED TERMINOLOGY

本 skill 領域專屬的 term。
每一個定義都由 glossary 擁有——step 使用 term，而不重述它的意思。

- **compile SOP** — 本 skill `references\` 中的 `SKILL-Compile.md`：一次編譯中 agent 所做的判斷，也就是它的 *Terms and Rules* 之後的 Step 1 到 Step 4——為 **Step Action** 分類、寫出 **Compiled Script**、修正它，以及判斷它的執行產出了什麼。
  它決定一份 **Compiled Script** 必須是什麼，它的每個 step 都以所依據的輸入開頭。
  本 skill 執行每一支程式、把輸入交給 **compile SOP**，並補上一次執行在它們之外需要的東西：**target skill**、向使用者提出的問題，以及要顯示的內容。
  本文件以編號加上標題引用它的 step，例如 **compile SOP** Step 1 *Classify the Step Actions*，讓它絕不會被誤認為本 skill 的 step。
- **target skill** — 本次執行所編譯的 skill，在 prompt 上以其目錄名稱或其 `SKILL.md` 的路徑指名。
- **Skill Source** — **target skill** 的 `SKILL.md`，取 **compile SOP** 的 *Terms and Rules* 中的意義。
- **Compiled Script** — 本次執行寫在 **Skill Source** 旁邊的 `skill.py`，取同一意義。
  它是本 skill 唯一的輸出。
- **source fingerprint** — **Compiled Script** 所記錄的 **Skill Source** 指紋，取 **compile SOP** Step 2 *Write the Compiled Script* 中的意義；該 step 也規定了 stale 的 **Compiled Script** 會做什麼。
  它由 Step 1 的 script 計算。
- **Step Action** — **Skill Source** 之 `# Workflow` 中的一個 step，取 **compile SOP** 的 *Terms and Rules* 中的意義，依其 **step identifier** 執行。
- **step identifier** — 指定一個 **Step Action** 時所用的 identifier，依 **compile SOP** Step 1 *Classify the Step Actions* 的規定，由其 `## Step N` 標題推導而來。
- **Step Action type** — **compile SOP** Step 1 *Classify the Step Actions* 中的四種 Action type 之一。
  每一種的意義由它的表擁有；本文件絕不重述。
- **handoff step** — 屬於任一種 cognitive type 的 **Step Action**，**Compiled Script** 以 **compile SOP** Step 2 *Write the Compiled Script* 的 handoff 結束它。
- **step inventory** — **Source Scanner** 為一份 **Skill Source** 列出的內容，取 **compile SOP** Step 1 *Classify the Step Actions* 之輸入中的意義。
- **Agentic Panel** — 一個以 caller 身分驅動 **Compiled Script** 的使用者介面，caller 取 **compile SOP** 的 *Terms and Rules* 中的意義。
  **compile SOP** 不點名它；本 skill 絕不撰寫它。
- **Source Scanner** — 判定一份 **Skill Source** 究竟能不能編譯，並印出它的 **step inventory** 與 **source fingerprint** 的程式；Step 1 執行它。
- **Contract Checker** — 依 contract 檢查一份 **Compiled Script** 的程式，只以 caller 的方式執行它，並讀取它的文字；Step 3 執行它。
- **side-effect-free input** — **compile SOP** Step 4 *Prove the Steps* 為一個 step 選的那種輸入，挑選成能走到該 step 的各個分支：空的日期區間、沒有子項的 ID、不在清冊中的主機。
- **core work** — 取 **compile SOP** 的 *Terms and Rules* 中的意義。
  一個 step 沒有執行程式的工作是不是 core work，由使用者在 Step 2 的選單中決定。
- **chore** — 取同一意義：那類工作中不是 core work 的那一種。

# CONFIGURATION

本 skill 執行時所使用的具體值。

- **compile SOP** — [SKILL-Compile.md](.github/common/skills/compile-skill/references/SKILL-Compile.md)，位於 `{skillGroups.common}\skills\compile-skill\references\`。
- **Skill Source** — `{skillGroups[<group>]}\skills\<skill-name>\SKILL.md`，於 Step 0 依 prompt 給出的名稱或路徑解析。
- **Compiled Script** — `skill.py`，位於 **Skill Source** 自己的目錄中（**compile SOP** 的 *Terms and Rules*）。
- **Source Scanner** — `{skillGroups.common}\skills\compile-skill\scripts\scan_source.py`。
- **Contract Checker** — `{skillGroups.common}\skills\compile-skill\scripts\check_compiled.py`。

# MUST FOLLOW

- 必須逐步執行 workflow，並顯示每個 step 的編號。
- 每個 step 必須自足。
  **No forward-reference。**
- 程式能以 deterministic 方式完成的 step 必須以 script 執行。
  需要閱讀、判斷或摘要的 step **不可**寫成 script——請寫成自然語言指示，讓 agent 直接執行。
- **遵守 `run step N` 選擇子**：執行 Step N，然後停止；絕不執行更後面的 step。
  本 skill 不寫 YAML checkpoint，因此每個 step 都從 prompt 與磁碟上的檔案重新推導自己的輸入——它做得到，因為 **Skill Source** 與 **Compiled Script** 是任何 step 唯一需要的狀態。
- **本 skill 既不產出 MD report，也不產出 YAML checkpoint。**
  **Compiled Script** 是它唯一的輸出。
- 依照 [scratch-rules.md](.github/common/rules/scratch-rules.md) 決定一次執行的拋棄式檔案放在哪裡、以及如何清理。
- **每一支程式都由本文件執行；compile SOP 不執行任何程式，也不提任何程式或本 skill。**
  下方的 step 執行 **Source Scanner**、**Contract Checker** 或 **Compiled Script**，並把它們印出與寫出的內容，交給它所指名的 **compile SOP** step，作為該 step 的輸入。
  它是下層文件，本文件是上層：**compile SOP** 只寫一次編譯需要的判斷；提到程式或本 skill 的 **compile SOP**，就認識了它本該保持分開的 system。
- **每個 step 都照 compile SOP 所寫的，去做它指名的那些 compile SOP step。**
  下方的 step 只補上一次執行在它們之外需要的東西——程式、**target skill**、向使用者提出的問題，以及要顯示的內容——絕不重述它們說的內容：複製進本文件的規則是第二份副本，兩者終將偏離。
  當本文件與 **compile SOP** 不一致時，以 **compile SOP** 為準；回報這個不一致，而不是在這次執行中自行解決。
- **compile SOP 的 step 對應到本 skill 的 step**：它的 Step 1 與 Step 2 在 Step 2 做，它的 Step 3 在檢查失敗時於 Step 3 做、在差異出在 script 時於 Step 4 做，它的 Step 4 在 Step 4 做。
  它說停止時，這次執行就在那裡結束，回報它所回報的內容，不再寫任何東西。
- **編譯期間絕不編輯 compile SOP。**
  對「一份 **Compiled Script** 必須是什麼」所做的變更是一項獨立的變更，要刻意地、在任何一次執行之外進行——絕不能是編譯某個 skill 的副作用。
- **只寫 Compiled Script。**
  絕不寫 **Agentic Panel**，也絕不寫 **target skill** 的任何其他檔案。
- **在 skill 結束前，顯示 Compiled Script 的路徑**——只顯示路徑，絕不顯示其內容，並呈現為可點擊的 Markdown 連結，絕不用 inline code 或純文字。
  每次執行都要這麼做，包含像 `run step 0` 這樣的部分執行。

# Prompt Examples


## Prompt 1

```
/compile-skill
report-skills
```

## Prompt 2

```
/compile-skill report-logs --force
```

## Prompt 3

```
/compile-skill
report-skills
run step 3
```

## Prompt 4

```
Compile the report-suts-usage skill into skill.py so I can run it directly.
```


# Workflow

## Step 0 - Warmup

- 先執行 `.venv`。
  Step 1 與 Step 3 的 script 會 import `PyYAML`，而 **Compiled Script** 需要 **compile SOP** Step 2 *Write the Compiled Script* 所指定的直譯器版本與套件。
  逐一確認它們都在，例如用 `python --version` 與 `python -c "import click, yaml"`；任何一項缺少就停止，並指出缺了什麼——絕不為一個 script 無法在其上執行的工具鏈編譯。

- 讀取 workspace 根目錄的 workspace config [config.yaml](config.yaml) 並解析：
  - **`skillGroups`**：群組名稱 -> skills 根目錄的對應——裸的 skill 名稱解析為 `{skillGroups[<group>]}\skills\<skill-name>\SKILL.md`，而本 skill 自己的目錄是 `{skillGroups.common}\skills\compile-skill\`。
  - 在下方各 step 中凡出現 `{skillGroups.common}` 或 `{skillGroups[<group>]}` 之處（包含指令中），都代入解析後的值。
  - 若 `config.yaml` 不存在或缺少 `skillGroups`，停止並詢問使用者。

- 本 skill 不呼叫任何屬於自己的 API，也不需要憑證。
  絕不為此提示使用者輸入。

- 執行 workflow 前，先確認下列 script／檔案存在。
  - `{skillGroups.common}\skills\compile-skill\scripts\scan_source.py`
  - `{skillGroups.common}\skills\compile-skill\scripts\check_compiled.py`
  - `{skillGroups.common}\skills\compile-skill\references\SKILL-Compile.md`

- prompt 採用上方 **Prompt Examples** 所示的其中一種形式。
  從中解析：
  - **target skill**（必要）：`/compile-skill` 之後的第一個詞，在同一行或下一行；或是白話 prompt 所指名的 skill。
    它可以是裸的 skill 名稱——在每個 `skillGroups` 根目錄下尋找 `<root>\skills\<name>\SKILL.md` 來解析——也可以是以 `SKILL.md` 結尾的路徑。
    在不只一個根目錄下都相符的名稱是有歧義的：列出所有相符項並詢問是哪一個，絕不挑第一個。
  - **`--force`**（選用）：不詢問就覆寫既有的 **Compiled Script**。
  - **`run step N`**（選用）：結尾的 step 選擇子。

- 若缺少 **target skill**，向使用者詢問。

- 確認 **Skill Source** 存在。
  它是否為本 skill 接受的來源，由 Step 1 判定，而不由本 step 判定。

- 依 **compile SOP** 的 *Terms and Rules* 的要求，確認 **target skill** 已經穩定。
  依已知的資訊判斷——使用者的說法，或 **Skill Source** 最近一次修改是多久以前——若它仍在修改中，就說明這點並詢問是否仍要編譯。

- 推導 **Compiled Script** 的路徑：**Skill Source** 目錄中的 `skill.py`。
  - 若它已存在，說明這點——但先不詢問：要不要覆寫它，是即將寫入它的那一刻才該問的問題，不該在來源都還沒經過判定之前就問。
  - 若它不存在，`run step 3` 或 `run step 4` 就沒有東西可檢查——說明這點並停止。

- 若 **Skill Source** 旁邊有一個 `main.py`，說明這點並保留它——本 skill 只寫 `skill.py`，要不要移除另一個執行器由使用者決定。

- 顯示解析後的 **Skill Source** 路徑與 **Compiled Script** 路徑。


## Step 1 - Validate the Skill Source

- 對 Step 0 解析出的 **Skill Source** 執行 **Source Scanner**，也就是 `scan_source.py`。
  - 範例：`python {skillGroups.common}/skills/compile-skill/scripts/scan_source.py --file "{skillGroups.common}/skills/report-skills/SKILL.md"`

- 依 exit code 處置：
  - `0`，valid：繼續，並留下它印出的 **step inventory** 與 **source fingerprint**。
  - `2`，`INVALID`：**就此停止 skill**——回報它印出的理由，並且不寫 **Compiled Script**。
  - `64`，沒有 verdict——命令格式錯誤，或檔案不存在、無法讀取：修正命令或路徑，再執行一次。

- 顯示 **step inventory**——每個 step 的編號與標題——以及任何警告。


## Step 2 - Classify and Compile the Step Actions

- 以 Step 1 印出的 **step inventory** 與 **source fingerprint** 為工作依據。
  遇到 `run step 2` 時，再執行一次 Step 1 的 script 來重新推導它們，並在判定為 `INVALID` 時，完全照 Step 1 的做法停止。

- 讀完整份 **Skill Source**，再讀完整份 **compile SOP**。
  每次執行都要讀——決定 type 與 script 形狀的是 **compile SOP**，而不是對前一次編譯的記憶。

- 做 **compile SOP** Step 1 *Classify the Step Actions*，交給它 **Skill Source**、**step inventory**，重新編譯時再加上既有 **Compiled Script** 的 docstring，並為使用者做到下列兩點：
  - 把它的分類呈現為一張 **Classification table**，欄位為 **Step identifier**、**Title**、**Step Action type**、**Arguments**、**Program**——它所呼叫的程式，或它沒有呼叫程式時使用者的決定——與 **Why**——用一行說明是什麼決定了該 type。
    表中 cognitive 的那幾列就是 **handoff steps**：這次執行不會編譯的 step。
  - 把它的每一個 core work 或 chore 問題，以選單向使用者提出：每個 step 一個問題，引用該 step 做什麼，提供下列三個選項，推薦其中一個並說明理由——重新編譯時，推薦既有 **Compiled Script** 的 docstring 所記錄的決定：
    1. **Chore**——本 skill 把它寫進 **Compiled Script**。
    2. **Core work**——這次執行停止。
    3. **Cognitive**——分類錯了，這個 step 改為 **handoff step**。

- 若 **Compiled Script** 已存在且沒有給 `--force`，在寫入任何東西之前，先說明這點並詢問是否覆寫——讓使用者看著 **Classification table** 作答，知道取而代之的會是什麼。
  若被拒絕，這次執行就此結束，什麼都不寫。

- 做 **compile SOP** Step 2 *Write the Compiled Script*，交給它分類、使用者的決定與 Step 1 印出的 **source fingerprint**，寫到 Step 0 推導出的路徑。

- 顯示 **Compiled Script** 的路徑與大小。


## Step 3 - Check the Script Contracts

- 對 **Skill Source** 與 **Compiled Script** 執行 **Contract Checker**，也就是 `check_compiled.py`。
  - 範例：`python {skillGroups.common}/skills/compile-skill/scripts/check_compiled.py --source "{skillGroups.common}/skills/report-skills/SKILL.md" --script "{skillGroups.common}/skills/report-skills/skill.py"`
  - 它只在 workspace 之外的暫存地點執行 script，不執行任何 deterministic **Step Action** 的實際工作：那由 Step 4 證明。

- 依 exit code 處置：
  - `0`，每一項檢查都通過：繼續。
  - `1`，至少一項檢查失敗：逐一回報每項失敗的檢查及其訊息，以這些檢查作為輸入做 **compile SOP** Step 3 *Correct the Script*，並重跑本 step 直到通過。
    修正的是 script——絕不是 **Skill Source**，也絕不是 **compile SOP**。
  - `2`，**Skill Source** 為 `INVALID`：停止，完全照 Step 1 的做法。
  - `4`，script 為 stale：絕不以把指紋寫進 script 的方式修正；完整的一趟執行時，回到 Step 1，`run step 3` 時，停止並說明必須以完整的一趟重新編譯它。
  - `64`，沒有 verdict——命令格式錯誤，或它所指名的檔案不存在、無法讀取：修正命令或路徑，再執行一次。

- **compile SOP** Step 2 *Write the Compiled Script* 用來審視 script 的那些規則，以及 script 從未被手動修改這一點，都回報為沒有檢查，絕不回報為通過：這裡和其他任何地方都沒有檢查能證明它們。

- 若某項失敗原來是 **compile SOP** 本身內部的矛盾，就明白說出來，留給使用者在另一次執行中解決。

- 顯示結果：通過了幾項檢查，以及 script 印出的 **Step Action** 清單。


## Step 4 - Prove the Deterministic Steps

- 以 `--export-schema` 執行磁碟上的 **Compiled Script**，把它印出的 **Step Action** 清單連同 **Skill Source** 交給 **compile SOP** Step 4 *Prove the Steps*：它為每個 deterministic **Step Action** 選一個 **side-effect-free input**，或說明該 step 為何不執行。
  - 範例：`python {skillGroups.common}/skills/report-skills/skill.py --export-schema`

- 照它說的方式，以它選的輸入執行它選定的每個 step：`python <Compiled Script> --step <id>`，再加上那些參數。
  把每次執行的 exit code、印出的內容與寫出的東西，交回 **compile SOP** Step 4 *Prove the Steps* 判斷。

- 它判定差異出在 script 時，以那項差異作為輸入做 **compile SOP** Step 3 *Correct the Script*，重做 Step 3，再重做本 step。

- 顯示：
  - 執行單一 **Step Action** 的指令：`python <Compiled Script> --step <id>`，再加上該 step 宣告的參數。
  - 一張 **Result table**，欄位為 **Step identifier**、**Step Action type** 與 **Result**——`passed` 並附上它產生的東西、`not run` 並附上原因，或對 **handoff step** 標 `handoff`，並指名使用者或 agent 必須在該處執行的來源 step。

- 以可點擊的 Markdown 連結呈現 **Compiled Script** 的路徑作結。
