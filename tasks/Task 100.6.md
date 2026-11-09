# Task 100.6 - 其餘 9 個 skill 補上 process record

**Status**：完成——9 個 skill 都補上 process record，`common` 的每個 skill 都寫 process record 了。
**Raised**：2026-11-06，[[Task 100]] 決定每個 skill 都寫 process record；[[Task 100.4]] 只改有 checkpoint、暫存檔或引用舊規則問題的 skill，其餘的留到本 task。
**Depends on**：[[Task 100.4]]

## 1. 背景

- [run-data-rules.md](../skill-groups/common/rules/run-data-rules.md) 規定每次執行都有 Run Number，並寫一份 `database\skill-runs\{skill}\{yymmdd}.{N}.yaml`。
- 這 9 個 skill 沒有 checkpoint，也不寫暫存檔，只缺 process record，做法都一樣。

## 2. 結論

—

## 3. 過程

### 2026-11-06 改好之後

- 9 個 skill 分給 3 個 subagent 改，只加 process record，不加 step 檔；一個 skill 一個 commit：add-tags `1b6036a`、add-tags-note `4215e77`、del-tags `cbc9902`、write-note `0e1e39d`、write-note-new-files `cfacd8a`、write-note-tags `af9d39c`、ask-note `beb3396`、check-wiki-doc `bf3abcb`、chinese `935974a`。
- check-wiki-doc 順便把設定名稱 `wikiRootDir` 改成 `wikiDir`，範圍是 SKILL.md、兩份 references 與 `build_dependency_graph.py` 的說明文字。
- chinese 的「不寫 YAML checkpoint」三處改成「不寫 step 檔」。
- `skill-groups/common/skills/` 下 22 個 SKILL.md 都提到 process record；chinese 的 parity check 是 0 failure。

### 留給使用者決定的

- Run Number 照範本在 Step 0 的最後取得，所以在 Step 0 中途就停下的 run（缺少輸入、找不到檔案）沒有 process record；要記下這種 run，範本與每個 skill 都要把它移到 Step 0 的最前面。
- check-wiki-doc 的步驟 5 在使用者同意之後才做，排在寫 `result: completed` 的步驟 4 之後；它加進同一份 process record，`result` 不變。
- chinese 的 `run step N` 不跑 Step 0，但仍先取得 Run Number、寫出 process record。

### 2026-11-06 要改的 skill

- add-tags、add-tags-note、ask-note、check-wiki-doc、chinese、del-tags、write-note、write-note-new-files、write-note-tags。
- 只有 chinese 有 SKILL-tw.md；這 9 個都沒有 README.md。

## 4. 要做的

1. 每個 skill 照 [SKILL-tmp.md](../skill-groups/common/templates/SKILL-tmp.md) 的寫法加上：
   - TERMINOLOGY 的 Run Number 與 Process record；CONFIGURATION 的 process record 路徑；
   - MUST FOLLOW 連到 run-data-rules.md，停止前顯示 process record 的路徑；
   - Step 0 取得 Run Number 並寫出 process record；每一步把自己加進 process record；最後一步寫 `result: completed`。
2. 有中文版的同時改中文版，跑 `check_parity.py`。
3. 一個 skill 一個 commit；在 CHANGES.md 加一筆。

## 5. 驗證

- `skill-groups/common/skills/` 下每個 SKILL.md 都提到 process record。
- chinese 的 parity check 是 0 failure。

## 6. 與其他 task 的關係

- [[Task 100]]：本 task 的上層。
- [[Task 100.4]]：先改的 13 個 skill，做法照它們。
- [[Task 100.5]]：檢查 Task 100 是否完成，包括本 task。

## 7. 知識

—

## 8. 日誌

### 2026-11-06

- 做完：9 個 skill 補上 process record。
- 提出。
