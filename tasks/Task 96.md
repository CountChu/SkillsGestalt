# Task 96 - Forge 必須有 .venv，skill 以 .venv 的 Python 執行 script

**Status**：完成——forge-setup.md 多了建立 `.venv` 的一步，SKILL-tmp.md 與 asd-ste 的 Step 0 要求 `.venv`，指令改用 `{python}`；其他 skill 的 Step 0 還沒跟上。
**Raised**：2026-11-02，check-skill 對 asd-ste 報 5.1：指令寫 `python`，在沒有 `.venv` 的 macOS 上找不到；使用者決定要求每個 Forge 都有 `.venv`。
**Depends on**：—

## 1. 背景

skill 的指令寫 `python …`，但 macOS 內建的 Python 只有 `python3`，Windows 則常常只有 `python`。
[[Task 95]] 讓 SkillsGestalt 有了自己的 `.venv`，但 SKILL.md 沒有要求 `.venv`，check-skill 仍報 5.1。
另外，agent 的每個指令都在新的 shell 裡執行，前一個指令 activate 的 `.venv` 不會留下來；所以只寫「Run `.venv` first」，照字面跑 `python` 仍會失敗。

## 2. 現況

### 2026-11-02 改好之後

- **forge-setup.md 與中文版**：「Make a Forge」多了第 3 步，在根目錄建 `.venv`、安裝 `{skillGroups.common}/requirements.txt`、把 `.venv/` 加進 `.gitignore`；原本的第 3 到 7 步變成第 4 到 8 步，引用步驟編號的地方跟著改。
  第 5 步的指令改用 `{python}`；「Change an Older Workspace」要做第 3 步，以及第 5 到 8 步。
- **requirements.txt**：從 SkillsGestalt 的 root 搬到 `.github/common/requirements.txt`，Forge 透過 skill group 拿得到。
- **SKILL-tmp.md 與中文版**：Step 0 的第一項改成找出 `{python}`，也就是 `.venv` 的 Python；後面每個 script 都以它執行；沒有 `.venv` 就停下，請使用者照 forge-setup.md 第 3 步建立。
  範例指令改用 `{python}`。
- **asd-ste 的 SKILL.md 與中文版**：Step 0 照範本改，18 個 `python {skillGroups…}` 指令都改成 `{python} {skillGroups…}`。
- 引用 SKILL-tmp.md 的 asd-ste、check-skill、compile-skill 與 gen-skill 的 README 與中文版，讀過之後重記指紋；gen-skill 只替換大寫的 placeholder，`{python}` 是執行時代入的值，不受影響。
- CHANGES.md 加一筆。

## 3. 要做的

### 已決定（2026-11-02）

使用者回答了 7 個問題，都照建議，只有最後一個例外：

1. **套件清單放在 `.github/common/requirements.txt`**。
2. **沒有 `.venv` 時停下**，說明照 forge-setup.md 第 3 步建立。
3. **Step 0 解析出 `{python}`**，指令寫 `{python}`，不靠 activate 留在 shell 裡。
4. **只改範本與 asd-ste**：其他 skill 之後再跟上。
5. **root 的 requirements.txt 搬到 `.github/common/`**，不留副本。
6. **InvestForge 只靠 CHANGES.md**，照 follow-gestalt 自己做。
7. **開好 task 就做**。

### 後續

- 其他 skill 的 Step 0 仍寫「Run `.venv` first」，指令仍寫 `python`；check-skill 只比對章節，不會報出這個差異。
- CLAUDE-tmp.md 給的 `gen_claude_md.py`、`check_tasks.py` 與 `check_chores.py` 指令也寫 `python`。

## 4. 驗證

- `check_ste.py --ste`，加上 `--custom` 與 `--spelling`：forge-setup.md 與 SKILL-tmp.md 都 PASS。
- `check_parity.py`：forge-setup、SKILL-tmp 與 asd-ste 的 SKILL.md 各和中文版比對，0 failure。
- `depends_on.py check`：引用 SKILL-tmp.md 的 8 份 README 重記之後都 UNCHANGED；只剩 check-md-deps 兩項舊的 CHANGED。
- `.venv/bin/python -m pip install -r .github/common/requirements.txt` 沒有要裝的新套件。

## 5. 與其他 task 的關係

- [[Task 95]]：建了 SkillsGestalt 的 `.venv` 與 requirements.txt；本 task 把 requirements.txt 搬到 `common`。
- [[Task 88]]：forge-setup.md 是它寫的接上 SkillsGestalt 的指南。

## 6. 知識

—

## 7. 日誌

### 2026-11-02

- 提出並完成：Forge 必須有 `.venv`，範本與 asd-ste 以 `{python}` 執行 script。
