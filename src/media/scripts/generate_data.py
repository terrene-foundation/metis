# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
# https://creativecommons.org/licenses/by/4.0/
"""Generate the MosaicHub Content Moderation labelled dataset.

Design goals (per PRODUCT_BRIEF + value-auditor stress test):

1. **Cost-table-driven label distribution.** False-negative cost ($320) vs
   false-positive cost ($15) creates a 21:1 asymmetry. Class proportions
   reflect realistic moderation backlog: ~60% safe, ~14% hate-speech /
   harassment, ~10% violence / threats, ~6% nsfw, ~5% weapons, ~3.5%
   csam_adjacent, ~1.5% self-harm. CSAM-adjacent is rare but the IMDA
   $1M ceiling makes it the hardest class.

2. **Per-modality skew.** 30% of posts are image-only, 60% text-only,
   10% multi-modal (~8,000 of 80,000). The multi-modal subset is the
   meme-attack class — joint meaning ≠ per-modality scores.

3. **Adversarial subset.** ~3% of harmful posts are crafted to score
   borderline on a single modality but flagrantly harmful jointly — this
   is the cohort the fusion moderator catches in Sprint 3.

4. **Deterministic.** Every random call routes through one rng seeded
   with SEED. Re-running this script is idempotent given the same seed.

Output (written to `src/media/data/`):

- `posts_labelled.csv`              — 80,000 posts × {has_*, *_class_label, regulator_class, reviewer_decision}
- `images/`                         — 24,000 procedural 32×32 PNG placeholders keyed by post_id
- `baseline_image_metrics.json`     — frozen-ResNet 5-class baseline (descriptive)
- `baseline_text_metrics.json`      — 3-family text leaderboard (descriptive)
- `fusion_baseline.json`            — early/late/joint per-architecture metrics (descriptive)
- `drift_baseline.json`             — per-modality reference distribution summary
- `scenarios/imda_csam_mandate.json`     — Sprint 3 mid-session injection
- `scenarios/election_cycle_drift.json`  — Sprint 4 mid-session injection
- `README.md`                       — file index for students

Determinism: SEED = 20260430. Re-running produces byte-identical artefacts
modulo OS file timestamps.

Usage:

    .venv/bin/python src/media/scripts/generate_data.py [--no-images]
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import polars as pl

SEED = 20260430
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
IMAGES_DIR = DATA_DIR / "images"
SCEN_DIR = DATA_DIR / "scenarios"

N_POSTS = 80_000
N_IMAGES = 24_000  # 30%
N_TEXT = 56_000  # 70%
N_MULTIMODAL = 8_000  # 10%

# --------------------------------------------------------------------------- #
# Class distributions (drive the contract grader's expected cost numbers)
# --------------------------------------------------------------------------- #

IMAGE_CLASS_DISTRIBUTION = {
    "safe": 0.62,
    "nsfw": 0.12,
    "violence": 0.10,
    "weapons": 0.10,
    "csam_adjacent": 0.06,  # rare but $1M-ceiling class
}

TEXT_CLASS_DISTRIBUTION = {
    "safe": 0.60,
    "hate_speech": 0.16,
    "harassment": 0.12,
    "threats": 0.08,
    "self_harm": 0.04,
}

# Reviewer-decision probabilities given the underlying class label. Models the
# fact that human reviewers are NOT perfect; ~88% on safe content (some over-
# zealous removals), ~92% on harmful content (some misses).
REVIEWER_AGREEMENT = {
    "safe": 0.88,
    "harmful": 0.92,
}

REGULATOR_CLASS_MAP = {
    "csam_adjacent": "csam_adjacent",
    "violence": "terrorism_or_violence",
    "weapons": "terrorism_or_violence",
    "self_harm": "self_harm",
    "threats": "harassment",
    "harassment": "harassment",
    "hate_speech": "harassment",
    "nsfw": "none",
    "safe": "none",
}


# --------------------------------------------------------------------------- #
# Post generation
# --------------------------------------------------------------------------- #


def _draw_class(rng: np.random.Generator, dist: dict[str, float]) -> str:
    classes = list(dist.keys())
    probs = np.array(list(dist.values()), dtype=np.float64)
    probs = probs / probs.sum()
    return str(rng.choice(classes, p=probs))


def _reviewer_decision(rng: np.random.Generator, image_lbl: str, text_lbl: str) -> str:
    """allow / review / remove. Reflects the policy in PRODUCT_BRIEF §5 #1."""
    is_harmful = image_lbl != "safe" or text_lbl != "safe"
    agreement = REVIEWER_AGREEMENT["harmful" if is_harmful else "safe"]
    if rng.random() < agreement:
        return "remove" if is_harmful else "allow"
    return "review"  # disagreement → human review queue


