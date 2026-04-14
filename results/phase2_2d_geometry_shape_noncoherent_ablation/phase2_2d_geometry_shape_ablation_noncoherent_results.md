# Phase 2 - 2D Geometry-Shape Non-Coherent Ablation

Phase 2 compares rectangular Group A and slanted Group B layouts at 0.5 and 1.9 lambda under non-coherent sources to separate topology and spacing effects.

Experimental conditions:
- Array: 12-channel 2D geometry derived from the phase-2 array layouts
- Geometry: Group A @ 0.5 lambda
- Geometry group: Group A @ 0.5 lambda
- Physical spacing: 0.5 lambda
- Azimuth and elevation range: [-15 deg, 15 deg]
- Minimum azimuth separation: 5 deg
- Sources: 2 non-coherent narrowband targets
- Snapshots: T = 200
- Methods: MUSIC, Root-MUSIC, ESPRIT
- Metric: horizontal-angle RMSE in degrees

| Geometry | Processing | Method | RMSE (deg) |
| --- | --- | --- | ---: |
| Group A @ 0.5 lambda | Baseline | ESPRIT | 17.3575 |
| Group A @ 0.5 lambda | Baseline | MUSIC | 0.1178 |
| Group A @ 0.5 lambda | Baseline | Root-MUSIC | 15.7336 |
| Group A @ 0.5 lambda | LRMC -> SS | ESPRIT | 0.2166 |
| Group A @ 0.5 lambda | LRMC -> SS | MUSIC | 0.6516 |
| Group A @ 0.5 lambda | LRMC -> SS | Root-MUSIC | 0.2666 |
| Group A @ 0.5 lambda | LRMC only | ESPRIT | 0.1596 |
| Group A @ 0.5 lambda | LRMC only | MUSIC | 0.3791 |
| Group A @ 0.5 lambda | LRMC only | Root-MUSIC | 0.1763 |
| Group A @ 0.5 lambda | SS -> LRMC | ESPRIT | 0.1512 |
| Group A @ 0.5 lambda | SS -> LRMC | MUSIC | 0.2377 |
| Group A @ 0.5 lambda | SS -> LRMC | Root-MUSIC | 0.1624 |
| Group A @ 0.5 lambda | Spatial smoothing only | ESPRIT | 17.3546 |
| Group A @ 0.5 lambda | Spatial smoothing only | MUSIC | 0.1353 |
| Group A @ 0.5 lambda | Spatial smoothing only | Root-MUSIC | 15.7303 |
| Group A @ 1.9 lambda | Baseline | ESPRIT | 5.9901 |
| Group A @ 1.9 lambda | Baseline | MUSIC | 0.1433 |
| Group A @ 1.9 lambda | Baseline | Root-MUSIC | 6.6495 |
| Group A @ 1.9 lambda | LRMC -> SS | ESPRIT | 0.2052 |
| Group A @ 1.9 lambda | LRMC -> SS | MUSIC | 0.2468 |
| Group A @ 1.9 lambda | LRMC -> SS | Root-MUSIC | 0.1978 |
| Group A @ 1.9 lambda | LRMC only | ESPRIT | 0.2727 |
| Group A @ 1.9 lambda | LRMC only | MUSIC | 0.2706 |
| Group A @ 1.9 lambda | LRMC only | Root-MUSIC | 0.2705 |
| Group A @ 1.9 lambda | SS -> LRMC | ESPRIT | 0.3447 |
| Group A @ 1.9 lambda | SS -> LRMC | MUSIC | 0.3656 |
| Group A @ 1.9 lambda | SS -> LRMC | Root-MUSIC | 0.3473 |
| Group A @ 1.9 lambda | Spatial smoothing only | ESPRIT | 5.9848 |
| Group A @ 1.9 lambda | Spatial smoothing only | MUSIC | 0.1145 |
| Group A @ 1.9 lambda | Spatial smoothing only | Root-MUSIC | 6.6105 |
| Group B @ 0.5 lambda | Baseline | ESPRIT | 16.4977 |
| Group B @ 0.5 lambda | Baseline | MUSIC | 0.1364 |
| Group B @ 0.5 lambda | Baseline | Root-MUSIC | 15.7313 |
| Group B @ 0.5 lambda | LRMC -> SS | ESPRIT | 0.1907 |
| Group B @ 0.5 lambda | LRMC -> SS | MUSIC | 0.3994 |
| Group B @ 0.5 lambda | LRMC -> SS | Root-MUSIC | 0.2079 |
| Group B @ 0.5 lambda | LRMC only | ESPRIT | 0.1605 |
| Group B @ 0.5 lambda | LRMC only | MUSIC | 0.3381 |
| Group B @ 0.5 lambda | LRMC only | Root-MUSIC | 0.1766 |
| Group B @ 0.5 lambda | SS -> LRMC | ESPRIT | 0.1221 |
| Group B @ 0.5 lambda | SS -> LRMC | MUSIC | 0.1809 |
| Group B @ 0.5 lambda | SS -> LRMC | Root-MUSIC | 0.1291 |
| Group B @ 0.5 lambda | Spatial smoothing only | ESPRIT | 16.4979 |
| Group B @ 0.5 lambda | Spatial smoothing only | MUSIC | 0.1153 |
| Group B @ 0.5 lambda | Spatial smoothing only | Root-MUSIC | 15.7309 |
| Group B @ 1.9 lambda | Baseline | ESPRIT | 5.4899 |
| Group B @ 1.9 lambda | Baseline | MUSIC | 0.1437 |
| Group B @ 1.9 lambda | Baseline | Root-MUSIC | 6.6228 |
| Group B @ 1.9 lambda | LRMC -> SS | ESPRIT | 0.2076 |
| Group B @ 1.9 lambda | LRMC -> SS | MUSIC | 0.2430 |
| Group B @ 1.9 lambda | LRMC -> SS | Root-MUSIC | 0.2219 |
| Group B @ 1.9 lambda | LRMC only | ESPRIT | 0.2792 |
| Group B @ 1.9 lambda | LRMC only | MUSIC | 0.2940 |
| Group B @ 1.9 lambda | LRMC only | Root-MUSIC | 0.2874 |
| Group B @ 1.9 lambda | SS -> LRMC | ESPRIT | 0.3272 |
| Group B @ 1.9 lambda | SS -> LRMC | MUSIC | 0.3045 |
| Group B @ 1.9 lambda | SS -> LRMC | Root-MUSIC | 0.3264 |
| Group B @ 1.9 lambda | Spatial smoothing only | ESPRIT | 5.5101 |
| Group B @ 1.9 lambda | Spatial smoothing only | MUSIC | 0.1211 |
| Group B @ 1.9 lambda | Spatial smoothing only | Root-MUSIC | 6.5981 |
| Group C @ 0.5 lambda | Baseline | ESPRIT | 16.4973 |
| Group C @ 0.5 lambda | Baseline | MUSIC | 0.1374 |
| Group C @ 0.5 lambda | Baseline | Root-MUSIC | 15.7274 |
| Group C @ 0.5 lambda | LRMC -> SS | ESPRIT | 0.2289 |
| Group C @ 0.5 lambda | LRMC -> SS | MUSIC | 0.6499 |
| Group C @ 0.5 lambda | LRMC -> SS | Root-MUSIC | 0.3086 |
| Group C @ 0.5 lambda | LRMC only | ESPRIT | 0.1600 |
| Group C @ 0.5 lambda | LRMC only | MUSIC | 0.2871 |
| Group C @ 0.5 lambda | LRMC only | Root-MUSIC | 0.1777 |
| Group C @ 0.5 lambda | SS -> LRMC | ESPRIT | 0.1516 |
| Group C @ 0.5 lambda | SS -> LRMC | MUSIC | 0.2135 |
| Group C @ 0.5 lambda | SS -> LRMC | Root-MUSIC | 0.1641 |
| Group C @ 0.5 lambda | Spatial smoothing only | ESPRIT | 16.4967 |
| Group C @ 0.5 lambda | Spatial smoothing only | MUSIC | 0.1353 |
| Group C @ 0.5 lambda | Spatial smoothing only | Root-MUSIC | 15.7289 |
| Group C @ 1.9 lambda | Baseline | ESPRIT | 5.4963 |
| Group C @ 1.9 lambda | Baseline | MUSIC | 0.1506 |
| Group C @ 1.9 lambda | Baseline | Root-MUSIC | 6.6196 |
| Group C @ 1.9 lambda | LRMC -> SS | ESPRIT | 0.2211 |
| Group C @ 1.9 lambda | LRMC -> SS | MUSIC | 0.2285 |
| Group C @ 1.9 lambda | LRMC -> SS | Root-MUSIC | 0.2212 |
| Group C @ 1.9 lambda | LRMC only | ESPRIT | 0.2849 |
| Group C @ 1.9 lambda | LRMC only | MUSIC | 0.2645 |
| Group C @ 1.9 lambda | LRMC only | Root-MUSIC | 0.2638 |
| Group C @ 1.9 lambda | SS -> LRMC | ESPRIT | 0.3254 |
| Group C @ 1.9 lambda | SS -> LRMC | MUSIC | 0.3264 |
| Group C @ 1.9 lambda | SS -> LRMC | Root-MUSIC | 0.3485 |
| Group C @ 1.9 lambda | Spatial smoothing only | ESPRIT | 5.5061 |
| Group C @ 1.9 lambda | Spatial smoothing only | MUSIC | 0.1303 |
| Group C @ 1.9 lambda | Spatial smoothing only | Root-MUSIC | 6.6039 |

