"""Subspace-Net 
Details
----------
    Name: data_handler.py
    Authors: D. H. Shmuel
    Created: 01/10/21
    Edited: 03/06/23

Purpose:
--------
    This scripts handle the creation and processing of synthetic datasets
    based on specified parameters and model types.
    It includes functions for generating datasets, reading data from files,
    computing autocorrelation matrices, and creating covariance tensors.

Attributes:
-----------
    Samples (from src.signal_creation): A class for creating samples used in dataset generation.

    The script defines the following functions:
    * create_dataset: Generates a synthetic dataset based on the specified parameters and model type.
    * read_data: Reads data from a file specified by the given path.
    * autocorrelation_matrix: Computes the autocorrelation matrix for a given lag of the input samples.
    * create_autocorrelation_tensor: Returns a tensor containing all the autocorrelation matrices for lags 0 to tau.
    * create_cov_tensor: Creates a 3D tensor containing the real part,
        imaginary part, and phase component of the covariance matrix.
    * set_dataset_filename: Returns the generic suffix of the datasets filename.

"""

# Imports
import copy
import hashlib
import json
import torch
import numpy as np
import itertools
from tqdm import tqdm
from src.signal_creation import Samples
from pathlib import Path
from src.system_model import SystemModelParams
from src.lrmc import (
    complete_nula_covariance,
    complete_nula_covariance_from_covariance,
    complete_rowwise_nula_covariance,
    compute_sample_covariance,
    covariance_to_autocorrelation_tensor,
    ensure_hermitian,
)
from src.ss_fusion_phase1p1 import build_ss_fusion_phase1p1_input

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def _is_2d_geometry(system_model_params: SystemModelParams) -> bool:
    geometry_name = getattr(system_model_params, "geometry_name", None)
    physical_sensor_positions_2d = getattr(
        system_model_params, "physical_sensor_positions_2d", None
    )
    return bool(
        physical_sensor_positions_2d is not None
        or (
            isinstance(geometry_name, str)
            and geometry_name.startswith("mimo_2d_12ch")
        )
    )


def _sample_constrained_angles(
    count: int,
    lower: float,
    upper: float,
    resolution: float,
    min_gap: float,
    fixed_gap: float = None,
):
    if count <= 0:
        return np.array([], dtype=float)
    decimals = max(0, int(np.ceil(-np.log10(resolution)))) if resolution < 1 else 0
    if fixed_gap is not None:
        fixed_gap = float(fixed_gap)
        if fixed_gap < 0:
            raise ValueError("_sample_constrained_angles: fixed_gap must be non-negative")
        span = (count - 1) * fixed_gap
        if upper - lower < span:
            raise ValueError(
                "_sample_constrained_angles: requested fixed gap does not fit inside the angular range"
            )
        start_candidates = np.arange(lower, upper - span + resolution * 0.5, resolution)
        if start_candidates.size == 0:
            raise ValueError(
                "_sample_constrained_angles: no valid start positions for requested fixed gap"
            )
        start = float(np.random.choice(start_candidates))
        values = start + fixed_gap * np.arange(count, dtype=float)
        return np.round(values, decimals=decimals)
    while True:
        values = np.round(np.random.uniform(low=lower, high=upper, size=count), decimals=decimals)
        values.sort()
        if count <= 1:
            return values
        diff_angles = np.array([np.abs(values[i + 1] - values[i]) for i in range(count - 1)])
        if np.sum(diff_angles >= min_gap) == count - 1:
            return values


def _sample_2d_doa_pairs(system_model_params: SystemModelParams):
    lower = float(getattr(system_model_params, "doa_min", -15.0))
    upper = float(getattr(system_model_params, "doa_max", 15.0))
    elevation_lower = float(getattr(system_model_params, "elevation_min", lower))
    elevation_upper = float(getattr(system_model_params, "elevation_max", upper))
    resolution = float(getattr(system_model_params, "doa_resolution", 0.01))
    min_gap = float(getattr(system_model_params, "min_doa_gap", 5.0))
    fixed_gap = getattr(system_model_params, "fixed_doa_gap", None)
    if fixed_gap is not None:
        fixed_gap = float(fixed_gap)
    azimuths = _sample_constrained_angles(
        count=int(system_model_params.M),
        lower=lower,
        upper=upper,
        resolution=resolution,
        min_gap=min_gap,
        fixed_gap=fixed_gap,
    )
    elevations = np.round(
        np.random.uniform(low=elevation_lower, high=elevation_upper, size=int(system_model_params.M)),
        decimals=max(0, int(np.ceil(-np.log10(resolution)))) if resolution < 1 else 0,
    )
    doa_pairs = list(zip(azimuths.tolist(), elevations.tolist()))
    return doa_pairs


