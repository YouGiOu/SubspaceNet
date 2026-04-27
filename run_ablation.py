"""Run strict ablation experiments for DOA estimation schemes."""

from __future__ import annotations

import argparse
import copy
import csv
import json
import time
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
from tqdm import tqdm

from src.criterions import RMSPELoss
from src.data_handler import create_dataset, create_mixed_dataset, load_datasets, load_mixed_datasets
from src.dataset_template import build_system_model_params_from_template
from src.methods import DBF, Esprit, MUSIC, RootMUSIC
from src.models import ModelGenerator
from src.training import TrainingParams, get_simulation_filename, train
from src.utils import R2D, set_unified_seed


TRADITIONAL_METHODS = {
    "dbf": DBF,
    "music": MUSIC,
    "esprit": Esprit,
    "root-music": RootMUSIC,
    "r-music": RootMUSIC,
}


METHOD_MARKDOWN_LABELS = {
    "dbf": "DBF",
    "music": "MUSIC",
    "esprit": "ESPRIT",
    "root-music": "Root-MUSIC",
    "r-music": "Root-MUSIC",
}


def parse_args():
    parser = argparse.ArgumentParser(description="Run DOA ablation experiments.")
    parser.add_argument(
        "--templates-dir",
        default="data/dataset_templates/ablation",
        help="Directory containing ablation JSON templates.",
    )
    parser.add_argument(
        "--experiments",
        default="all",
        help="Comma-separated list of experiment template names to run, or 'all'.",
    )
    parser.add_argument("--snr", type=float, default=None, help="Override SNR for all runs.")
    parser.add_argument(
        "--snapshots", type=int, default=None, help="Override T (number of snapshots)."
    )
    parser.add_argument(
        "--tau", type=int, default=None, help="Override tau for all SubspaceNet runs."
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Override random seed for reproducible fair comparison.",
    )
    parser.add_argument(
        "--results-dir",
        default="results/ablation",
        help="Root directory for ablation outputs.",
    )
    return parser.parse_args()


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
        raise ValueError(f"Unknown experiment template(s): {missing}")
    return [copy.deepcopy(all_templates[name]) for name in names]


def apply_overrides(template: Dict, args):
    system_model = template.setdefault("system_model", {})
    model = template.setdefault("model", {})
    if args.snr is not None:
        system_model["snr"] = args.snr
    if args.snapshots is not None:
        system_model["T"] = args.snapshots
    if args.tau is not None:
        model["tau"] = args.tau
    if args.seed is not None:
        template["seed"] = args.seed


def normalize_subspacenet_seeds(templates: Iterable[Dict], shared_seed: Optional[int]):
    subspacenet_templates = [
        template
        for template in templates
        if template.get("experiment_type") == "subspacenet"
    ]
    if not subspacenet_templates:
        return
    if shared_seed is None:
        shared_seed = subspacenet_templates[0].get("seed", 42)
    for template in subspacenet_templates:
        template["seed"] = shared_seed


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


def load_existing_result(result_dir: Path, template: Dict, method_name: str) -> Optional[Dict]:
    metrics_path = result_dir / "metrics.json"
    if not metrics_path.exists():
        return None
    try:
        with metrics_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except Exception:
        return None
    rmse_deg = payload.get("rmse_deg")
    if rmse_deg is None:
        return None
    result = {
        "scheme": template["template_name"],
        "method": method_name,
        "rmse_deg": float(rmse_deg),
        "avg_runtime_sec": payload.get("avg_runtime_sec"),
        "avg_lrmc_runtime_sec": payload.get("avg_lrmc_runtime_sec"),
        "avg_lrmc_iterations": payload.get("avg_lrmc_iterations"),
        "lrmc_convergence_rate": payload.get("lrmc_convergence_rate"),
        "avg_lrmc_final_residual": payload.get("avg_lrmc_final_residual"),
        "min_lrmc_eigenvalue": payload.get("min_lrmc_eigenvalue"),
        "min_lrmc_singular_value": payload.get("min_lrmc_singular_value"),
    }
    print(
        f"Skipping completed method for {template['template_name']} / {method_name} "
        f"using existing metrics at {metrics_path}"
    )
    return result


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


