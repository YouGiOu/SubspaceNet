"""Phase 1.1 utilities for learned fusion of three SS(2/3) -> LRMC branches."""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

import numpy as np
import torch

from src.lrmc import (
    complete_rowwise_nula_covariance,
    compute_sample_covariance,
    ensure_hermitian,
)
from src.system_model import SystemModelParams


PHASE1P1_SS_BRANCH_SUBSETS: Tuple[Tuple[int, int], ...] = (
    (0, 1),
    (0, 2),
    (1, 2),
)


def _resolve_phase1p1_branch_subsets(
    system_model_params: SystemModelParams,
) -> Tuple[Tuple[int, int], ...]:
    configured = getattr(system_model_params, "ss_fusion_branch_subsets", None)
    if configured is None:
        return PHASE1P1_SS_BRANCH_SUBSETS
    return tuple(tuple(int(index) for index in subset) for subset in configured)


def build_ss_fusion_phase1p1_branch_covariances(
    covariance: np.ndarray,
    system_model_params: SystemModelParams,
) -> Tuple[List[np.ndarray], List[Dict[str, object]]]:
    """Builds the three SS(2/3) -> LRMC branch covariances for Phase 1.1."""
    row_groups = getattr(system_model_params, "row_groups", None)
    sensor_positions = getattr(system_model_params, "sensor_positions", None)
    virtual_size = getattr(system_model_params, "virtual_array_size", None)
    if row_groups is None or sensor_positions is None or virtual_size is None:
        raise ValueError(
            "build_ss_fusion_phase1p1_branch_covariances: row_groups, sensor_positions, "
            "and virtual_array_size are required"
        )

    rank = getattr(system_model_params, "lrmc_rank", None)
    if rank is None:
        rank = int(system_model_params.M) + 1

    branch_covariances: List[np.ndarray] = []
    branch_diagnostics: List[Dict[str, object]] = []
    for row_subset in _resolve_phase1p1_branch_subsets(system_model_params):
        _, _, _, completed_covariance, diagnostics = complete_rowwise_nula_covariance(
            covariance=ensure_hermitian(np.asarray(covariance, dtype=np.complex128)),
            row_groups=row_groups,
            sensor_positions=sensor_positions,
            virtual_size=int(virtual_size),
            rank=int(rank),
            solver=getattr(system_model_params, "lrmc_solver", "svd"),
            init_strategy=getattr(system_model_params, "lrmc_init_strategy", "lag"),
            max_iter=int(getattr(system_model_params, "lrmc_max_iter", 100)),
            tol=float(getattr(system_model_params, "lrmc_tol", 1e-6)),
            epsilon=float(getattr(system_model_params, "lrmc_epsilon", 1e-8)),
            enforce_toeplitz=bool(
                getattr(system_model_params, "lrmc_enforce_toeplitz", False)
            ),
            nuclear_ridge=float(
                getattr(system_model_params, "lrmc_nuclear_ridge", 1e-8)
            ),
            variant="average_raw",
            ss_num_subarrays=2,
            ss_row_subset=row_subset,
        )
        completed_covariance = ensure_hermitian(completed_covariance)
        if not np.all(np.isfinite(completed_covariance)):
            raise AssertionError(
                "build_ss_fusion_phase1p1_branch_covariances: branch covariance contains non-finite values"
            )
        branch_covariances.append(completed_covariance)
        branch_diagnostics.append(
            {
                "row_subset": list(row_subset),
                "norm_fro": float(np.linalg.norm(completed_covariance)),
                "lrmc_runtime_sec": float(getattr(diagnostics, "runtime_sec", 0.0)),
                "lrmc_iterations": int(getattr(diagnostics, "iterations", 0)),
                "lrmc_converged": bool(getattr(diagnostics, "converged", False)),
                "min_eigenvalue": (
                    None
                    if getattr(diagnostics, "min_eigenvalue", None) is None
                    else float(diagnostics.min_eigenvalue)
                ),
                "min_singular_value": (
                    None
                    if getattr(diagnostics, "min_singular_value", None) is None
                    else float(diagnostics.min_singular_value)
                ),
            }
        )
    return branch_covariances, branch_diagnostics


def build_ss_fusion_phase1p1_input(
    X: torch.Tensor,
    system_model_params: SystemModelParams,
) -> torch.Tensor:
    """Converts snapshots into the 6-channel fusion input tensor [6, N, N]."""
    covariance = compute_sample_covariance(np.asarray(X.cpu().numpy(), dtype=np.complex128))
    branch_covariances, _ = build_ss_fusion_phase1p1_branch_covariances(
        covariance=covariance,
        system_model_params=system_model_params,
    )
    channels = []
    for covariance_branch in branch_covariances:
        channels.append(np.real(covariance_branch))
        channels.append(np.imag(covariance_branch))
    stacked = np.stack(channels, axis=0).astype(np.float32)
    return torch.tensor(stacked, dtype=torch.float32)


def covariance_batch_to_autocorrelation_tensor_phase1p1(
    covariance_batch: torch.Tensor,
    tau: int,
) -> torch.Tensor:
    """Converts a batch of complex covariances into SubspaceNet layout [B, tau, 2N, N]."""
    if covariance_batch.ndim != 3:
        raise ValueError(
            "covariance_batch_to_autocorrelation_tensor_phase1p1: expected [B, N, N] covariance batch"
        )
    batch_size, size, size_b = covariance_batch.shape
    if size != size_b:
        raise ValueError(
            "covariance_batch_to_autocorrelation_tensor_phase1p1: covariance matrices must be square"
        )
    if tau >= size:
        raise ValueError(
            "covariance_batch_to_autocorrelation_tensor_phase1p1: tau must be smaller than covariance size"
        )
    slices = []
    for lag in range(tau):
        shifted = torch.zeros_like(covariance_batch)
        if lag == 0:
            shifted = covariance_batch
        else:
            shifted[:, :, lag:] = covariance_batch[:, :, :-lag]
        stacked = torch.cat((shifted.real, shifted.imag), dim=1)
        slices.append(stacked)
    output = torch.stack(slices, dim=1)
    expected_shape = (batch_size, tau, 2 * size, size)
    if tuple(output.shape) != expected_shape:
        raise AssertionError(
            "covariance_batch_to_autocorrelation_tensor_phase1p1: "
            f"expected {expected_shape}, got {tuple(output.shape)}"
        )
    return output.to(torch.float32)
