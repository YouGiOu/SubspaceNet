# Phase 1C - Coherent NULA LRMC Toeplitz Ablation

Phase 1C evaluates whether Toeplitz enforcement improves coherent-signal LRMC on NULA after fixing rank=3 from Phase 1B.

Experimental conditions:
- Array: NULA [0, 1, 4, 8] on a 0.5 lambda grid
- Virtual ULA size: 9
- Signals: 2 coherent narrowband sources
- Snapshots: T = 200
- SNR: 10 dB
- DOA range: [-90 deg, 90 deg]
- Minimum separation: 15 deg
- Methods: MUSIC, Root-MUSIC, ESPRIT
- Phase 1C focus: Toeplitz enforcement after fixing rank=3 from Phase 1B
- LRMC solver fixed to svd, init fixed to lag
- Metric: DOA RMSE in degrees (periodic matching)

| Algorithm | RMSE (deg) |
| --- | ---: |
| LRMC rank=3, Toeplitz off (T=200) | ESPRIT | 10.2403 |
| LRMC rank=3, Toeplitz off (T=200) | MUSIC | 11.7051 |
| LRMC rank=3, Toeplitz off (T=200) | Root-MUSIC | 10.5215 |
| LRMC rank=3, Toeplitz on (T=200) | ESPRIT | 10.1074 |
| LRMC rank=3, Toeplitz on (T=200) | MUSIC | 10.3026 |
| LRMC rank=3, Toeplitz on (T=200) | Root-MUSIC | 9.9553 |
| No LRMC (T=200) | ESPRIT | 30.9618 |
| No LRMC (T=200) | MUSIC | 26.1946 |
| No LRMC (T=200) | Root-MUSIC | 31.1437 |

## Conclusion
- Toeplitz enforcement is useful overall under the current coherent-signal LRMC setting.
- The gain is modest rather than dramatic, so Toeplitz should be viewed as a helpful refinement, not the main source of improvement.
- The benefit is strongest for `MUSIC` and `Root-MUSIC`, while `ESPRIT` improves only slightly.
- Since Toeplitz does not hurt and gives the best overall classical result in this stage (`Root-MUSIC = 9.9553 deg`), it is reasonable to keep Toeplitz enabled in the next coherent-signal LRMC study.
