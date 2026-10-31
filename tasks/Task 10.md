# Task 10 - 讓 chinese skill 承接 RSDC twin 的專用規則

**Status**：完成——2026-10-11 五點都已完成：第 1、2、3 點，第 4 點（成對檢查缺的項目搬進 `check_parity.py`），第 5 點（Task 12 先做，已完成）。
**Raised**：2026-10-10，gen-rsdc-skill 拿掉處理中文的 step、把 RSDC twin 交給 chinese skill 時提出。
**Depends on**：—

## 1. 背景

問題：gen-rsdc-skill 原本由兩個 step 寫出並檢查 RSDC twin（`<system name>-RSDC-tw.md`）：Step 7 - Write the RSDC Twin 與 Step 8 - Check the RSDC Pair（原文在 commit `3f18282` 的 `.github/common/skills/gen-rsdc-skill/SKILL.md`）。
2026-10-10 這兩個 step 拿掉了，RSDC twin 改由 [chinese skill](../.github/common/skills/chinese/SKILL.md) 撰寫。
RSDC 沒有 frontmatter，chinese skill 會逐行翻譯它，逐行對齊本來就做得到；但 RSDC twin 還有幾條專有的規則，它不知道。

**重新整理（2026-10-10）**：寫下這一項之後又有多次更新，以下是整理後的現況。
先前的三個選項與「暫時傾向選項 1」由這份整理取代——選項 1 說「gen-rsdc-skill 與 imp-app 寫的 RSDC 都能用」，但 imp-app 的 RSDC 已經移到 gen-rsdc-app。

**範圍變了：Task 14 在等這一項**。
Task 14（gen-rsdc-app）決定 twin 最終交給 chinese，但要先做 Task 10；在那之前，gen-rsdc-app 暫時同一次執行寫兩份。
所以這一項擋住的不只是 gen-rsdc-skill 的 RSDC，還有所有 app 的 RSDC。
Task 14 擔心的「逐行對齊」chinese 已經做到，不必等這一項；但 gen-rsdc-app 自己寫 twin 的規則（例如標題逐字保留英文），交給 chinese 之前要確認 chinese 都涵蓋。

## 2. 現況

### 狀態細節

`check_parity.py` 新的檢查在既有 twin 找到的缺陷，9 份當天修好，3 份交給 Task 18 與 Task 14 第 3 期（見第 4 點最後一項）。

**原本列的四個缺口，現況**：

| 缺口 | 現況 |
|---|---|
| 標題加 `（繁體中文）` | 已解決（第 1 點）：規則是「twin 的標題與英文相同」，寫在 chinese 的規則裡，`check_parity.py` 與 `check_rsdc.py` 對還帶著後綴的標題發 WARN（commit `78934c2`）；兩個 repo 的 twin 都已收尾。 |
| 共用句子照範本 twin 的寫法 | 已解決（第 2 點，2026-10-11）：RSDC 在檔頭記下它用的範本（`> [[RSDC-App-tmp]]` 或 `> [[RSDC-Skill-System-tmp]]`），chinese 照那份範本 twin 的寫法抄共用句子，`check_parity.py` 對沒照抄的發 WARN。已寫好的 RSDC 還沒有這一行，等 Task 18 對齊時加上。 |
| RSDC 的術語保留英文 | 已解決（第 3 點）：Dataflow 用語都在 keep-English list 上了；2.1 定義的術語仍靠 chinese 讀檔辨認、保留英文。 |
| 跑成對檢查 | 已解決（第 4 點，2026-10-11）：`check_rsdc.py --tw` 有、`check_parity.py` 沒有的檢查已搬進 `check_parity.py`——每一節的 inline code 與章節引用，以及 Terms 節的 glossary term——chinese 寫完 twin 就在自己的 Step 3 檢查到，不必另外有人執行 `--tw`；過渡期間 gen-rsdc-app 照 Task 17 第 3 項自己執行 RSDC Checker。app 的 RSDC 已由 Task 12 與第 2 點解決：Checker 讀得了 App 範本，並從檔頭讀出範本。 |

