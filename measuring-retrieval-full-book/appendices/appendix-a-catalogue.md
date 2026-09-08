```{=latex}
\begin{landscape}\scriptsize
```

# Appendix A: Consolidated Metric Catalogue

Every metric in this book in one table, tagged by the dimension it answers and by the three facets
from Chapter 2: the unit it counts, the supervision it needs, and the stage of the pipeline it
looks at. Use it to find a metric; use the chapter for what the metric actually means.

---

## Dimensions

| Dimension | Question it answers |
|---|---|
| **Correctness** | Is the retrieved/generated content actually right, relevant, grounded, cited correctly? |
| **Alignment** | Do retrieval and generation actually cooperate (interplay, utility, interference)? |
| **Integrity/Drift** | Is the substrate trustworthy *over time* (staleness, drift, test-set adequacy, corpus health)? |
| **Efficiency/Cost** | What does the answer cost in latency, tokens, compute, and index maintenance? |

Anything measuring latency, throughput, index size or token spend belongs under Efficiency/Cost,
because those quantities trade directly against correctness through rerank depth, k and chunk
size, and a trade-off cannot be reasoned about with one side missing from the table.

## Facets

| Facet | Values |
|---|---|
| **Unit** | claim · passage · query · session · corpus · system |
| **Supervision** | ref (reference-based) · free (reference-free) · judge (LLM-as-judge) · human |
| **Stage** | R (retriever-only) · G (generator-only) · E2E (end-to-end) |
| **Tier** | ESTABLISHED established · EMERGING emerging · o practitioner-only |

---

## 0. Signals & Parameters (NOT metrics - moved out of the metric tables)

These are things you tune or compute with rather than things you report, which is why none of them
carries a quality dimension. Chapter 3 sets out the distinction.

| Item | Kind | Source |
|---|---|---|
| tf, idf, tf-idf | ranking feature | Manning Ch. 6 |
| Cosine similarity, vector length normalization | similarity function | Manning Ch. 6 |
| BM25 score | ranking function | Manning Ch. 11 |
| BM25 k1, b | hyperparameter | Manning Ch. 11 |
| Query-likelihood, doc/collection LM probability | ranking function | Manning Ch. 12 |
| LM smoothing, Jelinek-Mercer interpolation λ | hyperparameter | Manning Ch. 12 |
| PageRank, HITS hub/authority | link-analysis feature | Manning Ch. 21 |
| Rocchio movement, +/- feedback weights | algorithm parameter | Manning Ch. 9 |
| # expansion terms, expansion term weights | hyperparameter | Manning Ch. 9 |
| Vocabulary size, doc/collection frequency, posting-list length | corpus statistic | Manning Ch. 2 |
| Candidate-set size, top-K | system parameter | Manning Ch. 7 |

> Their effect is still measurable, so relevance-feedback effectiveness and query-expansion
> effectiveness both remain legitimate alignment metrics below, because a knob becomes a metric
> at the point where you measure the difference it makes.

---

## 1. Classical IR - Set & Rank Quality

| Metric | Dim | Unit | Sup | Stage | Tier | Source |
|---|---|---|---|---|---|---|
| TP/FP/TN/FN | Correctness | query | ref | R | ESTABLISHED | Manning Ch. 8 |
| Precision, Recall, F-measure, F1, Fβ | Correctness | query | ref | R | ESTABLISHED | Manning Ch. 8 |
| PR curve, Interpolated Precision, 11-pt | Correctness | query | ref | R | ESTABLISHED | Manning Ch. 8 |
| Average Precision (AP), MAP | Correctness | query | ref | R | ESTABLISHED | Manning Ch. 8 |
| Precision@K, R-Precision, PR Break-even | Correctness | query | ref | R | ESTABLISHED | Manning Ch. 8 |
| ROC curve, TPR/FPR, ROC-AUC | Correctness | query | ref | R | ESTABLISHED | Manning Ch. 8 |
| CG, DCG, nDCG, graded relevance | Correctness | query | ref | R | ESTABLISHED | Manning Ch. 8 |
| **MRR / MRR@k** *(new)* | Correctness | query | ref | R | ESTABLISHED | standard; Voorhees TREC-8 QA |
| **Success@k / Hit Rate@k** *(new)* | Correctness | query | ref | R | ESTABLISHED | standard |
| **ERR - Expected Reciprocal Rank** *(new)* | Correctness | query | ref | R | ESTABLISHED | Chapelle et al., CIKM'09 |
| **RBP - Rank-Biased Precision** *(new)* | Correctness | query | ref | R | ESTABLISHED | Moffat & Zobel, TOIS'08 |
| Inexact top-K effectiveness | Correctness | query | ref | R | ESTABLISHED | Manning Ch. 7 |
| Relevance-feedback effectiveness | Alignment | query | ref | R | ESTABLISHED | Manning Ch. 9 |
| Query-expansion effectiveness (pseudo/global/thesaurus) | Alignment | query | ref | R | ESTABLISHED | Manning Ch. 9 |

