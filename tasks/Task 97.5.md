# Task 97.5 - 三個 chore 的步驟改成 gestalt 的 skill，並以 hook 提醒

**Status**：取消——跟著 [[Task 97.4]] 取消，SessionStart hook 的提醒也不做；三個 chore 照舊。
**Raised**：2026-11-02，chore 的步驟每個 agency 都一樣，只有何時做與執行紀錄是各 agency 自己的；使用者決定把步驟放進 plugin。
**Depends on**：[[Task 97.4]]

## 1. 背景

- 一個 chore 有三部分：怎麼做（步驟）、何時做（條件）、做到哪（摘要表的「上次執行」與執行紀錄）。
- 步驟可以放在 plugin，所有 agency 共用一份。
- 條件與紀錄留在各 agency 的 repo；紀錄不能寫進 plugin，因為從 GitHub 安裝的 plugin 是複製的，每個版本的路徑不同。
- plugin 可以帶 SessionStart hook，每次 session 開始時跑 script 檢查條件。

## 2. 結論

—

## 3. 過程

### 2026-11-02 的規劃

**表 1：五個 chore 的去向**

| Chore | 誰做 | 去向 |
| --- | --- | --- |
| [follow-gestalt](../chores/follow-gestalt.md) | 每個 Forge | 步驟改成 gestalt 的 skill |
| [keep-english](../chores/keep-english.md) | 有 twin 的 agency | 步驟改成 gestalt 的 skill |
| [rerecord-ste-custom](../chores/rerecord-ste-custom.md) | 有 STE 檔的 agency | 步驟改成 gestalt 的 skill |
| [publish-gestalt](../chores/publish-gestalt.md) | 只有 SkillsGestalt | 留在 `chores/` |
| [pull-gestalt](../chores/pull-gestalt.md) | 只有 SkillsGestalt | 留在 `chores/` |

## 4. 要做的

1. 把三個 chore 的「怎麼做」寫成 `.github/common/skills/` 下的 skill，照 [skill-writing.md](../skill-groups/common/rules/skill-writing.md) 與 SKILL 範本，各有 README 與中文版。
2. 三個 chore 檔只留何時要做，並寫要執行哪個 skill；執行紀錄照舊寫在 `dashboard/chore-summary.md`。
3. 改 [chore-rules.md](../skill-groups/common/rules/chore-rules.md) 與中文版：chore 的步驟可以放在 skill；需要的話，`check_chores.py` 跟著改。
4. 在 gestalt 加 SessionStart hook：跑一支 script，看各 chore 的條件是否成立，成立就提醒；先在 Claude Code 做，VS Code 是否支援 plugin 的 hook 要實測。
5. 在 CHANGES.md 加一筆，讓 Forge 的 chore 檔也改成執行 skill。

## 5. 驗證

- 三個新 skill 的 check-skill 通過，中文版的 parity check 通過。
- `check_chores.py` 通過。
- CHANGES.md 有新條目時，新的 Claude Code session 一開始就提醒該做 follow-gestalt。

## 6. 與其他 task 的關係

- [[Task 97.4]]：建 marketplace 與 gestalt；本 task 的 skill 與 hook 放在它裡面。
- [[Task 97]]：本 task 的上層。

## 7. 知識

—

## 8. 日誌

### 2026-11-02

- 連結的目標路徑從 `../.github/` 改成 `../skill-groups/`，字句沒有改（[[Task 97.7]]）。
- 取消：跟著 [[Task 97.4]] 取消，hook 也不做。
- 提出。
