# Phase 2 2D LRMC / Spatial Smoothing Order Implementation Plan

## Goal
Implement a 2D-array DOA pipeline for the 12-channel geometry with `1.9λ` spacing and `[-15°, +15°]` azimuth/elevation FOV, then compare:
- spatial smoothing only
- LRMC only
- spatial smoothing -> LRMC
- LRMC -> spatial smoothing

## Implementation Notes
- Use the physical 2D geometry derived from `radar_array_geometry.cpp` as the data-generation source.
- Generate coherent narrowband snapshots from azimuth/elevation pairs, but keep the evaluation label as horizontal angle only.
- Treat the three `[0,1,4,8]` row replicas as geometry-equivalent 4-channel NULA blocks.
- Add row-wise covariance helpers so the pipeline can:
  - average the three rows before LRMC
  - complete one canonical row without smoothing
  - complete all rows and average completed covariances after LRMC
- Keep the LRMC numerics stable with the current Hermitian and PSD projection steps.

## Template / Runner
- Add JSON templates for each processing path.
- Add a dedicated launcher script for the Phase 2 comparison.
- Record the resolved template and per-method metrics in the results folder.

## Assumptions
- The `1.9λ` spacing is authoritative.
- The `[-15°, +15°]` FOV applies to both azimuth and elevation.
- The 5-degree separation constraint applies to horizontal angle only.
- Classical DOA evaluation is the first target; SubspaceNet retraining can follow later.
