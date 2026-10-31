# Task 61 - 規則只寫一次：找出定規則的 md 之間重複的規則

**Status**：完成——2026-10-30 重複的規則照使用者的決定改完；之後的重複檢查併進 [[Task 56]]。
**Raised**：2026-10-18，[[Task 32.8]] 審 skill-writing 時，使用者發現草稿中文版第 19、26 行重複；刪掉原文與草稿的兩處重複之後，問所有定規則的 md 要不要也檢查。
**Depends on**：—

## 1. 背景

- 同一條規則寫在兩個地方，改了一處、忘了另一處，兩份就會說不一樣的話；[skill-writing.md](../.github/common/rules/skill-writing.md) 說 glossary 的定義只寫一次，也是這個道理。
- header quote 的指紋只在重述的檔記錄了來源時才會提醒；沒有記錄來源的重述，來源改了不會有人發現。
- [[Task 32.8]] 在 skill-writing 找到三處原文本來就有的重複，使用者決定刪掉其中兩處（`f087677`）；「README 說明哪些檔案要一起改」是第一條要先讀 README 的理由，保留。

## 2. 現況

### 已決定（2026-10-18）

- 範圍：`.github/common` 裡定規則的 18 份英文檔，中文版跟著它的英文檔改，不另外檢查。
  - rules 的 6 份：[md-style.md](../.github/common/rules/md-style.md)、[report-md-rules.md](../.github/common/rules/report-md-rules.md)、[report-yaml-rules.md](../.github/common/rules/report-yaml-rules.md)、[scratch-rules.md](../.github/common/rules/scratch-rules.md)、[skill-writing.md](../.github/common/rules/skill-writing.md)、[tools.md](../.github/common/rules/tools.md)。
  - references 的 3 份：[DFD.md](../.github/common/references/DFD.md)、[RSDC-Standard.md](../.github/common/references/RSDC-Standard.md)、[tw-keep-english.md](../.github/common/references/tw-keep-english.md)。
  - skill 裡的 3 份：asd-ste 的 [ste-rules.md](../.github/common/skills/asd-ste/references/ste-rules.md) 與 [ste-custom.md](../.github/common/skills/asd-ste/references/ste-custom.md)，check-skill 的 [checking-criteria.md](../.github/common/skills/check-skill/references/checking-criteria.md)。
  - 範本 2 份：[SKILL-tmp.md](../.github/common/templates/SKILL-tmp.md)、[README-tmp.md](../.github/common/templates/README-tmp.md)。
  - CLAUDE.md 4 份：根目錄的 [CLAUDE.md](../CLAUDE.md)、`tasks/CLAUDE.md`、`chores/CLAUDE.md`、[skills/CLAUDE.md](../.github/common/skills/CLAUDE.md)。
- 處理原則：一條規則只留在擁有它的那份檔，其他檔改寫成「照 X」並連過去；刻意保留的重述，在它的 header quote 記錄來源，讓來源改動時指紋提醒。
  每組歸哪一份、刪哪一句，逐組由使用者決定。
- 時機：skill-writing、tools、README-tmp、SKILL-tmp 的 STE 草稿還在 [[Task 32]] 審，這 4 份等取代原檔之後再改，免得已通過的審核項目變回待審；其他檔可以先做，所以不寫成依賴。
- 提交：本 task 的修改前綴 `task 61`。

### 掃描結果（2026-10-18）

- 行號是 2026-10-18 的。
- 18 份共約 2,100 行、1,145 句；用字相近的有 65 組，45 組在同一份檔裡，20 組跨檔。
- 不用刪的四類：
  - RSDC-Standard 的 Changes in This Version 一節重述各版改過的規則：[[Task 58]] 明訂它是不寫來歷的例外。
  - ste-custom 的 Words 與 Rules 兩節刻意寫成平行，例如第 18 行與第 53 行。
  - SKILL-tmp 的每個 step 各有一段範本，例如第 127 行與第 153 行。
  - skills/CLAUDE.md 第 5–8 行重述 skill-writing 的第一條：SKILL.md 不連到 README，agent 靠這個檔找到 README；照處理原則，要不要在它的檔頭記錄 skill-writing.md，另外決定。
- 值得看的四組：
  1. 讀時間的指令：report-md-rules 第 36–37 行與第 53–54 行一字不差寫了兩次，分別在 Create 與 Update 兩節；report-yaml-rules 第 30–31 行再寫一次，格式多了秒。
  2. 版本規則：RSDC-Standard 的 Versioning 一節（第 388 行起）與 tw-keep-english 第 16–19 行各寫一套：檔名不含日期、只有改規則才換版、引用的文件不必改。
  3. 清單項目裡一句一行：md-style 第 37 行與 ste-rules 第 202 行各寫一次，而 ste-rules 沒有在檔頭記錄 md-style.md。
  4. Dataflow 畫什麼：checking-criteria 第 190 行重述 README-tmp 第 28 行「只有 step 執行時讀寫的才畫」，而 checking-criteria 沒有在檔頭記錄 README-tmp.md。
