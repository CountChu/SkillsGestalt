# Task 56 - 建立 md 巡檢的 chore：md-style 與重複的規則

**Status**：尚未開始——2026-10-18 記下，範圍是一句一行與英文的美式拼法；2026-10-30 併進 [[Task 61]] 的重複規則檢查。
**Raised**：2026-10-18，檢視哪些 task 適合做成 chore 時提出：[[Task 19]] 讓範圍內的 md 都一句一行之後，新寫或改過的檔沒有定期檢查。
**Depends on**：—

## 1. 背景

- [md-style.md](../.github/common/rules/md-style.md) 規定散文一個句子一行、英文用美式拼法（[[Task 38]]）等；根目錄的 CLAUDE.md 要求建立或修改 md 時照它寫。
- [[Task 19]] 讓範圍內的每一份 md 都改成一句一行；之後新寫、改過的檔，只有寫的人自己檢查。
- 在副本上以 reformat-md 的 `reformat_md.py --mode clean` 試跑，就看得出一份檔哪幾行不是一句一行；美式拼法有 [us-spelling.json](../.github/common/references/us-spelling.json) 可以對照。
- [[Task 61]] 讓定規則的 md 裡重複的規則只寫一次；之後新加的重述，沒有定期檢查。
- `reformat_md.py` 還有兩個已知的斷句問題（[[Task 36]]、[[Task 42]]）：修好之前，巡檢會漏掉那幾種一行多句，但不會誤報。

## 2. 現況

### 已決定（2026-10-18）

- 範圍：一句一行，加上英文檔的美式拼法。
- 不依賴 [[Task 36]] 與 [[Task 42]]：它們沒修好，只是少抓到幾種情況，不算白做。
- 提交：本 task 的修改前綴 `task 56`。

### 併進的重複檢查（2026-10-30）

- 使用者在 [[Task 61]] 決定把重複的規則檢查併進本 task，不另開 chore。
- 範圍：[[Task 61]] 的 18 份定規則的 md，之後新加的規則檔也加進來；md-style 的巡檢範圍不變。
- 方法：只用 [[Task 61]] 的「掃描方法」那種字詞相近的掃描；換了說法的重複要逐份讀、逐組判斷，不在每次巡檢做。
- 腳本：[[Task 61]] 的掃描腳本沒有放進 repo，建 chore 時再決定要不要寫成工具。
- 已決定保留的重述，巡檢時跳過，不再列出（理由見 [[Task 61]]）：
  - task-rules 與 chore-rules 之間的重述（[[Task 62.1]] 決定兩份各自寫完整）。
  - RSDC-Standard 的 Changes in This Version（[[Task 58]]）。
  - ste-custom 的 Words 與 Rules 兩節的平行寫法，以及 SKILL-tmp 每個 step 的範本段落。
  - 範本重述它說明的規則：SKILL-tmp 對 report-md-rules、report-yaml-rules；README-tmp 對 skill-writing、DFD.md、根目錄的 CLAUDE.md；report-md-rules 與 SKILL-tmp 之間只是佔位相近。
  - checking-criteria 重述它檢查的規則；它的檔頭記錄了 README-tmp 與 skill-writing。
  - 根目錄與 skills/ 的 CLAUDE.md 把人帶到規則檔的那幾句。
  - RSDC-Standard 的 Versioning 與 tw-keep-english 的版本段：各管自己這份檔。
  - ste-rules 的 1.14 與 md-style 的美式拼法：1.14 是 STE 自己的規則。
  - tw-keep-english 的 Why 欄：是保留英文的理由，不是規則。

### 要決定的

- 要查哪些檔：沿用 [[Task 19]] 的範圍，或全部 md；中文版要不要以 `--twin` 一起查。
- 何時要做：例如每週一次，或 md-style.md、`reformat_md.py` 改了之後。
- 找到的怎麼處理：直接以 `reformat_md.py` 改，或只列出、另開 task。
- 拼法怎麼查：`check_ste.py` 的拼法檢查只用在 STE 檔，其他英文檔要用哪支工具，要不要另寫一支。
- 結果怎麼記：完整清單存在 checkpoints、紀錄只寫總數，或像 [[keep-english]] 那樣和上一次比。

## 3. 要做的

1. 決定「要決定的」五項，照 [chore-rules.md](../.github/common/rules/chore-rules.md) 建立 chore 與摘要表的一列。
2. 需要的話，寫巡檢腳本；重複規則的掃描要不要寫成工具，也在這時決定。
3. 跑第一次。
   第一次的對象包括 [[Task 61]] 讀規則檔時找到的英式拼法（2026-10-30）：[ste-rules.md](../.github/common/skills/asd-ste/references/ste-rules.md) 的 judgement，[checking-criteria.md](../.github/common/skills/check-skill/references/checking-criteria.md) 的 judgement、honours、behaviour、capitalising、artefact、colour。
   checking-criteria 把 skill-writing 的「scripted-versus-not」叫作 script-versus-judgement，改拼法時一起決定名稱。

## 4. 驗證

- `check_chores.py` 與 `check_tasks.py` 都 PASS。
- 第一次巡檢列出的每一份，都照決定的方式處理了。

## 5. 與其他 task 的關係

- [[Task 19]]：定下一句一行的寫法與範圍。
- [[Task 38]]：美式拼法的規則與檢查。
- [[Task 36]]、[[Task 42]]：`reformat_md.py` 的斷句問題；修好之後，巡檢抓得更完整。
- [[Task 53]]：建立 chore 制度。
- [[Task 61]]：重複的規則只寫一次；之後的重複檢查併進本 task。

## 6. 日誌

### 2026-10-30

- [[Task 61]] 讀規則檔時找到的英式拼法，記進要做的第 3 項。
- 併進 [[Task 61]] 的重複規則檢查：記下範圍、方法與巡檢時跳過的已知重述；標題改成「建立 md 巡檢的 chore：md-style 與重複的規則」。
- [[Task 86]] 把 chore 改用名稱：本檔的 `[[Chore N]]` 連結改成新名稱。

### 2026-10-18

- 建立。
- 第 3 章連到的 `chores/CLAUDE.md` 已刪除，改連 [chore-rules.md](../.github/common/rules/chore-rules.md)（[[Task 62.1]]）。
