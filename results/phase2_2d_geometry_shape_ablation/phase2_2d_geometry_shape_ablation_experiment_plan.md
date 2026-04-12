# Phase 2 2D Geometry-Shape Ablation Plan

## Goal
Isolate whether the poor 2D `1.9 lambda` behavior is caused primarily by the **slanted/sheared physical layout**, by the larger spacing alone, or by the row sparse pattern changing from `[0,1,4,8]` to `[0,4,7,8]`.

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
- Elevation FOV: `[-15 deg, 15 deg]`
- Minimum azimuth separation: `5 deg`
- Methods: `MUSIC`, `Root-MUSIC`, `ESPRIT`
- Metric: horizontal-angle RMSE

## Hypotheses
- If Group A @ `1.9 lambda` performs much better than Group B @ `1.9 lambda`, then the slanted geometry is the main problem.
- If both `1.9 lambda` geometries perform similarly poorly, then spacing is the dominant factor.
- If Group B @ `0.5 lambda` is close to Group A @ `0.5 lambda`, then the slanted geometry mainly hurts when combined with the larger spacing.
- If Group C is close to Group B, then the changed row pattern `[0,4,7,8]` is the dominant factor.
- If Group C is close to Group A while Group B remains poor, then the slanted 2D layout is the dominant factor.

## Recommended Interpretation
- `0.5 lambda` cases tell us whether the slanted geometry alone is harmful.
- `1.9 lambda` cases tell us whether the slant interacts badly with the wider spacing.
- Group C keeps the row pattern `[0,4,7,8]` but removes the slanted row offsets, so it is the clean control for separating row-pattern effects from 2D layout effects.
