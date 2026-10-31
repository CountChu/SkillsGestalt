# Task 9 - 修正三份未通過 chinese parity check 的既有 twin

**Status**：完成——2026-10-10 三份都照 chinese 的規則改好，`check_parity.py` 都是 0 failure、也沒有警告。
**Raised**：2026-10-09，把 chinese skill 改成能翻譯任何英文 md 之後，用新的 `check_parity.py` 檢查 repo 裡全部 18 對 twin 時發現。
**Depends on**：—

## 1. 背景

背景：chinese skill 現在分兩種做法——有 frontmatter 的檔（每個 `SKILL.md`）逐個標題比對；沒有 frontmatter 的檔逐行對應（line for line），不另加 pairing line。
`check_parity.py` 也多了三項檢查：逐行對應、fenced block 逐字相同，以及畫面上會變成星號的粗體（只警告）。
下面三份 twin 都不是 chinese skill 寫的，失敗反映的是真實的差異，不是誤報；它們在舊版 `check_parity.py` 下本來就不通過（舊版假設每個檔都有 frontmatter、都連回 `SKILL.md`）。

## 2. 現況

### 狀態細節

SkillCompiler-RSDC-tw：block 6、7 換回英文檔的內容（逐字複製），「確定性」「工作流程」換成 deterministic、workflow。
Tasks-tw：依英文檔逐行重排成 39 行，多出的 pairing line 併進第 3 行、連回 `Tasks.md`；連到另一份文件的連結改連英文的 `SkillCompiler-RSDC.md`（使用者決定，與其他 twin 一致，chinese 的規則不必改）；目錄樹 block 逐字複製；順手把一處「退出狀態」統一成 exit status。
Home-RSDC-tw：四個章標題改回英文檔的字樣，「過期」換成 stale，L97 的「建置步驟」（build step，一般意思）改譯為「在建置時」；它是 seed document，已產生的 hub 不會跟著改。
下文「不在這一項」提到的 gen-rsdc-skill `SKILL-tw.md` 也已在 2026-10-10 重寫，parity 0 failure。

重現方式：`python .github/common/skills/chinese/scripts/check_parity.py --en <英文檔> --tw <twin> --keep .github/common/references/tw-keep-english.md`

| Twin | 失敗的檢查 | 差在哪裡 |
|---|---|---|
| [SkillCompiler-RSDC-tw.md](../.github/common/skills/compile-skill/references/SkillCompiler-RSDC-tw.md) | fenced blocks copied byte for byte | block 6（L367–408，JSON 範例）的 `name`、`description` 值譯成中文；block 7（L440–445，目錄樹）的樹狀符號改成 `├──`／`└──`，括號裡的說明譯成中文 |
| `.github/common/skills/compile-skill/references/Tasks-tw.md` | fenced blocks、link targets、line for line（行數 39 vs 41，19 行類型不同） | 舊格式：第 3 行另加一行 pairing line，之後整份錯開兩行；內文連到 `SkillCompiler-RSDC-tw.md`，英文檔連的是 `SkillCompiler-RSDC.md`；block 1（英文 L26–29、twin L28–31）的目錄樹與上一列的 block 7 同樣被改 |
| [Home-RSDC-tw.md](../.github/common/skills/imp-home/references/Home-RSDC-tw.md) | headings identical and in order | 四個章標題的問句譯成中文，例如英文的 `## 1 Requirements — "What problem does it solve?"` 寫成 `## 1 Requirements — 「它解決什麼問題？」`（L15、45、157、210） |

**不在這一項**：同一次檢查中，gen-rsdc-skill 的 `SKILL-tw.md` 也不通過，原因是另一個 session 正在改它的 `SKILL.md`（加了 Step 12 - Write the MD Report），twin 尚未同步；舊版 `check_parity.py` 一樣不通過，與本項無關。

## 3. 要做的

**各份的修法與要決定的**：

