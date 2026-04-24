"""Subspace-Net 
Details
----------
    Name: methods.py
    Authors: D. H. Shmuel
    Created: 01/10/21
    Edited: 03/06/23

Description:
-----------
This script contains the implementation of there subspace Doa estimation algorithms:
1. MUSIC (Multiple Signal Classification)
2. RootMUSIC
3. Esprit
and the implementation of the MVDR beamformer.
These algorithms are used to estimate the directions from which signals arrive at an array of sensors.

Purpose:
--------
The purpose of this script is to provide implementations of the MUSIC, RootMUSIC, Esprit and MVDR algorithms for DoA estimation.
These algorithms utilize subspace methods and covariance matrices to estimate the angles of arrival of signals in both broadband and narrowband scenarios.

Classes:
--------
- SubspaceMethod: A base class providing common functionality and methods for the subspace-based DoA estimation algorithms.
- MUSIC: A class representing the model-based MUSIC algorithm for DoA estimation.
- RootMUSIC: A class representing the model-based RootMUSIC algorithm for DoA estimation.
- Esprit: A class representing the model-based Esprit algorithm for DoA estimation.
- MVDR: A class representing the model-based MVDR algorithm for DoA estimation.

Methods:
--------
- SubspaceMethod:
  - calculate_covariance: Calculates the covariance matrix based on the given input samples.
  - subspace_separation: Performs subspace separation to obtain signal and noise subspaces.
  - spectrum_calculation: Calculates the MUSIC spectrum based on the noise subspace and steering vectors.
- MUSIC:
  - broadband: Implements the model-based MUSIC algorithm in the broadband scenario.
  - narrowband: Implements the model-based MUSIC algorithm in the narrowband scenario.
- RootMUSIC:
  - narrowband: Implements the model-based narrow-band RootMUSIC algorithm.
  - extract_angels_from_roots: Extracts the DoA predictions from the roots of the polynomial.
- Esprit:
  - narrowband: Implements the model-based narrow-band Esprit algorithm.
- MVDR:
  - narrowband: Implements the narrow-band MVDR beamformer algorithm with spatial smoothing.

"""

# Imports
import copy
import numpy as np
try:
    import scipy.signal as scipy_signal
except Exception:
    scipy_signal = None
from src.lrmc import (
    DEFAULT_ROW_GROUPS_2D,
    average_covariance_blocks,
    complete_nula_covariance,
    complete_nula_covariance_from_covariance,
    complete_rowwise_nula_covariance,
    compute_sample_covariance,
    resolve_row_subset,
    select_covariance_blocks,
    split_covariance_into_blocks,
)
from src.models import SubspaceNet
from src.system_model import SystemModel
from src.utils import sum_of_diag, find_roots, R2D


def _find_peaks_fallback(spectrum: np.ndarray):
    """Return local-maxima indices when SciPy peak finding is unavailable."""
    spectrum = np.asarray(spectrum).reshape(-1)
    if spectrum.size < 3:
        return np.arange(spectrum.size, dtype=int)

    peaks = []
    for idx in range(1, spectrum.size - 1):
        left = spectrum[idx - 1]
        center = spectrum[idx]
        right = spectrum[idx + 1]
        if center >= left and center >= right and (center > left or center > right):
            peaks.append(idx)

    if not peaks:
        peaks = [int(np.argmax(spectrum))]
    return np.asarray(peaks, dtype=int)


