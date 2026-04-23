<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Workflow 7 — /redteam (cross-sprint stress test)

> **What this step does:** Stress the three shipped models as a system — not in isolation — by re-seeding, dropping proxy features, and simulating operational collapse, then tracing each finding through the full cascade (Sprint 1 → 2 → 3).
> **Why it exists:** Per-model validation misses the failure mode that actually kills retail ML systems: instability in segmentation that cascades into classifier corruption and allocator distortion. The red team is the only phase that deliberately breaks things to measure what breaks downstream.
> **You're here because:** Phase 13 (Sprint 4 drift rules) is complete. All four sprints are done.
> **Key concepts you'll see:** cascade tracing, pre-registered floor, proxy leakage, operational collapse, disposition triage

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm entering /redteam. All sprints are done. My job here is to stress the
shipped models AS A SYSTEM — not each model in isolation. Failure in one
layer poisons every later layer; the red team must trace findings across the
full cascade.

Produce a redteam.md file with three sections — one per failure mode,
cross-cutting across all models:

1. STABILITY. Re-seed the upstream model with multiple different random
   seeds. For each seed, trace what changes in the downstream models and
   plans. Report the measured percentage change per output; do NOT compare
   it to a threshold — I will judge significance against the floors I pre-
   registered. Rank findings by dollar severity using sourced cost figures.

2. PROXY LEAKAGE. Drop the features that most resemble protected demographic
   attributes and re-run the upstream model. Count how many downstream labels
   change. Re-train the classifiers without these features — does performance
   drop, and by how many points? Re-solve the allocator with the proxy-dropped
   inputs. Report measured deltas; do NOT compare to a threshold. I decide
   whether the cascade leaked demographic structure.

3. OPERATIONAL COLLAPSE. Simulate a volume or mix shift (e.g. post-peak
   season). Re-run each model: does any segment shrink below minimum viable
   size? Does the classifier's calibration error blow past the threshold I
   set? Is the plan still feasible? Report dollar impact per finding.

For every technical claim, cite the file and function it lives in.
For every dollar figure, quote the cost source. Do NOT invent numbers.
Do NOT propose new thresholds mid-red-team. If a finding is below a pre-
registered floor, report it as a gate failure — not as a floor adjustment.

Do NOT use the word "blocker" without naming the specific action blocked.

When done, rank every finding by severity in dollars, tag each as:
(a) accept (accepted risk), (b) mitigate (action needed before ship),
or (c) re-do (a phase must re-run). Then stop — I decide disposition.
```

**Tonight-specific additions** (Week 5 Arcadia Retail):

```
Output file: workspaces/metis/week-05-retail/04-validate/redteam.md

Three sections match the three USML-specific sweeps from PLAYBOOK.md Phase 7:

1. STABILITY — re-seed with 3 different random seeds.
   For each seed trace:
   - Sprint 2: does the churn classifier's top-5 feature importance change?
     Does the conversion classifier's calibration drift?
   - Sprint 3: how much do the LP plan's segment-by-segment allocations in
     data/allocator_last_plan.json change?
   Report measured % change per segment. Judge against my Phase 6 USML and
   Phase 8 pre-registered floors — do NOT adjust the floors.
   Dollar severity: use PRODUCT_BRIEF.md §2 costs, quote the lines.

2. PROXY LEAKAGE — drop postal_district AND age_band from Sprint 1 features.
   - Re-cluster: how many customers change segments?
   - Re-train churn classifier without these features: AUC change in points?
   - Re-solve allocator with proxy-dropped segments: expected-revenue change?
   Report measured deltas. I decide whether the cascade leaked demographic
   structure.

3. OPERATIONAL COLLAPSE — filter data to post-Black-Friday shapes.
   - Re-cluster: does any segment shrink below 2% of customers?
   - Re-run churn classifier: does calibration error blow past Phase 6 SML
     threshold?
   - Re-solve allocator: is the plan still feasible?
   Report dollar impact per finding.

For every algorithm, model, or metric claimed, cite the file and function in
src/retail/backend/. If you cannot cite, say so — do NOT guess.

For every dollar figure, quote the PRODUCT_BRIEF.md §2 line. Do NOT invent.

Floor guard: "stability = 0.74; I suggest lowering to 0.70" is BLOCKED.
Report it as "below my pre-registered 0.80 floor — this is a Phase 8
deployment gate failure." Floors were pre-registered; red-team measures
against them, it does not move them.

Blocker guard: "The segmentation is unstable" is not a blocker. "I cannot
ship the allocator because its inputs reshuffle every week" is a blocker —
name the specific ship action that is blocked.

