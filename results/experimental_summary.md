# Experimental Summary

This document is the current handoff summary for the SubspaceNet / LRMC / subspace-method experiment workflow in this repo.

It serves two purposes:
- summarize the experimental conclusions reached so far
- document the current experiment-writing style and code conventions so later AI agents can continue the work consistently

If you are reading this as a new agent, treat this file as the current project state before adding new experiments or changing code.

## 1. Current Big Picture

The project has evolved from simple 1D sparse-NULA LRMC checks into a structured workflow covering:
- 1D coherent and non-coherent NULA controls
- 2D row-replicated hardware-style geometries
- geometry-shape ablations for Groups A, B, and C
- coherent and non-coherent classical baselines
- large-sample SubspaceNet training on the actual Group B `1.9 lambda` hardware geometry
- low-snapshot and ultra-low-snapshot classical boundary studies

The current best-supported conclusions are:
- spacing matters, but it is not the only factor
- source coherence matters a lot
- geometry modeling accuracy matters a lot, especially for LRMC
- Group B `1.9 lambda` is viable once the row geometry is modeled correctly
- the classical `SS -> LRMC` front end is the main canonical preprocessing path for Group B studies
- SubspaceNet-ESPRIT is currently the most promising learned head
- differentiable Root-MUSIC remains fragile

## 2. Core Experimental Workflow

### 2.1 Default pattern for new experiments

When adding a new experiment family, the current repo workflow is:

1. create a dedicated launcher at repo root
2. create a dedicated template directory under:
   - `data/dataset_templates/ablation/...`
3. create exactly one experiment-plan document under:
   - `results/<experiment_family>/..._experiment_plan.md`
4. run through `run_ablation.py`
5. let `run_ablation.py` generate:
   - `summary.csv`
   - the family markdown results file
   - per-method `metrics.json`

Important user preference:
- for pure experiment sweeps, add only an experiment plan
- do not add an implementation-plan document unless a new algorithm or new processing code is being introduced

### 2.2 Naming conventions

Current naming style is:
- launchers:
  - `run_phaseX_...py`
- template names:
  - embedded directly in JSON as `template_name`
- results folders:
  - `results/<family_name>/...`
- results markdown:
  - usually `<family_name>_results.md`
- plan docs:
  - usually `<family_name>_experiment_plan.md`

When coherent / non-coherent are both present, include that in names explicitly.

### 2.3 Template style

The current template schema uses:
- `experiment_type`
- `methods`
- `commands`
- `system_model`
- `model`
- `dataset`
- `report`
- `description`
- `template_name`

For classical experiments, the most important fields are:
- `system_model.signal_nature`
- `system_model.T`
- `system_model.array_spacing`
- `system_model.geometry_name`
- `system_model.sensor_positions`
- `system_model.row_groups`
- `system_model.canonical_row_group`
- `system_model.virtual_array_size`
- `system_model.covariance_mode`
- `system_model.use_lrmc`
- `system_model.lrmc_*`
- `system_model.doa_min`, `doa_max`
- `system_model.elevation_min`, `elevation_max`
- `system_model.min_doa_gap`

Newer dataset-generation control:
- `system_model.fixed_doa_gap`
  - if present, dataset generation uses an exact azimuth separation instead of only enforcing a minimum separation

### 2.4 Current canonical classical front end

For Group B hardware studies, the default classical front end is:
- `covariance_mode = "ss_then_lrmc"`
- meaning:
  - row-wise spatial smoothing first
  - then LRMC onto the virtual ULA

This is the path used for:
- most recent Group B classical baselines
- low-snapshot boundary studies
- the current SubspaceNet Group B training templates

## 3. Geometry Conventions

### 3.1 Group definitions

The project now uses these 2D geometry labels:

- Group A:
  - rectangular row-stacked geometry
  - row pattern `[0, 1, 4, 8]`
- Group B:
  - slanted / hardware geometry
  - row pattern `[0, 4, 7, 8]`
- Group C:
  - rectangular control geometry
  - row pattern `[0, 4, 7, 8]`

### 3.2 Very important implementation note

The Group B LRMC path was previously wrong because rowwise LRMC was effectively still using the old `[0, 1, 4, 8]` row model.

This has been fixed.

Current rule:
- for 2D row-replicated arrays, row geometry must be derived from the actual physical x-coordinates
- do not assume the nominal template row pattern unless it really matches the physical row