def _resolve_canonical_row_indices(system_model_params: SystemModelParams):
    row_groups = getattr(system_model_params, "row_groups", None)
    if row_groups is None:
        geometry_name = getattr(system_model_params, "geometry_name", None)
        physical_sensor_positions_2d = getattr(
            system_model_params, "physical_sensor_positions_2d", None
        )
        if physical_sensor_positions_2d is not None or (
            isinstance(geometry_name, str)
            and geometry_name.startswith("mimo_2d_12ch")
        ):
            row_groups = ((0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 10, 11))
    if not row_groups:
        return None
    canonical_group = getattr(system_model_params, "canonical_row_group", None)
    if canonical_group is None:
        canonical_group = len(row_groups) - 1
    canonical_group = int(max(0, min(int(canonical_group), len(row_groups) - 1)))
    return [int(index) for index in row_groups[canonical_group]]


def _extract_canonical_row_snapshot(
    X: torch.Tensor, system_model_params: SystemModelParams
):
    row_indices = _resolve_canonical_row_indices(system_model_params)
    if not row_indices:
        return X
    return X[row_indices, :]


def build_subspacenet_input(
    X: torch.Tensor,
    system_model_params: SystemModelParams,
    tau: int,
    model_type: str = "SubspaceNet",
):
    """Builds the SubspaceNet input tensor for either ULA or NULA+LRMC paths."""
    if model_type.startswith("SubspaceNetSingleRow"):
        row_snapshot = _extract_canonical_row_snapshot(X, system_model_params)
        return create_autocorrelation_tensor(row_snapshot, tau).to(torch.float)

    if model_type.startswith("SubspaceNetSSFusion"):
        return build_ss_fusion_phase1p1_input(X=X, system_model_params=system_model_params)

    if getattr(system_model_params, "use_lrmc", False):
        sensor_positions = getattr(system_model_params, "sensor_positions", None)
        virtual_size = getattr(system_model_params, "virtual_array_size", None)
        if sensor_positions is None or virtual_size is None:
            raise ValueError(
                "build_subspacenet_input: sensor_positions and virtual_array_size are required when use_lrmc=True"
            )
        rank = getattr(system_model_params, "lrmc_rank", None)
        if rank is None:
            rank = int(system_model_params.M) + 1
        # Use the explicit sample covariance path so ultra-low snapshot cases such
        # as T=1 stay consistent with the hardened classical pipeline.
        covariance = compute_sample_covariance(
            np.asarray(X.cpu().numpy(), dtype=np.complex128)
        )
        covariance = ensure_hermitian(covariance)
        row_groups = getattr(system_model_params, "row_groups", None)
        ss_num_subarrays = getattr(system_model_params, "ss_num_subarrays", None)
        ss_row_subset = getattr(system_model_params, "ss_row_subset", None)
        covariance_mode = str(
            getattr(system_model_params, "covariance_mode", "lrmc")
        ).lower()
        if row_groups and covariance_mode == "ss_then_lrmc":
            _, _, _, completed_covariance, diagnostics = complete_rowwise_nula_covariance(
                covariance=covariance,
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
                variant="average_raw",
                ss_num_subarrays=ss_num_subarrays,
                ss_row_subset=ss_row_subset,
            )
        elif row_groups and covariance_mode in {"lrmc_only", "lrmc"}:
            _, _, _, completed_covariance, diagnostics = complete_rowwise_nula_covariance(
                covariance=covariance,
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
                variant="canonical",
                ss_num_subarrays=ss_num_subarrays,
                ss_row_subset=ss_row_subset,
            )
        elif row_groups and covariance_mode == "lrmc_then_ss":
            _, _, _, completed_covariance, diagnostics = complete_rowwise_nula_covariance(
                covariance=covariance,
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
                variant="average_completed",
                ss_num_subarrays=ss_num_subarrays,
                ss_row_subset=ss_row_subset,
            )
        else:
            _, _, _, completed_covariance, diagnostics = complete_nula_covariance_from_covariance(
                covariance=covariance,
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
            )
        if diagnostics.min_singular_value is not None and diagnostics.min_singular_value <= 0:
            raise AssertionError(
                "build_subspacenet_input: completed covariance is numerically unstable"
            )
        return covariance_to_autocorrelation_tensor(
            ensure_hermitian(completed_covariance), tau
        )
    return create_autocorrelation_tensor(X, tau).to(torch.float)


