# Task 8 - 文件依賴的檢查方式——依賴方記下被依賴方的 hash

**Status**：完成——2026-10-10 做法定案並實作：依賴寫在檔頭引用區，由共用的 `depends_on.py` 檢查與記錄，套用在 skill ↔ RSDC 與範本 ↔ 標準（見下方「做了什麼」）；其他 skill 的後續工作移到 Task 13。
**Raised**：2026-10-09，討論文件之間的依賴時提出。
**Depends on**：—

## 1. 背景

構想：兩個文件 A 依賴 B（A ---> B）時，A 要記下 B 的 hash，之後用它檢查 B 有沒有變更；B 變了，A 就可能過期，要重新對照。
依賴的方向和 RSDC 的單向依賴一致：記 hash 的是上層文件（依賴方），被依賴的下層文件不知道有誰依賴它。

**評估（2026-10-10）**：構想正確，而且不是新機制——repo 裡已有兩份同樣做法的實作，要做的其實是把它抽成共用工具。
八個待決定事項多半已有前例可循。

- **補充上表**：
  - check-stop-price 的做法比表上寫的更完整：指紋記在 skill 目錄裡的 sidecar `plan-docs-hash.json`，由 `plan_docs_hash.py` 的兩個指令負責——`check` 只比對、不寫入，判定 `UNCHANGED`／`CHANGED`／`NO_RECORD`；`record` 只在 Rule Copies 已與文件一致之後才執行。
    正規化（UTF-8、去掉 BOM、換行一律 LF）與 compile-skill 的 `source_fingerprint()` 相同。
    這就是本構想的參考實作。
  - 漏了 **check-wiki-doc**：它是 repo 裡唯一通用的文件依賴管理——架構文件的〈文件依賴關係表〉、一條邊一列的〈文件依賴狀態表〉，以及〈文件狀態〉的 `待檢查` 欄。
    `待檢查` 要靠 agent 記得在改動之後打 ✓，在別處（Obsidian、其他 session）做的修改就會漏掉；記下 hash 正好能把它機械化。
    它的第 6 條也已規定只比對直接下層、不遞迴。
- **一個沒列出的陷阱：hash 不要存在依賴方 A 裡。**
  每次確認都會改動 A，A 自己的依賴方就跟著被判為變更——例如已編譯 skill 的 `SOURCE_SHA256` 失效、twin 被判為英文檔已改；RSDC 也沒有 frontmatter，twin 還要逐行對齊。
  照 check-stop-price 放在 A 旁邊的 sidecar，就沒有這個問題。
- **對八個問題的建議**：
  1. 存在哪裡：A 旁邊的 sidecar JSON（check-stop-price 的前例）。
  2. hash 什麼：預設整份檔案，先正規化 BOM 與換行（兩個前例都是）；skill ↔ RSDC 再細到被引用的節，以節的**標題**為鍵，節號變了也對得上。
  3. 確認：只有 `record` 會寫入，而且只在重讀並確認之後執行；`check` 永不寫入。
     由產生器產出的依賴方（twin、`skill.py`）可以在產生時自動記錄，因為它就是照當下的 B 產生的。
  4. 不符：預設警告；現在會停的地方（gen-rsdc-skill 的 Step 2）照舊停。
  5. 誰檢查：一支共用腳本，既有的檢查（`check_rsdc.py`、check-wiki-doc）呼叫它，或沿用它的記錄格式。
  6. 間接依賴：不遞迴（check-wiki-doc 第 6 條的前例）；A 真的依賴 C，就直接記 A → C。
  7. twin：值得做，由 chinese skill 產生 twin 時記下英文檔的 hash；可以排在後面。
  8. 用內容的 SHA-256，不用 git hash（兩個前例都是）。
- **為什麼值得做**：範本 ↔ 標準靠版本號，而 2026-10-09 同一天的修改都併入 261010（Task 3、Task 4 都是），標準的內容改了好幾次，版本號卻沒變；範本記著 261010，看不出它對齊的是哪一次。
  內容 hash 每一次都抓得到。

