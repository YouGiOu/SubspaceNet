"""Launch Phase 6B Group B hard-regime snapshot breakdown experiments."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


SIGNAL_NATURES = ["coherent", "noncoherent"]
SNAPSHOTS = [1, 2, 4, 8, 16, 25]


def build_experiments() -> list[str]:
    experiments = []
    for nature in SIGNAL_NATURES:
        for snapshots in SNAPSHOTS:
            experiments.append(
                f"phase6b_groupb_1p9_{nature}_raw_control_gap1_snr1_t{snapshots}"
            )
            experiments.append(
                f"phase6b_groupb_1p9_{nature}_ss_lrmc_control_gap1_snr1_t{snapshots}"
            )
            experiments.append(
                f"phase6b_groupb_1p9_{nature}_subspacenet_esprit_gap1_snr1_t{snapshots}"
            )
    return experiments


PHASE6B_EXPERIMENTS = build_experiments()


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Run Phase 6B Group B 1.9 lambda hard-regime snapshot breakdown "
            "experiments with raw controls, SS -> LRMC controls, and SubspaceNet-ESPRIT."
        )
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase6b_groupb_1p9_fixed_gap1_snr1_snapshot_breakdown",
        help="Dedicated output directory for the Phase 6B hard-regime snapshot breakdown study.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    command = [
        sys.executable,
        str(repo_root / "run_ablation.py"),
        "--templates-dir",
        "data/dataset_templates/ablation/phase6b_groupb_1p9_fixed_gap1_snr1_snapshot_breakdown",
        "--experiments",
        ",".join(PHASE6B_EXPERIMENTS),
        "--seed",
        str(args.seed),
        "--results-dir",
        args.results_dir,
    ]
    print(
        "Phase 6B experiment: Group B 1.9 lambda hard-regime snapshot breakdown "
        "with raw controls, SS -> LRMC controls, and SubspaceNet-ESPRIT"
    )
    print("Results will be written under:", args.results_dir)
    print("Command:", " ".join(command))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
