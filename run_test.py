"""Run template-driven evaluation and transfer-test experiments."""

from __future__ import annotations

import argparse
import copy
import csv
import json
import time
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import torch
from tqdm import tqdm

from src.data_handler import build_subspacenet_input, create_dataset, load_datasets
from src.dataset_template import build_system_model_params_from_template
from src.models import ModelGenerator
from src.training import get_simulation_filename
from src.utils import R2D, device, set_unified_seed


def parse_args():
    parser = argparse.ArgumentParser(description="Run evaluation / transfer-test templates.")
    parser.add_argument(
        "--templates-dir",
        default="data/dataset_templates/test",
        help="Directory containing evaluation JSON templates.",
    )
    parser.add_argument(
        "--experiments",
        default="all",
        help="Comma-separated list of test template names to run, or 'all'.",
    )
    parser.add_argument(
        "--results-dir",
        default="results/tests",
        help="Root directory for test outputs.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Override random seed for deterministic evaluation order.",
    )
    return parser.parse_args()


def ensure_dirs(*paths: Path):
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def save_json(path: Path, payload: Dict):
    def convert(value):
        if isinstance(value, Path):
            return str(value)
        if isinstance(value, np.ndarray):
            return value.tolist()
        if isinstance(value, (np.float32, np.float64)):
            return float(value)
        if isinstance(value, (np.int32, np.int64)):
            return int(value)
        return value

    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, default=convert)


def load_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def load_templates(templates_dir: Path) -> Dict[str, Dict]:
    templates = {}
    for path in sorted(templates_dir.rglob("*.json")):
        with path.open("r", encoding="utf-8-sig") as handle:
            template = json.load(handle)
        template_name = path.stem
        template["template_name"] = template_name
        template["template_path"] = str(path)
        templates[template_name] = template
    return templates


def select_templates(all_templates: Dict[str, Dict], selection: str) -> List[Dict]:
    if selection == "all":
        return [copy.deepcopy(template) for template in all_templates.values()]
    names = [name.strip() for name in selection.split(",") if name.strip()]
    missing = [name for name in names if name not in all_templates]
    if missing:
        raise ValueError(f"Unknown test template(s): {missing}")
    return [copy.deepcopy(all_templates[name]) for name in names]


def apply_overrides(template: Dict, args):
    if args.seed is not None:
        template["seed"] = args.seed


def periodic_rmse_deg(predictions_deg: np.ndarray, targets_deg: np.ndarray) -> float:
    predictions_deg = np.asarray(predictions_deg, dtype=float)
    targets_deg = np.asarray(targets_deg, dtype=float)
    if predictions_deg.shape[0] < targets_deg.shape[0]:
        while predictions_deg.shape[0] < targets_deg.shape[0]:
            random_angle = np.round(np.random.rand(1) * 180, decimals=2) - 90.0
            predictions_deg = np.insert(predictions_deg, 0, random_angle)
    elif predictions_deg.shape[0] > targets_deg.shape[0]:
        predictions_deg = predictions_deg[: targets_deg.shape[0]]
    errors = []
    for permutation in __import__("itertools").permutations(
        predictions_deg, len(predictions_deg)
    ):
        perm = np.asarray(permutation, dtype=float)
        error_deg = ((perm - targets_deg + 90.0) % 180.0) - 90.0
        errors.append(np.sqrt(np.mean(error_deg**2)))
    return float(np.min(errors))


def maybe_cuda_synchronize():
    if torch.cuda.is_available():
        torch.cuda.synchronize()


def compute_realized_gap_stats(
    generic_test_dataset: List[Tuple[torch.Tensor, torch.Tensor]]
):
    gap_values = []
    for _, doa in generic_test_dataset:
        doa_deg = np.sort(np.asarray(doa, dtype=float) * R2D)
        if doa_deg.size >= 2:
            gap_values.append(float(abs(doa_deg[1] - doa_deg[0])))
    if not gap_values:
        return {}
    gap_array = np.asarray(gap_values, dtype=float)
    return {
        "realized_mean_gap_deg": float(np.mean(gap_array)),
        "realized_median_gap_deg": float(np.median(gap_array)),
        "realized_min_gap_deg": float(np.min(gap_array)),
        "realized_max_gap_deg": float(np.max(gap_array)),
    }


def parse_reference_summary(path: Path):
    by_scheme: Dict[str, List[Dict[str, object]]] = {}
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            row["rmse_deg"] = float(row["rmse_deg"])
            by_scheme.setdefault(row["scheme"], []).append(row)
    return by_scheme


def build_reference_maps(reference_sources: Dict | None):
    if not reference_sources:
        return {}
    reference_maps = {}
    for key, value in reference_sources.items():
        if key.endswith("_summary_csv"):
            map_key = key.replace("_summary_csv", "")
            reference_maps[map_key] = parse_reference_summary(Path(value))
    return reference_maps


def get_reference_metrics(reference_maps: Dict[str, Dict], cell_config: Dict):
    coherence_key = cell_config.get("coherence_key")
    gap = cell_config.get("gap_deg")
    snr = cell_config.get("snr_db")
    if coherence_key is None or gap is None or snr is None:
        return None, None, None
    summary = reference_maps.get(coherence_key)
    if summary is None:
        return None, None, None

    control_scheme = f"phase6_groupb_1p9_{coherence_key}_control_gap{gap}_snr{snr}"
    learned_scheme = (
        f"phase6_groupb_1p9_{coherence_key}_subspacenet_esprit_gap{gap}_snr{snr}"
    )
    control_rows = summary.get(control_scheme, [])
    learned_rows = summary.get(learned_scheme, [])

    classical_best_method = None
    classical_best_rmse = None
    if control_rows:
        best_row = min(control_rows, key=lambda row: row["rmse_deg"])
        classical_best_method = best_row["method"]
        classical_best_rmse = float(best_row["rmse_deg"])

    direct_learned_rmse = None
    if learned_rows:
        direct_learned_rmse = float(learned_rows[0]["rmse_deg"])

    return classical_best_method, classical_best_rmse, direct_learned_rmse


