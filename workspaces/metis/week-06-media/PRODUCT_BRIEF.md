<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# MosaicHub Content Moderation Suite — Product Brief

Workshop product: the **MosaicHub Content Moderation Suite** — one product assembled as a four-layer multi-modal moderation stack (Vision → Text → Fusion → MLOps). By the end of the 210-minute workshop you will have shipped an image moderator (CNN), a text moderator (Transformer), a multi-modal fusion moderator (CLIP-style joint embedding), and drift monitors for all three (MLOps), against a pre-provisioned moderation backend, and defended a page of written decisions that explain why you shipped them that way.

Read this before writing your first prompt. Every dollar figure here is cited by the rubric and the contract grader; making them up in a journal entry scores zero.

Like Week 5, tonight **skips the build phase entirely**. The moderation backend (at `src/media/backend/`), viewer (at `apps/web/media/`), labelled image+text dataset (at `src/media/data/`), baseline CNN (frozen ResNet head, transfer-learned on the labelled set), baseline transformer text classifier (fine-tuned BERT-class), and the joint-embedding moderator with reference distribution registered are all pre-provisioned and running on your laptop before class starts. You walk in, paste one opening prompt, confirm preflight is green, and spend every minute of your 3.5 hours on the **full COC routine** — `/analyze`, `/todos`, `/implement`, `/redteam`, `/codify` — with the 14-phase ML Decision Playbook as the content of `/implement`. You do not scaffold, wire endpoints, or install libraries; you DO still run the routine you know, because that is the institutional muscle memory the course is building. Your job tonight is pure wielding: apply the Playbook to **deep computer vision** (Sprint 1), **transformer NLP** (Sprint 2), **multi-modal fusion** (Sprint 3), and **drift monitoring across modalities** (Sprint 4).

## 1. Business context

MosaicHub is a Singapore-headquartered short-form video and image platform. ~5 million monthly active users across SG, MY, ID, PH, TH; 80% Gen-Z; ~2 million text+image posts per day, ~100,000 video uploads per day, ~30 million daily reactions/comments. The platform is regulated under Singapore's Online Safety (Miscellaneous Amendments) Act 2023 — IMDA can issue takedown directives within 24 hours and the platform must remove "egregious content" (CSAM, terrorism, self-harm encouragement) within an "expeditious" window the regulator interprets in hours, not days. Two years of moderator-decision history sit in `src/media/data/posts_labelled.csv` (image+text+human-decision label).

The Trust & Safety team has been moderating with rules + keyword lists for three years. Reviewer queue depth has tripled since 2024; reviewer turnover is 40%/year; two near-miss CSAM incidents in Q1 2026 escalated to the CEO. The Head of T&S wants ML-assisted triage. The Head of Engineering wants to know when the models start lying. Legal wants a defensible audit trail for every auto-decision. They are asking whether multi-modal AI can triage 80% of clear-cut content automatically, route the 20% gray zone to human reviewers in under 60 seconds, and escalate IMDA-mandatory categories with a hard SLA.

Your job during the workshop is to commission Claude Code to train and evaluate this moderation stack, make the calls the tool cannot make for you, and write the journal that proves you made them.

Two planes run in parallel: the **Trust Plane** is where you decide (what counts as harmful, where the auto-remove line goes, single-modality vs joint, who handles cultural context, when to retrain); the **Execution Plane** is Claude Code, the pre-provisioned backend, and the labelled moderation dataset. If a question is _what_ or _how_, route it to the Execution Plane. If it is _which_, _whether_, _who wins_, or _is it good enough to ship_, it stays with you.

## 2. Cost table (ground truth — use these exact numbers)

These numbers come from MosaicHub's Trust & Safety finance pack. Every journal entry that names dollar impact must cite from this table. Two asymmetries drive every Phase 6 / 7 / 10 / 11 decision tonight: the **false-negative ($320) vs false-positive ($15) ratio of 21:1**, and the **IMDA $1M ceiling** that sits above any cost-balanced threshold and forces the CSAM-class threshold to be hard, not optimised.

