# Phase 2 2D LRMC / Spatial Smoothing Order Experiment Plan

## Goal
Determine which preprocessing order is best for horizontal-angle estimation on the new 2D array.

## Runs
- Baseline: no LRMC, no smoothing
- Spatial smoothing only
- LRMC only
- Spatial smoothing -> LRMC
- LRMC -> spatial smoothing

## Metrics
- Horizontal-angle RMSE
- Runtime per sample
- LRMC runtime and convergence rate
- Final LRMC residual / stability indicators

## Sweeps
- Snapshot count
- SNR
- LRMC rank
- Solver choice, if the default solver is not sufficient to separate the orderings

## Decision Rule
- Prefer the path with the lowest and most stable horizontal-angle RMSE.
- If RMSE is similar, prefer the path with simpler and more numerically stable preprocessing.

## Expected Output
- `summary.csv`
- one `metrics.json` per method and template
- a markdown summary table in the results root
