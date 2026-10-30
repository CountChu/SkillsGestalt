---
name: asd-ste
description: >-
  把一份英文 Markdown 檔改寫成 ASD-STE100 Simplified Technical English（STE，Issue 9）的 draft，寫在它旁邊給使用者審核，使用者核准之後再讓 draft 取代那個檔案。標題、fenced block、inline code、連結目標、placeholder，以及來源檔自己的 header quote 都維持不變，每一項陳述也都保留；散文依 STE 寫作規則與 STE dictionary 改寫，每行一句。腳本檢查 kept span、句子與段落的上限，並逐詞比對字典與 project-approved words；depends_on.py 記錄指紋；執行時會提議 commit draft、請 chinese skill 寫出它的繁體中文 twin，並產生一份把它與來源並排的 HTML review page。使用者核准後，它以 draft 與 draft 的 twin 取代 source file 與它的 twin，在每一份宣告 source file 的文件中重新記錄它，並檢查結果。每個 step 都把它做了什麼存進 YAML checkpoint，run step N 會把它讀回來。它拒絕 -tw.md twin、已經是 STE 的檔案，以及不是英文的來源檔；只有為了以核准的 draft 取代來源檔，才會改動來源檔。觸發語："rewrite in STE"、"Simplified Technical English"、"ASD-STE100"。
---

本文件為 [SKILL.md](.github/common/skills/asd-ste/SKILL.md) 的繁體中文版。
任一份改了某節，另一份必須在同一次執行中一起改。

> [ste-rules.md](references/ste-rules.md)  `2026-10-30`  `8014dc37df5f`

# TERMINOLOGY

在每個 skill 中意義都相同的 term。

- **`run step N`** — 放在 prompt 結尾、指名某一個 step 的選擇子。
  它**只**執行那一個 step，並從 YAML checkpoint 把先前每一個 step 的輸出讀回來。
- **Checkpoint Dir** — 存放某個 skill 的 YAML checkpoint，以及它的各個 step 所寫資料檔的目錄。
  每個 skill 都有自己的；本 skill 的寫在 **CONFIGURATION** 底下。
- **YAML checkpoint** — Checkpoint Dir 內的 `process.yaml`。
  每個 step 都把輸出寫在其中的 `step_{N}` 群組下，讓後續 step 讀回而不必重算。

# DEDICATED TERMINOLOGY

本 skill 領域專屬的 term。

- **source file** — 本次執行所改寫的英文 Markdown 檔：一份參考文件、一份規則檔、一份 template、一個 skill 的 `SKILL.md`——任何 `.md` 都可以。
- **draft** — 本次執行寫在 source file 旁邊、給使用者審核的檔案，位於 **draft tool** 所給的路徑。
  它是用 STE 重新說一遍的 source file：同樣的標題、fenced block、連結與 placeholder，同樣的陳述，只有散文經過改寫。
  使用者核准它之後，Step 7 就讓它取代 source file。
- **STE file** — 已經是 STE 的檔案：它的 header quote 宣告了 **STE specification**。
  draft 是一種，被 draft 取代過的 source file 也是。
- **STE specification** — `ASD-STE100_ISSUE9.pdf`，即 ASD-STE100 Simplified Technical English，Issue 9。
  沒有任何 step 讀它：Step 3 只為了 **header quote** 取它的指紋。
- **STE rules digest** — 本 skill 自己對 Part 1 寫作規則與一般建議的摘要，附上每一條的編號，後面接著這類文件最需要的替換詞，以及說明如何把 STE 套用到 Markdown 檔的 House Rules。
  Step 2 依它寫作。
- **STE dictionary** — 把 Part 2 的詞彙做成的一個 JSON 檔：每個核准詞附上它的詞性與可用的詞形，每個非核准詞附上取代它的核准詞。
  它也記錄了建置來源 PDF 的版次、日期與指紋。
- **project-approved words** — 本專案在 Issue 9 之外另行核准的詞，做成一張表：每個詞附上它的詞性、詞形、意思，以及使用者核准它的原因。
  `check_ste.py` 把每一個都當成核准詞，並印出一行 `[INFO]`，列出檔案用到的每一個。
- **project rules** — 本專案在 Issue 9 與 **STE rules digest** 的 House Rules 之外另加的寫作規則，做成 **project-approved words** 旁邊的第二張表：每條規則附上一個例子、檢查的方式，以及使用者加上它的原因。
  散文可能違反表中標為會檢查的規則時，`check_ste.py` 會印出一行 `[WARN]`，用兩個否定詞表達肯定意思的句子就是一例。
- **US spelling list** — 共用的英式拼法清單，每一個都附上它的美式拼法，是 [md-style.md](.github/common/rules/md-style.md) 的規則「Write English in American spelling」所依據的清單（STE rule 1.14）。
  `check_ste.py` 在散文與每一個 kept span 中找出每一個，以及它的 -s、-ed、-ing 與 -er 形。
- **technical word** — draft 用到、而 STE dictionary 不核准這種用法的詞：一個完全不核准的詞，或一個核准詞用在字典沒給它的技術意思上（STE rule 1.3），例如以 *record* 指 system 保留的資料。
  它是 source file 主題的技術名詞（STE rule 1.5），例如 *stage* 或 *Dataflow*，或是技術動詞（STE rule 1.12），例如 *parse*。
  **header note** 列出 draft 用到的每一個這種詞，`check_ste.py` 一個也不回報。
  md-style.md 允許保留英式拼法的名稱也列在那裡，讓拼法檢查放過它。
- **kept span** — source file 中逐位元組原樣進入 draft 的片段：每一行 `#` 標題、每一個 fenced block、每一個 inline-code span、每一個連結目標與 wiki link（`[[name]]`）、每一個 `{PLACEHOLDER}` token 與每一個 `{placeholder}` token、frontmatter 的鍵以及 `description` 以外的每一個值，以及 source file 自己 header quote 的每一行。
- **header quote** — Markdown 檔開頭、在它的 frontmatter 或標題底下的那一串 `>` 行：檔案有自己的版本時，第一行就是它，例如 `> Version: 261013`；其餘每行一個依賴，一個連結，接著是 **Dependency Checker** 記錄的日期與指紋，各自放在 inline code 中。
  draft 的 header quote 是 source file 自己的 header quote（如果有的話），後面再接一行宣告 STE specification 的行，例如 `` > [[ASD-STE100_ISSUE9.pdf]]  `2026-10-11`  `d1f4ea9e7cd6` ``。
  再加一行宣告 ste-custom.md：`> [[ste-custom]]`，記錄方式相同；即使散文沒用到任何 **project-approved words**，draft 也要遵守 **project rules**。
- **header note** — draft 中位於 header quote 底下的引用區塊，共三行：連到 source file 的連結、兩者不一致時以 source file 為準的陳述，以及 `Technical words:` 後面接著 draft 用到的每一個 **technical word**。
  draft 取代 source file 之後，第一行拿掉連結，第二行刪除。
