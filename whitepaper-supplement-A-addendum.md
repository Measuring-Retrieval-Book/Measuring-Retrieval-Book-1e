# Measuring Retrieval — Supplement A, Addendum

## Lifting the 🟡 Entries
### Plus one correction to Supplement A §B.2

---

**Purpose.** Supplement A marked five entries 🟡 ABSTRACT-ONLY, meaning I described them at the
level I had actually read rather than inferring method detail. This addendum lifts three of them to
method level, closes one with a correction, and leaves two honestly open.

**The correction matters more than the additions.** Reading the CKA paper properly reverses the
practical guidance I gave in Supplement A §B.2. If you acted on that section, read §AD.2 first.

---

# AD.1 Retrieval Robustness — the three metrics, now named

**Previously:** 🟡 ABSTRACT-ONLY — "three metrics, definitions not obtained."
**Now:** ✅ Named and characterized.

**Source:** Cao et al., *Evaluating the Retrieval Robustness of Large Language Models* ·
[arXiv:2505.21870](https://arxiv.org/abs/2505.21870)

## AD.1.1 The three metrics

The paper introduces retrieval robustness metrics — **no-degradation rate, retrieval size
robustness, and retrieval order robustness** — to quantify how reliably LLMs handle queries via RAG.

They derive from an explicit three-part definition of what robustness means. An LLM is retrieval
robust if:

1. its RAG performance is **equal to or better than** its non-RAG performance;
2. adding more retrieved documents leads to **equal or better** performance;
3. its RAG performance is **invariant to the order** of retrieved documents.

```
   THE THREE ROBUSTNESS METRICS
   ════════════════════════════

   NO-DEGRADATION RATE
   ┌────────────────────────────────────┐
   │  RAG ≥ no-RAG ?                    │
   │                                    │
   │  no-RAG:  ████████░░  0.62         │
   │  RAG:     ██████████  0.71  ✓      │
   │                                    │
   │  Fails when retrieval makes it     │
   │  WORSE — which happens more than   │
   │  anyone admits.                    │
   └────────────────────────────────────┘

   RETRIEVAL SIZE ROBUSTNESS
   ┌────────────────────────────────────┐
   │  more docs ≥ fewer docs ?          │
   │                                    │
   │  k=5   ████████░░                  │
   │  k=20  █████████░                  │
   │  k=50  ███████░░░  ✗ dropped       │
   └────────────────────────────────────┘

   RETRIEVAL ORDER ROBUSTNESS
   ┌────────────────────────────────────┐
   │  original ≈ reversed ≈ shuffled ?  │
   │                                    │
   │  original  ████████░░              │
   │  reversed  ███████░░░              │
   │  shuffled  ████████░░              │
   └────────────────────────────────────┘
```

## AD.1.2 Experimental setup, now specified

| Element | Detail |
|---|---|
| Benchmark | 1,500 questions — **500 each from NQ, HotpotQA, and ASQA** |
| Retrieval | Wikipedia, using both **sparse and dense** retrievers |
| Retrieval sizes tested | **5 to 100** documents |
| Orderings tested | **original rank, reversed rank, random shuffle** |
| Models | **11 LLMs from 5 families**, open and proprietary |
| Prompting | 3 strategies |
| Correctness scoring | **LLM-as-judge (LLaMA-3.3:70B)**, not string match |

That last row is worth noting: the authors deliberately moved away from string-match metrics, which
means the robustness figures inherit LLM-judge dependency (Supplement A §B.5).

## AD.1.3 The result — and the caveat that is the actual finding

Models achieve **over 80% on the geometric mean of the three metrics**. Read alone, that is
reassuring: usually RAG beats non-RAG, usually more documents help, usually order does not matter
much.

But the paper's conclusion is pointed about what the aggregate hides:

> Imperfect robustness results in **sample-level trade-offs, often hurting the performance of some
> samples for the improvement of others, which forfeits RAG's potential gains.**

```
   THE AGGREGATE THAT HIDES THE TRADE
   ══════════════════════════════════

   System-level:   no-RAG 0.62 ──▶ RAG 0.71    "+9 points!"

   Sample-level:
     ┌──────────────────────────────────────┐
     │ 34% of samples:  improved  ▲▲▲       │
     │ 19% of samples:  DEGRADED  ▼▼        │
     │ 47% of samples:  unchanged           │
     └──────────────────────────────────────┘

        o    "RAG gained us nine points."
       /|\
       / \

        o    "RAG gained you thirty-four points and
       /|\     LOST you nineteen. The nine is the
       / \     residue. Nineteen percent of your users
              got a worse answer than with no
              retrieval at all."

   (Illustrative split — the paper reports the
    phenomenon, not these exact figures.)
```

A second finding with a direct architectural implication: incorporating outputs generated with the
model's own knowledge **can enhance retrieval robustness, but also limits the best performance
achievable by RAG.** Hedging against retrieval failure costs you retrieval's upside. That is a real
trade-off, not a free win.

## AD.1.4 Revised recommendation

Supplement A recommended running the RQ1 test. That stands, but sharpen it:

**Do not evaluate robustness at the aggregate level only.** Compute the no-degradation rate
per-sample and report the *degraded* fraction explicitly. A system that improves the mean while
degrading a fifth of queries is not a system that got better — it is a system that redistributed
quality, and the losers are invisible in the mean.

If you can segment by query class, do — a 19% degradation rate concentrated in one customer segment
is a very different problem from 19% spread uniformly.

## AD.1.5 Two related works surfaced while lifting this entry

**RARE-Met** ([arXiv:2506.00789](https://arxiv.org/abs/2506.00789)) ✅ — a retrieval-aware robustness
metric with an explicit refusal clause. Its definition of robustness is stricter than Cao et al.'s
and connects directly to Supplement B §C.7:

- When the generator **can** answer without retrieval, it should answer correctly **regardless** of
  what retrieval returns — correct, incorrect, or irrelevant
- When the generator **cannot** answer without retrieval, it should answer correctly given correct
  retrieval, and otherwise **refuse rather than hallucinate**

This is the robustness metric that treats appropriate refusal as a success condition. If you adopted
Trust-Score for its refusal handling, RARE-Met is its robustness counterpart.

**A 2026 reproduction study** ([arXiv:2605.27105](https://arxiv.org/abs/2605.27105)) ✅ reproduces
both Cao et al. and *Lost in the Middle* under modern LLMs, using the same k grid and the same three
ordering schemes. Independent reproduction is rare in this literature and worth reading before you
treat either result as settled.

---

# AD.2 ⚠️ CORRECTION — the CKA family

**Previously:** 🟡 ABSTRACT-ONLY, presented in Supplement A §B.2 as a drift stack, with an
interpretation table implying that high similarity means a safe embedder swap.

**Now:** ✅ Read at conclusion and results level. **The paper's central finding inverts my framing.**

**Source:** Caspari, Ghosh Dastidar, Zerhoudi, Mitrović & Granitzer, CEUR-WS Vol-3784 (short paper) ·
[arXiv:2407.08275](https://arxiv.org/abs/2407.08275)

## AD.2.1 What the paper actually studied

19 embedding models across five BEIR datasets, using CKA for pairwise embedding comparison plus
Jaccard and rank similarity for retrieval behaviour at top-k. **The purpose was model
selection** — identifying clusters of similar models to streamline choosing one — not drift
monitoring.

My Supplement A framing extended it to temporal drift. I flagged that extension as mine at the
time, which was right. What I did not flag, because I had not read the results, is the finding
below.

## AD.2.2 The finding I got wrong

> Comparing embeddings with CKA generally showed intra- and inter-family clusters across datasets.
> These clusters also appeared when evaluating top-k retrieval similarity with **large k values**.
> However, **scores for low k values, which would commonly be chosen in RAG systems, show high
> variance and much lower similarity, especially on larger datasets.**

And more starkly, on the two larger datasets (FiQA-2018 and TREC-COVID): **most models retrieve
almost completely distinct text chunks.** Only one cluster (bge/UAE/mxbai) retained notable
similarity; the rest showed moderate-to-low similarity at best.

```
   WHAT I IMPLIED vs WHAT THE PAPER FOUND
   ══════════════════════════════════════

   SUPPLEMENT A (wrong emphasis):
     "If Jaccard and RankSimilarity are high, the
      migration is low risk."

   THE PAPER:
     At the small k RAG actually uses, similarity is
     LOW and UNSTABLE. Different models retrieve
     largely DIFFERENT chunks.

   ┌─────────────────────────────────────────────┐
   │  Jaccard similarity vs k                    │
   │                                             │
   │  1.0 ┤                          ╭────────   │
   │      │                     ╭────╯           │
   │  0.5 ┤              ╭──────╯                │
   │      │      ╭───────╯                       │
   │  0.0 ┤ ╱╲╱╲╱                                │
   │      └─┬────┬────┬────┬────┬────┬─────      │
   │        3   10   50  100  500  1000    k     │
   │        ▲▲▲                                  │
   │        └── where RAG lives.                 │
   │            High variance. Low similarity.   │
   └─────────────────────────────────────────────┘

        o    "So a high-CKA model is a safe swap?"
       /|\
       / \

        o    "CKA similarity at the embedding level
       /|\     does NOT imply similar retrieval at
       / \     k=3. That's the paper's point."
```

The authors add a caveat that makes it worse rather than better: their datasets are comparatively
small, while real RAG systems operate on millions of embeddings — so if a general trend of larger
datasets producing lower retrieval similarity holds, **real-world divergence may exceed what they
measured.**

## AD.2.3 Corrected guidance

| Supplement A said | Corrected |
|---|---|
| High Jaccard/RankSimilarity → low-risk migration | **Expect low similarity at RAG-typical k. Low similarity is the default, not the alarm.** |
| Use the three measures as a drift stack | Still valid — but calibrate against *your own* baseline, since cross-model similarity is inherently low |
| CKA as the primary instrument | **Jaccard and RankSimilarity at your production k are the operative measures.** CKA describes representation geometry, which does not transfer to retrieval behaviour at small k |

**The practical upshot is stronger, not weaker.** Every embedder swap is a high-risk change by
default. Do not reason from leaderboard proximity or from CKA — measure Jaccard and RankSimilarity
*at your actual k*, on *your actual corpus*, before migrating. Two models that look interchangeable
on MTEB may retrieve almost completely distinct chunks for your queries.

This also reinforces the Supplement A recommendation that mattered most: **freeze a baseline now.**
Its value just went up, because the thing you are guarding against is larger than I represented.

## AD.2.4 A second-order consequence for §B.5

If different embedders retrieve largely different chunks at small k, then **any evaluation number
computed under embedder A is not comparable to the same number under embedder B** — not just drift
metrics, but faithfulness, CUE quadrants, everything downstream. Embedder version belongs in your
experiment metadata alongside judge version.

---

# AD.3 Entries that remain open

Honesty about what this addendum did *not* close:

| Entry | Status | What is missing |
|---|---|---|
| **Query-level robustness** (Perçin et al., [2507.06956](https://arxiv.org/abs/2507.06956)) | 🟡 still abstract-only | Metric definitions; the per-query aggregation scheme |
| **Latest@10 / temporal freshness** ([2509.19376](https://arxiv.org/abs/2509.19376)) | 🟡 partially lifted | Results obtained and reported in Supp A; the Latest@10 formula itself not obtained |
| **Gain** (GainRAG, [2505.18710](https://arxiv.org/abs/2505.18710)) | 🟡 still framing-level | The gain estimation method and middleware training detail |
| **FActScore** ([2305.14251](https://arxiv.org/abs/2305.14251)) | 🟡 conceptual | Atomic-fact decomposition procedure |
| **Trust-Score components** ([2409.11242](https://arxiv.org/abs/2409.11242)) | 🟡 conceptual | The sub-scores that compose it |

These are described in Supplements A and B at the level I actually read them. None is described as
though I had the method when I did not.

```
        o    "Why not just fill those in? You know
       /|\     roughly what they do."
       / \

        o    "Because 'roughly' is how the AIS venue
       /|\     error happened, and how the SePer
       / \     reference-free claim got into
              circulation. Roughly is the failure mode."
```

---

# AD.4 Revised sourcing ledger for Supplement A

| Metric | Was | Now |
|---|---|---|
| eRAG | Conceptual | Conceptual (unchanged) |
| DIG | Conceptual | Conceptual (unchanged) |
| ΔSePer | ✅ Algorithm 1 | ✅ (unchanged) |
| Gain | 🟡 | 🟡 (unchanged — see AD.3) |
| WARG | Method named | Method named (unchanged) |
| CUE | ✅ Full construction | ✅ (unchanged) |
| MIRAGE ×4 | ✅ Definitions + split | ✅ (unchanged) |
| UDCG | ✅ Formula | ✅ (unchanged) |
| **CKA family** | 🟡 | ✅ **+ correction issued (AD.2)** |
| VersionQA | ✅ Composition + results | ✅ (unchanged) |
| **Retrieval Robustness** | 🟡 | ✅ **Three metrics named + setup** |
| Query robustness | 🟡 | 🟡 (unchanged) |
| Latest@10 | 🟡 | 🟡 partial |

**New entries added by this addendum:** RARE-Met (2506.00789), reproduction study (2605.27105).

---

# AD.5 Running correction log across all documents

| # | Correction | Where | Whose error |
|---|---|---|---|
| 1 | AIS is *Computational Linguistics* 49(4), not TACL | Catalogue | **Mine** |
| 2 | SePer is reference-based; a popular summary says otherwise | Supp A | Third party |
| 3 | MIRAGE is *Findings of* NAACL 2025 | Supp A | Catalogue |
| 4 | RAG-X's 14% gap is Accuracy − Context Hit Rate | Supp A | User's framing |
| 5 | eRAG/Gain/DIG/ΔSePer are one family, not four | Supp A | Catalogue structure |
| 6 | RAGAS paper ≠ RAGAS library | Supp B | Field-wide |
| 7 | SURE-RAG is not a hallucination detector | Catalogue | Catalogue |
| 8 | PEER and DUO are fairness metrics, not Correctness | Catalogue | Catalogue |
| 9 | **CKA similarity does not imply retrieval similarity at small k** | **Supp A §B.2** | **Mine** |

Two of the nine are mine. Both came from describing something I had not read at method level — the
exact failure this document set was structured to avoid, occurring twice anyway.

---

# AD.6 What this changes for the reader

If you have been following along and acting on these documents:

```
   ┌────────────────────────────────────────────────────┐
   │  ACTION ITEMS REVISED BY THIS ADDENDUM             │
   │                                                    │
   │  1. EMBEDDER MIGRATION                             │
   │     Was: "check similarity, migrate if high"       │
   │     Now: assume high risk. Measure Jaccard +       │
   │          RankSimilarity AT YOUR k, on YOUR corpus. │
   │          Expect low numbers — that is normal, and  │
   │          it is why the check matters.              │
   │                                                    │
   │  2. ROBUSTNESS REPORTING                           │
   │     Was: "run the RAG-vs-no-RAG test"              │
   │     Now: run it PER SAMPLE and report the          │
   │          DEGRADED fraction. The mean hides a       │
   │          redistribution.                           │
   │                                                    │
   │  3. EXPERIMENT METADATA                            │
   │     New: pin the EMBEDDER version alongside the    │
   │          judge version. Downstream metrics are     │
   │          not comparable across embedders.          │
   └────────────────────────────────────────────────────┘
```

---

# Appendix AD-A — Documents in this set

| # | Document | Covers | Status |
|---|---|---|---|
| 0 | `ir-rag-metrics-catalogue-v2.md` | Full index, all dimensions | Complete, 4 verification passes |
| 1 | `whitepaper-vol1-part1.md` | Ch 0–4: dimensions, facets, signals, set metrics | Complete |
| 2 | `whitepaper-supplement-A.md` | Alignment, Integrity/Drift | Complete + this addendum |
| 3 | `whitepaper-supplement-B.md` | Correctness/Grounding, Efficiency/Cost | Complete |
| 4 | **`whitepaper-supplement-A-addendum.md`** | 🟡 lifts + CKA correction | **this file** |

**Still to write:**

| Installment | Chapters | Contents |
|---|---|---|
| Vol I, 2 | 5–7 | Rank metrics (MRR, MAP, nDCG, ERR, RBP); incomplete judgments (bpref, infAP); rank comparison (τ, ρ, RBO) |
| Vol I, 3 | 8–10 | Diversity & novelty; fairness & exposure; online & counterfactual |
| Vol I, 4 | 11–12 | Significance & reporting; efficiency (classical) |
| Vol II, 8 | 22–24 | Meta-evaluation, judge reliability, deployment playbooks |

Volume I Installment 2 requires verifying five classical citations currently marked ⬜ — ERR
(Chapelle et al., CIKM'09), RBP (Moffat & Zobel, TOIS'08), RBO (Webber, Moffat & Zobel, TOIS'10),
bpref (Buckley & Voorhees, SIGIR'04), and infAP (Yilmaz & Aslam, CIKM'06). Those verifications
happen before that installment ships, per the policy in Volume I's header.
