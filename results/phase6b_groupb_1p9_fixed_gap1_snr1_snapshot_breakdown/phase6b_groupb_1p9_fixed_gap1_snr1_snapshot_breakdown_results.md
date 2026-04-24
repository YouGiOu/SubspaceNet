# Phase 6B - Group B 1.9 Lambda Hard-Regime Snapshot Breakdown

Phase 6B sweeps snapshots in the hardest currently targeted Group B regime (fixed gap = 1 deg, fixed SNR = 1 dB) and compares raw classical controls, SS -> LRMC classical controls, and SS -> LRMC -> SubspaceNet -> ESPRIT.

Experimental conditions:
- Array: Group B 12-channel 2D hardware geometry
- Physical spacing: 1.9 lambda
- Signals: coherent and non-coherent narrowband targets
- Snapshots sweep: T = 1, 2, 4, 8, 16, 25
- Fixed azimuth separation: 1 deg
- Fixed SNR: 1 dB
- Learned target: SS -> LRMC -> SubspaceNet -> ESPRIT
- Control branches: raw classical and SS -> LRMC classical
- Control methods: DBF, MUSIC, Root-MUSIC, ESPRIT
- Dataset size per cell: 45,000 samples
- Metric: horizontal-angle RMSE in degrees (periodic matching)

