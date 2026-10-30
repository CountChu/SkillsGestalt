# Task 27 - 確認在桌面版刪除 session 時是否會觸發 SessionEnd hook

**Status**：尚未開始——要實際測試。
**Raised**：2026-10-12，從 [[Task 23]] 的待辦移出；它與 asd-ste 無關，來自 skill token 的統計（`84bf91f`）。
**Depends on**：—

## 1. 背景

背景：`84bf91f` 讓 [skill_tokens_hook.py](../scripts/skill_tokens_hook.py) 把每個 session 的 skill 執行記進 `database/skill-tokens/`。
`~/.claude/settings.json` 在 `Stop` 與 `SessionEnd` 兩個 hook 都執行這支腳本。
官方文件列出的 `SessionEnd` 觸發原因，不包含在桌面版刪除 session，所以不知道刪除時它會不會執行。

## 2. 現況

**目前的狀況（2026-10-12）**

- 這支腳本只把錯誤寫進 `~/.claude/logs/skill-tokens-hook.log`，不記錄是哪個事件觸發的，也不記錄原因。
- 收到的紀錄檔路徑若不存在，腳本會直接結束、什麼都不做。
  所以即使刪除時有觸發，只要紀錄檔已經刪掉，結果也看不出差別。
- 資料不受影響：`Stop` hook 每次回話後都已記錄，紀錄檔消失時只會標記 `session_deleted: true`。

## 3. 要做的

**做法**

1. 讓腳本在 log 記下每次呼叫的事件名稱與原因，也就是 hook 輸入中的 `hook_event_name` 與 `reason`，以及紀錄檔當時是否存在。
2. 開一個測試 session，在桌面版刪除它，再查看 log。
3. 依結果決定要不要保留這行 log，並把結果記在本 task。

**牽涉的檔案**

- [skill_tokens_hook.py](../scripts/skill_tokens_hook.py)
- `~/.claude/settings.json` 的 `hooks`
- `~/.claude/logs/skill-tokens-hook.log`

## 4. 驗證

—

## 5. 與其他 task 的關係

**與其他 task 的關係**

- [[Task 23]]：本項原是它的待辦第 4 項，但與 asd-ste 無關。

## 6. 日誌

### 2026-10-18

- 2026-10-16 那一行連到的 `tasks/CLAUDE.md` 已刪除，連結改成 inline code，字句沒有改（[[Task 62.1]]）。

### 2026-10-16

- 依 `tasks/CLAUDE.md` 的格式重排成六章，內容沒有改。

### 2026-10-12

- 提出：從 Task 23 的待辦移出。