**兩份範本已對齊（Task 12，2026-10-10 完成）**：兩份範本已逐節對齊（甲類 17 項、乙類 5 項）。
共用句子的措辭仍來自兩份範本各自的 twin：App 範本約 85 句、Skill-System 範本約 59 句，兩份都有的 23 句在兩份 twin 裡寫法相同（2026-10-11 查）。
所以 chinese 仍要知道一份 RSDC 用的是哪一份範本，這就是第 2 點的檔頭紀錄要解決的事。

**同一批檔案**：chinese 的 `SKILL.md`、tw 與 `check_parity.py` 上，Task 13 的那一列已完成，標題規則也已落地（commit `78934c2`）；剩下的是這一項的第 2 點（照抄範本 twin 的寫法、對沒照抄的發 WARN）與第 4 點。

**進度（2026-10-11）**：五點都已完成，Task 10 完成。
`check_parity.py` 新的檢查在既有 twin 找到的缺陷，9 份已修，3 份交給 Task 18 與 Task 14 第 3 期。
原本預期做完第 1 點，chinese 寫出的 Skill-System 範本 RSDC twin 就能通過 `check_rsdc.py --tw` 所有判 FAIL 的檢查，這一點仍未實測，因為還沒有 chinese 寫的這種 twin。
現有的兩組 RSDC twin 用 `check_rsdc.py --tw` 檢查（2026-10-11；MermaidView 依 Task 18 歸為 App 形狀，改用 App 範本），各還有一項與標題無關的 FAIL：SkillCompiler-RSDC 的英文檔沒有連到 twin 的那一行，chinese 逐行翻譯不會自己加（Task 18 把它對齊範本、加上 Twin line 之後解決）；MermaidView-RSDC-tw 的 4.1 比英文多了一個 `\s` inline code。
兩份都已列入 Task 18。

**英文與中文之間的空白（2026-10-10）**：RSDC Checker 原本只對 RSDC twin 檢查「英文緊貼中文」，現在成為 chinese 對所有 twin 的規則：英文詞、數字、inline code 與 placeholder token（例如 `{THE_SYSTEM}`）緊貼中文字時留一個空白，緊貼全形標點時不必留；兩個中文字之間永遠不留空白，中間隔著粗體標記也一樣。
寫在 chinese 的 `SKILL.md` 與 tw（MUST FOLLOW 一條、Step 2 散文一句、Step 3 一則 WARN），`check_parity.py` 對兩種情形各發 WARN（inline code、placeholder token 與連結文字都算英文，粗體標記透明）。
同時清掉既有 twin 的 41 則警告，只改 twin、不動英文檔：加了 13 個空白（英文緊貼中文：imp-app、imp-home 的 `SKILL-tw.md`、`Home-RSDC-tw.md`、`MermaidView-RSDC-tw.md`），拿掉 46 個空白（多半在中文粗體前後：imp-home 的 `SKILL-tw.md`、`Home-RSDC-tw.md`、`Wireframe-tw.md`，imp-app 的 `SKILL-tw.md`）。

## 3. 要做的

**要決定的事**：

1. **標題規則**：確認「twin 的標題與英文相同」並記錄下來，再收尾仍帶著後綴的 twin。
   **已完成（2026-10-10）**：規則記在 chinese 的 `SKILL.md` 與 tw（Step 4 的 Headings：文件標題也逐字照搬，被覆寫的 twin 若還帶著 `（繁體中文）` 就拿掉），`check_parity.py` 與 `check_rsdc.py` 對還帶著後綴的標題發 WARN（commit `78934c2`）；InvestForge 的 13 份 RSDC 與 wireframe twin 在 commit `58b8b35` 拿掉了後綴。
   最後兩份是 InvestForge 的 `imp-inv-fin-sight` 與 `imp-inv-tech-rank` 的 `SKILL-tw.md`，整份還是舊格式：H1 標題帶 `（繁體中文對照）`、一段前言、frontmatter 寫成 `yaml` 區塊。
   這兩份已改成現行格式（frontmatter、pairing line、沒有 H1，與英文相同），沿用原本的譯文，`imp-inv-tech-rank` 另補回一處 **skill root** 的粗體；兩份的 `check_parity.py` 都是 0 個 failure（InvestForge commit `83aed45`）。
   兩份仍有 WARN，留給 chinese 下次重譯時處理：術語譯成了中文（「步驟」「孿生檔」「確定性」等），tech-rank 還有十幾處粗體不會顯示。
   兩個 repo 共 51 份 twin，標題現在都與英文相同。
