# Task 18 - 讓已寫好的 RSDC 跟上對齊後的範本

**Status**：進行中——這裡的 3 份中 [[Task 18.7]] 與 [[Task 18.2]] 已對齊，[[Task 18.8]] 還沒對齊；InvestForge 的 5 份在 Task 2 @ InvestForge。
**Raised**：2026-10-10，從 [[Task 12]] 拆出：兩份範本對齊之後，已寫好的 RSDC 都還是舊形狀。
**Depends on**：[[Task 12]]、[[Task 10]]、[[Task 33]]

## 1. 背景

[[Task 12]] 對齊了 RSDC-App-tmp 與 RSDC-Skill-System-tmp 兩份 template 的格式與內容，在那之前寫好的 RSDC 都還是舊形狀。
本 task 讓它們跟上 template，每一份 RSDC 一個 sub task。
這個 workspace 只留自己的 3 份；InvestForge 的 5 份由 Task 2 @ InvestForge 處理。

## 2. 現況

### 2026-10-20 查的結果

- **三份 RSDC**：
  - [[Task 18.7]] Home-RSDC（imp-home 的 seed）已對齊：`depends_on.py check` 三個指紋都 UNCHANGED，`check_rsdc.py` 單獨、中英對照與 `--skill` 三種檢查都 PASS。
  - [[Task 18.2]] SkillCompiler-RSDC 當天對齊完成：單獨、中英對照與 compile-skill 的 `--skill` 三種檢查都 PASS。
  - [[Task 18.8]] MermaidView-RSDC 還是舊形狀：單獨檢查 6 項 FAIL，2026-10-18 之後沒有修改。
- **Template**：兩份 template 記下的 RSDC-Standard（`ffeecb284711`）與 DFD（`09fb4a7e4730`）指紋，都與現在的檔案一致，`check_rsdc.py --standard` PASS。
- **不在這一項**：gen-imp-app 產生的 4 個 owner skill 的 design pair，在 Task 5 @ InvestForge。

各份 RSDC 的細節在它自己的 sub task。

## 3. 要做的

### Sub task

逐份對齊，每份一個 sub task，對齊完就打 ✅。

- [[Task 18.2]] ✅ SkillCompiler-RSDC
- [[Task 18.7]] ✅ Home-RSDC（imp-home 的 seed）
- [[Task 18.8]] ⬜ MermaidView-RSDC

### 共用規則

- **一次對齊一份，照 template 手動改**：節號改了，引用它的地方同一次一起改（2026-10-18 決定）。
- **加上 template 連結**：在檔頭引用區、連到標準的連結之下，加上它所用的 template——`> [[RSDC-Skill-System-tmp]]` 或 `> [[RSDC-App-tmp]]`——並以 `depends_on.py record <RSDC> --target "[[…]]" --config config.yaml` 記下指紋；之後重寫 twin 時，chinese 會照 template twin 的寫法抄共用句子。
  [[Task 18.8]] 還沒有這一行，所以 `check_rsdc.py` 單獨檢查會多一項 FAIL；沒有連結的 App 形狀 RSDC（如 MermaidView），Checker 會退回 Skill-System template，要用 `--template` 指定。
- **指紋以 `depends_on.py check` 為準**：對齊時用 `depends_on.py record` 記下當時的指紋。
- **中文版照 chinese skill 更新**：與 template 共用的句子，照抄 template 的中文版。

### 要決定的

1. [[Task 18.8]] 最後一節「How This Version Came About」怎麼處理，見 [[Task 58]]。

## 4. 驗證

每個 sub task 對齊之後，都要通過這些檢查，和 [[Task 18.7]] 一樣：

- `check_rsdc.py --rsdc` 單獨檢查 PASS。
- `check_rsdc.py --rsdc --tw` 中英對照 PASS。
- 引用它的每一份 SKILL.md，`check_rsdc.py --rsdc --skill` PASS。
  gen-rsdc-skill 引用 SkillCompiler-RSDC 時有一項已知誤判，見 [[Task 75]]。
- 中英兩份的 `check_parity.py` 0 failure；中文版以 INCREMENTAL 更新時，`diff_md.py --verify` PASS。
- `depends_on.py check` 的每個指紋都是 UNCHANGED。

