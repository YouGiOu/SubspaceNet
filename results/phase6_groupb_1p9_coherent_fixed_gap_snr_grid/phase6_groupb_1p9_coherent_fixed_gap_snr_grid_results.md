# Phase 6 - Group B 1.9 Lambda Coherent Fixed-Gap and SNR Grid

Phase 6 compares the coherent Group B SS -> LRMC classical controls against SS -> LRMC -> SubspaceNet -> ESPRIT over a 20-cell fixed-gap and SNR grid.

Experimental conditions:
- Array: Group B 12-channel 2D hardware geometry
- Physical spacing: 1.9 lambda
- Signals: 2 coherent narrowband targets
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
| Gap = 1 deg | SNR = 1 dB | SS -> LRMC | DBF | 7.8381 |
| Gap = 1 deg | SNR = 1 dB | SS -> LRMC | ESPRIT | 6.6485 |
| Gap = 1 deg | SNR = 1 dB | SS -> LRMC | MUSIC | 7.8162 |
| Gap = 1 deg | SNR = 1 dB | SS -> LRMC | Root-MUSIC | 7.2565 |
| Gap = 1 deg | SNR = 1 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.4147 |
| Gap = 1 deg | SNR = 10 dB | SS -> LRMC | DBF | 6.8058 |
| Gap = 1 deg | SNR = 10 dB | SS -> LRMC | ESPRIT | 5.4640 |
| Gap = 1 deg | SNR = 10 dB | SS -> LRMC | MUSIC | 6.5446 |
| Gap = 1 deg | SNR = 10 dB | SS -> LRMC | Root-MUSIC | 5.4822 |
| Gap = 1 deg | SNR = 10 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.3829 |
| Gap = 1 deg | SNR = 15 dB | SS -> LRMC | DBF | 6.7462 |
| Gap = 1 deg | SNR = 15 dB | SS -> LRMC | ESPRIT | 5.7761 |
| Gap = 1 deg | SNR = 15 dB | SS -> LRMC | MUSIC | 6.3620 |
| Gap = 1 deg | SNR = 15 dB | SS -> LRMC | Root-MUSIC | 5.4335 |
| Gap = 1 deg | SNR = 15 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.3586 |
| Gap = 1 deg | SNR = 5 dB | SS -> LRMC | DBF | 7.1281 |
| Gap = 1 deg | SNR = 5 dB | SS -> LRMC | ESPRIT | 5.4369 |
| Gap = 1 deg | SNR = 5 dB | SS -> LRMC | MUSIC | 7.0511 |
| Gap = 1 deg | SNR = 5 dB | SS -> LRMC | Root-MUSIC | 5.7864 |
| Gap = 1 deg | SNR = 5 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.3731 |
| Gap = 2 deg | SNR = 1 dB | SS -> LRMC | DBF | 7.8199 |
| Gap = 2 deg | SNR = 1 dB | SS -> LRMC | ESPRIT | 4.5874 |
| Gap = 2 deg | SNR = 1 dB | SS -> LRMC | MUSIC | 6.1762 |
| Gap = 2 deg | SNR = 1 dB | SS -> LRMC | Root-MUSIC | 5.2469 |
| Gap = 2 deg | SNR = 1 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.9976 |
| Gap = 2 deg | SNR = 10 dB | SS -> LRMC | DBF | 7.1865 |
| Gap = 2 deg | SNR = 10 dB | SS -> LRMC | ESPRIT | 3.7125 |
| Gap = 2 deg | SNR = 10 dB | SS -> LRMC | MUSIC | 4.3796 |
| Gap = 2 deg | SNR = 10 dB | SS -> LRMC | Root-MUSIC | 4.0701 |
| Gap = 2 deg | SNR = 10 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.6575 |
| Gap = 2 deg | SNR = 15 dB | SS -> LRMC | DBF | 7.1475 |
| Gap = 2 deg | SNR = 15 dB | SS -> LRMC | ESPRIT | 3.8603 |
| Gap = 2 deg | SNR = 15 dB | SS -> LRMC | MUSIC | 4.2658 |
| Gap = 2 deg | SNR = 15 dB | SS -> LRMC | Root-MUSIC | 4.0387 |
| Gap = 2 deg | SNR = 15 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.6687 |
| Gap = 2 deg | SNR = 5 dB | SS -> LRMC | DBF | 7.4749 |
| Gap = 2 deg | SNR = 5 dB | SS -> LRMC | ESPRIT | 3.6867 |
| Gap = 2 deg | SNR = 5 dB | SS -> LRMC | MUSIC | 4.6708 |
| Gap = 2 deg | SNR = 5 dB | SS -> LRMC | Root-MUSIC | 4.3131 |
| Gap = 2 deg | SNR = 5 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.7717 |
| Gap = 3 deg | SNR = 1 dB | SS -> LRMC | DBF | 2.5997 |
| Gap = 3 deg | SNR = 1 dB | SS -> LRMC | ESPRIT | 1.4188 |
| Gap = 3 deg | SNR = 1 dB | SS -> LRMC | MUSIC | 1.7411 |
| Gap = 3 deg | SNR = 1 dB | SS -> LRMC | Root-MUSIC | 1.6864 |
| Gap = 3 deg | SNR = 1 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.5363 |
| Gap = 3 deg | SNR = 10 dB | SS -> LRMC | DBF | 2.1675 |
| Gap = 3 deg | SNR = 10 dB | SS -> LRMC | ESPRIT | 1.1452 |
| Gap = 3 deg | SNR = 10 dB | SS -> LRMC | MUSIC | 1.4096 |
| Gap = 3 deg | SNR = 10 dB | SS -> LRMC | Root-MUSIC | 1.3902 |
| Gap = 3 deg | SNR = 10 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.2804 |
| Gap = 3 deg | SNR = 15 dB | SS -> LRMC | DBF | 2.0383 |
| Gap = 3 deg | SNR = 15 dB | SS -> LRMC | ESPRIT | 1.1095 |
| Gap = 3 deg | SNR = 15 dB | SS -> LRMC | MUSIC | 1.4010 |
| Gap = 3 deg | SNR = 15 dB | SS -> LRMC | Root-MUSIC | 1.3680 |
| Gap = 3 deg | SNR = 15 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.2681 |
| Gap = 3 deg | SNR = 5 dB | SS -> LRMC | DBF | 2.3414 |
| Gap = 3 deg | SNR = 5 dB | SS -> LRMC | ESPRIT | 1.1842 |
| Gap = 3 deg | SNR = 5 dB | SS -> LRMC | MUSIC | 1.4934 |
| Gap = 3 deg | SNR = 5 dB | SS -> LRMC | Root-MUSIC | 1.4654 |
| Gap = 3 deg | SNR = 5 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.3335 |
| Gap = 4 deg | SNR = 1 dB | SS -> LRMC | DBF | 0.2043 |
| Gap = 4 deg | SNR = 1 dB | SS -> LRMC | ESPRIT | 0.1683 |
| Gap = 4 deg | SNR = 1 dB | SS -> LRMC | MUSIC | 0.1663 |
| Gap = 4 deg | SNR = 1 dB | SS -> LRMC | Root-MUSIC | 0.1640 |
| Gap = 4 deg | SNR = 1 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.2463 |
| Gap = 4 deg | SNR = 10 dB | SS -> LRMC | DBF | 0.1842 |
| Gap = 4 deg | SNR = 10 dB | SS -> LRMC | ESPRIT | 0.1000 |
| Gap = 4 deg | SNR = 10 dB | SS -> LRMC | MUSIC | 0.1305 |
| Gap = 4 deg | SNR = 10 dB | SS -> LRMC | Root-MUSIC | 0.1223 |
| Gap = 4 deg | SNR = 10 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.1224 |
| Gap = 4 deg | SNR = 15 dB | SS -> LRMC | DBF | 0.1877 |
| Gap = 4 deg | SNR = 15 dB | SS -> LRMC | ESPRIT | 0.1001 |
| Gap = 4 deg | SNR = 15 dB | SS -> LRMC | MUSIC | 0.1299 |
| Gap = 4 deg | SNR = 15 dB | SS -> LRMC | Root-MUSIC | 0.1219 |
| Gap = 4 deg | SNR = 15 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.1186 |
| Gap = 4 deg | SNR = 5 dB | SS -> LRMC | DBF | 0.1851 |
| Gap = 4 deg | SNR = 5 dB | SS -> LRMC | ESPRIT | 0.1050 |
| Gap = 4 deg | SNR = 5 dB | SS -> LRMC | MUSIC | 0.1384 |
| Gap = 4 deg | SNR = 5 dB | SS -> LRMC | Root-MUSIC | 0.1250 |
| Gap = 4 deg | SNR = 5 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.1478 |
| Gap = 5 deg | SNR = 1 dB | SS -> LRMC | DBF | 1.1128 |
| Gap = 5 deg | SNR = 1 dB | SS -> LRMC | ESPRIT | 1.4333 |
| Gap = 5 deg | SNR = 1 dB | SS -> LRMC | MUSIC | 1.2754 |
| Gap = 5 deg | SNR = 1 dB | SS -> LRMC | Root-MUSIC | 1.2525 |
| Gap = 5 deg | SNR = 1 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.3298 |
| Gap = 5 deg | SNR = 10 dB | SS -> LRMC | DBF | 0.9190 |
| Gap = 5 deg | SNR = 10 dB | SS -> LRMC | ESPRIT | 1.2365 |
| Gap = 5 deg | SNR = 10 dB | SS -> LRMC | MUSIC | 1.1224 |
| Gap = 5 deg | SNR = 10 dB | SS -> LRMC | Root-MUSIC | 1.0890 |
| Gap = 5 deg | SNR = 10 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.2129 |
| Gap = 5 deg | SNR = 15 dB | SS -> LRMC | DBF | 0.7110 |
| Gap = 5 deg | SNR = 15 dB | SS -> LRMC | ESPRIT | 1.1527 |
| Gap = 5 deg | SNR = 15 dB | SS -> LRMC | MUSIC | 0.9082 |
| Gap = 5 deg | SNR = 15 dB | SS -> LRMC | Root-MUSIC | 0.8815 |
| Gap = 5 deg | SNR = 15 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.2027 |
| Gap = 5 deg | SNR = 5 dB | SS -> LRMC | DBF | 1.0664 |
| Gap = 5 deg | SNR = 5 dB | SS -> LRMC | ESPRIT | 1.2949 |
| Gap = 5 deg | SNR = 5 dB | SS -> LRMC | MUSIC | 1.2525 |
| Gap = 5 deg | SNR = 5 dB | SS -> LRMC | Root-MUSIC | 1.2084 |
| Gap = 5 deg | SNR = 5 dB | SS -> LRMC -> SubspaceNet | ESPRIT | 0.2436 |
