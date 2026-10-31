# Chore Rules

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-18`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-30`  `8cc2e2061175`

> 本檔案以 ASD-STE100 Simplified Technical English（STE）第 9 版寫成。
> 技術用字：agency、blob、cell、chapter、chore、column、command、commit、content、day、digit、directory、document、file、format、hunk、hyphen、icon、index、legend、letter、line、link、lowercase、paragraph、path、prefix、private、repository、root、section、session、shell、skill、stage、status、subject、summary、table、term、text、title、twin、vault、wikilink、word、workspace。

這些規則說明怎麼寫一個 workspace 的 chore、怎麼做 chore，以及怎麼維護它們的摘要表。
chore 是每次它的條件成立就要做的工作。
因此，chore 不會完成，但可以停用。
會完成的工作是 task，[task-rules.md](task-rules.md) 說明怎麼寫它。
建立、修改或停用一個 chore 時，把這件事記成 task。

## Files

- **每個 workspace 把它的 chore 放在根目錄的 `chores/` 目錄，一個 chore 一個檔案。**
  檔名是 chore 的名稱加上 `.md`，例如 `keep-english.md`。
  在檔案裡寫明何時要做、怎麼做這個 chore。
  這樣，任何 session 都能照著做。
  只做別的 agency 的 chore 的 workspace，可以沒有 `chores/`。
  `chores/` 裡不放程式或目錄，因為 chore 沒有自己的程式。
- **摘要表在 workspace 根目錄的 `dashboard/chore-summary.md`，不在 `chores/`。**
  它有開頭說明、表格、圖示的說明，以及執行紀錄。
  先讀這張表，找出該做的 chore。
  再只開那個 chore。
- **chore 做的是在做它的那個 workspace 的檔案上的工作。**
  一個 workspace 用了某個 agency 的 skill group，就可以做那個 agency 的 chore。
  workspace 不做用了它的 skill group 的那些 workspace 的 chore。
- **每個 chore 檔都用繁體中文寫。**
  [tw-keep-english.md](../references/tw-keep-english.md) 列出的每個 term 都留英文，和 TW twin 一樣。
  chore 檔沒有 TW twin。
  章名與 Status 行的狀態字是中文，`check_chores.py` 照原樣讀它們。

## Names

- **chore 的名稱由小寫字母、數字與連字號組成，以字母開頭。**
  例如 `keep-english`。
- **所有 agency 裡沒有兩個 chore 同名，和 skill 一樣。**
  所以一個名稱只指一個 chore，在別的 agency 也一樣。
- **chore 可以改名。**
  做這件事的 task 同時改每個連到這個 chore 的連結與它的執行紀錄。
- **停用的 chore，檔案留在 `chores/`，它的名稱不再用。**
  名稱再用一次，以它為前綴的 commit 就會指到兩個 chore。

## Links

- **連到本 workspace 的 chore 或 task 時用 wikilink，例如 `[[keep-english]]` 或 `[[Task 52]]`。**
- **連到 repository 裡的程式、skill、規則或文件時用 Markdown 連結。**
  路徑從 chore 檔所在的目錄算起。
  這類檔案常常同名，例如 `SKILL.md` 與 `README.md`，wikilink 會指到錯的檔案。
- **提到別的 agency 的 chore 時，寫成文字的名稱，例如 `keep-english`。**
  提到別的 workspace 的 task 時，寫成文字 `Task N @ <workspace>`。
  不要寫成連結。
  wikilink 只在它的 workspace 的 vault 裡找檔案。
  兩個 repository 不並排時，連到另一個 repository 的 Markdown 連結就會斷。
- **摘要表裡的連結不要寫別名，例如 `[[name|text]]`。**
  表格用 `|` 分欄。

## A Chore of a Different Agency

- **要做別的 agency 的 chore，就在本 workspace 的摘要表加它的一列。**
  Chore 欄寫成文字的名稱，不寫成連結。
  Title 與何時要做和那個 agency 的 chore 檔一樣。
  Started 是本 workspace 開始做這個 chore 的日期。
  Status 是這個 chore 在本 workspace 的狀態。