# sammary
These non-coherent results are very revealing. The short version is:

- non-coherent sources make the whole 2D problem much easier
- the geometry differences between A / B / C shrink dramatically
- MUSIC becomes almost perfect in every case
- LRMC is still useful for Root-MUSIC and ESPRIT, but the “best order” is no longer as dominant as in the coherent case

## 1. The biggest change is caused by source coherence
Compared with the coherent results in [`phase2_2d_geometry_shape_ablation_coherent_results.md`](/f:/workspace1/SubspaceNet/results/phase2_2d_geometry_shape_coherent_ablation/phase2_2d_geometry_shape_ablation_coherent_results.md), the non-coherent results in [`phase2_2d_geometry_shape_ablation_noncoherent_results.md`](/f:/workspace1/SubspaceNet/results/phase2_2d_geometry_shape_noncoherent_ablation/phase2_2d_geometry_shape_ablation_noncoherent_results.md) are far better overall.

Examples:

- Group B @ `1.9λ`, coherent baseline:
  - MUSIC `6.27°`
  - Root-MUSIC `6.84°`
  - ESPRIT `7.01°`

- Group B @ `1.9λ`, non-coherent baseline:
  - MUSIC `0.14°`
  - Root-MUSIC `6.62°`
  - ESPRIT `5.49°`

