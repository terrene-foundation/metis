<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 8 — Deployment Gate

> **What this phase does:** Run a go/no-go check against the floors you pre-registered in Phase 6, write a variance-grounded day-one monitoring plan, and name a specific rollback target — then execute the registry stage transition only after you sign off.
> **Why it exists:** "Feasible" is not the same as "shippable." Without a pre-registered check and a named rollback target, "deploy" is just a wish.
> **You're here because:** Phase 7 red-team just completed (`phase-07-redteam.md`). This is the gate between sprint work and the registry. You open this file TWICE tonight — once at the end of Sprint 1 USML, once at the end of Sprint 2 SML.
> **Key concepts you'll see:** deployment gate, PASS/FAIL floors, staging vs production, rollback channel, promotion criteria

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm entering Playbook Phase 8 — Deployment Gate. My decision here
is GO / NO-GO against the pre-registered floors I wrote in Phase 6,
plus the day-one monitoring plan and rollback trigger. I am
NOT proposing new criteria — I am checking the ones I already wrote.

Your job:

1. Read my Phase 6 floors from this sprint's journal file.
   Quote the values verbatim — the three floors for USML or the
   threshold rule + Brier calibration floor for SML. Do NOT
   propose or "suggest" new values.

2. Read my Phase 7 red-team findings. For every MITIGATE or
   RE-DO finding, flag it explicitly — I cannot ship through an
   unmitigated red-team finding. Name each one.

3. Measure the current artefact against each floor. Report PASS
   or FAIL per floor. If a floor fails, the gate is NO-GO unless
   I explicitly override in writing.

4. Draft the day-one monitoring plan. For each signal, name:
   (a) the signal (what is measured)
   (b) the cadence (weekly / monthly / daily)
   (c) the alert threshold — grounded in variance from the Phase 7
       sweep or from the scaffold's drift reference. "15% because
       the rolling variance's 95th percentile is 12%" is the
       correct form; "15% because it feels big" is not.
   (d) the owner (a role, not "the team")

5. Draft the rollback trigger — one specific signal + threshold
   + duration window. "Any segment drops below 2% of customers
   in one month" is specific; "if things go wrong" is not.

6. Draft the rollback TARGET — the artefact to fall back to. This
   must be something known to work today. For USML, the known
   fallback is the prior rule-based system, not a previous model
   version. For SML, the fallback is the previous threshold or
   rule-based flag logic — whichever is known to work.

7. Do NOT execute the registry stage transition yet. I sign the
   GO/NO-GO based on the PASS/FAIL table, then authorise the
   promotion myself.

For every technical claim — endpoint, file, function — cite.
Do NOT use "blocker" without naming the specific ship-action.

When the PASS/FAIL table, monitoring plan with variance-grounded
thresholds, rollback trigger, and rollback target are in the
journal, stop and wait for my GO/NO-GO call.
```

**Tonight-specific additions** (Week 5 Arcadia Retail):

_If this is your Sprint 1 USML pass (segmentation gate):_

```
Sprint 1 USML gate.
Journal file: copy journal/skeletons/phase_8_gate.md into
  workspaces/metis/week-05-retail/journal/phase_8_gate.md.
Phase 6 source: journal/phase_6_usml.md — the three USML floors
  (silhouette, bootstrap Jaccard, reassignment rate).
Phase 7 source: journal/phase_7_red_team.md — quote USML findings.
Monitoring signals for segmentation:
  - Segment-membership churn (monthly)
  - Monthly reassignment rate (monthly)
  - Campaign open-rate by segment (monthly, if feed a recommender)
Variance grounding: use observed values from Phase 7 sweep AND
  the scaffold drift reference at src/retail/data/drift_baseline.json.
Rollback target: the 2020 rule-based 5-segment system — not a
  previous clustering run. Previous random seeds are not rollback targets.
Monitoring owner for segmentation: E-com Ops Lead.
Registry endpoint to promote (after my GO): /segment/promote.
Registry state machine: staging → shadow → production.
Do NOT call /segment/promote until I say GO.
```

_If this is your Sprint 2 SML pass (classifier gate):_

```
Sprint 2 SML gate.
Journal file: copy journal/skeletons/phase_8_gate.md into
  workspaces/metis/week-05-retail/journal/phase_8_sml.md.
