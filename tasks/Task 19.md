# Task 19 - 決定 md 檔是否採用每個句子一行的寫法

**Status**：完成——2026-10-13 收尾：範圍內的 md 除了 tools 都已一句一行；tools 由 Task 31 的 STE 版取代，reformat_md.py 的兩個斷句問題由 Task 36 處理。
**Raised**：2026-10-11，把 task-summary.md 的說明文字改成每個句子一行之後提出。
**Depends on**：—

## 1. 背景

提議：md 檔的每一個句子都獨立成一行。
task-summary.md 的導言與圖例已經照這個寫法改了（2026-10-11）。
這個 task 要決定的是：其他 md 檔要不要也這樣寫，範圍多大，用什麼方式做。

**為什麼可能值得做**

- 一個句子一行，改動一句，diff 就只出現那一行。
  現在一個段落是一行，改一個字，整段都顯示為改動，兩個 session 同時改同一段也容易衝突。
- 逐行對照變得容易。
  twin 的規則本來就是「逐行對應英文檔」，句子成為一行之後，英文的一句和中文的一句直接對上，漏譯或多譯一眼看得出。

## 2. 現況

**能否用 reformat-md 完成（2026-10-11 查過）**

- 不能直接完成。
  本 task 先要做上面那些決定，這是判斷，工具做不了。
  reformat-md 也沒有拆句的轉換：它的九個轉換是為了清理從 Word、Docs、NotebookLM、Gemini 貼上的內容。
- 直接拿它處理 repo 的文件會改壞內容。
  在 check-skill 的 `SKILL-tw.md` 副本上跑一次（判定為 clean 模式），它刪掉了 9 處數字：Step 3 Inputs 表格編號欄的 1 到 6、`check 4，` 的 4、inline code `1, 2, 3, 4` 裡的 `2, 3`、fenced 範例裡 `checks 1-4` 的 `1-4`。
  原因是第 9 個轉換把句尾或表格 `|` 前的一兩位數字當成 NotebookLM 的引用編號刪掉，clean 模式也照跑，而且不避開 inline code 與 fenced block。
- 它一次只處理一個檔，輸出成另一份 `#v1` 副本。
  本 task 要的是 EN 與 tw 用同一個規則一起轉，轉完立刻跑 parity 檢查。
- 它可以是做法的一部分。
  它的規則檔已移到 [md-style.md](../.github/common/rules/md-style.md)，正好可以當共用的 md 寫作規則；`reformat_md.py` 也可以加一個拆句的轉換。
  前提是：先做完本 task 的決定；把只適合聊天匯出的轉換（尤其第 9 個）改成選用；並支援 EN 與 tw 成對處理。
- 規則與轉換要一起加。
  reformat-md 的 Step 0 要求 md-style.md 的每一條規則都有對應的轉換，腳本也不能執行規則以外的轉換，否則就停下。
  只在 md-style.md 加一條「每個句子一行」而腳本沒有對應的轉換，reformat-md 就會在 Step 0 停下。

**工具已完成，檔案還沒轉換（2026-10-11）**

- 用 10 組中英檔的副本試跑（`--mode clean`）：每一份都沒有少字或多字，標題不變，重跑結果相同，CRLF 換行也保留。
- 6 組逐段對得上：check-skill 的 SKILL、SKILL-tmp、RSDC-Standard、DFD、gen-rsdc-skill 的 SKILL、check-skill 的 checking-criteria。
- 4 組有譯文句子數與英文不同的段落，要由人調整譯文：
  - RSDC-App-tmp 與 RSDC-Skill-System-tmp 的 2.7 第 8 題：英文一個問句，中文分成兩個。
  - chinese 的 SKILL，Step 3 第 5 項：英文「The pairing line.」獨立成一句，中文用冒號併成一句。
  - SkillCompiler-RSDC 共 6 段，例如第 1 章開頭英文兩句，中文併成一句。

**轉換進度（2026-10-12）**

轉換前問了 8 個問題，決定如下：

- 先轉單一檔與轉完對得齊的中英對照，對不上的 10 組留到譯文調好再轉。
- 那 10 組逐段列出並提出譯文修改，由使用者確認。
- 只因轉換而變更的依賴指紋重記。
- 每批一個 commit。
- 驗證通過就用 `#v1` 取代原檔。
- 中英對照加跑 `check_parity.py`。
- 有其他 session 未 commit 改動的檔先跳過，task 檔放最後一批。
- task 19 維持進行中，直到全部完成。

