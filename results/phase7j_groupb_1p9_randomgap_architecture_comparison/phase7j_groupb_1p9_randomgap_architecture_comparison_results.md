# Phase 7J - Group B 1.9 Lambda Random-Gap Architecture Comparison

Phase 7J compares three from-scratch SubspaceNet-era architectures under the same 45,000-sample random-gap training recipe and the same fixed-gap plus random-gap evaluation families.

Experimental conditions:
- Array: Group B 12-channel 2D hardware geometry
- Physical spacing: 1.9 lambda
- Signals: 2 narrowband sources, 60% coherent / 40% non-coherent training mix
- Snapshots: T = 40
- Training set: 45,000 samples with a 40,500 / 4,500 train:test split
- Dataset mix: 50% structured protection + 50% continuous random-gap samples
- Structured coherent gap weights: 25/35/20/10/10 for gaps 1/2/3/4/5 deg
- Structured non-coherent gap weights: 25/30/20/15/10 for gaps 1/2/3/4/5 deg
- Random-gap bins: 1-2, 2-3, 3-5, 5-10, 10-29 deg
- Shared SNR weights: 35/30/20/15 for 1/5/10/15 dB
- Training mode: one uninterrupted 80-epoch run per model, from scratch
- Evaluation: reused 40-cell fixed-gap grid plus 8 random-gap cells

## Architecture Overview

| Model | Input path | Backbone | Fusion type | Training mode | Epochs |
| --- | --- | --- | --- | --- | ---: |
| Model C (C) | single-row linear-array covariance | 2x2 | none | from scratch | 80 |
| Model A (A) | SS(3/3) -> LRMC virtual ULA | 2x2 | none | from scratch | 80 |
| Model B (B) | SS(2/3 x 3) -> LRMC branch fusion | 3x3 | anti-rectifier spatial fusion | from scratch | 80 |

## Random-Gap Comparison

| Coherence | SNR (dB) | Model C RMSE | Model A RMSE | Model B RMSE | Delta A-C | Delta B-A | Delta B-C |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| coherent | 1 | 6.6067 | 5.0589 | 5.2194 | -1.5478 | +0.1605 | -1.3873 |
| coherent | 5 | 6.5231 | 4.9448 | 4.8010 | -1.5783 | -0.1437 | -1.7221 |
| coherent | 10 | 6.5010 | 4.8870 | 4.4829 | -1.6140 | -0.4041 | -2.0181 |
| coherent | 15 | 6.5669 | 4.9803 | 4.6291 | -1.5866 | -0.3512 | -1.9378 |
| non-coherent | 1 | 5.3135 | 4.6425 | 4.7814 | -0.6711 | +0.1389 | -0.5321 |
| non-coherent | 5 | 5.1411 | 4.4668 | 4.2991 | -0.6743 | -0.1677 | -0.8420 |
| non-coherent | 10 | 5.0768 | 4.4085 | 3.9846 | -0.6683 | -0.4240 | -1.0923 |
| non-coherent | 15 | 5.1143 | 4.4731 | 3.9853 | -0.6413 | -0.4877 | -1.1290 |

## Coherent 2-Degree Boundary

| SNR (dB) | Model C RMSE | Model A RMSE | Model B RMSE | Delta A-C | Delta B-A | Delta B-C |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 6.7351 | 1.9550 | 2.0226 | -4.7801 | +0.0676 | -4.7125 |
| 5 | 6.0349 | 1.7185 | 1.6951 | -4.3164 | -0.0234 | -4.3398 |
| 10 | 5.9195 | 1.6962 | 1.6641 | -4.2234 | -0.0321 | -4.2554 |
| 15 | 5.7662 | 1.6399 | 1.5926 | -4.1262 | -0.0473 | -4.1736 |

## Source-Cell Anchor

| Cell | Model C RMSE | Model A RMSE | Model B RMSE |
| --- | ---: | ---: | ---: |
| coherent, gap 1 deg, SNR 1 dB | 1.4384 | 0.9062 | 1.3451 |

## Summary Bucket Table

| Bucket | Model C mean RMSE | Model A mean RMSE | Model B mean RMSE |
| --- | ---: | ---: | ---: |
| in_domain_anchor | 1.4384 | 0.9062 | 1.3451 |
| coherent_2deg_boundary | 6.1139 | 1.7524 | 1.7436 |
| coherent_ood | 2.5026 | 1.0855 | 1.1574 |
| noncoherent_transfer | 1.4310 | 0.7244 | 0.7478 |
| coherent_random_gap | 6.5494 | 4.9677 | 4.7831 |
| noncoherent_random_gap | 5.1615 | 4.4977 | 4.2626 |