This fix lives in:
- [src/methods.py](/f:/workspace1/SubspaceNet/src/methods.py)

### 3.3 Current 2D limitation

The current 2D classical pipeline is still not a true 2D DOA estimator.

It works like this:
- 2D snapshots are generated using the physical 2D geometry
- then the data are reduced into a row-based 1D surrogate
- classical methods run on the reduced row model or LRMC-completed virtual ULA

So the current 2D studies should be interpreted as:
- 2D data generation
- 1D surrogate estimation

This is a known structural limitation.

## 4. Phase 3: 1D Spacing Scan

Reference file:
- [phase3_1d_spacing_scan_results.md](/f:/workspace1/SubspaceNet/results/phase3_1d_spacing_scan/phase3_1d_spacing_scan_results.md)

This is still one of the key control experiments.

### Result

| Spacing | MUSIC baseline | MUSIC + LRMC | Root-MUSIC baseline | Root-MUSIC + LRMC | ESPRIT baseline | ESPRIT + LRMC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.5 lambda | 26.59 | 10.55 | 32.08 | 9.62 | 31.60 | 9.73 |
| 1.0 lambda | 30.38 | 31.08 | 29.06 | 23.83 | 29.08 | 24.01 |
| 1.9 lambda | 38.52 | 38.91 | 32.26 | 28.58 | 32.36 | 28.49 |

### Interpretation

- `0.5 lambda` is the most favorable coherent 1D sparse-NULA regime for LRMC
- `1.0 lambda` already weakens LRMC significantly
- in the coherent 1D setup, `1.9 lambda` largely destroys the benefit of LRMC

This experiment was important because it initially suggested spacing was the dominant problem.

Later experiments showed the full story is more nuanced:
- spacing matters
- coherence matters
- geometry/topology matters
- estimator choice matters

## 5. Group B 1.9 Lambda Classical Conclusions

After the geometry fixes and the coherent/non-coherent 2D studies, the project has converged on these practical interpretations for Group B:

### Coherent Group B `1.9 lambda`

- classical Group B is workable
- `SS -> LRMC` is the main baseline path
- coherent errors are typically around the low-single-degree range in the better classical runs
- in the hardest tested coherent regime (`1 deg`, `1 dB`), classical performance remains poor even with `SS -> LRMC`, and additional snapshots help only modestly for the classical controls
- in that same hard coherent regime, `SS -> LRMC -> SubspaceNet -> ESPRIT` improves strongly as snapshots increase and remains far better than the classical controls even at very low `T`
- in Phase 7B Phase 1.1, a first learned SS-fusion model that fuses the three `SS(2/3)` LRMC branches slightly beat both the current `SS(3/3)` learned baseline and the best fixed `SS(2/3: rows 0+1)` learned baseline in the primary hard coherent cell
- in Phase 7B Phase 1.1.1, a safer `1x1` channel-only SS-fusion variant still beat the two fixed learned baselines, but it did not beat the earlier spatial-fusion Phase 1.1 model
- this regime is hard enough that learned methods can still matter

### Non-coherent Group B `1.9 lambda`

- classical Group B becomes much easier
- MUSIC becomes almost trivial in many settings
- Root-MUSIC / ESPRIT become very strong after LRMC-based preprocessing
- in the non-coherent fixed-gap / SNR grid, angular separation is not the dominant failure axis once SNR is moderate; even `1 deg` becomes highly workable for classical MUSIC / Root-MUSIC / ESPRIT
- unlike the coherent case, raw non-coherent MUSIC is already very strong at moderate SNR even without `SS -> LRMC`, while raw Root-MUSIC / ESPRIT still collapse and depend heavily on preprocessing
- `SS -> LRMC` remains important in the non-coherent regime mainly because it rescues Root-MUSIC / ESPRIT and stabilizes the `1 deg`, low-SNR corner, not because non-coherent MUSIC uniformly requires it
- in the hardest tested non-coherent regime (`1 deg`, `1 dB`), the classical pipeline also degrades badly at low snapshots, but `SS -> LRMC -> SubspaceNet -> ESPRIT` still stays clearly better and approaches sub-degree accuracy once snapshots become moderate
- this regime is easier than the coherent one, but still useful for testing whether learned heads stabilize

## 6. Phase 4A: Large-Sample Coherent SubspaceNet on Group B 1.9 Lambda

