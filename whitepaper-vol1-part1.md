# Measuring Retrieval

## A Practitioner's White Paper on IR and RAG Evaluation

### Volume I — Foundations and Classical Information Retrieval
### Installment 1 of 4: Dimensions, Facets, and Set-Based Metrics

---

**Companion to:** `ir-rag-metrics-catalogue-v2.md`
**Status:** Installment 1 covers Chapters 0–4. Roadmap for the remainder is in §0.5.
**Citation policy:** every arXiv identifier in this document was verified against arXiv or
Semantic Scholar records. Entries carried from memory without a lookup are marked ⬜ UNVERIFIED.
Nothing in this paper is cited from recall alone without that mark.

---

# Chapter 0 — How To Read This Paper

## 0.1 Who this is for

You are building or maintaining a retrieval system. It might be classical search over a document
collection, or a RAG pipeline feeding an LLM, or — most likely in 2026 — a hybrid where a retriever
you inherited feeds a generator someone else chose, and nobody is quite sure which one is
responsible when the answers go wrong.

You have a dashboard. It has numbers on it. The numbers are green. You are not confident.

That last sentence is the reason this paper exists. Most retrieval evaluation failures are not
failures of measurement — they are failures of *interpretation*. The metric was computed correctly
and meant something other than what the reader assumed. A system can post 0.84 context adherence
while a third of its correct answers are ungrounded guesses. A retriever can hit 57.6% recall while
22% of what it returns is redundant with something else it returned. Both of those are real,
published findings, and neither is visible on a dashboard that tracks accuracy.

## 0.2 What this paper is not

It is not a survey. Two good ones already exist and you should read them:

