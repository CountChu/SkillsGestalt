# Task 60 - 修正 Home-RSDC 的 fenced blocks FAIL：換行改成 LF，check_rsdc 報出換行不同

**Status**：完成——2026-10-18 Home-RSDC.md 與 Wireframe.md 改成 LF，`check_rsdc.py` 比對時把 CRLF 當成 LF，換行不同另報 WARN；Home-RSDC 的中英對照檢查 PASS。
**Raised**：2026-10-18，[[Task 59]] 改 imp-home 的中文版時，發現 Home-RSDC 的 `check_rsdc.py` 在 HEAD 就有一項 FAIL：fenced blocks are byte-identical。
**Depends on**：—

## 1. 背景

`check_rsdc.py` 比對 Home-RSDC.md 與它的中文版時，報 block 1（第 85 行）與 block 2（第 254 行）不同。
兩個 block 的內容其實逐字相同：英文版用 CRLF 換行，中文版用 LF，script 讀檔時留下了 `\r`，所以每一行都差一個 `\r`。
訊息只說 fenced blocks 不同，看不出原因是換行。

## 2. 現況

### 決定

- **改成 LF 的檔案**：imp-home 的 Home-RSDC.md 與 Wireframe.md。
  兩份的中文版都是 LF；Wireframe 目前沒有工具逐字比對它的 fenced block，但原因相同。
  repo 裡另有 30 個 CRLF 檔，其中的 Markdown 是 report-my-chats 與 write-note-chat 的 SKILL.md，它們沒有中文版，這次不改。
- **改 `check_rsdc.py`**：讀檔時把 CRLF 當成 LF，所有比對只看內容；中英兩份的換行不同時，另報一則 WARN，指出哪一份是 CRLF。
  換行不同不影響顯示，所以報 WARN，不報 FAIL。
  gen-rsdc-skill 沒有 README，也沒有文件逐項列出這些檢查，所以只改 script 與它的 docstring。
- **拼法一起改**：Home-RSDC.md 的 8 處英式拼法改成美式，behavior 3 處、color 2 處、memorize 2 處、initialize 1 處；Wireframe.md 第 9 行的 colour 也改成 color。
  這 9 處都是一般的敘述，不是程式碼或其他文件用的名稱，也不在範本的共用句子裡。
- **[[Task 59]] 的順帶發現連到這個 task**。

### 進度

- `check_rsdc.py`：`Doc` 讀檔時把 CRLF 換成 LF，並記下檔案是否用 CRLF；`check_pair` 在兩份換行不同時報 WARN；docstring 補上這兩點。
  改完後趁 Home-RSDC.md 還是 CRLF 時重跑：fenced blocks 改成 PASS，多一則 WARN 指出 Home-RSDC.md 用 CRLF、中文版用 LF，判定 PASS。
  其他 8 種執行的輸出都和改之前逐字相同：`--standard`、三份 RSDC 各自單獨檢查、SkillCompiler 與 MermaidView 的中英對照，以及兩次 `--skill`。
- Home-RSDC.md（330 行）與 Wireframe.md（78 行）改成 LF；忽略換行之後，內容只改了拼法的 9 行。
  depends_on 的指紋不受換行影響，但拼法改了內容，所以 Home-RSDC.md 的指紋從 `0b7b4166612e` 變成 `336c2a6c48a4`；沒有文件在檔頭記錄這兩份，不必重記。
- 中文版照 chinese skill：`diff_md.py` 用 `--ignore-cr-at-eol` 算 change set，所以只列出拼法的 8 行與 1 行。
  這幾行的中文本來就是正確的翻譯，中文版不用改；兩對 `check_parity.py` 0 failure，`diff_md.py --verify` PASS。
- 最後 Home-RSDC 中英對照的 `check_rsdc.py` PASS：15 項通過，0 警告。

### 順帶發現

- 三份 RSDC 單獨檢查時都有 6 項 FAIL，Home-RSDC 與 SkillCompiler 的 `--skill` 各有 2 項 FAIL，MermaidView 的中英對照有 1 項 FAIL。
  這些在改之前就有，這次沒有處理；單獨檢查的 FAIL 歸 [[Task 18]] 的 sub task：[[Task 18.2]]、[[Task 18.7]] 與 [[Task 18.8]]。
- 不少 Markdown 仍用英式拼法，例如 checking-criteria.md、SkillCompiler-RSDC.md、兩份 RSDC 範本與幾個 skill 的 SKILL.md。
  md-style 的美式拼法規則目前只由 `check_ste.py` 檢查 STE 檔，其他檔案屬於 [[Task 56]] 要建立的 md-style 巡檢。

## 3. 要做的

✅ 2026-10-18 兩份文件改成 LF 與美式拼法，`check_rsdc.py` 報出換行不同，Home-RSDC 的中英對照檢查 PASS。

## 4. 驗證

- Home-RSDC 中英對照的 `check_rsdc.py` PASS，15 項通過、0 警告；Home-RSDC.md 還是 CRLF 時，新的 WARN 指出換行不同，fenced blocks PASS。
- 其他 8 種 `check_rsdc.py` 執行的輸出和改之前逐字相同。
- Home-RSDC 與 Wireframe 兩對 `check_parity.py` 0 failure，`diff_md.py --verify` PASS。
- `git diff --ignore-cr-at-eol` 只列出拼法的 9 行。

## 5. 與其他 task 的關係

- [[Task 59]]：改 imp-home 的中文版時發現這項 FAIL。
- [[Task 56]]：其他 Markdown 的英式拼法，屬於它要建立的 md-style 巡檢。
- [[Task 18]]：三份 RSDC 單獨檢查的 FAIL 歸它的 sub task。

## 6. 知識

—

## 7. 日誌

### 2026-10-18

- 建立：使用者決定另開 task 處理 Home-RSDC 的 fenced blocks FAIL。
- 查出原因是換行不同；`check_rsdc.py` 比對時把 CRLF 當成 LF，換行不同另報 WARN；Home-RSDC.md 與 Wireframe.md 改成 LF，9 處英式拼法改成美式。
- 三份 RSDC 單獨檢查的 FAIL 交給 [[Task 18]] 的 sub task。
