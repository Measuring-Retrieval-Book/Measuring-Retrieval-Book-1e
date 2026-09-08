# 4. Classical IR Metrics

Classical IR gives the measurement grammar for retrieval. RAG changes the downstream system. The same grammar still matters.

## Set metrics

Precision measures the share of retrieved items that are relevant. Recall measures the share of relevant items that were retrieved. F1 combines the two when a single operating point is useful.

| Metric | Use | Watch |
|---|---|---|
| Precision | Topical cleanliness | Can reward timid retrieval |
| Recall | Coverage | Needs a known relevant set |
| F beta | Product-weighted tradeoff | Hides the separate movement of precision and recall |
| Precision@k | Top-k quality | Ignores relevant items below k |

## Rank metrics

Rank metrics add position. They model attention. High ranks matter more because users and generators consume early items first.

| Metric | User model | Best fit |
|---|---|---|
| MRR | First useful hit ends the search | Known-item lookup |
| MAP | Every relevant item matters | Recall-rich search |
| nDCG | Graded relevance with rank discount | General ranked retrieval |
| ERR | User may stop after satisfaction | Navigational search |
| RBP | Persistence at each rank | Stable, interpretable dashboards |

<div class="decision">
For RAG, compute rank metrics at the injected depth. The generator can use only the context it receives.
</div>

## Incomplete judgments

Judgment pools are incomplete in real systems. bpref and infAP reduce sensitivity to missing labels. They are useful when old test collections meet new retrievers.

## Comparing rankings

Kendall tau and Spearman rho compare full ranked lists. RBO compares top-heavy overlap and works with unequal lists. RBO is the practical drift metric for monthly retrieval monitoring.


## Metric cards

### Precision

Formula: retrieved relevant items divided by retrieved items.

Use it when the product experience is damaged by junk results. Legal search, clinical lookup, and support automation often need high precision near the top of the list.

Read precision with recall. High precision can come from a cautious retriever that returns too little.

### Recall

Formula: retrieved relevant items divided by all relevant items.

Use it when missing evidence is the primary harm. Compliance review, patent search, literature review, and retrieval for synthesis belong here.

Recall needs a denominator. In live systems that denominator is usually approximated by pooled judgments, curated cases, or task-specific audits.

### F beta

Formula: weighted harmonic mean of precision and recall.

Use beta greater than 1 when misses are costly. Use beta less than 1 when junk results are costly. Report the chosen beta beside the score.

### MRR

Formula: average reciprocal rank of the first relevant result.

Use it for known-item tasks: password reset article, account policy page, exact entity lookup. The first useful hit ends the search.

### MAP

Formula: average of precision values at relevant ranks, then averaged across queries.

Use it when many relevant items matter. MAP rewards systems that retrieve relevant items early and consistently.

### nDCG

Formula: discounted cumulative gain divided by ideal discounted cumulative gain.

Use it when judgments are graded. nDCG handles "excellent", "acceptable", and "weak" relevance in one score.

For RAG, choose k as injected context depth. If the retriever returns 50 passages and the generator receives 8, nDCG@8 describes the usable ranked evidence.

### RBP

Formula: rank-biased precision with persistence parameter p.

Use it when you want a stable top-heavy score. The parameter p expresses how likely the user or downstream consumer is to continue to the next rank.

### RBO

Formula: rank-biased overlap between two ranked lists.

Use it for drift. Compare today's ranking with a frozen baseline at the same k. Keep the query set and corpus timestamp visible.
