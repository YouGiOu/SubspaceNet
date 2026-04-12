# Phase 1E LRMC Coherent-Signal Initialization Ablation Plan

## Status
This document defines **Phase 1E**, the next coherent-signal LRMC study after the completed solver ablation in Phase 1D.

Completed before this stage:
- Phase 1A coherent NULA snapshot ablation
- Phase 1B coherent NULA rank ablation
- Phase 1C coherent NULA Toeplitz ablation
- Phase 1D coherent NULA solver ablation

Target of this stage:
- compare LRMC initialization strategies under the current best coherent-signal configuration

Not included yet in this stage:
- post-LRMC decorrelation
- SubspaceNet retraining

## Goal
Phase 1E tests whether LRMC initialization strategy materially affects coherent-signal NULA DOA estimation once rank, Toeplitz, and solver have already been fixed to the best settings identified so far.

## Why Initialization Comes Next
Phase 1D indicates that `svd` is better than `nuclear` and is also much faster. With rank, Toeplitz, and solver now fixed, the next unresolved optimization detail is initialization.

Initialization is important because the alternating low-rank completion solver is iterative and can be sensitive to the starting point, especially under coherent signals and structured missing patterns.

## Phase 1E Design
Fixed conditions:
- Array: NULA `[0, 1, 4, 8]` on a `0.5 lambda` grid
- Virtual ULA size: `9`
- Sources: `M = 2`, coherent, narrowband
- SNR: `10 dB`
- DOA range: `[-90 deg, 90 deg]`
- Minimum source separation: `15 deg`
- Seed: fixed at `42`
- Dataset size: `4096` generated training-side samples and `0.2` test ratio
- Snapshot count: `T = 200`
- LRMC rank: `3`
- LRMC solver: `svd`
- Toeplitz enforcement: `true`
- Methods: `MUSIC`, `Root-MUSIC`, `ESPRIT`

Variables in Phase 1E:
- Baseline: no LRMC
- LRMC init = `lag`
- LRMC init = `zero`
- LRMC init = `neighbor`
- LRMC init = `random`

## Methodological Note
The no-LRMC baseline is still executed directly on the physical NULA.

- `MUSIC` remains geometry-aware because it uses the explicit sensor positions.
- `Root-MUSIC` and `ESPRIT` are not converted to a physical ULA before execution.
- Therefore, the no-LRMC `Root-MUSIC` and `ESPRIT` results remain stress baselines rather than fully geometry-valid ULA-style baselines.

The LRMC branch completes the covariance onto a virtual ULA before classical estimation, which makes `Root-MUSIC` and `ESPRIT` much more methodologically appropriate there.

## Hypotheses
- `lag` is expected to remain strong because it uses observed lag structure directly.
- `zero` may be too crude and may slow or bias the completion process.
- `neighbor` may help if nearby lag information is informative under the structured mask.
- `random` is likely to be the least stable, but it is useful as a robustness stress test.

## What Counts as a Good Phase 1E Outcome
A useful Phase 1E outcome should answer:
- whether initialization strategy produces a meaningful RMSE difference
- whether the winning initialization is stable across all three methods
- whether the default initialization should remain `lag` or be updated

## Phase 1E Files
Template files used for this stage:
- [phase1e_nula_coherent_no_lrmc_t200.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc_init/phase1e_nula_coherent_no_lrmc_t200.json)
- [phase1e_nula_coherent_lrmc_lag_t200.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc_init/phase1e_nula_coherent_lrmc_lag_t200.json)
- [phase1e_nula_coherent_lrmc_zero_t200.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc_init/phase1e_nula_coherent_lrmc_zero_t200.json)
- [phase1e_nula_coherent_lrmc_neighbor_t200.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc_init/phase1e_nula_coherent_lrmc_neighbor_t200.json)
- [phase1e_nula_coherent_lrmc_random_t200.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc_init/phase1e_nula_coherent_lrmc_random_t200.json)

Canonical Phase 1E launcher:
- [run_phase1_coherent_lrmc_init.py](f:/workspace1/SubspaceNet/run_phase1_coherent_lrmc_init.py)

Recommended command:
```bash
python run_phase1_coherent_lrmc_init.py
```

Expected outputs:
- `results/phase1_coherent_lrmc_init/summary.csv`
- `results/phase1_coherent_lrmc_init/phase1_coherent_lrmc_init_results.md`

## What To Do After Phase 1E
After the initialization results are available, inspect the following before moving to the next stage:
- Is one initialization clearly best?
- Is the ranking stable across `MUSIC`, `Root-MUSIC`, and `ESPRIT`?
- Is initialization sensitivity small enough that later effort should shift to post-LRMC decorrelation?

If initialization sensitivity is weak, keep the best initialization fixed and move on to:
- post-LRMC decorrelation

Only after the best coherent-signal LRMC configuration is identified should SubspaceNet be reintroduced.