def generate_posts(rng: np.random.Generator) -> pl.DataFrame:
    """Build the labelled-post table.

    Strategy: assign every post (a) image_class_label, (b) text_class_label,
    (c) the modality flags (has_image / has_text / has_image_and_text), then
    derive (d) fusion_class_label for the multi-modal subset, (e)
    regulator_class via REGULATOR_CLASS_MAP, (f) reviewer_decision.
    """
    n = N_POSTS

    # Modality flags. We want exactly ~24k image, ~56k text, ~8k multi-modal.
    # Pick image-bearing rows first; from those, ~33% are also multi-modal
    # (since 8k of 24k = 33.3%); the remaining 16k are image-only.
    indices = np.arange(n)
    rng.shuffle(indices)
    image_set = set(indices[:N_IMAGES].tolist())
    text_set = set(indices[N_IMAGES : N_IMAGES + N_TEXT].tolist())
    # Multi-modal cohort: pick from BOTH sets; ~10k that overlap
    overlap = list(image_set & text_set)
    if len(overlap) < N_MULTIMODAL:
        # We need to force overlap by reassigning some text-only posts to
        # also-have-image. Pick text-only posts at random and add them to
        # image_set; remove those slots from the original image_set.
        text_only = [i for i in text_set if i not in image_set]
        image_only = [i for i in image_set if i not in text_set]
        rng.shuffle(text_only)
        rng.shuffle(image_only)
        need = N_MULTIMODAL - len(overlap)
        for k in range(min(need, len(text_only), len(image_only))):
            image_set.discard(image_only[k])
            image_set.add(text_only[k])
        overlap = list(image_set & text_set)
    # Trim to exactly N_MULTIMODAL
    rng.shuffle(overlap)
    multimodal_set = set(overlap[:N_MULTIMODAL])
    has_image = np.array([i in image_set for i in range(n)], dtype=bool)
    has_text = np.array([i in text_set for i in range(n)], dtype=bool)
    has_both = np.array([i in multimodal_set for i in range(n)], dtype=bool)

    # Class labels — draw independently per modality. For posts WITHOUT a
    # modality, label is "safe" (placeholder so the column is non-null).
    #
    # Fusion label rule (drives the joint-embedding signal):
    #   - Both modalities harmful  → cross_modal_harm with prob 0.85
    #     (the joint reinforces — late fusion catches this cleanly)
    #   - Both modalities safe     → cross_modal_harm with prob 0.18
    #     (the adversarial meme-attack subset — joint embedding wins here)
    #   - Mixed (one safe, one harmful) → cross_modal_harm with prob 0.30
    #     (early fusion's middle ground — class-pair signal in concat space)
    # Overall base rate ≈ 22 %, matching PRODUCT_BRIEF figure.
    image_labels = []
    text_labels = []
    fusion_labels = []
    for i in range(n):
        img = _draw_class(rng, IMAGE_CLASS_DISTRIBUTION) if has_image[i] else "safe"
        txt = _draw_class(rng, TEXT_CLASS_DISTRIBUTION) if has_text[i] else "safe"
        if has_both[i]:
            img_harm = img != "safe"
            txt_harm = txt != "safe"
            if img_harm and txt_harm:
                p_harm = 0.85
            elif not img_harm and not txt_harm:
                p_harm = 0.18  # adversarial meme-attack subset
            else:
                p_harm = 0.30
            fusion = "cross_modal_harm" if rng.random() < p_harm else "safe"
        else:
            fusion = "safe"  # placeholder for non-multimodal
        image_labels.append(img)
        text_labels.append(txt)
        fusion_labels.append(fusion)

    # Regulator class: take the more severe of (image, text) per post.
    reg_priority = [
        "csam_adjacent",
        "terrorism_or_violence",
        "self_harm",
        "harassment",
        "none",
    ]
    reg_idx = {k: i for i, k in enumerate(reg_priority)}
    regulator = []
    for img, txt in zip(image_labels, text_labels):
        a = REGULATOR_CLASS_MAP[img]
        b = REGULATOR_CLASS_MAP[txt]
        regulator.append(a if reg_idx[a] <= reg_idx[b] else b)

    # Reviewer decision
    reviewer = [_reviewer_decision(rng, img, txt) for img, txt in zip(image_labels, text_labels)]

    post_ids = [f"post_{i:06d}" for i in range(n)]

    df = pl.DataFrame(
        {
            "post_id": post_ids,
            "has_image": has_image.tolist(),
            "has_text": has_text.tolist(),
            "has_image_and_text": has_both.tolist(),
            "image_class_label": image_labels,
            "text_class_label": text_labels,
            "fusion_class_label": fusion_labels,
            "regulator_class": regulator,
            "reviewer_decision": reviewer,
        }
    )
    return df


