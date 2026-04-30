<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Inheritance vs Greenfield

> **One-line hook:** Most real ML projects are inherited, not greenfield — your job is to name what's already fixed and separate it from what's still yours to decide.

## The gist

**Greenfield** means you start from nothing: you choose the model family, the feature set, the evaluation framework, the infrastructure. That's rare in industry.

**Inheritance** is what actually happens: you walk into a project where someone made a K=3 baseline segmentation, committed to a three-family classifier sweep, wired drift monitoring to a fixed reference window, and used specific feature columns. You did not choose any of that. You inherit it. Your job is not to pretend you are starting from scratch; your job is to be explicit about what the inheritance commits you to — and then make the remaining decisions rigorously.

For Arcadia Retail this week: the scaffold ships a K=3 baseline (someone's decision), a three-family classifier sweep (logistic regression + random forest + gradient-boosted trees — someone's decision), a drift reference window (someone's decision), and seven behavioural feature columns (someone's decision). You did not make any of these. You acknowledge them in Phase 1 as the "fixed" layer, then run the Playbook to make the still-open decisions: final K, segment names, per-segment actions, classifier threshold, allocator weights, PDPA classification, retrain rules.

The key discipline of inheritance framing: write down what's fixed (cite the file and function) before you frame what's open. This prevents two failure modes. First, re-deciding things the scaffold already decided (wasting time). Second, treating inherited commitments as your own decisions in the rubric (mis-attribution that undermines the journal).

## Why it matters for ML orchestrators

Week 4 students sometimes spent 30 minutes trying to change the scaffold's baseline before realising it was intentional. That's 30 minutes of clock time gone. An inheritance audit at the start of Phase 1 takes 5 minutes and closes that trap.

## Common confusions

- **"Can I just override everything the scaffold committed to?"** — Technically yes; pedagogically no. The scaffold's commitments are the equivalent of inherited production code. Understand what they do and why before touching them. If you think K=3 is wrong, Phase 4–6 is where you prove it — not by deleting the baseline but by running a sweep and comparing.
- **"Inheritance is a constraint — greenfield is better"** — Not in industry. Inherited systems have battle-tested assumptions baked in. Your job is to augment and validate, not to rebuild from first principles every sprint.

## When you'll hit it

Used in: Phase 1 (Frame — the first thing you do is inventory the inheritance), workflow-01 (analyze — the entire `/analyze` phase is an inheritance audit), workflow-03 (Sprint 1 boot)

## Further reading

_(v1 stub — deeper treatment will be added in post-cohort passes)_

- Sculley et al., "Machine Learning: The High-Interest Credit Card of Technical Debt" — on hidden feedback loops in inherited systems
- Kleppmann, "Designing Data-Intensive Applications" ch. 1 — on evolving systems and their constraints
