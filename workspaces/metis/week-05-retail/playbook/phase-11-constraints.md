<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 11 — Constraint Classification

> **What this phase does:** For every rule the allocator must respect, decide whether it is hard (never crossable — law, contract, physics) or soft (crossable at a dollar cost), and set the penalty shape for each soft constraint. When the PDPA injection fires, re-run this phase and save both passes.
> **Why it exists:** The solver cannot distinguish a legal line from a preference — you must classify first, or you will either over-constrain the problem to infeasibility or silently allow a compliance violation.
> **You're here because:** Phase 10 set the objective (`phase-10-objective.md`). Constraints wrap the objective. You open this file TWICE if the PDPA injection fires — once before, once after.
> **Key concepts you'll see:** hard vs soft constraints, penalty calibration, constraint demotion, PDPA hard-line classification, regulatory trigger

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm entering Playbook Phase 11 — Constraint Classification. My
decision here is HARD vs SOFT per rule, and the DOLLAR PENALTY
SHAPE on every soft constraint. I am NOT setting penalty values;
I am choosing the shape ("soft with penalty per unit over cap").

Your job:

1. For each constraint in the list, classify:
   - HARD: law / contract / physical limit — never crossable.
     Name the specific regime (statute, clause, physical fact).
   - SOFT: preference / operational target — crossable at a cost.
     Name the penalty shape: "dollar penalty per unit of violation
     over the cap". Do NOT propose the dollar value; I set that.

2. For every soft constraint, quote the relevant cost rate from
   the project's cost source verbatim. If the rate is not in
   the cost source, say so — do NOT invent a number.

3. For every hard constraint, name the specific law, contract
   clause, or physical fact that makes it hard. "Probably hard"
   or "should be hard" is not a classification.

4. If all-hard produces an infeasible LP, identify which hard
   constraint is the candidate for demotion to soft, with a
   reasoned penalty. Infeasibility is a product problem, not a
   solver problem. Flag it clearly.

5. Do NOT POST to the constraints endpoint until I approve each
   rule. The classifications are my call; you draft, I sign.

Post-injection re-run (when the regulatory event fires mid-sprint):

When I paste the injection payload, copy the constraint skeleton
into a new journal file (e.g. phase_11_postpdpa.md). Do NOT
overwrite the first pass — the rubric scores BOTH files.

In the re-run:
- Re-classify the affected rule as HARD based on the new
  legal text.
- Show a before/after table: what changed, which regime now
  applies.
- Note explicitly that Phase 12 must re-solve — writing the
  post-injection journal file alone without re-running the
  solver is a rubric failure. The plan in the last-plan
  persistence file MUST be different from the first-pass plan.

Do NOT use "blocker" without naming the specific blocked
ship-action.

When first-pass classifications are drafted with cited regimes
and §-quoted rates, stop and wait for my approval. When the
injection fires, repeat into the new journal file and stop again.
```

**Tonight-specific additions** (Week 5 Arcadia Retail):

_First pass (pre-injection, before ~4:30pm):_

```
Journal file: copy journal/skeletons/phase_11_constraints.md into
  workspaces/metis/week-05-retail/journal/phase_11_constraints.md.
Scaffold constraint list from /allocate/constraints per
  src/retail/backend/routes/allocate.py:
  1. Touch budget cap
  2. Per-segment fatigue cap
  3. PDPA under-18 browsing feature
  4. Inventory availability
  5. Brand exclusion list

Classification guidance (first pass, before legal fires):
  1. Touch budget — is this a contract commitment or an operational
     preference? Name the party. Hard = named contract; Soft = budget
     preference with overspend penalty.
  2. Per-segment fatigue cap — almost always soft. Penalty shape:
     "dollar penalty per touch over the per-segment cap." The per-
     customer touch cost ($3) from PRODUCT_BRIEF.md §2 verbatim is
     the floor for the penalty rate.
  3. PDPA under-18 browsing — FIRST PASS: classify as soft or hard
     based on your current reading. Note the $220 per under-18 record
     exposure from PRODUCT_BRIEF.md §2 verbatim. Legal has not fired yet.
  4. Inventory availability — hard (physical): cannot sell what is not
     in stock. No regime needed beyond "physical limit".
  5. Brand exclusion list — hard (contract): naming the clause that
     forbids pushing brand X to segment Y.

The two §2 rows that drive Phase 11: $3 touch cost, $220 PDPA
  exposure. Also relevant: $8 cold-start fallback (may appear as a
  constraint penalty for cold-start sessions).

