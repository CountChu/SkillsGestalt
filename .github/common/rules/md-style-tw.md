# Markdown style

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-18`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-30`  `8cc2e2061175`

> 本檔案以 ASD-STE100 Simplified Technical English（STE）第 9 版寫成。
> 技術用字：abbreviation、app、backslash、block、block quote、body、bold、bracket、bullet、cell、character、chat export、citation、clause、closing bracket、colon、column、command、comma、configuration、context、decode、definition、delimiter、description、design document、diagram、digit、directory、directory tree、document、dollar sign、dynamic token、ellipsis、escape、export、extractor、fence、fenced block、fenced code block、field、file、formula、frontmatter、git、guard、handler、hard break、heading、history、idempotent-only mode、identifier、indent、inline code、inline math、key、LaTeX、line、list、marker、math、module、no-op、non-breaking space、note、page、paragraph、paste、path、pattern、prefix、preformatted block、proper name、prose、punctuation、quotation、quote、raw mode、raw paste、reformat、renderer、repository、script、section、semicolon、sentence、skill、span、spelling、string、style、subscript、table、text、thousands separator、title、token、transform、twin、unescape、unordered list、version、whitespace、word、word character、writer、year。

在這個 repository 中建立或改動 Markdown 檔案時，遵守這些規則：

- 無序清單的項目用 `-`，不用 `*`。
- 不要用 `**` 包住標題的文字。
  標題的 `#` 層級決定它的樣式。
- 在標題中，把編號前綴寫成 `1. name`。
  不要像 `1\. name` 那樣跳脫 `.`。
- 把目錄樹、ASCII 圖或其他預先排版的區塊放進 fenced code block。
  這樣，`#` 與 `_` 這類字元會照原樣顯示，也不需要用反斜線跳脫它們。
- 在渲染器可能把單獨的 `#` 讀成別的東西的地方，讓 `\#` 保持跳脫。
  渲染器可能把它讀成標籤（`#1`、`#tag`），或在行首時讀成標題。
- 刪除 NotebookLM/Gemini 匯出檔留在文字中的引用標記。
  這些標記是子句結尾的單獨 `1`、`1, 2` 或 `2-4`。
  它們指向筆記現在已不包含的來源文件，因此什麼文件也指不到。
- 數學式寫成 Obsidian 的數學式：行內數學式用 `$...$`，獨立成行的數學式用 `$$...$$`。
  把獨立成行的數學式放在只有那段數學式的一行。
  沒有任何渲染器會把聊天匯出檔中跳脫過的 LaTeX 讀成數學式（`\\\\(x\\\\)`、`\\\\ ... \\\\`，以及像 `\\text` 那樣帶兩個反斜線的指令）。
  把它改成 Obsidian 的數學式。
- 在 repository 的所有 Markdown 檔案中，正文都寫成一句一行。
  這條規則不適用於 `.github/external/` 中的檔案。
  - 句子結束於 `。`、`？` 或 `！`。
    `.`、`?` 或 `!` 後面接著一個空格與下一句的開頭時，也可以是句子的結尾。
    冒號或分號不結束句子。
  - 在括號內、引號內、inline code 內或數學式內，句末標點不結束句子。
    在縮寫（`e.g.`、`vs.`）或刪節號中，它也不結束句子。
    後面沒有空格時，在數字（`2.1`）、檔名或 URL 中，句末標點也不結束句子。
  - 一個句子跨越多行時，把它接成一行。
  - 標題、表格列、fenced block、引用區塊、HTML、獨立成行的數學式與 frontmatter，都維持原樣。
  - 在清單項目中，第一句之後的每一句都從新的一行開始。
    讓這些行的縮排與該項目的文字相同。
  - 繁體中文 twin 與它的英文檔逐句一一對應。
    因此，兩份檔案保持逐行對齊。

## Transforms applied by reformat_md.py

`reformat-md` skill 的 script（[reformat_md.py](.github/common/skills/reformat-md/scripts/reformat_md.py)）依下列順序，以這些轉換套用本節之前的規則：

