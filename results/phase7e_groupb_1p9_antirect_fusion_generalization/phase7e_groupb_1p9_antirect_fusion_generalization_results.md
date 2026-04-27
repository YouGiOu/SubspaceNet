# Phase 7E - Group B 1.9 Lambda Anti-Rectifier Fusion Generalization

Phase 7E evaluates the already trained Phase 7D anti-rectifier SS-fusion `3x3` model on reused cached Phase 6 test datasets across the coherent and non-coherent fixed-gap / SNR grids without retraining.

Experimental conditions:
- Array: Group B 12-channel 2D hardware geometry
- Physical spacing: 1.9 lambda
- Snapshots: T = 40
- Learned pipeline: SS(2/3 x 3) -> LRMC -> width-controlled anti-rectifier spatial fusion -> SubspaceNet backbone 3x3 -> ESPRIT
- Evaluation set: 20 coherent cells + 20 non-coherent cells
- Reuse rule: cached generic test snapshots reused when available; missing datasets are generated only as fallback by the core test runner
- Primary metric: horizontal-angle RMSE in degrees
- Runtime metric: end-to-end preprocessing plus learned inference path

Training-cell reference RMSE: `0.3592 deg`

## Coherent Reused Grid

| Gap (deg) | SNR (dB) | RMSE (deg) | Avg runtime / sample (s) | Delta vs training cell | Delta vs classical best | Delta vs direct learned | Cache status |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 1 | 0.3563 | 0.016863 | -0.0029 | -6.2922 | -0.0584 | generated |
| 1 | 5 | 0.9620 | 0.016282 | +0.6027 | -4.4749 | 0.5888 | generated |
| 1 | 10 | 1.5491 | 0.016475 | +1.1899 | -3.9150 | 1.1662 | generated |
| 1 | 15 | 1.6128 | 0.016393 | +1.2536 | -3.8207 | 1.2542 | generated |
| 2 | 1 | 1.9705 | 0.016481 | +1.6113 | -2.6169 | 0.9729 | generated |
| 2 | 5 | 2.1838 | 0.016612 | +1.8246 | -1.5029 | 1.4121 | generated |
| 2 | 10 | 2.5905 | 0.016428 | +2.2313 | -1.1220 | 1.9330 | generated |
| 2 | 15 | 2.5966 | 0.016401 | +2.2373 | -1.2637 | 1.9278 | generated |
| 3 | 1 | 1.5995 | 0.016531 | +1.2402 | 0.1806 | 1.0632 | generated |
| 3 | 5 | 1.8369 | 0.016308 | +1.4777 | 0.6527 | 1.5034 | generated |
| 3 | 10 | 2.1275 | 0.016146 | +1.7682 | 0.9823 | 1.8471 | generated |
| 3 | 15 | 2.1709 | 0.016081 | +1.8117 | 1.0615 | 1.9028 | generated |
| 4 | 1 | 1.9843 | 0.016279 | +1.6251 | 1.8203 | 1.7381 | generated |
| 4 | 5 | 2.0963 | 0.016278 | +1.7370 | 1.9912 | 1.9485 | generated |
| 4 | 10 | 2.2376 | 0.016083 | +1.8783 | 2.1375 | 2.1151 | generated |
| 4 | 15 | 2.2504 | 0.015850 | +1.8912 | 2.1503 | 2.1318 | generated |
| 5 | 1 | 2.5748 | 0.016570 | +2.2156 | 1.4620 | 2.2450 | generated |
| 5 | 5 | 2.6183 | 0.016364 | +2.2591 | 1.5519 | 2.3747 | generated |
| 5 | 10 | 2.7179 | 0.016036 | +2.3587 | 1.7989 | 2.5050 | generated |
| 5 | 15 | 2.7245 | 0.016011 | +2.3653 | 2.0135 | 2.5218 | generated |

## Non-Coherent Reused Grid

