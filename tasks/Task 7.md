# Task 7 - 決定如何處理 gen-rsdc-skill 與 chinese 的 Dataflow 揭露的多寫入者與往回讀取

**Status**：完成——2026-10-10 採用選項 1 的變體：不新增圖上的標記，改用圖上本來就有的雙向箭頭來區分。
**Raised**：2026-10-09，為 gen-rsdc-skill 的 SKILL.md 加上 `# Dataflow` 後，用 check-skill 的 `scan_skill.py` 檢查時發現。
**Depends on**：—

## 1. 背景

問題：[gen-rsdc-skill 的 SKILL.md](../.github/common/skills/gen-rsdc-skill/SKILL.md) 的 `# Dataflow` 照 SKILL template 畫出 Workflow 實際的讀寫後，`scan_skill.py` 回報兩類問題，check-skill 的 [checking-criteria.md](../.github/common/skills/check-skill/references/checking-criteria.md) 第 6 節第 4、6 項都會把它們判為 issue。
圖沒有畫錯：問題出在 workflow 本身的設計。

**原因**：

- **「寫 → 審查 → 檢查並修正」的循環**：Step 4 套用審查修改；Step 5、7、9 遇到 `[FAIL]` 就當場修正；Step 9 發現 skill 需要的名稱 English RSDC 沒有定義時，會在 RSDC pair 兩份的第 2 章補上契約。
- **就地修改既有的檔案**：Skill Source 在 Step 0–2 被讀取，Step 8 才改寫它。
  前面的 step 讀到的是執行前的版本，並不依賴 Step 8 的產出，但圖上分不出這個差別。

評估（2026-10-10）：選項 1 的方向對，但不必新增標記——圖上本來就有區分的記號，就是雙向箭頭（DFD.md：「一個 process 既讀又寫的資料」）。
兩類問題其實是兩件事：

- **多寫入者**：DFD.md 反對它的理由是「重跑其中一個，會悄悄抹掉另一個的結果」。
  這在後面的寫入者**只寫不讀**時成立，它蓋掉前一個的內容；後面的寫入者**讀了再改**（雙向箭頭）時不成立，它是在前一個的結果上繼續做。
  gen-rsdc-skill 的 RSDC 與 Skill Source、chinese 的 TW twin，每一個後面的寫入者都是雙向箭頭——「寫 → 審查 → 檢查並修正」本來就是這個形狀，不是 workflow 的缺陷。
- **讀取較後的寫入**：forward reference 的意思是讀到一份**還不存在**的資料。
  第一個寫入者也讀這份 record（雙向箭頭），表示它在執行開始之前就存在——Skill Source 是正在處理的 skill，keep-English list、TW twin 的舊檔與 git history 是先前的執行與使用者留下的——之前的 step 讀到的是它原本的樣子。
  第一個寫入者只寫不讀（它建立這份 record）時，更早的讀取仍是 forward reference。
- 選項 2（改 workflow）仍不可取，理由同前：檢查與修正併在同一個 step，是這類 skill 的正常形狀，要消掉只能失去分工。
  選項 3（接受並註明）會讓 check-skill 每次報出十幾筆 issue，把真正的問題淹沒。
- 真實的代價還在，所以規則沒有放寬成不設限：重跑第一個寫入者會讓其餘的編輯全部重做。
  這一點交給判斷（recommendation），不是掃描器能決定的。

## 2. 現況

**編號**：這一節寫成之後，gen-rsdc-skill 新增了 Step 1 - Check the RSDC Template Against the Standard（2026-10-09），原 Step 1–10 改為 Step 2–11。
下文的 step 編號是改號之前的；`scan_skill.py` 現在印出新編號，問題本身沒有變——新的 Step 1 只讀 RSDC standard 與 RSDC template。

**更新（2026-10-10）**：gen-rsdc-skill 拿掉了處理中文的 step（原 Step 7 Write the RSDC Twin、Step 8 Check the RSDC Pair、Step 11 Refresh the SKILL Twin），現在是 Step 0–9，兩份 twin 都交由 `chinese` skill。
重跑 `scan_skill.py` 的結果：`multi_writer_records` 只剩 English RSDC（Step 4、5、6、8）與 Skill Source（Step 7、8），RSDC twin 已不在其中；`reads_of_later_writes` 剩 Skill Source 7 對、English RSDC 7 對。
下文的清單是舊的結果，問題的性質不變。
之後又在 Step 0 之後新增 Step 1 - Locate the Skill Source and Its RSDC，原 Step 1–9 改為 Step 2–10，現在是 Step 0–10；原本由 Step 0 讀 Skill Source，現在由新的 Step 1 讀，兩類問題的數量都沒有變。

**併入 chinese skill（2026-10-10）**：為 [chinese skill](../.github/common/skills/chinese/SKILL.md) 加上 `# Dataflow` 後，`scan_skill.py` 報出同樣兩類問題，原因也相同：

