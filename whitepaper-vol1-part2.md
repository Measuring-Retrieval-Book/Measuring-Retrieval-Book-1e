# Measuring Retrieval

## Volume I — Foundations and Classical Information Retrieval
### Installment 2 of 4: Chapters 5–7
#### Rank-Based Metrics · Incomplete Judgments · Rank Comparison and Drift

---

**Citation status.** All five citations marked ⬜ UNVERIFIED in Installment 1 have been verified
against primary or authoritative secondary records and are now ✅. Full ledger in Appendix 2A.

**Reading order.** These three chapters form one argument:

```
   Ch 5  Rank matters. Here is how to weight it.
              │
              │  ...but every rank metric needs to know
              │     which documents are relevant.
              ▼
   Ch 6  You do not know that. Here is how to cope.
              │
              │  ...and RBP's residual points at a
              │     second use for rank metrics entirely.
              ▼
   Ch 7  Comparing two rankings — which is how you
         measure drift.
```

---

# Chapter 5 — Rank-Based Metrics

## 5.0 What Chapter 4 could not do

Every metric in Chapter 4 was rank-blind. P@10 scored relevant-at-positions-1,2,3 identically to
relevant-at-positions-8,9,10. No user experiences those as equivalent.

Rank-based metrics fix this by applying a **discount**: a weight that decreases with position. The
entire chapter is a series of answers to one question — *what shape should the discount be?*

```
   FOUR ANSWERS TO ONE QUESTION
   ════════════════════════════

   weight
     1.0 ┤●
         │ ●                MRR:  only the FIRST hit counts
     0.5 ┤  ●
         │   ●●             MAP:  average precision at each hit
         │     ●●●
     0.0 ┤        ●●●●●●    nDCG: 1/log₂(i+1)  — gentle
         └─┬─┬─┬─┬─┬─┬─┬─   ERR:  stops when satisfied
           1 2 3 4 5 6 7    RBP:  p^(i-1) — geometric
              rank

        o    "Which discount is correct?"
       /|\
       / \

        o    "None. Each encodes a different THEORY
       /|\     of how a user reads a result list.
       / \     Pick the theory that matches your user."
```

That framing — a metric as a **user model** — is the single most useful idea in classical IR
evaluation, and it is what makes UDCG (Supplement A §A.4.1) comprehensible: UDCG's contribution is
noticing that when the "user" is an LLM, every discount above encodes the wrong theory.

---

## 5.1 MRR — Mean Reciprocal Rank

**One-line:** The reciprocal of the position of the first relevant result, averaged over queries.

**Formula:**
```
   RR   = 1 / rank of first relevant result
   MRR  = (1/|Q|) · Σ_{q∈Q} 1/rank_q

   If no relevant result is retrieved, RR = 0.
```

**Facets:** Correctness | query | ref | R | ⬤ ✅ *(standard; popularized via TREC QA tracks)*

### The idea

MRR encodes the strictest possible user model: **the user looks until they find one good result,
then stops and never returns.** Everything after the first relevant hit is invisible.

This sounds crude and is exactly right for a large class of problems.

### Diagram

```
   THE USER WHO STOPS
   ══════════════════

   ┌──────────────┐        ┌──────────────┐
   │ 1. ✗         │        │ 1. ✓  ←STOP  │
   │ 2. ✗         │        │ 2. ✓         │
   │ 3. ✓  ←STOP  │        │ 3. ✓         │
   │ 4. ✓         │        │ 4. ✓         │
   │ 5. ✓         │        │ 5. ✓         │
   └──────────────┘        └──────────────┘
      RR = 1/3 = 0.33         RR = 1/1 = 1.00

   The left list has FOUR relevant results.
   The right list has FIVE.
   MRR cares about neither number.

        o    "That throws away most of the information."
       /|\
       / \

        o    "Deliberately. If your user needs ONE
       /|\     answer, the other four are decoration."
       / \
```

### Worked example

Five queries, position of first relevant result:

```
   q1: rank 1  →  RR = 1.000
   q2: rank 3  →  RR = 0.333
   q3: rank 2  →  RR = 0.500
   q4: none    →  RR = 0.000
   q5: rank 1  →  RR = 1.000
                       ─────
   MRR = (1.000+0.333+0.500+0.000+1.000)/5 = 0.567
```

Note the harshness of the drop-off: rank 1 → 1.00, rank 2 → 0.50, rank 3 → 0.33, rank 10 → 0.10.
**Moving a result from position 2 to position 1 is worth as much as moving one from position 10 to
position 5.**

### Advantages

- **Cheap labelling.** You only need to identify the *first* relevant document — often you can stop
  judging as soon as you find it.
- **Matches known-item and factoid search exactly.** If there is one right answer, MRR is not a
  simplification; it is the correct measurement.
- **Highly interpretable.** MRR 0.5 means "on average, the first good result is around position 2."
- **Very sensitive at the top**, which is where interface real estate actually is.

### Disadvantages

- **Discards everything after the first hit.** Recall is invisible. A system finding one of twenty
  relevant documents ties a system finding all twenty.
- **Unstable on single queries.** RR takes only the values 1, ½, ⅓, ¼… — there is no value between
  0.5 and 1.0. Small rank changes cause large jumps, and MRR over few queries is noisy.
- **Wrong model for exploratory or aggregative tasks.** A user writing a literature review does not
  stop at the first paper.
- **Zero for a query with no hits gives no partial credit** — a system that ranked the answer at 101
  scores identically to one that missed entirely at any depth.

### Domain examples

**Question answering / factoid retrieval.** MRR's home. "What year did X happen?" has one answer;
the position of that answer is the whole story.

**RAG chunk retrieval where one chunk suffices.** If your questions are typically answerable from a
single chunk, MRR on the gold chunk is an excellent cheap proxy — and it pairs naturally with
RAG-X's Exclusive Hit Rate (Supplement B §D.4), which tells you whether single-chunk sufficiency
actually holds in your corpus.

**Legal or medical research.** Poor fit as a primary metric. These are recall-driven aggregative
tasks; MRR will look excellent on a system that misses most of the relevant material.

### Recommendation

Use MRR when your task genuinely has **one** right answer, and say so explicitly when you report it.
The most common misuse is reporting MRR on an aggregative task because it looks good.

Report the number of queries alongside — MRR's discreteness makes it noisy, and MRR over 30 queries
should not be compared to three decimal places.

### Failure mode

