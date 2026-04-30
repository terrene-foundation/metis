<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 8 — Deployment Gate (promote to shadow)

> **What this phase does:** PASS/FAIL the chosen model against the pre-registered floors and Phase 7 findings. If PASS, promote to shadow stage in the registry. If FAIL, name the blocker and the rerun plan.
> **Why it exists:** This is the formal sign-off. Without it, models get promoted by default and accumulate risk silently. The gate forces an explicit YES/NO with named criteria.
> **You're here because:** Phase 7 surfaced robustness findings. Phase 8 decides ship or no-ship.
> **Key concepts you'll see:** PASS/FAIL gate, promotion stage, rollback signal, shadow vs production, sign-off authority

---

## 1. Paste this into Claude Code

**Universal core:**

```
I'm in Playbook Phase 8 — Deployment Gate. The decision is PASS / FAIL
against pre-registered floors and Phase 7 findings.

Produce the gate document with these sections:

1. Pre-registered floors recap (from Phase 6 / 7 journals)
2. Per-floor PASS/FAIL with the actual measured value
3. HIGH-severity Phase 7 findings — RESOLVED or ACCEPTED-WITH-MITIGATION?
4. Inference-cost feasibility (Phase 5's $/day check)
5. Overall: PASS or FAIL
6. If PASS: promote to which stage (staging / shadow / production)?
   And what's the rollback signal?
7. If FAIL: which floor failed, what's the rerun plan?

Do NOT auto-promote — I sign the gate.
Do NOT use "blocker" without specifics.
```

**Tonight-specific additions** (Week 6 MosaicHub):

```
Sprint detection:
- Sprint 1 (Vision): gate the image moderator. Endpoint:
  POST /moderate/image/promote with { version, to_stage }.
- Sprint 2 (Text): gate the text moderator. POST /moderate/text/promote.
- Sprint 3 (Fusion): gate the fusion moderator. (Combined with Phase 12
  acceptance for the queue allocator.)

Pre-registered floors (Sprint-specific, recap from Phase 6):
- Per-class precision floor (named in Phase 6 journal)
- Per-class recall floor
- csam_adjacent (Sprint 1): hard-floor 0.4 threshold honoured
- Brier ceiling per class (calibration)
- $/day inference cost ceiling

HIGH-severity Phase 7 findings to address:
- Adversarial perturbation findings: did any flip a class above $10k/year?
- OOD findings: did any market or aspect-ratio fail?
- Demographic skew: did any slice show Brier > 0.20?
- Cross-modal (Sprint 3): did the cute-puppy case fire?

Promotion stages:
- staging → shadow: model runs alongside production, scores logged but
  not auto-acted. Default Phase 8 PASS target.
- shadow → production: requires 7 days of shadow data + cross-modal
  redteam pass. NOT a Phase 8 tonight decision unless instructor
  approves accelerated promotion.
- production → archived: rollback or planned retirement.

Rollback signal (must be NAMED, not described):
- Sprint 1: image-class P/R drops below floor for 3 consecutive days
- Sprint 2: text-class Brier exceeds floor for 24 hours
- Sprint 3: cross-modal-harm FP rate exceeds 10% for 1 hour
- Sprint 3 (queue allocator): SLA breach > 25% over a 1-hour window

Endpoint:
- POST /moderate/{image,text,fusion}/promote with { version, to_stage }

Journal file: copy journal/skeletons/phase_8_gate.md (suffix _vision /
_text / _fusion).
```

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ Pre-registered floors recapped from Phase 6/7 journals
- ✓ Per-floor PASS/FAIL with actual values
- ✓ HIGH-severity findings explicitly resolved or accepted-with-mitigation
- ✓ Inference-cost feasibility confirmed
- ✓ Overall PASS or FAIL stated
- ✓ Rollback signal NAMED (not described)
- ✓ POST to promote endpoint with to_stage="shadow" (default)
- ✓ Stop signal pending my sign-off

**Signals of drift — push back if you see:**

- ✗ "Mostly PASS" — ask "is it PASS or FAIL? Per floor."
- ✗ HIGH findings noted but not resolved/accepted — ask for explicit disposition per finding
- ✗ Auto-promote without my sign-off — ask to wait
- ✗ Rollback "monitoring metrics" without named threshold — ask for the specific signal
- ✗ Promotion to "production" without 7-day shadow data — ask "didn't we agree shadow is the Phase 8 target?"

