# Chapter 10 - Online and Counterfactual Evaluation

## 10.0 The data you already have

Everything so far required judgments, meaning somebody sitting down and deciding what was
relevant. This chapter asks whether your users have already answered that question through
their behaviour, since they click on some results and ignore others every day.

The appeal is obvious, and Radlinski, Kurup and Joachims state it precisely: usage data can be
collected at essentially zero cost, it is available in real time, and it reflects the values of
the users themselves in the context of their actual information need.

They then demonstrate that the obvious way to use it does not work.

## 10.1 CAUTION The negative result that should reshape your dashboard

**Source:** Radlinski, Kurup & Joachims, *How Does Clickthrough Data Reflect Retrieval Quality?*,
**CIKM 2008, pp. 43-52, Napa Valley** VERIFIED

Running an operational search engine over the arXiv.org e-print archive under a controlled
experimental design, they tested eight absolute usage metrics. The finding was blunt:

> **None of the eight absolute usage metrics** explored, including the number of clicks, the
> frequency of query reformulations, and abandonment, **reliably reflect retrieval quality** for
> the sample sizes considered.

What did work was comparison. Paired experimental designs adapted from sensory analysis produced
accurate and reliable statements about the relative quality of two retrieval functions, and two
separate paired comparison tests analyzing clickthrough from an interleaved presentation of
ranking pairs both gave accurate and consistent results.

![The Result In One Picture](assets/diagrams/fig-076-the-result-in-one-picture.png){.diagram-figure width=96%}

The figure puts the two kinds of claim side by side. An absolute claim sounds like "clickthrough
rate went from 0.31 to 0.34", and that turns out to be unreliable at realistic sample sizes. A
paired claim sounds like "users preferred B's results 58% of the time", and that turns out to be
accurate and consistent.

So a team announcing that clickthrough improved three points and proposing to ship on that basis
is relying on one of the eight metrics that was tested and found unreliable. What they need is a
paired comparison rather than a shift in a level.

This matters enormously and is widely ignored, because most production teams monitor exactly the
absolute metrics that study found wanting. Clickthrough dashboards, abandonment rates,
reformulation counts, all eight categories are in daily use, and the published evidence says
those numbers do not tell you what you think they do at the sample sizes you have.

The explanation the authors offer is that interleaving gives searchers an easier task. Expressing
a relative preference between two rankers is something a click can genuinely convey, and
expressing an absolute quality level is not.

---

## 10.2 Interleaving

**One-line:** Blend two rankers' results into one list, show it to every user, and attribute each
click to the ranker that contributed the clicked item.

**Facets:** Correctness | session | human | R | ESTABLISHED VERIFIED
**Source:** Radlinski, Kurup & Joachims, CIKM 2008, pp. 43-52 VERIFIED

### The problem it solves

If absolute click metrics cannot tell you whether a ranker is good, you still need some way to
decide whether a new ranker is better than the one you are running. Standard A/B testing splits
users into two groups and compares them, which means the difference you are looking for has to
be large enough to show through all the natural variation between two populations of people.

### The idea

Rather than splitting the users, you split each result list. Take the rankings produced by both
rankers, blend them into a single list according to a fixed procedure, and show that one list to
everybody. Because you recorded which ranker contributed each item, a click on any item is a
point for whichever ranker put it there.

![Team-Draft Interleaving](assets/diagrams/fig-077-team-draft-interleaving.png){.diagram-figure width=96%}

The figure walks the team-draft variant, so named because the two rankers take turns picking
like captains choosing a team. Ranker A wants doc-P, doc-Q, doc-S, doc-T and ranker B wants
doc-Q, doc-R, doc-P, doc-U. The interleaved list comes out as doc-P credited to A, doc-Q
credited to B, doc-R credited to B, doc-S credited to A, doc-U credited to B and doc-T credited
to A. A user who clicks doc-R has given a point to B, and a user who clicks doc-S has given a
point to A. Aggregate that over thousands of sessions and you have a preference.

The figure also explains why this beats A/B testing. Under A/B, half your users see A and half
see B, so you are comparing two populations and the variation between people swamps the signal
you care about. Under interleaving, every user sees both, so the comparison happens within each
person, the variance largely disappears, and you reach significance on far less traffic.

### Advantages

- **Dramatically more sensitive than A/B testing,** because the within-subject comparison
  eliminates population variance.