- `multi_writer_records`：TW twin——Step 2 - Translate into the TW Twin 寫出它，Step 3 - Parity Check 檢查不通過時就地修正它（「寫 → 檢查並修正」的循環）。
- `reads_of_later_writes`，兩處（就地修改既有的檔案）：keep-English list——Step 1 讀取，Step 2 才在其中新增術語；TW twin——Step 2 覆寫前讀取舊檔，只為了保留標題的 `（繁體中文）` 後綴，Step 3 之後再修正它。
- chinese 的圖例最後一行已照實寫明這三處（"Both records are changed in place…"）。
  這裡若決定修訂規則（選項 1），那一行要跟著改，或換成規則要求的標記；若決定改 workflow（選項 2），chinese 能消掉的只有 Step 1 那一處——把 Step 1 清冊的第 8 項（散文用到哪些 keep-English 術語）移到 Step 2，Step 1 就不必讀清單——另外兩處就是就地覆寫與檢查並修正本身，消不掉。
- 重現時不必借別的 workspace 的 config：臨時寫一份只有 `skillGroups: {common: <workspace>/.github/common}` 的 config 給 `--config` 即可。
  但 `scan_skill.py` 以 config 所在的目錄當作 workspace 根目錄來解析連結，臨時 config 放在別處時，`broken_github_links` 會把 `.github/...` 的連結誤報為斷掉。

**`scan_skill.py` 的結果**：

- **`multi_writer_records`**（第 4 項 One writer per record）：
  - English RSDC：Step 3、4、5、7、9
  - RSDC twin：Step 6、7、9
  - Skill Source：Step 8、9
- **`reads_of_later_writes`**（第 6 項 No read of a later write）：
  - Skill Source：Step 0、1、2 讀取，Step 8、9 之後才改寫；Step 8 讀取，Step 9 再改。
    共 7 對。
  - English RSDC：Step 3 到 Step 9 之間反覆讀寫，共 13 對。
  - RSDC twin：Step 7 讀取，Step 9 再改。

重現方式（SkillsGestalt 沒有 `config.yaml`，要借一份有 `skillGroups` 的，例如 InvestForge 的）：`python .github/common/skills/check-skill/scripts/scan_skill.py --skill gen-rsdc-skill --template .github/common/templates/SKILL-tmp.md --config <有 skillGroups 的 config.yaml> --out <scratch 資料夾>/facts.yaml`，再看 `facts.yaml` 的 `dataflow` 一段。

做了什麼（2026-10-10；標準的修改併入 261010，EN 與 tw 一起改）：

- **DFD.md 與 tw**：多寫入者的缺陷加一句「唯一的例外是依序編輯的 record」，並新增一條「不算缺陷：依序編輯的 record」——後面的每個寫入者都讀取它；第一個寫入者也讀取它時，更早的 process 讀到的是它原本的樣子；代價是重跑第一個寫入者會重做其餘，流程要說明如何處理。
- **RSDC-Standard.md 與 tw**：261010 的 changelog 新增 **A record edited in turn is not a second writer.**
- **check-skill**：
  - `scan_skill.py` 的 `dataflow()`：`multi_writer_records` 只列被較後寫入者覆寫的 record（每筆多一個 `overwritten_by`）；新增 `records_edited_in_turn`（後面的每個寫入者都讀取它）與 `records_read_as_found`（第一個寫入者也讀取它，在它之前讀取的 step）；`reads_of_later_writes` 排除這兩種情形。
  - `checking-criteria.md` 與 tw 的第 6 節第 4、6 項：覆寫是 issue；依序編輯不是，只判斷重跑第一個寫入者會怎樣（沒有說明是 recommendation）；`records_read_as_found` 要確認那份 record 在執行前就存在，否則仍是 issue。
  - `SKILL.md` 與 tw 列出 dataflow 事實的那一句，補上兩個新事實。
- **SKILL template**（`templates/SKILL-tmp.md` 與 tw）`# Dataflow` 開頭的那句，「有兩個寫入者的 record」改為「被較後 step 覆寫的 record」；gen-rsdc-skill 與 chinese 的 `# Dataflow` 抄了同一句，一併改；chinese 圖例的最後一個項目，把「TW twin 有兩個寫入者」改為「依序編輯」，並說明每個寫入者也讀取它所改的 record。
- **兩份 RSDC 範本**（Skill-System 與 App，EN 與 tw）：一份 record 有多個寫入者的缺陷段落，改為「第二個寫入者不先讀取它」才是缺陷；Skill-System 範本的指示行同步。
  四份檔案記下的 `[[RSDC-Standard]]` 與 `[[DFD]]` 指紋，讀完變動、確認範本仍然成立之後，用 `depends_on.py record` 重新記下。

## 3. 要做的

**選項**：

1. **修訂規則**：在 [DFD.md](../.github/common/references/DFD.md) 的 "What Counts as a Defect"，以及 check-skill 準則第 6 節第 4、6 項，承認兩種情況——一個 step 當場修正它剛檢查過的檔案；一份就地修改的檔案，前面的 step 讀到的是它執行前的狀態——並讓 `scan_skill.py` 分辨得出來（例如由圖上的標記指出）。
   要注意：DFD.md 反對多寫入者的理由是「重跑其中一個，會悄悄抹掉另一個的結果」。
   就地修正不會抹掉別人的結果；但 Step 3 是整份重寫（它會先問），重跑它確實會抹掉 Step 4、5、7、9 的修正。
   DFD.md 屬於 RSDC standard，改它要在 `RSDC-Standard.md` 的 "Changes in This Version" 記下版本。
