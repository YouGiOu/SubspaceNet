# Phase 7E Group B 1.9 Lambda Anti-Rectifier Fusion Generalization Experiment Plan

## Goal
Test the generalization ability of the current strongest learned model:

- `SS(2/3 x 3) -> LRMC -> width-controlled anti-rectifier spatial fusion -> SubspaceNet(3x3) -> ESPRIT`

The main purpose is to evaluate the already trained hard-cell model on existing cached test datasets from other angular separations, other SNR values, and both coherence types, without introducing new dataset generation.

This phase is an evaluation-transfer study, not a retraining sweep.

## Primary Question
If a model is trained in the single hardest coherent source cell:
- coherent
- gap `1 deg`
- SNR `1 dB`
- `T = 40`

how well does it transfer to other Group B `1.9 lambda` cells when we change:
- angular separation
- SNR
- signal coherence

while keeping the physical geometry and the overall learned pipeline fixed?

## Why This Phase Matters
Phase `7D` established the strongest result so far in the primary coherent hard cell:
- anti-rectifier spatial fusion with the `3x3` backbone reached about `0.3592 deg`

That is an important local win, but it still leaves the main practical question open:
- is this model only highly tuned to the single `1 deg`, `1 dB`, coherent cell
- or has it learned a representation that transfers across nearby and moderately shifted Group B conditions?

Because the Phase 6 fixed-gap / SNR grids were already generated and cached for both coherent and non-coherent signals, the repo already contains a strong reuse-based test bed for this question.

## Model Under Test
Use the already trained Phase `7D` model checkpoint only.

Do not retrain.

Model under test:
- `SS(2/3 x 3) -> LRMC -> width-controlled anti-rectifier spatial fusion -> SubspaceNet(backbone 3x3) -> ESPRIT`

Recommended readable label:
- `anti-rectifier SS-fusion 3x3`

## Training Cell
The model was trained on:
- coherent
- gap `1 deg`
- SNR `1 dB`
- `T = 40`
- Group B `1.9 lambda`

This is the in-domain anchor cell for interpretation.

## Reusable Existing Datasets
The following cached dataset families already exist and can be reused from:
- `data/datasets/`

### Existing coherent fixed-gap / SNR grid caches
Reusable directories already present:
- `phase6_groupb_1p9_coherent_gap1_snr1_45k`
- `phase6_groupb_1p9_coherent_gap1_snr5_45k`
- `phase6_groupb_1p9_coherent_gap1_snr10_45k`
- `phase6_groupb_1p9_coherent_gap1_snr15_45k`
- `phase6_groupb_1p9_coherent_gap2_snr1_45k`
- `phase6_groupb_1p9_coherent_gap2_snr5_45k`
- `phase6_groupb_1p9_coherent_gap2_snr10_45k`
- `phase6_groupb_1p9_coherent_gap2_snr15_45k`
- `phase6_groupb_1p9_coherent_gap3_snr1_45k`
- `phase6_groupb_1p9_coherent_gap3_snr5_45k`
- `phase6_groupb_1p9_coherent_gap3_snr10_45k`
- `phase6_groupb_1p9_coherent_gap3_snr15_45k`
- `phase6_groupb_1p9_coherent_gap4_snr1_45k`
- `phase6_groupb_1p9_coherent_gap4_snr5_45k`
- `phase6_groupb_1p9_coherent_gap4_snr10_45k`
- `phase6_groupb_1p9_coherent_gap4_snr15_45k`
- `phase6_groupb_1p9_coherent_gap5_snr1_45k`
- `phase6_groupb_1p9_coherent_gap5_snr5_45k`
- `phase6_groupb_1p9_coherent_gap5_snr10_45k`
- `phase6_groupb_1p9_coherent_gap5_snr15_45k`