| Cost term                                                | Value                               | Unit                                                   | Where it shows up                               |
| -------------------------------------------------------- | ----------------------------------- | ------------------------------------------------------ | ----------------------------------------------- |
| False negative (harmful content left up, then reported)  | $320                                | per piece (regulator complaint risk + lawsuit defense) | Phase 6 metric weighting; Phase 7 Safety        |
| False positive (legitimate content auto-removed)         | $15                                 | per piece (creator trust + appeal-handling cost)       | Phase 6 metric weighting; Phase 7 Robustness    |
| Human reviewer time                                      | $22                                 | per minute on the queue                                | Phase 11 (queue cost); Phase 10 objective       |
| SG Online Safety Code violation (non-takedown of CSAM)   | $1,000,000                          | per incident — IMDA fine + CEO-level reputational      | Phase 11 (HARD ceiling); Phase 7 Safety         |
| Cold-start cost (novel content type, zero-shot misclass) | $8                                  | per misclassified novel meme format                    | Phase 11 (soft constraint); Phase 13 drift      |
| GPU inference cost                                       | $0.03                               | per 1,000 image classifications served                 | Phase 10 (cost-of-serving); Phase 6 (peak load) |
| Peak season                                              | Election cycles + major news events | seasonal adversarial spike                             | Phase 1 framing; Phase 13 drift context         |

Asymmetry: **$320 / $15 = 21:1** (false-negative-to-false-positive). Content moderation lives in this asymmetry — a symmetric metric (raw accuracy) systematically under-prices missing harmful content. The IMDA $1M ceiling on the CSAM class is structurally separate from the cost-balanced threshold logic; it is a regulatory floor, not a cost term to optimise.

Supporting business volumes (for Phase 1 framing):

- 2,000,000 text+image posts per day; 100,000 video uploads per day.
- Current rule+keyword system: 31% recall on harmful content (lots of false negatives), 4% false positive rate, no audit trail.
- Reviewer queue depth: average 8,000 items at start of workshop; SLA target = clear queue within 90 minutes.
- Scaffold sample: **80,000 labelled posts** (60% text, 30% image, 10% multi-modal memes); each has a human-reviewer decision label (allow / review / remove) AND a regulator-class flag (CSAM-adjacent / terrorism / self-harm / harassment / none).

## 3. Personas (who you are serving)

You play the Student role and commission the Execution Plane on behalf of the four Trust Plane personas below.

| Persona             | Plane           | What they do                                                                              | What they read                               |
| ------------------- | --------------- | ----------------------------------------------------------------------------------------- | -------------------------------------------- |
| Head of T&S         | Trust Plane     | Approves moderation policy + auto-remove thresholds; signs off on reviewer queue routing  | Policy doc, threshold dashboard, queue stats |
| Head of Engineering | Trust Plane     | Tracks live model performance; owns the decision to retrain or roll back any of the three | Drift charts, calibration plots              |
| Legal Counsel       | Trust Plane     | Signs off on IMDA-mandatory hard constraints; owns the audit trail                        | Decision log, hard-constraint table          |
| Reviewer Ops Lead   | Trust Plane     | Owns the human reviewer queue; sets SLA; owns reviewer training                           | Queue depth chart, reviewer-time chart       |
| ML Engineer         | Execution Plane | Ships training pipeline, registry, drift monitor (= Claude Code during the workshop)      | Logs, run tracker, model registry            |
| Student (you)       | Trust Plane     | Commissions every piece; graded on journal + contract grader                              | Viewer Pane, terminal, `PLAYBOOK.md`         |

## 4. The product story — one product, four layered modules (the multi-modal value chain)

This is a single moderation product built as the multi-modal value chain: **see → read → fuse → monitor**. Each module consumes the one above it. Skip a link and the whole chain misses the harm category that lives there (image-only sees pixels but misses the text overlay; text-only reads captions but misses the image; fusion catches both but drifts faster than either; monitor watches all three).

1. **The image moderator sees pixels (CNN · Sprint 1).** Every uploaded image gets a per-class score (NSFW / violence / weapons / CSAM-adjacent / safe). A pre-trained ResNet backbone with a fine-tuned classification head — transfer learning is the practical default for vision tonight, not training from scratch.
2. **The text moderator reads captions (Transformer · Sprint 2).** Every caption / comment / DM-content gets a per-class score (hate speech / harassment / threats / self-harm-encouragement / safe). A fine-tuned BERT-class encoder — you do not train a transformer from scratch in 50 minutes.
3. **The fusion moderator catches the meme (Multi-modal · Sprint 3).** A joint-embedding model (CLIP-style — image encoder + text encoder + alignment head) that catches cross-modal harm — the cute-puppy image + "destroy all humans" caption that Sprint 1 and Sprint 2 each individually rate as safe. This is where multi-modal earns its compute cost or doesn't.
4. **The drift monitor watches three differently-drifting models (MLOps · Sprint 4).** Three rules, three cadences, three signals: image-class distribution drift (weekly), text-token distribution drift (daily, faster — language moves faster than visual style), fusion calibration decay (per-incident). Without Sprint 4 the chain rots silently as adversaries learn the seams.

