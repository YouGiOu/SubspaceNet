# Phase 7F - Group B 1.9 Lambda Mixed-Condition Fine-Tuning

Phase 7F fine-tunes the Phase 7D anti-rectifier fusion checkpoint on a 360k mixed-condition dataset and evaluates it on the reused Phase 7E coherent and non-coherent fixed-gap / SNR grids.

Experimental conditions:
- Array: Group B 12-channel 2D hardware geometry
- Physical spacing: 1.9 lambda
- Model family: SS(2/3 x 3) -> LRMC -> width-controlled anti-rectifier spatial fusion -> SubspaceNet backbone 3x3 -> ESPRIT
- Initialization: fine-tune from the best Phase 7D checkpoint
- Training schedule: 8 sequential fine-tuning stages
- Per-stage mixed dataset size: 45,000 total samples
- Per-stage split: 40,500 training / 4,500 test samples
- Approximate total samples seen across stages: 360,000
- Coherence weighting: 60% coherent, 40% non-coherent
- Evaluation set: same reused 40-cell grid as Phase 7E
- Primary metric: horizontal-angle RMSE in degrees
- Comparison focus: source-cell retention and delta vs Phase 7E

Reference anchor RMSE: `0.3592 deg`

## Header And Bucket Meanings

- `Delta vs anchor`:
  difference relative to the Phase `7D` source hard-cell reference RMSE of `0.3592 deg`.
  Negative means the Phase `7F` result is better than the original Phase `7D` anchor.
  Positive means it is worse.

- `Delta vs classical best`:
  difference relative to the best classical control from the Phase 6 fixed-gap / SNR grid that used the canonical Group B classical front end:
  - `SS -> LRMC`
  - followed by `DBF`, `MUSIC`, `Root-MUSIC`, or `ESPRIT`

  Important:
  these are not raw original `Root-MUSIC` / `ESPRIT` numbers on the non-uniform array.
  They are Phase 6 classical controls with preprocessing, except for `DBF`, which is naturally reported from the corresponding classical control run.

- `Delta vs direct learned`:
  difference relative to the earlier direct per-cell learned Phase 6 reference trained specifically for that exact cell.

- `Delta vs Phase 7E`:
  difference relative to the zero-shot transfer result from Phase `7E`.

- `coherent_ood`:
  all coherent reused evaluation cells except the in-domain anchor cell `gap = 1 deg`, `SNR = 1 dB`.

- `noncoherent_transfer` or `full_noncoherent_transfer`:
  all reused non-coherent evaluation cells.

- `snr_shift_only`:
  cells where gap stays at `1 deg` and only SNR shifts.

- `gap_shift_only`:
  cells where SNR stays at `1 dB` and only gap shifts.

- `joint_gap_snr_shift`:
  cells where both gap and SNR differ from the source training cell.

## Coherent Reused Grid

