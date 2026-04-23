<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 5 — Implications

> **What this phase does:** Look at the Phase 4 leaderboard and make the human call — which approach do you stake your name on, with every rejected alternative given a reason, and every segment (or model family) profiled in plain business language.
> **Why it exists:** "Claude Code recommended it" with no paragraph underneath is not a decision; this phase forces you to own the pick and defend the rejections.
> **You're here because:** The Phase 4 leaderboard is complete (`phase-04-candidates.md`). This phase is opened TWICE — Sprint 1 USML and Sprint 2 SML.
> **Key concepts you'll see:** segment naming, interpretability-vs-accuracy tradeoff, "collapse to one segment", distinct-action test

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm entering Playbook Phase 5 — Implications. My decision here is the
pick — which candidate I stake my name on, named in one paragraph of
business language, with every rejected alternative given a reason.

Read the Phase 4 leaderboard I just produced. Then:

1. For each candidate (including the baseline), state in the same
   columns: separation or accuracy, stability, training complexity,
   interpretability. One row per candidate.

2. For the top 2 candidates, profile EACH output class or cluster in
   one paragraph of plain business language — no column names, no
   numbers. "Customers who shop weekly on weekends and ignore promos"
   is a profile; "segment with high weekend_browse_fraction and
   low_promo_resp" is a statistical artefact.

3. Recommend ONE candidate. Weight stability heavily for unsupervised
   models — a "best" model that reshuffles monthly is unusable. Weight
   interpretability over raw accuracy within 1 point for supervised
   models — a model that cannot be explained to the decision-maker
   will not get shipped.

4. For every alternative you reject, give a one-sentence reason. A
   rejected alternative with no reason is "Claude Code said so",
   which does not ship.

Do NOT propose floors, thresholds, or K values. The pick is mine;
the floors go in Phase 6 and are pre-registered BEFORE we revisit
the leaderboard there.

When the recommendation and one-paragraph profiles are in the journal,
stop and wait for my pick.
```

**Tonight-specific additions** (Week 5 Arcadia Retail):

```
If Sprint 1 USML (clustering):
  - Journal file: journal/skeletons/phase_5_implications.md →
    journal/phase_5_implications.md.
  - Stability-over-separation weighting is explicit: 0.62 silhouette
    with 88% Jaccard stability beats 0.71 silhouette with 62%
    stability. Write both numbers so the trade-off is visible.
  - Segment profiles must use Arcadia-level language: purchasing
    patterns, channel preferences, promo responsiveness — no column
    names or numeric feature values.
  - Distinct-action test: for the top candidate, write a one-sentence
    marketing action per segment. If two segments get the same
    one-sentence action, they should probably be collapsed.
  - Stakeholder reference: "CMO" owns the campaign-count ceiling;
    "CX Lead" approves segment names.

If Sprint 2 SML (classifier):
  - Journal file: journal/phase_5_sml.md.
  - Interpretability-over-AUC within 1 point: if logistic regression
    is within 1 AUC point of GBM, prefer LR because the CX Lead can
    explain it to the retention team.
  - Model profiles: for each family, one paragraph describing which
    behaviours it predicts well and which it misses — no metric names,
    no feature names.
