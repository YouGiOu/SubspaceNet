# Phase 1E - Coherent NULA LRMC Initialization Ablation

Phase 1E compares LRMC initialization strategies on coherent-signal NULA after fixing rank=3, Toeplitz=true, and solver=svd.

Experimental conditions:
- Array: NULA [0, 1, 4, 8] on a 0.5 lambda grid
- Virtual ULA size: 9
- Signals: 2 coherent narrowband sources
- Snapshots: T = 200
- SNR: 10 dB
- DOA range: [-90 deg, 90 deg]
- Minimum separation: 15 deg
- Methods: MUSIC, Root-MUSIC, ESPRIT
- Phase 1E focus: initialization comparison after fixing rank=3, Toeplitz=true, solver=svd
- Metric: DOA RMSE in degrees (periodic matching)

| Algorithm | RMSE (deg) |
| --- | ---: |
| LRMC init=lag, Toeplitz on (T=200) | ESPRIT | 10.1074 |
| LRMC init=lag, Toeplitz on (T=200) | MUSIC | 10.3026 |
| LRMC init=lag, Toeplitz on (T=200) | Root-MUSIC | 9.9553 |
| LRMC init=neighbor, Toeplitz on (T=200) | ESPRIT | 11.1160 |
| LRMC init=neighbor, Toeplitz on (T=200) | MUSIC | 11.6603 |
| LRMC init=neighbor, Toeplitz on (T=200) | Root-MUSIC | 11.2025 |
| LRMC init=random, Toeplitz on (T=200) | ESPRIT | 10.1715 |
| LRMC init=random, Toeplitz on (T=200) | MUSIC | 10.5069 |
| LRMC init=random, Toeplitz on (T=200) | Root-MUSIC | 9.8625 |
| LRMC init=zero, Toeplitz on (T=200) | ESPRIT | 10.1074 |
| LRMC init=zero, Toeplitz on (T=200) | MUSIC | 10.3026 |
| LRMC init=zero, Toeplitz on (T=200) | Root-MUSIC | 9.9553 |
| No LRMC (T=200) | ESPRIT | 30.9618 |
| No LRMC (T=200) | MUSIC | 26.1946 |
| No LRMC (T=200) | Root-MUSIC | 31.1437 |

## Conclusion
- Initialization sensitivity is weak under the current coherent-signal LRMC configuration.
- `lag` and `zero` are effectively tied, while `random` is very close and even slightly better for `Root-MUSIC` only.
- `neighbor` is consistently worse than the other initialization choices.
- Because `lag` is deterministic, stable, and already among the best settings, it remains the most reasonable default initialization for the next stage.
