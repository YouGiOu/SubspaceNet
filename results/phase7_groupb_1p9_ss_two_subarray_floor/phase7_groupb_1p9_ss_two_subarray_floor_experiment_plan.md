# Phase 7 Group B 1.9 Lambda Two-Subarray Spatial Smoothing Floor Experiment Plan

## Goal
Determine whether reducing row spatial smoothing from averaging `3` row-subarray covariances to averaging only `2` causes a meaningful performance change in the Group B `1.9 lambda` pipeline.

This phase is intended to answer two separate questions:
- does `2-of-3` SS materially degrade the current canonical `SS -> LRMC` baseline?
- if `2-of-3` does degrade performance, is the effect mostly due to fewer averaged subarrays or due to which specific row pair is selected?

## Scope
This study focuses on the validated Group B hardware-relevant regime:
- Group B 12-channel 2D geometry
- `1.9 lambda` spacing
- rowwise `SS -> LRMC` front end

Because the research question is about the lower limit of SS scale, the first experiment family should be targeted rather than broad.

## Spatial Smoothing Variants To Compare

### Primary Baseline
- `SS(3/3) -> LRMC`

This is the current canonical path and must be the reference for all comparisons.

### Two-Subarray Variants
All `C(3,2) = 3` row-pair choices should be tested:
- `SS(2/3: rows 0+1) -> LRMC`
- `SS(2/3: rows 0+2) -> LRMC`
- `SS(2/3: rows 1+2) -> LRMC`

These should be treated as distinct variants, not pooled into one average, because:
- two pairs are contiguous in row index
- one pair skips the middle row
- the physical contribution pattern may matter

## Control Groups To Compare

### Classical Controls
For each SS variant, evaluate:
- `DBF`
- `MUSIC`
- `Root-MUSIC`
- `ESPRIT`

### Learned Target
For each SS variant, evaluate:
- `SubspaceNet -> ESPRIT`

The learned comparison should use the same preprocessing variant as the classical control in that cell.

## Recommended Study Design
Use a two-stage plan.

### Stage A: Classical-First Screening
Run only classical controls first.

Purpose:
- quickly determine whether any `2-of-3` choice is clearly non-competitive
- identify whether row-pair choice matters enough to justify learned runs on all three variants

### Stage B: Learned Follow-Up
Run SubspaceNet-ESPRIT only on:
- the full `3-of-3` baseline
- the best `2-of-3` classical variant
- optionally the worst `2-of-3` classical variant if the gap is large and scientifically interesting

Purpose:
- avoid expensive learned training on every variant if the classical screen already shows one pair is clearly dominant or clearly unusable

## Recommended Signal Regimes
The first pass should include both:
- coherent
- non-coherent

Reason:
- coherent Group B is the more fragile and informative regime
- non-coherent Group B is easier and can show whether the SS reduction matters only in hard cases

If runtime must be limited, prioritize:
1. coherent
2. non-coherent

## Recommended Fixed Conditions For The First Pass
- Array: Group B 12-channel 2D hardware geometry
- Physical spacing: `1.9 lambda`
- Sources: `M = 2`, narrowband
- Snapshots: `T = 40`
- Azimuth range: `[-15 deg, 15 deg]`
- Elevation range: `[-15 deg, 15 deg]`
- LRMC rank: `3`
- LRMC solver: `svd`
- LRMC initialization: `lag`
- Virtual ULA size: `9`
- Seed: fixed at `42`
- Metric: horizontal-angle RMSE in degrees

## Recommended Test Cells
Do not start with a large full grid.

The first pass should focus on a small set of representative difficulty points:

### Hard coherent cells
- gap `1 deg`, SNR `1 dB`
- gap `2 deg`, SNR `1 dB`
- gap `1 deg`, SNR `10 dB`

### Easier anchor cells
- gap `3 deg`, SNR `10 dB`
- gap `5 deg`, SNR `10 dB`

### Matching non-coherent cells
Use the same gap/SNR set for non-coherent signals.

