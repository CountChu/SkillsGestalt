# Task 105 - clone-gestalt 加上 core.autocrlf=false

**Status**：完成——[[clone-gestalt]] 第 3 步改成 `git clone -c core.autocrlf=false`，也寫了已經 clone 好時怎麼補；`4. 驗證` 加一項行尾的檢查。
**Raised**：2026-11-13，在 DevBox 做 [[clone-gestalt]] 時，`gen_agents_md.py` 因為 checkout 出來的檔是 CRLF 而以 2 結束。
**Depends on**：—

## 1. 背景

- 在 DevBox（Windows 11）照 [[clone-gestalt]] 做；repo 已經 clone 好，在 `main`。
- 這台的 Git 在 `C:/Program Files/Git/etc/gitconfig` 設了 `core.autocrlf=true`，是 Windows 版 Git 安裝時的預設。
- repo 沒有 `.gitattributes`。
- [[Task 104]] 在另一台電腦的 scratchpad 試做時，沒有遇到這個問題。

## 2. 結論

- 原因：`core.autocrlf=true` 讓 checkout 出來的檔都是 CRLF；`gen_agents_md.py` 以 `read_bytes().decode('utf-8')` 讀檔，每一行後面多一個 `\r`，就找不到單獨一行的 `{AGENTS-local}`（`3.1`）。
- 這台的 clone 設 `core.autocrlf=false`，重新 checkout 後，`gen_agents_md.py` 與 `--check` 都是 PASS（`3.1`）。
- [[clone-gestalt]] 第 3 步改成 `git clone -c core.autocrlf=false`，並寫了已經 clone 好時怎麼補；`4. 驗證` 加上 `core.autocrlf` 與 `git ls-files --eol` 的檢查（`3.2`）。
- clone-gestalt 是 Private，Forge 不做，所以 `CHANGES.md` 不記。
- 還沒做：加 `.gitattributes`（`* text=auto eol=lf`），讓每台電腦都不必自己設；要做的話另開 task（`3.3`）。

## 3. 過程

### 3.1 gen_agents_md.py 以 2 結束（2026-11-13）

- `gen_agents_md.py` 與 `--check` 都印出 `the template has 0 line(s) {AGENTS-local}, not 1`，以 2 結束。
- `file` 顯示 `AGENTS-tmp.md` 與 `AGENTS.md` 都是 CRLF；`git config --show-origin --get core.autocrlf` 是系統的 gitconfig 的 `true`。
- 修法：`git config core.autocrlf false`，`git status` 沒有改動，`git rm -rq --cached .` 與 `git reset -q --hard HEAD` 重新 checkout；之後 `AGENTS-tmp.md` 是 LF，`gen_agents_md.py` 印出 unchanged，`--check` 是 PASS。
- `git ls-files --eol`：repo 裡有 8 個檔本來就是 CRLF（`.gitignore`、`server.js`、`app.css` 與 5 個 `.py`），298 個是 LF；設了 `false` 之後，沒有一個 `i/lf` 的檔是 `w/crlf`。

### 3.2 改 clone-gestalt（2026-11-13）

- 第 3 步：`git clone -c core.autocrlf=false ...`。`-c` 在 clone 時寫進這個 clone 的 `.git/config`，checkout 之前就生效，不必重新 checkout。
- 第 3 步也寫了失敗時的訊息，以及已經 clone 好才發現時怎麼補。
- `4. 驗證`：`git config --local core.autocrlf` 是 `false`；`git ls-files --eol` 沒有一行是 `i/lf` 而 `w/crlf`。這台的 clone 兩項都符合。
- `5. 與其他 task、chore 的關係` 加本 task。

### 3.3 另一種做法：.gitattributes

- 在根目錄加 `.gitattributes`，寫 `* text=auto eol=lf`：它跟著 repo 走，優先於 `core.autocrlf`，Mac 與 Windows 都 checkout 出 LF，commit 時也存成 LF。
- `core.autocrlf=false` 時，編輯器存成 CRLF 的檔，commit 時不會轉回 LF；`.gitattributes` 沒有這個問題。
- 加了之後要 `git add --renormalize .`，把 3.1 的 8 個 CRLF 檔改成 LF。
- 使用者這次只要求改 chore，所以沒有做。

## 4. 要做的

1. ✅ 找出 `gen_agents_md.py` 以 2 結束的原因，在這台的 clone 修好（`3.1`）。
2. ✅ [[clone-gestalt]] 加上 `core.autocrlf=false`（`3.2`）。
3. ✅ 要不要在 `CHANGES.md` 記一筆：clone-gestalt 是 Private，不記。

## 5. 驗證

- `check_chores.py` 與 `check_tasks.py` 都是 PASS（`external/ASD-STE100_ISSUE9.pdf` 照 clone-gestalt 第 6 步複製過來之後）。
- 這台的 clone：`git config --local core.autocrlf` 是 `false`，`git ls-files --eol` 沒有 `i/lf` 而 `w/crlf` 的行。

## 6. 與其他 task 的關係

- [[Task 104]]：建立 [[clone-gestalt]]。
- [[clone-gestalt]]：本 task 改的 chore。

## 7. 知識

—

## 8. 日誌

### 2026-11-13

- 建立 task：在 DevBox 做 [[clone-gestalt]] 時 `gen_agents_md.py` 以 2 結束，原因是 CRLF；這台的 clone 設 `core.autocrlf=false` 修好，寫成 `3.1`。
- 使用者要求把這一步加進 [[clone-gestalt]]：改第 3 步與 `4. 驗證`，寫成 `3.2`；`.gitattributes` 的做法寫成 `3.3`，沒有做。Status 是完成。
