# Phase 2 - 2D Geometry-Shape Ablation

Phase 2 compares rectangular Group A and slanted Group B layouts at 0.5 and 1.9 lambda to separate topology and spacing effects.

Experimental conditions:
- Array: 12-channel 2D geometry derived from the phase-2 array layouts
- Geometry: Group A @ 0.5 lambda
- Geometry group: Group A @ 0.5 lambda
- Physical spacing: 0.5 lambda
- Azimuth and elevation range: [-15 deg, 15 deg]
- Minimum azimuth separation: 5 deg
- Sources: 2 coherent narrowband targets
- Snapshots: T = 200
- Methods: MUSIC, Root-MUSIC, ESPRIT
- Metric: horizontal-angle RMSE in degrees

| Geometry | Processing | Method | RMSE (deg) |
| --- | --- | --- | ---: |
| Group A @ 0.5 lambda | Baseline | ESPRIT | 26.5747 |
| Group A @ 0.5 lambda | Baseline | MUSIC | 9.8204 |
| Group A @ 0.5 lambda | Baseline | Root-MUSIC | 26.8516 |
| Group A @ 0.5 lambda | LRMC -> SS | ESPRIT | 2.2651 |
| Group A @ 0.5 lambda | LRMC -> SS | MUSIC | 10.5338 |
| Group A @ 0.5 lambda | LRMC -> SS | Root-MUSIC | 2.4119 |
| Group A @ 0.5 lambda | LRMC only | ESPRIT | 9.2546 |
| Group A @ 0.5 lambda | LRMC only | MUSIC | 12.6993 |
| Group A @ 0.5 lambda | LRMC only | Root-MUSIC | 8.4482 |
| Group A @ 0.5 lambda | SS -> LRMC | ESPRIT | 1.3120 |
| Group A @ 0.5 lambda | SS -> LRMC | MUSIC | 7.4231 |
| Group A @ 0.5 lambda | SS -> LRMC | Root-MUSIC | 2.1714 |
| Group A @ 0.5 lambda | Spatial smoothing only | ESPRIT | 17.6523 |
| Group A @ 0.5 lambda | Spatial smoothing only | MUSIC | 0.4915 |
| Group A @ 0.5 lambda | Spatial smoothing only | Root-MUSIC | 15.9838 |
| Group A @ 1.9 lambda | Baseline | ESPRIT | 6.8541 |
| Group A @ 1.9 lambda | Baseline | MUSIC | 6.3041 |
| Group A @ 1.9 lambda | Baseline | Root-MUSIC | 6.7963 |
| Group A @ 1.9 lambda | LRMC -> SS | ESPRIT | 2.4917 |
| Group A @ 1.9 lambda | LRMC -> SS | MUSIC | 2.4327 |
| Group A @ 1.9 lambda | LRMC -> SS | Root-MUSIC | 2.4253 |
| Group A @ 1.9 lambda | LRMC only | ESPRIT | 5.1672 |
| Group A @ 1.9 lambda | LRMC only | MUSIC | 4.7270 |
| Group A @ 1.9 lambda | LRMC only | Root-MUSIC | 4.8797 |
| Group A @ 1.9 lambda | SS -> LRMC | ESPRIT | 1.3661 |
| Group A @ 1.9 lambda | SS -> LRMC | MUSIC | 1.1022 |
| Group A @ 1.9 lambda | SS -> LRMC | Root-MUSIC | 1.2830 |
| Group A @ 1.9 lambda | Spatial smoothing only | ESPRIT | 6.0407 |
| Group A @ 1.9 lambda | Spatial smoothing only | MUSIC | 0.1428 |
| Group A @ 1.9 lambda | Spatial smoothing only | Root-MUSIC | 6.8360 |
| Group B @ 0.5 lambda | Baseline | ESPRIT | 27.0534 |
| Group B @ 0.5 lambda | Baseline | MUSIC | 9.0204 |
| Group B @ 0.5 lambda | Baseline | Root-MUSIC | 26.3040 |
| Group B @ 0.5 lambda | LRMC -> SS | ESPRIT | 8.3907 |
| Group B @ 0.5 lambda | LRMC -> SS | MUSIC | 15.4641 |
| Group B @ 0.5 lambda | LRMC -> SS | Root-MUSIC | 8.4212 |
| Group B @ 0.5 lambda | LRMC only | ESPRIT | 15.2415 |
| Group B @ 0.5 lambda | LRMC only | MUSIC | 11.6271 |
| Group B @ 0.5 lambda | LRMC only | Root-MUSIC | 14.4006 |
| Group B @ 0.5 lambda | SS -> LRMC | ESPRIT | 6.7966 |
| Group B @ 0.5 lambda | SS -> LRMC | MUSIC | 6.7063 |
| Group B @ 0.5 lambda | SS -> LRMC | Root-MUSIC | 5.0279 |
| Group B @ 0.5 lambda | Spatial smoothing only | ESPRIT | 16.3850 |
| Group B @ 0.5 lambda | Spatial smoothing only | MUSIC | 0.1451 |
| Group B @ 0.5 lambda | Spatial smoothing only | Root-MUSIC | 15.6595 |
| Group B @ 1.9 lambda | Baseline | ESPRIT | 7.0124 |
| Group B @ 1.9 lambda | Baseline | MUSIC | 6.2742 |
| Group B @ 1.9 lambda | Baseline | Root-MUSIC | 6.8379 |
| Group B @ 1.9 lambda | LRMC -> SS | ESPRIT | 3.2646 |
| Group B @ 1.9 lambda | LRMC -> SS | MUSIC | 3.1035 |
| Group B @ 1.9 lambda | LRMC -> SS | Root-MUSIC | 3.2455 |
| Group B @ 1.9 lambda | LRMC only | ESPRIT | 4.8897 |
| Group B @ 1.9 lambda | LRMC only | MUSIC | 4.6201 |
| Group B @ 1.9 lambda | LRMC only | Root-MUSIC | 4.7083 |
| Group B @ 1.9 lambda | SS -> LRMC | ESPRIT | 2.0359 |
| Group B @ 1.9 lambda | SS -> LRMC | MUSIC | 1.7331 |
| Group B @ 1.9 lambda | SS -> LRMC | Root-MUSIC | 1.8003 |
| Group B @ 1.9 lambda | Spatial smoothing only | ESPRIT | 5.6927 |
| Group B @ 1.9 lambda | Spatial smoothing only | MUSIC | 0.1659 |
| Group B @ 1.9 lambda | Spatial smoothing only | Root-MUSIC | 6.8221 |
| Group C @ 0.5 lambda | Baseline | ESPRIT | 27.2503 |
| Group C @ 0.5 lambda | Baseline | MUSIC | 9.8046 |
| Group C @ 0.5 lambda | Baseline | Root-MUSIC | 26.5563 |
| Group C @ 0.5 lambda | LRMC -> SS | ESPRIT | 12.7553 |
| Group C @ 0.5 lambda | LRMC -> SS | MUSIC | 20.4248 |
| Group C @ 0.5 lambda | LRMC -> SS | Root-MUSIC | 12.9477 |
| Group C @ 0.5 lambda | LRMC only | ESPRIT | 16.2106 |
| Group C @ 0.5 lambda | LRMC only | MUSIC | 12.1536 |
| Group C @ 0.5 lambda | LRMC only | Root-MUSIC | 14.4376 |
| Group C @ 0.5 lambda | SS -> LRMC | ESPRIT | 13.8578 |
| Group C @ 0.5 lambda | SS -> LRMC | MUSIC | 12.0715 |
| Group C @ 0.5 lambda | SS -> LRMC | Root-MUSIC | 12.2900 |
| Group C @ 0.5 lambda | Spatial smoothing only | ESPRIT | 16.7432 |
| Group C @ 0.5 lambda | Spatial smoothing only | MUSIC | 0.5845 |
| Group C @ 0.5 lambda | Spatial smoothing only | Root-MUSIC | 16.0544 |
| Group C @ 1.9 lambda | Baseline | ESPRIT | 6.5620 |
| Group C @ 1.9 lambda | Baseline | MUSIC | 6.3129 |
| Group C @ 1.9 lambda | Baseline | Root-MUSIC | 6.6751 |
| Group C @ 1.9 lambda | LRMC -> SS | ESPRIT | 3.1263 |
| Group C @ 1.9 lambda | LRMC -> SS | MUSIC | 3.0530 |
| Group C @ 1.9 lambda | LRMC -> SS | Root-MUSIC | 3.1296 |
| Group C @ 1.9 lambda | LRMC only | ESPRIT | 4.9921 |
| Group C @ 1.9 lambda | LRMC only | MUSIC | 4.5426 |
| Group C @ 1.9 lambda | LRMC only | Root-MUSIC | 4.7669 |
| Group C @ 1.9 lambda | SS -> LRMC | ESPRIT | 1.9165 |
| Group C @ 1.9 lambda | SS -> LRMC | MUSIC | 1.9657 |
| Group C @ 1.9 lambda | SS -> LRMC | Root-MUSIC | 1.9336 |
| Group C @ 1.9 lambda | Spatial smoothing only | ESPRIT | 5.6795 |
| Group C @ 1.9 lambda | Spatial smoothing only | MUSIC | 0.1622 |
| Group C @ 1.9 lambda | Spatial smoothing only | Root-MUSIC | 6.7646 |

