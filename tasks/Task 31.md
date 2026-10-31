# Task 31 - 交給 asd-ste 為 .github/common 的 references、rules、templates 產生 STE 草稿

**Status**：完成——2026-10-13：11 份原檔的 STE 草稿與草稿中文版都已產生，可以交給 [[Task 32]] 審核：DFD 與 RSDC-Standard 的草稿改好（`c508e40`），report-yaml-rules（`2828bd5`）、scratch-rules（`1ac3459`）、skill-writing（`85d6cd3`）、tools（`fcc9ff4`）、report-md-rules（`7f3614d`）、md-style（`15aae9d`）、tw-keep-english（`dd12730`）、SKILL-tmp（`cbf93d6`）與 README-tmp（`692b3ef`）的草稿與草稿中文版寫好；[[Task 33]] 已從原檔拿掉指向中文版的那一句（2026-10-12），原本沒有中文版的 4 份，[[Task 34]] 已寫出中文版（2026-10-12）。
**Raised**：2026-10-12，列出 `.github/common` 底下（不含 `skills/`）的 md 檔之後，使用者要求逐步完成每一份的 STE 與 STE 中文版，人工審核後以 STE 取代原檔。
**Depends on**：[[Task 33]]、[[Task 34]]、[[Task 35]]

## 1. 背景

背景：[[Task 23]] 建立了 asd-ste skill。
用它寫成的 STE 草稿目前只有 DFD 與 RSDC-Standard 兩組，放在原檔旁邊，檔頭寫明「兩份不一致時，以原檔為準」。
本 task 把同一範圍的每一份檔案都交給 asd-ste 產生 STE 草稿與它的中文版。
本 task 自己不改原檔：人工審核與審核通過後的取代，都在 [[Task 32]]。

## 2. 現況

**檔案（2026-10-12）**

`.github/common` 底下、不含 `skills/` 的 11 份原檔；括號裡是行數，2026-10-12 第 2.1 步時重新量過。

| 資料夾 | 原檔 | 中文版 | STE 草稿 | STE 草稿中文版 |
|---|---|---|---|---|
| references | [DFD.md](../.github/common/references/DFD.md)（89） | [DFD-tw.md](../.github/common/references/DFD-tw.md)（89） | `DFD-ste.md`（153，2026-10-13 已取代原檔） | `DFD-ste-tw.md`（153，2026-10-13 已取代中文版） |
| references | [RSDC-Standard.md](../.github/common/references/RSDC-Standard.md)（308） | [RSDC-Standard-tw.md](../.github/common/references/RSDC-Standard-tw.md)（308） | `RSDC-Standard-ste.md`（718，2026-10-14 已取代原檔） | `RSDC-Standard-ste-tw.md`（718，2026-10-14 已取代中文版） |
| references | [tw-keep-english.md](../.github/common/references/tw-keep-english.md)（108） | [tw-keep-english-tw.md](../.github/common/references/tw-keep-english-tw.md)（108） | `tw-keep-english-ste.md`（129，2026-10-18 已取代原檔） | `tw-keep-english-ste-tw.md`（129，2026-10-18 已取代中文版） |
| rules | [md-style.md](../.github/common/rules/md-style.md)（76） | [md-style-tw.md](../.github/common/rules/md-style-tw.md)（76） | `md-style-ste.md`（153，2026-10-14 已取代原檔） | `md-style-ste-tw.md`（153，2026-10-14 已取代中文版） |
| rules | [report-md-rules.md](../.github/common/rules/report-md-rules.md)（61） | [report-md-rules-tw.md](../.github/common/rules/report-md-rules-tw.md)（61） | `report-md-rules-ste.md`（88，2026-10-18 已取代原檔） | `report-md-rules-ste-tw.md`（88，2026-10-18 已取代中文版） |
| rules | [report-yaml-rules.md](../.github/common/rules/report-yaml-rules.md)（17） | [report-yaml-rules-tw.md](../.github/common/rules/report-yaml-rules-tw.md)（17） | `report-yaml-rules-ste.md`（45，2026-10-18 已取代原檔） | `report-yaml-rules-ste-tw.md`（45，2026-10-18 已取代中文版） |
| rules | [scratch-rules.md](../.github/common/rules/scratch-rules.md)（27） | [scratch-rules-tw.md](../.github/common/rules/scratch-rules-tw.md)（27） | `scratch-rules-ste.md`（52，2026-10-18 已取代原檔） | `scratch-rules-ste-tw.md`（52，2026-10-18 已取代中文版） |
| rules | [skill-writing.md](../.github/common/rules/skill-writing.md)（28） | [skill-writing-tw.md](../.github/common/rules/skill-writing-tw.md)（28） | `skill-writing-ste.md`（48，2026-10-18 已取代原檔） | `skill-writing-ste-tw.md`（48，2026-10-18 已取代中文版） |
| rules | [tools.md](../.github/common/rules/tools.md)（54） | [tools-tw.md](../.github/common/rules/tools-tw.md)（54） | `tools-ste.md`（97，2026-10-18 已取代原檔） | `tools-ste-tw.md`（97，2026-10-18 已取代中文版） |
| templates | [README-tmp.md](../.github/common/templates/README-tmp.md)（172） | [README-tmp-tw.md](../.github/common/templates/README-tmp-tw.md)（172） | `README-tmp-ste.md`（196，2026-10-19 已取代原檔） | `README-tmp-ste-tw.md`（196，2026-10-19 已取代中文版） |
| templates | [SKILL-tmp.md](../.github/common/templates/SKILL-tmp.md)（161） | [SKILL-tmp-tw.md](../.github/common/templates/SKILL-tmp-tw.md)（164） | `SKILL-tmp-ste.md`（202，2026-10-19 已取代原檔） | `SKILL-tmp-ste-tw.md`（205，2026-10-19 已取代中文版） |

**已決定（2026-10-12）**

提出時問了 12 個問題，兩次改寫範圍時又問了 16 個，決定如下：

- **分工**：本 task 把產生 STE 草稿與草稿的中文版交給 asd-ste；人工審核、通過後的取代與取代後的後續，都歸 [[Task 32]]。
- **範圍**：其餘 9 份全部做——references 的 tw-keep-english、rules 的 6 份、templates 的 README-tmp 與 SKILL-tmp；DFD 與 RSDC-Standard 已有草稿，照下一段改好。
- **STE 中文版**：每一份草稿都配一份中文版。
  原本沒有中文版的 4 份（tw-keep-english、md-style、report-md-rules、report-yaml-rules），先由 [[Task 34]] 執行 /chinese 寫出原檔的中文版，再產生草稿；Task 34 已於 2026-10-12 寫出。
- **順序**：先改好 DFD 與 RSDC-Standard 兩份現有的草稿；其餘依 rules、references、templates 的順序做，範本影響最大，排最後。
  每完成一份，就可以交給 Task 32 審核。
