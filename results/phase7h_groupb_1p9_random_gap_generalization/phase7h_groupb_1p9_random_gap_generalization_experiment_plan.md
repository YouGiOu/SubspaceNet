# Phase 7H Group B 1.9 Lambda Random-Gap Generalization Experiment Plan

## Goal
Evaluate the current Phase `7G` boundary-repair model on test datasets with:
- random angular separations
- azimuth range still limited to `[-15 deg, 15 deg]`
- SNR values `1, 5, 10, 15 dB`

The purpose is to check whether the Phase `7G` model, which was tuned using fixed-gap and boundary-aware training logic, still performs well when the angular separation is no longer locked to the discrete `1, 2, 3, 4, 5 deg` grid.

This phase is an evaluation-only study, not a retraining phase.

## Model Under Test
Use the already trained Phase `7G` model checkpoint only.

Model family:
- `SS(2/3 x 3) -> LRMC -> width-controlled anti-rectifier spatial fusion -> SubspaceNet backbone 3x3 -> ESPRIT`

Recommended readable label:
- `Phase 7G boundary-repair anti-rectifier fusion 3x3`

## Primary Question
When evaluated on random azimuth separations inside the same `[-15 deg, 15 deg]` field of view, how well does the Phase `7G` model generalize compared with the earlier fixed-gap evaluations?

More specifically:
- does the model remain strong when gap is no longer one of the exact trained / evaluated grid values
- does it behave more like a true deployment model over continuous angle differences
- or does its strength depend mainly on the fixed-gap grid structure used in earlier phases

## Why This Phase Matters
Phases `7E`, `7F`, and `7G` all used evaluation sets organized around fixed azimuth gaps.

That was useful for:
- clean boundary analysis
- phase-to-phase comparability
- diagnosing the `1 deg` and `2 deg` coherent difficulty structure

But practical deployment will not present only those exact grid gaps.

So the next needed check is:
- continuous random gap evaluation

This phase therefore tests whether the current model behaves well under a more natural continuous test distribution while keeping the same geometry, snapshot count, and SNR support.

## Scope
Run only the Phase `7G` model checkpoint.

Do not retrain.

Do not run the older Phase `7D`, `7F`, or classical baselines again unless a later follow-up specifically requests it.

This plan is only for the new random-gap evaluation family.

## Fixed Conditions
Keep fixed:
- geometry: Group B 12-channel 2D hardware geometry
- physical spacing: `1.9 lambda`
- snapshots: `T = 40`
- azimuth range: `[-15 deg, 15 deg]`
- learned head: ESPRIT
- fusion design: width-controlled anti-rectifier spatial fusion
- backbone kernel: `3x3`
- checkpoint: use the best Phase `7G` checkpoint only

## Test Distribution
Use random source angles rather than exact fixed gaps.

### Angular setup
- azimuth range remains `[-15 deg, 15 deg]`
- source azimuths should be drawn randomly within that field of view
- the separation between the two sources is therefore random rather than fixed to one discrete grid value

### Important recommendation
Do not allow arbitrarily tiny accidental gaps unless that is explicitly desired.

Recommended default:
- keep a minimum azimuth gap constraint for dataset validity
- but do not set `fixed_doa_gap`

Best practical default:
- `min_doa_gap = 1 deg`
- no fixed-gap constraint

This preserves consistency with earlier hard-regime logic while still producing a continuous gap distribution.

## SNR Coverage
Evaluate separately at:
- `1 dB`
- `5 dB`
- `10 dB`
- `15 dB`

Recommended structure:
- one random-gap test dataset per SNR value

## Coherence Coverage
Because Phase `7G` was mainly a coherent boundary-repair phase, the most important first evaluation is:
- coherent random-gap testing

However, if practical coverage is desired and runtime is acceptable, the cleaner full design is:
- coherent random-gap family
- non-coherent random-gap family

### Recommended minimum scope
At minimum:
- coherent random-gap evaluation at all four SNR values

### Recommended full scope
Preferred if the user wants the strongest deployment readout:
- coherent: `4` SNR-specific random-gap test sets
- non-coherent: `4` SNR-specific random-gap test sets

Total:
- `8` evaluation cells

## Test Sample Count
Keep:
- `9,000` test samples per evaluation dataset

This matches the current repo’s paper-scale evaluation convention and keeps results comparable to the earlier phases.

## Dataset Generation Rule
This phase introduces new random-gap test sets, so cached fixed-gap Phase 6 datasets are not sufficient by themselves.

Therefore:
- new test datasets should be generated for this phase
- these new datasets should be saved for reuse
- no training dataset is required

## Recommended Naming
Suggested family:
- `results/phase7h_groupb_1p9_random_gap_generalization/`

Recommended markdown:
- `phase7h_groupb_1p9_random_gap_generalization_results.md`

Recommended launcher:
- `run_phase7h_groupb_1p9_random_gap_generalization.py`

