# Task 116 - 修正 check-skill 重新檢查時找到的 10 個 checker 缺陷

**Status**：完成——10 個 checker 缺陷修好了，表 5 的 5 個 item 照 Step 6 修好了，表 6 另開 [[Task 117]]；使用者決定不再重新檢查就結案。
**Raised**：2026-11-13，[[Task 114]] 第二次重新檢查時找到；使用者決定另開 task，讓 Task 114 修完它的 item 就能結案。
**Depends on**：—

## 1. 背景

[[Task 114]] 修好 check-skill 的兩批 checker 缺陷之後，以 check-skill run 261113.1 再檢查 check-skill、compile-skill 與 gen-skill，6 個 check 全做。
那次報告另外列出 7 個 checker 缺陷：第 1 個是 Task 114 自己在準則 6.2 引進的，當場改正了；其餘 6 個記在本 task。
Task 114 最後一次以 run 261113.2 檢查時，又列出 5 個 checker 缺陷：其中 4 個記在本 task，另 1 個是 gen-skill 的 placeholder 掃描，已在 [[Task 115]] 表 2 的第 1 項。
checker 缺陷是 check-skill 自己的問題：它讓 check 漏判或誤判，但不計入任何 skill 的 finding。
check-skill 不寫 MD report，那兩次的報告只在對話裡，所以每一項的重點都寫在第 3 章的表裡；行號是 2026-11-13 檢查當時的。

## 2. 結論

- 表 1 與表 2 的 10 個 checker 缺陷修好了，修法見表 3 與表 4；commit 是 `0db8a03`，只在本機的 `m1`，不在 GitHub 上。
- 重新檢查（run 261113.3）：check-skill ❌ 1·0、compile-skill ❌ 1·1、gen-skill ❌ 1·1，三列的 needs check 都清掉了；10 個缺陷都沒有再出現，item 見表 5，新的 checker 缺陷見表 6。
- 表 5 的 5 個 item 照 Step 6 修好了，compile-skill 4.1 選 (a)，改法見表 7；commit 與這段紀錄是同一個，也只在本機的 `m1`。
- 表 6 的 3 個 checker 缺陷另開 [[Task 117]]（`98c3326`）。
- 使用者決定不再重新檢查就結案：Skills Dashboard 上 check-skill、compile-skill 與 gen-skill 又標著 needs check，留給 [[Task 117]] 修好 checker 之後的那次檢查。
- 留下的問題：check_parity.py 對三份 twin 的舊行提出 keep-English 警告，屬於已經該做的 keep-english chore，見第 3 章。

## 3. 過程

### 2026-11-13 提出時的狀態

**表 1：run 261113.1 找到、還沒改的 checker 缺陷**

| # | 在哪裡 | 缺陷 | 例子 |
| --- | --- | --- | --- |
| 1 | `checking-criteria.md:154`，準則 3.2 | 只拿 MUST FOLLOW 宣告的輸出和 description 比，沒拿 step 實際寫的東西比；MUST FOLLOW 和 description 說法相同時，什麼也比不出來 | compile-skill 的 3.1 只有對照 Step 4 才看得出來 |
| 2 | `checking-criteria.md:245`，準則 6.3 | 沒說 Step 0 給的值只用來放檔或找檔時，算不算 step 的讀取；換一次執行可能判成相反 | 判為讀取：check-skill SKILL.md:235 指明是 Step 0 給的值，compile-skill SKILL.md:221 要看的旗標；判為不是：check-skill SKILL.md:462 只用來找檔、自己有箭頭的 placeholder |
| 3 | `checking-criteria.md:46`，準則 1.3 | 只判整個 glossary 區段不見，沒有準則判 step 用到、glossary 卻沒定義的名詞；[skill-writing.md](../skill-groups/common/rules/skill-writing.md) 要求每個這種名詞都有定義 | check-skill 在 SKILL.md:13 與 :247 用 Checkpoint Dir，compile-skill 在 SKILL.md:85 用 the Working Dir of a run，兩者都沒有 glossary 條目 |
| 4 | check-skill SKILL.md:294 與 `checking-criteria.md:147` | Step 3 說 check 3 不讀 fact group，但準則不准修法讓 description 超過上限，判這一點要用 `template_shape.frontmatter.description_chars` | 那次執行是自己數字元 |
| 5 | `scan_skill.py:47` 與 `:855` | `UNC_PATH` 接受兩個開頭的反斜線，所以 Python 字串裡跳脫的 Windows 分隔符號被當成 UNC 路徑；而且只在 Markdown 檔裡找 code span，所以這些 fact 的 `backticked` 都是 false | `scan_skill.py:170` 的 `\\common\\templates`、`update_dashboard.py:266` 的 `\\dashboard\\skills.md`；兩者都在註解裡，那次沒有影響 |
| 6 | `scan_skill.py:345` | 把加了反引號的大寫 `{PLACEHOLDER}` 算成 term placeholder 的變體；準則 4 從不判 code identifier，glossary 自己也提到那個 token | gen-skill SKILL.md:227 與 :275 |

