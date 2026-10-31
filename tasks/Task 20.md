# Task 20 - 為 skill 建立 README.md：Dependency，以及 SKILL.md 執行時用不到的內容

**Status**：完成——asd-ste 試點完成，gen-skill、check-skill 與範本也由 Task 22 跟上（2026-10-11）；其餘 skill 的拆分由 [[Task 24]] 處理。
**Raised**：2026-10-11，建立 asd-ste skill、整理它的 SKILL.md 文件依賴關係之後提出。
**Depends on**：—

## 1. 背景

目標：為 skill 寫一份 `README.md`，放在該 skill 的目錄，內容有兩部分。

- **Dependency**：SKILL.md 的文件依賴關係。
  格式沿用建立 asd-ste 時對話中定下的寫法：依時期分成「執行 skill 時」與「修改 skill 時」兩段，以純文字的樹狀圖表示。
- **從 SKILL.md 移出的內容**：SKILL.md 中執行時用不到、只給人看的部分。
  skill 被觸發時，整份 SKILL.md 都會載入 context；把這些內容移出，每次執行讀進 context 的量就會減少。
  這部分原本是 [[Task 21]]，2026-10-11 併入本 task，分析見下方「併入的 Task 21」一節。

SKILL.md 不引用 README.md，所以執行時不會載入它。
asd-ste 的 [README.md](../.github/common/skills/asd-ste/README.md) 是第一份成品，格式以它為準。

**併入的 Task 21：SKILL.md 中執行時用不到的內容**

以 asd-ste 的 [SKILL.md](../.github/common/skills/asd-ste/SKILL.md) 為例，行號與大小以 commit 60e9538 為準。
全檔 28 KB，下面第 1–6 項合計約 6.6 KB，是 23%。

1. `# Dataflow`（L128–206，3.5 KB，12.3%）：Workflow 的每個 step 都已寫明自己讀寫什麼，沒有任何 step 引用 Dataflow。
2. 各 step 開頭的 `**Purpose**` 行，共 6 行（1.3 KB，4.6%）：說明每個 step 為什麼要獨立存在，屬於設計理由。
3. `# Steps at a Glance`（L207–221，0.6 KB，2.0%）：step 與 script 的對照表，內容各 step 裡都有；不寫 YAML checkpoint 的 skill，YAML 欄全是「—」。
4. `# Workflow` 開頭的兩段（L224–226，0.5 KB，1.9%）：解釋 Purpose 是什麼，以及哪些 step 用 script、為什麼。
5. 寫 skill 時才用的規則（0.5 KB，1.8%）：TERMINOLOGY 裡 no forward-reference 的定義（L12–13），以及 MUST FOLLOW 的「step 要自足」與「能用程式做的就寫成 script」（L59–62）。
   它們規範的是怎麼寫步驟，不是怎麼執行步驟。
6. 範本殘留（0.2 KB，0.7%）：不呼叫 API 的 skill 裡說明不需要 `ADO_PAT` 的兩行（L239–240），以及後面沒有任何 step 用到的「Save the canonical skill invocation for reference in later steps.」（L271）。

可以精簡、但不建議整段刪除的有兩類：
- Step 1、Step 3 列出 script 會印什麼的清單（L286–294、L348–363，2.2 KB，7.7%）：script 的輸出本身就有 `[PASS]`／`[FAIL]` 標籤，但清單讓 agent 先知道要看什麼。
- MUST FOLLOW 與術語表裡說明理由的句子：嚴格說不是必要的，但在規則沒寫到的情況下，能幫 agent 做出正確判斷。

## 2. 現況

**已決定（2026-10-11）**

- **範圍**：先只做 asd-ste，作為試點；格式穩定之後，再決定是否推廣到其他 skill。
- **語言**：英文 `README.md`，再由 chinese skill 產生 `README-tw.md`。
- **合併**：Task 21 併入本 task，README.md 的內容一次規劃：Dependency，加上從 SKILL.md 移出的 Dataflow、Purpose 與 Steps at a Glance。
- **維護**：gen-skill 產生 skill 時一併寫出 README.md；check-skill 檢查 README.md 與 SKILL.md 是否一致。
- **依賴追蹤**：README.md 以 header quote 宣告 SKILL.md 所依賴的檔案，例如 `DFD.md`、`md-style.md`、`SKILL-tmp.md`，讓 `depends_on.py check` 在它們改了時提醒。
  例外是 `ste-rules.md`：SKILL.md 自己也要以 header quote 宣告它。
  Step 2 依 `ste-rules.md` 的 House Rules 寫作，兩者綁得最緊；它改了，SKILL.md 就要複查。
  寫法是路徑連結 `[ste-rules.md](references/ste-rules.md)`，相對於 SKILL.md 的位置，從任何 workspace 都解析得到。

試點開始時又決定了下列各項（2026-10-11）：

