# Phase 7G Group B 1.9 Lambda 2-Degree Boundary Repair Experiment Plan

## Goal
Repair the remaining `2 deg` boundary weakness observed after Phase `7F`, while preserving:
- the strong coherent `1 deg`, `1 dB` hard-cell capability
- the broad mixed-condition gains already achieved in Phase `7F`

Target model family:
- `SS(2/3 x 3) -> LRMC -> width-controlled anti-rectifier spatial fusion -> SubspaceNet(3x3) -> ESPRIT`

This phase is not a new architecture search.

It is a dataset-weighting and fine-tuning-distribution repair step.

## Primary Question
Can the current Phase `7F` broad-coverage model be improved specifically around the `2 deg` transition boundary by reweighting training toward `2 deg` coherent and nearby low-gap cells, without sacrificing:
- the original `1 deg`, `1 dB` coherent anchor too much
- the non-coherent generalization gains already obtained in Phase `7F`

## Why This Phase Matters
The current project history suggests:
- `1 deg` is the extreme coherent hard corner
- `3 - 5 deg` is much easier
- `2 deg` behaves like a transition boundary rather than a smooth midpoint

Phase `7F` improved broad generalization substantially, but the `2 deg` cells remained noticeably weaker than many neighboring conditions.

That suggests the next bottleneck is not architecture.

It is targeted boundary coverage.

## Working Hypothesis
The current model is simultaneously:
- strongly protected on the `1 deg`, `1 dB` coherent anchor
- broadly improved on many easier cells
- under-supported on the `2 deg` transition regime

So the correct next intervention is to increase explicit `2 deg` training support rather than starting over with a new model family.

## Model Initialization
Use the best Phase `7F` checkpoint as initialization.

Do not restart from:
- random initialization
- or the older Phase `7D` hard-cell specialist

Reason:
- Phase `7F` already contains the best current broad mixed-condition representation
- Phase `7G` should be a targeted repair of that model, not a reset

## Scope
This phase should change only:
- dataset weighting
- possibly the fine-tuning schedule

Do not change:
- geometry
- LRMC path
- anti-rectifier fusion design
- SubspaceNet backbone
- differentiable head

## Fixed Conditions
Keep fixed:
- geometry: Group B 12-channel 2D hardware geometry
- physical spacing: `1.9 lambda`
- snapshots: `T = 40`
- learned head: ESPRIT
- fusion design: width-controlled anti-rectifier spatial fusion
- backbone kernel: `3x3`
- `tau = 8`
- same canonical learned preprocessing path used in Phases `7D` and `7F`

## Training Budget
Keep the same practical wall-clock philosophy as Phase `7F`.

Recommended first attempt:
- keep total exposure roughly similar to the Phase `7F` budget
- do not exceed the established training-time envelope by a large margin

A practical default is:
- use another staged fine-tuning run of similar scale to Phase `7F`
- but redistribute sample density toward the `2 deg` boundary

## Dataset Philosophy
Phase `7G` should not use a fully uniform mixed dataset.

Instead it should use a boundary-aware dataset with three priorities:

1. preserve the coherent `1 deg` hard anchor
2. strongly reinforce the coherent `2 deg` boundary
3. keep enough non-coherent and easier-gap support to avoid losing the Phase `7F` broad gains

## Recommended Coherence Split
Keep the same high-level coherence emphasis as Phase `7F`:
- `60%` coherent
- `40%` non-coherent

Reason:
- the main unresolved weakness is still in the coherent boundary regime
- changing the coherence split now would confound the interpretation

## Recommended Dataset Structure
Use another hybrid dataset:
- stratified component
- weighted random component

Keep the same total scale as Phase `7F` unless runtime forces a reduction.

Recommended total:
- `360,000` samples

## New Core Change For Phase 7G
Relative to Phase `7F`, shift more probability mass toward:
- coherent `2 deg`
- especially coherent `2 deg` at `1 / 5 / 10 dB`

At the same time:
- keep coherent `1 deg`, `1 dB` protected
- avoid overflooding the dataset with easy `4 - 5 deg` cases