- **STE check** — Step 3 的 `check_ste.py` 所做的比對：source file 的每一個 kept span 都在 draft 中，而且 draft 遵守程式能量測的每一條 STE 規則。
  `[FAIL]` 是違反了一條規則；`[WARN]` 是讀者必須自行判斷的一個詞或一個句子。
  只給 `--ste` 時，`check_ste.py` 以程式能量測的規則檢查一份 STE file，不和任何 source file 比對。
- **Dependency Checker** — 共用的 `depends_on.py`：它讀取 header quote，取得其中所指名檔案的指紋，並記錄每一個日期與指紋。
- **dependent** — header quote 記錄了 source file 的文件，不論它在哪一個使用本 workspace 這個 skill group 的 workspace 裡。
  取代之後仍然成立的每一份，Step 7 都在其中重新記錄 source file。
- **draft tool** — 本 skill 的 `draft.py`：它給出一次執行為某個 source file 所用的路徑，並說明 source file 是不是 TW twin 或 STE file；它把核准的 draft 與它的 TW twin 放到 source file 與它的 TW twin 的位置；它也列出 dependent。
- **findings file** — `check_ste.py` 以 `--findings` 寫出的 JSON 檔：它回報的每一項發現，完整不截斷，即使印出的報告縮短了清單。
  Step 1 寫出 `step_1-findings.json`，Step 3 寫出 `step_3-findings.json`，都在 Checkpoint Dir 中。
- **step saver** — 本 skill 的 `save_step.py`：它把一個 step 的群組寫進 YAML checkpoint——標題、時間、step 給的值，以及整份 findings file——並讓其他每一個群組保持原樣。
- **TW twin** — 一份檔案的繁體中文版，由 `chinese` skill 寫在它旁邊。
- **pairing line** — TW twin 中位於第一個標題之上、連回它的英文檔的那一行；`chinese` skill 會在 frontmatter 底下加上一行。
- **review page** — Step 6 為審核 draft 的使用者產生的 HTML 頁面：source file 與 draft 左右並排，各在一欄、各自捲動；兩份 **TW twin** 以同樣的方式並排；以及 draft 與它的 TW twin 逐行並排。
  它們上方列出 STE check 的結果、留下的警告、technical word 與保留原文措辭的陳述，接著是 **review notes**；頁面上的標籤是繁體中文。
  review notes 的每一項，以及它底下的每一項，開頭都是它的 **review status**。
- **review notes** — review page 中由 Step 6 自己寫的部分：審核者應該對照的每一處，以及原因。
- **line reference** — review notes 標示一行的方式：`{{en-o:N}}` 是 source file 的第 N 行，`{{en-d:N}}` 是 draft 的，`{{tw-o:N}}` 是 source file 的 TW twin 的，`{{tw-d:N}}` 是 draft 的 TW twin 的；`N-M` 是一段範圍，`N,M` 是一份清單。
  **review builder** 把每一個都變成連結，點了就打開它那一行。
- **review builder** — 本 skill 的 `make_review.py`：它從四份檔案、YAML checkpoint 與 review notes 產生 review page；只要有 line reference 指不到任何一行，就不寫出頁面。
- **review status** — 審核者在 review notes 的一項上設定的標記：`[ ]` 待審、`[v]` 審核通過、`[?]` 待解釋或 `[x]` 不通過，每點一下就換到下一個。
  `[?]` 表示審核者看不懂這一項的處理方式：agent 在對話裡逐項解釋，review notes 維持原樣。
  `[v]` 表示 draft 的這一處照現狀通過，所以審核者同意某一項的建議時，標 `[x]`，不標 `[v]`。
  遇到 `[x]`，agent 照審核者的決定修改 draft，再重跑 Step 3 與 Step 6。
  一項以它自己的文字來辨認，所以在兩次產生 review page 之間改過的項目，會回到待審。
- **review server** — 本 skill 的 `review_server.js`，以 Node.js 執行：它提供 `checkpoints\asd-ste\` 底下的每一份 review page，列出它們與各自的審核進度，並把它所提供的頁面送來的 review status 寫進那份頁面 Checkpoint Dir 中的 `step_6-status.json`。
  它一直執行，直到使用者把它關掉；以檔案直接開啟的 review page 會顯示建頁時的 review status，但一個也不儲存。

# CONFIGURATION

本 skill 執行時使用的具體值。

- **source file** — prompt 給出的 `.md` 路徑，或在 Step 0 找到的、名稱與 prompt 所給相同的那一個檔案。
- **draft** — draft tool 所給的路徑，位於 source file 自己的目錄。
- **TW twin** — source file 的位於它旁邊，draft 的位於 draft 旁邊，路徑都由 draft tool 給出。
- **Checkpoint Dir** — `checkpoints\asd-ste\{parent}-{name}\`，其中 `{parent}` 是 source file 所在目錄的名稱，`{name}` 是 source file 去掉 `.md` 的檔名：`.github\common\references\DFD.md` 對應 `checkpoints\asd-ste\references-DFD\`。
  draft tool 也會給出它。
  每一份 source file 有一個，每一次執行都重用它。
  裡面有 YAML checkpoint `process.yaml`，以及 Step 1、Step 3 與 Step 6 寫出的檔案：`step_1-inventory.txt`、`step_1-findings.json`、`step_3-check.txt`、`step_3-findings.json`、`step_6-notes.html`、`step_6-review.html` 與 `step_6-status.json`。
- **STE rules digest** — `{skillGroups.common}\skills\asd-ste\references\ste-rules.md`。
- **STE dictionary** — `{skillGroups.common}\skills\asd-ste\references\ste-dictionary.json`。
- **project-approved words** — `{skillGroups.common}\skills\asd-ste\references\ste-custom.md` 的 Words 表。
- **project rules** — `{skillGroups.common}\skills\asd-ste\references\ste-custom.md` 的 Rules 表。
- **US spelling list** — `{skillGroups.common}\references\us-spelling.json`。
- **STE specification** — `ASD-STE100_ISSUE9.pdf`，以 Dependency Checker 尋找 `[[ASD-STE100_ISSUE9.pdf]]` 的方式找到：先在 draft 的 vault 底下找，再到每一個 `skillGroups` 根目錄底下找。
  在 SkillsGestalt workspace 中，它是 `external\ASD-STE100_ISSUE9.pdf`。
- **Dependency Checker** — `{skillGroups.common}\scripts\depends_on.py`。
- **draft tool** — `{skillGroups.common}\skills\asd-ste\scripts\draft.py`。
- **step saver** — `{skillGroups.common}\skills\asd-ste\scripts\save_step.py`。
- **review builder** — `{skillGroups.common}\skills\asd-ste\scripts\make_review.py`。
- **review server** — `{skillGroups.common}\skills\asd-ste\scripts\review_server.js`，位於 `http://127.0.0.1:8790/`，Checkpoint Dir `{parent}-{name}` 的 review page 在 `http://127.0.0.1:8790/{parent}-{name}/`。
- **parity check** — `chinese` skill 的 `{skillGroups.common}\skills\chinese\scripts\check_parity.py`，搭配 keep-English list `{skillGroups.common}\references\tw-keep-english.md`。

