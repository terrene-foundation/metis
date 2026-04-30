<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 11 — Constraint Classification (hard vs soft)

> **What this phase does:** Classify every queue allocator constraint as HARD (inviolable; LP infeasible if violated) or SOFT (preferential; soft penalty in objective per unit violated). The IMDA injection re-runs this phase mid-Sprint-3.
> **Why it exists:** A constraint mis-classified as soft when it should be hard exposes the platform to regulator action. Mis-classified the other way and the LP becomes infeasible (no plan exists).
> **You're here because:** Phase 10 set the objective. Phase 11 sets the rules the LP must respect.
> **Key concepts you'll see:** hard vs soft, IMDA hard floor, soft penalty in objective, infeasibility, post-injection re-run

---

## 1. Paste this into Claude Code

**Universal core:**

```
I'm in Playbook Phase 11 — Constraint Classification. For each constraint
the queue allocator faces, classify HARD or SOFT.

HARD constraints: inviolable. LP cannot return a plan that violates them.
- Physics (reviewers can't review zero posts and infinite posts)
- Law (regulator-mandated SLAs, hard floors)
- Contract (SLA committed to enterprise customers)

SOFT constraints: preferential. LP allowed to violate at a $ penalty
per unit.
- Customer-experience preferences (90min SLA target — hard for high-tier,
  soft for low-tier)
- Operational preferences (per-reviewer fairness)

Produce a table:
| constraint | hard/soft | reason | penalty (if soft) |

Do NOT classify everything as HARD by default — over-constraining makes
the LP infeasible.
Do NOT use "blocker" without specifics.
```

**Tonight-specific additions** (Week 6 MosaicHub):

```
First-pass constraint set (BEFORE the IMDA injection):

HARD candidates:
- Reviewer headcount: cap at scaffold's reviewer_count config (HARD —
  physics; can't conjure reviewers)
- Per-reviewer max-shift: 8 hours (HARD — labour law)
- Auto-remove decision must be auditable (HARD — legal)

SOFT candidates:
- 90-min SLA on standard queue (SOFT — penalty $X/min late, where X
  is your call, defended)
- Per-tier balance (SOFT — fairness preference, penalty $/imbalance-unit)
- Cold-start handling: when CSAM-adjacent score is missing (model error),
  default to expedited queue (SOFT — operational pref)

PENDING (will be re-classified post-injection):
- csam_adjacent threshold: currently SOFT (cost-balanced, e.g. 0.85);
  will become HARD post-IMDA at 0.40 with mandatory-route-to-human in 60s.

Endpoint:
- POST /queue/constraints with the classified set

After IMDA injection fires (Sprint 3, ~4:30pm):
- Re-classify csam_adjacent: HARD with regulator-mandated 0.40 threshold
  AND 60s mandatory-human-review SLA on the expedited queue.
- Save second pass as journal/phase_11_postimda.md.
- The first pass STAYS in journal/phase_11_constraints.md — do NOT
  overwrite. Both files must exist at end of session for the rubric.

CRITICAL: missing the post-IMDA re-classification scores 0 on D4.
Missing the post-IMDA re-solve (Phase 12) scores 0 on D3.

Journal files:
- First pass: journal/phase_11_constraints.md (copy from skeleton)
- Re-run: journal/phase_11_postimda.md (copy from skeleton)
```

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ First-pass: constraint table with hard/soft per row, reason per row, $ penalty per soft
- ✓ csam_adjacent flagged as PENDING re-classification post-IMDA
- ✓ POST /queue/constraints fired
- ✓ Post-IMDA: separate journal file `phase_11_postimda.md` exists with explicit re-classification
- ✓ Both first-pass and post-IMDA journals end at session close
- ✓ Stop signal pending Phase 12

**Signals of drift — push back if you see:**

- ✗ Everything classified as HARD — ask "the LP becomes infeasible; which can be soft with a penalty?"
- ✗ csam_adjacent not flagged as PENDING — ask "what happens after IMDA fires?"
- ✗ A soft constraint with no $ penalty — ask "soft requires a $ per unit violated"
- ✗ Post-IMDA overwriting first-pass — ask "we need both files for rubric"
- ✗ The 60s SLA on csam_adjacent missed in the post-IMDA re-classification