def create_dataset(
    system_model_params: SystemModelParams,
    samples_size: float,
    model_type: str,
    tau: int = None,
    save_datasets: bool = False,
    datasets_path: Path = None,
    true_doa: list = None,
    phase: str = None,
):
    """
    Generates a synthetic dataset based on the specified parameters and model type.

    Args:
    -----
        system_model_params (SystemModelParams): an instance of SystemModelParams
        samples_size (float): The size of the dataset.
        tau (int): The number of lags for auto-correlation (relevant only for SubspaceNet model).
        model_type (str): The type of the model.
        save_datasets (bool, optional): Specifies whether to save the dataset. Defaults to False.
        datasets_path (Path, optional): The path for saving the dataset. Defaults to None.
        true_doa (list, optional): Predefined angles. Defaults to None.
        phase (str, optional): The phase of the dataset (test or training phase for CNN model). Defaults to None.

    Returns:
    --------
        tuple: A tuple containing the desired dataset comprised of (X-samples, Y-labels).

    """
    generic_dataset = []
    model_dataset = []
    samples_model = Samples(system_model_params)
    # Generate permutations for CNN model training dataset
    if model_type.startswith("DeepCNN") and phase.startswith("train"):
        doa_permutations = []
        angles_grid = np.linspace(start=-90, stop=90, num=361)
        for comb in itertools.combinations(angles_grid, system_model_params.M):
            doa_permutations.append(list(comb))

    if model_type.startswith("DeepCNN") and phase.startswith("train"):
        for i, doa in tqdm(enumerate(doa_permutations)):
            # Samples model creation
            samples_model.set_doa(doa)
            # Observations matrix creation
            X = torch.tensor(
                samples_model.samples_creation(
                    noise_mean=0, noise_variance=1, signal_mean=0, signal_variance=1
                )[0],
                dtype=torch.complex64,
            )
            X_model = create_cov_tensor(X)
            # Ground-truth creation
            Y = torch.zeros_like(torch.tensor(angles_grid))
            for angle in doa:
                Y[list(angles_grid).index(angle)] = 1
            model_dataset.append((X_model, Y))
            generic_dataset.append((X, Y))
    else:
        for i in tqdm(range(samples_size)):
            # Samples model creation
            if _is_2d_geometry(system_model_params):
                if true_doa is None:
                    doa_pairs = _sample_2d_doa_pairs(system_model_params)
                else:
                    doa_pairs = true_doa
                samples_model.set_doa_2d(doa_pairs)
            else:
                if true_doa is None:
                    doa_values = _sample_constrained_angles(
                        count=int(system_model_params.M),
                        lower=float(getattr(system_model_params, "doa_min", -90.0)),
                        upper=float(getattr(system_model_params, "doa_max", 90.0)),
                        resolution=float(getattr(system_model_params, "doa_resolution", 0.01)),
                        min_gap=float(getattr(system_model_params, "min_doa_gap", 15.0)),
                        fixed_gap=getattr(system_model_params, "fixed_doa_gap", None),
                    )
                    samples_model.set_doa(doa_values)
                else:
                    samples_model.set_doa(true_doa)
            # Observations matrix creation
            X = torch.tensor(
                samples_model.samples_creation(
                    noise_mean=0, noise_variance=1, signal_mean=0, signal_variance=1
                )[0],
                dtype=torch.complex64,
            )
            if model_type.startswith("SubspaceNet"):
                # Generate the model input tensor from either direct autocorrelation
                # or NULA LRMC completed virtual covariance.
                X_model = build_subspacenet_input(
                    X=X,
                    system_model_params=system_model_params,
                    tau=tau,
                    model_type=model_type,
                )
            elif model_type.startswith("DeepCNN") and phase.startswith("test"):
                # Generate 3d covariance parameters tensor
                X_model = create_cov_tensor(X)
            else:
                X_model = X
            # Ground-truth creation
            Y = torch.tensor(samples_model.doa, dtype=torch.float64)
            generic_dataset.append((X, Y))
            model_dataset.append((X_model, Y))

    if save_datasets:
        model_dataset_filename = f"{model_type}_DataSet" + set_dataset_filename(
            system_model_params, samples_size
        )
        generic_dataset_filename = f"Generic_DataSet" + set_dataset_filename(
            system_model_params, samples_size
        )
        samples_model_filename = f"samples_model" + set_dataset_filename(
            system_model_params, samples_size
        )

        torch.save(obj=model_dataset, f=datasets_path / phase / model_dataset_filename)
        torch.save(
            obj=generic_dataset, f=datasets_path / phase / generic_dataset_filename
        )
        if phase.startswith("test"):
            torch.save(
                obj=samples_model, f=datasets_path / phase / samples_model_filename
            )

    return model_dataset, generic_dataset, samples_model


def _system_model_params_from_template_dict(template: dict):
    params = SystemModelParams()
    for name, value in template.get("system_model", {}).items():
        params.set_parameter(name, value)
    params.set_parameter("template_name", template.get("template_name"))
    return params


