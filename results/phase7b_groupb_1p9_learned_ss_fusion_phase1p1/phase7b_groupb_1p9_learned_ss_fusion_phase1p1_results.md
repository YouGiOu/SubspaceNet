# Phase 7B Phase 1.1 - Group B 1.9 Lambda Learned SS-Fusion Primary Hard Cell

Phase 7B Phase 1.1 compares the primary coherent hard-cell learned SS-fusion candidate against the current SS(3/3) learned baseline and the best fixed SS(2/3: rows 0+1) learned baseline.

Experimental conditions:
- Phase: 1.1 primary hard-cell reproduction
- Array: Group B 12-channel 2D hardware geometry
- Physical spacing: 1.9 lambda
- Signals: 2 coherent narrowband targets
- Cell: gap = 1 deg, SNR = 1 dB, T = 40
- Azimuth and elevation range: [-15 deg, 15 deg]
- Training scale: 45,000 samples total with 9,000 test samples
- Learned head: ESPRIT
- Candidate model: SubspaceNetSSFusionEspritPhase1p1
- Fixed learned baselines: SS(3/3) and SS(2/3: rows 0+1)
- Metric: horizontal-angle RMSE in degrees (periodic matching)

| Algorithm | RMSE (deg) |
| --- | ---: |
| Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3 x 3) -> LRMC -> learned fusion -> SubspaceNet | ESPRIT | 0.4516 |
| Coherent | Gap = 1 deg | SNR = 1 dB | SS(2/3: rows 0+1) -> LRMC -> SubspaceNet | ESPRIT | 0.6995 |
| Coherent | Gap = 1 deg | SNR = 1 dB | SS(3/3) -> LRMC -> SubspaceNet | ESPRIT | 0.4747 |
