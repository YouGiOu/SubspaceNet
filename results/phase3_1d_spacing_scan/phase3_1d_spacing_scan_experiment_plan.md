# Phase 3 1D Spacing Scan Experiment Plan

## Objective
Quantify how much of the 2D performance drop is caused by spacing itself, before attributing the remaining error to the 2D geometry simplification.

## Conditions
- Array: 1D sparse NULA `[0, 1, 4, 8]`
- Sources: 2 coherent narrowband targets
- Snapshot count: `T = 200`
- SNR: `10 dB`
- Minimum separation: `5 deg`
- Methods: MUSIC, Root-MUSIC, ESPRIT

## Spacing Sweep
- `0.5 lambda` with a wide FOV
- `1.0 lambda` with a medium FOV
- `1.9 lambda` with a narrow FOV

## Comparison Per Spacing
- Baseline without LRMC
- LRMC with the current best coherent configuration

## Metrics
- Horizontal-angle RMSE
- Runtime per sample
- LRMC convergence and final residual

## Interpretation Rule
- If LRMC still helps at `0.5 lambda` but collapses as spacing grows, then spacing is the main culprit.
- If LRMC already weakens sharply at `1.0 lambda`, then the geometry is becoming ambiguous earlier than expected.
- If the 1D scan remains healthy at `1.9 lambda` but the 2D case fails, then the 2D simplification is the main issue.
