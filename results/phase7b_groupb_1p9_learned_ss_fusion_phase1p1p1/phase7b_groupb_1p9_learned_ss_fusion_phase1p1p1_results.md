# Phase 7B Phase 1.1.1 - Group B 1.9 Lambda 1x1 SS-Fusion Primary Hard Cell

Phase 7B Phase 1.1.1 compares the new 1x1 channel-only learned SS-fusion candidate against the three learned baselines already established in the same primary coherent hard cell.

Experimental conditions:
- Phase: 1.1.1 controlled 1x1 channel-only fusion comparison
- Array: Group B 12-channel 2D hardware geometry
- Physical spacing: 1.9 lambda
- Signals: 2 coherent narrowband targets
- Cell: gap = 1 deg, SNR = 1 dB, T = 40
- Azimuth and elevation range: [-15 deg, 15 deg]
- Training scale: 45,000 samples total with 9,000 test samples
- Learned head: ESPRIT
- Fusion comparison: Phase 1.1 spatial fusion vs Phase 1.1.1 1x1 channel-only fusion
- Baselines: SS(3/3) and SS(2/3: rows 0+1)
- Metric: horizontal-angle RMSE in degrees (periodic matching)

| Algorithm | RMSE (deg) |
| --- | ---: |
| Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3 x 3) -> LRMC -> 1x1 learned fusion -> SubspaceNet | ESPRIT | 0.5414 |
| Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3 x 3) -> LRMC -> learned fusion -> SubspaceNet | ESPRIT | 0.4516 |
| Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 0+1) -> LRMC -> SubspaceNet | ESPRIT | 0.6995 |
| Coherent | Gap = 1 deg | SNR = 1 dB | SS(3/3) -> LRMC -> SubspaceNet | ESPRIT | 0.4747 |
