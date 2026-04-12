# Phase 1D LRMC Coherent-Signal Solver Ablation Plan

## Status
This document defines **Phase 1D**, the next coherent-signal LRMC study after the completed Toeplitz ablation in Phase 1C.

Completed before this stage:
- Phase 1A coherent NULA snapshot ablation
- Phase 1B coherent NULA rank ablation
- Phase 1C coherent NULA Toeplitz ablation

Target of this stage:
- compare LRMC solvers under the current best coherent-signal configuration

Not included yet in this stage:
- LRMC initialization comparison
- post-LRMC decorrelation
- SubspaceNet retraining

## Goal
Phase 1D tests whether the choice of LRMC solver materially affects coherent-signal NULA DOA estimation once the stronger structural settings have been fixed.

## Why Solver Comes Next
Phase 1B showed that `rank=3` remains the best rank overall, and Phase 1C showed that Toeplitz enforcement is helpful but not dramatic. With rank and Toeplitz now fixed, the next unresolved question is whether the solver itself limits performance.

The current code supports two solver modes:
- `svd`: alternating low-rank projection
- `nuclear`: convex nuclear-norm completion

If the solver choice matters, that will tell us whether coherent-signal performance is currently limited more by optimization behavior than by model structure alone.

## Phase 1D Design
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
- LRMC initialization: `lag`
- Toeplitz enforcement: `true`
- Methods: `MUSIC`, `Root-MUSIC`, `ESPRIT`

Variables in Phase 1D:
- Baseline: no LRMC
- LRMC solver = `svd`
- LRMC solver = `nuclear`

## Methodological Note
The no-LRMC baseline is still executed directly on the physical NULA.

- `MUSIC` remains geometry-aware because it uses the explicit sensor positions.
- `Root-MUSIC` and `ESPRIT` are not converted to a physical ULA before execution.
- Therefore, the no-LRMC `Root-MUSIC` and `ESPRIT` results remain stress baselines rather than fully geometry-valid ULA-style baselines.

The LRMC branch completes the covariance onto a virtual ULA before classical estimation, which makes `Root-MUSIC` and `ESPRIT` much more methodologically appropriate there.

## Practical Note
The `nuclear` solver path requires `cvxpy` in the active Python environment.

- The main launcher [run_phase1_coherent_lrmc_solver.py](f:/workspace1/SubspaceNet/run_phase1_coherent_lrmc_solver.py) now performs a preflight dependency check and will stop immediately with a clear message if `cvxpy` is missing.
- If you want to run only the currently supported subset without installing `cvxpy`, use [run_phase1_coherent_lrmc_solver_svd_only.py](f:/workspace1/SubspaceNet/run_phase1_coherent_lrmc_solver_svd_only.py).
- The `svd`-only fallback is useful for partial benchmarking, but it does **not** complete the intended Phase 1D solver comparison because the `nuclear` branch is still absent.

## Hypotheses
- The `nuclear` solver may improve the physical consistency of the completed covariance under coherent signals because it optimizes a global low-rank objective.
- The `svd` solver may remain competitive or even better because it is more directly aligned with the chosen rank constraint and may introduce less optimization noise.
- If the solver gap is small, then later improvements should focus on initialization and post-LRMC decorrelation rather than solver choice.

## What Counts as a Good Phase 1D Outcome
A useful Phase 1D outcome should answer:
- whether solver choice produces a meaningful RMSE difference
- whether one solver is consistently better across all three methods
- whether the computational cost of the `nuclear` solver is justified by any accuracy gain

## Phase 1D Files
Template files used for this stage:
- [phase1d_nula_coherent_no_lrmc_t200.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc_solver/phase1d_nula_coherent_no_lrmc_t200.json)
- [phase1d_nula_coherent_lrmc_svd_t200.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc_solver/phase1d_nula_coherent_lrmc_svd_t200.json)
- [phase1d_nula_coherent_lrmc_nuclear_t200.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc_solver/phase1d_nula_coherent_lrmc_nuclear_t200.json)

Canonical Phase 1D launcher:
- [run_phase1_coherent_lrmc_solver.py](f:/workspace1/SubspaceNet/run_phase1_coherent_lrmc_solver.py)

Recommended command:
```bash
python run_phase1_coherent_lrmc_solver.py
```

Expected outputs:
- `results/phase1_coherent_lrmc_solver/summary.csv`
- `results/phase1_coherent_lrmc_solver/phase1_coherent_lrmc_solver_results.md`

## What To Do After Phase 1D
After the solver results are available, inspect the following before moving to the next stage:
- Does `nuclear` outperform `svd` enough to justify its extra cost?
- Is the winning solver stable across `MUSIC`, `Root-MUSIC`, and `ESPRIT`?
- Should the solver now be fixed while moving on to initialization or post-LRMC decorrelation?

If solver sensitivity is weak, keep the simpler solver fixed and move on to:
- initialization comparison
- post-LRMC decorrelation

Only after the best coherent-signal LRMC configuration is identified should SubspaceNet be reintroduced.

## One small heads-up:
the current Toeplitz block inside the nuclear solver is still only a placeholder loop and does not add explicit CVXPY Toeplitz constraints before solve. The code does still project to Toeplitz afterward when enabled, so Phase 1D can run, but if we later want a fully strict convex Toeplitz-constrained formulation, that part should be improved.

head-up have been fixed.
