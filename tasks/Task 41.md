# Task 41 - 讓 check_ste.py 提醒字典不核准的技術用字

**Status**：完成——`check_ste.py` 會提醒字典不核准的技術用字，標題的兩個落差已補，Step 1 的例子已換；現有 STE 檔留下的警告由 [[Task 41.1]] 處理。
**Raised**：2026-10-14，[[Task 32]] 審核 RSDC-Standard 時發現：草稿把字典不核准的 capability 列進 Technical words，`check_ste.py` 沒有提醒。
**Depends on**：—

## 1. 背景

背景：STE Issue 9 的 Rule 1.6 規定，字典不核准的字，只有能歸進某個技術名詞類別時，才能當技術名詞用。
[check_ste.py](../skill-groups/common/skills/asd-ste/scripts/check_ste.py) 遇到 header note 的 `Technical words:` 裡的字就直接放行：字典本來就核准的，會以一行 `[INFO]` 列出（例如 record、standard），字典不核准的卻什麼都不說。
2026-10-13 第三輪審核時，capability 就這樣列進 RSDC-Standard 的草稿，字典給的替代字 FUNCTION 與 CAN 沒有人看到；2026-10-14 改由 [ste-custom.md](../skill-groups/common/skills/asd-ste/references/ste-custom.md) 核准。
program 也是這樣：RSDC-Standard、tw-keep-english 與 skill-writing 的草稿都把它列進 Technical words，字典給的替代字是 SEQUENCE；2026-10-18 [[Task 32.8]] 審 skill-writing 時改由 ste-custom.md 核准，programming 一起收進。

## 2. 現況

### 2026-11-01 改好之後

- `check_ste.py` 檢查 STE 檔時（Step 3 與 `--ste` 單獨檢查）多報三種：
  1. 字典不核准當名詞或形容詞用的技術用字：一行 `[WARN]`，附上替代字，並說明三種處理。
  2. 字典只不核准當動詞用的技術用字：一行 `[INFO]`，提醒只能當名詞用（Rule 1.7）。
  3. 標題裡字典沒收、也不是技術用字的字：一行 `[WARN]`，說明標題要先在 source file 改，或列為技術用字。
- 只在標題用到的技術用字算作用到，不再報「technical words listed but never used」。
- Step 1 的清冊也問標題裡字典沒收的字；檔名、識別碼、縮寫與大小寫混合的名稱不問。
- SKILL.md 與 SKILL-tw.md 的 Step 1 與 Step 3 跟著改；Step 1 的例子改成「把 *list* 當動詞」。
- 掃了 SkillsGestalt 的 18 個英文 STE 檔：`Technical words:` 共 363 個字，字典不核准的有 25 個，見表 1；判定都還是 PASS，多出的警告見 [[Task 41.1]]。

**表 1：列進 Technical words、字典不核准的字（2026-11-01）**

| 種類 | 程式怎麼報 | 字 |
|---|---|---|
| 名詞或形容詞不核准 | `[WARN]`，附替代字 | activity、event、process、request、route、setting、stage、partial、variable |
| 只有動詞不核准 | `[INFO]`，只能當名詞用 | block、branch、call、escape、file、filter、guard、hook、key、label、link、list、match、note、quote、save |

### 2026-10-14 審 report-md-rules 時發現的

[[Task 32]] 審 report-md-rules 的草稿時，又找到三個相關的落差，使用者決定一併記在這裡：

1. **標題檢查不問字典沒收錄的字**：清冊只問標題裡字典列為不核准、而且在任何詞性都不核准的字。
   report-md-rules.md 第 33 行「# Update MD report file」的 Update 字典裡沒有，所以清冊沒問，草稿的 Technical words 原本也沒列；審核時判定它是技術動詞，才列進去。
2. **技術用字只在內文找**：`prose()` 略過標題，所以只在標題用到的技術用字，會被報成「technical words listed but never used」。
   update 列進 report-md-rules-ste.md 的 Technical words 之後就是這樣，Step 3 留下這一則 WARN 並寫明原因。
   2026-10-16 草稿第 14 行改用 update 之後，這則 WARN 消失；落差仍在：只在標題用到的技術用字仍會被報。
   2026-10-18 update 收進專案核准詞（[[Task 51]]），不再是技術用字；落差仍在。
3. **SKILL.md Step 1 的例子**：Step 1 拿「*create* 當動詞」當標題違反 STE 的例子，但 create 已在 2026-10-14 收進 ste-custom.md，核准的意思是建立新的檔案或資料；例子要改，SKILL-tw.md 照 chinese skill 跟著改。

