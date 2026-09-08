# 2. Facets

A metric needs a label before it needs a number. The label has four facets.

| Facet | Values | Use |
|---|---|---|
| Unit | document, passage, claim, answer, session, system | Tells what item receives a score |
| Supervision | judged, reference-based, reference-free, behavioral | Tells where truth comes from |
| Stage | retrieval, generation, citation, evaluation, deployment | Tells which layer owns the fix |
| Tier | diagnostic, release gate, monitor, audit | Tells how often to compute it |

<div class="decision">
Write the facet line under every metric name. A reader should know where the number lives before seeing the formula.
</div>

Two metrics can share a formula shape and answer different product questions. Precision over retrieved documents, citation precision over cited passages, and claim precision over generated assertions belong to different operational layers.

The unit matters most. A claim-level score can improve when answers become shorter. A document-level score can improve while citations stay wrong. A session score can hide one catastrophic answer inside a long interaction.

The stage matters next. Retrieval teams can act on nDCG, recall, and redundancy. Generator teams can act on claim support and citation faithfulness. Platform teams can act on latency, token cost, and judge stability.
