# Phase 7J Group B 1.9 Lambda Random-Gap Architecture Comparison Experiment Plan

## Goal
Measure how much the current best learned architecture has improved over the original SubspaceNet baseline from the early project stage when both are trained from scratch on the same random-gap dataset.

This phase is meant to answer a specific paper-level question:
- how much improvement comes from the newer architecture itself
- compared with the original `2x2` SubspaceNet design
- when both models are trained fairly under the same continuous random-gap regime

## Primary Comparison
Compare these three models.

The comparison should separate:
- the original single-row no-SS learned baseline
- the original Group B `SS -> LRMC -> SubspaceNet(2x2)` learned baseline
- the current best learned architecture

### Model A: original SubspaceNet baseline
- `SS(3/3) -> LRMC -> SubspaceNet(backbone 2x2) -> ESPRIT`

This is the historical baseline representing the original project-era learned pipeline.

### Model B: current best architecture
- `SS(2/3 x 3) -> LRMC -> width-controlled anti-rectifier spatial fusion -> SubspaceNet(backbone 3x3) -> ESPRIT`

This is the current strongest learned architecture from the recent Phase `7D` to `7G` line.

### Model C: original no-SS single-row SubspaceNet baseline
- `single-row linear-array covariance -> SubspaceNet(backbone 2x2) -> ESPRIT`

Important meaning:
- no spatial smoothing
- no learned SS-fusion
- no 2D multi-row preprocessing path
- input is built from a single-row linear array rather than the full 2D hardware array reduction path

This model is meant to act as the earliest-style original SubspaceNet control.

## Core Principle
This phase is a fair from-scratch architecture comparison.

So:
- do not fine-tune from older checkpoints
- initialize all three models from scratch
- train all three for the same number of epochs
- use the same random-gap training distribution
- use the same evaluation sets

## Main Question
When all three models are trained from scratch for `80` epochs on the same random-gap dataset, how much does the current best architecture outperform:
- the original no-SS single-row `2x2` SubspaceNet baseline
- the original `SS(3/3) -> LRMC -> SubspaceNet(2x2)` baseline

in:
- random-gap generalization
- fixed-gap retention
- coherent hard-cell behavior

## Why This Phase Matters
The project already showed that:
- the `3x3` backbone helps
- anti-rectifier fusion helps
- targeted mixed-condition training helps
- random-gap training helps somewhat, but can also damage fixed-gap hard-cell skill if pushed too far

What is still missing is a clean answer to this simpler question:
- if we take:
  - the original single-row no-SS baseline
  - the original Group B `SS -> LRMC -> SubspaceNet(2x2)` baseline
  - the current best architecture
- train all of them from scratch on the same random-gap regime
- how much improvement comes from:
  - adding the Group B preprocessing path
  - architectural upgrades inside the learned model
  - or both together

That is the most direct way to quantify true model-progress relative to the original SubspaceNet design.

## Scope
This phase should compare architecture, not training-history effects.

Change:
- architecture

Hold fixed:
- geometry
- array spacing
- snapshots
- training distribution
- train/test split logic
- epoch count
- evaluation protocol

## Fixed Conditions
Keep fixed for all three models whenever they are conceptually shared:
- geometry: Group B 12-channel 2D hardware geometry
- physical spacing: `1.9 lambda`
- snapshots: `T = 40`
- azimuth range: `[-15 deg, 15 deg]`
- SNR support: `1, 5, 10, 15 dB`
- coherence split: `60% coherent`, `40% non-coherent`
- random-gap rule: continuous gaps with `min_doa_gap = 1 deg`
- learned head: ESPRIT
- training epochs: `80`

## Training Regime
Train all three models from scratch.

Do not initialize from:
- Phase `7D`
- Phase `7F`
- Phase `7G`
- or any other existing checkpoint

Reason:
- the user wants the architecture improvement relative to the original model, not the effect of fine-tuning history

## Dataset Philosophy
Use one shared random-gap training distribution family for all three models.

This should be the same dataset family, not separately sampled independent families for the three models.

Reason:
- if the random-gap samples differ between models, architecture comparison becomes noisy
- all three models should see the same training and evaluation data whenever practical

Important caveat for Model C:
- Model C does not consume the same intermediate tensor representation as Models A and B
- but it should still be generated from the same underlying source-angle, SNR, coherence, and snapshot realizations whenever practical

So the fairness rule should be:
- shared underlying stochastic dataset realizations
- model-specific input conversion allowed

## Recommended Training Dataset
Use a hybrid random-gap-focused dataset with:
- explicit continuous random-gap support
- but still enough low-gap density to keep the task meaningful

Recommended total dataset size:
- `45,000` samples

Recommended split:
- `90%` train
- `10%` test

So the default split is:
- `40,500` train
- `4,500` test

This phase intentionally uses a modest shared dataset rather than a very large one.

Reason:
- the main goal is to compare the relative improvement among the three models
- not to push any single model to its absolute best possible final accuracy

## Training Simplicity Rule
Do not use phased or staged training in this phase.

Train each model in one uninterrupted run:
- one shared `45,000`-sample dataset
- one `9:1` train:test split
- `80` epochs
- from scratch

