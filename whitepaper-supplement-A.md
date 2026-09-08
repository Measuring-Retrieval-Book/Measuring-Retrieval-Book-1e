# Measuring Retrieval — Supplement A

## Two Dimensions, Read From Source
### ALIGNMENT and INTEGRITY / DRIFT

---

**Relationship to the main text.** The white paper's Volume I works through classical IR in
chapter order. This supplement jumps ahead to two RAG-era dimensions, because they are the two
where the catalogue entry is a *name* and nothing more, and where reading the actual paper changes
what you would do with the metric.

**Sourcing standard for this document.** Every metric below was described after reading the
paper's method section — the formula, the algorithm, or the operational definition — not the
abstract. Where I could only obtain the abstract, the entry says so explicitly and is marked
🟡 ABSTRACT-ONLY. Where a widely-circulated secondary summary contradicts the paper, I flag it.

**Why these two dimensions together.** They are complements. Alignment asks whether your components
cooperate *right now*. Integrity asks whether that answer survives contact with time. A team that
measures only Alignment ships a system that was correct in March. A team that measures only
Integrity knows precisely how fast something it never understood is decaying.

---

# PART A — ALIGNMENT

# A.1 What Alignment actually is

## A.1.1 The dimension in one page

Classical IR had one component, so it had one question: was the ranking good? RAG has two
components, which creates a question classical IR never had to ask:

> **Both components scored well. Why did the system fail?**

Alignment metrics exist to answer that. They are not "retrieval metrics" or "generation metrics."
They are metrics of the *interface* between the two.

```
   WHY YOU CANNOT GET THIS FROM COMPONENT SCORES
   ═════════════════════════════════════════════

   RETRIEVER          INTERFACE          GENERATOR
   ─────────          ─────────          ─────────
   nDCG 0.89            ???              faithfulness 0.84
   recall 0.91                           fluency: fine
   MRR 0.86                              coherence: fine

        o    "Both sides are excellent."
       /|\
       / \

        o    "You have measured two ends of a bridge
       /|\     and nothing about the bridge."
       / \
```

## A.1.2 The four Alignment questions

Reading across the literature, Alignment metrics cluster into four distinct questions. This
taxonomy is mine, not any paper's, but it maps cleanly onto what the papers actually do:

| # | Question | Family | Metrics |
|---|---|---|---|
| 1 | **What did this passage contribute?** | Contribution | eRAG, DIG, ΔSePer, Gain |
| 2 | **Did the generator use what the retriever ranked highly?** | Attribution | WARG |
| 3 | **Which component caused this failure?** | Quadrant | CUE, MIRAGE |
| 4 | **Is this ranking good *for an LLM* specifically?** | Machine-utility ranking | UDCG |

Picking one metric from each family gives you far more diagnostic power than four metrics from
family 1 — which, as §A.2.6 shows, is what most teams accidentally do.

---

# A.2 Family 1 — The Contribution Metrics

## A.2.0 The shared idea

Four published metrics, four different research groups, one identical trick:

```
   THE ABLATION TRICK
   ══════════════════

   Ask the model WITHOUT the passage.     ──▶  measure something
   Ask the model WITH the passage.        ──▶  measure it again
   The DIFFERENCE is the passage's value.

        ┌──────────────┐        ┌──────────────┐
        │  q           │        │  q + passage │
        │              │  vs.   │              │
        └──────┬───────┘        └──────┬───────┘
               ▼                       ▼
            score₀                  score₁

              contribution = score₁ − score₀

   The four metrics differ ONLY in what "score" means.
```

| Metric | What is differenced | Source |
|---|---|---|
| **eRAG** | Downstream task performance | Salemi & Zamani, SIGIR'24 |
| **Gain** | Contribution to a correct output | Jiang et al., ACL'25 |
| **DIG** | LLM generation confidence | Wang et al., EMNLP'25 Oral |
| **ΔSePer** | Semantic perplexity (belief mass on the true answer) | Dai et al., ICLR'25 Spotlight |

Hold that table. It becomes the most important practical recommendation in this supplement (§A.2.6).

---

## A.2.1 eRAG — document-level downstream utility

**One-line:** Feed each retrieved document to the LLM *individually*, score the resulting output
against the task's ground truth, and use that score as the document's relevance label.

**Facets:** Alignment | passage | ref | E2E | ⬤ ✅
**Source:** Salemi & Zamani, SIGIR'24 · [arXiv:2404.13781](https://arxiv.org/abs/2404.13781)

### The idea, from the paper

The paper's motivating observation is blunt and worth internalizing: evaluating a retriever using
query–document relevance labels shows only a *small* correlation with the RAG system's downstream
performance. Human relevance and machine usefulness are not the same quantity, and the field had
been assuming they were.

eRAG's move is to stop asking humans what is relevant and start asking the *generator*. Each
document in the retrieval list is individually run through the LLM; the output is scored against the
downstream ground truth; that score becomes the document's label. You then aggregate those
per-document labels with any ordinary set-based or ranking metric you like — precision, nDCG,
whatever you already report.

That last property is the elegant part. **eRAG is not a replacement for nDCG. It is a replacement
for the relevance labels you feed into nDCG.**

### Diagram

```
   CLASSICAL LABELS vs eRAG LABELS
   ═══════════════════════════════

   CLASSICAL:
      human ──▶ "doc 3 is relevant" ──▶ nDCG
        o
       /|\   "It's about the right topic."
       / \

   eRAG:
      doc 3 alone ──▶ LLM ──▶ answer ──▶ score vs truth ──▶ label ──▶ nDCG
                              │
                              └── "Could the model actually
                                   ANSWER using only this?"

   Same nDCG formula. Completely different input.
```

### Reported results

Kendall's τ correlation with downstream RAG performance improves by **0.168 to 0.494** over
baseline methods. Runtime improves, and GPU memory consumption drops by **up to 50×** versus
end-to-end evaluation.

That 50× is not a footnote. It is the reason eRAG is deployable: full end-to-end evaluation over
every subset of retrieved documents is combinatorially hopeless, and eRAG's per-document
decomposition makes the problem linear.

### Advantages

- **Directly targets the thing you care about.** The label *is* downstream performance, not a proxy
  for it.
- **Drops into your existing metric stack.** Produces labels, so nDCG/MAP/P@K all still work.
- **Dramatically cheaper than true end-to-end.** The 50× memory reduction makes it viable in CI.
- **Component-agnostic.** Swap the retriever and the labels stay valid; swap the generator and they
  correctly become invalid, which is the right behaviour.

### Disadvantages

- **Requires downstream ground-truth labels.** This is reference-based. If you have no golden
  answers, eRAG is unavailable to you.
- **Independence assumption.** Each document is scored *alone*. A document that is useless in
  isolation but essential in combination with another scores zero. For multi-hop tasks this is a
  material blind spot — precisely the gap SURE-RAG identifies when it argues that missing hops
  cannot be detected by scoring passages independently.
- **Generator-bound.** Labels are valid only for the generator that produced them. Change the model
  and you must relabel.
- **Cost is linear in k, not free.** One LLM call per retrieved document per query.

### Domain examples

**Enterprise knowledge base (single-hop, FAQ-like).** Near-ideal fit. Most questions are answerable
from one chunk, so the independence assumption holds. Use eRAG labels to retrain your reranker and
you are optimizing the reranker for the generator you actually deploy.

**Financial multi-document analysis.** Poor fit as the sole metric. "What was the revenue change
across the three segments?" requires three documents jointly. Each scores near zero alone. eRAG will
report your retriever as failing when it succeeded. Pair with a set-level sufficiency measure.

**Medical guideline extraction.** Mixed. RAG-X's GuidelineQA work suggests these questions are often
single-source — but where they are not, the failure is silent and clinically consequential. Sample
and manually audit the zero-labelled documents before trusting the aggregate.

### Recommendation