# summary
The current results are much more coherent than the old ones, and they tell a clearer story.

From [`phase2_2d_geometry_shape_ablation_results.md`](/f:/workspace1/SubspaceNet/results/phase2_2d_geometry_shape_ablation/phase2_2d_geometry_shape_ablation_results.md), with the old report as context in [`phase2_2d_geometry_shape_ablation_results_old.md`](/f:/workspace1/SubspaceNet/results/phase2_2d_geometry_shape_ablation/phase2_2d_geometry_shape_ablation_results_old.md):

## Main conclusions

### 1. The old Group B failure was partly a bug, not a real geometry verdict
In the old results, Group B looked catastrophically bad once LRMC was involved:
- Group B @ `0.5λ`, `SS -> LRMC`:
  - MUSIC `22.68°`
  - Root-MUSIC `35.85°`
  - ESPRIT `35.59°`
- Group B @ `1.9λ`, `SS -> LRMC`:
  - roughly `8.4°-8.8°`

In the current results, after the row-geometry fix, Group B is much better:
- Group B @ `0.5λ`, `SS -> LRMC`:
  - MUSIC `6.71°`
  - Root-MUSIC `5.03°`
  - ESPRIT `6.80°`
- Group B @ `1.9λ`, `SS -> LRMC`:
  - MUSIC `1.73°`
  - Root-MUSIC `1.80°`
  - ESPRIT `2.04°`

