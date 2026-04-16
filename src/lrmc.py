"""Utilities for NULA covariance completion and SubspaceNet feature conversion."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
import time
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import torch


@dataclass
class LRMCDiagnostics:
    """Stores convergence and numerical diagnostics for LRMC."""

    solver: str
    rank: int
    iterations: int = 0
    converged: bool = False
    runtime_sec: float = 0.0
    observed_residuals: List[float] = field(default_factory=list)
    relative_changes: List[float] = field(default_factory=list)
    singular_values: List[List[float]] = field(default_factory=list)
    effective_ranks: List[int] = field(default_factory=list)
    min_eigenvalue: Optional[float] = None
    min_singular_value: Optional[float] = None
    observable_lags: List[int] = field(default_factory=list)


DEFAULT_ROW_GROUPS_2D: Tuple[Tuple[int, ...], ...] = (
    (0, 1, 2, 3),
    (4, 5, 6, 7),
    (8, 9, 10, 11),
)


def compute_sample_covariance(X: np.ndarray) -> np.ndarray:
    """Returns the sample covariance matrix R = (1/T) X X^H."""
    X = np.asarray(X, dtype=np.complex128)
    if X.ndim != 2:
        raise ValueError("compute_sample_covariance: X must be a 2D matrix")
    snapshots = X.shape[1]
    if snapshots <= 0:
        raise ValueError("compute_sample_covariance: X must contain snapshots")
    return (X @ np.conjugate(X.T)) / snapshots


def split_covariance_into_blocks(
    covariance: np.ndarray, row_groups: Sequence[Sequence[int]]
) -> List[np.ndarray]:
    """Extracts covariance blocks for the provided row groups."""
    covariance = ensure_hermitian(np.asarray(covariance, dtype=np.complex128))
    blocks = []
    for group in row_groups:
        indices = np.asarray(group, dtype=int)
        blocks.append(covariance[np.ix_(indices, indices)])
    return blocks


def average_covariance_blocks(blocks: Sequence[np.ndarray]) -> np.ndarray:
    """Averages covariance blocks elementwise."""
    if not blocks:
        raise ValueError("average_covariance_blocks: blocks must not be empty")
    reference_shape = np.asarray(blocks[0]).shape
    for block in blocks:
        if np.asarray(block).shape != reference_shape:
            raise ValueError("average_covariance_blocks: all blocks must have the same shape")
    stacked = np.stack([np.asarray(block, dtype=np.complex128) for block in blocks], axis=0)
    return np.mean(stacked, axis=0)


def enumerate_nula_lags(sensor_positions: Iterable[float]) -> Dict[int, List[Tuple[int, int]]]:
    """Returns a mapping from differential lag to physical sensor-index pairs."""
    positions = np.asarray(list(sensor_positions), dtype=int)
    lag_map: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
    for row, pos_i in enumerate(positions):
        for col, pos_j in enumerate(positions):
            lag_map[int(pos_i - pos_j)].append((row, col))
    return dict(lag_map)


def build_virtual_covariance_observation(
    covariance: np.ndarray,
    sensor_positions: Iterable[float],
    virtual_size: int,
) -> Tuple[np.ndarray, np.ndarray, Dict[int, List[Tuple[int, int]]]]:
    """
    Lifts physical sparse-array covariance into a partially observed virtual ULA covariance.

    Entries with the same lag are averaged and copied to every virtual entry sharing that lag.
    """
    covariance = np.asarray(covariance, dtype=np.complex128)
    if covariance.shape[0] != covariance.shape[1]:
        raise ValueError(
            "build_virtual_covariance_observation: covariance must be square"
        )
    positions = np.asarray(list(sensor_positions), dtype=int)
    if covariance.shape[0] != len(positions):
        raise ValueError(
            "build_virtual_covariance_observation: covariance shape must match sensor_positions"
        )
    if virtual_size <= int(np.max(positions)):
        raise ValueError(
            "build_virtual_covariance_observation: virtual_size must exceed max sensor position"
        )

    lag_map = enumerate_nula_lags(positions)
    lag_values: Dict[int, complex] = {}
    for lag, pairs in lag_map.items():
        lag_values[lag] = np.mean([covariance[i, j] for i, j in pairs])

    partial = np.zeros((virtual_size, virtual_size), dtype=np.complex128)
    mask = np.zeros((virtual_size, virtual_size), dtype=float)
    for row in range(virtual_size):
        for col in range(virtual_size):
            lag = row - col
            if lag in lag_values:
                partial[row, col] = lag_values[lag]
                mask[row, col] = 1.0

    partial = ensure_hermitian(partial)
    if not np.allclose(partial, np.conjugate(partial.T), atol=1e-10):
        raise AssertionError(
            "build_virtual_covariance_observation: partial covariance must be Hermitian"
        )
    return partial, mask, lag_map


def build_virtual_covariance_observation_from_covariance(
    covariance: np.ndarray,
    sensor_positions: Iterable[float],
    virtual_size: int,
) -> Tuple[np.ndarray, np.ndarray, Dict[int, List[Tuple[int, int]]]]:
    """Builds a partial virtual covariance from an already computed covariance matrix."""
    covariance = np.asarray(covariance, dtype=np.complex128)
    return build_virtual_covariance_observation(
        covariance=covariance,
        sensor_positions=sensor_positions,
        virtual_size=virtual_size,
    )


def initialize_missing_entries(
    partial: np.ndarray,
    mask: np.ndarray,
    strategy: str = "lag",
) -> np.ndarray:
    """Initializes missing entries before iterative LRMC."""
    estimate = np.array(partial, copy=True)
    if strategy.startswith("zero"):
        return estimate
    if strategy.startswith("random"):
        real_part = np.random.randn(*partial.shape)
        imag_part = np.random.randn(*partial.shape)
        random_fill = (real_part + 1j * imag_part) * (1 - mask)
        estimate = np.where(mask > 0, estimate, random_fill)
        return ensure_hermitian(estimate)

    virtual_size = partial.shape[0]
    lag_means: Dict[int, complex] = {}
    for lag in range(-(virtual_size - 1), virtual_size):
        lag_entries = []
        for row in range(virtual_size):
            col = row - lag
            if 0 <= col < virtual_size and mask[row, col] > 0:
                lag_entries.append(partial[row, col])
        if lag_entries:
            lag_means[lag] = np.mean(lag_entries)

    for row in range(virtual_size):
        for col in range(virtual_size):
            if mask[row, col] > 0:
                continue
            lag = row - col
            if lag in lag_means:
                estimate[row, col] = lag_means[lag]
            elif strategy.startswith("neighbor"):
                neighbors = []
                for delta in (1, -1, 2, -2):
                    if lag + delta in lag_means:
                        neighbors.append(lag_means[lag + delta])
                if neighbors:
                    estimate[row, col] = np.mean(neighbors)

    return ensure_hermitian(estimate)


def ensure_hermitian(matrix: np.ndarray) -> np.ndarray:
    """Returns the Hermitian projection of a complex square matrix."""
    return 0.5 * (matrix + np.conjugate(matrix.T))


def project_toeplitz(matrix: np.ndarray) -> np.ndarray:
    """Projects a matrix onto the Toeplitz set by diagonal averaging."""
    matrix = np.asarray(matrix, dtype=np.complex128)
    output = np.zeros_like(matrix)
    size = matrix.shape[0]
    for lag in range(-(size - 1), size):
        diagonal = np.diagonal(matrix, offset=lag)
        if diagonal.size == 0:
            continue
        mean_value = np.mean(diagonal)
        if lag >= 0:
            for row in range(size - lag):
                output[row, row + lag] = mean_value
        else:
            for row in range(size + lag):
                output[row - lag, row] = mean_value
    return ensure_hermitian(output)


def project_psd(
    matrix: np.ndarray, epsilon: float = 1e-8
) -> Tuple[np.ndarray, float, float]:
    """Projects a Hermitian matrix onto the PSD cone and returns stability stats."""
    hermitian = ensure_hermitian(matrix)
    eigenvalues, eigenvectors = np.linalg.eigh(hermitian)
    clipped = np.maximum(eigenvalues, epsilon)
    projected = (eigenvectors @ np.diag(clipped)) @ np.conjugate(eigenvectors.T)
    projected = ensure_hermitian(projected)
    singular_values = np.linalg.svd(projected, compute_uv=False)
    return projected, float(np.min(clipped)), float(np.min(singular_values))


def complete_covariance_svd(
    partial: np.ndarray,
    mask: np.ndarray,
    rank: int,
    max_iter: int = 100,
    tol: float = 1e-6,
    init_strategy: str = "lag",
    enforce_toeplitz: bool = False,
    epsilon: float = 1e-8,
) -> Tuple[np.ndarray, LRMCDiagnostics]:
    """Completes a partially observed covariance matrix via alternating low-rank projection."""
    estimate = initialize_missing_entries(partial, mask, strategy=init_strategy)
    diagnostics = LRMCDiagnostics(solver="svd", rank=rank)
    start = time.perf_counter()

    observed = np.where(mask > 0, partial, 0)
    normalizer = np.linalg.norm(observed) + epsilon
    prev = estimate
    for iteration in range(max_iter):
        estimate = np.where(mask > 0, partial, estimate)
        estimate = ensure_hermitian(estimate)
        u, singular_values, vh = np.linalg.svd(estimate, full_matrices=False)
        truncated = (u[:, :rank] * singular_values[:rank]) @ vh[:rank, :]
        estimate = np.where(mask > 0, partial, truncated)
        estimate = ensure_hermitian(estimate)
        if enforce_toeplitz:
            estimate = project_toeplitz(estimate)
            estimate = np.where(mask > 0, partial, estimate)
            estimate = ensure_hermitian(estimate)

        observed_residual = (
            np.linalg.norm(mask * (estimate - partial)) / normalizer
        )
        relative_change = np.linalg.norm(estimate - prev) / (
            np.linalg.norm(prev) + epsilon
        )
        diagnostics.observed_residuals.append(float(observed_residual))
        diagnostics.relative_changes.append(float(relative_change))
        diagnostics.singular_values.append(singular_values.tolist())
        diagnostics.effective_ranks.append(int(np.sum(singular_values > epsilon)))
        diagnostics.iterations = iteration + 1
        prev = np.array(estimate, copy=True)
        if relative_change < tol:
            diagnostics.converged = True
            break

    completed, min_eig, min_sv = project_psd(estimate, epsilon=epsilon)
    diagnostics.runtime_sec = time.perf_counter() - start
    diagnostics.min_eigenvalue = min_eig
    diagnostics.min_singular_value = min_sv
    return completed, diagnostics


def complete_covariance_nuclear_norm(
    partial: np.ndarray,
    mask: np.ndarray,
    rank: int,
    epsilon: float = 1e-8,
    enforce_toeplitz: bool = False,
    ridge_weight: float = 1e-8,
) -> Tuple[np.ndarray, LRMCDiagnostics]:
    """Completes a covariance matrix using convex nuclear-norm minimization."""
    try:
        import cvxpy as cp
    except ImportError as exc:
        raise ImportError(
            "complete_covariance_nuclear_norm: cvxpy is required for solver='nuclear'"
        ) from exc

    diagnostics = LRMCDiagnostics(solver="nuclear", rank=rank)
    start = time.perf_counter()
    size = partial.shape[0]
    Z = cp.Variable((size, size), hermitian=True)
    constraints = [cp.multiply(mask, Z - partial) == 0]
    if enforce_toeplitz:
        for row in range(size - 1):
            for col in range(size - 1):
                constraints.append(Z[row, col] == Z[row + 1, col + 1])
    objective = cp.normNuc(Z)
    if ridge_weight > 0:
        objective += 0.5 * ridge_weight * cp.sum_squares(cp.abs(Z))
    problem = cp.Problem(cp.Minimize(objective), constraints)
    problem.solve(solver=cp.SCS, verbose=False)
    estimate = np.asarray(Z.value, dtype=np.complex128)
    if enforce_toeplitz:
        estimate = project_toeplitz(estimate)
    completed, min_eig, min_sv = project_psd(estimate, epsilon=epsilon)
    diagnostics.runtime_sec = time.perf_counter() - start
    diagnostics.iterations = 1
    diagnostics.converged = problem.status in {cp.OPTIMAL, cp.OPTIMAL_INACCURATE}
    diagnostics.observed_residuals.append(
        float(np.linalg.norm(mask * (completed - partial)) / (np.linalg.norm(mask * partial) + epsilon))
    )
    diagnostics.relative_changes.append(0.0)
    diagnostics.singular_values.append(np.linalg.svd(completed, compute_uv=False).tolist())
    diagnostics.effective_ranks.append(int(np.sum(np.linalg.svd(completed, compute_uv=False) > epsilon)))
    diagnostics.min_eigenvalue = min_eig
    diagnostics.min_singular_value = min_sv
    return completed, diagnostics


def combine_diagnostics(diagnostics: Sequence[LRMCDiagnostics]) -> LRMCDiagnostics:
    """Combines several diagnostics objects into one summary object."""
    diagnostics = list(diagnostics)
    if not diagnostics:
        raise ValueError("combine_diagnostics: diagnostics must not be empty")
    combined = LRMCDiagnostics(
        solver=diagnostics[0].solver,
        rank=diagnostics[0].rank,
        iterations=int(np.round(np.mean([diag.iterations for diag in diagnostics]))),
        converged=all(diag.converged for diag in diagnostics),
        runtime_sec=float(np.sum([diag.runtime_sec for diag in diagnostics])),
        observed_residuals=[
            float(np.mean([diag.observed_residuals[-1] if diag.observed_residuals else 0.0 for diag in diagnostics]))
        ],
        relative_changes=[
            float(np.mean([diag.relative_changes[-1] if diag.relative_changes else 0.0 for diag in diagnostics]))
        ],
        singular_values=diagnostics[0].singular_values[-1:] if diagnostics[0].singular_values else [],
        effective_ranks=[int(np.round(np.mean([diag.effective_ranks[-1] if diag.effective_ranks else 0 for diag in diagnostics])))]
        if diagnostics[0].effective_ranks
        else [],
        min_eigenvalue=float(np.min([diag.min_eigenvalue for diag in diagnostics if diag.min_eigenvalue is not None]))
        if any(diag.min_eigenvalue is not None for diag in diagnostics)
        else None,
        min_singular_value=float(np.min([diag.min_singular_value for diag in diagnostics if diag.min_singular_value is not None]))
        if any(diag.min_singular_value is not None for diag in diagnostics)
        else None,
        observable_lags=sorted({lag for diag in diagnostics for lag in diag.observable_lags}),
    )
    return combined


def complete_nula_covariance(
    X: np.ndarray,
    sensor_positions: Iterable[float],
    virtual_size: int,
    rank: int,
    solver: str = "svd",
    init_strategy: str = "lag",
    max_iter: int = 100,
    tol: float = 1e-6,
    epsilon: float = 1e-8,
    enforce_toeplitz: bool = False,
    nuclear_ridge: float = 1e-8,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, LRMCDiagnostics]:
    """Runs the full LRMC pipeline from sparse snapshots to completed virtual covariance."""
    covariance = compute_sample_covariance(X)
    return complete_nula_covariance_from_covariance(
        covariance=covariance,
        sensor_positions=sensor_positions,
        virtual_size=virtual_size,
        rank=rank,
        solver=solver,
        init_strategy=init_strategy,
        max_iter=max_iter,
        tol=tol,
        epsilon=epsilon,
        enforce_toeplitz=enforce_toeplitz,
        nuclear_ridge=nuclear_ridge,
    )


def complete_nula_covariance_from_covariance(
    covariance: np.ndarray,
    sensor_positions: Iterable[float],
    virtual_size: int,
    rank: int,
    solver: str = "svd",
    init_strategy: str = "lag",
    max_iter: int = 100,
    tol: float = 1e-6,
    epsilon: float = 1e-8,
    enforce_toeplitz: bool = False,
    nuclear_ridge: float = 1e-8,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, LRMCDiagnostics]:
    """Runs LRMC when a covariance matrix is already available."""
    covariance = ensure_hermitian(np.asarray(covariance, dtype=np.complex128))
    partial, mask, lag_map = build_virtual_covariance_observation(
        covariance=covariance,
        sensor_positions=sensor_positions,
        virtual_size=virtual_size,
    )
    if solver.startswith("nuclear"):
        completed, diagnostics = complete_covariance_nuclear_norm(
            partial=partial,
            mask=mask,
            rank=rank,
            epsilon=epsilon,
            enforce_toeplitz=enforce_toeplitz,
            ridge_weight=nuclear_ridge,
        )
    else:
        completed, diagnostics = complete_covariance_svd(
            partial=partial,
            mask=mask,
            rank=rank,
            max_iter=max_iter,
            tol=tol,
            init_strategy=init_strategy,
            enforce_toeplitz=enforce_toeplitz,
            epsilon=epsilon,
        )
    diagnostics.observable_lags = sorted(lag_map.keys())
    return covariance, partial, mask, completed, diagnostics


def complete_rowwise_nula_covariance(
    covariance: np.ndarray,
    row_groups: Sequence[Sequence[int]],
    sensor_positions: Iterable[float],
    virtual_size: int,
    rank: int,
    solver: str = "svd",
    init_strategy: str = "lag",
    max_iter: int = 100,
    tol: float = 1e-6,
    epsilon: float = 1e-8,
    enforce_toeplitz: bool = False,
    nuclear_ridge: float = 1e-8,
    variant: str = "canonical",
) -> Tuple[np.ndarray, Optional[np.ndarray], Optional[np.ndarray], np.ndarray, LRMCDiagnostics]:
    """
    Completes a row-replicated NULA covariance according to the requested variant.

    Variants:
        - canonical: complete the canonical row only
        - average_raw: average row blocks first, then complete once
        - average_completed: complete each row block independently, then average completions
    """
    row_blocks = split_covariance_into_blocks(covariance, row_groups=row_groups)
    if variant == "average_raw":
        smoothed_covariance = average_covariance_blocks(row_blocks)
        covariance_out, partial, mask, completed, diagnostics = complete_nula_covariance_from_covariance(
            covariance=smoothed_covariance,
            sensor_positions=sensor_positions,
            virtual_size=virtual_size,
            rank=rank,
            solver=solver,
            init_strategy=init_strategy,
            max_iter=max_iter,
            tol=tol,
            epsilon=epsilon,
            enforce_toeplitz=enforce_toeplitz,
            nuclear_ridge=nuclear_ridge,
        )
        diagnostics.runtime_sec = float(diagnostics.runtime_sec)
        return covariance_out, partial, mask, completed, diagnostics

    if variant == "average_completed":
        completions = []
        diagnostics_list = []
        partial = None
        mask = None
        covariance_out = None
        for block in row_blocks:
            covariance_out, partial, mask, completed, diagnostics = complete_nula_covariance_from_covariance(
                covariance=block,
                sensor_positions=sensor_positions,
                virtual_size=virtual_size,
                rank=rank,
                solver=solver,
                init_strategy=init_strategy,
                max_iter=max_iter,
                tol=tol,
                epsilon=epsilon,
                enforce_toeplitz=enforce_toeplitz,
                nuclear_ridge=nuclear_ridge,
            )
            completions.append(completed)
            diagnostics_list.append(diagnostics)
        completed = average_covariance_blocks(completions)
        diagnostics = combine_diagnostics(diagnostics_list)
        return covariance_out, partial, mask, completed, diagnostics

    canonical_index = -1
    covariance_out, partial, mask, completed, diagnostics = complete_nula_covariance_from_covariance(
        covariance=row_blocks[canonical_index],
        sensor_positions=sensor_positions,
        virtual_size=virtual_size,
        rank=rank,
        solver=solver,
        init_strategy=init_strategy,
        max_iter=max_iter,
        tol=tol,
        epsilon=epsilon,
        enforce_toeplitz=enforce_toeplitz,
        nuclear_ridge=nuclear_ridge,
    )
    return covariance_out, partial, mask, completed, diagnostics


def covariance_to_autocorrelation_tensor(
    covariance: np.ndarray, tau: int
) -> torch.Tensor:
    """
    Converts a completed covariance matrix into the SubspaceNet tensor layout [tau, 2N, N].
    """
    covariance = np.asarray(covariance, dtype=np.complex128)
    if covariance.shape[0] != covariance.shape[1]:
        raise ValueError("covariance_to_autocorrelation_tensor: covariance must be square")
    size = covariance.shape[0]
    if tau >= size:
        raise ValueError("covariance_to_autocorrelation_tensor: tau must be smaller than covariance size")

    slices = []
    for lag in range(tau):
        shifted = np.zeros_like(covariance)
        if lag == 0:
            shifted = covariance
        else:
            shifted[:, lag:] = covariance[:, :-lag]
        stacked = np.concatenate((np.real(shifted), np.imag(shifted)), axis=0)
        slices.append(torch.tensor(stacked, dtype=torch.float32))
    tensor = torch.stack(slices, dim=0)
    expected_shape = (tau, 2 * size, size)
    if tuple(tensor.shape) != expected_shape:
        raise AssertionError(
            f"covariance_to_autocorrelation_tensor: expected {expected_shape}, got {tuple(tensor.shape)}"
        )
    return tensor


def plot_mask_and_convergence(
    mask: np.ndarray,
    diagnostics: LRMCDiagnostics,
    axes=None,
):
    """Plots the virtual covariance mask and LRMC residual history."""
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise ImportError("plot_mask_and_convergence: matplotlib is required") from exc

    if axes is None:
        _, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].imshow(mask, cmap="gray_r")
    axes[0].set_title("Observable Mask")
    axes[0].set_xlabel("Virtual Column")
    axes[0].set_ylabel("Virtual Row")
    axes[1].plot(diagnostics.observed_residuals, label="Observed residual")
    axes[1].plot(diagnostics.relative_changes, label="Relative change")
    axes[1].set_title("LRMC Convergence")
    axes[1].set_xlabel("Iteration")
    axes[1].legend(loc="best")
    return axes
