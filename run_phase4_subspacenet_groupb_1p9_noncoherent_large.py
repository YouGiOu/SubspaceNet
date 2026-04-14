"""Launch Phase 4B non-coherent SubspaceNet training on Group B at 1.9 lambda with 45,000 samples."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PHASE4_EXPERIMENTS = [
    "phase4b_groupb_1p9_noncoherent_subspacenet_45k",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run Phase 4B large-sample non-coherent SubspaceNet training on the Group B 2D geometry."
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase4_subspacenet_groupb_1p9_noncoherent_large",
        help="Dedicated output directory for the Phase 4B non-coherent SubspaceNet experiment.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    command = [
        sys.executable,
        str(repo_root / "run_ablation.py"),
        "--templates-dir",
        "data/dataset_templates/ablation/phase4_subspacenet_groupb_1p9_noncoherent_large",
        "--experiments",
        ",".join(PHASE4_EXPERIMENTS),
        "--seed",
        str(args.seed),
        "--results-dir",
        args.results_dir,
    ]
    print("Phase 4B experiment: non-coherent SubspaceNet on Group B 2D geometry at 1.9 lambda")
    print("Results will be written under:", args.results_dir)
    print("Command:", " ".join(command))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