def _generate_single_sample(
    system_model_params: SystemModelParams,
    model_type: str,
    tau: int,
):
    samples_model = Samples(system_model_params)
    if _is_2d_geometry(system_model_params):
        doa_pairs = _sample_2d_doa_pairs(system_model_params)
        samples_model.set_doa_2d(doa_pairs)
    else:
        doa_values = _sample_constrained_angles(
            count=int(system_model_params.M),
            lower=float(getattr(system_model_params, "doa_min", -90.0)),
            upper=float(getattr(system_model_params, "doa_max", 90.0)),
            resolution=float(getattr(system_model_params, "doa_resolution", 0.01)),
            min_gap=float(getattr(system_model_params, "min_doa_gap", 15.0)),
            fixed_gap=getattr(system_model_params, "fixed_doa_gap", None),
        )
        samples_model.set_doa(doa_values)

    X = torch.tensor(
        samples_model.samples_creation(
            noise_mean=0, noise_variance=1, signal_mean=0, signal_variance=1
        )[0],
        dtype=torch.complex64,
    )
    if model_type.startswith("SubspaceNet"):
        X_model = build_subspacenet_input(
            X=X,
            system_model_params=system_model_params,
            tau=tau,
            model_type=model_type,
        )
    elif model_type.startswith("DeepCNN"):
        X_model = create_cov_tensor(X)
    else:
        X_model = X
    Y = torch.tensor(samples_model.doa, dtype=torch.float64)
    return (X_model, Y), (X, Y)


def _convert_generic_dataset_to_model_dataset(
    generic_dataset: list,
    system_model_params: SystemModelParams,
    model_type: str,
    tau: int,
):
    model_dataset = []
    for X, Y in generic_dataset:
        X_model = build_subspacenet_input(
            X=X,
            system_model_params=system_model_params,
            tau=tau,
            model_type=model_type,
        )
        model_dataset.append((X_model, Y))
    return model_dataset


def _sample_from_generic_dataset(
    generic_dataset: list,
    sample_count: int,
):
    if sample_count <= 0:
        return []
    if sample_count <= len(generic_dataset):
        indices = np.random.choice(len(generic_dataset), size=sample_count, replace=False)
    else:
        indices = np.random.choice(len(generic_dataset), size=sample_count, replace=True)
    return [generic_dataset[int(index)] for index in indices]


def _mixed_dataset_cache_key(
    system_model_params: SystemModelParams,
    dataset_settings: dict,
    model_type: str,
    tau: int,
):
    payload = {
        "template_name": getattr(system_model_params, "template_name", None),
        "signal_type": getattr(system_model_params, "signal_type", None),
        "array_spacing": getattr(system_model_params, "array_spacing", None),
        "geometry_name": getattr(system_model_params, "geometry_name", None),
        "model_type": model_type,
        "tau": tau,
        "dataset": dataset_settings,
    }
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=True)
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]


def _mixed_dataset_file_paths(datasets_path: Path, model_type: str, cache_key: str):
    train_model = datasets_path / "train" / f"{model_type}_MixedTrain_{cache_key}.pt"
    test_model = datasets_path / "test" / f"{model_type}_MixedTest_{cache_key}.pt"
    test_generic = datasets_path / "test" / f"Generic_MixedTest_{cache_key}.pt"
    metadata = datasets_path / "test" / f"mixed_samples_model_{cache_key}.pt"
    return train_model, test_model, test_generic, metadata


def load_mixed_datasets(
    system_model_params: SystemModelParams,
    model_type: str,
    tau: int,
    dataset_settings: dict,
    datasets_path: Path,
    is_training: bool = False,
):
    cache_key = _mixed_dataset_cache_key(
        system_model_params=system_model_params,
        dataset_settings=dataset_settings,
        model_type=model_type,
        tau=tau,
    )
    train_model, test_model, test_generic, metadata = _mixed_dataset_file_paths(
        datasets_path, model_type, cache_key
    )
    datasets = []
    if is_training:
        if not train_model.exists():
            raise Exception("load_mixed_datasets: Training dataset doesn't exist")
        datasets.append(read_data(train_model))
    if not test_model.exists():
        raise Exception("load_mixed_datasets: Test dataset doesn't exist")
    if not test_generic.exists():
        raise Exception("load_mixed_datasets: Generic test dataset doesn't exist")
    if not metadata.exists():
        raise Exception("load_mixed_datasets: Mixed dataset metadata doesn't exist")
    datasets.append(read_data(test_model))
    datasets.append(read_data(test_generic))
    datasets.append(read_data(metadata))
    return datasets


