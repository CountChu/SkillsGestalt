# Task 54 - 建立 Chore 3：定期以 check-skill 檢查每個 skill

**Status**：尚未開始——2026-10-18 記下，等 [[Task 24]] 把其餘 skill 改成新格式之後再做。
**Raised**：2026-10-18，建立 chore 制度（[[Task 53]]）時列出的第三件例行工作：Skills Dashboard 只有 asd-ste 一列，其他 skill 的檢查結果不是還沒有，就是會隨範本與 skill 的修改而過期。
**Depends on**：[[Task 24]]

## 1. 背景

- check-skill 對一個 skill 做 6 項檢查：Template alignment、Config conformance、Description accuracy、Terminology usage、Cross-platform compatibility 與 Dataflow。
  每檢查一次，[update_dashboard.py](../.github/common/skills/check-skill/scripts/update_dashboard.py) 就把結果合併進 Skills Dashboard 中那個 skill 的一列。
- Skills Dashboard 是 wiki 裡的 `dashboard/skills.md`，在 `wikiDir`（iCloud 的 Obsidian vault InvLlmWiki）底下，不在 git 裡。
  repo 裡的 `dashboard/skill-dashboard.html` 是另一份，記的是 skill 的 token 用量。
- 2026-10-18 的現況：表上只有 asd-ste 一列，2026-10-14 檢查，Verdict 是 ❌ 2 · 0——description 超過 1024 字元，也沒提到 Step 6 會啟動審核伺服器。
  SkillsGestalt 的 common 有 31 個 skill、InvestForge 的 dedi 有 17 個，都還沒有列。
- 檢查結果會過期：範本（SKILL-tmp、README-tmp）、skill-writing.md 或 check-skill 的準則一改，每個 skill 都要重查。
  skill 被別的 session 改了，Needs check 不會自動打勾，只有 check-skill 自己的 Step 6 改它時才會標。
- 為什麼等 [[Task 24]]：[[Task 32]] 的 2.10、2.11 會以 STE 版取代兩份範本，Task 24 再把其餘 skill 改成新格式；在那之前全面檢查，多半只會報不符範本。

## 2. 現況

### 已決定（2026-10-18）

- 範圍：common 的 skill；2026-10-19 起不含其他 skill group（[[Task 62.5]]）。
- Skills Dashboard：common 的檢查結果寫進 SkillsLlmWiki 的 `dashboard/skills.md`；`wikiDir` 由根目錄的 [config.yaml](../config.yaml) 給（[[Task 62.6]]）。
- 時機：等 [[Task 24]] 做完再做。
- 提交：本 task 的修改前綴 `task 54`；Chore 3 每次執行的前綴是 `chore 3`。

### 要決定的

- 何時要做：例如範本、skill-writing.md 或 check-skill 的準則改了，或某個 skill 在儀表板的 Checked 日期之後被改過。
- 一次查幾個、先查哪些：common 的 30 個 skill 一次全跑太久，要定分批的大小與先後，例如還沒有列的、Checked 最舊的、Needs check 打勾的。
- 只檢查、不修改：check-skill 的 Step 6 會改 skill；chore 要不要只列出結果，修改另開 task。
- 找過期 skill 的腳本：比對每個 skill 資料夾在 git 裡最後一次修改的日期與儀表板的 Checked，列出該查的。
- 執行紀錄：儀表板不在 git 裡，Chore 3 的執行紀錄要寫什麼，例如這次查了哪些 skill、各自的 Verdict。

## 3. 要做的

1. 照 [chore-rules.md](../.github/common/rules/chore-rules.md) 決定「要決定的」五項，建立 `chores/Chore 3.md` 與摘要表的一列。
2. 需要的話，寫找過期 skill 的腳本。
3. 跑 Chore 3 的第一次。

## 4. 驗證

- `check_chores.py` 與 `check_tasks.py` 都 PASS。
- Chore 3 第一次執行之後，儀表板上有它查過的每個 skill 的一列。

## 5. 與其他 task 的關係

- [[Task 24]]：本 task 依賴它——其餘 skill 改成新格式之後，檢查才有意義。
- [[Task 32]]：Task 24 依賴它——2.10、2.11 以 STE 版取代 README-tmp 與 SKILL-tmp。
- [[Task 53]]：建立 chore 制度；[[Chore 1]] 與 [[Chore 2]] 是前兩個 chore。
- [[Task 40]]：記下 asd-ste 那一列的兩個 ❌，等使用者決定 description 怎麼改。

## 6. 日誌

### 2026-10-20

- 「已決定」加上 Skills Dashboard 的位置：SkillsLlmWiki，由根目錄的 config.yaml 給（[[Task 62.6]]）。

### 2026-10-19

- 範圍改成只有 common 的 skill，「要決定的」的 skill 數跟著改成 30 個（[[Task 62.5]]）。

### 2026-10-18

- 建立：背景記下 Skills Dashboard 的位置與現況；範圍定為兩個 skill group，其餘五項做的時候再決定。
- 第 3 章連到的 `chores/CLAUDE.md` 已刪除，改連 [chore-rules.md](../.github/common/rules/chore-rules.md)（[[Task 62.1]]）。