class SubspaceMethod(object):
    """
    An abstract class representing subspace-based method.

    Attributes:
        system_model: An instance of the SystemModel class representing the system model.

    Methods:
        __init__(self, system_model):
            Constructor for the SubspaceMethod class.

        calculate_covariance(self, X, mode="sample", model=None):
            Calculates the covariance matrix based on the specified mode.

        subspace_separation(self, covariance_mat, M):
            Performs subspace separation to obtain the noise and signal subspaces.
    """

    def __init__(self, system_model: SystemModel):
        """
        Constructor for the SubspaceMethod class.

        Args:
            system_model: An instance of the SystemModel class.

        Attributes:
            system_model: An instance of the SystemModel class.
        """
        self.system_model = system_model
        self.row_sensor_positions = self._get_row_sensor_positions()
        self.virtual_system_model = self._build_virtual_system_model(system_model)
        self.smoothed_virtual_system_model = self._build_smoothed_virtual_system_model()
        self.row_system_model = self._build_row_system_model(system_model)
        self.last_lrmc_diagnostics = None

    def _build_virtual_system_model(self, system_model: SystemModel):
        """Builds a virtual ULA model for LRMC-completed covariance processing."""
        virtual_size = getattr(system_model.params, "virtual_array_size", None)
        if not getattr(system_model.params, "use_lrmc", False):
            return None
        if virtual_size is None:
            return None
        params = copy.deepcopy(system_model.params)
        params.set_parameter("geometry_name", None)
        params.set_parameter("physical_sensor_positions_2d", None)
        params.set_parameter("row_groups", None)
        params.set_parameter("N", virtual_size)
        params.set_parameter("sensor_positions", list(range(virtual_size)))
        params.set_parameter("use_lrmc", False)
        params.set_parameter("virtual_array_size", virtual_size)
        return SystemModel(params)

    def _build_row_system_model(self, system_model: SystemModel):
        """Builds the reduced row-wise model used for row smoothing and baselines."""
        geometry_name = getattr(system_model.params, "geometry_name", None)
        physical_sensor_positions_2d = getattr(
            system_model.params, "physical_sensor_positions_2d", None
        )
        if (
            physical_sensor_positions_2d is None
            and not (isinstance(geometry_name, str) and geometry_name.startswith("mimo_2d_12ch"))
        ):
            return None
        row_positions = self.row_sensor_positions
        if row_positions is None:
            return None
        row_positions = list(row_positions)
        if len(row_positions) == 0:
            return None
        params = copy.deepcopy(system_model.params)
        params.set_parameter("geometry_name", None)
        params.set_parameter("physical_sensor_positions_2d", None)
        params.set_parameter("N", len(row_positions))
        params.set_parameter("sensor_positions", row_positions)
        params.set_parameter("use_lrmc", False)
        return SystemModel(params)

    def _build_smoothed_virtual_system_model(self):
        """Builds the reduced virtual ULA used after spatial smoothing."""
        if self.virtual_system_model is None:
            return None
        size = self.virtual_system_model.params.N
        sub_array_size = int(size / 2) + 1
        params = copy.deepcopy(self.virtual_system_model.params)
        params.set_parameter("geometry_name", None)
        params.set_parameter("physical_sensor_positions_2d", None)
        params.set_parameter("row_groups", None)
        params.set_parameter("N", sub_array_size)
        params.set_parameter("sensor_positions", list(range(sub_array_size)))
        params.set_parameter("virtual_array_size", sub_array_size)
        return SystemModel(params)

    def _get_row_groups(self):
        row_groups = getattr(self.system_model.params, "row_groups", None)
        if row_groups is None:
            geometry_name = getattr(self.system_model.params, "geometry_name", None)
            physical_sensor_positions_2d = getattr(
                self.system_model.params, "physical_sensor_positions_2d", None
            )
            if physical_sensor_positions_2d is not None or (
                isinstance(geometry_name, str) and geometry_name.startswith("mimo_2d_12ch")
            ):
                return DEFAULT_ROW_GROUPS_2D
            return None
        return tuple(tuple(int(index) for index in group) for group in row_groups)

    def _get_row_sensor_positions(self):
        """Derive the actual 1D sparse row geometry from the physical 2D coordinates."""
        row_positions = getattr(self.system_model.params, "sensor_positions", None)
        if row_positions is not None:
            row_positions = list(row_positions)

        physical_sensor_positions_2d = getattr(
            self.system_model.params, "physical_sensor_positions_2d", None
        )
        row_groups = self._get_row_groups()
        array_spacing = float(getattr(self.system_model.params, "array_spacing", 0.0) or 0.0)

        if physical_sensor_positions_2d is None or not row_groups or array_spacing <= 0:
            return row_positions

        canonical_group = getattr(self.system_model.params, "canonical_row_group", None)
        if canonical_group is None:
            canonical_group = len(row_groups) - 1
        canonical_group = int(max(0, min(canonical_group, len(row_groups) - 1)))

        x_positions = np.asarray(
            [physical_sensor_positions_2d[index][0] for index in row_groups[canonical_group]],
            dtype=float,
        )
        normalized_positions = (x_positions - np.min(x_positions)) / array_spacing
        rounded_positions = np.rint(normalized_positions)

        if (
            np.max(np.abs(normalized_positions - rounded_positions)) < 1e-6
            and np.all(np.diff(rounded_positions) >= 0)
        ):
            return rounded_positions.astype(int).tolist()
        return row_positions

    def apply_postprocessing(self, covariance_mat: np.ndarray):
        """Applies optional post-LRMC decorrelation on the completed covariance."""
        mode = str(getattr(self.system_model.params, "lrmc_postprocessing", "none")).lower()
        if mode in {"", "none"}:
            return covariance_mat

        def forward_backward_average(matrix: np.ndarray):
            size = matrix.shape[0]
            exchange = np.fliplr(np.eye(size))
            return 0.5 * (matrix + exchange @ np.conjugate(matrix) @ exchange)

        def spatial_smoothing_from_covariance(matrix: np.ndarray):
            size = matrix.shape[0]
            sub_array_size = int(size / 2) + 1
            number_of_sub_arrays = size - sub_array_size + 1
            smoothed = np.zeros((sub_array_size, sub_array_size), dtype=np.complex128)
            for start in range(number_of_sub_arrays):
                smoothed += matrix[start : start + sub_array_size, start : start + sub_array_size]
            return smoothed / number_of_sub_arrays

        output = np.asarray(covariance_mat, dtype=np.complex128)
        if mode in {"fba", "fba+ss", "ss+fba"}:
            output = forward_backward_average(output)
        if mode in {"spatial_smoothing", "ss", "fba+ss", "ss+fba"}:
            output = spatial_smoothing_from_covariance(output)
        return output

    def get_processing_model(self, mode: str):
        """Returns the appropriate array model for the selected covariance mode."""
        if mode.startswith("sample") and self.row_system_model is not None:
            return self.row_system_model
        if mode.startswith("spatial_smoothing") and self.row_system_model is not None:
            return self.row_system_model
        if mode == "lrmc_then_ss" and self.smoothed_virtual_system_model is not None:
            return self.smoothed_virtual_system_model
        if mode in {"ss_then_lrmc", "lrmc_only", "lrmc"} and self.virtual_system_model is not None:
            return self.virtual_system_model
        if mode.startswith("lrmc") and self.virtual_system_model is not None:
            post = str(getattr(self.system_model.params, "lrmc_postprocessing", "none")).lower()
            if post in {"spatial_smoothing", "ss", "fba+ss", "ss+fba"} and self.smoothed_virtual_system_model is not None:
                return self.smoothed_virtual_system_model
            return self.virtual_system_model
        return self.system_model

    def calculate_covariance(
        self, X: np.ndarray, mode: str = "sample", model: SubspaceNet = None
    ):
        """
        Calculates the covariance matrix based on the specified mode.

        Args:
        -----
            X (np.ndarray): Input samples matrix.
            mode (str): Covariance calculation mode. Options: "spatial_smoothing", "SubspaceNet", "sample".
            model: Optional model used for SubspaceNet covariance calculation.

        Returns:
        --------
            covariance_mat (np.ndarray): Covariance matrix.

        Raises:
        -------
            Exception: If the given model for covariance calculation is not from SubspaceNet type.
            Exception: If the covariance calculation mode is not defined.
        """

        self.last_lrmc_diagnostics = None

        ss_num_subarrays = getattr(self.system_model.params, "ss_num_subarrays", None)
        ss_row_subset = getattr(self.system_model.params, "ss_row_subset", None)

        def spatial_smoothing_covariance(X: np.ndarray):
            """
            Calculates the covariance matrix using spatial smoothing technique.

            Args:
            -----
                X (np.ndarray): Input samples matrix.

            Returns:
            --------
                covariance_mat (np.ndarray): Covariance matrix.
            """
            row_groups = self._get_row_groups()
            if row_groups:
                covariance = compute_sample_covariance(X)
                blocks = split_covariance_into_blocks(covariance, row_groups)
                selected_subset = resolve_row_subset(
                    row_groups=row_groups,
                    ss_num_subarrays=ss_num_subarrays,
                    ss_row_subset=ss_row_subset,
                )
                return average_covariance_blocks(
                    select_covariance_blocks(blocks, selected_subset)
                )
            # Define the sub-arrays size
            sub_array_size = int(self.system_model.params.N / 2) + 1
            # Define the number of sub-arrays
            number_of_sub_arrays = self.system_model.params.N - sub_array_size + 1
            # Initialize covariance matrix
            covariance_mat = np.zeros((sub_array_size, sub_array_size)) + 1j * np.zeros(
                (sub_array_size, sub_array_size)
            )
            for j in range(number_of_sub_arrays):
                # Run over all sub-arrays
                x_sub = X[j : j + sub_array_size, :]
                # Calculate sample covariance matrix for each sub-array
                sub_covariance = compute_sample_covariance(x_sub)
                # Aggregate sub-arrays covariances
                covariance_mat += sub_covariance
            # Divide overall matrix by the number of sources
            covariance_mat /= number_of_sub_arrays
            return covariance_mat

        def subspacnet_covariance(X: np.ndarray, subspacenet_model: SubspaceNet):
            """
            Calculates the covariance matrix using the SubspaceNet model.

            Args:
            -----
                X (np.ndarray): Input samples matrix.
                subspacenet_model (SubspaceNet): Model used for covariance calculation.

            Returns:
            --------
                covariance_mat (np.ndarray): Covariance matrix.

            Raises:
            -------
                Exception: If the given model for covariance calculation is not from SubspaceNet type.
            """
            # Validate model type
            if not isinstance(model, SubspaceNet):
                raise Exception(
                    (
                        "SubspaceMethod.subspacenet_covariance: given model for covariance\
                    calculation isn't from SubspaceNet type"
                    )
                )
            # Predict the covariance matrix using the SubspaceNet model
            subspacenet_model.eval()
            covariance_mat = subspacenet_model(X)[-1]
            # Convert to np.array type
            covariance_mat = np.array(covariance_mat.squeeze())
            return covariance_mat

        def lrmc_covariance(X: np.ndarray):
            """Calculates covariance via LRMC-completed virtual ULA covariance."""
            row_groups = self._get_row_groups()
            if row_groups and mode in {"lrmc_only", "lrmc", "lrmc_then_ss"}:
                covariance = compute_sample_covariance(X)
                variant = "canonical" if mode in {"lrmc_only", "lrmc"} else "average_completed"
                _, _, _, completed_covariance, diagnostics = complete_rowwise_nula_covariance(
                    covariance=covariance,
                    row_groups=row_groups,
                    sensor_positions=self.row_sensor_positions,
                    virtual_size=self.system_model.params.virtual_array_size,
                    rank=self.system_model.params.lrmc_rank,
                    solver=self.system_model.params.lrmc_solver,
                    init_strategy=getattr(self.system_model.params, "lrmc_init_strategy", "lag"),
                    max_iter=getattr(self.system_model.params, "lrmc_max_iter", 100),
                    tol=getattr(self.system_model.params, "lrmc_tol", 1e-6),
                    epsilon=getattr(self.system_model.params, "lrmc_epsilon", 1e-8),
                    enforce_toeplitz=getattr(
                        self.system_model.params, "lrmc_enforce_toeplitz", False
                    ),
                    nuclear_ridge=getattr(self.system_model.params, "lrmc_nuclear_ridge", 1e-8),
                    variant=variant,
                    ss_num_subarrays=ss_num_subarrays,
                    ss_row_subset=ss_row_subset,
                )
                self.last_lrmc_diagnostics = diagnostics
                return self.apply_postprocessing(completed_covariance)
            _, _, _, completed_covariance, diagnostics = complete_nula_covariance(
                X=np.asarray(X),
                sensor_positions=self.system_model.params.sensor_positions,
                virtual_size=self.system_model.params.virtual_array_size,
                rank=self.system_model.params.lrmc_rank,
                solver=self.system_model.params.lrmc_solver,
                init_strategy=getattr(self.system_model.params, "lrmc_init_strategy", "lag"),
                max_iter=getattr(self.system_model.params, "lrmc_max_iter", 100),
                tol=getattr(self.system_model.params, "lrmc_tol", 1e-6),
                epsilon=getattr(self.system_model.params, "lrmc_epsilon", 1e-8),
                enforce_toeplitz=getattr(
                    self.system_model.params, "lrmc_enforce_toeplitz", False
                ),
                nuclear_ridge=getattr(self.system_model.params, "lrmc_nuclear_ridge", 1e-8),
            )
            self.last_lrmc_diagnostics = diagnostics
            return self.apply_postprocessing(completed_covariance)

        def rowwise_lrmc_then_smoothing(X: np.ndarray):
            covariance = compute_sample_covariance(X)
            _, _, _, completed_covariance, diagnostics = complete_rowwise_nula_covariance(
                covariance=covariance,
                row_groups=self._get_row_groups(),
                sensor_positions=self.row_sensor_positions,
                virtual_size=self.system_model.params.virtual_array_size,
                rank=self.system_model.params.lrmc_rank,
                solver=self.system_model.params.lrmc_solver,
                init_strategy=getattr(self.system_model.params, "lrmc_init_strategy", "lag"),
                max_iter=getattr(self.system_model.params, "lrmc_max_iter", 100),
                tol=getattr(self.system_model.params, "lrmc_tol", 1e-6),
                epsilon=getattr(self.system_model.params, "lrmc_epsilon", 1e-8),
                enforce_toeplitz=getattr(
                    self.system_model.params, "lrmc_enforce_toeplitz", False
                ),
                nuclear_ridge=getattr(self.system_model.params, "lrmc_nuclear_ridge", 1e-8),
                variant="average_completed",
                ss_num_subarrays=ss_num_subarrays,
                ss_row_subset=ss_row_subset,
            )
            self.last_lrmc_diagnostics = diagnostics
            return self.apply_postprocessing(completed_covariance)

        def rowwise_smoothing_then_lrmc(X: np.ndarray):
            covariance = compute_sample_covariance(X)
            _, _, _, completed_covariance, diagnostics = complete_rowwise_nula_covariance(
                covariance=covariance,
                row_groups=self._get_row_groups(),
                sensor_positions=self.row_sensor_positions,
                virtual_size=self.system_model.params.virtual_array_size,
                rank=self.system_model.params.lrmc_rank,
                solver=self.system_model.params.lrmc_solver,
                init_strategy=getattr(self.system_model.params, "lrmc_init_strategy", "lag"),
                max_iter=getattr(self.system_model.params, "lrmc_max_iter", 100),
                tol=getattr(self.system_model.params, "lrmc_tol", 1e-6),
                epsilon=getattr(self.system_model.params, "lrmc_epsilon", 1e-8),
                enforce_toeplitz=getattr(
                    self.system_model.params, "lrmc_enforce_toeplitz", False
                ),
                nuclear_ridge=getattr(self.system_model.params, "lrmc_nuclear_ridge", 1e-8),
                variant="average_raw",
                ss_num_subarrays=ss_num_subarrays,
                ss_row_subset=ss_row_subset,
            )
            self.last_lrmc_diagnostics = diagnostics
            return self.apply_postprocessing(completed_covariance)

        if mode.startswith("spatial_smoothing"):
            return spatial_smoothing_covariance(X)
        elif mode.startswith("SubspaceNet"):
            return subspacnet_covariance(X, model)
        elif mode in {"lrmc_then_ss"}:
            return rowwise_lrmc_then_smoothing(X)
        elif mode in {"ss_then_lrmc"}:
            return rowwise_smoothing_then_lrmc(X)
        elif mode in {"lrmc_only", "lrmc"}:
            return lrmc_covariance(X)
        elif mode.startswith("lrmc"):
            return lrmc_covariance(X)
        elif mode.startswith("sample"):
            covariance = compute_sample_covariance(X)
            row_groups = self._get_row_groups()
            if row_groups:
                canonical_group = getattr(
                    self.system_model.params, "canonical_row_group", None
                )
                if canonical_group is None:
                    canonical_group = len(row_groups) - 1
                canonical_group = int(canonical_group)
                canonical_group = max(0, min(canonical_group, len(row_groups) - 1))
                return covariance[np.ix_(row_groups[canonical_group], row_groups[canonical_group])]
            return covariance
        else:
            raise Exception(
                (
                    f"SubspaceMethod.subspacnet_covariance: {mode} type for covariance\
                calculation is not defined"
                )
            )

    def subspace_separation(self, covariance_mat: np.ndarray, M: int):
        """
        Performs subspace separation to obtain the noise and signal subspaces.

        Args:
            covariance_mat (np.ndarray): Covariance matrix.
            M (int): Number of sources.

        Returns:
            noise_subspace (np.ndarray): Noise subspace.
            signal_subspace (np.ndarray): Signal subspace.
        """
        # Find eigenvalues and eigenvectors (EVD)
        eigenvalues, eigenvectors = np.linalg.eig(covariance_mat)
        # Sort eigenvectors based on eigenvalues order
        eigenvectors = eigenvectors[:, np.argsort(eigenvalues)[::-1]]
        # Assign signal subspace as the eigenvectors associated with M greatest eigenvalues
        signal_subspace = eigenvectors[:, 0:M]
        # Assign noise subspace as the eigenvectors associated with M lowest eigenvalues
        noise_subspace = eigenvectors[:, M:]
        return noise_subspace, signal_subspace


