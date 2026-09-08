# 3. Signals Need Decisions

A signal is an observation. A metric is a decision instrument.

Mean embedding distance is a signal. Token count is a signal. Number of retrieved chunks is a signal. They become metrics when paired with a defined decision, threshold, or comparison.

<div class="recipe">
Use this test: if the number moves, can the team name the action? If yes, it is ready for the dashboard. If no, keep it in the analysis notebook.
</div>

Common signals in retrieval work:

| Signal | Useful action |
|---|---|
| Retrieved chunk count | Debug fanout and routing |
| Mean similarity | Inspect retriever confidence |
| Token count | Estimate cost |
| Query length | Segment traffic |
| Judge confidence | Prioritize human review |

Production metrics should be boring. They should send engineers to the correct subsystem.
