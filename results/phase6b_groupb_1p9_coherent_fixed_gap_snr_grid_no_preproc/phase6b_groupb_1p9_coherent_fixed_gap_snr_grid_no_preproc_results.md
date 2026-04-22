# Phase 6B - Group B 1.9 Lambda Coherent Fixed-Gap and SNR Grid Without SS -> LRMC

Phase 6B evaluates the coherent Group B raw classical controls without SS -> LRMC preprocessing on the same fixed-gap and SNR grid used in Phase 6.

Experimental conditions:
- Array: Group B 12-channel 2D hardware geometry
- Physical spacing: 1.9 lambda
- Signals: 2 coherent narrowband targets
- Snapshots: T = 40
- Azimuth and elevation range: [-15 deg, 15 deg]
- Fixed azimuth separations: 1, 2, 3, 4, 5 deg
- SNR sweep: 1, 5, 10, 15 dB
- Preprocessing: none
- Control methods: DBF, MUSIC, Root-MUSIC, ESPRIT
- Dataset size per cell: 45,000 samples
- Metric: horizontal-angle RMSE in degrees (periodic matching)

| Algorithm | RMSE (deg) |
| --- | ---: |
| Gap = 1 deg | SNR = 1 dB | No preprocessing | DBF | 7.8190 |
| Gap = 1 deg | SNR = 1 dB | No preprocessing | ESPRIT | 10.5181 |
| Gap = 1 deg | SNR = 1 dB | No preprocessing | MUSIC | 7.3149 |
| Gap = 1 deg | SNR = 1 dB | No preprocessing | Root-MUSIC | 10.4446 |
| Gap = 1 deg | SNR = 10 dB | No preprocessing | DBF | 7.7859 |
| Gap = 1 deg | SNR = 10 dB | No preprocessing | ESPRIT | 10.5193 |
| Gap = 1 deg | SNR = 10 dB | No preprocessing | MUSIC | 7.3390 |
| Gap = 1 deg | SNR = 10 dB | No preprocessing | Root-MUSIC | 10.4457 |
| Gap = 1 deg | SNR = 15 dB | No preprocessing | DBF | 7.7878 |
| Gap = 1 deg | SNR = 15 dB | No preprocessing | ESPRIT | 10.5174 |
| Gap = 1 deg | SNR = 15 dB | No preprocessing | MUSIC | 7.3355 |
| Gap = 1 deg | SNR = 15 dB | No preprocessing | Root-MUSIC | 10.4433 |
| Gap = 1 deg | SNR = 5 dB | No preprocessing | DBF | 7.8054 |
| Gap = 1 deg | SNR = 5 dB | No preprocessing | ESPRIT | 10.5267 |
| Gap = 1 deg | SNR = 5 dB | No preprocessing | MUSIC | 7.3300 |
| Gap = 1 deg | SNR = 5 dB | No preprocessing | Root-MUSIC | 10.4421 |
| Gap = 2 deg | SNR = 1 dB | No preprocessing | DBF | 8.0620 |
| Gap = 2 deg | SNR = 1 dB | No preprocessing | ESPRIT | 10.6934 |
| Gap = 2 deg | SNR = 1 dB | No preprocessing | MUSIC | 9.7575 |
| Gap = 2 deg | SNR = 1 dB | No preprocessing | Root-MUSIC | 10.5772 |
| Gap = 2 deg | SNR = 10 dB | No preprocessing | DBF | 8.0297 |
| Gap = 2 deg | SNR = 10 dB | No preprocessing | ESPRIT | 10.6745 |
| Gap = 2 deg | SNR = 10 dB | No preprocessing | MUSIC | 9.7246 |
| Gap = 2 deg | SNR = 10 dB | No preprocessing | Root-MUSIC | 10.6188 |
| Gap = 2 deg | SNR = 15 dB | No preprocessing | DBF | 8.1472 |
| Gap = 2 deg | SNR = 15 dB | No preprocessing | ESPRIT | 10.6762 |
| Gap = 2 deg | SNR = 15 dB | No preprocessing | MUSIC | 9.7319 |
| Gap = 2 deg | SNR = 15 dB | No preprocessing | Root-MUSIC | 10.6152 |
| Gap = 2 deg | SNR = 5 dB | No preprocessing | DBF | 7.8864 |
| Gap = 2 deg | SNR = 5 dB | No preprocessing | ESPRIT | 10.6918 |
| Gap = 2 deg | SNR = 5 dB | No preprocessing | MUSIC | 9.7342 |
| Gap = 2 deg | SNR = 5 dB | No preprocessing | Root-MUSIC | 10.6125 |
| Gap = 3 deg | SNR = 1 dB | No preprocessing | DBF | 2.7386 |
| Gap = 3 deg | SNR = 1 dB | No preprocessing | ESPRIT | 9.1882 |
| Gap = 3 deg | SNR = 1 dB | No preprocessing | MUSIC | 7.7178 |
| Gap = 3 deg | SNR = 1 dB | No preprocessing | Root-MUSIC | 9.2365 |
| Gap = 3 deg | SNR = 10 dB | No preprocessing | DBF | 1.0059 |
| Gap = 3 deg | SNR = 10 dB | No preprocessing | ESPRIT | 9.1786 |
| Gap = 3 deg | SNR = 10 dB | No preprocessing | MUSIC | 7.6462 |
| Gap = 3 deg | SNR = 10 dB | No preprocessing | Root-MUSIC | 9.2461 |
| Gap = 3 deg | SNR = 15 dB | No preprocessing | DBF | 0.9825 |
| Gap = 3 deg | SNR = 15 dB | No preprocessing | ESPRIT | 9.1799 |
| Gap = 3 deg | SNR = 15 dB | No preprocessing | MUSIC | 7.6502 |
| Gap = 3 deg | SNR = 15 dB | No preprocessing | Root-MUSIC | 9.2459 |
| Gap = 3 deg | SNR = 5 dB | No preprocessing | DBF | 1.3121 |
| Gap = 3 deg | SNR = 5 dB | No preprocessing | ESPRIT | 9.1892 |
| Gap = 3 deg | SNR = 5 dB | No preprocessing | MUSIC | 7.6649 |
| Gap = 3 deg | SNR = 5 dB | No preprocessing | Root-MUSIC | 9.2411 |
| Gap = 4 deg | SNR = 1 dB | No preprocessing | DBF | 0.0992 |
| Gap = 4 deg | SNR = 1 dB | No preprocessing | ESPRIT | 7.9130 |
| Gap = 4 deg | SNR = 1 dB | No preprocessing | MUSIC | 6.0645 |
| Gap = 4 deg | SNR = 1 dB | No preprocessing | Root-MUSIC | 8.3065 |
| Gap = 4 deg | SNR = 10 dB | No preprocessing | DBF | 0.0886 |
| Gap = 4 deg | SNR = 10 dB | No preprocessing | ESPRIT | 7.9321 |
| Gap = 4 deg | SNR = 10 dB | No preprocessing | MUSIC | 6.0366 |
| Gap = 4 deg | SNR = 10 dB | No preprocessing | Root-MUSIC | 8.2912 |
| Gap = 4 deg | SNR = 15 dB | No preprocessing | DBF | 0.0884 |
| Gap = 4 deg | SNR = 15 dB | No preprocessing | ESPRIT | 7.9323 |
| Gap = 4 deg | SNR = 15 dB | No preprocessing | MUSIC | 6.0318 |
| Gap = 4 deg | SNR = 15 dB | No preprocessing | Root-MUSIC | 8.2938 |
| Gap = 4 deg | SNR = 5 dB | No preprocessing | DBF | 0.0905 |
| Gap = 4 deg | SNR = 5 dB | No preprocessing | ESPRIT | 7.9287 |
| Gap = 4 deg | SNR = 5 dB | No preprocessing | MUSIC | 6.0243 |
| Gap = 4 deg | SNR = 5 dB | No preprocessing | Root-MUSIC | 8.2873 |
| Gap = 5 deg | SNR = 1 dB | No preprocessing | DBF | 0.5073 |
| Gap = 5 deg | SNR = 1 dB | No preprocessing | ESPRIT | 8.2643 |
| Gap = 5 deg | SNR = 1 dB | No preprocessing | MUSIC | 6.9495 |
| Gap = 5 deg | SNR = 1 dB | No preprocessing | Root-MUSIC | 8.2488 |
| Gap = 5 deg | SNR = 10 dB | No preprocessing | DBF | 0.4988 |
| Gap = 5 deg | SNR = 10 dB | No preprocessing | ESPRIT | 8.2453 |
| Gap = 5 deg | SNR = 10 dB | No preprocessing | MUSIC | 6.9653 |
| Gap = 5 deg | SNR = 10 dB | No preprocessing | Root-MUSIC | 8.2470 |
| Gap = 5 deg | SNR = 15 dB | No preprocessing | DBF | 0.4988 |
| Gap = 5 deg | SNR = 15 dB | No preprocessing | ESPRIT | 8.2408 |
| Gap = 5 deg | SNR = 15 dB | No preprocessing | MUSIC | 6.9640 |
| Gap = 5 deg | SNR = 15 dB | No preprocessing | Root-MUSIC | 8.2474 |
| Gap = 5 deg | SNR = 5 dB | No preprocessing | DBF | 0.4991 |
| Gap = 5 deg | SNR = 5 dB | No preprocessing | ESPRIT | 8.2569 |
| Gap = 5 deg | SNR = 5 dB | No preprocessing | MUSIC | 6.9526 |
| Gap = 5 deg | SNR = 5 dB | No preprocessing | Root-MUSIC | 8.2359 |