- 掃描的限制：只比對用字相近的英文句子，換了說法的重複抓不到，例如 skill-writing 刪掉的「SKILL.md 不寫 Purpose，因為執行用不到」；所以還要逐份讀。

### 重新掃描（2026-10-30）

- 範圍裡的 `tasks/CLAUDE.md` 與 `chores/CLAUDE.md` 已由 [task-rules.md](../.github/common/rules/task-rules.md) 與 [chore-rules.md](../.github/common/rules/chore-rules.md) 取代，所以 18 份是 rules 的 8 份、references 的 3 份、asd-ste 與 check-skill 的 3 份、範本 2 份、根目錄的 CLAUDE.md 與 skills/CLAUDE.md。
- skill-writing、tools、README-tmp、SKILL-tmp 已由 [[Task 32]] 取代原檔，可以改了。
- 照下面的掃描方法重跑：比對 1,516 行，候選 154 組，跨檔 87 組。
- 跨檔的 87 組裡，61 組在 task-rules 與 chore-rules 之間，是 [[Task 62.1]] 決定兩份各自寫完整的結果。
- 其餘 26 組：RSDC-Standard 與 DFD 的 6 組都在 Changes in This Version 裡，是 [[Task 58]] 的例外；report-md-rules 與 SKILL-tmp 的 3 組是範本的佔位，不是重述規則。

### 決定與修改（2026-10-30）

- **第 1 組，讀時間的指令**：只刪 report-md-rules 裡的重複。
  Update 一節改成「Read them from the system clock at that time, as for `{DATETIME}` above.」，中文版跟著改；report-yaml-rules 的格式有秒，不算同一條規則，照舊。
- **第 2 組，版本規則**：照舊，不算重複。
  RSDC-Standard 的 Versioning 與 tw-keep-english 的版本段各管自己這份檔，tw-keep-english 還多了「或清單」，是同一個寫法，不是同一條規則。
- **第 3 組，清單項目一句一行**：刪掉 [ste-rules.md](../.github/common/skills/asd-ste/references/ste-rules.md) House Rule 3 的第二行，上一行已經連到 md-style.md。
- **第 4 組與其他三處，檢查標準與範本的重述**：保留，在檔頭記錄來源。
  [checking-criteria.md](../.github/common/skills/check-skill/references/checking-criteria.md) 與中文版的檔頭記錄 `[[README-tmp]]` 與 `[[skill-writing]]`。
  README-tmp 不記錄：它檔頭的路徑連結是給新 README 複製用的，`{COMMON_PATH}` 記錄不了；加 wikilink 紀錄的話，gen-skill 會把它們複製進每份新 README。
  照範本寫出的每份 README 本來就宣告並記錄 DFD.md 與 skill-writing.md，兩者一改，check-skill 就會報 CHANGED。
- **ste-rules 與 ste-custom**：House Rule 11 只留 ste-rules 自己的規則（核准詞不是技術用字、每份 STE 檔都宣告 ste-custom.md），兩張表放什麼、怎麼檢查、新的詞或規則怎麼加進去，改成照 [ste-custom.md](../.github/common/skills/asd-ste/references/ste-custom.md)。
- **skills/CLAUDE.md**：不在檔頭記錄 skill-writing.md；那一行本來就連過去，加上紀錄，每個 session 都要多讀，skill-writing 每改一次也要重記。
- **task-rules 與 chore-rules**：維持 [[Task 62.1]] 的決定。
- 檢查：report-md-rules 的 `check_ste.py --ste` PASS；兩對中英對照的 `check_parity.py` 0 failure，checking-criteria 的兩則警告在 HEAD 時就有；改過的 5 份重跑 `reformat_md.py` 都沒有變；asd-ste 的 SKILL.md 與中文版讀過 ste-rules 的改動之後重記，`depends_on.py check` 都是 UNCHANGED；check-skill 的 `scan_skill.py` 對 check-skill、asd-ste、gen-skill 都沒有缺少的標題。

### 逐份讀的結果與決定（2026-10-30）

