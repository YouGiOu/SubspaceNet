"""Launch the Phase 3 1D spacing scan for coherent NULA LRMC."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PHASE3_EXPERIMENTS = [
    "phase3a_spacing_0p5_no_lrmc_t200",
    "phase3a_spacing_0p5_lrmc_t200",
    "phase3a_spacing_1p0_no_lrmc_t200",
    "phase3a_spacing_1p0_lrmc_t200",
    "phase3a_spacing_1p9_no_lrmc_t200",
    "phase3a_spacing_1p9_lrmc_t200",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the Phase 3 1D spacing scan for coherent NULA LRMC."
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase3_1d_spacing_scan",
        help="Dedicated output directory for the Phase 3 spacing scan.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    command = [
        sys.executable,
        str(repo_root / "run_ablation.py"),
        "--templates-dir",
        "data/dataset_templates/ablation/phase3_1d_spacing_scan",
        "--experiments",
        ",".join(PHASE3_EXPERIMENTS),
        "--seed",
        str(args.seed),
        "--results-dir",
        args.results_dir,
    ]
    print("Phase 3 experiment: 1D spacing scan for coherent NULA LRMC")
    print("Results will be written under:", args.results_dir)
    print("Command:", " ".join(command))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
