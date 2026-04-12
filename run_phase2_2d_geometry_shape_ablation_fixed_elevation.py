"""Launch the Phase 2 2D geometry-shape ablation with elevation fixed at 0 degrees, across Group A / Group B / Group C."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PHASE2_EXPERIMENTS = [
    "phase2h_groupa_0p5_fixelev_baseline",
    "phase2h_groupa_0p5_fixelev_ss_only",
    "phase2h_groupa_0p5_fixelev_lrmc_only",
    "phase2h_groupa_0p5_fixelev_ss_lrmc",
    "phase2h_groupa_0p5_fixelev_lrmc_ss",
    "phase2h_groupb_0p5_fixelev_baseline",
    "phase2h_groupb_0p5_fixelev_ss_only",
    "phase2h_groupb_0p5_fixelev_lrmc_only",
    "phase2h_groupb_0p5_fixelev_ss_lrmc",
    "phase2h_groupb_0p5_fixelev_lrmc_ss",
    "phase2h_groupa_1p9_fixelev_baseline",
    "phase2h_groupa_1p9_fixelev_ss_only",
    "phase2h_groupa_1p9_fixelev_lrmc_only",
    "phase2h_groupa_1p9_fixelev_ss_lrmc",
    "phase2h_groupa_1p9_fixelev_lrmc_ss",
    "phase2h_groupb_1p9_fixelev_baseline",
    "phase2h_groupb_1p9_fixelev_ss_only",
    "phase2h_groupb_1p9_fixelev_lrmc_only",
    "phase2h_groupb_1p9_fixelev_ss_lrmc",
    "phase2h_groupb_1p9_fixelev_lrmc_ss",
    "phase2h_groupc_0p5_fixelev_baseline",
    "phase2h_groupc_0p5_fixelev_ss_only",
    "phase2h_groupc_0p5_fixelev_lrmc_only",
    "phase2h_groupc_0p5_fixelev_ss_lrmc",
    "phase2h_groupc_0p5_fixelev_lrmc_ss",
    "phase2h_groupc_1p9_fixelev_baseline",
    "phase2h_groupc_1p9_fixelev_ss_only",
    "phase2h_groupc_1p9_fixelev_lrmc_only",
    "phase2h_groupc_1p9_fixelev_ss_lrmc",
    "phase2h_groupc_1p9_fixelev_lrmc_ss",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the Phase 2 2D geometry-shape ablation with elevation fixed at 0 degrees across Group A / Group B / Group C."
    )
    parser.add_argument("--seed", type=int, default=42, help="Shared random seed.")
    parser.add_argument(
        "--results-dir",
        default="results/phase2_2d_geometry_shape_ablation_fixed_elevation",
        help="Dedicated output directory for the fixed-elevation geometry-shape ablation.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    command = [
        sys.executable,
        str(repo_root / "run_ablation.py"),
        "--templates-dir",
        "data/dataset_templates/ablation/phase2_2d_geometry_shape_ablation_fixed_elevation",
        "--experiments",
        ",".join(PHASE2_EXPERIMENTS),
        "--seed",
        str(args.seed),
        "--results-dir",
        args.results_dir,
    ]
    print(
        "Phase 2 experiment: 2D geometry-shape ablation across Group A / Group B / Group C and 0.5/1.9 lambda with fixed elevation"
    )
    print("Results will be written under:", args.results_dir)
    print("Command:", " ".join(command))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
