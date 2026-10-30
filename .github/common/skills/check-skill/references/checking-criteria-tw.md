# Checking Criteria

> [[README-tmp]]  `2026-10-30`  `43ace64a88a6`
> [[skill-writing]]  `2026-10-30`  `c7696bf6351a`

`check-skill` 這個 skill 所套用的判準。
**判準歸本檔案所有**——每一項 check 要找什麼，以及 issue 與 recommendation 的分界落在哪裡。
執行它們的 workflow 歸 `SKILL.md` 所有：哪一項 check 會跑、它讀什麼、它寫什麼。
要新增或修改某條判準，改的是本檔案，絕不是改某個 step。

只讀本次執行所選 check 對應的段落。
每一項 check 帶一個編號，其下每一條判準則以 `<check>.<n>` 定址——`1` 是整項 `Template alignment` check，`1.3` 只指它的第三條。

## Rules that apply to every check

- **把每一項 finding 分類為 issue 或 recommendation。**
  **issue** 違反了 checked skill 所承諾的契約——它的 template、它的 `config.yaml`、它自己的 description、它自己的字彙表，或必須接受它的那個 skill loader 的限制。
  **recommendation** 照現況能運作、但偏離參考基準；它永不阻擋，作者可以拒絕。
- **註明檔案與行號，並引述違規文字。**
  無法釘到行號的 finding 不可回報——絕不從某個 skill 的名稱、年紀或名聲去推斷違規。
- **絕不自行編造值。**
  每一項結論都要以該 step 所指名的輸入為依據。
  若從現有文字無法判斷，把它記為 `unknown` 並說明原因，而不是用猜的。
- **一項事實的 `region` 決定它是否被判定。**
  只判定 `body` region：出現在 `frontmatter` 或 `prompt_examples` 的字面路徑或平白行文，是在看不到 config 或字彙表的情況下寫的，屬於刻意為之。
  唯一的例外是主體*就是* frontmatter 的那項 check——`Description accuracy` 讀的正是 `description` 欄位本身。
- **來自 `SKILL.md` 以外檔案的事實不帶 region。**
  它改帶的是 `file`、`kind`（`script`、`reference`、`twin`、`skill config`、`doc`、`other`）以及 `backticked` / `fenced` / `commented` 旗標，而正是這些旗標在說明該路徑是被*使用*還是僅被*展示*。
  `readme_shape` 與 `dataflow` 事實屬於該 skill 的 `README.md`：它們的行號都是那份檔案的行，針對它們的 finding 引用的是 `README.md`。

## 1. Template alignment

**Why it exists** — 把 template 能回答的那一個問題——形狀——單獨拉出來，讓行文讀起來無懈可擊的 skill 中的結構缺陷依然會被回報。

兩份 template 是參考基準——`SKILL-tmp.md` 對應 `SKILL.md`，`README-tmp.md` 對應 `README.md`——**不是緊身衣**。
skill 可以正當地省略它不需要的 template 區段——不呼叫任何 API 的 skill 中的 `ADO_PAT` 條目、不執行任何腳本的 skill 中的 `.venv` 行。
只有在該 skill 明顯需要時，才回報缺少的區段。

1. **Frontmatter** — 它是否能解析為 YAML、`name` 是否與目錄名稱相符、是否有非空的 `description`，以及兩者是否都在 skill loader 所載明的限制之內（[VS Code: Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)）——`name` 最多 64 個字元，且只能由小寫字母、數字與連字號組成；`description` 最多 1024 個字元？
   請讀 `name_chars`、`name_charset_ok` 與 `description_chars`。
   **超過限制就是 issue，不論該 skill 其餘部分讀起來多好**：loader 會略過該 skill，既不報錯、也沒有任何診斷訊息，因此它永遠不會出現在可用的 skill 之中、根本無法被選取——而一份其餘部分都合乎格式的檔案，不會給其他任何判準留下可抓的東西。
   在這些限制之外，只檢查是否存在與結構——**絕不評斷 description 說了什麼**。
