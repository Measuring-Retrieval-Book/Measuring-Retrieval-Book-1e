# 8. Design Review Rules

## Rule 1. Faithfulness travels with retrieval hit rate

Faithfulness scores generated support. Retrieval hit rate scores whether the required evidence arrived. A team needs both numbers on one row.

## Rule 2. Relevance labels give partial evidence of generator utility

A passage can be topically relevant and harmful to reasoning. A passage can be tangential and useful. Use a contribution metric when generation is the product surface.

## Rule 3. Judge changes are system changes

A new judge can move scores while the product stays fixed. Pin the judge. Re-score the anchor set. Report alpha.

## Rule 4. Cost belongs in the same review as quality

Latency and tokens shape the feasible system. The cost-quality frontier is the artifact that lets a team choose a point deliberately.

## Rule 5. The metric should name the owner

Retriever, generator, evaluation, platform, and product teams need separate accountability. A metric that names no owner becomes ceremony.


## Rule 6. Name the denominator

A rate without its denominator invites misreadings. Claim rate, answer rate, query rate, and session rate can all move differently.

## Rule 7. Keep the failure sample

Every release review should include sampled failures beside aggregate scores. The sample teaches the team what the number means this week.

## Rule 8. Use expensive metrics as diagnostics

Some metrics are too costly for every build. Run them during release review, incident review, and method evaluation. Promote only the cheap, stable, high-signal subset to continuous monitoring.