def _load_or_create_generic_dataset_from_template(
    template_path: Path,
    phase: str,
):
    with template_path.open("r", encoding="utf-8-sig") as handle:
        template = json.load(handle)
    template["template_name"] = template_path.stem
    system_model_params = _system_model_params_from_template_dict(template)
    dataset_settings = template["dataset"]
    datasets_path = template_path.parents[4] / "data" / "datasets" / template["scenario_data_path"]
    sample_count = (
        dataset_settings["samples_size"]
        if phase == "train"
        else int(dataset_settings["train_test_ratio"] * dataset_settings["samples_size"])
    )
    generic_filenames = get_dataset_filename_candidates(
        "Generic_DataSet", system_model_params, sample_count
    )
    candidate_paths = [datasets_path / phase / name for name in generic_filenames]
    try:
        return read_first_existing(candidate_paths)
    except FileNotFoundError:
        (datasets_path / "train").mkdir(parents=True, exist_ok=True)
        (datasets_path / "test").mkdir(parents=True, exist_ok=True)
        _, generic_dataset, _ = create_dataset(
            system_model_params=system_model_params,
            samples_size=sample_count,
            model_type="Classical",
            tau=template.get("model", {}).get("tau", 8),
            save_datasets=True,
            datasets_path=datasets_path,
            true_doa=None,
            phase=phase,
        )
        return generic_dataset


def _normalized_split_counts(total_count: int, test_ratio: float):
    test_count = int(round(total_count * test_ratio))
    train_count = int(total_count - test_count)
    return train_count, test_count


def _weighted_choice(weight_mapping: dict):
    values = list(weight_mapping.keys())
    weights = np.asarray([float(weight_mapping[key]) for key in values], dtype=float)
    weights = weights / np.sum(weights)
    return values[int(np.random.choice(len(values), p=weights))]


def _generate_weighted_random_component(
    count: int,
    base_system_model_params: SystemModelParams,
    model_type: str,
    tau: int,
    weighted_random_config: dict,
    split_name: str,
):
    model_dataset = []
    generic_dataset = []
    coherence_weights = weighted_random_config.get("coherence_weights", {})
    snr_weights = weighted_random_config.get("snr_weights", {})
    gap_group_weights = weighted_random_config.get("gap_group_weights", [])
    if not coherence_weights or not snr_weights or not gap_group_weights:
        raise ValueError(
            "_generate_weighted_random_component: coherence_weights, snr_weights, "
            "and gap_group_weights are required"
        )

    for _ in tqdm(range(count), desc=f"mixed-random::{split_name}"):
        params = copy.deepcopy(base_system_model_params)
        coherence_key = _weighted_choice(coherence_weights)
        coherence_gap_groups = weighted_random_config.get(
            f"{coherence_key}_gap_group_weights", gap_group_weights
        )
        coherence_snr_weights = weighted_random_config.get(
            f"{coherence_key}_snr_weights", snr_weights
        )
        gap_group_probabilities = np.asarray(
            [float(group["weight"]) for group in coherence_gap_groups], dtype=float
        )
        gap_group_probabilities = gap_group_probabilities / np.sum(gap_group_probabilities)
        params.set_parameter(
            "signal_nature",
            "coherent" if coherence_key == "coherent" else "non-coherent",
        )
        params.set_parameter("snr", float(_weighted_choice(coherence_snr_weights)))
        group_index = int(
            np.random.choice(len(coherence_gap_groups), p=gap_group_probabilities)
        )
        gap_group = coherence_gap_groups[group_index]
        gaps = [float(value) for value in gap_group.get("gaps", [])]
        if not gaps:
            raise ValueError("_generate_weighted_random_component: gap group missing gaps")
        if len(gaps) == 1:
            selected_gap = float(gaps[0])
        else:
            selected_gap = float(np.round(np.random.uniform(min(gaps), max(gaps)), 2))
        params.set_parameter("min_doa_gap", selected_gap)
        params.set_parameter("fixed_doa_gap", selected_gap)
        model_sample, generic_sample = _generate_single_sample(
            system_model_params=params,
            model_type=model_type,
            tau=tau,
        )
        model_dataset.append(model_sample)
        generic_dataset.append(generic_sample)
    return model_dataset, generic_dataset


