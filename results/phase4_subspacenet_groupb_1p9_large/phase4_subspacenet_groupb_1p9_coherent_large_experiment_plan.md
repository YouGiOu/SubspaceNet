# Phase 4A Group B 1.9 Lambda Coherent SubspaceNet Large-Sample Experiment Plan

## Status
This document defines the first SubspaceNet training run on the validated Group B hardware geometry after the 2D geometry-shape debugging and LRMC row-geometry fixes.

Completed before this stage:
- Phase 2 2D LRMC / spatial-smoothing order studies
- Phase 2 geometry-shape ablations for Groups A, B, and C
- Fixed-elevation geometry controls
- 1D pattern-control experiments confirming that the sparse row pattern itself influences LRMC performance

Target of this stage:
- train SubspaceNet directly on the Group B `1.9 lambda` hardware geometry using a paper-scale `45,000`-sample dataset

Not included yet in this stage:
- non-coherent Group B SubspaceNet training
- architecture changes to SubspaceNet itself
- training on alternative preprocessing orders
- multi-seed training ablation

## Goal
Measure whether large-sample SubspaceNet training can become competitive on the actual Group B hardware geometry once the best classical front end has been identified.

## Why This Configuration
The latest geometry-shape experiments showed:
- Group B at `1.9 lambda` is now a valid and strong geometry once the row-geometry mismatch bug is fixed
- `SS -> LRMC` is the best overall classical preprocessing path for Root-MUSIC and ESPRIT on Group B
- the previous learned baselines were likely under-trained relative to the paper because they used only `4096` samples rather than `45,000`

So the most useful first learned-model run is:
- hardware geometry = Group B
- spacing = `1.9 lambda`
- preprocessing = `SS -> LRMC`
- dataset size = `45,000`

## Phase 4A Design
Fixed conditions:
- Array: Group B 12-channel 2D geometry
- Row pattern used by rowwise LRMC: `[0, 4, 7, 8]`
- Physical spacing: `1.9 lambda`
- Sources: `M = 2`, coherent, narrowband
- SNR: `10 dB`
- Snapshots: `T = 200`
- Azimuth range: `[-15 deg, 15 deg]`
- Elevation range: `[-15 deg, 15 deg]`
- Minimum azimuth separation: `5 deg`
- Preprocessing: `SS -> LRMC`
- LRMC rank: `3`
- LRMC solver: `svd`
- LRMC initialization: `lag`
- Virtual ULA size: `9`
- Seed: fixed at `42`
- Dataset size: `45,000`
- Train/test split: `0.2`

Learned variants in this phase:
- SubspaceNet with differentiable ESPRIT
- SubspaceNet with differentiable Root-MUSIC

## Expected Outputs
Running the launcher should produce:
- per-method metrics JSON files
- learned-model loss curves
- saved checkpoints
- `results/phase4_subspacenet_groupb_1p9_coherent_large/summary.csv`
- `results/phase4_subspacenet_groupb_1p9_coherent_large/phase4_subspacenet_groupb_1p9_coherent_large_results.md`

## What Counts as a Good Outcome
A useful Phase 4A outcome should answer:
- whether `45,000` samples materially improve learned performance on the Group B hardware geometry
- whether SubspaceNet-ESPRIT or SubspaceNet-Root-MUSIC is the better training target
- how close the learned model gets to the best classical Group B `SS -> LRMC` result

## Canonical Launcher
- [run_phase4_subspacenet_groupb_1p9_coherent_large.py](/f:/workspace1/SubspaceNet/run_phase4_subspacenet_groupb_1p9_coherent_large.py)

Recommended command:
```bash
python run_phase4_subspacenet_groupb_1p9_coherent_large.py
```

## Follow-Up Questions After Phase 4A
After the run finishes, inspect:
- whether the learning curve still improves near the final epoch
- whether the two differentiable heads converge to similar or very different RMSE
- whether the learned model is now close enough to the classical baseline to justify broader 2D SubspaceNet experiments

If the large-sample gain is still weak, the next likely directions are:
- multi-seed training stability checks
- non-coherent Group B training
- revisiting the SubspaceNet input representation for the 2D rowwise-LRMC pipeline

