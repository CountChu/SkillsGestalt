# Skill Writing Rules

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-18`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-30`  `8cc2e2061175`

> 本檔案以 ASD-STE100 Simplified Technical English（STE）第 9 版寫成。
> 技術用字：Dataflow、definition、file、glossary、line、link、natural language、noun、script、section、sentence、skill、summary、term、text、twin。

這些規則說明怎麼寫 skill 的 `SKILL.md` 與 `README.md`。
你在寫 skill 時使用這些規則，而不是在執行 skill 時。
因此，`SKILL.md` 不收錄這些規則。
`gen-skill` 依這些規則寫 skill，`check-skill` 確認 skill 遵守它們，skill 的 `README.md` 則引用它們。

# Rules

- **修改 skill 之前，先讀它的 `README.md`，如果這個 skill 有的話。**
  README 說明哪些檔案要一起改，以及改完之後要做哪些檢查。
  README 的「When the Skill Is Changed」一節列出的修改，都要在同一次執行中做完。
  完成修改之前，做完這一節列出的所有檢查。
- **每個 skill 都有一份 `README.md`，以 [README-tmp.md](../templates/README-tmp.md) 寫成。**
  它收錄執行時用不到的資訊，例如 Dataflow。
  它也說明哪些檔案要一起改，以及 skill 依賴哪些檔案。
  `SKILL.md` 只收錄執行時需要的資訊，因為每次執行都會讀它的全部內容。
  `SKILL.md` 沒有連到 `README.md` 的連結，所以沒有一次執行會讀 `README.md`。
  如果一個 skill 的 `SKILL.md` 有繁體中文 twin，這個 skill 也有 `README-tw.md`。
- **在 `SKILL.md` 的 glossary 中，為 step 需要的每一個名詞寫一個定義。**
  glossary 是 `SKILL.md` 的 `# TERMINOLOGY` 與 `# DEDICATED TERMINOLOGY` 兩節。
  `# TERMINOLOGY` 收錄在所有 skill 中一律指同一個項目的 term，`# DEDICATED TERMINOLOGY` 收錄只有這個 skill 使用的 term。

  之後各 step 使用這個 term，不再重寫它的定義。
  只有 glossary 有這個定義。
  如果某個 step 再寫一次定義，兩份定義就會變得不一樣。
  glossary 留在 `SKILL.md`，因為執行時必須知道它的 step 所用每一個 term 的定義。
- **每個 step 都自足：「no forward-reference」。**
  一個 step 不依賴排在它之後的 step。
  如果一個 step 為了控制流程而提到後面的 step，這個 step 就遵守這條規則。
  但如果一個 step 使用後面某個 step 的輸出，這個 step 就不遵守這條規則。
- **如果程式能以 deterministic 方式做某個 step，這個 step 就執行 script：「scripted-versus-not」。**
  如果一個 step 必須閱讀文字、做出決定或寫摘要，就不要為它寫 script。
  把這個 step 寫成自然語言的指示，讓 agent 直接照著做。
- **skill 只說明一次它怎麼遵守上一條規則**：哪些 step 執行 script、哪些不執行，以及原因。
  如果大多數 step 底下都有同樣的一行，那一行不帶任何資訊。
  而且 step 的 Purpose 通常也會給出同樣的原因。
  `README.md` 的「Files Each Step Uses」一節寫出這項資訊。
- **每個 step 都有一條 Purpose**：一句話，說明為什麼要有這個 step。
  也就是說，它說明把這個 step 與相鄰的 step 合在一起時，skill 會怎樣變差。
  Purpose 不是這個 step 做了什麼的摘要，因為 step 的指示就給出了這項資訊。
  如果 Purpose 把指示再寫一次，它就是第二份副本，兩份副本會變得不一樣。
  `README.md` 的「Step Purposes」一節寫出每一條 Purpose。
