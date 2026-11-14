"""Build the WEAVE Lab website from the YAML files in content/.

Usage:
    python build.py            # writes the site into docs/
    python build.py --serve    # builds, then serves docs/ at http://localhost:8000

Needs only Python 3 and PyYAML. All page text lives in content/*.yml;
this file holds layout only.
"""

import datetime as dt
import html
import re
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
OUT = ROOT / "docs"


def load(name):
    with open(CONTENT / f"{name}.yml", encoding="utf-8") as f:
        return yaml.safe_load(f)


# --------------------------------------------------------------------------
# Inline formatting: **bold**, *italic*, [text](url). Content is trusted.
# --------------------------------------------------------------------------
def md(text):
    if text is None:
        return ""
    s = str(text).strip()
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: link(m.group(2), m.group(1)), s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    return s


def link(url, label):
    ext = url.startswith("http")
    attrs = ' target="_blank" rel="noopener"' if ext else ""
    return f'<a href="{html.escape(url, quote=True)}"{attrs}>{label}</a>'


def esc(s):
    return html.escape(str(s or ""))


# --------------------------------------------------------------------------
# Page shell
# --------------------------------------------------------------------------
NAV = [
    ("index.html", "Home"),
    ("research.html", "Research"),
    ("people.html", "People"),
    ("publications.html", "Publications"),
    ("teaching.html", "Teaching & Mentoring"),
    ("news.html", "News & Media"),
    ("cv.html", "CV"),
    ("weather.html", "Weather"),
]


def page(site, filename, title, body, description=None):
    nav = "".join(
        f'<a href="{href}"{" aria-current=page" if href == filename else ""}>{label}</a>'
        for href, label in NAV
    )
    full_title = f"{site['name']} | {site['lab_name']}" if filename == "index.html" else f"{title} | {site['lab_name']}"
    desc = esc(description or f"{site['lab_name']} ({site['lab_full']}), {site['name']}'s research group at the {site['university']}.")
    updated = dt.date.today().strftime("%B %Y")
    links = " · ".join(link(l["url"], esc(l["label"])) for l in site["links"])
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="images/weave-logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="index.html">
      <img src="{site['logo']}" alt="" width="36" height="36">
      <span><b>{esc(site['lab_name'])}</b><small>{esc(site['name'])} · {esc(site['university'])}</small></span>
    </a>
    <button class="nav-toggle" aria-label="Menu" onclick="document.body.classList.toggle('nav-open')">&#9776;</button>
    <nav class="site-nav">{nav}</nav>
  </div>
</header>
<main>
{body}
</main>
<footer class="site-footer">
  <div class="wrap footer-inner">
    <div>
      <b>{esc(site['lab_name'])}</b> · {esc(site['lab_full'])}<br>
      {link(site['department_url'], esc(site['department']))}, {esc(site['university'])}<br>
      {esc(site['office'])}
    </div>
    <div class="footer-right">
      <a href="mailto:{esc(site['email'])}">{esc(site['email'])}</a><br>
      {links}<br>
      <span class="muted">Updated {updated}</span>
    </div>
  </div>
</footer>
<script src="js/site.js"></script>
</body>
</html>
"""


def page_head(title, lead=None):
    lead_html = f'<p class="lead">{md(lead)}</p>' if lead else ""
    return f'<section class="page-head"><div class="wrap"><h1>{esc(title)}</h1>{lead_html}</div></section>'


# --------------------------------------------------------------------------
# Publications
# --------------------------------------------------------------------------
HIGH_PROFILE = {"Science": "Science", "Proceedings of the National Academy of Sciences": "PNAS",
                "Nature Communications": "Nature Communications"}


def cite(p, number=None):
    authors = md(p["authors"])
    title = esc(p["title"])
    if not title.endswith("?"):
        title += "."
    details = f", {esc(p['details'])}" if p.get("details") else ""
    doi = p.get("doi")
    url = f"https://doi.org/{doi}" if doi else p.get("url")
    title_html = link(url, title) if url else title
    badge = f'<span class="badge">{HIGH_PROFILE[p["journal"]]}</span>' if p["journal"] in HIGH_PROFILE else ""
    num = f'<span class="pub-num">{number}</span>' if number else ""
    return (
        f'{num}<span class="pub-body">{authors} ({p["year"]}). <span class="pub-title">{title_html}</span> '
        f'<i>{esc(p["journal"])}</i>{details}. {badge}</span>'
    )


def pub_flags(p):
    """(first-authored by Y. Zheng, includes a mentored student † or postdoc ‡)."""
    a = p["authors"]
    first = a.startswith("**Zheng, Y.**")
    trainee = "†" in a or "‡" in a
    return first, trainee


LEGEND = "<b>Bold</b>: Youtong Zheng · † graduate student mentored by Youtong · ‡ postdoctoral researcher mentored by Youtong"


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------
def build_home(site, research, news, pubs, people):
    by_id = {p["id"]: p for p in pubs}
    cards = "".join(
        f'<a class="card theme-card" href="research.html#{t["id"]}"><h3>{esc(t["title"])}</h3><p>{md(t["short"])}</p><span class="more">Read more →</span></a>'
        for t in research["themes"]
    )
    news_items = "".join(
        f'<li><time>{fmt_month(n["date"])}</time><span>{md(n["text"])}</span></li>' for n in news[:6]
    )
    recent = [p for p in pubs if any(pub_flags(p))][:3]
    recent_html = "".join(f"<li>{cite(p)}</li>" for p in recent)
    links = "".join(f'<a class="btn ghost" href="{esc(l["url"])}" target="_blank" rel="noopener">{esc(l["label"])}</a>' for l in site["links"][:2])
    body = f"""
