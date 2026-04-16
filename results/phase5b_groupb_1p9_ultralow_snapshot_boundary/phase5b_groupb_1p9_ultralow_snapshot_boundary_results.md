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
| coherent | T = 10 | SS -> LRMC | ESPRIT | 1.8205 |
| coherent | T = 10 | SS -> LRMC | MUSIC | 1.7425 |
| coherent | T = 10 | SS -> LRMC | Root-MUSIC | 1.7328 |
| coherent | T = 2 | SS -> LRMC | ESPRIT | 1.9933 |
| coherent | T = 2 | SS -> LRMC | MUSIC | 1.8923 |
| coherent | T = 2 | SS -> LRMC | Root-MUSIC | 1.9956 |
| coherent | T = 4 | SS -> LRMC | ESPRIT | 1.9295 |
| coherent | T = 4 | SS -> LRMC | MUSIC | 1.8040 |
| coherent | T = 4 | SS -> LRMC | Root-MUSIC | 1.9534 |
| coherent | T = 6 | SS -> LRMC | ESPRIT | 2.0425 |
| coherent | T = 6 | SS -> LRMC | MUSIC | 2.0043 |
| coherent | T = 6 | SS -> LRMC | Root-MUSIC | 2.0207 |
| coherent | T = 8 | SS -> LRMC | ESPRIT | 1.7320 |
| coherent | T = 8 | SS -> LRMC | MUSIC | 1.7593 |
| coherent | T = 8 | SS -> LRMC | Root-MUSIC | 1.7095 |
| non-coherent | T = 1 | SS -> LRMC | ESPRIT | 3.3231 |
| non-coherent | T = 1 | SS -> LRMC | MUSIC | 3.3599 |
| non-coherent | T = 1 | SS -> LRMC | Root-MUSIC | 3.3656 |
| non-coherent | T = 10 | SS -> LRMC | ESPRIT | 0.8434 |
| non-coherent | T = 10 | SS -> LRMC | MUSIC | 0.8741 |
| non-coherent | T = 10 | SS -> LRMC | Root-MUSIC | 0.8792 |
| non-coherent | T = 2 | SS -> LRMC | ESPRIT | 1.8799 |
| non-coherent | T = 2 | SS -> LRMC | MUSIC | 1.9217 |
| non-coherent | T = 2 | SS -> LRMC | Root-MUSIC | 1.9375 |
| non-coherent | T = 4 | SS -> LRMC | ESPRIT | 1.2350 |
| non-coherent | T = 4 | SS -> LRMC | MUSIC | 1.2595 |
| non-coherent | T = 4 | SS -> LRMC | Root-MUSIC | 1.2701 |
| non-coherent | T = 6 | SS -> LRMC | ESPRIT | 1.0097 |
| non-coherent | T = 6 | SS -> LRMC | MUSIC | 1.0603 |
| non-coherent | T = 6 | SS -> LRMC | Root-MUSIC | 1.1309 |
| non-coherent | T = 8 | SS -> LRMC | ESPRIT | 0.8175 |
| non-coherent | T = 8 | SS -> LRMC | MUSIC | 0.8039 |
| non-coherent | T = 8 | SS -> LRMC | Root-MUSIC | 0.7597 |
