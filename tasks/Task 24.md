# Task 24 - 把其餘 skill 改成 SKILL.md 與 README.md 的新格式

**Status**：尚未開始——Task 22 讓 check-skill 一律要求新格式之後，其餘 skill 都還是舊格式。
**Raised**：2026-10-11，Task 22 決定 check-skill 一律要求新格式時提出。
**Depends on**：[[Task 22]]、[[Task 32]]

## 1. 背景

背景：[[Task 22]] 讓範本、gen-skill 與 check-skill 跟上 README.md 的拆分。
check-skill 現在要求每個 skill 都有一份以 [README-tmp.md](../.github/common/templates/README-tmp.md) 寫成的 README.md（判準 1.2），而 SKILL.md 裡留著 Dataflow、Steps at a Glance 或 Purpose 的，也是 issue（判準 1.11）。
規則見 [skill-writing.md](../.github/common/rules/skill-writing.md)；拆分的範例是 asd-ste、gen-skill 與 check-skill 的 README.md。

## 2. 現況

**目前的狀況（2026-10-11，以 `scan_skill.py` 掃 `common` 的 30 個 skill）**

- 有 README.md 的只有 asd-ste、gen-skill 與 check-skill；其餘 27 個在 check 1 都會有一項 issue。
- SKILL.md 仍有 Dataflow、Steps at a Glance、Purpose 行或介紹 Purpose 那一段的，共 8 個（括號內是行數）：ask-note（6）、check-md-deps（7）、chinese（8）、compile-skill（6）、gen-rsdc-app（5）、gen-rsdc-skill（14）、imp-app（8）、imp-home（6）。
- 其他群組的 skill 還沒掃過。

## 3. 要做的

**要改的地方**

- 每個 skill：以 README-tmp.md 寫出 README.md，有 SKILL-tw.md 的也寫 README-tw.md。
  把 Dataflow、Steps at a Glance 與 Purpose 行移過去，SKILL.md 拿掉這些內容，以及已移到 skill-writing.md 的規則；做法照 gen-skill 的 Step 5。
- gen-rsdc-skill：Task 22 只把 Step 8 改成照 README template 的 `## Dataflow` 畫，它仍把 `# Dataflow` 寫進目標 skill 的 SKILL.md。
  應改為寫進目標 skill 的 README.md，`check_rsdc.py` 檢查 skill 之 Dataflow 的部分也要跟著改。
- gen-imp-app：Step 3 從 SKILL template 寫出 owner skill，每個 step 都帶 step purpose。
  應改為同時寫出 README.md，把 step purpose 放進 Step Purposes。

**需要先決定的**

- 先做哪些 skill：被其他 skill 引用的，例如 chinese 與 check-md-deps，或依 Skills Dashboard 的順序。
- 其他群組的 skill 是否一起做。
- gen-rsdc-skill 與 gen-imp-app 的修改，是否與 [[Task 14]]、[[Task 17]] 一起做；那兩個 task 也在改這兩個 skill 周邊的檔案。

## 4. 驗證

—

## 5. 與其他 task 的關係

**等 [[Task 32]]（2026-10-12 決定）**：[[Task 31]] 讓 asd-ste 為 README-tmp.md 與 SKILL-tmp.md 產生 STE 草稿；Task 32 審核通過後由 asd-ste 取代原檔，再更新所有 skill 照範本抄的共用句子。
本 task 等 Task 32 完成再做，README.md 直接照 STE 範本寫，免得寫完再改一次。

- [[Task 54]]：依賴本 task——其餘 skill 改成新格式之後，才建立 Chore 3，定期以 check-skill 檢查每個 skill。

## 6. 知識

—

## 7. 日誌

### 2026-10-30

- [[Task 78]] 刪除了 report-my-chats 與 write-note-chat：清單從 10 個改成 8 個。

### 2026-10-18

- [[Task 54]] 依賴本 task，關係一章加上它。
- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-12

- 決定等 Task 32 完成再做，README.md 直接照 STE 範本寫。

### 2026-10-11

- 提出：Task 22 決定 check-skill 一律要求新格式，其餘 skill 都還是舊格式。
- 以 `scan_skill.py` 掃 `common` 的 30 個 skill，記下現況。
