# Phase 7F Group B 1.9 Lambda Mixed-Condition Fine-Tuning Experiment Plan

## Goal
Train a more practically deployable Group B `1.9 lambda` learned model by fine-tuning the current strongest Phase `7D` checkpoint on a broader mixed-condition dataset instead of a single hard-cell dataset.

Target model family:
- `SS(2/3 x 3) -> LRMC -> width-controlled anti-rectifier spatial fusion -> SubspaceNet(3x3) -> ESPRIT`

This phase is meant to improve generalization while preserving the very strong hard-cell capability already achieved in Phase `7D`.

## Primary Question
Can the current best hard-cell specialist be turned into a broader Group B model by fine-tuning on a mixed coherent / non-coherent dataset with controlled gap and SNR coverage, without losing too much performance in the original hardest coherent corner?

## Why This Phase Matters
The current evidence is:
- Phase `7D` produced the best single hard-cell result so far
- Phase `7E` showed that this model is a strong hard-cell specialist, but not yet a broadly transferable Group B default

So the next justified step is not another single-cell architectural tweak.

It is a dataset-design and training-distribution step:
- broaden coverage
- keep hard cases well represented
- start from the strongest existing checkpoint

## Model Initialization
Use the already trained best Phase `7D` checkpoint as initialization.

Do not train from scratch in the first Phase `7F` attempt.

Reason:
- the current Phase `7D` weights already encode a very strong solution for the hardest coherent corner
- the new training objective is an expansion of regime coverage, not a different task family
- fine-tuning is the most efficient way to preserve hard-cell skill while improving broader robustness

## Training Budget
Current empirical reference:
- `45,000` samples take a little over `1` hour of training in the present setup

Budget constraint:
- total training time should stay within about `9` hours

Recommended upper-bound dataset size:
- `360,000` total samples

Recommended split:
- `train_test_ratio = 0.2`

So:
- training portion: about `288,000`
- test portion: about `72,000`

This is the recommended first large mixed-condition run because it stays close to the available wall-clock budget while meaningfully expanding coverage.

## Fixed Conditions
Keep fixed:
- geometry: Group B 12-channel 2D hardware geometry
- physical spacing: `1.9 lambda`
- snapshots: `T = 40`
- learned head: ESPRIT
- fusion design: width-controlled anti-rectifier spatial fusion
- backbone kernel: `3x3`
- `tau = 8`
- same LRMC pipeline already used in Phase `7D`

## Dataset Philosophy
Do not use a purely random dataset.

Instead, use a mixed dataset with:
- explicit stratified coverage of important gap / SNR / coherence cells
- additional weighted random samples to improve interpolation and deployment realism
- deliberate over-representation of the hard coherent low-gap / low-SNR region

Reason:
- purely random angle generation underproduces the most important small-gap cases
- easy wide-gap examples would dominate loss and weaken the model exactly where robustness matters most

## Coherence Split
Use:
- `60%` coherent
- `40%` non-coherent

Reason:
- coherent cases remain the more important and structurally harder deployment target
- non-coherent coverage is still necessary because Phase `7E` showed coherence-type shift is a real transfer boundary

## Recommended Dataset Structure
Use a hybrid dataset with two components:

1. stratified grid component
2. weighted random component

Recommended totals:
- stratified grid component: `240,000`
- weighted random component: `120,000`
- total: `360,000`

## Component 1: Stratified Grid Coverage
Build an explicit grid over:
- coherence: coherent, non-coherent
- SNR: `1, 5, 10, 15 dB`
- fixed gap: `1, 2, 3, 4, 5 deg`

That produces:
- `2 x 4 x 5 = 40` condition cells

Distribute the `240,000` stratified samples using the required `60/40` coherence split.

### Coherent stratified allocation
Coherent share:
- `60%` of `240,000` = `144,000`

Coherent cells:
- `20`

So coherent stratified allocation:
- `7,200` samples per coherent cell

### Non-coherent stratified allocation
Non-coherent share:
- `40%` of `240,000` = `96,000`

Non-coherent cells:
- `20`

So non-coherent stratified allocation:
- `4,800` samples per non-coherent cell

This guarantees direct coverage of every important deployment cell while respecting your coherence weighting.

## Component 2: Weighted Random Coverage
Use the remaining `120,000` samples as weighted random cases drawn over the same overall field of view and SNR support.

This component is meant to:
- avoid overfitting to only fixed grid points
- provide interpolation behavior between grid cells
- keep hard regions emphasized

Apply the same coherence split:
- coherent random samples: `72,000`
- non-coherent random samples: `48,000`

### Random gap weighting
Recommended gap weighting:
- `50%` from `1 - 2 deg`
- `30%` from `3 deg`
- `20%` from `4 - 5 deg`

Interpretation:
- the hard low-gap region gets the most weight
- mid-gap still gets meaningful support
- easier wide-gap cells are present but not allowed to dominate

### Random SNR weighting
Recommended SNR weighting:
- `35%` at `1 dB`
- `30%` at `5 dB`
- `20%` at `10 dB`
- `15%` at `15 dB`

Interpretation:
- low-SNR cases remain emphasized
- moderate and easier SNR levels are still represented for deployment coverage

## Exact Recommended Sample Count Summary

### Stratified component
- coherent: `20` cells x `7,200` = `144,000`
- non-coherent: `20` cells x `4,800` = `96,000`
- subtotal: `240,000`

### Weighted random component
- coherent random: `72,000`
- non-coherent random: `48,000`
- subtotal: `120,000`

### Grand total
- `360,000`

## Training Strategy
Use fine-tuning, not fresh training.

### Recommended initialization
- load best Phase `7D` checkpoint

### Recommended learning rate
Lower the learning rate relative to the original Phase `7D` run.

