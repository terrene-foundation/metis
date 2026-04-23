<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

_[← Playbook index (README)](./README.md)_

## Phase 5 — Implications (Segment Selection)

```
──────────────────────────────────────────────────────────────────
 VALUE CHAIN:   Analyze ▸ Todos ▸ **USML ◉** ▸ SML ▸ Opt ▸ MLOps ▸ Close
 THIS PHASE:    Sprint 1 · Phase 5 of 8 — Implications
 LEVERS:        complexity-vs-interpretability · stability-vs-accuracy · speed-vs-performance
──────────────────────────────────────────────────────────────────
```

### Concept

Look at the Phase 4 leaderboard and make the human call: which approach, at which setting, do you stake your name on, and can you explain the trade-off in 30 seconds to someone who has never heard of silhouette. Every alternative gets rejected with a reason. "Claude Code recommended it" with no paragraph underneath is not a Phase 5.

### Why it matters (SML lens)

- Reinforces Week 4's model-selection discipline: top of the leaderboard is NOT automatically the pick. A Ridge that's 0.3% worse than XGBoost but trains in 2 seconds and is interpretable is often the right call for production.
- Reinforces Week 2's "defend in non-technical language" rule — if you can't explain it to the clinician/CMO/buyer, you can't ship it.
- Reinforces Week 3's fold-variance check: 82% mean precision with 15% fold-variance is more dangerous than 78% mean with 3% variance.

### Why it matters (USML lens)

- The "most statistically separated" clustering is often the **least actionable** — the algorithm finds a genuine pattern that marketing cannot build a campaign around ("customers who browse between 2–4 AM on Tuesdays").
- Each segment needs a **plain-language profile** — a paragraph a non-technical CMO can read. "Cluster 3: high_freq=0.81, low_promo_resp=0.22" is a statistical artefact; "customers who shop weekly on weekends and ignore promos" is a segment.
- **Stability trumps separation** in USML almost always. 0.62 silhouette with 88% stability beats 0.71 silhouette with 62% stability — the second one reshuffles 38% of customers each month, destroying every campaign plan.
- If a density-based approach leaves customers unassigned, the question isn't "is that OK" but "what is the cold-start fallback for those unassigned customers?" This cascades straight into Sprint 2.

### Your levers this phase

