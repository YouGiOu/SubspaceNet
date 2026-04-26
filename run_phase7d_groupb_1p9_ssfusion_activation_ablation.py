"""Launch Phase 7D Group B 1.9 lambda SS-fusion activation ablation."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path


PHASE7D_EXPERIMENTS = [
    "phase7d_gb19_coh_g1_s1_ssfusion_antirect_backbone3x3",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Run the Phase 7D Group B 1.9 lambda SS-fusion activation ablation "
            "for the primary coherent hard cell."
        )
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase7d_groupb_1p9_ssfusion_activation_ablation",
        help="Dedicated output directory for the Phase 7D study.",
    )
    parser.add_argument(
        "--templates-dir",
        default="data/dataset_templates/ablation/phase7d_groupb_1p9_ssfusion_activation_ablation",
        help="Generated template directory for the Phase 7D study.",
    )
    return parser.parse_args()


def ensure_phase7d_templates(repo_root: Path, generated_templates_dir: Path):
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

    template = json.loads(json.dumps(source_template))
    template["template_name"] = PHASE7D_EXPERIMENTS[0]
    template["description"] = (
        "Phase 7D coherent Group B 1.9 lambda learned SS-fusion activation ablation "
        "for gap=1 deg and SNR=1 dB using SS(2/3 x 3) -> LRMC -> width-controlled "
        "anti-rectifier learned fusion -> SubspaceNet backbone 3x3 -> ESPRIT."
    )
    template["scenario_data_path"] = "p7b_p1p1_coh_g1_s1_45k"
    template["methods"] = ["esprit"]
    template["seed"] = 42

    template["commands"]["CREATE_DATA"] = True
    template["commands"]["CACHE_DATASET"] = True
    template["commands"]["LOAD_DATA"] = False
    template["commands"]["TRAIN_MODEL"] = True
    template["commands"]["EVALUATE_MODE"] = True

    system_model = template["system_model"]
    system_model.pop("ss_num_subarrays", None)
    system_model.pop("ss_row_subset", None)
    system_model["subspacenet_backbone_kernel_size"] = 3
    system_model["ss_fusion_branch_subsets"] = [[0, 1], [0, 2], [1, 2]]
    system_model["ss_fusion_hidden_channels"] = 16
    system_model["ss_fusion_diagonal_loading"] = 1e-6

    model = template["model"]
    model["model_type"] = "SubspaceNetSSFusionAntiRectEspritPhase7d"
    model["diff_method"] = "esprit"
    model["tau"] = 8

    report = template["report"]
    report["markdown_output"] = (
        "phase7d_groupb_1p9_ssfusion_activation_ablation_results.md"
    )
    report["markdown_title"] = (
        "Phase 7D - Group B 1.9 Lambda SS-Fusion Activation Ablation"
    )
    report["markdown_description"] = (
        "Phase 7D runs a single controlled activation ablation in the primary coherent "
        "hard cell by replacing the spatial SS-fusion block's ReLU activations with a "
        "width-controlled anti-rectifier while keeping the Phase 7C 3x3 backbone setting."
    )
    report["markdown_conditions"] = [
        "Array: Group B 12-channel 2D hardware geometry",
        "Physical spacing: 1.9 lambda",
        "Signals: 2 coherent narrowband targets",
        "Cell: gap = 1 deg, SNR = 1 dB, T = 40",
        "Azimuth and elevation range: [-15 deg, 15 deg]",
        "Training scale: 45,000 samples total with 9,000 test samples",
        "Learned head: ESPRIT",
        "Controlled variable: fusion-block activation design only",
        "Fusion variant: width-controlled anti-rectifier spatial fusion",
        "Backbone: SubspaceNet 3x3",
        "Metric: horizontal-angle RMSE in degrees (periodic matching)",
    ]
    report["write_summary_csv"] = True
    report["markdown_scheme_label"] = (
        "Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3 x 3) -> LRMC -> anti-rectifier "
        "learned fusion -> SubspaceNet backbone 3x3"
    )

    target_path = generated_templates_dir / f"{template['template_name']}.json"
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


def write_phase7d_comparison_markdown(repo_root: Path, results_root: Path):
    candidate_metrics = (
        results_root
        / "phase7d_gb19_coh_g1_s1_ssfusion_antirect_backbone3x3"
        / "esprit"
        / "metrics.json"
    )
    relu_reference_metrics = (
        repo_root
        / "results"
        / "phase7c_groupb_1p9_subspacenet_backbone_3x3"
        / "phase7c_gb19_coh_g1_s1_ssfusion_spatial_backbone3x3"
        / "esprit"
        / "metrics.json"
    )
    best_baseline_metrics = (
        repo_root
        / "results"
        / "phase7c_groupb_1p9_subspacenet_backbone_3x3"
        / "phase7c_gb19_coh_g1_s1_ss33_backbone3x3"
        / "esprit"
        / "metrics.json"
    )

    candidate = _read_rmse(candidate_metrics)
    relu_reference = _read_rmse(relu_reference_metrics)
    best_baseline = _read_rmse(best_baseline_metrics)

    candidate_rmse = candidate[0] if candidate else None
    relu_reference_rmse = relu_reference[0] if relu_reference else None
    best_baseline_rmse = best_baseline[0] if best_baseline else None

    lines = [
        "# Phase 7D - Group B 1.9 Lambda SS-Fusion Activation Ablation",
        "",
        "Phase 7D runs a single controlled activation ablation in the primary coherent hard cell, replacing the spatial SS-fusion block's `ReLU` activations with a width-controlled anti-rectifier while keeping the `3x3` SubspaceNet backbone fixed.",
        "",
        "Experimental conditions:",
        "- Array: Group B 12-channel 2D hardware geometry",
        "- Physical spacing: 1.9 lambda",
        "- Signals: 2 coherent narrowband targets",
        "- Cell: gap = 1 deg, SNR = 1 dB, T = 40",
        "- Azimuth and elevation range: [-15 deg, 15 deg]",
        "- Training scale: 45,000 samples total with 9,000 test samples",
        "- Learned head: ESPRIT",
        "- Controlled variable: spatial fusion activation design only",
        "",
        "## Results",
        "",
        "| Variant | Backbone | RMSE (deg) | Delta vs ReLU spatial fusion | Delta vs plain SS(3/3) best baseline |",
        "| --- | --- | ---: | ---: | ---: |",
    ]

    candidate_text = f"{candidate_rmse:.4f}" if candidate_rmse is not None else "missing"
    delta_relu_text = "missing"
    delta_best_text = "missing"
    if candidate_rmse is not None and relu_reference_rmse is not None:
        delta_relu_text = f"{candidate_rmse - relu_reference_rmse:+.4f}"
    if candidate_rmse is not None and best_baseline_rmse is not None:
        delta_best_text = f"{candidate_rmse - best_baseline_rmse:+.4f}"
    lines.append(
        "| SS(2/3 x 3) -> LRMC -> anti-rectifier learned fusion | 3x3 | "
        f"{candidate_text} | {delta_relu_text} | {delta_best_text} |"
    )

    lines.extend(
        [
            "",
            "## Reference Values",
            "",
            "| Reference | RMSE (deg) |",
            "| --- | ---: |",
            f"| Phase 7C ReLU spatial fusion 3x3 | {relu_reference_rmse:.4f} |"
            if relu_reference_rmse is not None
            else "| Phase 7C ReLU spatial fusion 3x3 | missing |",
            f"| Phase 7C plain SS(3/3) 3x3 best baseline | {best_baseline_rmse:.4f} |"
            if best_baseline_rmse is not None
            else "| Phase 7C plain SS(3/3) 3x3 best baseline | missing |",
        ]
    )

    (
        results_root / "phase7d_groupb_1p9_ssfusion_activation_ablation_results.md"
    ).write_text("\n".join(lines) + "\n", encoding="utf-8")

    if candidate_rmse is not None:
        with (results_root / "phase7d_groupb_1p9_ssfusion_activation_ablation_comparison.csv").open(
            "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "scheme",
                    "fusion_activation",
                    "backbone_kernel",
                    "rmse_deg",
                    "delta_vs_relu_spatial_3x3",
                    "delta_vs_plain_ss33_3x3",
                ],
            )
            writer.writeheader()
            writer.writerow(
                {
                    "scheme": "SS(2/3 x 3) learned fusion",
                    "fusion_activation": "anti-rectifier width-controlled",
                    "backbone_kernel": 3,
                    "rmse_deg": candidate_rmse,
                    "delta_vs_relu_spatial_3x3": (
                        candidate_rmse - relu_reference_rmse
                        if relu_reference_rmse is not None
                        else ""
                    ),
                    "delta_vs_plain_ss33_3x3": (
                        candidate_rmse - best_baseline_rmse
                        if best_baseline_rmse is not None
                        else ""
                    ),
                }
            )


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    templates_dir = (repo_root / args.templates_dir).resolve()
    results_root = (repo_root / args.results_dir).resolve()
    ensure_phase7d_templates(repo_root, templates_dir)

    command = [
        sys.executable,
        str(repo_root / "run_ablation.py"),
        "--templates-dir",
        str(Path(args.templates_dir).as_posix()),
        "--experiments",
        ",".join(PHASE7D_EXPERIMENTS),
        "--seed",
        str(args.seed),
        "--results-dir",
        args.results_dir,
    ]
    print(
        "Phase 7D experiment: Group B 1.9 lambda SS-fusion activation ablation "
        "for the primary coherent hard cell"
    )
    print("Results will be written under:", args.results_dir)
    print("Command:", " ".join(command))
    subprocess.run(command, check=True)
    write_phase7d_comparison_markdown(repo_root, results_root)


if __name__ == "__main__":
    main()
