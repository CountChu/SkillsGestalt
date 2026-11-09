# Task 100.8 - CONFIGURATION 的輸入與工具要不要有自己的一組

**Status**：完成——範本的 CONFIGURATION 以「The inputs and tools」開頭，22 個 skill 都列出它們讀取或執行的每一項。
**Raised**：2026-11-06，[[Task 100.7]] 把 CONFIGURATION 分成兩組之後，輸入與工具不屬於任何一組，只好放在兩組之前。
**Depends on**：—

## 1. 背景

- [SKILL-tmp.md](../skill-groups/common/templates/SKILL-tmp.md) 的 CONFIGURATION 分成兩組，兩組都是一次 run 寫出的東西：
  - 「The working data of a run」：暫存檔、Checkpoint Dir；
  - 「The last outputs」：run record、handoff 檔、MD report。
- 很多 skill 的 CONFIGURATION 還列了它讀取或使用的東西：
  - imp-app：document templates、session resolver、test runner、deploy tool；
  - gen-rsdc-skill：RSDC standard、RSDC template、Source Scanner、RSDC Checker；
  - chinese：source file、keep-English list；
  - asd-ste：scripts 與 references。

## 2. 結論

—

## 3. 過程

### 已決定（2026-11-06）

使用者回答了 5 個問題，都照建議：

1. 選 A：範本加第三組，放在最前面。
2. 導言是「The inputs and tools, which the run reads or runs:」，中文版是「執行時讀取或執行的輸入與工具：」。
3. 這一組列出 skill 讀取的檔、執行的 script 與使用的外部程式；skill 寫出的東西不放這裡，又讀又寫的放在最後的輸出。
4. 先改範本、gen-skill 與 check-skill，再由 subagent 改各 skill。
5. 第一輪只搬既有的行、補 config.yaml 與 script 之後，還缺不少讀取的檔；使用者決定第二輪補齊。

### 2026-11-06 改好之後

- **範本**（`0bdab8d`）：SKILL-tmp 與中文版的 CONFIGURATION 先列「The inputs and tools」，例子是 Workspace configuration 與 Scripts；開頭那句改成「不讀取、不執行或不產出的就刪掉那一行」。
- **gen-skill**：Step 3 在這一組列出 skill 讀取的檔、執行的 script 與其他程式。
- **check-skill**：準則 1.3 加上「CONFIGURATION 最多三組，順序照範本；放錯組的行是 recommendation」。
- **第一輪**：22 個 skill 把兩組之前的輸入行搬進這一組，每個都補上 Workspace configuration；write-note 一系列另補 `database\tags.yaml`。
- **第二輪**：逐個 skill 對照步驟補上讀取的檔與呼叫的 skill，例如 run-data-rules.md、md-style.md、DFD.md、範本、chinese skill、gen-rsdc-app 的 handoff 檔、node、playwright-cli。
  - gen-rsdc-skill 的 Skill Source 會被 Step 8 修改，所以留在最後的輸出，輸入組另補 README template。
  - asd-ste 的 Dependents、check-skill 的 Checked skill、check-md-deps 的 Target files 是 skill 會改寫的檔，補進最後的輸出（照 [[Task 100.10]] 的決定）。
- 每個 skill 一個 commit；依賴紀錄重記後，`skill-groups/common` 的每一份都是 UNCHANGED。

### 2026-11-06 的狀況

- [[Task 100.7]] 把這些行放在兩組之前、CONFIGURATION 的導言之後，沒有標題。
- 讀者看得出兩組是什麼，看不出最前面那幾行是什麼；gen-skill 照範本寫新 skill 時，也不知道輸入要放哪裡。

## 4. 要做的

1. 請使用者從下面的選項決定。
   - **A（建議）**：範本加第三組，放在最前面，例如「The inputs and tools, which the run reads:」；各 skill 把那幾行放進這一組；gen-skill 與 check-skill 照它寫、照它檢查。
   - **B**：不加組，範本只寫一句「輸入與工具放在兩組之前」。
   - **C**：輸入與工具不放在 CONFIGURATION，改放 Step 0 的檢查清單。
2. 照決定改 SKILL-tmp.md 與中文版、gen-skill、check-skill，以及有輸入行的 skill，中文版也是。
3. 重記依賴紀錄；在 CHANGES.md 加一筆。

## 5. 驗證

- 每個 SKILL.md 的 CONFIGURATION 都照決定的做法寫。
- 有中文版的 parity check 是 0 failure；`skill-groups/common` 的依賴紀錄都是 UNCHANGED。

## 6. 與其他 task 的關係

- [[Task 100]]：本 task 的上層。
- [[Task 100.7]]：把 CONFIGURATION 分成兩組，留下這個問題。

## 7. 知識

—

## 8. 日誌

### 2026-11-06

- 做完：範本加上「The inputs and tools」一組，22 個 skill 分兩輪補齊。
- 提出。
