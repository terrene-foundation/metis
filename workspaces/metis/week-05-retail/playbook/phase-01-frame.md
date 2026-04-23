<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 1 — Frame

> **What this phase does:** Pin down exactly who is in scope, over what window, how many outputs the business can act on, and what it costs when the answer is wrong — in writing, before any code runs.
> **Why it exists:** Every later phase anchors to these numbers. Fuzzy framing produces statistically brilliant models that marketing silently ignores.
> **You're here because:** Sprint 1 just booted (you came from `workflow-03-sprint-1-usml-boot.md`). Next is Phase 2 — Data Audit.
> **Key concepts you'll see:** scope, operational ceiling, cost asymmetry, horizon, inheritance framing

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm entering Playbook Phase 1 — Frame. My decision here is the written
frame for this sprint's model — target, population, horizon, operational
ceiling, and the cost asymmetry in dollars that every later phase will
anchor to.

Draft the frame for me to edit. Produce these pieces, in order:

1. Target — one sentence naming WHAT is predicted/discovered, the unit
   (per customer, per session, per order), and the window in days or months.
2. Population — inclusions AND explicit exclusions (staff accounts, bot
   accounts, test accounts, low-signal users).
3. Horizon — named in days or months, not "near-term".
4. Primary cost term AND secondary cost term. Quote both from the
   project's cost source verbatim; do not invent numbers.
5. Operational ceiling — how many outputs can the downstream team act on
   in parallel, and WHO owns that ceiling (a role, not "the team").

Then show the dollar exposure per time period at a plausible
mis-classification rate, using only sourced numbers.

Do NOT propose values for target, K, or ceiling — those are my calls.
Do NOT use "blocker" without naming a specific next step I cannot take.

When the journal file has the five items drafted and the arithmetic
shown, stop and wait for my review.
```

**Tonight-specific additions** (Week 5 Arcadia Retail):

```
Sprint context: Sprint 1 USML — customer segmentation.
Cost source: PRODUCT_BRIEF.md §2. The two cost terms for Sprint 1 are
  - wrong-segment campaign cost ($45 per customer)
  - per-customer touch cost ($3)
Quote BOTH lines verbatim.
Journal file: copy journal/skeletons/phase_1_frame.md into
  workspaces/metis/week-05-retail/journal/phase_1_frame.md and fill in
  as we go. Leave blanks where I still own the call.
Dollar-exposure arithmetic: at 18,000 active customers and a plausible
  monthly misclassification rate, show dollar exposure per month using
  only numbers from PRODUCT_BRIEF.md §2.
