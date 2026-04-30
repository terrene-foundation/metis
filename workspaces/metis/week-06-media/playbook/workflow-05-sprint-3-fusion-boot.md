<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Workflow 5 — Sprint 3 Fusion Boot (multi-modal + queue allocator)

> **What this step does:** Boot Sprint 3 by copying skeleton journal files for the multi-modal fusion + reviewer queue allocator, confirming endpoints, and orienting on the IMDA injection that fires mid-sprint.
> **Why it exists:** Sprint 3 is two products in one — the fusion moderator (catches cross-modal harm) AND the queue allocator (LP that routes uncertain cases to humans). The IMDA injection at ~4:30 forces re-classification AND re-solve. Booting cleanly means you don't lose 15 minutes when the injection fires.
> **You're here because:** Sprint 2 Text wrapped (Phase 8 gate signed for the text moderator) and Sprint 3 is the fusion + queue.
> **Key concepts you'll see:** multi-modal fusion, joint embedding, LP queue allocator, IMDA injection, hard vs soft constraint

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm entering Sprint 3 — multi-modal fusion + reviewer queue allocator. This
sprint is two products in one. The fusion moderator catches cross-modal
harm (image-safe + text-safe but joint-meaning harmful). The queue allocator
solves a linear program that routes uncertain cases to human reviewers under
SLA + budget constraints. Phases 10, 11, 12 fire on the queue allocator,
not on the fusion moderator's classification head.

Before I start the phase walk, I need you to:

1. Copy the Sprint 3 skeletons from journal/skeletons/ into journal/.
   These cover phase_10_objective.md, phase_11_constraints.md,
   phase_12_accept.md, plus the post-injection variants
   phase_11_postimda.md and phase_12_postimda.md.

2. Confirm the fusion + queue endpoints are live by GET requests.

3. State, in writing: which phases drive the fusion ARCHITECTURE choice
   (Phase 5 multi-modal pass) vs which phases drive the QUEUE ALLOCATOR
   (Phases 10, 11, 12). Confusing the two is the #1 trap of this sprint.

4. State, in writing: when the IMDA injection fires (~4:30pm), what
   re-classification is required (Phase 11) AND what re-solve is required
   (Phase 12). Missing the Phase 12 re-solve is the most common D3
   (trade-off honesty) failure.

5. Do NOT propose objective weights or constraint penalties. Those are
   my pre-registration calls in phase_10_objective.md and
   phase_11_constraints.md.

6. Do NOT use the word "blocker" without naming a specific action.

Once skeletons are copied and endpoints confirmed live, summarise: (a) the
fusion architecture trade-off (early / late / joint-embedding), (b) the
queue allocator's LP shape (decision variables + constraint families + the
$22/min reviewer cost), (c) the IMDA injection mechanics. Then stop.
```

**Tonight-specific additions** (Week 6 MosaicHub):

```
Sprint: Sprint 3 Fusion + Queue.
Phases covered: 10 (objective), 11 (constraints), 12 (acceptance) —
plus the post-IMDA re-runs of 11 and 12.

Skeleton copy: copy phase_{10,11,12}_*.md skeletons (including the _postimda
variants) into workspaces/metis/week-06-media/journal/.

Endpoint checks (GET only):
- /moderate/fusion/score → returns cross_modal_harm_score on a sample post
- /moderate/fusion/architecture → current mode (early / late / joint)
- /queue/objective → current objective weights (if any pre-set)
- /queue/constraints → current constraint set
If any is not live, STOP and raise a hand.

Fusion architecture trade-off (NAME, do NOT pick — Phase 5 multi-modal
owns the pick):
- early-fusion: concatenate image + text features before classification head;
  cheap, brittle on adversarial cases.
- late-fusion: per-modality scores + meta-classifier; modular, slower to
  retrain.
- joint-embedding (CLIP-style): image encoder + text encoder + alignment
  head; most accurate on cross-modal harm, ~3× compute.

