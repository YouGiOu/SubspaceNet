# Phase 3b Non-Coherent MUSIC Validation on the 1.9 Lambda NULA

## Goal
Check whether MUSIC remains stable when the source model is switched from coherent to non-coherent on the sparse NULA `[0, 1, 4, 8]` with `1.9 lambda` spacing and a narrow `[-15 deg, 15 deg]` FOV.

## Condition
- Array: 1D sparse NULA `[0, 1, 4, 8]`
- Spacing: `1.9 lambda`
- Sources: 2 non-coherent narrowband targets
- Snapshot count: `T = 200`
- SNR: `10 dB`
- FOV: `[-15 deg, 15 deg]`
- Minimum separation: `5 deg`
- Method: MUSIC only

## Metric
- Horizontal-angle RMSE

## Interpretation
- If MUSIC is accurate here, then the earlier 1.9 lambda difficulty was likely driven mostly by coherence and/or LRMC preprocessing interactions.
- If MUSIC still shows large error, then `1.9 lambda` remains intrinsically ambiguous even under a narrow FOV.
