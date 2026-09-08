# C.3 RAGAS

**One-line:** Reference-free evaluation of RAG on three axes: is the answer grounded, does it
answer the question, and was the context relevant?

**Facets:** Correctness | claim | free/judge | E2E | ESTABLISHED VERIFIED
**Source:** Es, James, Espinosa-Anke & Schockaert, **EACL 2024 System Demonstrations,
pp. 150-158**, doi 10.18653/v1/2024.eacl-demo.16 ·
[arXiv:2309.15217](https://arxiv.org/abs/2309.15217)

### The problem it solves

Every claim-level method in §C.2 needs something to verify against, and the obvious candidate is a
ground-truth answer somebody wrote. Most teams starting out do not have those and cannot afford to
build them, which means they measure nothing at all. RAGAS exists to give you numbers on day one
by verifying the answer against the retrieved context rather than against a reference.

## C.3.1 CAUTION Paper and library drift - read this before citing RAGAS

The paper defines three components, being Faithfulness, Answer Relevance and Context Relevance.

The library, as commonly used and documented, reports four, being faithfulness, answer relevancy,
context precision and context recall, with context relevance largely superseded.

![The Citation Trap](assets/diagrams/fig-135-the-citation-trap.png){.diagram-figure width=96%}

The figure works the resulting exchange. A team says they evaluated with RAGAS and cites Es et al.
2024. Asked which metrics they reported, they name faithfulness, answer relevancy, context
precision and context recall. Two of those four do not appear in the paper they cited, and
context_recall is not reference-free, so their claim to have done reference-free evaluation is
wrong as well.

Two consequences matter. Citing the paper does not describe your setup, so if you report
context_recall you need to cite the library version alongside the paper. And the reference-free
claim breaks, because the paper's entire selling point is evaluation without ground-truth
annotations while Context Recall requires a reference answer. The moment you add it, RAGAS is no
longer reference-free, and the main reason you chose it has evaporated.

## C.3.2 How the metrics are computed

**Faithfulness** runs the pipeline from §C.2. A language model rewrites the answer into standalone
atomic statements, each statement is checked for entailment against the retrieved context, and the
score is the number of supported statements divided by the total.

**Answer Relevance** is computed by an inversion that is worth understanding, because it is
cleverer than it first appears and its blind spot follows directly from the design.

![Answer Relevance Runs Backwards](assets/diagrams/fig-136-answer-relevance-runs-backwards.png){.diagram-figure width=96%}

Rather than comparing the answer to the question, it generates questions from the answer and then
measures how similar those are to the question that was actually asked. Given the question "what
is the capital of Switzerland?" and the answer "Bern is the capital", the synthetic questions come
back as "what is the capital of Switzerland?" and "which city is Switzerland's capital?", which
are highly similar to the original, so the answer scores as relevant. Given the off-topic answer
"Switzerland has 26 cantons", the synthetic question is "how many cantons does Switzerland have?",
which is not similar, so the answer scores as irrelevant.

The blind spot is specific. This measures topicality rather than correctness, so a confidently
wrong answer to exactly the right question scores high on Answer Relevance.

## C.3.3 Advantages

- **Reference-free in its paper form,** which is the genuine differentiator and the reason it
  dominates adoption in continuous integration.
- **Cheap and fast** relative to any form of human evaluation.
- **Component-separated,** since faithfulness targets the generator while context relevance
  targets the retriever.
- **Ubiquitous,** with an enormous ecosystem and integrations everywhere, so a new engineer can
  run it on their first day.

## C.3.4 Disadvantages

- **Heuristic prompts that do not transfer.** This is the most substantive published criticism,
  and the ARES authors make it directly: RAGAS's carefully designed heuristic scoring prompts
  often fail to adapt when applied to new domains or corpora. If your domain sits far from the
  assumptions those prompts encode, the scores degrade in ways you will not see happening.
- **Faithfulness is not correctness.** A faithfulness of 0.8 means 20% of the statements are
  unsupported, and it says nothing at all about whether the supported 80% are true. An answer
  faithful to a wrong context scores perfectly.
- **It is a hallucination-rate proxy rather than a severity measure.** A faithfulness of 0.8 where
  the unsupported fifth happens to contain the refund amount or the drug dosage is not the same
  thing as 0.8 where the unsupported fifth is pleasantries.
- **Averaging the four into a single RAGAS Overall is common and wrong.** Some implementations
  report the arithmetic mean of context precision, context recall, faithfulness and answer
  relevance. Those have different units of analysis, and averaging across units is exactly what
  Volume I §2.1 warns against.
- **Depends on a language model judge,** so it inherits all of the judge-drift exposure from
  Supplement A §B.5.

## C.3.5 Domain examples

**Startup or early-stage RAG.** The right first choice. Being reference-free means you can measure
something on day one without an annotation budget, and something beats nothing decisively.

**Regulated enterprise.** Insufficient on its own, because faithfulness without a retrieval-hit
denominator reproduces exactly the Adherence Paradox from Supplement A §A.3.1. Pair it with CUE or
with RAGChecker's Self-Knowledge.

**Specialized technical domains** such as semiconductors, clinical coding or tax law. These carry
the highest risk of the prompt-transfer problem, so validate RAGAS scores against a small
human-labelled set in your own domain before trusting the aggregate. If agreement is poor, the
framework is not broken, it is out of domain.

## C.3.6 Recommendation

Use RAGAS as your entry-level, always-on continuous integration metric, in its paper-faithful
three-metric form, and be precise about which version you are citing.

The moment you add context_recall you have crossed into reference-based evaluation, so make that
choice deliberately and compare it against RAGChecker, which does reference-based claim-level
diagnosis considerably more thoroughly.

Never report a single averaged RAGAS score, because the decomposition is where all the value is.

---
