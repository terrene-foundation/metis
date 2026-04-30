<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 13 — Drift × 3 cadences (retrain rules)

> **What this phase does:** Write three retrain rules — one per model — at three cadences (image weekly / text daily / fusion per-incident). Each rule has signal + threshold (variance-grounded) + duration window + HITL disposition + seasonal exclusion.
> **Why it exists:** Without retrain rules, the moderators silently rot. With one universal cadence, fast-moving language drift triggers under-firing on text and over-firing on image. Stratified cadence is the only honest answer.
> **You're here because:** Sprint 4 booted. Phase 13 closes the chain.
> **Key concepts you'll see:** PSI, calibration decay, three cadences, variance-grounded threshold, HITL on first trigger

---

## 1. Paste this into Claude Code

**Universal core:**

```
I'm in Playbook Phase 13 — Drift Retrain Rules. Write three retrain rules,
one per model. For each:

1. Cadence: how often the rule is checked (weekly / daily / per-incident)
2. Signal(s): what is monitored (PSI, calibration decay, FN-rate spike)
3. Threshold per signal: variance-grounded (mean + N std-devs over a
   stable historical window)
4. Duration window: must persist for X consecutive checks before firing
5. HITL disposition on first trigger: human-approves OR auto-fires
6. Seasonal exclusion: windows when the rule does NOT auto-fire

Do NOT propose universal cadence. Three models = three cadences.
Do NOT use "blocker" without specifics.
```

**Tonight-specific additions** (Week 6 MosaicHub):

```
Three models, three cadences (cite from PRODUCT_BRIEF.md §4.4):

1. Image moderator (image_moderator) — WEEKLY
   - Signals: per-class PSI on score distribution; per-pixel-domain PSI
     on a representative embedding feature.
   - Threshold: PSI > N where N is variance-grounded (mean PSI + 3σ
     over a stable historical window). State the historical mean and σ
     used; do NOT guess a value.
   - Duration: signal exceeds threshold for 2 consecutive weekly checks.
   - HITL on first trigger: yes (always, first time).
   - Seasonal exclusion: election cycles, major news events.

2. Text moderator (text_moderator) — DAILY
   - Signals: token-frequency PSI on top-1000 tokens; per-class
     calibration decay (Brier delta vs registered baseline); per-class
     score-distribution PSI.
   - Threshold: variance-grounded (state historical mean and σ).
   - Duration: signal exceeds threshold for 5 consecutive daily checks
     (1 week of sustained drift).
   - HITL on first trigger: yes.
   - Seasonal exclusion: election cycles, major news events.

3. Fusion moderator (fusion_moderator) — PER-INCIDENT
   - Signals: cross-modal alignment-score variance vs registered
     baseline; per-incident calibration check on the post that triggered
     a complaint.
   - Threshold: per-incident — variance > N OR Brier_complaint - Brier_baseline
     > delta. State the historical baseline and what "complaint-triggered
     check" means.
   - Duration: per-incident, but multi-incident aggregation: if 5
     complaints in 7 days exceed threshold, escalate.
   - HITL on first trigger: yes.
   - Seasonal exclusion: election cycles, major news events (the spike
     in adversarial complaints would auto-trigger).

Variance-grounding: every threshold MUST be backed by historical variance
data. The scaffold's drift_baseline.json has the per-model reference.
Use mean + 3σ as the default threshold formula; state the actual values
read from the baseline file in the journal.

HITL on first trigger: explained in appendix/07-governance/hitl-patterns.md.
First time the rule fires, a human (Reviewer Ops Lead per personas in
PRODUCT_BRIEF.md §3) approves the retrain. After 30 days of stable post-
retrain operation, the rule may auto-fire on subsequent triggers.

Seasonal exclusions cited from PRODUCT_BRIEF.md §2: election cycles +
major news events.

Endpoint per model:
- POST /drift/retrain_rule with { model_id, signals, thresholds,
  duration_window, hitl, seasonal_exclusions }
- Call once per model_id (3 calls total).

Journal file: journal/phase_13_retrain.md (single file, three rules
inside).
```

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ Three rules written, one per model, three different cadences
- ✓ Each rule has signals, variance-grounded threshold, duration, HITL, seasonal exclusion
- ✓ Threshold values cite historical mean + σ from drift_baseline.json
- ✓ Seasonal exclusions cite PRODUCT_BRIEF.md §2
- ✓ POST /drift/retrain_rule fired three times (one per model_id)
- ✓ Stop signal pending /redteam