1. 從每一行的行尾刪除由兩個空格構成的 Markdown hard break。
2. 判斷輸入是否為從 Word/Docs 直接貼上的原始內容。
   為了找出直接貼上的原始內容，它尋找以 `**` 包住的標題、`\.` 跳脫、標題中的 `\-` 跳脫，或 `*` 項目符號。
   如果一個都找不到，這個檔案就是乾淨的，script 會進入 idempotent-only mode。
   在這個模式下，它不執行轉換 3–6、8 與 9。
   但它會執行改動數學式的轉換 7，以及把每一句各放在一行的轉換 10。
   這讓乾淨檔案上的第二次執行成為 no-op。

   有 `--mode raw` 或 `--mode clean` 時，script 採用該模式，而不從輸入判斷模式。
   `--twin` 以檔案所採用的模式，重新排版該檔案的 twin。
   因此，script 一律對一對檔案的兩份套用相同的模式。
   在這個 repository 中寫成、而不是從匯出檔貼上的檔案，用 `--mode clean`。
   只要一個 `*` 項目符號，就可能讓 script 把它當成貼上的內容，而 raw mode 會把每個標題都降一級。
3. **標題**：去掉標題周圍的 `**…**`，並取消標題文字中 `\.` 與 `\-` 的跳脫。
   然後它把每個標題都降一級（來源中的 `# 1. Requirements` 變成 `## 1. Requirements`），但第一個 `#` 行維持為文件的標題。
4. **項目符號**：把每個位於行首的 `*` 改成 `-`。
   它保留 `**bold**`，以及 YAML 字串中的 `*`。
5. **去除內文的跳脫**：`\-` → `-`、`\_` → `_`、`\[` → `[`、`\]` → `]`、`\>` → `>`、`\*` → `*`、`\=` → `=`、`\+` → `+`、`\~` → `~`、`\\n` → `\n`、`\\$` → `\$`。
   只是一個字元的錢字號維持跳脫，因此 Obsidian 不會開始一段數學式區段。
    - **`\#` 只在某些條件下才會改變。**
      只有在單獨的 `#` 不起作用的地方，它才變成 `#`。
      也就是說，那個 `#` 不在行首，後面也不接 word character、`-` 或 `/`。
      其他情況下，它照上面的規則保留反斜線。
      例如 `機會 \#1`、`\#tag` 與行首的 `\#`。
      不論有沒有反斜線，渲染器都只顯示 `#`，因此這個跳脫不會造成問題。
6. **把預先排版的區塊包進 fenced code block**：
    - `**Syntax**` 的內容 → ` ``` ` fence。
    - `**Example**` 的內容 → ` ```json ` fence。
    - `#### Config - <name>.yaml` 下方的 YAML 設定區塊（說明段落之後相鄰的 `key: value` 行） → ` ```yaml ` fence。
    - 以一行 `data/` 開頭、後面接著 `├──`/`└──` 行的目錄樹 → ` ``` ` fence。
    - 區塊已經在 fence 中時（下一個非空白行是 ` ``` `），每個 handler 都不會再把它放進 fence。
      因此，沒有完全清理乾淨的輸入，不會得到兩層 fence。
7. **把聊天匯出檔的 LaTeX 改成 Obsidian 的數學式。**
   Gemini/NotebookLM 貼上的內容，每一個 LaTeX 反斜線都有兩個反斜線（`\text` 以 `\\text` 出現，`\%` 以 `\\%` 出現），並以一個反斜線跳脫 Markdown 標點（`\=`、`\+`、`\-`、`\)`、`\_`、`\~`）。
   Delimiter 以四個連續反斜線的形式出現：行內數學式用 `\\\\(`…`\\\\)`，獨立成行的數學式則在兩側各用一個單獨的 `\\\\`。
   因此，一串連續的反斜線這樣解讀：4 個 = 一個 delimiter，2 個 = 一個 LaTeX 指令，更長的一串 = 兩者的和（6 = 4+2、8 = 4+4、10 = 4+4+2）。

   行內數學式變成 `$…$`，獨立成行的數學式則變成獨佔一行的 `$$…$$`。
   這個轉換把獨立成行的數學式前後的正文，放在不含那段數學式的行。
   這些決定很重要：
    - 在數學式中，`\~` 變成 `-`。
      來源用 `~` 表示數值的範圍（`10~12%`），但 LaTeX 把 `~` 讀成 non-breaking space。
      因此，`\text{10~12\%}` 會顯示成「10 12%」，而且沒有任何訊息告訴你。
    - `\%`、`\$` 與 `\_` 保留它們的反斜線。
      LaTeX 必須跳脫 `\%` 與 `\$`，而 `PV\_1` 是 LaTeX 的下標。
    - 這個轉換在**每一種**模式下都執行：raw mode 與 clean mode。
      它不改動沒有四個連續反斜線的行。
      因此，第二次執行不會造成任何改動，而這個轉換也能修復版本在 `#v1` 之後的檔案。
    - 這個轉換不改動含有 inline code 的行，因為 inline code 照原樣顯示它的文字。
      檔案當作範例顯示的跳脫 LaTeX，例如 md-style.md 中的那些，不是數學式，這個轉換也不改動它。
