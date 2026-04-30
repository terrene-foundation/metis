# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Fusion moderation endpoints — Sprint 3 of the Playbook (Multi-Modal · Decide).

Cross-modal harm scoring on the multi-modal subset (~8,000 image+text
memes). Three architectures are pre-trained at startup:
  - early_fusion    — concat image+text features → single classifier
  - late_fusion     — per-modality scores → meta-classifier
  - joint_embedding — CLIP-style alignment in shared space

The cross_modal_harm score disagrees with per-modality scores when the
joint meaning is harmful (cute-puppy + "destroy all humans" caption).
This is the architecture-choice surface for Phase 5 Multi-Modal.

Endpoints
---------
- `GET  /moderate/fusion/leaderboard`   — three architectures + macro_f1
- `POST /moderate/fusion/score`         — cross_modal_harm score for a post_id
- `GET  /moderate/fusion/architecture`  — current chosen architecture + stage
- `POST /moderate/fusion/architecture`  — switch architecture (early|late|joint)
- `GET  /moderate/fusion/threshold`     — current promoted_threshold
- `POST /moderate/fusion/threshold`     — set promoted_threshold + justification
- `POST /moderate/fusion/promote`       — promote chosen architecture to shadow|production
- `GET  /moderate/fusion/registry`      — promotion + threshold-change history
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..config import load_settings
from ..ml_context import (
    FUSION_CLASSES,
    get_context,
    synthesise_embeddings,
)

router = APIRouter()

VALID_ARCHITECTURES = ("early_fusion", "late_fusion", "joint_embedding")


# --------------------------------------------------------------------------- #
# Persistence
# --------------------------------------------------------------------------- #


def _threshold_path() -> Path:
    return load_settings().workspace_root / "fusion_threshold.json"


def _registry_path() -> Path:
    return load_settings().workspace_root / "fusion_registry.json"


def _default_threshold() -> dict:
    return {
        "threshold": 0.50,
        "justification": "default — student has not set",
        "updated_at": None,
    }


def _load_threshold() -> dict:
    p = _threshold_path()
    if p.exists():
        return json.loads(p.read_text())
    return _default_threshold()


def _save_threshold(state: dict) -> None:
    _threshold_path().parent.mkdir(parents=True, exist_ok=True)
    _threshold_path().write_text(json.dumps(state, indent=2))


def _load_registry() -> list[dict]:
    p = _registry_path()
    if p.exists():
        return json.loads(p.read_text())
    return []


def _append_registry(entry: dict) -> list[dict]:
    history = _load_registry()
    history.append(entry)
    _registry_path().parent.mkdir(parents=True, exist_ok=True)
    _registry_path().write_text(json.dumps(history, indent=2))
    return history


# --------------------------------------------------------------------------- #
# Serialisation
# --------------------------------------------------------------------------- #


def _serializable_entry(entry: Any) -> dict:
    return {
        "family": entry.family,
        "family_why": entry.family_why,
        "macro_f1": entry.macro_f1,
        "per_class": entry.per_class,
        "threshold": entry.threshold,
    }


def _entry_for(arch: str, fb: Any) -> Any:
    return {
        "early_fusion": fb.early_fusion,
        "late_fusion": fb.late_fusion,
        "joint_embedding": fb.joint_embedding,
    }[arch]


# --------------------------------------------------------------------------- #
# Request models
# --------------------------------------------------------------------------- #


class ScoreRequest(BaseModel):
    post_id: str = Field(
        description="post_id present in posts_labelled.csv has_image_and_text rows"
    )


class ArchitectureRequest(BaseModel):
    architecture: str = Field(description=f"one of: {', '.join(VALID_ARCHITECTURES)}")
    rationale: str = Field(min_length=10)


class ThresholdRequest(BaseModel):
    threshold: float = Field(ge=0.0, le=1.0)
    justification: str = Field(min_length=10)


class PromoteRequest(BaseModel):
    architecture: str = Field(description=f"one of: {', '.join(VALID_ARCHITECTURES)}")
    stage: str = Field(description="shadow | production")
    rationale: str = Field(min_length=10)