# MUST FOLLOW

- 必須逐步執行 workflow，並顯示每個 step 的編號。
- **遵守 `run step N` 選擇子**：執行 Step N，然後停止；絕不執行較後的 step。
  依 prompt 指名的 source file 找到 Checkpoint Dir：路徑可以直接得出 `{parent}-{name}`；只有名稱時，比對 `checkpoints\asd-ste\*-{name}\`，符合的不只一個就列給使用者選。
  從 YAML checkpoint 讀取 Step 0 解析出的路徑，以及先前每一個 step 的輸出。
  Step N 需要的群組不存在時，說明要先執行哪一個 step，然後停止。
- **本 skill 不產出 MD report，但會寫 YAML checkpoint。**
  draft 是它的輸出，Checkpoint Dir 則記錄每一次執行如何產出它，並存放 Step 6 為使用者產生的 review page。
  它其他的寫入，是 Step 4 所做的 commit，以及 Step 5 請 `chinese` skill 寫出的 TW twin，兩者都只在使用者答應時才做；還有 Step 7 所做的取代與記錄，只在使用者核准時才做。
- YAML checkpoint 的形狀與必填欄位，遵循 [report-yaml-rules.md](.github/common/rules/report-yaml-rules.md)。
- **以 step saver 存每個 step 的群組，絕不手寫。**
  每個 step 開始時，在 macOS/Linux 上以 `date '+%Y-%m-%d %H:%M:%S'`、在 PowerShell 中以 `Get-Date -Format "yyyy-MM-dd HH:mm:ss"` 從系統時鐘讀取開始時間，並在 step 結束時交給 step saver：step saver 會讀取結束時間並算出耗時，所以沒有任何時間是估計的。
  手抄進 YAML 的清單，會在毫無提示的情況下漏掉項目。
- **Checkpoint Dir 中的每一個資料檔，都只有一個寫入它的 step。**
  Step 1 寫 `step_1-inventory.txt` 與 `step_1-findings.json`，Step 3 寫 `step_3-check.txt` 與 `step_3-findings.json`，Step 6 寫 `step_6-notes.html`，並透過 review builder 寫 `step_6-review.html`；Step 6 啟動的 review server 寫 `step_6-status.json`；其他 step 都不改動它們。
  YAML checkpoint 是唯一的例外：每個 step 取代其中自己的群組，而 Step 0 會重新開始這個檔案，所以一次執行絕不會把自己的群組和先前執行的混在一起。
  只有 YAML checkpoint 所指名的檔案屬於它那一次執行：先前執行留下的檔案，會在它的 step 再次執行時被取代。
- **提早停止的執行，仍要存下它停在的那一個 step 的群組**，加上 `--stopped` 與原因：被拒絕的來源檔、`NOT-ENGLISH` 或 `SOURCE-FIRST` verdict、不同意覆寫、無法通過的檢查、缺少的 TW twin、draft tool 拒絕的取代。
  這樣 YAML checkpoint 就說明了為什麼那次執行沒有留下 draft、沒有留下 review page，或讓 source file 保持原樣。
- **使用者核准 draft 之前，source file 是唯讀的。**
  絕不編輯、重新排版或「修正」它——即使改寫暴露出它真正的缺陷也一樣。
  回報缺陷，留給使用者處理。
  只有 Step 7 會寫入它，而且只是把核准的 draft 放到它的位置。
- **拒絕本身是 TW twin、STE file，或不是英文的來源檔。**
  twin 該改寫的是它的英文檔，STE file 本來就是 STE，而 STE 是用英文寫的。
  Step 0 依 draft tool 的回報拒絕 TW twin 與 STE file；至於語言，由 Step 1 的 `check_ste.py` 決定，它的 verdict 具有約束力。
- **絕不變更 kept span。**
  改動過的標題、識別碼、路徑、連結目標或 placeholder，就不再對得上它所指稱的東西或指稱它的東西，STE check 也會拒絕它。
- **保留每一項陳述。**
  STE 改變的是一件事怎麼說，絕不改變說了什麼。
  丟掉一個條件的改寫讀起來更順，但它是錯的，而且沒有任何腳本找得到。
  一項無法在不改變其主張的情況下用 STE 說出的陳述，就保留它的 technical word 或它在來源中的措辭，並由 Step 2 列出它。
- **絕不手寫 header quote 裡的日期或指紋。**
  `depends_on.py record` 會在 STE check 通過後寫入它們；手打的指紋，等於為一次沒有人執行過的檢查背書。
- **以不含 BOM 的 UTF-8 寫入 draft**，使用檔案建立工具——或在修正時使用檔案編輯工具。
  絕不透過 shell 字串輸出它：文字中的反引號或 `$` 會在毫無提示的情況下被改寫。
- **只在使用者答應時 commit，而且只 commit draft。**
  沒有詢問就做的 commit，會把使用者尚未完成的編輯放進歷史，而別人暫存的檔案也不屬於這個 commit。
  Step 7 什麼都不 commit：取代與記錄涉及的檔案，由使用者在各個 workspace 中 commit。
- **skill 結束前，顯示 draft 的路徑、Step 6 產生 review page 之後它在 review server 上的連結——沒有 review server 執行時改為它的路徑——以及 YAML checkpoint 的路徑**——Step 7 之後改為顯示 source file 的路徑，取代 draft 的——只顯示路徑，絕不顯示內容，並呈現為可點擊的 Markdown 連結，絕不用 inline code 或純文字。
  YAML checkpoint 以相對於 workspace、使用正斜線的目標連結，例如 `[process.yaml](checkpoints/asd-ste/references-DFD/process.yaml)`。
  每一次執行都要這樣做，包括 `run step 0` 這類只執行一部分的執行。

# Prompt Examples


## Prompt 1

```
/asd-ste
.github/common/references/DFD.md
```

## Prompt 2

```
/asd-ste
DFD.md
```

## Prompt 3

```
/asd-ste
DFD
```

## Prompt 4

```
/asd-ste
DFD
run step 3
```

## Prompt 5

```
把 .github/common/references/DFD.md 用 ASD-STE100 的風格重寫成草稿，給我審核
```

## Prompt 6

```
/asd-ste
DFD
run step 6
```

## Prompt 7

```
/asd-ste
DFD
run step 7
```


# Workflow

## Step 0 - Warmup

- workspace 有 `.venv` 時先執行它——Dependency Checker 與 step saver 會 import `PyYAML`；`check_ste.py` 與 draft tool 只需要 Python 標準函式庫。

- 讀取 workspace 根目錄的 workspace config [config.yaml](config.yaml)（如果有的話），並解析：
  - **`skillGroups`**：群組名稱 -> skills 根目錄的對應——本 skill 自己的目錄是 `{skillGroups.common}\skills\asd-ste\`。
  - 沒有 `config.yaml`，或其中沒有 `skillGroups` 時，把 `{skillGroups.common}` 當成本 skill 自己目錄往上兩層的目錄——也就是含有 `skills\` 的那一層——並且只在 workspace 資料夾中尋找 source file。
  - 在下方各 step 中（包含指令內）凡出現 `{skillGroups.common}` 之處，都代換為解析後的值。

- 執行 workflow 之前，先確認下列腳本與檔案存在。
  - `{skillGroups.common}\skills\asd-ste\scripts\check_ste.py`
  - `{skillGroups.common}\skills\asd-ste\scripts\draft.py`
  - `{skillGroups.common}\skills\asd-ste\scripts\save_step.py`
  - `{skillGroups.common}\skills\asd-ste\scripts\make_review.py`
  - `{skillGroups.common}\skills\asd-ste\scripts\review_server.js`
  - `{skillGroups.common}\skills\asd-ste\references\ste-rules.md`
  - `{skillGroups.common}\skills\asd-ste\references\ste-dictionary.json`——缺少時就停止，並說明 `convert_spec.py` 能從 STE specification 重新建出它（`python {skillGroups.common}/skills/asd-ste/scripts/convert_spec.py --pdf <ASD-STE100_ISSUE9.pdf> --json <ste-dictionary.json>`，需先安裝 `pypdf` 與 `cryptography`）。
    不要在本次執行中建置它。
  - `{skillGroups.common}\skills\asd-ste\references\ste-custom.md`
  - `{skillGroups.common}\references\us-spelling.json`
  - `{skillGroups.common}\scripts\depends_on.py`

- prompt 採用上方 **Prompt Examples** 所示的其中一種形式。
  從中解析：
  - **source file**（必填）：一個 `.md` 檔的路徑，相對於 workspace 或絕對路徑皆可，如 Prompt 1；一個檔名，如 Prompt 2；或一個不含 `.md` 的名稱，如 Prompt 3，代表該名稱加上 `.md`。
  - **`run step N`**（選填）：放在結尾的 step 選擇子。

- 解析 source file：
  - 一個存在的路徑——絕對路徑，或相對於某個 workspace 資料夾——就是 source file。
  - 否則，在每一個 workspace 資料夾與每一個 `skillGroups` 根目錄底下，尋找名稱完全相同的檔案：`rg --files --hidden -g '<name>' -g '!.git' <folder>`。
    之所以需要 `--hidden`，是因為 `.github` 是隱藏目錄，而 `rg` 仍會略過 `.gitignore` 排除的檔案。
  - 只有一個符合時，它就是 source file。
    一個都沒有時，請使用者輸入路徑，並等待回答。
    有好幾個時，列出它們並詢問是哪一個——絕不挑第一個。

- 在 workspace 根目錄對 source file 執行 draft tool：`python {skillGroups.common}/skills/asd-ste/scripts/draft.py paths "<source file>"`。
  它以 JSON 印出 source file 的 TW twin、它的 draft、draft 的 TW twin 與 Checkpoint Dir，每個檔案是否存在，以及 source file 是不是 TW twin（`twin`）或 STE file（`ste`）。
  無法讀取 source file 時，它以 `2` 結束。

- 從 draft tool 取得 Checkpoint Dir，不存在時就建立它。
  找不到的 source file 無法命名 Checkpoint Dir，它那次執行也不會留下 YAML checkpoint。

- 當 source file 有下列情形時，停止並說明哪一項檢查失敗，而不是改寫它：
  - 不是以 `.md` 結尾——本 skill 只改寫 Markdown；
  - 是 TW twin——`twin` 為 true，該改寫的是它的英文檔；
  - 是 STE file——`ste` 為 true：它是 draft，或已被 draft 取代的 source file；
  - 開頭的 frontmatter 無法解析——draft 的 frontmatter 將無法與它比對。

  skill 停止之前，依本 step 最後一項所述存下 Step 0 的群組，加上 `--stopped` 與失敗的那一項檢查。

- 說明 draft 是否已經存在；要不要覆寫它，由 Step 2 詢問。

- 保存標準形式的 skill 呼叫，供後面的 step 參考。

- 顯示解析出的 source file 路徑與 draft 路徑。

- 以 step saver 在 `step_0` 底下存 YAML checkpoint，並以 `--new` 讓它重新開始：`skill`、`model`、`prompt`（標準形式的 skill 呼叫）、`source_file`、`source_twin`、`draft`、`draft_exists`、`draft_twin` 與 `checkpoint_dir`，每一項都照 draft tool 印出的值。
  - 範例：`python {skillGroups.common}/skills/asd-ste/scripts/save_step.py --checkpoint "checkpoints/asd-ste/references-DFD/process.yaml" --step 0 --title "Warmup" --begin "<begin>" --new --set skill=asd-ste --set model="<model>" --set prompt="<canonical invocation>" --set source_file=".github/common/references/DFD.md" --set source_twin=".github/common/references/DFD-tw.md" --set draft="<draft>" --json draft_exists=true --set draft_twin="<draft's TW twin>" --set checkpoint_dir="checkpoints/asd-ste/references-DFD"`


## Step 1 - Inventory the Source

- 以 `--src`、`--dict`、`--custom`、`--spelling`、`--report` 與 `--findings` 參數執行腳本 `check_ste.py`。
  - `--src`：Step 0 解析出的 source file。
  - `--dict`：**STE dictionary**。
  - `--custom`：**project-approved words**。
  - `--spelling`：**US spelling list**。
  - `--report`：Checkpoint Dir 中的 `step_1-inventory.txt`。
  - `--findings`：Checkpoint Dir 中的 `step_1-findings.json`，即本 step 的 **findings file**。
  - 範例：`python {skillGroups.common}/skills/asd-ste/scripts/check_ste.py --src ".github/common/references/DFD.md" --dict "{skillGroups.common}/skills/asd-ste/references/ste-dictionary.json" --custom "{skillGroups.common}/skills/asd-ste/references/ste-custom.md" --spelling "{skillGroups.common}/references/us-spelling.json" --report "checkpoints/asd-ste/references-DFD/step_1-inventory.txt" --findings "checkpoints/asd-ste/references-DFD/step_1-findings.json"`

- 腳本把清冊印到 **stdout**，同時也寫進這兩個檔案：
  1. frontmatter 的鍵，或說明沒有 frontmatter。
  2. 每一行標題，依序附上行號。
  3. 各個 fenced block，附上它們所在的行。
  4. 每一個 inline-code span、連結目標與 placeholder，各列一次。
     已停用寫法的 placeholder 不是 kept span：一則 `[WARN]` 會列出它，並附上轉換它的指令。
  5. 每個表格的欄數。
  6. source file 自己的 header quote，逐行列出。
  7. STE 的問題，各標為 `[TODO]`：超過上限的句子、含有不只一句的行、超過六句的段落、分號與縮約形、每一個非核准詞及其替換詞、字典沒有收錄的每一個詞、看起來是被動語態的句子、每一個雙重否定、每一個拉丁縮寫、每一個後面沒接 *that* 的 *make sure*，以及每一個英式拼法與它的美式拼法。
     project-approved word 不算問題：一行 `[INFO]` 列出散文用到的每一個。
     kept span 裡的英式拼法自成一個 `[TODO]`，要先改 source file：draft 原樣照抄那個 span。
     標題裡字典列為不核准、而且在任何詞性都不核准的每一個詞，也自成一個要判斷的 `[TODO]`。
  8. 散文中 CJK 字元所佔的比例，以及 **verdict**：`rewritable`、kept span 裡有英式拼法時的 `SOURCE-FIRST`，或 `NOT-ENGLISH`。

- **如果腳本以 `2` 結束、verdict 為 `NOT-ENGLISH`，就在這裡停止本 skill。**
  回報它印出的比例，說明 STE 是用英文寫的，並且不要寫出 draft。
  先依本 step 最後一項所述存下 Step 1 的群組，加上 `--stopped` 與比例。

- **如果腳本以 `3` 結束，verdict 為 `SOURCE-FIRST`，就在這裡停止本 skill。**
  draft 原樣照抄每一個 kept span，所以要先改 source file：回報 kept span 裡的每一個英式拼法，附上它的美式拼法與行號，並說明 source file 改好之後再重新執行。
  先依本 step 最後一項所述存下 Step 1 的群組，加上 `--stopped` 與那些拼法。

- 依清冊詢問的每一個標題詞所在的標題，判斷它：
  - 用在字典不核准的詞性或意思上——例如以 *kind* 表示 type，或把 *create* 當動詞——這個標題就違反 STE，只有 source file 能改。
    比照 `SOURCE-FIRST` 停止本 skill，指出每一個標題，以及它必須換掉的詞。
  - 用作 source file 主題的技術名詞或技術動詞（STE rules 1.5 與 1.12），例如把 *file* 當名詞，這個詞就保留，由 Step 2 把它列為 technical word。

- 以 `0` 結束代表 `rewritable`；每一個標題詞都判斷為保留之後，執行繼續。

- 顯示清冊的簡短摘要：標題、fence、連結與表格的數量，有多少句子超過上限，散文用了多少個非核准詞、字典外的詞與英式拼法，kept span 裡的每一個英式拼法，以及每一個標題詞與判斷的結果。

- 以 step saver 在 `step_1` 底下存 YAML checkpoint：以 `--data` 放入整份 findings file；`report_file` 與 `findings_file` 這兩個檔名；以及 `heading_words`，每一個判斷過的標題詞，附上它的行號與是否保留，以 JSON 清單傳入。
  - 範例：`python {skillGroups.common}/skills/asd-ste/scripts/save_step.py --checkpoint "checkpoints/asd-ste/references-DFD/process.yaml" --step 1 --title "Inventory the Source" --begin "<begin>" --data "checkpoints/asd-ste/references-DFD/step_1-findings.json" --set report_file=step_1-inventory.txt --set findings_file=step_1-findings.json --json heading_words='[]'`


## Step 2 - Rewrite in STE

- **這個 step 沒有腳本**——用更少、更簡單的字把同一件事說出來而不遺漏任何一點，是沒有任何程式做得到的閱讀與寫作，所以請自己依照下面的指示進行。

- 如果 draft 已經存在，說明這一點，並詢問使用者是否以完整的改寫覆寫它。
  回答 no 時，本次執行結束，不寫出 draft，並依本 step 最後一項所述存下 Step 2 的群組，加上 `--stopped`。

- 完整閱讀 **STE rules digest**、完整閱讀 source file，以及 Step 1 的清冊——在 `run step 2` 底下，就是 YAML checkpoint 的 `step_1` 群組，以及旁邊的 `step_1-inventory.txt`。

- 適用於下方每一項指示的規則：
  - **逐位元組照抄每一個 kept span**，以清冊所列為準。
  - **保留每一項陳述。**
    不丟掉、不合併掉、也不新增任何規則、條件、數字、例子或理由。
    一個長句變成好幾個句子或一份直式清單，絕不變成一個較短的主張。
  - **依 STE rules digest 與 project rules 寫作**：使用核准詞——STE dictionary 的詞與 project-approved words——的核准詞性、意義與詞形；只在 rule 1.5 或 1.12 允許時使用 technical word；指示句最多 20 個字，描述句最多 25 個字；使用主動語態；每個句子、每個段落各只有一個主題；一個段落最多六句；不用分號，也不用縮約形。
  - **處理清冊印出的每一個 `[TODO]`**：把每個非核准詞換成它的替換詞，或重新造句；把每個字典外的詞換掉，或在它確實是 technical word 時保留它；把每個英式拼法寫成它的美式拼法，或把 md-style.md 允許保留的名稱當成 technical word 保留。
  - **每行只放一個句子**，如 [md-style.md](.github/common/rules/md-style.md) 所要求。
  - **一件東西只用一個名稱。**
    source file 用來指稱某一項目的 term，在 draft 的每一個句子裡都是同一個 term。
  - 如果某項陳述無法在不改變其主張的情況下用 STE 說出，就保留它的 technical word 或它在來源中的措辭，而不要把主張轉述掉，並在本 step 結尾的顯示中列出它。

- 建構 draft：
  1. **Frontmatter**——只在 source file 有 frontmatter 時：每一個鍵與每一個值都不變，只有 `description` 以 STE 改寫，並維持相同的 scalar 樣式。
  2. **標題**——source file 的標題行，原樣不變，條件是它在 frontmatter 底下的第一行是標題。
  3. **Header quote**——source file 自己的 header quote 行，原樣不變，接著是後面什麼都不加的 `> [[ASD-STE100_ISSUE9.pdf]]`，再接著後面什麼都不加的 `> [[ste-custom]]`，散文沒用到 project-approved word 時也一樣：日期與指紋由 Dependency Checker 寫入。
  4. **Header note**——一個空行，接著是 digest 的 House Rules 給出的三行引用區塊：以檔名連到 source file 的連結、兩者不一致時以 source file 為準的陳述，以及 `Technical words:` 後面依字母順序接著 draft 用到的每一個 technical word。
  5. **內文**——source file 的標題與 fenced block 留在原位，其間是改寫後的散文，並遵守 digest 的 House Rules 中關於表格、強調、引文，以及 source file 自我指稱的規定。

- 以不含 BOM 的 UTF-8，使用檔案建立工具，把 draft 寫到 Step 0 時 draft tool 給出的路徑。

- 顯示 draft 的路徑、technical word 的數量，以及每一項保留來源措辭的陳述與原因。

- 以 step saver 在 `step_2` 底下存 YAML checkpoint：`overwrite`，是否覆寫了已存在的 draft；`technical_words`，header note 列出的清單；以及 `kept_wording`，每一項保留來源措辭的陳述，附上它在 draft 中的行號、內容與原因——清單以 `--json` 傳入。
  - 範例：`python {skillGroups.common}/skills/asd-ste/scripts/save_step.py --checkpoint "checkpoints/asd-ste/references-DFD/process.yaml" --step 2 --title "Rewrite in STE" --begin "<begin>" --json overwrite=true --json technical_words='["caller", "stage"]' --json kept_wording='[]'`


## Step 3 - STE Check

- 以 `--src`、`--ste`、`--dict`、`--custom`、`--spelling`、`--report` 與 `--findings` 參數執行腳本 `check_ste.py`。
  - `--src`：Step 0 解析出的 source file。
  - `--ste`：draft。
  - `--dict`：**STE dictionary**。
  - `--custom`：**project-approved words**。
  - `--spelling`：**US spelling list**。
  - `--report`：Checkpoint Dir 中的 `step_3-check.txt`。
  - `--findings`：Checkpoint Dir 中的 `step_3-findings.json`，即本 step 的 **findings file**。
  - 範例：`python {skillGroups.common}/skills/asd-ste/scripts/check_ste.py --src ".github/common/references/DFD.md" --ste "<draft>" --dict "{skillGroups.common}/skills/asd-ste/references/ste-dictionary.json" --custom "{skillGroups.common}/skills/asd-ste/references/ste-custom.md" --spelling "{skillGroups.common}/references/us-spelling.json" --report "checkpoints/asd-ste/references-DFD/step_3-check.txt" --findings "checkpoints/asd-ste/references-DFD/step_3-findings.json"`

- 腳本對每一項檢查在 **stdout** 印出一行，同時也寫進這兩個檔案，只要有任何一項失敗就以 `1` 結束：
  1. draft 是不含 BOM 的 UTF-8。
  2. frontmatter 的鍵相同，`description` 以外的每一個值都沒變——或兩份檔案都沒有 frontmatter。
  3. 標題行完全相同，順序也相同。
  4. fenced block 逐位元組相同，順序也相同。
  5. source file 的每一個 inline-code span、placeholder 與連結目標都還在。
     source file 沒有的連結目標，除了 header note 與 header quote 的之外，都是 `[WARN]`。
     兩份檔案都沒有已停用寫法的 placeholder。
  6. 表格的欄數相同。
  7. header quote 保留了 source file 自己的行，並宣告 `[[ASD-STE100_ISSUE9.pdf]]`。
     記錄的指紋若不是建置 STE dictionary 所用的那一個，就是 `[WARN]`。
     它也要宣告 `[[ste-custom]]`，散文沒用到 project-approved word 時也一樣，因為 draft 要遵守 **project rules**。
  8. header note 連到 source file。
     沒有 `Technical words:` 行的 header note 是 `[WARN]`。
  9. 每個句子都在上限之內，每行只有一個句子，每個段落最多六句，散文中沒有分號，也沒有縮約形。
  10. 沒有任何 kept span 含有 US spelling list 上、而 header note 沒有列為 technical word 的英式拼法。
      draft 是從 source file 照抄 kept span 的，所以要先改 source file。

- 它也會為下列每一項印出一行 `[WARN]`：每一個非核准詞，附上它的替換詞；STE dictionary 沒有收錄的每一個詞；散文中的每一個英式拼法，附上它的美式拼法；看起來是被動語態的每一個句子；每一個雙重否定，一條 **project rule** 禁止這種寫法；每一個拉丁縮寫（GR-6），附上應該改寫成的英文；每一個後面沒接 *that* 的 *make sure*（GR-1）；以及列出了卻從未使用的每一個 technical word。
  header note 列為 technical word 的詞不會被回報，它的複數形與動詞形也不會。
  project-approved word 也不會被回報：一行 `[INFO]` 列出散文用到的每一個。

- 如果腳本以 `1` 結束，就針對每一個 `[FAIL]` 修正 draft，並再次執行本 step 的指令，直到它以 `0` 結束。
  **修正 draft，絕不修正 source file。**

- 閱讀每一個 `[WARN]`，在它說得對的地方修正 draft，然後再執行一次指令：
  - 把非核准詞換成它的替換詞，或重新造句；
  - 字典外的詞只有在它是 technical word 時才保留，而且要加進 `Technical words:` 行；
  - 英式拼法改成它的美式拼法；若它是 md-style.md 允許保留的名稱，就加進 `Technical words:` 行；
  - 把拉丁縮寫換成警告給出的英文，並在 *make sure* 後面補上 *that*；
  - 把雙重否定改寫成肯定句，除非這兩個否定詞並不表示肯定的意思；
  - 把被動句改成主動句，除非沒有人知道是誰或什麼做了這個動作。

- 如果某個 `[FAIL]` 是 source file 本身的缺陷——一個沒有關閉的 fence、一列欄數錯誤的表格、一個已停用寫法的 placeholder、kept span 裡的英式拼法——就直接說明，不去動 source file，並回報為需要使用者修正的事項。
  檢查無法通過，所以依本 step 最後一項所述存下 Step 3 的群組，加上 `--stopped` 與那個缺陷。

- 腳本以 `0` 結束後，在 header quote 中記錄 STE specification：
  - 執行 `python {skillGroups.common}/scripts/depends_on.py record "<draft>" --target "[[ASD-STE100_ISSUE9.pdf]]"`，並在 workspace 有這個設定檔時加上 `--config config.yaml`。
  - 再以 `--target "[[ste-custom]]"` 執行同一個指令。
  - `--target` 讓 source file 自己的依賴行維持 source file 當初記錄的樣子：draft 只為它剛剛比對過的規格，以及 project-approved words 與 project rules 背書。
  - 如果它因為在 draft 的 vault 或某個 `skillGroups` 根目錄底下找不到名為 `ASD-STE100_ISSUE9.pdf` 的檔案而以 `2` 結束，就說明這一點，並讓那一行維持沒有 record 的狀態。

- 顯示檢查結果：每一項檢查的通過或失敗，以及每一個留下的警告與它留下的原因。

- 以 step saver 在 `step_3` 底下存 YAML checkpoint：以 `--data` 放入最後一次檢查的整份 findings file；`report_file` 與 `findings_file` 這兩個檔名；`check_runs`，檢查執行的次數；`warnings_left`，每一個留下的警告與它留下的原因；以及 `fingerprint`，Dependency Checker 記錄的日期與指紋，或是 `fingerprint_not_recorded` 加上原因；還有 `custom_fingerprint`，同樣記下 ste-custom.md 的日期與指紋。
  - 範例：`python {skillGroups.common}/skills/asd-ste/scripts/save_step.py --checkpoint "checkpoints/asd-ste/references-DFD/process.yaml" --step 3 --title "STE Check" --begin "<begin>" --data "checkpoints/asd-ste/references-DFD/step_3-findings.json" --set report_file=step_3-check.txt --set findings_file=step_3-findings.json --json check_runs=2 --json warnings_left='[]' --json fingerprint='{"date": "2026-10-11", "fingerprint": "d1f4ea9e7cd6"}' --json custom_fingerprint='{"date": "2026-10-11", "fingerprint": "<fingerprint>"}'`


## Step 4 - Offer to Commit

- 只有在有東西可 commit、而且 draft 沒有問題時，才提議 commit。
  在下列情形略過本 step，並說明原因：
  - draft 不在 git repository 中；
  - git 顯示它沒有任何改動；
  - 它沒有通過 STE check——看 YAML checkpoint 中 `step_3` 群組的 `verdict`。

- 詢問使用者是否要 commit draft，並顯示它的分支、commit 主旨，以及其他已經暫存、但這個 commit 不會包含的東西。
  - 主旨依循 repository 最近的主旨，以 `git log -5 --format=%s` 讀取：如果它們以被改動的文件命名，主旨就以 draft 的檔名命名。

- 回答 yes 時：
  - draft 是 git 的新檔案時先 `git add`，再以 `git commit -m "<subject>" -- <draft>` 只 commit 它，讓其他已暫存的東西維持暫存、不進入這個 commit。
  - 絕不 `git commit -a`，絕不 push、amend、建立或切換分支，也絕不略過 repository 的 hook。
    拒絕 commit 的 hook 連同它的輸出一起回報，本 step 就停在那裡。

- 回答 no 時，什麼都不 commit。

- 顯示 commit 的 hash 與主旨，或說明沒有 commit 任何東西。

- 以 step saver 在 `step_4` 底下存 YAML checkpoint：略過本 step 時，存 `skipped` 與原因；否則存 `answer`，yes 或 no，以及有 commit 時的 `commit`，即它的 hash 與主旨。
  - 範例：`python {skillGroups.common}/skills/asd-ste/scripts/save_step.py --checkpoint "checkpoints/asd-ste/references-DFD/process.yaml" --step 4 --title "Offer to Commit" --begin "<begin>" --set answer=yes --json commit='{"hash": "5c98468", "subject": "<subject>"}'`


## Step 5 - Offer the TW Twin

- 當 draft 沒有通過 STE check 時，略過本 step 並說明原因——看 YAML checkpoint 中 `step_3` 群組的 `verdict`。

- 詢問使用者是否要請 `chinese` skill 寫出 draft 的 TW twin，位於 Step 0 時 draft tool 給出的路徑。

- 回答 yes 時，以 draft 的路徑對 draft 執行 `chinese` skill——例如 `/chinese <draft>`。
  它會翻譯 draft，保留它的 header quote 與每一個 kept-English span，最後執行它自己的 parity check，並提議它自己的 twin commit。
  - 不要在這裡翻譯檔案，也不要在 `chinese` skill 執行期間編輯 draft——它把來源檔視為唯讀。

- 回答 no 時，說明沒有寫出任何 twin。

- 以 step saver 在 `step_5` 底下存 YAML checkpoint：略過本 step 時，存 `skipped` 與原因；否則存 `answer`，yes 或 no，以及寫出 TW twin 時的 `twin_file`，即它的路徑。
  - 範例：`python {skillGroups.common}/skills/asd-ste/scripts/save_step.py --checkpoint "checkpoints/asd-ste/references-DFD/process.yaml" --step 5 --title "Offer the TW Twin" --begin "<begin>" --set answer=no`


## Step 6 - Build the Review Page

- 當 draft 沒有通過 STE check 時，略過本 step 並說明原因——看 YAML checkpoint 中 `step_3` 群組的 `verdict`。

- 比對 `step_3` 群組的 `custom_fingerprint` 與 ste-custom.md 現在的指紋：`python {skillGroups.common}/scripts/depends_on.py hash "{skillGroups.common}/skills/asd-ste/references/ste-custom.md"`。
  兩者不同、或群組中沒有它時，表示 **project-approved words** 或 **project rules** 在上次 STE check 之後改過：先重跑 Step 3，再繼續本 step。

- 找出 CONFIGURATION 所指名的兩份 **TW twin**。
  缺少其中一份時就停止，並說明缺的是哪一份、由誰寫出：draft 的由 Step 5 寫出，在 `run step 5` 底下也一樣；source file 的由 `chinese` skill 寫出。
  先依本 step 最後一項所述存下 Step 6 的群組，加上 `--stopped` 與缺少的那一份 TW twin。

- 完整閱讀 source file、draft 與兩份 TW twin，以及 YAML checkpoint 的 `step_2` 與 `step_3` 群組。
  上一次 Step 0 之後沒有執行 Step 2 時，`step_2` 就不存在；這時 review page 不列出保留原文措辭的陳述，並說明原因。

- 以繁體中文，使用檔案建立工具，把 **review notes** 寫到 Checkpoint Dir 中的 `step_6-notes.html`：
  - 一段 HTML 片段，分成兩部分，各是一個 `<h3>` 標題，後面接一份 `<ol>` 清單：先是 draft 要看的地方，再是它的 TW twin 要看的地方。
  - 每一項指出一處要對照的地方，以及審核者為什麼該看它。
    這樣的地方包括：主張可能在改寫中跑掉的句子，並與來源的句子並列；一件東西有兩個名稱，或兩件東西共用一個名稱；draft 的 TW twin 譯得和 source file 的 TW twin 不同的 term；形狀改變了的清單或段落；以及 header quote 與 header note。
  - 每一行都以 **line reference** 標示，絕不寫成單純的數字，讓 review builder 能為它加上連結；在 review notes 中，`{{` 與 `}}` 不作其他用途。
  - 不要再列一次 review builder 自己會列出的項目——STE check 的結果、留下的警告、technical word 與保留原文措辭的陳述——但其中某一項引起需要審核者判斷的問題時，就指名它。

- 以 `--src`、`--ste`、`--src-tw`、`--ste-tw`、`--checkpoint`、`--notes`、`--out` 與 `--status` 參數執行 review builder。
  - `--src` 與 `--ste`：source file 與 draft。
  - `--src-tw` 與 `--ste-tw`：它們的 TW twin。
  - `--checkpoint`：YAML checkpoint。
  - `--notes`：Checkpoint Dir 中的 `step_6-notes.html`，即 review notes。
  - `--out`：Checkpoint Dir 中的 `step_6-review.html`，即 **review page**。
  - `--status`：Checkpoint Dir 中的 `step_6-status.json`，review page 一開始顯示的 review status；審核者設定第一個之前，它不存在。
  - 範例：`python {skillGroups.common}/skills/asd-ste/scripts/make_review.py --src ".github/common/references/DFD.md" --ste "<draft>" --src-tw ".github/common/references/DFD-tw.md" --ste-tw "<draft's TW twin>" --checkpoint "checkpoints/asd-ste/references-DFD/process.yaml" --notes "checkpoints/asd-ste/references-DFD/step_6-notes.html" --out "checkpoints/asd-ste/references-DFD/step_6-review.html" --status "checkpoints/asd-ste/references-DFD/step_6-status.json"`

- review builder 把 review page 的路徑、節數與行數、review notes 含有多少個 line reference，以及每一種 review status 各有幾項印到 **stdout**，寫出頁面後以 `0` 結束。
  當某個 line reference 指不到它那份檔案的任何一行時，它以 `1` 結束、不寫出頁面，並為每一個印出一行 `[FAIL]`：修正 review notes，絕不修正那四份檔案，然後再執行一次指令，直到它以 `0` 結束。
  檔案無法讀取，或 YAML checkpoint 沒有 `step_3` 群組時，它以 `2` 結束。

- 從 workspace 根目錄確認 **review server** 正在執行。
  它需要 Node.js：`node --version` 失敗時，說明這一點，並改為給出 review page 的路徑，而不是它的連結。
  - 詢問是否有一個在回應：`node {skillGroups.common}/skills/asd-ste/scripts/review_server.js --probe`。
  - 以 `0` 結束：有 review server 在回應，它已經在提供 review page。
  - 以 `1` 結束：沒有任何回應，所以在背景啟動一個，讓它在執行結束後繼續提供頁面，然後再詢問一次。
    在 macOS 與 Linux 上執行 `nohup node {skillGroups.common}/skills/asd-ste/scripts/review_server.js --root checkpoints/asd-ste > /dev/null 2>&1 &`；在 PowerShell 中執行 `Start-Process node -ArgumentList '{skillGroups.common}/skills/asd-ste/scripts/review_server.js','--root','checkpoints/asd-ste' -WindowStyle Hidden`。
  - 以 `2` 結束：別的程式占用了 port 8790；說明這一點，並改為給出 review page 的路徑，而不是它的連結。

- 以可點擊的 Markdown 連結顯示 review page 的連結 `http://127.0.0.1:8790/{parent}-{name}/`——沒有 review server 執行時改為它的路徑——以及 review notes 的項目數。
  agent 有瀏覽器面板時，也在那裡打開這個連結。

