# Task 106 - publish-gestalt 第 4 步拿掉 --co-author

**Status**：完成——[[publish-gestalt]] 第 4 步的指令不再加 `--co-author`，並寫明快照與 work branch 重新開始的 commit 都不寫 `Co-Authored-By`。
**Raised**：2026-11-13，照第 4 步發佈的快照 `4235a83` 有 `Co-Authored-By`，使用者要求拿掉，也要求改掉第 4 步。
**Depends on**：—

## 1. 背景

- [[publish-gestalt]] 第 4 步的指令有 `--co-author "<agent 的名稱與 email>"`。
- [publish_snapshot.py](../skill-groups/common/scripts/publish_snapshot.py) 有這個參數時，快照 commit 與 work branch 重新開始的 commit 都加一行 `Co-Authored-By`；沒有就不加。
- 2026-11-02 與 2026-11-10 的發佈，照使用者的決定沒有加，但第 4 步沒有跟著改。
- 2026-11-13 在 `devbox` 照第 4 步發佈，快照 `4235a83` 有這一行；使用者要求拿掉，換成 `7f62c8a`，見摘要表 `### publish-gestalt` 的 2026-11-13。

## 2. 結論

- [[publish-gestalt]] 第 4 步的指令拿掉 `--co-author`，加一句「不加 `--co-author`」；第 5 章加本 task。
- `publish_snapshot.py` 不改：`--co-author` 本來就是選用的，Forge 照 `publish:` 寫自己的 chore 時，可以自己決定。
- publish-gestalt 是 Private，Forge 不做，所以 `CHANGES.md` 不記。

## 3. 過程

### 3.1 找 --co-author 用在哪裡（2026-11-13）

- 在 repo 找 `co-author` 與 `Co-Authored`：只有 [[publish-gestalt]] 第 4 步、`publish_snapshot.py` 與摘要表的執行紀錄。
- `publish_snapshot.py` 的 `--co-author` 沒有預設值，不給就不加這一行。

### 3.2 改 publish-gestalt（2026-11-13）

- 第 4 步的指令拿掉 `--co-author "<agent 的名稱與 email>"`，下面加一行：不加 `--co-author`，快照與 work branch 重新開始的 commit 都不寫 `Co-Authored-By`。
- `5. 與其他 task、chore 的關係` 加本 task。

## 4. 要做的

1. ✅ 改 [[publish-gestalt]] 第 4 步（`3.2`）。
2. ✅ 要不要改 `publish_snapshot.py`：不改，參數是選用的（`2. 結論`）。
3. ✅ 要不要在 `CHANGES.md` 記一筆：publish-gestalt 是 Private，不記。

## 5. 驗證

- `check_chores.py` 與 `check_tasks.py` 都是 PASS。
- 下次發佈時，快照 commit 與 work branch 重新開始的 commit 都沒有 `Co-Authored-By`。

## 6. 與其他 task 的關係

- [[Task 78]]：建立 [[publish-gestalt]]。
- [[Task 105]]：同一天的另一個 task；它的發佈就是這次換掉的 `4235a83`。

## 7. 知識

—

## 8. 日誌

### 2026-11-13

- 建立 task：使用者要求把 [[publish-gestalt]] 第 4 步的 `--co-author` 拿掉；找出用到的地方，寫成 `3.1`；改第 4 步與第 5 章，寫成 `3.2`。Status 是完成。