## 2. 現況

**repo 裡已經有幾處各自做的類似機制**——它們說明需求是真的，也說明目前沒有共通的做法：

| 依賴方 A | 被依賴方 B | 現在怎麼檢查 B 有沒有變 | 缺點 |
|---|---|---|---|
| 已編譯的 `skill.py` | Skill Source（`SKILL.md`） | `skill.py` 記 `SOURCE_SHA256`，`check_compiled.py` 比對（compile-skill） | 只有這一組；整份檔案的 hash，任何改動都算變更 |
| check-stop-price 的 Rule Copies | 四份 Plan Docs 與 StopPriceChecker-RSDC | skill 記各檔的 SHA-256 指紋，不符就重新對照 | 做法寫在 skill 自己的流程裡，別的 skill 不能共用 |
| RSDC 範本（兩份） | RSDC 標準 | 範本記標準的 **Version**；gen-rsdc-skill 的 Step 2 以 `check_rsdc.py --standard` 比對，imp-app 在 Step 0 由 agent 比對 | 比的是人手動維護的版本號，不是內容；標準改了卻沒升版，就偵測不到 |
| skill | 它引用的 RSDC | `check_rsdc.py --skill` 檢查被引用的節存在、標題相符 | 節的內容改了，引用仍然通過 |
| 繁體中文 twin | 英文檔 | `check_parity.py` 與 `check_rsdc.py` 的 pair 檢查逐行比對結構 | 比對結構，不知道英文檔在 twin 寫成之後是否又改過 |

**決定**（2026-10-10，問過使用者）：

- **依賴寫在檔頭引用區，這是唯一的寫法**（改定）：文件開頭的 `>` 行——在 frontmatter、標題或 twin 的 pairing line 之下——每一行一個連結；連結後面各自一段 inline code：只算引用到的節時先寫 `cited`，然後是紀錄——確認的日期與當時的指紋，例如 `` > [[RSDC-Standard]]  `2026-10-10`  `a6b1c2712472` ``、`` > [[SkillCompiler-RSDC]]  `cited`  `2026-10-10`  `bd7932a83cd3` ``（2026-10-10 依使用者的例子改成這個格式）。
  連結與 `cited` 由宣告的人寫，日期與指紋由 `record` 填。
  RSDC 與 check-wiki-doc 的 wiki 筆記本來就在這裡宣告依賴（`> [[RSDC-Standard]]`），所以 skill、RSDC 與 wiki 筆記共用這一種寫法。
  這個 repo 與 InvestForge 都是 Obsidian vault，body 裡的 `[[...]]` 有反向連結，改名時也會自動更新；連結目標與 inline code 都會被 chinese skill 原樣抄進 twin。
  不在同一個 vault 的檔案，寫成 `[名稱](<路徑>)`，路徑可以用 `{wikiDir}`。
- **先前的寫法都不用了**：frontmatter 的兩種寫法（SKILL.md 的 `metadata` 字串、wiki 筆記的連結清單）已經拿掉。
  第二個 frontmatter 也不採用——只有檔案最開頭那一塊才是 frontmatter，第二塊其實是 body 的開頭：畫面上會顯示成分隔線與一段文字，skill 每次啟用都會讀進 context。
- **範本也用檔頭引用區，但不加 frontmatter**：範本加了 frontmatter，chinese skill 會把它當成 SKILL.md 那一類（在 twin 加 pairing line），範本與 twin 的行數就對不上。
  範本的檔頭本來就有 `> [[RSDC-Standard]]` 與 `> [[DFD]]`，指紋就記在這兩行後面；版本號仍寫在範本區塊裡給人讀。
  寫成的 RSDC 照抄這兩行，所以也帶著它所依據的標準指紋。
- **版本號與 hash 都留**：版本號給人讀，hash 給程式判斷。
- **共用腳本放在 `.github/common/scripts/`**。
- **第一步**：skill ↔ RSDC（compile-skill 與 gen-rsdc-skill）加上範本 ↔ 標準。
- **hash 不符就停下**：gen-rsdc-skill 的 Step 2 與 imp-app `reverse` 的 Step 0。

