# Task 115 - 修正沙盒測試找到的 gen-skill 與 SKILL-tmp.md 問題

**Status**：尚未開始——gen-skill 寫出的 skill 有 2 個 issue 來自範本與 gen-skill，gen-skill 的 SKILL.md 有 18 處寫法不清楚或互相矛盾，都還沒改。
**Raised**：2026-11-13，[[Task 114]] 在沙盒裡測 gen-skill 時找到；使用者決定另開 task。
**Depends on**：—

## 1. 背景

[[Task 114]] 照 gen-skill 的 [README.md](../skill-groups/common/skills/gen-skill/README.md) 測試 gen-skill：在 scratchpad 的沙盒 workspace 以 `/gen-skill count-md-words` 寫了一個拋棄式 skill，再以 `/check-skill` 6 個 check 全做檢查它。
沙盒的 `common` 是真的 SkillsGestalt common group，只讀；另有 `sandbox` group 與暫用的 wiki，做完已經刪掉。

寫出的 skill 沒有缺少的標題，也沒有留下 placeholder，README 的要求通過了。
但寫出的 skill 在 SkillsGestalt 以外的 workspace 有兩個 issue，原因在範本與 gen-skill，而不在這一個 skill。
照範本寫出的每個 skill 都會帶著這些問題，所以本 task 改的是範本與 gen-skill。

## 2. 結論

—

## 3. 過程

### 2026-11-13 提出時的狀態

- check-skill 對拋棄式 skill count-md-words 報了 2 個 issue、8 個 recommendation；check 6 通過，準則 5.8 因為 script 是空檔而無法判定。
  表裡的行號是 2026-11-12 測試當時的，SKILL-tmp.md 與 gen-skill 之後的修改可能讓它們移動。

**表 1：拋棄式 skill 的 finding**

| Item | 種類 | 準則 | 問題 | 根因 |
| --- | --- | --- | --- | --- |
| 1.2 | issue | 1.16 | SKILL.md 連到 `skill-groups/common/rules/report-md-rules.md` 與 `run-data-rules.md`，在 SkillsGestalt 以外的 workspace 解析不到 | SKILL-tmp.md:72-73 的連結照抄 |
| 5.1 | issue | 5.2 | step 的指令用 `\` 分隔，bash 與 zsh 讀不懂 | gen-skill 的 `{WORKING_DIR}` 寫法（L200）用反斜線，SKILL-tmp.md:182 的指令照抄 |
| 1.1 | recommendation | 1.10 | README 說 Step 2 的報告只來自計數檔，其實 Step 2 也讀 `step_0.yaml` | 這一個 skill 自己的 |
| 1.3 | recommendation | 1.3 | CONFIGURATION 描述 prompt 給的 Markdown 檔，和 glossary 重複 | gen-skill L205 |
| 1.4 | recommendation | 1.5 | `run step 1` 或 `run step 2` 沒說接續哪一次執行的 Run Number、Working Dir 與 run record | SKILL-tmp.md:69-71 |
| 2.1 | recommendation | 2.6 | 通用的 skill 放在 `sandbox` group | 沙盒的安排，不算問題 |
| 3.1 | recommendation | 3.1 | description 說 each section，其實只數 `##` 的節 | 這一個 skill 自己的 |
| 3.2 | recommendation | 3.2 | description 沒提 step file 與 run record | 這一個 skill 自己的 |
| 4.1 | recommendation | 4.3 | 標題 "Write the MD Report" 和 term **MD report** 寫法不同 | 這一個 skill 自己的 |
| 4.2 | recommendation | 4.1 | data file 的名稱在 MUST FOLLOW 與 Step 2 各寫一次 | gen-skill L208 與 run-data-rules.md:56 要的位置不同 |

- 測試的 subagent 另外列出 gen-skill 的 SKILL.md 中不清楚、互相矛盾或做不到的寫法，見表 2；行號是 gen-skill SKILL.md 2026-11-12 的行號。

**表 2：gen-skill SKILL.md 的寫法問題**

