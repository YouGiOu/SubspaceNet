# Phase 6 Group B 1.9 Lambda Non-Coherent Fixed-Gap and SNR Grid Experiment Plan

## Goal
Measure how non-coherent Group B `1.9 lambda` performance changes over the same fixed angular-separation and SNR grid used in the coherent Phase 6 study, while comparing the current learned target `SS -> LRMC -> SubspaceNet -> ESPRIT` against classical controls.

## Scope
This phase is the non-coherent counterpart of the coherent Phase 6 grid and keeps the same structure:
- Group B 12-channel 2D hardware geometry
- `1.9 lambda` spacing
- non-coherent sources
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
- Sources: `M = 2`, non-coherent, narrowband
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
- Metric: horizontal-angle RMSE in degrees

## Training Throughput Profile
This phase uses a more aggressive training configuration than the initial coherent setup to improve GPU utilization:
- training batch size: `256`
- validation batch size: `512`
- DataLoader workers: `8`
- pinned memory enabled
- persistent workers enabled
- prefetch factor: `4`

These changes are intended to improve throughput without changing the experiment definition itself.

## Learned Target
The learned branch in each cell is:
- `SS -> LRMC -> SubspaceNet -> ESPRIT`

## Control Group
The control branch in each cell evaluates:
- `DBF`
- `MUSIC`
- `Root-MUSIC`
- `ESPRIT`

All control methods use the same non-coherent Group B `SS -> LRMC` classical front end and are compared only on horizontal-angle RMSE.

## Expected Outputs
Running the launcher should produce:
- per-method `metrics.json` files
- SubspaceNet loss curves and checkpoints for each learned cell
- `results/phase6_groupb_1p9_noncoherent_fixed_gap_snr_grid/summary.csv`
- `results/phase6_groupb_1p9_noncoherent_fixed_gap_snr_grid/phase6_groupb_1p9_noncoherent_fixed_gap_snr_grid_results.md`

## Canonical Launcher
- [run_phase6_groupb_1p9_noncoherent_fixed_gap_snr_grid.py](/d:/workspace1/SubspaceNet/run_phase6_groupb_1p9_noncoherent_fixed_gap_snr_grid.py)

Recommended command:
```bash
python run_phase6_groupb_1p9_noncoherent_fixed_gap_snr_grid.py
```