**Why RBP matters for your §4:** it carries an explicit residual for unjudged documents, which is
what makes it the natural formal instrument for index-drift comparison in §5, since it reports how
much of the ranking nobody ever looked at.

### 1b. Incomplete & Unreliable Judgments *(new subsection)*

These are directly relevant to the test-set-adequacy theme in §3, because they measure
effectiveness in the case where your relevance judgments are sparse or came from a pool.

| Metric | Dim | Unit | Sup | Stage | Tier | Source |
|---|---|---|---|---|---|---|
| bpref | Correctness | query | ref | R | ESTABLISHED | Buckley & Voorhees, SIGIR'04 |
| infAP | Correctness | query | ref | R | ESTABLISHED | Yilmaz & Aslam, CIKM'06 |
| Pooling-depth bias | Integrity/Drift | corpus | ref | R | ESTABLISHED | Zobel, SIGIR'98 |
| Kappa / assessor agreement *(moved from NA)* | Integrity/Drift | corpus | human | R | ESTABLISHED | Manning Ch. 8 |
| Judgment-variation sensitivity | Integrity/Drift | corpus | human | R | ESTABLISHED | Voorhees, 1998 |

### 1c. Ranking Comparison & Stability *(new subsection)*

| Metric | Dim | Unit | Sup | Stage | Tier | Source |
|---|---|---|---|---|---|---|
| Kendall's τ, Spearman ρ | Integrity/Drift | query | free | R | ESTABLISHED | standard |
| **RBO - Rank-Biased Overlap** | Integrity/Drift | query | free | R | ESTABLISHED | Webber, Moffat & Zobel, TOIS'10 |

RBO is top-weighted and handles non-conjoint lists, meaning it can compare today's top-k against
last month's top-k even though the two lists contain different documents, which makes it the
closest off-the-shelf answer to the missing drift metric described in §5.

### 1d. Diversity, Novelty & Fairness *(new subsection)*

| Metric | Dim | Unit | Sup | Stage | Tier | Source |
|---|---|---|---|---|---|---|
| α-nDCG | Correctness | query | ref | R | ESTABLISHED | Clarke et al., SIGIR'08 |
| ERR-IA (intent-aware) | Correctness | query | ref | R | ESTABLISHED | Chapelle et al., 2011 |
| Subtopic recall | Correctness | query | ref | R | ESTABLISHED | Zhai et al., SIGIR'03 |
| Exposure / amortized fairness of attention | Correctness | system | ref | R | ESTABLISHED | Singh & Joachims, KDD'18 |
| Equity of attention | Correctness | system | ref | R | ESTABLISHED | Biega et al., SIGIR'18 |
| **PEER - Probability of Equal Expected Rank** *(relocated from §3)* | Fairness | query | ref | R | EMERGING | Yang et al., SIGIR'24 · [arXiv:2405.00978](https://arxiv.org/abs/2405.00978) |
| **DUO - Discounted Uniformity of Opinions** *(relocated from §3)* | Fairness | query | judge | R | EMERGING | Ziems et al., ACL'24 · [arXiv:2406.04298](https://arxiv.org/abs/2406.04298) |

| **Does RAG introduce unfairness?** - fairness of retrieved documents w.r.t. protected groups | Fairness | system | judge | E2E | EMERGING | Wu, Li, Wu, Tao & Fang, COLING'25 pp. 10021-10036 · [arXiv:2409.19804](https://arxiv.org/abs/2409.19804) |

Fairness in RAG is barely instrumented: across 63 surveyed RAG-evaluation papers, only **one**
evaluated whether retrieved documents fairly represent protected groups. If fairness matters for
your use case, you are close to the frontier and should expect to build the instrumentation.

**Two metrics that are commonly misfiled.** PEER measures whether documents in different languages
receive equal expected rank - a multilingual *fairness* criterion, not a relevance criterion. DUO
measures *indexical bias*: whether a ranked list over-represents one side of a contested question.
Both are routinely filed under correctness, which leads people to optimize them as quality
metrics. They are equity constraints, and their relationship to nDCG can be inverse.

Redundancy control matters more in RAG than it did in classical retrieval, because a duplicated
passage consumes context budget while adding no grounding at all. RAG-X in §3 formalizes this
through Pairwise Redundancy and Exclusive Hit Rate, having found that 22% of retrieved evidence
was redundant in their best pipeline even though recall looked adequate.

### 1e. Online & Counterfactual *(new subsection - entirely absent from v1)*

