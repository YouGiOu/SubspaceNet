# Paper Table I Reproduction - NULA + LRMC

Paper-style comparison for the NULA [0,1,4,8] using LRMC before classical subspace estimation.

Experimental conditions:
- Array: NULA [0, 1, 4, 8] on a 0.5 lambda grid
- Virtual ULA size: 9
- Signals: 2 coherent narrowband sources
- Snapshots: T = 100
- SNR: 10 dB
- DOA range: [-90 deg, 90 deg]
- Minimum separation: 15 deg
- LRMC: rank 3, solver svd
- Metric: DOA RMSE in degrees (periodic matching)

| Algorithm | RMSE (deg) |
| --- | ---: |
| LRMC + ESPRIT | 10.9278 |
| LRMC + MUSIC | 12.2555 |
| LRMC + Root-MUSIC | 11.3808 |
| LRMC + SubspaceNet + ESPRIT | 9.1651 |
| LRMC + SubspaceNet + Root-MUSIC | 10.7068 |
