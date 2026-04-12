# Phase 1A LRMC Coherent-Signal Snapshot Ablation Plan

## Status
This document now refers specifically to **Phase 1A**, the completed **snapshot ablation** only.

Completed in this stage:
- coherent NULA classical-method comparison
- snapshot sweep `T in {50, 100, 200, 400}`
- no-LRMC baseline versus default LRMC

Not completed yet in this stage:
- LRMC rank sweep
- LRMC solver comparison (`svd` vs `nuclear`)
- LRMC initialization comparison
- Toeplitz enforcement ablation
- post-LRMC decorrelation such as spatial smoothing or forward-backward averaging
- any SubspaceNet retraining based on the tuned LRMC settings

## Goal
Phase 1A isolates the effect of default LRMC on coherent-source DOA estimation for the NULA `[0, 1, 4, 8]` before any SubspaceNet training. The purpose is to determine whether LRMC consistently improves classical subspace methods and how that benefit changes with snapshot count.

## Why Phase 1A Comes First
Training SubspaceNet for every LRMC setting would make the study expensive and blur the source of any gain. A classical-only first stage gives a cleaner answer to three questions:
- Does LRMC help coherent NULA estimation at all?
- Is the benefit stable across snapshot counts?
- Which classical readout benefits most: MUSIC, Root-MUSIC, or ESPRIT?

## Phase 1A Design
Fixed conditions:
- Array: NULA `[0, 1, 4, 8]` on a `0.5 lambda` grid
- Sources: `M = 2`, coherent, narrowband
- SNR: `10 dB`
- DOA range: `[-90 deg, 90 deg]`
- Minimum source separation: `15 deg`
- Seed: fixed at `42`
- Dataset size: `4096` generated training-side samples and `0.2` test ratio
- Methods: `MUSIC`, `Root-MUSIC`, `ESPRIT`

Variables in Phase 1A:
- Snapshots: `T in {50, 100, 200, 400}`
- LRMC usage:
  - No LRMC baseline
  - Default LRMC with `rank=3`, `solver=svd`, `init=lag`, `toeplitz=false`

## Methodological Note
The no-LRMC baselines were executed on the physical NULA `[0, 1, 4, 8]` directly.

- `MUSIC` uses the explicit array geometry through the steering-vector calculation, so it remains geometry-aware on the NULA.
- `Root-MUSIC` and `ESPRIT` in this codebase were **not** converted or degraded to a 4-element ULA before execution.
- Therefore, the no-LRMC `Root-MUSIC` and `ESPRIT` runs should be interpreted as applying ULA-oriented subspace machinery directly to a NULA covariance, which is not a fully geometry-valid use of those algorithms.

This is intentional for Phase 1A: the purpose is to compare the weak direct-NULA baseline against the LRMC path that lifts the NULA covariance into a virtual ULA. Under LRMC, `Root-MUSIC` and `ESPRIT` become much more methodologically appropriate because they operate on the completed virtual ULA covariance rather than on the raw sparse-array covariance.

## Phase 1A Files
Template files used for this completed stage:
- [phase1_nula_coherent_no_lrmc_t50.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc/phase1_nula_coherent_no_lrmc_t50.json)
- [phase1_nula_coherent_lrmc_t50.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc/phase1_nula_coherent_lrmc_t50.json)
- [phase1_nula_coherent_no_lrmc_t100.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc/phase1_nula_coherent_no_lrmc_t100.json)
- [phase1_nula_coherent_lrmc_t100.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc/phase1_nula_coherent_lrmc_t100.json)
- [phase1_nula_coherent_no_lrmc_t200.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc/phase1_nula_coherent_no_lrmc_t200.json)
- [phase1_nula_coherent_lrmc_t200.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc/phase1_nula_coherent_lrmc_t200.json)
- [phase1_nula_coherent_no_lrmc_t400.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc/phase1_nula_coherent_no_lrmc_t400.json)
- [phase1_nula_coherent_lrmc_t400.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc/phase1_nula_coherent_lrmc_t400.json)

Canonical Phase 1A launcher:
- [run_phase1_coherent_lrmc_snapshot.py](f:/workspace1/SubspaceNet/run_phase1_coherent_lrmc_snapshot.py)

Legacy compatibility launcher:
- [run_phase1_coherent_lrmc.py](f:/workspace1/SubspaceNet/run_phase1_coherent_lrmc.py)

Recommended command:
```bash
python run_phase1_coherent_lrmc_snapshot.py
```

Expected outputs:
- `results/phase1_coherent_lrmc_snapshot/summary.csv`
- `results/phase1_coherent_lrmc_snapshot/phase1_coherent_lrmc_snapshot_results.md`

## Hypotheses
- LRMC should improve coherent NULA estimation over the no-LRMC baseline, especially when snapshots are limited.
- The benefit of LRMC may shrink as `T` grows because the sample covariance itself becomes more reliable.
- ESPRIT may remain the strongest readout after LRMC, but MUSIC and Root-MUSIC may respond differently to reconstruction artifacts.

## What Counts as a Good Phase 1A Outcome
A useful Phase 1A outcome is not only the best RMSE value. The main decision signal is the pattern:
- whether LRMC improves all three classical methods or only some of them
- whether the gain is strongest at low `T`
- whether the best classical method is stable across `T`

## What To Do After Phase 1A
After the snapshot results are available, inspect the following before moving to the next stage:
- Which snapshot regime benefits most from LRMC?
- Is `rank=3` plausible as a default, or does the pattern suggest underfitting or overfitting?
- Is the coherent-case bottleneck mainly covariance completion, or is an additional decorrelation step likely needed?

If LRMC clearly helps, the next coherent-signal stage should tune LRMC itself:
- `rank`
- `solver` (`svd` vs `nuclear`)
- `initialization`
- `Toeplitz enforcement`
- possible post-LRMC decorrelation such as spatial smoothing or forward-backward averaging

Only after the best classical LRMC configuration is identified should SubspaceNet be reintroduced.
