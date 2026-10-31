# Task 62.2 - 檢查腳本允許空號，只掃 git 追蹤的檔

**Status**：完成——2026-10-18 兩支檢查腳本允許空號、check 10 改看 git 的檔案清單，規則檔與中文版加上空號那一行的規則；使用者看過。
**Raised**：2026-10-18，[[Task 62]] 拆出的第 2 步：搬走 task 之後這裡會有空號，而在 InvestForge 跑一次檢查要 20 秒。
**Depends on**：—

## 1. 背景

- check 1 要求 task 從 1 連續編到 N，每個 task 的 sub task 從 1 連續編到 M。
  2026-10-18 時在 [check_tasks.py](../.github/common/scripts/check_tasks.py) 的第 196 與 201 行；[check_chores.py](../.github/common/scripts/check_chores.py) 的第 182 行對 chore 也一樣。
- [[Task 62.4]] 搬走 9 個之後，這裡會少 18.1、18.3–18.6、28、29、30 與 37，check 1 就會失敗。
- check 10 為了確認 wikilink 的目標存在，對整個 vault 做 `rglob`（check_tasks.py 第 272 行，check_chores.py 第 201 行）。
  2026-10-18 在 InvestForge 實測：53.8 萬個檔，19.9 秒，其中 InvDatabase 占 35.8 萬；git 追蹤的只有 810 個。
- [[Task 62.1]] 的 task-rules.md 與 chore-rules.md 已照本 task 之後的版本寫編號規則：號碼不重複、可以有空號、用過不再用。

## 2. 現況

### 已決定（2026-10-18）

動手前問了 8 個問題，都照建議：

- 空號記在摘要表：圖例下面一行，逐號列出，例如 `空號：18.1、18.3、28。`；沒有空號就不寫這一行。
  另外在圖例的說明裡寫一句：空號是搬出本 workspace 的 task 留下的號碼，不再使用；不點名搬到哪裡。
- check 1：從 1 到最大編號的每個號碼，不是有檔案，就是在空號那一行，不能兩者都是；sub task 也一樣。
  號碼要寫對、每個只寫一次，空號那一行只能有一行。
- 資料夾裡的 CLAUDE.md 不再是例外：規則是 `tasks/`、`chores/` 裡不放 CLAUDE.md，放了 check 1 就報 FAIL。
- check 10：vault 在 git repo 裡時，只在 git 追蹤或沒被忽略、而且還在的檔裡找 wikilink 的目標；不在 git repo 裡時照舊 `rglob`。
  代價：連到被忽略資料夾（例如 `checkpoints/`）的 wikilink，會報成斷掉。
- 兩支腳本各改一份，照舊只用標準函式庫。
- chore 的摘要表也支援空號那一行。
- task-rules.md 與 chore-rules.md 的 Numbers 一節各加一條：搬走時把號碼寫進空號那一行；中文版跟著改。

### 結果（2026-10-18）

- [check_tasks.py](../.github/common/scripts/check_tasks.py) 與 [check_chores.py](../.github/common/scripts/check_chores.py)：
  - 新的 `read_gaps` 讀空號那一行，check 1 照上面的規則檢查；兩支的 check 1 都不再放過 CLAUDE.md。
  - 新的 `known_names` 以 `git ls-files --cached --others --exclude-standard` 列出檔案，再去掉已刪掉的；不在 git repo 或沒有 git 時改用 `rglob`。
  - docstring 寫明空號那一行、check 1 的新規則，以及 check 10 在 git repo 裡看哪些檔。
- task-rules.md、chore-rules.md 與中文版：Numbers 一節加上空號那一行的規則；`check_ste.py --ste` PASS，`check_parity.py` 0 failure。
  ste-custom.md 有別的 session 還沒 commit 的改動（run 成為專案核准詞），那個 session 也在改兩份規則的 Technical words；兩份的 ste-custom 紀錄不在本 task 重記，留給那個 session 與 [[rerecord-ste-custom]]。

