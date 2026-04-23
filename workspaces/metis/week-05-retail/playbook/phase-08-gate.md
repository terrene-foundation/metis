<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

_[← Playbook index (README)](./README.md)_

## Phase 8 — Deployment Gate

```
──────────────────────────────────────────────────────────────────
 VALUE CHAIN:   Analyze ▸ Todos ▸ **USML ◉** ▸ SML ▸ Opt ▸ MLOps ▸ Close
 THIS PHASE:    Sprint 1 · Phase 8 of 8 — Deployment Gate
 LEVERS:        monitoring cadence · rollback channel · alert thresholds · promotion criteria
──────────────────────────────────────────────────────────────────
```

### Concept

The go/no-go. Write the criteria that must hold for this artefact to ship, the signals you monitor on day one, the specific measurable condition that triggers rollback. Then move the artefact from trial to shadow (or staging to production) in the registry. Every criterion is a signal and a threshold — no vibes.

### Why it matters (SML lens)

- Reinforces Week 4's ModelRegistry state-machine: illegal transitions blocked by the framework so you don't jump staging → production by accident.
- Reinforces Week 3's monitoring rule: "monitor production" means nothing; "monitor precision@50 weekly and alert when it drops below 0.62 for 2 consecutive weeks" is the point.
- Reinforces Week 2's "rollback is a path, not a wish" — you cannot roll back to a state that was never preserved.

### Why it matters (USML lens)

- The go signals are the **three floors from Phase 6**, not a single accuracy cutoff — the pre-commitment follows through.
- Monitoring signals include **segment-size stability**, **monthly reassignment rate**, and (where the segmentation feeds a recommender) **campaign open-rate-by-segment**. None of these exist in SML.
- **Rollback target is the previous rule-based system**, not a previous version of the same model — in USML "previous version" is a different random seed and isn't necessarily better. Rolling back to the 2020 rulebook is the honest fallback.

### Your levers this phase

- **Lever 1 (the big one): monitoring cadence.** Segmentation re-scores monthly; recommender drifts weekly; allocator daily. One alarm cannot watch all three.
- **Lever 2 (the rollback channel): shadow deployment.** Always promote to shadow before production. Production is the rollback channel's rollback channel.
- **Lever 3 (the alert thresholds): variance-grounded, not round numbers.** "15% drift" because it feels right is 1/4 on D5. "15% drift because the historical rolling variance has 95th percentile at 12%" is 4/4.
- **Lever 4 (the promotion criteria): the three floors re-tested, not re-declared.** The floors from Phase 6 must still hold on the deployment hold-out.

### Trust-plane question

Ship or don't ship, and on what monitoring?

### Paste this

```
I'm entering Playbook Phase 8 — Deployment Gate. The scaffold
pre-committed to the registry state machine (staging → shadow →
production) and the /segment/promote endpoint; my decision here is
ship-or-no-ship against my Phase 6 pre-registered floors, plus the
day-one monitoring plan and the rollback trigger. I am not
proposing new criteria; I am checking my pre-registered ones.

Copy journal/skeletons/phase_8_gate.md into
workspaces/metis/week-05-retail/journal/phase_8_gate.md (Sprint 1
USML) or journal/phase_8_sml.md (Sprint 2 SML).

Your job:

1. Read my Phase 6 floors from phase_6_usml.md (or phase_6_sml.md)
   — the three USML floors OR the SML threshold rule + Brier
   calibration floor. Quote the values I wrote, verbatim. Do NOT
   propose or "suggest" values.

2. Read my Phase 7 red-team findings from phase_7_red_team.md (or
   phase_7_sml.md). For every MITIGATE or RE-DO finding, flag it —
   I cannot ship through an unmitigated red-team finding.

3. Measure the current artefact (K=N chosen / classifier family
   chosen) against each floor. Report PASS or FAIL per floor. No
   threshold adjustments. If a floor fails, the gate is NO-GO
   unless I explicitly override in writing.

4. Draft the day-one monitoring plan. For each signal, name:
   (a) the signal,
   (b) the cadence (weekly / monthly / daily),
   (c) the alert threshold — GROUNDED IN VARIANCE, not a round
       number. "15% because the rolling variance's 95th percentile
       is 12%" is D5 = 4/4; "15% because it feels big" is D5 =
       1/4. Compute the variance from the observed Phase 7 sweep
       numbers I just produced, or from the scaffold's drift
       reference at src/retail/data/drift_baseline.json.
   (d) the owner (role — E-com Ops Lead for segmentation, CX Lead
       for classifier).

5. Draft the rollback trigger — one specific signal + threshold
   + duration window. "Any segment drops below 2% of customers in
   one month" is specific; "if things go wrong" is 0/4 on D5.

6. Draft the rollback TARGET — the artefact we fall back to. For
   Sprint 1 USML, the known-working rollback is the 2020
   rule-based 5-segment system (not a previous clustering). For
   Sprint 2 SML, the rollback is the previous threshold or the
   rule-based flag logic — whichever is known to work.

7. Do NOT execute /segment/promote yet. I sign the GO/NO-GO based
   on the PASS/FAIL table, then call /segment/promote myself (or
   authorize you to).

For every technical claim — endpoint, file, function — cite.
For every dollar figure (rare here), quote the §2 line.

Do NOT use "blocker" without naming the specific ship-action.

When the PASS/FAIL table, monitoring plan with variance-grounded
thresholds, rollback trigger, and rollback target are in the
journal, stop and wait for my GO/NO-GO call.
```

