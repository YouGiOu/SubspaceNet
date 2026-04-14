# Phase 4B Group B 1.9 Lambda Non-Coherent SubspaceNet Large-Sample Experiment Plan

## Status
This document defines the large-sample non-coherent SubspaceNet training run on the validated Group B hardware geometry after completing the coherent Phase 4A experiment.

Completed before this stage:
- Phase 2 2D LRMC / spatial-smoothing order studies
- Phase 2 geometry-shape ablations for Groups A, B, and C
- Fixed-elevation geometry controls
- 1D pattern-control experiments confirming that the sparse row pattern itself influences LRMC performance
- Phase 4A coherent large-sample SubspaceNet training on Group B

Target of this stage:
- train SubspaceNet directly on the Group B `1.9 lambda` hardware geometry under non-coherent sources using a paper-scale `45,000`-sample dataset

Not included yet in this stage:
- architecture changes to SubspaceNet itself
- training on alternative preprocessing orders
- multi-seed training ablation

## Goal
Test whether the previously under-performing differentiable Root-MUSIC head becomes more stable and accurate under non-coherent sources, while also measuring the corresponding non-coherent ESPRIT-head performance.

## Why This Configuration
The non-coherent classical experiments showed:
- Group B at `1.9 lambda` becomes a very favorable geometry under non-coherent sources
- MUSIC becomes nearly trivial, but Root-MUSIC and ESPRIT still benefit from LRMC-based preprocessing
- `LRMC -> SS` slightly outperformed `SS -> LRMC` for classical non-coherent Root-MUSIC / ESPRIT at `1.9 lambda`, but this phase keeps `SS -> LRMC` fixed to preserve comparability with the coherent SubspaceNet run

This phase is intentionally designed to answer:
- does non-coherence make the differentiable Root-MUSIC head train more smoothly?
- how much of the coherent Root-MUSIC instability was caused by source coherence rather than by the head itself?

## Phase 4B Design
Fixed conditions:
- Array: Group B 12-channel 2D geometry
- Row pattern used by rowwise LRMC: `[0, 4, 7, 8]`
- Physical spacing: `1.9 lambda`
- Sources: `M = 2`, non-coherent, narrowband
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
- `results/phase4_subspacenet_groupb_1p9_noncoherent_large/summary.csv`
- `results/phase4_subspacenet_groupb_1p9_noncoherent_large/phase4_subspacenet_groupb_1p9_noncoherent_large_results.md`

## What Counts as a Good Outcome
A useful Phase 4B outcome should answer:
- whether Root-MUSIC training becomes visibly more stable than in the coherent study
- whether the non-coherent Root-MUSIC RMSE approaches the strong classical non-coherent baseline
- whether non-coherent ESPRIT training remains strong or improves further

## Canonical Launcher
- [run_phase4_subspacenet_groupb_1p9_noncoherent_large.py](/f:/workspace1/SubspaceNet/run_phase4_subspacenet_groupb_1p9_noncoherent_large.py)

Recommended command:
```bash
python run_phase4_subspacenet_groupb_1p9_noncoherent_large.py
```

## Follow-Up Questions After Phase 4B
After the run finishes, inspect:
- whether the Root-MUSIC loss curve is smoother than in Phase 4A
- whether the Root-MUSIC head still underperforms relative to ESPRIT
- whether future work should continue with ESPRIT-first only, or whether Root-MUSIC becomes viable in the non-coherent regime