class MUSIC(SubspaceMethod):
    """
    A class representing the model-based MUSIC algorithm for DoA estimation.
    Inherits from the SubspaceMethod class.

    Attributes:
        system_model: An instance of the SystemModel class representing the system model.
        angels: An array of angles for direction of arrival (DOA) estimation.

    Methods:
    --------
        __init__(self, system_model): Constructor for the MUSIC class.

        broadband(self, X, known_num_of_sources=True):
            Implementation of the model-based non-coherent broadband MUSIC algorithm.

        narrowband(self, X, known_num_of_sources=True, mode: str="sample", model: SubspaceNet=None):
            Implementation of the model-based narrowband MUSIC algorithm.

        spectrum_calculation(self, Un, f =1, array_form="ULA"):
            Calculates the MUSIC spectrum and the core equation for DOA estimation.

        get_spectrum_peaks(self, spectrum: np.ndarray):
            Calculates the peaks of the MUSIC spectrum.

    """

    def __init__(self, system_model: SystemModel):
        """
        Constructor for the MUSIC class.

        Args:
            system_model: An instance of the SystemModel class.
        """
        super().__init__(system_model)
        # Angle axis for representation of the MUSIC spectrum.
        # Keep the scan window aligned with the dataset/template FOV so smaller
        # experiments do not waste time scanning the full +/-90 degree range.
        doa_min_deg = float(getattr(system_model.params, "doa_min", -90.0))
        doa_max_deg = float(getattr(system_model.params, "doa_max", 90.0))
        doa_resolution_deg = float(getattr(system_model.params, "doa_resolution", 0.01))
        if doa_max_deg <= doa_min_deg:
            doa_min_deg, doa_max_deg = -90.0, 90.0
        if doa_resolution_deg <= 0:
            doa_resolution_deg = 0.01
        num_samples = max(1, int(np.ceil((doa_max_deg - doa_min_deg) / doa_resolution_deg)))
        self._angels_deg = np.linspace(
            doa_min_deg, doa_max_deg, num_samples, endpoint=False, dtype=float
        )
        self._angels = self._angels_deg * np.pi / 180.0

    def spectrum_calculation(
        self,
        Un: np.ndarray,
        f: float = 1,
        array_form: str = "ULA",
        system_model: SystemModel = None,
    ):
        """
        Calculates the MUSIC spectrum and the core equation for DOA estimation,
        and calculate the peaks of the spectrum.

        Args:
        -----
            Un (np.ndarray): Noise subspace matrix.
            f (float, optional): Frequency. Defaults to 1.
            array_form (str, optional): Array form. Defaults to "ULA".

        Returns:
        --------
            spectrum (np.ndarray): MUSIC spectrum.
            core_equation (np.ndarray): Core equation.
        """
        core_equation = []
        system_model = system_model or self.system_model
        # Run over all angels in grid
        for angle in self._angels:
            # Calculate the steered vector to angle
            a = system_model.steering_vec(theta=angle, f=f, array_form=array_form, nominal = True)[
                : Un.shape[0]
            ]
            # Calculate the core equation element
            core_equation.append(np.conj(a).T @ Un @ np.conj(Un).T @ a)
        # Convert core equation to complex np.ndarray form
        core_equation = np.array(core_equation, dtype=complex)
        # MUSIC spectrum as the inverse core equation
        spectrum = 1 / core_equation
        return spectrum, core_equation

    def get_spectrum_peaks(self, spectrum: np.ndarray):
        """
        Calculates the peaks of the MUSIC spectrum.

        Args:
        -----
            spectrum (np.ndarray): MUSIC spectrum.

        Returns:
        --------
            peaks (list): the spectrum ordered peaks.
        """
        # Find spectrum peaks
        if scipy_signal is not None:
            peaks = list(scipy_signal.find_peaks(spectrum)[0])
        else:
            peaks = list(_find_peaks_fallback(spectrum))
        # Sort the peak by their amplitude
        peaks.sort(key=lambda x: spectrum[x], reverse=True)
        return peaks

    def broadband(self, X: np.ndarray, known_num_of_sources: bool = True):
        """
        Implementation of the model-based non-coherent broadband MUSIC algorithm.

        Args:
        -----
            X (np.ndarray): Input samples vector.
            known_num_of_sources (bool, optional): Flag indicating if the number of sources is known. Defaults to True.
        Returns:
        --------
            doa_predictions (list): Predicted DOAs.
            spectrum (np.ndarray): MUSIC spectrum.
            M (int): Number of sources.
        """
        # Number of frequency bins calculation
        number_of_bins = int(self.system_model.max_freq["Broadband"] / 10)
        # Whether the number of sources is given
        if known_num_of_sources:
            M = self.system_model.params.M
        else:
            # clustering technique
            pass
        # Convert samples to frequency domain
        X = np.fft.fft(X, axis=1, n=self.system_model.f_sampling["Broadband"])
        # Calculate general params for calculations
        num_of_samples = len(self._angels)
        # Initialize spectrum array
        spectrum = np.zeros((number_of_bins, num_of_samples))
        # Calculate narrow-band spectrum for every frequency bin
        for i in range(number_of_bins):
            # Find the index of relevant bin
            ind = (
                int(self.system_model.min_freq["Broadband"])
                + i * len(self.system_model.f_rng["Broadband"]) // number_of_bins
            )
            # Calculate sample covariance matrix for measurements in the bin range
            covariance_mat = self.calculate_covariance(
                X=X[
                    :,
                    ind : ind
                    + len(self.system_model.f_rng["Broadband"]) // number_of_bins,
                ],
                mode="sample",
            )
            # Get noise subspace
            Un, _ = self.subspace_separation(covariance_mat=covariance_mat, M=M)
            # Calculate narrow-band music spectrum
            spectrum[i], _ = self.spectrum_calculation(
                Un,
                f=ind + len(self.system_model.f_rng["Broadband"]) // number_of_bins - 1,
            )
        # Sum all bins spectrums contributions to unified music spectrum
        spectrum = np.sum(spectrum, axis=0)
        # Find spectrum peaks
        doa_predictions = self.get_spectrum_peaks(spectrum)
        # Associate predictions to angels
        predictions = self._angels[doa_predictions] * R2D
        # Take first M predictions
        predictions = predictions[:M][::-1]
        return predictions, spectrum, M

    def narrowband(
        self,
        X: np.ndarray,
        known_num_of_sources: bool = True,
        mode: str = "sample",
        model: SubspaceNet = None,
    ):
        """
        Implementation of the model-based narrow-band MUSIC algorithm.

        Args:
        -----
            X (np.ndarray): Input samples matrix.
            known_num_of_sources (bool, optional): Flag indicating if the number of sources is known. Defaults to True.
            mode (str, optional): Covariance calculation mode. Defaults to 'sample'.
            model: Optional model used for SubspaceNet covariance calculation.

        Returns:
        --------
            doa_predictions (list): Predicted DOAs.
            spectrum (np.ndarray): MUSIC spectrum.
            M (int): Number of sources.
        """
        # Whether the number of sources is given
        if known_num_of_sources:
            M = self.system_model.params.M
        else:
            # clustering technique
            pass
        # Calculate covariance matrix
        covariance_mat = self.calculate_covariance(X=X, mode=mode, model=model)
        processing_model = self.get_processing_model(mode)
        # Get noise subspace
        Un, _ = self.subspace_separation(covariance_mat=covariance_mat, M=M)
        # TODO: Check if this condition is hold after the change
        # Assign the frequency for steering vector calculation (multiplied in self.dist to get dist = 1/2)
        f = processing_model.max_freq[processing_model.params.signal_type]
        # Generate the MUSIC spectrum
        spectrum, _ = self.spectrum_calculation(Un, f=f, system_model=processing_model)
        # Find spectrum peaks
        doa_predictions = self.get_spectrum_peaks(spectrum)
        # Associate predictions to angels
        predictions = self._angels[doa_predictions] * R2D
        # Take first M predictions
        predictions = predictions[:M][::-1]
        return predictions, spectrum, M


