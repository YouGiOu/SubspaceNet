# Phase 5 Group B 1.9 Lambda Snapshot Boundary Experiment Plan

## Goal
Measure how classical subspace performance degrades as snapshot count decreases on the actual Group B `1.9 lambda` hardware geometry, under both coherent and non-coherent signals, so we can identify the most meaningful low-snapshot regime for the next SubspaceNet training stage.

## Scope
This study focuses on the same preprocessing path used in the current SubspaceNet work:
- Group B hardware geometry
- `1.9 lambda` spacing
- `SS -> LRMC` front end

That keeps the snapshot boundary directly relevant to later low-snapshot SubspaceNet training.

## Signal Regimes
- coherent
- non-coherent

## Snapshot Sweep
- `T = 10`
- `T = 25`
- `T = 50`
- `T = 100`
- `T = 200`

## Fixed Conditions
- Array: Group B 12-channel 2D hardware geometry
- Physical spacing: `1.9 lambda`
- Sources: `M = 2`, narrowband
- SNR: `10 dB`
- Azimuth range: `[-15 deg, 15 deg]`
- Elevation range: `[-15 deg, 15 deg]`
- Minimum azimuth separation: `5 deg`
- Preprocessing: `SS -> LRMC`
- LRMC rank: `3`
- LRMC solver: `svd`
- LRMC initialization: `lag`
- Methods: `MUSIC`, `Root-MUSIC`, `ESPRIT`
- Metric: horizontal-angle RMSE

## Hypotheses
- Coherent signals should degrade faster than non-coherent signals as `T` decreases.
- Root-MUSIC and ESPRIT should reveal the low-snapshot boundary more clearly than MUSIC.
- There should be a practical snapshot threshold below which the classical `SS -> LRMC` pipeline becomes weak enough that low-snapshot SubspaceNet training becomes especially meaningful.

## Intended Interpretation
- If classical performance remains strong down to very low `T`, then the low-snapshot SubspaceNet problem is less urgent.
- If coherent performance collapses sharply while non-coherent performance stays stable, then the first low-snapshot learned study should prioritize the coherent regime.
- If Root-MUSIC and ESPRIT break earlier than MUSIC, that suggests ESPRIT-style or Root-MUSIC-style learned heads are the right targets for the next low-snapshot experiments.

## Canonical Launcher
- [run_phase5_groupb_1p9_snapshot_boundary.py](/f:/workspace1/SubspaceNet/run_phase5_groupb_1p9_snapshot_boundary.py)

Recommended command:
```bash
python run_phase5_groupb_1p9_snapshot_boundary.py
```
