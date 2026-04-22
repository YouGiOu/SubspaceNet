"""Launch Phase 6 non-coherent Group B fixed-gap/SNR experiments on the 1.9 lambda geometry."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


GAPS_DEG = [5, 4, 3, 2, 1]
SNRS_DB = [1, 5, 10, 15]


def build_experiments() -> list[str]:
    experiments = []
    for gap in GAPS_DEG:
        for snr in SNRS_DB:
            experiments.append(
                f"phase6_groupb_1p9_noncoherent_control_gap{gap}_snr{snr}"
            )
            experiments.append(
                f"phase6_groupb_1p9_noncoherent_subspacenet_esprit_gap{gap}_snr{snr}"
            )
    return experiments


PHASE6_EXPERIMENTS = build_experiments()


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Run Phase 6 non-coherent Group B 1.9 lambda fixed-gap/SNR grid experiments "
            "with classical controls and SubspaceNet-ESPRIT."
        )
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase6_groupb_1p9_noncoherent_fixed_gap_snr_grid",
        help="Dedicated output directory for the Phase 6 fixed-gap/SNR grid study.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    command = [
        sys.executable,
        str(repo_root / "run_ablation.py"),
        "--templates-dir",
        "data/dataset_templates/ablation/phase6_groupb_1p9_noncoherent_fixed_gap_snr_grid",
        "--experiments",
        ",".join(PHASE6_EXPERIMENTS),
        "--seed",
        str(args.seed),
        "--results-dir",
        args.results_dir,
    ]
    print(
        "Phase 6 experiment: non-coherent Group B 1.9 lambda fixed-gap/SNR grid "
        "with classical controls and SubspaceNet-ESPRIT"
    )
    print("Results will be written under:", args.results_dir)
    print("Command:", " ".join(command))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
