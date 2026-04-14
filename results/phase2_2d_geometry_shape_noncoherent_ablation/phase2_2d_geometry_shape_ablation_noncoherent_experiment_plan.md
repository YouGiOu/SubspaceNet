# Phase 2 2D Geometry-Shape Non-Coherent Ablation Plan

## Goal
Measure how the three 2D geometry families behave under **non-coherent** sources, so we can separate geometry effects from the coherent-signal difficulties already seen in the corresponding coherent study.

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
- Sources: 2 non-coherent narrowband targets
- Snapshot count: `T = 200`
- SNR: `10 dB`
- Horizontal FOV: `[-15 deg, 15 deg]`
- Elevation FOV: `[-15 deg, 15 deg]`
- Minimum azimuth separation: `5 deg`
- Methods: `MUSIC`, `Root-MUSIC`, `ESPRIT`
- Metric: horizontal-angle RMSE

## Hypotheses
- Non-coherent sources should make the baseline and MUSIC paths much easier than in the coherent study.
- If Group B remains clearly worse than Group A even under non-coherent sources, then the difference is mainly geometric rather than coherence-driven.
- If the A/B/C gaps shrink strongly relative to the coherent study, then source coherence was a major amplifier of the geometry differences.
- `SS -> LRMC` should remain the strongest overall path for Root-MUSIC and ESPRIT if the geometry still benefits from preprocessing under non-coherent signals.

## Recommended Interpretation
- Compare this study directly against the coherent geometry-shape ablation to isolate the effect of source coherence.
- Inspect whether Group B, the hardware geometry, remains competitive under non-coherent signals at `1.9 lambda`.
- Use the Group C control to tell apart row-pattern effects from purely slanted-layout effects under the easier non-coherent regime.
