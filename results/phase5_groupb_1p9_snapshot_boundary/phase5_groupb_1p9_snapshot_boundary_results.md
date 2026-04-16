# Phase 5 - Group B 1.9 Lambda Snapshot Boundary Study

Phase 5 sweeps snapshot count on the Group B hardware geometry using the same SS -> LRMC front end as the SubspaceNet studies, to identify the low-snapshot boundary for coherent and non-coherent signals.

Experimental conditions:
- Array: Group B 12-channel 2D hardware geometry
- Physical spacing: 1.9 lambda
- Preprocessing: spatial smoothing before LRMC
- Azimuth and elevation range: [-15 deg, 15 deg]
- Minimum azimuth separation: 5 deg
- Sources: 2 narrowband targets
- Snapshot sweep: T = 10, 25, 50, 100, 200
- Methods: MUSIC, Root-MUSIC, ESPRIT
- Metric: horizontal-angle RMSE in degrees

| Geometry | Processing | Method | RMSE (deg) |
| --- | --- | --- | ---: |
| coherent | T = 10 | SS -> LRMC | ESPRIT | 1.8200 |
| coherent | T = 10 | SS -> LRMC | MUSIC | 1.6822 |
| coherent | T = 10 | SS -> LRMC | Root-MUSIC | 1.7782 |
| coherent | T = 100 | SS -> LRMC | ESPRIT | 2.0239 |
| coherent | T = 100 | SS -> LRMC | MUSIC | 1.8831 |
| coherent | T = 100 | SS -> LRMC | Root-MUSIC | 1.9469 |
| coherent | T = 200 | SS -> LRMC | ESPRIT | 2.0359 |
| coherent | T = 200 | SS -> LRMC | MUSIC | 1.7331 |
| coherent | T = 200 | SS -> LRMC | Root-MUSIC | 1.8003 |
| coherent | T = 25 | SS -> LRMC | ESPRIT | 1.7703 |
| coherent | T = 25 | SS -> LRMC | MUSIC | 1.6937 |
| coherent | T = 25 | SS -> LRMC | Root-MUSIC | 1.7389 |
| coherent | T = 50 | SS -> LRMC | ESPRIT | 1.8422 |
| coherent | T = 50 | SS -> LRMC | MUSIC | 1.6309 |
| coherent | T = 50 | SS -> LRMC | Root-MUSIC | 1.6716 |
| non-coherent | T = 10 | SS -> LRMC | ESPRIT | 0.8276 |
| non-coherent | T = 10 | SS -> LRMC | MUSIC | 0.8520 |
| non-coherent | T = 10 | SS -> LRMC | Root-MUSIC | 0.8677 |
| non-coherent | T = 100 | SS -> LRMC | ESPRIT | 0.3779 |
| non-coherent | T = 100 | SS -> LRMC | MUSIC | 0.3791 |
| non-coherent | T = 100 | SS -> LRMC | Root-MUSIC | 0.4002 |
| non-coherent | T = 200 | SS -> LRMC | ESPRIT | 0.3272 |
| non-coherent | T = 200 | SS -> LRMC | MUSIC | 0.3045 |
| non-coherent | T = 200 | SS -> LRMC | Root-MUSIC | 0.3264 |
| non-coherent | T = 25 | SS -> LRMC | ESPRIT | 0.5082 |
| non-coherent | T = 25 | SS -> LRMC | MUSIC | 0.4914 |
| non-coherent | T = 25 | SS -> LRMC | Root-MUSIC | 0.4860 |
| non-coherent | T = 50 | SS -> LRMC | ESPRIT | 0.4426 |
| non-coherent | T = 50 | SS -> LRMC | MUSIC | 0.4320 |
| non-coherent | T = 50 | SS -> LRMC | Root-MUSIC | 0.4464 |

# summary
These results give a pretty clear boundary picture.

From [`phase5_groupb_1p9_snapshot_boundary_results.md`](/f:/workspace1/SubspaceNet/results/phase5_groupb_1p9_snapshot_boundary/phase5_groupb_1p9_snapshot_boundary_results.md):

## Main conclusions

### 1. Coherent case is surprisingly flat across snapshots
For coherent signals, with Group B `1.9λ` and `SS -> LRMC`, performance barely changes from `T=10` to `T=200`.

- `T=10`:
  - MUSIC `1.68°`
  - Root-MUSIC `1.78°`
  - ESPRIT `1.82°`
- `T=200`:
  - MUSIC `1.73°`
  - Root-MUSIC `1.80°`
  - ESPRIT `2.04°`

So the coherent classical pipeline is already fairly snapshot-robust in this regime. There is no sharp collapse at low `T`.

That means:
- low snapshots are not the main pain point here
- for coherent Group B, the difficulty is more structural/model-based than simply “too few snapshots”

### 2. Non-coherent case degrades smoothly and predictably
For non-coherent signals, the trend is what we’d normally expect:

- `T=200`: around `0.30° - 0.33°`
- `T=100`: around `0.38° - 0.40°`
- `T=50`: around `0.43° - 0.45°`
- `T=25`: around `0.49° - 0.51°`
- `T=10`: around `0.83° - 0.87°`

So non-coherent performance does get worse as snapshots decrease, but still stays quite good even at `T=10`.

This suggests:
- non-coherent Group B is an easy regime for the classical `SS -> LRMC` pipeline
- low-snapshot SubspaceNet for non-coherent signals may not have much headroom unless we push to even smaller `T` or harsher SNR

### 3. The methods are very close within each regime
Another important point: the three methods are tightly clustered.

Coherent:
- all three methods stay around `1.6° - 2.0°`

Non-coherent:
- all three methods stay within a few hundredths of a degree of each other at each `T`

So the snapshot sweep does not show a strong method-specific boundary. It shows a regime-level boundary:
- coherent settles near `~1.8°`
- non-coherent settles near `~0.3° - 0.9°` depending on `T`

### 4. There is no obvious “training boundary” yet in the tested range
If the purpose is to decide where SubspaceNet under low-snapshot conditions becomes necessary, then within the current sweep:

- Coherent: no clear low-snapshot breakdown from `T=200` down to `T=10`
- Non-coherent: graceful degradation, but still strong at `T=10`

So based on these results alone, I would say:
- `T=10` is still not low enough to expose a sharp classical failure boundary for Group B `1.9λ` with `SS -> LRMC`

## Practical implication for next SubspaceNet stage

### For coherent signals
A low-snapshot SubspaceNet study is still reasonable, but not because classical performance collapses below `T=50`.
Instead:
- the classical coherent floor is already around `1.7° - 2.0°`
- so a learned model would need to beat that floor, not just survive lower `T`

### For non-coherent signals
I would be cautious about investing in low-snapshot SubspaceNet training yet.
Why:
- even at `T=10`, the classical pipeline is still below `1°`
- the potential gain may be limited

## Best next step
If you want to find a true low-snapshot boundary, I’d extend the sweep downward:
1. `T = 2, 4, 6, 8, 10, 15, 25`
2. probably for Group B only
3. and maybe add one lower-SNR sweep like `0 dB`

That would be much more likely to reveal where the classical pipeline really starts breaking.

## Bottom line
- In the tested range, there is no strong snapshot-driven failure boundary.
- Coherent performance is almost flat from `T=10` to `T=200`.
- Non-coherent performance degrades smoothly but remains strong.
- So for Group B `1.9λ`, the next meaningful “boundary” study probably needs either:
  - even smaller `T`, or
  - lower SNR, or
  - both.