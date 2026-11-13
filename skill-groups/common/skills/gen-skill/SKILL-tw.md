---
name: gen-skill
description: >-
  建立一個新的 skill，以 SKILL 與 README 兩份 template 逐步完成——從 prompt 解析 skill 名稱與描述，詢問新 skill 產出哪些輸出、使用哪一個 Working Dir、是否要繁體中文 twin，把 SKILL template 複製進選定的 skillGroups 根目錄，以取代每一個 placeholder 的方式，產出它從 prompt 上方的對話推出的 workflow，並為該 workflow 需要的任何 script 或參考檔建立佔位檔。接著以 README template 寫出該 skill 的 README.md——Dataflow、每個 step 的 Purpose、每個 step 用到的檔案、哪些檔案要一起改，以及它的 header quote 宣告的檔案，這些檔案的指紋由 depends_on.py 記錄。若已有同名 skill，則在使用者確認後才覆寫它。使用者要了 twin 時，由 chinese skill 寫出 SKILL-tw.md 與 README-tw.md，它可能在共用的 keep-English list 加入一個 term，並在使用者同意後 commit 這兩份 twin。每次執行都會寫出它的 run record。
---

本文件為 [SKILL.md](skill-groups/common/skills/gen-skill/SKILL.md) 的繁體中文版。
任一份改了某節，另一份必須在同一次執行中一起改。

# TERMINOLOGY

在每個 skill 中意義都相同的 term。

- **Run Number** — 一次執行的編號 `{yymmdd}.{N}`。
  `{N}` 是本 skill 在那一天的執行序號，從 1 開始。
- **Working Dir** — 每次執行的目錄，存放一次執行的所有 working data：它的 step 檔、資料檔與暫存檔。
  它是 Temp Dir 或 Checkpoint Dir，由 skill 的 CONFIGURATION 指明是哪一個。
