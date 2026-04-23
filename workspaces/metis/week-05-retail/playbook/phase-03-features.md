<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 3 — Feature Framing

> **What this phase does:** Classify every candidate input column on four axes — available at decision time, leaky, ethically loaded, raw or engineered — then run a proxy-drop test on demographic features before deciding what goes into the model.
> **Why it exists:** In unsupervised learning, an ethically loaded feature doesn't bias a metric — it creates a segment that is really a protected-class proxy, and no accuracy number will flag it.
> **You're here because:** Data Audit is done (`phase-02-data-audit.md`) and dispositions are approved. Now you decide which features go in.
> **Key concepts you'll see:** feature leakage, proxy-for-protected-class, availability-at-decision-time, feature engineering vs derivation

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm entering Playbook Phase 3 — Feature Framing. My decision here is
which features go into this sprint's model and which stay out —
especially features that look behavioural but are really proxies for
a protected class.

Copy the Phase 3 skeleton from journal/skeletons/phase_3_features.md
into the project journal.

For each candidate feature, classify on four axes:

1. Available at prediction time? (yes / no — if no, leakage risk)
2. Leaky from the label or from future data? (a value recorded after
   the decision point is future-data leakage)
3. Ethically loaded or regulatorily sensitive? Name the regime —
   PDPA §13 for under-18 personalised history (Singapore), GDPR
   Art. 9 for sensitive categories (EU), HIPAA for health data. If
   the feature is age-band-derived, postcode-derived, or
   category-purchase-derived (implying health or belief), flag it.
4. Raw or engineered? If engineered, one-line derivation.

For every feature you classify, cite the source — either the column
in the source dataset OR the function that derives it. If you cannot
cite, delete the claim.

Then run the proxy-drop test on the two strongest demographic
candidates:
A. Fit this sprint's model with the demographic feature IN.
B. Fit this sprint's model with the demographic feature OUT.
C. Report the reassignment rate — what fraction of records changed
   output between A and B.

Report the reassignment percentage only. Do NOT compare it to a
threshold — that is my call.

Recommend IN / OUT per feature with a one-line reason. I decide.
Do NOT apply the feature set yet.

When classification, proxy-drop results, and recommendations are in
the journal, stop and wait for my per-feature approval.
```

**Tonight-specific additions** (Week 5 Arcadia Retail):

```
Feature source: columns in src/retail/data/arcadia_customers.csv OR
  functions in src/retail/backend/ml_context.py. Cite one of these
  for every feature — no exceptions.
Proxy-drop candidates: postal_district AND age_band. Run both.
Endpoint for proxy-drop: /segment/fit per
  src/retail/backend/routes/segment.py.
Regime citations: PDPA §13 for under-18 personalised history
  (Singapore). ECOA for any income-proxy feature.
Dollar anchor: $220 per under-18 PDPA record from PRODUCT_BRIEF.md §2
  — quote the line verbatim if you mention it. Do NOT invent.
Feature scaling: standardisation is handled by the scaffold for
  distance-based clustering — do not add a separate step.
