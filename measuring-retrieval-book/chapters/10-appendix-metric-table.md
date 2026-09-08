# Appendix A. Metric Selection Table

| Product question | First metric | Companion metric | Owner |
|---|---|---|---|
| Are top results clean? | Precision@k | Recall@k | Retrieval |
| Did we find enough evidence? | Claim Recall | nDCG@injected-k | Retrieval |
| Are answers grounded? | Hallucination rate | Average claim count | Generation |
| Are citations useful? | Citation Precision | Citation Recall | Generation |
| Is the generator using retrieval? | Contribution metric | WARG | System |
| Did retrieval drift? | RBO against baseline | Jaccard@k | Retrieval |
| Did the judge drift? | Anchor-set alpha | Score delta by slice | Evaluation |
| Are we wasting context? | Pairwise Redundancy | Tokens per answer | Platform |
| Is latency acceptable? | TTFT p95 | Total latency p95 | Platform |
| Is evaluation affordable? | Judge calls per release | Human review minutes | Evaluation |

## Minimal release report

1. One paragraph describing the system change.
2. One table with the eight starter metrics.
3. One table with changed versions.
4. Ten sampled failures.
5. One decision: ship, hold, roll back, or run a targeted audit.
