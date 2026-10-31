# Task 32 - 人工審核 STE 草稿，通過後由 asd-ste 取代原檔

**Status**：完成——2026-10-19 11 份草稿都審核通過，並由 asd-ste 的 Step 7 取代原檔；範本的後續交給 [[Task 66]]（README）與 [[Task 70]]（SKILL.md）。
**Raised**：2026-10-12，從 [[Task 31]] 拆出：使用者決定 Task 31 只產生 STE 草稿，人工審核與審核通過後的取代歸本 task，取代由 asd-ste 新增的一步執行。
**Depends on**：[[Task 31]]、[[Task 38]]、[[Task 39]]

## 1. 背景

背景：asd-ste 現在把 STE 版寫在原檔旁邊，檔名在 `.md` 前面插入 `-ste`，寫完就留著，不會取代原檔。
它的 SKILL.md 與 README.md（含中文版）把 `-ste` 檔當成產出：用「`DFD.md` 變成 `DFD-ste.md`」當範例，README 的「改完要跑的檢查」也拿 DFD.md 與 DFD-ste.md 當測試材料。
使用者決定：`-ste` 檔只是給人審核用的暫存草稿，審核通過之後就成為原檔。

## 2. 現況

### 審核時決定的

**審核時決定的（2026-10-13）**

- **防範**：asd-ste 的 Step 1 發現 kept span 裡有不符 STE 的字，就停下：先改原文，再重跑；和本 task 其他 asd-ste 的修改一起做。
  另外兩項——`check_ste.py` 的拼法檢查與 md-style.md 的美式拼法規則——連同它們與 reformat-md 的衝突，2026-10-13 移到 [[Task 38]]。
- **其他中文版的 role 與 system**：現在就轉換。
  只改英文對應的那一行（逐節對應的中文版則是那一節）也寫 system 或 role 的地方；作業系統、檔案系統、系統時鐘等複合詞照舊；英文沒寫的，改成英文用的詞；英文寫 roles、systems 時，中文版也寫原形 role、system。
  別的 session 正在處理的中文版先跳過：RSDC-Standard 的兩份中文版，以及 InvestForge check-stop-price 的 SKILL-tw.md 與 StopPriceChecker-RSDC-tw.md。
- **House Rule 7**：ste-rules.md 的這一條只管原文自己的 twin 與 version，例子換成 tw-keep-english 的版本行。
  「This document」照舊，因為草稿說的是同樣的內容；工具要讀的 Version 行是例外，例如 `check_rsdc.py --standard` 讀的 RSDC-Standard.md，版本號緊接在「**Version**:」之後。
  House Rule 5 的檔頭註記範例也換成 DFD 草稿清單裡現有的字；ste-rules.md 改了，SKILL.md 與 SKILL-tw.md 的檔頭重記。
- **轉換改錯的譯法**（2026-10-14）：2026-10-13 把中文版的「角色」「系統」改回 role、system 時，英文那一行本身就寫著這兩個中文詞的地方也被改了。
  改錯的是 tw-keep-english-tw.md 與草稿中文版表格的 role、system 兩列（Replaces、Flagged 與「系統太常見」），以及 MermaidView-RSDC-tw.md 第 621 行——英文版那一格寫的就是「追到外部角色（六角形）就停」。
  審 tw-keep-english 之前，三份都改回原來的中文；英文檔裡寫著這兩個中文詞、又有中文版的，只有這三份的英文版。
  `check_parity.py --keep` 因此在這三行各報一則「角色」的 WARN；那一行寫的就是譯法本身，照舊由人判斷。

### 改 asd-ste 時決定的

**改 asd-ste 時決定的（2026-10-13）**

原本的五項待決定都在這一天決定，並照它們改了 asd-ste：

1. **測試材料**：README 的「改完要跑的檢查」改用 git 裡固定的版本——commit `1710643` 的 DFD.md 與它的草稿（使用者核准的那一版），以 `git show` 寫到 repository 以外或 git 忽略的目錄再跑；`ed0076e` 那一組照舊。
2. **辨認已經是 STE 的原檔**：看檔頭——header quote 宣告了 `[[ASD-STE100_ISSUE9.pdf]]` 的，就是 STE file，Step 0 拒收；草稿本身也因此被拒收。
3. **之後的檢查**：`check_ste.py` 加上只給 `--ste` 的用法，不需要原文，檢查程式能量測的規則、檔頭與 kept span 的拼法。
4. **取代時檔頭的 `[[ste-custom]]`**：保留，`ste-custom.md` 改了，`depends_on.py check` 才會提醒重新檢查。
5. **技術用字的定義**：SKILL.md、它的中文版與 House Rule 6 都補上規則 1.3：核准字用在字典沒給的技術意思時，也要列為技術用字。

一併照先前的決定做的：