def prepare_datasets(
    repo_root: Path,
    template: Dict,
    model_type: str,
    tau: int,
    need_training_split: bool,
):
    commands = template["commands"]
    dataset_settings = template["dataset"]
    scenario_data_path = template.get("scenario_data_path", template["template_name"])
    datasets_path = repo_root / "data" / "datasets" / scenario_data_path
    ensure_dirs(datasets_path, datasets_path / "train", datasets_path / "test")

    system_model_params = build_system_model_params_from_template(template)
    system_model_params.set_parameter("template_name", template["template_name"])
    samples_size = dataset_settings["samples_size"]
    train_test_ratio = dataset_settings["train_test_ratio"]
    mixed_dataset_config = dataset_settings.get("mixed_dataset")

    if mixed_dataset_config is not None:
        force_recreate = bool(commands.get("FORCE_RECREATE_DATA", False))
        prefer_cached_data = bool(
            commands.get("LOAD_DATA", False)
            or commands.get("CACHE_DATASET", False)
            or commands.get("CREATE_DATA", False)
        ) and not force_recreate

        loaded = None
        if prefer_cached_data:
            try:
                loaded = load_mixed_datasets(
                    system_model_params=system_model_params,
                    model_type=model_type,
                    tau=tau,
                    dataset_settings=dataset_settings,
                    datasets_path=datasets_path,
                    is_training=need_training_split,
                )
                print(
                    f"Using cached mixed dataset for {template['template_name']} from {datasets_path}"
                )
            except Exception:
                loaded = None

        if loaded is None and commands.get("LOAD_DATA", False) and not commands.get(
            "CREATE_DATA", False
        ):
            raise Exception(
                f"prepare_datasets: cached mixed dataset requested for {template['template_name']}, but it does not exist"
            )

        if loaded is None and commands.get("CREATE_DATA", False):
            (
                train_dataset,
                test_dataset,
                generic_test_dataset,
                samples_model,
            ) = create_mixed_dataset(
                system_model_params=system_model_params,
                dataset_settings=dataset_settings,
                model_type=model_type,
                tau=tau,
                save_datasets=True,
                datasets_path=datasets_path,
            )
            if not need_training_split:
                train_dataset = None
            return train_dataset, test_dataset, generic_test_dataset, samples_model, datasets_path

        if loaded is None:
            loaded = load_mixed_datasets(
                system_model_params=system_model_params,
                model_type=model_type,
                tau=tau,
                dataset_settings=dataset_settings,
                datasets_path=datasets_path,
                is_training=need_training_split,
            )

        if need_training_split:
            train_dataset, test_dataset, generic_test_dataset, samples_model = loaded
        else:
            test_dataset, generic_test_dataset, samples_model = loaded
            train_dataset = None
        return train_dataset, test_dataset, generic_test_dataset, samples_model, datasets_path

    force_recreate = bool(commands.get("FORCE_RECREATE_DATA", False))
    prefer_cached_data = bool(
        commands.get("LOAD_DATA", False)
        or commands.get("CACHE_DATASET", False)
        or commands.get("CREATE_DATA", False)
    ) and not force_recreate

    loaded = None
    if prefer_cached_data:
        try:
            loaded = load_datasets(
                system_model_params=system_model_params,
                model_type=model_type,
                samples_size=samples_size,
                datasets_path=datasets_path,
                train_test_ratio=train_test_ratio,
                is_training=need_training_split,
            )
            print(
                f"Using cached dataset for {template['template_name']} from {datasets_path}"
            )
        except Exception:
            loaded = None

    if loaded is None and commands.get("LOAD_DATA", False) and not commands.get("CREATE_DATA", False):
        raise Exception(
            f"prepare_datasets: cached dataset requested for {template['template_name']}, but it does not exist"
        )

    if loaded is None and commands.get("CREATE_DATA", False):
        train_dataset = None
        if need_training_split:
            train_dataset, _, _ = create_dataset(
                system_model_params=system_model_params,
                samples_size=samples_size,
                model_type=model_type,
                tau=tau,
                save_datasets=True,
                datasets_path=datasets_path,
                true_doa=None,
                phase="train",
            )
        test_dataset, generic_test_dataset, samples_model = create_dataset(
            system_model_params=system_model_params,
            samples_size=int(train_test_ratio * samples_size),
            model_type=model_type,
            tau=tau,
            save_datasets=True,
            datasets_path=datasets_path,
            true_doa=None,
            phase="test",
        )
        return train_dataset, test_dataset, generic_test_dataset, samples_model, datasets_path

    if loaded is None:
        loaded = load_datasets(
            system_model_params=system_model_params,
            model_type=model_type,
            samples_size=samples_size,
            datasets_path=datasets_path,
            train_test_ratio=train_test_ratio,
            is_training=need_training_split,
        )

    if need_training_split:
        train_dataset, test_dataset, generic_test_dataset, samples_model = loaded
    else:
        test_dataset, generic_test_dataset, samples_model = loaded
        train_dataset = None
    return train_dataset, test_dataset, generic_test_dataset, samples_model, datasets_path