Cascade: image score quality → text score quality → fusion's ability to catch what neither caught → monitoring coverage. One product, four layers, one chain of decisions.

## 4a. The four modules on the table tonight

### 4.1 Image Moderator (Sprint 1 · CNN · See)

**What it is.** A CNN-based image classifier that returns per-class probabilities (NSFW / violence / weapons / CSAM-adjacent / safe) for every uploaded image. The scaffold ships a frozen ResNet-50 backbone with a 5-class head fine-tuned on the 80k labelled posts; per-class precision / recall / F1 visible at `/moderate/image/leaderboard`. Scaffold sample: 24,000 image-bearing posts.

**Why it exists.** The Head of T&S cannot review 100,000 video frames + 600,000 images per day with humans alone. The image moderator triages the obvious 80% (clear NSFW, clear violence) and routes the gray zone to humans.

**Who signs off.** Head of T&S (per-class threshold) and Legal Counsel (CSAM-adjacent threshold is hard, not cost-balanced).

**Success at 5:30 pm.** A chosen architecture (frozen / partial-fine-tune / full-fine-tune) is promoted from staging to shadow in the image-moderator registry. Each of the 5 classes has a defended threshold tied to the $320 / $15 asymmetry AND the IMDA $1M ceiling for the CSAM class. K is defended in the Phase 6 journal tied to per-class PR curves AND the counterfactual lift vs the 31%-recall rule-based baseline.

### 4.2 Text Moderator (Sprint 2 · Transformer · Read)

**What it is.** A fine-tuned transformer (BERT-class, 110M-parameter range — fits on a modest GPU) that scores caption / comment text on (hate-speech / harassment / threats / self-harm-encouragement / safe). Same 3-family leaderboard pattern as Week 5 SML — fine-tuned BERT + fine-tuned RoBERTa + zero-shot LLM (the cheap-prompt baseline). The scaffold trains the first two at startup; `/moderate/text/leaderboard` exposes the comparison. Scaffold sample: 56,000 text-bearing posts.

**Why it exists.** The Head of T&S wants 60-second turnaround on text moderation; the regulator wants minutes on threats. Text is faster-changing than images — slang, dogwhistles, evolving codewords — so the transformer has to be retrainable on a faster cadence than the CNN.

**Who signs off.** Head of T&S (chosen family + per-class threshold) and Reviewer Ops Lead (threshold must respect the 8,000-item queue ceiling).

**Success at 5:30 pm.** Both the BERT and RoBERTa fine-tunes are on the leaderboard; chosen family is defended in Phase 5 SML; cost-based threshold defended in Phase 6 SML against the $320 / $15 asymmetry; calibration confirmed (Brier + reliability diagram); promotion to shadow in the text-moderator registry.

### 4.3 Fusion Moderator (Sprint 3 · Multi-Modal · Decide)

**What it is.** A CLIP-style joint embedding moderator. Image encoder (the Sprint 1 CNN's penultimate layer) + text encoder (the Sprint 2 transformer's pooled representation) + a small alignment head trained on the multi-modal subset. Returns a "cross-modal-harm" score that disagrees with the per-modality scores when the joint meaning is harmful. The scaffold ships an early-fusion baseline + a late-fusion variant; you pick the architecture in Phase 5 Multi-Modal. Scaffold sample: 8,000 multi-modal memes (the curated meme subset).

**Why it exists.** A cute puppy image (Sprint 1: safe) + "I want to destroy all humans" caption (Sprint 2: harmless joke; not a threat) is a HARMFUL meme. Single-modality scores miss the joint meaning. The fusion moderator is where the platform defends against the adversarial attack class that targets exactly this seam.

**Who signs off.** Head of T&S (fusion architecture choice) and Head of Engineering (compute budget — fusion is 3× more expensive than either modality alone).