- **一句一行**：草稿要是一句一行。
  兩份現有的草稿已經是（2026-10-12 用 reformat-md 在副本上試轉，沒有一句要拆）。
  `RSDC-Standard-ste` 與 `tools` 兩組原本在 [[Task 19]] 待轉的清單上，改由本 task 處理。
- **完成條件**：11 份草稿與它們的中文版都已產生，並通過下面的驗證。

**2026-10-12 做了什麼：第 1 步**（commit `c508e40`）

做之前問了 8 個問題，決定如下：新內容只寫進草稿、註明是刻意的；照使用者確認過的文字改；用編輯工具改草稿，再照 asd-ste 跑 `run step 3`、`4`、`5`；4 個檔一個 commit；中文版照 chinese 的流程譯好就寫入。

- **草稿**：RSDC-Standard-ste.md 改了 4 處——Version 行、版本規則句、「只改文字或版面」一段、261010 一節開頭一段；DFD-ste.md 改了 1 處——版本規則句。
- **asd-ste**：Step 3 兩份都 PASS；RSDC-Standard 留下 4 個被動句警告，都在照原文保留的粗體規則名稱裡。
  PDF 依賴重記為 2026-10-12。
  Step 4 先不 commit，Step 5 交給 chinese；YAML checkpoint 在 `checkpoints/asd-ste/references-DFD/` 與 `references-RSDC-Standard/`。
- **中文版**：chinese 判定 INCREMENTAL，DFD 譯 2 行、RSDC-Standard 譯 10 行；`check_parity.py` 0 failure、0 warning，`diff_md.py --verify` 通過。
- **一句一行**：用 reformat-md 在副本上試轉，沒有一句要拆。
- **刻意與原檔不同的 4 處**：給 Task 32 審核時對照，也記在 asd-ste 的 YAML checkpoint 的 `intentional_differences`。
  行號是 [[Task 33]] 第 2 步從兩份草稿拿掉指向中文版的 4 行、本 task 第 3 步在兩份的檔頭加上 `[[ste-custom]]` 一行之後的。
  1. RSDC-Standard-ste 第 28–29 行：只有規則改變才產生新版本；改規則時才照下列步驟做。
     原檔說每次修訂都更新版本。
  2. RSDC-Standard-ste 第 37–38 行：只改文字或版面時不改版本，在該版本的小節說明這次改動。
  3. RSDC-Standard-ste 第 405–407 行：261010 一節開頭說明文字已改寫成 STE、規則未變，以及新的版本規則。
  4. DFD-ste 第 23 行：只有改動 DFD.md 裡的規則才是標準的新版本。
     原檔說任何修改都是新版本。
- **順帶發現**：asd-ste 的 `save_step.py --help` 會出錯，因為說明文字裡的時間格式含 `%`，argparse 把它當成格式符號；照常傳參數則可用。
  留給 [[Task 32]] 改 asd-ste 時一併修。

**2026-10-12 做了什麼：第 2.1 步**（commit `2828bd5`）

做之前問了 4 個問題，決定如下：兩句難寫成 STE 的話照建議的說法寫（見下面第 3、4 點）；草稿與它的中文版一個 commit；這筆紀錄另一個 commit，順便更正表格與第 2 步清單裡過期的行數。

- **asd-ste**：Step 3 PASS，沒有 WARN；草稿 45 行、37 句，用了 27 個 technical word，沒有一句保留原文的說法。
  PDF 依賴記為 2026-10-12。
  Step 4 先不 commit，Step 5 交給 chinese；YAML checkpoint 在 `checkpoints/asd-ste/rules-report-yaml-rules/`。