### 2026-11-13 Task 114 最後一次檢查又找到的

**表 2：run 261113.2 找到、還沒改的 checker 缺陷**

| # | 在哪裡 | 缺陷 | 例子 |
| --- | --- | --- | --- |
| 1 | check-skill SKILL.md:294，check 3 的輸入 | check 3 只讀 SKILL.md；description 裡交給 compile SOP 或 script 去做的說法，只能判為 unknown；和表 1 的第 4 項是同一處 | compile-skill 的 description 有 4 個說法只能判為 unknown，`check_compiled.py` 其實都做到了 |
| 2 | `checking-criteria.md:229`，check 6 的規則 | 「圖與 step 不一致時，改的是圖」在 step 把工作交給另一個 skill 時方向相反：照做會拿掉確實會發生的寫入 | gen-skill 6.1 因此成了要選的 item |
| 3 | `scan_skill.py` 的 terminology 比對 | 把指涉不同東西的同一個詞算成 term 的使用，可能藏起一個沒用到的 term | gen-skill SKILL.md:115 的 "the `common` skill group" 被算成 **Skill group** 的使用 |
| 4 | `checking-criteria.md:74`，準則 1.12 | 只看有沒有粗體的答案、樹有沒有列出每個 step，不看答案和樹是否一致 | compile-skill README 說 Step 0、2、4 不跑 script，樹上的 Step 4 卻跑 skill.py，`run step 2` 時 Step 2 也會再跑 `scan_source.py` |

### 2026-11-13 掃描器的修正

**表 3：`scan_skill.py` 的修法**

| 缺陷 | 修法 |
| --- | --- |
| 表 1 第 5 項 | UNC 路徑要兩個反斜線配單一分隔符號，或四個配兩個；兩個配兩個是跳脫過、從分隔符號開始的路徑。script 的註解與 docstring 裡也找 code span，其他地方的反引號是程式語法 |
| 表 1 第 6 項 | 一般 term 的字以別的大小寫出現在 code 裡，是 code identifier，不算變體 |
| 表 1 第 3 項 | `terminology` 多了 `undefined_names`：檔案用了、卻沒有任何 `- **Name** —` 定義的名稱，包括兩個字以上的大寫名稱，與 SKILL-tmp.md 的 `# TERMINOLOGY` 給每個 skill 的 term；不找 frontmatter、Prompt Examples 與 heading 的字 |
| 表 2 第 4 項 | `files_each_step_uses` 多了 `scripted_rule`，即粗體句的文字，與每個 step 的 `runs` 行 |

- 以 HEAD 的掃描器與新的掃描器掃描 22 個 common skill（沙盒的 run 991231.43 與 991231.42），差別只有這些：假的 UNC 路徑都不見了，check-skill 的 `scan_skill.py` 與 `update_dashboard.py` 各一個，imp-app 的 `resolve_session.py` 兩個；check-skill 一個 docstring 裡的路徑變成 `backticked`；code 裡的 15 個大小寫變體不見了，都是 mermaid 圖與 CLI 參數裡的步驟名稱、data key 與 `{PLACEHOLDER}`；以及新的兩個 fact。
- `undefined_names` 在 22 個 skill 共列出 55 個名稱，包括表 1 第 3 項的兩個例子；其他的多半真的沒有定義，例如 check-wiki-doc 的 Run Number，少數是語言或專有名稱。
- 表 2 第 3 項的指涉，掃描器分辨不出來，所以改在準則 4。
- 表 1 第 3 項寫的是準則 1.3，`checking-criteria.md:46` 其實在準則 1.2 裡。

### 2026-11-13 準則與 SKILL.md 的修正

- 使用者確認了 9 處措辭，全部照提案改。

**表 4：準則與 SKILL.md 的修法**