| Gap (deg) | SNR (dB) | RMSE (deg) | Avg runtime / sample (s) | Delta vs anchor | Delta vs classical best (`SS -> LRMC` Phase 6 control) | Delta vs direct learned | Delta vs Phase 7E | Cache status |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 1 | 0.4481 | 0.016274 | +0.0889 | -6.2003 | 0.0334 | 0.0918 | loaded |
| 1 | 5 | 0.3401 | 0.015964 | -0.0192 | -5.0968 | -0.0330 | -0.6219 | loaded |
| 1 | 10 | 0.3454 | 0.016257 | -0.0139 | -5.1187 | -0.0376 | -1.2037 | loaded |
| 1 | 15 | 0.3518 | 0.016082 | -0.0074 | -5.0817 | -0.0068 | -1.2610 | loaded |
| 2 | 1 | 1.3768 | 0.016310 | +1.0176 | -3.2106 | 0.3792 | -0.5937 | loaded |
| 2 | 5 | 1.2617 | 0.016339 | +0.9025 | -2.4250 | 0.4900 | -0.9221 | loaded |
| 2 | 10 | 1.2397 | 0.016256 | +0.8805 | -2.4727 | 0.5823 | -1.3508 | loaded |
| 2 | 15 | 1.2022 | 0.016404 | +0.8430 | -2.6580 | 0.5335 | -1.3944 | loaded |
| 3 | 1 | 0.5596 | 0.016246 | +0.2004 | -0.8592 | 0.0233 | -1.0398 | loaded |
| 3 | 5 | 0.4919 | 0.016119 | +0.1327 | -0.6922 | 0.1584 | -1.3450 | loaded |
| 3 | 10 | 0.4987 | 0.016048 | +0.1394 | -0.6465 | 0.2183 | -1.6288 | loaded |
| 3 | 15 | 0.4935 | 0.016036 | +0.1342 | -0.6160 | 0.2253 | -1.6775 | loaded |
| 4 | 1 | 0.3481 | 0.016300 | -0.0111 | 0.1841 | 0.1018 | -1.6363 | loaded |
| 4 | 5 | 0.2390 | 0.016232 | -0.1202 | 0.1340 | 0.0912 | -1.8572 | loaded |
| 4 | 10 | 0.2429 | 0.016354 | -0.1163 | 0.1428 | 0.1205 | -1.9947 | loaded |
| 4 | 15 | 0.2423 | 0.015717 | -0.1169 | 0.1422 | 0.1237 | -2.0081 | loaded |
| 5 | 1 | 0.8888 | 0.016463 | +0.5296 | -0.2240 | 0.5590 | -1.6860 | loaded |
| 5 | 5 | 0.6073 | 0.016332 | +0.2481 | -0.4591 | 0.3638 | -2.0110 | loaded |
| 5 | 10 | 0.5321 | 0.016114 | +0.1729 | -0.3869 | 0.3192 | -2.1858 | loaded |
| 5 | 15 | 0.4904 | 0.015745 | +0.1311 | -0.2206 | 0.2876 | -2.2341 | loaded |

## Non-Coherent Reused Grid

| Gap (deg) | SNR (dB) | RMSE (deg) | Avg runtime / sample (s) | Delta vs anchor | Delta vs classical best (`SS -> LRMC` Phase 6 control) | Delta vs direct learned | Delta vs Phase 7E | Cache status |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 1 | 0.3693 | 0.016602 | +0.0101 | -4.7130 | -0.0308 | 0.0356 | loaded |
| 1 | 5 | 0.2448 | 0.016431 | -0.1145 | -0.6796 | -0.1339 | -0.5994 | loaded |
| 1 | 10 | 0.2440 | 0.016102 | -0.1152 | -0.1725 | -0.1304 | -1.2767 | loaded |
| 1 | 15 | 0.2529 | 0.016129 | -0.1064 | -0.1702 | -0.1265 | -1.3576 | loaded |
| 2 | 1 | 0.2795 | 0.016632 | -0.0797 | -0.3414 | -0.2876 | -0.5473 | loaded |
| 2 | 5 | 0.2554 | 0.016364 | -0.1039 | 0.1257 | -0.2898 | -0.6411 | loaded |
| 2 | 10 | 0.2853 | 0.016175 | -0.0739 | 0.1741 | -0.2401 | -1.0068 | loaded |
| 2 | 15 | 0.2854 | 0.016293 | -0.0738 | 0.1750 | -0.2251 | -1.0563 | loaded |
| 3 | 1 | 0.3422 | 0.016399 | -0.0170 | 0.1795 | -0.1354 | -1.0862 | loaded |
| 3 | 5 | 0.3140 | 0.016243 | -0.0452 | 0.2080 | 0.0533 | -1.0790 | loaded |
| 3 | 10 | 0.3257 | 0.016319 | -0.0336 | 0.2268 | 0.1154 | -1.2425 | loaded |
| 3 | 15 | 0.3302 | 0.016216 | -0.0290 | 0.2317 | 0.1276 | -1.2707 | loaded |
| 4 | 1 | 0.4608 | 0.016482 | +0.1015 | 0.3234 | 0.0610 | -1.5790 | loaded |
| 4 | 5 | 0.3507 | 0.016417 | -0.0085 | 0.2530 | 0.1507 | -1.6700 | loaded |
| 4 | 10 | 0.3434 | 0.016297 | -0.0158 | 0.2503 | 0.1845 | -1.8080 | loaded |
| 4 | 15 | 0.3402 | 0.016279 | -0.0190 | 0.2477 | 0.1872 | -1.8311 | loaded |
| 5 | 1 | 0.8445 | 0.016450 | +0.4853 | 0.6989 | 0.5387 | -1.6926 | loaded |
| 5 | 5 | 0.5789 | 0.016350 | +0.2196 | 0.4729 | 0.3742 | -2.0314 | loaded |
| 5 | 10 | 0.5025 | 0.016129 | +0.1433 | 0.3993 | 0.3530 | -2.2012 | loaded |
| 5 | 15 | 0.5037 | 0.016346 | +0.1445 | 0.4009 | 0.3588 | -2.2240 | loaded |

