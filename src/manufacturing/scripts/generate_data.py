#!/usr/bin/env python3
# Copyright (c) 2026 Terrene Foundation (Singapore CLG)
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
"""LumenCircuit Industrial AI — deterministic data generator.

Materialises:
  - data/boards_labelled.csv  (800 PCB inspection events)
  - data/images_pcb/<id>.png  (800 procedural 32x32 RGB PNGs)
  - data/images_safety/<id>.png  (200 procedural 32x32 RGB PNGs)
  - data/sensor_stream.csv  (30 days × 10 machines × 1-min cadence)
  - data/rl_episodes.json  (10,000 episodes × 3 policies)
  - data/baseline_vision_metrics.json  (per-arch P/R/F1 hint)
  - data/baseline_predmaint_metrics.json
  - data/baseline_rl_metrics.json
  - data/drift_baseline.json
  - data/scenarios/mom_wsh_shadow_mandate.json
  - data/scenarios/q4_demand_drift.json

Seed: 20260504. Re-run is safe — outputs are deterministic.

Run from the repo root:
    .venv/bin/python src/manufacturing/scripts/generate_data.py
"""

from __future__ import annotations

import csv
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np

SEED = 20260504
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
IMAGES_PCB = DATA / "images_pcb"
IMAGES_SAFETY = DATA / "images_safety"
SCENARIOS = DATA / "scenarios"

VISION_CLASSES = ("good", "minor_defect", "major_defect", "safety_critical_defect")
DEFECT_MODES = (
    "none",
    "solder_bridge",
    "missing_component",
    "tombstone",
    "cold_joint",
    "scratch",
    "contamination",
)
CLASS_DISTRIBUTION = {
    "good": 0.62,
    "minor_defect": 0.22,
    "major_defect": 0.12,
    "safety_critical_defect": 0.04,
}
DEFECT_MODE_BY_CLASS: dict[str, tuple[tuple[str, float], ...]] = {
    "good": (("none", 1.0),),
    "minor_defect": (("scratch", 0.5), ("contamination", 0.3), ("cold_joint", 0.2)),
    "major_defect": (
        ("solder_bridge", 0.4),
        ("missing_component", 0.35),
        ("tombstone", 0.25),
    ),
    "safety_critical_defect": (
        ("solder_bridge", 0.45),
        ("missing_component", 0.35),
        ("tombstone", 0.20),
    ),
}

# Per-class base color (RGB) for procedural PNGs
CLASS_BASE_COLOR: dict[str, tuple[int, int, int]] = {
    "good": (90, 160, 90),
    "minor_defect": (200, 200, 80),
    "major_defect": (220, 110, 60),
    "safety_critical_defect": (220, 50, 50),
}


def _png_bytes(rgb: tuple[int, int, int], noise_rng: np.random.Generator, size: int = 32) -> bytes:
    """Generate a minimal PNG (RGB, no alpha) with per-pixel noise around base color."""
    import struct
    import zlib

    w = h = size
    raw = bytearray()
    for _y in range(h):
        raw.append(0)  # filter type 0 (None) per scanline
        for _x in range(w):
            for c in rgb:
                jitter = int(noise_rng.normal(0, 25))
                v = max(0, min(255, c + jitter))
                raw.append(v)
    raw_bytes = bytes(raw)
    compressed = zlib.compress(raw_bytes, 6)

    def chunk(name: bytes, body: bytes) -> bytes:
        crc = zlib.crc32(name + body) & 0xFFFFFFFF
        return struct.pack(">I", len(body)) + name + body + struct.pack(">I", crc)

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)  # 8-bit RGB
    return sig + chunk(b"IHDR", ihdr) + chunk(b"IDAT", compressed) + chunk(b"IEND", b"")


def _ensure_dirs() -> None:
    for p in (DATA, IMAGES_PCB, IMAGES_SAFETY, SCENARIOS):
        p.mkdir(parents=True, exist_ok=True)