<section class="hero">
  <div class="wrap hero-inner">
    <div class="hero-text">
      <p class="eyebrow">{esc(site['lab_name'])} · {esc(site['lab_full'])}</p>
      <h1>{esc(site['name'])} <span class="zh">{esc(site['name_zh'])}</span></h1>
      <p class="role">{esc(site['title'])}, {link(site['department_url'], esc(site['department']))}, {esc(site['university'])}</p>
      <p class="intro">{md(site['intro'])}</p>
      <div class="actions">
        <a class="btn" href="mailto:{esc(site['email'])}">Email</a>
        <a class="btn ghost" href="cv.html">CV</a>
        {links}
      </div>
    </div>
    <img class="hero-photo" src="{site['photo']}" alt="{esc(site['name'])}">
  </div>
</section>
<section class="quote"><div class="wrap"><blockquote>“{esc(site['quote'])}”<cite>— {esc(site['quote_by'])}</cite></blockquote></div></section>
<section class="section"><div class="wrap">
  <div class="section-title"><h2>Research</h2><a href="research.html">All research →</a></div>
  <div class="grid cards4">{cards}</div>
</div></section>
<section class="section alt"><div class="wrap two-col">
  <div>
    <div class="section-title"><h2>News</h2><a href="news.html">All news →</a></div>
    <ul class="news">{news_items}</ul>
  </div>
  <div>
    <div class="callout">
      <h2>Join us</h2>
      <p>{md(site['join_us'])}</p>
      <a class="btn" href="mailto:{esc(site['email'])}">Email Youtong</a>
    </div>
    <div class="section-title small"><h3>Recent papers from the group</h3><a href="publications.html">All {len(pubs)} →</a></div>
    <ul class="pubs compact">{recent_html}</ul>
  </div>
</div></section>
<section class="section"><div class="wrap">
  <a class="group-banner" href="people.html">
    <img src="images/group-2025.jpg" alt="The WEAVE Lab group">
    <span>Meet the group →</span>
  </a>
</div></section>
"""
    return body


def build_research(research, pubs):
    by_id = {p["id"]: p for p in pubs}
    sections = []
    for t in research["themes"]:
        plist = "".join(f"<li>{cite(by_id[i])}</li>" for i in t.get("papers", []) if i in by_id)
        sections.append(
            f'<section class="theme" id="{t["id"]}"><h2>{esc(t["title"])}</h2><p class="theme-short">{md(t["short"])}</p>'
            f'<p>{md(t["text"])}</p><details open><summary>Key papers</summary><ul class="pubs compact">{plist}</ul></details></section>'
        )
    funding = "".join(f"<li>{md(f)}</li>" for f in research["funding"])
    body = page_head("Research", "We weave observations, simulations, theory, and machine learning together to understand clouds, convection, and precipitation.")
    body += f"""<section class="section"><div class="wrap narrow">
{''.join(sections)}
<div class="grid cards3 facts">
  <div class="card"><h3>Funding</h3><ul>{funding}</ul></div>
  <div class="card"><h3>Collaborators</h3><p>{md(research['collaborators'])}</p></div>
  <div class="card"><h3>Tools</h3><p>{md(research['tools'])}</p></div>