def get_named_reference_rmse(
    reference_maps: Dict[str, Dict], summary_key: str, scheme_name: str, method_name: str
):
    summary = reference_maps.get(summary_key)
    if summary is None:
        return None
    rows = summary.get(scheme_name, [])
    if not rows:
        return None
    for row in rows:
        if row.get("method") == method_name:
            return float(row["rmse_deg"])
    return float(rows[0]["rmse_deg"])


def resolve_source_model(repo_root: Path, source_model_config: Dict):
    experiment_dir = Path(source_model_config["experiment_dir"])
    if not experiment_dir.is_absolute():
        experiment_dir = (repo_root / experiment_dir).resolve()
    method_name = source_model_config.get("method_name", "esprit")
    resolved_template_path = experiment_dir / "resolved_template.json"
    metrics_path = experiment_dir / method_name / "metrics.json"
    template = load_json(resolved_template_path)
    metrics = load_json(metrics_path)
    checkpoint_dir = Path(metrics["checkpoint_dir"])
    if not checkpoint_dir.is_absolute():
        checkpoint_dir = checkpoint_dir.resolve()

    system_model_params = build_system_model_params_from_template(template)
    system_model_params.set_parameter("template_name", template["template_name"])
    model_config = (
        ModelGenerator()
        .set_model_type(template["model"]["model_type"])
        .set_diff_method(template["model"]["diff_method"])
        .set_tau(int(template["model"]["tau"]))
        .set_model(system_model_params)
    )
    model = model_config.model.to(device)

    checkpoint_name = get_simulation_filename(system_model_params, model_config)
    checkpoint_path = checkpoint_dir / checkpoint_name
    if not checkpoint_path.exists():
        candidates = [path for path in checkpoint_dir.iterdir() if path.is_file()]
        if not candidates:
            raise FileNotFoundError(f"No checkpoint files found in {checkpoint_dir}")
        candidates.sort(key=lambda path: path.stat().st_mtime, reverse=True)
        checkpoint_path = candidates[0]

    state_dict = torch.load(checkpoint_path, map_location=device)
    model.load_state_dict(state_dict)
    model.eval()
    return model, template, metrics, checkpoint_path


def prepare_generic_test_dataset(
    repo_root: Path,
    source_template: Dict,
    commands: Dict,
):
    system_model_params = build_system_model_params_from_template(source_template)
    system_model_params.set_parameter("template_name", source_template["template_name"])
    dataset_settings = source_template["dataset"]
    datasets_path = repo_root / "data" / "datasets" / source_template["scenario_data_path"]
    ensure_dirs(datasets_path, datasets_path / "test")

    loaded = None
    cache_status = "loaded"
    try:
        loaded = load_datasets(
            system_model_params=system_model_params,
            model_type="Classical",
            samples_size=dataset_settings["samples_size"],
            datasets_path=datasets_path,
            train_test_ratio=dataset_settings["train_test_ratio"],
            is_training=False,
        )
    except Exception:
        loaded = None

    if loaded is None:
        if not commands.get("GENERATE_MISSING_DATA", True):
            raise FileNotFoundError(
                f"No matching cached test dataset found for {source_template['template_name']} "
                f"and GENERATE_MISSING_DATA is disabled."
            )
        cache_status = "generated"
        test_dataset, generic_test_dataset, samples_model = create_dataset(
            system_model_params=system_model_params,
            samples_size=int(
                dataset_settings["train_test_ratio"] * dataset_settings["samples_size"]
            ),
            model_type="Classical",
            tau=int(source_template.get("model", {}).get("tau", 8)),
            save_datasets=bool(commands.get("SAVE_GENERATED_DATA", True)),
            datasets_path=datasets_path,
            true_doa=None,
            phase="test",
        )
        loaded = (test_dataset, generic_test_dataset, samples_model)

    _, generic_test_dataset, samples_model = loaded
    return generic_test_dataset, samples_model, system_model_params, datasets_path, cache_status


def evaluate_transfer_cell(
    model,
    generic_test_dataset: List[Tuple[torch.Tensor, torch.Tensor]],
    system_model_params,
    model_type: str,
    tau: int,
    cell_config: Dict,
    result_dir: Path,
):
    errors = []
    total_runtimes = []
    preprocess_runtimes = []
    forward_runtimes = []
    fusion_norms = []
    fusion_diag_means = []
    branch_norms = []
    progress = tqdm(
        generic_test_dataset,
        total=len(generic_test_dataset),
        desc=f"{cell_config['result_name']}::{cell_config.get('method_name', 'esprit')}",
    )
    with torch.no_grad():
        for X, doa in progress:
            maybe_cuda_synchronize()
            total_start = time.perf_counter()

            preprocess_start = time.perf_counter()
            model_input = build_subspacenet_input(
                X=X,
                system_model_params=system_model_params,
                tau=tau,
                model_type=model_type,
            )
            preprocess_end = time.perf_counter()

            inputs = model_input.unsqueeze(0).to(device, non_blocking=True)
            maybe_cuda_synchronize()
            forward_start = time.perf_counter()
            predictions_rad = model(inputs)[0].detach().cpu().numpy().squeeze()
            maybe_cuda_synchronize()
            forward_end = time.perf_counter()
            total_end = time.perf_counter()

            targets_deg = np.asarray(doa) * R2D
            predictions_deg = np.asarray(predictions_rad) * R2D
            errors.append(periodic_rmse_deg(predictions_deg, targets_deg))
            total_runtimes.append(total_end - total_start)
            preprocess_runtimes.append(preprocess_end - preprocess_start)
            forward_runtimes.append(forward_end - forward_start)

            diagnostics = getattr(model, "last_fusion_diagnostics", None)
            if diagnostics is not None:
                if diagnostics.get("fused_covariance_norm") is not None:
                    fusion_norms.append(float(diagnostics["fused_covariance_norm"]))
                if diagnostics.get("fused_diagonal_mean_real") is not None:
                    fusion_diag_means.append(
                        float(diagnostics["fused_diagonal_mean_real"])
                    )
                if diagnostics.get("input_branch_norms") is not None:
                    branch_norms.append(list(diagnostics["input_branch_norms"]))

    metrics = {
        "rmse_deg": float(np.mean(errors)),
        "avg_runtime_sec": float(np.mean(total_runtimes)),
        "avg_preprocess_runtime_sec": float(np.mean(preprocess_runtimes)),
        "avg_forward_runtime_sec": float(np.mean(forward_runtimes)),
        "dataset_pass_runtime_sec": float(np.sum(total_runtimes)),
        "num_test_samples": len(generic_test_dataset),
        "best_sample_rmse_deg": float(np.min(errors)),
        "worst_sample_rmse_deg": float(np.max(errors)),
        "median_sample_rmse_deg": float(np.median(errors)),
    }
    if fusion_norms:
        metrics["avg_fused_covariance_norm"] = float(np.mean(fusion_norms))
    if fusion_diag_means:
        metrics["avg_fused_diagonal_mean_real"] = float(np.mean(fusion_diag_means))
    if branch_norms:
        metrics["avg_input_branch_norms"] = (
            np.mean(np.asarray(branch_norms, dtype=float), axis=0).tolist()
        )
    if getattr(model, "last_fusion_diagnostics", None) is not None:
        kernel_type = model.last_fusion_diagnostics.get("fusion_kernel_type")
        if kernel_type:
            metrics["fusion_kernel_type"] = kernel_type
    if getattr(model, "backbone_kernel_size", None) is not None:
        metrics["subspacenet_backbone_kernel_size"] = int(model.backbone_kernel_size)

    save_json(result_dir / "metrics.json", metrics)
    return metrics


