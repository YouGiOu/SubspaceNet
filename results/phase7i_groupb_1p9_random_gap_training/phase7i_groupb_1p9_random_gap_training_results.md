# Phase 7I - Group B 1.9 Lambda Random-Gap Training

Phase 7I fine-tunes the Phase 7G boundary-repair model with a staged structured-plus-random-gap curriculum, then evaluates both fixed-gap retention and random-gap generalization in one combined results family.

Experimental conditions:
- Array: Group B 12-channel 2D hardware geometry
- Physical spacing: 1.9 lambda
- Model family: SS(2/3 x 3) -> LRMC -> width-controlled anti-rectifier spatial fusion -> SubspaceNet backbone 3x3 -> ESPRIT
- Initialization: fine-tune from the best Phase 7G checkpoint
- Training schedule: 3 sequential stages x 45,000 samples
- Per-stage split: 36,000 train / 9,000 held-out
- Structured/random stage mix: 31.5k/13.5k -> 24.8k/20.2k -> 18k/27k
- Random-gap rule: low-gap-biased continuous sampling with min_doa_gap = 1 deg
- Evaluation set: 40 fixed-gap cells plus 8 random-gap cells
- Primary metrics: fixed-gap retention and random-gap RMSE

Reference anchor RMSE: `0.3592 deg`

## Random-Gap Comparison

| Coherence | SNR (dB) | Phase 7H RMSE (deg) | Phase 7I RMSE (deg) | Delta vs Phase 7H |
| --- | ---: | ---: | ---: | ---: |
| coherent | 1 | 5.7377 | 4.2613 | -1.4765 |
| coherent | 5 | 5.6775 | 4.1244 | -1.5531 |
| coherent | 10 | 5.5513 | 4.0606 | -1.4907 |
| coherent | 15 | 5.6132 | 4.1196 | -1.4936 |
| non-coherent | 1 | 5.2800 | 3.6617 | -1.6183 |
| non-coherent | 5 | 5.1517 | 3.5491 | -1.6025 |
| non-coherent | 10 | 4.9561 | 3.4018 | -1.5543 |
| non-coherent | 15 | 4.9746 | 3.4530 | -1.5216 |

## Coherent 2-Degree Protection

| SNR (dB) | Phase 7G RMSE (deg) | Phase 7I RMSE (deg) | Delta vs Phase 7G |
| ---: | ---: | ---: | ---: |
| 1 | 1.2918 | 1.4158 | +0.1240 |
| 5 | 1.1271 | 1.2475 | +0.1204 |
| 10 | 1.0751 | 1.1628 | +0.0877 |
| 15 | 1.0423 | 1.1352 | +0.0929 |

## Source-Cell Retention

| Cell | Phase 7F | Phase 7G | Phase 7I | Delta vs Phase 7G |
| --- | ---: | ---: | ---: | ---: |
| coherent | gap 1 | snr 1 | 0.4481 | 0.3911 | 0.5042 | +0.1131 |
| coherent | gap 2 | snr 1 | 1.3768 | 1.2918 | 1.4158 | +0.1240 |
| coherent | gap 2 | snr 5 | 1.2617 | 1.1271 | 1.2475 | +0.1204 |
| coherent | gap 2 | snr 10 | 1.2397 | 1.0751 | 1.1628 | +0.0877 |
| coherent | gap 2 | snr 15 | 1.2022 | 1.0423 | 1.1352 | +0.0929 |
| coherent | gap 3 | snr 5 | 0.4919 | 0.4454 | 0.5457 | +0.1004 |
| non-coherent | gap 1 | snr 1 | 0.3693 | 0.3166 | 0.4010 | +0.0845 |
| non-coherent | gap 2 | snr 5 | 0.2554 | 0.2312 | 0.2179 | -0.0133 |

## Coherent Fixed-Gap Grid

| Gap (deg) | SNR (dB) | RMSE (deg) | Delta vs Phase 7G | Delta vs Phase 7F | Avg runtime / sample (s) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 1 | 0.5042 | 0.1131 | 0.0561 | 0.016196 |
| 1 | 5 | 0.3713 | 0.0686 | 0.0313 | 0.015849 |
| 1 | 10 | 0.3880 | 0.0791 | 0.0427 | 0.016053 |
| 1 | 15 | 0.3958 | 0.0823 | 0.0440 | 0.016019 |
| 2 | 1 | 1.4158 | 0.1240 | 0.0390 | 0.016198 |
| 2 | 5 | 1.2475 | 0.1204 | -0.0142 | 0.016159 |
| 2 | 10 | 1.1628 | 0.0877 | -0.0769 | 0.016160 |
| 2 | 15 | 1.1352 | 0.0929 | -0.0670 | 0.016155 |
| 3 | 1 | 0.6454 | 0.1104 | 0.0858 | 0.016291 |
| 3 | 5 | 0.5457 | 0.1004 | 0.0538 | 0.016038 |
| 3 | 10 | 0.5305 | 0.0996 | 0.0318 | 0.015952 |
| 3 | 15 | 0.5317 | 0.1016 | 0.0382 | 0.015793 |
| 4 | 1 | 0.3657 | -0.0099 | 0.0176 | 0.016109 |
| 4 | 5 | 0.2615 | 0.0209 | 0.0225 | 0.016032 |
| 4 | 10 | 0.2499 | 0.0186 | 0.0070 | 0.015846 |
| 4 | 15 | 0.2514 | 0.0224 | 0.0091 | 0.015634 |
| 5 | 1 | 0.8347 | -0.1297 | -0.0540 | 0.016281 |
| 5 | 5 | 0.6019 | -0.0865 | -0.0055 | 0.016072 |
| 5 | 10 | 0.5536 | -0.0674 | 0.0215 | 0.015800 |
| 5 | 15 | 0.5235 | -0.0635 | 0.0332 | 0.015605 |

