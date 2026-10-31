# Task 58 - md-style 加一條規則：文件不寫自己的來歷

**Status**：完成——2026-10-18 md-style 的 Rules checked elsewhere 加上這條規則，scratch-rules 刪掉一句來歷，report-my-chats 改寫一句，記錄 md-style 的 6 份 README 重記。
**Raised**：2026-10-18，審 scratch-rules（[[Task 32.7]]）時，使用者問草稿第 37 行「在這些規則之前，執行通常把暫存檔放在那裡」這類提及過去的話是否必要，決定把「不寫來歷」訂成規則。
**Depends on**：—

## 1. 背景

scratch-rules.md 原文第 21 行有「since that is the habit this replaces」，STE 草稿把它拆成獨立的一句「Before these rules, runs usually put their scratch files there.」，讀起來像在交代過去。
照規則做事的 agent 用不到這一句：前面已經說不要直接放在根目錄，後面幾行也把原因說完了。
事情怎麼演變到現在，git 歷史與 task 的日誌都記著。
使用者決定把「文件不寫自己的來歷」訂成規則，放在 [md-style.md](../.github/common/rules/md-style.md) 的 Rules checked elsewhere 一節。

## 2. 現況

### 決定

- **放在 md-style**：[CLAUDE.md](../CLAUDE.md) 要求新增或修改 Markdown 時都照 md-style 做，gen-skill 也一定讀它，寫文件的人下筆時就會看到。
  這一節本來就放會改動文字的規則，美式拼法就在這裡；`reformat_md.py` 不套用這一節，reformat-md 的 Step 0 核對 transform 時也跳過它，所以不必寫 transform。
  不放 ste-custom 的 Rules：asd-ste 要保留原文的意思，放在那裡會讓它改寫時刪掉原文的內容，而且只管得到 STE 檔。
  不放 skill-writing.md：它的範圍只有 SKILL.md 與 README.md，而且正由 [[Task 32.8]] 審核。
  不放根目錄的 CLAUDE.md：skill 執行時不讀它。
- **範圍**：repo 中所有 Markdown，本來就在記錄工作或變更的文字除外。
  例外是 `tasks/`、`chores/`、`dashboard/` 的檔案，RSDC 文件的 Changes in This Version 一節，以及 ste-custom.md 的 Why 欄；`.github/external/` 的檔案也除外。
- **只禁文字本身的來歷**：文字先前的版本、它取代的方法，以及它之前的做法。
  主題本身是過去的事就照寫，例如設計文件寫 app 取代的舊做法，那是在描述問題。
- **寫法**：用附允許例子的 A 版；例外放在子項，因為 STE 一段最多 6 句。
  沒有工具檢查這條規則，由審閱檔案的人檢查。
- **既有文件**：以關鍵字粗查剩下的文件，找到兩處，都在這個 task 改。
  scratch-rules.md 取代後的第 36 行刪掉；report-my-chats 的 SKILL.md 第 266 行改成直接的指示，後面說原因的部分留著。
- **依賴方在這個 task 裡重記**，照 `20417cf` 的前例。

### 進度

- md-style.md 第 167–174 行加上規則；Technical words 加上 app、design document、git、history，原有的順序不動。
  `check_ste.py --ste` PASS，只有改之前就有的 op 警告。
  `[[ASD-STE100_ISSUE9.pdf]]` 重記，日期從 2026-10-14 改成 2026-10-18，指紋不變；`[[ste-custom]]` 不變。
- md-style-tw.md 照 chinese skill 只譯 change set 的 10 行：檔頭兩行與第 167–174 行。
  history 譯成「來歷」，design document 譯成「設計文件」，app 照其他 twin 保留英文。
  `check_parity.py` 0 failure，`diff_md.py --verify` PASS，兩份的 Technical words 相同，共 108 個。
- scratch-rules.md 與它的中文版刪掉第 36 行「Before these rules, runs usually put their scratch files there.」，兩份都是 51 行。
  `check_ste.py --ste` PASS，檔頭兩條依賴都是 UNCHANGED；`check_parity.py` 0 failure，`diff_md.py --verify` PASS。
- report-my-chats 的 SKILL.md 第 266 行從「Wrapping a URL in backticks is the habit this replaces — …」改成「Never wrap a URL in backticks — …」。
  這個 skill 沒有 README，也沒有中文版，也沒有文件在檔頭記錄它。
- 依賴方：`draft.py dependents` 以本 workspace、InvestForge 與 BookMaster 為 root，md-style.md 由 asd-ste、check-skill、gen-skill 的 README 中英共 6 份記錄，scratch-rules.md 由 check-skill 的 2 份記錄。
  改之前這些紀錄都是最新的：HEAD 的 md-style.md 指紋正是紀錄裡的 `d58396f94a4d`。
  讀過三個 skill 的 When the Skill Is Changed：它們引用 md-style 是為了一句一行，asd-ste 另外為了美式拼法，check-skill 引用 scratch-rules 是為了 facts file 放在哪裡、怎麼清理，都仍成立。
  6 份重記之後，`depends_on.py check` 都是 UNCHANGED。

### 順帶發現

- app 不在 [tw-keep-english.md](../.github/common/references/tw-keep-english.md) 的清單上，但大多數 twin 都保留英文；只有 imp-home 的三份中文版有 37 處寫成「應用」。
  chinese skill 規定，清單沒有的詞若保留英文，要在同一個 step 加進清單；這次沒有改清單，由 [[Task 59]] 加進清單，並改掉這 37 處。
  compile-skill 的 Tasks-tw.md 有 2 處「應用程式」，翻的是英文的 application，不是 app 的譯法。

## 3. 要做的

✅ 2026-10-18 規則加進 md-style，兩處既有的來歷改掉，依賴方重記。

## 4. 驗證

- md-style.md 與 scratch-rules.md 的 `check_ste.py --ste` 都 PASS，警告和改之前相同。
- md-style 與 scratch-rules 兩對的 `check_parity.py` 都是 0 failure，`diff_md.py --verify` 都 PASS。
- 6 份 README 的 `depends_on.py check` 都是 UNCHANGED；三對 README 的 `check_parity.py` 都是 0 failure，警告和 HEAD 相同。
- check-skill 的 `scan_skill.py` 掃 asd-ste、check-skill、gen-skill：沒有缺少的標題，README 檔頭的紀錄都是 UNCHANGED。

## 5. 與其他 task 的關係

- [[Task 32.7]]：審 scratch-rules 時提出；那一句在 scratch-rules 取代之後是第 36 行，由這個 task 刪掉。
- [[Task 32.8]]：skill-writing 正在審，所以規則不放在 skill-writing.md。
- [[Task 55]]：依賴巡檢的 chore 還沒建立，這次的依賴方在 task 裡直接重記。
- [[Task 59]]：順帶發現的 app 由它加進 tw-keep-english。

## 6. 知識

—

## 7. 日誌

### 2026-10-18

- 建立：使用者決定把「文件不寫自己的來歷」訂成 md-style 的規則，並在這個 task 裡處理既有的兩處。
- 規則加進 md-style 與它的中文版；scratch-rules 刪掉一句，report-my-chats 改寫一句；記錄 md-style 與 scratch-rules 的 6 份 README 重記。
- 更正順帶發現：原本寫 Tasks-tw.md 的「應用程式」是 app 的另一種譯法，其實那兩處翻的是 application；app 的另一種譯法是 imp-home 中文版的「應用」，由 [[Task 59]] 處理。
