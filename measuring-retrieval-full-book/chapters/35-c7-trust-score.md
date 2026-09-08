# C.7 Trust-Score

**One-line:** A holistic measure of whether an LLM is *appropriate for the RAG task*, including
whether it correctly refuses.

**Facets:** Correctness | claim | ref | G | ESTABLISHED VERIFIED
**Source:** Song, Sim, Bhardwaj, Chieu, Majumder & Poria, **ICLR 2025 Oral** ·
[arXiv:2409.11242](https://arxiv.org/abs/2409.11242)

### The problem it solves

Every metric so far scores what the model said. None of them asks whether it should have said
anything at all. When the retrieved context does not contain the answer, the right behaviour is
to decline, and a metric that only grades answers will treat a confident guess and an honest
refusal as though the refusal were the worse outcome.

## C.7.1 What it adds

Trust-Score measures whether a given model is suitable for the RAG task, and the paired method
Trust-Align improves models against it.

The finding that matters for metric selection is that prompting methods such as in-context
learning fail to adapt models to the RAG task effectively when measured this way. Aligned models
substantially outperform the baselines across ASQA, QAMPARI and ELI5, and critically, Trust-Align
improves a model's ability to correctly refuse as well as its ability to produce quality citations.

## C.7.2 Why this closes a gap nothing else does

![The Metric That Rewards Saying "I Don'T Know"](assets/diagrams/fig-142-the-metric-that-rewards-saying-i-don-t-know.png){.diagram-figure width=96%}

The figure states the asymmetry. When the context is insufficient, a model that answers anyway is
penalized and a model that refuses is rewarded, which reverses the incentive every other metric
here creates.

The objection is predictable, which is that refusal rate is a product metric rather than a quality
metric. In RAG it is both, because an answer with no evidence behind it is a defect that happens
to be well formed.

There is a complication, and it comes from Supplement A's reading of *Sufficient Context*
([arXiv:2411.06037](https://arxiv.org/abs/2411.06037)). Models abstain less once RAG is added, and
they hallucinate more often than they abstain. Retrieval actively suppresses the behaviour
Trust-Score rewards, which makes the metric more necessary rather than less.

## C.7.3 Advantages and disadvantages

| Advantages | Disadvantages |
|---|---|
| Scores refusal as a first-class outcome | Reference-based |
| ICLR Oral; strong empirical validation across 27 models | Single operating point, not a coverage-risk curve |
| Paired alignment method, so it is actionable | Tied to the ALCE-style datasets it was validated on |
| Isolates *model suitability* from retriever quality | Composite score - decompose before acting |

## C.7.4 Recommendation

Use Trust-Score at model-selection time, alongside the model-intrinsic half of MIRAGE from
Supplement A §A.3.2. Both answer whether a given model is right for RAG, from different angles,
with MIRAGE working through context-utilization failures and Trust-Score through grounded
attribution and refusal.

For production, what you actually want is a coverage-risk curve, which means plotting accuracy
among the questions the system answered against the fraction it chose to answer, as you sweep the
threshold at which it abstains. Trust-Score gives you a single point on that curve. The curve is
more useful and nobody publishes it, so you will have to build it yourself.

---

## C.7.5 The components


Trust-Score is a composite built over three dimensions, being response truthfulness, factual
accuracy and attribution groundedness.

![Trust-Score Structure](assets/diagrams/fig-173-trust-score-structure.png){.diagram-figure width=96%}

Under response truthfulness sit two components. F1_GR is Grounded Refusal, computed as the macro
average of two separate F1 scores: F1_ref for correctly refusing unanswerable questions and F1_ans
for correctly answering answerable ones. Writing A_g for the questions that are genuinely
answerable and A_r for the questions the model chose to answer, the refusal precision is the
proportion of the model's refusals that were on genuinely unanswerable questions, and the refusal
recall is the proportion of genuinely unanswerable questions that the model refused. The second
component, F1_AC, is answer-calibrated answer correctness.

Under attribution groundedness sit citation recall and citation precision, adopted directly from
ALCE.

The design property that matters is that by penalizing both incorrect refusals and incorrect
non-refusals, F1_GR gives a balanced view of the model's over-responsiveness and its
under-responsiveness at the same time, which is the abstention-quality measurement that almost
nothing else provides.

The lineage is worth noting too. Trust-Score's attribution half is ALCE's citation precision and
recall, so §C.5 and §C.7 describe two halves of a single measurement tradition rather than two
competing ones.

For calibration, the benchmark composition is ASQA with 610 answerable and 338 unanswerable
questions, QAMPARI with 295 and 705, and ELI5 with 207 and 793. Note how heavily QAMPARI and ELI5
lean toward unanswerable, which is why refusal handling dominates the score on those two.
