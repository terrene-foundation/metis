<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

_[← Playbook index (README)](./README.md)_

## Phase 3 — Feature Framing (UNFOLDED this week)

```
──────────────────────────────────────────────────────────────────
 VALUE CHAIN:   Analyze ▸ Todos ▸ **USML ◉** ▸ SML ▸ Opt ▸ MLOps ▸ Close
 THIS PHASE:    Sprint 1 · Phase 3 of 8 — Feature Framing
 LEVERS:        availability · leakage · proxy check · engineered derivation
──────────────────────────────────────────────────────────────────
```

### Concept

Every candidate input column classified on four independent axes: (a) available at prediction time? (b) leaky? (c) ethically loaded or regulatorily sensitive? (d) raw or engineered? Week 4 folded this into Data Audit because a supervised regressor with one leaky feature produces a bad prediction you can measure. Week 5 unfolds it because in unsupervised learning, an ethically loaded feature doesn't bias a model — it _creates a segment that is really a protected-class proxy_, and no accuracy metric will flag it.

### Why it matters (SML lens)

- Reinforces Week 2's rule: a feature fails leakage review if it wasn't available at the moment of prediction (discharge date for readmission: no).
- Reinforces Week 3's engineered-feature discipline: RFM, tenure decile, channel-mix entropy — every derived feature has a one-line derivation or it is a hidden bug.
- Reinforces Week 4's feature importance ladder: if one feature dominates 80% of the signal, it's a leakage candidate until proven otherwise.
- Dollar framing: leaving a single leaky feature in Week 4's forecast meant the $40/$12 cost-asymmetry logic was against a self-fulfilling prophecy. The fix prevented a live-production disaster.

### Why it matters (USML lens)

