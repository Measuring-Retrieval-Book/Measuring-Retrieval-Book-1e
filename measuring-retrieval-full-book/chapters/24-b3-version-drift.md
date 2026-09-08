# B.3 Corpus & Version Drift - VersionQA

**One-line:** A benchmark of version-sensitive questions over evolving technical documentation,
measuring whether a system notices that a document *changed*.

**Facets:** Integrity/Drift | query | ref | E2E | EMERGING VERIFIED
**Source:** Huwiler, Stockinger & Fürst, *VersionRAG* ·
[arXiv:2510.08109](https://arxiv.org/abs/2510.08109)

### The problem it solves

Retrieval works by finding text that is semantically similar to the question, and semantic
similarity has no sense of time. A passage that was correct two years ago and has since been
superseded is still just as similar to the query as the passage that replaced it, so nothing in a
standard vector retrieval pipeline prefers the current one. The system then answers faithfully
from a document that is out of date, and every correctness metric in this book will call that a
success.

### The construction

VersionQA is 100 manually curated questions across 34 versioned technical documents, drawn from
Apache Spark changelogs covering versions 2.4.7 to 3.5.5, Bootstrap 5.2.3 to 5.3.5, and Node.js
documentation for Assert covering 11.15.0 to 23.11.0 and Errors covering 15.14.0 to 23.11.0.

Sixty percent of the queries require version-aware reasoning, spread across six categories.

| Category | Pairs | Version-sensitive |
|---|---|---|
| Content Retrieval | 20 | No |
| Content Retrieval Complex | 20 | No |
| Content Retrieval Version-Specific | 20 | **Yes** |
| Version Listing & Inquiry | 20 | **Yes** |
| Change Retrieval (Explicit) | 10 | **Yes** |
| Change Retrieval (Implicit) | 10 | **Yes** |

The last category is the hardest and the most revealing, because explicit change retrieval tells
the system a change occurred and asks what it was, while implicit change retrieval asks the system
to notice unprompted.

### The results

![Version-Sensitive Questions](assets/diagrams/fig-121-version-sensitive-questions.png){.diagram-figure width=96%}

On version-sensitive questions, naive RAG answered 58% correctly and GraphRAG 64%, against 90%
for the version-aware VersionRAG pipeline. On implicit change detection, meaning noticing an
undocumented modification without being told to look for one, the baselines scored between 0% and
10% while VersionRAG reached 60%.

That range of 0 to 10% is the most alarming number in this supplement. A team confident that their
RAG handles their documentation well should be asked whether it can say what changed between
version 2.1 and version 2.2 without being told that anything changed. Almost nobody's can.

Also worth noting for the efficiency dimension: VersionRAG requires 97% fewer tokens during
indexing than GraphRAG, which makes this one of the rare cases where a robustness improvement is
also cheaper to run.

### Advantages

- **Measures something nothing else measures.** Implicit change detection is invisible to every
  metric in Part A.
- **Small and runnable.** A hundred questions is a tractable benchmark to adapt to your own
  corpus.
- **The category breakdown is diagnostic,** so you can see whether you fail on explicit changes,
  implicit ones, or both.
- **Realistic corpus.** Software changelogs are genuinely versioned rather than synthetically
  aged, so the difficulty is real.

### Disadvantages

- **Domain-narrow,** being software documentation, so adapting it to legal, medical or financial
  versioning is real work rather than a configuration change.
- **Small n.** A hundred questions gives wide confidence intervals, so treat differences under
  about ten points cautiously.
- **It measures a benchmark rather than your corpus,** which means the right use for it is as a
  template.
- **A version-aware architecture is the paper's actual product,** and the benchmark is the
  supporting evidence for it.

### Domain examples

**Regulated policy documentation.** Standard operating procedures, compliance manuals and clinical
guidelines are all versioned and all safety-critical when stale. If your system returns the
superseded revision of a safety procedure, that failure is invisible to every correctness metric,
because the answer is perfectly faithful to the retrieved context.

**Software and API documentation.** The origin domain, so it applies directly.

**News and current events.** The hardest case, because versioning there is implicit and
continuous rather than marked by release numbers. §B.4 covers the temporal methods that apply.

### Recommendation

Build a 50-question version-sensitive set for your own corpus, using VersionQA's six-category
structure as the template, and weight it toward implicit change detection, since that is where
every baseline collapses.

Then run it quarterly. This is the only integrity metric in this part that directly measures the
failure your users will actually notice, because a stale answer looks entirely correct until
somebody acts on it.

---