## 3. 要做的

### Sub task

- [[Task 41.1]] ⬜ 處理現有 STE 檔裡字典不核准的技術用字與標題字

### 已決定（2026-11-01）

使用者回答了 7 個問題，都照建議：

1. **分兩種報**：名詞或形容詞不核准的報 `[WARN]`，附替代字；只有動詞不核准的報一行 `[INFO]`，提醒只能當名詞用。
2. **報出來之後三選一**，寫進 SKILL.md 的 Step 3：歸得進技術名詞類別就留著；否則改用替代字；專案常用就由使用者收進 ste-custom.md。
3. **Step 1 的清冊也問標題裡字典沒收的字**，一樣是要判斷的 `[TODO]`。
4. **只在標題用到的技術用字算作用到。**
5. **Step 1 的例子改成「把 *list* 當動詞」。**
6. **Step 3 也報標題裡字典沒收、也不是技術用字的字**，報 `[WARN]`。
7. **現有 STE 檔裡的警告另開 sub task** [[Task 41.1]]；本 task 只改程式與 SKILL.md。

### 改 asd-ste 時

先讀 asd-ste 的 [README.md](../skill-groups/common/skills/asd-ste/README.md) 的 When the Skill Is Changed，照它改，並跑它列出的檢查。

## 4. 驗證

照 asd-ste 的 README 的 When the Skill Is Changed：

- `check_ste.py` 對 commit `1710643` 的 DFD.md：清冊 exit `0`，另問 What 等標題字；DFD.md 與草稿的檢查 PASS。
- `check_ste.py` 對 commit `ed0076e` 的 DFD.md：清冊 exit `3`、`SOURCE-FIRST`，仍問 *Kinds*；檢查仍因 `Catalogue` FAIL。
- `check_ste.py --ste` 對 18 個 STE 檔：判定與改之前相同，DFD.md 仍 PASS，CLAUDE-local.md 原本就 FAIL。
- `check_parity.py` 對 SKILL.md 與 SKILL-tw.md：0 failure，3 則 WARN 改之前就有。
- `depends_on.py check` 對 SKILL.md 與 README.md：都 UNCHANGED。
- 沒有跑的：`/check-skill asd-ste`、`draft.py`、`make_review.py` 與 `review_server.js` 的檢查；這次沒動 draft.py、make_review.py、review_server.js，也沒改 SKILL.md 的章節結構。

## 5. 與其他 task 的關係

—

## 6. 知識

### 適合寫成新 topic

- **標題**：STE 的用字：核准字、不核准字與技術用字
- **內容**：STE 的字典把每個字＋詞性分成三種，見表 1；表 2 的三種例外讓其中一些字仍可以用；技術名詞的類別見表 3。
  - **`Technical words:` 的用法**：文件開頭的 `Technical words:` 一行列出文件用到的技術名詞與技術動詞。
    不為了消掉警告而列；what 不是技術名詞，就把句子改寫。
- **來源**：ASD-STE100 Issue 9，以及 asd-ste 的 [ste-rules.md](../skill-groups/common/skills/asd-ste/references/ste-rules.md)；topic 是白話版，細節以 ste-rules.md 為準。

**表 1：字典怎麼看一個字**

| 種類 | 字典寫什麼 | 數量 | 例子 |
|---|---|---|---|
| 核准字 | 核准的詞性；另列 509 個變化形，例如 removed、removes 對到 remove | 804 | test（核准名詞）、record（核准動詞） |
| 不核准字 | 不核准的詞性與替代字 | 1257 | capability（不核准名詞，替代字 FUNCTION、CAN）、check（不核准動詞，替代字 MAKE SURE、EXAMINE） |
| 字典沒收的字 | 沒有 | — | what、understand、repository |

表 1 是 partition：每個字＋詞性只落在一列。
以字計算時有 70 個字兩邊都有，例如 check 當名詞核准、當動詞不核准；所以 804 與 1257 是 [ste-dictionary.json](../skill-groups/common/skills/asd-ste/references/ste-dictionary.json) 依 Issue 9 整理的字數，字典換版時才會變。
不屬於表 2 任何一種例外時，核准字只照字典的詞性用，例如不寫「test the valve」，寫「do a test of the valve」；不核准字改用替代字；字典沒收的字，把句子改寫。

**表 2：讓字典沒核准的用法仍可以用的三種例外**