- **Postcode is not a neutral feature.** In Singapore it's a strong proxy for income, ethnicity, and school catchment. Cluster on it → a segmentation that looks behavioural and is actually demographic.
- **Under-18 status is a PDPA red line** (in Singapore; GDPR's under-16 in the EU). Including it is not bad manners; it's $220/record exposure.
- **The proxy check is the new tool:** cluster once with the demographic feature in, cluster once with it out, count how many customers change segments. If 30% move, the demographic was doing the work — the "behavioural" segmentation was demographic all along.
- Inferred sensitive attributes (purchases that imply health conditions, religion, sexual orientation) are equally loaded even when never named.

### Your levers this phase

- **Lever 1 (the big one): proxy-for-protected-class check.** On every demographic or demographic-adjacent feature, run the cluster-with / cluster-without swap and count reassignment. >30% reassignment → the feature was doing the demographic work.
- **Lever 2 (the discipline): availability audit.** Was this feature knowable at the moment the decision gets made? A feature that is only known retrospectively is a leakage bug wearing a pretty dress.
- **Lever 3 (the hygiene): engineered-feature derivation.** Every derived column has a one-line derivation recorded. No exceptions.
- **Lever 4 (the boundary): regulatory classification.** Name the regime (PDPA §13, GDPR Art. 9, HIPAA, ECOA) for each sensitive feature.
- **Skip unless specific:** feature scaling (standardization is universal for distance-based clustering — the scaffold handles it); encoding cardinality (handled by the scaffold's one-hot/frequency logic).

### Trust-plane question

Which features are safe, which are leaky, which are ethically loaded?

### Paste this

```
I'm entering Playbook Phase 3 — Feature Framing. The scaffold
pre-committed to the raw feature set loaded in
src/retail/backend/ml_context.py (customer-level behavioural and
demographic columns); my decision here is which features go into
Sprint 1 clustering and which stay out — especially the ones that
look behavioural but are really proxies for protected class.

Copy journal/skeletons/phase_3_features.md into
workspaces/metis/week-05-retail/journal/phase_3_features.md.

For each candidate feature, classify on four axes:

1. Available at prediction time? (yes / no — if no, leakage risk)
2. Leaky from the label or from future data? (a transaction_date
   >= decision_date is future-data leakage)
3. Ethically loaded or regulatorily sensitive? Name the regime —
   PDPA §13 for under-18 personalised-history (Singapore), GDPR
   Art. 9 for sensitive categories (EU), HIPAA for health. If the
   feature is age-band-derived, postal-district-derived, or
   category-purchase-derived (implying health or belief), flag it.
4. Raw or engineered? If engineered, one-line derivation.

For every feature you classify, cite the source — either the column
in src/retail/data/arcadia_customers.csv OR the function in
src/retail/backend/ml_context.py that derives it. If you cannot cite,
delete the claim.

Then run the proxy-drop test on the two strongest demographic
candidates (postal_district AND age_band):

A. Fit the clustering with the demographic feature IN.
B. Fit the clustering with the demographic feature OUT.
C. Report the reassignment rate — what fraction of customers
   changed segment between A and B.

Cite the exact function and endpoint you used (likely /segment/fit
per src/retail/backend/routes/segment.py). Report the reassignment
percentage — do NOT compare it to a threshold. My call.

Any dollar figure mentioned (e.g. $220 per under-18 PDPA record from
PRODUCT_BRIEF.md §2) must be quoted verbatim — do NOT invent.

Recommend IN / OUT per feature with a one-line reason. I decide.
Do NOT apply the feature set yet.

Do NOT use "blocker" without naming the specific phase blocked.

When classification, proxy-drop test, and recommendations are in the
journal, stop and wait for my per-feature approval.
```

### Why this prompt is written this way

- Inheritance-framed opening names the scaffold's raw-feature commitment and keeps the in/out decision with me — the agent drafts, doesn't decide.
- Cite-or-cut is required per feature to prevent invented columns — common Week 4 failure where the agent claims `weekend_browse_fraction` exists when it's actually `weekend_sessions` in the source.
- PDPA/GDPR/HIPAA are named explicitly because "ethically loaded" without a regime name scores 1/4 on rubric D4.
- The proxy-drop test is mechanical (A/B/report) to prevent the agent from "interpreting" the result — interpretation is my job, not theirs.
- Show-the-brief on the $220 PDPA figure is mandatory because the feature-out decision has teeth only when the dollar exposure is on the page.

### What to expect back

- `journal/phase_3_features.md` with every candidate feature on the four-axis table.
- The proxy-drop reassignment percentage for `postal_district` and for `age_band`, with the endpoint / function cited.
- A recommended IN / OUT per feature with reason, no thresholds applied.
- A named regime (PDPA §13, GDPR Art. 9, HIPAA, ECOA) for every feature flagged ethically loaded.
- A stop signal pending my per-feature approval.

### Push back if you see

- "Ethically loaded: unclear" or "possibly sensitive" with no named regime — "which regime? PDPA §13, GDPR Art. 9, HIPAA, or ECOA? if none applies, say so."
- A proxy-drop test reported as "passed" or "failed" — "please remove the pass/fail; report the reassignment percentage only. threshold is mine."
- An engineered feature with no one-line derivation — "what's the formula? cite the function or column combination."
- A feature list with no source citation — "which column in `arcadia_customers.csv` or which function in `ml_context.py` produces this?"
- A $220 figure not quoted from `PRODUCT_BRIEF.md §2` — "please paste the §2 row for the under-18 PDPA cost."

### Adapt for your next domain

- Change `postal_district and age_band` to your domain's strongest demographic proxies (zip code, birth year, country of origin).
- Change `PDPA §13 for under-18 personalised-history` to your jurisdiction's minor-protection regime.
- Change `arcadia_customers.csv` to your candidate-feature source.
- Change `category-purchase-derived (health / belief)` to the inferred-sensitive pattern in your data.
- Change the proxy-drop target (clustering) to your downstream model (classifier, recommender).

### Evaluation checklist

- [ ] Every candidate feature classified on all four axes — no hand-waving.
- [ ] Ethically-loaded features have a named rationale (which regime) AND a proxy-drop reassignment number.
- [ ] Engineered features have a derivation explanation (one sentence).
- [ ] Recommendation offered per feature, not bulk; you decide per feature.

### Journal schema — universal

```
Phase 3 — Feature Framing
Features IN: ____
Features OUT (with reason): ____
Ethically-loaded features kept IN with rationale: ____ (regime: ____)
Proxy-drop reassignment rate (if demographic feature kept): __%
Engineered feature derivations: ____
```

### Common failure modes

- "Ethically loaded" classified as "OK" with no rationale — scores 1/4 on D4.
- Proxy-drop test skipped because Claude Code "says postcode is fine" — student has outsourced their judgment.
- Engineered feature added without a one-line derivation — becomes a leakage vector six weeks later.

### Artefact

`workspaces/.../journal/phase_3_features.md`

### Instructor pause point

- Whiteboard the 4 axes as a 2×2 table (available × leaky, loaded × engineered). Place 10 Arcadia features into cells. Which cells ship? Which are show-stoppers?
- Ask: if a feature is both engineered AND loaded (e.g., "neighbourhood affluence index"), is it acceptable? Defensible rationale?
- Demonstrate: run the proxy-drop check live on postal_district. Report reassignment rate. Above what % does the segmentation stop being "behavioural"?

### Transfer to your next project

1. For each feature, can I defend its inclusion on all four axes, or am I hoping no one asks about (c)?
2. What are the protected-class features in MY domain (health condition, immigration status, language, age band, neighbourhood) — and have I run the proxy check?
3. Does every engineered feature have a one-line derivation recorded somewhere a future auditor can find — not in my head, on disk?

---

