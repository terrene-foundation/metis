<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

_[← Playbook index (README)](./README.md)_

## Phase 7 — Red-Team

```
──────────────────────────────────────────────────────────────────
 VALUE CHAIN:   Analyze ▸ Todos ▸ **USML ◉** ▸ SML ▸ Opt ▸ MLOps ▸ Close
 THIS PHASE:    Sprint 1 · Phase 7 of 8 — Red-team
 LEVERS:        subgroups · adversarial perturbations · proxy tests · acceptance
──────────────────────────────────────────────────────────────────
```

### Concept

Actively try to break the model before deployment does it for you. AI Verify frame — Transparency, Robustness, Safety — stays across weeks. Week 5 adds three USML-specific failure modes: **re-seed churn** (did the random seed, not the data, produce the segments?), **proxy leakage** (is a segment actually a demographic shadow?), **operational collapse** (does any segment shrink below 2% in one month, breaking the campaign it was built for?).

### Why it matters (SML lens)

- Reinforces Week 4's adversarial-drift dimension — "what does the model do on data it wasn't trained on" is universal.
- Reinforces Week 3's Safety dimension: the $220 PDPA breach and $45 wrong-segment are the concrete dollar handles for "who gets hurt when this silently fails."
- Reinforces Week 2's blast-radius rule — name the population that gets harmed, not "users."
- Reinforces the rule that Transparency failing is a finding, not a pass: if the algorithm doesn't expose feature importance, the limitation goes in the journal.

### Why it matters (USML lens)

- **Re-seed churn** has no SML analogue. If you re-run K-means with a different seed and 20% of customers move, the segmentation is a function of the seed, not a discovery.
- **Proxy leakage in USML is worse than SML.** In SML, the label forces you to notice when a protected attribute is doing the work. In USML, with no label, a demographic proxy masquerades indefinitely. Drop-one-demographic test: if the segment collapses, it was a proxy.
- **Operational collapse** — a small segment shrinks below your ability to run a campaign (e.g., below 2% of customers). This is also the Phase 13 drift signal; Phases 7 and 13 must use consistent thresholds.
- Small segments disproportionately contain vulnerable groups (new-to-market, under-18, low-income).

### Your levers this phase

- **Lever 1 (the big one): proxy-leakage audit.** For every apparent behavioural segment, run the drop-one-demographic test. If the segment dissolves when postcode/age is removed, the segment WAS demographics.
- **Lever 2 (the stability probe): re-seed / re-sample Jaccard.** Multiple seeds, multiple resamples. Report the distribution, not the mean.
- **Lever 3 (the operational stress): worst-subgroup severity.** Where does the model fail WORST — which customer segment, which month, which condition?
- **Lever 4 (the Safety frame): blast radius in dollars.** If this model silently went wrong for a week, what's the dollar damage AND who gets hurt?
- **Skip unless specific:** Fairness dimension (deferred to Week 7 — named in the journal explicitly so the deferral is not silent).

### Trust-plane question

How does this fail? What breaks it?

### Paste this

```
I'm entering Playbook Phase 7 — Red-team. The scaffold pre-committed
to the three red-team sweeps for USML (re-seed churn, proxy
leakage, operational collapse) and — in the SML replay — two for
SML (calibration-per-subgroup, feature-ablation). My decision here
is the disposition per finding (accept / mitigate / re-do); your
job is to run the sweeps and report numbers against my
pre-registered floors, not propose new ones.

Copy journal/skeletons/phase_7_red_team.md into
workspaces/metis/week-05-retail/journal/phase_7_red_team.md (Sprint
1) or journal/phase_7_sml.md (Sprint 2 replay).

USML sweeps (Sprint 1):

1. RE-SEED CHURN. Run /segment/fit 3 times with different random
   seeds, hold features and K constant. Report the per-segment
   Jaccard stability distribution — not the mean, the distribution.
   Cite the endpoint and function (src/retail/backend/routes/
   segment.py + the fit function in ml_context.py).

2. PROXY LEAKAGE. Drop postal_district, then drop age_band, then
   drop both. Re-cluster each time. Report the fraction of
   customers who changed segment vs the Phase 5 winning clustering.
   Cite the source columns in src/retail/data/arcadia_customers.csv.

3. OPERATIONAL COLLAPSE. Filter transactions to post-Black-Friday
   shapes (volume spike + mix shift, using src/retail/data/
   scenarios/catalog_drift.json if helpful). Re-cluster. Report
   the size of the smallest segment as a fraction of customers.

SML sweeps (Sprint 2 replay):

A. CALIBRATION-PER-SUBGROUP. Compute Brier score per customer
   segment for both churn and conversion classifiers. Cite the
   endpoint that returns calibration (per routes/predict.py).
   Report the subgroup with the worst calibration.

B. FEATURE-ABLATION. Drop the top-importance feature for each
   classifier, re-train, report the AUC drop. If the drop is >3
   points, that feature was doing more work than the rest
   combined.

For every claim — algorithm name, metric, endpoint, column — cite
the file and function. If you cannot cite, say so explicitly and
mark the finding uncertain.

For every dollar figure, quote the PRODUCT_BRIEF.md §2 line. The
relevant §2 costs for red-team ranking are $45 wrong-segment, $14
wasted impression, $220 under-18 PDPA, $8 cold-start.

CRITICAL: do NOT propose new thresholds or floors. The floors were
pre-registered in Phase 6; this phase MEASURES against them. If
re-seed Jaccard comes back at 0.74 and my Phase 6 floor was 0.80,
the finding is "below my pre-registered floor — Phase 8 gate
failure candidate", not "let me propose 0.70 as the new floor".

Rank findings by severity in dollars using §2 quotes. Tag each
finding as ACCEPT (accepted risk), MITIGATE (action before ship),
or RE-DO (a phase must re-run). My call on dispositions; your
recommendation in writing first.

Do NOT use "blocker" without naming the specific ship-action
blocked. "Segmentation unstable" is not a blocker; "cannot ship
the allocator because its input reshuffles every week" is.

When all five sweeps are in the journal with cited numbers, §2
quotes, and disposition recommendations, stop and wait for my
call per finding.
```

