# Phase 7C - Group B 1.9 Lambda SubspaceNet Backbone 3x3

Phase 7C runs the new `3x3` SubspaceNet-backbone variants only and compares them against the already completed `2x2` backbone references from Phase 7B in the same coherent hard cell.

Experimental conditions:
- Array: Group B 12-channel 2D hardware geometry
- Physical spacing: 1.9 lambda
- Signals: 2 coherent narrowband targets
- Cell: gap = 1 deg, SNR = 1 dB, T = 40
- Azimuth and elevation range: [-15 deg, 15 deg]
- Training scale: 45,000 samples total with 9,000 test samples
- Learned head: ESPRIT
- Controlled variable: SubspaceNet backbone kernel size 2x2 vs 3x3

## New 3x3 Runs

| Scheme | Fusion Type | Backbone | RMSE (deg) |
| --- | --- | --- | ---: |
| SS(3/3) | none | 3x3 | 0.4087 |
| SS(2/3: rows 0+1) | none | 3x3 | 0.5386 |
| SS(2/3 x 3) learned fusion | spatial 3x3 fusion | 3x3 | 0.4118 |
| SS(2/3 x 3) 1x1 learned fusion | 1x1 channel-only fusion | 3x3 | 0.4396 |

## Direct Comparison Against 2x2 References

| Scheme | Fusion Type | 2x2 RMSE (deg) | 3x3 RMSE (deg) | Delta (3x3 - 2x2) |
| --- | --- | ---: | ---: | ---: |
| SS(3/3) | none | 0.4747 | 0.4087 | -0.0660 |
| SS(2/3: rows 0+1) | none | 0.6995 | 0.5386 | -0.1610 |
| SS(2/3 x 3) learned fusion | spatial 3x3 fusion | 0.4516 | 0.4118 | -0.0398 |
| SS(2/3 x 3) 1x1 learned fusion | 1x1 channel-only fusion | 0.5414 | 0.4396 | -0.1018 |