```
   THE MRR CEILING

   System A: finds gold chunk at rank 1. Misses the
             other 6 relevant chunks entirely.
   System B: finds gold chunk at rank 1. Also finds
             all 6 others in the top 10.

   MRR:  A = 1.00     B = 1.00

        o    "Identical performance."
       /|\
       / \

        o    "For a single-answer task, genuinely yes.
       /|\     For anything else, you just declared a
       / \     6× recall difference invisible."
```

---

## 5.2 MAP — Mean Average Precision

**One-line:** For each query, average the precision measured at every position where a relevant
document appears; then average over queries.

**Formula:**
```
   AP  = (1/R) · Σ_{k=1}^{n} P@k · rel(k)

     where  R      = total number of relevant documents
            rel(k) = 1 if the document at rank k is relevant, else 0
            P@k    = precision at cutoff k

   MAP = mean of AP over all queries
```

**Facets:** Correctness | query | ref | R | ⬤ ✅ *(Manning Ch. 8)*

### The idea

MAP's user model: **the user is spread evenly across all relevant documents** — equally likely to
be looking for any one of them, and stopping when they find the one they want. That interpretation
is Robertson's, and it is worth knowing because it is the assumption most often violated.

Mechanically, AP rewards putting relevant documents early by computing precision *only at relevant
positions* — so each relevant document is scored by how clean the list was up to the point it
appeared.

### Diagram

```
   AP MEASURES PRECISION AT EACH HIT
   ═════════════════════════════════

   rank  doc   rel?   P@k at hits
   ────  ───   ────   ───────────
    1     A     ✓     1/1 = 1.000  ●
    2     B     ✗
    3     C     ✓     2/3 = 0.667  ●
    4     D     ✗
    5     E     ✓     3/5 = 0.600  ●
    6     F     ✗
    ...
   (R = 4 relevant documents exist; one never retrieved)

   AP = (1.000 + 0.667 + 0.600 + 0) / 4 = 0.567
                                     ▲
                                     └── the unretrieved
                                         relevant doc
                                         contributes ZERO

        o    "So AP punishes missing documents?"
       /|\
       / \

        o    "Yes — the divisor is R, not the number
       /|\     you found. That's how recall gets into
       / \     a precision-flavoured metric."
```

That divisor is the key design decision. **AP is a precision measure with a recall denominator**,
which is why it behaves like a balanced metric despite its name.

### Worked example

Two systems, same 4 relevant documents:

```
   SYSTEM A: relevant at ranks 1, 2, 3, 4
     AP = (1/1 + 2/2 + 3/3 + 4/4)/4 = (1+1+1+1)/4 = 1.000

   SYSTEM B: relevant at ranks 1, 5, 9, 13
     AP = (1/1 + 2/5 + 3/9 + 4/13)/4
        = (1.000 + 0.400 + 0.333 + 0.308)/4 = 0.510

   Same recall (4/4). Half the AP.
```

### Advantages

- **Single number that reflects both precision and recall, across the full ranking.** This is why
  MAP dominated TREC-era evaluation.
- **Stable and well-behaved.** More discriminative than MRR; less noisy across query sets.
- **Rewards early relevance without a hand-picked cutoff.** No arbitrary K.
- **Deeply studied.** Decades of literature on its statistical properties.

### Disadvantages

- **Requires knowing R, the total relevant count.** Zobel, Moffat and Park's critique targets
  exactly this: AP relies on the total number of *known* relevant documents, and so does nDCG, since
  the ideal list also requires them. With incomplete judgments, R is wrong and AP is biased. This is
  Chapter 6's whole subject.
- **Binary relevance only.** No graded judgments.
- **The uniform-user assumption is usually false.** Real users are not equally interested in every
  relevant document.
- **Averaging APs across queries with very different R conflates easy and hard queries.** A query
  with R=1 and a query with R=200 contribute equally to MAP.
- **Hard to explain to stakeholders.** "Mean of the average of precisions at relevant positions" is
  not a sentence that survives a steering committee.

### Domain examples

**Academic benchmarking on curated collections.** MAP's natural home — TREC-style collections have
reasonably complete judgments, so R is trustworthy.

**Patent and legal search.** Attractive because it balances precision and recall, but **use with
care**: R is precisely the quantity you do not know in a large corpus. Consider bpref or infAP
(Chapter 6) instead.

**Production web or e-commerce search.** Generally the wrong choice. R is unknowable, judgments are
sparse, and users never see beyond rank 10. Use nDCG@k or RBP.

### Recommendation

Use MAP when your judgments are **reasonably complete** — that is, on a curated evaluation
collection. On sparse or pooled judgments, MAP's headline stability is an illusion produced by a
denominator you guessed.

If you report MAP, report the mean and distribution of R across your query set. A MAP computed over
queries where R ranges from 1 to 200 is a weighted average whose weights nobody has examined.

---

## 5.3 DCG and nDCG

**One-line:** Sum the graded relevance of each result, discounted logarithmically by position, then
normalize by the best possible ordering.

**Formula:**
```
   DCG@k  = Σ_{i=1}^{k}  rel_i / log₂(i + 1)

   (a common alternative, "exponential gain":
    DCG@k = Σ (2^{rel_i} − 1) / log₂(i + 1) )

   IDCG@k = DCG@k of the ideal (perfectly sorted) ranking

   nDCG@k = DCG@k / IDCG@k        ∈ [0, 1]
```

**Facets:** Correctness | query | ref | R | ⬤ ✅
**Source:** Järvelin & Kekäläinen, *Cumulated Gain-Based Evaluation of IR Techniques*,
**ACM TOIS 20(4):422–446, 2002**

### The idea

Two contributions, and they are separable:

1. **Graded relevance.** Documents are not relevant/irrelevant but scored 0–3 (or 0–4). This alone
   is a major advance over everything in Chapter 4.
2. **Logarithmic discount.** `1/log₂(i+1)` — gentler than MRR's `1/i`, and chosen because it models
   a user whose attention declines but does not collapse.

Normalization by the ideal ranking is what makes nDCG comparable across queries with different
numbers of relevant documents.

### Diagram

