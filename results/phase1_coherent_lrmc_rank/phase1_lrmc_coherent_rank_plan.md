# Phase 1B LRMC Coherent-Signal Rank Ablation Plan

## Status
This document defines **Phase 1B**, the next coherent-signal LRMC study after the completed snapshot ablation in Phase 1A.

Completed before this stage:
- Phase 1A coherent NULA snapshot ablation

Target of this stage:
- LRMC rank sensitivity under the strongest snapshot setting from Phase 1A

Not included yet in this stage:
- LRMC solver comparison (`svd` vs `nuclear`)
- LRMC initialization comparison
- Toeplitz enforcement ablation
- post-LRMC decorrelation
- SubspaceNet retraining

## Goal
Phase 1B tests whether the default LRMC rank choice `rank=3` is actually optimal for coherent-signal NULA processing, or whether a lower or higher rank produces better downstream DOA estimation.

## Why Rank Comes Next
Phase 1A showed that default LRMC clearly helps coherent NULA estimation and that the strongest setting in that sweep was around `T=200`. The next most important unresolved question is whether the current rank assumption is well matched to the coherent-signal covariance structure.

Because LRMC rank directly controls the complexity of the recovered virtual covariance, it is the cleanest next hyperparameter to study before moving on to solver choice or structural constraints.

## Phase 1B Design
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
- LRMC solver: `svd`
- LRMC initialization: `lag`
- Toeplitz enforcement: `false`
- Methods: `MUSIC`, `Root-MUSIC`, `ESPRIT`

Variables in Phase 1B:
- Baseline: no LRMC
- LRMC rank: `2, 3, 4, 5`

## Methodological Note
The no-LRMC baseline is still executed directly on the physical NULA.

- `MUSIC` remains geometry-aware because it uses the explicit sensor positions.
- `Root-MUSIC` and `ESPRIT` are not converted to a physical ULA before execution.
- Therefore, the no-LRMC `Root-MUSIC` and `ESPRIT` results remain stress baselines rather than fully geometry-valid ULA-style baselines.

The LRMC branch completes the covariance onto a virtual ULA before classical estimation, which makes `Root-MUSIC` and `ESPRIT` much more methodologically appropriate there.

## Hypotheses
- `rank=3` may remain competitive, but coherent signals could benefit from a slightly different rank because the effective covariance structure is sensitive to source correlation and completion bias.
- If `rank=2` performs best, the current default may be over-parameterized.
- If `rank=4` or `5` performs best, the current default may be too restrictive.
- ESPRIT is expected to remain the strongest readout, but the best rank may differ by method.

## What Counts as a Good Phase 1B Outcome
A useful Phase 1B outcome should answer:
- whether `rank=3` is actually near-optimal
- whether the best rank is stable across `MUSIC`, `Root-MUSIC`, and `ESPRIT`
- whether changing rank produces a meaningful enough gain to justify making it a tuned hyperparameter

## Phase 1B Files
Template files used for this stage:
- [phase1b_nula_coherent_no_lrmc_t200.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc_rank/phase1b_nula_coherent_no_lrmc_t200.json)
- [phase1b_nula_coherent_lrmc_rank2_t200.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc_rank/phase1b_nula_coherent_lrmc_rank2_t200.json)
- [phase1b_nula_coherent_lrmc_rank3_t200.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc_rank/phase1b_nula_coherent_lrmc_rank3_t200.json)
- [phase1b_nula_coherent_lrmc_rank4_t200.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc_rank/phase1b_nula_coherent_lrmc_rank4_t200.json)
- [phase1b_nula_coherent_lrmc_rank5_t200.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc_rank/phase1b_nula_coherent_lrmc_rank5_t200.json)

Canonical Phase 1B launcher:
- [run_phase1_coherent_lrmc_rank.py](f:/workspace1/SubspaceNet/run_phase1_coherent_lrmc_rank.py)

Recommended command:
```bash
python run_phase1_coherent_lrmc_rank.py
```

Expected outputs:
- `results/phase1_coherent_lrmc_rank/summary.csv`
- `results/phase1_coherent_lrmc_rank/phase1_coherent_lrmc_rank_results.md`

## What To Do After Phase 1B
After the rank results are available, inspect the following before moving to the next stage:
- Does one rank dominate across all three methods?
- Is `rank=3` still a good default?
- Is the best rank gain large enough to justify tuning in later experiments?

If rank sensitivity is strong, keep the best rank fixed for the next coherent-signal study:
- Toeplitz enforcement ablation
- solver comparison (`svd` vs `nuclear`)
- initialization comparison
- post-LRMC decorrelation

Only after the best coherent-signal LRMC configuration is identified should SubspaceNet be reintroduced.