| 缺陷 | 改在哪裡 | 修法 |
| --- | --- | --- |
| 表 1 第 1 項 | 準則 3.2 | 比對每個 step 寫的東西，不只比 MUST FOLLOW 宣告的輸出 |
| 表 1 第 2 項 | 準則 6.3 | Step 0 給、之後的 step 用到的值，即使只用來找檔或放檔，也是一次讀取；從存放它的旗形，或從 Step 0 讀它的地方畫來的箭頭，有一個就夠 |
| 表 1 第 3 項 | 新的準則 4.7，讀 `undefined_names` | step 用到的未定義名稱是 issue，只有定義或 MUST FOLLOW 用到時是 recommendation；專有名稱、另一份文件的 heading，與 skill 說自己沒有的功能不算 |
| 表 1 第 4 項、表 2 第 1 項 | SKILL.md 裡 check 3 的輸入，與準則 3 | check 3 也讀 step 把主張交給它的 reference 或 script，與 `template_shape.frontmatter.description_chars`；這種主張拿那個檔案來判定 |
| 表 2 第 2 項 | check 6 的規則 | 以名稱把工作交給另一個 skill 的 step，讀寫的就是那個 skill 所讀寫的；圖上畫出的留著，step 也不必重述 |
| 表 2 第 3 項 | 準則 4 的開頭與 4.5 | 一次使用要指 glossary 所定義的東西才算數；每一處都指別的東西的 term 也算沒用到 |
| 表 2 第 4 項 | 準則 1.12，讀 `scripted_rule` 與 `runs` | 粗體句要與樹一致；行文另外區分出來的程式，與交給另一個 skill 的工作，不算不一致 |

- SKILL.md 的 Step 2 寫明新的 fact；README 的樹上 Step 3 多了 check 3 的讀取；Dataflow 已有 `CHECKED --> S3` 與 `FACTS --> S3`，不必改。
- 三份 twin 經 chinese run 261113.22 到 261113.24 更新，parity 與 verify 都是 0 failure；新寫的行照 keep-English list 用 glossary 與 script。
- CHANGES.md 加了一筆。
- 檢查：md-style 沒有改動，README 的 header quote 8 個都是 UNCHANGED，`scan_skill.py` 可以編譯。
- README 範本的樹本來就讓有 `runs` 行的 step 對上粗體句，所以 gen-skill 不必跟著改。

### 2026-11-13 重新檢查

- 以 `/check-skill check-skill, compile-skill, gen-skill` 6 個 check 全做（run 261113.3，subagent 跑 Steps 0 到 5）。
  check-skill ❌ 1 個 issue、0 個 recommendation，compile-skill ❌ 1、1，gen-skill ❌ 1、1；三列的 needs check 都清掉了。
- 表 1 與表 2 的 10 個缺陷都沒有再出現：compile-skill 的 description 每個主張都拿做那件事的檔案判定，沒有 unknown；長度以 `description_chars` 為準；沒有假的 UNC 路徑，也沒有 `{PLACEHOLDER}` 變體；"the `common` skill group" 判為指另一個東西；check 6 沒有要拿掉 gen-skill 交給 chinese skill 的讀寫。
- 新的準則照預期判出 item：6.3 判出兩個 Step 0 值的讀取，1.12 判出 compile-skill 粗體句與樹不一致，4.7 判出 compile-skill 的 Working Dir；check-skill 的 Checkpoint Dir 判為不是 finding，因為它的執行不處理 Checkpoint Dir。

**表 5：run 261113.3 的 item**

| Skill | Item | 種類 | 問題 | 報告的修法 |
| --- | --- | --- | --- | --- |
| check-skill | 6.1 | issue | Step 6 以 Step 0 解析的 `{python}`、`{skillGroups.common}` 與 `{wikiDir}` 找 script 與 Skills Dashboard，圖上卻沒有從 Run settings 畫到 Step 6 的箭頭（準則 6.3） | 在 `SETTINGS --> S2` 後加黑色的 `SETTINGS --> S6`，README-tw 也一樣 |
| compile-skill | 1.1 | issue | Files Each Step Uses 的粗體句說 Step 2 與 Step 4 不執行 script，樹上 Step 2 卻在 `run step 2` 時再執行 `scan_source.py`，Step 4 執行 `<target>/skill.py`（準則 1.12） | 粗體句後加一句：Step 2 只在 `run step 2` 時再執行 Source Scanner，Step 4 執行 Compiled Script 只是把它當成要證明的程式 |
| compile-skill | 4.1 | recommendation，要選 | MUST FOLLOW 與 **Step file** 的定義用到 Working Dir，卻沒有定義，而 skill 根本不寫 working data（準則 4.7） | (a) SKILL.md:85 改成說本 skill 不寫 working data，所以沒有 Working Dir；(b) 在 TERMINOLOGY 定義 **Working Dir** 並說它沒有；報告建議 (a) |
| gen-skill | 3.1 | recommendation | description 沒說 Step 6 的 chinese skill 可能在共用的 keep-English list 加 term，並在使用者答應時 commit twin（準則 3.3） | 改寫 description 那一句，共 993 字元 |
| gen-skill | 6.1 | issue | Step 1、4、6 用了 Step 0 定下的值，圖上沒有從 Parsed inputs 畫來的箭頭（準則 6.3） | 加黑色的 `INPUTS --> S1`、`INPUTS --> S4`、`INPUTS --> S6`，圖例那一句跟著改 |