```
   THE LOG DISCOUNT IS GENTLE
   ══════════════════════════

   rank   1/i (MRR-ish)   1/log₂(i+1) (DCG)
   ────   ─────────────   ─────────────────
    1        1.000            1.000
    2        0.500            0.631
    3        0.333            0.500
    5        0.200            0.387
   10        0.100            0.289
   20        0.050            0.228

        1.0 ┤●
            │ ○●              ○ = 1/log₂(i+1)
            │  ○ ●            ● = 1/i
        0.5 ┤   ○  ●
            │     ○   ●●
            │        ○○○ ●●●●●
        0.0 ┤            ○○○○○○
            └──────────────────────
              1  3  5  7  9  11  13

        o    "Why logarithmic specifically?"
       /|\
       / \

        o    "It's a modelling choice, not a derivation.
       /|\     Järvelin and Kekäläinen wanted a discount
       / \     that penalized depth without making rank 10
              worthless. Log does that. Other shapes
              would too — RBP picks a different one."
```

### Worked example

Graded relevance 0–3, k = 5:

```
   rank  rel   1/log₂(i+1)   contribution
   ────  ───   ───────────   ────────────
    1     3      1.000          3.000
    2     0      0.631          0.000
    3     2      0.500          1.000
    4     1      0.431          0.431
    5     3      0.387          1.161
                              ────────
                       DCG@5 =  5.592

   IDEAL ordering (3,3,2,1,0):
    1     3      1.000          3.000
    2     3      0.631          1.893
    3     2      0.500          1.000
    4     1      0.431          0.431
    5     0      0.387          0.000
                              ────────
                      IDCG@5 =  6.324

   nDCG@5 = 5.592 / 6.324 = 0.884
```

### Advantages

- **Handles graded relevance**, the only metric so far that does. Real relevance is not binary.
- **Bounded [0,1] and comparable across queries** thanks to normalization.
- **Tunable via the gain function.** Linear gain treats a 3 as three times a 1; exponential gain
  (`2^rel − 1`) treats it as seven times. That is a real modelling lever.
- **The industry default**, so external comparison is possible.
- **Works at any cutoff.**

### Disadvantages

- **IDCG requires knowing all relevant documents** — the same critique Zobel, Moffat and Park level
  at AP applies here: the ideal list requires all known relevant documents. With incomplete
  judgments, your denominator is wrong.
- **Two gain functions in circulation** and papers often do not say which. nDCG numbers are
  frequently not comparable across papers for this reason alone.
- **The log discount is an assumption, not a finding.** It is a reasonable model of human scanning
  and a *poor* model of an LLM consuming a prompt — the point UDCG makes directly.
- **Insensitive to the tail.** nDCG@10 says nothing about rank 11+.
- **Normalization can mask absolute quality.** nDCG 0.9 on a query where the best possible result is
  mediocre still reads 0.9.

### Domain examples

**Web and e-commerce search.** The default for good reason: graded relevance matches reality (a
perfect match, a decent match, a related item), and the log discount roughly matches scanning
behaviour.

**Enterprise search with expert users.** Works well, and here deeper cutoffs (nDCG@20) are
legitimate.

**RAG chunk ranking.** ⚠️ **This is where nDCG quietly stops working.** The log discount models
sequential human attention. An LLM processes the whole prompt at once, and — per *The Power of
Noise* and GainRAG — a tangentially relevant chunk can actively *harm* the answer, which nDCG scores
as a zero rather than a negative. If you report nDCG on RAG retrieval, put a distraction-sensitive
metric next to it (Supplement A §A.4).

### Recommendation

Use nDCG@k as your **primary classical ranking metric**, with k matched to your interface, and
**always state your gain function and your k**. "nDCG = 0.71" without those two facts is not a
reproducible claim.

For RAG, keep nDCG for continuity and comparability, but do not treat it as your decision metric.
Its user model is wrong for your consumer.

---

## 5.4 ERR — Expected Reciprocal Rank

**One-line:** MRR generalized to graded relevance, with the user stopping probabilistically once
satisfied.

**Formula:**
```
   ERR = Σ_{r=1}^{n}  (1/r) · R_r · Π_{i=1}^{r-1} (1 − R_i)

     where  R_i = (2^{g_i} − 1) / 2^{g_max}
            g_i = graded relevance of document at rank i

   R_i is the probability the user is satisfied by document i.
   The product term is the probability they were NOT satisfied earlier.
```

**Facets:** Correctness | query | ref | R | ⬤ ✅
**Source:** Chapelle, Metzler, Zhang & Grinspan, **CIKM 2009, pp. 621–630**,
doi 10.1145/1645953.1646033

### The idea

ERR is a **cascade model**. The user scans down the list; at each document there is a probability
they are satisfied and stop, determined by that document's grade. The metric is the expected
reciprocal rank of the stopping position.

The crucial property this buys: **a relevant document at rank 5 is worth less if there were already
relevant documents at ranks 1–4**, because the user probably never reached it. No metric before ERR
had this.

### Diagram

```
   THE CASCADE — DIMINISHING CREDIT
   ════════════════════════════════

   Case 1: relevant at rank 5, NOTHING above it
     ┌───────────────────────┐
     │ 1 ✗  ↓                │
     │ 2 ✗  ↓  user keeps    │  user very likely
     │ 3 ✗  ↓  scanning      │  REACHES rank 5
     │ 4 ✗  ↓                │
     │ 5 ✓  STOP             │  → rank 5 gets
     └───────────────────────┘    substantial credit

   Case 2: relevant at rank 5, ALSO relevant at rank 1
     ┌───────────────────────┐
     │ 1 ✓  STOP  ────────╮  │  user probably
     │ 2 ✗                │  │  NEVER REACHES 5
     │ 3 ✗                │  │
     │ 4 ✗                │  │  → rank 5 gets
     │ 5 ✓  (unseen) ◀────╯  │    almost no credit
     └───────────────────────┘

        o    "nDCG gives rank 5 the same discount
       /|\     in both cases."
       / \

        o    "Right. ERR doesn't. That's the whole
       /|\     contribution."
       / \
```

### Advantages

- **The most realistic user model** of any metric in this chapter for navigational and informational
  web search — Sakai, reviewing the field, singles out ERR as particularly useful.
- **Handles graded relevance.**
- **Correctly discounts redundancy.** If the answer appears three times, ERR credits roughly one of
  them. This is a genuine and rare property.
- **Bounded and comparable.**

### Disadvantages

- **The satisfaction model is parametric and fixed.** `R_i = (2^g − 1)/2^g_max` is a choice; it is
  not derived from your users' behaviour.
- **Assumes the user stops when satisfied**, which is wrong for aggregative tasks — the same failure
  mode as MRR, inherited.
- **Less widely reported than nDCG**, so external comparison is harder.
- **Harder to explain.** The product term is not intuitive.

### Domain examples

**Web search with navigational intent.** ERR's design target and its best fit.

