# Task 35 - 為 asd-ste 加上自訂核准字的 customization 檔

**Status**：完成——2026-10-12：asd-ste 能讀自訂核准字的清單（`a6e061f`）；`/check-skill asd-ste` 第一次找到的 4 個項目已修好（`a62dc08`），重跑 6 項都通過。
**Raised**：2026-10-12，[[Task 31]] 做第 2.5 步（report-md-rules）時，使用者決定把 current 與 now 列為核准字，並新建一份 customization 檔來放這類字。
**Depends on**：—

## 1. 背景

背景：asd-ste 的 `check_ste.py` 只認 STE 字典（`ste-dictionary.json`，由 ASD-STE100 Issue 9 的 PDF 產生）與草稿檔頭的 Technical words 行。
Issue 9 不核准 current（字典裡沒有）與 now（字典給 AT THIS TIME），但 report-md-rules 的「current local date-time」用 STE 改寫，會比原文長，也不比原文清楚。
本 task 讓 asd-ste 多讀一份由使用者決定的自訂核准字清單。

## 2. 現況

**2026-10-12 做了什麼**（commit `a6e061f`）

改之前另外問了 2 個問題：`/check-skill` 用 InvestForge 的 `config.yaml` 完整跑；commit 分成修改與紀錄兩個。

- **新檔**：`ste-custom.md` 與 `ste-custom-tw.md`，表格先放 current（adj）與 now（adv）；檔頭記錄 PDF 的指紋。
- **`check_ste.py`**：新增 `--custom`，以標題列找到表格，把每個詞與它的 Forms 當成核准詞；用到時印 `[INFO]`。
  STE file 用到自訂字卻沒宣告 `[[ste-custom]]` 是 FAIL，宣告了卻沒用到是 WARN；findings file 多了 `custom_words_used` 與 `customization`。
- **SKILL.md 與中文版**：description、STE customization 術語、header quote 的定義、CONFIGURATION、Step 0 檢查的檔案、Step 1 與 Step 3 的指令與檢查、Step 2 的 header quote、Step 3 的記錄指令與 `custom_fingerprint`；中文版照 chinese 判定 INCREMENTAL 更新。
- **README.md 與中文版**：Dataflow 加上 STE customization 這個 external input，以及兩條藍線（第 44、45 條，接在最後，不必重新編號）；圖例、Files Each Step Uses、When the Skill Is Changed、檢查清單與 Tracked Dependencies 跟著改。
- **ste-rules.md**：開頭與 1.1 指向自訂清單，House Rule 5 加上 `[[ste-custom]]` 那一行，新增 House Rule 11；SKILL.md 與中文版檔頭記的指紋重記為 `4c14fa369950`。
- **測試**：不給 `--custom` 時，DFD 的結果和以前一樣；用暫存檔試過「用了沒宣告 FAIL」「宣告了 PASS 並印 INFO」「宣告了沒用 WARN」「表格格式錯誤時以 2 結束」；`depends_on.py` 找得到 `[[ste-custom]]`，也能記錄、檢查它的指紋。

**2026-10-12 修 check-skill 的項目**（commit `a62dc08`）

使用者選了 `fix 1.1(a) 4.1 5.1 5.2`；套用前分兩輪問了 6 個問題，決定如下：5.1 連另外 3 個要執行的指令一起改；4.1 的兩個術語都不加粗；5.2 接在 `date` 指令後面；修完馬上重跑；commit 分成修改與紀錄兩個；checker defect 只記在這裡。

- **1.1(a)**：description 刪掉 header quote 與 header note 那一段，指紋那段縮成「records the fingerprints with depends_on.py」，YAML checkpoint 那句拿掉路徑，從 1211 字元變成 968 字元；中文版的 description 刪同樣三處。
- **4.1**：SKILL.md 第 150 行改成「the Dependency Checker and the step saver import `PyYAML`」，中文版第 154 行跟著改。
- **5.1**：11 個要執行的指令改用斜線——8 個 Example，加上 Step 0 的 `convert_spec.py`、Step 3 的 `depends_on.py record` 與 Step 5 的 `/chinese`；中文版的 11 行跟著改。
  只改指令，Step 0 檔案清單裡的路徑沒動。
- **5.2**：SKILL.md 第 77 行在 `date` 指令後面補上 PowerShell 的 `Get-Date -Format "yyyy-MM-dd HH:mm:ss"`，中文版第 81 行跟著改。
- **檢查**：`check_parity.py` 0 failure（仍是那 3 個 HEAD 就有的 WARN）；`diff_md.py --verify` 通過；reformat-md 試轉兩份都沒有改變。
- **重跑 `/check-skill asd-ste`**：6 項都 ✅，沒有 issue 也沒有 recommendation；Dashboard 上 asd-ste 那一列從 ❌ 2 · 2 變成 ✅ 0 · 0，needs check 清掉了。
  兩個 checker defect 照舊出現，不算進項目。

## 3. 要做的

**已決定（2026-10-12）**

問了 8 個問題，決定如下：

