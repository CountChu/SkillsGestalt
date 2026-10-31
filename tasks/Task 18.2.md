# Task 18.2 - SkillCompiler-RSDC

**Status**：完成——2026-10-20 照 Skill-System template 手動對齊，英文版從 658 行變成 801 行；單獨、中英對照與 compile-skill 的 `--skill` 三種檢查都 PASS，引用它節號的地方一起改。
**Raised**：2026-10-10，[[Task 18]] 提出時查的 8 份已寫好的 RSDC 之一。
**Depends on**：—

## 1. 背景

讓 compile-skill 的 [SkillCompiler-RSDC.md](../.github/common/skills/compile-skill/references/SkillCompiler-RSDC.md) 跟上 Skill-System 範本。
共用的規則與決定，見 [[Task 18]]。

## 2. 現況

### 2026-10-10 查的結果

- **SkillCompiler-RSDC**（compile-skill 的 `references/`）：舊格式（粗體標題），沒有檔頭引用區；第 3 章還是標準的舊順序（3.2 Directory Structure、3.3 Execution Flow）。

### 2026-10-18 查的結果

- `check_rsdc.py --rsdc` 單獨檢查有 6 項 FAIL：header quote 沒有連到標準與範本、標題不是 `# {SYSTEM} - RSDC`、四章的標題、小節不是 N.M 編號，以及範本的必要小節不齊。
- 658 行；引用它的是 compile-skill、check-md-deps、gen-rsdc-skill 的 SKILL.md 與中文版，以及 [[Task 72]]（原本是 compile-skill 的 Tasks.md 與中文版）；`depends_on.py` 的 docstring 拿它當範例。

### 決定（2026-10-20）

使用者回答了 11 個問題，除了 1.1 之外都照建議：

- **Compiler 留在系統內**：Compile 與 Verify 由 AI agent（Compiler）執行，要花 token。
  template 的 1.4 No tokens、2.10 No LLM, anywhere，以及第 3 章「不寫 agent 或 LLM 的 step」照實情改寫：只有 compile phase 花 token，system 的程式都不呼叫 LLM。
  使用者也說 template 不是 rule，並問要不要加一條不用 LLM 的 rule，決定另開 [[Task 76]]。
- **第 2 章的子節照 template 的節分散**：原 2.1 的三個子節分到 2.1 Terminology、2.5 Derivation Rules、2.3 Exception Paths、2.7 CLI 與 2.8 Invariants。
  2.5 分成 Step Identifier、Action Type、Core Work or Chore 與 Source Fingerprint 四個小節。
  2.3 只留一張 DFD，原本的讀寫表併進 DFD 與 Data Read/Write Rules，Inside Compile 與 Inside Verify 移到 3.2 Execution Flow 的 Compiler 之下。
  Config Schemas、Rule Constants 與 Platform Traps 沒有內容，不寫。
- **skill.py 被程式讀的部分移到 2.4**：`SOURCE_SHA256`、`COMPILED_AT` 與 docstring 記下的 chore 判定，寫成 Compiled Script 的欄位。
  compile-skill 引用第 3、4 章與 Inside Compile、Inside Verify 的地方，照 [[Task 18.7]] 改成不帶節號的說法。
- **Defects**：讀程式時看到的三處列進 4.5，另開 [[Task 74]] 改程式。
- **`--timeout` 的預設值**：保留，寫成設計；4.1 不列 No default for an input value。
- **拼法**：自己的句子改成美式；與 template 共用的句子照抄 template，所以第 754 行的 behaviour 留著。
- **1.1**：保留 AI automation agents，列三種使用者；3.1 另寫 Compiler。
- **gen-rsdc-skill 的範例引用**：`--skill` 的那一項 FAIL 記為已知誤判，另開 [[Task 75]]；第 260 行照新的 2.3 確認仍成立之後重記指紋。
- **commit**：一個 commit，三個新 task 一起提出。

### 進度

- 英文版：照 template 重寫成 801 行；header quote 連到 `[[RSDC-Standard]]`、`[[DFD]]` 與 `[[RSDC-Skill-System-tmp]]`，以 `depends_on.py record` 記下指紋。
  stage 是 Compile、Verify、Check freshness、Introspect 與 Run a step；role 是 person revising the skill、person compiling 與 caller；record 是 Compiled Script 與 step outputs。
  目標名稱縮短，例如 Stable before compiling；goals 表 7 列。
  新寫的是 2.6 Presentation Contract、2.8 Invariants、3.1 各 component 的工作與邊界、3.2 的 Compiled Script 與 4.5 Defects，依據是原文與兩支 script。
- 中文版：照 chinese skill 更新，判定 INCREMENTAL，change set 是 801 行中的 604 行。
  change set 以外的 197 行逐字保留，與 template 共用的句子照抄 template 的中文版，其餘翻譯；Terminology、Artifact Types 定義的詞與 stage 名稱保留英文。
