# Task 66 - README 的共用句子換成 STE 範本的寫法

**Status**：尚未開始——2026-10-19 記下：README-tmp 換成 STE 版之後，asd-ste、check-skill、gen-skill 的 README 與中文版還有 60 行照舊範本抄的共用句子。
**Raised**：2026-10-19，[[Task 32.10]] 以 Step 7 取代 README-tmp 之後，照 [[Task 32]] 的「範本的後續」列出受影響的句子；使用者決定另開本 task，一次改完。
**Depends on**：—

## 1. 背景

gen-skill 寫新 skill 的 `README.md` 時，整份抄 [README-tmp.md](../.github/common/templates/README-tmp.md)，所以每份新格式的 README 都有一批和範本相同的共用句子。
2026-10-19 [[Task 32.10]] 把 README-tmp 換成 STE 版，範本的說法改了，已經寫好的 README 還是舊的說法。
`check_parity.py` 只檢查和範本完全相同的行，所以這些舊句子不會被報出來，也不會再被檢查。

## 2. 現況

### 受影響的行（2026-10-19）

範本的行號指取代前的 README-tmp.md，也就是 commit `3f62423` 那一版。

- [asd-ste/README.md](../.github/common/skills/asd-ste/README.md)：18 行，第 13–16、26–29、159、160、182、204、326、327、429、438、445、475 行。
- [check-skill/README.md](../.github/common/skills/check-skill/README.md)：20 行，第 12–15、24–27、97、98、107、126、181、182、225、229、230、234、235、249 行。
- [gen-skill/README.md](../.github/common/skills/gen-skill/README.md)：22 行，第 11–14、23–26、93、94、104、123、169、173、174、213、215–217、222、223、236 行。
- 三份的中文版各有對應的行。
- 牽涉的範本句子有 22 句：舊範本第 13–16、25–28、68、70、75、86、110、114、115、147、149–151、156、157、172 行。
- 第 18、63、66 行新舊範本相同，不必改。

## 3. 要做的

1. 三份 README 的這些行換成新範本對應的句子，placeholder 換成各 skill 自己的值；中文版照 chinese skill 跟著改。
2. 每份改完，跑它自己 README 列的檢查，並重記記錄它的檔案。
3. SKILL-tmp（[[Task 32.11]]）2026-10-19 已取代；SKILL.md 的共用句子由 [[Task 70]] 處理，不在本 task。

## 4. 驗證

- 三對中英對照 `check_parity.py` 0 failure，`diff_md.py --verify` PASS。
- 三份 README 的 `depends_on.py check` 都是 UNCHANGED；check-skill 的 `scan_skill.py` 沒有新的問題。

## 5. 與其他 task 的關係

- [[Task 32.10]]：取代 README-tmp 之後提出。
- [[Task 32]]：「範本的後續」的規定；Task 32 完成時，範本的後續中 README 的部分交給本 task。
- [[Task 32.11]]：SKILL-tmp 取代之後，SKILL.md 的共用句子交給 [[Task 70]]。
- [[Task 70]]：SKILL.md 的共用句子，和本 task 是同一件事的另一半。

## 6. 知識

—

## 7. 日誌

### 2026-10-19

- 建立。
- SKILL-tmp 已由 [[Task 32.11]] 取代，SKILL.md 的共用句子另開 [[Task 70]]：要做的第 3 項與關係跟著改；[[Task 32]] 完成時，README 的部分交給本 task。