2. **Required headings** — `required_headings` 所列的每個標題是否都存在於 `SKILL.md`、且依 template 的順序排列，`readme_shape.required_headings` 所列的每個標題是否都存在於 `README.md`、且依 README template 的順序排列，並位於以該 skill 名稱為題的標題之下？
   那些是兩份 template 自己的標題，因此以它們為準判斷，絕不以記憶中的清單為準。
   請讀 `missing_headings`，以及 `readme_shape.missing_headings`、`heading_order_ok` 與 `title_is_skill_name`。
   只要各 step 倚賴了該 skill 從未定義的名詞——這幾乎總是如此——缺少 `# TERMINOLOGY` 或 `# DEDICATED TERMINOLOGY` 就是 issue；只有完全沒有自身領域詞彙的 skill 才可以省略 dedicated 那一節。
   對任何會寫出 MD report 或 YAML checkpoint 的 skill 而言，缺少 `# CONFIGURATION` 是 issue，因為它們的路徑沒有別的地方可放。
   **沒有 `README.md` 的 skill（`readme_shape.has_readme: false`）在這裡只算一項 issue，而不是缺幾節就算幾項**：它的 Dataflow、Step Purposes 與哪些檔案要隨它一起改，都沒有別的地方可放，check 6 也沒有東西可判定。
   對每一個 skill 而言，`README.md` 缺少 `## Dataflow` 都是 issue，理由見 check 6。
3. **Glossary placement** — `terms_defined_in_configuration` 是否指出某個由 `# CONFIGURATION` 加以定義、而非僅僅給出路徑的 term？
   `# CONFIGURATION` 承載具體值；字彙表擁有定義。
   `- **X** — <path>` 這樣的行放在那裡是正確的；`- **X** — <what X means>` 這樣的行則屬於 `# TERMINOLOGY` 或 `# DEDICATED TERMINOLOGY`。
4. **MUST FOLLOW contract** — 它是否宣告了逐步執行規則、它的 `run step N` 規則——選擇子的行為，或明確聲明本 skill 沒有這個選擇子——以及它的輸出契約（MD report / YAML checkpoint，或明確聲明兩者皆不產出）？
   no-forward-reference 規則與腳本與判斷之分的規則不在這裡宣告：[skill-writing.md](.github/common/rules/skill-writing.md) 為每一個 skill 收錄它們，判準 7 在各個 step 本身判定前者，判準 12 判定後者的回答。
5. **Step 0 - Warmup** — 它是否存在、是否命名為 `Warmup`，以及是否解析了後續 step 實際會用到的所有東西？
6. **Step numbering** — `## Step N` 標題是否從 0 開始連續，沒有重複或跳號？
7. **Forward references** — 是否有任何 step **依賴**排在它之後的 step？
   依照該參照的用途逐一判斷 `forward_references` 中的每一筆：為了控制流程而指名後方 step（`skip ahead when Step N found nothing`）是允許的，借用後方 step 的輸出則是 issue。
8. **Leftover placeholders** — `SKILL.md` 中，或從 `readme_shape.placeholder_tokens` 讀到的 `README.md` 中，是否還留著任何 `{PLACEHOLDER}` token，或從 `leftovers` 與 `readme_shape` 的 `old_placeholder_tokens` 讀到任何已停用寫法的 placeholder？
   從 template 遺留下來的 token 一律是 issue；該 step 只是在*展示*而非使用的 token 則不是——請讀 `backticked` 與 `fenced`，它們說明它是否位於 inline code 區段或 fenced 區塊之內。
   已停用寫法的 placeholder 不論是否只是展示，一律是 issue：修正方式是 `python {skillGroups.common}\scripts\placeholders.py convert <file>`，它會在該檔與其 twin 中轉換。
