# Task 82 - 把每個 agency 共通的 CLAUDE.md 規則抽成 common 的一份規則檔

**Status**：完成——2026-10-30 寫好 `agency-rules.md` 與中文版；本 repo 的 CLAUDE.md 以 Markdown 連結加 `@` import 引入，只留本 repo 的值與 Branches；InvestForge 與 BookMaster 要在它們自己的 tasks 改。
**Raised**：2026-10-30，比較本 repo 與 InvestForge 的 CLAUDE.md：共通的規則兩邊各寫一份，本 repo 改了 twins 一節之後，InvestForge 沒跟上。
**Depends on**：—

## 1. 背景

- 每個 agency 的根目錄都有自己的 CLAUDE.md；各 repo 是並排的資料夾，Claude Code 只載入自己 repo 的那一份。
- 共通的規則現在每份 CLAUDE.md 各寫一份，改一處就要記得改其他處。
- 使用 `common` 的 Forge 目前有 InvestForge 與 BookMaster（兩邊的 `config.yaml` 都指向本 repo 的 `.github/common`）。
- Claude Code 的 CLAUDE.md 支援 `@路徑` import；但整份引用本 repo 的 CLAUDE.md 不行：
  - 只能整份引用，Branches 一節（在 `m1` 工作、不在 `main` commit）會一起帶進 Forge。
  - 路徑寫死 `.github/common`、檢查指令「從根目錄執行」，在 Forge 會找不到檔。
  - 寫的是本 repo 的值：`{skillGroups.common}` 是 `.github/common`、keep-English 稽核是 [[keep-english]]、`config.example.yaml`。
  所以共通的規則要寫成一份不綁定任何 agency 的檔。

## 2. 現況

### 2026-10-30 比較的結果

本 repo 的 [CLAUDE.md](../CLAUDE.md) 在 `9073897`；InvestForge 的在它自己的 `a917362`。

| 規則 | 本 repo | InvestForge |
| --- | --- | --- |
| twins：同一次改 twin、用 chinese skill | 有 | 有 |
| twins：留英文的 term、清單換版本做 keep-English 稽核 | 有（[[keep-english]]） | 沒有 |
| 寫 Markdown 照 md-style.md | 有 | 沒有 |
| Tasks：task-rules.md 與 `check_tasks.py` | 有，路徑寫死 | 有，路徑用 `{skillGroups.common}` |
| Chores：chore-rules.md 與 `check_chores.py` | 有，路徑寫死 | 有，路徑用 `{skillGroups.common}` |
| Branches | 只有本 repo | — |

### 2026-10-30 做完之後

- `agency-rules.md` 與 `agency-rules-tw.md`：開頭說明各 agency 的 CLAUDE.md 引用本檔、不寫任何 agency 的值；四節是 Markdown、繁體中文 twins、Tasks、Chores。
- 本 repo 的 [CLAUDE.md](../CLAUDE.md)：一句「Follow agency-rules.md」加 Markdown 連結，下一行 `@.github/common/rules/agency-rules.md`；新的一節 Settings of This Agency 先說 agency-rules.md 用到這些設定，再寫出 `{skillGroups.common}` 是 `.github/common`、`config.example.yaml`、keep-English chore 是 [[keep-english]]，以及兩條可以直接執行的檢查指令；Branches 照舊。

## 3. 要做的

### 已決定（2026-10-30）

- 共用檔放在 `.github/common/rules/`，和 task-rules.md、chore-rules.md 一起。
- 內容只放每個 agency 都適用的規則：twins（含 keep-English）、md-style、Tasks、Chores。
- 不綁定 agency：路徑一律寫 `{skillGroups.common}`；keep-English 稽核的 chore 不寫編號，由各 agency 的 CLAUDE.md 寫出。
- 照本 repo 的規定，以 STE 寫，過 `check_ste.py`，另有 `-tw.md` 中文版。

### 開始做時決定的（2026-10-30）

