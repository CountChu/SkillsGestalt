# Task 38 - 為英文文件訂下美式拼法的規則與檢查

**Status**：完成——2026-10-13 `check_ste.py` 依共用的 `us-spelling.json` 檢查拼法，md-style.md 新增「Rules checked elsewhere」一節與美式拼法的規則，reformat-md 的 Step 0 不再因它停下，11 份草稿重跑都通過；既有檔案要不要轉換，照決定留到以後（見待決定）。
**Raised**：2026-10-13，[[Task 32]] 審核 DFD 時，範例圖的英式拼法 `Catalogue` 一路留到 STE 草稿；當時定下的防範中，與拼法有關的兩項和一項待決定移到本 task。
**Depends on**：—

## 1. 背景

背景：STE 規則 1.14 要用美式拼法，[ste-rules.md](../.github/common/skills/asd-ste/references/ste-rules.md) 舉的例子是 *Color*、*behavior*、*catalog*；這個 repo 卻沒有拼法的規則，英文檔多半寫成英式。
DFD.md 的範例圖把一份資料叫做 `Catalogue`，asd-ste 寫的草稿沒有改掉它，也沒有報出來：

- 圖在 fenced block 裡，是照抄原文的 kept span，草稿不能改。
- [check_ste.py](../.github/common/skills/asd-ste/scripts/check_ste.py) 略過句中以大寫開頭的字，當它們是名稱或寫成名稱的技術名詞（第 424 行）。

Task 32 已把 DFD 的四份都改成 `Catalog`（SkillsGestalt `4f57e68`）。

## 2. 現況

**結果（2026-10-13）**

- 第一個 commit `98cf26d`：字表與 `check_ste.py`。
  - `us-spelling.json` 有 191 組；腳本替英式與美式加上同樣的 -s、-ed、-ing、-er、-ers 字尾，`not_british` 列出美式也這樣拼的 7 個字形，例如 analyses。
  - `check_ste.py` 新增 `--spelling`：散文裡的報 `[WARN]` 並附美式拼法；kept span 裡的報 `[FAIL]`，說明先改原文；盤點把兩者都列成 `[TODO]`。
    句中以大寫開頭的字也查；header note 列為 technical word 的字、引文與網址不報；英式拼法不再同時報成「not in the dictionary」。
  - asd-ste 的 SKILL.md、README.md 與兩者的中文版，以及 STE rules digest 跟著改：新名詞 US spelling list，Step 0、1、2、3 的說明，Dataflow 多一個 external input 與兩條藍色箭頭，README 的 header quote 記錄 `us-spelling.json`。
  - 順手補上 [[Task 39]] 漏掉的：README 的 Files Each Step Uses，Step 0 的檢查清單少了 `make_review.py`。
- 第二個 commit `a173bc4`：md-style.md 的規則。
  - 新的一節是「Rules checked elsewhere」，規則寫成「Write English in American spelling」，並寫明 `us-spelling.json`、`check_ste.py` 與例外。
  - 中文版、STE 草稿與草稿的中文版跟著改；草稿的 Technical words 加上 proper name、quotation、spelling，並以 `run step 3` 更新 md-style 的 checkpoint。
  - reformat-md 的 Step 0 改成只對照這一節以外的規則；記錄 md-style.md 的 6 份 README 重記。
- 第三個 commit：重跑 11 份草稿時找到的唯一一處 kept span，是 README-tmp 的 placeholder `{WHY_THOSE_STEPS_NEED_JUDGEMENT}`。
  提出本 task 時的掃描沒有把 placeholder 算成 kept span，所以沒列出來。
  照決定先改原文：原文、中文版、草稿與草稿的中文版都改成 `{WHY_THOSE_STEPS_NEED_JUDGMENT}`，只有這四份檔案用到它；記錄 README-tmp.md 的 6 份 README 重記，並以 `run step 3` 更新範本的 checkpoint。
- 驗證：
  - `ed0076e` 的 DFD：檢查在圖裡的 `Catalogue`（第 85 行，fenced block）失敗，並說要先改原文；散文第 105、111 行是 `[WARN]`；盤點把這兩種都列出來。
  - 11 份草稿都通過；原文散文裡的英式拼法照決定不轉換，有 DFD.md 3 處、RSDC-Standard.md 7 處、skill-writing.md 2 處、tools.md 1 處、SKILL-tmp.md 1 處，草稿取代原文時就會消失。
  - reformat-md 的 Step 0：md-style.md 開頭的 8 條規則都對得上轉換，新的一節不在對照範圍，所以不會停下。
  - md-style、md-style 草稿、README-tmp、README-tmp 草稿、asd-ste 的 SKILL 與 README 各對的 `check_parity.py` 都是 0 failure，warning 與修改前相同；`diff_md.py --verify` 都 PASS。
  - `depends_on.py check` 找不到還記著 md-style.md 或 README-tmp.md 舊指紋的文件。
  - check-skill 對 asd-ste 的六項都通過；照 README 對 DFD 加上 `--spelling` 跑過 Step 0、1、3、4、6。

