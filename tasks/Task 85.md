# Task 85 - 讓 Forge 像使用 skill 一樣使用本 agency 的 chore，以 {agencies.X} 定位

**Status**：完成——2026-10-30 [chore-rules.md](../.github/common/rules/chore-rules.md) 與中文版加上「使用檔」的規則與 `agencies` 設定；[[keep-english]] 不再綁定本 agency，報告搬到 `checkpoints/chores/keep-english/`；`check_chores.py` 與 `gen_claude_md.py` 不必改。
各 Forge 改用 Chore 2，在它們自己的 tasks 做。
**Raised**：2026-10-30，比較本 agency 的 [[keep-english]] 與 InvestForge 的 keep-English 稽核：兩份逐字幾乎相同，只差稽核哪一邊的檔；使用者希望 chore 的用法和 skill 一樣，定義在一處，各 agency 拿來用。
**Depends on**：—

## 1. 背景

- skill 定義在 `{skillGroups.common}/skills/`，只有一份；每個 workspace 在自己的根目錄執行它，它只處理那個 workspace 的檔，checkpoints 也留在那裡。
- chore 現在每個 agency 各寫一份：[[keep-english]] 是本 agency 的 keep-English 稽核；[[Task 62.5]] 把它的範圍縮回本 agency 之後，InvestForge 另寫了一份幾乎相同的。
  兩份會各自分岔，和 [[Task 82]] 之前的 CLAUDE.md 一樣。
- `{skillGroups.common}` 指的是 skill group（`.github/common`），不是 agency 的根目錄；chore 在 agency 根目錄的 `chores/`，跟著 agency 走，不屬於 skill group。
- [chore-rules.md](../.github/common/rules/chore-rules.md) 已允許一個 workspace 引用它所用的 skill group 所在 workspace 的 chore，文字寫成 `Chore N @ <workspace>`；不允許反方向。
  所以 Forge 使用本 agency 的 chore 合乎現行規則；本 agency 不知道哪些 Forge 在用。

## 2. 現況

### 2026-10-30 [[keep-english]] 綁定本 agency 的地方

- 路徑寫死 `.github/common/…`。
- 報告目錄 `checkpoints/chores/chore-2/`，帶著本 agency 的編號。
- 「3. 怎麼做」的第 5 步：只提交 Chore 2 與摘要表，前綴 `chore 2: `。
- 「6. 執行紀錄」是本 agency 的；「5. 關係」裡的 [[Task 73]] 是本 agency 記要改的譯法的 task。

### 現行工具

- `check_chores.py`：摘要表每一列是 `[[Chore N]]`，對到本 agency `chores/` 裡的檔。
- `gen_claude_md.py`：`keepEnglishChore: Chore N` 換成 `[Chore N](chores/Chore%20N.md)`，只連到本 agency；`{skillGroups.X}` 的連結會改寫成從根目錄起算的相對路徑。

### 2026-10-30 做完之後

- [chore-rules.md](../.github/common/rules/chore-rules.md) 與中文版新增一節 A Chore of a Different Workspace：
  - 要做另一個 workspace 的 chore，在自己的 `chores/` 放一個使用檔，編號是自己的；1 到 4 章各一行「照 Chore N @ <agency> 的同一章」，第 1 章另寫 `{agencies.<agency>}/chores/Chore N.md`；「6. 執行紀錄」記自己的執行，摘要表照常有一列。
  - `config.yaml` 的 `agencies` 給出那些 agency 的根目錄。
  - 有不只一個 workspace 在做的 chore，第 1 到 4 章不寫任何一個 workspace 的值：路徑寫 `{skillGroups.common}`，報告目錄的名稱不含 chore 編號；每個 workspace 在自己的根目錄做，報告、執行紀錄與 commit 留在自己那裡。
