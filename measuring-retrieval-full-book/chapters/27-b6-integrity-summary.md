# B.6 Integrity - the summary card

![Decision map](assets/diagrams/fig-126-decision-map.png){.diagram-figure width=96%}

Three things are worth doing this week, and together they cost about an afternoon while unlocking
everything else in this part. Freeze a baseline of 500 queries with their top-k results stored.
Pin your judge model to a dated snapshot. Freeze a 100-item anchor set carrying human labels.

Four things belong in the quarter. Compute Jaccard and RankSimilarity against your baseline
monthly. Run CKA whenever you change embedder. Build a 50-question version-sensitive set using the
VersionQA template from §B.3. And run the comparison between RAG and no-RAG, which is the test
almost nobody runs and the one that reveals whether retrieval is helping at all.

Two things should be accepted as unsolved rather than worked around. Judge drift has no metric, so
use the protocol in §B.5 instead. Recency weighting does not transfer between corpora, and the
published evidence has it moving from 1.00 to 0.00 when a tuned parameter is carried across.

The one number to fear is implicit change detection, where baselines score between 0% and 10%. If
your corpus is versioned in any sense, your system almost certainly cannot tell you that a
document changed.

---
