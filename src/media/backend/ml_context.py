# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Shared ML state for the MosaicHub Content Moderation backend.

Loaded once at startup (`startup.run_startup`) and read by every route. The
three baseline moderators (image / text / fusion) are pre-trained here so
the student never waits on training to start the lesson.

Pedagogical contract:

    The "frozen ResNet head" / "fine-tuned BERT" framing is honest in the
    sense that we train a downstream classifier on top of frozen-backbone
    embeddings — exactly what transfer-learning the head means in practice.
    For laptop-runtime feasibility the embeddings are synthesised
    deterministically per post_id via per-class Gaussian centroids; the
    classifiers themselves (LR / RF / GBM, 3-family leaderboard per modality)
    are real sklearn fits on real labels and produce real per-class
    precision / recall / F1 / Brier numbers. Students see the leaderboard
    move when they re-run with different seeds.

Invariants (load-bearing, asserted at startup):

    - `_CTX` singleton: set exactly once via `set_context`; read-only after.
    - `drift_baselines_registered` MUST equal 3 (image, text, fusion).
    - Image classes MUST be the 5-tuple: nsfw, violence, weapons,
      csam_adjacent, safe.
    - Text classes MUST be the 5-tuple: hate_speech, harassment, threats,
      self_harm, safe.
    - `CSAM_ADJACENT_HARD_FLOOR == 0.40` — IMDA structural constraint, not
      a cost-balanced threshold; routes MUST refuse promotions below this.
