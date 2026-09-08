# Chapter 11 - Significance, Reporting, and the Progress Problem

## 11.0 The uncomfortable opening

It is worth starting with the conclusion here, because it reframes everything else in the
chapter.

**Source:** Armstrong, Moffat, Webber & Zobel, *Improvements That Don't Add Up: Ad-hoc Retrieval
Results Since 1998*, **CIKM 2009, pp. 601-610** VERIFIED

The authors went through a decade of published ad-hoc retrieval results and found that the
reported improvements did not accumulate. Individual papers routinely demonstrated statistically
significant gains over a baseline, and the absolute effectiveness of the field stayed flat.

![The Problem In One Picture](assets/diagrams/fig-081-the-problem-in-one-picture.png){.diagram-figure width=96%}

The figure draws the two stories side by side. What the papers implied, taken together, was a
line climbing steadily from 1998 to 2008. What actually happened was a flat line over the same
period. Each individual paper reported something like a 4% gain over its baseline at p < 0.05,
and ten years of those produced no cumulative gain at all.

Asked how that is possible when every result was significant, the answer is a combination of
weak baselines, selective reporting, multiple comparisons and results measured on different
collections. Every one of those is defensible within a single paper, and none of them adds up
across papers.

This result belongs in a book about metrics rather than in a book about statistics, because it
is the strongest available evidence that a good metric set is not sufficient on its own. The
field had nDCG, it had MAP, and it had significance testing, and its experiments still failed to
establish that anything was getting better.

If you take one thing from this chapter, take this: your comparison practice determines what
your metrics are capable of establishing.

---

## 11.1 Significance testing - which test?

**Source:** Smucker, Allan & Carterette, *A Comparison of Statistical Significance Tests for
Information Retrieval Evaluation*, **CIKM 2007, pp. 623-632** VERIFIED

### The problem it solves

You ran two systems over the same queries and one scored higher. Before you can claim it is
better, you have to rule out the possibility that the difference is an accident of which queries
happened to be in your set. That is what a significance test does, and the choice of test
matters more here than in many fields, because retrieval scores are not normally distributed,
queries vary enormously in difficulty, and sample sizes are small.

### The options

![The Test Menu](assets/diagrams/fig-082-the-test-menu.png){.diagram-figure width=96%}

The figure lists five and characterizes each. The paired t-test assumes the differences are
normally distributed and turns out to be surprisingly robust in practice even when they are not.
The randomization test, also called a permutation test, makes no distributional assumption at
all and is the recommended default. The bootstrap resamples the data and gives you confidence
intervals. The Wilcoxon signed-rank test works on ranks and therefore discards information about
magnitude. The sign test is the weakest of the five, since it uses only the direction of each
difference.

The recommendation is the paired randomization test, because it assumes the least, it is cheap
on modern hardware, and it tests directly the thing you actually want to know, which is whether
this difference could have arisen from chance assignment.

### The paired randomization test, mechanically

![How It Works](assets/diagrams/fig-083-how-it-works.png){.diagram-figure width=96%}

The procedure is simple enough to describe completely. For each query you have two scores, one
from system A and one from system B, and your observed difference D is the mean of A minus the
mean of B. Now, for each query independently, flip a coin and either swap that query's two
scores or leave them alone, then recompute the mean difference. Do that ten thousand times and
you have a distribution of differences that could have arisen if the labels A and B meant
nothing.

Your p-value is the fraction of those shuffled differences that are at least as large as the one
you observed. The logic underneath is worth stating plainly: if your observed difference is
unremarkable among random reshuffles of the same numbers, it is not evidence of anything.

### Recommendation

Use a paired randomization test as your default, and report the p-value, the effect size and a
confidence interval together. Never report a p-value on its own, because "significant" without a
magnitude tells the reader nothing about whether the difference is large enough to care about.

---

## 11.2 Statistical power and topic set size

Three verified works make overlapping points from different angles.

| Work | Citation | Finding |
|---|---|---|
| Voorhees & Buckley | *The Effect of Topic Set Size on Retrieval Experiment Error*, **SIGIR 2002, pp. 316-323** VERIFIED | Error rates depend strongly on the number of topics |
| Webber, Moffat & Zobel | *Statistical Power in Retrieval Experimentation*, **CIKM 2008, pp. 571-580** VERIFIED | Most IR experiments are underpowered |
| Sanderson & Zobel | *Information Retrieval System Evaluation: Effort, Sensitivity, and Reliability*, **SIGIR 2005, pp. 162-169** VERIFIED | Trades off judgment effort against reliability |

Statistical power is the probability that your experiment would detect a real difference of a
given size if one existed. Low power is usually described as a risk of missing real effects, and
it carries a second consequence that is less widely understood.

![The Power Problem](assets/diagrams/fig-084-the-power-problem.png){.diagram-figure width=96%}

