"""Launch Phase 6 non-coherent Group B fixed-gap/SNR controls without SS -> LRMC."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


GAPS_DEG = [5, 4, 3, 2, 1]
SNRS_DB = [1, 5, 10, 15]


def build_experiments() -> list[str]:
    experiments = []
    for gap in GAPS_DEG:
        for snr in SNRS_DB:
            experiments.append(
                f"phase6_groupb_1p9_noncoherent_control_no_preproc_gap{gap}_snr{snr}"
            )
    return experiments


PHASE6_NONCOHERENT_EXPERIMENTS = build_experiments()


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Run Phase 6 non-coherent Group B 1.9 lambda fixed-gap/SNR classical "
            "controls without SS -> LRMC preprocessing."
        )
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase6_groupb_1p9_noncoherent_fixed_gap_snr_grid_no_preproc",
        help="Dedicated output directory for the no-preprocessing non-coherent Phase 6 study.",
    )
    parser.add_argument(
        "--templates-dir",
        default="data/dataset_templates/ablation/phase6_groupb_1p9_noncoherent_fixed_gap_snr_grid_no_preproc",
        help="Generated template directory for the no-preprocessing non-coherent Phase 6 study.",
    )
    return parser.parse_args()


def ensure_phase6_noncoherent_templates(repo_root: Path, generated_templates_dir: Path):
    source_dir = (
        repo_root
        / "data"
        / "dataset_templates"
        / "ablation"
        / "phase6b_groupb_1p9_coherent_fixed_gap_snr_grid_no_preproc"
    )
    generated_templates_dir.mkdir(parents=True, exist_ok=True)

    for gap in GAPS_DEG:
        for snr in SNRS_DB:
            source_name = (
                f"phase6b_groupb_1p9_coherent_control_no_preproc_gap{gap}_snr{snr}.json"
            )
            target_name = (
                f"phase6_groupb_1p9_noncoherent_control_no_preproc_gap{gap}_snr{snr}.json"
            )
            with (source_dir / source_name).open("r", encoding="utf-8-sig") as handle:
                template = json.load(handle)

            template["template_name"] = target_name[:-5]
            template["description"] = (
                f"Phase 6 non-coherent Group B 1.9 lambda classical control cell at "
                f"gap={gap} deg and SNR={snr} dB without SS -> LRMC preprocessing."
            )
            # Keep the cache folder short enough for Windows path limits.
            template["scenario_data_path"] = f"p6nc_np_g{gap}_s{snr}_45k"

            system_model = template["system_model"]
            system_model["signal_nature"] = "non-coherent"

            report = template["report"]
            report["markdown_output"] = (
                "phase6_groupb_1p9_noncoherent_fixed_gap_snr_grid_no_preproc_results.md"
            )
            report["markdown_title"] = (
                "Phase 6 - Group B 1.9 Lambda Non-Coherent Fixed-Gap and SNR Grid Without SS -> LRMC"
            )
            report["markdown_description"] = (
                "This experiment evaluates the non-coherent Group B raw classical controls "
                "without SS -> LRMC preprocessing on the same fixed-gap and SNR grid used in the Phase 6 studies."
            )
            report["markdown_conditions"] = [
                "Array: Group B 12-channel 2D hardware geometry",
                "Physical spacing: 1.9 lambda",
                "Signals: 2 non-coherent narrowband targets",
                "Snapshots: T = 40",
                "Azimuth and elevation range: [-15 deg, 15 deg]",
                "Fixed azimuth separations: 1, 2, 3, 4, 5 deg",
                "SNR sweep: 1, 5, 10, 15 dB",
                "Preprocessing: none",
                "Control methods: DBF, MUSIC, Root-MUSIC, ESPRIT",
                "Dataset size per cell: 45,000 samples",
                "Metric: horizontal-angle RMSE in degrees (periodic matching)",
            ]
            report["write_summary_csv"] = True
            report["markdown_scheme_label"] = (
                f"Gap = {gap} deg | SNR = {snr} dB | No preprocessing"
            )

            with (generated_templates_dir / target_name).open(
                "w", encoding="utf-8"
            ) as handle:
                json.dump(template, handle, indent=2)
                handle.write("\n")


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    templates_dir = (repo_root / args.templates_dir).resolve()
    ensure_phase6_noncoherent_templates(repo_root, templates_dir)

    command = [
        sys.executable,
        str(repo_root / "run_ablation.py"),
        "--templates-dir",
        str(Path(args.templates_dir).as_posix()),
        "--experiments",
        ",".join(PHASE6_NONCOHERENT_EXPERIMENTS),
        "--seed",
        str(args.seed),
        "--results-dir",
        args.results_dir,
    ]
    print(
        "Phase 6 experiment: non-coherent Group B 1.9 lambda fixed-gap/SNR classical "
        "controls without SS -> LRMC preprocessing"
    )
    print("Results will be written under:", args.results_dir)
    print("Command:", " ".join(command))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
