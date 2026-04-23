<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

_[← Playbook index (README)](./README.md)_

## Phase 11 — Constraint Classification

```
──────────────────────────────────────────────────────────────────
 VALUE CHAIN:   Analyze ▸ Todos ▸ USML ✓ ▸ SML ✓ ▸ **Opt ◉** ▸ MLOps ▸ Close
 THIS PHASE:    Sprint 3 · Phase 11 of 12 — Constraints
 LEVERS:        hard-vs-soft · penalty calibration · demotion rules · regulatory triggers
──────────────────────────────────────────────────────────────────
```

### Concept

For each rule the system must respect, classify **hard** (law, physics, contract — never crossable) or **soft** (preference — we'd rather not, at what price). Soft constraints get dollar penalties. Hard constraints get a regulatory/physical reason. When the world changes mid-sprint (the PDPA injection), re-classify and save both passes — before and after.

### Why it matters (SML + Optimization lens)

- **LP constraints are linear inequalities.** `A x ≤ b`. A hard constraint forbids `A x > b`; a soft constraint allows `A x > b` at a cost (`+ λ (A x − b)` in the objective with penalty coefficient λ).
- **Dual / shadow prices on hard constraints** tell you the cost of the regulation. If the PDPA hard constraint has shadow price $50k, that's the dollar cost of compliance.
- **Slack variables** make soft constraints workable: `A x − s ≤ b` where `s ≥ 0` is the violation, and `c^T x + λ · s` is the penalized objective.
- **Infeasibility diagnosis.** When no `x` satisfies all hard constraints, the LP is infeasible. Fix: demote a hard constraint to soft with a big penalty, or widen the budget. Infeasibility is a product problem, not a solver problem.

### Your levers this phase

- **Lever 1 (the big one): hard-vs-soft classification.** Law / contract / physics → hard. Preference / convenience → soft.
- **Lever 2 (the soft-constraint penalty):** in dollars per unit of violation. "$2 per touch over the per-segment cap" — defensible? The penalty should make the solver trade off soft constraint violation against objective gain.
- **Lever 3 (the demotion rule):** if all-hard produces infeasibility, demote to soft with a reasoned penalty. Document which one demoted and why.
- **Lever 4 (the regulatory trigger):** when a law changes mid-sprint (the PDPA injection), re-classify + re-solve. Save both passes as separate journal entries.

### Trust-plane question

Hard or soft for each rule? Penalty for each soft?

### Paste this

```
I'm entering Playbook Phase 11 — Constraint Classification. The
scaffold pre-committed to the constraint list (touch budget,
per-segment fatigue cap, PDPA under-18 browsing, inventory
availability, brand exclusion) exposed at /allocate/constraints
per src/retail/backend/routes/allocate.py; my decision here is
HARD vs SOFT per rule, plus the DOLLAR PENALTY on every soft
constraint. This is also where the PDPA mid-sprint injection
re-fires — I run Phase 11 twice, saving both passes.

First pass (pre-injection):

Copy journal/skeletons/phase_11_constraints.md into
workspaces/metis/week-05-retail/journal/phase_11_constraints.md.

For each constraint, classify:

1. Touch budget cap — hard (contract with marketing) or soft
   (over-spend at $X penalty)?
2. Per-segment fatigue cap — almost always soft; what's the
   dollar penalty per over-touch? Cite the per-customer touch
   cost ($3) from PRODUCT_BRIEF.md §2 verbatim as the floor
   on the penalty.
3. PDPA under-18 browsing — classify as SOFT or HARD (first
   pass; legal has not fired yet). Note the $220 per under-18
   record exposure from PRODUCT_BRIEF.md §2 verbatim.
4. Inventory availability — hard (physical): you cannot sell
   what you don't have.
5. Brand exclusion list — contract hard: you cannot push brand
   X to segment Y.

For every classification, name WHY — the regime (PDPA §13, MAS
circular, contract clause, physical limit) or the stakeholder
(CMO preference, Ops preference).

For every dollar figure, quote PRODUCT_BRIEF.md §2 verbatim. The
two §2 rows that drive Phase 11 are the $3 touch cost and the
$220 PDPA exposure. The $8 cold-start fallback is also a §2 row
and may appear as a penalty.

Do NOT propose penalty VALUES. Your job is the shape
("soft-with-penalty-per-unit-over-cap"); my job is the number.

Post-injection re-run (when instructor fires PDPA at ~4:30):

When I paste the injection payload (src/retail/data/scenarios/
pdpa_redline.json), copy the skeleton AGAIN into
journal/phase_11_postpdpa.md. Do not overwrite the first pass —
the rubric scores BOTH files.

In the re-run:
- Re-classify the PDPA under-18 rule as HARD (PDPA §13).
- Quote the $220 per under-18 record from PRODUCT_BRIEF.md §2
  verbatim as the compliance anchor.
- Save a before / after table showing what changed.
- Note that Phase 12 must now re-run — the LP in
  data/allocator_last_plan.json must be re-solved under the new
  hard constraint. Writing phase_11_postpdpa.md alone is a D3
  zero; Phase 12 re-solve is non-negotiable.

Do NOT POST /allocate/constraints until I approve per rule. The
classifications are my call; you draft, I sign.

Do NOT use "blocker" without naming the specific blocked
ship-action.

When first-pass classifications are drafted with §2 quotes and
cited regimes, stop and wait for me. When PDPA fires, repeat
into phase_11_postpdpa.md and stop again.
```

### Why this prompt is written this way

- Inheritance-framed opening names the scaffold's constraint list and endpoint, keeping the hard-vs-soft call with me — constraint classification is the #1 rubric-teeth moment of Sprint 3.
- Show-the-brief is mandatory on $3 and $220 because these are the two §2 rows where the rubric has 4/4 vs 1/4 scoring on D4.
- Mid-sprint injection is baked into the same paste so I don't lose the clock hunting for a second paste when the instructor fires — the postpdpa flow is a reentrant re-run, not a new prompt.
- "Writing `phase_11_postpdpa.md` alone is a D3 zero" is the load-bearing anti-trap sentence — it names the single most common Sprint 3 failure and attaches it to the rubric directly.
- Forbidding the `/allocate/constraints` POST before my approval prevents the agent from silently locking in a soft PDPA classification.

### What to expect back

- `journal/phase_11_constraints.md` with hard/soft per rule + regime cited + §2 dollar quotes.
- Later (post-injection): `journal/phase_11_postpdpa.md` with PDPA re-classified as HARD, plus a before / after table and a note that Phase 12 must re-run.
- Penalty SHAPES (not values) drafted for every soft constraint.
- A stop signal pending my per-rule approval — no `/allocate/constraints` POST yet.
- After the injection: an explicit cue that Phase 12 re-solve is next.

### Push back if you see

- A proposed penalty value ("$5 per over-touch") — "please remove; I set the value, you set the shape."
- $220 or $3 not quoted from `PRODUCT_BRIEF.md §2` — "please quote the §2 row."
- PDPA classified as SOFT in the post-injection pass — "PDPA §13 is a legal hard line; re-classify as HARD."
- Post-injection journal written but no note about Phase 12 re-solve — "the LP plan must re-run; please flag that Phase 12 is next."
- `/allocate/constraints` POSTed before my approval — "please revert; approval is my call per rule."

### Adapt for your next domain

- Change `touch budget / fatigue cap / PDPA / inventory / brand exclusion` to your domain's five constraints.
- Change `PDPA §13` to your jurisdiction's equivalent regulatory anchor.
- Change the `$220 / $3` §2 quotes to your domain's compliance + operational rates.
- Change `pdpa_redline.json` to your domain's mid-sprint injection payload.
- Change the regime hierarchy (contract / law / physics / preference) to match your constraint vocabulary.

### Evaluation checklist

- [ ] Every constraint classified with explicit rationale (law / contract / physics / preference).
- [ ] Soft constraints have defensible penalty values.
- [ ] No constraint labelled "probably hard" without a reason.
- [ ] Post-injection: PDPA correctly re-classified as hard (PDPA §13).
- [ ] Post-injection re-solve produces a different plan than pre-injection.

### Journal schema — universal

```
Phase 11 — Constraints
Hard: ____ (regime + reason each)
Soft: ____ (penalty $ each)
What changed post-injection (if applicable): ____ (from ___ to ___)
Shadow price of key hard: $ ____ (cost of compliance)
```

### Common failure modes

- Constraint mis-classified as soft when law says hard (PDPA!) — 1/4 on D4.
- All-hard produces infeasibility → student panics instead of demoting one.
- Penalty values unspecified ("some penalty") — LP solver can't use them.
- Student writes `phase_11_postpdpa.md` but doesn't re-solve the LP — Phase 12 still has the old plan.

### Artefact

`POST /allocate/constraints` + `journal/phase_11_constraints.md` + `journal/phase_11_postpdpa.md`.

### Instructor pause point

- Inject PDPA live. Ask every student to re-classify the under-18 browsing feature in 90 seconds. Collect. Anyone still at "soft" loses D4 — discuss why.
- Draw the constraint ladder: law → contract → preference → convenience. Place 5 rules.
- Ask: if 3 constraints are hard and the allocator is infeasible, what went wrong? Walk the recovery (demote one + justify).

### Transfer to your next project

1. For each constraint, can I name the exact law / contract clause / physical limit that makes it hard — or is "probably hard" doing the work?
2. For each soft constraint, is the penalty a real dollar or hand-wave — and does it actually change the system's behaviour (traced to the objective function, not just the journal)?
3. When the regulator changes the rules mid-project, do I have a process to re-classify in writing, save the before/after, and re-run — or will I just patch and hope?

---

