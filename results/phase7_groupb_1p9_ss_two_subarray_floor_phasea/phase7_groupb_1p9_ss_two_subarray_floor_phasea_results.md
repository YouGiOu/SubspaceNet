# Phase 7A - Group B 1.9 Lambda Two-Subarray Spatial Smoothing Floor Screening

Phase 7A screens whether reducing Group B rowwise spatial smoothing from three row blocks to specific two-of-three row pairs materially changes classical SS -> LRMC performance under representative coherent and non-coherent difficulty cells.

Experimental conditions:
- Stage: A classical-first screening
- Array: Group B 12-channel 2D hardware geometry
- Physical spacing: 1.9 lambda
- Signals: 2 coherent narrowband targets
- Snapshots: T = 40
- Azimuth and elevation range: [-15 deg, 15 deg]
- Gap/SNR cells: (1 deg, 1 dB), (2 deg, 1 dB), (1 deg, 10 dB), (3 deg, 10 dB), (5 deg, 10 dB)
- Preprocessing family: rowwise SS -> LRMC
- SS variants: full 3/3 baseline and all three 2/3 row-pair choices
- Control methods: DBF, MUSIC, Root-MUSIC, ESPRIT
- Dataset size per cell: 10,000 samples total with 2,000 test samples
- Metric: horizontal-angle RMSE in degrees (periodic matching)

