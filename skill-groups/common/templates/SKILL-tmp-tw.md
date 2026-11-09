---
name: {SKILL_NAME}
description: {SKILL_DESCRIPTION}
---

本文件為 [SKILL-tmp.md](skill-groups/common/templates/SKILL-tmp.md) 的繁體中文版。
任一份改了某節，另一份必須在同一次執行中一起改。

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-19`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-11-02`  `c612bdfa1ea7`

> 本檔案以 ASD-STE100 Simplified Technical English（STE）第 9 版寫成。
> 技術用字：analysis、API、argument、bearer token、call、canonical skill invocation、column、command、configuration、configuration file、credential、data file、definition、development、directory、efficiency、file、folder、forward slash、glossary、header、inline code、key、line、link、link target、list、map、MD report、model、output directory、parse、parser、PAT、path、plain text、process、run record、project、raw data、registry、root、run、run number、save、scope、script、section、selector、separator、session、shell、skill、step file、table、temp dir、term、terminal、user、vault、wiki、workflow、working data、working dir、workspace、writer step。

# TERMINOLOGY

每個 skill 都以相同的定義使用這些 term。
本 skill 沒用到的 term 就刪掉。
如果 glossary 列出了 skill 沒用到的 term，skill 改變時，這個 term 的定義就可能變得不正確。

- **`run step N`** — 放在 prompt 結尾、用來識別某一個 step 的選擇子。
- **Run Number** — 一次執行的編號 `{yymmdd}.{N}`。
  `{N}` 是這個 skill 在那一天的執行序號，從 1 開始。
- **Working Dir** — 一次執行所用的目錄，存放這次執行所有的 working data：它的 step 檔、資料檔與暫存檔。
  它是 Temp Dir 或 Checkpoint Dir，**CONFIGURATION** 列出是哪一個。
  skill 不移除它。
- **Temp Dir** — 位於 workspace 根目錄 `temp\` 的 Working Dir。
- **Checkpoint Dir** — 位於 workspace 根目錄 `checkpoints\` 的 Working Dir。
- **Step file** — Working Dir 中的 `step_{N}.yaml`。
  每個 step 都把它的輸出寫在那裡。
  因此，後續的 step 讀取這些輸出，而不必再算一次。
- **Run record** — 記下一次執行每個 step 的時間與模型的檔案。
  分析一個 skill 的效率時使用它。
- **Handoff file** — 一次執行為另一個 skill 產生的檔案，放在 `handoff\`。
- **MD report** — skill 寫進 wiki vault 的 Markdown 報告，放在以該 skill 命名的資料夾中。
  它在各節結果之上帶有標準表頭（Skill、Run record、Created、Updated、Prompt）。

# DEDICATED TERMINOLOGY

只有本 skill 使用的 term。

- **{TERM_1}** — {TERM_1_DEFINITION}
- **{TERM_2}** — {TERM_2_DEFINITION}

# CONFIGURATION

本 skill 在一次執行中所使用的值。
本 skill 不讀取、不執行或不產出的項目，就刪掉它那一行。
兩行 Working Dir 只留一行。

執行時讀取或執行的輸入與工具：

- **Workspace configuration** — workspace 根目錄的 [config.yaml](config.yaml)。
- **Scripts** — `{skillGroups.{SKILL_GROUP}}\skills\{SKILL_NAME}\scripts\{SCRIPT_PATH_1}`。

一次執行的 working data，執行結束後沒有人、也沒有 skill 讀它：

- **Working Dir** — Temp Dir，`temp\{SKILL_NAME}\{yymmdd}.{N}\`。
- **Working Dir** — Checkpoint Dir，`checkpoints\{SKILL_NAME}\{yymmdd}.{N}\`。

最後的輸出，人、另一個 skill 或之後的分析會讀它：

- **Run record** — `database\skill-runs\{SKILL_NAME}\{yymmdd}.{N}.yaml`。
- **Handoff file** — `handoff\{SKILL_NAME}\{yymmdd}.{N}.md`。
- **MD report** — `{wikiDir}\{SKILL_NAME}\{REPORT_FILENAME}.md`。
  `wikiDir` 來自 workspace 的 [config.yaml](config.yaml)，由 Step 0 找出它的值。
  不要把 wiki 的根目錄寫死。

# MUST FOLLOW

- 逐一執行 workflow 的每個 step，並顯示每個 step 的編號。
- **遵守 `run step N` 選擇子**：執行 Step N，然後停止。
  從每一個先前 step 的 step 檔讀取它的輸出。
  不要執行後續的 step。
- MD report 的表頭與形狀，遵守 [report-md-rules.md](skill-groups/common/rules/report-md-rules.md)。
- 一次執行的 Run Number、step 檔、run record 與 Working Dir，遵守 [run-data-rules.md](skill-groups/common/rules/run-data-rules.md)。
- **Working Dir 中的每一份檔案都只有一個寫入它的 step。**
  產生資料檔的 step 會寫出整份檔案，而且只有那個 step 會改動它。
  後續做出決定的 step，把決定寫進它自己的 step 檔。
  它不在另一個 step 寫的檔案中新增、修改或刪除任何鍵。
  即使後續 step 的決定取代了那份檔案中的資料，這條規則也同樣適用。
- 如果不只一個 step 寫進同一份資料檔，第一個 step 再執行一次時，就會抹掉其他 step 的資料。
  例如，一次 parser 修正或一次 `run step 1`，都會把整份檔案重寫一次。
  這會抹掉所有後續 step 的結果，而且沒有任何訊息告訴你。
- **在 skill 停止之前，顯示 MD report 與 run record 的路徑。**
  只顯示這兩個路徑，不要顯示它們的內容。
  把這兩個路徑寫成點一下就能開啟的 Markdown 連結。
  不要寫成 inline code 或純文字。
  - **MD report** 要用帶有 `obsidian://open?vault={vaultName}&file=<vault-relative-path>` URI 的連結。
    vault 不在本 workspace 中，因此從 workspace 起算的連結目標找不到它。
    例如：`[{REPORT_FILENAME}.md](obsidian://open?vault={vaultName}&file={SKILL_NAME}/{REPORT_FILENAME}.md)`。
  - **run record** 要用從 workspace 起算的連結目標。
    以正斜線作為其中的分隔符號。
    例如：`[{yymmdd}.{N}.yaml](database/skill-runs/{SKILL_NAME}/{yymmdd}.{N}.yaml)`。
  - 每一次執行都要這樣做，只有一個 step 的執行也一樣，例如 `run step 0`。