**E-commerce.** Strong fit — a shopper who finds a suitable product does stop.

**RAG chunk retrieval.** ⚠️ Structurally wrong, and interestingly so. ERR assumes the reader stops
early. An LLM reads **every** chunk in the prompt. ERR's core innovation — discounting deep
positions because they are probably unseen — is precisely backwards for a consumer that sees
everything. Note however that ERR's *redundancy* discount is exactly right for RAG, which is why
RAG-X's Pairwise Redundancy exists as a separate measure.

### Recommendation

Use ERR for human-facing search where users satisfice. **Do not use it for RAG retrieval** — its
positional assumption is inverted for LLM consumers, even though its redundancy handling is
desirable.

If you want ERR's redundancy property in a RAG context, take Pairwise Redundancy and Exclusive Hit
Rate instead (Supplement B §D.4).

---

## 5.5 RBP — Rank-Biased Precision

**One-line:** A geometric-discount precision measure with an explicit **residual** quantifying how
much the score could change if unjudged documents were judged.

**Formula:**
```
   RBP = (1 − p) · Σ_{d=1}^{∞}  r_d · p^{d−1}

     where  r_d ∈ {0,1} is the relevance at rank d
            p  ∈ [0,1)  is user PERSISTENCE
                        (probability of continuing to rank d+1)

   p = 0.5  → impatient user, top-heavy
   p = 0.8  → moderate
   p = 0.95 → very persistent, near-uniform over depth
```

**Facets:** Correctness | query | ref | R | ⬤ ✅
**Source:** Moffat & Zobel, *Rank-Biased Precision for Measurement of Retrieval Effectiveness*,
**ACM TOIS 27(1), Article 2, 2008 (27 pages)**, doi 10.1145/1416950.1416952

### The idea

Two things make RBP distinctive, and the second is why it appears in this white paper at all.

**1. Persistence is an explicit parameter.** Rather than baking a discount shape in, RBP asks you to
state your user model as a number. `p` is the probability the user continues to the next rank. That
is an auditable assumption rather than a hidden one.

**2. It has a residual — and this is the important part.** Because the sum runs to infinity but your
judgments do not, RBP naturally produces a *range*: a lower bound (assume all unjudged documents are
irrelevant) and an upper bound (assume all are relevant). The gap is the **residual**, and it tells
you how much your evaluation is being driven by ignorance.

### Diagram

```
   THE RESIDUAL — A METRIC THAT ADMITS UNCERTAINTY
   ═══════════════════════════════════════════════

   ┌──────────────────────────────────────────────┐
   │  RBP = 0.42  [+0.05]     ← small residual    │
   │                             judgments are    │
   │  ├────────┤                 adequate         │
   │  0.42  0.47                                  │
   └──────────────────────────────────────────────┘

   ┌──────────────────────────────────────────────┐
   │  RBP = 0.42  [+0.31]     ← HUGE residual     │
   │                             your judgments   │
   │  ├────────────────────┤     cannot support   │
   │  0.42              0.73     this comparison  │
   └──────────────────────────────────────────────┘

        o    "Both systems scored 0.42."
       /|\
       / \

        o    "One of them might actually be 0.73.
       /|\     You need more judgments before you
       / \     can claim anything."

   NO OTHER METRIC IN THIS CHAPTER TELLS YOU THIS.
   nDCG and MAP report a point estimate and stay silent
   about how much of the ranking was never judged.
```

### Worked example

```
   p = 0.8,  so (1−p) = 0.2

   rank  rel   p^(d−1)   contribution
   ────  ───   ───────   ────────────
    1     1     1.000      0.2000
    2     0     0.800      0.0000
    3     1     0.640      0.1280
    4     ?     0.512        ——      ← UNJUDGED
    5     1     0.410      0.0819
                          ────────
              RBP (lower) = 0.4099

   Residual from rank 4 alone: 0.2 × 0.512 = 0.1024
   Plus all unjudged ranks beyond 5.

   Report: RBP = 0.41 [+0.10]
```

### Advantages

- **The residual is a genuine methodological advance.** It converts "we have incomplete judgments"
  from an unstated caveat into a reported number.
- **No need to know R.** Unlike AP and nDCG, RBP requires no total-relevant count — which is exactly
  the property Zobel, Moffat & Park argue for when they reject AP and nDCG in favour of RBP.
- **Persistence is explicit and auditable.** You state your user model rather than inheriting one.
- **Well-behaved under pooling.** Designed for incomplete judgments from the start.
- **Bridges directly into Chapter 6** — RBP is the rank metric that takes incompleteness seriously.

### Disadvantages

- **`p` must be chosen, and results move with it.** RBP at p=0.5 and RBP at p=0.95 are different
  metrics. Unreported `p` makes a number meaningless.
- **Binary relevance** in its base form (graded extensions exist).
- **Less familiar than nDCG.** You will spend meeting time explaining it.
- **The residual can be uncomfortably large**, which is a feature that reads as a bug to
  stakeholders who wanted one number.

### Domain examples

**Any evaluation with pooled or sparse judgments.** This is RBP's argument for existing, and it
covers most real production evaluation.

**Legal / patent search.** Judgments are always incomplete at scale. The residual tells you whether
your comparison is supportable — which in a discovery dispute is a defensible position rather than
an embarrassment.

**RAG retrieval evaluation.** Underused and well-suited. RAG judgments are almost always sparse
(you labelled the gold chunk and nothing else), so a point-estimate nDCG is overconfident.
**RBP's residual is arguably the most honest classical metric for RAG retrieval.**

### Recommendation

**Adopt RBP alongside nDCG, specifically for the residual.** Report `RBP@p=0.8 = 0.41 [+0.10]`. The
bracketed number will do more to improve your evaluation hygiene than any other single change in
this chapter, because it makes the cost of sparse judgments visible on the dashboard rather than in
a footnote nobody reads.

Set `p` from your observed user behaviour if you have it (mean scroll depth is a reasonable proxy),
and hold it fixed thereafter.

### Failure mode

```
   THE UNREPORTED PERSISTENCE

   Paper A: "RBP = 0.62"   (p = 0.95, not stated)
   Paper B: "RBP = 0.41"   (p = 0.50, not stated)

        o    "System A is much better."
       /|\
       / \

        o    "System A was measured with a user who
       /|\     reads 20 results. System B's user reads 2.
       / \     You compared two different questions."
```

---

## 5.6 Chapter 5 summary — which discount, and when

