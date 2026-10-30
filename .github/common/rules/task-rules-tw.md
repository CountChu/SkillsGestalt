# Task Rules

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-18`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-30`  `8cc2e2061175`

> 本檔案以 ASD-STE100 Simplified Technical English（STE）第 9 版寫成。
> 技術用字：blob、chapter、chore、column、command、commit、content、day、directory、document、file、format、heading、hunk、icon、index、legend、line、link、list、lowercase、note、paragraph、path、prefix、repository、root、section、sentence、session、shell、skill、stage、status、subject、summary、table、term、text、title、tree line、twin、vault、wikilink、word、workspace。

這些規則說明怎麼寫一個 workspace 的 task，以及怎麼維護它們的摘要表。
task 是一次 session 結束之後仍要繼續、而且會完成的工作。
每次某個條件成立就要再做一次的工作是 chore，不是 task。
[chore-rules.md](chore-rules.md) 說明怎麼寫 chore。

## Files

- **每個 workspace 把它的 task 放在根目錄的 `tasks/` 目錄，一個 task 一個檔案。**
  檔名是 `Task N.md`：`Task` 這個字、一個空格，以及 task 的編號。
  在檔案裡寫明 task 目前的狀態，以及這個 task 改動的檔案。
  這樣，沒有開始這個 task 的 session 也能接手。
- **摘要表在 workspace 根目錄的 `dashboard/task-summary.md`，不在 `tasks/`。**
  它有開頭說明、表格，以及狀態圖示的圖例。
  先讀這張表。
  再只開你需要的那個 task。
- **workspace 只放它自己的 task。**
  task 記錄的是在它自己 workspace 的檔案上做的工作。
  一個 workspace 用了另一個 workspace 的 skill group，就可以提到那個 workspace 的 task。
  workspace 不提到用了它的 skill group 的那些 workspace 的 task。
- **每個 task 檔都用繁體中文寫。**
  [tw-keep-english.md](../references/tw-keep-english.md) 列出的每個 term 都留英文，和 TW twin 一樣。
  task 檔沒有 TW twin。
  章名與 Status 行的狀態字是中文，`check_tasks.py` 照原樣讀它們。

## Links

- **連到 task 或其他筆記時用 wikilink，例如 `[[Task 2]]`。**
- **連到 repository 裡的程式、skill、規則或文件時用 Markdown 連結。**
  路徑從 task 檔所在的目錄算起。
  這類檔案常常同名，例如 `SKILL.md` 與 `README.md`，wikilink 會指到錯的檔案。
- **提到別的 workspace 的 task 時，寫成文字 `Task N @ <workspace>`，例如 `Task 62 @ SkillsGestalt`。**
  不要寫成連結。
  wikilink 只在它的 workspace 的 vault 裡找檔案。
  兩個 repository 不並排時，連到另一個 repository 的 Markdown 連結就會斷。
- **摘要表裡的連結不要寫別名，例如 `[[Task N|text]]`。**
  表格用 `|` 分欄。

## The Task File

task 檔的格式如下：

```
# Task N - 標題

**Status**：<尚未開始|進行中|完成>——<一行結論>
**Raised**：yyyy-mm-dd，<為什麼提出>
**Depends on**：[[Task M]]、[[Task K]]，沒有就寫 —

## 1. 背景
## 2. 現況
## 3. 要做的
## 4. 驗證
## 5. 與其他 task 的關係
## 6. 日誌
### yyyy-mm-dd
```

- **六個 `##` 章依序編號 1 到 6，章名就是這些。**
  沒有內容的章，寫 `—`。
  不要拿掉這一章。
- **在 `2. 現況` 裡，用 `###` 標題把內容分成小節。**
  Status 行只寫一行簡短的結論。
  其他內容寫在 `2. 現況` 與 `3. 要做的`。
- **在 `6. 日誌` 裡，每天寫一個 `### yyyy-mm-dd` section，記錄那一天的改動。**
  新的日期放在前面。
  同一天再改這個 task，就補在那一天的 section。
  檔案裡最後一個日期 section 一定是 Raised 行的日期。
- **Depends on 行只寫這個 task 之前必須先完成的 task。**
  它們完成之前，這個 task 不能做，或做了之後還得重做。
  只是相關的 task，寫在 `5. 與其他 task 的關係`。
  Depends on 行只寫同一個 workspace 的 task。
  別的 workspace 裡必須先完成的 task，寫在 `5. 與其他 task 的關係`。
- **照 [md-style.md](md-style.md) 寫。**

## Numbers

- **新 task 的編號，是這個 workspace 用過的最大編號的下一個。**
  這個最大編號可能在摘要表的 `空號：` 那一行。
