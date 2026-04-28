"""Launch Phase 7I Group B 1.9 lambda random-gap training study."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


PHASE7I_TEST_EXPERIMENTS = [
    "phase7i_groupb_1p9_random_gap_training_eval",
]
GAPS = [1, 2, 3, 4, 5]
SNRS = [1, 5, 10, 15]
RANDOM_GAP_SNRS = [1, 5, 10, 15]
PHASE7I_STAGE_COUNT = 3
PHASE7I_STAGE_SAMPLES = 45000
PHASE7I_STAGE_TEST_RATIO = 0.2
PHASE7I_STAGE_EPOCHS = 10


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Run the Phase 7I Group B 1.9 lambda random-gap training study."
        )
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase7i_groupb_1p9_random_gap_training",
        help="Dedicated output directory for the Phase 7I study.",
    )
    parser.add_argument(
        "--train-templates-dir",
        default="data/dataset_templates/ablation/phase7i_groupb_1p9_random_gap_training",
        help="Generated training-template directory for the Phase 7I study.",
    )
    parser.add_argument(
        "--test-templates-dir",
        default="data/dataset_templates/test/phase7i_groupb_1p9_random_gap_training",
        help="Generated test-template directory for the Phase 7I study.",
    )
    parser.add_argument(
        "--randomgap-support-dir",
        default="data/dataset_templates/ablation/phase7i_groupb_1p9_random_gap_training_support",
        help="Generated support-template directory for the Phase 7I random-gap evaluation datasets.",
    )
    return parser.parse_args()


def load_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


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


def get_stage_experiment_name(stage_index: int):
    return f"phase7i_gb19_randomgap_stage{stage_index:02d}_45k"


def get_final_stage_experiment_name():
    return get_stage_experiment_name(PHASE7I_STAGE_COUNT)


def structured_stage_mix(stage_index: int):
    if stage_index == 1:
        return 31500, 13500
    if stage_index == 2:
        return 24800, 20200
    return 18000, 27000


def coherent_structured_cell_count(stage_index: int, gap: int):
    stage_counts = {
        1: {1: 1180, 2: 1890, 3: 945, 4: 473, 5: 237},
        2: {1: 930, 2: 1488, 3: 744, 4: 372, 5: 186},
        3: {1: 675, 2: 1080, 3: 540, 4: 270, 5: 135},
    }
    return stage_counts[stage_index][gap]


def noncoherent_structured_cell_count(stage_index: int, gap: int):
    stage_counts = {
        1: {1: 945, 2: 945, 3: 630, 4: 315, 5: 315},
        2: {1: 744, 2: 744, 3: 496, 4: 248, 5: 248},
        3: {1: 540, 2: 540, 3: 360, 4: 180, 5: 180},
    }
    return stage_counts[stage_index][gap]


def phase7h_compatible_template_name(coherence_key: str, snr: int):
    prefix = "coh" if coherence_key == "coherent" else "noncoh"
    return f"phase7h_gb19_{prefix}_randomgap_s{snr}"


def ensure_phase7i_randomgap_support_templates(
    repo_root: Path, support_dir: Path, seed: int
):
    support_dir.mkdir(parents=True, exist_ok=True)
    generated_paths = {}
    for coherence_key in ["coherent", "noncoherent"]:
        for snr in RANDOM_GAP_SNRS:
            source_template = load_json(
                phase6_template_path(repo_root, coherence_key, 1, snr)
            )
            template = json.loads(json.dumps(source_template))
            template_name = phase7h_compatible_template_name(coherence_key, snr)
            template["template_name"] = template_name
            template["description"] = (
                "Phase 7I random-gap support template reusing the Phase 7H random-gap "
                f"dataset definition for {coherence_key} at SNR={snr} dB."
            )
            template["scenario_data_path"] = (
                f"p7h_{'c' if coherence_key == 'coherent' else 'n'}_rg_s{snr}"
            )
            template["seed"] = seed
            system_model = template["system_model"]
            system_model["snr"] = snr
            system_model["signal_nature"] = (
                "coherent" if coherence_key == "coherent" else "non-coherent"
            )
            system_model["doa_min"] = -15
            system_model["doa_max"] = 15
            system_model["min_doa_gap"] = 1
            if "fixed_doa_gap" in system_model:
                del system_model["fixed_doa_gap"]
            template["dataset"]["samples_size"] = 45000
            template["dataset"]["train_test_ratio"] = 0.2
            target_path = support_dir / f"{template_name}.json"
            with target_path.open("w", encoding="utf-8") as handle:
                json.dump(template, handle, indent=2)
                handle.write("\n")
            generated_paths[(coherence_key, snr)] = target_path
    return generated_paths


def ensure_phase7i_training_templates(
    repo_root: Path, generated_templates_dir: Path, seed: int
):
    generated_templates_dir.mkdir(parents=True, exist_ok=True)
    source_template = load_json(
        repo_root
        / "results"
        / "phase7g_groupb_1p9_boundary_2deg_repair"
        / "phase7g_gb19_boundary2deg_repair_stage08_45k"
        / "resolved_template.json"
    )

    stage_experiments = []
    for stage_index in range(1, PHASE7I_STAGE_COUNT + 1):
        stage_name = get_stage_experiment_name(stage_index)
        stage_experiments.append(stage_name)
        structured_total, random_total = structured_stage_mix(stage_index)
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
                        "total_samples": coherent_structured_cell_count(
                            stage_index, gap
                        ),
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
                        "total_samples": noncoherent_structured_cell_count(
                            stage_index, gap
                        ),
                    }
                )

        template = json.loads(json.dumps(source_template))
        template["template_name"] = stage_name
        template["description"] = (
            "Phase 7I Group B 1.9 lambda staged random-gap training run "
            f"{stage_index}/{PHASE7I_STAGE_COUNT} using a structured-plus-random curriculum."
        )
        template["scenario_data_path"] = f"p7i_rg_s{stage_index:02d}_45k"
        template["methods"] = ["esprit"]
        template["seed"] = seed + stage_index - 1

        template["commands"]["CREATE_DATA"] = True
        template["commands"]["CACHE_DATASET"] = True
        template["commands"]["LOAD_DATA"] = False
        template["commands"]["TRAIN_MODEL"] = True
        template["commands"]["EVALUATE_MODE"] = True

        template["dataset"] = {
            "samples_size": PHASE7I_STAGE_SAMPLES,
            "train_test_ratio": PHASE7I_STAGE_TEST_RATIO,
            "mixed_dataset": {
                "stratified_cells": stratified_cells,
                "weighted_random": {
                    "total_samples": random_total,
                    "coherence_weights": {"coherent": 0.6, "noncoherent": 0.4},
                    "snr_weights": {"1": 0.35, "5": 0.30, "10": 0.20, "15": 0.15},
                    "coherent_gap_group_weights": [
                        {"gaps": [1.0, 2.0], "weight": 0.35},
                        {"gaps": [2.0, 3.0], "weight": 0.25},
                        {"gaps": [3.0, 5.0], "weight": 0.20},
                        {"gaps": [5.0, 10.0], "weight": 0.10},
                        {"gaps": [10.0, 29.0], "weight": 0.10},
                    ],
                    "noncoherent_gap_group_weights": [
                        {"gaps": [1.0, 2.0], "weight": 0.30},
                        {"gaps": [2.0, 3.0], "weight": 0.25},
                        {"gaps": [3.0, 5.0], "weight": 0.20},
                        {"gaps": [5.0, 10.0], "weight": 0.15},
                        {"gaps": [10.0, 29.0], "weight": 0.10},
                    ],
                    "gap_group_weights": [
                        {"gaps": [1.0, 2.0], "weight": 0.33},
                        {"gaps": [2.0, 3.0], "weight": 0.25},
                        {"gaps": [3.0, 5.0], "weight": 0.20},
                        {"gaps": [5.0, 10.0], "weight": 0.12},
                        {"gaps": [10.0, 29.0], "weight": 0.10},
                    ],
                },
            },
        }

        training = template["training"]
        training["epochs"] = PHASE7I_STAGE_EPOCHS
        training["learning_rate"] = 3e-6
        training["scheduler_step_size"] = 6
        training["scheduler_gamma"] = 0.5
        if stage_index == 1:
            training["pretrained_experiment_dir"] = (
                "results/phase7g_groupb_1p9_boundary_2deg_repair/"
                "phase7g_gb19_boundary2deg_repair_stage08_45k"
            )
        else:
            training["pretrained_experiment_dir"] = (
                "results/phase7i_groupb_1p9_random_gap_training/"
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


def classify_fixed_split(coherence_key: str, gap: int, snr: int):
    if coherence_key == "coherent" and gap == 1 and snr == 1:
        return "in_domain_anchor"
    if coherence_key == "coherent":
        return "coherent_ood"
    return "noncoherent_transfer"


def ensure_phase7i_test_templates(
    repo_root: Path,
    generated_templates_dir: Path,
    randomgap_support_templates: dict,
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
                    or (coherence_key == "coherent" and gap == 2)
                    or (coherence_key == "coherent" and gap == 3 and snr == 5)
                    or (coherence_key == "noncoherent" and gap == 1 and snr == 1)
                    or (coherence_key == "noncoherent" and gap == 2 and snr == 5)
                )
                bucket_labels = [classify_fixed_split(coherence_key, gap, snr)]
                if coherence_key == "coherent" and gap == 2:
                    bucket_labels.append("coherent_2deg_boundary")
                evaluation_cells.append(
                    {
                        "template_path": str(
                            phase6_template_path(repo_root, coherence_key, gap, snr)
                        ),
                        "result_name": (
                            f"phase7i_gb19_{'coh' if coherence_key == 'coherent' else 'noncoh'}"
                            f"_g{gap}_s{snr}_randomgapft"
                        ),
                        "method_name": "esprit",
                        "coherence_key": coherence_key,
                        "coherence_label": coherence_label,
                        "gap_deg": gap,
                        "snr_db": snr,
                        "split": classify_fixed_split(coherence_key, gap, snr),
                        "bucket_labels": bucket_labels,
                        "retention_priority": retention_priority,
                        "reference_schemes": {
                            "phase7e": (
                                f"phase7e_gb19_{'coh' if coherence_key == 'coherent' else 'noncoh'}"
                                f"_g{gap}_s{snr}_antirect_transfer"
                            ),
                            "phase7f": (
                                f"phase7f_gb19_{'coh' if coherence_key == 'coherent' else 'noncoh'}"
                                f"_g{gap}_s{snr}_mixedft"
                            ),
                            "phase7g": (
                                f"phase7g_gb19_{'coh' if coherence_key == 'coherent' else 'noncoh'}"
                                f"_g{gap}_s{snr}_boundary2deg"
                            ),
                        },
                    }
                )

    for coherence_key, coherence_label in [
        ("coherent", "coherent"),
        ("noncoherent", "non-coherent"),
    ]:
        for snr in RANDOM_GAP_SNRS:
            evaluation_cells.append(
                {
                    "template_path": str(randomgap_support_templates[(coherence_key, snr)]),
                    "result_name": (
                        f"phase7i_gb19_{'coh' if coherence_key == 'coherent' else 'noncoh'}_randomgap_s{snr}"
                    ),
                    "method_name": "esprit",
                    "coherence_key": coherence_key,
                    "coherence_label": coherence_label,
                    "gap_deg": None,
                    "snr_db": snr,
                    "split": (
                        "coherent_random_gap"
                        if coherence_key == "coherent"
                        else "noncoherent_random_gap"
                    ),
                    "bucket_labels": [
                        (
                            "coherent_random_gap"
                            if coherence_key == "coherent"
                            else "noncoherent_random_gap"
                        )
                    ],
                    "retention_priority": False,
                    "reference_schemes": {
                        "phase7h": (
                            f"phase7h_gb19_{'coh' if coherence_key == 'coherent' else 'noncoh'}_randomgap_s{snr}"
                        )
                    },
                }
            )

    template = {
        "description": (
            "Phase 7I evaluates the random-gap-adapted model on both the reused fixed-gap "
            "40-cell grid and the Phase 7H-compatible 8-cell random-gap family."
        ),
        "experiment_type": "subspacenet_transfer_test",
        "seed": seed,
        "commands": {
            "GENERATE_MISSING_DATA": True,
            "SAVE_GENERATED_DATA": True,
        },
        "source_model": {
            "experiment_dir": (
                "results/phase7i_groupb_1p9_random_gap_training/"
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
            "phase7f_summary_csv": str(
                repo_root
                / "results"
                / "phase7f_groupb_1p9_mixed_condition_finetune"
                / "summary.csv"
            ),
            "phase7g_summary_csv": str(
                repo_root
                / "results"
                / "phase7g_groupb_1p9_boundary_2deg_repair"
                / "summary.csv"
            ),
            "phase7h_summary_csv": str(
                repo_root
                / "results"
                / "phase7h_groupb_1p9_random_gap_generalization"
                / "summary.csv"
            ),
        },
        "report": {
            "flat_results_root": True,
            "write_summary_csv": True,
            "markdown_output": "phase7i_groupb_1p9_random_gap_training_results.md",
            "markdown_title": (
                "Phase 7I - Group B 1.9 Lambda Random-Gap Training"
            ),
            "markdown_description": (
                "Phase 7I fine-tunes the Phase 7G boundary-repair model with a staged "
                "structured-plus-random-gap curriculum, then evaluates both fixed-gap "
                "retention and random-gap generalization in one combined results family."
            ),
            "markdown_conditions": [
                "Array: Group B 12-channel 2D hardware geometry",
                "Physical spacing: 1.9 lambda",
                "Model family: SS(2/3 x 3) -> LRMC -> width-controlled anti-rectifier spatial fusion -> SubspaceNet backbone 3x3 -> ESPRIT",
                "Initialization: fine-tune from the best Phase 7G checkpoint",
                "Training schedule: 3 sequential stages x 45,000 samples",
                "Per-stage split: 36,000 train / 9,000 held-out",
                "Structured/random stage mix: 31.5k/13.5k -> 24.8k/20.2k -> 18k/27k",
                "Random-gap rule: low-gap-biased continuous sampling with min_doa_gap = 1 deg",
                "Evaluation set: 40 fixed-gap cells plus 8 random-gap cells",
                "Primary metrics: fixed-gap retention and random-gap RMSE",
            ],
            "hybrid_random_gap_mode": True,
        },
        "template_name": PHASE7I_TEST_EXPERIMENTS[0],
    }

    target_path = generated_templates_dir / f"{PHASE7I_TEST_EXPERIMENTS[0]}.json"
    with target_path.open("w", encoding="utf-8") as handle:
        json.dump(template, handle, indent=2)
        handle.write("\n")


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    train_templates_dir = (repo_root / args.train_templates_dir).resolve()
    test_templates_dir = (repo_root / args.test_templates_dir).resolve()
    randomgap_support_dir = (repo_root / args.randomgap_support_dir).resolve()

    stage_experiments = ensure_phase7i_training_templates(
        repo_root, train_templates_dir, args.seed
    )
    randomgap_support_templates = ensure_phase7i_randomgap_support_templates(
        repo_root, randomgap_support_dir, args.seed
    )
    ensure_phase7i_test_templates(
        repo_root,
        test_templates_dir,
        randomgap_support_templates,
        args.seed,
    )

    print("Phase 7I experiment: Group B 1.9 lambda random-gap training")
    print("Results will be written under:", args.results_dir)
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
            f"Training stage {stage_index}/{PHASE7I_STAGE_COUNT}:",
            " ".join(train_command),
        )
        subprocess.run(train_command, check=True)

    test_command = [
        sys.executable,
        str(repo_root / "run_test.py"),
        "--templates-dir",
        str(Path(args.test_templates_dir).as_posix()),
        "--experiments",
        ",".join(PHASE7I_TEST_EXPERIMENTS),
        "--seed",
        str(args.seed),
        "--results-dir",
        args.results_dir,
    ]
    print("Evaluation command:", " ".join(test_command))
    subprocess.run(test_command, check=True)


if __name__ == "__main__":
    main()