**既有的英式拼法（2026-10-13 掃描）**

用一份常見英式拼法的字表，掃描兩個 repo 由 git 追蹤的英文 md，不含中文版、STE 草稿、`.github/external/` 與 `tasks/`。
字表沒有存進 repo，可能有漏掉的字。
「在 kept span 裡的」是在標題、fenced block、inline code 或連結目標裡的，其餘都在散文裡。

- DFD.md、RSDC-Standard.md、skill-writing.md、tools.md、SKILL-tmp.md 的 14 處，[[Task 32]] 以草稿取代原檔時就會消失。
- SKILL.md 裡的 `Honour` 多半來自 SKILL-tmp.md 的共用句子「Honour a `run step N` selector」，Task 32 的「範本的後續」改共用句子時會一併換掉。
- 中文版：SkillsGestalt 沒有；InvestForge 有 10 份、62 處，多半是照抄英文的名稱，例如 `Page behaviour`，英文檔轉換時照 chinese skill 跟著改，不另列。

**SkillsGestalt**：32 份、166 處，都在散文裡。

| 檔案 | 處數 | 英式拼法 |
| --- | --- | --- |
| `.github/common/references/DFD.md` | 3 | colour 2、catalogue |
| `.github/common/references/RSDC-Standard.md` | 7 | behaviour 5、authorisation、neighbouring |
| `.github/common/rules/skill-writing.md` | 2 | judgement、neighbour |
| `.github/common/rules/tools.md` | 1 | Standardising |
| `.github/common/skills/asd-ste/README.md` | 2 | judgement 2 |
| `.github/common/skills/asd-ste/SKILL.md` | 1 | Honour |
| `.github/common/skills/asd-ste/references/ste-rules.md` | 1 | judgement |
| `.github/common/skills/ask-note/SKILL.md` | 2 | judgement、neighbour |
| `.github/common/skills/check-md-deps/SKILL.md` | 3 | judgement 2、neighbour |
| `.github/common/skills/check-skill/README.md` | 1 | judgement |
| `.github/common/skills/check-skill/SKILL.md` | 3 | judgement 3 |
| `.github/common/skills/check-skill/references/checking-criteria.md` | 7 | colour 2、artefact、behaviour、capitalising、honours、judgement |
| `.github/common/skills/chinese/SKILL.md` | 5 | judgement 3、Honour、neighbour |
| `.github/common/skills/compile-skill/SKILL.md` | 6 | judgement 4、Honour、neighbour |
| `.github/common/skills/compile-skill/references/SkillCompiler-RSDC.md` | 9 | behaviour 4、judgement 3、Behavioural、judgements |
| `.github/common/skills/gen-imp-app/SKILL.md` | 13 | judgement 5、behaviour 4、Honour 2、neighbour 2 |
| `.github/common/skills/gen-rsdc-app/SKILL.md` | 5 | judgement 3、behaviour、neighbour |
| `.github/common/skills/gen-rsdc-app/assets/RSDC-App-tmp.md` | 4 | behaviour 4 |
| `.github/common/skills/gen-rsdc-skill/SKILL.md` | 7 | judgement 3、behaviour、Honour、judgements、neighbour |
| `.github/common/skills/gen-rsdc-skill/assets/RSDC-Skill-System-tmp.md` | 3 | behaviour 2、judgement |
| `.github/common/skills/gen-skill/README.md` | 2 | judgement、judgements |
| `.github/common/skills/gen-skill/SKILL.md` | 1 | neighbour |
| `.github/common/skills/imp-app/SKILL.md` | 14 | judgement 6、behaviour 3、colour、Colour、Honour、honour、neighbour |
| `.github/common/skills/imp-home/SKILL.md` | 9 | judgement 4、behaviour、colour、Colour、Honour、neighbour |
| `.github/common/skills/imp-home/references/Home-RSDC.md` | 10 | behaviour 3、colour 2、memorise 2、specialised 2、initialise |
| `.github/common/skills/imp-home/references/Wireframe.md` | 2 | centred、colour |
| `.github/common/skills/report-my-chats/SKILL.md` | 9 | labelled 3、judgement 2、acknowledgement、Honour、honoured、neighbour |
| `.github/common/skills/write-note-chat/SKILL.md` | 3 | acknowledgements、judgement、neighbour |
| `.github/common/skills/write-note-new-files/SKILL.md` | 1 | judgement |
| `.github/common/skills/write-note/SKILL.md` | 1 | judgement |
| `.github/common/templates/SKILL-tmp.md` | 1 | Honour |
| `mods/mermaid-view/MermaidView-RSDC.md` | 28 | behaviour 8、neighbours 5、colour 4、grey 4、greyed 3、centred 2、Behaviour、colours |

