# Task 92 - 同一天再發佈時，保留較早的歷史

**Status**：尚未開始——2026-10-31 記下：同一天第二次發佈會讓那天的 tag 改指新的歷史，較早的那段這次只靠手動另存的 tag 留著；做法還沒決定。
**Raised**：2026-10-31，[[publish-gestalt]] 當天第二次發佈之前，查到 `archive/m1-261031` 一改指，就有 34 個 commit 沒有任何 ref，其中 14 個 hash 被文件引用；使用者決定先手動另存再發佈，並開這個 task。
**Depends on**：—

## 1. 背景

- 每次發佈之後，`publish_snapshot.py` 把工作分支舊的歷史存成 tag `archive/<work>-<yymmdd>`，日期是發佈當天，再讓工作分支從新的快照重新開始。
- [[Task 79]] 定下一天一個 tag：同一天再發佈，就改指那天的 tag，並印出它原本指的 commit；[publish_snapshot.py](../skill-groups/common/scripts/publish_snapshot.py) 第 193 行的說明也這樣寫。
- tag 一改指，當天較早那次發佈之前的歷史就沒有任何 ref，之後可能被 `git gc` 清掉。
- [CLAUDE-local.md](../AGENTS-local.md) 第 18、19 行卻說：發佈之前的 commit 在這些 tag 裡，文件引用的 hash 到這些 tag 裡找。
  兩者互相矛盾：較早的那段被清掉之後，文件引用的 hash 就找不到了。

## 2. 現況

### 2026-10-31 第二次發佈

- 早上的發佈是 `93b4e1e`，取自 `m1` 的 `b2e967f`，舊的歷史存在 `archive/m1-261031`。
- 第二次發佈之前查到：只有 `archive/m1-261031` 指到的 commit 有 34 個，從 2026-10-30 的 `54647f7` 到 2026-10-31 的 `b2e967f`。
- 其中 14 個 hash 被 repo 的文件引用：
  - [CHANGES.md](../skill-groups/common/CHANGES.md) 2026-10-30 那筆條目的 11 個，Forge 照這筆條目做。
  - [摘要表](../dashboard/chore-summary.md) publish-gestalt 執行紀錄裡的 `b2e967f` 與 `54647f7`。
  - [[Task 82]] 的 `9073897`，[[Task 89]] 的 `b2e967f`。
- 使用者決定先手動另存：發佈之前建立 tag `archive/m1-261031-1`，指向 `b2e967f`，訊息寫明它是第二次發佈改指 `archive/m1-261031` 時留下的。
- 第二次發佈 `65c25e5` 讓 `archive/m1-261031` 改指 `3933273`，程式印出 `archive/m1-261031 moves: it was at b2e967f`；那 34 個 commit 由 `archive/m1-261031-1` 留著。
- 有後綴的 tag 已經有前例：[[pull-gestalt]] 每次 rebase 之前存的 `archive/<work>-<yymmdd>-pull`。

### 查法

- 先列出只有那個 tag 指到的 commit：`git rev-list <tag> --not <其他所有的 ref>`。
- 再找 git 追蹤的 md 檔裡，有沒有 7 到 12 位的 hash 是這些 commit 的開頭。

## 3. 要做的

### 已決定（2026-10-31）

- 這次的發佈先以手動建立的 `archive/m1-261031-1` 保住早上的歷史。
- 以後怎麼做，記在「要決定的」。
- commit 前綴：`task 92: `。

### 要決定的

- 同一天再發佈時，較早的 tag 怎麼命名：例如依序加 `-1`、`-2`，或每次發佈都以快照命名。
- 由 `publish_snapshot.py` 自己另存，或寫進 [[publish-gestalt]] 的 step。
- [CLAUDE-local.md](../AGENTS-local.md) 的「一天一個 tag」與 chore 檔的說明怎麼改。
- 要不要有一個檢查：文件引用的 hash 都找得到某個 tag 或分支，例如把上面的查法寫成程式。
- CHANGES.md 引用的是 `m1` 的 hash，只有這台電腦的 SkillsGestalt 查得到；別台電腦的 Forge 要不要改成引用快照。

### 做法

1. 決定「要決定的」各項。
2. 改 `publish_snapshot.py` 或 chore 的 step，以及 CLAUDE-local.md，再跑 `gen_claude_md.py`。
3. 在暫用的 clone 試同一天發佈兩次：兩次發佈之前的歷史都有 tag 指到。

## 4. 驗證

- 同一天發佈兩次之後，兩次發佈之前的歷史都還有 tag 指到。
- `check_chores.py`、`check_tasks.py` 與 `gen_claude_md.py --check` 都是 PASS。

## 5. 與其他 task 的關係

- [[Task 79]]：定下發佈之後重做 `m1`，以及一天一個 tag。
- [[Task 88.3]]：CHANGES.md 的條目引用 `m1` 的 hash。
- [[Task 89]]：[[pull-gestalt]] 的 `-pull` tag，是有後綴的前例。
- [[Task 91]]：改名之後的這次發佈，查到這個問題。
- [[publish-gestalt]]：執行紀錄記下這次的手動另存。

## 6. 知識

—

## 7. 日誌

### 2026-11-02

- 連結的目標從 `CLAUDE-local.md`、`CLAUDE-tmp.md`、`gen_claude_md.py` 改成改名後的 `AGENTS-local.md`、`AGENTS-tmp.md`、`gen_agents_md.py`，字句沒有改（[[Task 97.2]]）。
- 連結的目標路徑從 `../.github/` 改成 `../skill-groups/`，字句沒有改（[[Task 97.7]]）。

### 2026-10-31

- 建立 task：第二次發佈之前，查到 `archive/m1-261031` 改指會讓 34 個 commit 沒有任何 ref，其中 14 個 hash 被文件引用；使用者決定先手動另存成 `archive/m1-261031-1` 再發佈，以後的做法另外決定。
