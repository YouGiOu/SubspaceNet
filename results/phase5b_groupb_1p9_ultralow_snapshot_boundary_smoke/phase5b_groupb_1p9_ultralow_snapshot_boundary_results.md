# Phase 5B - Group B 1.9 Lambda Ultra-Low Snapshot Boundary Study

Phase 5B extends the Group B snapshot sweep down to T = 1, 2, 4, 6, 8, 10 using the same SS -> LRMC front end as the SubspaceNet studies, to identify the true ultra-low-snapshot boundary for coherent and non-coherent signals.

Experimental conditions:
- Array: Group B 12-channel 2D hardware geometry
- Physical spacing: 1.9 lambda
- Preprocessing: spatial smoothing before LRMC
- Azimuth and elevation range: [-15 deg, 15 deg]
- Minimum azimuth separation: 5 deg
- Sources: 2 narrowband targets
- Snapshot sweep: T = 1, 2, 4, 6, 8, 10
- Methods: MUSIC, Root-MUSIC, ESPRIT
- Metric: horizontal-angle RMSE in degrees

| Geometry | Processing | Method | RMSE (deg) |
| --- | --- | --- | ---: |
| coherent | T = 1 | SS -> LRMC | ESPRIT | 1.9576 |
| coherent | T = 1 | SS -> LRMC | MUSIC | 1.9329 |
| coherent | T = 1 | SS -> LRMC | Root-MUSIC | 1.9066 |