**InvestForge**：29 份、308 處，其中 17 處在 kept span 裡。

| 檔案 | 處數 | 英式拼法 | 在 kept span 裡的 |
| --- | --- | --- | --- |
| `.claude/skills/check-stop-price/SKILL.md` | 5 | judgement 5 | — |
| `.claude/skills/check-stop-price/references/StopPriceChecker-RSDC.md` | 14 | judgement 13、behaviour | — |
| `.claude/skills/extract-filled-orders/SKILL.md` | 6 | labelled 3、judgement 2、neighbour | — |
| `.claude/skills/imp-inv-ctl/SKILL.md` | 10 | behaviour 6、Behaviour、Honour、judgement、neighbour | behaviour |
| `.claude/skills/imp-inv-ctl/references/InvCtl-RSDC.md` | 7 | behaviour 4、recognised、recognises、Recognising | — |
| `.claude/skills/imp-inv-database/README.md` | 1 | analysing | — |
| `.claude/skills/imp-inv-database/SKILL.md` | 8 | behaviour 4、Behaviour、Honour、judgement、neighbour | behaviour |
| `.claude/skills/imp-inv-database/references/InvDatabase-RSDC.md` | 11 | analysed 7、behaviour 3、greyed | — |
| `.claude/skills/imp-inv-database/references/Wireframe.md` | 9 | grey 4、Analysing 3、analysed、coloured | Analysing 3、analysed |
| `.claude/skills/imp-inv-fin-sight/SKILL.md` | 6 | Behaviour、behaviour、Honour、judgement、neighbour、randomised | — |
| `.claude/skills/imp-inv-fin-sight/references/InvFinSight-RSDC.md` | 9 | behaviour 6、artefact、labelled、randomised | behaviour 5 |
| `.claude/skills/imp-inv-fin-sight/references/Wireframe.md` | 5 | grey 5 | — |
| `.claude/skills/imp-inv-tech-rank/README.md` | 1 | colours | colours |
| `.claude/skills/imp-inv-tech-rank/SKILL.md` | 7 | Behaviour、behaviour、behaviours、colour、Honour、judgement、neighbour | — |
| `.claude/skills/imp-inv-tech-rank/references/InvTechRank-RSDC.md` | 21 | colour 13、coloured 3、behaviour 2、cancelling、colours、serialised | — |
| `.claude/skills/imp-inv-tech-rank/references/Wireframe.md` | 15 | colour 5、coloured 2、colours 2、grey 2、greyed 2、cancelling、normalised | — |
| `.claude/skills/report-gross-margin/SKILL.md` | 6 | judgement 3、Honour、Prioritise、Recognising | — |
| `.claude/skills/select-stocks/SKILL.md` | 12 | judgement 8、labelled 2、Honour、neighbour | — |
| `InvCov/docs/InvCov-RSDC.md` | 9 | behaviour 4、analyse、colour、colours、labelled、serialises | analyse |
| `InvCov/docs/Prompts.md` | 5 | labelled 4、analyse | analyse、labelled |
| `InvCov/docs/Wireframe.md` | 6 | colour 2、greyed 2、centre、colours | — |
| `InvDataflow/docs/InvDataflow-RSDC.md` | 35 | catalogue 21、Catalogue 6、behaviour 4、neighbour、neighbourhood、recognised、summarises | catalogue 2 |
| `InvDataflow/docs/Prompts.md` | 18 | catalogue 6、behaviour 2、colour 2、Catalogue、centre、colours、judgement、learnt、neighbourhood、parameterised、travelling | — |
| `InvDataflow/docs/Wireframe.md` | 4 | catalogue 3、behaviour | — |
| `InvHome/docs/Home-RSDC.md` | 10 | behaviour 3、colour 2、memorise 2、specialised 2、initialise | — |
| `InvHome/docs/Wireframe.md` | 2 | centred、colour | — |
| `InvIndexAnalyzer/docs/InvIndexAnalyzer-RSDC.md` | 45 | behaviour 28、colour 5、analysed 4、colours 2、analyse、artefact、authorisation、cancelled、coloured、realisation | — |
| `InvIndexAnalyzer/docs/Prompts.md` | 3 | behaviour 2、totalling | — |
| `InvIndexAnalyzer/docs/Wireframe.md` | 18 | colour 7、emphasised 7、analyse、behaviour、grey、labelled | — |

## 3. 要做的

**已決定（2026-10-13）**