```
┌─────────────────────────────────────────────────────────────────┐
│  METRIC   USER MODEL                        USE WHEN            │
├─────────────────────────────────────────────────────────────────┤
│  MRR      stops at first hit, never         one right answer    │
│           returns                           exists             │
├─────────────────────────────────────────────────────────────────┤
│  MAP      equally interested in every       judgments are       │
│           relevant doc                      complete           │
├─────────────────────────────────────────────────────────────────┤
│  nDCG     attention declines logarith-      default for human   │
│           mically; relevance is graded      search              │
├─────────────────────────────────────────────────────────────────┤
│  ERR      satisfices; stops probabil-       navigational web /  │
│           istically; redundancy is waste    e-commerce          │
├─────────────────────────────────────────────────────────────────┤
│  RBP      continues with probability p;     judgments are       │
│           REPORTS ITS OWN UNCERTAINTY       SPARSE (i.e. most   │
│                                             real evaluations)   │
└─────────────────────────────────────────────────────────────────┘

   ⚠️ FOR RAG, ALL FIVE ENCODE THE WRONG READER.
   Every discount above models a human scanning sequentially.
   An LLM reads the whole prompt. See UDCG (Supplement A §A.4.1)
   and keep a distraction-sensitive metric alongside whichever
   of these you report.
```

---

# Chapter 6 — When You Do Not Know What Is Relevant

## 6.0 The problem Chapter 5 kept deferring

MAP needs R. nDCG needs the ideal ranking. Both require knowing **every** relevant document in the
corpus. In a collection of any size, nobody does.

The standard workaround is **pooling**: run several systems, take the top *d* results from each,
judge only that pool. Everything outside the pool is treated as irrelevant.

```
   POOLING, AND WHAT IT ASSUMES
   ════════════════════════════

   system A top-100 ─┐
   system B top-100 ─┼──▶ POOL ──▶ humans judge these
   system C top-100 ─┘              (say 4,000 docs)

   Corpus: 10,000,000 documents
   Judged:      4,000 documents
   Assumed irrelevant: 9,996,000

        o    "That's a big assumption."
       /|\
       / \

        o    "It's usually a fine one — most documents
       /|\     really are irrelevant. The problem is the
       / \     relevant ones that no pooled system found.
              They're invisible, and they're not random."
```

The bias is systematic: a *new* system that finds relevant documents no pooled system found gets **no
credit** for them. Pooling structurally favours systems similar to those that built the pool. Zobel
raised this in 1998 and it has never gone away.

## 6.1 bpref

**One-line:** Rank documents by how many *judged irrelevant* documents outrank each *judged
relevant* one — ignoring unjudged documents entirely.

**Formula:**
```
   bpref = (1/R) · Σ_{r}  ( 1 − |n ranked higher than r| / R )

     where  r = a judged-relevant document
            n = judged-IRRELEVANT documents ranked above r
                (counted only up to the first R of them)
            R = number of judged relevant documents

   Unjudged documents are SKIPPED, not counted as irrelevant.
```

**Facets:** Correctness | query | ref | R | ⬤ ✅
**Source:** Buckley & Voorhees, *Retrieval Evaluation with Incomplete Information*,
**SIGIR 2004, pp. 25–32**

### The idea

The insight is almost embarrassingly simple: **if you do not know whether a document is relevant,
do not pretend it is irrelevant. Skip it.**

MAP treats unjudged documents as irrelevant, which penalizes a system for retrieving something
nobody looked at. bpref only compares judged-relevant against judged-irrelevant, and asks: how often
did a known-bad document beat a known-good one?

### Diagram

```
   WHAT MAP SEES vs WHAT bpref SEES
   ════════════════════════════════

   rank  doc  judgment
   ────  ───  ────────
    1     A   ✓ relevant
    2     B   ? UNJUDGED
    3     C   ✗ irrelevant
    4     D   ✓ relevant
    5     E   ? UNJUDGED
    6     F   ✓ relevant

   MAP's view:              bpref's view:
   ┌──────────────┐         ┌──────────────┐
   │ 1 ✓          │         │ 1 ✓          │
   │ 2 ✗ (assumed)│         │ 2 (skipped)  │
   │ 3 ✗          │         │ 3 ✗          │
   │ 4 ✓          │         │ 4 ✓          │
   │ 5 ✗ (assumed)│         │ 5 (skipped)  │
   │ 6 ✓          │         │ 6 ✓          │
   └──────────────┘         └──────────────┘
   penalizes B and E        stays silent on B and E

        o    "But B might have been relevant!"
       /|\
       / \

        o    "Exactly. bpref refuses to guess.
       /|\     MAP guesses 'irrelevant' every time."
       / \
```

### Advantages

- **Robust to incomplete judgments** — its entire purpose, and it delivers: bpref system rankings
  degrade far more gracefully than MAP's as judgments are thinned.
- **No assumption about unjudged documents.**
- **Widely available** in `trec_eval` and standard tooling.
- **Good for evaluating novel systems** against old pools, where the new system retrieves unjudged
  material.

### Disadvantages

- **Still needs R**, the count of judged-relevant documents — so it is robust to *missing* judgments
  but not to a *biased* pool.
- **Less top-heavy than nDCG or RBP.** bpref weights all relevant documents roughly equally, so it
  under-rewards putting the best result first.
- **Harder to interpret.** "One minus the fraction of irrelevant documents ranked above" is not an
  intuitive quantity.
- **Correlates imperfectly with user-facing quality** because of the flat weighting.

### Domain examples

**Evaluating a new retriever against an old test collection.** The canonical use. If your new dense
retriever surfaces documents the BM25-era pool never saw, MAP will punish you for it and bpref will
not.

**RAG with gold-chunk-only labels.** Extremely relevant and almost never used. If you labelled one
gold chunk per question and nothing else, then *every other retrieved chunk is unjudged* — and MAP,
nDCG, and precision are all silently treating them as irrelevant. bpref is the honest choice here.

**Consumer search with click-derived labels.** Clicks give you sparse positive evidence and almost
no reliable negatives. bpref's asymmetry fits.

### Recommendation

**Use bpref whenever your judgments came from a pool you did not build, or from labels covering a
small fraction of what you retrieve.** Report it *alongside* MAP, not instead: the **gap between MAP
and bpref is a direct estimate of how much your judgments are distorting your evaluation.**

That comparison is cheap — both come out of the same tooling — and it is one of the highest-value
diagnostics in this volume.

---

## 6.2 infAP