結果：

- 已轉換並 commit 70 份（git log 中以 `task 19:` 開頭的 commit）：references 3 份、rules 5 份、SKILL-tmp 中英兩份、27 個 skill 的 41 份，以及 tasks/ 的 19 份。
  每一份除了空白和換行，都和轉換前逐字相同，粗體也完好；已轉的檔再轉一次都不會改變。
- 依賴指紋：只重記因這次轉換才變成已變更的記錄，只動到檔頭引用區。
  check-md-deps 對 check-wiki-doc 的 2 筆記錄在轉換前就已變更，維持原樣。
- 轉換中找到並修好三個工具缺陷，都是內容看起來沒變、實際卻壞了：
  - 第 7 個轉換（LaTeX 轉數學式）不避開 inline code，md-style.md 在 inline code 裡示範的跳脫 LaTeX 被轉掉。
    現在含 inline code 的行一律不轉。
  - 第 10 個轉換把中文句號後面緊接的 `**` 一律當成上一個粗體的結尾，例如 `…x。**Dependency Checker**`，斷行後粗體就失效。
    現在追蹤粗體開關，用來開頭的 `**` 歸下一句。
  - 粗體開關原本每行歸零，跨兩行的粗體會被拆壞。
    現在同一段落延續上一行的狀態。
  - check_reformat.py 原本三個都沒抓到。
    現在 clean 模式除了空白，任何字元改變都算失敗，並檢查粗體標記；最先轉好的 35 份也用它重新檢查過，全部通過。

**讓 Claude 在 skill 之外也照 md-style.md 寫（2026-10-12）**

- 問題：只有 reformat-md 與 asd-ste 的流程會讀 [md-style.md](../.github/common/rules/md-style.md)。
  Claude 不透過 skill 寫 md 時，自動載入的 CLAUDE.md 與 memory 都沒提到它。
- 做法：在根目錄 [CLAUDE.md](../CLAUDE.md) 加一條，只放連結，接在 twin 那條之後。
- 措辭：原句「Write every Markdown file of the repo to md-style.md.」可能被讀成「寫進 md-style.md」，也沒說修改時要照做。
  改成「When you create or edit a Markdown file in the repo, follow md-style.md.」，範圍與 md-style.md 的開頭一致。
- 沒有加 hook：靠 Claude 照做，不自動檢查。

**最後 8 組中英對照（2026-10-13）**

轉換前問了 7 個問題，決定如下：

- 中文版的 11 處照提案改：把句子合併或拆開，讓句數和英文一致，意思不變。
- MermaidView-RSDC.md 有 4 句以 ⌘ 或小寫的 mermaid-view 開頭，reformat_md.py 認不出是新句，所以在英文版手動換行。
- Tasks 與 SkillCompiler-RSDC 各有一段用直引號包住兩句的英文訊息，中英兩邊都改成 inline code。
- 兩份 RSDC 範本的第 8 題先只改本 repo，其他 workspace 的文件之後再跟著改。
- 只因轉換而變更的依賴指紋重記。
- 轉換、指紋、task 記錄分成 3 個 commit。

結果：

- 8 組 16 份已轉換並 commit（5edb298）。
  除了上述修改，其餘都只差空白與換行；check_reformat.py 與 check_parity.py 都通過，出現的 WARN 與轉換前相同。
- 依賴指紋重記 10 筆（8ae693d）：gen-rsdc-skill 與 compile-skill 的 SKILL(-tw) 所引用的 SkillCompiler-RSDC，以及 asd-ste、check-skill、gen-skill 的 README(-tw) 所引用的 chinese/SKILL.md。
- reformat_md.py 還有兩處不符合 md-style.md 的規則，這次繞過，沒有修：
  - 直引號 `"…"` 裡的句號會被當成句子結束，但 md-style.md 規定引號內不斷句；它只認得「」這類引號。
  - 以 ⌘ 或小寫名稱開頭的句子，它認不出是新句。

**task 檔與 InvestForge（2026-10-13）**

