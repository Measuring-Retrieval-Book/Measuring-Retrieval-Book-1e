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


# Keyword-bearing URLs and hand-written meta descriptions. Both matter for search:
# "chapter-04.html" tells a crawler nothing, and a description cut from the first
# paragraph tends to start mid-thought and run past the ~155 characters shown.
SLUGS = {
    "preface": "preface",
    "chapter-00": "how-to-read-this-book",
    "chapter-01": "four-dimensions-of-retrieval-evaluation",
    "chapter-02": "facet-system-unit-supervision-stage",
    "chapter-03": "signals-are-not-metrics",
    "chapter-04": "set-based-metrics-precision-recall-f1",
    "chapter-05": "rank-based-metrics-mrr-map-ndcg-err-rbp",
    "chapter-06": "incomplete-judgments-bpref-infap-pooling",
    "chapter-07": "comparing-rankings-rbo-kendall-tau",
    "chapter-08": "diversity-and-novelty-alpha-ndcg",
    "chapter-09": "fairness-and-exposure-in-ranking",
    "chapter-10": "online-and-counterfactual-evaluation",
    "chapter-11": "significance-testing-and-reporting",
    "chapter-12": "efficiency-cost-and-time",
    "classical-conclusion": "classical-ir-conclusion",
    "a1-alignment": "retriever-generator-alignment",
    "a2-contribution": "contribution-metrics-erag-dig-seper",
    "a3-quadrants": "cue-and-mirage-quadrant-metrics",
    "a4-machine-utility": "udcg-machine-utility-ranking",
    "a5-summary": "alignment-summary",
    "b1-integrity": "integrity-and-drift",
    "b2-representation-drift": "embedding-model-drift-cka",
    "b3-version-drift": "corpus-and-version-drift-versionrag",
    "b4-robustness": "retrieval-robustness-metrics",
    "b5-judge-drift": "llm-judge-drift",
    "b6-integrity-summary": "integrity-summary",
    "c1-correctness": "correctness-and-grounding-in-rag",
    "c2-claim-decomposition": "claim-decomposition-factscore",
    "c3-ragas": "ragas-evaluation-metrics",
    "c4-ragchecker": "ragchecker-nine-metrics",
    "c5-alce": "alce-citation-precision-and-recall",
    "c6-citation-faithfulness": "citation-faithfulness-post-rationalization",
    "c7-trust-score": "trust-score-refusal-and-attribution",
    "c8-metric-audit": "metric-confounding-audit",
    "c9-sufficiency": "sure-rag-evidence-sufficiency",
    "c10-correctness-summary": "correctness-summary",
    "d1-cost-centres": "rag-cost-centres",
    "d2-index-time": "index-time-metrics",
    "d3-query-time": "query-latency-and-ttft",
    "d4-token-economics": "token-economics-and-redundancy",
    "d5-evaluation-cost": "cost-of-evaluation",
    "d6-efficiency-summary": "efficiency-summary",
    "chapter-13": "can-you-trust-your-llm-judge",
    "chapter-14": "is-your-test-set-any-good",
    "chapter-15": "choosing-eight-metrics-to-instrument",
    "closing": "closing",
    "appendix-a-catalogue": "metric-catalogue",
    "appendix-b-evidence": "references",
    "appendix-c-figure-archive": "figure-archive",
}

