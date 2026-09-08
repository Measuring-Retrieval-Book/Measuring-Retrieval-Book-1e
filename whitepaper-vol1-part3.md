# Measuring Retrieval

## Volume I — Foundations and Classical Information Retrieval
### Installment 3 of 4: Chapters 8–10
#### Diversity & Novelty · Fairness & Exposure · Online & Counterfactual Evaluation

---

**Citation status.** All citations in this installment were verified before writing, per the policy
in Volume I's header. Ledger in Appendix 3A. **Zero ⬜ entries.**

**Why these three chapters belong together.** Chapters 4–7 all assumed one thing: that the only
party whose interests matter is the person issuing the query, and that relevance to that person is
the only quantity worth measuring. These three chapters each break that assumption in a different
direction.

```
   WHO ELSE HAS A STAKE?
   ═════════════════════

   Ch 8  The query had MULTIPLE INTENTS.
         Serving one well may serve the others not at all.
              │
   Ch 9  The DOCUMENTS have interests too.
         Ranking allocates attention, and attention is
         economic opportunity.
              │
   Ch 10 The USERS already told you what they think.
         You have been ignoring it because you did not
         know how to read it.
```

---

# Chapter 8 — Diversity and Novelty

## 8.0 The assumption that breaks

Every metric so far treats documents as **independently relevant**. The relevance of document 3 does
not depend on what documents 1 and 2 said.

That assumption is false in two distinct ways, and the literature separates them carefully:

```
   TWO DIFFERENT PROBLEMS, OFTEN CONFLATED
   ═══════════════════════════════════════

   AMBIGUITY (query side)          REDUNDANCY (document side)
   ──────────────────────          ──────────────────────────
   "jaguar"                        Five documents all saying
     ├─ the animal                 the same thing about the
     ├─ the car                    same subtopic
     └─ the OS version
                                   ┌────────────┐
   Serving only "car" fails        │ doc A ████ │
   two thirds of your users        │ doc B ████ │ ← identical
                                   │ doc C ████ │   content
                                   └────────────┘

        o    "Both are 'diversity problems'."
       /|\
       / \

        o    "They need different metrics. Ambiguity is
       /|\     about COVERAGE of intents. Redundancy is
       / \     about MARGINAL value of each document."
```

The framing that unified them comes from Clarke et al., whose stated motivation was that **ambiguity
in queries and redundancy in retrieved documents are poorly reflected by current evaluation
measures** — and who then built a framework that systematically rewards novelty and diversity.

## 8.0.1 Why this chapter matters more for RAG than for search

In classical search, a redundant document costs the user a slot they can skip in half a second. In
RAG, a redundant chunk costs you **context budget you paid for and cannot reuse**.

RAG-X measured this directly: 22.0% pairwise redundancy between top contexts, with Exclusive Hit
Rate at rank 2 of only 6.8% (Supplement B §D.4). Their prescribed remedy — Maximum Marginal
Relevance for diversity, and diverse re-ranking — is the *algorithmic* side of what this chapter
measures.

**If you work on RAG and have skipped diversity metrics as an academic nicety, this is the chapter
that changes your mind.**

---

## 8.1 Subtopic Recall (S-recall)

**One-line:** What fraction of a query's distinct subtopics is covered by the top k results?

**Formula:**
```
   S-recall@k = |{ subtopics covered by the top k documents }| / |{ all subtopics }|
```

**Facets:** Correctness | query | ref | R | ⬤ ✅
**Source:** Zhai, Cohen & Lafferty, *Beyond Independent Relevance: Methods and Evaluation Metrics
for Subtopic Retrieval*, **SIGIR 2003, pp. 10–17**

### The idea

The founding paper of this chapter, and the title says it: *beyond independent relevance*. Zhai,
Cohen and Lafferty's move was to annotate queries with **subtopics** and then ask a coverage
question rather than a relevance question.

The same paper also proposed a companion measure sometimes written **S-RR**: the reciprocal of the
rank position at which *complete* coverage of all aspects is achieved.

### Diagram

```
   COVERAGE, NOT RELEVANCE
   ═══════════════════════

   Query: "jaguar"   Subtopics: {animal, car, OS}

   SYSTEM A (relevance-optimal)     SYSTEM B (diverse)
   ┌───────────────────────┐        ┌───────────────────────┐
   │ 1. car review    [car]│        │ 1. car review    [car]│
   │ 2. car pricing   [car]│        │ 2. jaguar habitat [an]│
   │ 3. car dealers   [car]│        │ 3. Mac OS 10.2   [OS] │
   └───────────────────────┘        └───────────────────────┘
     nDCG:      0.95                  nDCG:      0.78
     S-recall@3: 1/3 = 0.33            S-recall@3: 3/3 = 1.00

        o    "System A has better nDCG."
       /|\
       / \

        o    "System A failed two thirds of the people
       /|\     who typed that word. nDCG can't see that
       / \     because it averages over one assumed intent."
```

### Advantages

- **Conceptually simple** and easy to explain to stakeholders — "did we cover all the meanings?"
- **Directly measures the ambiguity failure** that relevance metrics are blind to.
- **Cheap to compute** once subtopics are annotated.
- **Complements rather than replaces** the Chapter 5 metrics.

### Disadvantages

- **Requires subtopic annotation**, which is expensive and subjective. Who decides that "jaguar" has
  three intents and not seven?
- **Ignores rank entirely.** Covering all subtopics at ranks 1–3 scores the same as covering them at
  ranks 98–100. This is what α-nDCG fixes.
- **Ignores relevance grade.** A marginally relevant document covering a subtopic counts as fully as
  an excellent one.
- **Binary coverage.** Partial coverage of a subtopic is not representable.

### Domain examples

**Ambiguous consumer search.** Its home. Short queries with multiple readings are the norm in web
and e-commerce search.