| Survey | What it covers | ID |
|---|---|---|
| Gan et al. (2025) | Most comprehensive RAG evaluation survey; performance, factual accuracy, safety, computational efficiency | [arXiv:2504.14891](https://arxiv.org/abs/2504.14891) |
| Brehme, Ströhle & Breu (2025) | Systematic review of 63 papers; uniquely covers indexing and dataset generation | [arXiv:2504.20119](https://arxiv.org/abs/2504.20119) |

A survey tells you what exists. This paper tells you what to *do* — which metric to reach for,
what it will lie to you about, and what to put next to it so the lie is visible.

## 0.3 The diagram convention

Every metric gets a diagram. They are deliberately crude: stick figures, boxes, and a caption doing
the actual work. This is not decoration. A metric you cannot sketch on a whiteboard in thirty
seconds is a metric you do not understand well enough to defend in a design review.

If a diagram in this paper seems too simple, that is the point. The complexity in retrieval
evaluation is almost never in the mathematics. It is in remembering what the mathematics was
supposed to represent.

## 0.4 The per-metric template

Every metric from Chapter 4 onward follows this exact structure:

```
### Metric Name
  One-line          — what it measures, in a sentence
  Formula           — the actual computation
  Facets            — dimension | unit | supervision | stage
  The idea          — prose explanation
  Diagram           — the sketch
  Worked example    — real numbers, computed by hand
  Advantages        — when it earns its place
  Disadvantages     — how it misleads
  Domain examples   — three sectors, concretely
  Recommendation    — what to actually do
  Failure mode      — the specific way teams get burned
```

Skip to `Recommendation` if you are in a hurry. Read `Failure mode` if you are about to ship.

## 0.5 Roadmap

**Volume I — Classical IR**

| Installment | Chapters | Contents | Status |
|---|---|---|---|
| **1** | 0–4 | Dimensions, facets, signals-vs-metrics, set-based metrics | **this file** |
| 2 | 5–7 | Rank-based metrics; incomplete judgments; rank comparison and drift | planned |
| 3 | 8–10 | Diversity and novelty; fairness and exposure; online and counterfactual | planned |
| 4 | 11–12 | Significance and reporting; efficiency and cost | planned |

**Volume II — RAG-Era**

| Installment | Chapters | Contents |
|---|---|---|
| 5 | 13–15 | Grounding, attribution, citation quality |
| 6 | 16–18 | Alignment: utility, interference, the contribution family |
| 7 | 19–21 | Integrity, drift, staleness, robustness |
| 8 | 22–24 | Meta-evaluation, judge reliability, and deployment playbooks |

---

# Chapter 1 — The Four Dimensions

## 1.1 Why dimensions at all

A flat list of ninety metrics is not a catalogue. It is a menu, and menus encourage the worst
behaviour in evaluation: picking the metrics that are easy to compute, reporting all of them, and
letting the reader infer significance from quantity.

Dimensions impose a discipline: **every metric answers exactly one primary question.** If you cannot
say which question, you do not yet understand the metric well enough to report it.

```
        THE FOUR QUESTIONS
        ══════════════════

   CORRECTNESS          "Is this right?"
                         ↓
   ALIGNMENT            "Do my parts cooperate?"
                         ↓
   INTEGRITY / DRIFT    "Is it still right, six months on?"
                         ↓
   EFFICIENCY / COST    "What did being right cost me?"


        o    "All four are green."
       /|\
       / \

        o    "You have four metrics. You need four DIFFERENT metrics."
       /|\
       / \
```

## 1.2 Dimension I — Correctness

**The question:** is the retrieved or generated content actually right, relevant, grounded, and
cited correctly?

This is the dimension everyone starts with and most teams never leave. It covers precision, recall,
nDCG, faithfulness, citation accuracy, hallucination rate — the whole familiar apparatus.

Correctness has a seductive property: it is *locally verifiable*. You can look at one query, one
document, one claim, and say yes or no. This makes it easy to instrument, easy to explain to
stakeholders, and easy to over-trust.

**What Correctness cannot see:**

- Whether the right answer arrived for the wrong reason (see: the Accuracy Fallacy, §1.3)
- Whether your retriever and generator are working at cross purposes
- Whether today's 0.91 means the same thing as last quarter's 0.91
- What the 0.91 cost you in latency and tokens

```
   CORRECTNESS IS A PHOTOGRAPH, NOT A FILM

   ┌────────────────────┐
   │   Query #4,412     │      Correct? YES ✓
   │   Answer: "Bern"   │
   │   Truth:  "Bern"   │
   └────────────────────┘

        o     "We're at 91% correct!"
       /|\
       / \

        o     "On what? Retrieved from where? Compared to when?
       /|\      And how many tokens did that cost?"
       / \
```

## 1.3 Dimension II — Alignment

**The question:** do retrieval and generation actually cooperate?

This dimension does not exist in classical IR, because classical IR had only one component. The
moment you put a generator downstream of a retriever, a new class of failure appears: **both
components work, and the system still fails.**

The canonical evidence comes from RAG-E (Randl et al., [arXiv:2601.21803](https://arxiv.org/abs/2601.21803)),
which found that for 47.4–66.7% of queries the generator ignores the retriever's top-ranked
document, while 48.1–65.9% rely primarily on a document the retriever ranked as less relevant. They
name two failure modes:

- **Wasted retrieval** — the retriever found gold, the generator walked past it
- **Noise distraction** — the generator built its answer on a passage the retriever ranked low

```
      THE ALIGNMENT PROBLEM
      ═════════════════════

   RETRIEVER                    GENERATOR
   "Here are docs,              "Cool. I'll use
    ranked best first."          the third one."

    ┌──────────┐
    │ #1 ★★★★★ │ ──────────╮        o
    │ #2 ★★★★  │           │       /|\   "It's fine.
    │ #3 ★★    │ ◀─────────╯       / \    The answer was right."
    │ #4 ★     │
    └──────────┘

   Retriever metrics: EXCELLENT (nDCG 0.89)
   Generator metrics: EXCELLENT (faithfulness 0.84)
   System:            QUIETLY BROKEN

        o    "Which dashboard shows that?"
       /|\
       / \    "...none of them."
```

The sharpest published illustration is the **Accuracy Fallacy** from RAG-X
(Sivakumar, Sugumaran & Qiang, [arXiv:2603.03541](https://arxiv.org/abs/2603.03541)). On GuidelineQA,
their best pipeline scored 71% accuracy. Decomposed:

| Quadrant | Share | Meaning |
|---|---|---|
| Effective Use | 49.2% | Retriever found it, generator used it — genuine grounding |
| Lucky Guess | 33.9% | Retriever missed, generator was right anyway from parametric memory |
| Information Blindness | 8.5% | Retriever found it, generator ignored it |
| Correct Rejection | ~8.4% | Retriever missed, generator correctly showed low adherence |

And the detail that should worry you most: **context adherence on that same pipeline scored 0.84.**
The generator looked highly faithful while a third of its correct answers had no retrieved support
at all. The paper calls this the **Adherence Paradox**.

> **The single most important sentence in this chapter:** a faithfulness score is meaningless
> without a retrieval-hit denominator printed beside it. Faithfulness measures whether the answer
> matches the context. It does not measure whether the context contained the answer.

## 1.4 Dimension III — Integrity / Drift

**The question:** is the substrate trustworthy *over time*?

Correctness and Alignment are both measured at an instant. Integrity asks whether that instant
generalizes — to next month, to a new corpus, to a judge model that silently updated.

Four distinct things drift, and conflating them is the most common error in this dimension:

```
   FOUR THINGS THAT DRIFT (and they are NOT the same thing)
   ═══════════════════════════════════════════════════════

   1. THE CORPUS      Documents change. Policies get revised.
                      ──────────────────────────────────▶ time

   2. THE EMBEDDER    You upgrade the model. Vectors mean
                      something different now.
                      ──────────────────────────────────▶ time

   3. THE QUERIES     Users start asking about things that
                      didn't exist at launch.
                      ──────────────────────────────────▶ time

   4. THE JUDGE       Your LLM evaluator got a silent update.
                      Every longitudinal number is now void.
                      ──────────────────────────────────▶ time

        o    "Our drift metric is green."
       /|\
       / \   "Which of the four?"

        o    "...there are four?"
       /|\
       / \
```

Number 4 deserves special emphasis because it is invisible by construction. If your faithfulness
scores come from an LLM judge and that judge updates, nothing on your dashboard changes colour —
but every comparison against historical data has silently become invalid. Brehme et al. raise
exactly this: model advances could render previous evaluation results invalid, leaving open how to
establish a standard that stays consistent independent of LLM version.

The empirical picture for the corpus case is worse than most teams assume. VersionRAG
(Huwiler, Stockinger & Fürst, [arXiv:2510.08109](https://arxiv.org/abs/2510.08109)) reports that on
version-sensitive questions over technical documentation, naive RAG scores 58% and GraphRAG 64%,
against 90% for a version-aware pipeline. On *implicit change detection* — noticing that a document
changed without being told — the baselines score **0–10%**.

## 1.5 Dimension IV — Efficiency / Cost

**The question:** what did being right cost you?

In the original catalogue, latency, throughput, index size, and query cost were all filed under
`NA` — not a real dimension. That was wrong, and the field agrees: Gan et al.'s survey treats
computational efficiency as a co-equal axis alongside performance, factual accuracy, and safety.

The reason it must be a dimension rather than a footnote is that **it trades off directly against
Correctness**, and you cannot reason about a trade-off if one side is unmeasured.

```
      THE DIAL NOBODY LABELS
      ══════════════════════

              retrieve more ────────────▶ retrieve less
                    │                           │
        Correctness ▲                           ▼ Correctness
        Cost        ▲                           ▼ Cost
        Redundancy  ▲                           ▼ Redundancy

              ╭───────────────────────╮
              │    k = ???            │
              │    rerank depth = ??? │
              │    chunk size = ???   │
              ╰───────────────────────╯

        o    "We set k=5."
       /|\
       / \   "Why?"

        o    "It was in the tutorial."
       /|\
       / \
```

RAG-X gives the concrete number here: at MAP 0.44, **22% pairwise redundancy** between top-ranked
contexts, with an Exclusive Hit Rate at rank 2 of only 6.8%. Rank 2 was almost never contributing
anything rank 1 hadn't already supplied. That is a fifth of the context budget purchased and
discarded, and no Correctness metric will ever show it to you.

## 1.6 The dimension selection rule

```
   ┌─────────────────────────────────────────────────┐
   │  Before adding a metric to your dashboard:      │
   │                                                 │
   │  1. Which ONE dimension does it primarily       │
   │     answer?                                     │
   │                                                 │
   │  2. Do you already have a metric for that       │
   │     dimension?                                  │
   │                                                 │
   │  3. If yes — does this one measure something    │
   │     the existing one CANNOT?                    │
   │                                                 │
   │  If you cannot answer 3, you are adding noise,  │
   │  not signal.                                    │
   └─────────────────────────────────────────────────┘
```

A dashboard with one strong metric per dimension beats a dashboard with nine Correctness metrics.
The nine will correlate, they will move together, and their agreement will feel like corroboration
when it is actually a single measurement wearing nine hats. We will return to this in Volume II
with a concrete example: eRAG, Gain, DIG, and ΔSePer are four published metrics that all measure
passage contribution by differencing model behaviour with and without the passage. Reporting all
four does not quadruple your evidence.

---

# Chapter 2 — The Facet System

Dimensions tell you what question a metric answers. Facets tell you what it is *comparable to*.
Without them, teams routinely place a claim-level judge score next to a query-level ranking metric
and average them.

## 2.1 Facet A — Unit of analysis

```
   THE UNIT LADDER
   ═══════════════

   SYSTEM     ┃ one number for the whole deployment
              ┃  e.g. Elo, index size
   ───────────┃──────────────────────────────────────
   CORPUS     ┃ one number for the document collection
              ┃  e.g. coverage, pool bias, drift
   ───────────┃──────────────────────────────────────
   SESSION    ┃ one number per user journey
              ┃  e.g. sDCG, abandonment
   ───────────┃──────────────────────────────────────
   QUERY      ┃ one number per question
              ┃  e.g. nDCG, MRR, accuracy
   ───────────┃──────────────────────────────────────
   PASSAGE    ┃ one number per retrieved chunk
              ┃  e.g. DIG, Gain, context relevance
   ───────────┃──────────────────────────────────────
   CLAIM      ┃ one number per atomic assertion
              ┃  e.g. FActScore, Claim Recall


        o     "Our average score is 0.82."
       /|\
       / \    "Averaged over claims or over queries?"

        o     "Does it matter?"
       /|\
       / \

        o     "A query with 40 claims and a query with 2
       /|\     both count once at query level. They do NOT
       / \     count equally at claim level."
```

**The rule:** aggregate within a unit, never across units. A claim-level metric and a query-level
metric can appear on the same dashboard; they cannot appear in the same average.

## 2.2 Facet B — Supervision

| Value | Meaning | CI-friendly? | Cost |
|---|---|---|---|
| **ref** | Reference-based; needs golden answers | Yes | Label creation |
| **free** | Reference-free; needs no ground truth | Yes | Compute only |
| **judge** | LLM-as-judge scoring | Partly | API calls + drift risk |
| **human** | Human annotation | No | Time, expertise |

This facet is not academic. It determines *what you can run per commit*.

```
   THE CI GATE
   ═══════════

   every commit  ──▶  ref + free metrics      (fast, deterministic)
                          │
   nightly       ──▶  judge metrics           (slow, costs money, drifts)
                          │
   per release   ──▶  human anchor set        (slow, expensive, truth)

        o   "We run the full eval suite on every PR."
       /|\
       / \  "Including the LLM judge?"

        o   "...that's why the bill is like that."
       /|\
       / \
```

RAGAS is reference-free, which is precisely why it dominates CI/CD adoption — no golden answers
required. ALCE is reference-based. That single difference matters more for your engineering
practice than any difference in what they measure.

## 2.3 Facet C — Stage

```
   WHERE DOES THE METRIC LOOK?
   ═══════════════════════════

        ┌──────────┐          ┌──────────┐
   Q ──▶│ RETRIEVER│───ctx───▶│ GENERATOR│──▶ A
        └──────────┘          └──────────┘
             ▲                     ▲
             │                     │
            [R]                   [G]
        retriever-only        generator-only
        nDCG, MRR, recall     faithfulness, Trust-Score

        └──────────[E2E]────────────┘
              end-to-end
        accuracy, CUE, eRAG, WARG
```

The diagnostic value of this facet is high. If your E2E number drops and you do not have R and G
numbers beside it, you cannot localize the regression. This is the entire argument of RAG-X: RAG-X
decouples retrieval and generation performance to enable fine-grained error attribution, because
aggregate metrics fail to reveal whether an error stems from faulty retrieval or flawed generation.

## 2.4 Facet D — Verification tier

A late addition, and the one I got wrong myself while building the source catalogue.

| Mark | Meaning |
|---|---|
| ⬤ | Established — widely adopted, multiple independent uses |
| ◐ | Emerging — published, not yet widely replicated |
| ○ | Practitioner-only — blog/industry, no peer review |
| ✅ | Citation verified against primary source this pass |
| ⬜ | Citation asserted from memory, NOT verified |

**These are independent axes.** During construction of the companion catalogue, the AIS metric —
about as established as anything in attribution research — was carried with the venue "TACL'23".
It is actually *Computational Linguistics* 49(4):777–840. Established and verified are different
properties, and conflating them is how bad citations propagate.

```
        o    "It's a famous paper, I know the citation."
       /|\
       / \

        o    "Famous is not the same as checked."
       /|\
       / \

   [ Running total across four verification passes of the
     companion catalogue: 34 identifiers checked, 1 wrong.
     The wrong one came from the person most confident. ]
```

---

# Chapter 3 — Signals Are Not Metrics

## 3.1 The category error

The single largest structural defect in most metric catalogues is mixing three different kinds of
object into one table:

```
   ┌─────────────────┬──────────────────┬─────────────────┐
   │  SIGNALS        │  PARAMETERS      │  METRICS        │
   │  (features)     │  (knobs)         │  (measurements) │
   ├─────────────────┼──────────────────┼─────────────────┤
   │  tf-idf         │  BM25 k₁, b      │  nDCG           │
   │  BM25 score     │  smoothing λ     │  MAP            │
   │  cosine sim     │  # expansion     │  MRR            │
   │  PageRank       │    terms         │  recall@k       │
   │  query-likelihood│ chunk size      │  faithfulness   │
   ├─────────────────┼──────────────────┼─────────────────┤
   │ You RANK with   │ You TUNE these   │ You REPORT      │
   │ these           │                  │ these           │
   └─────────────────┴──────────────────┴─────────────────┘

        o    "BM25's b parameter — is that Correctness?"
       /|\
       / \

        o    "It's a knob. Knobs don't have dimensions.
       /|\     The METRIC you turn the knob to improve
       / \     has a dimension."
```

Asking "what dimension is `b`?" is a category error of the same shape as asking what colour the
number seven is. `b` is a length-normalization parameter in the BM25 scoring function. You tune it
to improve nDCG. nDCG has a dimension. `b` does not.

## 3.2 Why this matters practically

Three concrete harms:

1. **It corrupts your dimension counts.** If eleven of your "Correctness metrics" are actually
   ranking features, you have far less Correctness coverage than you think.

2. **It invites optimizing the wrong object.** Teams start reporting "our BM25 score improved,"
   which is not a statement about quality. Raw retrieval scores are not comparable across queries,
   across corpora, or across index rebuilds.

3. **It hides genuine gaps.** A catalogue padded with signals looks comprehensive. Strip them out
   and the actual measurement coverage is often thin — especially in Alignment and Integrity.

## 3.3 The test

```
   ┌────────────────────────────────────────────────┐
   │  IS IT A METRIC?                               │
   │                                                │
   │  Q: Could I put this number in a quarterly     │
   │     report as evidence the system is good?     │
   │                                                │
   │  "Our nDCG@10 is 0.71"          ──▶ METRIC     │
   │  "Our BM25 b is 0.75"           ──▶ knob       │
   │  "Our mean cosine sim is 0.83"  ──▶ signal     │
   │                                                │
   │  If the honest follow-up is "...and?",         │
   │  it is not a metric.                           │
   └────────────────────────────────────────────────┘
```

Note the third example carefully. Mean cosine similarity of retrieved chunks *feels* like a quality
metric and is reported as one constantly. It is not. A retriever returning five near-identical
irrelevant chunks can post a high mean similarity. Similarity to the query is a ranking signal;
whether the ranking was good is a separate measurement requiring relevance judgments.

## 3.4 The one legitimate exception

Signal *effects* are metrics. "Relevance-feedback effectiveness" — the delta in MAP from applying
Rocchio — is a genuine Alignment measurement. The distinction:

| Not a metric | Metric |
|---|---|
| Rocchio α, β, γ values | Δ MAP after relevance feedback |
| Number of expansion terms | Δ recall after query expansion |
| Chunk size | Δ Effective Use across chunk sizes |
| Embedding dimensionality | Δ nDCG across embedders |

The pattern: **a knob becomes a metric when you measure the difference it makes.**

---

# Chapter 4 — Set-Based Metrics

We begin with the oldest family. Everything in this chapter predates the web, most of it predates
1980, and all of it is still in your dashboard.

## 4.0 The confusion matrix, and why it deserves respect

```
                    RETRIEVED?
                 YES        NO
              ┌─────────┬─────────┐
        YES   │   TP    │   FN    │  ← relevant docs
   RELEVANT?  │  (win)  │ (missed)│
              ├─────────┼─────────┤
        NO    │   FP    │   TN    │  ← irrelevant docs
              │ (noise) │ (fine)  │
              └─────────┴─────────┘

   PRECISION = TP / (TP + FP)     "of what I returned, how much was good?"
   RECALL    = TP / (TP + FN)     "of what was good, how much did I return?"


   THE ASYMMETRY NOBODY MENTIONS:
   TN is enormous and useless. In a 10M-document corpus with
   20 relevant documents, TN ≈ 9,999,980. Any metric that uses
   TN (like plain accuracy) will read 0.999998 for a system
   that returns nothing at all.

        o    "Our retrieval accuracy is 99.9998%!"
       /|\
       / \

        o    "Your system returns the empty set."
       /|\
       / \   "...yes."
```

This is *the* reason IR uses precision and recall rather than accuracy. It is worth internalizing,
because the same trap reappears in RAG: any metric whose denominator is dominated by trivially
correct cases will look excellent and mean nothing.

---

## 4.1 Precision

**One-line:** Of the documents you returned, what fraction were relevant?

**Formula:** `P = TP / (TP + FP)`

**Facets:** Correctness | query | ref | R | ⬤ ✅ *(Manning, Raghavan & Schütze, Ch. 8)*

### The idea

Precision is the metric of *not wasting the reader's time*. It asks nothing about what you missed.
A system returning exactly one relevant document and nothing else scores a perfect 1.0, even if
nine hundred other relevant documents exist.

### Diagram

```
        THE FISHERMAN'S FIRST QUESTION
        ══════════════════════════════

   "Is everything in my net actually a fish?"

         ╔═══════════════╗
         ║  ><>   ><>    ║       ╔═══════════════╗
         ║      ><>      ║       ║  ><>   [boot] ║
         ║  ><>          ║       ║  [can] ><>    ║
         ╚═══════════════╝       ╚═══════════════╝
          PRECISION = 1.0         PRECISION = 0.5

              o                        o
             /|\  "Perfect!"          /|\  "Half my net is garbage."
             / \                      / \

   Neither figure has ANY idea how many fish are still
   in the river. That is a different question entirely.
```

### Worked example

A legal search returns 10 documents for "force majeure precedent, shipping, 2020–2024".
A paralegal reviews them: 6 are on point, 4 are about force majeure in construction contracts.

```
   TP = 6,  FP = 4
   P = 6 / (6 + 4) = 0.60
```

Sixty percent of the reviewer's reading time was well spent.

### Advantages

- **Directly interpretable as wasted effort.** `1 − P` is the fraction of returned material a human
  must read and discard. No other metric maps so cleanly onto a cost.
- **Cheap to judge.** You only need labels for what you returned, not for the whole corpus.
- **Robust to corpus size.** Unlike recall, it does not require knowing the total relevant set.

### Disadvantages

- **Silent about misses.** This is the big one. Precision cannot distinguish a system that found
  everything from one that found almost nothing, as long as both were tidy about it.
- **Trivially gamed by returning less.** Return only your single most confident result and precision
  climbs. This is why unqualified precision is nearly useless as an optimization target.
- **Ignores rank.** Precision@10 treats a relevant document at position 1 and position 10
  identically. Chapter 5 exists to fix this.
- **Set-based judgment hides gradation.** A "partially relevant" document must be forced into a
  binary. Graded relevance metrics (nDCG) handle this better.

### Domain examples

**Legal / e-discovery.** Precision is a direct budget line. In a document review costing roughly
$1–3 per document reviewed, a precision drop from 0.6 to 0.4 on a 50,000-document production is a
six-figure increase in review cost. Legal teams often specify contractual precision floors.

**Clinical decision support.** Here precision is a *safety* metric, not a cost metric. A clinician
receiving five guideline excerpts where two are for the wrong patient population is not merely
inconvenienced — the irrelevant material actively competes for attention during a time-pressured
decision. This is the setting where RAG-X found 22% pairwise redundancy: the same guidance
returned twice crowds out guidance that was never returned at all.

**E-commerce search.** Precision maps to conversion. A shopper searching "waterproof hiking boots
women's 8" who receives men's boots and non-waterproof boots in the top 10 will typically abandon
rather than scroll. Note that in this domain, precision at very shallow depth (P@3, P@5) matters far
more than P@10, because mobile viewports show three results.

### Recommendation

**Never report precision alone.** Always pair it with recall or a recall proxy. The standard pairing
is F1 (§4.3), but in production the more useful pairing is precision at a fixed shallow depth
alongside recall at a deeper one — for example, P@3 with Recall@50. These answer two genuinely
different operational questions: "is the top of the page clean?" and "did we find it at all?"

Set your depth to match your interface. If your UI shows 3 results, P@10 is measuring something no
user experiences.

### Failure mode to watch

```
   THE PRECISION RATCHET

   Week 1:  P@10 = 0.55, k = 10
   Week 4:  P@10 = 0.71, k = 10   "Great progress!"
   Week 8:  P@5  = 0.80, k = 5    "Even better!"
   Week 12: P@3  = 0.91, k = 3    "Best quarter ever!"

        o    "Recall over the same period?"
       /|\
       / \

        o    "We stopped tracking it in week 3."
       /|\
       / \

   The team optimized precision by returning less. Every
   number went up. The system found strictly less material
   every single week.
```

---

## 4.2 Recall

**One-line:** Of all the relevant documents that exist, what fraction did you return?

**Formula:** `R = TP / (TP + FN)`

**Facets:** Correctness | query | ref | R | ⬤ ✅ *(Manning Ch. 8)*

### The idea

Recall is the metric of *not missing things*. It is precision's mirror and its natural adversary:
you can almost always buy one with the other by adjusting how much you return.

Recall has a structural problem precision does not: computing it requires knowing `FN`, the relevant
documents you *failed* to return. In a corpus of any size, nobody knows that number. This is the
single hardest practical problem in retrieval evaluation, and Chapter 6 is devoted to it.

### Diagram

```
        THE FISHERMAN'S SECOND QUESTION
        ═══════════════════════════════

   "Did I get all the fish?"

     ╔═══════════╗
     ║  ><>  ><> ║        ~~~~~~~~~~~~~~~~~~~~~~~~
     ╚═══════════╝        ~  ><>    ><>    ><>   ~
       2 caught           ~     ><>      ><>     ~
                          ~~~~~~~~~~~~~~~~~~~~~~~~
                              5 still out there

              RECALL = 2 / 7 = 0.29

        o    "How do you know there are 7?"
       /|\
       / \

        o    "...I drained the river and counted."
       /|\
       / \

        o    "You cannot drain a 10-million-document river.
       /|\     This is why Chapter 6 exists."
       / \
```

### Worked example

Continuing the legal search. To establish truth, a senior associate reviews a random sample plus a
targeted search and concludes there were 15 genuinely on-point documents in the corpus. Your system
returned 6 of them.

```
   TP = 6,  FN = 9
   R = 6 / (6 + 9) = 0.40

   Note: precision was 0.60, recall is 0.40.
   Two numbers, same result set, very different stories.
```

### Advantages

- **The right metric when misses are expensive.** In legal discovery, medical safety, patent search,
  and compliance, a missed document can be catastrophic in a way that a redundant document is not.
- **Harder to game than precision.** You can inflate recall by returning everything, but that
  destroys precision so visibly that the gaming is self-announcing.
- **Sets the ceiling for everything downstream.** This is under-appreciated in RAG: **your generator
  cannot use what your retriever did not fetch.** Recall is the upper bound on Effective Use.

### Disadvantages

- **The denominator is usually unknowable.** This is not a minor caveat. Reported recall in most
  production systems is recall *against a labelled subset*, which can differ from true recall by a
  wide and unmeasured margin.
- **Trivially gamed by returning more.** Recall@1000 will look wonderful and mean nothing.
- **Says nothing about rank or redundancy.** Recall 0.9 achieved by returning the same fact nine
  times looks identical to recall 0.9 across nine distinct facts. RAG-X's Exclusive Hit Rate exists
  precisely to catch this.
- **Insensitive to context-window economics.** In RAG, high recall at k=50 is worthless if you can
  only fit 5 chunks in the prompt.

### Domain examples

**Patent prior-art search.** Recall is close to the only metric that matters. Missing a single
prior-art reference can invalidate a patent later at enormous cost. Searches routinely accept
precision below 0.1 in exchange for recall above 0.95 — the reviewer's time is cheap relative to
the downside.

**Pharmacovigilance / adverse-event detection.** Regulatory obligation makes missed reports a
compliance failure. Systems are tuned to very high recall with human triage absorbing the false
positives. Note the interaction with Chapter 12: this is a domain where the *cost* dimension is
consciously sacrificed.

**Customer-support RAG.** Here the calculus inverts. A support bot that retrieves 50 chunks to
guarantee recall will blow its context budget, and *Lost in the Middle* (Liu et al., TACL,
[arXiv:2307.03172](https://arxiv.org/abs/2307.03172) ✅) tells us the material in the middle of that
long context will be under-used anyway. Recall past what the generator can actually attend to is
recall you paid for and did not receive.

### Recommendation

Report recall at the depth your generator actually consumes, not at the depth your retriever
returns. If you retrieve 50 and pass 5 to the model, **Recall@5 is your real recall.** Recall@50 is
a statement about a reranker you may not have.

For domains where misses are expensive, do not chase recall alone — pair it with a *coverage
estimate* of how much of the relevant set your labels cover. An unqualified "recall 0.85" against
labels covering 10% of the corpus is a claim about your labels, not your system.

### Failure mode to watch

```
   THE RECALL MIRAGE

   Reported:  Recall@50 = 0.92    ✓ looks great
   Passed to generator:  top 5
   Actual Recall@5:      0.61
   Lost in the middle of those 5:  ~unknown

        o     "Our retriever has 92% recall."
       /|\
       / \

        o     "Your GENERATOR has 61% recall,
       /|\      and that's the number that
       / \      determines the answer."
```

---

## 4.3 F-measure, F1, and Fβ

**One-line:** The harmonic mean of precision and recall, optionally weighted toward one of them.

**Formula:**
```
   F1 = 2PR / (P + R)

   Fβ = (1 + β²) · PR / (β²P + R)

   β < 1  →  weights PRECISION more
   β = 1  →  balanced (F1)
   β > 1  →  weights RECALL more
```

**Facets:** Correctness | query | ref | R | ⬤ ✅ *(Manning Ch. 8)*

### The idea

F-measure exists because reporting two numbers invites cherry-picking. It collapses precision and
recall into one figure using the *harmonic* mean rather than the arithmetic mean — which is the
entire point, and the part most people forget.

### Diagram

```
   WHY HARMONIC, NOT ARITHMETIC
   ════════════════════════════

   System A:  P = 0.50,  R = 0.50
   System B:  P = 1.00,  R = 0.01   ← returns 1 doc, it's right

   ARITHMETIC MEAN:
      A: 0.500      B: 0.505   ← B "wins"

   HARMONIC MEAN (F1):
      A: 0.500      B: 0.020   ← B is correctly destroyed


        o    "System B has the highest average score!"
       /|\
       / \

        o    "System B returns one document and
       /|\     ignores 99% of the corpus."
       / \

   The harmonic mean PUNISHES IMBALANCE.
   That is not a side effect. That is the feature.
```

### Worked example

Our legal search: P = 0.60, R = 0.40.

```
   F1 = 2(0.60)(0.40) / (0.60 + 0.40)
      = 0.48 / 1.00
      = 0.48

   Now suppose it's e-discovery, where misses are 4× worse
   than wasted reading. Use β = 2:

   F2 = (1 + 4)(0.60)(0.40) / (4·0.60 + 0.40)
      = 5(0.24) / (2.4 + 0.4)
      = 1.20 / 2.80
      = 0.43

   F2 < F1 because this system's weakness IS recall,
   and F2 weights recall more heavily.
```

That last line is the whole value of β. Choosing β is choosing which failure you fear.

### Advantages

- **One number, honestly derived.** Unlike an arithmetic average, F1 cannot be gamed by extreme
  imbalance.
- **β makes your priorities explicit and auditable.** Writing "we optimize F2 because missed
  documents cost 4× more than reviewed ones" is a defensible, reviewable engineering statement.
- **Standard and comparable.** Nearly universal, so external benchmarks are interpretable.

### Disadvantages

- **Collapses information you often need.** F1 = 0.48 could be (0.6, 0.4) or (0.4, 0.6). Those
  demand entirely different fixes. **Always report P and R alongside F1.**
- **β is usually chosen by default, not by analysis.** Most teams use F1 because it is the default,
  not because their costs are symmetric. They almost never are.
- **Still rank-blind and still set-based.** All of §4.1's and §4.2's limitations carry over.
- **Poor fit for graded relevance.** Forcing "somewhat relevant" into binary loses real signal.
- **Misleading under class imbalance across queries.** Macro-averaged F1 over queries with wildly
  different relevant-set sizes can be dominated by easy queries.

### Domain examples

**E-discovery.** F2 or even F3 is common, formalizing that missing responsive documents carries
sanction risk while over-inclusion carries only review cost. Some protocols specify the β in the
discovery agreement itself.

**Spam / abuse filtering in search.** F0.5 is typical — suppressing a legitimate result (a precision
failure from the user's perspective) is worse than letting one spam result through.

**RAG chunk selection.** Here F-measure is often the *wrong* tool, and it is worth saying so
explicitly. Chunk-level precision and recall assume chunks are independently relevant. They are not:
two chunks can be individually relevant and jointly redundant, or individually marginal and jointly
sufficient. This is exactly the set-level property SURE-RAG
([arXiv:2605.03534](https://arxiv.org/abs/2605.03534)) was built to capture — it treats evidence
sufficiency as a set-level property because missing hops and unresolved conflicts cannot be detected
by scoring passages independently.

### Recommendation

Use F1 as a *summary* line, never as the primary optimization target, and never without P and R
printed next to it. Choose β deliberately: write down the relative cost of a false positive versus a
false negative in your domain, in whatever units you actually care about (dollars, minutes, risk),
and derive β from that ratio rather than accepting 1.

If you cannot articulate that cost ratio, that is useful information: it means you do not yet know
what your system is for.

### Failure mode to watch

```
   THE F1 PLATEAU

   Q1:  P=0.50 R=0.50  F1=0.50
   Q2:  P=0.60 R=0.42  F1=0.49
   Q3:  P=0.70 R=0.36  F1=0.48
   Q4:  P=0.80 R=0.31  F1=0.45

        o    "F1 is basically flat. We've plateaued."
       /|\
       / \

        o    "You haven't plateaued. You've been trading
       /|\     recall for precision for a year and F1
       / \     hid the whole trade from you."

   F1 moving slowly can mean 'no change' or it can mean
   'large opposing changes'. Only P and R can tell you which.
```

---

## 4.4 Precision@K

**One-line:** Precision computed over only the top K results.

**Formula:** `P@K = (relevant documents in top K) / K`

**Facets:** Correctness | query | ref | R | ⬤ ✅ *(Manning Ch. 8)*

### The idea

Plain precision assumes a result *set*. Real systems produce a result *list*, and users see the top
of it. P@K is the minimal acknowledgement that position matters — not by weighting positions, but by
drawing a hard line and ignoring everything past it.

### Diagram

```
   THE CUTOFF IS AN INTERFACE DECISION
   ═══════════════════════════════════

   ┌─────────────┐
   │ 1. ✓ relevant│  ┐
   │ 2. ✗         │  │ P@3 = 2/3 = 0.67
   │ 3. ✓ relevant│  ┘
   ├─────────────┤
   │ 4. ✗         │  ┐
   │ 5. ✓ relevant│  │ P@10 = 5/10 = 0.50
   │ 6. ✗         │  │
   │ 7. ✗         │  │
   │ 8. ✓ relevant│  │
   │ 9. ✗         │  │
   │10. ✓ relevant│  ┘
   └─────────────┘

        o    "Which one do we report?"
       /|\
       / \

        o    "How many results does your UI show?"
       /|\
       / \

        o    "Three."
       /|\
       / \   "Then P@10 is measuring an experience
              no human being has ever had."
```

### Worked example

A RAG pipeline retrieves 10 chunks but passes only the top 3 into the prompt (context budget).

```
   Relevant chunks at positions: 1, 3, 5, 8, 10

   P@3  = 2/3  = 0.67   ← what the GENERATOR sees
   P@5  = 3/5  = 0.60
   P@10 = 5/10 = 0.50   ← what the RETRIEVER produced

   The number that determines answer quality is P@3.
   The number most teams report is P@10.
```

### Advantages

- **Matches how systems are actually consumed.** Both humans and context windows are truncated.
- **No need for full corpus labels.** You judge K documents per query. That is a tractable
  annotation budget.
- **Directly actionable.** P@3 too low? Your reranker is the problem, not your recall.
- **Composable with the context budget.** In RAG, setting K to your prompt's chunk capacity turns
  P@K into a genuine measure of what the generator receives.

### Disadvantages

- **Rank-blind within the window.** Relevant at 1,2,3 scores the same as relevant at 8,9,10 for
  P@10. Users emphatically do not experience these as equivalent.
- **Arbitrary cutoff creates a cliff.** A document at position K+1 contributes nothing; at position
  K it contributes fully. Small ranking changes cause discontinuous metric jumps.
- **Not comparable across different K.** P@3 and P@10 are different metrics, not different
  precisions of the same thing.
- **Insensitive to how many relevant documents exist.** If only one relevant document exists,
  P@10 caps at 0.1 no matter how perfect the system. This is the flaw R-Precision was invented to
  fix (Installment 2).

### Domain examples

**Mobile e-commerce.** P@3 or P@4, matched to viewport. Anything deeper is measuring scroll
behaviour that most sessions never exhibit.

**RAG with a tight context budget.** Set K to the number of chunks you actually inject. If you
inject 5 chunks of 1,024 tokens, P@5 is your operative precision. RAG-X used k=3 with 1,024-token
chunks, which is a defensible, explicitly stated configuration — and the explicitness matters as
much as the value.

**Enterprise document search with expert users.** Here deeper K is legitimate. A financial analyst
searching filings will genuinely scan 20 results. P@20 is a real measurement of their experience,
not a theoretical one.

### Recommendation

**Choose K from your interface or your context window, then never change it silently.** If you must
change K, report both the old and new value for at least one release cycle, and expect the metric to
move for reasons unrelated to quality.

Report at least two depths — a shallow one matching what is consumed, and a deeper one matching what
is retrieved. The gap between them is your reranker's headroom.

### Failure mode to watch

```
   THE PHANTOM DEPTH

   Retriever config:  return top 50
   Reranker config:   rerank top 50 → top 10
   Prompt builder:    inject top 4  ← nobody remembers this
   Dashboard:         P@10

        o    "P@10 = 0.70. We're good."
       /|\
       / \

        o    "Six of those ten never reach the model."
       /|\
       / \

   The dashboard measures a stage of the pipeline that
   does not determine the output. Trace your actual
   injection count before choosing K.
```

---

## 4.5 Chapter 4 summary card

```
┌──────────────────────────────────────────────────────────────┐
│  SET-BASED METRICS: THE ONE-PAGE VERSION                     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Precision   "Was what I returned good?"                     │
│              → gamed by returning LESS                       │
│                                                              │
│  Recall      "Did I return what was good?"                   │
│              → gamed by returning MORE                       │
│              → denominator usually unknowable                │
│                                                              │
│  F1 / Fβ     "Both, harmonically, with a priority"           │
│              → NEVER report without P and R beside it        │
│              → choose β from real cost ratios                │
│                                                              │
│  P@K         "Was the part they SAW good?"                   │
│              → set K from your interface / context budget    │
│              → rank-blind within the window                  │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  ALL FOUR ARE RANK-BLIND.                                    │
│  ALL FOUR ASSUME BINARY RELEVANCE.                           │
│  Chapter 5 fixes rank. Chapter 5 also fixes gradation.       │
├──────────────────────────────────────────────────────────────┤
│  THE RAG-SPECIFIC WARNING:                                   │
│  These metrics score passages INDEPENDENTLY. Evidence        │
│  sufficiency is a SET property. Two individually-relevant    │
│  passages can be jointly redundant; two individually-weak    │
│  ones can be jointly sufficient. Nothing in this chapter     │
│  can see that. (See SURE-RAG, arXiv:2605.03534.)             │
└──────────────────────────────────────────────────────────────┘
```

---

# Appendix 1A — Verified sources cited in this installment

| # | Work | Identifier | Status |
|---|---|---|---|
| 1 | Manning, Raghavan & Schütze, *Introduction to Information Retrieval* | Cambridge UP, 2008 | ⬤ standard text |
| 2 | Gan et al., *RAG Evaluation in the Era of LLMs: A Comprehensive Survey* | [2504.14891](https://arxiv.org/abs/2504.14891) | ✅ |
| 3 | Brehme, Ströhle & Breu, *Can LLMs Be Trusted for Evaluating RAG Systems?* | [2504.20119](https://arxiv.org/abs/2504.20119) | ✅ |
| 4 | Randl et al., *RAG-E: Quantifying Retriever-Generator Alignment* | [2601.21803](https://arxiv.org/abs/2601.21803) | ✅ |
| 5 | Sivakumar, Sugumaran & Qiang, *RAG-X* | [2603.03541](https://arxiv.org/abs/2603.03541) | ✅ |
| 6 | Huwiler, Stockinger & Fürst, *VersionRAG* | [2510.08109](https://arxiv.org/abs/2510.08109) | ✅ |
| 7 | Liu et al., *Lost in the Middle* | [2307.03172](https://arxiv.org/abs/2307.03172) | ✅ |
| 8 | Qiu, Han & Huang, *SURE-RAG* | [2605.03534](https://arxiv.org/abs/2605.03534) | ✅ |
| 9 | Rashkin et al., *Measuring Attribution in NLG* | *Computational Linguistics* 49(4):777–840, 2023 | ✅ (venue corrected) |

---

# Appendix 1B — What Installment 2 covers

Chapter 5 introduces rank sensitivity and graded relevance:

- **MRR** — the metric for "one right answer exists"
- **MAP** — averaging precision at every relevant position
- **DCG / nDCG** — logarithmic position discount, graded relevance
- **ERR** *(Chapelle et al., CIKM'09)* ⬜ — cascade model, stops at satisfaction
- **RBP** *(Moffat & Zobel, TOIS'08)* ⬜ — geometric persistence, **with an explicit residual for
  unjudged documents**, which makes it the bridge into Chapter 6

Chapter 6 confronts the recall denominator problem directly: **bpref**, **infAP**, pooling depth
bias, and assessor agreement.

Chapter 7 covers rank comparison and the drift application: **Kendall's τ**, **Spearman ρ**, and
**RBO** *(Webber, Moffat & Zobel, TOIS'10)* ⬜ — plus **CKA**, **Jaccard**, and **RankSimilarity**
from Caspari et al. ([arXiv:2407.08275](https://arxiv.org/abs/2407.08275) ✅), which together form
the only fully-sourced drift stack currently available.

⬜ marks above indicate citations I have asserted but not yet verified against primary records.
They will be verified before Installment 2 ships, per the policy in the header.
