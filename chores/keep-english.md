# keep-english - keep-English 稽核

**Status**：使用中——keep-English list 換版本之後，對本 workspace 的全部中英對照跑一次 `audit_keep_english.py`；2026-10-30 稽核了 261030 版，清單下一次換版本再跑。
**Started**：2026-10-18，chinese skill 只在中文版被改到時才拿 keep-English list 檢查它，清單後來加的詞不會回頭套用到沒改到的中文版；由 [[Task 53]] 建立。
**When**：tw-keep-english.md 換了版本，和上次稽核的版本不同

## 1. 目的

[tw-keep-english.md](../.github/common/references/tw-keep-english.md) 列出中文版必須保留英文的術語，它的 Flagged 欄是不該出現的譯法，例如 script 的「腳本」、step 的「步驟」。
每次清單改版，沒被改到的中文版不會被重新檢查，就會和清單愈來愈不一致；稽核一次找出全部的落差，交給使用者決定要不要改。

## 2. 何時要做

- tw-keep-english.md 的 Version 行換了版本，和上次稽核用的版本不同；清單或它的規則改了，它就換版本。
- 看出該做了：從 workspace 的根目錄跑 `python {skillGroups.common}/scripts/audit_keep_english.py due --keep {skillGroups.common}/references/tw-keep-english.md --out checkpoints/chores/keep-english --baseline 261016`，印出 due、以 0 結束，就是該做了。
- 還沒有任何一份報告時，以 `--baseline` 的 261016 當上次的版本：2026-10-18 決定 261016 這一版不稽核，等下一版。
- 別的 agency 也照本 chore 做：每個 agency 在自己的根目錄執行，只稽核自己的中英對照，報告與執行紀錄留在自己那裡，見 [chore-rules.md](../.github/common/rules/chore-rules.md)。
  `{skillGroups.common}` 照執行的 agency 的 `config.yaml` 代換。

## 3. 怎麼做

1. 從 workspace 的根目錄跑 `python {skillGroups.common}/scripts/audit_keep_english.py audit --keep {skillGroups.common}/references/tw-keep-english.md --root . --out checkpoints/chores/keep-english`。
   它把完整的清單寫成 `checkpoints/chores/keep-english/<日期>-<版本>.txt`，並和上一份報告比，印出新出現的 `[NEW]` 與消失的 `[GONE]`。
2. 只列出，不改任何中文版：把總數、最多的幾種譯法與 `[NEW]` 交給使用者；要改的在執行的 agency 另開 task，照 chinese skill 改。
3. 「英文也寫中文」那一組分開列：英文那一行寫的就是那個中文詞，例如翻譯對照表的一列，不算進要決定的警告。
4. 在執行的 agency 自己的摘要表，`## 執行紀錄` 的 `### keep-english` 下寫下清單版本、對照的份數、有警告的中文版份數與行數，以及和上一份比的差異；摘要表的「上次執行」改成當天。
5. 報告在 checkpoints，git 不追蹤，所以只提交執行的 agency 自己的摘要表，前綴是 `chore keep-english: `；再跑 `check_chores.py`。

## 4. 驗證

- `audit_keep_english.py due ...` 印出 not due。
- `check_chores.py` PASS。

## 5. 與其他 task、chore 的關係

- [[Task 43]]：2026-10-14 第一次對兩個 workspace 的中英對照跑過 `check_parity.py --keep`，只列出、沒改；那次以 check_parity 的警告行計數，和本 chore 逐行計數的數字不能直接比。
- [[Task 53]]：建立本 chore 與 `audit_keep_english.py`。
- [[Task 62.5]]：2026-10-19 把範圍改成本 workspace 的中英對照。
- [[rerecord-ste-custom]]：另一件例行的檢查，對象是 ste-custom.md 的紀錄。
