# Phase 3 1D Spacing Scan Implementation Plan

## Goal
Isolate the effect of element spacing on the coherent NULA LRMC pipeline by keeping the geometry one-dimensional and scanning the same sparse array pattern `[0, 1, 4, 8]` across multiple spacings.

## Design
- Use a 1D NULA instead of the 2D array so that the scan is not confounded by row offsets or elevation coupling.
- Scan three spacings:
  - `0.5 lambda`
  - `1.0 lambda`
  - `1.9 lambda`
- For each spacing, keep the same coherent narrowband two-source setup and compare:
  - no LRMC baseline
  - LRMC with the best current coherent configuration

## Why This Is the Right First Check
- The phase 2 2D results suggest the ambiguity problem may be dominated by geometry, not solver quality.
- A 1D scan removes the 2D reduction as a confound and tells us whether the spacing alone is enough to cause the RMSE collapse.

## Template / Runner
- Add one template pair per spacing and a single launcher script.
- Keep the output grouped into one summary table so the three spacings can be compared side by side.

## Assumptions
- The sparse NULA pattern remains `[0, 1, 4, 8]`.
- The scan uses spacing-specific alias-free FOV limits.
- The source-count, snapshot count, and solver settings remain fixed so spacing is the main variable.