### Why this prompt is written this way

- Inheritance-framed opening names the scaffold's registry commitment and keeps the GO/NO-GO with me — the agent does not "pass" the gate on my behalf.
- Reading my Phase 6 values verbatim rather than re-proposing them is the structural defence of pre-registration — floors written in Phase 6 are the floors checked in Phase 8, unchanged.
- Variance-grounded monitoring thresholds are explicitly required with a 4/4-vs-1/4 scoring example, because the #1 D5 failure is "15% because it feels big".
- Forbidding `/segment/promote` until my GO is the structural anti-auto-ship — the agent does not decide to push staging → shadow.
- Rollback TARGET being the 2020 rulebook (USML) or previous threshold (SML) is named explicitly so the agent doesn't invent a "previous model version" that doesn't exist.

### What to expect back

- `journal/phase_8_gate.md` (or `_sml.md`) with a PASS/FAIL table of the Phase 6 floors.
- A day-one monitoring plan with signal / cadence / variance-grounded threshold / owner per line.
- A one-line rollback trigger (specific signal + threshold + duration).
- A named rollback target known to work today (2020 rulebook for USML; previous threshold for SML).
- A stop signal pending my GO/NO-GO — no `/segment/promote` call yet.

### Push back if you see

- A monitoring threshold without variance grounding — "what's the 95th percentile of historical variance? ground the number or remove it."
- A rollback target that's "a previous version of the model" without proof it exists — "is there actually a previous promoted model in the registry, or is this hypothetical?"
- Floors re-proposed ("recommend lowering stability to 0.75") — "my Phase 6 floor was 0.80; the gate checks against that, not a new value."
- `/segment/promote` called before I said GO — "please revert the promotion; GO is my call."
- Monitoring prose without a signal/cadence/threshold/owner — "please rewrite as a table with those four columns."

### Adapt for your next domain

- Change `/segment/promote` to your registry's promotion endpoint.
- Change `staging → shadow → production` to your registry's state machine.
- Change `drift_baseline.json` to your variance reference file.
- Change `2020 rulebook` (USML rollback) to your domain's incumbent / no-ML fallback.
- Change `E-com Ops Lead / CX Lead` to your monitoring owners.

### Evaluation checklist

- [ ] Go/no-go criteria are measurable (named metric thresholds, not "it looks good").
- [ ] Monitoring plan names specific signals + alert thresholds + cadence.
- [ ] Rollback trigger is automatable (specific signal, not "if things go bad").
- [ ] Registry stage transition executed (shadow minimum).
- [ ] Rollback target is known to work today (not "a prior version we'd roll back to").

### Journal schema — universal

```
Phase 8 — Deployment Gate
Go / No-Go: ____
Monitoring (signal + threshold + cadence + owner): ____
Rollback trigger (specific signal): ____
Rollback target (known-working): ____
Registry transition: staging → ____
```

### Common failure modes

- Monitoring written as prose, no signals — grader cannot verify.
- Rollback trigger tied to non-existent signal.
- Rollback target is "a previous model" that doesn't exist / is worse than the baseline.
- Illegal registry transition attempted (production → staging directly).

### Artefact

`workspaces/.../journal/phase_8_gate.md` + registry record at shadow or higher.

### Instructor pause point

- Ask: what signal fires the rollback this week? Can the monitoring system actually watch it? If "someone would notice" — it is not a signal.
- Walk through registry states on the board. Why can trial → pre-production but not trial → production directly?
- Demonstrate: show a monitoring plan as prose. Ask the class to rewrite as signal + threshold + cadence + owner. Count missing fields.

### Transfer to your next project

1. What specific signal — nameable by a monitoring system — fires my rollback, and have I verified the signal is actually collectable in my pipeline?
2. What is my rollback _target_ — a prior model version, a rule-based system, or a no-op default — and is it known to work today?
3. Have I executed the registry/artefact transition so the deployment is a recorded event, not an implicit understanding?

---

