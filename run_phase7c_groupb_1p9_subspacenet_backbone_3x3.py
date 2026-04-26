"""Launch Phase 7C Group B 1.9 lambda SubspaceNet 3x3 backbone experiment family."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path


PHASE7C_EXPERIMENTS = [
    "phase7c_gb19_coh_g1_s1_ss33_backbone3x3",
    "phase7c_gb19_coh_g1_s1_ss23_r01_backbone3x3",
    "phase7c_gb19_coh_g1_s1_ssfusion_spatial_backbone3x3",
    "phase7c_gb19_coh_g1_s1_ssfusion_1x1_backbone3x3",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Run Phase 7C Group B 1.9 lambda 3x3 SubspaceNet backbone experiments "
            "for the primary coherent hard cell."
        )
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase7c_groupb_1p9_subspacenet_backbone_3x3",
        help="Dedicated output directory for the Phase 7C study.",
    )
    parser.add_argument(
        "--templates-dir",
        default="data/dataset_templates/ablation/phase7c_groupb_1p9_subspacenet_backbone_3x3",
        help="Generated template directory for the Phase 7C study.",
    )
    return parser.parse_args()


def ensure_phase7c_templates(repo_root: Path, generated_templates_dir: Path):
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
            "template_name": "phase7c_gb19_coh_g1_s1_ss33_backbone3x3",
            "description": (
                "Phase 7C coherent Group B 1.9 lambda learned baseline for gap=1 deg "
                "and SNR=1 dB using SS(3/3) -> LRMC -> SubspaceNet backbone 3x3 -> ESPRIT."
            ),
            "scheme_label": "Coherent | Gap = 1 deg | SNR = 1 dB | SS(3/3) -> LRMC -> SubspaceNet backbone 3x3",
            "model_type": "SubspaceNet",
            "ss_num_subarrays": 3,
            "ss_row_subset": [0, 1, 2],
            "fusion_label": "none",
        },
        {
            "template_name": "phase7c_gb19_coh_g1_s1_ss23_r01_backbone3x3",
            "description": (
                "Phase 7C coherent Group B 1.9 lambda fixed-best-pair learned baseline "
                "for gap=1 deg and SNR=1 dB using SS(2/3: rows 0+1) -> LRMC -> "
                "SubspaceNet backbone 3x3 -> ESPRIT."
            ),
            "scheme_label": "Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 0+1) -> LRMC -> SubspaceNet backbone 3x3",
            "model_type": "SubspaceNet",
            "ss_num_subarrays": 2,
            "ss_row_subset": [0, 1],
            "fusion_label": "none",
        },
        {
            "template_name": "phase7c_gb19_coh_g1_s1_ssfusion_spatial_backbone3x3",
            "description": (
                "Phase 7C coherent Group B 1.9 lambda spatial-fusion learned model "
                "for gap=1 deg and SNR=1 dB using SS(2/3 x 3) -> LRMC -> learned fusion "
                "-> SubspaceNet backbone 3x3 -> ESPRIT."
            ),
            "scheme_label": "Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3 x 3) -> LRMC -> learned fusion -> SubspaceNet backbone 3x3",
            "model_type": "SubspaceNetSSFusionEspritPhase1p1",
            "ss_num_subarrays": None,
            "ss_row_subset": None,
            "fusion_label": "spatial 3x3 fusion",
        },
        {
            "template_name": "phase7c_gb19_coh_g1_s1_ssfusion_1x1_backbone3x3",
            "description": (
                "Phase 7C coherent Group B 1.9 lambda 1x1-fusion learned model for "
                "gap=1 deg and SNR=1 dB using SS(2/3 x 3) -> LRMC -> 1x1 learned fusion "
                "-> SubspaceNet backbone 3x3 -> ESPRIT."
            ),
            "scheme_label": "Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3 x 3) -> LRMC -> 1x1 learned fusion -> SubspaceNet backbone 3x3",
            "model_type": "SubspaceNetSSFusionEspritPhase1p1p1",
            "ss_num_subarrays": None,
            "ss_row_subset": None,
            "fusion_label": "1x1 channel-only fusion",
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
        system_model["subspacenet_backbone_kernel_size"] = 3
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
        report["markdown_output"] = "phase7c_groupb_1p9_subspacenet_backbone_3x3_results.md"
        report["markdown_title"] = (
            "Phase 7C - Group B 1.9 Lambda SubspaceNet Backbone 3x3"
        )
        report["markdown_description"] = (
            "Phase 7C runs only the new 3x3-backbone learned variants in the primary "
            "coherent hard cell and compares them against the existing 2x2 Phase 7B references."
        )
        report["markdown_conditions"] = [
            "Array: Group B 12-channel 2D hardware geometry",
            "Physical spacing: 1.9 lambda",
            "Signals: 2 coherent narrowband targets",
            "Cell: gap = 1 deg, SNR = 1 dB, T = 40",
            "Azimuth and elevation range: [-15 deg, 15 deg]",
            "Training scale: 45,000 samples total with 9,000 test samples",
            "Learned head: ESPRIT",
            "Controlled variable: SubspaceNet backbone kernel size 2x2 vs 3x3",
            "Fusion blocks are unchanged relative to Phase 7B",
            "Metric: horizontal-angle RMSE in degrees (periodic matching)",
        ]
        report["write_summary_csv"] = True
        report["markdown_scheme_label"] = variant["scheme_label"]

        target_path = generated_templates_dir / f"{variant['template_name']}.json"
        with target_path.open("w", encoding="utf-8") as handle:
            json.dump(template, handle, indent=2)
            handle.write("\n")


def _read_rmse(metrics_path: Path):
    if not metrics_path.exists():
        return None
    payload = json.loads(metrics_path.read_text(encoding="utf-8"))
    rmse = payload.get("rmse_deg")
    if rmse is None:
        return None
    return float(rmse), payload


def write_phase7c_comparison_markdown(repo_root: Path, results_root: Path):
    comparisons = [
        {
            "label": "SS(3/3)",
            "fusion_type": "none",
            "reference_metrics": repo_root
            / "results"
            / "phase7b_groupb_1p9_learned_ss_fusion_phase1p1"
            / "phase7b_gb19_coh_g1_s1_ss33_subspacenet_phase1p1"
            / "esprit"
            / "metrics.json",
            "candidate_metrics": results_root
            / "phase7c_gb19_coh_g1_s1_ss33_backbone3x3"
            / "esprit"
            / "metrics.json",
        },
        {
            "label": "SS(2/3: rows 0+1)",
            "fusion_type": "none",
            "reference_metrics": repo_root
            / "results"
            / "phase7b_groupb_1p9_learned_ss_fusion_phase1p1"
            / "phase7b_gb19_coh_g1_s1_ss23_r01_subspacenet_phase1p1"
            / "esprit"
            / "metrics.json",
            "candidate_metrics": results_root
            / "phase7c_gb19_coh_g1_s1_ss23_r01_backbone3x3"
            / "esprit"
            / "metrics.json",
        },
        {
            "label": "SS(2/3 x 3) learned fusion",
            "fusion_type": "spatial 3x3 fusion",
            "reference_metrics": repo_root
            / "results"
            / "phase7b_groupb_1p9_learned_ss_fusion_phase1p1"
            / "phase7b_gb19_coh_g1_s1_ssfusion_subspacenet_phase1p1"
            / "esprit"
            / "metrics.json",
            "candidate_metrics": results_root
            / "phase7c_gb19_coh_g1_s1_ssfusion_spatial_backbone3x3"
            / "esprit"
            / "metrics.json",
        },
        {
            "label": "SS(2/3 x 3) 1x1 learned fusion",
            "fusion_type": "1x1 channel-only fusion",
            "reference_metrics": repo_root
            / "results"
            / "phase7b_groupb_1p9_learned_ss_fusion_phase1p1p1"
            / "phase7b_gb19_coh_g1_s1_ssfusion_1x1_subspacenet_phase1p1p1"
            / "esprit"
            / "metrics.json",
            "candidate_metrics": results_root
            / "phase7c_gb19_coh_g1_s1_ssfusion_1x1_backbone3x3"
            / "esprit"
            / "metrics.json",
        },
    ]

    lines = [
        "# Phase 7C - Group B 1.9 Lambda SubspaceNet Backbone 3x3",
        "",
        "Phase 7C runs the new `3x3` SubspaceNet-backbone variants only and compares them against the already completed `2x2` backbone references from Phase 7B in the same coherent hard cell.",
        "",
        "Experimental conditions:",
        "- Array: Group B 12-channel 2D hardware geometry",
        "- Physical spacing: 1.9 lambda",
        "- Signals: 2 coherent narrowband targets",
        "- Cell: gap = 1 deg, SNR = 1 dB, T = 40",
        "- Azimuth and elevation range: [-15 deg, 15 deg]",
        "- Training scale: 45,000 samples total with 9,000 test samples",
        "- Learned head: ESPRIT",
        "- Controlled variable: SubspaceNet backbone kernel size 2x2 vs 3x3",
        "",
        "## New 3x3 Runs",
        "",
        "| Scheme | Fusion Type | Backbone | RMSE (deg) |",
        "| --- | --- | --- | ---: |",
    ]

    summary_rows = []
    for item in comparisons:
        candidate = _read_rmse(item["candidate_metrics"])
        candidate_rmse = candidate[0] if candidate else None
        lines.append(
            f"| {item['label']} | {item['fusion_type']} | 3x3 | "
            f"{candidate_rmse:.4f} |" if candidate_rmse is not None else
            f"| {item['label']} | {item['fusion_type']} | 3x3 | missing |"
        )
        if candidate_rmse is not None:
            summary_rows.append(
                {
                    "scheme": item["label"],
                    "fusion_type": item["fusion_type"],
                    "backbone_kernel": 3,
                    "rmse_deg": candidate_rmse,
                }
            )

    lines.extend(
        [
            "",
            "## Direct Comparison Against 2x2 References",
            "",
            "| Scheme | Fusion Type | 2x2 RMSE (deg) | 3x3 RMSE (deg) | Delta (3x3 - 2x2) |",
            "| --- | --- | ---: | ---: | ---: |",
        ]
    )

    for item in comparisons:
        reference = _read_rmse(item["reference_metrics"])
        candidate = _read_rmse(item["candidate_metrics"])
        reference_rmse = reference[0] if reference else None
        candidate_rmse = candidate[0] if candidate else None
        if reference_rmse is None or candidate_rmse is None:
            reference_text = f"{reference_rmse:.4f}" if reference_rmse is not None else "missing"
            candidate_text = f"{candidate_rmse:.4f}" if candidate_rmse is not None else "missing"
            lines.append(
                f"| {item['label']} | {item['fusion_type']} | {reference_text} | {candidate_text} | missing |"
            )
            continue
        delta = candidate_rmse - reference_rmse
        lines.append(
            f"| {item['label']} | {item['fusion_type']} | {reference_rmse:.4f} | {candidate_rmse:.4f} | {delta:+.4f} |"
        )

    (results_root / "phase7c_groupb_1p9_subspacenet_backbone_3x3_results.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    if summary_rows:
        with (results_root / "phase7c_groupb_1p9_subspacenet_backbone_3x3_comparison.csv").open(
            "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=["scheme", "fusion_type", "backbone_kernel", "rmse_deg"],
            )
            writer.writeheader()
            for row in summary_rows:
                writer.writerow(row)


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    templates_dir = (repo_root / args.templates_dir).resolve()
    results_root = (repo_root / args.results_dir).resolve()
    ensure_phase7c_templates(repo_root, templates_dir)

    command = [
        sys.executable,
        str(repo_root / "run_ablation.py"),
        "--templates-dir",
        str(Path(args.templates_dir).as_posix()),
        "--experiments",
        ",".join(PHASE7C_EXPERIMENTS),
        "--seed",
        str(args.seed),
        "--results-dir",
        args.results_dir,
    ]
    print(
        "Phase 7C experiment: Group B 1.9 lambda 3x3 SubspaceNet backbone "
        "primary coherent hard-cell family"
    )
    print("Results will be written under:", args.results_dir)
    print("Command:", " ".join(command))
    subprocess.run(command, check=True)
    write_phase7c_comparison_markdown(repo_root, results_root)


if __name__ == "__main__":
    main()
