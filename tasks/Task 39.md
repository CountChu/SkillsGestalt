# Task 39 - 讓 asd-ste 產生 STE 草稿的對照頁

**Status**：完成——2026-10-13 asd-ste 新增 Step 6 - Build the Review Page 與 review builder `make_review.py`；README 列出的檢查與 check-skill 的六項都通過。
**Raised**：2026-10-13，[[Task 32]] 送審 DFD 前手做了一份對照頁，產生的過程與格式都沒有寫在 asd-ste 裡，原型只在 session 的暫存資料夾。
**Depends on**：—

## 1. 背景

背景：Task 32 的「審核」要求送審前先做一份對照頁，逐節並排原文與草稿。
審核 DFD 時，對照頁由 session 暫存資料夾裡的 `make_review.py` 與 `review-script.js` 產生；那個資料夾別的 session 找不到，重開機也可能被清掉。

## 2. 現況

**已決定（2026-10-13）**

- **步驟**：asd-ste 新增 Step 6，接在 Step 5 之後；已有的 11 份草稿以 `run step 6` 補做。
  Task 32 規劃的「取代」一步接在 Step 6 之後。
- **註記**：腳本從 YAML checkpoint 與草稿列出機械項目：STE check 的結果與留下的 warning、technical words、保留原文措辭的陳述。
  agent 照 SKILL.md 規定的格式，補寫要人判斷的地方，行號寫成 `{{en-d:N}}` 這類記號，由腳本變成可點的連結。
- **存放**：對照頁寫在 Checkpoint Dir 的 `step_6-review.html`，例如 `checkpoints/asd-ste/references-DFD/step_6-review.html`，已被 git 忽略；agent 寫的註記是同一目錄的 `step_6-notes.html`。
- **格式**：照 DFD 的對照頁。
  三個頁籤：英文是原文對草稿，逐節；中文是原文中文版對草稿中文版，逐節；逐行是草稿對草稿中文版。
  上方是註記，行號可點，mermaid 區塊可展開，有亮暗兩種配色，介面用繁體中文。
- **缺中文版時**：草稿沒有中文版就停下，說明要先跑 Step 5。
  原檔沒有中文版時同樣停下，說明由 chinese skill 寫；使用者只決定了草稿那一邊，原檔這一邊比照辦理。
- **原型**：直接放進 `asd-ste/scripts/`，照 asd-ste 的 [README.md](../.github/common/skills/asd-ste/README.md) 的 When the Skill Is Changed 走完。
- **依賴**：[[Task 32]] 依賴本 task：本 task 完成之前，Task 32 不審核其餘 10 份草稿；已經送審的 DFD 用手做的對照頁照常審完。
- **commit**：兩個，前綴都是 `task 39`：先提交本 task 的建立，包括 task 檔、摘要表與 Task 32 的依賴；再提交 asd-ste 的修改。

**結果（2026-10-13）**

- `make_review.py`：由原型改寫。
  - 原文與草稿依標題的順序逐節並排，標題不一致時在頁面上標出；第一個標題之前的行，例如 frontmatter，自成一節。
  - 有 frontmatter 時，中文版在它底下多一段指回英文檔的說明；逐行頁略過這一段，行號在斜線後標出中文版的。
  - 腳本列出 STE check 的結果與留下的 warning、header note 的 technical words，以及 `step_2` 記下的保留原文措辭的陳述；沒有 `step_2` 時說明原因。
  - 註記的行號記號指不到任何一行時以 1 結束，不寫出頁面；檔案讀不到，或 checkpoint 沒有 `step_3` 時以 2 結束。
- SKILL.md：新增 Step 6，以及名詞 TW twin、review page、review notes、line reference、review builder；CONFIGURATION、MUST FOLLOW、Step 0 的檔案清單與 Prompt 6 跟著改；Step 5 的收尾移到 Step 6。
  description 加上對照頁之後是 1121 字元，超過 skill loader 的 1024 字元上限；check-skill 的 1.1 抓到，改寫成 1010 字元。
- README.md：Dataflow 加上 Step 6、原檔的中文版、`step_6` 群組與兩個檔案，藍色箭頭重新編號；圖的讀法、Step Purposes、Files Each Step Uses、When the Skill Is Changed 與改完要跑的檢查跟著改。
- 兩份中文版照 chinese skill 只改 change set：`check_parity.py` 都是 0 failure，warning 與修改前相同；`diff_md.py --verify` 都 PASS。
- 檢查：
  - `check_ste.py` 對 DFD.md 的盤點 exit 0，對 DFD.md 與 DFD-ste.md 的檢查 PASS。
  - SKILL、README、ste-custom 三對的 `check_parity.py` 都是 0 failure；`depends_on.py check` 全部 UNCHANGED。
  - check-skill 照 2026-10-12 那次的做法，以 InvestForge 的 `config.yaml` 執行：第一次掃描找到 1.1 的 description 長度，以及 4.1——Step 6 寫 `make_review.py` 而不是 review builder；改好之後六項都通過，Skills Dashboard 的 asd-ste 列已更新。
  - 對 DFD 跑 Step 0、1、3、4、6：YAML checkpoint 有這五個群組，各有 `title` 與 `time`；Step 4 因為 DFD-ste.md 沒有改動而略過。
    `step_6-review.html` 在瀏覽器中打開，點行號會切到對應的頁籤並標亮那幾行。
  - 註記指到 DFD-ste.md 第 154 行時，`make_review.py` 以 1 結束，不寫出頁面。
  - 11 份草稿都能產生頁面，沒有警告。