動手前問了 7 個問題，決定如下：

- Task 33.md 與 Task 34.md 用 reformat_md.py 轉；Task 16.md 有其他 session 未 commit 的改動，等它 commit 後再轉。
- InvestForge 的 InvCov-RSDC 照範本改第 8 題，並重記 `[[RSDC-App-tmp]]` 的指紋。
- InvestForge 的 StopPriceChecker-RSDC 有其他 session 未 commit 的改動，等它 commit 後再改。
- SkillsGestalt 兩個 commit、InvestForge 一個 commit；Task 19 維持進行中。
- reformat_md.py 的兩處問題另開 [[Task 36]]。

結果：

- [[Task 33]] 與 [[Task 34]] 的 3 行已轉成一句一行（497be8e）。
- InvestForge 的 InvCov-RSDC-tw.md 第 8 題照 RSDC-App-tmp-tw.md 改，中英兩份重記 `[[RSDC-App-tmp]]` 的指紋（InvestForge ee3ce1b）。
  check_parity.py 的第 8 題 WARN 已消失，依賴記錄全部 UNCHANGED。
- 其他 workspace 的 RSDC 都沒有引用這兩份範本，不受影響：ArtifactPipe、CompileSkill、EvernoteCli、GeminiChatOrganizer、LlmWikiGenerator，以及 InvestForge 其餘的 7 份。

**收尾（2026-10-13）**

動手前問了 7 個問題，決定如下：

- Task 16.md 裡 10-12 關閉 Task 16 的改動一直沒 commit，先照原樣 commit，再轉其中的 2 行。
- InvestForge 的 StopPriceChecker-RSDC 有 Stop Warning 的改動未 commit，所以以 HEAD 為底組出 blob，只 commit 第 8 題與 `[[RSDC-Skill-System-tmp]]` 的指紋。
- 它的中文版另有 2 條 shared-line WARN（Caller 與「黑色實線」那兩行），來自 Task 32 對範本中文版的修改，留給 [[Task 32]]。
- 每件工作各一個 commit；Task 19 標為完成。

結果：

- Task 16 的關閉照原樣 commit（5a74dca），[[Task 16]] 的 2 行轉成一句一行（baab0b2）。
- InvestForge 的 StopPriceChecker-RSDC-tw.md 第 8 題照 RSDC-Skill-System-tmp-tw.md 改，中英兩份重記 `[[RSDC-Skill-System-tmp]]` 的指紋（InvestForge 7ab1a64）。
  範本英文版在 5edb298 之後只改過檔頭引用區，指紋不受影響，所以這次重記只反映轉換。
  Stop Warning 的改動仍留在工作目錄，沒有動。
- 範圍內的 md 共 152 份，除了 tools 與它的中文版，都已一句一行；本 task 共轉換 89 份。

## 3. 要做的

**需要先弄清楚的**

- **範圍**（2026-10-11 已定）：repo 底下除了 external 目錄以外的所有 md。
  external 目錄指 `.github/external/`，裡面是匯入的第三方 skill；根目錄的 `external/` 只有一份 PDF，沒有 md。
  2026-10-11 時範圍內共 92 份：`.github/common` 70 份、`tasks/` 19 份、`mods/` 2 份、根目錄的 task-summary.md 1 份。
  我抽樣數了幾組文件裡「一行有兩個以上句子」的行數：RSDC 標準與 DFD（4 檔）272 行文字中有 180 行；兩份 RSDC 範本（4 檔）938 行中有 51 行；gen-rsdc-skill 的 SKILL（2 檔）583 行中有 162 行；SkillCompiler-RSDC（2 檔）308 行中有 151 行。
  這是粗略的估算，沒有把縮寫和小數點排除得很準。
  範本的比例低，因為它們本來就是一個段落一行或在約 100 欄折行；標準與 SKILL 的比例高，轉換的改動量大。
- **twin 的逐行對應**：EN 與 tw 的行數必須相同。
  句子拆開後，兩邊同一段的句子數也必須相同，否則行數對不上。
  翻譯時把兩句併成一句、或把一句拆成兩句，現在不會被發現，之後就會讓 parity check 失敗。
  要先決定：這是好事（逼出漏譯）還是負擔？
