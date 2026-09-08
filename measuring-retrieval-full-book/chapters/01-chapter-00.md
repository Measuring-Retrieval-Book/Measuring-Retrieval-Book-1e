# Chapter 0 - How To Read This Book

## 0.1 Who this is for

You are building or maintaining a system that finds things. It might be a classical search
engine running over a collection of documents, or it might be a RAG pipeline, which is a
setup where a search step pulls in some documents and a language model writes an answer using
them. Most likely it is a mixture of the two, where you inherited the search component,
somebody else chose the language model, and nobody is entirely sure which of the two is at
fault when the answers come out wrong.

You almost certainly have a dashboard already, and the numbers on it are green, although you
are not especially confident that they mean what you assume they mean.

That last sentence is the reason this book exists. Retrieval evaluation usually fails at the
point of interpretation rather than the point of calculation, which is to say that the number
was computed correctly and then understood to mean something it never meant. A system can
score 0.84 on context adherence, which sounds close to perfect, while still producing a third
of its correct answers as guesses that were not actually supported by anything it retrieved.
A search component can find 57.6% of the relevant material while 22% of what it returns is
duplicated content that crowds out something it never found at all. Both of those are real
published findings, and neither one is visible on a dashboard that tracks accuracy.

## 0.2 Scope and companion surveys

Two survey papers map the field broadly and are worth keeping beside this book, because they
cover the breadth while this book concentrates on depth.

| Survey | What it covers | ID |
|---|---|---|
| Gan et al. (2025) | Most comprehensive RAG evaluation survey; performance, factual accuracy, safety, computational efficiency | [arXiv:2504.14891](https://arxiv.org/abs/2504.14891) |
| Brehme, Ströhle & Breu (2025) | Systematic review of 63 papers; uniquely covers indexing and dataset generation | [arXiv:2504.20119](https://arxiv.org/abs/2504.20119) |

This book is an operating guide, so it is organized around what to do. For each metric it
tells you what the metric can tell you, what will distort it, and which companion measure
will reveal that distortion when it happens.

## 0.3 The diagram convention

Every metric in this book gets a diagram, and the diagrams deliberately use a plain visual
vocabulary of stick figures, boxes, color and a caption that carries the point. The reason
for keeping them simple is that a metric you can sketch on a whiteboard in thirty seconds is
a metric you can explain and defend in a design review, and the difficulty in retrieval
evaluation is almost never the arithmetic. The difficulty is that the meaning of a metric
drifts away from its mathematics until people are reading a number that no longer describes
their system.

You will not need to study the figures to follow the book. Where a figure carries a
calculation or a decision rule, the same material is worked through in the surrounding text.

## 0.4 The per-metric template

From Chapter 4 onward, every metric is presented in the same order, so that once you have
read a few of them you always know where to look for the part you need.

![ Metric Name](assets/diagrams/fig-001-metric-name.png){.diagram-figure width=96%}

The order matters, because each section answers a question raised by the one before it. The
entry opens with a one-line summary, the formula, and a facets line that tags the metric by
dimension, unit, supervision and stage, all of which are explained in Chapters 1 and 2. Then
comes the problem the metric was invented to solve, which describes the situation someone was
stuck in and what the earlier metrics could not tell them. The idea explains how the metric
works, building up one piece at a time. The worked example runs real numbers through it by
hand. Advantages and disadvantages cover when it earns its place and how it misleads. Domain
examples show it behaving differently in three different industries, and the recommendation
tells you what to actually do.

If you are in a hurry, skip to the recommendation. If you are about to ship something, read
the disadvantages first.

## 0.5 Roadmap

The book was written and released in installments, and the tables below show how the material
was originally divided. Everything listed here is present in this edition.

**Volume I - Classical IR**

| Installment | Chapters | Contents | Status |
|---|---|---|---|
| **1** | 0-4 | Dimensions, facets, signals and metrics, set-based metrics | **this file** |
| 2 | 5-7 | Rank-based metrics; incomplete judgments; rank comparison and drift | planned |
| 3 | 8-10 | Diversity and novelty; fairness and exposure; online and counterfactual | planned |
| 4 | 11-12 | Significance and reporting; efficiency and cost | planned |

**Volume II - RAG-Era**

| Installment | Chapters | Contents |
|---|---|---|
| 5 | 13-15 | Grounding, attribution, citation quality |
| 6 | 16-18 | Alignment: utility, interference, the contribution family |
| 7 | 19-21 | Integrity, drift, staleness, robustness |
| 8 | 22-24 | Meta-evaluation, judge reliability, and deployment playbooks |

---
