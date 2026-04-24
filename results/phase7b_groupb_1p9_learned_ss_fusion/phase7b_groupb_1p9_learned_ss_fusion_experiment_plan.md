# Phase 7B Group B 1.9 Lambda Learned SS-Fusion Experiment Plan

## Goal
Test whether a learnable fusion of the three `SS(2/3)` row-pair LRMC covariances can outperform both:
- the fixed `SS(3/3) -> LRMC -> SubspaceNet -> ESPRIT` pipeline
- any single fixed `SS(2/3) -> LRMC -> SubspaceNet -> ESPRIT` variant

This phase is motivated directly by Phase 7A, which showed:
- `SS(2/3)` can sometimes outperform `SS(3/3)`
- not all `2-of-3` row pairs behave the same
- row-pair identity matters most in hard coherent cells

The learned-fusion idea is therefore to let the model adaptively exploit these branch differences instead of hard-coding one averaging rule.

## Main Hypothesis
The new model can learn a better hard-regime covariance surrogate by fusing the three `2-of-3` LRMC branches than by relying on:
- a fixed `3-of-3` SS average
- or any one fixed row-pair choice

## Secondary Hypotheses
1. The largest gains, if they exist, will appear in hard coherent cells rather than easy cells.
2. In easier non-coherent cells, the learned fusion may offer little advantage because the classical and learned baselines are already near saturation.
3. If the learned fusion helps, it will likely help by behaving like an adaptive branch selector rather than a uniform average.

## Model Under Test
The candidate learned pipeline is:
- `three SS(2/3) branches`
- `LRMC on each branch`
- `learned covariance fusion`
- `SubspaceNet backbone`
- `differentiable ESPRIT head`

Readable label:
- `SS(2/3 x 3) -> LRMC -> learned fusion -> SubspaceNet -> ESPRIT`

## Baselines

### Learned Baselines
The new model must be compared against:
- `SS(3/3) -> LRMC -> SubspaceNet -> ESPRIT`
- best fixed `SS(2/3) -> LRMC -> SubspaceNet -> ESPRIT`
- optionally worst fixed `SS(2/3) -> LRMC -> SubspaceNet -> ESPRIT` for contrast

The "best fixed `SS(2/3)`" baseline should be chosen from Phase 7A evidence, not guessed.

For the current coherent hard-cell evidence, the strongest candidate to carry forward first is:
- `SS(2/3: rows 0+1)`

### Classical Reference Baselines
Each study cell should also report classical references:
- `SS(3/3) -> LRMC` classical controls
- best fixed `SS(2/3) -> LRMC` classical controls

These are not the main learning baselines, but they are important to show whether the new model is actually exceeding the best known classical preprocessing choices.

## Recommended Study Order

### Phase 1: Hard Coherent Feasibility
Break the first coherent feasibility screen into three ordered sub-phases rather than training all three cells at once.

This reduces risk while keeping the training scale scientifically comparable to the current strong SubspaceNet baseline.

### Phase 1.1: Primary Hard Cell Reproduction
Run only:
- coherent
- gap `1 deg`
- SNR `1 dB`
- `T = 40`

Use the current paper-scale SubspaceNet training size for this first check rather than a reduced screening budget.

Reason:
- this is the hardest and most important currently established coherent cell
- it already has an existing trained baseline for `SS(3/3) -> LRMC -> SubspaceNet -> ESPRIT`
- the new learned-fusion model can therefore be compared directly against a known strong reference without retraining that baseline first

This sub-phase answers:
- can learned SS fusion beat the existing strongest known learned baseline in the single most important coherent hard cell?

### Phase 1.2: Same Gap, Easier SNR
Only if Phase 1.1 is promising, extend to:
- coherent
- gap `1 deg`
- SNR `10 dB`
- `T = 40`

This sub-phase answers:
- does the gain persist when the cell is still separation-limited but less SNR-limited?

### Phase 1.3: Slightly Easier Separation
Only if Phases 1.1 and 1.2 remain promising, extend to:
- coherent
- gap `2 deg`
- SNR `1 dB`
- `T = 40`

This sub-phase answers:
- is the gain specific to the absolute hardest coherent point, or does it generalize to the next hard boundary cell?

### Phase 2: Hard Coherent Snapshot Stress
If Phase 1 is promising, extend to snapshot stress in the hardest cell:
- coherent
- gap `1 deg`
- SNR `1 dB`
- `T = 1, 2, 4, 8, 16, 25, 40`

This phase answers:
- does learned fusion improve low-snapshot robustness on top of current SubspaceNet?

### Phase 3: Non-Coherent Check
Only after coherent evidence is clear, test a smaller non-coherent set:
- gap `1 deg`, SNR `1 dB`, `T = 40`
- gap `1 deg`, SNR `10 dB`, `T = 40`
- gap `2 deg`, SNR `1 dB`, `T = 40`

