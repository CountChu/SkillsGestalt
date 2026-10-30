# Task 71 - 把 skill 目錄下的 Tasks.md 交給 tasks 管理

**Status**：完成——2026-10-20 Build the Agentic Panel 移成 [[Task 72]]，compile-skill 的 Tasks.md 與中文版已刪除，skill 的目錄下不再有 Tasks.md。
**Raised**：2026-10-20，使用者要 skill 目錄下的 Tasks.md 改由 `tasks/` 管理，摘要表與 `check_tasks.py` 才看得到其中的待辦。
**Depends on**：—

## 1. 背景

這個 workspace 的 task 從 [[Task 62]]（2026-10-18）起都照 [task-rules.md](../.github/common/rules/task-rules.md) 寫在根目錄的 `tasks/`，一個 task 一個檔，摘要表在 `dashboard/task-summary.md`。
compile-skill 的 `Tasks.md` 是 2026-10-04 寫的，比這個 workspace 的第一份 task 清單（2026-10-09）還早，用自己的格式記 skill compiler 的待辦。
摘要表看不到它，`check_tasks.py` 也不檢查它。
本 task 把它的待辦移進 `tasks/`，之後 skill 的目錄下不再有 Tasks.md。

## 2. 現況

### 2026-10-20 查的結果

- **只有一份**：整個 workspace 只有 compile-skill 的 `references/` 有 Tasks.md 與 `Tasks-tw.md`，各 45 行；`.github/external` 與 InvestForge 都沒有。
- **只有一項**：「1. Build the Agentic Panel」，Status 是 not started。
  它是從 [SkillCompiler-RSDC.md](../.github/common/skills/compile-skill/references/SkillCompiler-RSDC.md) 移出來的 Agentic Panel 設計，分成 What it must keep、Component、Location 與 Implementation choices 四節。
  What it must keep 引用 SkillCompiler-RSDC 的 §2.1 *Artifact Types and Flow*、§2.1 *Active Prompt Rule for Cognitive Steps*、§2.3 *Dataflow* 與 §2.4 *CLI*。
- **連到它的檔案**：只有 compile-skill 的 [SKILL.md](../.github/common/skills/compile-skill/SKILL.md) 第 53 行與 [SKILL-tw.md](../.github/common/skills/compile-skill/SKILL-tw.md) 第 46 行，在 Agentic Panel 的定義裡寫「building it is an open task in Tasks.md」。
  task 檔裡只有 [[Task 9]] 第 27 行是連到 Tasks-tw.md 的 Markdown link；其他提到它的地方都是純文字或 inline code。
- **中文版的 keep-English**：`check_parity.py --keep` 0 failure、1 個 warning：第 18、19、26 行的「腳本」，keep-English 清單把 script 留英文。
- **提到它的 task**：[[Task 9]]、[[Task 10]]、[[Task 13]]、[[Task 18.2]]、[[Task 33]]、[[Task 58]]、[[Task 59]]。
  只有 [[Task 18.2]] 還沒完成，它把 Tasks.md 與中文版列為引用 SkillCompiler-RSDC 的檔案；其餘都已完成，記的是當時做過的事。

### 已決定（2026-10-20）

使用者回答了 8 個問題，都照建議：

- **Agentic Panel 開成自己的 task**：移的時候用當時下一個號碼開新 task；本 task 只負責移過去、清掉 Tasks.md。
  建 panel 不屬於「移」這件事，所以不開成本 task 的 sub task。
- **內容照中文版搬**：task 檔用繁體中文寫，Tasks-tw.md 已有譯文，逐句搬進新 task 的章節。
  keep-English 清單上的詞改回英文，例如「腳本」寫 script；§ 引用加上連到 SkillCompiler-RSDC.md 的 Markdown link；Location 的目錄樹照抄。
- **SKILL.md 拿掉後半句**：SKILL.md 第 53 行只留 `The **design document** does not name it; this skill never writes it.`，SKILL-tw.md 第 46 行只留 `**design document** 不點名它；本 skill 絕不撰寫它。`。
  SKILL.md 不指向任何 task，panel 做完也不必再改；它在 common 裡，InvestForge 執行 compile-skill 時也會載入它。
- **Tasks.md 與 Tasks-tw.md 都刪除**：原文留在 git 歷史。
- **不加新規則**：task-rules.md 已規定 task 寫在 workspace 根目錄的 `tasks/`，一個 task 一個檔；Tasks.md 是在那之前寫的。
- **與 [[Task 18.2]] 不設 Depends on**：關係只寫在本 task，這次不改 [[Task 18.2]]，見「與其他 task 的關係」。
- **這次只提出本 task**：移的工作等使用者說再做。

### 開始做時的決定（2026-10-20）

使用者說開始做之後，又回答了 8 個問題，都照建議：

- **[[Task 72]] 的寫法**：標題是「建 Agentic Panel」，「驗證」寫「—」。
  Raised 用 2026-10-04，它第一次寫進 Tasks.md 的日子；搬到 InvestForge 的 task 也保留原本的 Raised，所以「要做的」第 1 點跟著改。
- **§ 的連結**：「背景」與 What it must keep 各連一次 SkillCompiler-RSDC.md，其餘 § 引用是純文字，[[Task 18.2]] 改節號時只要改字。
- **指位置的字**：Tasks-tw.md 第 3–4 行改成講 [[Task 72]] 自己，第 12 行的「以下是」改成指向「要做的」；其餘逐字照搬，只有「腳本」改成 script。
- **[[Task 9]]**：第 27 行的連結改成 repo 根目錄起的路徑，和它第 56 行與 [[Task 62.1]] 的前例一樣。
- **[[Task 18.2]]**：引用處寫成 [[Task 72]]，括號寫明原本是 compile-skill 的 Tasks.md 與中文版。
- **commit**：全部放進一個 commit，前綴是 `task 71:`。