Use eRAG to **generate labels, then compute nDCG on them**, and report that alongside nDCG on human
labels. The *gap between the two numbers* is your relevance–utility divergence, and it is one of the
most informative single numbers you can put on a RAG dashboard.

If your task is multi-hop, do not use eRAG alone. Its independence assumption is not a minor
approximation there; it is a structural mismatch.

### Failure mode

```
   THE INDEPENDENCE TRAP

   Question: "Did revenue grow faster than costs in FY24?"
   Doc A: revenue figures     ──alone──▶ can't answer ──▶ label 0
   Doc B: cost figures        ──alone──▶ can't answer ──▶ label 0
   Doc A + Doc B together     ──────────▶ perfect answer

   eRAG nDCG: 0.00           Actual system: works fine

        o    "Our retriever scores zero on eRAG."
       /|\
       / \

        o    "Your task is multi-hop. eRAG scores
       /|\     single documents. It's measuring the
       / \     wrong unit."
```

---

## A.2.2 DIG — Document Information Gain

**One-line:** A document's value is the difference in the LLM's *generation confidence* with and
without that document in the context.

**Facets:** Alignment | passage | free | E2E | ◐ ✅
**Source:** Wang et al., EMNLP'25 **Oral** · [arXiv:2509.12765](https://arxiv.org/abs/2509.12765)

### The idea, from the paper

The framing problem is that current RAG frameworks struggle to identify whether retrieved documents
*meaningfully contribute* to answer generation, which makes it hard to filter out irrelevant or
misleading content.

DIG's answer: measure the document's value by computing the difference of the LLM's generation
confidence with and without the document augmented. Then — and this is where it differs from eRAG —
use those DIG scores to **train a specialized reranker** that filters irrelevant documents and
prioritizes valuable ones.

### Diagram

```
   DIG: CONFIDENCE AS A PROXY FOR CONTRIBUTION
   ═══════════════════════════════════════════

   without doc:   "I think it's... Bern?"     confidence 0.41
                                                    │
   with doc:      "It's Bern."                confidence 0.93
                                                    │
                                    DIG = 0.93 − 0.41 = 0.52

        o    "So high DIG means the doc helped."
       /|\
       / \

        o    "High DIG means the model became MORE CONFIDENT.
       /|\     Those are the same thing only when the model
       / \     is well-calibrated. Hold that thought."
```

### Reported results

On NaturalQA, exact-match accuracy improves by **17.9%** over naive RAG, **4.5%** over
self-reflective RAG, and **12.5%** over modern ranking-based RAG, with an average **15.3%**
increment on GPT-4o across all datasets.

### Advantages

- **Reference-free.** No golden answers needed — a decisive practical advantage over eRAG and one
  that makes DIG viable in CI on unlabelled production traffic.
- **Cheap relative to full generation scoring.** Confidence is available from the forward pass.
- **Dual-use.** The same signal is both a diagnostic metric and a reranker training target.
- **Works with multiple retrievers.** The paper reports gains under both single- and
  multiple-retriever paradigms.

### Disadvantages

- **Confidence ≠ correctness.** This is the load-bearing weakness. A document that is *confidently
  wrong* — a plausible, on-topic, factually incorrect passage — will raise generation confidence and
  post a high DIG. DIG cannot distinguish "helped the model be right" from "helped the model be
  sure."
- **Inherits all LLM calibration pathologies.** If your generator is overconfident on a topic, DIG
  is miscalibrated on that topic.
- **Circularity when used as a training target.** If you train the reranker on DIG and then report
  DIG, you are reporting a metric the system was optimized against. Use a held-out generator.
- **Same independence assumption as eRAG.**

### Domain examples

**High-volume consumer support.** Excellent fit. Reference-free means you can compute it on live
traffic with no annotation, and support answers are typically single-source.

**Adversarial or misinformation-adjacent domains.** Dangerous. The confidence-versus-correctness gap
is exactly what an adversarial passage exploits — a well-written false passage is *designed* to
raise confidence. Do not use DIG as a safety metric in any domain where the corpus may contain
deliberately misleading content.

**Legal research.** Use with care. Legal text is written to sound authoritative, so confidence
gains are cheap and correctness gains are not. Pair DIG with a reference-based check on a
labelled subset.

### Recommendation

Use DIG when you need a reference-free contribution signal — that is its unique value. But **never
report DIG as evidence of correctness.** Report it as evidence of *influence*. A document with high
DIG changed the model's behaviour; whether it changed it for the better requires a different metric.

If you use DIG to train a reranker (its intended use), compute your *reported* DIG with a
different generator than the one used for training.

### Failure mode

```
   THE CONFIDENT LIAR

   Retrieved doc: a well-written, on-topic, WRONG passage
   Model without it:  "I'm not sure, possibly X?"   conf 0.35
   Model with it:     "It is definitely Y."          conf 0.95

   DIG = 0.60   ← the highest-scoring document in the set
   Answer = wrong

        o    "DIG ranked our worst document first."
       /|\
       / \

        o    "DIG ranked your most PERSUASIVE document first.
       /|\     It never claimed to rank the most correct one."
       / \
```

---

## A.2.3 ΔSePer — Semantic Perplexity Reduction

**One-line:** Sample many answers, cluster them by meaning, measure how much probability mass sits
on the *correct* meaning-cluster before and after retrieval; the increase is retrieval's utility.

**Facets:** Alignment | query | **ref** | E2E | ◐ ✅
**Source:** Dai, Xu, Ye, Liu & Xiong, ICLR'25 **Spotlight** · [arXiv:2503.01478](https://arxiv.org/abs/2503.01478)

### The idea, from the paper's Algorithm 1

This is the most mathematically involved metric in the family, and the algorithm is worth stating
because summaries of it circulate in mangled form.

```
   ALGORITHM 1 (as published)
   ══════════════════════════

   Require: model M, reference answer a*, entailment model E,
            threshold τ, number of samples N

   1. Sample N responses  rᵢ ~ P_M(r)
   2. Compute likelihoods ℓᵢ = P_M(rᵢ)
   3. SePer_H  (hard / clustering variant):
        a. Cluster responses so that E(rᵢ,rⱼ) ≥ τ within a cluster
        b. Identify C_{a*}, the cluster matching the reference answer
        c. P_M(a*) = Σ_{rᵢ ∈ C_{a*}} ℓᵢ
      SePer_S  (soft / kernel variant):
        a. kᵢ = E(rᵢ, a*)
        b. P_M(a*) = Σᵢ ℓᵢ · kᵢ
   4. Repeat with retrieved documents D to get P_M(a* | D)
   5. ΔSePer = P_M(a* | q, D) − P_M(a* | q)
```

Entailment is computed with `deberta-v2-xlarge-mnli`, which the authors note is far more efficient
than API-based entailment judgment without significant performance drop.

### ⚠️ A correction to a widely-circulated summary

A popular AI-paper-summary site states that SePer "doesn't require human annotations or ground truth
answers." **This is wrong.** Algorithm 1 requires `a*`, the reference answer, at step 3 in both
variants. You cannot identify the correct semantic cluster without knowing what correct means.

This matters operationally: if you adopted SePer believing it was reference-free, you built your
plan on a false premise. **SePer is reference-based.** DIG is the reference-free member of this
family.

```
        o    "The blog said SePer needs no ground truth."
       /|\
       / \

        o    "Step 3b: 'Identify C_{a*}, matching the
       /|\     reference answer.' Read the algorithm,
       / \     not the summary of the algorithm."
```

### Diagram

```
   BELIEF MASS ON THE RIGHT ANSWER
   ═══════════════════════════════

   BEFORE RETRIEVAL — sample 20 answers, cluster by meaning:

     ┌────────────┬────────────┬────────────┐
     │  "Bern"    │  "Zurich"  │ "Geneva"   │
     │   ████     │  ████████  │   ██████   │
     │   0.20     │    0.45    │    0.35    │
     └────────────┴────────────┴────────────┘
          ▲ correct cluster        P_M(a*) = 0.20

   AFTER RETRIEVAL:

     ┌────────────┬────────────┬────────────┐
     │  "Bern"    │  "Zurich"  │ "Geneva"   │
     │ ██████████ │     █      │     █      │
     │   0.88     │    0.07    │    0.05    │
     └────────────┴────────────┴────────────┘

              ΔSePer = 0.88 − 0.20 = 0.68

   NOTE: this is NOT token perplexity. Answers that
   MEAN the same thing are pooled, so "Bern" and
   "the city of Bern" land in one cluster.
```

