#!/usr/bin/env python3
"""BlackVault Finance and Research: static site builder. No dependencies.
Write Markdown in content/<area>/NAME.md, then run:  python3 build.py
"""
import os, re, json, html, shutil
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE, MAIN, AGRI = "https://finance.blackvault.co.ke", "https://www.blackvault.co.ke", "https://agri.blackvault.co.ke"
EMAIL, TEL, TELH = "enquiries@blackvault.co.ke", "+254 723 580 914", "+254723580914"
VISION = "To build enterprises of lasting economic value."
e = html.escape
CATS = [("industry", "Industry", "Sector structure, supply chains and operating economics."), ("finance", "Finance", "Markets, capital and financial conditions."), ("economy", "Economy", "Growth, inflation, policy and the forces behind them."), ("regional", "Regional", "Kenya, East Africa and neighbouring markets."), ("global", "Global", "Worldwide markets and the economies that move them."), ("letters", "Letters", "Periodic letters on what we are studying, what we got wrong and what changed our mind."), ("predictions", "Predictions", "Dated, falsifiable forecasts, graded after the fact."), ("analysis", "Analysis", "Longer, evidence-led examinations of a single question.")]
CD = {c[0]: c for c in CATS}
AGENDA = {
 "industry": ["How do staple-food supply chains in East Africa work, from farm to market?", "What are the operating economics of storage and logistics businesses?", "Which sectors turn local demand into durable enterprises?"],
 "finance": ["What does the cost of capital look like for small and medium enterprises in Kenya?", "How do interest-rate cycles change the returns on patient capital?", "What makes capital allocation disciplined rather than merely cautious?"],
 "economy": ["What drives food and fuel prices in Kenya, and how fast do shocks pass through?", "How do currency moves reach households and firms?", "What does public borrowing do to private credit?"],
 "regional": ["Where do prices for the same commodity differ across East African markets, and why?", "What do cross-border trade rules change for producers?", "Which regional infrastructure projects change the economics of whole sectors?"],
 "global": ["How do global commodity and rate cycles reach African markets?", "What does the energy transition change for resource economies?", "Which global technology shifts matter for real industries?"]}
FORMAT = {"letters": "A periodic letter from BlackVault: what we are studying, what we got wrong, and what changed our mind.", "predictions": "Every prediction records the claim, the date, the horizon, the evidence and a confidence level. It is graded when the horizon passes, and the grade is published whether we were right or wrong.", "analysis": "One question, examined at length, with sources named and the conclusion dated."}

def md(text):
    def inline(s):
        s = e(s); s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s); s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
        return re.sub(r"\[(.+?)\]\((https?://[^)\s]+|/[^)\s]*|mailto:[^)\s]+)\)", r'<a href="\2">\1</a>', s)
    out, para, lst, quote = [], [], [], []
    def flush():
        nonlocal para, lst, quote
        if para: out.append("<p>%s</p>" % inline(" ".join(para))); para = []
        if lst: out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % inline(x) for x in lst)); lst = []
        if quote: out.append("<blockquote><p>%s</p></blockquote>" % inline(" ".join(quote))); quote = []
    for line in text.splitlines():
        l = line.rstrip()
        if not l.strip(): flush(); continue
        m = re.match(r"(#{2,3})\s+(.*)", l)
        if m: flush(); n = len(m.group(1)); out.append("<h%d>%s</h%d>" % (n, inline(m.group(2)), n)); continue
        if l.startswith(("- ", "* ")):
            if para or quote: flush()
            lst.append(l[2:]); continue
        if l.startswith("> "):
            if para or lst: flush()
            quote.append(l[2:]); continue
        if lst or quote: flush()
        para.append(l.strip())
    flush(); return "\n".join(out)

def load():
    posts = []
    for cat in CD:
        d = os.path.join(ROOT, "content", cat)
        if not os.path.isdir(d): continue
        for f in sorted(os.listdir(d)):
            if not f.endswith(".md") or f.startswith("_"): continue
            m = re.match(r"---\n(.*?)\n---\n(.*)", open(os.path.join(d, f), encoding="utf-8").read(), re.S)
            if not m: continue
            meta = {}
            for ln in m.group(1).splitlines():
                if ":" in ln: k, v = ln.split(":", 1); meta[k.strip()] = v.strip()
            if meta.get("draft", "").lower() == "true": continue
            meta.update(body=m.group(2).strip(), cat=cat, slug=f[:-3]); meta.setdefault("title", f[:-3]); meta.setdefault("date", "1970-01-01"); meta.setdefault("summary", ""); meta.setdefault("author", "BlackVault Research")
            meta["url"] = "/%s/%s/" % (cat, f[:-3]); posts.append(meta)
    posts.sort(key=lambda p: p["date"], reverse=True); return posts

