# 5. RAG Metrics

RAG evaluation has three objects: evidence, answer, and judge.

![RAG layer diagram](assets/diagrams/rag-pipeline.png)

## Correctness and grounding

Claim decomposition is the clean unit for answer evaluation. Break the answer into atomic claims. Score whether each claim is supported, contradicted, or absent in the retrieved context.

RAGChecker is valuable because it separates retriever failures from generator failures. Claim Recall estimates whether required claims were found. Self-Knowledge estimates the rate of answers supplied from model memory. Hallucination estimates unsupported generated content.

RAGAS is useful for reference-free evaluation. Treat paper definitions and library implementations as separate instruments. Pin the version.

ALCE-style citation metrics ask whether citations support the sentence they cite. The leave-one-out trick tests whether a citation is doing real work.

## Alignment

Alignment asks whether retrieval helped generation. Contribution metrics estimate the utility of a document or passage by measuring what changes when it is present, absent, or perturbed.

| Family | Measures | Use |
|---|---|---|
| eRAG / DIG / SePer / Gain | Passage contribution to answer quality | Diagnose context utility |
| WARG | Gap between retrieved relevance and generated attribution | Detect wasted retrieval and low-rank dependence |
| CUE / MIRAGE quadrants | Relationship between answer quality and context use | Find lucky guesses and blind spots |
| UDCG | Utility and distraction in ranked context | Tune retrieval for generator use |

<div class="warning">
Pick one contribution metric for the dashboard. Use the others as audit tools during method work.
</div>

## Integrity

Integrity metrics watch change. Use RBO against a frozen baseline for rank drift. Use version-sensitive question sets for corpus drift. Use anchor sets and Krippendorff alpha for judge drift.

## Efficiency

Efficiency should include index-time, query-time, token-time, and evaluation-time costs.

| Cost center | Metric |
|---|---|
| Indexing | rebuild time, index size, embedding cost |
| Query serving | TTFT p50, TTFT p95, total latency |
| Context | tokens per query, pairwise redundancy, evidence hit rate |
| Evaluation | judge calls, human review minutes, audit cost |


## Metric cards

### Claim Recall

Unit: claim.

Question: did the retrieved context contain the information needed for the answer?

Use it as the ceiling metric. A generator cannot ground a claim in evidence that never arrived. Low Claim Recall sends work to retrieval, query rewriting, corpus coverage, or chunking.

### Self-Knowledge

Unit: answer or claim.

Question: how often did the model answer correctly from parametric memory while retrieved evidence missed the answer?

Use it to separate product success from retrieval success. This metric matters in domains where model memory is strong enough to hide retrieval failure.

### Hallucination

Unit: claim.

Question: which generated claims lack support?

Use it as a release gate for high-risk surfaces. Pair it with average claim count, because short answers generate fewer opportunities for unsupported claims.

### Citation Precision

Unit: citation.

Question: does the cited source support the sentence that cites it?

Use it when users see citations. A citation should carry evidence. Sentence-level checking gives the cleanest product signal.

### Contribution metrics

Unit: passage or document.

Question: how much did this retrieved item improve the generated answer?

Use one member of the family for the dashboard. Use perturbation studies and ablations during method development.

### WARG

Unit: query.

Question: does generated attribution follow retrieved relevance?

Use it before investing heavily in retriever ranking improvements. A low alignment score means the generator may be drawing value from low-ranked passages or ignoring top-ranked passages.

### Judge agreement

Unit: labeled item.

Question: does the automated judge agree with the human anchor set?

Use Krippendorff alpha for multi-label or missing-label settings. Report the anchor set date and judge snapshot.