- [[keep-english]]：兩條指令改寫 `{skillGroups.common}`，報告目錄改成 `checkpoints/chores/keep-english/`；「2. 何時要做」加上「別的 agency 也照本 chore 做」與 `{skillGroups.common}` 照執行的 agency 的 `config.yaml` 代換；「3. 怎麼做」的第 2、4、5 步改成執行的 agency 自己開 task、寫自己的執行紀錄、以自己的編號提交。
- 舊的兩份報告搬到 `checkpoints/chores/keep-english/`，執行紀錄裡的路徑跟著改並註明搬過。
- 原本以為 [[keep-english]] 的「5. 關係」有 [[Task 73]]，其實它只在「6. 執行紀錄」，所以不必搬。

### 2026-10-30 加上 checkpoints 的路徑規則

- 使用者要求：chore 若要 checkpoints，路徑是 `checkpoints/chores/<agency>/chore-<N>`。
- `<agency>` 與 `<N>` 指寫出 step 的那個 chore：Chore 2 @ SkillsGestalt 一律是 `checkpoints/chores/SkillsGestalt/chore-2`，別的 agency 用使用檔來做時，也在它自己的根目錄下用同一個路徑；所以定義裡可以直接寫這個路徑。
- 這條規則適用於每個用到 checkpoints 的 chore，寫在 [chore-rules.md](../.github/common/rules/chore-rules.md) 與中文版的 The Chore File 一節；它取代上面「報告目錄的名稱不含 chore 編號」那一句。
- [[keep-english]] 的兩條指令與執行紀錄改成這個路徑，報告從 `checkpoints/chores/keep-english/` 搬過去，`due` 仍是 not due。

## 3. 要做的

### 已決定（2026-10-30）

- 定位用 agency，不用 skill group：各 agency 的 `config.yaml` 加 `agencies`，和 `skillGroups` 並列，例如：

  ```yaml
  agencies:
    SkillsGestalt: ~/Library/CloudStorage/Dropbox/2-Areas-I/SkillsGestalt
  ```

  別的 agency 的 chore 在 `{agencies.<agency>}/chores/Chore N.md`，文字寫 `Chore N @ <agency>`，和現行規則的寫法一樣。
- 分開兩件事，和 skill 一樣：
  - **定義**：目的、何時做、指令與做法，只有一份，在擁有它的 agency 的 chore 檔。
  - **執行狀態**：上次執行、報告、執行紀錄、要改的記在哪個 task，留在執行的 agency。
- 共用的 chore 的定義不綁定 agency：路徑寫 `{skillGroups.common}`，報告目錄用中性的名稱（例如 `checkpoints/chores/keep-english/`），不寫本 agency 的 task。

### 開始做時決定的（2026-10-30）

- 執行的 agency 用自己的 chore 檔當使用檔，不在摘要表寫 `Chore 2 @ SkillsGestalt` 的列：摘要表、`check_chores.py`、`keepEnglishChore: Chore N` 與 `gen_claude_md.py` 都不必改，原本步驟 2、3 取消。
- 使用檔 1 到 4 章每章一行，指向那個 chore 的同一章，第 1 章另寫 `{agencies.<agency>}/chores/Chore N.md`。
- 本 agency 自己執行 [[keep-english]] 的紀錄照舊寫在 Chore 2 的「6. 執行紀錄」。
- 設 `agencies`，路徑和 skill 一樣由 `config.yaml` 決定；本 agency 的 `config.example.yaml` 不加範例，範例寫在 chore-rules.md。
- 報告目錄改成 `checkpoints/chores/keep-english/`，舊報告搬過去，`due` 才是 not due。
- 提交時，執行的 agency 提交自己的 chore 檔與摘要表，前綴用自己的編號。

### 步驟

1. [chore-rules.md](../.github/common/rules/chore-rules.md) 與中文版：加上使用別的 agency 的 chore 的規則、`agencies` 設定、定義與執行狀態各放哪裡、摘要表那一列的寫法。
2. `check_chores.py`：接受 `Chore N @ <agency>` 的列，以 `agencies` 找到那個檔。
3. `gen_claude_md.py`：支援 `{agencies.X}`，並把 `keepEnglishChore: Chore N @ <agency>` 換成連到 `{agencies.<agency>}/chores/Chore%20N.md` 的相對連結；沒有 `@` 時照舊連到本 agency。
4. [[keep-english]]：路徑改寫 `{skillGroups.common}`，報告目錄改成中性的名稱，「3. 怎麼做」的提交步驟改成不帶本 agency 的編號與 task；舊的報告搬到新的目錄或在執行紀錄註明。
5. 重新產生本 agency 的 CLAUDE.md，跑 `--check`。

