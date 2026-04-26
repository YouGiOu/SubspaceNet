# Phase 7C Group B 1.9 Lambda SubspaceNet 3x3 Backbone Implementation Plan

## Goal
Implement a `3x3`-kernel SubspaceNet backbone variant and make it available to the existing Group B learned pipelines so we can run a controlled backbone comparison against the current `2x2` backbone under the already-established Phase `7B` primary hard-cell setting.

This is an implementation-plan document because the change is not just a new sweep.

It introduces a new model/backbone option in the training code.

## Verified Current Architecture
The current Phase `7B` learned SS-fusion path is:

- three `SS(2/3)` row-pair branches
- rowwise `LRMC` on each branch to produce `9 x 9` complex covariances
- stack real and imaginary parts into a fusion tensor of shape `[B, 6, 9, 9]`
- fusion block:
  - Phase `1.1`: `3x3 -> 3x3 -> 1x1`
  - Phase `1.1.1`: `1x1 -> 1x1 -> 1x1`
- fused complex covariance with Hermitian projection and diagonal loading
- convert fused covariance to SubspaceNet autocorrelation layout `[B, tau, 2N, N]`
- current `tau = 8`, `N = 9`, so the actual tensor is `[B, 8, 18, 9]`
- SubspaceNet backbone
- differentiable ESPRIT head

Important correction relative to the shorthand architecture description:
- the current backbone is not plain `conv -> conv -> conv -> deconv -> deconv -> deconv`
- it is the repo's original anti-rectifier SubspaceNet:
  - `Conv2d(tau, 16, k=2)`
  - anti-rectifier to `32` channels
  - `Conv2d(32, 32, k=2)`
  - anti-rectifier to `64` channels
  - `Conv2d(64, 64, k=2)`
  - anti-rectifier to `128` channels
  - `ConvTranspose2d(128, 32, k=2)`
  - anti-rectifier to `64` channels
  - `ConvTranspose2d(64, 16, k=2)`
  - anti-rectifier to `32` channels
  - `ConvTranspose2d(32, 1, k=2)`
  - Gram/Hermitian surrogate covariance projection
  - ESPRIT

## Design Decision
The requested backbone change should replace the SubspaceNet encoder and decoder kernel sizes:

- from `2x2`
- to `3x3`

while keeping the rest of the backbone logic unchanged:

- same anti-rectifier structure
- same number of stages
- same channel counts
- same dropout
- same Gram / diagonal-loading surrogate covariance projection
- same ESPRIT head

Recommended first implementation choice:
- keep the current no-padding topology
- change only `kernel_size`

That yields this spatial path:

- input `[B, 8, 18, 9]`
- after encoder: `[18,9] -> [16,7] -> [14,5] -> [12,3]`
- after decoder: `[12,3] -> [14,5] -> [16,7] -> [18,9]`

This is the cleanest "2x2 backbone vs 3x3 backbone" comparison because it changes the receptive field without introducing padding policy as a second confounder.

## Recommended Parameterization Strategy
Do not fork the whole training/data path unnecessarily.

Instead, add an explicit backbone configuration parameter that defaults to the current behavior.

Recommended parameter:
- `subspacenet_backbone_kernel_size`

Recommended default:
- `2`

Recommended first supported values:
- `2`
- `3`

Optional future parameter, only if needed later:
- `subspacenet_backbone_name`

But for this phase, a single kernel-size parameter is likely enough.

## Model-Side Changes
Update the SubspaceNet family so the backbone kernel size is configurable.

### 1. Base `SubspaceNet`
Modify the constructor to accept:
- `backbone_kernel_size: int = 2`

Use it in:
- `conv1`
- `conv2`
- `conv3`
- `deconv2`
- `deconv3`
- `deconv4`

Add validation:
- raise if the kernel size is unsupported
- for now, restrict to `2` or `3`

### 2. Fusion Models
Ensure the Phase `1.1` and Phase `1.1.1` models can pass the same backbone kernel size through to the inherited SubspaceNet constructor.

Important scope rule:
- the fusion block itself should remain unchanged in this phase
- only the downstream SubspaceNet backbone changes

So:
- Phase `1.1` remains fusion `3x3 -> 3x3 -> 1x1`
- Phase `1.1.1` remains fusion `1x1 -> 1x1 -> 1x1`
- only the shared SubspaceNet backbone becomes `3x3`

## Training / Factory Changes
Update model construction so the new backbone option can be set from templates.

Files expected to change:
- `src/models.py`
- `src/training.py`

Possibly also:
- any model-factory or config plumbing that instantiates `SubspaceNet` variants from `system_model` or template parameters

Implementation rule:
- preserve existing behavior when the new parameter is absent
- existing Phase `4`, `6`, and `7B` templates should still instantiate the current `2x2` backbone automatically

## Template Configuration Changes
For the new experiment family only, add:
- `system_model.subspacenet_backbone_kernel_size = 3`

Everything else should remain aligned with the reused Phase `7B` hard-cell settings.

Do not change:
- fusion hidden width
- fusion diagonal loading
- dataset size
- optimizer
- seed
- tau
- LRMC settings
- hard-cell definition

## Naming Recommendation
Use explicit template names and readable scheme labels that surface the backbone difference.

Recommended wording:
- `SubspaceNet backbone 2x2`
- `SubspaceNet backbone 3x3`

Recommended template suffix:
- `_backbone3x3`

## Reuse Strategy
The user explicitly does not want to rerun the `2x2` experiments.

So the implementation should support:
- running only new `3x3` variants
- reusing existing `2x2` Phase `7B` metrics as the reference comparison

Recommended practical approach:
- create a new Phase `7C` family for the `3x3` runs
- compare against metrics already produced in:
  - `results/phase7b_groupb_1p9_learned_ss_fusion_phase1p1/`
  - `results/phase7b_groupb_1p9_learned_ss_fusion_phase1p1p1/`

## Verification Checklist
Before launching the new experiment family, verify:

1. `SubspaceNet` with `backbone_kernel_size=3` returns an output covariance of shape `[B, 9, 9]`.
2. The Phase `1.1` fusion model with backbone `3x3` still accepts `[B, 6, 9, 9]` fusion input.
3. The Phase `1.1.1` fusion model with backbone `3x3` still accepts `[B, 6, 9, 9]` fusion input.
4. The surrogate covariance remains finite after Gram/Hermitian projection.
5. ESPRIT still returns `[B, 2]`.
6. A one-batch smoke training pass completes without shape errors.

## Minimal File Set Expected
- `src/models.py`
- `src/training.py`
- `run_phase7c_groupb_1p9_subspacenet_backbone_3x3.py`
- `results/phase7c_groupb_1p9_subspacenet_backbone_3x3/phase7c_groupb_1p9_subspacenet_backbone_3x3_experiment_plan.md`

Possible additional changes:
- template-generation logic in the new launcher

## Non-Goals
This phase should not:

- redesign the Phase `1.1` fusion module
- redesign the Phase `1.1.1` `1x1` fusion module
- change `tau`
- change LRMC
- change the hard-cell dataset definition
- broaden to additional cells before the primary comparison is complete
- retrain the old `2x2` baseline family

## Success Condition For Implementation
The implementation is complete when:

- a new launcher can generate a Phase `7C` family
- that family runs only the new `3x3` backbone variants
- and its outputs can be compared directly against the already-finished `2x2` Phase `7B` backbone results in the same coherent hard cell
