# clone-gestalt - 在新電腦上裝 SkillsGestalt

**Status**：使用中——在一台新電腦上 clone GitHub 的 repo，建自己的工作分支並設成不能 push，複製不進 git 的檔，再確認 [[pull-gestalt]] 與 [[publish-gestalt]] 都能跑。
**Started**：2026-11-13，要在一台 DevBox 上也改、發佈 SkillsGestalt，而 CountDell 當初怎麼裝的沒有記下來；由 [[Task 104]] 建立。
**When**：要在一台新電腦上裝 SkillsGestalt，也要在上面改、發佈時
**Private**：只有 SkillsGestalt 做——它 clone 的是 SkillsGestalt 自己的 GitHub repo，還要從原本那台複製不公開的 `publish-keywords.local.txt`。

## 1. 目的

SkillsGestalt 可以在不只一台電腦上改、發佈，每台有自己的工作分支，例如 `m1`、`countdell`、`devbox`。
本 chore 讓一台新電腦第一次裝好 SkillsGestalt，之後就照 [[pull-gestalt]] 跟上別台的快照，照 [[publish-gestalt]] 發佈。
只拿來用、不在上面改的電腦，照 [README.md](../README.md) 的 Getting Started 做就好，不做本 chore。

## 2. 何時要做

- 要在一台還沒有 SkillsGestalt 的電腦上改、發佈 SkillsGestalt 時。
- 這台也要放 Forge 時，先做本 chore，再裝 Forge：Forge 的 `config.yaml` 以 `skillGroups.common` 指到這裡。
- 根目錄已經有 SkillsGestalt 的 clone 時不做，改做 [[pull-gestalt]]。

## 3. 怎麼做

`<work>` 是這台的工作分支，例如 `devbox`；名稱不能是 `main`，也不要和別台的工作分支一樣。

1. 要有 git 與 Python 3.10 以上，以及可以推到 GitHub repo `CountChu/SkillsGestalt` 的 GitHub 帳號；第一次 push 時，Git Credential Manager 會要求登入。
2. 到要放 SkillsGestalt 的目錄。這台也要放 Forge 的話，用 Forge 的 `config.yaml` 裡 `skillGroups.common` 指的位置，例如 `~/WorkArea/Innovation`。
3. `git clone https://github.com/CountChu/SkillsGestalt SkillsGestalt`，再 `cd SkillsGestalt`。
   clone 出來的本機 `main` 已經追蹤 `origin/main`，只放快照，不在上面 commit。
4. `git switch -c <work> main`，再 `git config branch.<work>.pushRemote no_push`。
   從本機的 `main` 建，`<work>` 就不追蹤遠端；`git push` 會失敗，只有 [[publish-gestalt]] 推 `main`。
5. 把 [config.example.yaml](../config.example.yaml) 複製成根目錄的 `config.yaml`，設 `wikiDir`；`config.yaml` 不進 git。
   不要寫 `publish:`。快照的作者是 `identity`，沒寫就是 `publish_snapshot.py` 的 `IDENTITY`，不受這台 git 的 `user.name` 與 `user.email` 影響（[[Task 90]]）。
6. 從原本那台複製這些不進 git、也不公開的檔，不要經過 git：
   - `publish-keywords.local.txt`：沒有它，`publish_snapshot.py` 以 `2` 結束。
   - `external/ASD-STE100_ISSUE9.pdf`：asd-ste 讀它。
   - 有的話，`skill-groups/external/` 的 skill。
7. 建 `.venv`：`python -m venv .venv --prompt Gestalt`，再用 `.venv` 的 python 執行 `-m pip install -r {skillGroups.common}/requirements.txt`（`{skillGroups.common}` 是 `config.yaml` 的 `skillGroups.common`，預設 `skill-groups/common`）；`.venv/` 不進 git。
8. 從根目錄跑 `python {skillGroups.common}/scripts/gen_agents_md.py`，再跑 AGENTS.md 給出的 `check_tasks.py` 與 `check_chores.py`，都要 PASS。
9. 跑 `python {skillGroups.common}/scripts/publish_snapshot.py check` 與 `incoming`：印出 `no change since the last release` 與 `nothing to pull`。
10. 在 `<work>` 上跑 `git push`，要失敗。
11. 在摘要表 `## 執行紀錄` 的 `### clone-gestalt` 下記一筆：哪台電腦、`<work>` 的名稱、clone 到的快照；摘要表的「上次執行」改成當天。
    這一筆在新電腦的 `<work>` 上 commit，commit 以 `chore clone-gestalt: ` 開頭，下次 [[publish-gestalt]] 時發佈。

## 4. 驗證

- `git branch -vv`：`main` 追蹤 `origin/main`；`<work>` 沒有 upstream，`git config branch.<work>.pushRemote` 是 `no_push`。
- `gen_agents_md.py --check`、`check_tasks.py` 與 `check_chores.py` 都是 PASS。
- `publish_snapshot.py check` 的掃描是 `nothing found`，`incoming` 印出 `nothing to pull`。
- `git status` 不列出 `config.yaml`、`.venv/` 與 `publish-keywords.local.txt`。

## 5. 與其他 task、chore 的關係

- [[Task 104]]：建立本 chore；在 scratchpad 照這些步驟從 GitHub clone 過一次。
- [[pull-gestalt]]：裝好之後，用它跟上別台的快照。
- [[publish-gestalt]]：裝好之後，用它發佈。
- [[Task 89]]、[[Task 90]]：另一台電腦的 pull 與快照的身分。
- [[Task 95]]：`.venv` 的建法。
