# D.3 Query-time metrics

## D.3.1 The standard set

| Metric | Facet | Note |
|---|---|---|
| **Query latency / response time** | query | Manning Ch. 8 - the classical measure |
| **Time-to-first-token (TTFT)** | query | Dominant *perceived* latency in streaming UIs |
| **Query throughput** | system | Manning Ch. 4 |
| **Query-processing cost** | query | Manning Ch. 7 |
| **Retrieval calls per answer** | query | **Agentic RAG only** - see §D.5 |

## D.3.2 Why TTFT matters more than total latency

Time-to-first-token is how long the user stares at an empty screen before anything appears, and in
any interface that streams its output, that wait is what people actually experience as speed.

![Two Systems, Same Total Latency](assets/diagrams/fig-151-two-systems-same-total-latency.png){.diagram-figure width=96%}

The figure compares two systems with identical total latency of 4.2 seconds. System A produces
four seconds of silence and then delivers the whole answer at once, so its TTFT is 4.0 seconds.
System B starts producing tokens after 0.6 seconds and streams the rest, so its TTFT is 0.6
seconds.

System A feels broken and system B feels fast, and a dashboard reporting total latency cannot tell
them apart.

Retrieval happens before the first token can be produced, which means your retrieval latency is
part of TTFT rather than something hidden inside a longer process. That is the strongest argument
for measuring retrieval speed as a quantity in its own right, because it is precisely the part the
user waits through with nothing on screen.

## D.3.3 Recommendation

Report TTFT at the median and the 95th percentile rather than mean total latency. Means hide the
tail, and the tail is what generates support tickets. If a reranker adds 200 milliseconds at the
median and three seconds at the 95th percentile, the median figure will justify shipping it and
the 95th percentile figure is what users meet on bad days.

---
