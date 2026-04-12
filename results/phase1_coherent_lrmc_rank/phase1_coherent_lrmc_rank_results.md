# Phase 1B - Coherent NULA LRMC Rank Ablation

Phase 1B evaluates coherent-signal LRMC rank sensitivity on NULA at the strongest snapshot regime identified in Phase 1A.

Experimental conditions:
- Array: NULA [0, 1, 4, 8] on a 0.5 lambda grid
- Virtual ULA size: 9
- Signals: 2 coherent narrowband sources
- Snapshots: T = 200
- SNR: 10 dB
- DOA range: [-90 deg, 90 deg]
- Minimum separation: 15 deg
- Methods: MUSIC, Root-MUSIC, ESPRIT
- Phase 1B focus: LRMC rank sensitivity at the strongest snapshot regime from Phase 1A
- LRMC solver fixed to svd, init fixed to lag, Toeplitz disabled
- Metric: DOA RMSE in degrees (periodic matching)

| Algorithm | RMSE (deg) |
| --- | ---: |
| LRMC rank=2 (T=200) | ESPRIT | 12.8339 |
| LRMC rank=2 (T=200) | MUSIC | 13.6922 |
| LRMC rank=2 (T=200) | Root-MUSIC | 12.5525 |
| LRMC rank=3 (T=200) | ESPRIT | 10.2403 |
| LRMC rank=3 (T=200) | MUSIC | 11.7051 |
| LRMC rank=3 (T=200) | Root-MUSIC | 10.5215 |
| LRMC rank=4 (T=200) | ESPRIT | 15.9814 |
| LRMC rank=4 (T=200) | MUSIC | 15.2750 |
| LRMC rank=4 (T=200) | Root-MUSIC | 15.3948 |
| LRMC rank=5 (T=200) | ESPRIT | 16.2117 |
| LRMC rank=5 (T=200) | MUSIC | 15.9101 |
| LRMC rank=5 (T=200) | Root-MUSIC | 16.3514 |
| No LRMC (T=200) | ESPRIT | 30.9618 |
| No LRMC (T=200) | MUSIC | 26.1946 |
| No LRMC (T=200) | Root-MUSIC | 31.1437 |
