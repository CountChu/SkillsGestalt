# Terms Kept in English in 繁體中文 Twins

> Version: 261030
> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-18`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-30`  `8cc2e2061175`

> 本檔案以 ASD-STE100 Simplified Technical English（STE）第 9 版寫成。
> 技術用字：agency、agent、alias、app、argument、automated、baseline、caller、canonical skill invocation、cell、character、checkpoint、class、clean mode、clock、cognitive、column、command、command line、commit、context、contract、data structure、delimiter、design document、diff、docstring、document、epoch、event、exit status、external input、fence、fenced block、file、fingerprint、flag、folded block scalar、Forge、frontmatter、Gestalt、glossary、handler、handoff、hard break、hash、heading、here-string、hexagon、hook、hunk、idempotent-only mode、identifier、import、inline code、inline-code span、interactive、interpolation、introspection、line、line break、link、link target、list、match、math、MD report、metadata、no-op、non-breaking space、null、one-run data、operating system、pairing line、parse、path、pattern、pipe、placeholder、plain scalar、process、prose、raw mode、record、regular expression、rendering、repository、request、route、scalar、schema、script、second、section、section partial、sentence、separator、session、shell、skill、span、spelling、stage、stale、statement、step、string、string literal、style、table、template、term、text、token、traceback、twin、variable、verdict、version、wiki、wireframe、word、word character、workflow、workspace。

每一份 `-tw` twin，都在它的正文中把下列清單的 term 保留為英文。
twin 的例子有 skill 的 `SKILL-tw.md`、設計文件的 `-RSDC-tw.md`，以及 wireframe 的 `-tw.md`。
每個 term 在 twin 中的拼法，都和英文檔相同。
這份清單把每個決定只記錄一次。
因此，同一個 term 不會在兩份 twin 中有兩種不同的譯法。

tw-keep-english.md 的檔名不含日期。
只有改動規則或清單，才會產生新版本，Version 行顯示新的版本。
因此，引用 tw-keep-english.md 的文件都不必跟著改。
改動的不是規則也不是清單時，版本維持不變。

## The rule

term 是一個詞或片語，在一份文件中一律指同一類項目。
例子有 *checkpoint*、*commit*、*placeholder* 與 *verdict*。
一個詞不是一律指同一類項目時，就是一般的詞，不是 term。
term 符合這三個條件中的**一個**，或符合不只一個時，保留英文：

- **twin 為它用了不只一種中文譯法。**
  譯者可以選其中一種譯法，下一份 twin 的譯者則可以選另一種。
  這時讀者就無法知道，這兩個詞是同一樣東西的名稱。
- **它是 system 中一種類型、狀態、outcome 或 role 的名稱。**
  替它取的中文詞，會對不上程式碼、schema 或英文文件所用的 identifier。
  這時讀者必須把這個詞再譯回英文，才找得到它所指的東西。
- **它是一個指令的名稱。**
  替它取的中文詞，會對不上你執行這個指令時打的名稱。
  這時讀者必須把這個詞再譯回英文，才找得到這個指令。

其餘的詞一律翻譯。
這適用於一般的詞，以及只有一種固定中文譯法的 term，例如指紋、規格或檢查。
如果某個 term 在一份文件的 glossary 中，該文件的規則讓它保留英文。
不論這個 term 在不在這份清單上，都是如此。

這份清單只適用於正文。
一律原樣照抄標題、inline-code span、fenced block、路徑與連結目標。

## The list

**Replaces** 欄列出譯者可能為這個 term 寫出的每一種譯法。
這一欄是給譯者，以及檢查 twin 的人看的。
這一欄的譯法，沒有一個在 twin 的正文中是正確的。
twin 的正文使用英文的 term。

工具在 twin 的正文中檢查 **Flagged** 欄的每一種譯法，找到時就顯示警告。
這些工具是 `chinese` skill 的 `check_parity.py --keep`，以及 `gen-rsdc-skill` skill 的 `check_rsdc.py`。

