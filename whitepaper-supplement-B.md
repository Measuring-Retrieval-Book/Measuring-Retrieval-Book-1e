# Measuring Retrieval — Supplement B

## Two Dimensions, Read From Source
### CORRECTNESS / GROUNDING and EFFICIENCY / COST

---

**Companion to:** Supplement A (Alignment, Integrity/Drift) and Volume I Installment 1.
**Sourcing standard:** metrics described after reading the paper's method section. Entries where I
obtained only the abstract are marked 🟡 ABSTRACT-ONLY. Discrepancies between papers and the
libraries that implement them are flagged explicitly — there is a significant one in §C.3.

---

# PART C — CORRECTNESS / GROUNDING

# C.1 Correctness means something different in RAG

## C.1.1 The shift

Volume I Chapter 4 treated Correctness as a property of a *retrieved set*: was this document
relevant, yes or no. RAG breaks that framing in two ways.

```
   WHAT "CORRECT" USED TO MEAN vs WHAT IT MEANS NOW
   ════════════════════════════════════════════════

   CLASSICAL IR                  RAG
   ────────────                  ───
   unit: document                unit: CLAIM
   question: relevant?           question: supported? by WHAT?
   binary                        three-way at minimum
   one judgment per doc          one judgment per atomic assertion

        o    "The answer is correct."
       /|\
       / \

        o    "Which parts of it? Supported by which
       /|\     passage? And would it still be correct
       / \     if you removed the retrieval?"
```

**Shift 1 — the unit dropped to the claim.** A paragraph-long answer contains a dozen assertions.
Some are supported by the context, some come from the model's weights, some are wrong. A single
response-level score averages these into meaninglessness.

**Shift 2 — correctness split from groundedness.** These are now two independent axes, and the
central insight of this supplement is that **a system can be high on one and low on the other in
either direction.**

## C.1.2 The two-axis picture

```
                       IS IT GROUNDED IN CONTEXT?
                       YES                 NO
                 ┌──────────────────┬──────────────────┐
      CORRECT    │  what you want   │  "Lucky Guess"   │
                 │                  │  (RAG-X)         │
                 │  supported and   │  "Self-Knowledge"│
                 │  right           │  (RAGChecker)    │
                 │                  │  ⚠️ unauditable   │
                 ├──────────────────┼──────────────────┤
      INCORRECT  │  "Noise          │  "Hallucination" │
                 │   Sensitivity"   │                  │
                 │  (RAGChecker)    │  the classic     │
                 │                  │  failure         │
                 │  faithfully      │                  │
                 │  wrong           │                  │
                 └──────────────────┴──────────────────┘
```

Three of those four boxes are failures, and **only one of them is what people mean when they say
"hallucination."** The top-right box — correct but ungrounded — is the one that survives every
review process, because the answer is right and nobody checks where it came from.

Note the convergence: RAG-X calls the top-right *Lucky Guess*, RAGChecker calls it *Self-Knowledge*.
Independently derived, same box.

---

# C.2 The claim-decomposition family

## C.2.0 The shared machinery

Nearly every modern grounding metric runs the same three-step pipeline:

```
   THE DECOMPOSITION PIPELINE
   ══════════════════════════

   1. EXTRACT      answer ──▶ list of atomic claims
                   (an LLM rewrites the answer into
                    standalone, fully-understandable statements)

   2. VERIFY       each claim ──▶ entailed by X? (NLI or LLM judge)
                   where X ∈ {context, ground truth, each chunk}

   3. AGGREGATE    count ──▶ ratio


        ┌─────────────────────────────────────┐
        │ "Bern has been the capital since    │
        │  1848 and has 133,000 residents."   │
        └─────────────────────────────────────┘
                        │ EXTRACT
                        ▼
        ┌─────────────────────────────────────┐
        │ c₁: Bern is the capital             │
        │ c₂: Bern became capital in 1848     │
        │ c₃: Bern has 133,000 residents      │
        └─────────────────────────────────────┘
                        │ VERIFY against context
                        ▼
                 c₁ ✓   c₂ ✓   c₃ ✗
                        │
                 faithfulness = 2/3 = 0.67
```

**The critical property:** what you verify *against* determines which metric you get. Same
extraction, same verifier, different reference text:

| Verify claims against... | You get |
|---|---|
| Retrieved context | Faithfulness |
| Ground-truth answer | Precision / Correctness |
| Each retrieved chunk individually | Context Precision, Noise Sensitivity |
| Nothing (claims *missing* from answer) | Recall |

This is why one framework can produce nine metrics from one extraction pass. It is also why those
nine metrics are cheaper together than separately — a point most teams miss when budgeting.

## C.2.1 FActScore — the ancestor

**One-line:** Decompose a long-form generation into atomic facts and score the precision of those
facts against a knowledge source.

**Facets:** Correctness | claim | judge | G | ⬤ ✅
**Source:** Min et al., EMNLP'23 · [arXiv:2305.14251](https://arxiv.org/abs/2305.14251)
🟡 Read at title/abstract level — *FActScore: Fine-grained Atomic Evaluation of Factual Precision in
Long Form Text Generation*.

FActScore is here for lineage rather than adoption. It established atomic-fact decomposition as the
unit of factuality evaluation, and every metric in §C.3–C.5 is a descendant. **It measures precision
only** — RAGChecker's Claim Recall is the recall counterpart that arrived later.

**Recommendation:** cite it as the origin; deploy a RAG-specific descendant instead.

---

# C.3 RAGAS

**One-line:** Reference-free evaluation of RAG on three axes: is the answer grounded, does it answer
the question, and was the context relevant?