def generate_boards(n: int = 800) -> list[dict]:
    rng = np.random.default_rng(SEED)
    boards: list[dict] = []
    classes = list(CLASS_DISTRIBUTION.keys())
    weights = list(CLASS_DISTRIBUTION.values())
    for i in range(n):
        cls = rng.choice(classes, p=weights)
        modes = DEFECT_MODE_BY_CLASS[cls]
        mode_choice = rng.choice([m[0] for m in modes], p=[m[1] for m in modes])
        ipc_class = "Class_3" if rng.random() < 0.6 else "Class_2"
        # AOI baseline: 78% recall on true defects, 12% FP rate
        truly_defective = cls != "good"
        if truly_defective:
            aoi_flag = bool(rng.random() < 0.78)
        else:
            aoi_flag = bool(rng.random() < 0.12)
        boards.append(
            {
                "image_id": f"board_{i:06d}",
                "class_label": cls,
                "defect_mode": mode_choice,
                "ipc_class": ipc_class,
                "aoi_flag": int(aoi_flag),
                "manual_decision": "fail" if truly_defective else "pass",
            }
        )
    return boards


def write_boards_csv(boards: list[dict]) -> None:
    path = DATA / "boards_labelled.csv"
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(boards[0].keys()))
        w.writeheader()
        w.writerows(boards)
    print(f"  wrote {path.name} ({len(boards)} rows)")


def write_pcb_images(boards: list[dict]) -> None:
    rng = np.random.default_rng(SEED + 1)
    for b in boards:
        path = IMAGES_PCB / f"{b['image_id']}.png"
        png = _png_bytes(CLASS_BASE_COLOR[b["class_label"]], rng)
        path.write_bytes(png)
    print(f"  wrote {len(boards)} PCB images -> {IMAGES_PCB.relative_to(ROOT.parent)}")


def write_safety_images(n: int = 200) -> None:
    rng = np.random.default_rng(SEED + 2)
    rows: list[dict] = []
    for i in range(n):
        ppe = bool(rng.random() < 0.65)
        zone = bool(rng.random() < 0.85)  # True = clear, False = breach
        col = (90, 160, 90) if (ppe and zone) else (220, 50, 50)
        path = IMAGES_SAFETY / f"safety_{i:04d}.png"
        path.write_bytes(_png_bytes(col, rng))
        rows.append(
            {
                "image_id": f"safety_{i:04d}",
                "ppe_present": int(ppe),
                "restricted_zone_clear": int(zone),
            }
        )
    with (DATA / "safety_labelled.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["image_id", "ppe_present", "restricted_zone_clear"])
        w.writeheader()
        w.writerows(rows)
    print(f"  wrote {n} safety images + safety_labelled.csv")


def generate_sensor_stream(
    n_machines: int = 10, n_days: int = 30, cadence_min: int = 1
) -> list[dict]:
    rng = np.random.default_rng(SEED + 3)
    rows: list[dict] = []
    start = datetime(2026, 4, 1, tzinfo=timezone.utc)
    # 4 of 10 machines fail; pick failure days uniformly across the window.
    failing_machines = rng.choice(n_machines, size=4, replace=False)
    failure_day = {int(m): int(rng.integers(low=10, high=n_days)) for m in failing_machines}
    samples_per_day = (24 * 60) // cadence_min
    for m in range(n_machines):
        is_failing = m in failure_day
        fail_at = failure_day.get(m, 9999)
        # Baseline drifts gradually as failure approaches.
        for day in range(n_days):
            for s in range(samples_per_day):
                ts = start + timedelta(minutes=day * 24 * 60 + s * cadence_min)
                # Severity ramp: 0 far from failure, up to 1.0 the day before.
                if is_failing and day < fail_at:
                    severity = max(0.0, (day - (fail_at - 7)) / 7.0)
                else:
                    severity = 0.0
                vibration = float(rng.normal(0.50 + severity * 0.40, 0.05))
                current = float(rng.normal(2.30 + severity * 0.30, 0.08))
                temp = float(rng.normal(45.0 + severity * 8.0, 1.2))
                cycle = int(s + day * samples_per_day + rng.integers(0, 2))
                rows.append(
                    {
                        "timestamp": ts.isoformat(),
                        "machine_id": f"smt_{m:02d}",
                        "vibration": round(vibration, 4),
                        "current": round(current, 4),
                        "temperature": round(temp, 3),
                        "cycle_count": cycle,
                        "fails_in_30d": int(is_failing),
                        "days_to_failure": int(fail_at - day) if is_failing else 9999,
                    }
                )
    return rows


def write_sensor_csv(rows: list[dict]) -> None:
    path = DATA / "sensor_stream.csv"
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"  wrote {path.name} ({len(rows):,} rows)")


