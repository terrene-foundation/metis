<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Phase 3 — Feature Framing

> **What this phase does:** Decide which features the moderator uses, classified by availability-at-decision-time, leakage risk, and proxy-for-protected-class status — for both image (pixel-level + augmentations + metadata) and text (tokens, embeddings, account metadata).
> **Why it exists:** Deep learning's "feature engineering" is augmentation choice + metadata inclusion + token preprocessing. A leaky augmentation or a proxy metadata feature corrupts the moderator silently.
> **You're here because:** Phase 2 surfaced the dataset's structural risks. Phase 3 turns them into feature decisions.
> **Key concepts you'll see:** in/out classification, augmentation choices, account metadata, embedding feature, proxy classification

---

## 1. Paste this into Claude Code

**Universal core:**

```
I'm in Playbook Phase 3 — Feature Framing. For each feature the model
WILL use, classify on three axes:

A. Available-at-decision-time (yes/no — leaky if no)
B. Proxy-for-protected-class risk (low/medium/high)
C. Engineering source (raw data / augmentation / metadata / embedding)

Produce a table:
| feature | A | B | C | rationale |

Then propose drop / keep / monitor for each, but the decision is mine.

Do NOT auto-drop features I might want for Phase 7 sweeps.
Do NOT use "blocker" without specifics.

When the table is drafted, stop.
```

**Tonight-specific additions** (Week 6 MosaicHub):

```
Sprint context: Sprint 1 image features. (Sprint 2 text features will be
in a separate Phase 3 SML pass — but tonight Phase 3 is folded into the
Sprint 1 walk.)

Feature surface for image moderator:

Pixel-level (raw):
- raw RGB image (224x224, ImageNet-normalised) — kept; the model needs it
- EXIF metadata — usually OFF (could carry GPS proxy)

Augmentations (training-only):
- random horizontal flip — usually KEEP
- random crop / resize — KEEP
- color jitter — KEEP if production handles varied exposure
- mixup / cutmix — review against label noise (memes break under mixup)
- adversarial training — flag for Phase 7

Account metadata:
- account_country — HIGH proxy risk (ethnicity proxy in SEA markets);
  feature must NOT enter the image moderator without Phase 7 sweep
- account_age_days — MEDIUM proxy (demographic proxy)
- post_time_of_day — MEDIUM (correlates with country/timezone)
- account_verified_status — LOW proxy, KEEP

Image embedding:
- ResNet-50 penultimate-layer 2048-dim vector — KEEP (this IS the model)
- CLIP image-encoder 768-dim vector — used by fusion (Sprint 3)

For each feature, classify on A/B/C. Recommend drop/keep/monitor.

Journal file: copy journal/skeletons/phase_3_features.md into
workspaces/metis/week-06-media/journal/phase_3_features.md.
```

---

## 2. Signals the output is on track

**Signals of success:**

- ✓ Feature table drafted with all 3 axes per feature
- ✓ Account metadata flagged with proxy-risk levels
- ✓ Augmentations have a "monitor" recommendation if mixup/cutmix is on
- ✓ Stop signal pending review

**Signals of drift — push back if you see:**

- ✗ `account_country` kept without explicit Phase 7 sweep — ask "what's the demographic-skew check plan?"
- ✗ Augmentations claimed leak-free without checking against label noise
- ✗ Auto-dropping features that should stay for the Phase 7 sweep
- ✗ Missing rationale per feature

---

## 3. Things you might not understand in this phase

- **In/out classification on 3 axes** — availability + proxy + engineering source
- **Augmentation choices** — which augmentations preserve the harm signal vs corrupt it
- **Account metadata as features** — useful but proxy-heavy
- **Embedding feature** — using a frozen encoder's output as a feature for downstream
- **Proxy classification** — when a feature is a stand-in for a protected class

---

## 4. Quick reference (30 sec, generic)

### In/out classification on 3 axes

Each feature is yes/no on availability at decision time, low/medium/high on proxy risk, and labelled with its source (raw / aug / metadata / embedding). The table forces a deliberate decision per feature rather than a wholesale "include everything." A high-proxy feature can still be in if Phase 7 has a sweep that catches its impact — but it must be flagged.

> **Deeper treatment:** [appendix/02-data/feature-framing.md](./appendix/02-data/feature-framing.md)

### Augmentation choices

Random horizontal flip is harmless for most image moderation. Mixup blends two images and their labels — if one image is harmful and the other safe, the blended label is "0.5 harmful" which corrupts the harm signal. Cutmix has a similar issue. Adversarial training adds robustness but doubles training time. Phase 4 unfreeze-depth interacts with augmentation: deeper unfreezing benefits more from aggressive augmentation.

> **Deeper treatment:** [appendix/02-data/feature-framing.md](./appendix/02-data/feature-framing.md)

### Account metadata as features

`account_country`, `account_age_days`, `account_verified_status` carry signal but also carry proxy risk. SEA markets have country-ethnicity correlation; using country as a feature can amplify demographic bias unless Phase 7 sweeps catch it. The default position: include verified-status (low risk), exclude country (high risk), include age with monitoring.

> **Deeper treatment:** [appendix/02-data/proxy-for-protected-class.md](./appendix/02-data/proxy-for-protected-class.md)

### Embedding feature

Using a frozen pre-trained encoder (ResNet-50, CLIP, BERT) to produce a vector that downstream classifiers consume. The embedding is a feature but ALSO is the model's representation. Tonight: ResNet-50 penultimate layer (2048-dim) is the image-moderator's representation; CLIP image-encoder + text-encoder feed the fusion moderator. Embedding choice IS architecture choice.

> **Deeper treatment:** [appendix/03-modeling/recommender-families.md](./appendix/03-modeling/recommender-families.md)

### Proxy classification

A feature is a "proxy for protected class" if it correlates with a protected attribute (race, religion, gender) without being one explicitly. `account_country` in SEA is a strong ethnicity proxy. `post_time_of_day` correlates with timezone which correlates with country. The Phase 7 demographic-skew sweep is the structural defence — if a proxy feature stays in, Phase 7 must show its impact is bounded.

> **Deeper treatment:** [appendix/02-data/proxy-for-protected-class.md](./appendix/02-data/proxy-for-protected-class.md)

---

## 5. Ask CC, grounded in our project (2 min)

```
You are helping me understand a concept from Metis Week 6 Phase 3.

Read the phase file and `workspaces/metis/week-06-media/journal/phase_3_features.md`.

Explain "<<< FILL IN: concept name >>>" — plain language, MosaicHub-grounded,
implications for Phase 3, what to push back on. Under 400 words.
```

---

## 6. Gate / next

- [ ] Feature table drafted with 3 axes per feature
- [ ] Account-country flagged HIGH proxy with Phase 7 sweep planned
- [ ] Augmentations classified, mixup/cutmix monitored
- [ ] Embedding features named (ResNet-50, CLIP)
- [ ] Stop signal pending review

**Next file:** [`phase-04-candidates.md`](./phase-04-candidates.md)