def resolve_pretrained_checkpoint(repo_root: Path, training_settings: Dict):
    experiment_dir_value = training_settings.get("pretrained_experiment_dir")
    if not experiment_dir_value:
        return None
    experiment_dir = Path(experiment_dir_value)
    if not experiment_dir.is_absolute():
        experiment_dir = (repo_root / experiment_dir).resolve()
    method_name = training_settings.get("pretrained_method_name", "esprit")
    resolved_template_path = experiment_dir / "resolved_template.json"
    metrics_path = experiment_dir / method_name / "metrics.json"
    metrics = load_json(metrics_path)
    checkpoint_dir = Path(metrics["checkpoint_dir"])
    if not checkpoint_dir.is_absolute():
        checkpoint_dir = checkpoint_dir.resolve()
    source_template = load_json(resolved_template_path)
    source_system_model_params = build_system_model_params_from_template(source_template)
    source_system_model_params.set_parameter(
        "template_name", source_template["template_name"]
    )
    source_model_config = (
        ModelGenerator()
        .set_model_type(source_template["model"]["model_type"])
        .set_diff_method(source_template["model"]["diff_method"])
        .set_tau(int(source_template["model"]["tau"]))
        .set_model(source_system_model_params)
    )
    checkpoint_name = get_simulation_filename(
        source_system_model_params, source_model_config
    )
    checkpoint_path = checkpoint_dir / checkpoint_name
    if not checkpoint_path.exists():
        candidates = [path for path in checkpoint_dir.iterdir() if path.is_file()]
        if not candidates:
            raise FileNotFoundError(f"No checkpoint files found in {checkpoint_dir}")
        candidates.sort(key=lambda path: path.stat().st_mtime, reverse=True)
        checkpoint_path = candidates[0]
    return checkpoint_path