DESCRIPTIONS = {
    "preface": "Why retrieval evaluation fails at interpretation rather than calculation, how this book is organized, and the reading paths through it.",
    "chapter-00": "How to read this book: who it is for, the per-metric template, and why a green dashboard is not the same as a system you can trust.",
    "chapter-01": "The four questions every retrieval metric answers: correctness, alignment, integrity and efficiency, and why four green metrics is not coverage.",
    "chapter-02": "The facet system: unit of analysis, supervision, stage and verification tier, and why you never average metrics across units.",
    "chapter-03": "Signals, parameters and metrics are three different things. Cosine similarity is a signal; BM25's b is a knob; only one of them belongs in a report.",
    "chapter-04": "Precision, recall, F1 and precision@K explained from scratch, with worked examples, how each is gamed, and why plain accuracy fails in retrieval.",
    "chapter-05": "MRR, MAP, DCG and nDCG, ERR and RBP, each worked by hand. Every rank metric encodes a theory of how its reader scans a list.",
    "chapter-06": "What to do when you do not know what is relevant: bpref, infAP, pooling bias and assessor agreement under incomplete judgments.",
    "chapter-07": "Rank-biased overlap and Kendall's tau for comparing two rankings without labels, and the cheapest drift protocol available.",
    "chapter-08": "Subtopic recall, alpha-nDCG and ERR-IA. Redundant passages cost a search user a slot and cost a RAG system context budget.",
    "chapter-09": "Fairness of exposure and equity of attention: what a ranking does to the things being ranked, and the corpus-health signal it gives you free.",
    "chapter-10": "Interleaving, inverse propensity scoring and the 2008 result that eight absolute click metrics do not reliably reflect retrieval quality.",
    "chapter-11": "Significance testing, statistical power, weak baselines and the reporting checklist. Good metrics badly compared produced a decade of illusory progress.",
    "chapter-12": "Time-biased gain, session metrics and the cost-quality frontier, plus the k-sweep experiment almost nobody runs.",
    "classical-conclusion": "The five claims from classical information retrieval that survive into the RAG era, and the three gaps the classical chapters cannot close.",
    "a1-alignment": "Alignment metrics measure the interface between retriever and generator, which is the failure both components can pass while the system fails.",
    "a2-contribution": "eRAG, DIG, SePer and Gain all ablate a passage and measure what changed. They are one family, and you should report exactly one of them.",
    "a3-quadrants": "CUE and MIRAGE sort every query into diagnostic quadrants, separating retriever-fixable failures from failures intrinsic to the model.",
    "a4-machine-utility": "UDCG rebuilds nDCG for a language model reader, with learned position weights and negative weight for passages that actively harm the answer.",
    "a5-summary": "What to put on an alignment dashboard: one contribution metric, one attribution metric, quadrant diagnosis and machine-utility ranking.",
    "b1-integrity": "Four separate things drift in a retrieval system: the corpus, the embedder, the queries and the judge. Each needs a different detector.",
    "b2-representation-drift": "CKA, Jaccard and rank similarity for embedding model comparison, and why every embedder swap is a high-risk change at RAG-typical k.",
    "b3-version-drift": "VersionQA and version-sensitive retrieval. Baselines detect an undocumented document change between 0 and 10 percent of the time.",
    "b4-robustness": "No-degradation rate, retrieval size and order robustness, and the sample-level trade-off that an 80 percent aggregate score conceals.",
    "b5-judge-drift": "There is no metric for LLM judge drift. The interim protocol: pin the snapshot, freeze an anchor set, track Krippendorff's alpha.",
    "b6-integrity-summary": "The drift work worth doing this week, this quarter, and the two problems to accept as unsolved.",
    "c1-correctness": "In RAG, correctness splits from groundedness. A correct and ungrounded answer is the failure that survives every review process.",
    "c2-claim-decomposition": "The extract-verify-aggregate pipeline behind nearly every grounding metric, and how the reference text you verify against decides the metric.",
    "c3-ragas": "RAGAS faithfulness, answer relevance and context relevance, plus the drift between the paper's three metrics and the library's four.",
    "c4-ragchecker": "RAGChecker's nine claim-level metrics from one extraction pass, the three worth promoting to a dashboard, and the trilemma it documents.",
    "c5-alce": "Citation precision and recall, and the leave-one-out test that catches a model citing everything to be safe.",
    "c6-citation-faithfulness": "A citation can support a claim the model never read. Post-rationalization affects up to 57 percent of citations and correctness cannot see it.",
    "c7-trust-score": "Trust-Score measures whether a model is suitable for RAG, including whether it correctly refuses when the context is insufficient.",
    "c8-metric-audit": "How to audit a composite metric before trusting it: decompose the variance, because a rate term can masquerade as a quality improvement.",
    "c9-sufficiency": "Evidence sufficiency is a property of the retrieved set. Two relevant passages can contradict each other, and passage-level scoring cannot see it.",
    "c10-correctness-summary": "Which grounding metrics to run given what you have, and the four rules that keep them honest.",
    "d1-cost-centres": "In RAG the efficiency knobs are the quality knobs. The four cost centres: index time, query time, tokens, and evaluation itself.",
    "d2-index-time": "Index-time metrics, and why timing a full rebuild is the number that gates every drift policy you have.",
    "d3-query-time": "Time-to-first-token against total latency, and why retrieval latency is the part the user waits through with nothing on screen.",
    "d4-token-economics": "Pairwise redundancy and exclusive hit rate. Duplicated context is bought at full token price and contributes no grounding.",
    "d5-evaluation-cost": "What each evaluation metric costs per query, and how to tier a suite so the full stack is not billed on every commit.",
    "d6-efficiency-summary": "What to measure across index time, query time, tokens and evaluation, and the one insight that ties them together.",
    "chapter-13": "Your LLM judge is an uncalibrated measuring instrument. Of 63 surveyed papers, 41 used one and six checked it against humans.",
    "chapter-14": "Coverage gaps, benchmark leakage and synthetic data quality. Score your benchmark with retrieval disabled and see what the gap tells you.",
    "chapter-15": "Narrowing seventy metrics to the eight worth instrumenting, what to leave off the dashboard, and a 90-day rollout.",
    "closing": "Evaluation is a design activity. Whatever you measure your system is shaped toward, and whatever you fail to measure it is free to sacrifice.",
    "appendix-a-catalogue": "Every metric in the book in one table, tagged by dimension, unit of analysis, supervision required and pipeline stage.",
    "appendix-b-evidence": "The full reference list for Measuring Retrieval, grouped by part: classical IR, alignment, integrity, correctness and meta-evaluation.",
    "appendix-c-figure-archive": "Figures from the source material that sit outside the chapter path, collected here rather than discarded.",
}

