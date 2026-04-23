<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
-->

_[← Playbook index (README)](./README.md)_

## Phase 1 — Frame

```
──────────────────────────────────────────────────────────────────
 VALUE CHAIN:   Analyze ▸ Todos ▸ **USML ◉** ▸ SML ▸ Opt ▸ MLOps ▸ Close
 THIS PHASE:    Sprint 1 · Phase 1 of 8 — Frame
 LEVERS:        scope · horizon · operational ceiling · cost asymmetry
──────────────────────────────────────────────────────────────────
```

### Concept

Declaring — in writing, before any code runs — exactly who is in scope, over what window, how many outputs the business can act on, and what it costs when the answer is wrong. Frame is the single sentence the whole downstream stack gets built on. If Frame is fuzzy, every later phase fails gracefully in your journal and catastrophically in production.

### Why it matters (SML lens)

- Reinforces Week 2 healthcare: "predict readmission" only became useful once scope narrowed to "patients discharged to home within 30 days of an inpatient stay."
- Reinforces Week 3 fraud: cost asymmetry ($40 missed-fraud vs $1 false-alarm) only meant something once volume was attached.
- Reinforces Week 4 forecasting: horizon has to be named in days — "forecast demand" is not a target; "forecast orders per depot per day for the next 14 days" is.
- The dollar cost of being wrong is the anchor every later phase refers back to. No anchor, no grounding.

### Why it matters (USML lens)

- With no label, there is no "accuracy" to fall back on if scope is fuzzy — a bad scope makes every segment unactionable and you won't notice until campaigns ship.
- You must commit to an **operational ceiling** BEFORE the data speaks. _"Marketing can run at most 6 parallel campaigns"_ — declared now, enforced in Phase 6. Waiting until after the elbow plot is how you end up with K=12 and a paralysed marketing team.
- The cost of wrongness has two faces in USML: the wrong-cohort cost AND the cost of touching them at all. SML usually has one cost per direction; USML has two because you're both choosing a cohort AND deciding to contact it.
- Peak seasonality changes the wrong-cohort math — the same 5% misclassification rate costs double when volume doubles.

### Your levers this phase — what to pull, what to ignore

