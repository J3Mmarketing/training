#!/usr/bin/env python3
"""J3M 教學資源站：產生首頁 index.html 與五個分類頁 topic/<id>/index.html
用法：在 gh-pages 根目錄執行  python3 _build/build_home.py .
新增教材或分類時只改 SECTIONS，再重新執行。"""
import sys, os, html
ROOT = sys.argv[1]

SECTIONS = [
 dict(id="slides", name="AI 簡報術", en="SLIDES", color="#B8860B",
  intro="從版面靈感到 AI 協作：先看懂好簡報的結構與風格，再把需求寫清楚交給 AI 製作。",
  outline=["版式構圖：一頁簡報怎麼排", "視覺風格：整份簡報怎麼定調", "AI 協作：把需求寫成提示詞"],
  items=[
   dict(href="slide-craft/", title="簡報技法圖鑑", sub="51 種平面版式與 AI 提示詞", kind="圖鑑",
    desc="收錄版面構圖、文字排版、色彩運用、數據呈現、圖像處理、圖解結構、重點強調、封面章節八大類共 51 種技法，每一種都附 16:9 版面示意、適用情境、製作步驟與常見錯誤。填入簡報主題即可複製提示詞，也能勾選多種技法，一次產出整份簡報的組合提示詞。",
    tags=["簡報設計","版面構圖","數據呈現","AI 提示詞"]),
   dict(href="slide-styles/", title="簡報風格圖鑑", sub="40 種視覺風格與配色字體", kind="圖鑑", new=True,
    desc="收錄極簡、編輯排印、商務專業、科技未來、大膽前衛、復古、手作插畫、自然東方八大類共 40 種簡報風格，每一種都有封面示意、色票、字體建議與版面要點。點色票可複製色碼，勾選多種風格即可產生「風格比稿」提示詞，讓 AI 一次做出幾個方向供你挑選。",
    tags=["簡報風格","配色","字體","AI 提示詞"]),
  ]),
 dict(id="video", name="AI 影片", en="VIDEO", color="#2B2D42",
  intro="從拍完到上架之間的實作流程：字幕、特效與自動化處理。",
  outline=["字幕：切分、樣式與燒錄", "特效：101 項動態與時間軸規劃", "自動化：去背、轉場與批次渲染"],
  items=[
   dict(href="shorts-subtitle/", title="短影音上字幕實戰手冊", sub="FFmpeg 與 ASS 字幕完整流程", kind="手冊",
    desc="用 FFmpeg 與 ASS 字幕製作直式短影音字幕的完整流程：語句邊界偵測、字卡切分、樣式設定、燒錄畫面、響度正規化，附常見坑速查與學員練習。",
    tags=["FFmpeg","ASS 字幕","短影音","自動化"]),
   dict(href="motion-craft/", title="動態技法圖鑑", sub="101 項影片特效與 AI 提示詞", kind="圖鑑", new=True,
    desc="整合 J3M 特效庫 30 項、HyperFrames 十二式、去背與轉場、外部 51 式特效包與片尾規格，共 101 項影片特效，每一項都有循環動態示意、實作要點與執行指令。可依影片段落與用途篩選，勾選多項即可產生整支影片的特效時間軸提示詞；另附 319 項網頁動態索引。",
    tags=["影片特效","HyperFrames","去背疊層","AI 提示詞"]),
  ]),
 dict(id="vibe", name="Vibe Coding", en="VIBE CODING", color="#1F6F5C",
  intro="用對話做出可以直接使用的工具與小應用，不必自己寫程式。",
  outline=["用對話描述需求", "讓 AI 產出可用的工具", "發布成網頁與他人分享"],
  items=[
   dict(href="finance-planner/", title="目標理財規劃器", sub="用 AI 開發的複利試算工具", kind="工具",
    desc="設定民國幾年要存到多少錢，組合市值型、高股息、主動式、美股 ETF 與定存，系統依過去 5 年回測報酬算出每月應存金額，並呈現保守、中性、樂觀三種情境。可逐月記錄實際投入與市值，自動重新試算剩餘期間的存款目標，明細可匯出 CSV。資料只存在使用者自己的瀏覽器。",
    tags=["複利試算","ETF 回測","情境分析","課堂示範"]),
   dict(href="https://sites.google.com/view/1000-vocabulary-que/full-page-embed", ext=True, title="用 Gemini 做互動小遊戲", sub="從對話直接匯出成網站", kind="範例",
    desc="➊ 在 Gemini 用對話做出一個互動式應用，例如「課程選擇小測驗」。<br>➋ 在產出的應用上找到匯出到 Google Sites 的選項。<br>➌ 系統會建立一份私人網站草稿，檢查過再決定要不要發布。<br>省掉自己架站與複製貼上程式碼，從對話到網頁草稿一次完成。範例是一款 1000 題的英語拼字闖關遊戲。",
    tags=["Gemini","Google Sites","互動應用","免寫程式"]),
  ]),
 dict(id="knowledge", name="AI 小知識", en="KNOWLEDGE", color="#7A4E2D",
  intro="依工具整理的行銷圖卡，點選書本即可翻閱各工具的最新重點。",
  outline=["依工具分類成書", "圖卡式重點整理", "翻頁快速回顧"],
  items=[
   dict(href="ai-knowledge/", title="J3M AI 小知識書櫃", sub="154 張行銷圖卡，依工具分類", kind="書櫃",
    desc="收錄 Claude、ChatGPT、Google Gemini、Gemini Notebook、Notion、Microsoft Copilot 等工具共 154 張行銷圖卡，分為 8 本書、44 則貼文。點選工具即可抽出該書，列出相關貼文，再以翻頁方式逐張檢視圖卡，適合快速回顧各工具的功能更新與操作要點。",
    tags=["Claude","Gemini","Notion","行銷圖卡"]),
  ]),
 dict(id="course", name="課程教材", en="COURSE", color="#1F3A5F",
  intro="搭配實體課程的完整講義，附操作步驟、提示詞與常見錯誤排除。",
  outline=["訓練行政的 AI 實務", "AI Agent 與工作流", "可直接套用的提示詞"],
  items=[
   dict(href="aipmp/", title="善用 AI 工具提升訓練行政效率", sub="NotebookLM 與 Gemini 行政實務", kind="講義",
    desc="NotebookLM 知識資料庫、Gemini 公文起草、DM 製作、Google Sheets 數據分析、Gemini Canvas 自動化報告。六個章節帶訓練行政人員把重複作業交給 AI，附資料庫建置流程與可直接套用的提示詞。",
    tags=["NotebookLM","Gemini","職訓行政","公文撰寫"]),
   dict(href="ai-evolution/", title="AI 工具進化論", sub="打造你的高效職場力", kind="講義",
    desc="從問 AI 升級到讓 AI 做事。Agent 的五個組成、Claude 與 ChatGPT 與 Gemini 三平台 Skills 比較、API 與連接器與 MCP 的差別，以及七個實際在跑的工作流。附 LINE 提醒小助理、Google 表單儀表板與目標設定三個系統化案例。",
    tags=["AI Agent","Skills","MCP","工作流"]),
  ]),
]

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700&family=Noto+Sans+TC:wght@400;500;700;900&family=Noto+Serif+TC:wght@700;900&display=swap">'

