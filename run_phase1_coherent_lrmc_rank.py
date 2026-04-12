"""Launch Phase 1B coherent-signal LRMC rank ablation experiments."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PHASE1B_EXPERIMENTS = [
    "phase1b_nula_coherent_no_lrmc_t200",
    "phase1b_nula_coherent_lrmc_rank2_t200",
    "phase1b_nula_coherent_lrmc_rank3_t200",
    "phase1b_nula_coherent_lrmc_rank4_t200",
    "phase1b_nula_coherent_lrmc_rank5_t200",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run Phase 1B coherent NULA LRMC rank ablation (classical methods only)."
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase1_coherent_lrmc_rank",
        help="Dedicated output directory for Phase 1B rank results.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    command = [
        sys.executable,
        str(repo_root / "run_ablation.py"),
        "--templates-dir",
        "data/dataset_templates/ablation/phase1_coherent_lrmc_rank",
        "--experiments",
        ",".join(PHASE1B_EXPERIMENTS),
        "--seed",
        str(args.seed),
        "--results-dir",
        args.results_dir,
    ]
    print("Phase 1B experiment: coherent NULA classical rank ablation with LRMC at T=200")
    print("Results will be written under:", args.results_dir)
    print("Command:", " ".join(command))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
