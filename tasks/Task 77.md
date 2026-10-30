# Task 77 - 拆出 SKILL-Compile.md，並替 compile-skill 寫 README

**Status**：完成——2026-10-20 寫好 compile SOP（SKILL-Compile.md）與 compile-skill 的 README，各有中文版；SOP 只寫 agent 的判斷，程式都由 SKILL.md 執行，RSDC 不動；`--skill` 有一項已知 FAIL，見 [[Task 75]]。
**Raised**：2026-10-20，[[Task 18.2]] 完成後，使用者提出：RSDC 只寫 compile 做什麼與給 skill 的介面，agent 的編譯做法寫成另一份給 skill 引用的文件，再以 README 描述各文件的關係。
**Depends on**：—

## 1. 背景

- compile-skill 每次編譯，[SKILL.md](../.github/common/skills/compile-skill/SKILL.md) 的 Step 2 都要讀 SkillCompiler-RSDC 的第 2 到 4 章。
  RSDC 約 70KB，其中 Presentation Contract、Verification Obligations 與 Defects 等和編譯無關，讀它們是浪費 token。
- 使用者的看法：system 與 agent 互不認識，由 skill 調控。
  RSDC 寫 system，以及 compile 做什麼、給 skill 的介面；agent 一步一步怎麼做，寫在另一份給 skill 引用的文件。
- 執行時讀的檔要自給自足：skill 引用的文件若再引用 RSDC，執行 skill 時就會把 RSDC 拉進來。
  所以新文件不連到 RSDC，「它依 RSDC 寫成」這層關係寫在 README；SKILL.md 不連到 README，執行時不會讀它。
- compile-skill 還沒有 README.md，而 [skill-writing.md](../.github/common/rules/skill-writing.md) 要求每個 skill 都有一份照 README-tmp.md 寫的 README。

## 2. 現況

### 2026-10-20 查的結果

- SkillCompiler-RSDC.md 約 70KB、801 行；compile-skill 的 SKILL.md 約 19KB。
- 要移出的內容約 120 行：2.5 的 Action Type 分類準則與 Core Work or Chore（第 385–417 行的一部分）、3.2 的 Compiler（第 602–686 行），以及第 4 章 `skill.py` 的寫法。
- SKILL.md 的 Step 2（第 203 行）要求讀 design document 的第 2 到 4 章；MUST FOLLOW 第 83–89 行寫 design document 是 source of record，step 只引用節號、不重述規則，只拿著 design document 就能編譯。
- README-tmp.md 本身以 STE 寫成；照 [[Task 64]]，gen-skill 照它寫 README 時拿掉 STE 標記，所以 asd-ste、gen-skill 與 check-skill 的 README 都是一般英文。

### 已決定（2026-10-20）

提出時使用者回答了 8 個問題，開始做之後又回答了兩輪；做到一半，使用者改了做法，再回答兩輪共 8 個問題。
寫好之後，使用者要 SOP 只寫 LLM 的判斷、呼叫程式交給 SKILL.md，又回答了兩輪共 8 個問題。
原本把 agent 的做法移出 RSDC、寫成 SkillCompiler-Compile.md 的做法，已經不用；現在的做法：

- **RSDC 不動**：SkillCompiler-RSDC 與中文版維持 [[Task 18.2]] 的樣子，原本已經做的修改全部恢復，gen-rsdc-skill 因此重記的兩行指紋也恢復。
- **檔名與位置**：`SKILL-Compile.md`，放在 compile-skill 的 `references/`，和 SkillCompiler-RSDC 放在一起，有中文版。
- **SOP 只寫 agent 的判斷**：分成 Step 1 Classify the Step Actions、Step 2 Write the Compiled Script、Step 3 Correct the Script 與 Step 4 Prove the Steps，是 RSDC 3.2 中 Compiler 的部分；它不執行、也不提任何程式。
  只寫指令、條件與數值，不寫原由；禁止事項照留，但不附理由。
- **每一步以一行「Input」開頭**：只描述資料本身，例如 step inventory、指紋、沒過的檢查與執行結果，不說是哪支程式產生的。
- **Step 1 之前留一小節 Terms and Rules**：名詞的定義，以及每個 step 都遵守的規則。
- **Compiled Script 的 contract 留在 Write**：欄位、CLI、exit status、metadata 與寫法；Source Scanner 與 Contract Checker 的指令與 exit status 回到 SKILL.md。
- **Correct the Script**：輸入是沒過的 contract 檢查，或 Step 4 判定出在 script 的差異；script 整份重寫，絕不改 Skill Source，之後從第一項檢查重來。
- **Prove 的分工**：SOP 為每個 deterministic step 選不會有副作用的輸入、判斷執行結果；SKILL.md 執行 `--export-schema` 與每個 `--step`。
- **沒有檢查能證明的規則**：SOP 的 Write 寫完後依它們審視 script；SKILL.md 的 Step 3 報告時註明它們沒有檢查、不算通過。
- **SOP 不連到 RSDC**：它依 RSDC 寫成這件事寫在 README，README 的檔頭以 `cited` 記下 RSDC 被引用各節的指紋。
- **SKILL.md 執行每一支程式**：Step 1 執行 Source Scanner、Step 3 執行 Contract Checker，都依 exit code 決定下一步；Step 2 與 Step 4 把程式的結果交給 SOP 的 step，另外只留執行時的互動，也就是選單、顯示、`--force` 與 `run step N`。
  這份文件在 SKILL.md 裡叫 **compile SOP**，引用寫成「**compile SOP** Step 1 *Classify the Step Actions*」；MUST FOLLOW 寫明 SOP 不提程式也不提本 skill，以及 SOP 的四步在本 skill 的哪一個 step 做。