This gives:
- enough hard cases to expose SS-floor effects
- enough easy cases to see whether differences disappear once the regime is not stressed

## Why These Cells
- `1 deg`, `1 dB` is the strongest stress point already shown to separate methods clearly
- `2 deg`, `1 dB` checks whether the effect persists just outside the sharpest boundary
- `1 deg`, `10 dB` separates low-SNR failure from low-separation failure
- `3 deg` and `5 deg` act as sanity anchors where large differences would be surprising

## Decision Rules

### Question 1: Is two-subarray SS materially worse than full SS?
Treat it as materially worse if one or more hard cells shows:
- a large and repeatable RMSE increase across multiple methods
- or a visible collapse in `Root-MUSIC` / `ESPRIT` while `SS(3/3)` remains stable

### Question 2: Does the chosen row pair matter?
Treat row-pair identity as important if:
- the three `2-of-3` variants are not clustered closely
- especially if `rows 0+2` differs strongly from the two contiguous choices

### Question 3: Is the effect mostly classical or also learned?
Treat it as broadly structural if both:
- classical controls worsen
- SubspaceNet-ESPRIT also worsens under the same SS reduction

Treat it as mainly estimator-specific if:
- classical methods degrade
- but SubspaceNet remains close to the full `3-of-3` baseline

## Baselines That Must Be Preserved
The report should always include:
- full `SS(3/3) -> LRMC` baseline
- the same methods with the candidate `2-of-3` SS variant

Optional but useful reference lines:
- no preprocessing (`sample`) classical baseline on the same cells

This optional raw baseline is useful because it helps separate:
- "2-of-3 SS is slightly weaker than full SS"
from
- "2-of-3 SS is so weak that it is approaching no-SS behavior"

## Metrics
Primary metric:
- horizontal-angle RMSE

Secondary metrics worth recording if available:
- method failure rate or invalid-estimate count
- LRMC diagnostics stability
- training convergence quality for SubspaceNet

## Intended Interpretation

### If all `2-of-3` variants stay close to `3-of-3`
Conclusion:
- the current SS stage has redundancy
- the lower useful SS scale may already be `2` subarrays

### If all `2-of-3` variants degrade similarly
Conclusion:
- the performance loss is mainly from reduced averaging count
- SS strength itself matters more than exact row choice

### If one `2-of-3` pair is clearly worse or better
Conclusion:
- row selection geometry matters
- the question is not only "how many subarrays" but also "which subarrays"

### If only hard coherent cells show a difference
Conclusion:
- the SS floor is a boundary-regime issue
- full `3-of-3` smoothing is mainly necessary near the coherent resolution limit

### If non-coherent results barely move
Conclusion:
- the SS-floor effect is mainly a coherent-regime stabilization issue

## Expected Outputs
Running the planned launcher should produce:
- `summary.csv`
- one family markdown results file
- per-method `metrics.json`

Recommended results path:
- `results/phase7_groupb_1p9_ss_two_subarray_floor_phasea/`

Recommended family markdown:
- `phase7_groupb_1p9_ss_two_subarray_floor_phasea_results.md`

## Template / Label Requirements
Every template should make the SS choice explicit in:
- `template_name`
- `markdown_scheme_label`
- `description`

Recommended labels:
- `SS(3/3) -> LRMC`
- `SS(2/3: rows 0+1) -> LRMC`
- `SS(2/3: rows 0+2) -> LRMC`
- `SS(2/3: rows 1+2) -> LRMC`

## Canonical Launcher
- `run_phase7_groupb_1p9_ss_two_subarray_floor_phasea.py`

Recommended command:
```bash
python run_phase7_groupb_1p9_ss_two_subarray_floor_phasea.py
```

## Follow-Up Decision
After the first pass:
- if `2-of-3` variants are nearly identical to `3-of-3`, the next experiment can move on to low-snapshot studies using the cheapest acceptable SS variant
- if `2-of-3` variants differ strongly, the next phase should focus on row-pair geometry rather than immediately moving to low-snapshot training
- if only one pair remains competitive, that pair should be the sole reduced-SS candidate in later learned experiments
