# Phase 3d - 1D NULA Pattern Control at 1.9 Lambda

Direct 1D control comparison between [0,1,4,8] and [0,4,7,8] under the same 1.9 lambda coherent setup.

Experimental conditions:
- Array: 1D sparse NULA [0, 1, 4, 8]
- Physical spacing: 1.9 lambda
- Sources: 2 coherent narrowband targets
- Snapshots: T = 200
- FOV: [-15 deg, 15 deg]
- Minimum separation: 5 deg

| Geometry | Processing | Method | RMSE (deg) |
| --- | --- | --- | ---: |
| Pattern A [0,1,4,8] | Baseline | ESPRIT | 6.3382 |
| Pattern A [0,1,4,8] | Baseline | MUSIC | 5.3576 |
| Pattern A [0,1,4,8] | Baseline | Root-MUSIC | 6.3504 |
| Pattern A [0,1,4,8] | LRMC | ESPRIT | 2.9282 |
| Pattern A [0,1,4,8] | LRMC | MUSIC | 2.8432 |
| Pattern A [0,1,4,8] | LRMC | Root-MUSIC | 2.7867 |
| Pattern A [0,1,4,8] | LRMC -> SS | ESPRIT | 2.7221 |
| Pattern A [0,1,4,8] | LRMC -> SS | MUSIC | 2.8557 |
| Pattern A [0,1,4,8] | LRMC -> SS | Root-MUSIC | 2.7979 |
| Pattern C [0,4,7,8] | Baseline | ESPRIT | 6.9551 |
| Pattern C [0,4,7,8] | Baseline | MUSIC | 6.1993 |
| Pattern C [0,4,7,8] | Baseline | Root-MUSIC | 6.9441 |
| Pattern C [0,4,7,8] | LRMC | ESPRIT | 4.6497 |
| Pattern C [0,4,7,8] | LRMC | MUSIC | 4.5617 |
| Pattern C [0,4,7,8] | LRMC | Root-MUSIC | 4.6720 |
| Pattern C [0,4,7,8] | LRMC -> SS | ESPRIT | 4.6242 |
| Pattern C [0,4,7,8] | LRMC -> SS | MUSIC | 4.6036 |
| Pattern C [0,4,7,8] | LRMC -> SS | Root-MUSIC | 4.5984 |

# summary
These results are very useful because they settle one important question: the `Group A` vs `Group C` gap is **not just a 2D artifact**.

From [`phase3d_nula_pattern_control_1p9_results.md`](/f:/workspace1/SubspaceNet/results/phase3d_nula_pattern_control_1p9/phase3d_nula_pattern_control_1p9_results.md) and [`summary.csv`](/f:/workspace1/SubspaceNet/results/phase3d_nula_pattern_control_1p9/summary.csv):

## Main finding
With the same 1D coherent `1.9λ` setup:

- Pattern A `[0,1,4,8]` baseline:
  - MUSIC `5.36°`
  - Root-MUSIC `6.35°`
  - ESPRIT `6.34°`
- Pattern C `[0,4,7,8]` baseline:
  - MUSIC `6.20°`
  - Root-MUSIC `6.94°`
  - ESPRIT `6.96°`

So even before LRMC, Pattern C is a bit worse.

After LRMC the gap gets larger:

- Pattern A `LRMC`:
  - about `2.79°` to `2.93°`
- Pattern C `LRMC`:
  - about `4.56°` to `4.67°`

And `LRMC -> SS` does not change that much:
- Pattern A stays around `2.72°` to `2.86°`
- Pattern C stays around `4.60°` to `4.62°`

## What this means
This tells us:

1. The remaining A-vs-C difference is real in the current pipeline.
- It is not coming only from 2D row geometry.
- It already exists in pure 1D.

2. The row-pattern change from `[0,1,4,8]` to `[0,4,7,8]` matters a lot for LRMC.
- Baseline difference is modest, about `0.6°`.
- LRMC difference is much larger, about `1.7°` to `1.9°`.
- So LRMC is more sensitive to the sparse-pattern choice than the raw subspace estimators are.

3. The old hardcoding bug was not the whole story.
- We did fix a real bug in the 2D row geometry handling.
- But this 1D control shows that even after that fix, Pattern C is intrinsically harder for the current LRMC setup.

## Important interpretation
There is still something a bit surprising here:

- `[0,1,4,8]` and `[0,4,7,8]` are mirror-related.
- Their difference-coarray support is the same.

So in a fully reflection-invariant idealized pipeline, you might expect them to behave nearly the same.

But in the current implementation, they do not.

That suggests the issue is now less likely to be a simple hardcoded bug and more likely to be an **algorithmic asymmetry** in how LRMC is formulated or initialized in [`src/lrmc.py`](/f:/workspace1/SubspaceNet/src/lrmc.py), or in how observations are embedded into the virtual ULA completion problem from [`src/methods.py`](/f:/workspace1/SubspaceNet/src/methods.py).

## Practical conclusion
The clean conclusion from this experiment is:

- `Group C` being worse than `Group A` is not just because of 2D layout.
- The 1D sparse pattern `[0,4,7,8]` is already harder than `[0,1,4,8]` in the current LRMC pipeline.
- So the poorer `Group C` and some of the `Group B` behavior are at least partly due to the sparse row pattern itself, not only the 2D arrangement.

## Best next step
The next most useful check is to inspect the LRMC observation/construction path for reflection asymmetry:
1. how the sparse covariance entries are mapped into the virtual ULA,
2. whether initialization is left-anchored or order-sensitive,
3. whether Toeplitz filling/projection is effectively favoring `[0,1,4,8]` over its mirror.

If you want, I can do that code-level review next and tell you exactly where the A/C asymmetry is coming from.