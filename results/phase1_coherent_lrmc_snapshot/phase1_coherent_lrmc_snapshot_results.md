# Phase 1A Coherent NULA LRMC Snapshot Ablation Results

## Purpose
This document records **Phase 1A** only: a classical-method snapshot ablation for coherent signals on the NULA `[0, 1, 4, 8]`. The goal of this stage was to test whether default LRMC improves coherent-source DOA estimation before any further LRMC tuning or SubspaceNet retraining.

## Experimental Conditions
- Array: NULA `[0, 1, 4, 8]` on a `0.5 lambda` grid
- Virtual ULA size: `9`
- Signals: `2` coherent narrowband sources
- SNR: `10 dB`
- DOA range: `[-90 deg, 90 deg]`
- Minimum separation: `15 deg`
- Methods: `MUSIC`, `Root-MUSIC`, `ESPRIT`
- Snapshot sweep: `T in {50, 100, 200, 400}`
- LRMC comparison:
  - no LRMC baseline
  - default LRMC with `rank=3`, `solver=svd`, `init=lag`, `toeplitz=false`
- Metric: DOA RMSE in degrees (periodic matching)
- Seed: `42`

## Methodological Note
In the no-LRMC branch, the algorithms were run on the physical NULA directly.

- `MUSIC` remains geometry-aware because it uses the explicit sensor positions in the steering-vector calculation.
- `Root-MUSIC` and `ESPRIT` were **not** degraded to a 4-element ULA before execution.
- As a result, the no-LRMC `Root-MUSIC` and `ESPRIT` entries are best interpreted as direct-NULA stress baselines, not as fully geometry-valid ULA-method baselines.

By contrast, the LRMC branch first completes the sparse-array covariance onto a virtual ULA of size `9`, so `Root-MUSIC` and `ESPRIT` are being applied in a much more appropriate setting there.

## Scope Note
Only the **snapshot experiment** has been completed so far.

The following planned coherent-signal LRMC studies have **not** been run yet:
- LRMC rank sweep
- LRMC solver comparison
- LRMC initialization comparison
- Toeplitz enforcement ablation
- post-LRMC decorrelation
- SubspaceNet retraining after LRMC tuning

## Results
| Setting | MUSIC | ESPRIT | Root-MUSIC |
| --- | ---: | ---: | ---: |
| No LRMC (T=50) | 24.2413 | 30.9365 | 31.0742 |
| Default LRMC (T=50) | 11.7797 | 10.6511 | 10.9682 |
| No LRMC (T=100) | 26.2546 | 31.2848 | 31.6643 |
| Default LRMC (T=100) | 12.3344 | 10.9278 | 11.4858 |
| No LRMC (T=200) | 26.1946 | 30.9618 | 31.1437 |
| Default LRMC (T=200) | 11.7051 | 10.2403 | 10.5215 |
| No LRMC (T=400) | 25.8087 | 31.2671 | 31.6898 |
| Default LRMC (T=400) | 11.7431 | 10.6434 | 10.9623 |

## Key Findings
- Default LRMC improved all three classical methods at every tested snapshot count.
- The improvement was large and stable across the full sweep.
- Without LRMC, increasing snapshots from `50` to `400` barely helped. The coherent NULA baseline remained poor, roughly `24-26 deg` for MUSIC and about `31 deg` for ESPRIT and Root-MUSIC.
- With default LRMC, the error dropped to about `10-12 deg` for all three methods, which shows that covariance completion is doing useful work even in the coherent case.
- ESPRIT was the best method after LRMC at every tested snapshot count. The best overall result in this stage was `Default LRMC (T=200) | ESPRIT = 10.2403 deg`.
- Root-MUSIC was consistently close to ESPRIT after LRMC, while MUSIC remained slightly worse.

## Improvement Magnitude
Approximate LRMC gain relative to the no-LRMC baseline:
- MUSIC: about `51%` to `55%` RMSE reduction
- ESPRIT: about `65%` to `67%` RMSE reduction
- Root-MUSIC: about `64%` to `66%` RMSE reduction

## Interpretation
The main conclusion from Phase 1A is that **default LRMC is clearly useful for coherent NULA signals**, and the gain is not marginal. It converts a very weak coherent-source baseline into a much more usable virtual covariance for classical subspace estimation.

At the same time, the snapshot sweep also suggests that **more snapshots alone are not the main missing ingredient**. The no-LRMC curves remain poor even as `T` increases, and the LRMC curves do not keep improving monotonically beyond `T=200`. This means the next bottleneck is likely **LRMC configuration and structure modeling**, not simply sample size.

One caution is important here: part of the large improvement for `Root-MUSIC` and `ESPRIT` comes from moving those methods from an ill-matched direct-NULA setting into an LRMC-generated virtual ULA setting. So the observed gain should be interpreted as the combined benefit of covariance completion and geometry regularization, not only as a generic denoising effect.

## Recommended Next Step
The next stage should keep the coherent NULA setting fixed and tune LRMC itself around the strongest snapshot regime, with `T=200` as the most reasonable starting point. The priority order should be:
1. LRMC rank sweep
2. Toeplitz enforcement ablation
3. solver comparison (`svd` vs `nuclear`)
4. initialization comparison
5. post-LRMC decorrelation

Only after the best coherent-signal LRMC configuration is identified should SubspaceNet be added back into the experiment chain.
