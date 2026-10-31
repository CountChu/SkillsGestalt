# Task 63 - 決定 task、chore 等新詞是否加進 keep-English list

**Status**：尚未開始——[[Task 62.1]] 的兩份規則中文版把 10 個詞留英文，keep-English list 還沒有它們的列。
**Raised**：2026-10-18，[[Task 62.1]] 寫 task-rules 與 chore-rules 的中文版時，照原本 `tasks/CLAUDE.md` 的中文寫法把這些詞留英文；使用者決定這次不改清單，另開本 task。
**Depends on**：—

## 1. 背景

- chinese skill 的規則：中文版留英文的 term，要在同一次加進 [tw-keep-english.md](../.github/common/references/tw-keep-english.md)。
- [[Task 62.1]] 的 `task-rules-tw.md` 與 `chore-rules-tw.md` 留英文的新詞：task、sub task、chore、wikilink、vault、session，以及 git 的 stage、index、blob、HEAD。
- 清單已有 stage 一列，但它說的是 RSDC 的 Dataflow 裡的 stage，不是 git 的 stage。
- 已有先例：13 份中文版把 vault 留英文、5 份把 session 留英文，清單都沒有它們的列。
- 清單一改就換版本；[[keep-english]] 在清單換版本之後，要對所有中英對照稽核一次。

## 2. 現況

—

## 3. 要做的

1. 照清單的 rule 逐詞判斷：留英文的加一列，寫出它取代的譯法與要 flag 的譯法；要翻譯的定一種譯法。
2. 決定 git 的 stage 與 RSDC 的 stage 怎麼在同一列分開說明。
3. 清單是 STE 檔：新的列照 STE 寫，清單的中文版照 chinese skill 跟著改。
4. 決定之後，`task-rules-tw.md` 與 `chore-rules-tw.md` 照決定改。

### 要決定的

- 每個詞留英文還是翻譯。
- 這次改清單，怎麼和其他正在改清單的 task 錯開，例如 [[Task 32]]。

## 4. 驗證

- 兩份規則中文版的 `check_parity.py --keep` 都是 0 failure。
- 清單與它的中文版 `check_parity.py` 0 failure，清單的 `check_ste.py --ste` PASS。

## 5. 與其他 task 的關係

- [[Task 62.1]]：本 task 的來源。
- [[keep-english]]：清單換版本之後要跑。

## 6. 日誌

### 2026-10-30

- [[Task 86]] 把 chore 改用名稱：本檔的 `[[Chore N]]` 連結改成新名稱。

### 2026-10-18

- 建立：[[Task 62.1]] 寫中文版時發現，使用者決定另開。