That pooling is the actual contribution. Token-level perplexity punishes paraphrase; semantic
clustering does not.

### Advantages

- **Measures belief, not surface form.** Robust to paraphrase in a way ROUGE/BLEU/exact-match are
  not.
- **Strongest human correlation in the family.** The paper reports SePer's entailment-based answer
  scoring achieving the highest accuracy among tested evaluators and being on par with human-level
  judgment, validated on the EVOUNA benchmark.
- **Two variants for two budgets.** SePer_H (hard clustering) is cheaper; SePer_S (soft kernel)
  gives a continuous, more nuanced score.
- **Isolates retrieval's contribution** from generation quality by construction.

### Disadvantages

- **Reference-based** — see the correction above.
- **Expensive.** N samples per query, per condition, plus an entailment model over every response
  pair for the hard variant. This is not a per-commit metric.
- **Threshold sensitivity.** `τ` controls clustering. Set it loose and distinct answers merge; set
  it tight and paraphrases fragment. The metric moves with τ and τ is rarely reported.
- **Entailment model is a dependency you now own.** Change deberta for something else and your
  historical numbers are not comparable — a Chapter-1-Dimension-III problem hiding inside an
  Alignment metric.

### Domain examples

**Research evaluation of retrievers.** The intended setting, and an excellent one. If you are
choosing between three retrievers offline, ΔSePer gives the most faithful ranking of their true
utility.

**Regulated domains needing paraphrase tolerance.** Clinical and legal answers are frequently
correct-but-differently-worded. Exact-match under-reports badly here; semantic clustering fixes it.

**Production monitoring.** Poor fit. N-sample Monte Carlo per query is not something you run on
live traffic. Use it on a fixed benchmark set at release cadence.

### Recommendation

Use ΔSePer as your **offline gold-standard utility measure** — the number you trust when choosing a
retriever — and something cheaper (DIG, or eRAG-labelled nDCG) for continuous monitoring. Report
`N` and `τ` alongside the score, always. A ΔSePer without its hyperparameters is not reproducible.

### Failure mode

```
   THE UNREPORTED THRESHOLD

   Team A: τ = 0.90 (tight)   ΔSePer = 0.31
   Team B: τ = 0.70 (loose)   ΔSePer = 0.58

   Same system. Same data. Same metric name.

        o    "Team B's retriever is much better!"
       /|\
       / \

        o    "Team B's clustering is much looser.
       /|\     You compared two different metrics
       / \     that share a name."
```

---

## A.2.4 Gain (GainRAG) — passage contribution to correct output

**One-line:** A signal estimating how well an input passage contributes to producing correct output,
used to train middleware that aligns retriever and LLM preferences.

**Facets:** Alignment | passage | free | E2E | ◐ ✅
**Source:** Jiang et al., ACL'25 · [arXiv:2505.18710](https://arxiv.org/abs/2505.18710)
🟡 Method read at abstract + framing level; full training detail not retrieved.

### The idea

GainRAG's premise is the most interesting sentence in this entire family, and it deserves quoting
in substance: there is a **preference gap** between retrievers and LLMs. Some highly relevant
passages *interfere* with LLM reasoning because they contain complex or contradictory information,
while some indirectly related or even inaccurate content *helps* the LLM generate more accurate
answers by providing suggestive information or logical clues.

