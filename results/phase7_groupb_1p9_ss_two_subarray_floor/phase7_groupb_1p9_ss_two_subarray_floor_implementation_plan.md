# Phase 7 Group B 1.9 Lambda Two-Subarray Spatial Smoothing Module Implementation Plan

## Goal
Add a configurable row-spatial-smoothing variant for the 2D Group B pipeline so the repo can compare:
- the current default smoothing over all `3` row subarrays
- every `2-of-3` row-subarray averaging choice

The implementation should make this comparison explicit and reproducible in both:
- classical `SS -> LRMC` evaluation
- `SS -> LRMC -> SubspaceNet` preprocessing

## Why A New Module Is Needed
The current Group B workflow treats row spatial smoothing as a fixed preprocessing step.

What is not yet parameterized is:
- how many row subarrays are averaged
- which specific row-subarray subset is used when fewer than all rows are included

Without that configurability, the question "is averaging `2` row-subarray covariances materially different from averaging `3`?" cannot be answered cleanly.

## Current Relevant Code Touch Points
- [src/methods.py](/f:/workspace1/SubspaceNet/src/methods.py)
  Current subspace-method covariance construction and rowwise LRMC integration.
- [src/data_handler.py](/f:/workspace1/SubspaceNet/src/data_handler.py)
  Current SubspaceNet input construction for `covariance_mode = "ss_then_lrmc"`.
- [src/lrmc.py](/f:/workspace1/SubspaceNet/src/lrmc.py)
  Current rowwise covariance splitting / averaging helpers used by LRMC preprocessing.
- `data/dataset_templates/ablation/...`
  Templates will need a way to specify the new SS variant cleanly.

## Functional Requirements
The new implementation should support:

1. Full current baseline
- average all `3` row-subarray covariances

2. Every `2-of-3` row-subarray choice
- top + middle
- top + bottom
- middle + bottom

3. Clear metadata in diagnostics and reports
- number of subarrays used
- exact subset used
- whether the mode is intended as a backward-compatible baseline or an ablation

4. Reuse across classical and learned pipelines
- classical control templates
- SubspaceNet preprocessing path

## Recommended Configuration Design
Avoid encoding this only as a new opaque `covariance_mode` string.

Preferred design:
- keep `covariance_mode = "ss_then_lrmc"` for the general path
- add explicit SS-selection parameters in `system_model`, for example:
  - `ss_num_subarrays`
  - `ss_row_subset`

Example semantics:
- `ss_num_subarrays = 3`, `ss_row_subset = null`
  means current default averaging over all rows
- `ss_num_subarrays = 2`, `ss_row_subset = [0, 1]`
  means average only top + middle row blocks

This is preferable because:
- it preserves the current canonical mode name
- it avoids proliferating multiple special-case covariance modes
- it makes result tables easier to interpret

## Backward-Compatibility Requirements
The default behavior must remain unchanged when the new parameters are absent:
- existing `ss_then_lrmc` templates must still use all `3` row subarrays
- old experiments must remain reproducible without editing their templates

## Internal Processing Requirements
The implementation should make the row selection explicit before covariance averaging.

That means:
- split covariance into row blocks as before
- select only the requested row-block subset
- average only that subset
- pass the resulting smoothed covariance into the existing LRMC path

The selection logic should not silently reorder rows.

The chosen subset should preserve the original row order:
- `[0, 1]`
- `[0, 2]`
- `[1, 2]`

## Validation Requirements
Before any large experiment sweep, the module should be validated with small deterministic checks.

Minimum validation items:
- confirm default mode matches current outputs exactly
- confirm each `2-of-3` subset uses the intended row blocks
- confirm bad subsets fail loudly
  - duplicate row index
  - out-of-range index
  - wrong subset length
- confirm classical and SubspaceNet preprocessing both honor the same subset parameters

## Diagnostics To Expose
To make later interpretation easier, diagnostics should record:
- selected row subset
- number of averaged subarrays
- effective smoothed covariance shape
- whether LRMC was run after subset averaging

If LRMC diagnostics are already emitted, SS-selection metadata should sit beside them rather than being hidden in template names only.

## Reporting / Naming Requirements
Templates and markdown labels should distinguish:
- full SS baseline
- 2-subarray top + middle
- 2-subarray top + bottom
- 2-subarray middle + bottom

Recommended readable scheme labels:
- `SS(3/3) -> LRMC`
- `SS(2/3: rows 0+1) -> LRMC`
- `SS(2/3: rows 0+2) -> LRMC`
- `SS(2/3: rows 1+2) -> LRMC`

Recommended learned labels:
- `SS(3/3) -> LRMC -> SubspaceNet`
- `SS(2/3: rows 0+1) -> LRMC -> SubspaceNet`
- `SS(2/3: rows 0+2) -> LRMC -> SubspaceNet`
- `SS(2/3: rows 1+2) -> LRMC -> SubspaceNet`

## Risks And Design Questions
1. The `top + bottom` choice may be qualitatively different from the two contiguous choices.
   It has larger row separation and may behave less like a reduced-sample average and more like a geometry-biased selection.

2. The effect may differ between classical and learned pipelines.
   A two-subarray SS variant that is acceptable for classical controls may still hurt SubspaceNet because the learned model was trained assuming the default preprocessing statistics.

3. The change may alter more than "smoothing strength."
   Using fewer rows changes both averaging count and which physical rows contribute, so the ablation should not be over-interpreted as a pure scalar SS-strength parameter unless all three `2-of-3` variants behave similarly.

## Out Of Scope For This Implementation Phase
- changing LRMC solver behavior
- changing row geometry derivation
- introducing single-row SS as the main study target
- retraining a brand-new architecture beyond existing SubspaceNet-ESPRIT templates

Single-row variants may be worth exploring later, but they should not be mixed into the first implementation pass unless the two-subarray results are already clearly understood.

## Planned Deliverables
- new SS-selection parameters supported in preprocessing code
- backward-compatible handling in classical and SubspaceNet input paths
- dataset-template support for row-subset selection
- one dedicated launcher for the experiment family
- one dedicated experiment-plan document
- result markdown and summary tables generated by `run_ablation.py`

## Suggested Launcher Name
- `run_phase7_groupb_1p9_ss_two_subarray_floor.py`

## Completion Criteria
This implementation phase is complete when:
- the repo can run full `3-of-3` and each `2-of-3` SS variant without manual code edits
- the default baseline remains unchanged
- the experiment family can label and compare variants unambiguously
