# Task 97.2 - 規則改寫在 AGENTS.md，CLAUDE.md 只引用它

**Status**：完成——規則寫在 AGENTS.md，CLAUDE.md 只有一行 `@AGENTS.md`，兩個檔都由 `gen_agents_md.py` 產生；InvestForge 要照 CHANGES.md 跟上。
**Raised**：2026-11-02，Copilot harness 不讀 CLAUDE.md，但不用設定就讀 AGENTS.md；使用者決定規則改寫在 AGENTS.md。
**Depends on**：—

## 1. 背景

- 根目錄的 CLAUDE.md 由 [gen_claude_md.py](../skill-groups/common/scripts/gen_agents_md.py) 從 [CLAUDE-tmp.md](../skill-groups/common/templates/AGENTS-tmp.md) 與 `CLAUDE-local.md` 產生，寫了 Markdown、twin、task、chore、設定與分支的規則。
- Copilot harness 讀 repo 根目錄到工作目錄之間每一層的 AGENTS.md；Claude Code 讀 CLAUDE.md，可以用 `@AGENTS.md` 引用另一個檔。
- 另外還有 `.github/common/skills/CLAUDE.md`，告訴 agent 改 skill 前先讀 README.md。

## 2. 現況

### 2026-11-02 查的結果

- 提到 CLAUDE.md 的檔（不算中文版）：CHANGES.md、forge-setup.md、glossary.md、chore-rules.md、task-rules.md、gen_claude_md.py、asd-ste 與 gen-skill 的 README.md、CLAUDE-tmp.md、config-forge-tmp.yaml、根目錄的 README.md、config.example.yaml，以及 chores 的 follow-gestalt.md 與 pull-gestalt.md。

### 已決定（2026-11-02）

使用者回答了 8 個問題，都照建議：

1. **範本與 local 檔改名**為 `AGENTS-tmp.md` 與 `AGENTS-local.md`。
2. **script 改名**為 `gen_agents_md.py`。
3. **CLAUDE.md 只有 `@AGENTS.md` 一行**。
4. **`skills/CLAUDE.md` 的內容搬進範本的 Skills 一節**，檔案刪掉：Copilot 只讀 repo 根目錄到工作目錄之間的 AGENTS.md，讀不到那一層。
5. **不相容舊的寫法**：只有 `CLAUDE-local.md` 時，script 停下並說明怎麼改名。
6. **AGENTS.md 也做 STE 檢查**，和原本的 CLAUDE.md 一樣。
7. **InvestForge 只靠 CHANGES.md**。
8. **tasks/ 的舊紀錄不改**，只修會斷的連結，日誌加一行。

### 2026-11-02 改好之後

- `git mv`：`CLAUDE-tmp.md` → [AGENTS-tmp.md](../skill-groups/common/templates/AGENTS-tmp.md)、`CLAUDE-local.md` → [AGENTS-local.md](../AGENTS-local.md)、`gen_claude_md.py` → [gen_agents_md.py](../skill-groups/common/scripts/gen_agents_md.py)；`skills/CLAUDE.md` 刪掉。
- gen_agents_md.py 寫出 AGENTS.md 與只有 `@AGENTS.md` 的 CLAUDE.md，`--check` 比對兩個檔；slot 改名為 `{AGENTS-local-top}` 與 `{AGENTS-local}`。
- 範本：引言寫明 script 也產生 CLAUDE.md；Skills 一節加上改 skill 前先讀 README.md 與 skill-writing.md 的規則；`Technical words:` 加上 directory、line、section。
- 改了上面列的檔裡指 CLAUDE.md 的地方，中文版也是；`config.yaml` 的註解也改了。
- 摘要表的開頭段落：連到 AGENTS.md，也補上 [[Task 97.7]] 漏改的 `../.github/` 連結。
- task 檔：11 個檔的連結目標改成改名後的檔；7 個檔連到已刪掉的 `skills/CLAUDE.md`，改成 inline code；日誌各加一行。
- CHANGES.md 加一筆；舊條目裡連到 `CLAUDE-tmp.md` 的連結目標改成 `AGENTS-tmp.md`，字句不改。

## 3. 要做的

1. 問使用者幾個細節：範本與 local 檔是否改名（例如 `AGENTS-tmp.md`、`AGENTS-local.md`）、script 是否改名、CLAUDE.md 除了 `@AGENTS.md` 是否還寫別的、`.github/common/skills/CLAUDE.md` 是否也改成 AGENTS.md。
2. 改 gen_claude_md.py：寫 AGENTS.md，CLAUDE.md 只有 `@AGENTS.md`；`--check` 也比對兩個檔。
3. 改上面列的檔裡指 CLAUDE.md 的地方，中文版也是。
4. 重新產生 SkillsGestalt 的 AGENTS.md 與 CLAUDE.md。
5. 在 CHANGES.md 加一筆，InvestForge 照 follow-gestalt 重新產生。

## 4. 驗證

- `gen_agents_md.py --check` 通過。
- 新的 Claude Code session 載入的規則和改之前相同。
- Copilot harness 的 Chat 照 task-rules 開 task。
- AGENTS.md 的 STE 檢查通過。

## 5. 與其他 task 的關係

- [[Task 97]]：本 task 的上層。
- [[Task 80]]：把根目錄的 CLAUDE.md 改寫成英文與 STE。

## 6. 知識

—

## 7. 日誌

### 2026-11-02

- 完成：AGENTS.md 與 CLAUDE.md 由 `gen_agents_md.py` 產生，範本與 local 檔改名，`skills/CLAUDE.md` 併進範本。
- 連結的目標路徑從 `../.github/` 改成 `../skill-groups/`，字句沒有改（[[Task 97.7]]）。
- 提出。
