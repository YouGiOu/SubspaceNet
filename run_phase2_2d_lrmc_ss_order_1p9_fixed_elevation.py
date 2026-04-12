"""Launch the Phase 2 2D LRMC / spatial smoothing order comparison at 1.9 lambda with fixed elevation."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PHASE2_EXPERIMENTS = [
    "phase2d_2d_1p9_fixelev_baseline",
    "phase2d_2d_1p9_fixelev_ss_only",
    "phase2d_2d_1p9_fixelev_lrmc_only",
    "phase2d_2d_1p9_fixelev_ss_lrmc",
    "phase2d_2d_1p9_fixelev_lrmc_ss",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the Phase 2 2D LRMC and spatial smoothing order study at 1.9 lambda with fixed elevation."
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase2_2d_lrmc_ss_order_1p9_fixed_elevation",
        help="Dedicated output directory for the fixed-elevation 1.9 lambda order study.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    command = [
        sys.executable,
        str(repo_root / "run_ablation.py"),
        "--templates-dir",
        "data/dataset_templates/ablation/phase2_2d_lrmc_ss_order_1p9_fixed_elevation",
        "--experiments",
        ",".join(PHASE2_EXPERIMENTS),
        "--seed",
        str(args.seed),
        "--results-dir",
        args.results_dir,
    ]
    print(
        "Phase 2 experiment: 2D LRMC / spatial smoothing order comparison at 1.9 lambda with fixed elevation"
    )
    print("Results will be written under:", args.results_dir)
    print("Command:", " ".join(command))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