- 以 step saver 在 `step_6` 底下存 YAML checkpoint：`notes_file` 與 `review_file` 這兩個檔名；`notes`，review notes 的項目數；`line_references`，review builder 印出的數目；以及 `review_url`，review page 的連結，或是 `review_server` 加上沒有 review server 執行的原因。
  - 範例：`python {skillGroups.common}/skills/asd-ste/scripts/save_step.py --checkpoint "checkpoints/asd-ste/references-DFD/process.yaml" --step 6 --title "Build the Review Page" --begin "<begin>" --set notes_file=step_6-notes.html --set review_file=step_6-review.html --json notes=12 --json line_references=42 --set review_url=http://127.0.0.1:8790/references-DFD/`

- 最後以可點擊的 Markdown 連結列出 draft 的路徑、存在的 TW twin 路徑、本 step 產生 review page 時它的連結——或它的路徑——以及 YAML checkpoint 的路徑。


## Step 7 - Replace the Source

- 當 draft 沒有通過 STE check 時——看 YAML checkpoint 中 `step_3` 群組的 `verdict`——或沒有產生 review page 時——`step_6` 群組中沒有 `review_file`——略過本 step 並說明原因。

- 照 Step 6 的方式比對兩個指紋：兩者不同時，先重跑 Step 3 與 Step 6，再詢問。