Scaffold commitment to acknowledge: baseline K=3 is pre-trained; you
  are NOT deciding K here (that's Phase 6 USML).
```

**How to paste:** Combine both blocks into a single paste.

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ `journal/phase_1_frame.md` exists and has items 1–5 drafted, with blanks where YOU still own the call
- ✓ Two verbatim quoted lines from `PRODUCT_BRIEF.md §2` (for $45 wrong-segment and $3 per touch)
- ✓ A plain-language dollar-exposure arithmetic using only sourced numbers (e.g. `$45 × 18,000 × 5% = $40,500/month`)
- ✓ Operational ceiling named WITH a role owner (e.g. "CMO owns the 6-segment ceiling")
- ✓ A stop signal waiting for your review
- ✓ Viewer (http://localhost:3000): no new rendered artifact — Frame is journal-only; confirm `journal/phase_1_frame.md` exists in the file tree

**Signals of drift — push back if you see:**

- ✗ A dollar figure without a quoted brief line ("which row of §2 is this from?")
- ✗ A target like "discover patterns" or "understand customers" (rewrite in the form "behavioural segment per active customer over N-month window")
- ✗ An operational ceiling without a role owner ("who owns the ceiling — CMO, CX Lead, agency? Name the role.")
- ✗ A horizon phrased as "near-term" or "recent" ("please express horizon in days or months")
- ✗ A proposed K anywhere ("K is Phase 6's call — please remove")

---

## 3. Things you might not understand in this phase

_(v1 — if a concept you struggled with isn't here, flag it back to the author)_

- **Scope** — what exactly "in scope" means, and why exclusions matter as much as inclusions
- **Operational ceiling** — the real-world cap on how many outputs your downstream team can act on in parallel
- **Cost asymmetry** — the fact that the two ways of being wrong rarely cost the same
- **Horizon** — the time window the model is trained to predict over, named in units (days, months)
- **Inheritance framing** — how to frame a sprint when the scaffold already committed to things before you arrived

---

## 4. Quick reference (30 sec, generic)

### Scope

Who counts and who doesn't, stated explicitly. "All customers" is not a scope. "18,000 active customers in last 90 days, excluding staff and bot accounts" is. Scope is a LIST OF EXCLUSIONS as much as inclusions — the things you deliberately left out signal how carefully you framed the problem. A fuzzy scope means every later phase fails gracefully in your journal and catastrophically in production.

> **Deeper treatment:** [appendix/01-framing/target-and-population.md](./appendix/01-framing/target-and-population.md)

### Operational ceiling

How many distinct outputs your downstream team can actually act on in parallel. A 4-person marketing team cannot run 12 segment-specific campaigns — so the ceiling caps model complexity. Always named WITH a role owner ("CMO owns the 6-segment ceiling"), because an unowned ceiling evaporates under quarterly planning pressure. The ceiling is the single most effective anti-over-engineering constraint a commissioner can set.

> **Deeper treatment:** [appendix/01-framing/horizon-and-ceiling.md](./appendix/01-framing/horizon-and-ceiling.md)

### Cost asymmetry

The cost of being wrong in one direction vs the other, with dollar units attached. "False alarms cost $X, missed events cost $Y" — stated up front. Without asymmetry, threshold decisions later (Phase 6) have no anchor and default to 0.5 (the silent killer). With asymmetry, threshold becomes arithmetic. Tonight: wrong-segment $45, per-touch $3 — a ~15:1 ratio.

> **Deeper treatment:** [appendix/01-framing/cost-asymmetry.md](./appendix/01-framing/cost-asymmetry.md)

### Horizon

The window over which the model's prediction is meaningful, named in UNITS (days, months) — never in vibes ("near-term", "recent"). "Forecast demand" is not a horizon. "Forecast demand per SKU per day for the next 14 days" is. Horizon choice interacts with seasonality: an 18-month horizon trained on Arcadia data will average across Black Friday, which silently breaks in production.

> **Deeper treatment:** [appendix/01-framing/horizon-and-ceiling.md](./appendix/01-framing/horizon-and-ceiling.md)

### Inheritance framing

Framing a sprint when the scaffold already committed to things before you arrived. You are NOT starting from zero — you are naming what's already fixed (baseline K=3, three-family classifier sweep, cost source = PRODUCT_BRIEF.md §2) and separating it from what's still your call (final K, segment names, per-segment actions, thresholds). Inheritance framing is the default in industry — greenfield is the exception. Get comfortable with it.

> **Deeper treatment:** [appendix/01-framing/inheritance-vs-greenfield.md](./appendix/01-framing/inheritance-vs-greenfield.md)

---

## 5. Ask CC, grounded in our project (2 min)

Paste this if §4 isn't enough. CC will read our codebase and journal and tailor the explanation to Arcadia Retail.

```
You are helping me understand a concept from Metis Week 5, where I am
building an ML system for Arcadia Retail. I'm currently in Playbook
Phase 1 — Frame.

Read `workspaces/metis/week-05-retail/playbook/phase-01-frame.md` for
what this phase does, and read `workspaces/metis/week-05-retail/journal/`
for the current state of our work.

Explain "<<< FILL IN: concept name, e.g. operational ceiling >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current Arcadia state
3. Implications for the decision I'm about to make (or just made) in Phase 1
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

Before moving on:

- [ ] `journal/phase_1_frame.md` exists with items 1–5 drafted
- [ ] Both cost terms quoted verbatim from `PRODUCT_BRIEF.md §2`
- [ ] Dollar-exposure arithmetic shown using only sourced numbers
- [ ] Operational ceiling named WITH a role owner
- [ ] No proposed K, no "blocker" without a named next step

**Next file:** [`phase-02-data-audit.md`](./phase-02-data-audit.md)
