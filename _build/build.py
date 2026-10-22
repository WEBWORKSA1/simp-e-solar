#!/usr/bin/env python3
"""Simple.solar static site builder.

Run from the repo root:  python3 _build/build.py
Reads page fragments from _build/pages, guides from _build/guides, data from _build/data.py,
and writes finished HTML into the repo root (served as-is by GitHub Pages).
"""
import json, os, re, html, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
B = ROOT / "_build"
import sys; sys.path.insert(0, str(B))
import data as D  # noqa: E402

SITE = "https://simple.solar"
NAME = "Simple.solar"
TODAY = datetime.date.today().isoformat()
UPDATED_HUMAN = datetime.date.today().strftime("%B %Y")
ADSENSE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>'
OWNER = "https://web.works/contact"

NAV = [
    ("quotes", "quotes.html", "Get quotes"),
    ("tools", "tools/index.html", "Calculators"),
    ("guides", "guides/index.html", "Guides"),
    ("states", "states/index.html", "By state"),
    ("videos", "videos.html", "Videos"),
    ("community", "community.html", "Community"),
]

LOGO = ('<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="15" r="7" fill="#FFC23D"/>'
        '<g stroke="#FFC23D" stroke-width="2.4" stroke-linecap="round"><path d="M20 2.5v2.6M8.6 6.8l1.8 1.8M31.4 6.8l-1.8 1.8M4.5 15h2.6M32.9 15h2.6"/></g>'
        '<path d="M6 37 11 24h18l5 13z" fill="currentColor"/><path d="M14.5 24 13 37M25.5 24 27 37M8.5 30.5h23" stroke="var(--bg)" stroke-width="1.6"/></svg>')

ICONS = {
  "roof": '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round" aria-hidden="true"><path d="M6 32 32 10l26 22"/><path d="M12 28v26h40V28"/><path d="M20 22l12-9 12 9v7H20z" fill="#FFC23D" stroke="currentColor"/><path d="M26 54V40h12v14"/></svg>',
  "plug": '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round" stroke-linecap="round" aria-hidden="true"><rect x="8" y="8" width="30" height="40" rx="3" fill="#FFC23D"/><path d="M8 21h30M8 34h30M23 8v40"/><path d="M38 40h8a8 8 0 0 1 8 8v8"/><path d="M50 56h8"/></svg>',
  "battery": '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round" aria-hidden="true"><rect x="10" y="14" width="40" height="40" rx="5"/><path d="M22 8h16v6H22z"/><path d="M33 22 24 37h9l-3 11 10-16h-9l3-10z" fill="#FFC23D"/></svg>',
  "calc": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.6" aria-hidden="true"><rect x="9" y="5" width="30" height="38" rx="4"/><rect x="14" y="10" width="20" height="8" rx="1.5" fill="#FFC23D"/><path d="M16 25h.01M24 25h.01M32 25h.01M16 32h.01M24 32h.01M32 32h.01M16 38h.01M24 38h.01" stroke-width="4" stroke-linecap="round"/></svg>',
  "sun": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" aria-hidden="true"><circle cx="24" cy="24" r="8" fill="#FFC23D"/><path d="M24 4v6M24 38v6M4 24h6M38 24h6M9.9 9.9l4.2 4.2M33.9 33.9l4.2 4.2M9.9 38.1l4.2-4.2M33.9 14.1l4.2-4.2"/></svg>',
  "panel": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linejoin="round" aria-hidden="true"><path d="M8 10h32l-4 22H4z" fill="#FFC23D"/><path d="M6 21h32M14 10l-3 22M26 10l-2 22M20 32v8M12 40h16"/></svg>',
  "van": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linejoin="round" aria-hidden="true"><path d="M4 32V16a4 4 0 0 1 4-4h22l8 8h4a2 2 0 0 1 2 2v10z"/><rect x="10" y="7" width="16" height="4" fill="#FFC23D"/><circle cx="13" cy="34" r="4" fill="var(--bg)"/><circle cx="35" cy="34" r="4" fill="var(--bg)"/></svg>',
  "plugsmall": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="6" y="6" width="22" height="28" rx="2" fill="#FFC23D"/><path d="M6 20h22M17 6v28"/><path d="M28 30h6a6 6 0 0 1 6 6v6"/></svg>',
  "money": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="12" width="40" height="24" rx="4"/><circle cx="24" cy="24" r="6" fill="#FFC23D"/><path d="M10 18h.01M38 30h.01" stroke-width="4" stroke-linecap="round"/></svg>',
  "match": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="24" cy="24" r="18"/><circle cx="24" cy="24" r="10" fill="#FFC23D"/><circle cx="24" cy="24" r="3" fill="currentColor"/></svg>',
}