| Geometry | Processing | Method | RMSE (deg) |
| --- | --- | --- | ---: |
| coherent | T = 1 | SS -> LRMC | DBF | 8.1158 |
| coherent | T = 1 | SS -> LRMC | ESPRIT | 7.8429 |
| coherent | T = 1 | SS -> LRMC | MUSIC | 8.0477 |
| coherent | T = 1 | SS -> LRMC | Root-MUSIC | 8.0012 |
| coherent | T = 1 | SS -> LRMC -> SubspaceNet | ESPRIT | 2.6079 |
| coherent | T = 1 | raw sample | DBF | 8.3314 |
| coherent | T = 1 | raw sample | ESPRIT | 10.2962 |
| coherent | T = 1 | raw sample | MUSIC | 8.2260 |
| coherent | T = 1 | raw sample | Root-MUSIC | 10.4034 |
| coherent | T = 16 | SS -> LRMC | DBF | 7.7773 |
| coherent | T = 16 | SS -> LRMC | ESPRIT | 6.9183 |
| coherent | T = 16 | SS -> LRMC | MUSIC | 7.8612 |
| coherent | T = 16 | SS -> LRMC | Root-MUSIC | 7.4121 |
| coherent | T = 16 | SS -> LRMC -> SubspaceNet | ESPRIT | 0.5461 |
| coherent | T = 16 | raw sample | DBF | 7.8434 |
| coherent | T = 16 | raw sample | ESPRIT | 10.4637 |
| coherent | T = 16 | raw sample | MUSIC | 7.3892 |
| coherent | T = 16 | raw sample | Root-MUSIC | 10.4789 |
| coherent | T = 2 | SS -> LRMC | DBF | 7.8710 |
| coherent | T = 2 | SS -> LRMC | ESPRIT | 7.4860 |
| coherent | T = 2 | SS -> LRMC | MUSIC | 7.8136 |
| coherent | T = 2 | SS -> LRMC | Root-MUSIC | 7.7083 |
| coherent | T = 2 | SS -> LRMC -> SubspaceNet | ESPRIT | 1.4497 |
| coherent | T = 2 | raw sample | DBF | 7.9539 |
| coherent | T = 2 | raw sample | ESPRIT | 10.5194 |
| coherent | T = 2 | raw sample | MUSIC | 8.1116 |
| coherent | T = 2 | raw sample | Root-MUSIC | 10.4480 |
| coherent | T = 25 | SS -> LRMC | DBF | 7.8026 |
| coherent | T = 25 | SS -> LRMC | ESPRIT | 6.7288 |
| coherent | T = 25 | SS -> LRMC | MUSIC | 7.7749 |
| coherent | T = 25 | SS -> LRMC | Root-MUSIC | 7.2592 |
| coherent | T = 25 | SS -> LRMC -> SubspaceNet | ESPRIT | 0.4901 |
| coherent | T = 25 | raw sample | DBF | 7.7547 |
| coherent | T = 25 | raw sample | ESPRIT | 10.3952 |
| coherent | T = 25 | raw sample | MUSIC | 7.3971 |
| coherent | T = 25 | raw sample | Root-MUSIC | 10.4179 |
| coherent | T = 4 | SS -> LRMC | DBF | 7.7864 |
| coherent | T = 4 | SS -> LRMC | ESPRIT | 7.3318 |
| coherent | T = 4 | SS -> LRMC | MUSIC | 7.8027 |
| coherent | T = 4 | SS -> LRMC | Root-MUSIC | 7.6006 |
| coherent | T = 4 | SS -> LRMC -> SubspaceNet | ESPRIT | 0.8017 |
| coherent | T = 4 | raw sample | DBF | 7.8773 |
| coherent | T = 4 | raw sample | ESPRIT | 10.4599 |
| coherent | T = 4 | raw sample | MUSIC | 7.4979 |
| coherent | T = 4 | raw sample | Root-MUSIC | 10.4422 |
| coherent | T = 8 | SS -> LRMC | DBF | 7.7931 |
| coherent | T = 8 | SS -> LRMC | ESPRIT | 7.1708 |
| coherent | T = 8 | SS -> LRMC | MUSIC | 7.8149 |
| coherent | T = 8 | SS -> LRMC | Root-MUSIC | 7.5010 |
| coherent | T = 8 | SS -> LRMC -> SubspaceNet | ESPRIT | 0.6072 |
| coherent | T = 8 | raw sample | DBF | 7.8537 |
| coherent | T = 8 | raw sample | ESPRIT | 10.5416 |
| coherent | T = 8 | raw sample | MUSIC | 7.4630 |
| coherent | T = 8 | raw sample | Root-MUSIC | 10.5160 |
| non-coherent | T = 1 | SS -> LRMC | DBF | 7.7773 |
| non-coherent | T = 1 | SS -> LRMC | ESPRIT | 7.1228 |
| non-coherent | T = 1 | SS -> LRMC | MUSIC | 7.5339 |
| non-coherent | T = 1 | SS -> LRMC | Root-MUSIC | 7.3776 |
| non-coherent | T = 1 | SS -> LRMC -> SubspaceNet | ESPRIT | 2.0599 |
| non-coherent | T = 1 | raw sample | DBF | 8.2889 |
| non-coherent | T = 1 | raw sample | ESPRIT | 10.1725 |
| non-coherent | T = 1 | raw sample | MUSIC | 8.0989 |
| non-coherent | T = 1 | raw sample | Root-MUSIC | 10.4085 |
| non-coherent | T = 16 | SS -> LRMC | DBF | 7.6470 |
| non-coherent | T = 16 | SS -> LRMC | ESPRIT | 5.5743 |
| non-coherent | T = 16 | SS -> LRMC | MUSIC | 7.5502 |
| non-coherent | T = 16 | SS -> LRMC | Root-MUSIC | 6.6129 |
| non-coherent | T = 16 | SS -> LRMC -> SubspaceNet | ESPRIT | 0.4217 |
| non-coherent | T = 16 | raw sample | DBF | 7.8451 |
| non-coherent | T = 16 | raw sample | ESPRIT | 8.3626 |
| non-coherent | T = 16 | raw sample | MUSIC | 6.4068 |
| non-coherent | T = 16 | raw sample | Root-MUSIC | 9.2692 |
| non-coherent | T = 2 | SS -> LRMC | DBF | 7.4996 |
| non-coherent | T = 2 | SS -> LRMC | ESPRIT | 6.5252 |
| non-coherent | T = 2 | SS -> LRMC | MUSIC | 7.2350 |
| non-coherent | T = 2 | SS -> LRMC | Root-MUSIC | 6.9242 |
| non-coherent | T = 2 | SS -> LRMC -> SubspaceNet | ESPRIT | 1.0701 |
| non-coherent | T = 2 | raw sample | DBF | 7.9353 |
| non-coherent | T = 2 | raw sample | ESPRIT | 9.8433 |
| non-coherent | T = 2 | raw sample | MUSIC | 7.8594 |
| non-coherent | T = 2 | raw sample | Root-MUSIC | 10.3159 |
| non-coherent | T = 25 | SS -> LRMC | DBF | 7.8183 |
| non-coherent | T = 25 | SS -> LRMC | ESPRIT | 5.4475 |
| non-coherent | T = 25 | SS -> LRMC | MUSIC | 7.7376 |
| non-coherent | T = 25 | SS -> LRMC | Root-MUSIC | 6.7142 |
| non-coherent | T = 25 | SS -> LRMC -> SubspaceNet | ESPRIT | 0.4082 |
| non-coherent | T = 25 | raw sample | DBF | 7.7989 |
| non-coherent | T = 25 | raw sample | ESPRIT | 8.1786 |
| non-coherent | T = 25 | raw sample | MUSIC | 6.1941 |
| non-coherent | T = 25 | raw sample | Root-MUSIC | 8.9545 |
| non-coherent | T = 4 | SS -> LRMC | DBF | 7.4995 |
| non-coherent | T = 4 | SS -> LRMC | ESPRIT | 6.2014 |
| non-coherent | T = 4 | SS -> LRMC | MUSIC | 7.2084 |
| non-coherent | T = 4 | SS -> LRMC | Root-MUSIC | 6.6924 |
| non-coherent | T = 4 | SS -> LRMC -> SubspaceNet | ESPRIT | 0.6317 |
| non-coherent | T = 4 | raw sample | DBF | 7.8831 |
| non-coherent | T = 4 | raw sample | ESPRIT | 9.4534 |
| non-coherent | T = 4 | raw sample | MUSIC | 7.0766 |
| non-coherent | T = 4 | raw sample | Root-MUSIC | 10.0725 |
| non-coherent | T = 8 | SS -> LRMC | DBF | 7.5418 |
| non-coherent | T = 8 | SS -> LRMC | ESPRIT | 5.8803 |
| non-coherent | T = 8 | SS -> LRMC | MUSIC | 7.4352 |
| non-coherent | T = 8 | SS -> LRMC | Root-MUSIC | 6.6561 |
| non-coherent | T = 8 | SS -> LRMC -> SubspaceNet | ESPRIT | 0.4708 |
| non-coherent | T = 8 | raw sample | DBF | 7.8808 |
| non-coherent | T = 8 | raw sample | ESPRIT | 8.9120 |
| non-coherent | T = 8 | raw sample | MUSIC | 6.5815 |
| non-coherent | T = 8 | raw sample | Root-MUSIC | 9.6753 |
