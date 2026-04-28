# Phase 7I Group B 1.9 Lambda Random-Gap Training Experiment Plan

## Goal
Train a new version of the current best boundary-aware model so it generalizes to:
- continuous random angular separations inside `[-15 deg, 15 deg]`
- SNR values `1, 5, 10, 15 dB`
- both coherent and non-coherent signals

while preserving as much as possible of the fixed-gap and `2 deg` boundary performance already achieved in Phase `7G`.

Target model family:
- `SS(2/3 x 3) -> LRMC -> width-controlled anti-rectifier spatial fusion -> SubspaceNet(3x3) -> ESPRIT`

This phase is a training-distribution expansion step, not a new architecture search.

## Primary Question
Can the Phase `7G` model be turned from a strong fixed-gap / boundary-aware specialist into a more deployment-ready model by adding explicit random-gap training support, without losing too much of:
- the coherent `1 deg`, `1 dB` anchor
- the coherent `2 deg` boundary repair
- the broad fixed-gap gains already obtained in Phases `7F` and `7G`

## Why This Phase Matters
Phase `7H` showed that the current Phase `7G` model transfers poorly to random-gap evaluation:
- coherent random-gap mean RMSE was about `5.6449 deg`
- non-coherent random-gap mean RMSE was about `5.0906 deg`

That failure is too large to ignore if practical deployment is expected to involve continuous source separations rather than only the fixed `1, 2, 3, 4, 5 deg` grid.

At the same time, Phase `7G` is still valuable because it already solved two important problems:
- strong coherent hard-cell performance
- targeted `2 deg` boundary repair

So the next step should be:
- keep the Phase `7G` model family
- initialize from the best Phase `7G` checkpoint
- expand the training distribution to include explicit random-gap support

## Working Hypothesis
The poor Phase `7H` result is mainly a distribution-support problem.

The current model was trained mostly on:
- fixed-gap cells
- low-gap boundary-aware distributions

So it is not surprising that it performs poorly when evaluated on continuous random gaps with very different realized gap statistics.

The correct next intervention is therefore:
- mixed structured + random-gap fine-tuning

not:
- replacing the architecture
- or abandoning fixed-gap supervision entirely

## Model Initialization
Use the best Phase `7G` checkpoint as initialization.

Do not restart from:
- random initialization
- Phase `7D`
- or Phase `7F`

Reason:
- Phase `7G` currently has the best combination of hard-cell skill and coherent `2 deg` boundary repair
- Phase `7I` should broaden that model, not rebuild it from scratch

## Scope
This phase should change only:
- training data distribution
- dataset composition
- fine-tuning schedule

Do not change:
- geometry
- SS and LRMC preprocessing path
- anti-rectifier fusion design
- SubspaceNet backbone
- differentiable ESPRIT head

## Fixed Conditions
Keep fixed:
- geometry: Group B 12-channel 2D hardware geometry
- physical spacing: `1.9 lambda`
- snapshots: `T = 40`
- azimuth range: `[-15 deg, 15 deg]`
- learned head: ESPRIT
- fusion design: width-controlled anti-rectifier spatial fusion
- backbone kernel: `3x3`
- `tau = 8`
- same canonical learned preprocessing path as Phases `7D` to `7H`

## Training Budget
Keep the same practical training-time envelope used in the recent mixed-condition phases.

Recommended total effective exposure:
- about `360,000` samples

Important practical note:
- this should be interpreted as total exposure across stages
- it does not mean loading one monolithic `360,000`-sample dataset into memory at once

Reason:
- earlier runs already showed that very large dataset loading can freeze the system
- the training plan therefore needs staged data exposure rather than one giant in-memory training set

Recommended split per stage:
- `80%` train
- `20%` held-out validation / test according to the repo’s usual convention

## Dataset Philosophy
Do not switch to a purely random-gap dataset.

Do not keep a purely fixed-gap dataset either.

Use a hybrid dataset with three components:
1. protected structured fixed-gap component
2. boundary-focused low-gap component
3. continuous random-gap component

This is the key Phase `7I` design choice.

## Required Practical Constraint
Because the system previously froze when loading a huge dataset, Phase `7I` should be run as staged fine-tuning.

That means:
- do not build one giant training dataset and keep all of it resident in memory
- do not require the loader to materialize the full `360,000` samples simultaneously
- instead, split training into smaller phases or chunks and continue fine-tuning across them