## Recommended Stratified Grid Allocation
Keep the same explicit condition grid:
- coherence: coherent, non-coherent
- SNR: `1, 5, 10, 15 dB`
- fixed gap: `1, 2, 3, 4, 5 deg`

But do not keep the coherent cells uniformly weighted anymore.

### Recommended coherent stratified weighting
Within the coherent portion of the stratified dataset:
- `1 deg`: medium-high weight
- `2 deg`: highest weight
- `3 deg`: medium weight
- `4 - 5 deg`: lower weight

Recommended coherent gap weights:
- `1 deg`: `25%`
- `2 deg`: `40%`
- `3 deg`: `20%`
- `4 deg`: `10%`
- `5 deg`: `5%`

Within each gap, distribute evenly across:
- `1, 5, 10, 15 dB`

Interpretation:
- `2 deg` becomes the dominant coherent boundary target
- `1 deg` remains protected
- wider easy gaps are still represented but no longer consume much coherent budget

### Recommended non-coherent stratified weighting
Keep the non-coherent side closer to broad coverage, but still bias mildly toward small gaps:
- `1 deg`: `30%`
- `2 deg`: `30%`
- `3 deg`: `20%`
- `4 deg`: `10%`
- `5 deg`: `10%`

Within each gap, again distribute evenly across:
- `1, 5, 10, 15 dB`

Reason:
- Phase `7F` already improved non-coherent transfer strongly
- non-coherent training should now mainly support retention, not dominate optimization

## Recommended Weighted Random Allocation
Use the random component to reinforce the same priority more continuously.

### Coherent random gap weighting
Recommended coherent random gap weighting:
- `1 deg`: `25%`
- `2 deg`: `45%`
- `3 deg`: `20%`
- `4 - 5 deg`: `10%`

### Non-coherent random gap weighting
Recommended non-coherent random gap weighting:
- `1 deg`: `25%`
- `2 deg`: `35%`
- `3 deg`: `20%`
- `4 - 5 deg`: `20%`

### Shared SNR weighting
Recommended SNR weighting:
- `1 dB`: `35%`
- `5 dB`: `30%`
- `10 dB`: `20%`
- `15 dB`: `15%`

Reason:
- the low-SNR boundary remains more operationally important
- this stays consistent with the earlier hard-case emphasis

## Practical Simplification Rule
If the exact weighted sampling implementation becomes cumbersome, the minimum acceptable simplification is:
- explicitly oversample coherent `2 deg` cells by at least `1.5x - 2x` relative to coherent `1 deg`
- and by much more relative to coherent `4 - 5 deg`

This is the essential design intent of Phase `7G`.

## Training Strategy
Use fine-tuning from Phase `7F`.

### Learning rate
Use a smaller fine-tuning rate than the first broadening jump into Phase `7F`.

Recommended range:
- `2e-6` to `5e-6`

Preferred starting point:
- `2e-6` or `3e-6`

Reason:
- Phase `7G` is a targeted repair step
- too large a rate risks erasing the broad coverage already gained in Phase `7F`

### Duration
Recommended first pass:
- shorter than Phase `7F` if possible
- enough to measure targeted repair without overcooking the model

A practical default:
- `20 - 40` epochs of repair fine-tuning

## Protected Monitoring Cells
The following cells should be explicitly tracked as protected metrics:

### Hard anchor protection
- coherent `gap = 1 deg`, `SNR = 1 dB`

### Boundary repair targets
- coherent `gap = 2 deg`, `SNR = 1 dB`
- coherent `gap = 2 deg`, `SNR = 5 dB`
- coherent `gap = 2 deg`, `SNR = 10 dB`
- coherent `gap = 2 deg`, `SNR = 15 dB`

### Broad-retention checks
- coherent `gap = 3 deg`, `SNR = 5 dB`
- non-coherent `gap = 1 deg`, `SNR = 1 dB`
- non-coherent `gap = 2 deg`, `SNR = 5 dB`

## Evaluation Set
Evaluate on the same reused Phase `7E` / Phase `7F` 40-cell grid:
- `20` coherent cells
- `20` non-coherent cells

This is essential for a clean before/after comparison against:
- Phase `7E`
- Phase `7F`

