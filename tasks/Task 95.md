# Task 95 - SkillsGestalt 的 .venv，以及修正 check-skill 對 asd-ste 報的 5.1 與 6.1

**Status**：完成——SkillsGestalt 有了自己的 `.venv` 與 requirements.txt；asd-ste 的 Step 0 寫明 `rg` 是 ripgrep，Dataflow 補上三條讀取的箭頭。
**Raised**：2026-11-02，[[Task 41.1]] 改完 asd-ste 之後跑 check-skill，使用者點名修 5.1 與 6.1，並要求 SkillsGestalt 要有自己的 `.venv`。
**Depends on**：—

## 1. 背景

2026-11-02 以 check-skill 的 6 項 check 檢查 asd-ste，得到 4 個 issue 與 1 個 recommendation。
使用者點名修 1.1、3.1、5.1 與 6.1：1.1 與 3.1 是 description 的問題，記在 [[Task 93]]；5.1 與 6.1 記在本 task。
沒點名的 5.2 是：指令寫 `python`，但這台 Mac 沒有 `.venv` 時只有 `python3`。
使用者要 SkillsGestalt 建自己的 `.venv`，不改 SKILL.md。

## 2. 結論

—

## 3. 過程

### 2026-11-02 改好之後

- **`.venv`**：在 root，照 InvestForge 的 `.venv` 以 Homebrew 的 python@3.10 建，Python 3.10.21，prompt 是 `Gestalt`；`.gitignore` 原本就排除它。
- **requirements.txt**：在 root，是 `pip freeze` 的結果，照 InvestForge 用 `==` 釘版本；裝了 PyYAML、pypdf 與 cryptography，後兩個給 `convert_spec.py` 重建 STE 字典時用。
  在別台機器以 `python3.10 -m venv .venv --prompt Gestalt`，再 `.venv/bin/python -m pip install -r requirements.txt` 建。
- **5.1**：asd-ste 的 SKILL.md 與 SKILL-tw.md 在 Step 0 的 `rg` 指令下加一句：`rg` 是 ripgrep，沒有它時改用 agent 的檔案搜尋工具，並包含隱藏目錄。
- **6.1**：asd-ste 的 README.md 與 README-tw.md 的 Dataflow 加上 `INVT --> S2`、`CUSTOM --> S6`、`CONFIG --> S3` 三條黑色箭頭，加在最後，`linkStyle` 的編號不變。
- Skills Dashboard 的 asd-ste 列標記為要重查。

## 4. 要做的

### 已決定（2026-11-02）

使用者回答了 9 個問題：

1. **`.venv` 和 InvestForge 的一樣**：Homebrew 的 python@3.10。
2. **套件**：PyYAML、pypdf 與 cryptography。
3. **requirements.txt 放在 root**，照 InvestForge 用 `==` 釘版本。
4. **prompt 是 `Gestalt`**。
5. **5.2 不修**：SkillsGestalt 有了 `.venv`，就不會遇到。
6. **SKILL-tw.md 的 description 照 chinese skill 翻譯新的 description**。
7. **開新 task**，1.1 與 3.1 記在 [[Task 93]]，兩邊各一個 commit。

## 5. 驗證

- `check_parity.py`：SKILL.md 與 README.md 各和中文版比對，0 failure；警告都是改之前就有的。
- `depends_on.py check` 查 asd-ste 的 README.md：9 項都 UNCHANGED。
- `.venv/bin/python --version` 是 3.10.21，`pip freeze` 和 requirements.txt 相同。
- 沒有重跑 check-skill；Skills Dashboard 的 asd-ste 列標記為要重查。

## 6. 與其他 task 的關係

- [[Task 93]]：同一次 check-skill 的 1.1 與 3.1，改 asd-ste 的 description。
- [[Task 41.1]]：改完 asd-ste 之後跑了這次 check-skill。

## 7. 知識

### 適合寫成新 topic

—

### 適合併進現有 topic

—

### 不算知識

- **這台 Mac 沒有 `python`，只有 `python3`**：skill 的指令照 SKILL-tmp 寫 `python`，要靠 `.venv` 才能照字面跑。

## 8. 日誌

### 2026-11-02

- [[Task 96]] 把 requirements.txt 從 root 搬到 `.github/common/requirements.txt`。
- 提出並完成：建 `.venv` 與 requirements.txt，修 asd-ste 的 5.1 與 6.1。