- **範圍**：
  1. `check_ste.py` 加上規則 1.14 的拼法檢查，句中以大寫開頭的字與 kept span 都要查；kept span 裡的，報成「先改原文」。
  2. [md-style.md](../.github/common/rules/md-style.md) 加上「English uses American spelling」一條，它的 STE 草稿 md-style-ste.md 也加；兩者的中文版照 chinese skill 跟著改。
  3. 解決這條規則與 reformat-md 的衝突，見「動手前決定的」。
- **既有檔案**：先不轉換，只把既有的英式拼法列在下方的清單，之後再決定。
- **依賴**：[[Task 32]] 依賴本 task：本 task 完成之前，Task 32 不審核其餘 10 份草稿；已經送審的 DFD 照常審完。
- **留在 Task 32 的**：asd-ste 的 Step 1 發現 kept span 裡有不符 STE 的字就停下，這項防範也管 kind 這類未核准的字，所以仍和 Task 32 其他 asd-ste 的修改一起做。

**動手前決定的（2026-10-13）**

原本待決定的第 1、2 項，以及做法的細節，問過之後決定：

- **與 reformat-md 的衝突**：md-style.md 另立一節「Rules checked elsewhere」，拼法規則放在那裡，並寫明由什麼檢查；reformat-md 的 Step 0 只對照這一節以外的規則。
- **怎麼認出英式拼法**：英美對照字表；-s、-ed、-ing 這些字尾變化由腳本推出。
- **字表**：共用的 `.github/common/references/us-spelling.json`，JSON 不需要中文版；內容是掃描到的字，加上常見的英式拼法。
- **嚴重度**：散文裡的是 `[WARN]`，附上美式拼法；kept span 裡的是 `[FAIL]`，說明要先改原文。
- **例外**：規則寫明引文、專有名詞，以及其他文件或程式碼也用的名稱保留原本的拼法；STE file 的 header note 列為 technical word 的字不報。
- **Step 1 的盤點**：kept span 裡的列成「先改原文」的 `[TODO]`，exit code 不變；Step 1 停下仍是 [[Task 32]] 的防範。
- **commit**：三個，前綴 `task 38`。

**待決定**

1. **既有檔案之後要不要轉換**：本 workspace 的既有檔案；轉換會改到被其他文件記錄的檔案，要重記指紋；kept span 裡的名稱一改，中文版與引用它的地方都要跟著改。

**要做的**

1. 決定原本待決定的第 1、2 項，已在「動手前決定的」。
2. 改 asd-ste：照「改 asd-ste 時」加上拼法檢查，再對 [[Task 31]] 的 11 份草稿與它們的原檔重跑 `check_ste.py`。
   kept span 裡找到的，先改原文，草稿與兩份中文版跟著改，記錄原文的文件重記。
3. md-style.md、md-style-ste.md 與兩者的中文版加上規則，並照「動手前決定的」處理 reformat-md；記錄 md-style.md 的文件重記。

**改 asd-ste 時**

先讀 asd-ste 的 [README.md](../.github/common/skills/asd-ste/README.md) 的 When the Skill Is Changed，照它改 SKILL.md、README.md 與兩者的中文版、`check_ste.py`，並跑它列出的檢查。
reformat-md 沒有 README.md，改它時照 [skill-writing.md](../.github/common/rules/skill-writing.md)。

## 4. 驗證

**驗證**

- 用 `ed0076e` 的 DFD.md 與 DFD-ste.md 測試：拼法檢查要報出圖裡的 `Catalogue`，並說要先改原文。
- 11 份草稿重跑 `check_ste.py`，沒有 FAIL。
- md-style.md 加上規則之後，reformat-md 的 Step 0 不會停下。
- md-style.md 與它的草稿，兩對中英對照的 `check_parity.py` 都是 0 failure；`depends_on.py check` 找不到還記著 md-style.md 舊指紋的文件。

## 5. 與其他 task 的關係

**與其他 task 的關係**

- [[Task 32]]：本 task 的來源；它依賴本 task，本 task 完成之前不審核其餘 10 份草稿。
- [[Task 31]]：產生 11 份草稿；本 task 加上拼法檢查之後，要對它們重跑。

## 6. 日誌

### 2026-10-19

- 「待決定 1」只留本 workspace 的既有檔案，另一個 workspace 的那部分移出本 task（[[Task 62.5]]）。

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-13

- 提出：Task 32 審核 DFD 時，範例圖的英式拼法 `Catalogue` 一路留到 STE 草稿。
- 動手前決定了與 reformat-md 的衝突、字表、嚴重度、例外與 commit 的做法。
- 完成三個 commit：字表與 `check_ste.py`、md-style.md 的規則、README-tmp 的 placeholder。
- 掃描兩個 repo 既有的英式拼法，列成清單。
