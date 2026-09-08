#!/usr/bin/env python3
"""Build the multi-page HTML edition.

One page per chapter, with previous/next navigation, a dark reading mode, and the
metadata search engines need. Part dividers and orientation stubs are folded into
the page that follows them, since a page holding only a divider is not worth a click.
"""
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
OUT = REPO / "docs"
BASE = "https://measuring-retrieval-book.github.io/Measuring-Retrieval-Book-1e"
PDF = ("https://github.com/Measuring-Retrieval-Book/Measuring-Retrieval-Book-1e/raw/main/"
       "measuring-retrieval-full-book/measuring-retrieval-full.pdf")
TITLE = "Measuring Retrieval"
SUB = "A working book on metrics, evidence, and evaluation design"
AUTHOR = "Madhava Gaikwad"
PUBLISHED = "2026-09"

# Files that carry no readable content of their own.
STUB = re.compile(r"(part-[a-z]+|orientation|dedication)\.md$")


def slug(path: Path) -> str:
    name = path.stem
    name = re.sub(r"^\d+[a-z]?-", "", name)
    return name


def group_pages(order):
    """Fold stub files into the content page that follows them."""
    pages, pending = [], []
    for rel in order:
        path = ROOT / rel
        if STUB.search(rel):
            pending.append(path)
            continue
        pages.append({"sources": pending + [path], "slug": slug(path)})
        pending = []
    if pending:
        pages[-1]["sources"].extend(pending)
    return pages


def render(sources):
    cmd = ["pandoc", *[str(s) for s in sources], "--from=markdown+raw_tex-implicit_figures",
           f"--resource-path={ROOT}", "--to=html5", "--section-divs"]
    body = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    body = re.sub(r'(src="assets/diagrams/[^"]+?)\.png(")', r"\1.svg\2", body)
    return body


def first_heading(body, fallback):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
    return re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else fallback


def description(body):
    for m in re.finditer(r"<p>(.*?)</p>", body, re.S):
        text = re.sub(r"<[^>]+>", "", m.group(1))
        text = html.unescape(re.sub(r"\s+", " ", text)).strip()
        if len(text) > 80:
            return (text[:297] + "...") if len(text) > 300 else text
    return f"{TITLE}: {SUB}."


def toc_for(body):
    """Section ids live on the wrapping div under --section-divs, headings alongside."""
    out = []
    for m in re.finditer(r'<section id="([^"]+)" class="level2">\s*<h2[^>]*>(.*?)</h2>', body, re.S):
        label = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        out.append((m.group(1), label))
    return out


NAV = """<div class="nav"><span class="navlinks">[ {prev} | <a href="index.html">Contents</a> | {next} ]</span><button type="button" id="mode" class="mode" aria-label="Toggle dark reading mode">Dark mode</button></div>"""


def nav(pages, i):
    prev = f'<a href="{pages[i-1]["file"]}" rel="prev">&lt;&lt; Previous</a>' if i > 0 else "<span class=\"off\">&lt;&lt; Previous</span>"
    nxt = f'<a href="{pages[i+1]["file"]}" rel="next">Next &gt;&gt;</a>' if i < len(pages) - 1 else "<span class=\"off\">Next &gt;&gt;</span>"
    return NAV.format(prev=prev, next=nxt)


HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="{author}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="{book}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<link rel="stylesheet" href="assets/site.css">
{extra}<script>(function(){{try{{if(localStorage.getItem('mr-mode')==='dark')document.documentElement.className='dark';}}catch(e){{}}}})();</script>
</head>
<body>
<div class="page">
"""

FOOT = """</div>
<script>
(function(){
  var b=document.getElementById('mode');if(!b)return;
  function set(d){document.documentElement.className=d?'dark':'';b.textContent=d?'Light mode':'Dark mode';
    try{localStorage.setItem('mr-mode',d?'dark':'light');}catch(e){}}
  set(document.documentElement.className==='dark');
  b.addEventListener('click',function(){set(document.documentElement.className!=='dark');});
})();
</script>
</body>
</html>
"""


def page_head(title, desc, canon, ogtype="article", extra=""):
    return HEAD.format(title=html.escape(title), desc=html.escape(desc), author=AUTHOR,
                       canon=canon, ogtype=ogtype, book=html.escape(TITLE), extra=extra)


def build():
    OUT.mkdir(exist_ok=True)
    order = [l.strip() for l in (ROOT / "book-files.txt").read_text().splitlines() if l.strip()]
    pages = group_pages(order)

    for p in pages:
        p["body"] = render(p["sources"])
        p["title"] = first_heading(p["body"], p["slug"])
        p["desc"] = description(p["body"])
        p["file"] = f"{p['slug']}.html"
        p["sections"] = toc_for(p["body"])

    for i, p in enumerate(pages):
        canon = f"{BASE}/{p['file']}"
        ld = json.dumps({
            "@context": "https://schema.org", "@type": "Chapter",
            "name": p["title"], "description": p["desc"], "url": canon,
            "position": i + 1,
            "isPartOf": {"@type": "Book", "name": TITLE, "author": {"@type": "Person", "name": AUTHOR}},
        })
        head = page_head(f"{p['title']} - {TITLE}", p["desc"], canon,
                         extra=f'<script type="application/ld+json">{ld}</script>\n')
        crumb = (f'<p class="crumb"><a href="index.html">{html.escape(TITLE)}</a> '
                 f'&rsaquo; {html.escape(p["title"])}</p>')
        (OUT / p["file"]).write_text(
            head + crumb + nav(pages, i) + "<hr>\n" + p["body"] + "<hr>\n" + nav(pages, i)
            + f'<p class="foot">{html.escape(TITLE)} &middot; {AUTHOR} &middot; First edition, September 2026</p>'
            + FOOT, encoding="utf-8")

    # ---- contents / landing page ----
    items = []
    for i, p in enumerate(pages):
        subs = "".join(f'<li><a href="{p["file"]}#{sid}">{html.escape(lab)}</a></li>'
                       for sid, lab in p["sections"][:14])
        items.append(f'<li><a href="{p["file"]}">{html.escape(p["title"])}</a>'
                     + (f"<ul>{subs}</ul>" if subs else "") + "</li>")
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "Book", "name": TITLE, "alternateName": SUB,
        "author": {"@type": "Person", "name": AUTHOR}, "datePublished": PUBLISHED,
        "bookEdition": "First edition", "inLanguage": "en", "numberOfPages": 292,
        "url": BASE + "/", "genre": ["Information retrieval", "Machine learning evaluation"],
        "about": ["Information retrieval evaluation", "Retrieval-augmented generation",
                  "Search metrics", "nDCG", "RAG evaluation", "LLM evaluation"],
        "description": ("An operating guide to evaluation metrics for search and retrieval-augmented "
                        "generation: what each metric can tell you, what distorts it, and which "
                        "companion measure exposes that distortion."),
        "workExample": {"@type": "Book", "bookFormat": "https://schema.org/EBook",
                        "potentialAction": {"@type": "ReadAction", "target": PDF}},
    })
    desc = ("Measuring Retrieval is a working book on evaluation metrics for information retrieval "
            "and RAG systems. Seventy metrics across correctness, alignment, integrity and "
            "efficiency, each with a worked example, its failure modes and a recommendation.")
    head = page_head(f"{TITLE} - {SUB}", desc, BASE + "/", ogtype="book",
                     extra=f'<script type="application/ld+json">{ld}</script>\n')
    (OUT / "index.html").write_text(head + f"""
<header class="title">
<h1>{html.escape(TITLE)}</h1>
<p class="sub">{html.escape(SUB)}</p>
<p class="by">{AUTHOR}</p>
<p class="ed">First edition &middot; September 2026</p>
<div class="nav"><span class="navlinks">[ <a href="preface.html">Start reading</a> | <a href="{PDF}">PDF, 292 pages</a> | <a href="https://github.com/Measuring-Retrieval-Book/Measuring-Retrieval-Book-1e">Source</a> ]</span><button type="button" id="mode" class="mode" aria-label="Toggle dark reading mode">Dark mode</button></div>
</header>
<hr>
<section class="dedication"><p>For my mother.</p></section>
<hr>
<h2>About this book</h2>
<p>Retrieval evaluation usually fails at the point of interpretation rather than the point of
calculation. The number was computed correctly and then understood to mean something it never
meant. A system can score 0.84 on context adherence while a third of its correct answers are
ungrounded guesses, and a retriever can reach 57.6% recall with 22% of what it returns duplicated.
Both are published findings, and neither is visible on a dashboard that tracks accuracy.</p>
<p>This book covers roughly seventy metrics across four dimensions. <em>Correctness</em> asks
whether the content is right, <em>alignment</em> asks whether retrieval and generation cooperate,
<em>integrity</em> asks whether it is still right six months later, and <em>efficiency</em> asks
what being right cost you. Every metric gets a diagram, a worked example computed in the open, its
failure modes and a recommendation.</p>
<p>It assumes no background. Terms are defined where they first appear and every calculation runs
in the text, so a reader new to the field can follow it, while the technical content, the findings
and the citations are those of the published literature.</p>
<h2>Contents</h2>
<div class="toc"><ol>{''.join(items)}</ol></div>
<hr>
<p class="foot">{html.escape(TITLE)} &middot; {AUTHOR} &middot; First edition, September 2026 &middot;
<a href="https://github.com/Measuring-Retrieval-Book/Measuring-Retrieval-Book-1e">github.com/Measuring-Retrieval-Book</a></p>
""" + FOOT, encoding="utf-8")

    # ---- assets ----
    (OUT / "assets").mkdir(exist_ok=True)
    shutil.copy2(ROOT / "assets" / "site.css", OUT / "assets" / "site.css")
    dst = OUT / "assets" / "diagrams"
    dst.mkdir(exist_ok=True)
    for f in (ROOT / "assets" / "diagrams").glob("*.svg"):
        shutil.copy2(f, dst / f.name)

    # ---- crawler files ----
    urls = "".join(
        f"<url><loc>{BASE}/{f}</loc><lastmod>2026-09-01</lastmod>"
        f"<priority>{p}</priority></url>\n"
        for f, p in [("", "1.0")] + [(pg["file"], "0.8") for pg in pages])
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    (OUT / ".nojekyll").write_text("")
    print(f"Built {len(pages) + 1} pages into {OUT}")


if __name__ == "__main__":
    sys.exit(build())
