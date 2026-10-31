# Task 80 - 根目錄的 CLAUDE.md 改寫成英文

**Status**：完成——2026-10-30 [CLAUDE.md](../CLAUDE.md) 全部改成英文，以 ASD-STE100 寫，`check_ste.py` PASS。
**Raised**：2026-10-30，使用者比較 InvestForge 與 SkillsGestalt 的 CLAUDE.md 之後，要把 SkillsGestalt 的寫成英文。
**Depends on**：—

## 1. 背景

[CLAUDE.md](../CLAUDE.md) 的開頭與規則連結是英文，但 Branches、Tasks、Chores 三節是中文。
InvestForge 的 CLAUDE.md 全部是英文；[task-rules.md](../.github/common/rules/task-rules.md) 這些共用規則也是英文。

## 2. 現況

- CLAUDE.md 全部是英文，開頭有 header quote，宣告 ASD-STE100 Issue 9 與 ste-custom，並列出 technical words。
- Branches、Tasks、Chores 三節照原本的中文逐句翻譯，內容不變；指令照舊用實際路徑 `.github/common`。

## 3. 要做的

### 已決定（2026-10-30）

- 照原本的中文逐句翻譯，不照 InvestForge 的句子。
- 不建中文版 `CLAUDE-tw.md`：它是給 agent 讀的，InvestForge 也沒有。
- 以 ASD-STE100 寫，過 `check_ste.py`；中文的術語都換成英文，檔名與路徑照舊。
- Branches 一節的 tag 說明與 [[publish-github]] 的連結一起翻成英文。

## 4. 驗證

- `check_ste.py --ste CLAUDE.md` 是 PASS。
- `depends_on.py check CLAUDE.md` 是 UNCHANGED。
- `reformat_md.py --mode clean` 不改動。

## 5. 與其他 task 的關係

- [[Task 79]]：加了 Branches 一節。

## 6. 日誌

### 2026-10-30

- 建立 task 並完成：CLAUDE.md 改寫成 STE 英文，加上 header quote。
- 修正：為了讓段落不超過 6 句而拆開的 Tasks 一節，新段落開頭的「This file」讀起來像指 CLAUDE.md，改成「The `config.yaml`」；Branches 一節拆開的第二段開頭是「The commits」，沒有這個問題。
- 照 InvestForge 的 CLAUDE.md，開頭那條 twin 的規則搬成一節「繁體中文 twins」，放在 Branches 與 Tasks 之間，並加上 keep-English list 與它換版本後要做的 [[keep-english]]；開頭只留 md-style 那條。
- Branches 一節移到最後，內容不變；順序成為 繁體中文 twins、Tasks、Chores、Branches。
- [[Task 86]] 把 chore 改用名稱：本檔的 `[[Chore N]]` 連結改成新名稱。
