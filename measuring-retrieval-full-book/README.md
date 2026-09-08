# Measuring Retrieval: Full Book Edition

By **Madhava Gaikwad**.

This package builds the complete source-derived manuscript as a production PDF and HTML
edition. The current PDF is 283 pages. It includes 61 ordered manuscript files, 173 rebuilt
color diagrams, a consolidated catalogue, twelve visual synthesis plates, and a complete
diagram ledger.

## Build

```sh
make pdf
make html
make lint
```

The PDF build uses Pandoc and XeLaTeX. Node.js and Sharp render the SVG diagram masters to PNG.
The page size is 7 by 10 inches.

## Editorial guarantees

- The manuscript covers the nine explicit source files listed in `SOURCE_LEDGER.md`.
- The private `bk` directory stays outside the source list.
- Every fenced source block has a stable color figure asset.
- The CKA correction and retrieval-robustness definitions are integrated into their chapters.
- The catalogue remains available as a full appendix.

## Files

- `chapters/`: ordered manuscript chapters and part dividers
- `appendices/`: catalogue, evidence status, and visual synthesis
- `assets/diagrams/`: editable SVG figures plus rendered PNG files
- `assets/covers/`: dark front and light back fractal artwork
- `SOURCE_LEDGER.md`: source completeness record
- `DIAGRAM_LEDGER.md`: figure provenance record
- `scripts/style_lint.py`: house-style checks