**表 6：重新檢查找到的 checker 缺陷**

| # | 在哪裡 | 缺陷 | 例子 |
| --- | --- | --- | --- |
| 1 | `scan_skill.py:76` 的 `FILE_LITERAL` | 檔名有大括號就不算 literal，所以 `step_{N}.yaml` 從不被記錄，而它正是準則 4.1 自己的例子 | check-skill、compile-skill 與 gen-skill 的 **Step file** 都得到 `literals: []` |
| 2 | SKILL.md:294 的 check 4 輸入，準則 4.4 與 4.6 | check 4 只讀 `terminology` fact group，裡面只有含 term 字詞的行；沒用 term 的表格標頭、換了說法重述的定義，都不在任何 fact 裡 | check-skill SKILL.md:224 的 **Skills table** 與它的欄位 |
| 3 | SKILL.md:295 與 :36，準則 5.7 | Step 3 的表說 check 5 不讀 fact group，**facts file** 的定義也只列 check 1、2、4、6；準則 5.7 卻要讀 `template_shape.working_dir` | 這次執行為 5.7 讀了它 |

- 表 6 的 3 項另開 [[Task 117]]。

### 2026-11-13 Step 6

- 使用者照建議決定：表 5 全修，compile-skill 4.1 選 (a)；先 commit checker 的修正（`0db8a03`），Step 6 修完並 commit 後結案，不再重新檢查。
- 照 check-skill 的 Step 6 一項一項改，改法照報告。
  每份 twin 經 chinese skill 更新：check-skill 的 README 是 run 261113.25，compile-skill 的 README 與 SKILL.md 是 261113.26 與 261113.27，gen-skill 的 SKILL.md 與 README 是 261113.28 與 261113.29。

**表 7：run 261113.3 的 Step 6**

| Skill | Item | 改了什麼 |
| --- | --- | --- |
| check-skill | 6.1 | README.md 與 README-tw.md 的 Dataflow 加了黑色的 `SETTINGS --> S6`，是第 40 條箭頭，linkStyle 不變 |
| compile-skill | 1.1 | README.md 與 README-tw.md 的粗體句後加一句：Step 2 只在 `run step 2` 時再執行 Source Scanner，Step 4 執行 Compiled Script 只是把它當成要證明的程式 |
| compile-skill | 4.1(a) | SKILL.md 與 SKILL-tw.md 的 MUST FOLLOW 改成：Run Number 與 run record 遵守 run-data-rules.md；本 skill 不寫 working data，所以它的執行沒有 Working Dir |
| gen-skill | 3.1 | SKILL.md 與 SKILL-tw.md 的 description 改成：chinese skill 寫出兩份 twin，可能在共用的 keep-English list 加入 term，並在使用者同意後 commit twin；description 共 993 字元 |
| gen-skill | 6.1 | README.md 與 README-tw.md 的 Dataflow 加了黑色的 `INPUTS --> S1`、`INPUTS --> S4` 與 `INPUTS --> S6`，是第 37 到 39 條箭頭；圖例的黑色資料多了 Step 4 與 Step 6 寫入或交出的路徑，與 Step 1 核對 `none` 回答的 workflow |

