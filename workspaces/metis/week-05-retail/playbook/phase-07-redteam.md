<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 7 — Red-Team

> **What this phase does:** Actively try to break this sprint's model before deployment does it for you — running stability, proxy, operational-stress, and calibration sweeps against the Phase 6 pre-registered floors, then ranking findings by dollar severity.
> **Why it exists:** The model passes your Phase 4 leaderboard metrics. This phase asks whether it also holds up under conditions it wasn't trained on, and whether it is silently doing something you didn't intend.
> **You're here because:** Floors are pre-registered in Phase 6 (`phase-06-metric-threshold.md`). This phase is opened TWICE — Sprint 1 USML and Sprint 2 SML.
> **Key concepts you'll see:** re-seeding stability, proxy leakage sweep, operational collapse, adversarial subgroup

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm entering Playbook Phase 7 — Red-Team. My decision here is the
disposition per finding — ACCEPT (accepted risk), MITIGATE (action
before ship), or RE-DO (a phase must re-run). Your job is to run the
sweeps and report numbers AGAINST my Phase 6 pre-registered floors,
not propose new ones.

Copy the Phase 7 skeleton from journal/skeletons/phase_7_red_team.md
into the project journal.

For every claim — algorithm name, metric, endpoint, column — cite the
file and function. If you cannot cite, say so explicitly and mark the
finding uncertain.

For every dollar figure, quote the cost source verbatim. Do NOT invent.

CRITICAL: Do NOT propose new thresholds or floors. The floors were
pre-registered in Phase 6. If a metric comes back below my pre-registered
floor, the finding is "below my pre-registered floor — Phase 8 gate
failure candidate", not "let me propose a new floor."

Rank findings by severity in dollars. Tag each finding:
  ACCEPT — accepted risk with rationale
  MITIGATE — action required before ship (name the action)
  RE-DO — a named prior phase must re-run

My call on final dispositions; write your recommendation first.

Do NOT use "blocker" without naming the specific ship-action blocked.
"Model is unstable" is not a blocker; "cannot ship the allocator
because its input reshuffles every week" is.

When all sweeps are in the journal with cited numbers, sourced dollar
severity, and disposition recommendations, stop and wait for my call
per finding.
```

**Tonight-specific additions** (Week 5 Arcadia Retail):

```
If Sprint 1 USML (clustering):
  - Journal file: journal/skeletons/phase_7_red_team.md →
    journal/phase_7_red_team.md.

  Sweep 1 — RE-SEED CHURN: Run /segment/fit 3 times with different
    random seeds, hold features and K constant. Report the per-segment
    Jaccard stability DISTRIBUTION — not the mean, the distribution.
    Cite: src/retail/backend/routes/segment.py + fit function in
    ml_context.py.

  Sweep 2 — PROXY LEAKAGE: Drop postal_district, then drop age_band,
    then drop both. Re-cluster each time. Report the fraction of
    customers who changed segment vs the Phase 5 winning clustering.
    Cite source columns in src/retail/data/arcadia_customers.csv.

  Sweep 3 — OPERATIONAL COLLAPSE: Filter transactions to
    post-Black-Friday shapes (volume spike + mix shift, using
    src/retail/data/scenarios/catalog_drift.json if available).
    Re-cluster. Report the size of the smallest segment as a fraction
    of customers.

  Dollar severity ranking: use $45 wrong-segment, $14 wasted
    impression, $220 under-18 PDPA, $8 cold-start — all from
    PRODUCT_BRIEF.md §2. Quote the row, don't paraphrase.

If Sprint 2 SML (classifier):
  - Journal file: journal/phase_7_sml.md.

  Sweep A — CALIBRATION-PER-SUBGROUP: Compute Brier score per
    customer segment for both churn and conversion classifiers. Cite
    the endpoint that returns calibration (per routes/predict.py).
    Report the subgroup with the worst calibration.

  Sweep B — FEATURE-ABLATION: Drop the top-importance feature for
    each classifier, re-train, report the AUC drop. If the drop is
    >3 points, that feature was doing disproportionate work.

  Dollar severity: $120 CAC (missed churn), $3 touch (false alarm),
    $220 PDPA (proxy leakage if demographic feature found). Quote the
    §2 line for each.

Fairness: mark "Fairness dimension — deferred to Week 7 per Playbook"
  explicitly in the journal. Do NOT skip silently.
