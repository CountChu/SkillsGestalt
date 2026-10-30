# Chore Rules

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-18`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-30`  `8cc2e2061175`

> 本檔案以 ASD-STE100 Simplified Technical English（STE）第 9 版寫成。
> 技術用字：blob、cell、chapter、chore、column、command、commit、content、day、directory、document、file、format、hunk、icon、index、legend、line、link、lowercase、paragraph、path、prefix、repository、root、section、sentence、session、shell、skill、stage、status、subject、summary、table、term、text、title、twin、vault、wikilink、word、workspace。

這些規則說明怎麼寫一個 workspace 的 chore、怎麼做 chore，以及怎麼維護它們的摘要表。
chore 是每次它的條件成立就要做的工作。
因此，chore 不會完成，但可以停用。
會完成的工作是 task，[task-rules.md](task-rules.md) 說明怎麼寫它。
建立、修改或停用一個 chore 時，把這件事記成 task。

## Files

- **每個 workspace 把它的 chore 放在根目錄的 `chores/` 目錄，一個 chore 一個檔案。**
  檔名是 `Chore N.md`：`Chore` 這個字、一個空格，以及 chore 的編號。
  在檔案裡寫明何時要做、怎麼做這個 chore。
  也記下每一次做的紀錄。
  這樣，任何 session 都能照著做。
- **摘要表在 workspace 根目錄的 `dashboard/chore-summary.md`，不在 `chores/`。**
  它有開頭說明、表格，以及圖示與欄位的說明。
  先讀這張表，找出該做的 chore。
  再只開那個 chore。
- **workspace 只放它自己的 chore。**
  chore 做的是在它自己 workspace 的檔案上的工作。
  一個 workspace 用了另一個 workspace 的 skill group，就可以提到那個 workspace 的 chore。
  workspace 不提到用了它的 skill group 的那些 workspace 的 chore。
- **每個 chore 檔都用繁體中文寫。**
  [tw-keep-english.md](../references/tw-keep-english.md) 列出的每個 term 都留英文，和 TW twin 一樣。
  chore 檔沒有 TW twin。
  章名與 Status 行的狀態字是中文，`check_chores.py` 照原樣讀它們。

## Links

- **連到 chore 或 task 時用 wikilink，例如 `[[Chore 1]]` 或 `[[Task 52]]`。**
- **連到 repository 裡的程式、skill、規則或文件時用 Markdown 連結。**
  路徑從 chore 檔所在的目錄算起。
  這類檔案常常同名，例如 `SKILL.md` 與 `README.md`，wikilink 會指到錯的檔案。
- **提到別的 workspace 的 chore 時，寫成文字 `Chore N @ <workspace>`，例如 `Chore 2 @ SkillsGestalt`。**
  提到別的 workspace 的 task 時，寫成 `Task N @ <workspace>`。
  不要寫成連結。
  wikilink 只在它的 workspace 的 vault 裡找檔案。
  兩個 repository 不並排時，連到另一個 repository 的 Markdown 連結就會斷。
- **摘要表裡的連結不要寫別名，例如 `[[Chore N|text]]`。**
  表格用 `|` 分欄。

## The Chore File

chore 檔的格式如下：

```
# Chore N - 標題

**Status**：<使用中|暫停|停用>——<一行結論>
**Started**：yyyy-mm-dd，<為什麼建立>
**When**：<何時要做，一行>

## 1. 目的
## 2. 何時要做
## 3. 怎麼做
## 4. 驗證
## 5. 與其他 task、chore 的關係
## 6. 執行紀錄
### yyyy-mm-dd
```

- **六個 `##` 章依序編號 1 到 6，章名就是這些。**
  沒有內容的章，寫 `—`。
  不要拿掉這一章。
- **在 `2. 何時要做` 裡，寫出開始這個 chore 的條件。**
  也寫出怎麼看出條件成立了，例如一個指令的輸出。
- **在 `3. 怎麼做` 裡，寫出要跑的指令與 step，以及結果怎麼 commit。**
- **在 `6. 執行紀錄` 裡，每天寫一個 `### yyyy-mm-dd` section。**
  這個 section 記錄那一天做了什麼、結果，以及 commit。
  新的日期放在前面。
  同一天再做這個 chore，就補在那一天的 section。
  還沒做過的，寫 `—`。
  日期不早於 Started 行的日期。
- **照 [md-style.md](md-style.md) 寫。**

## Numbers

- **chore 有自己的編號，從 1 起。**
  一個 chore 與一個 task 可以有同一個號碼。
- **新 chore 的編號，是這個 workspace 的 chore 用過的最大編號的下一個。**
  這個最大編號可能在摘要表的 `空號：` 那一行。
- **號碼用過就不再用。**
  chore 搬到別的 workspace 之後，這個 workspace 裡沒有檔案用它的編號，這不是錯誤。
  號碼再用一次，以它為前綴的 commit 就會指到兩個 chore。
- **chore 搬到別的 workspace 時，把它的號碼加進 `空號：` 那一行。**
  這一行在摘要表的圖例下面，例如 `空號：3、5。`。
  每個號碼寫一次，號碼之間用 `、` 分開。
  再寫一句說明：這一行的 chore 搬到了別的 workspace，它的號碼不會再有 chore 用。
  每個號碼都有檔案時，不寫這一行。
- **`check_chores.py` 確認從 1 到最大編號的每個號碼，不是有檔案，就是在這一行。**
  有檔案的號碼不在這一行。

## The Summary Table

- **新增 chore 時，在表的最上面加它的一列，因為最新的 chore 排在最前。**
- **欄位是 Chore、Started、Title、何時要做、上次執行與 Status。**
  - 何時要做：照抄 chore 檔的 When 行。
  - 上次執行：chore 檔 `6. 執行紀錄` 裡最新的日期；還沒做過就寫 `—`。
- **每做一次 chore，就同時改它的 `6. 執行紀錄` 與表中的上次執行。**
- **chore 的狀態改變時，改它自己的 Status 行與表中的圖示。**
  狀態圖示是：🔁 使用中、⏸️ 暫停、⏹️ 停用。
  表下方的圖例列出它們。

## Commits

- **chore 每次執行的 commit，主旨以小寫的 `chore N: ` 開頭，後面接摘要。**
  例如 `chore 1: ste-custom.md is recorded again in the 22 STE files`。
- **建立、修改或停用 chore 的 commit 屬於一個 task，主旨以 `task N: ` 開頭。**
- **只 commit 你改的 hunk。**
  別的 session 會同時改同一些檔案。
  commit 之前，先看 `git status` 與 HEAD。
  別的 session 也在改你改過的檔案時，等它 commit。
  或是 stage 一個 blob：HEAD 的那份檔案只加上你的行，用 `git hash-object -w`，再用 `git update-index --cacheinfo`。
- **`dashboard/chore-summary.md` 一律 stage 這樣的 blob。**
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
python {skillGroups.common}/scripts/check_chores.py --summary dashboard/chore-summary.md --chores-dir chores
```

- `{skillGroups.common}` 是這個 workspace 的 skill group `common` 的根目錄。
  workspace 根目錄的 `CLAUDE.md` 寫出代換好這個路徑的指令。
- 這個指令比對摘要表與每個 chore 檔。
  它比對編號、順序、連結、標題、Started 日期與何時要做。
  它也比對上次執行、狀態圖示、執行紀錄與章的編號。
  有不一致時，它以 exit code `1` 結束。
- Windows 預設的編碼印不出中文與圖示時，先設 `PYTHONIOENCODING=utf-8`。
