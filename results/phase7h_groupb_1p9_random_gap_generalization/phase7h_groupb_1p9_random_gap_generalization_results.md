# Phase 7H - Group B 1.9 Lambda Random-Gap Generalization

Phase 7H evaluates the Phase 7G boundary-repair anti-rectifier fusion model on newly generated random-gap test sets so the angular separation is continuous rather than locked to the earlier fixed-gap grid.

Experimental conditions:
- Array: Group B 12-channel 2D hardware geometry
- Physical spacing: 1.9 lambda
- Model family: SS(2/3 x 3) -> LRMC -> width-controlled anti-rectifier spatial fusion -> SubspaceNet backbone 3x3 -> ESPRIT
- Checkpoint under test: best Phase 7G boundary-repair model
- Evaluation distribution: random azimuth gaps inside [-15 deg, 15 deg]
- Gap rule: min_doa_gap = 1 deg, with no fixed_doa_gap constraint
- Snapshots: T = 40
- Test sample count: 9,000 per dataset
- Primary metric: horizontal-angle RMSE in degrees
- Extra reporting: realized random-gap distribution summary per dataset

Reference anchor RMSE: `0.3592 deg`

## Coherent Random-Gap Table

| SNR (dB) | RMSE (deg) | Avg runtime / sample (s) | Mean gap (deg) | Median gap (deg) | Min gap (deg) | Max gap (deg) | Samples |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 5.7377 | 0.016078 | 10.6000 | 9.3400 | 1.0000 | 29.7400 | 9000 |
| 5 | 5.6775 | 0.015922 | 10.7088 | 9.5900 | 1.0000 | 29.6900 | 9000 |
| 10 | 5.5513 | 0.015989 | 10.5667 | 9.3100 | 1.0000 | 29.7900 | 9000 |
| 15 | 5.6132 | 0.015784 | 10.7653 | 9.6500 | 1.0000 | 29.8300 | 9000 |

## Non-Coherent Random-Gap Table

| SNR (dB) | RMSE (deg) | Avg runtime / sample (s) | Mean gap (deg) | Median gap (deg) | Min gap (deg) | Max gap (deg) | Samples |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 5.2800 | 0.016356 | 10.6217 | 9.3550 | 1.0000 | 29.8900 | 9000 |
| 5 | 5.1517 | 0.015949 | 10.7583 | 9.6000 | 1.0000 | 29.6400 | 9000 |
| 10 | 4.9561 | 0.015989 | 10.6370 | 9.5000 | 1.0000 | 29.5100 | 9000 |
| 15 | 4.9746 | 0.015869 | 10.6634 | 9.4700 | 1.0000 | 29.6900 | 9000 |

## Bucket Summary

| Bucket | Cells | Mean RMSE (deg) | Median RMSE (deg) | Best RMSE (deg) | Worst RMSE (deg) | Mean runtime / sample (s) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| coherent_random_gap | 4 | 5.6449 | 5.6454 | 5.5513 | 5.7377 | 0.015943 |
| noncoherent_random_gap | 4 | 5.0906 | 5.0632 | 4.9561 | 5.2800 | 0.016040 |
| random_gap_generalization | 8 | 5.3678 | 5.4156 | 4.9561 | 5.7377 | 0.015992 |