- **執行時的依賴**：DFD 與文字樹兩者都留；check-skill 之後要比對兩者是否一致。
- **README.md 的章節**：依時期分章，依序是 When the Skill Runs（Dataflow、Step Purposes、Files Each Step Uses）、When the Skill Is Changed、Tracked Dependencies。
- **Purpose**：各 step 的 Purpose 移到 README.md。
  原本是 Steps at a Glance 表格的 Purpose 欄，2026-10-11 改為 Step Purposes 一節：不用表格，只列舉每個 step 與它的 Purpose，不再列 Script；「哪些 step 執行 script」那段移到 Files Each Step Uses。
- **其餘移出的內容**：第 6 項直接刪除；第 4、5 項移到新的共用規則檔 `.github/common/rules/skill-writing.md`，配 `skill-writing-tw.md`。
  SKILL.md 不連到它，由 README.md 與 gen-skill、check-skill 引用。
- **文字樹的寫法**：放在 fenced block 裡；chinese skill 照抄 fenced block，所以 README-tw.md 的樹也是英文。
- **工具與範本**：試點完成後另開 task，即 [[Task 22]]。
- **過時的檢視檔**：刪除未追蹤的 `SKILL-tw.mermaid.html`，因為 SKILL-tw.md 之後不再有圖。

README.md 的讀者也包括修改 skill 的 agent，為了讓 agent 真的會去讀它，又決定了下列各項（2026-10-11）：

- **README.md 的開頭**：加一句，說明修改 skill 之前先讀這份，做完 When the Skill Is Changed 列出的修改，再跑那裡列出的檢查。
- **skill-writing.md**：新增第一條規則，修改有 README.md 的 skill 之前先讀它；skill-writing-tw.md 同步。
- **自動載入**：在 `.github/common/skills/` 放一份 [CLAUDE.md](../.github/common/skills/CLAUDE.md)，英文、不要 twin，只指向 README.md 與 skill-writing.md。
  Claude Code 讀到這個目錄底下的檔案時會載入它；SKILL.md 不連到 README.md，這份檔案就是 agent 找到 README.md 的方式。
  VS Code Copilot 的 `.instructions.md` 這次不做。

**後來決定的（2026-10-11，在 Task 22 中）**

- 推廣到其他 skill：check-skill 一律要求新格式，每個 skill 都要有 README.md；其餘 skill 由 [[Task 24]] 逐一拆分。
- gen-skill 怎麼產生 README.md：新增 Step 5 - Build README.md，從 [README-tmp.md](../.github/common/templates/README-tmp.md) 寫出；「修改 skill 時」那一節由 gen-skill 依各 step 判斷寫成。
- README.md 的 header quote 宣告哪些檔案：依 skill 的內容而定，規則寫在 gen-skill 的 Step 5；asd-ste 的 README.md 另外加上 `README-tmp.md`。

**目前狀態**

- asd-ste 試點已完成（2026-10-11），起點是 commit ea20160 的 asd-ste。
  - 新檔 [README.md](../.github/common/skills/asd-ste/README.md) 與 [README-tw.md](../.github/common/skills/asd-ste/README-tw.md)，依時期分章，收錄 Dataflow、列舉各 step Purpose 的 Step Purposes、兩張文字樹，以及 header quote 宣告的依賴。
  - SKILL.md 從 28.6 KB 減為 22.0 KB，少了 23%：移出 Dataflow、Steps at a Glance、Workflow 開頭兩段與 6 行 Purpose，刪除第 6 項，並在 frontmatter 底下以 header quote 宣告 `ste-rules.md`；SKILL-tw.md 同步。
  - 新的共用規則檔 [skill-writing.md](../.github/common/rules/skill-writing.md) 與 [skill-writing-tw.md](../.github/common/rules/skill-writing-tw.md)，收錄第 4、5 項。
  - 刪除過時、未追蹤的 `SKILL-tw.mermaid.html`。

- check-skill 的 `scan_skill.py` 原本回報 asd-ste 缺少 Dataflow 與 Steps at a Glance 標題，6 個 step 也沒有 Purpose；Task 22 讓它改到 README.md 找之後，asd-ste 通過這些檢查（2026-10-11）。
- 原本的已知問題（`convert_spec.py` 的未 commit 修改）已在 commit 4c2ed8b 解決；PDF 已在 commit 39ed8db 進了 git。

**範例**

先前在這裡的 asd-ste 依賴圖草稿，已寫成 [README.md](../.github/common/skills/asd-ste/README.md) 的 When the Skill Runs、When the Skill Is Changed 與 Tracked Dependencies 三章。
以 README.md 為準，這裡不再保留副本，免得兩份各自走樣。

## 3. 要做的

**Dependency 的格式**

- 開頭先給路徑縮寫，例如 `asd-ste/` 指 `.github/common/skills/asd-ste/`，`common/` 指 `.github/common/`；`external/` 位於 workspace 根目錄。
- **執行 skill 時**：依 Workflow 的 step 逐一列出，每一行以一個動詞開頭。
  - 讀：讀取內容的檔案。
  - 查：只確認檔案存在，或有需要才查其中一段。
  - 跑：執行的 script 或 skill，底下再列出它讀寫的檔案。
  - 寫、改：產生或修正的檔案。

  最後列出執行時完全不讀、只被 SKILL.md 引用的檔案。