Reference file:
- [phase4_subspacenet_groupb_1p9_coherent_large_results.md](/f:/workspace1/SubspaceNet/results/phase4_subspacenet_groupb_1p9_coherent_large/phase4_subspacenet_groupb_1p9_coherent_large_results.md)

### Result

- SubspaceNet-ESPRIT: about `0.96 deg`
- SubspaceNet-Root-MUSIC: about `5.67 deg`

### Interpretation

- ESPRIT training succeeded and clearly beat the comparable classical coherent Group B baseline
- Root-MUSIC training was unstable and under-performed badly
- the Root-MUSIC loss curve oscillated heavily
- the ESPRIT loss curve was smooth and healthy

Current working interpretation:
- SubspaceNet-ESPRIT is the main viable learned path
- differentiable Root-MUSIC is still structurally fragile in this repo

## 7. Phase 4B: Large-Sample Non-Coherent SubspaceNet on Group B 1.9 Lambda

Reference files:
- [phase4_subspacenet_groupb_1p9_noncoherent_large_experiment_plan.md](/f:/workspace1/SubspaceNet/results/phase4_subspacenet_groupb_1p9_noncoherent_large/phase4_subspacenet_groupb_1p9_noncoherent_large_experiment_plan.md)
- [esprit metrics.json](/f:/workspace1/SubspaceNet/results/phase4_subspacenet_groupb_1p9_noncoherent_large/phase4b_groupb_1p9_noncoherent_subspacenet_45k/esprit/metrics.json)

### Status

This run was started, but Root-MUSIC did not converge well and was stopped early by the user.

As a result:
- no family-level `results.md` was generated
- no family-level `summary.csv` was generated
- the ESPRIT branch completed and produced metrics
- the Root-MUSIC branch should currently be treated as incomplete / aborted

### Available result

From the completed ESPRIT branch:
- SubspaceNet-ESPRIT RMSE: about `0.2604 deg`

### Interpretation

- non-coherent large-sample SubspaceNet-ESPRIT is very strong
- it is markedly better than the coherent learned ESPRIT result
- the non-coherent regime is substantially easier for the learned model as well as for the classical pipeline
- Root-MUSIC still appears unreliable enough that it should not currently be treated as a stable learned head

## 8. Phase 5: Group B 1.9 Lambda Snapshot Boundary

Reference file:
- [phase5_groupb_1p9_snapshot_boundary_results.md](/f:/workspace1/SubspaceNet/results/phase5_groupb_1p9_snapshot_boundary/phase5_groupb_1p9_snapshot_boundary_results.md)

This sweep covered:
- coherent and non-coherent
- `T = 10, 25, 50, 100, 200`
- Group B `1.9 lambda`
- `SS -> LRMC`

### Main conclusion

In that range, there was no strong low-snapshot collapse:
- coherent performance was surprisingly flat
- non-coherent performance degraded smoothly but remained strong

This motivated a deeper ultra-low-snapshot follow-up.

## 9. Phase 5B: Ultra-Low Snapshot Boundary

Reference file:
- [phase5b_groupb_1p9_ultralow_snapshot_boundary_results.md](/f:/workspace1/SubspaceNet/results/phase5b_groupb_1p9_ultralow_snapshot_boundary/phase5b_groupb_1p9_ultralow_snapshot_boundary_results.md)

This sweep covered:
- coherent and non-coherent
- `T = 1, 2, 4, 6, 8, 10`
- Group B `1.9 lambda`
- `SS -> LRMC`

### Coherent trend

Coherent performance remains surprisingly stable even down to `T = 1`:
- roughly `1.7 deg` to `2.0 deg` across methods over the full `T = 1..10` range

Representative values:
- `T = 1`: about `1.91 - 1.96 deg`
- `T = 10`: about `1.73 - 1.82 deg`

### Non-coherent trend

Non-coherent performance now shows the expected low-snapshot breakdown:
- `T = 10`: about `0.76 - 0.88 deg`
- `T = 8`: about `0.76 - 0.82 deg`
- `T = 6`: about `1.01 - 1.13 deg`
- `T = 4`: about `1.23 - 1.27 deg`
- `T = 2`: about `1.88 - 1.94 deg`
- `T = 1`: about `3.32 - 3.37 deg`

### Interpretation