# --------------------------------------------------------------------------- #
# Procedural image synthesis (deterministic per post_id)
# --------------------------------------------------------------------------- #


def _class_color(klass: str) -> tuple[int, int, int]:
    """Per-class base RGB for procedural image synthesis. Deterministic."""
    palette = {
        "safe": (140, 200, 140),
        "nsfw": (220, 130, 90),
        "violence": (200, 60, 60),
        "weapons": (110, 110, 130),
        "csam_adjacent": (90, 30, 30),
    }
    return palette.get(klass, (180, 180, 180))


def write_procedural_images(
    image_post_ids: list[str], image_labels: list[str], rng: np.random.Generator
) -> int:
    """Write 32×32 PNG placeholders for each image-bearing post.

    Each PNG is a noise-modulated per-class colour patch — deterministic
    per post_id. Total disk = ~12 MB for 24,000 files. Used as a teaching
    artefact only; the backend does NOT read pixels at inference time
    (it uses synthesised embeddings — see ml_context.py).
    """
    from PIL import Image  # local import keeps top-level fast on --no-images

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    written = 0
    for pid, lbl in zip(image_post_ids, image_labels):
        # Stable per-post seed via numpy from post_id hash
        seed = int.from_bytes(pid.encode()[:4].ljust(4, b"\0"), "big")
        local_rng = np.random.default_rng(seed)
        base = np.array(_class_color(lbl), dtype=np.float32)
        noise = local_rng.normal(loc=0.0, scale=18.0, size=(32, 32, 3)).astype(np.float32)
        img = np.clip(base[None, None, :] + noise, 0, 255).astype(np.uint8)
        Image.fromarray(img, mode="RGB").save(IMAGES_DIR / f"{pid}.png", optimize=False)
        written += 1
    return written


# --------------------------------------------------------------------------- #
# Baseline metrics — descriptive snapshots; the backend re-trains on startup
# --------------------------------------------------------------------------- #


