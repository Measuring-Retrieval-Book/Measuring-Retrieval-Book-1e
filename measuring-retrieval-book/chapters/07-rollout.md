# 7. A 90-Day Rollout

## Week 1

Freeze the baseline. Save 500 queries, top-k results, embedder version, retriever version, corpus timestamp, injected k, and judge version.

Create a 100-item human-labeled anchor set. Time a full index rebuild. Record the number.

## Weeks 2 to 4

Run the retrieval contribution experiment. Measure semantic test coverage. Compute pairwise redundancy. Compare MAP and bpref to estimate judgment distortion. Run a position-bias test on the judge.

## Month 2

Run a k sweep over k = 1, 3, 5, 10, 20, 50. Plot recall, answer quality, redundancy, tokens, and TTFT. Set k at the knee of the curve.

## Month 3

Run the full diagnostic layer offline. Promote three RAGChecker metrics. Sample CUE quadrants. Run WARG once to test whether the generator follows the retrieved ranking. Build a 50-question version-sensitive set.

## Ongoing

Run RBO monthly. Run expensive diagnostics per release. Run the judge anchor set for every judge change. Run Jaccard and RankSimilarity for every embedder change.