def build_bucket_summary(rows: List[Dict]):
    bucket_rows = []
    bucket_names = []
    for row in rows:
        labels = row.get("bucket_labels", "")
        if labels:
            bucket_names.extend(labels.split("|"))
    for bucket in sorted(set(bucket_names)):
        members = [row for row in rows if bucket in row.get("bucket_labels", "").split("|")]
        if not members:
            continue
        rmse_values = np.asarray([row["rmse_deg"] for row in members], dtype=float)
        runtime_values = np.asarray([row["avg_runtime_sec"] for row in members], dtype=float)
        bucket_rows.append(
            {
                "bucket_name": bucket,
                "num_cells": len(members),
                "mean_rmse_deg": float(np.mean(rmse_values)),
                "median_rmse_deg": float(np.median(rmse_values)),
                "best_rmse_deg": float(np.min(rmse_values)),
                "worst_rmse_deg": float(np.max(rmse_values)),
                "mean_runtime_sec": float(np.mean(runtime_values)),
            }
        )
    return bucket_rows


def row_gap_sort_value(row: Dict):
    gap = row.get("gap_deg")
    return float(gap) if gap is not None else 999.0


def row_sort_key(row: Dict):
    return (row.get("coherence", ""), row_gap_sort_value(row), row.get("snr_db", 0))


def write_summary_csv(rows: List[Dict], output_path: Path):
    fieldnames = [
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
        "avg_preprocess_runtime_sec",
        "avg_forward_runtime_sec",
        "dataset_pass_runtime_sec",
        "num_test_samples",
        "realized_mean_gap_deg",
        "realized_median_gap_deg",
        "realized_min_gap_deg",
        "realized_max_gap_deg",
        "delta_vs_source_train_cell_rmse_deg",
        "phase6_classical_best_method",
        "phase6_classical_best_rmse_deg",
        "delta_vs_phase6_classical_best_rmse_deg",
        "phase6_direct_learned_rmse_deg",
        "delta_vs_phase6_direct_learned_rmse_deg",
        "phase7e_reference_rmse_deg",
        "delta_vs_phase7e_reference_rmse_deg",
        "phase7f_reference_rmse_deg",
        "delta_vs_phase7f_reference_rmse_deg",
        "phase7g_reference_rmse_deg",
        "delta_vs_phase7g_reference_rmse_deg",
        "phase7h_reference_rmse_deg",
        "delta_vs_phase7h_reference_rmse_deg",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key) for key in fieldnames})