## 3. 要做的

1. ✅ check 1：允許空號，空號記在摘要表的空號那一行；sub task 也一樣。
2. ✅ 新 task 的號碼是用過的最大號碼加 1，最大的可能在空號那一行；規則檔寫明。
3. ✅ check 10：vault 是 git repo 時，只在 git 追蹤或沒被忽略的檔裡找 wikilink 的目標（`git ls-files --cached --others --exclude-standard`）；不是 git repo 時照舊 `rglob`。
4. ✅ 兩支腳本的 docstring 跟著改；[[Task 62.1]] 的規則檔寫的檢查項目也一致。
5. ✅ 使用者看過之後 commit，前綴 `task 62.2`；兩份規則檔照規則只 stage 自己的修改。

## 4. 驗證

- 在 scratchpad 的副本上刪掉幾個 task 檔與它們的列，check 1 PASS；再放一個沒有父 task 的 sub task 檔，check 1 以 1 結束。
- 以 `--vault` 指向 InvestForge 跑一次，幾秒內跑完，找到的斷掉的連結和 `rglob` 的結果相同。
- 這裡的 `check_tasks.py` 與 `check_chores.py` 照舊 PASS。

### 結果（2026-10-18）

- 在 scratchpad 的 12 個副本上跑 check 1，結果都和預期相同：
  - 刪掉 28、29、18.1，沒有空號那一行：FAIL，列出 28、29 與 18.1；加上 `空號：18.1、28、29。`：PASS。
  - 空號那一行有 30，而 30 有檔案：FAIL。
  - `0`、`2x` 與寫了兩次的 28：FAIL，三處都列出。
  - `tasks/` 裡放一個 CLAUDE.md：FAIL。
  - 刪掉 Task 62、把 62 寫進空號，sub task 留著：FAIL，「sub tasks of Task 62, which has no file」。
  - 刪掉最大的 Task 63、把 63 寫進空號：PASS。
  - 兩行空號：FAIL。
  - 空號有 70.1，而 Task 70 不是檔案也不是空號：FAIL。
  - chore：刪掉 Chore 1 沒寫空號 FAIL，寫了 PASS；`chores/` 裡放 CLAUDE.md：FAIL。
- check 10 在一個小 git repo 裡：已追蹤與未追蹤的檔都找得到；被忽略資料夾裡的檔與已刪掉的檔報成斷掉；舊的 `rglob` 版只報已刪掉的那一個。
- 以 `--vault ../InvestForge` 跑這裡的 task：新版 0.2 秒、舊版 20.7 秒，兩邊找到的 859 個斷掉的連結相同。
  在這裡不加 `--vault`：新版 0.11 秒，舊版 0.40 秒。
- 這裡的 `check_tasks.py` 18 項、`check_chores.py` 14 項 PASS。

## 5. 與其他 task 的關係

- [[Task 6]]：`check_tasks.py` 是那時寫的。
- [[Task 53]]：`check_chores.py` 是那時寫的。
- [[Task 62.4]]：搬走 task 之前，要先做完本 task；搬走時把 9 個號碼寫進空號那一行，並在圖例的說明加一句。

## 6. 日誌

### 2026-10-30

- [[Task 86]] 把 chore 改用名稱：本檔的 `[[Chore N]]` 連結改成新名稱。

### 2026-10-18

- 從 [[Task 62]] 拆出。
- 在 InvestForge 量了 `rglob` 的時間：53.8 萬個檔，19.9 秒。
- [[Task 62.1]] 的規則檔已寫好改過之後的編號規則，背景記下這一點：腳本要跟上。
- 開始：問了 8 個問題，見「已決定」。
- 改好兩支腳本、兩份規則檔與中文版，在 scratchpad 驗證過，結果見第 4 章。
- 使用者看過，同意 commit；本 task 完成。
