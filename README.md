# Measuring Retrieval

**A working book on metrics, evidence, and evaluation design for information retrieval and RAG.**
By Madhava Gaikwad.

Retrieval evaluation usually fails at the point of interpretation rather than the point of
calculation. The number was computed correctly and then understood to mean something it never
meant. This book is an operating guide to the metrics: what each one can tell you, what distorts
it, and which companion measure exposes that distortion.

## Read it

| Edition | Where |
|---|---|
| **HTML** | [`measuring-retrieval-full-book/index.html`](measuring-retrieval-full-book/index.html) - full book, with contents, vector figures |
| **PDF** | [`measuring-retrieval-full-book/measuring-retrieval-full.pdf`](measuring-retrieval-full-book/measuring-retrieval-full.pdf) - 323 pages, 7 x 10 in |

## What is in it

Seventy-odd metrics across four dimensions, each one asking a different question. Correctness asks
whether the content is right. Alignment asks whether retrieval and generation cooperate. Integrity
asks whether it is still right six months later. Efficiency asks what being right cost you.

- **Volume I, Chapters 0-12** - classical information retrieval: set-based and rank-based metrics,
  incomplete judgments, rank comparison, diversity, fairness, online and counterfactual evaluation,
  significance, and cost.
- **Part A, Alignment** - contribution metrics, attribution, quadrant diagnosis, machine-utility
  ranking.
- **Part B, Integrity** - representation drift, version drift, robustness, judge drift.
- **Part C, Correctness** - claim decomposition, RAGAS, RAGChecker, ALCE, citation faithfulness,
  Trust-Score, sufficiency.
- **Part D, Efficiency** - cost centres, index and query time, token economics, evaluation cost.
- **Chapters 13-15** - judge reliability, test-set quality, and narrowing seventy metrics down to
  eight you actually instrument.
- **Appendices** - consolidated catalogue, an evidence ledger carrying the verification status of
  roughly 130 citations, twelve visual synthesis plates, and a figure archive.

Every metric gets a diagram, a worked example computed in the open, its failure modes, and a
recommendation.

## Build it

```sh
cd measuring-retrieval-full-book
make pdf     # Pandoc + XeLaTeX, 7 x 10 in
make html    # single-file HTML with contents; also written to index.html
make lint    # house-style checks
```

The PDF build rasterizes the 173 SVG diagram masters to PNG through Node and Sharp. The HTML
edition points at the SVG masters instead, so it stays sharp at any zoom and the figures come to
828K rather than 31M. Rendered PNGs are not tracked here because `make diagrams` regenerates them.

`NODE` in the Makefile is an absolute path and will need changing on another machine.

## Provenance

The manuscript is built from nine Markdown sources and one slide deck.
[`SOURCE_LEDGER.md`](measuring-retrieval-full-book/SOURCE_LEDGER.md) records every source with its
size and a content hash, and [`DIAGRAM_LEDGER.md`](measuring-retrieval-full-book/DIAGRAM_LEDGER.md)
maps each of the 173 figures back to the source file and line it came from. Appendix B carries the
citation verification status, including two corrections of the author's own errors.

## Repository layout

```
*.md                          the nine source whitepapers
measuring-retrieval-full-book/   the book: chapters, appendices, assets, build
measuring-retrieval-book/        an earlier, much shorter draft
```