| Gap (deg) | SNR (dB) | RMSE (deg) | Avg runtime / sample (s) | Delta vs training cell | Delta vs classical best | Delta vs direct learned | Cache status |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 1 | 0.3337 | 0.016711 | -0.0255 | -4.7486 | -0.0664 | generated |
| 1 | 5 | 0.8442 | 0.016472 | +0.4850 | -0.0801 | 0.4655 | generated |
| 1 | 10 | 1.5207 | 0.016290 | +1.1615 | 1.1042 | 1.1463 | generated |
| 1 | 15 | 1.6105 | 0.016367 | +1.2513 | 1.1875 | 1.2311 | generated |
| 2 | 1 | 0.8268 | 0.016600 | +0.4675 | 0.2058 | 0.2597 | generated |
| 2 | 5 | 0.8965 | 0.016324 | +0.5373 | 0.7668 | 0.3513 | generated |
| 2 | 10 | 1.2922 | 0.016283 | +0.9329 | 1.1810 | 0.7668 | generated |
| 2 | 15 | 1.3417 | 0.016248 | +0.9825 | 1.2313 | 0.8312 | generated |
| 3 | 1 | 1.4284 | 0.016702 | +1.0692 | 1.2657 | 0.9508 | generated |
| 3 | 5 | 1.3930 | 0.016514 | +1.0337 | 1.2870 | 1.1323 | generated |
| 3 | 10 | 1.5682 | 0.016395 | +1.2090 | 1.4694 | 1.3580 | generated |
| 3 | 15 | 1.6009 | 0.016389 | +1.2417 | 1.5024 | 1.3983 | generated |
| 4 | 1 | 2.0398 | 0.016600 | +1.6806 | 1.9024 | 1.6401 | generated |
| 4 | 5 | 2.0207 | 0.016492 | +1.6615 | 1.9230 | 1.8208 | generated |
| 4 | 10 | 2.1514 | 0.016342 | +1.7922 | 2.0583 | 1.9926 | generated |
| 4 | 15 | 2.1713 | 0.016424 | +1.8121 | 2.0788 | 2.0183 | generated |
| 5 | 1 | 2.5371 | 0.016595 | +2.1778 | 2.3915 | 2.2313 | generated |
| 5 | 5 | 2.6103 | 0.016452 | +2.2511 | 2.5043 | 2.4056 | generated |
| 5 | 10 | 2.7037 | 0.016419 | +2.3445 | 2.6004 | 2.5542 | generated |
| 5 | 15 | 2.7278 | 0.016291 | +2.3686 | 2.6249 | 2.5829 | generated |

## Bucket Summary

| Bucket | Cells | Mean RMSE (deg) | Median RMSE (deg) | Best RMSE (deg) | Worst RMSE (deg) | Mean runtime / sample (s) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| coherent_ood | 19 | 2.1265 | 2.1709 | 0.9620 | 2.7245 | 0.016295 |
| full_noncoherent_transfer | 20 | 1.6809 | 1.5845 | 0.3337 | 2.7278 | 0.016446 |
| gap_shift_only | 9 | 1.6994 | 1.9705 | 0.3337 | 2.5748 | 0.016563 |
| in_domain_anchor | 1 | 0.3563 | 0.3563 | 0.3563 | 0.3563 | 0.016863 |
| joint_gap_snr_shift | 24 | 2.1095 | 2.1711 | 0.8965 | 2.7278 | 0.016299 |
| noncoherent_transfer | 20 | 1.6809 | 1.5845 | 0.3337 | 2.7278 | 0.016446 |
| snr_shift_only | 7 | 1.2047 | 1.5207 | 0.3337 | 1.6128 | 0.016427 |

## Comparison Table

