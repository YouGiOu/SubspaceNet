# Revised Plan: LRMC + SubspaceNet DOA for NULA `[0, 1, 4, 8]`

## Summary
Implement a thesis-ready pipeline that takes narrowband snapshots from the non-uniform linear array `[0,1,4,8]`, constructs a partially observed virtual-ULA covariance of size `9×9`, completes it with low-rank matrix completion using default rank `r=K+1=3`, and converts the completed covariance into the feature format required by a retrained SubspaceNet. The implementation should preserve the repo’s original ULA path while adding a parallel NULA+LRMC path with diagnostics, visualization, and sensitivity experiments.

This revision explicitly strengthens: convergence monitoring for structured masks, lag-to-virtual-array validation, Toeplitz/PSD decision points, shape assertions for SubspaceNet input, and numerical-stability checks after PSD projection.

## Phase 1: Problem Definition, Lag Coverage, and Thesis Figures
- Formalize the physical array as `S=[0,1,4,8]`, the virtual ULA as positions `V=[0,1,...,8]`, and the signal model with `K=2`.
- Define the sample covariance exactly as implemented: `R_phys = (1/T) X X^H`, even if thesis notation later uses a different averaging symbol.
- Enumerate the physical difference set from `[0,1,4,8]` and verify which lags are directly observable.
- Confirm whether the chosen virtual ULA size `9` is:
  - aperture-based (`0..8`), or
  - intended to represent recoverable coarray support.
- Produce a lag map and mask heatmap showing observable versus missing entries in the `9×9` virtual covariance.
- Lock the matrix-structure policy for implementation:
  - default: Hermitian + PSD enforced,
  - optional ablation: Hermitian + PSD + Toeplitz projection.

Outputs:
- Mathematical definitions for `R_phys`, `R_partial`, mask `Omega`, lag mapping, and `R_completed`.
- A table/figure proving how the 9 virtual positions relate to the physical array and which entries are missing.
- A written note in the thesis explaining that structured masks weaken classical LRMC guarantees.

Code hints:
- `numpy` for lag enumeration and index mapping.
- `matplotlib.pyplot.imshow` for mask heatmaps.
- `collections.defaultdict` for lag-to-entry grouping.

Validation:
- Assert that every observable entry in `R_partial` corresponds to at least one physical sensor pair.
- Verify Hermitian-consistent filling of observed entries.

## Phase 2: Add NULA Geometry Without Breaking the Existing ULA Path
- Extend `SystemModelParams` to accept explicit `sensor_positions` and `virtual_array_size`.
- Update array creation so the original ULA behavior remains the default when `sensor_positions` is absent.
- Refactor steering-vector generation to use explicit coordinates for NULA experiments.
- Add a dedicated NULA data-generation path that produces snapshots `X ∈ C^(4×T)` while keeping the existing ULA dataset path unchanged.
- Keep experiment configuration explicit:
  - `sensor_positions=[0,1,4,8]`
  - `physical_sensor_count=4`
  - `virtual_array_size=9`
  - `K=2`

Outputs:
- Backward-compatible geometry support.
- Reproducible NULA snapshot generator.

Code hints:
- `numpy.asarray(sensor_positions)`.
- Assertions for monotonic increasing positions and `len(sensor_positions)==N`.

Validation:
- Unit-check steering vector dimensions for both ULA and NULA modes.
- Confirm covariance shape is `4×4` before virtual lifting.

Risks:
- Current repo mixes “sensor count” and “feature dimension”; keep physical and virtual dimensions separate in naming and config.

## Phase 3: LRMC Module with Convergence Diagnostics and Stability Checks
- Implement a standalone LRMC preprocessing module with interface:
  - input: `X`, `sensor_positions`, `virtual_size`, `rank`, solver settings
  - output: `R_partial`, `Omega`, `R_completed`, diagnostics
- Build the partial virtual covariance by mapping physical covariance entries into the `9×9` virtual grid.
- Implement two completion methods:
  - default engineering solver: truncated-SVD alternating completion with fixed rank `3`
  - comparison solver: nuclear-norm optimization via `cvxpy`
- Add robust initialization strategies:
  - zero fill
  - lag-average fill
  - optional neighbor-lag interpolation for structured-missing-pattern mitigation
- Track convergence each iteration:
  - residual on observed entries
  - relative change in completed matrix
  - singular values
  - effective numerical rank
- Add optional iteration visualization for thesis figures: residual versus iteration count.
- Post-process with:
  - Hermitian symmetrization `(R + R^H)/2`
  - PSD projection via eigenvalue clipping
  - numerical stability check on minimum singular value or minimum eigenvalue against `epsilon`

Outputs:
- A reusable LRMC solver module.
- Logged convergence traces and plotting hooks.