## Retention Table

| Cell | RMSE (deg) | Delta vs anchor | Delta vs Phase 7E |
| --- | ---: | ---: | ---: |
| coherent | gap 1 | snr 1 | 0.4481 | +0.0889 | 0.0918 |
| coherent | gap 2 | snr 1 | 1.3768 | +1.0176 | -0.5937 |
| coherent | gap 2 | snr 5 | 1.2617 | +0.9025 | -0.9221 |
| non-coherent | gap 1 | snr 1 | 0.3693 | +0.0101 | 0.0356 |

## Bucket Summary

| Bucket | Cells | Mean RMSE (deg) | Median RMSE (deg) | Best RMSE (deg) | Worst RMSE (deg) | Mean runtime / sample (s) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| coherent_ood | 19 | 0.6185 | 0.4935 | 0.2390 | 1.3768 | 0.016175 |
| full_noncoherent_transfer | 20 | 0.3727 | 0.3352 | 0.2440 | 0.8445 | 0.016333 |
| gap_shift_only | 9 | 0.6077 | 0.4608 | 0.2795 | 1.3768 | 0.016432 |
| in_domain_anchor | 1 | 0.4481 | 0.4481 | 0.4481 | 0.4481 | 0.016274 |
| joint_gap_snr_shift | 24 | 0.4982 | 0.4205 | 0.2390 | 1.2617 | 0.016214 |
| noncoherent_transfer | 20 | 0.3727 | 0.3352 | 0.2440 | 0.8445 | 0.016333 |
| snr_shift_only | 7 | 0.3069 | 0.3401 | 0.2440 | 0.3693 | 0.016224 |

## Comparison Table

