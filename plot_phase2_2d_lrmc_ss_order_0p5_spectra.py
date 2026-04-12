"""Generate spectrum plots for the phase2 0.5 lambda 2D order study."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch

from src.data_handler import load_datasets
from src.dataset_template import build_system_model_params_from_template
from src.methods import Esprit, MUSIC, RootMUSIC
from src.utils import R2D


CASE_ORDER = [
    "phase2b_2d_0p5_baseline",
    "phase2b_2d_0p5_ss_only",
    "phase2b_2d_0p5_lrmc_only",
    "phase2b_2d_0p5_ss_lrmc",
    "phase2b_2d_0p5_lrmc_ss",
]

CASE_LABELS = {
    "phase2b_2d_0p5_baseline": "Baseline",
    "phase2b_2d_0p5_ss_only": "Spatial smoothing only",
    "phase2b_2d_0p5_lrmc_only": "LRMC only",
    "phase2b_2d_0p5_ss_lrmc": "SS -> LRMC",
    "phase2b_2d_0p5_lrmc_ss": "LRMC -> SS",
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate MUSIC spectrum plots for the phase2 0.5 lambda study."
    )
    parser.add_argument(
        "--results-dir",
        default="results/phase2_2d_lrmc_ss_order_0p5",
        help="Root results directory containing the experiment subfolders.",
    )
    parser.add_argument(
        "--datasets-root",
        default="data/datasets",
        help="Root dataset directory used by the experiments.",
    )
    parser.add_argument(
        "--sample-index",
        type=int,
        default=0,
        help="Test-sample index to plot for every case.",
    )
    parser.add_argument(
        "--zoom-min",
        type=float,
        default=-20.0,
        help="Lower x-axis limit for the zoomed figure.",
    )
    parser.add_argument(
        "--zoom-max",
        type=float,
        default=20.0,
        help="Upper x-axis limit for the zoomed figure.",
    )
    return parser.parse_args()


def load_case_context(repo_root: Path, case_name: str):
    case_dir = repo_root / "results" / "phase2_2d_lrmc_ss_order_0p5" / case_name
    resolved_template = case_dir / "resolved_template.json"
    if not resolved_template.exists():
        raise FileNotFoundError(f"Missing resolved template: {resolved_template}")
    template = json.loads(resolved_template.read_text(encoding="utf-8"))
    params = build_system_model_params_from_template(template)
    params.set_parameter("template_name", template["template_name"])
    datasets_path = repo_root / "data" / "datasets" / template["template_name"]
    _, generic_test_dataset, samples_model = load_datasets(
        system_model_params=params,
        model_type="Classical",
        samples_size=int(template["dataset"]["samples_size"]),
        datasets_path=datasets_path,
        train_test_ratio=float(template["dataset"]["train_test_ratio"]),
        is_training=False,
    )
    return template, samples_model, generic_test_dataset


def compute_case_outputs(samples_model, sample_x: torch.Tensor, template: dict):
    mode = str(template.get("system_model", {}).get("covariance_mode", "sample")).lower()
    system_model = samples_model
    x_np = np.asarray(sample_x.cpu().numpy(), dtype=np.complex128)

    music = MUSIC(system_model)
    music_predictions, music_spectrum, _ = music.narrowband(x_np, mode=mode)

    root_music = RootMUSIC(system_model)
    root_predictions, _, _, _, _ = root_music.narrowband(x_np, mode=mode)

    esprit = Esprit(system_model)
    esprit_predictions, _ = esprit.narrowband(x_np, mode=mode)

    return {
        "music": {
            "spectrum": np.abs(np.asarray(music_spectrum)),
            "predictions": np.asarray(music_predictions, dtype=float),
        },
        "root-music": {
            "predictions": np.asarray(root_predictions, dtype=float),
        },
        "esprit": {
            "predictions": np.asarray(esprit_predictions, dtype=float),
        },
    }


def plot_case_figure(
    output_path: Path,
    title: str,
    ang_grid_deg: np.ndarray,
    spectrum: np.ndarray,
    true_doa_deg: np.ndarray,
    music_predictions: np.ndarray,
    root_predictions: np.ndarray,
    esprit_predictions: np.ndarray,
    xlim: tuple[float, float] | None = None,
):
    fig, ax = plt.subplots(figsize=(10, 5))
    normalized = spectrum / (np.max(spectrum) + 1e-12)
    ax.plot(ang_grid_deg, normalized, color="tab:blue", lw=1.6, label="MUSIC spectrum")

    def add_markers(values, label, color, linestyle):
        values = np.asarray(values, dtype=float).reshape(-1)
        first = True
        for value in values:
            ax.axvline(
                value,
                color=color,
                linestyle=linestyle,
                alpha=0.85,
                linewidth=1.5,
                label=label if first else None,
            )
            first = False

    add_markers(true_doa_deg, "True DOA", "black", "--")
    add_markers(music_predictions, "MUSIC estimate", "tab:blue", ":")
    add_markers(root_predictions, "Root-MUSIC estimate", "tab:orange", "-.")
    add_markers(esprit_predictions, "ESPRIT estimate", "tab:green", (0, (3, 1, 1, 1)))

    ax.set_title(title)
    ax.set_xlabel("Angle [deg]")
    ax.set_ylabel("Normalized spectrum [a.u.]")
    ax.grid(True, alpha=0.25)
    if xlim is not None:
        ax.set_xlim(*xlim)
    ax.set_ylim(0.0, 1.05)
    ax.legend(loc="upper right", fontsize=8, ncol=2)
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def plot_overview(
    output_path: Path,
    case_payloads: list[dict],
    xlim: tuple[float, float] | None = None,
):
    fig, axes = plt.subplots(len(case_payloads), 1, figsize=(12, 3.0 * len(case_payloads)), sharex=True)
    if len(case_payloads) == 1:
        axes = [axes]
    for ax, payload in zip(axes, case_payloads):
        spectrum = payload["music"]["spectrum"]
        ang_grid_deg = payload["ang_grid_deg"]
        normalized = spectrum / (np.max(spectrum) + 1e-12)
        ax.plot(ang_grid_deg, normalized, color="tab:blue", lw=1.4)
        for doa in payload["true_doa_deg"]:
            ax.axvline(doa, color="black", linestyle="--", alpha=0.8, linewidth=1.2)
        for value in payload["music"]["predictions"]:
            ax.axvline(value, color="tab:blue", linestyle=":", alpha=0.8, linewidth=1.1)
        for value in payload["root-music"]["predictions"]:
            ax.axvline(value, color="tab:orange", linestyle="-.", alpha=0.8, linewidth=1.1)
        for value in payload["esprit"]["predictions"]:
            ax.axvline(value, color="tab:green", linestyle=(0, (3, 1, 1, 1)), alpha=0.8, linewidth=1.1)
        ax.set_ylabel(payload["label"])
        ax.grid(True, alpha=0.2)
        ax.set_ylim(0.0, 1.05)
        if xlim is not None:
            ax.set_xlim(*xlim)
    axes[-1].set_xlabel("Angle [deg]")
    fig.suptitle("Phase 2 0.5 lambda angle spectra for the same sample across cases", y=0.995)
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    results_root = (repo_root / args.results_dir).resolve()
    output_root = results_root / "spectra"
    case_output_root = output_root / "cases"
    case_output_root.mkdir(parents=True, exist_ok=True)

    case_payloads = []
    print(f"Plotting sample index {args.sample_index} for:")
    for case_name in CASE_ORDER:
        template, samples_model, generic_test_dataset = load_case_context(repo_root, case_name)
        if args.sample_index >= len(generic_test_dataset):
            raise IndexError(
                f"sample-index {args.sample_index} is out of range for {case_name} "
                f"(dataset size {len(generic_test_dataset)})"
            )
        sample_x, sample_y = generic_test_dataset[args.sample_index]
        outputs = compute_case_outputs(samples_model, sample_x, template)
        ang_grid_deg = MUSIC(samples_model)._angels * R2D
        true_doa_deg = np.asarray(sample_y.cpu().numpy(), dtype=float) * R2D
        case_payload = {
            "case_name": case_name,
            "label": CASE_LABELS[case_name],
            "music": outputs["music"],
            "root-music": outputs["root-music"],
            "esprit": outputs["esprit"],
            "true_doa_deg": true_doa_deg,
            "ang_grid_deg": ang_grid_deg,
        }
        case_payloads.append(case_payload)
        print(
            f"- {case_name}: true DOA {np.round(case_payload['true_doa_deg'], 3).tolist()} deg"
        )
        plot_case_figure(
            output_path=case_output_root / f"{case_name}_spectrum_full.png",
            title=f"{CASE_LABELS[case_name]} | sample {args.sample_index}",
            ang_grid_deg=ang_grid_deg,
            spectrum=case_payload["music"]["spectrum"],
            true_doa_deg=case_payload["true_doa_deg"],
            music_predictions=case_payload["music"]["predictions"],
            root_predictions=case_payload["root-music"]["predictions"],
            esprit_predictions=case_payload["esprit"]["predictions"],
            xlim=(-90.0, 90.0),
        )
        plot_case_figure(
            output_path=case_output_root / f"{case_name}_spectrum_zoom.png",
            title=f"{CASE_LABELS[case_name]} | sample {args.sample_index} (zoom)",
            ang_grid_deg=ang_grid_deg,
            spectrum=case_payload["music"]["spectrum"],
            true_doa_deg=case_payload["true_doa_deg"],
            music_predictions=case_payload["music"]["predictions"],
            root_predictions=case_payload["root-music"]["predictions"],
            esprit_predictions=case_payload["esprit"]["predictions"],
            xlim=(args.zoom_min, args.zoom_max),
        )

    plot_overview(
        output_path=output_root / "phase2_2d_lrmc_ss_order_0p5_spectra_overview.png",
        case_payloads=case_payloads,
        xlim=(-90.0, 90.0),
    )
    plot_overview(
        output_path=output_root / "phase2_2d_lrmc_ss_order_0p5_spectra_zoom.png",
        case_payloads=case_payloads,
        xlim=(args.zoom_min, args.zoom_max),
    )
    print(f"Saved spectrum plots to {output_root}")


if __name__ == "__main__":
    main()