# --------------------------------------------------------------------------- #
# Endpoints
# --------------------------------------------------------------------------- #


@router.get("/leaderboard")
def leaderboard() -> dict:
    """Three fusion architectures with their macro_f1 + per-class metrics."""
    ctx = get_context()
    fb = ctx.fusion_baseline
    out: dict[str, Any] = {}
    for arch in VALID_ARCHITECTURES:
        entry = _entry_for(arch, fb)
        if entry is None:
            out[arch] = {"available": False}
        else:
            out[arch] = {"available": True, **_serializable_entry(entry)}
    return {
        "modality": "fusion",
        "classes": list(FUSION_CLASSES),
        "label_definition": (
            "Binary cross-modal harm: 1 = joint meaning is harmful even when "
            "individual modalities are individually safe (the meme attack "
            "class); 0 = safe."
        ),
        "chosen_architecture": fb.chosen_architecture,
        "chosen_macro_f1": fb.macro_f1,
        "stage": fb.stage,
        "candidates": out,
        "note": (
            "Phase 5 Multi-Modal decision: pick early|late|joint on coverage "
            "gain × dollar value vs compute cost delta. Joint embedding "
            "is 3× more expensive than either modality alone."
        ),
    }


@router.post("/score")
def score(req: ScoreRequest) -> dict:
    """Return cross_modal_harm score for one multi-modal post.

    Uses the currently-chosen architecture from the in-memory baseline.
    """
    ctx = get_context()
    fb = ctx.fusion_baseline
    if req.post_id not in set(ctx.fusion_post_ids):
        raise HTTPException(
            404,
            f"post_id {req.post_id!r} is not multi-modal; check has_image_and_text",
        )

    image_label_lookup = dict(
        zip(ctx.posts["post_id"].to_list(), ctx.posts["image_class_label"].to_list())
    )
    text_label_lookup = dict(
        zip(ctx.posts["post_id"].to_list(), ctx.posts["text_class_label"].to_list())
    )
    fusion_label_lookup = dict(
        zip(ctx.posts["post_id"].to_list(), ctx.posts["fusion_class_label"].to_list())
    )

    img_emb = synthesise_embeddings(
        [req.post_id], [image_label_lookup[req.post_id]], modality="image"
    )
    txt_emb = synthesise_embeddings(
        [req.post_id], [text_label_lookup[req.post_id]], modality="text"
    )

    arch = fb.chosen_architecture
    entry = _entry_for(arch, fb)
    if entry is None:
        raise HTTPException(
            500,
            f"architecture {arch!r} has no trained model — startup may have failed on the multi-modal subset",
        )

    if arch == "early_fusion":
        X = np.hstack([img_emb, txt_emb])
    elif arch == "late_fusion":
        chosen_img = ctx.image_baseline.candidates[ctx.image_baseline.chosen_family]
        chosen_txt = ctx.text_baseline.candidates[ctx.text_baseline.chosen_family]
        img_logits = chosen_img.model.predict_proba(chosen_img.scaler.transform(img_emb))
        txt_logits = chosen_txt.model.predict_proba(chosen_txt.scaler.transform(txt_emb))
        X = np.hstack([img_logits, txt_logits])
    else:  # joint_embedding
        norm_img = img_emb / (np.linalg.norm(img_emb, axis=1, keepdims=True) + 1e-9)
        norm_txt = txt_emb / (np.linalg.norm(txt_emb, axis=1, keepdims=True) + 1e-9)
        X = norm_img * norm_txt

    X_std = entry.scaler.transform(X)
    proba = entry.model.predict_proba(X_std)[0]
    if proba.shape[0] < len(FUSION_CLASSES):
        full = np.zeros(len(FUSION_CLASSES), dtype=np.float32)
        for src_idx, cls_int in enumerate(entry.model.classes_):
            full[int(cls_int)] = proba[src_idx]
        proba = full

    harm_p = float(proba[FUSION_CLASSES.index("cross_modal_harm")])
    state = _load_threshold()
    tau = float(state["threshold"])
    decision = "auto_route_human_review" if harm_p >= tau else "allow"
    return {
        "modality": "fusion",
        "architecture": arch,
        "post_id": req.post_id,
        "ground_truth_label": fusion_label_lookup[req.post_id],
        "individual_modality_labels": {
            "image": image_label_lookup[req.post_id],
            "text": text_label_lookup[req.post_id],
        },
        "cross_modal_harm_probability": round(harm_p, 4),
        "threshold": tau,
        "decision": decision,
        "explanation": (
            "cross_modal_harm exceeds the per-modality scores when joint "
            "meaning is harmful but individual scores are individually safe — "
            "the meme-attack class."
        ),
    }


