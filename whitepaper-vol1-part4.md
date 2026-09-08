# Measuring Retrieval

## Volume I — Foundations and Classical Information Retrieval
### Installment 4 of 4: Chapters 11–12 + Volume I Conclusion
#### Significance & Reporting · Efficiency, Cost, and Time

---

**Citation status.** All citations verified before writing. The two ⬜ entries deferred from
Installment 3 — sDCG and time-biased gain — are now ✅ and treated properly in Chapter 12.
**Volume I closes with zero unverified citations.**

**What this installment is for.** Chapters 4–10 gave you metrics. Chapter 11 asks whether the
*differences* you observe in them are real. Chapter 12 asks what those metrics cost to achieve.

Then the Volume closes with the finding that should govern how you read everything before it.

---

# Chapter 11 — Significance, Reporting, and the Progress Problem

## 11.0 The uncomfortable opening

Let us begin with the conclusion, because it reframes the chapter.

**Source:** Armstrong, Moffat, Webber & Zobel, *Improvements That Don't Add Up: Ad-hoc Retrieval
Results Since 1998*, **CIKM 2009, pp. 601–610** ✅

The authors examined a decade of published ad-hoc retrieval results and found that the reported
improvements **did not accumulate**. Papers routinely demonstrated statistically significant gains
over a baseline, and yet the field's absolute effectiveness had not advanced correspondingly.

```
   THE PROBLEM IN ONE PICTURE
   ══════════════════════════

   WHAT THE PAPERS SAID          WHAT ACTUALLY HAPPENED
   ────────────────────          ──────────────────────

   effectiveness                 effectiveness
        │        ╱                    │
        │      ╱                      │  ~~~~~~~~~~~~~
        │    ╱                        │
        │  ╱                          │
        └──────────── time            └──────────── time
        1998      2008                1998      2008

   Each paper: "+4% over baseline, p < 0.05"
   Ten years of those: no cumulative gain.

        o    "How is that possible? They were
       /|\     all significant."
       / \

        o    "Weak baselines. Selective reporting.
       /|\     Multiple comparisons. Different
       / \     collections. All of it defensible
              per-paper and none of it additive."
```

**Why this belongs in a white paper about metrics rather than a methods appendix:** it is the
strongest available evidence that *having good metrics is not sufficient*. The field in question had
nDCG, MAP, and significance testing. It still could not tell whether it was improving.

If you take one thing from Chapter 11: **the failure mode is not bad metrics. It is good metrics
compared badly.**

---

## 11.1 Significance testing — which test?

**Source:** Smucker, Allan & Carterette, *A Comparison of Statistical Significance Tests for
Information Retrieval Evaluation*, **CIKM 2007, pp. 623–632** ✅

### The idea

IR effectiveness scores are not normally distributed, queries vary enormously in difficulty, and
sample sizes are small. Those three facts make the choice of significance test consequential rather
than ceremonial.

### The options

```
   THE TEST MENU
   ═════════════

   ┌────────────────────┬──────────────────────────────────┐
   │ TEST               │ CHARACTER                        │
   ├────────────────────┼──────────────────────────────────┤
   │ Paired t-test      │ assumes normality; surprisingly  │
   │                    │ robust in practice               │
   ├────────────────────┼──────────────────────────────────┤
   │ Randomization      │ makes no distributional          │
   │ (permutation) test │ assumption; recommended default  │
   ├────────────────────┼──────────────────────────────────┤
   │ Bootstrap          │ resampling; gives intervals      │
   ├────────────────────┼──────────────────────────────────┤
   │ Wilcoxon signed-   │ rank-based; discards magnitude   │
   │ rank               │                                  │
   ├────────────────────┼──────────────────────────────────┤
   │ Sign test          │ weakest; only direction          │
   └────────────────────┴──────────────────────────────────┘

        o    "Which one?"
       /|\
       / \

        o    "Paired randomization. It assumes least,
       /|\     it's cheap on modern hardware, and it
       / \     directly tests the thing you care about:
              could this difference have arisen by
              chance assignment?"
```

### The paired randomization test, mechanically