## Evaluation Cells

### Minimum coherent-only version
1. coherent random-gap, `1 dB`
2. coherent random-gap, `5 dB`
3. coherent random-gap, `10 dB`
4. coherent random-gap, `15 dB`

### Preferred coherent + non-coherent version
1. coherent random-gap, `1 dB`
2. coherent random-gap, `5 dB`
3. coherent random-gap, `10 dB`
4. coherent random-gap, `15 dB`
5. non-coherent random-gap, `1 dB`
6. non-coherent random-gap, `5 dB`
7. non-coherent random-gap, `10 dB`
8. non-coherent random-gap, `15 dB`

## Main Hypotheses
1. The Phase `7G` model should remain strongest in coherent low-SNR random-gap evaluation because that is the regime most aligned with its development history.
2. If the model has genuinely learned useful continuous structure rather than only discrete fixed-gap behavior, performance under random gaps should stay close to the neighboring fixed-gap phase results.
3. If the model depends heavily on the fixed-gap training/evaluation structure, random-gap performance may drop, especially in coherent low-SNR settings.
4. Non-coherent random-gap evaluation, if included, should remain easier overall than coherent random-gap evaluation.

## Metrics
Primary metric:
- horizontal-angle RMSE in degrees

Secondary metrics:
- average runtime per sample
- dataset-pass runtime
- if available, summary statistics of the realized random-gap distribution:
  - mean gap
  - median gap
  - minimum realized gap
  - maximum realized gap

## Strongly Recommended Extra Reporting
Because this phase uses random gaps, the results markdown should include a short description of the realized test-gap distribution for each dataset.

At minimum, report:
- number of test samples
- minimum realized gap
- mean realized gap
- median realized gap
- maximum realized gap

Reason:
- this makes the random-gap datasets interpretable
- otherwise RMSE alone is harder to compare against fixed-gap phases

## Baselines For Interpretation
This phase does not need new baseline reruns.

Interpretation should compare against:
- the relevant fixed-gap Phase `7G` cells
- the Phase `7F` random-neighboring difficulty intuition
- the earlier fixed-gap coherent and non-coherent trends from Phases `5C`, `7E`, `7F`, and `7G`

The main question is not exact leaderboard comparison.

It is whether the model behaves smoothly and plausibly when gap is continuous rather than discretized.

## Success Criteria

### Minimal success
The model remains stable and clearly usable under random-gap evaluation, without obvious collapse in the low-SNR coherent case.

### Strong success
The random-gap RMSE values remain broadly consistent with the neighboring fixed-gap phase conclusions, suggesting the model has learned a useful continuous structure rather than only memorizing discrete gap cells.

### Informative negative result
If random-gap performance drops noticeably relative to the fixed-gap phases, that is still useful evidence that:
- the current training/evaluation loop has overfit somewhat to the fixed-gap regime structure
- future deployment training should include more continuous random-gap sampling explicitly

## Recommended Result Tables
At minimum, report:

1. coherent random-gap table
- SNR
- RMSE
- avg runtime / sample
- realized mean gap
- realized median gap
- realized min / max gap

2. non-coherent random-gap table, if included
- SNR
- RMSE
- avg runtime / sample
- realized mean gap
- realized median gap
- realized min / max gap

3. summary comparison paragraph
- compare random-gap coherent results against the earlier fixed-gap coherent trend
- compare random-gap non-coherent results against the earlier fixed-gap non-coherent trend

## Interpretation Rules

### If coherent random-gap RMSE stays close to fixed-gap expectations
Conclusion:
- the model is not merely exploiting the discrete evaluation grid
- it is learning a more continuous low-gap structure

### If coherent random-gap RMSE is much worse than fixed-gap expectations
Conclusion:
- the model may still be too tuned to the fixed-gap training/evaluation regime
- future dataset design should include more continuous random-gap support explicitly

### If non-coherent random-gap remains clearly easier than coherent random-gap
Conclusion:
- the earlier phase interpretation still holds under continuous gap sampling

### If coherent and non-coherent random-gap results become unexpectedly similar
Conclusion:
- investigate the realized gap distribution carefully first
- then re-check whether the random dataset generation is making the two families more alike than intended

## Runtime Metric
Use the same runtime style as the recent phases:
- end-to-end preprocessing plus learned inference path
- average runtime per sample

If convenient, also report:
- dataset-pass runtime

## Canonical Command
Recommended command:
```bash
python run_phase7h_groupb_1p9_random_gap_generalization.py
```

## Go / No-Go Rule
Treat the Phase `7G` model as more practically deployment-ready only if:
- it remains stable under random-gap evaluation
- low-SNR coherent random-gap performance is still strong enough to match the phase trend expectations
- and the results do not suggest a severe dependence on the fixed-gap grid structure

Otherwise:
- keep the current model as a strong fixed-gap / boundary-aware research model
- and plan a future training phase with explicitly continuous random-gap sampling
