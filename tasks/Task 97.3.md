# Task 97.3 - skill 只寫動作，不寫某個 agent 才有的工具名稱

**Status**：完成——check-skill 改成「問使用者一題多選題」，skill-writing.md 多一條規則，check 5 多了 criterion 5.6；Forge 照 CHANGES.md 用 5.6 查自己的 skill。
**Raised**：2026-11-02，check-skill 寫死 Copilot 的 `vscode_askQuestions`，Claude Code 沒有這個工具；使用者決定 skill 只寫動作。
**Depends on**：—

## 1. 背景

- Copilot 與 Claude Code 讓使用者選擇的工具不同：Copilot 是 `vscode_askQuestions`，Claude Code 是 `AskUserQuestion`。
- skill 寫了工具名稱，換一個 agent 就找不到這個工具。

## 2. 現況

### 2026-11-02 查的結果

- common 的 skill、規則與範本（不算中文版）裡，只有 [check-skill/SKILL.md](../skill-groups/common/skills/check-skill/SKILL.md) 第 176 行寫了工具名稱 `vscode_askQuestions`。
- `update_dashboard.py` 的 `vscode_url` 是 `vscode://file` 連結，不是 agent 的工具，不在本 task 的範圍。

### 已決定（2026-11-02）

使用者回答了 8 個問題，都照建議：

1. **第 176 行改成「ask the user one multiple-choice question」**，header、question、multiSelect 與六個選項照舊。
2. **skill-writing.md 的新規則放在 Rules 最後**。
3. **check-skill 加 criterion 5.6 Agent-specific tool names**，放在 check 5 Cross-platform compatibility 下面。
4. **由 agent 讀 SKILL.md 判斷**，`scan_skill.py` 不改：工具名稱沒有固定的格式。
5. **5.6 找到的是 issue**：別的 agent 沒有這個工具，這個 step 會失敗或被略過。
6. **CHANGES.md 請 Forge 用 5.6 查自己的 skill**。
7. **Skills Dashboard 不動**，下次執行 check 5 時才有 5.6 的結果。
8. **一個 commit**，本 task 標完成。

### 2026-11-02 改好之後

- [check-skill/SKILL.md](../skill-groups/common/skills/check-skill/SKILL.md) 的 check picker 改成問一題多選題；picker 的選項 5 與 Step 3 的表也寫到 step 寫的工具。
- [skill-writing.md](../skill-groups/common/rules/skill-writing.md) 多一條：step 寫要做的動作，不寫只有某個 agent 才有的工具名稱；`Technical words:` 加上 action、criterion、question。
- [checking-criteria.md](../skill-groups/common/skills/check-skill/references/checking-criteria.md) 的 check 5 多一句說明與 criterion 5.6；`vscode_url` 這類只是前綴相同的名稱不算。
- check-skill 的 README 寫明 skill-writing.md 也決定 5.6。
- 以上的中文版都跟著改；依賴 skill-writing.md 的 10 個檔重記指紋。
- [CHANGES.md](../skill-groups/common/CHANGES.md) 加一筆。

## 3. 要做的

1. check-skill 第 176 行改成動作，例如「讓使用者從選項中選擇要套用的檢查」；中文版也是。
2. [skill-writing.md](../skill-groups/common/rules/skill-writing.md) 加一條規則：skill 寫要做的動作，不寫某個 agent 才有的工具名稱；中文版也是。
3. 照 check-skill 的 README，看是否要加一項檢查來找出工具名稱。
4. 在 CHANGES.md 加一筆。

## 4. 驗證

- common 的檔裡找不到 `vscode_askQuestions`、`AskUserQuestion` 這類工具名稱。
- skill-writing.md 與 check-skill 的 STE 檢查與 parity check 通過。

## 5. 與其他 task 的關係

- [[Task 97]]：本 task 的上層。
- [[Task 76]]：也在 skill-writing.md 加規則；兩個 task 同時做的話，會改到同一個檔。

## 6. 知識

—

## 7. 日誌

### 2026-11-02

- 完成：改了 check-skill、skill-writing.md 與 checking-criteria.md，中文版也是；CHANGES.md 加一筆。
- 連結的目標路徑從 `../.github/` 改成 `../skill-groups/`，字句沒有改（[[Task 97.7]]）。
- 提出。