| 例外 | 條件 | 適用於表 1 的哪幾種 | 例子 | 怎麼處理 |
|---|---|---|---|---|
| 技術名詞（Rule 1.5 到 1.11） | 歸得進表 3 的一個類別；不能當動詞用 | 不核准字、字典沒收的字；核准字用在字典沒給的技術意思時也算（Rule 1.3） | repository（沒收）、file（只有動詞不核准，當名詞用）、record（核准動詞，當名詞「系統保存的資料」用） | 列進 `Technical words:` |
| 技術動詞（Rule 1.12、1.13） | 電腦處理類的動作；不能當名詞用 | 不核准字、字典沒收的字 | parse、commit（沒收） | 列進 `Technical words:` |
| ste-custom.md 核准的字 | SkillsGestalt 與各個 Forge 常用、又不適合當技術用字；ste-custom.md 在 `common` skill group，大家共用 | 不核准字、字典沒收的字 | capability、program（不核准名詞）、create（不核准動詞）、update（沒收） | 收進 [ste-custom.md](../skill-groups/common/skills/asd-ste/references/ste-custom.md) |

表 2 的例外跨過表 1 的列：同一個字在表 1 落一列，在表 2 也可能落一列。

**表 3：SkillsGestalt 的文件用得到的技術名詞類別**

例子取自 2026-11-01 SkillsGestalt repo 裡 18 個英文 STE 檔的 `Technical words:`：16 個在 `common` skill group，Forge 也用；2 個是 SkillsGestalt 自己的 CLAUDE-local.md 與 CLAUDE.md。
括號是列過它的檔案數。

| 編號 | 類別 | 例子 |
|---|---|---|
| 6 | 系統、元件、它們的功能、設定與零件 | app（4 檔）、module（2 檔）、handler（2 檔） |
| 7 | 數學、科學與工程用語 | hash（3 檔）、hexagon（3 檔）、parallelogram（3 檔） |
| 9 | 數字、單位與時間 | day（6 檔）、second（2 檔）、byte（2 檔） |
| 10 | 引用的文字 | —（引號或 inline code 裡的字，不列進 `Technical words:`） |
| 11 | 角色、個人、團體與組織 | agency（6 檔）、Forge（5 檔）、user（4 檔） |
| 15 | 文件、文件的部分、標準與指引 | section（12 檔）、document（11 檔）、template（7 檔） |
| 17 | 顏色 | blue（2 檔） |
| 19 | 電腦科學與資訊科技 | file（17 檔）、script（10 檔）、repository（8 檔） |

### 適合併進現有 topic

—

### 不算知識

—

## 7. 日誌

### 2026-11-02

- 連結的目標路徑從 `../.github/` 改成 `../skill-groups/`，字句沒有改（[[Task 97.7]]）。
- [[Task 41.1]] 依使用者「所有標題不歸 STE 管」的決定，拿掉本 task 加的「標題裡字典沒收的字」警告與 Step 1 的標題字 `[TODO]`。

### 2026-11-01

- 使用者回答 7 個問題，改 `check_ste.py`、SKILL.md 與 SKILL-tw.md；「現況」、「要做的」與「驗證」跟著改，本 task 完成。
- 開 sub task [[Task 41.1]]，處理現有 STE 檔多出的警告。

- 「知識」一章加上一則新 topic：STE 怎麼管字，含核准字、不核准字與兩種技術用字。
- 這則 topic 改用三個表：字的分類、字典的數量、技術名詞類別；表裡說過的條列刪掉。
- 三個表加上表號，表 1 到表 3，「內容」一行改成「見表 1 到表 3」。
- 原本的表 1 混了兩種分法，不是 partition：拆成表 1「字典怎麼看一個字」與表 2「讓字典沒核准的用法仍可以用的三種例外」；字典的數量併進新的表 1，技術名詞類別仍是表 3。
- 表 3 的例子換成專案 `Technical words:` 實際列過的字，並寫明來源與檔案數。
- 「這個專案」改寫成 SkillsGestalt：表 3 的標題與來源說明寫出 repo 名與 `common` 的檔數；表 2 的「專案核准詞」改稱「ste-custom.md 核准的字」。

### 2026-10-18

- 第 2 項補記：[[Task 51]] 把 update 收進專案核准詞，它不再是技術用字。
- 背景補記：[[Task 32.8]] 把 program 與 programming 收進專案核准詞，「要決定的」那份不核准的名詞清單拿掉 program。
- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。
- 第 2 項補記：[[Task 32]] 審 report-md-rules 第二輪時，草稿第 14 行改用 update，那則 WARN 消失，落差仍在。

### 2026-10-14

- 提出：Task 32 審核 RSDC-Standard 時發現 `check_ste.py` 沒有提醒字典不核准的技術用字。
- 審 report-md-rules 時再記下三項相關的落差。