### Why this prompt is written this way

- Inheritance-framed opening names which sweeps are pre-committed (five, split 3+2 across USML and SML) and keeps the disposition call with me — the Trust Plane stays clean.
- Cite-or-cut is enforced because red-team findings without citations become un-auditable "the model failed" claims that score 1/4 on D3.
- "Do NOT propose new thresholds" is the load-bearing anti-cheat — without it the agent lowers floors post-hoc to pass the red team, destroying Phase 6's pre-registration value.
- ACCEPT / MITIGATE / RE-DO triage is explicit so the disposition vocabulary matches what `/redteam` expects at the COC-level close.
- One paste covers both USML (Sprint 1) and SML (Sprint 2 replay) because the disposition discipline is identical and separating them doubles the paste load.

### What to expect back

- `journal/phase_7_red_team.md` (Sprint 1) or `journal/phase_7_sml.md` (Sprint 2) with five cited findings.
- Per-segment Jaccard distribution (not just mean) from the re-seed sweep.
- Proxy-drop reassignment percentages for postal_district, age_band, and both combined.
- Brier-score-per-subgroup for churn and conversion classifiers.
- A ranked finding list with §2-quoted dollar severity and ACCEPT/MITIGATE/RE-DO tags.
- A stop signal pending my disposition call.

### Push back if you see

- A new threshold proposed ("I suggest lowering the stability floor to 0.70") — "my Phase 6 floor was X; this is a failure against that floor, not a floor adjustment."
- A finding without a file-and-function citation — "which file and function produced this?"
- A dollar severity without a §2 quote — "please quote the §2 row for this cost."
- Mean Jaccard only, without the distribution — "please report the distribution across seeds, not the mean."
- "Blocker: the model is unstable" — "which ship-action is blocked?"

### Adapt for your next domain

- Change `re-seed / proxy / operational collapse` USML sweeps to your domain's unsupervised stress tests.
- Change `calibration-per-subgroup / feature-ablation` SML sweeps to your domain's classifier stress tests.
- Change `postal_district, age_band` to your domain's protected-proxy candidates.
- Change `post-Black-Friday filter` to your domain's known regime-shift scenario.
- Change the `$45 / $14 / $220 / $8` §2 costs to your own cost table's equivalents.

### Evaluation checklist

- [ ] **Transparency:** top 3 features per segment / class named; one-sentence plain-language explanation of one output.
- [ ] **Robustness:** 3 worst subgroups with metrics; 3 worst months / conditions; adversarial perturbation behaviour.
- [ ] **Safety:** tail-risk in dollars; degenerate-input behaviour; blast-radius memo naming who is harmed.
- [ ] Fairness row ends with "deferred to Week 7 per Playbook" — explicit, not silent.

### Journal schema — universal

```
Phase 7 — Red-Team
Transparency: top features ____; one-sentence explanation ____
Robustness: worst subgroups ____; worst conditions ____
Safety: worst-1% cost $____; degenerate-input behaviour ____; blast radius ____
USML-specific: re-seed Jaccard distribution ____; proxy collapse test ____; operational collapse ____
Fairness: deferred to Week 7 per Playbook
Blockers: ____
Accepted risks: ____
Mitigations to ship with: ____
```

### Common failure modes

- Red-team stops at "the model sometimes gets confused" — no specifics.
- Explainability output produced (feature importance) but not surfaced as a Transparency finding (orphaned call).
- Safety dimension skipped because it "feels abstract" — grounding in $220 and $45 forces it concrete.

### Artefact

`workspaces/.../journal/phase_7_red_team.md`

### Instructor pause point

- Re-run the winning clustering with three seeds. Students compute churn by hand. Above what threshold is the segmentation unshippable?
- Ask: if segment 3 collapses when postcode is dropped, what do you tell the CMO — "ship anyway" or "re-cluster"? Make the dollar trade-off explicit.
- Demonstrate: filter to post-Black-Friday data and re-cluster. Smallest segment? If below 2%, which campaign is now uneconomical?

### Transfer to your next project

1. What is my domain's analogue of re-seed churn (any source of randomness that could be driving the output rather than the data)?
2. What is my domain's analogue of proxy leakage (any protected-class feature that could be silently doing the work of an apparently-neutral output)?
3. What is the smallest population my product can act on economically, and what signal tells me when a population dropped below it?

---

