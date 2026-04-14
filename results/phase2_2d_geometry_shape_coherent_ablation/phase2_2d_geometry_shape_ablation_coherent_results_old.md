# Phase 2 - 2D Geometry-Shape Ablation

Phase 2 compares rectangular Group A and slanted Group B layouts at 0.5 and 1.9 lambda to separate topology and spacing effects.

Experimental conditions:
- Array: 12-channel 2D geometry derived from the phase-2 array layouts
- Geometry cases: Group A and Group B
- Physical spacings: 0.5 lambda and 1.9 lambda
- Azimuth and elevation range: [-15 deg, 15 deg]
- Minimum azimuth separation: 5 deg
- Sources: 2 coherent narrowband targets
- Snapshots: T = 200
- Methods: MUSIC, Root-MUSIC, ESPRIT
- Metric: horizontal-angle RMSE in degrees

| Geometry | Processing | Method | RMSE (deg) |
| --- | --- | --- | ---: |
| Group A @ 0.5 lambda | Baseline | MUSIC | 9.8204 |
| Group A @ 0.5 lambda | Baseline | Root-MUSIC | 26.8516 |
| Group A @ 0.5 lambda | Baseline | ESPRIT | 26.5747 |
| Group A @ 0.5 lambda | Spatial smoothing only | MUSIC | 0.4915 |
| Group A @ 0.5 lambda | Spatial smoothing only | Root-MUSIC | 15.9838 |
| Group A @ 0.5 lambda | Spatial smoothing only | ESPRIT | 17.6523 |
| Group A @ 0.5 lambda | LRMC only | MUSIC | 12.6993 |
| Group A @ 0.5 lambda | LRMC only | Root-MUSIC | 8.4482 |
| Group A @ 0.5 lambda | LRMC only | ESPRIT | 9.2546 |
| Group A @ 0.5 lambda | SS -> LRMC | MUSIC | 7.4231 |
| Group A @ 0.5 lambda | SS -> LRMC | Root-MUSIC | 2.1714 |
| Group A @ 0.5 lambda | SS -> LRMC | ESPRIT | 1.3120 |
| Group A @ 0.5 lambda | LRMC -> SS | MUSIC | 10.5338 |
| Group A @ 0.5 lambda | LRMC -> SS | Root-MUSIC | 2.4119 |
| Group A @ 0.5 lambda | LRMC -> SS | ESPRIT | 2.2651 |
| Group A @ 1.9 lambda | Baseline | MUSIC | 6.3041 |
| Group A @ 1.9 lambda | Baseline | Root-MUSIC | 6.7963 |
| Group A @ 1.9 lambda | Baseline | ESPRIT | 6.8541 |
| Group A @ 1.9 lambda | Spatial smoothing only | MUSIC | 0.1428 |
| Group A @ 1.9 lambda | Spatial smoothing only | Root-MUSIC | 6.8360 |
| Group A @ 1.9 lambda | Spatial smoothing only | ESPRIT | 6.0407 |
| Group A @ 1.9 lambda | LRMC only | MUSIC | 4.7270 |
| Group A @ 1.9 lambda | LRMC only | Root-MUSIC | 4.8797 |
| Group A @ 1.9 lambda | LRMC only | ESPRIT | 5.1672 |
| Group A @ 1.9 lambda | SS -> LRMC | MUSIC | 1.1022 |
| Group A @ 1.9 lambda | SS -> LRMC | Root-MUSIC | 1.2830 |
| Group A @ 1.9 lambda | SS -> LRMC | ESPRIT | 1.3661 |
| Group A @ 1.9 lambda | LRMC -> SS | MUSIC | 2.4327 |
| Group A @ 1.9 lambda | LRMC -> SS | Root-MUSIC | 2.4253 |
| Group A @ 1.9 lambda | LRMC -> SS | ESPRIT | 2.4917 |
| Group B @ 0.5 lambda | Baseline | MUSIC | 11.8144 |
| Group B @ 0.5 lambda | Baseline | Root-MUSIC | 26.3040 |
| Group B @ 0.5 lambda | Baseline | ESPRIT | 27.0534 |
| Group B @ 0.5 lambda | Spatial smoothing only | MUSIC | 10.5078 |
| Group B @ 0.5 lambda | Spatial smoothing only | Root-MUSIC | 15.6595 |
| Group B @ 0.5 lambda | Spatial smoothing only | ESPRIT | 16.3850 |
| Group B @ 0.5 lambda | LRMC only | MUSIC | 20.6716 |
| Group B @ 0.5 lambda | LRMC only | Root-MUSIC | 31.4671 |
| Group B @ 0.5 lambda | LRMC only | ESPRIT | 31.9036 |
| Group B @ 0.5 lambda | SS -> LRMC | MUSIC | 22.6778 |
| Group B @ 0.5 lambda | SS -> LRMC | Root-MUSIC | 35.8503 |
| Group B @ 0.5 lambda | SS -> LRMC | ESPRIT | 35.5920 |
| Group B @ 0.5 lambda | LRMC -> SS | MUSIC | 28.7605 |
| Group B @ 0.5 lambda | LRMC -> SS | Root-MUSIC | 31.9488 |
| Group B @ 0.5 lambda | LRMC -> SS | ESPRIT | 31.8534 |
| Group B @ 1.9 lambda | Baseline | MUSIC | 7.9686 |
| Group B @ 1.9 lambda | Baseline | Root-MUSIC | 6.8379 |
| Group B @ 1.9 lambda | Baseline | ESPRIT | 7.0124 |
| Group B @ 1.9 lambda | Spatial smoothing only | MUSIC | 7.4562 |
| Group B @ 1.9 lambda | Spatial smoothing only | Root-MUSIC | 6.8221 |
| Group B @ 1.9 lambda | Spatial smoothing only | ESPRIT | 5.6927 |
| Group B @ 1.9 lambda | LRMC only | MUSIC | 8.9439 |
| Group B @ 1.9 lambda | LRMC only | Root-MUSIC | 9.2719 |
| Group B @ 1.9 lambda | LRMC only | ESPRIT | 9.3351 |
| Group B @ 1.9 lambda | SS -> LRMC | MUSIC | 8.3775 |
| Group B @ 1.9 lambda | SS -> LRMC | Root-MUSIC | 8.6257 |
| Group B @ 1.9 lambda | SS -> LRMC | ESPRIT | 8.8413 |
| Group B @ 1.9 lambda | LRMC -> SS | MUSIC | 8.0526 |
| Group B @ 1.9 lambda | LRMC -> SS | Root-MUSIC | 8.4653 |
| Group B @ 1.9 lambda | LRMC -> SS | ESPRIT | 8.5297 |
