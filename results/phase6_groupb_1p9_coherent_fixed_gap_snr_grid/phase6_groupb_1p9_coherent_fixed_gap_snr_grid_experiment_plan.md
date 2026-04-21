# Phase 6 Group B 1.9 Lambda Coherent Fixed-Gap and SNR Grid Experiment Plan

## Goal
Measure how coherent Group B `1.9 lambda` performance changes over a joint grid of fixed angular separation and SNR, while comparing the current learned target `SS -> LRMC -> SubspaceNet -> ESPRIT` against classical controls.

## Scope
This study is intentionally targeted at the most meaningful coherent Group B weakness identified so far:
- small angular separation

To make that boundary more informative, this phase adds a modest SNR sweep while keeping the rest of the validated pipeline fixed:
- Group B 12-channel 2D hardware geometry
- `1.9 lambda` spacing
- coherent sources
- `SS -> LRMC` classical front end
- SubspaceNet with differentiable ESPRIT head

## Grid Definition
Fixed angular separations:
- `1 deg`
- `2 deg`
- `3 deg`
- `4 deg`
- `5 deg`

Fixed SNR values:
- `1 dB`
- `5 dB`
- `10 dB`
- `15 dB`

This yields `20` experiment cells.

Each cell includes:
- one SubspaceNet-ESPRIT training run
- one classical control template with `DBF`, `MUSIC`, `Root-MUSIC`, and `ESPRIT`

## Fixed Conditions
- Array: Group B 12-channel 2D hardware geometry
- Physical spacing: `1.9 lambda`
- Row pattern used by rowwise LRMC: `[0, 4, 7, 8]`
- Sources: `M = 2`, coherent, narrowband
- Snapshots: `T = 40`
- Azimuth range: `[-15 deg, 15 deg]`
- Elevation range: `[-15 deg, 15 deg]`
- Preprocessing: `SS -> LRMC`
- LRMC rank: `3`
- LRMC solver: `svd`
- LRMC initialization: `lag`
- Virtual ULA size: `9`
- Dataset size per cell: `45,000`
- Training epochs: `80`
- Seed: fixed at `42`
- Metric: horizontal-angle RMSE in degrees

## Learned Target
The learned branch in each cell is:
- `SS -> LRMC -> SubspaceNet -> ESPRIT`

This phase intentionally does not include differentiable Root-MUSIC training, because the current repo evidence still supports ESPRIT as the stable learned default.

## Control Group
The control branch in each cell evaluates:
- `DBF`
- `MUSIC`
- `Root-MUSIC`
- `ESPRIT`

All control methods use the same coherent Group B `SS -> LRMC` classical front end and are compared only on horizontal-angle RMSE.

## Why This Phase Matters
Phase 5C showed that coherent Group B performance is much more sensitive to angular separation than to snapshot count in the previously tested ranges.

This phase extends that result in the most practical next direction:
- keep the low-snapshot regime moderately challenging at `T = 40`
- sweep separation and SNR together
- check where SubspaceNet-ESPRIT offers the clearest advantage over classical baselines

## Expected Outputs
Running the launcher should produce:
- per-method `metrics.json` files
- SubspaceNet loss curves and checkpoints for each learned cell
- `results/phase6_groupb_1p9_coherent_fixed_gap_snr_grid/summary.csv`
- `results/phase6_groupb_1p9_coherent_fixed_gap_snr_grid/phase6_groupb_1p9_coherent_fixed_gap_snr_grid_results.md`

## Canonical Launcher
- [run_phase6_groupb_1p9_coherent_fixed_gap_snr_grid.py](/d:/workspace1/SubspaceNet/run_phase6_groupb_1p9_coherent_fixed_gap_snr_grid.py)

Recommended command:
```bash
python run_phase6_groupb_1p9_coherent_fixed_gap_snr_grid.py
```