This was an important correction to the earlier intuition:
- coherent Group B is not primarily snapshot-limited in this ultra-low range
- non-coherent Group B does have a real ultra-low-snapshot boundary
- if future low-snapshot SubspaceNet training is pursued, the low-`T` non-coherent regime is now a meaningful target too

### Important implementation fix discovered here

The ultra-low-snapshot experiments initially failed because:
- `np.cov(X)` was still being used in classical covariance construction
- this is not appropriate at `T = 1`

This was fixed by switching those paths to the repo's own:
- `(1/T) X X^H` sample covariance implementation

And LRMC covariance inputs are now Hermitian-projected more defensively.

Relevant files:
- [src/methods.py](/f:/workspace1/SubspaceNet/src/methods.py)
- [src/lrmc.py](/f:/workspace1/SubspaceNet/src/lrmc.py)

## 10. Phase 5C: Fixed Angular-Separation Sweep

Reference files:
- [run_phase5c_groupb_1p9_fixed_separation_sweep.py](/f:/workspace1/SubspaceNet/run_phase5c_groupb_1p9_fixed_separation_sweep.py)
- [phase5c_groupb_1p9_fixed_separation_sweep_experiment_plan.md](/f:/workspace1/SubspaceNet/results/phase5c_groupb_1p9_fixed_separation_sweep/phase5c_groupb_1p9_fixed_separation_sweep_experiment_plan.md)
- [phase5c_groupb_1p9_fixed_separation_sweep_results.md](/f:/workspace1/SubspaceNet/results/phase5c_groupb_1p9_fixed_separation_sweep/phase5c_groupb_1p9_fixed_separation_sweep_results.md)

This sweep covered:
- coherent and non-coherent
- fixed azimuth separations `5, 4, 3, 2, 1 deg`
- Group B `1.9 lambda`
- `SS -> LRMC`
- `T = 200`

### Coherent trend

The coherent Group B pipeline is highly sensitive to angular separation, and this axis is much more revealing than the earlier snapshot sweeps.

Representative values:
- `5 deg`: about `1.03 - 1.16 deg`
- `4 deg`: about `0.10 - 0.14 deg`
- `3 deg`: about `1.38 - 1.59 deg`
- `2 deg`: about `3.75 - 4.30 deg`
- `1 deg`: about `5.22 - 6.39 deg`

Interpretation:
- coherent Group B remains strong down to around `3 - 5 deg`
- performance begins to degrade sharply at `2 deg`
- `1 deg` is a clear classical failure regime for coherent signals

The `4 deg` point is unusually strong relative to `5 deg` and `3 deg`, so it should be treated as a good empirical result rather than a strict monotonic law. The broader pattern is still clear: coherent performance breaks down rapidly below about `3 deg`.

### Non-coherent trend

The non-coherent Group B pipeline is extremely robust to angular separation in this tested range.

Representative values:
- `5 deg`: about `0.092 - 0.094 deg`
- `4 deg`: about `0.093 - 0.095 deg`
- `3 deg`: about `0.095 - 0.098 deg`
- `2 deg`: about `0.098 - 0.116 deg`
- `1 deg`: about `0.101 - 0.108 deg` for ESPRIT / Root-MUSIC, `0.329 deg` for MUSIC

Interpretation:
- non-coherent Root-MUSIC and ESPRIT remain essentially stable even down to `1 deg`
- non-coherent MUSIC degrades somewhat at `1 deg`, but still stays much better than the coherent case
- for Group B, angular separation is mainly a coherent-signal bottleneck, not a non-coherent one

### Boundary conclusion

Phase 5C provides one of the clearest current training-boundary signals in the repo:
- low snapshot count was not the main coherent failure axis
- small angular separation is a much stronger coherent failure axis

So if future SubspaceNet training is meant to target a classical weakness, the most meaningful next regimes are:
- coherent Group B with very small separation, especially `1 - 2 deg`
- or combined hard regimes such as small separation plus low snapshots

Important new template option added for this:
- `fixed_doa_gap`

This allows dataset generation to enforce exact azimuth separations like:
- `5 deg`, `4 deg`, `3 deg`, `2 deg`, `1 deg`

instead of only enforcing a minimum gap.

Relevant files:
- [src/system_model.py](/f:/workspace1/SubspaceNet/src/system_model.py)
- [src/data_handler.py](/f:/workspace1/SubspaceNet/src/data_handler.py)
- [src/signal_creation.py](/f:/workspace1/SubspaceNet/src/signal_creation.py)