**Facets:** Correctness | claim | free/judge | E2E | ⬤ ✅
**Source:** Es, James, Espinosa-Anke & Schockaert, **EACL 2024 System Demonstrations, pp. 150–158**,
doi 10.18653/v1/2024.eacl-demo.16 · [arXiv:2309.15217](https://arxiv.org/abs/2309.15217)

## C.3.1 ⚠️ Paper-versus-library drift — read this before citing RAGAS

The paper defines **three** components: Faithfulness, Answer Relevance, and Context Relevance.

The library, as commonly used and documented, reports **four**: faithfulness, answer relevancy,
**context precision**, and **context recall** — with `context relevance` largely superseded.

```
   THE CITATION TRAP
   ═════════════════

   PAPER (2309.15217)          LIBRARY (what you run)
   ──────────────────          ──────────────────────
   Faithfulness                faithfulness
   Answer Relevance            answer_relevancy
   Context Relevance           context_precision
                               context_recall
                               (+ answer_correctness, ...)

        o    "We evaluated with RAGAS (Es et al., 2024)."
       /|\
       / \

        o    "Which four metrics did you report?"
       /|\
       / \

        o    "Faithfulness, answer relevancy, context
       /|\     precision, context recall."
       / \

        o    "Two of those aren't in the paper you cited.
       /|\     And context_recall isn't reference-free,
       / \     so your 'reference-free evaluation' claim
              is wrong too."
```

**Two consequences that matter:**

1. **Citing the paper does not describe your setup.** If you report context_recall, cite the library
   version, not just the paper.
2. **The reference-free claim breaks.** The paper's selling point is evaluation *without ground
   truth annotations*. Context Recall requires a reference answer. The moment you add it, RAGAS is
   no longer reference-free — and the main reason you chose it has evaporated.

## C.3.2 How the metrics are computed

**Faithfulness.** Statement generation (an LLM rewrites the answer into standalone atomic
statements), then NLI verification of each statement against the retrieved context, then
`score = supported statements / total statements`.

**Answer Relevance.** Computed by an inversion: generate synthetic questions *from the answer*, then
measure similarity to the original question. A relevant answer should reproduce a similar question.

```
   ANSWER RELEVANCE RUNS BACKWARDS
   ═══════════════════════════════

   original q:  "What is the capital of Switzerland?"
                            │
   answer:      "Bern is the capital."
                            │ generate questions FROM the answer
                            ▼
   synthetic:   "What is the capital of Switzerland?"
                "Which city is Switzerland's capital?"
                            │ cosine similarity to original
                            ▼
                        HIGH → relevant


   Off-topic answer:  "Switzerland has 26 cantons."
                            │
   synthetic:   "How many cantons does Switzerland have?"
                            │
                        LOW → not relevant
```

This is clever and has a specific blind spot: it measures *topicality*, not correctness. A
confidently wrong answer to the right question scores high on Answer Relevance.

## C.3.3 Advantages

- **Reference-free in its paper form.** The genuine differentiator, and the reason it dominates CI
  adoption.
- **Cheap and fast** relative to human evaluation.
- **Component-separated** — faithfulness targets the generator, context relevance the retriever.
- **Ubiquitous.** Enormous ecosystem, integrations everywhere, easy for a new engineer to run.

## C.3.4 Disadvantages

- **Heuristic prompts that do not transfer.** This is the most substantive published criticism: the
  ARES authors note that RAGAS's carefully designed heuristic scoring prompts often fail to adapt
  when applied to new domains or corpora. If your domain is far from the prompts' assumptions, the
  scores degrade in ways you will not see.
- **Faithfulness ≠ correctness.** A faithfulness of 0.8 means 20% of statements are unsupported —
  but it says nothing about whether the supported 80% are *right*. Faithful-to-wrong-context scores
  perfectly.
- **A hallucination-rate proxy, not a severity measure.** 0.8 faithfulness where the unsupported
  20% happens to contain the refund amount or the dosage is not the same as 0.8 where it contains
  pleasantries.
- **Averaging four metrics into a "RAGAS Overall" is common and bad.** Some implementations report
  the arithmetic mean of context precision, context recall, faithfulness, and answer relevance.
  These have different units of analysis (Facet A, Volume I §2.1) and averaging them is exactly the
  cross-unit aggregation Volume I warns against.
- **LLM-judge dependency** — inherits all of Supplement A §B.5's judge-drift exposure.

## C.3.5 Domain examples

**Startup / early-stage RAG.** The right first choice. Reference-free means you can measure
something on day one without an annotation budget, and "something" beats "nothing" decisively.

**Regulated enterprise.** Insufficient alone. Faithfulness without a retrieval-hit denominator
reproduces exactly the Adherence Paradox from Supplement A §A.3.1. Pair with CUE or RAGChecker's
Self-Knowledge.

**Specialized technical domains** (semiconductors, clinical coding, tax law). Highest risk of the
prompt-transfer problem. Validate RAGAS scores against a small human-labelled set *in your domain*
before trusting the aggregate. If agreement is poor, the framework is not broken — it is
out-of-domain.

## C.3.6 Recommendation

Use RAGAS as your **entry-level, always-on CI metric**, in its paper-faithful three-metric form,
and be precise about which version you cite.

The moment you add context_recall you have crossed into reference-based evaluation. That is a fine
choice — but make it deliberately, and at that point compare against RAGChecker, which does
reference-based claim-level diagnosis far more thoroughly.

**Never report a single averaged "RAGAS score."** The decomposition is the value.

---

# C.4 RAGChecker — the nine-metric diagnostic

**One-line:** Claim-level entailment checking that produces overall, retriever, and generator
metrics from a single extraction pass.

**Facets:** Correctness + Alignment | claim & chunk | ref + judge | E2E | ⬤ ✅
**Source:** Ru et al., **NeurIPS 2024 Datasets & Benchmarks Track** ·
[arXiv:2408.08067](https://arxiv.org/abs/2408.08067)

## C.4.1 The full metric set, as defined

RAGChecker processes query, retrieved context, response, and ground-truth answer, and emits three
groups. Definitions below are the paper's, as reproduced in a downstream benchmark that restates
them formally:

### Overall (needs response + ground truth only — no context required)

| Metric | Definition |
|---|---|
| **Precision** | Proportion of correct claims in the response |
| **Recall** | Proportion of ground-truth claims mentioned in the response |
| **F1** | Harmonic mean |

### Retriever

| Metric | Definition |
|---|---|
| **Claim Recall (CR)** | Proportion of ground-truth claims covered by the retrieved chunks |
| **Context Precision (CP)** | `|{r-chunk}| / k` — where a chunk is an *r-chunk* if **any** ground-truth claim is entailed in it |

### Generator

| Metric | Definition |
|---|---|
| **Faithfulness (FT)** | Proportion of response claims entailed by retrieved chunks — **regardless of correctness** |
| **Self-Knowledge (SK)** | Proportion of **correct** response claims **not** entailed by retrieved context |
| **Context Utilization (CU)** | Ratio of correct response claims supported by retrieved chunks, to total relevant ground-truth claims entailed by retrieved chunks |
| **Hallucination (HL)** | Proportion of incorrect claims entailed by **neither** the ground-truth answer **nor** any retrieved chunk |
| **Relevant Noise Sensitivity NS(I)** | Proportion of incorrect response claims entailed by **relevant** chunks |
| **Irrelevant Noise Sensitivity NS(II)** | Proportion of incorrect response claims entailed by **irrelevant** chunks |

## C.4.2 The design detail worth understanding

**Context Precision is defined at chunk level, not claim level, and this is deliberate.** The
paper's reasoning: a chunk contains multiple pieces of information at once, so the best possible
retriever can only achieve a claim-level precision score *lower than 100%*, and that upper bound
varies with the text. A metric whose ceiling moves with your corpus is not a usable metric — hence
the chunk-level definition.

```
   WHY CHUNK-LEVEL PRECISION
   ═════════════════════════

   A 1,024-token chunk contains:
   ┌────────────────────────────────────┐
   │ ✓ the fact you need                │
   │ · four sentences of context        │
   │ · a tangential aside               │
   │ · a table caption                  │
   └────────────────────────────────────┘

   CLAIM-LEVEL precision: ~1/8 = 0.125
                          ...even for a PERFECT retriever

        o    "Our context precision is 0.12."
       /|\
       / \

        o    "That's the ceiling, not your score.
       /|\     Chunks contain more than the answer.
       / \     That's what chunks ARE."
```

## C.4.3 The trilemma — the paper's most useful finding

> **The trilemma of context utilization, noise sensitivity, and faithfulness makes it difficult to
> improve all aspects simultaneously.**

```
              CONTEXT UTILIZATION
                      ▲
                     ╱ ╲
                    ╱   ╲
                   ╱     ╲
                  ╱       ╲
                 ╱  pick   ╲
                ╱    two    ╲
               ╱             ╲
              ▼───────────────▼
      NOISE               FAITHFULNESS
   SENSITIVITY↓

        o    "We'll optimize all three."
       /|\
       / \

        o    "The paper says you can't. Prioritize in
       /|\     the prompt based on your targets, your
       / \     users, and your generator's capability."
```

The paper also gives concrete tuning direction, which is unusually actionable:

| Goal | Chunk strategy |
|---|---|
| Better **context precision** | Larger chunks, fewer of them |
| Better **context utilization** / lower **noise sensitivity** | The opposite — smaller, more numerous |
| Better **recall / F1** | Moderately increase number and size — but the effect **saturates**, since total relevant information is fixed |

And a measured effect: faithfulness rose 88.1 → 92.2 as k went 5 → 20. More context made the
generator *more* faithful — the opposite of the common intuition that more context invites drift.

## C.4.4 Advantages

- **Nine metrics from one extraction pass.** Far cheaper than nine separate evaluations.
- **The only framework here that separates faithfulness from correctness by construction.** FT is
  explicitly "regardless of correctness." That honesty is rare and valuable.
- **Self-Knowledge is the Lucky Guess detector.** Correct claims not entailed by context — the
  dangerous top-right quadrant of §C.1.2, measured directly.
- **Two-way noise sensitivity** distinguishes "misled by good chunks" from "misled by bad chunks,"
  which have different fixes.
- **Actionable tuning guidance** published alongside.
- **Open implementation** (`amazon-science/RAGChecker`), so results are reproducible.

## C.4.5 Disadvantages

- **Reference-based.** Requires ground-truth answers throughout. No golden answers, no RAGChecker.
- **Expensive.** Claim extraction plus entailment checking across response × context × ground truth.
  Reference implementations use 70B-class models for both extractor and checker.
- **Two LLM dependencies** (extractor and checker), each independently subject to version drift.
- **Nine numbers is a lot of dashboard.** Teams report all nine and read none. See §C.4.6.
- **Claim extraction quality is an unmeasured upstream dependency.** If the extractor splits an
  answer badly, every downstream metric inherits the error, and nothing in the framework surfaces
  that.

## C.4.6 Recommendation

Run the full nine offline. **Promote three to your dashboard:**

```
   ┌───────────────────────────────────────────────┐
   │  THE THREE THAT EARN DASHBOARD SPACE          │
   │                                               │
   │  Claim Recall     ── did retrieval get it?    │
   │                      (the ceiling on all      │
   │                       downstream quality)     │
   │                                               │
   │  Self-Knowledge   ── the Lucky Guess rate.    │
   │                      Correct but ungrounded.  │
   │                      Nobody else measures     │
   │                      this and it is the       │
   │                      most dangerous box.      │
   │                                               │
   │  Hallucination    ── wrong AND unsupported.   │
   │                      The classic failure.     │
   │                                               │
   │  Keep the other six for diagnosis when one    │
   │  of these three moves.                        │
   └───────────────────────────────────────────────┘
```

**Do not put Faithfulness on the dashboard without Claim Recall beside it.** This is the third time
this supplement pair has made that point, and it is the single most repeated failure in RAG
evaluation.

---

# C.5 ALCE — citation precision and recall

**One-line:** Does the cited evidence actually support the sentence, and is every citation
*necessary*?

**Facets:** Correctness | claim | ref | G | ⬤ ✅
**Source:** Gao, Yen, Yu & Chen, **EMNLP 2023, pp. 6465–6488** ·
[arXiv:2305.14627](https://arxiv.org/abs/2305.14627)

## C.5.1 The three axes

ALCE assesses responses on **citation quality, correctness, and fluency**. Correctness checks
whether the generated answer entails the gold reference according to the NLI model TRUE.

## C.5.2 How citation precision actually works — the leave-one-out trick

This is the mechanism worth knowing, because it is genuinely clever and widely misunderstood:

```
   CITATION RECALL
   ═══════════════
   Does the CONCATENATION of cited documents entail the sentence?

   sentence: "Bern became the capital in 1848."
   cited:    [1] [2] [3]

   concat([1],[2],[3]) ──entails?──▶ YES  → recall credit


   CITATION PRECISION — the leave-one-out test
   ═══════════════════════════════════════════
   For EACH cited document, remove it and re-test entailment.

   remove [1]:  concat([2],[3]) ──entails?──▶ YES
                    ▲
                    └── then [1] was UNNECESSARY.
                        Precision penalty.

   remove [2]:  concat([1],[3]) ──entails?──▶ NO
                    ▲
                    └── [2] was load-bearing. Good citation.


        o    "I'll cite everything to be safe."
       /|\
       / \

        o    "Every unnecessary citation costs you
       /|\     precision. ALCE was built to catch
       / \     exactly that padding."
```

**This is the anti-shotgun-citation metric.** A model that cites all five retrieved chunks for every
sentence will score perfect recall and terrible precision.

## C.5.3 Advantages

- **Precision genuinely measures citation *necessity*,** not just presence. Very few metrics do.
- **Reproducible by design** — the paper's stated motivation was that prior work relied on
  commercial search engines and human evaluation, making comparison impossible.
- **Three genuinely distinct axes.** Fluency separated from correctness separated from attribution.
- **Three datasets** (ASQA, QAMPARI, ELI5) covering short-form, list, and long-form answers.

## C.5.4 Disadvantages

- **Computationally infeasible for multi-source inference at scale.** The leave-one-out test is
  combinatorial in the number of citations per sentence; a downstream multimodal paper flags exactly
  this as ALCE's blocking limitation.
- **Reference-based.** Needs gold answers.
- **NLI model dependency** (TRUE) — another pinned-version obligation.
- **Sentence-level granularity.** A sentence containing two facts with one citation is scored as a
  unit.

## C.5.5 Domain examples

**Anything with a regulatory citation obligation.** Legal briefs, medical literature reviews,
financial research notes. Citation precision is the metric that catches the "cite everything"
defensive behaviour that makes outputs unreviewable.

**Consumer search summaries.** Recall matters more than precision here — users want to know the
claim is backed, and rarely audit whether each link was load-bearing.

**High-citation-density technical writing.** Watch the cost. If your sentences average six
citations, the leave-one-out test is six entailment calls per sentence.

## C.5.6 Recommendation

Use ALCE's **precision** notion specifically if your product shows citations to users. Recall alone
rewards padding, and padded citations destroy user trust faster than missing ones — a user who
clicks a citation and finds it irrelevant stops clicking citations.

If full leave-one-out is too expensive, approximate: sample sentences rather than testing all, and
cap the test at sentences with ≤3 citations.

---

# C.6 Citation correctness ≠ citation faithfulness

**One-line:** A citation can be *correct* — the document does support the claim — while the model
never actually used that document. The citation was attached afterward.

**Facets:** Correctness | claim | judge | G | ◐ ✅
**Source:** Wallat, Heuss, de Rijke & Anand · [arXiv:2412.18004](https://arxiv.org/abs/2412.18004)

## C.6.1 Post-rationalization

The paper's contribution is to disentangle two notions that prior work applied inconsistently:

- **Citation correctness** — does the cited document support the statement?
- **Citation faithfulness** — is the model's reliance on the cited document *genuine*, reflecting
  actual reference use rather than superficial alignment with prior beliefs?

They name the failure **post-rationalization**: the model produces an answer from parametric memory,
then attaches a citation that happens to support it.

```
   POST-RATIONALIZATION
   ════════════════════

   WHAT YOU THINK HAPPENED        WHAT ACTUALLY HAPPENED
   ───────────────────────        ──────────────────────
   read doc [2]                   answer from memory
        ↓                              ↓
   form answer                    search retrieved docs for
        ↓                         one that agrees
   cite [2]                            ↓
                                  cite it

   Citation correctness: ✓ PASSES both times.
   The document really does support the claim.

        o    "Our citation accuracy is 94%."
       /|\
       / \

        o    "Up to 57% of citations in the systems
       /|\     studied were unfaithful. Correctness
       / \     cannot see this."
```

**Reported: current attributed answers often lack citation faithfulness — up to 57% of citations.**

## C.6.2 Why this is the same phenomenon as the Adherence Paradox

Notice the convergence across three independent papers:

| Paper | Name | Finding |
|---|---|---|
| RAG-X | Lucky Guess / Adherence Paradox | 33.9% correct-but-ungrounded; adherence 0.84 |
| RAGChecker | Self-Knowledge | Correct claims not entailed by context |
| Wallat et al. | Post-rationalization | Up to 57% of citations unfaithful |

Three research groups, three vocabularies, **one failure mode**: the system looks grounded and is
not. If you take one thing from Supplement B, take this.

## C.6.3 Recommendation

If you ship citations, measure faithfulness, not only correctness. The cheapest approximation is a
**counterfactual check on a sample**: remove the cited document, re-run, and see whether the answer
changes. If it does not, the citation was decorative.

This is the same ablation logic as Supplement A's contribution family — applied to citations rather
than to passages.

---

# C.7 Trust-Score

**One-line:** A holistic measure of whether an LLM is *appropriate for the RAG task*, including
whether it correctly refuses.

**Facets:** Correctness | claim | ref | G | ⬤ ✅
**Source:** Song, Sim, Bhardwaj, Chieu, Majumder & Poria, **ICLR 2025 Oral** ·
[arXiv:2409.11242](https://arxiv.org/abs/2409.11242)

## C.7.1 What it adds

Trust-Score's framing gap: plenty of work evaluates end-to-end RAG quality, but little addresses
whether a given LLM is *appropriate* for the RAG task at all. The paired method, Trust-Align,
improves models against it.

The finding that matters for metric selection: prompting methods such as in-context learning **fail
to effectively adapt LLMs to the RAG task** as measured by Trust-Score. Aligned models substantially
outperform baselines across ASQA, QAMPARI, and ELI5 — and critically, Trust-Align enhances models'
ability to **correctly refuse** as well as to provide quality citations.

## C.7.2 Why this closes a gap nothing else does

```
   THE METRIC THAT REWARDS SAYING "I DON'T KNOW"
   ═════════════════════════════════════════════

   Almost every metric in this supplement pair
   scores what the model SAID.

   Trust-Score scores whether it should have
   said anything at all.

   ┌──────────────────────────────────────┐
   │ context insufficient                 │
   │ model answers anyway   ──▶ penalized │
   │ model refuses          ──▶ REWARDED  │
   └──────────────────────────────────────┘

        o    "Refusal rate is a product metric,
       /|\     not a quality metric."
       / \

        o    "In RAG it's both. An answer with no
       /|\     evidence behind it is a defect that
       / \     happens to be well-formed."
```

**The complication**, from Supplement A's reading of *Sufficient Context* (arXiv:2411.06037):
models **abstain less** once RAG is added, and hallucinate more than they abstain. Retrieval
actively suppresses the behaviour Trust-Score rewards. That makes Trust-Score more necessary, not
less.

## C.7.3 Advantages / Disadvantages

| Advantages | Disadvantages |
|---|---|
| Scores refusal as a first-class outcome | Reference-based |
| ICLR Oral; strong empirical validation across 27 models | Single operating point, not a coverage–risk curve |
| Paired alignment method, so it is actionable | Tied to the ALCE-style datasets it was validated on |
| Isolates *model suitability* from retriever quality | Composite score — decompose before acting |

## C.7.4 Recommendation

Use Trust-Score at **model-selection time**, alongside MIRAGE's LLM-intrinsic half (Supplement A
§A.3.2). Both answer "is this model right for RAG?" from different angles — MIRAGE via context
utilization failures, Trust-Score via grounded attribution and refusal.

For production, what you actually want is a **coverage–risk curve**: plot accuracy-among-answered
against fraction-answered as you sweep the abstention threshold. Trust-Score gives you one point on
that curve. The curve is more useful and nobody publishes it, so you will have to build it.

---

# C.8 TriFEX, PKP, and PR — the metric that audits other metrics

**One-line:** Attributes each generated claim to its origin — query, context, or reference — and
isolates genuinely internalized knowledge from prompt leakage.

**Facets:** Correctness | claim | human-validated | G | ◐ ✅
**Source:** Oestreich, Bley, Binder, Müller, Sydorenko & Alcalde ·
[arXiv:2603.23047](https://arxiv.org/abs/2603.23047)

## C.8.1 The construction

**TriFEX** is a human-validated, triple-based evaluation pipeline that attributes generated claims
to their origin — user query, context, or reference. **PKP (Parametric Knowledge Precision)**
isolates internalized knowledge by filtering out claims leaked in the prompt.

```
   CLAIM ORIGIN ATTRIBUTION
   ════════════════════════

   generated claim ──┬──▶ was it in the QUERY?      → leaked
                     ├──▶ was it in the CONTEXT?    → retrieved
                     └──▶ neither?                  → parametric

   PKP scores only the third bucket, for correctness.
   PR (Parametric Rate) counts how OFTEN the third
   bucket is used.
```

## C.8.2 The finding that should change how you read every other metric

The paper demonstrates that an existing knowledge-internalization metric is **retrieval-sensitive**,
with about **75% of its cross-condition variance driven by changes in the rate at which internal
knowledge is expressed (PR), rather than by changes in its actual correctness (PKP).**

```
   THE VARIANCE DECOMPOSITION
   ══════════════════════════

   You observe:  metric moved from 0.61 → 0.74
   You conclude: "the model got better"

   Actual decomposition:
     ~75% ──▶ PR moved (model expressed internal
               knowledge more OFTEN)
     ~25% ──▶ PKP moved (that knowledge got more
               CORRECT)

        o    "So three quarters of our improvement was..."
       /|\
       / \

        o    "...a change in behaviour frequency,
       /|\     not a change in quality. The metric
       / \     conflated them."
```

The paper also reports that **ROUGE and BERTScore fail to detect factual differences** that the
triple-based evaluation reveals — a direct warning against surface-similarity metrics in RAG.

## C.8.3 Generalizing the lesson: the metric confounding audit

This finding is not really about PKP. It is a **general method** you should apply to any composite
metric before trusting a cross-condition comparison:

```
   ┌────────────────────────────────────────────────┐
   │  METRIC CONFOUNDING AUDIT                      │
   │                                                │
   │  Before reporting that metric M improved:      │
   │                                                │
   │  1. Can M be decomposed into a RATE term and   │
   │     a QUALITY term?                            │
   │                                                │
   │  2. If yes — decompose the variance.           │
   │                                                │
   │  3. If most movement is in the rate term,      │
   │     you have measured a behaviour change,      │
   │     not a quality change.                      │
   │                                                │
   │  Candidates in this supplement:                │
   │    Self-Knowledge (rate of use × correctness)  │
   │    Faithfulness   (claim count × support rate) │
   │    Hallucination  (verbosity × error rate)     │
   └────────────────────────────────────────────────┘
```

Note the last one especially. **Hallucination rate is a proportion, so a model that says less will
score better without becoming more truthful.** RAGChecker reports average number of response claims
alongside its metrics for exactly this reason — and most teams drop that column.

## C.8.4 Recommendation

You will probably not adopt PKP — it is domain-specific to electronic design automation. Adopt the
**method**: decompose any rate-times-quality metric before reporting a change, and always report
claim counts alongside claim-proportion metrics.

---

# C.9 SURE-RAG — sufficiency as a set property

**One-line:** Three-way evidence sufficiency (supports / refutes / insufficient) computed over the
retrieved *set*, not passage by passage.

**Facets:** Correctness | passage-set | ref | E2E | ◐ ✅
**Source:** Qiu, Han & Huang · [arXiv:2605.03534](https://arxiv.org/abs/2605.03534)

## C.9.1 The core argument

> **Relevance does not guarantee sufficiency: a topical passage may still fail to justify the
> answer.**

SURE-RAG treats evidence sufficiency as a **set-level property**, because missing hops and
unresolved conflicts cannot be detected by scoring passages independently. A shared claim–evidence
verifier produces a local relation distribution per (claim, passage) pair, which SURE-RAG aggregates
into four answer-level feature blocks — coverage, relation strength, uncertainty, and retrieval —
producing a three-way decision and an auditable selective score.

```
   WHY SET-LEVEL MATTERS
   ═════════════════════

   PASSAGE-BY-PASSAGE SCORING:
     p₁: relevant ✓    p₂: relevant ✓    p₃: relevant ✓
     verdict: great retrieval

   SET-LEVEL REALITY:
     p₁ and p₂ CONTRADICT each other
     p₃ is missing the second hop
     verdict: insufficient

        o    "All three passages scored well."
       /|\
       / \

        o    "Independently. The problem is BETWEEN them."
       /|\
       / \
```

This is the same structural point Volume I §4.5 raised about set-based metrics, arriving from the
opposite direction.

## C.9.2 ⚠️ It is not a hallucination detector

The paper runs an explicit boundary-mapping experiment: contrasting SURE-RAG with GPT-4o on
HaluBench unsafe detection, **the ranking reverses** (0.3343 vs 0.7389 unsafe-F1), indicating that
controlled sufficiency verification and natural hallucination detection are **distinct problems**.

Filing SURE-RAG next to hallucination metrics invites exactly the misuse the authors warn against.

## C.9.3 Reported results

| Measure | Value |
|---|---|
| Calibrated Macro-F1 | 0.9075 (raw 0.8951 ± 0.0069) |
| DeBERTa mean-pooling baseline | 0.6516 |
| GPT-4o judge baseline | 0.7284 |
| Strong concat cross-encoder | 0.8888 ± 0.0109 |
| Risk at 30% coverage | 0.2588 → 0.1642 (**37% relative reduction**) |

Note that GPT-4o as a judge scored 0.7284 against a purpose-built verifier's 0.9075. That is a
concrete data point on the limits of general-purpose LLM judging.

## C.9.4 Recommendation

Adopt SURE-RAG's **framing** immediately regardless of the implementation: your retrieval evaluation
should ask whether the retrieved *set* justifies the answer, not whether each passage is topical.
Every metric in Volume I Chapter 4 and most of §C.3–C.5 scores passages independently.

If you are multi-hop, this is not optional. It is the difference between measuring your system and
measuring a proxy for it.

---

# C.10 Correctness — summary card

```
┌────────────────────────────────────────────────────────────────┐
│  CORRECTNESS / GROUNDING: THE DASHBOARD                        │
├────────────────────────────────────────────────────────────────┤
│  NO GOLDEN ANSWERS:                                            │
│     RAGAS (paper form, 3 metrics) — and know its limits        │
│                                                                │
│  GOLDEN ANSWERS AVAILABLE:                                     │
│     RAGChecker → promote Claim Recall, Self-Knowledge,         │
│     Hallucination. Keep the other six for diagnosis.           │
│                                                                │
│  SHIPPING CITATIONS:                                           │
│     ALCE citation precision (necessity, not just presence)     │
│     + a counterfactual faithfulness spot-check                 │
│                                                                │
│  CHOOSING A MODEL:                                             │
│     Trust-Score + MIRAGE's LLM-intrinsic half                  │
│                                                                │
│  MULTI-HOP:                                                    │
│     SURE-RAG framing — sufficiency is a SET property           │
├────────────────────────────────────────────────────────────────┤
│  THE FOUR RULES                                                │
│                                                                │
│  1. Faithfulness NEVER ships without Claim Recall beside it.   │
│                                                                │
│  2. Correct-but-ungrounded is a real and dangerous category.   │
│     Three papers named it independently: Lucky Guess,          │
│     Self-Knowledge, post-rationalization. Measure it.          │
│                                                                │
│  3. Report claim COUNTS next to claim PROPORTIONS. A model     │
│     that says less scores better on hallucination rate         │
│     without being more truthful.                               │
│                                                                │
│  4. Cite the version you ran. RAGAS-the-paper and              │
│     RAGAS-the-library are not the same evaluation.             │
└────────────────────────────────────────────────────────────────┘
```

---

# PART D — EFFICIENCY / COST

# D.1 The dimension nobody instruments

## D.1.1 Why it was missing

In the source catalogue, every efficiency measure sat under `NA` — not a real dimension. That
reflected the field: for a decade, retrieval efficiency was an infrastructure concern, not an
evaluation one. Latency belonged to SRE, quality belonged to research, and nobody owned the
trade-off between them.

RAG collapsed that separation, because in RAG the efficiency knobs *are* the quality knobs.

```
   THE KNOBS ARE THE SAME KNOBS
   ════════════════════════════

              k ▲                    k ▼
    ┌─────────────────────┬─────────────────────┐
    │ recall        ▲     │ recall        ▼     │
    │ faithfulness  ▲     │ faithfulness  ▼     │
    │ context util  ▼     │ context util  ▲     │
    │ noise sens.   ▲     │ noise sens.   ▼     │
    │ TOKENS        ▲▲▲   │ TOKENS        ▼▼▼   │
    │ LATENCY       ▲▲    │ LATENCY       ▼▼    │
    └─────────────────────┴─────────────────────┘

        o    "Quality and cost are separate concerns."
       /|\
       / \

        o    "They're the same dial. You cannot tune
       /|\     one without moving the other."
       / \
```

Gan et al.'s survey confirms the field has caught up: it treats computational efficiency as a
co-equal axis alongside performance, factual accuracy, and safety.

## D.1.2 The four cost centres

```
   ═══════════════════════════════════════════════════════
   WHERE THE MONEY GOES              MEASURED BY
   ═══════════════════════════════════════════════════════
   INDEX TIME    building and        upload time, indexing
                 refreshing the      time, index size,
                 vector store        rebuild cadence
   ───────────────────────────────────────────────────────
   QUERY TIME    retrieving and      retrieval speed,
                 reranking           throughput, TTFT
   ───────────────────────────────────────────────────────
   TOKEN         context you pay     prompt tokens,
                 for and don't use   redundancy, EHR@k
   ───────────────────────────────────────────────────────
   EVALUATION    measuring all       judge calls, extraction
                 of the above        calls, GPU-hours
   ═══════════════════════════════════════════════════════
```

The fourth is the one teams discover by receiving an invoice.

---

# D.2 Index-time metrics

**Source:** the four metrics below are the ones identified in the Brehme, Ströhle & Breu systematic
review as the standard set for database performance evaluation:
**upload time, indexing time, retrieval speed, and throughput**
([arXiv:2504.20119](https://arxiv.org/abs/2504.20119)).

The review's summary of the state of practice is itself the finding: the indexing component is
evaluated **primarily on performance metrics** like indexing and retrieval speed, while other
factors are assessed only as part of overall system performance. In other words, nobody is measuring
whether your indexing *choices* — chunk size, overlap, embedding model — are good, except
indirectly.

## D.2.1 The metrics

| Metric | Unit | What it tells you |
|---|---|---|
| **Upload time** | corpus | Ingestion pipeline throughput |
| **Indexing time** | corpus | Cost of a full rebuild — the number that determines whether re-embedding is feasible |
| **Retrieval speed** | query | Per-query latency at the vector store |
| **Throughput** | system | Concurrent query capacity |
| **Index size** | corpus | Storage cost; also a proxy for memory pressure |

## D.2.2 The metric that changes decisions: rebuild cost

```
   WHY INDEXING TIME IS A DRIFT METRIC IN DISGUISE
   ═══════════════════════════════════════════════

   Supplement A §B.2 recommendation:
     "re-embed when the embedder changes"

   That recommendation is FREE if a rebuild takes 2 hours.
   It is a PROJECT if a rebuild takes 3 weeks.

        o    "We'll re-index quarterly."
       /|\
       / \

        o    "Have you timed a full rebuild?"
       /|\
       / \

        o    "...no."
       /|\
       / \   "Then you don't have a drift policy.
              You have a drift aspiration."
```

**Concrete evidence that architecture choice dominates here:** VersionRAG requires **97% fewer
tokens during indexing than GraphRAG**, which the authors note makes it practical for large-scale
deployment ([arXiv:2510.08109](https://arxiv.org/abs/2510.08109)). A 30× indexing cost difference is
the difference between a system you can refresh and one you cannot.

## D.2.3 Recommendation

**Time a full rebuild once, and write the number down.** It is the single most decision-relevant
efficiency number and almost nobody has it. Every drift and freshness policy in Supplement A is
gated on it.

---

# D.3 Query-time metrics

## D.3.1 The standard set

| Metric | Facet | Note |
|---|---|---|
| **Query latency / response time** | query | Manning Ch. 8 — the classical measure |
| **Time-to-first-token (TTFT)** | query | Dominant *perceived* latency in streaming UIs |
| **Query throughput** | system | Manning Ch. 4 |
| **Query-processing cost** | query | Manning Ch. 7 |
| **Retrieval calls per answer** | query | **Agentic RAG only** — see §D.5 |

## D.3.2 Why TTFT matters more than total latency

```
   TWO SYSTEMS, SAME TOTAL LATENCY
   ═══════════════════════════════

   SYSTEM A:  [────── 4s silence ──────][burst]
              TTFT 4.0s    total 4.2s

   SYSTEM B:  [0.6s][t-o-k-e-n-s-s-t-r-e-a-m-i-n-g]
              TTFT 0.6s    total 4.2s

        o    "Identical latency."
       /|\
       / \

        o    "System A feels broken. System B feels fast.
       /|\     Your dashboard cannot tell them apart."
       / \
```

Retrieval sits *before* the first token, so **retrieval latency is TTFT latency**. This is the
strongest argument for measuring retrieval speed separately rather than folding it into an
end-to-end number: it is the part the user waits through with nothing on screen.

## D.3.3 Recommendation

Report **TTFT at p50 and p95**, not mean total latency. Means hide the tail, and the tail is what
generates support tickets. If a reranker adds 200ms at p50 and 3s at p95, the p50 number will
justify shipping it and the p95 number is the one users experience on bad days.

---

# D.4 Token economics — the wasted-context problem

This is where Efficiency stops being an infrastructure concern and becomes a quality concern.

## D.4.1 The measurable waste

RAG-X supplies the concrete numbers ([arXiv:2603.03541](https://arxiv.org/abs/2603.03541)), and they
are worse than intuition suggests. On their best-performing pipeline (MAP 0.44, GuidelineQA):

| Metric | Value | Reading |
|---|---|---|
| **Pairwise Redundancy** (contexts 1 & 2) | **22.0%** | A fifth of the context overlaps |
| **Exclusive Hit Rate @ rank 2** | **6.8%** | Rank 2 almost never adds anything new |
| Recall | 57.6% | "Adequate coverage" |

The paper's own reading: although standard recall suggests adequate coverage, the retriever is
returning **overlapping evidence rather than complementary context, wasting retrieval capacity.**
Their prescribed fix is Maximum Marginal Relevance for diversity, and diverse re-ranking.

```
   WHAT YOU PAY FOR vs WHAT YOU GET
   ════════════════════════════════

   You budget 3 chunks × 1,024 tokens = 3,072 tokens

   ┌─────────────┬─────────────┬─────────────┐
   │  chunk 1    │  chunk 2    │  chunk 3    │
   │  ███████    │  ██▓▓▓▓▓    │  ███████    │
   │             │   ▓ = same  │             │
   │             │   info as   │             │
   │             │   chunk 1   │             │
   └─────────────┴─────────────┴─────────────┘

   Effective distinct information: ~2.3 chunks
   Tokens purchased: 3,072
   Tokens carrying new information: ~2,350

        o    "Our recall is 57.6%."
       /|\
       / \

        o    "Your DISTINCT recall is lower, and you
       /|\     paid full price for the duplicates."
       / \
```

## D.4.2 The metrics to adopt

| Metric | Definition | Source |
|---|---|---|
| **Pairwise Redundancy** | Overlap between top-ranked contexts | RAG-X ✅ |
| **Exclusive Hit Rate (EHR@k)** | % of queries where ground truth appears in **only one** retrieved context | RAG-X ✅ |
| **Prompt tokens per query** | Direct cost | standard |
| **Wasted-context ratio** | Tokens in passages with zero attribution | *proposed* — approximate with WARG or EHR |

**EHR@k is the diagnostic one and it reads counterintuitively.** RAG-X observed that on GuidelineQA,
the best retriever's EHR@1 dropped to 0.1 at its highest-recall setting — high recall was achieved
by returning the same answer in multiple chunks. On MedQuAD-GHR, EHR@1 reached 0.30, indicating a
"single-source-of-truth" pattern where the generator's success depends entirely on attending to the
first retrieved passage.

Those two readings imply **opposite engineering responses**: the first says add diversity; the
second says protect rank 1 at all costs. One metric, two corpora, two strategies.

## D.4.3 Recommendation

**Add Pairwise Redundancy to your dashboard.** It is cheap — no LLM calls, just chunk similarity —
and it is the only Efficiency metric that directly reveals quality waste.

If redundancy exceeds ~20%, implement MMR before increasing k. Increasing k when redundancy is high
buys you more duplicates at full token price.

---

# D.5 The cost of evaluation itself

## D.5.1 The invoice nobody forecasts

Every metric in Supplements A and B has a price:

```
   ═══════════════════════════════════════════════════════════
   METRIC                    COST PER QUERY
   ═══════════════════════════════════════════════════════════
   Precision / Recall / nDCG   ~free (given labels)
   ───────────────────────────────────────────────────────────
   RAGAS faithfulness          1 extraction + n entailment
   ───────────────────────────────────────────────────────────
   RAGChecker (all nine)       1 extraction × 2 (response + GT)
                               + entailment across
                                 claims × chunks
   ───────────────────────────────────────────────────────────
   ALCE citation precision     leave-one-out:
                               COMBINATORIAL in citations
                               per sentence
   ───────────────────────────────────────────────────────────
   eRAG                        k LLM calls (one per document)
   ───────────────────────────────────────────────────────────
   ΔSePer                      N samples × 2 conditions
                               + entailment over response pairs
   ───────────────────────────────────────────────────────────
   MIRAGE                      3 inference runs
                               (Base / Oracle / Mixed)
   ───────────────────────────────────────────────────────────
   WARG                        Shapley approximation — heavy
   ═══════════════════════════════════════════════════════════

        o    "We'll run the full suite on every PR."
       /|\
       / \

        o    "Add up that column first."
       /|\
       / \
```

## D.5.2 The published efficiency wins

Two papers explicitly optimized evaluation cost, and both numbers are large enough to change your
architecture:

- **eRAG: up to 50× less GPU memory** than end-to-end evaluation, with improved runtime
  ([arXiv:2404.13781](https://arxiv.org/abs/2404.13781)). This is what makes utility-based labelling
  feasible at all.
- **MIRAGE: a 37,800-chunk retrieval pool — about 1% of a full wiki-dump** — significantly reducing
  computational cost while maintaining relevance to large-scale benchmarks like MTEB
  ([arXiv:2504.17137](https://arxiv.org/abs/2504.17137)).

Both are instances of the same principle: **evaluation does not need to run at production scale to
be informative.** A well-constructed 1% sample beats a full-corpus evaluation you cannot afford to
run often enough to catch regressions.

## D.5.3 The tiering recommendation

```
   ┌──────────────────────────────────────────────────────┐
   │  EVALUATION COST TIERS                               │
   │                                                      │
   │  EVERY COMMIT   ── ref + free metrics only           │
   │                    P@K, Recall@k, Pairwise Redundancy│
   │                    latency, TTFT                     │
   │                    cost: ~zero                       │
   │                                                      │
   │  NIGHTLY        ── one judge-based metric on a       │
   │                    fixed 200-query sample            │
   │                    RAGAS or RAGChecker-3             │
   │                                                      │
   │  PER RELEASE    ── the expensive diagnostics         │
   │                    ΔSePer, WARG, full RAGChecker,    │
   │                    CUE quadrants                     │
   │                                                      │
   │  PER MODEL      ── procurement instruments           │
   │  CHANGE            MIRAGE, Trust-Score, CKA          │
   │                                                      │
   │  QUARTERLY      ── human anchor set + version-       │
   │                    sensitive set + judge agreement   │
   └──────────────────────────────────────────────────────┘
```

---

# D.6 Efficiency — summary card

```
┌────────────────────────────────────────────────────────────────┐
│  EFFICIENCY / COST: WHAT TO MEASURE                            │
├────────────────────────────────────────────────────────────────┤
│  INDEX TIME                                                    │
│    ▸ Full rebuild duration ── the number that gates every      │
│      drift policy you have. Time it. Write it down.            │
│    ▸ Index size, upload time, indexing time                    │
│                                                                │
│  QUERY TIME                                                    │
│    ▸ TTFT at p50 and p95 (NOT mean total latency)              │
│    ▸ Retrieval latency separately — it IS the TTFT             │
│                                                                │
│  TOKENS                                                        │
│    ▸ Pairwise Redundancy ── cheap, and reveals quality waste   │
│    ▸ EHR@k ── tells you whether to add diversity or protect    │
│      rank 1. Opposite strategies, same metric.                 │
│    ▸ Prompt tokens per query                                   │
│                                                                │
│  EVALUATION                                                    │
│    ▸ Tier your suite. The full stack on every commit is not    │
│      diligence, it is an unexamined invoice.                   │
├────────────────────────────────────────────────────────────────┤
│  THE ONE INSIGHT                                               │
│  In RAG the efficiency knobs ARE the quality knobs. k, chunk   │
│  size, and rerank depth move recall, faithfulness, context     │
│  utilization, noise sensitivity, latency, and cost — all at    │
│  once, and not all in the same direction. You cannot reason    │
│  about that trade-off with one side unmeasured.                │
└────────────────────────────────────────────────────────────────┘
```

---

# Appendix B1 — Sourcing ledger

| Metric | Read at | Definitions obtained? |
|---|---|---|
| RAGChecker ×9 | **Formal restatement of paper definitions** | ✅ All nine, precisely |
| RAGAS | Paper components + computation method | ✅ + library-drift discrepancy |
| ALCE | **Mechanism described in detail** | ✅ Leave-one-out precision |
| Citation faithfulness | Paper abstract + framing | ✅ Post-rationalization, 57% |
| Trust-Score | Paper abstract + results | ✅ Conceptual; components not itemized |
| TriFEX / PKP / PR | Paper abstract, verbatim | ✅ Including 75% variance finding |
| SURE-RAG | Paper abstract, verbatim | ✅ Four feature blocks + boundary experiment |
| FActScore | Title + abstract 🟡 | Conceptual only |
| Index-time metrics | Brehme survey account | ✅ Four named metrics |
| RAG-X efficiency | **Paper Table IV** | ✅ Redundancy 22.0%, EHR@2 6.8% |

# Appendix B2 — Corrections and warnings issued

1. **RAGAS paper ≠ RAGAS library.** Paper: three metrics including Context Relevance. Library:
   four, commonly including context_recall — which is **reference-based**, breaking the
   reference-free claim that motivates choosing RAGAS.
2. **RAGChecker's Context Precision is chunk-level by design**, because claim-level precision has a
   corpus-dependent ceiling below 100%. Do not "fix" it to claim level.
3. **SURE-RAG is not a hallucination detector** — the paper's own boundary experiment shows the
   ranking reverses against GPT-4o on HaluBench.
4. **Hallucination rate is a proportion.** A model that generates fewer claims scores better without
   improving. Report claim counts alongside.
5. **Three papers named one failure independently:** RAG-X's Lucky Guess, RAGChecker's
   Self-Knowledge, Wallat et al.'s post-rationalization. Correct-but-ungrounded is the most
   under-measured category in RAG.

# Appendix B3 — Cross-supplement index of the recurring warning

The single point made in every part of this white paper so far:

| Location | Formulation |
|---|---|
| Vol I §1.3 | A faithfulness score is meaningless without a retrieval-hit denominator |
| Supp A §A.3.1 | The Adherence Paradox — 0.84 adherence, 33.9% ungrounded |
| Supp B §C.1.2 | The top-right quadrant survives every review |
| Supp B §C.4.6 | Do not dashboard Faithfulness without Claim Recall |
| Supp B §C.6.2 | Three independent papers, one failure mode |

If a reader takes nothing else from four documents, this is the thing to take.