2. **共用句子的措辭**：要不要做；要做的話，chinese 怎麼知道範本——在 RSDC 的檔頭引用區記下範本（Task 13 的格式）、由呼叫者傳入，或等 Task 12 把兩份範本對齊成一套。
   **已決定（2026-10-10）**：要做，在 RSDC 的檔頭記下範本。
   **已完成（2026-10-11）**，做法與驗證見下方最後兩項。
   - **問題**：共用句子是 RSDC 從範本照抄、不含佔位符的句子，Task 12 之後 App 範本約 85 句、Skill-System 範本約 59 句。
     gen-rsdc-app 現在自己寫 twin，照範本 twin 的寫法（它的 `SKILL.md` 第 204 行）；twin 交給 chinese 之後，chinese 每句重譯，同一句在各份 twin 的寫法就不同。
     例如 MermaidView-RSDC-tw 第 51、629 行就和 App 範本 twin 不同；使用者在 Task 12 逐句審過的中文也會被丟掉。
   - **格式**：RSDC 的檔頭引用區多一行 `> [[RSDC-App-tmp]]` 或 `> [[RSDC-Skill-System-tmp]]`，用 `depends_on.py` 的格式，日期與指紋由 `record` 填入。
     InvestForge 的 RSDC 也找得到範本：`[[名稱]]` 在自己的 vault 找不到時，會到 config.yaml 的 skillGroups 底下找。
   - **誰寫**：gen-rsdc-skill 與 gen-rsdc-app 寫英文 RSDC 時加上這一行，並執行 `record`。
     範本自己不放這一行（範本不依賴自己），只在範本的指示區說明。
   - **chinese**：來源的檔頭連到一份範本（名稱以 `-tmp` 結尾，旁邊有它的 `-tw` twin）時，和範本某一行完全相同的英文行，照抄範本 twin 的對應行；`check_parity.py` 對沒照抄的發 WARN。
     只比對整行完全相同的句子，填了佔位符的句子仍由 chinese 翻譯。
   - **check_rsdc.py `--tw`**：從檔頭讀範本，不再固定用 Skill-System 範本，app 的 RSDC 也就能做共用句子這一項檢查（與第 4 點相關）。
   - **附帶效果**：範本改版後，`depends_on.py check` 會對記錄了它的 RSDC 報 CHANGED，指出哪些 RSDC 落後於範本。
   - **舊 RSDC**：重新產生時才寫入——記下指紋，等於聲明已對照過現在的範本。
     要不要先補一行不帶紀錄的連結，實作時再定。
     **決定（2026-10-11）**：不先補——舊 RSDC 大多是舊形狀，照抄得到的句子很少；Task 18 對齊每一份時，再加上範本連結並 record。
   - **時機**：依第 5 點，等 Task 12 把範本定稿後實作。
     2026-10-11：Task 12 已完成，當天實作。
   - **與 [[Task 17]]、[[Task 18]] 的關係**：gen-rsdc-app 寫範本紀錄的部分，和 Task 17 對 gen-rsdc-app 的修改（Optional 的節、4.5 的主張列、執行 RSDC Checker）改的是同一個檔案，最好一起做。
     Task 18 要讓 8 份已寫好的 RSDC 跟上範本，對齊時正好寫入範本紀錄，所以格式與兩個產生 RSDC 的 skill 最好在 Task 18 之前改好。
     **2026-10-11**：gen-rsdc-app 寫範本紀錄的部分已在這一項做完，Task 17 不必再做；兩項都已加上註記。
   - **沒選的做法**：不做（各自翻譯）；由呼叫者傳入（直接執行 `/chinese` 時沒有人傳，關係也不留在文件裡）；比對所有範本、不必知道是哪一份（不必改文件格式，但來源不寫在文件裡，也不能指出哪些 RSDC 落後於範本）。
   - **做了什麼（2026-10-11）**：
     - 兩份範本與它們的 twin：指示區各加一行，說明填好的文件在檔頭引用區、連到標準的連結之下連到範本，由 `depends_on.py` 記下指紋。
     - chinese 的 `scripts/scan_md.py`：新增 `template_pair()`，從檔頭找出 `[[…-tmp]]`，先在文件的 vault 找、找不到再到 `{skillGroups.common}` 找（不需要 config），確認範本與它的 twin 逐行對應；Step 1 的清冊多一段 template，列出每一個 shared line 與範本 twin 的寫法。
     - chinese 的 `scripts/check_parity.py`：逐行對應的 twin，對寫法與範本 twin 不同的 shared line 發 WARN，全部相同時 PASS；範本找不到、沒有 twin 或不逐行對應，也發 WARN。
     - chinese 的 `SKILL.md` 與 tw：加上 **template** 與 **shared line** 兩個詞、MUST FOLLOW 一條（shared line 照抄、不翻譯）、Step 0 到 Step 3 的說明，Dataflow 多一個外部輸入「template and its twin」。
       description 沒有改：它是 1019 字元，再加就超過載入器的 1024 字元上限。
     - `check_rsdc.py`：沒有 `--template` 時從檔頭讀出範本，`--tw-template` 預設為範本旁的 twin；檢查英文 RSDC 時新增一項「檔頭連到它所用的範本」，缺了判 FAIL。
     - gen-rsdc-skill 的 Step 5 與 gen-rsdc-app 的 Step 1（EN 與 tw）：寫 RSDC 時加上範本連結，寫完以 `depends_on.py record … --config config.yaml` 記下指紋——放在另一個 workspace 的 RSDC 要靠 config 找到範本；兩邊的 Dataflow 各多一支 config.yaml 到該 step 的箭頭。
   - **驗證（2026-10-11）**：用合成的 RSDC 測過：shared line 全照抄時 PASS、有一句不同時 WARN；`record` 記下範本指紋，`check` 報 UNCHANGED；`check_rsdc.py` 從檔頭選出 App 範本，沒有連結時退回 Skill-System 範本並判 FAIL；範本不存在、範本 twin 不逐行對應、檔頭連到兩份範本三種情況都會說明原因。
     新舊腳本對兩個 repo 51 組既有 twin 的結果完全相同；`check_rsdc.py` 對既有 RSDC 只多出「沒有連到範本」一項 FAIL。
     改過的三個 skill 與兩份範本 parity 都是 0 failure（gen-rsdc-app 原本就有一則 WARN），`depends_on.py check` 全部 UNCHANGED，兩份範本對標準的自我檢查都 PASS，check-skill 的掃描沒有新的 Dataflow 問題。