- **文件不提 `-ste`**：SKILL.md、README.md 與兩者的中文版把草稿稱為 draft；草稿的路徑由新的 `draft.py paths` 算出，只有這支腳本知道草稿的檔名。
- **新增 Step 7 - Replace the Source**：問審核結果；通過就由 `draft.py replace` 把草稿與它的中文版寫回原檔名，檔頭註記刪成兩行（House Rule 5），再刪掉草稿；接著以 `draft.py dependents` 找出記錄原檔的文件，讀過改動後重記，最後跑 `check_ste.py --ste`、parity check 與 `depends_on.py check`。
  改 task 檔的連結、reformat-md 的 Step 0 與 commit 仍由本 task 手動做。
- **防範（Step 1 停下）**：kept span 裡有英式拼法時，清冊的 verdict 是 `SOURCE-FIRST`，以 `3` 結束，Step 1 停下，先改原文。
  標題裡字典不核准、而且在任何詞性都不核准的詞，清冊列成「要判斷」：腳本分不出詞性，例如 *file* 當名詞是技術名詞，當動詞才違反 STE，所以由 Step 1 判斷；用在不核准的詞性或意思上，就和 `SOURCE-FIRST` 一樣停下。

### 進度

**進度**

- 其他中文版的「角色」「系統」：2026-10-13 轉換完成，SkillsGestalt 19 份、122 處，InvestForge 5 份、12 處。
  InvDataflow-RSDC-tw.md 表格第 4 列的兩處，英文寫的是 app，就改成 app；InvHome 的 Home-RSDC-tw.md 不是逐行對應，那一行手改。
  每一份的 `check_parity.py` 和轉換前比，沒有新的 failure 或 warning，「角色」的 WARN 都消失；InvestForge 原本就有 failure 的 4 份，failure 也和轉換前一樣。
  RSDC-Standard 的兩份中文版先跳過，同日在本 session 接手轉換：RSDC-Standard-tw.md 53 處，第 297 行的「系統外部」英文只寫 outside，改成「來自外部」；RSDC-Standard-ste-tw.md 85 處，粗體記號前的兩處補上空格。
  兩對的 `check_parity.py` 和轉換前比，只少了「角色」的 WARN；對照頁以 「O - Task 38」 原本的註記重建。
  跳過的那兩份不在本 workspace，2026-10-19 移出本 task（[[Task 62.5]]）。
  2026-10-14 發現 3 份共 5 行改錯：英文那一行本身就寫著「角色」或「系統」，已改回，見「審核時決定的」；上面說「角色」的 WARN 都消失，其中 tw-keep-english 那兩份就是這個錯造成的。
- asd-ste：2026-10-13 改完，README 列出的檢查都跑過——SKILL.md、README.md 與兩者的中文版 `check_parity.py` 0 failure，`depends_on.py check` 都是 UNCHANGED，check-skill 的 `scan_skill.py` 找不到沒畫到的 step、多寫入者的 record 或沒用到的術語，以 `1710643` 的 DFD 副本跑過 Step 0、1、3、4、6。
  新的標題詞檢查在其他原文找到要判斷的詞，審那幾份時要看：RSDC-Standard 的 way（One-way）與 Design，tw-keep-english 的 list，report-md-rules 的 Create 與 file，scratch-rules 的 File，tools 的 Search 與 need，README-tmp 的 Runs 與 Files，SKILL-tmp 的 Prompt。
- 其餘 10 份：2026-10-13 決定等 [[Task 38]] 加上拼法檢查、重跑過 `check_ste.py` 之後再審。
  同一天也決定等 [[Task 39]] 讓 asd-ste 能產生對照頁；DFD 用手做的對照頁照常審完。
  兩個 task 同日都已完成：11 份草稿加上拼法檢查重跑都通過；唯一一處 kept span 裡的英式拼法是 README-tmp 的 placeholder，四份檔案都已改成 `{WHY_THOSE_STEPS_NEED_JUDGMENT}`。

## 3. 要做的

### 已決定

**已決定（2026-10-12）**

- **分工**：本 task 逐份審核 [[Task 31]] 產生的草稿與它的中文版；通過的，由 asd-ste 新增的一步取代原檔，再做取代後的後續。
- **審核**：逐份進行；送審前先做一份對照頁，逐節並排原文與草稿。
  2026-10-13 決定對照頁由 asd-ste 新增的 Step 6 產生，見 [[Task 39]]。
- **asd-ste 的修改**：
  - **文件不提 `-ste`**：草稿仍寫在原檔旁邊，`-ste` 只出現在腳本裡，由腳本算出草稿的路徑；SKILL.md 與 README.md（含中文版）只稱它為「待審的草稿」。
  - **新增取代的一步**：問使用者審核結果，通過就以草稿取代原檔。
    這一步接在 [[Task 39]] 新增的 Step 6 之後，也就是產生對照頁之後。
  - **草稿的中文版**：和草稿放在一起，由 chinese skill 照草稿逐行寫成；取代時一起寫回原檔的 `-tw.md`。