Phase 6 source: journal/phase_6_sml.md — the threshold rule +
  Brier calibration floor.
Phase 7 source: journal/phase_7_sml.md — quote SML findings.
Monitoring signals for classifiers:
  - Calibration decay (weekly — Brier score rolling)
  - AUC decay (weekly)
  - Feature PSI (weekly, top 5 features)
Variance grounding: use Phase 7 sweep values and
  src/retail/data/drift_baseline.json.
Rollback target: the previous threshold or the rule-based flag
  logic — whichever is known to work today.
Monitoring owner for classifiers: CX Lead.
Registry endpoint to promote (after my GO): /segment/promote (same
  endpoint, different model_id).
Do NOT call /segment/promote until I say GO.
```

**How to paste:** Use the USML block or the SML block alongside the universal core — whichever sprint you are closing.

---

## 2. Signals the output is on track

**Signals of success (Sprint 1 USML pass):**

- ✓ `journal/phase_8_gate.md` exists with a PASS/FAIL table of Phase 6 USML floors, each quoted verbatim
- ✓ Every Phase 7 MITIGATE / RE-DO finding named and addressed (or flagged as blocking GO)
- ✓ Monitoring plan as a table: signal / cadence / variance-grounded threshold / owner — one row per signal
- ✓ Alert threshold shows the variance computation ("95th percentile of historical drift variance = X%") not just the final number
- ✓ Rollback trigger is a single sentence with a specific signal, a threshold, and a duration window
- ✓ Rollback target is named and known to work today — not hypothetical
- ✓ Stop signal waiting for your GO/NO-GO — no registry transition yet
- ✓ Viewer (http://localhost:3000) shows: deployment-gate panel with a PASS/FAIL stamp against USML floors (silhouette, bootstrap Jaccard, reassignment rate), and registry state transition to shadow visible

**Signals of success (Sprint 2 SML pass):**

- ✓ `journal/phase_8_sml.md` exists with a PASS/FAIL table of Phase 6 SML floors (threshold rule + Brier floor), each quoted verbatim
- ✓ Every Phase 7 SML MITIGATE / RE-DO finding named and addressed (or flagged as blocking GO)
- ✓ Monitoring plan as a table: signal / cadence / variance-grounded threshold / owner — one row per signal for calibration decay, AUC decay, feature PSI
- ✓ Rollback trigger specific to classifier (threshold or rule-based flag)
- ✓ Stop signal waiting for your GO/NO-GO — no registry transition yet
- ✓ Viewer (http://localhost:3000) shows: deployment-gate panel with PASS/FAIL stamp against SML floors, and classifier registry transition to shadow visible

**Signals of drift — push back if you see:**

- ✗ Viewer shows nothing new after CC reports the phase complete — CC may have described the work without running it. Re-prompt: "show me the deployment-gate panel in the viewer; what does it say?"

- ✗ A monitoring threshold with no variance grounding ("15% feels about right") — ask "what is the 95th percentile of historical variance for this signal? ground the number or remove it"
- ✗ A rollback target described as "a previous model version" with no proof it exists — ask "is there an actual promoted model in the registry, or is this hypothetical?"
- ✗ A floor value different from what Phase 6 wrote — ask "my Phase 6 floor was X; the gate checks X, not a revised value"
- ✗ `/segment/promote` called before you said GO — ask to revert; GO is your call
- ✗ Monitoring plan written as prose with no signal/cadence/threshold/owner — ask for it as a four-column table
- ✗ Red-team findings ignored — ask "which MITIGATE findings are still unaddressed?"

---

## 3. Things you might not understand in this phase

_(v1 — if a concept you struggled with isn't here, flag it back to the author)_

- **Deployment gate** — the formal go/no-go check where pre-registered floors are tested against the current artefact, with a binary outcome
- **PASS/FAIL floors** — the specific metric thresholds you wrote in Phase 6; the gate checks them, not new ones proposed today
- **Staging vs production** — the two live environments in the registry state machine; shadow sits between them and is the minimum safe promotion destination
- **Rollback channel** — the specific artefact you fall back to if the deployed model degrades; must exist and work today, not in principle
- **Promotion criteria** — the set of conditions (floors passed, red-team clear, monitoring in place) that must ALL be true before you authorise the registry transition

---

## 4. Quick reference (30 sec, generic)

### Deployment gate

A gate is a binary outcome on a pre-registered list. "Looks good" is not a gate. A gate has: a list of floors (written before the sprint), a measurement against each floor, a PASS or FAIL, and a human signature. The point of writing floors in Phase 6 is so the Phase 8 gate is not invented in Phase 8. Without pre-registration, every sprint auto-passes because the floor is set after the measurement.

> **Deeper treatment:** [appendix/05-deployment/deployment-gate.md](./appendix/05-deployment/deployment-gate.md)

### PASS/FAIL floors

Floors are the minimum acceptable values for the metric(s) that determine whether a model is ready to deploy. You write them in Phase 6 before you see the final results; you check them in Phase 8 after. A floor that fails means NO-GO unless you override in writing with a reason. Override requires the business rationale, not a revised metric. An override without a reason is a gap in the audit trail.

> **Deeper treatment:** [appendix/04-evaluation/pre-registered-floors.md](./appendix/04-evaluation/pre-registered-floors.md)

### Staging vs production

The registry state machine tonight is: trial → staging → shadow → production. You never jump staging to production directly. Shadow is the in-between: the model runs against live traffic but its outputs are not acted on — so you can observe it without consequence. Shadow is the minimum safe promotion; production is the rollback channel's rollback channel. Promotion is a one-way door unless you have a rollback target.

> **Deeper treatment:** [appendix/05-deployment/shadow-staging-promotion.md](./appendix/05-deployment/shadow-staging-promotion.md)

### Rollback channel

The specific artefact you fall back to when the deployed model degrades. "We'd roll back to a prior version" is not a rollback channel; "we fall back to the 2020 rule-based 5-segment system currently running in staging" is. The rollback target must exist today, be known to work, and be reachable in one step. If you need to re-train to roll back, you don't have a rollback channel — you have a wish.

> **Deeper treatment:** [appendix/05-deployment/rollback-patterns.md](./appendix/05-deployment/rollback-patterns.md)

### Promotion criteria

The AND-list that must all be true before you sign GO: floors all pass, red-team findings all mitigated, monitoring plan in place with variance-grounded thresholds, rollback target named and reachable. Any single FALSE makes it NO-GO. The criteria are yours — the agent checks and reports, but GO is your signature.

> **Deeper treatment:** [appendix/05-deployment/deployment-gate.md](./appendix/05-deployment/deployment-gate.md)

---

## 5. Ask CC, grounded in our project (2 min)

Paste this if §4 isn't enough. CC will read our codebase and journal and tailor the explanation to Arcadia Retail.

```
You are helping me understand a concept from Metis Week 5, where I am
building an ML system for Arcadia Retail. I'm currently in Playbook
Phase 8 — Deployment Gate.

