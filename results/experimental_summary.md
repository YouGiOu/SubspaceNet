# Experimental Summary

This document summarizes the current experimental results across the coherent and non-coherent NULA studies, the 1D spacing scan, the 2D row-replicated array studies, and the SubspaceNet baseline runs.

## 1. Main Takeaways

- Array spacing has a strong effect on the classical subspace pipeline, but it is not the only factor.
- For the 1D sparse NULA `[0, 1, 4, 8]`, `0.5 lambda` is the most favorable regime for LRMC and classical DOA estimation.
- At `1.9 lambda`, MUSIC can still work very well for non-coherent signals under a narrow FOV, but Root-MUSIC and ESPRIT remain much more fragile.
- The 2D row-replicated array is currently being used as a 2D snapshot generator and then reduced to a 1D surrogate for estimation. This structural mismatch is a major reason why the 2D results are not as strong as the 1D ones.
- Fixing elevation in the 2D experiments does not materially improve the results, so elevation is not the main culprit.
- Root-MUSIC and ESPRIT in the current implementation are highly sensitive to the array model and should be interpreted cautiously on non-ULA or reduced-geometry cases.

## 2. Phase 1: Coherent 1D NULA LRMC Studies

The coherent sparse NULA experiments established the basic behavior of LRMC on the `[0, 1, 4, 8]` geometry.

### Key outcomes

- LRMC helped significantly compared with the raw baseline.
- Toeplitz enforcement and solver changes provided smaller but still meaningful effects.
- The coherent 1D setting is the first regime where LRMC clearly adds value over the direct baseline.

### Representative result

From the coherent LRMC results:
- Baseline MUSIC was around the mid-20 degree range.
- LRMC reduced MUSIC / Root-MUSIC / ESPRIT to roughly the 10 degree range in the best coherent 1D setups.

## 3. Phase 3: 1D Spacing Scan

The spacing scan showed that spacing matters a lot for coherent sparse NULA processing.

### Observed trend

- `0.5 lambda`: LRMC is very effective.
- `1.0 lambda`: LRMC still helps, but the gain is much smaller.
- `1.9 lambda`: LRMC benefit is largely lost for the coherent 1D case.

### Representative RMSE values

| Spacing | MUSIC baseline | MUSIC + LRMC | Root-MUSIC baseline | Root-MUSIC + LRMC | ESPRIT baseline | ESPRIT + LRMC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.5 lambda | 26.59 | 10.55 | 32.08 | 9.62 | 31.60 | 9.73 |
| 1.0 lambda | 30.38 | 31.08 | 29.06 | 23.83 | 29.08 | 24.01 |
| 1.9 lambda | 38.50 | 38.90 | 32.26 | 28.58 | 32.36 | 28.49 |

### Interpretation

- The array manifold becomes increasingly difficult as spacing grows.
- LRMC cannot fully recover performance once the geometry becomes too ambiguous.
- This was the first strong evidence that the array geometry, not only the solver, controls the final RMSE.

## 4. Phase 2: 2D Row-Replicated Array, Coherent Signals

The 2D study uses the row-replicated 12-channel geometry with three translated `[0, 1, 4, 8]` rows.

### Important implementation note

The current 2D classical pipeline is still effectively 1D at estimation time:
- baseline uses the canonical row only
- LRMC completes a virtual ULA from the row-reduced covariance
- `SS -> LRMC` and `LRMC -> SS` still end up as 1D surrogate estimators

So the 2D data generation is genuine, but the estimation step is not a true 2D DOA solver.

### Original 2D coherent 1.9 lambda result

The original 2D coherent 1.9 lambda study produced RMSEs around:
- MUSIC: `7.97 deg`
- Root-MUSIC: `6.84 deg`
- ESPRIT: `7.01 deg`

The preprocessing variants were all in a similar range, with spatial smoothing only being the best of the tested options for ESPRIT.

### Fixed-elevation 2D coherent 1.9 lambda result

When elevation was fixed to a single angle, the results changed only slightly:
- MUSIC: `7.85 deg`
- Root-MUSIC: `6.87 deg`
- ESPRIT: `6.99 deg`

This shows that elevation variation is not the main reason the 2D results are weaker.

### Interpretation

- The 2D pipeline is limited mainly by the 2D-to-1D reduction and the fact that the estimators are still fundamentally 1D methods.
- Elevation is a secondary factor, not the dominant one.

## 5. Phase 2: 2D Row-Replicated Array, 0.5 lambda

