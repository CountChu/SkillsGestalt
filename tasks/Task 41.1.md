# Task 41.1 - 處理現有 STE 檔裡字典不核准的技術用字與標題字

**Status**：完成——8 個術語收進 ste-custom.md，`check_ste.py` 不再查標題的字；17 個 STE 檔只剩 glossary.md 與 DFD.md 的 setting 一項警告，照決定保留。
**Raised**：2026-11-01，[[Task 41]] 決定把現有 STE 檔的警告另開 sub task。
**Depends on**：—

## 1. 背景

[[Task 41]] 讓 [check_ste.py](../skill-groups/common/skills/asd-ste/scripts/check_ste.py) 多報兩種 `[WARN]`：字典不核准當名詞或形容詞用的技術用字，以及標題裡字典沒收、也不是技術用字的字。
asd-ste 的 README 說，規則改了之後，每個已取代 source 的 STE 檔都要以 `check_ste.py --ste` 再查一次，並手動修正。

## 2. 結論

—

## 3. 過程

### 2026-11-02 處理之後

- `check_ste.py` 不再查標題的字：拿掉清冊的標題字 `[TODO]`、檢查的「標題裡字典沒收的字」`[WARN]`，以及兩個 findings key `heading_words_to_decide` 與 `heading_words_not_in_dictionary`。
  只在標題用到的技術用字仍算用到；標題裡的英式拼法仍由 kept span 的拼字檢查查。
- 18 個 STE 檔的判定都和處理之前相同：17 個 PASS，CLAUDE-local.md 原本就因 header quote 沒宣告 STE 規格與 ste-custom 而 FAIL。
- 各個字怎麼處理，見表 2。

**表 2：每個字典不核准的技術用字的處理**

| 字 | 處理 | 用在哪些檔的 `Technical words:` |
|---|---|---|
| activity、event、partial、process、request、route、stage、variable | 收進 ste-custom.md，當名詞核准 | 從 DFD.md、RSDC-Standard.md、tw-keep-english.md、report-yaml-rules.md、scratch-rules.md 拿掉 |
| stage（git 動詞，stage a blob） | 當技術動詞留著，意思和 ste-custom.md 的 stage 不同 | chore-rules.md、task-rules.md 留著；`[INFO]` 說字典仍核准它 |
| process（作業系統的行程） | 當技術名詞留著，意思和 ste-custom.md 的 process 不同 | SKILL-tmp.md 留著；`[INFO]` 說字典仍核准它 |
| setting（`config.yaml` 的一個設定項） | 當技術名詞留著（類別 6） | glossary.md、DFD.md；每次 `--ste` 仍報這一行 `[WARN]` |

### 2026-11-01 查的結果

以 `check_ste.py --ste`，加上 `--custom` 與 `--spelling`，查 SkillsGestalt 的 18 個英文 STE 檔；17 個有新的警告，見表 1。
括號是標題的行號。

**表 1：每個 STE 檔多出的警告**

| 檔案 | 字典不核准的技術用字 | 標題裡字典沒收的字 |
|---|---|---|
| `.github/common/references/DFD.md` | process, request, setting | What（110） |
| `.github/common/references/RSDC-Standard.md` | activity, process, request, stage | Responsibilities（1）, Core（27）, Dependency（27）, Principle（27）, Writing（27）, Requirements（57）, Coding（342）, Versioning（387） |
| `.github/common/references/forge-setup.md` | — | Older（123） |
| `.github/common/references/glossary.md` | setting | — |
| `.github/common/references/tw-keep-english.md` | event, process, request, route, stage, variable | English（1）, Adding（150） |
| `.github/common/rules/chore-rules.md` | stage | — |
| `.github/common/rules/md-style.md` | — | Markdown（1）, checked（153）, elsewhere（153） |
| `.github/common/rules/report-yaml-rules.md` | partial | — |
| `.github/common/rules/scratch-rules.md` | stage | — |
| `.github/common/rules/skill-writing.md` | — | Writing（1） |
| `.github/common/rules/task-rules.md` | stage | Sub（122） |
| `.github/common/rules/tools.md` | — | Pick（29）, what（29）, banned（81）, narrowed（81）, Print（92） |
| `.github/common/templates/CLAUDE-tmp.md` | — | Markdown（22） |
| `.github/common/templates/README-tmp.md` | — | Dataflow（32）, Dependencies（174）, Tracked（174） |
| `.github/common/templates/SKILL-tmp.md` | process | Warmup（100） |
| `CLAUDE-local.md` | — | Agency（3） |
| `CLAUDE.md` | — | Markdown（20） |

