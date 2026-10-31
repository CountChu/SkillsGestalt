# Task 69 - 盤點 task 檔裡其他 keep-English 譯法，決定 check_tasks.py 要不要掃描

**Status**：尚未開始——task 檔與摘要表約有 960 處寫了 keep-English list 的 Flagged 譯法，還沒決定哪些要改，也沒有工具檢查 task 檔。
**Raised**：2026-10-19，[[Task 68]] 用清單的 Flagged 欄掃過全部 task 檔，發現除了 pairing line，其他 term 也寫成中文；使用者決定另開本 task，`check_tasks.py` 要不要掃描也放在這裡決定。
**Depends on**：—

## 1. 背景

- [task-rules.md](../.github/common/rules/task-rules.md) 要求 task 檔像 TW twin 一樣，把 [tw-keep-english.md](../.github/common/references/tw-keep-english.md) 列出的每個 term 留英文。
  這條規則是 2026-10-18 由 [[Task 62.1]] 寫進去的，大部分 task 檔寫在它之前。
- 中文版有兩個工具檢查：chinese skill 的 `check_parity.py --keep`，以及 [[keep-english]] 跑的 `audit_keep_english.py`。
  `audit_keep_english.py` 只看旁邊有 `-tw.md` 的檔，task 檔沒有 TW twin，不在它的範圍；`check_tasks.py` 也不查。

## 2. 現況

### 盤點（2026-10-19）

[[Task 68]] 改完之後，用清單 261018 版的 Flagged 欄比對全部 task 檔與摘要表的全文，不算本 task 與 Task 68。
比對時較長的譯法先比，所以「術語表」不算進「術語」；fenced block、inline code 與談譯法本身的地方都算進去了。

- 共 963 處：task 檔 949 處，分布在 73 個檔；摘要表 14 處。
- 最多的是「範本」（template）541、「腳本」（script）105、「術語」（term）66、「提交」（commit）39、「佔位符」（placeholder）37、「步驟」（step）32、「過期」（stale）27、「行內程式碼」（inline code）23、「角色」（role）18、「術語表」（glossary）14。
- 2026-10-18 以後提出的 task 有 100 處，之前的有 849 處；在日誌裡的有 59 處。
- 有些是在談譯法本身，不是寫錯，例如 [[Task 48]] 的「術語」、[[Task 9]] 的「確定性」與「工作流程」。

## 3. 要做的

1. 用和 `check_parity.py --keep` 相同的方式重新盤點：只看 prose，排除 fenced block、標題、inline code 與連結目標，談譯法本身的地方另外列出。
2. 逐個譯法決定改不改，以及規則生效前寫的 task、日誌與摘要表的 Title 各怎麼處理。
3. 決定 `check_tasks.py` 要不要掃描：只 WARN 還是 FAIL、談譯法本身的地方怎麼排除；或讓 `audit_keep_english.py` 也稽核 task 檔。
   `check_tasks.py` 在 common 裡，改了它，用 common 的 InvestForge 也會跟著被檢查。
4. 照決定改；改了 `check_tasks.py`，就一併改它的 docstring 與 task-rules 的中英兩份。

## 4. 驗證

- 重新盤點，留下的譯法都是決定不改的。
- `check_tasks.py` PASS。

## 5. 與其他 task 的關係

- [[Task 68]]：本 task 的來源；它先改了 pairing line 的譯法。
- [[Task 63]]：可能在清單加上 task、chore 等新詞；它先做完的話，本 task 的盤點要包括這些詞。
- [[Task 62.1]]：把 keep-English 的要求寫進 task-rules。
- [[keep-english]]：稽核中文版的 keep-English 譯法；task 檔不在它的範圍。

## 6. 知識

—

## 7. 日誌

### 2026-10-30

- [[Task 86]] 把 chore 改用名稱：本檔的 `[[Chore N]]` 連結改成新名稱。

### 2026-10-19

- 建立：[[Task 68]] 掃過全部 task 檔時發現，使用者決定另開，`check_tasks.py` 的掃描也放在這裡。