| # | 行 | 問題 |
| --- | --- | --- |
| 1 | L29、L227、L275 | 「掃描 `{` 之後的大寫字母，只有 `{PLACEHOLDER}` 可以留著」會掃到 Run Number 的 `{N}`，它卻必須留下；check-skill 的掃描器要兩個字元以上，兩者不一致 |
| 2 | L200 | `{WORKING_DIR}` 寫成 `temp\<skill-name>\{yymmdd}.{N}`，把反斜線放進範本會執行的指令（SKILL-tmp.md:182） |
| 3 | Step 3（L194-225） | 沒說要改寫範本中只在一個環境成立的內容：`skill-groups/common/rules/...` 的連結（SKILL-tmp.md:72-73）、沒說接續哪一次執行的 `run step N`（SKILL-tmp.md:69-71），以及 "All the steps of the run use this file of raw data"（SKILL-tmp.md:188） |
| 4 | L144-146 | 選 skill group 的規則沒有使用者指定 group 或測試 group 的情況，也沒說要問使用者 |
| 5 | L147-148 | 先說不必登錄，又說新的 group 資料夾要另外加進 workspace 檔；沒說 gen-skill 要不要做，假設有 VS Code 的 workspace 檔，又說 VS Code 掃描 `<root>/<dir>/SKILL.md`，但 skill 其實在 `<root>/skills/<name>/SKILL.md` |
| 6 | L33 對 L55、L67 | 說 new skill directory 是唯一的輸出，但每次執行也寫 run record |
| 7 | 只有 L192 | 範本中寫給作者看的句子（SKILL-tmp.md:15-16、45-46、158）只靠一條通則拿掉；照字面執行會留在新的 SKILL.md 裡 |
| 8 | Step 3 | 沒說要改寫只有 `/{SKILL_NAME}` 的 Prompt 1 與 Prompt 2，它們因此看不出 Step 0 要解析的輸入 |
| 9 | L203 | "Edit the MUST FOLLOW section" 底下的子項目卻在改 CONFIGURATION 與 TERMINOLOGY |
| 10 | L205 | prompt 給的輸入檔沒有固定的路徑，它在 CONFIGURATION 的那一行因此成了定義（表 1 的 1.3） |
| 11 | L208 | 「把 Run Number 給 script」和 L200 與範本給 Working Dir 路徑的做法不同；data file 的名稱放 CONFIGURATION，run-data-rules.md:56 卻要它在 MUST FOLLOW（表 1 的 4.2） |
| 12 | L212 | 「Working Dir 裡的檔寫成 `step_3.yaml`」和 check-skill 準則 4.1 的範例相反 |
| 13 | L224-225 | 只為 skill 不產出的輸出拿掉 `Save MD report file`；沒有規則處理一個 step 不寫 skill 會產出的某種輸出，也沒有規則處理範本中需要判斷的 Step 2 遇到可以寫成程式的 step |
| 14 | L236-237 | "placeholder script file" 與 "placeholder file" 的 placeholder 和 glossary 的意思不同，也沒說空檔的內容長什麼樣 |
| 15 | L250-252 | `{COMMON_DIR}` 與 `{COMMON_PATH}` 用相對路徑，common group 在 workspace 以外時會變成 7 層與 10 層的 `../`，把只對這台電腦成立的路徑寫進 README |
| 16 | L259 | 「step 讀取或執行的、new skill directory 以外的每個檔」照字面讀，連 `config.yaml`、輸入檔與 `.venv` 的 Python 都算 |
| 17 | L75-76 對 L185 | 拿掉 STE 標記交給 Step 2，Step 2 自己卻只寫 "Copy the SKILL template" |
| 18 | L121 | 說 `wikiDir` 是 Step 1 的 MD report 目錄要用的，但 Step 1 從不使用它的值 |

## 4. 要做的

1. 先讀 gen-skill 的 [README.md](../skill-groups/common/skills/gen-skill/README.md) 與 [skill-writing.md](../skill-groups/common/rules/skill-writing.md)。
   [SKILL-tmp.md](../skill-groups/common/templates/SKILL-tmp.md) 與 README-tmp.md 是共用的範本，改了會影響每個照範本寫的 skill；先列出要改的地方，請使用者確認。
2. 照表 1 的根因改範本與 gen-skill：rules 的連結改用 `{skillGroups.common}`，`{WORKING_DIR}` 改用正斜線，`run step N` 說明接續哪一次執行。
3. 照表 2 改 gen-skill 的 SKILL.md，以及它的 README.md 與中文版。
4. 在沙盒裡再測一次：以 `/gen-skill` 寫一個拋棄式 skill，以 `/check-skill` 檢查它，再刪掉沙盒。

## 5. 驗證

- 沙盒裡重測的 skill 沒有缺少的標題，也沒有留下 placeholder，表 1 的兩個 issue 不再出現。
- 改過的範本與 skill，照各自的 README 跑檢查：`check_parity.py` 沒有 `[FAIL]`，`depends_on.py check` 都是 UNCHANGED。

## 6. 與其他 task 的關係

- [[Task 114]]：在它的第 5 步找到這些問題。
  它的表 6 也有 gen-skill 自己的 item，例如 Step 4 的空檔改叫 stub、Step 5 的指令改用正斜線；那些由 Task 114 修，本 task 從修好之後的 gen-skill 做起。

## 7. 知識

—

## 8. 日誌

### 2026-11-13

- 改名：countdell 上的 SkillsGestalt 已把 Task 103 到 113 用於別的事，所以本 task 由 Task 105 改成 Task 115；Task 104 到 107 依序改成 114 到 117，彼此的連結跟著改，內容不變。
  在這之前的 commit 以 `task 105:` 開頭。
- 提出：[[Task 114]] 在沙盒裡測 gen-skill 時找到，使用者決定另開 task。
