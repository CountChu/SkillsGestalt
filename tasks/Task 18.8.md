# Task 18.8 - MermaidView-RSDC

**Status**：尚未開始——舊格式（粗體標題），單獨檢查有 6 項 FAIL；最後一節「How This Version Came About」要決定怎麼處理。
**Raised**：2026-10-10，[[Task 18]] 提出時查的 8 份已寫好的 RSDC 之一。
**Depends on**：—

## 1. 背景

讓 [MermaidView-RSDC.md](../mods/mermaid-view/MermaidView-RSDC.md)，也就是 mermaid-view 的 design of record，跟上 App 範本。
共用的規則與決定，見 [[Task 18]]。

## 2. 現況

### 2026-10-11 重新查過

- **MermaidView-RSDC**：2026-10-10 有一次 commit（24fc273），那是 mermaid-view 本身的修改，不是對齊；形狀仍是舊的。

### 2026-10-18 查的結果

- `check_rsdc.py --rsdc` 單獨檢查有 6 項 FAIL：header quote 沒有連到標準與範本、標題不是 `# {SYSTEM} - RSDC`、四章的標題、小節不是 N.M 編號，以及範本的必要小節不齊。
- 914 行；中英對照另有 1 項 FAIL：中文版 4.1 多了一個 `\s`。
- 最後一節「How This Version Came About」寫的是這份文件的來歷；[[Task 58]] 的規則只讓 RSDC 文件的 Changes in This Version 一節記錄變更，而 App 範本沒有這一節。
- 這個 repo 裡沒有檔案引用它；它的程式碼不在這個 repo。

## 3. 要做的

照 [[Task 18]] 2026-10-18 的決定對齊：照範本手動改，節號改了，引用處同一次一起改。

## 4. 驗證

—

## 5. 與其他 task 的關係

- [[Task 58]]：不寫來歷的規則。
- [[Task 60]]：記下單獨檢查的 6 項 FAIL。

## 6. 知識

—

## 7. 日誌

### 2026-10-18

- 從 [[Task 18]] 拆出；屬於這份 RSDC 的內容搬到這裡，內容沒有改。
- 補上 2026-10-18 查的結果。

### 2026-10-11

- 重新查過：2026-10-10 那次 commit 是 mermaid-view 本身的修改，形狀仍是舊的。

### 2026-10-10

- 列為 [[Task 18]] 要對齊的 RSDC 之一。
