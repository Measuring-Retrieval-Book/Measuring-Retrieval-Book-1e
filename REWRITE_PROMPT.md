# Task: rewrite *Measuring Retrieval* so that it actually teaches, start to finish, without stopping

You are rewriting a 61-file technical book about evaluation metrics for search and RAG systems. The
book currently reads like a reference card for someone who already knows the material. Your job is
to turn it into something that teaches the material to someone who does not. Work through the whole
manuscript in one continuous run. Do not stop to check in, do not ask questions, and do not
summarize chapters back to me as you go.

## The project

Working directory: `/Users/madhavagaikwad/Desktop/product/metrics/measuring-retrieval-full-book`

The book is *Measuring Retrieval* by Madhava Gaikwad. It builds to a PDF through Pandoc and XeLaTeX.
The manuscript is 61 Markdown files listed in reading order in `book-files.txt`, with 57 in
`chapters/` and 4 in `appendices/`, totalling about 40,000 words.

Thirteen of those files are structural stubs containing only raw LaTeX and HTML part dividers or a
single orientation heading. They have no prose. Skip them and record them as skipped. The other
48 files carry the writing.

## Who you are writing for

Write as though you are explaining each metric to a bright fifteen-year-old who is interested and
paying attention but knows none of the background. That means:

- Define every technical term in plain words the first time it appears in a chapter. Words like
  *corpus*, *relevance judgment*, *rank*, *cutoff*, *graded relevance*, *ideal ranking*, *denominator*,
  *embedding*, *chunk*, *judge*, *drift* and *ground truth* all need this treatment.
- Introduce the concrete situation before the abstraction. Describe what someone is actually trying
  to do and what goes wrong, then name the metric that addresses it.
- Show every calculation step by step, in ordinary sentences, with the real numbers visible.
- Never use a symbol, an acronym or a formula the reader has not been walked through. If a formula
  contains a logarithm, say in plain words what the logarithm does to the numbers and give the
  reader the resulting multipliers, so they can follow the shape of it without computing anything.
- Never assume knowledge from an earlier chapter without a one-line reminder of what it was.

Keep the content itself serious and complete. Do not remove technical material, do not soften real
findings, and do not turn the book into an introduction. Some of the mathematics, particularly in
the drift, counterfactual evaluation and statistical significance chapters, is genuinely hard and
will stay hard. The rule is that the motivation for every metric, and the way you read its number,
must be understandable at that level, even where the machinery underneath is not.

## The voice

Write like an articulate person explaining something to another person, not like a model trying to
make every sentence memorable.

- Use complete, naturally connected sentences. Human explanation is causal and consequential:
  here is the situation, here is why it matters, here is what follows, here is what to do, here is
  what goes wrong if you get it wrong.
- Use ordinary conjunctions and subordinate clauses to carry that logic: *because, although, while,
  when, since, so, which, if, unless.* Do not split one coherent idea into several short dramatic
  sentences.
- Prefer plain words over impressive ones, and specific reasoning over quotable phrasing.

Avoid throughout: manufactured contrasts of the form "It wasn't X. It was Y."; compressed metaphors
and slogans, especially as the opening line of a section; artificial profundity and closing lines
that reach for significance; em dashes used for rhetorical effect, since commas and conjunctions do
the job and the build forbids Unicode dashes anyway; and paragraphs that are obviously bullet points
converted into prose, meaning a stack of short parallel sentences with nothing connecting them.

Before finishing any paragraph, ask whether a thoughtful person would actually say this while
explaining the material to a colleague over coffee. If not, rewrite it.

## Why the book reads badly now

Three separate causes, and you need to fix all three.

**One. The connectives were stripped out.** `scripts/style_lint.py` fails the build on *but, however,
although, while, whereas, though, yet, instead, rather than, unlike, versus, despite, nevertheless,
conversely*, on *not just* and *not only*, and on any *not X ... but Y* construction. The prose was
written to satisfy that filter, so sentences that should have been joined by a subordinate clause
were split apart, and the result reads like a list of assertions.

Your first action, before touching any chapter, is to edit `scripts/style_lint.py` and delete the
rules named `contrast marker`, `expanded contrast` and `direct contrast` from its `rules`
dictionary. Keep the `unicode dash` rule exactly as it is, because the build depends on plain ASCII
hyphens. Leave the rest of the script working so `make lint` still runs.

