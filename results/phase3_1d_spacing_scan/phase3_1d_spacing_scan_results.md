# Phase 3 - 1D Spacing Scan for Coherent NULA LRMC

Phase 3 scans element spacing on the 1D sparse NULA to separate spacing effects from the 2D geometry confound.

Experimental conditions:
- Array: NULA [0, 1, 4, 8] on a 1D grid
- Spacing: 0.5 lambda
- Sources: 2 coherent narrowband targets
- Snapshots: T = 200
- SNR: 10 dB
- DOA range: [-90 deg, 90 deg]
- Minimum separation: 5 deg
- Methods: MUSIC, Root-MUSIC, ESPRIT
- Metric: horizontal-angle RMSE in degrees

| Algorithm | RMSE (deg) |
| --- | ---: |
| 0.5 lambda LRMC | ESPRIT | 9.7307 |
| 0.5 lambda LRMC | MUSIC | 10.5476 |
| 0.5 lambda LRMC | Root-MUSIC | 9.6192 |
| 0.5 lambda no LRMC | ESPRIT | 31.5997 |
| 0.5 lambda no LRMC | MUSIC | 26.5870 |
| 0.5 lambda no LRMC | Root-MUSIC | 32.0789 |
| 1.0 lambda LRMC | ESPRIT | 24.0114 |
| 1.0 lambda LRMC | MUSIC | 31.0806 |
| 1.0 lambda LRMC | Root-MUSIC | 23.8332 |
| 1.0 lambda no LRMC | ESPRIT | 29.0800 |
| 1.0 lambda no LRMC | MUSIC | 30.3840 |
| 1.0 lambda no LRMC | Root-MUSIC | 29.0573 |
| 1.9 lambda LRMC | ESPRIT | 28.4908 |
| 1.9 lambda LRMC | MUSIC | 38.9112 |
| 1.9 lambda LRMC | Root-MUSIC | 28.5756 |
| 1.9 lambda no LRMC | ESPRIT | 32.3578 |
| 1.9 lambda no LRMC | MUSIC | 38.5167 |
| 1.9 lambda no LRMC | Root-MUSIC | 32.2615 |
