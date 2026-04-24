# Phase 6B Group B 1.9 Lambda Hard-Regime Snapshot Breakdown Experiment Plan

## Goal
Find the low-snapshot breakdown point of SubspaceNet in a genuinely hard Group B operating regime by sweeping snapshots while holding angular separation and SNR fixed at difficult values.

## Hard Regime Definition
This phase fixes the operating point to:
- Group B 12-channel 2D hardware geometry
- `1.9 lambda` spacing
- fixed azimuth separation: `1 deg`
- fixed SNR: `1 dB`

This is intended to probe where the learned pipeline begins to fail relative to both LRMC-assisted and raw classical baselines.

## Signal Regimes
- coherent
- non-coherent

## Snapshot Sweep
- `T = 1`
- `T = 2`
- `T = 4`
- `T = 8`
- `T = 16`
- `T = 25`

## Comparison Pipelines
Each `(signal regime, T)` cell includes:
- raw classical controls without `SS -> LRMC`
- `SS -> LRMC` classical controls
- `SS -> LRMC -> SubspaceNet -> ESPRIT`

The classical methods evaluated in both control branches are:
- `DBF`
- `MUSIC`
- `Root-MUSIC`
- `ESPRIT`

## Fixed Conditions
- Array: Group B 12-channel 2D hardware geometry
- Physical spacing: `1.9 lambda`
- Row pattern used by rowwise LRMC: `[0, 4, 7, 8]`
- Sources: `M = 2`, narrowband
- Azimuth range: `[-15 deg, 15 deg]`
- Elevation range: `[-15 deg, 15 deg]`
- Fixed azimuth separation: `1 deg`
- Fixed SNR: `1 dB`
- Dataset size per cell: `45,000`
- Training epochs: `80`
- Learned metric target: horizontal-angle RMSE in degrees

## Learned Pipeline
The learned branch uses:
- `SS -> LRMC` preprocessing
- SubspaceNet with differentiable ESPRIT head

This phase keeps the ESPRIT head only, consistent with the current repo preference for stable learned training.

## Throughput Profile
This phase uses the same faster SubspaceNet training profile now used by the Phase 6 grid studies:
- training batch size: `256`
- validation batch size: `512`
- DataLoader workers: `8`
- pinned memory enabled
- persistent workers enabled
- prefetch factor: `4`

## Why This Phase Matters
The earlier work showed:
- coherent Group B becomes difficult at very small angular separation
- non-coherent Group B is stronger overall, but still has a real ultra-low-snapshot boundary

This phase combines those insights into a sharper breakdown test by using:
- the hardest separation already identified in the repo
- low SNR
- an explicit snapshot sweep
- both raw and LRMC-assisted classical references

## Expected Outputs
Running the launcher should produce:
- per-method `metrics.json` files
- SubspaceNet loss curves and checkpoints for each learned cell
- `results/phase6b_groupb_1p9_fixed_gap1_snr1_snapshot_breakdown/summary.csv`
- `results/phase6b_groupb_1p9_fixed_gap1_snr1_snapshot_breakdown/phase6b_groupb_1p9_fixed_gap1_snr1_snapshot_breakdown_results.md`

## Canonical Launcher
- [run_phase6b_groupb_1p9_fixed_gap1_snr1_snapshot_breakdown.py](/d:/workspace1/SubspaceNet/run_phase6b_groupb_1p9_fixed_gap1_snr1_snapshot_breakdown.py)

Recommended command:
```bash
python run_phase6b_groupb_1p9_fixed_gap1_snr1_snapshot_breakdown.py
```
