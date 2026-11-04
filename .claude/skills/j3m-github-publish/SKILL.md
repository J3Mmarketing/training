---
name: j3m-github-publish
description: 將 J3M 的課程教材、互動工具或 demo 網頁上傳到 GitHub（J3Mmarketing/training）並發布到教學資源站 https://j3mmarketing.github.io/training/ 時使用。涵蓋分支規則、資料夾結構、首頁主題框與分類頁的產生方式、提交身分、推送後驗證，以及理財規劃器各版本的同步規則。只要使用者提到「上傳 GitHub」「放到教學資源站」「加到目錄頁」「更新網站」，就應使用本 skill。
---

# J3M 教學資源站發布規則

## 一、儲存庫與分支

| 項目 | 規則 |
|---|---|
| 儲存庫 | `J3Mmarketing/training` |
| 網站網址 | `https://j3mmarketing.github.io/training/` |
| 發布分支 | **`gh-pages`**：網站只從這個分支發布，所有要上線的內容都推到這裡 |
| `main` 分支 | 僅作備份，不會出現在網站上。README.md 是舊版教材，不是目錄頁 |

- 不要以為 `main` 的 README 是目錄頁。真正的目錄頁是 `gh-pages` 的 `index.html`（標題「J3M 教學資源站」，由 `_build/build_home.py` 產生的五大主題首頁）。
- 動手前先 `git fetch origin gh-pages`，確認目前收錄了哪些卡片與資料夾。

## 二、資料夾結構

每一份教材或工具各自放在一個資料夾，入口固定為 `index.html`：

```
gh-pages/
├── index.html            ← 首頁：五大主題框架（由 _build 產生，不要手改）
├── topic/                ← 分類頁（由 _build 產生，不要手改）
│   ├── slides/           ← AI 簡報術
│   ├── video/            ← AI 影片
│   ├── vibe/             ← Vibe Coding
│   ├── knowledge/        ← AI 小知識
│   └── course/           ← 課程教材
├── _build/build_home.py  ← 首頁與分類頁的產生器（Jekyll 不會發布底線開頭的資料夾）
├── about/                ← 關於 J3M
├── slide-craft/  slide-styles/        ← AI 簡報術的教材
├── shorts-subtitle/  motion-craft/    ← AI 影片的教材
├── finance-planner/                   ← Vibe Coding 的教材
├── ai-knowledge/                      ← AI 小知識的教材
└── aipmp/  ai-evolution/              ← 課程教材的教材
```

- 資料夾名稱使用小寫英文與連字號（kebab-case），不使用中文或空格。
- 教材資料夾放在根目錄，不放進 `topic/`；連結使用相對路徑。
- 教材頁頂部的 eyebrow 放回首頁連結 `href="../"`，格式：`J3M 教學資源站 · 主題名稱 · 英文名稱`。

## 三、首頁與分類頁

網站分三層：首頁（五個主題框）→ 分類頁 `topic/<主題>/`（該主題的完整教材卡片）→ 教材頁。

- 首頁每個主題框只顯示：編號、主題名稱、一句簡介、三點大綱、「本節收錄」清單（類型、標題、副標）。不放教材的長說明與標籤。
- 分類頁顯示該主題所有教材的完整卡片（類型、標題、副標、說明、四個標籤），底部連到其他主題。
- 主題順序固定為：AI 簡報術、AI 影片、Vibe Coding、AI 小知識、課程教材。

### 3.1 新增教材的步驟

首頁與分類頁都由 `_build/build_home.py` 的 `SECTIONS` 資料產生，**不要直接編輯 `index.html` 或 `topic/` 內的 HTML**。

1. 在對應主題的 `items` 清單最後加入一筆：
   ```python
   dict(href="資料夾名稱/", title="教材標題", sub="一句話副標", kind="圖鑑", new=True,
        desc="兩到四句說明：解決什麼問題、包含哪些內容、學員能帶走什麼。",
        tags=["標籤一","標籤二","標籤三","標籤四"]),
   ```
2. `kind` 使用：圖鑑、手冊、講義、工具、書櫃、範例。外部連結加 `ext=True`，`href` 填完整網址。
3. `new=True` 只給最新上架的教材；新增時移除較舊教材的 `new`。
4. 在 gh-pages 根目錄執行 `python3 _build/build_home.py .`，首頁、分類頁、份數與編號會一起更新。
5. 以桌機與手機寬度各檢查一次首頁與分類頁，確認沒有橫向捲動。

### 3.2 新增或調整主題

- 在 `SECTIONS` 中新增一筆主題：`id`（資料夾名）、`name`、`en`、`color`、`intro`、`outline`（三點大綱）、`items`。
- 主題在清單中的順序就是首頁與導覽列的順序。
- 執行產生器後，`topic/<id>/` 會自動建立；刪除主題時，同時刪除對應的 `topic/<id>/` 資料夾。

### 3.3 文案原則

- 文案遵循 J3M 語氣：繁體中文全形標點、英數前後留空格、不使用 emoji、理性專業。
- 首頁的 `sub` 控制在 15 字左右；長說明只寫在 `desc`。
- 不修改既有教材的內容與順序，除非使用者明確要求。

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
