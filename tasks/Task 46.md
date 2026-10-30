# Task 46 - 把 RSDC 的 Terms 改名為 Terminology

**Status**：完成——2026-10-16 建立，同日在建立它的 session 做完：RSDC 第 2 章的 Terms 改名為 Terminology，RSDC-Standard 換成 261016。
**Raised**：2026-10-16，[[Task 32]] 審 tw-keep-english 的草稿（2.3）第 1 項 `[?]`（glossary 定義的 term 保留英文）時，使用者問 RSDC 的 Terms 與 skill 的 TERMINOLOGY 要不要統一；比較兩個方向之後，決定把 RSDC 的 Terms 改為 Terminology。
**Depends on**：—

## 1. 背景

RSDC 第 2 章的第一項叫 Terms，寫出後面各項會用到的名詞；skill 的 SKILL.md 則在 `# TERMINOLOGY` 與 `# DEDICATED TERMINOLOGY` 底下定義名詞。
兩者都是 glossary，chinese skill 兩種名稱都認得，但名稱不一致。
反過來把 skill 的 TERMINOLOGY 改成 TERMS，要改三個 repo 共 46 份 SKILL.md 與三支工具；改 RSDC 的 Terms 只牽涉一份標準、它的兩份範本、兩份 RSDC 與兩支工具。

## 2. 現況

### 已決定（2026-10-16）

- RSDC 第 2 章的 Terms 改名為 Terminology：RSDC-Standard 的規則、兩份 RSDC 範本的「2.1 Terms」標題，以及已經有這一節的 InvCov-RSDC 與 StopPriceChecker-RSDC。
- 節名是 RSDC 必須遵守的形狀，改名算改規則：RSDC-Standard 換成 261016，「This version replaces」改成 261010，「Changes in This Version」最上方新增 261016 的小節；兩份範本第 12 行記的標準版本跟著換。
- 工具只認新名稱 Terminology：`check_rsdc.py` 找 RSDC 定義的名詞、chinese skill 的 `scan_md.py` 認 glossary，都改成 Terminology。
- 「Changes in This Version」裡過去版本的紀錄照舊，那是當時的名稱。
- 中文版照英文改成 Terminology，節名保留英文。
- [[Task 32]] 2.3 的第 1 項（草稿第 38 行的措辭）另外處理，不在本 task。
- 提交：commit 前綴 `task 46`，兩個 repo 各一個；InvestForge 只提交標題與檔頭紀錄那幾行。

### 結果（2026-10-16）

- RSDC-Standard 與中文版：header 的 Version 換成 261016，上一版寫成 261010；現行規則的 4 處改成 Terminology；Technical words 加上 terminology，共 125 個；「Changes in This Version」最上方新增 261016 的小節，說明改名的原因、跟著改的工具，以及規則沒變。
- 兩份範本與中文版：「## 2.1 Terminology」，第 12 行改記標準的 261016；範本自己的版本仍是 261016。
- InvestForge：InvCov-RSDC、StopPriceChecker-RSDC 與中文版的標題改成「## 2.1 Terminology」。
- `check_rsdc.py` 只認 Terminology；chinese 的 `scan_md.py` 改用 `TERMINOLOGY_HEADING_RE`，SKILL.md 與中文版的兩處跟著改；ste-rules.md 的例子改成 `**Terminology**:`。
- 重記：記錄 RSDC-Standard 的 8 份、記錄兩份範本的 InvestForge 4 份、記錄 chinese SKILL.md 的 6 份 README、記錄 ste-rules.md 的 asd-ste SKILL.md 與中文版。

### 涉及的檔案

- RSDC-Standard.md 與中文版：header 的 Version、第 22 行的上一版、現行規則提到 Terms 的第 93、96、98、168 行，以及新的 261016 小節。
- RSDC-App-tmp.md、RSDC-Skill-System-tmp.md 與中文版：「## 2.1 Terms」與第 12 行的標準版本。
- InvestForge：InvCov-RSDC.md、StopPriceChecker-RSDC.md 與中文版的「## 2.1 Terms」。
- `check_rsdc.py` 第 741、745、881 行；chinese 的 `scan_md.py` 第 26、27、70 行，SKILL.md 第 29、309 行與中文版。
- asd-ste 的 ste-rules.md：House Rule 9 拿 RSDC-Standard 的 `**Terms**:` 當粗體標籤的例子。
- 不改：mods/mermaid-view/MermaidView-RSDC.md 第 100 行的粗體標籤「**Terms**」（舊格式，不是節標題，工具不讀；中文版譯成「術語」），以及 skill 的「Terms that mean the same thing in every skill」等一般用法。

## 3. 要做的

1. 改 RSDC-Standard 與中文版，換版本，新增 261016 的小節；`check_ste.py --ste` 重新檢查。
2. 改兩份範本與中文版、InvestForge 兩份 RSDC 與中文版。
3. 改 `check_rsdc.py`、`scan_md.py`、chinese 的 SKILL.md 與中文版、ste-rules.md。
4. 重記：記錄 RSDC-Standard、兩份範本、chinese SKILL.md、ste-rules.md 的文件，讀過改動後重記。

## 4. 驗證

- RSDC-Standard 的 `check_ste.py --ste` PASS。
- 兩份範本的 `check_rsdc.py --standard` PASS；InvCov 與 StopPriceChecker 的 `--rsdc` 與中英對照都 PASS，Terminology 定義的名詞照樣被檢查。
- chinese 的 `scan_md.py` 把 RSDC 的 Terminology 一節認成 glossary。
- 改到的中英對照 `check_parity.py` 0 failure，`diff_md.py --verify` PASS；重記的文件 `depends_on.py check` 都是 UNCHANGED。

## 5. 與其他 task 的關係

- [[Task 32]]：審 2.3 時提出；2.3 的第 1 項另外處理。
- [[Task 45]]：版本寫在 header quote 的第一行，本 task 換版本時改的就是那一行。

## 6. 日誌

### 2026-10-16

- 建立：決定把 RSDC 的 Terms 改名為 Terminology，換成 261016，工具只認新名稱。
- 做完：RSDC-Standard 的 `check_ste.py --ste` PASS，只有原本的 4 個被動句警告；兩份範本的 `check_rsdc.py --standard` 都是 8 項 PASS，記的標準版本是 261016。
  InvCov 與 StopPriceChecker 的 `check_rsdc.py --rsdc` 與中英對照都 PASS，「Terminology 定義的名詞在中文版都有用到」照樣在檢查；chinese 的 `scan_md.py` 在 InvCov-RSDC 的 Terminology 一節讀到 8 個 glossary term。
  改到的中英對照 `check_parity.py` 都是 0 failure、警告和之前相同，`diff_md.py --verify` 都 PASS；重記的 20 份 `depends_on.py check` 都是 UNCHANGED。