9. **Prompt Examples** — 是否至少有一個 `/` 叫用範例、在該 skill 遵守 `run step N` 的情況下是否有一個範例展示它，以及 workflow 是否真的會解析這些範例所示的內容？
10. **Step Purposes** — `README.md` 的 `## Step Purposes` 是否列出 `SKILL.md` 的每一個 `## Step N`，名稱與它的標題完全相同、順序也相同，每一項底下都縮排寫著它的 Purpose？
    請讀 `readme_shape.step_purposes`：`steps_missing`、`items_not_steps`、`items_without_purpose` 與 `order_ok`。
    漏掉或名稱不符的 step，或沒有 Purpose 的 step，都是 issue：Purpose 是 step 為何存在的唯一紀錄，而 [skill-writing.md](.github/common/rules/skill-writing.md) 把它放在那裡，不放在別處。
    也要判斷它寫了什麼：一條只是在重述該 step 的指示、而沒有說明該 step 為何要*獨立存在*的 Purpose 是 recommendation，因為 skill-writing.md 說那是終將偏離的第二份副本。
11. **執行時用不到的內容不留在 `SKILL.md`** — `SKILL.md` 是否還留著 `# Dataflow` 或 `# Steps at a Glance` 一節、`- **Purpose**:` 行，或介紹 Purpose 的那一段，又是否連到 `README.md`？
    請讀 `readme_shape.readme_content_in_skill_md`：`found` 與 `links_to_readme`。
    每一項都是 issue：每次執行都會載入整份 `SKILL.md`，而與 `README.md` 中那一份並存的第二份副本會與它偏離，一個連結則會把執行引進一份不含任何執行所需內容的檔案。
    修正方式是把內容移進 `README.md`，或在 `README.md` 已經有它時直接刪除。
12. **Files Each Step Uses** — `README.md` 的 `## Files Each Step Uses` 是否以一句粗體句回答「哪些 step 執行腳本」那條規則一次，並在它的樹中以每個 step 的標題指名每一個 step？
    請讀 `readme_shape.files_each_step_uses`：`answers_scripted_rule`、`steps_missing` 與 `items_not_steps`。
    漏掉或名稱不符的 step 是 issue：拿這棵樹去對照 Workflow 的讀者，不是找不到那個 step，就是找到另一個。
    缺少那句回答是 recommendation，因為各個 step 仍寫明了自己執行什麼。
13. **Tracked dependencies** — `README.md` 的 header quote 宣告的每一個檔案，是否都仍和記錄時一樣？
    請讀 `readme_shape.header_quote`：每一項都帶著 `depends_on.py check` 給它的狀態。
    `MISSING` 是 issue：那個連結指不到任何檔案，它宣告的依賴完全沒有被追蹤。
    `CHANGED`、`NO_RECORD` 或 `NOTHING_CITED` 是 recommendation：skill 所依賴的某個檔案，在有人確認 skill 依然成立之後改過，或從未被確認——修正方式是讀它改了什麼，讓 `SKILL.md` 與 `README.md` 跟著一致，再以 `depends_on.py record` 重新記錄。
    沒有 header quote 的 `README.md`，或 header quote 無法被 `depends_on.py` 讀取（`error`）的 `README.md`，是 issue：每一個 skill 至少都依賴它的兩份 template 與 skill-writing.md。
    絕不以肉眼判斷指紋；狀態由腳本決定。
14. **README 的 twin** — 當 `SKILL.md` 有繁體中文 twin 時（`readme_shape.skill_has_twin`），`README.md` 是否也有一份（`readme_shape.has_twin`）？
    缺少 `README-tw.md` 是 recommendation：[skill-writing.md](.github/common/rules/skill-writing.md) 要求它，但少了它，skill 照樣能執行。

## 2. Config conformance

**Why it exists** — 讓 workspace 的唯一事實來源真的可以被執行：一個本應來自 `config.yaml` 的路徑，在行文中讀起來一點問題也沒有，只有在有人刻意去找它時才會現形。