- 詢問使用者 draft 是否通過了審核，並指出 draft、它的 TW twin 與 review page。
  - 只有明確的通過，才會取代 source file。
  - 使用者要求的修改，改在 draft 上，或經由 `chinese` skill 改在它的 TW twin 上；接著重跑 Step 3 與 Step 6，本 step 再問一次。
  - 其他任何回答，都讓每一份檔案維持原樣。

- 通過時，在 workspace 根目錄執行 draft tool：`python {skillGroups.common}/skills/asd-ste/scripts/draft.py replace "<source file>"`。
  它把 draft 寫到 source file 上，把 draft 的 TW twin 寫到 source file 的 TW twin 上，header note 依 digest 的 House Rule 5 刪成兩行，TW twin 的 pairing line 改為連回 source file；header quote 維持原樣。
  接著它刪除 draft 與它的 TW twin，並印出它做了什麼。
  當 source file 有 TW twin、而 draft 的 TW twin 不存在，某個 header note 不符合 House Rule 5 給出的形式，或 draft 的 TW twin 有 frontmatter、卻沒有連到 draft 的 pairing line 時，它以 `1` 結束，什麼都不寫：說明是哪一種，並停止。

- 找出 dependent：執行 `python {skillGroups.common}/skills/asd-ste/scripts/draft.py dependents "<source file>" --root <folder>`，每一個 workspace 資料夾與每一個 `skillGroups` 根目錄各給一個 `--root`。
  詢問使用者還有哪些 workspace 使用本 workspace 的 skill group——例如 `config.yaml` 在 `skillGroups` 中指名它的 workspace——並把每一個的資料夾再加一個 `--root`。

