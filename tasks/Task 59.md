# Task 59 - 把 app 加進 tw-keep-english，imp-home 中文版的「應用」改成 app

**Status**：完成——2026-10-18 tw-keep-english 加上 app 一列，版本改成 261018；imp-home 三份中文版的 37 處「應用」改好。
**Raised**：2026-10-18，[[Task 58]] 翻 md-style 的中文版時，發現 app 不在 keep-English list 上，但大多數 twin 都保留英文；使用者決定把它加進清單。
**Depends on**：—

## 1. 背景

chinese skill 規定，清單沒有的詞若在 twin 裡保留英文，要在同一個 step 加進 [tw-keep-english.md](../.github/common/references/tw-keep-english.md)。
app 在大多數 twin 裡都保留英文，卻不在清單上。
imp-home 的三份中文版把 app 寫成「應用」，所以 twin 已用了兩種譯法。
compile-skill 的 Tasks-tw.md 有 2 處「應用程式」，翻的是英文的 application，不算 app 的譯法。

## 2. 現況

### 決定

- **新的一列**放在 agent 與 automated 之間：`| app | 應用, 應用程式 | — | It is the name of a type in the system, and twins use two renderings for it: 應用, and the English word app. |`。
  Replaces 列出 imp-home 用過的「應用」，以及譯者最容易寫出的「應用程式」。
  Flagged 寫「—」：「應用」也是一般用詞，「應用程式」又是 application 的正確譯法，Tasks-tw.md 就用了兩次，標哪一個都會誤報。
  Why 寫兩個理由：系統裡有 imp-app、gen-rsdc-app、RSDC-App-tmp 與 `appDir`，寫成中文就對不上這些名稱；而且 twin 已用了兩種譯法。
- **清單改了，所以版本從 261016 改成 261018**，照清單自己的規則。
- **imp-home 的 37 處在這個 task 一起改**，照 [[Task 48]] 的前例。
  每一處都先對照英文：SKILL-tw.md 的 35 處與 Home-RSDC-tw.md 的 1 處指的都是 app，改成 app。
  Wireframe-tw.md 第 46 行的英文是「and one the hub serves itself」，one 指的是前面的 link，所以照英文改譯成「連結」，不改成 app。
- **更正 [[Task 58]]**：它的順帶發現把 Tasks-tw.md 的「應用程式」當成 app 的譯法；改成正確的事實，並連到這個 task。

### 進度

- tw-keep-english.md 第 67 行加上 app 一列，Version 改成 261018；`check_ste.py --ste` PASS，只有改之前就有的 op 警告。
  `[[ASD-STE100_ISSUE9.pdf]]` 重記，日期從 2026-10-16 改成 2026-10-18，指紋不變；`[[ste-custom]]` 不動。
- 中文版照 chinese skill 只改 change set 的 3 行：Version、`[[ASD-STE100_ISSUE9.pdf]]` 兩行照抄，新的一列翻譯 Why 欄，寫法照 repository 與 script 兩列。
  同一天 [[Task 32.8]] 的 session 也在改這兩份的 Technical words 那一行，還沒提交，所以 change set 在 `git clone --shared` 的暫存副本裡算，副本裡 `check_parity.py` 0 failure，`diff_md.py --verify` PASS。
  提交時只 stage 以 HEAD 加上這 3 行做成的 blob，那一行留給它自己提交。
- 37 份中文版在新舊清單下的 `check_parity.py` 結果完全相同：Flagged 寫「—」，所以這一列不會多出警告。
  scan_md.py 讀得到新的一列，例如 Home-RSDC.md 的 app 有 70 處。
- imp-home：SKILL-tw.md 改了 26 行、35 處，Home-RSDC-tw.md 改了第 5 行，Wireframe-tw.md 改了第 46 行；三份都不再有「應用」。
  三對的 `check_parity.py` 都是 0 failure，警告和改之前相同；Home-RSDC 的 `check_rsdc.py` 結果也和改之前相同。
  imp-home 沒有 README，沒有文件在檔頭記錄 tw-keep-english.md。

### 順帶發現

- Home-RSDC 的 `check_rsdc.py` 在 HEAD 就有一項 FAIL：fenced blocks are byte-identical。
  這次沒有處理，由 [[Task 60]] 處理。

## 3. 要做的

✅ 2026-10-18 app 加進清單，imp-home 三份中文版改好，Task 58 的紀錄更正。

## 4. 驗證

- tw-keep-english.md `check_ste.py --ste` PASS，警告和改之前相同。
- tw-keep-english 中英兩份 `check_parity.py` 0 failure，警告和 HEAD 相同；`diff_md.py --verify` PASS。
- imp-home 三對 `check_parity.py` 0 failure，警告和改之前相同。

## 5. 與其他 task 的關係

- [[Task 58]]：翻 md-style 的中文版時發現 app 不在清單上。
- [[Task 48]]：把 term 加進清單時，一起改了中文版裡的「術語」；這次照同樣的做法。
- [[Task 32.8]]：同一天在改 tw-keep-english 的 Technical words，兩邊分開提交。
- [[Task 60]]：處理順帶發現的 fenced blocks FAIL。

## 6. 日誌

### 2026-10-18

- 建立：使用者決定把 app 加進 tw-keep-english，並在這個 task 裡改掉 imp-home 中文版的「應用」。
- app 加進清單，版本改成 261018；imp-home 三份中文版改好；Task 58 的順帶發現更正。
- 順帶發現的 fenced blocks FAIL 由 [[Task 60]] 處理。