## 11. Current Training Workflow for SubspaceNet

### Current preferred learned target

At the moment, the main practical learned target is:
- Group B
- `1.9 lambda`
- SubspaceNet-ESPRIT

The current most promising architectural extension beyond the standard learned target is now:
- learned SS-fusion on top of the Group B `SS(2/3)` LRMC branch family

The first hard-cell fusion results are encouraging, but they should still be treated as early targeted successes rather than a fully validated replacement for the standard pipeline.

Current interpretation of the learned SS-fusion variants:
- spatial-fusion Phase `1.1` is the strongest result so far in the primary hard coherent cell
- `1x1` channel-only fusion Phase `1.1.1` still improves over the two fixed learned baselines, which suggests adaptive branch fusion itself is useful
- however, the current `1x1` restriction loses some of the gain seen in the spatial-fusion model, so channel-only fusion should presently be treated as a useful structural ablation rather than the new preferred learned-fusion default

Current interpretation after the Phase 7C backbone ablation:
- enlarging the SubspaceNet backbone kernel from `2x2` to `3x3` improved every tested learned variant in the primary coherent hard cell
- the biggest absolute gain was on the weaker fixed baseline `SS(2/3: rows 0+1)`, which improved from about `0.6995 deg` to about `0.5386 deg`
- the standard `SS(3/3) -> LRMC -> SubspaceNet -> ESPRIT` path improved from about `0.4747 deg` to about `0.4087 deg`
- the spatial learned-fusion path also improved from about `0.4516 deg` to about `0.4118 deg`, but after the backbone change it no longer clearly beats the plain `SS(3/3)` baseline
- in this hard cell, the current best single result is therefore the plain `SS(3/3)` learned baseline with the `3x3` backbone, while the spatial-fusion `3x3` model remains a very close second
- current working interpretation: local receptive-field size inside the SubspaceNet backbone matters enough that some of the earlier apparent fusion advantage was at least partly backbone-limited

Current interpretation after the Phase 7D activation ablation:
- replacing the spatial fusion block's plain `ReLU` with a width-controlled anti-rectifier improved the `3x3` spatial-fusion model from about `0.4118 deg` to about `0.3592 deg`
- this new anti-rectifier fusion result now beats both the earlier ReLU spatial-fusion `3x3` model and the plain `SS(3/3)` `3x3` baseline at about `0.4087 deg`
- the gain is large enough that it is unlikely to be explained as noise in this context, especially because the comparison was intentionally kept width-controlled rather than allowing a naive doubled-width anti-rectifier expansion
- current working interpretation: sign-preserving activation inside the covariance-fusion block matters materially in this hard coherent regime, and the earlier Phase 7C result was limited not only by backbone receptive field but also by information loss inside the ReLU-based fusion block
- current best single learned result in the primary coherent hard cell is now the width-controlled anti-rectifier spatial-fusion model with the `3x3` backbone

### Current paper-scale training configuration

The large-sample runs use:
- `45,000` samples
- cached dataset reuse
- accelerated batching / DataLoader settings

### Current training optimizations already implemented

The repo already includes:
- configurable validation batch size
- configurable DataLoader workers
- `pin_memory`
- `persistent_workers`
- non-blocking GPU transfers
- `optimizer.zero_grad(set_to_none=True)`
- dataset cache reuse in `run_ablation.py`

### Current SubspaceNet backbone definitions for paper diagrams

For the current Group B `1.9 lambda` learned runs, the SubspaceNet backbone takes the LRMC-completed virtual covariance and converts it into a `tau`-slice real/imaginary tensor with shape:
- input to the backbone: `[B, tau, 2N_v, N_v]`
- in the current paper-scale Group B setup:
  - `tau = 8`
  - `N_v = 9`
  - so the actual input tensor is `[B, 8, 18, 9]`

Shared structure of both backbone variants:
- three encoder convolutions
- after each convolution, an anti-rectifier block concatenates `ReLU(x)` and `ReLU(-x)`, which doubles the channel count
- two decoder transposed convolutions, each again followed by anti-rectification
- one dropout layer with rate `0.2`
- one final transposed convolution to reconstruct a single-channel tensor
- no pooling
- no batch normalization
- no padding and stride `1` throughout