- **中文版**：還沒有中文版，chinese 判定 FULL，45 行逐行整份翻譯；`check_parity.py` 0 failure、0 warning；keep-English 清單沒有加詞。
- **一句一行**：用 reformat-md 在副本上試轉，兩份都沒有改變。
- **審核時可以留意的地方**：行號是草稿的。
  1. 原檔第 4 行括號裡的話，拆成第 10–13 行四句：checkpoint 都放在 workspace 根目錄的 `checkpoints\`；這個目錄不變；它不像 MD report 的根目錄，不能在 `config.yaml` 設定；最後才說有兩種佈局。
  2. 結構：原檔第 10、11 行各是一句，草稿把欄位改成子清單（第 21–27 行）。
     原檔第 12–13 行的一個條列改寫後有 8 句，超過一段 6 句的上限，所以拆成第 28–31 行與第 32–35 行兩個條列。
     原檔第 14–16 行也拆成第 36–40 行與第 41–44 行兩個條列：第 38–40 行是子清單，接在它後面的句子會被併進最後一個子項目。
  3. 第 34–35 行：「重建的時間就是捏造的」寫成「從其他資料再取得的時間不是你量到的，是你做出來的」，照使用者選的說法。
  4. 第 41–42 行：「分鐘無條件捨去，不要四捨五入，四捨五入會讓它偏大」寫成「只算滿的分鐘；四捨五入可能讓分鐘數偏大」，照使用者選的說法；加上「可能」，因為四捨五入只在秒數 ≥ 30 時才偏大。
  5. 第 43–44 行：guess 不在 STE 字典裡，寫成「不要用估計值代替這個值」；第 45 行的 merge/update 寫成 change。

**2026-10-12 做了什麼：第 2.2 步**（commit `1ac3459`）

做之前問了 4 個問題，決定如下：原檔第 21 行的粗體開頭改寫成粗體的 STE 句子；noise 保留，列為 technical word；untracked file 保留，列為 technical word，和 `git status` 的用語一致；commit 與紀錄和 2.1 一樣。

- **asd-ste**：Step 3 PASS，沒有 WARN，只有一條 INFO：noise 本來就是核准字，照使用者的選擇仍列為 technical word。
  草稿 52 行、40 句，用了 20 個 technical word，沒有一句保留原文的說法；PDF 依賴記為 2026-10-12；YAML checkpoint 在 `checkpoints/asd-ste/rules-scratch-rules/`。
- **中文版**：還沒有中文版，chinese 判定 FULL，52 行逐行整份翻譯；`check_parity.py` 0 failure、0 warning；keep-English 清單沒有加詞。
  untracked file 照原檔中文版譯成「未被追蹤的檔案」；app 照原檔中文版保留英文。
- **一句一行**：用 reformat-md 在副本上試轉，兩份都沒有改變。
- **審核時可以留意的地方**：行號是草稿的。
  1. 第 9 行：原檔的 throwaway files 寫成 scratch files，一樣東西只用一個名稱（STE 1.11）；第 17 行的 throwaway script 寫成 temporary script。
  2. 第 17–18 行：原檔第 9 行的四個例子寫成兩句；intermediate JSON 寫成「這次執行在兩個 step 之間使用的 JSON 檔」。
  3. 第 20、22–23 行：own 不在 STE 字典裡，「各有自己的路徑」寫成「各有不同的路徑」；「同一個想當然耳的名稱上相撞，後到的靜默覆蓋」寫成「可能用到同一個常見的名稱；第二次執行會取代第一次的檔案，而且不會告訴你」。
  4. 第 26 行：引號裡的 "mine" 與 "everything that matches" 改寫成「你可能以為它只會移除你的檔案，但它會移除所有符合萬用字元的檔案」，不再用引號。
  5. 第 31–33 行：「刻意留下：那是它走到哪裡的紀錄」寫成「可以把檔案留在 `temp\`，因為它們顯示這次執行做了多少工作」；「只有一個家的全部意義」寫成「把所有暫存檔放在同一個位置最重要的原因」。
  6. 第 35–40 行：粗體開頭寫成「workspace 的根目錄不是放暫存檔的正確位置」，照使用者選的做法；「這是它取代的習慣」寫成「在這些規則之前，執行通常把暫存檔放在那裡」。
  7. 第 43 行：build 當動詞不是核准字，「A built app」寫成「An app」；第 51 行：already 不是核准字，「git 本來就已忽略它」寫成「git 會忽略它」。
- **順帶發現**：兩個 workspace 裡已有 34 份中文版把 app 留成英文，keep-English 清單卻沒有這一條；照 chinese 的規則，留英文的詞要列進清單。
  這不在本 task 的範圍，沒有改清單。

**2026-10-12 做了什麼：第 2.3 步**（commit `85d6cd3`）

做之前分兩輪問了 6 個問題，決定如下：deterministically 寫出它的意思；drift 寫成「兩份會變得不一樣」；self-contained 保留，規則名 no forward-reference 加引號；`gen-skill`、`check-skill` 用 inline code；Purpose 定義裡的「損失」寫成「合併時會出的問題」；commit 與紀錄和 2.1、2.2 一樣。

- **asd-ste**：Step 3 PASS，沒有 WARN；草稿 48 行、37 句，用了 20 個 technical word；PDF 依賴記為 2026-10-12；YAML checkpoint 在 `checkpoints/asd-ste/rules-skill-writing/`。
  保留原文說法的有一處：第 32 行的 self-contained，照使用者的選擇保留，和 SKILL-tmp 的寫法一致；它不在 STE 字典裡，`check_ste.py` 把 self- 當字首、contained 當 contain 的變化，所以不報。
- **中文版**：還沒有中文版，chinese 判定 FULL，48 行逐行整份翻譯；`check_parity.py` 0 failure、0 warning；keep-English 清單沒有加詞。
- **一句一行**：用 reformat-md 在副本上試轉，兩份都沒有改變。
- **審核時可以留意的地方**：行號是草稿的。
  1. 第 9–12 行：原檔第 3–4 行寫成四句；`gen-skill`、`check-skill` 改用 inline code，照使用者的選擇。
  2. 第 16–20 行：原檔用被動句寫的規則改成祈使句，例如「修改 skill 之前，先讀它的 `README.md`」；節名照 DFD-ste 的做法加引號，例如 "When the Skill Is Changed"；load 當動詞不是核准字，「載入」寫成「讀」。
  3. 第 30、46 行：drift 寫成「兩份會變得不一樣」，照使用者的選擇。
  4. 第 32–33 行：粗體保留 self-contained，規則名加引號；「絕不依賴後面的 step」寫成「沒有後面那些 step 也必須能正確運作」。
  5. 第 36 行：deterministically 寫成「同樣的輸入總是得到同樣的輸出」，照使用者的選擇。
  6. 第 39 行：「只回答上一條規則一次」寫成「只說明一次它怎麼遵守上一條規則」。
  7. 第 43–44 行：Purpose 寫成「說明為什麼要有這個 step 的一句話，也就是把它與相鄰的 step 合在一起時會出的問題」，照使用者的選擇。
- **順帶發現**：原檔的中文版用了 keep-English 清單標記的譯法：skill-writing-tw 把 glossary 譯成「術語表」、script 譯成「腳本」，`check_parity.py` 有 2 個 WARN；scratch-rules-tw 也把 script 譯成「腳本」，有 1 個 WARN。
  這兩份草稿的中文版都照清單留了英文；Task 32 用草稿取代原檔時，這些 WARN 會一起消失。

**2026-10-12 做了什麼：第 2.4 步**（commit `fcc9ff4`）

做之前分兩輪問了 6 個問題，決定如下：「that is noise」寫出意思；ripgrep、ugrep、grep 改用 inline code，macOS 列為 technical word；harness 保留，列為 technical word；引號裡的口號改寫成 STE；「Exception —」改成「But if」；commit 與紀錄和前幾份一樣。

- **asd-ste**：Step 3 跑了 3 次。
  第 1 次有 1 個 FAIL（一句 26 字）與 4 個 WARN（size、way、filters、paths）：長句拆成兩句，size 與 way 改寫掉，filter 與 path 列為 technical word（字典本身把 filter 標成 TN）。
  第 2、3 次 PASS，沒有 WARN，只有一條 INFO：hit 只核准當動詞，這裡當名詞用，所以仍列為 technical word。
  草稿 97 行，用了 35 個 technical word，沒有一句保留原文的說法；PDF 依賴記為 2026-10-12；YAML checkpoint 在 `checkpoints/asd-ste/rules-tools/`。
- **中文版**：還沒有中文版，chinese 判定 FULL，97 行逐行整份翻譯；`check_parity.py` 0 failure、0 warning；keep-English 清單沒有加詞。
- **一句一行**：原檔一行不只一句的有 12 行，草稿已是一句一行；用 reformat-md 在副本上試轉，兩份都沒有改變。
- **審核時可以留意的地方**：行號是草稿的。
  1. 第 9–12 行：few 不是核准字，「fewer tokens」寫成「a smaller number of tokens」；count 只核准當動詞，「Every byte count below is measured」寫成「We measured all the numbers of bytes that follow」。
  2. 第 16–23 行：search 當動詞不是核准字，寫成「use `rg` for a search」；「The reason is not output size」寫成「The cause is not the number of bytes in the output」；「省下的是寫錯的指令不必重跑」寫成「你不會把指令寫錯，然後再執行一次」。
  3. 第 24–25 行：`ripgrep`、`ugrep`、GNU `grep` 改用 inline code，`ugrep` 仍是粗體，照使用者的選擇；「flag semantics are not identical」寫成「旗標不一定給出同樣的結果」。
  4. 第 31–36、66–69 行：兩個表格的標題列不變，其他儲存格改寫成 STE，例如「What does it look like in context?」寫成「Which lines are around it?」；中文版的標題列照 chinese 的規則留英文。
  5. 第 38、46–49 行：「is **gone**」寫成「has **no** hits」；「range versus whole file」寫成「a range with the full file」。
  6. 第 54、55、76 行：「that is noise」、「Exception —」與引號裡的口號，照使用者選的寫法。
  7. 第 77–79 行：「用 `sed -n '1,$p'` 規避整檔讀取的禁令，token 一樣多還多一層混淆」寫成三句：token 一樣多、指令看不清楚它讀了整份檔案、這樣做沒有遵守規則。
  8. 第 97 行：「the most-overlooked token sink of all」寫成「the cause of a high number of tokens that agents most frequently do not see」。
  9. 中文版：alias 照「只有一種通用譯法就翻譯」的規則譯成「別名」，原檔中文版留英文；第 85 行引號裡別的 skill 的指示，草稿照 House Rule 10 照抄英文，中文版照原檔中文版翻譯。
- **順帶發現**：原檔中文版 tools-tw 把 glossary 譯成「術語表」、step 譯成「步驟」，`check_parity.py` 有 2 個 WARN；草稿的中文版照清單留了英文。
  中文版裡 harness 和 app 一樣留英文，keep-English 清單也沒有這一條；沒有改清單。

**2026-10-12 做了什麼：第 2.5 步**（commit `7f3614d`）

做之前分兩輪問了 7 個問題，決定如下：「fails **silently**」寫成「沒有錯誤訊息」，message 列為 technical word；wrapper 與 orchestration 保留，列為 technical word；反引號那個條列留在同一個條列，合併成 6 句；escaping、interpolation、single-quoted here-string、double-quoted string 保留，列為 technical word；commit 與紀錄和前幾份一樣。
使用者另外決定把 current 與 now 列為核准字，並新建一份 customization 檔來放它們；這件事開成 [[Task 35]]，做完才回來做本步。

- **asd-ste**：Step 1 與 Step 3 都加上 `--custom`；Step 3 第一次就 PASS，沒有 WARN，只有一條 INFO：current 用在第 35、41、52 行。
  這是第一份用到自訂字的草稿，檔頭引用區除了 PDF，也宣告 `[[ste-custom]]`，兩個指紋都記為 2026-10-12（PDF `d1f4ea9e7cd6`，ste-custom `ca72f0ff1a59`）。
  草稿 88 行、49 句，用了 47 個 technical word，沒有一句保留原文的說法；YAML checkpoint 在 `checkpoints/asd-ste/rules-report-md-rules/`。
  Step 2 的群組存了兩次：第一次讀錯了行，存成空的 technical word 清單，隨即重存，`note` 記下原因。
- **中文版**：還沒有中文版，chinese 判定 FULL，88 行逐行整份翻譯；`check_parity.py` 0 failure、0 warning；keep-English 清單沒有加詞。
  record 在這份裡是一般動詞，譯成「記錄」；wrapper 與 orchestration 照原檔中文版譯成「外層包裝」「編排」。
- **一句一行**：用 reformat-md 在副本上試轉，兩份都沒有改變。
- **審核時可以留意的地方**：行號是草稿的。
  1. 第 3–4 行：檔頭引用區多了 `[[ste-custom]]` 那一行；清單一改，`depends_on.py check` 會把這份標成 CHANGED。
  2. 第 11–15 行：原檔第 4 行拆成三句，「never hardcode」寫成「Do not hard-code」；下一層的條列拆成兩句，「the header fields below」寫成「the fields of its header」，因為 below 只核准當介系詞。
  3. 第 36–39 行：「從時鐘取得——兩種指令——絕不用估計或記憶中的值」拆成四句，「remembered value」寫成「a previous value」。
  4. 第 44–46 行：「this normalized form」寫成「this standard text」；「剛好觸發這次執行的外層包裝、編排或 agent 指示文字」寫成「它周圍的文字，即使那段文字啟動了這次執行」，再用一句列出三個例子。
  5. 第 63 行：「讓報告文字經過 shell 指令，正是它被毀損的原因」寫成「損壞報告文字的原因，是文字所經過的 shell 指令」。
  6. 第 66–70 行：反引號那個條列合併成 6 句，「fails **silently**」寫成「You get **no error message**」，照使用者選的寫法。
  7. 第 85 行：「the single quotes exist to prevent」寫成「The single-quoted here-string is there to prevent this escaping」：複數的 single quotes 對不上 technical word 清單，而兩者指的是同一個東西。
  8. 第 87–88 行：「讓一次成功的寫入看起來像失敗」寫成「你可能以為 shell 沒有寫入這個檔案，雖然 shell 已經正確地寫入了它」。

**2026-10-12 做了什麼：第 2.6 步**（commit `15aae9d`）

做之前分三輪問了 8 個問題，決定如下：第 3–6 條轉換的粗體標籤照抄，第 7–10 條的粗體句子改寫成 STE；escape 保留，當 technical verb 列進 technical word；第 9 條的「Known limits」一段改成直式清單；no-op 與 idempotent-only mode 保留，列為 technical word；commit 與紀錄和前幾份一樣。
silently 原本建議照 2.5 寫成「and no message tells you」，並把 message 列為 technical word；使用者決定改把 message 列為 customization，也就是加進 ste-custom.md 當核准字。
2.5 的 report-md-rules-ste 因此要從 Technical words 行拿掉 message，重查並重記指紋；這件事記在本步，前綴 task 31。

- **ste-custom.md 加 message**（commit `3063001`）：表格與中文版各加一列 message（n），Why 欄寫明是使用者在本步核准、Issue 9 沒有收錄這個詞，而「and no message tells you」說出了 silently 的意思。
  清單一改，`depends_on.py check` 就把 report-md-rules-ste 的 `[[ste-custom]]` 標成 CHANGED，和 [[Task 35]] 設計的一樣。
  同一個 commit 裡，report-md-rules-ste 與中文版的 Technical words 行拿掉 message，`run step 3` 重查 PASS，兩份檔頭的 ste-custom 指紋都重記為 `7f4a6b87895d`（2.5 記的是 `ca72f0ff1a59`）。
- **asd-ste**：Step 1 與 Step 3 都用 `--custom`；Step 3 跑了 3 次。
  第 1 次 PASS，有 5 種 WARN：op ×3、dynamic、preformatted、quotation、trees。
  後 4 種都是複數對不上 Technical words 行裡的片語：第 17 行改成單數的「a directory tree, an ASCII diagram or a different preformatted block」，第 107 行改成「the extractor for each dynamic token」，第 33 行的 quotation marks 改成 quotes，quotation mark 也從 Technical words 行拿掉。
  第 2、3 次 PASS，只留下 op ×3：no-op 照使用者的選擇保留，`check_ste.py` 把有連字號的詞拆開，所以報 op。
  兩條 INFO：paste 只核准當名詞，草稿第 58 行當動詞用，所以仍列為 technical word；自訂字用了 now（第 23 行）與 message（第 70、89 行），檔頭引用區因此也宣告 `[[ste-custom]]`。
  草稿 153 行、129 句，用了 102 個 technical word；PDF 與 ste-custom 的指紋都記為 2026-10-12（PDF `d1f4ea9e7cd6`，ste-custom `7f4a6b87895d`）；YAML checkpoint 在 `checkpoints/asd-ste/rules-md-style/`。
  「Transforms applied by reformat_md.py」一節的 10 個編號一條對一條保留，reformat-md 的 Step 0 照樣能逐條對照。
- **中文版**：還沒有中文版，chinese 判定 FULL，153 行逐行整份翻譯；`check_parity.py` 0 failure、0 warning；keep-English 清單沒有加詞。
  草稿寫 repository，中文版照 keep-English 清單留英文；原檔與原檔中文版寫的是 repo。
  fenced code block 和清單上的 fenced block 是同一個東西，照原檔中文版留英文。
- **一句一行**：用 reformat-md 在副本上試轉，兩份都沒有改變。
- **審核時可以留意的地方**：行號是草稿的。
  1. 第 3–4、23、70、89 行：檔頭引用區多了 `[[ste-custom]]` 那一行，因為第 23 行用了 now、第 70 與 89 行用了 message；silently 寫成「and no message tells you」，照使用者的決定。
  2. 第 10–27 行：原檔混用 header 與 heading，草稿全文一律寫 heading（STE 1.11：一樣東西只用一個名稱），只有照抄的 **Headers** 標籤例外；repo 寫成 repository。
     原檔括號裡的理由，與「so characters like `#` and `_` render literally」各寫成第二句；convert 不是核准字，「convert it」寫成「Change it to Obsidian math」。
  3. 第 28–41 行：原檔第 13–19 行的一個條列有 7 句，改寫後超過一段 6 句的上限，所以寫成兩句的條列，下面接 6 個子項目：句子在哪裡結束、在哪裡不結束、接成一行、維持原樣、清單項目、中文版。
     end 當動詞不是核准字，「ends」寫成 stop，或寫成名詞的 end。
  4. 第 45–59 行：「operationalizes the rules above」寫成「applies the rules before this section」；skill 名稱 `reformat-md` 照前幾份的做法改用 inline code。
     轉換 2（原檔第 26–30 行）改寫後有 11 句，拆成兩段：第 48–53 行說怎麼判斷、什麼時候進入 idempotent-only mode，第 55–59 行說 `--mode` 與 `--twin`。
  5. 第 60、62、64、72、79、97、109、140 行：第 3–6 條的粗體標籤照抄，第 7–10 條的粗體句子改寫成 STE、仍然加粗，照使用者的選擇；例如「**Inline-codes identifiers**」寫成「**Puts identifiers in inline code**」。
     第 66 行的粗體小標「**`\#` is conditional.**」也寫成 STE 的句子「**A `\#` changes only in some conditions.**」；escape、unescape 照使用者的選擇當 technical verb 保留。
  6. 第 79–96 行：原檔第 44 行一行有粗體標題和 6 句，寫成第 80–82 行與第 84–86 行兩段。
     第 92–94 行「so it is idempotent」寫成「Thus, a second run makes no change」，照使用者的選擇，idempotent 單獨當形容詞，不列 technical word；「promoted past `#v1`」寫成「at a version after `#v1`」。
     第 96 行「as in this file」寫成「as in md-style.md」：草稿本身不是 md-style.md，取代原檔之後兩者才是同一份。
  7. 第 103–108 行：「would be coded wherever it stands alone」寫成「the transform can put the name in inline code at each location where the name is a word」；「on a later pass」寫成「in a subsequent run」。
  8. 第 112–114 行：「the order matters — a whole-line citation must be matched before the whitespace pattern, which would otherwise …」拆成三句；「strand `1,`」寫成「`1,` stays in the text」。
  9. 第 133–138 行：「Known limits」一段改成直式清單，三條各一項，照使用者的選擇。
  10. 第 53、131、153 行：no-op 照使用者的選擇保留，Step 3 因此留下 op ×3 的 WARN。
