<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 1 — Frame

> **What this phase does:** Pin down exactly what content is in scope, over what window, how many auto-decisions per minute the system can sustain, and what it costs when the answer is wrong — in writing, before any code runs.
> **Why it exists:** Every later phase anchors to these numbers. Fuzzy framing produces statistically brilliant moderators that Legal Counsel silently rejects.
> **You're here because:** Sprint 1 just booted (you came from `workflow-03-sprint-1-vision-boot.md`). Next is Phase 2 — Data Audit.
> **Key concepts you'll see:** scope, throughput ceiling, cost asymmetry, horizon, inheritance framing

---

## 1. Paste this into Claude Code

**Universal core:**

```
I'm entering Playbook Phase 1 — Frame. My decision here is the written
frame for this sprint's model — target, population, horizon, throughput
ceiling, and the cost asymmetry in dollars that every later phase will
anchor to.

Draft the frame for me to edit. Produce these pieces, in order:

1. Target — one sentence naming WHAT is predicted/classified, the unit
   (per post, per image, per caption), and the window in seconds or hours
   (moderation latency matters).
2. Population — inclusions AND explicit exclusions (test posts, internal
   accounts, system-generated content, posts already auto-removed).
3. Horizon — named in seconds or hours, not "fast".
4. Primary cost term AND secondary cost term. Quote both from
   PRODUCT_BRIEF.md §2 verbatim; do not invent numbers.
5. Throughput ceiling — how many posts per minute can the auto-decision
   layer handle before the queue overflows, and WHO owns the ceiling
   (a role, not "the team").

Then show the dollar exposure per day at a plausible mis-classification
rate, using only sourced numbers.

Do NOT propose values for thresholds, fusion architecture, or the
auto-remove ceiling — those are my calls.
Do NOT use "blocker" without naming a specific next step I cannot take.

When the journal file has the five items drafted and the arithmetic
shown, stop and wait for my review.
```

**Tonight-specific additions** (Week 6 MosaicHub):

```
Sprint context: Sprint 1 Vision/CNN — image moderator (5 classes).
Cost source: PRODUCT_BRIEF.md §2. The two cost terms for Sprint 1 are
  - false-negative cost ($320 per piece — harmful left up)
  - false-positive cost ($15 per piece — legitimate auto-removed)
Quote BOTH lines verbatim.
Journal file: copy journal/skeletons/phase_1_frame.md into
  workspaces/metis/week-06-media/journal/phase_1_frame.md and fill in
  as we go. Leave blanks where I still own the call.
Dollar-exposure arithmetic: at 600,000 image-bearing posts/day and a
  plausible per-class FN/FP rate, show daily dollar exposure using only
  numbers from PRODUCT_BRIEF.md §2.
Scaffold commitment to acknowledge: ResNet-50 frozen + 5-class head is
  pre-trained; you are NOT deciding architecture here (that's Phase 5).
The IMDA $1M ceiling on csam_adjacent is a SEPARATE structural cost,
  not the cost-balanced FN/FP arithmetic. Acknowledge it as a hard floor
  in the Phase 1 frame, but don't fold it into the cost-balanced math.
```

**How to paste:** Combine both blocks into a single paste.

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ `journal/phase_1_frame.md` exists with items 1–5 drafted
- ✓ Two verbatim quoted lines from `PRODUCT_BRIEF.md §2` ($320 FN, $15 FP)
- ✓ Plain-language daily dollar-exposure arithmetic using only sourced numbers
- ✓ Throughput ceiling named WITH a role owner ("Reviewer Ops Lead owns the X-posts/min ceiling")
- ✓ Stop signal pending review
- ✓ Viewer: no new artefact — Frame is journal-only

**Signals of drift — push back if you see:**

- ✗ A dollar figure without a quoted brief line — ask "which row of §2?"
- ✗ A target like "moderate harmful content" — rewrite as "5-class score per image with auto-decision under N seconds"
- ✗ Ceiling without a role owner — ask "who owns it?"
- ✗ Horizon as "fast" or "real-time" — ask for seconds or hours
- ✗ A proposed threshold value — Phase 6 owns thresholds

---

## 3. Things you might not understand in this phase

