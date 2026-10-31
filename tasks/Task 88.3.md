# Task 88.3 - 改了會影響 Forge 的東西時怎麼通知

**Status**：完成——2026-10-31 會影響 Forge 的改動記在 [CHANGES.md](../.github/common/CHANGES.md)，Forge 以 chore [[follow-gestalt]] 處理；寫條目的規則在本 repo 的 CLAUDE-local.md；Task 82 到 88 的改動補記成第一批條目。
**Raised**：2026-10-31，[[Task 88]] 拆出的第 3 步：本 repo 一改，Forge 立刻跟著變，卻沒有規則說要怎麼告知。
**Depends on**：—

## 1. 背景

- Forge 直接讀本 repo 的工作目錄，沒有版本：`skillGroups.common` 指向本 repo 的 `.github/common`，`agencies` 指向本 repo 的根目錄。
- [[Task 86]] 改了 `check_chores.py` 與 chore 的寫法，InvestForge 在改成新寫法之前，`check_chores.py` 一直 FAIL；這次是在對話裡手動通知 Task 13 @ InvestForge 的 session。
- 會影響 Forge 的東西：`{skillGroups.common}` 裡的 rules、templates、scripts 與 skills，以及 Forge 透過 `agencies` 做的 chore。

## 2. 現況

- [CHANGES.md](../.github/common/CHANGES.md)：繁體中文，沒有英文版；開頭說明「會影響」的意思與格式，每天一個 `### yyyy-mm-dd`，新的在前，每一筆寫改了什麼、commit 與「Forge 要做」。
  第一批條目補記 2026-10-30 的改動（CLAUDE.md 由模板產生、`keepEnglishChore`、chore 改用名稱、沒有 `chores/` 也可以、chore 不放自己的程式），以及 2026-10-31 的 follow-gestalt 本身；被同一天取代的做法（`agency-rules.md`、使用檔）只在取代它的那一筆提到。
- [[follow-gestalt]]：定義在本 repo，Forge 透過 `agencies` 做；何時要做是 `CHANGES.md` 有比上次處理的那一筆新的條目；怎麼做是照條目做、重新產生 CLAUDE.md、跑兩個檢查、在摘要表記下處理到哪一筆。
  本 repo 的摘要表也有它的一列（每個 chore 檔都要有一列），上次執行是 —，本 repo 自己不做。
- [CLAUDE-local.md](../CLAUDE-local.md) 的 Settings of This Agency 加兩句：`common` 的改動會讓 Forge 要做事或檢查出現 `FAIL` 時，在 CHANGES.md 記一筆；每個 Forge 做 follow-gestalt 處理這些條目；重新產生 CLAUDE.md。

## 3. 要做的

### 開始做時決定的（2026-10-31）

- 通知的方式：一份變更紀錄 `CHANGES.md`，加上一個給 Forge 做的 chore；不在 commit 主旨加註，也不在各 Forge 開 task。
- 「會影響 Forge」：Forge 必須做點什麼，或它的檢查會從 PASS 變成 FAIL；只改措辭的不記。
- `CHANGES.md` 放在 `.github/common/`，繁體中文，沒有英文版。
- 補記 Task 82 到 88 的改動，作為第一批條目。
- chore 叫 `follow-gestalt`；`CHANGES.md` 有比上次處理的那一筆新的條目時就該做，不必寫程式。
- 條目的格式：`### yyyy-mm-dd` 一天一節，每一筆寫改了什麼、commit、Forge 要做什麼。
- 寫條目的規則只寫在本 repo 的 `CLAUDE-local.md`：只有 SkillsGestalt 寫條目；forge-setup.md 與 task-rules.md 不改。

## 4. 驗證

- 照決定的方式，模擬一次會影響 Forge 的改動，Forge 那邊能從通知知道要做什麼。

2026-10-31 的結果：

- 本 repo：`check_chores.py` 18 passed，[[follow-gestalt]] 的指令 `{skillGroups.common}/scripts/gen_claude_md.py` 通過程式路徑的檢查；重新產生的 CLAUDE.md `check_ste.py` 是 PASS，`--check` 是 PASS；`reformat_md.py --mode clean` 只把 CHANGES.md 的一句移到自己的一行。
- 模擬的 Forge（Task 88.2 照指南做出的 BookForge）：摘要表加一列文字的 `follow-gestalt` 與它的執行紀錄，`check_chores.py` 18 passed。
- 還沒在 InvestForge 實際做過一次 follow-gestalt：forge-setup.md 的 chore 摘要表範例沒有這一列，新的 Forge 要從 CHANGES.md 2026-10-31 那一筆知道要加。

## 5. 與其他 task 的關係

- [[Task 88]]：本 task 是它的第 3 步。
- [[Task 86]]：這次的問題就是它造成的。

## 6. 知識

—

## 7. 日誌

### 2026-10-31

- 建立：列出通知方式的候選，還沒決定。
- 開始做並完成：寫好 `CHANGES.md` 與第一批條目、chore [[follow-gestalt]]，CLAUDE-local.md 加上寫條目的規則。
