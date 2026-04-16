"""Launch the Phase 5 Group B 1.9 lambda snapshot-boundary study."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PHASE5_EXPERIMENTS = [
    "phase5_groupb_1p9_coherent_ss_lrmc_t10",
    "phase5_groupb_1p9_coherent_ss_lrmc_t25",
    "phase5_groupb_1p9_coherent_ss_lrmc_t50",
    "phase5_groupb_1p9_coherent_ss_lrmc_t100",
    "phase5_groupb_1p9_coherent_ss_lrmc_t200",
    "phase5_groupb_1p9_noncoherent_ss_lrmc_t10",
    "phase5_groupb_1p9_noncoherent_ss_lrmc_t25",
    "phase5_groupb_1p9_noncoherent_ss_lrmc_t50",
    "phase5_groupb_1p9_noncoherent_ss_lrmc_t100",
    "phase5_groupb_1p9_noncoherent_ss_lrmc_t200",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the Phase 5 Group B 1.9 lambda snapshot-boundary study."
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase5_groupb_1p9_snapshot_boundary",
        help="Dedicated output directory for the Phase 5 snapshot study.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    command = [
        sys.executable,
        str(repo_root / "run_ablation.py"),
        "--templates-dir",
        "data/dataset_templates/ablation/phase5_groupb_1p9_snapshot_boundary",
        "--experiments",
        ",".join(PHASE5_EXPERIMENTS),
        "--seed",
        str(args.seed),
        "--results-dir",
        args.results_dir,
    ]
    print("Phase 5 experiment: Group B 1.9 lambda snapshot-boundary study")
    print("Results will be written under:", args.results_dir)
    print("Command:", " ".join(command))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
