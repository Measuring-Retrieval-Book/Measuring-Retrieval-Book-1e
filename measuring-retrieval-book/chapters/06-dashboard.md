# 6. The Starter Dashboard

Start with eight measurements and two context lines.

![Core dashboard](assets/diagrams/core-dashboard.png)

| Number | Metric | Dimension | Reason |
|---:|---|---|---|
| 1 | Claim Recall | Correctness | Sets the ceiling for grounded answer quality |
| 2 | Self-Knowledge | Correctness | Measures correct answers supplied without retrieved support |
| 3 | Hallucination | Correctness | Tracks unsupported generated content |
| 4 | nDCG@injected-k | Correctness | Keeps continuity with retrieval evaluation |
| 5 | One contribution metric | Alignment | Measures whether context helps the answer |
| 6 | RBO against frozen baseline | Integrity | Detects rank drift cheaply |
| 7 | Pairwise Redundancy | Efficiency | Finds repeated context and wasted tokens |
| 8 | TTFT p50 / p95 | Efficiency | Measures the latency users feel first |

Context lines:

| Line | Reason |
|---|---|
| Average claim count per answer | Prevents brevity from looking like quality |
| retrieval contribution experiment | Shows whether retrieval earns its operational cost |

<div class="recipe">
Report each metric with owner, unit, denominator, evaluation set, judge version, and date.
</div>


## Dashboard rows

Each row should include:

| Field | Purpose |
|---|---|
| Metric | Names the instrument |
| Dimension | Names the question |
| Owner | Names the team that can act |
| Unit | Prevents denominator confusion |
| Set | Names the evaluation slice |
| Version | Pins corpus, embedder, generator, and judge |
| Last run | Makes staleness visible |
| Action band | Converts movement into work |

## Action bands

Action bands make a score operational.

| Band | Meaning | Action |
|---|---|---|
| Green | Within expected range | Monitor |
| Yellow | Movement needs review | Sample failures |
| Red | Product risk | Block release or roll back |

Use bands sparingly. A band with no owner creates noise.