- **Temp Dir** — 位於 `temp\<skill-name>\{yymmdd}.{N}\` 的 Working Dir，在 workspace 根目錄之下。
- **Checkpoint Dir** — 位於 `checkpoints\<skill-name>\{yymmdd}.{N}\` 的 Working Dir，在 workspace 根目錄之下。
- **Step file** — Working Dir 內的 `step_{N}.yaml`。
  每個 step 都把輸出寫進自己的 step 檔，讓後續 step 讀回而不必重算。
- **Run record** — `database\skill-runs\<skill-name>\{yymmdd}.{N}.yaml`，一次執行每個 step 的時間與模型；每個 skill 都寫一份。
- **MD report** — skill 寫進 wiki vault 的 Markdown 報告，放在以該 skill 命名的資料夾中，於結果各節之上帶有標準表頭（Skill、Run record、Created、Updated、Prompt）。

# DEDICATED TERMINOLOGY

本 skill 領域專屬的 term。

- **SKILL template** — Step 2 複製成新 skill 之 `SKILL.md` 的那個 template 檔案。
  它的 placeholder 就是 Step 3 要取代的對象，因此它的形狀就是每一份被產出的 `SKILL.md` 的起點。
- **README template** — Step 5 複製成新 skill 之 `README.md` 的那個 template 檔案：skill 中執行時用不到、修改時才用得到的部分。
  它的 placeholder 就是 Step 5 要取代的對象。
- **placeholder** — 兩份 template 裡的 `{PLACEHOLDER}` token，站在真實值應該在的位置：大括號裡是大寫字母、數字與底線。
  只要還留著一個，不論在不在反引號裡，這次執行就沒有結束；`{PLACEHOLDER}` 這個名稱本身只用來談論 placeholder，從來不是一個 placeholder，而小寫的大括號，例如 `{skillGroups.common}`，是執行時才解析的值。
- **Skill group** — 新 skill 要寫進哪個 `skillGroups` 鍵的根目錄。
- **new skill directory** — 本 skill 建立並填寫的那個目錄：新 skill 的 `SKILL.md`、它的 `README.md`，以及旁邊的任何輔助檔。
  它是本 skill 唯一的輸出。
- **TW twins** — Step 6 請 `chinese` skill 寫在所產生之 `SKILL.md` 與 `README.md` 旁邊的 `SKILL-tw.md` 與 `README-tw.md`。
  它們是選用的：Step 1 會詢問，而多數 skill 並不需要。
- **Dependency Checker** — 共用的 `depends_on.py`：它讀取一個檔案的 header quote，為其宣告的檔案計算指紋，並記錄每一項的日期與指紋。

# CONFIGURATION

本 skill 執行時所使用的具體值。

執行時讀取或執行的輸入與工具：

- **Workspace configuration** — workspace 根目錄的 [config.yaml](config.yaml)。
- **SKILL template** — `{skillGroups.common}\templates\SKILL-tmp.md`。
- **README template** — `{skillGroups.common}\templates\README-tmp.md`。
- **Dependency Checker** — `{skillGroups.common}\scripts\depends_on.py`。
- **DFD notation** — `{skillGroups.common}\references\DFD.md`。
- **skill-writing rules** — `{skillGroups.common}\rules\skill-writing.md`。
- **run data rules** — `{skillGroups.common}\rules\run-data-rules.md`。
- **chinese skill** — `{skillGroups.common}\skills\chinese\SKILL.md`。

最後的輸出，人、另一個 skill 或之後的分析會讀它：

- **Run record** — `database\skill-runs\gen-skill\{yymmdd}.{N}.yaml`。
- **new skill directory** — `{skillGroups[<group>]}\skills\<skill-name>\`，其中 `<group>` 是 Step 0 選定的 **Skill group**。
- **TW twins** — `SKILL-tw.md` 與 `README-tw.md`，位於 **new skill directory** 之中。

# MUST FOLLOW

- 必須逐步執行 workflow，並顯示每個 step 的編號。
- **本 skill 沒有 `run step N` 選擇子——每一次執行都是完整的一趟。**
  每個 step 都餵給下一個，而且沒有一個是昂貴的，因此沒有值得續跑的對象。
  絕不替它發明一個 step 選擇子。
- **本 skill 既不產出 MD report，也不產出 step 檔。**
  它的產物是 **new skill directory**：Step 2 複製、Step 3 填寫的那份 `SKILL.md`、Step 4 建立的任何 `scripts\` 或 `references\` 佔位檔、Step 5 寫出的 `README.md`，以及使用者在 Step 1 要求時的 **TW twins**。
  除此之外，每一次執行都寫出自己的 **Run record**。
- 依 [run-data-rules.md](skill-groups/common/rules/run-data-rules.md) 處理一次執行的 Run Number、run record 與 Working Dir。
  在最後一個 step 之前停下的執行，依它所說，在 run record 中寫入 `result: stopped` 與 `stopped_at`。
- **skill 結束之前，顯示 run record 的路徑**——只顯示路徑，絕不顯示內容，寫成可點擊的 Markdown 連結，絕不寫成 inline code 或純文字。
  連結目標從 workspace 開始，以正斜線為分隔符號：`[{yymmdd}.{N}.yaml](database/skill-runs/gen-skill/{yymmdd}.{N}.yaml)`。
- **所產生的 `SKILL.md` 絕不連到它的 `README.md`。**
  skill 每次執行都會載入整份 `SKILL.md`，一個連結會把執行引進一份不含任何執行所需內容的檔案。
- **新 skill 的 `SKILL.md` 與 `README.md` 不帶 template 的任何 STE 標記。**
  以 ASD-STE100 Simplified Technical English 寫成的 template，在 header quote 宣告 `[[ASD-STE100_ISSUE9.pdf]]` 與 `[[ste-custom]]`，並有一段 header note，說明它是 STE 檔並列出它的技術用字。
  Step 2 與 Step 5 從複製來的檔案拿掉這兩行 header quote 與整段 header note：本 skill 寫進新檔案的內容從不經過 STE 檢查，留著這些標記，就等於宣稱做過一次沒有人做過的檢查。
- **絕不手寫 header quote 中的日期或指紋。**
  **Dependency Checker** 會在 Step 5 寫入它們，那時它所擔保的 `README.md` 已經寫好；手打的指紋，擔保的是一次沒有人做過的閱讀。
- **絕不手寫 TW twins。**
  Step 6 委派給 `chinese` skill，而該 skill 的 parity check 才是證明每一份 twin 保住了其來源檔之 headings、fences、tables、links 與 placeholders 的依據。
  在這裡寫出來的 twin 會跳過那道檢查。

# Prompt Examples


## Prompt 1

```
/gen-skill
compare-builds
Compare two pipeline builds and report differences.
```

## Prompt 2

```
/gen-skill
Compare two pipeline builds and report differences.
example:
/compare-builds
https://dev.azure.com/contoso/Firmware/_build/results?buildId=1234567&view=results
https://dev.azure.com/contoso/Firmware/_build/results?buildId=1234500&view=results
```


# Workflow

## Step 0 - Warmup

- 找出 `{python}`，也就是 workspace 根目錄的 `.venv` 裡的 Python。
  macOS 與 Linux 上它是 `.venv/bin/python`，Windows 上是 `.venv\Scripts\python.exe`。
  後面 step 的每個 script 都以 `{python}` 執行：**Dependency Checker** 需要 `PyYAML`。
  每個指令都在新的 shell 裡執行，新的 shell 不會沿用另一個指令啟動的 `.venv`。
  workspace 沒有 `.venv` 時，停下來。
  請使用者照 `common` skill group 的 forge-setup.md 第 3 步建立它。

- 讀取 workspace 根目錄的 workspace config [config.yaml](config.yaml) 並解析：
  - **`skillGroups`**：群組名稱 -> skills 根目錄路徑的對應（例如 `common` / `dedi` / `external`）。
    下方用到的每個 skills 根目錄都是 `{skillGroups[<group>]}\skills\`，而兩份 template 都在 `{skillGroups.common}\templates\` 之下。
    絕不寫死 `skill-groups\...`。
  - **`wikiDir`**：新 skill 之 MD report 目錄所用的 wiki 根目錄（Step 1）。
- 若 `config.yaml` 不存在或缺少所需的鍵，停止並詢問使用者。

- 開始執行 workflow 之前，檢查下列檔案是否存在；缺少任何一個時，停止並指出缺少的是哪一個。
  - **SKILL template** 與 **README template**。
  - `{skillGroups.common}\references\DFD.md`——Step 5 畫 Dataflow 所依的畫法。
  - `{skillGroups.common}\rules\skill-writing.md`——Step 3 與 Step 5 寫作所依的規則。
  - **Dependency Checker**。

- prompt 採用上方 **Prompt Examples** 所示形式之一。
  依下列方式解析：
  - **Prompt 1**：
    - **Skill name** = 第 2 行（例如 `compare-builds`）。
    - **Skill description** = 第 3 行。
  - **Prompt 2**：
    - **Skill description** = 第 2 行。
    - **Skill name** = `example:` 之後第一行的斜線指令名稱（例如 `/compare-builds` 取為 `compare-builds`）。
    - 其餘的範例行視為推斷 workflow steps 用的對話脈絡，而非 gen-skill 的輸入。

- 若無法從這些形式解析出 skill 名稱或描述，向使用者索取。
  忽略任何其他形狀的 prompt。

- 下列項目不從 prompt 解析：
  - **Skill group**：`skillGroups` 的鍵之一，依該 skill 是什麼而定。
    通用且與專案無關的 skill 放 `common`；只在某一個專案裡才講得通的 skill 放該專案的群組。
    絕不選 `external`——那個根目錄保留給匯入的第三方 skill。
    - 不需要另外註冊：每一個 `skillGroups` 根目錄都已列在 workspace 檔案的 `chat.agentSkillsLocations` 之下。
      VS Code 掃描每個根目錄只往下一層（`<root>/<dir>/SKILL.md`），因此新增的群組資料夾必須以自己的一筆項目加進那裡（相對路徑、正斜線、不用萬用字元），並加進 `config.yaml` 的 `skillGroups`，其下的 skill 才會被發現。
  - **Workflow steps**：從 prompt 上方的對話脈絡推斷。

- 檢查是否已有同名 skill 存在於任一 `skillGroups` 根目錄下（`{skillGroups[<group>]}\skills\<skill-name>\`）。
  若已存在，警告使用者並詢問是否覆寫。

- 保留 canonical skill invocation，作為 run record 的 `prompt`。

- 依 run-data-rules.md 所說取得 Run Number，並寫出這次執行的 run record。
  把這個 step 加進 run record。


## Step 1 - Ask which output files the skill produces

- 詢問使用者新 skill 產出下列哪些，並接受 `both`、`md`、`steps` 或 `none`：
  - 位於 `{wikiDir}\<skill-name>\` 之下的一份 **MD report**。
  - 位於它的 **Working Dir** 裡的 **step 檔**。
  每個 skill 都寫一份 **run record**，所以不必問。

- 若會產出 MD report，詢問它的檔名樣式（例如 `run-pr-{prId}-{yymmdd}`）。

- 詢問新 skill 使用哪一個 **Working Dir**，並接受 `temp`、`checkpoints` 或 `none`：
  - `temp` → **Temp Dir**，`temp\<skill-name>\{yymmdd}.{N}\`。
  - `checkpoints` → **Checkpoint Dir**，`checkpoints\<skill-name>\{yymmdd}.{N}\`。
  - `none` → 該 skill 不寫 working data：沒有 step 檔、沒有資料檔，也沒有暫存檔。
  一次執行絕不同時使用兩者，因此它的 step 檔、資料檔與暫存檔全都放進這裡選定的那一個。
  只有在該 skill 不產出 step 檔、也不寫資料檔與暫存檔時才接受 `none`；否則再問一次。

- 詢問這個新 skill 是否也要 **TW twins**，並接受 `yes` 或 `no`。
  預設為 `no`——多一份 twin，日後每一次修改要動的範圍就加倍，因為任一份改了某節，另一份必須在同一次執行中一起改。
  這一題和輸出一起在這裡問，因為答案也決定 `README.md` 的內容：有 twin 的 skill 會把它們列在要一起改的檔案中，並宣告它所依賴的 `chinese` skill。

- 把這個 step 加進 run record。


## Step 2 - Copy the SKILL template

- 把 **SKILL template** 複製到 **new skill directory** 的 `SKILL.md`，並顯示目的路徑。

- 把這個 step 加進 run record。


## Step 3 - Build SKILL.md

- 依 [skill-writing.md](skill-groups/common/rules/skill-writing.md) 寫作：每個 step 都自足，程式能以 deterministic 方式完成的 step 執行腳本，而 `SKILL.md` 中不放任何執行時用不到的內容——不放 Dataflow 與 Purpose，它們在 Step 5 寫進 `README.md`，也不放連到那份 `README.md` 的連結。

- 把複製後檔案中的每一個 **placeholder** 全部取代掉：
  - `{SKILL_NAME}` → Step 0 解析出的 skill 名稱。
  - `{SKILL_DESCRIPTION}` → Step 0 解析出的 skill 描述。
  - `{SKILL_GROUP}` → Step 0 選定的 **Skill group**。
  - `{NATURAL_LANGUAGE_PROMPT}` → 一個實際可用的自然語言範例 prompt。
  - `{REPORT_FILENAME}` → Step 1 得到的 MD report 檔名樣式。
  - `{WORKING_DIR}` → Step 1 選定的 Working Dir，帶入新 skill 的名稱，去掉最後的反斜線：`temp\<skill-name>\{yymmdd}.{N}` 或 `checkpoints\<skill-name>\{yymmdd}.{N}`。
    選 `none` 時，用到它的 step 改寫成不用它。

- 依 Step 1 的回答編輯 MUST FOLLOW 區段：
  - 不產出 MD report → 移除 report-md-rules 與 MD report 兩行。
  - 在 CONFIGURATION 的「輸入與工具」一組，列出 skill 讀取的每一個檔、它執行的每一個 script 與它使用的其他程式，例如範本、reference 或另一個 skill；skill 寫出的東西都不放在這裡。
  - 在 CONFIGURATION 中，沒有別的 skill 讀它的輸出就移除 Handoff file 那一行。
  - 在 CONFIGURATION 中，只保留 Step 1 回答的那一行 Working Dir，即 Temp Dir 那一行或 Checkpoint Dir 那一行，並移除另一行；選 `none` 時兩行都移除。
    在保留的路徑之後寫上 skill 放進去的東西；執行會寫暫存檔之 script 的 step，把 Run Number 傳給該 script。
  - 在 TERMINOLOGY 中，保留 Working Dir 這個 term 與 Step 1 選定的那一種的 term，並移除另一種。
    在 Working Dir 這個 term 中，把「它是 Temp Dir 或 Checkpoint Dir，**CONFIGURATION** 列出是哪一個。」改成寫出選定的那一種，例如「在本 skill 中，它是 Checkpoint Dir，**CONFIGURATION** 列出它。」
    選 `none` 時三個都移除，Step file 這個 term 也移除。
  - 在 CONFIGURATION 之後，把這個目錄稱為 Working Dir，絕不稱為 Temp Dir 或 Checkpoint Dir；其中的檔案寫成 Working Dir 中的 `step_3.yaml`，而不寫完整路徑。
  - 沒有 Working Dir → 移除「每份檔案只有一個寫入者」那一項和緊接在後、說明其原因的那一項——沒有 Working Dir，它們就什麼也規範不到。
  - 每個 skill 都保留 run-data-rules 那一行與顯示路徑那一行，因為每個 skill 都寫 run record；沒有 MD report 時，路徑那一行只顯示 run record。

- 編輯 Step 0 - Warmup：
  - 若該 skill 沒有任何 step 執行 script，移除 `{python}` 那一條。
  - 在 `config.yaml` 那一條中，只保留該 skill 實際需要的鍵（Step 1 說沒有 MD report 時就拿掉 `wikiDir`）。
  - 若該 skill 不呼叫 Azure DevOps，移除 `ADO_PAT` 的解析與驗證兩條。
  - 移除 scripts／files 檢查區段，或以該 skill 的腳本取代 `{SCRIPT_PATH_1}`。
  - 把 `{INPUT_1}` / `{INPUT_2}` 換成該 skill 從其 prompt 解析的輸入。
  - 若 Step 1 說沒有 step 檔，移除 `step_0.yaml` 那一行；保留 Run Number 與 run record 那兩行。

- 用 Step 0 推斷出的 workflow steps 取代 `{STEP_N_TITLE}` placeholder 區段——以及其中的每一個 placeholder，包含名稱不是 `{STEP_N_*}` 的那些（例如 `{SCRIPT_1_ACTION_1}`、`{ROW_1}`、`{COLUMN_1}`）。
  依需要增加或刪除 step 區段，並針對該 skill 不產出的輸出，刪掉各區段的 `Save step_N.yaml` / `Save MD report file` 那一行；保留每一個 `Add this step to the run record` 那一行。

- 不要留下任何 **placeholder**——收尾前先掃過檔案，找緊接在 `{` 之後的大寫字母；只有 `{PLACEHOLDER}` 可以留著。

- 顯示產生出來的 SKILL.md 內容。

- 把這個 step 加進 run record。


## Step 4 - Create supporting files

- 若 Step 3 寫出的任何 step 會執行 script，就在 **new skill directory** 的 `scripts\` 之下為它建立一個佔位 script 檔。
- 若 Step 3 寫出的任何 step 需要參考用的 template，就在 **new skill directory** 的 `references\` 之下為它建立一個佔位檔。
- 顯示已建立的檔案清單。

- 把這個 step 加進 run record。


## Step 5 - Build README.md

- 把 **README template** 複製到 **new skill directory** 的 `README.md`，並依 [skill-writing.md](skill-groups/common/rules/skill-writing.md)，以 Step 3 寫出的 `SKILL.md`、Step 4 建立的檔案與 Step 1 的回答填寫它。
  它提到的每一個 step，名稱都與該 step 在 `SKILL.md` 中的標題完全相同、連編號一起。

- 取代開頭部分的 placeholder：
  - `{SKILL_NAME}` → Step 0 解析出的 skill 名稱。
  - `{SKILL_DIR}` → **new skill directory**，相對於 workspace，使用正斜線。
  - `{COMMON_DIR}` → `{skillGroups.common}`，相對於 workspace，使用正斜線。
  - `{COMMON_PATH}` → 從 **new skill directory** 到 `{skillGroups.common}` 的相對路徑，使用正斜線——`common` 群組中的 skill 為 `../..`。
  - `{MORE_PATH_ABBREVIATIONS}` → 圖中用到的其他每一個簡寫各一行，例如一次執行所處理的檔案或 Working Dir；沒有的話就什麼也不寫。

- 保留 header quote 中適用於新 skill 的行，移除其餘的行：
  - 一律保留：`DFD.md`、`md-style.md`、`skill-writing.md`、`run-data-rules.md`、`SKILL-tmp.md` 與 `README-tmp.md`。
  - 寫 MD report 時保留 `report-md-rules.md`。
  - Step 1 的回答要了 **TW twins** 時，保留 `chinese/SKILL.md`。
  - **new skill directory** 之外、任何 step 會讀取或執行的其他每一個檔案，各加一行，例如共用的腳本——寫成相對於 `README.md` 的路徑連結，和 template 中的各行一樣。

- **Dataflow**：重畫 template 的圖，讓它畫的是這個 skill，而不是 template 的範例，畫法依 [DFD.md](skill-groups/common/references/DFD.md)：每個 step 都是一個圓角方框，名稱與它的標題完全相同；每個 step 讀取的每一份輸入與寫出的每一個 record——prompt、`config.yaml`、讀取的每一份文件、Working Dir 中的每一份資料檔，以及每個 step 自己的 step 檔與在 MD report 中的那一節。
  Step 1 說該 skill 不產出的東西一併拿掉，重新為 `linkStyle` 中的藍色箭頭編號，並讓圖下方的圖例與圖現在所畫的一致。

- **Step Purposes**：每個 step 一項，第一行是它的標題，縮排的下一行是它的 Purpose——一句話說明這個 step 為何要獨立存在、把它折進相鄰的 step 裡 skill 會損失什麼，絕不是這個 step 做了什麼的摘要。

- **Files Each Step Uses**：在那句粗體句中回答「哪些 step 執行腳本」那條規則一次，說明哪些 step 執行腳本、哪些不執行，以及原因。
  接著在 fenced block 的樹中，於每個 step 底下列出它讀取、檢查、執行——並在它底下列出該腳本讀寫什麼——以及寫出的檔案。

- **When the Skill Is Changed**：在 fenced block 的樹中列出與 `SKILL.md` 一起改的檔案（`⇄`）以及它遵守的規則（`─▶`）：它的腳本與參考檔，以及各 step 對它們的說法；只有在 Step 1 的回答要了 **TW twins** 時才列 twin 的那幾行；規則的那幾行與上面保留的 header quote 一致。
  在 `outputs already written` 底下，指出先前的執行留下、而修改 skill 之後可能停在舊形狀的東西；沒有的話，移除那一支。
  把 `{SKILL_REGRESSION_CHECK}` 換成一次能證明 skill 修改後仍然可用的執行，或移除那一行。

- **Tracked Dependencies**：在 fenced block 的樹中，依同樣的順序列出 header quote 宣告的每一個檔案。

- 不要留下任何 **placeholder**——收尾前先掃過檔案，找緊接在 `{` 之後的大寫字母；只有 `{PLACEHOLDER}` 可以留著。

- 以 **Dependency Checker** 記錄 header quote，它會在每一行之後寫入日期與指紋：
  - 範例：`{python} {skillGroups.common}/scripts/depends_on.py record "<new skill directory>/README.md"`，其中 **new skill directory** 用絕對路徑：這支 script 從目前的目錄讀相對路徑，而不是從 workspace 根目錄。
  - 有一行指不到任何檔案時，它以 `2` 結束：修正那個連結，再記錄一次。

- 以可點擊的 Markdown 連結顯示 `README.md` 的路徑。

- 把這個 step 加進 run record。


## Step 6 - Create the TW twins

- 若 Step 1 的回答是 `no`，說明沒有寫出任何 twin，然後直接做這個 step 的最後兩項。

- 若是 `yes`，就先對 **new skill directory** 的 `SKILL.md`、再對它的 `README.md` 執行 `chinese` skill，把各自的路徑交給它——例如 `/chinese {skillGroups[<group>]}/skills/<skill-name>/SKILL.md`。
  每一次執行都在來源檔旁邊寫出 **TW twins** 中的一份，讓每一個 heading、inline-code span、link target 與 placeholder token 都保留英文——`README.md` 的 header quote 也在其中——並以它自己的 parity check 收尾，接著提議把 twin 與它的來源一起 commit，只在使用者答應時才 commit，而且可能在 keep-English list 中加入一個 term；對 `SKILL.md` 的那一次執行，還會在 twin 的 frontmatter 下方加上 pairing line。

- 不要在這裡翻譯任何一份檔案，也不要在過程中編輯所產生的 `SKILL.md` 或 `README.md`——`chinese` skill 視其來源檔為唯讀。

- 以可點擊的 Markdown 連結顯示 **TW twins** 的路徑。

- 把這個 step 加進 run record，並寫入 `result: completed`，因為這是最後一個 step。

- 以可點擊的 Markdown 連結顯示 run record 的路徑作為結尾。
