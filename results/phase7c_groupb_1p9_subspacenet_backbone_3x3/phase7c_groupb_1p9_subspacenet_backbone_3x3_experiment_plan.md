# Phase 7C Group B 1.9 Lambda SubspaceNet 3x3 Backbone Experiment Plan

## Goal
Quickly test whether replacing the original SubspaceNet `2x2` encoder/decoder kernels with `3x3` kernels changes performance in the already-established Phase `7B` primary coherent hard-cell setting.

This is a controlled backbone comparison, not a new regime sweep.

## Primary Question
Under exactly the same Phase `7B` primary hard-cell setting, does a `3x3` SubspaceNet backbone outperform, match, or underperform the current `2x2` backbone?

## Fixed Cell
Use the same cell already established in:
- Phase `7B` Phase `1.1`
- Phase `7B` Phase `1.1.1`

That means:
- Group B `1.9 lambda`
- coherent
- `M = 2`
- gap `1 deg`
- SNR `1 dB`
- `T = 40`
- azimuth and elevation range `[-15 deg, 15 deg]`
- learned head: ESPRIT
- `tau = 8`
- canonical preprocessing for the learned paths already used in those phases

## Scope
Run only the new `3x3` backbone variants.

Do not rerun the old `2x2` variants.

Use the already completed Phase `7B` results as the comparison reference.

## Comparison Set
The cleanest comparison set is the same four learned pipelines already used across Phase `1.1` and Phase `1.1.1`, but with the backbone changed to `3x3`.

### New Runs Required
1. `SS(3/3) -> LRMC -> SubspaceNet(backbone 3x3) -> ESPRIT`
2. `SS(2/3: rows 0+1) -> LRMC -> SubspaceNet(backbone 3x3) -> ESPRIT`
3. `SS(2/3 x 3) -> LRMC -> Phase 1.1 spatial fusion -> SubspaceNet(backbone 3x3) -> ESPRIT`
4. `SS(2/3 x 3) -> LRMC -> Phase 1.1.1 1x1 fusion -> SubspaceNet(backbone 3x3) -> ESPRIT`

### Existing 2x2 References To Reuse
1. Phase `1.1` standard learned baseline:
- `SS(3/3) -> LRMC -> SubspaceNet(backbone 2x2) -> ESPRIT`

2. Phase `1.1` best fixed reduced-SS learned baseline:
- `SS(2/3: rows 0+1) -> LRMC -> SubspaceNet(backbone 2x2) -> ESPRIT`

3. Phase `1.1` spatial-fusion learned model:
- `SS(2/3 x 3) -> LRMC -> learned fusion -> SubspaceNet(backbone 2x2) -> ESPRIT`

4. Phase `1.1.1` `1x1` learned-fusion model:
- `SS(2/3 x 3) -> LRMC -> 1x1 learned fusion -> SubspaceNet(backbone 2x2) -> ESPRIT`

## Main Hypotheses
1. A `3x3` backbone may help because the surrogate-covariance refinement stage sees a wider local receptive field at every encoder and decoder block.
2. Any gain is most likely to appear in the fusion-based models, where the backbone is already operating on a fused covariance representation built from difficult coherent branch structure.
3. A wider kernel may also hurt by over-smoothing or by making training less stable in this small spatial domain, so underperformance remains plausible.

## Controlled Variable
The intended changed variable is:
- SubspaceNet encoder/decoder kernel size

From:
- `2x2`

To:
- `3x3`

Everything else should be held fixed as closely as possible:
- same dataset definition
- same seed
- same training scale
- same optimizer and schedule
- same fusion block
- same LRMC settings
- same evaluation code

## Training Scale
Use the same large-training scale already used for the former hard-cell learned runs.

Recommended target:
- keep the same sample counts and split definitions used in Phase `1.1` and Phase `1.1.1`

Reason:
- this is the fairest backbone comparison
- any reduction in training scale would weaken interpretation

## Metrics
Primary metric:
- horizontal-angle RMSE in degrees

Secondary metrics:
- validation RMSE
- train/validation loss stability
- runtime per epoch
- GPU memory footprint if easy to log

## Success Criteria

### Minimal success
At least one `3x3` backbone variant improves over its direct `2x2` counterpart without obvious instability.

### Strong success
The `3x3` backbone improves the main fusion candidate:
- Phase `1.1` spatial-fusion model

and either:
- also improves the `1x1` fusion model
- or improves both fixed learned baselines

### Informative negative result
If all `3x3` variants match or underperform the `2x2` references, that is still useful evidence that:
- the original `2x2` SubspaceNet backbone is already well matched to this covariance-resolution setting
- widening the receptive field alone is not the reason the Phase `7B` gains appeared

## Interpretation Rules

### If 3x3 helps only the fusion models
Conclusion:
- wider backbone context is most useful after adaptive branch fusion
- the effect is probably interacting with fused covariance cleanup rather than plain LRMC completion

### If 3x3 helps all four models
Conclusion:
- the SubspaceNet backbone itself was likely under-receptive in the current `9 x 9` covariance regime
- the improvement is not specific to one fusion design

### If 3x3 helps none of the models
Conclusion:
- the current `2x2` backbone remains the practical default
- future work should focus on fusion design or training strategy rather than backbone kernel size

### If 3x3 helps fixed baselines but not fusion models
Conclusion:
- the wider kernel may mainly compensate for weaker preprocessing
- the stronger fusion models may already be saturating the useful local structure

## Recommended Output Structure
Create a new family:
- `results/phase7c_groupb_1p9_subspacenet_backbone_3x3/`

Recommended family markdown:
- `phase7c_groupb_1p9_subspacenet_backbone_3x3_results.md`

Recommended `summary.csv`:
- include only the newly run `3x3` variants

The markdown discussion should also include a direct comparison table against the reused `2x2` references.

## Recommended Result Table
At minimum, report:

- scheme label
- fusion type
- backbone kernel
- RMSE
- delta vs direct `2x2` counterpart

Recommended row pairing:
- `SS(3/3)` `2x2` vs `3x3`
- `SS(2/3: rows 0+1)` `2x2` vs `3x3`
- spatial-fusion `2x2` vs `3x3`
- `1x1`-fusion `2x2` vs `3x3`

## Canonical Launcher
Recommended new launcher:
- `run_phase7c_groupb_1p9_subspacenet_backbone_3x3.py`

Recommended command:
```bash
python run_phase7c_groupb_1p9_subspacenet_backbone_3x3.py
```

## Go / No-Go Rule
Promote the `3x3` backbone beyond this cell only if:

- training remains stable
- at least the main fusion candidate is improved or clearly competitive
- and the gain is large enough to justify the added architectural change

Otherwise:
- keep the current `2x2` backbone as default
- treat the `3x3` run as a targeted architectural ablation
