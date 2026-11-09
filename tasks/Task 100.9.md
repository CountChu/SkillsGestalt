# Task 100.9 - write-note 系列不寫暫存檔，MUST FOLLOW 卻提到 scratch files

**Status**：完成——三個 skill 的 MUST FOLLOW 拿掉「and the scratch files」，和 add-tags 一致。
**Raised**：2026-11-06，[[Task 100.7]] 時發現 write-note 一系列的 MUST FOLLOW 寫著遵守 run-data-rules 的 scratch files，但它們不寫暫存檔。
**Depends on**：—

## 1. 背景

- write-note、write-note-new-files、write-note-tags 的 MUST FOLLOW 都寫著：
  > Obey run-data-rules.md for the Run Number, the run record and the scratch files of a run.
- 這三個 skill 都沒有 script，也不在 `temp\` 寫任何東西。
- 其他不寫暫存檔的 skill，例如 add-tags，這一句只寫「the Run Number and the run record」。

## 2. 結論

—

## 3. 過程

### 已決定（2026-11-06）

- 使用者選 A：拿掉「and the scratch files」。

### 2026-11-06 改好之後

- write-note `f874161`、write-note-new-files `d62b3ef`、write-note-tags `0565f30`：MUST FOLLOW 那一句改成「for the Run Number and the run record of a run.」。
- `git grep -n 'scratch files of a run'` 在這三個 skill 沒有輸出。

### 2026-11-06 的狀況

- 多寫的「scratch files」讓讀者以為這個 skill 會寫暫存檔；check-skill 也可能判定這一句與步驟不合。

## 4. 要做的

1. 請使用者從下面的選項決定。
   - **A（建議）**：三個 skill 拿掉「and the scratch files」，和 add-tags 一致；只改這一句。
   - **B**：保留，以後加了 script 就會用到。
2. 照決定改，一個 skill 一個 commit。

## 5. 驗證

- `git grep -n 'scratch files of a run' -- skill-groups/common/skills/write-note*` 照決定的結果：A 沒有輸出，B 照舊。

## 6. 與其他 task 的關係

- [[Task 100]]：本 task 的上層。
- [[Task 100.6]]：替這三個 skill 加上 run record 時寫了這一句。
- [[Task 100.7]]：發現這個問題。

## 7. 知識

—

## 8. 日誌

### 2026-11-06

- 做完：使用者選 A，三個 skill 拿掉「and the scratch files」。
- 提出。