- **順帶發現**：原檔第 44 行說「Two decisions worth knowing」，下面卻列了四條（第 45–49 行），只有前兩條是「決定」；草稿照原文寫「These two decisions are important」（第 86 行），留給 Task 32 審核時決定要不要改。
  `check_ste.py` 這次碰到兩個限制：複數對不上 Technical words 行裡的片語（directory trees、dynamic tokens、quotation marks），以及把有連字號的 technical word 拆開（no-op 報成 op）；2.5 也碰過前一個（single quotes）。
  沒有改 asd-ste，留給 [[Task 32]] 改 asd-ste 時一併考慮。

**2026-10-13 做了什麼：第 3 步**（commit `b37ba4f`、`dd12730`）

做之前分三輪問了 12 個問題，決定如下：表格的標題列與 Term、Replaces、Flagged 三欄照抄，因為 `scan_md.py`、`check_parity.py`、`check_rsdc.py` 都讀這張表；Term 欄的詞全部列進 Technical words；Why it stays English 欄改寫成完整的 STE 句子；當動詞用的 names 寫成「It is the name of …」；common、in use、settled 寫成「twins use … renderings」、standard 與「occurs too frequently to flag」；rendering 與 flag 列為 technical word；app 與 harness 不加；commit 與紀錄和前幾份一樣。
使用者另外決定把 translate、warning、translator、reader、state、outcome、role 加進 ste-custom.md 當核准字。
flag 原本也要加，但它在 DFD-ste、RSDC-Standard-ste 是 DFD 的旗形圖形，在 tools-ste 是指令列旗標，都是另一種意思的名詞；`check_ste.py` 分不出意思，所以改列 technical word。
加字牽動已寫好的草稿：用到 reader 與 role 的 DFD-ste、RSDC-Standard-ste 照 House Rule 11 跟上，行號全部改成新的；這些改動和加字是同一個 commit，前綴 task 31。