### Existing non-coherent fixed-gap / SNR grid caches
Reusable directories already present:
- `phase6_groupb_1p9_noncoherent_gap1_snr1_45k`
- `phase6_groupb_1p9_noncoherent_gap1_snr5_45k`
- `phase6_groupb_1p9_noncoherent_gap1_snr10_45k`
- `phase6_groupb_1p9_noncoherent_gap1_snr15_45k`
- `phase6_groupb_1p9_noncoherent_gap2_snr1_45k`
- `phase6_groupb_1p9_noncoherent_gap2_snr5_45k`
- `phase6_groupb_1p9_noncoherent_gap2_snr10_45k`
- `phase6_groupb_1p9_noncoherent_gap2_snr15_45k`
- `phase6_groupb_1p9_noncoherent_gap3_snr1_45k`
- `phase6_groupb_1p9_noncoherent_gap3_snr5_45k`
- `phase6_groupb_1p9_noncoherent_gap3_snr10_45k`
- `phase6_groupb_1p9_noncoherent_gap3_snr15_45k`
- `phase6_groupb_1p9_noncoherent_gap4_snr1_45k`
- `phase6_groupb_1p9_noncoherent_gap4_snr5_45k`
- `phase6_groupb_1p9_noncoherent_gap4_snr10_45k`
- `phase6_groupb_1p9_noncoherent_gap4_snr15_45k`
- `phase6_groupb_1p9_noncoherent_gap5_snr1_45k`
- `phase6_groupb_1p9_noncoherent_gap5_snr5_45k`
- `phase6_groupb_1p9_noncoherent_gap5_snr10_45k`
- `phase6_groupb_1p9_noncoherent_gap5_snr15_45k`

### Existing in-domain anchor cache
Also already present:
- `p7b_p1p1_coh_g1_s1_45k`

This can be used if an exact Phase `7D`-style in-domain evaluation anchor is wanted in addition to the Phase 6 coherent `gap1/snr1` cache.

## Important Reuse Note
The underlying test datasets already exist and should be reused.

However, because the Phase `7D` model type is not the same cached model type as the old Phase 6 SubspaceNet test tensors, the clean reuse rule should be:
- reuse the existing cached test snapshots and labels
- reuse the existing cached generic test datasets and `samples_model`
- if needed, rebuild only the model-input tensors for the Phase `7D` model from those cached generic snapshots
- do not resample DOAs
- do not regenerate observation noise
- do not create new random datasets unless the cache is genuinely missing

In short:
- dataset reuse is required
- model-input conversion is allowed
- stochastic dataset regeneration is not part of this phase

## Scope

### Primary evaluation set
Evaluate on the full reused Phase 6 grid:
- `20` coherent cells
- `20` non-coherent cells

Total reusable evaluation cells:
- `40`

### Recommended interpretation split
For analysis, separate the reused cells into:

1. In-domain anchor
- coherent, gap `1 deg`, SNR `1 dB`

2. Coherent OOD cells
- all other coherent cells: `19`

3. Non-coherent transfer cells
- all non-coherent cells: `20`

This split helps distinguish:
- ordinary hard-cell reproduction
- same-regime coherent transfer
- coherence-shift transfer

## Recommended OOD Buckets
To make the conclusions clearer, report the results in these buckets:

### Bucket A: SNR shift only
Keep gap fixed at `1 deg`, vary SNR:
- coherent: `(1 deg, 5/10/15 dB)`
- non-coherent: `(1 deg, 1/5/10/15 dB)`

### Bucket B: gap shift only
Keep SNR fixed at `1 dB`, vary gap:
- coherent: `(2/3/4/5 deg, 1 dB)`
- non-coherent: `(1/2/3/4/5 deg, 1 dB)`

### Bucket C: joint gap + SNR shift
Change both:
- coherent: gaps `2..5 deg`, SNR `5/10/15 dB`
- non-coherent: gaps `2..5 deg`, SNR `5/10/15 dB`

### Bucket D: full non-coherent transfer
All `20` non-coherent cells as one family

This is important because non-coherent transfer is not just a mild parameter shift.
It is a meaningful signal-model shift relative to the coherent training cell.

## Main Hypotheses
1. The anti-rectifier fusion model should transfer best to nearby coherent hard cells, especially small gap and low-SNR cells.
2. Transfer to easier coherent cells may remain strong or even improve in RMSE because the task itself becomes easier.
3. Transfer to non-coherent cells may still be good, but because the model was trained on coherent structure, this should be treated as meaningful out-of-distribution transfer rather than assumed success.
4. If performance stays strong across much of the reused grid, that would support the interpretation that the learned model has captured useful Group B structural priors rather than merely memorizing one hard cell.

## Baselines For Comparison
This phase is primarily about generalization of the strongest learned model, not about retraining baselines.

Still, interpretation should compare against existing Phase 6 / Phase 7 references where useful:
- Phase 6 classical controls on each reused cell
- Phase 6 or Phase 7 learned references where the same cell was previously trained directly