---

## 3. Things you might not understand in this phase

- **PASS/FAIL gate** — explicit YES/NO with per-floor verdict, not vibes
- **Promotion stage** — staging → shadow → production, each with criteria
- **Rollback signal** — the named, monitorable signal that triggers automatic rollback
- **Shadow vs production** — shadow runs alongside, scores logged but not acted; production drives real auto-decisions
- **Sign-off authority** — the human (you, tonight) signs the gate; the agent doesn't auto-promote

---

## 4. Quick reference (30 sec, generic)

### PASS/FAIL gate

The Phase 8 gate is binary at the floor level: each pre-registered floor either passed or failed; the overall gate passes only if all floors pass AND no HIGH finding is unresolved. "Mostly passed" is BLOCKED — the rubric D5 (reversal condition) zeros vague gates. The gate is the structural place that prevents soft-quitting on a model that didn't quite make it.

> **Deeper treatment:** [appendix/05-deployment/deployment-gate.md](./appendix/05-deployment/deployment-gate.md)

### Promotion stage

The model registry has stages: staging (newly trained, untested in prod) → shadow (running alongside prod, scores logged but not acted) → production (driving auto-decisions) → archived (retired). Phase 8's PASS target is shadow — not production, because production requires shadow-period data first. The exception is instructor-accelerated promotion in the workshop.

> **Deeper treatment:** [appendix/05-deployment/deployment-gate.md](./appendix/05-deployment/deployment-gate.md)

### Rollback signal

A named, monitorable signal whose threshold-breach triggers automatic rollback. "Per-class P/R drops below floor for 3 consecutive days" is a rollback signal. "Things look bad" is not. The rollback signal must be in the same monitoring system Phase 13 sets up — otherwise rollback is manual and slow.

> **Deeper treatment:** [appendix/06-monitoring/retrain-rules.md](./appendix/06-monitoring/retrain-rules.md)

### Shadow vs production

Shadow: model runs in parallel to whatever's currently in production (or to no model, if first deploy). Predictions are logged but NOT acted on — auto-decisions still come from the rule system or the previous model. Shadow gives you 7 days of real-traffic data to confirm the offline holdout matched production. Production: model drives real auto-decisions; rollback signals fire on breach.

> **Deeper treatment:** [appendix/05-deployment/deployment-gate.md](./appendix/05-deployment/deployment-gate.md)

### Sign-off authority

The human signs the Phase 8 gate. Tonight that's you. The agent produces the gate document; you write PASS or FAIL into the journal. This isn't theatre — Legal Counsel signs Phase 8 in production reality. Tonight's exercise is teaching you to occupy that role: read the document, verify the floors, sign or send it back.

> **Deeper treatment:** [appendix/07-governance/hitl-patterns.md](./appendix/07-governance/hitl-patterns.md)

---

## 5. Ask CC, grounded in our project (2 min)

```
You are helping me understand a concept from Metis Week 6 Phase 8.

Read the phase file and `workspaces/metis/week-06-media/journal/phase_8_gate*.md`.

Explain "<<< FILL IN: concept name >>>" — plain language, MosaicHub-grounded,
implications for Phase 8 gate, what to push back on. Under 400 words.
```

---

## 6. Gate / next

- [ ] Per-floor PASS/FAIL stated with actual values
- [ ] HIGH-severity findings each have an explicit disposition
- [ ] Inference-cost feasibility confirmed
- [ ] Overall PASS or FAIL
- [ ] Rollback signal named (specific, monitorable)
- [ ] Awaiting my sign-off before promote endpoint fires

**Next file:** Sprint 1 → [`workflow-04-sprint-2-text-boot.md`](./workflow-04-sprint-2-text-boot.md). Sprint 2 → [`workflow-05-sprint-3-fusion-boot.md`](./workflow-05-sprint-3-fusion-boot.md). Sprint 3 → [`workflow-06-sprint-4-mlops-boot.md`](./workflow-06-sprint-4-mlops-boot.md).
