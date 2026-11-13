# Task 100.1 - 把很少用的 skill 搬到 skill-groups/archived

**Status**：完成——6 個 skill 搬到 `skill-groups/archived/skills/`，report-my-chats 的空殼移到垃圾桶，發佈時排除 `skill-groups/archived/`。
**Raised**：2026-11-06，[[Task 100]] 盤點很少用的 skill，使用者決定封存其中 7 個，搬過去的 skill 不能執行，只是保存。
**Depends on**：—

## 1. 背景

- [[Task 100]] 的表 3 列出封存的決定與證據：`database\skill-tokens` 的執行紀錄、兩個 vault 的報告資料夾，以及別的 skill 有沒有用它。
- 封存的 skill 不必跟著 [[Task 100]] 改成新的 checkpoint 與 `handoff` 做法。

## 2. 結論

—

## 3. 過程

### 2026-11-06 改好之後

- **搬到 `skill-groups/archived/skills/`**：report-logs、report-week、report-skills、notify-week、synch-two-mds 從 `common` 搬過來，eli5 從 `external` 搬過來。
- **report-my-chats**：只剩 git 不追蹤的 `scripts\__pycache__\`，沒有 SKILL.md，移到垃圾桶，不搬。
- **`skill-groups/archived/README.md`**：說明這裡的 skill 不在 `skillGroups` 裡，不能執行；要再用時搬回 skill group，再跑 check-skill。
- **`skill-groups/external/README.md`**：eli5 搬走之後 `external` 沒有 skill，`skillGroups.external` 照舊保留；這個檔說明它的用途，也讓 git 留著這個目錄。
- **發佈**：[publish_snapshot.py](../skill-groups/common/scripts/publish_snapshot.py) 的 `EXCLUDED` 與 `PRIVATE_PATH` 加上 `skill-groups/archived`；[publish-gestalt](../chores/publish-gestalt.md) 的三處跟著改。
- **compile-skill 的例子**：[SKILL.md](../skill-groups/common/skills/compile-skill/SKILL.md) 與中文版的 report-skills 換成 chinese，report-logs 換成 reformat-md。
- **eli5 的例子**：[glossary.md](../skill-groups/common/references/glossary.md) 與中文版、[config.example.yaml](../config-tmp.yaml) 拿掉「例如 eli5」。
- **CHANGES.md** 加一筆，讓 Forge 跟上。

### 已決定（2026-11-06）

使用者回答了 8 個問題：

1. **封存哪些**：report-skills、report-logs、report-week、notify-week、synch-two-mds、eli5、report-my-chats。
2. **note 與 tag 一族、write-topic、check-wiki-doc 不封存**。
3. **怎麼進行**：開本 task，當場做。
4. **add-tags 與 del-tags 的 Step 2 先不動**：vault 裡舊的 report-logs 報告還在，Step 2 仍改得到。
5. **結構**：`skill-groups/archived/skills/<name>/`。
6. **`skillGroups.external` 保留**。
7. **`skill-groups/archived/` 整個不發佈**：eli5 的原作者與授權不明。
8. **compile-skill 的例子換成 chinese 與 reformat-md**；report-my-chats 移到垃圾桶。

## 4. 要做的

—

## 5. 驗證

- `skill-groups/common/skills/` 剩 22 個 skill，`skill-groups/archived/skills/` 有 6 個。
- `git grep` 在 `skill-groups/common` 找不到這 6 個 skill 的名稱，只剩 add-tags 與 del-tags 提到的 `{wikiDir}\report-logs\` 報告路徑。
- `check_parity.py`：compile-skill 的 SKILL.md、glossary.md 各和中文版比對。

## 6. 與其他 task 的關係

- [[Task 100]]：本 task 的上層；封存的決定寫在它的表 3。
- [[Task 78]]：定下發佈時排除 `skill-groups/external/`。
- [[Task 97]]：Copilot 找 skill 的位置；InvestForge 的 workspace 檔仍列著 `skill-groups/external/skills`，經 CHANGES.md 處理。

## 7. 知識

—

## 8. 日誌

### 2026-11-06

- [[Task 100]] 的表格重新編號，封存的決定從表 5 改為表 3，本檔的兩處引用跟著改。
- 提出並完成：6 個 skill 搬到 `skill-groups/archived/skills/`，report-my-chats 移到垃圾桶。
