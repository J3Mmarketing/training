---
name: j3m-github-publish
description: 將 J3M 的課程教材、互動工具或 demo 網頁上傳到 GitHub（J3Mmarketing/training）並發布到教學資源站 https://j3mmarketing.github.io/training/ 時使用。涵蓋分支規則、資料夾結構、首頁卡片與分類格式、提交身分、推送後驗證，以及理財規劃器各版本的同步規則。只要使用者提到「上傳 GitHub」「放到教學資源站」「加到目錄頁」「更新網站」，就應使用本 skill。
---

# J3M 教學資源站發布規則

## 一、儲存庫與分支

| 項目 | 規則 |
|---|---|
| 儲存庫 | `J3Mmarketing/training` |
| 網站網址 | `https://j3mmarketing.github.io/training/` |
| 發布分支 | **`gh-pages`**：網站只從這個分支發布，所有要上線的內容都推到這裡 |
| `main` 分支 | 僅作備份，不會出現在網站上。README.md 是舊版教材，不是目錄頁 |

- 不要以為 `main` 的 README 是目錄頁。真正的目錄頁是 `gh-pages` 的 `index.html`（標題「J3M 教學資源站」，2026/11 起為網站形式的首頁）。
- 動手前先 `git fetch origin gh-pages`，確認目前收錄了哪些卡片與資料夾。

## 二、資料夾結構

每一份教材或工具各自放在一個資料夾，入口固定為 `index.html`：

```
gh-pages/
├── index.html            ← 首頁（網站形式的目錄頁）
├── about/                ← 關於 J3M
├── aipmp/                ← 課程教材 01
├── ai-evolution/         ← 課程教材 02
├── slide-craft/          ← AI 簡報術 01 簡報技法圖鑑
├── slide-styles/         ← AI 簡報術 02 簡報風格圖鑑
├── shorts-subtitle/      ← 影片製作 01
├── motion-craft/         ← 影片製作 02 動態技法圖鑑
├── finance-planner/      ← Vibe Coding 01
└── ai-knowledge/         ← AI 小知識 01
```

- 資料夾名稱使用小寫英文與連字號（kebab-case），不使用中文或空格。
- 連結一律使用相對路徑，例如 `href="finance-planner/"`；子頁面回首頁使用 `href="../"`。
- 子頁面頂部的 eyebrow 放回首頁連結，格式：`J3M 教學資源站 · 分類名稱 · 英文名稱`。

## 三、首頁新增教材

首頁（2026/11 改版）由五個部分組成：固定導覽列、首屏（標語、搜尋、最新上架）、分類索引卡、各分類區塊、頁尾。目前分類依序為：

| 分類 | 區塊 id | 代表色變數 | 封面英文標籤 |
|---|---|---|---|
| 課程教材 | `course` | `--c-course` | COURSE |
| AI 簡報術 | `slides` | `--c-slides` | SLIDES |
| 影片製作 | `video` | `--c-video` | VIDEO |
| Vibe Coding | `vibe` | `--c-vibe` | VIBE CODING |
| AI 小知識 | `knowledge` | `--c-know` | KNOWLEDGE |

### 3.1 新增卡片

在對應分類的 `<section class="sec" id="…">` 內，於 `<div class="cards">` 的最後一張卡片之後新增，編號依該分類遞增：

```html
      <a class="card" href="資料夾名稱/">
        <div class="cover"><span class="lab">SLIDES</span><span class="badge">NEW</span><span class="no">03</span></div>
        <div class="body"><div class="t">教材標題：一句話副標</div>
        <p class="d">兩到四句說明：解決什麼問題、包含哪些內容、學員能帶走什麼。</p>
        <div class="tags"><span class="tag">標籤一</span><span class="tag">標籤二</span><span class="tag">標籤三</span><span class="tag">標籤四</span></div><span class="go">開啟圖鑑 →</span></div>
      </a>
```

- `lab` 使用上表的封面英文標籤；`no` 為該分類內的兩位數編號。
- `badge`（NEW）只放在最新上架的教材；新增時移除較舊教材的 NEW。
- `go` 的文字依類型：講義「開啟講義 →」、手冊「開啟手冊 →」、圖鑑「開啟圖鑑 →」、工具「開啟工具 →」。外部連結加 `target="_blank" rel="noopener"`，文字改為「前往範例 ↗」。
- 固定四個標籤，以工具名稱或主題關鍵字為主。

### 3.2 同步更新的位置

每新增一份教材，以下三處也要一起改，否則數字會對不上：

