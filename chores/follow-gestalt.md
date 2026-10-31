# follow-gestalt - 跟上 Gestalt 的改動

**Status**：使用中——Forge 透過 `agencies` 做本 chore，處理 SkillsGestalt 的 `CHANGES.md`；SkillsGestalt 自己不做。
**Started**：2026-10-31，Forge 直接讀 SkillsGestalt，它一改，Forge 就跟著變，卻沒有人告訴 Forge 要做什麼；由 [[Task 88.3]] 建立。
**When**：`{skillGroups.common}/CHANGES.md` 有比上次處理的那一筆新的條目

## 1. 目的

[CHANGES.md](../.github/common/CHANGES.md) 記下 `common` skill group 裡會影響 Forge 的改動，每一筆寫明 Forge 要做什麼。
Forge 照本 chore 定期看它，把新的條目做完，再確認自己的檢查仍然 PASS。

## 2. 何時要做

- 打開 `{skillGroups.common}/CHANGES.md`，看最上面的條目。
- 和摘要表 `## 執行紀錄` 的 `### follow-gestalt` 最新一筆記下的「處理到」比：有更新的條目，就是該做了。
- 還沒做過時，從 Forge 接上 SkillsGestalt 那一天之後的條目做起。

## 3. 怎麼做

1. 照時間先後，讀「處理到」之後的每一筆，照它的「Forge 要做」做。
   要做的事比較多時，在本 agency 的 tasks 開一個 task，在那裡做。
2. 從根目錄執行 `python {skillGroups.common}/scripts/gen_claude_md.py`，重新產生 CLAUDE.md。
3. 執行 CLAUDE.md 給出的 `check_tasks.py` 與 `check_chores.py` 指令，都要 PASS。
4. 在摘要表 `## 執行紀錄` 的 `### follow-gestalt` 下記一筆：處理了哪幾筆、處理到哪一筆（日期與 commit）、開了哪個 task；摘要表的「上次執行」改成當天。
5. 只提交本 agency 自己的檔，前綴 `chore follow-gestalt: `。

## 4. 驗證

- `gen_claude_md.py --check` 是 PASS。
- `check_tasks.py` 與 `check_chores.py` 都是 PASS。
- `CHANGES.md` 裡沒有比「處理到」更新的條目。

## 5. 與其他 task、chore 的關係

- [[Task 88.3]]：建立本 chore 與 `CHANGES.md`。
- [[keep-english]]：另一個給 Forge 做的 chore。
