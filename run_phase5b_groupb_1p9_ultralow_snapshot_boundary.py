"""Launch the Phase 5B Group B 1.9 lambda ultra-low snapshot study."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PHASE5B_EXPERIMENTS = [
    "phase5b_groupb_1p9_coherent_ss_lrmc_t1",
    "phase5b_groupb_1p9_coherent_ss_lrmc_t2",
    "phase5b_groupb_1p9_coherent_ss_lrmc_t4",
    "phase5b_groupb_1p9_coherent_ss_lrmc_t6",
    "phase5b_groupb_1p9_coherent_ss_lrmc_t8",
    "phase5b_groupb_1p9_coherent_ss_lrmc_t10",
    "phase5b_groupb_1p9_noncoherent_ss_lrmc_t1",
    "phase5b_groupb_1p9_noncoherent_ss_lrmc_t2",
    "phase5b_groupb_1p9_noncoherent_ss_lrmc_t4",
    "phase5b_groupb_1p9_noncoherent_ss_lrmc_t6",
    "phase5b_groupb_1p9_noncoherent_ss_lrmc_t8",
    "phase5b_groupb_1p9_noncoherent_ss_lrmc_t10",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the Phase 5B Group B 1.9 lambda ultra-low snapshot study."
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase5b_groupb_1p9_ultralow_snapshot_boundary",
        help="Dedicated output directory for the Phase 5B ultra-low snapshot study.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    command = [
        sys.executable,
        str(repo_root / "run_ablation.py"),
        "--templates-dir",
        "data/dataset_templates/ablation/phase5b_groupb_1p9_ultralow_snapshot_boundary",
        "--experiments",
        ",".join(PHASE5B_EXPERIMENTS),
        "--seed",
        str(args.seed),
        "--results-dir",
        args.results_dir,
    ]
    print("Phase 5B experiment: Group B 1.9 lambda ultra-low snapshot study")
    print("Results will be written under:", args.results_dir)
    print("Command:", " ".join(command))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
