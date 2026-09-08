# 1. The Four Questions

Retrieval evaluation starts with four questions.

![The four questions](assets/diagrams/four-dimensions.png)

| Dimension | Question | Typical failure it catches |
|---|---|---|
| Correctness | Is the retrieved or generated content right? | Irrelevant result, unsupported answer, wrong citation |
| Alignment | Do the retriever and generator cooperate? | The answer is correct while retrieval contributed little |
| Integrity | Has the system changed over time? | Embedder drift, corpus drift, judge drift |
| Efficiency | What did quality cost? | Latency, token waste, redundant context, rebuild expense |

<div class="law">
Every dashboard should answer all four questions. Many teams answer the first question many times.
</div>

Correctness is the local question. It asks whether a document, claim, answer, or citation passes a judgment.

Alignment is the system question. It asks whether the retrieved evidence helped the generator produce the answer.

Integrity is the time question. It asks whether the score has the same meaning after a release, model change, corpus update, or judge change.

Efficiency is the resource question. It asks whether the extra quality is worth the latency, tokens, engineering work, and operational risk.
