# Phase 5C - Group B 1.9 Lambda Fixed-Separation Study

Phase 5C sweeps fixed two-source angular separation on the Group B hardware geometry using the same SS -> LRMC front end as the current classical and SubspaceNet studies.

Experimental conditions:
- Array: Group B 12-channel 2D hardware geometry
- Physical spacing: 1.9 lambda
- Snapshots: T = 200
- Preprocessing: spatial smoothing before LRMC
- Azimuth and elevation range: [-15 deg, 15 deg]
- Fixed azimuth separation sweep: 5, 4, 3, 2, 1 deg
- Sources: 2 narrowband targets
- Methods: MUSIC, Root-MUSIC, ESPRIT
- Metric: horizontal-angle RMSE in degrees

| Geometry | Processing | Method | RMSE (deg) |
| --- | --- | --- | ---: |
| coherent | Gap = 1 deg | SS -> LRMC | ESPRIT | 5.5524 |
| coherent | Gap = 1 deg | SS -> LRMC | MUSIC | 6.3890 |
| coherent | Gap = 1 deg | SS -> LRMC | Root-MUSIC | 5.2237 |
| coherent | Gap = 2 deg | SS -> LRMC | ESPRIT | 3.7526 |
| coherent | Gap = 2 deg | SS -> LRMC | MUSIC | 4.2964 |
| coherent | Gap = 2 deg | SS -> LRMC | Root-MUSIC | 4.1263 |
| coherent | Gap = 3 deg | SS -> LRMC | ESPRIT | 1.3773 |
| coherent | Gap = 3 deg | SS -> LRMC | MUSIC | 1.4823 |
| coherent | Gap = 3 deg | SS -> LRMC | Root-MUSIC | 1.5935 |
| coherent | Gap = 4 deg | SS -> LRMC | ESPRIT | 0.1010 |
| coherent | Gap = 4 deg | SS -> LRMC | MUSIC | 0.1358 |
| coherent | Gap = 4 deg | SS -> LRMC | Root-MUSIC | 0.1218 |
| coherent | Gap = 5 deg | SS -> LRMC | ESPRIT | 1.1560 |
| coherent | Gap = 5 deg | SS -> LRMC | MUSIC | 1.0325 |
| coherent | Gap = 5 deg | SS -> LRMC | Root-MUSIC | 1.0590 |
| non-coherent | Gap = 1 deg | SS -> LRMC | ESPRIT | 0.1011 |
| non-coherent | Gap = 1 deg | SS -> LRMC | MUSIC | 0.3294 |
| non-coherent | Gap = 1 deg | SS -> LRMC | Root-MUSIC | 0.1079 |
| non-coherent | Gap = 2 deg | SS -> LRMC | ESPRIT | 0.0979 |
| non-coherent | Gap = 2 deg | SS -> LRMC | MUSIC | 0.1159 |
| non-coherent | Gap = 2 deg | SS -> LRMC | Root-MUSIC | 0.0983 |
| non-coherent | Gap = 3 deg | SS -> LRMC | ESPRIT | 0.0946 |
| non-coherent | Gap = 3 deg | SS -> LRMC | MUSIC | 0.0977 |
| non-coherent | Gap = 3 deg | SS -> LRMC | Root-MUSIC | 0.0975 |
| non-coherent | Gap = 4 deg | SS -> LRMC | ESPRIT | 0.0934 |
| non-coherent | Gap = 4 deg | SS -> LRMC | MUSIC | 0.0946 |
| non-coherent | Gap = 4 deg | SS -> LRMC | Root-MUSIC | 0.0946 |
| non-coherent | Gap = 5 deg | SS -> LRMC | ESPRIT | 0.0925 |
| non-coherent | Gap = 5 deg | SS -> LRMC | MUSIC | 0.0935 |
| non-coherent | Gap = 5 deg | SS -> LRMC | Root-MUSIC | 0.0936 |
