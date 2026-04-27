"""Launch Phase 7F Group B 1.9 lambda mixed-condition fine-tuning study."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


PHASE7F_TEST_EXPERIMENTS = [
    "phase7f_groupb_1p9_mixed_condition_finetune_eval",
]

GAPS = [1, 2, 3, 4, 5]
SNRS = [1, 5, 10, 15]
PHASE7F_STAGE_COUNT = 8
PHASE7F_STAGE_SAMPLES = 45000
PHASE7F_STAGE_TRAINING_SAMPLES = 40500
PHASE7F_STAGE_TEST_SAMPLES = 4500
PHASE7F_STRATIFIED_SAMPLES = 30000
PHASE7F_WEIGHTED_RANDOM_SAMPLES = 15000
PHASE7F_COHERENT_CELL_SAMPLES = 900
PHASE7F_NONCOHERENT_CELL_SAMPLES = 600
PHASE7F_STAGE_EPOCHS = 6
PHASE7F_STAGE_TEST_RATIO = 0.1


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Run the Phase 7F Group B 1.9 lambda mixed-condition fine-tuning study."
        )
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase7f_groupb_1p9_mixed_condition_finetune",
        help="Dedicated output directory for the Phase 7F study.",
    )
    parser.add_argument(
        "--train-templates-dir",
        default="data/dataset_templates/ablation/phase7f_groupb_1p9_mixed_condition_finetune",
        help="Generated training-template directory for the Phase 7F study.",
    )
    parser.add_argument(
        "--test-templates-dir",
        default="data/dataset_templates/test/phase7f_groupb_1p9_mixed_condition_finetune",
        help="Generated test-template directory for the Phase 7F study.",
    )
    return parser.parse_args()


def classify_split(coherence_key: str, gap: int, snr: int):
    if coherence_key == "coherent" and gap == 1 and snr == 1:
        return "in_domain_anchor"
    if coherence_key == "coherent":
        return "coherent_ood"
    return "noncoherent_transfer"


def classify_buckets(coherence_key: str, gap: int, snr: int):
    buckets = [classify_split(coherence_key, gap, snr)]
    if coherence_key == "coherent":
        if gap == 1 and snr in {5, 10, 15}:
            buckets.append("snr_shift_only")
        if snr == 1 and gap in {2, 3, 4, 5}:
            buckets.append("gap_shift_only")
    else:
        if gap == 1 and snr in {1, 5, 10, 15}:
            buckets.append("snr_shift_only")
        if snr == 1 and gap in {1, 2, 3, 4, 5}:
            buckets.append("gap_shift_only")
        buckets.append("full_noncoherent_transfer")
    if gap in {2, 3, 4, 5} and snr in {5, 10, 15}:
        buckets.append("joint_gap_snr_shift")
    return buckets


def phase6_template_path(repo_root: Path, coherence_key: str, gap: int, snr: int):
    family = (
        "phase6_groupb_1p9_coherent_fixed_gap_snr_grid"
        if coherence_key == "coherent"
        else "phase6_groupb_1p9_noncoherent_fixed_gap_snr_grid"
    )
    filename = (
        f"phase6_groupb_1p9_{coherence_key}_subspacenet_esprit_gap{gap}_snr{snr}.json"
    )
    return (
        repo_root
        / "data"
        / "dataset_templates"
        / "ablation"
        / family
        / filename
    )


def load_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def get_stage_experiment_name(stage_index: int):
    return f"phase7f_gb19_mixed_antirect_finetune_stage{stage_index:02d}_45k"


def get_final_stage_experiment_name():
    return get_stage_experiment_name(PHASE7F_STAGE_COUNT)


def ensure_phase7f_training_templates(
    repo_root: Path, generated_templates_dir: Path, seed: int
):
    generated_templates_dir.mkdir(parents=True, exist_ok=True)
    source_template = load_json(
        repo_root
        / "results"
        / "phase7d_groupb_1p9_ssfusion_activation_ablation"
        / "phase7d_gb19_coh_g1_s1_ssfusion_antirect_backbone3x3"
        / "resolved_template.json"
    )

    stratified_cells = []
    for gap in GAPS:
        for snr in SNRS:
            stratified_cells.append(
                {
                    "template_path": str(
                        phase6_template_path(repo_root, "coherent", gap, snr)
                    ),
                    "coherence_key": "coherent",
                    "gap_deg": gap,
                    "snr_db": snr,
                    "total_samples": 7200,
                }
            )
            stratified_cells.append(
                {
                    "template_path": str(
                        phase6_template_path(repo_root, "noncoherent", gap, snr)
                    ),
                    "coherence_key": "noncoherent",
                    "gap_deg": gap,
                    "snr_db": snr,
                    "total_samples": 4800,
                }
            )

    stage_experiments = []
    for stage_index in range(1, PHASE7F_STAGE_COUNT + 1):
        stage_name = get_stage_experiment_name(stage_index)
        stage_experiments.append(stage_name)
        template = json.loads(json.dumps(source_template))
        template["template_name"] = stage_name
        template["description"] = (
            "Phase 7F Group B 1.9 lambda staged mixed-condition fine-tuning run "
            f"{stage_index}/{PHASE7F_STAGE_COUNT} using a 45k mixed dataset chunk."
        )
        template["scenario_data_path"] = f"p7f_mixft_s{stage_index:02d}_45k"
        template["methods"] = ["esprit"]
        template["seed"] = seed + stage_index - 1

        template["commands"]["CREATE_DATA"] = True
        template["commands"]["CACHE_DATASET"] = True
        template["commands"]["LOAD_DATA"] = False
        template["commands"]["TRAIN_MODEL"] = True
        template["commands"]["EVALUATE_MODE"] = True

        template["dataset"] = {
            "samples_size": PHASE7F_STAGE_SAMPLES,
            "train_test_ratio": PHASE7F_STAGE_TEST_RATIO,
            "mixed_dataset": {
                "stratified_cells": [
                    {
                        **cell,
                        "total_samples": (
                            PHASE7F_COHERENT_CELL_SAMPLES
                            if cell["coherence_key"] == "coherent"
                            else PHASE7F_NONCOHERENT_CELL_SAMPLES
                        ),
                    }
                    for cell in stratified_cells
                ],
                "weighted_random": {
                    "total_samples": PHASE7F_WEIGHTED_RANDOM_SAMPLES,
                    "coherence_weights": {"coherent": 0.6, "noncoherent": 0.4},
                    "snr_weights": {"1": 0.35, "5": 0.30, "10": 0.20, "15": 0.15},
                    "gap_group_weights": [
                        {"gaps": [1.0, 2.0], "weight": 0.50},
                        {"gaps": [3.0], "weight": 0.30},
                        {"gaps": [4.0, 5.0], "weight": 0.20},
                    ],
                },
            },
        }

        training = template["training"]
        training["epochs"] = PHASE7F_STAGE_EPOCHS
        training["learning_rate"] = 5e-6
        training["scheduler_step_size"] = 4
        training["scheduler_gamma"] = 0.5
        if stage_index == 1:
            training["pretrained_experiment_dir"] = (
                "results/phase7d_groupb_1p9_ssfusion_activation_ablation/"
                "phase7d_gb19_coh_g1_s1_ssfusion_antirect_backbone3x3"
            )
        else:
            training["pretrained_experiment_dir"] = (
                "results/phase7f_groupb_1p9_mixed_condition_finetune/"
                f"{get_stage_experiment_name(stage_index - 1)}"
            )
        training["pretrained_method_name"] = "esprit"

        report = template["report"]
        report["write_summary_csv"] = False
        report["markdown_output"] = ""

        target_path = generated_templates_dir / f"{stage_name}.json"
        with target_path.open("w", encoding="utf-8") as handle:
            json.dump(template, handle, indent=2)
            handle.write("\n")
    return stage_experiments


def ensure_phase7f_test_templates(
    repo_root: Path,
    generated_templates_dir: Path,
    seed: int,
):
    generated_templates_dir.mkdir(parents=True, exist_ok=True)
    phase7d_metrics = load_json(
        repo_root
        / "results"
        / "phase7d_groupb_1p9_ssfusion_activation_ablation"
        / "phase7d_gb19_coh_g1_s1_ssfusion_antirect_backbone3x3"
        / "esprit"
        / "metrics.json"
    )

    evaluation_cells = []
    for coherence_key, coherence_label in [
        ("coherent", "coherent"),
        ("noncoherent", "non-coherent"),
    ]:
        for gap in GAPS:
            for snr in SNRS:
                retention_priority = (
                    (coherence_key == "coherent" and gap == 1 and snr == 1)
                    or (coherence_key == "coherent" and gap == 2 and snr in {1, 5})
                    or (coherence_key == "noncoherent" and gap == 1 and snr == 1)
                )
                evaluation_cells.append(
                    {
                        "template_path": str(
                            phase6_template_path(repo_root, coherence_key, gap, snr)
                        ),
                        "result_name": (
                            f"phase7f_gb19_{'coh' if coherence_key == 'coherent' else 'noncoh'}"
                            f"_g{gap}_s{snr}_mixedft"
                        ),
                        "method_name": "esprit",
                        "coherence_key": coherence_key,
                        "coherence_label": coherence_label,
                        "gap_deg": gap,
                        "snr_db": snr,
                        "split": classify_split(coherence_key, gap, snr),
                        "bucket_labels": classify_buckets(coherence_key, gap, snr),
                        "retention_priority": retention_priority,
                        "reference_schemes": {
                            "phase7e": (
                                f"phase7e_gb19_{'coh' if coherence_key == 'coherent' else 'noncoh'}"
                                f"_g{gap}_s{snr}_antirect_transfer"
                            )
                        },
                    }
                )

    template = {
        "description": (
            "Phase 7F evaluates the mixed-condition fine-tuned anti-rectifier fusion "
            "model on the same reused Phase 7E 40-cell grid."
        ),
        "experiment_type": "subspacenet_transfer_test",
        "seed": seed,
        "commands": {
            "GENERATE_MISSING_DATA": True,
            "SAVE_GENERATED_DATA": True,
        },
        "source_model": {
            "experiment_dir": (
                "results/phase7f_groupb_1p9_mixed_condition_finetune/"
                f"{get_final_stage_experiment_name()}"
            ),
            "method_name": "esprit",
            "reference_rmse_deg": float(phase7d_metrics["rmse_deg"]),
        },
        "evaluation_cells": evaluation_cells,
        "reference_sources": {
            "coherent_summary_csv": str(
                repo_root
                / "results"
                / "phase6_groupb_1p9_coherent_fixed_gap_snr_grid"
                / "summary.csv"
            ),
            "noncoherent_summary_csv": str(
                repo_root
                / "results"
                / "phase6_groupb_1p9_noncoherent_fixed_gap_snr_grid"
                / "summary.csv"
            ),
            "phase7e_summary_csv": str(
                repo_root
                / "results"
                / "phase7e_groupb_1p9_antirect_fusion_generalization"
                / "summary.csv"
            ),
        },
        "report": {
            "flat_results_root": True,
            "write_summary_csv": True,
            "markdown_output": "phase7f_groupb_1p9_mixed_condition_finetune_results.md",
            "markdown_title": (
                "Phase 7F - Group B 1.9 Lambda Mixed-Condition Fine-Tuning"
            ),
            "markdown_description": (
                "Phase 7F fine-tunes the Phase 7D anti-rectifier fusion checkpoint on a "
                "360k mixed-condition dataset and evaluates it on the reused Phase 7E "
                "coherent and non-coherent fixed-gap / SNR grids."
            ),
            "markdown_conditions": [
                "Array: Group B 12-channel 2D hardware geometry",
                "Physical spacing: 1.9 lambda",
                "Model family: SS(2/3 x 3) -> LRMC -> width-controlled anti-rectifier spatial fusion -> SubspaceNet backbone 3x3 -> ESPRIT",
                "Initialization: fine-tune from the best Phase 7D checkpoint",
                "Training schedule: 8 sequential fine-tuning stages",
                "Per-stage mixed dataset size: 45,000 total samples",
                "Per-stage split: 40,500 training / 4,500 test samples",
                "Approximate total samples seen across stages: 360,000",
                "Coherence weighting: 60% coherent, 40% non-coherent",
                "Evaluation set: same reused 40-cell grid as Phase 7E",
                "Primary metric: horizontal-angle RMSE in degrees",
                "Comparison focus: source-cell retention and delta vs Phase 7E",
            ],
        },
        "template_name": PHASE7F_TEST_EXPERIMENTS[0],
    }

    target_path = generated_templates_dir / f"{PHASE7F_TEST_EXPERIMENTS[0]}.json"
    with target_path.open("w", encoding="utf-8") as handle:
        json.dump(template, handle, indent=2)
        handle.write("\n")


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    train_templates_dir = (repo_root / args.train_templates_dir).resolve()
    test_templates_dir = (repo_root / args.test_templates_dir).resolve()

    stage_experiments = ensure_phase7f_training_templates(
        repo_root, train_templates_dir, args.seed
    )
    ensure_phase7f_test_templates(repo_root, test_templates_dir, args.seed)
    test_command = [
        sys.executable,
        str(repo_root / "run_test.py"),
        "--templates-dir",
        str(Path(args.test_templates_dir).as_posix()),
        "--experiments",
        ",".join(PHASE7F_TEST_EXPERIMENTS),
        "--seed",
        str(args.seed),
        "--results-dir",
        args.results_dir,
    ]

    print(
        "Phase 7F experiment: Group B 1.9 lambda mixed-condition fine-tuning "
        "followed by reused-grid evaluation"
    )
    print("Results will be written under:", args.results_dir)
    print(
        "Staged training schedule:",
        f"{PHASE7F_STAGE_COUNT} stages x {PHASE7F_STAGE_SAMPLES:,} samples",
    )
    for stage_index, experiment_name in enumerate(stage_experiments, start=1):
        train_command = [
            sys.executable,
            str(repo_root / "run_ablation.py"),
            "--templates-dir",
            str(Path(args.train_templates_dir).as_posix()),
            "--experiments",
            experiment_name,
            "--seed",
            str(args.seed + stage_index - 1),
            "--results-dir",
            args.results_dir,
        ]
        print(
            f"Training stage {stage_index}/{PHASE7F_STAGE_COUNT}:",
            " ".join(train_command),
        )
        subprocess.run(train_command, check=True)
    print("Evaluation command:", " ".join(test_command))
    subprocess.run(test_command, check=True)


if __name__ == "__main__":
    main()
