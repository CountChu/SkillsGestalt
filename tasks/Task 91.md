# Task 91 - chore publish-github 改名為 publish-gestalt

**Status**：完成——2026-10-31 chore 改名為 [[publish-gestalt]]：43 個 wikilink 與 2 個 Markdown 連結改成新名稱，9 個 task 檔各加一行日誌；`publish_snapshot.py` 的 `RESTART` 新舊兩個前綴都認；當時的紀錄照舊。
**Raised**：2026-10-31，[[Task 89]] 加上 [[pull-gestalt]] 之後，使用者提議把發佈的 chore 改名，和 pull-gestalt 成對；討論之後選了 `publish-gestalt`。
**Depends on**：—

## 1. 背景

- `publish-github` 是 SkillsGestalt 的 private chore：把工作分支做成快照，拿掉不公開的路徑並掃描之後，推到 GitHub 上 `CountChu/SkillsGestalt` 的 `main`。
  [[Task 78]] 建立它，[[Task 86]] 把它從 `Chore 3` 改成現在的名稱。
- [[pull-gestalt]] 把 GitHub 上的新快照拿進工作分支，[[follow-gestalt]] 讓 Forge 跟上 Gestalt 的改動；兩個名稱都以 gestalt 指 SkillsGestalt，只有發佈的 chore 以平台 GitHub 命名。
- 使用者先提議 `push-gestalt`；2026-10-31 討論之後保留 publish，理由是：
  - 這個 chore 的重點是公開：先做快照，拿掉 `external/` 與 `.github/external/`，掃描公司內部的資訊，使用者同意之後才推；推只是最後一個 step。
  - pull-gestalt 只改本機，舊的工作分支存在 tag 裡；發佈一推出去就公開了，名稱以 push 和 pull 成對，會讓兩者看起來一樣輕。
  - 其他地方都用 publish：使用者說「發佈」，CLAUDE-local.md 寫 "To publish"，程式是 `publish_snapshot.py`，子指令是 `publish`。
  - 工作分支設了 `pushRemote no_push`；如果之後用私有的 bare repo 讓兩台電腦各推自己的工作分支，push 就有兩種意思。
- [chore-rules.md](../.github/common/rules/chore-rules.md) 的 Names 一節：chore 可以改名，做改名的 task 要改每個連結與執行紀錄；停用的 chore 名稱不再用，因為 commit 前綴會指到兩個 chore。
  改名之後的舊名稱也是同樣的道理：git 歷史裡有 `chore publish-github: ` 開頭的 commit。

## 2. 現況

### 2026-10-31 用到舊名稱的地方

- 下面的行號與個數是 2026-10-31 的；別的 session 也在改這些檔，動手前以 `git grep publish-github` 重新找一次。
- `[[publish-github]]` 的 wikilink 共 42 個：
  - [pull-gestalt](../chores/pull-gestalt.md) 3 個，[摘要表](../dashboard/chore-summary.md) 1 個。
  - [[Task 26]] 2 個、[[Task 78]] 5 個、[[Task 79]] 4 個、[[Task 80]] 1 個、[[Task 86]] 1 個、[[Task 87]] 11 個、[[Task 88]] 1 個、[[Task 89]] 7 個、[[Task 90]] 6 個。
- Markdown 連結：[CLAUDE-local.md](../CLAUDE-local.md) 第 20 行與 [[Task 26]] 第 20 行連到 `chores/publish-github.md`。
  CLAUDE.md 第 74 行是 `gen_claude_md.py` 從 CLAUDE-local.md 產生的。
- chore 檔 `chores/publish-github.md`：標題行，以及第 49、52 行的 commit 前綴 `chore publish-github: `；第 52 行也寫了執行紀錄的小節 `### publish-github`。
- [摘要表](../dashboard/chore-summary.md)：那一列，以及執行紀錄的小節 `### publish-github`。
- [publish_snapshot.py](../.github/common/scripts/publish_snapshot.py) 有 4 處：
  - 第 4 行，開頭的說明。
  - 第 77 行的 `RESTART`：`check` 列出上次發佈之後的 commit 時，以它略過「重新開始」的 commit。
  - 第 194 行，「重新開始」的 commit 的訊息。
  - 第 233 行，`incoming` 印出的 `nothing to pull`。
- 工作分支上已經有舊前綴的「重新開始」commit：本機 `m1` 的 `ce189f1`；另一台電腦的工作分支發佈之後，也會有這樣的 commit。
- 不是連結的舊名稱，照 [[Task 86]] 的前例是當時的紀錄：
  - inline code：[[Task 86]] 的 Status 行、新舊名稱的對照與 `../chores/publish-github.md`，[[Task 87]] 的測試紀錄，以及 [[Task 86]] 寫的 commit 前綴。
  - 純文字：[[Task 89]] 日誌的「publish-github 先做它」，摘要表執行紀錄的「上次 publish-github 的執行紀錄」。
  - [CHANGES.md](../.github/common/CHANGES.md) 第 18 行的舊條目。