def _frozen_baseline_image_metrics() -> dict:
    return {
        "modality": "image",
        "backbone": "ResNet-50 (frozen)",
        "head": "5-class linear classification head (frozen during scaffold; backend re-fits at startup)",
        "n_train": int(N_IMAGES * 0.75),
        "n_test": int(N_IMAGES * 0.25),
        "per_class": {
            "nsfw": {
                "precision": 0.83,
                "recall": 0.79,
                "f1": 0.81,
                "brier": 0.082,
                "base_rate": 0.12,
            },
            "violence": {
                "precision": 0.78,
                "recall": 0.82,
                "f1": 0.80,
                "brier": 0.094,
                "base_rate": 0.10,
            },
            "weapons": {
                "precision": 0.74,
                "recall": 0.76,
                "f1": 0.75,
                "brier": 0.105,
                "base_rate": 0.10,
            },
            "csam_adjacent": {
                "precision": 0.71,
                "recall": 0.86,
                "f1": 0.78,
                "brier": 0.088,
                "base_rate": 0.06,
            },
            "safe": {
                "precision": 0.95,
                "recall": 0.92,
                "f1": 0.93,
                "brier": 0.045,
                "base_rate": 0.62,
            },
        },
        "macro_f1": 0.814,
        "note": (
            "Descriptive baseline only — the backend re-trains the 3-family "
            "leaderboard at startup against the live posts_labelled.csv. "
            "These numbers are the 'reference picture' Phase 4 students "
            "compare their live runs against."
        ),
    }


def _frozen_baseline_text_metrics() -> dict:
    return {
        "modality": "text",
        "leaderboard": [
            {
                "family": "fine_tuned_bert",
                "n_train": int(N_TEXT * 0.75),
                "n_test": int(N_TEXT * 0.25),
                "per_class": {
                    "hate_speech": {"precision": 0.84, "recall": 0.80, "f1": 0.82, "brier": 0.078},
                    "harassment": {"precision": 0.81, "recall": 0.78, "f1": 0.79, "brier": 0.086},
                    "threats": {"precision": 0.86, "recall": 0.83, "f1": 0.84, "brier": 0.071},
                    "self_harm": {"precision": 0.89, "recall": 0.81, "f1": 0.85, "brier": 0.064},
                    "safe": {"precision": 0.94, "recall": 0.95, "f1": 0.94, "brier": 0.041},
                },
                "macro_f1": 0.848,
            },
            {
                "family": "fine_tuned_roberta",
                "macro_f1": 0.842,
                "note": "Comparable to BERT; ~30% slower fine-tune.",
            },
            {
                "family": "zero_shot_llm",
                "macro_f1": 0.741,
                "note": "Cheap baseline; weakest on rare classes (self_harm).",
            },
        ],
        "chosen_family": "fine_tuned_bert",
    }


def _frozen_fusion_baseline() -> dict:
    return {
        "modality": "fusion",
        "n_multimodal": N_MULTIMODAL,
        "architectures": [
            {
                "name": "early_fusion",
                "macro_f1": 0.762,
                "note": "Concat image+text features → single classifier — cheapest.",
            },
            {
                "name": "late_fusion",
                "macro_f1": 0.781,
                "note": "Per-modality scores → meta-classifier — modular.",
            },
            {
                "name": "joint_embedding",
                "macro_f1": 0.823,
                "note": (
                    "CLIP-style alignment in shared space — best on cross-modal "
                    "harm; 3× compute."
                ),
            },
        ],
        "chosen_architecture": "joint_embedding",
        "cross_modal_harm_base_rate": 0.22,
    }


def _frozen_drift_baseline() -> dict:
    return {
        "image": {
            "modality": "image",
            "cadence": "weekly",
            "feature_dim": 32,
            "n_reference": N_IMAGES,
            "rationale": "Visual style moves slowly; weekly is sufficient for image moderator drift.",
        },
        "text": {
            "modality": "text",
            "cadence": "daily",
            "feature_dim": 32,
            "n_reference": N_TEXT,
            "rationale": "Slang and dogwhistles evolve daily; faster cadence is required.",
        },
        "fusion": {
            "modality": "fusion",
            "cadence": "per_incident",
            "feature_dim": 32,
            "n_reference": N_MULTIMODAL,
            "rationale": "Adversaries probe joint seams in real time; per-incident retrain rule.",
        },
    }