**One-line:** Average precision estimated statistically from a random sample of judgments, with
confidence properties.

**Facets:** Correctness | query | ref | R | ⬤ ✅
**Source:** Yilmaz & Aslam, *Estimating Average Precision with Incomplete and Imperfect Judgments*,
**CIKM 2006, Arlington VA, pp. 102–111**. Extended: *Estimating average precision when judgments are
incomplete*, **Knowledge and Information Systems 16(2):173–211, 2008**

### The idea

Where bpref changes the *definition* to cope with missing judgments, infAP keeps AP's definition and
changes the *estimation*. If your judged documents are a **random sample** of the pool, AP can be
estimated with known statistical properties — an unbiased estimate rather than a redefinition.

### Diagram

```
   TWO STRATEGIES FOR ONE PROBLEM
   ══════════════════════════════

   bpref:  "Change the metric so missing
            judgments don't matter."
            ┌──────────────────────┐
            │ skip the unknowns    │
            └──────────────────────┘

   infAP:  "Keep the metric. Sample properly.
            ESTIMATE the true value."
            ┌──────────────────────┐
            │ random sample ──▶ AP̂ │
            │        + confidence  │
            └──────────────────────┘

        o    "Which is better?"
       /|\
       / \

        o    "Depends on whether you CONTROLLED the
       /|\     sampling. infAP needs a random sample.
       / \     bpref works on whatever pool you
              inherited."
```

That distinction is the practical decision rule and it is usually decided for you: if you are
evaluating on someone else's collection, you did not control sampling, so bpref. If you are building
your own judgment set from scratch, sample randomly and use infAP.

### Advantages

- **Statistically principled** — an estimator with confidence properties, not a heuristic.
- **Comparable to AP**, since it estimates the same quantity. No reinterpretation needed.
- **Efficient use of annotation budget.** You can decide how many judgments to buy and know what
  precision you get.

### Disadvantages

- **Requires random sampling of the judgment pool.** If your labels came from clicks, from a pool, or
  from "whatever the annotators got through," infAP's assumptions are violated.
- **More complex to implement** than bpref.
- **Still an estimate**, with variance that must be reported to be meaningful.
- **Does not fix pool bias.** If relevant documents exist that no system retrieved, no amount of
  sampling within the pool will find them.

### Recommendation

If you are **building** an evaluation set, sample randomly and use infAP with confidence intervals.
If you **inherited** one, use bpref. Do not use infAP on a non-random judgment set and report it as
though the estimator's properties hold — they do not.

---

## 6.3 Pool bias and assessor agreement

Two things that are not metrics but without which the metrics above are decoration.

### 6.3.1 Pooling depth bias

**Source:** Zobel, *How Reliable Are the Results of Large-Scale Information Retrieval Experiments?*,
**SIGIR 1998, pp. 307–314** ✅. See also Webber, Moffat & Zobel, *The Effect of Pooling and
Evaluation Depth on Metric Stability*, **EVIA 2010, pp. 7–15** ✅.

```
   THE BIAS THAT CANNOT BE SAMPLED AWAY
   ════════════════════════════════════

   ┌────────────────────────────────────────┐
   │  CORPUS                                │
   │                                        │
   │   ┌──────────────┐                     │
   │   │  THE POOL    │      ● ●   ●        │
   │   │  ✓ ✓ ✗ ✓ ✗   │    ●    ●     ●     │
   │   │  ✗ ✓ ✗ ✗ ✓   │       ●   ●         │
   │   └──────────────┘                     │
   │                     ▲                  │
   │                     └── relevant docs   │
   │                         NO pooled system│
   │                         retrieved       │
   └────────────────────────────────────────┘

   bpref: cannot see them
   infAP: cannot see them
   Nothing inside the pool can see them.

        o    "So how do we know they exist?"
       /|\
       / \

        o    "You don't. That's the point. You can only
       /|\     bound the problem — by pooling more
       / \     systems, or by reporting RBP's residual."
```

### 6.3.2 Assessor agreement

Human relevance judgments disagree, and the disagreement is substantial — Voorhees' work on
variations in relevance judgments established that system *rankings* are surprisingly stable under
assessor disagreement even though absolute scores are not.

**Practical consequence:** trust your *relative* comparisons more than your absolute numbers. A
system that scores nDCG 0.71 versus another's 0.68 on the same judgments is a meaningful comparison.
"Our nDCG is 0.71" as a standalone quality claim is much weaker than it looks.

Report Cohen's κ for two assessors, **Krippendorff's α for more than two** — a point that returns in
Volume II when the assessors are LLM judges.

---

## 6.4 Chapter 6 summary

```
┌───────────────────────────────────────────────────────────────┐
│  YOU DO NOT KNOW WHAT IS RELEVANT. NOW WHAT?                  │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  INHERITED a judgment pool     ──▶  bpref                     │
│                                     (+ report MAP−bpref gap)  │
│                                                               │
│  BUILDING a judgment set       ──▶  random sample + infAP     │
│                                     with confidence intervals │
│                                                               │
│  WANT UNCERTAINTY ON THE FACE                                 │
│  OF THE METRIC                 ──▶  RBP with residual (§5.5)  │
│                                                               │
│  SPARSE RAG LABELS             ──▶  bpref, and stop reporting │
│  (gold chunk only)                  precision as though       │
│                                     unjudged = irrelevant     │
├───────────────────────────────────────────────────────────────┤
│  THE DIAGNOSTIC WORTH RUNNING TODAY                           │
│  Compute MAP and bpref on the same runs. The gap between      │
│  them estimates how much your incomplete judgments are        │
│  distorting your conclusions. It costs one command.           │
└───────────────────────────────────────────────────────────────┘
```

---

# Chapter 7 — Comparing Two Rankings

## 7.0 A different question

Chapters 4–6 asked *is this ranking good?* Chapter 7 asks *are these two rankings the same?* — which
requires no relevance judgments at all.

That property is why this chapter is the bridge to drift measurement. You cannot ask "is my
retrieval still good?" without labels. You *can* ask "is my retrieval still doing what it did in
January?" with nothing but two result lists.

```
   THE PIVOT
   ═════════

   "IS IT GOOD?"              "IS IT THE SAME?"
   needs labels               needs NO labels
   ──────────────             ─────────────────
   nDCG, MAP, RBP             Kendall τ, RBO
        │                          │
        │                          │
   quality metric             DRIFT metric
```

## 7.1 Kendall's τ and Spearman's ρ

