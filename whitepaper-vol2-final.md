# Measuring Retrieval

## Volume II — The RAG Era
### Final Installment: Chapters 13–15
#### Meta-Evaluation · Judge Reliability · The Narrowing Exercise

---

**Citation status.** Two of the three outstanding 🟡 entries are lifted to ✅ in Appendix 5A
(Trust-Score components; GainRAG method). One remains 🟡 and is stated as such.

**What this document is for.** Everything before it described metrics. This one answers two
questions that determine whether any of it works:

1. **Can you trust the thing doing the measuring?** (Chapters 13–14)
2. **Which eight metrics should you actually instrument?** (Chapter 15)

Chapter 15 is the one to read if you read only one chapter in this entire white paper.

---

# Chapter 13 — Can You Trust Your Judge?

## 13.0 The dependency nobody audits

Most modern RAG metrics — faithfulness, context relevance, CUE's adherence axis, answer
correctness — are computed by an LLM. That LLM is a measuring instrument, and no other instrument in
your stack is deployed with so little calibration.

```
   THE UNAUDITED INSTRUMENT
   ════════════════════════

   ┌────────────────────────────────────────────┐
   │  Your thermometer:  calibrated, certified, │
   │                     traceable              │
   │                                            │
   │  Your scale:        calibrated annually    │
   │                                            │
   │  Your LLM judge:    "gpt-4o"               │
   └────────────────────────────────────────────┘

        o    "It correlates well with humans."
       /|\
       / \

        o    "On whose data? At what agreement?
       /|\     Which snapshot? When did you last
       / \     check?"
```

## 13.1 The empirical picture

