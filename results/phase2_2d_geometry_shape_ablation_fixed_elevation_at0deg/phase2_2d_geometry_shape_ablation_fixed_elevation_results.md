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
| Group B @ 0.5 lambda | Baseline | MUSIC | 8.9943 |
| Group B @ 0.5 lambda | Baseline | Root-MUSIC | 26.3429 |
| Group B @ 0.5 lambda | LRMC -> SS | ESPRIT | 6.7390 |
| Group B @ 0.5 lambda | LRMC -> SS | MUSIC | 15.9822 |
| Group B @ 0.5 lambda | LRMC -> SS | Root-MUSIC | 6.2907 |
| Group B @ 0.5 lambda | LRMC only | ESPRIT | 15.3567 |
| Group B @ 0.5 lambda | LRMC only | MUSIC | 11.1723 |
| Group B @ 0.5 lambda | LRMC only | Root-MUSIC | 14.5181 |
| Group B @ 0.5 lambda | SS -> LRMC | ESPRIT | 1.7258 |
| Group B @ 0.5 lambda | SS -> LRMC | MUSIC | 8.2916 |
| Group B @ 0.5 lambda | SS -> LRMC | Root-MUSIC | 4.5950 |
| Group B @ 0.5 lambda | Spatial smoothing only | ESPRIT | 16.7410 |
| Group B @ 0.5 lambda | Spatial smoothing only | MUSIC | 0.1076 |
| Group B @ 0.5 lambda | Spatial smoothing only | Root-MUSIC | 15.9659 |
| Group B @ 1.9 lambda | Baseline | ESPRIT | 6.9910 |
| Group B @ 1.9 lambda | Baseline | MUSIC | 6.2665 |
| Group B @ 1.9 lambda | Baseline | Root-MUSIC | 6.8711 |
| Group B @ 1.9 lambda | LRMC -> SS | ESPRIT | 2.2213 |
| Group B @ 1.9 lambda | LRMC -> SS | MUSIC | 2.1244 |
| Group B @ 1.9 lambda | LRMC -> SS | Root-MUSIC | 2.1195 |
| Group B @ 1.9 lambda | LRMC only | ESPRIT | 4.8991 |
| Group B @ 1.9 lambda | LRMC only | MUSIC | 4.6228 |
| Group B @ 1.9 lambda | LRMC only | Root-MUSIC | 4.7153 |
| Group B @ 1.9 lambda | SS -> LRMC | ESPRIT | 0.5162 |
| Group B @ 1.9 lambda | SS -> LRMC | MUSIC | 0.2980 |
| Group B @ 1.9 lambda | SS -> LRMC | Root-MUSIC | 0.2561 |
| Group B @ 1.9 lambda | Spatial smoothing only | ESPRIT | 5.7061 |
| Group B @ 1.9 lambda | Spatial smoothing only | MUSIC | 0.0945 |
| Group B @ 1.9 lambda | Spatial smoothing only | Root-MUSIC | 6.8355 |
| Group C @ 0.5 lambda | Baseline | ESPRIT | 27.2211 |
| Group C @ 0.5 lambda | Baseline | MUSIC | 8.9943 |
| Group C @ 0.5 lambda | Baseline | Root-MUSIC | 26.3429 |
| Group C @ 0.5 lambda | LRMC -> SS | ESPRIT | 15.2704 |
| Group C @ 0.5 lambda | LRMC -> SS | MUSIC | 21.0387 |
| Group C @ 0.5 lambda | LRMC -> SS | Root-MUSIC | 14.9559 |
| Group C @ 0.5 lambda | LRMC only | ESPRIT | 15.3567 |
| Group C @ 0.5 lambda | LRMC only | MUSIC | 11.1723 |
| Group C @ 0.5 lambda | LRMC only | Root-MUSIC | 14.5181 |
| Group C @ 0.5 lambda | SS -> LRMC | ESPRIT | 15.3982 |
| Group C @ 0.5 lambda | SS -> LRMC | MUSIC | 10.6982 |
| Group C @ 0.5 lambda | SS -> LRMC | Root-MUSIC | 14.5555 |
| Group C @ 0.5 lambda | Spatial smoothing only | ESPRIT | 28.2787 |
| Group C @ 0.5 lambda | Spatial smoothing only | MUSIC | 8.9724 |
| Group C @ 0.5 lambda | Spatial smoothing only | Root-MUSIC | 27.3326 |
| Group C @ 1.9 lambda | Baseline | ESPRIT | 6.9910 |
| Group C @ 1.9 lambda | Baseline | MUSIC | 6.2665 |
| Group C @ 1.9 lambda | Baseline | Root-MUSIC | 6.8711 |
| Group C @ 1.9 lambda | LRMC -> SS | ESPRIT | 4.8140 |
| Group C @ 1.9 lambda | LRMC -> SS | MUSIC | 4.7803 |
| Group C @ 1.9 lambda | LRMC -> SS | Root-MUSIC | 4.7655 |
| Group C @ 1.9 lambda | LRMC only | ESPRIT | 4.8991 |
| Group C @ 1.9 lambda | LRMC only | MUSIC | 4.6228 |
| Group C @ 1.9 lambda | LRMC only | Root-MUSIC | 4.7153 |
| Group C @ 1.9 lambda | SS -> LRMC | ESPRIT | 4.8642 |
| Group C @ 1.9 lambda | SS -> LRMC | MUSIC | 4.8038 |
| Group C @ 1.9 lambda | SS -> LRMC | Root-MUSIC | 4.8098 |
| Group C @ 1.9 lambda | Spatial smoothing only | ESPRIT | 6.9948 |
| Group C @ 1.9 lambda | Spatial smoothing only | MUSIC | 5.9370 |
| Group C @ 1.9 lambda | Spatial smoothing only | Root-MUSIC | 6.8861 |