**RAG over heterogeneous corpora.** Underused and valuable. If a user asks "what is our refund
policy?" and your corpus contains regional variants, S-recall over regions tells you whether you
retrieved one region's policy or acknowledged that several exist.

**Multi-hop RAG.** ⚠️ Careful — this is a *different* problem that looks similar. Multi-hop needs
several passages that **jointly** support one answer; diversity needs passages covering **distinct**
answers. S-recall measures the second. Conflating them will lead you to optimize for spread when you
needed conjunction. SURE-RAG's set-sufficiency framing (Supplement B §C.9) is the multi-hop tool.

### Recommendation

Use S-recall as a **cheap first diversity diagnostic** when you suspect intent ambiguity. It is the
easiest metric in this chapter to instrument and it will tell you whether you have a problem worth
spending on α-nDCG for.

Do not use it as an optimization target — its rank-blindness means a system can game it by burying
diverse results deep.

---

## 8.2 α-nDCG

**One-line:** nDCG where a document's gain is discounted by how many previously-seen documents
already covered the same subtopic.

**Formula (sketch):**
```
   For each nugget/subtopic i, track how many times it has
   already been seen among the documents above rank k.

   gain(d_k) = Σ_i  rel(d_k, i) · (1 − α)^{count_i(k−1)}

   α-DCG@k = Σ_{k}  gain(d_k) / log₂(k + 1)

   α-nDCG@k = α-DCG@k / ideal α-DCG@k

   α ∈ [0,1]  is the novelty penalty.
   α = 0  → reduces to ordinary nDCG (no novelty reward)
   α = 0.5 → each repeat is worth half the previous
```

**Facets:** Correctness | query | ref | R | ⬤ ✅
**Source:** Clarke, Kolla, Cormack, Vechtomova, Ashkan, Büttcher & MacKinnon, *Novelty and Diversity
in Information Retrieval Evaluation*, **SIGIR 2008, pp. 659–666**, doi 10.1145/1390334.1390446

### The idea

α-nDCG merges Chapter 5's positional discount with a **second, orthogonal discount for redundancy**.
A document covering a fresh subtopic gets full gain; the fifth document covering the same subtopic
gets `(1−α)⁴` of it.

The authors' framing of *why* is worth carrying forward: **evaluation measures act as objective
functions to be optimized by retrieval systems**, so a measure that ignores redundancy will produce
systems that generate it. That argument applies with full force to RAG rerankers.

### Diagram

```
   TWO DISCOUNTS, MULTIPLIED
   ═════════════════════════

   POSITIONAL (from nDCG)      NOVELTY (new in α-nDCG)
   1/log₂(k+1)                 (1−α)^{times seen before}

   rank  subtopic  seen?  positional  novelty   gain
   ────  ────────  ─────  ──────────  ───────   ────
    1      A       0×       1.000      1.000    1.000
    2      A       1×       0.631      0.500    0.316   ← halved
    3      A       2×       0.500      0.250    0.125   ← quartered
    4      B       0×       0.431      1.000    0.431   ← FRESH,
                                                          beats rank 3
                                             (α = 0.5)

        o    "Rank 4 scores higher than rank 3?"
       /|\
       / \

        o    "Yes. It said something new. That inversion
       /|\     IS the metric — it's what makes diversity
       / \     worth optimizing."
```

### Advantages

- **The canonical diversity metric.** Widely implemented and understood; used in TREC Web track
  diversity tasks.
- **Combines relevance, position, and novelty** in one number without discarding any.
- **α is an explicit, auditable knob** — how much do you punish redundancy?
- **Backwards compatible.** At α = 0 it *is* nDCG, so adoption is incremental.

### Disadvantages

- **Requires nugget/subtopic-level judgments** — significantly more annotation than binary or graded
  relevance. Each document must be labelled for *which* subtopics it covers.
- **The ideal ranking is expensive to compute** and is NP-hard in general; implementations use greedy
  approximations, which means "α-nDCG" can differ between toolkits.
- **α must be reported.** Same discipline as RBP's `p` and RBO's `p`.
- **Assumes subtopics are independent and equally important.** ERR-IA relaxes the second.

### Domain examples

**Web search over ambiguous queries.** The design target.

**News and media recommendation.** Redundancy is the dominant failure mode — ten outlets covering
one story. α-nDCG is the right measure and is rarely used.

**RAG context assembly.** ⚠️ **The strongest under-exploited fit in this white paper.** Your chunks
carry overlapping content; your context budget is finite; RAG-X measured 22% redundancy in a
production-grade pipeline. α-nDCG over chunk-level subtopics is a principled measure of context
efficiency, and it already exists rather than needing invention. The annotation cost is the barrier,
not the concept.

### Recommendation

If you have or can afford nugget-level annotations, **α-nDCG at α = 0.5 alongside plain nDCG** is
the most informative diversity pair available. The **gap between them is your redundancy cost**,
expressed in the same units as your primary quality metric.

For RAG specifically, the cheap approximation is RAG-X's Pairwise Redundancy — no annotation
required, and it captures the same signal at lower fidelity.

---

## 8.3 ERR-IA and the intent-aware family

**One-line:** ERR computed per intent, then averaged with intent probabilities as weights.

**Formula (sketch):**
```
   ERR-IA(ranking) = Σ_i  P(intent_i | query) · ERR_i(ranking)

   where ERR_i is ordinary ERR (§5.4) computed treating only
   documents relevant to intent i as relevant.
```

**Facets:** Correctness | query | ref | R | ⬤ ✅
**Source:** Chapelle, Ji, Liao, Velipasaoglu, Lai & Wu, *Intent-Based Diversification of Web Search
Results: Metrics and Algorithms*, **Information Retrieval 14(6):572–592, 2011**

### The idea, and its relationship to α-nDCG

The intent-aware ("-IA") construction is general: take any metric, compute it once per intent, and
average weighted by how likely each intent is. That gives DCG-IA, MAP-IA, ERR-IA.

