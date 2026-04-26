# Phase 7D Group B 1.9 Lambda SS-Fusion Activation Ablation Experiment Plan

## Goal
Test whether replacing the plain `ReLU` activations inside the current strongest spatial SS-fusion module with the same sign-preserving anti-rectifier style used in SubspaceNet improves performance in the primary coherent hard cell.

This phase is intentionally narrow.

It is not a broad new sweep.

It is a controlled fusion-module ablation on top of the already strongest `3x3` backbone setting.

## Primary Question
In the primary coherent hard cell:
- gap `1 deg`
- SNR `1 dB`
- `T = 40`

does changing the activation inside the Phase `1.1` spatial learned-fusion block from plain `ReLU` to a SubspaceNet-style anti-rectifier improve the current `3x3` learned-fusion model?

## Why This Phase Matters
Phase `7C` showed two important things:
- the `3x3` SubspaceNet backbone improves every learned variant
- after that backbone improvement, the spatial-fusion model is still very strong but no longer clearly beats the plain `SS(3/3)` learned baseline

That leaves an important structural question:
- is the remaining fusion limitation partly caused by the fusion block using standard `ReLU`, which discards negative responses
- while the downstream SubspaceNet backbone uses a sign-preserving anti-rectifier representation

Because the fusion input is built from stacked real and imaginary covariance channels, sign information is structurally meaningful.

This makes activation handling inside the fusion block a plausible next lever.

## Test Cell
Use exactly the same main cell as Phase `7C`:
- coherent
- Group B `1.9 lambda`
- gap `1 deg`
- SNR `1 dB`
- `T = 40`

## Scope
Run only the strongest current learned-fusion pipeline:
- `SS(2/3 x 3) -> LRMC -> spatial learned fusion -> SubspaceNet(backbone 3x3) -> ESPRIT`

Do not rerun:
- `SS(3/3)` baseline
- fixed `SS(2/3: rows 0+1)` baseline
- `1x1` fusion model

Use the already completed Phase `7C` spatial-fusion `3x3` result as the direct reference.

## Direct Comparison

### Existing Reference To Reuse
Current strongest spatial-fusion reference:
- `SS(2/3 x 3) -> LRMC -> learned fusion(ReLU) -> SubspaceNet(backbone 3x3) -> ESPRIT`
- current RMSE: about `0.4118 deg`

### New Run Required
Candidate ablation:
- `SS(2/3 x 3) -> LRMC -> learned fusion(anti-rectifier style) -> SubspaceNet(backbone 3x3) -> ESPRIT`

Readable label:
- `SS(2/3 x 3) -> LRMC -> anti-rectifier learned fusion -> SubspaceNet backbone 3x3`

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
- `tau = 8`
- Backbone kernel: `3x3`
- Seed: fixed at `42`

## Controlled Variable
The intended changed variable is:
- activation design inside the spatial SS-fusion module

From:
- standard `ReLU`

To:
- SubspaceNet-style anti-rectifier / sign-preserving activation

Everything else should be held fixed as closely as possible:
- same dataset definition
- same seed
- same training scale
- same optimizer and schedule
- same branch construction
- same LRMC settings
- same `3x3` backbone
- same evaluation code

## Important Fairness Rule
This should be treated as an activation ablation, not a hidden-capacity expansion.

That means the anti-rectifier fusion variant should be implemented so that:
- the comparison stays as parameter-controlled as practical
- post-activation channel growth does not accidentally become the main changed variable

What this means in concrete code terms:
- the current spatial fusion block is:
  - `Conv2d(6 -> h, k=3) -> ReLU -> Conv2d(h -> h, k=3) -> ReLU -> Conv2d(h -> 2, k=1)`
- SubspaceNet's anti-rectifier is not a drop-in scalar activation
  - it maps a tensor with `h` channels to `2h` channels by concatenating `ReLU(x)` and `ReLU(-x)`
- so if we naively replace each `ReLU` with anti-rectification, the fusion block would become effectively:
  - `Conv2d(6 -> h, k=3) -> AntiRect(h -> 2h) -> Conv2d(2h -> h, k=3) -> AntiRect(h -> 2h) -> Conv2d(2h -> 2, k=1)`
- that is no longer a pure activation swap
  - intermediate tensors are wider
  - later convolutions see more input channels
  - parameter count and representational capacity both change

Why that matters:
- if the anti-rectifier model wins after that naive change, we would not know whether it won because:
  - sign-preserving activation is better
  - or because the fusion module quietly became larger and more expressive

### Preferred Fair Implementation
The anti-rectifier variant should keep the effective hidden width as close as practical to the current ReLU model.

Recommended interpretation:
- keep the post-activation width fixed at about `h`, not `2h`

One clean way to do that is:
- change the pre-activation convolution width from `h` to `h/2`
- then apply anti-rectification so the output width returns to about `h`