---

## 3. Things you might not understand in this phase

- **Hard vs soft** — inviolable vs preferential-with-penalty
- **IMDA hard floor** — regulator-mandated minimum that converts soft → hard
- **Soft penalty in objective** — $ per unit violated, added to LP objective
- **Infeasibility** — what happens when the hard constraint set has no valid plan
- **Post-injection re-run** — Phase 11 fires twice tonight; second pass overrides on csam_adjacent

---

## 4. Quick reference (30 sec, generic)

### Hard vs soft

Hard constraints: violating them makes the plan invalid; the LP cannot return a plan that violates them. Examples tonight: reviewer headcount, labour-law shift cap, post-IMDA csam_adjacent. Soft constraints: violating them is allowed; each violation adds a $ penalty to the objective. Examples tonight: 90min SLA target, per-reviewer fairness, cold-start default.

> **Deeper treatment:** [appendix/07-governance/hard-vs-soft-constraints.md](./appendix/07-governance/hard-vs-soft-constraints.md)

### IMDA hard floor

The IMDA mandate converts csam_adjacent from a cost-balanced soft threshold (e.g. 0.85) to a regulator-mandated HARD threshold (0.40 with 60s mandatory-human-review). The LP must respect this — no auto-remove above 0.40 without expedited-human routing. Mis-classifying as soft = regulator action ($1M per incident). Mis-classifying as hard before the injection = unnecessarily tight LP.

> **Deeper treatment:** [appendix/07-governance/pdpa-basics.md](./appendix/07-governance/pdpa-basics.md)

### Soft penalty in objective

When a constraint is soft, the LP objective gets a term: `slack_for_constraint × $penalty`. The solver minimises the total objective including penalties — so it'll violate the soft constraint if doing so saves more $ elsewhere. The penalty value is your call; it should reflect real cost (e.g. $X per minute late on SLA reflects creator-trust impact).

> **Deeper treatment:** [appendix/07-governance/hard-vs-soft-constraints.md](./appendix/07-governance/hard-vs-soft-constraints.md)

### Infeasibility

When the hard constraint set has no valid plan, the LP returns INFEASIBLE. Common cause: hard constraints over-tightened (e.g. classifying SLA as hard when reviewer headcount can't possibly meet it). Recovery: soften one of the constraints. Tonight, the post-IMDA hard-floor + reviewer-headcount can collide; expanding expedited reviewers may be the soft-side fix.

> **Deeper treatment:** [appendix/07-governance/hard-vs-soft-constraints.md](./appendix/07-governance/hard-vs-soft-constraints.md)

### Post-injection re-run

Phase 11 fires twice tonight: once at start of Sprint 3 (cost-balanced csam_adjacent), once after IMDA injection (regulator-mandated csam_adjacent). Both journal files must exist at session end. The post-IMDA file is `phase_11_postimda.md`; it does NOT overwrite `phase_11_constraints.md`. Skipping the re-run scores 0 on rubric D4.

> **Deeper treatment:** [appendix/07-governance/pdpa-basics.md](./appendix/07-governance/pdpa-basics.md)

---

## 5. Ask CC, grounded in our project (2 min)

```
You are helping me understand a concept from Metis Week 6 Phase 11.

Read the phase file and `workspaces/metis/week-06-media/journal/phase_11_*.md`
(both first-pass and postimda).

Explain "<<< FILL IN: concept name >>>" — plain language, MosaicHub-grounded,
implications for Phase 11, what to push back on. Under 400 words.
```

---

## 6. Gate / next

- [ ] First-pass: constraint table classified hard/soft with reasons and penalties
- [ ] csam_adjacent flagged PENDING re-classification
- [ ] POST /queue/constraints fired
- [ ] Post-IMDA: `phase_11_postimda.md` exists with explicit re-classification
- [ ] Both files survive session close
- [ ] Stop signal pending Phase 12

**Next file:** [`phase-12-acceptance.md`](./phase-12-acceptance.md)
