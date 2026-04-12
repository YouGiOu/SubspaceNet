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
| Baseline | ESPRIT | 32.9102 |
| Baseline | MUSIC | 38.1875 |
| Baseline | Root-MUSIC | 32.2944 |
| LRMC -> SS | ESPRIT | 33.6669 |
| LRMC -> SS | MUSIC | 37.6485 |
| LRMC -> SS | Root-MUSIC | 33.6106 |
| LRMC only | ESPRIT | 34.0933 |
| LRMC only | MUSIC | 38.2542 |
| LRMC only | Root-MUSIC | 34.1885 |
| SS -> LRMC | ESPRIT | 34.1618 |
| SS -> LRMC | MUSIC | 38.0366 |
| SS -> LRMC | Root-MUSIC | 34.1794 |
| Spatial smoothing only | ESPRIT | 34.6272 |
| Spatial smoothing only | MUSIC | 38.5196 |
| Spatial smoothing only | Root-MUSIC | 35.6776 |