- **Lever 1 (the big one): complexity-vs-interpretability.** Complex model that wins by 0.02 silhouette but nobody can name the segments = lose. Simple model with slightly worse stats but named segments = win.
- **Lever 2 (usually matters): stability-vs-accuracy trade.** Always weight stability heavily; a "best" model that reshuffles monthly is unusable.
- **Lever 3 (only if scaling): speed-vs-performance.** If one candidate takes 10× to train for 2% gain, that only matters if you retrain often.
- **Skip unless specific:** hyperparameter micro-tuning (if you need to, do it here; don't leave it for Phase 8).

### Trust-plane question

Given the leaderboard, which approach do I stake my name on and why?

### Paste this

```
I'm entering Playbook Phase 5 — Implications. The scaffold
pre-committed to the leaderboard I'm about to read (produced in
Phase 4); my decision here is the pick — which candidate I stake my
name on, named in one paragraph of business language each, with every
rejected alternative given a reason.

Copy the Phase 5 skeleton from journal/skeletons/phase_5_implications.md
into workspaces/metis/week-05-retail/journal/phase_5_implications.md
(Sprint 1 USML). If this is the Sprint 2 SML replay, use
journal/phase_5_sml.md.

Read the Phase 4 leaderboard I just produced. Then:

1. For each candidate on the leaderboard (including the baseline),
   state: how well-separated (USML) or how accurate (SML), how
   stable across seeds / folds, how complex to train, how
   interpretable. One row per candidate, same columns.

2. For the top 2 USML candidates, profile EACH cluster in one
   paragraph of plain business language — no column names, no
   numbers. "Customers who shop on weekends and ignore promos" is
   a profile; "segment with high weekend_browse_fraction and
   low_promo_resp" is a statistical artefact.

   For SML, profile each model family the same way: which
   behaviours does this family predict well? which does it miss?
   What would the CX Lead hear if they asked "why did it pick
   this customer for retention?"

3. Recommend ONE candidate. For USML: weight stability over
   separation — 0.62 silhouette with 88% stability beats 0.71
   silhouette with 62% stability, because the second reshuffles
   every month and the CMO cannot campaign on a moving target.
   For SML: weight interpretability-over-AUC within 1 AUC point
   — the CX Lead will not ship a model she cannot explain to the
   retention team.

4. For every alternative you reject, give a one-sentence reason. A
   rejected alternative with no reason is "Claude Code said so",
   which does not ship.

Do NOT propose floors, thresholds, or K values. The pick is mine —
you write the recommendation and the rationale; I sign or overrule
in my journal. The floors go in Phase 6 and are pre-registered
BEFORE we revisit the leaderboard there.

Do NOT use "blocker" without naming the specific phase blocked. A
leaderboard where two candidates are within 1 point is a decision I
need to make, not a blocker.

When the recommendation and one-paragraph profiles are in the
journal, stop and wait for my pick.
```

### Why this prompt is written this way

- Inheritance-framed opening distinguishes the leaderboard (scaffold-produced via Phase 4) from the pick (my call at Phase 5) — prevents the agent from merging Phase 4 observation and Phase 5 decision.
- Plain-language cluster profiles are load-bearing because Phase 5 failure mode #3 is "cluster names read like column dumps" — CMO cannot act on `high_weekend_browse_fraction`.
- Stability-over-separation (USML) and interpretability-over-AUC (SML) are stated explicitly because the agent will default to the leaderboard top row unless told not to.
- "Rejected alternative with no reason is 'Claude Code said so'" is the anti-outsourcing clause — protects my Trust Plane call.
- Forbidding floors here preserves the Phase 6 pre-registration — any floor named in Phase 5 becomes post-hoc in Phase 6.

### What to expect back

- `journal/phase_5_implications.md` (or `_sml.md`) with a leaderboard-shape table plus a recommendation.
- One-paragraph plain-language profile per cluster (USML) or per model family (SML).
- A rejection reason for every non-recommended alternative.
- An explicit stability-or-interpretability framing for the recommendation.
- A stop signal pending my pick.

### Push back if you see

- Cluster profile that includes column names or numeric feature values — "please rewrite in plain language; no column names, no numbers. would a CMO recognize this segment on the street?"
- Recommendation based only on the top-of-leaderboard metric — "did you weigh stability (USML) or interpretability (SML)? top-of-leaderboard isn't automatic."
- Rejected alternative with no reason — "why was this rejected? one sentence, please."
- A proposed floor or threshold — "please remove; Phase 6 pre-registration is corrupted if I see a floor proposed here."
- "Recommend K=5" without the segment profiles — "profile every segment first; actionability comes before counting."

### Adapt for your next domain

- Change `weekend_browse_fraction / promo_resp` cluster-language examples to your domain's behavioural vocabulary.
- Change `CMO / CX Lead / retention team` stakeholders to the ones on your approval chain.
- Change `stability-over-separation` weighting for USML to your domain's trump dimension.
- Change `interpretability-over-AUC within 1 point` to your SML trade-off band.
- Change `Sprint 1 / Sprint 2` framing to your lifecycle naming.

### Evaluation checklist

- [ ] Every candidate compared on the same metrics.
- [ ] Headline advantage classified as meaningful (multiple %) vs noise (<1%).
- [ ] Stability examined explicitly (not assumed).
- [ ] Each cluster / class has a one-paragraph plain-language profile.
- [ ] Recommendation defensible in 30 seconds to a non-technical executive.

### Journal schema — universal

```
Phase 5 — Implications (Chosen)
Picked: ____ (family × hyperparameters)
Named outputs (one line each): ____
Rejected alternatives + why: ____
Why not the top of the leaderboard, if applicable: ____
```

### Common failure modes

- Student picks top of leaderboard without checking stability — scores 2/4 on D3.
- Student accepts Claude Code's recommendation verbatim — no Trust-plane decision happened.
- Cluster names read like column dumps ("segment with high RFM_R, low RFM_F") — CMO can't act on them.

### Artefact

`workspaces/.../journal/phase_5_segment_selection.md`

### Instructor pause point

- Pick the winning candidate. Read one segment's profile aloud. Ask the class: would you build a campaign for this? What would it be called? If nobody has a name within 30 seconds, the segment is weak.
- Show two candidates — one with higher silhouette, one with higher stability. Ask: which do you ship? Whose career is on the line?
- Ask: if 18% of customers are unassigned in the winning candidate, what do you tell the CMO? Is "they get the default campaign" acceptable?

### Transfer to your next project

1. For every output class, can I write a one-paragraph plain-language profile a non-technical executive could act on tomorrow?
2. Am I picking on the single most impressive metric, or have I weighted stability and actionability at least as heavily as separation/accuracy?
3. What is my explicit rejection reason for every alternative on the leaderboard — and does it hold up to "you're just lazy" pushback?

---

Same shape as Sprint 1 phases, applied to the classifiers. The levers and failure modes transfer. Key differences:

**Phase 5 SML — Implications.** Pick between logistic regression, random forest, GBM. Ensemble usually wins but not by enough to justify complexity over LR + domain features. Profile each model: "LR picks up weekend_browse_fraction and visits_per_week most; GBM picks up interactions between them." Name the winning family in one paragraph a non-technical executive could act on.

**Phase 7 SML — Red-team.** Re-seed the split, report variance. Drop-one-feature proxy tests: does any classifier rely on age_band (PDPA)? Worst-subgroup severity: which customer segment does the classifier most mispredict? Calibration per subgroup — are probabilities equally reliable across segments?

**Phase 8 SML — Gate.** Promote churn classifier + conversion classifier to shadow. Monitoring: calibration drift weekly, AUC decay monthly, per-subgroup performance gaps. Rollback: calibration error > 0.08 for 2 weeks OR AUC drop > 3 points.

All three journal entries (`phase_5_sml.md`, `phase_7_sml.md`, `phase_8_sml.md`) follow the same schema as Sprint 1.

---

# SPRINT 3 — OPTIMIZATION · Decide · Phases 10–12

**Why these are separate phases.** Phases 10–12 apply when your product has a **secondary optimization layer** on top of the models (allocator, scheduler, solver). Arcadia has one: given segments × predicted responses × budget × constraints, allocate campaigns optimally. Week 4's route planner was the Sprint 3 equivalent. **Deferrable** if your next project has no secondary layer (pure classification, pure clustering).

---