</div>
</div></section>"""
    return body


def build_people(site, people):
    pi = people["pi"]
    members = "".join(
        f"""<article class="person">
  <img src="{m['photo']}" alt="{esc(m['name'])}" loading="lazy">
  <h3>{esc(m['name'])}</h3>
  <p class="person-role">{esc(m['role'])}{' · since ' + str(m['since']) if m.get('since') else ''}</p>
  <p class="person-topic">{md(m.get('topic'))}</p>
  <p class="person-meta">{esc(m.get('background'))}</p>
  {f'<p class="person-awards">{md(m["awards"])}</p>' if m.get('awards') else ''}
</article>"""
        for m in people["members"]
    )
    alumni = "".join(f"<li>{md(a)}</li>" for a in people["alumni"])
    work = "".join(f"<li>{md(w)}</li>" for w in people["how_we_work"])
    body = page_head("People")
    body += f"""<section class="section"><div class="wrap">
<figure class="group-photo"><img src="images/group-2025.jpg" alt="The WEAVE Lab group"><figcaption>The group in the lab, January 2025.</figcaption></figure>
<article class="pi">
  <img src="{pi['photo']}" alt="{esc(pi['name'])}">
  <div><h2>{esc(pi['name'])}</h2><p class="person-role">{esc(pi['role'])}</p><p>{md(pi['bio'])}</p>
  <p><a href="cv.html">Full CV →</a></p></div>
</article>
<h2>Current members</h2>
<div class="people-grid">{members}</div>
<div class="two-col top-gap">
  <div><h2>How we work</h2><ul class="plain">{work}</ul></div>
  <div><h2>Alumni</h2><ul class="plain">{alumni}</ul>
    <div class="callout"><h3>Join us</h3><p>{md(site['join_us'])}</p><a class="btn" href="mailto:{esc(site['email'])}">Email Youtong</a></div>
  </div>
</div>
</div></section>"""
    return body


def build_publications(site, pubs, manuscripts, conferences):
    total = len(pubs)
    years = []
    for p in pubs:
        if p["year"] not in years:
            years.append(p["year"])
    n = total
    blocks = []
    for y in years:
        items = []
        for p in [q for q in pubs if q["year"] == y]:
            led, trainee = pub_flags(p)
            text = re.sub("<[^>]+>", "", f'{p["authors"]} {p["title"]} {p["journal"]} {p["year"]}').lower()
            items.append(
                f'<li class="pub" data-first="{int(led)}" data-trainee="{int(trainee)}" data-text="{esc(text)}">{cite(p, n)}</li>'
            )
            n -= 1
        blocks.append(f'<section class="pub-year" data-year="{y}"><h2>{y}</h2><ol class="pubs">{"".join(items)}</ol></section>')
    led_n = sum(pub_flags(p)[0] for p in pubs)
    tr_n = sum(pub_flags(p)[1] for p in pubs)
    mans = "".join(
        f'<li><span class="pub-body">{md(m["authors"])}. <span class="pub-title">{esc(m["title"])}.</span> '
        f'<i>{esc(m["journal"])}</i>, <span class="status">{esc(m["status"])}</span>.</span></li>'
        for m in manuscripts
    )
    confs = "".join(f"<li>{md(c)}</li>" for c in conferences)
    body = page_head(
        "Publications",
        f"{total} peer-reviewed papers, including *Science*, *PNAS*, *Nature Communications*, and 20 in "
        f"*Geophysical Research Letters*. Also on [Google Scholar](https://scholar.google.com/citations?user=xTpHltEAAAAJ).",
    )
    body += f"""<section class="section"><div class="wrap narrow">
<p class="legend top">{LEGEND}</p>
<p class="toc"><a href="#manuscripts">Manuscripts in review</a> · <a href="#papers">Peer-reviewed papers</a> · <a href="#conferences">Conference presentations</a></p>
<h2 id="manuscripts">Manuscripts in review</h2>
<ul class="pubs">{mans}</ul>
<h2 id="papers">Peer-reviewed papers</h2>
<div class="pub-tools">
  <input id="pub-search" type="search" placeholder="Search title, author, journal…" aria-label="Search publications">
  <div class="chips" role="group" aria-label="Filter">
    <button class="chip active" data-filter="all">All ({total})</button>
    <button class="chip" data-filter="first">First author: Youtong ({led_n})</button>
    <button class="chip" data-filter="trainee">With mentored students and postdocs ({tr_n})</button>
  </div>
