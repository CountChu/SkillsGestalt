# Task 18.8 - MermaidView-RSDC

**Status**：完成——照 App 範本對齊，單獨、中英對照與指紋三種檢查都 PASS。
**Raised**：2026-10-10，[[Task 18]] 提出時查的 8 份已寫好的 RSDC 之一。
**Depends on**：—

## 1. 背景

讓 [MermaidView-RSDC.md](../mods/mermaid-view/MermaidView-RSDC.md)，也就是 mermaid-view 的 design of record，跟上 App 範本。
共用的規則與決定，見 [[Task 18]]。

## 2. 現況

### 2026-10-31 對齊之後

- 英文版與中文版各 921 行，逐行對齊；最後一節「How This Version Came About」已刪除。
- `check_rsdc.py --rsdc` 單獨檢查：27 項通過、0 項失敗、2 項警告。
  兩項警告都接受：2.8 的節名加了說明，不在範本的節名裡；4.1 的「version 3.9」被讀成引用 3.9 節。
- `check_rsdc.py --rsdc --tw` 中英對照：13 項通過、0 項失敗；與範本共用的句子，中文版都照範本的中文版寫。
- `check_parity.py` 0 failure，2 項警告都保留：L14 是照抄範本中文版的共用句子，L766 是畫面上的按鈕文字。
- `depends_on.py check`：英文版與中文版的三個指紋都 UNCHANGED，2026-10-31 重記。
- 2026-10-18 記下的中文版 4.1 多一個 `\s`，已在重寫中文版時一併修正。

### App 範本（2026-10-31）

- **App 範本是 [RSDC-App-tmp.md](../skill-groups/common/skills/gen-rsdc-app/assets/RSDC-App-tmp.md)**，旁邊有中文版 RSDC-App-tmp-tw.md。
  它是寫 app 的 RSDC 時用的骨架：四章的章名、每一節的節名與順序都已定好，要填的內容以 `{PLACEHOLDER}` 標出，開頭是 `>` 的行是寫作指示，寫完就刪。
- **節分兩種**：標 **Optional** 的節，app 沒有內容就省略；沒標的是必要節，`check_rsdc.py` 會查它在不在，節名要一字不差，或以節名加一個空格開頭。
- **另一份範本是 RSDC-Skill-System-tmp**，給幾個 skill 組成的系統用，例如 [[Task 18.2]] 的 SkillCompiler-RSDC；App 範本的例子是 [[Task 18.7]] 的 Home-RSDC。
- **App 範本預設的 app 是 hub 底下的那種**：以 `node server.js` 啟動，有 HTTP 路由，讀自己的 `app.config.json`，可以由 hub 載入。
- **mermaid-view 不是這種 app**：它由 Finder Quick Action、Claude Code mod，以及頁面載入的 Page Script 與 Page Style 組成，沒有 server、沒有設定檔，也不由 hub 載入。
  所以 App 範本有這些地方，mermaid-view 沒有內容可寫：
  - 必要節 2.5 Config Schemas、2.8 HTTP API、2.9 Mountable Handler；
  - 1.4 的目標「Opens from the hub, runs alone」，以及 2.10 目標表裡對應的那一列；
  - 3.1 的「Node serves and spawns; Python decides.」一段；
  - 4.1 到 4.3 為 `server.js`、`app.js`、Node 與 Python 寫好的幾條規則。

### 2026-10-11 重新查過

- **MermaidView-RSDC**：2026-10-10 有一次 commit（24fc273），那是 mermaid-view 本身的修改，不是對齊；形狀仍是舊的。

### 2026-10-18 查的結果

- `check_rsdc.py --rsdc` 單獨檢查有 6 項 FAIL：header quote 沒有連到標準與範本、標題不是 `# {SYSTEM} - RSDC`、四章的標題、小節不是 N.M 編號，以及範本的必要小節不齊。
- 914 行；中英對照另有 1 項 FAIL：中文版 4.1 多了一個 `\s`。
- 最後一節「How This Version Came About」寫的是這份文件的來歷；[[Task 58]] 的規則只讓 RSDC 文件的 Changes in This Version 一節記錄變更，而 App 範本沒有這一節。
- 這個 repo 裡沒有檔案引用它；它的程式碼不在這個 repo。

## 3. 要做的

