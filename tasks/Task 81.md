# Task 81 - 術語表：Agency、Gestalt 與 Forge

**Status**：完成——2026-10-30 寫好 [glossary.md](../.github/common/references/glossary.md) 與中文版；workspace 保留，定義成 agency 的 repository 根目錄；README 與中文版加上一節；agency、Forge、Gestalt 加進 keep-English list。
**Raised**：2026-10-30，使用者討論 SkillsGestalt 與 InvestForge 的架構，定下名稱之後，要寫進術語表，先建立本 task。
**Depends on**：—

## 1. 背景

SkillsGestalt 與 InvestForge 各有許多 skills 與 agents，共同完成工作；兩邊都有自己的 wiki，也都有自己的 tasks 與 chores。
InvestForge 透過 `config.yaml` 的 `skillGroups.common` 使用 SkillsGestalt 的共用 skills、rules、templates 與 scripts，另有自己的 `dedi`。
文件現在把兩者都叫 workspace，但這個字和 VS Code 的 workspace 撞名：`InvestForge.code-workspace` 把 SkillsGestalt 也掛成其中一個資料夾。

## 2. 現況

- 名稱已定（2026-10-30）：
  - **Agency**：一個 repo 加上它自己的 wiki，裡面的 skills 與 agents 共同完成工作；SkillsGestalt 與 InvestForge 都是一個 agency。
    Agency 是一種類別，不是整個組織。
  - **Gestalt**：主題是 skill 本身的 agency，提供 `common` skill group，規定每個 skill 的形態；SkillsGestalt 是它，只有一個。
  - **Forge**：主題是一個領域的 agency，使用 `common`，加上自己的 `dedi`；InvestForge 是它，之後的領域也叫 XxxForge。
  - repo 名稱就是「主題 + 角色」：Skills + Gestalt、Invest + Forge。
- 名稱的由來：討論過 workspace、studio、crew、guild、聖堂（Sanctum）；Gestalt（完形）指整體大於部分之和，也指一個東西的完整形態，比只保存規則的聖堂貼切，也直接用了已有的 repo 名稱。
- 術語表是 [glossary.md](../.github/common/references/glossary.md) 與 [glossary-tw.md](../.github/common/references/glossary-tw.md)，分兩節：Agencies（agency、Gestalt、Forge）與 Parts of an Agency（workspace、wiki、knowledge-base root、skill group、agent、task、chore）。
- [README.md](../README.md) 與中文版在 What Is Here 前加上 Gestalt and Forge 一節，連到術語表。
- [tw-keep-english.md](../.github/common/references/tw-keep-english.md) 與中文版加上 agency、Forge、Gestalt，版本從 261018 換成 261030。

## 3. 要做的

### 已決定（2026-10-30）

- 術語表以英文 ASD-STE100 寫，過 `check_ste.py`，另有 `-tw.md` 中文版。
- 中文的稱呼：agency、Gestalt、Forge 都保留英文，加進 keep-English list；Gestalt 在說明德文意思的句子裡註明「完形」。
  建立 task 時原本說 Forge 可以寫「工坊」，開始做時使用者改成三個都保留英文。
- 術語表要收的名稱：
  - Agency、Gestalt、Forge，以及 Gestalt 只有一個、Forge 可以有很多。
  - wiki（每個 agency 的 Obsidian vault，`config.yaml` 的 `wikiDir`）與 knowledge-base root（裝著所有 wiki 的 `Documents`，`wikiRootDir`）。
  - skill group：`common`、`dedi`、`external`，即 `config.yaml` 的 `skillGroups`。
  - agent：在 agency 裡使用 skills 做事的 agent。
  - task 與 chore：每個 agency 都有的待辦與例行工作。

### 開始做時決定的（2026-10-30）

- 術語表放在 `.github/common/references/glossary.md`，和 DFD、RSDC-Standard 一樣是參考文件；每個 Forge 透過 `{skillGroups.common}` 讀得到。
- 文件裡的 workspace（147 個檔、571 處）保留不換：術語表把它定義成 agency 的 repository 根目錄，agency 則是 workspace 加上 wiki 與 agents。
- README 與中文版加一節，連到術語表；根目錄的 CLAUDE.md 不改。
- 每個術語寫成粗體加定義的清單，和 skill 的 TERMINOLOGY 一樣；以 SkillsGestalt 與 InvestForge 當例子；不畫關係圖。

## 4. 驗證

- 術語表的英文版 `check_ste.py` 是 PASS，與中文版的 `check_parity.py` 是 0 failure。
- 術語表說明的 `wikiDir`、`wikiRootDir`、`skillGroups` 和兩邊 `config.yaml` 的現況一致。
- 改了哪些文件，就照它們各自的規則檢查。

2026-10-30 的結果：

- `glossary.md` 與 `tw-keep-english.md` 的 `check_ste.py` 都是 PASS；`depends_on.py record` 記下 glossary.md 的 header quote。
- `check_parity.py` 對 glossary、tw-keep-english 與 README 三組都是 0 failure。
- `reformat_md.py --mode clean` 不改動任何一個檔。

## 5. 與其他 task 的關係

- [[Task 80]]：討論起於比較兩邊 CLAUDE.md 的 Tasks 與 Chores 兩節。
- InvestForge 的文件若要改，在 InvestForge 自己的 tasks 開 task，不在本 task 改。
- [[keep-english]]：keep-English list 換成 261030 版，下一次 keep-English 稽核該做了。

## 6. 知識

—

## 7. 日誌

### 2026-10-30

- 建立 task：名稱定為 Agency、Gestalt 與 Forge（Agency 是類別）；術語表的語言與要收的名稱已定，位置與是否取代 workspace 還沒決定。
- 開始做：術語表放在 references，workspace 保留並定義成 agency 的 repository 根目錄；寫好術語表與中文版、README 的一節，keep-English list 加上三個 term；本 task 完成，[[keep-english]] 該做了。
- [[Task 86]] 把 chore 改用名稱：本檔的 `[[Chore N]]` 連結改成新名稱。
