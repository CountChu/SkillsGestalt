# Terms Kept in English in 繁體中文 Twins

> Version: 261030
> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-18`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-30`  `8cc2e2061175`

> This file is in ASD-STE100 Simplified Technical English (STE), Issue 9.
> Technical words: agency, agent, alias, app, argument, automated, baseline, caller, canonical skill invocation, cell, character, checkpoint, class, clean mode, clock, cognitive, column, command, command line, commit, context, contract, data structure, delimiter, design document, diff, docstring, document, epoch, event, exit status, external input, fence, fenced block, file, fingerprint, flag, folded block scalar, Forge, frontmatter, Gestalt, glossary, handler, handoff, hard break, hash, heading, here-string, hexagon, hook, hunk, idempotent-only mode, identifier, import, inline code, inline-code span, interactive, interpolation, introspection, line, line break, link, link target, list, match, math, MD report, metadata, no-op, non-breaking space, null, one-run data, operating system, pairing line, parse, path, pattern, pipe, placeholder, plain scalar, process, prose, raw mode, record, regular expression, rendering, repository, request, route, scalar, schema, script, second, section, section partial, sentence, separator, session, shell, skill, span, spelling, stage, stale, statement, step, string, string literal, style, table, template, term, text, token, traceback, twin, variable, verdict, version, wiki, wireframe, word, word character, workflow, workspace.

Each `-tw` twin keeps the terms of the list that follows in English in its prose.
Examples of a twin are the `SKILL-tw.md` of a skill, the `-RSDC-tw.md` of a design document and the `-tw.md` of a wireframe.
The spelling of each term in a twin is the same as in the English file.
This list records each decision one time.
Thus, the same term does not get two different renderings in two twins.

The name of tw-keep-english.md does not contain a date.
Only a change to a rule or to the list makes a new version, and the Version line shows the new version.
Thus, it is not necessary to change the documents that refer to tw-keep-english.md.
When a change does not change a rule or the list, the version stays the same.

## The rule

A term is a word or a phrase that always identifies the same type of item in a document.
Examples are *checkpoint*, *commit*, *placeholder* and *verdict*.
When a word does not always identify the same type of item, it is a general word, not a term.
A term stays in English when **one** of these three conditions is correct, or when more than one is correct:

- **Twins use more than one Chinese rendering for it.**
  A translator can select one of the renderings, and the translator of the next twin can select a different one.
  Then a reader cannot know that the two words are the names of the same item.
- **It is the name of a type, a state, an outcome or a role in the system.**
  A Chinese word for it does not agree with the identifier that the code, a schema or the English document uses.
  Then a reader must translate the word into English again to find the item that it identifies.
- **It is the name of a command.**
  A Chinese word for it does not agree with the name that you write to operate the command.
  Then a reader must translate the word into English again to find the command.

Translate all the other words.
This applies to a general word, and to a term that has one standard Chinese rendering, for example 指紋, 規格 or 檢查.
If a term is in the glossary of a document, the rules of that document keep the term in English.
This is correct when the term is on this list, and also when it is not on it.

This list applies only to prose.
Always copy a heading, an inline-code span, a fenced block, a path and a link target without a change.

## The list

The **Replaces** column gives each rendering that a translator can write for the term.
This column is for the translator, and for the person who examines the twin.
No rendering in this column is correct in the prose of a twin.
The prose of a twin uses the English term.

A tool examines the prose of a twin for each rendering in the **Flagged** column, and shows a warning when it finds one.
These tools are `check_parity.py --keep` of the `chinese` skill and `check_rsdc.py` of the `gen-rsdc-skill` skill.

Some renderings are also general words, or parts of general words.
Examples are 自動 in 自動化, and 互動 as a general word.
A tool also finds these renderings in correct sentences.
When a reader gets warnings about correct text, the reader can start to ignore all the warnings.
Thus, only the **Replaces** column shows these renderings.
When the **Flagged** column shows "—", the term has no rendering that a tool can examine the prose for without false alarms.

A rendering that a tool finds causes a `[WARN]` line, not a `[FAIL]` line.
A rendering that usually identifies the term can also identify a different item, in a sentence about that item.
Thus, a person reads each warning, and then makes a decision.