Queue allocator LP shape:
- Decision variables: x[post, queue_tier] = number of posts of this tier
  routed to reviewer queue
- Objective: minimise (FN cost × expected FN at tier + FP cost × expected
  FP at tier + reviewer_minutes × $22 + GPU_inference × $0.03/1k)
- Constraints (the Phase 11 classification call): reviewer headcount cap
  (HARD — physics), SLA window of 90 minutes (SOFT — penalty per minute
  late), CSAM-adjacent must-route-to-human within 60 seconds (HARD AFTER
  IMDA injection — soft before).

IMDA injection mechanics (~4:30pm):
- Trigger: instructor fires src/media/scripts/scenario_inject.py
  imda_csam_mandate
- Effect: writes data/scenarios/imda_csam_mandate.json marker
- Required Phase 11 re-classification: CSAM-adjacent threshold from
  cost-balanced (e.g. 0.85) to HARD (regulator floor; we used 0.40 in the
  example tonight — confirm your floor against the IMDA mandate file).
  Mandatory-route-to-human within 60 seconds becomes a HARD constraint.
- Required Phase 12 re-solve: re-run /queue/solve with the new constraint
  set; quantify the queue-cost shadow price (compliance cost in $ of
  reviewer-time).
- Files to write: phase_11_postimda.md (re-classification with rationale)
  AND phase_12_postimda.md (re-solve with quantified compliance cost).
  Skipping the Phase 12 re-write is the most common D3 zero in this sprint.