**Mid-sprint injection (~4:30pm).** **IMDA issues a CSAM mandate clarification:** any post scoring >0.4 on the CSAM-adjacent class MUST route to mandatory human review within 60 seconds AND must be auto-blurred in the meantime, regardless of any cost-balanced auto-remove threshold the platform set. This forces re-classification of the CSAM-class threshold from soft (cost-balanced) to hard (legally mandated), AND re-solving the human-reviewer queue allocator (Phase 11 + Phase 12 both, like Week 5's PDPA fire). Students re-journal Phase 11 + 12 as `_postimda.md`.

**Success at 5:30 pm.** `/moderate/fusion/score` produces the joint score; the architecture choice (early / late / joint) is defended in Phase 10 + 11 journals; post-IMDA re-run saved as `phase_11_postimda.md` AND `phase_12_postimda.md` (skipping the Phase 12 re-run is the single most common D3 failure).

### 4.4 Drift Monitor × 3 models (Sprint 4 · MLOps · Monitor)

**What it is.** Three drift rules, one per artefact, because the three models drift on different signals at different cadences. Image moderator drifts on **per-class score distribution + per-pixel-domain distribution** (weekly — visual style moves slowly). Text moderator drifts on **token frequency + embedding distribution + per-class calibration** (daily — language moves fast). Fusion moderator drifts on **cross-modal alignment score variance + per-incident calibration decay** (per-incident — adversaries probe joint seams in real time). The scaffold's `/drift/check` accepts a window name and returns per-feature PSI + per-class calibration decay + overall severity per model.

**Why it exists.** Without Sprint 4 a "working" moderator silently degrades to "31% recall like the old keyword system" over the next quarter without anyone noticing. The Reviewer Ops Lead needs three drift rules — one per model — with variance-grounded thresholds, duration windows, and human-in-the-loop on first trigger. The Phase 13 journal captures all three in one entry.

**Who signs off.** Head of Engineering (monitoring + retrain rules), Head of T&S (re-training approval under HITL first trigger), Reviewer Ops Lead (queue impact during retrain).

**Success at 5:30 pm.** `/drift/retrain_rule` has been called for each of the three model IDs (image / text / fusion) with defensible thresholds. Each rule names: signal, threshold, duration window, HITL disposition, seasonal exclusions (election cycles, major news events). The Phase 13 journal entry covers all three.

## 5. The five Trust Plane decision moments

Tonight collapses into five moments where the decision has teeth. Every other phase produces artefacts; these five are where you can silently ship a weak product if you are not paying attention. They are the rubric's highest-pressure points.

1. **Define what counts as harmful** (Phase 1). _Tonight_: which of CSAM-adjacent / terrorism / self-harm-encouragement / hate-speech / harassment / sexual-content / violence-depiction belong on the auto-remove side, which belong on the human-review side, which are "creator-warn" only. Policy decision, not technical — the model enforces rules YOU write.
2. **Set the auto-remove confidence threshold per class** (Phase 6) — defended in $ of (false-negative cost × FN rate at threshold) + (false-positive cost × FP rate at threshold), with the IMDA $1M ceiling forcing CSAM-adjacent to a structurally hard threshold (not cost-balanced — see decision moment 4).
3. **Choose the fusion architecture** (Phase 5 Multi-Modal). Early-fusion (concatenate image + text features before classification head — cheap, brittle on adversarial cases), late-fusion (per-modality scores + meta-classifier — modular, slower to retrain), or joint-embedding (CLIP-style — most accurate on cross-modal harm, 3× compute). Defended with multi-modal coverage gain × dollar value vs compute cost delta.
4. **Re-classify CSAM-adjacent threshold as hard when IMDA mandate fires** (Phase 11 + re-run Phase 12). Not just the journal entry — re-solve the reviewer queue allocator with the new HARD constraint and quantify the queue-cost shadow price (compliance cost in $ of reviewer time).
5. **Set retrain rules × 3 models, grounded in historical variance** (Phase 13). Three rules, three cadences (image weekly / text daily / fusion per-incident), three signals. No universal "auto-retrain when X" — signal + threshold + duration window + HITL.

All five are non-negotiable tonight.

## 6. 5:30 pm success definition

By the close of the workshop, a passing run looks like this. Every item is grader-verifiable or rubric-verifiable.

- [ ] **All four modules' endpoints return real data** (no `{"status":"ok"}` stubs): `/moderate/image/leaderboard` + `/moderate/image/threshold` (per-class), `/moderate/text/leaderboard` + `/moderate/text/threshold` (per-class), `/moderate/fusion/score` + `/moderate/fusion/architecture`, `/drift/check` ran against the recent_30d window for all three model IDs, `/drift/retrain_rule` called for image / text / fusion.
- [ ] **At least 14 journal entries** at `journal/phase_N_{vision,text,fusion,...}.md`. Each one names its signal, threshold, and duration under `## Reversal condition` — never the phrase "if data changes".
- [ ] **IMDA injection produces four files, not two**: `journal/phase_11_constraints.md`, `journal/phase_11_postimda.md`, `journal/phase_12_accept.md`, `journal/phase_12_postimda.md`. The IMDA re-run hits the FUSION moderator's reviewer-queue allocator, not just the threshold. The compliance cost (queue-time delta in dollars) is quantified in `phase_12_postimda.md`.
- [ ] **Phase 13 journal has three rules**, one per model (image / text / fusion), each with signal + variance-grounded threshold + duration window + HITL disposition + seasonal exclusions (elections, news events).
- [ ] **The value-chain banner on the viewer shows all four sprints green** at close, and the five decision moments all ticked.

Combined score target: ≥ 0.60 (60% journal rubric mean + 40% endpoint-contract grader).

## 7. What is different from Week 5 (read this if you took Week 5)

- **No scaffold work, but the COC routine still runs.** The backend, data labeller, baseline CNN, baseline transformer text classifier, fusion-moderator stub, and drift reference for all three models are pre-provisioned at `src/media/` and `apps/web/media/`. Your first prompt confirms preflight is green, then you enter `/analyze` (inventorying baseline commitments and open decisions), `/todos` (Playbook phases as plan; instructor gate), `/implement` (four sprints CNN→Transformer→Fusion→MLOps), `/redteam`, `/codify`. The Playbook phases are the CONTENT of `/implement`, not a replacement for the routine.
- **Deep learning replaces classical ML.** Week 5 was clustering + tabular classifiers + LP. Week 6 is CNN (transfer learning) + Transformer (fine-tuning) + multi-modal fusion (joint embedding). The Playbook phases stay the same — the model families and metrics swap.
- **Three classifiers, three modalities.** Week 5 had two SML classifiers (churn + conversion) on tabular features. Week 6 has three classifiers across three modalities (image / text / fusion). Each demands its own threshold defense in Phase 6.
- **Per-class thresholds replace single thresholds.** Week 5 picked one threshold per binary classifier. Week 6 picks one threshold per class per moderator (5 image classes × image moderator + 5 text classes × text moderator + 1 cross-modal-harm threshold for fusion). Phase 6 is correspondingly heavier.
- **IMDA is the new PDPA** — Week 5's PDPA-§13 under-18 browsing → Week 6's IMDA CSAM mandate clarification. Same rubric pressure (hard/soft constraint classification), different regulatory surface. Fires mid-Sprint-3 at 4:30 against the FUSION queue allocator (re-run Phase 11 + 12).
- **The queue allocator is the new campaign allocator** — Week 5 optimised marketing budget across (segment × campaign) under PDPA + touch budget + inventory. Week 6 optimises reviewer-minute budget across (incoming-post × queue-tier) under IMDA + reviewer headcount + SLA. Phase 12 asks the same questions: feasibility, queue-time gap, pathologies (tier starvation? reviewer overload?), accept / re-tune / fall back / redesign.
- **Drift cadences are stratified by modality.** Week 5 had three drift signals on a similar cadence. Week 6's three signals operate on weekly (image) / daily (text) / per-incident (fusion) cadences. Phase 13 must defend each cadence separately — universal "weekly retrain" is BLOCKED.

## 8. Where to go next

- `START_HERE.md` — student manual with the opening prompt, the COC-wrapped clock, and the four-sprint flow.
- `PLAYBOOK.md` — the universal 14-phase procedure with teaching blocks (CNN lens + Transformer lens + Multi-Modal lens + Your levers + Transfer to next project) per phase.
- `SCAFFOLD_MANIFEST.md` — every pre-built file, who writes it, who reads it.
- `src/media/data/posts_labelled.csv` — the labelled moderation dataset (image+text+human-decision label).
- `src/media/data/baseline_image_metrics.json` + `baseline_text_metrics.json` — pre-built baseline per-class metrics.
- `src/media/data/drift_baseline.json` — registered drift reference distribution (per modality).
- `src/media/data/scenarios/` — mid-session injection payloads (`imda_csam_mandate.json`, `election_cycle_drift.json`).
- `journal/skeletons/` — fill-in-the-blank per-phase templates; copy into `journal/phase_N_*.md` at the start of each phase.