def generate_rl_episodes(n_per_policy: int = 10000) -> dict[str, list[dict[str, float]]]:
    rng = np.random.default_rng(SEED + 4)
    out: dict[str, list[dict[str, float]]] = {}
    # Policy parameters chosen so the leaderboard ranks PPO > DQN > Random
    # on the default reward weights, with PPO producing zero hard-floor
    # violations and Random producing many.
    policy_specs = {
        "ppo_continuous": {
            "throughput_mean": 54.0,
            "throughput_sd": 2.0,
            "defect_rate_mean": 0.018,
            "defect_rate_sd": 0.005,
            "energy_mean": 0.062,
            "energy_sd": 0.005,
            "safety_violation_rate": 0.0001,
            "max_temp_mean": 240.0,
            "max_temp_sd": 4.0,
        },
        "dqn_discrete": {
            "throughput_mean": 51.0,
            "throughput_sd": 3.0,
            "defect_rate_mean": 0.025,
            "defect_rate_sd": 0.008,
            "energy_mean": 0.068,
            "energy_sd": 0.008,
            "safety_violation_rate": 0.001,
            "max_temp_mean": 245.0,
            "max_temp_sd": 6.0,
        },
        "random_baseline": {
            "throughput_mean": 38.0,
            "throughput_sd": 8.0,
            "defect_rate_mean": 0.084,
            "defect_rate_sd": 0.030,
            "energy_mean": 0.092,
            "energy_sd": 0.020,
            "safety_violation_rate": 0.040,
            "max_temp_mean": 252.0,
            "max_temp_sd": 12.0,
        },
    }
    for policy, p in policy_specs.items():
        episodes = []
        for _ in range(n_per_policy):
            thr = float(np.clip(rng.normal(p["throughput_mean"], p["throughput_sd"]), 0.0, 90.0))
            defect = float(
                np.clip(rng.normal(p["defect_rate_mean"], p["defect_rate_sd"]), 0.0, 0.5)
            )
            energy = float(np.clip(rng.normal(p["energy_mean"], p["energy_sd"]), 0.0, 0.30))
            safety = int(rng.random() < p["safety_violation_rate"])
            line_speed = float(
                np.clip(rng.normal(p["throughput_mean"] + 4.0, p["throughput_sd"]), 0.0, 95.0)
            )
            max_temp = float(
                np.clip(rng.normal(p["max_temp_mean"], p["max_temp_sd"]), 200.0, 280.0)
            )
            ret = 1.0 * thr - 5.0 * defect - 0.10 * energy - 0.50 * safety
            episodes.append(
                {
                    "throughput": round(thr, 3),
                    "defect_rate": round(defect, 4),
                    "energy_per_board": round(energy, 4),
                    "safety_violation": float(safety),
                    "line_speed": round(line_speed, 3),
                    "max_zone_temp": round(max_temp, 3),
                    "return": round(ret, 3),
                }
            )
        out[policy] = episodes
    return out


def write_rl_json(eps: dict[str, list[dict[str, float]]]) -> None:
    path = DATA / "rl_episodes.json"
    path.write_text(json.dumps(eps))
    total = sum(len(v) for v in eps.values())
    print(f"  wrote {path.name} ({total:,} episodes across {len(eps)} policies)")


