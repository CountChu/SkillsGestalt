# Task 11 - 統一六份 twin 中被 keep-English list 新標記的譯法

**Status**：完成——2026-10-10 改好六份 twin：被標記的譯法換成英文（template、placeholder、inline code、twin，gen-skill 的「雙胞胎」換成 TW twin），連同清單 261005 就有的舊警告（deterministic、step、agent、stale）一起改，共 76 處，每份行數不變。
**Raised**：2026-10-10，用 chinese skill 翻譯它自己的 `SKILL.md` 時，依 keep-English list 的規則加了 10 個術語（版本 261005 → 261010），其中幾個附帶的標記譯法，在六份既有 twin 中產生了新的警告。
**Depends on**：—

## 1. 背景

背景：[tw-keep-english.md](../.github/common/references/tw-keep-english.md) 261010 新增的術語是 frontmatter、placeholder、inline code、fenced block、template、twin、verdict、skill、folded block scalar、plain scalar。
依清單本身的規則，它們有一種以上的譯法在用，或指稱系統中的某種類型或角色；而且在既有 twin 裡，保留英文本來就是多數（例如 template 有 81 處英文，範本 13 處）。
這些只是 `[WARN]`，不會讓 parity check 失敗；它們指出同一個概念在不同 twin 裡有不同寫法。

重現方式：`python .github/common/skills/chinese/scripts/check_parity.py --en <英文檔> --tw <twin> --keep .github/common/references/tw-keep-english.md`，看 `[WARN] '<譯法>' at ...` 那幾行。

## 2. 現況

### 狀態細節

RSDC-Standard-tw 歷史條目裡的 7 處「範本」也改了，不發新版本——只是 twin 的譯法統一，英文原文與規則都沒變。
六份 `check_parity.py` 都是 0 failure，不再有被標記譯法的警告；剩下 gen-skill 與 imp-app 的「unbolded」提醒不屬於本項。

| Twin | 被標記的譯法 → 應保留的英文 | 所在的行（2026-10-10） |
|---|---|---|
| [RSDC-Standard-tw.md](../.github/common/references/RSDC-Standard-tw.md) | 範本 → template | L105、107、121、125、126、139、147 |
| [check-skill 的 SKILL-tw.md](../.github/common/skills/check-skill/SKILL-tw.md) | 佔位符 → placeholder；行內程式碼 → inline code | L170；L173 |
| [checking-criteria-tw.md](../.github/common/skills/check-skill/references/checking-criteria-tw.md) | 行內程式碼 → inline code；佔位符 → placeholder | L28、87；L42 |
| [gen-skill 的 SKILL-tw.md](../.github/common/skills/gen-skill/SKILL-tw.md) | 範本 → template；雙胞胎 → twin | L22、146；L4、43、152、154 |
| [imp-app 的 SKILL-tw.md](../.github/common/skills/imp-app/SKILL-tw.md) | 孿生檔 → twin | L61、63、105 |
| [Wireframe-tw.md](../.github/common/skills/imp-home/references/Wireframe-tw.md) | 孿生檔 → twin | L3 |

**同幾份 twin 裡還有清單 261005 就有的舊警告**，不屬於本項，可以順手一起處理：check-skill 的 twin「確定性」1 行；gen-skill 的 twin「確定性」1 行、「步驟」1 行；imp-app 的 twin「代理人」1 行、「確定性」4 行、「過期」1 行、「步驟」26 行；Wireframe-tw「過期」1 行。

## 3. 要做的

**修法**：逐一讀過每個警告，指稱該術語的換成英文，同一個字用在別的意思上的就保留——清單的規則就是這樣要求的。
只換字、不動其他內容，三份逐行對應的 twin（RSDC-Standard-tw、checking-criteria-tw、Wireframe-tw）也就仍然逐行對應。
要注意的：

- **gen-skill 的「雙胞胎」**：它是字彙表術語 **TW twin** 的譯法，要換成 `TW twin`，不只是 twin。
  L4 在 frontmatter 的 description 裡，改完要用 `yaml.safe_load` 重新解析。
- **imp-app 的「孿生檔」**：L61、63 是字彙表中 **design pair** 與 **wireframe pair** 的定義（英文是 "its 繁體中文 twin"），L105 是 MUST FOLLOW 底下一條規則的粗體開頭；換成「繁體中文 twin」。
- **RSDC-Standard-tw 的「範本」**：七處都在 "Changes in This Version" 底下 261010、261009、261008 的條目裡。
  **要先決定**兩件事：要不要動這些歷史紀錄的用字（不動，警告就一直留著）；改的話要不要發新版本——標準的慣例是每次修改都是一個新版本，但這次改的是 twin 的用字，不是規則。
- **Wireframe-tw 的 L3** 是 pairing line。
  Wireframe 是 imp-home 的 **seed documents** 之一：改了只影響之後產生的 hub，已經產生的 hub 不會跟著改（同 Task 9 對 Home-RSDC 的說明）。

**也可以反過來**：若決定某個詞改為翻譯（例如 template 一律寫「範本」），就把那一列從清單拿掉並更新版本行，而不是改這些 twin。
但那樣要改的是其他寫英文的 twin——template 有 81 處——工作量大得多。

**牽涉的檔案**：上表的六份 twin；若決定改清單而不是改 twin，則是 `.github/common/references/tw-keep-english.md`（版本行與清單列）。

## 4. 驗證

驗證：六份的 `check_parity.py` 不再出現上表的警告，failure 仍為 0。

## 5. 與其他 task 的關係

與其他項的關係：Task 9（另外三份 twin 的修正）與 Task 10（chinese skill 承接 RSDC twin 的規則）也都在動 twin 與 chinese skill，可以排在同一次處理。

## 6. 知識

—

## 7. 日誌

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-10

- 提出：用 chinese skill 翻譯它自己的 `SKILL.md` 時，keep-English list 加了 10 個術語，在六份既有 twin 產生新警告。
- 改好六份 twin：被標記的譯法換成英文，連同舊警告共 76 處。
- RSDC-Standard-tw 歷史條目的 7 處「範本」也改了，沒有發新版本。