def plot_loss_curves(train_loss: List[float], valid_loss: List[float], output_path: Path):
    plt.figure(figsize=(8, 5))
    plt.plot(range(1, len(train_loss) + 1), train_loss, label="train")
    plt.plot(range(1, len(valid_loss) + 1), valid_loss, label="validation")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Training Convergence")
    plt.legend(loc="best")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def run_traditional_method(
    method_name: str,
    method_class,
    generic_test_dataset: List,
    system_model,
    result_dir: Path,
    template: Dict,
):
    method = method_class(system_model)
    system_model_config = template.get("system_model", {})
    method_mode = system_model_config.get("covariance_mode")
    if not method_mode:
        method_mode = "lrmc" if system_model_config.get("use_lrmc", False) else "sample"
    per_sample_rmse = []
    per_sample_runtime = []
    lrmc_runtimes = []
    lrmc_iterations = []
    lrmc_convergence = []
    lrmc_residuals = []
    lrmc_min_eigenvalues = []
    lrmc_min_singular_values = []
    progress = tqdm(
        generic_test_dataset,
        total=len(generic_test_dataset),
        desc=f"{template['template_name']}::{method_name}",
    )
    for X, doa in progress:
        observations = np.asarray(X)
        doa_deg = np.asarray(doa) * R2D
        start = time.perf_counter()
        if method_name == "dbf":
            predictions, spectrum, _ = method.narrowband(observations, mode=method_mode)
        elif method_name == "music":
            predictions, spectrum, _ = method.narrowband(observations, mode=method_mode)
        elif method_name in {"r-music", "root-music"}:
            predictions, roots, predictions_all, roots_angles, _ = method.narrowband(
                observations, mode=method_mode
            )
            spectrum = None
        elif method_name == "esprit":
            predictions, _ = method.narrowband(observations, mode=method_mode)
            spectrum = None
        else:
            raise ValueError(f"Unsupported traditional method: {method_name}")
        per_sample_runtime.append(time.perf_counter() - start)
        diagnostics = getattr(method, "last_lrmc_diagnostics", None)
        if diagnostics is not None:
            lrmc_runtimes.append(float(getattr(diagnostics, "runtime_sec", 0.0)))
            lrmc_iterations.append(int(getattr(diagnostics, "iterations", 0)))
            lrmc_convergence.append(bool(getattr(diagnostics, "converged", False)))
            if getattr(diagnostics, "observed_residuals", None):
                lrmc_residuals.append(float(diagnostics.observed_residuals[-1]))
            if getattr(diagnostics, "min_eigenvalue", None) is not None:
                lrmc_min_eigenvalues.append(float(diagnostics.min_eigenvalue))
            if getattr(diagnostics, "min_singular_value", None) is not None:
                lrmc_min_singular_values.append(float(diagnostics.min_singular_value))
        per_sample_rmse.append(periodic_rmse_deg(predictions, doa_deg))

    rmse_deg = float(np.mean(per_sample_rmse))
    avg_runtime_sec = float(np.mean(per_sample_runtime)) if per_sample_runtime else None
    avg_lrmc_runtime_sec = float(np.mean(lrmc_runtimes)) if lrmc_runtimes else None
    avg_lrmc_iterations = float(np.mean(lrmc_iterations)) if lrmc_iterations else None
    lrmc_convergence_rate = float(np.mean(lrmc_convergence)) if lrmc_convergence else None
    avg_lrmc_residual = float(np.mean(lrmc_residuals)) if lrmc_residuals else None
    min_lrmc_eigenvalue = float(np.min(lrmc_min_eigenvalues)) if lrmc_min_eigenvalues else None
    min_lrmc_singular_value = float(np.min(lrmc_min_singular_values)) if lrmc_min_singular_values else None
    save_json(
        result_dir / "metrics.json",
        {
            "template_name": template["template_name"],
            "method_name": method_name,
            "rmse_deg": rmse_deg,
            "avg_runtime_sec": avg_runtime_sec,
            "avg_lrmc_runtime_sec": avg_lrmc_runtime_sec,
            "avg_lrmc_iterations": avg_lrmc_iterations,
            "lrmc_convergence_rate": lrmc_convergence_rate,
            "avg_lrmc_final_residual": avg_lrmc_residual,
            "min_lrmc_eigenvalue": min_lrmc_eigenvalue,
            "min_lrmc_singular_value": min_lrmc_singular_value,
            "num_test_samples": len(generic_test_dataset),
        },
    )
    return {
        "scheme": template["template_name"],
        "method": method_name,
        "rmse_deg": rmse_deg,
        "avg_runtime_sec": avg_runtime_sec,
        "avg_lrmc_runtime_sec": avg_lrmc_runtime_sec,
        "avg_lrmc_iterations": avg_lrmc_iterations,
        "lrmc_convergence_rate": lrmc_convergence_rate,
        "avg_lrmc_final_residual": avg_lrmc_residual,
        "min_lrmc_eigenvalue": min_lrmc_eigenvalue,
        "min_lrmc_singular_value": min_lrmc_singular_value,
    }


