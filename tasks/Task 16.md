# Task 16 - 讓 compile-skill 與 gen-skill 處理檔頭引用區的依賴格式

**Status**：完成——2026-10-12 關閉：觸發條件仍未出現，依賴改宣告在 README.md 之後觸發的機會也變小了；真的發生時再開新 task（見下方「現況查核」）。
**Raised**：2026-10-10，從 [[Task 13]] 拆出：其餘各列都已做完，只剩這兩列要等觸發條件。
**Depends on**：[[Task 13]]

## 1. 背景

依賴格式見 Task 13：文件開頭的檔頭引用區一行一個連結，後面是確認的日期與指紋，由共用的 [depends_on.py](../.github/common/scripts/depends_on.py) 讀寫。

**觸發條件**：某個已編譯的 skill（有 `skill.py` 的）在 `SKILL.md` 宣告依賴，例如 gen-rsdc-skill 的 Step 8 為它加上 `> [[<system name>-RSDC]]`。
到那時 compile-skill 若還沒改，那個 skill 每次 `record`，它的 `skill.py` 都會被判為過期。
2026-10-10 查的時候，唯一編譯過的 skill 是 InvestForge 的 report-inv-week，它的 `SKILL.md` 沒有檔頭引用區。

## 2. 現況

### 狀態細節

gen-skill 那一列已由 Task 22 完成（2026-10-11）。

**現況查核（2026-10-12）**

- 觸發條件仍未出現。
  已編譯的 skill 仍只有 InvestForge 的 report-inv-week，它的 `SKILL.md` 沒有檔頭引用區。
  在 `SKILL.md` 宣告依賴的 skill 有 gen-rsdc-skill、asd-ste、compile-skill、check-md-deps，四個都沒有 `skill.py`。
- 觸發的機會變小了。
  [[Task 20]]、[[Task 22]] 之後，skill 的依賴多半宣告在 `README.md`，而 compile-skill 的 `source_fingerprint()`（`scan_source.py`）只對 `SKILL.md` 算 hash。
  所以 `README.md` 裡的依賴再怎麼 `record`，都不會讓已編譯的 `skill.py` 被判為過期。
  仍會觸發的只剩一種：被編譯的 skill 在 `SKILL.md` 本身宣告依賴。
  例如：
  - 用 gen-rsdc-skill 為某個 skill 寫 RSDC，Step 8 在它的 `SKILL.md` 加上 `> [[<system name>-RSDC]]`，之後又把那個 skill 編譯。
  - 編譯 asd-ste 這類本來就在 `SKILL.md` 宣告依賴的 skill。
- 2026-10-12 決定關閉本 task。
  真的發生時再開新 task，上表 compile-skill 那一列就是要做的事：先改 SkillCompiler-RSDC，再讓 `scan_source.py` 與 `check_compiled.py` 跳過檔頭引用區。

## 3. 要做的

| Skill | 現在 | 要做什麼 | 牽涉的檔案 |
|---|---|---|---|
| compile-skill | 編譯流程不讀依賴；`source_fingerprint()` 對整份檔案算 hash，檔頭那一行也算在內 | 讓它跳過檔頭引用區，否則已編譯的 skill 之後每次 `record`，它的 `skill.py` 都會被判為過期 | SkillCompiler-RSDC（先改）、`scan_source.py`、`check_compiled.py`、已編譯 `skill.py` 內嵌的那一份 |
| gen-skill | 已完成（[[Task 22]]，2026-10-11）：Step 5 在新 skill 的 `README.md` 寫出檔頭引用區，並以 `depends_on.py record` 記錄 | 無：依賴宣告在 `README.md`；`SKILL.md` 自己要宣告的依賴，例如 RSDC，仍由寫它的 skill 加上 | `gen-skill/SKILL.md`、`templates/README-tmp.md` |

## 4. 驗證

—

## 5. 與其他 task 的關係

—

## 6. 知識

—

## 7. 日誌

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-12

- 查核現況：觸發條件仍未出現，依賴改宣告在 README.md 之後觸發的機會也變小了。
- 決定關閉本 task，真的發生時再開新 task。

### 2026-10-11

- gen-skill 那一列已由 Task 22 完成。

### 2026-10-10

- 提出：從 Task 13 拆出，其餘各列都已做完，只剩這兩列要等觸發條件。
- 查過已編譯的 skill：只有 InvestForge 的 report-inv-week，它的 `SKILL.md` 沒有檔頭引用區。