</div>
{''.join(blocks)}
<p id="pub-empty" class="muted" hidden>No papers match.</p>
<h2 id="conferences">Conference presentations (since 2023)</h2>
<ul class="pubs compact">{confs}</ul>
</div></section>"""
    return body


def build_teaching(teaching):
    approach = "".join(f'<div class="card"><h3>{esc(a["title"])}</h3><p>{md(a["text"])}</p></div>' for a in teaching["approach"])
    courses = []
    for c in teaching["courses"]:
        img = f'<img class="course-img" src="{c["image"]}" alt="{esc(c.get("image_alt", ""))}" loading="lazy">' if c.get("image") else ""
        quote = (f'<blockquote class="course-quote">“{esc(c["quote"])}”<cite>— {esc(c["quote_by"])}</cite></blockquote>'
                 if c.get("quote") else "")
        terms = "".join(f'<span class="chip static">{esc(t)}</span>' for t in c["terms"])
        new = ' <span class="badge">New course developed</span>' if c.get("new") else ""
        courses.append(f"""<article class="course-row{' has-img' if img else ''}">
  {img}
  <div>
    <p class="course-code">{esc(c['code'])}{new}</p>
    <h3>{esc(c['title'])}</h3>
    <p class="muted small">{esc(c['level'])}</p>
    <p>{md(c['description'])}</p>
    {quote}
    <p class="terms"><span class="muted small">Taught (enrollment):</span> {terms}</p>
  </div>
</article>""")
    quotes = "".join(f'<blockquote>“{esc(q["text"])}”<cite>— {esc(q["course"])} student</cite></blockquote>' for q in teaching["student_quotes"])
    m = teaching["mentoring"]
    groups = "".join(
        f'<div class="mentor-group"><h3>{esc(g["title"])}</h3><ul class="plain">' + "".join(f"<li>{md(i)}</li>" for i in g["items"]) + "</ul></div>"
        for g in m["groups"]
    )
    body = page_head("Teaching & Mentoring", teaching["intro"])
    body += f"""<section class="section"><div class="wrap">