## Non-Coherent Fixed-Gap Grid

| Gap (deg) | SNR (dB) | RMSE (deg) | Delta vs Phase 7G | Delta vs Phase 7F | Avg runtime / sample (s) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 1 | 0.4010 | 0.0845 | 0.0317 | 0.016345 |
| 1 | 5 | 0.2868 | 0.0666 | 0.0421 | 0.016154 |
| 1 | 10 | 0.2770 | 0.0508 | 0.0330 | 0.015929 |
| 1 | 15 | 0.2855 | 0.0499 | 0.0326 | 0.016003 |
| 2 | 1 | 0.2769 | 0.0169 | -0.0026 | 0.016331 |
| 2 | 5 | 0.2179 | -0.0133 | -0.0374 | 0.016107 |
| 2 | 10 | 0.2298 | -0.0233 | -0.0555 | 0.016010 |
| 2 | 15 | 0.2284 | -0.0249 | -0.0571 | 0.015921 |
| 3 | 1 | 0.3616 | 0.0053 | 0.0193 | 0.016309 |
| 3 | 5 | 0.3069 | -0.0080 | -0.0071 | 0.016206 |
| 3 | 10 | 0.3048 | -0.0166 | -0.0209 | 0.016109 |
| 3 | 15 | 0.3039 | -0.0208 | -0.0263 | 0.016197 |
| 4 | 1 | 0.4654 | -0.0400 | 0.0046 | 0.016348 |
| 4 | 5 | 0.3710 | -0.0031 | 0.0203 | 0.016229 |
| 4 | 10 | 0.3609 | 0.0025 | 0.0175 | 0.016212 |
| 4 | 15 | 0.3551 | 0.0036 | 0.0149 | 0.016147 |
| 5 | 1 | 0.7378 | -0.1723 | -0.1067 | 0.016293 |
| 5 | 5 | 0.5260 | -0.1142 | -0.0529 | 0.016270 |
| 5 | 10 | 0.4826 | -0.0833 | -0.0200 | 0.016060 |
| 5 | 15 | 0.4913 | -0.0769 | -0.0124 | 0.016107 |

## Coherent Random-Gap Table

| SNR (dB) | Phase 7H RMSE (deg) | Phase 7I RMSE (deg) | Delta vs Phase 7H | Mean gap (deg) | Median gap (deg) | Min gap (deg) | Max gap (deg) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 5.7377 | 4.2613 | -1.4765 | 10.6000 | 9.3400 | 1.0000 | 29.7400 |
| 5 | 5.6775 | 4.1244 | -1.5531 | 10.7088 | 9.5900 | 1.0000 | 29.6900 |
| 10 | 5.5513 | 4.0606 | -1.4907 | 10.5667 | 9.3100 | 1.0000 | 29.7900 |
| 15 | 5.6132 | 4.1196 | -1.4936 | 10.7653 | 9.6500 | 1.0000 | 29.8300 |

## Non-Coherent Random-Gap Table

| SNR (dB) | Phase 7H RMSE (deg) | Phase 7I RMSE (deg) | Delta vs Phase 7H | Mean gap (deg) | Median gap (deg) | Min gap (deg) | Max gap (deg) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 5.2800 | 3.6617 | -1.6183 | 10.6217 | 9.3550 | 1.0000 | 29.8900 |
| 5 | 5.1517 | 3.5491 | -1.6025 | 10.7583 | 9.6000 | 1.0000 | 29.6400 |
| 10 | 4.9561 | 3.4018 | -1.5543 | 10.6370 | 9.5000 | 1.0000 | 29.5100 |
| 15 | 4.9746 | 3.4530 | -1.5216 | 10.6634 | 9.4700 | 1.0000 | 29.6900 |

## Bucket Summary

| Bucket | Cells | Mean RMSE (deg) | Median RMSE (deg) | Best RMSE (deg) | Worst RMSE (deg) | Mean runtime / sample (s) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| coherent_2deg_boundary | 4 | 1.2403 | 1.2052 | 1.1352 | 1.4158 | 0.016168 |
| coherent_ood | 19 | 0.6322 | 0.5317 | 0.2499 | 1.4158 | 0.016002 |
| coherent_random_gap | 4 | 4.1415 | 4.1220 | 4.0606 | 4.2613 | 0.016085 |
| in_domain_anchor | 1 | 0.5042 | 0.5042 | 0.5042 | 0.5042 | 0.016196 |
| noncoherent_random_gap | 4 | 3.5164 | 3.5011 | 3.4018 | 3.6617 | 0.016222 |
| noncoherent_transfer | 20 | 0.3635 | 0.3310 | 0.2179 | 0.7378 | 0.016164 |