- **取代的方式**：草稿的內容寫回原檔名，草稿的中文版寫回 `-tw.md`，再刪掉草稿。
  檔頭保留 PDF 那一行依賴，註記只留「本檔以 ASD-STE100 STE Issue 9 寫成」與 `Technical words:` 兩行，拿掉指向原檔的連結與「以原檔為準」；中文版同步。
- **每取代一份要一併做的**：
  - 重記依賴它的指紋：先找出所有在檔頭引用區記錄它的文件，包括其他 workspace（例如 InvestForge）裡的文件——[[Task 19]] 轉換 DFD.md 時就漏掉了 InvestForge 的一對，見 [[Task 18]]。
    2026-10-12 時，記著 DFD.md 的有 14 份：兩份 RSDC 範本與它們的中文版，asd-ste、check-skill、gen-skill 的 README 與中文版，InvestForge 的 StopPriceChecker-RSDC 與 InvCov-RSDC 與它們的中文版；記著 RSDC-Standard.md 的是其中 8 份（範本與 InvestForge 的 RSDC）。
    指紋不含檔頭引用區，所以重記只動到這些文件的檔頭，不會一路連鎖下去。
    讀過改動、確認那些文件仍然成立，再用 `depends_on.py record` 重記。
  - 取代 RSDC-Standard 時，Version 行要寫成「**Version**: 261010.」這樣，版本號緊接在後面，`check_rsdc.py --standard` 才讀得到；引用它節號的 skill 與範本要對一次。
  - 跑檢查：中英對照的 `check_parity.py`、`check_ste.py`，取代 RSDC-Standard 時再跑 `check_rsdc.py --standard`，以及受影響文件各自的檢查。
  - 取代 md-style.md 之後，跑一次 reformat-md 的 Step 0：它逐條對照 md-style.md「Transforms applied by reformat_md.py」一節的 10 個編號與腳本的轉換，對不上就停下（見 [[Task 31]] 的 2.6）。
  - 指向被刪掉之草稿的連結要改掉，check_tasks 才不會報斷掉的連結：Task 23.md 的 4 個連結改成行內程式碼；[[Task 31]] 表格裡的草稿連結，改成標明已取代。
  - 取代與重記產生的修改，兩個 repo 各一個 commit，前綴 `task 32`。
- **範本的後續**：asd-ste 取代 README-tmp 與 SKILL-tmp 之後，所有 skill 的 SKILL.md 與 README.md 裡照範本抄的共用句子也要跟著改。
  先列出受影響的 skill 與句子，由使用者決定一次改完或分批；中文版照 chinese skill 的流程跟著改。
  2026-10-19 [[Task 32.11]] 決定 SKILL-tmp 的 MUST FOLLOW 標籤寫成「Honor a `run step N` selector」：照抄舊標籤「Honour …」的 14 份 SKILL.md 要一起改成 Honor，其中 6 份在 InvestForge，屬於那個 workspace 自己的 task。
  2026-10-19 本 task 完成時，範本的後續連同它的驗證交給 [[Task 66]]（README 的共用句子）與 [[Task 70]]（SKILL.md 的共用句子）。
- **驗證**：每取代一份，`depends_on.py check` 找不到還記著舊指紋的文件；中英對照的 `check_parity.py` 0 failure；`check_ste.py` 沒有 FAIL。
  範本的後續做完之後，check-skill 掃描所有 skill，沒有新的 issue；2026-10-19 起由 [[Task 66]] 與 [[Task 70]] 做這項驗證。

### 要做的

**要做的**

1. ✅ 改 asd-ste（2026-10-13），見「改 asd-ste 時決定的」。
2. 逐份審核 Task 31 交來的草稿：以 Step 6 產生對照頁，送使用者審核；通過就打 ✅，子項的編號固定不變。
   - [[Task 32.1]] ✅ DFD
   - [[Task 32.2]] ✅ RSDC-Standard
   - [[Task 32.3]] ✅ tw-keep-english
   - [[Task 32.4]] ✅ md-style
   - [[Task 32.5]] ✅ report-md-rules
   - [[Task 32.6]] ✅ report-yaml-rules
   - [[Task 32.7]] ✅ scratch-rules
   - [[Task 32.8]] ✅ skill-writing
   - [[Task 32.9]] ✅ tools
   - [[Task 32.10]] ✅ README-tmp
   - [[Task 32.11]] ✅ SKILL-tmp
