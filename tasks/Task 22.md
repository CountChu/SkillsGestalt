# Task 22 - 讓 gen-skill、check-skill 與 SKILL 範本跟上 README.md 的拆分

**Status**：完成——範本、gen-skill 與 check-skill 都已跟上，gen-skill 與 check-skill 自己也拆出 README.md（2026-10-11）；其餘 skill 的拆分由 [[Task 24]] 處理。
**Raised**：2026-10-11，Task 20 的 asd-ste 試點完成時，依「試點後另開 task」的決定提出。
**Depends on**：[[Task 20]]

## 1. 背景

背景：[[Task 20]] 把 asd-ste 的 SKILL.md 中執行時用不到的內容移到 [README.md](../.github/common/skills/asd-ste/README.md)，寫 skill 的共用規則則移到 [skill-writing.md](../.github/common/rules/skill-writing.md)。
產生與檢查 skill 的工具，原本仍以為這些內容在 SKILL.md 裡：check-skill 的 `scan_skill.py` 回報 asd-ste 缺少 Dataflow 與 Steps at a Glance，gen-skill 也不寫 README.md。

## 2. 現況

**已決定（2026-10-11）**

動手前問了 8 個問題，決定如下：

- **舊格式**：check-skill 一律要求新格式。
  沒有 README.md 的 skill，在 check 1 算一項 issue；SKILL.md 裡還留著 Dataflow、Steps at a Glance 或 Purpose 的，也是 issue。
- **範圍**：改範本、gen-skill 與 check-skill，並把 gen-skill 與 check-skill 自己也拆出 README.md 與 README-tw.md；其餘 skill 另開 [[Task 24]]。
- **gen-skill 寫 README.md 的時機**：新增獨立的 Step 5 - Build README.md，原本的 TW twin 改為 Step 6。
- **twin 的時機**：Step 1 詢問輸出檔時，一併詢問要不要 TW twin，Step 5 寫 README.md 時就知道要不要列 twin。
- **已移到 skill-writing.md 的規則**：SKILL 範本拿掉 no forward-reference、step 要自足、能用程式做就寫成腳本，以及「每個名詞只定義一次」；check-skill 的判準 1.4 也不再要求 MUST FOLLOW 宣告前兩條。
- **check-skill 的 README 檢查**：併入 check 1 Template alignment，不新增 check 7；Dataflow 仍由 check 6 檢查，改到 README.md 讀。
- **連帶影響**：gen-rsdc-skill 只做最小修補，改讀 README template 的 `## Dataflow`；它與 gen-imp-app 仍寫出舊格式的問題，記到 Task 24。
- **README.md 的 header quote**：依 skill 的內容而定。
  一律宣告 `DFD.md`、`md-style.md`、`skill-writing.md`、`SKILL-tmp.md` 與 `README-tmp.md`；寫 MD report 加 `report-md-rules.md`，寫 YAML checkpoint 加 `report-yaml-rules.md`，MUST FOLLOW 有那一行時加 `scratch-rules.md`，有 twin 加 `chinese/SKILL.md`，再加上 step 讀取或執行的其他共用檔案。

下列各項沒有另外詢問，由實作時決定：

- README 範本另有 twin `README-tmp-tw.md`，與 `SKILL-tmp-tw.md` 一樣；新寫的 README 都是每行一句。
  SKILL 範本只刪除內容，不重排成每行一句，留給 [[Task 19]]。
- header quote 的狀態：`MISSING` 是 issue，`CHANGED`、`NO_RECORD` 與 `NOTHING_CITED` 是 recommendation；沒有 header quote 的 README.md 是 issue。
- 已有 SKILL-tw.md、卻沒有 README-tw.md 的 skill，是 recommendation。
- 判準的編號只往後加，既有的編號不變，Skills Dashboard 上記錄的判準編號才不會指錯。

**做了什麼**

- 範本：新增 [README-tmp.md](../.github/common/templates/README-tmp.md) 與 [README-tmp-tw.md](../.github/common/templates/README-tmp-tw.md)，章節照 asd-ste 的 README.md，並以 placeholder 代入 skill 名稱、路徑、header quote 與各節內容。
  [SKILL-tmp.md](../.github/common/templates/SKILL-tmp.md) 與 twin 拿掉 Dataflow、Steps at a Glance、Workflow 開頭兩段、Purpose 行，以及已移到 skill-writing.md 的規則。
- [skill-writing.md](../.github/common/rules/skill-writing.md) 與 twin：新增「每個 skill 都有一份 README.md」，並把 Purpose 與「哪些 step 執行腳本」的回答都指向 README.md。
- [gen-skill](../.github/common/skills/gen-skill/SKILL.md)：Step 1 一併詢問 twin，Step 3 依 skill-writing.md 寫且不放 Dataflow 與 Purpose，新增 Step 5 - Build README.md（含 `depends_on.py record`），Step 6 為 SKILL.md 與 README.md 各寫一份 twin；新增 [README.md](../.github/common/skills/gen-skill/README.md) 與 README-tw.md。
- [check-skill](../.github/common/skills/check-skill/SKILL.md)：`scan_skill.py` 新增 `--readme-template` 與 `--depends-on`，記錄 `readme_shape` 事實，Dataflow 改從 README.md 讀；[checking-criteria.md](../.github/common/skills/check-skill/references/checking-criteria.md) 改寫判準 1.2、1.4、1.8、1.10，新增 1.11 到 1.14，check 6 改讀 README.md；7 行 Purpose 移到新增的 [README.md](../.github/common/skills/check-skill/README.md) 與 README-tw.md。
- gen-rsdc-skill：Step 0 的檢查清單與 Step 8 改讀 README template 的 `## Dataflow`，它的 Dataflow 節點與圖例跟著改。
- asd-ste 的 README.md：header quote 加上 `README-tmp.md`，「修改時」樹中的工具一節改寫，回歸檢查加上 `/check-skill asd-ste`；重新記錄 `SKILL-tmp.md` 與 `skill-writing.md` 的指紋。

**順帶發現**

- 有 4 個 skill 的 description 超過 1024 字元，skill loader 會略過它們：asd-ste 1108、gen-imp-app 1148、imp-home 2263、report-my-chats 1225。
  check-skill 的判準 1.1 會把它們報為 issue；這次沒有改。

## 3. 要做的

—

## 4. 驗證

**驗證（2026-10-11）**

- `check_parity.py`：README 範本、SKILL 範本、skill-writing、gen-skill 的 SKILL 與 README、check-skill 的 SKILL、README 與 checking-criteria、gen-rsdc-skill、asd-ste 的 README，共 11 組都沒有失敗。
- 每行一句：README 範本、三份 README 與 skill-writing 的 `reformat_md.py` 都不再改動任何一行，`check_reformat.py --twin` 都通過。
- `depends_on.py check`：asd-ste、gen-skill、check-skill 的 README.md 與 asd-ste 的 SKILL.md 全部 UNCHANGED。
- `scan_skill.py` 掃 `common` 的 30 個 skill 都沒有錯誤；asd-ste、gen-skill、check-skill 的 README.md 沒有缺少的標題，Step Purposes、Files Each Step Uses 與 Dataflow 都與 SKILL.md 的 step 標題一致，Dataflow 沒有 DFD 缺陷。

## 5. 與其他 task 的關係

—

## 6. 日誌

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-11

- 提出：Task 20 的 asd-ste 試點完成時，依「試點後另開 task」的決定提出。
- 範本、gen-skill 與 check-skill 都已跟上，gen-skill 與 check-skill 自己也拆出 README.md。
