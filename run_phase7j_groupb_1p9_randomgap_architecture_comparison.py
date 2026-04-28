"""Launch Phase 7J Group B 1.9 lambda random-gap architecture comparison."""

from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
import sys
from pathlib import Path


GAPS = [1, 2, 3, 4, 5]
SNRS = [1, 5, 10, 15]
RANDOM_GAP_SNRS = [1, 5, 10, 15]
PHASE7J_SAMPLES = 45000
PHASE7J_TEST_RATIO = 0.1
PHASE7J_EPOCHS = 80
PHASE7J_STRUCTURED_TOTAL = 22500
PHASE7J_RANDOM_TOTAL = 22500

MODEL_SPECS = [
    {
        "model_id": "C",
        "model_key": "modelc",
        "model_name": "Model C",
        "paper_label": "single-row no-SS 2x2",
        "input_path": "single-row linear-array covariance",
        "backbone": "2x2",
        "fusion_type": "none",
        "training_mode": "from scratch",
        "model_type": "SubspaceNetSingleRow",
        "use_lrmc": False,
        "covariance_mode": "sample",
        "backbone_kernel_size": 2,
    },
    {
        "model_id": "A",
        "model_key": "modela",
        "model_name": "Model A",
        "paper_label": "SS(3/3) -> LRMC -> SubspaceNet(2x2)",
        "input_path": "SS(3/3) -> LRMC virtual ULA",
        "backbone": "2x2",
        "fusion_type": "none",
        "training_mode": "from scratch",
        "model_type": "SubspaceNet",
        "use_lrmc": True,
        "covariance_mode": "ss_then_lrmc",
        "backbone_kernel_size": 2,
    },
    {
        "model_id": "B",
        "model_key": "modelb",
        "model_name": "Model B",
        "paper_label": "anti-rectifier SS-fusion 3x3",
        "input_path": "SS(2/3 x 3) -> LRMC branch fusion",
        "backbone": "3x3",
        "fusion_type": "anti-rectifier spatial fusion",
        "training_mode": "from scratch",
        "model_type": "SubspaceNetSSFusionAntiRectEspritPhase7d",
        "use_lrmc": True,
        "covariance_mode": "ss_then_lrmc",
        "backbone_kernel_size": 3,
    },
]


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Run the Phase 7J Group B 1.9 lambda random-gap architecture comparison."
        )
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase7j_groupb_1p9_randomgap_architecture_comparison",
        help="Dedicated output directory for the Phase 7J study.",
    )
    parser.add_argument(
        "--train-templates-dir",
        default=(
            "data/dataset_templates/ablation/"
            "phase7j_groupb_1p9_randomgap_architecture_comparison"
        ),
        help="Generated training-template directory for the Phase 7J study.",
    )
    parser.add_argument(
        "--test-templates-dir",
        default=(
            "data/dataset_templates/test/"
            "phase7j_groupb_1p9_randomgap_architecture_comparison"
        ),
        help="Generated test-template directory for the Phase 7J study.",
    )
    parser.add_argument(
        "--randomgap-support-dir",
        default=(
            "data/dataset_templates/ablation/"
            "phase7j_groupb_1p9_randomgap_architecture_comparison_support"
        ),
        help="Generated support-template directory for random-gap evaluation datasets.",
    )
    return parser.parse_args()


def load_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def save_json(path: Path, payload: dict):
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


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


def phase7h_compatible_template_name(coherence_key: str, snr: int):
    prefix = "coh" if coherence_key == "coherent" else "noncoh"
    return f"phase7h_gb19_{prefix}_randomgap_s{snr}"


def largest_remainder_counts(total: int, weighted_items: list[tuple]):
    total_weight = sum(float(weight) for _, weight in weighted_items)
    raw_counts = []
    assigned = 0
    for index, (key, weight) in enumerate(weighted_items):
        raw = 0.0 if total_weight <= 0 else total * float(weight) / total_weight
        floor_value = int(math.floor(raw))
        raw_counts.append((key, floor_value, raw - floor_value, index))
        assigned += floor_value
    remaining = int(total - assigned)
    raw_counts.sort(key=lambda item: (-item[2], item[3]))
    for index in range(remaining):
        key, floor_value, fraction, order = raw_counts[index]
        raw_counts[index] = (key, floor_value + 1, fraction, order)
    raw_counts.sort(key=lambda item: item[3])
    return {key: count for key, count, _, _ in raw_counts}


