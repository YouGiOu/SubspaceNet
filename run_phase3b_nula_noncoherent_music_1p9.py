"""Launch the Phase 3b non-coherent MUSIC validation on the 1.9 lambda NULA."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PHASE3_EXPERIMENTS = [
    "phase3b_nula_nc_music_1p9_no_lrmc_t200",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the Phase 3b non-coherent MUSIC validation on the 1.9 lambda NULA."
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase3b_nula_noncoherent_music_1p9",
        help="Dedicated output directory for the non-coherent 1.9 lambda MUSIC validation.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    command = [
        sys.executable,
        str(repo_root / "run_ablation.py"),
        "--templates-dir",
        "data/dataset_templates/ablation/phase3b_nula_noncoherent_music_1p9",
        "--experiments",
        ",".join(PHASE3_EXPERIMENTS),
        "--seed",
        str(args.seed),
        "--results-dir",
        args.results_dir,
    ]
    print("Phase 3b experiment: non-coherent MUSIC validation on the 1.9 lambda NULA")
    print("Results will be written under:", args.results_dir)
    print("Command:", " ".join(command))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
