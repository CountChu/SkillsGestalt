# Task 67 - draft.py replace 把中文版的 pairing line 指回原檔

**Status**：完成——2026-10-19 draft.py replace 把有 frontmatter 的中文版的 pairing line 指回原檔，找不到 pairing line 就拒絕；在副本上取代 SKILL-tmp，check_parity.py 0 failure。
**Raised**：2026-10-19，[[Task 32.11]] 準備 SKILL-tmp 的草稿送審時發現：草稿中文版的 pairing line 連到 SKILL-tmp-ste.md，`draft.py replace` 不會改它；使用者決定另開本 task 修 draft.py。
**Depends on**：—

## 1. 背景

chinese skill 替有 frontmatter 的檔案寫中文版時，在 frontmatter 下面加一行 pairing line，連回英文檔；每一份 SKILL.md 都是這樣。
例如 SKILL-tmp-tw.md 第 6 行是 `本文件為 [SKILL-tmp.md](.github/common/templates/SKILL-tmp.md) 的繁體中文版。`。
asd-ste 草稿的中文版也由 chinese skill 寫成，所以它的 pairing line 連到草稿：SKILL-tmp-ste-tw.md 第 6 行連到 SKILL-tmp-ste.md。
[draft.py](../.github/common/skills/asd-ste/scripts/draft.py) 的 `replace` 把草稿中文版寫到原檔中文版的位置，只把檔頭註記刪成兩行，pairing line 照舊，接著刪掉草稿。
取代之後，原檔中文版的 pairing line 連到已刪除的 SKILL-tmp-ste.md；`check_parity.py` 找不到連回 SKILL-tmp.md 的 pairing line，報「pairing line present」失敗。
SKILL-tmp 是 [[Task 32]] 第一份有 frontmatter 的草稿；以後替任何 SKILL.md 寫 STE 草稿，都會遇到同樣的問題。

## 2. 現況

### 發現（2026-10-19）

- 草稿中文版：`SKILL-tmp-ste-tw.md` 第 6 行。
- `draft.py` 的 `tidy()` 只處理檔頭註記那兩行（`TW_NAMES`、`TW_CORRECT`），`replace()` 沒有處理 pairing line。
- `check_parity.py` 對有 frontmatter 的一對，檢查第一個標題之上有沒有連到原檔檔名的連結。
  取代時，檔頭註記裡連到 SKILL-tmp.md 的兩個連結都刪掉了，只剩連到 SKILL-tmp-ste.md 的 pairing line。
- line for line 的中文版沒有加上去的 pairing line：原檔頂端連到 `-tw.md` 的那一行，中文版譯成連回英文檔。
  目前沒有草稿是這種情形，修的時候一併確認。

### 已決定（2026-10-19）

- 找 pairing line 的規則和 `check_parity.py` 相同：有 frontmatter 的草稿中文版裡，第一個標題之上、第一個目標檔名是草稿檔名的連結所在的那一行。
  只改那一行裡指到草稿的連結，連結的文字與目標都把草稿的檔名換成原檔的檔名。
- 有 frontmatter 的草稿中文版找不到這一行時，`replace` 以 `1` 結束、什麼都不寫，和 header note 不符合 House Rule 5 時一樣。
- 程式寫在 draft.py 裡，用 check_ste.py 的 `read_doc` 找好的 frontmatter、fence 與標題。
  不從 chinese skill 的 `scan_md.py` import：它在模組層 import yaml，draft.py 的每個指令就都要 PyYAML。
- 改了 pairing line 時，`replace` 多印一行 `pointed the pairing line of … (line N) back at …`，Step 7 把它存進 `replaced`。
- SKILL.md 的 DEDICATED TERMINOLOGY 加上 pairing line 的定義，Step 7 用這個名詞。
- README 改三處：Files Each Step Uses 說明取代的那句、When the Skill Is Changed 的 draft.py 節點下對 `check_parity.py` 的依賴、檢查清單 draft.py 那一條的 SKILL-tmp 取代與拒絕。
- 檢查只跑涵蓋這次修改的那幾條，另在 scratchpad 確認 line for line 的情形；全部一個 commit。

### 結果（2026-10-19）

