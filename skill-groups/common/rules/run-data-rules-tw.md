# Run Data Rules

> [[ASD-STE100_ISSUE9.pdf]]  `2026-11-06`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-11-06`  `c612bdfa1ea7`

> 本檔案以 ASD-STE100 Simplified Technical English（STE）第 9 版寫成。
> 技術用字：agent、analysis、app、canonical skill invocation、checkpoint、clock、command、commit、data file、definition、design document、directory、efficiency、epoch、field、file、folder、format、git、handoff、handoff file、handoff files、heading、language、list、metadata、minute、model、noise、path、root、rounding、run、scratchpad、script、second、section、session、skill、temp dir、timestamp、title、untracked file、user、vault、wiki、wildcard、working data、working dir、workspace。

這些規則說明 skill 的一次執行把它的資料寫在哪裡，以及什麼時候移除這些資料。
一次執行寫兩種資料：

- **一次執行的 working data** 把每個 step 的輸出交給之後的 step。
  它也幫助這次執行完成它的工作，並在它停下之後接著做。
  執行結束後，沒有人、也沒有 skill 必須讀它。
- **最後的輸出**是執行結束後，人、另一個 skill 或之後的分析要讀的資料。

## The Number of a Run

- **每次執行都有一個編號 `{yymmdd}.{N}`。**
  `{yymmdd}` 是這次執行開始的日期。
  `{N}` 是這個 skill 在那一天的執行序號，從 1 開始。
- **Step 0 取得這個編號。**
  它在 `database\skill-runs\{skill}\` 中找出該日期最大的 `{N}`，再加 1。
  接著它立刻寫出這次執行的 run record，所以另一次執行不會取得同一個編號。
  這第一份 run record 寫著 `result: stopped` 與 `stopped_at: step_0`。
- **一次執行的 Working Dir、run record 與 handoff 檔使用同一個編號。**
  所以你可以在每個目錄中找到同一次執行的資料，而這些檔案不必互相引用。

## The Working Data of a Run

### The Working Dir

- **一次執行的 Working Dir 存放這次執行所有的 working data。**
  它是 workspace 根目錄下列兩個目錄之一：
  - **Temp Dir**，`temp\{skill}\{yymmdd}.{N}\`。
  - **Checkpoint Dir**，`checkpoints\{skill}\{yymmdd}.{N}\`。
- **這兩個目錄的結構相同。**
  每個目錄永遠是同一個。
  你不能在 `config.yaml` 中設定它。
  這兩個目錄都在 `.gitignore` 中，所以其中的檔案都不會進入 commit。
- **寫 skill 的人從這兩個目錄中選一個。**
  skill 的 CONFIGURATION 一節寫出它。
  skill 的執行不使用另一個目錄。
  在 CONFIGURATION 一節之後，skill 使用 Working Dir 這個名稱。
- **如果 Working Dir 不存在，就建立它。**

### Step Files

- **每個 step 把它的輸出寫進 Working Dir 中自己的 step 檔 `step_{N}.yaml`**，例如 `step_0.yaml` 與 `step_1.yaml`。
  之後的 step 從 step 檔讀取這些輸出，不再計算一次。
  另外，`run step N` 從 step N 重新開始一次執行時，也讀取它們。
- **step 檔只包含它那個 step 的輸出。**
  它不包含 step 的標題，也不包含時間。
  run record 包含它們。
- **一次執行的資料檔也放在它的 Working Dir 中。**
  每個 skill 都在自己的 MUST FOLLOW 一節中寫出每個資料檔的名稱。

### Temporary Files

- **把一次執行的每一個暫存檔都放進它的 Working Dir。**
  暫存檔是一次執行寫出、但不是 step 檔、資料檔或其 skill 的輸出的每一個項目。
  例如做測試或檢查的臨時 script，以及這次執行保留下來的指令輸出。
  其他例子是這次執行在寫出輸出之前使用的 JSON 檔，以及為了測試而做的目錄臨時副本。
- **Working Dir 中檔案的名稱說明檔案的功能**，例如 `facts.yaml`。
  名稱不以 skill 的名稱開頭，因為 Working Dir 的路徑已經寫出 skill 與這次執行。
  所以兩次執行不會用到同一個檔案。
- **step 執行的 script 也把它的暫存檔放進這次執行的 Working Dir。**
  step 把 Run Number 交給 script，由 script 組出 Working Dir 的路徑。
  這條規則適用於每一種語言。
  不要使用系統的暫存目錄，例如 Python 的 `tempfile` 或 Node 的 `os.tmpdir()`。
- **step 執行的 script 使用 skill 執行時所在 workspace 的根目錄。**
  如果 step 的指令給出根目錄，script 就使用那個根目錄。
  如果沒有，根目錄是從目前的目錄往上，最近一個有 `config.yaml`、且其中有 `skillGroups` 的目錄。
  script 不從它自己檔案的位置找出根目錄。
  workspace 可以使用另一個 workspace 的 skill group，這時 script 上方的 `config.yaml` 是另一個 workspace 的 `config.yaml`。
- **不在 skill 的執行中運作的 script，把它的暫存檔放進 `temp\`。**
  它的目錄名稱以 script 的名稱開頭，例如 `temp\publish-gestalt-index-{pid}\`。
  script 在停下之前移除這個目錄。

### The Removal of the Working Dir

- **skill 不移除 Working Dir，也不移除其中的檔案。**
  在完成工作之前就停下的執行，把它的檔案留在 Working Dir。
  這些檔案顯示出它做了多少工作。
- **`temp\` 與 `checkpoints\` 中的每個項目都可以在你想要的時候安全地手動移除。**
  移除一個項目時，寫出它的完整名稱。
  不要使用萬用字元，因為萬用字元也可能符合另一次執行的檔案。

## The Last Outputs

### The Run Record in `database\skill-runs\`

- **一次執行的 run record 是 `database\skill-runs\{skill}\{yymmdd}.{N}.yaml`。**
  它記下這次執行每個 step 使用的時間，以及執行該 step 的模型。
  所以在多次執行之後，你可以分析一個 skill 的效率。
  不要移除它。
- **run record 不引用 step 檔。**
  它和 Working Dir 有同一個編號。
- **run record 有下列欄位：**
  - `skill`：skill 的名稱。
  - `run`：這次執行的編號 `{yymmdd}.{N}`。
  - `prompt`：canonical skill invocation，也就是 [report-md-rules.md](report-md-rules.md) 中的 `{USER_PROMPT}`。
  - `result`：執行完成最後一個 step 時是 `completed`，在那之前是 `stopped`。
  - `stopped_at`：只在 `result` 是 `stopped` 時寫，是沒有完成的 step，例如 `step_3`。
- **step 把它的項目加進 run record 時，也重新寫出 `stopped_at`。**
  如果這個 step 完成了，而且不是最後一個 step，`stopped_at` 是下一個 step。
  如果執行在這個 step 停下，`stopped_at` 是這個 step。
  最後一個 step 寫出 `result: completed`，並移除 `stopped_at`。
  所以執行在最後一個 step 之前停下、沒有寫出結果時，它的 run record 會說出它停在哪一個 step。
  - `steps`：一份清單，每個開始過的 step 一個項目。
- **`steps` 的每個項目有下列欄位：**
  - `step`：step 的編號。
  - `title`：skill 定義中該 step 的標題，例如 `Warmup`。
  - `model`：執行這個 step 的 AI 模型。
  - `time`：`begin` 與 `end`，格式為 `yyyy-MM-dd HH:mm:ss`；以及 `taken`，格式為 `Xm Ys`。
- **每個 step 開始時，從本機的系統時鐘讀取 `time.begin` 的值。**
  該 step 結束時，從同一個時鐘讀取 `time.end` 的值。
  在 PowerShell 中，用 `Get-Date -Format "yyyy-MM-dd HH:mm:ss"`。
  在 macOS/Linux 上，用 `date '+%Y-%m-%d %H:%M:%S'`。
- **`time.begin` 與 `time.end` 不要使用估計值或大約的時間戳記。**
  也不要在 step 之後從檔案的 metadata 取得這些時間戳記。
  從其他資料重新取得的時間是錯的，因為你沒有量測它。
- **把 `time.taken` 的值算成 `end - begin`。**
  例如：
  - 在 PowerShell 中，用 `$ts = (Get-Date $end) - (Get-Date $begin); "{0}m {1}s" -f [math]::Floor($ts.TotalMinutes), $ts.Seconds`。
  - 在 macOS/Linux 上，以 epoch 秒數計算兩個時間的差。
    再把這個差用 `taken` 的格式寫出。
- **`time.taken` 只算完整的分鐘。**
  不要四捨五入，因為四捨五入可能讓分鐘數太大。
  不要把 `time.taken` 的值寫死。
  不要使用這個值的估計值。
- **`run step N` 重新開始一次執行時，把它做的 step 加進 `steps` 清單。**
  接著寫出新的 `result`。

### Handoff Files in `handoff\`

- **handoff 檔是一次執行為另一個 skill 產生的資料。**
  這次執行每次都重新產生它，由另一個 skill 讀取。
- **一次執行的 handoff 檔是 workspace 根目錄的 `handoff\{skill}\{yymmdd}.{N}.md`。**
  `{skill}` 是寫出這個檔案的 skill。
  每個 handoff 檔都是 Markdown 檔。
  這個目錄在 `.gitignore` 中。
- **寫出 handoff 檔的 skill，在自己的 MUST FOLLOW 一節中寫出它。**
  讀取這個檔案的 skill，寫出是哪個 skill 寫的。
- **讀取 handoff 檔的 skill，讀使用者指定的檔案。**
  使用者沒有指定時，它讀編號最大的檔案。
  它說明自己讀了哪個檔案。
- **skill 不移除 handoff 檔。**
  在你想要的時候手動移除它。

### Shared Data in `database\`

- **workspace 根目錄的 `database\` 包含許多 skill 使用、並在多次執行中累積的資料**，例如 `database\tags.yaml`。
  一次執行在這些資料中加上內容，或改變它。
  它不會每次都重新產生這些資料。
  一次執行每次為另一個 skill 重新產生的資料是 handoff 檔。
- **寫出 `database\` 中某個檔案的 skill，在自己的 MUST FOLLOW 一節中寫出這個檔案的名稱。**
- **不要移除 `database\` 中的資料。**
  這個目錄在 `.gitignore` 中。

### MD Reports in the Vault

- **一次執行的 MD report 放在 wiki vault 中，它的 skill 的資料夾裡。**
  它給人閱讀。
  [report-md-rules.md](report-md-rules.md) 說明怎麼寫它。
- **MD report 的 `Run record` 欄位寫出這次執行的 run record 的路徑。**

## Locations That You Must Not Use

- **不要使用 agent 的 scratchpad。**
  例如，Claude Code 的每個 session 都有自己的 scratchpad。
  另一個 session、另一個 agent 和 script 都找不到它。
- **不要使用系統的暫存目錄。**
  使用 Working Dir。
  有一個例外：不可以找到 workspace 檔案的測試，例如它的 `config.yaml`。
  這種測試在系統的暫存目錄中執行，因為那個目錄在 workspace 之外。
  測試停下時，script 移除這個目錄，發生錯誤之後也一樣。
- **不要把一次執行的資料放在 workspace 的根目錄。**
  執行寫在那裡的檔案是未追蹤的檔案，*但 git 不會忽略它*。
  所以它會在 `git status` 中顯示成雜訊。
  另外，如果你在 commit 之後使用 `git clean -fd`，它會移除這個檔案，而且不會先取得你的同意。
  同時，`git clean -fd` 會移除與它相鄰、屬於其他執行的所有檔案。
- **不要把一次執行的資料放在它的原始檔旁邊。**
  一次執行所有的 working data 都用 Working Dir。

## Directories That These Rules Do Not Control

**app 的 `temp\` 目錄是另一個目錄。**
app 可以有一個 `temp\` 目錄，放它的某個 stage 交給下一個 stage 的資料。
這個目錄是 app 的一部分。
app 的 design document 說明它。
這些規則不適用於它。

**另外，`__pycache__` 不是一次執行的暫存檔。**
當你在 script 所在的目錄執行它時，Python 會產生 `__pycache__` 作為副作用。
另外，git 會忽略它。
移除 `__pycache__` 是可選的。