- InvestForge、`config.example.yaml`、template `CLAUDE-tmp.md` 與 chore-rules.md 都沒有提到舊名稱。
- repo 之外：這台 Mac 上 Claude 的 memory `branches-m1-main-archive.md` 也提到它。

### 2026-10-31 做完之後

- chore 檔改名為 [publish-gestalt.md](../chores/publish-gestalt.md)：標題行、兩處 commit 前綴與執行紀錄的小節名稱跟著改，關係一章加上本 task，寫明舊名稱與舊前綴。
- 43 個 wikilink 改成 [[publish-gestalt]]：[pull-gestalt](../chores/pull-gestalt.md) 3 個、[摘要表](../dashboard/chore-summary.md) 1 個，其餘在 9 個 task 檔；[[Task 90]] 在本 task 建立之後多了 1 個，所以是 7 個。
- [CLAUDE-local.md](../CLAUDE-local.md) 與 [[Task 26]] 的 Markdown 連結改到 `chores/publish-gestalt.md`；CLAUDE.md 以 `gen_claude_md.py` 重新產生，只差那一行。
- 9 個 task 檔各在日誌的 2026-10-31 加一行：[[Task 26]]、[[Task 78]]、[[Task 79]]、[[Task 80]]、[[Task 86]]、[[Task 87]] 新增這一天，[[Task 88]]、[[Task 89]]、[[Task 90]] 接在當天的最後。
- [摘要表](../dashboard/chore-summary.md)：那一列與執行紀錄的小節改成新名稱；小節裡「上次 publish-github 的執行紀錄」是當時的紀錄，照舊。
- [publish_snapshot.py](../.github/common/scripts/publish_snapshot.py)：開頭的說明、新的「重新開始」commit 的前綴與 `incoming` 的訊息改成新名稱。
  `RESTART` 是 `^chore (?:publish-gestalt|publish-github): \S+ starts again from `，上面的註解說明 publish-github 是舊名稱，工作分支上還可能有它的「重新開始」commit。
- [config.example.yaml](../config.example.yaml) 第 9 行：[[Task 90]] 在本 task 建立之後加上的 `identity` 註解也寫著舊名稱，改成新名稱；本機的 `config.yaml` 沒有提到它。
- 照舊的：inline code、commit 前綴與純文字的紀錄，[CHANGES.md](../.github/common/CHANGES.md) 第 18 行，以及 git 歷史。
- repo 之外：這台 Mac 上 Claude 的 memory `branches-m1-main-archive.md` 改成新名稱，也記下舊名稱與舊前綴。

## 3. 要做的

### 已決定（2026-10-31）

- 新名稱是 `publish-gestalt`；中文標題「發佈到 GitHub」與「何時要做」照舊。
- 以 `git mv` 把 `chores/publish-github.md` 改成 `chores/publish-gestalt.md`，標題行改成 `# publish-gestalt - 發佈到 GitHub`。
- 每個 wikilink 與 2 個 Markdown 連結都改成新名稱：舊的連結找不到檔案，`check_tasks.py` 與 `check_chores.py` 會 FAIL。
- 不是連結的舊名稱照 [[Task 86]] 的前例照舊：inline code、commit 前綴，以及日誌與執行紀錄裡的純文字，都是當時的紀錄。
- 每個改到連結的 task 檔，在當天的日誌加一行，連到本 task。
- chore 檔第 49、52 行的 commit 前綴改成 `chore publish-gestalt: `，執行紀錄的小節改成 `### publish-gestalt`；小節裡的紀錄不改。
- `publish_snapshot.py` 的 `RESTART` 新舊兩個前綴都認：工作分支上還有舊前綴的「重新開始」commit，`check` 要照樣略過它們；新的「重新開始」commit 用新前綴。
- 不在 [CHANGES.md](../.github/common/CHANGES.md) 加條目：這是 private chore，Forge 不做它，也沒有 Forge 提到它；第 18 行的舊條目照舊。
- 新的 chore 檔在「與其他 task、chore 的關係」加一行，寫明舊名稱 `publish-github` 與本 task：在 git 歷史看到舊前綴的人，才找得到這個 chore。
- 改完之後不發佈，等使用者要求；另一台電腦在發佈之後，才會由 [[pull-gestalt]] 拿到改名。
- commit 前綴：`task 91: `。

### 開始做時決定的（2026-10-31）