def evaluate_subspacenet_rmse_deg(model, test_dataset: List):
    model.eval()
    errors = []
    fusion_norms = []
    fusion_diag_means = []
    branch_norms = []
    with torch.no_grad():
        for X, doa in test_dataset:
            inputs = X.unsqueeze(0).to(next(model.parameters()).device)
            predictions_rad = model(inputs)[0].detach().cpu().numpy().squeeze()
            targets_deg = np.asarray(doa) * R2D
            predictions_deg = np.asarray(predictions_rad) * R2D
            errors.append(periodic_rmse_deg(predictions_deg, targets_deg))
            diagnostics = getattr(model, "last_fusion_diagnostics", None)
            if diagnostics is not None:
                if diagnostics.get("fused_covariance_norm") is not None:
                    fusion_norms.append(float(diagnostics["fused_covariance_norm"]))
                if diagnostics.get("fused_diagonal_mean_real") is not None:
                    fusion_diag_means.append(float(diagnostics["fused_diagonal_mean_real"]))
                if diagnostics.get("input_branch_norms") is not None:
                    branch_norms.append(list(diagnostics["input_branch_norms"]))
    summary = {}
    if fusion_norms:
        summary["avg_fused_covariance_norm"] = float(np.mean(fusion_norms))
    if fusion_diag_means:
        summary["avg_fused_diagonal_mean_real"] = float(np.mean(fusion_diag_means))
    if branch_norms:
        summary["avg_input_branch_norms"] = np.mean(np.asarray(branch_norms, dtype=float), axis=0).tolist()
    if getattr(model, "last_fusion_diagnostics", None) is not None:
        kernel_type = model.last_fusion_diagnostics.get("fusion_kernel_type")
        if kernel_type:
            summary["fusion_kernel_type"] = kernel_type
    if getattr(model, "backbone_kernel_size", None) is not None:
        summary["subspacenet_backbone_kernel_size"] = int(model.backbone_kernel_size)
    return float(np.mean(errors)), summary


def train_subspacenet_variant(
    repo_root: Path,
    template: Dict,
    method_name: str,
    result_dir: Path,
):
    seed = template.get("seed", 42)
    print(f"Starting experiment {template['template_name']} / {method_name}")
    set_unified_seed(seed)
    template = copy.deepcopy(template)
    template["model"]["diff_method"] = "root_music" if method_name == "root-music" else method_name
    system_model_params = build_system_model_params_from_template(template)
    system_model_params.set_parameter("template_name", template["template_name"])
    model_settings = template["model"]
    training_settings = template["training"]
    tau = model_settings["tau"]

    train_dataset, test_dataset, _, _, _ = prepare_datasets(
        repo_root=repo_root,
        template=template,
        model_type=model_settings["model_type"],
        tau=tau,
        need_training_split=True,
    )

    model_config = (
        ModelGenerator()
        .set_model_type(model_settings["model_type"])
        .set_diff_method(model_settings["diff_method"])
        .set_tau(tau)
        .set_model(system_model_params)
    )

    checkpoint_dir = result_dir / "checkpoints"
    ensure_dirs(checkpoint_dir)
    simulation_filename = get_simulation_filename(system_model_params, model_config)

    set_unified_seed(seed)
    simulation_parameters = (
        TrainingParams()
        .set_batch_size(training_settings["batch_size"])
        .set_validation_batch_size(training_settings.get("validation_batch_size"))
        .set_dataloader_options(
            num_workers=training_settings.get("num_workers", 0),
            pin_memory=training_settings.get("pin_memory"),
            persistent_workers=training_settings.get("persistent_workers"),
            prefetch_factor=training_settings.get("prefetch_factor"),
        )
        .set_epochs(training_settings["epochs"])
        .set_model(model=model_config)
        .set_optimizer(
            optimizer="Adam",
            learning_rate=training_settings["learning_rate"],
            weight_decay=training_settings["weight_decay"],
        )
        .set_training_dataset(train_dataset)
        .set_schedular(
            step_size=training_settings["scheduler_step_size"],
            gamma=training_settings["scheduler_gamma"],
        )
        .set_criterion()
    )
    pretrained_checkpoint = resolve_pretrained_checkpoint(repo_root, training_settings)
    if pretrained_checkpoint is not None:
        simulation_parameters.load_model(pretrained_checkpoint)

    model, train_loss, valid_loss = train(
        training_parameters=simulation_parameters,
        model_name=simulation_filename,
        plot_curves=False,
        saving_path=checkpoint_dir,
    )
    plot_loss_curves(train_loss, valid_loss, result_dir / "loss_curve.png")
    rmse_deg, model_eval_summary = evaluate_subspacenet_rmse_deg(model, test_dataset)
    save_json(
        result_dir / "metrics.json",
        {
            "template_name": template["template_name"],
            "method_name": method_name,
            "rmse_deg": rmse_deg,
            "seed": seed,
            "loss_measure": "rmse_deg",
            "train_loss": train_loss,
            "valid_loss": valid_loss,
            "checkpoint_dir": str(checkpoint_dir),
            "pretrained_checkpoint_path": (
                str(pretrained_checkpoint) if pretrained_checkpoint is not None else None
            ),
            **model_eval_summary,
        },
    )
    return {"scheme": template["template_name"], "method": method_name, "rmse_deg": rmse_deg}


