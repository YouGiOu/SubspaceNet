# Phase 1F - Coherent NULA LRMC Post-Processing Ablation

Phase 1F compares post-LRMC decorrelation strategies on coherent-signal NULA after fixing rank=3, Toeplitz=true, solver=svd, and init=lag.

Experimental conditions:
- Array: NULA [0, 1, 4, 8] on a 0.5 lambda grid
- Virtual ULA size: 9
- Signals: 2 coherent narrowband sources
- Snapshots: T = 200
- SNR: 10 dB
- DOA range: [-90 deg, 90 deg]
- Minimum separation: 15 deg
- Methods: MUSIC, Root-MUSIC, ESPRIT
- Phase 1F focus: post-LRMC decorrelation after fixing rank=3, Toeplitz=true, solver=svd, init=lag
- Metric: DOA RMSE in degrees (periodic matching)

| Algorithm | RMSE (deg) |
| --- | ---: |
| LRMC + FBA (T=200) | ESPRIT | 10.1074 |
| LRMC + FBA (T=200) | MUSIC | 10.3947 |
| LRMC + FBA (T=200) | Root-MUSIC | 9.8865 |
| LRMC + FBA + spatial smoothing (T=200) | ESPRIT | 10.1963 |
| LRMC + FBA + spatial smoothing (T=200) | MUSIC | 10.4618 |
| LRMC + FBA + spatial smoothing (T=200) | Root-MUSIC | 10.3085 |
| LRMC + spatial smoothing (T=200) | ESPRIT | 10.1963 |
| LRMC + spatial smoothing (T=200) | MUSIC | 10.4618 |
| LRMC + spatial smoothing (T=200) | Root-MUSIC | 10.3085 |
| LRMC no post-processing (T=200) | ESPRIT | 10.1074 |
| LRMC no post-processing (T=200) | MUSIC | 10.3026 |
| LRMC no post-processing (T=200) | Root-MUSIC | 9.9553 |
| No LRMC (T=200) | ESPRIT | 30.9618 |
| No LRMC (T=200) | MUSIC | 26.1946 |
| No LRMC (T=200) | Root-MUSIC | 31.1437 |

## Conclusion
- Post-LRMC decorrelation has only a limited effect under the current best coherent-signal LRMC configuration.
- `FBA` is almost neutral: it leaves `ESPRIT` unchanged, slightly worsens `MUSIC`, and gives only a very small gain for `Root-MUSIC`.
- `spatial smoothing` and `FBA + spatial smoothing` are slightly worse than the no-post-processing LRMC baseline.
- This suggests that LRMC plus Toeplitz enforcement has already captured most of the useful structural regularization, leaving little room for additional covariance cleanup.
- The likely reason spatial smoothing does not help more is that it reduces the effective virtual aperture, so the decorrelation benefit is offset by the loss of array resolution.
- Therefore, post-LRMC decorrelation should not become part of the default coherent-signal LRMC pipeline in its current form.
