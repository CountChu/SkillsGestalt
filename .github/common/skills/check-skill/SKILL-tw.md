---
name: check-skill
description: >-
  檢查被指名之 skill 的 SKILL.md 與 README.md：比對 SKILL 與 README 兩份 template、在該 skill 目錄下的每一份文字檔上比對 workspace 的 `config.yaml` 慣例、檢查它的 description 是否與其 workflow 實際所做的相符、它的行文是否使用自己定義的 term、它的指令與腳本能否在 Windows、macOS 與 Linux 上執行，以及它的 README.md 中的 Dataflow 是否畫出各個 step 實際讀寫的東西。prompt 以編號選取這六項 check（`1` 指整項 check，`1.3` 指單一條判準），否則由 picker 詢問。它在對話中逐項 check 回報：先給 verdict，再把每個問題編號為 `<check>.<n>`，附上可以直接改的修正，或在需要使用者做選擇時，引述原文各行並列出以字母標示的選項。它不寫 MD report，也不寫 YAML checkpoint；它唯一保留的檔案是 Skills Dashboard（vault 中的 `dashboard\skills.md`），每個 skill 一列，帶著每一項 check 最新的 verdict。只有在使用者指名項目之後，它才會編輯 checked skill，並把每一處變更同步到該 skill 的繁體中文 twin，再把它標為需要重新檢查。
---

本文件為 [SKILL.md](.github/common/skills/check-skill/SKILL.md) 的繁體中文版。
任一份改了某節，另一份必須在同一次執行中一起改。

# TERMINOLOGY

在每個 skill 中意義都相同的 term。

- **Checkpoint Dir** — 存放某個 skill 之 YAML checkpoint 的每次執行目錄。
  每個會寫出 YAML checkpoint 的 skill 都有自己的。
- **YAML checkpoint** — Checkpoint Dir 內的 `process.yaml`。
  每個 step 都把輸出寫在其中的 `step_{N}` 群組下，讓後續 step 讀回而不必重算。
- **MD report** — skill 寫進 wiki vault 的 Markdown 報告，放在以該 skill 命名的資料夾中，於結果各節之上帶有標準表頭（Skill、Checkpoint、Created、Updated、Prompt）。

# DEDICATED TERMINOLOGY

本 skill 領域專屬的 term。

- **`{yymmdd-hh}`** — 執行戳記：執行開始的日期與小時，在 Step 0 讀取一次（例如 `260806-11`）。
  它命名 **facts file**，而它的日期（寫成 `yyyy-mm-dd`）就是每個 checked skill 在 **Skills Dashboard** 上那一列所記錄的日期，因此一次執行不會落在兩個戳記底下。
- **checked skill** — 本次執行所檢視的 skill。
  Step 0-5 對它只會讀取；Step 6 會編輯它，而且只針對使用者指名的那些 **items**。
