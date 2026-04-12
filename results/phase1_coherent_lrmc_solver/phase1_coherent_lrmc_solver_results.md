# Phase 1D - Coherent NULA LRMC Solver Ablation

Phase 1D compares LRMC solver choices on coherent-signal NULA after fixing rank=3 and enabling Toeplitz.

Experimental conditions:
- Array: NULA [0, 1, 4, 8] on a 0.5 lambda grid
- Virtual ULA size: 9
- Signals: 2 coherent narrowband sources
- Snapshots: T = 200
- SNR: 10 dB
- DOA range: [-90 deg, 90 deg]
- Minimum separation: 15 deg
- Methods: MUSIC, Root-MUSIC, ESPRIT
- Phase 1D focus: solver comparison after fixing rank=3 and enabling Toeplitz
- LRMC rank fixed to 3, init fixed to lag, Toeplitz enabled
- Metric: DOA RMSE in degrees (periodic matching)

| Algorithm | RMSE (deg) |
| --- | ---: |
| LRMC solver=nuclear, Toeplitz on (T=200) | ESPRIT | 13.5819 |
| LRMC solver=nuclear, Toeplitz on (T=200) | MUSIC | 14.2414 |
| LRMC solver=nuclear, Toeplitz on (T=200) | Root-MUSIC | 13.5829 |
| LRMC solver=svd, Toeplitz on (T=200) | ESPRIT | 10.1074 |
| LRMC solver=svd, Toeplitz on (T=200) | MUSIC | 10.3026 |
| LRMC solver=svd, Toeplitz on (T=200) | Root-MUSIC | 9.9553 |
| No LRMC (T=200) | ESPRIT | 30.9618 |
| No LRMC (T=200) | MUSIC | 26.1946 |
| No LRMC (T=200) | Root-MUSIC | 31.1437 |

## Conclusion
- Under the current coherent-signal LRMC setting, the `svd` solver performs better than the `nuclear` solver for all three classical methods.
- The `svd` solver also ran much faster during the experiment, so it is preferable in both accuracy and efficiency.
- The `nuclear` solver does not provide enough benefit to justify its added computational cost in the current setup.
- Therefore, the coherent-signal LRMC pipeline should keep `solver=svd` fixed in the next stage.
