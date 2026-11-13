# clean-checkpoints - 清理 checkpoints\ 的舊項目

**Status**：使用中——`checkpoints\` 超過門檻時，用 skill `clean-checkpoints` 列出舊的項目，使用者確認後送到資源回收筒。
**Started**：2026-11-12，run-data-rules.md 說 `checkpoints\` 的項目都可以手動移除，但沒有固定的做法，一個 Forge 的 `checkpoints\` 半年累積到約 18 GB；由 [[Task 103]] 建立。
**When**：checkpoints\ 超過 config.yaml 的 cleanCheckpoints.maxSizeGB（沒寫時 10 GB）

## 1. 目的

[run-data-rules.md](../skill-groups/common/rules/run-data-rules.md) 規定 Working Dir 可以放在 `checkpoints\`，也說 `checkpoints\` 的每個項目都可以手動移除；但每次執行會多一個資料夾，沒人清就一直長大。
本 chore 決定何時清；怎麼列、怎麼移，由 skill [clean-checkpoints](../skill-groups/common/skills/clean-checkpoints/SKILL.md) 做。
不清的項目：設定的 `keep` 裡的 skill 資料夾（別的 skill 還會讀）、還沒完成的 task 提到的項目、`checkpoints\chores\`，以及最新的檔案還在保留天數內的項目。

## 2. 何時要做

- `checkpoints\` 超過執行的 agency 的 `config.yaml` 裡 `cleanCheckpoints.maxSizeGB`；沒寫時是 10 GB。
- 看出該做了：從 workspace 的根目錄跑 `python {skillGroups.common}/skills/clean-checkpoints/scripts/clean_checkpoints.py list --run <yymmdd>.<N>`，第一行印出 `over`，就是該做了；印出 `not over` 就不用做。
  這個指令只列出、不移任何東西；`<yymmdd>.<N>` 用當天沒用過的號碼，例如 `261112.1`，結果在 `temp\clean-checkpoints\<yymmdd>.<N>\items.yaml`。
- 別的 agency 也照本 chore 做：每個 agency 在自己的根目錄執行，只清自己的 `checkpoints\`，設定與執行紀錄留在自己那裡，見 [chore-rules.md](../skill-groups/common/rules/chore-rules.md)。
  `{skillGroups.common}` 照執行的 agency 的 `config.yaml` 代換。

## 3. 怎麼做

1. 確認執行的 agency 的 `config.yaml` 有 `cleanCheckpoints`（範例在 SkillsGestalt 的 [config-tmp.yaml](../config-tmp.yaml)）；別的 skill 還會讀的資料夾要先寫進 `keep`。
2. 跑 skill：`/clean-checkpoints`。
   - Step 1 列出每個項目與理由；沒超過門檻就停。
   - Step 2 給使用者看可以清的項目，問要全部、部分或都不要；使用者沒說要的一律不動。
   - Step 3 只把使用者確認、而且當下仍可以清的項目送到資源回收筒；不直接刪除。
3. 在執行的 agency 自己的摘要表，`## 執行紀錄` 的 `### clean-checkpoints` 下寫：清理前的大小、門檻、送到資源回收筒的項目數與大小、略過或失敗的項目，以及 skill 的 run record；摘要表的「上次執行」改成當天。
4. `checkpoints\` 與 `temp\` 都不在 git，所以只提交執行的 agency 自己的摘要表，前綴是 `chore clean-checkpoints: `；再跑 `check_chores.py`。

## 4. 驗證

- `clean_checkpoints.py list --run <yymmdd>.<N>` 印出 `not over`，或剩下的都是不清的項目。
- 資源回收筒裡有這次送進去的項目，確認後才清空資源回收筒。
- `check_chores.py` PASS。

## 5. 與其他 task、chore 的關係

- [[Task 103]]：建立本 chore 與 skill `clean-checkpoints`。
- [[Task 100]]：定了 Checkpoint Dir 與 Temp Dir 的規則，寫成 run-data-rules.md。
