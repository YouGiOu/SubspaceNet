"""Launch Phase 7A Group B 1.9 lambda two-subarray SS floor screening."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


STAGE_A_CELLS = [
    (1, 1),
    (2, 1),
    (1, 10),
    (3, 10),
    (5, 10),
]

SIGNAL_REGIMES = [
    ("coherent", "coh"),
    ("non-coherent", "noncoh"),
]

SS_VARIANTS = [
    {
        "key": "ss33",
        "label": "SS(3/3) -> LRMC",
        "ss_num_subarrays": 3,
        "ss_row_subset": [0, 1, 2],
        "description": "full three-row spatial smoothing before LRMC",
    },
    {
        "key": "ss23_r01",
        "label": "SS(2/3: rows 0+1) -> LRMC",
        "ss_num_subarrays": 2,
        "ss_row_subset": [0, 1],
        "description": "two-of-three spatial smoothing with rows 0+1 before LRMC",
    },
    {
        "key": "ss23_r02",
        "label": "SS(2/3: rows 0+2) -> LRMC",
        "ss_num_subarrays": 2,
        "ss_row_subset": [0, 2],
        "description": "two-of-three spatial smoothing with rows 0+2 before LRMC",
    },
    {
        "key": "ss23_r12",
        "label": "SS(2/3: rows 1+2) -> LRMC",
        "ss_num_subarrays": 2,
        "ss_row_subset": [1, 2],
        "description": "two-of-three spatial smoothing with rows 1+2 before LRMC",
    },
]


def build_experiments() -> list[str]:
    experiments: list[str] = []
    for signal_nature, signal_key in SIGNAL_REGIMES:
        for gap, snr in STAGE_A_CELLS:
            for variant in SS_VARIANTS:
                experiments.append(
                    f"phase7_gb19_{signal_key}_g{gap}_s{snr}_{variant['key']}"
                )
    return experiments


PHASE7_STAGE_A_EXPERIMENTS = build_experiments()


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Run Phase 7A Group B 1.9 lambda two-subarray spatial-smoothing floor "
            "screening for classical controls."
        )
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase7_groupb_1p9_ss_two_subarray_floor",
        help="Dedicated output directory for the Phase 7A screening study.",
    )
    parser.add_argument(
        "--templates-dir",
        default="data/dataset_templates/ablation/phase7_groupb_1p9_ss_two_subarray_floor",
        help="Generated template directory for the Phase 7A screening study.",
    )
    return parser.parse_args()


def _source_template_name(signal_nature: str, gap: int, snr: int) -> str:
    regime_prefix = "coherent" if signal_nature == "coherent" else "noncoherent"
    return f"phase6_groupb_1p9_{regime_prefix}_control_gap{gap}_snr{snr}.json"


def _source_templates_dir(repo_root: Path, signal_nature: str) -> Path:
    regime_dir = (
        "phase6_groupb_1p9_coherent_fixed_gap_snr_grid"
        if signal_nature == "coherent"
        else "phase6_groupb_1p9_noncoherent_fixed_gap_snr_grid"
    )
    return (
        repo_root
        / "data"
        / "dataset_templates"
        / "ablation"
        / regime_dir
    )


def ensure_phase7_templates(repo_root: Path, generated_templates_dir: Path):
    generated_templates_dir.mkdir(parents=True, exist_ok=True)

    for signal_nature, signal_key in SIGNAL_REGIMES:
        source_dir = _source_templates_dir(repo_root, signal_nature)
        regime_title = "Coherent" if signal_nature == "coherent" else "Non-Coherent"

        for gap, snr in STAGE_A_CELLS:
            source_name = _source_template_name(signal_nature, gap, snr)
            with (source_dir / source_name).open("r", encoding="utf-8-sig") as handle:
                source_template = json.load(handle)

            for variant in SS_VARIANTS:
                template = json.loads(json.dumps(source_template))
                template_name = (
                    f"phase7_gb19_{signal_key}_g{gap}_s{snr}_{variant['key']}"
                )
                target_name = f"{template_name}.json"

                template["template_name"] = template_name
                template["description"] = (
                    f"Phase 7A {signal_nature} Group B 1.9 lambda classical screening "
                    f"cell at gap={gap} deg and SNR={snr} dB using "
                    f"{variant['description']}."
                )
                template["methods"] = ["dbf", "music", "root-music", "esprit"]
                template["commands"]["CREATE_DATA"] = True
                template["commands"]["LOAD_DATA"] = True
                template["commands"]["TRAIN_MODEL"] = False
                template["commands"]["EVALUATE_MODE"] = True
                template["scenario_data_path"] = (
                    f"p7_ssfloor_{signal_key}_g{gap}_s{snr}_45k"
                )

                system_model = template["system_model"]
                system_model["signal_nature"] = signal_nature
                system_model["covariance_mode"] = "ss_then_lrmc"
                system_model["use_lrmc"] = True
                system_model["ss_num_subarrays"] = variant["ss_num_subarrays"]
                system_model["ss_row_subset"] = variant["ss_row_subset"]

                report = template["report"]
                report["markdown_output"] = (
                    "phase7_groupb_1p9_ss_two_subarray_floor_results.md"
                )
                report["markdown_title"] = (
                    "Phase 7A - Group B 1.9 Lambda Two-Subarray Spatial Smoothing Floor Screening"
                )
                report["markdown_description"] = (
                    "Phase 7A screens whether reducing Group B rowwise spatial smoothing "
                    "from three row blocks to specific two-of-three row pairs materially "
                    "changes classical SS -> LRMC performance under representative coherent "
                    "and non-coherent difficulty cells."
                )
                report["markdown_conditions"] = [
                    "Stage: A classical-first screening",
                    "Array: Group B 12-channel 2D hardware geometry",
                    "Physical spacing: 1.9 lambda",
                    f"Signals: 2 {signal_nature} narrowband targets",
                    "Snapshots: T = 40",
                    "Azimuth and elevation range: [-15 deg, 15 deg]",
                    "Gap/SNR cells: (1 deg, 1 dB), (2 deg, 1 dB), (1 deg, 10 dB), (3 deg, 10 dB), (5 deg, 10 dB)",
                    "Preprocessing family: rowwise SS -> LRMC",
                    "SS variants: full 3/3 baseline and all three 2/3 row-pair choices",
                    "Control methods: DBF, MUSIC, Root-MUSIC, ESPRIT",
                    "Dataset size per cell: 45,000 samples",
                    "Metric: horizontal-angle RMSE in degrees (periodic matching)",
                ]
                report["write_summary_csv"] = True
                report["markdown_scheme_label"] = (
                    f"{regime_title} | Gap = {gap} deg | SNR = {snr} dB | {variant['label']}"
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
    ensure_phase7_templates(repo_root, templates_dir)

    command = [
        sys.executable,
        str(repo_root / "run_ablation.py"),
        "--templates-dir",
        str(Path(args.templates_dir).as_posix()),
        "--experiments",
        ",".join(PHASE7_STAGE_A_EXPERIMENTS),
        "--seed",
        str(args.seed),
        "--results-dir",
        args.results_dir,
    ]
    print(
        "Phase 7A experiment: Group B 1.9 lambda two-subarray spatial-smoothing "
        "floor screening for classical controls"
    )
    print("Results will be written under:", args.results_dir)
    print("Command:", " ".join(command))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