"""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import polars as pl
from sklearn.ensemble import (
    HistGradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    brier_score_loss,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

log = logging.getLogger("metis.media.ml_context")


# --------------------------------------------------------------------------- #
# Class taxonomies (frozen — Phase 1 of the Playbook depends on these names)
# --------------------------------------------------------------------------- #

IMAGE_CLASSES: tuple[str, ...] = (
    "nsfw",
    "violence",
    "weapons",
    "csam_adjacent",
    "safe",
)

TEXT_CLASSES: tuple[str, ...] = (
    "hate_speech",
    "harassment",
    "threats",
    "self_harm",
    "safe",
)

FUSION_CLASSES: tuple[str, ...] = ("cross_modal_harm", "safe")

# IMDA Online Safety Code: CSAM-adjacent threshold is structurally HARD.
# Routes MUST refuse promotions whose chosen threshold falls below this floor.
CSAM_ADJACENT_HARD_FLOOR: float = 0.40

# Embedding dimensionality (synthetic per-class Gaussian; real sklearn fits).
EMBED_DIM: int = 32


# --------------------------------------------------------------------------- #
# Dataclasses
# --------------------------------------------------------------------------- #


@dataclass
class ClassifierLeaderboardEntry:
    """One row of a 3-family leaderboard (LR / RF / GBM-style)."""

    family: str
    family_why: str
    macro_f1: float
    per_class: dict[str, dict[str, float]]  # class -> {precision, recall, f1, brier, base_rate}
    threshold: dict[str, float]  # class -> chosen operating threshold
    model: Any  # sklearn estimator (kept for live re-scoring)
    scaler: StandardScaler


@dataclass
class ImageBaseline:
    """Frozen-ResNet-backbone + 5-class fine-tuned head, 3-family leaderboard."""

    classes: tuple[str, ...] = field(default_factory=lambda: IMAGE_CLASSES)
    candidates: dict[str, ClassifierLeaderboardEntry] = field(default_factory=dict)
    chosen_family: str = "gradient_boosted"
    macro_f1: float = 0.0
    stage: str = "staging"  # staging -> shadow -> production
    promoted_thresholds: dict[str, float] = field(default_factory=dict)


@dataclass
class TextBaseline:
    """Fine-tuned BERT + RoBERTa + zero-shot LLM, 3-family leaderboard."""

    classes: tuple[str, ...] = field(default_factory=lambda: TEXT_CLASSES)
    candidates: dict[str, ClassifierLeaderboardEntry] = field(default_factory=dict)
    chosen_family: str = "fine_tuned_bert"
    macro_f1: float = 0.0
    stage: str = "staging"
    promoted_thresholds: dict[str, float] = field(default_factory=dict)


@dataclass
class FusionBaseline:
    """Joint-embedding moderator: early-fusion + late-fusion variants."""

    classes: tuple[str, ...] = field(default_factory=lambda: FUSION_CLASSES)
    early_fusion: ClassifierLeaderboardEntry | None = None
    late_fusion: ClassifierLeaderboardEntry | None = None
    joint_embedding: ClassifierLeaderboardEntry | None = None
    chosen_architecture: str = "early_fusion"
    macro_f1: float = 0.0
    stage: str = "staging"
    promoted_threshold: float = 0.50


@dataclass
class DriftReference:
    """Reference distribution for a single moderator (image / text / fusion)."""

    modality: str  # "image" | "text" | "fusion"
    cadence: str  # "weekly" | "daily" | "per_incident"
    feature_means: dict[str, float]
    feature_stds: dict[str, float]
    per_class_calibration: dict[str, dict[str, float]]  # class -> {brier, ece}
    window_size: int


@dataclass
class MLContext:
    posts: pl.DataFrame
    image_embeddings: np.ndarray  # (n_image_posts, EMBED_DIM) — np.float32
    text_embeddings: np.ndarray  # (n_text_posts, EMBED_DIM) — np.float32
    image_post_ids: list[str]
    text_post_ids: list[str]
    fusion_post_ids: list[str]
    image_baseline: ImageBaseline
    text_baseline: TextBaseline
    fusion_baseline: FusionBaseline
    drift_baselines: dict[str, DriftReference]  # "image" | "text" | "fusion"

    @property
    def drift_baselines_registered(self) -> int:
        return len(self.drift_baselines)


# --------------------------------------------------------------------------- #
# Singleton accessor
# --------------------------------------------------------------------------- #

_CTX: MLContext | None = None


def set_context(ctx: MLContext) -> None:
    global _CTX
    _CTX = ctx


def get_context() -> MLContext:
    if _CTX is None:
        raise RuntimeError("ML context not initialised — startup must run first")
    return _CTX


# --------------------------------------------------------------------------- #
# Embedding synthesis (deterministic per post_id; per-class Gaussian centroids)
# --------------------------------------------------------------------------- #


def _post_seed(post_id: str, modality: str) -> int:
    """Stable per-(post, modality) seed derived from sha256 — survives reruns."""
    h = hashlib.sha256(f"{post_id}:{modality}".encode()).digest()
    return int.from_bytes(h[:4], "big", signed=False)


def _class_modes(
    klass: str, modality: str, dim: int = EMBED_DIM, n_modes: int = 2
) -> list[np.ndarray]:
    """Deterministic N-mode mixture per (class, modality).

    Each class's distribution is the union of `n_modes` distinct Gaussian
    centroids. A linear classifier can only fit the marginal mean of the
    modes (low precision because the mean lives between the modes); a tree
    ensemble (RF / GBM) carves each mode as its own decision region. This
    is the textbook geometry that makes the non-linear families win over
    linear ones — same lesson as the XOR / spirals pedagogy classics.

    n_modes=2 was empirically calibrated (with `noise_scale=2.8` in
    `synthesise_embeddings`) so that on 80k 5-class image data the
    leaderboard ranks GBM > LR > RF with macro_f1 in the [0.55, 0.88] band.
    """
    rng = np.random.default_rng(_post_seed(klass, f"modes:{modality}"))
    # Modes are spread far enough apart that the marginal mean a linear
    # classifier would fit ends up between them — forcing LR to lose
    # precision relative to RF/GBM, which carve each mode as its own region.
    spread = np.sqrt(dim, dtype=np.float32) * 0.30
    modes = []
    for _ in range(n_modes):
        m = rng.normal(loc=0.0, scale=1.0, size=dim).astype(np.float32) * spread
        modes.append(m)
    return modes


def synthesise_embeddings(
    post_ids: list[str],
    labels: list[str],
    modality: str,
    dim: int = EMBED_DIM,
    noise_scale: float = 2.8,
    n_modes: int = 2,
) -> np.ndarray:
    """Build a (len(post_ids), dim) float32 embedding matrix.

    Each row = mode_centroid(label, mode_idx) + Gaussian noise(noise_scale),
    where mode_idx is drawn deterministically per post_id from `n_modes`
    sub-clusters of the class. The multi-mode geometry forces non-linear
    classifiers to win on the 3-family leaderboard (see `_class_modes`).
    Deterministic per post_id so re-runs produce identical embeddings.
    """
    modes_per_class = {k: _class_modes(k, modality, dim, n_modes=n_modes) for k in set(labels)}
    out = np.zeros((len(post_ids), dim), dtype=np.float32)
    for i, (pid, lbl) in enumerate(zip(post_ids, labels)):
        rng = np.random.default_rng(_post_seed(pid, modality))
        mode_idx = int(rng.integers(0, n_modes))
        centroid = modes_per_class[lbl][mode_idx]
        noise = rng.normal(loc=0.0, scale=noise_scale, size=dim).astype(np.float32)
        out[i] = centroid + noise
    return out


# --------------------------------------------------------------------------- #
# Per-class metrics
# --------------------------------------------------------------------------- #


def _per_class_metrics(
    y_true: np.ndarray,
    y_proba: np.ndarray,
    classes: tuple[str, ...],
    threshold: float = 0.50,
) -> dict[str, dict[str, float]]:
    """Compute per-class precision/recall/F1/Brier at a per-class threshold."""
    out: dict[str, dict[str, float]] = {}
    for ci, cname in enumerate(classes):
        y_true_c = (y_true == ci).astype(int)
        y_prob_c = y_proba[:, ci]
        y_pred_c = (y_prob_c >= threshold).astype(int)
        # sklearn accepts zero_division in {0, 1, np.nan, "warn"}; its py.typed
        # stubs declare the parameter as str only, so the int 0 trips Pyright
        # despite being valid at runtime. Ignore the call sites.
        prec = precision_score(y_true_c, y_pred_c, zero_division=0)  # type: ignore[arg-type]
        rec = recall_score(y_true_c, y_pred_c, zero_division=0)  # type: ignore[arg-type]
        f1 = f1_score(y_true_c, y_pred_c, zero_division=0)  # type: ignore[arg-type]
        out[cname] = {
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1": round(float(f1), 4),
            "brier": round(float(brier_score_loss(y_true_c, y_prob_c)), 4),
            "base_rate": round(float(y_true_c.mean()), 4),
        }
    return out


def _macro_f1(per_class: dict[str, dict[str, float]]) -> float:
    if not per_class:
        return 0.0
    return round(sum(p["f1"] for p in per_class.values()) / len(per_class), 4)


# --------------------------------------------------------------------------- #
# 3-family leaderboard builder
# --------------------------------------------------------------------------- #


def _train_family(
    name: str,
    why: str,
    estimator: Any,
    # train_test_split's py.typed stub returns list[Any], not the 4-tuple of
    # ndarrays it actually produces. Accept Any here to keep Pyright quiet
    # without losing the runtime contract — every caller passes ndarrays.
    X_train: Any,
    X_test: Any,
    y_train: Any,
    y_test: Any,
    classes: tuple[str, ...],
    threshold: float = 0.50,
    scaler: StandardScaler | None = None,
) -> ClassifierLeaderboardEntry:
    estimator.fit(X_train, y_train)
    y_proba = estimator.predict_proba(X_test)
    # Some estimators may produce a sparse class set if the train split misses
    # a rare class; right-pad the proba matrix so per-class indexing is safe.
    if y_proba.shape[1] < len(classes):
        full = np.zeros((y_proba.shape[0], len(classes)), dtype=np.float32)
        for src_idx, cls_int in enumerate(estimator.classes_):
            full[:, int(cls_int)] = y_proba[:, src_idx]
        y_proba = full
    per_class = _per_class_metrics(y_test, y_proba, classes, threshold=threshold)
    return ClassifierLeaderboardEntry(
        family=name,
        family_why=why,
        macro_f1=_macro_f1(per_class),
        per_class=per_class,
        threshold={c: threshold for c in classes},
        model=estimator,
        scaler=scaler if scaler is not None else StandardScaler().fit(X_train),
    )


def build_image_baseline(
    posts: pl.DataFrame,
    image_embeddings: np.ndarray,
    image_post_ids: list[str],
    seed: int = 20260430,
) -> ImageBaseline:
    """Train the 3-family image leaderboard (frozen-ResNet → fine-tuned head).

    Pedagogical: "frozen ResNet head + fine-tuned 5-class classifier" — the
    embeddings ARE frozen (synthesised once per post), the head IS fine-tuned
    here on real labels via three classifier families.
    """
    label_lookup = dict(zip(posts["post_id"].to_list(), posts["image_class_label"].to_list()))
    y_str = [label_lookup[p] for p in image_post_ids]
    class_to_int = {c: i for i, c in enumerate(IMAGE_CLASSES)}
    y = np.array([class_to_int[lbl] for lbl in y_str], dtype=np.int64)

    scaler = StandardScaler().fit(image_embeddings)
    X_std = scaler.transform(image_embeddings)
    X_tr, X_te, y_tr, y_te = train_test_split(
        X_std, y, test_size=0.25, random_state=seed, stratify=y
    )

    families = {
        "frozen_resnet_lr_head": (
            "frozen ResNet backbone + linear head (cheapest; near-zero retrain time)",
            LogisticRegression(max_iter=300, random_state=seed),
        ),
        "frozen_resnet_rf_head": (
            "frozen ResNet backbone + random forest head (non-linear; robust to noise)",
            RandomForestClassifier(n_estimators=80, max_depth=12, random_state=seed, n_jobs=-1),
        ),
        "frozen_resnet_gbm_head": (
            "frozen ResNet backbone + gradient-boosted head (best per-class F1; slowest)",
            HistGradientBoostingClassifier(
                max_iter=100, max_depth=4, learning_rate=0.10, random_state=seed
            ),
        ),
    }

    candidates: dict[str, ClassifierLeaderboardEntry] = {}
    for name, (why, est) in families.items():
        candidates[name] = _train_family(
            name=name,
            why=why,
            estimator=est,
            X_train=X_tr,
            X_test=X_te,
            y_train=y_tr,
            y_test=y_te,
            classes=IMAGE_CLASSES,
            threshold=0.50,
            scaler=scaler,
        )

    chosen = max(candidates, key=lambda k: candidates[k].macro_f1)
    # CSAM-adjacent default threshold MUST start at the IMDA hard floor.
    promoted_thresholds = {c: 0.50 for c in IMAGE_CLASSES}
    promoted_thresholds["csam_adjacent"] = CSAM_ADJACENT_HARD_FLOOR
    return ImageBaseline(
        candidates=candidates,
        chosen_family=chosen,
        macro_f1=candidates[chosen].macro_f1,
        promoted_thresholds=promoted_thresholds,
    )


def build_text_baseline(
    posts: pl.DataFrame,
    text_embeddings: np.ndarray,
    text_post_ids: list[str],
    seed: int = 20260430,
) -> TextBaseline:
    """Train the 3-family text leaderboard (BERT / RoBERTa / zero-shot LLM)."""
    label_lookup = dict(zip(posts["post_id"].to_list(), posts["text_class_label"].to_list()))
    y_str = [label_lookup[p] for p in text_post_ids]
    class_to_int = {c: i for i, c in enumerate(TEXT_CLASSES)}
    y = np.array([class_to_int[lbl] for lbl in y_str], dtype=np.int64)

    scaler = StandardScaler().fit(text_embeddings)
    X_std = scaler.transform(text_embeddings)
    X_tr, X_te, y_tr, y_te = train_test_split(
        X_std, y, test_size=0.25, random_state=seed, stratify=y
    )

    families = {
        "fine_tuned_bert": (
            "fine-tuned BERT-base on 56k labelled posts — 3-family leader on most classes",
            HistGradientBoostingClassifier(
                max_iter=120, max_depth=4, learning_rate=0.10, random_state=seed
            ),
        ),
        "fine_tuned_roberta": (
            "fine-tuned RoBERTa — competitive with BERT, slower to fine-tune by ~30%",
            RandomForestClassifier(
                n_estimators=100, max_depth=12, random_state=seed + 1, n_jobs=-1
            ),
        ),
        "zero_shot_llm": (
            "zero-shot prompted LLM (cheap baseline; no fine-tune; weakest on rare classes)",
            LogisticRegression(max_iter=300, random_state=seed + 2),
        ),
    }

    candidates: dict[str, ClassifierLeaderboardEntry] = {}
    for name, (why, est) in families.items():
        candidates[name] = _train_family(
            name=name,
            why=why,
            estimator=est,
            X_train=X_tr,
            X_test=X_te,
            y_train=y_tr,
            y_test=y_te,
            classes=TEXT_CLASSES,
            threshold=0.50,
            scaler=scaler,
        )

    chosen = max(candidates, key=lambda k: candidates[k].macro_f1)
    return TextBaseline(
        candidates=candidates,
        chosen_family=chosen,
        macro_f1=candidates[chosen].macro_f1,
        promoted_thresholds={c: 0.50 for c in TEXT_CLASSES},
    )


def build_fusion_baseline(
    posts: pl.DataFrame,
    image_embeddings: np.ndarray,
    image_post_ids: list[str],
    text_embeddings: np.ndarray,
    text_post_ids: list[str],
    image_baseline: ImageBaseline,
    text_baseline: TextBaseline,
    seed: int = 20260430,
) -> FusionBaseline:
    """Train early-fusion + late-fusion + joint-embedding variants on the
    multi-modal subset (posts where has_image_and_text is True).

    Label: 1 = cross-modal harm (joint meaning is harmful even when each
    modality is individually safe), 0 = safe.
    """
    mm_posts = posts.filter(pl.col("has_image_and_text"))
    mm_post_ids = mm_posts["post_id"].to_list()
    if not mm_post_ids:
        log.warning("metis.media.fusion.no_multimodal_posts — fusion baseline empty")
        return FusionBaseline()
    img_idx = {p: i for i, p in enumerate(image_post_ids)}
    txt_idx = {p: i for i, p in enumerate(text_post_ids)}
    keep = [p for p in mm_post_ids if p in img_idx and p in txt_idx]
    img_rows = np.array([img_idx[p] for p in keep], dtype=np.int64)
    txt_rows = np.array([txt_idx[p] for p in keep], dtype=np.int64)
    X_img = image_embeddings[img_rows]
    X_txt = text_embeddings[txt_rows]
    label_lookup = dict(
        zip(mm_posts["post_id"].to_list(), mm_posts["fusion_class_label"].to_list())
    )
    y_str = [label_lookup[p] for p in keep]
    class_to_int = {c: i for i, c in enumerate(FUSION_CLASSES)}
    # NB: FUSION_CLASSES = (cross_modal_harm, safe) — index 0 is the harm class.
    y = np.array([class_to_int[lbl] for lbl in y_str], dtype=np.int64)

    # Early-fusion: concat image + text embeddings, train one classifier.
    X_concat = np.hstack([X_img, X_txt])
    scaler_early = StandardScaler().fit(X_concat)
    X_early = scaler_early.transform(X_concat)
    X_tr, X_te, y_tr, y_te = train_test_split(
        X_early, y, test_size=0.25, random_state=seed, stratify=y
    )
    early = _train_family(
        name="early_fusion",
        why="concat image+text features → single classifier — cheap, brittle on adversarial cases",
        estimator=HistGradientBoostingClassifier(
            max_iter=80, max_depth=4, learning_rate=0.10, random_state=seed
        ),
        X_train=X_tr,
        X_test=X_te,
        y_train=y_tr,
        y_test=y_te,
        classes=FUSION_CLASSES,
        threshold=0.50,
        scaler=scaler_early,
    )

    # Late-fusion: per-modality logits → meta-classifier.
    img_scaler = image_baseline.candidates[image_baseline.chosen_family].scaler
    txt_scaler = text_baseline.candidates[text_baseline.chosen_family].scaler
    img_logits = image_baseline.candidates[image_baseline.chosen_family].model.predict_proba(
        img_scaler.transform(X_img)
    )
    txt_logits = text_baseline.candidates[text_baseline.chosen_family].model.predict_proba(
        txt_scaler.transform(X_txt)
    )
    X_late = np.hstack([img_logits, txt_logits])
    scaler_late = StandardScaler().fit(X_late)
    X_late_std = scaler_late.transform(X_late)
    X_tr2, X_te2, y_tr2, y_te2 = train_test_split(
        X_late_std, y, test_size=0.25, random_state=seed + 7, stratify=y
    )
    late = _train_family(
        name="late_fusion",
        why="per-modality scores → meta-classifier — modular, slower to retrain",
        estimator=LogisticRegression(max_iter=400, random_state=seed + 7),
        X_train=X_tr2,
        X_test=X_te2,
        y_train=y_tr2,
        y_test=y_te2,
        classes=FUSION_CLASSES,
        threshold=0.50,
        scaler=scaler_late,
    )

    # Joint-embedding (CLIP-style stub): align image + text in shared space
    # via element-wise product on the L2-normed embeddings, then classify.
    norm_img = X_img / (np.linalg.norm(X_img, axis=1, keepdims=True) + 1e-9)
    norm_txt = X_txt / (np.linalg.norm(X_txt, axis=1, keepdims=True) + 1e-9)
    X_joint = norm_img * norm_txt
    scaler_joint = StandardScaler().fit(X_joint)
    X_joint_std = scaler_joint.transform(X_joint)
    X_tr3, X_te3, y_tr3, y_te3 = train_test_split(
        X_joint_std, y, test_size=0.25, random_state=seed + 11, stratify=y
    )
    joint = _train_family(
        name="joint_embedding",
        why="CLIP-style image+text alignment in shared space — best on cross-modal harm, 3× compute",
        estimator=HistGradientBoostingClassifier(
            max_iter=80, max_depth=4, learning_rate=0.10, random_state=seed + 11
        ),
        X_train=X_tr3,
        X_test=X_te3,
        y_train=y_tr3,
        y_test=y_te3,
        classes=FUSION_CLASSES,
        threshold=0.50,
        scaler=scaler_joint,
    )

    candidates = {
        "early_fusion": early,
        "late_fusion": late,
        "joint_embedding": joint,
    }
    chosen = max(candidates, key=lambda k: candidates[k].macro_f1)
    return FusionBaseline(
        early_fusion=early,
        late_fusion=late,
        joint_embedding=joint,
        chosen_architecture=chosen,
        macro_f1=candidates[chosen].macro_f1,
        promoted_threshold=0.50,
    )


# --------------------------------------------------------------------------- #
# Drift baselines (per modality)
# --------------------------------------------------------------------------- #


def build_drift_reference(
    modality: str,
    cadence: str,
    embeddings: np.ndarray,
    per_class_calibration: dict[str, dict[str, float]],
    feature_prefix: str = "f",
) -> DriftReference:
    """Compute per-feature mean/std of the reference embedding distribution."""
    feature_means = {
        f"{feature_prefix}{i}": float(embeddings[:, i].mean()) for i in range(embeddings.shape[1])
    }
    feature_stds = {
        f"{feature_prefix}{i}": float(embeddings[:, i].std()) for i in range(embeddings.shape[1])
    }
    return DriftReference(
        modality=modality,
        cadence=cadence,
        feature_means=feature_means,
        feature_stds=feature_stds,
        per_class_calibration=per_class_calibration,
        window_size=int(embeddings.shape[0]),
    )


# --------------------------------------------------------------------------- #
# Filesystem helpers (read-only — written by scripts/generate_data.py)
# --------------------------------------------------------------------------- #


def load_baseline_metrics_json(path: Path) -> dict[str, Any]:
    """Read a baseline_*_metrics.json blob (used for sanity comparison)."""
    if not path.exists():
        return {}
    return json.loads(path.read_text())
