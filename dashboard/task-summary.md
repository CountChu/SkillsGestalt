# Tasks

跨 session 的待辦工作。
每個 task 是 `tasks/Task N.md` 一個檔案。
本檔只放下面的摘要表：先讀這張表，再只開需要的那個 task。
task 檔的格式與摘要表的維護方式，見 [task-rules.md](../.github/common/rules/task-rules.md)；檢查指令見根目錄的 [CLAUDE.md](../CLAUDE.md)。

| Task | Raised | Title | Status | Depends on |
| --- | --- | --- | --- | --- |
| [[Task 88]] | 2026-10-31 | 讓別的 agency 能自己接上 SkillsGestalt | ✅ | — |
| ├─ [[Task 88.1]] | 2026-10-31 | Forge 用的 config.yaml 範本 | ✅ | — |
| ├─ [[Task 88.2]] | 2026-10-31 | 接上 SkillsGestalt 的指南 forge-setup.md | ✅ | [[Task 88.1]] ✅ |
| └─ [[Task 88.3]] | 2026-10-31 | 改了會影響 Forge 的東西時怎麼通知 | ✅ | — |
| [[Task 87]] | 2026-10-30 | chore 不放自己的程式，只呼叫 skill group 裡的 | ✅ | [[Task 86]] ✅ |
| [[Task 86]] | 2026-10-30 | chore 改用名稱，不用編號，和 skill 一樣 | ✅ | [[Task 85]] ✅ |
| [[Task 85]] | 2026-10-30 | 讓 Forge 像使用 skill 一樣使用本 agency 的 chore，以 {agencies.X} 定位 | ✅ | — |
| [[Task 84]] | 2026-10-30 | 由 CLAUDE-tmp.md 與 CLAUDE-local.md 產生 CLAUDE.md | ✅ | [[Task 82]] ✅、[[Task 83]] ✅ |
| [[Task 83]] | 2026-10-30 | CLAUDE.md 裡 common 的路徑要和 config.yaml 一致 | ✅ | [[Task 82]] ✅ |
| [[Task 82]] | 2026-10-30 | 把每個 agency 共通的 CLAUDE.md 規則抽成 common 的一份規則檔 | ✅ | — |
| [[Task 81]] | 2026-10-30 | 術語表：Agency、Gestalt 與 Forge | ✅ | — |
| [[Task 80]] | 2026-10-30 | 根目錄的 CLAUDE.md 改寫成英文 | ✅ | — |
| [[Task 79]] | 2026-10-30 | 本機分支改名：master 改為 m1，public 改為 main | ✅ | — |
| [[Task 78]] | 2026-10-30 | 把 SkillsGestalt 公開到 GitHub，排除 checkpoints 與公司內部資訊 | ✅ | — |
| [[Task 77]] | 2026-10-20 | 拆出 SKILL-Compile.md，並替 compile-skill 寫 README | ✅ | — |
| [[Task 76]] | 2026-10-20 | skill-writing.md 加一條規則：skill 執行的程式不呼叫 LLM | ⬜ | — |
| [[Task 75]] | 2026-10-20 | 讓 check_rsdc.py 與 depends_on.py 分辨範例引用 | ⬜ | — |
| [[Task 74]] | 2026-10-20 | 修正 compile-skill 兩支 script 的三個缺陷 | ⬜ | — |
| [[Task 73]] | 2026-10-20 | 照 keep-English 稽核改中文版的譯法：261018 版 | ⬜ | — |
| [[Task 72]] | 2026-10-04 | 建 Agentic Panel | ⬜ | — |
| [[Task 71]] | 2026-10-20 | 把 skill 目錄下的 Tasks.md 交給 tasks 管理 | ✅ | — |
| [[Task 70]] | 2026-10-19 | SKILL.md 的共用句子換成 STE 範本的寫法 | ⬜ | — |
| [[Task 69]] | 2026-10-19 | 盤點 task 檔裡其他 keep-English 譯法，決定 check_tasks.py 要不要掃描 | ⬜ | — |
| [[Task 68]] | 2026-10-19 | 把 task 檔裡的「配對行」改成 pairing line | ✅ | — |
| [[Task 67]] | 2026-10-19 | draft.py replace 把中文版的 pairing line 指回原檔 | ✅ | — |
| [[Task 66]] | 2026-10-19 | README 的共用句子換成 STE 範本的寫法 | ⬜ | — |
| [[Task 65]] | 2026-10-18 | 檢查 README-tmp 的 Dataflow | ⬜ | [[Task 32.10]] ✅ |
| [[Task 64]] | 2026-10-18 | gen-skill 抄範本時，不帶 STE 檔頭 | ✅ | — |
| [[Task 63]] | 2026-10-18 | 決定 task、chore 等新詞是否加進 keep-English list | ⬜ | — |
| [[Task 62]] | 2026-10-18 | 讓每個 workspace 有自己的 task 與 chore | 🔄 | — |
| ├─ [[Task 62.1]] | 2026-10-18 | task 與 chore 的規則搬進 common | ✅ | — |
| ├─ [[Task 62.2]] | 2026-10-18 | 檢查腳本允許空號，只掃 git 追蹤的檔 | ✅ | — |
| ├─ [[Task 62.3]] | 2026-10-18 | 建立 InvestForge 的 task 與 chore | ✅ | [[Task 62.1]] ✅ |
| ├─ [[Task 62.4]] | 2026-10-18 | 搬走 InvestForge 的 9 個 task，Task 18 只留這裡的 3 份 | ✅ | [[Task 62.2]] ✅、[[Task 62.3]] ✅ |
| ├─ [[Task 62.5]] | 2026-10-18 | 拆開 Task 32、38、54、55 與 Chore 2 | ✅ | [[Task 62.3]] ✅ |
| ├─ [[Task 62.6]] | 2026-10-18 | SkillsGestalt 自己的 config.yaml | ✅ | — |
| └─ [[Task 62.7]] | 2026-10-18 | asd-ste 的 Step 7 只重記本 workspace 的依賴方 | ⬜ | [[Task 62.5]] ✅ |
| [[Task 61]] | 2026-10-18 | 規則只寫一次：找出定規則的 md 之間重複的規則 | ✅ | — |
| [[Task 60]] | 2026-10-18 | 修正 Home-RSDC 的 fenced blocks FAIL：換行改成 LF，check_rsdc 報出換行不同 | ✅ | — |
| [[Task 59]] | 2026-10-18 | 把 app 加進 tw-keep-english，imp-home 中文版的「應用」改成 app | ✅ | — |
| [[Task 58]] | 2026-10-18 | md-style 加一條規則：文件不寫自己的來歷 | ✅ | — |
| [[Task 57]] | 2026-10-18 | 擴充 Chore 1：列出已是核准詞的技術用字，並在拼法清單改了之後重查 | ⬜ | — |
| [[Task 56]] | 2026-10-18 | 建立 md 巡檢的 chore：md-style 與重複的規則 | ⬜ | — |
| [[Task 55]] | 2026-10-18 | 建立依賴巡檢的 chore：定期找出檔頭紀錄過期的文件 | ⬜ | — |
| [[Task 54]] | 2026-10-18 | 建立 Chore 3：定期以 check-skill 檢查每個 skill | ⬜ | [[Task 24]] ⬜ |
| [[Task 53]] | 2026-10-18 | 建立 chore：會重複做的例行工作 | ✅ | — |
| [[Task 52]] | 2026-10-18 | ste-custom 一天改好幾次時，集中一次重記 | ✅ | — |
| [[Task 51]] | 2026-10-18 | 把 update 收進專案核准詞，STE 檔不再把它列為技術用字 | ✅ | — |
| [[Task 50]] | 2026-10-17 | 讓 ste-custom.md 分成 Words 與 Rules，加上第一條專案規則：不用雙重否定 | ✅ | — |
| [[Task 49]] | 2026-10-17 | 把 false 與 false alarm 收進專案核准詞 | ✅ | — |
| [[Task 48]] | 2026-10-16 | 把中文版裡指 term 的「術語」改成 term | ✅ | — |
| [[Task 47]] | 2026-10-16 | 把 phrase 收進專案核准詞，STE 檔不再把它列為技術用字 | ✅ | — |
| [[Task 46]] | 2026-10-16 | 把 RSDC 的 Terms 改名為 Terminology | ✅ | — |
| [[Task 45]] | 2026-10-16 | 把文件的版本寫進 header quote，讓工具讀它 | ✅ | — |
| [[Task 44]] | 2026-10-16 | 把 rule 收進專案核准詞，STE 檔不再把它列為技術用字 | ✅ | — |
| [[Task 43]] | 2026-10-14 | 把 technical term 改稱 term（術語），STE customization 改稱 project-approved word（專案核准詞） | ✅ | — |
| [[Task 42]] | 2026-10-14 | 讓 reformat_md.py 斷句時不把 inline code 誤當成數學式 | ✅ | — |
| [[Task 41]] | 2026-10-14 | 讓 check_ste.py 提醒字典不核准的技術用字 | ⬜ | — |
| [[Task 40]] | 2026-10-13 | 更新 asd-ste 的對照頁 | 🔄 | — |
| [[Task 39]] | 2026-10-13 | 讓 asd-ste 產生 STE 草稿的對照頁 | ✅ | — |
| [[Task 38]] | 2026-10-13 | 為英文文件訂下美式拼法的規則與檢查 | ✅ | — |
| [[Task 36]] | 2026-10-13 | 讓 reformat_md.py 在直引號內不斷句，並認得以 ⌘ 或小寫名稱開頭的句子 | ✅ | — |
| [[Task 35]] | 2026-10-12 | 為 asd-ste 加上自訂核准字的 customization 檔 | ✅ | — |
| [[Task 34]] | 2026-10-12 | 為 .github/common 中沒有中文版的 4 份原檔執行 /chinese | ✅ | [[Task 33]] ✅ |
| [[Task 33]] | 2026-10-12 | 從所有原檔拿掉指向中文版的那一句 | ✅ | — |
| [[Task 32]] | 2026-10-12 | 人工審核 STE 草稿，通過後由 asd-ste 取代原檔 | ✅ | [[Task 31]] ✅、[[Task 38]] ✅、[[Task 39]] ✅ |
| ├─ [[Task 32.1]] | 2026-10-12 | DFD | ✅ | — |
| ├─ [[Task 32.2]] | 2026-10-12 | RSDC-Standard | ✅ | — |
| ├─ [[Task 32.3]] | 2026-10-12 | tw-keep-english | ✅ | — |
| ├─ [[Task 32.4]] | 2026-10-12 | md-style | ✅ | — |
| ├─ [[Task 32.5]] | 2026-10-12 | report-md-rules | ✅ | — |
| ├─ [[Task 32.6]] | 2026-10-12 | report-yaml-rules | ✅ | — |
| ├─ [[Task 32.7]] | 2026-10-12 | scratch-rules | ✅ | — |
| ├─ [[Task 32.8]] | 2026-10-12 | skill-writing | ✅ | — |
| ├─ [[Task 32.9]] | 2026-10-12 | tools | ✅ | — |
| ├─ [[Task 32.10]] | 2026-10-12 | README-tmp | ✅ | [[Task 64]] ✅ |
| └─ [[Task 32.11]] | 2026-10-12 | SKILL-tmp | ✅ | [[Task 64]] ✅、[[Task 67]] ✅ |
| [[Task 31]] | 2026-10-12 | 交給 asd-ste 為 .github/common 的 references、rules、templates 產生 STE 草稿 | ✅ | [[Task 33]] ✅、[[Task 34]] ✅、[[Task 35]] ✅ |
| [[Task 27]] | 2026-10-12 | 確認在桌面版刪除 session 時是否會觸發 SessionEnd hook | ⬜ | — |
| [[Task 26]] | 2026-10-12 | 決定 ASD-STE100 規格的 PDF 是否留在 git 中 | ✅ | — |
| [[Task 25]] | 2026-10-12 | 舊檔中的 `___PLACEHOLDER___` 一律視為錯誤 | ✅ | [[Task 15]] ✅ |
| [[Task 24]] | 2026-10-11 | 把其餘 skill 改成 SKILL.md 與 README.md 的新格式 | ⬜ | [[Task 22]] ✅、[[Task 32]] ✅ |
| [[Task 23]] | 2026-10-11 | 建立 asd-ste skill：把 Markdown 改寫成 ASD-STE100 STE | ✅ | — |
| [[Task 22]] | 2026-10-11 | 讓 gen-skill、check-skill 與 SKILL 範本跟上 README.md 的拆分 | ✅ | [[Task 20]] ✅ |
| [[Task 21]] | 2026-10-11 | 把 SKILL.md 中執行時用不到的內容移到 README.md | ✅ | — |
| [[Task 20]] | 2026-10-11 | 為 skill 建立 README.md：Dependency，以及 SKILL.md 執行時用不到的內容 | ✅ | — |
| [[Task 19]] | 2026-10-11 | 決定 md 檔是否採用每個句子一行的寫法 | ✅ | — |
| [[Task 18]] | 2026-10-10 | 讓已寫好的 RSDC 跟上對齊後的範本 | 🔄 | [[Task 12]] ✅、[[Task 10]] ✅、[[Task 33]] ✅ |
| ├─ [[Task 18.2]] | 2026-10-10 | SkillCompiler-RSDC | ✅ | — |
| ├─ [[Task 18.7]] | 2026-10-10 | Home-RSDC（imp-home 的 seed） | ✅ | — |
| └─ [[Task 18.8]] | 2026-10-10 | MermaidView-RSDC | ⬜ | — |
| [[Task 17]] | 2026-10-10 | 讓 gen-rsdc-app 與 imp-app 跟上對齊後的 App 範本 | ✅ | [[Task 12]] ✅ |
| [[Task 16]] | 2026-10-10 | 讓 compile-skill 與 gen-skill 處理檔頭引用區的依賴格式 | ✅ | [[Task 13]] ✅ |
| [[Task 15]] | 2026-10-10 | 把其餘範本與 skill 的佔位符改成大括號寫法 | ✅ | — |
| [[Task 14]] | 2026-10-10 | 將 imp-app 的 reverse 抽成 gen-rsdc-code skill，由 imp-app reverse 呼叫 | ✅ | [[Task 10]] ✅、[[Task 12]] ✅、[[Task 17]] ✅ |
| [[Task 13]] | 2026-10-10 | 讓其他 skill 處理檔頭引用區的依賴格式 | ✅ | — |
| [[Task 12]] | 2026-10-10 | 對齊 RSDC-App-tmp 與 RSDC-Skill-System-tmp 兩份範本的格式與內容 | ✅ | — |
| [[Task 11]] | 2026-10-10 | 統一六份 twin 中被 keep-English list 新標記的譯法 | ✅ | — |
| [[Task 10]] | 2026-10-10 | 讓 chinese skill 承接 RSDC twin 的專用規則 | ✅ | — |
| [[Task 9]] | 2026-10-09 | 修正三份未通過 chinese parity check 的既有 twin | ✅ | — |
| [[Task 8]] | 2026-10-09 | 文件依賴的檢查方式——依賴方記下被依賴方的 hash | ✅ | — |
| [[Task 7]] | 2026-10-09 | 決定如何處理 gen-rsdc-skill 與 chinese 的 Dataflow 揭露的多寫入者與往回讀取 | ✅ | — |
| [[Task 6]] | 2026-10-09 | 評估是否建立 tasks skill 來處理 tasks.md | ✅ | — |
| [[Task 5]] | 2026-10-09 | 將兩份 RSDC 範本第 2 章的 Flowchart 改稱 DFD | ✅ | — |
| [[Task 4]] | 2026-10-09 | 為 RSDC-Responsibilities 改一個較短的名稱 | ✅ | — |
| [[Task 3]] | 2026-10-09 | 決定 RSDC-Skill-System-tmp 的 Dataflow 是否只留 DFD | ✅ | — |
| [[Task 2]] | 2026-10-09 | 兩份 RSDC 範本的 Naming and Data Structures 對齊標準 | ✅ | — |
| [[Task 1]] | 2026-10-09 | 決定 Skill Source 是否改名為 Skill MD File | ✅ | — |

Status：⬜ 尚未開始　🔄 進行中　✅ 完成　⊘ 取消。
每一項的細節（例如「尚未決定」）寫在它自己的 **Status** 行。
Depends on：這個 task 開始之前要先完成的 task，後面的圖示是那個 task 現在的狀態；— 表示沒有。
空號：18.1、18.3、18.4、18.5、18.6、28、29、30、37。
空號是移出本 workspace 的 task 留下的號碼，不再使用。
