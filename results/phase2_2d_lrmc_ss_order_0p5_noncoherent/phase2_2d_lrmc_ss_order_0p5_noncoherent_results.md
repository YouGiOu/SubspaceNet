# Phase 2 - 2D LRMC / Spatial Smoothing Order Study at 0.5 Lambda, Non-Coherent Signals

Phase 2 reruns the 2D order comparison with the row-replicated array rescaled to 0.5 lambda spacing and non-coherent sources.

Experimental conditions:
- Array: 12-channel row-replicated 2D geometry
- Physical spacing: 0.5 lambda
- Azimuth and elevation range: [-15 deg, 15 deg]
- Minimum azimuth separation: 5 deg
- Sources: 2 non-coherent narrowband targets
- Snapshots: T = 200
- Methods: MUSIC, Root-MUSIC, ESPRIT
- Metric: horizontal-angle RMSE in degrees

| Algorithm | RMSE (deg) |
| --- | ---: |
| Baseline | ESPRIT | 17.3575 |
| Baseline | MUSIC | 0.1178 |
| Baseline | Root-MUSIC | 15.7336 |
| LRMC -> SS | ESPRIT | 0.2166 |
| LRMC -> SS | MUSIC | 0.5876 |
| LRMC -> SS | Root-MUSIC | 0.2666 |
| LRMC only | ESPRIT | 0.1596 |
| LRMC only | MUSIC | 0.2538 |
| LRMC only | Root-MUSIC | 0.1763 |
| SS -> LRMC | ESPRIT | 0.1512 |
| SS -> LRMC | MUSIC | 0.1665 |
| SS -> LRMC | Root-MUSIC | 0.1624 |
| Spatial smoothing only | ESPRIT | 17.3546 |
| Spatial smoothing only | MUSIC | 0.1159 |
| Spatial smoothing only | Root-MUSIC | 15.7303 |
