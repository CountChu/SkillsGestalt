# YAML Checkpoint Rules

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-18`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-30`  `8cc2e2061175`

> 本檔案以 ASD-STE100 Simplified Technical English（STE）第 9 版寫成。
> 技術用字：canonical skill invocation、checkpoint、clock、definition、directory、epoch、field、file、flat file、format、hard-code、heading、layout、metadata、minute、model、partial、path、root、rounding、second、section、skill、subfield、timestamp、workspace。

- 每個 skill 都在自己的 MUST FOLLOW 一節中寫出它的 YAML checkpoint 的路徑。
  YAML checkpoint 放在 workspace 根目錄的 `checkpoints\` 目錄中。
  這個目錄永遠是同一個。
  你在 `config.yaml` 中設定 MD report 的根目錄，但不能在那裡設定 `checkpoints\` 目錄。
  在這個目錄中，skill 使用兩種佈局：
  - `checkpoints\{skill_name}\{run_dir}\process.yaml` 把每次執行放在不同的目錄中。
    該次執行還會在 checkpoint 所在的同一個目錄中寫出資料檔或 section partials 時，skill 使用這種佈局。
  - `checkpoints\{skill_name}\{report_filename}.yaml` 是每次執行一份的扁平檔案。
- 每個 step 都必須把它重要的輸出欄位寫進這份 YAML checkpoint 檔案。
- 每個 step 都把它的輸出放在名為 `step_{number}` 的群組中（例如 `step_0` 與 `step_1`）。
- 每個 step 都必須包含一個 `title` 欄位。
  這個欄位的值與 skill 定義中該 step 的標題相符（例如 `Warmup` 與 `Fetch PR Info`）。
- `step_0` 必須包含下列欄位：
  - `skill`：skill 的名稱。
  - `model`：執行這個 skill 的 AI 模型。
  - `prompt`：canonical skill invocation，也就是 [report-md-rules.md](.github/common/rules/report-md-rules.md) 中的 `{USER_PROMPT}`。
- 每個 step 都必須包含一個 `time` 欄位，其中有下列子欄位：
  - `begin` 與 `end`，格式為 `yyyy-MM-dd HH:mm:ss`。
  - `taken`，格式為 `Xm Ys`。
- 每個 step 開始時，從本機的系統時鐘讀取 `time.begin` 的值。
  該 step 結束時，從同一個時鐘讀取 `time.end` 的值。
  在 PowerShell 中，用 `Get-Date -Format "yyyy-MM-dd HH:mm:ss"`。
  在 macOS/Linux 上，用 `date '+%Y-%m-%d %H:%M:%S'`。
- 不要用估計值或約略的時間戳記當作 `time.begin` 與 `time.end`。
  也不要在 step 之後從檔案的 metadata 取得這些時間戳記。
  從其他資料再次取得的時間是捏造的，因為你並沒有量到它。
- 以 `end - begin` 算出 `time.taken` 的值。
  例如：
  - 在 PowerShell 中，用 `$ts = (Get-Date $end) - (Get-Date $begin); "{0}m {1}s" -f [math]::Floor($ts.TotalMinutes), $ts.Seconds`。
  - 在 macOS/Linux 上，以 epoch 秒數算出兩個時間的差。
    然後把這個差寫成 `taken` 的格式。
- `time.taken` 只算滿的分鐘。
  不要四捨五入，因為四捨五入可能讓分鐘數偏大。
  不要把 `time.taken` 的值寫死。
  不要用估計值代替這個值。
- 如果 YAML 檔已經存在，只合併或更新相關的 `step_{number}` 群組。