Two things make ERR-IA notable:

1. **Intent probabilities are explicit weights.** If 80% of "jaguar" searchers want the car, ERR-IA
   says so rather than treating the three intents as equal — a genuine advance over S-recall and
   α-nDCG, both of which weight subtopics uniformly.
2. **ERR-IA is a generalization of α-nDCG.** The authors show this directly, and argue ERR-IA is the
   better metric versus earlier proposals like DCG-IA and MAP-IA. It was used to evaluate the
   diversity task in the **TREC 2010 Web track**.

```
   THE WEIGHTING THAT α-nDCG LACKS
   ═══════════════════════════════

   Query: "jaguar"
     P(car)    = 0.80
     P(animal) = 0.15
     P(OS)     = 0.05

   α-nDCG's view:          ERR-IA's view:
   ┌──────────────┐        ┌──────────────┐
   │ car    ▓▓▓▓  │        │ car    ██████│ 0.80
   │ animal ▓▓▓▓  │        │ animal ▓     │ 0.15
   │ OS     ▓▓▓▓  │        │ OS     ·     │ 0.05
   └──────────────┘        └──────────────┘
   all equal               weighted by demand

        o    "So a system serving only 'car' scores..."
       /|\
       / \

        o    "...0.80 under ERR-IA and 0.33 under
       /|\     S-recall. ERR-IA is right if your
       / \     traffic really is 80% car searchers."
```

### Advantages

- **Intent probabilities make the metric match your actual traffic.** The most realistic diversity
  measure available.
- **Generalizes α-nDCG**, so it is strictly more expressive.
- **Inherits ERR's cascade model**, including its correct handling of redundancy.
- **The -IA construction is reusable** for any base metric.

### Disadvantages

- **Requires intent probabilities**, which are hard to estimate and often just guessed. A wrong
  P(intent) distribution gives a confidently wrong metric.
- **Requires per-intent relevance judgments** — the most expensive annotation in this chapter.
- **Inherits ERR's stop-when-satisfied assumption**, which as §5.4 established is *inverted* for LLM
  consumers.
- **Complex to implement and to explain.**

### Domain examples

**Large-scale web search.** ERR-IA's home, and the one setting where intent probabilities can be
estimated reliably from query logs.

**E-commerce with mixed intent.** "Apple" — fruit, phone, record label. Query logs give you the
priors.

**Enterprise or RAG search.** Usually impractical. You lack the traffic volume to estimate intent
priors, and per-intent judgments are prohibitive. Use α-nDCG or S-recall instead.

### Recommendation

Use ERR-IA only if you can estimate intent probabilities **from data**. A guessed prior makes ERR-IA
worse than α-nDCG, because it adds a confident weighting on top of the same underlying judgments and
gives you a number that looks more precise while being less trustworthy.

## 8.3.1 NRBP — the diversity metric with a residual

Worth flagging because it connects two chapters: **NRBP (Novelty- and Rank-Biased Precision)** is an
adaptation of RBP for search result diversification, from Clarke, Kolla & Vechtomova, *An
Effectiveness Measure for Ambiguous and Underspecified Queries*, **ICTIR 2009** ✅.

If you adopted RBP for its residual (§5.5) and you also care about diversity, NRBP is the natural
combination — geometric persistence weighting, novelty discounting, and honest reporting of
uncertainty in one measure. It is the least-used metric in this chapter and arguably the best-suited
to sparse-judgment settings.

For meta-evaluation of this whole family, see Clarke, Craswell, Soboroff & Ashkan, *A Comparative
Analysis of Cascade Measures for Novelty and Diversity*, **WSDM 2011, pp. 75–84** ✅.

---

## 8.4 Chapter 8 summary

```
┌─────────────────────────────────────────────────────────────────┐
│  DIVERSITY METRICS: WHAT TO USE                                 │
├─────────────────────────────────────────────────────────────────┤
│  S-recall       coverage of subtopics; RANK-BLIND               │
│                 → cheapest diagnostic; use first                │
├─────────────────────────────────────────────────────────────────┤
│  α-nDCG         position × novelty; α is the knob               │
│                 → the workhorse. Report alongside nDCG;         │
│                   the GAP is your redundancy cost               │
├─────────────────────────────────────────────────────────────────┤
│  ERR-IA         intent-weighted; generalizes α-nDCG             │
│                 → only if you can estimate intent priors        │
│                   FROM DATA                                     │
├─────────────────────────────────────────────────────────────────┤
│  NRBP           novelty + RBP's residual                        │
│                 → best fit for sparse judgments; underused      │
├─────────────────────────────────────────────────────────────────┤
│  FOR RAG, IF YOU CAN AFFORD NO ANNOTATION:                      │
│  RAG-X's Pairwise Redundancy + Exclusive Hit Rate               │
│  (Supplement B §D.4) capture the same signal, label-free.       │
├─────────────────────────────────────────────────────────────────┤
│  THE ARGUMENT TO REMEMBER                                       │
│  Clarke et al.: evaluation measures act as objective functions  │
│  to be optimized. A measure blind to redundancy will produce    │
│  systems that generate it. Your reranker is optimizing whatever │
│  you measure — including the things you forgot to measure.      │
└─────────────────────────────────────────────────────────────────┘
```

---

# Chapter 9 — Fairness and Exposure

## 9.0 A different kind of stakeholder

Every metric so far scores a ranking by its value **to the searcher**. Chapter 9 asks what the
ranking does **to the ranked**.

Singh and Joachims frame this against the Probability Ranking Principle — the classical claim that
the ideal ranking orders items by decreasing probability of relevance, because that maximizes
utility to the user. Their question: is that uncompromising focus on utility to users still
appropriate when the items being ranked are not books?