- **Reflects real users** in their real context rather than annotators imagining that context.
- **Zero annotation cost.**
- **Validated at scale,** in Chapelle, Joachims, Radlinski & Yue, *Large-Scale Validation and
  Analysis of Interleaved Search Evaluation* VERIFIED, and Hofmann, Whiteson & de Rijke,
  *Fidelity, Soundness, and Efficiency of Interleaved Comparison Methods*, **ACM TOIS
  31(4):1-43, 2013** VERIFIED.
- **Extends past two systems,** through Schuth, Sietsma, Whiteson, Lefortier & de Rijke,
  *Multileaved Comparisons for Fast Online Evaluation*, **CIKM 2014** VERIFIED.

### Disadvantages

- **Relative only.** Interleaving tells you that B beats A and never that either of them is any
  good, so you cannot build a quality dashboard out of it.
- **Requires live traffic,** which makes it unavailable before launch, for low-traffic systems,
  and in regulated environments where experimenting on users is not permitted.
- **Inherits click biases.** Position bias, presentation bias and trust bias all survive the
  switch to a paired design.
- **Implementation subtleties matter.** A naive blending procedure can be biased, and team-draft
  and optimized variants exist precisely because the obvious approach has flaws. See Radlinski &
  Craswell, *Optimized Interleaving for Online Retrieval Evaluation*, **WSDM 2013** VERIFIED.
- **Not applicable to RAG generation.** You can interleave retrieved documents, and you cannot
  meaningfully interleave two generated answers, because the user reads one piece of text.

### Domain examples

**High-traffic consumer search.** Interleaving's home. If you have the traffic, it is the most
sensitive comparison instrument available anywhere in this book.

**RAG retriever comparison.** CAUTION Partially applicable and underexplored. If your interface
shows the retrieved sources, you can interleave those and read a preference from which sources
get clicked. If retrieval is invisible to the user, the method is simply unavailable, and the
gap in RAG evaluation remains open.

**Enterprise search.** Often starved of traffic. A tool serving 200 queries a day will not reach
significance in any useful timeframe.

### Recommendation

If you have the traffic, interleave for every ranker comparison and stop using absolute click
metrics for that purpose. The 2008 result is unambiguous, since the absolute metrics were
unreliable and the paired comparisons were reliable.

Keep absolute metrics for monitoring, which is the job of noticing that something broke, and use
interleaving for deciding, which is the job of choosing between two options. Those are different
jobs and one number cannot do both.

---

## 10.3 Counterfactual evaluation and IPS

**One-line:** Reweight logged interactions by the inverse of their observation propensity, so you
can estimate how a *new* ranker would have performed using *old* logs.

**Formula (sketch):**

![For a logged click on document d at position k](assets/diagrams/fig-078-for-a-logged-click-on-document-d-at-position-k.png){.diagram-figure width=96%}

**Facets:** Correctness | system | human | R | ESTABLISHED VERIFIED
**Source:** Joachims, Swaminathan & Schnabel, *Unbiased Learning-to-Rank with Biased Feedback*,
**WSDM 2017, pp. 781-789**

### The problem it solves

Interleaving requires you to deploy the candidate ranker to real users, which is fine for the
one or two candidates you are serious about and impossible for the twenty you would like to
screen. What you want is a way to ask how a new ranker would have done using logs that your
current ranker produced, without showing anything to anybody.

### The idea

The obstacle is position bias. A document that sat at rank 20 received very few clicks, and you
cannot tell from the raw count whether it was bad or simply never seen. Inverse propensity
scoring separates those two by dividing the observed clicks by the probability that the document
was examined at all, which is what the formula panel describes: the weight for a click on a
document at position k is 1 divided by the probability of examination at position k. Documents
shown at low-attention positions get weighted up, correcting for the fact that they were rarely
looked at, and the result is an unbiased estimate of the underlying relevance.

![The Propensity Correction](assets/diagrams/fig-079-the-propensity-correction.png){.diagram-figure width=96%}

The figure works four ranks. Rank 1 received 500 clicks with an examination probability of 0.90,
correcting to 556. Rank 2 received 200 clicks at probability 0.60, correcting to 333. Rank 10
received 20 clicks at probability 0.10, correcting to 200. Rank 20 received just 5 clicks at
probability 0.03, correcting to 167.

Reading the raw log, rank 20 looks terrible with its five clicks. Adjusted for the fact that it
was examined only three percent of the time, it performed comparably to rank 10. The log was
measuring exposure rather than quality, and the correction is what separates the two.

### Advantages

