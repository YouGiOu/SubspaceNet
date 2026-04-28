"""Launch Phase 7H Group B 1.9 lambda random-gap generalization study."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


PHASE7H_TEST_EXPERIMENTS = [
    "phase7h_groupb_1p9_random_gap_generalization_eval",
]
GAPS = [1, 5, 10, 15]


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Run the Phase 7H Group B 1.9 lambda random-gap generalization study."
        )
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase7h_groupb_1p9_random_gap_generalization",
        help="Dedicated output directory for the Phase 7H study.",
    )
    parser.add_argument(
        "--test-templates-dir",
        default="data/dataset_templates/test/phase7h_groupb_1p9_random_gap_generalization",
        help="Generated test-template directory for the Phase 7H study.",
    )
    parser.add_argument(
        "--support-templates-dir",
        default="data/dataset_templates/ablation/phase7h_groupb_1p9_random_gap_generalization_support",
        help="Generated source-template directory for the Phase 7H random-gap datasets.",
    )
    return parser.parse_args()


def load_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def phase6_template_path(repo_root: Path, coherence_key: str, snr: int):
    family = (
        "phase6_groupb_1p9_coherent_fixed_gap_snr_grid"
        if coherence_key == "coherent"
        else "phase6_groupb_1p9_noncoherent_fixed_gap_snr_grid"
    )
    filename = (
        f"phase6_groupb_1p9_{coherence_key}_subspacenet_esprit_gap1_snr{snr}.json"
    )
    return (
        repo_root
        / "data"
        / "dataset_templates"
        / "ablation"
        / family
        / filename
    )


def support_template_name(coherence_key: str, snr: int):
    prefix = "coh" if coherence_key == "coherent" else "noncoh"
    return f"phase7h_gb19_{prefix}_randomgap_s{snr}"


def ensure_phase7h_support_templates(
    repo_root: Path, support_templates_dir: Path, seed: int
):
    support_templates_dir.mkdir(parents=True, exist_ok=True)
    generated_paths = {}
    for coherence_key in ["coherent", "noncoherent"]:
        for snr in GAPS:
            source_template = load_json(phase6_template_path(repo_root, coherence_key, snr))
            template = json.loads(json.dumps(source_template))
            template_name = support_template_name(coherence_key, snr)
            template["template_name"] = template_name
            template["description"] = (
                "Phase 7H random-gap test source template derived from the Phase 6 "
                f"{coherence_key} Group B 1.9 lambda family at SNR={snr} dB."
            )
            template["scenario_data_path"] = f"p7h_{'c' if coherence_key == 'coherent' else 'n'}_rg_s{snr}"
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
            target_path = support_templates_dir / f"{template_name}.json"
            with target_path.open("w", encoding="utf-8") as handle:
                json.dump(template, handle, indent=2)
                handle.write("\n")
            generated_paths[(coherence_key, snr)] = target_path
    return generated_paths


def ensure_phase7h_test_templates(
    repo_root: Path,
    generated_templates_dir: Path,
    support_template_paths: dict,
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
        for snr in GAPS:
            evaluation_cells.append(
                {
                    "template_path": str(support_template_paths[(coherence_key, snr)]),
                    "result_name": (
                        f"phase7h_gb19_{'coh' if coherence_key == 'coherent' else 'noncoh'}_randomgap_s{snr}"
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
                        "random_gap_generalization",
                        (
                            "coherent_random_gap"
                            if coherence_key == "coherent"
                            else "noncoherent_random_gap"
                        ),
                    ],
                    "retention_priority": False,
                }
            )

    template = {
        "description": (
            "Phase 7H evaluates the Phase 7G boundary-repair model on newly generated "
            "random-gap coherent and non-coherent Group B test datasets."
        ),
        "experiment_type": "subspacenet_transfer_test",
        "seed": seed,
        "commands": {
            "GENERATE_MISSING_DATA": True,
            "SAVE_GENERATED_DATA": True,
        },
        "source_model": {
            "experiment_dir": (
                "results/phase7g_groupb_1p9_boundary_2deg_repair/"
                "phase7g_gb19_boundary2deg_repair_stage08_45k"
            ),
            "method_name": "esprit",
            "reference_rmse_deg": float(phase7d_metrics["rmse_deg"]),
        },
        "evaluation_cells": evaluation_cells,
        "report": {
            "flat_results_root": True,
            "write_summary_csv": True,
            "markdown_output": "phase7h_groupb_1p9_random_gap_generalization_results.md",
            "markdown_title": (
                "Phase 7H - Group B 1.9 Lambda Random-Gap Generalization"
            ),
            "markdown_description": (
                "Phase 7H evaluates the Phase 7G boundary-repair anti-rectifier fusion "
                "model on newly generated random-gap test sets so the angular separation "
                "is continuous rather than locked to the earlier fixed-gap grid."
            ),
            "markdown_conditions": [
                "Array: Group B 12-channel 2D hardware geometry",
                "Physical spacing: 1.9 lambda",
                "Model family: SS(2/3 x 3) -> LRMC -> width-controlled anti-rectifier spatial fusion -> SubspaceNet backbone 3x3 -> ESPRIT",
                "Checkpoint under test: best Phase 7G boundary-repair model",
                "Evaluation distribution: random azimuth gaps inside [-15 deg, 15 deg]",
                "Gap rule: min_doa_gap = 1 deg, with no fixed_doa_gap constraint",
                "Snapshots: T = 40",
                "Test sample count: 9,000 per dataset",
                "Primary metric: horizontal-angle RMSE in degrees",
                "Extra reporting: realized random-gap distribution summary per dataset",
            ],
            "random_gap_mode": True,
        },
        "template_name": PHASE7H_TEST_EXPERIMENTS[0],
    }

    target_path = generated_templates_dir / f"{PHASE7H_TEST_EXPERIMENTS[0]}.json"
    with target_path.open("w", encoding="utf-8") as handle:
        json.dump(template, handle, indent=2)
        handle.write("\n")


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    test_templates_dir = (repo_root / args.test_templates_dir).resolve()
    support_templates_dir = (repo_root / args.support_templates_dir).resolve()

    support_template_paths = ensure_phase7h_support_templates(
        repo_root, support_templates_dir, args.seed
    )
    ensure_phase7h_test_templates(
        repo_root, test_templates_dir, support_template_paths, args.seed
    )

    test_command = [
        sys.executable,
        str(repo_root / "run_test.py"),
        "--templates-dir",
        str(Path(args.test_templates_dir).as_posix()),
        "--experiments",
        ",".join(PHASE7H_TEST_EXPERIMENTS),
        "--seed",
        str(args.seed),
        "--results-dir",
        args.results_dir,
    ]

    print("Phase 7H experiment: Group B 1.9 lambda random-gap generalization")
    print("Results will be written under:", args.results_dir)
    print("Evaluation command:", " ".join(test_command))
    subprocess.run(test_command, check=True)


if __name__ == "__main__":
    main()