- 檔名是 `agency-rules.md`，對上 [[Task 81]] 術語表的 agency。
- `@` 沒被展開時：CLAUDE.md 先有一句「Follow agency-rules.md」與 Markdown 連結，下一行才是 `@` import，兩種 agent 都找得到。
- 本 repo 的 CLAUDE.md 留兩條實際路徑的檢查指令，照 task-rules.md 與 chore-rules.md「CLAUDE.md 給出實際路徑的指令」的要求；共用檔只說執行 CLAUDE.md 給的指令。
- 「這份檔是各 agency 的 CLAUDE.md 引用的」只寫在共用檔自己的開頭，README 與術語表不改。
- CLAUDE.md 不在 header quote 記共用檔的指紋：`@` 每次都載入最新的。
- 共用檔照本 repo 原本的句子，只去掉綁定的值；md-style 獨立一節 Markdown。

### 步驟

1. 寫共用檔與中文版。
2. 本 repo 的 CLAUDE.md：刪掉 twins、Tasks、Chores 三節與 md-style 一條，改成一行 `@` import；只留本 repo 的值（`{skillGroups.common}` 是 `.github/common`、keep-English 稽核是 [[keep-english]]、`config.example.yaml`）與 Branches。
3. 共用檔之後一改，所有 Forge 都跟著變；在共用檔自己的開頭註明這份檔是各 agency 的 CLAUDE.md 引用的。

## 4. 驗證

- 共用檔 `check_ste.py` 是 PASS，與中文版 `check_parity.py` 是 0 failure。
- 本 repo 的 CLAUDE.md 載入後，原本的每一條規則都還在，`check_tasks.py` 與 `check_chores.py` 照舊能跑。
- 共用檔裡沒有寫死的 `.github/common`，也沒有本 repo 的 chore 編號。

2026-10-30 的結果：

- `agency-rules.md` 與本 repo 的 CLAUDE.md，`check_ste.py` 都是 PASS；`reformat_md.py --mode clean` 不改動；兩份的 `depends_on.py` header quote 都記好了。
- `agency-rules.md` 與中文版 `check_parity.py` 是 0 failure。
- 共用檔與中文版裡找不到 `.github/common`、`Chore` 加編號、SkillsGestalt 或 InvestForge。
- 把改之前的 CLAUDE.md 每一句和「新的 CLAUDE.md 加上共用檔」對照：每一條規則都還在，不同的只有連結路徑，以及綁定的值搬到 Settings of This Agency。
- `check_tasks.py` 與 `check_chores.py` 照新的 CLAUDE.md 的指令執行，都是 PASS。
- 還沒在新的 Claude Code session 實際確認 `@` 有被展開：下一個在本 repo 開始的 session 會載入它。

## 5. 與其他 task 的關係

- [[Task 84]]：取代本 task 的做法。
- [[Task 80]]：把 CLAUDE.md 改寫成英文；本 task 改的是同一份檔。
- [[Task 81]]：術語表定義了 agency、Gestalt 與 Forge；共用檔用這些名稱。
- InvestForge 與 BookMaster 的 CLAUDE.md 要改成引用共用檔，在它們自己的 tasks 開 task，不在本 task 改。

## 6. 知識

—

## 7. 日誌

### 2026-10-30

- 建立：比較本 repo 與 InvestForge 的 CLAUDE.md，決定把共通的規則抽成 common 的一份規則檔；檔名與 `@` 沒被展開時的對策還沒決定。
- 開始做並完成：檔名 `agency-rules.md`，CLAUDE.md 用連結加 `@` 引入，留本 repo 的值、兩條檢查指令與 Branches。
- CLAUDE.md 的 Values of This Agency 改名為 Settings of This Agency，開頭加一句說明 agency-rules.md 用到這些設定；agency-rules.md 與中文版指整組設定的 value 改成 setting，`{skillGroups.common}` 的值照舊叫 value。
- [[Task 84]] 改成由模板 `CLAUDE-tmp.md` 與 `CLAUDE-local.md` 產生 CLAUDE.md：`agency-rules.md` 與中文版刪掉，共用規則搬進模板；本檔指向它們的連結改成純文字。
- [[Task 86]] 把 chore 改用名稱：本檔的 `[[Chore N]]` 連結改成新名稱。
