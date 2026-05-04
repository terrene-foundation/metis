<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Workflow 3 — Sprint 1 Vision Boot (Transfer-learned PCB QC inspector)

> **What this step does:** Boot Sprint 1 by confirming preflight is green, copying skeleton journal files, confirming the vision endpoints are live, and getting a written orientation from Claude Code — before any Phase 1 prompt fires.
> **Why it exists:** A misconfigured or hallucinated boot wastes 15–20 minutes mid-sprint. Confirming endpoints live and skeleton files in place up front means Phase 1 starts on solid ground. Sprint 1 is the heaviest sprint — it covers Phases 1–8 (six of them shared with Sprint 2's first run).
> **You're here because:** The instructor approved your todo plan and Sprint 1 is ready to start.
> **Key concepts you'll see:** sprint boot, preflight, transfer-learning prohibition, edge-latency budget, cite-or-confirm, threshold shapes vs values

---

## 1. Boot the environment (one-time, paste-or-run)

Before anything else, in a separate terminal (NOT inside `claude`), confirm the scaffold runs and the viewer is up. These three commands are idempotent — re-run them any time something looks off.

```bash
# Preflight: green = scaffold loaded, baselines fitted, drift refs registered
.venv/bin/python src/manufacturing/scripts/preflight.py

# Backend: boots FastAPI on http://127.0.0.1:8000 (METIS_API_PORT to override)
src/manufacturing/scripts/run_backend.sh &

# Viewer: http://localhost:3000 — six cards polling backend every 5s
( cd apps/web/manufacturing && ./serve.sh ) &
```

If preflight exits non-zero, STOP and raise a hand. Do not try to debug the scaffold.

---

## 2. Paste this into Claude Code

**Universal core** (transfers to any ML project):

```
I'm entering /implement for a transfer-learning sprint. Someone pre-built
the scaffold before me. My job in this sprint is to decide the chosen
architecture, the per-class auto-pass thresholds, defend each in dollar
terms, and sign the deployment gate.

Before I start the phase walk, I need you to:

1. Copy the sprint skeletons from journal/skeletons/ into journal/ — one
   file per phase, named consistently. Leave the blanks blank; I fill them
   phase by phase. The skeleton inventory is in journal/skeletons/README.md.

2. Confirm the sprint endpoints are live by making GET requests to each.
   If any endpoint is not live, STOP and raise a hand — do not attempt to
   debug the scaffold.

3. For every architecture or model family you name in this sprint, cite
   the specific file and function you read it from. If you cannot cite a
   file and function, say "I did not read the source for this — I can
   confirm after I check." Do NOT name architectures that are not in the
   scaffold.

4. For any dollar figure you state, quote the exact line from the project's
   cost source. Do NOT invent numbers.

5. Do NOT propose the per-class thresholds for the pre-registration phase.
   Those are my pre-registration; I write them in the phase journal BEFORE
   seeing the leaderboard. If you propose values here, you corrupt the
   pre-registration.

6. Do NOT use the word "blocker" without naming a specific action I cannot take.

Once skeletons are copied and endpoints confirmed live, summarise: (a) the
phases of this sprint and the single Trust Plane decision each phase owns,
(b) the per-class threshold decision shape only — not by value, (c) the
red-team sweeps specific to this sprint's vision model.

Then stop and wait for my Phase 1 prompt.
```

**Tonight-specific additions** (Week 7 LumenCircuit Sprint 1):

```
Sprint: Sprint 1 Vision QC — transfer-learned PCB inspector (4 classes:
good, minor_defect, major_defect, safety_critical_defect).

Phases covered: Playbook phases 1, 2, 3, 4, 5, 6, 7, 8. Phases 1, 2, 3 are
shared across sprints — framed once here, not re-run in Sprint 2.
Phase 6 in this sprint is the per-class variant: 4 thresholds with
different defenses (cost-balanced for 3 classes, WSH hard floor 0.40 for
safety_critical_defect).

Skeleton copy: copy phase_{1..8}_vision.md skeletons from journal/skeletons/
into workspaces/metis/week-07-manufacturing/journal/. Inventory in
journal/skeletons/README.md.

Endpoint checks (GET only, all on http://127.0.0.1:8000):
- /health → returns boards/sensor_rows/rl_episodes counts + baselines + drift_refs_active
- /inspect/vision/leaderboard → 3 archs × 4 per-class P/R/F1
- /inspect/vision/registry → registry state
- /state/current → viewer aggregator

If any is not live, STOP and raise a hand — do not debug.

Three architectures cite (cite, do not pick):
- resnet50_lr_head — frozen ResNet-50 backbone + LogisticRegression head
- efficientnet_b0_rf_head — frozen EfficientNet-B0 backbone + RandomForest head
- vit_small_gbm_head — frozen ViT-Small backbone + HistGradientBoosting head
Cite each in src/manufacturing/backend/ml_context.py. Note these all share
the same frozen-embedding scaffold; they differ in head classifier AND
embedding dimensionality (per SCAFFOLD_MANIFEST.md "Implementation deviations").

CRITICAL — Transfer-learning prohibition: do NOT name "training the CNN
from scratch" as a Phase 4 candidate. The scaffold uses frozen backbone +
fine-tuned head ONLY; full from-scratch training is not in 50 minutes of
budget. Phase 4 candidates are the 3 architectures above; the sweep varies
which head pairs with which backbone (controlled by /inspect/vision/train
with `unfreeze_layers`).

Edge-latency budget: 80 ms/board on Jetson-class hardware (PRODUCT_BRIEF
§4.1 + §7). The Phase 5 architecture pick MUST cite this constraint AND
the per-class P/R/F1 leaderboard AND the 49:1 cost asymmetry. EfficientNet
typically wins on edge throughput; ViT-Small typically wins on accuracy
but is data-hungry at 800 images.

Dollar figures for Sprint 1: major-defect-shipped FN cost ($4,200 per board)
and false-scrap FP cost ($85 per board). Asymmetry: 49:1. The WSH
$1,000,000+ ceiling on safety_critical_defect is structurally separate
(HARD constraint, not cost-balanced). All three come from PRODUCT_BRIEF.md
§2 / specs/business-costs.md — quote the exact line.

Decision shape to name (NOT values): per-class auto-pass threshold
(4 thresholds, 3 cost-balanced + 1 WSH-floor-bound at ≥0.40). Do NOT
propose numeric thresholds here — that is my pre-registration call in
phase_6_vision.md, before I see the Phase 4 leaderboard.

Phase 7 sweeps to name (NOT execute): list the three vision-specific
red-team sweeps from the phase-07-redteam.md file: adversarial pixel
perturbation (board-image noise, JPEG compression), out-of-distribution
robustness (line × shift × supplier variation), demographic-skew analog
(per-line × per-shift recall stratification — a manufacturing equivalent
to demographic skew).

After the summary, stop and wait for my Phase 1 prompt.
```

**How to paste:** Combine both blocks into a single paste into your `claude` session.

---

## 3. First three phases of Sprint 1 (paste-ready journal blocks)

After the boot summary, you will run Phases 1, 2, 3 in sequence. Each phase has its own file (`phase-01-frame.md`, `phase-02-data-audit.md`, `phase-03-features.md`) with the full prompt — but for ultra-fast booting these condensed paste blocks let you skip ahead if the room is on the clock.

**Phase 1 condensed (full version: `phase-01-frame.md`):**

```
Playbook Phase 1 — Frame. Draft target / population / horizon /
throughput-ceiling / cost-asymmetry for the LumenCircuit Vision QC inspector
into journal/phase_1_frame.md. Quote $4,200 (major-defect FN) and $85
(false-scrap FP) verbatim from specs/business-costs.md. Show daily $
exposure at 12,000 inspection events/day. Acknowledge the WSH $1M ceiling
on safety_critical_defect as a SEPARATE structural floor, not part of the
49:1 cost-balanced math. Do NOT propose thresholds. Stop when drafted.
```

**Phase 2 condensed (full version: `phase-02-data-audit.md`):**

```
Playbook Phase 2 — Data Audit. Six-category audit on
src/manufacturing/data/boards_labelled.csv (800 rows) AND
sensor_stream.csv (432k rows) AND rl_episodes.json. Categories: label
quality (per-class kappa on the 100-board double-labelled subset),
temporal leakage (any feature computed AFTER inspection), survivorship
(boards auto-removed by AOI never reached human label), distribution
shift (per-line / per-shift / per-supplier balance), missingness
(per-machine sensor gaps), proxy variables (line_id and shift correlate
with operator cohort). Cite row counts. Stop when journal is drafted.
```

**Phase 3 condensed (full version: `phase-03-features.md`):**

```
Playbook Phase 3 — Feature Framing. For Sprint 1 image features, classify
on three axes: available-at-decision-time / proxy-risk / engineering-source.
Surface board image, defect-mode label, and account metadata (line_id,
shift, supplier_lot_id). Flag line_id + shift as MEDIUM proxy risk for
the per-line skew sweep in Phase 7. Stop when table drafted.
```

---

## 4. Signals the output is on track

**Signals of success:**

- ✓ Eight skeleton files copied: `journal/phase_{1..8}_vision.md` all exist with blanks intact
- ✓ A live GET against `/inspect/vision/leaderboard` returning 3 archs × 4 per-class P/R/F1
- ✓ A live GET against `/inspect/vision/registry` returning the registry state
- ✓ Written summary of the eight phases with one Trust Plane decision each
- ✓ Per-class threshold decision shape named (4 thresholds, safety_critical_defect flagged as WSH-floor-bound) with NO numeric values
- ✓ Three Phase 7 sweeps named (not executed)
- ✓ Stop signal pending the Phase 1 walk-prompt
- ✓ Viewer (http://localhost:3000) refreshes and shows: Sprint 1 tile activates; vision card shows "awaiting Phase 4 leaderboard"

**Signals of drift — push back if you see:**

- ✗ A threshold value proposed (e.g. "major_defect ≥ 0.85") — ask "please remove the proposed value; I pre-register thresholds in `phase_6_vision.md`."
- ✗ "Train CNN from scratch" named for Phase 4 — ask "the scaffold uses frozen backbone + fine-tuned head; full from-scratch is not in budget."
- ✗ A dollar figure not quoted from `specs/business-costs.md` — ask "please quote the exact line from the cost spec."
- ✗ Skeletons not copied to `journal/` — ask "please copy the skeletons now so every phase has a live journal file."
- ✗ A baseline F1 that is suspicious (e.g. 0.99 across all classes) — ask "is the backend actually live? Please re-run the GET and show me the output."
- ✗ Edge-latency budget not mentioned — ask "doesn't Phase 5 need to defend against the 80 ms/board edge constraint?"

---

## 5. Acceptance criteria for Sprint 1

Sprint 1 is complete when ALL of:

- ✓ `journal/phase_{1..8}_vision.md` all exist and are filled (8 files)
- ✓ `POST /inspect/vision/threshold` fired 4 times (one per class), with `safety_critical_defect` ≥ 0.40 (otherwise the endpoint returns 409 — the WSH hard floor is enforced server-side)
- ✓ `POST /inspect/vision/promote` fired with `to_stage: "shadow"` for the chosen architecture
- ✓ `journal/phase_8_vision.md` records PASS/FAIL with named rollback signal
- ✓ Viewer Sprint 1 tile is green at session close

The single file that proves Sprint 1 ran end-to-end: **`journal/phase_8_vision.md`** with PASS verdict, named rollback signal, and a successful POST to `/inspect/vision/promote` recorded in the journal.

---

## 6. Quick reference (30 sec, generic)

### Sprint boot

The setup ritual that runs before any Playbook phase prompt in a sprint: confirm preflight green, copy skeletons, confirm endpoints live, get an orientation summary. The boot exists because a hallucinated endpoint or a missing skeleton file creates failure mid-phase when you can least afford to debug it. Ten minutes at boot saves 20 minutes of confusion mid-Phase 4.

### Transfer-learning prohibition

In tonight's scaffold, the vision QC inspector uses a frozen pre-trained backbone + fine-tuned head — that's the only Phase 4 candidate family. Full from-scratch CNN training does not fit in the 50-minute Sprint 1 budget. The Phase 4 sweep varies the head + backbone pairing, not the architecture family. Asking Claude Code to "use AutoML to find the best CNN" raises a ValueError and burns 15 minutes.

### Edge-latency budget

Vision QC runs on Jetson-class hardware on the inspection cameras — 80 ms/board is the contractual latency budget per `PRODUCT_BRIEF.md §4.1` and `§7`. Phase 5 architecture pick MUST cite this constraint. EfficientNet-B0 typically wins on edge throughput; ViT-Small wins on accuracy but is data-hungry. The trade-off is partly an edge-deployment trade-off, not just an accuracy one.

### Cite-or-confirm

A tighter variant of cite-or-cut: either (a) name the file and function you read it from, or (b) say explicitly "I have not checked the source for this yet." Option (b) is acceptable at boot; it becomes unacceptable mid-phase. The distinction matters because some scaffold claims (like which augmentations were applied) are buried in `ml_context.py` and require a real read — Claude Code will confabulate if you don't demand the confirmation.

### Threshold shapes vs threshold values

Naming the shape of a constraint means saying "per-class auto-pass threshold (4 of them, 3 cost-balanced + 1 WSH-floor-bound)." It does NOT mean saying "major_defect ≥ 0.85." The value is your pre-registration call, written in `phase_6_vision.md` before you see results. If the boot summary names a value, the pre-registration is already corrupted.

---

## 7. Gate / next

Before moving on:

- [ ] Eight skeleton files exist in `journal/phase_{1..8}_vision.md`
- [ ] `/inspect/vision/leaderboard` returned 3 archs × 4 per-class entries
- [ ] `/inspect/vision/registry` returned registry state
- [ ] Summary written: eight phases, one Trust Plane decision each, per-class threshold shape (no values), three Phase 7 sweeps named, edge-latency budget acknowledged
- [ ] Claude Code has stopped and is waiting for the Phase 1 prompt

**Next file:** [`phase-01-frame.md`](./phase-01-frame.md)