@router.get("/architecture")
def get_architecture() -> dict:
    ctx = get_context()
    fb = ctx.fusion_baseline
    return {
        "modality": "fusion",
        "chosen_architecture": fb.chosen_architecture,
        "stage": fb.stage,
        "macro_f1": fb.macro_f1,
        "available": [arch for arch in VALID_ARCHITECTURES if _entry_for(arch, fb) is not None],
    }


@router.post("/architecture")
def set_architecture(req: ArchitectureRequest) -> dict:
    if req.architecture not in VALID_ARCHITECTURES:
        raise HTTPException(
            422,
            f"unknown architecture {req.architecture!r}; expected one of {list(VALID_ARCHITECTURES)}",
        )
    ctx = get_context()
    fb = ctx.fusion_baseline
    entry = _entry_for(req.architecture, fb)
    if entry is None:
        raise HTTPException(
            422,
            f"architecture {req.architecture!r} not available — only fitted architectures may be selected",
        )
    fb.chosen_architecture = req.architecture
    fb.macro_f1 = entry.macro_f1
    _append_registry(
        {
            "event": "architecture_set",
            "architecture": req.architecture,
            "macro_f1": entry.macro_f1,
            "rationale": req.rationale,
            "at": datetime.now(timezone.utc).isoformat(),
        }
    )
    return {
        "modality": "fusion",
        "chosen_architecture": req.architecture,
        "macro_f1": entry.macro_f1,
        "stage": fb.stage,
    }


@router.get("/threshold")
def get_threshold() -> dict:
    return _load_threshold()


@router.post("/threshold")
def set_threshold(req: ThresholdRequest) -> dict:
    state = {
        "threshold": req.threshold,
        "justification": req.justification,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    _save_threshold(state)
    _append_registry(
        {
            "event": "threshold_set",
            "threshold": req.threshold,
            "justification": req.justification,
            "at": state["updated_at"],
        }
    )
    return state


@router.post("/promote")
def promote(req: PromoteRequest) -> dict:
    if req.stage not in {"shadow", "production"}:
        raise HTTPException(422, f"stage must be 'shadow' or 'production', got {req.stage!r}")
    if req.architecture not in VALID_ARCHITECTURES:
        raise HTTPException(
            422,
            f"unknown architecture {req.architecture!r}; expected one of {list(VALID_ARCHITECTURES)}",
        )
    ctx = get_context()
    fb = ctx.fusion_baseline
    entry = _entry_for(req.architecture, fb)
    if entry is None:
        raise HTTPException(
            422,
            f"architecture {req.architecture!r} not available — startup did not fit this variant",
        )
    fb.chosen_architecture = req.architecture
    fb.macro_f1 = entry.macro_f1
    fb.stage = req.stage
    history = _append_registry(
        {
            "event": "promote",
            "architecture": req.architecture,
            "stage": req.stage,
            "rationale": req.rationale,
            "at": datetime.now(timezone.utc).isoformat(),
        }
    )
    return {
        "modality": "fusion",
        "promoted_architecture": req.architecture,
        "stage": req.stage,
        "history_length": len(history),
    }


@router.get("/registry")
def registry() -> dict:
    history = _load_registry()
    return {
        "modality": "fusion",
        "history_length": len(history),
        "history": history,
    }