class RootMUSIC(SubspaceMethod):
    """
    A class representing the model-based Root MUSIC algorithm for DoA estimation.
    Inherits from the SubspaceMethod class.

    Attributes:
    -----------
        system_model: An instance of the SystemModel class representing the system model.

    Methods:
    --------
        narrowband(X: np.ndarray, known_num_of_sources: bool = True, mode: str = "sample"):
            Implementation of the model-based narrow-band RootMUSIC algorithm.

        extract_predictions_from_roots(self, roots: np.ndarray):
            Extracts the DoA predictions  from the roots of the polynomial.
    """

    def __init__(self, system_model: SystemModel):
        """
        Constructor for the RootMUSIC class.

        Args:
            system_model: An instance of the SystemModel class.
        """
        super().__init__(system_model)

    def narrowband(
        self,
        X: np.ndarray,
        known_num_of_sources: bool = True,
        mode: str = "sample",
        model: SubspaceNet = None,
    ):
        """
        Implementation of the model-based narrow-band RootMUSIC algorithm.

        Args:
        -----
            X (np.ndarray): Input samples vector.
            known_num_of_sources (bool, optional): Flag indicating if the number of sources is known. Defaults to True.
            mode (str, optional): Covariance calculation mode. Defaults to "sample".
            model: Optional model used for SubspaceNet covariance calculation.

        Returns:
        --------
            doa_predictions (np.ndarray): Predicted DOAs.
            roots (np.ndarray): Roots of the polynomial defined by F matrix diagonals.
            doa_predictions_all (np.ndarray): All predicted angles.
            roots_angels_all (np.ndarray): Phase components of all the roots.
            M (int): Number of sources.

        """
        # Whether the number of sources is given
        if known_num_of_sources:
            M = self.system_model.params.M
        else:
            # clustering technique
            pass
        # Calculate covariance matrix
        covariance_mat = self.calculate_covariance(X=X, mode=mode, model=model)
        # Get noise subspace
        Un, _ = self.subspace_separation(covariance_mat=covariance_mat, M=M)
        # Generate hermitian noise subspace matrix
        F = Un @ np.conj(Un).T
        # Calculates the sum of F matrix diagonals
        coefficients = sum_of_diag(F)
        # Calculates the roots of the polynomial defined by F matrix diagonals
        roots = list(find_roots(coefficients))
        # Sort roots by their distance from the unit circle
        roots.sort(key=lambda x: abs(abs(x) - 1))
        # Calculate all predicted angels for spectrum presentation
        doa_predictions_all, roots_angels_all = self.extract_predictions_from_roots(
            roots
        )
        # Take only roots which inside the unit circle
        roots_inside = [root for root in roots if ((abs(root) - 1) < 0)][:M]
        # Calculate DoA out of the roots inside the unit circle
        doa_predictions, _ = self.extract_predictions_from_roots(roots_inside)
        return doa_predictions, roots, doa_predictions_all, roots_angels_all, M

    def extract_predictions_from_roots(self, roots: np.ndarray):
        """
        Extracts the DoA predictions  from the roots of the polynomial.

        Args:
        -----
            roots (np.ndarray): Roots of the polynomial.

        Returns:
        --------
            doa_predictions (np.ndarray): Extracted DOAs.
            roots_angels (np.ndarray): Phase components of the roots.

        """
        array_spacing = float(getattr(self.system_model.params, "array_spacing", 0.5))
        if array_spacing <= 0:
            array_spacing = 0.5
        # Calculate the phase component of the roots
        roots_angels = np.angle(roots)
        # Calculate the DoA out of the phase component using the actual spacing.
        normalized_phase = roots_angels / (2 * np.pi * array_spacing)
        normalized_phase = np.clip(normalized_phase, -1.0, 1.0)
        doa_predictions = np.arcsin(normalized_phase) * R2D
        return doa_predictions, roots_angels