```
   HOW IT WORKS
   ════════════

   For each query, you have two scores: A_q and B_q.
   Observed difference: D = mean(A) − mean(B)

   Now: for each query, randomly SWAP A_q and B_q
        (or don't), with probability ½.
        Recompute the mean difference.
        Repeat 10,000 times.

   ┌──────────────────────────────────────────┐
   │  distribution of shuffled differences    │
   │                                          │
   │           ▁▃▅███▅▃▁                      │
   │      ─────────────────────────── 0       │
   │                        ▲                 │
   │                        └── your observed  │
   │                            D             │
   │                                          │
   │  p = fraction of shuffles ≥ |D|          │
   └──────────────────────────────────────────┘

   If your observed difference is unremarkable among
   random reshuffles, it is not evidence of anything.
```

### Recommendation

**Use a paired randomization test as your default.** Report the p-value, the effect size, and a
confidence interval. Never report a p-value alone — "significant" without a magnitude tells the
reader nothing about whether the difference matters.

---

## 11.2 Statistical power and topic set size

Two verified works make the same point from different angles:

| Work | Citation | Finding |
|---|---|---|
| Voorhees & Buckley | *The Effect of Topic Set Size on Retrieval Experiment Error*, **SIGIR 2002, pp. 316–323** ✅ | Error rates depend strongly on the number of topics |
| Webber, Moffat & Zobel | *Statistical Power in Retrieval Experimentation*, **CIKM 2008, pp. 571–580** ✅ | Most IR experiments are underpowered |
| Sanderson & Zobel | *Information Retrieval System Evaluation: Effort, Sensitivity, and Reliability*, **SIGIR 2005, pp. 162–169** ✅ | Trades off judgment effort against reliability |

```
   THE POWER PROBLEM
   ═════════════════

   50 queries.  nDCG 0.712 vs 0.698.  p = 0.04.

        o    "Significant improvement!"
       /|\
       / \

        o    "With 50 queries and that effect size,
       /|\     what's your power to detect a real
       / \     difference? If it's 0.35, then most
              real improvements would come back
              non-significant — and some
              non-improvements come back significant."

   ┌───────────────────────────────────────────┐
   │  UNDERPOWERED STUDIES DON'T JUST MISS     │
   │  REAL EFFECTS. They also inflate the      │
   │  ones they DO detect, because only large  │
   │  observed differences clear the bar —     │
   │  including the ones that are large by     │
   │  chance.                                  │
   └───────────────────────────────────────────┘
```

### Recommendation

**Compute the number of queries you need before running the experiment**, not after. If you cannot
get enough, say so and report confidence intervals wide enough to be honest.

For RAG specifically: evaluation sets of 50–100 questions are common and are almost always
underpowered for the effect sizes people claim. If you are comparing two rerankers that differ by
two points of accuracy, 100 questions will not settle it.

---

## 11.3 Multiple comparisons and the weak-baseline problem

These are the two mechanisms Armstrong et al.'s finding rests on.

### 11.3.1 Multiple comparisons

```
   THE TWENTY-CONFIGURATION PROBLEM
   ════════════════════════════════

   You try 20 chunk sizes.
   You test each against baseline at α = 0.05.

   Expected false positives if NOTHING works: 1

        o    "Chunk size 384 was significantly better!"
       /|\
       / \

        o    "You ran twenty tests. One coming back
       /|\     significant is the EXPECTED outcome
       / \     under the null. Correct for it, or
              hold out a confirmation set."
```

Correct with Bonferroni (conservative), Holm, or Benjamini–Hochberg (false-discovery-rate). Or
better: **choose your configuration on a development set and confirm once on a held-out set.**

### 11.3.2 Weak baselines

This is the subtler and more damaging mechanism. A well-tuned BM25 is a strong baseline; an untuned
one is not. Papers comparing against untuned baselines report gains that vanish against properly
configured ones — and each such paper is individually defensible while the aggregate is misleading.