def graded(p): return p.get("status", "open").lower() in ("correct", "incorrect", "partly correct")

EMB = '<svg class="mark" viewBox="0 0 1200 1200" aria-hidden="true" focusable="false"><g fill="#C5A572"><path fill-rule="evenodd" d="M572 27V572H27ZM536 113V536H113Z"/><path d="M643 68V554H1129Z"/><path d="M69 643H555V1129Z"/><path fill-rule="evenodd" d="M626 626H1171L626 1171ZM662 662V1085L1085 662Z"/></g></svg>'

def page(title, desc, path, body):
    cats = "".join('<li><a href="/%s/">%s</a></li>' % (c[0], c[1]) for c in CATS)
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta name="theme-color" content="#111210">
<link rel="canonical" href="{SITE}{path}"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png"><link rel="alternate" type="application/rss+xml" href="/rss.xml" title="BlackVault Finance and Research">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{SITE}{path}"><meta property="og:image" content="{SITE}/assets/og-image.png"><meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&display=swap" rel="stylesheet"><link rel="stylesheet" href="/assets/css/site.css"></head>
<body class="fin"><a class="skip" href="#main">Skip to content</a><div id="prog"></div>
<header><div class="wrap bar"><a class="word" href="/" aria-label="BlackVault Finance and Research home">BlackVault<span class="subl">Finance and Research</span></a>
<button class="menu" aria-expanded="false" aria-controls="nav"><i aria-hidden="true"></i><span>Menu</span></button>
<nav id="nav" aria-label="Primary"><ul><li><a href="/#areas">Research areas</a></li><li><a href="/#agenda">Agenda</a></li><li><a href="/predictions/">Prediction ledger</a></li><li><a href="/method/">Method</a></li><li class="cta"><a href="/request/">Request research</a></li></ul>
<div class="navfoot">{VISION}<br><a href="mailto:{EMAIL}">{EMAIL}</a></div></nav></div></header>
<main id="main">{body}</main>
<footer><div class="wrap"><div class="ftop"><div><a class="word" href="/">BlackVault</a><p class="vis">{VISION}</p><p class="stat">Finance and Research is a research house in its first stage. Research is general information and is not investment advice.</p></div>
<div><h4>Research areas</h4><ul>{cats}</ul></div>
<div><h4>This site</h4><ul><li><a href="/method/">Method and standards</a></li><li><a href="/predictions/">Prediction ledger</a></li><li><a href="/request/">Request research</a></li><li><a href="/subscribe/">Subscribe</a></li><li><a href="/rss.xml">RSS</a></li><li><a href="/disclaimer/">Disclaimer</a></li></ul></div>
<div><h4>BlackVault</h4><ul><li><a href="{MAIN}">Group website</a></li><li><a href="{MAIN}/corporate/">Corporate</a></li><li><a href="{AGRI}">Agri Ventures</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="tel:{TELH}">{TEL}</a></li></ul></div></div>
<div class="fine"><span>© BlackVault. All rights reserved.</span><span>BlackVault is an early-stage venture group. Nothing here is an offer, solicitation or personal recommendation.</span></div></div></footer>
<script src="/assets/js/site.js" defer></script></body></html>"""

def rows(posts):
    if not posts: return '<p class="empty">Nothing published here yet. Our first pieces are in preparation.</p>'
    out = []
    for p in posts:
        x = ""
        if p["cat"] == "predictions" and p.get("status"): x = '<span class="pill st-%s">%s</span>' % (re.sub(r"\W", "", p["status"].lower()), e(p["status"]))
        out.append(f'<a class="row" href="{p["url"]}"><span class="rd">{e(p["date"])}</span><span class="rt"><strong>{e(p["title"])}</strong><small>{e(p["summary"])}</small></span><span class="rc">{CD[p["cat"]][1]} {x}</span></a>')
    return '<div class="rows">%s</div>' % "".join(out)

def write(path, content):
    full = os.path.join(ROOT, path.strip("/")) if path.endswith((".html", ".xml", ".json", ".txt")) else os.path.join(ROOT, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True); open(full, "w", encoding="utf-8").write(content)

def phero(h, p): return f'<div class="phero"><div class="wrap"><p class="kicker" style="color:#b4b7ae">BlackVault Finance and Research</p><h1>{h}</h1><p>{p}</p></div></div>'

def build():
    # clear generated pages (keep assets and content)
    for d in os.listdir(ROOT):
        if os.path.isdir(os.path.join(ROOT, d)) and d not in ("assets", "content", ".git"): shutil.rmtree(os.path.join(ROOT, d))
    posts = load(); np_ = len(posts); preds = [p for p in posts if p["cat"] == "predictions"]; ng = sum(1 for p in preds if graded(p))
    idx = "".join(f'<a class="row ia" href="/{k}/"><span class="t">{n}</span><span class="d">{d}</span><span class="c">{sum(1 for p in posts if p["cat"] == k)} published</span></a>' for k, n, d in CATS)
    seg = "".join(f'<button type="button" aria-pressed="{"true" if i == 0 else "false"}" aria-controls="ag{i}">{CD[k][1]}</button>' for i, k in enumerate(AGENDA))
    secs = "".join(f'<div class="sector" id="ag{i}"{"" if i == 0 else " hidden"}><p class="lead">{CD[k][2]}</p><p class="label">Questions on our agenda</p><ol class="qs">{"".join("<li><span>%s</span></li>" % q for q in AGENDA[k])}</ol></div>' for i, k in enumerate(AGENDA))
    home = f"""<div class="hero on-dark" id="top">{EMB}<div class="wrap"><p class="kicker">A research house, starting out</p><h1>Research for decisions that last.</h1>