- **修改 skill 時**：以檔案為單位列出。
  `⇄` 表示兩邊必須一起改、保持一致；`─▶` 表示依賴對方的規定或格式。
  涵蓋 SKILL.md 與它的 twin、script、reference、範本與規則（`SKILL-tmp.md`、`DFD.md`、`md-style.md`）、共用的 script（`depends_on.py`）、各自的檢查工具，以及改了規則或字典之後要回頭處理的既有產出。
  最後寫出修改後要跑的回歸測試。
- 另列用 header quote 宣告、`depends_on.py check` 追蹤得到的依賴。

提議的去處：

- 每個 skill 自己的設計說明（第 1–3 項）→ 該 skill 目錄的 `README.md`。
  Steps at a Glance 多加一欄 Purpose，各 step 就不必再有 Purpose 行。
  SKILL.md 不引用 README.md，執行時就不會載入它。
- 所有 skill 共用的寫作規則（第 4、5 項）→ `.github/common/rules/` 底下的一份共用規則檔，由 gen-skill 與 check-skill 引用。
  這些內容在每個 skill 都一樣，寫進每份 README.md 等於複製很多份。
- 範本殘留（第 6 項）→ 直接刪除。
  check-skill 的檢查標準已寫明，skill 不需要的範本段落可以省略，例如不呼叫 API 的 skill 不必有 `ADO_PAT` 那一條。

需要一起改的地方：

- 範本：[SKILL-tmp.md](../.github/common/templates/SKILL-tmp.md) 與 [SKILL-tmp-tw.md](../.github/common/templates/SKILL-tmp-tw.md) 要拆出一份 README 範本。
- [gen-skill](../.github/common/skills/gen-skill/SKILL.md)：Step 3 要同時產生 README.md；Step 5 產生 twin 時，README.md 也要有 twin。
- [check-skill](../.github/common/skills/check-skill/SKILL.md)：[checking-criteria.md](../.github/common/skills/check-skill/references/checking-criteria.md) 的必要標題、MUST FOLLOW 契約、Step Purpose 與 Dataflow 各項，以及 `scan_skill.py`，都要改成到 README.md 找 Dataflow 與 Purpose。
- 現有的 skill：30 個 skill 中，有 Dataflow 與 Steps at a Glance 的有 5 個，有 Purpose 行的有 12 個，有 SKILL-tw.md 的有 10 個（2026-10-11 計）。

風險：

- 圖與表離開 SKILL.md 之後，改 step 時比較容易忘記更新 README.md。
  check-skill 必須比對 README.md 的 step 名稱、Dataflow 的 step 節點與 SKILL.md 的 step 標題是否一致；這是本方案成立的前提。
- Purpose 移走之後，執行中的 agent 看不到每個 step 存在的理由。
  理由若對執行時的判斷有幫助，應寫進 step 的指示或 MUST FOLLOW，而不是留在 Purpose。

**牽涉的檔案**

- 試點寫出或修改的：[asd-ste/SKILL.md](../.github/common/skills/asd-ste/SKILL.md)、[SKILL-tw.md](../.github/common/skills/asd-ste/SKILL-tw.md)、[README.md](../.github/common/skills/asd-ste/README.md)、[README-tw.md](../.github/common/skills/asd-ste/README-tw.md)，以及 [skill-writing.md](../.github/common/rules/skill-writing.md)、[skill-writing-tw.md](../.github/common/rules/skill-writing-tw.md) 與 [CLAUDE.md](../.github/common/skills/CLAUDE.md)。
- 由 Task 22 處理的：範本 [SKILL-tmp.md](../.github/common/templates/SKILL-tmp.md)、[SKILL-tmp-tw.md](../.github/common/templates/SKILL-tmp-tw.md)，以及 [gen-skill/SKILL.md](../.github/common/skills/gen-skill/SKILL.md)、[check-skill/SKILL.md](../.github/common/skills/check-skill/SKILL.md)。
- 推廣到其他 skill 時：每個 skill 目錄的 `README.md` 與 `README-tw.md`。

## 4. 驗證

- 驗證都通過：三組 twin 的 `check_parity.py` 沒有失敗；`depends_on.py check` 對 SKILL.md、SKILL-tw.md、README.md 與 README-tw.md 全部 UNCHANGED；六份檔案都是每行一句，英中逐句對齊；`check_ste.py` 對 DFD.md 與 DFD-ste.md 的回歸測試通過。

## 5. 與其他 task 的關係

**與其他 task 的關係**

- [[Task 19]]：README.md 與共用規則檔都要遵守每個句子一行的寫法。
- [[Task 21]]：已併入本 task（2026-10-11），上一節是它的分析。
- [[Task 22]]：讓 gen-skill、check-skill 與 SKILL 範本跟上本 task 的拆分。
- [[Task 24]]：把其餘 skill 改成新格式。

## 6. 知識

—

## 7. 日誌

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-11

- 提出：建立 asd-ste skill、整理它的 SKILL.md 文件依賴關係之後。
- asd-ste 試點完成，Task 21 併入本 task。
- 在 Task 22 中決定推廣到其他 skill，其餘 skill 的拆分由 Task 24 處理。
