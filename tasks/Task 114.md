# Task 114 - 處理 check-skill 兩次檢查剩下的 finding 與 checker 缺陷，並重新檢查

**Status**：完成——表 11 的 9 個 item 照 Step 6 修好了，表 12 的 checker 缺陷都有了去處；使用者決定不再重新檢查就結案。
**Raised**：2026-11-12，修完 check-skill 兩次檢查的一部分 item 之後，使用者要把剩下的工作記成 task，讓別的 session 接著做。
**Depends on**：—

## 1. 背景

2026-11-12 以 check-skill 檢查了兩個 skill：

- run 261112.1：`/check-skill check-skill`，6 個 check 全做，❌，5 個 issue、5 個 recommendation，另有 8 個 checker 缺陷。
- run 261112.2：`/check-skill compile-skill`，只做 check 1 與 check 5，⚠️，0 個 issue、4 個 recommendation，另有 3 個 checker 缺陷。

下表是已經修好的 item。
commit 都只在本機的 `m1`，還不在 GitHub 上。

**表 1：已修好的 item**

| Run | Item | 修法 | Commit |
| --- | --- | --- | --- |
| 261112.1 | 6.1 | Dataflow 畫出 Step 3 讀的 skill group script | `9bca33c` |
| 261112.1 | 5.1 | Step 0 改用 SKILL-tmp.md 的 `{python}` 寫法，指令都以 `{python}` 開頭 | `996c89f` |
| 261112.2 | 1.1、1.2、5.1、5.2 | MUST FOLLOW 拿掉 skill-writing.md 已有的兩條規則；Step 2 的 Purpose 重寫；兩支 script 從 workspace 根目錄讀相對路徑 | `beaac7d` |

check-skill 不寫 MD report，兩次的報告只留在那次對話裡。
所以剩下的每一項都寫在第 3 章的表裡。
表裡的行號是檢查當時的，之後的修改可能讓它們移動。

## 2. 結論

- 表 3 的 10 個 checker 缺陷已修好，commit 是 `45fcaca`，只在本機的 `m1`，不在 GitHub 上；修法見表 5。
- 以修好的 checker 重跑 check-skill（run 261112.3）：check-skill ❌ 2·2、compile-skill ❌ 1·3、gen-skill ❌ 3·4，item 見表 6；Skills Dashboard 上兩列的 needs check 已清掉。
- 沙盒裡的 gen-skill 測試通過 README 的要求：沒有缺少的標題，也沒有留下 placeholder；它找到的 gen-skill 與範本的問題另開 [[Task 115]]。
- SkillsGestalt 的 `.venv` 裝了 `click` 8.4.2，requirements.txt 列的套件都裝齊了。
- 表 6 的 15 個 item 照 Step 6 修好了（`9631b6b`）；三個 skill 在 Skills Dashboard 上標著 needs check。
- 表 7 的 12 個 checker 缺陷修好了（`227ed73`）；修法見表 8。
- 第二次重新檢查（run 261113.1）：check-skill ❌ 1·2、compile-skill ❌ 1·4、gen-skill ⚠️ 0·1，item 見表 9。
- 表 9 的 9 個 item 照 Step 6 修好了（`b8ed7eb`）。
- 表 10 的第 2 到 7 項另開 [[Task 116]]。
- 最後一次重新檢查（run 261113.2）：check-skill ⚠️ 0·2、compile-skill ❌ 1·4、gen-skill ❌ 1·1，三列的 needs check 都清掉了；新的 item 見表 11，新的 checker 缺陷見表 12。
- 表 11 的 9 個 item 照 Step 6 修好了，gen-skill 6.1 選 (a)；commit 與這段紀錄是同一個，也只在本機的 `m1`。
- 表 12 的第 1、2、4、5 項記進 [[Task 116]] 的表 2，第 3 項已在 [[Task 115]] 表 2 的第 1 項。
- 使用者決定不再重新檢查就結案：Skills Dashboard 上 check-skill、compile-skill 與 gen-skill 又標著 needs check，留給 [[Task 116]] 修好 checker 之後的那次檢查。

## 3. 過程

### 2026-11-12 提出時的狀態

- run 261112.1 還有 8 個 item 沒處理：3 個 issue、5 個 recommendation，其中 4 個要使用者選選項。
  item 的編號只在那次報告裡有效；重跑 check-skill 會重新編號，要照新的報告指名。

**表 2：run 261112.1 剩下的 item**