3. **術語**：把 Dataflow 用語加進 keep-English list（發新版本）。
   通用、便宜，對所有 twin 都有效。
   **已完成（2026-10-10）**：`tw-keep-english.md` 現在有 7 個 Dataflow 用語：caller、external input、one-run data、outcome、process、request、stage（commit `38abf86`）。
   當初加了 8 行，其中 one-call data 是 App 範本當時的用語；Task 12 把第三種資料統一成 one-run data 之後，這一行已經刪掉（commit `b9b96ff`）。
   process（DFD 的處理單元）不在原本列的六個裡，一併加上。
   版本照同一天併入的做法，維持 261010。
   Flagged 只放不會誤報的譯法：呼叫者、呼叫端、外部輸入、單次執行資料。
   呼叫方原本也在 Flagged，但它是「呼叫方式」的一部分，會誤報，已經移除。
   階段（「工作階段」是 session、「準備階段」是 phase）、請求、要求、結果、程序、行程都太常見，只列在 Replaces。
   新清單讓 12 份 twin 多了 WARN，已全部改好：35 處「呼叫者」「呼叫端」照英文改成 caller，分布在 RSDC-Standard-tw、Home-RSDC-tw、gen-rsdc-app／imp-app／imp-home 的 SKILL-tw，以及 InvestForge 的 6 份 app RSDC twin；SkillCompiler-RSDC-tw 的 5 處「外部輸入」照英文原文改成 input from outside，因為它的英文還沒改用標準的 external input。
   改完之後，兩個 repo 的 twin 都不再出現 caller 與 external input 的 Flagged 譯法；這 12 份的 FAIL 與改之前相同，`depends_on.py check` 也全部 UNCHANGED。
