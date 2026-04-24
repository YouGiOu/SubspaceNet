"""Generate configurable angular-spectrum plots for the 2D array studies."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from src.dataset_template import build_system_model_params_from_template
from src.methods import DBF, Esprit, MUSIC, MVDR, RootMUSIC
from src.signal_creation import Samples
from src.utils import R2D


GEOMETRY_TEMPLATE_ROOT = Path("data/dataset_templates/ablation/phase2_2d_geometry_shape_ablation")

PIPELINE_ALIASES = {
    "original": "sample",
    "baseline": "sample",
    "sample": "sample",
    "ss": "spatial_smoothing",
    "spatial_smoothing": "spatial_smoothing",
    "ss_only": "spatial_smoothing",
    "lrmc": "lrmc_only",
    "lrmc_only": "lrmc_only",
    "ss_then_lrmc": "ss_then_lrmc",
    "ss_lrmc": "ss_then_lrmc",
    "lrmc_then_ss": "lrmc_then_ss",
    "lrmc_ss": "lrmc_then_ss",
}

PIPELINE_CONFIGS = {
    "sample": {"suffix": "baseline", "mode": "sample", "label": "Original"},
    "spatial_smoothing": {
        "suffix": "ss_only",
        "mode": "spatial_smoothing",
        "label": "SS",
    },
    "lrmc_only": {"suffix": "lrmc_only", "mode": "lrmc_only", "label": "LRMC"},
    "ss_then_lrmc": {
        "suffix": "ss_lrmc",
        "mode": "ss_then_lrmc",
        "label": "SS->LRMC",
    },
    "lrmc_then_ss": {
        "suffix": "lrmc_ss",
        "mode": "lrmc_then_ss",
        "label": "LRMC->SS",
    },
}

CURVE_METHODS = {
    "dbf": DBF,
    "music": MUSIC,
    "mvdr": MVDR,
}

ESTIMATE_METHODS = {
    "root-music": RootMUSIC,
    "esprit": Esprit,
}

METHOD_LABELS = {
    "dbf": "DBF",
    "music": "MUSIC",
    "mvdr": "MVDR",
    "root-music": "Root-MUSIC",
    "esprit": "ESPRIT",
}

PIPELINE_FILENAME_LABELS = {
    "sample": "orig",
    "spatial_smoothing": "ss",
    "lrmc_only": "lrmc",
    "ss_then_lrmc": "ss_lrmc",
    "lrmc_then_ss": "lrmc_ss",
}

GROUP_LABELS = {"a": "A", "b": "B", "c": "C"}


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Generate angular-spectrum figures for configurable 2D array geometries, "
            "preprocessing pipelines, and signal conditions."
        )
    )
    parser.add_argument(
        "--array-group",
        required=True,
        choices=["A", "B", "C", "a", "b", "c"],
        help="Physical array group to use.",
    )
    parser.add_argument(
        "--spacing",
        required=True,
        help="Physical spacing in lambda units. Supported values: 0.5 or 1.9.",
    )
    parser.add_argument(
        "--signal-nature",
        default="coherent",
        choices=["coherent", "non-coherent", "noncoherent"],
        help="Signal model for snapshot generation.",
    )
    parser.add_argument(
        "--num-targets",
        type=int,
        required=True,
        help="Number of targets in the generated scene.",
    )
    parser.add_argument(
        "--target-azimuths",
        required=True,
        help="Comma-separated target azimuths in degrees.",
    )
    parser.add_argument(
        "--target-elevations",
        default=None,
        help="Optional comma-separated target elevations in degrees. Defaults to all zeros.",
    )
    parser.add_argument(
        "--snapshots",
        type=int,
        required=True,
        help="Number of snapshots T.",
    )
    parser.add_argument(
        "--snr",
        type=float,
        required=True,
        help="SNR in dB.",
    )
    parser.add_argument(
        "--pipelines",
        default="sample",
        help=(
            "Comma-separated preprocessing pipelines. Supported: "
            "original/sample, ss/spatial_smoothing, lrmc/lrmc_only, "
            "ss_then_lrmc/ss_lrmc, lrmc_then_ss/lrmc_ss."
        ),
    )
    parser.add_argument(
        "--curve-methods",
        default="music",
        help="Comma-separated spectrum-producing methods. Supported: dbf,music,mvdr.",
    )
    parser.add_argument(
        "--estimate-overlays",
        default="",
        help="Optional comma-separated estimate-only overlays. Supported: root-music,esprit.",
    )
    parser.add_argument(
        "--scan-min",
        type=float,
        default=None,
        help="Optional lower azimuth scan limit in degrees. Auto-derived if omitted.",
    )
    parser.add_argument(
        "--scan-max",
        type=float,
        default=None,
        help="Optional upper azimuth scan limit in degrees. Auto-derived if omitted.",
    )
    parser.add_argument(
        "--scan-resolution",
        type=float,
        default=None,
        help="Optional azimuth scan resolution in degrees.",
    )
    parser.add_argument(
        "--output-dir",
        default="results/angular_spectra",
        help="Directory for generated spectrum figures.",
    )
    parser.add_argument(
        "--output-format",
        default="png",
        choices=["png", "pdf"],
        help="Image format for the generated figure.",
    )
    parser.add_argument(
        "--figure-title",
        default=None,
        help="Optional custom title. Defaults to a config-derived title.",
    )
    parser.add_argument(
        "--peak-markers",
        action="store_true",
        help="Draw predicted-peak markers for curve-producing methods when available.",
    )
    parser.add_argument(
        "--export-csv",
        action="store_true",
        help="Export angular-spectrum curve samples to CSV files.",
    )
    return parser.parse_args()


def parse_float_list(raw: str | None, *, default_value: float | None = None, count: int | None = None):
    if raw is None:
        if count is None or default_value is None:
            return None
        return [float(default_value) for _ in range(count)]
    values = [float(item.strip()) for item in raw.split(",") if item.strip()]
    return values


def normalize_signal_nature(value: str) -> str:
    value = value.strip().lower()
    if value == "noncoherent":
        return "non-coherent"
    return value


def normalize_spacing(value: str) -> tuple[str, float]:
    normalized = value.strip().lower().replace("λ", "").replace("lambda", "")
    if normalized in {"0.5", "0p5"}:
        return "0p5", 0.5
    if normalized in {"1.9", "1p9"}:
        return "1p9", 1.9
    raise ValueError(f"Unsupported spacing: {value}. Supported values are 0.5 and 1.9.")


def normalize_pipeline_list(raw: str):
    pipelines = []
    for item in raw.split(","):
        key = item.strip().lower()
        if not key:
            continue
        canonical = PIPELINE_ALIASES.get(key)
        if canonical is None:
            raise ValueError(f"Unsupported pipeline: {item}")
        if canonical not in pipelines:
            pipelines.append(canonical)
    if not pipelines:
        raise ValueError("At least one pipeline must be provided.")
    return pipelines


def normalize_method_list(raw: str, supported: dict[str, object], label: str):
    methods = []
    for item in raw.split(","):
        key = item.strip().lower()
        if not key:
            continue
        if key not in supported:
            raise ValueError(f"Unsupported {label}: {item}")
        if key not in methods:
            methods.append(key)
    return methods


def load_template(repo_root: Path, group: str, spacing_label: str, pipeline_key: str):
    suffix = PIPELINE_CONFIGS[pipeline_key]["suffix"]
    path = (
        repo_root
        / GEOMETRY_TEMPLATE_ROOT
        / f"phase2g_group{group}_{spacing_label}_{suffix}.json"
    )
    if not path.exists():
        raise FileNotFoundError(f"Missing template for geometry/pipeline selection: {path}")
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def build_scene_params(template: dict, args, azimuths_deg: list[float], elevations_deg: list[float]):
    params = build_system_model_params_from_template(template)
    params.set_parameter("M", int(args.num_targets))
    params.set_parameter("T", int(args.snapshots))
    params.set_parameter("snr", float(args.snr))
    params.set_parameter("signal_nature", normalize_signal_nature(args.signal_nature))
    scan_min = args.scan_min
    scan_max = args.scan_max
    if scan_min is None or scan_max is None:
        margin = max(5.0, 0.5 * max(1.0, max(azimuths_deg) - min(azimuths_deg)))
        auto_min = max(-90.0, min(azimuths_deg) - margin)
        auto_max = min(90.0, max(azimuths_deg) + margin)
        if scan_min is None:
            scan_min = auto_min
        if scan_max is None:
            scan_max = auto_max
    if scan_max <= scan_min:
        raise ValueError("scan-max must be greater than scan-min")
    params.set_parameter("doa_min", float(scan_min))
    params.set_parameter("doa_max", float(scan_max))
    params.set_parameter(
        "elevation_min",
        float(min(elevations_deg) - 1.0 if elevations_deg else -15.0),
    )
    params.set_parameter(
        "elevation_max",
        float(max(elevations_deg) + 1.0 if elevations_deg else 15.0),
    )
    params.set_parameter("min_doa_gap", 0.0)
    params.set_parameter("fixed_doa_gap", None)
    if args.scan_resolution is not None:
        params.set_parameter("doa_resolution", float(args.scan_resolution))
    return params


def generate_scene_observations(params, azimuths_deg: list[float], elevations_deg: list[float]):
    samples_model = Samples(params)
    samples_model.set_doa_2d(list(zip(azimuths_deg, elevations_deg)))
    observations, _, _, _ = samples_model.samples_creation(
        noise_mean=0,
        noise_variance=1,
        signal_mean=0,
        signal_variance=1,
    )
    return samples_model, np.asarray(observations, dtype=np.complex128)


def compute_curve(method_name: str, pipeline_key: str, params, observations: np.ndarray):
    system_model = Samples(params)
    method_class = CURVE_METHODS[method_name]
    method = method_class(system_model)
    mode = PIPELINE_CONFIGS[pipeline_key]["mode"]
    if method_name == "mvdr":
        predictions, spectrum = method.narrowband(observations, mode=mode)
        if predictions is None:
            predictions = np.asarray([], dtype=float)
    else:
        predictions, spectrum, _ = method.narrowband(observations, mode=mode)
    ang_grid_deg = np.asarray(method._angels_deg, dtype=float)
    spectrum = np.abs(np.asarray(spectrum, dtype=np.complex128).reshape(-1))
    return {
        "method_name": method_name,
        "pipeline_key": pipeline_key,
        "label": f"{METHOD_LABELS[method_name]} | {PIPELINE_CONFIGS[pipeline_key]['label']}",
        "ang_grid_deg": ang_grid_deg,
        "spectrum": spectrum,
        "predictions": np.asarray(predictions, dtype=float).reshape(-1),
    }


def compute_estimate_overlay(method_name: str, pipeline_key: str, params, observations: np.ndarray):
    system_model = Samples(params)
    method_class = ESTIMATE_METHODS[method_name]
    method = method_class(system_model)
    mode = PIPELINE_CONFIGS[pipeline_key]["mode"]
    if method_name == "root-music":
        predictions, _, _, _, _ = method.narrowband(observations, mode=mode)
    else:
        predictions, _ = method.narrowband(observations, mode=mode)
    return {
        "method_name": method_name,
        "pipeline_key": pipeline_key,
        "label": f"{METHOD_LABELS[method_name]} | {PIPELINE_CONFIGS[pipeline_key]['label']}",
        "predictions": np.asarray(predictions, dtype=float).reshape(-1),
    }


def build_output_stem(
    group: str,
    spacing_label: str,
    signal_nature: str,
    num_targets: int,
    azimuths_deg: list[float],
    elevations_deg: list[float],
    snapshots: int,
    snr: float,
    curve_methods: list[str],
    pipelines: list[str],
):
    az_label = "_".join(f"{value:g}" for value in azimuths_deg)
    el_label = "_".join(f"{value:g}" for value in elevations_deg)
    combos = "__".join(
        f"{method}-{PIPELINE_FILENAME_LABELS[pipeline]}"
        for pipeline in pipelines
        for method in curve_methods
    )
    signal_label = signal_nature.replace("-", "")
    return (
        f"angspec_group{group.upper()}_{spacing_label}_{signal_label}_"
        f"M{num_targets}_az{az_label}_el{el_label}_T{snapshots}_snr{snr:g}_{combos}"
    ).replace("+", "p").replace("-", "m")


def shorten_output_stem(output_stem: str, output_dir: Path, output_format: str):
    candidate = output_dir / f"{output_stem}.{output_format}"
    if len(str(candidate)) <= 220:
        return output_stem

    digest = hashlib.sha1(output_stem.encode("utf-8")).hexdigest()[:12]
    head = output_stem.split("_", 9)
    if len(head) >= 9:
        compact_prefix = "_".join(head[:9])
    else:
        compact_prefix = output_stem[:80]
    compact_prefix = compact_prefix[:110].rstrip("_")
    return f"{compact_prefix}_cfg{digest}"


def build_default_title(group: str, spacing_value: float, signal_nature: str, snapshots: int, snr: float):
    signal_label = "Non-coherent" if signal_nature == "non-coherent" else "Coherent"
    return (
        f"Angular Spectra | Group {group.upper()} | {spacing_value:g} lambda | "
        f"{signal_label} | T={snapshots} | SNR={snr:g} dB"
    )


def plot_spectra(
    output_path: Path,
    title: str,
    curve_payloads: list[dict],
    estimate_payloads: list[dict],
    true_azimuths_deg: list[float],
    show_peak_markers: bool,
):
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = plt.cm.tab20(np.linspace(0, 1, max(1, len(curve_payloads))))

    for idx, payload in enumerate(curve_payloads):
        normalized = payload["spectrum"] / (np.max(payload["spectrum"]) + 1e-12)
        ax.plot(
            payload["ang_grid_deg"],
            normalized,
            linewidth=1.6,
            color=colors[idx],
            label=payload["label"],
        )
        if show_peak_markers and payload["predictions"].size > 0:
            for pred_idx, value in enumerate(payload["predictions"]):
                ax.axvline(
                    value,
                    color=colors[idx],
                    linestyle=":",
                    linewidth=1.1,
                    alpha=0.7,
                    label=f"{payload['label']} peak" if pred_idx == 0 else None,
                )

    for idx, value in enumerate(true_azimuths_deg):
        ax.axvline(
            value,
            color="black",
            linestyle="--",
            linewidth=1.4,
            alpha=0.85,
            label="True DOA" if idx == 0 else None,
        )

    overlay_styles = {
        "root-music": "-.",
        "esprit": (0, (3, 1, 1, 1)),
    }
    overlay_color_map = {
        pipeline_key: colors[min(idx, len(colors) - 1)]
        for idx, pipeline_key in enumerate([payload["pipeline_key"] for payload in curve_payloads])
    }
    for payload in estimate_payloads:
        color = overlay_color_map.get(payload["pipeline_key"], "tab:gray")
        linestyle = overlay_styles.get(payload["method_name"], "-.")
        for pred_idx, value in enumerate(payload["predictions"]):
            ax.axvline(
                value,
                color=color,
                linestyle=linestyle,
                linewidth=1.2,
                alpha=0.8,
                label=payload["label"] if pred_idx == 0 else None,
            )

    ax.set_title(title)
    ax.set_xlabel("Angle [deg]")
    ax.set_ylabel("Normalized spectrum [a.u.]")
    ax.set_ylim(0.0, 1.05)
    ax.grid(True, alpha=0.25)
    ax.legend(loc="upper right", fontsize=8, ncol=2)
    fig.tight_layout()
    fig.savefig(output_path, dpi=220)
    plt.close(fig)


def plot_method_specific_spectra(
    output_path: Path,
    title: str,
    method_name: str,
    curve_payloads: list[dict],
    estimate_payloads: list[dict],
    true_azimuths_deg: list[float],
    show_peak_markers: bool,
):
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = plt.cm.tab10(np.linspace(0, 1, max(1, len(curve_payloads))))

    for idx, payload in enumerate(curve_payloads):
        normalized = payload["spectrum"] / (np.max(payload["spectrum"]) + 1e-12)
        ax.plot(
            payload["ang_grid_deg"],
            normalized,
            linewidth=1.8,
            color=colors[idx],
            label=PIPELINE_CONFIGS[payload["pipeline_key"]]["label"],
        )
        if show_peak_markers and payload["predictions"].size > 0:
            for pred_idx, value in enumerate(payload["predictions"]):
                ax.axvline(
                    value,
                    color=colors[idx],
                    linestyle=":",
                    linewidth=1.1,
                    alpha=0.75,
                    label=(
                        f"{PIPELINE_CONFIGS[payload['pipeline_key']]['label']} peak"
                        if pred_idx == 0
                        else None
                    ),
                )

    overlay_styles = {
        "root-music": "-.",
        "esprit": (0, (3, 1, 1, 1)),
    }
    for payload in estimate_payloads:
        pipeline_label = PIPELINE_CONFIGS[payload["pipeline_key"]]["label"]
        color_idx = min(
            next(
                (
                    idx
                    for idx, curve_payload in enumerate(curve_payloads)
                    if curve_payload["pipeline_key"] == payload["pipeline_key"]
                ),
                0,
            ),
            len(colors) - 1,
        )
        color = colors[color_idx]
        linestyle = overlay_styles.get(payload["method_name"], "-.")
        for pred_idx, value in enumerate(payload["predictions"]):
            ax.axvline(
                value,
                color=color,
                linestyle=linestyle,
                linewidth=1.2,
                alpha=0.8,
                label=(
                    f"{METHOD_LABELS[payload['method_name']]} | {pipeline_label}"
                    if pred_idx == 0
                    else None
                ),
            )

    for idx, value in enumerate(true_azimuths_deg):
        ax.axvline(
            value,
            color="black",
            linestyle="--",
            linewidth=1.4,
            alpha=0.85,
            label="True DOA" if idx == 0 else None,
        )

    ax.set_title(f"{title} | {METHOD_LABELS[method_name]}")
    ax.set_xlabel("Angle [deg]")
    ax.set_ylabel("Normalized spectrum [a.u.]")
    ax.set_ylim(0.0, 1.05)
    ax.grid(True, alpha=0.25)
    ax.legend(loc="upper right", fontsize=8, ncol=2)
    fig.tight_layout()
    fig.savefig(output_path, dpi=220)
    plt.close(fig)


def write_curve_payloads_csv(output_path: Path, curve_payloads: list[dict]):
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "method",
                "pipeline",
                "angle_deg",
                "normalized_spectrum",
                "raw_spectrum",
            ]
        )
        for payload in curve_payloads:
            normalized = payload["spectrum"] / (np.max(payload["spectrum"]) + 1e-12)
            for angle_deg, normalized_value, raw_value in zip(
                payload["ang_grid_deg"], normalized, payload["spectrum"]
            ):
                writer.writerow(
                    [
                        payload["method_name"],
                        payload["pipeline_key"],
                        float(angle_deg),
                        float(normalized_value),
                        float(raw_value),
                    ]
                )


def write_estimate_payloads_csv(output_path: Path, estimate_payloads: list[dict]):
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["method", "pipeline", "prediction_deg"])
        for payload in estimate_payloads:
            for value in payload["predictions"]:
                writer.writerow(
                    [
                        payload["method_name"],
                        payload["pipeline_key"],
                        float(value),
                    ]
                )


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    group = args.array_group.lower()
    spacing_label, spacing_value = normalize_spacing(args.spacing)
    signal_nature = normalize_signal_nature(args.signal_nature)
    azimuths_deg = parse_float_list(args.target_azimuths)
    if azimuths_deg is None:
        raise ValueError("target-azimuths must be provided")
    elevations_deg = parse_float_list(
        args.target_elevations, default_value=0.0, count=len(azimuths_deg)
    )

    if args.num_targets != len(azimuths_deg):
        raise ValueError(
            f"num-targets={args.num_targets} does not match the number of target azimuths ({len(azimuths_deg)})"
        )
    if len(elevations_deg) != len(azimuths_deg):
        raise ValueError("target-elevations must match target-azimuths in length")

    pipelines = normalize_pipeline_list(args.pipelines)
    curve_methods = normalize_method_list(args.curve_methods, CURVE_METHODS, "curve method")
    estimate_methods = normalize_method_list(
        args.estimate_overlays, ESTIMATE_METHODS, "estimate overlay"
    )

    baseline_template = load_template(repo_root, group, spacing_label, "sample")
    base_params = build_scene_params(baseline_template, args, azimuths_deg, elevations_deg)
    _, observations = generate_scene_observations(base_params, azimuths_deg, elevations_deg)

    curve_payloads = []
    estimate_payloads = []
    for pipeline_key in pipelines:
        template = load_template(repo_root, group, spacing_label, pipeline_key)
        params = build_scene_params(template, args, azimuths_deg, elevations_deg)
        for method_name in curve_methods:
            curve_payloads.append(
                compute_curve(method_name, pipeline_key, params, observations)
            )
        for method_name in estimate_methods:
            estimate_payloads.append(
                compute_estimate_overlay(method_name, pipeline_key, params, observations)
            )

    output_dir = (repo_root / args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_stem = build_output_stem(
        group=group,
        spacing_label=spacing_label,
        signal_nature=signal_nature,
        num_targets=args.num_targets,
        azimuths_deg=azimuths_deg,
        elevations_deg=elevations_deg,
        snapshots=args.snapshots,
        snr=args.snr,
        curve_methods=curve_methods,
        pipelines=pipelines,
    )
    output_stem = shorten_output_stem(output_stem, output_dir, args.output_format)
    run_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = output_dir / f"{output_stem}_{run_stamp}"
    run_dir.mkdir(parents=True, exist_ok=True)
    output_path = run_dir / f"{output_stem}_combined.{args.output_format}"
    title = args.figure_title or build_default_title(
        group=group,
        spacing_value=spacing_value,
        signal_nature=signal_nature,
        snapshots=args.snapshots,
        snr=args.snr,
    )

    for method_name in curve_methods:
        method_curve_payloads = [
            payload for payload in curve_payloads if payload["method_name"] == method_name
        ]
        plot_method_specific_spectra(
            output_path=run_dir / f"{output_stem}_{method_name}.{args.output_format}",
            title=title,
            method_name=method_name,
            curve_payloads=method_curve_payloads,
            estimate_payloads=estimate_payloads,
            true_azimuths_deg=azimuths_deg,
            show_peak_markers=args.peak_markers,
        )
        if args.export_csv:
            write_curve_payloads_csv(
                run_dir / f"{output_stem}_{method_name}.csv",
                method_curve_payloads,
            )

    plot_spectra(
        output_path=output_path,
        title=title,
        curve_payloads=curve_payloads,
        estimate_payloads=estimate_payloads,
        true_azimuths_deg=azimuths_deg,
        show_peak_markers=args.peak_markers,
    )
    if args.export_csv:
        write_curve_payloads_csv(run_dir / f"{output_stem}_combined.csv", curve_payloads)
        if estimate_payloads:
            write_estimate_payloads_csv(
                run_dir / f"{output_stem}_estimates.csv", estimate_payloads
            )
    print(f"Saved angular spectrum figures to {run_dir}")


if __name__ == "__main__":
    main()
