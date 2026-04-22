# Phase 6B Experiment Plan - Group B 1.9 Lambda Coherent Fixed-Gap/SNR Grid Without SS -> LRMC

## Goal

Measure how the raw classical controls perform on the coherent Group B `1.9 lambda` fixed-gap and SNR grid when the canonical `SS -> LRMC` preprocessing is removed.

## Motivation

Phase 6 established the `SS -> LRMC` classical baseline and compared it against `SS -> LRMC -> SubspaceNet -> ESPRIT`. This follow-up control keeps the same grid and same classical methods, but removes the preprocessing front end so the effect of that front end can be isolated directly.

## Experimental Design

- Geometry: Group B `1.9 lambda`
- Signal regime: coherent narrowband
- Methods: DBF, MUSIC, Root-MUSIC, ESPRIT
- Snapshots: `T = 40`
- Azimuth/elevation range: `[-15 deg, 15 deg]`
- Fixed azimuth gaps: `1, 2, 3, 4, 5 deg`
- SNR sweep: `1, 5, 10, 15 dB`
- Preprocessing: none
- Metric: horizontal-angle RMSE in degrees

## Dataset Policy

- Reuse the Phase 6 scenario data path for each grid cell when the cached dataset is available.
- If the cache is not present locally, regenerate the equivalent dataset with the same seed and per-cell configuration so the no-preprocessing control can still be measured reproducibly.

## Expected Output

- `summary.csv`
- `phase6b_groupb_1p9_coherent_fixed_gap_snr_grid_no_preproc_results.md`
- per-cell `metrics.json` for DBF, MUSIC, Root-MUSIC, and ESPRIT