Do NOT POST /allocate/constraints until I approve per rule.
```

_Post-injection re-run (when instructor fires PDPA at ~4:30pm):_

```
When I paste src/retail/data/scenarios/pdpa_redline.json:
  - Copy the skeleton AGAIN into:
    workspaces/metis/week-05-retail/journal/phase_11_postpdpa.md
  - Do NOT overwrite phase_11_constraints.md — both files must exist.
  - Re-classify PDPA under-18 browsing as HARD (PDPA §13).
  - Quote the $220 per under-18 record from PRODUCT_BRIEF.md §2 verbatim
    as the compliance anchor.
  - Show a before/after table: constraint name | first-pass classification
    | post-injection classification | regime change.
  - State explicitly: "Phase 12 must now re-solve. The file at
    data/allocator_last_plan.json must be different from the first-pass
    plan. If it is byte-identical, the solver did not pick up the new
    hard constraint."
  - Writing phase_11_postpdpa.md without triggering the Phase 12 re-solve
    is a rubric failure (D3 zero). Name this risk explicitly.
```

**How to paste:** Use the universal core plus the first-pass block. Keep the post-injection block ready to paste when the instructor fires the PDPA injection.

---

## 2. Signals the output is on track

**Signals of success (first pass):**

- ✓ `journal/phase_11_constraints.md` exists with HARD or SOFT per constraint and a cited regime for every HARD
- ✓ Every soft constraint has a penalty shape (not a value) — "dollar penalty per unit over cap"
- ✓ $3 touch cost and $220 PDPA exposure both quoted verbatim from `PRODUCT_BRIEF.md §2`
- ✓ No constraint labelled "probably hard" — a regime or a physical fact is named for every HARD
- ✓ Stop signal waiting for your per-rule approval — no `/allocate/constraints` POST yet
- ✓ Viewer (http://localhost:3000) shows: constraint panel with HARD/SOFT classification per rule and dollar penalties for soft constraints

**Signals of success (post-injection):**

- ✓ `journal/phase_11_postpdpa.md` exists alongside `journal/phase_11_constraints.md` — both present
- ✓ PDPA re-classified as HARD (PDPA §13) in the post-injection file
- ✓ Before/after table showing what changed and which regime now applies
- ✓ Explicit note that Phase 12 must re-solve and that `data/allocator_last_plan.json` must be different
- ✓ Viewer (http://localhost:3000) shows: constraint panel updated with the under-18 PDPA row highlighted in red (hard-line), and a change indicator showing the reclassification

**Signals of drift — push back if you see:**

- ✗ Viewer shows nothing new after the PDPA injection — CC may have only written the journal entry without re-classifying in the constraint panel. Re-prompt: "show me the constraint panel; does the PDPA row show as hard-line?"

- ✗ A proposed penalty value ("$5 per over-touch") — "please remove; I set the value, you set the shape"
- ✗ $220 or $3 not quoted from `PRODUCT_BRIEF.md §2` — "please quote the §2 row for this rate"
- ✗ PDPA still classified as SOFT in the post-injection pass — "PDPA §13 is a legal hard line; re-classify as HARD"
- ✗ Post-injection journal written but no note about Phase 12 re-solve — "the LP plan must re-run; name that Phase 12 is next and that the plan file must change"
- ✗ `/allocate/constraints` POSTed before your approval — "please revert; approval is my call per rule"
- ✗ A constraint called "hard" without a named regime — "what law, contract clause, or physical fact makes this hard?"

---

## 3. Things you might not understand in this phase

_(v1 — if a concept you struggled with isn't here, flag it back to the author)_

- **Hard vs soft constraints** — the binary that determines whether the solver can ever cross the boundary (never, for hard) or can cross it at a cost (for soft)
- **Penalty calibration** — choosing the dollar penalty for a soft constraint so the solver actually trades off violation against objective gain, rather than ignoring the constraint or never violating it
- **Constraint demotion** — downgrading a hard constraint to soft (with a large penalty) when the all-hard problem is infeasible; a product decision, not a solver fix
- **PDPA hard-line classification** — why under-18 browsing data becomes a legal hard constraint (PDPA §13) after the injection fires, and why "soft with a large penalty" is not acceptable as a substitute
- **Regulatory trigger** — the mid-sprint event where a new or clarified legal rule forces you to re-classify a constraint and re-solve; the before/after documentation is the audit trail

---

## 4. Quick reference (30 sec, generic)

### Hard vs soft constraints

Hard: the solver must never violate this boundary. Reason: law, contract, physics. Example: "do not use under-18 browsing data" (law), "do not allocate more inventory than exists" (physics). Soft: the solver prefers not to violate this boundary but can, at a cost. Reason: operational preference. Example: "try to keep per-segment touches under the fatigue cap — but if a campaign is very high-value, over-touching costs $X per extra touch." The distinction is not "how important" but "is there a law or contract or physical fact that makes it absolute?"

> **Deeper treatment:** [appendix/07-governance/hard-vs-soft-constraints.md](./appendix/07-governance/hard-vs-soft-constraints.md)

### Penalty calibration

For a soft constraint, the penalty coefficient in the objective function determines whether the solver ever violates the constraint. If the penalty is too low, the solver ignores the constraint whenever the objective gain is even small. If the penalty is too high, the soft constraint behaves like a hard constraint — nothing is gained by making it soft. Calibration sets the penalty at a level where the solver occasionally violates the constraint in high-value situations but not trivially. Tonight: the per-touch cost ($3 from §2) is the floor for the fatigue-cap penalty, because violating the cap below $3/touch would never be worth it.

> **Deeper treatment:** [appendix/07-governance/hard-vs-soft-constraints.md](./appendix/07-governance/hard-vs-soft-constraints.md)

### Constraint demotion

When every constraint is hard, the solver may find no feasible plan — no solution that satisfies all of them simultaneously. Infeasibility is a product problem: the constraints are mutually exclusive given the budget and data. The fix is to identify one hard constraint that is not actually a legal absolute (it only felt hard), demote it to soft with a large penalty, and re-solve. The penalty must be large enough to make violation rare — but the option to violate must exist. Document the demotion: which constraint, why it was reclassified, what the new penalty is, who approved.

> **Deeper treatment:** [appendix/07-governance/hard-vs-soft-constraints.md](./appendix/07-governance/hard-vs-soft-constraints.md)

### PDPA hard-line classification

PDPA §13 (Singapore Personal Data Protection Act) prohibits processing certain categories of personal data — including browsing data from persons under 18 — for marketing without explicit consent. When the injection fires, the under-18 browsing feature crosses from "operational preference" into a legal absolute. "Soft with a large penalty" is not a substitute: a penalty means the solver will occasionally violate the rule when the revenue gain is high enough. That is precisely what the law prohibits. The re-classification from soft to hard, and the re-solve that follows, are the audit trail that compliance actually happened.

> **Deeper treatment:** [appendix/07-governance/pdpa-basics.md](./appendix/07-governance/pdpa-basics.md)

### Regulatory trigger

A mid-sprint event where a new or clarified legal rule forces a constraint re-classification and a re-solve. Tonight: the PDPA injection fires at ~4:30pm. The trigger produces two journal files — before and after — and forces a re-solve. Both files must be on disk. The plan file must be different. The before/after table is the audit trail. In production, regulatory triggers happen without warning; the discipline of maintaining the before/after documentation is the practice run.

> **Deeper treatment:** [appendix/07-governance/pdpa-basics.md](./appendix/07-governance/pdpa-basics.md)

---

## 5. Ask CC, grounded in our project (2 min)

Paste this if §4 isn't enough. CC will read our codebase and journal and tailor the explanation to Arcadia Retail.

```
You are helping me understand a concept from Metis Week 5, where I am
building an ML system for Arcadia Retail. I'm currently in Playbook
Phase 11 — Constraint Classification.

Read `workspaces/metis/week-05-retail/playbook/phase-11-constraints.md` for
what this phase does, and read `workspaces/metis/week-05-retail/journal/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. PDPA hard-line classification >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current Arcadia state
3. Implications for the decision I'm about to make (or just made) in Phase 11
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

Before moving on:

- [ ] `journal/phase_11_constraints.md` exists: HARD/SOFT per constraint, regime cited for every HARD, penalty shape (not value) for every SOFT
- [ ] $3 touch cost and $220 PDPA exposure quoted verbatim from `PRODUCT_BRIEF.md §2`
- [ ] You approved each classification before `/allocate/constraints` was POSTed
- [ ] If PDPA injection has fired: `journal/phase_11_postpdpa.md` also exists with PDPA re-classified as HARD and a before/after table
- [ ] If PDPA injection has fired: explicit note present that Phase 12 must re-solve and `data/allocator_last_plan.json` must change

**Next file:** [`phase-12-acceptance.md`](./phase-12-acceptance.md)

Phase 12 runs the solver, checks feasibility and pathologies, and produces your ACCEPT / RE-TUNE / FALL-BACK / REDESIGN disposition. If the PDPA injection has already fired, you will run Phase 12 twice — first-pass and post-injection — before moving on.