8. **把 identifier 放進 inline code**，只在 raw mode 下，也只在內文中。
   它不在 fence 中、標題行中，或含有 inline code 的行上這樣做。
   script 中有一份 identifier 清單：模組（`parser.py`、`topic_mgr.py`、`render_md.py`、`exporter.py`）、設定檔（`sync_config.yaml`、`export_template.yaml`）、工具（`pathlib`、`jinja2`、`child_process.spawn`）與路徑（`data/0-raw/`、`data/1-sessions/`、`data/2-turns_md/`、`data/3-topics/`、`data/4-exports/`、`0-raw/`）。
   這個轉換也把文件在 `{a, b, …}` 集合中列出的每一個 identifier 放進 inline code。
   例如一個資料結構的欄位名稱（`visibilityFlag`、`timestamp`、`timestampUtc`、`sessionId`、`topicId`、`turnId`、`beginTime`、`endTime`、`sessionIds`）與設定鍵（`rawDir`、`sessionsDir`、`turnsMdDir`、`topicsDir`、`exportsDir`、`sessionGapSeconds`）。

   在這個 repository 中寫成的檔案，可能在集合中列出一個名稱，例如 `step_{N}` 的 `N`。
   如果這個轉換在 clean mode 下也執行，它會在那個名稱作為一個詞出現的每一處，把它放進 inline code。
   因此，這個轉換只在 raw mode 下執行。
   它不改動帶有 `$`/`$$` 數學式區段的行。
   `\text{ROIC}` 會把 `ROIC` 交給 dynamic token 的擷取器。
   沒有這條規則，這個轉換可能在之後的某一次執行中，把公式改成 `$$\text{`ROIC`}$$`。