After the summary, stop and wait for my Phase 10 prompt.
```

**How to paste:** Combine both blocks into a single paste.

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ Skeleton files copied: `phase_10_objective.md`, `phase_11_constraints.md`, `phase_12_accept.md`, `phase_11_postimda.md`, `phase_12_postimda.md`
- ✓ All four endpoints (`/moderate/fusion/score`, `/moderate/fusion/architecture`, `/queue/objective`, `/queue/constraints`) returned 200
- ✓ Summary names the three fusion architectures with their cost / accuracy trade-offs
- ✓ Summary names the LP decision variables, objective, and constraint families
- ✓ IMDA injection mechanics named: trigger script, marker file, required Phase 11 re-classification, required Phase 12 re-solve, the four journal files (NOT two)
- ✓ Stop signal pending Phase 10
- ✓ Viewer Sprint 3 tile activates

**Signals of drift — push back if you see:**

- ✗ A proposed objective weight (e.g. "FN cost × 0.7 + reviewer × 0.3") — ask to remove
- ✗ The IMDA injection described as "Phase 11 only" — ask "where does the Phase 12 re-solve fit?"
- ✗ Fusion architecture conflated with the queue allocator's LP — ask "Phase 5 picks fusion arch; Phases 10–12 are about the queue. Which one are we in?"
- ✗ A claim that joint-embedding is "obviously best" without compute-cost trade-off — ask "what is the daily $ cost of joint-embedding vs late-fusion at our 600k images/day rate?"

---

## 3. Things you might not understand in this step

- **Multi-modal fusion** — combining image + text signals so the joint meaning is captured (the cute-puppy + "destroy all humans" meme)
- **Joint embedding** — CLIP-style architecture where image + text are encoded into the same space and compared
- **LP queue allocator** — linear program that decides how many posts to route to which reviewer tier under budget + SLA
- **IMDA injection** — mid-Sprint-3 regulatory event that converts the CSAM-adjacent threshold from soft to hard
- **Hard vs soft constraint** — hard = inviolable (physics, law, contract); soft = preferential with a dollar penalty per unit violated

---

## 4. Quick reference (30 sec, generic)

### Multi-modal fusion

A model architecture that combines two or more modalities (image + text + audio) into a single decision. Three families tonight: early-fusion (concatenate features early), late-fusion (per-modality scores + meta-classifier), joint-embedding (CLIP-style — encode each modality into a shared space, then classify jointly). The decision in Phase 5 multi-modal is which to ship, defended in cross-modal coverage gain × dollar value vs compute-cost delta. Joint-embedding wins on coverage but is 3× compute.

> **Deeper treatment:** [appendix/03-modeling/recommender-families.md](./appendix/03-modeling/recommender-families.md)

### Joint embedding

CLIP-style architecture: an image encoder and a text encoder, both trained so an image and its caption end up at similar points in a shared embedding space. The classification head then operates on the joint embedding. Catches cross-modal harm because the joint embedding captures meaning the per-modality encoders miss. Costs more because you need both encoders to fine-tune; benefits when adversaries target the cross-modal seam.

> **Deeper treatment:** [appendix/03-modeling/recommender-families.md](./appendix/03-modeling/recommender-families.md)

### LP queue allocator

A linear program that routes incoming posts to reviewer queues under a budget. Decision variables: how many posts of each tier go to which queue. Objective: minimise expected mis-classification cost + reviewer-minute cost + GPU inference cost. Constraints: reviewer headcount, SLA, IMDA mandates. The LP is solved per-batch (every few minutes); the resulting plan tells the routing layer what to do. Phases 10, 11, 12 each shape one part of the LP — objective weights, constraint classification, acceptance.

> **Deeper treatment:** [appendix/05-deployment/deployment-gate.md](./appendix/05-deployment/deployment-gate.md)

### IMDA injection

A scripted event mid-Sprint-3 (~4:30pm) that simulates a regulator clarification: any post scoring above 0.4 on the CSAM-adjacent class MUST be routed to mandatory human review within 60 seconds AND auto-blurred in the meantime. The injection is the analog to Week 5's PDPA fire. The required response is a Phase 11 re-classification (CSAM-adjacent moves from soft cost-balanced to hard regulator-mandated) AND a Phase 12 re-solve (run /queue/solve with the new constraint, quantify the compliance cost). Two files must result: `phase_11_postimda.md` and `phase_12_postimda.md`.

> **Deeper treatment:** [appendix/07-governance/hard-vs-soft-constraints.md](./appendix/07-governance/hard-vs-soft-constraints.md)

### Hard vs soft constraint

Hard constraints are inviolable: violating them makes the plan invalid. Examples tonight: reviewer headcount (you can't conjure reviewers from nothing), CSAM-adjacent must-route-to-human after IMDA fires (regulator-mandated). Soft constraints are preferences with a dollar penalty per unit violated: SLA window (90 min), per-tier review-time budget. The Phase 11 classification call is the load-bearing decision — mis-classifying soft as hard makes the LP infeasible; mis-classifying hard as soft exposes you to regulator action.

> **Deeper treatment:** [appendix/07-governance/hard-vs-soft-constraints.md](./appendix/07-governance/hard-vs-soft-constraints.md)

---

## 5. Ask CC, grounded in our project (2 min)

```
You are helping me understand a concept from Metis Week 6 Sprint 3 (fusion +
queue), where I am building an ML system for MosaicHub.

Read `workspaces/metis/week-06-media/playbook/workflow-05-sprint-3-fusion-boot.md`
for what this step does, and read `workspaces/metis/week-06-media/journal/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. joint embedding >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current MosaicHub state
3. Implications for the decision I'm about to make (or just made) in Sprint 3
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

- [ ] Five skeleton files copied (`phase_10`, `phase_11`, `phase_12`, `phase_11_postimda`, `phase_12_postimda`)
- [ ] All four fusion + queue endpoints returned 200
- [ ] Summary names the three fusion architectures with cost trade-offs
- [ ] Summary names LP shape (variables + objective + constraint families)
- [ ] IMDA injection mechanics named, including the FOUR journal files
- [ ] Claude Code stopped, waiting for Phase 10 prompt

**Next file:** [`phase-10-objective.md`](./phase-10-objective.md)
