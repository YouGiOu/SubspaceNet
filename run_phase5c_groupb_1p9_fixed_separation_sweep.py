"""Launch the Phase 5C Group B 1.9 lambda fixed-separation study."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PHASE5C_EXPERIMENTS = [
    "phase5c_groupb_1p9_coherent_ss_lrmc_gap5",
    "phase5c_groupb_1p9_coherent_ss_lrmc_gap4",
    "phase5c_groupb_1p9_coherent_ss_lrmc_gap3",
    "phase5c_groupb_1p9_coherent_ss_lrmc_gap2",
    "phase5c_groupb_1p9_coherent_ss_lrmc_gap1",
    "phase5c_groupb_1p9_noncoherent_ss_lrmc_gap5",
    "phase5c_groupb_1p9_noncoherent_ss_lrmc_gap4",
    "phase5c_groupb_1p9_noncoherent_ss_lrmc_gap3",
    "phase5c_groupb_1p9_noncoherent_ss_lrmc_gap2",
    "phase5c_groupb_1p9_noncoherent_ss_lrmc_gap1",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the Phase 5C Group B 1.9 lambda fixed-separation study."
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase5c_groupb_1p9_fixed_separation_sweep",
        help="Dedicated output directory for the Phase 5C separation study.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    command = [
        sys.executable,
        str(repo_root / "run_ablation.py"),
        "--templates-dir",
        "data/dataset_templates/ablation/phase5c_groupb_1p9_fixed_separation_sweep",
        "--experiments",
        ",".join(PHASE5C_EXPERIMENTS),
        "--seed",
        str(args.seed),
        "--results-dir",
        args.results_dir,
    ]
    print("Phase 5C experiment: Group B 1.9 lambda fixed-separation study")
    print("Results will be written under:", args.results_dir)
    print("Command:", " ".join(command))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
