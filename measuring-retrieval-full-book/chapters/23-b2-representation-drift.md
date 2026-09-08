# B.2 Representation Drift - the CKA family

**One-line:** Three complementary measures of whether two embedding models, or the same model at
two points in time, actually behave the same way.

**Facets:** Integrity/Drift | corpus & query | free | R | EMERGING VERIFIED
**Source:** Caspari, Dastidar, Zerhoudi, Mitrovic & Granitzer, *Beyond Benchmarks: Evaluating
Embedding Model Similarity for RAG Systems* · [arXiv:2407.08275](https://arxiv.org/abs/2407.08275)
OPEN Read at method-summary level via the Brehme survey's account plus the paper's abstract.

### The problem it solves

Sooner or later you will want to change your embedding model, because a newer one scores better
on a public leaderboard or because the one you are running is being deprecated. The question you
need answered before you do it is whether the new model will retrieve the same things the old one
did, and the honest answer is that most teams have no instrument for asking.

Every practitioner blog on RAG drift recommends some version of tracking the mean cosine distance
from a baseline centroid and alerting above 0.05. Those thresholds have no published validation
behind them. They are folklore with a number attached. This section supplies the actual
instruments.

### The three measures

![Three Questions, Three Instruments](assets/diagrams/fig-118-three-questions-three-instruments.png){.diagram-figure width=96%}

CKA, meaning Centered Kernel Alignment, asks whether two embedders represent text similarly by
comparing the geometry of the representations themselves. Jaccard asks whether they retrieve the
same documents, by taking the overlap of the two result sets while ignoring order.
RankSimilarity asks whether they retrieve those documents in the same order.

The table in the figure works through the combinations. High on all three means the two models are
genuinely the same. Low CKA with high Jaccard and high RankSimilarity means different underlying
mathematics producing the same behaviour, which is safe to swap. High CKA with low Jaccard means
similar geometry producing divergent results, which needs investigating. High CKA and high Jaccard
with low RankSimilarity means the same documents arriving in a new order, which matters a great
deal for RAG because position within the prompt affects how the material gets used.

That third row is the one to internalize. Two embedders can be geometrically similar and
behaviourally different, so representation similarity does not imply retrieval similarity, which
is exactly why one number is not enough.

## Correction incorporated into this edition

**Previously:** OPEN ABSTRACT-ONLY, presented in Supplement A §B.2 as a drift stack, with an
interpretation table implying that high similarity means an embedder swap is safe.

**Now:** VERIFIED Read at conclusion and results level. The paper's central finding inverts that
framing.

**Source:** Caspari, Ghosh Dastidar, Zerhoudi, Mitrović & Granitzer, CEUR-WS Vol-3784 (short
paper) · [arXiv:2407.08275](https://arxiv.org/abs/2407.08275)

## AD.2.1 What the paper actually studied

The study covered 19 embedding models across five BEIR datasets, using CKA for pairwise embedding
comparison plus Jaccard and rank similarity for retrieval behaviour at top-k. Its purpose was
model selection, meaning the identification of clusters of similar models so that choosing one
becomes easier, rather than drift monitoring.

The Supplement A framing extended that work to temporal drift, and it flagged the extension as an
extension at the time, which was right. What it did not flag, because the results had not been
read, is the finding below.

## AD.2.2 The finding that was got wrong

> Comparing embeddings with CKA generally showed intra- and inter-family clusters across datasets.
> These clusters also appeared when evaluating top-k retrieval similarity with **large k values**.
> **Scores for low k values, which would commonly be chosen in RAG systems, show high variance and
> much lower similarity, especially on larger datasets.**

More starkly, on the two larger datasets, FiQA-2018 and TREC-COVID, most models retrieve almost
completely distinct text chunks. Only one cluster, made up of bge, UAE and mxbai, retained notable
similarity, and the rest showed moderate to low similarity at best.

![Corrected CKA guidance](assets/diagrams/fig-129-what-i-implied-vs-what-the-paper-found.png){.diagram-figure width=96%}

The figure sets the two claims against each other. Supplement A implied that high Jaccard and
RankSimilarity meant a low-risk migration. The paper found that at the small k RAG actually uses,
similarity is low and unstable, with different models retrieving largely different chunks. The
curve underneath makes the shape clear: Jaccard similarity is near zero and highly variable at k
values of 3 and 10, rises through k of 50 and 100, and only approaches 1.0 out past k of 500. RAG
lives at the left-hand end of that curve, in the high-variance, low-similarity region.

So a model with high CKA is not a safe swap, because similarity at the level of the embedding
geometry does not imply similar retrieval at k=3, and that is the paper's point.

The authors add a caveat that strengthens the conclusion rather than weakening it. Their datasets
are comparatively small, while real RAG systems operate over millions of embeddings, so if larger
datasets produce lower retrieval similarity then real-world divergence may exceed what they were
able to measure.

## AD.2.3 Corrected guidance

| Supplement A said | Corrected |
|---|---|
| High Jaccard/RankSimilarity -> low-risk migration | **Expect low similarity at RAG-typical k. Low similarity is the default, not the alarm.** |
| Use the three measures as a drift stack | Calibrate against *your own* baseline, since cross-model similarity is inherently low |
| CKA as the primary instrument | **Jaccard and RankSimilarity at your production k are the operative measures.** CKA describes representation geometry, which does not transfer to retrieval behaviour at small k |

The practical upshot is stronger rather than weaker. Every embedder swap is a high-risk change by
default, so do not reason from leaderboard proximity or from CKA. Measure Jaccard and
RankSimilarity at your actual k, on your actual corpus, before migrating anything, because two
models that look interchangeable on MTEB may retrieve almost completely distinct chunks for your
queries.

This also reinforces the Supplement A recommendation that mattered most, which is to freeze a
baseline now. Its value has just gone up, because the thing you are guarding against turns out to
be larger than the original framing represented.

## AD.2.4 A second-order consequence for §B.5

If different embedders retrieve largely different chunks at small k, then any evaluation number
computed under embedder A is not comparable to the same number computed under embedder B. That
applies to drift metrics, to faithfulness, to the CUE quadrants and to every downstream measure in
this book. Embedder version therefore belongs in your experiment metadata alongside judge version.

---
