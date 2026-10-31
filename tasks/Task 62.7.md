# Task 62.7 - asd-ste 的 Step 7 只重記本 workspace 的依賴方

**Status**：尚未開始——要等 InvestForge 的依賴巡檢 chore 建好、跑過一次。
**Raised**：2026-10-18，[[Task 62]] 拆出的第 7 步：上游停在自己的邊界。
**Depends on**：[[Task 62.5]]

## 1. 背景

- asd-ste 的 Step 7 找依賴方時，要問使用者還有哪些 workspace 用這個 skill group，把它們的資料夾加成 `--root`。
  2026-10-18 時在 [SKILL.md](../.github/common/skills/asd-ste/SKILL.md) 的第 512–513 行。
- 所以這裡以 STE 版取代一份共用檔時，會直接去 InvestForge 重記指紋，commit 用這裡的編號；例如 [[Task 32.1]]、[[Task 32.2]] 與 [[Task 32.8]]。
- [[rerecord-ste-custom]] 的第 1 步也一樣：其他用這個 skill group、而且有 STE 檔的 workspace，各加一個 `--root`。
- [[Task 32]] 的「要做的」也寫著，重記時要找其他 workspace（例如 InvestForge）裡的文件。
- 能判斷「讀過改動仍然成立」的，是依賴方的主人；InvestForge 的依賴方，改由 InvestForge 自己的依賴巡檢 chore 重記。

## 2. 現況

—

## 3. 要做的

1. 確認 InvestForge 的依賴巡檢 chore 已建好，而且至少跑過一次；Task 11 @ InvestForge 建它。
2. 先讀 asd-ste 的 [README.md](../.github/common/skills/asd-ste/README.md) 的 When the Skill Is Changed，照它改。
3. Step 7 只以本 workspace 的資料夾與它的 `skillGroups` 根目錄為 `--root`，不再問其他 workspace；SKILL.md、README.md 與兩份中文版一起改，跑 README 列出的檢查。
4. [[rerecord-ste-custom]] 的第 1 步只留 `--root .`；改 chore 這件事記在本 task。
5. [[Task 32]] 的「要做的」那一條改成只找本 workspace。

### 要決定的

- 取代之後，Step 7 要不要告訴使用者：其他 workspace 的依賴方，會在它們下一次依賴巡檢時重記。
  這句話不點名任何一個 workspace。

## 4. 驗證

- asd-ste 的 README 列出的檢查都通過。
- 照新的 Step 7 取代下一份共用檔時，`draft.py dependents` 只給本 workspace 的 `--root`，這裡的 task 日誌沒有寫到 InvestForge。
- `check_chores.py` PASS。

## 5. 與其他 task 的關係

- [[Task 32]]：32.9–32.11 還會跑 Step 7；本 task 做完之前照舊。
- [[Task 55]]：這裡的依賴巡檢 chore；本 workspace 的依賴方由它與 Step 7 重記。
- Task 11 @ InvestForge：建立 InvestForge 的依賴巡檢 chore；建好、跑過一次之後，本 task 才能做。
- [[rerecord-ste-custom]]：第 1 步跟著改。

## 6. 日誌

### 2026-10-30

- [[Task 86]] 把 chore 改用名稱：本檔的 `[[Chore N]]` 連結改成新名稱。

### 2026-10-19

- [[Task 62.5]] 在 InvestForge 開了 Task 11 @ InvestForge，第 1 步與第 5 章寫上它。

### 2026-10-18

- 從 [[Task 62]] 拆出。
- 查到 [[rerecord-ste-custom]] 的第 1 步也會加其他 workspace 的 `--root`，一起列進來。