class Esprit(RootMUSIC):
    """
    A class representing the model-based Esprit algorithm for DoA estimation.
    Inherits from the RootMUSIC class.

    Attributes:
    -----------
        system_model: An instance of the SystemModel class representing the system model.

    Methods:
    --------
        narrowband(X: np.ndarray, known_num_of_sources: bool = True, mode: str = "sample"):
            Implementation of the model-based narrow-band RootMUSIC algorithm.

        extract_predictions_from_roots(self, roots: np.ndarray):
            Extracts the DoA predictions  from the roots of the polynomial.
    """

    def __init__(self, system_model: SystemModel):
        """
        Constructor for the RootMUSIC class.

        Args:
            system_model: An instance of the SystemModel class.
        """
        super().__init__(system_model)

    def narrowband(
        self,
        X: np.ndarray,
        known_num_of_sources: bool = True,
        mode: str = "sample",
        model: SubspaceNet = None,
    ):
        """
        Implementation of the model-based narrow-band Esprit algorithm.

        Args:
        -----
            X (np.ndarray): Input samples matrix.
            known_num_of_sources (bool, optional): Flag indicating if the number of sources is known. Defaults to True.
            mode (str, optional): Covariance calculation mode. Defaults to 'sample'.
            model: Optional model used for SubspaceNet covariance calculation.

        Returns:
        --------
            doa_predictions (list): Predicted DOAs.
            M (int): Number of sources.
        """
        # Whether the number of sources is given
        if known_num_of_sources:
            M = self.system_model.params.M
        else:
            # clustering technique
            pass
        # Calculate covariance matrix
        covariance_mat = self.calculate_covariance(X=X, mode=mode, model=model)
        # Get noise subspace
        _, Us = self.subspace_separation(covariance_mat=covariance_mat, M=M)
        # Separate the signal subspace into 2 overlapping subspaces
        Us_upper, Us_lower = (
            Us[0 : covariance_mat.shape[0] - 1],
            Us[1 : covariance_mat.shape[0]],
        )
        # Generate Phi matrix
        phi = np.linalg.pinv(Us_upper) @ Us_lower
        # Find eigenvalues and eigenvectors (EVD) of Phi
        phi_eigenvalues, _ = np.linalg.eig(phi)
        # Calculate DoA out of the eigenvalues of Phi
        doa_predictions = -1 * self.extract_predictions_from_roots(phi_eigenvalues)[0]
        return doa_predictions, M


