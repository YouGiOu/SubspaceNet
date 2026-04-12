"""Launch Phase 1E coherent-signal LRMC initialization ablation experiments."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PHASE1E_EXPERIMENTS = [
    "phase1e_nula_coherent_no_lrmc_t200",
    "phase1e_nula_coherent_lrmc_lag_t200",
    "phase1e_nula_coherent_lrmc_zero_t200",
    "phase1e_nula_coherent_lrmc_neighbor_t200",
    "phase1e_nula_coherent_lrmc_random_t200",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run Phase 1E coherent NULA LRMC initialization ablation (classical methods only)."
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase1_coherent_lrmc_init",
        help="Dedicated output directory for Phase 1E initialization results.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    command = [
        sys.executable,
        str(repo_root / "run_ablation.py"),
        "--templates-dir",
        "data/dataset_templates/ablation/phase1_coherent_lrmc_init",
        "--experiments",
        ",".join(PHASE1E_EXPERIMENTS),
        "--seed",
        str(args.seed),
        "--results-dir",
        args.results_dir,
    ]
    print("Phase 1E experiment: coherent NULA classical initialization ablation with LRMC at T=200")
    print("Results will be written under:", args.results_dir)
    print("Command:", " ".join(command))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