2. **改 gen-rsdc-skill 的 workflow**：例如檢查的 step 只檢查、不修正，失敗就回到負責寫的 step。
   這消不掉問題：修正所需的資料會往回流（較後的檢查 step 產出、較前的 step 讀取），一樣是往回讀。
   要完全消除，只能把寫和檢查併成同一個 step，失去現在的分工。
3. **接受，並在圖例註明**：成本最低，但 check-skill 每次都會報出這些 issue，真正的問題會被淹沒。

**牽涉的檔案**：

- 規則：`.github/common/references/DFD.md` 與 tw；`.github/common/references/RSDC-Standard.md` 與 tw（記版本）；`.github/common/skills/check-skill/references/checking-criteria.md` 與 tw 的第 6 節。
- 檢查：`.github/common/skills/check-skill/scripts/scan_skill.py` 的 `dataflow()`（`multi_writer_records`、`reads_of_later_writes`）。
- 範本：SKILL template（`.github/common/templates/SKILL-tmp.md` 與 tw）`# Dataflow` 的開頭段落，說這張圖要讓「有兩個寫入者的 record……或讀取較後 step 所寫之物的 step」一眼就看得出來；規則修訂的話，這句要跟著改。
- skill：gen-rsdc-skill 的 `SKILL.md` 與 tw 的 `# Dataflow`；選 2 的話還有 Step 3–9。
  chinese 的 `SKILL.md` 與 tw 的 `# Dataflow`（圖例的最後一行）；選 2 的話還有它的 Step 1 與 Step 2。
  日後其他有檢查並修正循環、或會就地修改檔案的 skill 加上 Dataflow 時，也會遇到同樣的問題。

**另一件相關的小事**：gen-rsdc-skill 的 Dataflow 圖例引用 [SkillCompiler-RSDC](../.github/common/skills/compile-skill/references/SkillCompiler-RSDC.md) §2.3 *Dataflow*（Step 1、9 畫成雙邊框，因為它們執行的 Source Scanner 屬於 SkillCompiler 這個 RSDC system）。
SkillCompiler-RSDC 還是舊格式；用現在的 RSDC 範本重寫後，Dataflow 會是 2.2，這個引用就過期了，而目前沒有任何檢查會發現。

留下的：

- **`records_read_as_found` 需要判斷**：掃描器只看「第一個寫入者也讀取它」，不能確認那份 record 真的在執行前就存在。
  第一個寫入者若是為了別的理由才讀它，會被誤放行；這一點寫進判準，由 check-skill 在讀事實時確認。
- **已寫好的 RSDC**：InvestForge 的 StopPriceChecker-RSDC 裡 Check Table 的「兩個寫入者」缺陷，現在要重新判斷——Back-solve 若讀取並修改 Judge 寫的表，就是依序編輯，不再是缺陷；但「重跑 Judge 會抹掉 Back-solve 的欄位」這個代價仍在，要留在 Exception Paths。
- 下面「另一件相關的小事」（SkillCompiler-RSDC 的 §2.3 引用）沒有處理。

## 4. 驗證

驗證：

- 重跑 `scan_skill.py`：gen-rsdc-skill 原本 2 筆多寫入者、14 筆讀取較後寫入，現在 0 與 0，另列 2 筆依序編輯的 record 與 1 筆原本樣子的讀取；chinese 原本 1 筆與 6 筆，現在 0 與 0，另列 1 筆依序編輯與 3 筆原本樣子的讀取。
  其餘所有 skill 掃描不出錯，也沒有新增的 Dataflow 問題。
- 反向測試（合成的 skill）：兩個只寫不讀的寫入者仍被列為 `multi_writer_records`；先只寫的建立者加上雙向箭頭的編輯者，列為依序編輯；在建立者之前讀取的 step 仍被列為 `reads_of_later_writes`。
- 用範本填的樣本：single PASS（29 項）、pair PASS（13 項）；所有改過的雙語檔，chinese parity 的結果與 HEAD 相同；`scan_source.py` 對 gen-rsdc-skill、chinese、check-skill 都 valid；`depends_on.py check` 四份範本全部 UNCHANGED。

## 5. 與其他 task 的關係

—

## 6. 知識

—

## 7. 日誌

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-10

- 採用選項 1 的變體：不新增圖上的標記，改用圖上本來就有的雙向箭頭來區分。
- DFD.md、RSDC-Standard.md、check-skill、SKILL template 與兩份 RSDC 範本依此修改，EN 與 tw 一起改。
- 重跑 scan_skill.py 與反向測試，gen-rsdc-skill 與 chinese 的多寫入者及讀取較後寫入都歸零。

### 2026-10-09

- 提出：為 gen-rsdc-skill 的 SKILL.md 加上 Dataflow 後，用 scan_skill.py 檢查時發現多寫入者與往回讀取的問題。
