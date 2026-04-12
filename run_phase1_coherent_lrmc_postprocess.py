"""Launch Phase 1F coherent-signal LRMC post-processing ablation experiments."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PHASE1F_EXPERIMENTS = [
    "phase1f_nula_coherent_no_lrmc_t200",
    "phase1f_nula_coherent_lrmc_none_t200",
    "phase1f_nula_coherent_lrmc_fba_t200",
    "phase1f_nula_coherent_lrmc_ss_t200",
    "phase1f_nula_coherent_lrmc_fba_ss_t200",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run Phase 1F coherent NULA LRMC post-processing ablation (classical methods only)."
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase1_coherent_lrmc_postprocess",
        help="Dedicated output directory for Phase 1F post-processing results.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    command = [
        sys.executable,
        str(repo_root / "run_ablation.py"),
        "--templates-dir",
        "data/dataset_templates/ablation/phase1_coherent_lrmc_postprocess",
        "--experiments",
        ",".join(PHASE1F_EXPERIMENTS),
        "--seed",
        str(args.seed),
        "--results-dir",
        args.results_dir,
    ]
    print("Phase 1F experiment: coherent NULA classical post-processing ablation with LRMC at T=200")
    print("Results will be written under:", args.results_dir)
    print("Command:", " ".join(command))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