<p class="toc"><a href="#approach">Approach</a> · <a href="#courses">Courses</a> · <a href="#students-say">What students say</a> · <a href="#mentoring">Mentoring</a></p>
<h2 id="approach">Approach</h2>
<div class="grid cards3">{approach}</div>
<h2 id="courses">Courses at the University of Houston</h2>
<div class="courses">{''.join(courses)}</div>
<p class="muted small">Earlier: {md(teaching['earlier'])}</p>
<h2 id="students-say">What students say</h2>
<div class="quotes grid cards2">{quotes}</div>
<p class="muted small">From anonymous UH course evaluations.</p>
</div></section>
<section class="section alt" id="mentoring"><div class="wrap">
<h2>Mentoring</h2>
<p class="narrow-text">{md(m['intro'])}</p>
<div class="mentor-grid">{groups}</div>
<p><a href="people.html">Meet the current group →</a></p>
</div></section>"""
    return body


def timeline(rows):
    return '<dl class="timeline">' + "".join(f"<dt>{esc(r['when'])}</dt><dd>{md(r['what'])}</dd>" for r in rows) + "</dl>"


def build_news(news, cv):
    by_year = {}
    for n in news:
        by_year.setdefault(str(n["date"])[:4], []).append(n)
    blocks = "".join(
        f'<h2>{y}</h2><ul class="news">' + "".join(f'<li><time>{fmt_month(n["date"])}</time><span>{md(n["text"])}</span></li>' for n in items) + "</ul>"
        for y, items in by_year.items()
    )
    media = "".join(f'<h3 class="media-h">{esc(s["title"])}</h3>{timeline(s["items"])}' for s in cv["media"])
    return (page_head("News & Media")
            + '<section class="section"><div class="wrap narrow"><p class="toc"><a href="#news">News</a> · <a href="#media">Media coverage and research highlights</a></p>'
            + f'<div id="news">{blocks}</div>'
            + f'<h2 id="media">Media coverage and research highlights</h2>{media}</div></section>')


def build_cv(site, cv):
    secs = cv["sections"]
    toc = " · ".join(f'<a href="#{s["id"]}">{esc(s["title"])}</a>' for s in secs)
    extra = ' · <a href="publications.html">Publications</a> · <a href="teaching.html">Teaching &amp; mentoring</a> · <a href="news.html#media">Media</a>'
    body = page_head("Curriculum Vitae", f"{site['name']}, Ph.D. · {site['title']}, {site['department']}, {site['university']}.")
    body += f'<section class="section"><div class="wrap narrow"><p class="toc">{toc}{extra}</p>'
    body += f'<h2 id="interests">Research interests</h2><p>{md(cv["interests"])}</p>'
    body += "".join(f'<h2 id="{s["id"]}">{esc(s["title"])}</h2>{timeline(s["items"])}' for s in secs)
    body += "</div></section>"
    return body


def build_weather():
    # Every image points at a "latest" product URL. site.js reloads each one every few minutes
    # (with a cache-busting query), so an open page keeps showing the newest image.
    panels = [
        ("Houston radar (KHGX), loop", "https://radar.weather.gov/ridge/standard/KHGX_loop.gif", "https://radar.weather.gov/station/khgx/standard", 2),
        ("GOES-19 GeoColor, continental U.S.", "https://cdn.star.nesdis.noaa.gov/GOES19/ABI/CONUS/GEOCOLOR/1250x750.jpg", "https://www.star.nesdis.noaa.gov/GOES/conus.php?sat=G19", 5),
        ("GOES-19 water vapor (band 9)", "https://cdn.star.nesdis.noaa.gov/GOES19/ABI/CONUS/09/1250x750.jpg", "https://www.star.nesdis.noaa.gov/GOES/conus.php?sat=G19", 5),
        ("U.S. radar mosaic, loop", "https://radar.weather.gov/ridge/standard/CONUS_loop.gif", "https://radar.weather.gov/", 2),
        ("NWS surface analysis", "https://www.wpc.ncep.noaa.gov/sfc/namussfcwbg.gif", "https://www.wpc.ncep.noaa.gov/html/sfc-zoom.php", 30),
        ("WPC short-range forecast, day 1", "https://www.wpc.ncep.noaa.gov/basicwx/92fndfd.gif", "https://www.wpc.ncep.noaa.gov/basicwx/basicwx_ndfd.php", 30),
    ]
    figs = "".join(
        f'<figure class="card wx"><a href="{page_url}" target="_blank" rel="noopener"><img class="live" data-src="{img}" data-refresh="{mins}" src="{img}" alt="{esc(t)}"></a>'
        f'<figcaption>{esc(t)} <span class="muted small">· refreshes every {mins} min · <span class="stamp"></span></span></figcaption></figure>'
        for t, img, page_url, mins in panels
    )
    body = page_head("Live weather", "Live maps from NOAA. Each image reloads by itself while this page is open (radar every 2 minutes, satellite every 5, analyses every 30). Click an image for its source page.")
    body += f'<section class="section"><div class="wrap"><div class="grid cards2">{figs}</div></div></section>'
    return body


def fmt_month(d):
    d = str(d)
    try:
        return dt.datetime.strptime(d[:7], "%Y-%m").strftime("%b %Y")
    except ValueError:
        return d


# --------------------------------------------------------------------------
def main():
    site = load("site")
    research = load("research")
    people = load("people")
    pubs = load("publications")
    manuscripts = load("manuscripts")
    conferences = load("conferences")
    teaching = load("teaching")
    news = load("news")
    cv = load("cv")

    # Empty docs/ (keep the folder itself, which a local preview server may hold open).
    OUT.mkdir(exist_ok=True)
    for item in OUT.iterdir():
        shutil.rmtree(item) if item.is_dir() else item.unlink()
    shutil.copytree(ROOT / "static", OUT, dirs_exist_ok=True)
    (OUT / ".nojekyll").write_text("")

    pages = {
        "index.html": ("Home", build_home(site, research, news, pubs, people)),
        "research.html": ("Research", build_research(research, pubs)),
        "people.html": ("People", build_people(site, people)),
        "publications.html": ("Publications", build_publications(site, pubs, manuscripts, conferences)),
        "teaching.html": ("Teaching & Mentoring", build_teaching(teaching)),
        "news.html": ("News & Media", build_news(news, cv)),
        "cv.html": ("CV", build_cv(site, cv)),
        "weather.html": ("Live weather", build_weather()),
    }
    for fn, (title, body) in pages.items():
        (OUT / fn).write_text(page(site, fn, title, body), encoding="utf-8")
    # Old URLs from the previous site redirect to the new pages.
    for old, new in {"publications": "publications.html", "teaching": "teaching.html", "cv": "cv.html",
                     "group": "people.html", "news": "news.html", "weather": "weather.html", "about": "index.html"}.items():
        (OUT / old).mkdir(exist_ok=True)
        (OUT / old / "index.html").write_text(
            f'<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=../{new}"><link rel="canonical" href="../{new}">',
            encoding="utf-8")
    print(f"Built {len(pages)} pages into {OUT}")

    if "--serve" in sys.argv:
        import functools
        import http.server
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
        print("Serving at http://localhost:8000")
        http.server.ThreadingHTTPServer(("127.0.0.1", 8000), handler).serve_forever()


if __name__ == "__main__":
    main()