**Source:** Brehme, Ströhle & Breu, *Can LLMs Be Trusted for Evaluating RAG Systems? A Survey of
Methods and Datasets*, **SDS 2025** · [arXiv:2504.20119](https://arxiv.org/abs/2504.20119) ✅

Across a systematic review of **63 papers**:

| Finding | Number |
|---|---|
| Papers using LLMs as judges | **41** |
| Papers comparing LLM judges against human judges | **6** |
| Result in those six | A *positive correlation* |

```
   41 USED. 6 CHECKED.
   ═══════════════════

   ████████████████████████████████████████  41 used LLM judges
   ██████                                     6 validated against humans

        o    "Six studies found positive correlation.
       /|\     That's reassuring."
       / \

        o    "'Positive correlation' is the weakest
       /|\     possible finding. r = 0.3 is a positive
       / \     correlation. The survey's own conclusion
              is that LLMs can be trusted 'to some
              extent' and their validity 'remains to be
              thoroughly established.'"
```

The review also names the circularity directly: it is unresolved whether evaluation quality is
compromised when an LLM generates the questions, answers them, and then evaluates its own output.

**If your pipeline uses one framework for both synthetic test generation and judging, you are inside
that loop.**

## 13.2 A concrete ceiling on general-purpose judging

SURE-RAG (Supplement B §C.9) provides a hard number that is worth quoting whenever someone proposes
GPT-as-judge for a specialized task:

| Verifier | Macro-F1 |
|---|---|
| **Purpose-built calibrated verifier** | **0.9075** |
| Strong concat cross-encoder | 0.8888 ± 0.0109 |
| **GPT-4o as judge** | **0.7284** |
| DeBERTa mean-pooling | 0.6516 |

```
   THE GAP
   ═══════

   purpose-built  ██████████████████  0.91
   cross-encoder  █████████████████   0.89
   GPT-4o judge   ██████████████      0.73
   DeBERTa pool   █████████████       0.65

        o    "GPT-4o is state of the art."
       /|\
       / \

        o    "At generating. As a VERIFIER on a
       /|\     specific task, a purpose-built model
       / \     beat it by 18 points. General
              capability is not measurement
              capability."
```

## 13.3 The four judge biases to test for

None of these is unique to RAG; all of them contaminate RAG metrics.

```
   ┌────────────────────┬────────────────────────────────┐
   │ BIAS               │ HOW TO TEST                    │
   ├────────────────────┼────────────────────────────────┤
   │ POSITION           │ Swap A/B order; re-score.      │
   │ prefers whichever  │ Disagreement rate IS the bias. │
   │ came first         │                                │
   ├────────────────────┼────────────────────────────────┤
   │ VERBOSITY          │ Score matched-content pairs at │
   │ prefers longer     │ two lengths. Any systematic    │
   │ answers            │ preference is bias.            │
   ├────────────────────┼────────────────────────────────┤
   │ SELF-PREFERENCE    │ Have judge X score outputs from│
   │ prefers its own    │ X and from Y. Compare against  │
   │ family's outputs   │ human ranking.                 │
   ├────────────────────┼────────────────────────────────┤
   │ VERSION DRIFT      │ Frozen anchor set, re-run on   │
   │ silently changes   │ every judge change. See §13.5. │
   │ over time          │                                │
   └────────────────────┴────────────────────────────────┘
```

**Position bias has the cheapest test and is almost never run.** Swap the order of two candidate
answers and re-score. If the verdict flips more than a few percent of the time, your pairwise judge
results are partly noise.

## 13.4 Use α, not κ

A small technical point with real consequences.

```
   COHEN'S κ vs KRIPPENDORFF'S α
   ═════════════════════════════

   Cohen's κ:        exactly TWO raters, nominal data
   Krippendorff's α: ANY number of raters, handles
                     missing data, works on nominal /
                     ordinal / interval scales

   Your setup: 1 LLM judge + 2 human annotators,
               and the humans didn't both label
               everything.

        o    "We'll report Cohen's kappa."
       /|\
       / \

        o    "You have three raters and incomplete
       /|\     overlap. κ can't represent that.
       / \     Use α."
```

Volume I §6.3.2 established the underlying point from the classical literature: assessor
disagreement leaves *system rankings* surprisingly stable while *absolute scores* move. Trust your
relative comparisons more than your absolute numbers — and that guidance applies with more force,
not less, when the assessor is a language model.

## 13.5 The judge-drift protocol

There is still no published metric for judge drift. This is the interim procedure, restated as a
standing operating requirement rather than a suggestion.

```
   ┌──────────────────────────────────────────────────────┐
   │  JUDGE DRIFT PROTOCOL                                │
   │                                                      │
   │  1. PIN the dated snapshot. Not "gpt-4o" —            │
   │     the version string.                              │
   │                                                      │
   │  2. FREEZE an anchor set: 100–200 items with          │
   │     human labels. Never regenerate it.                │
   │                                                      │
   │  3. ON EVERY JUDGE CHANGE, re-run the anchor set     │
   │     and record Krippendorff's α.                      │
   │                                                      │
   │  4. IF α MOVES MATERIALLY: your historical series    │
   │     is broken. Draw a vertical line on the chart      │
   │     and say so. Do not let the line continue.         │
   │                                                      │
   │  5. NEVER let one model generate synthetic test      │
   │     data AND judge results.                           │
   │                                                      │
   │  6. RECORD the judge version in every experiment     │
   │     record, beside the embedder version.              │
   └──────────────────────────────────────────────────────┘
```

Step 4 is the one teams resist, because it makes a dashboard look broken. The dashboard *is* broken;
the line was already meaningless.

---

# Chapter 14 — Is Your Test Set Any Good?

## 14.0 The layer below the metrics

Chapter 13 asked whether the judge is trustworthy. Chapter 14 asks whether the *questions* are.

A perfect metric computed by a perfect judge over an inadequate test set tells you nothing. And test
sets fail in ways that are invisible from inside them.

```
   FOUR WAYS A TEST SET LIES
   ═════════════════════════

   1. COVERAGE GAP    ── whole regions of the corpus
                         are never queried
   2. LEAKAGE         ── the answers are in the model's
                         training data
   3. NO DIVERSITY    ── 200 questions, one template
   4. PRIVACY LEAK    ── synthetic questions carry
                         real sensitive content

        o    "Our eval set has 500 questions."
       /|\
       / \

        o    "Covering what fraction of your corpus?"
       /|\
       / \

        o    "...I don't know how to answer that."
       /|\
       / \   "That's what §14.1 is for."
```

## 14.1 Semantic Test Coverage

**One-line:** Embed document chunks and test questions in one vector space, then quantify how much
of the corpus your questions actually reach.

**Facets:** Integrity/Drift | corpus | free | R | ◐ ✅
**Source:** [arXiv:2510.00001](https://arxiv.org/abs/2510.00001)

### The construction

The paper's framing of the gap is precise: current practice lacks a systematic method to ensure test
sets adequately cover the underlying knowledge base, leaving developers with **significant blind
spots**.

The method embeds document chunks and test questions into a unified vector space and computes three
coverage metrics — **basic proximity, content-weighted coverage, and multi-topic question
coverage** — plus outlier detection to filter irrelevant questions and refine the set.

```
   COVERAGE IN EMBEDDING SPACE
   ═══════════════════════════

   ·  = document chunk
   ○  = test question

   ┌─────────────────────────────────────────┐
   │   ○·· ·                                 │
   │  ·○···                    · · ·         │
   │   ·· ○                   · · · ·        │
   │  ·  ·                     · · ·         │
   │        ○·                  ▲            │
   │       ··                   │            │
   │                    ┌───────┴─────────┐  │
   │                    │ UNCOVERED REGION│  │
   │                    │ no question ever │  │
   │                    │ goes here        │  │
   │                    └─────────────────┘  │
   └─────────────────────────────────────────┘

        o    "Our eval passes at 91%."
       /|\
       / \

        o    "On the region your questions reach.
       /|\     That cluster on the right has never
       / \     been tested. It could be anything."
```

### Advantages / Disadvantages

| Advantages | Disadvantages |
|---|---|
| Answers a question nothing else answers | Coverage in *embedding* space, not semantic space — inherits your embedder's blind spots |
| Reference-free; needs no labels | Uncovered ≠ important; some regions deserve no questions |
| Actionable — points at where to write new questions | Depends on chunking choices |
| Outlier detection prunes bad questions too | ◐ single paper, limited replication |

### Recommendation

**Run this once, today, on your existing eval set.** It is cheap — embeddings you already have plus
clustering — and it almost always reveals a region of your corpus nobody has tested. That finding
alone usually justifies the afternoon.

Then use it as a *generation* target: write questions for the uncovered clusters rather than adding
more questions to the crowded ones.

## 14.2 Leakage and contamination

**Source:** *Generating Leakage-Free Benchmarks for Robust RAG Evaluation* ·
[arXiv:2605.08838](https://arxiv.org/abs/2605.08838) ✅

The problem, and it is severe: if your test question's answer is in the model's training data, the
model can answer it **without retrieval**. Your RAG evaluation is then measuring parametric memory
wearing a retrieval costume.

```
   THE LEAKAGE TRAP
   ════════════════

   Question: "What is the capital of Switzerland?"
   Retrieval: returns nothing useful
   Answer: "Bern"  ✓ CORRECT

   Your metrics:
     accuracy      ✓ high
     faithfulness  ✓ high (nothing contradicts it)
     Lucky Guess   ← the ONLY metric that catches this

        o    "Our RAG scores 89% on our benchmark."
       /|\
       / \

        o    "What does it score with retrieval
       /|\     DISABLED?"
       / \

        o    "...86%."
       /|\
       / \   "Then your retrieval is worth three
              points and your benchmark is leaked."
```

**The diagnostic is trivial and almost nobody runs it: score your benchmark with retrieval turned
off.** The gap between RAG-on and RAG-off is the most honest single number about whether your
retrieval earns its keep. It is also Cao et al.'s RQ1 (Supplement A Addendum §AD.1), so you get a
robustness metric for free.

This connects directly to the Brehme survey's observation that widely-used public datasets —
HotpotQA, Natural Questions, MS MARCO — are built on **publicly available knowledge**, which
presents a challenge because the RAG system becomes redundant when the LLM has already been trained
on that knowledge.

## 14.3 Synthetic test-set quality

**Source:** Driouich et al., *Diverse And Private Synthetic Datasets Generation for RAG evaluation:
A multi-agent framework*, **TRUST-AI@ECAI 2025** · [arXiv:2508.18929](https://arxiv.org/abs/2508.18929) ✅

Two axes that pull against each other:

```
   THE SYNTHETIC DATA TENSION
   ══════════════════════════

   DIVERSITY ◀───────────────────▶ PRIVACY

   more varied questions           less risk of
   = better coverage               reproducing real
                                   sensitive content

   Generate from your real corpus  ── high diversity,
                                      privacy risk
   Generate from templates         ── safe, low diversity
```

**BenchmarkQED** (Microsoft Research) is the tooling counterpart: **AutoQ** synthesizes queries
across a local-to-global spectrum, **AutoE** evaluates answers on relevance, comprehensiveness,
diversity, and empowerment, and **AutoD** curates datasets. ⚠️ It is *software*, not a paper —
cite it as a tool.

## 14.4 The open gap

```
   ┌──────────────────────────────────────────────────┐
   │  STILL MISSING: MUTATION KILL RATE FOR RAG       │
   │                                                  │
   │  In software testing, you deliberately inject    │
   │  bugs and measure what fraction your test suite  │
   │  catches. That's mutation testing.               │
   │                                                  │
   │  The RAG analogue would be: corrupt the corpus   │
   │  in known ways — swap a date, negate a claim,    │
   │  delete a passage — and measure what fraction    │
   │  of corruptions your eval set detects.           │
   │                                                  │
   │  Nobody has published this. It is the most       │
   │  obvious missing instrument in RAG evaluation.   │
   │                                                  │
   │  VersionRAG's implicit change detection          │
   │  (0–10% baseline) is the closest existing work.  │
   └──────────────────────────────────────────────────┘
```

If you want a research contribution rather than a dashboard, this is the gap.

---

# Chapter 15 — The Narrowing Exercise

## 15.0 Seventy metrics down to eight

Everything so far has been a catalogue. This chapter is the answer to "so what do I actually
instrument?"

The governing principle, from Volume I's conclusion: **a dashboard with one strong metric per
dimension beats a dashboard with nine metrics from one dimension.** Nine correlated metrics moving
together feel like corroboration and are a single measurement wearing nine hats.

## 15.1 The decision tree

```
   START: WHAT KIND OF SYSTEM DO YOU HAVE?
   ═══════════════════════════════════════

   ┌─ Do you have golden answers?
   │
   ├── NO ──▶ REFERENCE-FREE TRACK
   │          Correctness:  RAGAS faithfulness (3-metric form)
   │          Alignment:    DIG  ·or·  WARG
   │          Integrity:    RBO vs frozen baseline
   │          Efficiency:   Pairwise Redundancy + TTFT p95
   │          ⚠️ Add: RAG-off comparison (leakage check)
   │
   └── YES ─▶ Do you ship citations to users?
              │
              ├── YES ──▶ ATTRIBUTION TRACK
              │           Correctness: RAGChecker (CR, SK, HL)
              │                      + ALCE citation precision
              │           Alignment:   CUE quadrants
              │           Integrity:   RBO + version-sensitive set
              │           Efficiency:  tokens/query + EHR@k
              │
              └── NO ───▶ Is retrieval single-shot or agentic?
                          │
                          ├── SINGLE ──▶ CORE TRACK  (§15.2)
                          │
                          └── AGENTIC ─▶ CORE TRACK
                                       + retrieval calls/answer
                                       + redundant-query rate
                                       ⚠️ largely uninstrumented
                                          territory
```

## 15.2 The Core Track — the eight-metric starter kit

For a typical reference-based, single-shot RAG system:

```
┌──────────────────────────────────────────────────────────────────┐
│  THE EIGHT                                                       │
├───┬──────────────────────────┬──────────────┬────────────────────┤
│ # │ METRIC                   │ DIMENSION    │ WHY THIS ONE       │
├───┼──────────────────────────┼──────────────┼────────────────────┤
│ 1 │ Claim Recall             │ Correctness  │ ceiling on all     │
│   │ (RAGChecker)             │              │ downstream quality │
├───┼──────────────────────────┼──────────────┼────────────────────┤
│ 2 │ Self-Knowledge           │ Correctness  │ the Lucky Guess    │
│   │ (RAGChecker)             │              │ rate. Nothing else │
│   │                          │              │ measures it.       │
├───┼──────────────────────────┼──────────────┼────────────────────┤
│ 3 │ Hallucination            │ Correctness  │ the classic        │
│   │ (RAGChecker)             │              │ failure            │
├───┼──────────────────────────┼──────────────┼────────────────────┤
│ 4 │ nDCG@k  (k = injected)   │ Correctness  │ continuity +       │
│   │                          │              │ comparability      │
├───┼──────────────────────────┼──────────────┼────────────────────┤
│ 5 │ One contribution metric  │ Alignment    │ pick ONE: eRAG /   │
│   │                          │              │ DIG / ΔSePer       │
├───┼──────────────────────────┼──────────────┼────────────────────┤
│ 6 │ RBO vs frozen baseline   │ Integrity    │ cheapest real      │
│   │                          │              │ drift metric       │
├───┼──────────────────────────┼──────────────┼────────────────────┤
│ 7 │ Pairwise Redundancy      │ Efficiency   │ reveals quality    │
│   │                          │              │ waste, label-free  │
├───┼──────────────────────────┼──────────────┼────────────────────┤
│ 8 │ TTFT p50 / p95           │ Efficiency   │ the latency users  │
│   │                          │              │ actually feel      │
└───┴──────────────────────────┴──────────────┴────────────────────┘

   PLUS TWO NON-NEGOTIABLE CONTEXT LINES:

   ▸ Average claim count per response
     (else hallucination-rate improvements are just brevity)

   ▸ RAG-on vs RAG-off accuracy
     (else you don't know if retrieval earns its keep)
```

## 15.3 What NOT to instrument

Equally important, and rarely said:

```
   ┌──────────────────────────────────────────────────────┐
   │  LEAVE THESE OFF THE DASHBOARD                       │
   │                                                      │
   │  ✗ More than one contribution metric                 │
   │    eRAG, Gain, DIG, ΔSePer are one family            │
   │                                                      │
   │  ✗ Faithfulness without Claim Recall beside it       │
   │    the Adherence Paradox. Three papers. Enough.      │
   │                                                      │
   │  ✗ An averaged composite "RAG score"                 │
   │    cross-unit aggregation destroys the diagnosis     │
   │                                                      │
   │  ✗ CTR / abandonment as QUALITY measures             │
   │    eight absolute metrics tested in 2008; none       │
   │    reliably reflected quality. Keep for monitoring.  │
   │                                                      │
   │  ✗ nDCG at retrieval depth when you inject fewer     │
   │    measure what the generator SEES                   │
   │                                                      │
   │  ✗ Mean cosine similarity of retrieved chunks        │
   │    a signal, not a metric (Vol I Ch 3)               │
   └──────────────────────────────────────────────────────┘
```

## 15.4 The 90-day rollout

Sequenced by cost and dependency, not by importance.

```
   WEEK 1 — FREE, AND UNLOCKS EVERYTHING
   ═════════════════════════════════════
   □ Freeze a baseline: 500 queries + top-k, stamped with
     embedder version and k
   □ Pin the judge model to a dated snapshot
   □ Freeze a 100-item human-labelled anchor set
   □ Time a full index rebuild. Write the number down.
   □ Trace your ACTUAL injected k (not retrieved k)

   WEEK 2–4 — THE CHEAP DIAGNOSTICS
   ════════════════════════════════
   □ RAG-on vs RAG-off on your benchmark   ← do this first
   □ Semantic test coverage of your eval set
   □ Pairwise Redundancy at current k
   □ MAP vs bpref gap (judgment-distortion estimate)
   □ Position-bias test on your judge (swap A/B, re-score)

   MONTH 2 — THE k-SWEEP
   ═════════════════════
   □ k ∈ {1,3,5,10,20,50} × {recall, quality, redundancy,
     tokens, TTFT}
   □ Plot quality vs tokens. Find the knee. Set k there.

   MONTH 3 — THE DIAGNOSTIC LAYER
   ══════════════════════════════
   □ RAGChecker full nine, offline; promote three
   □ CUE quadrants on a sample
   □ WARG once — is the generator even using your ranking?
   □ Build a 50-question version-sensitive set

   ONGOING
   ═══════
   □ Monthly: RBO vs baseline
   □ Per release: the expensive diagnostics
   □ Per judge change: anchor set + Krippendorff's α
   □ Per embedder change: Jaccard + RankSimilarity at your k
```

**Week 1 is the highest-leverage work in this entire white paper**, and none of it requires a metric
at all. It is pure instrumentation. Teams that skip it discover six months later that they cannot
answer "has this changed?" — which forecloses the entire Integrity dimension permanently.

## 15.5 The three findings to carry into every design review

```
   ┌──────────────────────────────────────────────────────────┐
   │  1. FAITHFULNESS NEVER SHIPS ALONE                       │
   │                                                          │
   │  RAG-X: adherence 0.84, and 33.9% of correct answers     │
   │  ungrounded. Three independent papers named this:        │
   │  Lucky Guess, Self-Knowledge, post-rationalization.      │
   │  Always print a retrieval-hit denominator beside it.     │
   ├──────────────────────────────────────────────────────────┤
   │  2. RELEVANCE AND UTILITY CAN POINT OPPOSITE WAYS        │
   │                                                          │
   │  Cuconasu et al. and Jiang et al., independently:        │
   │  highly relevant passages can interfere with reasoning;  │
   │  tangential ones can help. Your relevance labels do      │
   │  not describe what the model needs.                      │
   ├──────────────────────────────────────────────────────────┤
   │  3. YOUR GENERATOR MAY IGNORE YOUR RANKING               │
   │                                                          │
   │  RAG-E: on 47–67% of queries the generator ignored the   │
   │  retriever's top-ranked document. Run WARG BEFORE you    │
   │  spend a quarter improving nDCG.                         │
   └──────────────────────────────────────────────────────────┘
```

---

# Closing: What This White Paper Argues

Across eight documents and roughly 130 verified citations, one claim runs underneath everything:

> **Evaluation is not a reporting activity. It is a design activity.**

Clarke et al. put it most sharply in 2008 — evaluation measures act as objective functions to be
optimized. Whatever you measure, your system will be shaped toward. Whatever you *fail* to measure,
it will be free to sacrifice.

That is why redundancy reached 22% in a production medical RAG pipeline in 2026. Not because anyone
chose it. Because nobody measured it, and the reranker optimized what it was scored on.

```
        o    "So the metrics ARE the system design."
       /|\
       / \

        o    "The metrics are the only part of the
       /|\     design that you can still change after
       / \     you've shipped. Choose them like it
              matters."
```

## The honest limits of this document set

| Limit | Detail |
|---|---|
| **One 🟡 remains** | Perçin et al. query-level robustness — method not obtained |
| **Two of my own errors** | AIS venue; CKA interpretation. Both from describing unread work |
| **The mutation-kill-rate gap** | Named, not solved |
| **Judge drift has no metric** | Only a protocol |
| **Online RAG evaluation** | You can interleave sources, not generated answers. No good published answer |
| **Multi-turn RAG** | Session is the right unit; almost everything reports per-turn |

---

# Appendix 5A — Final 🟡 resolution

## Trust-Score — components, now specified ✅

**Source:** Song, Sim, Bhardwaj, Chieu, Majumder & Poria, ICLR 2025 **Oral** ·
[arXiv:2409.11242](https://arxiv.org/abs/2409.11242)

Trust-Score is a composite over **three dimensions**: response truthfulness, factual accuracy, and
attribution groundedness.

```
   TRUST-SCORE STRUCTURE
   ═════════════════════

   RESPONSE TRUTHFULNESS
   ├── F1_GR  Grounded Refusal (macro-avg of two F1s)
   │     ├── F1_ref : correctly REFUSING unanswerable Qs
   │     │     P_ref = |¬A_r ∩ ¬A_g| / |¬A_r|
   │     │     R_ref = |¬A_r ∩ ¬A_g| / |¬A_g|
   │     └── F1_ans : correctly ANSWERING answerable Qs
   │
   └── F1_AC  answer-calibrated Answer Correctness

   ATTRIBUTION GROUNDEDNESS
   ├── R_cite  Citation Recall     ┐ adopted directly
   └── P_cite  Citation Precision  ┘ from ALCE (Gao et al.)

   where A_g / ¬A_g = ground-truth answerable / unanswerable
         A_r / ¬A_r = model answered / refused
```

**The design property that matters:** by penalizing both incorrect refusals and incorrect
non-refusals, F1_GR gives a balanced evaluation of the model's **over-responsiveness and
under-responsiveness**. That is exactly the abstention-quality measurement Supplement B §C.7 said
was missing — it was there, inside the composite, all along.

**The lineage worth noting:** Trust-Score's attribution half *is* ALCE's citation precision and
recall. Supplement B §C.5 and §C.7 describe two halves of one measurement tradition.

Benchmark composition, for calibration: ASQA (610 answerable / 338 unanswerable), QAMPARI (295/705),
ELI5 (207/793). Note how unanswerable-heavy QAMPARI and ELI5 are — which is why refusal handling
dominates the score there.

## GainRAG — method, now specified ✅

**Source:** Jiang, Zhao, Li, Wang & Qin, *GainRAG: Preference Alignment in Retrieval-Augmented
Generation through Gain Signal Synthesis*, **ACL 2025 Long Papers**, Vienna ·
[arXiv:2505.18710](https://arxiv.org/abs/2505.18710)

The full title resolves the ambiguity: this is **gain signal synthesis**, not gain measurement.

Method: estimate gain signals, then train a **middleware selector** that predicts which passages
provide positive generation gain — overcoming naive relevance by aligning retriever output with
generator benefit. A **pseudo-passage strategy** mitigates degradation. Trained on a small subset of
HotpotQA and WebQuestions; generalizes across 6 datasets. Baselines: StandardRAG, Self-RAG, and
BGE-Reranker-base, all at top-1.

**Confirms the §A.2.4 warning.** Gain is a training signal for a selector. Reporting it as a metric
on a system trained with it is circular. Use a held-out generator, or better, report something else.

## Perçin et al. — remains 🟡

*Investigating the Robustness of Retrieval-Augmented Generation at the Query Level*, GEM 2025 ·
[arXiv:2507.06956](https://arxiv.org/abs/2507.06956). Existence and title verified ✅; **metric
definitions not obtained.** Described in Supplement A §B.4.2 at abstract level only, and left that
way.

---

# Appendix 5B — Master document index

| # | Document | Covers |
|---|---|---|
| 0 | `ir-rag-metrics-catalogue-v2.md` | Complete indexed catalogue; 4 verification passes |
| 1 | `whitepaper-vol1-part1.md` | Ch 0–4: dimensions, facets, signals, set metrics |
| 2 | `whitepaper-vol1-part2.md` | Ch 5–7: rank metrics, incomplete judgments, rank comparison |
| 3 | `whitepaper-vol1-part3.md` | Ch 8–10: diversity, fairness, online/counterfactual |
| 4 | `whitepaper-vol1-part4.md` | Ch 11–12 + Vol I conclusion: significance, efficiency, time |
| 5 | `whitepaper-supplement-A.md` | Alignment; Integrity/Drift |
| 6 | `whitepaper-supplement-A-addendum.md` | 🟡 lifts; CKA correction |
| 7 | `whitepaper-supplement-B.md` | Correctness/Grounding; Efficiency/Cost |
| 8 | **`whitepaper-vol2-final.md`** | **Ch 13–15: meta-eval, judges, narrowing** |

## Where to start, by reader

| If you are... | Read |
|---|---|
| Deciding what to instrument tomorrow | **Ch 15** (this doc) |
| Debugging a RAG system that "should work" | Supplement A §A.3 (CUE, MIRAGE) |
| Choosing a retriever or embedder | Supplement A §B.2 + the Addendum correction |
| Choosing a generator | Supplement B §C.7 + Supplement A §A.3.2 |
| Building an eval set from scratch | Ch 14, then Vol I Ch 6 |
| Writing a paper | Vol I Ch 11 |
| Learning the field properly | Vol I in order, then the supplements |

## Correction log — final

| # | Correction | Whose |
|---|---|---|
| 1 | AIS is *Computational Linguistics* 49(4), not TACL | **Mine** |
| 2 | SePer is reference-based; popular summary says otherwise | Third party |
| 3 | MIRAGE is *Findings of* NAACL 2025 | Catalogue |
| 4 | RAG-X's 14% gap = Accuracy − Context Hit Rate | User framing |
| 5 | eRAG/Gain/DIG/ΔSePer are one family | Catalogue structure |
| 6 | RAGAS paper ≠ RAGAS library | Field-wide |
| 7 | SURE-RAG is not a hallucination detector | Catalogue |
| 8 | PEER and DUO are fairness metrics | Catalogue |
| 9 | CKA similarity ≠ retrieval similarity at small k | **Mine** |

**Nine corrections. Two mine. Zero across 54 classical citations; nine across the RAG-era material.**

That distribution is the last finding, and it is a practical one: **verify anything from the last
two years before you build on it.** The old literature has been checked by many people. The new
literature — and especially its secondary summaries — has not.
