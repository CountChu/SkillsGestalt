# Task 74 - 修正 compile-skill 兩支 script 的三個缺陷

**Status**：尚未開始——SkillCompiler-RSDC 的 4.5 Defects 列出的三個缺陷，程式都還沒改。
**Raised**：2026-10-20，[[Task 18.2]] 對齊 SkillCompiler-RSDC 時讀程式碼看到三處和文件不一致；使用者決定列進 4.5 Defects，另開 task 改程式。
**Depends on**：—

## 1. 背景

[SkillCompiler-RSDC.md](../.github/common/skills/compile-skill/references/SkillCompiler-RSDC.md) 的 4.5 Defects 列出程式做了第 2 章說不該做的事的地方。
這三處都是讀程式碼時看到的，還沒在執行中觀察到。
本 task 改 [scan_source.py](../.github/common/skills/compile-skill/scripts/scan_source.py) 與 [check_compiled.py](../.github/common/skills/compile-skill/scripts/check_compiled.py)，改好之後把缺陷從 4.5 拿掉。

## 2. 現況

### 2026-10-20 讀程式碼看到的

- **Source Scanner 讀取 Skill Source 兩次**：`scan()` 先以 `read_text()` 讀取要判定的文字，再由 `source_fingerprint()` 重新讀取檔案算 fingerprint。
  兩次讀取之間若有變更，fingerprint 就屬於另一份來源，違反 2.5 Source Fingerprint；3.2 的 Source Scanner 第 1 步也寫「讀取一次」。
- **Contract Checker 不檢查 stale 執行寫了什麼**：它先確認執行處仍是空的，之後才在同一處執行 stale 副本兩次，所以那兩次有沒有寫檔沒被檢查到。
  2.3 規定 refusal 什麼都不寫；4.4 Verification Obligations 的「Introspection and refusals write nothing」那一列，已寫明 stale 的兩次不在檢查之內。
- **無法解析的 stale script 被回報成檢查失敗**：它先解析 script，才讀記錄的 fingerprint；script 無法解析時以 `1` 結束。
  照 2.7 CLI，stale 的 script 要以 `4` 結束、其他都不檢查，因為 stale 的 script 要重新編譯，而不是修正。

## 3. 要做的

1. 照 [skills/CLAUDE.md](../.github/common/skills/CLAUDE.md) 先讀 [skill-writing.md](../.github/common/rules/skill-writing.md)；compile-skill 沒有 README.md。
2. 每個缺陷先做出能重現它的執行，再改程式。
3. 改好一個，就把它從 4.5 Defects 拿掉；4.4 那一列的 Proven by 跟著改，中文版照 [chinese](../.github/common/skills/chinese/SKILL.md) skill 更新。

## 4. 驗證

- 三個缺陷改之前都能重現，改之後都不再發生。
- `check_rsdc.py --rsdc` 單獨檢查與中英對照都 PASS；compile-skill 的 SKILL.md 與 gen-rsdc-skill 的 SKILL.md 記下的 `[[SkillCompiler-RSDC]]` 指紋若變了，讀過之後重記。
- `scan_source.py` 與 `check_compiled.py` 對同一份 Skill Source 的 fingerprint 仍然一致。

## 5. 與其他 task 的關係

- [[Task 18.2]]：對齊 SkillCompiler-RSDC 時發現這三處，寫進 4.5 Defects。

## 6. 知識

—

## 7. 日誌

### 2026-10-20

- 提出：[[Task 18.2]] 讀程式碼時看到三處和文件不一致，使用者決定另開 task 改程式。