CSS = """
:root{
  --paper:#F5F7FA; --surface:#FFFFFF; --surface-2:#EDF0F5;
  --ink:#14171C; --ink-2:#3C4452; --muted:#66707F;
  --line:#D8DEE7; --accent:#F5B800; --accent-text:#8A6400;
  --shadow:0 1px 2px rgba(20,23,28,.06), 0 10px 28px -14px rgba(20,23,28,.22);
  --f-disp:"Noto Serif TC",Georgia,serif; --f-body:"Noto Sans TC","PingFang TC","Microsoft JhengHei",system-ui,sans-serif; --f-mono:"JetBrains Mono",ui-monospace,monospace;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --paper:#0E1116; --surface:#161A21; --surface-2:#1D222B;
    --ink:#E9ECF1; --ink-2:#C2C9D4; --muted:#8A94A3;
    --line:#2A313C; --accent:#F5B800; --accent-text:#F5B800;
    --shadow:0 1px 2px rgba(0,0,0,.4), 0 12px 30px -16px rgba(0,0,0,.8);
  }
}
:root[data-theme="dark"]{
  --paper:#0E1116; --surface:#161A21; --surface-2:#1D222B;
  --ink:#E9ECF1; --ink-2:#C2C9D4; --muted:#8A94A3;
  --line:#2A313C; --accent:#F5B800; --accent-text:#F5B800;
  --shadow:0 1px 2px rgba(0,0,0,.4), 0 12px 30px -16px rgba(0,0,0,.8);
}
*{box-sizing:border-box}
[hidden]{display:none!important}
html{scroll-behavior:smooth;scroll-padding-top:80px}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--f-body);font-size:16px;line-height:1.75;-webkit-font-smoothing:antialiased}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:30;background:var(--surface)}
a{color:inherit}
:focus-visible{outline:3px solid var(--accent);outline-offset:3px}
.wrap{max-width:1120px;margin:0 auto;padding-left:max(20px,env(safe-area-inset-left,0px));padding-right:max(20px,env(safe-area-inset-right,0px))}
.nav{position:sticky;top:env(safe-area-inset-top,0px);z-index:20;background:var(--surface);border-bottom:1px solid var(--line)}
.nav .wrap{display:flex;align-items:center;gap:20px;min-height:64px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;font-weight:900;white-space:nowrap}
.brand .mk{width:32px;height:32px;border-radius:8px;background:var(--accent);color:#14171C;display:grid;place-items:center;font-family:var(--f-mono);font-size:12px;font-weight:700}
.menu{display:flex;gap:2px;overflow-x:auto;scrollbar-width:none;margin-left:auto}
.menu::-webkit-scrollbar{display:none}
.menu a{text-decoration:none;font-size:14px;font-weight:500;color:var(--ink-2);padding:6px 12px;border-radius:99px;white-space:nowrap}
.menu a:hover,.menu a[aria-current="page"]{background:var(--surface-2);color:var(--ink)}
.menu a.about{border:1px solid var(--line);margin-left:6px}
@media (max-width:760px){.nav .wrap{flex-wrap:wrap;gap:4px;padding-block:10px}.menu{margin-left:0;width:100%}}
.eyebrow{font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:var(--muted);font-weight:700;margin:0 0 10px}
.eyebrow a{text-decoration:none;border-bottom:1px solid var(--line)}
h1{font-family:var(--f-disp);font-weight:900;line-height:1.2;margin:0 0 12px;letter-spacing:-.01em;text-wrap:balance}
h1 .hl{background:linear-gradient(transparent 62%,var(--accent) 62%,var(--accent) 92%,transparent 92%);padding-inline:2px}
.lede{font-size:17px;color:var(--ink-2);margin:0;max-width:40em}
footer{margin-top:72px;background:var(--surface);border-top:1px solid var(--line)}
footer .wrap{padding-block:32px calc(32px + env(safe-area-inset-bottom,0px));display:flex;flex-wrap:wrap;justify-content:space-between;gap:16px 32px;font-size:13.5px;color:var(--muted)}
footer p{margin:0;max-width:62ch}
footer b{color:var(--ink)}
footer nav{display:flex;flex-wrap:wrap;gap:16px;align-items:flex-start}
footer .wrap{align-items:flex-start}
footer nav a{color:var(--ink-2);text-decoration:none;border-bottom:1px solid var(--line)}
@media (prefers-reduced-motion:reduce){*{transition:none!important}html{scroll-behavior:auto}}
"""