```

**How to paste:** Combine both blocks into a single paste.

---

## 2. Signals the output is on track

**Signals of success (USML — Sprint 1):**

- ✓ Every candidate on the leaderboard compared in the same columns
- ✓ Plain-language segment profile per cluster for the top 2 candidates (no column names, no numbers)
- ✓ Stability weighting explicit — "0.62 silhouette / 88% Jaccard" shape of reasoning visible
- ✓ Distinct-action test: one-sentence marketing action per segment in the top candidate
- ✓ Rejection reason for every non-recommended candidate
- ✓ No floors or K proposed
- ✓ Viewer (http://localhost:3000) shows segment profile cards populated with plain-language descriptions for the top candidate's clusters

**Signals of success (SML — Sprint 2):**

- ✓ Plain-language model-family profile for each of the 3 families
- ✓ Interpretability-vs-AUC trade-off named explicitly (within-1-point decision visible)
- ✓ Rejection reasons written for non-recommended families
- ✓ No threshold named
- ✓ Viewer (http://localhost:3000) shows the picked classifier highlighted in the leaderboard panel

**Signals of drift — push back if you see:**

- ✗ Cluster profile includes column names or numbers ("please rewrite in plain language; no column names, no numbers — would a CMO recognize this segment on the street?")
- ✗ Recommendation based only on top-of-leaderboard metric without checking stability or interpretability ("did you weigh stability (USML) or interpretability (SML)? top-of-leaderboard isn't automatic")
- ✗ Rejected alternative with no reason ("why was this rejected? one sentence please")
- ✗ A proposed floor or threshold ("please remove; Phase 6 pre-registration is corrupted if I see a floor here")
- ✗ Viewer shows nothing new after CC reports the phase complete — CC may have described the work, not run it. Re-prompt: "show me the rendered segment profile cards"

---

## 3. Things you might not understand in this phase

_(v1 — if a concept you struggled with isn't here, flag it back to the author)_

- **Segment naming** — giving a cluster a human-readable label based on its behavioural character, not its numeric feature values
- **Interpretability-vs-accuracy tradeoff** — the tension between a model that is easy to explain and one that scores best on a metric, and how to decide which matters more in context
- **"Collapse to one segment"** — when two segments are so similar in their actionable meaning that treating them separately adds cost without adding value
- **Distinct-action test** — the test of whether each segment genuinely warrants a different business action, which is the real criterion for keeping a segment distinct

---

## 4. Quick reference (30 sec, generic)

### Segment naming

Giving a cluster a name that a non-technical stakeholder can act on. "Cluster 3" is a label; "Weekend Browsers Who Ignore Promos" is a name. The name should describe a behaviour pattern that marketing can build a campaign around without looking at any data. If you cannot name a segment in 10 words without using a feature name or a number, the segment is probably a statistical artefact rather than a real customer group.

> **Deeper treatment:** [appendix/03-modeling/unsupervised-families.md](./appendix/03-modeling/unsupervised-families.md)

### Interpretability-vs-accuracy tradeoff

A more complex model (GBM, neural net) often scores a few percentage points higher than a simpler one (logistic regression). But the simpler model can be explained to a non-technical decision-maker: "this customer scores high because they last purchased 4 months ago and visited 3 times this quarter." The question is whether the accuracy gain is worth the loss of explainability. A rule of thumb: if the two models are within 1 AUC point, prefer the simpler model. The decision-maker will not ship what they cannot explain to their boss.

> **Deeper treatment:** [appendix/03-modeling/supervised-families.md](./appendix/03-modeling/supervised-families.md)

### "Collapse to one segment"

When two segments are so similar in actionable terms that treating them as two distinct segments adds operational cost without adding campaign value. The test is the distinct-action test: write a one-sentence marketing action for each segment. If two segments get the same sentence, they should be collapsed into one. This is the most common reason to pick a lower K than the silhouette curve recommends — statistical separation is not the same as business separation.

> **Deeper treatment:** [appendix/01-framing/horizon-and-ceiling.md](./appendix/01-framing/horizon-and-ceiling.md)

### Distinct-action test

For every cluster or output class: write one sentence naming what the business does differently for this group versus the others. If the sentence is identical to another segment's sentence, the two segments are operationally one — collapse them. This test is not about marketing creativity; it is about whether the model produces outputs the business can act on distinctly. A model with 7 segments and only 3 distinct actions is a 3-segment model with overhead.

> **Deeper treatment:** [appendix/01-framing/horizon-and-ceiling.md](./appendix/01-framing/horizon-and-ceiling.md)

---

## 5. Ask CC, grounded in our project (2 min)

Paste this if §4 isn't enough. CC will read our codebase and journal and tailor the explanation to Arcadia Retail.

```
You are helping me understand a concept from Metis Week 5, where I am
building an ML system for Arcadia Retail. I'm currently in Playbook
Phase 5 — Implications.

Read `workspaces/metis/week-05-retail/playbook/phase-05-implications.md`
for what this phase does, and read `workspaces/metis/week-05-retail/journal/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. distinct-action test >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current Arcadia state
3. Implications for the decision I'm about to make (or just made) in Phase 5
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

Before moving on:

- [ ] Every leaderboard candidate compared in the same columns
- [ ] Plain-language profile for every cluster or model family in the top candidate
- [ ] Distinct-action test run: one-sentence action per cluster (USML)
- [ ] Rejection reason written for every non-recommended candidate
- [ ] No floors, thresholds, or K values proposed

**Next file:** [`phase-06-metric-threshold.md`](./phase-06-metric-threshold.md)

This file is opened twice — once for Sprint 1 USML and once for Sprint 2 SML. When you return here for Sprint 2, re-read the tonight-specific additions for the SML branch.