`config.yaml` 是 `wikiDir` 與 `skillGroups` 的唯一事實來源。
需要其中任一者的 skill 必須在 Step 0 解析它，而不是寫死。
**並非每一個字面路徑都是缺陷**——`checkpoints\`、`database\` 與 `packages\` 位於 workspace 內，以字面書寫是正確的；而像 `](.github/common/rules/report-md-rules.md)` 這樣的 Markdown 連結目標，是本專案自己的連結慣例：連結必須在磁碟上解析得到，因此它是刻意寫成字面的，永遠不是 finding。

本項 check 的主體是**整個 skill 目錄**，而不只是 `SKILL.md`。
判準 1-6 判定 `SKILL.md` 的 `config_shape` 事實；判準 7-8 则判定該目錄下每一份其他文字檔的 `dir_config_shape` 事實——各個腳本、各份 reference、繁體中文 twin，以及該 skill 自己的 `config.yaml`。
寫死在腳本裡的路徑，壞法與寫死在某個 step 裡的一模一樣，而一次執行中再也沒有別的環節會打開那些檔案。

1. **`wikiDir` resolution** — 若該 skill 會讀寫 wiki vault 中的任何東西，Step 0 是否有從 `config.yaml` 解析 `wikiDir`？
2. **Hardcoded wiki paths** — 是否有任何 body step 使用字面的 `wiki\<skill>\` 路徑而非 `{wikiDir}\<skill>\`？
   這是 issue：vault 根目錄是可設定的，且位於 workspace 之外，因此字面路徑會寫到錯誤的位置。
3. **Unresolved placeholders** — 該 skill 是否在任何地方使用了 `{wikiDir}`、`{vaultName}` 或 `{skillGroups.<group>}`，卻沒有在 Step 0 解析它？
   從未被解析的 placeholder 是 issue。
4. **`skillGroups` resolution** — 該 skill 是透過 `{skillGroups.<group>}` 而非字面的 `.github\...` 去取得自己的目錄或另一個 skill 的目錄嗎？
   寫死的 `.github\` 路徑在 skill 在群組之間搬動時就會壞掉。
5. **Absolute paths** — 是否有機器專屬的絕對路徑（例如 `C:\Users\...`）被寫死在 SKILL.md 中，而該處本應是 config 鍵或 workspace 相對路徑？
6. **Group placement** — 該 skill 是否位於其內容所隱含的 `skillGroups` 根目錄之下：與專案無關的放 `common`、專案專屬的放 `dedi`、匯入的第三方放 `external`？
7. **Hardcoded paths outside `SKILL.md`** — skill 目錄下的任何腳本、reference、twin 或其他檔案，是否寫死了字面 wiki 路徑、機器專屬的絕對路徑（`C:\Users\...`、`D:\...`）、UNC 分享（`\\host\share\...`）或字面的 `.github\` 路徑？
   請讀 `dir_config_shape.hardcoded_paths`；每一筆事實都帶有 `file`、`kind` 與 `line`。
   該檔案真的**使用**的路徑——預設值、常數、fallback——是 issue：它從 `SKILL.md` 看不見，所以沒有別的判準能觸及它。
   只是被**展示**的路徑不是 finding，而這由 `commented`、`fenced` 與 `backticked` 定誰——模組 docstring、`--help` 字串或 fenced 區塊中的用法範例是文件，而佔位用的主機名（`\\host\share`）即使這些旗標都是 false 也依然是文件。
8. **Site-specific values belong in the skill's own `config.yaml`** — 當 `dir_config_shape.has_own_config` 為 true 時，分享根目錄、主機、vault 路徑或實驗室專屬的目錄放在*那裡*是正確的，放在別處則是缺陷。
   一個自己指名這類路徑、而不是從該 config 讀取或以 CLI 參數接手的腳本，即使目前值是對的也是 issue：下一台機器需要改程式碼而不是改 config。
   若該 skill 沒有自己的 `config.yaml`，該值屬於 workspace 的 `config.yaml` 或屬於一個參數；請讀每個檔案的 `reads_config_yaml` 行號，來分辨哪些檔案是從 config 解析路徑、哪些是把路徑寫死的。

## 3. Description accuracy

**Why it exists** — 檢查那段在 skill 被選中之前唯一會被讀到、且任何結構性 check 都觸及不了的文字；形狀完美但 description 寫錯的 skill，根本從來不會被選上。

**description 是主張；workflow 才是事實依據。**

- **workflow 具有權威性。**
  當 description 與各 step 不一致時，錯的是 description——絕不回報說 workflow 需要改成符合 description。
- 判定**準確度與涵蓋度，絕不判定風格**。
  用字、語氣與句構是作者的裁量，判準 1.1 所強制的 1024 字元限制以內的長度也是。
  只有在 description 主張了 workflow 不做的事、或省略了 workflow 一定會做的事時，才回報 finding。
- `description` 是 skill *選取*階段唯一會被讀到的 `SKILL.md` 部分——本文要等到該 skill 被選中之後才會被讀。
  這裡的一項省略會讓使用者永遠選不到這個 skill，請依這個代價來衡量 finding 的份量。
- **同時**引述 description 的主張與與之矛盾或將其省略的那個 step。
- **修正絕不可讓 description 超過該限制。**
  補上未聲明的輸出或動作會讓它變長，而超過限制的 description 會付出判準 1.1 所說的代價——比它所修正的那項遺漏更嚴重的缺陷。
  沒有空間時，修正要指名該刪去什麼來騰出空間。

1. **Overstated** — description 是否主張了某項沒有任何 step 執行的輸入、動作或輸出？
   這是 issue：它會讓這個 skill 被選來做它做不到的工作。
2. **Unstated output** — 該 skill 是否總是寫出某個 description 從未提及的東西？
   請比對 MUST FOLLOW 契約所宣告的每一項輸出——MD report、YAML checkpoint、資料儲存、HTML 頁面。
3. **Unstated action** — 是否有某個 step 做了 description 省略的實質行為，例如寫入 ADO、連線到某台主機、觸發 pipeline、寄送郵件，或變更共用檔案？
4. **Stale** — description 是否仍在描述某個 step 早已改掉的行為，例如更名的輸出目錄或已移除的引數？
5. **Trigger coverage** — 一個用日常語言詢問這個 skill 所做之事的使用者，真的會匹配到這段 description 嗎？
   指出那些會匹配失敗的說法。

## 4. Terminology usage

**Why it exists** — 讓字彙表負起責任：一個 term 只有在行文真的用了它時才值得定義，而一次執行中沒有別的東西會把定義拿來與用法相比。

- 只判定行文。
  term 的小寫形式出現在**資料鍵**（`store_file`、`stored`）、**CLI 旗標**（`--share-root`）、**使用者可見字串**或**程式碼識別字**中，照現況就是正確的——絕不回報。
- 只有當變體所指與該 term **意義相同**時才算缺陷。
  先確認所指對象——同樣的字詞可能指的是不同的東西，那時把它們改成大寫反而會顛倒意思。

1. **Literal instead of term** — 某一節是否在已為某物定義 term 之處，仍直接指名原始產物（例如已定義 **YAML checkpoint** 卻寫 `process.yaml`）？
   引入該字面名稱的那一條字彙表條目保留它；其他每一處行文用法都應改用 term。
2. **Wrong term** — 某一節是否在應指甲 term 處用了乙 term（例如所指之物住在檔案*內部*，卻指名了目錄）？
   這是 issue，不是風格問題：它誤述了所指對象。
3. **Variant spelling** — 已定義的 term 是否被寫成不同的大小寫或形態（`store file` 對 **Store file**、`launched run` 對 **Launched run**）？
4. **Restated definition** — 某一節是否重新解釋某個 term 的意思，而不是直接使用它？
   定義歸字彙表所有；重述定義的 step 終將與它偏離。
5. **Unused term** — 是否有 term 被定義了，卻在字彙表之外從未使用？
   不是行文該用它，就是該把這個 term 刪掉。
6. **Heading consistency** — 表格欄位標頭與區段名稱是否使用了它們所指涉的 term？

## 5. Cross-platform compatibility

**Why it exists** — 在作者機器上能跑的指令，讀起來與到處都能跑的指令一模一樣，而一次執行中沒有任何東西會真的去執行這些指令，因此這是唯一會問它們能否在不同 shell 下存活的一關。

skill 本身、以及它與它的 Python 腳本所叫用的工具或指令，必須能在 Windows、macOS 與 Linux 上運行——否則就必須聲明它所假定的平台。

- 只判定 skill 實際**叫用**的指令，而非僅僅**展示**的指令。
  某個 step 叫 agent 去執行、位於 fenced 區塊或 inline code 區段中的指令才算在範圍內；被當作「不要這麼做」的範例而引用的指令則不算——請把 `backticked`、`fenced` 與前後行文一起讀。
- **已聲明的平台不算缺陷。**
  明說只跑單一平台的 skill——例如建立在 Outlook COM 自動化或 Windows 排程工作之上、並已明言如此的 skill——其 `powershell` 與 `cmd` 指令不予回報。
  判定的是未聲明的假定，絕不判定已聲明者。
- 嚴重度：當 skill 在三個平台之一上會直接失敗、卻未說明時，是 **issue**；當存在可攜的替代寫法、而現行寫法只是縮小了 skill 可運行的範圍時，是 **recommendation**。

1. **Shell commands in steps** — 某個 step 所執行的指令是否使用了平台專屬的內建指令（Windows 的 `copy`、`dir`、`type`、`del`、`move`；macOS 的 `open`、`pbcopy`、`osascript`），卻未指名其他平台上的對應寫法、或未聲明它假定的平台？
2. **Path separators in executable commands** — agent 必須執行的指令中是否帶有 `\` 分隔符？
   反斜線路徑在 Windows shell、批次檔與 config 值中是正確的，但在 bash/zsh 中會壞掉。
   行文中的路徑歸 `Config conformance` 判定——本判準只判定可執行指令中的路徑。
3. **Script subprocess use** — skill 所指名的 Python 腳本是否透過 `os.system`、`subprocess.run(..., shell=True)` 或平台專屬執行檔來開子行程，而其實用 `pathlib` 加上 `subprocess` 引數列表即可？
   `shell=True` 是 issue：它把腳本綁死在單一 shell 的引號規則與內建指令集上。
4. **Platform-specific Python APIs** — 腳本是否呼叫 `os.startfile`、`win32com`、`ctypes.windll`、AppleScript 或類似 API，卻沒有依平台分支、也未聲明平台需求？
5. **External tools assumed present** — skill 或其腳本是否假定某個並非三平台皆標準配備的工具存在（`powershell`、`pbcopy`、`xdg-open`、僅 GNU 版才有的 `sed`/`date` 旗標），卻未指明該需求，也未在存在時給出可攜的替代方案？

## 6. Dataflow

**Why it exists** — skill 的 Dataflow 是唯一一處能一眼看出每個 step 讀寫什麼的地方，因此讀者會讀它而不去讀各個 step；一次執行中沒有別的東西會拿這張圖去和各個 step 比對，於是一份與 step 脫節的 Dataflow，正好在被倚賴的地方誤導人。

Dataflow 是該 skill 之 `README.md` 的 `## Dataflow`，finding 引用的每一行都是那份檔案的行（`dataflow.file`）。
它以 [DFD.md](.github/common/references/DFD.md) 為準——它的資料種類、形狀、線條，以及任何 DFD 都要檢查的兩種缺陷——也以 `SKILL.md` 的各個 step 為準；它如何排列，由 README template 的 `## Dataflow` 示範。
留在 `SKILL.md` 的 Dataflow 由判準 1.11 回報，絕不屬於本 check。