| Algorithm | RMSE (deg) |
| --- | ---: |
| Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 0+1) -> LRMC | DBF | 7.8367 |
| Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 0+1) -> LRMC | ESPRIT | 4.2093 |
| Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 0+1) -> LRMC | MUSIC | 6.4984 |
| Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 0+1) -> LRMC | Root-MUSIC | 4.7042 |
| Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 0+2) -> LRMC | DBF | 7.7207 |
| Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 0+2) -> LRMC | ESPRIT | 7.0196 |
| Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 0+2) -> LRMC | MUSIC | 7.7937 |
| Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 0+2) -> LRMC | Root-MUSIC | 7.4766 |
| Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 1+2) -> LRMC | DBF | 7.7709 |
| Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 1+2) -> LRMC | ESPRIT | 7.1775 |
| Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 1+2) -> LRMC | MUSIC | 7.8201 |
| Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 1+2) -> LRMC | Root-MUSIC | 7.6007 |
| Coherent | Gap = 1 deg | SNR = 1 dB | SS(3/3) -> LRMC | DBF | 7.6475 |
| Coherent | Gap = 1 deg | SNR = 1 dB | SS(3/3) -> LRMC | ESPRIT | 6.5777 |
| Coherent | Gap = 1 deg | SNR = 1 dB | SS(3/3) -> LRMC | MUSIC | 7.7250 |
| Coherent | Gap = 1 deg | SNR = 1 dB | SS(3/3) -> LRMC | Root-MUSIC | 7.0916 |
| Coherent | Gap = 1 deg | SNR = 10 dB | SS(2/3: rows 0+1) -> LRMC | DBF | 6.5971 |
| Coherent | Gap = 1 deg | SNR = 10 dB | SS(2/3: rows 0+1) -> LRMC | ESPRIT | 3.2262 |
| Coherent | Gap = 1 deg | SNR = 10 dB | SS(2/3: rows 0+1) -> LRMC | MUSIC | 6.1247 |
| Coherent | Gap = 1 deg | SNR = 10 dB | SS(2/3: rows 0+1) -> LRMC | Root-MUSIC | 3.4772 |
| Coherent | Gap = 1 deg | SNR = 10 dB | SS(2/3: rows 0+2) -> LRMC | DBF | 6.9050 |
| Coherent | Gap = 1 deg | SNR = 10 dB | SS(2/3: rows 0+2) -> LRMC | ESPRIT | 6.5955 |
| Coherent | Gap = 1 deg | SNR = 10 dB | SS(2/3: rows 0+2) -> LRMC | MUSIC | 6.7074 |
| Coherent | Gap = 1 deg | SNR = 10 dB | SS(2/3: rows 0+2) -> LRMC | Root-MUSIC | 6.1465 |
| Coherent | Gap = 1 deg | SNR = 10 dB | SS(2/3: rows 1+2) -> LRMC | DBF | 7.0321 |
| Coherent | Gap = 1 deg | SNR = 10 dB | SS(2/3: rows 1+2) -> LRMC | ESPRIT | 6.8077 |
| Coherent | Gap = 1 deg | SNR = 10 dB | SS(2/3: rows 1+2) -> LRMC | MUSIC | 7.0704 |
| Coherent | Gap = 1 deg | SNR = 10 dB | SS(2/3: rows 1+2) -> LRMC | Root-MUSIC | 6.3806 |
| Coherent | Gap = 1 deg | SNR = 10 dB | SS(3/3) -> LRMC | DBF | 6.6451 |
| Coherent | Gap = 1 deg | SNR = 10 dB | SS(3/3) -> LRMC | ESPRIT | 5.3780 |
| Coherent | Gap = 1 deg | SNR = 10 dB | SS(3/3) -> LRMC | MUSIC | 6.5013 |
| Coherent | Gap = 1 deg | SNR = 10 dB | SS(3/3) -> LRMC | Root-MUSIC | 5.3511 |
| Coherent | Gap = 2 deg | SNR = 1 dB | SS(2/3: rows 0+1) -> LRMC | DBF | 7.4218 |
| Coherent | Gap = 2 deg | SNR = 1 dB | SS(2/3: rows 0+1) -> LRMC | ESPRIT | 3.6137 |
| Coherent | Gap = 2 deg | SNR = 1 dB | SS(2/3: rows 0+1) -> LRMC | MUSIC | 4.1927 |
| Coherent | Gap = 2 deg | SNR = 1 dB | SS(2/3: rows 0+1) -> LRMC | Root-MUSIC | 3.7478 |
| Coherent | Gap = 2 deg | SNR = 1 dB | SS(2/3: rows 0+2) -> LRMC | DBF | 7.8928 |
| Coherent | Gap = 2 deg | SNR = 1 dB | SS(2/3: rows 0+2) -> LRMC | ESPRIT | 6.0507 |
| Coherent | Gap = 2 deg | SNR = 1 dB | SS(2/3: rows 0+2) -> LRMC | MUSIC | 6.9516 |
| Coherent | Gap = 2 deg | SNR = 1 dB | SS(2/3: rows 0+2) -> LRMC | Root-MUSIC | 6.6148 |
| Coherent | Gap = 2 deg | SNR = 1 dB | SS(2/3: rows 1+2) -> LRMC | DBF | 8.0351 |
| Coherent | Gap = 2 deg | SNR = 1 dB | SS(2/3: rows 1+2) -> LRMC | ESPRIT | 6.2226 |
| Coherent | Gap = 2 deg | SNR = 1 dB | SS(2/3: rows 1+2) -> LRMC | MUSIC | 6.9680 |
| Coherent | Gap = 2 deg | SNR = 1 dB | SS(2/3: rows 1+2) -> LRMC | Root-MUSIC | 6.7924 |
| Coherent | Gap = 2 deg | SNR = 1 dB | SS(3/3) -> LRMC | DBF | 7.6794 |
| Coherent | Gap = 2 deg | SNR = 1 dB | SS(3/3) -> LRMC | ESPRIT | 4.6153 |
| Coherent | Gap = 2 deg | SNR = 1 dB | SS(3/3) -> LRMC | MUSIC | 6.0834 |
| Coherent | Gap = 2 deg | SNR = 1 dB | SS(3/3) -> LRMC | Root-MUSIC | 5.2166 |
| Coherent | Gap = 3 deg | SNR = 10 dB | SS(2/3: rows 0+1) -> LRMC | DBF | 5.8316 |
| Coherent | Gap = 3 deg | SNR = 10 dB | SS(2/3: rows 0+1) -> LRMC | ESPRIT | 2.8092 |
| Coherent | Gap = 3 deg | SNR = 10 dB | SS(2/3: rows 0+1) -> LRMC | MUSIC | 3.2840 |
| Coherent | Gap = 3 deg | SNR = 10 dB | SS(2/3: rows 0+1) -> LRMC | Root-MUSIC | 3.0135 |
| Coherent | Gap = 3 deg | SNR = 10 dB | SS(2/3: rows 0+2) -> LRMC | DBF | 2.4290 |
| Coherent | Gap = 3 deg | SNR = 10 dB | SS(2/3: rows 0+2) -> LRMC | ESPRIT | 1.7232 |
| Coherent | Gap = 3 deg | SNR = 10 dB | SS(2/3: rows 0+2) -> LRMC | MUSIC | 2.2224 |
| Coherent | Gap = 3 deg | SNR = 10 dB | SS(2/3: rows 0+2) -> LRMC | Root-MUSIC | 2.1462 |
| Coherent | Gap = 3 deg | SNR = 10 dB | SS(2/3: rows 1+2) -> LRMC | DBF | 2.3330 |
| Coherent | Gap = 3 deg | SNR = 10 dB | SS(2/3: rows 1+2) -> LRMC | ESPRIT | 1.8360 |
| Coherent | Gap = 3 deg | SNR = 10 dB | SS(2/3: rows 1+2) -> LRMC | MUSIC | 2.1845 |
| Coherent | Gap = 3 deg | SNR = 10 dB | SS(2/3: rows 1+2) -> LRMC | Root-MUSIC | 2.2736 |
| Coherent | Gap = 3 deg | SNR = 10 dB | SS(3/3) -> LRMC | DBF | 2.3422 |
| Coherent | Gap = 3 deg | SNR = 10 dB | SS(3/3) -> LRMC | ESPRIT | 1.1835 |
| Coherent | Gap = 3 deg | SNR = 10 dB | SS(3/3) -> LRMC | MUSIC | 1.4575 |
| Coherent | Gap = 3 deg | SNR = 10 dB | SS(3/3) -> LRMC | Root-MUSIC | 1.4343 |
| Coherent | Gap = 5 deg | SNR = 10 dB | SS(2/3: rows 0+1) -> LRMC | DBF | 1.7007 |
| Coherent | Gap = 5 deg | SNR = 10 dB | SS(2/3: rows 0+1) -> LRMC | ESPRIT | 1.9612 |
| Coherent | Gap = 5 deg | SNR = 10 dB | SS(2/3: rows 0+1) -> LRMC | MUSIC | 1.8663 |
| Coherent | Gap = 5 deg | SNR = 10 dB | SS(2/3: rows 0+1) -> LRMC | Root-MUSIC | 1.9114 |
| Coherent | Gap = 5 deg | SNR = 10 dB | SS(2/3: rows 0+2) -> LRMC | DBF | 1.0647 |
| Coherent | Gap = 5 deg | SNR = 10 dB | SS(2/3: rows 0+2) -> LRMC | ESPRIT | 1.6258 |
| Coherent | Gap = 5 deg | SNR = 10 dB | SS(2/3: rows 0+2) -> LRMC | MUSIC | 1.4056 |
| Coherent | Gap = 5 deg | SNR = 10 dB | SS(2/3: rows 0+2) -> LRMC | Root-MUSIC | 1.4415 |
| Coherent | Gap = 5 deg | SNR = 10 dB | SS(2/3: rows 1+2) -> LRMC | DBF | 0.9068 |
| Coherent | Gap = 5 deg | SNR = 10 dB | SS(2/3: rows 1+2) -> LRMC | ESPRIT | 1.6087 |
| Coherent | Gap = 5 deg | SNR = 10 dB | SS(2/3: rows 1+2) -> LRMC | MUSIC | 1.2818 |
| Coherent | Gap = 5 deg | SNR = 10 dB | SS(2/3: rows 1+2) -> LRMC | Root-MUSIC | 1.3081 |
| Coherent | Gap = 5 deg | SNR = 10 dB | SS(3/3) -> LRMC | DBF | 0.9261 |
| Coherent | Gap = 5 deg | SNR = 10 dB | SS(3/3) -> LRMC | ESPRIT | 1.2343 |
| Coherent | Gap = 5 deg | SNR = 10 dB | SS(3/3) -> LRMC | MUSIC | 1.1133 |
| Coherent | Gap = 5 deg | SNR = 10 dB | SS(3/3) -> LRMC | Root-MUSIC | 1.0714 |
| Non-Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 0+1) -> LRMC | DBF | 7.8451 |
| Non-Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 0+1) -> LRMC | ESPRIT | 5.1077 |
| Non-Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 0+1) -> LRMC | MUSIC | 7.4984 |
| Non-Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 0+1) -> LRMC | Root-MUSIC | 6.4553 |
| Non-Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 0+2) -> LRMC | DBF | 7.9621 |
| Non-Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 0+2) -> LRMC | ESPRIT | 5.3113 |
| Non-Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 0+2) -> LRMC | MUSIC | 7.5466 |
| Non-Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 0+2) -> LRMC | Root-MUSIC | 6.5520 |
| Non-Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 1+2) -> LRMC | DBF | 7.8135 |
| Non-Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 1+2) -> LRMC | ESPRIT | 5.1604 |
| Non-Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 1+2) -> LRMC | MUSIC | 7.6478 |
| Non-Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 1+2) -> LRMC | Root-MUSIC | 6.5267 |
| Non-Coherent | Gap = 1 deg | SNR = 1 dB | SS(3/3) -> LRMC | DBF | 7.9893 |
| Non-Coherent | Gap = 1 deg | SNR = 1 dB | SS(3/3) -> LRMC | ESPRIT | 4.9503 |
| Non-Coherent | Gap = 1 deg | SNR = 1 dB | SS(3/3) -> LRMC | MUSIC | 7.5588 |
| Non-Coherent | Gap = 1 deg | SNR = 1 dB | SS(3/3) -> LRMC | Root-MUSIC | 6.4739 |
| Non-Coherent | Gap = 1 deg | SNR = 10 dB | SS(2/3: rows 0+1) -> LRMC | DBF | 5.3200 |
| Non-Coherent | Gap = 1 deg | SNR = 10 dB | SS(2/3: rows 0+1) -> LRMC | ESPRIT | 0.5752 |
| Non-Coherent | Gap = 1 deg | SNR = 10 dB | SS(2/3: rows 0+1) -> LRMC | MUSIC | 2.3852 |
| Non-Coherent | Gap = 1 deg | SNR = 10 dB | SS(2/3: rows 0+1) -> LRMC | Root-MUSIC | 1.0278 |
| Non-Coherent | Gap = 1 deg | SNR = 10 dB | SS(2/3: rows 0+2) -> LRMC | DBF | 5.2135 |
| Non-Coherent | Gap = 1 deg | SNR = 10 dB | SS(2/3: rows 0+2) -> LRMC | ESPRIT | 0.6785 |
| Non-Coherent | Gap = 1 deg | SNR = 10 dB | SS(2/3: rows 0+2) -> LRMC | MUSIC | 2.2854 |
| Non-Coherent | Gap = 1 deg | SNR = 10 dB | SS(2/3: rows 0+2) -> LRMC | Root-MUSIC | 1.0285 |
| Non-Coherent | Gap = 1 deg | SNR = 10 dB | SS(2/3: rows 1+2) -> LRMC | DBF | 5.2375 |
| Non-Coherent | Gap = 1 deg | SNR = 10 dB | SS(2/3: rows 1+2) -> LRMC | ESPRIT | 0.6305 |
| Non-Coherent | Gap = 1 deg | SNR = 10 dB | SS(2/3: rows 1+2) -> LRMC | MUSIC | 2.3694 |
| Non-Coherent | Gap = 1 deg | SNR = 10 dB | SS(2/3: rows 1+2) -> LRMC | Root-MUSIC | 1.0083 |
| Non-Coherent | Gap = 1 deg | SNR = 10 dB | SS(3/3) -> LRMC | DBF | 5.1962 |
| Non-Coherent | Gap = 1 deg | SNR = 10 dB | SS(3/3) -> LRMC | ESPRIT | 0.4314 |
| Non-Coherent | Gap = 1 deg | SNR = 10 dB | SS(3/3) -> LRMC | MUSIC | 1.6027 |
| Non-Coherent | Gap = 1 deg | SNR = 10 dB | SS(3/3) -> LRMC | Root-MUSIC | 0.6607 |
| Non-Coherent | Gap = 2 deg | SNR = 1 dB | SS(2/3: rows 0+1) -> LRMC | DBF | 7.6332 |
| Non-Coherent | Gap = 2 deg | SNR = 1 dB | SS(2/3: rows 0+1) -> LRMC | ESPRIT | 0.8660 |
| Non-Coherent | Gap = 2 deg | SNR = 1 dB | SS(2/3: rows 0+1) -> LRMC | MUSIC | 3.4761 |
| Non-Coherent | Gap = 2 deg | SNR = 1 dB | SS(2/3: rows 0+1) -> LRMC | Root-MUSIC | 1.1646 |
| Non-Coherent | Gap = 2 deg | SNR = 1 dB | SS(2/3: rows 0+2) -> LRMC | DBF | 7.5349 |
| Non-Coherent | Gap = 2 deg | SNR = 1 dB | SS(2/3: rows 0+2) -> LRMC | ESPRIT | 0.8546 |
| Non-Coherent | Gap = 2 deg | SNR = 1 dB | SS(2/3: rows 0+2) -> LRMC | MUSIC | 3.5011 |
| Non-Coherent | Gap = 2 deg | SNR = 1 dB | SS(2/3: rows 0+2) -> LRMC | Root-MUSIC | 1.1940 |
| Non-Coherent | Gap = 2 deg | SNR = 1 dB | SS(2/3: rows 1+2) -> LRMC | DBF | 7.6859 |
| Non-Coherent | Gap = 2 deg | SNR = 1 dB | SS(2/3: rows 1+2) -> LRMC | ESPRIT | 0.9057 |
| Non-Coherent | Gap = 2 deg | SNR = 1 dB | SS(2/3: rows 1+2) -> LRMC | MUSIC | 3.5385 |
| Non-Coherent | Gap = 2 deg | SNR = 1 dB | SS(2/3: rows 1+2) -> LRMC | Root-MUSIC | 1.2910 |
| Non-Coherent | Gap = 2 deg | SNR = 1 dB | SS(3/3) -> LRMC | DBF | 7.6942 |
| Non-Coherent | Gap = 2 deg | SNR = 1 dB | SS(3/3) -> LRMC | ESPRIT | 0.6826 |
| Non-Coherent | Gap = 2 deg | SNR = 1 dB | SS(3/3) -> LRMC | MUSIC | 3.4612 |
| Non-Coherent | Gap = 2 deg | SNR = 1 dB | SS(3/3) -> LRMC | Root-MUSIC | 0.8787 |
| Non-Coherent | Gap = 3 deg | SNR = 10 dB | SS(2/3: rows 0+1) -> LRMC | DBF | 4.1993 |
| Non-Coherent | Gap = 3 deg | SNR = 10 dB | SS(2/3: rows 0+1) -> LRMC | ESPRIT | 0.1023 |
| Non-Coherent | Gap = 3 deg | SNR = 10 dB | SS(2/3: rows 0+1) -> LRMC | MUSIC | 0.1285 |
| Non-Coherent | Gap = 3 deg | SNR = 10 dB | SS(2/3: rows 0+1) -> LRMC | Root-MUSIC | 0.1104 |
| Non-Coherent | Gap = 3 deg | SNR = 10 dB | SS(2/3: rows 0+2) -> LRMC | DBF | 4.1887 |
| Non-Coherent | Gap = 3 deg | SNR = 10 dB | SS(2/3: rows 0+2) -> LRMC | ESPRIT | 0.1030 |
| Non-Coherent | Gap = 3 deg | SNR = 10 dB | SS(2/3: rows 0+2) -> LRMC | MUSIC | 0.1283 |
| Non-Coherent | Gap = 3 deg | SNR = 10 dB | SS(2/3: rows 0+2) -> LRMC | Root-MUSIC | 0.1185 |
| Non-Coherent | Gap = 3 deg | SNR = 10 dB | SS(2/3: rows 1+2) -> LRMC | DBF | 4.1372 |
| Non-Coherent | Gap = 3 deg | SNR = 10 dB | SS(2/3: rows 1+2) -> LRMC | ESPRIT | 0.1016 |
| Non-Coherent | Gap = 3 deg | SNR = 10 dB | SS(2/3: rows 1+2) -> LRMC | MUSIC | 0.1212 |
| Non-Coherent | Gap = 3 deg | SNR = 10 dB | SS(2/3: rows 1+2) -> LRMC | Root-MUSIC | 0.1155 |
| Non-Coherent | Gap = 3 deg | SNR = 10 dB | SS(3/3) -> LRMC | DBF | 4.2098 |
| Non-Coherent | Gap = 3 deg | SNR = 10 dB | SS(3/3) -> LRMC | ESPRIT | 0.0983 |
| Non-Coherent | Gap = 3 deg | SNR = 10 dB | SS(3/3) -> LRMC | MUSIC | 0.1116 |
| Non-Coherent | Gap = 3 deg | SNR = 10 dB | SS(3/3) -> LRMC | Root-MUSIC | 0.1041 |
| Non-Coherent | Gap = 5 deg | SNR = 10 dB | SS(2/3: rows 0+1) -> LRMC | DBF | 0.1050 |
| Non-Coherent | Gap = 5 deg | SNR = 10 dB | SS(2/3: rows 0+1) -> LRMC | ESPRIT | 0.1147 |
| Non-Coherent | Gap = 5 deg | SNR = 10 dB | SS(2/3: rows 0+1) -> LRMC | MUSIC | 0.1171 |
| Non-Coherent | Gap = 5 deg | SNR = 10 dB | SS(2/3: rows 0+1) -> LRMC | Root-MUSIC | 0.1098 |
| Non-Coherent | Gap = 5 deg | SNR = 10 dB | SS(2/3: rows 0+2) -> LRMC | DBF | 0.1026 |
| Non-Coherent | Gap = 5 deg | SNR = 10 dB | SS(2/3: rows 0+2) -> LRMC | ESPRIT | 0.1147 |
| Non-Coherent | Gap = 5 deg | SNR = 10 dB | SS(2/3: rows 0+2) -> LRMC | MUSIC | 0.1160 |
| Non-Coherent | Gap = 5 deg | SNR = 10 dB | SS(2/3: rows 0+2) -> LRMC | Root-MUSIC | 0.1099 |
| Non-Coherent | Gap = 5 deg | SNR = 10 dB | SS(2/3: rows 1+2) -> LRMC | DBF | 0.1094 |
| Non-Coherent | Gap = 5 deg | SNR = 10 dB | SS(2/3: rows 1+2) -> LRMC | ESPRIT | 0.1144 |
| Non-Coherent | Gap = 5 deg | SNR = 10 dB | SS(2/3: rows 1+2) -> LRMC | MUSIC | 0.1150 |
| Non-Coherent | Gap = 5 deg | SNR = 10 dB | SS(2/3: rows 1+2) -> LRMC | Root-MUSIC | 0.1102 |
| Non-Coherent | Gap = 5 deg | SNR = 10 dB | SS(3/3) -> LRMC | DBF | 0.1067 |
| Non-Coherent | Gap = 5 deg | SNR = 10 dB | SS(3/3) -> LRMC | ESPRIT | 0.1065 |
| Non-Coherent | Gap = 5 deg | SNR = 10 dB | SS(3/3) -> LRMC | MUSIC | 0.1085 |
| Non-Coherent | Gap = 5 deg | SNR = 10 dB | SS(3/3) -> LRMC | Root-MUSIC | 0.1035 |