def write_baseline_metrics_hints() -> None:
    """Pedagogical hint files — NOT load-bearing; backend re-trains live."""
    (DATA / "baseline_vision_metrics.json").write_text(
        json.dumps(
            {
                "expected_leaderboard_ranking": [
                    "resnet50_lr_head",
                    "efficientnet_b0_rf_head",
                    "vit_small_gbm_head",
                ],
                "macro_f1_band": [0.55, 0.92],
                "rationale": "ResNet wins at 800-image scale; ViT undertrained on small data.",
            },
            indent=2,
        )
    )
    (DATA / "baseline_predmaint_metrics.json").write_text(
        json.dumps(
            {
                "expected_leaderboard_ranking": [
                    "lightgbm_features",
                    "lstm_sequence",
                    "survival_forest_tte",
                ],
                "windows": [3, 7, 14],
                "rationale": "LightGBM on hand-engineered features wins at 10-machine scale.",
            },
            indent=2,
        )
    )
    (DATA / "baseline_rl_metrics.json").write_text(
        json.dumps(
            {
                "expected_leaderboard_ranking": [
                    "ppo_continuous",
                    "dqn_discrete",
                    "random_baseline",
                ],
                "rationale": "PPO produces zero hard-floor violations; Random hits the floor frequently.",
            },
            indent=2,
        )
    )
    (DATA / "drift_baseline.json").write_text(
        json.dumps(
            {
                "vision": {"cadence": "weekly", "registered": True},
                "predmaint": {"cadence": "daily", "registered": True},
                "rl": {"cadence": "per_deployment", "registered": True},
            },
            indent=2,
        )
    )
    print("  wrote 4 baseline_*.json hint files")


def write_scenarios() -> None:
    (SCENARIOS / "mom_wsh_shadow_mandate.json").write_text(
        json.dumps(
            {
                "trigger": "MOM/WSH Inspectorate near-miss audit",
                "effective_iso": "2026-04-30T00:00:00+08:00",
                "expires_iso": "2026-07-30T00:00:00+08:00",
                "scope": [
                    "agent.setpoint_adjustment if line_speed > 60 boards/min OR reflow zone > 250 °C",
                    "agent.safety_alert if restricted-zone access pattern detected",
                ],
                "mandate": "shadow-mode only — recommend, human confirms",
                "rationale": (
                    "Following near-miss at peer fabricator (industry-wide notice): "
                    "any agent action affecting safety-relevant parameters MUST run in "
                    "shadow mode for 90 days while MOM completes its audit."
                ),
                "estimated_compliance_shadow_price_dollars_per_day": 15000,
            },
            indent=2,
        )
    )
    (SCENARIOS / "q4_demand_drift.json").write_text(
        json.dumps(
            {
                "trigger": "Q4 automotive ramp + medical certification cycle",
                "effective_iso": "2026-10-01T00:00:00+08:00",
                "expires_iso": "2026-12-31T00:00:00+08:00",
                "modality_affected": "predmaint",
                "expected_psi_lift": 0.30,
                "rationale": (
                    "Throughput target rises ~22% in Q4; sensor distributions shift outside "
                    "the recent_30d window. Drift monitor MUST flag this without auto-retraining "
                    "(seasonal exclusion in Phase 13)."
                ),
            },
            indent=2,
        )
    )
    print("  wrote 2 scenario files")


def main() -> None:
    print("metis.manufacturing.generate_data starting (seed=%d)" % SEED)
    _ensure_dirs()
    boards = generate_boards()
    write_boards_csv(boards)
    write_pcb_images(boards)
    write_safety_images()
    sensor_rows = generate_sensor_stream()
    write_sensor_csv(sensor_rows)
    eps = generate_rl_episodes()
    write_rl_json(eps)
    write_baseline_metrics_hints()
    write_scenarios()
    print("metis.manufacturing.generate_data ok")


if __name__ == "__main__":
    main()