So once coherence is removed:
- MUSIC almost collapses to near-zero error immediately
- Root-MUSIC and ESPRIT still need preprocessing, but they are much easier to rescue

## 2. MUSIC is now excellent almost everywhere
This is the clearest pattern in the whole table.

For all geometries and both spacings:
- baseline MUSIC is already around `0.12° - 0.15°`
- spatial smoothing only is also around `0.11° - 0.14°`

That means:
- under non-coherent sources, MUSIC is no longer the bottleneck
- geometry A / B / C barely matters for MUSIC in practice

So if the task is specifically non-coherent + MUSIC:
- the geometry-shape differences are almost irrelevant
- LRMC is not needed for accuracy
- spatial smoothing only is already enough, and often best or tied-best

## 3. Root-MUSIC and ESPRIT still benefit strongly from LRMC
For Root-MUSIC and ESPRIT, the non-coherent baseline is still not good:

Examples:
- Group A @ `0.5λ` baseline:
  - Root-MUSIC `15.73°`
  - ESPRIT `17.36°`
- Group B @ `1.9λ` baseline:
  - Root-MUSIC `6.62°`
  - ESPRIT `5.49°`

But once LRMC is added, they drop into the sub-degree regime:

- Group A @ `0.5λ`, `SS -> LRMC`:
  - Root-MUSIC `0.162°`
  - ESPRIT `0.151°`
- Group B @ `1.9λ`, `LRMC -> SS`:
  - Root-MUSIC `0.222°`
  - ESPRIT `0.208°`
- Group C @ `1.9λ`, `LRMC -> SS`:
  - Root-MUSIC `0.221°`
  - ESPRIT `0.221°`

So LRMC remains very useful for the shift-invariant methods even in the non-coherent regime.

## 4. Geometry differences are now much smaller
This is probably the most important geometry conclusion.

In the coherent study:
- A / B / C differed a lot
- especially when LRMC and smoothing were involved

In the non-coherent study:
- those gaps shrink a lot
- all three geometries become quite workable

At `1.9λ`:
- Group A best subspace-style result is around `0.198° - 0.205°` with `LRMC -> SS`
- Group B best is around `0.208° - 0.222°` with `LRMC -> SS`
- Group C best is around `0.221° - 0.229°` with `LRMC -> SS`

That is a very small spread.

So the conclusion here is:
- geometry still matters a little
- but source coherence was the main amplifier of the geometry sensitivity

## 5. The best processing order changes a bit
In the coherent case, `SS -> LRMC` was clearly the strongest overall classical pipeline.

In the non-coherent case:
- for `0.5λ`, `SS -> LRMC` is often the best or tied-best for Root-MUSIC / ESPRIT
- for `1.9λ`, `LRMC -> SS` is slightly better than `SS -> LRMC` for all three groups

Examples at `1.9λ`:
- Group A:
  - `LRMC -> SS`: `0.205 / 0.198°`
  - `SS -> LRMC`: `0.345 / 0.347°`
- Group B:
  - `LRMC -> SS`: `0.208 / 0.222°`
  - `SS -> LRMC`: `0.327 / 0.326°`
- Group C:
  - `LRMC -> SS`: `0.221 / 0.221°`
  - `SS -> LRMC`: `0.325 / 0.349°`

So for non-coherent `1.9λ`, the preferred order appears to flip:
- coherent: `SS -> LRMC`
- non-coherent: `LRMC -> SS`

That is a meaningful algorithmic result.

## 6. Practical conclusion for Group B
Since Group B is your hardware geometry:

- Group B @ `1.9λ` is very good under non-coherent signals
- MUSIC is already excellent without LRMC
- Root-MUSIC / ESPRIT become excellent with LRMC-based preprocessing
- geometry is no longer a serious problem in this regime

For Group B @ `1.9λ` non-coherent:
- if using MUSIC: baseline or SS-only is enough
- if using Root-MUSIC / ESPRIT: `LRMC -> SS` looks best

## Bottom line
The non-coherent study shows that:

- the large geometry sensitivity seen before was driven mainly by coherence
- Group B is not intrinsically problematic under non-coherent sources
- all three 2D geometries become strong once coherence is removed
- for non-coherent `1.9λ`, `LRMC -> SS` now looks slightly better than `SS -> LRMC` for Root-MUSIC / ESPRIT
- MUSIC is essentially solved already in this regime
