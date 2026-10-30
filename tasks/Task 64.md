# Task 64 - gen-skill 抄範本時，不帶 STE 檔頭

**Status**：完成——2026-10-19 gen-skill 抄範本時拿掉範本的 STE 標記；用 STE 版的 README-tmp 寫一個拋棄式 skill，驗證新的 README.md 沒有 STE 檔頭。
**Raised**：2026-10-18，[[Task 32.10]] 準備 README-tmp 的 STE 草稿送審時發現：gen-skill 整份抄範本，範本的 header note 兩行會留在新的 README.md，把它標成 STE 檔；SKILL-tmp 也一樣。
**Depends on**：—

## 1. 背景

STE 檔的檔頭有兩部分：引用區宣告 `[[ASD-STE100_ISSUE9.pdf]]` 與 `[[ste-custom]]`，header note 是「This file is in ASD-STE100 Simplified Technical English (STE), Issue 9.」與「Technical words: …」兩行。
[gen-skill](../.github/common/skills/gen-skill/SKILL.md) 的 Step 2 把 SKILL 範本抄成新 skill 的 `SKILL.md`，Step 5 把 README 範本抄成 `README.md` 再填寫。
Step 5 只留引用區裡適用的依賴行，所以 PDF 與 ste-custom 那兩行會被拿掉；header note 卻沒有規則處理，會留在新的檔案裡。
新 skill 的 `SKILL.md` 與 `README.md` 不是 STE 檔：gen-skill 填進去的內容沒有經過 STE 檢查，標成 STE 檔就說錯了。

## 2. 現況

### 已決定（2026-10-19）

- README-tmp 審核通過之後，使用者決定先做本 task，再取代 README-tmp。
- 規則寫成 MUST FOLLOW 的一條，兩個範本共用，不在 Step 2 與 Step 5 各寫一次。
- gen-skill 的 README 在 When the Skill Is Changed 的兩個範本節點各補一行。
- 驗證：README-tmp 取代原檔之後，用 gen-skill 寫一個拋棄式 skill，確認新的 `README.md` 沒有 STE 檔頭，再跑 check-skill，跑完刪掉。
- 提交：規則一個 commit，前綴 `task 64`；README-tmp 取代原檔的 commit 先提交，驗證之後再補一個 `task 64` 的 commit，記下結果。

### 結果（2026-10-19）

- gen-skill 的 MUST FOLLOW 加上「The new skill's `SKILL.md` and `README.md` carry none of a template's STE marks.」：Step 2 與 Step 5 從複製來的檔案拿掉 `[[ASD-STE100_ISSUE9.pdf]]`、`[[ste-custom]]` 兩行與整段 header note。
- README 的兩個範本節點各加一行「a template in STE: MUST FOLLOW drops its STE header-quote lines and its header note from the copy」。
- 中文版照 chinese skill 改：SKILL.md 有 frontmatter，MUST FOLLOW 一節照原有的譯文加上新的一條；README 只多兩行 fenced 的內容。
- 檢查：兩對中英對照 `check_parity.py` 0 failure、警告和之前相同，`diff_md.py --verify` 都 PASS；README 的 `depends_on.py check` 都是 UNCHANGED；check-skill 的 `scan_skill.py` 只有行號多了 3。

### 驗證（2026-10-19）

- README-tmp 取代原檔之後，在 InvestForge 的 dedi 群組照 gen-skill 的步驟寫一個最小的拋棄式 skill `zz-ste-mark-check`：沒有 MD report、YAML checkpoint 與 TW twins，Step 0 之後只有一個不執行 script 的 step。
- Step 5 複製來的 `README.md` 在第 12、13 行有 `[[ASD-STE100_ISSUE9.pdf]]` 與 `[[ste-custom]]`，第 15、16 行有 header note；照新的規則拿掉之後，新的 `SKILL.md` 與 `README.md` 都找不到 ASD-STE100、ste-custom 與 Technical words。
- `depends_on.py record` 記下引用區留下的 5 行，`check` 都是 UNCHANGED。
- check-skill 的 `scan_skill.py`：`SKILL.md` 與 `README.md` 都沒有缺少的標題，順序正確，沒有 leftover 與 placeholder，Dataflow 也沒有問題。
- 跑完刪掉拋棄式 skill，InvestForge 的 git status 和跑之前相同。
- SKILL-tmp 還不是 STE 版，所以 Step 2 複製來的 `SKILL.md` 本來就沒有 STE 標記；這條規則對 `SKILL.md` 的作用，要等 [[Task 32.11]] 取代 SKILL-tmp 之後才用得到。

## 3. 要做的

1. ✅ gen-skill 抄範本時，拿掉範本的 STE 檔頭：引用區的 `[[ASD-STE100_ISSUE9.pdf]]` 與 `[[ste-custom]]` 兩行，以及 header note 的兩行；SKILL 範本與 README 範本都適用。
2. ✅ 先讀 gen-skill 的 [README.md](../.github/common/skills/gen-skill/README.md) 的 When the Skill Is Changed 與 [skill-writing.md](../.github/common/rules/skill-writing.md)，照它改，並跑它列出的檢查；中文版照 chinese skill 跟著改。
3. ✅ 在 [[Task 32.10]] 與 [[Task 32.11]] 以 Step 7 取代範本之前做完。
4. ✅ README-tmp 取代原檔之後，用 gen-skill 寫一個拋棄式 skill，確認新的 `README.md` 沒有 STE 檔頭，再跑 check-skill；跑完刪掉。

## 4. 驗證

- 用 STE 版的範本跑一次 gen-skill，例如在 workspace 以外的副本上：新的 `SKILL.md` 與 `README.md` 沒有 STE 的引用行與 header note。
- gen-skill 的 README 列出的檢查都通過。

## 5. 與其他 task 的關係

- [[Task 32.10]]、[[Task 32.11]]：README-tmp 與 SKILL-tmp 的 STE 草稿；取代原檔之前，要先做完本 task。

## 6. 日誌

### 2026-10-19

- gen-skill 的 MUST FOLLOW 加上不帶範本 STE 標記的規則，README 的兩個範本節點各補一行，中文版照 chinese skill 改；檢查都通過，驗證等 README-tmp 取代原檔之後跑。
- README-tmp 取代原檔之後，在 InvestForge 用 gen-skill 寫拋棄式 skill `zz-ste-mark-check` 驗證：新的 `README.md` 沒有 STE 檔頭，check-skill 的 scan 沒有問題，跑完刪掉；本 task 完成。

### 2026-10-18

- 建立。