4. **成對檢查**：由誰執行；app 的 RSDC 沒有 checker，要怎麼辦。
   **現況（2026-10-11）**：後半已由 Task 12 解決，RSDC Checker 用 `--template`、`--tw-template` 指定就讀得了 App 範本（以 App 範本自我檢查，12 項通過，2 項失敗只是 Twin 連結的佔位符）。
   剩下「由誰執行」：gen-rsdc-skill 原本由 Step 8 執行 `--tw`，那一步已經拿掉；gen-rsdc-app 執行 RSDC Checker 排在 Task 17 第 3 項；chinese 寫完 RSDC twin 之後要不要執行，尚未決定。
   第 2 點已於 2026-10-11 做完，Checker 現在從檔頭讀出範本，不必手動指定。
   **已決定（2026-10-11）**：選項 2——把缺的檢查搬進 `check_parity.py`。
   **已完成（2026-10-11）**，做法、驗證與既有 twin 的新失敗見下方最後三項。
   - **問題**：成對檢查是 `check_rsdc.py --tw`，以前由 gen-rsdc-skill 的 Step 8 在寫完 twin 後執行；twin 改由 chinese 寫之後，沒有任何 step 執行它。
     chinese 自己的 `check_parity.py` 已涵蓋大部分項目（行數與行種類、標題、fenced block、連結、keep-English 的標記譯法、英文與中文之間的空白、標題後綴、shared line），只有 `--tw` 有的是四項：每一節的 inline code 相同（FAIL）、每一節的章節引用相同（FAIL）、RSDC 自己定義的詞（2.1 Terms、Artifact Types、Naming and Data Structures、stage 名稱）在 twin 裡被譯成中文（WARN）、條列不是範本的格式（WARN）。
   - **inline code 是所有 twin 的漏洞**：chinese 規定 inline code 逐字照搬，`check_parity.py` 卻從不比對。
     2026-10-11 對兩個 repo 的 52 組 twin 試算，20 組至少有一節的 inline code 不同。
     抽查多半是真的缺陷：InvFinSight-RSDC-tw 把 inline code 裡的公式譯成中文（`price × shares` 變成 `收盤價 × 發行股數`），imp-inv-ctl 的 SKILL-tw 把 `<vault-relative-path>` 譯成中文。
     少數是誤判：含反引號、用兩個反引號包住的 inline code，以及 pairing line 裡互換的檔名（`X-tw.md` 對 `X.md`）。
     章節引用不同的有 2 組（InvFinSight 的 RSDC twin 與 wireframe twin）。
   - **要做的**：
     1. `check_parity.py` 比對每一節的 inline code（FAIL）：用 `scan_md.py` 的 `CODE_SPAN_RE`（認得多個反引號），並排除 pairing line 那一行互換的檔名。
     2. `check_parity.py` 比對每一節的章節引用 `§N.M`（FAIL）。
     3. 讓 `check_parity.py` 把 RSDC 的 Terms 節（`- **名稱** —` 條列）也當成 glossary term，套用既有的粗體與未加粗次數檢查；實作時先確認不會誤報。
     4. 條列格式的 WARN 只屬範本，留在 `check_rsdc.py`，不搬。
     5. chinese 的 `SKILL.md` 與 tw：parity check 的定義與 Step 3 的清單加上第 1、2 項。
   - **既有的 twin**：新出現的失敗不一次修完。
     Task 18 與 Task 14 第 3 期本來就要重寫的舊 twin，留到那時處理；SkillsGestalt 裡真正的缺陷（imp-home 的 SKILL-tw 多一個 `imp-app`、MermaidView-RSDC-tw 多一個 `\s`），實作時再看。
     **2026-10-11**：兩處都是中文在英文說 which 的地方重複同一個名稱，沒有漏掉什麼；改以集合比對之後不算缺陷，SkillsGestalt 的 twin 全部通過。
   - **過渡**：gen-rsdc-app 現在同一次寫兩份，照 Task 17 第 3 項在寫完後執行 RSDC Checker；Task 14 把 twin 交給 chinese 之後，就由 chinese 的 Step 3 檢查。
   - **`check_rsdc.py --tw` 留著**：給產生 RSDC 的 skill 與手動使用；和 `check_parity.py` 重複的部分，日後再看要不要精簡。
   - **沒選的做法**：chinese 執行 `check_rsdc.py --tw`（通用的 chinese 會依賴 gen-rsdc-skill 的腳本，inline code 的漏洞也只在 RSDC 補上）；只由產生 RSDC 的 skill 執行（gen-rsdc-skill 不寫 twin，twin 重譯時也沒人檢查）；由 check-md-deps 定期掃描（不是寫完當下）；維持手動（容易忘）。
   - **做了什麼（2026-10-11）**：
     - `check_parity.py`：新增「每一節的 inline code 相同」與「每一節的章節引用相同」兩項 FAIL。
       以段落為單位讀取，被斷行切開的 inline code 仍是一個；以集合比對，中文在英文說 which 的地方重複一個名稱不算缺陷；pairing line 不列入，來源檔中指名 twin 的 span 與 twin 中指名來源檔的 span 視為同一個。
       章節引用是 `§2.3`；檔頭連到範本的檔案，不帶 § 的 `2.3` 也算——比原本記的「只比 `§N.M`」多了這一項，對應 `check_rsdc.py --tw` 原本對 RSDC 內部引用的檢查。
       一般文件不比裸編號，因為英文的「1.8s」對中文的「1.8 秒」這類單位寫法會誤報。
     - `scan_md.py`：`glossary_terms()` 也讀任何層級名為 Terms 的節（RSDC 的 2.1 Terms），所以 `check_parity.py` 既有的粗體與未加粗次數檢查，也套用到 RSDC 定義的術語。
     - chinese 的 `SKILL.md` 與 tw：glossary term 與 parity check 的定義、Step 1 第 4 項，以及 Step 3 新增的第 7、8 項（之後各項順延）。
   - **驗證（2026-10-11）**：合成的 RSDC 測過：連到範本的檔案漏掉不帶 § 的引用會 FAIL，沒連到範本的檔案不比裸編號；Terms 節的術語被譯成中文會 FAIL；跨行的 inline code 不會誤判。
     新舊腳本對兩個 repo 的 52 組 twin 比較，只有新加的兩項造成差異。
     SkillsGestalt 的 twin 全部通過，chinese 自己的 pair 是 0 failure、0 warning；兩份範本加上 Terms 的 glossary 檢查之後，結果不變。
   - **既有 twin 的新失敗（2026-10-11）**：12 份，都在 InvestForge，逐一看過都是真的缺陷——inline code 的內容被譯成中文（`<vault-relative-path>` 變成 `<vault 相對路徑>`、`unchanged` 變成 `不變`、`{holding name}` 變成 `{持股名稱}`），inline code 漏掉（InvDataflow-RSDC-tw 少了 `declared nothing`），或被改掉（`[Header]` 變成 `[Panel]`）。
     - 已有 task 負責的 3 份：InvDataflow-RSDC-tw（Task 18）；InvDatabase 與 InvFinSight 的 RSDC twin（Task 14 第 3 期，owner skill 的 design pair）。
       已在 Task 18、Task 14 註記各自的缺陷。
     - 沒有 task 負責的 9 份：check-stop-price、extract-filled-orders、select-stocks 與 4 個 owner skill（imp-inv-ctl、imp-inv-database、imp-inv-fin-sight、imp-inv-tech-rank）的 SKILL-tw，以及 InvDatabase、InvFinSight 的 Wireframe-tw。
       **2026-10-11 已修**：被譯成中文的 inline code 改回英文原樣（`<vault-relative-path>`、`证券买入(name)`、`Magic <score>/<largest> @period`、`{group} ({n})`、`unchanged` 等），`[Panel]` 改回 `[Header]`，InvFinSight 的 Wireframe-tw 拿掉自己加上的 §；4 個 owner skill 的 SKILL-tw 原本用 `SKILL.md` 指英文檔——twin 裡的「本檔」會指到自己——改寫成「旁邊的英文版」。
       新檢查的失敗全部消失，沒有新增任何 FAIL 或 WARN，InvDatabase 的 Wireframe-tw 還順帶補回了 placeholder `{group}`。
       其中 4 份現在完全通過；另外 5 份仍有之前就存在的失敗（標題被譯成中文、行數不同、frontmatter 的 name、粗體次數、連結），不在這一項。
