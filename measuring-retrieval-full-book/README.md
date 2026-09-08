# Measuring Retrieval: Full Book Edition

By **Madhava Gaikwad**.

This package builds the book as a production PDF and as a multi-page HTML edition. The PDF runs
to 292 pages at 7 by 10 inches. The manuscript is 62 ordered files with 173 color diagrams, a
consolidated metric catalogue, a full reference list, and a figure archive.

## Build

```sh
make pdf     # Pandoc + XeLaTeX
make html    # single-file HTML
make site    # multi-page HTML edition into ../docs
make lint
```

The PDF build uses Pandoc and XeLaTeX. Node.js and Sharp render the SVG diagram masters to PNG.
The page size is 7 by 10 inches.

## Editorial guarantees

- Every figure has a stable SVG master, and the prose never depends on reading one.
- The PDF and the HTML edition are built from the same Markdown.
- `make lint` enforces plain ASCII hyphens, which the fonts require.

## Files

- `chapters/`: ordered manuscript chapters and part dividers
- `appendices/`: catalogue, evidence status, and visual synthesis
- `assets/diagrams/`: editable SVG figures plus rendered PNG files
- `assets/covers/`: dark front and light back fractal artwork
- `DIAGRAM_LEDGER.md`: build-time index mapping figures to assets
- `scripts/build_site.py`: builds the multi-page HTML edition into `docs/`
- `scripts/style_lint.py`: house-style checks