- DFD 的審核照決定仍用手做的對照頁；Step 6 為 DFD 產生的頁在 `checkpoints/asd-ste/references-DFD/step_6-review.html`，被 git 忽略。
  其餘 10 份的頁還沒產生，[[Task 32]] 等 [[Task 38]] 完成後，再以 `run step 6` 產生。

**後續：上下兩區各自捲動（2026-10-13）**

使用者看過 DFD 的頁之後，要求把頁面分成兩個各自捲動的區域。
問過之後決定：

- 上方是標題、腳本列出的項目與審核重點，下方是頁籤與並排的檔案，兩區各自捲動；點註記裡的行號只捲動下方，註記留在原處。
- 中間的分隔線可以拖曳，也可以用上下方向鍵調整；每次打開時，上方佔視窗高度的 35%，拖曳後的位置不記住。
- 視窗寬度不到 900 像素時，改回整頁一起捲動，這時原文與草稿本來就上下排。
- 只改 `make_review.py` 的版面：SKILL.md 與 README.md 描述的內容沒有變，兩份文件都不動；記進本 task，前綴 `task 39`。

**後續：保留前一個連結的反白（2026-10-13）**

使用者要求點第 2 個行號時，保留第 1 個的反白。
問過之後決定：

- 最多兩組反白：剛點的較深，前一個較淡；點第 3 個時，第 1 個不再標亮。
- 點到已經反白的那一組：捲過去，並讓它變成剛點的，另一組變淡；點的是本來就深的那一組，就只捲過去。
- 註記裡對應的行號連結也標出同樣的深淺，一眼看出每組反白來自哪一則註記。
- 頁籤列右端加一個「清除反白」按鈕，沒有反白時不能按。
- 仍只改 `make_review.py`，記進本 task，前綴 `task 39`。

## 3. 要做的

**要做的**

1. 把原型改寫成 `asd-ste/scripts/make_review.py`：讀四份檔案、YAML checkpoint 與註記，產生對照頁；註記裡的行號記號指不到任何一行時，以 1 結束。
2. SKILL.md 加上 Step 6，以及它用到的名詞、設定與規則；README.md 重畫 Dataflow，補上 Step Purposes、Files Each Step Uses、When the Skill Is Changed 與改完要跑的檢查。
3. SKILL-tw.md 與 README-tw.md 照 chinese skill 的流程跟著改。
4. 跑 README 列出的檢查，並以 `run step 6` 為 DFD 產生一次對照頁。

## 4. 驗證

驗證：在瀏覽器以 1280×800 打開 DFD 的頁，上方 280 像素、下方 510 像素，各自捲動，整頁不捲；點註記裡的行號，上方的捲動位置不變，下方捲到那幾行並標亮；拖曳分隔線、按方向鍵都會改變兩區的大小；700 像素寬時分隔線隱藏，整頁一起捲動。
README 的檢查重跑過：DFD 以 `run step 6` 重新產生頁面，指到第 154 行的註記仍以 1 結束，11 份草稿都能產生頁面；check-skill 六項仍都通過。

驗證：在瀏覽器依序點 DFD 頁的行號，深淺與連結的標示都照上面的規則移動，跨頁籤也保留，「清除反白」全部清掉後按鈕變成不能按。
README 的檢查與 check-skill 都重跑過，結果與上一段相同。

## 5. 與其他 task 的關係

**與其他 task 的關係**

- [[Task 32]]：依賴本 task；對照頁原本是它「審核」的一部分，它規劃的取代一步接在 Step 6 之後，改 asd-ste 時也要照這次的方式重畫 Dataflow。
- [[Task 38]]：也要改 asd-ste，在 `check_ste.py` 加上拼法檢查；後做的在先做的之上改。

## 6. 日誌

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-13

- 提出：Task 32 送審 DFD 前手做了一份對照頁，產生的過程沒有寫在 asd-ste 裡。
- asd-ste 新增 Step 6 與 `make_review.py`，檢查都通過。
- 後續：對照頁分成上下兩區各自捲動，並保留前一個連結的反白。