## 4. 要做的

### 已決定（2026-11-02）

使用者回答了 11 個問題：

1. **chore-rules 與 task-rules 的 stage 是 git 動詞**：當技術動詞留著。
2. **DFD、RSDC 與 tw-keep-english 定義的 8 個術語**：收進 ste-custom.md。
3. **glossary 與 DFD 的 setting**：當技術名詞留著，警告留著。
4. **SKILL-tmp 的 process 是作業系統的行程**：當技術名詞留著。
5. **所有標題不歸 STE 管**：`check_ste.py` 拿掉標題字的檢查，清冊的 `[TODO]` 也拿掉；ste-rules.md 原本就說標題照原文保留。
6. **只在標題出現的名稱不列進 `Technical words:`**：Markdown、English、Agency 與 Dataflow 都不列。
7. **8 個術語從各檔的 `Technical words:` 拿掉**：意思不同的 stage 與 process 例外。
8. **DFD.md 與 RSDC-Standard.md 的指紋改了**：照拿掉，引用它們的文件以 `depends_on.py record --target` 重記。
9. **CHANGES.md 加一筆**。

## 5. 驗證

- `check_ste.py --ste`，加上 `--custom` 與 `--spelling`，查 18 個英文 STE 檔：判定都和處理之前相同，結果見「現況」。
- asd-ste README 列的 DFD 測試：commit `1710643` 的清冊 exit 0、檢查 PASS；commit `ed0076e` 的清冊 exit 3、SOURCE-FIRST，不再問標題裡的 *Kinds*，檢查因 `Catalogue` FAIL。
- `check_parity.py`：SKILL.md、README.md 與 ste-custom.md 各和中文版比對，0 failure。
- `draft.py recheck`：32 個檔都重查並重記 ste-custom.md，PASS。
- `depends_on.py check`，查每個有 header quote 的檔：只剩 check-md-deps 對 check-wiki-doc 的兩項 CHANGED，2026-10-10 就有，與本 task 無關。
- 沒跑 `/check-skill asd-ste`；draft.py、make_review.py 與 review_server.js 沒改。

## 6. 與其他 task 的關係

- [[Task 41]]：它加的「標題裡字典沒收的字」警告，本 task 拿掉。

## 7. 知識

### 適合寫成新 topic

—

### 適合併進現有 topic

—

### 不算知識

- **改了 STE 檔的 `Technical words:` 行，它的指紋就變**：引用它的每份文件都報 CHANGED，Forge 的也一樣；header quote 的紀錄則不算進指紋。

## 8. 日誌

### 2026-11-02

- 連結的目標路徑從 `../.github/` 改成 `../skill-groups/`，字句沒有改（[[Task 97.7]]）。
- 使用者回答 11 個問題：8 個術語收進 ste-custom.md，標題不歸 STE 管。
- 改 `check_ste.py`、asd-ste 的 SKILL.md 與 README，以及它們的中文版；5 個 STE 檔的 `Technical words:` 拿掉這些字。
- 引用 DFD.md、RSDC-Standard.md、report-yaml-rules.md 與 scratch-rules.md 的文件重記指紋；`draft.py recheck` 重記 ste-custom.md。
- CHANGES.md 加一筆；「現況」、「要做的」、「驗證」與「知識」四章跟著改，本 task 完成。

### 2026-11-01

- 從 [[Task 41]] 拆出，記下 18 個 STE 檔的查核結果。
