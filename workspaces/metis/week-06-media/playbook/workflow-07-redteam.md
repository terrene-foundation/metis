<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Workflow 7 — /redteam (cross-sprint cascade stress)

> **What this step does:** Stress-test the four-layer cascade end-to-end after all sprints have shipped. Image robustness → text robustness → fusion robustness under each — the cascade either holds or it doesn't.
> **Why it exists:** A robust image moderator is useless if the text moderator above it fails on the same adversarial input. `/redteam` finds where the cascade breaks under coordinated attack.
> **You're here because:** All four sprints completed; Phase 8 gates signed; Phase 13 retrain rules written.
> **Key concepts you'll see:** cascade red-team, adversarial input, distribution shift, blast radius, severity ranking

---

## 1. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm running /redteam on the entire shipped product. The four-layer cascade
(image → text → fusion → drift) must be stressed end-to-end, not per-layer.

Read every Phase 7 journal entry I wrote tonight (one per sprint). Read the
Phase 8 deployment gates. Read the IMDA post-injection Phase 12 entry.

Then, for each of the three AI Verify dimensions in scope tonight
(transparency, robustness, safety — fairness deferred to Week 7):

1. Identify cross-sprint findings — places where one sprint's result
   exposes a vulnerability in another sprint's output. Example: if image
   moderation has 0.62 recall on weapons (Sprint 1), what is the impact
   on the fusion moderator (Sprint 3) when an adversary uploads a weapon
   image with neutral text?

