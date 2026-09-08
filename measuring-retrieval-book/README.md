# Measuring Retrieval Book

An early, much shorter draft, superseded by `measuring-retrieval-full-book/`. Kept for reference.

## Build

```sh
pandoc metadata.yaml chapters/*.md --css assets/book.css --toc --number-sections -o measuring-retrieval.pdf
```

## Files

- `chapters/*.md`: book chapters
- `assets/book.css`: PDF and HTML styling
- `assets/diagrams/*.svg`: colorful explanatory diagrams
- `assets/fractal-light.svg`: frontend fractal
- `assets/fractal-dark.svg`: backend fractal
