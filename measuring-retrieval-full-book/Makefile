PYTHON ?= python3
PANDOC ?= pandoc
NODE ?= /Users/madhavagaikwad/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node
NODE_PATH ?= /Users/madhavagaikwad/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules
BOOK = measuring-retrieval-full.pdf
HTML = measuring-retrieval-full.html
FILES = cover.md \
	chapters/00-dedication.md \
	chapters/00-preface.md \
	chapters/00a-part-classical.md \
	chapters/01-chapter-00.md \
	chapters/02-chapter-01.md \
	chapters/03-chapter-02.md \
	chapters/04-chapter-03.md \
	chapters/05-chapter-04.md \
	chapters/06-chapter-05.md \
	chapters/07-chapter-06.md \
	chapters/08-chapter-07.md \
	chapters/09-chapter-08.md \
	chapters/10-chapter-09.md \
	chapters/11-chapter-10.md \
	chapters/12-chapter-11.md \
	chapters/13-chapter-12.md \
	chapters/14-classical-conclusion.md \
	chapters/15-part-alignment.md \
	chapters/15a-alignment-orientation.md \
	chapters/16-a1-alignment.md \
	chapters/17-a2-contribution.md \
	chapters/18-a3-quadrants.md \
	chapters/19-a4-machine-utility.md \
	chapters/20-a5-summary.md \
	chapters/21-part-integrity.md \
	chapters/21a-integrity-orientation.md \
	chapters/22-b1-integrity.md \
	chapters/23-b2-representation-drift.md \
	chapters/24-b3-version-drift.md \
	chapters/25-b4-robustness.md \
	chapters/26-b5-judge-drift.md \
	chapters/27-b6-integrity-summary.md \
	chapters/28-part-correctness.md \
	chapters/28a-correctness-orientation.md \
	chapters/29-c1-correctness.md \
	chapters/30-c2-claim-decomposition.md \
	chapters/31-c3-ragas.md \
	chapters/32-c4-ragchecker.md \
	chapters/33-c5-alce.md \
	chapters/34-c6-citation-faithfulness.md \
	chapters/35-c7-trust-score.md \
	chapters/36-c8-metric-audit.md \
	chapters/37-c9-sufficiency.md \
	chapters/38-c10-correctness-summary.md \
	chapters/39-part-efficiency.md \
	chapters/39a-efficiency-orientation.md \
	chapters/40-d1-cost-centres.md \
	chapters/41-d2-index-time.md \
	chapters/42-d3-query-time.md \
	chapters/43-d4-token-economics.md \
	chapters/44-d5-evaluation-cost.md \
	chapters/45-d6-efficiency-summary.md \
	chapters/46-part-operation.md \
	chapters/46a-operation-orientation.md \
	chapters/47-chapter-13.md \
	chapters/48-chapter-14.md \
	chapters/49-chapter-15.md \
	chapters/50-closing.md \
	appendices/appendix-a-catalogue.md \
	appendices/appendix-b-evidence.md \
	appendices/appendix-c-figure-archive.md \
	back-cover.md

.PHONY: all diagrams pdf html site lint clean

all: pdf html site

diagrams:
	$(PYTHON) scripts/polish_svg_text.py
	NODE_PATH=$(NODE_PATH) $(NODE) scripts/render_diagrams.cjs

pdf: diagrams
	$(PANDOC) $(FILES) --metadata-file=metadata.yaml --resource-path=. --from=markdown+raw_tex-implicit_figures --pdf-engine=xelatex --top-level-division=chapter -o $(BOOK)

html: diagrams
	$(PANDOC) $(FILES) --metadata-file=metadata.yaml --resource-path=. --from=markdown+raw_tex-implicit_figures --standalone --toc --toc-depth=2 --section-divs --css=assets/book.css -o $(HTML)
	$(PYTHON) scripts/html_use_svg.py $(HTML)
	cp $(HTML) index.html

site: diagrams
	rm -f ../docs/*.html ../docs/sitemap.xml
	$(PYTHON) scripts/build_site.py

lint:
	$(PYTHON) scripts/style_lint.py

clean:
	find assets/diagrams -maxdepth 1 -type f -name '*.png' -delete
	rm -f $(BOOK) $(HTML) index.html
	rm -rf ../docs