- [draft.py](../.github/common/skills/asd-ste/scripts/draft.py)：`tidy()` 收到草稿與原檔的檔名時，以 `pairing_line()` 找有 frontmatter 的中文版的 pairing line，以 `point_back()` 把它指回原檔，並傳回它在寫出的檔案中的行號；docstring 與 exit status 一併寫上。
- [SKILL.md](../.github/common/skills/asd-ste/SKILL.md)：DEDICATED TERMINOLOGY 加上 pairing line；Step 7 寫上 replace 把 TW twin 的 pairing line 指回 source file，以及找不到它時以 `1` 結束。
- [README.md](../.github/common/skills/asd-ste/README.md)：照上面的三處改。
- 中文版照 chinese skill 改：SKILL-tw.md 逐個標題比對，變更集是 DEDICATED TERMINOLOGY 與 Step 7 兩節，沿用原有的譯文，只譯改到的句子；README-tw.md 是 line for line，三個 hunk，fenced 的兩行逐字照抄。

### 驗證（2026-10-19）

- 在 scratchpad 的副本上，對 commit `9722c0f` 時的 SKILL-tmp 四份檔案跑 `draft.py replace`：印出 `pointed the pairing line of templates/SKILL-tmp-tw.md (line 6) back at SKILL-tmp.md`，`check_parity.py` 0 failure。
  第 6 行和現在的 SKILL-tmp-tw.md 第 6 行相同。
  修改前的 draft.py 在同樣的副本上留下連到 SKILL-tmp-ste.md 的 pairing line，`check_parity.py` 報 pairing line present 與 link targets match one for one 兩項失敗。
- 把 pairing line 從草稿中文版的副本拿掉：`replace` 以 `1` 結束，四份檔案都沒有改動。
- line for line：造一組沒有 frontmatter、開頭連到 `-tw.md` 的檔案與草稿。
  草稿中文版的那一行照 chinese skill 的規則連回原檔，不是連回草稿，所以 `replace` 不動它，取代之後 `check_parity.py` 0 failure；這種情形不用另外處理。
- pairing line 的連結帶錨點、用反斜線或同一行有兩個連結時，都只改指到草稿的那一個；pairing line 在 header note 之下時，印出的行號是寫出的檔案中的行號。
- README 列出的檢查：DFD 的 `paths`、`replace` 與第二次以 `1` 結束、`dependents`（本 workspace 與 InvestForge，16 份）都和修改前一樣。
  三對 `check_parity.py` 0 failure，警告和修改前相同；兩份中文版的 `diff_md.py --verify` 都 PASS。
  SKILL.md 與 README 的 `depends_on.py check` 都 UNCHANGED；check-skill 的 `scan_skill.py` 只多了 pairing line 這個名詞與 1 行，沒有新的問題。

## 3. 要做的

1. ✅ 先讀 asd-ste 的 [README.md](../.github/common/skills/asd-ste/README.md) 的 When the Skill Is Changed 與 [skill-writing.md](../.github/common/rules/skill-writing.md)，照它改，並跑它列出的檢查。
2. ✅ `draft.py replace` 把草稿中文版的 pairing line 指回原檔：連結的文字與目標，都把草稿的檔名換成原檔的檔名。
3. ✅ SKILL.md 的 Step 7 與 README 說明 replace 做的事的地方，一併寫上 pairing line；中文版照 chinese skill 跟著改。
4. ✅ 在 [[Task 32.11]] 以 Step 7 取代 SKILL-tmp 之前做完。

## 4. 驗證

- 在 workspace 以外的副本上，對 SKILL-tmp 跑 `draft.py replace`：原檔中文版的 pairing line 連到 SKILL-tmp.md，`check_parity.py` 0 failure。
- asd-ste README 列出的檢查都通過。

## 5. 與其他 task 的關係

- [[Task 32.11]]：SKILL-tmp 的草稿；它的 Step 7 要等本 task 做完。
- [[Task 62.7]]：也要改 asd-ste 的 Step 7，兩個 task 會改到同一份 SKILL.md 與 README；本 task 做完時它還沒開始。

## 6. 知識

—

## 7. 日誌

### 2026-10-19

- 建立。
- draft.py replace 把有 frontmatter 的中文版的 pairing line 指回原檔，找不到就拒絕；SKILL.md 加上 pairing line 的定義，Step 7 寫上這兩件事，README 改三處，中文版照 chinese skill 改。
- 在副本上取代 SKILL-tmp，`check_parity.py` 0 failure；line for line 的情形不用另外處理；README 的檢查都通過，本 task 完成。
- 照 keep-English list，標題與內文共 23 處譯成中文的 pairing line 改成英文，意思沒有改；摘要表的 Title 跟著改（[[Task 68]]）。
- [[Task 32.11]] 以 Step 7 取代 SKILL-tmp，草稿中文版已刪除；指向它的連結改成行內程式碼，字句沒有改。