- **ste-custom.md 加 7 個字**（commit `b37ba4f`）：表格與中文版各加 7 列，Why 欄寫明是使用者在本步核准，以及 Issue 9 為什麼不夠。
  清單一改，指紋從 `7f4a6b87895d` 變成 `36190b0228ae`；宣告或用到這些字的 4 份草稿都用 `run step 3` 重查 PASS，兩個指紋都重記為 2026-10-13。
  - DFD-ste 與 RSDC-Standard-ste：reader 與 role 的意思和核准的一樣，照 House Rule 11 從 Technical words 行拿掉，檔頭加上 `[[ste-custom]]` 一行，第 4 行以後因此都往後移一行。
    第 1 步「刻意與原檔不同的 4 處」的行號、表格裡的行數，以及兩個 checkpoint 的 `intentional_differences`，都改成新行號。
  - report-md-rules-ste 與 md-style-ste：沒有用到新加的字，只有 `[[ste-custom]]` 的指紋改變。
  - 這 4 份的中文版由 chinese 判定 INCREMENTAL，只改檔頭與技術用字行；`check_parity.py` 0 failure，`diff_md.py --verify` 通過。
  - 其餘 3 份草稿與 tools-ste 沒有用到這些字，不受影響。
- **asd-ste**：Step 1 與 Step 3 都用 `--custom`；Step 2 寫草稿時試跑了 3 次 `check_ste.py`，修掉一句 27 個字的長句、at least、define、save、separate、ways、phase，並把 list、technical term、operating system 等字列為 technical word。
  複數的「technical terms」又對不上 Technical words 行裡的片語，改回原檔的單數。
  Step 3 跑了 2 次，都 PASS，只留下 op ×1（第 87 行）：no-op 是清單上的詞，它的 Term 欄照抄。
  草稿 129 行、32 句，用了 126 個 technical word，其中 71 個來自 Term 欄：outcome 是自訂字，照 House Rule 11 不列。
  7 個新加的自訂字都用到了，檔頭引用區因此宣告 `[[ste-custom]]`；PDF 與 ste-custom 的指紋都記為 2026-10-13（PDF `d1f4ea9e7cd6`，ste-custom `36190b0228ae`）；YAML checkpoint 在 `checkpoints/asd-ste/references-tw-keep-english/`。
  `scan_md.py` 與 `check_rsdc.py` 從草稿讀到的 72 個詞與 91 個 Flagged 譯法，和從原檔讀到的完全相同：Task 32 用草稿取代原檔之後，這份清單照樣能用。