HOME_CSS = """
.hero{padding-block:56px 36px}
.hero h1{font-size:clamp(34px,5.4vw,54px)}
.jump{display:flex;flex-wrap:wrap;gap:8px;margin-top:22px;padding:0;list-style:none}
.jump a{display:inline-flex;align-items:center;gap:8px;text-decoration:none;font-size:14px;font-weight:700;background:var(--surface);border:1px solid var(--line);border-radius:99px;padding:6px 14px 6px 8px}
.jump a:hover{border-color:var(--ink)}
.jump i{width:22px;height:22px;border-radius:50%;background:var(--cc);color:#fff;display:grid;place-items:center;font-style:normal;font-family:var(--f-mono);font-size:11px}
.frames{display:grid;gap:22px}
.frame{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);background:var(--surface);border:1px solid var(--line);border-radius:18px;overflow:hidden;box-shadow:var(--shadow)}
.frame .lead{padding:28px 30px;border-left:8px solid var(--cc);display:flex;flex-direction:column;gap:12px}
.frame .top{display:flex;align-items:baseline;gap:12px}
.frame .no{font-family:var(--f-mono);font-size:13px;font-weight:700;color:var(--muted)}
.frame .en{font-size:11.5px;letter-spacing:.18em;font-weight:700;color:var(--muted)}
.frame h2{font-family:var(--f-disp);font-weight:900;font-size:30px;line-height:1.25;margin:0}
.frame h2 a{text-decoration:none}
.frame h2 a:hover{color:var(--accent-text)}
.frame .intro{margin:0;color:var(--ink-2);font-size:15px}
.outline{list-style:none;margin:0;padding:0;display:grid;gap:4px;font-size:14.5px}
.outline li{display:grid;grid-template-columns:24px 1fr}
.outline b{color:var(--accent-text);font-weight:500}
.enter{margin-top:auto;font-size:14px;font-weight:700;color:var(--accent-text);text-decoration:none;align-self:flex-start;border-bottom:2px solid var(--accent)}
.enter:hover{color:var(--ink)}
.frame .list{background:var(--surface-2);padding:22px 26px;display:flex;flex-direction:column}
.list h3{margin:0 0 8px;font-size:12px;letter-spacing:.2em;color:var(--muted);font-weight:700}
.item{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:14px;align-items:center;text-decoration:none;padding:14px 0;border-top:1px solid var(--line)}
.item:first-of-type{border-top:0}
.item .k{font-size:11.5px;font-weight:700;color:#fff;background:var(--cc);border-radius:6px;padding:2px 8px;white-space:nowrap}
.item b{display:block;font-size:16px;line-height:1.45}
.item small{display:block;font-size:13px;color:var(--muted);line-height:1.5}
.item .ar{font-size:15px;color:var(--muted);white-space:nowrap}
.item .new{font-size:10.5px;font-weight:700;background:var(--accent);color:#14171C;border-radius:99px;padding:0 7px;margin-left:6px;vertical-align:2px}
.item:hover b{color:var(--accent-text)}
.item:hover .ar{color:var(--accent-text)}
@media (max-width:820px){.frame{grid-template-columns:minmax(0,1fr)}.frame .lead{border-left:0;border-top:8px solid var(--cc);padding:22px}.frame .list{padding:16px 22px}}
"""

