# Phase 5B Group B 1.9 Lambda Ultra-Low Snapshot Boundary Experiment Plan

## Goal
Probe the true ultra-low-snapshot boundary of the classical Group B `1.9 lambda` pipeline by extending the previous snapshot sweep down to `T = 1, 2, 4, 6, 8, 10` for both coherent and non-coherent signals.

## Scope
This study keeps the same front end used in the current Group B SubspaceNet work:
- Group B hardware geometry
- `1.9 lambda` spacing
- `SS -> LRMC` front end

That keeps the boundary directly relevant to later low-snapshot SubspaceNet decisions.

## Signal Regimes
- coherent
- non-coherent

## Snapshot Sweep
- `T = 1`
- `T = 2`
- `T = 4`
- `T = 6`
- `T = 8`
- `T = 10`

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
- A sharper low-snapshot breakdown should appear below `T = 10`, especially for coherent signals.
- Non-coherent performance should remain stronger than coherent performance at the same ultra-low `T`.
- If a practical boundary exists for future low-snapshot SubspaceNet training, it is more likely to appear in this `T = 1..10` regime than in the earlier `T = 10..200` sweep.

## Intended Interpretation
- If the coherent pipeline remains stable even at `T = 1..4`, then snapshot scarcity is not the main driver of the remaining coherent difficulty.
- If the non-coherent pipeline stays strong while the coherent one degrades sharply, then the first low-snapshot learned study should prioritize coherent signals.
- If all three classical methods degrade together, then the boundary is regime-driven rather than method-specific.

## Canonical Launcher
- [run_phase5b_groupb_1p9_ultralow_snapshot_boundary.py](/f:/workspace1/SubspaceNet/run_phase5b_groupb_1p9_ultralow_snapshot_boundary.py)

Recommended command:
```bash
python run_phase5b_groupb_1p9_ultralow_snapshot_boundary.py
```
