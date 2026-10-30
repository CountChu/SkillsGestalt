# Task 23 - 建立 asd-ste skill：把 Markdown 改寫成 ASD-STE100 STE

**Status**：完成——2026-10-12 待辦都做完或移出：STE 檔重驗與 RSDC-Standard-ste.md 重跑已完成，另兩項移到 [[Task 26]]、[[Task 27]]。
**Raised**：2026-10-11，補記建立 asd-ste skill 的那個 session 所做的工作。
**Depends on**：—

## 1. 背景

背景：使用者先請 Claude 依 ASD-STE100 Simplified Technical English（STE）Issue 9，把 [RSDC-Standard.md](../.github/common/references/RSDC-Standard.md) 改寫成 STE 版，再用 gen-skill 把這個做法建成 skill。
`/asd-ste` 接受路徑、檔名或不含 `.md` 的名稱，在原檔旁寫出 `<name>-ste.md`。
那個 session 在 Claude Code 中進行，無法直接呼叫 gen-skill，所以照 [gen-skill 的 SKILL.md](../.github/common/skills/gen-skill/SKILL.md) 手動執行，並依使用者的要求，在建立過程中問了 12 個問題。

## 2. 現況

**已決定（2026-10-11）**

- 輸出只有 `<name>-ste.md`，不寫 MD report。
  YAML checkpoint 是同一個 session 之後加上的，見本節最後一項。
- `config.yaml` 可省略：沒有時，以 skill 目錄往上兩層的目錄作為 `{skillGroups.common}`。
- 字典 JSON 從 PDF 抽出，只含詞、詞性、詞形與替換詞，commit 進 git，所以執行時不讀 PDF 的內容。
  只有 Step 3 由 `depends_on.py` 讀 PDF 的位元組來算 fingerprint；找不到 PDF 時，header quote 的那一行不記錄。
- STE file 已存在時，先詢問，同意後整份重寫。
- 所有 `#` 標題原樣保留。
- 檔頭的 header quote 只列 PDF，也就是 `[[ASD-STE100_ISSUE9.pdf]]`，日期與 fingerprint 由 `depends_on.py record` 寫入；原檔不列為依賴。
- 檔頭的 header note 連回原檔，並以 `Technical words:` 一行列出用到的 technical word。
- 結尾提議 commit，以及請 chinese skill 產生 `-ste-tw.md`。
- scripts 完整實作，不只建 placeholder。
- 只在 VS Code 使用，不建 Claude Code 的 symlink。
- 擴充 `depends_on.py` 以支援 PDF，而不是讓 asd-ste 自己計算 fingerprint。
- SKILL.md 產生繁體中文 twin。
- YAML checkpoint：使用者之後要求執行時要有 YAML checkpoint，又決定了下列各項。
  - 每份原文一個目錄 `checkpoints/asd-ste/{上層目錄}-{name}/`，每次執行都重用，不照 repo 慣例每次執行另開一個 `{target}-{yymmdd-hhmm}` 目錄。
    目錄名一律加上上層目錄，以區分不同目錄的同名原文，例如各 skill 的 `SKILL.md`。
  - `run step N` 照範本，從 checkpoint 讀前面 step 的輸出。
  - 每個 step 存完整清單，由 script 產生並合併進 checkpoint。
  - `check_ste.py` 的完整輸出另存成文字檔。
  - 提早停止的執行，例如拒絕原文、NOT-ENGLISH 或不同意覆寫，也寫 checkpoint，記下停在哪裡與原因。

**做了什麼**

- `3245c36`：[depends_on.py](../.github/common/scripts/depends_on.py) 支援 PDF。
  `[[名稱.副檔名]]` 找不到 `名稱.md` 時，直接找同名的檔案；不是 UTF-8 文字的檔案，以整個檔案位元組的 SHA-256 取 fingerprint；`.md` 的算法不變。
- `9d5558f`：建立 [asd-ste](../.github/common/skills/asd-ste/SKILL.md)，含 SKILL-tw.md、[check_ste.py](../.github/common/skills/asd-ste/scripts/check_ste.py)、字典 JSON 與 [ste-rules.md](../.github/common/skills/asd-ste/references/ste-rules.md)。
  `check_ste.py` 盤點原文，並檢查 STE file：kept span、句長（指示句 20 字、描述句 25 字）、每段 6 句、每行一句、分號、縮約形，以及逐詞比對字典。
  `ste-rules.md` 是以自己的話寫的規則摘要，加上 House Rules。
- STE 版文件：
  - `RSDC-Standard-ste.md` 是那個 session 在 skill 建立之前手寫的；它在 2026-10-14 經 [[Task 32]] 審核後取代了 RSDC-Standard.md。
    之後整理成每句一行、加上 twin，並以 `977fdf7` commit，這些都不是那個 session 做的。
  - `DFD-ste.md`（`5c98468`）是用 asd-ste 實測產生的；它在 2026-10-13 經 [[Task 32]] 審核後取代了 DFD.md。
    它的 twin 由其他 session 加入（`8ec2e1f`），之後兩者一起修正（`201d446`、`60e9538`）。
