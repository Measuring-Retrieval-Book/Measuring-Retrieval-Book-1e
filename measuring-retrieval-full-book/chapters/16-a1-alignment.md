# A.1 What Alignment actually is

## A.1.1 The dimension in one page

Classical retrieval had one component, so it had one question to answer: was the ranking any
good? RAG has two components working in sequence, which creates a question classical retrieval
never had to ask.

> **Both components scored well. Why did the system fail?**

Alignment metrics exist to answer that question. They are not retrieval metrics and they are not
generation metrics, because both of those already exist and neither can see the problem. They
measure the interface between the two components.

![Why You Cannot Get This From Component Scores](assets/diagrams/fig-096-why-you-cannot-get-this-from-component-scores.png){.diagram-figure width=96%}

The figure lays out why component scores cannot be added together to give you this. On the
retriever side you have nDCG at 0.89, recall at 0.91 and MRR at 0.86. On the generator side you
have faithfulness at 0.84, with fluency and coherence both fine. In between the two, where the
retrieved documents are actually handed over and used or ignored, you have nothing at all.

A team looking at that dashboard will say both sides are excellent, and what they have done is
measure the two ends of a bridge while measuring nothing about the bridge.

## A.1.2 The four Alignment questions

Read across the literature, alignment metrics cluster into four distinct questions, and this
book uses the following synthesis of the published methods.

| # | Question | Family | Metrics |
|---|---|---|---|
| 1 | **What did this passage contribute?** | Contribution | eRAG, DIG, ΔSePer, Gain |
| 2 | **Did the generator use what the retriever ranked highly?** | Attribution | WARG |
| 3 | **Which component caused this failure?** | Quadrant | CUE, MIRAGE |
| 4 | **Is this ranking good *for an LLM* specifically?** | Machine-utility ranking | UDCG |

Picking one metric from each of the four families gives you far more diagnostic power than four
metrics drawn from family 1, and family 1 is where most teams accidentally end up, for reasons
§A.2.6 explains.

---
