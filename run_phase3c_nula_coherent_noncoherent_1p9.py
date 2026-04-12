"""Launch the Phase 3c 1D NULA 1.9 lambda comparison for coherent and non-coherent signals."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PHASE3_EXPERIMENTS = [
    "phase3c_nula_c_1p9_baseline_t200",
    "phase3c_nula_c_1p9_lrmc_t200",
    "phase3c_nula_c_1p9_lrmc_ss_t200",
    "phase3c_nula_nc_1p9_baseline_t200",
    "phase3c_nula_nc_1p9_lrmc_t200",
    "phase3c_nula_nc_1p9_lrmc_ss_t200",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the Phase 3c 1D NULA 1.9 lambda comparison for coherent and non-coherent signals."
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase3c_nula_coherent_noncoherent_1p9",
        help="Dedicated output directory for the Phase 3c comparison.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    command = [
        sys.executable,
        str(repo_root / "run_ablation.py"),
        "--templates-dir",
        "data/dataset_templates/ablation/phase3c_nula_coherent_noncoherent_1p9",
        "--experiments",
        ",".join(PHASE3_EXPERIMENTS),
        "--seed",
        str(args.seed),
        "--results-dir",
        args.results_dir,
    ]
    print("Phase 3c experiment: 1D NULA 1.9 lambda coherent/non-coherent comparison")
    print("Results will be written under:", args.results_dir)
    print("Command:", " ".join(command))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
