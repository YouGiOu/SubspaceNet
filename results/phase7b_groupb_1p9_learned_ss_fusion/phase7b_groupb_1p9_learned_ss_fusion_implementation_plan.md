# Phase 7B Group B 1.9 Lambda Learned SS-Fusion Module Implementation Plan

## Goal
Design a learnable preprocessing module that replaces the fixed averaging implicit in the current rowwise spatial-smoothing stage.

The new module should:
- build LRMC-completed covariance matrices from each `2-of-3` row-pair SS choice
- fuse them with learnable convolutional processing
- output one fused covariance surrogate
- feed that fused covariance into the existing SubspaceNet pipeline as the downstream learned head

The intended effect is to let the network learn when the best behavior is closer to:
- `SS(3/3)`
- `SS(2/3: rows 0+1)`
- `SS(2/3: rows 0+2)`
- `SS(2/3: rows 1+2)`

without forcing that weighting to be fixed by hand.

## Feasibility Assessment
This idea is feasible in this repo, but only if it is implemented as a wrapper around the existing SubspaceNet input path rather than by trying to feed an `N x N x 3` cube directly into the current SubspaceNet unchanged.

Why:
- current SubspaceNet expects an input tensor shaped like `[batch, tau, 2N, N]`
- that tensor is produced after one covariance matrix is already chosen and converted into the repo's autocorrelation-style representation
- current SubspaceNet therefore does not have a native entry point for a three-branch covariance cube

So the practical design is:
1. compute three LRMC-completed covariance matrices
2. stack them into a three-channel covariance cube
3. run a learnable fusion block
4. reconstruct one fused complex covariance matrix
5. convert that fused covariance into the standard SubspaceNet input tensor
6. pass it through the existing SubspaceNet backbone and ESPRIT head

That makes the approach realistic without rewriting the whole SubspaceNet model.

## Current Relevant Code Touch Points
- [src/data_handler.py](/f:/workspace1/SubspaceNet/src/data_handler.py)
  Current `build_subspacenet_input(...)` path for LRMC-based preprocessing.
- [src/models.py](/f:/workspace1/SubspaceNet/src/models.py)
  Current SubspaceNet architecture and model registration flow.
- [src/lrmc.py](/f:/workspace1/SubspaceNet/src/lrmc.py)
  Current rowwise LRMC completion utilities used after SS.
- [src/methods.py](/f:/workspace1/SubspaceNet/src/methods.py)
  Classical evaluation flow and SubspaceNet covariance usage.

## Current Input-Shape Reality
The covariance size should be decided by the code, not by assumption.

Given the current Group B LRMC setup:
- the virtual ULA size is typically `9`
- so each LRMC-completed covariance is expected to be `9 x 9`

The proposed fusion input is therefore most likely:
- `9 x 9 x 3`

not `8 x 8 x 3`.

The plan should explicitly avoid hard-coding `8`.

All code should derive the covariance size from:
- `virtual_array_size`
- or the actual completed covariance returned by the LRMC path

## Proposed Architecture

### High-Level Structure
The new model family should be:
- `three SS(2/3) LRMC branches`
- `learnable covariance-fusion module`
- `existing SubspaceNet backbone`
- `existing differentiable ESPRIT head`

### Recommended First Version
Use only the three `2-of-3` branches:
- rows `0+1`
- rows `0+2`
- rows `1+2`

Do not include the explicit `SS(3/3)` branch in version 1.

Reason:
- your stated goal is to let the network learn a replacement for fixed averaging over the pairwise alternatives
- adding `SS(3/3)` as a fourth branch can be a later ablation once the simpler three-branch version is understood

### Fusion-Block Input Representation
Each branch should produce one complex LRMC-completed covariance.

For a convolutional fusion block, represent each covariance by real-valued channels.

Recommended options:

Option A:
- stack real and imaginary parts for each branch
- total channels = `6`

Option B:
- stack real, imaginary, and phase for each branch
- total channels = `9`

Recommended first version:
- use real + imaginary only

Reason:
- it matches the current SubspaceNet internal representation more naturally
- phase can be added later if needed

So the practical first fusion tensor is likely:
- shape `[batch, 6, N, N]`

not a literal `[batch, N, N, 3]` tensor in the final implementation.

