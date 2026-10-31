# Task 83 - CLAUDE.md 裡 common 的路徑要和 config.yaml 一致

**Status**：完成——2026-10-30 先寫了 `check_claude_md.py`，後來被 [[Task 84]] 取代；重新打開之後，[gen_claude_md.py](../.github/common/scripts/gen_claude_md.py) 加上開頭的插入點，連到 common 的連結改成相對路徑。
**Raised**：2026-10-30，使用者指出 CLAUDE.md 寫死了 `.github/common/rules/agency-rules.md`，而路徑應該由 `config.yaml` 決定。
**Depends on**：[[Task 82]]

## 1. 背景

[[Task 82]] 把每個 agency 共通的規則抽成 `agency-rules.md`，本 repo 的 [CLAUDE.md](../CLAUDE.md) 以一個 Markdown 連結加一行 `@` import 引入它。
這兩處都寫了實際路徑 `.github/common/rules/agency-rules.md`；Settings of This Agency 一節的 `{skillGroups.common}` 的值與兩條檢查指令也是。
而 `{skillGroups.common}` 的值由根目錄的 `config.yaml` 決定：`config.yaml` 一改，CLAUDE.md 的這些路徑就不對了，沒有東西會發現。

不能直接在 CLAUDE.md 寫 `{skillGroups.common}/rules/agency-rules.md`：

- `@` import 由 Claude Code 在 session 開始時讀檔，它不懂 `{skillGroups.common}`，也不讀 `config.yaml`；寫成佔位符就找不到檔，而且不報錯，共用規則等於沒有載入。
- Markdown 連結寫成佔位符也打不開。
- 只有 agent 讀到的文字能用佔位符，由 agent 查 `config.yaml` 展開；但這樣規則不會自動載入。

## 2. 現況

- 本 repo 的 CLAUDE.md 有四處由 `config.yaml` 決定、但寫成實際路徑：`@` import 那一行、agency-rules.md 的連結、`{skillGroups.common}` 的值、兩條檢查指令。
- `check_claude_md.py` 檢查五項：config（`skillGroups.common` 有設、資料夾存在）、import、link、value、commands；路徑展開 `~`、解析相對路徑之後才比，`@` 與連結以 CLAUDE.md 的資料夾為準，值與指令以 `config.yaml` 的資料夾為準；`@` 指向的檔與指令的 script 也要存在；找不到某一處算 FAIL。
- 參數 `--claude` 與 `--config`，預設是 `CLAUDE.md` 與 `config.yaml`；輸出和 `check_tasks.py` 一樣，每項一行，最後是 verdict；0 通過、1 有 FAIL、2 檔案缺或讀不了。
- 本 repo 的 CLAUDE.md：「Follow agency-rules.md」的下一句註明它的路徑是 `{skillGroups.common}/rules/agency-rules.md`，由 `check_claude_md.py` 確認和 `config.yaml` 一致；Settings of This Agency 加上 `check_claude_md.py` 的指令。
- `agency-rules.md` 與中文版的開頭加上：改了 `CLAUDE.md` 或 `config.yaml` 之後，執行 `CLAUDE.md` 給出的 `check_claude_md.py` 指令。

### 2026-10-30 重新打開之後

- 評估 InvestForge 接上 [[Task 84]] 的機制時發現兩點：模板只有最後一個插入點，InvestForge 的設定說明會排在共用規則後面；`skillGroups.common` 是 `~/…` 時，Markdown 連結裡的 `~` 點不開。
- [CLAUDE-tmp.md](../.github/common/templates/CLAUDE-tmp.md) 在引言與 `gen_claude_md.py` 指令之後、`## Markdown` 之前加一行 `{CLAUDE-local-top}`。
- [gen_claude_md.py](../.github/common/scripts/gen_claude_md.py)：
  - `CLAUDE-local.md` 裡獨佔一行的 `{CLAUDE-local}` 把它分成兩段：以上放進 `{CLAUDE-local-top}`，以下放進 `{CLAUDE-local}`；沒有這一行就全部放在結尾，開頭的插入點連同它的空行拿掉。
  - 連結目標以 `{skillGroups.X}` 開頭、而那個值是絕對路徑或 `~` 開頭時，改寫成從根目錄起算的相對路徑；算不出相對路徑（例如 Windows 上不同磁碟）就照 `config.yaml` 寫的值。
    指令與 inline code 照舊用 `config.yaml` 寫的值。

## 3. 要做的

### 已決定（2026-10-30）

- CLAUDE.md 的 `@` 與連結照舊寫實際路徑；Forge 寫絕對路徑，`@` 支援 `~`。
- 在 `@` 的上一句旁邊註明這個路徑是 `{skillGroups.common}/rules/agency-rules.md`，由 `check_claude_md.py` 檢查。
- 新寫 `{skillGroups.common}/scripts/check_claude_md.py`：讀 `config.yaml` 的 `skillGroups.common`，展開之後比對 CLAUDE.md 的這四處，不一致就 FAIL：
  - `@` import 那一行。
  - agency-rules.md 的 Markdown 連結。
  - Settings of This Agency 寫出的 `{skillGroups.common}` 的值。
  - 兩條檢查指令（`check_tasks.py`、`check_chores.py`）的路徑。