# Files that carry no readable content of their own.
STUB = re.compile(r"(part-[a-z]+|orientation|dedication)\.md$")


def base_name(path: Path) -> str:
    return re.sub(r"^\d+[a-z]?-", "", path.stem)


def slug(path: Path) -> str:
    return SLUGS.get(base_name(path), base_name(path))


def group_pages(order):
    """Fold stub files into the content page that follows them."""
    pages, pending = [], []
    for rel in order:
        path = ROOT / rel
        if STUB.search(rel):
            pending.append(path)
            continue
        pages.append({"sources": pending + [path], "slug": slug(path),
                      "key": base_name(path)})
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
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Measuring Retrieval, first edition, September 2026, by Madhava Gaikwad">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{img}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
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
                       canon=canon, ogtype=ogtype, book=html.escape(TITLE), extra=extra,
                       img=f"{BASE}/assets/og-card.png")


def build():
    OUT.mkdir(exist_ok=True)
    order = [l.strip() for l in (ROOT / "book-files.txt").read_text().splitlines() if l.strip()]
    pages = group_pages(order)

    for p in pages:
        p["body"] = render(p["sources"])
        p["title"] = first_heading(p["body"], p["slug"])
        p["desc"] = DESCRIPTIONS.get(p["key"], description(p["body"]))
        p["file"] = f"{p['slug']}.html"
        p["sections"] = toc_for(p["body"])

    for i, p in enumerate(pages):
        canon = f"{BASE}/{p['file']}"
        crumbs = json.dumps({
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": TITLE, "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": p["title"], "item": canon},
            ],
        })
        ld = json.dumps({
            "@context": "https://schema.org", "@type": "Chapter",
            "name": p["title"], "description": p["desc"], "url": canon,
            "position": i + 1,
            "isPartOf": {"@type": "Book", "name": TITLE, "author": {"@type": "Person", "name": AUTHOR}},
        })
        head = page_head(f"{p['title']} - {TITLE}", p["desc"], canon,
                         extra=f'<script type="application/ld+json">{ld}</script>\n'
                               f'<script type="application/ld+json">{crumbs}</script>\n')
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
    desc = ("A working book on evaluation metrics for search and RAG: seventy metrics, each with a "
            "worked example, its failure modes, and what to actually put on a dashboard.")
    head = page_head(f"{TITLE} - Metrics for IR and RAG evaluation", desc, BASE + "/", ogtype="book",
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
    shutil.copy2(ROOT / "assets" / "og-card.png", OUT / "assets" / "og-card.png")
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
    nf = page_head(f"Page not found - {TITLE}",
                   "That page does not exist. The contents page lists every chapter of Measuring Retrieval.",
                   BASE + "/404.html",
                   extra='<meta name="robots" content="noindex, follow">\n')
    (OUT / "404.html").write_text(
        nf + '<header class="title"><h1>Page not found</h1>'
        '<p class="sub">That page does not exist, or it has moved.</p>'
        '<div class="nav"><span class="navlinks">[ <a href="index.html">Contents</a> | '
        '<a href="preface.html">Start reading</a> ]</span>'
        '<button type="button" id="mode" class="mode">Dark mode</button></div></header><hr>'
        f'<p class="foot">{html.escape(TITLE)} &middot; {AUTHOR}</p>' + FOOT, encoding="utf-8")

    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    (OUT / ".nojekyll").write_text("")
    print(f"Built {len(pages) + 1} pages into {OUT}")


if __name__ == "__main__":
    sys.exit(build())