```
   WHAT RANKING ACTUALLY ALLOCATES
   ═══════════════════════════════

   ┌─────────────────────────────────────────┐
   │  rank 1  ████████████████  ← attention  │
   │  rank 2  ████████          │            │
   │  rank 3  █████             │  exposure  │
   │  rank 4  ███               │            │
   │  rank 5  ██                │            │
   │  ...     ·                 ▼            │
   └─────────────────────────────────────────┘

   When the ranked items are JOB CANDIDATES,
   that column is economic opportunity.

   When they are SELLERS, it is revenue.
   When they are ARTICLES, it is influence.

        o    "We just rank by relevance."
       /|\
       / \

        o    "Relevance scores are continuous.
       /|\     Exposure is winner-take-most. A
       / \     candidate 1% less relevant can get
              80% less attention."
```

That last point is the technical heart of the chapter: **small differences in relevance produce
large differences in exposure**, because position bias is steep. That is not a fairness opinion; it
is a measurement fact about ranked interfaces. Biega et al. note that position bias has been
established by eye-tracking and other empirical studies, and — importantly — persists even when the
elements at different ranks are randomly permuted.

## 9.0.1 Why a RAG practitioner should not skip this chapter

Three reasons, in increasing order of urgency:

1. **Your corpus has authors.** If your enterprise RAG systematically surfaces one team's
   documentation and never another's, you have made an organizational decision by accident.
2. **Regulation is arriving.** Ranked-output fairness is already litigated in hiring and lending.
3. **It is nearly unmeasured in RAG.** Across 63 RAG-evaluation papers surveyed by Brehme et al.,
   **one** evaluated whether retrieved documents fairly represent protected groups. If fairness
   matters for your use case, you are at the frontier and will be building rather than adopting.

---

## 9.1 Fairness of Exposure — group fairness

**One-line:** Constrain a ranking so that *groups* of items receive exposure proportional to their
merit.