- 由 subagent 逐份讀 18 份，找掃描抓不到、換了說法的重複：跨檔 12 組（C1–C12）、同一份檔裡 10 組（W1–W10），由使用者逐組決定。
- 照舊的：
  - C2：SKILL-tmp 對 Checkpoint Dir 的「一個 writer」比 DFD.md 嚴（後面的 step 不改前一個 step 的檔），是範本選的較嚴做法，不矛盾。
  - C3–C5：SKILL-tmp 重述 report-yaml-rules 與 report-md-rules 的 step_N 組、MD report 的五個欄位與 report 的位置，當作範本的重述。
  - C6、C8、C10：README-tmp 重述 skill-writing、DFD.md 與 CLAUDE.md 的規則，當作範本的重述。
  - C6、C9、C11：skills/CLAUDE.md 第 6、8 行與根目錄 CLAUDE.md 的 task、chore 位置與 md-style 範圍，是把人帶到規則檔的指標。
  - C7：ste-rules 的 1.14 是 STE 自己的規則，不是重述 md-style。
  - C12：tw-keep-english 的 Why 欄是保留英文的理由，不是規則；DFD.md 若換掉 role 的形狀，第 125 行要跟著改。
- 改了的：
  - C1：「每份 STE 檔都宣告 ste-custom.md」只留在 ste-rules 的 House Rule 5，House Rule 11 拿掉那一句，ste-custom 第 8 行改成照 House Rule 5。
  - W1：SKILL-tmp 的 glossary 只定義 `run step N`，「從 YAML checkpoint 讀取先前 step 的輸出」移到 MUST FOLLOW 的那一條。
  - W2、W3：ste-rules 的 House Rule 5 與 7 改成照 House Rule 1 保留檔頭與 frontmatter；「核准詞不列為技術用字」只留在 House Rule 6。
  - W4：RSDC-Standard 第 1 章的兩句改成一句，指到 Invariants 結尾的目標表；只改措辭，照它的版本規則不換版。
  - W5：report-yaml-rules 的 `Xm Ys` 與「只算滿的分鐘」各只寫一次。
  - W6：report-md-rules 的 Update 一節改成照 `{DATETIME}` 設定 Updated。
  - W7：task-rules 拿掉「建立 task 時，第一個日期 section 就是 Raised 的日期」，留下「最後一個日期 section 一定是 Raised 的日期」。
  - W8：skill-writing 第 21 行不再列出 README 的各節，由第 44、49 行說。
  - W9：md-style 的轉換 5 與 9 改成照上面的規則，不再重述 `\#` 與引用標記的理由。
  - W10：checking-criteria 的 description 長度、超過上限的代價與 Dataflow 的理由，各只留在它的判準裡。
  - 要做的第 5 項：skill-writing 那條規則的粗體標題帶上「scripted-versus-not」。
- 範圍外：ste-rules 與 checking-criteria 仍有英式拼法（judgement、behaviour、colour 等），使用者決定記進 [[Task 56]]；checking-criteria 把同一條規則叫作 script-versus-judgement，和 skill-writing 的 scripted-versus-not 不同，改拼法時一起看。
- 檢查：
  - 改過的 STE 檔（SKILL-tmp、RSDC-Standard、report-yaml-rules、report-md-rules、task-rules、skill-writing、md-style）`check_ste.py --ste` 都 PASS；md-style 新寫的一句原本超過 20 字，拆成兩句。
  - 9 對中英對照 `check_parity.py` 0 failure；ste-custom 中文版的兩個連結順序原本和英文相反，已改；RSDC-Standard 與 checking-criteria 的警告在 HEAD 時就有。
  - 改過的檔重跑 `reformat_md.py` 都沒有變。
  - 記錄它們的文件讀過改動之後重記 42 筆：RSDC-Standard 的 12 份（含 InvestForge 的 4 份）、gen-skill、check-skill、compile-skill、asd-ste 的 README 與中文版、checking-criteria 兩份、asd-ste 的 SKILL 兩份。
  - ste-custom 改了，照它的規定以 `draft.py recheck` 重查並重記 26 份 STE 檔，都 PASS。
  - 之後所有記錄都是 UNCHANGED，只剩 check-md-deps 對 check-wiki-doc 的兩筆 CHANGED，在本 task 之前就有。
  - check-skill 的 `scan_skill.py` 對 check-skill、asd-ste、gen-skill、compile-skill 都沒有缺少的標題。

### 掃描方法

- 每份英文檔一行當一句；略過 fenced block、表格列與 block quote，也略過去掉 a、the、of、to、and 這類虛詞之後少於 6 個詞的行。
- 兩句的詞集合重疊（交集除以聯集）至少 0.45，而且詞序列的相似度（Python `difflib.SequenceMatcher` 的 ratio）至少 0.55，就列為一組候選；同一份檔裡相鄰的兩行不比。
- 這次的腳本沒有放進 repo；要重跑就照這兩條寫一支，做成 chore 時再決定要不要變成工具。

## 3. 要做的