- [[Task 90]] 在 `config.example.yaml` 加上的註解寫著舊名稱：它說明現在的設定，不是當時的紀錄，所以改成新名稱。
- 全部放在一個 commit：只改檔名、還沒改連結的 commit，`check_tasks.py` 與 `check_chores.py` 會 FAIL。
- 每個 task 檔加的日誌是「[[Task 91]] 把 chore `publish-github` 改名為 `publish-gestalt`：本檔的連結跟著改，意思不變。」
- chore 檔關係一章的那一行，連舊前綴一起寫。
- `RESTART` 上面的註解加一句，說明 publish-github 是舊名稱，免得之後被當成多餘的寫法刪掉。
- [[Task 90]] 是別的 session 的 task：照樣改它的連結、加一行日誌，以 HEAD 加上本 task 的行做成 blob 來 stage。
- 不用 `git mv`：它會馬上把改名放進 index，別的 session 在這之間 commit，就會帶走它；改成在 commit 的同一個指令裡，stage 舊檔的刪除與新檔的 blob，git 一樣記成改名。

### 做法

1. 以 `git grep publish-github` 重新找一次用到舊名稱的地方。
2. 以 `git mv` 改 chore 檔的名稱，改標題行、commit 前綴與執行紀錄的小節名稱，並在關係一章加上舊名稱。
3. 改 [pull-gestalt](../chores/pull-gestalt.md) 與[摘要表](../dashboard/chore-summary.md)：連結，以及執行紀錄的小節名稱。
4. 改 [publish_snapshot.py](../.github/common/scripts/publish_snapshot.py) 的 4 處，`RESTART` 新舊都認。
5. 改 [CLAUDE-local.md](../CLAUDE-local.md) 第 20 行，再跑 `gen_claude_md.py` 重新產生 CLAUDE.md。
6. 改 task 檔的連結，各加一行日誌。
7. 更新這台 Mac 上 Claude 的 memory。
8. 跑「驗證」一章的檢查。

## 4. 驗證

- `check_chores.py`、`check_tasks.py` 與 `gen_claude_md.py --check` 都是 PASS。
- repo 裡沒有 `[[publish-github]]`，也沒有連到 `chores/publish-github.md` 的連結；舊名稱只在 inline code、純文字的紀錄、CHANGES.md 第 18 行與本 task 裡。
- `RESTART` 對新舊兩個前綴的「重新開始」commit 都相符；`publish_snapshot.py check` 列出的 commit 裡沒有 `ce189f1`。
- `reformat_md.py --mode clean` 不改動改過的 chore 檔、摘要表與 task 檔。

2026-10-31 的結果：

- `check_chores.py` 18 passed，`check_tasks.py` 18 passed，`gen_claude_md.py --check` 是 PASS。
- 在 inline code 與 fenced block 以外，repo 裡找不到 `[[publish-github]]`，也找不到連到 `chores/publish-github.md` 的連結。
- `RESTART` 對 `chore publish-github: m1 starts again from main 93b4e1e …` 與 `chore publish-gestalt: m1 starts again from …` 都相符，對 `chore publish-gestalt: the release …` 與 `chore pull-gestalt: …` 不相符；`py_compile` 通過。
- 以改過的程式跑 `publish_snapshot.py check`：以 0 結束，掃描是 nothing found，列出 `m1` 在上次發佈之後的 7 個 commit，其中沒有 `ce189f1`。
- `reformat_md.py --mode clean` 不改動改過的 13 個 md 檔。

## 5. 與其他 task 的關係

- [[Task 78]]：建立這個 chore。
- [[Task 86]]：chore 改用名稱，也定下改名時連結與紀錄的做法；本 task 照它的前例。
- [[Task 89]]：建立 [[pull-gestalt]]；本 task 讓發佈的 chore 和它用同一個名詞。
- [[Task 90]]：同一天改了 `publish_snapshot.py` 與這個 chore，讓快照的作者與 committer 由程式指定。
- [[follow-gestalt]]：Forge 跟上 Gestalt 的 chore，名稱也以 gestalt 指 SkillsGestalt。
- 另一台電腦的 SkillsGestalt：發佈之後，照 [[pull-gestalt]] 拿到改名；它若有還沒發佈的執行紀錄，摘要表可能衝突，pull-gestalt 的 step 7 寫了怎麼處理。

## 6. 知識

—

## 7. 日誌

### 2026-10-31

- 建立 task：使用者提議把 `publish-github` 改名為 `push-gestalt`，討論之後選 `publish-gestalt`；記下用到舊名稱的地方與做法，還沒有開始改。
- 開始做並完成：動手前問了 6 個問題，決定寫在「開始做時決定的」；chore 改名，43 個 wikilink 與 2 個 Markdown 連結改成新名稱，9 個 task 檔各加一行日誌，`publish_snapshot.py` 與 `config.example.yaml` 跟著改；三個檢查都 PASS。
