# Task 100.10 - set-tag-status 與 check-wiki-doc 在 CONFIGURATION 多列的輸出

**Status**：完成——使用者決定保留這 3 行，檔案不改。
**Raised**：2026-11-06，[[Task 100.7]] 要 subagent 只重新分組，但它在兩個 skill 補上了原本沒列的輸出。
**Depends on**：—

## 1. 背景

- [[Task 100.7]] 的說明只要求把 CONFIGURATION 原有的行分成兩組。
- 改 set-tag-status 與 check-wiki-doc 的 subagent 補上了它們寫出、但原本沒列的東西。

## 2. 結論

—

## 3. 過程

### 已決定（2026-11-06）

- 使用者選 A：保留 set-tag-status 的 Tags file，以及 check-wiki-doc 的 HTML 依賴圖與架構文件兩行；CONFIGURATION 列出 skill 寫出的每一項。
- 兩個 SKILL.md 不改；這 3 行在 [[Task 100.7]] 的 commit 裡（set-tag-status `225df9b`、check-wiki-doc `bba7ad9`）。

### 2026-11-06 的狀況

- **set-tag-status**：多了 **Tags file** `database\tags.yaml`；這個 skill 的主要工作就是改其中一個 tag 的 status。
- **check-wiki-doc**：多了兩行：
  - **HTML 依賴圖**：架構文件旁邊的 `{架構文件名}-文件依賴圖.html`；
  - **架構文件與待查文件**：步驟 4 寫回結果與檔頭紀錄，步驟 5 經使用者同意後修改它們。
- 這幾項確實是它們寫出的東西，但超出了「只重新分組」的範圍。

## 4. 要做的

1. 請使用者從下面的選項決定。
   - **A（建議）**：保留；範本的意思是 CONFIGURATION 列出 skill 寫出的每一項。
   - **B**：拿掉這 3 行，回到只重新分組。
2. 照決定改，一個 skill 一個 commit。

## 5. 驗證

- 兩個 SKILL.md 的 CONFIGURATION 照決定的結果。

## 6. 與其他 task 的關係

- [[Task 100]]：本 task 的上層。
- [[Task 100.7]]：多列的輸出是在這個 task 加的。

## 7. 知識

—

## 8. 日誌

### 2026-11-06

- 做完：使用者選 A，保留這 3 行，檔案不改。
- 提出。