有些譯法也是一般用語，或是一般用語的一部分。
例子有自動化裡的自動，以及作為一般詞的互動。
工具在正確的句子中也會找到這些譯法。
讀者收到關於正確文字的警告時，可能會開始忽略所有的警告。
因此，只有 **Replaces** 欄列出這些譯法。
**Flagged** 欄寫「—」時，表示這個 term 沒有任何譯法，能讓工具檢查正文而不誤報。

工具找到的譯法，產生的是 `[WARN]` 行，而不是 `[FAIL]` 行。
平常指這個 term 的譯法，在講另一個項目的句子中，也可能指那個項目。
因此，由人讀過每一則警告，再做決定。

| Term | Replaces | Flagged | Why it stays English |
|---|---|---|---|
| agency | 代理機構, 機構 | 代理機構 | 它是 glossary 裡一種項目的名稱，沒有標準的中文譯法。 |
| agent | 代理人, 代理 | 代理人 | twin 已用了兩種譯法，而且它是一種 role 的名稱。 |
| alias | 別名 | — | 它是 shell 的一個指令的名稱：替它取的中文詞，會對不上 `alias` 這個指令。 |
| app | 應用, 應用程式 | — | 它是 system 中一種類型的名稱，而且 twin 已用了兩種譯法：應用，以及英文的 app。 |
| automated | 自動, 無頭自動 | 無頭自動 | 它是一種 step 類型的名稱。 |
| baseline | 基準, 基線 | 基線 | 它是 diff 所依據的 commit 的名稱，而且 twin 已用了不只一種譯法。基準太常出現，不列入 Flagged。 |
| caller | 呼叫者, 呼叫端, 呼叫方 | 呼叫者, 呼叫端 | 它是在 system 外部啟動 system、並提供其 request 的 role 的名稱，而且 twin 已用了三種譯法。呼叫方太常出現，不列入 Flagged，例如呼叫方式裡就有它。 |
| canonical skill invocation | 標準形式的 skill 呼叫, 標準的 skill 呼叫, 標準化的 skill 叫用方式, 標準化的 skill 呼叫形式, 標準化的 skill 呼叫式, 正規化的 skill 呼叫形式 | 標準形式的 skill 呼叫, 標準的 skill 呼叫, 標準化的 skill 叫用方式, 標準化的 skill 呼叫形式, 標準化的 skill 呼叫式, 正規化的 skill 呼叫形式 | 它是 Step 0 所保存的 `/<skill-name>` 指令及其解析後引數的名稱，而且 twin 已用了六種譯法。 |
| checkpoint | 檢查點 | 檢查點 | 它是一種 record 的名稱。 |
| clean mode | 乾淨模式, 清理模式 | 乾淨模式, 清理模式 | 它是 `reformat-md` 的一種模式的名稱，由 `--mode clean` 選用。 |
| cognitive | 認知型, 認知性 | 認知型, 認知性 | 它是一種 step 類型的名稱，而且 twin 已用了兩種譯法。 |
| commit | 提交, 送交 | 提交 | 它是 `git` 的一種 record 的名稱，而且 twin 已用了不只一種譯法。 |
| context | 上下文, 前後文, 語境, 情境 | — | 它是 pattern 必須在比對處周圍找到的文字的名稱，而且 twin 已用了四種譯法。它們全都太常出現，不列入 Flagged。 |
| delimiter | 定界符, 分隔符號, 分隔符 | 定界符 | 它是開啟或關閉一段內容的符號的名稱，例如一段數學式，而且 twin 已用了不只一種譯法。分隔符太常出現，不列入 Flagged，因為它也是 separator 的名稱。 |
| deterministic | 確定性, 決定性 | 確定性, 決定性 | 它是一種 step 類型的名稱，而且 twin 已用了兩種譯法。 |
| diff | 差異, 比對 | — | 它是 `git` 比較一個檔案的兩個版本時所給的輸出的名稱，而且 twin 已用了不只一種譯法。兩種譯法都太常出現，不列入 Flagged。 |
| docstring | 文件字串, 說明字串 | 文件字串 | 它是程式一部分的名稱，而且沒有固定的中文譯法。 |
| epoch | 紀元, 紀元時間 | 紀元 | 它是時鐘開始計秒的那個時間點的名稱，而且沒有固定的中文譯法。 |
| exit status | 結束狀態, 退出狀態 | 結束狀態 | 它是程式的一種 outcome 的名稱，而且 twin 已用了不只一種譯法。 |
| external input | 外部輸入 | 外部輸入 | 它是 DFD 中一種資料的名稱。 |
| fence | 圍欄, 柵欄 | 圍欄, 柵欄 | 它是開啟或關閉 fenced block 的那一行的名稱，而且沒有固定的中文譯法。 |
| fenced block | 程式碼區塊, 圍欄區塊 | 程式碼區塊, 圍欄區塊 | twin 已用了兩種譯法，而且它是 Markdown 檔案中 twin 原樣照抄的部分的名稱。 |
| folded block scalar | 摺疊區塊純量, 折疊式區塊 | — | 它是 YAML 一種 scalar 寫法的名稱，而且沒有固定的中文譯法。 |
| Forge | 工坊, 鍛造坊 | 工坊, 鍛造坊 | 它是 glossary 裡一種 agency 的名稱，沒有標準的中文譯法。 |
| frontmatter | 前置資料, 頁首資訊, 前言 | 前置資料, 頁首資訊 | twin 已用了兩種譯法，而且它是檢查會解析的檔案部分的名稱。 |
| Gestalt | 完形, 格式塔 | 格式塔 | 它是 glossary 裡一種 agency 的名稱。twin 可能用兩種譯法；在說明這個德文字的意思的句子裡，完形是正確的。 |
| glossary | 詞彙表, 術語表 | 詞彙表, 術語表 | twin 已用了三種譯法：詞彙表、術語表，以及英文的 glossary。 |
| handler | 處理器, 處理常式, 處理函式 | 處理器, 處理常式, 處理函式 | 它是程式針對某一種輸入或事件所用的程式碼的名稱，而且 twin 已用了三種譯法。 |
| handoff | 交棒 | 交棒 | 它是一種 outcome 的名稱。 |
| hard break | 強制換行, 硬換行 | 強制換行, 硬換行 | 它是 Markdown 在行尾保留的換行的名稱，而且 twin 已用了兩種譯法。 |
| hash | 雜湊, 雜湊值 | 雜湊 | 它是一種值的名稱，而且 twin 已用了不只一種譯法。 |
| here-string | 此處字串 | 此處字串 | 它是 PowerShell 一種字串常值的名稱，而且沒有固定的中文譯法。 |
| hook | 鉤子, 掛鉤 | 鉤子, 掛鉤 | 它是 repository 一部分的名稱，而且 twin 已用了不只一種譯法。 |
| hunk | 區塊, 差異區塊 | 差異區塊 | 它是 diff 一部分的名稱，而且沒有固定的中文譯法。 |
| idempotent-only mode | 冪等模式 | 冪等模式 | 它是 `reformat-md` 在檔案於執行開始時就已乾淨時所進入的模式的名稱。 |
| identifier | 識別碼, 識別字, 標識符 | 識別碼, 識別字, 標識符 | 它是程式或資料結構替某個項目所取名稱的總稱，而且 twin 已用了三種譯法。 |
| import | 匯入, 引入, 導入 | — | 它是 Python 一種陳述式的名稱，而且 twin 已用了三種譯法。 |
| inline code | 行內程式碼, 行內代碼 | 行內程式碼, 行內代碼 | twin 已用了兩種譯法：行內程式碼，以及英文的 inline code。 |
| interactive | 互動 | — | 它是一種 step 類型的名稱。 |
| interpolation | 內插, 插值, 插補 | 插補 | 它是 shell 把變數的值放進字串的做法的名稱，而且 twin 已用了三種譯法。內插與插值太常出現，不列入 Flagged，因為它們也是兩個數值之間的內插的名稱。 |
| introspection | 自省, 內省 | 自省, 內省 | 它是一種契約的名稱，而且 twin 已用了兩種譯法。 |
| MD report | MD 報告 | MD 報告 | 它是 skill 一種輸出的名稱。 |
| metadata | 元數據, 元資料, 中繼資料, 詮釋資料 | 元數據, 中繼資料, 詮釋資料 | 它是提供其他資料相關資訊的資料的名稱，而且 twin 已用了四種譯法。元資料太常出現，不列入 Flagged，例如單元資料與多元資料裡就有它。 |
| no-op | 空操作, 無操作 | 空操作, 無操作 | 它是一次沒有造成任何改動的執行的名稱，而且沒有固定的中文譯法。 |
| non-breaking space | 不斷行空格, 不換行空格, 不間斷空格 | 不斷行空格, 不換行空格, 不間斷空格 | 它是一行不會在該處斷開的空格的名稱，而且 twin 已用了三種譯法。 |
| null | 空值 | — | 它是一種值的名稱，拼法和資料所用的相同。 |
| one-run data | 一次執行的資料, 單次執行資料 | 單次執行資料 | 它是 DFD 中一種資料的名稱，而且沒有固定的中文譯法。一次執行的資料也是一般的片語，例如超過任何一次執行的資料，它太常出現，不列入 Flagged。 |
| outcome | 結果 | — | 它是一次執行交還給 caller 的 one-run data 的名稱。結果太常出現，不列入 Flagged。 |
| pairing line | 配對行 | 配對行 | 它是 twin 中有連結連回其來源的那一行的名稱，而且沒有固定的中文譯法。 |
| pattern | 模式, 樣式 | — | 它是符合正規表示式的文字的名稱，而且 twin 已用了兩種譯法。兩種譯法都太常出現，不列入 Flagged。 |
| pipe | 豎線, 直線, 管道符號 | 豎線, 管道符號 | 它是表格儲存格之間的字元的名稱，而且 twin 已用了三種譯法。直線太常出現，不列入 Flagged。 |
| placeholder | 佔位符, 占位符 | 佔位符, 占位符 | twin 已用了兩種譯法：佔位符，以及英文的 placeholder。 |
| plain scalar | 純量, 普通純量 | — | 它是 YAML 一種 scalar 寫法的名稱，而且沒有固定的中文譯法。 |
| process | 程序, 行程, 進程 | — | 它是 DFD 所顯示的工作單位的名稱。它不是作業系統的 process，而且 twin 已用了三種譯法。它們全都太常出現，不列入 Flagged，因為程序指的是 procedure，行程指的是作業系統的 process。 |
| prompt | 提示詞, 提示 | 提示詞 | twin 已用了兩種譯法，而且它是 skill 一種輸入的名稱。 |
| raw mode | 原始模式 | 原始模式 | 它是 `reformat-md` 的一種模式的名稱，由 `--mode raw` 選用。 |
| record | 紀錄, 記錄 | — | 它是 DFD 中一種資料的名稱，也是記錄指紋時得到的 outcome 的名稱。兩種譯法都太常出現，不列入 Flagged。 |
| repository | 儲存庫, 版本庫, 倉庫 | 儲存庫, 版本庫 | 它是 system 中一種類型的名稱，而且 twin 已用了三種譯法。 |
| request | 請求, 要求 | — | 它是 caller 提供的 one-run data 的名稱，而且 twin 已用了兩種譯法。在 app 中，它是路由收到的資料。兩種譯法都太常出現，不列入 Flagged。 |
| role | 角色 | 角色 | 它是向 system 提供資料、或從 system 讀取資料的人或程式的名稱。DFD 把它畫成 system 外部的六角形。 |
| schema | 綱要, 結構描述 | 綱要, 結構描述 | 它是檔案或 record 必須符合的結構的名稱，而且 twin 已用了不只一種譯法。 |
| script | 腳本, 指令碼 | 腳本, 指令碼 | twin 已用了兩種譯法：腳本，以及英文的 script。 |
| section partial | 章節片段, 局部檔 | 章節片段, 局部檔 | 它是存放一次執行輸出中某一節的檔案的名稱，而且沒有固定的中文譯法。執行把它寫在它的 checkpoint 旁邊。 |
| shell | 殼層, 命令列 | 殼層 | 它是啟動人或 agent 所寫指令的程式的名稱，而且 twin 已用了不只一種譯法。命令列指的是 command line，它太常出現，不列入 Flagged。 |
| skill | 技能 | 技能 | 它是 system 中一種類型的名稱。 |
| stage | 階段 | — | 它是 RSDC 的 Dataflow 中一個 process 的名稱。階段太常出現，不列入 Flagged，因為工作階段是 session，準備階段是一段時期。 |
| stale | 過期 | 過期 | 它是一種狀態的名稱。 |
| step | 步驟 | 步驟 | twin 已用了兩種譯法：步驟，以及英文的 step。 |
| system | 系統 | — | 它是 DFD 或設計文件所呈現之對象的名稱。它的 role 在它外部，它的 process 與 record 在它內部。系統太常出現，不列入 Flagged，因為作業系統指的是 operating system。 |
| template | 範本, 模板 | 範本, 模板 | twin 已用了兩種譯法：範本，以及英文的 template。 |
| term | 術語, 技術詞 | 術語, 技術詞 | twin 已用了兩種譯法：術語，以及英文的 term。 |
| token | 詞元, 權杖, 標記 | 詞元 | twin 已用了三種譯法，用在它是 LLM 所計算的單位時，也用在它是解析後字串的一部分時。 |
| traceback | 回溯, 追蹤訊息 | — | 它是程式因錯誤而停止時所給的輸出的名稱，而且沒有固定的中文譯法。 |
| twin | 孿生檔, 雙胞胎 | 孿生檔, 雙胞胎 | twin 已用了三種譯法：孿生檔、雙胞胎，以及英文的 twin。 |
| verdict | 判定結果, 裁決 | — | 它是一種 outcome 的名稱。 |
| wiki | 維基 | — | 它是 skill 寫入其 MD report 的位置的名稱，由 `wikiDir` 設定。維基太常出現，不列入 Flagged，例如維基百科裡就有它。 |
| wireframe | 線框圖, 線框稿 | 線框圖, 線框稿 | 它是 system 中一種文件類型的名稱，而且沒有固定的中文譯法。 |
| word character | 文字字元, 單字字元 | 文字字元, 單字字元 | 它是正規表示式中一類字元的名稱，而且 twin 已用了兩種譯法。 |
| workflow | 工作流程, 流程 | 工作流程 | twin 已用了兩種譯法，而且它是 skill 中一節的名稱。 |
| workspace | 工作區, 工作空間 | — | twin 已用了兩種譯法，而且它是 system 讀取資料的位置的名稱。 |

## Adding a term

如果譯者遇到不在這份清單上的 term，就套用「The rule」一節所給的規則。
如果這個 term 保留英文，譯者就在同一件工作中把它加入這份清單。
這個 term 的那一列，列出它所取代的譯法。
工具可以在 twin 中檢查其中一些譯法，而不會誤報。
那一列也把這些譯法，列為要列入 Flagged 的譯法。
如果譯者把這個 term 翻譯出來，整份 twin 就只用一種譯法。