def structured_cell_totals():
    coherent_gap_totals = largest_remainder_counts(
        13500,
        [(1, 0.25), (2, 0.35), (3, 0.20), (4, 0.10), (5, 0.10)],
    )
    noncoherent_gap_totals = largest_remainder_counts(
        9000,
        [(1, 0.25), (2, 0.30), (3, 0.20), (4, 0.15), (5, 0.10)],
    )
    coherent_counts = {}
    noncoherent_counts = {}
    for gap in GAPS:
        coherent_counts[gap] = largest_remainder_counts(
            coherent_gap_totals[gap], [(snr, 1.0) for snr in SNRS]
        )
        noncoherent_counts[gap] = largest_remainder_counts(
            noncoherent_gap_totals[gap], [(snr, 1.0) for snr in SNRS]
        )
    return coherent_counts, noncoherent_counts


def build_stratified_cells(repo_root: Path):
    coherent_counts, noncoherent_counts = structured_cell_totals()
    cells = []
    for gap in GAPS:
        for snr in SNRS:
            cells.append(
                {
                    "template_path": str(
                        phase6_template_path(repo_root, "coherent", gap, snr)
                    ),
                    "coherence_key": "coherent",
                    "gap_deg": gap,
                    "snr_db": snr,
                    "total_samples": coherent_counts[gap][snr],
                }
            )
            cells.append(
                {
                    "template_path": str(
                        phase6_template_path(repo_root, "noncoherent", gap, snr)
                    ),
                    "coherence_key": "noncoherent",
                    "gap_deg": gap,
                    "snr_db": snr,
                    "total_samples": noncoherent_counts[gap][snr],
                }
            )
    return cells


