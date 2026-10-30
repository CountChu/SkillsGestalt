# Task 72 - 建 Agentic Panel

**Status**：尚未開始——設計是它從 SkillCompiler-RSDC 移出時的樣子，還沒有人開始做。
**Raised**：2026-10-04，Agentic Panel 的設計從 SkillCompiler-RSDC 移出，在 compile-skill 的 Tasks.md 留成一項待辦。
**Depends on**：—

## 1. 背景

本 task 是圍繞 skill compiler、但它的 design document——[SkillCompiler-RSDC.md](../.github/common/skills/compile-skill/references/SkillCompiler-RSDC.md)——沒有涵蓋的待辦工作。
本 task 依賴那份文件；那份文件從不依賴本 task。
design document 不點名 Agentic Panel：對它來說，panel 只是又一個 caller（§2.1 *Terminology*）——一個依 Compiled Script 的 introspection 建立互動流程的使用者介面（§2.7 *CLI*）。
它自己的設計已從那份文件移出，因為沒有任何 compiler 會產出它，而 design document 也不點名使用它所規定之內容的應用程式。
「要做的」是它被移出時的那份設計——給日後實作 Agentic Panel 的人作為起點，也是屆時它自己那份 design document 的雛形。

## 2. 現況

### 2026-10-20 移來時的狀態

- 還沒有人開始做；Tasks.md 寫的 Status 是 not started。
- 這個 workspace 還沒有 Location 寫的 `system/` 目錄。
- 「要做的」引用的節號，已改成 SkillCompiler-RSDC 照 template 對齊後的節號（[[Task 18.2]]）。

## 3. 要做的

### What it must keep

以下是 design document（[SkillCompiler-RSDC.md](../.github/common/skills/compile-skill/references/SkillCompiler-RSDC.md)）的規則，只引用、不重述，使 Agentic Panel 在規則改變時跟著遵守：

- 它只透過 Compiled Script 的 introspection 與執行來使用 script（§2.7 *CLI*）。
- 它以 exit status 分辨成功、refusal、stale script 的 refusal 與 handoff，絕不把 refusal 或 handoff 當成成功（§2.2 *Artifact Types* 中的 outcome 定義；§2.7 *CLI* 中的 exit status）。
- 它絕不提供執行 Cognitive step 的選項，而是顯示 handoff（§2.7 *CLI*、§2.8 *Invariants*）。
- 它絕不向人索取 credential，也絕不把 credential 放在命令列上傳遞（§2.3 *Dataflow*，它的 Data Read/Write Rules）。

### Component

**Agentic Panel App**：一個獨立存在的全域 UI 應用程式，負責執行 introspection 指令，將它的 JSON 渲染為 step 列表與 Prompt Area，並針對 Cognitive step 提供明確的 handoff 提示。
人在某個 skill 的目錄上啟動它；它讀取 script 的 introspection，並把人輸入的內容轉成 `skill.py` 的命令列選項來執行一個 step。
在 design document 的 Dataflow 中，它是 Introspect 與 Run a step 的 caller。

### Location

```text
system/
`-- agentic_panel.py   (Agentic Panel: independent UI panel that parses and drives skills)
```

它位於每一個 skill 的目錄之外，也沒有任何 skill 依賴它。

### Implementation choices

- 使用 Python 原生的 `subprocess.run` 搭配 `--export-schema` 來擷取目標 skill 的 JSON。
- **UI 框架與渲染**：推薦使用 Textual、Streamlit 或 Gradio。
  讀取每個 step 的 `type` 欄位後：
  - 若為 `deterministic_automated`，因不需使用者輸入 variable，可直接在清單上顯示一鍵執行按鈕。
  - 若為 `deterministic_interactive`，在展開的 Prompt Area 中顯示常規的輸入表單——每個參數一個控制項，依它的 `type` 選擇：`path` 用檔案路徑選擇器，`boolean` 用核取方塊，其餘用文字框——並提供執行按鈕。
  - 若為 `cognitive_automated` 或 `cognitive_interactive`，則**隱藏執行按鈕**，並在 Prompt Area 給予高度顯眼的強調框（如紅色或黃底黑字），顯示：**`Warning: This step is a cognitive task and cannot be processed by this system. Please have the user invoke the Skill separately.`**

## 4. 驗證

—

## 5. 與其他 task 的關係

- **[[Task 71]]**（2026-10-20）：把本 task 從 compile-skill 的 Tasks.md 移到這裡；Tasks.md 與中文版已刪除。
- **[[Task 18.2]]**（2026-10-20）：對齊 SkillCompiler-RSDC，本 task 引用的節號同一次改成對齊後的節號。
  §2.1 *Artifact Types and Flow* 依引用的內容改成 §2.1 *Terminology* 或 §2.2 *Artifact Types*，§2.4 *CLI* 改成 §2.7 *CLI*，§2.1 *Active Prompt Rule for Cognitive Steps* 改成 §2.7 *CLI* 與 §2.8 *Invariants*。

## 6. 日誌

### 2026-10-20

- 從 compile-skill 的 Tasks.md 移到這裡（[[Task 71]]）：內容照 Tasks-tw.md 逐句搬，「腳本」改成 script，講那份檔與「以下」的字改成講本 task 與「要做的」，其餘字句沒有改。
- 「背景」與 What it must keep 各加一個連到 SkillCompiler-RSDC.md 的連結；「現況」寫的是移來時的狀態。
- 「背景」與「要做的」引用 SkillCompiler-RSDC 的節號，改成 [[Task 18.2]] 對齊後的節號，其餘字句沒有改；「現況」與「與其他 task 的關係」照這次的改動改寫。

### 2026-10-04

- 寫進 compile-skill 的 Tasks.md，是那裡唯一的一項，Status 是 not started。