- PDF 轉 MD 的試行與撤回：
  - `6ec542c` 把規格轉成兩份 MD，放在 `external/`、不進 git，讓 Step 2 與 Step 3 查詢核准意義與例句。
    同一份解析也重建了字典 JSON：核准詞依詞性計算是 877 個，比字典介紹頁寫的 875 個多兩個，多出的兩個是先前漏抓的詞條。
  - 使用者之後決定刪除這兩份 MD，並移除查詢功能（`4c2ed8b`）。
    `convert_spec.py` 改為只產生字典 JSON，而且與先前的 JSON 逐位元組相同。
- `910f3d8`：每個 step 把輸出存進 YAML checkpoint，決定見「已決定」的最後一項。
  新增 [save_step.py](../.github/common/skills/asd-ste/scripts/save_step.py)，把一個 step 的 group 合併進 `process.yaml`，並從系統時鐘取結束時間、算出耗時；`check_ste.py` 新增 `--report` 與 `--findings`，把完整輸出與 findings JSON 存在 checkpoint 旁。
  在 DFD 上逐一實跑 `run step 0`、`1`、`3`、`4`，後面的 step 都從 checkpoint 讀到前面的輸出，Step 3 的結果是 PASS。
- `2190697`：讓修改 skill 的 agent 先讀 README.md，加了三個指引：asd-ste 的 README.md 開頭一句、[skill-writing.md](../.github/common/rules/skill-writing.md) 的第一條規則，以及新的 [CLAUDE.md](../.github/common/skills/CLAUDE.md)，各項決定記在 [[Task 20]]。
- 2026-10-12，完成原本的待辦 1、2：
  - `684260d`：以 `/asd-ste RSDC-Standard` 重跑 `RSDC-Standard-ste.md`，以舊版為底稿，逐段對照原文。
    依 House Rules 補上 header quote 與 header note，把 twin、版本與檔名都說成 RSDC-Standard.md 的，並改正原本沒過的 5 項檢查。
    逐段對照時，也補回舊版漏掉或改變的陳述，並讓一個名稱只指一件事。
    `check_ste.py` 第 5 次執行通過，header quote 記錄了規格的 fingerprint `d1f4ea9e7cd6`，header note 列出 127 個 technical word。
    剩下 4 個被動語態警告，都在照原文保留的粗體標題中（House Rule 9）。
  - `2da3e93`：chinese skill 增量更新 `RSDC-Standard-ste-tw.md`，只重譯 710 行中改到的 296 行，parity check 通過。
  - 重驗：DFD-ste.md 在 2026-10-12 以目前的 `check_ste.py` 再驗一次，仍然通過，所以兩份 `-ste.md` 都已通過重驗。

**其他 session 的改動**

其他 session 也改了 asd-ste；「做了什麼」描述的是各 commit 當時的狀態，之後可能已被下列改動修改。

- 一般建議與檢查：
  - `a892f73` 把 GR-1～GR-8 摘要進 ste-rules.md。
  - `37e7432` 新增兩項警告：GR-6 的拉丁縮寫，以及 GR-1 的後面沒接 *that* 的 *make sure*。
  - `ea20160` 修正括號內的字詞、分號與被動語態原本不被檢查的漏洞。
- 依 [[Task 20]]：
  - `3387b89`：把執行時用不到的內容，例如 Dataflow，從 SKILL.md 移到 README.md。
  - `6b1ad3f`：各 step 的 Purpose 改列在 README.md。
  - `11ed3f1`：精簡術語表，並把寫 skill 的規則移到 skill-writing.md。

## 3. 要做的

**移出的待辦**

- PDF 進 git 的版權問題：移到 [[Task 26]]。
- 刪除 session 是否觸發 hook：移到 [[Task 27]]。

**牽涉的檔案**

- `.github/common/skills/asd-ste/`：SKILL.md、SKILL-tw.md、README.md、README-tw.md、`scripts/`、`references/`。
- [depends_on.py](../.github/common/scripts/depends_on.py)
- `.github/common/references/` 中的 RSDC-Standard-ste.md、DFD-ste.md，以及兩者的 twin。
- [external/ASD-STE100_ISSUE9.pdf](../external/ASD-STE100_ISSUE9.pdf)
- `checkpoints/asd-ste/`：YAML checkpoint，不進 git。

## 4. 驗證

—

## 5. 與其他 task 的關係

**與其他 task 的關係**

- [[Task 20]] 與 [[Task 21]]（已併入 Task 20）：建立 asd-ste 之後，檢視 SKILL.md 中執行時用不到的內容而提出；asd-ste 是拆出 README.md 的試點。
- [[Task 22]]：讓 gen-skill、check-skill 與 SKILL 範本跟上這次拆分。
- [[Task 26]]、[[Task 27]]：從本 task 的待辦移出。

## 6. 日誌

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-12

- 完成原本的待辦 1、2：重跑 RSDC-Standard-ste.md，並增量更新它的 twin。
- DFD-ste.md 以目前的 check_ste.py 重驗，仍然通過。
- 其餘兩項待辦移到 Task 26 與 Task 27。

### 2026-10-11

- 提出：補記建立 asd-ste skill 的那個 session 所做的工作。
- 建立 asd-ste，並擴充 depends_on.py 支援 PDF。
