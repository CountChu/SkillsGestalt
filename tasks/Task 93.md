# Task 93 - 縮短超過 1024 字元的 skill description，並寫出 asd-ste 的 Step 6 會啟動審核伺服器

**Status**：完成——四個 skill 的 description 都在 1024 字元以內，check-skill 的 1.1 都通過；imp-home 另補上 MD report 與 YAML checkpoint。
**Raised**：2026-11-01，[[Task 40]] 驗證對照頁時，check-skill 找到 asd-ste 的 description 有兩個問題；使用者要求另開 task，並一併盤點其他 skill。
**Depends on**：—

## 1. 背景

skill loader 只接受 1024 字元以內的 description，超過的 skill 可能載不進來。
[[Task 40]] 第 1 項的驗證時，check-skill 對 asd-ste 報出兩個問題：

- **1.1**：SKILL.md 的 description 太長。
- **3.3**：description 沒有寫出 Step 6 會在背景啟動審核伺服器 `review_server.js`。

這兩個問題是 asd-ste 既有的，不是 Task 40 造成的；Skills Dashboard 的 asd-ste 列記成 ❌。

## 2. 現況

### 2026-11-02 四個 skill 都改好之後

**表 1：四個 skill 的 description 字元數**

| Skill | 改之前 | 改之後 |
|---|---|---|
| asd-ste | 1254 | 958 |
| imp-home | 2263 | 971 |
| gen-imp-app | 1148 | 967 |
| chinese | 1161 | 1007 |

- **刪掉的**：每個指令或 step「為什麼這樣做」的理由，以及實作細節，例如 imp-home 的 mount 怎麼委派、chinese 的 `(SKILL.md becomes SKILL-tw.md)`；行為、產出與觸發語都留著。
- **imp-home 的 check 3**：description 原本沒寫每次執行都會寫的 MD report 與 YAML checkpoint，這次補上。
- **中文版**：imp-home 與 chinese 的 SKILL-tw.md 照新的英文重譯；`check_parity.py` 0 failure，警告數和改之前相同。
- **check-skill 的 check 1 與 3**：1.1 都通過，check 3 都 ✅。
  check 1 另報出三個 skill 都還是舊格式，沒有 README.md，imp-home 與 chinese 的 Purpose 還在 SKILL.md；這屬於 [[Task 24]]。

### 2026-11-02 asd-ste 改好之後

- 2026-11-02 的 check-skill 報出同樣兩項，編號是 1.1 與 3.1；使用者點名修這兩項。
- asd-ste 的 description 從 1254 字元縮成 958 字元，並寫出 Step 6 的 HTML review page 由本機 Node.js 的 review server 提供。
- 拿掉的細節：段落上限、project-approved words、depends_on.py 記錄指紋，以及「只為了以核准的 draft 取代來源檔才改動它」那一句。
- SKILL-tw.md 的 description 照 chinese skill 翻譯新的 description；`check_parity.py` 0 failure。
- Skills Dashboard 的 asd-ste 列標記為要重查；這次跑 check-skill 時 dashboard 檔不存在，是新建的。

### 2026-11-01 盤點

量的是 SKILL.md frontmatter 裡 `description:` 的字元數。

**超過 1024 字元，本 task 要縮短**（2026-11-01 量的值；那時 imp-home 量成 2316，2026-11-02 以 check-skill 量是 2263）

- [imp-home](../skill-groups/common/skills/imp-home/SKILL.md)：2316
- [asd-ste](../skill-groups/common/skills/asd-ste/SKILL.md)：1254
- [gen-imp-app](../skill-groups/common/skills/gen-imp-app/SKILL.md)：1177
- [chinese](../skill-groups/common/skills/chinese/SKILL.md)：1161

**在 1000 與 1024 之間，只記下，本 task 不改**

- check-skill：1018
- gen-rsdc-skill：1017
- gen-rsdc-app：1013
- compile-skill：1002

## 3. 要做的

1. 縮短 asd-ste、imp-home、gen-imp-app、chinese 四個 skill 的 description，每一個都在 1024 字元以內。
   動手之前，先和使用者確認要拿掉或改寫哪些內容。
2. asd-ste 的 description 寫出 Step 6 會在背景啟動審核伺服器。
3. 每一個 skill 都照它的 README.md 的 When the Skill Is Changed 改，並跑它列出的檢查；沒有 README.md 的 skill，照 [skill-writing.md](../skill-groups/common/rules/skill-writing.md)。
4. 有 `SKILL-tw.md` 的 skill（asd-ste、imp-home、chinese），中文版照 chinese skill 跟著改。
5. 改完以 check-skill 檢查四個 skill，並更新 Skills Dashboard 的列。

**牽涉的檔案**

- 四個 skill 的 `SKILL.md`，以及 asd-ste、imp-home、chinese 的 `SKILL-tw.md`
- Skills Dashboard

## 4. 驗證

- check-skill 的 check 1 與 3，跑 asd-ste、imp-home、gen-imp-app 與 chinese：四個 skill 的 1.1 都通過，check 3 都 ✅；asd-ste 另跑了全部六項，都 ✅。
- `check_parity.py`：asd-ste、imp-home 與 chinese 的 SKILL.md 各和中文版比對，0 failure。

## 5. 與其他 task 的關係

- [[Task 40]]：驗證對照頁時發現 asd-ste 的兩個問題，記在它第 1、3、9 項的驗證裡。
- [[Task 24]]：把其餘 skill 改成新格式時，也會改到這些 SKILL.md；兩個 task 不要同時做。
- [[Task 54]]：建立定期以 check-skill 檢查每個 skill 的 chore；之後同類的問題由它找出來。

## 6. 知識

### 適合寫成新 topic

—

### 適合併進現有 topic

—

### 不算知識

- **縮短 description 時，先刪「為什麼」的理由與實作細節**：行為、產出與觸發語要留著，否則 check 3 會報少寫了東西。

## 7. 日誌

### 2026-11-02

- 連結的目標路徑從 `../.github/` 改成 `../skill-groups/`，字句沒有改（[[Task 97.7]]）。
- 使用者核准 imp-home、gen-imp-app 與 chinese 的新 description，並回答其他 3 個問題；三個 skill 的 description 都縮到 1024 字元以內，中文版跟著重譯。
- check-skill 報 imp-home 的 3.1：description 沒寫 MD report 與 YAML checkpoint；使用者點名修，補上之後 check 3 變成 ✅。
- 引用 chinese/SKILL.md 的 asd-ste、check-skill、compile-skill 與 gen-skill 的 README 與中文版，因為只改了 description，讀過之後重記指紋。
- 「現況」、「驗證」與「知識」三章跟著改，本 task 完成。
- 改好 asd-ste 的 description（check-skill 的 1.1 與 3.1）；其餘三個 skill 仍待做，Status 改為進行中。
- 同一次 check-skill 的 5.1 與 6.1，以及 SkillsGestalt 的 `.venv`，記在 [[Task 95]]。
- 重跑 check-skill，報出 3.1：縮短時拿掉了「the source's own」，description 變成說 draft 的 header quote 不變；改回「the source's own header quote」，958 字元，中文版改成「來源檔自己的 header quote」。

### 2026-11-01

- 提出：從 [[Task 40]] 的驗證結果移出，並盤點全部 skill 的 description 長度。