- **SKILL.md 不連到 RSDC**：檔頭的 `[[SkillCompiler-RSDC]]` 記錄移到 README；`check_rsdc.py --skill` 因此有一項 FAIL，記在 [[Task 75]]。
- **README**：照 README-tmp.md 的結構，用一般英文寫，不帶 STE 標記；SKILL.md 的 Purpose 與「Steps 1 and 3 run a script」那段搬到 README。
- **Depends on**：不設；寫好就 commit，這次的修改也記在本 task。

### 進度

- [SKILL-Compile.md](../.github/common/skills/compile-skill/references/SKILL-Compile.md)：199 行，Terms and Rules 之後是 Step 1 到 Step 4，每一步以 Input 開頭；metadata 的 JSON 範例照抄 RSDC 2.4。
  中文版照 [chinese](../.github/common/skills/chinese/SKILL.md) skill 更新：第一版逐行翻譯，判定 FULL；改成四步時判定 INCREMENTAL，翻譯 34 行、逐字保留 165 行。
- compile-skill 的 SKILL.md：DEDICATED TERMINOLOGY、MUST FOLLOW 與 Workflow 改寫，Step 1 與 Step 3 又執行程式、依 exit code 決定下一步，15 處引用 SOP 的 step；Workflow 開頭的 Purpose 說明與各 step 的 Purpose 移到 README。
  中文版照 chinese skill 更新，判定 INCREMENTAL；改到的句子把「腳本」「術語表」改成 script、glossary，檔頭的引用區拿掉。
- compile-skill 的 [README.md](../.github/common/skills/compile-skill/README.md)：Dataflow 有 30 個箭頭，藍色的是 10、11、13、14、19、24 與 25；SOP 連到 Step 2、3、4，Step 3 與 Step 4 修正時會整份重寫 Compiled Script。
  檔頭記下 RSDC 被引用 14 節的指紋 `0ac8fa44bb74`；中文版照 chinese skill 逐行翻譯，改成四步時判定 INCREMENTAL。

### 順帶發現

- check-skill 的 `scan_skill.py` 把 SKILL.md 裡往後的 step 編號列進 forward_references，從 4 筆變成 5 筆；多出的是 Step 0 引用 **compile SOP** Step 2，引用的是 SOP 的 step，不是本 skill 後面的 step。
- Dataflow 中 Compiled Script 由 Step 2、3、4 輪流寫入，`scan_skill.py` 把它列進 records_edited_in_turn；這是修正時整份重寫的設計，README 的圖說已寫明。
- check-md-deps 的 SKILL.md 與中文版 Step 3 的 record 範例，原本對 compile-skill 的 SKILL.md 記錄 `[[SkillCompiler-RSDC]]`；這筆 record 現在在 compile-skill 的 README.md，範例已跟著改成 README.md。
- compile-skill 的 SKILL.md 沒有「# Dataflow」一節，`--skill` 檢查照舊報 WARN，屬於 [[Task 24]]。

## 3. 要做的

✅ 2026-10-20 寫好 SKILL-Compile.md、README 與兩份中文版；SOP 只寫 agent 的判斷，程式都由 SKILL.md 執行；RSDC 恢復成 [[Task 18.2]] 的樣子。

## 4. 驗證

- compile-skill 的 SKILL.md、SKILL-Compile.md 與兩份中文版，都沒有提到 RSDC 或 design document，也沒有 § 引用：一次編譯只讀 SKILL.md 與 SOP。
- SOP 沒有提到 Source Scanner、Contract Checker 或它們的檔名；SOP 裡沒有 because、so that、otherwise 這類原由句。
- SOP 的 inline code 逐項對照 RSDC：只有 `skills/<name>/SKILL.md` 是 SOP 自己的寫法，其餘都和 RSDC 相同。
- SKILL.md 的 15 處 SOP 引用，節名都和 SOP 的標題相同。
- `check_rsdc.py --rsdc` 單獨 PASS，30 項通過；中英對照 PASS，13 項通過、2 個警告，都和 [[Task 18.2]] 相同。
- compile-skill 的 `check_rsdc.py --skill` 判 FAIL，6 項通過、1 項失敗：the skill links to SkillCompiler-RSDC.md，是本 task 的設計，記在 [[Task 75]]；gen-rsdc-skill 的 `--skill` 和之前一樣，是 [[Task 75]] 的已知誤判。
- `check_parity.py`：SOP、README 與 SKILL 三對都是 0 failure，沒有警告；三份中文版以 INCREMENTAL 更新時，`diff_md.py --verify` 都 PASS，change set 以外的行或節逐字保留。
- `depends_on.py check`：README 與中文版的 8 個依賴都是 UNCHANGED；RSDC 與中文版、gen-rsdc-skill 與中文版的記錄恢復後也都是 UNCHANGED。
- 三對以 `reformat_md.py --mode clean` 重排後都沒有差異。
- check-skill 的 `scan_skill.py`：SKILL.md 與 README 的必要標題齊全，Step Purposes 與 Files Each Step Uses 對得上五個 step，Dataflow 沒有漏畫的 step，也沒有無來源的資料。
- `scan_source.py` 照常判定 compile-skill 的 SKILL.md 為 valid。

