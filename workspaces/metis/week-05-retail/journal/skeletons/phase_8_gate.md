# Phase 8 — Deployment Gate

**Sprint:** 1 (USML) or 2 (SML) · **Time:** **_:_**

## Go / No-Go

<GO / NO-GO with one-sentence reason>

## Ship criteria (must hold)

- **Criterion 1:** **_ at _** (re-tested on deployment hold-out)
- **Criterion 2:** **_ at _**
- **Criterion 3:** **_ at _**

## Monitoring plan

- **Signal:** **_ · **Threshold:** _** · **Cadence:** **_ · **Owner:** _** · **Alert channel:** \_\_\_
- **Signal:** **_ · **Threshold:** _** · **Cadence:** **_ · **Owner:** _** · **Alert channel:** \_\_\_

## Rollback trigger (specific signal, not vibes)

- **Signal:** \_\_\_
- **Threshold:** \_\_\_
- **Duration before triggering:** \_\_\_

## Rollback target (must be known-working today)

<Prior model version / rule-based system / no-op default. Verify it still works before calling it the target.>

## Registry transition

staging → **_ (shadow / production)
Transition reason: _**

## Risks accepted

<What are we shipping despite a Phase 7 finding? Named, dollar-bounded.>

## Reversal condition (D5)

<What would un-ship this? "If rollback trigger fires, revert to **_ within _** hours.">