| Cell | Phase 6 classical best (`SS -> LRMC` control family) | RMSE (deg) | Avg runtime / sample (s) | Delta vs classical best | Direct Phase 6 learned RMSE (deg) | Delta vs direct learned | Phase 7E RMSE (deg) | Delta vs Phase 7E |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| coherent | gap 1 | snr 1 | esprit (6.6485) | 0.4481 | 0.016274 | -6.2003 | 0.4147 | +0.0334 | 0.3563 | +0.0918 |
| coherent | gap 1 | snr 5 | esprit (5.4369) | 0.3401 | 0.015964 | -5.0968 | 0.3731 | -0.0330 | 0.9620 | -0.6219 |
| coherent | gap 1 | snr 10 | esprit (5.4640) | 0.3454 | 0.016257 | -5.1187 | 0.3829 | -0.0376 | 1.5491 | -1.2037 |
| coherent | gap 1 | snr 15 | root-music (5.4335) | 0.3518 | 0.016082 | -5.0817 | 0.3586 | -0.0068 | 1.6128 | -1.2610 |
| coherent | gap 2 | snr 1 | esprit (4.5874) | 1.3768 | 0.016310 | -3.2106 | 0.9976 | +0.3792 | 1.9705 | -0.5937 |
| coherent | gap 2 | snr 5 | esprit (3.6867) | 1.2617 | 0.016339 | -2.4250 | 0.7717 | +0.4900 | 2.1838 | -0.9221 |
| coherent | gap 2 | snr 10 | esprit (3.7125) | 1.2397 | 0.016256 | -2.4727 | 0.6575 | +0.5823 | 2.5905 | -1.3508 |
| coherent | gap 2 | snr 15 | esprit (3.8603) | 1.2022 | 0.016404 | -2.6580 | 0.6687 | +0.5335 | 2.5966 | -1.3944 |
| coherent | gap 3 | snr 1 | esprit (1.4188) | 0.5596 | 0.016246 | -0.8592 | 0.5363 | +0.0233 | 1.5995 | -1.0398 |
| coherent | gap 3 | snr 5 | esprit (1.1842) | 0.4919 | 0.016119 | -0.6922 | 0.3335 | +0.1584 | 1.8369 | -1.3450 |
| coherent | gap 3 | snr 10 | esprit (1.1452) | 0.4987 | 0.016048 | -0.6465 | 0.2804 | +0.2183 | 2.1275 | -1.6288 |
| coherent | gap 3 | snr 15 | esprit (1.1095) | 0.4935 | 0.016036 | -0.6160 | 0.2681 | +0.2253 | 2.1709 | -1.6775 |
| coherent | gap 4 | snr 1 | root-music (0.1640) | 0.3481 | 0.016300 | +0.1841 | 0.2463 | +0.1018 | 1.9843 | -1.6363 |
| coherent | gap 4 | snr 5 | esprit (0.1050) | 0.2390 | 0.016232 | +0.1340 | 0.1478 | +0.0912 | 2.0963 | -1.8572 |
| coherent | gap 4 | snr 10 | esprit (0.1000) | 0.2429 | 0.016354 | +0.1428 | 0.1224 | +0.1205 | 2.2376 | -1.9947 |
| coherent | gap 4 | snr 15 | esprit (0.1001) | 0.2423 | 0.015717 | +0.1422 | 0.1186 | +0.1237 | 2.2504 | -2.0081 |
| coherent | gap 5 | snr 1 | dbf (1.1128) | 0.8888 | 0.016463 | -0.2240 | 0.3298 | +0.5590 | 2.5748 | -1.6860 |
| coherent | gap 5 | snr 5 | dbf (1.0664) | 0.6073 | 0.016332 | -0.4591 | 0.2436 | +0.3638 | 2.6183 | -2.0110 |
| coherent | gap 5 | snr 10 | dbf (0.9190) | 0.5321 | 0.016114 | -0.3869 | 0.2129 | +0.3192 | 2.7179 | -2.1858 |
| coherent | gap 5 | snr 15 | dbf (0.7110) | 0.4904 | 0.015745 | -0.2206 | 0.2027 | +0.2876 | 2.7245 | -2.2341 |
| non-coherent | gap 1 | snr 1 | esprit (5.0823) | 0.3693 | 0.016602 | -4.7130 | 0.4002 | -0.0308 | 0.3337 | +0.0356 |
| non-coherent | gap 1 | snr 5 | esprit (0.9243) | 0.2448 | 0.016431 | -0.6796 | 0.3787 | -0.1339 | 0.8442 | -0.5994 |
| non-coherent | gap 1 | snr 10 | esprit (0.4165) | 0.2440 | 0.016102 | -0.1725 | 0.3744 | -0.1304 | 1.5207 | -1.2767 |
| non-coherent | gap 1 | snr 15 | esprit (0.4230) | 0.2529 | 0.016129 | -0.1702 | 0.3794 | -0.1265 | 1.6105 | -1.3576 |
| non-coherent | gap 2 | snr 1 | esprit (0.6209) | 0.2795 | 0.016632 | -0.3414 | 0.5671 | -0.2876 | 0.8268 | -0.5473 |
| non-coherent | gap 2 | snr 5 | esprit (0.1297) | 0.2554 | 0.016364 | +0.1257 | 0.5452 | -0.2898 | 0.8965 | -0.6411 |
| non-coherent | gap 2 | snr 10 | esprit (0.1112) | 0.2853 | 0.016175 | +0.1741 | 0.5254 | -0.2401 | 1.2922 | -1.0068 |
| non-coherent | gap 2 | snr 15 | esprit (0.1104) | 0.2854 | 0.016293 | +0.1750 | 0.5105 | -0.2251 | 1.3417 | -1.0563 |
| non-coherent | gap 3 | snr 1 | root-music (0.1627) | 0.3422 | 0.016399 | +0.1795 | 0.4776 | -0.1354 | 1.4284 | -1.0862 |
| non-coherent | gap 3 | snr 5 | esprit (0.1060) | 0.3140 | 0.016243 | +0.2080 | 0.2607 | +0.0533 | 1.3930 | -1.0790 |
| non-coherent | gap 3 | snr 10 | esprit (0.0988) | 0.3257 | 0.016319 | +0.2268 | 0.2102 | +0.1154 | 1.5682 | -1.2425 |
| non-coherent | gap 3 | snr 15 | esprit (0.0985) | 0.3302 | 0.016216 | +0.2317 | 0.2026 | +0.1276 | 1.6009 | -1.2707 |
| non-coherent | gap 4 | snr 1 | root-music (0.1373) | 0.4608 | 0.016482 | +0.3234 | 0.3997 | +0.0610 | 2.0398 | -1.5790 |
| non-coherent | gap 4 | snr 5 | esprit (0.0978) | 0.3507 | 0.016417 | +0.2530 | 0.2000 | +0.1507 | 2.0207 | -1.6700 |
| non-coherent | gap 4 | snr 10 | esprit (0.0931) | 0.3434 | 0.016297 | +0.2503 | 0.1589 | +0.1845 | 2.1514 | -1.8080 |
| non-coherent | gap 4 | snr 15 | esprit (0.0925) | 0.3402 | 0.016279 | +0.2477 | 0.1530 | +0.1872 | 2.1713 | -1.8311 |
| non-coherent | gap 5 | snr 1 | root-music (0.1456) | 0.8445 | 0.016450 | +0.6989 | 0.3058 | +0.5387 | 2.5371 | -1.6926 |
| non-coherent | gap 5 | snr 5 | dbf (0.1060) | 0.5789 | 0.016350 | +0.4729 | 0.2047 | +0.3742 | 2.6103 | -2.0314 |
| non-coherent | gap 5 | snr 10 | dbf (0.1033) | 0.5025 | 0.016129 | +0.3993 | 0.1495 | +0.3530 | 2.7037 | -2.2012 |
| non-coherent | gap 5 | snr 15 | dbf (0.1029) | 0.5037 | 0.016346 | +0.4009 | 0.1449 | +0.3588 | 2.7278 | -2.2240 |