- **Lever 1 (the big one): scope.** Inclusions AND explicit exclusions. "18,000 active customers in last 90 days, excluding staff + bot accounts" is a scope. "All customers" is not. Pulled by telling Claude Code what counts and what doesn't.
- **Lever 2 (usually matters): operational ceiling.** How many outputs can your business _act on_? The answer caps model complexity. A 4-person marketing team cannot run 12 segments.
- **Lever 3 (the anchor): cost asymmetry in dollars.** Two directions, two numbers, with units. "$40 per missed event, $12 per false alarm" lets every later phase do math.
- **Lever 4 (rarely adjusted): horizon.** Days, not "near-term." Forces precision.
- **Skip unless specific:** population segmentation at this phase (that's Sprint 1's output, not its input); peak-season adjustments (Phase 13's problem).

### Trust-plane question

What is the target, the population, the horizon, the cost of being wrong?

### Paste this

```
I'm entering Playbook Phase 1 — Frame. The scaffold pre-committed to the
product (retail intelligence suite) and the sprint structure (USML →
SML → Opt → MLOps); my decision here is the written frame for Sprint 1
segmentation — target, population, horizon, operational ceiling, and
the cost asymmetry in dollars that every later phase will anchor to.

Copy journal/skeletons/phase_1_frame.md into
workspaces/metis/week-05-retail/journal/phase_1_frame.md and fill in
the blanks as we go. Leave fields I have not decided yet as TODO — do
NOT propose values for me.

Draft the frame for me to edit. Produce these pieces, in order:

1. Target — one sentence naming WHAT is predicted/discovered, the unit
   (per customer, per session), and the window in days or months.
2. Population — inclusions AND explicit exclusions (staff accounts,
   bot accounts, test accounts, customers with <3 transactions).
3. Horizon — named in days or months, not "near-term".
4. Primary cost term AND secondary cost term. The two retail cost
   terms that anchor Sprint 1 are the wrong-segment campaign cost
   and the per-customer touch cost. Quote BOTH lines verbatim from
   PRODUCT_BRIEF.md §2 — the row and the exact dollar value. If you
   cannot find the line, say so; do NOT invent a number.
5. Operational ceiling — how many segments marketing can actually run
   in parallel, and WHO owns that ceiling (a role, not "the team").

Then answer one framing question in plain language: at a plausible
monthly mis-segmentation volume, what is the dollar exposure per
month if we ship the wrong K? Show the arithmetic using only numbers
from PRODUCT_BRIEF.md §2 — no invented counts.

Do NOT use the word "blocker" without naming the specific next step
I cannot take. Fuzzy scope is not a blocker; it's a to-do for me.

When the journal file has the five items drafted and the arithmetic
shown, stop and wait for me to review.
```

### Why this prompt is written this way

- Inheritance-framed opening names what the scaffold committed to (product + sprint order) and what remains my call (the written frame) — protects against agent drift into greenfield framing.
- Show-the-brief is mandatory on the two cost terms ($45 wrong-segment, $3 touch) because the cost anchor carries through every later phase — a Phase 1 without a quoted brief line is a 1/4 on rubric D1.
- Forbidding value proposals on target, K, and ceiling keeps the agent as a drafter, not a decider — the Trust Plane stays with me.
- The "dollar exposure per month" arithmetic is required BEFORE Phase 4 so the ceiling and cost asymmetry graduate from words to a number the CMO would recognize.
- No-fake-blockers guard is one line because Phase 1 has no real blockers — only fuzzy scope, which is a drafting task.

### What to expect back

- `journal/phase_1_frame.md` filled in for items 1–5 with blanks only where I still own the call.
- Two verbatim quoted lines from `PRODUCT_BRIEF.md §2` — one for wrong-segment ($45), one for per-customer touch ($3).
- A plain-language dollar-exposure arithmetic line (count × rate) using only brief-sourced numbers.
- A one-sentence named operational ceiling with a role attached (e.g. "CMO owns the campaign-count ceiling").
- A stop signal pending my review.

### Push back if you see

- A dollar figure with no quoted brief line — "which row of `PRODUCT_BRIEF.md §2` is this from? paste the row."
- A target like "discover patterns" or "understand customers" — "please rewrite in the form 'behavioural segment per active customer over an N-month window'."
- An operational ceiling without a role owner — "who owns the ceiling? the CMO, the CX Lead, the agency? name the role."
- A horizon phrased as "near-term" or "recent" — "please express horizon in days or months."
- A proposed K anywhere in the frame — "please remove the K; that's Phase 6's decision, not Phase 1's."

### Adapt for your next domain

- Change `wrong-segment campaign cost ($45)` to your domain's primary cost term.
- Change `per-customer touch cost ($3)` to the secondary / operational cost.
- Change `marketing ceiling on parallel campaigns` to the ceiling your ops team owns.
- Change `active customers in last 90 days` to your scope — inclusions and exclusions.
- Change `PRODUCT_BRIEF.md §2` to the brief section that holds your cost table.

### Evaluation checklist

- [ ] Target / output precise (not "segments" but "behavioural segments over 90-day window, at most 6, distinct marketing action per segment").
- [ ] Population scope explicit — inclusions AND exclusions.
- [ ] Horizon / window named in units (days, months).
- [ ] Cost asymmetry quantified with dollars and units attached.
- [ ] Operational ceiling declared and sourced (who owns it?).

### Journal schema — universal

```
Phase 1 — Frame
Target / output: ____
Population: ____ (inclusions: ____; exclusions: ____)
Horizon / window: ____
Primary cost term: $__ per ____ (the side that loses more)
Secondary cost term: $__ per ____
Operational ceiling: ____ (owned by ____)
What would flip my mind: ____
```

> **Retail instantiation:** Target = "behavioural segment per active customer, max 6 segments"; Population = "18,000 customers active in last 90 days, excl. staff/bots"; Horizon = "6-month rolling"; Primary cost = $45 per wrong-segment campaign; Secondary = $3 per touch; Ceiling = 6 (owned by CMO); Flip = "if marketing restructures to run >6 campaigns".

### Common failure modes

- Target drifts into fuzzy language ("discover patterns") — downstream phases lose grounding.
- Horizon left implicit — the model learns behaviour across seasons that should not be averaged.
- Cost asymmetry stated as "X:Y ratio" without dollars — scores 2/4 on rubric D1.
- Operational ceiling omitted — student ends up with a statistically brilliant K=12 that marketing silently ignores.

### Artefact

`workspaces/.../journal/phase_1_frame.md`

### Instructor pause point

- Write the Sprint 1 frame on the whiteboard. Ask the class: which three numbers would change if Arcadia were a 2,000-customer boutique? Which would change if it were Lazada?
- Ask: what's the smallest operational ceiling that still ships a useful product? Why isn't "premium vs mass" always the right answer?
- Demonstrate: show $45 × 18,000 × 5% = $40,500/month on the board. Ask: does the CMO care at this number? What number flips her from "nice to have" to "must ship"?

### Transfer to your next project

1. Who is explicitly in scope and who is explicitly OUT? (Scope is a list of exclusions, not just inclusions.)
2. What is the operational ceiling on how many outputs your business can act on — and who, not the model, owns that ceiling?
3. What does it cost, in dollars, when a single unit is wrong — and is there a volume that turns that unit cost into a monthly number your executive will care about?

---

