# Phase 2 2D LRMC / Spatial Smoothing Order Experiment Plan at 0.5 Lambda

## Goal
Re-run the 2D order comparison with the same row-replicated `[0,1,4,8]` layout, but scaled to `0.5 lambda`, to see whether the improved spacing restores LRMC usefulness.

## Runs
- Baseline: no LRMC, no smoothing
- Spatial smoothing only
- LRMC only
- Spatial smoothing -> LRMC
- LRMC -> spatial smoothing

## Conditions
- Array: 12-channel 2D row layout
- Physical positions:
  - `(0, 0), (1, 0), (4, 0), (8, 0)`
  - `(0, 1), (1, 1), (4, 1), (8, 1)`
  - `(0, 2), (1, 2), (4, 2), (8, 2)`
- Spacing: `0.5 lambda`
- Sources: 2 coherent narrowband targets
- Snapshot count: `T = 200`
- SNR: `10 dB`
- FOV: keep the earlier `[-15 deg, 15 deg]` horizontal/elevation range for comparability
- Minimum azimuth separation: `5 deg`

## Metrics
- Horizontal-angle RMSE
- Runtime per sample
- LRMC runtime and convergence rate
- Final LRMC residual / numerical stability indicators

## Interpretation
- If LRMC recovers a large gain at `0.5 lambda`, then the poor `1.9 lambda` result was mainly a spacing problem.
- If the gain remains small even at `0.5 lambda`, then the 2D row-replicated structure itself is the main limiting factor.
