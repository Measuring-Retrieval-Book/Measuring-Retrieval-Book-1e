# C.9 SURE-RAG - sufficiency as a set property

**One-line:** Three-way evidence sufficiency (supports / refutes / insufficient) computed over the
retrieved *set*, not passage by passage.

**Facets:** Correctness | passage-set | ref | E2E | EMERGING VERIFIED
**Source:** Qiu, Han & Huang · [arXiv:2605.03534](https://arxiv.org/abs/2605.03534)

### The problem it solves

Every metric in this book so far scores passages one at a time, which quietly assumes that a set
of individually good passages is a good set. It is not. Two passages can each be relevant while
contradicting each other, and a set can be missing a step of reasoning that no individual passage
was responsible for supplying.

## C.9.1 The core argument

> **Relevance does not guarantee sufficiency: a topical passage may still fail to justify the
> answer.**

SURE-RAG treats evidence sufficiency as a property of the whole set, on the grounds that missing
reasoning steps and unresolved conflicts cannot be detected by scoring passages independently. A
shared claim-evidence verifier produces a local relation distribution for each claim and passage
pair, and SURE-RAG aggregates those into four answer-level feature blocks covering coverage,
relation strength, uncertainty and retrieval, which together produce a three-way decision and an
auditable selective score.

![Why Set-Level Matters](assets/diagrams/fig-146-why-set-level-matters.png){.diagram-figure width=96%}

The figure contrasts the two readings of the same retrieval. Scored passage by passage, p1, p2 and
p3 are all relevant, so the verdict is that retrieval did well. Looked at as a set, p1 and p2
contradict each other and p3 is missing the second reasoning hop, so the verdict is that the
evidence is insufficient.

All three passages scored well independently, and the problem lives between them.

This is the same structural point Volume I §4.5 raised about set-based metrics, arriving from the
opposite direction.

## C.9.2 CAUTION It is not a hallucination detector

The paper runs an explicit boundary-mapping experiment, contrasting SURE-RAG with GPT-4o on
HaluBench unsafe detection, and the ranking reverses, at 0.3343 against 0.7389 on unsafe-F1. That
indicates controlled sufficiency verification and natural hallucination detection are distinct
problems rather than two views of one problem.

Filing SURE-RAG next to hallucination metrics invites exactly the misuse the authors warn against.

## C.9.3 Reported results

| Measure | Value |
|---|---|
| Calibrated Macro-F1 | 0.9075 (raw 0.8951 ± 0.0069) |
| DeBERTa mean-pooling baseline | 0.6516 |
| GPT-4o judge baseline | 0.7284 |
| Strong concat cross-encoder | 0.8888 ± 0.0109 |
| Risk at 30% coverage | 0.2588 -> 0.1642 (**37% relative reduction**) |

Note that GPT-4o used as a judge scored 0.7284 against a purpose-built verifier's 0.9075. That is
a concrete data point on the limits of general-purpose language model judging, and it is worth
keeping in mind wherever this book recommends a judge.

## C.9.4 Recommendation

Adopt SURE-RAG's framing immediately, whatever you do about the implementation. Your retrieval
evaluation should ask whether the retrieved set justifies the answer rather than whether each
passage is on topic, and every metric in Volume I Chapter 4 along with most of §C.3 through §C.5
scores passages independently.

If your questions are multi-hop, this is not optional. It is the difference between measuring your
system and measuring a proxy for it that happens to look reasonable.

---
