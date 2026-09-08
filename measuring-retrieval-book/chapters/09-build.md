# Build Notes

The book is Pandoc-ready Markdown.

Build a PDF from the `measuring-retrieval-book` directory:

```sh
pandoc metadata.yaml chapters/*.md --css assets/book.css --toc --number-sections -o measuring-retrieval.pdf
```

Build HTML for quick review:

```sh
pandoc metadata.yaml chapters/*.md --css assets/book.css --toc --number-sections -s -o measuring-retrieval.html
```

The SVG diagrams are in `assets/diagrams`. The frontend and backend fractals are in `assets`.
