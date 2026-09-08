# C.2 The claim-decomposition family

## C.2.0 The shared machinery

Nearly every modern grounding metric runs the same three-step pipeline, so it is worth
understanding once rather than four times.

![The Decomposition Pipeline](assets/diagrams/fig-134-the-decomposition-pipeline.png){.diagram-figure width=96%}

Step one is extraction, where a language model rewrites the answer into a list of atomic claims,
meaning standalone statements that can be understood on their own. Step two is verification, where
each claim is checked for entailment against some reference text, using either a natural language
inference model or a language model judge. Step three is aggregation, where the counts become a
ratio.

The figure works an example. The answer "Bern has been the capital since 1848 and has 133,000
residents" extracts into three claims: that Bern is the capital, that Bern became the capital in
1848, and that Bern has 133,000 residents. Verified against the retrieved context, the first two
are entailed and the third is not, so faithfulness comes out as 2/3 = 0.67.

The critical property is that what you verify against determines which metric you get. Same
extraction, same verifier, different reference text.

| Verify claims against... | You get |
|---|---|
| Retrieved context | Faithfulness |
| Ground-truth answer | Precision / Correctness |
| Each retrieved chunk individually | Context Precision, Noise Sensitivity |
| Nothing (claims *missing* from answer) | Recall |

This is why a single framework can produce nine metrics from one extraction pass. It is also why
those nine metrics cost far less together than separately, which is a point most teams miss when
they are budgeting for evaluation.

## C.2.1 FActScore - the ancestor

**One-line:** Decompose a long-form generation into atomic facts and score the precision of those
facts against a knowledge source.

**Facets:** Correctness | claim | judge | G | ESTABLISHED VERIFIED
**Source:** Min et al., EMNLP'23 · [arXiv:2305.14251](https://arxiv.org/abs/2305.14251)
OPEN Read at title and abstract level - *FActScore: Fine-grained Atomic Evaluation of Factual
Precision in Long Form Text Generation*.

FActScore establishes the lineage for everything in this part, because it made atomic-fact
decomposition the unit of factuality evaluation, and every metric in §C.3 through §C.5 is a
descendant of it. It measures precision only, meaning it asks what fraction of the claims in an
answer are supported, and says nothing about claims that should have been there and were not.
RAGChecker's Claim Recall is the recall counterpart, and it arrived later.

**Recommendation:** cite FActScore as the origin of the approach and deploy one of the
RAG-specific descendants rather than FActScore itself.

---