- **No deployment risk,** since you evaluate a candidate ranker without any user ever seeing it.
- **Reuses existing logs,** which is of enormous practical value when logs are the one asset you
  already have.
- **Statistically principled,** with unbiasedness guarantees that hold under stated assumptions.
- **Position-bias estimation is itself now tractable,** through Agarwal, Zaitsev, Wang, Li,
  Najork & Joachims, *Estimating Position Bias Without Intrusive Interventions*, **WSDM 2019**
  VERIFIED, which removes the need for randomization experiments that degrade the user
  experience while you run them.

### Disadvantages

- **Requires propensity estimates,** and any error in those propagates straight into the result.
- **High variance when propensities are small.** Dividing by 0.03 amplifies the noise just as
  effectively as it amplifies the signal.
- **Assumes the logging policy had support** over the actions you want to evaluate, meaning a
  document your old ranker never showed generates no data at all, and no amount of reweighting
  can create it.
- **Complex to implement correctly,** and easy to implement in a way that is subtly wrong while
  still producing plausible numbers.

### Domain examples

**Large-scale search and recommendation.** The intended setting, and where it delivers most.

**RAG reranker selection.** A genuinely promising and underused application. If you log which
chunks were retrieved and whether the resulting answer was correct, IPS-style reweighting lets
you estimate how a new reranker would have done offline. Note that the support problem is
particularly severe here, because your log only contains chunks your current retriever surfaced
in the first place.

**Anything low-traffic.** Variance will dominate the estimate. Do not bother.

### Recommendation

Use counterfactual evaluation to shortlist candidates offline, then interleave the top two or
three online. Neither instrument replaces the other, since IPS is cheap and becomes biased when
the model behind it is misspecified, while interleaving is expensive and trustworthy.

CAUTION The support assumption is the failure mode to watch. If you are evaluating a retriever
that surfaces documents your current one never did, your logs are silent on exactly the cases
that matter, and IPS will confidently report on the subset it can see while saying nothing about
the rest.

---

## 10.4 Session and satisfaction measures

A brief treatment, since these are considerably less standardized than everything above.

| Metric | What it captures | Note |
|---|---|---|
| **sDCG** | DCG extended over a multi-query session | Järvelin et al., ECIR 2008 OPEN *not verified this pass* |
| **Abandonment rate** | Sessions with no click | CAUTION Among the eight metrics found unreliable in 2008 |
| **Reformulation rate** | User rewrote the query | CAUTION Also among the eight |
| **Task completion time** | Time to satisfy the need | Manning Ch. 8 VERIFIED |
| **Time-biased gain** | Gain discounted by time spent | Smucker & Clarke, SIGIR 2012 OPEN *not verified this pass* |

Two of these carry the 2008 warning explicitly. Abandonment and reformulation are diagnostic
signals, useful for noticing that something has broken, and they are not quality measures, so do
not build a comparison on them.

Two entries carry OPEN status, meaning the underlying method was not available in enough detail to
characterize it here.

## 10.4.1 The implicit-feedback foundation

Worth citing whenever somebody proposes reading quality directly off clicks: Joachims, Granka,
Pan, Hembrooke, Radlinski & Gay, *Evaluating the Accuracy of Implicit Feedback from Clicks and
Query Reformulations in Web Search*, **ACM TOIS 25(2), Article 7, 2007** VERIFIED. This is the
eye-tracking-backed study that established what clicks do and do not tell you, and it both
predates and underpins the 2008 negative result.

---

## 10.5 Chapter 10 summary

![Decision map](assets/diagrams/fig-080-decision-map.png){.diagram-figure width=96%}

The hierarchy comes down to whether you are deciding or monitoring. For deciding between
rankers, use interleaving if you have high traffic, since it is the most sensitive instrument
available; use IPS or counterfactual estimation to shortlist when you cannot deploy; and fall
back to offline metrics when traffic is low, because an online test will never reach
significance. For monitoring, absolute click metrics are genuinely useful, and they remain
unsuitable for deciding whether one system is better than another.

The 2008 result restated: eight absolute usage metrics, including clicks, reformulations and
abandonment, did not reliably reflect retrieval quality at realistic sample sizes, and paired
interleaved comparisons did. Most production dashboards are built on the first group.

There is also a gap specific to RAG. You can interleave retrieved sources, and you cannot
interleave generated answers, because the user reads one text and has no second version to
prefer. No published method resolves online RAG evaluation, and anyone claiming otherwise is
extrapolating past the evidence.

---