Reason:
- this keeps the comparison simple and controlled
- and avoids making training schedule another confounding factor

## Structured Portion
The structured component should protect the known hard regimes.

Recommended coherent structured weighting:
- `1 deg`: `25%`
- `2 deg`: `35%`
- `3 deg`: `20%`
- `4 deg`: `10%`
- `5 deg`: `10%`

Recommended non-coherent structured weighting:
- `1 deg`: `25%`
- `2 deg`: `30%`
- `3 deg`: `20%`
- `4 deg`: `15%`
- `5 deg`: `10%`

Within each gap:
- distribute evenly across `1, 5, 10, 15 dB`

## Random-Gap Portion
Use continuous random-gap sampling inside `[-15 deg, 15 deg]` with:
- `min_doa_gap = 1 deg`

Recommended random-gap bins for sampling control:
- `1 - 2 deg`
- `2 - 3 deg`
- `3 - 5 deg`
- `5 - 10 deg`
- `10 - 29 deg`

### Coherent random-gap weights
- `1 - 2 deg`: `35%`
- `2 - 3 deg`: `25%`
- `3 - 5 deg`: `20%`
- `5 - 10 deg`: `10%`
- `10 - 29 deg`: `10%`

### Non-coherent random-gap weights
- `1 - 2 deg`: `30%`
- `2 - 3 deg`: `25%`
- `3 - 5 deg`: `20%`
- `5 - 10 deg`: `15%`
- `10 - 29 deg`: `10%`

### Shared SNR weighting
- `1 dB`: `35%`
- `5 dB`: `30%`
- `10 dB`: `20%`
- `15 dB`: `15%`

## Shared Dataset Recommendation
Recommended top-level mix inside the shared `45,000`-sample dataset:
- `50%` structured low-gap protection
- `50%` continuous random-gap samples

Interpretation:
- enough structure to keep the hard coherent `1 - 2 deg` regime visible
- enough continuous random-gap support to make the comparison relevant to Phase `7H` and `7I`

## Fairness Rules
To keep this comparison interpretable:

1. Use the same training data for all three models
- same shared dataset
- same train/validation splits
- same seeds when practical

For Model C:
- allow a model-specific conversion from the shared underlying dataset into the single-row linear-array input representation
- but do not resample a different random dataset just for Model C

2. Use the same optimizer family and general schedule
- unless one model literally cannot train under it

3. Use the same total epoch count
- `80` epochs for all three models in one uninterrupted run

4. Use the same evaluation sets
- fixed-gap reused grid
- random-gap evaluation family

5. Do not tune one architecture much more aggressively than the others
- the point is fair comparison, not separate best-possible leaderboard chasing

## Training Hyperparameters
Recommended default:
- optimizer and scheduler: same as the current stable SubspaceNet training path in the repo
- batch size: same family for all three models
- total epochs: `80`
- validation cadence: at least once per epoch

Because all three models train from scratch, this phase should use the same initialization style and same training-control logic wherever the architectures allow.

## Checkpoint Policy
For each model:
- save normal training checkpoints
- save best-validation checkpoint overall
- report the final selected checkpoint used for evaluation

Recommended selection rule:
- evaluate using the best-validation checkpoint from the single `80`-epoch run

Reason:
- this avoids forcing one model to be judged by a weaker late-epoch checkpoint if mild overtraining appears

## Protected Monitoring Cells
Track the same protected cells for all three architectures:

### Hard coherent anchor
- coherent `gap = 1 deg`, `SNR = 1 dB`

### Coherent boundary cells
- coherent `gap = 2 deg`, `SNR = 1, 5, 10, 15 dB`

### Broad fixed-gap checks
- coherent `gap = 3 deg`, `SNR = 5 dB`
- non-coherent `gap = 1 deg`, `SNR = 1 dB`
- non-coherent `gap = 2 deg`, `SNR = 5 dB`

### Random-gap deployment checks
- coherent random-gap, `1, 5, 10, 15 dB`
- non-coherent random-gap, `1, 5, 10, 15 dB`

## Evaluation Set
Evaluate all three models on the same two families.

### Fixed-gap evaluation
Reuse the standard 40-cell grid:
- `20` coherent cells
- `20` non-coherent cells

### Random-gap evaluation
Reuse the 8 random-gap Phase `7H` / `7I` datasets:
- coherent random-gap at `1, 5, 10, 15 dB`
- non-coherent random-gap at `1, 5, 10, 15 dB`

Reason:
- this gives one direct architecture comparison for both structured and deployment-style regimes

## Main Hypotheses
1. The current best architecture should outperform the original `2x2` SubspaceNet baseline on the coherent hard low-gap regimes.
2. The current best architecture should also outperform the original no-SS single-row baseline on random-gap evaluation, especially in coherent low-SNR settings.
3. If Model A already beats Model C clearly, that means the Group B `SS -> LRMC` preprocessing path is itself a major source of the improvement.
4. If Model B then also beats Model A clearly, that is strong evidence that the newer architecture itself is materially better rather than only benefiting from preprocessing.
5. If the Model B versus Model A gap becomes small, then much of the recent project gain came from training-distribution design and preprocessing rather than architecture alone.