Shared channel flow:
- input: `tau`
- `conv1`: `tau -> 16`
- anti-rectifier: `16 -> 32`
- `conv2`: `32 -> 32`
- anti-rectifier: `32 -> 64`
- `conv3`: `64 -> 64`
- anti-rectifier: `64 -> 128`
- `deconv2`: `128 -> 32`
- anti-rectifier: `32 -> 64`
- `deconv3`: `64 -> 16`
- anti-rectifier: `16 -> 32`
- dropout: `32 -> 32`
- `deconv4`: `32 -> 1`

After the final reconstruction:
- output tensor shape is `[B, 1, 2N_v, N_v]`
- it is reshaped to `[B, 2N_v, N_v]`
- the first `N_v` rows are interpreted as the real part and the last `N_v` rows as the imaginary part
- these are combined into a complex surrogate covariance `Rz` with shape `[B, N_v, N_v]`
- `Rz` is then passed to the differentiable subspace head, which is ESPRIT in the current preferred learned path

#### `2x2` backbone

This is the default historical backbone used by the main SubspaceNet and Phase 7B learned-fusion baselines.

Layer-by-layer shape flow in the current Group B setup (`[B, 8, 18, 9]` input):
- input: `[B, 8, 18, 9]`
- `conv1(k=2)`: `[B, 16, 17, 8]`
- anti-rectifier: `[B, 32, 17, 8]`
- `conv2(k=2)`: `[B, 32, 16, 7]`
- anti-rectifier: `[B, 64, 16, 7]`
- `conv3(k=2)`: `[B, 64, 15, 6]`
- anti-rectifier: `[B, 128, 15, 6]`
- `deconv2(k=2)`: `[B, 32, 16, 7]`
- anti-rectifier: `[B, 64, 16, 7]`
- `deconv3(k=2)`: `[B, 16, 17, 8]`
- anti-rectifier: `[B, 32, 17, 8]`
- dropout: `[B, 32, 17, 8]`
- `deconv4(k=2)`: `[B, 1, 18, 9]`
- reshape / split real-imag: `[B, 18, 9] -> [B, 9, 9] + [B, 9, 9] -> Rz [B, 9, 9]`

Interpretation:
- the `2x2` backbone is the less aggressive local-coupling version
- it shrinks the spatial support more gradually
- in the current `18 x 9` input setting, its bottleneck feature map is `15 x 6`

#### `3x3` backbone

This is the Phase 7C backbone ablation, where the channel plan is unchanged and only the kernel size is enlarged from `2x2` to `3x3`.

Layer-by-layer shape flow in the current Group B setup (`[B, 8, 18, 9]` input):
- input: `[B, 8, 18, 9]`
- `conv1(k=3)`: `[B, 16, 16, 7]`
- anti-rectifier: `[B, 32, 16, 7]`
- `conv2(k=3)`: `[B, 32, 14, 5]`
- anti-rectifier: `[B, 64, 14, 5]`
- `conv3(k=3)`: `[B, 64, 12, 3]`
- anti-rectifier: `[B, 128, 12, 3]`
- `deconv2(k=3)`: `[B, 32, 14, 5]`
- anti-rectifier: `[B, 64, 14, 5]`
- `deconv3(k=3)`: `[B, 16, 16, 7]`
- anti-rectifier: `[B, 32, 16, 7]`
- dropout: `[B, 32, 16, 7]`
- `deconv4(k=3)`: `[B, 1, 18, 9]`
- reshape / split real-imag: `[B, 18, 9] -> [B, 9, 9] + [B, 9, 9] -> Rz [B, 9, 9]`

Interpretation:
- the `3x3` backbone keeps exactly the same encoder-decoder depth and channel schedule as the `2x2` model
- the only controlled architectural change is the larger local receptive field at every convolution and transposed-convolution stage
- because there is no padding, the `3x3` version compresses the spatial dimensions faster
- in the current `18 x 9` input setting, its bottleneck feature map is `12 x 3`

### Current warning

Differentiable Root-MUSIC is still unstable enough that:
- it should be treated as experimental
- ESPRIT should be the default learned head unless there is a specific reason to investigate Root-MUSIC further

## 12. Current Coding / Experiment Style Rules For Future AI Agents

If you are another AI continuing this repo, follow these rules.

### 12.1 For experiment additions

- add:
  - a launcher
  - templates
  - one experiment plan doc
- do not add an implementation-plan doc unless actual algorithm code changes are required

### 12.2 For geometry-sensitive work

