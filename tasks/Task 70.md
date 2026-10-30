# Task 70 - SKILL.md 的共用句子換成 STE 範本的寫法

**Status**：尚未開始——2026-10-19 記下：SKILL-tmp 換成 STE 版之後，本 workspace 有 26 份 SKILL.md 還留著照舊範本抄的共用句子。
**Raised**：2026-10-19，[[Task 32.11]] 以 Step 7 取代 SKILL-tmp 之後，照 [[Task 32]] 的「範本的後續」列出受影響的句子；使用者決定另開本 task，和處理 README 的 [[Task 66]] 分開。
**Depends on**：—

## 1. 背景

gen-skill 寫新 skill 的 `SKILL.md` 時，整份抄 [SKILL-tmp.md](../.github/common/templates/SKILL-tmp.md)，所以每份新格式的 SKILL.md 都有一批和範本相同的共用句子。
2026-10-19 [[Task 32.11]] 把 SKILL-tmp 換成 STE 版，範本的說法改了，已經寫好的 SKILL.md 還是舊的說法。
MUST FOLLOW 的標籤也從「Honour a `run step N` selector」改成「Honor a `run step N` selector」，也就是原本名稱的美式拼法。
check-skill 只拿範本的標題比對，所以這些舊句子不會被報出來。

## 2. 現況

### 受影響的句子（2026-10-19）

舊行號指取代前的 SKILL-tmp.md，也就是 commit `5a92ef6` 那一版；新行號指取代後的 SKILL-tmp.md。
份數只算本 workspace 的 SKILL.md，並只算和舊句子一字不差的行；各檔的行號等開始做時再算。

- 舊第 8 行 → 新第 14 行，12 份：asd-ste、ask-note、check-md-deps、check-skill、chinese、compile-skill、gen-imp-app、gen-rsdc-app、gen-rsdc-skill、gen-skill、imp-app、imp-home。
- 舊第 11 行 → 新第 18 行，7 份：asd-ste、chinese、compile-skill、gen-imp-app、gen-rsdc-skill、imp-app、imp-home。
- 舊第 12 行 → 新第 19 行，5 份：asd-ste、gen-imp-app、gen-rsdc-skill、imp-app、imp-home。
- 舊第 13 行 → 新第 20 行，7 份：check-skill、gen-imp-app、gen-rsdc-app、gen-rsdc-skill、gen-skill、imp-app、imp-home。
- 舊第 14 行 → 新第 21–22 行，5 份：asd-ste、gen-imp-app、gen-rsdc-skill、imp-app、imp-home。
- 舊第 15 行 → 新第 23 行，7 份：asd-ste、check-skill、gen-imp-app、gen-rsdc-app、gen-skill、imp-app、imp-home。
- 舊第 16 行 → 新第 24–25 行，8 份：asd-ste、check-skill、compile-skill、gen-imp-app、gen-rsdc-app、gen-skill、imp-app、imp-home。
- 舊第 17 行 → 新第 26–27 行，6 份：check-skill、compile-skill、gen-imp-app、gen-rsdc-app、gen-rsdc-skill、gen-skill。
- 舊第 21 行 → 新第 31 行，12 份：和舊第 8 行同樣的 12 份。
- 舊第 28 行 → 新第 38 行，12 份：和舊第 8 行同樣的 12 份。
- 舊第 36 行 → 新第 48 行，26 份：add-tags、add-tags-note、asd-ste、ask-note、check-md-deps、check-skill、chinese、compile-skill、del-tags、gen-imp-app、gen-rsdc-app、gen-rsdc-skill、gen-skill、imp-app、imp-home、notify-week、reformat-md、report-logs、report-skills、report-week、set-tag-status、synch-two-mds、write-note、write-note-new-files、write-note-tags、write-topic。
- 舊第 37 行（Honour 標籤）→ 新第 49–50 行，整行相同的 6 份：asd-ste、chinese、compile-skill、gen-imp-app、imp-app、imp-home。
  gen-rsdc-skill 的標籤相同、標籤後面的內容不同，標籤也要改成 Honor。
