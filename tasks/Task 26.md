# Task 26 - 決定 ASD-STE100 規格的 PDF 是否留在 git 中

**Status**：尚未開始——要由使用者決定，還沒有決定。
**Raised**：2026-10-12，從 [[Task 23]] 的待辦移出。
**Depends on**：—

## 1. 背景

背景：asd-ste skill 以 ASD-STE100 Simplified Technical English（STE）Issue 9 的規格 PDF 為依據，見 [[Task 23]]。
PDF 在 [external/ASD-STE100_ISSUE9.pdf](../external/ASD-STE100_ISSUE9.pdf)，由其他 session 的 `39ed8db` commit 進 repo（2026-10-11）。
規格的版權頁寫明，未經 ASD 書面授權不得複製全部或部分內容，未經 STEMG 許可也不得散布。
建立 asd-ste 的 session 因此建議 PDF 不進 git，並建議把 `external/` 加進 `.gitignore`；當時使用者選擇不加。
從 PDF 抽出的字典 [ste-dictionary.json](../.github/common/skills/asd-ste/references/ste-dictionary.json) 也屬於規格的部分內容，當時由使用者決定 commit。

## 2. 現況

**目前的狀況（2026-10-12）**

- repo 沒有任何 remote，所以 PDF 只在本機的 git 歷史中，還沒有經由 git 散布出去。
  repo 放在 Dropbox 資料夾裡，檔案本身會隨 Dropbox 同步，這一點與 git 無關。
- asd-ste 執行時不讀 PDF 的內容，只在 Step 3 由 `depends_on.py` 讀它的位元組來算 fingerprint。
  找不到 PDF 時，STE 檔 header quote 的那一行不記錄，其餘照常。
- 字典 JSON 才是執行時真正用到的檔案：沒有它，asd-ste 在 Step 0 就會停下，要用 `convert_spec.py` 從 PDF 重建。

## 3. 要做的

**要決定的**

1. PDF：
   - 保留在 git 中：維持現狀；之後若要推到 remote 或分享 repo，再重新決定。
   - 只移出追蹤：`git rm --cached`，並加進 `.gitignore`；檔案留在磁碟上，asd-ste 照常可用，但先前的 commit 仍含有它。
   - 連歷史一起清除：移出追蹤之後，再改寫 git 歷史，從所有 commit 中拿掉它；`39ed8db` 之後每個 commit 的 hash 都會改變。
2. 字典 JSON：是否一起處理。
   移出 git 時，其他 clone 要先用 `convert_spec.py` 從 PDF 重建它，asd-ste 才能執行。

**牽涉的檔案**

- [external/ASD-STE100_ISSUE9.pdf](../external/ASD-STE100_ISSUE9.pdf)
- [ste-dictionary.json](../.github/common/skills/asd-ste/references/ste-dictionary.json)
- [.gitignore](../.gitignore)

## 4. 驗證

—

## 5. 與其他 task 的關係

**與其他 task 的關係**

- [[Task 23]]：建立 asd-ste；本項原是它的待辦第 3 項。

## 6. 日誌

### 2026-10-30

- [[Task 78]] 把 SkillsGestalt 公開到 GitHub 時，決定 PDF 不放進公開版；本機的 git 仍保留它，是否留在 git 中仍未決定。

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-12

- 提出：從 Task 23 的待辦移出，要由使用者決定 PDF 是否留在 git 中。
- 記下現況與要決定的事，還沒有決定。
