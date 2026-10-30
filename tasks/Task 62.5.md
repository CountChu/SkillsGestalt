# Task 62.5 - 拆開 Task 32、38、54、55 與 Chore 2

**Status**：完成——5 項都只留這裡的部分；InvestForge 開了 Task 7–11 與 Chore 1；使用者看過。
**Raised**：2026-10-18，[[Task 62]] 拆出的第 5 步：一半是 InvestForge 的 task 與 chore 拆成兩邊。
**Depends on**：[[Task 62.3]]

## 1. 背景

2026-10-18 時，這 5 項裡屬於 InvestForge 的部分：

- [[Task 32]]（進行中）：「跳過、之後要轉的」InvestForge check-stop-price 的 SKILL-tw.md 4 處、StopPriceChecker-RSDC-tw.md 3 處，是「角色」「系統」改留英文的轉換。
- [[Task 38]]（完成）：「待決定 1」問既有檔案要不要轉成美式拼法，其中 InvestForge 有 29 份、308 處，17 處在 kept span 裡。
- [[Task 54]]（尚未開始）：Chore 3 要查兩組 skill，common 與 InvestForge 的 dedi。
- [[Task 55]]（尚未開始）：依賴巡檢的範圍是兩個 workspace 的全部 md。
- [[Chore 2]]（使用中）：`audit_keep_english.py audit` 帶著 `--root . --root ../InvestForge`。

## 2. 現況

### 已決定（2026-10-19）

動手前問了 8 個問題，都照建議：

- InvestForge 這次就建 keep-English 稽核的 chore，就是 Chore 1 @ InvestForge；第一次的基準和 [[Chore 2]] 一樣是 261016。
  清單已經不是 261016 版，所以兩個 chore 現在都該跑。
- 拆出去的事，在 InvestForge 各開一個 task，Raised 都是 2026-10-19：
  - Task 7 @ InvestForge：建立 keep-English 稽核的 chore，本 task 一起做完。
  - Task 8 @ InvestForge：check-stop-price 兩份中文版的「角色」「系統」，來自 [[Task 32]]。
  - Task 9 @ InvestForge：既有檔案的英式拼法要不要轉，來自 [[Task 38]]。
  - Task 10 @ InvestForge：check-skill 的 chore，查 dedi 的 skill，來自 [[Task 54]]；dedi 的 skill 還不是新格式，記在它的「要決定的」，不另開 task。
  - Task 11 @ InvestForge：依賴巡檢的 chore，來自 [[Task 55]]，是 [[Task 62.7]] 的前提。
- [[Task 32]] 裡「跳過、之後要轉的」那一句改寫成已移出，不點名去處；下一行的提醒搬到 Task 8 @ InvestForge。
- [[Task 54]]、[[Task 55]] 只改「已決定」與還要做的；背景裡 2026-10-18 的數字是紀錄，保留。
- 兩個 chore 等本 task commit 之後再跑，各自 commit，前綴 `chore 2: ` 與 `chore 1: `；只列出，不改中文版。
- InvestForge 的 commit 前綴是 `task 7`，和 [[Task 62.3]] 在那裡用 `task 1` 一樣；這裡的 commit 前綴是 `task 62.5`。

### 結果（2026-10-19）

- 這裡：
  - [[Task 32]]：「進度」裡跳過的那兩份改寫成已移出，提醒的那一行拿掉。
  - [[Task 38]]：「待決定 1」只留本 workspace 的既有檔案。
  - [[Task 54]]：範圍改成只有 common 的 skill；「要決定的」的 48 個改成 30 個。
  - [[Task 55]]：範圍、「要決定的」的包裝腳本與驗證改成本 workspace。
  - [[Chore 2]]：Status 行與「怎麼做」的指令只對本 workspace，第 5 章記下本 task。
  - [[Task 62.7]]：第 1 步與第 5 章寫上 Task 11 @ InvestForge。
  - 每一項都加了一行日誌。
- InvestForge：Task 7–11、`chores/Chore 1.md`、`dashboard/chore-summary.md`，以及根目錄 CLAUDE.md 的 `## Chores` 一節；task 的摘要表加上 5 列。
- 檢查：這裡的 `check_tasks.py` 18 項、`check_chores.py` 14 項 PASS；InvestForge 的 `check_tasks.py` 18 項（16 個 task 檔）、`check_chores.py` 14 項 PASS。
  兩個 chore 的 `due` 都從各自的根目錄跑得通，都印出 due：清單是 261018，基準是 261016。

## 3. 要做的

1. ✅ [[Task 32]]：check-stop-price 兩份中文版那一項，在 InvestForge 另立 task；Task 32 只留這裡的部分。
2. ✅ [[Task 38]]：「待決定 1」只留這裡的既有檔案；InvestForge 的 29 份，在 InvestForge 另立 task 決定。
3. ✅ [[Task 54]]：範圍改成只有 common；InvestForge 另立 task，建立它自己的 check-skill chore，查 dedi 的 skill。
   Skills Dashboard 的位置照 [[Task 62.6]]。
4. ✅ [[Task 55]]：範圍改成這裡的全部 md；InvestForge 另立 task，建立它自己的依賴巡檢 chore，那個 chore 是 [[Task 62.7]] 的前提。
5. ✅ [[Chore 2]]：「怎麼做」的指令只留 `--root .`，Status 行與目的改成本 workspace 的中英對照。
   InvestForge 另立 keep-English 稽核的 chore：觸發條件一樣是 tw-keep-english.md 換了版本，報告放在 InvestForge 的 `checkpoints/chores/`。
6. ✅ InvestForge 的第一個 chore 建立時，同時建它的 `chores/`、`dashboard/chore-summary.md` 與根目錄 CLAUDE.md 的 Chores 一節（[[Task 62.3]] 決定）。
7. ✅ 改過的每一項加一節日誌；兩邊都跑 `check_tasks.py` 與 `check_chores.py`。
8. ✅ 使用者看過之後 commit：InvestForge 一個，前綴 `task 7`；這裡一個，前綴 `task 62.5`。

## 4. 驗證

- 這 5 項沒有一件還要做的事會改 InvestForge 的檔；已記下的紀錄照 [[Task 62]] 的「已決定」保留。
- 兩邊的 `check_tasks.py` 與 `check_chores.py` 都 PASS。
- 兩個 chore 的 `due` 指令，從各自的根目錄跑得通。

## 5. 與其他 task 的關係

- [[Task 62.6]]：[[Task 54]] 的 Skills Dashboard 放哪裡。
- [[Task 62.7]]：InvestForge 的依賴巡檢 chore 建好、跑過一次之後才能做。

## 6. 日誌

### 2026-10-19

- 開始：問了 8 個問題，見「已決定」。
- 這裡的 5 項只留本 workspace 的部分；InvestForge 開了 Task 7–11 與 Chore 1。
- 驗證的第 3 項原本是「Chore 2 的 `due` 照舊印出 not due」；清單已換過版本，`due` 本來就會印出 due，所以改成兩個 `due` 指令都跑得通。
- 使用者看過，同意 commit；本 task 完成。

### 2026-10-18

- 從 [[Task 62]] 拆出，列出 5 項裡屬於 InvestForge 的部分。
- [[Task 62.3]] 決定 InvestForge 的 `chores/` 等第一個 chore 再建，第 3 章加上一步。
