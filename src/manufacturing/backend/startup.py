# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""Startup: load boards + sensor + RL episodes, train baselines, register drift refs."""

from __future__ import annotations

import json
import logging
import warnings
from pathlib import Path

import numpy as np
import polars as pl
from sklearn.exceptions import ConvergenceWarning

# Suppress sklearn numerical warnings from synthetic-embedding fits — same
# rationale as Week 6: outputs are numerically valid; warnings clutter the
# student log on a synthetic dataset.
warnings.filterwarnings("ignore", category=RuntimeWarning, module="sklearn")
warnings.filterwarnings("ignore", category=RuntimeWarning, module="numpy")
warnings.filterwarnings("ignore", category=ConvergenceWarning)

from .config import load_settings
from .ml_context import (
    AGENT_TASK_CLASSES,
    AgentPolicy,
    MLContext,
    PREDMAINT_WINDOWS,
    VISION_ARCH_DIMS,
    VISION_CLASSES,
    build_drift_reference,
    build_predmaint_baseline,
    build_rl_baseline,
    build_vision_baseline,
    set_context,
    synthesise_image_embeddings,
)

log = logging.getLogger("metis.manufacturing.startup")


def _require(path: Path, label: str) -> None:
    if not path.exists():
        raise RuntimeError(
            f"{label} missing at {path} — run "
            f"`.venv/bin/python src/manufacturing/scripts/generate_data.py` "
            f"from the repo root to materialise the LumenCircuit dataset."
        )