Read that twice. Two independent research groups — Jiang et al. here, and Cuconasu et al. in *The
Power of Noise* (SIGIR'24) — arrived at the same counterintuitive finding by different routes.
**Relevance and usefulness are not merely imperfectly correlated. They sometimes point in opposite
directions.**

### Diagram

```
   THE PREFERENCE GAP
   ══════════════════

   RETRIEVER'S RANKING          LLM'S ACTUAL PREFERENCE
   ───────────────────          ───────────────────────
   1. dense, technical,     ──▶  confusing, hurts answer
      highly relevant

   2. tangential, simple,   ──▶  provides the logical
      "less relevant"            clue that unlocks it

        o    "So we should retrieve WORSE documents?"
       /|\
       / \

        o    "You should stop assuming your relevance
       /|\     labels describe what the model needs.
       / \     That's what 'gain' measures."
```

### ⚠️ The circularity warning

Gain is defined *in order to train a middleware*. If you train on gain and then report gain, you are
reporting a metric your system was optimized against. That number will look excellent and mean
nothing.

**If you adopt gain as a metric, compute it with a held-out generator that was not part of the
training loop.** This warning applies in weaker form to DIG (also used as a reranker target) and
does not apply to eRAG or ΔSePer, which were designed as measurements first.

### Advantages

- **Names a real and under-appreciated phenomenon.** The preference gap is the single most useful
  concept in this supplement for reasoning about why a good retriever can hurt.
- **Actionable by design** — the middleware is the deliverable, not just the number.
- **Trainable with limited data**, per the paper's framing.

### Disadvantages

- **Circular if reported naively** (above).
- **Primarily an optimization signal.** It was not designed as a reporting metric, and using it as
  one is off-label.
- **Pseudo-passage strategy** is introduced to mitigate degradation, which implies the raw signal
  has a degradation mode. Understand that before deploying.

### Domain examples

**Any domain where you control the reranker.** This is where gain belongs — as a training signal,
not a dashboard line.

**Domains with dense, technical source material.** Precisely where the preference gap bites: legal
statutes, clinical guidelines, engineering specs. The most "relevant" passage is often the least
usable one.

### Recommendation

**Treat gain as a training signal and report something else.** Its diagnostic value to you is
conceptual — internalize the preference gap — rather than numerical.

---

## A.2.5 WARG — Weighted Attribution-Relevance Gap

**One-line:** Measures how well the generator's actual document usage aligns with the retriever's
ranking, using attribution methods on both sides.

**Facets:** Alignment | passage | free | E2E | ◐ ✅
**Source:** Randl, Rocchietti, Henriksson, Abedjan, Lindgren & Pavlopoulos ·
[arXiv:2601.21803](https://arxiv.org/abs/2601.21803)

### The idea, from the paper

WARG is family 2 — attribution rather than contribution. Instead of ablating passages, RAG-E
computes what each component actually *attended to*:

- **Retriever side:** Integrated Gradients, adapted for retrieval
- **Generator side:** PMCSHAP, a Monte-Carlo-stabilized Shapley value approximation
- **WARG:** the gap between the two attributions

### The two failure modes it names

```
   WASTED RETRIEVAL              NOISE DISTRACTION
   ════════════════              ═════════════════

   Retriever: "#1 is best"       Retriever: "#4 is weak"
   Generator: ignores #1          Generator: builds answer on #4

   ┌────────┐                    ┌────────┐
   │#1 ★★★★★│ ← never used       │#1 ★★★★★│
   │#2 ★★★★ │ ← used             │#2 ★★★★ │
   │#3 ★★★  │                    │#3 ★★★  │
   │#4 ★    │                    │#4 ★     │ ← primary source
   └────────┘                    └────────┘

   You paid to retrieve gold      Your answer rests on
   and threw it away.             the weakest evidence.
```

### Reported prevalence — the number that should alarm you

| Failure | Share of queries |
|---|---|
| Generator ignores retriever's top-ranked document | **47.4 – 66.7%** |
| Generator relies primarily on a lower-ranked document | **48.1 – 65.9%** |

On domain-specific data the figures were roughly 60% and 57%. These are not edge cases. **On most
queries, in the systems studied, the generator is not using the document the retriever worked
hardest to find.**

### Advantages

- **Reference-free.** No golden answers required.
- **Mathematically grounded** in established attribution theory (Integrated Gradients, Shapley),
  rather than heuristic.
- **Produces named, actionable failure modes** rather than a bare scalar.
- **Auditable** — the intended use case is high-stakes deployment where you must explain the
  system's behaviour.

### Disadvantages

- **Computationally heavy.** Shapley approximation over passages is expensive even
  Monte-Carlo-stabilized.
- **Requires model internals.** Integrated Gradients needs gradients. Closed API models are
  wholly or partly out of reach.
- **Attribution ≠ causation.** What a model attended to and what changed its answer are correlated,
  not identical. This is a live debate in interpretability generally.
- **Newer and less replicated** than the contribution family.

### Domain examples

**Regulated high-stakes deployment.** The paper's own framing. If you must justify to a regulator
why the system said what it said, WARG's audit trail is the most defensible artefact in this
supplement.

**Debugging a reranker that "isn't helping."** If reranking improves nDCG but not answer accuracy,
WARG will tell you whether the generator is even looking at the reordered top.

**Closed-model API deployments.** Not usable for the retriever half unless you host the embedder.

### Recommendation

Run WARG **once, diagnostically**, before you invest in reranker improvements. If 60% of your
queries show wasted retrieval, improving retrieval ranking is close to worthless — the generator
is not consuming the ranking. Fix the interface first: prompt ordering, chunk formatting, explicit
citation instructions.

This is the highest-leverage insight in the supplement. Teams routinely spend quarters improving
nDCG for a generator that ignores rank order entirely.

---

## A.2.6 ⚠️ THE MOST IMPORTANT PAGE IN THIS SUPPLEMENT

### Four metrics, one measurement

```
   ┌──────────────────────────────────────────────────────────┐
   │  eRAG      differences  downstream task performance      │
   │  Gain      differences  contribution to correct output   │
   │  DIG       differences  generation confidence            │
   │  ΔSePer    differences  semantic belief mass             │
   └──────────────────────────────────────────────────────────┘
                            │
                            ▼
              ALL FOUR ABLATE THE PASSAGE AND
              MEASURE WHAT CHANGED.

   ┌────────────────────────────────────────────┐
   │  DASHBOARD                                 │
   │                                            │
   │  eRAG-nDCG   0.74  ▲                       │
   │  mean DIG    0.71  ▲                       │
   │  ΔSePer      0.69  ▲    "Four independent  │
   │  mean Gain   0.73  ▲     metrics agree!"   │
   └────────────────────────────────────────────┘

        o    "Strong corroboration across four metrics."
       /|\
       / \

        o    "One measurement wearing four hats.
       /|\     They agree because they're the same
       / \     question asked four ways."
```

### The rule

**Pick exactly one contribution metric.** Choose on supervision and cost, not on what it measures —
because what they measure is substantially the same thing:

| If you have... | Use | Why |
|---|---|---|
| Golden answers + offline compute budget | **ΔSePer** | Best human correlation; the gold standard |
| Golden answers + need it in CI | **eRAG** | Produces labels; 50× cheaper than E2E |
| No golden answers | **DIG** | The only reference-free option in the family |
| A reranker you're training | **Gain** (as signal, not metric) | Designed for this; report something else |

Then spend the freed dashboard slots on the *other three families* — WARG for attribution, CUE or
MIRAGE for quadrant diagnosis, UDCG for machine-utility ranking. Those measure genuinely different
things, and their disagreement is informative in a way the contribution family's agreement is not.

---

# A.3 Family 3 — The Quadrant Metrics

## A.3.1 CUE — Context Utilization Efficiency

**One-line:** Cross-reference *did the retriever find it?* against *did the generator adhere to it?*
and sort every query into one of four diagnostic quadrants.

**Facets:** Alignment | query | judge | E2E | ◐ ✅
**Source:** Sivakumar, Sugumaran & Qiang, RAG-X · [arXiv:2603.03541](https://arxiv.org/abs/2603.03541)

### The construction, from the paper

Two binary axes:

1. **Retrieval success** — determined by a cascading relevance function: exact substring match,
   then token-level overlap ≥ 0.80, then sentence-level semantic similarity ≥ 0.75
2. **Generator context adherence** — LLM-judged, thresholded at ≥ 0.7

### Diagram

```
                    GENERATOR ADHERES TO CONTEXT?
                       YES              NO
                 ┌──────────────┬──────────────┐
        FOUND    │ EFFECTIVE    │ INFORMATION  │
   RETRIEVER     │    USE       │  BLINDNESS   │
        IT?      │              │              │
                 │ the only     │ you had it,  │
                 │ real success │ model missed │
                 ├──────────────┼──────────────┤
        MISSED   │ HALLUCINATION│   CORRECT    │
                 │ "LUCKY GUESS"│  REJECTION   │
                 │              │              │
                 │ right answer │ model knew   │
                 │ NO evidence  │ it didn't    │
                 │  ⚠️ DANGER   │ know ✓       │
                 └──────────────┴──────────────┘

   Measured on GuidelineQA (Llama-3.1-8B + Qwen3-Embedding-8B):

     Effective Use          49.2%
     Lucky Guess            33.9%   ← a THIRD of the system
     Information Blindness   8.5%
     Correct Rejection      ~8.4%
```

### The Adherence Paradox

The same pipeline scored **Context Adherence 0.84** — the generator looked highly faithful. A third
of its correct answers had no retrieved support. The paper's diagnosis: a high adherence score
*incorrectly attributes* parametric answers to the context, giving a false sense of grounding.

```
   THE 14% GAP (state it correctly)
   ════════════════════════════════

   Accuracy            71.0%
   Context Hit Rate    57.6%
                      ──────
   Gap                 13.4%  ≈ 14%   ← THIS is the paper's 14%

   Accuracy            71.0%
   Effective Use       49.2%
                      ──────
   Gap                 21.8%           ← a DIFFERENT quantity

   Do not merge these. They will not reconcile.
```

### Advantages

- **Mutually exclusive, jointly exhaustive.** Every query lands in exactly one box. Percentages sum
  to 100 and are directly interpretable.
- **Localizes the fix.** High Lucky Guess → improve retriever coverage. High Information Blindness →
  refine the generation prompt. The paper supplies exactly these prescriptions.
- **Exposes the Adherence Paradox**, which no single-scalar metric can.
- **Correct Rejection is a first-class outcome**, not a failure. Very few metrics reward appropriate
  ignorance.

### Disadvantages

- **Requires ground truth** for the retrieval-success axis.
- **Two thresholds** (0.80 / 0.75 for relevance, 0.7 for adherence). Move them and the quadrants
  move. Report them.
- **LLM judge on the adherence axis** — inherits judge drift and judge cost.
- **Binary axes discard gradation.** A passage that is 0.69 adherent and one that is 0.01 adherent
  are both "NO".
- **Validated in one domain** (medical QA) so far.

### Domain examples

**Clinical decision support.** The origin domain. Lucky Guess is a *patient-safety* category here:
a clinically correct answer with no traceable source cannot be audited, defended, or corrected.

**Legal research.** Directly transferable. An unsupported-but-correct citation is arguably worse
than a wrong one, because it survives review.

**Consumer chat.** Lower stakes, and Lucky Guess may be acceptable. But you should still *know* the
number — if a third of your answers come from parametric memory, your retrieval system is doing
less work than your invoice suggests.

### Recommendation

**If you adopt one Alignment metric from this entire supplement, adopt CUE.** It subsumes the
diagnostic value of a faithfulness score while fixing faithfulness's central flaw, and its output
tells you which component to work on.

Report all four quadrants, never a single derived number. The whole point is the decomposition.

---

## A.3.2 MIRAGE's four metrics

**One-line:** Four mutually exhaustive metrics of RAG *adaptability*, computed by comparing model
behaviour across closed-book, oracle-context, and mixed-context conditions.

**Facets:** Alignment | query | ref | E2E | ◐ ✅
**Source:** Park, Moon, Park & Lim, **Findings of NAACL 2025**, pp. 2883–2900 ·
[arXiv:2504.17137](https://arxiv.org/abs/2504.17137)

> **Catalogue correction:** the companion catalogue lists this as "NAACL'25". It is *Findings of
> NAACL 2025*. Also note the name collision documented in the catalogue — four unrelated artefacts
> are called MIRAGE. Always pair the name with the arXiv ID.

### The construction, from the paper

Three experimental setups per question:

| Setup | Context given |
|---|---|
| **Base** | Closed-book — query only |
| **Oracle** | The correct context |
| **Mixed** | Correct *and* noisy contexts — the realistic case |

The dataset is 7,560 curated instances over a 37,800-entry retrieval pool drawn from IfQA,
NaturalQA, TriviaQA, DROP, and PopQA.

### The four metrics

```
   ┌─────────────────────────┬────────────────────────────────┐
   │ NOISE VULNERABILITY     │ susceptibility to noise in the │
   │                         │ context                        │
   ├─────────────────────────┼────────────────────────────────┤
   │ CONTEXT ACCEPTABILITY   │ ability to leverage provided   │
   │                         │ context for accurate answers   │
   ├─────────────────────────┼────────────────────────────────┤
   │ CONTEXT INSENSITIVITY   │ fails to utilise the context   │
   ├─────────────────────────┼────────────────────────────────┤
   │ CONTEXT MISINTERPRETATION│ uses context, gets it wrong   │
   └─────────────────────────┴────────────────────────────────┘
```

### The finding that makes this metric worth adopting

This is the part no abstract-level reading would give you, and it is the reason MIRAGE earns a place
beside CUE:

> **Noise Vulnerability and Context Acceptability change drastically with retriever performance.
> Context Insensitivity and Context Misinterpretation are consistent for a given model regardless of
> shots or retriever — they depend solely on the LLM's capabilities.**

```
   THE FOUR METRICS SPLIT INTO TWO DIAGNOSTIC HALVES
   ═════════════════════════════════════════════════

   ┌──────────────────────┐    ┌──────────────────────┐
   │  RETRIEVER-SENSITIVE │    │   LLM-INTRINSIC      │
   │                      │    │                      │
   │  Noise Vulnerability │    │ Context Insensitivity│
   │  Context Acceptability│   │ Context Misinterp.   │
   │                      │    │                      │
   │  ▲ change retriever  │    │  ▲ change MODEL      │
   │    to move these     │    │    to move these     │
   └──────────────────────┘    └──────────────────────┘

        o    "Context Insensitivity went up. New retriever?"
       /|\
       / \

        o    "That half doesn't move with the retriever.
       /|\     Something changed about your generator."
       / \
```

That is a genuine causal decomposition. Two of your four numbers tell you to work on retrieval; the
other two tell you to change models or prompts. Very few evaluation frameworks offer that.

The paper also notes this explains why overall performance does not reach perfect scores even in the
Oracle setting — the LLM-intrinsic failures persist when the context is *known correct*.

### Advantages

- **Mutually exhaustive**, like CUE — the four account for all behaviour.
- **Separates retriever-fixable from model-fixable failures.** The single most valuable property.
- **Efficient by design.** The 37,800-chunk pool is about 1% of a full wiki-dump, cutting
  computational cost while retaining relevance to large benchmarks like MTEB.
- **Public dataset and code**, so results are reproducible rather than described.

### Disadvantages

- **Wikipedia-domain benchmark.** Your domain is not Wikipedia. Findings transfer as *guidance*, not
  as *your numbers*.
- **Requires the oracle condition**, i.e. known-correct context — so it needs a labelled dataset,
  not live traffic.
- **Three inference runs per question** (Base / Oracle / Mixed), so 3× generation cost.
- **Noise is dichotomous, not graded.** A later critique notes MIRAGE does not permit granular
  control over noise levels, unlike RGB. If you need a noise *dose–response* curve, MIRAGE will not
  give you one.

### Domain examples

**Model selection for a RAG deployment.** The ideal use. Run MIRAGE across candidate LLMs; the
LLM-intrinsic half gives you a clean comparison uncontaminated by retriever choice.

**Retriever selection.** Equally valid, using the other half. This is the rare framework that
supports both decisions with one run.

**Domain-specific production monitoring.** Poor fit. Requires oracle labels and three runs per
question.

### Recommendation

Use MIRAGE as an **offline procurement instrument**, not a monitoring one. Before committing to a
retriever–LLM pair, run it and read the two halves separately. If Context Insensitivity is high on
your preferred model, no retrieval investment will fix it — that is the paper's central practical
message.

Pair with CUE: MIRAGE tells you *which component is weak in general*; CUE tells you *what is
happening on your actual traffic*.

---

# A.4 Family 4 — Machine-Utility Ranking

## A.4.1 UDCG — Utility and Distraction-aware Cumulative Gain

**One-line:** nDCG rebuilt for a reader that is a language model rather than a human — with a
learned positional discount and *negative* weight for distracting passages.

**Facets:** Alignment | passage | ref | R | ◐ ✅
**Source:** Trappolini et al., EACL 2026 · [arXiv:2510.21440](https://arxiv.org/abs/2510.21440)

### The two misalignments it identifies

The paper's argument against classical IR metrics in RAG is precise, and it is the cleanest
statement of the problem in the literature:

1. **Human vs. machine position discount.** nDCG, MAP, and MRR assume users examine documents
   sequentially with diminishing attention to lower ranks. LLMs process all retrieved documents *as
   a whole*, not sequentially.
2. **Human relevance vs. machine utility.** Classical metrics do not account for related-but-
   irrelevant documents that *actively degrade* generation quality rather than merely being ignored.

Point 2 is the deeper one. In classical IR, an irrelevant document at rank 5 costs you a slot. In
RAG, it can cost you the answer.

```
   THE SIGN PROBLEM
   ════════════════

   CLASSICAL IR:              RAG:
   relevance ∈ [0, 3]         utility ∈ [−?, +?]

   ┌──────────────┐           ┌──────────────┐
   │ irrelevant   │           │ distracting  │
   │   gain = 0   │           │  gain < 0    │
   │              │           │              │
   │ "costs you   │           │ "costs you   │
   │  a slot"     │           │  the ANSWER" │
   └──────────────┘           └──────────────┘

        o    "nDCG says this doc contributes zero."
       /|\
       / \

        o    "It contributes NEGATIVE. nDCG has no
       /|\     way to express that."
       / \
```

### The formula, as published

```
   UDCG_θ(q, C) = σ( Σᵢ₌₁ᵏ αᵢ uᵢ⁺  +  Σᵢ₌₁ᵏ βᵢ uᵢ⁻ )

   where
     uᵢ⁺, uᵢ⁻   positive and negative parts of passage utility uᵢ
     αᵢ, βᵢ      positional weights for relevance and distraction
     σ(x)        sigmoid, bounding the metric to [0,1]

   2k learnable parameters, fitted with a linear model on
   feature vectors [u₁⁺ … uₖ⁺, u₁⁻ … uₖ⁻] trained to predict
   end-to-end answer accuracy.
```

Note what that last clause means: **UDCG's positional discount is not assumed, it is learned from
your data to maximize correlation with answer accuracy.** nDCG's `1/log₂(i+1)` is a模型 of human
attention written down in 2002. UDCG's `αᵢ` is an empirical fact about your generator.

### Reported results

Across five datasets and six LLMs, UDCG improves correlation with end-to-end answer accuracy by up
to **36%** over traditional metrics.

### Advantages

- **Models distraction with a negative term** — structurally impossible in nDCG.
- **Learned position weights** reflect your actual generator, not a 20-year-old attention model.
- **Directly optimized for the thing you care about**: correlation with answer accuracy.
- **Bounded [0,1]** via sigmoid, so averaging across questions is well-behaved.

### Disadvantages

- **Requires utility annotations**, positive and negative — a new and more expensive annotation
  schema than binary or graded relevance.
- **2k learned parameters must be fit**, which needs end-to-end accuracy labels. You are training a
  metric.
- **Generator-specific and k-specific.** Change the LLM or change k and the weights are stale.
  Every UDCG number is implicitly conditioned on a model and a context size.
- **Not comparable across systems** unless they share the fitted weights — which undercuts the main
  reason people like nDCG.
- **Newest metric here**, with least independent replication.

### Domain examples

**A stable, long-lived production pipeline.** The best fit. If your generator and k are stable for
quarters at a time, fitting UDCG weights once is a sound investment and gives you the most
accuracy-predictive retrieval metric available.

**Rapid model iteration.** Poor fit. If you swap generators monthly, you are refitting the metric
monthly, and your time series is discontinuous each time.

**Academic benchmarking / leaderboards.** Problematic. Cross-system comparability is exactly what
learned per-system weights destroy. Use nDCG for the leaderboard and UDCG for your own engineering.

### Recommendation

Adopt UDCG when your generator is stable and you have the annotation budget for a
utility-with-distraction schema. Its value is not that it is a better number — it is that it is the
only ranking metric that can tell you a passage was **actively harmful**.

If you cannot afford it, the cheap approximation is: **stop reporting nDCG alone in RAG.** Report it
next to a distraction-sensitive measure — MIRAGE's Noise Vulnerability, or CUE's Lucky Guess rate —
so the negative contributions are visible somewhere.

### Failure mode

```
   THE STALE WEIGHTS

   Jan:  fit UDCG weights on Llama-3.1-8B, k=5
   Mar:  swap to Llama-4, keep the dashboard
   Jun:  "UDCG has been flat for two quarters"

        o    "Stable retrieval quality!"
       /|\
       / \

        o    "You're scoring a new generator with
       /|\     the old one's attention profile.
       / \     The number is measuring a model
              you no longer run."
```

---

# A.5 Alignment — the summary card

```
┌────────────────────────────────────────────────────────────────┐
│  ALIGNMENT: WHAT TO ACTUALLY PUT ON THE DASHBOARD              │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  PICK ONE contribution metric:                                 │
│     golden answers + offline  ──▶ ΔSePer                       │
│     golden answers + CI       ──▶ eRAG                         │
│     no golden answers         ──▶ DIG                          │
│                                                                │
│  PLUS one from each other family:                              │
│     attribution               ──▶ WARG                         │
│     quadrant diagnosis        ──▶ CUE  (or MIRAGE offline)     │
│     machine-utility ranking   ──▶ UDCG (if generator stable)   │
│                                                                │
├────────────────────────────────────────────────────────────────┤
│  THE THREE THINGS TO REMEMBER                                  │
│                                                                │
│  1. Never report faithfulness/adherence without a              │
│     retrieval-hit denominator beside it. (Adherence Paradox)   │
│                                                                │
│  2. Relevance and utility can point in OPPOSITE directions.    │
│     Two independent groups found this. (Preference Gap)        │
│                                                                │
│  3. On most queries the generator may not be using your        │
│     top-ranked document at all. Check before optimizing        │
│     rank. (47–67%, WARG)                                       │
└────────────────────────────────────────────────────────────────┘
```

---

# PART B — INTEGRITY / DRIFT

# B.1 What Integrity actually is

## B.1.1 The dimension

Every metric in Part A is computed at an instant. Integrity asks the only question that matters six
months later:

> **Does that instant still describe the system?**

This dimension is the least instrumented of the four, and the reason is structural: drift metrics
require a *baseline*, and baselines require that someone six months ago had the foresight to freeze
one. Most teams did not.

## B.1.2 The four drift types — and why conflating them is the standard error

```
   ═══════════════════════════════════════════════════════════
   TYPE          WHAT MOVES              DETECTED BY
   ═══════════════════════════════════════════════════════════
   CORPUS        documents change,       VersionQA-style
                 get revised, get        version-sensitive tests
                 superseded              (§B.3)
   ───────────────────────────────────────────────────────────
   REPRESENTATION you change embedder,   CKA / Jaccard /
                 vectors mean            RankSimilarity (§B.2)
                 something new
   ───────────────────────────────────────────────────────────
   QUERY         users ask about         per-class recall,
                 things that didn't      query robustness (§B.4)
                 exist at launch
   ───────────────────────────────────────────────────────────
   JUDGE         your LLM evaluator      NOTHING. This is the
                 silently updated        open problem. (§B.5)
   ═══════════════════════════════════════════════════════════
```

Each type has a different detector, and a metric built for one is blind to the others. A team
reporting "drift: green" almost always means *one* of these four.

---

# B.2 Representation Drift — the CKA family

**One-line:** Three complementary measures of whether two embedding models — or the same model at
two points in time — actually behave the same way.

**Facets:** Integrity/Drift | corpus & query | free | R | ◐ ✅
**Source:** Caspari, Dastidar, Zerhoudi, Mitrovic & Granitzer, *Beyond Benchmarks: Evaluating
Embedding Model Similarity for RAG Systems* · [arXiv:2407.08275](https://arxiv.org/abs/2407.08275)
🟡 Read at method-summary level via the Brehme survey's account plus the paper's abstract.

### Why this matters more than it sounds

Every practitioner blog on RAG drift recommends some version of "track mean cosine distance from a
baseline centroid, alert above 0.05." Those thresholds have **no published validation**. They are
folklore with a number attached.

This paper supplies the actual instruments.

### The three measures

```
   THREE QUESTIONS, THREE INSTRUMENTS
   ══════════════════════════════════

   1. CKA  (Centered Kernel Alignment)
      "Do these two embedders REPRESENT text similarly?"
      ── compares the representation geometry itself

   2. JACCARD
      "Do they RETRIEVE the same documents?"
      ── set overlap of results, order-blind

   3. RANKSIMILARITY
      "Do they retrieve them in the same ORDER?"
      ── rank-aware overlap of retrieved chunks


   ┌───────────┬──────────┬───────────────┬──────────────────┐
   │ CKA       │ Jaccard  │ RankSimilarity│ Interpretation   │
   ├───────────┼──────────┼───────────────┼──────────────────┤
   │ high      │ high     │ high          │ genuinely same   │
   │ LOW       │ high     │ high          │ different maths, │
   │           │          │               │ same behaviour — │
   │           │          │               │ safe to swap     │
   │ high      │ LOW      │ —             │ similar geometry,│
   │           │          │               │ divergent results│
   │           │          │               │ ⚠️ investigate    │
   │ high      │ high     │ LOW           │ same docs, new   │
   │           │          │               │ order — matters  │
   │           │          │               │ a lot for RAG    │
   └───────────┴──────────┴───────────────┴──────────────────┘
```

That third row is the one to internalize. Two embedders can be geometrically similar and
behaviourally different. Representation similarity does not imply retrieval similarity, which is
precisely why one number is insufficient.

### The two axes of application

```
   SAME INSTRUMENT, TWO COMPARISONS
   ════════════════════════════════

   ACROSS MODELS              ACROSS TIME
   (did the swap change       (did the corpus drift
    what surfaces?)            under a fixed embedder?)

   embedder A ──┐             corpus @ Jan ──┐
                ├── CKA                       ├── Jaccard
   embedder B ──┘             corpus @ Jun ──┘   RankSimilarity

   The paper's framing is the first.
   The second is the drift application, and it is
   a natural extension rather than a published result.
```

I flag that honestly: applying these to *temporal* drift rather than *cross-model* comparison is my
extrapolation from the paper's method, not a claim the authors make.

### Advantages

- **Published and validated**, unlike every centroid-distance heuristic in circulation.
- **Three-way decomposition is diagnostic**, not just an alarm.
- **Reference-free.** No labels needed — you are comparing two systems to each other.
- **Cheap.** No LLM calls.

### Disadvantages

- **CKA needs representation access.** Closed embedding APIs may not expose what you need.
- **No published thresholds.** The paper gives you instruments, not alert levels. You must
  establish your own baselines.
- **Comparative, not absolute.** These tell you *whether things changed*, never *whether things are
  good*. A consistently bad retriever scores perfectly stable.
- **Temporal application is unvalidated** (see flag above).

### Domain examples

**Any embedder migration.** This is the killer application. Before swapping `text-embedding-3-small`
for something newer, run all three. If Jaccard and RankSimilarity are high, the migration is low
risk regardless of what the leaderboards say. If they are low, you are shipping a different system.

**Regulated environments with change control.** These three numbers are exactly the evidence a
change-approval board needs and cannot currently get.

**Multilingual or multi-domain corpora.** Compute per-segment. Aggregate similarity can be high
while one language or one document class diverges completely.

### Recommendation

**Freeze a baseline today.** Pick 500 representative queries, record the top-k for each under your
current embedder, and store it. That artefact costs almost nothing and is the prerequisite for every
drift measurement you will ever want to make. Without it, in six months you will have no way to
answer "has this changed?" — which is the entire dimension.

Then run Jaccard and RankSimilarity against that baseline monthly, and CKA whenever you change
models.

### Failure mode

```
   THE MISSING BASELINE

   Month 1:  ship it
   Month 7:  "users say results got worse"
   Month 7:  "when did it change?"
             "what did it look like before?"
             "...we don't have that."

        o    "Can we measure the drift?"
       /|\
       / \

        o    "Drift is a comparison. You have one
       /|\     side of it."
       / \

   Cost of freezing a baseline: one afternoon.
   Cost of not having one: the entire dimension.
```

---

# B.3 Corpus & Version Drift — VersionQA

**One-line:** A benchmark of version-sensitive questions over evolving technical documentation,
measuring whether a system notices that a document *changed*.

**Facets:** Integrity/Drift | query | ref | E2E | ◐ ✅
**Source:** Huwiler, Stockinger & Fürst, *VersionRAG* · [arXiv:2510.08109](https://arxiv.org/abs/2510.08109)

### The construction

VersionQA is **100 manually curated questions across 34 versioned technical documents**, drawn from
Apache Spark changelogs (2.4.7–3.5.5), Bootstrap (5.2.3–5.3.5), and Node.js documentation for Assert
(11.15.0–23.11.0) and Errors (15.14.0–23.11.0).

**60% of queries require version-aware reasoning**, across six categories:

| Category | Pairs | Version-sensitive |
|---|---|---|
| Content Retrieval | 20 | No |
| Content Retrieval Complex | 20 | No |
| Content Retrieval Version-Specific | 20 | **Yes** |
| Version Listing & Inquiry | 20 | **Yes** |
| Change Retrieval (Explicit) | 10 | **Yes** |
| Change Retrieval (Implicit) | 10 | **Yes** |

### The results

```
   VERSION-SENSITIVE QUESTIONS
   ═══════════════════════════
   Naive RAG        58%   ███████████
   GraphRAG         64%   ████████████
   VersionRAG       90%   ██████████████████


   IMPLICIT CHANGE DETECTION
   (noticing an undocumented modification)
   ═══════════════════════════════════════
   Baselines      0–10%   ▏
   VersionRAG       60%   ████████████

        o    "Our RAG handles our docs fine."
       /|\
       / \

        o    "Can it tell you what changed between
       /|\     v2.1 and v2.2 without being told
       / \     a change occurred?"

        o    "...no."
       /|\
       / \    "Neither can anyone else's. 0-10%."
```

That 0–10% is the most alarming number in this entire supplement. Semantic similarity has no
temporal dimension: a superseded passage is *just as similar* to the query as its replacement, and
nothing in a standard vector retrieval pipeline prefers the current one.

Also worth noting for the Efficiency dimension: VersionRAG requires **97% fewer tokens during
indexing than GraphRAG**, which is the rare case of a robustness improvement that is also cheaper.

### Advantages

- **Measures something nothing else measures.** Implicit change detection is invisible to every
  metric in Part A.
- **Small and runnable.** 100 questions is a tractable benchmark to adapt to your own corpus.
- **Category breakdown is diagnostic** — you can see whether you fail on explicit or implicit
  changes.
- **Realistic corpus.** Software changelogs are genuinely versioned, not synthetically aged.

### Disadvantages

- **Domain-narrow.** Software documentation. Adapting it to legal, medical, or financial versioning
  is real work.
- **Small n.** 100 questions gives wide confidence intervals; treat differences under ~10 points
  cautiously.
- **Measures a benchmark, not your corpus.** The right use is as a *template*.
- **Version-aware architecture is the paper's actual product**; the benchmark is supporting
  evidence.

### Domain examples

**Regulated policy documentation.** SOPs, compliance manuals, clinical guidelines — all versioned,
all safety-critical when stale. If your RAG returns the superseded revision of a safety procedure,
the failure is invisible to every Correctness metric because the answer is *faithful to the
retrieved context*.

**Software/API documentation.** The origin domain. Directly applicable.

**News and current events.** The hardest case. Versioning is implicit and continuous rather than
discrete. VersionQA's method does not transfer cleanly; see §B.4's temporal work instead.

### Recommendation

**Build a 50-question version-sensitive set for your own corpus.** Use VersionQA's six-category
structure as the template. Weight it toward implicit change detection, since that is where every
baseline collapses.

Then run it quarterly. This is the only Integrity metric in this supplement that directly measures
the failure your users will actually notice.

---

# B.4 Robustness — the perturbation family

## B.4.1 Retrieval Robustness (three metrics)

**One-line:** Three metrics corresponding to three questions: is RAG always better than no-RAG, do
more documents always help, and does document order matter?

**Facets:** Integrity/Drift | system | free | E2E | ◐ ✅
**Source:** Cao et al. · [arXiv:2505.21870](https://arxiv.org/abs/2505.21870)
🟡 ABSTRACT-ONLY — the three metric definitions were not retrievable; the research questions and
headline finding are as stated.

### The construction

A benchmark of **1,500 open-domain questions**, each with documents retrieved from Wikipedia, tested
across **11 LLMs and 3 prompting strategies**. One robustness metric per research question:

```
   RQ1: Is RAG always better than non-RAG?
   RQ2: Do more retrieved documents always help?
   RQ3: Does document order affect results?

        o    "Obviously yes, yes, and no."
       /|\
       / \

        o    "All three are empirical questions with
       /|\     surprising answers. That's why the paper
       / \     exists."
```

### The headline finding

All 11 LLMs exhibited **surprisingly high retrieval robustness** — but differing degrees of
imperfect robustness still prevented them from fully realizing RAG's benefits.

That is a genuinely two-sided result and worth reporting honestly: the models are more robust than
the "Lost in the Middle" literature might lead you to expect, *and* the residual fragility is still
costing you.

### Advantages / Disadvantages

| Advantages | Disadvantages |
|---|---|
| Reference-free; needs no golden answers per query | 🟡 Metric definitions not obtained — cannot give formulas |
| Directly tests three decisions you actually make (use RAG? what k? what order?) | Wikipedia/open-domain; your domain may differ |
| Broad model coverage (11 LLMs) makes findings generalizable | Reports aggregate robustness, not per-query diagnosis |

### Recommendation

Run the **RQ1 test on your own system regardless of whether you adopt the metrics**: compare
RAG against no-RAG on a fixed question set. It is the single cheapest experiment in this supplement
and it answers the question nobody asks — *is the retrieval system earning its keep at all?*

Teams almost never run this after launch. If RAG-off performs within a few points of RAG-on on a
meaningful slice of your traffic, you have found either a routing opportunity or a serious problem.

## B.4.2 Query-level robustness under perturbation

**One-line:** Robustness measured per-query under input perturbation, rather than aggregated.

**Facets:** Integrity/Drift | query | free | E2E | ◐ ✅
**Source:** Perçin et al., GEM 2025 · [arXiv:2507.06956](https://arxiv.org/abs/2507.06956)
🟡 ABSTRACT-ONLY.

The complement to B.4.1: same concern, finer unit. Aggregate robustness can be high while a specific
query class is catastrophically fragile — and query classes map onto user segments, which map onto
customers.

**Recommendation:** if you adopt one robustness measure, prefer the query-level one and segment it
by query class. An aggregate robustness score is the kind of number that stays green while a
specific customer's use case breaks.

## B.4.3 Temporal freshness — Latest@10

**One-line:** Whether a recency prior actually surfaces the freshest relevant item.

**Facets:** Integrity/Drift | query | ref | R | ◐ ✅
**Source:** [arXiv:2509.19376](https://arxiv.org/abs/2509.19376) 🟡 ABSTRACT-ONLY.

### Why it's here: a citable negative result

The paper tests a recency prior on three corpora of increasing realism, and the honest finding is
that **freshness via a recency prior is real but partial and parameter-sensitive — not solved.**

The specifics are instructive:

- Synthetic stream: Latest@10 = 1.00, but the authors themselves call this a sanity check, since
  near-identical intra-topic embeddings reduce the task to a recency sort
- CERT logon corpus (849,579 events): 1.00 **only with a corpus-tuned recency weight** — and
  **0.00** at the synthetic-tuned default
- NVD CVE descriptions: 0.00 → 0.60, beating a semantic-then-newest baseline at 0.20

```
   THE PARAMETER CLIFF

   recency weight tuned on corpus A  ──▶ Latest@10 = 1.00 on A
   same weight applied to corpus B   ──▶ Latest@10 = 0.00 on B

        o    "We enabled the recency prior."
       /|\
       / \

        o    "With whose tuning?"
       /|\
       / \
```

A metric that goes from 1.00 to 0.00 based on a hyperparameter transferred between corpora is not a
metric you can adopt from a blog post.

The paper also reports that labelling weekly clusters as growth/drift/decay scored only **0.08
macro-F1** with a fixed-threshold rule — rising to 0.49 when the labelling rule was fixed and 0.96
with clustering noise removed. The failure was localized to the *labelling rule*, not the clusterer.

**Recommendation:** cite this when someone proposes a recency-weighting heuristic. It is the
strongest published evidence that the obvious fix does not straightforwardly work.

---

# B.5 The open problem — judge drift

There is no metric for this. That is the finding.

```
   THE INVISIBLE DRIFT
   ═══════════════════

   Your faithfulness score:  0.87 ──── 0.87 ──── 0.87 ──── 0.87
                             Jan       Mar       Jun       Sep
                                        ▲
                                        │
                              judge model silently
                              updated here

   Nothing on the dashboard changed colour.
   Every comparison across that line is void.

        o    "Faithfulness has been stable all year."
       /|\
       / \

        o    "Faithfulness has been measured by two
       /|\     different instruments all year."
       / \
```

### The evidence

The Brehme, Ströhle & Breu systematic review of 63 RAG-evaluation papers
([arXiv:2504.20119](https://arxiv.org/abs/2504.20119)) states the problem directly: rapid LLM
development means advances in models could render previous evaluation results invalid, since a new
model might produce entirely different outcomes — leaving open how to adapt prior results and
establish a standard evaluation framework that remains consistent and independent of specific LLM
versions.

The same review supplies the number that makes this urgent: of the 63 papers, **41 used LLMs as
judges and only six compared LLM judges against human judges.** Those six found a positive
correlation, which is a weak bar. The review also flags the circularity: it is unresolved whether
evaluation quality is compromised when an LLM generates questions, answers them, and evaluates its
own output.

### The interim protocol

Until someone publishes a metric, do this:

```
   ┌──────────────────────────────────────────────────┐
   │  JUDGE DRIFT PROTOCOL (no published metric yet)  │
   │                                                  │
   │  1. PIN the judge model version. Explicitly.     │
   │     Not "gpt-4o" — the dated snapshot.           │
   │                                                  │
   │  2. FREEZE an anchor set: 100–200 items with     │
   │     human labels.                                │
   │                                                  │
   │  3. On EVERY judge change, re-run the anchor     │
   │     set. Record judge–human agreement            │
   │     (Krippendorff's α, not κ — you'll have       │
   │     more than two raters).                       │
   │                                                  │
   │  4. If α moves materially, your historical       │
   │     series is broken. Say so in the report       │
   │     rather than letting the line continue.       │
   │                                                  │
   │  5. NEVER let the same model generate synthetic  │
   │     test data AND judge the results.             │
   └──────────────────────────────────────────────────┘
```

Step 5 is the one most commonly violated, usually unknowingly, by teams using one framework for both
synthetic test generation and evaluation.

---

# B.6 Integrity — the summary card

```
┌────────────────────────────────────────────────────────────────┐
│  INTEGRITY / DRIFT: WHAT TO ACTUALLY DO                        │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  THIS WEEK (costs one afternoon, unlocks everything):          │
│    ▸ Freeze a baseline: 500 queries, top-k results, stored     │
│    ▸ Pin your judge model to a dated snapshot                  │
│    ▸ Freeze a 100-item human-labelled anchor set               │
│                                                                │
│  THIS QUARTER:                                                 │
│    ▸ Jaccard + RankSimilarity vs. baseline (monthly)           │
│    ▸ CKA on any embedder change                                │
│    ▸ 50-question version-sensitive set, VersionQA template     │
│    ▸ RAG-vs-no-RAG comparison (the test nobody runs)           │
│                                                                │
│  ACCEPT AS UNSOLVED:                                           │
│    ▸ Judge drift — no metric exists; use the protocol          │
│    ▸ Recency weighting — published evidence says it does       │
│      not transfer between corpora (1.00 → 0.00)                │
│                                                                │
├────────────────────────────────────────────────────────────────┤
│  THE ONE NUMBER TO FEAR                                        │
│  Implicit change detection: baselines score 0–10%.             │
│  If your corpus is versioned, your system almost certainly     │
│  cannot tell you that a document changed.                      │
└────────────────────────────────────────────────────────────────┘
```

---

# Appendix A — Sourcing ledger for this supplement

| Metric | Read at | Formula/algorithm obtained? |
|---|---|---|
| eRAG | Abstract + method framing | Conceptual, not symbolic |
| DIG | Abstract + method statement | Conceptual (confidence differencing) |
| ΔSePer | **Algorithm 1, verbatim** | ✅ Full algorithm + both variants |
| Gain | Abstract + framing 🟡 | No |
| WARG | Paper body (intro + RQ2) | Method named (IG + PMCSHAP), formula no |
| CUE | **Paper §III-B, verbatim** | ✅ Full construction + thresholds |
| MIRAGE ×4 | Paper body + repo + results discussion | Definitions + the diagnostic split |
| UDCG | **Paper §5, formula verbatim** | ✅ UDCG_θ equation |
| CKA family | Survey account + abstract 🟡 | Instruments named, formulas no |
| VersionQA | Paper body (Tables 2 & 3) | ✅ Dataset composition + results |
| Retrieval Robustness | Abstract only 🟡 | No — three metrics not defined |
| Query robustness | Abstract only 🟡 | No |
| Latest@10 | Abstract only 🟡 | Results yes, formula no |

Entries marked 🟡 should be re-read before this supplement is treated as final. I have described
them at the level I actually obtained, rather than inferring detail I did not read.

# Appendix B — Corrections issued by this supplement

1. **SePer is reference-based.** A widely-circulated summary claims it needs no ground truth.
   Algorithm 1 requires the reference answer `a*`. The summary is wrong.
2. **MIRAGE venue** — *Findings of* NAACL 2025, pp. 2883–2900, not the main conference.
3. **RAG-X's 14% gap** is Accuracy (71%) − Context Hit Rate (57.6%), not
   Accuracy − Effective Use (21.8%). These are different quantities.
4. **Four metrics, one measurement** — eRAG, Gain, DIG, ΔSePer are one family. Reporting all four
   is not corroboration.