def _scenario_imda_csam_mandate() -> dict:
    return {
        "scenario_id": "imda_csam_mandate",
        "sprint": 3,
        "phase": "11+12 re-run",
        "fires_at": "approx 4:30pm during the workshop",
        "event": (
            "IMDA Online Safety Code clarification: ALL posts scoring > 0.40 on "
            "the csam_adjacent class MUST route to mandatory human review within "
            "60 seconds AND must be auto-blurred in the meantime, regardless of "
            "any cost-balanced auto-remove threshold the platform set."
        ),
        "expected_trust_plane_response": (
            "(1) Re-classify the csam_adjacent threshold from soft (cost-balanced) "
            "to hard (legally mandated) — the IMDA hard floor of 0.40 is now "
            "structurally non-negotiable. "
            "(2) Re-solve the queue allocator with imda_priority as a HARD "
            "constraint — sum_r x[imda_priority, r] >= backlog × 4.0 minutes "
            "MUST hold, regardless of cost. "
            "(3) Re-journal Phase 11 as phase_11_postimda.md AND Phase 12 as "
            "phase_12_postimda.md. The Phase 12 re-run is the most common D3 "
            "(trade-off honesty) zero — students forget the LP needs re-solving. "
            "(4) Quantify the compliance cost in $ of reviewer-time (the shadow "
            "price of the IMDA mandate) in phase_12_postimda.md."
        ),
        "mutates": {
            "fusion_threshold_hard_floor": 0.40,
            "queue_constraint_imda_priority_must_clear_within_sla": True,
        },
        "compliance_cost_terms": {
            "fn_csam_dollar_per_incident": 1_000_000,
            "reviewer_dollar_per_minute_senior": 32.0,
        },
    }


def _scenario_election_cycle_drift() -> dict:
    return {
        "scenario_id": "election_cycle_drift",
        "sprint": 4,
        "phase": "13",
        "fires_at": "approx end of Sprint 3 / start of Sprint 4",
        "event": (
            "Singapore General Election cycle commences. Adversarial drift is "
            "observed on the text moderator — coordinated coded-language "
            "campaigns shift the token-frequency distribution by ~+30% on a "
            "25% subset of inbound posts. The hate_speech and threats class "
            "PSI spikes from 0.04 (steady) to 0.31 (severe) within 18 hours. "
            "Per-class calibration on threats decays by 0.06 Brier."
        ),
        "expected_trust_plane_response": (
            "(1) /drift/check?model_id=text&window=election_cycle_drift "
            "fires SEVERE on multiple features. "
            "(2) Re-train the text moderator (Phase 13 cadence: daily). "
            "(3) Phase 13 retrain rule for text MUST name the seasonal "
            "exclusion: election cycles + major news events are the trigger, "
            "not exception. "
            "(4) Image and fusion drift cadences (weekly / per-incident) are "
            "NOT re-tuned — they have different underlying signals. A "
            "universal 'auto-retrain when X' rule is BLOCKED."
        ),
        "mutates": {
            "drift_text_subset_shift_sigma": 0.30,
            "drift_text_affected_fraction": 0.25,
            "drift_text_psi_jump": [0.04, 0.31],
        },
    }


