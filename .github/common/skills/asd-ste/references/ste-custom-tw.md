# Project-Approved Words and Rules

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-12`  `d1f4ea9e7cd6`

本專案在 ASD-STE100 Simplified Technical English 的 Issue 9 之外另行核准的詞與寫作規則。
asd-ste skill 使用這些詞，就像使用 [ste-dictionary.json](ste-dictionary.json) 的核准詞一樣；遵守這些規則，就像遵守 [ste-rules.md](ste-rules.md) 的 House Rules 一樣。
`check_ste.py --custom` 會讀取詞的表格，規則表格中標為會檢查的每一條規則，則由 `check_ste.py` 檢查。
每份 STE file 都在它的 header quote 中宣告本檔：`> [[ste-custom]]`，照 [ste-rules.md](ste-rules.md) 的 House Rule 5，再由 `depends_on.py record` 記錄它的指紋。
本檔一改，`depends_on.py check` 就會回報每一份 STE file 為 CHANGED，但不必每改一次就重新檢查一次。
當天最後一次修改之後，從 workspace 根目錄執行一次 [draft.py](../scripts/draft.py) `recheck`，每個 workspace 資料夾各給一個 `--root`，並把它重記的結果單獨 commit。
它以 `run step 3` 的方式重新檢查草稿、以 `check_ste.py --ste` 重新檢查草稿取代過的檔案，在通過的每一份中重記本檔，沒通過的則連同它的 `[FAIL]` 一一列出，交給你修正。
正在處理的那份草稿是例外：立刻對它執行 run step 3；本檔在它上次檢查之後改過時，Step 6 與 Step 7 會自己先重跑。

## Words

- 每個詞只在它那一列給出的詞性與詞形中、以它的意思獲得核准。
- `check_ste.py` 把每一個都當成核准詞，並以一行 `[INFO]` 列出檔案用到的每一個，讓審核的人看到每一個 Issue 9 不核准的詞。
- 一個詞只有在使用者決定之後才加進表格，它的 Why 欄寫明何時、為什麼。
- `check_ste.py` 以標題列找到這張表格：標題列的五個儲存格要維持原樣。
  詞性照字典的寫法——`n`、`v`、`adj`、`adv`、`prep`、`conj`、`pron`——以逗號分隔。
  詞形以逗號分隔；沒有詞形時寫 `—`。

| Word | Part of speech | Forms | Meaning | Why |
|---|---|---|---|---|
| current | adj | — | 現在這個時候的，例如「the current date and time」 | 2026-10-12，使用者在以 STE 改寫 report-md-rules.md 時（Task 31 第 2.5 步）核准：Issue 9 沒有收錄這個詞，而「current local date-time」沒有同樣簡短、清楚的 STE 寫法。 |
| now | adv | — | 在這個時候 | 2026-10-12，使用者與 current 一起核准：Issue 9 不核准這個詞，並以 AT THIS TIME 取代。 |
| message | n | — | 程式顯示給人看、告知某種狀況的文字，例如「no error message」 | 2026-10-12，使用者在以 STE 改寫 md-style.md 時（Task 31 第 2.6 步）核准：Issue 9 沒有收錄這個詞，而「and no message tells you」說出了 silently 的意思；report-md-rules-ste.md 原本把它列為 technical word。 |
| translate | v | translates, translated, translating | 把一段文字用另一種語言重新寫出，就像 twin 對它的英文檔所做的 | 2026-10-13，使用者在以 STE 改寫 tw-keep-english.md 時（Task 31 第 3 步）核准：Issue 9 沒有收錄這個詞，而那份檔案講的就是翻譯。 |
| translator | n | — | 翻譯文字的人或 agent | 2026-10-13，使用者與 translate 一起核准：Issue 9 沒有收錄這個詞。 |
| reader | n | — | 閱讀文件或其中資料的人或程式 | 2026-10-13，使用者與 translate 一起核准：Issue 9 沒有收錄這個詞；DFD-ste.md 與 RSDC-Standard-ste.md 原本把它列為 technical word。 |
| warning | n | — | 檢查針對可能的問題所顯示、不會中止執行的一行，例如一行 `[WARN]` | 2026-10-13，使用者與 translate 一起核准：Issue 9 只把 WARNING 列為 technical noun。 |
| state | n | — | system 的某個部分可能處於的狀況之一，例如 stale 就是一種 state | 2026-10-13，使用者在以 STE 改寫 tw-keep-english.md 時（Task 31 第 3 步）核准：Issue 9 以 CONDITION 取代這個詞，但那份檔案的規則把 type、state、outcome 與 role 當成 system 裡的四種東西。 |
| outcome | n | — | 一次執行或一個 step 交回的結果，例如 verdict 或 handoff | 2026-10-13，使用者與 state 一起核准：Issue 9 沒有收錄這個詞，而 outcome 本身就是 keep-English list 上的詞。 |
| role | n | — | 一個人或一個程式在一次執行中所擔任的 role，例如使用者、agent 或 caller | 2026-10-13，使用者與 state 一起核准：Issue 9 沒有收錄這個詞；DFD-ste.md 與 RSDC-Standard-ste.md 原本把它列為 technical word。 |
| depend | v | depends, depended, depending | 依賴另一份檔案：那份檔案一改，這裡就可能必須跟著改，例如 README 依賴它的檔頭引用區所宣告的每一份檔案 | 2026-10-13，使用者在以 STE 改寫 README-tmp.md 時（Task 31 第 4 步）核准：Issue 9 對這個詞只給了 IF，而檔頭引用區與 depends_on.py 都以它命名。 |
| interact | v | interacts, interacted, interacting | 彼此作用，例如 role 向 system 提供資料、或從 system 讀取資料 | 2026-10-13，使用者在審核 DFD-ste.md 時（Task 32）核准：Issue 9 沒有收錄這個詞，而「does work with the system」說不出「interacts with the system」的意思。 |
| purpose | n | — | 一個東西存在或被做的原因，或拿來做什麼，例如一種資料或一個 step 的 purpose | 2026-10-14，使用者在審核 RSDC-Standard.md 時（Task 32）核准：Issue 9 把這個詞從字表中移除，只把它列為法律與規範類的 technical noun；最接近的核准詞 FUNCTION 說的是一個東西做什麼，不是拿來做什麼。 |
| capability | n | — | 規格要求 system 要能做到的一件事，例如 RSDC-Standard.md 對照表的每一列 | 2026-10-14，使用者與 purpose 一起核准：Issue 9 以 FUNCTION 與 CAN 取代這個詞，但 RSDC-Standard.md 有一條規則名為「Not every control is a capability」，這種粗體標籤要維持原樣，而內文必須用同一個名稱稱呼那件事。 |
| create | v | creates, created, creating | 建立新的檔案、新的目錄或新的資料，例如 skill 建立它的 MD report 檔案 | 2026-10-14，使用者在審核 report-md-rules.md 時（Task 32）核准：Issue 9 以 MAKE 與 CAUSE 取代這個詞，但 report-md-rules.md 的第一節名為「Create MD report file」，這個標題要維持原樣，而內文必須用同一個詞稱呼這個動作。2026-10-18，使用者在審核 scratch-rules.md 時（Task 32.7）加上新的目錄，例如「Create the directory if it is not there」。 |
| rule | n | — | 說明該做什麼、不該做什麼的一條規定，例如 report-yaml-rules.md 的每一項 | 2026-10-16，使用者在審核 report-yaml-rules.md 時（Task 32 第 2.6 步）核准：Issue 9 沒有收錄這個詞，而本專案的每一份規則檔都用到它，例如標題「YAML Checkpoint Rules」；原本有 10 份 STE 檔把它列為 technical word。 |
| phrase | n | — | 合在一起使用的一組詞，例如「a word or a phrase」 | 2026-10-16，使用者在審核 tw-keep-english.md 時（Task 32 第 2.3 步）核准：Issue 9 沒有收錄這個詞，而 term 的定義說的是「a word or a phrase」；原本有 2 份 STE 檔把它列為 technical word。 |
| false | adj | — | 不真實或不正確的，例如 false alarm 就是對正確事物發出的警告 | 2026-10-17，使用者在審核 tw-keep-english.md 時（Task 32 第 2.3 步）核准：Issue 9 不核准這個詞，並以 INCORRECT 取代，但原文寫的是「without false alarms」。 |
| false alarm | n | false alarms | 對正確事物發出的警告，例如工具在正確的句子裡找到某個譯法 | 2026-10-17，使用者與 false 一起核准：Issue 9 沒有收錄 alarm，而原文寫的是「without false alarms」。 |
| update | v | updates, updated, updating | 修改檔案或其中的資料，讓它成為最新的狀態，例如 skill 更新它的 MD report 檔案 | 2026-10-18，使用者在審核 report-md-rules.md 時（Task 32.5）核准：Issue 9 沒有收錄這個詞，而 report-md-rules.md 的第二節名為「Update MD report file」，這個標題要維持原樣，而內文必須用同一個詞稱呼這個動作；report-md-rules-ste.md 原本把它列為 technical word。 |
| merge | v | merges, merged, merging | 把新的值併進既有的檔案或群組，沒有改的值照舊，例如 step 把它的群組合併進 YAML checkpoint | 2026-10-18，使用者在審核 report-yaml-rules.md 時（Task 32.6）核准：Issue 9 沒有收錄這個詞，而 report-yaml-rules.md 寫的是「merge/update only the relevant `step_{number}` group」；草稿原本寫的 change 說不出沒有改的值會照舊。 |
| own | adj, pron | — | 屬於前面提到的那一個、不屬於別的，例如「each output has its own path」；當代名詞時，指屬於它的那一個，例如「a path of its own」 | 2026-10-18，使用者在審核 scratch-rules.md 時（Task 32.7）核准：Issue 9 沒有收錄這個詞，而「has its own path」說出了「has a different path」沒說出的意思：這個路徑只給那一種輸出用。 |
| program | n | — | 電腦執行的一組指令，例如 script 或 `check_ste.py` | 2026-10-18，使用者在審核 skill-writing.md 時（Task 32.8）核准：Issue 9 不核准這個名詞，並以 SEQUENCE 取代，但 sequence 是 step 的順序，不是電腦執行的一組指令，例如「A step that a program can do deterministically runs a script」；原本有 3 份 STE 檔把它列為 technical word。 |
| programming | n | — | 寫程式這件工作，例如「the programming style」 | 2026-10-18，使用者與 program 一起核准：Issue 9 沒有收錄這個詞；RSDC-Standard.md 原本把它列為 technical word。 |
| deterministic | adj | — | 同樣的輸入總是得到同樣的輸出，例如 script 能做的 step | 2026-10-18，使用者在審核 skill-writing.md 時（Task 32.8）核准：Issue 9 沒有收錄這個詞，而 skill-writing.md 寫的是「A step that a program can do deterministically runs a script」；它是 keep-English list 上的 term，tw-keep-english.md 原本把它列為 technical word。 |
| deterministically | adv | — | 以同樣的輸入總是得到同樣輸出的方式 | 2026-10-18，使用者與 deterministic 一起核准：Issue 9 沒有收錄這個詞。 |
| search | v, n | searches, searched, searching | 在檔案或文字中找一個 pattern，就像 `rg` 所做的；當名詞時，指這樣做一次，例如「a verification search」 | 2026-10-18，使用者在審核 tools.md 時（Task 32.9）核准：Issue 9 以 EXAMINE 取代這個詞，但 tools.md 的第一節名為「Search with `rg`」，這個標題要維持原樣，而內文必須用同一個詞稱呼這個動作；tools-ste.md 與 DFD.md 原本把它列為 technical word。 |
| need | v | needs, needed, needing | 處於某樣東西對你是必要的狀況，例如「the range you need」 | 2026-10-18，使用者在審核 tools.md 時（Task 32.9）核准：Issue 9 以 NECESSARY 取代這個詞，但 tools.md 在兩個標題「Pick the flag by what you need to know」與「Read only the range you need」中用到它，這兩個標題要維持原樣，表格的標題列「What you need」也用到它。 |
| exception | n | — | 規則或預設做法不涵蓋的情況，例如「Exception: if rg cannot isolate the one range that you want」 | 2026-10-18，使用者在審核 tools.md 時（Task 32.9）核准：Issue 9 不核准這個詞，也沒有給替代的詞，而 tools.md 的一條規則用「Default:」與「Exception —」開頭兩個項目，草稿保留這一對。 |
| run | v, n | runs, ran, running | 讓程式、script、skill 或 step 做它的工作，例如「When the Skill Runs」；當名詞時，指這樣做一次，例如「each run of the skill」 | 2026-10-18，使用者在審核 README-tmp.md 時（Task 32.10）核准：Issue 9 以 OPERATE 取代這個詞，但 README-tmp.md 有一節名為「When the Skill Runs」，每一份 README 都要維持這個標題原樣，而 STE 檔也用這個名詞稱呼 skill 執行的一次；原本有 10 份 STE 檔與 2 份草稿把它列為 technical word。 |
| prompt | n | — | 使用者給 agent 的文字，例如啟動 skill 的指令與它的輸入，如「Prompt Examples」 | 2026-10-19，使用者在審核 SKILL-tmp.md 時（Task 32.11）核准：Issue 9 只把這個詞列為形容詞，而且不核准，但 SKILL-tmp.md 有一節名為「Prompt Examples」，另有「Prompt 1」到「Prompt 3」三節，每一份 SKILL.md 都要維持這些標題原樣；它是 keep-English list 上的 term，tw-keep-english.md、README-tmp.md 與 SKILL-tmp 的草稿原本把它列為 technical word。 |

## Rules

- 每一條規則，都是使用者在 Issue 9 的規則與 ste-rules.md 的 House Rules 之外，為本專案加上的寫作規則；草稿要遵守每一條。
- 一條規則只有在使用者決定之後才加進表格，它的 Why 欄寫明何時、為什麼。
- Checked 欄寫出這條規則怎麼檢查：`check_ste.py` 在正文可能違反它的地方發出一行 `[WARN]`，由人逐一讀過再決定；寫 `—` 表示只由審核的人檢查。

| Rule | Example | Checked | Why |
|---|---|---|---|
| 不要用兩個否定表達一個肯定的意思：改寫成肯定句。 | 「Do not write a command incorrectly.」改成「Write each command correctly.」 | `check_ste.py` 發出一行 `[WARN]`「double negative?」：否定詞之後，在同一個子句中接著一個由否定字首加上核准詞所構成的詞 | 2026-10-17，使用者在審核 tw-keep-english.md 時（Task 32 第 2.3 步）決定：Issue 9 沒有關於雙重否定的規則，而兩個否定會讓讀者停下來，才找得到肯定的意思。 |
| 原文替一樣東西取的名稱，例如一條規則的名稱，要照原樣保留，寫在引號裡。 | 「The scripted-versus-not rule of skill-writing.md」寫成「the "scripted-versus-not" rule of skill-writing.md」，不寫成「the rule of skill-writing.md about scripts」。 | — | 2026-10-18，使用者在審核 README-tmp.md 時（Task 32.10）決定：草稿把 scripted-versus-not 規則寫成「the rule of skill-writing.md about scripts」，但 check-skill、gen-skill 與三份 README 都用這個名稱稱呼它，而 STE 規定一樣東西只用一個名稱（規則 1.11）；skill-writing-ste.md 也因同樣的理由把「no forward-reference」寫在引號裡。 |
