# Phase 7B Phase 1.1.1 Group B 1.9 Lambda 1x1 SS-Fusion Module Implementation Plan

## Goal
Implement a safer learned SS-fusion variant for the primary hard coherent cell by replacing the current spatial fusion block with a `1x1` channel-only fusion block.

The purpose of this phase is not to redesign the whole learned pipeline.

It is to answer one focused question:
- if the learned fusion is restricted to mix only across branch channels at each covariance entry, can it outperform the current Phase `1.1` baselines while reducing the risk of damaging covariance structure?

## Motivation
Phase `1.1` already showed that learned SS-fusion can beat:
- the current `SS(3/3) -> LRMC -> SubspaceNet` learned baseline
- the best fixed `SS(2/3: rows 0+1) -> LRMC -> SubspaceNet` learned baseline

However, the current fusion block still uses spatial convolutions:
- `3x3`
- `3x3`
- then `1x1`

That means it can mix neighboring covariance entries, not only branch channels.

The main concern for this follow-up is:
- the branch covariances are already good structured objects
- a spatial CNN may improve performance, but it can also distort the covariance matrix in ways that are hard to interpret

The `1x1` version is therefore intended as a more structure-preserving adaptive fusion baseline.

## Design Principle
The `1x1` fusion module should:
- preserve the existing three-branch `SS(2/3) -> LRMC` preprocessing
- preserve the existing wrapper architecture
- change only the learnable fusion operator

This keeps the comparison with Phase `1.1` clean.

## Current Relevant Code Touch Points
- [src/models.py](/f:/workspace1/SubspaceNet/src/models.py)
  Current `SubspaceNetSSFusionEspritPhase1p1` implementation and fusion block definition.
- [src/ss_fusion_phase1p1.py](/f:/workspace1/SubspaceNet/src/ss_fusion_phase1p1.py)
  Current three-branch covariance construction and fusion input assembly.
- [src/data_handler.py](/f:/workspace1/SubspaceNet/src/data_handler.py)
  Current model-type dispatch for the SS-fusion input path.
- [src/training.py](/f:/workspace1/SubspaceNet/src/training.py)
  Current model selection / training path for the learned-fusion model.

## Required Functional Change
The only intended architectural change is:
- replace the current spatial fusion stack with a `1x1` channel-mixing fusion block

Current Phase `1.1` fusion block:
- `Conv2d(6, hidden, kernel_size=3, padding=1)`
- `Conv2d(hidden, hidden, kernel_size=3, padding=1)`
- `Conv2d(hidden, 2, kernel_size=1)`

Phase `1.1.1` target:
- use `1x1` kernels only in the fusion module

## Recommended First Version

### Input
Keep the current Phase `1.1` fusion input unchanged:
- three branch covariances
- real and imaginary parts stacked as channels
- input shape `[batch, 6, N, N]`

This preserves comparability.

### Fusion Block
Recommended first `1x1` fusion stack:
- `Conv2d(6, hidden, kernel_size=1)`
- nonlinearity
- optional second `Conv2d(hidden, hidden, kernel_size=1)`
- nonlinearity
- `Conv2d(hidden, 2, kernel_size=1)`

This allows nonlinear channel mixing while avoiding direct spatial mixing across neighboring covariance entries.

### Output
Keep the current output logic unchanged:
- output fused real / imaginary channels
- reconstruct complex covariance
- Hermitian projection
- optional diagonal loading
- finite-value checks
- convert to the standard SubspaceNet autocorrelation-style tensor
- forward into the existing SubspaceNet-ESPRIT backbone

## Why 1x1 Is A Meaningful Variant
This change makes the model much closer to:
- adaptive branch weighting

and much less like:
- free covariance image editing

At each covariance entry `(i, j)`, the model can still learn:
- how much to trust each branch
- how to combine real and imaginary components across branches

But it cannot directly reshape the local spatial pattern by mixing neighboring entries.

That makes the result:
- easier to interpret
- lower-risk structurally
- a better test of whether the gain in Phase `1.1` comes from branch fusion itself or from broader spatial CNN flexibility

## Backward-Compatibility Requirements
This phase should be additive.

Requirements:
- do not replace the current Phase `1.1` model
- add a separate model family for the `1x1` version
- keep old templates and old training results reproducible

Recommended new model name:
- `SubspaceNetSSFusionEspritPhase1p1p1`

## Diagnostics Requirements
The `1x1` version should keep the current Phase `1.1` fusion diagnostics and add enough information to support fair comparison.

Minimum diagnostics:
- input branch norms
- fused covariance norm
- fused diagonal mean
- model configuration indicating that fusion kernels are `1x1`

If feasible, also record:
- learned channel-weight summary statistics

## Numerical Safeguards
Keep all current safeguards from Phase `1.1`:
- branch covariances must be Hermitian and finite before fusion
- fused covariance must be Hermitian-projected
- diagonal loading must remain configurable
- non-finite fused outputs must fail loudly

Do not weaken these protections for this variant.

## Fair Comparison Requirements
To isolate the effect of kernel type, Phase `1.1.1` should keep fixed:
- same hard cell
- same dataset scale
- same branch definitions
- same downstream SubspaceNet backbone
- same training protocol as closely as possible

The main changed variable should be:
- `3x3` spatial fusion versus `1x1` channel-only fusion

## Risks
1. The `1x1` model may lose the small gain achieved by the Phase `1.1` spatial CNN.
   That would suggest that some useful spatial correction was actually being learned.

2. The `1x1` model may simply reproduce the best fixed branch.
   That is still useful because it would indicate that adaptive branch selection, not spatial refinement, is the main source of benefit.

3. The gain may be too small to separate reliably from run-to-run variation.
   This is why the comparison should stay tightly matched to the Phase `1.1` setup.

## Out Of Scope
- changing the three branch definitions
- adding `SS(3/3)` as a fusion branch
- replacing ESPRIT
- changing dataset generation rules
- introducing attention, transformer, or graph-style fusion in this phase

## Deliverables
- one new `1x1` SS-fusion model family
- model registration for the new family
- templates and launcher support for the Phase `1.1.1` experiment
- one dedicated experiment-plan document

## Completion Criteria
This implementation phase is complete when:
- the repo can train and evaluate the `1x1` SS-fusion variant as a separate model family
- the only substantive fusion change relative to Phase `1.1` is kernel type
- the model preserves the current covariance-projection and stabilization safeguards
- the resulting experiment can be compared directly against the three Phase `1.1` baselines
