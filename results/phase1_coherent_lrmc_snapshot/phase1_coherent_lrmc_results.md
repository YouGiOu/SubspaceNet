# Phase 1 - Coherent NULA LRMC Snapshot Ablation

Phase 1 evaluates whether default LRMC improves coherent-signal subspace estimation on NULA before any SubspaceNet training.

Experimental conditions:
- Array: NULA [0, 1, 4, 8] on a 0.5 lambda grid
- Signals: 2 coherent narrowband sources
- SNR: 10 dB
- DOA range: [-90 deg, 90 deg]
- Minimum separation: 15 deg
- Methods: MUSIC, Root-MUSIC, ESPRIT
- Phase 1 focus: snapshot sensitivity and default LRMC benefit
- Snapshot sweep: T in {50, 100, 200, 400}
- Metric: DOA RMSE in degrees (periodic matching)

| Algorithm | RMSE (deg) |
| --- | ---: |
| Default LRMC (T=100) | ESPRIT | 10.9278 |
| Default LRMC (T=100) | MUSIC | 12.3344 |
| Default LRMC (T=100) | Root-MUSIC | 11.4858 |
| Default LRMC (T=200) | ESPRIT | 10.2403 |
| Default LRMC (T=200) | MUSIC | 11.7051 |
| Default LRMC (T=200) | Root-MUSIC | 10.5215 |
| Default LRMC (T=400) | ESPRIT | 10.6434 |
| Default LRMC (T=400) | MUSIC | 11.7431 |
| Default LRMC (T=400) | Root-MUSIC | 10.9623 |
| Default LRMC (T=50) | ESPRIT | 10.6511 |
| Default LRMC (T=50) | MUSIC | 11.7797 |
| Default LRMC (T=50) | Root-MUSIC | 10.9682 |
| No LRMC (T=100) | ESPRIT | 31.2848 |
| No LRMC (T=100) | MUSIC | 26.2546 |
| No LRMC (T=100) | Root-MUSIC | 31.6643 |
| No LRMC (T=200) | ESPRIT | 30.9618 |
| No LRMC (T=200) | MUSIC | 26.1946 |
| No LRMC (T=200) | Root-MUSIC | 31.1437 |
| No LRMC (T=400) | ESPRIT | 31.2671 |
| No LRMC (T=400) | MUSIC | 25.8087 |
| No LRMC (T=400) | Root-MUSIC | 31.6898 |
| No LRMC (T=50) | ESPRIT | 30.9365 |
| No LRMC (T=50) | MUSIC | 24.2413 |
| No LRMC (T=50) | Root-MUSIC | 31.0742 |