**Two. The entries state instead of build.** Each metric currently opens with its formula and a
summary of its properties, which reminds a reader who already knows the metric and teaches nothing
to a reader who does not. The section on nDCG, for example, lists its "two contributions" before the
reader has been told what problem graded relevance solves, and uses the term IDCG in its
disadvantages before the text has ever defined it.

**Three. The explanations are locked inside pictures.** All 173 figures were generated from fenced
text blocks in the original sources, so the worked arithmetic, the decision trees and the comparison
panels became PNG images, and the prose around them was written assuming the reader would decode the
picture. The text is still recoverable from the SVG masters, and recovering it is a large part of
this job.

## Recovering the figure text

Every figure reference in the manuscript points at a PNG in `assets/diagrams/`, and the SVG master
sits beside it under the same name. For a figure referenced as
`assets/diagrams/fig-040-rank-rel-1-log2-i-1-contribution.png`, read
`assets/diagrams/fig-040-rank-rel-1-log2-i-1-contribution.svg` and pull its text with:

```sh
grep -o '>[^<]*<' assets/diagrams/<name>.svg | sed 's/^>//;s/<$//' | grep -v '^ *$'
```

Do this for every figure in every file you rewrite. The recovered text will contain the worked
numbers, the decision criteria, or the comparison the figure was making. Carry that content into
the prose so a reader who never looks at the picture can still follow the argument, and leave the
figure exactly where it is as visual support.

Two cautions. The recovered text contains box-drawing characters, arrows, HTML entities such as
`&quot;`, and other decoration. Never paste any of it into the Markdown. Read it, understand what
it says, and write the content out yourself in plain sentences and plain ASCII. Also, the numbers in
those figures are the book's real worked examples, so reproduce them exactly and do not invent
replacements.

## The shape of a metric entry after rewriting

Most sections from Chapter 4 onward describe a single metric. Rewrite each one into this order.
Keep the metadata block at the top as it is, because readers scan it:

```
## X.Y Metric Name

**One-line:** (unchanged, stays terse)
**Formula:** (unchanged, with its figure)
**Facets:** (unchanged)
**Source:** (unchanged)

### The problem it solves      <- NEW section, always first
### The idea
### Worked example
### Advantages
### Disadvantages
### Domain examples
### Recommendation
```

`### The problem it solves` is new and you add it to every metric entry. It describes, in two or
three connected sentences, the concrete situation someone was in and what the metrics available
before this one failed to tell them. It must not mention the metric's formula.

`### The idea` explains how the metric works, building each piece in the order the reader needs it,
defining terms as they arrive.

`### Worked example` must now carry the arithmetic in readable sentences, using the numbers you
recovered from the figure, so the reader can follow the calculation from the inputs to the final
value without looking at the image.

Delete the standalone `### Diagram` heading wherever it appears and move the figure it contained
inline into whichever section it supports, keeping the image reference itself unchanged.

`### Advantages`, `### Disadvantages`, `### Domain examples` and `### Recommendation` keep their
names and stay as they are structurally. Their bullets stay bullets and keep their bold lead-in
labels, and the sentences inside them get the same explanatory treatment as everything else.

## Calibration example

This is the current text of section 5.3, and it is representative of the problem:

> **One-line:** Sum the graded relevance of each result, discounted logarithmically by position,
> then normalize by the best possible ordering.
>
> ### The idea
>
> Two contributions, and they are separable:
>
> 1. **Graded relevance.** Documents receive scores from 0-3 (or 0-4). This alone is a major advance
>    over everything in Chapter 4.
> 2. **Logarithmic discount.** `1/log2(i+1)` - gentler than MRR's `1/i`, and chosen because it models
>    a user whose attention declines gradually.

This is the level and voice to write at instead:

