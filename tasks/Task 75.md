# Task 75 - 讓 check_rsdc.py 與 depends_on.py 分辨範例引用

**Status**：尚未開始——gen-rsdc-skill 的範例引用仍被當成對 SkillCompiler-RSDC 的引用，`--skill` 檢查有一項 FAIL。
**Raised**：2026-10-20，[[Task 18.2]] 對齊 SkillCompiler-RSDC 之後，gen-rsdc-skill 的 `check_rsdc.py --skill` 仍有一項 FAIL；使用者決定記為已知誤判，另開 task 處理。
**Depends on**：—

## 1. 背景

gen-rsdc-skill 的 [SKILL.md](../.github/common/skills/gen-rsdc-skill/SKILL.md) 只有第 260 行真的引用 SkillCompiler-RSDC（§2.3 *Dataflow*）。
第 587 行與第 599 行的 §2.7 *Presentation Contract*、§2.6 *The Verdict* 與 §2.6 *Derivation Rules*，是在教 target skill 怎麼引用它自己的 RSDC，是範例。
兩支程式都把它們當成對 SkillCompiler-RSDC 的引用：

- [check_rsdc.py](../.github/common/skills/gen-rsdc-skill/scripts/check_rsdc.py) 的 `--skill` 檢查，把 SKILL.md 裡的每一個 § 引用都對照到 `--rsdc` 指定的 RSDC。
- [depends_on.py](../.github/common/scripts/depends_on.py) 的 `cited` 依節名對照，所以 gen-rsdc-skill 記下的指紋也涵蓋 SkillCompiler-RSDC 的 Derivation Rules 與 Presentation Contract；這兩節一改，gen-rsdc-skill 就被判為 CHANGED。

## 2. 現況

### 2026-10-20 查的結果

- `check_rsdc.py --rsdc SkillCompiler-RSDC.md --skill gen-rsdc-skill/SKILL.md` 判 FAIL，9 項通過、1 項失敗：第 587、599 行的 4 個範例引用，節名和 SkillCompiler-RSDC 那一節的節名不同。
- 第 260 行的 §2.3 *Dataflow* 通過，[[Task 18.2]] 確認仍成立後重記了指紋。
- gen-rsdc-skill 與 check-md-deps 都沒有 README.md。
- compile-skill 的 `--skill` 也判 FAIL，6 項通過、1 項失敗：the skill links to SkillCompiler-RSDC.md。
  原因和範例引用不同：[[Task 77]] 讓 compile-skill 的 SKILL.md 只讀 SKILL-Compile.md、不連到 RSDC，RSDC 的指紋改記在它的 README.md；`--skill` 預設 skill 會連到它的 RSDC，這個前提對 compile-skill 不成立。

## 3. 要做的

1. 決定怎麼讓程式認出範例引用，例如範例的那一行不算，或範例用不同的寫法。
2. 照決定改 `check_rsdc.py` 與 `depends_on.py`；兩支都改的話，`cited` 的說明（docstring 與 check-md-deps 的 SKILL.md）跟著改。
3. 若改的是範例的寫法，gen-rsdc-skill 的 SKILL.md 與中文版照 [chinese](../.github/common/skills/chinese/SKILL.md) skill 一起改。

## 4. 驗證

- `check_rsdc.py --rsdc SkillCompiler-RSDC.md --skill gen-rsdc-skill/SKILL.md` PASS。
- gen-rsdc-skill 記下的 `[[SkillCompiler-RSDC]]` 指紋只涵蓋 §2.3 Dataflow：改 SkillCompiler-RSDC 的其他節，它仍是 UNCHANGED。
- 引用 RSDC 的其他 SKILL.md，`--skill` 的結果和改之前一樣。

## 5. 與其他 task 的關係

- [[Task 18.2]]：對齊 SkillCompiler-RSDC 之後發現這項 FAIL，記為已知誤判。
- [[Task 18]]：它的「驗證」要求引用 RSDC 的每一份 SKILL.md 都 PASS，gen-rsdc-skill 這一項要等本 task。
- [[Task 77]]：compile-skill 的 SKILL.md 不再連到 SkillCompiler-RSDC，`--skill` 因此判 FAIL。

## 6. 日誌

### 2026-10-20

- 提出：[[Task 18.2]] 之後 gen-rsdc-skill 的 `--skill` 仍有一項 FAIL，原因是範例引用。
- 「2026-10-20 查的結果」記下 compile-skill 的 `--skill` FAIL：SKILL.md 不再連到 RSDC（[[Task 77]]）。