| Term | Replaces | Flagged | Why it stays English |
|---|---|---|---|
| agency | 代理機構, 機構 | 代理機構 | It is the name of a type of item in the glossary, and it has no standard Chinese rendering. |
| agent | 代理人, 代理 | 代理人 | Twins use two renderings for it, and it is the name of a role. |
| alias | 別名 | — | It is the name of a command of the shell: a Chinese word for it does not agree with the command `alias`. |
| app | 應用, 應用程式 | — | It is the name of a type in the system, and twins use two renderings for it: 應用, and the English word app. |
| automated | 自動, 無頭自動 | 無頭自動 | It is the name of a type of step. |
| baseline | 基準, 基線 | 基線 | It is the name of the commit that a diff starts from, and twins use more than one rendering for it. 基準 occurs too frequently to flag. |
| caller | 呼叫者, 呼叫端, 呼叫方 | 呼叫者, 呼叫端 | It is the name of the role external to the system that starts the system and supplies its request, and twins use three renderings for it. 呼叫方 occurs too frequently to flag, for example in 呼叫方式. |
| canonical skill invocation | 標準形式的 skill 呼叫, 標準的 skill 呼叫, 標準化的 skill 叫用方式, 標準化的 skill 呼叫形式, 標準化的 skill 呼叫式, 正規化的 skill 呼叫形式 | 標準形式的 skill 呼叫, 標準的 skill 呼叫, 標準化的 skill 叫用方式, 標準化的 skill 呼叫形式, 標準化的 skill 呼叫式, 正規化的 skill 呼叫形式 | It is the name of the `/<skill-name>` command and its parsed arguments, as Step 0 keeps them, and twins use six renderings for it. |
| checkpoint | 檢查點 | 檢查點 | It is the name of a record. |
| clean mode | 乾淨模式, 清理模式 | 乾淨模式, 清理模式 | It is the name of a mode of `reformat-md`, which `--mode clean` selects. |
| cognitive | 認知型, 認知性 | 認知型, 認知性 | It is the name of a type of step, and twins use two renderings for it. |
| commit | 提交, 送交 | 提交 | It is the name of a record of `git`, and twins use more than one rendering for it. |
| context | 上下文, 前後文, 語境, 情境 | — | It is the name of the text that a pattern must find around a match, and twins use four renderings for it. All of them occur too frequently to flag. |
| delimiter | 定界符, 分隔符號, 分隔符 | 定界符 | It is the name of a mark that opens or closes a span, for example a span of math, and twins use more than one rendering for it. 分隔符 occurs too frequently to flag, because it is also the name of a separator. |
| deterministic | 確定性, 決定性 | 確定性, 決定性 | It is the name of a type of step, and twins use two renderings for it. |
| diff | 差異, 比對 | — | It is the name of the output that `git` gives when it compares two versions of a file, and twins use more than one rendering for it. The two renderings occur too frequently to flag. |
| docstring | 文件字串, 說明字串 | 文件字串 | It is the name of a part of a program, and it has no standard Chinese rendering. |
| epoch | 紀元, 紀元時間 | 紀元 | It is the name of the time from which a clock counts its seconds, and it has no standard Chinese rendering. |
| exit status | 結束狀態, 退出狀態 | 結束狀態 | It is the name of an outcome of a program, and twins use more than one rendering for it. |
| external input | 外部輸入 | 外部輸入 | It is the name of a type of data in a DFD. |
| fence | 圍欄, 柵欄 | 圍欄, 柵欄 | It is the name of the line that opens or closes a fenced block, and it has no standard Chinese rendering. |
| fenced block | 程式碼區塊, 圍欄區塊 | 程式碼區塊, 圍欄區塊 | Twins use two renderings for it, and it is the name of a part of a Markdown file that a twin copies without a change. |
| folded block scalar | 摺疊區塊純量, 折疊式區塊 | — | It is the name of a YAML scalar style, and it has no standard Chinese rendering. |
| Forge | 工坊, 鍛造坊 | 工坊, 鍛造坊 | It is the name of a type of agency in the glossary, and it has no standard Chinese rendering. |
| frontmatter | 前置資料, 頁首資訊, 前言 | 前置資料, 頁首資訊 | Twins use two renderings for it, and it is the name of a part of a file that the checks parse. |
| Gestalt | 完形, 格式塔 | 格式塔 | It is the name of a type of agency in the glossary. Twins can use two renderings for it, and 完形 is correct in a sentence that gives the sense of the German word. |
| glossary | 詞彙表, 術語表 | 詞彙表, 術語表 | Twins use three renderings for it: 詞彙表, 術語表, and the English word glossary. |
| handler | 處理器, 處理常式, 處理函式 | 處理器, 處理常式, 處理函式 | It is the name of the code that a program uses for one type of input or event, and twins use three renderings for it. |
| handoff | 交棒 | 交棒 | It is the name of an outcome. |
| hard break | 強制換行, 硬換行 | 強制換行, 硬換行 | It is the name of a line break that Markdown keeps at the end of a line, and twins use two renderings for it. |
| hash | 雜湊, 雜湊值 | 雜湊 | It is the name of a value, and twins use more than one rendering for it. |
| here-string | 此處字串 | 此處字串 | It is the name of a PowerShell string literal, and it has no standard Chinese rendering. |
| hook | 鉤子, 掛鉤 | 鉤子, 掛鉤 | It is the name of a part of a repository, and twins use more than one rendering for it. |
| hunk | 區塊, 差異區塊 | 差異區塊 | It is the name of a part of a diff, and it has no standard Chinese rendering. |
| idempotent-only mode | 冪等模式 | 冪等模式 | It is the name of the mode that `reformat-md` goes into when a file is clean at the start of the run. |
| identifier | 識別碼, 識別字, 標識符 | 識別碼, 識別字, 標識符 | It is the name of the name that a program or a data structure gives to an item, and twins use three renderings for it. |
| import | 匯入, 引入, 導入 | — | It is the name of a Python statement, and twins use three renderings for it. |
| inline code | 行內程式碼, 行內代碼 | 行內程式碼, 行內代碼 | Twins use two renderings for it: 行內程式碼, and the English words inline code. |
| interactive | 互動 | — | It is the name of a type of step. |
| interpolation | 內插, 插值, 插補 | 插補 | It is the name of the procedure that a shell uses to put the value of a variable into a string, and twins use three renderings for it. 內插 and 插值 occur too frequently to flag, because they are also the names of an interpolation between two numbers. |
| introspection | 自省, 內省 | 自省, 內省 | It is the name of a contract, and twins use two renderings for it. |
| MD report | MD 報告 | MD 報告 | It is the name of an output of a skill. |
| metadata | 元數據, 元資料, 中繼資料, 詮釋資料 | 元數據, 中繼資料, 詮釋資料 | It is the name of data that gives information about other data, and twins use four renderings for it. 元資料 occurs too frequently to flag, for example in 單元資料 and 多元資料. |
| no-op | 空操作, 無操作 | 空操作, 無操作 | It is the name of a run that makes no change, and it has no standard Chinese rendering. |
| non-breaking space | 不斷行空格, 不換行空格, 不間斷空格 | 不斷行空格, 不換行空格, 不間斷空格 | It is the name of a space where a line does not break, and twins use three renderings for it. |
| null | 空值 | — | It is the name of a value, with the spelling that the data uses. |
| one-run data | 一次執行的資料, 單次執行資料 | 單次執行資料 | It is the name of a type of data in a DFD, and it has no standard Chinese rendering. 一次執行的資料 is also a usual phrase, for example in 超過任何一次執行的資料, and it occurs too frequently to flag. |
| outcome | 結果 | — | It is the name of the one-run data that a run gives back to its caller. 結果 occurs too frequently to flag. |
| pairing line | 配對行 | 配對行 | It is the name of the line of a twin that has a link back to its source, and it has no standard Chinese rendering. |
| pattern | 模式, 樣式 | — | It is the name of the text that agrees with a regular expression, and twins use two renderings for it. The two renderings occur too frequently to flag. |
| pipe | 豎線, 直線, 管道符號 | 豎線, 管道符號 | It is the name of the character between the cells of a table, and twins use three renderings for it. 直線 occurs too frequently to flag. |
| placeholder | 佔位符, 占位符 | 佔位符, 占位符 | Twins use two renderings for it: 佔位符, and the English word placeholder. |
| plain scalar | 純量, 普通純量 | — | It is the name of a YAML scalar style, and it has no standard Chinese rendering. |
| process | 程序, 行程, 進程 | — | It is the name of the unit of work that a DFD shows. It is not a process of an operating system, and twins use three renderings for it. All of them occur too frequently to flag, because 程序 is a procedure and 行程 is a process of an operating system. |
| prompt | 提示詞, 提示 | 提示詞 | Twins use two renderings for it, and it is the name of an input of a skill. |
| raw mode | 原始模式 | 原始模式 | It is the name of a mode of `reformat-md`, which `--mode raw` selects. |
| record | 紀錄, 記錄 | — | It is the name of a type of data in a DFD, and of the outcome when you record a fingerprint. The two renderings occur too frequently to flag. |
| repository | 儲存庫, 版本庫, 倉庫 | 儲存庫, 版本庫 | It is the name of a type in the system, and twins use three renderings for it. |
| request | 請求, 要求 | — | It is the name of the one-run data that a caller supplies, and twins use two renderings for it. In an app, it is the data that a route receives. The two renderings occur too frequently to flag. |
| role | 角色 | 角色 | It is the name of a person or a program that supplies data to the system or reads data from it. A DFD shows it as a hexagon external to the system. |
| schema | 綱要, 結構描述 | 綱要, 結構描述 | It is the name of the structure that a file or a record must agree with, and twins use more than one rendering for it. |
| script | 腳本, 指令碼 | 腳本, 指令碼 | Twins use two renderings for it: 腳本, and the English word script. |
| section partial | 章節片段, 局部檔 | 章節片段, 局部檔 | It is the name of a file that holds one section of the output of a run, and it has no standard Chinese rendering. The run writes it adjacent to its checkpoint. |
| shell | 殼層, 命令列 | 殼層 | It is the name of the program that starts the commands that a person or an agent writes, and twins use more than one rendering for it. 命令列 is a command line, and it occurs too frequently to flag. |
| skill | 技能 | 技能 | It is the name of a type in the system. |
| stage | 階段 | — | It is the name of a process of the Dataflow of an RSDC. 階段 occurs too frequently to flag, because 工作階段 is a session and 準備階段 is a period. |
| stale | 過期 | 過期 | It is the name of a state. |
| step | 步驟 | 步驟 | Twins use two renderings for it: 步驟, and the English word step. |
| system | 系統 | — | It is the name of the item that a DFD or a design document shows. Its roles are external to it, and its processes and records are in it. 系統 occurs too frequently to flag, because 作業系統 is an operating system. |
| template | 範本, 模板 | 範本, 模板 | Twins use two renderings for it: 範本, and the English word template. |
| term | 術語, 技術詞 | 術語, 技術詞 | Twins use two renderings for it: 術語, and the English word term. |
| token | 詞元, 權杖, 標記 | 詞元 | Twins use three renderings for it, when it is the unit that an LLM counts and when it is a part of a parsed string. |
| traceback | 回溯, 追蹤訊息 | — | It is the name of the output of a program when an error stops it, and it has no standard Chinese rendering. |
| twin | 孿生檔, 雙胞胎 | 孿生檔, 雙胞胎 | Twins use three renderings for it: 孿生檔, 雙胞胎, and the English word twin. |
| verdict | 判定結果, 裁決 | — | It is the name of an outcome. |
| wiki | 維基 | — | It is the name of the location where a skill writes its MD report, as `wikiDir` sets it. 維基 occurs too frequently to flag, for example in 維基百科. |
| wireframe | 線框圖, 線框稿 | 線框圖, 線框稿 | It is the name of a type of document in the system, and it has no standard Chinese rendering. |
| word character | 文字字元, 單字字元 | 文字字元, 單字字元 | It is the name of a class of characters in a regular expression, and twins use two renderings for it. |
| workflow | 工作流程, 流程 | 工作流程 | Twins use two renderings for it, and it is the name of a section of a skill. |
| workspace | 工作區, 工作空間 | — | Twins use two renderings for it, and it is the name of a location that a system reads from. |

## Adding a term

If a translator finds a term that is not on this list, the translator applies the rule that the section "The rule" gives.
If the term stays in English, the translator adds it to this list as a part of the same work.
The row of the term gives the renderings that it replaces.
A tool can examine a twin for some of these renderings without false alarms.
The row also gives each of these renderings as a rendering to flag.
If the translator translates the term, the full twin uses only one rendering for it.
