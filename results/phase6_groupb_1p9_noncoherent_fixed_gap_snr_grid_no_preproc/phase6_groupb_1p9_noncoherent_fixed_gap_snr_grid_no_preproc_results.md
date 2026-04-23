# Phase 6 - Group B 1.9 Lambda Non-Coherent Fixed-Gap and SNR Grid Without SS -> LRMC

This experiment evaluates the non-coherent Group B raw classical controls without SS -> LRMC preprocessing on the same fixed-gap and SNR grid used in the Phase 6 studies.

Experimental conditions:
- Array: Group B 12-channel 2D hardware geometry
- Physical spacing: 1.9 lambda
- Signals: 2 non-coherent narrowband targets
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
| Gap = 1 deg | SNR = 1 dB | No preprocessing | DBF | 7.8463 |
| Gap = 1 deg | SNR = 1 dB | No preprocessing | ESPRIT | 8.0267 |
| Gap = 1 deg | SNR = 1 dB | No preprocessing | MUSIC | 5.8624 |
| Gap = 1 deg | SNR = 1 dB | No preprocessing | Root-MUSIC | 8.6494 |
| Gap = 1 deg | SNR = 10 dB | No preprocessing | DBF | 7.8375 |
| Gap = 1 deg | SNR = 10 dB | No preprocessing | ESPRIT | 7.7602 |
| Gap = 1 deg | SNR = 10 dB | No preprocessing | MUSIC | 0.1215 |
| Gap = 1 deg | SNR = 10 dB | No preprocessing | Root-MUSIC | 7.6359 |
| Gap = 1 deg | SNR = 15 dB | No preprocessing | DBF | 7.8530 |
| Gap = 1 deg | SNR = 15 dB | No preprocessing | ESPRIT | 7.7626 |
| Gap = 1 deg | SNR = 15 dB | No preprocessing | MUSIC | 0.0985 |
| Gap = 1 deg | SNR = 15 dB | No preprocessing | Root-MUSIC | 7.6200 |
| Gap = 1 deg | SNR = 5 dB | No preprocessing | DBF | 7.8584 |
| Gap = 1 deg | SNR = 5 dB | No preprocessing | ESPRIT | 7.7619 |
| Gap = 1 deg | SNR = 5 dB | No preprocessing | MUSIC | 1.8226 |
| Gap = 1 deg | SNR = 5 dB | No preprocessing | Root-MUSIC | 7.7079 |
| Gap = 2 deg | SNR = 1 dB | No preprocessing | DBF | 7.2997 |
| Gap = 2 deg | SNR = 1 dB | No preprocessing | ESPRIT | 7.6830 |
| Gap = 2 deg | SNR = 1 dB | No preprocessing | MUSIC | 0.3420 |
| Gap = 2 deg | SNR = 1 dB | No preprocessing | Root-MUSIC | 7.5595 |
| Gap = 2 deg | SNR = 10 dB | No preprocessing | DBF | 7.5517 |
| Gap = 2 deg | SNR = 10 dB | No preprocessing | ESPRIT | 7.6597 |
| Gap = 2 deg | SNR = 10 dB | No preprocessing | MUSIC | 0.0968 |
| Gap = 2 deg | SNR = 10 dB | No preprocessing | Root-MUSIC | 7.3257 |
| Gap = 2 deg | SNR = 15 dB | No preprocessing | DBF | 7.5642 |
| Gap = 2 deg | SNR = 15 dB | No preprocessing | ESPRIT | 7.6568 |
| Gap = 2 deg | SNR = 15 dB | No preprocessing | MUSIC | 0.0943 |
| Gap = 2 deg | SNR = 15 dB | No preprocessing | Root-MUSIC | 7.3043 |
| Gap = 2 deg | SNR = 5 dB | No preprocessing | DBF | 7.4167 |
| Gap = 2 deg | SNR = 5 dB | No preprocessing | ESPRIT | 7.6602 |
| Gap = 2 deg | SNR = 5 dB | No preprocessing | MUSIC | 0.1157 |
| Gap = 2 deg | SNR = 5 dB | No preprocessing | Root-MUSIC | 7.3458 |
| Gap = 3 deg | SNR = 1 dB | No preprocessing | DBF | 0.9667 |
| Gap = 3 deg | SNR = 1 dB | No preprocessing | ESPRIT | 8.0794 |
| Gap = 3 deg | SNR = 1 dB | No preprocessing | MUSIC | 0.1445 |
| Gap = 3 deg | SNR = 1 dB | No preprocessing | Root-MUSIC | 7.5363 |
| Gap = 3 deg | SNR = 10 dB | No preprocessing | DBF | 0.5391 |
| Gap = 3 deg | SNR = 10 dB | No preprocessing | ESPRIT | 8.0353 |
| Gap = 3 deg | SNR = 10 dB | No preprocessing | MUSIC | 0.0967 |
| Gap = 3 deg | SNR = 10 dB | No preprocessing | Root-MUSIC | 7.2976 |
| Gap = 3 deg | SNR = 15 dB | No preprocessing | DBF | 0.5390 |
| Gap = 3 deg | SNR = 15 dB | No preprocessing | ESPRIT | 8.0314 |
| Gap = 3 deg | SNR = 15 dB | No preprocessing | MUSIC | 0.0937 |
| Gap = 3 deg | SNR = 15 dB | No preprocessing | Root-MUSIC | 7.2939 |
| Gap = 3 deg | SNR = 5 dB | No preprocessing | DBF | 0.6007 |
| Gap = 3 deg | SNR = 5 dB | No preprocessing | ESPRIT | 8.0444 |
| Gap = 3 deg | SNR = 5 dB | No preprocessing | MUSIC | 0.1060 |
| Gap = 3 deg | SNR = 5 dB | No preprocessing | Root-MUSIC | 7.3506 |
| Gap = 4 deg | SNR = 1 dB | No preprocessing | DBF | 0.4664 |
| Gap = 4 deg | SNR = 1 dB | No preprocessing | ESPRIT | 8.5958 |
| Gap = 4 deg | SNR = 1 dB | No preprocessing | MUSIC | 0.1216 |
| Gap = 4 deg | SNR = 1 dB | No preprocessing | Root-MUSIC | 7.3223 |
| Gap = 4 deg | SNR = 10 dB | No preprocessing | DBF | 0.1839 |
| Gap = 4 deg | SNR = 10 dB | No preprocessing | ESPRIT | 8.6112 |
| Gap = 4 deg | SNR = 10 dB | No preprocessing | MUSIC | 0.0912 |
| Gap = 4 deg | SNR = 10 dB | No preprocessing | Root-MUSIC | 7.2278 |
| Gap = 4 deg | SNR = 15 dB | No preprocessing | DBF | 0.1873 |
| Gap = 4 deg | SNR = 15 dB | No preprocessing | ESPRIT | 8.6080 |
| Gap = 4 deg | SNR = 15 dB | No preprocessing | MUSIC | 0.0911 |
| Gap = 4 deg | SNR = 15 dB | No preprocessing | Root-MUSIC | 7.2307 |
| Gap = 4 deg | SNR = 5 dB | No preprocessing | DBF | 0.2177 |
| Gap = 4 deg | SNR = 5 dB | No preprocessing | ESPRIT | 8.6244 |
| Gap = 4 deg | SNR = 5 dB | No preprocessing | MUSIC | 0.0971 |
| Gap = 4 deg | SNR = 5 dB | No preprocessing | Root-MUSIC | 7.2279 |
| Gap = 5 deg | SNR = 1 dB | No preprocessing | DBF | 1.1572 |
| Gap = 5 deg | SNR = 1 dB | No preprocessing | ESPRIT | 7.5544 |
| Gap = 5 deg | SNR = 1 dB | No preprocessing | MUSIC | 0.1447 |
| Gap = 5 deg | SNR = 1 dB | No preprocessing | Root-MUSIC | 7.0697 |
| Gap = 5 deg | SNR = 10 dB | No preprocessing | DBF | 0.6629 |
| Gap = 5 deg | SNR = 10 dB | No preprocessing | ESPRIT | 7.5419 |
| Gap = 5 deg | SNR = 10 dB | No preprocessing | MUSIC | 0.0951 |
| Gap = 5 deg | SNR = 10 dB | No preprocessing | Root-MUSIC | 7.0413 |
| Gap = 5 deg | SNR = 15 dB | No preprocessing | DBF | 0.6619 |
| Gap = 5 deg | SNR = 15 dB | No preprocessing | ESPRIT | 7.5389 |
| Gap = 5 deg | SNR = 15 dB | No preprocessing | MUSIC | 0.0905 |
| Gap = 5 deg | SNR = 15 dB | No preprocessing | Root-MUSIC | 7.0409 |
| Gap = 5 deg | SNR = 5 dB | No preprocessing | DBF | 0.7174 |
| Gap = 5 deg | SNR = 5 dB | No preprocessing | ESPRIT | 7.5505 |
| Gap = 5 deg | SNR = 5 dB | No preprocessing | MUSIC | 0.1038 |
| Gap = 5 deg | SNR = 5 dB | No preprocessing | Root-MUSIC | 7.0473 |