### 2026-10-20 做完的結果

- **[[Task 72]] 建 Agentic Panel**：Tasks-tw.md 除了標題、項目標題與 Status 行，28 行都在 [[Task 72]] 裡，其中 7 行照決定改寫，沒有留下「腳本」。
- **compile-skill**：SKILL.md 第 53 行與 SKILL-tw.md 第 46 行拿掉了後半句；Tasks.md 與 Tasks-tw.md 已刪除，`references/` 只剩 SkillCompiler-RSDC 與中文版。
- **其他 task**：[[Task 9]] 第 27 行的連結改成 inline code，[[Task 18.2]] 第 21 行的這一項改寫成 [[Task 72]]，兩個 task 的日誌各加一行。
  本 task 第 10 行與第 18 行連到這兩份檔的連結，也改成 inline code。
- **檢查**：`find .github -name "Tasks*.md"` 沒有輸出，也沒有 Markdown link 或 wikilink 連到這兩份檔。
  SKILL.md 與中文版的 `check_parity.py --keep` 0 failure，`diff_md.py --verify` PASS。
  4 個 warning（「腳本」「識別碼」「術語表」「術語」）都在沒改的句子裡，HEAD 的版本就有。

## 3. 要做的

照「已決定」做，順序如下：

1. **開 Agentic Panel 的 task**：用當時下一個號碼，照 task-rules.md 寫六章，摘要表最上面加一列。
   Tasks-tw.md 第 3–4 行的開場與第 10–12 行移出 design document 的原因，寫進「背景」。
   What it must keep、Component、Location 與 Implementation choices 寫進「要做的」，各成一個 `###` 小節。
   Raised 寫 2026-10-04，它第一次寫進 Tasks.md 的日子，日誌也從那一天起；Status 是尚未開始。
2. **改 compile-skill 的 SKILL.md 與 SKILL-tw.md**：照「已決定」拿掉後半句。
   改之前照 [skills/CLAUDE.md](../.github/common/skills/CLAUDE.md) 讀 [skill-writing.md](../.github/common/rules/skill-writing.md)；compile-skill 沒有 README.md。
   中文版照 [chinese](../.github/common/skills/chinese/SKILL.md) skill 更新。
3. **刪除 Tasks.md 與 Tasks-tw.md**。
4. **改 task 檔裡會斷的連結**：[[Task 9]] 第 27 行連到 Tasks-tw.md 的 Markdown link 改成 inline code，字句不改，並在它的日誌加一行，連到本 task。
5. **[[Task 18.2]] 還沒完成時**：它列的引用處裡，把 Tasks.md 與中文版換成新的 task，並在它的日誌加一行，連到本 task。

## 4. 驗證

- `find .github -name "Tasks*.md"` 沒有輸出：skill 的目錄下不再有 Tasks.md。
- 搜尋 `Tasks.md` 與 `Tasks-tw.md`，沒有 Markdown link 或 wikilink 還連到它們。
- `check_tasks.py` PASS，新 task 與本 task 都在摘要表裡。
- compile-skill 的 SKILL.md 與中文版：`check_parity.py --keep` 0 failure；中文版以 INCREMENTAL 更新時，`diff_md.py --verify` PASS。
- 新 task 包含 Tasks-tw.md 標題與 Status 行之外的每一句，keep-English 清單上的詞都是英文，「腳本」這類 Flagged 的譯法一個都沒有。
- 新 task 與本 task 的副本以 `reformat_md.py --mode clean` 重排後，與原檔沒有差異。

## 5. 與其他 task 的關係

- **[[Task 72]]**：本 task 從 compile-skill 的 Tasks.md 移出來的 Agentic Panel。
- **[[Task 18.2]]**：對齊 SkillCompiler-RSDC 之後，panel 內容引用的節號會變。
  照 Skill-System template 的節號，預計 §2.1 *Artifact Types and Flow* 變成 §2.2 *Artifact Types*，§2.4 *CLI* 變成 §2.8 *CLI*。
  不設 Depends on：先做 [[Task 18.2]]，它會照「引用處同一次一起改」改到 Tasks.md，本 task 照改好的搬；先做本 task，就照「要做的」第 5 點改 [[Task 18.2]]。
- **[[Task 62]]**（2026-10-18）：每個 workspace 有自己的 `tasks/` 與摘要表，task-rules.md 也由它寫成；Tasks.md 早於這些規則。
- **[[Task 70]]**：它把 SKILL.md 的共用句子換成 STE template 的寫法，也會改 compile-skill 的 SKILL.md 與中文版；兩個 task 不要同時改這兩份檔。
- **[[Task 9]]**（2026-10-10 完成）：第 27 行的表格有連到 Tasks-tw.md 的 Markdown link，刪檔時照「要做的」第 4 點改。

## 6. 日誌

### 2026-10-20

- 提出：skill 的目錄下只有 compile-skill 有 Tasks.md，裡面只有 Build the Agentic Panel 一項。
- 使用者回答了 8 個問題，都照建議；決定寫在「現況」的「已決定（2026-10-20）」。
- 使用者說開始做，又回答了 8 個問題，都照建議；決定與結果寫在「現況」的「開始做時的決定（2026-10-20）」與「2026-10-20 做完的結果」。
- 照「要做的」做完 5 點，本 task 完成；「要做的」第 1 點的 Raised 依開始做時的決定改成 2026-10-04。
- 第 10 行與第 18 行連到的 `Tasks.md` 與 `Tasks-tw.md` 已刪除，連結改成 inline code，字句沒有改。
