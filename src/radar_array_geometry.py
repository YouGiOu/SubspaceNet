"""2D radar array geometry helpers derived from radar_array_geometry.cpp."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np


GEOMETRY_NAME_2D_12CH = "mimo_2d_12ch"
DEFAULT_ARRAY_SPACING_LAMBDA = 1.9


@dataclass(frozen=True)
class RadarArrayGeometry2D:
    """Container for the fixed 2D geometry used in the order study."""

    name: str
    sensor_positions_2d: np.ndarray
    row_groups: Tuple[Tuple[int, ...], ...]
    canonical_row_group: int
    array_spacing: float


def get_mimo_2d_12ch_geometry(
    array_spacing: float = DEFAULT_ARRAY_SPACING_LAMBDA,
) -> RadarArrayGeometry2D:
    """
    Returns the fixed 12-channel 2D geometry used by the new study.

    The coordinates are derived from the existing C++ geometry file and are
    expressed in wavelength units so the steering phase can use them directly.
    """
    base_spacing = float(array_spacing)
    rx_coords = np.array(
        [
            [-8.0, 0.0],
            [-4.0, 0.0],
            [-1.0, 0.0],
            [0.0, 0.0],
        ],
        dtype=float,
    )
    tx_coords = np.array(
        [
            [0.0, 2.0],
            [4.0, 1.0],
            [8.0, 0.0],
        ],
        dtype=float,
    )

    sensor_positions = []
    row_groups = []
    for tx_index, tx in enumerate(tx_coords):
        row = []
        for rx_index, rx in enumerate(rx_coords):
            # The C++ file stores the virtual antenna as tx + rx with a flipped y-axis.
            x = (tx[0] + rx[0]) * base_spacing
            y = -(tx[1] + rx[1]) * base_spacing
            sensor_positions.append([x, y])
            row.append(tx_index * len(rx_coords) + rx_index)
        row_groups.append(tuple(row))

    return RadarArrayGeometry2D(
        name=GEOMETRY_NAME_2D_12CH,
        sensor_positions_2d=np.asarray(sensor_positions, dtype=float),
        row_groups=tuple(row_groups),
        canonical_row_group=len(row_groups) - 1,
        array_spacing=base_spacing,
    )