| Cell | Phase 6 classical best | Transferred RMSE (deg) | Avg runtime / sample (s) | Delta vs classical best | Direct Phase 6 learned RMSE (deg) | Delta vs direct learned |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| coherent | gap 1 | snr 1 | esprit (6.6485) | 0.3563 | 0.016863 | -6.2922 | 0.4147 | -0.0584 |
| coherent | gap 1 | snr 5 | esprit (5.4369) | 0.9620 | 0.016282 | -4.4749 | 0.3731 | +0.5888 |
| coherent | gap 1 | snr 10 | esprit (5.4640) | 1.5491 | 0.016475 | -3.9150 | 0.3829 | +1.1662 |
| coherent | gap 1 | snr 15 | root-music (5.4335) | 1.6128 | 0.016393 | -3.8207 | 0.3586 | +1.2542 |
| coherent | gap 2 | snr 1 | esprit (4.5874) | 1.9705 | 0.016481 | -2.6169 | 0.9976 | +0.9729 |
| coherent | gap 2 | snr 5 | esprit (3.6867) | 2.1838 | 0.016612 | -1.5029 | 0.7717 | +1.4121 |
| coherent | gap 2 | snr 10 | esprit (3.7125) | 2.5905 | 0.016428 | -1.1220 | 0.6575 | +1.9330 |
| coherent | gap 2 | snr 15 | esprit (3.8603) | 2.5966 | 0.016401 | -1.2637 | 0.6687 | +1.9278 |
| coherent | gap 3 | snr 1 | esprit (1.4188) | 1.5995 | 0.016531 | +0.1806 | 0.5363 | +1.0632 |
| coherent | gap 3 | snr 5 | esprit (1.1842) | 1.8369 | 0.016308 | +0.6527 | 0.3335 | +1.5034 |
| coherent | gap 3 | snr 10 | esprit (1.1452) | 2.1275 | 0.016146 | +0.9823 | 0.2804 | +1.8471 |
| coherent | gap 3 | snr 15 | esprit (1.1095) | 2.1709 | 0.016081 | +1.0615 | 0.2681 | +1.9028 |
| coherent | gap 4 | snr 1 | root-music (0.1640) | 1.9843 | 0.016279 | +1.8203 | 0.2463 | +1.7381 |
| coherent | gap 4 | snr 5 | esprit (0.1050) | 2.0963 | 0.016278 | +1.9912 | 0.1478 | +1.9485 |
| coherent | gap 4 | snr 10 | esprit (0.1000) | 2.2376 | 0.016083 | +2.1375 | 0.1224 | +2.1151 |
| coherent | gap 4 | snr 15 | esprit (0.1001) | 2.2504 | 0.015850 | +2.1503 | 0.1186 | +2.1318 |
| coherent | gap 5 | snr 1 | dbf (1.1128) | 2.5748 | 0.016570 | +1.4620 | 0.3298 | +2.2450 |
| coherent | gap 5 | snr 5 | dbf (1.0664) | 2.6183 | 0.016364 | +1.5519 | 0.2436 | +2.3747 |
| coherent | gap 5 | snr 10 | dbf (0.9190) | 2.7179 | 0.016036 | +1.7989 | 0.2129 | +2.5050 |
| coherent | gap 5 | snr 15 | dbf (0.7110) | 2.7245 | 0.016011 | +2.0135 | 0.2027 | +2.5218 |
| non-coherent | gap 1 | snr 1 | esprit (5.0823) | 0.3337 | 0.016711 | -4.7486 | 0.4002 | -0.0664 |
| non-coherent | gap 1 | snr 5 | esprit (0.9243) | 0.8442 | 0.016472 | -0.0801 | 0.3787 | +0.4655 |
| non-coherent | gap 1 | snr 10 | esprit (0.4165) | 1.5207 | 0.016290 | +1.1042 | 0.3744 | +1.1463 |
| non-coherent | gap 1 | snr 15 | esprit (0.4230) | 1.6105 | 0.016367 | +1.1875 | 0.3794 | +1.2311 |
| non-coherent | gap 2 | snr 1 | esprit (0.6209) | 0.8268 | 0.016600 | +0.2058 | 0.5671 | +0.2597 |
| non-coherent | gap 2 | snr 5 | esprit (0.1297) | 0.8965 | 0.016324 | +0.7668 | 0.5452 | +0.3513 |
| non-coherent | gap 2 | snr 10 | esprit (0.1112) | 1.2922 | 0.016283 | +1.1810 | 0.5254 | +0.7668 |
| non-coherent | gap 2 | snr 15 | esprit (0.1104) | 1.3417 | 0.016248 | +1.2313 | 0.5105 | +0.8312 |
| non-coherent | gap 3 | snr 1 | root-music (0.1627) | 1.4284 | 0.016702 | +1.2657 | 0.4776 | +0.9508 |
| non-coherent | gap 3 | snr 5 | esprit (0.1060) | 1.3930 | 0.016514 | +1.2870 | 0.2607 | +1.1323 |
| non-coherent | gap 3 | snr 10 | esprit (0.0988) | 1.5682 | 0.016395 | +1.4694 | 0.2102 | +1.3580 |
| non-coherent | gap 3 | snr 15 | esprit (0.0985) | 1.6009 | 0.016389 | +1.5024 | 0.2026 | +1.3983 |
| non-coherent | gap 4 | snr 1 | root-music (0.1373) | 2.0398 | 0.016600 | +1.9024 | 0.3997 | +1.6401 |
| non-coherent | gap 4 | snr 5 | esprit (0.0978) | 2.0207 | 0.016492 | +1.9230 | 0.2000 | +1.8208 |
| non-coherent | gap 4 | snr 10 | esprit (0.0931) | 2.1514 | 0.016342 | +2.0583 | 0.1589 | +1.9926 |
| non-coherent | gap 4 | snr 15 | esprit (0.0925) | 2.1713 | 0.016424 | +2.0788 | 0.1530 | +2.0183 |
| non-coherent | gap 5 | snr 1 | root-music (0.1456) | 2.5371 | 0.016595 | +2.3915 | 0.3058 | +2.2313 |
| non-coherent | gap 5 | snr 5 | dbf (0.1060) | 2.6103 | 0.016452 | +2.5043 | 0.2047 | +2.4056 |
| non-coherent | gap 5 | snr 10 | dbf (0.1033) | 2.7037 | 0.016419 | +2.6004 | 0.1495 | +2.5542 |
| non-coherent | gap 5 | snr 15 | dbf (0.1029) | 2.7278 | 0.016291 | +2.6249 | 0.1449 | +2.5829 |
