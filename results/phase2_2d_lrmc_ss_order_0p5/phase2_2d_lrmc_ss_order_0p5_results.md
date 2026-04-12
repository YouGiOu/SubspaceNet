# Phase 2 - 2D LRMC / Spatial Smoothing Order Study at 0.5 Lambda

Phase 2 reruns the 2D order comparison with the row-replicated array rescaled to 0.5 lambda spacing.

Experimental conditions:
- Array: 12-channel row-replicated 2D geometry
- Physical spacing: 0.5 lambda
- Azimuth and elevation range: [-15 deg, 15 deg]
- Minimum azimuth separation: 5 deg
- Sources: 2 coherent narrowband targets
- Snapshots: T = 200
- Methods: MUSIC, Root-MUSIC, ESPRIT
- Metric: horizontal-angle RMSE in degrees

| Algorithm | RMSE (deg) |
| --- | ---: |
| Baseline | ESPRIT | 26.5747 |
| Baseline | MUSIC | 23.4916 |
| Baseline | Root-MUSIC | 26.8516 |
| LRMC -> SS | ESPRIT | 2.2651 |
| LRMC -> SS | MUSIC | 5.3956 |
| LRMC -> SS | Root-MUSIC | 2.4119 |
| LRMC only | ESPRIT | 9.2546 |
| LRMC only | MUSIC | 9.7899 |
| LRMC only | Root-MUSIC | 8.4482 |
| SS -> LRMC | ESPRIT | 1.3120 |
| SS -> LRMC | MUSIC | 4.1220 |
| SS -> LRMC | Root-MUSIC | 2.1714 |
| Spatial smoothing only | ESPRIT | 17.6523 |
| Spatial smoothing only | MUSIC | 0.8326 |
| Spatial smoothing only | Root-MUSIC | 15.9838 |


## Summary
This 0.5 lambda rerun is substantially more favorable than the earlier 1.9 lambda case. The lower spacing restores a much cleaner array manifold, and the preprocessing order now matters in a meaningful way.

Main results:
- Baseline remains relatively weak across all methods.
- LRMC only improves performance substantially, but it is not the best option overall.
- Spatial smoothing only is excellent for MUSIC, but much weaker for Root-MUSIC and ESPRIT.
- SS -> LRMC is the best overall pipeline for Root-MUSIC and ESPRIT.
- LRMC -> SS is close, but consistently a bit worse than SS -> LRMC.

Best results by method:
- MUSIC: Spatial smoothing only, 0.8326 deg
- Root-MUSIC: SS -> LRMC, 2.1714 deg
- ESPRIT: SS -> LRMC, 1.3120 deg

Interpretation:
- The large improvement over the 1.9 lambda study confirms that spacing was the dominant source of ambiguity.
- The 0.5 lambda geometry is much more suitable for covariance completion and classical DOA estimation.
- For the shift-invariant methods, smoothing before LRMC is the preferred order.
- MUSIC appears to benefit most from spatial smoothing alone, and LRMC adds little on top of that for this setup.

Practical conclusion:
- If the goal is a single robust classical pipeline for this 0.5 lambda 2D array, SS -> LRMC is the best default.
- If the goal is MUSIC only, spatial smoothing alone is the simplest and strongest choice.