def run_experiment(repo_root: Path, template: Dict, results_root: Path) -> List[Dict]:
    seed = template.get("seed", 42)
    print(f"\nStarting experiment {template['template_name']}")
    set_unified_seed(seed)
    system_model_params = build_system_model_params_from_template(template)
    system_model_params.set_parameter("template_name", template["template_name"])
    tau = template.get("model", {}).get("tau", 8)
    experiment_type = template["experiment_type"]
    methods = template.get("methods", [])
    if not methods:
        raise ValueError(f"Experiment {template['template_name']} has no methods configured")

    experiment_dir = results_root / template["template_name"]
    ensure_dirs(experiment_dir)
    save_json(experiment_dir / "resolved_template.json", template)

    results = []
    if experiment_type in {"dbf", "subspace"}:
        _, _, generic_test_dataset, samples_model, _ = prepare_datasets(
            repo_root=repo_root,
            template=template,
            model_type="Classical",
            tau=tau,
            need_training_split=False,
        )
        for method_name in methods:
            method_dir = experiment_dir / method_name
            ensure_dirs(method_dir)
            existing_result = load_existing_result(method_dir, template, method_name)
            if existing_result is not None:
                results.append(existing_result)
                continue
            method_class = TRADITIONAL_METHODS[method_name]
            results.append(
                run_traditional_method(
                    method_name=method_name,
                    method_class=method_class,
                    generic_test_dataset=generic_test_dataset,
                    system_model=samples_model,
                    result_dir=method_dir,
                    template=template,
                )
            )
    elif experiment_type == "subspacenet":
        for method_name in methods:
            method_dir = experiment_dir / method_name
            ensure_dirs(method_dir)
            existing_result = load_existing_result(method_dir, template, method_name)
            if existing_result is not None:
                results.append(existing_result)
                continue
            results.append(
                train_subspacenet_variant(
                    repo_root=repo_root,
                    template=template,
                    method_name=method_name,
                    result_dir=method_dir,
                )
            )
    else:
        raise ValueError(f"Unsupported experiment type: {experiment_type}")
    return results


def write_summary(results: List[Dict], results_root: Path):
    table_path = results_root / "summary.csv"
    with table_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "scheme",
                "method",
                "rmse_deg",
                "avg_runtime_sec",
                "avg_lrmc_runtime_sec",
                "avg_lrmc_iterations",
                "lrmc_convergence_rate",
                "avg_lrmc_final_residual",
                "min_lrmc_eigenvalue",
                "min_lrmc_singular_value",
            ],
        )
        writer.writeheader()
        for item in results:
            writer.writerow(item)

    labels = [f"{item['scheme']}\n{item['method']}" for item in results]
    values = [item["rmse_deg"] for item in results]
    plt.figure(figsize=(max(10, len(labels) * 1.2), 5))
    plt.bar(range(len(labels)), values)
    plt.xticks(range(len(labels)), labels, rotation=45, ha="right")
    plt.ylabel("DOA RMSE (deg)")
    plt.title("Ablation Study Comparison")
    plt.tight_layout()
    plt.savefig(results_root / "summary.png")
    plt.close()

    print("\nAblation summary (RMSE deg):")
    for item in results:
        print(
            f"- {item['scheme']} / {item['method']}: {item['rmse_deg']:.4f} deg"
        )