9. **刪除 NotebookLM/Gemini 的引用標記。**
   匯出檔以單獨的 `1`、清單 `1, 2` / `3, 4`，或範圍 `2-4`，標出文字每一部分的來源文件。
   標記出現在四種位置，而 pattern 的順序很重要。
   script 必須先找出只有一個標記的行，再使用空白的 pattern。
   否則，空白的 pattern 只會刪掉 `1, 2` 中的 ` 2`，而 `1,` 會留在文字中：
    - 只有一個標記的一行。
      轉換 7 可能產生這種行：它拆開 `…\\\\ 6` 時，會得到獨立成行的數學式區塊，以及只有那個 `6` 的一行。
      這個轉換刪掉這一行，而不是把它變成空行。
    - `效果）1。`、`機會成本」1。`：直接緊接在右括號（`）」』】》〉`）之後。
    - ` 1。`、` 3, 4。`、`\$60 2,\$60`：標記前面是空白，後面是子句的結尾。
    - `**：2 這樣…`、`（EBIT / EV）3 更高的…`：標記位於子句的開頭，而不是結尾。

    不是標記的數字維持安全，因為每一個 pattern 都必須有子句結尾的 context（`。，、：；！？`、`**`、表格儲存格的 `|`、ASCII 的 `,`，或行尾）。
    `40%`、`\$5`、`第 141 頁` 與 `1.` 清單標記不會出現在那種 context 中。
    另外還有兩道防護。
    標記最多**兩位數**。
    因此，script 把單獨的 `2024。` 或 `141。` 讀成年份或頁碼，而不是引用標記。
    而且，ASCII 逗號的 context 不接受千分位分隔符號（`,(?!\d{3}(?!\d))`），因此 `1,000` 保留它的 `1`。

    這個轉換只在 raw mode 下執行，而且不在 inline code 或表格列中執行。
    在這個 repository 中寫成的檔案裡，step 編號或列號就位在引用標記會出現的位置（`Step 3。`、`| 1 |`）。
    它只刪除文字，因此第二次執行是 no-op。

    這個轉換有三個已知的限制：
    - 句尾的一位或兩位數（`本益比是 15。`）看起來和引用標記一樣。
      因此，這個轉換會刪掉它，雖然它不是標記。
    - 這個轉換不改動後面接著 `（` 的標記（`**已動用有形資本**, 2（…`）。
      如果它刪掉這個標記，標記前面的逗號會留在文字中。
    - 遇到 `）N 中文` 這種形狀時，這個轉換分不出引用標記，和屬於文字一部分的數字（`（含）3 個月`）。

10. **把正文的每一句各放在一行**，在 raw mode 與 clean mode 下都執行。
    它採用本節之前那條規則所給的句子定義。
    有些行寬度達 60 欄以上（一個 CJK 字元算兩欄），而它們的結尾不是句子的結尾。
    在這些行中，句子延續到下一行，這個轉換就把兩行接在一起。
    較短的行，例如 `**Raised**: 2026-10-11`，是作者有意的換行，它維持不動。

    接著，它在每一個於該行中結束的句子之後斷行。
    在清單項目中，它讓後面的每一句與該項目的文字有相同的縮排。
    緊接在句末標點之後的 `**`，只有在它關閉一段尚未關閉的粗體時，才歸給前一句。
    開啟粗體的 `**`，例如 `…x。**Name**` 中的那一個，會放在下一行的開頭，因為在行尾它無法開啟粗體。

    它只改動換行，以及換行周圍的空格。
    它把兩行接在一起時，不在兩個 CJK 字元之間放空格。
    因此，第二次執行是 no-op。

## Rules checked elsewhere

這些規則也適用於 repository 中的所有 Markdown 檔。
但 `reformat_md.py` 不套用它們，因為每一條都會改動文字。
`check_reformat.py` 只讓重新排版改動換行，以及換行周圍的空格。
每一條規則都說明由哪一個工具檢查它。

- 英文要用美式拼法："color"、"behavior"、"catalog" 與 "judgment"，而不是 "colour"、"behaviour"、"catalogue" 與 "judgement"。
  [us-spelling.json](.github/common/references/us-spelling.json) 列出每一個英式拼法與它的美式拼法。
  `asd-ste` skill 的 `check_ste.py` script 用這份清單檢查 STE file。
  不要改動引文或專有名詞的拼法。
  其他文件或程式碼也用的名稱，同樣保留它的拼法，例如元件、檔案或 identifier 的名稱。
  在 STE file 中，把這樣的名稱放進 `Technical words:` 清單，檢查就會接受它。
- 不要在一段文字裡寫這段文字自己的來歷。
  這段來歷包括這段文字先前的版本、它所取代的方法，以及在它之前的做法。
  git 與 `tasks/` 中的檔案保存這段來歷。
  app 所取代的做法不是它的設計文件的來歷，那份文件可以寫它。
  沒有工具檢查這條規則：由審閱這個檔案的人檢查它。
  - 這條規則不適用於記錄工作或變更的文字。
    這些文字是 `tasks/`、`chores/` 與 `dashboard/` 中的檔案、RSDC 文件的 `Changes in This Version` 一節，以及 `ste-custom.md` 的 `Why` 欄。
    此外，這條規則也不適用於 `.github/external/` 中的檔案。