**做了什麼**（第一步）：

- **共用腳本** [depends_on.py](../.github/common/scripts/depends_on.py)，三個指令：
  - `check`：逐一比對，判定 `UNCHANGED`／`CHANGED`／`NO_RECORD`／`NOTHING_CITED`／`MISSING`，不寫入；有變更時 exit 1，找不到檔案時 exit 2。
  - `record`：重讀並確認之後才執行，在每個連結後面寫入確認的日期與目前的指紋；`--target` 只記一個依賴，而且它得先在檔頭引用區宣告——宣告由寫文件的人（或 step）負責，紀錄才是腳本的事。
    不會改 twin，只提醒 twin 有自己的檔頭引用區。
  - `hash`：印出一個檔案的指紋，`--cited-by` 時只算被引用的節。
  - 指紋：SHA-256 前 12 碼；UTF-8、去掉 BOM、換行一律 LF（和 `plan_docs_hash.py`、`source_fingerprint()` 相同，已比對確認前 12 碼一致）；計算時去掉被依賴方自己的檔頭引用區（連同其後的空行，所以有沒有檔頭引用區算出來都一樣），所以確認依賴不會讓下游跟著被判為改過。
    `cited` 只算 A 以 `§N.M *標題*` 引用的節，依標題開頭比對（同 RSDC Checker），不依節號；引用緊接在另一個 `.md` 檔名之後的不算。
- **範本 ↔ 標準**：
  - 兩份範本與 tw 的檔頭引用區，用 `depends_on.py record` 在 `> [[RSDC-Standard]]` 與 `> [[DFD]]` 後面記下指紋；範本區塊只留版本號，並說明指紋記在上面的連結後面。
  - `check_rsdc.py --standard` 除了版本號，也從範本的檔頭引用區讀出指紋來比對：不符 FAIL（exit 1）；範本沒連到標準，或連結後面沒有紀錄時 exit 2。
    它保留檔頭連結的規則也改了：連結後面的紀錄不算在比對內，寫成的 RSDC 日後重新記錄標準，仍算保留了連結。
  - gen-rsdc-skill 的 Step 2（停下、`step-2.yaml` 多 `pins`、MD report 一併列出）與 imp-app `reverse` 的 Step 0（agent 對 `RSDC-App-tmp.md` 執行 `check`）照此改寫，EN 與 tw 一起改。
- **skill ↔ RSDC**：
  - compile-skill 與 gen-rsdc-skill 的 `SKILL.md` 與 tw，在檔頭引用區宣告並記下 `> [[SkillCompiler-RSDC]]`（`cited`）。
    這是 2026-10-10 的基準：確認過每一處引用都落在 RSDC 的某一節，但沒有重讀內容。
  - gen-rsdc-skill 的 Step 8 在 Skill Source 的 frontmatter 正下方宣告 `> [[<system name>-RSDC]]`，Step 9 在引用檢查通過後用 `record` 在它後面記下 RSDC；字彙表的 Skill Source 改寫為「Step 8 編輯它；Step 9 修正它的引用，並在它裡面記下它所引用的 RSDC」（Step 9 本來就會修正它，這只是讓定義說實話；多寫入者的問題仍是 Task 7）。
- **驗證**：`depends_on.py` 在 scratch 樣本上測過檔頭引用區的位置判斷（在標題或 pairing line 之下才算，H2 之後或前面超過兩行不算）、`[[名稱]]`（含別名）與路徑連結、`.obsidian`／`.git` 作為 vault 根目錄、有沒有檔頭引用區指紋都一樣、只改未引用的節不觸發、改被引用的節觸發、BOM／CRLF、`{wikiDir}` 與 `--config`、名稱重複的筆記、各種格式錯誤；`check_rsdc.py --standard` 對兩份範本 PASS，標準內容改了而版本沒變時 FAIL，少了指紋時 exit 2；用範本填的樣本 single／pair 照舊 PASS；四份 SKILL 的 `check_parity.py` 0 failure（imp-app 的 11 個警告與改之前相同）；`scan_source.py` 都 valid；check-skill 的 frontmatter 檢查通過。