class MVDR(MUSIC):
    """
    A class representing the model-based MVDR algorithm for DoA estimation.
    Inherits from the MUSIC class.

    Attributes:
        system_model: An instance of the SystemModel class representing the system model.

    Methods:
    narrowband(self, X:np.ndarray, mode: str="sample", model: SubspaceNet=None, eps:float = 1):
        Implementation of the narrow-band Minimum Variance beamformer algorithm.

    """

    def __init__(self, system_model: SystemModel):
        """
        Constructor for the MVDR class.

        Args:
            system_model: An instance of the SystemModel class.
        """
        super().__init__(system_model)

    def narrowband(
        self,
        X: np.ndarray,
        mode: str = "sample",
        model: SubspaceNet = None,
        eps: float = 1,
    ):
        """
        Implementation of the narrow-band Minimum Variance beamformer algorithm.

        Args:
        -----
            X (np.ndarray): Input samples vector.
            mode (str, optional): Covariance calculation mode. Defaults to "sample".
            model (SubspaceNet, optional): SubspaceNet model. Defaults to None.
            eps (float, optional): Diagonal loading factor. Defaults to 1.

        Returns:
        --------
            response_curve (np.ndarray): The response curve of the MVDR beamformer.

        """
        response_curve = []
        # Calculate covariance matrix
        covariance_mat = self.calculate_covariance(X=X, mode=mode, model=model)
        processing_model = self.get_processing_model(mode)
        # Diagonal Loading
        diagonal_loaded_covariance = covariance_mat + eps * np.trace(
            covariance_mat
        ) * np.identity(covariance_mat.shape[0])
        # BeamForming response calculation
        inv_covariance = np.linalg.inv(diagonal_loaded_covariance)
        # TODO: Check if this condition is hold after the change
        # Assign the frequency for steering vector calculation (multiplied in self.dist to get dist = 1/2)
        f = processing_model.max_freq[processing_model.params.signal_type]
        for angle in self._angels:
            # Calculate the steering vector
            a = processing_model.steering_vec(
                theta=angle, f=f, array_form="ULA",
                nominal=True).reshape((processing_model.params.N, 1))
            # Adaptive calculation of optimal_weights
            optimal_weights = (inv_covariance @ a) / (np.conj(a).T @ inv_covariance @ a)
            # Calculate beamformer gain at specific angle
            response_curve.append(
                (
                    (
                        np.conj(optimal_weights).T
                        @ diagonal_loaded_covariance
                        @ optimal_weights
                    ).reshape((1))
                ).item()
            )
        response_curve = np.array(response_curve, dtype=complex)
        predictions = None
        return predictions, response_curve


