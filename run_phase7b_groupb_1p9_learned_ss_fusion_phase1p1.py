"""Launch Phase 7B Phase 1.1 Group B learned SS-fusion experiment family."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


PHASE1P1_EXPERIMENTS = [
    "phase7b_gb19_coh_g1_s1_ss33_subspacenet_phase1p1",
    "phase7b_gb19_coh_g1_s1_ss23_r01_subspacenet_phase1p1",
    "phase7b_gb19_coh_g1_s1_ssfusion_subspacenet_phase1p1",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Run Phase 7B Phase 1.1 Group B 1.9 lambda learned SS-fusion experiments "
            "for the primary coherent hard cell."
        )
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase7b_groupb_1p9_learned_ss_fusion_phase1p1",
        help="Dedicated output directory for the Phase 7B Phase 1.1 study.",
    )
    parser.add_argument(
        "--templates-dir",
        default="data/dataset_templates/ablation/phase7b_groupb_1p9_learned_ss_fusion_phase1p1",
        help="Generated template directory for the Phase 7B Phase 1.1 study.",
    )
    return parser.parse_args()


def ensure_phase7b_phase1p1_templates(repo_root: Path, generated_templates_dir: Path):
    source_path = (
        repo_root
        / "data"
        / "dataset_templates"
        / "ablation"
        / "phase6_groupb_1p9_coherent_fixed_gap_snr_grid"
        / "phase6_groupb_1p9_coherent_subspacenet_esprit_gap1_snr1.json"
    )
    generated_templates_dir.mkdir(parents=True, exist_ok=True)

    with source_path.open("r", encoding="utf-8-sig") as handle:
        source_template = json.load(handle)

    variants = [
        {
            "template_name": "phase7b_gb19_coh_g1_s1_ss33_subspacenet_phase1p1",
            "description": (
                "Phase 7B Phase 1.1 coherent Group B 1.9 lambda learned baseline for "
                "gap=1 deg and SNR=1 dB using SS(3/3) -> LRMC -> SubspaceNet -> ESPRIT."
            ),
            "scheme_label": "Coherent | Gap = 1 deg | SNR = 1 dB | SS(3/3) -> LRMC -> SubspaceNet",
            "model_type": "SubspaceNet",
            "ss_num_subarrays": 3,
            "ss_row_subset": [0, 1, 2],
        },
        {
            "template_name": "phase7b_gb19_coh_g1_s1_ss23_r01_subspacenet_phase1p1",
            "description": (
                "Phase 7B Phase 1.1 coherent Group B 1.9 lambda fixed-best-pair learned "
                "baseline for gap=1 deg and SNR=1 dB using SS(2/3: rows 0+1) -> LRMC -> "
                "SubspaceNet -> ESPRIT."
            ),
            "scheme_label": "Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 0+1) -> LRMC -> SubspaceNet",
            "model_type": "SubspaceNet",
            "ss_num_subarrays": 2,
            "ss_row_subset": [0, 1],
        },
        {
            "template_name": "phase7b_gb19_coh_g1_s1_ssfusion_subspacenet_phase1p1",
            "description": (
                "Phase 7B Phase 1.1 coherent Group B 1.9 lambda learned SS-fusion model "
                "for gap=1 deg and SNR=1 dB using three SS(2/3) -> LRMC branches followed by "
                "learned fusion and the SubspaceNet-ESPRIT backbone."
            ),
            "scheme_label": "Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3 x 3) -> LRMC -> learned fusion -> SubspaceNet",
            "model_type": "SubspaceNetSSFusionEspritPhase1p1",
            "ss_num_subarrays": None,
            "ss_row_subset": None,
        },
    ]

    for variant in variants:
        template = json.loads(json.dumps(source_template))
        template["template_name"] = variant["template_name"]
        template["description"] = variant["description"]
        template["scenario_data_path"] = "p7b_p1p1_coh_g1_s1_45k"
        template["methods"] = ["esprit"]
        template["seed"] = 42

        template["commands"]["CREATE_DATA"] = True
        template["commands"]["CACHE_DATASET"] = True
        template["commands"]["LOAD_DATA"] = False
        template["commands"]["TRAIN_MODEL"] = True
        template["commands"]["EVALUATE_MODE"] = True

        system_model = template["system_model"]
        if variant["ss_num_subarrays"] is None:
            system_model.pop("ss_num_subarrays", None)
            system_model.pop("ss_row_subset", None)
        else:
            system_model["ss_num_subarrays"] = variant["ss_num_subarrays"]
            system_model["ss_row_subset"] = variant["ss_row_subset"]
        system_model["ss_fusion_branch_subsets"] = [[0, 1], [0, 2], [1, 2]]
        system_model["ss_fusion_hidden_channels"] = 16
        system_model["ss_fusion_diagonal_loading"] = 1e-6

        model = template["model"]
        model["model_type"] = variant["model_type"]
        model["diff_method"] = "esprit"
        model["tau"] = 8

        report = template["report"]
        report["markdown_output"] = "phase7b_groupb_1p9_learned_ss_fusion_phase1p1_results.md"
        report["markdown_title"] = (
            "Phase 7B Phase 1.1 - Group B 1.9 Lambda Learned SS-Fusion Primary Hard Cell"
        )
        report["markdown_description"] = (
            "Phase 7B Phase 1.1 compares the primary coherent hard-cell learned SS-fusion "
            "candidate against the current SS(3/3) learned baseline and the best fixed "
            "SS(2/3: rows 0+1) learned baseline."
        )
        report["markdown_conditions"] = [
            "Phase: 1.1 primary hard-cell reproduction",
            "Array: Group B 12-channel 2D hardware geometry",
            "Physical spacing: 1.9 lambda",
            "Signals: 2 coherent narrowband targets",
            "Cell: gap = 1 deg, SNR = 1 dB, T = 40",
            "Azimuth and elevation range: [-15 deg, 15 deg]",
            "Training scale: 45,000 samples total with 9,000 test samples",
            "Learned head: ESPRIT",
            "Candidate model: SubspaceNetSSFusionEspritPhase1p1",
            "Fixed learned baselines: SS(3/3) and SS(2/3: rows 0+1)",
            "Metric: horizontal-angle RMSE in degrees (periodic matching)",
        ]
        report["write_summary_csv"] = True
        report["markdown_scheme_label"] = variant["scheme_label"]

        target_path = generated_templates_dir / f"{variant['template_name']}.json"
        with target_path.open("w", encoding="utf-8") as handle:
            json.dump(template, handle, indent=2)
            handle.write("\n")


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    templates_dir = (repo_root / args.templates_dir).resolve()
    ensure_phase7b_phase1p1_templates(repo_root, templates_dir)

    command = [
        sys.executable,
        str(repo_root / "run_ablation.py"),
        "--templates-dir",
        str(Path(args.templates_dir).as_posix()),
        "--experiments",
        ",".join(PHASE1P1_EXPERIMENTS),
        "--seed",
        str(args.seed),
        "--results-dir",
        args.results_dir,
    ]
    print(
        "Phase 7B Phase 1.1 experiment: Group B 1.9 lambda learned SS-fusion "
        "primary coherent hard-cell family"
    )
    print("Results will be written under:", args.results_dir)
    print("Command:", " ".join(command))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