- **`config.yaml` 的 `agencies` 給出每個 agency 的根目錄，只要本 workspace 做那個 agency 的 chore。**
  例如 `agencies:` 裡的一行 `SkillsGestalt: ~/Library/CloudStorage/Dropbox/2-Areas-I/SkillsGestalt`。
  `check_chores.py` 在 `{agencies.<agency>}/chores/<name>.md` 找到那個 chore 檔。
- **不做別的 agency 的 private chore。**
  它的檔案有一行 `**Private**`，見 The Chore File 一節。
- **一個 chore 若有不只一個 workspace 在做，它的檔案不寫任何一個 workspace 自己的值。**
  skill group 裡的路徑寫成 `{skillGroups.common}`。
  每個 workspace 在自己的根目錄、對自己的檔做這個 chore，報告、執行紀錄與 commit 都留在自己那裡。

## The Chore File

chore 檔的格式如下：

```
# <name> - 標題

**Status**：<使用中|暫停|停用>——<一行結論>
**Started**：yyyy-mm-dd，<為什麼建立>
**When**：<何時要做，一行>
**Private**：<只有哪個 agency 做，為什麼；不是 private 就不寫這一行>

## 1. 目的
## 2. 何時要做
## 3. 怎麼做
## 4. 驗證
## 5. 與其他 task、chore 的關係
```

- **五個 `##` 章依序編號 1 到 5，章名就是這些。**
  沒有內容的章，寫 `—`。
  不要拿掉這一章。
- **在 `2. 何時要做` 裡，寫出開始這個 chore 的條件。**
  也寫出怎麼看出條件成立了，例如一個指令的輸出。
- **在 `3. 怎麼做` 裡，寫出要跑的指令與 step，以及結果怎麼 commit。**
- **chore 沒有自己的程式。**
  它的 step 使用 skill，或 skill group 裡的程式。
  程式的路徑用 `{skillGroups.X}` 寫，例如 `{skillGroups.common}/scripts/audit_keep_english.py`。
  skill 說明怎麼做這件工作，chore 說明什麼時候做，並記下每一次的執行。
  所以每個程式只在一個地方，每個 agency 都找得到。
- **private chore 在 When 行後面有一行 `**Private**`。**
  只有擁有這個 chore 的 agency 做它。
  它的程式可以寫那個 agency 的值，但和所有程式一樣放在 skill group 裡。
- **chore 若要在 `checkpoints/` 放檔，放在 `checkpoints/chores/<name>`。**
  `<name>` 是 chore 的名稱。
  所以每個做這個 chore 的 workspace 都用同一個路徑。
- **chore 檔不放執行紀錄。**
  每個 workspace 把這個 chore 的執行記在自己的摘要表，見 The Summary Table 一節。
- **照 [md-style.md](md-style.md) 寫。**

## The Summary Table

- **各列照 Started 日期排，新的在前。**
  兩列的日期相同時，照名稱排。
- **欄位是 Chore、Started、Title、何時要做、上次執行與 Status。**
  - 何時要做：照抄 chore 檔的 When 行。
  - 上次執行：這個 chore 的執行紀錄裡最新的日期；還沒做過就寫 `—`。
- **圖例下面的 `## 執行紀錄` 一節放執行紀錄。**
  做過的每個 chore 有一個 `### <name>` section，順序和表格一樣。
  裡面每做過一天，就寫一個 `#### yyyy-mm-dd` section。
  這個 section 記錄那一天做了什麼、結果，以及 commit。
  新的日期放在前面，日期不早於那一列的 Started。
  同一天再做這個 chore，就補在那一天的 section。
- **每做一次 chore，就同時改它的執行紀錄與上次執行。**
- **chore 的狀態改變時，改它自己的 Status 行與表中的圖示。**
  狀態圖示是：🔁 使用中、⏸️ 暫停、⏹️ 停用。
  表下方的圖例列出它們。

## Commits

- **chore 每次執行的 commit，主旨以 `chore <name>: ` 開頭，後面接摘要。**
  例如 `chore rerecord-ste-custom: ste-custom.md is recorded again in the 22 STE files`。
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
  它比對名稱、順序、連結、標題、Started 日期與何時要做。
  它也比對上次執行、狀態圖示、執行紀錄與章的編號。
  有不一致時，它以 exit code `1` 結束。
- Windows 預設的編碼印不出中文與圖示時，先設 `PYTHONIOENCODING=utf-8`。
