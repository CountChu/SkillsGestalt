# Task 32.11 - SKILL-tmp

**Status**：完成——2026-10-19 審核的 48 項全部通過，由 Step 7 取代原檔；SKILL.md 的共用句子交給 Task 70。
**Raised**：2026-10-12，[[Task 32]] 提出時列出的草稿之一，原本是它要做的 2.11。
**Depends on**：[[Task 64]]、[[Task 67]]

## 1. 背景

審核 [[Task 31]] 為 [SKILL-tmp.md](../.github/common/templates/SKILL-tmp.md) 產生的 STE 草稿與草稿中文版；通過就由 asd-ste 的 Step 7 取代原檔與它的中文版。
分工、取代的方式與「每取代一份要一併做的」，見 [[Task 32]]。

## 2. 現況

### 開始時決定的（2026-10-19）

- **MUST FOLLOW 的 run step N 標籤**：寫成「**Honor a `run step N` selector**」，也就是原文名稱的美式拼法。
  原文第 37 行是「Honour …」，草稿原本寫「Obey …」；House Rule 9 與 [[Task 32.10]] 在 ste-custom.md 加上的規則，都要求保留原文的名稱。
  照抄這個標籤的 SKILL.md 有 14 份：本 workspace 8 份（asd-ste、chinese、compile-skill、gen-rsdc-skill、gen-imp-app、imp-app、imp-home、report-my-chats），InvestForge 6 份（imp-inv-ctl、imp-inv-database、imp-inv-fin-sight、imp-inv-tech-rank、report-gross-margin、select-stocks）；先前記的 8 份只數了本 workspace。
  本 workspace 的 8 份由 [[Task 70]] 改成 Honor，InvestForge 的 6 份由那邊自己的 task 處理；report-my-chats 第 165 行的「honoured per **MUST FOLLOW**」指的就是這個標籤。
  另外考慮過的寫法：照原樣寫 Honour 會留一則英式拼法的警告，把它列進技術用字也消不掉，`check_ste.py` 會改報「列了卻沒用到」；維持 Obey 則改掉了名稱。
- **改回原文的字**：草稿是在 run、own、exception、create 收進 ste-custom.md 之前寫的，這些地方改回原文的字。
  run 有 10 行：草稿第 20、49、50、51、61、103、119、131、134、154 行，原本寫 operate、Do、Activate 或 start；第 103 行因此和原文一樣寫成「Run `.venv` first.」。
  own 有 2 行（第 22、57 行），exception 有 1 行（第 60 行，句子縮成 24 字），create 有 1 行（第 149 行）；中文版跟著改了 5 行。
- **標題的 Prompt**：prompt 以名詞收進 ste-custom.md，四個標題維持原樣；它也是 keep-English list 上的 term。
  tw-keep-english.md、README-tmp.md 與本草稿的 Technical words 拿掉 prompt，中文版同步；README-tmp 等 [[Task 32.10]] 提交取代之後才改，記錄它的 6 份 README 跟著重記。
- **中文版的 pairing line**：草稿中文版第 6 行連到 SKILL-tmp-ste.md，`draft.py replace` 不會改它，取代之後會連到已刪除的草稿；另開 [[Task 67]] 修 draft.py，Step 7 要等它做完。
- **對照頁**：標出原文哪些句子被各 skill 的 SKILL.md 照抄、各有幾份，取代之後照它做「範本的後續」。
  另外兩句開啟清單項目的粗體句（原文第 41、45 行）是指示句，不是名稱，維持改寫。

### 取代時決定的（2026-10-19）

- **gen-skill**：它的 Step 3 規定，沒有 YAML checkpoint 時拿掉「the one-writer-per-JSON line」；新範本把這一條拆成兩個清單項目，照原句只會拿掉第一項。
  改成連同緊接在後、說明其原因的那一項一起拿掉，和取代一起做。
- **範本的後續**：SKILL.md 的共用句子另開 [[Task 70]]，和處理 README 的 [[Task 66]] 分開；Task 70 列出範本句子與照抄的 skill，各檔的行號開始做時再算。
- **[[Task 32]]**：11 份草稿都審完並取代，標成完成；範本的後續連同它的驗證交給 [[Task 66]] 與 [[Task 70]]。

### 進度