The figure runs the scenario. Fifty queries, nDCG of 0.712 against 0.698, p = 0.04, and a team
announcing a significant improvement. The question that should follow is what their power was to
detect a real difference of that size, and if the answer is 0.35, then most genuine improvements
in that setup would come back non-significant while some non-improvements come back significant.

The second consequence is the one to remember. Underpowered studies do not merely miss real
effects, they also inflate the effects they do detect, because only a large observed difference
can clear the significance bar, which includes differences that are large purely by chance.

### Recommendation

Work out how many queries you need before you run the experiment rather than afterwards. If you
cannot get that many, say so plainly and report confidence intervals wide enough to be honest
about it.

For RAG specifically, evaluation sets of 50 to 100 questions are common and are almost always
underpowered for the effect sizes people claim from them. If you are comparing two rerankers
that differ by two points of accuracy, a hundred questions will not settle the question and no
amount of careful testing will make them settle it.

---

## 11.3 Multiple comparisons and the weak-baseline problem

These are the two mechanisms that Armstrong et al.'s finding rests on.

### 11.3.1 Multiple comparisons

![The Twenty-Configuration Problem](assets/diagrams/fig-085-the-twenty-configuration-problem.png){.diagram-figure width=96%}

Suppose you try twenty chunk sizes and test each one against your baseline at the conventional
threshold of 0.05. That threshold means each individual test has a one in twenty chance of
coming back significant when nothing real is happening, so across twenty tests the expected
number of false positives is exactly one, even if none of the twenty configurations is any
better than the baseline.

So a team announcing that chunk size 384 was significantly better has observed the outcome you
would expect under the assumption that nothing works. The fix is either to correct for the
number of tests or to hold out a confirmation set.

Correct with Bonferroni, which is simple and conservative, or with Holm, or with
Benjamini-Hochberg, which controls the false discovery rate rather than the family-wise error
rate. Better still, choose your configuration on a development set and confirm it exactly once
on a held-out set that you have not touched.

### 11.3.2 Weak baselines

This is the subtler mechanism and it does more damage. A well-tuned BM25 is a strong baseline
and an untuned one is not, so a paper comparing against an untuned baseline reports a gain that
partly or wholly disappears once the baseline is configured properly. Each such paper can be
individually defensible, and the aggregate trend across many of them is still misleading.

![Why Improvements Don'T Add Up](assets/diagrams/fig-086-why-improvements-don-t-add-up.png){.diagram-figure width=96%}

The figure works the arithmetic. Paper 1 beats a weak BM25 by 8%, paper 2 by 6%, paper 3 by 7%,
so a reader combining them expects something in the region of 21% over BM25. In reality all
three sit roughly level with a properly tuned BM25, and the entire apparent gain was a
description of how badly the baseline had been configured.

The RAG-era relevance is direct and current, because dense retrieval papers routinely compare
against BM25 with its default k1 and b values. Note also the finding from *The Power of Noise*
(Cuconasu et al., SIGIR'24), where BM25 outperformed dense retrieval methods in terms of
perplexity on the fundamental text-completion task, and a broad set of sparse methods beat every
dense method tested across varying query lengths. Sparse baselines are stronger than the field's
habits assume.

### 11.3.3 Score standardization

For comparison across collections there is a published remedy: Webber, Moffat & Zobel, *Score
Standardization for Inter-Collection Comparison of Retrieval Systems*, **SIGIR 2008, pp. 51-58**
VERIFIED. If you need to compare results measured on different collections, and RAG
practitioners often do across domains, then raw metric values are not comparable and
standardization is what to do about it.

---

## 11.4 The reporting checklist

Everything in Volume I, condensed into the things that have to appear beside a number for that
number to mean anything to a reader.

![Decision map](assets/diagrams/fig-087-decision-map.png){.diagram-figure width=96%}

About the metric itself, state the metric name and the cutoff k, the gain function if you are
reporting nDCG, the persistence p if you are reporting RBP or RBO, the novelty parameter α if
you are reporting α-nDCG, and where your judgments came from along with how much of the
retrieved material they cover.

About the comparison, state the number of queries, which significance test you used with paired
randomization preferred, the effect size and confidence interval alongside the p-value, any
multiple-comparison correction if you ran more than one test, and the configuration of your
baseline including whether it was tuned.

Then add one honesty line, which is either RBP's residual, or the gap between MAP and bpref, or
any other statement of how much your incomplete judgments could move the number.

For RAG there are five more: the embedder name and version, the generator name and version, the
judge model with a dated snapshot if anything was scored by a language model, the chunk size and
overlap, and the value of k that was actually injected into the prompt rather than the k that
was retrieved.

That last item recurs throughout this book because it is the most common silent error in RAG
evaluation, where metrics get reported at retrieval depth while the generator consumes a
considerably shallower slice.

---