1. ✅ 照處理原則，逐組請使用者決定：先處理值得看的四組，再看其他跨檔的候選，最後是同一份檔裡的候選（2026-10-30，見「決定與修改」）。
2. ✅ 逐份讀範圍內的 18 份，找出掃描抓不到、換了說法的重複，同樣逐組決定（2026-10-30）。
3. ✅ 每改一份，照它的種類做該做的事（2026-10-30）：
   - STE 檔（DFD、RSDC-Standard、tw-keep-english、md-style、report-md-rules、report-yaml-rules、scratch-rules）：`check_ste.py --ste` 重查，中文版照 chinese skill 跟著改，記錄它的文件讀過之後重記；RSDC-Standard 與 tw-keep-english 還要照各自的版本規則決定換不換版。
   - skill 裡的檔（ste-rules、ste-custom、checking-criteria）：先讀那個 skill 的 README 的 When the Skill Is Changed，照它改，並跑它列的檢查；ste-custom 改了，照 [[rerecord-ste-custom]] 當天集中重記。
   - 還在 [[Task 32]] 審的 4 份：等取代原檔之後再改。
4. ✅ 做完之後，決定重複檢查要不要做成 chore：併進 [[Task 56]] 的 md-style 巡檢，或另開一個。
   使用者決定併進 [[Task 56]]，只用字詞相近的掃描，範圍是這 18 份；已決定保留的重述列在 Task 56，巡檢時跳過（2026-10-30）。
5. ✅ skill-writing 那條「If a program can do a step deterministically, the step operates a script.」的規則，在粗體標題帶上「scripted-versus-not」這個名稱，照「no forward-reference」的寫法放在引號裡（2026-10-30）。
   check-skill、gen-skill、gen-imp-app 與三份 README 都用這個名稱稱呼它，skill-writing 卻沒有寫出這個名稱；改了之後名稱才有出處。
   skill-writing 是 STE 檔：`check_ste.py --ste` 重查，中文版照 chinese skill 跟著改，記錄 skill-writing.md 的 6 份 README 讀過之後重記。
   這一項是 [[Task 32.10]] 審 README-tmp 時，使用者在 2026-10-18 交給本 task 的。

## 4. 驗證

- 值得看的四組與之後找到的每一組，都照使用者的決定處理，或寫明保留的理由。
- 改過的每一份：STE 檔的 `check_ste.py --ste` PASS，中英對照的 `check_parity.py` 0 failure、`diff_md.py --verify` PASS，記錄它的文件 `depends_on.py check` 都是 UNCHANGED。
- `check_tasks.py` PASS。

## 5. 與其他 task 的關係

- [[Task 32]]：審 skill-writing（[[Task 32.8]]）時提出；還在審的 4 份等取代原檔之後再處理。
- [[Task 58]]：RSDC 文件的 Changes in This Version 一節是不寫來歷的例外，那裡重述改過的規則不算重複。
- [[Task 24]]：14 個舊格式 skill 的 SKILL.md 仍重述 skill-writing 的第 4、5 條（step 自成一體、程式能做的 step 執行 script），改成新格式時拿掉，不在本 task 處理。
- [[Task 56]]：md-style 巡檢的 chore；本 task 做完之後，決定重複檢查要不要併進去。
- [[Task 32.10]]：審 README-tmp 時決定保留規則的名稱 scripted-versus-not，skill-writing 補上這個名稱交給本 task（要做的第 5 項）。

## 6. 日誌

### 2026-10-30

- 重新掃描：跨檔 87 組，其中 61 組是 task-rules 與 chore-rules 刻意的重述。
- 原本的四組與另外三組由使用者決定：改了 report-md-rules 與中文版、ste-rules，checking-criteria 與中文版的檔頭記錄兩個來源；第 2 組、skills/CLAUDE.md、task-rules 與 chore-rules 照舊。
- 逐份讀範圍內的 18 份：跨檔 12 組、同檔 10 組，使用者決定改 C1 與 W1–W10，其餘照舊；skill-writing 的規則標題帶上 scripted-versus-not。
- 檢查與重記：STE 檢查、中英對照、一句一行都通過；重記 42 筆，ste-custom 以 `draft.py recheck` 重記 26 份。
- 英式拼法記進 [[Task 56]]。
- 重複檢查併進 [[Task 56]]，本 task 完成。
- [[Task 86]] 把 chore 改用名稱：本檔的 `[[Chore N]]` 連結改成新名稱。

### 2026-10-18

- 建立：記下範圍、處理原則與時機，以及快速掃描的結果與方法。
- `tasks/CLAUDE.md` 與 `chores/CLAUDE.md` 已刪除：它們的規則改寫成 [task-rules.md](../.github/common/rules/task-rules.md) 與 [chore-rules.md](../.github/common/rules/chore-rules.md)，兩份各自寫完整，共用的約 10 條規則兩份都寫（[[Task 62.1]]）；範圍裡指向它們的連結改成 inline code。
- [[Task 32.10]] 交來要做的第 5 項：skill-writing 那條規則的標題帶上「scripted-versus-not」這個名稱。
