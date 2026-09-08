# Preface {.unnumbered}

When you build a search system, or a system that feeds search results to a language model,
you eventually have to answer a simple question: is it any good? The usual way to answer it
is to compute a number, put the number on a dashboard, and watch it. This book is about what
those numbers actually mean, because a number that is computed correctly can still be read
wrongly, and a system that is measured wrongly tends to get built wrongly.

Every metric in this book carries a set of assumptions with it. It assumes a particular kind
of reader looking at the results, a particular thing being counted, a particular way of
deciding what counts as a correct answer, and a particular point in the system where the
measurement is taken. The number is useful when those assumptions match the system you are
actually reviewing, and it quietly misleads you when they do not. Because choosing what to
measure ends up shaping what gets built, evaluation turns out to be a design activity rather
than a reporting one.

This edition brings the complete classical information retrieval material and the newer RAG
material together into a single manuscript. It keeps the worked calculations, the
implementation guidance, the evidence ledgers, and the failure sketches from the sources it
was built from, and where a later correction revised an earlier section, the correction
appears beside the section it revises. Throughout, one working rule decides whether a metric
belongs in the book at all, which is that it has to answer an operational question no other
metric already answers.

## Reading paths

You do not have to read this book in order, although Chapters 0 through 3 are worth reading
first whatever your goal is, since everything later depends on the vocabulary they set up.

| Goal | Starting point |
|---|---|
| Learn retrieval evaluation in sequence | Chapter 0 |
| Diagnose a RAG pipeline | Part II, then Part IV |
| Choose a retriever or embedder | Part III |
| Choose a generator | Chapters C.7 and A.3 |
| Build an evaluation set | Chapter 14 |
| Select a production dashboard | Chapter 15 |

## Diagram system

Every metric in this book gets a figure, and the figures are meant to be part of the
argument rather than decoration. Each one is a sketch you could redraw on a whiteboard in
about thirty seconds, which matters because a metric you can sketch quickly is a metric you
can defend in a design review. The color coding is consistent throughout: cyan marks flow
through a system, gold marks a decision, coral marks a failure, emerald marks the conditions
under which something works, and indigo marks the structure of a system.

The prose does not depend on the figures. Wherever a figure carries a calculation or a
decision rule, the same content is worked through in the text as well, so you can follow the
argument without stopping to study the picture.

## Source policy

The manuscript is built from nine Markdown sources and one PowerPoint deck, and it keeps two
records of where its material came from. The source ledger lists every source file, its
size, which chapters it fed, and how many figures came out of it, while the diagram ledger
maps each figure back to the exact line of the source it was generated from. Appendix B goes
further and records the verification status of roughly 130 citations, including two places
where earlier versions of this material got something wrong and the correction that followed.

```{=latex}
\mainmatter
```