- 2026-10-18 [[Task 32.10]] 把 run 收進 ste-custom.md：草稿與中文版的 Technical words 拿掉 run，Step 3 重跑 PASS，沒有警告，`[[ste-custom]]` 重記。
- 2026-10-19 照上面的決定改了草稿與中文版。
  Step 1 重跑，清冊不再問 Prompt；Step 3 PASS，沒有警告，PDF 與 `[[ste-custom]]` 重記。
  Step 6 產生對照頁送審：13 項註記、48 個審核項目、183 個行號連結，在 review server 的 `templates-SKILL-tmp/`。
- 2026-10-19 使用者審核的 48 項全部是 [v]，草稿通過；[[Task 64]] 與 [[Task 67]] 都已完成。
  Step 7 以草稿取代原檔與中文版：檔頭註記刪成兩行，中文版的 pairing line 指回 SKILL-tmp.md，兩份草稿刪除。
  記錄 SKILL-tmp.md 的 6 份 README（asd-ste、check-skill、gen-skill 與它們的中文版）只引用範本的標題與結構，讀過仍成立，已重記；InvestForge 沒有記錄它的檔案。
- 2026-10-19 gen-skill 的 Step 3 照上面的決定改了，中文版照 chinese skill 跟著改。

## 3. 要做的

- ✅ 2.11 SKILL-tmp——2026-10-19 審核通過，由 Step 7 取代原檔。

「範本的後續」中 SKILL.md 的部分交給 [[Task 70]]，README 的部分在 [[Task 66]]。

## 4. 驗證

- 取代之後：`check_ste.py --ste` PASS，沒有警告；SKILL-tmp 兩份的 `check_parity.py` 0 failure；6 份 README 的 `depends_on.py check` 中 SKILL-tmp.md 都是 UNCHANGED。
- gen-skill：SKILL.md 與 README.md 兩對的 `check_parity.py` 0 failure，警告和改之前相同；`diff_md.py --verify` PASS；README 的 `depends_on.py check` 都是 UNCHANGED；check-skill 的 `scan_skill.py` 沒有缺少的標題，leftovers 都是 gen-skill 說明 placeholder 時原本就寫的。

## 5. 與其他 task 的關係

- [[Task 64]]：gen-skill 抄範本時不帶 STE 檔頭，本草稿取代原檔之前要先做完。
- [[Task 67]]：draft.py replace 把中文版的 pairing line 指回原檔，本草稿取代原檔之前要先做完。
- [[Task 32.10]]：README-tmp 的草稿，有同樣的 gen-skill 問題；run 在那裡收進 ste-custom.md，保留名稱的規則也在那裡建立。
- [[Task 70]]：SKILL.md 的共用句子換成 STE 範本的寫法，本草稿取代之後提出。
- [[Task 66]]：README 的共用句子換成 STE 範本的寫法；SKILL.md 的部分由 [[Task 70]] 處理。
- [[Task 38]]：定下美式拼法的規則，既有檔案的英式拼法留到以後處理；SKILL.md 裡的 Honour 標籤由 [[Task 70]] 改成 Honor。

## 6. 日誌

### 2026-10-19

- 記下開始時要決定的 MUST FOLLOW 標籤：保留 run step N 的名稱，列出三種寫法與各自的影響；Status 行、要做的與關係跟著補上。
- 開始審核：標籤寫成 Honor，草稿改回 run、own、exception、create，prompt 收進 ste-custom.md，另開 [[Task 67]] 修 draft.py 的 pairing line；照抄標籤的 SKILL.md 改記為 14 份，含 InvestForge 6 份。
- 重跑 Step 1、3，Step 6 產生對照頁送審；README-tmp 與 tw-keep-english 拿掉 prompt，README-tmp 的 6 份依賴重記；Depends on 加上 [[Task 67]]，關係加上 [[Task 66]]。
- 照 keep-English list，4 處譯成中文的 pairing line 改成英文，意思沒有改（[[Task 68]]）。
- 審核通過，48 項全部是 [v]；Step 7 取代原檔與中文版，6 份 README 重記，檢查都通過；gen-skill 的 Step 3 照新範本改成拿掉兩個 one-writer 的清單項目。
- SKILL.md 的共用句子交給新開的 [[Task 70]]；本 task 完成。

### 2026-10-18

- 從 [[Task 32]] 拆出：原本是它要做的 2.11；屬於這份檔案的內容搬到這裡，內容沒有改。
- [[Task 32.10]] 把 run 收進 ste-custom.md，草稿與中文版的 Technical words 拿掉 run，Step 3 重跑 PASS；Depends on 加上 [[Task 64]]。

### 2026-10-12

- 列為 [[Task 32]] 要審核的草稿之一。
