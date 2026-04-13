"""Launch the Phase 3d 1D NULA row-pattern control at 1.9 lambda."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PHASE3_EXPERIMENTS = [
    "phase3d_nula_a_1p9_baseline_t200",
    "phase3d_nula_a_1p9_lrmc_t200",
    "phase3d_nula_a_1p9_lrmc_ss_t200",
    "phase3d_nula_c_1p9_baseline_t200",
    "phase3d_nula_c_1p9_lrmc_t200",
    "phase3d_nula_c_1p9_lrmc_ss_t200",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the Phase 3d 1D NULA pattern control at 1.9 lambda."
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase3d_nula_pattern_control_1p9",
        help="Dedicated output directory for the Phase 3d comparison.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    command = [
        sys.executable,
        str(repo_root / "run_ablation.py"),
        "--templates-dir",
        "data/dataset_templates/ablation/phase3d_nula_pattern_control_1p9",
        "--experiments",
        ",".join(PHASE3_EXPERIMENTS),
        "--seed",
        str(args.seed),
        "--results-dir",
        args.results_dir,
    ]
    print("Phase 3d experiment: 1D NULA row-pattern control at 1.9 lambda")
    print("Results will be written under:", args.results_dir)
    print("Command:", " ".join(command))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
