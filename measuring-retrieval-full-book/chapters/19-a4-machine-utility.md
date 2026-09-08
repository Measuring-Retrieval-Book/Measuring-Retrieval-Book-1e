# A.4 Family 4 - Machine-Utility Ranking

## A.4.1 UDCG - Utility and Distraction-aware Cumulative Gain

**One-line:** nDCG rebuilt for a language-model reader, with a learned positional discount and
*negative* weight for distracting passages.

**Facets:** Alignment | passage | ref | R | EMERGING VERIFIED
**Source:** Trappolini et al., EACL 2026 · [arXiv:2510.21440](https://arxiv.org/abs/2510.21440)

### The problem it solves

Every ranking metric in Volume I was built around a person reading down a list and losing
interest. The reader in a RAG system is a language model that receives the whole prompt at once,
so the assumption the metrics were built on no longer describes anybody.

The paper identifies two distinct misalignments, and this is the cleanest statement of the
problem anywhere in the literature.

The first is the machine position discount. nDCG, MAP and MRR all assume the reader examines
documents in order with diminishing attention as they go down, while a language model processes
all the retrieved documents as a whole.

The second is machine utility, and it is the deeper one. Classical metrics have no way to
represent a document that actively degrades the answer. In classical retrieval, an irrelevant
document at rank 5 costs you a slot. In RAG, it can cost you the answer.

![The Sign Problem](assets/diagrams/fig-113-the-sign-problem.png){.diagram-figure width=96%}

The figure names this the sign problem. In classical retrieval, relevance runs from 0 to 3, so an
irrelevant document has a gain of zero and costs you a slot. In RAG, utility can be negative, so a
distracting document has a gain below zero and costs you the answer. When nDCG says a document
contributes zero, it may in fact be contributing negatively, and nDCG has no way to express that.

### The idea

![UDCG formula](assets/diagrams/fig-114-udcg-q-c-1-u-1-u.png){.diagram-figure width=96%}

Reading the formula, each passage's utility is split into a positive part and a negative part,
written u+ and u-. Each of those gets its own positional weight, α for the relevant contribution
and β for the distracting one. The two weighted sums are added and passed through a sigmoid
function, written σ, which squashes the result into the range 0 to 1 so that averaging across
questions behaves sensibly.

That gives 2k learnable parameters for a list of length k, and they are fitted with a linear model
over the feature vector of positive and negative utilities, trained to predict end-to-end answer
accuracy.

Note what that last clause means, because it is the real departure. UDCG's positional discount is
not assumed, it is learned from your data so as to maximize correlation with answer accuracy.
nDCG's 1/log2(i+1) is a model of human attention that somebody wrote down in 2002. UDCG's α is an
empirical fact about your generator.

### Reported results

Across five datasets and six language models, UDCG improves correlation with end-to-end answer
accuracy by up to 36% over the traditional metrics.

### Advantages

- **Models distraction with a negative term,** which is structurally impossible in nDCG no matter
  how you configure it.
- **Learned position weights** reflect the generator you actually run rather than a twenty-year-old
  model of human attention.
- **Directly optimized for the thing you care about,** namely correlation with answer accuracy.
- **Bounded between 0 and 1** through the sigmoid, so averaging across questions is well behaved.

### Disadvantages

- **Requires utility annotations covering both positive and negative cases,** which is a new and
  more expensive annotation schema than binary or graded relevance.
- **The 2k parameters have to be fitted,** which needs end-to-end accuracy labels, so you are
  training a metric before you can use it.
- **Generator-specific and k-specific.** Change the model or change k and the weights are stale,
  so every UDCG number is implicitly conditioned on a particular model and context size.
- **Not comparable across systems** unless they share the fitted weights, which undercuts the main
  reason people like nDCG in the first place.
- **The newest metric here,** with the least independent replication behind it.

### Domain examples

**A stable, long-lived production pipeline.** The best fit. If your generator and your k are
stable for quarters at a time, fitting the weights once is a sound investment and gives you the
most accuracy-predictive retrieval metric available.

**Rapid model iteration.** A poor fit, because swapping generators monthly means refitting the
metric monthly, and your time series breaks at every refit.

**Academic benchmarking and leaderboards.** Problematic, since cross-system comparability is
exactly what learned per-system weights destroy. Use nDCG for the leaderboard and UDCG for your
own engineering decisions.

### Recommendation

Adopt UDCG when your generator is stable and you have the annotation budget for a
utility-with-distraction schema. Its value is not that it produces a better number, it is that it
is the only ranking metric that can tell you a passage was actively harmful.

If you cannot afford it, the cheap version of the same discipline is to stop reporting nDCG alone
in RAG. Report it next to a distraction-sensitive measure, such as MIRAGE's Noise Vulnerability or
CUE's Lucky Guess rate, so that the negative contributions are visible somewhere on the page.

### Failure mode

![The Stale Weights](assets/diagrams/fig-115-the-stale-weights.png){.diagram-figure width=96%}

In January a team fits UDCG weights on Llama-3.1-8B at k=5. In March they swap to Llama-4 and keep
the same dashboard. By June they report that UDCG has been flat for two quarters and conclude
retrieval quality is stable.

They are scoring a new generator using the old one's attention profile, so the number is measuring
a model they no longer run.

---