## 5. 與其他 task 的關係

- [[Task 18.2]]：SkillCompiler-RSDC 剛照 template 對齊，Compiler 留在系統內；本 task 的 SOP 依它寫成，RSDC 不動。
- [[Task 75]]：`check_rsdc.py --skill` 預設 skill 會連到並引用它的 RSDC；compile-skill 改成只讀 SKILL-Compile.md 之後，這個前提不再成立，那一項 FAIL 記在它的現況。
- [[Task 76]]：system 與 agent 的分工；本 task 是這個分工在 SkillCompiler 上的做法。
  SkillCompiler-RSDC 3.1 第 593 行與 3.2 第 604 行仍寫成 Compiler 執行程式，要不要改留給它決定。
- [[Task 74]]：它改兩支 script 時會改 RSDC 的 4.5 Defects；README 引用的節不含 4.5，改它不會要求重讀 SOP，但它若改了 SOP 依據的節，例如 2.7 的 exit status，SOP 要跟著改。
- [[Task 70]]：它會改 compile-skill 的 SKILL.md 與中文版裡的共用句子；本 task 已改完這兩份檔，它從這個版本開始。
- [[Task 64]]：gen-skill 寫 README 時拿掉 STE 標記；本 task 的 README 照這個做法用一般英文。
- [[Task 73]]：SKILL-tw.md 改到的句子把「腳本」改成 script，該檔的稽核數字會比它記下的少。
- [[Task 24]]：compile-skill 的 SKILL.md 沒有 Dataflow 一節，屬於它要改的 skill 格式。

## 6. 日誌

### 2026-10-21

- 使用者問 RSDC 要不要跟著改：這次不改；3.1 第 593 行與 3.2 第 604 行要不要寫成由 skill 調控，留給 [[Task 76]]。

### 2026-10-20

- 提出：使用者要把 agent 的編譯做法拆成給 skill 引用的文件，並以 README 描述各文件的關係；回答了 8 個問題，決定寫在「已決定（2026-10-20）」。
- 開始做：使用者又回答了兩輪問題，例如 RSDC 每一節的去處、新文件分五節、README 用一般英文；寫了 SkillCompiler-Compile.md 與 README，RSDC 移出 agent 的做法，SKILL.md 改讀新文件。
- 更正「2026-10-20 查的結果」關於 README 的一行：原本說 asd-ste 的 README 是用 STE 寫的先例，是把內文的 ASD-STE100 誤當成 STE 檔；那幾份 README 都是一般英文（[[Task 64]]）。
- 使用者改了做法：RSDC 這次的修改全部恢復，SkillCompiler-Compile.md 改名為 SKILL-Compile.md，照 RSDC 以 Step 1 到 Step 5 寫成 SOP、不寫原由；又回答了兩輪共 8 個問題，「已決定（2026-10-20）」改寫成現在的做法。
- 寫好 SKILL-Compile.md 與中文版，SKILL.md 與中文版改成只指向 SOP，README 與中文版跟著改並重記 RSDC 的指紋；在 [[Task 75]] 記下 compile-skill 的 `--skill` FAIL。
- 照「順帶發現」改 [check-md-deps](../.github/common/skills/check-md-deps/SKILL.md) 的 SKILL.md 與中文版：Step 3 的 record 範例改成對 compile-skill 的 README.md 記錄 `[[SkillCompiler-RSDC]]`，因為對 SKILL.md 執行舊範例時，`depends_on.py record` 會以 `2` 結束；中文版照 chinese skill 更新，判定 INCREMENTAL，`check_parity.py` 0 failure，`diff_md.py --verify` PASS，兩份以 `reformat_md.py --mode clean` 重排都沒有差異。
- 使用者問 SOP 能不能只寫 LLM 的判斷、呼叫 script 交給 SKILL；回答了兩輪共 8 個問題，「已決定（2026-10-20）」改寫：SOP 改成四步，程式都由 SKILL.md 執行。
- SOP 與中文版、SKILL.md 與中文版、README 與中文版照新的分工改寫；RSDC 與 README 記下的指紋都不用動。