- **中文版**：還沒有中文版，chinese 判定 FULL，129 行逐行整份翻譯；keep-English 清單沒有加詞。
  `check_parity.py` 0 failure、91 個 warning，全在表格列，是清單自己列出的譯法，和原檔中文版的 91 個是同一組，照 chinese 的規則留著，和 [[Task 34]] 一樣。
  三份檔案的 Term、Replaces、Flagged 三欄一字不差；Why 欄的說法盡量沿用原檔中文版，例如「沒有固定的中文譯法」「不列入 Flagged」。
- **一句一行**：用 reformat-md 在副本上試轉，兩份都沒有改變。
- **審核時可以留意的地方**：行號是草稿的。
  1. 第 3–4、8 行：檔頭宣告 `[[ste-custom]]`；Technical words 行有 126 個詞，71 個是 Term 欄的詞，outcome 是自訂字所以不列。
  2. 第 10–14 行：原檔第 3 行拆成三句，「spelled exactly as the English file spells them」寫成「The spelling of each term in a twin is the same as in the English file」；once 不是核准字，寫成 one time。
  3. 第 16–19 行：照 House Rule 7，Version 行寫成「The version of tw-keep-english.md is 261012.」；沒有程式讀這一行，所以不必像 RSDC-Standard-ste 那樣只留數字。
     原檔第 7 行拆成三句。
  4. 第 23 行：「**either** of these holds」寫成「when **one** of these two conditions is correct, or when the two are correct」，因為 at least 不是核准的片語，而 either 只要有一個條件成立。
  5. 第 25–30 行：兩條規則照使用者的選擇寫成「Twins use more than one Chinese rendering for it」與「It is the name of a type, a state, an outcome or a role in the system」；兩句超過 25 字的長句各拆成兩句。
  6. 第 32–35 行：「Everything else is translated」寫成祈使句「Translate all the other words」；「whether or not it is listed here」寫成「This is correct when the term is on this list, and also when it is not on it」。
  7. 第 42–45 行：「may search for … and warn about」寫成「can examine … and show a warning」；「too common to search for without false alarms」寫成「occur too frequently: if a tool examines the prose for them, it shows too many incorrect warnings」。
  8. 第 49–120 行：72 列的 Why 欄都寫成完整的句子，分號後面的部分拆成第二句，例如 baseline 那一列。
     Why 欄裡的 skill 與工具名稱照前幾份的做法改用 inline code（`reformat-md`、`git`）。
     另外改寫的有：diff 的「a comparison」寫成「the output that `git` gives when it compares two versions of a file」；pipe 的「separates the cells」寫成「the character between the cells」；stage 的「準備階段 a phase」寫成「準備階段 is a period」；identifier 的「names the name」寫成「It is the name of the name」，中文版譯成「總稱」。
  9. 第 124–129 行：原檔第 107 行 34 字的長句拆成四句；「the rule above」寫成「the rule that the section "The rule" gives」。
- **順帶發現**：
  1. RSDC-Standard-ste-tw 第 186 行與原檔中文版 RSDC-Standard-tw 第 72 行，都把 metadata 譯成「元數據」，`check_parity.py` 各有 1 個 WARN。
     metadata 是 [[Task 34]] 才加進清單的詞，這兩份寫成時還沒有這一條；這次是 INCREMENTAL，change set 以外的行要一字不動，所以沒有改，留給 Task 32。
  2. RSDC-Standard 的 checkpoint 原本存的被動句行號（56、235、318），在 [[Task 33]] 拿掉 4 行之後就過期了；這次重存成目前的 53、232、315。
  3. `check_ste.py` 的複數片語限制這次又碰到一次（technical terms），和 2.6 記的一樣。

**2026-10-13 做了什麼：第 4 步**（commit `ffd16e4`、`cbf93d6`、`692b3ef`）

做之前分兩輪問了 7 個問題，決定如下：範本裡會被 gen-skill 抄進每個新 skill 的共用句子，一樣改寫成 STE；範本中的 this file、this skill、this `SKILL.md` 指的是照範本寫出來的檔案，保留不改，不套 House Rule 7；save 保留，當 technical verb；depend 加進 ste-custom.md；粗體開頭改寫成 STE、保留粗體；先 SKILL-tmp、後 README-tmp，各自一個 commit。
已寫好的 skill 不受影響：Task 32 取代範本之後，由它的「範本的後續」讓各 skill 的共用句子跟上。

- **ste-custom.md 加 depend**（commit `ffd16e4`）：表格與中文版各加一列 depend（v，詞形 depends、depended、depending）。
  清單一改，指紋從 `36190b0228ae` 變成 `2c858ad55ffc`；宣告 `[[ste-custom]]` 的 5 份草稿（DFD、RSDC-Standard、tw-keep-english、report-md-rules、md-style）都沒有用到 depend，`run step 3` 重查 PASS 並重記，中文版只改檔頭那一行，判定 INCREMENTAL，`diff_md.py --verify` 通過。
  另外 4 份草稿沒有宣告，也沒有用到 depend，不受影響。
  ste-custom.md 的中文版是先改、才跑 `diff_md.py`，所以它判定 FULL；`--verify` 以 `b37ba4f` 為基準，確認其餘 28 行一字未動。
