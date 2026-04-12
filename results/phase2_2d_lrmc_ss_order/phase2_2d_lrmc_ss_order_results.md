# Phase 2 - 2D LRMC / Spatial Smoothing Order Study

Phase 2 compares spatial smoothing only, LRMC only, and both processing orders on the 2D 12-channel array with 1.9 lambda spacing.

Experimental conditions:
- Array: 12-channel 2D geometry derived from radar_array_geometry.cpp
- Physical spacing: 1.9 lambda
- Azimuth and elevation range: [-15 deg, 15 deg]
- Minimum azimuth separation: 5 deg
- Sources: 2 coherent narrowband targets
- Snapshots: T = 200
- Methods: MUSIC, Root-MUSIC, ESPRIT
- Metric: horizontal-angle RMSE in degrees

| Algorithm | RMSE (deg) |
| --- | ---: |
| Baseline | ESPRIT | 7.0124 |
| Baseline | MUSIC | 7.9686 |
| Baseline | Root-MUSIC | 6.8379 |
| LRMC -> SS | ESPRIT | 8.5297 |
| LRMC -> SS | MUSIC | 8.0526 |
| LRMC -> SS | Root-MUSIC | 8.4653 |
| LRMC only | ESPRIT | 9.3351 |
| LRMC only | MUSIC | 8.9439 |
| LRMC only | Root-MUSIC | 9.2719 |
| SS -> LRMC | ESPRIT | 8.8413 |
| SS -> LRMC | MUSIC | 8.3775 |
| SS -> LRMC | Root-MUSIC | 8.6257 |
| Spatial smoothing only | ESPRIT | 5.6927 |
| Spatial smoothing only | MUSIC | 7.4562 |
| Spatial smoothing only | Root-MUSIC | 6.8221 |