- 報告為 gen-skill 3.1 建議的中文寫「keep-English 清單」；gen-skill 的 twin 本來就寫 keep-English list，所以照 chinese skill 的規則沿用。
- 5 份 twin 的 parity 與 verify 都是 0 failure。
- check_parity.py 也對三份 twin 的舊行提出 keep-English 警告；這些行都在 change set 之外，照 Step 6「只改 item 指名的東西」留著。
  它們是 check-skill README-tw.md 第 133 到 135 行與 gen-skill README-tw.md 第 124、132、133 行的「腳本」，以及 gen-skill SKILL-tw.md 第 196、224、263、270、271、273 行的「腳本」與第 209 行的「範本」。
  chore 摘要表已記著 tw-keep-english.md 換成 261110 之後，[keep-english](../chores/keep-english.md) 該做了；這些行屬於那個 chore。
- 三個 skill 在 Skills Dashboard 上標了 needs check；run 261113.3 的 run record 加了 Step 6。

## 4. 要做的

—

## 5. 驗證

- 改之前與改之後的 facts 比對：表 1 的第 5、6 項不再出現，新的 `undefined_names`、`scripted_rule` 與 `runs` 列出預期的東西，其他 fact 沒有意外的變化；表 2 的第 3 項改在準則，facts 看不出來。
- check-skill README 列的檢查都通過：掃描 asd-ste、gen-skill、check-skill，`check_parity.py` 沒有 `[FAIL]`，`depends_on.py check` 都是 UNCHANGED。
- 再跑一次 `/check-skill`，報告沒有再列出表 1 與表 2 的缺陷。
- Step 6 之後，三個 skill 的 README 列的檢查都通過：掃描 asd-ste、gen-skill、check-skill 與 compile-skill，README 沒有缺少的 heading 或 step，header quote 都是 UNCHANGED；九組 twin 的 `check_parity.py` 沒有 `[FAIL]`；三份 README 的 `depends_on.py check` 都是 UNCHANGED；md-style 沒有改動。
  `check_reformat.py --twin` 對兩份 SKILL-tw.md 報 frontmatter 下方的 pairing line 對不上，HEAD 就是這樣，不是這次造成的。
- 沒有跑 `/check-skill`：使用者決定留給 [[Task 117]]；也沒有跑 gen-skill 的沙盒測試，因為這次的修改不影響 gen-skill 寫出的 skill。

## 6. 與其他 task 的關係

- [[Task 114]]：在它的第二次與最後一次重新檢查找到這些缺陷；它修過的兩批 checker 缺陷記在它的表 5 與表 8。
- [[Task 115]]：最後一次重新檢查的另 1 個 checker 缺陷，gen-skill 的 placeholder 掃描，記在它的表 2。
- [[Task 117]]：表 6 的 3 個 checker 缺陷記在那裡；它修好之後的檢查，清掉本 task 的 Step 6 留下的 needs check。
- [[Task 54]]：定期以 check-skill 檢查每個 skill 的 chore；這些缺陷修好之後，那個 chore 的結果更可靠。

## 7. 知識

—

## 8. 日誌

### 2026-11-13

- 改名：countdell 上的 SkillsGestalt 已把 Task 103 到 113 用於別的事，所以本 task 由 Task 106 改成 Task 116；Task 104 到 107 依序改成 114 到 117，彼此的連結跟著改，內容不變。
  在這之前的 commit 以 `task 106:` 開頭。
- 結案：照 Step 6 修好表 5 的 5 個 item，見表 7；表 6 另開 [[Task 117]]；Skills Dashboard 上三個 skill 標著 needs check。
- 使用者照建議決定：表 5 全修，compile-skill 4.1 選 (a)；表 6 另開新 task；先 commit checker 的修正，Step 6 修完並 commit 後結案；commit 掃描器、準則、SKILL.md、README、三份 twin 與 CHANGES.md。
- 重新檢查（run 261113.3）：10 個缺陷都沒有再出現；item 記在表 5，新的 checker 缺陷記在表 6。
- 使用者確認 9 處措辭，全部照提案改；改好準則、SKILL.md、README 與三份 twin，開始重新檢查，還沒 commit；見第 3 章。
- 改好掃描器的 4 處並比對 facts，見第 3 章；準則與 SKILL.md 的措辭列給使用者確認。
- 開始：使用者要接著做本 task；改之前的 facts 留在沙盒的 run 991231.40，掃描 check-skill、compile-skill、gen-skill 與 asd-ste。
- 提出：[[Task 114]] 第二次重新檢查時找到，使用者決定另開 task。
- 加入表 2：[[Task 114]] 最後一次重新檢查（run 261113.2）又找到 4 個，使用者同意記在這裡；標題由 6 個缺陷改為 10 個。