## Main Hypotheses
1. The `2 deg` weakness is a dataset-density problem, not a new architecture problem.
2. Reweighting toward coherent `2 deg` should improve the boundary cells substantially.
3. Some small loss on easier wide-gap cells is acceptable if the `2 deg` coherent boundary improves enough.
4. If the anchor degrades too much, then the repair weighting or learning rate is too aggressive.

## Baselines For Comparison
The most important comparisons are:

1. Phase `7F` mixed-condition model
- primary baseline for broad generalization

2. Phase `7D` hard-cell specialist
- reference for best pure source-cell performance

3. Phase `7E` zero-shot transfer model
- reference for what broad transfer looked like before mixed-condition fine-tuning

4. Phase 6 classical best controls
- especially around coherent `2 deg`

## Success Criteria

### Minimal success
The coherent `2 deg` cells improve clearly relative to Phase `7F`, while the coherent `1 deg`, `1 dB` anchor does not degrade badly.

### Strong success
The coherent `2 deg` boundary improves substantially across multiple SNR values, and the model keeps most of the broad Phase `7F` gains elsewhere.

### Informative negative result
If the coherent `2 deg` cells improve but the `1 deg`, `1 dB` anchor or the non-coherent broad gains collapse, then:
- the boundary emphasis is directionally correct
- but the weighting or fine-tuning aggressiveness is too strong

### No-go result
If the `2 deg` cells do not improve materially, then:
- the weakness is not mainly sample-allocation driven
- and the next step may need curriculum design, loss reweighting, or architecture-side boundary handling

## Metrics
Primary metric:
- horizontal-angle RMSE in degrees

Secondary metrics:
- mean coherent `2 deg` RMSE across all four SNRs
- per-cell coherent `2 deg` RMSE
- coherent `1 deg`, `1 dB` anchor retention
- coherent OOD mean RMSE
- non-coherent transfer mean RMSE
- delta vs Phase `7F`
- delta vs Phase `7D` anchor
- average runtime per sample

## Recommended Result Tables
At minimum, report:

1. coherent `2 deg` boundary table
- SNR
- Phase `7F` RMSE
- Phase `7G` RMSE
- delta

2. source-cell retention table
- coherent `1 deg`, `1 dB`
- Phase `7D`
- Phase `7F`
- Phase `7G`

3. coherent reused-grid table
- same format as Phase `7F`

4. non-coherent reused-grid table
- same format as Phase `7F`

5. summary bucket table
- coherent `2deg_boundary`
- coherent_ood
- noncoherent_transfer

## Interpretation Rules

### If coherent `2 deg` improves and anchor stays stable
Conclusion:
- the remaining weakness was mainly a sampling-density problem
- boundary-aware dataset design is the correct next lever

### If coherent `2 deg` improves but anchor worsens notably
Conclusion:
- the direction is correct
- but the repair run needs stronger anchor protection or a lower LR

### If coherent `2 deg` improves but non-coherent broad transfer collapses
Conclusion:
- the coherent emphasis is too narrow
- Phase `7F` broadening needs stronger retention support during the repair run

### If little changes at `2 deg`
Conclusion:
- the issue is not solved by oversampling alone
- future work should examine curriculum, loss weighting, or architecture-side handling of the boundary regime

## Recommended Outputs
Create a new family:
- `results/phase7g_groupb_1p9_boundary_2deg_repair/`

Recommended markdown:
- `phase7g_groupb_1p9_boundary_2deg_repair_results.md`

Recommended `summary.csv`:
- one row per reused evaluation cell

## Canonical Launcher
Recommended launcher:
- `run_phase7g_groupb_1p9_boundary_2deg_repair.py`

Recommended command:
```bash
python run_phase7g_groupb_1p9_boundary_2deg_repair.py
```

## Go / No-Go Rule
Promote the Phase `7G` model over Phase `7F` only if:
- coherent `2 deg` performance improves meaningfully
- the coherent `1 deg`, `1 dB` anchor remains acceptably close to the Phase `7F` / Phase `7D` levels
- and the broader non-coherent transfer gains do not collapse

Otherwise:
- keep Phase `7F` as the best broad-coverage model
- and treat Phase `7G` as a diagnostic boundary-repair attempt rather than the new default