- do not assume row geometry from old templates
- derive row geometry from physical 2D coordinates when working in the 2D rowwise LRMC path
- be careful with Group B vs Group A/C row patterns

### 12.3 For ultra-low-snapshot work

- avoid `np.cov` in fragile classical covariance paths
- prefer the explicit sample covariance helper
- keep Hermitian stabilization in mind before LRMC

### 12.4 For documentation style

Current repo style prefers:
- dedicated per-family results markdown
- direct file naming that includes:
  - phase number
  - geometry or regime
  - coherent / noncoherent when relevant
- explicit `markdown_group_label` and `markdown_scheme_label` in templates for readable result tables

### 12.5 For Windows path-length safety

- be careful with Windows path-length limits when defining new `scenario_data_path` values
- long experiment names combined with long dataset filenames can cause `torch.save(...)` to fail even when the directory exists
- keep cache-folder names shorter when the template name or signal label is already long, especially for large-sample sweeps
- if a run fails at dataset save time with "file cannot be opened" on Windows, check the full output path length before assuming the dataset code is wrong

### 12.6 For SubspaceNet work

- keep dataset caching enabled for large runs
- prefer ESPRIT-first unless Root-MUSIC is the explicit research target
- if Root-MUSIC is retried, inspect the differentiable Root-MUSIC head carefully before spending long training time

## 13. Current Practical Conclusions

