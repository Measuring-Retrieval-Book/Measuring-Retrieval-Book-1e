# Measuring Retrieval Book

This folder contains a Pandoc-ready Markdown book generated from the top-level metrics whitepapers in this directory.

The generator skipped the `bk/` folder.

## Build

```sh
cd /Users/madhavagaikwad/Desktop/product/metrics/measuring-retrieval-book
pandoc metadata.yaml chapters/*.md --css assets/book.css --toc --number-sections -o measuring-retrieval.pdf
```

## Files

- `chapters/*.md`: book chapters
- `assets/book.css`: PDF and HTML styling
- `assets/diagrams/*.svg`: colorful explanatory diagrams
- `assets/fractal-light.svg`: frontend fractal
- `assets/fractal-dark.svg`: backend fractal