def write_bucket_summary_csv(rows: List[Dict], output_path: Path):
    fieldnames = [
        "bucket_name",
        "num_cells",
        "mean_rmse_deg",
        "median_rmse_deg",
        "best_rmse_deg",
        "worst_rmse_deg",
        "mean_runtime_sec",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def format_float(value):
    if value is None or value == "":
        return "missing"
    return f"{float(value):.4f}"


def write_transfer_markdown(
    rows: List[Dict],
    bucket_rows: List[Dict],
    output_path: Path,
    report: Dict,
    source_train_rmse: float,
):
    if report.get("hybrid_random_gap_mode", False):
        fixed_rows = [row for row in rows if row.get("gap_deg") is not None]
        random_rows = [row for row in rows if row.get("gap_deg") is None]
        coherent_fixed_rows = [
            row for row in fixed_rows if row.get("coherence") == "coherent"
        ]
        noncoherent_fixed_rows = [
            row for row in fixed_rows if row.get("coherence") == "non-coherent"
        ]
        coherent_random_rows = [
            row for row in random_rows if row.get("coherence") == "coherent"
        ]
        noncoherent_random_rows = [
            row for row in random_rows if row.get("coherence") == "non-coherent"
        ]
        coherent_fixed_rows.sort(key=row_sort_key)
        noncoherent_fixed_rows.sort(key=row_sort_key)
        coherent_random_rows.sort(key=lambda row: row.get("snr_db", 0))
        noncoherent_random_rows.sort(key=lambda row: row.get("snr_db", 0))

        lines = [f"# {report.get('markdown_title', 'Transfer Test Results')}", ""]
        description = report.get("markdown_description", "")
        if description:
            lines.extend([description, ""])
        conditions = report.get("markdown_conditions", [])
        if conditions:
            lines.append("Experimental conditions:")
            for condition in conditions:
                lines.append(f"- {condition}")
            lines.append("")
        lines.append(f"Reference anchor RMSE: `{source_train_rmse:.4f} deg`")
        lines.append("")

        random_gap_rows = [
            row for row in random_rows if row.get("phase7h_reference_rmse_deg") is not None
        ]
        if random_gap_rows:
            lines.append("## Random-Gap Comparison")
            lines.append("")
            lines.append("| Coherence | SNR (dB) | Phase 7H RMSE (deg) | Phase 7I RMSE (deg) | Delta vs Phase 7H |")
            lines.append("| --- | ---: | ---: | ---: | ---: |")
            for row in sorted(random_gap_rows, key=row_sort_key):
                phase7h_text = f"{row['phase7h_reference_rmse_deg']:.4f}"
                delta_phase7h_text = f"{row['delta_vs_phase7h_reference_rmse_deg']:+.4f}"
                lines.append(
                    f"| {row.get('coherence', 'unknown')} | {row.get('snr_db', '')} | {phase7h_text} | {row['rmse_deg']:.4f} | {delta_phase7h_text} |"
                )
            lines.append("")

        coherent_2deg_rows = [
            row
            for row in coherent_fixed_rows
            if int(row.get("gap_deg", 0)) == 2
            and row.get("phase7g_reference_rmse_deg") is not None
        ]
        if coherent_2deg_rows:
            lines.append("## Coherent 2-Degree Protection")
            lines.append("")
            lines.append("| SNR (dB) | Phase 7G RMSE (deg) | Phase 7I RMSE (deg) | Delta vs Phase 7G |")
            lines.append("| ---: | ---: | ---: | ---: |")
            for row in coherent_2deg_rows:
                lines.append(
                    f"| {row.get('snr_db', '')} | {row['phase7g_reference_rmse_deg']:.4f} | {row['rmse_deg']:.4f} | {row['delta_vs_phase7g_reference_rmse_deg']:+.4f} |"
                )
            lines.append("")

        retention_rows = [
            row
            for row in fixed_rows
            if row.get("split") == "in_domain_anchor"
            or bool(row.get("retention_priority"))
        ]
        if retention_rows:
            lines.append("## Source-Cell Retention")
            lines.append("")
            lines.append("| Cell | Phase 7F | Phase 7G | Phase 7I | Delta vs Phase 7G |")
            lines.append("| --- | ---: | ---: | ---: | ---: |")
            for row in sorted(retention_rows, key=row_sort_key):
                cell_label = (
                    f"{row.get('coherence', 'unknown')} | gap {row.get('gap_deg', '?')} | snr {row.get('snr_db', '?')}"
                )
                phase7f_text = (
                    f"{row['phase7f_reference_rmse_deg']:.4f}"
                    if row.get("phase7f_reference_rmse_deg") is not None
                    else "missing"
                )
                phase7g_text = (
                    f"{row['phase7g_reference_rmse_deg']:.4f}"
                    if row.get("phase7g_reference_rmse_deg") is not None
                    else "missing"
                )
                delta_phase7g_text = (
                    f"{row['delta_vs_phase7g_reference_rmse_deg']:+.4f}"
                    if row.get("delta_vs_phase7g_reference_rmse_deg") is not None
                    else "missing"
                )
                lines.append(
                    f"| {cell_label} | {phase7f_text} | {phase7g_text} | {row['rmse_deg']:.4f} | {delta_phase7g_text} |"
                )
            lines.append("")

        if coherent_fixed_rows:
            lines.append("## Coherent Fixed-Gap Grid")
            lines.append("")
            lines.append("| Gap (deg) | SNR (dB) | RMSE (deg) | Delta vs Phase 7G | Delta vs Phase 7F | Avg runtime / sample (s) |")
            lines.append("| ---: | ---: | ---: | ---: | ---: | ---: |")
            for row in coherent_fixed_rows:
                lines.append(
                    f"| {row.get('gap_deg', '')} | {row.get('snr_db', '')} | {row['rmse_deg']:.4f} | "
                    f"{format_float(row.get('delta_vs_phase7g_reference_rmse_deg')) if row.get('delta_vs_phase7g_reference_rmse_deg') is not None else 'missing'} | "
                    f"{format_float(row.get('delta_vs_phase7f_reference_rmse_deg')) if row.get('delta_vs_phase7f_reference_rmse_deg') is not None else 'missing'} | "
                    f"{row['avg_runtime_sec']:.6f} |"
                )
            lines.append("")

        if noncoherent_fixed_rows:
            lines.append("## Non-Coherent Fixed-Gap Grid")
            lines.append("")
            lines.append("| Gap (deg) | SNR (dB) | RMSE (deg) | Delta vs Phase 7G | Delta vs Phase 7F | Avg runtime / sample (s) |")
            lines.append("| ---: | ---: | ---: | ---: | ---: | ---: |")
            for row in noncoherent_fixed_rows:
                lines.append(
                    f"| {row.get('gap_deg', '')} | {row.get('snr_db', '')} | {row['rmse_deg']:.4f} | "
                    f"{format_float(row.get('delta_vs_phase7g_reference_rmse_deg')) if row.get('delta_vs_phase7g_reference_rmse_deg') is not None else 'missing'} | "
                    f"{format_float(row.get('delta_vs_phase7f_reference_rmse_deg')) if row.get('delta_vs_phase7f_reference_rmse_deg') is not None else 'missing'} | "
                    f"{row['avg_runtime_sec']:.6f} |"
                )
            lines.append("")

        if coherent_random_rows:
            lines.append("## Coherent Random-Gap Table")
            lines.append("")
            lines.append(
                "| SNR (dB) | Phase 7H RMSE (deg) | Phase 7I RMSE (deg) | Delta vs Phase 7H | Mean gap (deg) | Median gap (deg) | Min gap (deg) | Max gap (deg) |"
            )
            lines.append("| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
            for row in coherent_random_rows:
                lines.append(
                    f"| {row.get('snr_db', '')} | {format_float(row.get('phase7h_reference_rmse_deg')) if row.get('phase7h_reference_rmse_deg') is not None else 'missing'} | {row['rmse_deg']:.4f} | "
                    f"{format_float(row.get('delta_vs_phase7h_reference_rmse_deg')) if row.get('delta_vs_phase7h_reference_rmse_deg') is not None else 'missing'} | "
                    f"{format_float(row.get('realized_mean_gap_deg'))} | {format_float(row.get('realized_median_gap_deg'))} | "
                    f"{format_float(row.get('realized_min_gap_deg'))} | {format_float(row.get('realized_max_gap_deg'))} |"
                )
            lines.append("")

        if noncoherent_random_rows:
            lines.append("## Non-Coherent Random-Gap Table")
            lines.append("")
            lines.append(
                "| SNR (dB) | Phase 7H RMSE (deg) | Phase 7I RMSE (deg) | Delta vs Phase 7H | Mean gap (deg) | Median gap (deg) | Min gap (deg) | Max gap (deg) |"
            )
            lines.append("| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
            for row in noncoherent_random_rows:
                lines.append(
                    f"| {row.get('snr_db', '')} | {format_float(row.get('phase7h_reference_rmse_deg')) if row.get('phase7h_reference_rmse_deg') is not None else 'missing'} | {row['rmse_deg']:.4f} | "
                    f"{format_float(row.get('delta_vs_phase7h_reference_rmse_deg')) if row.get('delta_vs_phase7h_reference_rmse_deg') is not None else 'missing'} | "
                    f"{format_float(row.get('realized_mean_gap_deg'))} | {format_float(row.get('realized_median_gap_deg'))} | "
                    f"{format_float(row.get('realized_min_gap_deg'))} | {format_float(row.get('realized_max_gap_deg'))} |"
                )
            lines.append("")

        lines.append("## Bucket Summary")
        lines.append("")
        lines.append(
            "| Bucket | Cells | Mean RMSE (deg) | Median RMSE (deg) | Best RMSE (deg) | Worst RMSE (deg) | Mean runtime / sample (s) |"
        )
        lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
        for row in bucket_rows:
            lines.append(
                f"| {row['bucket_name']} | {row['num_cells']} | {row['mean_rmse_deg']:.4f} | "
                f"{row['median_rmse_deg']:.4f} | {row['best_rmse_deg']:.4f} | "
                f"{row['worst_rmse_deg']:.4f} | {row['mean_runtime_sec']:.6f} |"
            )
        output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return

    if report.get("random_gap_mode", False):
        coherent_rows = [row for row in rows if row.get("coherence") == "coherent"]
        noncoherent_rows = [
            row for row in rows if row.get("coherence") == "non-coherent"
        ]
        coherent_rows.sort(key=lambda row: row.get("snr_db", 0))
        noncoherent_rows.sort(key=lambda row: row.get("snr_db", 0))

        lines = [f"# {report.get('markdown_title', 'Transfer Test Results')}", ""]
        description = report.get("markdown_description", "")
        if description:
            lines.extend([description, ""])
        conditions = report.get("markdown_conditions", [])
        if conditions:
            lines.append("Experimental conditions:")
            for condition in conditions:
                lines.append(f"- {condition}")
            lines.append("")
        lines.append(f"Reference anchor RMSE: `{source_train_rmse:.4f} deg`")
        lines.append("")

        if coherent_rows:
            lines.append("## Coherent Random-Gap Table")
            lines.append("")
            lines.append(
                "| SNR (dB) | RMSE (deg) | Avg runtime / sample (s) | Mean gap (deg) | Median gap (deg) | Min gap (deg) | Max gap (deg) | Samples |"
            )
            lines.append(
                "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"
            )
            for row in coherent_rows:
                lines.append(
                    f"| {row.get('snr_db', '')} | {row['rmse_deg']:.4f} | {row['avg_runtime_sec']:.6f} | "
                    f"{format_float(row.get('realized_mean_gap_deg'))} | {format_float(row.get('realized_median_gap_deg'))} | "
                    f"{format_float(row.get('realized_min_gap_deg'))} | {format_float(row.get('realized_max_gap_deg'))} | "
                    f"{row.get('num_test_samples', '')} |"
                )
            lines.append("")

        if noncoherent_rows:
            lines.append("## Non-Coherent Random-Gap Table")
            lines.append("")
            lines.append(
                "| SNR (dB) | RMSE (deg) | Avg runtime / sample (s) | Mean gap (deg) | Median gap (deg) | Min gap (deg) | Max gap (deg) | Samples |"
            )
            lines.append(
                "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"
            )
            for row in noncoherent_rows:
                lines.append(
                    f"| {row.get('snr_db', '')} | {row['rmse_deg']:.4f} | {row['avg_runtime_sec']:.6f} | "
                    f"{format_float(row.get('realized_mean_gap_deg'))} | {format_float(row.get('realized_median_gap_deg'))} | "
                    f"{format_float(row.get('realized_min_gap_deg'))} | {format_float(row.get('realized_max_gap_deg'))} | "
                    f"{row.get('num_test_samples', '')} |"
                )
            lines.append("")

        lines.extend(["## Bucket Summary", ""])
        lines.append(
            "| Bucket | Cells | Mean RMSE (deg) | Median RMSE (deg) | Best RMSE (deg) | Worst RMSE (deg) | Mean runtime / sample (s) |"
        )
        lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
        for row in bucket_rows:
            lines.append(
                f"| {row['bucket_name']} | {row['num_cells']} | {row['mean_rmse_deg']:.4f} | "
                f"{row['median_rmse_deg']:.4f} | {row['best_rmse_deg']:.4f} | "
                f"{row['worst_rmse_deg']:.4f} | {row['mean_runtime_sec']:.6f} |"
            )
        output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return

    coherent_rows = [row for row in rows if row.get("coherence") == "coherent"]
    noncoherent_rows = [row for row in rows if row.get("coherence") == "non-coherent"]
    coherent_rows.sort(key=row_sort_key)
    noncoherent_rows.sort(key=row_sort_key)

    lines = [f"# {report.get('markdown_title', 'Transfer Test Results')}", ""]
    description = report.get("markdown_description", "")
    if description:
        lines.extend([description, ""])
    conditions = report.get("markdown_conditions", [])
    if conditions:
        lines.append("Experimental conditions:")
        for condition in conditions:
            lines.append(f"- {condition}")
        lines.append("")
    lines.append(f"Reference anchor RMSE: `{source_train_rmse:.4f} deg`")
    lines.append("")
    boundary_rows = [
        row
        for row in coherent_rows
        if int(row.get("gap_deg", 0)) == 2
    ]
    boundary_rows = [
        row for row in boundary_rows if row.get("phase7f_reference_rmse_deg") is not None
    ]
    boundary_baseline_label = report.get("boundary_baseline_label", "Phase 7F")
    boundary_current_label = report.get("boundary_current_label", "Current")
    if boundary_rows:
        lines.append("## Coherent 2-Degree Boundary")
        lines.append("")
        lines.append(
            f"| SNR (dB) | {boundary_baseline_label} RMSE (deg) | {boundary_current_label} RMSE (deg) | Delta vs {boundary_baseline_label} |"
        )
        lines.append("| ---: | ---: | ---: | ---: |")
        for row in boundary_rows:
            phase7f_text = (
                f"{row['phase7f_reference_rmse_deg']:.4f}"
                if row.get("phase7f_reference_rmse_deg") is not None
                else "missing"
            )
            delta_phase7f_text = (
                f"{row['delta_vs_phase7f_reference_rmse_deg']:+.4f}"
                if row.get("delta_vs_phase7f_reference_rmse_deg") is not None
                else "missing"
            )
            lines.append(
                f"| {row.get('snr_db', '')} | {phase7f_text} | {row['rmse_deg']:.4f} | {delta_phase7f_text} |"
            )
        lines.append("")
    lines.append("## Coherent Reused Grid")
    lines.append("")
    lines.append("| Gap (deg) | SNR (dB) | RMSE (deg) | Avg runtime / sample (s) | Delta vs anchor | Delta vs classical best | Delta vs direct learned | Delta vs Phase 7E | Delta vs Phase 7F | Cache status |")
    lines.append("| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |")
    for row in coherent_rows:
        lines.append(
            f"| {row.get('gap_deg', '')} | {row.get('snr_db', '')} | {row['rmse_deg']:.4f} | "
            f"{row['avg_runtime_sec']:.6f} | {row['delta_vs_source_train_cell_rmse_deg']:+.4f} | "
            f"{format_float(row['delta_vs_phase6_classical_best_rmse_deg']) if row['delta_vs_phase6_classical_best_rmse_deg'] is not None else 'missing'} | "
            f"{format_float(row['delta_vs_phase6_direct_learned_rmse_deg']) if row['delta_vs_phase6_direct_learned_rmse_deg'] is not None else 'missing'} | "
            f"{format_float(row['delta_vs_phase7e_reference_rmse_deg']) if row.get('delta_vs_phase7e_reference_rmse_deg') is not None else 'missing'} | "
            f"{format_float(row['delta_vs_phase7f_reference_rmse_deg']) if row.get('delta_vs_phase7f_reference_rmse_deg') is not None else 'missing'} | "
            f"{row.get('dataset_cache_status', 'unknown')} |"
        )
    lines.extend(["", "## Non-Coherent Reused Grid", ""])
    lines.append("| Gap (deg) | SNR (dB) | RMSE (deg) | Avg runtime / sample (s) | Delta vs anchor | Delta vs classical best | Delta vs direct learned | Delta vs Phase 7E | Delta vs Phase 7F | Cache status |")
    lines.append("| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |")
    for row in noncoherent_rows:
        lines.append(
            f"| {row.get('gap_deg', '')} | {row.get('snr_db', '')} | {row['rmse_deg']:.4f} | "
            f"{row['avg_runtime_sec']:.6f} | {row['delta_vs_source_train_cell_rmse_deg']:+.4f} | "
            f"{format_float(row['delta_vs_phase6_classical_best_rmse_deg']) if row['delta_vs_phase6_classical_best_rmse_deg'] is not None else 'missing'} | "
            f"{format_float(row['delta_vs_phase6_direct_learned_rmse_deg']) if row['delta_vs_phase6_direct_learned_rmse_deg'] is not None else 'missing'} | "
            f"{format_float(row['delta_vs_phase7e_reference_rmse_deg']) if row.get('delta_vs_phase7e_reference_rmse_deg') is not None else 'missing'} | "
            f"{format_float(row['delta_vs_phase7f_reference_rmse_deg']) if row.get('delta_vs_phase7f_reference_rmse_deg') is not None else 'missing'} | "
            f"{row.get('dataset_cache_status', 'unknown')} |"
        )
    retention_rows = [
        row
        for row in rows
        if row.get("split") == "in_domain_anchor"
        or bool(row.get("retention_priority"))
    ]
    if retention_rows:
        lines.extend(["", "## Retention Table", ""])
        lines.append("| Cell | RMSE (deg) | Delta vs anchor | Delta vs Phase 7E | Delta vs Phase 7F |")
        lines.append("| --- | ---: | ---: | ---: | ---: |")
        for row in retention_rows:
            cell_label = f"{row.get('coherence', 'unknown')} | gap {row.get('gap_deg', '?')} | snr {row.get('snr_db', '?')}"
            lines.append(
                f"| {cell_label} | {row['rmse_deg']:.4f} | {row['delta_vs_source_train_cell_rmse_deg']:+.4f} | "
                f"{format_float(row['delta_vs_phase7e_reference_rmse_deg']) if row.get('delta_vs_phase7e_reference_rmse_deg') is not None else 'missing'} | "
                f"{format_float(row['delta_vs_phase7f_reference_rmse_deg']) if row.get('delta_vs_phase7f_reference_rmse_deg') is not None else 'missing'} |"
            )
    lines.extend(["", "## Bucket Summary", ""])
    lines.append("| Bucket | Cells | Mean RMSE (deg) | Median RMSE (deg) | Best RMSE (deg) | Worst RMSE (deg) | Mean runtime / sample (s) |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for row in bucket_rows:
        lines.append(
            f"| {row['bucket_name']} | {row['num_cells']} | {row['mean_rmse_deg']:.4f} | "
            f"{row['median_rmse_deg']:.4f} | {row['best_rmse_deg']:.4f} | "
            f"{row['worst_rmse_deg']:.4f} | {row['mean_runtime_sec']:.6f} |"
        )
    lines.extend(["", "## Comparison Table", ""])
    lines.append("| Cell | Phase 6 classical best | RMSE (deg) | Avg runtime / sample (s) | Delta vs classical best | Direct Phase 6 learned RMSE (deg) | Delta vs direct learned | Phase 7E RMSE (deg) | Delta vs Phase 7E | Phase 7F RMSE (deg) | Delta vs Phase 7F |")
    lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for row in sorted(rows, key=row_sort_key):
        cell_label = f"{row.get('coherence', 'unknown')} | gap {row.get('gap_deg', '?')} | snr {row.get('snr_db', '?')}"
        classical_label = (
            f"{row['phase6_classical_best_method']} ({row['phase6_classical_best_rmse_deg']:.4f})"
            if row.get("phase6_classical_best_method") is not None
            else "missing"
        )
        direct_learned_text = (
            f"{row['phase6_direct_learned_rmse_deg']:.4f}"
            if row.get("phase6_direct_learned_rmse_deg") is not None
            else "missing"
        )
        delta_direct_text = (
            f"{row['delta_vs_phase6_direct_learned_rmse_deg']:+.4f}"
            if row.get("delta_vs_phase6_direct_learned_rmse_deg") is not None
            else "missing"
        )
        delta_classical_text = (
            f"{row['delta_vs_phase6_classical_best_rmse_deg']:+.4f}"
            if row.get("delta_vs_phase6_classical_best_rmse_deg") is not None
            else "missing"
        )
        phase7e_text = (
            f"{row['phase7e_reference_rmse_deg']:.4f}"
            if row.get("phase7e_reference_rmse_deg") is not None
            else "missing"
        )
        delta_phase7e_text = (
            f"{row['delta_vs_phase7e_reference_rmse_deg']:+.4f}"
            if row.get("delta_vs_phase7e_reference_rmse_deg") is not None
            else "missing"
        )
        phase7f_text = (
            f"{row['phase7f_reference_rmse_deg']:.4f}"
            if row.get("phase7f_reference_rmse_deg") is not None
            else "missing"
        )
        delta_phase7f_text = (
            f"{row['delta_vs_phase7f_reference_rmse_deg']:+.4f}"
            if row.get("delta_vs_phase7f_reference_rmse_deg") is not None
            else "missing"
        )
        lines.append(
            f"| {cell_label} | {classical_label} | {row['rmse_deg']:.4f} | "
            f"{row['avg_runtime_sec']:.6f} | {delta_classical_text} | "
            f"{direct_learned_text} | {delta_direct_text} | {phase7e_text} | {delta_phase7e_text} | {phase7f_text} | {delta_phase7f_text} |"
        )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_subspacenet_transfer_test(repo_root: Path, template: Dict, results_root: Path):
    seed = template.get("seed", 42)
    print(f"\nStarting test experiment {template['template_name']}")
    set_unified_seed(seed)
    commands = template.get("commands", {})
    report = template.get("report", {})
    flat_results_root = bool(report.get("flat_results_root", False))
    experiment_root = results_root if flat_results_root else results_root / template["template_name"]
    ensure_dirs(experiment_root)
    save_json(experiment_root / "resolved_test_template.json", template)

    model, source_template, source_metrics, checkpoint_path = resolve_source_model(
        repo_root=repo_root,
        source_model_config=template["source_model"],
    )
    source_train_rmse = float(source_metrics["rmse_deg"])
    reference_anchor_rmse = float(
        template.get("source_model", {}).get("reference_rmse_deg", source_train_rmse)
    )
    tau = int(source_template["model"]["tau"])
    model_type = source_template["model"]["model_type"]
    reference_maps = build_reference_maps(template.get("reference_sources"))

    save_json(experiment_root / "source_model_info.json", {
        "checkpoint_path": str(checkpoint_path),
        "source_train_rmse_deg": source_train_rmse,
        "reference_anchor_rmse_deg": reference_anchor_rmse,
        "source_template_name": source_template.get("template_name"),
        "source_model_type": model_type,
    })

    rows = []
    for cell_config in template.get("evaluation_cells", []):
        cell_template_path = Path(cell_config["template_path"])
        if not cell_template_path.is_absolute():
            cell_template_path = (repo_root / cell_template_path).resolve()
        source_cell_template = load_json(cell_template_path)
        source_cell_template["template_name"] = cell_template_path.stem
        generic_test_dataset, _, system_model_params, datasets_path, cache_status = (
            prepare_generic_test_dataset(
                repo_root=repo_root,
                source_template=source_cell_template,
                commands=commands,
            )
        )
        method_name = cell_config.get("method_name", "esprit")
        cell_dir = experiment_root / cell_config["result_name"] / method_name
        ensure_dirs(cell_dir)
        save_json(cell_dir / "resolved_source_template.json", source_cell_template)

        metrics = evaluate_transfer_cell(
            model=model,
            generic_test_dataset=generic_test_dataset,
            system_model_params=system_model_params,
            model_type=model_type,
            tau=tau,
            cell_config=cell_config,
            result_dir=cell_dir,
        )
        gap_stats = compute_realized_gap_stats(generic_test_dataset)

        classical_best_method, classical_best_rmse, direct_learned_rmse = (
            get_reference_metrics(reference_maps, cell_config)
        )
        phase7e_reference_rmse = None
        reference_schemes = cell_config.get("reference_schemes", {})
        if reference_schemes.get("phase7e"):
            phase7e_reference_rmse = get_named_reference_rmse(
                reference_maps,
                summary_key="phase7e",
                scheme_name=reference_schemes["phase7e"],
                method_name=method_name,
            )
        phase7f_reference_rmse = None
        if reference_schemes.get("phase7f"):
            phase7f_reference_rmse = get_named_reference_rmse(
                reference_maps,
                summary_key="phase7f",
                scheme_name=reference_schemes["phase7f"],
                method_name=method_name,
            )
        phase7g_reference_rmse = None
        if reference_schemes.get("phase7g"):
            phase7g_reference_rmse = get_named_reference_rmse(
                reference_maps,
                summary_key="phase7g",
                scheme_name=reference_schemes["phase7g"],
                method_name=method_name,
            )
        phase7h_reference_rmse = None
        if reference_schemes.get("phase7h"):
            phase7h_reference_rmse = get_named_reference_rmse(
                reference_maps,
                summary_key="phase7h",
                scheme_name=reference_schemes["phase7h"],
                method_name=method_name,
            )
        row = {
            "scheme": cell_config["result_name"],
            "method": method_name,
            "coherence": cell_config.get("coherence_label"),
            "gap_deg": cell_config.get("gap_deg"),
            "snr_db": cell_config.get("snr_db"),
            "split": cell_config.get("split"),
            "bucket_labels": "|".join(cell_config.get("bucket_labels", [])),
            "dataset_cache_status": cache_status,
            "dataset_path": str(datasets_path),
            "rmse_deg": metrics["rmse_deg"],
            "avg_runtime_sec": metrics["avg_runtime_sec"],
            "avg_preprocess_runtime_sec": metrics["avg_preprocess_runtime_sec"],
            "avg_forward_runtime_sec": metrics["avg_forward_runtime_sec"],
            "dataset_pass_runtime_sec": metrics["dataset_pass_runtime_sec"],
            "num_test_samples": metrics["num_test_samples"],
            "realized_mean_gap_deg": gap_stats.get("realized_mean_gap_deg"),
            "realized_median_gap_deg": gap_stats.get("realized_median_gap_deg"),
            "realized_min_gap_deg": gap_stats.get("realized_min_gap_deg"),
            "realized_max_gap_deg": gap_stats.get("realized_max_gap_deg"),
            "delta_vs_source_train_cell_rmse_deg": metrics["rmse_deg"] - reference_anchor_rmse,
            "phase6_classical_best_method": classical_best_method,
            "phase6_classical_best_rmse_deg": classical_best_rmse,
            "delta_vs_phase6_classical_best_rmse_deg": (
                None if classical_best_rmse is None else metrics["rmse_deg"] - classical_best_rmse
            ),
            "phase6_direct_learned_rmse_deg": direct_learned_rmse,
            "delta_vs_phase6_direct_learned_rmse_deg": (
                None if direct_learned_rmse is None else metrics["rmse_deg"] - direct_learned_rmse
            ),
            "phase7e_reference_rmse_deg": phase7e_reference_rmse,
            "delta_vs_phase7e_reference_rmse_deg": (
                None if phase7e_reference_rmse is None else metrics["rmse_deg"] - phase7e_reference_rmse
            ),
            "phase7f_reference_rmse_deg": phase7f_reference_rmse,
            "delta_vs_phase7f_reference_rmse_deg": (
                None if phase7f_reference_rmse is None else metrics["rmse_deg"] - phase7f_reference_rmse
            ),
            "phase7g_reference_rmse_deg": phase7g_reference_rmse,
            "delta_vs_phase7g_reference_rmse_deg": (
                None if phase7g_reference_rmse is None else metrics["rmse_deg"] - phase7g_reference_rmse
            ),
            "phase7h_reference_rmse_deg": phase7h_reference_rmse,
            "delta_vs_phase7h_reference_rmse_deg": (
                None if phase7h_reference_rmse is None else metrics["rmse_deg"] - phase7h_reference_rmse
            ),
            "retention_priority": bool(cell_config.get("retention_priority", False)),
        }
        save_json(cell_dir / "metrics.json", {**metrics, **row})
        rows.append(row)

    rows.sort(key=row_sort_key)
    bucket_rows = build_bucket_summary(rows)
    if report.get("write_summary_csv", False):
        write_summary_csv(rows, experiment_root / "summary.csv")
        write_bucket_summary_csv(
            bucket_rows,
            experiment_root / f"{template['template_name']}_bucket_summary.csv",
        )
    markdown_output = report.get("markdown_output")
    if markdown_output:
        write_transfer_markdown(
            rows=rows,
            bucket_rows=bucket_rows,
            output_path=experiment_root / markdown_output,
            report=report,
            source_train_rmse=reference_anchor_rmse,
        )
    return rows


def run_test_experiment(repo_root: Path, template: Dict, results_root: Path):
    experiment_type = template.get("experiment_type")
    if experiment_type == "subspacenet_transfer_test":
        return run_subspacenet_transfer_test(repo_root, template, results_root)
    raise ValueError(f"Unsupported test experiment type: {experiment_type}")


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    templates_dir = (repo_root / args.templates_dir).resolve()
    results_root = (repo_root / args.results_dir).resolve()
    ensure_dirs(results_root)

    templates = load_templates(templates_dir)
    selected_templates = select_templates(templates, args.experiments)
    for template in selected_templates:
        apply_overrides(template, args)

    all_results = []
    for template in selected_templates:
        all_results.extend(run_test_experiment(repo_root, template, results_root))

    if all_results:
        print("\nTest summary (RMSE deg):")
        for item in all_results:
            print(f"- {item['scheme']} / {item['method']}: {item['rmse_deg']:.4f} deg")


if __name__ == "__main__":
    main()