**One-line:** Classical rank-correlation coefficients measuring how similarly two rankings order the
same items.

**Formula (Kendall's τ):**
```
   τ = (concordant pairs − discordant pairs) / total pairs

   τ = 1   identical ordering
   τ = 0   independent
   τ = −1  reversed
```

**Facets:** Integrity/Drift | query | free | R | ⬤ ✅ *(standard statistics)*

### Advantages

- **Simple, well-understood, universally implemented.**
- **No labels required.**
- **Interpretable** as a probability of pairwise agreement.
- **Standard for meta-evaluation** — comparing how two *metrics* rank systems, which is how eRAG's
  headline result is expressed (τ improvements of 0.168–0.494).

### Disadvantages

- **Uniform weighting across ranks.** A swap between positions 1 and 2 counts the same as a swap
  between positions 999 and 1000. For retrieval this is badly wrong.
- **Requires conjoint lists** — both rankings must cover the same item set. Two retrievers over the
  same corpus with different top-10s do not satisfy this.
- **Undefined behaviour on truncated lists**, which is what you actually have.

```
        o    "τ = 0.94. Very stable."
       /|\
       / \

        o    "Where were the disagreements?"
       /|\
       / \

        o    "Ranks 1 and 2 swapped."
       /|\
       / \   "So the top result changed and your
              metric called it 94% stable. τ cannot
              see that ranks 1-2 matter more."
```

### Recommendation

Use τ for **meta-evaluation** — comparing metric rankings of systems, where uniform weighting is
appropriate because all systems matter equally. **Do not use it for retrieval drift**, where top
ranks dominate. Use RBO.

Note the specialized alternative: Yilmaz, Aslam & Robertson's AP-correlation
(**SIGIR 2008, pp. 587–594** ✅) is a top-weighted rank correlation built for IR precisely because τ
is not.

---

## 7.2 RBO — Rank-Biased Overlap

**One-line:** A top-weighted similarity measure for ranked lists that may be of different lengths and
may not share the same items.

**Formula:**
```
   RBO(S, T) = (1 − p) · Σ_{d=1}^{∞}  p^{d−1} · |S_{1:d} ∩ T_{1:d}| / d

     where  S_{1:d}  = top d items of list S
            |·∩·|/d  = AGREEMENT at depth d
            p        = persistence / patience
                       (larger p = more weight on deeper ranks)
```

**Facets:** Integrity/Drift | query | free | R | ⬤ ✅
**Source:** Webber, Moffat & Zobel, *A Similarity Measure for Indefinite Rankings*,
**ACM TOIS 28(4):20:1–20:38, 2010**

### The idea

RBO was built for what the authors call **indefinite rankings** — lists that are top-weighted,
possibly of different lengths, and **non-conjoint** (they need not contain the same items). That is
an exact description of two retrieval result lists.

Mechanically: compute the overlap at each depth, divide by the depth to get *agreement*, then take a
geometrically weighted average of agreement across all depths.

Note the family resemblance to RBP (§5.5) — same authors, same persistence parameter, same
geometric weighting. **RBO is RBP's idea applied to comparison instead of quality.**

### Diagram

```
   AGREEMENT AT EACH DEPTH
   ═══════════════════════

   List S (January)      List T (June)
   ┌──────────┐          ┌──────────┐
   │ 1. doc-A │          │ 1. doc-A │   depth 1: 1/1 = 1.00
   │ 2. doc-B │          │ 2. doc-C │   depth 2: 1/2 = 0.50
   │ 3. doc-C │          │ 3. doc-B │   depth 3: 3/3 = 1.00
   │ 4. doc-D │          │ 4. doc-E │   depth 4: 3/4 = 0.75
   │ 5. doc-E │          │ 5. doc-F │   depth 5: 4/5 = 0.80
   └──────────┘          └──────────┘

   RBO = geometric-weighted average of
         (1.00, 0.50, 1.00, 0.75, 0.80, ...)

   with p=0.9, shallow depths dominate.

   ┌────────────────────────────────────────────┐
   │  WHY THIS BEATS JACCARD FOR DRIFT          │
   │                                            │
   │  Jaccard:  |S∩T| / |S∪T|  at ONE depth     │
   │            order-blind, needs a fixed k    │
   │                                            │
   │  RBO:      every depth, weighted, and      │
   │            ORDER-SENSITIVE                 │
   │                                            │
   │  Two indexes returning the same 10 docs in │
   │  reversed order:                           │
   │     Jaccard = 1.00  ("no change!")         │
   │     RBO     ≈ 0.5   (correctly alarmed)    │
   └────────────────────────────────────────────┘
```

### Advantages

- **Top-weighted**, so it respects that rank 1 matters more than rank 50.
- **Handles non-conjoint lists** — the two lists need not contain the same documents. Essential when
  comparing two retrievers or two index versions.
- **Handles different lengths**, including comparing a short ideal list to a long actual one.
- **No labels required.** Pure comparison.
- **Has a residual**, like RBP — it can report bounds when lists are truncated.
- **Tunable persistence** via `p`, letting you match the depth your consumer actually reads.
- **Widely adopted outside IR** (search-engine comparison, ML, network analysis), so implementations
  are plentiful.

### Disadvantages

- **`p` must be chosen and reported.** Same discipline as RBP.
- **Comparative only.** RBO tells you two rankings differ; it never tells you which is better. A
  consistently terrible retriever scores RBO 1.0 against itself.
- **Infinite sum requires truncation** in practice, with an extrapolation assumption.
- **Less familiar than Jaccard**, so you will explain it.

### Domain examples

**Index drift monitoring.** The headline use, and the recommendation Supplement A made. Freeze 500
queries and their top-k; recompute monthly; report RBO against baseline. Falling RBO with no
deployment event means your corpus moved.

**Embedder migration.** ⚠️ Read the correction in the Supplement A Addendum first. Caspari et al.
found that at the small k RAG actually uses, different embedders retrieve **almost completely
distinct chunks** on larger datasets. So expect *low* RBO between two models — that is the normal
state, not the alarm. The comparison that matters is **the same model over time**, where RBO should
be near 1.0 absent a real change.

**A/B comparison of rerankers.** RBO between pre- and post-rerank lists quantifies how much work the
reranker is actually doing. Near 1.0 means you deployed a no-op.

### Recommendation

**RBO is the single most useful metric in this installment for RAG practitioners**, and it is almost
never used in the field.

Concretely:

```
   ┌────────────────────────────────────────────────────┐
   │  THE RBO DRIFT PROTOCOL                            │
   │                                                    │
   │  1. Freeze 500 representative queries              │
   │  2. Record top-k for each, today, with the         │
   │     embedder version and k stamped on it           │
   │  3. Monthly: recompute, report                     │
   │     RBO(today, baseline) at p matched to your k    │
   │  4. Alert on a sustained decline, not a single dip │
   │  5. Re-baseline deliberately after any intentional │
   │     change, and keep the old baseline              │
   │                                                    │
   │  Cost: one afternoon to set up, minutes per month. │
   │  This is the cheapest real drift metric available. │
   └────────────────────────────────────────────────────┘
```

### Failure mode

```
   THE SELF-SATISFIED BASELINE

   Jan:  RBO vs baseline = 1.00
   Mar:  RBO vs baseline = 1.00
   Jun:  RBO vs baseline = 1.00

        o    "Rock solid. No drift at all."
       /|\
       / \

        o    "Is the corpus still being updated?"
       /|\
       / \

        o    "...the ingestion job failed in February."
       /|\
       / \

   Perfect stability can mean 'healthy' or it can mean
   'nothing is happening'. RBO cannot distinguish them.
   Pair it with a corpus-freshness check.
```

---

## 7.3 Chapter 7 summary

```
┌────────────────────────────────────────────────────────────────┐
│  COMPARING RANKINGS                                            │
├────────────────────────────────────────────────────────────────┤
│  Kendall τ / Spearman ρ                                        │
│    ▸ uniform weighting, conjoint lists required                │
│    ▸ USE FOR: meta-evaluation (do two METRICS rank systems     │
│      the same way?)                                            │
│    ▸ NOT FOR: retrieval drift                                  │
│                                                                │
│  AP-correlation (Yilmaz, Aslam & Robertson, SIGIR'08)          │
│    ▸ top-weighted alternative to τ, built for IR               │
│                                                                │
│  RBO (Webber, Moffat & Zobel, TOIS'10)                         │
│    ▸ top-weighted, non-conjoint, variable-length, has a        │
│      residual, needs no labels                                 │
│    ▸ USE FOR: drift, embedder migration, reranker impact       │
│    ▸ the metric this white paper recommends most strongly      │
│      relative to how rarely it is used                         │
├────────────────────────────────────────────────────────────────┤
│  THE CONNECTING INSIGHT                                        │
│  RBP (§5.5) and RBO (§7.2) are the same idea — geometric        │
│  persistence weighting with an explicit residual — applied      │
│  once to QUALITY and once to COMPARISON. Same authors. If you   │
│  adopt one, adopt both; the mental model transfers for free.    │
└────────────────────────────────────────────────────────────────┘
```

---

# Appendix 2A — Citation verification ledger

All Installment 1 ⬜ entries now resolved:

| Metric | Citation | Was | Now |
|---|---|---|---|
| **ERR** | Chapelle, Metzler, Zhang & Grinspan, CIKM 2009, pp. 621–630, doi 10.1145/1645953.1646033 | ⬜ | ✅ |
| **RBP** | Moffat & Zobel, ACM TOIS 27(1), Article 2, 2008, 27pp, doi 10.1145/1416950.1416952 | ⬜ | ✅ |
| **RBO** | Webber, Moffat & Zobel, *A Similarity Measure for Indefinite Rankings*, ACM TOIS 28(4):20:1–20:38, 2010 | ⬜ | ✅ |
| **bpref** | Buckley & Voorhees, *Retrieval Evaluation with Incomplete Information*, SIGIR 2004, pp. 25–32 | ⬜ | ✅ |
| **infAP** | Yilmaz & Aslam, CIKM 2006, Arlington VA, pp. 102–111; extended in *Knowl. Inf. Syst.* 16(2):173–211, 2008 | ⬜ | ✅ |

**Additional citations verified while researching this installment:**

| Work | Citation | Status |
|---|---|---|
| nDCG origin | Järvelin & Kekäläinen, *Cumulated Gain-Based Evaluation of IR Techniques*, ACM TOIS 20(4):422–446, 2002 | ✅ |
| Pooling reliability | Zobel, SIGIR 1998, pp. 307–314 | ✅ |
| Pooling depth & stability | Webber, Moffat & Zobel, EVIA 2010, pp. 7–15 | ✅ |
| The case against AP/nDCG | Zobel, Moffat & Park, *Against Recall: Is It Persistence, Cardinality, Density, Coverage, or Totality?*, SIGIR Forum 43(1):3–15, 2009 | ✅ |
| Top-weighted rank correlation | Yilmaz, Aslam & Robertson, *A New Rank Correlation Coefficient for Information Retrieval*, SIGIR 2008, pp. 587–594 | ✅ |
| Progress illusion | Armstrong, Moffat, Webber & Zobel, *Improvements That Don't Add Up: Ad-hoc Retrieval Results Since 1998*, CIKM 2009, pp. 601–610 | ✅ — reserved for Chapter 11 |

**Zero unverified citations remain in this installment.**

---

# Appendix 2B — Running correction log

Unchanged from the Supplement A Addendum: nine corrections, two of them mine. No new corrections
arose in this installment — the classical literature verified cleanly, which is itself informative.
Older, more-cited work has had its citations checked by more people.

---

# Appendix 2C — Document set status

| # | Document | Covers | Status |
|---|---|---|---|
| 0 | `ir-rag-metrics-catalogue-v2.md` | Full index | Complete |
| 1 | `whitepaper-vol1-part1.md` | Ch 0–4 | Complete |
| 2 | `whitepaper-supplement-A.md` | Alignment, Integrity/Drift | Complete + addendum |
| 3 | `whitepaper-supplement-B.md` | Correctness, Efficiency | Complete |
| 4 | `whitepaper-supplement-A-addendum.md` | 🟡 lifts, CKA correction | Complete |
| 5 | **`whitepaper-vol1-part2.md`** | **Ch 5–7** | **this file** |

**Remaining:**

| Installment | Chapters | Contents | Notes |
|---|---|---|---|
| Vol I, 3 | 8–10 | Diversity & novelty (α-nDCG, ERR-IA, subtopic recall); fairness & exposure; online & counterfactual (interleaving, IPS) | Needs ~8 citations verified |
| Vol I, 4 | 11–12 | Significance & reporting; classical efficiency | Armstrong et al. already ✅ |
| Vol II, 8 | 22–24 | Meta-evaluation, judge reliability, deployment playbooks | Draws on Brehme survey, already read |