## 3. 要做的

**要決定的**：

1. **hash 存在哪裡**：依賴方的 frontmatter 或文件開頭的一段（例如 `depends-on` 列出路徑與 hash），或旁邊的檔案。
   RSDC 文件沒有 frontmatter，而且寫成的 RSDC 不能提到 skill，所以放在上層文件裡比較自然。
2. **hash 什麼**：整份檔案最簡單，但連錯字修正都會觸發；只 hash 被引用的節更精準，但要能取出節（RSDC 的節號、skill 的 step 標題），而且節號改了就對不上。
   換行與空白要先正規化——repo 同時有 Windows 路徑和 Dropbox 同步，CRLF 與 LF 不能算成不同的內容。
3. **「已對照過」怎麼記**：只有在人（或 Claude）實際重讀 B 並確認 A 仍然成立之後，才更新 A 記的 hash；自動更新會讓檢查失去意義。
   需要一個明確的「確認」動作。
4. **不符時怎麼辦**：是警告（可能過期）還是失敗？
   多半應該是警告，因為多數變更不影響 A。
5. **誰來檢查**：共用一支腳本，還是併進 check-skill、`check_rsdc.py` 等既有的檢查；要不要取代上表中人手動維護的版本號比對。
6. **間接依賴**：A 依賴 B、B 依賴 C，C 變了，B 過期，A 要不要也算過期？
7. **twin 怎麼辦**：twin 依賴英文檔，要不要同樣記英文檔的 hash，補上現有結構比對看不到的「英文檔之後又改了」。
8. **用 git 還是內容 hash**：記 git 的 commit 或 blob hash 很省事，但離開 git（Dropbox 同步的副本、其他 repo）就失效；內容的 SHA-256 哪裡都能算。

**暫時的傾向（尚未決定）**：用內容的 SHA-256，由一支共用腳本負責「檢查」與「確認後更新」，不符時只警告；先從 skill ↔ RSDC 與 範本 ↔ 標準這兩組開始，因為前者現在完全沒有內容檢查，後者靠人手動維護的版本號。

**牽涉的檔案**（若要做）：

- 檢查：`.github/common/skills/check-skill/scripts/scan_skill.py`、`.github/common/skills/gen-rsdc-skill/scripts/check_rsdc.py`（`--skill` 與 pair 檢查）、`.github/common/skills/compile-skill/scripts/check_compiled.py`（可當作現成的參考實作）。
- 規則：`.github/common/references/RSDC-Standard.md` 與 tw 的 Core Writing Principle（單向依賴）；[DFD.md](../.github/common/references/DFD.md) 已寫明「文件之間的引用不畫成線」，所以這種依賴不畫在 Dataflow 裡，要另外找地方說明。
- skill：gen-rsdc-skill 的 Step 2 與 imp-app 的 Step 0（版本比對）；gen-rsdc-skill 的 Step 9（引用檢查）。
- 與 Task 6（tasks skill）、Task 7 有關：Task 6 若建檢查腳本，這支腳本可以共用；Task 7 的 check-skill 檢查也在同一支 `scan_skill.py`。

**還沒做的**：各 skill 的後續工作——chinese（含 twin ↔ 英文檔）、check-wiki-doc、compile-skill 的 `source_fingerprint()`、check-skill、gen-skill，以及 check-stop-price 的遷移——移到 [[Task 13]]。
imp-app 的範本比對已改由它執行 `depends_on.py check`，不再是 agent 自己比。

## 4. 驗證

—

## 5. 與其他 task 的關係

—

## 6. 日誌

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-10

- 評估後定案：依賴寫在檔頭引用區，由共用的 depends_on.py 檢查與記錄。
- 第一步套用在 skill 與 RSDC、範本與標準兩組，其他 skill 的後續工作移到 Task 13。

### 2026-10-09

- 提出：討論文件之間的依賴時，想到依賴方記下被依賴方的 hash 來檢查有沒有變更。