def write_configured_markdowns(results: List[Dict], selected_templates: List[Dict], results_root: Path):
    markdown_groups = {}
    template_report_map = {
        template["template_name"]: template.get("report", {}) for template in selected_templates
    }
    for template in selected_templates:
        report = template.get("report", {})
        output_name = report.get("markdown_output")
        if not output_name:
            continue
        group = markdown_groups.setdefault(
            output_name,
            {
                "title": report.get("markdown_title", template["template_name"]),
                "description": report.get("markdown_description", ""),
                "conditions": report.get("markdown_conditions", []),
                "schemes": [],
            },
        )
        group["schemes"].append(template["template_name"])

    for output_name, config in markdown_groups.items():
        group_results = [item for item in results if item["scheme"] in config["schemes"]]
        if not group_results:
            continue
        has_group_labels = any(
            template_report_map.get(scheme, {}).get("markdown_group_label")
            for scheme in config["schemes"]
        )
        lines = [f"# {config['title']}", ""]
        if config["description"]:
            lines.extend([config["description"], ""])
        if config["conditions"]:
            lines.append("Experimental conditions:")
            for condition in config["conditions"]:
                lines.append(f"- {condition}")
            lines.append("")
        if has_group_labels:
            lines.extend(
                [
                    "| Geometry | Processing | Method | RMSE (deg) |",
                    "| --- | --- | --- | ---: |",
                ]
            )
        else:
            lines.extend([
                "| Algorithm | RMSE (deg) |",
                "| --- | ---: |",
            ])

        def result_sort_key(item):
            report = template_report_map.get(item["scheme"], {})
            group_label = report.get("markdown_group_label", "")
            scheme_label = report.get("markdown_scheme_label")
            method_label = METHOD_MARKDOWN_LABELS.get(item["method"], item["method"])
            return (group_label, scheme_label or "", method_label, item["scheme"])

        sorted_results = sorted(group_results, key=result_sort_key)
        for item in sorted_results:
            report = template_report_map.get(item["scheme"], {})
            group_label = report.get("markdown_group_label")
            scheme_label = report.get("markdown_scheme_label")
            method_label = METHOD_MARKDOWN_LABELS.get(item["method"], item["method"])
            if has_group_labels:
                lines.append(
                    f"| {group_label or item['scheme']} | {scheme_label or ''} | {method_label} | {item['rmse_deg']:.4f} |"
                )
            else:
                label = f"{scheme_label} | {method_label}" if scheme_label else f"{item['scheme']} / {method_label}"
                lines.append(f"| {label} | {item['rmse_deg']:.4f} |")
        output_path = results_root / output_name
        output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


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
    normalize_subspacenet_seeds(selected_templates, args.seed)

    if args.tau is None:
        subspacenet_taus = {
            template["template_name"]: template.get("model", {}).get("tau", 8)
            for template in selected_templates
            if template.get("experiment_type") == "subspacenet"
        }
        if len(set(subspacenet_taus.values())) > 1:
            raise ValueError(
                f"SubspaceNet taus are misaligned for fair comparison: {subspacenet_taus}"
            )

    all_results = []
    for template in selected_templates:
        all_results.extend(run_experiment(repo_root, template, results_root))

    should_write_summary = any(
        template.get("report", {}).get("write_summary_csv", False)
        for template in selected_templates
    )
    if should_write_summary:
        write_summary(all_results, results_root)
    write_configured_markdowns(all_results, selected_templates, results_root)


if __name__ == "__main__":
    main()