- **skill directory** — checked skill 自己的資料夾：它的 `SKILL.md` 與 `README.md`、它們的繁體中文 twin、它的 `scripts\`、它的 `references\`，以及它自己的 `config.yaml`。
  掃描會讀**其中的每一份文字檔**，因為寫死在腳本裡的路徑，壞法與寫死在某個 step 裡的一模一樣。
- **check** — 六項可選檢視之一，在 **checking criteria** 中帶編號：`1` `Template alignment`、`2` `Config conformance`、`3` `Description accuracy`、`4` `Terminology usage`、`5` `Cross-platform compatibility`、`6` `Dataflow`。
  一次執行套用其任意組合，並可以 `<check>.<n>` 編號把某一項縮到單一條判準。
- **checking criteria** — 六項 check 所套用的判準：每一項 check 都遵循的規則，以及每一項各自的編號判準。
  **判準歸它所有**；執行它們的 workflow 歸本文件所有，因此新增或修改一條判準，改的是那份檔案，絕不是改某個 step。
- **facts file** — 掃描所寫出的暫存 YAML：每個 checked skill 一份 YAML 文件，只記事實、絕不記 verdict。
  它是每項 check 讀取的輸入，並在 **Skills Dashboard** 更新之後刪除。
- **fact group** — 某個 checked skill 之 facts-file 文件的一個頂層鍵：`template_shape`、`config_shape`、`dir_config_shape`、`leftovers`、`readme_shape`、`terminology`、`dataflow`。
- **region** — 某項事實被找到的 `SKILL.md` 區域：`frontmatter`、`prompt_examples` 或 `body`。
  只有 `body` 會被判定。
  來自 **skill directory** 其他位置的事實不帶 region——它改帶的是所在檔案與該檔案的類別，而 `readme_shape` 與 `dataflow` 事實屬於該 skill 的 `README.md`。
- **finding** — 一項釘在特定檔案與行號上的缺陷，並引述違規文字。
  無法釘到行號的缺陷不算 finding，也不可回報。
- **issue** — 違反契約的 finding：checked skill 沒有做到它的 template、它的 `config.yaml`、它自己的 description 或它自己的字彙表所承諾的事，或是超出了必須接受它的那個 skill loader 的限制。
- **recommendation** — 照現況能運作、但偏離參考基準的 finding。
  永不阻擋；作者可以拒絕。
- **verdict** — 某一項 check 對某一個 checked skill 的結果：✅ 沒有 finding、⚠️ 只有 recommendation、❌ 至少一項 issue、➖ 不適用（對沒有字彙表的 skill 所做的 check 4，以及對 `README.md` 中沒有 Dataflow 的 skill 所做的 check 6）。
- **item** — 報告中一個帶編號的條目 `<check>.<n>`，承載一項 finding 以及解決它的變更；它要不是 **direct fix**，就是 **decision item**。
  使用者以指名編號來套用 item，而一個編號只在印出它的那份報告中才有意義。
  它與判準編號形狀相同，但情境永遠不同：在 prompt 的 check 那一行上，`1.3` 是 check 1 的第 3 條判準；在回覆報告時，`1.3` 則是 check 1 的第 3 個 item。
- **direct fix** — 只有一個明顯變更的 item：先是它的 Problem，再是它的 Fix。
- **decision item** — 由使用者決定如何解決的 item：先是它的 Original 各行，再是它的 Problem，然後是以字母標示的各個選項。
- **option** — 解決某個 decision item 的一種以字母標示的方式，`(a)`、`(b)` 依此類推，套用時與其 item 一起指名（`1.3(a)`）。
- **checker defect** — `scan_skill.py` 或某項 check 自身指示中的誤報或盲點，而非 checked skill 的問題。
  不計入任何計數，也永遠不會是 item。
- **Skills Dashboard** — wiki vault 的 `dashboard\` 資料夾中那份不帶戳記的 `skills.md`：每個 skill group 一個 section，其中每個 checked skill 一列，每項 check 一格，格中是該 check 最新的 verdict 與計數，外加最後一次檢查它的日期（寫成 `yyyy-mm-dd`），以及它此後是否被編輯過。
  它是跨執行合併而成的現況檢視——絕不是歷史紀錄，也絕不由單次執行整份重寫。
- **needs check** — Step 6 在它編輯過的 skill 上所設的 dashboard 標記：那一列的各格描述的是該 skill 被編輯之前的樣子。
  只有完整地重新套用該列所持有之每一項 check 的執行，才會清除它。

# CONFIGURATION

本 skill 執行時所使用的具體值。

- **facts file** — `temp\check-skill-facts-{yymmdd-hh}.yaml`，位於 workspace 根目錄之下。
- **checking criteria** — [checking-criteria.md](.github/common/skills/check-skill/references/checking-criteria.md)，位於 `{skillGroups.common}\skills\check-skill\references\` 之下。
- **Skills Dashboard** — `{wikiDir}\dashboard\skills.md`，其中 `wikiDir` 來自 workspace 的 [config.yaml](config.yaml)（於 Step 0 解析）——絕不寫死 wiki 根目錄。

# MUST FOLLOW

- 必須逐步執行 workflow，並顯示每個 step 的編號。
- **本 skill 沒有 `run step N` 選擇子——每一次執行都是完整的一趟。**
  它所做的事沒有任何昂貴或不可逆到值得續跑，而選擇子本來要縮小的工作，已經由 prompt 上的 check 編號縮小了。
  絕不替它發明一個 step 選擇子。
  Step 6 也不是選擇子：只有當使用者以指名 item 來回覆報告時，它才會執行。
- **在使用者指名 item 之前只做檢查。**
  Step 0-5 絕不修改 checked skill——不編輯、不改名、不重新排版、不自動修正，連空白字元的更動都不行。
  Step 6 只為使用者以編號指名的那些 **items** 修改它，其餘一概不動，而且只在他們指名之後才動手。
  修正再明顯，也仍是一個交給使用者選擇的 item，絕不在沒被要求時自行套用。
- **本 skill 既不產出 MD report，也不產出 YAML checkpoint**，也沒有 Checkpoint Dir。
  它在對話中回報，而它唯一保留的檔案是 **Skills Dashboard**。
  **facts file** 是暫存檔，在 Step 5 結束時刪除。
  它開啟的其他每個檔案——每個 checked **skill directory** 中的每一份文字檔、SKILL 與 README 兩份 template、某份 `README.md` 在其 header quote 中宣告的檔案、`DFD.md`、`config.yaml`——都只讀不寫，唯一的例外是 Step 6 為被指名的 item 所編輯的檔案。
- **Skills Dashboard 只合併寫入，絕不由單次執行整份重寫。**
  其形狀歸 `update_dashboard.py` 所有：本次執行沒有檢查的 skill 保留原樣的那一列，本次執行沒有套用的 check 保留它那一格，並標上最後一次套用它的那次執行的日期。
  絕不手動編輯 dashboard——不是由腳本寫出的列，就是下一次執行讀不懂的列。
- 依照 [scratch-rules.md](.github/common/rules/scratch-rules.md) 決定 facts file 放在哪裡，以及如何清理。
- **在 skill 結束前，顯示 Skills Dashboard 的路徑**——只顯示路徑，絕不顯示其內容，並呈現為可點擊的 Markdown 連結，絕不用 inline code 或純文字。
  vault 位於本 workspace 之外，因此要用 `obsidian://open?vault={vaultName}&file=dashboard/skills.md` URI 連結它（例如 `[skills.md](obsidian://open?vault={vaultName}&file=dashboard/skills.md)`）。
  每次執行都要這麼做，包含因為沒有 skill 可解析或沒有選取任何 check 而提前停下的執行——並在那時說明 dashboard 沒有被更新。