def build_shared_mixed_dataset_config(repo_root: Path):
    return {
        "stratified_cells": build_stratified_cells(repo_root),
        "weighted_random": {
            "total_samples": PHASE7J_RANDOM_TOTAL,
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
    }


def training_template_name(model_spec: dict):
    return f"phase7j_gb19_{model_spec['model_key']}_randomgap_45k"


def test_template_name(model_spec: dict):
    return f"phase7j_gb19_{model_spec['model_key']}_eval"


def ensure_phase7j_randomgap_support_templates(
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
                "Phase 7J random-gap support template reusing the Phase 7H-compatible "
                f"random-gap definition for {coherence_key} at SNR={snr} dB."
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
            system_model.pop("fixed_doa_gap", None)
            template["dataset"]["samples_size"] = 45000
            template["dataset"]["train_test_ratio"] = 0.2
            target_path = support_dir / f"{template_name}.json"
            save_json(target_path, template)
            generated_paths[(coherence_key, snr)] = target_path
    return generated_paths


def ensure_phase7j_training_templates(
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
    mixed_dataset = build_shared_mixed_dataset_config(repo_root)
    template_names = []
    for model_spec in MODEL_SPECS:
        template = json.loads(json.dumps(source_template))
        template_name = training_template_name(model_spec)
        template_names.append(template_name)
        template["template_name"] = template_name
        template["description"] = (
            "Phase 7J fair from-scratch architecture comparison on a shared "
            f"45,000-sample random-gap dataset for {model_spec['paper_label']}."
        )
        template["scenario_data_path"] = f"p7j_{model_spec['model_key']}_45k"
        template["seed"] = seed
        template["methods"] = ["esprit"]
        template["commands"]["CREATE_DATA"] = True
        template["commands"]["CACHE_DATASET"] = True
        template["commands"]["LOAD_DATA"] = False
        template["commands"]["TRAIN_MODEL"] = True
        template["commands"]["EVALUATE_MODE"] = True
        template["dataset"] = {
            "samples_size": PHASE7J_SAMPLES,
            "train_test_ratio": PHASE7J_TEST_RATIO,
            "mixed_dataset": mixed_dataset,
        }

        system_model = template["system_model"]
        system_model["T"] = 40
        system_model["snr"] = 1
        system_model["signal_nature"] = "coherent"
        system_model["doa_min"] = -15
        system_model["doa_max"] = 15
        system_model["min_doa_gap"] = 1
        system_model.pop("fixed_doa_gap", None)
        system_model["subspacenet_backbone_kernel_size"] = model_spec[
            "backbone_kernel_size"
        ]
        system_model["use_lrmc"] = model_spec["use_lrmc"]
        system_model["covariance_mode"] = model_spec["covariance_mode"]
        if model_spec["use_lrmc"]:
            system_model["ss_num_subarrays"] = 3
            system_model["ss_row_subset"] = [0, 1, 2]
        else:
            system_model.pop("ss_num_subarrays", None)
            system_model.pop("ss_row_subset", None)
        if model_spec["model_type"].startswith("SubspaceNetSSFusion"):
            system_model["ss_fusion_hidden_channels"] = 16
            system_model["ss_fusion_diagonal_loading"] = 1e-6

        template["model"]["model_type"] = model_spec["model_type"]
        template["model"]["tau"] = 8
        template["model"]["diff_method"] = "esprit"

        training = template["training"]
        training.pop("pretrained_experiment_dir", None)
        training.pop("pretrained_method_name", None)
        training["epochs"] = PHASE7J_EPOCHS
        training["learning_rate"] = 1e-5
        training["weight_decay"] = 1e-9
        training["scheduler_step_size"] = 40
        training["scheduler_gamma"] = 0.5

        report = template["report"]
        report["write_summary_csv"] = False
        report["markdown_output"] = ""

        save_json(generated_templates_dir / f"{template_name}.json", template)

    return template_names


def classify_fixed_split(coherence_key: str, gap: int, snr: int):
    if coherence_key == "coherent" and gap == 1 and snr == 1:
        return "in_domain_anchor"
    if coherence_key == "coherent":
        return "coherent_ood"
    return "noncoherent_transfer"


def build_evaluation_cells(repo_root: Path, randomgap_support_templates: dict, model_spec: dict):
    evaluation_cells = []
    for coherence_key, coherence_label in [
        ("coherent", "coherent"),
        ("noncoherent", "non-coherent"),
    ]:
        for gap in GAPS:
            for snr in SNRS:
                bucket_labels = [classify_fixed_split(coherence_key, gap, snr)]
                if coherence_key == "coherent" and gap == 2:
                    bucket_labels.append("coherent_2deg_boundary")
                evaluation_cells.append(
                    {
                        "template_path": str(
                            phase6_template_path(repo_root, coherence_key, gap, snr)
                        ),
                        "result_name": (
                            f"phase7j_{model_spec['model_key']}_"
                            f"{'coh' if coherence_key == 'coherent' else 'noncoh'}"
                            f"_g{gap}_s{snr}"
                        ),
                        "method_name": "esprit",
                        "coherence_key": coherence_key,
                        "coherence_label": coherence_label,
                        "gap_deg": gap,
                        "snr_db": snr,
                        "split": classify_fixed_split(coherence_key, gap, snr),
                        "bucket_labels": bucket_labels,
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
                        f"phase7j_{model_spec['model_key']}_"
                        f"{'coh' if coherence_key == 'coherent' else 'noncoh'}_randomgap_s{snr}"
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
                }
            )
    return evaluation_cells


def ensure_phase7j_test_templates(
    repo_root: Path,
    generated_templates_dir: Path,
    randomgap_support_templates: dict,
    seed: int,
):
    generated_templates_dir.mkdir(parents=True, exist_ok=True)
    template_names = []
    for model_spec in MODEL_SPECS:
        template_name = test_template_name(model_spec)
        template_names.append(template_name)
        template = {
            "description": (
                "Phase 7J evaluates one from-scratch architecture variant on the shared "
                "40-cell fixed-gap grid and the shared 8-cell random-gap family."
            ),
            "experiment_type": "subspacenet_transfer_test",
            "seed": seed,
            "commands": {
                "GENERATE_MISSING_DATA": True,
                "SAVE_GENERATED_DATA": True,
            },
            "source_model": {
                "experiment_dir": (
                    "results/phase7j_groupb_1p9_randomgap_architecture_comparison/"
                    f"{training_template_name(model_spec)}"
                ),
                "method_name": "esprit",
            },
            "evaluation_cells": build_evaluation_cells(
                repo_root, randomgap_support_templates, model_spec
            ),
            "report": {
                "write_summary_csv": True,
            },
            "template_name": template_name,
        }
        save_json(generated_templates_dir / f"{template_name}.json", template)
    return template_names


def load_summary_rows(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            for key in [
                "gap_deg",
                "snr_db",
                "rmse_deg",
                "avg_runtime_sec",
                "realized_mean_gap_deg",
                "realized_median_gap_deg",
                "realized_min_gap_deg",
                "realized_max_gap_deg",
            ]:
                value = row.get(key)
                if value in {"", None}:
                    row[key] = None
                else:
                    row[key] = float(value)
            rows.append(row)
    return rows


def model_rows_by_cell(rows: list[dict]):
    keyed = {}
    for row in rows:
        keyed[(row.get("coherence"), row.get("gap_deg"), row.get("snr_db"))] = row
    return keyed


def bucket_stats(rows: list[dict], bucket_name: str):
    members = [
        row
        for row in rows
        if bucket_name in str(row.get("bucket_labels", "")).split("|")
    ]
    if not members:
        return None
    rmse_values = [row["rmse_deg"] for row in members if row.get("rmse_deg") is not None]
    runtime_values = [
        row["avg_runtime_sec"] for row in members if row.get("avg_runtime_sec") is not None
    ]
    return {
        "bucket_name": bucket_name,
        "num_cells": len(members),
        "mean_rmse_deg": sum(rmse_values) / len(rmse_values),
        "mean_runtime_sec": (
            None
            if not runtime_values
            else sum(runtime_values) / len(runtime_values)
        ),
    }


def format_float(value, digits: int = 4):
    if value is None:
        return "missing"
    return f"{float(value):.{digits}f}"


def delta_text(lhs: float | None, rhs: float | None):
    if lhs is None or rhs is None:
        return "missing"
    return f"{(lhs - rhs):+.4f}"


def write_combined_outputs(results_root: Path):
    model_eval_rows = {}
    for model_spec in MODEL_SPECS:
        summary_path = results_root / test_template_name(model_spec) / "summary.csv"
        rows = load_summary_rows(summary_path)
        for row in rows:
            row["model_id"] = model_spec["model_id"]
            row["model_name"] = model_spec["model_name"]
            row["paper_label"] = model_spec["paper_label"]
            row["input_path"] = model_spec["input_path"]
            row["backbone"] = model_spec["backbone"]
            row["fusion_type"] = model_spec["fusion_type"]
            row["training_mode"] = model_spec["training_mode"]
        model_eval_rows[model_spec["model_id"]] = rows

    combined_rows = []
    for model_spec in MODEL_SPECS:
        combined_rows.extend(model_eval_rows[model_spec["model_id"]])

    summary_path = results_root / "summary.csv"
    fieldnames = [
        "model_id",
        "model_name",
        "paper_label",
        "input_path",
        "backbone",
        "fusion_type",
        "training_mode",
        "scheme",
        "method",
        "coherence",
        "gap_deg",
        "snr_db",
        "split",
        "bucket_labels",
        "dataset_cache_status",
        "dataset_path",
        "rmse_deg",
        "avg_runtime_sec",
        "realized_mean_gap_deg",
        "realized_median_gap_deg",
        "realized_min_gap_deg",
        "realized_max_gap_deg",
    ]
    with summary_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in combined_rows:
            writer.writerow({field: row.get(field) for field in fieldnames})

    bucket_names = [
        "in_domain_anchor",
        "coherent_2deg_boundary",
        "coherent_ood",
        "noncoherent_transfer",
        "coherent_random_gap",
        "noncoherent_random_gap",
    ]
    bucket_csv_path = (
        results_root
        / "phase7j_groupb_1p9_randomgap_architecture_comparison_bucket_summary.csv"
    )
    with bucket_csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "model_id",
                "model_name",
                "bucket_name",
                "num_cells",
                "mean_rmse_deg",
                "mean_runtime_sec",
            ],
        )
        writer.writeheader()
        for model_spec in MODEL_SPECS:
            rows = model_eval_rows[model_spec["model_id"]]
            for bucket_name in bucket_names:
                stats = bucket_stats(rows, bucket_name)
                if stats is None:
                    continue
                writer.writerow(
                    {
                        "model_id": model_spec["model_id"],
                        "model_name": model_spec["model_name"],
                        **stats,
                    }
                )

    model_maps = {
        model_id: model_rows_by_cell(rows) for model_id, rows in model_eval_rows.items()
    }
    random_keys = sorted(
        [
            key
            for key in model_maps["B"].keys()
            if key[1] is None
        ],
        key=lambda item: (item[0], item[2]),
    )
    boundary_keys = sorted(
        [
            key
            for key in model_maps["B"].keys()
            if key[0] == "coherent" and key[1] == 2.0
        ],
        key=lambda item: item[2],
    )
    anchor_key = ("coherent", 1.0, 1.0)

    lines = [
        "# Phase 7J - Group B 1.9 Lambda Random-Gap Architecture Comparison",
        "",
        "Phase 7J compares three from-scratch SubspaceNet-era architectures under the same 45,000-sample random-gap training recipe and the same fixed-gap plus random-gap evaluation families.",
        "",
        "Experimental conditions:",
        "- Array: Group B 12-channel 2D hardware geometry",
        "- Physical spacing: 1.9 lambda",
        "- Signals: 2 narrowband sources, 60% coherent / 40% non-coherent training mix",
        "- Snapshots: T = 40",
        "- Training set: 45,000 samples with a 40,500 / 4,500 train:test split",
        "- Dataset mix: 50% structured protection + 50% continuous random-gap samples",
        "- Structured coherent gap weights: 25/35/20/10/10 for gaps 1/2/3/4/5 deg",
        "- Structured non-coherent gap weights: 25/30/20/15/10 for gaps 1/2/3/4/5 deg",
        "- Random-gap bins: 1-2, 2-3, 3-5, 5-10, 10-29 deg",
        "- Shared SNR weights: 35/30/20/15 for 1/5/10/15 dB",
        "- Training mode: one uninterrupted 80-epoch run per model, from scratch",
        "- Evaluation: reused 40-cell fixed-gap grid plus 8 random-gap cells",
        "",
        "## Architecture Overview",
        "",
        "| Model | Input path | Backbone | Fusion type | Training mode | Epochs |",
        "| --- | --- | --- | --- | --- | ---: |",
    ]
    for model_spec in MODEL_SPECS:
        lines.append(
            f"| {model_spec['model_name']} ({model_spec['model_id']}) | {model_spec['input_path']} | "
            f"{model_spec['backbone']} | {model_spec['fusion_type']} | {model_spec['training_mode']} | {PHASE7J_EPOCHS} |"
        )

    lines.extend(
        [
            "",
            "## Random-Gap Comparison",
            "",
            "| Coherence | SNR (dB) | Model C RMSE | Model A RMSE | Model B RMSE | Delta A-C | Delta B-A | Delta B-C |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for key in random_keys:
        row_c = model_maps["C"].get(key)
        row_a = model_maps["A"].get(key)
        row_b = model_maps["B"].get(key)
        lines.append(
            f"| {key[0]} | {int(key[2])} | {format_float(row_c.get('rmse_deg') if row_c else None)} | "
            f"{format_float(row_a.get('rmse_deg') if row_a else None)} | "
            f"{format_float(row_b.get('rmse_deg') if row_b else None)} | "
            f"{delta_text(row_a.get('rmse_deg') if row_a else None, row_c.get('rmse_deg') if row_c else None)} | "
            f"{delta_text(row_b.get('rmse_deg') if row_b else None, row_a.get('rmse_deg') if row_a else None)} | "
            f"{delta_text(row_b.get('rmse_deg') if row_b else None, row_c.get('rmse_deg') if row_c else None)} |"
        )

    lines.extend(
        [
            "",
            "## Coherent 2-Degree Boundary",
            "",
            "| SNR (dB) | Model C RMSE | Model A RMSE | Model B RMSE | Delta A-C | Delta B-A | Delta B-C |",
            "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for key in boundary_keys:
        row_c = model_maps["C"].get(key)
        row_a = model_maps["A"].get(key)
        row_b = model_maps["B"].get(key)
        lines.append(
            f"| {int(key[2])} | {format_float(row_c.get('rmse_deg') if row_c else None)} | "
            f"{format_float(row_a.get('rmse_deg') if row_a else None)} | "
            f"{format_float(row_b.get('rmse_deg') if row_b else None)} | "
            f"{delta_text(row_a.get('rmse_deg') if row_a else None, row_c.get('rmse_deg') if row_c else None)} | "
            f"{delta_text(row_b.get('rmse_deg') if row_b else None, row_a.get('rmse_deg') if row_a else None)} | "
            f"{delta_text(row_b.get('rmse_deg') if row_b else None, row_c.get('rmse_deg') if row_c else None)} |"
        )

    row_c = model_maps["C"].get(anchor_key)
    row_a = model_maps["A"].get(anchor_key)
    row_b = model_maps["B"].get(anchor_key)
    lines.extend(
        [
            "",
            "## Source-Cell Anchor",
            "",
            "| Cell | Model C RMSE | Model A RMSE | Model B RMSE |",
            "| --- | ---: | ---: | ---: |",
            f"| coherent, gap 1 deg, SNR 1 dB | {format_float(row_c.get('rmse_deg') if row_c else None)} | "
            f"{format_float(row_a.get('rmse_deg') if row_a else None)} | "
            f"{format_float(row_b.get('rmse_deg') if row_b else None)} |",
            "",
            "## Summary Bucket Table",
            "",
            "| Bucket | Model C mean RMSE | Model A mean RMSE | Model B mean RMSE |",
            "| --- | ---: | ---: | ---: |",
        ]
    )
    for bucket_name in bucket_names:
        stats_c = bucket_stats(model_eval_rows["C"], bucket_name)
        stats_a = bucket_stats(model_eval_rows["A"], bucket_name)
        stats_b = bucket_stats(model_eval_rows["B"], bucket_name)
        lines.append(
            f"| {bucket_name} | {format_float(stats_c['mean_rmse_deg']) if stats_c else 'missing'} | "
            f"{format_float(stats_a['mean_rmse_deg']) if stats_a else 'missing'} | "
            f"{format_float(stats_b['mean_rmse_deg']) if stats_b else 'missing'} |"
        )

    output_path = (
        results_root
        / "phase7j_groupb_1p9_randomgap_architecture_comparison_results.md"
    )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    results_root = (repo_root / args.results_dir).resolve()
    train_templates_dir = (repo_root / args.train_templates_dir).resolve()
    test_templates_dir = (repo_root / args.test_templates_dir).resolve()
    randomgap_support_dir = (repo_root / args.randomgap_support_dir).resolve()
    results_root.mkdir(parents=True, exist_ok=True)

    train_experiments = ensure_phase7j_training_templates(
        repo_root, train_templates_dir, args.seed
    )
    randomgap_support_templates = ensure_phase7j_randomgap_support_templates(
        repo_root, randomgap_support_dir, args.seed
    )
    test_experiments = ensure_phase7j_test_templates(
        repo_root, test_templates_dir, randomgap_support_templates, args.seed
    )

    print("Phase 7J experiment: Group B 1.9 lambda random-gap architecture comparison")
    print("Results will be written under:", args.results_dir)
    for experiment_name in train_experiments:
        train_command = [
            sys.executable,
            str(repo_root / "run_ablation.py"),
            "--templates-dir",
            str(Path(args.train_templates_dir).as_posix()),
            "--experiments",
            experiment_name,
            "--seed",
            str(args.seed),
            "--results-dir",
            args.results_dir,
        ]
        print("Training command:", " ".join(train_command))
        subprocess.run(train_command, check=True)

    for experiment_name in test_experiments:
        test_command = [
            sys.executable,
            str(repo_root / "run_test.py"),
            "--templates-dir",
            str(Path(args.test_templates_dir).as_posix()),
            "--experiments",
            experiment_name,
            "--seed",
            str(args.seed),
            "--results-dir",
            args.results_dir,
        ]
        print("Evaluation command:", " ".join(test_command))
        subprocess.run(test_command, check=True)

    write_combined_outputs(results_root)


if __name__ == "__main__":
    main()
