# Phase 6 - Group B 1.9 Lambda Non-Coherent Fixed-Gap and SNR Grid

Phase 6 compares the non-coherent Group B SS -> LRMC classical controls against SS -> LRMC -> SubspaceNet -> ESPRIT over a 20-cell fixed-gap and SNR grid.

Experimental conditions:
- Array: Group B 12-channel 2D hardware geometry
- Physical spacing: 1.9 lambda
- Signals: 2 non-coherent narrowband targets
- Snapshots: T = 40
- Azimuth and elevation range: [-15 deg, 15 deg]
- Fixed azimuth separations: 1, 2, 3, 4, 5 deg
- SNR sweep: 1, 5, 10, 15 dB
- Preprocessing: spatial smoothing before LRMC
- Learned target: SubspaceNet-ESPRIT
- Control methods: DBF, MUSIC, Root-MUSIC, ESPRIT
- Dataset size per cell: 45,000 samples
- Metric: horizontal-angle RMSE in degrees (periodic matching)

| Algorithm | RMSE (deg) |
| --- | ---: |
| Gap = 1 deg | SNR = 1 dB | SS -> LRMC | DBF | 7.9169 |
| Gap = 1 deg | SNR = 1 dB | SS -> LRMC | ESPRIT | 5.0823 |
| Gap = 1 deg | SNR = 1 dB | SS -> LRMC | MUSIC | 7.6110 |
| Gap = 1 deg | SNR = 1 dB | SS -> LRMC | Root-MUSIC | 6.6123 |
| Gap = 1 deg | SNR = 1 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.4002 |
| Gap = 1 deg | SNR = 10 dB | SS -> LRMC | DBF | 5.2787 |
| Gap = 1 deg | SNR = 10 dB | SS -> LRMC | ESPRIT | 0.4165 |
| Gap = 1 deg | SNR = 10 dB | SS -> LRMC | MUSIC | 1.5837 |
| Gap = 1 deg | SNR = 10 dB | SS -> LRMC | Root-MUSIC | 0.6742 |
| Gap = 1 deg | SNR = 10 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.3744 |
| Gap = 1 deg | SNR = 15 dB | SS -> LRMC | DBF | 5.2813 |
| Gap = 1 deg | SNR = 15 dB | SS -> LRMC | ESPRIT | 0.4230 |
| Gap = 1 deg | SNR = 15 dB | SS -> LRMC | MUSIC | 1.2252 |
| Gap = 1 deg | SNR = 15 dB | SS -> LRMC | Root-MUSIC | 0.5884 |
| Gap = 1 deg | SNR = 15 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.3794 |
| Gap = 1 deg | SNR = 5 dB | SS -> LRMC | DBF | 6.0596 |
| Gap = 1 deg | SNR = 5 dB | SS -> LRMC | ESPRIT | 0.9243 |
| Gap = 1 deg | SNR = 5 dB | SS -> LRMC | MUSIC | 4.6481 |
| Gap = 1 deg | SNR = 5 dB | SS -> LRMC | Root-MUSIC | 1.5695 |
| Gap = 1 deg | SNR = 5 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.3787 |
| Gap = 2 deg | SNR = 1 dB | SS -> LRMC | DBF | 7.6043 |
| Gap = 2 deg | SNR = 1 dB | SS -> LRMC | ESPRIT | 0.6209 |
| Gap = 2 deg | SNR = 1 dB | SS -> LRMC | MUSIC | 3.2511 |
| Gap = 2 deg | SNR = 1 dB | SS -> LRMC | Root-MUSIC | 0.7714 |
| Gap = 2 deg | SNR = 1 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.5671 |
| Gap = 2 deg | SNR = 10 dB | SS -> LRMC | DBF | 5.8592 |
| Gap = 2 deg | SNR = 10 dB | SS -> LRMC | ESPRIT | 0.1112 |
| Gap = 2 deg | SNR = 10 dB | SS -> LRMC | MUSIC | 0.2416 |
| Gap = 2 deg | SNR = 10 dB | SS -> LRMC | Root-MUSIC | 0.1347 |
| Gap = 2 deg | SNR = 10 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.5254 |
| Gap = 2 deg | SNR = 15 dB | SS -> LRMC | DBF | 5.8211 |
| Gap = 2 deg | SNR = 15 dB | SS -> LRMC | ESPRIT | 0.1104 |
| Gap = 2 deg | SNR = 15 dB | SS -> LRMC | MUSIC | 0.2341 |
| Gap = 2 deg | SNR = 15 dB | SS -> LRMC | Root-MUSIC | 0.1339 |
| Gap = 2 deg | SNR = 15 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.5105 |
| Gap = 2 deg | SNR = 5 dB | SS -> LRMC | DBF | 6.5452 |
| Gap = 2 deg | SNR = 5 dB | SS -> LRMC | ESPRIT | 0.1297 |
| Gap = 2 deg | SNR = 5 dB | SS -> LRMC | MUSIC | 0.2664 |
| Gap = 2 deg | SNR = 5 dB | SS -> LRMC | Root-MUSIC | 0.1523 |
| Gap = 2 deg | SNR = 5 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.5452 |
| Gap = 3 deg | SNR = 1 dB | SS -> LRMC | DBF | 3.9119 |
| Gap = 3 deg | SNR = 1 dB | SS -> LRMC | ESPRIT | 0.2266 |
| Gap = 3 deg | SNR = 1 dB | SS -> LRMC | MUSIC | 0.2343 |
| Gap = 3 deg | SNR = 1 dB | SS -> LRMC | Root-MUSIC | 0.1627 |
| Gap = 3 deg | SNR = 1 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.4776 |
| Gap = 3 deg | SNR = 10 dB | SS -> LRMC | DBF | 4.2907 |
| Gap = 3 deg | SNR = 10 dB | SS -> LRMC | ESPRIT | 0.0988 |
| Gap = 3 deg | SNR = 10 dB | SS -> LRMC | MUSIC | 0.1147 |
| Gap = 3 deg | SNR = 10 dB | SS -> LRMC | Root-MUSIC | 0.1049 |
| Gap = 3 deg | SNR = 10 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.2102 |
| Gap = 3 deg | SNR = 15 dB | SS -> LRMC | DBF | 4.2825 |
| Gap = 3 deg | SNR = 15 dB | SS -> LRMC | ESPRIT | 0.0985 |
| Gap = 3 deg | SNR = 15 dB | SS -> LRMC | MUSIC | 0.1162 |
| Gap = 3 deg | SNR = 15 dB | SS -> LRMC | Root-MUSIC | 0.1054 |
| Gap = 3 deg | SNR = 15 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.2026 |
| Gap = 3 deg | SNR = 5 dB | SS -> LRMC | DBF | 4.3501 |
| Gap = 3 deg | SNR = 5 dB | SS -> LRMC | ESPRIT | 0.1060 |
| Gap = 3 deg | SNR = 5 dB | SS -> LRMC | MUSIC | 0.1192 |
| Gap = 3 deg | SNR = 5 dB | SS -> LRMC | Root-MUSIC | 0.1077 |
| Gap = 3 deg | SNR = 5 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.2607 |
| Gap = 4 deg | SNR = 1 dB | SS -> LRMC | DBF | 0.1883 |
| Gap = 4 deg | SNR = 1 dB | SS -> LRMC | ESPRIT | 0.1666 |
| Gap = 4 deg | SNR = 1 dB | SS -> LRMC | MUSIC | 0.1506 |
| Gap = 4 deg | SNR = 1 dB | SS -> LRMC | Root-MUSIC | 0.1373 |
| Gap = 4 deg | SNR = 1 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.3997 |
| Gap = 4 deg | SNR = 10 dB | SS -> LRMC | DBF | 0.1444 |
| Gap = 4 deg | SNR = 10 dB | SS -> LRMC | ESPRIT | 0.0931 |
| Gap = 4 deg | SNR = 10 dB | SS -> LRMC | MUSIC | 0.0966 |
| Gap = 4 deg | SNR = 10 dB | SS -> LRMC | Root-MUSIC | 0.0963 |
| Gap = 4 deg | SNR = 10 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.1589 |
| Gap = 4 deg | SNR = 15 dB | SS -> LRMC | DBF | 0.1475 |
| Gap = 4 deg | SNR = 15 dB | SS -> LRMC | ESPRIT | 0.0925 |
| Gap = 4 deg | SNR = 15 dB | SS -> LRMC | MUSIC | 0.0962 |
| Gap = 4 deg | SNR = 15 dB | SS -> LRMC | Root-MUSIC | 0.0959 |
| Gap = 4 deg | SNR = 15 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.1530 |
| Gap = 4 deg | SNR = 5 dB | SS -> LRMC | DBF | 0.1471 |
| Gap = 4 deg | SNR = 5 dB | SS -> LRMC | ESPRIT | 0.0978 |
| Gap = 4 deg | SNR = 5 dB | SS -> LRMC | MUSIC | 0.1025 |
| Gap = 4 deg | SNR = 5 dB | SS -> LRMC | Root-MUSIC | 0.0997 |
| Gap = 4 deg | SNR = 5 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.2000 |
| Gap = 5 deg | SNR = 1 dB | SS -> LRMC | DBF | 0.1545 |
| Gap = 5 deg | SNR = 1 dB | SS -> LRMC | ESPRIT | 0.1738 |
| Gap = 5 deg | SNR = 1 dB | SS -> LRMC | MUSIC | 0.1603 |
| Gap = 5 deg | SNR = 1 dB | SS -> LRMC | Root-MUSIC | 0.1456 |
| Gap = 5 deg | SNR = 1 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.3058 |
| Gap = 5 deg | SNR = 10 dB | SS -> LRMC | DBF | 0.1033 |
| Gap = 5 deg | SNR = 10 dB | SS -> LRMC | ESPRIT | 0.1057 |
| Gap = 5 deg | SNR = 10 dB | SS -> LRMC | MUSIC | 0.1085 |
| Gap = 5 deg | SNR = 10 dB | SS -> LRMC | Root-MUSIC | 0.1035 |
| Gap = 5 deg | SNR = 10 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.1495 |
| Gap = 5 deg | SNR = 15 dB | SS -> LRMC | DBF | 0.1029 |
| Gap = 5 deg | SNR = 15 dB | SS -> LRMC | ESPRIT | 0.1051 |
| Gap = 5 deg | SNR = 15 dB | SS -> LRMC | MUSIC | 0.1098 |
| Gap = 5 deg | SNR = 15 dB | SS -> LRMC | Root-MUSIC | 0.1030 |
| Gap = 5 deg | SNR = 15 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.1449 |
| Gap = 5 deg | SNR = 5 dB | SS -> LRMC | DBF | 0.1060 |
| Gap = 5 deg | SNR = 5 dB | SS -> LRMC | ESPRIT | 0.1109 |
| Gap = 5 deg | SNR = 5 dB | SS -> LRMC | MUSIC | 0.1115 |
| Gap = 5 deg | SNR = 5 dB | SS -> LRMC | Root-MUSIC | 0.1076 |
| Gap = 5 deg | SNR = 5 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.2047 |
