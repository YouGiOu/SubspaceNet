# Phase 7B Phase 1.1.1 Group B 1.9 Lambda 1x1 SS-Fusion Experiment Plan

## Goal
Evaluate whether a `1x1` channel-only SS-fusion module can outperform the three current learned baselines already established for the primary hard coherent cell from Phase `1.1`.

This phase is intentionally narrow.

It is not a broad new sweep.

It is a controlled architectural comparison built directly on top of Phase `1.1`.

## Primary Question
In the primary coherent hard cell:
- gap `1 deg`
- SNR `1 dB`
- `T = 40`

does the `1x1` SS-fusion model outperform:
- the current spatial-CNN SS-fusion Phase `1.1` model
- the standard `SS(3/3) -> LRMC -> SubspaceNet -> ESPRIT` baseline
- the best fixed `SS(2/3: rows 0+1) -> LRMC -> SubspaceNet -> ESPRIT` baseline

## Why This Phase Matters
Phase `1.1` already established that learned fusion is promising in the single most important coherent hard cell.

What remains unclear is why it helped:
- because adaptive branch fusion is genuinely useful
- or because the `3x3` spatial CNN had enough freedom to rewrite local covariance structure

The `1x1` variant is the cleanest next test because it restricts the model to channel mixing at each covariance entry.

If the `1x1` model still wins, that would strongly support the interpretation that:
- the value is mainly adaptive branch fusion

If it loses clearly, that would suggest that:
- some of the gain from Phase `1.1` came from spatial covariance editing rather than pure branch fusion

## Test Cell
Use exactly the same main cell as Phase `1.1`:
- coherent
- Group B `1.9 lambda`
- gap `1 deg`
- SNR `1 dB`
- `T = 40`

## Training Scale
Use the same current SubspaceNet large-training scale as Phase `1.1`.

Reason:
- this phase is meant to be directly comparable to Phase `1.1`
- reducing the training scale would weaken the interpretation of any observed difference

## Candidate Model
Candidate learned pipeline:
- `SS(2/3 x 3) -> LRMC -> 1x1 learned fusion -> SubspaceNet -> ESPRIT`

Readable label:
- `SS(2/3 x 3) -> LRMC -> 1x1 learned fusion -> SubspaceNet`

## Baselines
The three comparison baselines for this phase are:

1. Current learned SS-fusion Phase `1.1`
- `SS(2/3 x 3) -> LRMC -> learned fusion -> SubspaceNet`

2. Standard learned baseline
- `SS(3/3) -> LRMC -> SubspaceNet`

3. Best fixed reduced-SS learned baseline
- `SS(2/3: rows 0+1) -> LRMC -> SubspaceNet`

These baselines should be reused directly from Phase `1.1` if:
- the cell definition matches exactly
- the training scale matches closely enough
- the evaluation protocol is unchanged

Only rerun a baseline if fairness requires it.

## Fixed Conditions
- Array: Group B 12-channel 2D hardware geometry
- Physical spacing: `1.9 lambda`
- Sources: `M = 2`, coherent, narrowband
- Snapshots: `T = 40`
- Azimuth range: `[-15 deg, 15 deg]`
- Elevation range: `[-15 deg, 15 deg]`
- Gap: `1 deg`
- SNR: `1 dB`
- LRMC rank: `3`
- LRMC solver: `svd`
- LRMC initialization: `lag`
- Learned head: ESPRIT
- Seed: fixed at `42`

## Controlled Variable
The main changed variable relative to Phase `1.1` should be:
- fusion kernel type

Current Phase `1.1`:
- spatial CNN fusion with `3x3` kernels before final `1x1` projection

Phase `1.1.1`:
- `1x1` channel-only fusion

Everything else should be held as constant as practical.

## Success Criteria

### Minimal success
The `1x1` model beats both fixed learned baselines:
- `SS(3/3) -> LRMC -> SubspaceNet`
- `SS(2/3: rows 0+1) -> LRMC -> SubspaceNet`

in the primary hard coherent cell.

### Strong success
The `1x1` model also matches or beats the current Phase `1.1` spatial-fusion model.

That would indicate that:
- the main value is adaptive branch fusion itself
- spatial covariance mixing is not necessary for the observed gain

### Informative negative result
If the `1x1` model beats the fixed baselines but loses to the Phase `1.1` spatial-fusion model, then:
- adaptive branch fusion is useful
- but some additional value may still come from spatial processing

### No-go result
If the `1x1` model loses clearly to all three Phase `1.1` baselines, then:
- channel-only fusion is probably too restrictive in this formulation
- the current spatial-fusion path remains the more promising direction

## Metrics
Primary metric:
- horizontal-angle RMSE

Secondary metrics:
- training stability
- validation RMSE
- fusion diagnostics
- runtime / memory overhead relative to Phase `1.1`

## Interpretation Rules

### If 1x1 beats all three baselines
Conclusion:
- the branch-fusion idea is strong
- the gain does not rely on free spatial convolution
- a more structure-preserving learned fusion should become the preferred next direction

### If 1x1 beats the two fixed baselines but not Phase `1.1`
Conclusion:
- adaptive fusion is genuinely helpful
- but the current spatial CNN still adds something beyond channel-only mixing

### If 1x1 ties Phase `1.1` within a small margin
Conclusion:
- the safer `1x1` formulation may be preferable on engineering grounds because it is simpler and more structure-preserving

### If 1x1 loses to `SS(3/3)` and the fixed `rows 0+1` baseline
Conclusion:
- the current channel-only formulation is not sufficient
- future constrained-fusion work should likely use weighted fusion, residual fusion, or better structural constraints rather than this exact module

## Expected Outputs
Running this phase should produce:
- per-model `metrics.json`
- training curves and checkpoints
- one family markdown results file
- `summary.csv`

Recommended results path:
- `results/phase7b_groupb_1p9_learned_ss_fusion_phase1p1p1/`

Recommended markdown result file:
- `phase7b_groupb_1p9_learned_ss_fusion_phase1p1p1_results.md`

## Canonical Launcher
- `run_phase7b_groupb_1p9_learned_ss_fusion_phase1p1p1.py`

Recommended command:
```bash
python run_phase7b_groupb_1p9_learned_ss_fusion_phase1p1p1.py
```

## Go / No-Go Rule
Promote the `1x1` variant to the next coherent hard cells only if:
- it is stable to train
- it beats the two fixed learned baselines
- and it is at least competitive with the current Phase `1.1` spatial-fusion model

Otherwise:
- keep the current Phase `1.1` model as the stronger adaptive-fusion reference
- and treat the `1x1` result as a useful structural ablation rather than a replacement