- **Scope** — what counts and what doesn't, stated explicitly with exclusions
- **Throughput ceiling** — posts/minute the auto-decision layer can sustain before overflow
- **Cost asymmetry** — the 21:1 FN-vs-FP imbalance that drives every threshold downstream
- **Horizon** — the latency window in seconds (60s for CSAM-adjacent under IMDA, otherwise hours)
- **Inheritance framing** — naming what the scaffold already fixed vs what remains your call

---

## 4. Quick reference (30 sec, generic)

### Scope

Who counts and who doesn't, stated explicitly. "All posts" is not a scope. "Posts in image+text format from active human accounts in the SG/MY/ID/PH/TH region, excluding internal test accounts and system-generated reposts" is. Scope is a LIST OF EXCLUSIONS as much as inclusions — the things you deliberately left out signal how carefully you framed the problem. A fuzzy scope means every later phase fails gracefully in your journal and catastrophically in production.

> **Deeper treatment:** [appendix/01-framing/target-and-population.md](./appendix/01-framing/target-and-population.md)

### Throughput ceiling

The cap on how many posts/minute the auto-decision layer can sustain before queue depth grows monotonically. Named WITH a role owner ("Reviewer Ops Lead owns the X-posts/min ceiling"), because an unowned ceiling evaporates under traffic surge. If your CNN takes 50ms per image and you have one GPU, throughput is 1,200 posts/min. Above that, queue grows. The ceiling caps Phase 6 threshold-tightness: tighter thresholds = more posts to human review = queue cost.

> **Deeper treatment:** [appendix/01-framing/horizon-and-ceiling.md](./appendix/01-framing/horizon-and-ceiling.md)

### Cost asymmetry

The cost of being wrong in one direction vs the other, with dollar units attached. "FN $320 / FP $15 = 21:1" — stated up front. Without asymmetry, threshold decisions later (Phase 6) have no anchor and default to 0.5. With asymmetry, threshold becomes arithmetic minimising (FN cost × FN rate + FP cost × FP rate) at each threshold. The IMDA $1M ceiling on CSAM-adjacent is a SEPARATE structural cost, not part of the cost-balanced asymmetry — it forces a hard regulatory floor.

> **Deeper treatment:** [appendix/01-framing/cost-asymmetry.md](./appendix/01-framing/cost-asymmetry.md)

### Horizon

The latency window over which the auto-decision is meaningful, named in UNITS (seconds, hours). "Fast moderation" is not a horizon. "60-second auto-decision for CSAM-adjacent (IMDA-mandated), 90-minute SLA for human-review queue, hourly batch for bulk reposts" is. Horizon interacts with throughput: a 60s horizon at 600k images/day means at least 7 GPUs running constantly.

> **Deeper treatment:** [appendix/01-framing/horizon-and-ceiling.md](./appendix/01-framing/horizon-and-ceiling.md)

### Inheritance framing

Framing a sprint when the scaffold already committed to things. You are NOT starting from zero — name what's already fixed (ResNet-50 frozen, BERT-base, early-fusion default, 80k labelled posts, drift refs registered) and separate from what's still your call (per-class thresholds, fusion arch, retrain rules). Inheritance framing is the default in industry.

> **Deeper treatment:** [appendix/01-framing/inheritance-vs-greenfield.md](./appendix/01-framing/inheritance-vs-greenfield.md)

---

## 5. Ask CC, grounded in our project (2 min)

```
You are helping me understand a concept from Metis Week 6 Phase 1.

Read `workspaces/metis/week-06-media/playbook/phase-01-frame.md` and
`workspaces/metis/week-06-media/journal/phase_1_frame.md`.

Explain "<<< FILL IN: concept name >>>" — plain language, MosaicHub-grounded,
implications for my Phase 1 decision, what to push back on. Under 400 words.
```

---

## 6. Gate / next

- [ ] `journal/phase_1_frame.md` has items 1–5 drafted
- [ ] Both cost terms quoted verbatim from `PRODUCT_BRIEF.md §2`
- [ ] Daily dollar-exposure arithmetic shown using only sourced numbers
- [ ] Throughput ceiling named WITH a role owner
- [ ] No proposed thresholds; no "blocker" without a named next step

**Next file:** [`phase-02-data-audit.md`](./phase-02-data-audit.md)
