# Home — Wireframe

**本文件擁有頁面的元素清單與它的外觀：頁面必須 *包含* 什麼，以及它必須 *長什麼樣子*。**
hub 必須 *做* 什麼不在這裡決定。

**兩份設計文件不提到對方，兩個方向都不提。**
各自聲明自己的範圍，所以兩份都可以先讀，而且任一份重新編號時，另一份也不會變成 stale。
一條規則若它的理由在另一份檔案裡，就在這裡**完整地寫出來**，而不是引用——一個值得擁有的理由，就值得寫在它適用的地方。
**顏色、hover 狀態與框線屬於這裡**，與它們所描述的元素在一起；而一句即使按鈕重新上色也仍然成立的話，則屬於設計文件。

它是**規定性的，不是一次掃描**：它說明頁面必須有什麼，而執行中的頁面要拿來對照它。
除非某一列的 Visibility 另有說明，否則底下每一個元素都是必要的。

---

## 1 Page structure

一頁、單欄、置中。
沒有面板、沒有篩選器、沒有控制項——hub 所做的一切就是導覽。

```
<main>
  <h1>            title, from the app config
  <p>             one-line summary
  <div.buttons>   the button grid, in link-list order
    <a>           one per link entry
      <span.label>
      <span.url>
      <span.note>   only when the entry has a note
```

## 2 Elements

| # | Element | Kind | Content | Visibility |
|---|---|---|---|---|
| 1 | Heading | `h1` | app config 的 `title`，已跳脫 | always |
| 2 | Summary | `p` | 一行固定文字，邀請讀者挑一個 app | always |
| 3 | Button grid | `div.buttons` | 每一筆 link entry 一個 anchor，依 link list 的順序 | always |
| 4 | Button | `a` | 整筆項目；`href` 是該項目逐字照登並已跳脫的 `href` | 每筆 link entry 一個 |
| 5 | Button label | `span.label` | 該項目的 `label`，已跳脫 | always，在每一顆按鈕裡 |
| 6 | Button URL | `span.url` | 該項目逐字照登並已跳脫的 `href`，以等寬字體 | always，在每一顆按鈕裡 |
| 7 | Button note | `span.note` | 該項目的 `note`，已跳脫 | 只在該項目帶有 note 時 |
| 8 | Empty state | `p.empty` | 一行說明沒有設定任何連結、以及該怎麼辦 | 只在 link list 為空時，並取代 grid |

**每一顆按鈕都是同一個元素、帶同一組 class。**
一個頁面無法導覽過去的連結，與一個由 hub 自己提供的連結，都由第 4–7 列渲染，跟其他任何項目一模一樣：沒有額外 class、沒有標記、順序也沒有差別。
頁面無從分辨它們，而那是設計，不是疏漏。

## 3 Pages other than the hub page

這些頁面抵達得了，但不是 hub 頁面，而且它們帶著自己的 markup 而不是那份樣式表——一個 mount 的失敗會在它前綴底下的任何深度回應，因此不存在哪一條相對路徑指向樣式表會是正確的。

| Page | Reached by | Must contain |
|---|---|---|
| Mount not prepared | 某個 app 載入不起來的 mount 底下的任何路徑 | 該 mount 的 label、原因、找過的目錄、組裝它的 skill，以及一個回到 `/` 的連結 |
| Mount failed while answering | 一個 throw 或 reject 了的被掛載 app | 純文字，指名那個 app 與錯誤，並說明 hub 與它其他的 mount 都不受影響 |
| Health | `GET /healthz` | JSON：`{ok, title, links, dead, mounts, assembledAt}`，其中 `mounts` 是每一個已設定 mount 一個 `{prefix, label, ok, error}` |

## 4 Visibility states

- **button note**（第 7 列）是按鈕內部唯一可以缺席的元素。
- **empty state**（第 8 列）與 **button grid**（第 3 列）互斥。
- 頁面上沒有任何東西是因為一次互動才出現的——根本沒有互動。
  一個點擊之後清單就改變的頁面，代表有什麼被加了進來，而這份文件沒有承載它。

## 5 What the page must not contain

- **任何地方都不得有 `<script>`。**
  渲染發生在伺服器；沒有任何東西要交給客戶端執行。
- **除了那唯一一份同源樣式表之外，沒有任何外部參照**：無 CDN、無網路字型、無圖片、無分析工具。
- **沒有超出 §2 那些 class 的按鈕層級樣式掛勾**，而那正是讓 2.4 的規則可以靠檢視就強制執行的原因。

## 6 Defects found by checking a running page

在這裡記下活頁面顯示了什麼、而這份清單沒有預測到的，並附上日期。
顯示錯值的元素仍然是一個元素——兩個事實都要記，並把它違反的那條規則也寫進設計的 Specification。

*（目前沒有紀錄）*
