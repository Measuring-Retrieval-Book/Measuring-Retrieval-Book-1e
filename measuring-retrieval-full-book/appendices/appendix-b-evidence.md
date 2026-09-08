# Appendix B: Evidence Status and Corrections

This appendix is the book's audit trail. It preserves the citation checks, the correction logs,
the document indexes and the final method resolutions from every installment of the manuscript, so
that any claim in the chapters can be traced back to the pass in which it was checked and to the
status it was carried at.

Two things are worth knowing before you read it. The verification marks record whether a citation
was checked against the primary source during a given pass, which is a separate question from how
established the metric itself is, for the reasons §2.4 sets out. And where a later pass overturned
an earlier reading, both readings are kept rather than the earlier one being quietly deleted.

## Ledger from `whitepaper-vol1-part1.md`

### Appendix 1A - Verified sources cited in this installment

| # | Work | Identifier | Status |
|---|---|---|---|
| 1 | Manning, Raghavan & Schütze, *Introduction to Information Retrieval* | Cambridge UP, 2008 | ESTABLISHED standard text |
| 2 | Gan et al., *RAG Evaluation in the Era of LLMs: A Comprehensive Survey* | [2504.14891](https://arxiv.org/abs/2504.14891) | VERIFIED |
| 3 | Brehme, Ströhle & Breu, *Can LLMs Be Trusted for Evaluating RAG Systems?* | [2504.20119](https://arxiv.org/abs/2504.20119) | VERIFIED |
| 4 | Randl et al., *RAG-E: Quantifying Retriever-Generator Alignment* | [2601.21803](https://arxiv.org/abs/2601.21803) | VERIFIED |
| 5 | Sivakumar, Sugumaran & Qiang, *RAG-X* | [2603.03541](https://arxiv.org/abs/2603.03541) | VERIFIED |
| 6 | Huwiler, Stockinger & Fürst, *VersionRAG* | [2510.08109](https://arxiv.org/abs/2510.08109) | VERIFIED |
| 7 | Liu et al., *Lost in the Middle* | [2307.03172](https://arxiv.org/abs/2307.03172) | VERIFIED |
| 8 | Qiu, Han & Huang, *SURE-RAG* | [2605.03534](https://arxiv.org/abs/2605.03534) | VERIFIED |
| 9 | Rashkin et al., *Measuring Attribution in NLG* | *Computational Linguistics* 49(4):777-840, 2023 | VERIFIED (venue corrected) |

---

### Appendix 1B - What Installment 2 covers

Chapter 5 introduces rank sensitivity and graded relevance:

- **MRR** - the metric for "one right answer exists"
- **MAP** - averaging precision at every relevant position
- **DCG / nDCG** - logarithmic position discount, graded relevance
- **ERR** *(Chapelle et al., CIKM'09)* OPEN - cascade model, stops at satisfaction
- **RBP** *(Moffat & Zobel, TOIS'08)* OPEN - geometric persistence, **with an explicit residual for
  unjudged documents**, which makes it the bridge into Chapter 6

Chapter 6 confronts the recall denominator problem directly: **bpref**, **infAP**, pooling depth
bias, and assessor agreement.

Chapter 7 covers rank comparison and the drift application: **Kendall's τ**, **Spearman ρ**, and
**RBO** *(Webber, Moffat & Zobel, TOIS'10)* OPEN - plus **CKA**, **Jaccard**, and **RankSimilarity**
from Caspari et al. ([arXiv:2407.08275](https://arxiv.org/abs/2407.08275) VERIFIED), which together form
the only fully-sourced drift stack currently available.

OPEN marks above indicate citations awaiting primary-record verification.
They will be verified before Installment 2 ships, per the policy in the header.

## Ledger from `whitepaper-vol1-part2.md`

### Appendix 2A - Citation verification ledger

All Installment 1 OPEN entries now resolved:

| Metric | Citation | Was | Now |
|---|---|---|---|
| **ERR** | Chapelle, Metzler, Zhang & Grinspan, CIKM 2009, pp. 621-630, doi 10.1145/1645953.1646033 | OPEN | VERIFIED |
| **RBP** | Moffat & Zobel, ACM TOIS 27(1), Article 2, 2008, 27pp, doi 10.1145/1416950.1416952 | OPEN | VERIFIED |
| **RBO** | Webber, Moffat & Zobel, *A Similarity Measure for Indefinite Rankings*, ACM TOIS 28(4):20:1-20:38, 2010 | OPEN | VERIFIED |
| **bpref** | Buckley & Voorhees, *Retrieval Evaluation with Incomplete Information*, SIGIR 2004, pp. 25-32 | OPEN | VERIFIED |
| **infAP** | Yilmaz & Aslam, CIKM 2006, Arlington VA, pp. 102-111; extended in *Knowl. Inf. Syst.* 16(2):173-211, 2008 | OPEN | VERIFIED |

**Additional citations verified during this evidence pass:**

| Work | Citation | Status |
|---|---|---|
| nDCG origin | Järvelin & Kekäläinen, *Cumulated Gain-Based Evaluation of IR Techniques*, ACM TOIS 20(4):422-446, 2002 | VERIFIED |
| Pooling reliability | Zobel, SIGIR 1998, pp. 307-314 | VERIFIED |
| Pooling depth & stability | Webber, Moffat & Zobel, EVIA 2010, pp. 7-15 | VERIFIED |
| The case against AP/nDCG | Zobel, Moffat & Park, *Against Recall: Is It Persistence, Cardinality, Density, Coverage, or Totality?*, SIGIR Forum 43(1):3-15, 2009 | VERIFIED |
| Top-weighted rank correlation | Yilmaz, Aslam & Robertson, *A New Rank Correlation Coefficient for Information Retrieval*, SIGIR 2008, pp. 587-594 | VERIFIED |
| Progress illusion | Armstrong, Moffat, Webber & Zobel, *Improvements That Don't Add Up: Ad-hoc Retrieval Results Since 1998*, CIKM 2009, pp. 601-610 | VERIFIED - reserved for Chapter 11 |

**Zero unverified citations remain in this installment.**

---

### Appendix 2B - Running correction log

Unchanged from the Supplement A Addendum: nine corrections, two of them mine. No new corrections
arose in this installment - the classical literature verified cleanly, which is itself informative.
Older, more-cited work has had its citations checked by more people.

---

### Appendix 2C - Document set status

| # | Document | Covers | Status |
|---|---|---|---|
| 0 | `ir-rag-metrics-catalogue-v2.md` | Full index | Complete |
| 1 | `whitepaper-vol1-part1.md` | Ch 0-4 | Complete |
| 2 | `whitepaper-supplement-A.md` | Alignment, Integrity/Drift | Complete + addendum |
| 3 | `whitepaper-supplement-B.md` | Correctness, Efficiency | Complete |
| 4 | `whitepaper-supplement-A-addendum.md` | OPEN lifts, CKA correction | Complete |
| 5 | **`whitepaper-vol1-part2.md`** | **Ch 5-7** | **this file** |

**Remaining:**

| Installment | Chapters | Contents | Notes |
|---|---|---|---|
| Vol I, 3 | 8-10 | Diversity & novelty (α-nDCG, ERR-IA, subtopic recall); fairness & exposure; online & counterfactual (interleaving, IPS) | Needs ~8 citations verified |
| Vol I, 4 | 11-12 | Significance & reporting; classical efficiency | Armstrong et al. already VERIFIED |
| Vol II, 8 | 22-24 | Meta-evaluation, judge reliability, deployment playbooks | Draws on Brehme survey, already read |

## Ledger from `whitepaper-vol1-part3.md`

### Appendix 3A - Citation verification ledger

**Chapter 8 - Diversity and Novelty**

| Work | Citation | Status |
|---|---|---|
| Subtopic recall | Zhai, Cohen & Lafferty, *Beyond Independent Relevance*, SIGIR 2003, pp. 10-17 | VERIFIED |
| α-nDCG | Clarke, Kolla, Cormack, Vechtomova, Ashkan, Büttcher & MacKinnon, SIGIR 2008, pp. 659-666, doi 10.1145/1390334.1390446 | VERIFIED |
| ERR-IA | Chapelle, Ji, Liao, Velipasaoglu, Lai & Wu, *Intent-Based Diversification of Web Search Results*, Information Retrieval 14(6):572-592, 2011 | VERIFIED |
| NRBP | Clarke, Kolla & Vechtomova, *An Effectiveness Measure for Ambiguous and Underspecified Queries*, ICTIR 2009 | VERIFIED |
| Cascade meta-analysis | Clarke, Craswell, Soboroff & Ashkan, WSDM 2011, pp. 75-84, doi 10.1145/1935826.1935847 | VERIFIED |

**Chapter 9 - Fairness and Exposure**

| Work | Citation | Status |
|---|---|---|
| Fairness of Exposure | Singh & Joachims, KDD 2018, pp. 2219-2228, doi 10.1145/3219819.3220088; arXiv:1802.07281 | VERIFIED |
| Equity of Attention | Biega, Gummadi & Weikum, SIGIR 2018, Ann Arbor MI, doi 10.1145/3209978.3210063 | VERIFIED |
| Ranked-output fairness | Yang & Stoyanovich, *Measuring Fairness in Ranked Outputs*, SSDBM 2017 | VERIFIED |
| Fair Ranking Track | TREC 2019, arXiv:2003.11650 | VERIFIED |
| RAG fairness | Wu, Li, Wu, Tao & Fang, COLING 2025, pp. 10021-10036, arXiv:2409.19804 | VERIFIED |

**Chapter 10 - Online and Counterfactual**

| Work | Citation | Status |
|---|---|---|
| Interleaving + the negative result | Radlinski, Kurup & Joachims, CIKM 2008, pp. 43-52, Napa Valley | VERIFIED |
| Implicit feedback accuracy | Joachims, Granka, Pan, Hembrooke, Radlinski & Gay, ACM TOIS 25(2), Art. 7, 2007 | VERIFIED |
| IPS / unbiased LTR | Joachims, Swaminathan & Schnabel, WSDM 2017, pp. 781-789 | VERIFIED |
| Position bias estimation | Agarwal, Zaitsev, Wang, Li, Najork & Joachims, WSDM 2019 | VERIFIED |
| Interleaving at scale | Chapelle, Joachims, Radlinski & Yue, *Large-Scale Validation and Analysis of Interleaved Search Evaluation* | VERIFIED |
| Interleaving properties | Hofmann, Whiteson & de Rijke, ACM TOIS 31(4):1-43, 2013 | VERIFIED |
| Multileaving | Schuth, Sietsma, Whiteson, Lefortier & de Rijke, CIKM 2014 | VERIFIED |
| Optimized interleaving | Radlinski & Craswell, WSDM 2013 | VERIFIED |
| Click test statistics | Yue, Gao, Chapelle, Zhang & Joachims, SIGIR 2010 | VERIFIED |

**OPEN Deferred to Installment 4:** sDCG (Järvelin et al., ECIR 2008); time-biased gain
(Smucker & Clarke, SIGIR 2012). Both carry OPEN status in §10.4.

---

### Appendix 3B - Running correction log

Nine corrections total, two of them mine. **No new corrections in this installment** - as in
Installment 2, the classical literature verified cleanly. The pattern across four installments is
consistent: well-cited pre-2015 work checks out; 2024-2026 preprints and secondary summaries are
where the errors live.

Two entries were relocated: **PEER** and **DUO** now sit in Chapter 9. The original catalogue had
misfiled them as Correctness metrics.

---

### Appendix 3C - Document set status

| # | Document | Covers | Status |
|---|---|---|---|
| 0 | `ir-rag-metrics-catalogue-v2.md` | Full index | Complete |
| 1 | `whitepaper-vol1-part1.md` | Ch 0-4 | Complete |
| 2 | `whitepaper-supplement-A.md` | Alignment, Integrity/Drift | Complete + addendum |
| 3 | `whitepaper-supplement-B.md` | Correctness, Efficiency | Complete |
| 4 | `whitepaper-supplement-A-addendum.md` | OPEN lifts, CKA correction | Complete |
| 5 | `whitepaper-vol1-part2.md` | Ch 5-7 | Complete |
| 6 | **`whitepaper-vol1-part3.md`** | **Ch 8-10** | **this file** |

**Remaining:**

| Installment | Chapters | Contents | Prerequisites |
|---|---|---|---|
| Vol I, 4 | 11-12 | Significance & reporting; classical efficiency; session metrics | Armstrong et al. VERIFIED; needs sDCG + time-biased gain OPEN |
| Vol II, 8 | 22-24 | Meta-evaluation, judge reliability, deployment playbooks | Brehme survey already read |

Installment 4 completes Volume I. Chapter 11 has one citation already verified and waiting -
Armstrong, Moffat, Webber & Zobel, *Improvements That Don't Add Up: Ad-hoc Retrieval Results Since
1998*, CIKM 2009, pp. 601-610 - which argues that a decade of reported retrieval improvements did
not accumulate. It is the natural closing argument for a volume about measurement.

## Ledger from `whitepaper-vol1-part4.md`

### Appendix 4A - Citation verification ledger

**Chapter 11**

| Work | Citation | Status |
|---|---|---|
| The progress problem | Armstrong, Moffat, Webber & Zobel, *Improvements That Don't Add Up*, CIKM 2009, pp. 601-610 | VERIFIED |
| Significance tests | Smucker, Allan & Carterette, CIKM 2007, pp. 623-632 | VERIFIED |
| Statistical power | Webber, Moffat & Zobel, CIKM 2008, pp. 571-580 | VERIFIED |
| Topic set size | Voorhees & Buckley, SIGIR 2002, pp. 316-323 | VERIFIED |
| Effort/sensitivity/reliability | Sanderson & Zobel, SIGIR 2005, pp. 162-169 | VERIFIED |
| Score standardization | Webber, Moffat & Zobel, SIGIR 2008, pp. 51-58 | VERIFIED |
| Statistical inference in IR | Savoy, *Information Processing and Management* 33(4):495-512, 1997 | VERIFIED |
| Biased judgments | Büttcher, Clarke, Yeung & Soboroff, SIGIR 2007, pp. 63-70 | VERIFIED |

**Chapter 12**

| Work | Citation | Status |
|---|---|---|
| **Time-biased gain** | Smucker & Clarke, *Time-Based Calibration of Effectiveness Measures*, SIGIR 2012, pp. 95-104, doi 10.1145/2348283.2348300 - **Best Paper** | VERIFIED *(was OPEN)* |
| TBG simulation | Smucker & Clarke, *Stochastic Simulation of Time-Biased Gain*, CIKM 2012, pp. 2040-2044 | VERIFIED |
| TBG user variance | Smucker & Clarke, *Modeling User Variance in Time-Biased Gain*, HCIR 2012, doi 10.1145/2391224.2391227 | VERIFIED |
| **sDCG** | Järvelin, Price, Delcambre & Nielsen, ECIR 2008, LNCS 4956, pp. 4-15, doi 10.1007/978-3-540-78646-7_4 | VERIFIED *(was OPEN)* |
| SRBP | Lipani, Carterette & Yilmaz, ICTIR 2019 | VERIFIED |
| Multi-query sessions | Kanoulas, Carterette, Clough & Sanderson, SIGIR 2011 | VERIFIED |
| Classical efficiency | Manning, Raghavan & Schütze, Ch. 4, 5, 7, 8, 20 | VERIFIED |

**Both Installment 3 deferrals resolved. Volume I contains zero OPEN entries.**

---

### Appendix 4B - Volume I citation summary

| Installment | Chapters | Citations verified | Corrections issued |
|---|---|---|---|
| 1 | 0-4 | 9 | 0 |
| 2 | 5-7 | 11 | 0 |
| 3 | 8-10 | 19 | 0 |
| 4 | 11-12 | 15 | 0 |
| **Total** | **0-12** | **54** | **0** |

**Zero corrections across all of Volume I.** Every classical citation verified as stated on first
attempt.

Contrast with the RAG-era material: nine corrections across the catalogue and supplements, two of
them mine. The pattern is unambiguous and worth stating as a finding in its own right -
**pre-2015 heavily-cited work has been checked by many people; 2024-2026 preprints and their
secondary summaries have not.** Calibrate your trust accordingly, and verify anything from the
last two years before you build on it.

---

### Appendix 4C - Document set status

| # | Document | Covers | Status |
|---|---|---|---|
| 0 | `ir-rag-metrics-catalogue-v2.md` | Full index, 4 verification passes | Complete |
| 1 | `whitepaper-vol1-part1.md` | Ch 0-4 | Complete |
| 2 | `whitepaper-supplement-A.md` | Alignment, Integrity/Drift | Complete |
| 3 | `whitepaper-supplement-B.md` | Correctness, Efficiency | Complete |
| 4 | `whitepaper-supplement-A-addendum.md` | OPEN lifts + CKA correction | Complete |
| 5 | `whitepaper-vol1-part2.md` | Ch 5-7 | Complete |
| 6 | `whitepaper-vol1-part3.md` | Ch 8-10 | Complete |
| 7 | **`whitepaper-vol1-part4.md`** | **Ch 11-12 + conclusion** | **this file** |

#### VERIFIED VOLUME I COMPLETE

**Remaining in the plan:**

| Document | Contents | Prerequisites |
|---|---|---|
| Vol II final installment | Meta-evaluation; LLM-judge reliability; deployment playbooks; the narrowing exercise (70 metrics -> a working set of 8-10) | Brehme survey read; three OPEN entries still open (Perçin, GainRAG method, Trust-Score components) |

The Volume II installment is the one that turns all of this into something operational: a decision
tree from "what kind of system do you have" to "instrument these eight things," plus the
meta-evaluation material on whether your judges can be trusted at all.

## Ledger from `whitepaper-supplement-A.md`

### Appendix A - Sourcing ledger for this supplement

| Metric | Read at | Formula/algorithm obtained? |
|---|---|---|
| eRAG | Abstract + method framing | Conceptual, not symbolic |
| DIG | Abstract + method statement | Conceptual (confidence differencing) |
| ΔSePer | **Algorithm 1, verbatim** | VERIFIED Full algorithm + both variants |
| Gain | Abstract + framing OPEN | No |
| WARG | Paper body (intro + RQ2) | Method named (IG + PMCSHAP), formula no |
| CUE | **Paper §III-B, verbatim** | VERIFIED Full construction + thresholds |
| MIRAGE ×4 | Paper body + repo + results discussion | Definitions + the diagnostic split |
| UDCG | **Paper §5, formula verbatim** | VERIFIED UDCG_θ equation |
| CKA family | Survey account + abstract OPEN | Instruments named, formulas no |
| VersionQA | Paper body (Tables 2 & 3) | VERIFIED Dataset composition + results |
| Retrieval Robustness | Abstract only OPEN | No - three metrics not defined |
| Query robustness | Abstract only OPEN | No |
| Latest@10 | Abstract only OPEN | Results yes, formula no |

Entries marked OPEN require another primary-source reading. Their descriptions stay within the
evidence obtained during this pass.

### Appendix B - Corrections issued by this supplement

1. **SePer is reference-based.** A widely-circulated summary claims it needs no ground truth.
   Algorithm 1 requires the reference answer `a*`. The summary is wrong.
2. **MIRAGE venue** - *Findings of* NAACL 2025, pp. 2883-2900, not the main conference.
3. **RAG-X's 14% gap** is Accuracy (71%) - Context Hit Rate (57.6%), not
   Accuracy - Effective Use (21.8%). These are different quantities.
4. **Four metrics, one measurement** - eRAG, Gain, DIG, ΔSePer are one family. Reporting all four
   is not corroboration.

## Ledger from `whitepaper-supplement-A-addendum.md`

### AD.3 Entries that remain open

Honesty about what this addendum did *not* close:

| Entry | Status | What is missing |
|---|---|---|
| **Query-level robustness** (Perçin et al., [2507.06956](https://arxiv.org/abs/2507.06956)) | OPEN still abstract-only | Metric definitions; the per-query aggregation scheme |
| **Latest@10 / temporal freshness** ([2509.19376](https://arxiv.org/abs/2509.19376)) | OPEN partially lifted | Results obtained and reported in Supp A; the Latest@10 formula itself not obtained |
| **Gain** (GainRAG, [2505.18710](https://arxiv.org/abs/2505.18710)) | OPEN still framing-level | The gain estimation method and middleware training detail |
| **FActScore** ([2305.14251](https://arxiv.org/abs/2305.14251)) | OPEN conceptual | Atomic-fact decomposition procedure |
| **Trust-Score components** ([2409.11242](https://arxiv.org/abs/2409.11242)) | OPEN conceptual | The sub-scores that compose it |

Supplements A and B describe these entries at the level supported by the available source material.


![Evidence boundary](assets/diagrams/fig-130-o-why-not-just-fill-those-in-you-know.png){.diagram-figure width=96%}


---

### AD.4 Revised sourcing ledger for Supplement A

| Metric | Was | Now |
|---|---|---|
| eRAG | Conceptual | Conceptual (unchanged) |
| DIG | Conceptual | Conceptual (unchanged) |
| ΔSePer | VERIFIED Algorithm 1 | VERIFIED (unchanged) |
| Gain | OPEN | OPEN (unchanged - see AD.3) |
| WARG | Method named | Method named (unchanged) |
| CUE | VERIFIED Full construction | VERIFIED (unchanged) |
| MIRAGE ×4 | VERIFIED Definitions + split | VERIFIED (unchanged) |
| UDCG | VERIFIED Formula | VERIFIED (unchanged) |
| **CKA family** | OPEN | VERIFIED **+ correction issued (AD.2)** |
| VersionQA | VERIFIED Composition + results | VERIFIED (unchanged) |
| **Retrieval Robustness** | OPEN | VERIFIED **Three metrics named + setup** |
| Query robustness | OPEN | OPEN (unchanged) |
| Latest@10 | OPEN | OPEN partial |

**New entries added by this addendum:** RARE-Met (2506.00789), reproduction study (2605.27105).

---

### AD.5 Running correction log across all documents

| # | Correction | Where | Whose error |
|---|---|---|---|
| 1 | AIS is *Computational Linguistics* 49(4), not TACL | Catalogue | **Mine** |
| 2 | SePer is reference-based; a popular summary says otherwise | Supp A | Third party |
| 3 | MIRAGE is *Findings of* NAACL 2025 | Supp A | Catalogue |
| 4 | RAG-X's 14% gap is Accuracy - Context Hit Rate | Supp A | User's framing |
| 5 | eRAG/Gain/DIG/ΔSePer are one family, not four | Supp A | Catalogue structure |
| 6 | RAGAS paper ≠ RAGAS library | Supp B | Field-wide |
| 7 | SURE-RAG is not a hallucination detector | Catalogue | Catalogue |
| 8 | PEER and DUO are fairness metrics, not Correctness | Catalogue | Catalogue |
| 9 | **CKA similarity does not imply retrieval similarity at small k** | **Supp A §B.2** | **Mine** |

Two of the nine are mine. Both came from describing something I had not read at method level - the
exact failure this document set was structured to avoid, occurring twice anyway.

---

### AD.6 What this changes for the reader

If you have been following along and acting on these documents:


![Decision map](assets/diagrams/fig-131-decision-map.png){.diagram-figure width=96%}


---

### Appendix AD-A - Documents in this set

| # | Document | Covers | Status |
|---|---|---|---|
| 0 | `ir-rag-metrics-catalogue-v2.md` | Full index, all dimensions | Complete, 4 verification passes |
| 1 | `whitepaper-vol1-part1.md` | Ch 0-4: dimensions, facets, signals, set metrics | Complete |
| 2 | `whitepaper-supplement-A.md` | Alignment, Integrity/Drift | Complete + this addendum |
| 3 | `whitepaper-supplement-B.md` | Correctness/Grounding, Efficiency/Cost | Complete |
| 4 | **`whitepaper-supplement-A-addendum.md`** | OPEN lifts + CKA correction | **this file** |

**Still to write:**

| Installment | Chapters | Contents |
|---|---|---|
| Vol I, 2 | 5-7 | Rank metrics (MRR, MAP, nDCG, ERR, RBP); incomplete judgments (bpref, infAP); rank comparison (τ, ρ, RBO) |
| Vol I, 3 | 8-10 | Diversity & novelty; fairness & exposure; online & counterfactual |
| Vol I, 4 | 11-12 | Significance & reporting; efficiency (classical) |
| Vol II, 8 | 22-24 | Meta-evaluation, judge reliability, deployment playbooks |

Volume I Installment 2 requires verifying five classical citations currently marked OPEN - ERR
(Chapelle et al., CIKM'09), RBP (Moffat & Zobel, TOIS'08), RBO (Webber, Moffat & Zobel, TOIS'10),
bpref (Buckley & Voorhees, SIGIR'04), and infAP (Yilmaz & Aslam, CIKM'06). Those verifications
happen before that installment ships, per the policy in Volume I's header.

## Ledger from `whitepaper-supplement-B.md`

### Appendix B1 - Sourcing ledger

| Metric | Read at | Definitions obtained? |
|---|---|---|
| RAGChecker ×9 | **Formal restatement of paper definitions** | VERIFIED All nine, precisely |
| RAGAS | Paper components + computation method | VERIFIED + library-drift discrepancy |
| ALCE | **Mechanism described in detail** | VERIFIED Leave-one-out precision |
| Citation faithfulness | Paper abstract + framing | VERIFIED Post-rationalization, 57% |
| Trust-Score | Paper abstract + results | VERIFIED Conceptual; components not itemized |
| TriFEX / PKP / PR | Paper abstract, verbatim | VERIFIED Including 75% variance finding |
| SURE-RAG | Paper abstract, verbatim | VERIFIED Four feature blocks + boundary experiment |
| FActScore | Title + abstract OPEN | Conceptual only |
| Index-time metrics | Brehme survey account | VERIFIED Four named metrics |
| RAG-X efficiency | **Paper Table IV** | VERIFIED Redundancy 22.0%, EHR@2 6.8% |

### Appendix B2 - Corrections and warnings issued

1. **RAGAS paper ≠ RAGAS library.** Paper: three metrics including Context Relevance. Library:
   four, commonly including context_recall - which is **reference-based**, breaking the
   reference-free claim that motivates choosing RAGAS.
2. **RAGChecker's Context Precision is chunk-level by design**, because claim-level precision has a
   corpus-dependent ceiling below 100%. Do not "fix" it to claim level.
3. **SURE-RAG is not a hallucination detector** - the paper's own boundary experiment shows the
   ranking reverses against GPT-4o on HaluBench.
4. **Hallucination rate is a proportion.** A model that generates fewer claims scores better without
   improving. Report claim counts alongside.
5. **Three papers named one failure independently:** RAG-X's Lucky Guess, RAGChecker's
   Self-Knowledge, Wallat et al.'s post-rationalization. Correct and ungrounded is the most
   under-measured category in RAG.

### Appendix B3 - Cross-supplement index of the recurring warning

The single point made in every part of this white paper so far:

| Location | Formulation |
|---|---|
| Vol I §1.3 | A faithfulness score is meaningless without a retrieval-hit denominator |
| Supp A §A.3.1 | The Adherence Paradox - 0.84 adherence, 33.9% ungrounded |
| Supp B §C.1.2 | The top-right quadrant survives every review |
| Supp B §C.4.6 | Do not dashboard Faithfulness without Claim Recall |
| Supp B §C.6.2 | Three independent papers, one failure mode |

If a reader takes nothing else from four documents, this is the thing to take.

## Ledger from `whitepaper-vol2-final.md`

### Appendix 5A - Final OPEN resolution

#### Trust-Score - components, now specified VERIFIED

**Source:** Song, Sim, Bhardwaj, Chieu, Majumder & Poria, ICLR 2025 **Oral** ·
[arXiv:2409.11242](https://arxiv.org/abs/2409.11242)

Trust-Score is a composite over **three dimensions**: response truthfulness, factual accuracy, and
attribution groundedness.


![Trust-Score Structure](assets/diagrams/fig-173-trust-score-structure.png){.diagram-figure width=96%}


**The design property that matters:** by penalizing both incorrect refusals and incorrect
non-refusals, F1_GR gives a balanced evaluation of the model's **over-responsiveness and
under-responsiveness**. That is exactly the abstention-quality measurement Supplement B §C.7 said
was missing - it was there, inside the composite, all along.

**The lineage worth noting:** Trust-Score's attribution half *is* ALCE's citation precision and
recall. Supplement B §C.5 and §C.7 describe two halves of one measurement tradition.

Benchmark composition, for calibration: ASQA (610 answerable / 338 unanswerable), QAMPARI (295/705),
ELI5 (207/793). Note how unanswerable-heavy QAMPARI and ELI5 are - which is why refusal handling
dominates the score there.

#### GainRAG - method, now specified VERIFIED

**Source:** Jiang, Zhao, Li, Wang & Qin, *GainRAG: Preference Alignment in Retrieval-Augmented
Generation through Gain Signal Synthesis*, **ACL 2025 Long Papers**, Vienna ·
[arXiv:2505.18710](https://arxiv.org/abs/2505.18710)

The full title resolves the ambiguity: this is **gain signal synthesis**, not gain measurement.

Method: estimate gain signals, then train a **middleware selector** that predicts which passages
provide positive generation gain - overcoming naive relevance by aligning retriever output with
generator benefit. A **pseudo-passage strategy** mitigates degradation. Trained on a small subset of
HotpotQA and WebQuestions; generalizes across 6 datasets. Baselines: StandardRAG, Self-RAG, and
BGE-Reranker-base, all at top-1.

**Confirms the §A.2.4 warning.** Gain is a training signal for a selector. Reporting it as a metric
on a system trained with it is circular. Use a held-out generator, or better, report something else.

#### Perçin et al. - remains OPEN

*Investigating the Robustness of Retrieval-Augmented Generation at the Query Level*, GEM 2025 ·
[arXiv:2507.06956](https://arxiv.org/abs/2507.06956). Existence and title verified VERIFIED; **metric
definitions not obtained.** Described in Supplement A §B.4.2 at abstract level only, and left that
way.

---

### Appendix 5B - Master document index

| # | Document | Covers |
|---|---|---|
| 0 | `ir-rag-metrics-catalogue-v2.md` | Complete indexed catalogue; 4 verification passes |
| 1 | `whitepaper-vol1-part1.md` | Ch 0-4: dimensions, facets, signals, set metrics |
| 2 | `whitepaper-vol1-part2.md` | Ch 5-7: rank metrics, incomplete judgments, rank comparison |
| 3 | `whitepaper-vol1-part3.md` | Ch 8-10: diversity, fairness, online/counterfactual |
| 4 | `whitepaper-vol1-part4.md` | Ch 11-12 + Vol I conclusion: significance, efficiency, time |
| 5 | `whitepaper-supplement-A.md` | Alignment; Integrity/Drift |
| 6 | `whitepaper-supplement-A-addendum.md` | OPEN lifts; CKA correction |
| 7 | `whitepaper-supplement-B.md` | Correctness/Grounding; Efficiency/Cost |
| 8 | **`whitepaper-vol2-final.md`** | **Ch 13-15: meta-eval, judges, narrowing** |

#### Where to start, by reader

| If you are... | Read |
|---|---|
| Deciding what to instrument tomorrow | **Ch 15** (this doc) |
| Debugging a RAG system that "should work" | Supplement A §A.3 (CUE, MIRAGE) |
| Choosing a retriever or embedder | Supplement A §B.2 + the Addendum correction |
| Choosing a generator | Supplement B §C.7 + Supplement A §A.3.2 |
| Building an eval set from scratch | Ch 14, then Vol I Ch 6 |
| Writing a paper | Vol I Ch 11 |
| Learning the field properly | Vol I in order, then the supplements |

#### Correction log - final

| # | Correction | Whose |
|---|---|---|
| 1 | AIS is *Computational Linguistics* 49(4), not TACL | **Mine** |
| 2 | SePer is reference-based; popular summary says otherwise | Third party |
| 3 | MIRAGE is *Findings of* NAACL 2025 | Catalogue |
| 4 | RAG-X's 14% gap = Accuracy - Context Hit Rate | User framing |
| 5 | eRAG/Gain/DIG/ΔSePer are one family | Catalogue structure |
| 6 | RAGAS paper ≠ RAGAS library | Field-wide |
| 7 | SURE-RAG is not a hallucination detector | Catalogue |
| 8 | PEER and DUO are fairness metrics | Catalogue |
| 9 | CKA similarity ≠ retrieval similarity at small k | **Mine** |

**Nine corrections. Two mine. Zero across 54 classical citations; nine across the RAG-era material.**

That distribution is the last finding, and it is a practical one: **verify anything from the last
two years before you build on it.** The old literature has been checked by many people. The new
literature - and especially its secondary summaries - has not.