Recommended first attempt:
- fine-tuning learning rate between `2e-6` and `5e-6`

Preferred starting point:
- `5e-6`

Reason:
- large enough to adapt to the broader mixed distribution
- small enough to reduce catastrophic forgetting of the original hard coherent skill

### Recommended first-pass duration
Do not assume the very first run must use the full original epoch count.

Recommended first fine-tuning pass:
- about `40 - 60` epochs

Reason:
- enough to test whether broader robustness improves
- short enough to avoid wasting time if hard-cell forgetting appears early

## Retention Requirement
The original coherent hard cell must remain a protected metric throughout training.

Always monitor:
- coherent `gap = 1 deg`, `SNR = 1 dB`
- coherent `gap = 2 deg`, `SNR = 1/5 dB`
- non-coherent `gap = 1 deg`, `SNR = 1 dB`

Reason:
- these cells best expose whether the model is retaining the hard coherent skill while gaining broader coverage

## Evaluation Plan
After training, evaluate using:
- the same Phase `7E` coherent fixed-gap / SNR grid
- the same Phase `7E` non-coherent fixed-gap / SNR grid

That means:
- `20` coherent reused cells
- `20` non-coherent reused cells

This keeps the generalization comparison directly aligned with the existing transfer study.

## Main Hypotheses
1. Fine-tuning from Phase `7D` will retain much more of the hard coherent skill than training a broad mixed dataset from scratch.
2. The mixed-condition dataset should improve broad coherent and non-coherent coverage relative to the zero-shot transfer behavior seen in Phase `7E`.
3. The largest gains should appear in cells that are near the hard boundary but not identical to the source cell:
   - coherent `1 - 2 deg`
   - low to moderate SNR
4. If the model becomes broadly better but the source hard cell degrades too much, the dataset is too easy-dominated or the fine-tuning rate is too aggressive.

## Baselines For Comparison
The most important baselines are:

1. Phase `7D` hard-cell specialist
- best single-cell coherent model

2. Phase `7E` zero-shot transfer result
- same architecture, no mixed-condition retraining

3. Direct per-cell learned references
- where available from earlier phase results

4. Phase 6 classical best controls
- on each reused evaluation cell

## Success Criteria

### Minimal success
Compared with Phase `7E`, the fine-tuned model improves broad reused-grid performance while keeping the original coherent `1 deg`, `1 dB` cell near its current accuracy.

### Strong success
The fine-tuned model:
- preserves the source hard-cell performance within a small margin
- improves coherent OOD mean RMSE substantially relative to Phase `7E`
- improves non-coherent transfer substantially relative to Phase `7E`
- remains competitive with classical controls and direct learned references across a much larger portion of the reused grid

### Informative negative result
If broad-grid performance improves but the source hard cell degrades badly, that is still useful evidence that:
- the dataset broadening strategy is working
- but the current weighting or fine-tuning aggressiveness is too high for hard-case retention

### No-go result
If the model loses hard-cell performance and still fails to improve broad transfer enough, then:
- the proposed weighting is not yet effective
- and the next change should be dataset weighting or training schedule, not another architecture change

## Metrics
Primary metric:
- horizontal-angle RMSE in degrees

Secondary metrics:
- source-cell RMSE retention
- coherent OOD mean RMSE
- non-coherent transfer mean RMSE
- delta vs Phase `7E` on each reused cell
- delta vs Phase 6 classical best on each reused cell
- delta vs direct per-cell learned references where available
- average runtime per sample

## Runtime Metric
Record runtime in the same style as Phase `7E`:
- end-to-end preprocessing plus learned inference path
- average runtime per sample
- average dataset-pass runtime if convenient

Reason:
- the main expected change is accuracy/generalization
- runtime should be checked to confirm the broader model does not introduce an unexpected deployment cost

## Interpretation Rules

### If broad transfer improves and hard-cell retention stays strong
Conclusion:
- mixed-condition fine-tuning is the correct next direction
- the model is moving from specialist toward deployable default

### If broad transfer improves but hard-cell retention weakens
Conclusion:
- the general idea is correct
- but weighting, curriculum, or LR must be adjusted to protect the hardest coherent corner

### If coherent transfer improves much more than non-coherent transfer
Conclusion:
- the current `60/40` split still favors coherent specialization strongly
- a later follow-up can increase non-coherent weight if deployment requires it

### If non-coherent transfer improves while coherent hard-cell retention collapses
Conclusion:
- the mixed dataset has become too broad or too easy-dominated
- the coherent hard corner needs stronger sampling or lower fine-tuning rate

## Recommended Outputs
Create a new family:
- `results/phase7f_groupb_1p9_mixed_condition_finetune/`

Recommended markdown:
- `phase7f_groupb_1p9_mixed_condition_finetune_results.md`

Recommended `summary.csv`:
- one row per evaluation cell on the reused Phase `7E` grid

The results markdown should include:
- source-cell retention table
- coherent reused-grid table
- non-coherent reused-grid table
- bucket summary table
- comparison vs Phase `7E`

## Canonical Launcher
Recommended launcher:
- `run_phase7f_groupb_1p9_mixed_condition_finetune.py`

Recommended command:
```bash
python run_phase7f_groupb_1p9_mixed_condition_finetune.py
```

## Go / No-Go Rule
Promote the Phase `7F` model as the new broader Group B default only if:
- source hard-cell performance remains close to the current Phase `7D` best result
- coherent OOD transfer clearly improves over Phase `7E`
- non-coherent transfer also improves meaningfully over Phase `7E`

Otherwise:
- keep Phase `7D` as the best hard-cell specialist
- and treat Phase `7F` as the first dataset-broadening step rather than the final deployable model