## 4. 驗證

- 本 agency：`check_chores.py` 與 `gen_claude_md.py --check` 都是 PASS；[[keep-english]] 照新的步驟跑 `due` 得到 not due。
- 暫用副本模擬一個 Forge：`config.yaml` 設 `agencies.SkillsGestalt` 與 `keepEnglishChore: Chore 2 @ SkillsGestalt`，摘要表有一列 `Chore 2 @ SkillsGestalt`。
  - 產生的 CLAUDE.md 連到 `../SkillsGestalt/chores/Chore%202.md`，連得到。
  - `check_chores.py` 是 PASS；把 `agencies` 拿掉，它報錯。
  - 照 Chore 2 的步驟，從副本的根目錄跑 `audit_keep_english.py`，只稽核副本的中英對照，報告寫在副本裡。
- Chore 2 的定義裡沒有寫死的 `.github/common`，也沒有本 agency 的 task。

2026-10-30 的結果：

- 本 agency：`check_chores.py` 是 PASS；[[keep-english]] 照新的指令跑 `due`，得到 not due。
- 暫用副本模擬一個 Forge：`config.yaml` 設 `agencies.SkillsGestalt` 與 `keepEnglishChore: Chore 1`，`chores/Chore 1.md` 是使用檔，摘要表照舊是 `[[rerecord-ste-custom]]`。
  - `check_chores.py` 是 PASS；第一次的 FAIL 只是副本裡沒有那個 chore 檔連到的 task，補上之後就 PASS。
  - 從副本的根目錄跑 Chore 2 的 `audit` 指令：只稽核副本的中英對照，報告寫在副本的 `checkpoints/chores/keep-english/`，本 agency 的報告目錄沒有變。
- chore-rules.md `check_ste.py` 是 PASS，與中文版 `check_parity.py` 是 0 failure，`diff_md.py --verify` 確認中文版只改了新的一節與 technical words；`reformat_md.py --mode clean` 不改動。
- [[keep-english]] 的第 1 到 4 章，指令裡沒有寫死的 `.github/common`；剩下的兩個 Markdown 連結是從 Chore 2 檔起算的相對路徑，指向本 agency 裡的檔，在哪裡讀都對。

## 5. 與其他 task 的關係

- [[Task 62.5]]：2026-10-19 把 [[keep-english]] 的範圍縮回本 agency；本 task 不改這一點，只讓 Forge 能使用同一份定義。
- [[Task 84]]：`gen_claude_md.py` 與 `keepEnglishChore`；本 task 讓它能連到別的 agency 的 chore。
- [[Task 81]]：術語表的 agency；`agencies` 的名稱照它。
- 各 Forge 改用 [[keep-english]]，在它們自己的 tasks 做，不在本 task 改。

## 6. 日誌

### 2026-10-30

- 建立：使用者希望 chore 的用法和 skill 一樣；chore 跟著 agency 走，以 `{agencies.X}` 定位，不用 `{skillGroups.common}`。
- 開始做並完成：改用使用檔，不改 `check_chores.py` 與 `gen_claude_md.py`；chore-rules.md 與中文版加上規則，[[keep-english]] 不再綁定本 agency，報告搬到中性的目錄；以模擬的 Forge 試過。
- 加上 checkpoints 的路徑規則 `checkpoints/chores/<agency>/chore-<N>`，取代中性名稱；[[keep-english]] 的報告搬到 `checkpoints/chores/SkillsGestalt/chore-2`。
- [[Task 86]] 把 chore 改用名稱：本檔的 `[[Chore N]]` 連結改成新名稱。