2. Rank by severity, naming for each finding:
   - The blast radius in dollars (use the cost table)
   - The detection cadence (which Phase 13 drift signal would catch it)
   - The mitigation (within tonight's product, not "rebuild from scratch")

3. Write the findings to 04-validate/redteam.md.

Do NOT invent findings. Do NOT use the word "blocker" without specifics.
Do NOT propose values for thresholds I have already pre-registered.

After the file is written, stop. The instructor reviews before /codify.
```

**Tonight-specific additions** (Week 6 MosaicHub):

```
Output file: workspaces/metis/week-06-media/04-validate/redteam.md

Cross-sprint findings to specifically check:

A. Sprint 1 → Sprint 3 (image → fusion):
   - If image moderator recall on weapons is below 0.80, what fusion
     scenarios slip through? Use the fusion holdout (8k multi-modal
     subset) to quantify.
   - If image moderator FP rate on safe is high, what queue load impact?
     Use the $22/min reviewer cost.

B. Sprint 2 → Sprint 3 (text → fusion):
   - If text moderator is miscalibrated on hate-speech (Brier > 0.15),
     what fusion scenarios over-trigger? Quantify in $ of FP cost.
   - Singlish / Malay / code-mixed text — how does the text moderator's
     OOD performance affect fusion's cross-modal-harm score?

C. Sprint 1 + 2 → Sprint 3 fusion blind spots:
   - The cute-puppy + "destroy all humans" canonical case. Confirm fusion
     catches it; if not, what's the FN cost across a year given 100k such
     memes posted?

D. IMDA hard-line robustness:
   - With CSAM-adjacent threshold = 0.40 (HARD), what is the FP load on
     reviewer queue? At $22/min × N false-routes, is the SLA achievable?
   - Adversarial pixels designed to score 0.39 (just under the IMDA floor):
     how vulnerable are we?

E. Sprint 4 → cross-cascade detection:
   - For each Phase 7 robustness finding above, name the Phase 13 drift
     signal that would detect it in production. If no signal catches it,
     that's an MLOps gap — flag it.

Severity-rank all findings; for each, name blast-radius in $, detection
cadence (image weekly / text daily / fusion per-incident), and mitigation.

After /redteam.md is written, stop and wait for /codify.
```

**How to paste:** Combine both blocks into a single paste.

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ `04-validate/redteam.md` exists with at least 8 findings, severity-ranked
- ✓ Each finding names blast-radius in $, detection cadence, mitigation
- ✓ At least one cross-sprint finding (image → fusion or text → fusion or fusion → queue)
- ✓ IMDA hard-line robustness checked (FP load + adversarial-just-under-floor)
- ✓ Each robustness finding mapped to a Phase 13 detection signal (or flagged as MLOps gap)
- ✓ Stop signal pending `/codify`

**Signals of drift — push back if you see:**

- ✗ Findings that don't cite blast-radius in $ — ask "which line of `PRODUCT_BRIEF.md` §2 grounds the dollar amount?"
- ✗ Per-sprint findings only (no cross-sprint) — ask "what's the cascade impact? A robust image alone is useless if the fusion moderator above it fails on the same input."
- ✗ A finding without a detection signal — ask "if this fires in production, which Phase 13 signal catches it? If none, that's an MLOps gap to flag."
- ✗ "Rebuild from scratch" as a mitigation — ask "what's a mitigation we can ship tonight, within the existing scaffold?"
- ✗ Inventing findings (no source data) — ask "which holdout, which post_id, which file proves this?"

---

## 3. Things you might not understand in this step

- **Cascade red-team** — stressing the chain end-to-end, not per-layer
- **Blast radius** — how many users, $ exposure, regulator visibility a failure produces
- **Severity ranking** — ordering findings by (probability × blast radius), not by how scary they sound
- **Detection cadence** — how fast a Phase 13 drift signal would catch the failure in production
- **Mitigation** — a fix shippable tonight, within the scaffold, not a future research project

---

## 4. Quick reference (30 sec, generic)

### Cascade red-team

Stress-testing the chain end-to-end rather than per-layer. Each individual model can be robust on its own holdout while the joint cascade fails on a coordinated input. The canonical case: image moderator says "safe" (0.91 confidence), text moderator says "harmless joke" (0.88 confidence), fusion moderator either catches the cross-modal harm or misses it. If fusion misses, the cascade fails despite both upstream models scoring high. Cascade red-team finds these joint failures.

> **Deeper treatment:** [appendix/03-modeling/recommender-families.md](./appendix/03-modeling/recommender-families.md)

### Blast radius

The size and visibility of a failure. Three components: how many users see it, how much $ it costs (FN × $320, FP × $15, IMDA × $1M), how visible it is to regulators (private user complaint vs IMDA takedown directive vs CEO-level escalation). A finding with a large blast radius and a clear detection signal warrants immediate attention; a finding with a small blast radius and no detection is a future-task.

> **Deeper treatment:** [appendix/07-governance/hitl-patterns.md](./appendix/07-governance/hitl-patterns.md)

### Severity ranking

Ordering findings by (probability × blast radius), not by how scary they sound or how much effort they took to discover. A finding that costs $50/year in expected FN cost is lower severity than one that costs $5M/year, even if the second is rarer. Severity ranking forces you to allocate mitigation effort against actual risk, not against how loudly the finding presents.

> **Deeper treatment:** [appendix/07-governance/hitl-patterns.md](./appendix/07-governance/hitl-patterns.md)

### Detection cadence

How fast a Phase 13 drift signal would surface the failure in production. Image weekly, text daily, fusion per-incident. A finding with no detection cadence is silent — it can run for months before anyone notices. A finding with detection at the right cadence is bounded — a regression can run for at most one window before alerting.

> **Deeper treatment:** [appendix/06-monitoring/drift-types.md](./appendix/06-monitoring/drift-types.md)

### Mitigation

A fix shippable tonight, within the scaffold. "Retrain with more data" is a mitigation if the data is on hand. "Add a new model architecture" is a research project, not a mitigation. The Phase 8 deployment gates committed to specific monitoring; mitigations that fall within those monitors are shippable, those that don't are research.

> **Deeper treatment:** [appendix/05-deployment/deployment-gate.md](./appendix/05-deployment/deployment-gate.md)

---

## 5. Ask CC, grounded in our project (2 min)

```
You are helping me understand a concept from Metis Week 6 /redteam, where I
am stress-testing the MosaicHub moderation cascade end-to-end.

Read `workspaces/metis/week-06-media/playbook/workflow-07-redteam.md` for
what this step does, and read `workspaces/metis/week-06-media/journal/` and
`workspaces/metis/week-06-media/04-validate/redteam.md` for the current state.

Explain "<<< FILL IN: concept name, e.g. cascade red-team >>>" to me:

1. In plain language (I code but haven't studied ML formally)
2. Why it matters for THIS project, grounded in our current MosaicHub state
3. Implications for the finding I'm about to write (or just wrote) in /redteam
4. What I should push back on if you later propose something related to this concept

Keep under 400 words. No jargon without an immediate plain-language gloss.
```

---

## 6. Gate / next

- [ ] `04-validate/redteam.md` exists with ≥8 findings, severity-ranked
- [ ] Each finding has blast-radius $, detection cadence, mitigation
- [ ] At least one cross-sprint finding documented
- [ ] IMDA hard-line robustness checked
- [ ] Each finding mapped to a Phase 13 signal or flagged as MLOps gap
- [ ] Claude Code stopped, waiting for `/codify`

**Next file:** [`workflow-08-codify.md`](./workflow-08-codify.md)
