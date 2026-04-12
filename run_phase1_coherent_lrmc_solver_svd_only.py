"""Launch the supported Phase 1D subset when cvxpy is unavailable."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PHASE1D_SVD_ONLY_EXPERIMENTS = [
    "phase1d_nula_coherent_no_lrmc_t200",
    "phase1d_nula_coherent_lrmc_svd_t200",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the no-LRMC + SVD subset of Phase 1D when cvxpy is unavailable."
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase1_coherent_lrmc_solver_svd_only",
        help="Dedicated output directory for the partial Phase 1D SVD-only run.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    command = [
        sys.executable,
        str(repo_root / "run_ablation.py"),
        "--templates-dir",
        "data/dataset_templates/ablation/phase1_coherent_lrmc_solver",
        "--experiments",
        ",".join(PHASE1D_SVD_ONLY_EXPERIMENTS),
        "--seed",
        str(args.seed),
        "--results-dir",
        args.results_dir,
    ]
    print("Phase 1D fallback: running only the no-LRMC + SVD subset because cvxpy is unavailable")
    print("Results will be written under:", args.results_dir)
    print("Command:", " ".join(command))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