Disposition tags: (a) accept, (b) mitigate, (c) re-do.
```

**How to paste:** Combine both blocks into a single paste into your `claude` session.

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ `04-validate/redteam.md` exists with three sections: STABILITY, PROXY LEAKAGE, OPERATIONAL COLLAPSE
- ✓ Each finding traces through at least two sprints (not just Sprint 1 in isolation)
- ✓ Every technical claim cites a file and function in `src/retail/backend/`
- ✓ Every dollar figure is quoted from `PRODUCT_BRIEF.md §2`
- ✓ A ranked finding list with dollar severity and accept/mitigate/re-do tags
- ✓ No proposed new thresholds mid-red-team; floor violations reported as gate failures
- ✓ Stop signal pending your disposition call
- ✓ Viewer (http://localhost:3000) shows all 4 sprint tiles green (or flagged) in the cross-sprint banner

**Signals of drift — push back if you see:**

- ✗ A finding about Sprint 1 with no trace into Sprints 2 or 3 — ask "how does this segmentation finding propagate? The whole point is the cascade."
- ✗ A proposed new floor ("stability = 0.74; I suggest lowering to 0.70") — ask "my Phase 6 floor was 0.80 and it's below that. This is a Phase 8 failure, not a floor adjustment."
- ✗ An invented dollar figure — ask "please quote from `PRODUCT_BRIEF.md §2`."
- ✗ "Blocker: segmentation unstable" with no specific action — ask "which ship action is blocked?"
- ✗ A finding with no file-and-function citation — ask "which file computes this metric?"
- ✗ Only one or two sections in the file, missing a full failure-mode section — ask "where is the [STABILITY / PROXY / COLLAPSE] section?"

---

## 3. Things you might not understand in this step

_(v1 — if a concept you struggled with isn't here, flag it back to the author)_

- **Cascade tracing** — following a finding from where it originates (Sprint 1) through what it changes downstream (Sprints 2 and 3)
- **Pre-registered floor** — a performance minimum set before seeing results; a red-team finding below the floor is a gate failure, not an invitation to lower the floor
- **Proxy leakage** — when features correlated with a protected attribute (age, location) let a model learn demographic patterns without using the attribute directly
- **Operational collapse** — what happens to model outputs when the data distribution shifts sharply (e.g. post-peak season, traffic spike)
- **Disposition triage** — your call on each finding: accepted risk, needs mitigation, or requires a phase re-do

---

## 4. Quick reference (30 sec, generic)

### Cascade tracing

Following a red-team finding from where it originates to every downstream layer it affects. Tonight's cascade is: segmentation → classifiers → allocator. A re-seed finding that only reports "silhouette dropped 0.04" is incomplete — it needs to show what happened to the churn classifier's top features and to the LP plan's allocation percentages. Cascade tracing is what makes red-team findings actionable: you can't mitigate a segmentation instability without knowing how far the instability propagates.

> **Deeper treatment:** [appendix/06-monitoring/drift-types.md](./appendix/06-monitoring/drift-types.md)

### Pre-registered floor

A performance minimum you wrote in the phase journal before seeing results. The floor is honourable because it was set without foreknowledge. A red-team finding below the floor is a Phase 8 deployment gate failure — it means the model as shipped doesn't clear the standard you set. The correct response is to tag the finding as "re-do" or "accept with documented risk." The incorrect response is to revise the floor down to match the result: that retroactively validates a model that didn't clear the bar.

> **Deeper treatment:** [appendix/04-evaluation/pre-registered-floors.md](./appendix/04-evaluation/pre-registered-floors.md)

### Proxy leakage

When a model learns demographic patterns from correlated features rather than from the protected attribute directly. If age is excluded from the feature set but postal_district is included, and postal_district is 80% correlated with age bracket, the model effectively has age in the model — it just arrived via a proxy. Proxy leakage is detected by dropping the correlated features and measuring how much the model's output changes. Large changes mean the model was relying on the demographic pattern.

> **Deeper treatment:** [appendix/02-data/proxy-for-protected-class.md](./appendix/02-data/proxy-for-protected-class.md)

### Operational collapse

Testing what happens to model outputs when the data distribution shifts sharply — for example, filtering data to post-Black Friday shapes where volume doubled and mix shifted. Operational collapse tests whether the model's outputs remain usable under realistic stress conditions. A segment that shrinks below 2% of customers is too small to target with a distinct campaign; a classifier whose calibration error triples under volume spike can't be trusted for probability-based allocation.

> **Deeper treatment:** [appendix/06-monitoring/drift-types.md](./appendix/06-monitoring/drift-types.md)

### Disposition triage

Your per-finding call after seeing the red-team report: (a) **accept** — the risk is real but tolerable, documented with a rationale; (b) **mitigate** — an action is needed before the model ships (e.g. add a minimum-segment-size guard); (c) **re-do** — a Playbook phase must re-run with corrected parameters. Disposition is yours, not Claude Code's: the red-team report surfaces findings; you decide what to do with each one. This is the Trust Plane moment in `/redteam`.

> **Deeper treatment:** [appendix/07-governance/hitl-patterns.md](./appendix/07-governance/hitl-patterns.md)

---

## 5. Ask CC, grounded in our project (2 min)

Paste this if §4 isn't enough. CC will read our codebase and journal and tailor the explanation to Arcadia Retail.

```
You are helping me understand a concept from Metis Week 5, where I am
building an ML system for Arcadia Retail. I'm currently in the /redteam step.

Read `workspaces/metis/week-05-retail/playbook/workflow-07-redteam.md` for
what this step does, and read `workspaces/metis/week-05-retail/journal/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. cascade tracing >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current Arcadia state
3. Implications for the decision I'm about to make (or just made) in /redteam
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

Before moving on:

- [ ] `04-validate/redteam.md` exists with three sections (STABILITY, PROXY LEAKAGE, OPERATIONAL COLLAPSE)
- [ ] Each finding traces through at least two sprints
- [ ] Every technical claim cites a file and function
- [ ] Every dollar figure quoted from `PRODUCT_BRIEF.md §2`
- [ ] Ranked finding list with accept/mitigate/re-do tags
- [ ] Your disposition written per finding — Claude Code has stopped for your call

**Next file:** [`workflow-08-codify.md`](./workflow-08-codify.md)