5. **順序**：Task 12 與這一項誰先——Task 14 在等這一項，而第 2、4 點取決於 Task 12 的結果。
   **已決定（2026-10-10）**：Task 12 先做；第 2、4 點等它對齊完範本再定。
   Task 12 已於 2026-10-10 完成。

**牽涉的檔案**：

- `.github/common/skills/chinese/SKILL.md` 與 tw、`scripts/scan_md.py`、`scripts/check_parity.py`（第 2、4 點已完成）。
- `.github/common/skills/gen-rsdc-skill/SKILL.md`、`.github/common/skills/gen-rsdc-app/SKILL.md` 與它們的 tw（第 2 點：寫英文 RSDC 時在檔頭記下範本，已完成）。
- `.github/common/references/tw-keep-english.md`（第 3 點，已完成）。
- `.github/common/skills/gen-rsdc-skill/scripts/check_rsdc.py` 的 `--tw` 模式：成對檢查已經寫好，Task 12 之後也讀得了 App 範本（`--template`、`--tw-template`），只是現在沒有任何 step 會執行它；第 2 點已讓它從檔頭讀出範本。
  第 4 點決定它留給產生 RSDC 的 skill 與手動使用，twin 的成對檢查改由 `check_parity.py` 承擔。
- 共用句子措辭的來源（指示區已各加一行，說明檔頭的範本連結）：`.github/common/skills/gen-rsdc-skill/assets/RSDC-Skill-System-tmp-tw.md` 與 `.github/common/skills/gen-rsdc-app/assets/RSDC-App-tmp-tw.md`。
- 還帶著標題後綴的 twin（第 1 點，已收尾）：`.github/common/skills/compile-skill/references/Tasks-tw.md`、`SkillCompiler-RSDC-tw.md`，InvestForge 的 7 份 RSDC twin（StopPriceChecker、InvDataflow、InvIndexAnalyzer、InvCtl、InvFinSight、InvDatabase、InvTechRank），以及 InvestForge 的 `imp-inv-fin-sight`、`imp-inv-tech-rank` 的 `SKILL-tw.md`。
- 日後要重寫的 RSDC twin：InvestForge 的 `.claude/skills/check-stop-price/references/StopPriceChecker-RSDC-tw.md`（舊格式），以及其他已寫好的 RSDC，都已列入 Task 18。

## 4. 驗證

—

## 5. 與其他 task 的關係

—

## 6. 知識

—

## 7. 日誌

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-11

- 第 2 點（共用句子照範本 twin 的寫法）、第 4 點（成對檢查搬進 `check_parity.py`）完成，第 5 點的 Task 12 已完成。
- 五點都完成，Task 10 完成。
- 9 份既有 twin 的缺陷當天修好，3 份交給 Task 18 與 Task 14 第 3 期。

### 2026-10-10

- 提出：gen-rsdc-skill 拿掉處理中文的 step，把 RSDC twin 交給 chinese skill。
- 第 1 點（標題規則）與第 3 點（Dataflow 用語加進 keep-English list）完成。
- Task 12 完成，兩份範本對齊。
- 英文與中文之間的空白成為 chinese 對所有 twin 的規則。
