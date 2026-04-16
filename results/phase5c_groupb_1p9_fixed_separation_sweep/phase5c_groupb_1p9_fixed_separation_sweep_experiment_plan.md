# Phase 5C Group B 1.9 Lambda Fixed-Separation Experiment Plan

## Goal
Measure how classical subspace performance changes as the two-source angular separation is tightened from `5 deg` down to `1 deg` on the actual Group B `1.9 lambda` hardware geometry, under both coherent and non-coherent signals.

## Scope
This study keeps the same classical front end used in the current Group B work:
- Group B hardware geometry
- `1.9 lambda` spacing
- `SS -> LRMC` front end

To isolate angular-resolution effects, this study uses a fixed high-snapshot operating point:
- `T = 200`

## Signal Regimes
- coherent
- non-coherent

## Fixed-Separation Sweep
- `5 deg`
- `4 deg`
- `3 deg`
- `2 deg`
- `1 deg`

## Fixed Conditions
- Array: Group B 12-channel 2D hardware geometry
- Physical spacing: `1.9 lambda`
- Sources: `M = 2`, narrowband
- Snapshots: `T = 200`
- SNR: `10 dB`
- Azimuth range: `[-15 deg, 15 deg]`
- Elevation range: `[-15 deg, 15 deg]`
- Preprocessing: `SS -> LRMC`
- LRMC rank: `3`
- LRMC solver: `svd`
- LRMC initialization: `lag`
- Methods: `MUSIC`, `Root-MUSIC`, `ESPRIT`
- Metric: horizontal-angle RMSE

## Dataset Generation Rule
This experiment uses a new template option:
- `fixed_doa_gap`

When present, dataset generation enforces the requested exact azimuth separation instead of only requiring a minimum gap.

## Hypotheses
- Performance should degrade as angular separation decreases.
- Coherent signals should degrade faster than non-coherent signals at the same separation.
- The first strong classical failure boundary for later SubspaceNet angle-resolution training is more likely to appear at small separation than at moderate snapshot reduction.

## Canonical Launcher
- [run_phase5c_groupb_1p9_fixed_separation_sweep.py](/f:/workspace1/SubspaceNet/run_phase5c_groupb_1p9_fixed_separation_sweep.py)

Recommended command:
```bash
python run_phase5c_groupb_1p9_fixed_separation_sweep.py
```
