# Task 41 - 讓 check_ste.py 提醒字典不核准的技術用字

**Status**：尚未開始——2026-10-14 記下問題，同日審 report-md-rules 時再記下三項；`check_ste.py` 與 asd-ste 的 SKILL.md 都還沒動。
**Raised**：2026-10-14，[[Task 32]] 審核 RSDC-Standard 時發現：草稿把字典不核准的 capability 列進 Technical words，`check_ste.py` 沒有提醒。
**Depends on**：—

## 1. 背景

背景：STE Issue 9 的 Rule 1.6 規定，字典不核准的字，只有能歸進某個技術名詞類別時，才能當技術名詞用。
[check_ste.py](../.github/common/skills/asd-ste/scripts/check_ste.py) 遇到 header note 的 `Technical words:` 裡的字就直接放行：字典本來就核准的，會以一行 `[INFO]` 列出（例如 record、standard），字典不核准的卻什麼都不說。
2026-10-13 第三輪審核時，capability 就這樣列進 RSDC-Standard 的草稿，字典給的替代字 FUNCTION 與 CAN 沒有人看到；2026-10-14 改由 [ste-custom.md](../.github/common/skills/asd-ste/references/ste-custom.md) 核准。
program 也是這樣：RSDC-Standard、tw-keep-english 與 skill-writing 的草稿都把它列進 Technical words，字典給的替代字是 SEQUENCE；2026-10-18 [[Task 32.8]] 審 skill-writing 時改由 ste-custom.md 核准，programming 一起收進。

## 2. 現況

**審 report-md-rules 時發現的（2026-10-14）**

[[Task 32]] 審 report-md-rules 的草稿時，又找到三個相關的落差，使用者決定一併記在這裡：

1. **標題檢查不問字典沒收錄的字**：清冊只問標題裡字典列為不核准、而且在任何詞性都不核准的字。
   report-md-rules.md 第 33 行「# Update MD report file」的 Update 字典裡沒有，所以清冊沒問，草稿的 Technical words 原本也沒列；審核時判定它是技術動詞，才列進去。
2. **技術用字只在內文找**：`prose()` 略過標題，所以只在標題用到的技術用字，會被報成「technical words listed but never used」。
   update 列進 report-md-rules-ste.md 的 Technical words 之後就是這樣，Step 3 留下這一則 WARN 並寫明原因。
   2026-10-16 草稿第 14 行改用 update 之後，這則 WARN 消失；落差仍在：只在標題用到的技術用字仍會被報。
   2026-10-18 update 收進專案核准詞（[[Task 51]]），不再是技術用字；落差仍在。
3. **SKILL.md Step 1 的例子**：Step 1 拿「*create* 當動詞」當標題違反 STE 的例子，但 create 已在 2026-10-14 收進 ste-custom.md，核准的意思是建立新的檔案或資料；例子要改，SKILL-tw.md 照 chinese skill 跟著改。

## 3. 要做的

**要決定的**

- 字典不核准的技術用字要怎麼報：`[INFO]`、`[WARN]`，或只在它被用到的詞性不核准時才報。
  RSDC-Standard 的草稿還有 activity、process、request、stage 這幾個不核准的名詞，以及 branch、call、file、key、label、link、list、run 這幾個只有動詞不核准的字。
- 只有動詞不核准、在草稿裡當名詞用的字（例如 file、list）要不要略過。
- 報出來之後怎麼處理：留在 Technical words 並寫明理由、改用替代字，或收進 ste-custom.md。
- 標題裡字典沒收錄的字要不要也問，只在標題用到的技術用字要不要算作用到，以及 Step 1 的例子要換成什麼。

**改 asd-ste 時**

先讀 asd-ste 的 [README.md](../.github/common/skills/asd-ste/README.md) 的 When the Skill Is Changed，照它改，並跑它列出的檢查。

## 4. 驗證

—

## 5. 與其他 task 的關係

—

## 6. 知識

—

## 7. 日誌

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