def create_mixed_dataset(
    system_model_params: SystemModelParams,
    dataset_settings: dict,
    model_type: str,
    tau: int,
    save_datasets: bool = False,
    datasets_path: Path = None,
):
    mixed_config = dataset_settings.get("mixed_dataset")
    if mixed_config is None:
        raise ValueError("create_mixed_dataset: dataset_settings.mixed_dataset is required")
    train_ratio = 1.0 - float(dataset_settings.get("train_test_ratio", 0.2))
    test_ratio = float(dataset_settings.get("train_test_ratio", 0.2))

    train_model_dataset = []
    test_model_dataset = []
    test_generic_dataset = []
    metadata = {
        "mixed_dataset": mixed_config,
        "train_samples_size": 0,
        "test_samples_size": 0,
    }

    for cell_config in mixed_config.get("stratified_cells", []):
        total_samples = int(cell_config["total_samples"])
        train_count, test_count = _normalized_split_counts(total_samples, test_ratio)
        template_path = Path(cell_config["template_path"])
        train_generic_source = _load_or_create_generic_dataset_from_template(
            template_path, phase="train"
        )
        test_generic_source = _load_or_create_generic_dataset_from_template(
            template_path, phase="test"
        )
        sampled_train_generic = _sample_from_generic_dataset(
            train_generic_source, train_count
        )
        sampled_test_generic = _sample_from_generic_dataset(
            test_generic_source, test_count
        )
        train_model_dataset.extend(
            _convert_generic_dataset_to_model_dataset(
                sampled_train_generic,
                system_model_params=system_model_params,
                model_type=model_type,
                tau=tau,
            )
        )
        converted_test_model = _convert_generic_dataset_to_model_dataset(
            sampled_test_generic,
            system_model_params=system_model_params,
            model_type=model_type,
            tau=tau,
        )
        test_model_dataset.extend(converted_test_model)
        test_generic_dataset.extend(sampled_test_generic)
        metadata["train_samples_size"] += len(sampled_train_generic)
        metadata["test_samples_size"] += len(sampled_test_generic)

    weighted_random_config = mixed_config.get("weighted_random")
    if weighted_random_config is not None:
        total_random_samples = int(weighted_random_config["total_samples"])
        random_train_count, random_test_count = _normalized_split_counts(
            total_random_samples, test_ratio
        )
        random_train_model, _ = _generate_weighted_random_component(
            count=random_train_count,
            base_system_model_params=system_model_params,
            model_type=model_type,
            tau=tau,
            weighted_random_config=weighted_random_config,
            split_name="train",
        )
        random_test_model, random_test_generic = _generate_weighted_random_component(
            count=random_test_count,
            base_system_model_params=system_model_params,
            model_type=model_type,
            tau=tau,
            weighted_random_config=weighted_random_config,
            split_name="test",
        )
        train_model_dataset.extend(random_train_model)
        test_model_dataset.extend(random_test_model)
        test_generic_dataset.extend(random_test_generic)
        metadata["train_samples_size"] += len(random_train_model)
        metadata["test_samples_size"] += len(random_test_model)

    if save_datasets:
        cache_key = _mixed_dataset_cache_key(
            system_model_params=system_model_params,
            dataset_settings=dataset_settings,
            model_type=model_type,
            tau=tau,
        )
        train_model, test_model, test_generic, metadata_path = _mixed_dataset_file_paths(
            datasets_path, model_type, cache_key
        )
        ensure_train = train_model.parent
        ensure_test = test_model.parent
        ensure_train.mkdir(parents=True, exist_ok=True)
        ensure_test.mkdir(parents=True, exist_ok=True)
        torch.save(obj=train_model_dataset, f=train_model)
        torch.save(obj=test_model_dataset, f=test_model)
        torch.save(obj=test_generic_dataset, f=test_generic)
        torch.save(obj=metadata, f=metadata_path)

    return train_model_dataset, test_model_dataset, test_generic_dataset, metadata


# def read_data(Data_path: str) -> torch.Tensor:
def read_data(path: str):
    """
    Reads data from a file specified by the given path.

    Args:
    -----
        path (str): The path to the data file.

    Returns:
    --------
        torch.Tensor: The loaded data.

    Raises:
    -------
        None

    Examples:
    ---------
        >>> path = "data.pt"
        >>> read_data(path)

    """
    assert isinstance(path, (str, Path))
    data = torch.load(path)
    return data


def read_first_existing(paths):
    """
    Reads the first existing path from a list of candidate dataset paths.

    Args:
    -----
        paths (list[Path]): Candidate paths to attempt.

    Returns:
    --------
        torch.Tensor: The loaded data.

    Raises:
    -------
        FileNotFoundError: If none of the candidate paths exists.
    """
    for path in paths:
        if Path(path).exists():
            return read_data(path)
    raise FileNotFoundError(f"None of the candidate paths exist: {paths}")