## Recommended Fusion Output
The fusion module should output one fused complex covariance matrix with shape:
- `[batch, N, N]`

This fused covariance should then be:
- Hermitian-symmetrized
- optionally diagonally stabilized if needed
- converted into the repo's existing autocorrelation-style SubspaceNet tensor

The output should not bypass the current SubspaceNet backbone.

That keeps the comparison clean:
- only the preprocessing fusion becomes learnable
- the downstream learned head remains the known working SubspaceNet-ESPRIT path

## Minimum New Components

### 1. Multi-branch covariance builder
Add a utility that, for one sample, returns all three LRMC-completed covariances:
- `SS(2/3: rows 0+1) -> LRMC`
- `SS(2/3: rows 0+2) -> LRMC`
- `SS(2/3: rows 1+2) -> LRMC`

This should reuse the existing rowwise LRMC path rather than duplicating LRMC logic.

### 2. Learnable covariance-fusion module
Add a new PyTorch module that:
- accepts the stacked covariance channels
- uses a small CNN stack
- outputs one fused complex covariance

The first version should be intentionally small.

Reason:
- the sample budget is not huge by modern CV standards
- the scientific question is whether adaptive fusion helps, not whether a deep image backbone helps

### 3. Wrapper model
Add a new model class that:
- calls the three-branch covariance builder
- applies the fusion module
- converts the fused covariance into the current SubspaceNet input format
- forwards into the original SubspaceNet-ESPRIT backbone

### 4. Model registration
Add one new model type to the model generator so experiments can request this architecture cleanly.

## Numerical Requirements
The fused covariance must remain numerically sane.

Required safeguards:
- Hermitian projection after fusion
- optional diagonal loading / stabilization before conversion to downstream input
- explicit finite-value checks

Without this, the learned fusion block may output matrices that are easy to optimize numerically but invalid as covariance surrogates.

## Recommended Training Strategy
Do not train the full new architecture on a large broad grid first.

Start with the hard coherent cell family where the SS-floor result is most meaningful:
- coherent
- Group B `1.9 lambda`
- low separation

This keeps the experiment aligned with the reason the module exists.

## Backward-Compatibility Requirements
The new model should be additive, not disruptive.

Requirements:
- existing SubspaceNet templates continue to run unchanged
- current `build_subspacenet_input(...)` behavior remains unchanged for old models
- the new fusion path is only activated for the new model family

## Diagnostics To Record
The implementation should expose branch-level information so later analysis is possible.

Useful diagnostics:
- per-branch covariance norms
- learned fusion-map statistics
- branch contribution summaries, if an attention-style or weighted fusion is used
- fused covariance stability indicators

If the module behaves like a black box, it will be hard to tell whether it truly learned branch selection or just learned a weak surrogate covariance prior.

## Recommended Naming
Suggested model family name:
- `SubspaceNetSSFusionEsprit`

Suggested conceptual label:
- `SS(2/3 x 3) -> LRMC -> learned fusion -> SubspaceNet -> ESPRIT`

## Risks
1. The module may simply relearn the behavior of one fixed row pair.
   That is still useful scientifically, but it must be diagnosed explicitly.

2. The fusion block may overfit easy covariance statistics rather than genuinely improving hard-cell robustness.

3. The extra learned stage may help only because it increases total model capacity rather than because it exploits the SS-floor structure.
   This is why strong baselines are necessary.

4. The branch covariances are highly correlated.
   The gain may be small unless the model is encouraged to use branch differences meaningfully.

## Out Of Scope For The First Implementation Pass
- replacing the downstream ESPRIT head
- trying differentiable Root-MUSIC again
- introducing transformer-style fusion
- mixing coherent and non-coherent training in one first implementation unless the experiment plan explicitly calls for it

## Deliverables
- one new multi-branch covariance builder
- one learnable covariance-fusion module
- one wrapper SubspaceNet model family
- model registration for ablation templates
- one dedicated experiment-plan document

## Completion Criteria
This implementation phase is complete when:
- the repo can train and evaluate the new learned-fusion model without changing old SubspaceNet paths
- the fusion model consumes three `2-of-3` LRMC covariance branches and emits one fused covariance
- the fused covariance is passed into the original SubspaceNet-style downstream processing
- branch-aware diagnostics are available for later interpretation
