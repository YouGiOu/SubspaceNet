"""Convenience launcher for plot_angular_spectra.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


# Edit this block to change the generated spectrum figure.
CONFIG = {
    "array_group": "B",
    "spacing": "1.9",
    "signal_nature": "coherent",
    # If None, derive automatically from target_azimuths.
    "num_targets": None,
    "target_azimuths": [-2.0, 1.0],
    "target_elevations": [0.0, 0.0],
    "snapshots": 40,
    "snr": 10.0,
    "pipelines": [
        "original",
        # "ss",
        # "lrmc",
        # "ss_then_lrmc",
        # "lrmc_then_ss",
    ],
    # "curve_methods": ["music", "dbf", "mvdr"],
    "curve_methods": ["music"],
    # "estimate_overlays": ["root-music", "esprit"],
    "scan_min": -15.0,
    "scan_max": 15.0,
    "scan_resolution": 0.05,
    "output_dir": "results/angular_spectra",
    "output_format": "png",
    "figure_title": None,
    "peak_markers": True,
    "export_csv": True,
}


def join_values(values) -> str:
    return ",".join(str(value) for value in values)


def resolve_num_targets() -> int:
    azimuths = CONFIG.get("target_azimuths", [])
    elevations = CONFIG.get("target_elevations")

    if not azimuths:
        raise ValueError("CONFIG['target_azimuths'] must contain at least one value.")
    if elevations is not None and len(elevations) != len(azimuths):
        raise ValueError(
            "CONFIG['target_elevations'] must match CONFIG['target_azimuths'] in length."
        )

    configured = CONFIG.get("num_targets")
    derived = len(azimuths)
    if configured is None:
        return derived
    configured = int(configured)
    if configured != derived:
        raise ValueError(
            f"CONFIG['num_targets']={configured} does not match "
            f"len(CONFIG['target_azimuths'])={derived}. "
            "Set num_targets to None or make them match."
        )
    return configured


def build_command(repo_root: Path) -> list[str]:
    num_targets = resolve_num_targets()
    command = [
        sys.executable,
        str(repo_root / "plot_angular_spectra.py"),
        "--array-group",
        str(CONFIG["array_group"]),
        "--spacing",
        str(CONFIG["spacing"]),
        "--signal-nature",
        str(CONFIG["signal_nature"]),
        "--num-targets",
        str(num_targets),
        f"--target-azimuths={join_values(CONFIG['target_azimuths'])}",
        "--snapshots",
        str(CONFIG["snapshots"]),
        "--snr",
        str(CONFIG["snr"]),
        "--pipelines",
        join_values(CONFIG["pipelines"]),
        "--curve-methods",
        join_values(CONFIG["curve_methods"]),
        "--output-dir",
        str(CONFIG["output_dir"]),
        "--output-format",
        str(CONFIG["output_format"]),
    ]

    target_elevations = CONFIG.get("target_elevations")
    if target_elevations is not None:
        command.append(f"--target-elevations={join_values(target_elevations)}")

    estimate_overlays = CONFIG.get("estimate_overlays")
    if estimate_overlays:
        command.extend(["--estimate-overlays", join_values(estimate_overlays)])

    if CONFIG.get("scan_min") is not None:
        command.extend(["--scan-min", str(CONFIG["scan_min"])])
    if CONFIG.get("scan_max") is not None:
        command.extend(["--scan-max", str(CONFIG["scan_max"])])
    if CONFIG.get("scan_resolution") is not None:
        command.extend(["--scan-resolution", str(CONFIG["scan_resolution"])])
    if CONFIG.get("figure_title"):
        command.extend(["--figure-title", str(CONFIG["figure_title"])])
    if CONFIG.get("peak_markers"):
        command.append("--peak-markers")
    if CONFIG.get("export_csv"):
        command.append("--export-csv")

    return command


def main():
    repo_root = Path(__file__).resolve().parent
    command = build_command(repo_root)
    print("Launching configurable angular-spectrum plot generation")
    print("Command:", " ".join(command))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