# def autocorrelation_matrix(X: torch.Tensor, lag: int) -> torch.Tensor:
def autocorrelation_matrix(X: torch.Tensor, lag: int):
    """
    Computes the autocorrelation matrix for a given lag of the input samples.

    Args:
    -----
        X (torch.Tensor): Samples matrix input with shape [N, T].
        lag (int): The requested delay of the autocorrelation calculation.

    Returns:
    --------
        torch.Tensor: The autocorrelation matrix for the given lag.

    """
    Rx_lag = torch.zeros(X.shape[0], X.shape[0], dtype=torch.complex128).to(device)
    for t in range(X.shape[1] - lag):
        # meu = torch.mean(X,1)
        x1 = torch.unsqueeze(X[:, t], 1).to(device)
        x2 = torch.t(torch.unsqueeze(torch.conj(X[:, t + lag]), 1)).to(device)
        Rx_lag += torch.matmul(x1 - torch.mean(X), x2 - torch.mean(X)).to(device)
    Rx_lag = Rx_lag / (X.shape[-1] - lag)
    Rx_lag = torch.cat((torch.real(Rx_lag), torch.imag(Rx_lag)), 0)
    return Rx_lag


# def create_autocorrelation_tensor(X: torch.Tensor, tau: int) -> torch.Tensor:
def create_autocorrelation_tensor(X: torch.Tensor, tau: int):
    """
    Returns a tensor containing all the autocorrelation matrices for lags 0 to tau.

    Args:
    -----
        X (torch.Tensor): Observation matrix input with size (BS, N, T).
        tau (int): Maximal time difference for the autocorrelation tensor.

    Returns:
    --------
        torch.Tensor: Tensor containing all the autocorrelation matrices,
                    with size (Batch size, tau, 2N, N).

    Raises:
    -------
        None

    """
    Rx_tau = []
    for i in range(tau):
        Rx_tau.append(autocorrelation_matrix(X, lag=i))
    Rx_autocorr = torch.stack(Rx_tau, dim=0)
    return Rx_autocorr


# def create_cov_tensor(X: torch.Tensor) -> torch.Tensor:
def create_cov_tensor(X: torch.Tensor):
    """
    Creates a 3D tensor of size (NxNx3) containing the real part, imaginary part, and phase component of the covariance matrix.

    Args:
    -----
        X (torch.Tensor): Observation matrix input with size (N, T).

    Returns:
    --------
        Rx_tensor (torch.Tensor): Tensor containing the auto-correlation matrices, with size (Batch size, N, N, 3).

    Raises:
    -------
        None

    """
    Rx = torch.cov(X)
    Rx_tensor = torch.stack((torch.real(Rx), torch.imag(Rx), torch.angle(Rx)), 2)
    return Rx_tensor


def load_datasets(
    system_model_params: SystemModelParams,
    model_type: str,
    samples_size: float,
    datasets_path: Path,
    train_test_ratio: float,
    is_training: bool = False,
):
    """
    Load different datasets based on the specified parameters and phase.

    Args:
    -----
        system_model_params (SystemModelParams): an instance of SystemModelParams.
        model_type (str): The type of the model.
        samples_size (float): The size of the overall dataset.
        datasets_path (Path): The path to the datasets.
        train_test_ratio (float): The ration between train and test datasets.
        is_training (bool): Specifies whether to load the training dataset.

    Returns:
    --------
        List: A list containing the loaded datasets.

    """
    datasets = []
    # Define test set size
    test_samples_size = int(train_test_ratio * samples_size)
    # Generate datasets filenames
    model_dataset_filenames = get_dataset_filename_candidates(
        f"{model_type}_DataSet", system_model_params, test_samples_size
    )
    generic_dataset_filenames = get_dataset_filename_candidates(
        "Generic_DataSet", system_model_params, test_samples_size
    )
    samples_model_filenames = get_dataset_filename_candidates(
        "samples_model", system_model_params, test_samples_size
    )

    # Whether to load the training dataset
    if is_training:
        # Load training dataset
        try:
            model_trainingset_filenames = get_dataset_filename_candidates(
                f"{model_type}_DataSet", system_model_params, samples_size
            )
            train_dataset = read_first_existing(
                [datasets_path / "train" / name for name in model_trainingset_filenames]
            )
            datasets.append(train_dataset)
        except:
            raise Exception("load_datasets: Training dataset doesn't exist")
    # Load test dataset
    try:
        test_dataset = read_first_existing(
            [datasets_path / "test" / name for name in model_dataset_filenames]
        )
        datasets.append(test_dataset)
    except:
        raise Exception("load_datasets: Test dataset doesn't exist")
    # Load generic test dataset
    try:
        generic_test_dataset = read_first_existing(
            [datasets_path / "test" / name for name in generic_dataset_filenames]
        )
        datasets.append(generic_test_dataset)
    except:
        raise Exception("load_datasets: Generic test dataset doesn't exist")
    # Load samples models
    try:
        samples_model = read_first_existing(
            [datasets_path / "test" / name for name in samples_model_filenames]
        )
        datasets.append(samples_model)
    except:
        raise Exception("load_datasets: Samples model dataset doesn't exist")
    return datasets