- **怎麼定義「一個句子」**：中文以「。」「？」「！」結尾；英文以句號、問號、驚嘆號加空白結尾。
  但英文有縮寫（e.g.、i.e.、vs.）、節號與版本號（2.1、261010）、檔名與網址、行內程式碼裡的句點；清單項目、表格的儲存格、標題、引用區塊（`>` 開頭）、程式碼區塊要不要拆；句子中間的冒號與分號不拆。
  這些都要寫成規則，轉換才能用腳本做。
- **顯示**：Markdown 把同一段落裡的單一換行當作空白，預覽時句子會接在一起。
  Obsidian 要把設定裡的 Strict line breaks 關掉，才會照原樣分行；GitHub 與其他預覽器不會。
  如果讀者不只在 Obsidian 看，要決定能不能接受預覽時看不到分行。
- **和現有版面規則的衝突**：RSDC 範本目前的規則是約 100 欄折行（App 範本）或一個段落一行（Skill-System 範本）。
  Task 12 把兩者的版面列為「乙類」差異，當時選的是哪一種，要回頭看，免得這次又改一遍。

**牽涉的檔案（若要做）**

- 規則的寫法：放在哪裡？
  可能是 chinese skill（twin 的版面）、RSDC 標準（文件的寫法），或一份共用的 md 寫作規則，例如 [md-style.md](../.github/common/rules/md-style.md)。
- 檢查：`.github/common/skills/chinese/scripts/check_parity.py` 與 `.github/common/skills/gen-rsdc-skill/scripts/check_rsdc.py` 的 pair 檢查逐行比較行的種類，句子拆開後仍然適用，但兩邊的句子數不同時會報失敗。
  `.github/common/scripts/check_tasks.py` 的圖例檢查只看圖例第一行，不受影響。
- 轉換：一支腳本，依上面的句子定義拆行，並能在 EN 與 tw 兩邊用同一個規則，轉換後立刻跑 parity 檢查。
- 已在 task-summary.md 做的部分：導言兩段與圖例；表格與標題不動。

**做法（2026-10-11 決定：(a)）**

- 規則寫進 [md-style.md](../.github/common/rules/md-style.md)，`reformat_md.py` 完全依照它，新增第 10 個轉換「每個句子一行」。
  句子的定義、哪些地方不拆，以及「twin 與英文檔的句子一對一」都寫在那條規則裡。
  規則寫進去就生效，之後新寫或修改的 md 都照它寫。
- 第 8、9 個轉換（加 inline code、刪引用編號）改成只在 raw 模式執行，第 9 個也不再動 inline code 與表格列。
  repo 裡的檔案一律用 `--mode clean`，因為一個 `*` 條列就會被當成貼上的檔案，raw 模式會把每個標題降一級。
- reformat-md 成對處理中英兩份：由英文檔決定模式，兩份一起轉。
- 新增 [check_reformat.py](../.github/common/skills/reformat-md/scripts/check_reformat.py)，作為 reformat-md 的最後一步。
  它逐字比對原檔與結果，列出每一段少掉或多出的文字，並逐段比對中英兩份的句子行數。

## 4. 驗證

—

## 5. 與其他 task 的關係

交給其他 task 的：

- tools 與它的中文版：由 [[Task 31]] 寫成 STE 之後取代原檔，原檔不必再轉。
- reformat_md.py 的兩個斷句問題：[[Task 36]]。
- StopPriceChecker-RSDC-tw.md 的 2 條 shared-line WARN：[[Task 32]]。

## 6. 知識

—

## 7. 日誌

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-13

- 最後 8 組中英對照轉換並 commit。
- task 檔與 InvestForge 的 RSDC 轉換並 commit。
- 收尾：Task 16.md 與 StopPriceChecker-RSDC 處理完，Task 19 標為完成。

### 2026-10-12

- 已轉換並 commit 70 份。
- 轉換中修好 reformat_md.py 與 check_reformat.py 的三個缺陷。
- 在根目錄 CLAUDE.md 加一條連到 md-style.md 的規則。

### 2026-10-11

- 提出：把 task-summary.md 的說明文字改成每個句子一行之後。
- 決定範圍與做法 (a)：規則寫進 md-style.md，reformat_md.py 新增第 10 個轉換。
- 工具完成，檔案還沒轉換。