- **報告所引用的每一個檔案與行號都必須是可點擊的連結。**
  報告是在對話中閱讀的，而 checked skill 通常位於本 workspace 之外，因此只有絕對路徑的目標才能指向它。
  - 格式：`[<file>:<n>](<absolute-path>:<n>)`——例如 `[SKILL.md:44](C:/Users/.../.github/dedi-boot-times/skills/report-boot-times-html/SKILL.md:44)`。
  - `<absolute-path>` 是該 finding 所在的檔案——checked skill 自己的 `SKILL.md`，或某項 check 2 finding 所指名的腳本、reference 或 config 檔——透過 `skillGroups` 解析，全程以**正斜線**書寫。
    一個反斜線就會悄悄讓連結失效。
    路徑中含有空白時，以 `<…>` 包住目標。
  - 適用於每一行 Problem 與 Original，以及行文中引用的每一行。
    範圍以 `<file>:<n>-<m>` 作為文字，而目標指向 `<n>`，因為目標只能定址單一行。
  - 絕不把行號寫成純文字或 inline code，也絕不用一個連結涵蓋兩個不連續的行——各自分別引用。

# Prompt Examples


## Prompt 1

```
/check-skill
report-boot-times-html
```

## Prompt 2

```
/check-skill
report-pipeline, triage-test-case
1, 2, 3, 4
```

## Prompt 3

```
/check-skill
report-pipeline
1.3, 4
```


# Workflow

## Step 0 - Warmup

- 先執行 `.venv`——掃描腳本會 import `PyYAML`。

- 讀取 workspace 根目錄的 workspace config [config.yaml](config.yaml) 並解析：
  - **`skillGroups`**：群組名稱 -> skills 根目錄的對應——每個可檢查的 skill 都位於 `{skillGroups[<group>]}\skills\<skill-name>\SKILL.md`，而本 skill 自己的目錄是 `{skillGroups.common}\skills\check-skill\`。
  - **`wikiDir`**：wiki 根目錄——**Skills Dashboard** 位於 `{wikiDir}\dashboard\` 之下。
    它同時也是 config-conformance check 用來比對的值，因此能分辨出正確解析 `wikiDir` 的 skill 與寫死 wiki 路徑的 skill。
  - **`vaultName`**：`wikiDir` 的最後一段路徑（例如 `MyVault`）——用來組出 dashboard 之 `obsidian://` 連結的 Obsidian vault 名稱。
  - 在下方各 step 中（包含指令內）凡出現 `{skillGroups.common}`、`{wikiDir}` 或 `{vaultName}` 之處，都代換為解析後的值。
  - 若 `config.yaml` 不存在或缺少所需的鍵，停止並詢問使用者。

- 本 skill 不呼叫任何 Azure DevOps API，也不需要 `ADO_PAT`——它只讀取本機檔案。
  絕不索取憑證。

- 執行 workflow 前先確認下列腳本／檔案是否存在。
  - `{skillGroups.common}\skills\check-skill\scripts\scan_skill.py`
  - `{skillGroups.common}\skills\check-skill\scripts\update_dashboard.py`
  - `{skillGroups.common}\skills\check-skill\references\checking-criteria.md`
  - `{skillGroups.common}\references\DFD.md`
  - `{skillGroups.common}\scripts\depends_on.py`

- 確認 SKILL template 與 README template 存在於 `{skillGroups.common}\templates\SKILL-tmp.md` 與 `{skillGroups.common}\templates\README-tmp.md`。
  它們是 alignment check 用來比對 skill 之 `SKILL.md` 與 `README.md` 的參考基準，因此若缺少任何一份就停止並告知使用者，而不是拿記憶中的形狀來比對。

- prompt 採用上方 **Prompt Examples** 所示形式之一。
  從中解析：
  - **Skill names**（必要）：一個或多個 skill 名稱，以逗號或空白分隔（例如 `report-pipeline, triage-test-case`）。
    逐一比對 `skillGroups` 根目錄解析；回報任何對不到 skill 的名稱並將其捨棄。
    本 skill 絕不提供 skill 清單供人挑選——一個裝著 workspace 內每個 skill 的清單，回答起來比直接打字還慢——因此當 prompt 未指名任何 skill 時，請要求使用者輸入 skill 名稱並等待回答。
  - **Check numbers**（選用）：skill 名稱之後的那一行，以逗號或空白分隔（例如 `1, 2, 3, 4`）。
    `1` 選取整項 check；`1.3` 只選取該 check 的第三條判準，其餘各條不列入本次執行。
    回報並捨棄超出 1-6 的編號，以及 **checking criteria** 未定義的判準編號。
    當這一行不存在時，保留選取未決——由 Step 1 向使用者詢問。

- 若缺少必要輸入，向使用者索取。

- 在此**只讀一次**時鐘，並在整次執行中沿用該 `{yymmdd-hh}` 戳記，讓同一次執行的 **facts file** 與 dashboard 各列不會因跨小時或跨午夜而落在兩個戳記底下。
  在同一小時內重跑會沿用同一個戳記，並覆寫該小時的 facts file；dashboard 只保留日期，因此同一天的每一次執行都記錄同一個日期。

- 顯示解析後的 `wikiDir`、解析出的 skill 名稱與 check 編號，以及 `{yymmdd-hh}` 戳記。


## Step 1 - Resolve Skills and Select Checks

- 取 Step 0 解析出的 skill 名稱，確認每個都能解析到某個 `skillGroups` 根目錄下的 `<root>\skills\<skill-name>\SKILL.md`，並記錄其群組與其**絕對** `SKILL.md` 路徑——報告中的每一條行號連結，以及該 skill 在 **Skills Dashboard** 上的那一列，都由它組成。
  捨棄並回報任何無法解析的名稱。
  若沒有任何名稱可解析，停止並要求使用者指名一個 skill——絕不退回去檢查所有 skill。

