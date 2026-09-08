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
| **HTML** | [measuring-retrieval-book.github.io](https://measuring-retrieval-book.github.io/Measuring-Retrieval-Book-1e/) - one page per chapter, with contents and a dark reading mode |
| **PDF** | [`measuring-retrieval-full-book/measuring-retrieval-full.pdf`](measuring-retrieval-full-book/measuring-retrieval-full.pdf) - 292 pages, 7 x 10 in |

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
- **Appendices** - a consolidated catalogue of every metric, the full reference list, twelve
  visual synthesis plates, and a figure archive.

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

## Repository layout

```
measuring-retrieval-full-book/   the book: chapters, appendices, assets, build
docs/                            the HTML edition, served by GitHub Pages
*.md                             source material the book was assembled from
```

## Licence and citation

Text and figures are the author's. If you cite the book:

> Gaikwad, M. (2026). *Measuring Retrieval: A working book on metrics, evidence, and evaluation
> design*. First edition.