- **SKILL-tmp**（commit `cbf93d6`）：
  - asd-ste：Step 2 寫草稿時試跑了 4 次 `check_ste.py`；Step 3 跑了 2 次，都 PASS，沒有 WARN。
    草稿 202 行、120 句，用了 62 個 technical word；自訂字用了 current 與 message，檔頭引用區因此宣告 `[[ste-custom]]`。
    檔頭引用區與註記放在 frontmatter 之後、`# TERMINOLOGY` 之前，和 asd-ste 自己的 SKILL.md 一樣；兩個指紋都記為 2026-10-13；YAML checkpoint 在 `checkpoints/asd-ste/templates-SKILL-tmp/`。
  - 中文版：chinese 判定 FULL；有 frontmatter，所以逐節對應，frontmatter 下面加兩行 pairing line；`check_parity.py` 0 failure、0 warning。
    script 與 canonical skill invocation 照 keep-English 清單留英文，原檔中文版譯成「腳本」與「標準化的 skill 叫用方式」；scratch file 照 2.2 譯成「暫存檔」。
- **README-tmp**（commit `692b3ef`）：
  - asd-ste：Step 2 試跑了 3 次；Step 3 跑了 2 次，都 PASS，沒有 WARN。
    草稿 196 行、54 句，用了 38 個 technical word；自訂字用了 depend、reader、role。
    檔頭引用區是原檔的 9 行 `{COMMON_PATH}` 連結，後面接上 PDF 與 `[[ste-custom]]` 兩行；`depends_on.py record --target` 只寫這兩行。
    4 個 fenced block 由 script 從原檔照抄；YAML checkpoint 在 `checkpoints/asd-ste/templates-README-tmp/`。
  - 中文版：chinese 判定 FULL，196 行逐行翻譯，fenced block 由 script 從草稿照抄；`check_parity.py` 0 failure、0 warning。
    中文版也是先寫、才跑 Step 1 的兩支 script；它是新檔，沒有基準，所以判定一樣是 FULL。
- **一句一行**：兩組都用 reformat-md 在副本上試轉，四份都沒有改變。
- **審核時可以留意的地方**：行號是草稿的。
  1. SKILL-tmp-ste 第 6–11 行：檔頭引用區與註記放在 frontmatter 之後；取代範本時要決定它們怎麼處理，見順帶發現 1。
  2. SKILL-tmp-ste 第 15–17 行：「a term defined but never used is drift waiting to happen」寫成「the definition of the term can become incorrect when the skill changes」。
  3. SKILL-tmp-ste 第 49–51 行：「Must run workflow step by step」寫成「Do the workflow one step at a time」；「**Honour a `run step N` selector**」寫成「**Obey a `run step N` selector**」，honour 是英式拼法，也不在字典裡。
  4. SKILL-tmp-ste 第 55–63 行：「**Every JSON … has exactly one writer step.**」那一條改寫後有 10 句，超過一段 6 句的上限，所以分成兩個條列，第 61–63 行另成一條，說明原因。
     「without a word」寫成「and no message tells you」，和 md-style-ste 的做法一樣。
  5. SKILL-tmp-ste 第 64–74 行：粗體開頭寫成 STE 句子「**Before the skill stops, show the paths of the MD report and of the YAML checkpoint.**」；clickable 寫成「that open with a click」，因為 click 只核准當名詞。
  6. SKILL-tmp-ste 第 103 行：「Run `.venv` first」寫成「Activate `.venv` first」：run 當動詞不是核准字，activate 說出了這一行要做的事。
  7. SKILL-tmp-ste 第 114、144 行：「ask the user」寫成「tell the user to supply it」，因為 ask 不是核准字。
  8. SKILL-tmp-ste 第 116–132 行：ADO_PAT 那兩條的長句拆開；PAT、User scope、registry、session、terminal、credential、bearer token 列為 technical word；「**STOP the skill immediately**」照原文保留。
  9. SKILL-tmp-ste 第 146–148 行等：save 照使用者的選擇保留為 technical verb，例如「Save `step_0` of the YAML checkpoint, with the parsed inputs.」。
  10. README-tmp-ste 第 19–26、35–44 行：兩段改寫後超過 6 句，各分成兩段。
  11. README-tmp-ste 第 19、136、177、179 行：depend 照使用者的決定成為自訂字，句子照原文用 depends on。
  12. README-tmp-ste 第 81–92 行：圖例的寫法和 DFD-ste 一致，例如「moves data」「goes into a record」「only controls how a step operates」。
  13. README-tmp-ste 第 131 行：「No run reads SKILL-tw.md, this file or README-tw.md.」照原文保留；中文版照原檔中文版的寫法，站在中文版自己的角度寫成「SKILL-tw.md、README.md 或本檔」。
  14. README-tmp-ste 第 170–172 行：「no failure」寫成「the two checks show no `[FAIL]` line」，「every check passes」寫成「each check shows no problem」，因為 pass 當動詞不是核准字。
  15. 兩份：this file、this skill、this `SKILL.md` 照使用者的選擇保留；fenced block 裡的文字照 House Rule 1 照抄，所以不是 STE。
- **順帶發現**：
  1. 兩份範本草稿的檔頭混了兩種依賴：README-tmp 原本的 9 行，是照範本寫出的 README 的依賴；草稿加上的 PDF 與 `[[ste-custom]]` 兩行與檔頭註記，SKILL-tmp-ste 的也一樣，則是範本這份 STE 檔自己的依賴。
     Task 32 取代範本之後，gen-skill 會把這些行一起抄進每個新 skill；要決定取代時拿掉它們，或讓 gen-skill 不抄，可以列入 [[Task 32]] 的「範本的後續」。
  2. `check_ste.py` 又碰到兩個限制：
     - 判斷 technical word 有沒有用到時，只認 -s 與 -es 的形式，不認 -ed；只用到 parsed 的檔案，會被報成「technical words listed but never used」。
       這次改寫成 parses 避開。
     - 它移除含空格的 technical word 片語時，順序不固定；重疊的片語，例如 data file 與 raw data 遇上 raw data file，會讓結果隨每次執行而不同。
       這次改寫成不重疊的說法。
  3. 原檔中文版 SKILL-tmp-tw 把 script 譯成「腳本」、canonical skill invocation 譯成「標準化的 skill 叫用方式」，都是 keep-English 清單標記的譯法；草稿的中文版照清單留了英文，取代之後這些會一起消失。

## 3. 要做的

**DFD 與 RSDC-Standard 的草稿要先改的（2026-10-12）**

由 asd-ste 修改這兩份草稿、跑 `check_ste.py`，再由 chinese skill 更新草稿的中文版：

- **版本號是「規則的版本」**：評估過 261010 這類版本號存在的理由之後決定保留它，但只有規則改變才升版；措辭、格式、翻譯與 STE 改寫都不升版。
  這次的 STE 改寫因此維持 261010，兩份 RSDC 範本記的版本也不必改。