## Baselines For Interpretation
The key comparison is internal:
- Model C versus Model A
- Model A versus Model B
- Model C versus Model B

Secondary interpretation references:
- Phase `7D` hard-cell result
- Phase `7G` fixed-gap boundary-repair result
- Phase `7I` random-gap training result

But these are context only.

The primary paper-facing comparison should be:
- original no-SS single-row `2x2` SubspaceNet baseline trained from scratch on random-gap data
- original Group B `SS -> LRMC -> SubspaceNet(2x2)` baseline trained from scratch on the same random-gap data
- current best architecture trained from scratch on the same random-gap data

## Success Criteria

### Minimal success
The current best architecture clearly beats at least both older baselines on random-gap evaluation while remaining at least competitive on fixed-gap protected cells.

### Strong success
The current best architecture beats both older baselines on:
- coherent random-gap evaluation
- non-coherent random-gap evaluation
- coherent `1 deg` anchor
- coherent `2 deg` boundary mean

### Informative negative result
If the current best architecture improves only slightly over Model A, that suggests the recent gains came more from data curriculum and checkpoint history than from architecture alone.

### Surprising result
If the original no-SS or original `SS -> LRMC` `2x2` baseline trains unexpectedly well under the shared random-gap regime and closes most of the gap, that would mean the architecture advantage is smaller than the recent phase-by-phase history suggests.

## Metrics
Primary metrics:
- coherent random-gap mean RMSE
- non-coherent random-gap mean RMSE
- overall random-gap mean RMSE
- coherent `1 deg`, `1 dB` anchor RMSE
- coherent `2 deg` boundary mean RMSE

Secondary metrics:
- coherent OOD mean RMSE on the fixed-gap grid
- non-coherent transfer mean RMSE on the fixed-gap grid
- per-cell fixed-gap RMSE
- per-cell random-gap RMSE
- average runtime per sample

## Recommended Result Tables
At minimum, report:

1. architecture overview table
- model name
- input path
- backbone
- fusion type
- training mode
- total epochs

2. random-gap comparison table
- coherence type
- SNR
- Model C RMSE
- original `2x2` baseline RMSE
- current best architecture RMSE
- delta `A - C`
- delta `B - A`
- delta `B - C`

3. coherent `2 deg` boundary table
- SNR
- Model C RMSE
- original `2x2` baseline RMSE
- current best architecture RMSE
- delta `A - C`
- delta `B - A`
- delta `B - C`

4. source-cell anchor table
- coherent `1 deg`, `1 dB`
- Model C
- original `2x2` baseline
- current best architecture

5. summary bucket table
- in_domain_anchor
- coherent_2deg_boundary
- coherent_ood
- noncoherent_transfer
- coherent_random_gap
- noncoherent_random_gap

6. optional stage table
- model
- best validation RMSE
- selected checkpoint

## Interpretation Rules

### If the current best architecture wins broadly
Conclusion:
- the project has achieved a real architecture-level improvement over the original SubspaceNet design

### If Model A beats Model C clearly but Model B only slightly beats Model A
Conclusion:
- most of the gain comes from the Group B `SS -> LRMC` preprocessing and hardware-aware pipeline
- the newer architecture adds a smaller incremental gain on top

### If Model B beats both Model C and Model A clearly
Conclusion:
- the project has improved both the preprocessing path and the learned architecture itself

### If the current best architecture wins mainly on low-gap coherent cells
Conclusion:
- the newer architecture is especially better at the hard regime the project has been targeting

### If random-gap results are similar but fixed-gap hard-cell results differ strongly
Conclusion:
- the newer architecture is mainly a hard-boundary specialist advantage rather than a general continuous-gap improvement

### If one of the older baselines closes most of the gap
Conclusion:
- recent gains are driven more by better training distribution and staging than by architecture alone

## Recommended Outputs
Create a new family:
- `results/phase7j_groupb_1p9_randomgap_architecture_comparison/`

Recommended markdown:
- `phase7j_groupb_1p9_randomgap_architecture_comparison_results.md`

Recommended `summary.csv`:
- one row per evaluation cell per model

## Canonical Launcher
Recommended launcher:
- `run_phase7j_groupb_1p9_randomgap_architecture_comparison.py`

Recommended command:
```bash
python run_phase7j_groupb_1p9_randomgap_architecture_comparison.py
```

## Go / No-Go Rule
Claim a meaningful architecture improvement over the original SubspaceNet only if the current best model clearly beats the original `2x2` baseline under this fair from-scratch random-gap comparison.

For the three-model version, the preferred paper interpretation is:
- `C -> A` measures the gain from moving from the original single-row no-SS setup to the Group B `SS -> LRMC` learned pipeline
- `A -> B` measures the gain from the newer architecture on top of that pipeline
- `C -> B` measures the total end-to-end project improvement

This phase should be interpreted mainly as:
- a controlled relative-comparison study
- not a final best-accuracy training recipe

Otherwise:
- conclude that architecture progress is smaller than expected
- and treat training-distribution design as the dominant source of recent gains
