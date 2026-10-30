# Task 1 - 決定 Skill Source 是否改名為 Skill MD File

**Status**：完成——2026-10-09 決定不改名；改為把 gen-rsdc-skill 字彙表裡的定義寫清楚。
**Raised**：2026-10-09，編輯 gen-rsdc-skill 的 `SKILL-tw.md` 時提出。
**Depends on**：—

## 1. 背景

提議：把寫成 skill 的那份 `SKILL.md` 改稱為 **Skill MD File**，不再稱為 **Skill Source**。
改名必須涵蓋以下範圍，一個檔案才會始終只有一個名稱：

- **這個術語屬於 compile-skill。**
  **Skill Source** 是 [SkillCompiler-RSDC.md](../.github/common/skills/compile-skill/references/SkillCompiler-RSDC.md) 的一種 artifact type（§2.1 *Artifact Types and Flow*），通篇使用，也出現在它的 twin、compile-skill 的 `SKILL.md` 與其 twin，以及 `scan_source.py` 與 `check_compiled.py` 印出的訊息中。
  在那裡，這個詞帶著一組對比：Skill Source 是 compiler 轉成 Compiled Script 的那一方。
  改名要從那份 design document 開始，並且要刻意決定保留或放棄這組對比。
- **gen-rsdc-skill 借用了它。**
  它的字彙表、CONFIGURATION 與各個 step 都稱這個檔案為 **Skill Source**，而它的 Step 1 讀的是 `scan_source.py` 的輸出，那裡也用同一個名稱指這個檔案。
  只在 gen-rsdc-skill 改名，skill 和它所執行的 scanner 就會用兩個名稱指同一個檔案。
- **twin 不能單獨改術語。**
  繁體中文 twin 的每一個字彙表術語都保留英文，拼法與英文檔相同，所以 `SKILL-tw.md` 只能與 `SKILL.md` 一起改——chinese skill 的 parity check 也會在兩份中比對這個術語。

### 評估

評估（2026-10-09）：上面三點都正確，但範圍漏了幾項，而且新名稱不比舊名稱好。

- **漏掉的範圍**：
  - 散文：repo 內 8 個檔案共 226 處——SkillCompiler-RSDC 與 tw 各 50、gen-rsdc-skill 的 `SKILL.md` 與 tw 各 39、compile-skill 的 `SKILL.md` 與 tw 各 18、`check_compiled.py` 7、`scan_source.py` 5。
  - 程式裡帶 "source" 的名稱：`scan_source.py` 的檔名（`check_compiled.py` import 它，兩個 skill 都依名稱執行它）、component **Source Scanner**、`check_compiled.py` 的 `--source`，以及每個已編譯的 `skill.py` 都有、`check_compiled.py` 會讀的 `SOURCE_SHA256`。
    只改散文，同一個檔案仍有兩套叫法；連這些一起改，就要重新編譯已編譯的 `skill.py`（例如 InvestForge 的 report-inv-week），或讓 `check_compiled.py` 新舊名稱都接受。
  - repo 外：`CompileSkill/docs/CompileSkill-RSDC.md` 與 tw 各 6 處（另一個 git repo 裡較舊的版本）；InvestForge report-inv-week 的 `skill.py` docstring 2 處。
- **「一個檔案只有一個名稱」不是 repo 的慣例。**
  各 skill 依檔案在自己裡面的角色命名：`chinese` skill 稱它 **source file**，gen-imp-app 稱 **skill pair**。
  要守住的是：一個 skill 與它所執行的工具之間，只用一個名稱。
- **新名稱比較差。**
  在 compile-skill，"Source" 正是 compiler 輸入的意思：與 Compiled Script 成對，新鮮度也是對照它檢查的（source fingerprint）。"
  MD File" 說的是格式而不是角色，也容易和 **MD report** 混淆。
- **真正的問題在 gen-rsdc-skill。**
  它一直拿 `SKILL.md` 和程式碼對照，例如 "a rule the Skill Source states and the code does not keep"，"Skill Source" 容易被讀成「skill 的原始碼」。
  compile-skill 沒有這個問題。

## 2. 現況

做了什麼：gen-rsdc-skill 的 `SKILL.md` 與 `SKILL-tw.md` 各改一行 **Skill Source** 的定義——寫明它是 target skill 的指示，不是它所執行之程式的程式碼；以及這個名稱沿用 compile-skill 的，為的是讓本 skill 與 Source Scanner 用同一個名稱稱呼這個檔案。

## 3. 要做的

若日後仍要改名：範圍是上面「漏掉的範圍」全部，名稱要依角色而不是格式來取。
最好和 SkillCompiler-RSDC 對齊標準一起做——它的 §2.1 還叫 *Artifact Types and Flow*（標準 261009 已改名為 Artifact Types），compile-skill 對它的引用反正要改，一起做只動一次。

## 4. 驗證

`check_parity.py` 0 failure，`scan_source.py` valid。

## 5. 與其他 task 的關係

—

## 6. 日誌

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-09

- 提出：編輯 gen-rsdc-skill 的 `SKILL-tw.md` 時，提議把 Skill Source 改名為 Skill MD File。
- 評估後決定不改名，改為把 gen-rsdc-skill 字彙表裡 Skill Source 的定義寫清楚。
- gen-rsdc-skill 的 `SKILL.md` 與 `SKILL-tw.md` 各改一行定義。