三個 sub task 都 ✅ 時，本 task 完成。

## 5. 與其他 task 的關係

- **Task 2 @ InvestForge**：InvestForge 的 5 份 RSDC——StopPriceChecker、InvCov、InvDataflow、InvIndexAnalyzer 與 InvHome 的 Home-RSDC。
  它們原是本 task 的 Task 18.1、18.3–18.6，2026-10-18 移過去。
- **Task 5 @ InvestForge**：gen-imp-app 產生的 4 個 owner skill 的 design pair，原是本 workspace 的 Task 30。
- **[[Task 17]]**（2026-10-11）：RSDC Checker 能檢查 app 的 RSDC——`check_rsdc.py` 不再把 App template 有的 Directory Structure 與 Presentation Form 判為 FAIL，沒有 CLI 節時也改用 3.1 的 component 檢查 stage 與 4.5。
  App 形狀的那幾份對齊後可以用它驗證；用 gen-rsdc-app 重寫時，它會自己執行。
- **[[Task 33]]**（2026-10-12 完成）：兩份 RSDC template 已沒有 Twin 行；`check_rsdc.py` 遇到 RSDC 連到自己的中文版、或中文版連回英文，都判 FAIL。
  已寫好的 RSDC 都拿掉了指向中文版的那一句，所以還沒對齊的幾份照現在的 template 對齊，不必再處理這一行。
- **[[Task 58]]**：文件不寫自己的來歷；[[Task 18.8]] 最後一節「How This Version Came About」要照它處理。
- **[[Task 60]]**：記下各份單獨檢查的 6 項 FAIL。
- **[[Task 75]]**：gen-rsdc-skill 的範例引用被 `--skill` 當成對 SkillCompiler-RSDC 的引用；修好之前，這一項 FAIL 是已知誤判。

## 6. 日誌

### 2026-10-20

- 依 2026-10-20 的情況調整本 task，各 sub task 沒有改。
- 補上「背景」與「驗證」；「驗證」寫的是每個 sub task 都要通過的檢查。
- 「現況」換成 2026-10-20 查的結果；原本以 8 份來寫的兩節拿掉，它們的重點在 2026-10-10、2026-10-11 的日誌與各 sub task 裡。
- 「要做的」整理成 sub task 清單、共用規則與一個待決定；2026-10-18 的決定與加 template 連結的做法寫進共用規則。
- 移到 InvestForge 的 task 改寫成 Task 2 @ InvestForge 與 Task 5 @ InvestForge；「與其他 task 的關係」也加上 [[Task 58]] 與 [[Task 60]]。
- 使用者決定先做 [[Task 18.2]]，當天對齊完成；「要決定的」只留 [[Task 18.8]] 的那一節，「現況」、共用規則、「驗證」與「與其他 task 的關係」跟著改。

### 2026-10-18

- 拆成 sub task Task 18.1–[[Task 18.8]]，每份 RSDC 一個，屬於各份的內容搬過去，內容沒有改。
- 使用者決定一次對齊一份，先做 [[Task 18.7]]；SkillCompiler、Home-RSDC 的 seed 與 MermaidView 照範本手動改，引用處同一次一起改。
- [[Task 18.7]] imp-home 的 Home-RSDC 對齊完成。
- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。
- 18.1、18.3、18.4、18.5 與 18.6 移出本 workspace：sub task 清單與「要決定的」只留這裡的 3 份，第 2 點跟著移出；指向它們的 wikilink 改成純文字（[[Task 62.4]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-12

- StopPriceChecker 對齊完成（InvestForge `db70105`），DFD 指紋在 `45333f6` 重記。
- InvCov 對齊完成（InvestForge `1357e12`）。
- Task 33 完成，已寫好的 RSDC 不必再處理指向中文版的那一句。

### 2026-10-11

- 重新查過 8 份，都還沒對齊。
- 記下對齊時要加範本連結、補 InvDataflow-RSDC-tw 的 inline code，以及 RSDC Checker 能檢查 app 的 RSDC。

### 2026-10-10

- 從 Task 12 拆出，查了 8 份已寫好的 RSDC 的形狀。