```
   WHY IMPROVEMENTS DON'T ADD UP
   ═════════════════════════════

   Paper 1: our method beats weak-BM25 by 8%
   Paper 2: our method beats weak-BM25 by 6%
   Paper 3: our method beats weak-BM25 by 7%

   Combined expectation: ~21% over BM25
   Reality: all three are roughly level with
            a properly tuned BM25.

        o    "So the baseline was the problem."
       /|\
       / \

        o    "The baseline is ALWAYS the problem.
       /|\     Armstrong et al. found a decade of it."
```

**The RAG-era relevance is direct and current.** Dense retrieval papers routinely compare against
BM25 configurations with default `k₁` and `b`. And note the finding from *The Power of Noise*
(Cuconasu et al., SIGIR'24) — BM25 outperformed dense retrieval methods in terms of perplexity for
the fundamental text-completion task, and a broad set of sparse methods beat all the dense methods
tested for varying query lengths. Sparse baselines are stronger than the field's habits assume.

### 11.3.3 Score standardization

For cross-collection comparison: Webber, Moffat & Zobel, *Score Standardization for
Inter-Collection Comparison of Retrieval Systems*, **SIGIR 2008, pp. 51–58** ✅. If you need to
compare results across collections — and RAG practitioners often do, across domains — raw metric
values are not comparable and standardization is the published remedy.

---

## 11.4 The reporting checklist

Everything in Volume I, condensed into what must appear beside a number for it to mean anything.

```
┌─────────────────────────────────────────────────────────────┐
│  BEFORE YOU REPORT A RETRIEVAL METRIC                       │
│                                                             │
│  THE METRIC                                                 │
│  □ Metric name AND cutoff k                                 │
│  □ Gain function, if nDCG (linear or exponential)           │
│  □ Persistence p, if RBP or RBO                             │
│  □ Novelty α, if α-nDCG                                     │
│  □ Judgment source and coverage                             │
│                                                             │
│  THE COMPARISON                                             │
│  □ Number of queries                                        │
│  □ Significance test used (paired randomization preferred)  │
│  □ Effect size and confidence interval, not just p          │
│  □ Multiple-comparison correction, if >1 test               │
│  □ Baseline configuration — was it TUNED?                   │
│                                                             │
│  THE HONESTY LINE                                           │
│  □ RBP residual, or MAP−bpref gap, or some statement of     │
│    how much judgment incompleteness could move the number   │
│                                                             │
│  FOR RAG, ADDITIONALLY                                      │
│  □ Embedder name AND version                                │
│  □ Generator name AND version                               │
│  □ Judge model AND dated snapshot, if LLM-judged            │
│  □ Chunk size and overlap                                   │
│  □ k actually injected into the prompt (not k retrieved)    │
└─────────────────────────────────────────────────────────────┘
```

That last item recurs because it is the most common silent error in RAG evaluation: reporting
metrics at retrieval depth while the generator consumes a shallower slice.

---

# Chapter 12 — Efficiency, Cost, and Time

## 12.0 Reclaiming a dimension

Volume I Chapter 1 promoted Efficiency/Cost from `NA` to a full dimension. This chapter is the
classical half of that; Supplement B Part D is the RAG half.

The classical measures are unglamorous and well-understood:

| Metric | Source | Note |
|---|---|---|
| Query response time / latency | Manning Ch. 8 ✅ | The user-facing number |
| Query throughput | Manning Ch. 4 ✅ | Capacity |
| Indexing throughput | Manning Ch. 4 ✅ | Gates your refresh policy |
| Index size | Manning Ch. 5 ✅ | Storage and memory pressure |
| Query-processing cost | Manning Ch. 7 ✅ | Per-query compute |
| Crawl throughput | Manning Ch. 20 ✅ | Ingestion capacity |

Chapter 12's contribution is not to re-list these. It is to establish that **time is not merely a
cost — it is part of the quality measurement itself.**

---

## 12.1 Time-Biased Gain

**One-line:** Gain accumulated as a function of *time spent*, discounted by the probability the user
is still reading.

**Formula (structure):**
```
   TBG = ∫  G(t) · D(t)  dt

     G(t) = gain accumulated by time t
     D(t) = decay function: probability the user
            CONTINUES until time t,  with D(0) = 1
```

**Facets:** Efficiency/Cost + Correctness | session | ref | E2E | ⬤ ✅
**Source:** Smucker & Clarke, *Time-Based Calibration of Effectiveness Measures*, **SIGIR 2012,
pp. 95–104**, doi 10.1145/2348283.2348300 — **SIGIR 2012 Best Paper**

### The idea

Every metric in Chapters 5–8 discounts by **rank**. Time-biased gain discounts by **elapsed time**.

That substitution has a consequence most metrics cannot express: two results at the same rank are
not equally costly if one takes longer to evaluate. A long document, a poor summary, a slow-loading
page — all consume the user's budget without appearing anywhere in nDCG.

The authors' stated motivation makes this concrete: summaries are designed to, and do, speed the
rate at which users find relevant documents — so metrics should reflect the value of summaries by
using a user model that incorporates the time required. **Rank-based metrics are blind to snippet
quality by construction.**

### Diagram

```
   RANK DISCOUNT vs TIME DISCOUNT
   ══════════════════════════════

   TWO RESULT LISTS, IDENTICAL nDCG:

   LIST A                        LIST B
   ┌───────────────────────┐     ┌───────────────────────┐
   │ 1. rel — good snippet │     │ 1. rel — bad snippet, │
   │    (3 sec to judge)   │     │    40-page PDF        │
   │                       │     │    (90 sec to judge)  │
   │ 2. rel — good snippet │     │ 2. rel — bad snippet  │
   │    (3 sec)            │     │    (90 sec)           │
   └───────────────────────┘     └───────────────────────┘

   nDCG:  identical
   TBG:   List A vastly better

        o    "But the same documents were retrieved."
       /|\
       / \

        o    "The user gave up during item 1 of List B.
       /|\     Retrieval was identical; the EXPERIENCE
       / \     wasn't. Time-biased gain is the only
              measure here that notices."

   ┌─────────────────────────────────────────────────┐
   │  D(t): probability the user is still reading    │
   │                                                 │
   │  1.0 ┤●                                         │
   │      │ ●●                                       │
   │  0.5 ┤    ●●●                                   │
   │      │        ●●●●                              │
   │  0.0 ┤             ●●●●●●●●●                    │
   │      └────────────────────────── t (seconds)    │
   │        0    30   60   90   120                  │
   │                                                 │
   │  Gain arriving after the user leaves is worth   │
   │  nothing. Rank cannot represent this.           │
   └─────────────────────────────────────────────────┘
```

### Advantages

- **Unifies quality and cost in one number** — the only metric in this volume that does.
- **Captures snippet and document-length effects** that every rank-based metric ignores.
- **Grounded in observed behaviour**, with calibration from user studies rather than assumed
  discounts.
- **Best-paper recognition** and a substantial follow-on literature: *Stochastic Simulation of
  Time-Biased Gain* (CIKM 2012, pp. 2040–2044) ✅ and *Modeling User Variance in Time-Biased Gain*
  (HCIR 2012) ✅.

### Disadvantages

- **Requires time estimates** per document — document length, snippet quality, load time. That is
  instrumentation most teams lack.
- **The decay function must be calibrated**, ideally from your own users. A borrowed `D(t)` is a
  borrowed user model.
- **Harder to compute and to explain** than nDCG.
- **Rarely reported**, so no external comparability.

### Domain examples

**Enterprise document search.** Excellent fit and badly underused. Corpora with wildly varying
document lengths — a two-page memo versus a 400-page manual — are exactly where rank-based metrics
mislead.

**Mobile search.** Time costs are large and variable. TBG's framing is the right one.

**RAG.** ⚠️ Interesting inversion. The *user's* reading time is now spent on one generated answer,
so TBG does not transfer directly. But the **model's** budget is the analogue: tokens consumed, and
whether gain arrives inside the context window or past the point of effective attention. *Lost in
the Middle* is, in this framing, a `D(t)` for LLMs — a decay function over context position rather
than over seconds. Nobody has formalized TBG for RAG, and it is a genuine open opportunity.

### Recommendation

If your corpus has highly variable document lengths or your snippets vary in quality, **TBG will
tell you something nDCG structurally cannot.** Start by simply logging time-to-judgment in your
annotation tool — you will get the input data as a by-product and can decide later whether to
compute the full measure.

---

## 12.2 Session metrics

### 12.2.1 sDCG

**One-line:** DCG extended across the multiple queries of a single search session, with later
queries discounted.

**Facets:** Correctness | session | ref | R | ⬤ ✅
**Source:** Järvelin, Price, Delcambre & Nielsen, *Discounted Cumulated Gain Based Evaluation of
Multiple-Query IR Sessions*, **ECIR 2008, LNCS 4956, pp. 4–15**, doi 10.1007/978-3-540-78646-7_4

### The idea

The paper's premise is a direct criticism of everything in Chapters 4–8: the common assumption of a
**single query per topic and session poorly represents real life.**

sDCG applies a second discount across *queries* in addition to DCG's discount across *ranks*.
Relevant results arriving in a later reformulation are worth less, because the user paid
reformulation effort to reach them.

```
   TWO NESTED DISCOUNTS
   ════════════════════

   SESSION
   ├── query 1  (full weight)
   │     ├── rank 1  1/log₂(2)
   │     ├── rank 2  1/log₂(3)
   │     └── rank 3  1/log₂(4)
   ├── query 2  (discounted — user had to reformulate)
   │     ├── rank 1  ...
   │     └── ...
   └── query 3  (discounted further)
         └── ...

        o    "Why penalize later queries? The user
       /|\     found what they wanted."
       / \

        o    "They found it after three attempts.
       /|\     A system that answered on attempt one
       / \     is better, and single-query metrics
              score them identically."
```

### Advantages / Disadvantages

| Advantages | Disadvantages |
|---|---|
| Models real multi-query behaviour | Requires session-level judgments and logs |
| Rewards answering early in the session | Two discount parameters to set and report |
| Captures reformulation cost, which no single-query metric can | Rarely implemented; little tooling |
| Graded relevance throughout | Session boundaries are ambiguous in practice |

### 12.2.2 SRBP — the session analogue of RBP

**Source:** Lipani, Carterette & Yilmaz, *From a User Model for Query Sessions to Session Rank
Biased Precision (SRBP)*, **ICTIR 2019** ✅

Noted because it completes a pattern this white paper has traced three times now:

```
   THE RBP FAMILY
   ══════════════

   RBP   (§5.5)   quality, single ranking     Moffat & Zobel 2008
   RBO   (§7.2)   comparison of rankings      Webber et al. 2010
   NRBP  (§8.3.1) quality + novelty           Clarke et al. 2009
   SRBP  (§12.2)  quality across a session    Lipani et al. 2019

   One user model — geometric persistence with an
   explicit residual — extended four ways.

        o    "So if I learn RBP..."
       /|\
       / \

        o    "...you get the other three nearly free.
       /|\     Best return on conceptual investment
       / \     in classical IR."
```

### Recommendation

Use sDCG or SRBP if your users reformulate — which, for enterprise search and conversational RAG,
they overwhelmingly do. For conversational RAG in particular, **your unit of analysis is the session,
not the query**, and every metric in Chapters 4–8 is measuring the wrong unit.

This is a real and largely unaddressed gap: multi-turn RAG evaluation mostly reports per-turn
metrics, which cannot see whether turn 3 was needed because turns 1 and 2 failed.

---

## 12.3 The cost–quality frontier

The practical synthesis of this chapter.

```
   YOU ARE ALWAYS ON A FRONTIER
   ════════════════════════════

   quality
      │           ╭──────────── ← diminishing returns
      │        ╭──╯
      │      ╭─╯
      │    ╭─╯
      │  ╭─╯
      │╭─╯
      └──────────────────────── cost
        k=1  3   5   10  20  50

   RAGChecker's measured saturation:
     "moderately increasing the number and size of
      chunks improves recall and thus F1 with minimal
      effort... the effect SATURATES as the total
      amount of relevant information is fixed"

        o    "So where do we sit on this curve?"
       /|\
       / \

        o    "Nobody knows, because almost nobody
       /|\     plots it. They pick k from a tutorial
       / \     and never revisit it."
```

### The experiment worth running

```
   ┌──────────────────────────────────────────────────┐
   │  THE k-SWEEP                                     │
   │                                                  │
   │  For k ∈ {1, 3, 5, 10, 20, 50}, record:          │
   │                                                  │
   │    ▸ Recall@k                                    │
   │    ▸ your primary quality metric                 │
   │    ▸ Pairwise Redundancy                         │
   │    ▸ prompt tokens per query                     │
   │    ▸ TTFT p50 / p95                              │
   │                                                  │
   │  Plot quality against tokens. Find the knee.     │
   │                                                  │
   │  Cost: one afternoon. Almost nobody does it.     │
   │  It is the single highest-value experiment in    │
   │  this volume.                                    │
   └──────────────────────────────────────────────────┘
```

Two published data points to anchor your expectations: RAGChecker observed faithfulness rising
88.1 → 92.2 as k went 5 → 20, so more context made the generator *more* faithful. But RAG-X
measured 22.0% pairwise redundancy at its best configuration. **More context helped, and a fifth of
it was duplicate.** Both are true, and only a sweep tells you which effect dominates for you.

---

# Volume I — Conclusion

## The five things that survive

Across nine chapters and roughly seventy metrics, five claims have earned their place.

### 1. A metric is a user model

```
   MRR    ── user stops at the first hit
   nDCG   ── attention declines logarithmically
   ERR    ── user satisfices probabilistically
   RBP    ── user continues with probability p
   TBG    ── user has a time budget
   sDCG   ── user reformulates
   UDCG   ── the "user" is a language model
```

Choosing a metric is choosing a theory of your reader. When the reader changed — from human to
LLM — every classical discount became the wrong shape, which is the entire argument of Supplement A.

### 2. Report the uncertainty or the number is decoration

RBP's residual and the MAP−bpref gap both exist to quantify how much your judgment incompleteness
could be moving your conclusions. Neither is expensive. Both are nearly always omitted.

### 3. Evaluation measures become objective functions

Clarke et al.'s argument, and the most consequential sentence in Volume I: measures act as
objective functions to be optimized. **A system will be optimized against whatever you measure,
including the things you forgot to measure.** Redundancy went unmeasured, so systems produced it —
22% of it, in a production-grade medical RAG pipeline, in 2026.

### 4. Absolute click metrics do not work; paired comparisons do

Eight absolute usage metrics tested in 2008; none reliably reflected retrieval quality. Interleaved
paired comparisons did. Most production dashboards are still built on the first group.

### 5. Good metrics, badly compared, produce a decade of illusory progress

Armstrong et al. is the closing argument. The field had nDCG, MAP, and significance tests, and still
could not tell whether it was improving — because of weak baselines, multiple comparisons, and
non-cumulative reporting.

```
        o    "So what do I actually do?"
       /|\
       / \

        o    "Pick metrics that match your reader.
       /|\     Report their uncertainty. Tune your
       / \     baseline as hard as your system.
              Compare in pairs. Correct for the
              number of things you tried.

              And plot the k-sweep. Seriously."
```

## What Volume I could not do

Three gaps this volume names honestly and does not close:

| Gap | Where it is addressed |
|---|---|
| Every classical discount assumes a human reader | Supplement A §A.4 (UDCG) |
| Nothing here measures whether the generator *used* the retrieval | Supplement A (Alignment) |
| Nothing here measures grounding, claims, or citations | Supplement B (Correctness) |

Volume I is the foundation. It is not sufficient for RAG, and it was never going to be — but the
practitioners who skip it end up reinventing bpref badly, and calling redundancy a new discovery.

---

# Appendix 4A — Citation verification ledger

**Chapter 11**

| Work | Citation | Status |
|---|---|---|
| The progress problem | Armstrong, Moffat, Webber & Zobel, *Improvements That Don't Add Up*, CIKM 2009, pp. 601–610 | ✅ |
| Significance tests | Smucker, Allan & Carterette, CIKM 2007, pp. 623–632 | ✅ |
| Statistical power | Webber, Moffat & Zobel, CIKM 2008, pp. 571–580 | ✅ |
| Topic set size | Voorhees & Buckley, SIGIR 2002, pp. 316–323 | ✅ |
| Effort/sensitivity/reliability | Sanderson & Zobel, SIGIR 2005, pp. 162–169 | ✅ |
| Score standardization | Webber, Moffat & Zobel, SIGIR 2008, pp. 51–58 | ✅ |
| Statistical inference in IR | Savoy, *Information Processing and Management* 33(4):495–512, 1997 | ✅ |
| Biased judgments | Büttcher, Clarke, Yeung & Soboroff, SIGIR 2007, pp. 63–70 | ✅ |

**Chapter 12**

| Work | Citation | Status |
|---|---|---|
| **Time-biased gain** | Smucker & Clarke, *Time-Based Calibration of Effectiveness Measures*, SIGIR 2012, pp. 95–104, doi 10.1145/2348283.2348300 — **Best Paper** | ✅ *(was ⬜)* |
| TBG simulation | Smucker & Clarke, *Stochastic Simulation of Time-Biased Gain*, CIKM 2012, pp. 2040–2044 | ✅ |
| TBG user variance | Smucker & Clarke, *Modeling User Variance in Time-Biased Gain*, HCIR 2012, doi 10.1145/2391224.2391227 | ✅ |
| **sDCG** | Järvelin, Price, Delcambre & Nielsen, ECIR 2008, LNCS 4956, pp. 4–15, doi 10.1007/978-3-540-78646-7_4 | ✅ *(was ⬜)* |
| SRBP | Lipani, Carterette & Yilmaz, ICTIR 2019 | ✅ |
| Multi-query sessions | Kanoulas, Carterette, Clough & Sanderson, SIGIR 2011 | ✅ |
| Classical efficiency | Manning, Raghavan & Schütze, Ch. 4, 5, 7, 8, 20 | ✅ |

**Both Installment 3 deferrals resolved. Volume I contains zero ⬜ entries.**

---

# Appendix 4B — Volume I citation summary

| Installment | Chapters | Citations verified | Corrections issued |
|---|---|---|---|
| 1 | 0–4 | 9 | 0 |
| 2 | 5–7 | 11 | 0 |
| 3 | 8–10 | 19 | 0 |
| 4 | 11–12 | 15 | 0 |
| **Total** | **0–12** | **54** | **0** |

**Zero corrections across all of Volume I.** Every classical citation verified as stated on first
attempt.

Contrast with the RAG-era material: nine corrections across the catalogue and supplements, two of
them mine. The pattern is unambiguous and worth stating as a finding in its own right —
**pre-2015 heavily-cited work has been checked by many people; 2024–2026 preprints and their
secondary summaries have not.** Calibrate your trust accordingly, and verify anything from the
last two years before you build on it.

---

# Appendix 4C — Document set status

| # | Document | Covers | Status |
|---|---|---|---|
| 0 | `ir-rag-metrics-catalogue-v2.md` | Full index, 4 verification passes | Complete |
| 1 | `whitepaper-vol1-part1.md` | Ch 0–4 | Complete |
| 2 | `whitepaper-supplement-A.md` | Alignment, Integrity/Drift | Complete |
| 3 | `whitepaper-supplement-B.md` | Correctness, Efficiency | Complete |
| 4 | `whitepaper-supplement-A-addendum.md` | 🟡 lifts + CKA correction | Complete |
| 5 | `whitepaper-vol1-part2.md` | Ch 5–7 | Complete |
| 6 | `whitepaper-vol1-part3.md` | Ch 8–10 | Complete |
| 7 | **`whitepaper-vol1-part4.md`** | **Ch 11–12 + conclusion** | **this file** |

## ✅ VOLUME I COMPLETE

**Remaining in the plan:**

| Document | Contents | Prerequisites |
|---|---|---|
| Vol II final installment | Meta-evaluation; LLM-judge reliability; deployment playbooks; the narrowing exercise (70 metrics → a working set of 8–10) | Brehme survey read; three 🟡 entries still open (Perçin, GainRAG method, Trust-Score components) |

The Volume II installment is the one that turns all of this into something operational: a decision
tree from "what kind of system do you have" to "instrument these eight things," plus the
meta-evaluation material on whether your judges can be trusted at all.