- 舊第 38 行 → 新第 51 行，2 份：gen-imp-app、imp-home。
- 舊第 39 行 → 新第 52 行，3 份：asd-ste、gen-imp-app、imp-home。
- 舊第 40 行 → 新第 53 行，3 份：check-md-deps、compile-skill、gen-imp-app。
- 舊第 41–44 行 → 新第 54–62 行，1 份：imp-app；新範本把這一條拆成兩個清單項目。
- 舊第 45 行 → 新第 63–66 行，1 份：gen-imp-app。
- 舊第 48 行 → 新第 73 行，3 份：gen-imp-app、imp-app、imp-home。
- 舊第 79 行 → 新第 104 行，22 份：add-tags、add-tags-note、ask-note、check-skill、chinese、compile-skill、del-tags、gen-imp-app、gen-rsdc-app、gen-rsdc-skill、gen-skill、imp-app、imp-home、notify-week、report-logs、report-skills、report-week、synch-two-mds、write-note、write-note-new-files、write-note-tags、write-topic。
- 舊第 81 行 → 新第 107–108 行，1 份：gen-imp-app。
- 舊第 84 行 → 新第 113 行，6 份：ask-note、check-skill、gen-imp-app、gen-skill、imp-app、imp-home。
- 舊第 98 行 → 新第 133 行，7 份：asd-ste、check-skill、chinese、compile-skill、gen-imp-app、gen-rsdc-skill、report-week。
- 舊第 102 行 → 新第 138 行，12 份：和舊第 8 行同樣的 12 份。
- 舊第 103 行 → 新第 139 行，8 份：asd-ste、ask-note、check-md-deps、check-skill、chinese、compile-skill、gen-rsdc-skill、imp-home。
- 舊第 107 行 → 新第 143 行，3 份：check-skill、chinese、gen-imp-app。
- 舊第 109 行 → 新第 145 行，5 份：asd-ste、chinese、gen-imp-app、gen-rsdc-skill、imp-app。
- 舊第 112 行 → 新第 148 行，2 份：gen-imp-app、report-week。
- 舊第 129 行與第 155 行 → 新第 165 行與第 195 行，各 4 份：gen-imp-app、imp-app、imp-home、report-week。
- 舊第 140 行 → 新第 177 行，3 份：asd-ste、check-md-deps、chinese。
- 舊第 77 行「Run `.venv` first.」（6 份）與舊第 121 行「The script:」（5 份），新範本和舊範本相同，不必改。

### 另一個 workspace

InvestForge 的 SKILL.md 也照抄了舊範本，例如 Honour 標籤有 6 份、舊第 36 行有 15 份；那邊的修改由 InvestForge 自己的 task 處理。

## 3. 要做的

1. 由使用者決定一次改完或分批。
2. 照新範本改這些 SKILL.md 的句子，placeholder 的位置換成各 skill 自己的值；Honour 標籤改成 Honor。
3. 改每個 skill 之前，先讀它的 README.md（有的話）與 [skill-writing.md](../.github/common/rules/skill-writing.md)，照 README 的 When the Skill Is Changed 改，並跑它列出的檢查；中文版照 chinese skill 跟著改。
4. 開始做時再算各檔的行號。

## 4. 驗證

- 每對中英對照的 `check_parity.py` 0 failure，`diff_md.py --verify` PASS。
- check-skill 掃描所有 skill，沒有新的 issue；這原本是 [[Task 32]]「範本的後續」的驗證。

## 5. 與其他 task 的關係

- [[Task 32.11]]：取代 SKILL-tmp 之後提出。
- [[Task 32]]：「範本的後續」的規定；Task 32 完成時，SKILL.md 的部分交給本 task。
- [[Task 66]]：README 的共用句子，和本 task 是同一件事的另一半。
- [[Task 38]]：美式拼法的規則；SKILL.md 裡的 Honour 標籤在本 task 改成 Honor。

## 6. 日誌

### 2026-10-30

- [[Task 78]] 刪除了 report-my-chats 與 write-note-chat：各項清單拿掉它們、份數跟著減少，只列了 report-my-chats 的兩項（舊第 125 行、舊第 143 行）整行刪掉；Status 的 28 份改成 26 份；Honour 標籤那一項拿掉指向 report-my-chats 第 165 行的一句。
- [[Task 78]] 刪除了 mail-inline skill：「舊第 36 行」與「舊第 79 行」兩項的清單拿掉它，份數由 29、25 改成 28、24；Status 的 29 份也改成 28 份。

### 2026-10-19

- 建立。