- **檔案**：`asd-ste/references/ste-custom.md`，一張 Markdown 表格，欄位是 Word、Part of speech、Forms、Meaning、Why；配一份中文版 `ste-custom-tw.md`。
- **讀取**：`check_ste.py` 新增 `--custom` 參數，Step 1 與 Step 3 的指令都明寫它；沒給就只用字典，舊的指令照樣能跑。
- **顯示**：草稿用到自訂的字時，印一條 `[INFO]`，不算 WARN。
- **檔頭引用區**：用到自訂字的草稿，在檔頭引用區宣告 `[[ste-custom]]`，由 `depends_on.py record` 記下指紋；清單一改，`depends_on.py check` 就會標出這些草稿。
- **第一批字**：current（adj）與 now（adv）。
- **順序**：先做完本 task，再回到 Task 31 的 2.5。
- **已寫好的草稿**：用 `--custom` 重查 6 份已寫好的草稿，記下結果。
- **紀錄**：開新的 task，commit 前綴 `task 35`；Task 31 依賴本 task。

**要做的**（照 asd-ste README 的 When the Skill Is Changed）

1. 新增 `ste-custom.md` 與它的中文版。
2. `check_ste.py`：`--custom`、表格的解析、`[INFO]`、檔頭引用區的檢查。
3. SKILL.md 與 SKILL-tw.md：術語、CONFIGURATION、Step 0 檢查的檔案、Step 1 與 Step 3 的指令與檢查、Step 2 的檔頭引用區、Step 3 的記錄指令。
4. README.md 與 README-tw.md：Dataflow 加一個外部輸入，Files Each Step Uses、When the Skill Is Changed 與 Tracked Dependencies 跟著改。
5. ste-rules.md：House Rule 5 加上自訂清單那一行，再加一條 House Rule；SKILL.md 檔頭記的指紋重記。
6. 檢查：README 列的 5 項，加上 6 份已寫好的草稿的重查。

## 4. 驗證

**驗證（2026-10-12）**

- **README 列的檢查**：
  1. `check_ste.py` 加 `--custom`，DFD 的清冊與檢查都通過。
  2. `check_parity.py`：SKILL、README 與 ste-custom 三對都 0 failure；SKILL 有 3 個、README 有 2 個 WARN，都是 HEAD 就有的譯法（標準形式的 skill 呼叫、識別碼、腳本），不是這次改的句子；兩份 INCREMENTAL 更新的中文版 `diff_md.py --verify` 都通過。
  3. `depends_on.py check`：SKILL.md 與 README.md 都 UNCHANGED。
  4. `/check-skill asd-ste`：見下一點。
  5. 對 DFD 跑 Step 0、1、3、4：YAML checkpoint 有 step_0、1、3、4，各有 title 與 time；Step 3 PASS，DFD-ste.md 沒有變動，Step 4 跳過。
     跑之前把 `checkpoints/asd-ste/references-DFD/` 備份，跑完還原，Task 31 第 1 步記的 `intentional_differences` 仍在。
- **一句一行**：改過的 4 份 Markdown 用 reformat-md 在副本上試轉，都沒有改變。
- **6 份已寫好的草稿**：用 `--custom` 重查都是 PASS，沒有一份用到自訂字；RSDC-Standard 仍是第 1 步留下的 4 個被動句警告。
- **`/check-skill asd-ste`**（用 InvestForge 的 `config.yaml`；Skills Dashboard 在 InvLlmWiki 的 `dashboard/skills.md`，這次新建）：
  1 ❌（1 個 issue）、2 ✅、3 ✅、4 ⚠️（1 個 recommendation）、5 ❌（1 個 issue、1 個 recommendation）、6 ✅。
  - **1.1 description 1211 字元，超過 1024 的上限**：HEAD 就已是 1108 字元，本 task 又加了 103 字元。
  - **4.1 SKILL.md 第 150 行用 `depends_on.py`**，而 glossary 定義了 Dependency Checker：HEAD 就有。
  - **5.2 8 個範例指令的路徑用反斜線**，在 macOS 與 Linux 的 shell 照字面執行會失效：HEAD 就有，本 task 加的 `--custom` 照著原來的寫法。
  - **5.1 MUST FOLLOW 第 77 行只寫 `date '+%Y-%m-%d %H:%M:%S'`**，沒有 PowerShell 的寫法：HEAD 就有。
  - **checker defect**：以 InvestForge 為 workspace 掃描，第 75、249 行的 `.github/common/rules/` 連結被當成斷掉的連結；`depends_on.py` 是共用的腳本，被當成 `scripts/` 裡缺少的檔案。

## 5. 與其他 task 的關係

**與其他 task 的關係**

- [[Task 31]]：依賴本 task——第 2.5 步要用 current。
- [[Task 32]]：用草稿取代原檔時，用到自訂字的那幾份也要保留 `[[ste-custom]]` 那一行，和 PDF 那一行一樣。
- [[Task 23]]：建立 asd-ste。

## 6. 知識

—

## 7. 日誌

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-12

- 提出：Task 31 做第 2.5 步時，決定為 asd-ste 新建自訂核准字的 customization 檔。
- asd-ste 能讀自訂核准字的清單。
- 用 /check-skill asd-ste 找到的 4 個項目修好，重跑 6 項都通過。
