# Task 57 - 擴充 Chore 1：列出已是核准詞的技術用字，並在拼法清單改了之後重查

**Status**：尚未開始——2026-10-18 記下，兩件例行的後續併進 [[Chore 1]]，不另立 chore。
**Raised**：2026-10-18，檢視哪些 task 適合做成 chore 時提出：Technical words 的清理與拼法清單改了之後的重查，都跟著 STE 檔的重檢一起做最順。
**Depends on**：—

## 1. 背景

- Technical words 的清理：[[Task 44]]、[[Task 47]]、[[Task 49]]、[[Task 51]] 都是「某個字收進專案核准詞，再把它從每份 STE 檔與草稿的 Technical words 拿掉」，2026-10-16 到 10-18 做了四次。
  `check_ste.py` 其實會以 `[INFO] technical words the dictionary approves anyway` 說出清單裡已經核准的字，但 `draft.py recheck` 只印 FAIL 與 WARN，所以 [[Chore 1]] 跑完也看不到。
- 拼法清單：asd-ste 的 README 寫著 [us-spelling.json](../.github/common/references/us-spelling.json) 加了字，就要重查每份 STE 檔；但 STE 檔的檔頭沒有記錄它的指紋，改了不會報 CHANGED，也就沒有人知道該重查。

## 2. 現況

### 已決定（2026-10-18）

- 兩件都併進 [[Chore 1]]，不另立 chore。
- 提交：本 task 的修改前綴 `task 57`。

### 要決定的

- `recheck` 怎麼列出已經核准的技術用字：照樣印成 `[INFO]`，或當成要處理的一項；列出之後由 Chore 1 直接從清單拿掉，或另開 task。
- us-spelling.json 改了怎麼讓 Chore 1 知道：每份 STE 檔的檔頭加上它的紀錄，像 ste-custom.md 一樣；或由 `recheck` 記下上次用的指紋，另外比對。
- 改了之後，Chore 1 的標題與「何時要做」要不要跟著調整。

## 3. 要做的

1. 決定「要決定的」三項。
2. 改 `draft.py recheck`；先讀 asd-ste 的 [README.md](../.github/common/skills/asd-ste/README.md) 的 When the Skill Is Changed，照它改並跑它列出的檢查。
3. 改 [[Chore 1]] 的「何時要做」與「怎麼做」，摘要表跟著改。

## 4. 驗證

- 在 workspace 以外的副本上把一個技術用字收進 ste-custom.md：`recheck` 列出每一份還把它列為技術用字的檔。
- 在副本上改 us-spelling.json：Chore 1「看出該做了」的方法會列出要重查的檔。
- `check_chores.py` 與 `check_tasks.py` 都 PASS。

## 5. 與其他 task 的關係

- [[Chore 1]]：本 task 擴充它。
- [[Task 52]]：寫了 `draft.py recheck`。
- [[Task 44]]、[[Task 47]]、[[Task 49]]、[[Task 51]]：四次 Technical words 的清理。
- [[Task 38]]：us-spelling.json 與美式拼法的檢查。

## 6. 日誌

### 2026-10-18

- 建立。
