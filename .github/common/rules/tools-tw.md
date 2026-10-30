# Tool Rules

> [[ASD-STE100_ISSUE9.pdf]]  `2026-10-18`  `d1f4ea9e7cd6`
> [[ste-custom]]  `2026-10-30`  `8cc2e2061175`

> 本檔案以 ASD-STE100 Simplified Technical English（STE）第 9 版寫成。
> 技術用字：alias、binary、block、byte、call、command、content、default、definition、directory、false negative、field、file、filter、flag、glossary、harness、hit、line、macOS、path、pattern、prefix、preview、project、query、scope、separator、skill、string、term、token、verification。

這些規則說明所有 skill 該用哪些命令列工具。
這些規則是為了**讓 token 的數量更少**，而不是因為某個執行檔比另一個執行檔好。

底下所有的位元組數，都是我們對一份 363 行、37,948 bytes 的 `SKILL.md` 量到的。

# 1. Search with `rg`

- 搜尋一律用 `rg`（`ripgrep`）。
  不要用 `grep`。
- **原因不是輸出的位元組數。**
  同一個查詢，`rg` 與 `grep` 給出的輸出一個位元組都不差（我們量到兩者都是 3,728 bytes）。
  你得到的是 `rg` 的**預設值**。
  `rg` 會自動略過 `.gitignore` 中的路徑與二進位檔。
  因此，你不用再加上濾網，例如 `| grep -v __pycache__`。
  結果是你第一次就把每個指令寫對，只要執行一次。
- 在 macOS 上，`grep` 可能是 **`ugrep`** 的 alias（`grep --version` 會顯示 `ugrep`）。
  `ugrep` 的旗標不一定和 GNU `grep` 的旗標給出同樣的結果。
  如果你混用這兩個工具，會得到不容易看出來的差異。
  如果你一律用 `rg`，就不會有這個問題。

## Pick the flag by what you need to know

| What you need | Use | Measured output |
| :--- | :--- | ---: |
| 有沒有？命中幾處？ | `rg -c pattern file` | **2 bytes** |
| 哪些檔案含有它？ | `rg -l pattern dir/` | **153 bytes** |
| 它周圍有哪些行？ | `rg -n pattern -A3 file` | **298 bytes** |
| 所有命中，完整列出 | `rg -n pattern file` | **2,830 bytes** |

- 要確認某個字串**沒有**命中時，用 `rg -c` 或 `rg -l`，而**不是** `rg -n`。
  這兩個指令的輸出相差超過 1,400×。
- **驗證用的搜尋，必須涵蓋每一個可能含有這個字串的目錄。**
  假陰性最常見的原因是：你只檢查了 `scripts/`，就說整個專案都乾淨了。
  如果搜尋的範圍不對，任何搜尋工具都幫不了你。

# 2. Read only the range you need

- 重要的是比較**範圍與整份檔案**，而不是比較兩個工具。
  從那份 `SKILL.md` 讀一個 9 行的區塊時，整份檔案是 **37,948** bytes。
  那 9 行是 **~1,200** bytes。
  那 97% 就是這條規則的目的。
- **預設：`rg -n pattern -B<n> -A<n>`。**
  這個指令不需要行號。
  因此這個指令只是一次呼叫，而不是先搜尋、再用第二次呼叫讀出那幾行。
  內容相同時，它比 `sed` 多用一些位元組（行號的前綴，以及 `--` 分隔線）。
  這個差別小到不重要。
- **例外：如果 `rg` 無法只取出你要的那一段，就用 `sed -n 'A,Bp'`。**
  `rg` 沒有指定行號範圍的旗標。
  因此在兩種情況下，`rg` 給不出你要的範圍。
  這兩種情況看起來不同，其實是同一個問題：
  - pattern 命中**多處**，`-A`／`-B` 會列出每一個區塊。
  - **沒有**能找出這個範圍的 pattern（例如只是檔案中段的一段行號）。

  這個差別並不小。
  `Checkpoint Dir` 在那份 `SKILL.md` 中出現 17 次。
  你只想讀第 37–38 行的那一處：

  | | Output |
  | :--- | ---: |
  | `rg -n 'Checkpoint Dir' -A1`：全部 17 個區塊 | **4,693 bytes** |
  | `sed -n '37,38p'`：只有你要的那一個 | **119 bytes** |

  例如，glossary 給出一個 term 的定義，之後每一個 step 都用到這個 term。
  這種情況很常見。
  先用 `rg -c` 數一數命中幾處。
  如果超過一處，就用 `sed`。
  （檔案的開頭或結尾，用 `head` 或 `tail`。）
- 規則是「**只讀需要的那幾行**」，不是「用 `rg`」，也不是「用 `sed`」。
  如果你用 `sed -n '1,$p'` 去讀這條規則不讓你讀的整份檔案，用掉的 token 一樣多。
  而且從這個指令看不清楚它讀了整份檔案。
  這樣做，你並沒有遵守這條規則。

# 3. `cat` is narrowed, not banned

- `cat` 只用在下列其中一種情況：
  - 你知道檔案很小（約少於 100 行，例如 `config.yaml`）。
  - 規則要求你**整份讀完**（例如某個 skill 規定「讀這個目錄裡的每一個 `.md`，不要抽樣」）。
- 其他所有檔案，都照第 2 條處理。
- **不要同時對一個以上的大檔使用 `cat`。**
  如果輸出太大，harness 會把它存成檔案，只給出 2KB 的預覽。
  接著你必須一次一個地重新讀這些檔案。
  這比一開始就一次讀一個檔案用掉更多 token。

# 4. Print only the fields you are about to use

- 當 `python -c` 或同類的指令檢視 JSON 或 YAML 時，**只顯示下一個 step 需要的欄位**。
  不要顯示整個結構。
- 如果你把兩個 step 之間的大型檔案（`market-data.json` 這類檔案）整份顯示出來，用掉的 token 通常比最大的一次 `cat` 還多。
  在 agent 的工作中，這是 agent 最常沒注意到、會讓 token 數量變多的原因。