## Raw No-Preprocessing Reference

The `Phase 6 classical best` column above refers to the preprocessed classical controls from:
- coherent: Phase `6` with `SS -> LRMC`
- non-coherent: Phase `6` with `SS -> LRMC`

It does **not** refer to the raw original shift-invariant methods on the non-uniform array.

Those raw no-preprocessing references were run separately in:
- [phase6b_groupb_1p9_coherent_fixed_gap_snr_grid_no_preproc_results.md](/d:/workspace1/SubspaceNet/results/phase6b_groupb_1p9_coherent_fixed_gap_snr_grid_no_preproc/phase6b_groupb_1p9_coherent_fixed_gap_snr_grid_no_preproc_results.md)
- [phase6_groupb_1p9_noncoherent_fixed_gap_snr_grid_no_preproc_results.md](/d:/workspace1/SubspaceNet/results/phase6_groupb_1p9_noncoherent_fixed_gap_snr_grid_no_preproc/phase6_groupb_1p9_noncoherent_fixed_gap_snr_grid_no_preproc_results.md)

These runs confirm the earlier project conclusion that pure original `Root-MUSIC` and `ESPRIT` are poor on the Group B non-uniform array without preprocessing.

### Raw `Root-MUSIC` / `ESPRIT` RMSE Ranges Without Preprocessing

| Regime | Raw Root-MUSIC RMSE range (deg) | Raw ESPRIT RMSE range (deg) |
| --- | ---: | ---: |
| Coherent Group B `1.9 lambda` | `8.2488 - 10.6188` | `7.9130 - 10.6934` |
| Non-coherent Group B `1.9 lambda` | `7.0409 - 8.6494` | `7.5419 - 8.6244` |

### Representative Raw No-Preprocessing Reference Cells

| Regime | Cell | Raw Root-MUSIC (deg) | Raw ESPRIT (deg) |
| --- | --- | ---: | ---: |
| Coherent | gap `1`, snr `1` | `10.4446` | `10.5181` |
| Coherent | gap `4`, snr `1` | `8.3065` | `7.9130` |
| Coherent | gap `5`, snr `15` | `8.2474` | `8.2408` |
| Non-coherent | gap `1`, snr `1` | `8.6494` | `8.0267` |
| Non-coherent | gap `2`, snr `5` | `7.3458` | `7.6602` |
| Non-coherent | gap `5`, snr `15` | `7.0409` | `7.5389` |

Interpretation:
- yes, the earlier recollection was correct
- on this non-uniform Group B array, raw `Root-MUSIC` and raw `ESPRIT` perform very poorly without preprocessing
- the much stronger Phase 6 classical `Root-MUSIC` / `ESPRIT` numbers used in the main comparison come from the `SS -> LRMC` front end, not from the raw original methods