# Prompt Examples


## Prompt 1

```
/{SKILL_NAME}
```

## Prompt 2

```
/{SKILL_NAME}
run step 0
```

## Prompt 3

```
{NATURAL_LANGUAGE_PROMPT}
```


# Workflow

## Step 0 - Warmup

- 找出 `{python}`，也就是 workspace 根目錄的 `.venv` 裡的 Python。
  macOS 與 Linux 上它是 `.venv/bin/python`，Windows 上是 `.venv\Scripts\python.exe`。
  後面 step 的每個 script 都以 `{python}` 執行。
  每個指令都在新的 shell 裡執行，新的 shell 不會沿用另一個指令啟動的 `.venv`。
  workspace 沒有 `.venv` 時，停下來。
  請使用者照 `common` skill group 的 forge-setup.md 第 3 步建立它。

- 讀取 [config.yaml](config.yaml)，也就是 workspace 根目錄的設定檔，並找出這些值：
  - **`wikiDir`**：MD report 的根目錄。
    本 skill 的報告放進 `{wikiDir}\{SKILL_NAME}\`。
  - **`vaultName`**：`wikiDir` 路徑的最後一段，例如 `MyVault`。
    它是 Obsidian vault 的名稱，`obsidian://` 連結會用到它。
  - **`skillGroups`**：從群組名稱到其 skills 根目錄的對應表。
    本 skill 的目錄是 `{skillGroups.{SKILL_GROUP}}\skills\{SKILL_NAME}\`。
  - 把後續 step 中的每一個 `{wikiDir}`、`{vaultName}` 與 `{skillGroups.{SKILL_GROUP}}`，換成你找到的值。
    指令中也要這樣做。
  - 如果 `config.yaml` 不存在，或缺少必要的鍵，就停止，並請使用者提供。

- 以 `[Environment]::GetEnvironmentVariable('ADO_PAT','User')` 取得 PAT。
  這會取得 **User-scope** 的值，而不是 session 的 `$env:ADO_PAT`。
  如果使用者在自己的 terminal 中設定 `$env:ADO_PAT`，這個值只存在於該行程。
  本 skill 執行所在的 terminal **看不到**這個值。
  但每個 shell 都會直接從 registry 讀取 User scope 目前的值。
  把這個值放進 session，各 step 的 script 讀取 `os.getenv("ADO_PAT")`，因此就能取得它：

  ```powershell
  $env:ADO_PAT = [Environment]::GetEnvironmentVariable('ADO_PAT','User')
  ```

- 確認 `ADO_PAT` 不是空的，而且**能正常運作**。
  做法是呼叫一個 ADO API，例如列出 projects 的那個 API。
  如果 PAT 是空的，或呼叫得到錯誤（例如 `401 Unauthorized`），**立即停止本 skill**。
  告訴使用者 `ADO_PAT` 無法使用。
  然後請使用者在 User scope 中保存一個新的 PAT（`[Environment]::SetEnvironmentVariable('ADO_PAT','<new-pat>','User')`），之後再執行本 skill。
  不要改用其他憑證，例如 Azure CLI 或 `ADO_BEARER` 的 bearer token。

- 執行 workflow 之前，確認下列 script 與檔案都在。
  只寫出開發本 skill 時加進 skill 目錄的檔案。
  這些檔案在 skill 的目錄中，緊鄰這份 `SKILL.md`。
  - `{skillGroups.{SKILL_GROUP}}\skills\{SKILL_NAME}\scripts\{SCRIPT_PATH_1}`

- prompt 符合 **Prompt Examples** 中的某一個例子。
  解析它，並找出這些項目：
  - {INPUT_1}
  - {INPUT_2}

- 如果缺少必要的輸入，請使用者提供。

- 保存 canonical skill invocation，讓後續的 step 可以參照它。

- 照 run-data-rules.md 取得 Run Number，並寫出這次執行的 run record。

- 以解析出的輸入，保存 `step_0.yaml`。
  把這個 step 加進 run record。
  在這個 step 中，不必建立 MD report 檔，因為這次執行此時可能還沒有重要的結果。


## Step 1 - {STEP_1_TITLE}

- 以 `{STEP_1_ARG_1}` 與 `{STEP_1_ARG_2}` 引數執行 script `{SCRIPT_PATH_1}`。
  - `{STEP_1_ARG_3}`：這次執行的 Working Dir。
  - 範例：`{python} {skillGroups.{SKILL_GROUP}}\skills\{SKILL_NAME}\scripts\{SCRIPT_PATH_1} {STEP_1_ARG_1} {STEP_1_ARG_1_VALUE} {STEP_1_ARG_3} "{WORKING_DIR}"`

- 該 script：
  1. {SCRIPT_1_ACTION_1}
  2. {SCRIPT_1_ACTION_2}
  3. 把結果以 `{STEP_1_OUTPUT}` 存進輸出目錄。
     這次執行的所有 step 都使用這份原始資料檔，它不是 step 檔。

- 保存 `step_1.yaml`，內容為：{STEP_1_CHECKPOINT_FIELDS}。
  把這個 step 加進 run record。

- 保存 MD report 檔。
  在檔案末尾加上一個 **{STEP_1_SECTION}** 區段，並顯示它：
  - **{STEP_1_TABLE} table**，各列為：
    - **{ROW_1}**
    - **{ROW_2}**：{ROW_2_RENDER_RULE}


## Step 2 - {STEP_2_TITLE}

- 讀取 Step 1 存在 Working Dir 的 `{STEP_1_OUTPUT}` 資料檔。
  以 {STEP_2_INPUT_KEY} 作為輸入。

- 這些規則適用於下列每一項指示：
  - {STEP_2_RULE_1}
  - {STEP_2_RULE_2}
  - 每一個決定都只根據你讀到的資料。
    不要提供資料中沒有的值。
    如果無法從資料對 {STEP_2_AMBIGUOUS_CASE} 做出決定，就把它記為 `unknown`。
    然後說明原因，不要用估計值。

- 對每一個 {STEP_2_ITEM}：
  1. {STEP_2_INSTRUCTION_1}
  2. {STEP_2_INSTRUCTION_2}
  3. {STEP_2_INSTRUCTION_3}

- 把結果寫進 `step_2.yaml`，作為 `{STEP_2_OUTPUT_KEY}`。
  不要寫進 `{STEP_1_OUTPUT}`，因為那份檔案是 Step 1 的。

- 保存 `step_2.yaml`，內容為：{STEP_2_CHECKPOINT_FIELDS}。
  把這個 step 加進 run record，並寫出 `result: completed`，因為它是最後一個 step。

- 保存 MD report 檔。
  在檔案末尾加上一個 **{STEP_2_SECTION}** 區段，並顯示它：
  - **Summary line**：{STEP_2_SUMMARY}。
  - **{STEP_2_TABLE} table**，欄位為：
    - **{COLUMN_1}**
    - **{COLUMN_2}**：{COLUMN_2_RENDER_RULE}
  - **Notes**：{STEP_2_NOTES}
