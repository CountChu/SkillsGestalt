# Task 73 - 照 keep-English 稽核改中文版的譯法：261018 版

**Status**：尚未開始——2026-10-20 [[keep-english]] 的稽核找到 19 份中文版、264 行警告，還沒改。
**Raised**：2026-10-20，[[keep-english]] 第一次稽核：keep-English list 換成 261018 版之後，沒被改到的中文版還有清單不要的譯法。
**Depends on**：—

## 1. 背景

- [tw-keep-english.md](../.github/common/references/tw-keep-english.md) 列出中文版要留英文的 term，它的 Flagged 欄是不該出現的譯法。
- chinese skill 只在中文版被改到時才檢查它，所以清單後來加的詞，不會回頭套用到沒改到的中文版。
- 稽核只列出，不判斷：同一個詞用在別的意思時是對的，所以每一行都要有人讀過再決定。

## 2. 現況

### 2026-10-20 稽核的結果

- 清單 261018 版：33 對中英對照，19 份中文版有 264 行警告；完整的清單在 `checkpoints/chores/chore-2/2026-10-20-261018.txt`，git 不追蹤。
- 最多的譯法：script 的「腳本」206 行（16 份）、step 的「步驟」24 行（1 份）、identifier 的「識別碼」9 行（6 份）。
- 警告最多的中文版：SkillCompiler-RSDC-tw.md 67 行、imp-home 的 SKILL-tw.md 34 行、compile-skill 的 SKILL-tw.md 23 行、check-skill 的 SKILL-tw.md 22 行、chinese 的 SKILL-tw.md 21 行。
- 「英文也寫中文」1 行：MermaidView-RSDC-tw.md 的「角色」，英文那一行寫的就是這個中文詞，不用改。

### 已決定（2026-10-20）

- 一個 task 包全部警告；報告的檔案清單就是要做的，太大時再拆 sub task。
- 這次只開 task，不改中文版。

## 3. 要做的

1. 逐份讀報告列出的警告：指那個 term 的譯法改成英文，同一個詞用在別的意思的保留。
2. 照 [chinese](../.github/common/skills/chinese/SKILL.md) skill 改：中文版只改那幾行，再跑 `check_parity.py --keep`。
3. 改完一份就在日誌記一行；全部改完之後，再跑一次稽核的指令，和這份報告比。

## 4. 驗證

- 重跑稽核，這 19 份中文版的警告只剩讀過、確定要保留的。
- 每份改過的中文版，`check_parity.py` 都沒有新的 failure。

## 5. 與其他 task 的關係

- [[keep-english]]：本 task 的來源。
- [[Task 63]]：task、chore 等新詞要不要加進 keep-English list；清單一改就換版本，[[keep-english]] 要再跑。

## 6. 日誌

### 2026-10-30

- [[Task 86]] 把 chore 改用名稱：本檔的 `[[Chore N]]` 連結改成新名稱。

### 2026-10-20

- 建立：[[keep-english]] 第一次稽核之後開的。