This phase answers:
- is the learned-fusion gain specific to coherent hard cells, or broader?

## Fixed Conditions
- Array: Group B 12-channel 2D hardware geometry
- Physical spacing: `1.9 lambda`
- Sources: `M = 2`, narrowband
- Azimuth range: `[-15 deg, 15 deg]`
- Elevation range: `[-15 deg, 15 deg]`
- Virtual ULA size: derive from code, expected to be `9`
- LRMC rank: `3`
- LRMC solver: `svd`
- LRMC initialization: `lag`
- Learned head: ESPRIT only
- Seed: fixed at `42`

## Dataset Size Guidance
For Phase 1.1, use the current standard SubspaceNet large-training scale so the first comparison is directly aligned with the strongest existing learned baseline in the same cell.

Recommended rule:
- Phase 1.1: use the current full SubspaceNet training scale
- Phases 1.2 and 1.3: keep the same full scale if Phase 1.1 is promising and resources permit
- if runtime becomes limiting after Phase 1.1, later sub-phases may fall back to a reduced screening size, but that should be treated as a secondary screening mode rather than the primary evidence

Important comparison rule:
- when Phase 1.1 uses the same training scale and same cell as the existing `SS(3/3) -> LRMC -> SubspaceNet -> ESPRIT` run, the baseline should be reused directly from the existing result if the preprocessing, dataset definition, and training protocol match closely enough
- if any of those differ materially, rerun the baseline in the new family for fairness

## Metrics
Primary metric:
- horizontal-angle RMSE

Secondary metrics:
- training loss stability
- validation RMSE
- branch-fusion diagnostics
- runtime / memory overhead relative to standard SubspaceNet

## Success Criteria

### Minimal success
In Phase 1.1, the new model beats the existing `SS(3/3) -> LRMC -> SubspaceNet -> ESPRIT` baseline in the `1 deg`, `1 dB`, `T = 40` coherent cell without obvious training instability.

### Strong success
The new model consistently beats both:
- full `SS(3/3)` learned baseline
- best fixed `SS(2/3)` learned baseline

across Phases `1.1`, `1.2`, and `1.3`.

### Negative but still useful result
If the new model matches but does not beat the best fixed `SS(2/3)` baseline, that still suggests:
- the useful information may already be captured by selecting the right fixed row pair
- adaptive fusion may not justify the added model complexity

## Key Ablation Questions

### 1. Does learned fusion beat the best fixed row pair?
This is the main scientific question.

If no:
- the practical conclusion may simply be to use the best fixed `2-of-3` branch in hard coherent cells

If yes:
- then branch interaction contains useful information beyond fixed selection

### 2. Is the gain due to multi-branch information or just extra capacity?
To partially control for this, compare against:
- standard SubspaceNet with its current input
- fixed best `SS(2/3)` SubspaceNet baseline

### 3. Does the model act like a soft selector?
This should be checked through diagnostics rather than inference alone.

If the model repeatedly emphasizes one row pair in one regime and another pair in another regime, that strongly supports the original idea.

## Interpretation Rules

### If learned fusion wins mainly in coherent `1 deg` cells
Conclusion:
- the method is targeting the right boundary
- it is likely exploiting regime-dependent branch differences

### If learned fusion wins nowhere
Conclusion:
- the practical value of Phase 7A may be simpler branch selection, not adaptive fusion

### If learned fusion helps only at low snapshots
Conclusion:
- the main value is not average performance but hard-regime robustness

### If learned fusion helps in coherent but not non-coherent cells
Conclusion:
- the method is specifically addressing the hard coherent SS-floor problem

## Risks
1. Training may become less stable because the model now learns both covariance fusion and surrogate covariance refinement.
2. The gain may disappear after fair comparison with the best fixed `SS(2/3)` learned baseline.
3. The model may overfit to the small number of hard training cells used in the first feasibility sweep.

## Expected Outputs
Running the experiment family should produce:
- per-model `metrics.json`
- training curves and checkpoints
- one results markdown summary
- `summary.csv`

Recommended results path:
- `results/phase7b_groupb_1p9_learned_ss_fusion/`

Recommended family markdown:
- `phase7b_groupb_1p9_learned_ss_fusion_results.md`

## Canonical Launcher
- `run_phase7b_groupb_1p9_learned_ss_fusion.py`

Recommended command:
```bash
python run_phase7b_groupb_1p9_learned_ss_fusion.py
```

## Go / No-Go Rule After Phase 1.1
Proceed to larger-scale training only if:
- the new model is stable to train
- it beats the reused or rerun `SS(3/3)` learned baseline in Phase `1.1`
- and it is competitive with or better than the best fixed `SS(2/3)` learned baseline for that same cell

Otherwise, the better next step is likely:
- a fixed-row-pair learned study
- not a more complex adaptive-fusion architecture
