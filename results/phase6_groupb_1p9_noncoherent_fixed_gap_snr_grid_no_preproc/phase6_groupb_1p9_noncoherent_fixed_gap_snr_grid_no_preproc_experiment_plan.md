# Phase 6 Experiment Plan - Group B 1.9 Lambda Non-Coherent Fixed-Gap/SNR Grid Without SS -> LRMC

## Goal

Measure how the raw classical controls perform on the non-coherent Group B `1.9 lambda` fixed-gap and SNR grid when the canonical `SS -> LRMC` preprocessing is removed.

## Motivation

The coherent no-preprocessing control already isolates the value of the `SS -> LRMC` front end in the harder coherent regime. This matching non-coherent study keeps the same grid and same raw classical methods, changing only the signal nature from coherent to non-coherent so the preprocessing effect can be compared across regimes.

## Experimental Design

- Geometry: Group B `1.9 lambda`
- Signal regime: non-coherent narrowband
- Methods: DBF, MUSIC, Root-MUSIC, ESPRIT
- Snapshots: `T = 40`
- Azimuth/elevation range: `[-15 deg, 15 deg]`
- Fixed azimuth gaps: `1, 2, 3, 4, 5 deg`
- SNR sweep: `1, 5, 10, 15 dB`
- Preprocessing: none
- Metric: horizontal-angle RMSE in degrees

## Dataset Policy

- Reuse the matching Phase 6 non-coherent scenario data path for each grid cell when the cached dataset is available.
- If the cache is not present locally, regenerate the equivalent dataset with the same seed and per-cell configuration so the no-preprocessing control can still be measured reproducibly.

## Expected Output

- `summary.csv`
- `phase6_groupb_1p9_noncoherent_fixed_gap_snr_grid_no_preproc_results.md`
- per-cell `metrics.json` for DBF, MUSIC, Root-MUSIC, and ESPRIT
