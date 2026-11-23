# 化學鍵結與分子結構：LLM Wiki 教學簡報

大一普化「化學鍵結與分子結構」。依 Karpathy 的 LLM Wiki 做法：先把來源整理成 Wiki，再只用 Wiki 產生教學 HTML 簡報。

## 1. LLM Wiki 主題與簡介
主題涵蓋能量觀點的化學鍵、電負度與極性、晶格能、路易斯結構與共振、形式電荷、VSEPR、混成軌域、分子軌域與鍵級、分子間作用力、金屬鍵與固體類型。每頁固定 9 個欄位（定義、重點、例題、常見誤解、矛盾、相關頁面、來源、信心程度、重要單字）。

## 2. Wiki 成果
- [`wiki/`](wiki/)：56 頁（含 `index.md`、`log.md`、`glossary.md`）
- [`schema/CLAUDE.md`](schema/CLAUDE.md)：Wiki 規則（v5，含 changelog）
- 來源：Zumdahl 10e（Ch.4 §4.9、8、9、10 部分）與 OpenStax Chemistry 2e（§7.5、§8.4）。**6 份來源**（6 個章節／小節檔，出自 2 本書；以 Zumdahl 為主，4 份）；課本 PDF 不放入 repo，見 [`raw/README.md`](raw/README.md)。

## 3. 教學 HTML 簡報
[`slides/index.html`](slides/index.html)（31 頁；左右鍵翻頁；每頁有「Wiki 依據」與中英對照單字表）。啟用 GitHub Pages 後：`https://<帳號>.github.io/<repo>/slides/`

## 4. Loop／Graph
流程圖與說明見 [`report/index.html`](report/index.html)：① 讀 index → ② 查 Wiki → ③ 大綱 → ④ 草稿（論點＋出處）→ ⑤ 檢查 → ⑥ 生成 HTML → ⑦ 視覺檢查。③④⑤ 為小圈；缺資料時回 Ingest 為大圈。

## 5. 一次實際執行的檢查紀錄
見 [`wiki/分析-簡報檢查報告.md`](wiki/分析-簡報檢查報告.md)：31 頁、170 條論點，論點→Wiki 原文字串檢查失敗 0，簡報數字須出現在 Wiki 的檢查失敗 0；渲染截圖檢查數頁；完整 Lint 跑過一次（56 頁）。檢查程式在 `schema/`。

## 6. 反思
見 `report/index.html` 的 Step 4。摘要：最常出錯的是 Ingest 的讀取與抄寫（PDF 文字抽取弄壞符號、頁碼／圖號誤植），所以把數值核對提早到讀取當下、把連結與欄位檢查改成每次寫入後自動跑。

## 已知限制
- 6 份來源出自 2 本書，以 Zumdahl 為主；大多數頁面信心程度為「中」。
- 自動檢查是寬鬆的字串比對（論點與字串同一人寫），建議另有人對照課本抽查。
- 未解決：H–H 的 −458 與 432 kJ/mol；N≡N 的 941 與 942；晶格能兩本書符號相反（已說明）、數值差約 2%。
