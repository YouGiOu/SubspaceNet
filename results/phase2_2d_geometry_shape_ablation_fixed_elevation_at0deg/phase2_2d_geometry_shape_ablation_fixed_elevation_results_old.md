# Phase 2 - 2D Geometry-Shape Ablation with Fixed Elevation

Phase 2 compares rectangular Group A and slanted Group B layouts at 0.5 and 1.9 lambda with elevation fixed at 0 deg to isolate elevation-dependent phase effects.

Experimental conditions:
- Array: 12-channel 2D geometry derived from the phase-2 array layouts
- Geometry: Group A @ 0.5 lambda
- Physical spacings: 0.5 lambda and 1.9 lambda across the experiment family
- Azimuth range: [-15 deg, 15 deg]
- Elevation: fixed at 0 deg
- Minimum azimuth separation: 5 deg
- Sources: 2 coherent narrowband targets
- Snapshots: T = 200
- Methods: MUSIC, Root-MUSIC, ESPRIT
- Metric: horizontal-angle RMSE in degrees

| Geometry | Processing | Method | RMSE (deg) |
| --- | --- | --- | ---: |
| Group A @ 0.5 lambda | Baseline | ESPRIT | 26.0885 |
| Group A @ 0.5 lambda | Baseline | MUSIC | 9.7426 |
| Group A @ 0.5 lambda | Baseline | Root-MUSIC | 26.5986 |
| Group A @ 0.5 lambda | LRMC -> SS | ESPRIT | 1.3169 |
| Group A @ 0.5 lambda | LRMC -> SS | MUSIC | 9.5612 |
| Group A @ 0.5 lambda | LRMC -> SS | Root-MUSIC | 1.6720 |
| Group A @ 0.5 lambda | LRMC only | ESPRIT | 1.1038 |
| Group A @ 0.5 lambda | LRMC only | MUSIC | 7.2357 |
| Group A @ 0.5 lambda | LRMC only | Root-MUSIC | 2.2286 |
| Group A @ 0.5 lambda | SS -> LRMC | ESPRIT | 1.0611 |
| Group A @ 0.5 lambda | SS -> LRMC | MUSIC | 6.9181 |
| Group A @ 0.5 lambda | SS -> LRMC | Root-MUSIC | 2.3264 |
| Group A @ 0.5 lambda | Spatial smoothing only | ESPRIT | 26.8409 |
| Group A @ 0.5 lambda | Spatial smoothing only | MUSIC | 9.8182 |
| Group A @ 0.5 lambda | Spatial smoothing only | Root-MUSIC | 27.4199 |
| Group A @ 1.9 lambda | Baseline | ESPRIT | 6.5432 |
| Group A @ 1.9 lambda | Baseline | MUSIC | 4.8781 |
| Group A @ 1.9 lambda | Baseline | Root-MUSIC | 6.4658 |
| Group A @ 1.9 lambda | LRMC -> SS | ESPRIT | 2.8085 |
| Group A @ 1.9 lambda | LRMC -> SS | MUSIC | 2.6677 |
| Group A @ 1.9 lambda | LRMC -> SS | Root-MUSIC | 2.8465 |
| Group A @ 1.9 lambda | LRMC only | ESPRIT | 3.1752 |
| Group A @ 1.9 lambda | LRMC only | MUSIC | 3.0281 |
| Group A @ 1.9 lambda | LRMC only | Root-MUSIC | 2.9245 |
| Group A @ 1.9 lambda | SS -> LRMC | ESPRIT | 3.1878 |
| Group A @ 1.9 lambda | SS -> LRMC | MUSIC | 2.9921 |
| Group A @ 1.9 lambda | SS -> LRMC | Root-MUSIC | 3.0212 |
| Group A @ 1.9 lambda | Spatial smoothing only | ESPRIT | 6.4944 |
| Group A @ 1.9 lambda | Spatial smoothing only | MUSIC | 5.2210 |
| Group A @ 1.9 lambda | Spatial smoothing only | Root-MUSIC | 6.6923 |
| Group B @ 0.5 lambda | Baseline | ESPRIT | 27.2211 |
| Group B @ 0.5 lambda | Baseline | MUSIC | 11.9905 |
| Group B @ 0.5 lambda | Baseline | Root-MUSIC | 26.3429 |
| Group B @ 0.5 lambda | LRMC -> SS | ESPRIT | 35.5630 |
| Group B @ 0.5 lambda | LRMC -> SS | MUSIC | 28.6123 |
| Group B @ 0.5 lambda | LRMC -> SS | Root-MUSIC | 34.9761 |
| Group B @ 0.5 lambda | LRMC only | ESPRIT | 32.6259 |
| Group B @ 0.5 lambda | LRMC only | MUSIC | 21.5400 |
| Group B @ 0.5 lambda | LRMC only | Root-MUSIC | 32.2202 |
| Group B @ 0.5 lambda | SS -> LRMC | ESPRIT | 39.4546 |
| Group B @ 0.5 lambda | SS -> LRMC | MUSIC | 22.7469 |
| Group B @ 0.5 lambda | SS -> LRMC | Root-MUSIC | 39.0300 |
| Group B @ 0.5 lambda | Spatial smoothing only | ESPRIT | 16.7410 |
| Group B @ 0.5 lambda | Spatial smoothing only | MUSIC | 10.5081 |
| Group B @ 0.5 lambda | Spatial smoothing only | Root-MUSIC | 15.9659 |
| Group B @ 1.9 lambda | Baseline | ESPRIT | 6.9910 |
| Group B @ 1.9 lambda | Baseline | MUSIC | 7.8517 |
| Group B @ 1.9 lambda | Baseline | Root-MUSIC | 6.8711 |
| Group B @ 1.9 lambda | LRMC -> SS | ESPRIT | 8.0259 |
| Group B @ 1.9 lambda | LRMC -> SS | MUSIC | 7.8855 |
| Group B @ 1.9 lambda | LRMC -> SS | Root-MUSIC | 8.0605 |
| Group B @ 1.9 lambda | LRMC only | ESPRIT | 9.3074 |
| Group B @ 1.9 lambda | LRMC only | MUSIC | 8.7996 |
| Group B @ 1.9 lambda | LRMC only | Root-MUSIC | 9.1013 |
| Group B @ 1.9 lambda | SS -> LRMC | ESPRIT | 8.5554 |
| Group B @ 1.9 lambda | SS -> LRMC | MUSIC | 8.1419 |
| Group B @ 1.9 lambda | SS -> LRMC | Root-MUSIC | 8.4558 |
| Group B @ 1.9 lambda | Spatial smoothing only | ESPRIT | 5.7061 |
| Group B @ 1.9 lambda | Spatial smoothing only | MUSIC | 7.3862 |
| Group B @ 1.9 lambda | Spatial smoothing only | Root-MUSIC | 6.8355 |
