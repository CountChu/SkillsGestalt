# Create MD report file

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-18`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-30`  `8cc2e2061175`

> 本檔案以 ASD-STE100 Simplified Technical English（STE）第 9 版寫成。
> 技術用字：argument、backtick、byte、cache、canonical skill invocation、checkpoint、clock、command、content、disk、double-quoted string、editor、escape character、escaping、fence、field、file、file-editing tool、filename、frontmatter、hard-code、header、here-string、interpolation、line、orchestration、parse、path、pipe、placeholder、root、section、shell、single-quoted here-string、skill、string、table、template、text、title、wiki、workflow、workspace、wrapper。

- 每個 skill 都在自己的 MUST FOLLOW 一節中寫出它的報告檔名（例如 `run-pr-{prId}-{yymmdd}`）。
- 在 `{wikiDir}\{skill_name}\{REPORT_FILENAME}.md` 建立 MD report 檔案。
  從 workspace 的 [config.yaml](config.yaml)（位於 workspace 根目錄）讀取 `wikiDir`。
  不要把 wiki 的根目錄寫死。
  - 如果檔案已經存在，依照下面的規則更新它的檔頭欄位。
    然後刪除檔頭之後的所有內容。
- 用這份 template 寫出 MD report 檔案，並把 placeholder 換成它們的值：

  ````markdown
  # {REPORT_TITLE}

  - **Skill**: {SKILL_NAME}
  - **Checkpoint**: `{CHECKPOINT_PATH}`
  - **Created**: {DATETIME}
  - **Updated**: {DATETIME}
  - **Prompt**:
  ```
  {USER_PROMPT}
  ```
  ````

  Placeholders：
  - `{REPORT_TITLE}` → 這次 skill 執行的報告標題。
  - `{SKILL_NAME}` → skill 的名稱，取自 YAML frontmatter。
  - `{CHECKPOINT_PATH}` → 這次執行的 YAML checkpoint 的路徑，即 skill 的 MUST FOLLOW 一節所寫的路徑（例如 `checkpoints\report-pipeline\{reportName}\process.yaml` 或 `checkpoints\report-known-issues\{reportName}.yaml`）。
  - `{DATETIME}` → 目前的本地日期與時間（`YYYY-MM-DD HH:MM`）。
    在寫入時從系統時鐘讀取它。
    在 PowerShell 中，用 `Get-Date -Format "yyyy-MM-dd HH:mm"`。
    在 macOS/Linux 上，用 `date '+%Y-%m-%d %H:%M'`。
    不要用估計值，或之前看到的時間。
    - **Created**：如果 MD report 檔案已經存在，保留它最初的 Created 值。
    - **Updated**：一律設為目前的日期與時間。
  - `{USER_PROMPT}` → Step 0 保存的 **canonical skill invocation**。
    它是 `/<skill-name>` 指令，後面接著 skill 解析出的引數（例如 `/report-week-note` 接著 `7/9 - 7/14`）。
    記錄這個 canonical skill invocation。
    **不要**記錄它周圍的文字，即使那段文字啟動了這次執行。
    這種文字的例子有外層包裝、編排，以及給 agent 的指示。


# Update MD report file

- 在每一個會往 MD report 檔案加入內容的 workflow step 結束時，套用這些規則。
- 照上面 `{DATETIME}` 的說明設定 **Updated** 欄位。


# Write the MD report file safely

- 報告裡有很多反引號、程式碼的 fence 與表格的 pipe。
  因此，文字**如何**寫到磁碟上，和文字的內容一樣重要。
- **可以的話，直接用編輯檔案的工具寫入檔案。**
  損壞報告文字的原因，是文字所經過的 shell 指令。
  而且，建立報告並不需要使用 shell。
- **不要讓報告文字經過 PowerShell 的雙引號字串。**
  在 `"..."` 中，反引號是 PowerShell 的跳脫字元，PowerShell 會在寫出文字之前改變它。
  `` `r `` 變成 CR，`` `n `` 變成 LF，`` `a `` 變成 BEL，`` `t `` 變成 TAB，其他每一個 `` `x `` 都只變成 `x`。
  例如，``verified `resolved` `` 這一行寫到磁碟上會變成 `verified ` + CR + `esolved`。
  而且，三個反引號的 fence 會變成一個反引號。
  你**不會收到錯誤訊息**：指令會顯示它正確執行了。
- 如果非用 shell 不可，就把文字放進**單引號的 here-string**。
  單引號的 here-string 不做跳脫，也不做 interpolation。
  然後以不含 BOM 的 UTF-8 寫出這些文字：

  ```powershell
  $md = @'
  ...report text, backticks and fences intact...
  '@
  $md = $md.Replace('{UPDATED}', $now)
  [System.IO.File]::WriteAllText($path, $md, [System.Text.UTF8Encoding]::new($false))
  ```

  在 here-string **之後**再用 `.Replace(...)` 替換這些值。
  如果你在 `"$var"` 中使用 interpolation，跳脫就會再次發生。
  單引號的 here-string 正是為了防止這種跳脫而存在。
- 用 shell 寫入之後，用 `[System.IO.File]::ReadAllText($path)` 確認寫出的位元組是正確的。
  編輯器可能從它的快取讀取這個檔案，並顯示檔案先前的內容。
  這時你可能以為 shell 沒有寫入這個檔案，雖然 shell 已經正確地寫入了它。