Example when the current hidden width is `h = 16`:
- current ReLU block:
  - `Conv2d(6 -> 16, k=3) -> ReLU -> Conv2d(16 -> 16, k=3) -> ReLU -> Conv2d(16 -> 2, k=1)`
- fairer anti-rectifier block:
  - `Conv2d(6 -> 8, k=3) -> AntiRect(8 -> 16) -> Conv2d(16 -> 8, k=3) -> AntiRect(8 -> 16) -> Conv2d(16 -> 2, k=1)`

This is not perfectly parameter-matched, but it is much closer to the intended ablation because:
- the hidden feature width seen by the later stages stays near the original design
- the main changed factor is sign-preserving activation behavior rather than a large width increase

### Non-Preferred Implementation
Avoid this version as the main experiment:
- `Conv2d(6 -> 16, k=3) -> AntiRect(16 -> 32) -> Conv2d(32 -> 16, k=3) -> AntiRect(16 -> 32) -> Conv2d(32 -> 2, k=1)`

Reason:
- this variant changes both activation style and effective hidden width at the same time
- any gain would be hard to interpret cleanly

### Decision Rule For This Phase
For Phase `7D`, the main reported anti-rectifier result should come from the width-controlled implementation above.

If desired, the naive doubled-width anti-rectifier version can be run later as a separate follow-up, but it should be labeled explicitly as:
- activation plus capacity change

not as a pure activation ablation.

## Training Scale
Use the same current SubspaceNet large-training scale as Phase `7C`.

Reason:
- this phase is meant to be directly comparable to the completed spatial-fusion `3x3` run
- reducing training scale would weaken interpretation

## Main Hypotheses
1. A sign-preserving activation may help because the fusion input carries real/imaginary covariance structure where positive and negative responses are both meaningful.
2. If the fusion block currently loses useful negative evidence under plain `ReLU`, the anti-rectifier variant may recover some of the gap to the plain `SS(3/3)` `3x3` winner.
3. The change may also do little or even hurt if the current fusion block is already capacity-limited or if the extra sign-splitting makes optimization noisier.

## Success Criteria

### Minimal success
The anti-rectifier fusion variant beats the current ReLU-based spatial-fusion `3x3` reference:
- better than about `0.4118 deg`

### Strong success
The anti-rectifier fusion variant not only beats the current ReLU-based fusion reference, but also reaches or beats the current best overall `3x3` result:
- plain `SS(3/3)` `3x3` baseline at about `0.4087 deg`

### Informative negative result
If the anti-rectifier fusion variant matches or underperforms the ReLU-based fusion reference, that is still useful evidence that:
- the current fusion limitation is not mainly an activation-sign issue
- future work should focus more on fusion structure, weighting constraints, or training strategy than on activation replacement alone

## Metrics
Primary metric:
- horizontal-angle RMSE

Secondary metrics:
- validation RMSE
- train/validation loss stability
- fusion diagnostics
- runtime per epoch
- memory overhead if easy to log

## Interpretation Rules

### If anti-rectifier clearly helps
Conclusion:
- sign-preserving activation is beneficial inside the covariance-fusion block
- the mismatch between ReLU-based fusion and anti-rectifier-based backbone was likely a real limitation
- this activation should be carried into the next fusion follow-up

### If anti-rectifier ties ReLU within a small margin
Conclusion:
- activation choice is not a major driver here
- the simpler ReLU fusion remains acceptable on engineering grounds

### If anti-rectifier loses clearly
Conclusion:
- plain ReLU is sufficient or preferable in the current fusion block
- the remaining fusion gap should be pursued elsewhere

## Expected Outputs
Running this phase should produce:
- per-model `metrics.json`
- training curves and checkpoints
- one family markdown results file
- `summary.csv`

Recommended results path:
- `results/phase7d_groupb_1p9_ssfusion_activation_ablation/`

Recommended markdown result file:
- `phase7d_groupb_1p9_ssfusion_activation_ablation_results.md`

## Recommended Result Table
At minimum, report:
- fusion activation type
- backbone kernel
- RMSE
- delta vs ReLU spatial-fusion `3x3` reference
- delta vs plain `SS(3/3)` `3x3` best baseline

## Canonical Launcher
Recommended new launcher:
- `run_phase7d_groupb_1p9_ssfusion_activation_ablation.py`

Recommended command:
```bash
python run_phase7d_groupb_1p9_ssfusion_activation_ablation.py
```

## Go / No-Go Rule
Promote the anti-rectifier fusion variant beyond this cell only if:
- training remains stable
- it improves over the current ReLU-based spatial-fusion `3x3` reference
- and it is at least competitive with the current best `SS(3/3)` `3x3` baseline

Otherwise:
- keep the current ReLU-based fusion as the reference implementation
- and treat this run as a targeted activation ablation rather than a new default