- **以 Step 0 解析出的 check 編號作為要套用的 check。**
  `1` 把整項 check 納入範圍；`1.3` 只把那一條判準納入範圍，把 check 1 的其餘各條排除在本次執行之外；下方各 step 依此判定，報告也要明講。

- **只有當 Step 0 沒有解析到任何 check 編號時，才呈現 check picker**，透過 `vscode_askQuestions` 讓使用者選擇要套用哪些 check。
  絕不沿用前一次執行的選擇：
  - 一個問題，`header: checks`，`question: Select the checks to apply`，`multiSelect: true`。
  - 六個選項，全部標為 recommended：
    - `1 Template alignment` — 該 skill 的 `SKILL.md` 與 `README.md` 是否遵循 `SKILL-tmp.md` 與 `README-tmp.md`？
    - `2 Config conformance` — 該 skill 是否遵循 workspace 的 `config.yaml`？
    - `3 Description accuracy` — 該 skill 的 `description` 是否與其 workflow 實際所做與所產出的相符？
    - `4 Terminology usage` — 每一節是否都使用該 skill 自己定義的 term，而不是重述或換句話說？
    - `5 Cross-platform compatibility` — 該 skill 要執行的指令與它的腳本，是否在 Windows、macOS 與 Linux 上都能運作，或說明它假定的平台？
    - `6 Dataflow` — 該 skill 之 `README.md` 中的 Dataflow 是否以 DFD 畫法，畫出它的各個 step 實際讀寫的東西？
  - 若使用者什麼都沒選，停止並說明沒有選取任何 check。

- 顯示解析後的選擇：
  - **Summary line**：有多少 skill 成功解析，以及選了哪些 check。
  - **Skills table**，欄位為 **Skill**、**Group**、**Path**。
  - **Notes**：每一個被捨棄的名稱；明確指名每一項**未**被選取的 check，因為沒跑過的 check 不等於一張健康證明；被縮小的 check 中所排除的每一條判準，同理也要指名。


## Step 2 - Scan the Selected Skills

- 針對整批選擇執行一次 `scan_skill.py` 腳本，把每個被選取的 skill 都傳進去。
  - `--skill`：一個被選取的 skill 名稱；每個 skill 重複一次此旗標。
  - `--out`：**CONFIGURATION** 之下所給的 **facts file** 路徑。
  - `--template`：Step 0 已確認的 SKILL template 路徑。
    腳本會從中讀出必要的標題，因此參考基準絕不是寫死在程式碼裡、記憶中的形狀。
  - `--readme-template`：Step 0 已確認的 README template 路徑，以同樣的方式讀出 `README.md` 的標題。
  - `--depends-on`：`{skillGroups.common}\scripts\depends_on.py`，腳本載入它，以 `depends_on.py check` 讀取的方式讀取每一份 `README.md` 的 header quote。
  - 範例：`python {skillGroups.common}\skills\check-skill\scripts\scan_skill.py --skill report-pipeline --skill triage-test-case --out "temp\check-skill-facts-{yymmdd-hh}.yaml" --template "{skillGroups.common}\templates\SKILL-tmp.md" --readme-template "{skillGroups.common}\templates\README-tmp.md" --depends-on "{skillGroups.common}\scripts\depends_on.py"`