- **Version 行**：RSDC-Standard 的草稿寫成「**Version**: The version of RSDC-Standard.md is 261010.」，`check_rsdc.py --standard` 讀不到版本號，要改成「**Version**: 261010.」。
- **版本規則句**：標準說「改版時只更新版本行並加一節」，DFD 說「本文件的任何改動都是標準的新版本」；兩句都改成只有規則改變才升版，其他修改保留版本，並在該版的一節註明。
- **Changes in This Version**：在 261010 一節最前面加一條，說明文字已改寫成 STE（涵蓋 DFD），規則沒有改變。

**要做的**

1. ✅ DFD 與 RSDC-Standard：請 asd-ste 照上一段修改兩份草稿，chinese skill 更新它們的中文版（2026-10-12 完成，見下）。
2. ✅ rules 的 6 份：逐份交給 asd-ste 產生草稿，再由 chinese skill 寫草稿的中文版（2026-10-12 完成）。
   依行數由短到長，一份一步；每一步完成時打 ✅ 並附 commit，6 份都完成再在第 2 步打 ✅。
   - **2.1 ✅ report-yaml-rules**（17 行，`2828bd5`）：中文版已由 Task 34 寫出（2026-10-12）；草稿與草稿中文版 2026-10-12 完成，見下。
     asd-ste 的 README 與中文版記錄它的指紋（2 份）；asd-ste 的 `save_step.py` 照它寫 YAML checkpoint。
   - **2.2 ✅ scratch-rules**（27 行，`1ac3459`）：有中文版；草稿與草稿中文版 2026-10-12 完成，見下。
     check-skill 的 README 與中文版記錄它的指紋（2 份）。
   - **2.3 ✅ skill-writing**（28 行，`85d6cd3`）：有中文版；草稿與草稿中文版 2026-10-12 完成，見下。
     asd-ste、check-skill、gen-skill 的 README 與中文版記錄它的指紋（6 份）；`skills/CLAUDE.md` 要求改 skill 之前先讀它。
   - **2.4 ✅ tools**（54 行，`fcc9ff4`）：有中文版；草稿與草稿中文版 2026-10-12 完成，見下。
     沒有文件記錄它的指紋；是 [[Task 19]] 交來的那一組，原檔還不是一句一行，草稿寫成 STE 時就一句一行。
   - **2.5 ✅ report-md-rules**（61 行，`7f3614d`）：中文版已由 Task 34 寫出（2026-10-12）；草稿與草稿中文版 2026-10-12 完成，見下。
     沒有文件記錄它的指紋；InvestForge 的 report-cash-level 與 report-gross-margin 的 `gen_report.py` 照它寫報告的檔頭。
   - **2.6 ✅ md-style**（76 行，`15aae9d`）：中文版已由 Task 34 寫出（2026-10-12）；草稿與草稿中文版 2026-10-12 完成，見下。
     asd-ste、check-skill、gen-skill 的 README 與中文版記錄它的指紋（6 份）。
     reformat-md 的 Step 0 會讀它，逐條對照「Transforms applied by reformat_md.py」一節的 10 個編號與腳本的轉換；草稿要保留這 10 個編號，一條對一條。
3. ✅ references 的 tw-keep-english（108 行，`dd12730`）：同上；中文版已由 Task 34 寫出（2026-10-12）；草稿與草稿中文版 2026-10-13 完成，見下。
   Task 34 為它加了 26 個詞，原檔從 82 行變成 108 行。
4. ✅ templates 的 README-tmp 與 SKILL-tmp：同上；草稿與草稿中文版 2026-10-13 完成（SKILL-tmp `cbf93d6`、README-tmp `692b3ef`），見下。

## 4. 驗證

**驗證**

- 每一份草稿：`check_ste.py` 沒有 FAIL，草稿與中文版的 `check_parity.py` 0 failure，一句一行。
- 2026-10-13 第 4 步完成之後，11 份全部重驗一次：`check_ste.py` 都 PASS；`check_parity.py` 都 0 failure，warning 只有 RSDC-Standard 的「元數據」與 tw-keep-english 表格裡的譯法；用 reformat-md 在副本上試轉，22 份都沒有改變；`depends_on.py check` 都 UNCHANGED，README-tmp 除外，它的 `{COMMON_PATH}` 連結要 `--config` 才讀得到，原檔也一樣。

## 5. 與其他 task 的關係

**與其他 task 的關係**

- [[Task 32]]：依賴本 task——它逐份審核這裡產生的草稿，通過後由 asd-ste 取代原檔。
- [[Task 33]]：本 task 依賴它，2026-10-12 已完成——原檔與兩份現有的草稿都已沒有指向中文版的那一句，其餘的草稿產生時也不必寫這一句。
- [[Task 34]]：本 task 依賴它——原本沒有中文版的 4 份，由它先寫出原檔的中文版；2026-10-12 已完成。
- [[Task 23]]：建立 asd-ste，本 task 用它產生草稿。
- [[Task 19]]：`RSDC-Standard-ste` 與 `tools` 兩組改由本 task 處理。
- [[Task 25]]：會改 `check_ste.py` 對 `___X___` 的處理；範本用的是 `{X}`，不受影響。
- [[Task 26]]：決定 ASD-STE100 的 PDF 是否留在 git；草稿的檔頭連到它，PDF 若只移出 git、仍留在磁碟上，連結照樣找得到。

## 6. 知識

—

## 7. 日誌

### 2026-10-19

- 表格裡 README-tmp（[[Task 32.10]]）的草稿已取代原檔，指向草稿的連結改成行內程式碼。
- 照 keep-English list，1 處譯成中文的 pairing line 改成英文，意思沒有改（[[Task 68]]）。
- 表格裡 SKILL-tmp（[[Task 32.11]]）的草稿已取代原檔，指向草稿的連結改成行內程式碼。

### 2026-10-18

- 表格裡 tw-keep-english（[[Task 32.3]]）、report-md-rules（[[Task 32.5]]）、report-yaml-rules（[[Task 32.6]]）、scratch-rules（[[Task 32.7]]）、skill-writing（[[Task 32.8]]）與 tools（[[Task 32.9]]）的草稿已取代原檔，指向草稿的連結改成行內程式碼。
- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-14

- RSDC-Standard 與 md-style 的 STE 草稿與草稿中文版取代了原檔。

### 2026-10-13

- DFD 的 STE 草稿與草稿中文版取代了原檔。
- 完成第 3 步（tw-keep-english）與第 4 步（SKILL-tmp、README-tmp）。
- 11 份全部重驗一次。

### 2026-10-12

- 提出：列出 `.github/common` 底下的 md 檔，決定逐份產生 STE 草稿與草稿中文版。
- 完成第 1 步（DFD 與 RSDC-Standard 的草稿改好）與第 2 步的 6 份 rules。