- 程式寫成每個 agency 都能用：相對路徑與 `~` 開頭的絕對路徑都要處理；本 task 只改本 repo，Forge 在自己的 tasks 接上。
- 改 CLAUDE.md 或 `config.yaml` 之後就跑：寫進 `agency-rules.md` 與中文版，和 `check_tasks.py` 一樣是「改完就跑」；指令寫在各 agency 的 CLAUDE.md 的 Settings of This Agency。

### 開始做時決定的（2026-10-30）

- 路徑展開成絕對路徑再比，不比字串；`.github/common` 與 `./.github/common` 算一致。
- CLAUDE.md 找不到四處之一就是 FAIL。
- 「檢查指令」是每一條 `python …/scripts/<name>.py`，之後加的 `check_claude_md.py` 自己也在內。
- 也確認 `@` 指向的檔存在：路徑一致但檔不在，規則一樣沒有載入。
- 來源說明另起一句，寫在「Follow agency-rules.md」的下一句。

### 重新打開時決定的（2026-10-30）

- 插入點用做法 B：開頭與結尾各一個，`CLAUDE-local.md` 以一行 `{CLAUDE-local}` 分段；開頭的插入點在引言與指令之後、`## Markdown` 之前。
- 連結用做法 C：只有 Markdown 連結的目標改成相對路徑，不含帳號名稱；算不出來就照 `config.yaml` 寫的值。
- 記在本 task：使用者決定重新打開本 task。
- 做完之後通知正在做 InvestForge Task 13 的 session。

### 步驟

1. 寫 `check_claude_md.py`，在本 repo 與一份改過 `config.yaml` 的暫用副本上試跑：一致時 PASS，不一致時 FAIL 並指出哪一處。
2. 本 repo 的 CLAUDE.md：在 `@` 的上一句加上來源說明，Settings of This Agency 加上 `check_claude_md.py` 的指令。
3. agency-rules.md 與中文版：加上「改 CLAUDE.md 或 `config.yaml` 之後，執行 CLAUDE.md 給的 `check_claude_md.py` 指令」。

## 4. 驗證

- 本 repo 跑 `check_claude_md.py` 是 PASS。
- 把暫用副本的 `skillGroups.common` 改成別的值，四處都各報一個 FAIL。
- CLAUDE.md 與 agency-rules.md `check_ste.py` 是 PASS，agency-rules.md 與中文版 `check_parity.py` 是 0 failure。

2026-10-30 的結果：

- 本 repo：`check_claude_md.py` 5 passed，0 failed。
- 暫用副本把 `skillGroups.common` 改成 `other`：import、link、value、commands 四項都是 FAIL，各指出哪一行。
- 暫用副本照 Forge 的寫法，`config.yaml` 與 CLAUDE.md 都用 `~` 或 `/Users/...` 開頭的絕對路徑：5 passed。
- `config.yaml` 沒有 `skillGroups.common`：config 一項 FAIL。
- CLAUDE.md 與 agency-rules.md 的 `check_ste.py` 都是 PASS；agency-rules.md 與中文版 `check_parity.py` 是 0 failure，`diff_md.py --verify` 確認中文版只改了新加的那一行；`reformat_md.py --mode clean` 不改動。

重新打開之後的結果（2026-10-30）：

- 本 repo：`gen_claude_md.py --check` 照舊是 PASS，產生的 CLAUDE.md 一個字都沒變，沒有連續三個換行。
- 模擬的 InvestForge（它的 `config.yaml`，加上分成兩段的 `CLAUDE-local.md`）：Workspace configuration 與 Skills 排在 `## Markdown` 之前，Python environment 與 Settings 排在 `## Chores` 之後；`{{skillGroups.g}}` 留成 `{skillGroups.g}`。
- 以 InvestForge 的真實位置計算連結的起點，得到 `../SkillsGestalt/.github/common`；SkillsGestalt 自己照舊是 `.github/common`。
- 模板 `check_ste.py` 是 PASS，`reformat_md.py --mode clean` 不改動。

## 5. 與其他 task 的關係

- [[Task 84]]：取代本 task 的做法。
- [[Task 82]]：建立 agency-rules.md 與 CLAUDE.md 的 `@` import；本 task 確保它的路徑對。
- InvestForge 與 BookMaster 的 CLAUDE.md 接上 `check_claude_md.py`，在它們自己的 tasks 做。

## 6. 日誌

### 2026-10-30

- 建立 task：路徑照舊寫實際值，文字註明來源，加 `check_claude_md.py` 檢查它和 `config.yaml` 一致。
- 開始做並完成：寫好 `check_claude_md.py` 並試跑四種情況，CLAUDE.md 註明來源並給出指令，agency-rules.md 與中文版加上「改完就跑」。
- [[Task 84]] 以 `gen_claude_md.py --check` 取代 `check_claude_md.py`，後者刪掉；本檔指向它的連結改成純文字。
- 重新打開：評估 InvestForge 時發現插入點與 `~` 連結兩個問題；`gen_claude_md.py` 加上開頭的插入點與相對連結，以模擬的 InvestForge 試過；完成。