- **step 才是實際執行的東西。**
  當圖與某個 step 對該 step 讀寫什麼的說法不一致時，要改的是圖——除非是 step 本身違反了這張圖要檢查的規則，例如某個 record 多了第二個寫入者，那時 finding 針對的是 step。
- **只有 step 在執行時讀寫的東西才是一條邊。**
  step 只是引用的文件——它遵循的規則檔、它指名的某一節——不是它讀取的資料，圖上沒有畫它也不是 finding。
- 嚴重度：當圖說了不實的事、或漏掉了實際會執行的東西——一個 step、一次讀、一次寫、一個寫入者——是 **issue**；只有畫法不對、但所說的沒有一件不實——顏色、圖例的一行——是 **recommendation**。

1. **Every step, named exactly** — Workflow 的每一個 `## Step N` 是否都是圖中的一個 step，名稱與它的標題完全相同、連編號一起；圖上又是否沒有把不是 step 的東西畫成 step？
   請讀 `steps_not_drawn` 與 `processes_not_steps`。
   漏掉或名稱不符的 step 是 issue：拿這張圖去對照 Workflow 的讀者，不是找不到那個 step，就是找到另一個。
2. **Shapes and lines** — Dataflow 是否畫成一張 mermaid 流程圖，圖下附有說明每種形狀與每種線代表什麼的圖例？
   每個節點是否都以它的種類在 DFD.md 中的形狀畫出——external input 是平行四邊形、one-run data 是旗形、record 是圓柱、step 是圓角方框（執行 RSDC system 程式的 step 則是雙框）、skill 之外的 role 是六角形？
   箭頭是否恰好在它的資料被寫進 record、或被轉成 record 的內容時才是藍色，又是否沒有任何實線箭頭直接連接兩份資料？
   請讀 `mermaid_blocks`、`nodes`、`edges`、`edges_between_data` 與 `legend_lines`。
   沒有圖的 Dataflow 是 issue，因為沒有東西可讀；形狀說錯了節點的種類也是 issue，因為讀者正是靠形狀得知這份資料是否活得比這次執行久；兩份資料之間的實線箭頭同樣是 issue，因為它畫出了沒有任何 step 搬動的資料移動。
   顏色或圖例不對是 recommendation。