- **號碼用過就不再用。**
  task 搬到別的 workspace 之後，這個 workspace 裡沒有檔案用它的編號，這不是錯誤。
  號碼再用一次，以它為前綴的 commit 就會指到兩個 task。
- **task 或 sub task 搬到別的 workspace 時，把它的號碼加進 `空號：` 那一行。**
  這一行在摘要表的圖例下面，例如 `空號：18.1、18.3、28。`。
  每個號碼寫一次，號碼之間用 `、` 分開。
  再寫一句說明：這一行的 task 搬到了別的 workspace，它的號碼不會再有 task 用。
  每個號碼都有檔案時，不寫這一行。
- **`check_tasks.py` 確認從 1 到最大編號的每個號碼，不是有檔案，就是在這一行。**
  有檔案的號碼不在這一行。

## Sub Tasks

- **一個 task 可以有 sub task，每個 sub task 一個 `Task N.M.md` 檔。**
  sub task 的標題是 `# Task N.M - 標題`，wikilink 是 `[[Task N.M]]`。
  M 在每個 task 裡從 1 起，編號的規則也適用於它。
- **只靠編號表示 sub task 屬於哪個 task。**
  不要為此另加一行。
  task 的 Depends on 行不列它的 sub task。
- **sub task 的格式和 task 一樣**：Status、Raised、Depends on 三行，以及六章。
- **sub task 的內容只寫在那個 sub task。**
  之後的紀錄也只寫在那裡。
  task 本身只留 sub task 清單，以及所有 sub task 共用的規則與決定。
  清單每項一行：連結、狀態圖示與標題，例如 `- [[Task 32.1]] ✅ DFD`。
- **sub task 的狀態改變時，改它自己的 Status 行與摘要表中的圖示。**
  也改它在 task 的 sub task 清單中的圖示。

## The Summary Table

- **新增 task 時，在表的最上面加它的一列，因為最新的 task 排在最前。**
- **sub task 的列放在它的 task 那一列的正下方，依編號由小到大。**
  在 sub task 的連結前加上線條。
  最後一個 sub task 寫 `└─ [[Task N.M]]`。
  其餘的 sub task 寫 `├─ [[Task N.M]]`。
  新增 sub task 時，把原本最後一列的 `└─` 改成 `├─`。
  Depends on 欄裡的連結前不加線條。
- **Depends on 欄重複 Depends on 行的連結，每個連結後面接那個 task 現在的圖示**，例如 `[[Task 1]] ✅`。
- **task 的狀態改變時，改它自己的 Status 行與表中的圖示。**
  每個連到它的列，Depends on 欄中它的圖示也要改。
- **狀態圖示是：⬜ 尚未開始、🔄 進行中、✅ 完成。**
  表下方的圖例列出它們。

## Commits

- **task 的工作所做的 commit，主旨以小寫的 `task N: ` 開頭，後面接摘要。**
  sub task 用 `task N.M: ` 開頭。
  一個 commit 碰到幾個 task 時，寫主要的那個。
- **只 commit 你改的 hunk。**
  別的 session 會同時改同一些檔案。
  commit 之前，先看 `git status` 與 HEAD。
  別的 session 也在改你改過的檔案時，等它 commit。
  或是 stage 一個 blob：HEAD 的那份檔案只加上你的行，用 `git hash-object -w`，再用 `git update-index --cacheinfo`。
- **`dashboard/task-summary.md` 與有 sub task 的 task 的檔案，一律 stage 這樣的 blob。**
  不要 `git add` 整個檔案。
  別的 session 可能在你檢查之後、`git add` 之前，在檔案裡加了一列。
  這樣，你的 commit 就會帶進別的 session 加的那一列。
- **檢查 HEAD 與它後面的每個 step 放在同一個 shell 指令裡，step 之間用 `&&` 串起來。**
  這些 step 是 stage blob 的指令、`git add` 與 `git commit`。
  檢查單獨放在一行時，擋不住後面幾行的指令。
- **`git commit` 之前，確認 index 裡只有你的路徑。**
  別的 session 可能 stage 了它的檔案，你的 commit 就會帶進它們。

## Check

每次改完，都從 workspace 的根目錄執行這個指令：

```bash
python {skillGroups.common}/scripts/check_tasks.py --summary dashboard/task-summary.md --tasks-dir tasks
```

- `{skillGroups.common}` 是這個 workspace 的 skill group `common` 的根目錄。
  workspace 根目錄的 `CLAUDE.md` 寫出代換好這個路徑的指令。
- 這個指令比對摘要表與每個 task 檔。
  它比對編號、順序、連結、標題與 Raised 日期。
  它也比對狀態圖示、Depends on 行、日期 section 與章的編號。
  有不一致時，它以 exit code `1` 結束。
- Windows 預設的編碼印不出中文與圖示時，先設 `PYTHONIOENCODING=utf-8`。
