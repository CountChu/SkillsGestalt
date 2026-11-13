# Task 117 - 修正 check-skill run 261113.3 找到的 3 個 checker 缺陷

**Status**：尚未開始——check-skill run 261113.3 找到的 3 個 checker 缺陷都還沒改。
**Raised**：2026-11-13，[[Task 116]] 重新檢查時找到；使用者決定另開 task，讓 Task 116 修完它的 item 就能結案。
**Depends on**：—

## 1. 背景

[[Task 116]] 修好 check-skill 的 10 個 checker 缺陷之後，以 check-skill run 261113.3 再檢查 check-skill、compile-skill 與 gen-skill，6 個 check 全做。
那次報告另外列出 3 個 checker 缺陷，記在本 task。
checker 缺陷是 check-skill 自己的問題：它讓 check 漏判或誤判，但不計入任何 skill 的 finding。
check-skill 不寫 MD report，那次的報告只在對話裡，所以每一項的重點都寫在第 3 章的表裡；行號是 commit `0db8a03` 的。

## 2. 結論

—

## 3. 過程

### 2026-11-13 提出時的狀態

**表 1：run 261113.3 找到的 checker 缺陷**

| # | 在哪裡 | 缺陷 | 例子 |
| --- | --- | --- | --- |
| 1 | `scan_skill.py:76` 的 `FILE_LITERAL` | 檔名有大括號就不算 literal，所以 `step_{N}.yaml` 從不被記錄，而它正是準則 4.1 自己的例子 | check-skill、compile-skill 與 gen-skill 的 **Step file** 都得到 `literals: []` |
| 2 | SKILL.md:294 的 check 4 輸入，準則 4.4 與 4.6 | check 4 只讀 `terminology` fact group，裡面只有含 term 字詞的行；沒用 term 的表格標頭、換了說法重述的定義，都不在任何 fact 裡 | check-skill SKILL.md:224 的 **Skills table** 與它的欄位 |
| 3 | SKILL.md:295 與 :36，準則 5.7 | Step 3 的表說 check 5 不讀 fact group，**facts file** 的定義也只列 check 1、2、4、6；準則 5.7 卻要讀 `template_shape.working_dir` | run 261113.3 為 5.7 讀了它 |

## 4. 要做的

1. 先讀 check-skill 的 [README.md](../skill-groups/common/skills/check-skill/README.md)，照 When the Skill Is Changed 一起改；中文版照 [chinese](../skill-groups/common/skills/chinese/SKILL.md) skill 更新。
2. 修表 1 的 3 項。
   準則的措辭改動會影響每個 Forge 的檢查結果，先列出要改的文字請使用者確認；掃描器的修正先以改之前的 facts 為基準比對。
3. 改完之後，以 `/check-skill check-skill, compile-skill, gen-skill` 6 個 check 全做，確認這些缺陷不再出現；這次檢查也清掉 [[Task 116]] 結案時留下的 needs check。

## 5. 驗證

- 改之前與改之後的 facts 比對：`step_{N}.yaml` 記成 literal，其他 fact 沒有意外的變化。
- check-skill README 列的檢查都通過：掃描 asd-ste、gen-skill、check-skill，`check_parity.py` 沒有 `[FAIL]`，`depends_on.py check` 都是 UNCHANGED。
- 再跑一次 `/check-skill`，報告沒有再列出表 1 的缺陷。

## 6. 與其他 task 的關係

- [[Task 116]]：在它的重新檢查（run 261113.3）找到這些缺陷，記在它的表 6；它照 Step 6 修的 check-skill、compile-skill 與 gen-skill 在 Skills Dashboard 上會標著 needs check，留給本 task 第 4 章第 3 項的檢查清掉。
- [[Task 54]]：定期以 check-skill 檢查每個 skill 的 chore；這些缺陷修好之後，那個 chore 的結果更可靠。

## 7. 知識

—

## 8. 日誌

### 2026-11-13

- 改名：countdell 上的 SkillsGestalt 已把 Task 103 到 113 用於別的事，所以本 task 由 Task 107 改成 Task 117；Task 104 到 107 依序改成 114 到 117，彼此的連結跟著改，內容不變。
  在這之前的 commit 以 `task 107:` 開頭。
- 提出：[[Task 116]] 重新檢查（run 261113.3）時找到，使用者決定另開 task。