| Item | 種類 | 準則 | 問題 | 報告的修法 |
| --- | --- | --- | --- | --- |
| 1.1 | recommendation | 1.3 | `# CONFIGURATION` 的 **Checked skill** 一行在下定義、沒有給值，又重複了 glossary 的 **checked skill** 與 **skill directory** | 換成給值的一行：**checked skill** 是 **skill directory** `{skillGroups.<group>}\skills\<skill>\`，Step 6 只為指名的 item 改它；中文版同一行跟著改 |
| 3.1 | recommendation | 3.5 | description 只說 check 5 看指令與 script 能不能在 Windows、macOS、Linux 執行，沒說它也找只有某個 agent 才有的工具 | description 改成 "run on Windows, macOS, Linux and any agent"，並把 "(`dashboard\skills.md` in the vault)" 縮成 "(`dashboard\skills.md`)"，共 1016 字元；中文版的 description 跟著改 |
| 4.1 | recommendation | 4.3 | Step 6 寫 "the checked skill's directory"，沒有用 **skill directory** | 改成 **skill directory**；和 1.1 是同一個根因 |
| 4.2 | recommendation | 4.4 | Step 6 又解釋一次 **needs check**，少了「整列」的條件，讀起來像只跑部分準則的 run 也會清掉標記，`update_dashboard.py` 並不會 | 改成 "The cells stay as the last check left them, and the row keeps its **needs check** mark until a run clears it."；中文版同一行跟著改 |
| 4.3 | recommendation，要選 | 4.3 | glossary 與 3 行內文寫 **Run record**，另外 11 行內文寫 run record | (a) 11 行內文改成 Run record；(b) 4 個 **Run record** 改成 **run record**；報告建議 (b)；表 3 的第 9 項修好之後，這一項應該不會再出現 |
| 6.2 | issue，要選 | 6.2 | Dataflow 把 facts file 畫成 one-run data，但它留在 `temp/check-skill/{yymmdd}.{N}/` | (a) 改畫成 record，6 個箭頭改藍，README 與中文版各改 6 行；(b) 改準則 6.2，允許這種畫法；報告建議 (a) |
| 6.3 | issue，要選 | 6.3 | Step 0 與 Step 1 都解析 skill 名稱、都回報找不到的名稱，圖只畫了 Step 1 讀 checked skill | (a) 刪掉 Step 0 那一行與中文版的同一行；(b) 兩個都留，補畫 `CHECKED --> S0`，並在 Step 0 的樹加一行；報告建議 (a) |
| 6.4 | issue，要選 | 6.3 | Step 0 會等使用者打 skill 名稱，但沒有箭頭把它帶進 Step 0 | (a) 當成 Answer 畫，加 `ANSWERS --> S0`，index 37 與 38 已經用掉，所以它是 39；(b) 把它算進 Prompt，只改圖例一行；報告建議 (b) |

- 兩次 run 共報了 11 個 checker 缺陷；其中兩個是同一個，所以下表有 10 列。
  checker 缺陷是 check-skill 自己的問題，Step 6 不修，要另外交代。

**表 3：checker 缺陷**

| # | 在哪裡 | 缺陷 | Run |
| --- | --- | --- | --- |
| 1 | `scan_skill.py:277` | term 的 pattern 以 `(?![\w-])` 結尾，複數形永遠比對不到：`unused_terms` 列出 **Step file**，其實 SKILL.md 寫的是 "step files" | 261112.1 |
| 2 | `scan_skill.py:272` | 把定義裡加了反引號的檔名當成 term 指的東西：skill directory、region、issue、verdict、checker defect 得到 112 個沒有意義的 `literal_uses` | 261112.1 |
| 3 | `scan_skill.py:111` | `SKIP_DIRS`（`__pycache__`、`.git`、`.venv`、`node_modules`、`temp`）跳過的檔案沒有列在 `skipped`，SKILL.md 卻說 scan 列出每個跳過的檔案 | 261112.1 |
| 4 | `scan_skill.py:34` | `STEP_REF` 把每個 `Step N` 都當成受檢 skill 的 step：compile-skill 的 "compile SOP Step 2" 被列成 forward reference | 261112.2 |
| 5 | `scan_skill.py:51` 與 `:885` | `NAMED_SCRIPT` 把 SKILL.md 裡每個 `*.py` 名稱都當成 skill 自己的 script，又只跟 `scripts/*.py` 比：`scripts_named_but_missing` 列出 compile-skill 的 `main.py`、`skill.py`，與 check-skill 的 `depends_on.py` | 261112.1、261112.2 |
| 6 | check-skill SKILL.md，Step 3 的 Inputs 表 | check 1 只拿到 `template_shape`、`readme_shape`、`terminology`，準則 1.8 卻讀 `leftovers`；也沒有準則讀 `leftovers` 的 `broken_github_links`、`scripts_named_but_missing`、`scripts_on_disk_not_named`，掃到的失效連結與缺少的 script 沒人判 | 261112.1、261112.2 |
| 7 | `checking-criteria.md:63` | 準則 1.8 給的修法指令 `python {skillGroups.common}\scripts\placeholders.py convert <file>` 用 `\` 分隔，bash 與 zsh 會當成跳脫字元，又用不帶路徑的 `python`；check 5 的輸入不含 references，所以沒有 check 判 reference 給 agent 執行的指令 | 261112.1 |
| 8 | `checking-criteria.md:232` | 照字面讀 "A gap either way is an issue"，連 step 讀回自己的輸出、每個在對話裡的顯示都算進去；那次 run 是照準則的理由判的 | 261112.1 |
| 9 | `checking-criteria.md:162` | 範例把 **Store file** 的小寫 `store file` 算成變體，但 SKILL-tmp.md 寫 **Run record** 與 "the run record"，所以照範本寫的每個 skill 都會得到表 2 的 4.3 那種 item | 261112.1 |
| 10 | check-skill SKILL.md 的連結規則 | 只列 SKILL.md 與 check 2 的 finding 指到的 script、reference、config，漏了 check 1 與 check 6 會引用的 README.md，以及 check 5 會引用的 script | 261112.1 |

- run 261112.2 只做了 check 1 與 check 5，下表的三個觀察屬於沒做的 check 3、4、6，還沒判定。

**表 4：compile-skill 沒判定的觀察**

| # | 在哪裡 | 觀察 |
| --- | --- | --- |
| (a) | compile-skill SKILL.md 的 **Step file** | 定義寫成在 "a skill's per-run checkpoint directory"，SKILL-tmp.md 則放在 Working Dir；這個 skill 不寫 step file，只在 MUST FOLLOW 用到複數形 |
| (b) | compile-skill SKILL.md，MUST FOLLOW 的 run-data-rules 那一條 | 說要照 run-data-rules.md 處理 "the Working Dir of a run"，但這個 skill 沒有 Working Dir，glossary 也沒有這個詞 |
| (c) | compile-skill README.md，Files Each Step Uses 的粗體句 | 說 Step 0、2、4 不跑 script，但 Step 4 會跑 Compiled Script，`run step 2` 時 Step 2 也會再跑 `scan_source.py` |

- SkillsGestalt 的 `.venv` 沒有 `click`，compile-skill 編出來的 script 在這裡跑不起來；[requirements.txt](../skill-groups/common/requirements.txt) 已經列了 `click==8.4.2`。
- gen-skill 在 `55046b5` 改了 Step 0、Step 3 與 Step 5，它的 [README.md](../skill-groups/common/skills/gen-skill/README.md) 列的兩個檢查還沒跑：`/check-skill gen-skill`，與寫一個拋棄式 skill 的 `/gen-skill`。

### 2026-11-12 修表 3 的 checker 缺陷

- 改 check-skill 之前，先用改之前的 `scan_skill.py` 掃描 check-skill、compile-skill、gen-skill、asd-ste，留下比對的基準。
- 每一項的修法如下表；check-skill 的 `literal_uses` 從 117 個降到 0，compile-skill 的 "**compile SOP** Step 2" 不再算成 forward reference，`depends_on.py` 不再算成找不到的 script。

**表 5：checker 缺陷的修法**

| # | 修法 | 改的檔 |
| --- | --- | --- |
| 1 | term 的比對也接受複數形，字首大小寫不同也算用了那個 term | `scan_skill.py`、SKILL.md Step 2 第 7 項 |
| 2 | 只有定義開頭的檔名算是 term 指的檔案 | `scan_skill.py`、SKILL.md Step 2 第 7 項 |
| 3 | 不進去的目錄列在 `skipped`，一個目錄一筆 | `scan_skill.py`、SKILL.md Step 2 第 4 項 |
| 4 | 粗體名稱或 code span 加一個空格之後的 `Step N` 列在 `other_document_steps`，不算 forward reference | `scan_skill.py`、SKILL.md Step 2 第 2 項 |
| 5 | skill 的 script 包括直接放在 skill directory 裡的；skill group 的 `scripts/` 裡有的不算找不到 | `scan_skill.py`、SKILL.md Step 2 第 5 項、README 的 Dataflow 與 Files Each Step Uses |
| 6 | check 1 的輸入加上 `leftovers`；新增準則 1.16，判失效連結、找不到的 script 與沒有 step 指名的 script | SKILL.md Step 3、`checking-criteria.md` |
| 7 | 1.8 的指令改成 `{python} {skillGroups.common}/scripts/placeholders.py convert <file>`；check 5 也判 reference 給 agent 執行的指令 | `checking-criteria.md`、SKILL.md Step 3、README 的 Files Each Step Uses |
| 8 | 6.3 的缺口不包括 step 讀回自己寫的東西，也不包括只在對話中顯示的東西 | `checking-criteria.md` |
| 9 | 4.3 的範例改成 `md report` 對 **MD report**；字首與複數形不算變體 | `checking-criteria.md` |
| 10 | 連結規則加上 README.md，以及 finding 指名的任何 script、reference 或 config 檔 | SKILL.md 的 MUST FOLLOW |

- README 的 Dataflow 加了 `GSCRIPTS --> S2`，排在最後、黑色，所以藍色箭頭的編號都沒變。
- 三份 twin 經 chinese run 261112.25 到 261112.27 更新，parity 與 verify 都是 0 failure；CHANGES.md 加了一條。
- README 列的檢查：掃描 asd-ste、gen-skill、check-skill，README 沒有缺少的標題，header quote 都是 UNCHANGED；md-style 沒有改動。

### 2026-11-12 重新檢查

- 以修好的 checker 跑 `/check-skill check-skill, compile-skill, gen-skill`，6 個 check 全做（run 261112.3，subagent 跑 Steps 0 到 5）。
  總結是 check-skill ❌ 2 個 issue、2 個 recommendation，compile-skill ❌ 1、3，gen-skill ❌ 3、4。
  Skills Dashboard 上 check-skill 與 compile-skill 的 needs check 已清掉，gen-skill 多了一列。
- 表 2 再出現的有 1.1、4.2、6.2、6.4（這次的編號是 1.1、4.1、6.2、6.1）；4.3 沒再出現，因為表 3 的第 9 項修好了；3.1、4.1、6.3 這次判為沒問題。
- 要選選項的是 check-skill 6.1、6.2，以及 gen-skill 4.2、5.2、6.1。
  check-skill 6.2(b) 要改 README-tmp.md，gen-skill 5.2(a) 要改 `depends_on.py`，都在受檢的 skill 以外，Step 6 改不到。

**表 6：run 261112.3 的 item**

| Skill | Item | 種類 | 問題 | 報告的修法 |
| --- | --- | --- | --- | --- |
| check-skill | 1.1 | recommendation | CONFIGURATION 的 **Checked skill** 一行沒有給位置，又重複 glossary 的規則 | 換成指向 **skill directory** `{skillGroups[<group>]}\skills\<skill-name>\` 的一行；和 4.1 是同一個根因 |
| check-skill | 4.1 | recommendation | Step 6 又解釋一次 **needs check**，而且少了「整列」 | 刪掉 Step 6 那一行，與中文版的同一行 |
| check-skill | 6.1 | issue，要選 | Step 0 會等使用者打 skill 名稱，圖上沒有它的來源 | (a) 畫成 Answers，加 `ANSWERS --> S0` 並改藍；(b) 把回覆算進 Prompt，只改圖例一行；報告建議 (b) |
| check-skill | 6.2 | issue，要選 | facts file 留在 Working Dir，卻畫成 one-run data | (a) 改畫成 record，`S2 --> FACTS` 改藍，圖例改 3 行；(b) 改 README-tmp.md 與準則 6.4；報告建議 (a) |
| compile-skill | 4.1 | recommendation | Step 0 寫 `skill.py`，term 是 **Compiled Script** | 改成 **Compiled Script** |
| compile-skill | 6.1 | issue | Step 0 會問使用者三件事，圖上沒有答案進 Step 0 | 加 `ANSWERS --> S0`（黑色），圖例的 Answers 加上 Step 0 的三個回覆 |
| compile-skill | 6.2 | recommendation | Step 1 與 Step 3 執行 SkillCompiler 的程式，卻畫成圓角框 | 改成雙邊框，圖例加一句 |
| compile-skill | 6.3 | recommendation | 同一份 fingerprint 離開 Step 1 是黑色、進 Step 2 是藍色 | 箭頭 8 也改藍 |
| gen-skill | 3.1 | recommendation | description 沒提每次執行都寫的 run record | description 結尾加 "Every run writes its run record." |
| gen-skill | 3.2 | recommendation | description 沒說 workflow 是從 prompt 上面的對話推出來的 | 改成 "generates the workflow it infers from the conversation above the prompt by replacing every placeholder" |
| gen-skill | 4.1 | recommendation | Step 2 的標題寫 Template，term 是 **SKILL template** | 改名為 "Step 2 - Copy the SKILL Template"，README 與中文版跟著改 |
| gen-skill | 4.2 | issue，要選 | placeholder 同時指範本裡的 token，與 Step 4 建立的空檔 | (a) Step 4 的檔改叫 stub；(b) 另立 term **placeholder file**；報告建議 (a) |
| gen-skill | 5.1 | issue | Step 5 的指令用 `\` 分隔，bash 與 zsh 會把它吃掉 | 改成正斜線 |
| gen-skill | 5.2 | recommendation，要選 | `depends_on.py` 從目前的目錄讀 README 的路徑 | (a) 改 `depends_on.py`，從 workspace 根目錄讀；(b) Step 5 給 README 的絕對路徑；報告建議 (b) |
| gen-skill | 6.1 | issue，要選 | Step 6 畫了 chinese skill 的 commit，卻沒畫它讀寫的 keep-English list | (a) 畫出 keep-English list；(b) 兩個都不畫；報告建議 (a) |

- 在 scratchpad 的沙盒 workspace（`common` 只讀，另有 `sandbox` group 與暫用的 wiki）以 `/gen-skill count-md-words` 寫了一個拋棄式 skill，再以 `/check-skill` 6 個 check 全做檢查它；沒有寫到沙盒以外，做完已刪掉沙盒。
  沒有缺少的標題，也沒有留下 placeholder，只剩 Run Number 的 `{N}`。
  check-skill 對它報了 2 個 issue、8 個 recommendation；2 個 issue 都來自範本與 gen-skill：SKILL-tmp.md 的 `skill-groups/common/rules/...` 連結只在 SkillsGestalt 解析得到，gen-skill 的 `{WORKING_DIR}` 用反斜線，讓指令在 macOS 與 Linux 上失敗。
  測試的 subagent 另外列出 gen-skill SKILL.md 18 處不清楚或互相矛盾的寫法，例如它要求掃描 `{` 之後的大寫字母，卻會掃到必須留下的 `{N}`。
- 兩次重跑也找到新的 checker 缺陷，見表 7。

**表 7：重新檢查時找到的 checker 缺陷**

| # | 缺陷 |
| --- | --- |
| 1 | 準則 6.2 說雙邊框是 DFD.md 給的形狀，DFD.md 卻沒有；只有 gen-rsdc-skill 定義它 |
| 2 | terminology 的 fact 沒有 SKILL.md 說每個 fact 都有的 `backticked`、`fenced`、`line_text` |
| 3 | check 4 說它比對定義與用法，卻沒有準則這麼做；SKILL.md 說 facts file 是每個 check 都讀的輸入，Step 3 卻說 check 3 與 check 5 不讀 fact group |
| 4 | 沒有準則比對 `# TERMINOLOGY` 的定義與範本，所以 compile-skill 的 **Step file** 定義沒人看 |
| 5 | `scan_skill.py` 會給 `templates\` 底下的檔 kind `template`，SKILL.md 與準則都沒列這種 kind |
| 6 | 準則 1.3 沒有給 CONFIGURATION 裡的定義一個嚴重度 |
| 7 | DFD.md 的顏色規則沒涵蓋：一份 one-run data 之後被另一個 step 變成 record 的內容 |
| 8 | `ABS_PATH` 只認磁碟代號開頭的路徑，macOS 與 Linux 的絕對路徑不算 fact |
| 9 | 行數以 `split("\n")` 計算，結尾有換行的檔多算一行 |
| 10 | 準則 4.1 的範例 `step_1.yaml` 與 SKILL-tmp.md、gen-skill 要 Working Dir 裡的檔寫成 `step_3.yaml` 的做法相反 |
| 11 | 範本的 "run Step N" 在每個照範本寫的 skill 都被算成 **`run step N`** 的變體 |
| 12 | `update_dashboard.py` 為 macOS 的路徑產生 `vscode://file//private/...`，多一個斜線，還沒驗證 VS Code 開不開得了 |

### 2026-11-13 照 Step 6 修表 6

- 表 6 的 15 個 item 全部照報告的修法修了，有選項的照報告的建議，接在 run 261112.3 之後；run record 記了 Step 6。
  - check-skill：SKILL.md 的 1.1、4.1，README.md 的 6.1(b)、6.2(a)；facts file 改畫成 record。
  - compile-skill：SKILL.md 的 4.1，README.md 的 6.1、6.2、6.3；Step 1 與 Step 3 畫成雙邊框，check-skill 的掃描器也把雙邊框讀成 step。
  - gen-skill：description 的 3.1、3.2，Step 2 改名為 "Step 2 - Copy the SKILL Template"（README 的三處跟著改），Step 4 的空檔改叫 stub，Step 5 的指令改用正斜線並給 README 的絕對路徑，README 的 Dataflow 畫出 keep-English list。
- 六份 twin 經 chinese run 261113.1 到 261113.6 更新，parity 與 verify 都是 0 failure；剩下的 warning 都在這次沒改的句子裡。
- 檢查：三個 skill 的 README 沒有缺少的 step，Dataflow 沒有沒畫的 step，header quote 都是 UNCHANGED；md-style 沒有改動。
- Skills Dashboard 上三個 skill 都標了 needs check。

### 2026-11-13 修表 7 的 checker 缺陷

- 12 項都在 check-skill 裡修，沒有改共用的 DFD.md 與 SKILL-tmp.md；每一項的修法如下表。

**表 8：表 7 的修法**

| # | 修法 | 改的檔 |
| --- | --- | --- |
| 1 | 準則 6.2 說雙邊框不在 DFD.md 裡，由 gen-rsdc-skill 畫 | `checking-criteria.md` |
| 2 | terminology 的每一處使用都帶 `backticked`、`fenced` 與 `line_text` | `scan_skill.py`、SKILL.md Step 2 第 7 項 |
| 3 | check 4 的 Why it exists 改成它真正做的事；facts file 是 check 1、2、4 與 6 的輸入 | `checking-criteria.md`、SKILL.md 的 DEDICATED TERMINOLOGY |
| 4 | 新增準則 1.17，以新的 `shared_terms` 比對 `# TERMINOLOGY` 的定義與範本的定義 | `scan_skill.py`、`checking-criteria.md`、SKILL.md Step 2 第 7 項、README |
| 5 | file 的 kind 加上 `template` | SKILL.md Step 2 第 4 項、`checking-criteria.md` |
| 6 | 準則 1.3：CONFIGURATION 裡的定義是 recommendation | `checking-criteria.md` |
| 7 | 準則 6.2：照 DFD.md 的 Query 例子，資料繼續進入 record 的箭頭是藍色，中途經過旗形也一樣，停在 step 或只控制 step 的是黑色 | `checking-criteria.md` |
| 8 | 絕對路徑也包括 `/Users/<name>`、`/home/<name>`、`/private/...`、`/Volumes/...`，以及爬進這些目錄的 `../` 路徑 | `scan_skill.py`、SKILL.md Step 2 第 3 項、準則 2.5 與 2.7 |
| 9 | 行數以 `splitlines()` 計算，結尾的換行不再多算一行 | `scan_skill.py` |
| 10 | 準則 4.1 的範例改成 `step_{N}.yaml`；step 以名稱存自己的 step file 不算 | `checking-criteria.md` |
| 11 | 標籤加了反引號的 term 只在 inline code 或 fenced 區塊裡比對 | `scan_skill.py`、SKILL.md Step 2 第 7 項 |
| 12 | `vscode://file/` 後面只有一個斜線 | `update_dashboard.py` |

- 改之前與改之後掃描 check-skill、compile-skill、gen-skill、asd-ste 比對：行數都少一行；範本的 "run Step N" 不再算成變體；四個 skill 都有幾個 `# TERMINOLOGY` 的定義和範本用字不同，由準則 1.17 判斷意思是否相同。
- 三份 twin 經 chinese run 261113.7 到 261113.9 更新，parity 與 verify 都是 0 failure；CHANGES.md 加了 2026-11-13 這一條。
- README 列的檢查：掃描 asd-ste、gen-skill、check-skill，README 沒有缺少的標題，header quote 都是 UNCHANGED；md-style 沒有改動。

### 2026-11-13 第二次重新檢查

- 以修好的 checker 跑 `/check-skill check-skill, compile-skill, gen-skill`，6 個 check 全做（run 261113.1，subagent 跑 Steps 0 到 5）。
  check-skill ❌ 1 個 issue、2 個 recommendation，compile-skill ❌ 1、4，gen-skill ⚠️ 0、1；三列的 needs check 都清掉了。
- 報告指出表 8 第 7 項我加的那一句和 DFD.md 的 Query 例子矛盾：DFD.md 讓同一個 Query 進入 record 的箭頭是藍色，停在 Search 的箭頭是黑色，那一句卻讓載著它的每個箭頭都是藍色，因此有 6 個箭頭的顏色無法判定。
  已改成照 DFD.md 的例子判斷；這 6 個箭頭照現在畫的黑色是對的，不必改。
  中文版由 chinese run 261113.10 重做，它取代 261113.9。

**表 9：run 261113.1 的 item**

| Skill | Item | 種類 | 問題 | 報告的修法 |
| --- | --- | --- | --- | --- |
| check-skill | 4.1 | recommendation | Step 6 說 "needing a re-check"，term 是 **needs check** | 改成 "set the skill's needs check mark on the dashboard" |
| check-skill | 6.1 | issue | Step 2 讀 Step 0 給的 Run Number 與 template 的路徑，圖上沒有從 Run settings 來的箭頭 | 加 `SETTINGS --> S2`，黑色 |
| check-skill | 6.2 | recommendation | facts file 改成 record 之後，把資料帶進 Step 2 的箭頭仍是黑色 | 箭頭 9 與 11 到 14 改藍，圖例改兩行 |
| compile-skill | 1.1 | recommendation | **Step file** 的定義放在 checkpoint 目錄，範本放在 Working Dir（準則 1.17） | 改成範本的意思 |
| compile-skill | 3.1 | issue，要選 | description 說 skill.py 是唯一的輸出，但 Step 4 的證明執行會寫出被證明的 step 所寫的東西 | (a) 寫出證明執行會寫的東西，刪掉開頭一句騰出字數；(b) 只把說法縮小；報告建議 (a) |
| compile-skill | 4.1 | recommendation | Step 2 又解釋一次 **handoff steps**，和 glossary 的定義不同 | 刪掉那段解釋 |
| compile-skill | 6.1 | recommendation | `USER --> ANSWERS` 是黑色，但 Answers 會成為 Compiled Script 的內容 | 箭頭 1 改藍 |
| compile-skill | 6.2 | recommendation | 圖上的 Resolved paths 沒有 `--force`，Step 2 卻要看它 | 旗形改名為 "Resolved paths and --force"，圖例跟著改 |
| gen-skill | 4.1 | recommendation | Step 2 的標題寫成 SKILL Template，term 是 **SKILL template** | 改成 "Step 2 - Copy the SKILL template"，共 8 處 |

**表 10：第二次重新檢查找到的 checker 缺陷**

| # | 缺陷 | 狀態 |
| --- | --- | --- |
| 1 | 準則 6.2 新加的那一句和 DFD.md 的 Query 例子矛盾 | 已改正 |
| 2 | 準則 3.2 只拿 MUST FOLLOW 宣告的輸出比，沒拿 step 實際寫的東西比 | 還沒改 |
| 3 | 準則 6.3 沒說 Step 0 給的值只用來放檔或找檔時，算不算讀取 | 還沒改 |
| 4 | 沒有準則檢查 step 用到、glossary 卻沒定義的名詞，skill-writing.md 卻要求每個這種名詞都有定義 | 還沒改 |
| 5 | check 3 說它不讀 fact group，可是判 description 的長度要用 `description_chars` | 還沒改 |
| 6 | `scan_skill.py` 把 Python 字串裡跳脫的反斜線認成 UNC 路徑，而且不在 Markdown 以外的檔案裡找 code span | 還沒改 |
| 7 | `scan_skill.py` 把 `{PLACEHOLDER}` token 算成 term placeholder 的變體 | 還沒改 |

### 2026-11-13 照 Step 6 修表 9

- 表 9 的 9 個 item 全部照報告的修法修了，compile-skill 3.1 照報告的建議選 (a)，接在 run 261113.1 之後；run record 記了 Step 6。
  - check-skill：Step 6 改用 **needs check**；README 加了 `SETTINGS --> S2`，帶資料進 facts file 的 5 個箭頭改藍，圖例改兩行。
  - compile-skill：**Step file** 改成範本的意思；description 寫明證明執行會寫的東西，刪掉 "It has no design of its own"，共 1015 字元；Step 2 不再重新解釋 **handoff steps**；README 的 `USER --> ANSWERS` 改藍，旗形改名為 "Resolved paths and --force"。
  - gen-skill：Step 2 的標題改為 "Step 2 - Copy the SKILL template"，README 的三處跟著改。
- 六份 twin 經 chinese run 261113.11 到 261113.16 更新，parity 與 verify 都是 0 failure。
- 檢查：四個 skill 的 README 沒有缺少的 step，Dataflow 沒有沒畫的 step，header quote 都是 UNCHANGED；md-style 沒有改動。
- Skills Dashboard 上三個 skill 都標了 needs check。
- 表 10 的第 2 到 7 項記在 [[Task 116]]。

### 2026-11-13 最後一次重新檢查

- 以 `/check-skill check-skill, compile-skill, gen-skill` 6 個 check 全做（run 261113.2，subagent 跑 Steps 0 到 5）。
  check-skill ⚠️ 0 個 issue、2 個 recommendation，compile-skill ❌ 1、4，gen-skill ❌ 1、1；三列的 needs check 都清掉了。
- 上一輪的 item 都沒有再出現；這一輪的 item 是新的判斷，多半是又解釋一次的定義、description 的說法，與 Dataflow 漏畫的讀取。

**表 11：run 261113.2 的 item**

| Skill | Item | 種類 | 問題 | 報告的修法 |
| --- | --- | --- | --- | --- |
| check-skill | 4.1 | recommendation | Step 3 與 Step 4 又解釋一次 **checker defect**，Step 3 那一份已經走樣 | Step 3 只說記下每個 checker defect 與誤導它的那一行；Step 4 的兩行縮成一行 |
| check-skill | 4.2 | recommendation | Step 0 又解釋一次 `{yymmdd-hh}`，而且說錯了：dashboard 只記日期，跨一個小時不會把一次執行分開 | 兩行換成「在這裡讀一次時鐘，整次執行都用同一個 stamp」 |
| compile-skill | 3.1 | recommendation | description 說被拒的來源「什麼都不寫」，但 run record 照寫 | 改成 "is refused with no skill.py written" |
| compile-skill | 3.2 | recommendation | description 說每次執行都以執行它作結，但 `run step N`、INVALID 的來源與拒絕覆寫都不會 | 改成 "It then runs skill.py" |
| compile-skill | 4.1 | recommendation | Step 4 的標題寫 Deterministic Steps，term 是 **Step Action** | 改名為 "Step 4 - Prove the Deterministic Step Actions"，README 三處跟著改 |
| compile-skill | 6.1 | issue | `run step 2` 時 Step 2 會再跑 Step 1 的 script，它會讀 config.yaml，圖上沒畫 | 加 `CONFIG --> S2`，黑色；README 的樹加一行 |
| compile-skill | 6.2 | recommendation | `SRC --> S1` 是黑色，但它的資料經 step inventory 與 source fingerprint 進了 Compiled Script；圖例又把 fingerprint 說成 step inventory 的 | 箭頭 7 改藍，圖例那一句重寫 |
| gen-skill | 5.1 | recommendation | Step 6 的 `/chinese` 範例路徑用反斜線 | 改成正斜線 |
| gen-skill | 6.1 | issue，要選 | Step 6 只說 twin 與 parity check，圖上卻畫了 chinese skill 的 commit 與 keep-English list | (a) Step 6 寫明 chinese skill 還會在使用者答應時 commit、可能加一個 term，並補畫 `ANSWERS --> S6`；(b) 拿掉圖上的 git history 與 keep-English list；報告建議 (a) |

**表 12：最後一次重新檢查找到的 checker 缺陷**

| # | 缺陷 | 建議的去處 |
| --- | --- | --- |
| 1 | check 3 只讀 SKILL.md，description 裡交給 compile SOP 與 script 的說法只能判為 unknown | [[Task 116]]，和它表 1 的第 4 項同一處 |
| 2 | 準則 6 的「圖要跟著 step 改」，在 step 把工作交給另一個 skill 時方向相反 | [[Task 116]] |
| 3 | gen-skill 的 placeholder 掃描會掃到必須留下的 `{N}`，沒有準則判得到 | 已在 [[Task 115]] 表 2 的第 1 項 |
| 4 | 掃描器把指涉不同東西的同一個詞算成 term 的使用，例如 gen-skill 的 "the `common` skill group" | [[Task 116]] |
| 5 | 準則 1.12 只看有沒有粗體的答案，不看它和樹是否一致，例如 compile-skill 的 README 說 Step 4 不跑 script，樹上卻跑 skill.py | [[Task 116]] |

### 2026-11-13 照 Step 6 修表 11，結案

- 使用者決定：表 11 全部修，gen-skill 6.1 選 (a)；表 12 的第 1、2、4、5 項記進 [[Task 116]]；修完 commit 之後就結案，不再重新檢查。
- 表 11 的 9 個 item 全部照報告的修法修了，接在 run 261113.2 之後；run record 記了 Step 6。
  - check-skill：Step 0 只說在這裡讀一次時鐘，整次執行都用同一個 `{yymmdd-hh}`；Step 3 只說記下每個 **checker defect** 與誤導它的那一行，Step 4 的兩行縮成一行。
  - compile-skill：description 改成 "is refused with no skill.py written" 與 "It then runs skill.py"，共 1012 字元；Step 4 改名為 "Step 4 - Prove the Deterministic Step Actions"，README 三處跟著改；README 加了黑色的 `CONFIG --> S2` 與樹上 Step 2 的一行，`SRC --> S1` 改藍，圖例那一句重寫。
  - gen-skill：Step 6 的 `/chinese` 範例路徑改用正斜線；Step 6 寫明 chinese skill 只在使用者答應時 commit twin，也可能在 keep-English list 加一個 term；README 補畫 `ANSWERS --> S6`。
- 五份 twin 經 chinese run 261113.17 到 261113.21 更新，parity 與 verify 都是 0 failure。
- 檢查：SkillsGestalt 有 header quote 的 61 個檔案，59 個是 UNCHANGED，README-tmp.md 與它的 twin 要給 `--config` 才能查，和之前一樣；md-style 沒有改動。
- Skills Dashboard 上三個 skill 都標了 needs check。
- 表 12 的第 1、2、4、5 項記進 [[Task 116]] 的表 2，它的標題改為 10 個缺陷。

## 4. 要做的

—

## 5. 驗證

- 在 SkillsGestalt 執行 `.venv/bin/python -c "import click"` 成功。
- `/check-skill check-skill` 與 `/check-skill compile-skill` 的 6 個 check 都沒有 issue，或每個 finding 都由使用者決定過；Skills Dashboard 上這兩列的 needs check 都已清掉。
  最後一次重新檢查（run 261113.2）之後，表 11 的每個 item 都由使用者決定過，needs check 也清掉了；照 Step 6 修好之後又標上的 needs check，使用者決定留給 [[Task 116]]。
- 每個改過的 twin，`check_parity.py` 沒有 `[FAIL]`；改過的檔案，`depends_on.py check` 都是 UNCHANGED。
- 拋棄式 skill 沒有缺少的 heading，也沒有留下 placeholder，而且已經刪掉。

## 6. 與其他 task 的關係

- [[Task 115]]：沙盒測試找到的 gen-skill 與 SKILL-tmp.md 的問題，從本 task 分出去；表 6 裡 gen-skill 自己的 item 仍由本 task 修。
- [[Task 116]]：第二次與最後一次重新檢查找到、還沒改的 10 個 checker 缺陷，從本 task 分出去，讓本 task 修完表 9 與表 11 就能結案；它的那次檢查也清掉本 task 留下的 needs check。
- [[Task 74]]：compile-skill 兩支 script 的另外三個缺陷，與這裡的 item 無關；`beaac7d` 也改了這兩支 script 讀相對路徑的方式，做 Task 74 時以那一版為準。
- [[Task 54]]：定期以 check-skill 檢查每個 skill 的 chore；表 3 的 checker 缺陷修好之後，那個 chore 的結果才不會有這些誤報。
- [[Task 73]]：keep-English 稽核。
  這幾次 chinese run 看到的「腳本」「範本」warning 在 HEAD 就有，屬於它，不在這裡處理。

## 7. 知識

—

## 8. 日誌

### 2026-11-13

- 改名：countdell 上的 SkillsGestalt 已把 Task 103 到 113 用於別的事，所以本 task 由 Task 104 改成 Task 114；Task 104 到 107 依序改成 114 到 117，彼此的連結跟著改，內容不變。
  在這之前的 commit 以 `task 104:` 開頭。
- 結案：照 Step 6 修好表 11 的 9 個 item，表 12 的第 1、2、4、5 項記進 [[Task 116]]；見第 3 章。
- 使用者決定：表 11 全部修，gen-skill 6.1 選 (a)；表 12 照建議的去處；修完 commit 之後結案，不再重新檢查。
- 最後一次重新檢查：item 記在表 11，checker 缺陷記在表 12。
- 照 Step 6 修好表 9 的 9 個 item（`b8ed7eb`），並提出 [[Task 116]]（`31ab456`）；見第 3 章。
- 使用者決定：表 9 全部修，compile-skill 3.1 選 (a)；表 10 的第 2 到 7 項另開 [[Task 116]]；先 commit 表 7（`227ed73`）。
- 第二次重新檢查：item 記在表 9，新的 checker 缺陷記在表 10；改正表 8 第 7 項和 DFD.md 矛盾的那一句。
- 修好表 7 的 12 個 checker 缺陷（`227ed73`），開始重新檢查；見第 3 章。
- 照 Step 6 修好表 6 的 15 個 item（`9631b6b`）；見第 3 章。
- 使用者決定：表 6 全部修，有選項的照報告的建議；表 7 留在本 task，表 6 修完再做；gen-skill 與範本的問題另開 [[Task 115]]；先 commit 修好的 checker；裝 `click`。
- commit 修好的 checker（`45fcaca`），在 SkillsGestalt 的 `.venv` 裝了 `click` 8.4.2，並提出 [[Task 115]]。

### 2026-11-12

- 重新檢查：run 261112.3 的 item 記在表 6，新的 checker 缺陷記在表 7；沙盒裡的 gen-skill 測試通過，沙盒已刪掉。
- 修好表 3 的 10 個 checker 缺陷（還沒 commit），開始重新檢查；見第 3 章。
- 改名：本來提為 Task 103，但另一台電腦 countdell 上的 SkillsGestalt 已把 Task 103 用於另一件事，所以改成 Task 104。
- 提出：修完 run 261112.1 的 5.1、6.1，與 run 261112.2 的 1.1、1.2、5.1、5.2 之後，使用者要把剩下的工作記成 task。
