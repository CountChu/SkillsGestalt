# Task 76 - skill-writing.md 加一條規則：skill 執行的程式不呼叫 LLM

**Status**：尚未開始——規則的位置與措辭方向已決定，還沒寫；SkillCompiler-RSDC 3.1 的兩句要不要改，也留給本 task。
**Raised**：2026-10-20，[[Task 18.2]] 對齊 SkillCompiler-RSDC 時，使用者問要不要加一條「skill 所使用的 system 不應該使用 LLM」的 rule、該加在哪裡。
**Depends on**：—

## 1. 背景

現在沒有任何 rule 明說 skill 執行的程式不可以呼叫 LLM：

- Skill-System template 的固定句（1.4 的 No tokens、2.10 的 No LLM, anywhere，以及第 3 章「不寫 agent 或 LLM 的 step」）是 template，不是 rule。
- gen-rsdc-skill 把 system 定義成 deterministic、不用 LLM 的 Python script，但只約束它處理的 skill。
- [skill-writing.md](../.github/common/rules/skill-writing.md) 第 38 行規定程式能確定地做的 step 交給 script，要讀文字、做判斷、寫摘要的 step 交給 agent，但沒有說 script 不呼叫 LLM。

## 2. 現況

### 已決定（2026-10-20）

- **放在 skill-writing.md**，接在第 38 行那條規則之後：它決定哪些 step 交給 script；gen-skill 照它寫 skill，check-skill 照它檢查。
- **以程式為準，不以 system 為準**：大意是「skill 執行的程式不呼叫 LLM；需要 LLM 的工作，是 agent 照 SKILL.md 的指示做的 step」。
  照 [[Task 18.2]] 的決定，SkillCompiler 的 Compiler（AI agent）留在系統內；以 system 為準，SkillCompiler 就違反規則，以程式為準則符合，因為它的三支程式都不呼叫 LLM。
- **不放的地方**：RSDC-Standard 也管 app，它的範例 ArtifactFlowAgent 本身有 Agent 層；Skill-System template 不是 rule；SKILL template 的 MUST FOLLOW 會把規則抄進每份 SKILL.md，而 skill-writing.md 規定寫 skill 的規則不放進 SKILL.md。

### SkillCompiler-RSDC 3.1 的兩句（2026-10-21）

[[Task 77]] 把 compile-skill 的編譯做法寫成 compile SOP（SKILL-Compile.md）：SOP 只寫 agent 的判斷，不執行、也不提任何程式；Source Scanner、Contract Checker 與 Compiled Script 都由 SKILL.md 執行，再把結果交給 SOP 的 step。
[SkillCompiler-RSDC.md](../.github/common/skills/compile-skill/references/SkillCompiler-RSDC.md) 沒有跟著改，其中兩句仍寫成 Compiler 執行程式：

- 第 593 行，3.1 的 How they interact：Compiler 從命令列執行 Source Scanner 與 Contract Checker、讀它們印出的內容，並以 caller 的方式執行 Compiled Script。
- 第 604 行，3.2 Compiler 的開頭：Compiler 先做 Compile，再做 Verify。

在 RSDC 裡，Compiler 指整個做編譯的 AI agent，它照 SKILL.md 去執行程式，所以這兩句沒有錯；3.1 的分工，以及第 567 行的「whatever procedure it follows」，都和新的做法一致。
使用者決定 RSDC 先不改，留給本 task 決定這兩句要不要改成「做編譯的 skill 執行程式，再把結果交給 Compiler」，寫出 system 與 agent 互不認識、由 skill 調控。
範圍只有這兩句，[[Task 18.2]] 的「Compiler 留在系統內」不重新討論。

## 3. 要做的

1. 以 STE 寫這條規則，放在 skill-writing.md 第 38 行那條之後；`check_ste.py --ste` PASS。
2. skill-writing-tw.md 照 [chinese](../.github/common/skills/chinese/SKILL.md) skill 更新。
3. 記錄 skill-writing.md 的檔案，以 `depends_on.py check` 找出來，讀過之後重記。
4. 決定 check-skill 要不要加一項檢查，例如找 script 裡的 LLM client。
5. 決定 SkillCompiler-RSDC 3.1 第 593 行與 3.2 第 604 行要不要改成由 skill 執行程式、再把結果交給 Compiler，見「現況」；要改的話，中文版照 chinese skill 一起改。

## 4. 驗證

- `check_ste.py --ste` PASS，警告和改之前相同。
- skill-writing.md 中英兩份的 `check_parity.py` 0 failure；中文版以 INCREMENTAL 更新時，`diff_md.py --verify` PASS。
- 記錄 skill-writing.md 的每一份檔案，`depends_on.py check` 都是 UNCHANGED。
- 若改了 SkillCompiler-RSDC：`check_rsdc.py --rsdc` 單獨與中英對照都 PASS；中文版的 `check_parity.py` 0 failure，`diff_md.py --verify` PASS。
  compile-skill 的 README 與中文版記的 `[[SkillCompiler-RSDC]]` 指紋會變成 CHANGED，讀過 SKILL-Compile.md、確認它仍成立之後重記。

## 5. 與其他 task 的關係

- [[Task 18.2]]：使用者在這裡提出，並決定 Compiler 留在 SkillCompiler 的系統內。
- [[Task 77]]：compile SOP 只寫 agent 的判斷，程式由 SKILL.md 執行；RSDC 3.1 那兩句要不要跟著改，留給本 task。

## 6. 知識

—

## 7. 日誌

### 2026-10-21

- 從 [[Task 77]] 轉來：SkillCompiler-RSDC 3.1 第 593 行與 3.2 第 604 行要不要改成由 skill 執行程式，使用者決定留給本 task；「現況」「要做的」與「驗證」各加一項。

### 2026-10-20

- 提出：使用者問要不要加這條 rule、加在哪裡，決定放在 skill-writing.md、以程式為準，另開本 task。