Acceptable implementation styles:
- multiple sequential training stages with different dataset files
- chunked cached datasets loaded one stage at a time
- streaming / iterable loading if the current codebase supports it cleanly

The simplest and safest recommendation is:
- staged fine-tuning with multiple medium-size datasets

## Recommended Coherence Split
Keep the same high-level coherence emphasis used in Phases `7F` and `7G`:
- `60%` coherent
- `40%` non-coherent

Reason:
- coherent low-gap behavior is still the dominant difficulty
- keeping the same split reduces interpretation confounds

## Recommended Top-Level Dataset Mix
Recommended total dataset composition across all stages:
- `55%` structured fixed-gap / boundary-aware data
- `45%` random-gap data

For about `360,000` total effective samples, that means:
- about `198,000` structured samples
- about `162,000` random-gap samples

Reason:
- the model still needs explicit protection on the fixed hard cells
- but nearly half the training mass should now teach continuous-gap behavior directly

## Staged Training Design
Recommended total exposure:
- about `360,000` samples

Recommended staged layout:
- `3` stages
- about `120,000` samples per stage

Reason:
- `120,000` is large enough to be meaningful
- but much safer than one monolithic `360,000` dataset load
- it also lets us control curriculum and monitor forgetting between stages

### Recommended stage logic
Stage 1:
- structured-heavy adaptation
- stabilize from Phase `7G` initialization
- preserve anchor and `2 deg` boundary skill while introducing a small amount of random-gap data

Stage 2:
- balanced mixed training
- strongest joint exposure to structured and random-gap data

Stage 3:
- random-gap consolidation with fixed-gap protection
- improve deployment-style transfer while keeping protected structured support active

### Recommended stage sizes
Practical default:
- Stage 1: `120,000`
- Stage 2: `120,000`
- Stage 3: `120,000`

This keeps the total near:
- `360,000`

### Recommended per-stage mix
Stage 1:
- `70%` structured
- `30%` random-gap

Stage 2:
- `55%` structured
- `45%` random-gap

Stage 3:
- `40%` structured
- `60%` random-gap

Interpretation:
- Stage 1 protects the existing Phase `7G` specialization
- Stage 2 becomes the main mixed-regime learning phase
- Stage 3 pushes random-gap robustness without fully removing structured anchor support

### Optional safer fallback
If `120,000` samples per stage still feels risky on this machine, use:
- `4` stages of about `90,000` samples each

with the same overall structured-to-random progression.

This is preferable to risking another full-system freeze.

## Structured Component
The structured component should follow the same general logic as Phase `7G`, because Phase `7G` already fixed the coherent `2 deg` weakness.

Structured component total across all stages:
- about `198,000`

### Structured coherent weighting
Within the coherent structured subset, keep boundary emphasis:
- `1 deg`: `25%`
- `2 deg`: `40%`
- `3 deg`: `20%`
- `4 deg`: `10%`
- `5 deg`: `5%`

Within each gap, distribute evenly across:
- `1, 5, 10, 15 dB`

### Structured non-coherent weighting
Within the non-coherent structured subset:
- `1 deg`: `30%`
- `2 deg`: `30%`
- `3 deg`: `20%`
- `4 deg`: `10%`
- `5 deg`: `10%`

Within each gap, distribute evenly across:
- `1, 5, 10, 15 dB`

## Random-Gap Component
The new ingredient in Phase `7I` is the explicit random-gap component.

Random-gap component total across all stages:
- about `162,000`

### Random-gap sampling rules
Use:
- azimuth range `[-15 deg, 15 deg]`
- no fixed-gap constraint
- `min_doa_gap = 1 deg`

But do not sample random gaps uniformly over all valid separations.

Instead, use a low-gap-biased continuous distribution so the model sees:
- many hard and boundary cases
- but also meaningful medium and wide separations

### Recommended random-gap binning for sampling control
To implement a continuous but controllable distribution, define random-gap bins:
- `1 - 2 deg`
- `2 - 3 deg`
- `3 - 5 deg`
- `5 - 10 deg`
- `10 - 29 deg`

Inside each selected bin:
- sample the actual gap continuously at random
- then sample source locations inside `[-15 deg, 15 deg]` subject to that gap

### Recommended coherent random-gap weights
Within the coherent random-gap subset:
- `1 - 2 deg`: `35%`
- `2 - 3 deg`: `25%`
- `3 - 5 deg`: `20%`
- `5 - 10 deg`: `10%`
- `10 - 29 deg`: `10%`