照 [[Task 18]] 2026-10-18 的決定對齊：照範本手動改，節號改了，引用處同一次一起改。

### 已決定（2026-10-31）

使用者回答了 9 個問題，都照建議：

1. **照 App 範本寫。**
2. **沒有內容可寫的必要節保留節名**：2.5 Config Schemas 與 2.9 Mountable Handler 各寫明 mermaid-view 沒有這一項，以及原因；hub 的目標不放進 1.4。
3. **兩個入口寫在 2.8**：節名寫成 `2.8 HTTP API — none; the two entrances`，Quick Action、`/mermaid <file>` 與 `/mermaid` 各照 Takes、Answers、Refuses 寫，下面加 Guards。
4. **「How This Version Came About」刪掉**，來歷留在 git 歷史。
5. **4.3 與 4.6 依性質拆開**：違反第 2 章的 3 項放進 4.6 Defects；其餘寫進 4.3，或併進 4.5 未驗證的列；4.3 補上 escape 與 strict mode 等現有的安全做法。
6. **Inside Highlight 的圖與表搬到 3.2 的 Page Script**；它的順序規則以文字寫進 2.6 的「The Order of a Marking」。
7. **Stage Read/Write Table 與 Data Read/Write Rules 的表刪掉**；DFD 畫不出的內容，例如 outcome 由三個 stage 各寫一部分，寫進 Data Read/Write Rules 的條列。
8. **中文版照 chinese skill 整份重寫**：原句沒變的沿用舊譯法。
9. **不讀已安裝的程式核對**：只搬移內容、改形狀，不加新發現。

## 4. 驗證

照 [[Task 18]] 的「驗證」，結果見「現況」一章的「2026-10-31 對齊之後」：

- `check_rsdc.py --rsdc` 單獨檢查 PASS。
- `check_rsdc.py --rsdc --tw` 中英對照 PASS。
- `check_parity.py` 0 failure；中文版是整份重寫，不跑 `diff_md.py --verify`。
- `depends_on.py check` 的每個指紋都 UNCHANGED。
- 沒有 SKILL.md 引用 MermaidView-RSDC，所以沒有 `--skill` 檢查。

## 5. 與其他 task 的關係

- [[Task 58]]：不寫來歷的規則。
- [[Task 60]]：記下單獨檢查的 6 項 FAIL。

## 6. 知識

### 適合寫成新 topic

—

### 適合併進現有 topic

—

### 不算知識

- **`check_parity.py` 把一次定義兩個詞的 term 讀成一個 term**：2.1 的 `- **Component** and **line** —` 與 `- **Upstream** and **downstream** —`，被讀成 `Component** and **line` 這樣一整串。
  中文版只好把這兩條的標籤整段留英文；要修，就改它讀 glossary term 的 regex，或把英文拆成兩條，留給另一個 task。
- **App 範本只為 server 型的 app 寫**：mermaid-view 這類不是 server 的 app，有三個必要節只能寫「沒有」。

## 7. 日誌

### 2026-11-02

- 連結的目標路徑從 `../.github/` 改成 `../skill-groups/`，字句沒有改（[[Task 97.7]]）。

### 2026-10-31

- 開始對齊前，比對了 MermaidView-RSDC 與 App 範本，發現 mermaid-view 不是範本預設的 server 型 app。
- 「現況」一章加上「App 範本」一節：範本是什麼，以及 mermaid-view 沒有內容可寫的地方。
- 「要做的」一章加上「要決定的」5 項：第 1 項是要不要套 App 範本，第 4 項由 [[Task 18]] 的「要決定的」移來。
- Status 行的結論跟著改。
- 使用者決定照 App 範本寫，並回答了其餘 8 個問題；「要決定的」改成「已決定」。
- MermaidView-RSDC 照 App 範本對齊，中文版照 chinese skill 整份重寫；三種檢查都 PASS，本 task 完成。
- 「現況」、「驗證」與「知識」三章跟著補上。

### 2026-10-18

- 從 [[Task 18]] 拆出；屬於這份 RSDC 的內容搬到這裡，內容沒有改。
- 補上 2026-10-18 查的結果。

### 2026-10-11

- 重新查過：2026-10-10 那次 commit 是 mermaid-view 本身的修改，形狀仍是舊的。

### 2026-10-10

- 列為 [[Task 18]] 要對齊的 RSDC 之一。
