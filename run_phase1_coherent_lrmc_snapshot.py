"""Launch Phase 1A coherent-signal LRMC snapshot ablation experiments."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PHASE1_EXPERIMENTS = [
    "phase1_nula_coherent_no_lrmc_t50",
    "phase1_nula_coherent_lrmc_t50",
    "phase1_nula_coherent_no_lrmc_t100",
    "phase1_nula_coherent_lrmc_t100",
    "phase1_nula_coherent_no_lrmc_t200",
    "phase1_nula_coherent_lrmc_t200",
    "phase1_nula_coherent_no_lrmc_t400",
    "phase1_nula_coherent_lrmc_t400",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run Phase 1A coherent NULA LRMC snapshot ablation (classical methods only)."
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase1_coherent_lrmc_snapshot",
        help="Dedicated output directory for Phase 1A snapshot results.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    command = [
        sys.executable,
        str(repo_root / "run_ablation.py"),
        "--templates-dir",
        "data/dataset_templates/ablation/phase1_coherent_lrmc",
        "--experiments",
        ",".join(PHASE1_EXPERIMENTS),
        "--seed",
        str(args.seed),
        "--results-dir",
        args.results_dir,
    ]
    print("Phase 1A experiment: coherent NULA classical snapshot ablation with and without default LRMC")
    print("Results will be written under:", args.results_dir)
    print("Command:", " ".join(command))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