- 該腳本**只蒐集事實、絕不下判定**——它記錄每個檔案含有什麼，把每一項判斷留給各項 check：
  1. 在 `skillGroups` 根目錄下解析每個 skill 並讀取其 `SKILL.md`。
  2. 記錄 **template-shape** 事實：YAML frontmatter 是否可解析且帶有 `name` / `description`、`name` 是否等於目錄名稱、`name` 與 `description` 的字元數（`name_chars`、`description_chars`）以及 `name` 是否只含小寫字母、數字與連字號（`name_charset_ok`）、SKILL template 自身所定義的頂層標題（`required_headings`，從 `--template` 檔案讀取，因此 template 一改參考基準就跟著改）、該 skill 具備其中哪些、缺少哪些（`missing_headings`）、既有的那些是否維持 template 的相對順序、找到的 `## Step N` 標題、是否從 0 開始連續、Step 0 是否命名為 `Warmup`，以及每一處指向後方的 step 參照。
  3. 記錄該 `SKILL.md` 的 **config-shape** 事實：每一個字面上的 `wiki\` / `wiki/` 路徑、每一個 `{wikiDir}` / `{vaultName}` / `{skillGroups...}` placeholder 及 Step 0 是否解析它、每一個機器專屬的絕對路徑、每一個 UNC 分享路徑，以及每一個直接寫死而非透過 `skillGroups` 的 `.github\...` 路徑。
  4. 記錄 **dir-config-shape** 事實：對 **skill directory 下的每一份其他文字檔**——各個腳本、各份 reference、繁體中文 twin、它自己的 `config.yaml`——蒐集同樣那組寫死路徑的事實，每一筆帶有所在檔案、該檔案的 `kind`（`script`、`reference`、`twin`、`skill config`、`doc`、`other`）、行號、該行是否為註解或 Python docstring（`commented`），以及該 skill 是否有自己的 `config.yaml`（`has_own_config`）。
     它也會列出被略過的檔案與原因——二進位檔，或超過掃描大小上限者——讓沒人檢查過的檔案永遠不會被誤認為乾淨的檔案。
  5. 記錄 **leftovers**：任何 `{PLACEHOLDER}` token、任何已停用寫法的 placeholder（另列於 `old_placeholder_tokens`）、任何在磁碟上解析不到的 `.github` rules 連結、SKILL.md 指名卻不存在的任何 `scripts\*.py`，以及磁碟上存在但 SKILL.md 從未指名的任何腳本。
  6. 為每一項事實標上它所在的 region、它是否位於 inline code 區段之內（`backticked`）或 fenced 區塊之內（`fenced`），以及它所在的整行原文（`line_text`）——字面路徑在 `frontmatter` 與 `prompt_examples` 中是預期之內的、只有在 `body` 中才可疑，被反引號包住或被 fence 包住的 token 是正在被*展示*而非被遺留，而那一行原文就是 finding 要引述的內容。
     來自 `SKILL.md` 以外的事實，則以所在檔案與 `commented` 旗標取代 region。
     以同一份檔案中的同一個 token 出現在兩行為例，看這些欄位各自定了什麼：

     ```
     - `{SKILL_NAME}` -> the skill name parsed in Step 0.
       backticked: true  -> the step is describing the token. Not a leftover.

     - Replace {SKILL_NAME} with the parsed name.
       backticked: false -> the token really was left behind. A finding, which
                            quotes this whole line from line_text.
     ```
  7. 記錄 **terminology** 事實：該 skill 是否有字彙表區段（任何名稱含 `TERMINOLOGY` 的 `#` 標題）、它定義的每個 term、字彙表之外每一行完全照用該 term 之處、每一行改以其大小寫或形態變體出現之處、每一行直接使用該定義所引入之檔名之處，以及每一個定義在 `CONFIGURATION` 標題下而非字彙表中的 term（`terms_defined_in_configuration`）。
     沒有字彙表的 skill 會得到 `has_glossary: false`，而其 `CONFIGURATION` 中的定義仍會被記錄。
  8. 記錄該 skill 之 `README.md` 的 **readme-shape** 事實：它是否有 `README.md`（`has_readme`），以及它與 `SKILL.md` 是否有繁體中文 twin；它的標題，以及 README template 定義的 `#` 與 `##` 標題（`required_headings`，從 `--readme-template` 檔案讀出）中缺少哪些（`missing_headings`）、現有的是否保持 template 的順序；它的 header quote 宣告的每一項依賴，以及 `depends_on.py check` 給它的狀態——`UNCHANGED`、`CHANGED`、`NO_RECORD`、`NOTHING_CITED` 或 `MISSING`；對照 Workflow，它的 Step Purposes 漏掉、名稱不符或沒給 Purpose 的每一個 step，它的 Files Each Step Uses 之樹漏掉或名稱不符的每一個 step，以及那一節是否以一句粗體句回答「哪些 step 執行腳本」那條規則；其中的每一個 `{PLACEHOLDER}` token 與每一個已停用寫法的 placeholder（另列於 `old_placeholder_tokens`）；以及 `SKILL.md` 中放著應屬於 `README.md` 之內容——`# Dataflow` 或 `# Steps at a Glance` 標題、`- **Purpose**:` 行、介紹 Purpose 的那一段——或連到它的每一行。
  9. 記錄該 skill 之 `README.md` 中 `## Dataflow` 的 **dataflow** 事實，每一個行號都是那份檔案的行：它是否有 Dataflow（`has_dataflow`），以及其中有幾張 mermaid 圖；第一張圖中的每個節點及其所用的形狀、每一支箭頭及其是否為虛線、雙頭或藍色，以及圖後跟著幾行圖例；對照 Workflow，圖上漏掉或名稱不符的每一個 step；還有每一個被較後 step 覆寫的 record、每一個由好幾個 step 依序編輯的 record、每一份沒有任何東西提供的資料、每一支連接兩份資料的實線箭頭、每一次對較後 step 所寫之物的讀取，以及每一個在第一個寫入者之前的 step 讀到它原本樣子的 record。
  10. 把 facts file 寫到 `--out` 路徑——每個 skill 一份 YAML 文件——並將其路徑與每個 skill 一列摘要印到 **stdout**。

- 讀取位於 `temp\check-skill-facts-{yymmdd-hh}.yaml` 的 facts file。
  每一項事實都帶有行號，因此針對它回報 finding 時要引述那一行。

- 每個 skill 顯示一行：其群組、行數與 step 數量、缺少的標題、它是否有 `README.md` 以及其中缺少的標題，以及其 **skill directory** 中被掃描讀取與略過的檔案數量——並連同原因指名每一份被略過的檔案，因為沒被讀過的檔案並不算合規。


## Step 3 - Apply the Selected Checks

- **本 step 不使用腳本**——判定某處偏離究竟是真正的缺陷，還是刻意且有充分理由的例外，是程式做不到的閱讀與判斷，因此請自行依下列指示進行。

- 依編號升冪走過 Step 1 納入範圍的每一項 check。
  每一項都是：讀它的輸入、判定、記錄，然後換下一項。
  未被選取的 check 要明講，並且不為它產生任何判定。