TOPIC_CSS = """
.hero{padding-block:44px 28px;border-bottom:1px solid var(--line);display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:36px;align-items:end}
.hero h1{font-size:clamp(32px,5vw,48px)}
.hero .bar{width:56px;height:8px;border-radius:4px;background:var(--cc);margin-bottom:16px}
.outline{padding:20px 22px;background:var(--surface);border:1px solid var(--line);border-radius:14px;font-size:15px}
.outline ul{list-style:none;margin:0;padding:0;display:grid;gap:6px}
.outline h2{margin:0 0 4px;font-size:12px;letter-spacing:.2em;color:var(--muted);font-weight:700}
.outline li{display:grid;grid-template-columns:24px 1fr}
.outline b{color:var(--accent-text);font-weight:500}
@media (max-width:760px){.hero{grid-template-columns:minmax(0,1fr);gap:20px}}
.cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px;padding-top:32px}
@media (max-width:760px){.cards{grid-template-columns:minmax(0,1fr)}}
.card{display:flex;flex-direction:column;text-decoration:none;background:var(--surface);border:1px solid var(--line);border-radius:16px;overflow:hidden;box-shadow:var(--shadow);transition:transform .2s;min-width:0}
.card:hover{transform:translateY(-3px)}
.cover{position:relative;height:110px;background:var(--cc);color:#fff;overflow:hidden}
.cover::before{content:"";position:absolute;right:-30px;top:-40px;width:180px;height:180px;border-radius:50%;border:26px solid rgba(255,255,255,.1)}
.cover .lab{position:absolute;left:20px;top:16px;font-size:11.5px;letter-spacing:.18em;font-weight:700;opacity:.85}
.cover .kind{position:absolute;left:20px;bottom:16px;font-size:12px;font-weight:700;background:rgba(255,255,255,.18);border-radius:6px;padding:2px 10px}
.cover .no{position:absolute;right:20px;bottom:6px;font-family:var(--f-mono);font-size:54px;font-weight:700;line-height:1;opacity:.92}
.cover .new{position:absolute;left:20px;top:40px;font-size:11px;font-weight:700;background:var(--accent);color:#14171C;border-radius:99px;padding:1px 9px}
.body{padding:20px 22px 22px;display:flex;flex-direction:column;flex:1}
.card .t{font-family:var(--f-disp);font-weight:700;font-size:21px;line-height:1.4;margin:0 0 2px}
.card .s{font-size:14px;color:var(--muted);margin:0 0 10px}
.card .d{font-size:14.5px;color:var(--ink-2);margin:0}
.tags{display:flex;flex-wrap:wrap;gap:7px;margin-top:14px}
.tag{font-size:11.5px;font-weight:700;color:var(--muted);background:var(--surface-2);border:1px solid var(--line);border-radius:99px;padding:3px 11px}
.go{margin-top:auto;padding-top:16px;font-size:14px;font-weight:700;color:var(--accent-text)}
.others{margin-top:48px;padding-top:24px;border-top:1px solid var(--line)}
.others h2{font-size:12px;letter-spacing:.2em;color:var(--muted);font-weight:700;margin:0 0 12px}
.others div{display:flex;flex-wrap:wrap;gap:8px}
.others a{text-decoration:none;font-size:14px;font-weight:700;background:var(--surface);border:1px solid var(--line);border-left:5px solid var(--oc);border-radius:10px;padding:8px 14px}
.others a:hover{border-color:var(--ink);border-left-color:var(--oc)}
"""