```

**How to paste:** Combine both blocks into a single paste.

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ Every candidate feature classified on all four axes — no hand-waving on any axis
- ✓ Every feature citation names a specific column in `arcadia_customers.csv` OR a function in `ml_context.py`
- ✓ Proxy-drop reassignment percentages reported for `postal_district` and `age_band` (numbers only, no pass/fail)
- ✓ Every ethically-loaded feature has a named regime (PDPA §13, GDPR Art. 9, HIPAA, ECOA)
- ✓ IN / OUT recommendations given per feature — no bulk "all clear"
- ✓ No feature set applied yet — stop signal waiting for approval
- ✓ Viewer (http://localhost:3000) shows: feature inventory panel with all candidate features listed, each tagged with availability / leakage / proxy / engineered status

**Signals of drift — push back if you see:**

- ✗ "Ethically loaded: unclear" or "possibly sensitive" with no named regime ("which regime? PDPA §13, GDPR Art. 9, HIPAA, or ECOA?")
- ✗ Proxy-drop result reported as "passed" or "failed" ("please remove the pass/fail; report the reassignment percentage only — threshold is mine")
- ✗ An engineered feature with no one-line derivation ("what's the formula? cite the function or column combination")
- ✗ A feature listed with no source citation ("which column or function in `ml_context.py` produces this?")
- ✗ A $220 figure not quoted from `PRODUCT_BRIEF.md §2` ("please paste the §2 row")
- ✗ Viewer shows nothing new after CC reports the phase complete — re-prompt: "show me the feature inventory panel in the viewer"

---

## 3. Things you might not understand in this phase

_(v1 — if a concept you struggled with isn't here, flag it back to the author)_

- **Feature leakage** — using information that wouldn't have been available at the moment the decision is made, causing the model to cheat
- **Proxy-for-protected-class** — a feature that looks neutral (postcode, age band) but is actually a stand-in for a protected characteristic (race, income, age)
- **Availability-at-decision-time** — the discipline of asking "could I have known this value when the decision was made?" for every single feature
- **Feature engineering vs derivation** — the difference between creating a new column (engineering) and just renaming or transforming an existing one (derivation), and why the distinction matters for auditability

---

## 4. Quick reference (30 sec, generic)

### Feature leakage

Using a feature that encodes the answer — either because it was recorded AFTER the decision point (future-data leakage) or because it's derived directly from the target (label leakage). Classic example: a discharge diagnosis code used to predict readmission, where the diagnosis is only written at discharge — the same time you're trying to predict. Leaky features produce suspiciously good models that fail completely in production when the "future" data isn't available yet.

> **Deeper treatment:** [appendix/02-data/leakage.md](./appendix/02-data/leakage.md)

### Proxy-for-protected-class

A feature that appears neutral — postcode, shopping-hours pattern, purchase category — but is statistically correlated with a protected characteristic such as race, religion, or income level. In Singapore, postal district is a strong proxy for ethnicity and school catchment. The proxy check is mechanical: cluster with the feature in, cluster with it out, count how many records change segment. If 30%+ move, the feature was doing the demographic work.

> **Deeper treatment:** [appendix/02-data/proxy-for-protected-class.md](./appendix/02-data/proxy-for-protected-class.md)

### Availability-at-decision-time

For every feature: "Could I have known this value at the exact moment the model makes its prediction?" A transaction date that falls after the decision point is future-data leakage. A cumulative spend figure computed from data after the cutoff is leakage. This axis is asked separately from leakage because a feature can be available AND still leaky from the label. Both axes must pass independently.

> **Deeper treatment:** [appendix/02-data/leakage.md](./appendix/02-data/leakage.md)

### Feature engineering vs derivation

Engineering creates new signal from multiple source columns — RFM score, channel-mix entropy, tenure decile. Derivation transforms a single column — log of spend, binned age. The distinction matters because engineered features are harder to audit: they combine multiple columns and any of those columns could be leaky or ethically loaded. Every engineered feature needs a one-line derivation (the formula or function call) on record so a future auditor can trace it.

> **Deeper treatment:** [appendix/02-data/feature-framing.md](./appendix/02-data/feature-framing.md)

---

## 5. Ask CC, grounded in our project (2 min)

Paste this if §4 isn't enough. CC will read our codebase and journal and tailor the explanation to Arcadia Retail.

```
You are helping me understand a concept from Metis Week 5, where I am
building an ML system for Arcadia Retail. I'm currently in Playbook
Phase 3 — Feature Framing.

Read `workspaces/metis/week-05-retail/playbook/phase-03-features.md`
for what this phase does, and read `workspaces/metis/week-05-retail/journal/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. proxy-for-protected-class >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current Arcadia state
3. Implications for the decision I'm about to make (or just made) in Phase 3
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

Before moving on:

- [ ] Every candidate feature classified on all four axes
- [ ] Proxy-drop reassignment percentages reported (not pass/fail) for `postal_district` and `age_band`
- [ ] Every ethically-loaded feature has a named regulatory regime
- [ ] Every engineered feature has a one-line derivation
- [ ] IN / OUT decision made per feature; none applied yet

**Next file:** [`phase-04-candidates.md`](./phase-04-candidates.md)
