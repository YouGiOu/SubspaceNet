# Phase 3d 1D NULA Pattern Control at 1.9 Lambda

## Goal
Test whether the remaining Group A vs Group C gap comes from a real 1D sparse-row difference or from a residual implementation asymmetry.

## Runs
For each row pattern:
- Baseline
- LRMC only
- LRMC -> SS

Row patterns:
- Pattern A: `[0, 1, 4, 8]`
- Pattern C: `[0, 4, 7, 8]`

## Conditions
- Array: 1D sparse NULA
- Spacing: `1.9 lambda`
- Sources: 2 coherent narrowband targets
- Snapshot count: `T = 200`
- SNR: `10 dB`
- FOV: `[-15 deg, 15 deg]`
- Minimum separation: `5 deg`
- Methods: `MUSIC`, `Root-MUSIC`, `ESPRIT`

## Interpretation
- If Pattern A and Pattern C are nearly identical in 1D, then the remaining 2D Group A vs Group C gap is not coming from the row pattern itself.
- If Pattern C is still noticeably worse in 1D, then the row pattern `[0,4,7,8]` is intrinsically harder for the current LRMC and subspace pipeline.
