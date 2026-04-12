"""Launch Phase 1D coherent-signal LRMC solver ablation experiments."""

from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path


PHASE1D_EXPERIMENTS = [
    "phase1d_nula_coherent_no_lrmc_t200",
    "phase1d_nula_coherent_lrmc_svd_t200",
    "phase1d_nula_coherent_lrmc_nuclear_t200",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run Phase 1D coherent NULA LRMC solver ablation (classical methods only)."
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase1_coherent_lrmc_solver",
        help="Dedicated output directory for Phase 1D solver results.",
    )
    return parser.parse_args()


def ensure_phase1d_dependencies():
    if importlib.util.find_spec("cvxpy") is None:
        raise SystemExit(
            "Phase 1D requires the optional dependency 'cvxpy' for the nuclear solver. "
            "Install it first, or run 'python run_phase1_coherent_lrmc_solver_svd_only.py' "
            "to execute only the supported no-LRMC + SVD subset."
        )


def main():
    args = parse_args()
    ensure_phase1d_dependencies()
    repo_root = Path(__file__).resolve().parent
    command = [
        sys.executable,
        str(repo_root / "run_ablation.py"),
        "--templates-dir",
        "data/dataset_templates/ablation/phase1_coherent_lrmc_solver",
        "--experiments",
        ",".join(PHASE1D_EXPERIMENTS),
        "--seed",
        str(args.seed),
        "--results-dir",
        args.results_dir,
    ]
    print("Phase 1D experiment: coherent NULA classical solver ablation with LRMC at T=200")
    print("Results will be written under:", args.results_dir)
    print("Command:", " ".join(command))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
