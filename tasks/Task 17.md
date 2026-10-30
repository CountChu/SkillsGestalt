# Task 17 - 讓 gen-rsdc-app 與 imp-app 跟上對齊後的 App 範本

**Status**：完成——2026-10-11 三項都做完（見下方「做了什麼」）。
**Raised**：2026-10-10，從 [[Task 12]] 拆出：App 範本對齊之後，用到它的 skill 還沒跟上。
**Depends on**：[[Task 12]]

## 1. 背景

[App 範本](../.github/common/skills/gen-rsdc-app/assets/RSDC-App-tmp.md)在 Task 12 改了三件 skill 會碰到的事：

- **可省略的節**：2.6 Derivation Rules 與 4.4 Platform Traps 標為 Optional，範本開頭寫明 app 沒有可寫的內容就省略，之後各節依序遞補。
  [gen-rsdc-app](../.github/common/skills/gen-rsdc-app/SKILL.md) 寫 design pair 的規則卻是「範本有的節都寫，沒有的都不寫」，沒有提到 Optional。
- **4.5 Verification Obligations 改成以主張為列**：表頭是 `| Claim | Rule | Proven by | Performed by |`，3.1 的每個 component 至少出現在一列，尚未證明的主張標 *not verified*。
  gen-rsdc-app（EN、tw 各 6 處）與 imp-app（各 10 處）仍以「每個 component 一列 acceptance」描述它：字彙表的 **acceptance**、寫 design pair 時「每個 component 一列」、交回與記錄的 Components 表的 Acceptance 欄，以及 imp-app 的 update（Step 3）補改 acceptance 列、test（Step 4）從 acceptance 列讀出 Component。
  gen-imp-app 的字彙表也有 **acceptance**。
- **RSDC Checker 讀得了 App 範本**（Task 12 的丙）：以 App 範本為形狀（`--template`、`--tw-template` 指向 gen-rsdc-app 的範本）檢查範本本身，12 項通過；2 項失敗只是 Twin 連結的佔位符，和 Skill-System 範本的自我檢查相同。
  但 gen-rsdc-app 與 imp-app 都不執行它，app 的 RSDC 仍然沒有機械檢查。

## 2. 現況

**[[Task 10]] 第 2 點已做的（2026-10-11）**：gen-rsdc-app 的 Step 1（EN 與 tw）已規定在 design pair 的檔頭連到 `> [[RSDC-App-tmp]]`，並以 `depends_on.py record … --config config.yaml` 記下，這一項不必再做。
`check_rsdc.py` 也已改成從檔頭讀出範本：第 3 點執行 RSDC Checker 時，連到範本的 app RSDC 不必再指定 `--template`；而檢查英文 RSDC 時，沒有連到範本會判 FAIL。

**做了什麼**（2026-10-11）：

1. gen-rsdc-app（EN 與 tw）寫 design pair 的規則加上例外：標 Optional 而 app 沒有內容的那一節省略，之後各節依序遞補編號。
2. 「acceptance」改名為 **verification obligation**：4.5 Verification Obligations 的一列，每個 component 至少出現在一列，尚未證明的標 *not verified*。
   - gen-rsdc-app、imp-app（EN 與 tw）與 gen-imp-app 的字彙表與步驟都改了；Components 表的 Acceptance 欄改為 Obligations 欄，YAML 的 `acceptanceRows` 改為 `verificationObligations`。
   - imp-app 的 update 補或改提到所改 component 的列；test 由 Proven by 或 Performed by 提到該 test 的那一列找出 component。
     gen-imp-app 的 Step 3 第 4 部分也改成以主張為列。
3. gen-rsdc-app 的 Step 1 寫完並記錄之後執行 RSDC Checker（先英文檔、再這一對），有 FAIL 就改到通過，交回的內容附上結果；Dataflow 與 Steps at a Glance 一起改。
   - `check_rsdc.py`：範本有 Directory Structure 或 Presentation Form 時不再禁止這兩節；沒有 CLI 節時，「每個 stage 有 component 執行」與「4.5 提到每個 component」改用 3.1 的 component 檢查。

## 3. 要做的

**要做的**：

1. gen-rsdc-app 寫 design pair 的規則加上 Optional 的例外（EN 與 tw）。
2. 「acceptance」改成 4.5 的主張列：gen-rsdc-app、imp-app、gen-imp-app 的字彙表與步驟，以及交回、記錄 components 的表格欄位；imp-app 的 update 與 test 改成依新的表找 component 與要補的列。
3. gen-rsdc-app 寫完 design pair 之後執行 RSDC Checker。
   先拿一份照新範本填好的 app RSDC 試跑，確認只屬 skill system 的檢查不會誤報。

**牽涉的檔案**：gen-rsdc-app、imp-app 的 `SKILL.md` 與 tw；gen-imp-app 的 `SKILL.md`；若有只屬 skill system 的檢查要跳過，還有 `check_rsdc.py`。

## 4. 驗證

**驗證**：App 範本與 tw 機械填成的合成樣本（另一份省略 4.4、之後遞補），修改前 Checker 判 2 項 FAIL（就是那兩節），修改後英文檔與 pair 全部通過；反向測試抓得到沒有執行者的 stage（FAIL）與 4.5 沒提到的 component（WARN）。
既有 7 份 RSDC 的 Checker 輸出與修改前逐字相同。
兩份 twin 依 chinese 的 INCREMENTAL 更新，parity 0 失敗，`diff_md.py --verify` 通過。

## 5. 與其他 task 的關係

**相關**：gen-rsdc-app 是 [[Task 14]] 建立的。
Task 14 的第 2 期（在新位置做範本對齊）已由 Task 12 做完；它的「要決定的」第 5 點也提到 Checker 的支援放在 gen-rsdc-app。

## 6. 日誌

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-11

- 三項都做完：gen-rsdc-app 與 imp-app 跟上對齊後的 App 範本，並執行 RSDC Checker。
- gen-rsdc-app 的 Step 1 規定連到 `RSDC-App-tmp`，`check_rsdc.py` 改成從檔頭讀出範本。

### 2026-10-10

- 提出：從 Task 12 拆出，App 範本對齊之後，用到它的 skill 還沒跟上。
