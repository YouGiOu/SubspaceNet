# Phase 3c 1D NULA 1.9 Lambda Coherent vs Non-Coherent Comparison

## Goal
Test whether the large errors seen in the earlier 1.9 lambda studies were driven mainly by signal coherence, by the LRMC preprocessing path, or by the array spacing itself.

## Runs
For each signal type:
- Baseline
- LRMC only
- LRMC -> SS

Signal types:
- Coherent
- Non-coherent

## Conditions
- Array: 1D sparse NULA `[0, 1, 4, 8]`
- Spacing: `1.9 lambda`
- Sources: 2 targets
- Snapshot count: `T = 200`
- SNR: `10 dB`
- FOV: `[-15 deg, 15 deg]`
- Minimum separation: `5 deg`
- Methods: `MUSIC`, `Root-MUSIC`, `ESPRIT`

## Metrics
- Horizontal-angle RMSE
- Runtime per sample
- LRMC convergence / residual diagnostics

## Interpretation
- If non-coherent MUSIC remains accurate while coherent methods fail, the main issue is source coherence and estimator choice.
- If LRMC helps only in the coherent case, then LRMC is mainly compensating for coherence-related rank deficiency.
- If the 1.9 lambda case still fails even for non-coherent signals under LRMC, then spacing itself remains a hard limit.