- **Inputs**，逐項 check。
  此處指名的每一個 fact group 都來自 Step 2 寫在 `temp\check-skill-facts-{yymmdd-hh}.yaml` 的 facts file：

  | # | Check | Input |
  |---|-------|-------|
  | 1 | Template alignment | 位於 `{skillGroups.common}\templates\SKILL-tmp.md` 與 `{skillGroups.common}\templates\README-tmp.md` 的兩份 template，外加 `template_shape`、`readme_shape` 與 `terminology` fact group |
  | 2 | Config conformance | workspace 的 [config.yaml](config.yaml)，外加 `config_shape` 與 `dir_config_shape` fact group，以及 checked skill 自己的 `config.yaml`（如果有） |
  | 3 | Description accuracy | 每個被選取的 skill 的**整份** `SKILL.md`——它的 `description` 欄位、它的 `# MUST FOLLOW` 契約，以及每一個 step 區段。本項不讀任何 fact group |
  | 4 | Terminology usage | `terminology` fact group。facts 顯示 `has_glossary: false` 的 skill 不在範圍內——它的 verdict 是 ➖ `no glossary — not applicable`，且不產生任何 finding，而不是替它捏造它從未主張過的 term；它缺少字彙表這件事已經由 check 1 提出為 issue |
  | 5 | Cross-platform compatibility | 每個被選取的 skill 的**整份** `SKILL.md`，以及它 `scripts\` 底下的每一支腳本——某個 step 要 agent 執行的指令，以及每支腳本的子行程與平台專屬呼叫。本項不讀任何 fact group |
  | 6 | Dataflow | `dataflow` fact group、[DFD.md](.github/common/references/DFD.md)，以及每個被選取的 skill 的**整份** `SKILL.md` 與 `README.md`——每一個 step 區段，用來比對它讀寫的東西與 `README.md` 中 Dataflow 所畫的。facts 顯示 `has_dataflow: false` 的 skill 不在範圍內——它的 verdict 是 ➖ `no Dataflow — not applicable`；它缺少 `README.md` 或 Dataflow 這件事已經由 check 1 提出為 issue |

- 依 **checking criteria** 判定每個被選取的 skill——先讀它的 `Rules that apply to every check` 一節，再讀當前所套用之 check 的那一節，且只限於 Step 1 納入範圍的那幾條判準。
  判定前兩節都要讀過；絕不憑記憶中的判準辦事。

- **為報告記錄每一項 finding**，逐項 check、逐個 skill：它的嚴重度——**issue** 或 **recommendation**——它違反的判準（`<check>.<criterion>`）、它的檔案與行號、取自 `line_text` 的整行違規原文、它為何違反契約或偏離基準，以及如何解決它。
  - 只有一個明顯變更的 finding 成為 **direct fix**；記錄那個變更，若是用字上的變更，連同替換文字一起記錄。
  - 有不只一種合理解決方式的 finding——通常是兩處彼此矛盾，必須由使用者說明哪一處為準——成為 **decision item**；記錄它牽涉的每一行，以及每一個 **option**，連同該 option 會變更的行與檔案，以及它的代價。
  - check 3 的 finding 要同時記錄 description 的主張，以及與之矛盾或遺漏它的那個 step，因為 workflow 才是權威，要改的是那個主張。

- **也要記錄每一項 check 查過而乾淨的部分**，供報告的 notes 使用——每一項都留下紀錄，而不是悄悄放過：
  - Check 1 — 通過的判準，以及每一個被該 check 判定為正當省略的 template 區段。
  - Check 2 — 通過的判準；每一個被判定為刻意為之的字面路徑，連同其 region——若來自 `SKILL.md` 以外則連同其檔案與類別——一併指名，讓刻意的字面路徑不會被誤認為未經審視的；以及掃描所略過的每一份檔案，因為沒被讀過的檔案並不算合規。
  - Check 3 — 通過的判準，以及每一項被記為 `unknown` 的主張，因為 workflow 既無法確認也無法否定的主張並不算通過。
  - Check 4 — 檢視了多少個 term、其中有多少被使用，以及每一個因為沒有字彙表而被略過的 skill，明確指名，因為被略過的 skill 並不等於一致的 skill。
  - Check 5 — 通過的判準、每一個被判定為只是展示而非執行的指令，以及該 skill 所聲明的每一個平台，因為已聲明的平台不算缺陷。
  - Check 6 — 通過的判準、比對了多少個 step、多少份資料與多少支箭頭，以及每一個因為沒有 Dataflow 而被略過的 skill，明確指名，因為被略過的 skill 並不等於合規的 skill。

- 在每一項 finding 之外，另行記錄判定過程中暴露出的每一個 **checker defect**——`scan_skill.py` 弄錯的事實，或誤導判定的判準——連同誤導它的那一行。


## Step 4 - Report the Findings

- **本 step 不使用腳本**——把論證鋪陳到讀者能據以行動，是寫作而非計算，因此請自行依下列指示進行。

- **在對話中回報。**
  本 step 的任何內容都不寫入檔案。

- **呈現 Step 3 的 finding，不做任何新的判定。**
  撰寫時注意到的缺口，是那項本該抓到它的 check 的缺口——把它記為 **checker defect**，絕不記為新的 **item**。

- **每個 checked skill 一個區段**，依 Step 1 解析它們的順序排列，開頭一行：該 skill、它的群組，以及它的整體 **verdict** 與總數。

- **在其中，每一項跑過的 check 一個子區段**，依編號順序，各自以 **verdict → notes → items** 的順序排列：
  - **Verdict** — 該 check 對此 skill 的 **verdict**。
    縮到部分判準的 check 要在旁邊指名那些判準，讓縮小後的通過絕不被讀成整項通過。
  - **Notes** — 一兩句不編號的句子，說明查了什麼、查過而乾淨的是什麼：通過的判準、檢視過的事實，以及 Step 3 為此 check 記錄的 notes。
    它們不佔編號。
  - **Direct fixes**，然後 **Needs your decision**——兩個標籤一律出現。
    空的那一個寫 **None**：這個空位本身就說明該 check 是乾淨的，而不是被略過。

- **每個 item 以 `<check>.<n>` 編號：**
  - `<n>` 在每一項 check 中從 1 開始，絕不跨 check 延續——check 3 的第一個 item 是 `3.1`。
  - direct fix 與 decision item 共用同一組序號：direct fix 在前，decision item 接續其後，因此任何 check 都不會出現兩個 `3.1`。
  - **None** 不佔編號。
  - 編號只在本報告中有效；重跑會重新編號，因此舊編號絕不指涉新報告中的 item。
  - 當本次執行檢查了不只一個 skill 時，編號只在其 skill 的區段內唯一，使用者要兩者一起指名（`imp-app 1.1`）。

- **每個 item 的標題寫成** `**<check>.<n> <the problem in one line>**`，後面接它的嚴重度，以及它違反的判準。

- **direct fix 的順序是 Problem → Fix：**
  - **Problem** — 以連結呈現它的檔案與行號、引述違規文字，並說明它為何違反契約或偏離基準。
  - **Fix** — 改什麼、改在哪些檔案；只要該變更是用字上的變更，就附上替換文字本身。

- **decision item 的順序是 Original → Problem → Options**——原文排在最前面，因為使用者必須先看到該 skill 實際怎麼寫，才能選邊，而問題敘述裡的轉述不足以做到這一點：
  - **Original** — 這項決策牽涉的每一行，各自以連結呈現其檔案與行號，並在連結下方以區塊引言**完整**引述：從行首到行尾逐字照抄，只去掉行首縮排與條列符號。
    絕不節錄某一行，也絕不用 `…` 省略——被切斷的一行會失去這項選擇所取決的條件與範圍。
    表格列則整列引述。
  - **Problem** — 那些行為何互相矛盾，或這項選擇是在哪幾者之間。
  - **Options** — `(a)`、`(b)` 依此類推，各自說明它改什麼、動到哪些行與檔案，以及它的代價。
    然後是 **Recommended**：你會選的那個 **option**，並以一句話說明其他為什麼比較差。

- **展開的篇幅要與決策相稱。**
  direct fix 維持兩三行；decision item 值得完整處理。
  把簡單的 item 灌水到跟複雜的一樣長，只會把複雜的那個淹沒。

- **對某個 skill 之 `SKILL.md` 或 `README.md` 的變更，也要指名那份檔案的繁體中文 twin**（如果它有的話）——twin 在同一次編輯中一起改，因此這項修正會動到兩份檔案。

- 以一個 skill、一項 check 為例的形狀：

  ```
  ❌ imp-app (common) — 4 issues, 8 recommendations across checks 1-4

  ### 1 Template alignment — ❌

  Criteria 1.1, 1.2, 1.5-1.8 and 1.10 pass: <what was looked at>.

  **Direct fixes**

  **1.1 No Prompt Example shows `run step N`** — issue, criterion 1.9
  - **Problem**: [SKILL.md:138](<absolute-path>:138) — <quoted text>; <why>.
  - **Fix**: <what changes, in SKILL.md and SKILL-tw.md>.

  **Needs your decision**

  **1.2 `# CONFIGURATION` defines `app dir` instead of giving its value** — issue, criterion 1.3
  - **Original**:
    - [SKILL.md:39](<absolute-path>:39)
      > <the whole line>
    - [SKILL.md:93](<absolute-path>:93)
      > <the whole line>
  - **Problem**: <why the two lines conflict>.
  - **Options**:
    - (a) <change> — touches SKILL.md:93 and SKILL-tw.md:91; <cost>.
    - (b) <change> — touches SKILL.md:39 and SKILL-tw.md:37; <cost>.
  - **Recommended**: (a) — <why (b) is worse>.
  ```

- **報告以下列內容作結，依此順序，此外別無他物：**
  1. **Root cause** — 只有當多項 check 中的 finding 源自同一個原因時才寫：指名該原因，以及它所牽動的 item 編號。
     那些 item 仍留在各自的 check 之下；絕不把它們搬到這裡。
  2. **Checker defects** — Step 3 記錄的每一個 checker defect，註明誤導掃描或該 check 的那一行，並明確聲明它是 `scan_skill.py` 或某項 check 自身指示中的缺陷，而非 checked skill 的問題。
     不編號、不計數——checker 的 bug 不是作者的債。
  3. **Not selected** — 本次執行沒有套用的 check，以一行指名，因為沒跑過的 check 不等於乾淨的 check。
  4. **How to apply** — 使用者以指名編號來套用 item（例如 `fix 1.1 3.2`、`fix 1.2(a)`、`fix all of check 1`），在他們指名之前什麼都不會改。


## Step 5 - Update the Skills Dashboard

- **每一次執行都要跑本 step**，包含每個 checked skill 都回報乾淨的那一次。
  乾淨的一列正是「前一次執行的那些 finding 已經不在了」的證據，因此略過它，會讓一個已修好的 skill 看起來仍是壞的。

- 針對每個 checked skill 各執行一次 `update_dashboard.py` 腳本。
  - `--dashboard`：**CONFIGURATION** 之下所給的 **Skills Dashboard** 路徑。
  - `--run`：本次執行的 `{yymmdd-hh}` 戳記。
    腳本只記錄它的日期，寫成 `yyyy-mm-dd`。
  - `--skill`、`--group`、`--path`：該 skill、它的群組與它的絕對 `SKILL.md` 路徑，皆依 Step 1 所解析。
    群組決定那一列歸在哪個 section 底下。
  - `--result`：每一項跑過的 check 各一次，依 Step 3 的計數寫成 `<check>:<issues>:<recommendations>`；縮到部分判準的 check 則寫成 `<check>:<issues>:<recommendations>:<criteria>`，判準之間以 `+` 相連（例如 `1:0:1:1.3+1.5`）；沒有字彙表的 skill 則寫成 `4:na`，沒有 Dataflow 的 skill 則寫成 `6:na`。
  - 範例：`python {skillGroups.common}\skills\check-skill\scripts\update_dashboard.py --dashboard "{wikiDir}\dashboard\skills.md" --run {yymmdd-hh} --skill report-pipeline --group dedi-triage-pipeline --path "<absolute SKILL.md path>" --result 1:1:5 --result 2:0:0 --result 3:0:2 --result 4:na`

- 該腳本：
  1. dashboard 還不存在時連同表頭一起建立它，否則讀回它的表格。
  2. 以本次執行套用的 check 取代該 skill 對應的各格，並且**對本次執行未選取的 check 不記錄任何東西**——那一格保留先前的結果，並標上產生它的那次執行的日期，因為沒跑過的 check 並不是「它的 finding 已經不在了」的證據。
  3. 把該列的 **Checked** 設為本次執行的日期、把該 skill 連結到它的 `SKILL.md`，並依各格重新計算該列的整體 verdict。
  4. 只有當本次執行完整地重新套用了該列所持有的每一項 check 時，才清除該列的 **needs check** 標記。
  5. 其他每個 skill 的列都不動，把每一列歸到它的 group 的 section 底下——section 依 group 排序、列依 skill 排序——並刷新表頭的 **Updated** 欄位。
  6. 把它變更的每一格印成 `old -> new`。

- 逐個 skill 顯示其呼叫所變更的各格，寫成 `old -> new`，讓使用者看到 dashboard 動了、以及怎麼動的。
  只有當某一格從先前某次執行留下的值降下來時，才說某項 finding 已經不在了——那個下降才是證據，單憑本次執行則不是。

- 以確切的檔名刪除 **facts file**——`temp\check-skill-facts-{yymmdd-hh}.yaml`，絕不使用萬用字元。
  本 step 之後沒有任何東西會讀它。


## Step 6 - Apply the Named Items

- **只有當使用者以指名 item 來回覆報告時才執行。**
  使用者沒有回覆報告的那次執行，在 Step 5 就已完成。

- **本 step 不使用腳本**——解決一項 finding 意味著改寫行文、同時保住它的意思，這需要判斷。

- **依報告的編號讀取所選項目**——`fix 1.1 3.2`、像 `1.1-1.3` 這樣的範圍、`all of check 3`，或 `all`：
  - **decision item** 需要它的 **option**（`1.2(a)`）；只指名 item 卻沒有 option 時，詢問要哪一個，絕不替使用者挑。
  - 當本次執行檢查了不只一個 skill 時，編號需要連同它的 skill 一起指名（`imp-app 1.1`）。
  - 報告中沒有的編號，或可能指兩個 item 的編號，都是要問使用者的問題，絕不猜測。

- **依指名的順序逐一套用 item**，每套用一項就回報一項：改了什麼、在哪些檔案、在哪幾行，並以連結呈現。

- 適用於每一個 item 的規則：
  - **只改該 item 指名的內容，其餘一概不動。**
    編輯時注意到的問題要回報、不要修正——它還沒被判定過，而判定它的是下一次執行。
  - **在同一個 step 中把每一處變更同步到被改之檔案的繁體中文 twin**——`SKILL.md` 同步到 `SKILL-tw.md`，`README.md` 同步到 `README-tw.md`——放在相同的標題之下，並讓每一個標題、字彙表 term、inline-code 區段、fenced 區塊與連結目標都保持英文。
    帶有 `-tw` twin 的 reference 檔案被改動時，也以同樣的方式與它的 twin 一起改。
  - **傳遞改名**——term、檔案、標題或腳本旗標的改名——到 **skill directory** 中指名它的每一處：字彙表、每一個 step、各份 twin、每個腳本的說明文字，以及 `README.md` 的 Dataflow、Step Purposes 與 Files Each Step Uses，它們以每個 step 的標題指名它。
  - **當某項變更改動了一個數值或一條定義時，找出該 skill 中重述它的每一個其他句子**——行文常會複述表格的數字或字彙表條目——並一併修改，讓這項修正不會自己開出一道新的偏離。
  - **當某項變更引入或改寫了一個 term 時，在同一次編輯中更新它的字彙表條目**，並在行文指名它之處都使用該 term——以粗體呈現，拼法與字彙表相同。
  - **絕不編輯 checked skill 目錄之外的東西。**
    **checker defect** 只有在使用者另外要求時，才在本 skill 中修正。

- **套用完最後一個 item 之後，在 dashboard 上把該 skill 標為需要重新檢查**，讓它那一列不會被誤認為是對已編輯之 skill 的檢查結果：
  - 範例：`python {skillGroups.common}\skills\check-skill\scripts\update_dashboard.py --dashboard "{wikiDir}\dashboard\skills.md" --skill imp-app --mark-modified`
  - 各格維持最後一次檢查所留下的樣子——它們描述的是這些編輯之前的 skill——而下一次重新套用每一項 check 的執行會清除 **needs check** 標記。

- 最後列出已套用的 item、任何被略過的 item 及原因，並說明對該 skill 重跑 `/check-skill` 才能確認這些修正。
