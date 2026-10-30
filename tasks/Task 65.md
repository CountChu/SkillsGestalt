# Task 65 - 檢查 README-tmp 的 Dataflow

**Status**：尚未開始——2026-10-18 記下：等 [[Task 32.10]] 把 README-tmp 換成 STE 版之後，對照 DFD.md 檢查它的 Dataflow 一節與中文版。
**Raised**：2026-10-18，使用者要求檢查 README-tmp 的 Dataflow。
**Depends on**：[[Task 32.10]]

## 1. 背景

[README-tmp.md](../.github/common/templates/README-tmp.md) 是每個 skill 的 `README.md` 的範本；它的 `## Dataflow` 一節有說明文字、一張 mermaid 範例圖與圖例，gen-skill 照它寫出每個新 skill 的 Dataflow。
範本的 Dataflow 若和 [DFD.md](../.github/common/references/DFD.md) 的記法不一致，照它寫成的每一份 README 都會帶著同樣的落差。
[[Task 32.10]] 正在把 README-tmp 改寫成 STE；使用者決定等它取代原檔之後再查，免得取代後文字與行號都變了，查過的要重做。

## 2. 現況

### 已決定（2026-10-18）

- 範圍：README-tmp 的 `## Dataflow` 一節，也就是說明文字、mermaid 範例圖與圖例，以及 [README-tmp-tw.md](../.github/common/templates/README-tmp-tw.md) 對應的一節；照範本寫成的各 skill README 不在範圍內。
- 依據：DFD.md 的記法，也就是三種資料、五種形狀、線的種類與兩種顏色、圖例，以及它列的缺陷。
- 時機：等 [[Task 32.10]] 取代原檔之後，對 STE 版查。
- 產出：列出每個發現，寫明行號、依據與建議，由使用者逐項決定；決定要改的，在本 task 改原文、中文版與受影響的檔。

### 順帶發現（不在本 task 的範圍）

- check-skill 的 [checking-criteria.md](../.github/common/skills/check-skill/references/checking-criteria.md) 判準 6.2 說每個節點的形狀照 DFD.md，卻列了 DFD.md 沒有的雙邊框，也就是跑 RSDC 系統程式的 step（`[["…"]]`）；這個畫法出自 [gen-rsdc-skill 的 SKILL.md](../.github/common/skills/gen-rsdc-skill/SKILL.md)。
  README-tmp 的圖例也沒有它；只有 gen-rsdc-skill 寫的 skill 用得到，查的時候一併判斷要不要另外處理。

## 3. 要做的

1. 確認 [[Task 32.10]] 已取代原檔，README-tmp 已是 STE 版。
2. 對照 DFD.md 檢查 README-tmp 的 Dataflow 一節：
   - 說明文字：三種資料、step 的名稱、只畫執行時讀寫的資料，說法和 DFD.md 一致。
   - 範例圖：每個節點的形狀合它的種類；每條線的種類與顏色，包括 `linkStyle` 列出的藍線，合 DFD.md 的規則；role 畫出了它讀與供給的資料；圖裡沒有 DFD.md 列的缺陷。
   - 圖例：每種形狀與每種線都說到，說法和 DFD.md 一致。
3. 中文版對應的一節照 chinese skill 的做法比對：圖照抄，文字照英文。
4. 列出發現，交給使用者逐項決定。
   要改的，STE 版照 asd-ste 的規則改，中文版照 chinese skill 跟著改；記錄 README-tmp.md 的文件讀過改動之後重記。

## 4. 驗證

- 每個發現都寫明 README-tmp 的行號與 DFD.md 的依據，使用者對每一項都做了決定。
- 有改的話：STE 版的 `check_ste.py --ste` PASS，中英對照的 `check_parity.py` 0 failure，記錄 README-tmp.md 的文件 `depends_on.py check` 都是 UNCHANGED。

## 5. 與其他 task 的關係

- [[Task 32.10]]：README-tmp 的 STE 草稿；取代原檔之後才做本 task。
- [[Task 61]]：規則只寫一次；它的第 4 組是 checking-criteria 重述 README-tmp「只畫執行時讀寫的資料」這一句。
- [[Task 24]]：其餘 skill 改成新格式時照 README-tmp 寫 README，Dataflow 也照它畫。

## 6. 日誌

### 2026-10-18

- 建立：使用者要求檢查 README-tmp 的 Dataflow；決定只查範本的 Dataflow 一節與中文版，對照 DFD.md，等 [[Task 32.10]] 取代原檔之後再做，查完列出發現由使用者逐項決定。