**Facets:** Fairness | system | ref | R | ⬤ ✅
**Source:** Singh & Joachims, *Fairness of Exposure in Rankings*, **KDD 2018, pp. 2219–2228**,
doi 10.1145/3219819.3220088 · [arXiv:1802.07281](https://arxiv.org/abs/1802.07281)

### The idea

Rather than proposing one fairness metric, Singh and Joachims provide a **framework**: express a
fairness criterion as a *constraint on exposure allocation*, then find the ranking policy that
maximizes user utility subject to that constraint.

Their motivating example is a web service connecting employers to potential employees, where
exposure translates directly into probability of interview. Different fairness notions —
demographic parity, disparity of treatment, disparity of impact — become different constraints in
the same optimization.

### Diagram

```
   EXPOSURE VS MERIT
   ═════════════════

   Two groups, nearly equal average relevance:
     Group A: mean relevance 0.62
     Group B: mean relevance 0.60

   RELEVANCE-OPTIMAL RANKING:
   ┌──────────────────────────────────┐
   │ 1. A   ████████████████          │
   │ 2. A   ████████                  │  Group A exposure: 87%
   │ 3. A   █████                     │  Group B exposure: 13%
   │ 4. B   ███                       │
   │ 5. B   ██                        │
   └──────────────────────────────────┘

   A 3% relevance gap → a 74-point exposure gap.

        o    "The ranking is correct though."
       /|\
       / \

        o    "It's utility-optimal. Whether it's
       /|\     ACCEPTABLE is a different question,
       / \     and it's the one this framework
              lets you answer."
```

### Advantages

- **A framework, not a single metric.** You express *your* fairness criterion rather than adopting
  someone else's.
- **Explicitly trades off against utility**, so the cost of fairness is measured rather than hidden.
- **Group-level formulation is what most regulation targets.**
- **Well-developed follow-on literature** — policy learning for fairness in ranking (NeurIPS 2019),
  dynamic learning-to-rank (SIGIR 2020) — so it is a living line of work rather than a one-off.

### Disadvantages

- **Requires group membership labels**, which are often unavailable, legally sensitive, or both.
- **Group fairness can be satisfied while individuals are treated unfairly** — the gap Biega et al.
  target (§9.2).
- **You must choose a fairness criterion**, and that choice is normative, not technical. The
  framework will not make it for you.
- **Requires a merit estimate**, which is usually the relevance score — importing all of relevance
  estimation's biases into the fairness constraint.

### Domain examples

**Hiring and marketplace platforms.** The design target, and where the stakes are clearest.

**Enterprise RAG over multi-team documentation.** A genuinely useful reframing: treat teams as
groups and measure whether retrieval systematically favours one team's docs. Cheap to compute if
your metadata has an owner field, and it frequently surfaces something real.

**Consumer web search.** Contested territory. Whether search engines owe publishers exposure
fairness is an active policy debate, not a settled engineering question.

### Recommendation

If you have group labels and any stakes attached to exposure, **measure the exposure distribution
before you attempt to constrain it.** Most teams have never computed it and are surprised by the
concentration. Measurement is cheap; the normative decision about what to do is the expensive part
and should be made by people beyond the engineering team.

---

## 9.2 Equity of Attention — individual fairness, amortized

**One-line:** Individual items should receive attention proportional to their relevance — not
necessarily in any single ranking, but **amortized across many rankings**.

**Facets:** Fairness | system | ref | R | ⬤ ✅
**Source:** Biega, Gummadi & Weikum, *Equity of Attention: Amortizing Individual Fairness in
Rankings*, **SIGIR 2018, Ann Arbor MI**, doi 10.1145/3209978.3210063

### The key distinction — and why both papers exist

These two 2018 papers are constantly cited together and are **not** the same thing. Biega et al. say
so explicitly: Singh and Joachims proposed a notion of *group* fairness based on equality of
exposure for demographic groups, which is technically complementary and similar in spirit, but is
geared for a different purpose and **does not aim at individual fairness**.

```
   THE TWO 2018 PAPERS
   ═══════════════════

   SINGH & JOACHIMS (KDD)        BIEGA ET AL. (SIGIR)
   ──────────────────────        ────────────────────
   GROUP fairness                INDIVIDUAL fairness
   demographic parity            per-item proportionality
   within ONE ranking            AMORTIZED over many
                                 rankings

        o    "Which one do I need?"
       /|\
       / \

        o    "Group labels and regulatory exposure
       /|\     → Singh & Joachims.
       / \     A marketplace where each seller is a
              stakeholder → Biega et al.
              They answer different questions."
```

### The amortization insight

This is the contribution worth internalizing. **A single ranking cannot be individually fair** —
someone must be first. But *over a thousand queries*, attention can be allocated proportionally to
merit.

```
   AMORTIZATION
   ════════════

   Query 1:  A B C      Individually unfair (A wins)
   Query 2:  B C A      Individually unfair (B wins)
   Query 3:  C A B      Individually unfair (C wins)
             ───────
   Amortized: A, B, C each got top position once.
              FAIR IN AGGREGATE.

        o    "So unfairness is fine if it averages out?"
       /|\
       / \

        o    "It's the only fairness achievable in a
       /|\     ranked interface. Position 1 is scarce
       / \     by construction. Amortization is the
              honest response to that scarcity."
```

### Advantages

- **Individual-level**, so no group labels required — a substantial practical advantage.
- **Amortization is the right frame for a repeated-interface system**, which is what search is.
- **Actionable over time** rather than requiring per-query compromise.
- **Avoids the group-definition problem** entirely.

### Disadvantages

- **Requires tracking attention over time**, so you need logging infrastructure most teams lack.
- **Merit estimation is still the weak link** — proportional to *estimated* relevance.
- **Slow to correct.** An item under-exposed for six months is not made whole by next month's
  ranking.
- **Does not satisfy group-fairness requirements**, so it may not meet a regulatory obligation.

### Domain examples

**Two-sided marketplaces.** The natural fit — each seller is an individual stakeholder with a
legitimate claim to proportional attention.

**Academic and content search.** Amortized author-level exposure is a real concern in citation
dynamics and almost never measured.

**RAG over an internal knowledge base.** A quietly useful application: amortized attention per
*document* reveals which parts of your corpus are never retrieved. Documents with zero lifetime
exposure are either redundant or unfindable, and both are worth knowing.

### Recommendation

Use amortized exposure as a **corpus-health diagnostic** even if fairness is not your motivation.
Compute the distribution of lifetime retrieval counts across your corpus. A long tail of never-
retrieved documents tells you either your corpus is bloated or your retrieval has blind spots — and
you cannot tell which from any other metric in this white paper.

## 9.2.1 Related instruments worth knowing

| Work | Contribution | Status |
|---|---|---|
| Yang & Stoyanovich, *Measuring Fairness in Ranked Outputs*, SSDBM 2017 | Early statistical-parity measures for rankings | ✅ |
| TREC 2019 Fair Ranking Track ([arXiv:2003.11650](https://arxiv.org/abs/2003.11650)) | A shared task and test collection | ✅ |
| Wu, Li, Wu, Tao & Fang, COLING 2025 pp. 10021–10036 ([arXiv:2409.19804](https://arxiv.org/abs/2409.19804)) | *Does RAG introduce unfairness in LLMs?* — the one RAG fairness evaluation in the surveyed literature | ✅ |
| PEER ([arXiv:2405.00978](https://arxiv.org/abs/2405.00978)) | Language fairness in multilingual IR — equal expected rank across languages | ✅ |
| DUO ([arXiv:2406.04298](https://arxiv.org/abs/2406.04298)) | Indexical bias — over-representation of one side of a contested question | ✅ |

The last two were misfiled as Correctness metrics in the source catalogue and corrected during the
verification passes. They belong here.

---

## 9.3 Chapter 9 summary

```
┌────────────────────────────────────────────────────────────────┐
│  FAIRNESS: WHAT TO MEASURE                                     │
├────────────────────────────────────────────────────────────────┤
│  GROUP labels available + regulatory exposure                  │
│    → Fairness of Exposure (Singh & Joachims, KDD'18)           │
│                                                                │
│  NO group labels, repeated-interface system                    │
│    → Equity of Attention (Biega et al., SIGIR'18)              │
│                                                                │
│  Multilingual retrieval                                        │
│    → PEER                                                      │
│                                                                │
│  Contested / political topics                                  │
│    → DUO (indexical bias)                                      │
├────────────────────────────────────────────────────────────────┤
│  THE DIAGNOSTIC TO RUN EVEN IF FAIRNESS ISN'T YOUR GOAL        │
│                                                                │
│  Compute the exposure distribution over your corpus.           │
│  Two things fall out for free:                                 │
│    ▸ how concentrated attention is                             │
│    ▸ which documents are NEVER retrieved                       │
│  The second is a corpus-health signal no other metric gives.   │
├────────────────────────────────────────────────────────────────┤
│  ⚠️ REMEMBER: these metrics can TRADE OFF against nDCG. They   │
│  are constraints, not quality measures. Optimizing them will   │
│  reduce measured relevance, and that is the intended           │
│  behaviour, not a regression.                                  │
└────────────────────────────────────────────────────────────────┘
```

---

# Chapter 10 — Online and Counterfactual Evaluation

## 10.0 The data you already have

Everything so far required judgments — someone deciding what was relevant. Chapter 10 asks whether
your users have already answered that question through their behaviour.

The appeal is obvious, and Radlinski, Kurup and Joachims state it precisely: unlike expert
judgments, usage data can be collected at essentially zero cost, it is available in real time, and
it reflects the values of the **users** rather than those of judges far removed from the users'
context at the time of the information need.

Then they demonstrate that the obvious way to use it does not work.

## 10.1 ⚠️ The negative result that should reshape your dashboard

**Source:** Radlinski, Kurup & Joachims, *How Does Clickthrough Data Reflect Retrieval Quality?*,
**CIKM 2008, pp. 43–52, Napa Valley** ✅

Deploying an operational search engine on the arXiv.org e-print archive, under a controlled
experiment design, they tested eight absolute usage metrics. The finding:

> **None of the eight absolute usage metrics** explored — including number of clicks, frequency of
> query reformulations, and abandonment — **reliably reflect retrieval quality** for the sample sizes
> considered.

However, **paired experiment designs adapted from sensory analysis produce accurate and reliable
statements** about the relative quality of two retrieval functions. Two paired comparison tests
analyzing clickthrough from an **interleaved presentation** of ranking pairs both gave accurate and
consistent results.

```
   THE RESULT IN ONE PICTURE
   ═════════════════════════

   ABSOLUTE METRICS              PAIRED / INTERLEAVED
   ────────────────              ────────────────────
   "CTR went from 0.31           "Users preferred B's
    to 0.34"                      results 58% of the time"

        ✗ unreliable                  ✓ accurate and
          at realistic                  consistent
          sample sizes

   ┌──────────────────────────────────────────────────┐
   │  o   "Our CTR improved 3 points. Ship it."       │
   │ /|\                                              │
   │ / \                                              │
   │                                                  │
   │  o   "CTR is one of the eight metrics that was   │
   │ /|\   tested and found unreliable. You need a    │
   │ / \   paired comparison, not a level shift."     │
   └──────────────────────────────────────────────────┘
```

**Why this matters enormously and is widely ignored:** most production teams monitor exactly the
absolute metrics this paper found unreliable. CTR dashboards, abandonment rates, reformulation
counts — all eight categories. The published evidence says those numbers do not tell you what you
think they do at the sample sizes you have.

The explanation offered is that interleaving gives searchers the **easier task** of expressing a
*relative* preference between two rankers, rather than requiring the analyst to infer quality from
an absolute level.

---

## 10.2 Interleaving

**One-line:** Blend two rankers' results into one list, show it to every user, and attribute each
click to the ranker that contributed the clicked item.

**Facets:** Correctness | session | human | R | ⬤ ✅
**Source:** Radlinski, Kurup & Joachims, CIKM 2008, pp. 43–52 ✅

### Diagram

```
   TEAM-DRAFT INTERLEAVING
   ═══════════════════════

   RANKER A          RANKER B          INTERLEAVED
   ────────          ────────          ───────────
   1. doc-P          1. doc-Q          1. doc-P   [A]
   2. doc-Q          2. doc-R          2. doc-Q   [B]
   3. doc-S          3. doc-P          3. doc-R   [B]
   4. doc-T          4. doc-U          4. doc-S   [A]
                                       5. doc-U   [B]
                                       6. doc-T   [A]

   User clicks doc-R  ──▶  point to B
   User clicks doc-S  ──▶  point to A

   Aggregate over thousands of sessions ──▶ preference

   ┌──────────────────────────────────────────────────┐
   │  WHY THIS BEATS A/B TESTING                      │
   │                                                  │
   │  A/B:  half your users see A, half see B.        │
   │        You compare two POPULATIONS.              │
   │        Population variance swamps the signal.    │
   │                                                  │
   │  Interleaving: EVERY user sees both.             │
   │        You compare within-subject.               │
   │        Variance collapses. Far more sensitive.   │
   └──────────────────────────────────────────────────┘
```

### Advantages

- **Dramatically more sensitive than A/B testing** — within-subject comparison eliminates population
  variance, which is why it needs far less traffic to reach significance.
- **Reflects real users** in their real context.
- **Zero annotation cost.**
- **Validated at scale** — see Chapelle, Joachims, Radlinski & Yue, *Large-Scale Validation and
  Analysis of Interleaved Search Evaluation* ✅, and Hofmann, Whiteson & de Rijke, *Fidelity,
  Soundness, and Efficiency of Interleaved Comparison Methods*, **ACM TOIS 31(4):1–43, 2013** ✅.
- **Extends to more than two systems** — Schuth, Sietsma, Whiteson, Lefortier & de Rijke,
  *Multileaved Comparisons for Fast Online Evaluation*, **CIKM 2014** ✅.

### Disadvantages

- **Relative only.** Interleaving tells you B beats A. It never tells you either is good. You cannot
  build a quality dashboard from it.
- **Requires live traffic**, so it is unavailable pre-launch, for low-traffic systems, or in
  regulated environments where you cannot experiment on users.
- **Inherits click biases.** Position bias, presentation bias, and trust bias all persist.
- **Implementation subtleties matter.** Naive interleaving can be biased; team-draft and optimized
  variants exist because the obvious approach has flaws — see Radlinski & Craswell, *Optimized
  Interleaving for Online Retrieval Evaluation*, **WSDM 2013** ✅.
- **Not applicable to RAG generation.** You can interleave retrieved *documents*; you cannot
  meaningfully interleave two generated *answers* — the user sees one text.

### Domain examples

**High-traffic consumer search.** Interleaving's home. If you have the traffic, it is the most
sensitive comparison instrument available.

**RAG retriever comparison.** ⚠️ Partially applicable and underexplored. If your interface shows
retrieved sources, you can interleave those and read preference from source clicks. If the retrieval
is invisible to the user, you cannot — and this is a real gap in RAG evaluation with no good answer
yet.

**Enterprise search.** Often traffic-starved. A tool with 200 daily queries will not reach
significance in a useful timeframe.

### Recommendation

**If you have the traffic, interleave for every ranker comparison and stop relying on absolute click
metrics for that purpose.** The 2008 result is unambiguous: absolute metrics were unreliable,
paired comparisons were not.

Keep absolute metrics for *monitoring* (did something break?) and use interleaving for *deciding*
(is B better than A?). Those are different jobs and the same number cannot do both.

---

## 10.3 Counterfactual evaluation and IPS

**One-line:** Reweight logged interactions by the inverse of their observation propensity, so you can
estimate how a *new* ranker would have performed using *old* logs.

**Formula (sketch):**
```
   For a logged click on document d at position k:

     weight = 1 / P(examined at position k)

   Documents shown at low-attention positions get UP-weighted,
   correcting for the fact that they were rarely examined.
```

**Facets:** Correctness | system | human | R | ⬤ ✅
**Source:** Joachims, Swaminathan & Schnabel, *Unbiased Learning-to-Rank with Biased Feedback*,
**WSDM 2017, pp. 781–789**

### The idea

Interleaving requires deploying the candidate ranker. Counterfactual evaluation does not: **estimate
a new ranker's performance from logs generated by the old one.**

The obstacle is position bias. A document at rank 20 got few clicks — but was it bad, or simply
unseen? IPS answers by dividing observed clicks by the probability of examination, producing an
unbiased estimate of the underlying relevance.

### Diagram

```
   THE PROPENSITY CORRECTION
   ═════════════════════════

   RAW LOG                    IPS-CORRECTED
   ───────                    ─────────────
   rank  clicks  P(examine)   corrected
    1      500      0.90        556
    2      200      0.60        333
   10       20      0.10        200
   20        5      0.03        167

        o    "Rank 20 only got 5 clicks."
       /|\
       / \

        o    "It was examined 3% of the time. Adjusted,
       /|\     it performed comparably to rank 10.
       / \     Your log said it was terrible. Your log
              was measuring exposure, not quality."
```

### Advantages

- **No deployment risk.** Evaluate a candidate ranker without exposing users to it.
- **Reuses existing logs** — enormous practical value.
- **Statistically principled**, with unbiasedness guarantees under stated assumptions.
- **Position-bias estimation is itself now tractable** — Agarwal, Zaitsev, Wang, Li, Najork &
  Joachims, *Estimating Position Bias Without Intrusive Interventions*, **WSDM 2019** ✅, removes the
  need for randomization experiments that degrade user experience.

### Disadvantages

- **Requires propensity estimates**, and errors in them propagate directly into the result.
- **High variance when propensities are small.** Dividing by 0.03 amplifies noise as well as signal.
- **Assumes the logging policy had support** over the actions you want to evaluate. A document your
  old ranker *never* showed has no data, and no reweighting creates it.
- **Complex to implement correctly**, and easy to implement subtly wrongly.

### Domain examples

**Large-scale search and recommendation.** The intended setting and where it delivers most.

**RAG reranker selection.** A genuinely promising and underused application: if you log which chunks
were retrieved and whether the answer was correct, IPS-style reweighting lets you estimate a new
reranker offline. Note the support problem is severe here — your log only contains chunks your
current retriever surfaced.

**Anything low-traffic.** Variance will dominate. Do not bother.

### Recommendation

Use counterfactual evaluation to **shortlist** candidates offline, then interleave the top two or
three online. Neither instrument replaces the other: IPS is cheap and biased-if-misspecified,
interleaving is expensive and trustworthy.

⚠️ **The support assumption is the failure mode to watch.** If you are evaluating a retriever that
surfaces documents your current one never did, your logs are silent on exactly the cases that
matter, and IPS will confidently report on the subset it can see.

---

## 10.4 Session and satisfaction measures

Brief treatment, since these are less standardized.

| Metric | What it captures | Note |
|---|---|---|
| **sDCG** | DCG extended over a multi-query session | Järvelin et al., ECIR 2008 ⬜ *not verified this pass* |
| **Abandonment rate** | Sessions with no click | ⚠️ Among the eight metrics found unreliable in 2008 |
| **Reformulation rate** | User rewrote the query | ⚠️ Also among the eight |
| **Task completion time** | Time to satisfy the need | Manning Ch. 8 ✅ |
| **Time-biased gain** | Gain discounted by time spent | Smucker & Clarke, SIGIR 2012 ⬜ *not verified this pass* |

Two of these carry the 2008 warning explicitly. Abandonment and reformulation are *diagnostic*
signals — useful for spotting that something broke — not *quality* measures.

Two entries remain ⬜. They are marked as such rather than presented as verified, and will be
resolved before Installment 4, which covers the session and efficiency material properly.

## 10.4.1 The implicit-feedback foundation

Worth citing when someone proposes reading quality directly off clicks: Joachims, Granka, Pan,
Hembrooke, Radlinski & Gay, *Evaluating the Accuracy of Implicit Feedback from Clicks and Query
Reformulations in Web Search*, **ACM TOIS 25(2), Article 7, 2007** ✅. This is the eye-tracking-backed
study establishing what clicks do and do not tell you, and it predates and underpins the 2008
negative result.

---

## 10.5 Chapter 10 summary

```
┌────────────────────────────────────────────────────────────────┐
│  ONLINE EVALUATION: THE HIERARCHY                              │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  DECIDING between rankers                                      │
│    ▸ high traffic     → INTERLEAVING (most sensitive)          │
│    ▸ no deployment    → IPS / counterfactual (shortlist)       │
│    ▸ low traffic      → offline metrics; online won't reach    │
│                         significance                           │
│                                                                │
│  MONITORING for breakage                                       │
│    ▸ absolute click metrics ARE useful here                    │
│    ▸ they are NOT useful for deciding quality                  │
│                                                                │
├────────────────────────────────────────────────────────────────┤
│  ⚠️ THE 2008 RESULT, RESTATED                                  │
│                                                                │
│  Eight absolute usage metrics — clicks, reformulations,        │
│  abandonment among them — did NOT reliably reflect retrieval   │
│  quality at realistic sample sizes.                            │
│                                                                │
│  Paired interleaved comparisons DID.                           │
│                                                                │
│  Most production dashboards are built on the first group.      │
├────────────────────────────────────────────────────────────────┤
│  THE RAG GAP                                                   │
│  You can interleave retrieved SOURCES. You cannot interleave   │
│  generated ANSWERS — the user reads one text. There is no      │
│  good published answer to online RAG evaluation yet, and       │
│  anyone claiming otherwise is extrapolating.                   │
└────────────────────────────────────────────────────────────────┘
```

---

# Appendix 3A — Citation verification ledger

**Chapter 8 — Diversity and Novelty**

| Work | Citation | Status |
|---|---|---|
| Subtopic recall | Zhai, Cohen & Lafferty, *Beyond Independent Relevance*, SIGIR 2003, pp. 10–17 | ✅ |
| α-nDCG | Clarke, Kolla, Cormack, Vechtomova, Ashkan, Büttcher & MacKinnon, SIGIR 2008, pp. 659–666, doi 10.1145/1390334.1390446 | ✅ |
| ERR-IA | Chapelle, Ji, Liao, Velipasaoglu, Lai & Wu, *Intent-Based Diversification of Web Search Results*, Information Retrieval 14(6):572–592, 2011 | ✅ |
| NRBP | Clarke, Kolla & Vechtomova, *An Effectiveness Measure for Ambiguous and Underspecified Queries*, ICTIR 2009 | ✅ |
| Cascade meta-analysis | Clarke, Craswell, Soboroff & Ashkan, WSDM 2011, pp. 75–84, doi 10.1145/1935826.1935847 | ✅ |

**Chapter 9 — Fairness and Exposure**

| Work | Citation | Status |
|---|---|---|
| Fairness of Exposure | Singh & Joachims, KDD 2018, pp. 2219–2228, doi 10.1145/3219819.3220088; arXiv:1802.07281 | ✅ |
| Equity of Attention | Biega, Gummadi & Weikum, SIGIR 2018, Ann Arbor MI, doi 10.1145/3209978.3210063 | ✅ |
| Ranked-output fairness | Yang & Stoyanovich, *Measuring Fairness in Ranked Outputs*, SSDBM 2017 | ✅ |
| Fair Ranking Track | TREC 2019, arXiv:2003.11650 | ✅ |
| RAG fairness | Wu, Li, Wu, Tao & Fang, COLING 2025, pp. 10021–10036, arXiv:2409.19804 | ✅ |

**Chapter 10 — Online and Counterfactual**

| Work | Citation | Status |
|---|---|---|
| Interleaving + the negative result | Radlinski, Kurup & Joachims, CIKM 2008, pp. 43–52, Napa Valley | ✅ |
| Implicit feedback accuracy | Joachims, Granka, Pan, Hembrooke, Radlinski & Gay, ACM TOIS 25(2), Art. 7, 2007 | ✅ |
| IPS / unbiased LTR | Joachims, Swaminathan & Schnabel, WSDM 2017, pp. 781–789 | ✅ |
| Position bias estimation | Agarwal, Zaitsev, Wang, Li, Najork & Joachims, WSDM 2019 | ✅ |
| Interleaving at scale | Chapelle, Joachims, Radlinski & Yue, *Large-Scale Validation and Analysis of Interleaved Search Evaluation* | ✅ |
| Interleaving properties | Hofmann, Whiteson & de Rijke, ACM TOIS 31(4):1–43, 2013 | ✅ |
| Multileaving | Schuth, Sietsma, Whiteson, Lefortier & de Rijke, CIKM 2014 | ✅ |
| Optimized interleaving | Radlinski & Craswell, WSDM 2013 | ✅ |
| Click test statistics | Yue, Gao, Chapelle, Zhang & Joachims, SIGIR 2010 | ✅ |

**⬜ Deferred to Installment 4:** sDCG (Järvelin et al., ECIR 2008); time-biased gain
(Smucker & Clarke, SIGIR 2012). Both are marked ⬜ in §10.4 rather than presented as verified.

---

# Appendix 3B — Running correction log

Nine corrections total, two of them mine. **No new corrections in this installment** — as in
Installment 2, the classical literature verified cleanly. The pattern across four installments is
consistent: well-cited pre-2015 work checks out; 2024–2026 preprints and secondary summaries are
where the errors live.

Two relocations confirmed rather than corrected: **PEER** and **DUO** now sit in Chapter 9 where they
belong, having been misfiled as Correctness metrics in the original catalogue.

---

# Appendix 3C — Document set status

| # | Document | Covers | Status |
|---|---|---|---|
| 0 | `ir-rag-metrics-catalogue-v2.md` | Full index | Complete |
| 1 | `whitepaper-vol1-part1.md` | Ch 0–4 | Complete |
| 2 | `whitepaper-supplement-A.md` | Alignment, Integrity/Drift | Complete + addendum |
| 3 | `whitepaper-supplement-B.md` | Correctness, Efficiency | Complete |
| 4 | `whitepaper-supplement-A-addendum.md` | 🟡 lifts, CKA correction | Complete |
| 5 | `whitepaper-vol1-part2.md` | Ch 5–7 | Complete |
| 6 | **`whitepaper-vol1-part3.md`** | **Ch 8–10** | **this file** |

**Remaining:**

| Installment | Chapters | Contents | Prerequisites |
|---|---|---|---|
| Vol I, 4 | 11–12 | Significance & reporting; classical efficiency; session metrics | Armstrong et al. ✅; needs sDCG + time-biased gain ⬜ |
| Vol II, 8 | 22–24 | Meta-evaluation, judge reliability, deployment playbooks | Brehme survey already read |

Installment 4 completes Volume I. Chapter 11 has one citation already verified and waiting —
Armstrong, Moffat, Webber & Zobel, *Improvements That Don't Add Up: Ad-hoc Retrieval Results Since
1998*, CIKM 2009, pp. 601–610 — which argues that a decade of reported retrieval improvements did
not accumulate. It is the natural closing argument for a volume about measurement.
