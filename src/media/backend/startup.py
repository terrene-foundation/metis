# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Startup: load posts, train 3 baselines, register 3 drift refs, publish ctx."""

from __future__ import annotations

import logging
import warnings
from pathlib import Path

import polars as pl
from sklearn.exceptions import ConvergenceWarning

# Suppress sklearn numerical warnings from synthetic-embedding fits — same
# rationale as Week 5: outputs are numerically valid; warnings clutter the
# student log on a synthetic dataset.
warnings.filterwarnings("ignore", category=RuntimeWarning, module="sklearn")
warnings.filterwarnings("ignore", category=RuntimeWarning, module="numpy")
warnings.filterwarnings("ignore", category=ConvergenceWarning)

from .config import load_settings
from .ml_context import (
    IMAGE_CLASSES,
    MLContext,
    TEXT_CLASSES,
    build_drift_reference,
    build_fusion_baseline,
    build_image_baseline,
    build_text_baseline,
    set_context,
    synthesise_embeddings,
)

log = logging.getLogger("metis.media.startup")


def _require(path: Path, label: str) -> None:
    if not path.exists():
        raise RuntimeError(
            f"{label} missing at {path} — run `python src/media/scripts/generate_data.py` "
            f"from the repo root to materialise the MosaicHub dataset."
        )


def run_startup_sync() -> None:
    settings = load_settings()
    data_dir = settings.data_dir

    _require(data_dir / "posts_labelled.csv", "posts_labelled")
    _require(data_dir / "baseline_image_metrics.json", "baseline_image_metrics")
    _require(data_dir / "baseline_text_metrics.json", "baseline_text_metrics")
    _require(data_dir / "fusion_baseline.json", "fusion_baseline")
    _require(data_dir / "drift_baseline.json", "drift_baseline")

    log.info("metis.media.startup.loading_posts")
    posts = pl.read_csv(data_dir / "posts_labelled.csv")
    log.info(
        "metis.media.startup.posts_loaded total=%d image=%d text=%d multimodal=%d",
        len(posts),
        int(posts["has_image"].sum()),
        int(posts["has_text"].sum()),
        int(posts["has_image_and_text"].sum()),
    )

    image_posts = posts.filter(pl.col("has_image"))
    text_posts = posts.filter(pl.col("has_text"))
    image_post_ids = image_posts["post_id"].to_list()
    text_post_ids = text_posts["post_id"].to_list()
    fusion_post_ids = posts.filter(pl.col("has_image_and_text"))["post_id"].to_list()

    log.info("metis.media.startup.synthesising_image_embeddings n=%d", len(image_post_ids))
    image_labels = image_posts["image_class_label"].to_list()
    image_embeddings = synthesise_embeddings(image_post_ids, image_labels, modality="image")
    log.info("metis.media.startup.synthesising_text_embeddings n=%d", len(text_post_ids))
    text_labels = text_posts["text_class_label"].to_list()
    text_embeddings = synthesise_embeddings(text_post_ids, text_labels, modality="text")

    log.info("metis.media.startup.training_image_baseline (3-family leaderboard)")
    image_baseline = build_image_baseline(posts, image_embeddings, image_post_ids)
    for fam, entry in image_baseline.candidates.items():
        log.info(
            "metis.media.startup.image[%s] macro_f1=%.3f",
            fam,
            entry.macro_f1,
        )
    log.info(
        "metis.media.startup.image_chosen=%s macro_f1=%.3f",
        image_baseline.chosen_family,
        image_baseline.macro_f1,
    )

    log.info("metis.media.startup.training_text_baseline (3-family leaderboard)")
    text_baseline = build_text_baseline(posts, text_embeddings, text_post_ids)
    for fam, entry in text_baseline.candidates.items():
        log.info(
            "metis.media.startup.text[%s] macro_f1=%.3f",
            fam,
            entry.macro_f1,
        )
    log.info(
        "metis.media.startup.text_chosen=%s macro_f1=%.3f",
        text_baseline.chosen_family,
        text_baseline.macro_f1,
    )

    log.info("metis.media.startup.training_fusion_baseline (early/late/joint)")
    fusion_baseline = build_fusion_baseline(
        posts,
        image_embeddings,
        image_post_ids,
        text_embeddings,
        text_post_ids,
        image_baseline,
        text_baseline,
    )
    log.info(
        "metis.media.startup.fusion_chosen=%s macro_f1=%.3f n_multimodal=%d",
        fusion_baseline.chosen_architecture,
        fusion_baseline.macro_f1,
        len(fusion_post_ids),
    )

    log.info(
        "metis.media.startup.registering_drift_baselines (image weekly / text daily / fusion per-incident)"
    )
    image_calib = {
        c: {
            "brier": image_baseline.candidates[image_baseline.chosen_family].per_class[c]["brier"],
            "ece": 0.0,  # placeholder; calibration plot lives in /drift/check
        }
        for c in IMAGE_CLASSES
    }
    text_calib = {
        c: {
            "brier": text_baseline.candidates[text_baseline.chosen_family].per_class[c]["brier"],
            "ece": 0.0,
        }
        for c in TEXT_CLASSES
    }
    fusion_calib = {
        "cross_modal_harm": {
            "brier": (
                fusion_baseline.early_fusion.per_class["cross_modal_harm"]["brier"]
                if fusion_baseline.early_fusion is not None
                else 0.0
            ),
            "ece": 0.0,
        }
    }
    drift_baselines = {
        "image": build_drift_reference(
            modality="image",
            cadence="weekly",
            embeddings=image_embeddings,
            per_class_calibration=image_calib,
            feature_prefix="img_f",
        ),
        "text": build_drift_reference(
            modality="text",
            cadence="daily",
            embeddings=text_embeddings,
            per_class_calibration=text_calib,
            feature_prefix="txt_f",
        ),
        "fusion": build_drift_reference(
            modality="fusion",
            cadence="per_incident",
            embeddings=(
                image_embeddings[: len(fusion_post_ids)]
                if len(fusion_post_ids) > 0
                else image_embeddings
            ),
            per_class_calibration=fusion_calib,
            feature_prefix="fus_f",
        ),
    }

    ctx = MLContext(
        posts=posts,
        image_embeddings=image_embeddings,
        text_embeddings=text_embeddings,
        image_post_ids=image_post_ids,
        text_post_ids=text_post_ids,
        fusion_post_ids=fusion_post_ids,
        image_baseline=image_baseline,
        text_baseline=text_baseline,
        fusion_baseline=fusion_baseline,
        drift_baselines=drift_baselines,
    )
    set_context(ctx)
    # Hard invariant: 3 drift refs MUST be registered.
    if ctx.drift_baselines_registered != 3:
        raise RuntimeError(
            f"drift_baselines_registered={ctx.drift_baselines_registered}, expected 3 "
            f"(image weekly / text daily / fusion per-incident)"
        )
    log.info(
        "metis.media.startup.ready posts=%d image_baseline_f1=%.3f text_baseline_f1=%.3f "
        "fusion_baseline_f1=%.3f drift_refs=%d",
        len(posts),
        image_baseline.macro_f1,
        text_baseline.macro_f1,
        fusion_baseline.macro_f1,
        ctx.drift_baselines_registered,
    )


async def run_startup() -> None:
    run_startup_sync()
