"""Launch the Phase 2 2D LRMC / spatial smoothing order comparison at 0.5 lambda spacing."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PHASE2_EXPERIMENTS = [
    "phase2b_2d_0p5_baseline",
    "phase2b_2d_0p5_ss_only",
    "phase2b_2d_0p5_lrmc_only",
    "phase2b_2d_0p5_ss_lrmc",
    "phase2b_2d_0p5_lrmc_ss",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the Phase 2 2D LRMC and spatial smoothing order study at 0.5 lambda spacing."
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase2_2d_lrmc_ss_order_0p5",
        help="Dedicated output directory for the 0.5 lambda order study.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    command = [
        sys.executable,
        str(repo_root / "run_ablation.py"),
        "--templates-dir",
        "data/dataset_templates/ablation/phase2_2d_lrmc_ss_order_0p5",
        "--experiments",
        ",".join(PHASE2_EXPERIMENTS),
        "--seed",
        str(args.seed),
        "--results-dir",
        args.results_dir,
    ]
    print("Phase 2 experiment: 2D LRMC / spatial smoothing order comparison at 0.5 lambda")
    print("Results will be written under:", args.results_dir)
    print("Command:", " ".join(command))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