E = html.escape
def go_text(it):
    return "前往範例 ↗" if it.get("ext") else {"圖鑑":"開啟圖鑑 →","手冊":"開啟手冊 →","工具":"開啟工具 →","講義":"開啟講義 →","書櫃":"開啟書櫃 →"}.get(it["kind"],"開啟 →")
def href(it, prefix):
    return it["href"] if it.get("ext") else prefix + it["href"]
def attrs(it):
    return ' target="_blank" rel="noopener"' if it.get("ext") else ""
def menu(prefix, current=None):
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{prefix}topic/{s["id"]}/"{cur if s["id"]==current else ""}>{s["name"]}</a>' for s in SECTIONS)
    return f'''<nav class="nav" aria-label="主要導覽">
  <div class="wrap">
    <a class="brand" href="{prefix or "./"}"><span class="mk">J3M</span>教學資源站</a>
    <div class="menu">{links}<a class="about" href="{prefix}about/">關於 J3M</a></div>
  </div>
</nav>'''
def footer(prefix):
    return f'''<footer>
  <div class="wrap">
    <p><b>J3M 數學行銷人</b>｜AI 工具教學與行銷自動化顧問。本站以 GitHub Pages 靜態託管，內容持續增補；手冊中的參數取自實際專案，請依自己的素材重新推導。</p>
    <nav aria-label="站外連結"><a href="{prefix}about/">關於 J3M</a><a href="https://www.youtube.com/@J3M_AI" target="_blank" rel="noopener">YouTube @J3M_AI</a><a href="https://www.threads.com/@j3m_ai" target="_blank" rel="noopener">Threads @j3m_ai</a></nav>
  </div>
</footer>'''
def page(title, desc, css, body):
    return f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light dark">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="J3M 數學行銷人">
{FONTS}
<style>{CSS}{css}</style>
</head>
<body>
{body}
</body>
</html>
'''

# ---------- 首頁 ----------
frames = []
for i, s in enumerate(SECTIONS, 1):
    items = "".join(f'''
        <a class="item" href="{href(it,"")}"{attrs(it)}><span class="k">{it["kind"]}</span><span><b>{it["title"]}{'<span class="new">NEW</span>' if it.get("new") else ""}</b><small>{it["sub"]}</small></span><span class="ar">{"↗" if it.get("ext") else "→"}</span></a>''' for it in s["items"])
    outline = "".join(f'<li><b>{"➊➋➌➍➎"[j]}</b><span>{o}</span></li>' for j, o in enumerate(s["outline"]))
    frames.append(f'''
    <section class="frame" id="{s["id"]}" style="--cc:{s["color"]}">
      <div class="lead">
        <div class="top"><span class="no">0{i}</span><span class="en">{s["en"]}</span></div>
        <h2><a href="topic/{s["id"]}/">{s["name"]}</a></h2>
        <p class="intro">{s["intro"]}</p>
        <ul class="outline">{outline}</ul>
        <a class="enter" href="topic/{s["id"]}/">進入{s["name"]}（{len(s["items"])} 份）→</a>
      </div>
      <div class="list">
        <h3>本節收錄</h3>{items}
      </div>
    </section>''')
jump = "".join(f'<li><a href="#{s["id"]}" style="--cc:{s["color"]}"><i>{i}</i>{s["name"]}</a></li>' for i, s in enumerate(SECTIONS, 1))
home = f'''{menu("")}
<div class="wrap">
  <header class="hero">
    <p class="eyebrow">J3M 數學行銷人 · Math · Marketing · Management</p>
    <h1>教學資源站<span class="hl">．</span></h1>
    <p class="lede">課程講義以外的延伸內容都在這裡，分成五個主題。先看每一節的大綱，再點進去找需要的教材。</p>
    <ul class="jump">{jump}</ul>
  </header>
  <main class="frames">{"".join(frames)}
  </main>