The 0.5 lambda 2D study was much healthier than the 1.9 lambda version.

### Coherent signals

Best results from the coherent 0.5 lambda 2D study:
- MUSIC: spatial smoothing only, `0.8326 deg`
- Root-MUSIC: `SS -> LRMC`, `2.1714 deg`
- ESPRIT: `SS -> LRMC`, `1.3120 deg`

### Non-coherent signals

Best results from the non-coherent 0.5 lambda 2D study:
- MUSIC: baseline / spatial smoothing only, around `0.116 deg`
- Root-MUSIC: `SS -> LRMC`, `0.1624 deg`
- ESPRIT: `SS -> LRMC`, `0.1512 deg`

### Interpretation

- `0.5 lambda` restores a much cleaner manifold.
- For coherent data, smoothing-first preprocessing is the best choice.
- For non-coherent data, MUSIC is already very strong without LRMC, while Root-MUSIC and ESPRIT still benefit from LRMC.
- `SS -> LRMC` is generally the most reliable order for the shift-invariant methods.

## 6. Phase 3b / 3c: 1D NULA at 1.9 lambda, Coherent vs Non-Coherent

These experiments were used to isolate the effect of coherence and to verify the spacing-aware Root-MUSIC / ESPRIT fix.

### Non-coherent 1.9 lambda NULA

The non-coherent 1.9 lambda NULA results were excellent for MUSIC and very strong after LRMC for all classical methods:
- MUSIC baseline: `0.0177 deg`
- MUSIC + LRMC: `0.1748 deg`
- Root-MUSIC + LRMC: `0.1850 deg`
- ESPRIT + LRMC: `0.1790 deg`
- LRMC -> SS slightly improved the shift-invariant methods further to around `0.145 deg`

### Coherent 1.9 lambda NULA

The coherent 1.9 lambda NULA case was much harder:
- MUSIC baseline: `5.3576 deg`
- MUSIC + LRMC: `2.8432 deg`
- Root-MUSIC baseline: `6.3504 deg`
- Root-MUSIC + LRMC: `2.7867 deg`
- ESPRIT baseline: `6.3382 deg`
- ESPRIT + LRMC: `2.9282 deg`

### Interpretation

- 1.9 lambda is not inherently fatal for MUSIC under a narrow FOV when signals are non-coherent.
- Coherence is a major source of difficulty.
- Root-MUSIC and ESPRIT are much more fragile than MUSIC.
- The spacing-aware inversion fix was necessary to make the Root-MUSIC / ESPRIT results meaningful.

## 7. SubspaceNet Baselines

The previously trained SubspaceNet models on non-coherent NULA + LRMC reached roughly:
- Root-MUSIC: `2.86 deg`
- ESPRIT: `2.13 deg`

These results are much weaker than the best classical pipelines in the newer 1D / 2D non-coherent experiments.

### Interpretation

- The training set size used in the repo is much smaller than the `J = 45,000` sample regime mentioned in the paper.
- The learned model likely needs more data, a better-matched preprocessing front end, or a harder target regime to become competitive.

## 8. Overall Conclusions

1. `0.5 lambda` is the most favorable spacing for the current sparse-NULA LRMC pipeline.
2. `1.9 lambda` is not universally bad, but it is much more sensitive to signal coherence and estimator choice.
3. MUSIC is the most robust classical method in the narrow-FOV experiments.
4. Root-MUSIC and ESPRIT are highly geometry-sensitive in this code base and should be used with spacing-aware caution.
5. The current 2D pipeline is still structurally limited because it reduces 2D measurements to a 1D surrogate before estimation.
6. Fixing elevation does not materially improve the 2D coherent results, so elevation is not the main issue.
7. If SubspaceNet is to be trained next, the best candidate inputs are likely the strongest classical preprocessing outputs, not the raw 2D snapshots.

## 9. Recommended Next Steps

- If the goal is classical performance:
  - keep `0.5 lambda` as the preferred regime
  - use `SS -> LRMC` for Root-MUSIC / ESPRIT
  - use spatial smoothing only or baseline MUSIC when it already performs best

- If the goal is to improve SubspaceNet:
  - increase the training set size substantially
  - compare against the best classical preprocessing output
  - decide whether the target is coherent, non-coherent, 1D, or 2D before training

- If the goal is to understand the 2D array better:
  - move toward a true 2D DOA estimator
  - or run a controlled 2D diagnostic with fixed elevation and a true 2D-aware method

