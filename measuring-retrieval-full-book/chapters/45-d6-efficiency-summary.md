# D.6 Efficiency - summary card

![Decision map](assets/diagrams/fig-155-decision-map.png){.diagram-figure width=96%}

For index time, measure the duration of a full rebuild, because that number gates every drift
policy you have, and then record index size, upload time and indexing time alongside it.

For query time, report TTFT at the median and the 95th percentile rather than mean total latency,
and measure retrieval latency separately, since retrieval is what TTFT is made of.

For tokens, track Pairwise Redundancy, which is cheap and reveals quality waste, and EHR@k, which
tells you whether to add diversity or to protect rank 1, and note that those are opposite
strategies read off the same metric. Track prompt tokens per query alongside them.

For evaluation itself, tier your suite. Running the full stack on every commit is not diligence,
it is an invoice nobody has examined.

The one insight to carry out of this part is that in RAG the efficiency knobs are the quality
knobs. Changing k, chunk size or rerank depth moves recall, faithfulness, context utilization,
noise sensitivity, latency and cost all at once, and not all in the same direction. You cannot
reason about that trade-off with one side of it unmeasured.

---
