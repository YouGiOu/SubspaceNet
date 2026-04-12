# Phase 1F LRMC Coherent-Signal Post-Processing Ablation Plan

## Status
This document defines **Phase 1F**, the next coherent-signal LRMC study after the completed initialization ablation in Phase 1E.

Completed before this stage:
- Phase 1A coherent NULA snapshot ablation
- Phase 1B coherent NULA rank ablation
- Phase 1C coherent NULA Toeplitz ablation
- Phase 1D coherent NULA solver ablation
- Phase 1E coherent NULA initialization ablation

Target of this stage:
- compare post-LRMC decorrelation strategies under the current best coherent-signal configuration

Not included yet in this stage:
- SubspaceNet retraining

## Goal
Phase 1F tests whether additional post-LRMC covariance processing improves coherent-signal NULA DOA estimation after rank, Toeplitz, solver, and initialization have already been fixed.

## Why Post-Processing Comes Next
Earlier stages established a stable default LRMC configuration:
- `rank = 3`
- `toeplitz = true`
- `solver = svd`
- `init = lag`

The remaining coherent-signal question is whether covariance completion alone is enough, or whether a dedicated decorrelation step after LRMC can further improve subspace separation.

## Phase 1F Design
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
- Toeplitz enforcement: `true`
- Methods: `MUSIC`, `Root-MUSIC`, `ESPRIT`

Variables in Phase 1F:
- Baseline: no LRMC
- LRMC with no post-processing
- LRMC + forward-backward averaging (`fba`)
- LRMC + spatial smoothing (`ss`)
- LRMC + forward-backward averaging + spatial smoothing (`fba+ss`)

## Methodological Note
The no-LRMC baseline is still executed directly on the physical NULA.

- `MUSIC` remains geometry-aware because it uses the explicit sensor positions.
- `Root-MUSIC` and `ESPRIT` are not converted to a physical ULA before execution.
- Therefore, the no-LRMC `Root-MUSIC` and `ESPRIT` results remain stress baselines rather than fully geometry-valid ULA-style baselines.

The LRMC branch completes the covariance onto a virtual ULA before classical estimation. In this phase, optional decorrelation is then applied on the completed covariance:
- `fba`: forward-backward averaging
- `ss`: spatial smoothing via averaged overlapping virtual subarrays
- `fba+ss`: apply forward-backward averaging first, then spatial smoothing

When spatial smoothing is used, the effective virtual ULA dimension is reduced to the subarray size used by the smoothing step.

## Hypotheses
- Forward-backward averaging may improve robustness by reinforcing conjugate symmetry in the completed covariance.
- Spatial smoothing may help coherent-source separation more directly, because it is a classical decorrelation mechanism.
- The combined `fba+ss` setting may outperform either method alone if the two effects are complementary.
- If post-processing gains are weak, then LRMC completion itself may already be the dominant improvement mechanism.

## What Counts as a Good Phase 1F Outcome
A useful Phase 1F outcome should answer:
- whether post-LRMC decorrelation improves over the current best LRMC baseline
- whether the gain is consistent across all three methods
- whether one post-processing strategy should become part of the default coherent-signal LRMC pipeline

## Phase 1F Files
Template files used for this stage:
- [phase1f_nula_coherent_no_lrmc_t200.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc_postprocess/phase1f_nula_coherent_no_lrmc_t200.json)
- [phase1f_nula_coherent_lrmc_none_t200.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc_postprocess/phase1f_nula_coherent_lrmc_none_t200.json)
- [phase1f_nula_coherent_lrmc_fba_t200.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc_postprocess/phase1f_nula_coherent_lrmc_fba_t200.json)
- [phase1f_nula_coherent_lrmc_ss_t200.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc_postprocess/phase1f_nula_coherent_lrmc_ss_t200.json)
- [phase1f_nula_coherent_lrmc_fba_ss_t200.json](f:/workspace1/SubspaceNet/data/dataset_templates/ablation/phase1_coherent_lrmc_postprocess/phase1f_nula_coherent_lrmc_fba_ss_t200.json)

Canonical Phase 1F launcher:
- [run_phase1_coherent_lrmc_postprocess.py](f:/workspace1/SubspaceNet/run_phase1_coherent_lrmc_postprocess.py)

Recommended command:
```bash
python run_phase1_coherent_lrmc_postprocess.py
```

Expected outputs:
- `results/phase1_coherent_lrmc_postprocess/summary.csv`
- `results/phase1_coherent_lrmc_postprocess/phase1_coherent_lrmc_postprocess_results.md`

## What To Do After Phase 1F
After the post-processing results are available, inspect the following before moving to the next stage:
- Does post-LRMC decorrelation improve the current best LRMC baseline?
- Is one strategy clearly best: `fba`, `ss`, or `fba+ss`?
- Is the gain large enough to make post-processing part of the default coherent-signal pipeline?

After this stage, the coherent-signal LRMC configuration should be stable enough to justify reintroducing SubspaceNet.
