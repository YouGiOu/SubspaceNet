# Phase 1C LRMC Coherent-Signal Toeplitz Ablation Plan

## Status
This document defines **Phase 1C**, the next coherent-signal LRMC study after the completed rank ablation in Phase 1B.

Completed before this stage:
- Phase 1A coherent NULA snapshot ablation
- Phase 1B coherent NULA rank ablation

Target of this stage:
- test whether Toeplitz enforcement improves coherent-signal LRMC performance once the best rank has been fixed

Not included yet in this stage:
- LRMC solver comparison (`svd` vs `nuclear`)
- LRMC initialization comparison
- post-LRMC decorrelation
- SubspaceNet retraining

## Goal
Phase 1C tests whether enforcing Toeplitz structure during LRMC improves coherent-signal NULA DOA estimation when using the best rank identified in Phase 1B.

## Why Toeplitz Comes Next
Phase 1B indicates that `rank=3` remains the strongest choice overall. Once rank is fixed, the next most meaningful structural question is whether physics-informed Toeplitz projection helps the recovered virtual covariance become more suitable for classical subspace estimation.

Toeplitz enforcement is attractive because the virtual ULA covariance should ideally inherit approximate shift-invariant structure. If it helps, it gives a principled way to regularize LRMC beyond rank truncation alone.

## Phase 1C Design
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
- LRMC initialization: `lag`
- Methods: `MUSIC`, `Root-MUSIC`, `ESPRIT`

Variables in Phase 1C:
- Baseline: no LRMC
- LRMC with Toeplitz disabled
- LRMC with Toeplitz enabled

## Methodological Note
The no-LRMC baseline is still executed directly on the physical NULA.

- `MUSIC` remains geometry-aware because it uses the explicit sensor positions.
- `Root-MUSIC` and `ESPRIT` are not converted to a physical ULA before execution.
- Therefore, the no-LRMC `Root-MUSIC` and `ESPRIT` results remain stress baselines rather than fully geometry-valid ULA-style baselines.

The LRMC branch completes the covariance onto a virtual ULA before classical estimation, which makes `Root-MUSIC` and `ESPRIT` much more methodologically appropriate there.

## Hypotheses
- Toeplitz enforcement may improve the physical consistency of the completed covariance and therefore reduce RMSE.
- If Toeplitz helps, the gain should be most visible for `ESPRIT` and `Root-MUSIC`, which depend strongly on virtual ULA structure.
- If Toeplitz hurts, that would suggest the projection is too restrictive under the current completion noise and coherent-source setting.

## What Counts as a Good Phase 1C Outcome
A useful Phase 1C outcome should answer:
- whether Toeplitz enforcement provides a measurable improvement over the current best LRMC baseline
- whether the effect is consistent across all three methods or only some of them
- whether Toeplitz should become part of the default coherent-signal LRMC recipe

## Phase 1C Files
Template files used for this stage:
- [phase1c_nula_coherent_no_lrmc_t200.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc_toeplitz/phase1c_nula_coherent_no_lrmc_t200.json)
- [phase1c_nula_coherent_lrmc_no_toeplitz_t200.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc_toeplitz/phase1c_nula_coherent_lrmc_no_toeplitz_t200.json)
- [phase1c_nula_coherent_lrmc_toeplitz_t200.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc_toeplitz/phase1c_nula_coherent_lrmc_toeplitz_t200.json)

Canonical Phase 1C launcher:
- [run_phase1_coherent_lrmc_toeplitz.py](f:/workspace1/SubspaceNet/run_phase1_coherent_lrmc_toeplitz.py)

Recommended command:
```bash
python run_phase1_coherent_lrmc_toeplitz.py
```

Expected outputs:
- `results/phase1_coherent_lrmc_toeplitz/summary.csv`
- `results/phase1_coherent_lrmc_toeplitz/phase1_coherent_lrmc_toeplitz_results.md`

## What To Do After Phase 1C
After the Toeplitz results are available, inspect the following before moving to the next stage:
- Does Toeplitz enforcement improve the current best LRMC baseline?
- Is the gain stable across `MUSIC`, `Root-MUSIC`, and `ESPRIT`?
- Should Toeplitz become part of the default coherent-signal LRMC configuration?

If Toeplitz helps, keep it fixed for the next coherent-signal stage:
- solver comparison (`svd` vs `nuclear`)
- initialization comparison
- post-LRMC decorrelation

Only after the best coherent-signal LRMC configuration is identified should SubspaceNet be reintroduced.