```

**How to paste:** Combine both blocks into a single paste.

---

## 2. Signals the output is on track

**Signals of success (USML — Sprint 1):**

- ✓ Three sweeps complete: re-seed Jaccard distribution, proxy-drop reassignment percentages, operational collapse segment sizes
- ✓ Jaccard reported as a DISTRIBUTION across seeds (not just mean)
- ✓ Proxy-drop results for `postal_district`, `age_band`, and both combined — each with a reassignment percentage
- ✓ Findings measured against Phase 6 pre-registered floors — no new floor proposed
- ✓ Dollar severity quoted from `PRODUCT_BRIEF.md §2` for each finding
- ✓ Fairness row explicitly marked "deferred to Week 7 per Playbook"
- ✓ Viewer (http://localhost:3000) shows red-team findings panel with stability / proxy / operational-collapse rows and ACCEPT/MITIGATE/RE-DO tags

**Signals of success (SML — Sprint 2):**

- ✓ Calibration-per-subgroup Brier score for both churn and conversion classifiers, worst subgroup named
- ✓ Feature-ablation AUC drop reported for each classifier's top feature
- ✓ Findings measured against Phase 6 pre-registered Brier floor — no new floor proposed
- ✓ Dollar severity quoted for each finding
- ✓ Fairness row explicitly marked "deferred to Week 7 per Playbook"
- ✓ Viewer (http://localhost:3000) shows calibration-per-subgroup panel and feature-ablation chart

**Signals of drift — push back if you see:**

- ✗ A new threshold proposed ("I suggest lowering the stability floor to 0.70") — "my Phase 6 floor was X; this is a failure against that floor, not a floor adjustment"
- ✗ A finding without a file-and-function citation ("which file and function produced this?")
- ✗ A dollar severity without a §2 quote ("please quote the §2 row for this cost")
- ✗ Mean Jaccard only, without the distribution ("please report the distribution across seeds, not the mean")
- ✗ Fairness row absent or silent ("please add the fairness row explicitly, marked 'deferred to Week 7 per Playbook'")
- ✗ "Blocker: the model is unstable" without a named ship-action blocked
- ✗ Viewer shows nothing new after CC reports the phase complete — re-prompt: "show me the red-team findings panel in the viewer"

---

## 3. Things you might not understand in this phase

_(v1 — if a concept you struggled with isn't here, flag it back to the author)_

- **Re-seeding stability** — the test for whether the random seed, rather than the data, is driving the model's output
- **Proxy leakage sweep** — the systematic test for whether a behavioural output is secretly being driven by a demographic feature that was supposed to be excluded
- **Operational collapse** — when a segment or population drops below the minimum size at which a campaign or action is economically viable
- **Adversarial subgroup** — the specific customer group on which the model performs worst, which is usually also the group with the most to lose from being mis-served

---

## 4. Quick reference (30 sec, generic)

### Re-seeding stability

K-means and similar algorithms use a random starting point (seed) before converging. Different seeds can produce different final clusters, especially when the data doesn't have strong natural structure. The re-seeding test runs the same algorithm with 3+ different seeds, holding features and K constant, and measures the Jaccard overlap between each pair of results. If 20%+ of customers move between seeds, the segmentation is a function of the seed — not a discovery. Report the distribution of Jaccard scores, not just the mean: a mean of 0.75 with two seeds at 0.5 is very different from a mean of 0.75 with all seeds above 0.70.

> **Deeper treatment:** [appendix/03-modeling/stability-protocols.md](./appendix/03-modeling/stability-protocols.md)

### Proxy leakage sweep

Running the model with a suspected demographic feature dropped, then measuring how many records change their output. If removing `postal_district` causes 30%+ of customers to change segment, the "behavioural" segmentation was actually a demographic segmentation in disguise. The proxy-drop test is run at Phase 3 (feature framing) and re-run here at Phase 7 with the FINAL model — because the feature selection you approved in Phase 3 may have left indirect proxies that emerge only after the full model is fit. Any segment that collapses on a demographic drop must be flagged.

> **Deeper treatment:** [appendix/02-data/proxy-for-protected-class.md](./appendix/02-data/proxy-for-protected-class.md)

### Operational collapse

When a segment or class shrinks below the minimum population at which a targeted action is economical. For Arcadia: a segment below 2% of 18,000 customers is 360 people — too small for a dedicated email campaign. If a post-Black-Friday re-cluster puts any segment below that floor, the campaign built around it loses its economic basis. Operational collapse is also the Phase 13 drift signal — the threshold you set here must match the retrain trigger you set in Phase 13.

> **Deeper treatment:** [appendix/06-monitoring/segment-membership-churn.md](./appendix/06-monitoring/segment-membership-churn.md)

### Adversarial subgroup

The customer segment on which the model performs worst. In supervised learning: the subgroup with the highest Brier score, highest false-negative rate, or lowest calibration. In unsupervised learning: the segment with the lowest stability (reshuffles most across seeds) or the smallest size (most likely to collapse). The adversarial subgroup is usually also the group most likely to contain vulnerable populations — new-to-market customers, low-frequency buyers, recently acquired users. Name it explicitly; do not let it disappear into an average.

> **Deeper treatment:** [appendix/04-evaluation/calibration-and-brier.md](./appendix/04-evaluation/calibration-and-brier.md)

---

## 5. Ask CC, grounded in our project (2 min)

Paste this if §4 isn't enough. CC will read our codebase and journal and tailor the explanation to Arcadia Retail.

```
You are helping me understand a concept from Metis Week 5, where I am
building an ML system for Arcadia Retail. I'm currently in Playbook
Phase 7 — Red-Team.

Read `workspaces/metis/week-05-retail/playbook/phase-07-redteam.md`
for what this phase does, and read `workspaces/metis/week-05-retail/journal/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. proxy leakage sweep >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current Arcadia state
3. Implications for the decision I'm about to make (or just made) in Phase 7
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

Before moving on:

- [ ] All sweeps complete with cited numbers (USML: 3 sweeps; SML: 2 sweeps)
- [ ] Jaccard distribution reported (not just mean) for re-seeding sweep
- [ ] Every finding measured against Phase 6 pre-registered floor — no new floor proposed
- [ ] Dollar severity present and sourced from `PRODUCT_BRIEF.md §2`
- [ ] ACCEPT / MITIGATE / RE-DO tag per finding, pending your disposition call
- [ ] Fairness row explicitly marked "deferred to Week 7 per Playbook"

**Next file:** [`phase-08-gate.md`](./phase-08-gate.md)

This file is opened twice — once for Sprint 1 USML (Phase 8 decides whether to promote the segmentation) and once for Sprint 2 SML (Phase 8 decides whether to promote the classifiers). When you return here for Sprint 2, re-read the tonight-specific additions for the SML branch.