Read `workspaces/metis/week-05-retail/playbook/phase-08-gate.md` for
what this phase does, and read `workspaces/metis/week-05-retail/journal/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. rollback channel >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current Arcadia state
3. Implications for the decision I'm about to make (or just made) in Phase 8
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

Before moving on:

- [ ] `journal/phase_8_gate.md` (Sprint 1) or `journal/phase_8_sml.md` (Sprint 2) exists with a PASS/FAIL table
- [ ] Every Phase 6 floor quoted verbatim — no revised values
- [ ] Every Phase 7 MITIGATE / RE-DO finding addressed (or GO explicitly overrides in writing)
- [ ] Monitoring plan is a four-column table (signal / cadence / variance-grounded threshold / owner)
- [ ] Rollback trigger: one sentence, specific signal + threshold + duration window
- [ ] Rollback target: named artefact known to work today (2020 rulebook for USML; prior threshold or flag logic for SML)
- [ ] You signed GO — and only then was /segment/promote called

**If this is your Sprint 1 USML pass:**

**Next file:** [`workflow-04-sprint-2-sml-boot.md`](./workflow-04-sprint-2-sml-boot.md)

Sprint 1 is complete. Sprint 2 (SML — churn and conversion classifiers) boots next. You will re-open phase-04 through phase-08 for the SML sprint; the journal files will be suffixed `_sml.md`.

**If this is your Sprint 2 SML pass:**

**Next file:** [`workflow-05-sprint-3-opt-boot.md`](./workflow-05-sprint-3-opt-boot.md)

Sprint 2 is complete. Sprint 3 (optimisation — LP allocator) boots next.