def _readme(generated_at: str) -> str:
    return f"""# MosaicHub Content Moderation — Data Files

Generated {generated_at} by `src/media/scripts/generate_data.py` (seed {SEED}).

| File | Role | Consumed by |
| --- | --- | --- |
| `posts_labelled.csv` | 80,000 labelled posts (image+text+multimodal) | startup, all routes |
| `images/` | 24,000 procedural 32×32 PNGs keyed by post_id | teaching reference (backend uses synthesised embeddings) |
| `baseline_image_metrics.json` | descriptive frozen-ResNet baseline | Phase 4 reference |
| `baseline_text_metrics.json` | descriptive 3-family text leaderboard | Phase 5 reference |
| `fusion_baseline.json` | descriptive early/late/joint metrics | Phase 5 Multi-Modal |
| `drift_baseline.json` | per-modality cadence + reference summary | Phase 13 reference |
| `scenarios/imda_csam_mandate.json` | Sprint 3 mid-injection (Phase 11 + 12 re-run) | scenario_inject.py |
| `scenarios/election_cycle_drift.json` | Sprint 4 mid-injection (Phase 13 drift) | scenario_inject.py |

**Ground truth the student must NEVER see directly:**

- `regulator_class` column — the regulator-mandated severity bucket.
- `fusion_class_label` column — the cross-modal harm ground truth.
- The 22% adversarial subset within multi-modal — the meme-attack cohort.

The descriptive baselines are the "reference picture" — students compare
their live `/moderate/*/leaderboard` runs against these numbers in Phase 4-6.
The backend re-trains the live baselines at startup against the same
labelled CSV; the live numbers will track these closely but vary with seed.
"""


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--no-images",
        action="store_true",
        help="skip the 24k procedural-image generation (saves ~60s on first run)",
    )
    args = p.parse_args(argv)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SCEN_DIR.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)

    print(f"[generate_data] seed={SEED}")
    print("[generate_data] generating posts table…")
    posts = generate_posts(rng)
    posts_path = DATA_DIR / "posts_labelled.csv"
    posts.write_csv(posts_path)
    print(f"[generate_data] posts → {posts_path} ({len(posts):,} rows)")

    if not args.no_images:
        image_posts = posts.filter(pl.col("has_image"))
        print(f"[generate_data] writing {len(image_posts):,} procedural PNGs to {IMAGES_DIR}…")
        n_written = write_procedural_images(
            image_posts["post_id"].to_list(),
            image_posts["image_class_label"].to_list(),
            rng,
        )
        print(f"[generate_data] images → {n_written:,} files")
    else:
        IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        print("[generate_data] images skipped (--no-images)")

    metrics_files = [
        ("baseline_image_metrics.json", _frozen_baseline_image_metrics()),
        ("baseline_text_metrics.json", _frozen_baseline_text_metrics()),
        ("fusion_baseline.json", _frozen_fusion_baseline()),
        ("drift_baseline.json", _frozen_drift_baseline()),
    ]
    for name, payload in metrics_files:
        out = DATA_DIR / name
        out.write_text(json.dumps(payload, indent=2))
        print(f"[generate_data] {name} → {out}")

    scenarios = [
        ("imda_csam_mandate.json", _scenario_imda_csam_mandate()),
        ("election_cycle_drift.json", _scenario_election_cycle_drift()),
    ]
    for name, payload in scenarios:
        out = SCEN_DIR / name
        out.write_text(json.dumps(payload, indent=2))
        print(f"[generate_data] scenarios/{name} → {out}")

    readme_path = DATA_DIR / "README.md"
    readme_path.write_text(_readme(datetime.now(timezone.utc).isoformat()))
    print(f"[generate_data] README → {readme_path}")

    # Sanity report
    print("\n[generate_data] sanity:")
    print(f"  posts: {len(posts):,}")
    print(f"  has_image: {int(posts['has_image'].sum()):,}  (target {N_IMAGES:,})")
    print(f"  has_text: {int(posts['has_text'].sum()):,}  (target {N_TEXT:,})")
    print(
        f"  has_image_and_text: {int(posts['has_image_and_text'].sum()):,}  (target {N_MULTIMODAL:,})"
    )
    img_dist = posts.filter(pl.col("has_image"))["image_class_label"].value_counts()
    print(f"  image-class distribution:\n{img_dist}")
    txt_dist = posts.filter(pl.col("has_text"))["text_class_label"].value_counts()
    print(f"  text-class distribution:\n{txt_dist}")
    fus_dist = posts.filter(pl.col("has_image_and_text"))["fusion_class_label"].value_counts()
    print(f"  fusion-class distribution:\n{fus_dist}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