So the previous conclusion “Group B breaks LRMC” was too strong. A large part of that was the wrong row geometry being fed into LRMC.

### 2. `SS -> LRMC` is still the strongest overall pipeline
Across essentially all useful 2D cases, `SS -> LRMC` is the best or near-best overall classical pipeline.

Best examples:
- Group A @ `1.9λ`:
  - `SS -> LRMC` gives `1.10° / 1.28° / 1.37°`
- Group B @ `1.9λ`:
  - `SS -> LRMC` gives `1.73° / 1.80° / 2.04°`
- Group C @ `1.9λ`:
  - `SS -> LRMC` gives `1.97° / 1.93° / 1.92°`

`LRMC only` helps, but not as much.  
`LRMC -> SS` is usually worse than `SS -> LRMC`.

### 3. The `1.9λ` cases are now better than the `0.5λ` cases
This is one of the most interesting outcomes.

For all three geometries, the `1.9λ` runs are clearly better than the corresponding `0.5λ` runs.

Examples:
- Group A:
  - `SS -> LRMC` improves from about `7.42 / 2.17 / 1.31°` at `0.5λ`
  - to `1.10 / 1.28 / 1.37°` at `1.9λ`
- Group B:
  - `SS -> LRMC` improves from about `6.71 / 5.03 / 6.80°`
  - to `1.73 / 1.80 / 2.04°`
- Group C:
  - `SS -> LRMC` improves from about `12.07 / 12.29 / 13.86°`
  - to `1.97 / 1.93 / 1.92°`

So in this narrowed `±15°` FOV setup, larger spacing is not hurting the 2D pipeline. It is helping.

### 4. Group A is still best, but Group B is now clearly viable
At `1.9λ`, ordering by the best pipeline (`SS -> LRMC`) is:

- Group A: about `1.10°-1.37°`
- Group B: about `1.73°-2.04°`
- Group C: about `1.92°-1.97°`

So:
- Group A remains the strongest geometry
- Group B is no longer a failure case
- Group C is slightly worse than B and clearly worse than A

That suggests the slanted geometry itself is not the main problem anymore. Once the row geometry is modeled correctly, Group B actually works quite well.

### 5. The remaining hard case is the row pattern, not just the 2D layout
Group B and Group C share the row pattern `[0,4,7,8]`, while Group A uses `[0,1,4,8]`.

The results now point to:
- `[0,1,4,8]` being the best row pattern for this pipeline
- `[0,4,7,8]` being workable, but consistently a bit worse

That matches the pure 1D control in [`phase3d_nula_pattern_control_1p9_results.md`](/f:/workspace1/SubspaceNet/results/phase3d_nula_pattern_control_1p9/phase3d_nula_pattern_control_1p9_results.md), where Pattern C `[0,4,7,8]` was also worse than Pattern A `[0,1,4,8]`.

## MUSIC-specific note
MUSIC still has its own pattern:
- `Spatial smoothing only` gives extremely low MUSIC RMSE in all geometries:
  - Group A @ `1.9λ`: `0.1428°`
  - Group B @ `1.9λ`: `0.1659°`
  - Group C @ `1.9λ`: `0.1622°`

So if the target method is specifically MUSIC, smoothing alone is already excellent.
But for Root-MUSIC and ESPRIT, `SS -> LRMC` is much better.

## Bottom line
The cleaned-up interpretation is:

- The previous severe Group B collapse was largely caused by a row-geometry modeling bug.
- After the fix, all three 2D geometries benefit strongly from `SS -> LRMC`, especially at `1.9λ`.
- Group A is still the best geometry overall.
- Group B is no longer problematic in principle.
- The remaining performance gap is more about the sparse row pattern `[0,1,4,8]` vs `[0,4,7,8]` than about “slanted vs rectangular” layout alone.

If you want, I can next write this interpretation directly into [`phase2_2d_geometry_shape_ablation_results.md`](/f:/workspace1/SubspaceNet/results/phase2_2d_geometry_shape_ablation/phase2_2d_geometry_shape_ablation_results.md) as a short “Key Findings” section.
