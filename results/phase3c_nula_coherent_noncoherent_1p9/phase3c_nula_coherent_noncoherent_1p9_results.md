# Phase 3c - 1D NULA 1.9 Lambda Coherent vs Non-Coherent Comparison

Baseline MUSIC / Root-MUSIC / ESPRIT on the sparse NULA [0,1,4,8] with 1.9 lambda spacing.

Experimental conditions:
- Array: 1D sparse NULA [0, 1, 4, 8]
- Physical spacing: 1.9 lambda
- Sources: 2 coherent/non-coherent narrowband targets
- Snapshots: T = 200
- FOV: [-15 deg, 15 deg]
- Minimum separation: 5 deg

| Algorithm | RMSE (deg) |
| --- | ---: |
| Coherent LRMC -> SS | ESPRIT | 2.7221 |
| Coherent LRMC -> SS | MUSIC | 2.8557 |
| Coherent LRMC -> SS | Root-MUSIC | 2.7979 |
| Coherent LRMC | ESPRIT | 2.9282 |
| Coherent LRMC | MUSIC | 2.8432 |
| Coherent LRMC | Root-MUSIC | 2.7867 |
| Coherent baseline | ESPRIT | 6.3382 |
| Coherent baseline | MUSIC | 5.3576 |
| Coherent baseline | Root-MUSIC | 6.3504 |
| Non-coherent LRMC -> SS | ESPRIT | 0.1448 |
| Non-coherent LRMC -> SS | MUSIC | 0.1602 |
| Non-coherent LRMC -> SS | Root-MUSIC | 0.1497 |
| Non-coherent LRMC | ESPRIT | 0.1790 |
| Non-coherent LRMC | MUSIC | 0.1748 |
| Non-coherent LRMC | Root-MUSIC | 0.1850 |
| Non-coherent baseline | ESPRIT | 5.8638 |
| Non-coherent baseline | MUSIC | 0.0177 |
| Non-coherent baseline | Root-MUSIC | 6.8487 |

# summary
The 1.9λ 1D results are actually very informative.

What this says
The 1.9λ spacing is not the whole story.
For non-coherent MUSIC, 1.9λ is actually fine.
MUSIC baseline is already excellent: 0.0177°.
So the earlier 30°-level failures were not simply “because spacing is 1.9λ.”
Coherence matters a lot.
In the coherent case, all three methods are much worse.
LRMC helps a lot, but only down to about 2.7°-2.9°, not to the sub-degree regime.
That suggests the coherent rank-deficiency is still a major difficulty.
Root-MUSIC and ESPRIT are much more fragile than MUSIC.
In the non-coherent case, MUSIC is near perfect even without LRMC.
Root-MUSIC and ESPRIT are still bad without LRMC, but become excellent with LRMC.
That means the preprocessing is much more useful for the shift-invariant methods than for MUSIC.
LRMC -> SS does not change much here.
In both coherent and non-coherent cases, LRMC -> SS is only a tiny adjustment over LRMC alone.
So for this 1D 1.9λ setup, LRMC is the dominant step, and the post-smoothing step is not the main driver.
My interpretation
The earlier large errors were likely caused by a combination of:

coherent sources
the estimator type
the older 2D row-replicated setup
and, before the fix, the spacing-inversion assumption in Root-MUSIC / ESPRIT
This 1D experiment shows that:

1.9λ is not inherently fatal for MUSIC under a narrow FOV
but coherent-source estimation is still substantially harder
Root-MUSIC and ESPRIT are the most sensitive to the preprocessing model
Practical conclusion
If the goal is to understand the hard case:

the coherent 2D row-replicated setting is still the most interesting challenge
the non-coherent 1D 1.9λ case is almost too easy for MUSIC, but useful as a control
If the goal is to improve SubspaceNet training:

the non-coherent 1D 1.9λ result suggests the learned model should not be judged on MUSIC alone
the more meaningful target is the coherent or 2D case where classical methods still struggle