| Metric | Dim | Unit | Sup | Stage | Tier | Source |
|---|---|---|---|---|---|---|
| Interleaving (team-draft) preference | Correctness | session | human | R | ESTABLISHED | Radlinski et al., CIKM'08 |
| CTR, abandonment rate, reformulation rate | Correctness | session | human | E2E | ESTABLISHED | standard |
| Click-model-based relevance estimation | Correctness | query | human | R | ESTABLISHED | Chuklin et al., 2015 |
| IPS / off-policy ranking evaluation | Correctness | system | human | R | ESTABLISHED | Joachims et al., WSDM'17 |
| Task completion time, user satisfaction | Correctness | session | human | E2E | ESTABLISHED | Manning Ch. 8 |
| sDCG (session DCG) | Correctness | session | ref | R | ESTABLISHED | Järvelin et al., ECIR'08 |
| Time-biased gain | Efficiency/Cost | session | ref | E2E | ESTABLISHED | Smucker & Clarke, SIGIR'12 |

### 1f. Significance & Reporting *(new subsection)*

These evaluation controls make the metrics above meaningful.

| Item | Source |
|---|---|
| Paired randomization test | Smucker, Allan & Carterette, CIKM'07 |
| Multiple-comparison correction | standard |
| Effect size + CI reporting alongside point estimates | standard |

### 1g. Efficiency/Cost - classical *(reclassified from `NA`)*

| Metric | Dim | Unit | Sup | Stage | Tier | Source |
|---|---|---|---|---|---|---|
| Query response time / latency | Efficiency/Cost | query | free | R | ESTABLISHED | Manning Ch. 8 |
| Query throughput, indexing throughput | Efficiency/Cost | system | free | R | ESTABLISHED | Manning Ch. 4 |
| Index size | Efficiency/Cost | corpus | free | R | ESTABLISHED | Manning Ch. 5 |
| Query-processing cost | Efficiency/Cost | query | free | R | ESTABLISHED | Manning Ch. 7 |
| Crawl throughput | Efficiency/Cost | corpus | free | R | ESTABLISHED | Manning Ch. 20 |
| Crawl coverage, recrawl frequency, crawl freshness | Integrity/Drift | corpus | free | R | ESTABLISHED | Manning Ch. 20 |

---

## 2. RAG-Era - Foundational Anchors *(new section)*

The papers the rest of the field descends from.

| Metric / Framework | Dim | Unit | Sup | Stage | Tier | Citation |
|---|---|---|---|---|---|---|
| **RAGAS** - Faithfulness, Answer Relevance, Context Relevance | Correctness | claim | free/judge | E2E | ESTABLISHED | Es, James, Espinosa-Anke & Schockaert, EACL'24 demos pp. 150-158 · [arXiv:2309.15217](https://arxiv.org/abs/2309.15217) |
| **ALCE** - fluency, correctness, citation quality (citation precision/recall) | Correctness | claim | ref | E2E | ESTABLISHED | Gao, Yen, Yu & Chen, EMNLP'23 pp. 6465-6488 · [arXiv:2305.14627](https://arxiv.org/abs/2305.14627) |
| **AIS** - Attributable to Identified Sources CAUTION *venue corrected* | Correctness | claim | human | G | ESTABLISHED | Rashkin, Nikolaev, Lamm, Aroyo, Collins, Das, Petrov, Tomar, Turc & Reitter, ***Computational Linguistics* 49(4):777-840, 2023** - **not** TACL |
| **FActScore** - atomic-fact precision | Correctness | claim | judge | G | ESTABLISHED | Min et al., EMNLP'23 · [arXiv:2305.14251](https://arxiv.org/abs/2305.14251) VERIFIED |
| **RAGTruth** - word- and case-level hallucination annotation with intensity ratings | Correctness | claim | human | G | ESTABLISHED | Niu, Wu, Zhu, Xu, Shum, Zhong, Song & Zhang, ACL'24 pp. 10862-10878 · [arXiv:2401.00396](https://arxiv.org/abs/2401.00396) VERIFIED |
| **UMBRELA** - open reproduction of Bing relevance assessor | Correctness | passage | judge | R | ESTABLISHED | Upadhyay et al. · arXiv:2406.06519 |
| LLM relevance-assessment agreement at scale | Integrity/Drift | passage | judge | R | ESTABLISHED | Upadhyay et al. · arXiv:2411.08275 |

**RAGAS is reference-free**, which is why it dominates continuous-integration deployment, since it
needs no golden answers, while ALCE is reference-based. That distinction is exactly what the
`Supervision` column exists to surface, because it determines what you can run on every commit and
what you can only run offline.

### Survey anchor