Code hints:
- `numpy.linalg.svd`, `numpy.linalg.eigh`
- `cvxpy.Variable((9,9), complex=True, hermitian=True)`
- `cvxpy.normNuc`
- `time.perf_counter` for solver runtime
- `dataclasses.dataclass` for solver diagnostics container

Validation:
- Residual on observed entries should monotonically decrease or stabilize.
- Hermitian error should be near machine precision after projection.
- Minimum eigenvalue after PSD projection should be `>= -epsilon`.
- Minimum singular value should be checked against a chosen floor for numerical stability.

Risks:
- The deterministic mask may stall or bias LRMC.
- If convergence is poor, increase regularization, improve initialization, or compare with Toeplitz-constrained variants.

## Phase 4: Convert Completed Covariance into SubspaceNet-Compatible Features
- Define a single canonical conversion from `R_completed ∈ C^(9×9)` to SubspaceNet input.
- Preferred path: derive an autocorrelation-style tensor with shape `[tau, 18, 9]`, matching the repo’s real/imag stacking convention for `2N × N`.
- Add explicit shape assertions:
  - `R_completed.shape == (9,9)`
  - final tensor shape is `[tau, 18, 9]`
  - real/imag stacking order matches the existing repo convention
- Validate the `tau` choice:
  - default candidates: `tau ∈ {4,6,8}`
  - assert `tau < 9` unless padding is intentionally introduced
- If padding is needed, document the exact rule and keep it identical across train/val/test.
- Add consistency checks that reconstructed lag slices from `R_completed` remain compatible with the downstream model assumptions.

Outputs:
- A deterministic feature-conversion function from completed covariance to model tensor.
- Assertions and debug logs for shape safety.

Code hints:
- Mirror the layout used by current autocorrelation preprocessing.
- Use `torch.from_numpy` after complex-to-real conversion.

Validation:
- Batch-free single-sample conversion should succeed before integrating dataset generation.
- Feature tensors from repeated runs with the same seed should match exactly.

## Phase 5: Retrain SubspaceNet for the Virtual ULA Path
- Treat LRMC-completed virtual covariance as the new input domain and retrain SubspaceNet accordingly.
- Audit which model assumptions depend on the old array dimension or input geometry before training.
- Refactor only the parts needed so the existing ULA experiments still work.
- Use new datasets generated from the NULA→LRMC→virtual-feature pipeline.
- Keep labels as the true two-source DOAs.

Implementation focus:
- Check all layers and operations that implicitly assume the old array size.
- Verify forward-pass compatibility for `N_v=9` before full training.
- Decide whether to train from scratch or partially initialize from existing weights; default to training from scratch unless shape-compatible transfer is trivial.

Outputs:
- A trainable SubspaceNet path for virtual-ULA inputs of size `9`.
- Experiment configs saved with geometry, rank, `tau`, solver type, SNR, and snapshot count.

Validation:
- Dry-run one batch through forward and loss computation.
- Confirm no shape mismatch in model, loss, or evaluation code.

Risks:
- Solver artifacts may leak into learned features.
- Model layers tied to prior dimensions may fail silently if assumptions are not explicitly checked.

## Phase 6: Evaluation, Sensitivity Analysis, and Thesis-Grade Results
- Evaluate three systems:
  - sparse-array baseline without LRMC
  - LRMC + classical subspace method
  - LRMC + SubspaceNet
- Include sensitivity studies for:
  - LRMC rank around `3`
  - SNR
  - snapshot count `T`
  - `tau`
  - solver type
  - optional Toeplitz constraint
- Explicitly study rank sensitivity:
  - default `r=3`
  - also test higher rank when SNR is low or snapshots are limited
  - report impact on completion residual and DOA RMSE
- Add robustness figures:
  - residual vs iteration
  - singular value spectra
  - mask heatmap
  - RMSE vs SNR
  - RMSE vs snapshots
- Use multiple seeds and report mean/std where practical.

Acceptance criteria:
- `R_completed` is Hermitian and numerically PSD.
- Convergence diagnostics are recorded for LRMC.
- Feature tensor generation is shape-safe and reproducible.
- LRMC + SubspaceNet shows measurable value over at least one baseline in the target NULA setting.

Code hints:
- `matplotlib` for curves and heatmaps
- `pandas` for result tables
- repo seed helper plus explicit NumPy/Torch seeds

## Defaults and Assumptions
- Narrowband scenario only.
- Physical NULA: `[0,1,4,8]`.
- Source count: `K=2`.
- Virtual ULA size: `9`.
- Default LRMC rank: `3`, but sensitivity analysis is mandatory.
- Default matrix constraints: Hermitian + PSD; Toeplitz treated as an ablation/decision point, not hard-coded from the start.
- Default SubspaceNet integration path: retrain on LRMC-derived virtual-ULA features.
- Original ULA code path must remain functional and unchanged in behavior unless the new config is enabled.