Reason:
- the model must learn continuous behavior near the critical boundary
- but should not become blind to medium and large separations

### Recommended non-coherent random-gap weights
Within the non-coherent random-gap subset:
- `1 - 2 deg`: `30%`
- `2 - 3 deg`: `25%`
- `3 - 5 deg`: `20%`
- `5 - 10 deg`: `15%`
- `10 - 29 deg`: `10%`

Reason:
- keep the same general shape
- but slightly reduce the extreme low-gap concentration relative to coherent data

### Shared SNR weighting
Use the same SNR bias as the recent hard-case-aware phases:
- `1 dB`: `35%`
- `5 dB`: `30%`
- `10 dB`: `20%`
- `15 dB`: `15%`

This keeps low-SNR support strong while still covering the deployment range.

## Practical Simplification Rule
If implementing fully continuous weighted random-gap sampling is cumbersome, the minimum acceptable simplification is:
- generate random-gap samples by bin
- control the number of samples per bin explicitly
- sample the actual gap uniformly inside each chosen bin

The important point is:
- random-gap support must be continuous
- but it must still be biased toward the low-gap boundary

## Training Strategy
Use fine-tuning from Phase `7G`.

### Learning rate
Use a small continuation-learning rate.

Recommended range:
- `2e-6` to `5e-6`

Preferred starting point:
- `3e-6`

Reason:
- the model already contains useful boundary structure
- Phase `7I` is broadening, not rebuilding
- too large a rate risks erasing the Phase `7G` gains

### Duration
Recommended first pass:
- `10 - 20` epochs per stage

Reason:
- enough to adapt at each stage
- safer than one long uninterrupted run on a massive mixed dataset
- allows monitoring after each stage before proceeding

Recommended total:
- about `30 - 50` epochs across all stages

## Stage Transition Rule
After each stage:
- save a checkpoint
- evaluate on the protected monitoring cells
- evaluate on at least a small random-gap validation subset

Proceed to the next stage only if:
- anchor degradation is acceptable
- coherent `2 deg` protection remains acceptable
- and random-gap validation is not clearly collapsing

If a stage causes obvious forgetting:
- reduce the next stage learning rate
- increase the structured share in the next stage
- or stop early and keep the best earlier checkpoint

This staged checkpointing rule is part of the recommended plan, not an optional afterthought.

## Protected Monitoring Cells
The following conditions should be monitored explicitly during training.

### Hard anchor protection
- coherent `gap = 1 deg`, `SNR = 1 dB`

### Boundary protection
- coherent `gap = 2 deg`, `SNR = 1 dB`
- coherent `gap = 2 deg`, `SNR = 5 dB`
- coherent `gap = 2 deg`, `SNR = 10 dB`
- coherent `gap = 2 deg`, `SNR = 15 dB`

### Broad fixed-gap retention checks
- coherent `gap = 3 deg`, `SNR = 5 dB`
- non-coherent `gap = 1 deg`, `SNR = 1 dB`
- non-coherent `gap = 2 deg`, `SNR = 5 dB`

### Random-gap deployment checks
- coherent random-gap, `1 dB`
- coherent random-gap, `5 dB`
- coherent random-gap, `10 dB`
- coherent random-gap, `15 dB`
- non-coherent random-gap, `1 dB`
- non-coherent random-gap, `5 dB`
- non-coherent random-gap, `10 dB`
- non-coherent random-gap, `15 dB`

## Evaluation Set
Evaluate the trained Phase `7I` model on both:

1. the reused 40-cell fixed-gap grid from Phases `7E`, `7F`, and `7G`
- `20` coherent cells
- `20` non-coherent cells

2. the random-gap evaluation family from Phase `7H`
- coherent random-gap at `1, 5, 10, 15 dB`
- non-coherent random-gap at `1, 5, 10, 15 dB`

This is essential because Phase `7I` must be judged on both:
- fixed-gap retention
- random-gap improvement

## Main Hypotheses
1. Adding explicit random-gap training should reduce the severe Phase `7H` random-gap failure substantially.
2. Starting from Phase `7G` should preserve much of the existing `1 deg` and `2 deg` skill.
3. Some degradation on a few fixed-gap cells may be acceptable if random-gap performance improves dramatically.
4. If random-gap improves only slightly while fixed-gap performance worsens clearly, then the random-gap dataset mix is too aggressive or poorly targeted.

## Baselines For Comparison
The most important comparisons are:

1. Phase `7G`
- best current fixed-gap / boundary-aware model