> ### The problem it solves
>
> Every metric up to this point asks a yes or no question about each result, so a document is either
> relevant or it is not. Imagine asking a librarian to look through ten books your search returned
> and mark the useful ones. If the only thing they are allowed to write is yes or no, then a book
> that answers your question completely and a book that mentions your topic once both get the same
> yes, and you have thrown away most of what the librarian actually knew. DCG was designed to keep
> that information.
>
> ### The idea
>
> The first change is that each result gets a score instead of a label, usually a whole number from
> 0 to 3, where 3 means the result is exactly what the person wanted and 0 means it is useless.
> These scores come from a human rater and are called graded relevance judgments.
>
> The second change is that a result near the top of the list counts for more than the same result
> further down, because people read from the top and often stop partway. So each result's score is
> divided by a number that grows as you move down the list. That number is log2(i+1), where i is the
> position, and you do not need to work the logarithm out yourself to use it. What matters is the
> shape it produces: position 1 keeps its full score, position 2 keeps about 63% of it, position 3
> keeps half, and position 5 keeps about 39%. The decline is gradual, which is meant to reflect a
> reader whose attention fades rather than stops.
>
> ### Worked example
>
> Suppose five results come back and a rater scores them, in order, 3, 0, 2, 1 and 3. The first
> result sits at position 1 and keeps its full value, contributing 3.000. The second was judged
> useless, so it contributes nothing no matter where it sits. The third contributes 2 multiplied by
> 0.500, which is 1.000. The fourth contributes 1 multiplied by 0.431, which is 0.431. The fifth
> contributes 3 multiplied by 0.387, which is 1.161. Adding those together gives DCG@5 = 5.592.
>
> That number is hard to interpret on its own, because a query that happens to have several highly
> relevant documents can reach a larger total than a query that only has one, without the search
> system having done any better on it. So you compare the result against the best score those same
> five judgments could possibly have produced, which means putting them in their ideal order of
> 3, 3, 2, 1, 0 and running the same calculation. That ideal total is called IDCG, and here it comes
> to 6.324. Dividing one by the other gives nDCG@5 = 5.592 / 6.324 = 0.884. Because every query is
> now scored against its own ceiling, the results can be averaged across a whole set of queries.

Notice what changed. The reader is given a situation before a formula, every term is defined where
it first appears, the logarithm is explained by its effect rather than its definition, the
arithmetic is fully visible in the text, and normalization is introduced because a problem made it
necessary. Write everything at that level.

## What you must preserve exactly

1. **Chapter and section headings**, with their existing numbering and titles. Do not add, remove,
   merge or reorder chapters or numbered sections. The only heading changes permitted are the ones
   specified above: adding `### The problem it solves` and removing `### Diagram`.
2. **Every figure reference**, byte for byte, including its attribute block, for example
   `![The Log Discount Is Gentle](assets/diagrams/fig-039-the-log-discount-is-gentle.png){.diagram-figure width=96%}`.
   Do not correct the odd capitalization in figure alt text, because those strings are tracked in
   `DIAGRAM_LEDGER.md`.
3. **Every fenced code block**, including the raw `{=latex}` and `{=html}` blocks. Never edit inside
   a fence.
4. **Every Markdown table**, including its cell text.
5. **Every formula, metric value, statistic, percentage, dollar figure, citation, author name, venue,
   arXiv identifier and URL.** Invent nothing and change nothing factual. If a claim looks wrong,
   keep it and note the file and line in the log instead of correcting it.
6. **Second person voice, present tense, American spelling, and plain ASCII hyphens.**

## Length

Let the text grow as much as teaching it properly requires. Doubling a metric entry is expected and
fine, and a substantially longer PDF is an acceptable outcome. None of that growth should be
padding, since every added sentence should be doing explanatory work the original left for the
reader to reconstruct on their own.

## How to run

Edit the files in place. Do not create a parallel directory and do not write backup copies.

Work through `book-files.txt` in order. For each file:

1. Read the file.
2. Extract the text from the SVG master of every figure it references.
3. Rewrite the file completely, applying everything above.
4. Write it back to the same path.
5. Append one line to `REWRITE_LOG.md` at the manuscript root, in the form
   `<path> | <before words> -> <after words> | <figures recovered> | <note or "ok">`.
6. Move straight on to the next file.

Manage your context deliberately, because this is a long run. Work on one file at a time, do not
keep finished files in context, and do not re-read files you have completed. When something is
ambiguous, choose the option that teaches better, note it in the log, and keep going.

Do not stop between files, do not narrate progress, and do not ask for approval to continue. The run
ends when every file in `book-files.txt` has been rewritten or recorded as a skipped stub.

## When you reach the end

1. Run `python3 scripts/style_lint.py` and report the result. It should pass once the three contrast
   rules are gone, and any remaining findings will be Unicode dashes you introduced, which you should
   fix.
2. Attempt `make pdf`. The Makefile hardcodes an absolute Node path under `~/.cache/codex-runtimes/`,
   so the diagram render step may fail. If it does, report the error plainly and stop, without trying
   to repair the toolchain, install anything or edit the Makefile.
3. Give a short closing report: files rewritten, files skipped, total word count before and after,
   how many figures you recovered text from, the lint result, the build result, and any factual
   oddities you logged.