3. **Agreement with the steps** — 圖上說每個 step 讀寫的東西，是否與該 step 自己那一節在執行時讀寫的相符？
   逐一拿每個 step 的那一節，去比對它的箭頭。
   不論哪一邊有缺口都是 issue：圖上漏掉的讀取，是沒人畫出來源的資料；漏掉的寫入，是沒人看得見寫入者的 record。
4. **One writer per record** — 每個 record 是否都恰好只有一個寫入者：Checkpoint Dir 中的每一份資料檔、YAML checkpoint 的每一個 `step_{N}` 群組、MD report 的每一節？
   請讀 `multi_writer_records` 與 `records_edited_in_turn`。
   較後的 step 不讀取就直接寫入的 record 是 issue，不論是圖上這樣畫、還是 step 真的這樣做：重跑其中一個，就會悄悄抹掉另一個的結果。
   較後的每個寫入者也讀取它的 record——雙向箭頭——是依序編輯，不算缺陷（DFD.md）；只需判斷重跑第一個寫入者，對它之後的編輯會怎樣，各 step 沒有說明就是 recommendation，例如第一個寫入者不先問就覆寫，而較後的 step 又沒有重新執行。
5. **No data without a source** — step 讀取的每一份資料，是否都是 external input、由 skill 之外的 role 提供，或由某個 step 寫出？
   請讀 `unsourced_data`。
   沒有任何東西提供的資料是 issue：沒有人負責產生它，要到它第一次缺席時才會被發現。
6. **No read of a later write** — 是否有任何 step 讀取較後 step 所寫的東西？
   請讀 `reads_of_later_writes`。
   每一筆都是 issue：那是發生在資料上的 forward reference，與判準 1.7 在各個 step 的行文中所判定的是同一種缺陷。
   也請讀 `records_read_as_found`：其中每一筆是第一個寫入者也讀取它的 record，所以在那個寫入者之前的 step 讀到的是它原本的樣子，掃描器因此把它們排除在 `reads_of_later_writes` 之外。
   請確認這份 record 在執行開始之前就已存在，例如執行會編輯的檔案，像它所處理的 skill；若是執行才建立它，那些 step 讀的就是一份還沒有人寫的 record，每一筆仍是 issue。