def get_dataset_filename_candidates(
    prefix: str, system_model_params: SystemModelParams, samples_size: float
):
    """
    Returns supported dataset filename variants for backward compatibility.

    Args:
    -----
        prefix (str): Dataset filename prefix.
        system_model_params (SystemModelParams): an instance of SystemModelParams.
        samples_size (float): The size of the overall dataset.

    Returns:
    --------
        list[str]: Candidate filenames ordered from newest to legacy format.
    """
    filenames = [prefix + set_dataset_filename(system_model_params, samples_size)]
    legacy_suffix_filename = (
        f"_{system_model_params.signal_type}_"
        + f"{system_model_params.signal_nature}_{samples_size}_M={system_model_params.M}_"
        + f"N={system_model_params.N}_T={system_model_params.T}_SNR={system_model_params.snr}_"
        + f"eta={system_model_params.eta}_sv_noise_var{system_model_params.sv_noise_var}_"
        + ".h5"
    )
    filenames.append(prefix + legacy_suffix_filename)
    return filenames


def set_dataset_filename(system_model_params: SystemModelParams, samples_size: float):
    """Returns the generic suffix of the datasets filename.

    Args:
    -----
        system_model_params (SystemModelParams): an instance of SystemModelParams.
        samples_size (float): The size of the overall dataset.

    Returns:
    --------
        str: Suffix dataset filename
    """
    suffix_filename = (
        f"_{system_model_params.signal_type}_"
        + f"{system_model_params.signal_nature}_{samples_size}_M={system_model_params.M}_"
        + f"N={system_model_params.N}_T={system_model_params.T}_SNR={system_model_params.snr}_"
        + f"eta={system_model_params.eta}_sv_noise_var{system_model_params.sv_noise_var}_"
        + f"bias={system_model_params.bias}_"
        + get_experiment_suffix(system_model_params)
        + ".h5"
    )
    return suffix_filename


def get_experiment_suffix(system_model_params: SystemModelParams):
    """Returns an optional suffix for non-default experiment metadata."""
    suffix = ""
    template_name = getattr(system_model_params, "template_name", None)
    if template_name:
        suffix += f"tpl={template_name}_"
    geometry_name = getattr(system_model_params, "geometry_name", None)
    if geometry_name:
        suffix += f"geo={geometry_name}_"
    sensor_positions = getattr(system_model_params, "sensor_positions", None)
    if sensor_positions is not None:
        geometry = "-".join(str(int(pos)) for pos in sensor_positions)
        suffix += f"arr={geometry}_"
    array_spacing = getattr(system_model_params, "array_spacing", None)
    if array_spacing is not None:
        suffix += f"d={array_spacing}_"
    virtual_size = getattr(system_model_params, "virtual_array_size", None)
    if virtual_size is not None:
        suffix += f"v={virtual_size}_"
    doa_min = getattr(system_model_params, "doa_min", None)
    doa_max = getattr(system_model_params, "doa_max", None)
    min_doa_gap = getattr(system_model_params, "min_doa_gap", None)
    fixed_doa_gap = getattr(system_model_params, "fixed_doa_gap", None)
    if doa_min is not None and doa_max is not None:
        suffix += f"fov={doa_min}to{doa_max}_"
    if min_doa_gap is not None:
        suffix += f"gap={min_doa_gap}_"
    if fixed_doa_gap is not None:
        suffix += f"fixedgap={fixed_doa_gap}_"
    ss_num_subarrays = getattr(system_model_params, "ss_num_subarrays", None)
    ss_row_subset = getattr(system_model_params, "ss_row_subset", None)
    if ss_num_subarrays is not None:
        suffix += f"ssn={int(ss_num_subarrays)}_"
    if ss_row_subset is not None:
        subset = "-".join(str(int(index)) for index in ss_row_subset)
        suffix += f"ssrows={subset}_"
    if getattr(system_model_params, "use_lrmc", False):
        rank = getattr(system_model_params, "lrmc_rank", None)
        if rank is None:
            rank = int(system_model_params.M) + 1
        suffix += (
            f"mc={getattr(system_model_params, 'lrmc_solver', 'svd')}_"
            + f"r={rank}_"
        )
    # Keep Windows paths short enough for torch.save/open while preserving uniqueness.
    if len(suffix) > 72:
        import hashlib

        digest = hashlib.sha1(suffix.encode("utf-8")).hexdigest()[:12]
        suffix = f"tpl={template_name or 'exp'}_{digest}_"
    return suffix