**Signals of drift — push back if you see:**

- ✗ Universal cadence proposed — ask "what's the rationale per model?"
- ✗ Threshold values without variance-grounding — ask "what's the historical mean and σ?"
- ✗ Auto-retrain on first trigger — ask "where's HITL?"
- ✗ Seasonal exclusions missing — ask "election cycles?"
- ✗ Only one POST fired — ask "we have three model_ids"

---

## 3. Things you might not understand in this phase

- **PSI per cadence** — population stability index measured at the cadence appropriate to the modality
- **Calibration decay** — Brier drift over time; matters for queue-allocator probabilities
- **Three cadences** — stratifying retrain frequency by modality drift speed
- **Variance-grounded threshold** — a threshold backed by historical variance, not a guess
- **HITL on first trigger** — first time the rule fires, a human approves; after 30 days stable, auto-fire allowed

---

## 4. Quick reference (30 sec, generic)

### PSI per cadence

PSI (Population Stability Index): sum over bins of (p_now - p_ref) × ln(p_now/p_ref). PSI < 0.10 = stable; 0.10–0.25 = moderate drift; > 0.25 = significant drift. Cadence determines what window of "now" you compare against the reference. Image PSI computed weekly; text PSI computed daily; fusion PSI computed per-incident — same formula, different windows.

> **Deeper treatment:** [appendix/06-monitoring/psi.md](./appendix/06-monitoring/psi.md)

### Calibration decay

Brier score drift over time. Even if F1 holds, the model's P=0.7 may now correspond to actual frequency P=0.55. Calibration decay matters because the queue allocator (Sprint 3) consumes probabilities directly. Tonight's rules monitor calibration as a separate signal alongside PSI for the text moderator (because the queue allocator is sensitive to text probabilities).

> **Deeper treatment:** [appendix/06-monitoring/calibration-decay.md](./appendix/06-monitoring/calibration-decay.md)

### Three cadences

Image: weekly (visual style moves slowly). Text: daily (language moves fast — slang, dogwhistles, evolving codewords). Fusion: per-incident (adversaries probe joint seams in real time, only when they discover them). The universal "weekly retrain" rule under-reacts on text and over-reacts on image. Three cadences are the only honest answer.

> **Deeper treatment:** [appendix/06-monitoring/drift-types.md](./appendix/06-monitoring/drift-types.md)

### Variance-grounded threshold

A threshold that is mean + N standard deviations over a historical stable window. The N is a product decision (3σ ≈ 99.7% of stable distribution). The threshold is honest because it's grounded in the data the model was trained on; an arbitrary "PSI > 0.25" is borrowed from a textbook and might be too tight or too loose for our system.

> **Deeper treatment:** [appendix/06-monitoring/psi.md](./appendix/06-monitoring/psi.md)

### HITL on first trigger

First time the rule fires (signal exceeds threshold over duration window), a human reviewer approves before retrain auto-runs. After the first successful retrain AND 30 days of stable post-retrain operation, the rule may auto-fire on subsequent triggers. The first-trigger HITL prevents catastrophic auto-retrains from a one-day data anomaly.

> **Deeper treatment:** [appendix/07-governance/hitl-patterns.md](./appendix/07-governance/hitl-patterns.md)

---

## 5. Ask CC, grounded in our project (2 min)

```
You are helping me understand a concept from Metis Week 6 Phase 13.

Read the phase file and `workspaces/metis/week-06-media/journal/phase_13_retrain.md`.

Explain "<<< FILL IN: concept name >>>" — plain language, MosaicHub-grounded,
implications for Phase 13 retrain rules, what to push back on. Under 400 words.
```

---

## 6. Gate / next

- [ ] Three rules written, three cadences, variance-grounded thresholds
- [ ] Each rule has signal + threshold + duration + HITL + seasonal
- [ ] Threshold values cite drift_baseline.json
- [ ] POST /drift/retrain_rule fired three times
- [ ] Stop signal pending /redteam

**Next file:** [`workflow-07-redteam.md`](./workflow-07-redteam.md)