2. Phase `7H`
- direct random-gap evaluation result of the unadapted Phase `7G` model

3. Phase `7F`
- best broad mixed-condition fixed-gap generalization baseline before boundary repair

4. Phase 6 classical best controls
- useful only as secondary context on the fixed-gap grid

## Success Criteria

### Minimal success
Random-gap RMSE improves clearly relative to Phase `7H`, while the coherent `1 deg`, `1 dB` anchor and coherent `2 deg` boundary remain usable.

### Strong success
Random-gap RMSE drops substantially for both coherent and non-coherent evaluation, and the model keeps most of the key Phase `7G` fixed-gap strengths.

### Informative negative result
If random-gap improves but fixed-gap boundary performance degrades too much, that still shows the direction is correct, but the random-gap share is too high or the fine-tuning is too aggressive.

### Practical failure mode
If training repeatedly becomes unstable or freezes because dataset loading is still too heavy, then:
- the staged design is still too coarse for the current machine
- and the next attempt should reduce per-stage dataset size further rather than reverting to monolithic loading

### No-go result
If random-gap remains poor even after explicit random-gap training, then:
- the current architecture or loss may still be too specialized to fixed-gap supervision
- or the random-gap data generation and conditioning strategy needs redesign

## Metrics
Primary metrics:
- horizontal-angle RMSE in degrees on the 40-cell fixed-gap grid
- horizontal-angle RMSE in degrees on the 8 random-gap evaluation cells

Secondary metrics:
- coherent random-gap mean RMSE
- non-coherent random-gap mean RMSE
- overall random-gap mean RMSE
- coherent `2 deg` mean RMSE across SNRs
- coherent `1 deg`, `1 dB` anchor retention
- delta vs Phase `7G`
- delta vs Phase `7H`
- average runtime per sample

## Recommended Result Tables
At minimum, report:

1. random-gap comparison table
- coherence type
- SNR
- Phase `7H` RMSE
- Phase `7I` RMSE
- delta

2. coherent `2 deg` protection table
- SNR
- Phase `7G` RMSE
- Phase `7I` RMSE
- delta

3. source-cell retention table
- coherent `1 deg`, `1 dB`
- Phase `7D`
- Phase `7F`
- Phase `7G`
- Phase `7I`

4. full coherent fixed-gap table
- same style as Phase `7F` / `7G`

5. full non-coherent fixed-gap table
- same style as Phase `7F` / `7G`

6. bucket summary table
- coherent_random_gap
- noncoherent_random_gap
- coherent_2deg_boundary
- coherent_ood
- noncoherent_transfer

## Interpretation Rules

### If random-gap improves strongly and fixed-gap retention stays solid
Conclusion:
- explicit random-gap training was the missing piece
- the model is moving toward a more deployment-ready mixed regime

### If random-gap improves strongly but coherent `2 deg` weakens notably
Conclusion:
- the direction is correct
- but the structured fixed-gap protection needs to be stronger

### If coherent random-gap improves but non-coherent random-gap stays weak
Conclusion:
- the random-gap training distribution still overemphasizes coherent structure
- more non-coherent random-gap support is needed

### If little changes on random-gap evaluation
Conclusion:
- random-gap failure is not solved just by adding random-gap samples
- future work may need curriculum design, loss shaping, or a different fusion/backbone training strategy

## Recommended Outputs
Create a new family:
- `results/phase7i_groupb_1p9_random_gap_training/`

Recommended markdown:
- `phase7i_groupb_1p9_random_gap_training_results.md`

Recommended `summary.csv`:
- one row per fixed-gap or random-gap evaluation cell

## Canonical Launcher
Recommended launcher:
- `run_phase7i_groupb_1p9_random_gap_training.py`

Recommended implementation note:
- the launcher should support stage-wise dataset selection or stage-wise template resolution
- so each training stage can load only its current chunk instead of the full training pool

Recommended command:
```bash
python run_phase7i_groupb_1p9_random_gap_training.py
```

## Go / No-Go Rule
Promote the Phase `7I` model over Phase `7G` only if:
- random-gap performance improves materially over Phase `7H`
- the coherent `1 deg`, `1 dB` anchor remains reasonably strong
- coherent `2 deg` boundary performance does not collapse
- and the fixed-gap broad coverage remains acceptable

Otherwise:
- keep Phase `7G` as the best fixed-gap / boundary-aware specialist
- and treat Phase `7I` as the first random-gap adaptation attempt rather than the new default