def run_startup_sync() -> None:
    settings = load_settings()
    data_dir = settings.data_dir

    _require(data_dir / "boards_labelled.csv", "boards_labelled")
    _require(data_dir / "sensor_stream.csv", "sensor_stream")
    _require(data_dir / "rl_episodes.json", "rl_episodes")
    _require(data_dir / "baseline_vision_metrics.json", "baseline_vision_metrics")
    _require(data_dir / "baseline_predmaint_metrics.json", "baseline_predmaint_metrics")
    _require(data_dir / "baseline_rl_metrics.json", "baseline_rl_metrics")
    _require(data_dir / "drift_baseline.json", "drift_baseline")

    log.info("metis.manufacturing.startup.loading_boards")
    boards = pl.read_csv(data_dir / "boards_labelled.csv")
    log.info(
        "metis.manufacturing.startup.boards_loaded total=%d good=%d minor=%d major=%d critical=%d",
        len(boards),
        int((boards["class_label"] == "good").sum()),
        int((boards["class_label"] == "minor_defect").sum()),
        int((boards["class_label"] == "major_defect").sum()),
        int((boards["class_label"] == "safety_critical_defect").sum()),
    )

    log.info("metis.manufacturing.startup.loading_sensor_stream")
    sensor_stream = pl.read_csv(data_dir / "sensor_stream.csv")
    machine_ids = sorted(sensor_stream["machine_id"].unique().to_list())
    log.info(
        "metis.manufacturing.startup.sensor_loaded rows=%d machines=%d",
        len(sensor_stream),
        len(machine_ids),
    )

    log.info("metis.manufacturing.startup.loading_rl_episodes")
    rl_episodes = json.loads((data_dir / "rl_episodes.json").read_text())
    log.info(
        "metis.manufacturing.startup.rl_episodes_loaded ppo=%d dqn=%d random=%d",
        len(rl_episodes.get("ppo_continuous", [])),
        len(rl_episodes.get("dqn_discrete", [])),
        len(rl_episodes.get("random_baseline", [])),
    )

    image_ids = boards["image_id"].to_list()
    image_labels = boards["class_label"].to_list()
    log.info("metis.manufacturing.startup.synthesising_vision_embeddings (3 archs)")
    vision_embeddings: dict[str, np.ndarray] = {}
    for arch in VISION_ARCH_DIMS.keys():
        vision_embeddings[arch] = synthesise_image_embeddings(image_ids, image_labels, arch=arch)

    log.info("metis.manufacturing.startup.training_vision_baseline (3-arch leaderboard)")
    vision_baseline = build_vision_baseline(boards, vision_embeddings, image_ids)
    for arch, entry in vision_baseline.candidates.items():
        log.info(
            "metis.manufacturing.startup.vision[%s] macro_f1=%.3f",
            arch,
            entry.macro_f1,
        )
    log.info(
        "metis.manufacturing.startup.vision_chosen=%s macro_f1=%.3f",
        vision_baseline.chosen_arch,
        vision_baseline.macro_f1,
    )

    log.info("metis.manufacturing.startup.training_predmaint_baseline (3-family × 3-window)")
    predmaint_baseline = build_predmaint_baseline(sensor_stream, machine_ids)
    for window in PREDMAINT_WINDOWS:
        for family, entry in predmaint_baseline.leaderboard[window].items():
            log.info(
                "metis.manufacturing.startup.predmaint[%dd][%s] f1=%.3f brier=%.3f",
                window,
                family,
                entry.macro_f1,
                entry.brier,
            )
    log.info(
        "metis.manufacturing.startup.predmaint_chosen family=%s window=%dd",
        predmaint_baseline.chosen_family,
        predmaint_baseline.chosen_window,
    )

    log.info("metis.manufacturing.startup.aggregating_rl_baseline (3-policy leaderboard)")
    rl_baseline = build_rl_baseline(rl_episodes)
    for policy, entry in rl_baseline.leaderboard.items():
        log.info(
            "metis.manufacturing.startup.rl[%s] thr=%.2f defect=%.3f safety_violations=%d return=%.2f",
            policy,
            entry.throughput_boards_per_min,
            entry.defect_rate,
            entry.safety_violations,
            entry.avg_return,
        )

    log.info(
        "metis.manufacturing.startup.registering_drift_baselines (vision weekly / predmaint daily / rl per-deployment)"
    )
    chosen_vision_arch = vision_baseline.chosen_arch
    vision_calib = {
        c: {
            "brier": vision_baseline.candidates[chosen_vision_arch].per_class[c]["brier"],
            "ece": 0.0,
        }
        for c in VISION_CLASSES
    }
    predmaint_chosen_entry = predmaint_baseline.leaderboard[predmaint_baseline.chosen_window][
        predmaint_baseline.chosen_family
    ]
    predmaint_calib = {
        "fail_within_window": {
            "brier": predmaint_chosen_entry.brier,
            "ece": 0.0,
        }
    }
    rl_calib = {
        rl_baseline.chosen_policy: {
            "brier": 0.0,  # RL reward is not a probability; brier is N/A
            "ece": 0.0,
        }
    }

    # PredMaint reference embeddings: re-use the LightGBM hand-engineered feature
    # matrix at the chosen window so the drift signal is in the same feature space
    # the baseline trains on.
    from .ml_context import synthesise_sensor_window_features  # local import to avoid cycle

    predmaint_X, _ = synthesise_sensor_window_features(
        sensor_stream, machine_ids, predmaint_baseline.chosen_window
    )
    # RL reference: per-episode return distribution under the chosen reward.
    rl_returns = np.array(
        [e["return"] for e in rl_episodes.get(rl_baseline.chosen_policy, [])],
        dtype=np.float32,
    ).reshape(-1, 1)
    if rl_returns.size == 0:
        rl_returns = np.zeros((1, 1), dtype=np.float32)

    drift_baselines = {
        "vision": build_drift_reference(
            modality="vision",
            cadence="weekly",
            embeddings=vision_embeddings[chosen_vision_arch],
            per_class_calibration=vision_calib,
            feature_prefix="vis_f",
        ),
        "predmaint": build_drift_reference(
            modality="predmaint",
            cadence="daily",
            embeddings=predmaint_X,
            per_class_calibration=predmaint_calib,
            feature_prefix="pm_f",
        ),
        "rl": build_drift_reference(
            modality="rl",
            cadence="per_deployment",
            embeddings=rl_returns,
            per_class_calibration=rl_calib,
            feature_prefix="rl_f",
        ),
    }

    agent_policy = AgentPolicy(
        autonomy={
            "vision_triage": "recommend",
            "maintenance_scheduling": "recommend",
            "setpoint_adjustment": "shadow",
            "safety_alert": "shadow",
        },
        mom_mandate_active=False,
    )
    # Sanity invariant on agent task taxonomy.
    if set(agent_policy.autonomy.keys()) != set(AGENT_TASK_CLASSES):
        raise RuntimeError(
            f"agent_policy.autonomy keys {sorted(agent_policy.autonomy.keys())} != "
            f"AGENT_TASK_CLASSES {sorted(AGENT_TASK_CLASSES)}"
        )

    ctx = MLContext(
        boards=boards,
        sensor_stream=sensor_stream,
        rl_episodes=rl_episodes,
        vision_embeddings=vision_embeddings,
        vision_image_ids=image_ids,
        sensor_machine_ids=machine_ids,
        vision_baseline=vision_baseline,
        predmaint_baseline=predmaint_baseline,
        rl_baseline=rl_baseline,
        agent_policy=agent_policy,
        agent_audit=[],
        drift_baselines=drift_baselines,
    )
    set_context(ctx)
    if ctx.drift_baselines_registered != 3:
        raise RuntimeError(
            f"drift_baselines_registered={ctx.drift_baselines_registered}, expected 3 "
            f"(vision weekly / predmaint daily / rl per-deployment)"
        )
    log.info(
        "metis.manufacturing.startup.ready boards=%d sensor_rows=%d "
        "vision_baseline_f1=%.3f predmaint_baseline=%s/%dd rl_chosen=%s drift_refs=%d",
        len(boards),
        len(sensor_stream),
        vision_baseline.macro_f1,
        predmaint_baseline.chosen_family,
        predmaint_baseline.chosen_window,
        rl_baseline.chosen_policy,
        ctx.drift_baselines_registered,
    )


async def run_startup() -> None:
    run_startup_sync()