1. The project's most validated hardware-relevant regime is now Group B `1.9 lambda`.
2. Classical Group B performance is strong once row geometry is modeled correctly and the canonical `SS -> LRMC` front end is used.
3. For coherent Group B, `SS -> LRMC` is not merely a mild improvement for subspace methods; it is the enabling preprocessing step that makes MUSIC, Root-MUSIC, and ESPRIT workable on the hardware geometry.
4. Without `SS -> LRMC`, coherent Group B subspace baselines largely collapse across the tested fixed-gap and SNR grid, while DBF remains comparatively unaffected; this indicates that the main preprocessing gain is structural recovery of a usable subspace model rather than a uniform improvement for every estimator.
5. In coherent Group B, small angular separation is now the clearest failure axis. In the tested `T = 40`, `1 - 15 dB` regime, gap size matters much more than SNR, and the strongest classical degradation still occurs around `1 - 2 deg`.
6. Coherent Group B therefore remains a meaningful learned target, especially in low-separation regimes where the classical `SS -> LRMC` pipeline is still imperfect.
7. SubspaceNet-ESPRIT is currently the strongest learned path and produces its most meaningful gains exactly in the hard coherent low-separation cells, where it reduces multi-degree classical errors to sub-degree RMSE.
8. The hard-regime snapshot breakdown at fixed `1 deg`, `1 dB` shows that for both coherent and non-coherent signals, lowering snapshots hurts `SS -> LRMC -> SubspaceNet -> ESPRIT` much less than it hurts the classical controls; the learned pipeline keeps a large advantage even at `T = 1..4` and becomes especially strong again by `T = 16..25`.
9. That same snapshot breakdown sharpens the coherent interpretation: in the hardest coherent cell, the main classical bottleneck is not simply lack of snapshots, because even at `T = 25` the classical `SS -> LRMC` controls remain very poor, while the learned model improves rapidly with additional `T`.
10. In non-coherent Group B, the fixed-gap / SNR grid confirms that this regime is much easier than the coherent one: once SNR is moderate, classical MUSIC / Root-MUSIC / ESPRIT with `SS -> LRMC` remain very strong even at `1 deg`.
11. The non-coherent Phase 6 results also show an important method split without preprocessing: raw MUSIC can already be excellent at moderate SNR, whereas raw Root-MUSIC / ESPRIT still fail badly; in the non-coherent regime, `SS -> LRMC` is therefore most important for subspace-method rescue and low-SNR robustness rather than for making every classical method viable.
12. In the non-coherent regime, SubspaceNet-ESPRIT is still strongest in the hardest `1 deg`, low-SNR cells, but it is no longer uniformly better than the best classical preprocessed method once the task becomes easy; this means the main remaining learned value is in hard-edge robustness rather than broad average dominance.
13. The Phase 7A two-subarray screening shows that reducing spatial smoothing from `3-of-3` row blocks to `2-of-3` is not a single scalar weakening; which row pair is chosen matters a lot in coherent hard cells. The contiguous `rows 0+1` variant can outperform the full `3-of-3` baseline in the hardest coherent cells, while the skip-middle `rows 0+2` and `rows 1+2` choices are usually worse there.
14. In easier or non-coherent cells, the difference between `3-of-3` and `2-of-3` spatial smoothing becomes much smaller. This means the spatial-smoothing floor is mainly a hard coherent boundary issue rather than a universal requirement of the Group B pipeline.
15. The Phase 7A result also means reduced-SS variants should not be treated as pure "less smoothing" controls. Row-pair geometry matters enough that future reduced-SS studies should preserve pair identity explicitly rather than collapsing all `2-of-3` choices into one bucket.
16. Phase 7B Phase 1.1 provided the first positive evidence that the reduced-SS branch diversity can be exploited by a learned model rather than only by fixed branch selection. In the primary hard coherent cell (`1 deg`, `1 dB`, `T = 40`), the learned SS-fusion model achieved about `0.4516 deg`, slightly better than the then-current `SS(3/3)` learned baseline at about `0.4747 deg` and clearly better than the best fixed `SS(2/3: rows 0+1)` learned baseline at about `0.6995 deg`.
17. Phase 7B Phase 1.1.1 refined that interpretation. The `1x1` channel-only fusion model achieved about `0.5414 deg` in the same hard coherent cell, which is still better than the fixed `SS(2/3: rows 0+1)` learned baseline and only moderately worse than the fixed `SS(3/3)` learned baseline, but worse than the earlier spatial-fusion Phase `1.1` result.
18. Phase 7C then changed the picture again by holding the learned schemes fixed and enlarging the SubspaceNet backbone kernel from `2x2` to `3x3`. All four tested learned variants improved in the same hard coherent cell: `SS(3/3)` improved from about `0.4747 deg` to about `0.4087 deg`, `SS(2/3: rows 0+1)` from about `0.6995 deg` to about `0.5386 deg`, spatial learned fusion from about `0.4516 deg` to about `0.4118 deg`, and `1x1` channel-only fusion from about `0.5414 deg` to about `0.4396 deg`.
19. The Phase 7C ranking was informative because, before the activation follow-up, the plain `SS(3/3)` learned baseline briefly became the best performer and the spatial-fusion model fell to a very close second. That result showed that backbone receptive-field size is itself a strong lever in the hard coherent Group B regime and that some of the earlier fusion advantage had been backbone-limited.
20. Phase 7D then sharpened the interpretation again. When the `3x3` spatial-fusion model replaced plain `ReLU` with a width-controlled anti-rectifier, its RMSE improved from about `0.4118 deg` to about `0.3592 deg`, beating both the ReLU spatial-fusion `3x3` reference and the plain `SS(3/3)` `3x3` baseline at about `0.4087 deg`.
21. This Phase 7D result is important because the anti-rectifier comparison was intentionally width-controlled rather than implemented as a naive doubled-width expansion. That makes the improvement much stronger evidence that sign-preserving activation inside the covariance-fusion block is genuinely useful in the primary hard coherent cell, rather than the gain being mainly a by-product of increased hidden capacity.
22. The learned SS-fusion path is therefore no longer just promising but structurally reinforced. The current best configuration in the primary hard coherent cell is now `SS(2/3 x 3) -> LRMC -> width-controlled anti-rectifier spatial fusion -> SubspaceNet(3x3) -> ESPRIT`.
23. Root-MUSIC remains the most fragile component in both classical and learned forms and should still be treated as experimental unless it is the explicit object of study.
24. The experiment framework is now mature enough that future work should be targeted:
   - coherent low-separation Group B, especially `1 - 2 deg`
   - combined hard regimes such as low-separation plus low-snapshot
   - focused SubspaceNet-ESPRIT improvements in the hard coherent cells
   - preprocessing ablations that distinguish when non-coherent MUSIC can skip `SS -> LRMC` versus when Root-MUSIC / ESPRIT still require it
   - reduced-SS follow-up centered on the best coherent `2-of-3` row pair rather than treating all two-subarray variants as equivalent
   - learned SS-fusion follow-up that checks whether the new anti-rectifier spatial-fusion gain persists across the next coherent hard cells
   - structure-aware SS-fusion follow-up that clarifies whether the best next model should use anti-rectifier spatial fusion, channel-only fusion, or more explicitly constrained weighted fusion