<div class="intro"><p>BlackVault Finance and Research studies industries, finance and economies, from Nairobi to the world. We are at the start, so we show our agenda and our method before our results, and we publish as the work is ready.</p><div class="btns"><a class="btn" href="#agenda">Our agenda</a><a class="btn ghost" href="/method/">How we work</a></div></div>
<div class="status"><span>Launching</span><span>Nairobi, Kenya</span><span>{np_} publications</span><span>{len(preds)} predictions recorded</span></div></div></div>
<section id="areas"><div class="wrap"><div class="split"><div><p class="kicker">Coverage</p><h2>Eight research areas</h2></div><p class="lead">Industry, finance, economy, regional and global analysis, plus letters, predictions and longer analysis.</p></div><div class="idx">{idx}</div></div></section>
<section id="agenda" class="ivory"><div class="wrap"><div class="split"><div><p class="kicker">Research agenda</p><h2>What we intend to find out</h2></div><p class="lead">These are the questions we are starting with. They are not yet answered, and the agenda will change as we learn.</p></div>
<div class="ix single"><div class="views"><div class="view"><div class="seg" role="group" aria-label="Research areas">{seg}</div>{secs}<p class="note">Planned agenda. Subject to change. Answers appear in Publications as they are completed.</p></div></div></div></div></section>
<section id="latest-sec"><div class="wrap"><div class="split"><div><p class="kicker">Publications</p><h2>Latest research</h2></div><div><input id="q" class="search" type="search" placeholder="Search titles and summaries" aria-label="Search publications"></div></div><div id="latest" style="margin-top:40px">{rows(posts[:12])}</div></div></section>
<section class="on-dark"><div class="wrap"><p class="kicker">Prediction ledger</p><h2 style="font-size:clamp(1.85rem,4.4vw,3.5rem);max-width:18ch;line-height:1.05">We write predictions down, then grade them.</h2>
<div class="counts"><div><b>{len(preds)}</b><span>Predictions recorded</span></div><div><b>{ng}</b><span>Graded</span></div><div><b>{len(preds) - ng}</b><span>Open</span></div></div>
<p class="sub-dk">Every entry carries a date, a horizon, the evidence and a confidence level. The ledger is public from the first entry, and wrong calls stay on it.</p><div class="btns" style="margin-top:28px"><a class="btn" href="/predictions/">Open the ledger</a></div></div></section>
<section class="ivory"><div class="wrap"><div class="split"><div><p class="kicker">Method</p><h2>How we hold ourselves to account</h2></div><p class="lead">A new research house earns trust by being checkable.</p></div>
<div class="rules"><div><h3>Sources named</h3><p>Every piece lists its sources and the date each was accessed.</p></div><div><h3>Conclusions dated</h3><p>We say what we concluded and when, so changes of mind are visible.</p></div><div><h3>Confidence stated</h3><p>High, moderate or low, defined on the method page.</p></div><div><h3>Predictions graded</h3><p>Correct, partly correct or incorrect, published openly.</p></div><div><h3>Errors corrected</h3><p>Openly, with a dated note.</p></div><div><h3>Interests disclosed</h3><p>Where BlackVault or a venture has a stake, the piece says so.</p></div></div>
<div class="btns" style="margin-top:40px"><a class="btn" href="/method/">Read the method</a></div></div></section>
<section><div class="wrap split"><div><p class="kicker">Work with us</p><h2>Ask us a question</h2></div><div><p class="lead">If there is a question you need researched, a dataset we should see, or an error we should correct, tell us.</p><div class="btns" style="margin-top:28px"><a class="btn" href="/request/">Request research</a><a class="btn ghost" href="/subscribe/">Subscribe</a></div></div></div></section>"""
    write("/", page("BlackVault Finance and Research | A research house in Nairobi", "BlackVault Finance and Research studies industries, finance and economies, from Nairobi to the world. Research agenda, method and prediction ledger.", "/", home))
    for k, n, d in CATS:
        ps = [p for p in posts if p["cat"] == k]
        if k in AGENDA: intro = '<p class="label">On our agenda</p><ol class="qs">%s</ol>' % "".join("<li><span>%s</span></li>" % q for q in AGENDA[k])
        else: intro = '<p class="label">Format</p><p class="lead" style="max-width:40rem">%s</p>' % FORMAT[k]
        body = phero(n, d) + f'<section><div class="wrap">{intro}<h2 style="font-size:clamp(1.5rem,2.6vw,2rem);margin:56px 0 24px">Publications</h2>{rows(ps)}</div></section>'
        write("/%s/" % k, page(f"{n} | BlackVault Finance and Research", d, "/%s/" % k, body))
    # ledger
    if preds:
        trs = "".join(f'<tr><td>{e(p["date"])}</td><td><a href="{p["url"]}"><strong>{e(p["title"])}</strong></a></td><td>{e(p.get("horizon", ""))}</td><td>{e(p.get("confidence", ""))}</td><td><span class="pill st-{re.sub(chr(92) + "W", "", p.get("status", "open").lower())}">{e(p.get("status", "Open"))}</span></td></tr>' for p in preds)
        tbl = f'<div class="scroll"><table class="tbl"><thead><tr><th>Date</th><th>Claim</th><th>Horizon</th><th>Confidence</th><th>Status</th></tr></thead><tbody>{trs}</tbody></table></div>'
    else: tbl = '<p class="empty">The ledger is open and has no entries yet. The first prediction will be recorded here with its date, horizon and evidence.</p>'
    anat = "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in [("Claim", "A statement that can be proved wrong."), ("Date", "The day it was recorded. Entries are never back-dated."), ("Horizon", "When it will be graded."), ("Evidence", "What the claim rests on, with sources."), ("Confidence", "High, moderate or low."), ("What would change our mind", "Stated in advance."), ("Grade", "Correct, partly correct or incorrect, with a dated note.")])
    led = phero("Prediction ledger", "Our forecasts, written down, dated and graded.") + f'<section><div class="wrap"><div class="counts light"><div><b>{len(preds)}</b><span>Recorded</span></div><div><b>{ng}</b><span>Graded</span></div><div><b>{len(preds) - ng}</b><span>Open</span></div></div><div style="margin-top:48px">{tbl}</div></div></section><section class="ivory"><div class="wrap split"><div><p class="kicker">Entry format</p><h2>What every entry contains</h2></div><dl class="anat">{anat}</dl></div></section>'
    write("/predictions/", page("Prediction ledger | BlackVault Finance and Research", "Dated, falsifiable forecasts from BlackVault Research, graded after the fact.", "/predictions/", led))
    for p in posts:
        meta = f'<span>{e(p["date"])}</span><span>{CD[p["cat"]][1]}</span><span>{e(p["author"])}</span>' + "".join(f"<span>{k.title()}: {e(p[k])}</span>" for k in ("horizon", "confidence", "status") if p.get(k))
        b = f'<article class="art"><div class="wrap"><a href="/{p["cat"]}/" class="back">{CD[p["cat"]][1]}</a><h1>{e(p["title"])}</h1><div class="meta">{meta}</div><div class="prose">{md(p["body"])}</div><p class="note">General information, not investment advice. See the <a href="/disclaimer/">disclaimer</a>.</p></div></article>'
        write(p["url"], page(p["title"] + " | BlackVault", p["summary"] or p["title"], p["url"], b))
    method_rows = [("Sources", "Primary data and documents first, then official statistics, then reputable secondary sources. Opinion comes last and is labelled. Every piece names its sources and the date each was accessed."), ("Confidence", "High: strong evidence from several independent sources. Moderate: reasonable evidence with gaps. Low: thin or conflicting evidence, stated plainly."), ("Dating", "Each piece carries a date. Material updates are added as dated notes, and the original text is not silently changed."), ("Predictions", "Written down with a claim, date, horizon, evidence and confidence. Graded when the horizon passes, whether right or wrong."), ("Corrections", "Errors are corrected openly with a dated note. Send corrections to " + EMAIL + "."), ("Independence", "Research is written to inform. Where BlackVault or one of its ventures has an interest in a subject, the piece says so."), ("Limits", "BlackVault is an early-stage group. Research is general information, not investment advice. See the disclaimer.")]
    mp = phero("Method and standards", "How BlackVault Research sources, dates, grades and corrects its work.") + '<section><div class="wrap"><div class="rules one">' + "".join(f"<div><h3>{a}</h3><p>{b}</p></div>" for a, b in method_rows) + "</div></div></section>"
    write("/method/", page("Method and standards | BlackVault Finance and Research", "How BlackVault Research sources, dates, grades and corrects its work.", "/method/", mp))
    req = phero("Request research", "Tell us what you need to understand.") + f'<section><div class="wrap"><div class="idx">' + "".join(f'<a class="row ia" href="mailto:{EMAIL}?subject={s}"><span class="t">{t}</span><span class="d">{d}</span><span class="c">Email us</span></a>' for t, d, s in [("Ask a research question", "A topic, sector or market you need studied. We will say honestly whether it fits our agenda.", "Research%20request"), ("Share data or a document", "A dataset, filing or source we should see.", "Data%20or%20document"), ("Report a correction", "An error in anything we have published.", "Correction")]) + '</div></div></section>'
    write("/request/", page("Request research | BlackVault Finance and Research", "Ask BlackVault a research question, share data or report a correction.", "/request/", req))
    disc = phero("Disclaimer", "Please read before relying on any publication.") + '<section><div class="wrap"><div class="prose"><p>BlackVault Finance and Research publishes general information and opinion. It is not investment, legal, tax or accounting advice, and it is not an offer or solicitation to buy or sell any security or product.</p><p>Forecasts and predictions are uncertain and may prove wrong. Past performance is not a guide to future results. Readers should seek independent professional advice before making decisions.</p><p>BlackVault is an early-stage venture group. This website does not claim any regulatory authorisation to provide investment services.</p></div></div></section>'
    write("/disclaimer/", page("Disclaimer | BlackVault Finance and Research", "Disclaimer for BlackVault Finance and Research publications.", "/disclaimer/", disc))
    sub = phero("Subscribe", "Receive research and letters by email or RSS.") + f'<section><div class="wrap"><p class="lead" style="max-width:36rem">Email us to join the distribution list.</p><div class="btns" style="margin-top:28px"><a class="btn" href="mailto:{EMAIL}?subject=Subscribe%20to%20BlackVault%20Research">Request subscription</a><a class="btn ghost" href="/rss.xml">Follow by RSS</a></div></div></section>'
    write("/subscribe/", page("Subscribe | BlackVault Finance and Research", "Subscribe to BlackVault research and letters.", "/subscribe/", sub))
    write("/404.html", page("Page not found | BlackVault", "Page not found.", "/404.html", phero("Page not found", "The page may have moved.") + '<section><div class="wrap"><a class="btn" href="/">Back to home</a></div></section>'))
    urls = ["/"] + ["/%s/" % c[0] for c in CATS] + ["/method/", "/request/", "/disclaimer/", "/subscribe/"] + [p["url"] for p in posts]
    write("/sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    write("/search.json", json.dumps([{"t": p["title"], "s": p["summary"], "u": p["url"], "d": p["date"], "c": CD[p["cat"]][1]} for p in posts]))
    items = "".join(f"<item><title>{e(p['title'])}</title><link>{SITE}{p['url']}</link><guid>{SITE}{p['url']}</guid><description>{e(p['summary'])}</description></item>" for p in posts[:30])
    write("/rss.xml", f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>BlackVault Finance and Research</title><link>{SITE}</link><description>Research, analysis, letters and predictions.</description>{items}</channel></rss>')
    write("/robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    print("Built %d publications, %d pages" % (np_, len(urls) + 1))
if __name__ == "__main__": build()
