<!--
Copyright (c) 2026 Terrene Foundation (Singapore CLG)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
-->

# Metis — Monorepo Layout

Metis is an MBA-course training monorepo. Every week's workshop ships a small ML-powered product; over the term, those products accumulate into a catalogue the student can point at and say "I commissioned all of these." The repo is organised as a multi-product monorepo from Week 5 onward.

## Rule of thumb

Students always initialise from the repo root: `cd ~/repos/training/metis && claude`. The opening prompt in each week's `START_HERE.md` tells Claude Code which workspace is active. The COC phases (`/analyze`, `/todos`, `/implement`, `/redteam`, `/codify`) run against that workspace. Implementation code lives in `src/<domain>/`; UI lives in `apps/<platform>/<domain>/`; session artefacts (plans, todos, journal, red-team) live in `workspaces/<name>/`.

## Layout

```
metis/
├── pyproject.toml              # single shared dependency manifest
├── .venv/                      # single shared venv (uv-managed)
├── .env                        # single shared env (API keys, ports)
├── CLAUDE.md                   # COC rules for every session
├── MONOREPO.md                 # (this file)
│
├── src/                        # the products
│   ├── supply_chain/           # Week 4 — Northwind Control Tower (legacy location)
│   │   └── (still under workspaces/metis/week-04-supply-chain/src/)
│   └── retail/                 # Week 5 — Arcadia Retail Intelligence Suite
│       ├── backend/            # FastAPI app, routes, ml_context, startup, config
│       ├── data/               # datasets + pre-baked baselines + scenarios
│       └── scripts/            # generate_data, preflight, run_backend, scenario_inject
│
├── apps/                       # the UIs
│   ├── web/                    # browser-based viewers
│   │   └── retail/             # Week 5 dashboard
│   └── mobile/                 # reserved for later weeks
│
└── workspaces/metis/           # per-session records (COC doctrine)
    ├── week-04-supply-chain/
    │   ├── PRODUCT_BRIEF.md    # student-facing product context
    │   ├── PLAYBOOK.md         # 14-phase ML Decision Playbook
    │   ├── START_HERE.md       # student manual
    │   ├── briefs/             # student-writable input
    │   ├── 01-analysis/        # /analyze outputs
    │   ├── 04-validate/        # /redteam outputs
    │   ├── todos/active/       # /todos outputs
    │   ├── journal/            # Playbook-phase journal entries
    │   └── specs/              # domain truth (per rules/specs-authority.md)
    └── week-05-retail/
        ├── PRODUCT_BRIEF.md
        ├── PLAYBOOK.md
        ├── START_HERE.md
        ├── SCAFFOLD_MANIFEST.md
        ├── briefs/
        ├── 01-analysis/
        ├── 04-validate/
        ├── todos/active/
        ├── journal/
        └── specs/
```

## Why this split

1. **COC doctrine** (`workspaces/CLAUDE.md`): workspaces are session records. The actual codebase lives at project root. Week 4 violated this by putting `src/` inside the workspace; Week 5 fixes it.
2. **Cross-week reuse**: a retail product can borrow a primitive from the supply-chain product (e.g., a cost-curve utility) without reaching into a workspace that is supposedly a session log.
3. **Single dependency boundary**: one `pyproject.toml`, one `.venv`, one `.env`. Students never debug "why does Week 4's env not work for Week 5".
4. **Predictable onboarding**: every week looks the same. `claude` at `metis/`, opening prompt names the workspace, scaffold runs from `src/<domain>/scripts/run_backend.sh`.

## Backfilling Week 4

Week 4's `src/` + `apps/web/` + `scripts/` currently live inside `workspaces/metis/week-04-supply-chain/`. They will be migrated to `src/supply_chain/` and `apps/web/supply_chain/` in a follow-up session — deferred tonight to avoid breaking the shipped Week 4 workshop.

## For students

You will never think about this layout during class. Your opening prompt and your `START_HERE.md` always direct you to the right places. If you run into a path error and the scaffold points you at `src/retail/`, that is this file's business — not yours.