class DBF(MUSIC):
    """
    Conventional digital beamforming (Bartlett beamformer) for DOA estimation.
    Inherits the angular grid and peak-picking logic from MUSIC.
    """

    def __init__(self, system_model: SystemModel):
        super().__init__(system_model)

    def narrowband(self, X: np.ndarray, mode: str = "sample", model: SubspaceNet = None):
        """
        Implementation of conventional narrowband digital beamforming.

        Args:
        -----
            X (np.ndarray): Input samples matrix.
            mode (str): Covariance calculation mode.
            model: Optional SubspaceNet model when mode is "SubspaceNet".

        Returns:
        --------
            predictions (np.ndarray): Predicted DOAs in degrees.
            spectrum (np.ndarray): Bartlett response curve.
            M (int): Number of sources.
        """
        M = self.system_model.params.M
        covariance_mat = self.calculate_covariance(X=X, mode=mode, model=model)
        processing_model = self.get_processing_model(mode)
        spectrum = []
        f = processing_model.max_freq[processing_model.params.signal_type]
        for angle in self._angels:
            steering = processing_model.steering_vec(
                theta=angle, f=f, array_form="ULA", nominal=True
            ).reshape((processing_model.params.N, 1))
            response = np.real(np.conj(steering).T @ covariance_mat @ steering).item()
            spectrum.append(response)
        spectrum = np.asarray(spectrum, dtype=float)
        doa_predictions = self.get_spectrum_peaks(spectrum)
        predictions = self._angels[doa_predictions] * R2D
        predictions = predictions[:M][::-1]
        return predictions, spectrum, M