Gan, Yu, Zhang et al. (2025), *Retrieval Augmented Generation Evaluation in the Era of Large
Language Models: A Comprehensive Survey* · [arXiv:2504.14891](https://arxiv.org/abs/2504.14891).
Reviews performance, factual accuracy, safety, **and computational efficiency** as co-equal axes -
independent support for promoting Efficiency/Cost out of `NA`.

---

## 3. RAG-Era - Verified Metrics (2024-2026)

All arXiv IDs below re-verified against arXiv records.

| Metric | Dim | Unit | Sup | Stage | Tier | Citation |
|---|---|---|---|---|---|---|
| eRAG - document-level downstream utility | Alignment | passage | free | E2E | ESTABLISHED | Salemi & Zamani, SIGIR'24 · [arXiv:2404.13781](https://arxiv.org/abs/2404.13781) |
| CAUTION **PEER** - Probability of Equal Expected Rank - *moved to §1d, this is a **language-fairness** metric* | ~~Correctness~~ -> Fairness | query | ref | R | EMERGING | Eugene Yang et al., *Language Fairness in Multilingual Information Retrieval*, SIGIR'24 · [arXiv:2405.00978](https://arxiv.org/abs/2405.00978) |
| CAUTION **DUO** - Discounted Uniformity of Opinions (PAIR) - *this is an **indexical-bias** metric* | ~~Correctness~~ -> Fairness | query | judge | R | EMERGING | Caleb Ziems et al., *Measuring and Addressing Indexical Bias in Information Retrieval*, ACL'24 · [arXiv:2406.04298](https://arxiv.org/abs/2406.04298) |
| GECE - Generative Expected Calibration Error *(introduced for **long-tail knowledge** detection)* | Alignment | query | free | E2E | EMERGING | Dongyang Li et al., *On the Role of Long-tail Knowledge in RA-LLMs*, ACL'24 · [arXiv:2406.16367](https://arxiv.org/abs/2406.16367) |
| nROUGE - Doc2Token | Correctness | query | ref | R | EMERGING | Kaihao Li, Lin & Lee (Walmart), eCom@SIGIR'24 · [arXiv:2406.19647](https://arxiv.org/abs/2406.19647) |
| **RAGChecker** - Claim Recall, Context Precision, Context Utilization, Noise Sensitivity, Hallucination, Self-Knowledge, Faithfulness | Correctness + Alignment | claim | judge | E2E | ESTABLISHED | Ru et al., NeurIPS'24 · [arXiv:2408.08067](https://arxiv.org/abs/2408.08067) |
| Citation correctness w/ over-citation adjustment | Correctness | claim | ref | G | EMERGING | Qian et al., CCIR'24 · [arXiv:2410.11217](https://arxiv.org/abs/2410.11217) |
| Fine-grained citation support (Full/Partial/None) | Correctness | claim | judge | G | EMERGING | Zhang et al. · [2406.15264](https://arxiv.org/abs/2406.15264) = [2408.12398](https://arxiv.org/abs/2408.12398) (LLM4Eval@SIGIR'24) - *one contribution, two versions* |
| Citation correctness and citation faithfulness (post-rationalization) | Correctness | claim | judge | G | EMERGING | Wallat et al. · [arXiv:2412.18004](https://arxiv.org/abs/2412.18004) |
| **MIRAGE** CAUTION *see naming note* - Noise Vulnerability, Context Acceptability, Context Insensitivity, Context Misinterpretation | Alignment | query | free | E2E | EMERGING | Park et al., NAACL'25 · [arXiv:2504.17137](https://arxiv.org/abs/2504.17137) |
| Retrieval Robustness (RAG ablation, #docs, doc-order) | Integrity/Drift | system | free | E2E | EMERGING | Cao et al. · [arXiv:2505.21870](https://arxiv.org/abs/2505.21870) |
| Query-level robustness under perturbation | Integrity/Drift | query | free | E2E | EMERGING | Perçin et al., GEM 2025 · [arXiv:2507.06956](https://arxiv.org/abs/2507.06956) |
| **GainRAG** - Gain (passage contribution to correct output) | Alignment | passage | free | E2E | EMERGING | Jiang et al., ACL'25 · [arXiv:2505.18710](https://arxiv.org/abs/2505.18710) |
| **InfoGain-RAG** - Document Information Gain (DIG) | Alignment | passage | free | E2E | EMERGING | Wang et al., EMNLP'25 · [arXiv:2509.12765](https://arxiv.org/abs/2509.12765) |
| Semantic Perplexity (SePer), ΔSePer | Alignment | query | ref | E2E | EMERGING | Dai et al., ICLR'25 Spotlight · [arXiv:2503.01478](https://arxiv.org/abs/2503.01478) |
| UDCG - Utility & Distraction-aware Cumulative Gain | Alignment | passage | ref | E2E | EMERGING | Trappolini et al., EACL'26 · [arXiv:2510.21440](https://arxiv.org/abs/2510.21440) |
| **RAG-E** - WARG (Weighted Attribution-Relevance Gap) | Alignment | passage | free | E2E | EMERGING | Randl, Rocchietti, Henriksson, Abedjan, Lindgren & Pavlopoulos · [arXiv:2601.21803](https://arxiv.org/abs/2601.21803) |
| **TriFEX** + PKP (Parametric Knowledge Precision), PR (Parametric Rate) | Correctness | claim | human-validated | G | EMERGING | Oestreich, Bley, Binder, Müller, Sydorenko & Alcalde · [arXiv:2603.23047](https://arxiv.org/abs/2603.23047) |
| **Trust-Score** *(not "TRUST-SCORE")* - holistic LLM trustworthiness in RAG; includes **correct refusal** + citation quality. Paired method: Trust-Align | Correctness | claim | ref | G | ESTABLISHED | Song, Sim, Bhardwaj, Chieu, Majumder & Poria, **ICLR'25 Oral** · [arXiv:2409.11242](https://arxiv.org/abs/2409.11242) |
| **SURE-RAG** - 3-way evidence sufficiency (supports / refutes / insufficient) | Correctness | passage-set | ref | E2E | EMERGING | Qiu, Han & Huang · [arXiv:2605.03534](https://arxiv.org/abs/2605.03534) |
| ARES - context relevance / faithfulness / answer relevance judges | Correctness | claim | judge | E2E | ESTABLISHED | Saad-Falcon, Khattab, Potts & Zaharia, NAACL'24 pp. 338-354 · [arXiv:2311.09476](https://arxiv.org/abs/2311.09476) |
| VERA - Validation and Evaluation of Retrieval-Augmented Systems | Correctness | query | judge | E2E | EMERGING | Ding, Banerjee, Mombaerts, Li, Borogovac & Weinstein, **Sep** 2024 · [arXiv:2409.03759](https://arxiv.org/abs/2409.03759) |
| AutoNuggetizer - nugget-based fact extraction/scoring | Correctness | claim | judge | E2E | ESTABLISHED | TREC 2024 RAG Track · arXiv:2411.09607 |
| RAGElo - Elo-based ranking of RAG variants | Correctness | system | judge | E2E | EMERGING | Rackauckas, Câmara & Zavrel · arXiv:2406.14783 |
| **RAGAlign@K** *(new)* - agreement between binary retrieval and binary generation outcome | Alignment | query | judge | E2E | EMERGING | arXiv:2602.06526 |
| **CUE - Context Utilization Efficiency** (RAG-X) - cross-references retrieval success against generator context-adherence (≥0.7) into four quadrants: Effective Use · Information Blindness · Hallucination "Lucky Guess" · Correct Rejection | Alignment | query | judge | E2E | EMERGING | Sivakumar, Sugumaran & Qiang (Oakland Univ.), *RAG-X: Systematic Diagnosis of RAG for Medical Question Answering* · [arXiv:2603.03541](https://arxiv.org/abs/2603.03541), 3 Mar 2026 |
| **Pairwise Redundancy** (RAG-X) - overlap between top-ranked contexts | Efficiency/Cost | passage | free | R | EMERGING | same paper - 22.0% measured at MAP 0.44 |
| **Exclusive Hit Rate (EHR@k)** (RAG-X) - % of queries where ground truth appears in only one retrieved context | Alignment | query | ref | R | EMERGING | same paper |
| **No-Hit Rate / Context-k Hit Rate** (RAG-X) | Correctness | query | ref | R | EMERGING | same paper |

### Three entries that are commonly misread

1. **SURE-RAG is not a hallucination detector.** The paper's own boundary-mapping experiment
   contrasts it with GPT-4o on HaluBench unsafe detection and finds the ranking *reverses*
   (0.3343 and 0.7389 unsafe-F1), concluding that controlled sufficiency verification and natural
   hallucination detection are distinct problems. Filing it next to Hallucination metrics invites
   exactly the misuse the authors warn against.

2. **PKP/PR is a warning about other metrics.** The paper's headline finding
   is that an existing knowledge-internalization metric is retrieval-sensitive, with roughly 75% of
   its cross-condition variance driven by PR (how often internal knowledge is expressed). That
   belongs in §6 as a meta-evaluation caution.

3. **WARG's failure modes deserve their own rows.** RAG-E names two: *wasted retrieval* (generator
   ignores the retriever's top-ranked document) and *noise distraction* (generator relies primarily
   on a lower-ranked document). Reported at 47.4-66.7% and 48.1-65.9% of queries respectively -
   these are diagnosable conditions.

### CAUTION Naming collision - "MIRAGE"

At least three distinct artifacts share the name. Disambiguate on every reference:

| Name | ID | What it is |
|---|---|---|
| MIRAGE (Park et al., NAACL'25) | 2504.17137 | RAG interaction-failure taxonomy - **your entry** |
| MIRAGE-Bench | 2410.13716 | Multilingual RAG benchmark arena |
| MiRAGE | 2510.24870 | Multimodal RAG evaluation |
| MIRAGE (medical) | 2402.13178 | Xiong, Jin, Lu & Zhang, ACL Findings'24 pp. 6233-6251 - *Benchmarking RAG for Medicine*, a **fourth** distinct MIRAGE |

Four artifacts, one name, no shared lineage. Always pair "MIRAGE" with an arXiv ID or venue.

---

## 4. RAG-Era - Coverage Gaps to Fill

Pending integration; each entry includes its purpose.

| Metric / Work | Dim | Why it belongs | Citation |
|---|---|---|---|
| Lost-in-the-Middle positional sensitivity | Alignment | UDCG's "LLM positional discount" operationalizes this; cite the phenomenon | Liu et al., TACL'24 · arXiv:2307.03172 |
| The Power of Noise | Alignment | Some irrelevant context *helps* - essential for interpreting Noise Sensitivity / Noise Vulnerability | Cuconasu, **Trappolini**, Siciliano, Filice, Campagnano, Maarek, Tonellotto & Silvestri, SIGIR'24 pp. 719-729 · arXiv:2401.14887 VERIFIED |
| **Sufficient Context** | Correctness | Direct parallel to SURE-RAG. Key findings: **models abstain *less* with RAG and hallucinate more than they abstain**, and 55.4% of Musique instances have insufficient context | Joren, Zhang, Ferng, Juan, Taly & Rashtchian, ICLR'25 · [arXiv:2411.06037](https://arxiv.org/abs/2411.06037) VERIFIED |
| BEIR - zero-shot retrieval transfer | Integrity/Drift | The domain-transfer measure this catalogue otherwise lacks | Thakur et al., NeurIPS D&B'21 · arXiv:2104.08663 VERIFIED |
| MTEB - Massive Text Embedding Benchmark | Integrity/Drift | Embedding-model selection & version drift | Muennighoff et al., EACL · arXiv:2210.07316 VERIFIED |
| FreshStack | Integrity/Drift | Realistic technical-document retrieval, freshness-aware | arXiv:2504.13128 |
| RAGBench | Correctness | Explainable RAG benchmark w/ TRACe framework | arXiv:2407.11005 |
| RULER / needle-in-haystack | Alignment | The null hypothesis: is retrieval earning its keep with long context? | - |
| **Abstention quality**: refusal rate, IDK-precision, coverage-risk curves | Correctness | CAUTION *Gap partially closed* - Trust-Score (§3) scores correct refusal; SURE-RAG emits a selective score at a coverage threshold. *Sufficient Context* shows that **models abstain less once RAG is added, and hallucinate more than they abstain.** Retrieval actively suppresses the desired behaviour. A coverage-risk curve is the minimum instrument | selective-prediction literature + arXiv:2411.06037 |
| MultiHop-RAG | NA (dataset) | Multi-hop query benchmark | Tang & Yang · arXiv:2401.15391 |
| FRAMES - *Fact, Fetch and Reason* | NA (dataset) | Unified RAG evaluation, multi-hop | Krishna et al., NAACL'25 pp. 4745-4759 · arXiv:2409.12941 |
| CRAG - Comprehensive RAG Benchmark | NA (dataset) | Broad-coverage benchmark | Yang et al. · arXiv:2406.04744 |
| FaithEval | Correctness | Faithfulness under counterfactual/unanswerable context | Ming et al. · arXiv:2410.03727 |
| Lynx | Correctness | Open-source LLM *trained* to detect hallucination - a judge you can pin | Ravi et al. · arXiv:2407.08488 |
| Long²RAG - Key Point Recall (KPR) | Correctness | Long-context, long-form generation | Qi et al. · arXiv:2410.23000 |
| Sub-question coverage | Correctness | Does the answer cover what matters? Decompositional | Xie, Laban, Choubey, Xiong & Wu · arXiv:2410.15531 |
| CoFE-RAG - full-chain evaluation | Alignment | Evaluates every stage and the endpoints | Liu et al. · arXiv:2410.12248 |
| RAGProbe | Integrity/Drift | Automated scenario probing of RAG apps | Sivasothy et al. · arXiv:2409.19019 |
| ReEval | Integrity/Drift | Hallucination eval via transferable adversarial attacks | Yu et al., NAACL'24 Findings pp. 1333-1351 |
| BERGEN | NA (library) | Benchmarking library - reproducibility infrastructure | Rau et al. · arXiv:2407.01102 |
| RAG-QA Arena | Correctness | Domain robustness, long-form | Han et al. · arXiv:2407.13998 |
| CORAL | Correctness | Multi-turn conversational RAG | Cheng et al. · arXiv:2410.23090 |
| **Agentic RAG**: retrieval calls per answer, redundant-query rate, search efficiency | Efficiency/Cost | Iterative and agentic retrieval have almost no measurement vocabulary | emerging |
| Trustworthy-RAG survey (safety, privacy, robustness) | Integrity/Drift | Covers the safety axis, which this catalogue does not | arXiv:2502.06872 |

### Efficiency/Cost - RAG-specific *(new)*

| Metric | Unit | Notes |
|---|---|---|
| Prompt/context tokens per query | query | Trades directly against k and rerank depth |
| Wasted-context ratio | query | VERIFIED **Now has a published instrument**: RAG-X's Pairwise Redundancy + EHR@k (arXiv:2603.03541). Pairs with WARG |
| Time-to-first-token | query | Dominant perceived-latency term |
| Retrieval calls per answer | query | Agentic RAG only |
| Index build + refresh cost | corpus | The recurring term everyone omits at design time |

---

## 5. Integrity / Drift

| Metric | Dim | Unit | Sup | Tier | Source |
|---|---|---|---|---|---|
| Index drift (schema / semantic / staleness layers) | Integrity/Drift | corpus | free | o | practitioner blogs, 2026 |
| Context trustworthiness (freshness, ownership, lineage, canonical alignment) | Integrity/Drift | corpus | free | o | Atlan, Apr 2026 |
| Retrieval confidence decay (declining top-K similarity over time) | Integrity/Drift | query | free | o | practitioner, 2026 |
| Per-class embedding drift (centroid/cosine shift by query class) | Integrity/Drift | corpus | free | o | dev.to, May 2026 |
| Query-document alignment score (cross-encoder and vector disagreement) | Integrity/Drift | query | free | o | C# Corner, 2026 |
| **Latest@10 / recency-prior freshness** *(new)* | Integrity/Drift | query | ref | EMERGING | [arXiv:2509.19376](https://arxiv.org/abs/2509.19376) |
| **VersionQA accuracy** *(new)* - 100 curated questions over 34 versioned technical docs; 60% version-sensitive | Integrity/Drift | query | ref | EMERGING | Huwiler, Stockinger & Fürst · [arXiv:2510.08109](https://arxiv.org/abs/2510.08109) VERIFIED |
| **RBO(top-k_t, top-k_{t-1})** *(proposed)* | Integrity/Drift | query | free | ESTABLISHED (borrowed) | Webber et al., TOIS'10 |
| **CKA - Centered Kernel Alignment** *(new)* - similarity between embedding-model representations | Integrity/Drift | corpus | free | EMERGING | Caspari, Dastidar, Zerhoudi, Mitrovic & Granitzer · [arXiv:2407.08275](https://arxiv.org/abs/2407.08275) |
| **Jaccard similarity of retrieved sets** *(new)* | Integrity/Drift | query | free | EMERGING | same paper |
| **RankSimilarity** *(new)* - rank-aware overlap of retrieved chunks | Integrity/Drift | query | free | EMERGING | same paper |

### CAUTION Use the published instrument

*Beyond Benchmarks: Evaluating Embedding Model Similarity for RAG Systems* (arXiv:2407.08275)
supplies exactly what §5 was missing: CKA for comparing embedding-model representations, plus
Jaccard and RankSimilarity for comparing the retrieved sets those models produce. Together with RBO that gives you a **fully sourced drift stack**, so you do not have to rely on the
ad-hoc mean-cosine-distance thresholds circulating in practitioner blogs, none of which have any
published validation behind them.

Apply it in two directions. Across models, it asks whether swapping the embedder changed what
surfaces, and across time it asks whether the corpus drifted while the embedder stayed fixed. The
instrument is the same in both cases and only the comparison axis differs.

### The state of drift measurement

No formal adaptation of the standard distribution-shift tests to retrieval sets has been
published. Two works partially cover the space:

- *Freshness and the Limits of Heuristic Trend Detection in Temporal RAG* (2509.19376) reports that
  freshness via a recency prior is partial and parameter-sensitive. It is a
  citable **negative result**, which is stronger than "not found in literature."
- VersionRAG/VersionQA quantifies the cost of staleness: standard RAG reaches 58% accuracy on
  version-sensitive questions and GraphRAG 64%, against 90% for a version-aware pipeline. The
  sharper number is **implicit change detection** - tracking undocumented modifications - where
  VersionRAG reaches 60% and the baselines score **0-10%**. If your corpus is versioned technical
  documentation, that near-zero baseline is the single most alarming figure in this catalogue.

**Recommendation:** stop treating drift as unmeasurable and adopt RBO as the interim formalism,
since it is top-weighted, handles non-conjoint lists, carries a residual term for unjudged items,
and has twenty years of retrieval literature behind it. That makes it a better default than any of
the centroid-distance thresholds circulating in practitioner blogs.

---

## 6. Meta-Evaluation - Evaluating the Evaluators

| Metric | Dim | Unit | Tier | Source |
|---|---|---|---|---|
| Semantic Test Coverage (basic / weighted / multi-cluster) | Integrity/Drift | corpus | EMERGING | [arXiv:2510.00001](https://arxiv.org/abs/2510.00001) |
| Coverage & Rigor (BenchmarkQED: AutoQ / AutoE / AutoD) CAUTION *software suite, not a paper* | Integrity/Drift | corpus | EMERGING | Microsoft Research · github.com/microsoft/benchmark-qed - AutoQ synthesizes local<->global queries; AutoE scores relevance, comprehensiveness, diversity, empowerment; AutoD curates datasets |
| Leakage / contamination detection in synthetic benchmarks | Integrity/Drift | corpus | EMERGING | [arXiv:2605.08838](https://arxiv.org/abs/2605.08838) |
| Diversity + privacy-leakage scoring of synthetic QA sets | Integrity/Drift | corpus | EMERGING | [arXiv:2508.18929](https://arxiv.org/abs/2508.18929) |
| **Judge-human agreement (Krippendorff's α)** *(new)* | Integrity/Drift | claim | ESTABLISHED | use α, not κ - you will have >2 raters |
| **Judge position bias** *(new)* | Integrity/Drift | query | ESTABLISHED | LLM-as-judge literature |
| **Judge verbosity bias** *(new)* | Integrity/Drift | query | ESTABLISHED | LLM-as-judge literature |
| **Judge self-preference bias** *(new)* | Integrity/Drift | query | EMERGING | Panickssery et al., 2024 |
| **Judge-model version drift** *(new)* | Integrity/Drift | system | o | - |
| **Metric confounding audit** *(new)* | Integrity/Drift | system | EMERGING | generalizes the PKP/PR finding, 2603.23047 |
| *(gap - no "mutation kill rate" for RAG test suites)* | Integrity/Drift | corpus | - | open |

**Judge-model version drift is the most underrated metric in this entire catalogue** - and this is
no longer just my assertion. A systematic review of 63 RAG-evaluation papers (Brehme, Ströhle & Breu,
SDS'25 · [arXiv:2504.20119](https://arxiv.org/abs/2504.20119)) raises exactly this: advances in
models could invalidate previous evaluation results, since a new model may produce entirely
different outcomes, leaving open how to establish a standard that stays consistent independent of
LLM version. Pin judge versions, and re-run a frozen anchor set on every judge change.

**The empirical case is weak.** Of those 63 papers, **41 used LLMs as judges. Six compared LLM
judges against human judges** - and those six found merely a positive correlation,
which is a weak bar. The same review flags the circularity directly: when one LLM generates the
questions, answers them, and then evaluates its own output, it is unclear whether evaluation quality
survives. If your pipeline uses an LLM for synthetic test generation *and* for judging, you are
inside that loop. Budget for a human-labelled anchor set; there is no published evidence that
full automation is safe.

**Metric confounding audit** generalizes the PKP and PR result, which is that before trusting any
composite metric across conditions you should decompose its variance, because a metric where
roughly 75% of the cross-condition movement comes from an expression-rate term is measuring the
wrong target.

---

## 7. Provenance & Confidence Notes

Anything marked o is practitioner-only, meaning it comes from industry writing rather than
peer-reviewed work, and it should never be reported alongside an ESTABLISHED entry without that
tier visible. Mixing peer-reviewed metrics with blog-post heuristics in one table is how
unvalidated thresholds acquire an authority nobody granted them.

### The Accuracy Fallacy - and one arithmetic caution

RAG-X's headline result on GuidelineQA (Llama-3.1-8B + Qwen3-Embedding-8B, α=1, MAP 0.44):

| Quadrant | Share |
|---|---|
| Effective Use - grounded success | 49.2% |
| Hallucination / "Lucky Guess" - right answer, no supporting evidence | 33.9% |
| Information Blindness - evidence retrieved, generator missed it | 8.5% |
| Correct Rejection - implied remainder | ~8.4% |

CAUTION **The 14% gap is not accuracy-minus-Effective-Use.** The paper defines it as the gap between
**Accuracy (71%) and Context Hit Rate (57.6%)** - i.e. 71 - 57.6 ≈ 13.4%. The distance from 71% to
49.2% Effective Use is ~22 points, a different and larger quantity. Quoting "a 14-point gap between
accuracy and grounded answers" merges the two and will not reconcile if anyone checks. State them
separately.

Note also that Context Adherence scored **0.84** on the same pipeline - the generator looked highly
faithful. A third of its correct answers were ungrounded. This is the **Adherence Paradox**,
and it is the strongest single argument in the catalogue for why adherence/faithfulness scores must
never be reported without a retrieval-hit denominator beside them.


```{=latex}
\end{landscape}
```
