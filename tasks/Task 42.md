# Task 42 - 讓 reformat_md.py 斷句時不把 inline code 誤當成數學式

**Status**：完成——2026-10-30 `is_prose()` 先拿掉 inline code 再找 `$$`；check-wiki-doc 的 `checking-criteria.md` 多拆出一行，report-cash-level 的 `SKILL.md` 不必重排。
**Raised**：2026-10-14，[[Task 32]] 審核 md-style 的草稿時發現：md-style.md 第 12、44 行一行有好幾句，重新排版也不會拆開。
**Depends on**：—

## 1. 背景

背景：reformat-md 的轉換 10 把正文的每一句各放在一行，但 [reformat_md.py](../.github/common/skills/reformat-md/scripts/reformat_md.py) 的 `is_prose()` 遇到含 `$$` 的行，就當成不是正文，整行略過。
[md-style.md](../.github/common/rules/md-style.md) 讓獨立成行的數學式維持原樣，指的是 `$$...$$` 自成一行的數學式；這個判斷卻連 inline code 裡的 `$$` 也算進去。
md-style.md 第 12 行（數學式的規則）與第 44 行（轉換 7）都在 inline code 裡寫了 `$$`，所以一行有好幾句，以 `--mode clean` 重新排版也不會變。
md-style 的 STE 草稿已經把這兩行拆成一句一行，取代之後 md-style.md 本身不再有這個情形，但其他檔案仍可能有。

## 2. 現況

2026-10-14 md-style.md 已由 STE 版取代，那兩行已拆成一句一行；腳本的問題仍在，其他檔案仍可能遇到。

### 現況查核（2026-10-20）

- [reformat_md.py](../.github/common/skills/reformat-md/scripts/reformat_md.py) 第 438 行的 `is_prose()` 仍以 `"$$" in s` 判斷，連 inline code 裡的 `$$` 也算，問題仍在。
- 實測的方法：把 `is_prose()` 改成先拿掉 inline code 再找 `$$`，以修正版與原版對同一批檔案的副本各跑一次 `--mode clean`，比對兩邊的結果。
- 本 workspace 含 `$$` 的 md 有 5 份，修正後只有一份會變：check-wiki-doc 的 [checking-criteria.md](../.github/common/skills/check-wiki-doc/references/checking-criteria.md) 第 266 行，多拆出一行。
- InvestForge 含 `$$` 的 md 有 11 份，`$$` 全在 inline code 裡的只有一行：report-cash-level 的 `SKILL.md` 第 93 行。
- 這兩份都沒有中文版，所以不必一起重排 twin。
- reformat-md 仍沒有 README.md。

### 做了什麼（2026-10-30）

- [reformat_md.py](../.github/common/skills/reformat-md/scripts/reformat_md.py) 新增 `outside_code()`，`is_prose()` 判斷 `$$` 之前先拿掉 inline code，照「已決定」的做法。
- check-wiki-doc 的 [checking-criteria.md](../.github/common/skills/check-wiki-doc/references/checking-criteria.md) 第 266 行拆成兩行。
- InvestForge 的 report-cash-level `SKILL.md` 第 93 行只有一句，修好之後也不會拆開，所以不必重排。
  這份檔案的其他地方本來就不是一句一行，新舊兩版都會改，和本 task 無關。

## 3. 要做的

**已決定（2026-10-20）**

- 怎麼認出獨立成行的數學式：只看拿掉 inline code 之後的文字。
  一行的 `$$` 都在 inline code 裡，就當正文斷句；inline code 外有 `$$` 的行照舊略過。
  只改 `is_prose()` 的一行；另一個做法「只認以 `$$` 開頭的行」會把寫在正文中間的 `$$…$$` 切開，不採用。
- 改好之後重新排版：兩個 workspace 都重排上面查到的兩份檔案，各自在自己的 repo commit。
  重排只會多拆出幾行，字句不變，以 `check_reformat.py` 確認。

**步驟**

1. 改 `is_prose()`：判斷 `$$` 之前先拿掉 inline code。
2. 照「4. 驗證」測過。
3. 重排 check-wiki-doc 的 `checking-criteria.md`，以及 InvestForge 的 report-cash-level `SKILL.md`。

2026-10-30 三步都已做完；第 3 步只有 check-wiki-doc 那一份要重排，見「2. 現況」的「做了什麼」。

**改 reformat-md 時**

reformat-md 沒有 README.md：先讀 [skill-writing.md](../.github/common/rules/skill-writing.md)，改好之後以 `check_reformat.py` 確認重新排版只改了換行與換行周圍的空格。
動手時 reformat-md 若已有 README.md（[[Task 24]]），就照它的 When the Skill Is Changed 做。

## 4. 驗證

- 一行的 `$$` 只在 inline code 裡：重新排版會把它拆成一句一行。
- 獨立成行的 `$$…$$`，以及 inline code 外含 `$$` 的行：照舊不動。
- 重排的兩份檔案，`check_reformat.py` 都是 PASS。
- 對同一份檔案再跑一次 `reformat_md.py`，沒有任何變化。

結果（2026-10-30）：[[Task 36]] 的 `test_reformat.py` 有兩個 `$$` 的例子，都 PASS；check-wiki-doc 那一份的 `check_reformat.py` PASS，只改了空白；再跑一次沒有變化。

## 5. 與其他 task 的關係

- [[Task 36]]：也改 `reformat_md.py` 的斷句（直引號、⌘ 開頭的句子）。
  兩個問題各自獨立，不互相依賴；一起做可以只重排一次、只跑一次檢查。
- [[Task 56]]：md-style 巡檢的 chore；本 task 修好之前，巡檢會漏掉這種一行多句，但不會誤報。
- [[Task 24]]：替其餘 skill 加上 README.md；若它先做完，「改 reformat-md 時」改讀 reformat-md 的 README.md。

## 6. 知識

—

## 7. 日誌

### 2026-10-30

- 改 `is_prose()`，和 [[Task 36]] 一起做，以它的 `test_reformat.py` 測過。
- 重排 check-wiki-doc 的 `checking-criteria.md`；report-cash-level 的 `SKILL.md` 不必重排。

### 2026-10-20

- 重新查過現況：問題仍在；實測修正只會動到兩個 workspace 各一行，兩份都沒有中文版。
- 決定做法（先拿掉 inline code 再找 `$$`）與重新排版的範圍，寫上步驟、驗證方式與相關的 task。

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-14

- 提出：Task 32 審核 md-style 的草稿時發現問題。
- md-style.md 由 STE 版取代，那兩行已拆成一句一行。
