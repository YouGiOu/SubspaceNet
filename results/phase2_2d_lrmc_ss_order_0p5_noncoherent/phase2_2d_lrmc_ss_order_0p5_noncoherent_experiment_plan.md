# Phase 2 2D LRMC / Spatial Smoothing Order Experiment at 0.5 Lambda, Non-Coherent Signals

## Goal
Re-run the 2D order comparison with the same row-replicated `[0,1,4,8]` layout scaled to `0.5 lambda`, but switch the source model from coherent to non-coherent signals.

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
- Sources: 2 non-coherent narrowband targets
- Snapshot count: `T = 200`
- SNR: `10 dB`
- FOV: `[-15 deg, 15 deg]` in azimuth and elevation
- Minimum azimuth separation: `5 deg`

## Metrics
- Horizontal-angle RMSE
- Runtime per sample
- LRMC runtime and convergence rate
- Final LRMC residual / numerical stability indicators

## What This Tests
- Whether the `0.5 lambda` geometry is still beneficial when coherence is removed.
- Whether spatial smoothing is still the dominant step, or whether LRMC becomes less important once the signals are non-coherent.
- Whether the best processing order changes between coherent and non-coherent source models.

## Interpretation
- If LRMC helps much less for non-coherent sources, that would mean the coherent-source structure was a major reason LRMC mattered in the earlier study.
- If the same `SS -> LRMC` order still wins, then the geometry and order conclusions are robust beyond the coherent case.