- compile-skill 的 SKILL.md：42 處 § 引用改成 33 處，都在第 1、2 章；引用第 3、4 章的地方改成不帶節號的說法，改到的行把 judgement 改成 judgment。
  中文版照 chinese skill 只改那幾行，改到的句子把「識別碼」「腳本」改回英文。
- [[Task 72]]（原 Tasks.md）：引用的節號改成新的，並在它的日誌記一行。
- `scan_source.py` 與 `check_compiled.py`：docstring 與註解裡的節號改成新的。
- 重記：compile-skill 與 gen-rsdc-skill 的 SKILL.md 與中文版裡 `[[SkillCompiler-RSDC]]` 的 `cited` 指紋。

### 順帶發現

- 中文版還有 12 行「腳本」，以及 4 行措辭和 template 中文版不同的共用句子，都在 change set 以外，照規則逐字保留；「腳本」屬於 [[Task 73]]。
  [[Task 73]] 的稽核數字是這次改之前的：SkillCompiler-RSDC-tw.md 從 67 行降到 12 行，compile-skill 的 SKILL-tw.md 也少了 3 行。
- compile-skill 的 SKILL.md 沒有「# Dataflow」一節，`--skill` 檢查報 WARN；HEAD 就有，屬於 [[Task 24]] 要改的 skill 格式。
- [[Task 71]] 的「與其他 task 的關係」預計 §2.4 *CLI* 會變成 §2.8 *CLI*，實際是 §2.7 *CLI*，因為 Config Schemas 沒寫。

## 3. 要做的

✅ 2026-10-20 照 template 對齊，中文版、compile-skill 的 SKILL.md、[[Task 72]] 與兩支 script 的引用一起改。

## 4. 驗證

- 英文版單獨檢查 `check_rsdc.py --rsdc --skill-name compile-skill` PASS，30 項通過，0 個警告。
- 中英對照 `check_rsdc.py --rsdc --tw --keep` PASS，13 項通過，2 個警告，見「順帶發現」。
- compile-skill 的 `check_rsdc.py --rsdc --skill` PASS：33 處 § 引用都落在寫出節名的那一節，也沒有引用 Design 與 Coding；1 個警告，見「順帶發現」。
- gen-rsdc-skill 的 `--skill` 判 FAIL，9 項通過、1 項失敗：第 587、599 行的 4 個範例引用，是已知誤判，見 [[Task 75]]；第 260 行的 §2.3 *Dataflow* 通過。
- SkillCompiler-RSDC 與 compile-skill、gen-rsdc-skill 的 SKILL.md，三對 `check_parity.py` 都是 0 failure，`diff_md.py --verify` 都 PASS；警告都在沒有改的行上，SKILL.md 的警告少於 HEAD。
- `depends_on.py check`：SkillCompiler-RSDC 與中文版的 3 個指紋，以及四份 SKILL 的 `[[SkillCompiler-RSDC]]`，都是 UNCHANGED。
- 英文版與中文版以 `reformat_md.py --mode clean` 重排後都沒有差異；英文版的英式拼法只剩第 754 行 template 共用句的 behaviour。
- 兩支 script 以 `py_compile` 編譯通過，`scan_source.py` 照常判定 compile-skill 的 SKILL.md 為 valid。

## 5. 與其他 task 的關係

- [[Task 60]]：記下單獨檢查的 6 項 FAIL。
- [[Task 71]]、[[Task 72]]：compile-skill 的 Tasks.md 移到 [[Task 72]]，所以這次改的是 [[Task 72]] 的引用。
- [[Task 73]]：中文版剩下的「腳本」。
- [[Task 74]]、[[Task 75]]、[[Task 76]]：這次提出的三個 task。
- [[Task 24]]：compile-skill 的 SKILL.md 沒有 Dataflow 一節，屬於它要改的 skill 格式。
- [[Task 58]]：寫新的內容時照它的規則，不寫文件自己的來歷。

## 6. 知識

—

## 7. 日誌

### 2026-10-20

- compile-skill 的 Tasks.md 與中文版已刪除，內容移到 [[Task 72]]；「2026-10-18 查的結果」列的引用處，這一項改寫成 [[Task 72]]，其餘字句沒有改（[[Task 71]]）。
- 使用者決定先做本 task；回答了 11 個問題，決定寫在「現況」的「決定（2026-10-20）」。
- 英文版照 template 重寫，中文版照 chinese skill 更新；compile-skill 的 SKILL.md 與中文版、[[Task 72]] 與兩支 script 的引用一起改，四份 SKILL 重記指紋。
- 提出 [[Task 74]]、[[Task 75]] 與 [[Task 76]]。

### 2026-10-18

- 從 [[Task 18]] 拆出；屬於這份 RSDC 的內容搬到這裡，內容沒有改。
- 補上 2026-10-18 查的結果。

### 2026-10-10

- 列為 [[Task 18]] 要對齊的 RSDC 之一。
