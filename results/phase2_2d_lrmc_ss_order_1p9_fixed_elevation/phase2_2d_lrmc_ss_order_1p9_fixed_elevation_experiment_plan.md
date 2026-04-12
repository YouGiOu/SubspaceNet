# Phase 2 2D LRMC / Spatial Smoothing Order Experiment at 1.9 Lambda with Fixed Elevation

## Goal
Test whether the poor 2D results at `1.9 lambda` are partly caused by the elevation dimension. This experiment keeps the same 2D geometry and processing order study as the original Phase 2 1.9 lambda run, but fixes elevation to a single value.

## Runs
- Baseline: no LRMC, no smoothing
- Spatial smoothing only
- LRMC only
- Spatial smoothing -> LRMC
- LRMC -> spatial smoothing

## Conditions
- Array: 12-channel 2D row-replicated geometry
- Physical spacing: `1.9 lambda`
- Azimuth range: `[-15 deg, 15 deg]`
- Elevation: fixed to a single angle
- Minimum azimuth separation: `5 deg`
- Sources: 2 coherent narrowband targets
- Snapshot count: `T = 200`
- SNR: `10 dB`
- Methods: `MUSIC`, `Root-MUSIC`, `ESPRIT`

## Metrics
- Horizontal-angle RMSE
- Runtime per sample
- LRMC convergence and residual diagnostics

## Interpretation
- If fixing elevation improves the 2D results materially, then elevation coupling is a major contributor to the previous degradation.
- If performance remains similar to the unfixed-elevation case, then the main limitation is the 2D-to-1D reduction or the 1.9 lambda geometry itself.
- The comparison is intended to isolate elevation influence, not to change the algorithmic pipeline.
