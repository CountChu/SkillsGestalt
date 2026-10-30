# Scratch File Rules

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-18`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-30`  `8cc2e2061175`

> 本檔案以 ASD-STE100 Simplified Technical English（STE）第 9 版寫成。
> 技術用字：app、checkpoint、command、commit、design document、directory、file、git、noise、path、root、scratch、script、skill、stage、untracked file、wildcard、workspace。

這些規則說明一次執行把它的暫存檔放在哪裡，以及怎麼移除這些檔案。

- **把每一個暫存檔都放進 workspace 根目錄的 `temp\`。**
  不要把它直接放在 workspace 的根目錄。
  不要把它放在它所檢查的原始碼旁邊。
  如果目錄不在，就建立它。
  這個目錄列在 `.gitignore` 中，所以裡面的檔案都不會進到 commit。
- **一次執行寫出的項目中，凡不是它的 skill 所指明的輸出，都是暫存檔。**
  例如做測試或檢查用的臨時 script，以及這次執行保留下來的指令輸出。
  其他例子還有這次執行在寫出它的輸出之前使用的 JSON 檔，以及為了測試而做的一份目錄臨時副本。
  MD report、YAML checkpoint、`database\` 檔案與 app 的目錄都是輸出，不是暫存檔。
  這些輸出各有自己的路徑。
- **讓暫存檔的名稱以產生它的 skill 的名稱開頭**，如 `temp\{skill-name}-{what-it-does}.py`。
  不這樣做的話，兩個不同 skill 的執行可能會用到同一個常見的名稱。
  這時第二次執行會取代第一次執行的檔案，而且不會告訴你。
- **移除這次執行建立的暫存檔，並寫出每一個檔案的完整名稱。**
  不要使用萬用字元。
  你可能以為 `Remove-Item temp\_s*.py` 只會移除你的檔案，但它會移除所有符合這個萬用字元的檔案。
  這些檔案可能包含另一次執行在那個時候正在使用的檔案。
  而且 `Remove-Item` **不**經過資源回收筒，所以它會永久移除未被追蹤的檔案。
  不要移除 `temp\` 目錄。
- **執行結束後留下的暫存檔不算錯誤。**
  一次執行若在完成工作之前停下，可以把檔案留在 `temp\`，因為它們顯示這次執行做了多少工作。
  `temp\` 裡的每一個項目都可以在你想要的時候安全地手動移除。
  這是把所有暫存檔都放在同一個位置最重要的原因。

**workspace 的根目錄不是放暫存檔的正確位置。**
執行寫在那裡的檔案是未被追蹤的檔案，*但 git 不會忽略它*。
因此，它會在 `git status` 裡顯示成雜訊。
而且，如果你在 commit 之後執行 `git clean -fd`，它會移除這個檔案，不會先取得你的同意。
同時，`git clean -fd` 也會移除其他執行放在它旁邊的所有檔案。

**app 的 `temp\` 目錄是另一個目錄。**
app 可以有一個 `temp\` 目錄，存放它的某個 stage 交給下一個 stage 的資料。
這個目錄是 app 的一部分。
app 的設計文件說明這個目錄。
這些規則不適用於它。
這些規則只適用於 workspace 根目錄的 `temp\` 目錄。

**`__pycache__` 也不是暫存檔。**
你在 script 所在的目錄中執行它時，Python 會產生 `__pycache__`，作為副作用。
而且 git 會忽略它。
移除 `__pycache__` 是可選的，而且不屬於移除暫存檔的程序。
