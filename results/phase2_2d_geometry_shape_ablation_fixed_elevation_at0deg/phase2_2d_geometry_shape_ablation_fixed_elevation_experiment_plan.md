# Phase 2 2D Geometry-Shape Ablation with Fixed Elevation

## Goal
Re-run the Group A / Group B / Group C geometry-shape ablation with the elevation angle fixed at `0 deg` to test whether elevation-dependent phase progression is the main reason the slanted geometry violates the virtual-ULA LRMC prior, while also separating slanted-layout effects from the `[0,4,7,8]` row-pattern effect.

## Geometry Cases
- Group A @ `0.5 lambda`
- Group B @ `0.5 lambda`
- Group C @ `0.5 lambda`
- Group A @ `1.9 lambda`
- Group B @ `1.9 lambda`
- Group C @ `1.9 lambda`

## Processing Paths
- Baseline: no LRMC, no smoothing
- Spatial smoothing only
- LRMC only
- Spatial smoothing -> LRMC
- LRMC -> spatial smoothing

## Fixed Conditions
- Array size: 12 channels
- Sources: 2 coherent narrowband targets
- Snapshot count: `T = 200`
- SNR: `10 dB`
- Horizontal FOV: `[-15 deg, 15 deg]`
- Elevation: fixed at `0 deg`
- Minimum azimuth separation: `5 deg`
- Methods: `MUSIC`, `Root-MUSIC`, `ESPRIT`
- Metric: horizontal-angle RMSE

## Hypothesis Check
- If Group B improves sharply when elevation is fixed, then the slanted geometry is mainly failing because the elevation-dependent phase progression breaks the Toeplitz / virtual-ULA approximation.
- If Group B remains poor even with fixed elevation, then the geometry mismatch itself is the dominant problem, not elevation variation.
- If Group A changes only slightly while Group B changes a lot, that is strong evidence that the slanted layout is uniquely sensitive to elevation coupling.
- If Group C tracks Group B more closely than Group A, then the `[0,4,7,8]` row pattern is itself the dominant difficulty.
- If Group C tracks Group A while Group B remains poor, then the slanted 2D placement is the dominant difficulty.