- 對每一個 dependent，閱讀 source file 改了什麼——它的 `git diff`——以及這個 dependent 引用它的每一處。
  - dependent 仍然成立時，重新記錄 source file：`python {skillGroups.common}/scripts/depends_on.py record "<dependent>" --target "<link>"`，並在 dependent 所在的 workspace 有這個設定檔時加上 `--config config.yaml`。
  - 它不再成立時，不要記錄：指出它，以及這次修改讓它哪裡不成立，交給使用者修正。

- 檢查結果，每次修正之後重跑該項檢查，直到它通過：
  - `check_ste.py`，`--ste` 設為 source file，`--dict`、`--custom` 與 `--spelling` 同 Step 3：沒有 `[FAIL]`。
  - 對 source file 與它的 TW twin 做 **parity check**：沒有 failure。
  - 對每一個重新記錄的 dependent 執行 `depends_on.py check`：source file 為 `UNCHANGED`。

- 顯示已取代的 source file 與它的 TW twin、刪除的檔案、每一個 dependent 是否重新記錄或為什麼沒有，以及每一項檢查的結果。
  說明什麼都沒有 commit：由使用者在各個 workspace 中 commit 這些修改。

- 以 step saver 在 `step_7` 底下存 YAML checkpoint：略過本 step 時，`skipped` 與原因；否則 `answer`，使用者的回答；取代之後再加上 `replaced`，draft tool 印出的那幾行；`dependents`，每一個 dependent 與它的連結、是否重新記錄；以及 `checks`，每一項檢查與它的結果。
  - 範例：`python {skillGroups.common}/skills/asd-ste/scripts/save_step.py --checkpoint "checkpoints/asd-ste/references-DFD/process.yaml" --step 7 --title "Replace the Source" --begin "<begin>" --set answer=pass --json replaced='[]' --json dependents='[]' --json checks='[]'`

- 最後以可點擊的 Markdown 連結列出 source file 的路徑、它的 TW twin 的路徑，以及 YAML checkpoint 的路徑。
