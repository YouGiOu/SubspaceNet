# Phase 2 - 2D LRMC / Spatial Smoothing Order Study at 1.9 Lambda with Fixed Elevation

Phase 2 reruns the 2D order comparison at 1.9 lambda with elevation fixed to isolate elevation influence.

Experimental conditions:
- Array: 12-channel row-replicated 2D geometry
- Physical spacing: 1.9 lambda
- Azimuth range: [-15 deg, 15 deg]
- Elevation: fixed to a single angle
- Minimum azimuth separation: 5 deg
- Sources: 2 coherent narrowband targets
- Snapshots: T = 200
- Methods: MUSIC, Root-MUSIC, ESPRIT
- Metric: horizontal-angle RMSE in degrees

| Algorithm | RMSE (deg) |
| --- | ---: |
| Baseline | ESPRIT | 6.9910 |
| Baseline | MUSIC | 7.8517 |
| Baseline | Root-MUSIC | 6.8711 |
| LRMC -> SS | ESPRIT | 8.0259 |
| LRMC -> SS | MUSIC | 7.8855 |
| LRMC -> SS | Root-MUSIC | 8.0605 |
| LRMC only | ESPRIT | 9.3074 |
| LRMC only | MUSIC | 8.7996 |
| LRMC only | Root-MUSIC | 9.1013 |
| SS -> LRMC | ESPRIT | 8.5554 |
| SS -> LRMC | MUSIC | 8.1419 |
| SS -> LRMC | Root-MUSIC | 8.4558 |
| Spatial smoothing only | ESPRIT | 5.7061 |
| Spatial smoothing only | MUSIC | 7.3862 |
| Spatial smoothing only | Root-MUSIC | 6.8355 |