1. 該分類標題旁的 `<span class="count">N 份</span>`。
2. 分類索引卡（`<nav class="cats">`）中對應分類的 `<em>N 份</em>`。
3. 首屏「最新上架」（`<aside class="latest">`）：新教材放在第一列並加 NEW，維持三列，移除最舊的一列。

首屏的「份教材」數字由 JavaScript 自動計算，不需手改；「本 AI 圖鑑」數字為手動，新增圖鑑時要加一。

### 3.3 新增分類

1. 在 `:root` 加入新的代表色變數，例如 `--c-ops`（兩個主題共用，不需放進深色區塊）。
2. 導覽列 `.menu` 加入 `<a href="#新id">分類名稱</a>`，放在「關於 J3M」之前。
3. 分類索引卡加一張 `<a class="cat" href="#新id" style="--cc:var(--c-新)">`；超過五類時，把 `.cats` 的欄數 `repeat(5,…)` 改成實際數量或改為兩列。
4. 新增 `<section class="sec" id="新id" style="--cc:var(--c-新)">`，包含 `sec-head`、`cat-note` 與 `cards`。

### 3.4 文案與修改原則

- 文案遵循 J3M 語氣：繁體中文全形標點、英數前後留空格、不使用 emoji、理性專業。
- 不修改既有卡片的內容與順序，除非使用者明確要求。
- 每張卡片最多兩欄並排；手機版自動改為單欄，不需另外處理。
- 修改後在桌機與手機寬度各檢查一次，確認沒有橫向捲動。

## 四、獨立網頁的必要處理

從 claude.ai Artifact 搬到 GitHub Pages 的 HTML，發布前必須補齊：

1. **完整文件骨架**：Artifact 原始檔沒有 `<!doctype html>`、`<html>`、`<head>`、charset 與 viewport，需包上：
   ```html
   <!doctype html>
   <html lang="zh-Hant">
   <head>
   <meta charset="utf-8">
   <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
   <style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
   </head>
   <body>
   ……原始內容……
   </body>
   </html>
   ```
2. **移除對 claude.ai 的依賴**：`window.claude.use(...)` 在 GitHub Pages 不存在。凡是匯出、下載功能，必須有原生下載的備援（`Blob` + `<a download>`）。
3. **外部資源**：字型與函式庫使用 Google Fonts 與 cdnjs，指定確切版本號。

## 五、提交與推送

1. 提交身分固定為：
   ```
   git config user.email noreply@anthropic.com
   git config user.name Claude
   ```
   否則 GitHub 會顯示 Unverified。
2. 提交訊息使用繁體中文，簡述新增或修改的內容，結尾附上當次對話規定的 Co-Authored-By 與 Claude-Session 兩行。
3. 推送前先 `git fetch origin gh-pages` 並 rebase，再 `git push -u origin gh-pages`。
4. 若推送回傳 403（Claude doesn't have GitHub access），請使用者安裝 Claude GitHub App：`https://github.com/apps/claude/installations/select_target`，或到 `https://claude.ai/connect-github` 重新連結。不要改用其他方式繞過。

## 六、推送後驗證

1. 用 `git ls-remote origin gh-pages` 確認遠端的最新提交就是剛推送的那一筆。若本機顯示「尚未推送」但 ls-remote 已是新提交，代表本機追蹤紀錄過期，執行 `git fetch origin +refs/heads/gh-pages:refs/remotes/origin/gh-pages` 更新即可，不要重複推送。
2. 用 `gh run list -R J3Mmarketing/training -L 1` 等待 `pages build and deployment` 顯示 `completed success`，並確認 headSha 與推送的提交一致。
3. 雲端環境無法連線到 `github.io`，無法親自檢查畫面。回報時要如實說明，並請使用者打開目錄頁與新頁面確認。

## 七、理財規劃器的版本規則

| 版本 | 用途 | 可否上傳 GitHub |
|---|---|---|
| personal | 使用者真實財務規劃 | **不可**。只存在 claude.ai 私人頁面與使用者桌機 |
| demo | 上課示範 | 可，發布於 `gh-pages/finance-planner/` |
| public | 提供給不同使用者 | 目前只在 claude.ai，上傳前需使用者同意 |

- 修改 demo 版時，同步更新兩處：claude.ai 的 demo 頁面，以及 `gh-pages/finance-planner/index.html`，保持內容一致。
- 共同功能（例如清除資料）先改 `main` 基礎版本，再合併到 personal、demo、public。
- 備份檔（`.json`）可能含真實財務資料，不納入版本控制。

## 八、回報格式

完成後依序回報：

1. 網站與新頁面的網址
2. 新增或修改了哪些檔案、哪張卡片
3. 部署結果（成功或失敗）
4. 尚未驗證的部分，以及需要使用者確認的事項