3. 通過的，由 asd-ste 取代原檔，再做「每取代一份要一併做的」：DFD ✅ 2026-10-13，RSDC-Standard ✅ 2026-10-14，md-style ✅ 2026-10-14，tw-keep-english ✅ 2026-10-18，report-md-rules ✅ 2026-10-18，report-yaml-rules ✅ 2026-10-18，scratch-rules ✅ 2026-10-18，skill-writing ✅ 2026-10-18，tools ✅ 2026-10-18，README-tmp ✅ 2026-10-19，SKILL-tmp ✅ 2026-10-19。
4. ✅ README-tmp 與 SKILL-tmp 取代之後，做「範本的後續」：2026-10-19 交給 [[Task 66]]（README）與 [[Task 70]]（SKILL.md）。

### 改 asd-ste 時

**改 asd-ste 時**

先讀 asd-ste 的 [README.md](../.github/common/skills/asd-ste/README.md) 的 When the Skill Is Changed，照它改 SKILL.md、README.md 與兩者的中文版、`check_ste.py`、`save_step.py`，並跑它列出的檢查。

## 4. 驗證

—

## 5. 與其他 task 的關係

**與其他 task 的關係**

- [[Task 31]]：本 task 依賴它——審核的草稿由它產生。
- [[Task 38]]：本 task 依賴它——美式拼法的規則與檢查，2026-10-13 從本 task 審核 DFD 時定下的防範移過去；它完成之前，DFD 以外的草稿不審核。
- [[Task 39]]：本 task 依賴它——對照頁改由 asd-ste 的 Step 6 產生；它完成之前，DFD 以外的草稿不審核。
- [[Task 24]]：依賴本 task——它要照 README-tmp.md 為 27 個 skill 寫 README.md，等範本取代、後續做完之後再寫，才不必重改一次。
- [[Task 18]]、Task 30：DFD 與 RSDC-Standard 被取代之後，它們對齊的文件記的指紋要重記。
  兩份都已取代，記錄它們的文件都已重記（2026-10-13、2026-10-14）。
- [[Task 23]]：建立 asd-ste。
- [[Task 26]]：決定 ASD-STE100 的 PDF 是否留在 git；取代後的檔頭仍連到它。
- [[Task 66]]、[[Task 70]]：本 task 完成時，範本的後續交給它們，README 與 SKILL.md 各一個。

## 6. 知識

—

## 7. 日誌

### 2026-10-19

- [[Task 32.10]] README-tmp 審核通過，由 Step 7 取代原檔；Status 行補上 README-tmp，剩 1 份。
- [[Task 32.11]] SKILL-tmp 的草稿送審，子項清單的圖示改成 🔄；「範本的後續」補上 MUST FOLLOW 標籤改成 Honor 的 14 份 SKILL.md。
- 「進度」裡跳過、之後要轉的那兩份中文版不在本 workspace，移出本 task，下一行的提醒也一起移出（[[Task 62.5]]）。
- [[Task 32.11]] SKILL-tmp 審核通過，由 Step 7 取代原檔；11 份草稿都審完並取代，本 task 完成，範本的後續交給 [[Task 66]] 與 [[Task 70]]。
- 要做的第 3 項補上 skill-writing、tools、README-tmp 與 SKILL-tmp 的取代日期，Status 行改寫成完成的結論。

### 2026-10-18

- 把要做的 2.1–2.11 拆成 sub task [[Task 32.1]]–[[Task 32.11]]，屬於各份檔案的內容搬過去，內容沒有改。
- [[Task 32.5]] report-md-rules 審核通過，由 Step 7 取代原檔。
- [[Task 32.6]] report-yaml-rules 審核通過，由 Step 7 取代原檔。
- [[Task 32.7]] scratch-rules 審核通過，由 Step 7 取代原檔；Status 行補上 32.6 與 32.7，剩 4 份。
- [[Task 32.8]] skill-writing 審核通過，由 Step 7 取代原檔；Status 行補上 32.8，剩 3 份。
- [[Task 32.9]] tools 審核通過，由 Step 7 取代原檔；Status 行補上 32.9，剩 2 份。
- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。
- 指向 Task 30 的 wikilink 改成純文字：它已移出本 workspace（[[Task 62.4]]）。

### 2026-10-17

- [[Task 50]]：ste-custom.md 加上 Rules 一章，第一條是不用雙重否定；8 份草稿重跑 Step 3 都 PASS，2.3 的對照頁重建，tools 的草稿（2.9）第 24 行改成肯定句。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-14

- RSDC-Standard 與 md-style 審核通過，由 Step 7 取代原檔。
- tw-keep-english 與 report-md-rules 產生對照頁送審。
- 發現 3 份中文版的「角色」「系統」轉換改錯，已改回。

### 2026-10-13

- asd-ste 加上取代的一步（Step 7），待決定的五項都已決定。
- 其他中文版的「角色」「系統」轉換完成。

### 2026-10-12

- 從 Task 31 拆出，決定審核與取代的分工和方式。
