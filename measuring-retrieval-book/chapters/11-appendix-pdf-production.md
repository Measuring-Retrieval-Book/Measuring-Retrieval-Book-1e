# Appendix B. PDF Production Checklist

## Before building

Run a structure scan:

```sh
rg -n "^#|^##|^###" chapters
```

## Build

```sh
make pdf
```

## Review

Check the cover, table of contents, diagrams, tables, and page breaks.

## Suggested next production pass

1. Replace placeholder author metadata.
2. Add citation keys if the PDF needs formal references.
3. Add chapter openers from the original whitepaper source where more narrative depth is wanted.
4. Add a glossary for teams new to IR.