def esc(s): return html.escape(str(s), quote=True)

JEKYLL = "--full" not in sys.argv   # default: thin pages + Jekyll layouts (GitHub Pages renders them)
R_OVERRIDE = None

def rel(depth):
    if R_OVERRIDE is not None:
        return R_OVERRIDE
    return "../" * depth

def parse_fragment(path):
    raw = path.read_text(encoding="utf-8")
    meta = {}
    m = re.match(r"\s*<!--meta\n(.*?)\n-->\n?", raw, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1); meta[k.strip()] = v.strip()
        raw = raw[m.end():]
    return meta, raw

def head(title, desc, canon, depth, jsonld=None, og_type="website", extra=""):
    r = rel(depth)
    ld = ""
    if jsonld:
        for block in (jsonld if isinstance(jsonld, list) else [jsonld]):
            ld += '<script type="application/ld+json">' + json.dumps(block, ensure_ascii=False) + "</script>\n"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#16233F">
<meta name="google-adsense-account" content="ca-pub-6620975821265271">
<link rel="icon" href="{r}assets/img/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="{r}site.webmanifest">
<script>try{{var t=localStorage.getItem("ss-theme");if(t)document.documentElement.setAttribute("data-theme",t)}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/css/site.css">
{ADSENSE}
{ld}{extra}</head>
"""

def header(depth, active):
    r = rel(depth)
    if active == "@@LIQUID@@":
        items = "".join(
            f'<li><a href="{r}{href}"{{% if page.nav == "{key}" %}} aria-current="page"{{% endif %}}>{label}</a></li>'
            for key, href, label in NAV)
    else:
        items = "".join(
            f'<li><a href="{r}{href}"{" aria-current=\"page\"" if key == active else ""}>{label}</a></li>'
            for key, href, label in NAV)
    return f"""<body>
<a class="skip" href="#main">Skip to content</a>
<div class="ownerbar"><a href="{OWNER}" target="_blank" rel="noopener">Contact, if you are interested in this website/domain name/Sponsorship/Advertisement/Partnership</a></div>
<header class="site-head">
 <div class="wrap head-row">
  <a class="brand" href="{r}index.html" aria-label="{NAME} home">{LOGO}<span>Simple<b>.</b>solar</span></a>
  <button class="icon-btn menu-btn" aria-expanded="false" aria-controls="nav" aria-label="Menu"><svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><path d="M2 5h16M2 10h16M2 15h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>
  <nav id="nav" aria-label="Main"><ul>{items}</ul></nav>
  <button class="icon-btn" data-theme-toggle aria-label="Switch light or dark theme"><svg width="18" height="18" viewBox="0 0 20 20" aria-hidden="true"><path d="M10 2a8 8 0 1 0 8 8 6 6 0 0 1-8-8z" fill="currentColor"/></svg></button>
  <a class="btn sun small head-cta" href="{r}quotes.html">Compare quotes</a>
 </div>
</header>
<main id="main">
"""

def footer(depth, extra_scripts=""):
    r = rel(depth)
    return f"""</main>
<footer class="site-foot">
 <div class="wrap">
  <div class="foot-grid">
   <div>
    <a class="brand" href="{r}index.html">{LOGO}<span>Simple<b>.</b>solar</span></a>
    <p class="muted" style="margin-top:12px;max-width:34ch">Solar, explained simply. Honest numbers, plain-English guides and free calculators for homeowners, renters and RV owners.</p>
    <form class="form news" data-form="Newsletter signup" data-ok="You're on the list. One useful email a month, no spam.">
     <div class="hp"><label>Leave empty<input name="_hp" tabindex="-1" autocomplete="off"></label></div>
     <label class="hide" for="nl-email">Email</label>
     <input id="nl-email" name="email" type="email" required placeholder="Your email" autocomplete="email">
     <input type="hidden" name="list" value="Monthly solar brief">
     <button class="btn ink small" type="submit">Get the monthly brief</button>
     <p class="form-status" aria-live="polite" style="flex-basis:100%"></p>
    </form>
   </div>
   <div><h4>Start here</h4><ul>
    <li><a href="{r}quotes.html">Compare installer quotes</a></li>
    <li><a href="{r}tools/savings-calculator.html">Savings calculator</a></li>
    <li><a href="{r}tools/solar-match.html">Which solar fits me?</a></li>
    <li><a href="{r}guides/is-solar-worth-it.html">Is solar worth it?</a></li>
    <li><a href="{r}states/index.html">Solar by state</a></li>
   </ul></div>
   <div><h4>Learn</h4><ul>
    <li><a href="{r}guides/index.html">All guides</a></li>
    <li><a href="{r}glossary.html">Solar glossary</a></li>
    <li><a href="{r}videos.html">Video library</a></li>
    <li><a href="{r}resources.html">Trusted resources</a></li>
    <li><a href="{r}faq.html">FAQ</a></li>
   </ul></div>
   <div><h4>Work with us</h4><ul>
    <li><a href="{r}installers.html">For installers</a></li>
    <li><a href="{r}advertise.html">Advertise and sponsor</a></li>
    <li><a href="{r}careers.html">Careers</a></li>
    <li><a href="{r}contests.html">Contests and prizes</a></li>
    <li><a href="{r}support.html">Support the site</a></li>
   </ul></div>
   <div><h4>About</h4><ul>
    <li><a href="{r}about.html">About us</a></li>
    <li><a href="{r}editorial-policy.html">Editorial policy</a></li>
    <li><a href="{r}contact.html">Contact</a></li>
    <li><a href="{r}privacy.html">Privacy</a></li>
    <li><a href="{r}terms.html">Terms</a></li>
    <li><a href="{r}disclaimer.html">Disclaimer</a></li>
    <li><a href="{r}trademark.html">Trademark and copyright</a></li>
   </ul></div>
  </div>
  <div class="foot-legal">
   <span>© <span data-year>{datetime.date.today().year}</span> {NAME}. Independent publisher. Not affiliated with any solar manufacturer, installer or brand with a similar name — see our <a href="{r}trademark.html">trademark and copyright notice</a>.</span>
   <span>Estimates are educational, not quotes. <a href="{r}disclaimer.html">Read the disclaimer</a>.</span>
  </div>
 </div>
</footer>
<div class="consent" id="consent" hidden role="dialog" aria-label="Cookie notice">
 <p>We use cookies for ads (Google AdSense) and basic site preferences. Choose personalised ads or essential only. <a href="{r}privacy.html">Privacy policy</a>.</p>
 <div class="row"><button class="btn sun small" data-consent="all">Accept all</button><button class="btn ghost small" data-consent="essential">Essential only</button></div>
</div>
<script src="{r}assets/js/config.js"></script>
<script src="{r}assets/js/main.js"></script>
{extra_scripts}</body>
</html>
"""

def ad(slot):
    return f'<div class="ad-slot" data-slot="{slot}"></div>'

def write(relpath, content):
    p = ROOT / relpath
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    SITEMAP.append(relpath)

SITEMAP = []

def yq(v):
    return json.dumps(v if v is not None else "", ensure_ascii=True)

def ld_html(jsonld):
    out = ""
    if jsonld:
        for block in (jsonld if isinstance(jsonld, list) else [jsonld]):
            out += '<script type="application/ld+json">' + json.dumps(block, ensure_ascii=False) + "</script>\n"
    return out

def emit(out, title, desc, canon, depth, jsonld, active, body, scripts="", og_type="website", layout="default", extra_fm=None):
    if not JEKYLL:
        write(out, head(title, desc, canon, depth, jsonld, og_type) + header(depth, active) + body + footer(depth, scripts))
        return
    fm = {"layout": layout, "title": title, "description": desc, "canon": canon,
          "r": "/" if out == "404.html" else rel(depth), "nav": active or "", "og_type": og_type,
          "jsonld": ld_html(jsonld), "scripts": scripts}
    if out == "404.html":
        fm["permalink"] = "/404.html"
    if extra_fm: fm.update(extra_fm)
    front = "---\n" + "".join(f"{k}: {yq(v)}\n" for k, v in fm.items()) + "---\n"
    write(out, front + body)

def build_layouts():
    global R_OVERRIDE
    R_OVERRIDE = "{{ page.r }}"
    h = head("@@TITLE@@", "@@DESC@@", "@@CANON@@", 0, None, "@@OG@@", extra="{{ page.jsonld }}")
    h = h.replace("@@TITLE@@", "{{ page.title | escape }}").replace("@@DESC@@", "{{ page.description | escape }}") \
         .replace("@@CANON@@", "{{ page.canon }}").replace("@@OG@@", "{{ page.og_type }}")
    layout = h + header(0, "@@LIQUID@@") + "{{ content }}\n" + footer(0, "{{ page.scripts }}")
    (ROOT / "_layouts").mkdir(exist_ok=True)
    (ROOT / "_layouts/default.html").write_text(layout, encoding="utf-8")
    R_OVERRIDE = None

ORG_LD = {"@context": "https://schema.org", "@type": "Organization", "name": NAME, "url": SITE,
          "logo": SITE + "/assets/img/favicon.svg"}

def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + "/" + u}
                                for i, (n, u) in enumerate(items)]}

def page_scripts(meta, depth):
    out = ""
    for s in [x.strip() for x in meta.get("scripts", "").split(",") if x.strip()]:
        out += f'<script src="{rel(depth)}assets/js/{s}"></script>\n'
    return out

def tpl(body, depth):
    """Simple substitutions inside fragments."""
    r = rel(depth)
    body = body.replace("{{r}}", r)
    for k, v in ICONS.items():
        body = body.replace("{{icon:" + k + "}}", v)
    body = body.replace("{{ad:top}}", ad("top")).replace("{{ad:bottom}}", ad("bottom")).replace("{{ad:inArticle}}", ad("inArticle"))
    body = body.replace("{{updated}}", UPDATED_HUMAN)
    body = body.replace("{{guide_list_8}}", guide_list_html(depth, limit=8))
    body = body.replace("{{guide_list}}", guide_list_html(depth))
    body = body.replace("{{video_grid}}", video_grid_html())
    body = body.replace("{{video_grid_small}}", video_grid_html(limit=3))
    body = body.replace("{{state_options}}", state_options())
    body = body.replace("{{state_grid}}", state_grid_html(depth))
    body = body.replace("{{lead_form}}", lead_form_html(depth))
    return body

# ---------------------------------------------------------------- helpers using data

GUIDES = []  # filled in main()

def guide_list_html(depth, cats=None, limit=None):
    r = rel(depth)
    items = [g for g in GUIDES if not cats or g["cat"] in cats]
    if limit: items = items[:limit]
    return '<ul class="glist">' + "".join(
        f'<li><a href="{r}guides/{g["slug"]}.html"><strong>{esc(g["title"])}</strong><span>{esc(g["description"])}</span><em>{g["mins"]} min</em></a></li>'
        for g in items) + "</ul>"

def video_grid_html(limit=None, topic=None):
    vids = [v for v in D.VIDEOS if not topic or topic in v.get("topics", [])]
    if limit: vids = vids[:limit]
    if not vids: return ""
    return '<div class="grid-3">' + "".join(
        f'<figure class="vid"><button class="yt" data-yt="{v["id"]}" aria-label="Play: {esc(v["title"])}"></button>'
        f'<figcaption>{esc(v["title"])}<small>{esc(v["channel"])} — {esc(v["why"])}</small></figcaption></figure>'
        for v in vids) + "</div>"

def state_options():
    return "".join(f'<option value="{s["code"]}">{esc(s["name"])}</option>' for s in D.STATES)

def state_grid_html(depth):
    r = rel(depth)
    return '<div class="state-grid">' + "".join(
        f'<a href="{r}states/{s["slug"]}.html"><span>{esc(s["name"])}</span><small>{s["rate"]:.0f}¢</small></a>'
        for s in sorted(D.STATES, key=lambda x: x["name"])) + "</div>"

def lead_form_html(depth):
    r = rel(depth)
    return (B / "partials" / "lead_form.html").read_text(encoding="utf-8").replace("{{r}}", r).replace("{{state_options}}", state_options())

# ---------------------------------------------------------------- page builders

def build_simple_pages():
    for f in sorted((B / "pages").glob("*.html")):
        meta, body = parse_fragment(f)
        out = meta.get("out", f.name)
        depth = out.count("/")
        canon = SITE + "/" + ("" if out == "index.html" else out)
        ld = [ORG_LD] if out == "index.html" else []
        if out == "index.html":
            ld.append({"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": SITE})
        if meta.get("faq") == "yes":
            qs = re.findall(r'<details class="faq"><summary>(.*?)</summary>(.*?)</details>', body, re.S)
            if qs:
                ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                    {"@type": "Question", "name": html.unescape(re.sub("<.*?>", "", q)),
                     "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"\s+", " ", html.unescape(re.sub("<.*?>", "", a))).strip()}}
                    for q, a in qs]})
        if meta.get("tool"):
            ld.append({"@context": "https://schema.org", "@type": "WebApplication", "name": meta["title"],
                       "applicationCategory": "UtilityApplication", "operatingSystem": "Any",
                       "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "url": canon})
        title = meta["full_title"] if "full_title" in meta else f'{meta["title"]} | {NAME}'
        scripts = page_scripts(meta, depth)
        if out == "404.html":
            scripts = scripts.replace('src="', 'src="/')
        emit(out, title, meta["description"], canon, depth, ld or None, meta.get("nav", ""), tpl(body, depth), scripts)

def build_guides():
    for g in GUIDES:
        depth = 1
        r = "../"
        body = tpl(g["body"], depth)
        # TOC from h2s with ids
        heads = []
        def addid(m):
            text = re.sub("<.*?>", "", m.group(1))
            sid = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60]
            heads.append((sid, text))
            return f'<h2 id="{sid}">{m.group(1)}</h2>'
        body = re.sub(r"<h2>(.*?)</h2>", addid, body)
        # insert an in-article ad slot after the 2nd h2 section start
        parts = body.split("<h2 ", 3)
        if len(parts) > 3:
            body = parts[0] + "<h2 " + parts[1] + "<h2 " + parts[2] + ad("inArticle") + "<h2 " + parts[3]
        toc = "".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in heads)
        related = [x for x in GUIDES if x["cat"] == g["cat"] and x["slug"] != g["slug"]][:3]
        if len(related) < 3:
            related += [x for x in GUIDES if x not in related and x["slug"] != g["slug"]][: 3 - len(related)]
        rel_html = '<ul class="glist" style="grid-template-columns:1fr">' + "".join(
            f'<li><a href="{x["slug"]}.html"><strong>{esc(x["title"])}</strong><span>{esc(x["description"])}</span><em>{x["mins"]} min</em></a></li>' for x in related) + "</ul>"
        vids = video_grid_html(limit=3, topic=g.get("video"))
        vid_block = f'<h2 id="watch">Watch: a short explainer</h2>{vids}' if vids and g.get("video") else ""
        answer = f'<div class="answer"><strong>Short answer</strong>{g["answer"]}</div>' if g.get("answer") else ""
        canon = f'{SITE}/guides/{g["slug"]}.html'
        ld = [
            {"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["description"],
             "datePublished": g.get("published", "2026-10-22"), "dateModified": TODAY,
             "author": {"@type": "Organization", "name": NAME + " editorial team", "url": SITE + "/about.html"},
             "publisher": ORG_LD, "mainEntityOfPage": canon},
            crumbs_ld([("Home", ""), ("Guides", "guides/index.html"), (g["title"], f'guides/{g["slug"]}.html')]),
        ]
        qs = re.findall(r'<details class="faq"><summary>(.*?)</summary>(.*?)</details>', g["body"], re.S)
        if qs:
            ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": html.unescape(re.sub("<.*?>", "", q)),
                 "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"\s+", " ", html.unescape(re.sub("<.*?>", "", a))).strip()}}
                for q, a in qs]})
        page = f"""<div class="wrap page-head">
 <p class="crumbs"><a href="../index.html">Home</a> / <a href="index.html">Guides</a> / {esc(g["catname"])}</p>
 <h1>{esc(g["title"])}</h1>
 <p class="lede">{esc(g["description"])}</p>
</div>
<div class="wrap article-grid">
 <article class="prose">
  <p class="byline">By the {NAME} editorial team. Reviewed {UPDATED_HUMAN}. {g["mins"]}-minute read. <a href="../editorial-policy.html">How we research</a>.</p>
  {answer}
  {body}
  {vid_block}
  <div class="panel sunny" style="margin-top:2em"><h3 class="mt0">Want real numbers for your home?</h3><p>Answer six quick questions and up to three vetted local installers will send quotes you can compare side by side. Free, no obligation.</p><a class="btn ink" href="../quotes.html">Compare quotes</a></div>
  {ad("bottom")}
  <h2 id="related" style="margin-top:2em">Keep reading</h2>
  {rel_html}
 </article>
 <aside class="side"><div class="sticky">
  <nav class="panel toc" aria-label="On this page"><h3 class="mt0">On this page</h3><ol>{toc}</ol></nav>
  <div class="panel leafy"><h3 class="mt0">Run your numbers</h3><p class="mb0">Free tools: <a href="../tools/savings-calculator.html">savings</a>, <a href="../tools/system-size.html">system size</a>, <a href="../tools/battery-sizer.html">battery backup</a>, <a href="../tools/power-station.html">power station</a>.</p></div>
  {ad("sidebar")}
 </div></aside>
</div>
"""
        emit(f'guides/{g["slug"]}.html', f'{g["title"]} | {NAME}', g["description"], canon, depth, ld, "guides", page, og_type="article")

def money(x):
    return "${:,.0f}".format(round(x, -1) if abs(x) >= 100 else x)

def state_numbers(s, bill):
    kwh_month = bill / (s["rate"] / 100)
    kwh_year = kwh_month * 12
    offset = 0.9
    size_kw = kwh_year * offset / (s["sun"] * 365 * 0.78)
    cost = size_kw * 1000 * D.COST_PER_WATT
    save1 = kwh_year * offset * s["rate"] / 100 * D.EXPORT_FACTOR
    # 25-year savings with 3% utility escalation, 0.5%/yr degradation
    total = 0; payback = None; cum = -cost
    for y in range(1, 26):
        sv = save1 * (1.03 ** (y - 1)) * (0.995 ** (y - 1))
        total += sv; cum += sv
        if payback is None and cum >= 0: payback = y
    return dict(kwh=kwh_month, size=size_kw, cost=cost, save1=save1, total=total, net=total - cost, payback=payback)

def build_states():
    ranked = sorted(D.STATES, key=lambda s: state_numbers(s, 150)["payback"] or 99)
    rank = {s["code"]: i + 1 for i, s in enumerate(ranked)}
    rows = ""
    for s in sorted(D.STATES, key=lambda x: x["name"]):
        n = state_numbers(s, 150)
        rows += (f'<tr><td><a href="{s["slug"]}.html">{esc(s["name"])}</a></td><td class="num" data-v="{s["rate"]}">{s["rate"]:.1f}¢</td>'
                 f'<td class="num" data-v="{s["sun"]}">{s["sun"]:.1f}</td><td class="num" data-v="{n["size"]:.2f}">{n["size"]:.1f} kW</td>'
                 f'<td class="num" data-v="{n["save1"]:.0f}">{money(n["save1"])}</td><td class="num" data-v="{n["payback"] or 99}">{n["payback"] or "25+"} yrs</td>'
                 f'<td class="num" data-v="{rank[s["code"]]}">{rank[s["code"]]}</td></tr>')
    meta, body = parse_fragment(B / "partials" / "states_index.html")
    body = body.replace("{{rows}}", rows).replace("{{cpw}}", f'{D.COST_PER_WATT:.2f}').replace("{{rate_src}}", D.RATE_SOURCE).replace("{{sun_src}}", D.SUN_SOURCE)
    canon = SITE + "/states/index.html"
    emit("states/index.html", meta["full_title"], meta["description"], canon, 1, [crumbs_ld([("Home", ""), ("Solar by state", "states/index.html")])], "states", tpl(body, 1))

    tmpl_meta, tmpl = parse_fragment(B / "partials" / "state_page.html")
    if JEKYLL:
        lay = re.sub(r"\{\{([a-z_0-9]+)\}\}", r"{{ page.\1 }}", tpl(tmpl, 1))
        (ROOT / "_layouts/state.html").write_text("---\nlayout: default\n---\n" + lay, encoding="utf-8")
    for s in D.STATES:
        bills = [100, 150, 250]
        tbl = ""
        for b in bills:
            n = state_numbers(s, b)
            tbl += (f'<tr><td>{money(b)}/month</td><td class="num">{n["kwh"]:.0f} kWh</td><td class="num">{n["size"]:.1f} kW</td>'
                    f'<td class="num">{money(n["cost"])}</td><td class="num">{money(n["save1"])}</td><td class="num">{n["payback"] or "25+"} yrs</td><td class="num">{money(n["net"])}</td></tr>')
        n = state_numbers(s, 150)
        avg_rate = sum(x["rate"] for x in D.STATES) / len(D.STATES)
        avg_sun = sum(x["sun"] for x in D.STATES) / len(D.STATES)
        rate_vs = "above" if s["rate"] > avg_rate * 1.05 else ("below" if s["rate"] < avg_rate * 0.95 else "close to")
        sun_vs = "more" if s["sun"] > avg_sun * 1.05 else ("less" if s["sun"] < avg_sun * 0.95 else "about the same")
        verdict = ("Strong" if (n["payback"] or 99) <= 9 else "Good" if (n["payback"] or 99) <= 12 else "Fair" if (n["payback"] or 99) <= 16 else "Weak")
        verdict_text = {
            "Strong": "Rooftop solar pays back quickly here for most sunny, owner-occupied homes. Get at least three quotes.",
            "Good": "Solar usually makes financial sense here if your roof faces south, east or west with little shade.",
            "Fair": "Solar can work, but the margin is thinner. Quote shopping and a cash or low-rate loan matter more.",
            "Weak": "Pure payback is slow at today's power prices. Plug-in solar, a battery for backup or waiting for better pricing may suit you better.",
        }[verdict]
        nb = sorted(D.STATES, key=lambda x: abs(x["rate"] - s["rate"]))[1:5]
        nb_html = " ".join(f'<a class="pill" href="{x["slug"]}.html">{esc(x["name"])}</a>' for x in nb)
        body = tmpl
        rep = {
            "{{name}}": esc(s["name"]), "{{code}}": s["code"], "{{rate}}": f'{s["rate"]:.1f}', "{{sun}}": f'{s["sun"]:.1f}',
            "{{rate_vs}}": rate_vs, "{{sun_vs}}": sun_vs, "{{avg_rate}}": f"{avg_rate:.1f}", "{{avg_sun}}": f"{avg_sun:.1f}",
            "{{rows}}": tbl, "{{verdict}}": verdict, "{{verdict_text}}": verdict_text, "{{rank}}": str(rank[s["code"]]),
            "{{size150}}": f'{n["size"]:.1f}', "{{save150}}": money(n["save1"]), "{{payback150}}": str(n["payback"] or "25+"),
            "{{cost150}}": money(n["cost"]), "{{cpw}}": f'{D.COST_PER_WATT:.2f}',
            "{{plugin}}": s.get("plugin", D.PLUGIN_DEFAULT), "{{policy}}": s.get("policy", D.POLICY_DEFAULT),
            "{{neighbors}}": nb_html, "{{rate_src}}": D.RATE_SOURCE, "{{sun_src}}": D.SUN_SOURCE,
            "{{yearly_kwh_kw}}": f'{s["sun"] * 365 * 0.78:,.0f}',
        }
        if not JEKYLL:
            for k, v in rep.items(): body = body.replace(k, v)
        title = f'Solar in {s["name"]}: Cost, Savings and Payback ({datetime.date.today().year})'
        desc = f'Is solar worth it in {s["name"]}? {s["rate"]:.1f}¢/kWh power, {s["sun"]:.1f} sun hours a day, a typical {n["size"]:.1f} kW system and {n["payback"] or "25+"}-year payback, in plain English.'
        canon = f'{SITE}/states/{s["slug"]}.html'
        faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": f'Is solar worth it in {s["name"]}?', "acceptedAnswer": {"@type": "Answer", "text": f'{verdict} case. {verdict_text} For a $150 monthly bill we estimate a {n["size"]:.1f} kW system, about {money(n["save1"])} first-year savings and a {n["payback"] or "25+"}-year payback.'}},
            {"@type": "Question", "name": f'How much does a solar system cost in {s["name"]}?', "acceptedAnswer": {"@type": "Answer", "text": f'At about ${D.COST_PER_WATT:.2f} per watt before incentives, a {n["size"]:.1f} kW system costs roughly {money(n["cost"])}. Local quotes vary by roof, equipment and installer.'}},
        ]}
        ld = [crumbs_ld([("Home", ""), ("Solar by state", "states/index.html"), (s["name"], f'states/{s["slug"]}.html')]), faq_ld]
        if JEKYLL:
            emit(f'states/{s["slug"]}.html', f"{title} | {NAME}", desc, canon, 1, ld, "states", "", og_type="article",
                 layout="state", extra_fm={k.strip("{}"): v for k, v in rep.items()})
        else:
            emit(f'states/{s["slug"]}.html', f"{title} | {NAME}", desc, canon, 1, ld, "states", tpl(body, 1), og_type="article")

def build_guides_index():
    meta, body = parse_fragment(B / "partials" / "guides_index.html")
    sections = ""
    for cat, catname, blurb in D.GUIDE_CATS:
        lst = guide_list_html(1, cats=[cat])
        sections += f'<section class="wrap" style="padding-bottom:34px" id="{cat}"><div class="sec-head"><h2 class="mb0">{esc(catname)}</h2><p>{esc(blurb)}</p></div>{lst}</section>'
        if cat == D.GUIDE_CATS[1][0]:
            sections += f'<div class="wrap">{ad("inArticle")}</div>'
    body = body.replace("{{sections}}", sections)
    emit("guides/index.html", meta["full_title"], meta["description"], SITE + "/guides/index.html", 1, [crumbs_ld([("Home", ""), ("Guides", "guides/index.html")])], "guides", tpl(body, 1))

def build_data_js():
    js = "window.SS_DATA=" + json.dumps({
        "states": [{k: s[k] for k in ("code", "name", "slug", "rate", "sun")} for s in D.STATES],
        "cpw": D.COST_PER_WATT, "exportFactor": D.EXPORT_FACTOR, "battery": D.BATTERY,
    }, separators=(",", ":")) + ";\n"
    (ROOT / "assets/js/data.js").write_text(js, encoding="utf-8")

def build_sitemap():
    urls = sorted(set(SITEMAP))
    skip = {"404.html", "thank-you.html"}
    body = "".join(
        f"<url><loc>{SITE}/{'' if u == 'index.html' else u}</loc><lastmod>{TODAY}</lastmod>"
        f"<priority>{'1.0' if u == 'index.html' else '0.8' if u in ('quotes.html',) or u.startswith('tools/') else '0.7' if u.startswith('guides/') else '0.6'}</priority></url>\n"
        for u in urls if u not in skip)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}</urlset>\n', encoding="utf-8")

def load_guides():
    cats = {c: n for c, n, _ in D.GUIDE_CATS}
    order = {slug: i for i, slug in enumerate(D.GUIDE_ORDER)}
    for f in (B / "guides").glob("*.html"):
        meta, body = parse_fragment(f)
        words = len(re.sub("<.*?>", " ", body).split())
        GUIDES.append(dict(slug=f.stem, title=meta["title"], description=meta["description"], cat=meta["cat"],
                           catname=cats[meta["cat"]], answer=meta.get("answer", ""), video=meta.get("video", ""),
                           body=body, words=words, mins=max(3, round(words / 230))))
    GUIDES.sort(key=lambda g: order.get(g["slug"], 999))

def main():
    load_guides()
    if JEKYLL:
        build_layouts()
    build_data_js()
    build_simple_pages()
    build_guides()
    build_guides_index()
    build_states()
    build_sitemap()
    total = sum(g["words"] for g in GUIDES)
    print(f"Built {len(SITEMAP)} pages; {len(GUIDES)} guides, {total:,} guide words.")

if __name__ == "__main__":
    main()
