# Task 68 - 把 task 檔裡的「配對行」改成 pairing line

**Status**：完成——2026-10-19 四個 task 檔與摘要表共 33 處改成 pairing line，Task 67 的標題跟著改；check_tasks.py PASS。
**Raised**：2026-10-19，做 [[Task 67]] 時發現：keep-English list 把 pairing line 留英文，task-rules 要求 task 檔照它寫，有幾個 task 檔卻寫「配對行」；`check_tasks.py` 不查 keep-English 的 term，所以沒有被發現。
**Depends on**：—

## 1. 背景

- [task-rules.md](../.github/common/rules/task-rules.md) 要求 task 檔像 TW twin 一樣，把 [tw-keep-english.md](../.github/common/references/tw-keep-english.md) 列出的每個 term 留英文；這條規則是 2026-10-18 由 [[Task 62.1]] 寫進去的。
- 清單上 pairing line 那一列的 Replaces 與 Flagged 都是「配對行」，理由是它沒有標準的中文譯法。
- Task 8、10、11、13、19、33 已經寫 pairing line；寫「配對行」的是 Task 9、31、32.11、67 與摘要表。
- `check_tasks.py` 不查 keep-English 的 term，chinese skill 的 `check_parity.py --keep` 與 [[keep-english]] 的稽核也不看 task 檔。

## 2. 現況

### 已決定（2026-10-19）

做之前分兩輪問了 8 個問題，決定如下：

- 五個檔全改，也包括規則生效前寫的 Task 9 與 Task 31。
- 新開本 task 記錄，不併進 [[Task 63]]：Task 63 決定新詞要不要加進清單，不是修正清單上已有的 term。
- Task 67 的標題改成「draft.py replace 把中文版的 pairing line 指回原檔」，摘要表的 Title 與 Task 32.11 引用這句的地方跟著改。
- 日誌裡的也改：只換名稱，日誌記錄的事情不變。
- 中英文之間留半形空格，全形標點與粗體記號旁不留，照 [[Task 48]] 的做法。
- 其他 keep-English 譯法與 `check_tasks.py` 的掃描另開 [[Task 69]]，這次都不做。
- 一個 commit，前綴 `task 68: `。

### 結果（2026-10-19）

- [[Task 9]]：4 處，在背景、現況與要做的。
- [[Task 31]]：1 處，在現況裡 2026-10-13 第 4 步的紀錄。
- [[Task 32.11]]：4 處，在現況、與其他 task 的關係與日誌。
- [[Task 67]]：23 處，在標題、Status 行、Raised 行，以及背景、現況、要做的、驗證與日誌五章。
- 摘要表：Task 67 那一列的 Title。
- 改到的四個 task 檔，各在日誌的 2026-10-19 補一行，連到本 task，照 [[Task 62.1]] 與 [[Task 62.4]] 改別的 task 檔時的做法。
- 改完之後，task 檔與摘要表裡還寫「配對行」的，只有本 task 談這個譯法本身的地方。

## 3. 要做的

1. ✅ 33 處改成 pairing line，Task 67 的標題與摘要表的 Title 一起改。
2. ✅ 改到的四個 task 檔在日誌補一行。
3. ✅ 跑 `check_tasks.py`。

## 4. 驗證

- `check_tasks.py` PASS。
- task 檔與摘要表裡的「配對行」，只剩本 task 談這個譯法本身的地方。

## 5. 與其他 task 的關係

- [[Task 67]]：在這裡發現，23 處在它的檔案裡，它的標題跟著改。
- [[Task 69]]：其他 keep-English 譯法的盤點與 `check_tasks.py` 的掃描。
- [[Task 63]]：決定 task、chore 等新詞要不要加進清單；本 task 不併進去。
- [[Task 48]]：中文版的「術語」改成 term；中英文之間的空格照它。

## 6. 知識

—

## 7. 日誌

### 2026-10-30

- [[Task 86]] 把 chore 改用名稱：本檔的 `[[Chore N]]` 連結改成新名稱。

### 2026-10-19

- 建立：做 [[Task 67]] 時發現；問了 8 個問題，決定五個檔全改，其他譯法與掃描另開 [[Task 69]]。
- 做完：33 處改成 pairing line，Task 67 的標題與摘要表的 Title 跟著改，四個 task 檔的日誌各補一行；`check_tasks.py` PASS。