</div>
{footer("")}'''
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(
    page("J3M 教學資源站", "J3M 數學行銷人的課程補充教材、實作手冊與 AI 工具圖鑑。", HOME_CSS, home))

# ---------- 分類頁 ----------
for i, s in enumerate(SECTIONS, 1):
    cards = "".join(f'''
    <a class="card" href="{href(it,"../../")}"{attrs(it)}>
      <div class="cover"><span class="lab">{s["en"]}</span>{'<span class="new">NEW</span>' if it.get("new") else ""}<span class="kind">{it["kind"]}</span><span class="no">{n:02d}</span></div>
      <div class="body"><div class="t">{it["title"]}</div><p class="s">{it["sub"]}</p>
      <p class="d">{it["desc"]}</p>
      <div class="tags">{"".join(f'<span class="tag">{t}</span>' for t in it["tags"])}</div><span class="go">{go_text(it)}</span></div>
    </a>''' for n, it in enumerate(s["items"], 1))
    outline = "".join(f'<li><b>{"➊➋➌➍➎"[j]}</b><span>{o}</span></li>' for j, o in enumerate(s["outline"]))
    others = "".join(f'<a href="../{o["id"]}/" style="--oc:{o["color"]}">{o["name"]}</a>' for o in SECTIONS if o["id"] != s["id"])
    body = f'''{menu("../../", s["id"])}
<div class="wrap" style="--cc:{s["color"]}">
  <header class="hero">
    <div>
      <p class="eyebrow"><a href="../../">J3M 教學資源站</a> · 0{i} {s["en"]}</p>
      <div class="bar"></div>
      <h1>{s["name"]}</h1>
      <p class="lede">{s["intro"]}</p>
    </div>
    <div class="outline"><h2>本節大綱</h2><ul>{outline}</ul></div>
  </header>
  <main class="cards">{cards}
  </main>
  <section class="others"><h2>其他主題</h2><div>{others}</div></section>
</div>
{footer("../../")}'''
    d = os.path.join(ROOT, "topic", s["id"]); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(
        page(f'{s["name"]}｜J3M 教學資源站', s["intro"], TOPIC_CSS, body))
print("ok", len(SECTIONS))
