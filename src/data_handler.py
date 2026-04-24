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


def build_subspacenet_input(
    X: torch.Tensor,
    system_model_params: SystemModelParams,
    tau: int,
    model_type: str = "SubspaceNet",
):
    """Builds the SubspaceNet input tensor for either ULA or NULA+LRMC paths."""
    if model_type.startswith("SubspaceNetSSFusionEspritPhase1p1p1"):
        return build_ss_fusion_phase1p1_input(X=X, system_model_params=system_model_params)
    if model_type.startswith("SubspaceNetSSFusionEspritPhase1p1"):
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