1. **SkillCompiler-RSDC-tw.md**：把 block 6、7 換回英文檔的內容，逐字複製；順便讀過兩個 keep-English 警告——'確定性'（L14、74、78，deterministic）與 '工作流程'（L26、33，workflow）。
   這份 RSDC 還是舊格式（§2.1 仍叫 *Artifact Types and Flow*），Task 1 與 Task 7 都提到它日後要依現在的 RSDC 範本重寫；重寫若在即，這兩個 block 可以併進去一起改。
   不論哪一種，結果都一樣：`check_rsdc.py` 的 pair 檢查同樣要求 fenced block 逐字相同。
2. **Tasks-tw.md**：用 chinese skill 重新產生——`/chinese .github\common\skills\compile-skill\references\Tasks.md`（覆寫前會先問）。
   重新產生後，pairing line 由第 3 行的譯文承擔、連回 `Tasks.md`，不再另加一行；標題的 `（繁體中文）` 會保留（chinese Step 2 的例外）。
   **要先決定**：twin 連到另一份文件時，連英文檔還是那份文件的 twin？
   chinese 的規則是連結目標一律不變，也就是連 `SkillCompiler-RSDC.md`；repo 裡其他 twin 也都連英文檔，只有這份連 twin。
   若要讓 twin 連 twin，要先改 chinese 的 `SKILL.md`（Step 2 第 5 點 Links）與 `check_parity.py` 的 link targets 檢查，例如容許：英文檔連 `X.md`、而 `X-tw.md` 存在時，twin 連 `X-tw.md`。
3. **Home-RSDC-tw.md**：把四個章標題改回英文檔的字樣；順便讀過兩個 keep-English 警告——'過期'（L11、27、81、150，stale）與 '步驟'（L97，step）。
   依據是 RSDC standard 261008 的變更紀錄（`RSDC-Standard.md` 第 132 行）：twin "keeps the headings, the topic names and the Dataflow's terms in English, so that both use the same words as every RSDC and its twin"。
   要注意兩點：
   - Home-RSDC 是 imp-home 的 **seed documents** 之一，`gen` 會把它複製到每個 hub 的 `docs\`。
     改 seed 只影響之後產生的 hub；已經產生的 hub 各有自己的 `docs\Home-RSDC-tw.md`，不會跟著改。
   - imp-home 本身沒有規定 twin 的標題要不要譯，只要求兩份在同一節號下一起改。

暫時的傾向（尚未決定）：三份都照 chinese 的規則改——SkillCompiler-RSDC-tw 只換兩個 block、Tasks-tw 用 chinese 重新產生並連英文檔、Home-RSDC-tw 改回英文標題。

**牽涉的檔案**：

- `.github/common/skills/compile-skill/references/SkillCompiler-RSDC-tw.md`
- `.github/common/skills/compile-skill/references/Tasks-tw.md`
- `.github/common/skills/imp-home/references/Home-RSDC-tw.md`
- 若決定 twin 可以連 twin：`.github/common/skills/chinese/SKILL.md` 與 `.github/common/skills/chinese/scripts/check_parity.py`。

## 4. 驗證

驗證：三份的 `check_parity.py` 都 0 failure。

## 5. 與其他 task 的關係

—

## 6. 知識

—

## 7. 日誌

### 2026-10-20

- 「狀態細節」的表格連到的 `Tasks-tw.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 71]]）。

### 2026-10-19

- 照 keep-English list，4 處譯成中文的 pairing line 改成英文，意思沒有改（[[Task 68]]）。

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-10

- 三份 twin 都照 chinese 的規則改好，check_parity.py 都是 0 failure。
- gen-rsdc-skill 的 SKILL-tw.md 也已重寫。

### 2026-10-09

- 提出：把 chinese skill 改成能翻譯任何英文 md 之後，用新的 check_parity.py 檢查全部 18 對 twin 時發現三份未通過。