The most important comparison questions are:
- how much degradation occurs relative to the model's own training cell
- whether coherent transfer remains better than classical controls in hard cells
- whether non-coherent transfer is competitive with classical controls in easier cells

## Fixed Conditions
Keep fixed:
- geometry: Group B 12-channel 2D hardware geometry
- physical spacing: `1.9 lambda`
- snapshots: `T = 40`
- learned head: ESPRIT
- fusion design: width-controlled anti-rectifier spatial fusion
- backbone kernel: `3x3`
- checkpoint: use the already trained Phase `7D` checkpoint only

## Metrics
Primary metric:
- horizontal-angle RMSE in degrees

Secondary metrics:
- average runtime per sample
- average runtime per evaluation batch or per dataset pass, if that is easier to log consistently
- delta vs the training cell RMSE
- delta vs the corresponding classical Phase 6 control on the same reused cell
- average RMSE within each OOD bucket
- worst-cell RMSE
- best-cell RMSE

## Runtime Speed Metric
Because Phase `7E` is a transfer-evaluation study rather than only a pure accuracy check, runtime speed should also be recorded explicitly.

Recommended runtime measurements:
- average end-to-end evaluation time per sample
- average end-to-end evaluation time per reused test cell

If available with low implementation effort, also report:
- average model forward time per sample
- average LRMC plus model pipeline time per sample

Important interpretation note:
- the most useful runtime figure in this phase is the full inference-path cost on reused test data
- that means preprocessing plus learned inference is preferable to reporting neural-network forward time alone

If GPU timing is noisy or inconvenient, CPU wall-clock timing is acceptable as long as:
- the same evaluation path is used for every reused cell
- the timing method is kept consistent across the whole Phase `7E` study

## Success Criteria

### Minimal success
The model remains clearly usable across the coherent OOD cells, especially in the small-gap regime:
- coherent gaps `1 - 2 deg`
- low to moderate SNR

### Strong success
The model transfers well across most coherent OOD cells and remains competitive on much of the non-coherent grid too, without catastrophic collapse.

### Informative negative result
If performance is strong only in the original coherent hard cell and degrades sharply elsewhere, that is still useful evidence that:
- the current strongest model is highly cell-specialized
- broader robustness would likely require multi-cell or mixed-condition training

## Interpretation Rules

### If coherent OOD transfer is strong but non-coherent transfer is weak
Conclusion:
- the model has learned robust coherent Group B structure
- but it has not generalized across coherence type

### If both coherent and non-coherent transfer are strong
Conclusion:
- the learned model is capturing broader geometry-conditioned covariance structure, not only the single training cell

### If only nearby hard cells transfer well
Conclusion:
- the current model is locally robust around the training regime
- but still behaves mainly as a specialized hard-cell expert

### If easier cells perform much better than the training cell
Conclusion:
- the model likely learned a useful structural prior and then benefits naturally as the task becomes easier

## Recommended Output Structure
Create a new family:
- `results/phase7e_groupb_1p9_antirect_fusion_generalization/`

Recommended markdown:
- `phase7e_groupb_1p9_antirect_fusion_generalization_results.md`

Recommended `summary.csv`:
- one row per reused evaluation cell

## Recommended Result Tables
At minimum, report:

1. full coherent reused grid
- gap
- SNR
- RMSE
- average runtime per sample
- delta vs Phase `7D` training-cell RMSE

2. full non-coherent reused grid
- gap
- SNR
- RMSE
- average runtime per sample
- delta vs Phase `7D` training-cell RMSE

3. grouped summary table
- bucket name
- number of cells
- mean RMSE
- mean runtime per sample
- median RMSE
- worst RMSE

4. optional comparison table
- reused cell
- Phase 6 classical best method
- Phase 7E transferred model RMSE
- Phase 7E transferred model runtime
- difference

## Canonical Launcher
Recommended new launcher:
- `run_phase7e_groupb_1p9_antirect_fusion_generalization.py`

Recommended command:
```bash
python run_phase7e_groupb_1p9_antirect_fusion_generalization.py
```

## Go / No-Go Rule
Treat the current Phase `7D` model as a candidate broader default only if:
- it transfers well across the coherent OOD cells
- it shows no catastrophic failure on the non-coherent grid
- and its advantages are not limited only to the exact training cell

Otherwise:
- treat it as the best current hard-cell specialist
- and plan any broader deployment around mixed-cell or mixed-regime retraining
