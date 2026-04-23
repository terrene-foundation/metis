<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 14 — Fairness Audit (Deferred to Week 7)

> **Status:** Not executed in Week 5. This is a planned phase, not a gap — see below for why deferral is the right call and what happens in the interim.

## Why this phase is deferred

A fairness audit done without the right foundations produces a defensive document, not a real audit. Running it well requires two things Week 5 students haven't built yet: (1) knowing which protected classes actually apply in the jurisdiction — Singapore PDPA, EU GDPR Article 22, US ECOA — not just a general notion of "demographic groups"; and (2) running disparate-impact tests with statistical baselines, which needs the credit-risk and healthcare case material from Weeks 6 and 7. A half-done fairness audit ("no segment is more than 60% one demographic, so we're fine") is worse than no audit — it creates a document the student later references as real.

## What Phase 14 covers (when it runs in Week 7)

Phase 14 has three parts. First, a **disparate-impact analysis** per segment and per model output: does the segmentation, the classifier, or the allocator produce materially different outcomes for different demographic subgroups? The test requires a baseline — what differential rate would be acceptable — and significance — is the observed differential larger than sampling noise? Second, **subgroup metrics**: instead of one overall AUC or Brier score, compute the same metrics for each identifiable subgroup and report the gaps. Third, **mitigation**: if a gap is found, the options are (a) adjust the training data, (b) add a fairness constraint to the allocator (a hard constraint in Phase 11), or (c) document that the gap is accepted with a business reason and regulatory sign-off. None of these options are available without first measuring the gap.

## What you do in Week 5 instead

Three interim steps stand in for Phase 14 until Week 7. During Phase 3 (Feature Audit), run the proxy-check for every demographic-like feature and document proxy concerns explicitly in the Phase 3 journal. During Phase 7 (Red Team), the Safety dimension flags "small-segment vulnerable-population overlap" as a finding with the note "deferred to Week 7 per Playbook." These two interim steps ensure Phase 14 is not silently skipped — it is visibly deferred, with a trail.

## Week 7 placeholder

Phase 14 Fairness Audit is a scheduled deliverable in Week 7. The journal entry from Phase 3 (proxy concerns) and Phase 7 (Safety finding) feed directly into Week 7's opening context. No additional setup is needed in Week 5.
